# Analysis: Province-to-PRS92/PTM Zone Mapping

**Aspect:** province-zone-mapping (supplementary reference for zone selection logic)
**Date:** 2026-02-26
**Authority:** DAO 98-12 (DENR Administrative Order No. 98-12, "Revised Manual for Land Surveying Regulations in the Philippines"), Section 65; DAO 2005-13 ("Revised Guidelines for the Implementation of PRS92"); DENR Manual on Land Survey Procedures (DMC 2010-13, Annex)
**Sources:** NAMRIA Coast and Geodetic Survey Dept, EPSG registry (3121-3125), Studocu/CourseHero reproductions of DAO 98-12 Annex, Quizlet PPCS-PTM flashcards, epsg.io zone definitions

---

## Summary

This document provides the complete mapping of all 82 Philippine provinces to their assigned PRS92/PPCS-PTM zones per DAO 98-12. It includes zone boundary edge cases, the Palawan special zone anomaly, easting range analysis for zone detection, and geographic discrepancies between administrative zone assignments and strict longitude-based zone boundaries.

---

## 1. PRS92/PPCS-PTM Zone Definitions

| Zone | EPSG | Central Meridian | Nominal Longitude Band | Area of Use (per EPSG) |
|------|------|-----------------|----------------------|----------------------|
| I | 3121 | 117°00'E | West of 118°E | Philippines west of 118°E onshore/offshore |
| II | 3122 | 119°00'E | 118°E -- 120°E | Palawan; Calamian Islands |
| III | 3123 | 121°00'E | 120°E -- 122°E | Luzon (west of 122°E); Mindoro |
| IV | 3124 | 123°00'E | 122°E -- 124°E | SE Luzon (east of 122°E); Tablas; Masbate; Panay; Cebu; Negros; W Mindanao |
| V | 3125 | 125°00'E | 124°E -- 126°E | E Mindanao (east of 124°E); Bohol; Samar |

Common parameters across all zones:
- **Projection:** Transverse Mercator
- **Ellipsoid:** Clarke 1866 (a = 6,378,206.4 m, 1/f = 294.978698213898)
- **Scale factor at central meridian:** 0.99995
- **False Easting:** 500,000 m
- **False Northing:** 0 m
- **Latitude of origin:** 0° (Equator)

---

## 2. Complete Province-to-Zone Mapping Table (DAO 98-12)

### Key to columns
- **Province**: Current name (DAO 98-12 name in parentheses if different)
- **Region**: Administrative region
- **Zone**: DAO 98-12 assigned PPCS-PTM zone
- **EPSG**: Corresponding EPSG code
- **Approx. Longitude**: Approximate centroid longitude for cross-reference
- **Notes**: Edge cases, splits, or anomalies

---

### Zone I (a) -- EPSG:3121* (Special: CM 118°30'E)

| # | Province | Region | Zone | EPSG | Approx. Long. | Notes |
|---|----------|--------|------|------|---------------|-------|
| 1 | Palawan | MIMAROPA (IV-B) | I(a) | 3121* | 118.7°E | **Special CM 118°30'E** -- see Section 4.1 |

**CRITICAL NOTE:** DAO 98-12 assigns Palawan to "Zone I" but with a **non-standard central meridian of 118°30'E** (not the standard 117°E of EPSG:3121). This is sometimes called "Zone I(a)" in surveying literature. See Section 4.1 for implications.

---

### Zone II -- EPSG:3122 (CM 119°E)

**No provinces are assigned to Zone II in DAO 98-12.** The EPSG registry defines Zone 2 as covering Palawan/Calamian Islands (118-120°E), but the DAO assigns Palawan to the special Zone I(a) instead. Zone II exists in the EPSG registry but has no province-level assignments under the DAO.

---

### Zone III -- EPSG:3123 (CM 121°E)

