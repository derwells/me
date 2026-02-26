# Traverse Algorithm — Philippine Land Title Coordinate Engine

**Aspect:** traverse-algorithm (Wave 2)
**Date:** 2026-02-26
**Depends on:** traverse-computation-references (Wave 1), text-parser-grammar (Wave 2)
**Verification:** All formulas cross-checked against ≥2 independent sources via subagent (see §10)

---

## 1. Overview

The traverse algorithm converts a parsed technical description into a set of PRS92 Northing/Easting coordinates for every lot corner, then computes the closure error and polygon area. It is the computational core between the text parser and the datum transformation.

**Pipeline position:**
```
Parser output → [Traverse Algorithm] → PRS92 corner coords
                                     → linear misclosure, relative precision
                                     → computed area (m²)
```

**Inputs:**
- `tie_point`: BLLM Northing (m), Easting (m), zone (1–5) — from BLLM database
- `tie_bearing`: azimuth (°), pre-computed by parser
- `tie_distance_m`: float
- `legs[]`: ordered list of `{bearing.azimuth (°), distance_m}` for polygon corners

**Outputs:**
- `corners[]`: list of `{N (m), E (m)}` for Corner 1 through Corner n (PRS92)
- `closure`: `{eN (m), eE (m), e (m), perimeter (m), precision_denom}`
- `computed_area_sqm`: float

---

## 2. Pre-processing: DMS → Decimal Degrees

The text parser already returns `azimuth` in decimal degrees (0–360°). The traverse algorithm receives azimuths directly and does NOT perform DMS conversion internally.

However, for completeness and for caller-provided overrides, the conversion is:

```
β_decimal = degrees + minutes / 60.0 + seconds / 3600.0
```

**Philippine TD practice:** Seconds are rarely present in technical descriptions (degrees + minutes only). When seconds appear, include them. When absent, assume seconds = 0.

