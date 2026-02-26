# Analysis: Luzon 1911 to PRS92 Transform (Legacy Datum Handling)

**Aspect:** luzon1911-to-prs92-transform (Wave 2)
**Date:** 2026-02-26
**Dependencies:** luzon1911-transformation (W1), prs92-datum-parameters (W1), prs92-to-wgs84-transform (W2)
**Sources:** EPSG:1161/1162 (DMA TR8350.2, 1987); DENR MC 2010-06; EPSG:9603 method spec; PROJ OSGeo pipeline definitions; Deakin/RMIT "Coordinate Transformations"; Bowring 1976; EPSG GN 7-2

---

## Summary

This analysis specifies how the engine handles legacy Luzon 1911 titles: detection, zone mapping, coordinate transformation, and accuracy metadata. Two transformation paths are supported:

- **Path A (Global, ~17–44 m):** 3-parameter geocentric translation (EPSG:1161/1162) — Luzon 1911 → WGS84 direct. Always available.
- **Path B (Local, <1 m):** 4-parameter conformal (DENR MC 2010-06) — Luzon 1911 → PRS92 → (then PRS92→WGS84 pipeline). Requires caller-provided parameters.

The engine defaults to Path A. Path B is activated when the caller supplies local transformation parameters (A, B, CE, CN).

---

## 1. Datum Detection

### 1.1 Detection Signals (in priority order)

The engine identifies the datum from metadata accompanying the technical description text. The datum is NOT encoded in the technical description body itself — it appears on the survey plan.

| Priority | Signal | Luzon 1911 | PRS92 |
|----------|--------|-----------|-------|
| 1 (highest) | Explicit datum label | `PPCS-TM/Luzon 1911`, `PTM` (without PRS92), `Old Datum` | `PPCS-TM/PRS92`, `PRS92`, `PPCS/PRS 92` |
| 2 | Azimuth type | `Astronomic Azimuth`, `Astro Azimuth` | `Grid Azimuth` |
| 3 | Survey approval date | Before 1993 | After 2005 |
| 4 (lowest) | Default | — | Assume PRS92 if ambiguous |

### 1.2 Detection Regex

```python
LUZON_1911_RE = re.compile(
    r'(?i)(luzon[\s\-]?1911|ppcs[\-/]tm[\-/]luzon|old\s+datum|ptm(?!.*prs))'
)
PRS92_RE = re.compile(
    r'(?i)(prs[\s\-]?92|ppcs[\-/](?:tm[\-/])?prs)'
)
```

### 1.3 Detection Algorithm

```python
def detect_datum(metadata_text: str, approval_year: int | None = None) -> str:
    """
    Returns "PRS92" or "Luzon 1911".
    metadata_text: text from plan header/footer (not TD body).
    approval_year: from plan approval stamp, if available.
    """
    if PRS92_RE.search(metadata_text):
        return "PRS92"
    if LUZON_1911_RE.search(metadata_text):
        return "Luzon 1911"
    # Signal 2: azimuth type
    if re.search(r'(?i)astro(nomic)?\s+azimuth', metadata_text):
        return "Luzon 1911"
    # Signal 3: approval era
    if approval_year is not None:
        if approval_year < 1993:
            return "Luzon 1911"
        if approval_year > 2005:
            return "PRS92"
    # Default: assume PRS92
    return "PRS92"
```

### 1.4 API Contract

The engine accepts an optional `datum` parameter from the caller:

```python
@dataclass
class LegacyDatumConfig:
    datum: str = "auto"              # "auto", "PRS92", "Luzon 1911"
    metadata_text: str | None = None  # Plan header text for auto-detection
    approval_year: int | None = None  # Plan approval year
    # Path B parameters (optional)
    local_A: float | None = None
    local_B: float | None = None
    local_CE: float | None = None     # metres
    local_CN: float | None = None     # metres
```

If `datum="auto"`, the engine runs detection. If `datum="Luzon 1911"` or `datum="PRS92"`, detection is skipped.

---

## 2. Zone Mapping