| # | Province | Region | Approx. Long. | Notes |
|---|----------|--------|---------------|-------|
| 2 | Abra | CAR | 120.7°E | |
| 3 | Apayao | CAR | 121.1°E | |
| 4 | Benguet | CAR | 120.6°E | |
| 5 | Ifugao | CAR | 121.1°E | |
| 6 | Kalinga | CAR | 121.2°E | |
| 7 | Mountain Province | CAR | 121.1°E | |
| 8 | Metro Manila (NCR) | NCR | 121.0°E | |
| 9 | Ilocos Norte | Region I | 120.6°E | |
| 10 | Ilocos Sur | Region I | 120.4°E | |
| 11 | La Union | Region I | 120.3°E | |
| 12 | Pangasinan | Region I | 120.3°E | |
| 13 | Batanes | Region II | 121.9°E | |
| 14 | Cagayan | Region II | 121.8°E | |
| 15 | Isabela (west of 122°E) | Region II | 121.7°E | **Split province** -- municipalities east of 122°E are Zone IV |
| 16 | Nueva Vizcaya | Region II | 121.1°E | |
| 17 | Quirino | Region II | 121.6°E | |
| 18 | Aurora | Region III* | 121.6°E | Reassigned to Region III in some listings; originally Region IV |
| 19 | Bataan | Region III | 120.5°E | |
| 20 | Bulacan | Region III | 120.9°E | |
| 21 | Nueva Ecija | Region III | 121.0°E | |
| 22 | Pampanga | Region III | 120.7°E | |
| 23 | Tarlac | Region III | 120.6°E | |
| 24 | Zambales | Region III | 120.1°E | |
| 25 | Batangas | CALABARZON (IV-A) | 121.0°E | |
| 26 | Cavite | CALABARZON (IV-A) | 120.9°E | |
| 27 | Laguna | CALABARZON (IV-A) | 121.3°E | |
| 28 | Quezon (west of 122°E) | CALABARZON (IV-A) | 121.8°E | **Split province** -- municipalities east of 122°E are Zone IV; Polillo Islands remain Zone III |
| 29 | Rizal | CALABARZON (IV-A) | 121.1°E | |
| 30 | Marinduque | MIMAROPA (IV-B) | 121.9°E | |
| 31 | Occidental Mindoro | MIMAROPA (IV-B) | 120.9°E | |
| 32 | Oriental Mindoro | MIMAROPA (IV-B) | 121.3°E | |
| 33 | Sulu | BARMM | 121.0°E | Geographic anomaly -- see Section 4.3 |
| 34 | Tawi-Tawi | BARMM | 119.8°E | **Geographic anomaly** -- see Section 4.3 |

**Zone III total: 33 provinces** (counting Isabela and Quezon as Zone III primary, with partial Zone IV splits)

---

### Zone IV -- EPSG:3124 (CM 123°E)

| # | Province | Region | Approx. Long. | Notes |
|---|----------|--------|---------------|-------|
| 35 | Isabela (east of 122°E) | Region II | >122°E | Split from Zone III |
| 36 | Quezon (east of 122°E) | CALABARZON (IV-A) | >122°E | Split from Zone III |
| 37 | Romblon | MIMAROPA (IV-B) | 122.3°E | |
| 38 | Albay | Region V (Bicol) | 123.5°E | |
| 39 | Camarines Norte | Region V (Bicol) | 122.8°E | |
| 40 | Camarines Sur | Region V (Bicol) | 123.3°E | |
| 41 | Catanduanes | Region V (Bicol) | 124.2°E | Near Zone IV/V boundary |
| 42 | Masbate | Region V (Bicol) | 123.6°E | |
| 43 | Sorsogon | Region V (Bicol) | 124.0°E | Near Zone IV/V boundary |
| 44 | Aklan | Region VI (W. Visayas) | 122.4°E | |
| 45 | Antique | Region VI (W. Visayas) | 122.0°E | Near Zone III/IV boundary |
| 46 | Capiz | Region VI (W. Visayas) | 122.6°E | |
| 47 | Guimaras | Region VI (W. Visayas) | 122.6°E | |
| 48 | Iloilo | Region VI (W. Visayas) | 122.5°E | |
| 49 | Negros Occidental | Region VI (W. Visayas) | 122.9°E | |
| 50 | Cebu | Region VII (C. Visayas) | 123.8°E | **Camotes Islands = Zone V** |
| 51 | Negros Oriental | Region VII (C. Visayas) | 123.3°E | |
| 52 | Siquijor | Region VII (C. Visayas) | 123.6°E | |
| 53 | Zamboanga del Norte | Region IX (Zamboanga) | 122.9°E | |
| 54 | Zamboanga del Sur | Region IX (Zamboanga) | 123.3°E | |
| 55 | Zamboanga Sibugay | Region IX (Zamboanga) | 122.6°E | |
| 56 | Basilan | BARMM | 122.0°E | Near Zone III/IV boundary |

