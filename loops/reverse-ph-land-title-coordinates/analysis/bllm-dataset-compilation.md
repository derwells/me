# Analysis: BLLM Dataset Compilation

**Aspect:** bllm-dataset-compilation (Wave 2)
**Date:** 2026-02-26
**Depends on:** bllm-database-sources (Wave 1), prs92-datum-parameters (Wave 1), province-zone-mapping (supplementary)
**Verification:** Province→zone mapping verified against DAO 98-12 + EPSG registry via subagent. Dataset characteristics verified against raw tiepoints.json via subagent. Monument type abbreviations cross-checked against DENR DAO 72 and DAO 98-48.

---

## Summary

The primary BLLM dataset is TitlePlotterPH's `tiepoints.json` (85,303 records, 117 provinces, ~50k cadastral monuments + ~16k PRS92 geodetic control points). This analysis specifies the engine's enriched dataset structure, zone inference logic, datum inference logic, name normalization, coverage statistics by region, and the lookup algorithm. Three GeoIDEx records provide independent cross-reference points with both PTM grid and PRS92 geographic coordinates. The engine must also support caller-provided BLLM coordinates for monuments absent from the embedded dataset.

---

## 1. Source Dataset: tiepoints.json

### 1.1 Raw Structure

**File:** `resources/tiepoints.json` in TitlePlotterPH QGIS plugin
**Size:** 15.9 MB (16,645,674 bytes)
**Format:** JSON array of flat objects
**Total records:** 85,303
**Unique provinces:** 117 (includes cities listed as provinces: Manila, Quezon City, Makati, etc.)
**Unique province-municipality pairs:** 1,983
**Records with null Municipality:** 2,907

```json
{
  "Tie Point Name": "BLLM 1",
  "Description": "BLLM No. 1, Cad 614-D, Municipality of Botolan, Province of Zambales",
  "Province": "ZAMBALES",
  "Municipality": "BOTOLAN",
  "Northing": 1691760.514,
  "Easting": 394854.244
}
```

### 1.2 Coordinate Ranges

| Metric | Value |
|--------|-------|
| Northing min | 517,288.414 m (~4.7°N, Tawi-Tawi) |
| Northing max | 2,299,151.130 m (~20.8°N, Batanes) |
| Easting min | 54,725.020 m (~4° from CM) |
| Easting max | 1,116,895.955 m (likely data error or different projection) |
| Typical Easting range | 390,000 – 610,000 m (within ±1° of CM) |

**Data quality note:** 1 record has `" "` (string) for Northing. The engine loader must filter non-numeric coordinates.

### 1.3 Record Types by Monument Category

| Type | Prefix | Count | Full Name | Datum Likelihood |
|------|--------|-------|-----------|-----------------|
| BBM | BBM | 26,155 | Barangay Boundary Monument | Luzon 1911 |
| BLLM | BLLM | 19,568 | Bureau of Lands Location Monument | Luzon 1911 |
| PRS 92 | Province codes | 15,609 | PRS92 Geodetic Control Points | PRS92 (explicit) |
| MBM | MBM | 9,174 | Municipal Boundary Monument | Luzon 1911 |
| BLBM | BLBM | 4,850 | Bureau of Lands Barrio Monument | Luzon 1911 |
| Monument | MON | 1,372 | General Monuments | Luzon 1911 |
| Triangulation | TS | 1,085 | C&GS Triangulation Stations | Luzon 1911 |
| PBM | PBM | 788 | Provincial Boundary Monument | Luzon 1911 |
| Other | Various | 6,702 | P-points, boundary descriptions, misc | Unknown |

**Correction from verification:** BBM = **Barangay** (formerly Barrio) Boundary Monument, NOT "Bureau of Lands Boundary Monument." Confirmed by DENR DAO 72 and DENR DAO 98-48.

---

## 2. Zone Inference Logic

### 2.1 Problem