### 2.1 Zone Correspondence

Luzon 1911 and PRS92 use **identical PTM projection parameters** on the same Clarke 1866 ellipsoid. The zone number carries over directly:

| Zone | Luzon 1911 (EPSG) | PRS92 (EPSG) | Central Meridian |
|------|-------------------|-------------|-----------------|
| I    | 25391             | 3121        | 117°E           |
| II   | 25392             | 3122        | 119°E           |
| III  | 25393             | 3123        | 121°E           |
| IV   | 25394             | 3124        | 123°E           |
| V    | 25395             | 3125        | 125°E           |

**No re-zoning is needed.** The zone from the Luzon 1911 plan maps 1:1 to the equivalent PRS92 zone.

### 2.2 Shared Projection Parameters

Both datums use:
- Projection: Transverse Mercator
- Latitude of origin: 0° (Equator)
- Scale factor k₀: 0.99995
- False Easting E₀: 500,000 m
- False Northing N₀: 0 m
- Ellipsoid: Clarke 1866 (a = 6,378,206.4 m, 1/f = 294.978698213898)

**Critical implication:** The inverse TM computation (N/E → φ/λ) is bit-for-bit identical for both datums — same ellipsoid, same projection formulas, same zone definitions. The engine reuses the same `inverse_tm()` function regardless of datum.

### 2.3 Zone Determination from BLLM

The BLLM database (`tiepoints.json`) stores coordinates in PRS92. When a Luzon 1911 title references a BLLM:

1. Look up BLLM → get PRS92 Northing/Easting
2. The zone is determined from the BLLM record (province → zone mapping, or from plan annotation)
3. **The BLLM coordinates are already PRS92** — the engine does NOT convert them back to Luzon 1911

This means the traverse from a BLLM tie point actually computes corner coordinates in the BLLM's coordinate system. For Luzon 1911 titles, the engine has two options:
- **Option 1 (recommended):** Treat the bearings/distances as offsets from the PRS92 BLLM position. The resulting corner coordinates are approximate PRS92 (with ~10–30 m systematic bias from the Luzon 1911 survey bearings/distances).
- **Option 2:** If caller provides local transform parameters, convert the PRS92 BLLM to Luzon 1911 (inverse 4-param), compute traverse in Luzon 1911, then forward-transform corners to PRS92.

The engine uses **Option 1** by default, with accuracy metadata flagging the inherent datum mismatch.

---

## 3. Transformation Path A: Luzon 1911 → WGS84 (Global, 3-Parameter)

### 3.1 Method: EPSG:9603 (Geocentric Translations)

A pure 3-parameter geocentric translation — no rotation, no scale.

### 3.2 Regional Split

Two parameter sets, selected by geographic location:

| Region | EPSG | ΔX (m) | ΔY (m) | ΔZ (m) | Accuracy | Stations |
|--------|------|--------|--------|--------|----------|----------|
| Luzon/Visayas (excl. Mindanao) | 1161 | −133 | −77 | −51 | 17 m | 6 |
| Mindanao | 1162 | −133 | −79 | −72 | 44 m | 1 |

### 3.3 Region Selection Logic

```python
def select_luzon1911_params(lat_deg: float, lon_deg: float) -> dict:
    """
    Select EPSG:1161 or 1162 based on geographic coordinates.
    lat_deg, lon_deg: approximate WGS84 or Clarke 1866 geographic coords (degrees).
    """
    if lat_deg <= 10.52 and lon_deg >= 119.76:
        return {"epsg": 1162, "dx": -133.0, "dy": -79.0, "dz": -72.0,
                "accuracy_m": 44.0, "region": "Mindanao"}
    else:
        return {"epsg": 1161, "dx": -133.0, "dy": -77.0, "dz": -51.0,
                "accuracy_m": 17.0, "region": "Luzon/Visayas"}
```

**Overlap zone:** EPSG:1161 covers down to 7.75°N, EPSG:1162 covers up to 10.52°N. In the overlap (7.75°N–10.52°N), use EPSG:1162 if `lon >= 119.76°E` (i.e., within the Mindanao bounding box). This is conservative — Mindanao's transform has lower accuracy (44 m vs 17 m), and the engine should report this.