**Zone IV total: 22 provinces** (counting Isabela and Quezon Zone IV portions, plus Cebu main island)

---

### Zone V -- EPSG:3125 (CM 125°E)

| # | Province | Region | Approx. Long. | Notes |
|---|----------|--------|---------------|-------|
| 57 | Biliran | Region VIII (E. Visayas) | 124.5°E | |
| 58 | Eastern Samar | Region VIII (E. Visayas) | 125.4°E | |
| 59 | Leyte | Region VIII (E. Visayas) | 124.8°E | |
| 60 | Northern Samar | Region VIII (E. Visayas) | 124.7°E | |
| 61 | Samar (Western Samar) | Region VIII (E. Visayas) | 124.9°E | |
| 62 | Southern Leyte | Region VIII (E. Visayas) | 125.2°E | |
| 63 | Bohol | Region VII (C. Visayas) | 124.0°E | On Zone IV/V boundary |
| 64 | Cebu -- Camotes Islands | Region VII (C. Visayas) | 124.4°E | Sub-provincial split from Cebu Zone IV |
| 65 | Bukidnon | Region X (N. Mindanao) | 125.0°E | |
| 66 | Camiguin | Region X (N. Mindanao) | 124.7°E | |
| 67 | Lanao del Norte | Region X (N. Mindanao) | 123.9°E | **Geographic discrepancy** -- see Section 4.4 |
| 68 | Misamis Occidental | Region X (N. Mindanao) | 123.7°E | **Geographic discrepancy** -- see Section 4.4 |
| 69 | Misamis Oriental | Region X (N. Mindanao) | 124.6°E | |
| 70 | Davao de Oro (fmr. Compostela Valley) | Region XI (Davao) | 126.0°E | |
| 71 | Davao del Norte | Region XI (Davao) | 125.6°E | |
| 72 | Davao del Sur | Region XI (Davao) | 125.4°E | |
| 73 | Davao Occidental | Region XI (Davao) | 125.5°E | Post-DAO 98-12 province (created 2013) |
| 74 | Davao Oriental | Region XI (Davao) | 126.2°E | |
| 75 | Cotabato (North Cotabato) | Region XII (SOCCSKSARGEN) | 124.9°E | |
| 76 | Sarangani | Region XII (SOCCSKSARGEN) | 125.3°E | |
| 77 | South Cotabato | Region XII (SOCCSKSARGEN) | 124.8°E | |
| 78 | Sultan Kudarat | Region XII (SOCCSKSARGEN) | 124.4°E | |
| 79 | Agusan del Norte | Region XIII (Caraga) | 125.5°E | |
| 80 | Agusan del Sur | Region XIII (Caraga) | 125.9°E | |
| 81 | Dinagat Islands | Region XIII (Caraga) | 125.6°E | Post-DAO 98-12 province (created 2006) |
| 82 | Surigao del Norte | Region XIII (Caraga) | 125.9°E | |
| 83 | Surigao del Sur | Region XIII (Caraga) | 126.1°E | |
| 84 | Lanao del Sur | BARMM | 124.3°E | |
| 85 | Maguindanao del Norte | BARMM | 124.4°E | Post-DAO 98-12 split (2022) from Maguindanao |
| 86 | Maguindanao del Sur | BARMM | 124.5°E | Post-DAO 98-12 split (2022) from Maguindanao |

**Zone V total: 27 provinces** (counting Camotes Islands as sub-provincial; counting Maguindanao del Norte/Sur as 2)

---

## 3. Zone Summary Statistics

