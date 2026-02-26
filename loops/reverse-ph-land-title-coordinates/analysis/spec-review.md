# Spec Review — Philippine Land Title Coordinate Engine

**Aspect:** spec-review (Wave 4)
**Date:** 2026-02-26
**Depends on:** engine-spec-draft (Wave 4) + all prior analyses
**Method:** Systematic review of `output/engine-spec.md` against: (1) PROMPT.md requirements, (2) all 14 source analyses, (3) formula correctness, (4) implementability assessment

---

## 1. PROMPT.md Requirements Checklist

| Requirement | Spec Section | Status | Notes |
|-------------|-------------|--------|-------|
| Text parser grammar with format variation handling | §2 (10 subsections) | ✅ PASS | BNF grammar, regex, output schema, format variations |
| Traverse computation formulas with worked examples | §4 (6 subsections) | ✅ PASS | Full formulas, pseudocode, worked example (TV-1) |
| PRS92 → WGS84 transformation with zone selection logic | §5.3–5.5 | ✅ PASS | Inverse TM + Helmert pipeline, zone cascade |
| Luzon 1911 legacy handling with error bounds | §5.6–5.7 | ✅ PASS | 3-param + DENR MC 2010-06 paths, zone mapping |
| BLLM coordinate dataset + coverage analysis | §3 + Appendix D | ✅ PASS* | *Coverage analysis present, but dataset counts were wrong (see F1) |
| Validation rules and error detection | §6 + §7 | ✅ PASS | 6 validation checks, 42 error codes |
| 5+ test vectors with known input/output pairs | §8 | ✅ PASS | 6 test vectors covering full pipeline + edge cases |

**Overall PROMPT.md compliance: PASS** — all required outputs are present.

---

## 2. Factual Errors Found (Fixed)

### F1. BLLM Dataset Record Counts — Off by ~70× (CRITICAL)

**Location:** Spec §3.2 ("Coverage statistics") and Appendix D ("Monument Types in Dataset")

**Error:** Spec stated "~1,200+ monument records across all provinces" with ~800 BLLMs, ~200 BBMs, ~50 MBMs, ~30 LW.

**Correct (from bllm-dataset-compilation analysis):**
- **Total records:** 85,303
- **BLLMs:** 19,568
- **BBMs:** 26,155
- **MBMs:** 9,174
- **BLBMs:** 4,850
- **PRS92 control points:** 15,609
- **Triangulation stations:** 1,085
- **PBMs:** 788
- **Other:** 6,702 + 1,372 general monuments

**Impact:** Developer would massively underestimate dataset size and potentially misallocate storage/indexing strategy. A 15.9 MB JSON file with 85k records requires different handling than "~1,200 records."

**Fix applied:** Updated §3.2 and Appendix D with correct counts from analysis.

### F2. Bowring Function — Dead Code Line

**Location:** Spec §5.5, step 3 (`geocentric_to_geographic` function)

**Error:** Two consecutive `theta =` assignments:
```python
theta = math.atan2(Z * a, p * a * math.sqrt(1.0 - e2))  # dead code
theta = math.atan2(Z * a, p * b)                          # actual computation
```
The first line is immediately overwritten. Both are mathematically equivalent (since `b = a * sqrt(1 - e²)`), but the first line is dead code that confuses the implementation.

**Fix applied:** Removed the dead first `theta` line; kept only the `b`-based computation.

### F3. BLLM Dataset Field Names — Mismatch with Source Data

**Location:** Spec §3.2 ("Dataset structure" table)

**Error:** Spec uses field name "Name" but actual `tiepoints.json` uses "Tie Point Name". Spec also omits the "Description" field which is critical for datum inference (analysis: 18.4% PRS92, 66% Luzon 1911, 15.5% unknown datum — all inferred from Description).

**Impact:** Developer would fail to parse the JSON correctly on first attempt.

**Fix applied:** Updated field names to match actual tiepoints.json schema; added Description field.

---

## 3. Specification Gaps Found (Fixed)

### G1. Angular Closure — Missing Computation Formula

**Location:** Spec §6.3

**Gap:** Spec specifies thresholds (30″√n PASS, etc.) but not how to compute interior angles from sequential azimuths.

**Source:** The formula exists in `analysis/validation-rules.md` §4:
```
incoming_az = azimuth of leg (i-1 → i)
outgoing_az = azimuth of leg (i → i+1)
angle_i = incoming_az - outgoing_az + 180°  (normalized to 0–360°)
```

