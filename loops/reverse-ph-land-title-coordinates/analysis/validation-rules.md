# Validation Rules — Philippine Land Title Coordinate Engine

**Aspect:** validation-rules (Wave 2)
**Date:** 2026-02-26
**Depends on:** traverse-algorithm, traverse-computation-references, text-parser-grammar, prs92-datum-parameters (all Wave 1–2)
**Verification:** All formulas cross-checked against ≥2 independent sources via subagent (see §8)

---

## 1. Overview

The validation layer runs after the traverse computation and before the datum transformation. It answers: *Is this traverse result trustworthy?* It does NOT correct the data — it flags problems.

**Pipeline position:**
```
Parser → Traverse → [Validation] → Datum Transform → WGS84 output
                        ↓
              validation_result: {
                  closure_status,
                  area_status,
                  angular_status,
                  geometry_status,
                  warnings[],
                  errors[]
              }
```

**Design principle:** The engine faithfully reproduces the polygon described in the title. Validation detects anomalies but never silently alters the data. Every validation check returns a status (`pass`, `warn`, `fail`) with a numeric result and a human-readable message.

---

## 2. Validation Check 1: Linear Closure Error

The primary quality metric for a closed traverse. Measures how well the polygon closes back to Corner 1.

### Formulas

```
eN = Σ ΔNᵢ    (sum of all polygon leg ΔN; should be 0)
eE = Σ ΔEᵢ    (sum of all polygon leg ΔE; should be 0)

e = √(eN² + eE²)     [linear misclosure, meters]
P = Σ distanceᵢ       [perimeter, meters]
k = P / e             [precision denominator; higher = better]

Relative precision = 1 : k
```

**Equivalent check (using computed coordinates):**
```
eN = N_(n+1)_computed − N₁
eE = E_(n+1)_computed − E₁
```

### Tolerance Thresholds

**Regulatory basis:** DENR DAO 2007-29 §29 requires lot surveys to meet tertiary control accuracy. Tertiary control linear error per §28(b): not to exceed 1:5,000.

| Threshold | Precision (1:k) | Action | Basis |
|-----------|-----------------|--------|-------|
| PASS | k ≥ 5,000 | Proceed normally | DAO 2007-29 §28(b) Tertiary = 1:5,000 |
| WARN | 3,000 ≤ k < 5,000 | Proceed with warning flag | Engine-defined practical threshold (older/rural surveys) |
| FLAG | 1,000 ≤ k < 3,000 | Output with quality caveat | Engine-defined; possible transcription error |
| FAIL | k < 1,000 | Do not output coordinates | Engine-defined; data not usable |

**Note on the 1:3,000 WARN threshold:** DAO 2007-29 §30 states isolated surveys must also meet tertiary control accuracy (1:5,000). The 1:3,000 warn threshold is NOT a regulatory standard — it is an engine-defined practical relaxation to handle older pre-PRS92 surveys where original precision was lower. It was previously attributed to DAO 2007-29 in this project's Wave 1 analysis but is corrected here.

**Note on k → ∞:** If e = 0 (perfect closure — possible with short, simple lots in full-precision computation), set k = ∞ and status = PASS.

### Edge case: very short perimeter

For a lot with perimeter P = 40 m, even a small closure error of e = 0.01 m yields k = 4,000 (WARN). Short-perimeter lots are sensitive to rounding in the original survey. The engine should include the absolute misclosure (e in meters) alongside the ratio to help the caller assess significance. An e < 0.05 m with k ≥ 1,000 is generally acceptable regardless of the ratio.

### Output schema

```json
{
  "closure": {
    "eN_m": -0.012,
    "eE_m": -0.008,
    "e_m": 0.014,
    "perimeter_m": 92.05,
    "precision_denom": 6575,
    "ratio_str": "1:6575",
    "status": "pass",
    "message": "Closure 1:6,575 meets tertiary standard (1:5,000)"
  }
}
```

---

## 3. Validation Check 2: Area Cross-Check

Compares the computed polygon area (from the shoelace formula) against the stated area in the technical description.

### Formula

**Shoelace area** (with coordinate shift for floating-point stability):

```python
N_min = min(Nᵢ)
E_min = min(Eᵢ)
n_adj = [Nᵢ - N_min for each corner]
e_adj = [Eᵢ - E_min for each corner]

two_A = Σᵢ (e_adj[i] × n_adj[(i+1) % n] - e_adj[(i+1) % n] × n_adj[i])
computed_area_sqm = |two_A| / 2.0
```

