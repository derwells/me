# Analysis: Luzon 1911 Transformation

**Aspect:** luzon1911-transformation (Wave 1)
**Date:** 2026-02-25
**Sources:** EPSG:4253, EPSG:1161, EPSG:1162, EPSG:25391–25395; DENR MC 2010-06 (Manual of Procedures on Transformation to PRS92); DMA TR8350.2 (1987)

---

## Summary

Luzon 1911 is the legacy datum used in Philippine land surveys prior to the adoption of PRS92 in 1993. Both datums use the Clarke 1866 ellipsoid and the same PTM zone projections (identical central meridians, scale factor, false easting/northing). The coordinate difference between Luzon 1911 and PRS92 reflects accumulated distortions in the original triangulation network — typically 10–30 m, varying by location.

Three transformation paths exist:
1. **DENR MC 2010-06 local transform** (Luzon 1911 → PRS92 direct): highest accuracy (<1 m residuals), but requires locally-derived parameters per cadastral area — not globally available
2. **Global 3-parameter Helmert via WGS84** (Luzon 1911 → WGS84 → PRS92): ~17–44 m accuracy, publicly available from EPSG
3. **Engine fallback**: Use Luzon 1911 → WGS84 directly if only WGS84 output is needed; skip PRS92 intermediate

---

## 1. Luzon 1911 Datum Parameters

### Geographic CRS (EPSG:4253)

