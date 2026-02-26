# Analysis: Traverse Computation References

**Wave**: 1 — Source Acquisition
**Date**: 2026-02-25
**Depends on**: none
**Required by**: traverse-algorithm (Wave 2)

---

## Summary

All mathematical foundations for geodetic traverse computation are well-established in open literature. The core formulas are simple trigonometry; the complexity for the Philippine land title engine lies in bearing format parsing and Philippine-specific tolerance values.

---

## Key Findings

### 1. Polar-to-Rectangular Conversion

The fundamental operation for each traverse leg:

```
ΔN = distance × cos(azimuth)
ΔE = distance × sin(azimuth)
```

**Critical**: Use azimuth (0°–360°, clockwise from North) in code, not bearing. Convert bearing → azimuth as a preprocessing step. This eliminates quadrant sign tables entirely — sin/cos produce correct signs automatically.

**Bearing → Azimuth rules** (handle in parser):
| Bearing | Azimuth |
|---|---|
| N β E | β |
| S β E | 180° − β |
| S β W | 180° + β |
| N β W | 360° − β |

Special cases from tech-description-samples analysis:
- "Due North" → Az = 0°
- "Due South" → Az = 180°
- "Due East" → Az = 90°
- "Due West" → Az = 270°
- Degrees only (no cardinal): treat as azimuth directly if > 90°, else ambiguous (flag as error)

### 2. Cumulative Corner Coordinates

Chain the polar→rectangular conversion from Corner 1:

```
(N₁, E₁) = from tie line: N_BLLM + dist_tie×cos(az_tie), E_BLLM + dist_tie×sin(az_tie)

For i = 2 to n:
    (Nᵢ, Eᵢ) = (Nᵢ₋₁ + distᵢ₋₁ × cos(azᵢ₋₁), Eᵢ₋₁ + distᵢ₋₁ × sin(azᵢ₋₁))
```

Closure: corner n+1 should equal corner 1. Misclosure = distance between them.

### 3. Closure Error Metrics

```
eN = Σ ΔNᵢ   (should be 0 for closed polygon)
eE = Σ ΔEᵢ   (should be 0)
e  = √(eN² + eE²)    [linear misclosure, meters]
P  = Σ distᵢ          [perimeter, meters]
k  = P / e            [precision denominator]
Relative precision = 1:k
```

**Philippine tolerances** (DENR DAO 2007-29 §28.b):
- Cadastral lot (urban): 1:5,000 (e.g., max e = 0.24 m for P = 1,200 m)
- Isolated lot (rural): ~1:3,000
- Engine recommendation: warn at 1:3,000; error at 1:1,000

### 4. Polygon Area — Shoelace Formula

```
2A = |Σᵢ (Eᵢ × Nᵢ₊₁ − Eᵢ₊₁ × Nᵢ)|,  indices mod n
A  = 2A / 2   [square meters]
```

**Implementation note**: Subtract (N_min, E_min) or centroid from all coordinates before summing to preserve floating-point precision with PRS92-scale values (~500,000 m Northings).

Area cross-check: compare computed area (m²) to stated area in technical description. Allowable discrepancy is typically < 2% for older surveys, < 0.5% for modern GNSS surveys.

### 5. Bowditch Adjustment — Engine Role

**Do not apply** Bowditch to the title's bearing/distance sequence. Philippine land titles publish the original survey bearings and distances, which were adjusted by the geodetic engineer before plan approval. The engine should:
1. Compute traverse as-stated
2. Report misclosure as a validation output
3. If misclosure is small (1:3,000 or better): proceed to coordinate output
4. If misclosure is large: flag as data quality issue (likely transcription error or format mismatch)

Bowditch is only relevant if the engine needs to produce a "best-fit" coordinate set despite misclosure — which should be a documented option, not the default.

### 6. Tie Line Foundation

Everything depends on the tie line traversing from the BLLM to Corner 1:

```
N_C1 = N_BLLM + dist_tie × cos(az_tie_bearing)
E_C1 = E_BLLM + dist_tie × sin(az_tie_bearing)
```

BLLM coordinate accuracy (from bllm-database-sources analysis): TitlePlotterPH tiepoints.json provides ~50,000 monuments with Northing/Easting (PRS92 assumed but not labeled). BLLM coordinate error propagates 1:1 to all lot corners. A 5 m BLLM error shifts every corner by 5 m.

---

## What's Available vs. What's Still Needed

**Available (from this wave)**:
- Complete polar→rectangular formulas
- Complete closure computation
- Shoelace area formula with precision note
- Philippine tolerance reference range
- Bowditch formula (for reference, not primary engine path)

**Still needed (Wave 2: traverse-algorithm)**:
- Worked numerical example end-to-end (BLLM → traverse → closure)
- DMS-to-decimal-degrees conversion with seconds handling
- PRS92 zone coordinate example numbers for verification

**Still needed (Wave 2: validation-rules)**:
- Exact tolerance values from DAO 2007-29 §28.b full text
- Area discrepancy tolerance (% or m²)
- Angular closure check formulation for bearing sequences

---

## Data Written

Processed reference: `input/traverse-computation-references.md`

Contains:
- Bearing↔azimuth conversion tables
- Forward and inverse computation formulas (Eqs A-1 through A-6 from Jerrymahun COGO)
- Cumulative traverse chain formula
- Closure error and relative precision formulas
- Shoelace polygon area formula with floating-point implementation note
- Bowditch correction formulas
- Philippine survey tolerance reference
- Tie-line formula

---

## Sources

- Jerrymahun COGO Chapter A: https://www.jerrymahun.com/index.php/home/open-access/12-iv-cogo/21-cogo-chap-a
- Jerrymahun Traverse Adjustment Chapter E: https://jerrymahun.com/index.php/home/open-access/17-trav-comps/44-travcomps-chap-e
- Wikipedia Shoelace Formula: https://en.wikipedia.org/wiki/Shoelace_formula
- John D. Cook, Surveyor's Formula: https://www.johndcook.com/blog/2018/09/26/polygon-area/
- DENR AO 2010-17: https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/52040
- DENR DAO 2007-29: https://legaldex.com/laws/revised-regulations-on-land-surveys