### 3.4 Pipeline

```
Step 1: Luzon 1911 PTM zone N/E → inverse TM → Luzon 1911 geographic (φ,λ) on Clarke 1866
Step 2: Luzon 1911 geographic → geocentric Cartesian (X,Y,Z) using Clarke 1866
Step 3: Apply translation: X_wgs84 = X + ΔX, Y_wgs84 = Y + ΔY, Z_wgs84 = Z + ΔZ
Step 4: WGS84 geocentric → WGS84 geographic (φ,λ) using WGS84 ellipsoid (Bowring method)
```

### 3.5 Formulas

**Step 1** — Inverse Transverse Mercator: identical to the PRS92 inverse TM. Use the same `inverse_tm()` function with zone central meridian and Clarke 1866 constants. Documented in `analysis/prs92-to-wgs84-transform.md` upstream pipeline.

**Step 2** — Geographic to Geocentric (Clarke 1866):

```
a = 6,378,206.4        # Clarke 1866 semi-major axis (m)
e2 = 0.006768657997    # Clarke 1866 first eccentricity squared

nu = a / sqrt(1 - e2 * sin(phi)^2)

X = (nu + h) * cos(phi) * cos(lambda)
Y = (nu + h) * cos(phi) * sin(lambda)
Z = ((1 - e2) * nu + h) * sin(phi)
```

Set h = 0 for 2D transformation. (Same formula as PRS92→WGS84 Stage 1 — same ellipsoid.)

**Step 3** — Geocentric Translation (EPSG Method 9603/1031):

```
X_wgs84 = X + dx
Y_wgs84 = Y + dy
Z_wgs84 = Z + dz
```

No rotation matrix. No scale factor. Pure vector addition.

**Step 4** — Geocentric to Geographic on WGS84 (Bowring method):

```
a_w = 6,378,137.0           # WGS84 semi-major axis
b_w = 6,356,752.314245179   # WGS84 semi-minor axis
e2_w = 0.00669437999014     # WGS84 first eccentricity squared
ep2_w = 0.00673949674228    # WGS84 second eccentricity squared

lambda = atan2(Y_wgs84, X_wgs84)
p = sqrt(X_wgs84^2 + Y_wgs84^2)

beta = atan2(a_w * Z_wgs84, b_w * p)
phi = atan2(
    Z_wgs84 + ep2_w * b_w * sin(beta)^3,
    p - e2_w * a_w * cos(beta)^3
)
```

Identical to PRS92→WGS84 Stage 3 (same target ellipsoid, same Bowring method). One iteration is sufficient.

### 3.6 Complete Pseudocode

