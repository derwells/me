# Test Vectors — PH Land Title Coordinate Engine

**Aspect:** test-vectors (Wave 3)
**Date:** 2026-02-26
**Depends on:** All Wave 1 and Wave 2 analyses; format-variations (W3); error-handling (W3)
**Verification method:** All coordinates computed using IEEE 754 double-precision Python (`math` module). Inverse TM round-trips verified to < 0.05 mm.

---

## Overview

Six test vectors covering the full engine pipeline: text parsing, traverse computation, datum transformation, validation, and error handling. Each test vector specifies:

1. **Input:** Raw technical description text
2. **Expected parsed structure:** Tie point, bearings/azimuths, distances
3. **Expected traverse output:** Corner coordinates (PRS92 N/E), closure error, computed area
4. **Expected WGS84 output:** Final lat/lon for each corner
5. **Validation checks:** Closure ratio, area cross-check, datum flags

All BLLM coordinates are **hypothetical** (marked as such) — the engine's traverse arithmetic is verified against these hypothetical starting points. The relative geometry (lot shape, closure, area) is verified against the original technical descriptions.

### Critical Implementation Note: Inverse TM Formula

The inverse Transverse Mercator requires `M = (N - N₀) / k₀` (Snyder PP1395 eq. 8-20), NOT `M = N - N₀`. Since N₀ = 0 for all PRS92 zones, this simplifies to `M = N / k₀ = N / 0.99995`. Omitting the k₀ divisor causes ~94 m latitude error at typical Philippine northings. Verified by round-trip: forward TM → inverse TM recovery to < 0.05 mm across all 5 zones.

---

## TV-1: Sample 1 — PLS-1110, Alilem, Ilocos Sur (1983, Grid, Luzon 1911 era)

### 1.1 Input Text

```
A parcel of land (Lot 1, PLS-1110, Alilem Public Land Subdivision), situated in Alilem,
Ilocos Sur, Island of Luzon. Bounded on the S. along line 1-2 by Guis-it St. (10.00 m.
wide); on the W. along line 2-3 by Lot-167, PLS-1110; on the N. along line 3-4 by Lot-164,
PLS-1110; and on the E. along line 4-1 by Lot-2 of the consolidation and subd. plan.

Beginning at a point marked "1" of Lot-1 on plan, being S. 65° 02' E., 348.29 m. from BLLM
No. 1, PLS-1110, Alilem Public Land Subd., thence N. 77° 42' W., 16.41 m. to point 2;
thence N. 10° 27' E., 30.59 m. to point 3; thence S. 69° 49' E., 16.76 m. to point 4;
thence S. 10° 42' W., 28.29 m. to point 1, point of beginning, containing an area of FOUR
HUNDRED EIGHTY FIVE (485) SQUARE METERS.

All points referred to are indicated on the plan and were marked on the ground with BL cyl.
conc. mons. 15x40 cms.
Bearings: Grid; date of original survey was April–May, 1983.
```

### 1.2 Expected Parsed Structure

```json
{
  "lot_id": {
    "lot_number": "1",
    "survey_plan": "PLS-1110",
    "location": {"municipality": "Alilem", "province": "Ilocos Sur", "island": "Luzon"}
  },
  "tie_point": {
    "raw_name": "BLLM No. 1, PLS-1110, Alilem Public Land Subd.",
    "monument_type": "BLLM",
    "monument_number": 1
  },
  "tie_bearing": {"ns": "S", "deg": 65, "min": 2, "ew": "E", "azimuth": 114.966667},
  "tie_distance_m": 348.29,
  "legs": [
    {"bearing": {"ns": "N", "deg": 77, "min": 42, "ew": "W", "azimuth": 282.300000}, "distance_m": 16.41},
    {"bearing": {"ns": "N", "deg": 10, "min": 27, "ew": "E", "azimuth": 10.450000}, "distance_m": 30.59},
    {"bearing": {"ns": "S", "deg": 69, "min": 49, "ew": "E", "azimuth": 110.183333}, "distance_m": 16.76},
    {"bearing": {"ns": "S", "deg": 10, "min": 42, "ew": "W", "azimuth": 190.700000}, "distance_m": 28.29, "closing": true}
  ],
  "stated_area_sqm": 485.0,
  "bearing_type": "grid",
  "survey_date": "April–May, 1983",
  "corner_count": 4
}
```