**Discrepancy:**
```
diff_sqm = |computed_area_sqm - stated_area_sqm|
diff_pct = (diff_sqm / stated_area_sqm) × 100
```

### Tolerance Thresholds

There is no specific DENR regulation for the discrepancy between computed-from-bearings area and stated area in a technical description. The closest regulatory reference is DAO 2007-29 §30(b) for relocation/verification surveys: ±1 sq m per hectare (0.01%). However, that applies to re-survey vs. original, not to computational reproduction from bearings/distances.

The computed-vs-stated discrepancy arises from:
1. Rounding in original DMS bearings (minutes truncated/rounded)
2. Rounding in distances (typically to nearest cm)
3. The original surveyor's Bowditch adjustment (shifts corners slightly from stated bearings)
4. Area stated to nearest integer sq m (typical for older titles)

**Engine-defined thresholds:**

| Threshold | Discrepancy | Action | Rationale |
|-----------|------------|--------|-----------|
| PASS | ≤ 0.5% | No flag | Normal computational rounding |
| WARN | 0.5% < diff ≤ 2.0% | Warning flag | Common in pre-GNSS surveys; rounding artifacts |
| FLAG | 2.0% < diff ≤ 5.0% | Quality caveat | Possible transcription error or incomplete parsing |
| FAIL | > 5.0% | Error flag | Likely data error; missing legs, wrong BLLM, or parse failure |

**Absolute floor:** For very small lots (< 100 sq m), a ≤ 1 sq m absolute difference overrides the percentage check to avoid false flags from percentage amplification.

### Output schema

```json
{
  "area_check": {
    "computed_sqm": 484.85,
    "stated_sqm": 485.0,
    "diff_sqm": 0.15,
    "diff_pct": 0.03,
    "status": "pass",
    "message": "Area discrepancy 0.03% (0.15 m²) within tolerance"
  }
}
```

---

## 4. Validation Check 3: Angular Closure (Interior Angle Sum)

Verifies that the interior angles of the closed polygon sum to the theoretical value.

### Formulas

**Theoretical sum of interior angles:**
```
θ_theoretical = (n - 2) × 180°
```
where n = number of corners (= number of polygon legs).

**Interior angle at corner i:**
The interior angle at corner i is the deflection between the incoming and outgoing traverse legs. Given azimuths:
```
incoming_az = azimuth of leg (i-1 → i)
outgoing_az = azimuth of leg (i → i+1)

# Interior angle (for a clockwise-wound polygon with right-turn convention):
angle_i = incoming_az - outgoing_az + 180°

# Normalize to 0–360° range:
angle_i = angle_i mod 360°
```

**Alternative (more robust) computation using reverse azimuth:**
```
reverse_az = (incoming_az + 180°) mod 360°
angle_i = outgoing_az - reverse_az
if angle_i < 0: angle_i += 360°
```

This gives the interior angle measured clockwise from the reverse of the incoming leg to the outgoing leg. For a convex polygon traversed counter-clockwise (standard Philippine TD convention), this yields the interior angle directly.

**Angular misclosure:**
```
θ_measured = Σ angle_i
angular_misclosure = |θ_measured - θ_theoretical|
```

### Why this check is secondary for the engine

Unlike field surveys where angles are independently measured, the engine computes angles from the same bearings used for the traverse. If the bearings and distances produce a reasonable linear closure, the angular closure is automatically consistent. However, the angular check catches:

1. **Parse errors** — a misread bearing flips a quadrant, causing a large angular anomaly
2. **Missing legs** — if a leg was dropped, the angle sum will be wrong
3. **Concavity detection** — interior angles > 180° indicate a concave polygon, which the engine must handle correctly in area computation

### Tolerance Thresholds

**Regulatory basis:** DAO 2007-29 §28(b) specifies angular error for control surveys:
- Primary: 2.5″√n
- Secondary: 10″√n
- Tertiary (lot surveys): 30″√n

For the engine's purpose (computed from stated bearings, not field-measured angles), we use a relaxed threshold:

| Threshold | Angular Misclosure | Action |
|-----------|-------------------|--------|
| PASS | ≤ 30″√n | Consistent with field survey standards |
| WARN | 30″√n < misc ≤ 1°×√n | Possible bearing rounding; investigate |
| FAIL | > 1°×√n or any angle < 0° or > 360° | Parse error or data corruption |