The tiepoints.json file does **not** store a PTM zone per record. All five PTM zones use identical False Easting (500,000 m), so Easting values overlap completely across zones. Zone cannot be determined from coordinates alone.

### 2.2 Solution: Province-Based Zone Lookup

Zone is determined by the Province field using the DAO 98-12 mapping table. Full mapping documented in `analysis/province-zone-mapping.md`.

**Zone distribution of the 85,303 tiepoints.json records (by province):**

| Zone | Record Count | % of Dataset | Central Meridian |
|------|-------------|-------------|-----------------|
| I(a) — Palawan | 1,686 | 2.0% | 118°30'E (special) |
| III | 41,282 | 48.4% | 121°E |
| IV | 24,917 | 29.2% | 123°E |
| V | 17,418 | 20.4% | 125°E |
| **Total** | **85,303** | **100%** | |

Zone II has no assigned provinces per DAO 98-12.

### 2.3 Zone Inference Algorithm

```
function infer_zone(province: str, municipality: str | None) -> ZoneDefinition:
    # Normalize province name
    province = normalize_province(province)

    # Handle split provinces requiring municipality
    if province == "ISABELA" and municipality in ISABELA_ZONE_IV_SET:
        return ZONE_IV
    if province == "QUEZON" and municipality in QUEZON_ZONE_IV_SET:
        return ZONE_IV
    if province == "CEBU" and municipality in CAMOTES_SET:
        return ZONE_V

    # Standard lookup from DAO 98-12 table
    return PROVINCE_ZONE_TABLE[province]
```

### 2.4 Province Name Normalization

The Province field in tiepoints.json uses ALL CAPS. Additional normalizations needed:

| Raw Province | Normalized | Zone | Notes |
|-------------|-----------|------|-------|
| MANILA | Metro Manila | III | Listed as province in dataset |
| QUEZON CITY | Metro Manila | III | Listed as province in dataset |
| MAKATI | Metro Manila | III | Listed as province in dataset |
| COTABATO | Cotabato (North Cotabato) | V | Not Cotabato City |
| DAVAO DEL SUR | Davao del Sur | V | May include pre-2013 Davao Occidental areas |
| COMPOSTELA VALLEY | Davao de Oro | V | Old province name |

The engine must maintain a `province_alias` table mapping tiepoints.json province names to canonical DAO 98-12 names.

### 2.5 Easting Sanity Check

After zone assignment, validate that the Easting value is consistent:
- **Normal range:** 390,000 – 610,000 m (within ±1° of CM)
- **Warning range:** 350,000 – 650,000 m (within ±1.5° of CM)
- **Error range:** < 350,000 or > 650,000 m → likely wrong zone or data error

For split provinces (Isabela, Quezon), an Easting > 611,000 in Zone III suggests the record may belong to Zone IV.

---

## 3. Datum Inference Logic

### 3.1 Problem

The tiepoints.json file mixes Luzon 1911 and PRS92 coordinates **without a per-record datum field**. The two datums differ by approximately **7–13 meters** in grid coordinates (empirically confirmed by subagent comparing co-located monuments). Using wrong-datum coordinates would introduce this error directly into the traverse starting point.

**Correction from verification:** The Luzon 1911 → PRS92 shift is ~7–13 m, NOT 100–300 m. The ~150–170 m figure applies to Luzon 1911 → WGS84. These are different transformations.

### 3.2 Detection Rules

| Rule | Indicator | Inferred Datum | Confidence |
|------|-----------|---------------|------------|
| R1 | Description contains "PRS 92" or "PRS-92" | PRS92 | High |
| R2 | Tie Point Name has province-code prefix (e.g., ABY, BLN, QZN) | PRS92 | High |
| R3 | Description contains "Cad" or "Pls" (cadastral/public land survey ref) | Luzon 1911 | Medium-High |
| R4 | Description contains "Mcadm" | Luzon 1911 | Medium |
| R5 | No datum indicators | Unknown — flag for review | Low |

### 3.3 Empirical Datum Breakdown

From subagent analysis of all 85,303 records:

| Datum | Detection Rule | Record Count | % |
|-------|---------------|-------------|---|
| PRS92 | R1+R2 (Description has "PRS 92") | 15,734 | 18.4% |
| Luzon 1911 | R3+R4 (Description has "Cad"/"Pls"/"Mcadm") | 56,320 | 66.0% |
| Unknown | No clear indicator | 13,249 | 15.5% |

### 3.4 Empirical Datum Shift Magnitude

The subagent found co-located monuments (same BLLM at same physical location) appearing in both datums:

| Monument | Luzon 1911 N | PRS92 N | Luzon 1911 E | PRS92 E | 2D Shift (m) |
|----------|-------------|---------|-------------|---------|-------------|
| BLLM 5, La Trinidad (Benguet) | 1,823,343.414 | 1,823,335.928 | 453,935.840 | 453,941.193 | 9.2 |
| BLLM 6, La Trinidad (Benguet) | — | — | — | — | 9.1 |
| BLLM 1, Kabayan (Benguet) | — | — | — | — | 7.2 |
| CBM 2, Baguio Townsite | — | — | — | — | 13.4 |

**Summary:** Luzon 1911 → PRS92 grid shift is ~7–13 m in Benguet (Zone III). Shift magnitude varies regionally.

### 3.5 Datum Handling Strategy for Engine

1. **Always store the inferred datum per record** in the enriched dataset.
2. **PRS92 records are preferred** — they match the engine's primary PRS92 pipeline without transformation.
3. **Luzon 1911 records require adjustment** — apply the Luzon 1911 → PRS92 transform documented in `analysis/luzon1911-to-prs92-transform.md`:
   - **Path A (default):** 3-parameter geocentric translation (EPSG:1161 or EPSG:1162), ~17–44 m accuracy on geographic coordinates; on grid coordinates the shift is ~7–13 m.
   - **Path B (if CE/CN available):** 4-parameter conformal (DENR MC 2010-06), ~10 cm accuracy.
4. **Unknown-datum records:** Flag with `datum_confidence: "low"` and default to PRS92 interpretation (smaller error if wrong vs. applying an unnecessary datum shift).
5. **Survey plan datum takes precedence** — if the title's survey plan specifies PRS92 or a pre-1993 vintage, that overrides the BLLM's inferred datum.

---

## 4. Coverage Analysis by Region

### 4.1 Records Per Region

| Region | Zone(s) | Records | Provinces | Coverage Quality |
|--------|---------|---------|-----------|-----------------|
| Region I (Ilocos) | III | 9,420 | 4 | Good |
| Region II (Cagayan Valley) | III/IV | 5,371 | 5 | Good |
| Region III (Central Luzon) | III | 11,765 | 7 | Good |
| NCR (Metro Manila) | III | 1,038 | 1* | Moderate (fragmented by city-as-province) |
| CALABARZON (IV-A) | III | 10,837 | 5 | Good |
| MIMAROPA (IV-B) | I(a)/III/IV | 4,237 | 5 | Moderate (Palawan sparse) |
| CAR (Cordillera) | III | 2,808 | 6 | Moderate (mountainous terrain) |
| Region V (Bicol) | IV | 6,605 | 6 | Good |
| Region VI (W. Visayas) | IV | 9,284 | 6 | Good |
| Region VII (C. Visayas) | IV/V | 5,839 | 4 | Good |
| Region VIII (E. Visayas) | V | 4,268 | 6 | Moderate |
| Region IX (Zamboanga) | IV | 2,542 | 3 | Moderate |
| Region X (N. Mindanao) | V | 3,850 | 5 | Moderate |
| Region XI (Davao) | V | 3,424 | 5 | Moderate |
| Region XII (SOCCSKSARGEN) | V | 2,755 | 4 | Moderate |
| Region XIII (Caraga) | V | 3,153 | 5 | Moderate |
| BARMM | III/IV/V | 2,107 | 5+ | Poor (severely incomplete) |

