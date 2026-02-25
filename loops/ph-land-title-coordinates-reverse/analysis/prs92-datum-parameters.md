# Analysis: PRS92 Datum Parameters

**Aspect:** prs92-datum-parameters (Wave 1)
**Date:** 2026-02-25
**Sources:** EPSG registry (EPSG:3121–3125, EPSG:4683, EPSG:15708)

---

## Summary

All parameters for PRS92 are confirmed from the EPSG registry. Two distinct sets of information are needed by the engine: (1) the projection parameters for converting PRS92 Easting/Northing to PRS92 geographic (lat/lng on Clarke 1866), and (2) the 7-parameter Helmert shift for converting PRS92 geographic to WGS84.

---

## 1. Clarke 1866 Ellipsoid Constants

Used by all five PRS92 zones and by legacy Luzon 1911.

| Constant            | Value                  | Notes                              |
|---------------------|------------------------|-------------------------------------|
| Semi-major axis (a) | 6,378,206.4 m         | Equatorial radius                   |
| Semi-minor axis (b) | 6,356,583.8 m         | Polar radius                        |
| Inverse flattening  | 294.978698213898      | 1/f                                 |
| e² (first ecc²)     | 0.006768657997        | e² = 1 − (b/a)²                    |
| e'² (second ecc²)   | 0.006814784945        | e'² = (a²−b²)/b²                   |

These constants are used in both the forward TM projection (geographic → projected) and its inverse.

---

## 2. Philippine Transverse Mercator Zone Definitions

### Shared Projection Parameters
- Method: Transverse Mercator
- Latitude of origin: 0° (Equator)
- Scale factor k₀: 0.99995
- False Easting E₀: 500,000 m
- False Northing N₀: 0 m

### Zone Table

| Zone | EPSG | CM (λ₀) | Coverage (approximate)                            |
|------|------|---------|----------------------------------------------------|
| 1    | 3121 | 117°E   | West of 118°E                                      |
| 2    | 3122 | 119°E   | 118°E–120°E (Palawan, Calamian Is.)               |
| 3    | 3123 | 121°E   | 120°E–122°E (Luzon W, Mindoro)                    |
| 4    | 3124 | 123°E   | 122°E–124°E (SE Luzon, Cebu, Panay, Negros, W Mindanao) |
| 5    | 3125 | 125°E   | East of 124°E (E Mindanao, Bohol, Samar)          |

**Geographic extent of all zones combined:** 116.04°E–129.95°E, 3.0°N–22.18°N.

### Zone Selection Logic

Zone is deterministic from the site longitude λ (decimal degrees, WGS84 ≈ PRS92 for this purpose):

```
if   λ < 118.0:  zone = 1, CM = 117°E
elif λ < 120.0:  zone = 2, CM = 119°E
elif λ < 122.0:  zone = 3, CM = 121°E
elif λ < 124.0:  zone = 4, CM = 123°E
else:            zone = 5, CM = 125°E
```

**Practical note:** In Philippine survey practice, the PTM zone is always annotated on the survey plan ("PTM Zone III", etc.) and also identifiable from the BLLM record. The engine should:
1. Prefer explicit zone from the survey plan text or BLLM record.
2. Fall back to longitude-based selection only if zone is ambiguous.

---

## 3. PRS92 → WGS84 Transformation

### Parameters (EPSG:15708)

7-parameter Helmert (Bursa-Wolf), **Coordinate Frame rotation convention** (EPSG:9607):

| Parameter | Symbol | Value     | Unit        |
|-----------|--------|-----------|-------------|
| X translation | dx | −127.62  | metres      |
| Y translation | dy | −67.24   | metres      |
| Z translation | dz | −47.04   | metres      |
| X rotation  | rx   | +3.068   | arc-seconds |
| Y rotation  | ry   | −4.903   | arc-seconds |
| Z rotation  | rz   | −1.578   | arc-seconds |
| Scale factor | ds  | −1.06    | ppm         |