**Practical note:** For titles with bearings stated to the nearest minute (typical), each bearing has ±0.5′ rounding error. Over n legs, the angular misclosure from rounding alone can be up to n × 1′. For a 10-corner lot: up to 10′ (600″) misclosure from rounding. The 30″√n formula at n=10 gives 95″ ≈ 1.6′. So bearing-rounding misclosure will often exceed the field-survey angular tolerance. The engine should evaluate angular closure primarily as a **sanity check** (catching gross errors > 1°) rather than as a precision metric.

### Output schema

```json
{
  "angular_check": {
    "n_corners": 4,
    "theoretical_sum_deg": 360.0,
    "computed_sum_deg": 359.983,
    "misclosure_deg": 0.017,
    "misclosure_arcsec": 61.2,
    "threshold_arcsec": 60.0,
    "status": "pass",
    "message": "Angular misclosure 61.2\" within field tolerance 30\"√4 = 60\""
  }
}
```

---

## 5. Validation Check 4: Geometry Sanity Checks

A set of quick structural checks that catch data problems before full computation.

### 5.1 Minimum Corner Count

```
if n_corners < 3: FAIL "Polygon requires at least 3 corners"
```

### 5.2 Bearing Range Validity

For quadrant bearings, the angle β must be in [0°, 90°]:
```
if bearing.deg > 90: WARN "Bearing angle exceeds 90° — invalid for quadrant bearing"
if bearing.deg == 90 and bearing.min > 0: same warning
```

**Exception:** "Due North" (0°), "Due East" (90°), "Due South" (180°), "Due West" (270°) are valid as azimuths. The parser handles these separately.

After conversion to azimuth, valid range is [0°, 360°):
```
if azimuth < 0 or azimuth >= 360: FAIL "Azimuth out of range"
```

### 5.3 Distance Positivity

```
if distance_m <= 0: FAIL "Distance must be positive"
if distance_m < 0.01: WARN "Distance < 1 cm — possible parse error"
```

### 5.4 Winding Order Consistency

The shoelace formula's signed area indicates winding:
- Positive signed area → counter-clockwise (CCW) winding
- Negative signed area → clockwise (CW) winding

Philippine TDs conventionally traverse lots clockwise when viewed on a north-up plan. However, winding order does not affect correctness — the shoelace formula uses `abs()`. This check is informational only:

```json
{
  "winding": "CW",
  "note": "Standard Philippine convention"
}
```

### 5.5 Self-Intersection Detection

A self-intersecting polygon has undefined area and indicates a data error. Check: do any non-adjacent polygon edges cross?

**Algorithm:** For each pair of non-adjacent edges, test for intersection using the standard 2D line segment intersection test. For n edges, this is O(n²). Given typical lot sizes (4–20 corners), this is negligible.

```python
def segments_intersect(p1, p2, p3, p4):
    """Test if segment p1-p2 intersects segment p3-p4."""
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return False  # Collinear cases omitted for simplicity
```

**Action on self-intersection:** FAIL — polygon is invalid. Most likely cause: bearing misparse (wrong quadrant) or missing corner.

### 5.6 Duplicate Consecutive Corners

If two consecutive corners have identical (or near-identical) coordinates:
```
if distance(corner_i, corner_{i+1}) < 0.001 m: WARN "Duplicate consecutive corners"
```

### Output schema

```json
{
  "geometry": {
    "n_corners": 4,
    "min_corners_check": "pass",
    "bearing_range_check": "pass",
    "distance_positivity_check": "pass",
    "winding": "CW",
    "self_intersection_check": "pass",
    "duplicate_corners_check": "pass",
    "status": "pass"
  }
}
```

---

## 6. Validation Check 5: BLLM Resolution Confidence

The BLLM coordinates are the absolute anchor. Their quality determines the absolute accuracy of all corner coordinates.

### Checks

| Check | Condition | Action |
|-------|-----------|--------|
| BLLM found in database | Name matched after normalization | INFO |
| BLLM not found | No match after 3-tier lookup | ERROR: `BLLMNotFound` |
| Ambiguous match | Multiple records match | ERROR: `AmbiguousBLLM` |
| Caller-provided BLLM | Coordinates supplied externally | INFO: mark as `caller_provided` |
| Datum mismatch | BLLM datum ≠ title datum | WARN: document accuracy impact |
| Zone inference | Zone assigned via province lookup | INFO: record inferred zone |
| Zone mismatch | Inferred zone ≠ BLLM zone | ERROR: coordinate system inconsistency |