*NCR records are split across Manila, Quezon City, Makati, etc. as separate "provinces" in the dataset.

### 4.2 Bottom 15 Provinces by Record Count

| Province | Records | Region | Zone | Notes |
|----------|---------|--------|------|-------|
| DINAGAT ISLANDS | 0 | Caraga | V | Not in dataset (created 2006) |
| DAVAO OCCIDENTAL | 0 | Davao | V | Not in dataset (created 2013) |
| MAGUINDANAO DEL NORTE | 0 | BARMM | V | Not in dataset (split 2022) |
| MAGUINDANAO DEL SUR | 0 | BARMM | V | Not in dataset (split 2022) |
| BATANES | 148 | Region II | III | Small island province |
| CAMIGUIN | 165 | Region X | V | Small island province |
| SIQUIJOR | 191 | Region VII | IV | Small island province |
| GUIMARAS | 238 | Region VI | IV | Small island province |
| BILIRAN | 258 | Region VIII | V | Small province |
| MARINDUQUE | 284 | MIMAROPA | III | Island province |
| SULU | 325 | BARMM | III | Conflict-affected |
| TAWI-TAWI | 198 | BARMM | III | Conflict-affected |
| APAYAO | 198 | CAR | III | Mountainous, sparse |
| MAKATI | 63 | NCR | III | City-as-province artifact |
| BASILAN | 374 | BARMM | IV | Conflict-affected |

### 4.3 Coverage Gaps Summary

**Critical gaps (no/minimal data):**
1. **Post-2006 provinces** — Dinagat Islands, Davao Occidental, Maguindanao del Norte/del Sur: zero records. Covered by parent province records (Surigao del Norte, Davao del Sur, Maguindanao).
2. **BARMM interior** — Lanao del Sur (785 records) and Maguindanao (1,024 combined as old province) have limited coverage relative to land area. Many rural municipalities lack monuments.
3. **CAR mountain areas** — Mountain Province (185), Kalinga (252), Ifugao (215), Apayao (198): mountainous terrain with limited cadastral surveys.

**Moderate gaps:**
4. **NCR fragmentation** — Metro Manila records are split across Manila (233), Quezon City (345), Makati (63), etc. as separate provinces. Need to aggregate under "Metro Manila" for lookup.
5. **Palawan** — 1,686 records but very large land area; interior municipalities underrepresented.
6. **Rural Mindanao** — Several provinces have moderate count but large area (Sultan Kudarat 534, Cotabato 686, Bukidnon 1,450 relative to its large area).

**Well-covered provinces (top 5):**
- Iloilo: 4,618
- Pangasinan: 4,363
- Quezon: 4,288
- Bohol: 3,265
- Batangas: 2,841

### 4.4 Municipality Coverage Depth

Of the 1,983 unique province-municipality pairs in the dataset, many municipalities have only 1-5 monuments. The engine must expect that for any given technical description, the specific BLLM may not be in the database. The caller-provided BLLM coordinate fallback is essential.

---

## 5. Cross-Reference Data: GeoIDEx

GeoIDEx (cadastre.geoidex.com) provides ~200 demonstration records for Region III (Nueva Ecija), with both PTM grid coordinates AND PRS92 geographic coordinates. These serve as ground truth for validating the engine's inverse TM computation.

### 5.1 Cross-Reference Points

| Monument | Province | PTM Northing (m) | PTM Easting (m) | PRS92 Lat (°) | PRS92 Lng (°) | Datum | Zone |
|----------|----------|------------------|-----------------|----------------|----------------|-------|------|
| BLLM-87 | Nueva Ecija | (in dataset) | (in dataset) | 15.28093399 | 120.96881830 | PRS92 | III |
| BLLM-100 | Nueva Ecija | 1,706,822.866 | 492,272.848 | 15.22194556 | 120.93101400 | PRS92 | III |
| BLLM-154 | Nueva Ecija | (in dataset) | 1,706,822.866 | 15.41223014 | 120.93774460 | PRS92 | III |