### 1.3 Expected Traverse Output

**BLLM coordinates (hypothetical, PRS92 Zone 3):**
- N_BLLM = 1,882,450.000 m, E_BLLM = 447,320.000 m

**Tie line:**
- Az = 114.966667°, dist = 348.29 m
- ΔN = −147.010047 m, ΔE = +315.743520 m

**Corner coordinates (PRS92 Zone 3, metres):**

| Corner | Northing | Easting |
|--------|----------|---------|
| 1 | 1,882,302.989953 | 447,635.743520 |
| 2 | 1,882,306.485782 | 447,619.710202 |
| 3 | 1,882,336.568402 | 447,625.258536 |
| 4 | 1,882,330.785780 | 447,640.989362 |

**Leg deltas:**

| Leg | ΔN (m) | ΔE (m) |
|-----|--------|--------|
| 1→2 | +3.495829 | −16.033318 |
| 2→3 | +30.082621 | +5.548335 |
| 3→4 | −5.782622 | +15.730826 |
| 4→1 | −27.798116 | −5.252509 |

**Closure:**
- eN = −0.002289 m, eE = −0.006666 m
- e = 0.007048 m
- Perimeter = 92.05 m
- Precision ratio = 1:13,061 → **PASS** (exceeds 1:5,000)

**Area:**
- Computed (shoelace) = 484.653 m²
- Stated = 485.0 m²
- Discrepancy = 0.072% → **PASS** (below 0.5% threshold)

### 1.4 Expected WGS84 Output

Transform pipeline: PRS92 Zone 3 N/E → inverse TM (Clarke 1866) → Helmert EPSG:15708 → WGS84

| Corner | WGS84 Latitude | WGS84 Longitude | Lat DMS | Lon DMS |
|--------|---------------|-----------------|---------|---------|
| 1 | 17.017654819° | 120.509491642° | 17° 01' 03.557" N | 120° 30' 34.170" E |
| 2 | 17.017686040° | 120.509340976° | 17° 01' 03.670" N | 120° 30' 33.628" E |
| 3 | 17.017957993° | 120.509392369° | 17° 01' 04.649" N | 120° 30' 33.813" E |
| 4 | 17.017906101° | 120.509540248° | 17° 01' 04.462" N | 120° 30' 34.345" E |

**Metadata:**
- Datum source: PRS92 (grid bearings + 1983 date → Luzon 1911 era; BLLM stored as PRS92 in tiepoints.json → traverse computed in PRS92)
- Transform accuracy: 0.05 m (Helmert EPSG:15708)
- BLLM coordinates are hypothetical — absolute position unverified; relative geometry verified

### 1.5 Validation Summary

| Check | Result | Value |
|-------|--------|-------|
| Linear closure | PASS | 1:13,061 (threshold: 1:5,000) |
| Area cross-check | PASS | 0.072% (threshold: 0.5%) |
| Bearing consistency | PASS | Grid bearings, all quadrants exercised |
| Geometry | PASS | 4 corners, no self-intersection |
| BLLM confidence | N/A | Hypothetical coordinates |

---

## TV-2: Sample 3 — Mr-1018-D, Malabon, Rizal (1950, True, Luzon 1911)

### 2.1 Input Text

```
Beginning at a point marked "1" on plan, being S. 44° 36′ W., 90.02 meters from B.L.L.M. 1,
municipality of Malabon, Rizal, thence N. 68° 44′ E., 5.81 meters to point 2; thence S. 23°
11′ E., 32.85 meters to point 3; thence S. 23° 11′ E., 47.00 meters to point 4; thence S.
23° 34′ E., 15.33 meters to point 5; thence S. 22° 59′ E., 17.24 meters to point 6; thence
S. 61° 37′ W., 5.99 meters to point 7; thence N. 23° 08′ W., 113.14 meters to the point of
beginning, containing an area of 664 square meters, more or less.

All points referred to are indicated on the plan and are marked on the ground.
Bearings true; declination 0° 56′ E.; date of survey, May 15, 1950 and that of the approval,
January 17, 1951.
```