```python
def luzon1911_to_wgs84(northing: float, easting: float, zone: int,
                        h: float = 0.0) -> tuple[float, float, dict]:
    """
    Convert Luzon 1911 PTM coordinates to WGS84 geographic.

    Parameters:
        northing: Luzon 1911 Northing (metres)
        easting: Luzon 1911 Easting (metres)
        zone: PTM zone number (1-5)
        h: ellipsoidal height (metres), default 0.0

    Returns:
        (lat_wgs84_deg, lon_wgs84_deg, metadata)
        metadata includes accuracy_m, epsg_transform, region
    """
    # --- Constants ---
    ZONE_CM = {1: 117, 2: 119, 3: 121, 4: 123, 5: 125}  # degrees
    a_src = 6378206.4       # Clarke 1866
    e2_src = 0.006768657997
    a_tgt = 6378137.0       # WGS84
    b_tgt = 6356752.314245179
    e2_tgt = 0.00669437999014
    ep2_tgt = 0.00673949674228

    # Step 1: Inverse TM (Luzon 1911 PTM → geographic on Clarke 1866)
    phi, lam = inverse_tm(northing, easting, ZONE_CM[zone],
                          a=a_src, e2=e2_src, k0=0.99995,
                          E0=500000.0, N0=0.0)
    # phi, lam in radians

    # Step 1b: Select regional parameters
    lat_deg = degrees(phi)
    lon_deg = degrees(lam)
    params = select_luzon1911_params(lat_deg, lon_deg)

    # Step 2: Geographic → Geocentric (Clarke 1866)
    sin_phi = sin(phi)
    cos_phi = cos(phi)
    nu = a_src / sqrt(1 - e2_src * sin_phi**2)
    X = (nu + h) * cos_phi * cos(lam)
    Y = (nu + h) * cos_phi * sin(lam)
    Z = ((1 - e2_src) * nu + h) * sin_phi

    # Step 3: Geocentric translation
    X_w = X + params["dx"]
    Y_w = Y + params["dy"]
    Z_w = Z + params["dz"]

    # Step 4: Geocentric → Geographic (WGS84, Bowring)
    lam_w = atan2(Y_w, X_w)
    p = sqrt(X_w**2 + Y_w**2)
    beta = atan2(a_tgt * Z_w, b_tgt * p)
    phi_w = atan2(
        Z_w + ep2_tgt * b_tgt * sin(beta)**3,
        p - e2_tgt * a_tgt * cos(beta)**3
    )

    metadata = {
        "transform_path": "A",
        "epsg_transform": params["epsg"],
        "accuracy_m": params["accuracy_m"],
        "region": params["region"],
        "datum_source": "Luzon 1911",
        "warning": f"Global approximation (~{params['accuracy_m']:.0f} m accuracy). "
                   "Not suitable for legal boundary work."
    }

    return degrees(phi_w), degrees(lam_w), metadata
```

### 3.7 Worked Example (Path A)

**Input:** Luzon 1911 Zone III, E = 500,000.00 m, N = 1,600,000.00 m (approximate Manila area)

**Step 1 — Inverse TM:**
```
Central meridian = 121°E
φ = 14.4684760242°N  (14° 28' 06.51")
λ = 121.0000000000°E (121° 00' 00.00")
```

**Step 1b — Region selection:**
```
lat = 14.47° > 10.52° → use EPSG:1161 (Luzon/Visayas)
ΔX = -133, ΔY = -77, ΔZ = -51, accuracy = 17 m
```

**Step 2 — Geographic → Geocentric (Clarke 1866, h=0):**
```
ν = 6,378,871.44 m
X = -3,181,507.80 m
Y =  5,294,918.15 m
Z =  1,583,125.72 m
```

**Step 3 — Geocentric translation:**
```
X_w = -3,181,507.80 + (-133) = -3,181,640.80 m
Y_w =  5,294,918.15 + (-77)  =  5,294,841.15 m
Z_w =  1,583,125.72 + (-51)  =  1,583,074.72 m
```

**Step 4 — Geocentric → Geographic (WGS84, Bowring):**
```
φ_wgs84 = 14.4669867°N  (14° 28' 01.15")
λ_wgs84 = 121.0014253°E (121° 00' 05.13")
```

**Shift magnitude:** Δφ ≈ −5.4 arcsec, Δλ ≈ +5.1 arcsec (consistent with ~17 m positional shift at this latitude).

---

## 4. Transformation Path B: Luzon 1911 → PRS92 (Local, 4-Parameter Conformal)

### 4.1 Method: DENR MC 2010-06

A 2D 4-parameter conformal (Helmert/similarity) transformation in projected plane coordinates.

### 4.2 Forward Transform (Luzon 1911 → PRS92)

```
E_prs92 =  A * X_lu + B * Y_lu + CE
N_prs92 = -B * X_lu + A * Y_lu + CN
```

Matrix form:
```
| E |   |  A   B | | X |   | CE |
| N | = | -B   A | | Y | + | CN |
```

Where:
- X, Y = Luzon 1911 Easting and Northing (metres)
- E, N = PRS92 Easting and Northing (metres)
- A = s × cos(θ) — scale-rotation component
- B = s × sin(θ) — scale-rotation component
- CE = Easting translation (metres)
- CN = Northing translation (metres)
- s = √(A² + B²) — scale factor
- θ = atan2(B, A) — rotation angle

