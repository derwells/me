# Source: Luzon 1911 Transformation Parameters
**Fetched:** 2026-02-25
**Sources:** EPSG registry (EPSG:4253, EPSG:1161, EPSG:1162, EPSG:25391–25395), DENR MC 2010-06 (via elibrary.judiciary.gov.ph)

---

## Luzon 1911 Geographic CRS (EPSG:4253)

- **Type:** Geographic 2D CRS
- **Ellipsoid:** Clarke 1866 (a = 6,378,206.4 m; 1/f = 294.978698213898) — same as PRS92
- **Origin (datum anchor):** Station Balanacan, Marinduque
  - Latitude: N 13° 33' 41.000"
  - Longitude: E 121° 52' 03.000"
- **WGS84 bounds:** 116.89°E–126.65°E, 4.99°N–19.45°N
- **Status:** Deprecated, replaced by PRS92 (EPSG:4683)

---

## Luzon 1911 Projected Zones (EPSG:25391–25395)

Same TM projection parameters as PRS92 zones:
- Latitude of origin: 0° (Equator)
- Scale factor k₀: 0.99995
- False Easting E₀: 500,000 m
- False Northing N₀: 0 m

| Luzon 1911 Zone | EPSG   | Central Meridian | Replaces / Replaced By |
|-----------------|--------|-----------------|------------------------|
| Zone I          | 25391  | 117°E           | PRS92 Zone 1 (EPSG:3121) |
| Zone II         | 25392  | 119°E           | PRS92 Zone 2 (EPSG:3122) |
| Zone III        | 25393  | 121°E           | PRS92 Zone 3 (EPSG:3123) |
| Zone IV         | 25394  | 123°E           | PRS92 Zone 4 (EPSG:3124) |
| Zone V          | 25395  | 125°E           | PRS92 Zone 5 (EPSG:3125) |

---

## Luzon 1911 → WGS84 Transformations

### EPSG:1161 — Philippines excluding Mindanao
- **Method:** Geocentric translations (EPSG:9603) — 3-parameter Helmert
- **ΔX = −133 m, ΔY = −77 m, ΔZ = −51 m** (no rotations, no scale)
- **Accuracy:** 17.0 m total (8 m in X, 11 m in Y, 9 m in Z)
- **Coverage:** 7.75°N–19.45°N, 116.89°E–125.88°E
- **Derived at:** 6 stations
- **Source:** U.S. Defense Mapping Agency TR8350.2, September 1987
- **Scope:** Military survey

### EPSG:1162 — Mindanao only
- **Method:** Geocentric translations (EPSG:9603) — 3-parameter Helmert
- **ΔX = −133 m, ΔY = −79 m, ΔZ = −72 m** (no rotations, no scale)
- **Accuracy:** 44.0 m total (25 m per axis)
- **Coverage:** 4.99°N–10.52°N, 119.76°E–126.65°E
- **Derived at:** 1 station
- **Source:** U.S. Defense Mapping Agency TR8350.2, September 1987
- **Scope:** Military survey

---

## Luzon 1911 → PRS92 Transformation (DENR MC 2010-06)

### Mathematical Model

4-parameter conformal transformation in projected (plane) coordinates:

```
A*X + B*Y + CE = E
-B*X + A*Y + CN = N
```

Where:
- X, Y = PPCS-TM/Luzon 1911 Easting and Northing (metres)
- E, N = PPCS-TM/PRS92 Easting and Northing (metres)
- A, B = scale and rotation constants (derived by least squares)
- CE, CN = translation shift constants (derived by least squares, metres)

### Key Properties

1. **Parameters are LOCAL, not global** — computed per cadastral area/municipality
2. **Both datums use the same ellipsoid** (Clarke 1866), so transformation is purely a datum realization difference, not an ellipsoid change
3. **Typical coordinate shift:** ~10–30 m depending on location (from comparison of TOWGS84 values)
4. **In practice:** A ≈ 1.0, B ≈ 0 (very small rotation/scale), so the transform reduces approximately to a simple shift: E ≈ X + CE, N ≈ Y + CN

### Data Sources for Parameter Derivation

Control points with known positions in BOTH systems:
- Reference Monuments (BLLM, geodetic): weight = 4
- Project Control Points: weight = 2
- Lot Corners: weight = 0.5

Minimum requirement: Enough points to solve 4 unknowns (A, B, CE, CN), with check points reserved for validation.

### Accuracy Specifications (DENR MC 2010-06)

- Points with residual errors > 1.0 m **excluded** from parameter derivation
- Check point tolerance: coordinates within **5 cm** of model
- Adjoining cadastral area boundary consistency: minimum 10 undisturbed corner monuments validated
- Final approved accuracy acceptable at ≤ ±10 cm for recovered corners

---

## Implied Luzon 1911 → PRS92 Global Approximate Shift

Derived from TOWGS84 parameter differences (Luzon 1911 vs PRS92):

| Axis | Luzon 1911 → WGS84 | WGS84 → PRS92 | Net shift |
|------|-------------------|---------------|-----------|
| X    | −133 m            | +127.62 m     | ≈ +5.4 m  |
| Y    | −77 m             | +67.24 m      | ≈ +9.8 m  |
| Z    | −51 m             | +47.04 m      | ≈ +4.0 m  |

Plus PRS92's rotation terms (rx=3.068", ry=−4.903", rz=−1.578") and scale (−1.06 ppm), absent in Luzon 1911.

Resulting grid coordinate shifts (plane, varies by location): approximately **10–30 metres**.

---

## Detection Signals on Survey Plans

The datum label is explicitly noted on DENR-approved survey plans (Psd, Csd, Psu, Cad):

| Signal | Luzon 1911 (old) | PRS92 (current) |
|--------|-----------------|-----------------|
| Datum label | "PPCS-TM/Luzon 1911", "PTM", "Old Datum" | "PPCS-TM/PRS92", "PRS92" |
| Zone notation | "PTM Zone III" (Roman numerals) | "PTM Zone III" or "PRS92 Zone 3" |
| Azimuth type | "Astronomic Azimuth" | "Grid Azimuth" |
| Approval era | Generally pre-mid-1990s to early 2000s | Post-EO 45 (1993), enforced ~1995+ |
| Survey control | Triangulation stations (manual) | GPS/GNSS control |

**Note:** Transition period (~1993–2005) may produce ambiguous plans. The explicit datum label on the plan is the definitive identifier.