### 2.2 Expected Parsed Structure

Key parsing tests:
- Monument code: **B.L.L.M.** (periods between letters) → normalizes to "BLLM"
- Monument number: 1 (no "No." prefix)
- Descriptor: "municipality of Malabon, Rizal"
- Bearing type: True (with declination 0° 56′ E. — informational only, not applied)
- Area format: numerals only ("664 square meters")
- Area suffix: "more or less"
- 7 corners (heptagon)
- Two legs share the same bearing (S 23° 11' E) — legs 2→3 and 3→4

```json
{
  "tie_bearing": {"ns": "S", "deg": 44, "min": 36, "ew": "W", "azimuth": 224.600000},
  "tie_distance_m": 90.02,
  "legs": [
    {"bearing": {"azimuth": 68.733333}, "distance_m": 5.81},
    {"bearing": {"azimuth": 156.816667}, "distance_m": 32.85},
    {"bearing": {"azimuth": 156.816667}, "distance_m": 47.00},
    {"bearing": {"azimuth": 156.433333}, "distance_m": 15.33},
    {"bearing": {"azimuth": 157.016667}, "distance_m": 17.24},
    {"bearing": {"azimuth": 241.616667}, "distance_m": 5.99},
    {"bearing": {"azimuth": 336.866667}, "distance_m": 113.14, "closing": true}
  ],
  "stated_area_sqm": 664.0,
  "bearing_type": "true",
  "corner_count": 7
}
```

### 2.3 Expected Traverse Output

**BLLM coordinates (hypothetical, PRS92 Zone 3 — Malabon is in Metro Manila):**
- N_BLLM = 1,620,500.000 m, E_BLLM = 501,200.000 m

**Corner coordinates (PRS92 Zone 3, metres):**

| Corner | Northing | Easting |
|--------|----------|---------|
| 1 | 1,620,435.903415 | 501,136.792182 |
| 2 | 1,620,438.010755 | 501,142.206535 |
| 3 | 1,620,407.813396 | 501,155.138743 |
| 4 | 1,620,364.608651 | 501,173.641446 |
| 5 | 1,620,350.557243 | 501,179.770623 |
| 6 | 1,620,334.685780 | 501,186.502211 |
| 7 | 1,620,331.838324 | 501,181.232288 |

**Closure:**
- eN = −0.022329 m, eE = −0.009453 m
- e = 0.024248 m
- Perimeter = 237.36 m
- Precision ratio = 1:9,789 → **PASS** (exceeds 1:5,000)

**Area:**
- Computed (shoelace) = 663.523 m²
- Stated = 664.0 m²
- Discrepancy = 0.072% → **PASS** (below 0.5% threshold)

### 2.4 Expected WGS84 Output

Transform pipeline: PRS92 Zone 3 N/E → inverse TM → Helmert → WGS84
(Note: BLLM stored as PRS92. For Luzon 1911 titles with PRS92 BLLM, the engine uses PRS92 pipeline and flags the datum mismatch.)

| Corner | WGS84 Latitude | WGS84 Longitude |
|--------|---------------|-----------------|
| 1 | 14.651686213° | 121.011911536° |
| 2 | 14.651705259° | 121.011961800° |
| 3 | 14.651432324° | 121.012081849° |
| 4 | 14.651041824° | 121.012253609° |
| 5 | 14.650914822° | 121.012310506° |
| 6 | 14.650771370° | 121.012372994° |
| 7 | 14.650745635° | 121.012324071° |

**Metadata:**
- Datum source: Luzon 1911 (True bearings, 1950 survey)
- Datum mismatch: true (BLLM coordinates from PRS92 database)
- Transform path: PRS92 pipeline (default when BLLM is PRS92)
- Warning: "Luzon 1911 title with PRS92 BLLM coordinates. Relative corner positions are accurate. Absolute position accuracy ~7–13 m."

### 2.5 Datum Comparison

For the same grid coordinates, the Luzon 1911 Path A (EPSG:1161) gives a different WGS84 result:

| Method | Corner 1 Lat | Corner 1 Lon | Δ from PRS92 |
|--------|-------------|-------------|-------------|
| PRS92 pipeline | 14.651686213° | 121.011911536° | — |
| Luzon 1911 Path A (EPSG:1161) | 14.651693191° | 121.011979857° | +0.8 m N, +7.3 m E |

The ~7 m horizontal difference is consistent with the known Luzon 1911 → PRS92 grid shift in Metro Manila.

---

## TV-3: Sample 5 — Psu-(af)-02-001767, Peñablanca, Cagayan (2011, True, PRS92)

### 3.1 Input Text

```
A parcel of land (Lot No. 1, Plan Psu-(af)-02-001767) situated in Barangay Patagueleg,
Municipality of Peñablanca, Province of Cagayan, Island of Luzon.

Beginning at a point marked "1" on plan, being N. 11 deg. 05' W., 4,317.52 m. from BLLM.
No. 1, Pls-793; thence S. 36 deg. 43' E., 98.73 m. to point 2; thence S. 83 deg. 12' E.,
519.94 m. to point 3; thence S. 83 deg. 16' E., 196.00 m. to point 4; thence S. 00 deg. 06'
W., 5.55 m. to point 5; thence N. 83 deg. 04' W., 247.07 m. to point 6; thence N. 83 deg.
04' W., 236.00 m. to point 7; thence N. 83 deg. 04' W., 239.99 m. to point 8; thence N. 35
deg. 56' W., 94.00 m. to point 9; thence N. 80 deg. 13' W., 180.26 m. to point 10; thence
Due North 5.64 m. to point 11; thence S. 80 deg. 27' E., 183.16 m. to point of beginning,
containing an area of FOUR THOUSAND NINE HUNDRED TWENTY-SIX (4,926) SQUARE METERS, more or
less.

Bearings true; date of survey 01 March 2011.
```

### 3.2 Key Parsing Tests

- Bearing format: **"deg."** (spelled out degrees)
- **Due North** bearing in leg 10→11 → azimuth = 0.000°
- Near-zero bearing: S 00° 06' W → azimuth = 180.100°
- Three consecutive identical bearings: N 83° 04' W (legs 5→6, 6→7, 7→8) → azimuth = 276.933333°
- Long tie line: 4,317.52 m
- 11 corners
- Monument code: **BLLM.** (trailing period) with **No.** prefix
- Survey plan: **Psu-(af)-02-001767** — parenthetical qualifier, region code 02

### 3.3 Expected Traverse Output

**BLLM coordinates (hypothetical, PRS92 Zone 3 — Cagayan is Zone 3):**
- N_BLLM = 1,990,000.000 m, E_BLLM = 480,000.000 m

**Corner coordinates (PRS92 Zone 3, metres):**

| Corner | Northing | Easting |
|--------|----------|---------|
| 1 | 1,994,236.992315 | 479,170.015015 |
| 2 | 1,994,157.850172 | 479,229.041570 |
| 3 | 1,994,096.287213 | 479,745.324056 |
| 4 | 1,994,073.306503 | 479,939.972167 |
| 5 | 1,994,067.756511 | 479,939.962480 |
| 6 | 1,994,097.581413 | 479,694.699234 |
| 7 | 1,994,126.070007 | 479,460.425035 |
| 8 | 1,994,155.040252 | 479,222.190015 |
| 9 | 1,994,231.152086 | 479,167.026724 |
| 10 | 1,994,261.782379 | 478,989.388178 |
| 11 | 1,994,267.422379 | 478,989.388178 |

**Closure:**
- eN = +0.042311 m, eE = −0.005215 m
- e = 0.042631 m
- Perimeter = 2,006.34 m
- Precision ratio = 1:47,063 → **PASS** (exceeds 1:5,000)

**Area:**
- Computed (shoelace) = 4,924.125 m²
- Stated = 4,926.0 m²
- Discrepancy = 0.038% → **PASS** (below 0.5% threshold)

### 3.4 Expected WGS84 Output

| Corner | WGS84 Latitude | WGS84 Longitude |
|--------|---------------|-----------------|
| 1 | 18.029574895° | 120.804552394° |
| 2 | 18.028860397° | 120.805110670° |
| 3 | 18.028309140° | 120.809987223° |
| 4 | 18.028103348° | 120.811825764° |
| 5 | 18.028053202° | 120.811825727° |
| 6 | 18.028320350° | 120.809509094° |
| 7 | 18.028575502° | 120.807296252° |
| 8 | 18.028834941° | 120.805045991° |
| 9 | 18.029522097° | 120.804524231° |
| 10 | 18.029797103° | 120.802846233° |
| 11 | 18.029848063° | 120.802846174° |

**Metadata:**
- Datum source: PRS92 (2011 survey, post-DENR MC 2010-06)
- Transform accuracy: 0.05 m (Helmert EPSG:15708)

---

## TV-4: Sample 2 — Psd-55969, Angeles, Pampanga (Error Detection)

### 4.1 Input Text

```
Beginning at a point marked "1" on plan, being S. 29° 48' E., 393.43 m. from B.B2. No. 42,
Angeles Cadastro, thence S. 9° 35' E., 27.99 m. to point "2"; thence S. 45° 36' W., 16.95
m. to point "3"; thence S. 86° 15' W., 5.95 m. to point "4"; thence N. 51° W., 24.01 m. to
point "5"; thence N. 45° 07' E., 21.99 m. to the point of beginning.

Bearings true; date of original survey: January–July, 1916; date of subdivision survey:
July 15–18, 1958.
```

### 4.2 Key Parsing Tests

- Monument code: **B.B2.** (Barangay Boundary Monument type 2) — non-BLLM tie point
- Quoted corner numbers: `point "2"`, `point "3"` etc.
- **Degrees-only bearing**: `N. 51° W.` (no minutes) → minutes default to 0
- Closing phrase: `to the point of beginning` (no corner number)
- Pre-1993 survey dates (1916 original, 1958 subdivision) → Luzon 1911

### 4.3 Expected Traverse Output

**BLLM coordinates (hypothetical, PRS92 Zone 3):**
- N_BLLM = 1,670,500.000 m, E_BLLM = 483,200.000 m

**Corner coordinates (PRS92 Zone 3, metres):**

| Corner | Northing | Easting |
|--------|----------|---------|
| 1 | 1,670,158.595038 | 483,395.524465 |
| 2 | 1,670,130.995652 | 483,400.184295 |
| 3 | 1,670,119.136358 | 483,388.073983 |
| 4 | 1,670,118.747210 | 483,382.136722 |
| 5 | 1,670,133.857192 | 483,363.477448 |

**Closure:**
- eN = −9.220 m, eE = −16.466 m
- e = 18.872 m
- Perimeter = 96.89 m
- Precision ratio = **1:5** → **FAIL** (below 1:1,000 threshold)

### 4.4 Expected Engine Behavior

This is an **error detection** test vector. The engine should:

1. **Parse successfully** — all bearings and distances are syntactically valid
2. **Resolve tie point** — B.B2. No. 42 is unlikely to be in the BLLM database → raise `BLLMNotFound` or return `source: "caller-provided"` if override coordinates are given
3. **Compute traverse** — produce corner coordinates as shown
4. **FAIL validation** — linear closure 1:5 is catastrophically bad
5. **Report diagnostic** — the closure failure diagnostic should identify that the traverse does not close
6. **Set output degradation level** — "relative polygon" (no WGS84 output, since closure fails)

**Root cause:** The bearing `N. 45° 07' E.` for the closing leg (5→1) cannot close a pentagon with the stated geometry. The original survey likely has additional information (a court document excerpt may have omitted corners or altered bearings). This tests the engine's ability to detect and report non-closing traverses.

### 4.5 Expected Validation Output

```json
{
  "closure": {
    "status": "fail",
    "e_m": 18.872,
    "precision_denom": 5,
    "threshold_used": "1:1000 (minimum)",
    "diagnostic": "Traverse does not close. Linear misclosure 18.87 m on 96.89 m perimeter."
  },
  "area_check": {
    "status": "skip",
    "reason": "Closure failed — area computation unreliable"
  },
  "overall_status": "FATAL",
  "degradation_level": "relative_polygon",
  "confidence_score": 0.1
}
```

---

## TV-5: Inverse TM Round-Trip Verification

### 5.1 Purpose

Validates the inverse Transverse Mercator implementation in isolation, independent of traverse computation. Uses synthetic test points across multiple zones.

### 5.2 Test Points

All points use Clarke 1866 ellipsoid (a = 6,378,206.4 m, e² = 0.006768657997), k₀ = 0.99995, E₀ = 500,000 m, N₀ = 0 m.

| ID | Zone | CM (°E) | Input φ (°) | Input λ (°) | Forward N (m) | Forward E (m) | Round-trip φ error | Round-trip λ error |
|----|------|---------|------------|------------|---------------|---------------|-------------------|-------------------|
| A | 3 | 121 | 17.020000 | 120.510000 | 1,882,377.499769 | 447,828.824695 | < 0.05 mm | < 0.01 mm |
| B | 3 | 121 | 18.030000 | 120.805000 | 1,994,093.279355 | 479,352.725070 | < 0.05 mm | < 0.01 mm |
| C | 5 | 125 | 11.178000 | 124.960000 | 1,236,016.792139 | 495,631.305981 | < 0.03 mm | < 0.01 mm |
| D | 4 | 123 | 10.310000 | 123.890000 | 1,140,150.583881 | 597,485.123388 | < 0.03 mm | < 0.01 mm |

### 5.3 Test Procedure

For each point:
1. Compute forward TM from (φ, λ) → (N, E) using the given zone parameters
2. Compute inverse TM from (N, E) → (φ', λ') using the same zone parameters
3. Verify: |φ' − φ| < 1e-9° AND |λ' − λ| < 1e-9° (sub-millimetre)

### 5.4 Full Pipeline Test (Inverse TM + Helmert)

For Test Point A (Zone 3, Ilocos Sur area):

```
Input PRS92 grid:  N = 1,882,377.499769 m, E = 447,828.824695 m, Zone 3
→ Inverse TM →     φ = 17.020000° N, λ = 120.510000° E (on Clarke 1866)
→ Geographic → Geocentric (Clarke 1866, h=0)
→ Helmert EPSG:15708 (Coordinate Frame)
→ Geocentric → Geographic (WGS84, Bowring)
→ WGS84:          Lat = 17.018334...° N, Lon = 120.511339...° E
```

The PRS92-to-WGS84 shift is approximately:
- Δlat ≈ −1.67" (southward, ~185 m)
- Δlon ≈ +4.82" (eastward, ~154 m)

This is consistent with the known PRS92→WGS84 offset at ~17°N latitude.

---

## TV-6: Bearing Format Variations

### 6.1 Purpose

Tests the parser's ability to handle all bearing format variants identified in the Wave 1 corpus, without running the full traverse pipeline.

### 6.2 Test Cases

| ID | Input Bearing Text | Expected Azimuth (°) | Format |
|----|-------------------|---------------------|--------|
| B1 | `S. 65° 02' E.` | 114.966667 | Standard with ° symbol |
| B2 | `N. 11 deg. 05' W.` | 348.916667 | Spelled-out "deg." |
| B3 | `N. 51° W.` | 309.000000 | Degrees only, no minutes |
| B4 | `Due North` | 0.000000 | Cardinal direction |
| B5 | `Due West` | 270.000000 | Cardinal direction |
| B6 | `S. 00 deg. 06' W.` | 180.100000 | Near-zero bearing |
| B7 | `N. 83 deg. 04' W.` | 276.933333 | Typical NW bearing |
| B8 | `S. 80 deg. 27' E.` | 99.550000 | SE bearing near 90° |
| B9 | `N 77° 42' W` | 282.300000 | No periods after N/W |

### 6.3 Error Cases

| ID | Input Bearing Text | Expected Result | Error Code |
|----|-------------------|----------------|------------|
| E1 | `50 deg. 50' E.` | Parse failure | BearingMissingPrefix |
| E2 | `N. 22 deg. 40'` | Parse failure | BearingMissingSuffix |
| E3 | `S. 95° 10' W.` | Warning | BearingOutOfRange (>90° for quadrant) |

---

## Cross-Cutting Verification Notes

### A. Inverse TM Formula Correctness

The key formula for inverse TM footpoint latitude:

```
M = (N - N₀) / k₀     ← CORRECT (Snyder PP1395 eq. 8-20)
M = N - N₀              ← WRONG (omits scale factor)

mu = M / (a × (1 - e²/4 - 3e⁴/64 - 5e⁶/256))
```

For N₀ = 0 (all PRS92 zones), M = N / 0.99995. Verified by round-trip to < 0.05 mm across all 4 test zones (TV-5). The M = N variant introduces ~94 m latitude error at N ≈ 1,880,000 m.

### B. Shoelace Area Precision

All area computations use the coordinate-shift technique (subtract N_min, E_min before summation) to avoid catastrophic cancellation with large PRS92 coordinates (~1,800,000 m Northing). Without this shift, IEEE 754 double precision loses ~7 significant digits, making area computation unreliable for small lots.

### C. GeoIDEx Cross-Reference Data Quality Issue

The GeoIDEx cross-reference points recorded in `analysis/bllm-dataset-compilation.md` (Section 5.1) contain data transcription errors:
- BLLM-100 and BLLM-154 share an identical Northing (1,706,822.866 m) — impossible for two distinct monuments
- The given PTM Northing for BLLM-100 (1,706,822.866) does not correspond to the stated PRS92 latitude (15.222°); it corresponds to latitude ~15.434° (verified by round-trip)

These GeoIDEx points should NOT be used as test vectors until re-verified against the original source. The synthetic round-trip tests in TV-5 provide equivalent validation of the inverse TM computation.

### D. Tolerance Thresholds (from validation-rules analysis)

| Check | PASS | WARN | FLAG | FAIL |
|-------|------|------|------|------|
| Linear closure | ≥ 1:5,000 | 1:3,000–1:5,000 | 1:1,000–1:3,000 | < 1:1,000 |
| Area discrepancy | ≤ 0.5% | 0.5%–2% | 2%–5% | > 5% |
| Angular closure | ≤ 30″√n | 30″√n–60″√n | 60″√n–120″√n | > 120″√n |

---

## Summary Table

| TV | Sample | Corners | Datum | Closure | Area Δ% | Pipeline Test |
|----|--------|---------|-------|---------|---------|---------------|
| 1 | PLS-1110, Alilem | 4 | Luzon 1911 era (PRS92 BLLM) | 1:13,061 PASS | 0.07% PASS | Full pipeline |
| 2 | Mr-1018-D, Malabon | 7 | Luzon 1911 | 1:9,789 PASS | 0.07% PASS | Full pipeline + datum mismatch |
| 3 | Psu-02-001767, Cagayan | 11 | PRS92 | 1:47,063 PASS | 0.04% PASS | Full pipeline + Due North |
| 4 | Psd-55969, Angeles | 5 | Luzon 1911 | 1:5 FAIL | N/A | Error detection |
| 5 | Synthetic round-trips | — | PRS92 | N/A | N/A | Inverse TM verification |
| 6 | Bearing format cases | — | — | N/A | N/A | Parser unit tests |

---

## Sources

- Wave 1: `analysis/tech-description-samples.md` — 8-sample corpus
- Wave 2: `analysis/traverse-algorithm.md` — formulas and worked example
- Wave 2: `analysis/prs92-to-wgs84-transform.md` — Helmert pipeline
- Wave 2: `analysis/inverse-tm-formulas.md` — inverse TM formulas (Snyder PP1395)
- Wave 2: `analysis/luzon1911-to-prs92-transform.md` — EPSG:1161/1162 path
- Wave 2: `analysis/validation-rules.md` — tolerance thresholds
- Wave 2: `analysis/bllm-dataset-compilation.md` — GeoIDEx cross-reference data (with noted quality issues)
- Wave 3: `analysis/format-variations.md` — bearing format catalog
- Wave 3: `analysis/error-handling.md` — error codes and diagnostic logic
- Computations: Python `math` module, IEEE 754 double precision, all scripts in `raw/`