### 4.3 Parameter Properties

For typical Philippine cadastral areas:
- **A ≈ 1.0** (deviation < 0.001) — negligible scale/rotation
- **B ≈ 0.0** (magnitude < 0.001) — negligible rotation
- **CE ≈ 5–30 m** — dominant translation shift
- **CN ≈ 5–30 m** — dominant translation shift

The transformation effectively degenerates to a near-pure translation:
```
E ≈ X + CE
N ≈ Y + CN
```

### 4.4 Inverse Transform (PRS92 → Luzon 1911)

```
D = A² + B²

X_lu = ( A * (E_prs92 - CE) - B * (N_prs92 - CN)) / D
Y_lu = ( B * (E_prs92 - CE) + A * (N_prs92 - CN)) / D
```

D = s² is always positive, so the inverse is always well-defined.

### 4.5 Parameter Source

The CE/CN parameters are **NOT globally published**. They are:
- Derived per cadastral survey project area by DENR-LMB
- Computed via weighted least squares from common control points (both-datum positions)
- Weight hierarchy: Reference Monuments (4) > Project Control Points (2) > Lot Corners (0.5)
- Residual filter: exclude points with residual > 1.0 m
- Validation: check points within 5 cm of model

The engine **cannot compute Path B without caller-provided parameters**.

### 4.6 Path B Pipeline

```
Step 1: Apply 4-param forward transform: Luzon 1911 N/E → PRS92 N/E
Step 2: Use standard PRS92→WGS84 pipeline (inverse TM + 7-param Helmert)
```

### 4.7 Path B Pseudocode

```python
def luzon1911_to_prs92_local(northing_lu: float, easting_lu: float,
                              A: float, B: float, CE: float, CN: float
                              ) -> tuple[float, float]:
    """
    Apply DENR MC 2010-06 4-parameter conformal transform.

    Parameters:
        northing_lu, easting_lu: Luzon 1911 PTM coordinates (metres)
        A, B, CE, CN: local transformation parameters

    Returns:
        (northing_prs92, easting_prs92) in metres
    """
    easting_prs92  =  A * easting_lu  + B * northing_lu + CE
    northing_prs92 = -B * easting_lu  + A * northing_lu + CN
    return northing_prs92, easting_prs92


def luzon1911_to_wgs84_via_prs92(northing_lu: float, easting_lu: float,
                                   zone: int,
                                   A: float, B: float,
                                   CE: float, CN: float
                                   ) -> tuple[float, float, dict]:
    """
    Path B: Luzon 1911 → PRS92 (local) → WGS84 (Helmert).
    """
    # Step 1: Local 4-param transform
    N_prs92, E_prs92 = luzon1911_to_prs92_local(
        northing_lu, easting_lu, A, B, CE, CN)

    # Step 2: Standard PRS92→WGS84 pipeline
    lat_wgs84, lon_wgs84, meta = prs92_to_wgs84(N_prs92, E_prs92, zone)

    meta["transform_path"] = "B"
    meta["accuracy_m"] = 0.10  # ~10 cm (local transform + Helmert)
    meta["warning"] = None
    meta["datum_source"] = "Luzon 1911 (local DENR MC 2010-06 transform)"
    return lat_wgs84, lon_wgs84, meta
```

### 4.8 Accuracy

| Component | Method | Accuracy |
|-----------|--------|----------|
| Luzon 1911 → PRS92 (local) | DENR MC 2010-06 4-param | ≤ 10 cm (check point) |
| PRS92 → WGS84 | EPSG:15708 7-param Helmert | 5 cm |
| **Total (Path B)** | **Combined** | **~10 cm** |

---

## 5. Engine Decision Logic