### 5.2 Validation Use

For BLLM-100:
- **Given:** Northing = 1,706,822.866 m, Easting = 492,272.848 m, Zone III (CM 121°E)
- **Expected PRS92 geographic:** Lat = 15.22194556°, Lng = 120.93101400°
- **Engine should compute:** Inverse TM from PTM Zone III → PRS92 geographic, then Helmert to WGS84
- **Cross-check:** Inverse TM result should match GeoIDEx PRS92 lat/lng to < 1 mm

These points are documented for use in Wave 3 test vectors.

---

## 6. Enriched Dataset Structure for Engine

### 6.1 Per-Record Schema

The engine's embedded dataset enriches the raw tiepoints.json with inferred fields:

```json
{
  "name": "BLLM 1",
  "name_normalized": "BLLM 1",
  "description": "BLLM No. 1, Cad 614-D, Municipality of Botolan, Province of Zambales",
  "province": "ZAMBALES",
  "province_normalized": "ZAMBALES",
  "municipality": "BOTOLAN",
  "northing": 1691760.514,
  "easting": 394854.244,
  "zone": 3,
  "zone_cm": 121.0,
  "datum": "Luzon1911",
  "datum_confidence": "medium-high",
  "datum_detection_rule": "R3",
  "monument_type": "BLLM",
  "source": "LMB-tiepoints"
}
```

### 6.2 Added Fields

| Field | Type | Derivation |
|-------|------|-----------|
| `name_normalized` | string | Uppercase, whitespace-compressed, "No." removed |
| `province_normalized` | string | Mapped through alias table to canonical DAO 98-12 name |
| `zone` | int (1-5) | Province-based lookup per DAO 98-12 |
| `zone_cm` | float | Central meridian in degrees (118.5 for Palawan, 121/123/125 for others) |
| `datum` | "PRS92" \| "Luzon1911" \| "Unknown" | Inferred from Description field per rules in Section 3.2 |
| `datum_confidence` | "high" \| "medium-high" \| "low" | Based on detection rule strength |
| `datum_detection_rule` | string | Which rule triggered (R1-R5) |
| `monument_type` | string | Parsed from Tie Point Name prefix (BLLM, BBM, MBM, etc.) |
| `source` | string | Always "LMB-tiepoints" for embedded dataset |

### 6.3 Data Quality Filters Applied During Enrichment

1. **Drop non-numeric coordinates:** Filter records where Northing or Easting is not a number (1 record known: `" "` Northing).
2. **Drop null Tie Point Name or Province:** Already handled in raw data (0 nulls in these fields).
3. **Municipality null fallback:** 2,907 records have null Municipality. Leave as null in enriched data — lookup algorithm handles this.
4. **Easting sanity check:** Flag records with Easting < 200,000 or > 800,000 for manual review (may indicate wrong zone or non-PTM coordinates).

---

## 7. Lookup Algorithm

### 7.1 Name Normalization

Technical descriptions reference monuments in varied formats:

| Tech Description Text | Parsed Name | Normalization |
|----------------------|-------------|---------------|
| "BLLM No. 1, Cad. 614-D" | BLLM 1 | Remove "No.", compress whitespace |
| "B.L.L.M. 1" | BLLM 1 | Remove dots |
| "BBM # 22" | BBM 22 | Remove "#" |
| "Cor. Sts. 1 & 2, Blk. 10" | COR STS 1 & 2 BLK 10 | Uppercase, remove dots |
| "BLLM 1, Legazpi Cad-47" | BLLM 1 | Name is just "BLLM 1"; cadastral ref extracted separately |

Normalization function:
```
function normalize_name(raw_name: str) -> str:
    name = raw_name.upper()
    name = name.replace("NO.", "").replace("NO ", " ")
    name = name.replace("#", "")
    name = re.sub(r'\.(?=[A-Z])', '', name)  # Remove dots in abbreviations
    name = re.sub(r'\s+', ' ', name).strip()
    return name
```