| Zone | EPSG | CM | Province Count | Regions Covered |
|------|------|----|---------------|-----------------|
| I(a) | 3121* | 118°30'E | 1 | MIMAROPA (Palawan only) |
| II | 3122 | 119°E | 0 | None assigned |
| III | 3123 | 121°E | 33 | CAR, NCR, Region I, II, III, CALABARZON, MIMAROPA, BARMM (Sulu, Tawi-Tawi) |
| IV | 3124 | 123°E | 22 | Region II (partial), CALABARZON (partial), MIMAROPA (Romblon), Region V, VI, VII (partial), IX, BARMM (Basilan) |
| V | 3125 | 125°E | 27 | Region VII (Bohol, Camotes), VIII, X, XI, XII, XIII, BARMM (Lanao del Sur, Maguindanao) |

**Total: 83 province-level assignments** (82 current provinces + Camotes Islands sub-provincial split)

---

## 4. Zone Boundary Edge Cases and Anomalies

### 4.1 Palawan: Zone I(a) with Non-Standard Central Meridian

**The Problem:** DAO 98-12 assigns Palawan to "Zone I" but specifies a central meridian of **118°30'E**, not the standard EPSG:3121 central meridian of 117°E. Meanwhile, EPSG:3122 (Zone 2) has a central meridian of 119°E and lists Palawan in its area of use.

**Explanation:** Palawan stretches from approximately 117.0°E (southwestern tip near Balabac) to 120.3°E (northeastern Calamian Islands/Coron area). The centroid longitude is approximately 118.7°E. A central meridian of 118°30'E minimizes distortion across the entire province better than either the standard Zone 1 (117°E) or Zone 2 (119°E) central meridians.