### Confidence levels

```
high:    BLLM found, single match, PRS92 datum, zone confirmed
medium:  BLLM found, single match, Luzon 1911 datum (shift applied)
low:     BLLM found but ambiguous match resolved by province filter
manual:  Caller-provided coordinates (accuracy unknown)
none:    BLLM not found (engine cannot proceed without coordinates)
```

### Output schema

```json
{
  "bllm_resolution": {
    "query": "BLLM NO. 1, PLS-1110",
    "match_status": "found",
    "match_count": 1,
    "confidence": "medium",
    "datum": "luzon1911",
    "zone": 3,
    "zone_source": "province_lookup",
    "northing_m": 1882450.000,
    "easting_m": 447320.000,
    "warnings": ["BLLM datum is Luzon 1911; shift to PRS92 applied with ~10m uncertainty"]
  }
}
```

---

## 7. Validation Check 6: Datum and Bearing Type Consistency

Cross-checks between the inferred datum, bearing type, survey date, and zone.

### Rules

| # | Rule | Condition | Action |
|---|------|-----------|--------|
| 1 | Grid bearing requires zone | bearing_type = "grid" and zone is unknown | ERROR |
| 2 | Pre-1993 survey = Luzon 1911 default | survey_date < 1993-06 and no explicit PRS92 label | INFO: assume Luzon 1911 |
| 3 | Post-2010 survey = PRS92 default | survey_date ≥ 2010 and no explicit datum label | INFO: assume PRS92 |
| 4 | Ambiguous era (1993–2010) | Survey date in transition period | WARN: datum uncertain |
| 5 | True bearing + datum transform | bearing_type = "true" means bearings reference geographic north, not grid north | INFO: no grid-to-true correction needed |
| 6 | BLLM datum vs title datum | BLLM in Luzon 1911 but title inferred PRS92 (or vice versa) | WARN: datum mismatch |

### Output schema

```json
{
  "datum_consistency": {
    "bearing_type": "grid",
    "inferred_datum": "luzon1911",
    "survey_date": "1983",
    "zone": 3,
    "status": "pass",
    "warnings": [],
    "notes": ["Pre-1993 grid bearings → Luzon 1911 PTM Zone 3 assumed"]
  }
}
```

---

## 8. Verification Summary

All validation formulas and thresholds were cross-checked via subagent against ≥2 independent sources.

| Formula / Threshold | Status | Sources |
|---------------------|--------|---------|
| Linear misclosure: e = √(eN² + eE²), k = P/e | **CONFIRMED** | KFUPM CE260 lecture notes; U. Washington GIS course; Engineering Training Publication |
| Angular misclosure: θ = (n−2)×180°, C = k√n | **CONFIRMED** | Jerrymahun Ch. B; School of PE; Chegg worked examples |
| PH angular tolerance: 30″√n (tertiary/lot) | **CONFIRMED** | DAO 2007-29 §28(b) via Quizlet flashcards; Course Hero §28b; Scribd DAO PDF |
| Shoelace area + coordinate shift | **CONFIRMED** | Wikipedia Shoelace Formula; John D. Cook "Surveyor's Formula"; Rosetta Code |
| PH lot survey linear tolerance: 1:5,000 | **CONFIRMED** | DAO 2007-29 §29 (lot = tertiary); Quizlet; Course Hero |
| Bowditch: corr_i = −e × (Lᵢ/P) | **CONFIRMED** | Jerrymahun Ch. E; Esri GIS Dictionary; HK PolyU glossary |
| Non-default Bowditch for title reproduction | **CONFIRMED** | RPLS.com professional forum; McKissock retracement guidance; ALTA survey principles |
| Area tolerance: ≤0.5% pass, ≤2% warn | **Engine-defined** | No specific DENR % for computed-vs-stated; DAO 2007-29 §30(b) has ±1 sq m / ha for relocation only |

### Conflict found and resolved

**1:3,000 rural tolerance:** Previously attributed to DAO 2007-29 in this project's Wave 1 analysis (`traverse-computation-references.md`). Subagent verification found **no 1:3,000 threshold in DAO 2007-29**. Section 30 states isolated surveys must meet tertiary control accuracy = 1:5,000. The 1:3,000 value may originate from older DENR manuals (DAO 98-12 or predecessors). The engine retains 1:3,000 as a WARN threshold (not PASS) to accommodate older surveys, but it is now documented as **engine-defined, not regulatory**.