| Parameter | Value |
|-----------|-------|
| Ellipsoid | Clarke 1866 |
| Semi-major axis (a) | 6,378,206.4 m |
| Inverse flattening (1/f) | 294.978698213898 |
| Datum anchor | Station Balanacan, Marinduque (φ=13°33'41.000"N, λ=121°52'03.000"E) |
| Status | Deprecated; replaced by PRS92 (EPSG:4683) |

**Critical note:** Luzon 1911 and PRS92 share the same ellipsoid (Clarke 1866) and the same projection parameters. The difference is purely in datum realization — the 3D position of the coordinate origin and the accumulated distortions in the triangulation network.

---

## 2. Projected Zones: Luzon 1911 → PRS92 Correspondence

Both systems use the **same PTM projection parameters**:
- Projection: Transverse Mercator
- Latitude of origin: 0°
- Scale factor k₀: 0.99995
- False Easting E₀: 500,000 m
- False Northing N₀: 0 m

Zone mapping is direct:

| Zone | Luzon 1911 EPSG | PRS92 EPSG | Central Meridian |
|------|----------------|------------|-----------------|
| I    | 25391          | 3121       | 117°E           |
| II   | 25392          | 3122       | 119°E           |
| III  | 25393          | 3123       | 121°E           |
| IV   | 25394          | 3124       | 123°E           |
| V    | 25395          | 3125       | 125°E           |

When the engine encounters a Luzon 1911 title, the zone number carries over directly to the PRS92 zone — no re-zoning needed.

---

## 3. Transformation Path A: Luzon 1911 → WGS84 (Global, Low Accuracy)

Two EPSG transformations based on 3-parameter geocentric translations:

### EPSG:1161 — Luzon/Visayas (excluding Mindanao)

| Parameter | Value |
|-----------|-------|
| ΔX | −133 m |
| ΔY | −77 m |
| ΔZ | −51 m |
| Rotations | 0 (none) |
| Scale | 0 (none) |
| Accuracy | 17.0 m total (8 m X, 11 m Y, 9 m Z) |
| Coverage | 7.75°N–19.45°N, 116.89°E–125.88°E |
| Derived at | 6 stations (DMA TR8350.2, Sep 1987) |

### EPSG:1162 — Mindanao only

| Parameter | Value |
|-----------|-------|
| ΔX | −133 m |
| ΔY | −79 m |
| ΔZ | −72 m |
| Rotations | 0 (none) |
| Scale | 0 (none) |
| Accuracy | 44.0 m total (25 m per axis) |
| Coverage | 4.99°N–10.52°N, 119.76°E–126.65°E |
| Derived at | 1 station (DMA TR8350.2, Sep 1987) |

### Application Formula

Identical structure to PRS92→WGS84 Helmert, but with only 3 parameters (no rotation, no scale). Geocentric translation pipeline:

```
1. Luzon 1911 geographic (φ,λ) → geocentric Cartesian (X,Y,Z) using Clarke 1866
2. Apply: X_wgs84 = X_lu1911 + ΔX
          Y_wgs84 = Y_lu1911 + ΔY
          Z_wgs84 = Z_lu1911 + ΔZ
3. WGS84 geocentric (X,Y,Z) → WGS84 geographic (φ,λ) using WGS84 ellipsoid
```

### Regional Split Logic

```
if latitude < 10.52° and longitude > 119.76°:
    use EPSG:1162 (Mindanao): ΔX=-133, ΔY=-79, ΔZ=-72
else:
    use EPSG:1161 (Luzon/Visayas): ΔX=-133, ΔY=-77, ΔZ=-51
```

Overlap zone (Mindanao coast near 10.52°N): use EPSG:1162.

---

## 4. Transformation Path B: Luzon 1911 → PRS92 (Local, High Accuracy)

Per DENR MC 2010-06, the standard procedure for cadastral conversion uses a **4-parameter conformal transformation in projected coordinates**:

### Mathematical Model

```
A * X  +  B * Y  +  CE  =  E
-B * X  +  A * Y  +  CN  =  N
```

Where:
- **X, Y** = Luzon 1911 PPCS-TM Easting and Northing (metres)
- **E, N** = PRS92 Easting and Northing (metres)
- **A, B** = scale and rotation parameters (typically A ≈ 1.0, B ≈ 0)
- **CE, CN** = Easting and Northing shift constants (metres, local)

Since A ≈ 1 and B ≈ 0 in most Philippine cadastral areas (negligible rotation and scale difference), the transformation degenerates to:

```
E ≈ X + CE
N ≈ Y + CN
```

### Parameter Derivation Requirements

1. Minimum: Common control points with coordinates known in both systems
2. Weight hierarchy: Reference Monuments (4) > Project Control Points (2) > Lot Corners (0.5)
3. Residual filter: Exclude points with residual > 1.0 m
4. Validation: Check points within 5 cm of model; 10+ boundary corners verified
5. Approval: Regional Technical Director for Lands → LMB

### Accuracy

- Accepted residuals: < 1.0 m for parameter derivation
- Check point accuracy: ≤ 5 cm
- Approved corner accuracy: ≤ ±10 cm

### Practical Constraint for Engine

The CE/CN parameters are NOT globally published. They are maintained by LMB (Land Management Bureau) and NAMRIA per cadastral project. The engine **cannot compute this transformation without external data**. Options:

1. **Prompt caller to provide CE/CN** if they have them (from LMB documentation)
2. **Fall back to global Helmert** (17–44 m accuracy) for visual display
3. **Flag as requiring professional transformation** for legal/boundary-critical use

---

## 5. Implied Global Approximate Shift (Luzon 1911 → PRS92)

Can be estimated from the difference in TOWGS84 parameters:

| Component | Luzon 1911→WGS84 | WGS84→PRS92 (inverted) | Net (approx) |
|-----------|-----------------|----------------------|--------------|
| ΔX (m)    | −133            | +127.62              | ≈ +5.4 m     |
| ΔY (m)    | −77             | +67.24               | ≈ +9.8 m     |
| ΔZ (m)    | −51             | +47.04               | ≈ +4.0 m     |
| Rotations | 0               | inverse of 3.068", −4.903", −1.578" | small |
| Scale     | 0               | inverse of −1.06 ppm | tiny |

In projected (plane) coordinates, this translates to approximately **10–30 m coordinate shift** between Luzon 1911 and PRS92, varying by location due to non-uniform triangulation distortions.

---

## 6. Detection Method for Engine

The engine must determine the datum of an input title. Detection signals (in order of reliability):

### Signal 1: Explicit Datum Label on Survey Plan (Most Reliable)

| Text found on plan | Datum |
|-------------------|-------|
| "PPCS-TM/Luzon 1911" | Luzon 1911 |
| "PTM" without PRS92 qualifier | Luzon 1911 (pre-1993 usage) |
| "Old Datum" | Luzon 1911 |
| "PPCS-TM/PRS92", "PRS92" | PRS92 |
| "PPCS/PRS 92" | PRS92 |

Parser regex patterns:
```
luzon_1911_pattern: r'(?i)(luzon[\s\-]?1911|ppcs[\-/]tm[\-/]luzon|old\s+datum|ptm(?!.*prs))'
prs92_pattern:      r'(?i)(prs[\s\-]?92|ppcs[\-/](?:tm[\-/])?prs)'
```

### Signal 2: Azimuth Type

| Text | Datum era |
|------|-----------|
| "Astronomic Azimuth" or "Astro Azimuth" | Likely Luzon 1911 (pre-GPS era) |
| "Grid Azimuth" | PRS92 era |

### Signal 3: Survey Approval Date

- EO 45 signed 1993, implemented gradually (~1995–2000 in practice)
- Surveys approved before 1993: almost certainly Luzon 1911
- Surveys approved 1993–2005: ambiguous — check explicit label
- Surveys approved after 2005: almost certainly PRS92 (DENR fully enforced by then)

### Signal 4: Survey Plan Number Pattern

Plan numbers do not reliably encode datum (numbering sequences continued across the transition), so this is unreliable. Do NOT use as primary signal.

### Default: Assume PRS92 if ambiguous

If none of the above signals are conclusive, assume PRS92. Legacy titles that have been reissued or transformed will carry PRS92 labels.

---

## 7. Engine Workflow for Luzon 1911 Titles

```
detect_datum(plan_text) → "Luzon 1911" or "PRS92"

if datum == "Luzon 1911":
    determine_region(bllm_coordinates):
        if latitude < 10.52 and longitude > 119.76:
            transform_params = EPSG_1162  # Mindanao
        else:
            transform_params = EPSG_1161  # Luzon/Visayas

    # Option A: Direct WGS84 output (sufficient for display)
    corner_wgs84 = luzon1911_geocentric_to_wgs84(corner_lu1911, transform_params)

    # Option B: PRS92 output (if needed for downstream survey computations)
    if caller_provides_CE_CN:
        corner_prs92 = apply_4param_transform(corner_lu1911, A, B, CE, CN)
    else:
        corner_prs92 = global_approximate_via_wgs84(corner_lu1911)
        flag_accuracy = "~17-44m (global approximation; provide LMB CE/CN for <1m accuracy)"
```

---

## 8. Error Bounds Summary

| Transformation | Method | Accuracy | Notes |
|---------------|--------|----------|-------|
| Luzon 1911 → WGS84 (Luzon/Visayas) | EPSG:1161 (3-param Helmert) | ~17 m | 6 stations, 1987 |
| Luzon 1911 → WGS84 (Mindanao) | EPSG:1162 (3-param Helmert) | ~44 m | 1 station, 1987 |
| Luzon 1911 → PRS92 (local) | DENR MC 2010-06 (4-param) | <1 m residuals; ≤5 cm check | Requires LMB parameters |
| PRS92 → WGS84 | EPSG:15708 (7-param Helmert) | 0.05 m | Full 7-parameter |

**For the engine spec:** Document that Luzon 1911 title processing carries inherent ~17–44 m positional uncertainty when using global parameters, and flag this clearly in output metadata.

---

## 9. Gaps / Open Questions

- **LMB CE/CN parameter access**: No public API or database found for the locally-derived Luzon 1911 → PRS92 shift constants per cadastral area. Would need LMB/NAMRIA access.
- **TitlePlotterPH tiepoints.json**: The plugin's bundled BLLM database uses PRS92 coordinates. If a Luzon 1911 title references a BLLM, the database lookup will return PRS92 coordinates, and no Luzon 1911 conversion of the BLLM is needed — the BLLM is used as-is in PRS92, and the traverse should be computed in PRS92 (after transforming the tie line start point).
- **Accuracy for title boundary retracement**: The 17–44 m accuracy of the global transformation is sufficient for approximate visual display but NOT for legal boundary retracement. A developer note should state this limitation.

---

## Sources

- [EPSG:4253 Luzon 1911](https://epsg.io/4253)
- [EPSG:1161 Luzon 1911 to WGS 84 (1) — Philippines excl. Mindanao](https://epsg.io/1161)
- [EPSG:1162 Luzon 1911 to WGS 84 (2) — Mindanao](https://epsg.io/1162)
- [EPSG:25391–25395 Luzon 1911 / Philippines Zone I–V](https://epsg.io/25391)
- [DENR MC 2010-06 — Manual of Procedures on Transformation to PRS92](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/49164)
- [DENR MC 2010-06 summary — LegalDex](https://legaldex.com/laws/manual-of-procedures-on-the-transformation-and-integration-of-cadastral-data-into-the-philippine-reference-system-of-1992-prs92)
- [Coordinate systems for Philippines — tool-online.com](https://tool-online.com/index/systemes-coordonnees/philippines.html)