### 7.2 Three-Tier Lookup

```
function lookup_bllm(name, province=None, municipality=None,
                     cadastral_ref=None) -> BLLMRecord | Error:

    normalized = normalize_name(name)

    # === Tier 1: Exact name match ===
    candidates = filter(dataset, name_normalized == normalized)

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) == 0:
        # Try fuzzy: "BLLM 1, LEGAZPI CAD-47" might be stored as
        # just "BLLM 1" with "Cad 614-D" in Description
        candidates = filter(dataset, name_normalized.startswith(normalized))

    if len(candidates) == 0:
        raise BLLMNotFound(name, province, municipality)

    # === Tier 2: Narrow by province ===
    if province:
        prov_norm = normalize_province(province)
        prov_candidates = filter(candidates, province_normalized == prov_norm)
        if len(prov_candidates) >= 1:
            candidates = prov_candidates

    if len(candidates) == 1:
        return candidates[0]

    # === Tier 3: Narrow by municipality or cadastral reference ===
    if municipality:
        muni_candidates = filter(candidates,
            municipality and municipality.upper().contains(municipality.upper()))
        if len(muni_candidates) >= 1:
            candidates = muni_candidates

    if cadastral_ref:
        cad_candidates = filter(candidates,
            description.upper().contains(cadastral_ref.upper()))
        if len(cad_candidates) >= 1:
            candidates = cad_candidates

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:
        raise AmbiguousBLLM(candidates)

    raise BLLMNotFound(name, province, municipality)
```

### 7.3 Disambiguation Statistics

Common name collisions in the dataset:

| Name | Occurrences | Notes |
|------|-------------|-------|
| BLLM 1 | ~800+ | Every cadastral survey has a "BLLM 1" — Province is essential |
| BBM 1 | ~600+ | Same pattern |
| MBM 1 | ~200+ | Same pattern |

**Province disambiguates in >95% of cases.** Municipality further narrows the remaining cases. The cadastral reference in the Description (e.g., "Cad 614-D") is the final disambiguator.

---

## 8. Engine API for BLLM Resolution

### 8.1 Input Interface

```
resolve_bllm(
    # From parsed technical description
    monument_name: str,           # "BLLM 1"
    cadastral_reference: str,     # "Cad 614-D" (from tie block or survey footer)
    province: str | None,         # From title metadata or survey plan
    municipality: str | None,     # From title metadata or tech description

    # Caller-provided override (bypasses lookup entirely)
    override_northing: float | None,
    override_easting: float | None,
    override_zone: int | None,    # 1-5
    override_datum: str | None,   # "PRS92" or "Luzon1911"
) -> BLLMResult
```

### 8.2 Output Interface

```
BLLMResult:
    northing: float              # PTM Northing in metres
    easting: float               # PTM Easting in metres
    zone: int                    # 1-5
    zone_cm: float               # Central meridian in degrees
    datum: str                   # "PRS92" or "Luzon1911"
    datum_confidence: str        # "high", "medium-high", "low"
    source: str                  # "embedded-dataset", "caller-provided"
    monument_name: str           # Matched name
    warnings: list[str]          # e.g., ["datum_inferred_from_description",
                                 #        "multiple_candidates_narrowed_by_province"]
```

### 8.3 BLLM-to-Traverse Handoff

After BLLM resolution, the engine uses the result to initialize the traverse:
1. **If datum = PRS92:** Use Northing/Easting directly as the traverse starting point (BLLM coordinate).
2. **If datum = Luzon1911 and survey plan is PRS92:** Apply Luzon 1911 → PRS92 transformation to the BLLM coordinate before traverse. (See `analysis/luzon1911-to-prs92-transform.md`, Path A or Path B.)
3. **If datum = Luzon1911 and survey plan is Luzon 1911:** Use Northing/Easting directly. The entire traverse will be in Luzon 1911, and datum transformation happens after traverse completion.
4. **If datum = Unknown:** Default to PRS92 interpretation. Add warning.