**Control survey tier labels:** The Wave 1 analysis stated "Primary 1:10,000, Secondary 1:5,000." Subagent verification corrected this: Primary = 1:20,000 (3rd order), Secondary = 1:10,000 (4th order), Tertiary = 1:5,000. This does not affect the engine's lot survey thresholds (which use the tertiary value) but is documented here for reference accuracy.

---

## 9. Complete Validation Output Schema

```json
{
  "validation": {
    "closure": {
      "eN_m": -0.012,
      "eE_m": -0.008,
      "e_m": 0.014,
      "perimeter_m": 92.05,
      "precision_denom": 6575,
      "ratio_str": "1:6575",
      "status": "pass",
      "message": "Closure 1:6,575 meets tertiary standard (1:5,000)"
    },
    "area_check": {
      "computed_sqm": 484.85,
      "stated_sqm": 485.0,
      "diff_sqm": 0.15,
      "diff_pct": 0.03,
      "status": "pass",
      "message": "Area discrepancy 0.03% (0.15 m²) within tolerance"
    },
    "angular_check": {
      "n_corners": 4,
      "theoretical_sum_deg": 360.0,
      "computed_sum_deg": 359.983,
      "misclosure_deg": 0.017,
      "misclosure_arcsec": 61.2,
      "status": "pass",
      "message": "Angular misclosure within tolerance"
    },
    "geometry": {
      "n_corners": 4,
      "min_corners_check": "pass",
      "bearing_range_check": "pass",
      "distance_positivity_check": "pass",
      "winding": "CW",
      "self_intersection_check": "pass",
      "duplicate_corners_check": "pass",
      "status": "pass"
    },
    "bllm_resolution": {
      "confidence": "medium",
      "status": "found",
      "warnings": []
    },
    "datum_consistency": {
      "status": "pass",
      "warnings": []
    },
    "overall_status": "pass",
    "overall_confidence": "medium",
    "warnings": [],
    "errors": []
  }
}
```

**Overall status logic:**
```
if any check.status == "fail": overall = "fail"
elif any check.status == "flag": overall = "flag"
elif any check.status == "warn": overall = "warn"
else: overall = "pass"
```

**Overall confidence** = minimum of (bllm_resolution.confidence, closure quality, datum certainty).

---

## 10. Validation Decision Matrix

Summary of all thresholds for quick reference:

### Linear Closure

| k (precision denom) | Status | Action |
|---------------------|--------|--------|
| ≥ 5,000 | PASS | Proceed |
| 3,000–4,999 | WARN | Proceed with warning |
| 1,000–2,999 | FLAG | Output with quality caveat |
| < 1,000 | FAIL | Do not output coordinates |

### Area Discrepancy

| % difference | Status | Action |
|-------------|--------|--------|
| ≤ 0.5% | PASS | Proceed |
| 0.5%–2.0% | WARN | Common in older surveys |
| 2.0%–5.0% | FLAG | Investigate parse/data error |
| > 5.0% | FAIL | Likely data error |

### Angular Misclosure

| Misclosure | Status | Action |
|-----------|--------|--------|
| ≤ 30″√n | PASS | Consistent with field standards |
| 30″√n – 1°×√n | WARN | Bearing rounding effects |
| > 1°×√n or invalid angles | FAIL | Parse error or data corruption |

### BLLM Confidence

| Condition | Confidence | Action |
|-----------|-----------|--------|
| Single PRS92 match | High | Proceed |
| Single Luzon 1911 match | Medium | Proceed with datum note |
| Ambiguous, resolved by province | Low | Proceed with warning |
| Caller-provided | Manual | Mark as unverified |
| Not found | None | Cannot proceed |

---

## 11. Implementation Notes

### Validation is non-blocking by default

The engine should compute the traverse and output coordinates even when validation produces WARN or FLAG. Only FAIL status blocks output. The caller receives the full validation report and decides how to use flagged results.

### Validation order

Run checks in this order (fast checks first, expensive checks last):

1. Geometry sanity (O(1) per check except self-intersection)
2. BLLM resolution confidence (database lookup, already done)
3. Datum consistency (rule evaluation, O(1))
4. Linear closure (already computed by traverse algorithm)
5. Area cross-check (already computed by traverse algorithm)
6. Angular closure (requires computing interior angles from azimuths)
7. Self-intersection (O(n²), run last)