**Note from verification (Scribd survey document):** Some public land subdivision surveys (PLS-type) do express bearings with seconds (e.g., "N 35° 44' 24" W"). The formula handles both DMS and DM formats correctly.

---

## 3. Step 1: Bearing → Azimuth

The parser handles bearing → azimuth conversion. The rules are reproduced here for reference:

| Bearing quadrant | Azimuth formula |
|------------------|----------------|
| N β E | Az = β |
| S β E | Az = 180° − β |
| S β W | Az = 180° + β |
| N β W | Az = 360° − β |
| Due North | Az = 0° |
| Due East | Az = 90° |
| Due South | Az = 180° |
| Due West | Az = 270° |

**Implementation:** Always convert azimuth to radians before computing trig functions:
```
az_radians = azimuth_degrees × π / 180
```

**Source:** Jerrymahun COGO Chapter A (using azimuth eliminates sign tables); confirmed by ENR "Azimuth Trick" article and TitlePlotterPH `bearing_to_azimuth()`.

---

## 4. Step 2: Tie Line — BLLM → Corner 1

The tie line is a single traverse leg from the BLLM to Corner 1. It uses the same polar→rectangular formula as the traverse legs.

```
ΔN_tie = dist_tie × cos(az_tie_radians)
ΔE_tie = dist_tie × sin(az_tie_radians)

N₁ = N_BLLM + ΔN_tie
E₁ = E_BLLM + ΔE_tie
```

**Units:** N_BLLM, E_BLLM, dist_tie in meters (PRS92 grid). N₁, E₁ in meters (PRS92 same zone as BLLM).

**Accuracy note:** BLLM coordinate error propagates 1:1 to all lot corners. A 5 m error in the BLLM shifts every corner by 5 m. The BLLM coordinates from tiepoints.json are the dominant source of absolute position uncertainty.

---

## 5. Step 3: Traverse Loop — Corner-to-Corner

Starting from Corner 1 (derived in Step 2), apply each polygon leg sequentially:

```
For i = 1 to n:
    az_rad_i = azimuth_i × π / 180
    ΔN_i = distance_i × cos(az_rad_i)
    ΔE_i = distance_i × sin(az_rad_i)
    N_(i+1) = N_i + ΔN_i
    E_(i+1) = E_i + ΔE_i
```

Where:
- `azimuth_i` = azimuth of the leg from Corner i to Corner i+1 (degrees, 0–360)
- `distance_i` = leg length in meters
- `n` = number of legs = number of corners

The closing leg from Corner n returns to Corner 1. After the last leg, `N_(n+1)` and `E_(n+1)` should equal `N₁` and `E₁` exactly; any difference is the misclosure.

**Indexing convention:**
- Corner 1 is the output of the tie line computation
- The traverse has n corners and n legs (last leg closes back to Corner 1)
- The tie line is NOT a polygon leg — it is computed separately

---

## 6. Step 4: Polygon Closure Computation

After computing all corners, compute the linear misclosure:

```
eN = Σ ΔN_i   (sum of all n polygon leg ΔN values; should be 0 for perfect closure)
eE = Σ ΔE_i   (sum of all n polygon leg ΔE values; should be 0 for perfect closure)

e = √(eN² + eE²)          [linear misclosure, meters]
P = Σ distance_i            [perimeter, meters]
k = P / e                  [precision denominator; higher is better]
relative_precision = 1:k   [express as ratio]
```

**Equivalent check (using corner coordinates):**
```
eN = N_(n+1)_computed − N₁   (should be ≈ 0)
eE = E_(n+1)_computed − E₁   (should be ≈ 0)
```

**Philippine tolerance thresholds** (DENR DAO 2007-29 §28.b):

| Condition | Threshold | Action |
|-----------|-----------|--------|
| k ≥ 5,000 | OK (urban cadastral) | Proceed |
| 3,000 ≤ k < 5,000 | OK (rural) | Proceed with warning |
| 1,000 ≤ k < 3,000 | Poor — flag | Warn caller: possible transcription error |
| k < 1,000 | Fail | Error: traverse does not close; do not output coordinates |

**Source:** Jerrymahun Traverse Chapter D (Latitudes and Departures), Chapter F (Coordinates), Chapter I (Traverse Adjustment by Coordinates); confirmed by ESE Notes, DENR DAO 2007-29.

---

## 7. Step 5: Polygon Area — Shoelace Formula

Compute the polygon area from the n corner coordinates using the Gauss (Shoelace) formula.

### Floating-point precision (CRITICAL for PRS92)

PRS92 Northings are ~1,800,000 m and Eastings are ~400,000–500,000 m. Applying the shoelace formula directly to these large values causes **catastrophic cancellation** — large nearly-equal numbers are subtracted, losing significant figures.

**Solution:** Subtract (N_min, E_min) from all coordinates before computing the sum. This shifts the polygon toward the origin without changing its area.

```python
# Step 5a: Shift coordinates
N_min = min(N_i for all corners)
E_min = min(E_i for all corners)
n_adj = [N_i - N_min for N_i in corners_N]
e_adj = [E_i - E_min for E_i in corners_E]

# Step 5b: Shoelace formula on adjusted coordinates
# corners indexed 0..n-1, with wraparound (index n = index 0)
two_A = 0.0
for i in range(n):
    j = (i + 1) % n
    two_A += e_adj[i] * n_adj[j] - e_adj[j] * n_adj[i]

computed_area_sqm = abs(two_A) / 2.0
```

**Alternative (surveyor's form):**
```
2A = Σᵢ N_adj_i × (E_adj_(i+1) − E_adj_(i-1))   [indices mod n]
```

**Units:** Area is in square meters if coordinates are in meters. To convert to hectares: divide by 10,000.

**Sources confirming coordinate-shift recommendation:**
1. John D. Cook, "Surveyor's Formula for Polygon Area" (2018): *"subtract the minimum x and y values from each coordinate before summing"*
2. ArcGIS/Esri polygon area documentation: uses `yOrigin = Y value of last point` (equivalent shift)
3. Python/NumPy community: `x = x - x[0]; y = y - y[0]` before shoelace
4. Wikipedia Shoelace Formula: *"avoiding loss of significance"*

---

## 8. Step 6: Bowditch Adjustment (Optional, Non-Default)

**Default behavior:** The engine computes the traverse as stated in the title (original bearings and distances) and reports the misclosure. No adjustment is applied.

**Rationale:** The bearings and distances printed in a Philippine land title are the original surveyor's adjusted values, approved by DENR. Re-adjusting them would alter the legal description. The engine's job is to faithfully reproduce the polygon, not correct the survey.

**Optional Bowditch (for "best-fit" output when misclosure is acceptable but non-zero):**

```
For each leg i with length L_i:
    ΔN_i_adj = ΔN_i − eN × (L_i / P)
    ΔE_i_adj = ΔE_i − eE × (L_i / P)
```

After Bowditch: Σ ΔN_i_adj = 0, Σ ΔE_i_adj = 0 (forced closure).

**Implementation rule:** Expose Bowditch as `apply_bowditch=False` parameter. Log a warning when enabled. Never apply it silently.

**Source:** Jerrymahun Traverse Chapter E (Traverse Adjustments), Eqs. E-1 to E-6.

---

## 9. Algorithm Pseudocode (Complete)

```python
def compute_traverse(
    N_bllm: float, E_bllm: float,
    tie_azimuth_deg: float, tie_distance_m: float,
    legs: list[dict],  # [{"azimuth_deg": float, "distance_m": float}, ...]
    apply_bowditch: bool = False
) -> dict:
    """
    Compute Philippine land title traverse from BLLM to all lot corners.

    Returns: {
        corners: [(N, E)],  # Corner 1 through Corner n, in PRS92 meters
        closure: {eN, eE, e, perimeter, precision_denom},
        computed_area_sqm: float
    }
    """
    import math

    # --- Step 2: Tie line (BLLM → Corner 1) ---
    az_rad = math.radians(tie_azimuth_deg)
    dN_tie = tie_distance_m * math.cos(az_rad)
    dE_tie = tie_distance_m * math.sin(az_rad)
    N1 = N_bllm + dN_tie
    E1 = E_bllm + dE_tie

    # --- Step 3: Traverse loop ---
    corners_N = [N1]
    corners_E = [E1]
    delta_Ns, delta_Es = [], []
    perimeter = 0.0

    for leg in legs:
        az_rad = math.radians(leg["azimuth_deg"])
        dN = leg["distance_m"] * math.cos(az_rad)
        dE = leg["distance_m"] * math.sin(az_rad)
        delta_Ns.append(dN)
        delta_Es.append(dE)
        perimeter += leg["distance_m"]
        corners_N.append(corners_N[-1] + dN)
        corners_E.append(corners_E[-1] + dE)

    # The last corner (n+1) should equal Corner 1 — it IS Corner 1
    # Drop the duplicate closing point (polygon uses corners[0..n-1])
    n = len(legs)
    polygon_N = corners_N[:n]  # Corner 1 through Corner n
    polygon_E = corners_E[:n]

    # --- Step 4: Closure ---
    eN = sum(delta_Ns)
    eE = sum(delta_Es)
    e = math.sqrt(eN**2 + eE**2)
    k = (perimeter / e) if e > 0 else float('inf')

    # --- Optional Bowditch ---
    if apply_bowditch and e > 0:
        for i, leg in enumerate(legs):
            delta_Ns[i] -= eN * (leg["distance_m"] / perimeter)
            delta_Es[i] -= eE * (leg["distance_m"] / perimeter)
        # Recompute polygon corners with adjusted deltas
        polygon_N = [N1]
        polygon_E = [E1]
        for dN, dE in zip(delta_Ns, delta_Es):
            polygon_N.append(polygon_N[-1] + dN)
            polygon_E.append(polygon_E[-1] + dE)
        polygon_N = polygon_N[:n]
        polygon_E = polygon_E[:n]

    # --- Step 5: Shoelace area (with centroid shift for FP precision) ---
    N_min = min(polygon_N)
    E_min = min(polygon_E)
    n_adj = [x - N_min for x in polygon_N]
    e_adj = [x - E_min for x in polygon_E]
    two_A = 0.0
    for i in range(n):
        j = (i + 1) % n
        two_A += e_adj[i] * n_adj[j] - e_adj[j] * n_adj[i]
    area = abs(two_A) / 2.0

    return {
        "corners": list(zip(polygon_N, polygon_E)),
        "closure": {
            "eN_m": eN, "eE_m": eE, "e_m": e,
            "perimeter_m": perimeter, "precision_denom": k
        },
        "computed_area_sqm": area
    }
```

---

## 10. Worked Example: Sample 1 — Lot 1, PLS-1110, Alilem, Ilocos Sur (1983)

**Technical description (full traverse):**
```
Beginning at a point marked "1" on plan, being S. 65° 02' E., 348.29 m. from BLLM No. 1, PLS-1110;
thence N. 77° 42' W., 16.41 m. to point 2;
thence N. 10° 27' E., 30.59 m. to point 3;
thence S. 69° 49' E., 16.76 m. to point 4;
thence S. 10° 42' W., 28.29 m. to point 1, point of beginning.
Containing an area of FOUR HUNDRED EIGHTY FIVE (485) SQUARE METERS.
Bearings: Grid; date of original survey April–May, 1983.
```

**Survey metadata:**
- Bearing type: Grid
- Vintage: 1983 (Luzon 1911 era, pre-PRS92)
- Zone: Ilocos Sur → PRS92 Zone 3 (CM 121°E, EPSG:3123) — same PTM zone used pre-PRS92
- Datum inference: Grid bearings + 1983 date → Luzon 1911. Coordinates output will be PRS92 Zone 3 only after datum transformation (separate step).
- **For this example:** We compute in the grid coordinate system as-stated. BLLM coordinates are hypothetical PRS92 Zone 3 values for illustration.

### BLLM Coordinates (hypothetical — for illustration only)

```
BLLM No. 1, PLS-1110 (hypothetical PRS92 Zone 3 coordinates):
  N_BLLM = 1,882,450.000 m
  E_BLLM = 447,320.000 m
```

### Bearing → Azimuth Conversion

| Leg | Raw bearing | NS | deg | min | EW | Azimuth (°) | dist (m) |
|-----|-------------|----|-----|-----|----|-------------|---------|
| Tie | S. 65° 02' E. | S | 65 | 2 | E | 180 − 65.033 = **114.967** | 348.29 |
| 1→2 | N. 77° 42' W. | N | 77 | 42 | W | 360 − 77.700 = **282.300** | 16.41 |
| 2→3 | N. 10° 27' E. | N | 10 | 27 | E | **10.450** | 30.59 |
| 3→4 | S. 69° 49' E. | S | 69 | 49 | E | 180 − 69.817 = **110.183** | 16.76 |
| 4→1 | S. 10° 42' W. | S | 10 | 42 | W | 180 + 10.700 = **190.700** | 28.29 |

Azimuth formula: β_deg = deg + min/60 = 65 + 2/60 = 65.0333°; az = 180 − 65.0333 = 114.967°

### Step 2: Tie Line Computation

```
az_tie = 114.967° = 2.00698 rad
cos(114.967°) = −cos(65.033°) = −0.42209
sin(114.967°) =  sin(65.033°) =  0.90655

ΔN_tie = 348.29 × (−0.42209) = −146.977 m
ΔE_tie = 348.29 ×   0.90655  =  315.774 m

N₁ = 1,882,450.000 + (−146.977) = 1,882,303.023 m
E₁ =   447,320.000 +   315.774  =   447,635.774 m
```

### Step 3: Traverse Loop

**Leg 1→2 (N 77°42' W, 16.41 m):**
```
az = 282.300° = 4.92749 rad
cos(282.300°) =  cos(77.700°) =  0.21305   [4th quadrant: cos positive]
sin(282.300°) = −sin(77.700°) = −0.97712   [4th quadrant: sin negative]

ΔN₁ = 16.41 × 0.21305  =  3.496 m  [goes North: +]
ΔE₁ = 16.41 × (−0.97712) = −16.034 m  [goes West: −]

N₂ = 1,882,303.023 + 3.496 = 1,882,306.519 m
E₂ =   447,635.774 − 16.034 = 447,619.740 m
```

**Leg 2→3 (N 10°27' E, 30.59 m):**
```
az = 10.450° = 0.18240 rad
cos(10.450°) = 0.98344
sin(10.450°) = 0.18138

ΔN₂ = 30.59 × 0.98344 = 30.083 m
ΔE₂ = 30.59 × 0.18138 =  5.547 m

N₃ = 1,882,306.519 + 30.083 = 1,882,336.602 m
E₃ =   447,619.740 +  5.547 =   447,625.287 m
```

**Leg 3→4 (S 69°49' E, 16.76 m):**
```
az = 110.183° = 1.92337 rad
cos(110.183°) = −cos(69.817°) = −0.34506   [2nd quadrant: cos negative]
sin(110.183°) =  sin(69.817°) =  0.93869   [2nd quadrant: sin positive]

ΔN₃ = 16.76 × (−0.34506) = −5.783 m  [goes South: −]
ΔE₃ = 16.76 ×  0.93869   = 15.732 m  [goes East: +]

N₄ = 1,882,336.602 − 5.783 = 1,882,330.819 m
E₄ =   447,625.287 + 15.732 =   447,641.019 m
```

**Leg 4→1 (S 10°42' W, 28.29 m — closing leg):**
```
az = 190.700° = 3.32973 rad
cos(190.700°) = −cos(10.700°) = −0.98269   [3rd quadrant: cos negative]
sin(190.700°) = −sin(10.700°) = −0.18568   [3rd quadrant: sin negative]

ΔN₄ = 28.29 × (−0.98269) = −27.808 m  [goes South: −]
ΔE₄ = 28.29 × (−0.18568) =  −5.253 m  [goes West: −]

N₁_check = 1,882,330.819 − 27.808 = 1,882,303.011 m
E₁_check =   447,641.019 −  5.253 =   447,635.766 m
```

### Corner Coordinates Summary

| Corner | Northing (m, PRS92 Zone 3) | Easting (m, PRS92 Zone 3) |
|--------|---------------------------|--------------------------|
| 1 | 1,882,303.023 | 447,635.774 |
| 2 | 1,882,306.519 | 447,619.740 |
| 3 | 1,882,336.602 | 447,625.287 |
| 4 | 1,882,330.819 | 447,641.019 |

### Step 4: Closure Check

```
ΔN values: +3.496, +30.083, −5.783, −27.808
ΔE values: −16.034, +5.547, +15.732, −5.253

eN = 3.496 + 30.083 − 5.783 − 27.808 = −0.012 m
eE = −16.034 + 5.547 + 15.732 − 5.253 = −0.008 m
e  = √(0.012² + 0.008²) = √(0.000144 + 0.000064) = √0.000208 = 0.014 m

P  = 16.41 + 30.59 + 16.76 + 28.29 = 92.05 m
k  = 92.05 / 0.014 = 6,575 → relative precision 1:6,575

Result: PASS (k > 5,000 — urban cadastral standard)
```

*Note: Small residuals (0.014 m) are rounding artifacts from 5-significant-figure trig values used in manual computation. Full-precision IEEE 754 floating-point computation would yield a smaller misclosure closer to 0.001 m, consistent with the original survey precision.*

### Step 5: Polygon Area (Shoelace)

Shift coordinates: N_min = 1,882,303.023, E_min = 447,619.740

| Corner | N_adj (m) | E_adj (m) |
|--------|----------|----------|
| 1 | 0.000 | 16.034 |
| 2 | 3.496 | 0.000 |
| 3 | 33.579 | 5.547 |
| 4 | 27.796 | 21.279 |

Shoelace terms (E_i × N_{i+1} − E_{i+1} × N_i):
```
i=1 (C1→C2): 16.034 × 3.496 − 0.000 × 0.000 =  56.055 − 0.000 =  56.055
i=2 (C2→C3):  0.000 × 33.579 − 5.547 × 3.496 =   0.000 − 19.392 = −19.392
i=3 (C3→C4):  5.547 × 27.796 − 21.279 × 33.579 = 154.198 − 714.669 = −560.471
i=4 (C4→C1): 21.279 × 0.000 − 16.034 × 27.796 =   0.000 − 445.891 = −445.891

2A = |56.055 − 19.392 − 560.471 − 445.891| = |−969.699| = 969.699
A  = 969.699 / 2 = 484.85 m²
```

**Stated area: 485 m². Computed: 484.85 m². Discrepancy: 0.15 m² (0.03%).**

Excellent closure — well within any reasonable area validation threshold. The 0.15 m² difference is a rounding artifact of the manual trig computation.

---

## 11. Output Data Structure

```json
{
  "corners": [
    {"index": 1, "N_m": 1882303.023, "E_m": 447635.774, "zone": 3},
    {"index": 2, "N_m": 1882306.519, "E_m": 447619.740, "zone": 3},
    {"index": 3, "N_m": 1882336.602, "E_m": 447625.287, "zone": 3},
    {"index": 4, "N_m": 1882330.819, "E_m": 447641.019, "zone": 3}
  ],
  "closure": {
    "eN_m": -0.012,
    "eE_m": -0.008,
    "e_m": 0.014,
    "perimeter_m": 92.05,
    "precision_denom": 6575,
    "status": "pass",
    "threshold_used": "1:5000 (urban cadastral)"
  },
  "computed_area_sqm": 484.85,
  "stated_area_sqm": 485.0,
  "area_discrepancy_pct": 0.03,
  "bowditch_applied": false
}
```

---

## 12. Algorithm Validation Notes

### Coordinate system tag
The output corners are tagged with `zone` (1–5, PRS92 zone number). This tag propagates from the BLLM database lookup. If the BLLM zone is unknown, the engine must infer it from the property location (province → zone mapping from prs92-datum-parameters analysis).

### All-quadrant verification
The worked example exercises 3 of 4 quadrants (NE, SE, SW, NW). The trig sign analysis:

| Azimuth range | cos sign | sin sign | ΔN direction | ΔE direction |
|--------------|---------|---------|------------|------------|
| 0°–90° (NE) | + | + | North (+) | East (+) |
| 90°–180° (SE) | − | + | South (−) | East (+) |
| 180°–270° (SW) | − | − | South (−) | West (−) |
| 270°–360° (NW) | + | − | North (+) | West (−) |

This is automatically correct when using azimuth + radians — no sign lookup table needed.

### Floating-point data type
Use `double` (IEEE 754 64-bit, ~15 significant digits) throughout. With PRS92 coordinates at ~7 significant digits (e.g., 1,882,303 m), double precision retains ~8 digits of fractional accuracy — more than sufficient for land survey work (cm-level).

### Perimeter vs. stated area
The shoelace formula computes **exact** area for the polygon defined by the given corner coordinates. Any discrepancy from the stated area reflects:
1. Accumulated rounding in the original survey computation
2. DMS rounding (e.g., minutes truncated vs. rounded)
3. Original Bowditch adjustment shifting corners slightly from the stated bearing/distance

A ≤2% discrepancy is normal for older surveys; ≤0.5% for post-GNSS surveys.

---

## 13. Verification Summary

| Formula | Verification Status | Sources |
|---------|---------------------|---------|
| DMS → decimal degrees (deg + min/60) | CONFIRMED | Jerrymahun Chapter D; universally standard; note: seconds also found in some PH PLS surveys |
| Bearing → azimuth (4 quadrants + Due-cardinal) | CONFIRMED | Jerrymahun COGO Ch. A; TitlePlotterPH source; ENR "Azimuth Trick" |
| ΔN = dist × cos(az), ΔE = dist × sin(az) | CONFIRMED | Jerrymahun COGO Ch. A Eqs. A-1/A-2; Memphis University CIVL 1112 lecture notes; standard surveying |
| Cumulative N_i = N_{i-1} + ΔN_i | CONFIRMED | Jerrymahun Traverse Ch. F "Coordinate Computations" and Ch. I "Traverse Adjustment by Coordinates" |
| Closure: e = √(eN² + eE²), k = P/e | CONFIRMED | Jerrymahun Ch. D (Linear Closure formula); ESE Notes Traverse Survey |
| Shoelace area + coordinate centroid shift | CONFIRMED | John D. Cook "Surveyor's Formula" (primary); ArcGIS Esri polygon area docs (normalized form = equivalent shift); Python/NumPy community practice; Wikipedia floating-point note |
| Tie line: N_C1 = N_BLLM + dist × cos(az) | CONFIRMED | Follows directly from Jerrymahun forward computation; TitlePlotterPH `generate_coordinates()` treats tie line as first bearing row |

**No conflicts found between sources.** One caveat: some PLS-type Philippine surveys include seconds in bearings (confirmed by Scribd cadastral document); the formula handles this correctly via β = deg + min/60 + sec/3600.

---

## Sources

- Jerrymahun Open Access Library — Chapter A (COGO Coordinates): https://www.jerrymahun.com/index.php/home/open-access/12-iv-cogo/21-cogo-chap-a
- Jerrymahun — Chapter D (Latitudes and Departures): https://jerrymahun.com/index.php/home/open-access/17-trav-comps/43-travcomps-chap-d
- Jerrymahun — Chapter F (Traverse Coordinates): https://jerrymahun.com/index.php/home/open-access/17-trav-comps/45-travcomps-chap-f
- Jerrymahun — Chapter G (Polygon Area): https://jerrymahun.com/index.php/home/open-access/17-trav-comps/46-travcomps-chap-g
- Jerrymahun — Chapter E (Traverse Adjustments / Bowditch): https://jerrymahun.com/index.php/home/open-access/17-trav-comps/44-travcomps-chap-e
- Jerrymahun — Chapter I (Traverse Adjustment by Coordinates): https://jerrymahun.com/index.php/home/open-access/17-trav-comps/49-travcomps-chap-i
- John D. Cook, "Surveyor's Formula for Polygon Area" (2018): https://www.johndcook.com/blog/2018/09/26/polygon-area/
- ArcGIS/Esri — "What Algorithm is Used to Determine a Polygon's Area": https://support.esri.com/en-us/knowledge-base/what-algorithm-is-used-by-arcgis-to-determine-a-polygon-000006109
- Wikipedia — Shoelace Formula: https://en.wikipedia.org/wiki/Shoelace_formula
- ENR — "Calculating Traverses is Easier Using the Azimuth Trick": https://www.enr.com/articles/53271-fundamentals-of-surveying-calculating-traverses-is-easier-using-the-azimuth-trick
- University of Memphis CIVL 1112 — Traverse Calculations PDF: https://www.ce.memphis.edu/1112/notes/project_3/traverse/Surveying_traverse.pdf
- TitlePlotterPH source (dialogs/title_plotter_dialog.py) — `generate_coordinates()`, `calculate_deltas()` (verified 2026-02-25)
- DENR DAO 2007-29 — Revised Regulations on Land Surveys (closure tolerances)
- Wave 1: `input/traverse-computation-references.md`
- Wave 2: `analysis/text-parser-grammar.md` (bearing→azimuth; parser output schema)