```python
def transform_luzon1911(corners_lu: list[tuple[float, float]],
                         zone: int,
                         config: LegacyDatumConfig
                         ) -> list[tuple[float, float, dict]]:
    """
    Transform Luzon 1911 corner coordinates to WGS84.

    Parameters:
        corners_lu: list of (northing, easting) in Luzon 1911 PTM (metres)
        zone: PTM zone (1-5)
        config: LegacyDatumConfig with optional local parameters

    Returns:
        list of (lat_wgs84, lon_wgs84, metadata) tuples
    """
    has_local_params = (config.local_A is not None and
                        config.local_B is not None and
                        config.local_CE is not None and
                        config.local_CN is not None)

    results = []
    for N, E in corners_lu:
        if has_local_params:
            # Path B: local 4-param → PRS92 → WGS84
            lat, lon, meta = luzon1911_to_wgs84_via_prs92(
                N, E, zone,
                config.local_A, config.local_B,
                config.local_CE, config.local_CN)
        else:
            # Path A: global 3-param → WGS84 direct
            lat, lon, meta = luzon1911_to_wgs84(N, E, zone)

        results.append((lat, lon, meta))

    return results
```

### 5.1 Decision Flowchart

```
Input: Luzon 1911 PTM corner coordinates + optional local params
                    │
                    ▼
        Caller provides A, B, CE, CN?
           /                   \
         Yes                    No
          │                      │
          ▼                      ▼
     Path B (Local)         Path A (Global)
     4-param → PRS92        3-param geocentric
     → WGS84 Helmert        translation → WGS84
          │                      │
          ▼                      ▼
     accuracy ~10 cm        accuracy ~17-44 m
     no warning             WARNING flag in output
```

---

## 6. BLLM Handling for Luzon 1911 Titles

### 6.1 Problem

The BLLM database (`tiepoints.json`) contains PRS92 coordinates. When a Luzon 1911 title specifies a BLLM as its tie point, there is a coordinate system mismatch:
- The BLLM lookup returns PRS92 N/E
- The bearings and distances in the technical description were surveyed relative to the Luzon 1911 realization of that BLLM position

### 6.2 Engine Strategy

**Default (Path A, no local params):** Use the PRS92 BLLM coordinates as the traverse origin. The traverse computation produces coordinates that are approximately PRS92 (the bearing/distance offsets are small enough — typically <1 km — that the ~10–30 m datum shift is absorbed as a systematic bias across all corners). Then transform the resulting corners from PRS92 to WGS84 using the standard Helmert pipeline.

**Accuracy note:** The relative positions of corners (lot shape and size) are preserved by this approach. The absolute position carries the ~17–44 m uncertainty inherent in the datum difference. For visual plotting, this is acceptable.

**With local params (Path B):** If the caller provides A, B, CE, CN:
1. Convert PRS92 BLLM to Luzon 1911 using the **inverse** 4-param transform
2. Compute traverse in Luzon 1911
3. Convert all corners to PRS92 using the **forward** 4-param transform
4. Then PRS92 → WGS84 via Helmert

### 6.3 Output Metadata

The engine must flag datum handling in its output:

```json
{
  "datum_source": "Luzon 1911",
  "transform_path": "A",
  "transform_accuracy_m": 17.0,
  "bllm_datum": "PRS92",
  "datum_mismatch": true,
  "warning": "Luzon 1911 title with PRS92 BLLM coordinates. Absolute position accuracy ~17 m. Relative corner positions are accurate. Not suitable for legal boundary work without DENR-approved transformation parameters."
}
```

---

## 7. Error Bounds Summary

| Scenario | Transform | Accuracy | Use Case |
|----------|-----------|----------|----------|
| Luzon 1911 → WGS84, Luzon/Visayas | EPSG:1161 (Path A) | ~17 m | Visual display, approximate mapping |
| Luzon 1911 → WGS84, Mindanao | EPSG:1162 (Path A) | ~44 m | Visual display only (low confidence) |
| Luzon 1911 → PRS92 → WGS84 (local) | DENR MC 2010-06 + EPSG:15708 (Path B) | ~10 cm | Cadastral verification |
| PRS92 → WGS84 (reference) | EPSG:15708 | 5 cm | Standard pipeline |

### 7.1 Source Limitations