**Accuracy:** 0.05 m (stated by EPSG for topographic mapping scope)

### Helmert Transformation Formula

The Coordinate Frame rotation convention applies as:

```
[Xwgs84]   [1+ds   +rz  -ry] [Xprs92]   [dx]
[Ywgs84] = [-rz  1+ds   +rx] [Yprs92] + [dy]
[Zwgs84]   [+ry   -rx  1+ds] [Zprs92]   [dz]
```

Where:
- X, Y, Z are geocentric Cartesian coordinates (metres)
- ds is in parts per million (divide by 10⁶ in formula)
- rx, ry, rz are converted from arc-seconds to radians (divide by 206,264.806...)

**Step-by-step pipeline:**
1. PRS92 geographic (φ, λ on Clarke 1866) → geocentric Cartesian (X, Y, Z) using Clarke 1866 a, b
2. Apply 7-parameter Helmert → WGS84 geocentric Cartesian
3. WGS84 geocentric Cartesian → WGS84 geographic (φ, λ on WGS84 ellipsoid)

### Sign Convention Warning

The EPSG:15708 transformation uses **Coordinate Frame rotation** (EPSG method 9607). This differs from **Position Vector** convention (EPSG:9606) by negation of all three rotation values.

- **Coordinate Frame** (EPSG 9607): rx=+3.068, ry=−4.903, rz=−1.578 ← EPSG canonical, use this
- **Position Vector** (ISO 19111): rx=−3.068, ry=+4.903, rz=+1.578 ← NOT what EPSG specifies

PROJ 6+ pipeline with `+convention=coordinate_frame` uses the EPSG values directly (safe).
Legacy PROJ4 `+towgs84` convention varies by version; prefer the explicit pipeline.

For the Philippines, this sign distinction causes ~0.1–0.3m positional error at the scale of Philippine surveys (given rotation magnitudes of a few arc-seconds). For title boundary precision requirements, use the correct convention.

---

## 4. Implementation Notes for Later Waves

### Wave 2 (prs92-to-wgs84-transform)
This analysis provides all parameters needed for the full inverse-TM + Helmert pipeline spec:
- Ellipsoid constants for inverse TM: a, b, e², e'², k₀, E₀, N₀, CM per zone
- Helmert 7-parameter shift with correct sign convention
- Need to derive inverse TM formulas (series expansion or iterative)

### Zone Annotation in Survey Plans
Survey plans use ordinal notation: "PTM Zone I" through "PTM Zone V" (Roman numerals), corresponding to EPSG 3121–3125. Some older plans use "PTZ" abbreviation.

### No Zone for Batanes (far north)
Batanes islands (21°N–22.18°N) fall within Zone 3 (121°E). No special zone exists for the far north.

---

## 5. Gaps / Open Questions

- **Luzon 1911 → PRS92 pre-transformation**: Luzon 1911 also uses Clarke 1866 and the same PTM projection — the datum shift is handled separately (covered in luzon1911-transformation aspect).
- **Offshore areas**: The transformation applies offshore as well (Philippines — onshore and offshore), relevant for foreshore titles.
- **Higher-accuracy grid shifts**: NAMRIA may maintain a grid shift file (NTv2 format) for higher accuracy than the 7-parameter Helmert (0.05m). This was not found in public sources; the Helmert transform at 0.05m accuracy is the publicly documented standard.

---

## Sources
- [EPSG:3121 PRS92 / Philippines Zone 1](https://epsg.io/3121)
- [EPSG:3122 PRS92 / Philippines Zone 2](https://epsg.io/3122)
- [EPSG:3123 PRS92 / Philippines Zone 3](https://epsg.io/3123)
- [EPSG:3124 PRS92 / Philippines Zone 4](https://epsg.io/3124)
- [EPSG:3125 PRS92 / Philippines Zone 5](https://epsg.io/3125)
- [EPSG:15708 PRS92 to WGS 84 (1)](https://epsg.io/15708)
- [PROJ Geodetic Transformation Documentation](https://proj.org/usage/transformation.html)