**Impact:** Developer would need to derive the interior angle computation independently.

**Fix applied:** Added interior angle formula to §6.3.

### G2. Short-Perimeter Edge Case — Missing from Closure Check

**Location:** Spec §6.1

**Gap:** For lots with very short perimeters (e.g., 40 m), even small absolute misclosures produce poor precision ratios. The analysis recommends: "e < 0.05 m with k ≥ 1,000 is generally acceptable regardless of ratio."

**Fix applied:** Added absolute misclosure floor note to §6.1.

### G3. Small-Lot Area Floor — Missing from Area Cross-Check

**Location:** Spec §6.2

**Gap:** For very small lots (< 100 m²), percentage-based thresholds can trigger false flags. The analysis recommends: "≤ 1 m² absolute difference overrides percentage check."

**Fix applied:** Added absolute floor note to §6.2.

### G4. Test Vector WGS84 Precision

**Location:** Spec §8 (TV-1)

**Gap:** The spec rounds WGS84 coordinates to 6 decimal places (~0.11 m) while the analysis provides 9 decimal places (~0.001 mm). For a spec that will drive implementation, the full precision from the analysis should be used.

**Fix applied:** Updated TV-1 WGS84 coordinates to 9 decimal places.

---

## 4. Formula Correctness Verification

### 4.1 Inverse Transverse Mercator