### Bowditch interaction

If `apply_bowditch=True`, the area cross-check should compare the Bowditch-adjusted area to the stated area (which should have better agreement since the original survey was also Bowditch-adjusted). Report both raw and adjusted areas.

### Coordinate precision

All validation computations use IEEE 754 double (64-bit float). Intermediate values are never rounded. Only the final output values are rounded for display:
- Coordinates: 3 decimal places (mm precision)
- Closure error: 3 decimal places
- Area: 2 decimal places
- Angles: 1 arcsecond precision

---

## Sources

### Primary (Philippine regulatory)
- DENR DAO 2007-29 — Revised Regulations on Land Surveys, §28(b) (traverse specifications), §29 (lot survey accuracy), §30 (isolated surveys): [Scribd](https://www.scribd.com/doc/33770276/DAO-2007-29), [LegalDex](https://legaldex.com/laws/revised-regulations-on-land-surveys)
- DENR DMC 2010-13 — Manual on Land Survey Procedures: [FAO Legal](https://faolex.fao.org/docs/pdf/phi152415.pdf), [Studocu](https://www.studocu.com/ph/document/andres-bonifacio-college/civil-engineering/manual-on-land-survey-procedures/99791185)
- DENR DAO 2010-17 — IVAS IRR (relocation survey area tolerance): [SC E-Library](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/52040)

### Traverse computation (cross-verification)
- Jerrymahun COGO Ch. A (bearing→azimuth): https://jerrymahun.com/index.php/home/open-access/12-iv-cogo/21-cogo-chap-a
- Jerrymahun Traverse Ch. B (angular misclosure): https://jerrymahun.com/index.php/home/open-access/17-trav-comps/41-travcomps-chap-b?showall=1
- Jerrymahun Traverse Ch. D (linear closure): https://jerrymahun.com/index.php/home/open-access/17-trav-comps/43-travcomps-chap-d
- Jerrymahun Traverse Ch. E (Bowditch adjustment): https://jerrymahun.com/index.php/home/open-access/17-trav-comps/44-travcomps-chap-e
- KFUPM CE260 lecture notes (linear misclosure formula): https://faculty.kfupm.edu.sa/ce/hawahab/WEBPAGE/CE260/NOTES/CH%206.pdf
- U. Washington GIS course (misclosure): http://gis.washington.edu/phurvitz/courses/esrm304/lectures/2009/Hurvitz/procedures/linear_misclosure.html
- School of PE (errors in surveying): https://schoolofpe.com/blogs/news/errors-in-surveying-how-to-identify-and-calculate-for-ca-surveying-exam-html

### Area computation (cross-verification)
- John D. Cook, "Surveyor's Formula for Polygon Area": https://www.johndcook.com/blog/2018/09/26/polygon-area/
- Wikipedia, Shoelace Formula: https://en.wikipedia.org/wiki/Shoelace_formula
- Rosetta Code, Shoelace Formula: https://rosettacode.org/wiki/Shoelace_formula_for_polygonal_area

### Philippine area discrepancy context
- Respicio & Co., "Lot Title vs. Lot Plan Discrepancy": https://www.lawyer-philippines.com/articles/lot-title-vs-lot-plan-discrepancy-resurvey-re-titling-and-remedies-under-property-law
- CREBA, "Technical errors in land titles": https://creba.ph/technical-errors-in-land-titles-detection-correction/

### DAO 2007-29 specific values (cross-verification)
- Quizlet, DAO 2007-29 Survey Accuracies: https://quizlet.com/434000634/dao-2007-29-survey-accuracies-flash-cards/
- Course Hero, Section 28b DAO 2007-29: https://www.coursehero.com/file/p7b9fecv/As-per-Section-28b-Project-Control-DAO-2007-29-the-accuracy-control-for-an-area/
- Studocu, DAO 2007-29: https://www.studocu.com/ph/document/nueva-vizcaya-state-university/geodetic-engineering/denr-administrative-order-no-2007-29-in-the-philippines/38055162

### Prior analyses in this loop
- `analysis/traverse-algorithm.md` — closure formulas, shoelace area, worked example
- `analysis/traverse-computation-references.md` — base formulas, Philippine tolerances
- `analysis/text-parser-grammar.md` — parser error codes, bearing validity
- `analysis/prs92-datum-parameters.md` — zone definitions for zone consistency check
- `analysis/luzon1911-to-prs92-transform.md` — datum detection logic for consistency check
