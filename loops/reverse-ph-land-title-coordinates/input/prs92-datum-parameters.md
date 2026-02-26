# PRS92 Datum Parameters — Cached Reference

Source: EPSG registry (epsg.io), fetched 2026-02-25.
Primary entries: EPSG:3121–3125 (projected), EPSG:4683 (geographic), EPSG:15708 (transformation).

---

## Datum & Ellipsoid

**Datum name:** Philippine Reference System 1992 (PRS92)
**EPSG (geographic CRS):** 4683
**Ellipsoid:** Clarke 1866
- Semi-major axis (a): 6,378,206.4 m
- Semi-minor axis (b): 6,356,583.8 m
- Inverse flattening (1/f): 294.978698213898
- First eccentricity squared (e²): ≈ 0.006768657997
- Second eccentricity squared (e'²): ≈ 0.006814784945

**Established by:** GPS campaign at 330 first-order geodetic stations.
**Authority:** NAMRIA (National Mapping and Resource Information Authority), Coast and Geodetic Survey Department.

---

## Projected Zones — Philippine Transverse Mercator (PTM)

All zones share these projection parameters:
- Projection method: Transverse Mercator (Gauss-Krüger)
- Latitude of natural origin: 0° (Equator)
- Scale factor at natural origin: 0.99995
- False Easting: 500,000 m
- False Northing: 0 m
- Units: metres

### Zone Table

| EPSG  | Zone | Central Meridian | Area of Use                                              | PROJ.4 lon_0 |
|-------|------|-----------------|----------------------------------------------------------|-------------|
| 3121  | 1    | 117°E           | West of 118°E                                            | +lon_0=117  |
| 3122  | 2    | 119°E           | ~118°E–120°E (Palawan, Calamian Islands)                | +lon_0=119  |
| 3123  | 3    | 121°E           | ~120°E–122°E (Luzon west of 122°E, Mindoro)             | +lon_0=121  |
| 3124  | 4    | 123°E           | ~122°E–124°E (SE Luzon, Tablas, Masbate, Panay, Cebu, Negros, W Mindanao) | +lon_0=123 |
| 3125  | 5    | 125°E           | East of 124°E (E Mindanao, Bohol, Samar)                | +lon_0=125  |

**Overall coverage bounding box:** 116.04°E–129.95°E, 3.0°N–22.18°N

### Zone Selection Rule
Based on site longitude (from BLLM geographic coordinates or survey plan annotation):
- lon < 118°E → Zone 1
- 118°E ≤ lon < 120°E → Zone 2
- 120°E ≤ lon < 122°E → Zone 3
- 122°E ≤ lon < 124°E → Zone 4
- lon ≥ 124°E → Zone 5

In practice, the PTM zone is always stated on the survey plan (e.g., "PTM Zone III") or derivable from the BLLM record.

### PROJ.4 Strings (per zone)

```
Zone 1: +proj=tmerc +lat_0=0 +lon_0=117 +k=0.99995 +x_0=500000 +y_0=0 +ellps=clrk66 +towgs84=-127.62,-67.24,-47.04,3.068,-4.903,-1.578,-1.06 +units=m +no_defs
Zone 2: +proj=tmerc +lat_0=0 +lon_0=119 +k=0.99995 +x_0=500000 +y_0=0 +ellps=clrk66 +towgs84=-127.62,-67.24,-47.04,3.068,-4.903,-1.578,-1.06 +units=m +no_defs
Zone 3: +proj=tmerc +lat_0=0 +lon_0=121 +k=0.99995 +x_0=500000 +y_0=0 +ellps=clrk66 +towgs84=-127.62,-67.24,-47.04,3.068,-4.903,-1.578,-1.06 +units=m +no_defs
Zone 4: +proj=tmerc +lat_0=0 +lon_0=123 +k=0.99995 +x_0=500000 +y_0=0 +ellps=clrk66 +towgs84=-127.62,-67.24,-47.04,3.068,-4.903,-1.578,-1.06 +units=m +no_defs
Zone 5: +proj=tmerc +lat_0=0 +lon_0=125 +k=0.99995 +x_0=500000 +y_0=0 +ellps=clrk66 +towgs84=-127.62,-67.24,-47.04,3.068,-4.903,-1.578,-1.06 +units=m +no_defs
```

---

## PRS92 → WGS84 Transformation

**EPSG transformation code:** 15708 ("PRS92 to WGS 84 (1)")
**Method:** Coordinate Frame rotation — geog2D domain (EPSG:9607)
**Accuracy:** 0.05 metres
**Scope:** Topographic mapping

### 7-Parameter Helmert Values

| Parameter            | Value        | Unit        |
|----------------------|-------------|-------------|
| X-axis translation   | −127.62     | metres      |
| Y-axis translation   | −67.24      | metres      |
| Z-axis translation   | −47.04      | metres      |
| X-axis rotation (rx) | +3.068      | arc-seconds |
| Y-axis rotation (ry) | −4.903      | arc-seconds |
| Z-axis rotation (rz) | −1.578      | arc-seconds |
| Scale difference (ds)| −1.06       | ppm         |

**Sign convention: Coordinate Frame rotation (EPSG:9607)**
- Rotations are in the Coordinate Frame convention (also called "Bursa-Wolf" in some literature), NOT Position Vector (ISO 19111).
- In PROJ 6+ pipelines: use `+convention=coordinate_frame` with these rotation values directly.
- In legacy PROJ4 `+towgs84`: the convention is ambiguous across versions; use the pipeline approach for safety.

### PROJ Pipeline String (EPSG:15708 canonical)
```
+proj=pipeline
+step +proj=axisswap +order=2,1
+step +proj=unitconvert +xy_in=deg +xy_out=rad
+step +proj=push +v_3
+step +proj=cart +ellps=clrk66
+step +proj=helmert +x=-127.62 +y=-67.24 +z=-47.04 +rx=3.068 +ry=-4.903 +rz=-1.578 +s=-1.06 +convention=coordinate_frame
+step +inv +proj=cart +ellps=WGS84
+step +proj=pop +v_3
+step +proj=unitconvert +xy_in=rad +xy_out=deg
+step +proj=axisswap +order=2,1
```

### WGS84 Ellipsoid (target)
- a = 6,378,137.0 m
- 1/f = 298.257223563
- b = 6,356,752.3142 m

---

## Sources
- EPSG:3121 https://epsg.io/3121
- EPSG:3122 https://epsg.io/3122
- EPSG:3123 https://epsg.io/3123
- EPSG:3124 https://epsg.io/3124
- EPSG:3125 https://epsg.io/3125
- EPSG:4683 https://epsg.io/4683
- EPSG:15708 https://epsg.io/15708