The survey plan's datum (determined from plan vintage — pre-1993 = Luzon 1911, post-1993 = PRS92) dictates the coordinate reference system for the traverse computation, not the BLLM record's datum.

---

## 9. Dataset Size & Performance Considerations

| Metric | Value |
|--------|-------|
| Total records | 85,303 |
| Estimated JSON size (enriched) | ~25 MB |
| Estimated memory (in-memory DataFrame) | ~30–40 MB |
| Lookup time (indexed by name) | < 1 ms |
| Startup load time | < 2 seconds |

### 9.1 Indexing Strategy

For fast lookup, the engine should build these indexes at load time:
1. **Primary index:** `name_normalized` → list of records (hash map)
2. **Secondary index:** `(name_normalized, province_normalized)` → list of records
3. **Tertiary index:** `province_normalized` → list of records (for browsing)

### 9.2 Lazy Loading

The full 85,303-record dataset can be loaded once at engine initialization. For web/serverless deployments where cold start matters, consider:
- **Province-partitioned files:** Split into per-province JSON files, load only the relevant province.
- **SQLite:** Convert to indexed SQLite for O(log n) lookups without loading entire dataset.

---

## 10. Recommendations for Engine Implementation

1. **Bundle the enriched dataset** — Pre-process tiepoints.json at build time: add zone, datum, normalized names. Ship as a single JSON or SQLite file.

2. **Province alias table is critical** — NCR cities (Manila, Quezon City, Makati, etc.) must map to "Metro Manila." Old province names must map to current names. The tiepoints.json Province field is messy.

3. **Caller-provided BLLM coordinates must be first-class** — Given 15.5% unknown-datum records and significant coverage gaps (BARMM, CAR, post-2006 provinces), many titles will require caller-provided coordinates.

4. **Datum mismatch warning** — When the BLLM's inferred datum doesn't match the survey plan's expected datum, emit a warning but don't block computation. The ~7–13 m shift is significant for cadastral accuracy but may be acceptable for visualization/mapping use cases.

5. **GeoIDEx cross-reference** — The 3 GeoIDEx points (BLLM-87, BLLM-100, BLLM-154 in Nueva Ecija) provide ground truth for testing the inverse TM computation. Include in Wave 3 test vectors.

---

## Sources

1. **TitlePlotterPH tiepoints.json** — github.com/isaacenage/TitlePlotterPH/resources/tiepoints.json (85,303 records, verified via GitHub API)
2. **DAO 98-12** — DENR Administrative Order 98-12, Section 65: PPCS-PTM Zone Assignment of Provinces (verified via Studocu, Course Hero, Quizlet reproductions)
3. **EPSG Registry** — epsg.io codes 3121–3125, 4683, 15708 (IOGP/NAMRIA)
4. **DENR DAO 72** — Monument type abbreviation definitions: BLLM, BBM (Barangay BM), MBM, PBM
5. **DENR DAO 98-48** — Monument type abbreviation confirmation: "Bureau of Land Location Monuments (BLLM), Provincial Boundary Monuments (PBM), Municipal Boundary Monuments (MBM), Barrio Boundary Monuments (BBM)"
6. **GeoIDEx** — cadastre.geoidex.com, BLLM-87/100/154 cross-reference points (Region III, Nueva Ecija)
7. **Geoportal Philippines** — geoportal.gov.ph/gpapps/lotplotter, UserEcho topic #151 ("not all municipality has a complete tie point data")
8. **Subagent verification** — Province→zone mapping cross-checked against DAO 98-12 + EPSG + geographic longitude data (4 independent source categories). Dataset characteristics verified via direct tiepoints.json parsing. Monument types verified against DENR DAO 72 + DAO 98-48.
9. **Balicanta et al. (2019)** — "Linking the Different Coordinate Systems in the Philippines" (UNOOSA), confirming PRS92 retained most Luzon 1911 parameters to minimize coordinate changes.