**Implication for engine:**
- Land titles from Palawan use the special DAO 98-12 Zone I parameters (CM = 118°30'E), **not** the standard EPSG:3121 or EPSG:3122.
- If implementing with standard EPSG codes, neither 3121 nor 3122 is exactly correct for Palawan. A custom projection definition is needed:
  ```
  +proj=tmerc +lat_0=0 +lon_0=118.5 +k=0.99995 +x_0=500000 +y_0=0 +ellps=clrk66 +units=m
  ```
- In practice, some surveyors may have used standard Zone 2 (EPSG:3122, CM 119°E) for the northern Calamian Islands area. Always check the survey plan notation.

### 4.2 Split Provinces (Straddle 122°E Boundary)

Two provinces are officially split across the Zone III/IV boundary at 122°E longitude:

**Isabela (Region II):**
- Municipalities west of 122°E: Zone III (EPSG:3123)
- Municipalities east of 122°E: Zone IV (EPSG:3124)
- The eastern municipalities of Isabela that cross 122°E include parts near the Sierra Madre mountain range.

**Quezon (CALABARZON):**
- Municipalities west of 122°E: Zone III (EPSG:3123)
- Municipalities east of 122°E: Zone IV (EPSG:3124)
- Polillo Islands: Zone III (despite being near 122°E)
- The eastern coastal municipalities of Quezon, particularly those facing the Philippine Sea, cross the 122°E line.

**Implication for engine:** For these two provinces, the zone cannot be determined by province alone. The specific municipality must be checked, or the BLLM easting value relative to the zone central meridian can be used as a discriminator (see Section 5).

### 4.3 Sulu and Tawi-Tawi in Zone III (Geographic Anomaly)

**The Problem:** Sulu's centroid is at ~121.0°E (fits Zone III). However, Tawi-Tawi's centroid is at ~119.8°E, with western islands (Sitangkai at 119.4°E, Bongao at 119.7°E) falling solidly in Zone 2 territory (118-120°E). Despite this, DAO 98-12 assigns both to Zone III.

**Explanation:**
1. The Sulu Archipelago is treated as a unified mapping region for administrative continuity.
2. Zone II is reserved exclusively for Palawan/Calamian Islands in the DAO framework.
3. Sulu at ~121°E is perfectly centered on Zone III's CM, and keeping Tawi-Tawi in the same zone as Sulu avoids splitting the archipelago.
4. The distortion for western Tawi-Tawi (1-2° from CM 121°E) is within acceptable limits for cadastral surveying.

**Implication for engine:** Tawi-Tawi titles use Zone III (EPSG:3123) despite the geographic position suggesting Zone II. This is one of the strongest reasons that zone determination must be based on the DAO province-to-zone table, not raw longitude.

### 4.4 Region X Provinces: Zone V Despite Zone IV Geography

**The Problem:** DAO 98-12 assigns all of Region X (Northern Mindanao) to Zone V (CM 125°E), but two provinces have centroids well within Zone IV territory:
- **Misamis Occidental:** ~123.7°E (Zone IV range: 122-124°E)
- **Lanao del Norte:** ~123.9°E (Zone IV range: 122-124°E)

Even Misamis Oriental (~124.6°E) and Camiguin (~124.7°E) are near the Zone IV/V boundary rather than being clearly in Zone V.

**Explanation:** The DAO chose regional administrative coherence over strict longitude-based assignment. All of Region X is assigned to a single zone to simplify administration. The westernmost municipalities of Misamis Occidental are approximately 1.5° west of the Zone V central meridian (125°E), which introduces noticeable but still within-tolerance distortion.

**Implication for engine:** This is a second strong case where province-based zone lookup (following DAO 98-12) differs from what pure longitude would suggest. The engine must use the DAO table, not compute zones from coordinates.

### 4.5 Cebu: Camotes Islands Sub-Provincial Split

Cebu province is primarily in Zone IV, but the **Camotes Islands** (municipalities of Poro, Tudela, San Francisco, Pilar) are assigned to Zone V. Camotes Islands are located at approximately 124.4°E, on the Zone IV/V boundary.

**Implication for engine:** For Cebu province, a sub-provincial check is needed if the lot is in the Camotes Islands group.

### 4.6 Provinces Created After DAO 98-12 (1998)

Several provinces were created after the DAO 98-12 zone assignments were published:

| Province | Created | Parent Province | Inherited Zone | Approx. Long. |
|----------|---------|----------------|----------------|---------------|
| Davao de Oro | 2019 (renamed from Compostela Valley) | -- | V | 126.0°E |
| Davao Occidental | 2013 | Davao del Sur | V | 125.5°E |
| Dinagat Islands | 2006 | Surigao del Norte | V | 125.6°E |
| Maguindanao del Norte | 2022 | Maguindanao | V | 124.4°E |
| Maguindanao del Sur | 2022 | Maguindanao | V | 124.5°E |
| Zamboanga Sibugay | 2001 | Zamboanga del Sur | IV | 122.6°E |
| Biliran | 1992* | Leyte | V | 124.5°E |
| Guimaras | 1992* | Iloilo | IV | 122.6°E |

*Biliran and Guimaras were created in 1992, just before DAO 98-12 (1998), and are included in the DAO.

**Implication for engine:** Davao Occidental, Dinagat Islands, Maguindanao del Norte, Maguindanao del Sur, and Zamboanga Sibugay inherit their parent province's zone. Older titles from these areas will reference the parent province name.

### 4.7 Other Near-Boundary Provinces

These provinces are close to zone boundaries but have clear assignments:

| Province | Zone | Approx. Long. | Nearest Boundary | Distance to Boundary |
|----------|------|---------------|-------------------|---------------------|
| Antique | IV | 122.0°E | Zone III/IV (122°E) | ~0°E |
| Basilan | IV | 122.0°E | Zone III/IV (122°E) | ~0°E |
| Catanduanes | IV | 124.2°E | Zone IV/V (124°E) | ~0.2°E into Zone V territory |
| Sorsogon | IV | 124.0°E | Zone IV/V (124°E) | ~0°E |
| Bohol | V | 124.0°E | Zone IV/V (124°E) | ~0°E |
| Sultan Kudarat | V | 124.4°E | Zone IV/V (124°E) | ~0.4°E |

**Catanduanes** is a notable case: at 124.2°E, it is geographically in Zone V territory but assigned to Zone IV with the rest of the Bicol region. Similar to the Region X situation, regional coherence takes precedence.

---

## 5. Easting Value Analysis for Zone Detection

### 5.1 Easting Ranges Per Zone

All PRS92 PTM zones share a false easting of 500,000 m. The central meridian of each zone maps to exactly 500,000 m E. Points west of the CM have easting < 500,000; points east have easting > 500,000.

For a 2° wide zone (±1° from CM), at typical Philippine latitudes (5°N to 20°N):

| Distance from CM | Approx. Easting at 5°N | Approx. Easting at 14°N | Approx. Easting at 20°N |
|-------------------|------------------------|--------------------------|--------------------------|
| -1.0° (1° west) | ~389,000 m | ~393,000 m | ~396,000 m |
| -0.5° | ~444,000 m | ~446,000 m | ~448,000 m |
| 0° (at CM) | 500,000 m | 500,000 m | 500,000 m |
| +0.5° | ~556,000 m | ~554,000 m | ~552,000 m |
| +1.0° (1° east) | ~611,000 m | ~607,000 m | ~604,000 m |

**Approximate easting range within a zone: 389,000 -- 611,000 m (wider at equator, narrower toward poles).**

**Practical range for Philippine land titles: ~390,000 m to ~610,000 m.**

### 5.2 Can Zone Be Detected From Easting Alone?

**No.** Because all five zones use the same false easting (500,000 m), easting values from different zones overlap completely. A point with easting 495,000 m could be in any of the five zones.

### 5.3 Easting as a Consistency Check

While easting alone cannot identify the zone, it can be used as a **sanity check** once a zone is selected:

1. If easting is **far from 500,000 m** (e.g., < 350,000 or > 650,000), the point is likely in the wrong zone or the coordinates are erroneous.
2. If a province near a zone boundary (e.g., Isabela) produces easting very different from 500,000 m, it may be in the "other" zone for that split province.

**Decision rules for split provinces (Isabela, Quezon):**
- If the BLLM easting in Zone III is between 500,000 and 611,000 m, the lot is likely east of 121°E but west of 122°E: Zone III is correct.
- If the BLLM easting in Zone III is > 611,000 m, the BLLM (and thus the lot) may actually be east of 122°E, suggesting Zone IV.
- Conversely, if in Zone IV the easting is < 389,000 m, the BLLM may be west of 122°E, suggesting Zone III.

### 5.4 Northing Ranges

Northing values are more useful for rough geographic placement since they are not offset by false northing (false northing = 0):

| Latitude | Approx. Northing |
|----------|-----------------|
| 5°N (southern Mindanao/Tawi-Tawi) | ~553,000 m |
| 7°N (central Mindanao) | ~774,000 m |
| 10°N (Visayas) | ~1,106,000 m |
| 14°N (Metro Manila) | ~1,549,000 m |
| 16°N (Cagayan Valley) | ~1,770,000 m |
| 18°N (Batanes) | ~1,991,000 m |
| 20°N (northernmost Batanes) | ~2,212,000 m |

**Northing can help disambiguate zones** because certain northing ranges exclude certain zones:
- Northing > 1,500,000 m (latitude > ~13.5°N): likely Luzon, so Zone III or IV
- Northing < 900,000 m (latitude < ~8°N): likely southern Mindanao or Sulu, so Zone III (Sulu/Tawi-Tawi), IV (Zamboanga/Basilan), or V (Mindanao)
- Northing ~1,000,000 to ~1,300,000 m: Visayas, could be Zone IV or V

---

## 6. Zone Selection Algorithm for the Engine

Given a province name (from the title or survey plan) and optionally a municipality:

```
function select_zone(province, municipality=None):

    # Lookup table from DAO 98-12 (this document, Section 2)
    zone_table = load_province_zone_table()

    # Handle split provinces
    if province == "Isabela":
        if municipality in ISABELA_ZONE_IV_MUNICIPALITIES:
            return Zone.IV  # EPSG:3124
        else:
            return Zone.III  # EPSG:3123 (default for Isabela)

    if province == "Quezon":
        if municipality in QUEZON_ZONE_IV_MUNICIPALITIES:
            return Zone.IV
        if municipality in QUEZON_POLILLO_MUNICIPALITIES:
            return Zone.III  # Polillo explicitly Zone III
        else:
            return Zone.III  # default

    if province == "Cebu":
        if municipality in CEBU_CAMOTES_MUNICIPALITIES:
            return Zone.V  # EPSG:3125
        else:
            return Zone.IV  # EPSG:3124

    if province == "Palawan":
        return Zone.PALAWAN_SPECIAL  # CM 118°30'E, custom proj

    # Standard lookup
    return zone_table[normalize_province_name(province)]
```

**Province name normalization** is needed because titles may use:
- Old names: "Compostela Valley" -> Davao de Oro (Zone V)
- Pre-split names: "Maguindanao" -> Maguindanao del Norte or del Sur (both Zone V)
- Variant spellings: "Cotabato" vs "North Cotabato"

---

## 7. Compact Lookup Table (for implementation)

```python
# Province -> (Zone, EPSG) mapping
# For split provinces, the "primary" zone is listed
PROVINCE_ZONE_MAP = {
    # Zone I(a) - Special
    "Palawan":                 ("I(a)", 3121),  # CM 118°30'E, NOT standard 3121

    # Zone III
    "Abra":                    ("III", 3123),
    "Apayao":                  ("III", 3123),
    "Benguet":                 ("III", 3123),
    "Ifugao":                  ("III", 3123),
    "Kalinga":                 ("III", 3123),
    "Mountain Province":       ("III", 3123),
    "Metro Manila":            ("III", 3123),
    "Ilocos Norte":            ("III", 3123),
    "Ilocos Sur":              ("III", 3123),
    "La Union":                ("III", 3123),
    "Pangasinan":              ("III", 3123),
    "Batanes":                 ("III", 3123),
    "Cagayan":                 ("III", 3123),
    "Isabela":                 ("III", 3123),  # PRIMARY; east of 122°E = Zone IV
    "Nueva Vizcaya":           ("III", 3123),
    "Quirino":                 ("III", 3123),
    "Aurora":                  ("III", 3123),
    "Bataan":                  ("III", 3123),
    "Bulacan":                 ("III", 3123),
    "Nueva Ecija":             ("III", 3123),
    "Pampanga":                ("III", 3123),
    "Tarlac":                  ("III", 3123),
    "Zambales":                ("III", 3123),
    "Batangas":                ("III", 3123),
    "Cavite":                  ("III", 3123),
    "Laguna":                  ("III", 3123),
    "Quezon":                  ("III", 3123),  # PRIMARY; east of 122°E = Zone IV
    "Rizal":                   ("III", 3123),
    "Marinduque":              ("III", 3123),
    "Occidental Mindoro":      ("III", 3123),
    "Oriental Mindoro":        ("III", 3123),
    "Sulu":                    ("III", 3123),
    "Tawi-Tawi":               ("III", 3123),

    # Zone IV
    "Romblon":                 ("IV", 3124),
    "Albay":                   ("IV", 3124),
    "Camarines Norte":         ("IV", 3124),
    "Camarines Sur":           ("IV", 3124),
    "Catanduanes":             ("IV", 3124),
    "Masbate":                 ("IV", 3124),
    "Sorsogon":                ("IV", 3124),
    "Aklan":                   ("IV", 3124),
    "Antique":                 ("IV", 3124),
    "Capiz":                   ("IV", 3124),
    "Guimaras":                ("IV", 3124),
    "Iloilo":                  ("IV", 3124),
    "Negros Occidental":       ("IV", 3124),
    "Cebu":                    ("IV", 3124),  # Camotes Islands = Zone V
    "Negros Oriental":         ("IV", 3124),
    "Siquijor":                ("IV", 3124),
    "Zamboanga del Norte":     ("IV", 3124),
    "Zamboanga del Sur":       ("IV", 3124),
    "Zamboanga Sibugay":       ("IV", 3124),
    "Basilan":                 ("IV", 3124),

    # Zone V
    "Biliran":                 ("V", 3125),
    "Eastern Samar":           ("V", 3125),
    "Leyte":                   ("V", 3125),
    "Northern Samar":          ("V", 3125),
    "Samar":                   ("V", 3125),
    "Southern Leyte":          ("V", 3125),
    "Bohol":                   ("V", 3125),
    "Bukidnon":                ("V", 3125),
    "Camiguin":                ("V", 3125),
    "Lanao del Norte":         ("V", 3125),
    "Misamis Occidental":      ("V", 3125),
    "Misamis Oriental":        ("V", 3125),
    "Davao de Oro":            ("V", 3125),
    "Davao del Norte":         ("V", 3125),
    "Davao del Sur":           ("V", 3125),
    "Davao Occidental":        ("V", 3125),
    "Davao Oriental":          ("V", 3125),
    "Cotabato":                ("V", 3125),
    "Sarangani":               ("V", 3125),
    "South Cotabato":          ("V", 3125),
    "Sultan Kudarat":          ("V", 3125),
    "Agusan del Norte":        ("V", 3125),
    "Agusan del Sur":          ("V", 3125),
    "Dinagat Islands":         ("V", 3125),
    "Surigao del Norte":       ("V", 3125),
    "Surigao del Sur":         ("V", 3125),
    "Lanao del Sur":           ("V", 3125),
    "Maguindanao del Norte":   ("V", 3125),
    "Maguindanao del Sur":     ("V", 3125),
}

# Aliases for name normalization
PROVINCE_ALIASES = {
    "Compostela Valley":       "Davao de Oro",
    "North Cotabato":          "Cotabato",
    "Maguindanao":             "Maguindanao del Sur",  # default to del Sur (larger area)
    "Western Samar":           "Samar",
    "Shariff Kabunsuan":       "Maguindanao del Norte",  # abolished province
    "NCR":                     "Metro Manila",
    "National Capital Region": "Metro Manila",
}

# Municipalities in split-zone provinces
ISABELA_ZONE_IV_MUNICIPALITIES = [
    # Municipalities east of 122°E longitude
    # (To be populated from detailed DAO 98-12 annex or NAMRIA data)
]

QUEZON_ZONE_IV_MUNICIPALITIES = [
    # Municipalities east of 122°E longitude (excluding Polillo)
    # (To be populated from detailed DAO 98-12 annex or NAMRIA data)
]

CEBU_CAMOTES_MUNICIPALITIES = [
    "Poro",
    "Tudela",
    "San Francisco",
    "Pilar",
]
```

---

## 8. Projection Definition for Palawan (Zone I-a)

Since Palawan uses a non-standard central meridian not matching any EPSG code, the projection must be defined manually:

```
# PROJ4 string for Palawan (DAO 98-12 Zone I-a)
+proj=tmerc +lat_0=0 +lon_0=118.5 +k=0.99995 +x_0=500000 +y_0=0 +ellps=clrk66 +towgs84=-127.62,-67.24,-47.04,3.068,-4.903,-1.578,-1.06 +units=m +no_defs

# WKT (abbreviated)
PROJCS["PRS92 / Philippines Zone I(a) Palawan",
  GEOGCS["PRS92", DATUM["Philippine_Reference_System_1992",
    SPHEROID["Clarke 1866", 6378206.4, 294.978698213898],
    TOWGS84[-127.62, -67.24, -47.04, 3.068, -4.903, -1.578, -1.06]],
  PRIMEM["Greenwich", 0],
  UNIT["degree", 0.0174532925199433]],
  PROJECTION["Transverse_Mercator"],
  PARAMETER["latitude_of_origin", 0],
  PARAMETER["central_meridian", 118.5],
  PARAMETER["scale_factor", 0.99995],
  PARAMETER["false_easting", 500000],
  PARAMETER["false_northing", 0],
  UNIT["metre", 1]]
```

---

## 9. Sources

1. **DAO 98-12** -- DENR Administrative Order No. 98-12, "Revised Manual for Land Surveying Regulations in the Philippines" (1998), Section 65: Zone Assignment of Provinces
2. **DAO 2005-13** -- DENR Administrative Order No. 2005-13, "Revised Guidelines for the Implementation of PRS92" (2005)
3. **EPSG Registry** -- epsg.io codes 3121-3125 (NAMRIA/CGSD as information source)
4. **Studocu reproduction** -- "List of PTM Zoning per Province DAO 98-12" (Bicol University, BS Geodetic Engineering)
5. **Course Hero reproduction** -- "PPCS-PTM Zone Assignment of Provinces with GIS Subject"
6. **Quizlet flashcards** -- "PPCS-PTM Zone Assignment of Provinces"
7. **Scribd** -- "PPCS-PTM Zone Assignments PDF" and "DAO 98-12 by Engr. Broddett B. Abatayo"