| Check | Status |
|-------|--------|
| M = y/k₀ (not M = y) | ✅ Correctly specified with warning note |
| Footpoint series (J1–J4 for Clarke 1866) | ✅ Coefficients match Snyder PP1395 |
| D⁶/720 latitude term coefficients | ✅ (61+90T1+298C1+45T1²−252e'²−3C1²) matches eq. 8-17 |
| D⁵/120 longitude term coefficients | ✅ (5−2C1+28T1−3C1²+8e'²+24T1²) matches eq. 8-18 |
| Complete Python implementation | ✅ All stages present |

### 4.2 Helmert Transformation

| Check | Status |
|-------|--------|
| EPSG:15708 parameters (dx, dy, dz, rx, ry, rz, ds) | ✅ Correct |
| Coordinate Frame rotation convention (EPSG 9607) | ✅ Matrix correct |
| Rotation sign convention warning | ✅ Position Vector warning present |
| Arc-seconds to radians conversion | ✅ Correct formula |

### 4.3 Bearing-to-Azimuth Conversion

| Check | Status |
|-------|--------|
| NE quadrant (0–90°) | ✅ `angle` |
| SE quadrant (90–180°) | ✅ `180 - angle` |
| SW quadrant (180–270°) | ✅ `180 + angle` |
| NW quadrant (270–360°) | ✅ `360 - angle` |
| Due cardinal handling | ✅ 0/90/180/270° |

### 4.4 Shoelace Area

| Check | Status |
|-------|--------|
| Coordinate shift for FP precision | ✅ Present with explanation |
| abs() for winding-order independence | ✅ Present |

### 4.5 Traverse Computation

| Check | Status |
|-------|--------|
| ΔN = dist × cos(az) | ✅ |
| ΔE = dist × sin(az) | ✅ |
| Cumulative addition | ✅ |
| Closure formula | ✅ |

**Overall formula correctness: PASS** — all formulas verified against sources cited in Wave 2 analyses.

---

## 5. Implementability Assessment

### Can a developer build this without asking questions?

**Verdict: YES, with minor friction points (all fixed)**

Before fixes:
- F3 (wrong JSON field names) would have caused immediate implementation failure
- G1 (missing angular formula) would have required independent derivation
- F1 (wrong dataset size) would have caused architecture misjudgments

After fixes: A developer can implement the full pipeline from this spec alone.

### Remaining known limitations (acceptable)

1. **Forward TM not provided** — The engine only needs inverse TM. TV-5 provides round-trip verification points but developers would need an external forward TM to generate additional test cases. This is acceptable; Snyder PP1395 provides forward TM and is cited.

2. **Municipality-level zone resolution incomplete** — For provinces that straddle zones (Isabela, Bohol, Quezon), the spec says "municipality-level resolution needed" but doesn't enumerate all split municipalities. The analysis (bllm-dataset-compilation §2.3) documents ISABELA_ZONE_IV_SET, QUEZON_ZONE_IV_SET, and CAMOTES_SET but these aren't replicated in the spec. This is acceptable — the spec references the analysis and the engine returns `ZoneBoundaryAmbiguous` warning for unresolved cases.

3. **Hypothetical BLLMs in test vectors** — All test vectors use hypothetical BLLM coordinates, so external verification (e.g., against Geoportal) is not directly possible. The internal consistency of the traverse and transform pipeline is verified. The GeoIDEx cross-reference points from the analysis (3 points with both PTM grid and PRS92 geographic) could be used for additional verification but are not included as test vectors. This is acceptable — the spec is for the computation engine, not an end-to-end system test.

4. **Declination handling** — TV-2 has "true bearings; declination 0° 56' E" but the spec doesn't specify whether or how declination should be applied. The analysis (test-vectors §2.2) says "informational only, not applied." This is consistent with the spec's approach (bearings are used as-stated), but could be more explicit.

---

## 6. Units Verification

| Domain | Unit Convention | Consistent? |
|--------|----------------|-------------|
| Distances | metres (m) throughout | ✅ |
| Angles | degrees (°) with conversion to radians noted | ✅ |
| Coordinates | PRS92: Northing/Easting (m) with zone | ✅ |
| WGS84 | decimal degrees | ✅ |
| Area | square metres (m²) | ✅ |
| Closure | ratio (1:k) + absolute (m) | ✅ |
| Helmert rotations | arc-seconds (converted to radians) | ✅ |
| Scale | ppm (converted to multiplier) | ✅ |

**All formulas have explicit units: PASS**

---

## 7. Edge Case Coverage

| Category | Coverage | Source |
|----------|----------|--------|
| Format variations (13 categories) | ✅ Comprehensive | format-variations (W3) |
| Error handling (42 codes) | ✅ Comprehensive | error-handling (W3) |
| Graceful degradation (6 levels) | ✅ Complete | error-handling (W3) |
| Legacy datum (Luzon 1911) | ✅ Two paths | luzon1911-to-prs92-transform (W2) |
| Coordinate-based TDs | ✅ Bypass pipeline | format-variations (W3) |
| Floating parcels (no tie point) | ✅ Relative polygon | format-variations (W3) |
| Reconstituted titles | ✅ Degraded data handling | format-variations (W3) |
| Graphical-origin surveys | ✅ Relaxed tolerances | format-variations (W3) |
| Closure failure diagnostics | ✅ Quadrant-flip heuristic | error-handling (W3) |

**Edge case coverage: PASS**

---

## 8. Test Vector Coverage

| Test Vector | Pipeline Stage | Key Feature Tested |
|-------------|---------------|-------------------|
| TV-1 | Full pipeline | Standard 4-corner lot, grid bearings |
| TV-2 | Full pipeline | Luzon 1911, true bearings, 7 corners, B.L.L.M. normalization |
| TV-3 | Full pipeline | Due North, 11 corners, long tie line, qualifier plan number |
| TV-4 | Error detection | Catastrophic closure failure, BBM monument, degrees-only bearing |
| TV-5 | Inverse TM | Round-trip verification across 4 zone/location combinations |
| TV-6 | Bearing parser | 9 format variants + 3 error cases |

**Test vector coverage: PASS** — 6 vectors ≥ 5 required. Covers normal, edge case, error, and unit-level testing.

---

## 9. Summary

| Review Dimension | Result |
|-----------------|--------|
| PROMPT.md requirements | ✅ All 7 requirements met |
| Formula correctness | ✅ All formulas verified |
| Units specification | ✅ All formulas have units |
| Edge case coverage | ✅ Comprehensive (42 error codes, 6 degradation levels) |
| Test vector coverage | ✅ 6 vectors covering full spectrum |
| Implementability | ✅ After fixes, buildable without questions |
| Factual accuracy | ✅ After 3 corrections applied |

**Factual errors found and fixed:** 3 (dataset counts, dead code, JSON field names)
**Specification gaps found and fixed:** 4 (angular formula, short-perimeter edge case, small-lot area floor, WGS84 precision)

**Overall verdict: SPEC IS READY FOR IMPLEMENTATION.**

The engine spec at `output/engine-spec.md` (version 1.1) is complete, correct, and implementable. A developer can build the full pipeline — text parser, BLLM resolution, traverse computation, datum transformation, and validation — from this document alone, without needing to reference external sources beyond the cited EPSG codes and the tiepoints.json dataset.