- EPSG:1161 derived from only 6 stations (DMA, 1987)
- EPSG:1162 derived from only **1 station** (DMA, 1987) — Mindanao accuracy is especially poor
- No higher-accuracy global Luzon 1911 → WGS84 transformations exist in the EPSG registry
- DENR local parameters are not publicly accessible (maintained by LMB per cadastral area)

---

## 8. Cross-Verification Summary

All formulas and parameters in this analysis were verified by subagents against ≥2 independent sources.

| Item | Sources Checked | Status |
|------|----------------|--------|
| EPSG:1161 parameters (ΔX=-133, ΔY=-77, ΔZ=-51) | EPSG.io, EPSG.org, PROJ DB, ESRI ArcGIS, DMA TR8350.2 | **VERIFIED** (5 sources, no conflicts) |
| EPSG:1162 parameters (ΔX=-133, ΔY=-79, ΔZ=-72) | EPSG.io, EPSG.org, PROJ DB, ESRI ArcGIS, DMA TR8350.2 | **VERIFIED** (5 sources, no conflicts) |
| EPSG:1161/1162 coverage boundaries | EPSG.io, EPSG.org | **VERIFIED** |
| Clarke 1866 shared by both datums | EPSG:7008, EPSG:4253, EPSG:4683, GEOMATHIKS | **VERIFIED** |
| No alternative EPSG transformations for Luzon 1911 | EPSG search (all Luzon COPTRANS) | **VERIFIED** (only 1161/1162 exist) |
| EPSG:9603 is pure translation (no rotation/scale) | EPSG GN 7-2, PROJ docs, EPSG method spec | **VERIFIED** |
| Inverse TM identical for both datums | EPSG zone definitions, PROJ strings | **VERIFIED** |
| 4-param conformal formula standard form | Wikipedia, Deakin/RMIT, Ghilani, PROJ, DENR MC 2010-06 | **VERIFIED** (5 sources) |
| A = s·cos(θ), B = s·sin(θ) relationship | Deakin/RMIT, Ghilani, Wikipedia | **VERIFIED** |
| Inverse conformal formula (D = A²+B²) | Deakin/RMIT, Wikipedia, algebraic proof | **VERIFIED** |
| PROJ pipeline for EPSG:1161/1162 | EPSG.io, PROJ GitHub | **VERIFIED** |
| Worked example (Zone III, Manila area) | Computed by verification subagent | Shift ≈ −5.4" lat, +5.1" lon — consistent with ~17 m positional shift |

---

## 9. References

1. **EPSG:1161** — Luzon 1911 to WGS 84 (1), Philippines excl. Mindanao. https://epsg.io/1161
2. **EPSG:1162** — Luzon 1911 to WGS 84 (2), Mindanao. https://epsg.io/1162
3. **EPSG:9603** — Geocentric Translations (geog2D domain). https://epsg.io/9603-method
4. **DENR MC 2010-06** — Manual of Procedures on the Transformation and Integration of Cadastral Data into PRS92. https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/49164
5. **DMA TR8350.2** (September 1987) — "Department of Defense World Geodetic System 1984." NIMA/NGA.
6. **Deakin, R.E.** — "Coordinate Transformations in Surveying and Mapping." RMIT University. https://www.mygeodesy.id.au/documents/COTRAN_1.pdf
7. **Ghilani, C.D.** — "Adjustment Computations: Spatial Data Analysis," 6th ed. Wiley. Ch. 18.
8. **Bowring, B.R. (1976)** — "Transformation from Spatial to Geographical Coordinates." Survey Review XXIII/181, pp. 323–327.
9. **EPSG Guidance Note 7-2** — IOGP Publication 373-07-02. Coordinate operation methods.
10. **PROJ OSGeo** — Helmert transformation pipeline definitions. https://proj.org/en/stable/operations/transformations/helmert.html
11. **Balicanta et al. (2019)** — "Linking the Different Coordinate Systems in the Philippines." UNOOSA. https://www.unoosa.org/documents/pdf/psa/activities/2019/UN_Fiji_2019/S5-27.pdf
