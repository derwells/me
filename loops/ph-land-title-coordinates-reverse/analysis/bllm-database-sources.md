# Analysis: BLLM Database Sources

**Aspect:** bllm-database-sources (Wave 1)
**Date:** 2026-02-25
**Sources:** TitlePlotterPH GitHub repo, Geoportal Philippines, cadastre.geoidex.com, pdfcoffee/Scribd BLLM PDFs, Geoportal userecho forums, NAMRIA/LMB/FOI portal

---

## Summary

Four distinct publicly accessible BLLM coordinate sources were identified. The most practically useful is the `tiepoints.json` embedded in the TitlePlotterPH QGIS plugin (15.9 MB; Northing/Easting PTM fields; province + municipality + name keying). The Geoportal Philippines Lot Plotter embeds the same LMB dataset but exposes it as WGS84 lat/lng via a web UI. Neither source is complete — "not all municipalities have complete tie point data" is explicitly acknowledged by Geoportal. The authoritative complete source is DENR-LMB, accessible only via formal request. Coverage gaps are severe in rural Mindanao and BARMM.

---

## Source 1: TitlePlotterPH — `resources/tiepoints.json`

**Repository:** github.com/isaacenage/TitlePlotterPH
**File:** `resources/tiepoints.json`
**File size:** 15.9 MB (GitHub blob truncated; raw content too large to fetch directly)
**Origin:** Land Management Bureau (LMB) dataset, bundled into QGIS plugin
**License:** Not stated; bundled as plugin data
**Last updated:** Per repo update history (active as of 2024–2025)

### Data Fields

Normalized by the plugin's `tie_point_selector_dialog.py` to title case:

| Field | Type | Description |
|---|---|---|
| `Tie Point Name` | string | Monument label, e.g. "BLLM 1, LEGAZPI CAD-47" |
| `Description` | string | Free-text description (may be empty) |
| `Province` | string | Province name, ALL CAPS in raw data |
| `Municipality` | string | Municipality/city name; falls back to Province if null |
| `Northing` | float | PTM Northing in metres |
| `Easting` | float | PTM Easting in metres |

### Loading & Lookup Logic

```python
# Loaded once at module level as pandas DataFrame
json_path = os.path.join(plugin_root, "resources", "tiepoints.json")
with open(json_path) as f:
    raw_data = json.load(f)
# Keys normalized: "PROVINCE" → "Province", etc.
# Rows with null Tie Point Name or Province dropped
# Null Municipality → Province fallback

# Lookup: filter by Province (exact dropdown), Municipality (substring),
# Tie Point Name (space/case-insensitive substring)
# Returns: {'northing': float, 'easting': float, 'Tie Point Name': str,
#            'Province': str, 'Municipality': str}
```

### Coordinate System

The `Northing` and `Easting` values are in **Philippine Transverse Mercator (PTM)** coordinates. For pre-1993 BLLMs, these are in the **Luzon 1911 (PPCS)** datum; for post-1993 re-surveyed monuments, they are in **PRS92**. The file does not tag individual records with a datum — the engine must infer from context (survey vintage, region, or explicit zone annotation on plan).

**Zone is NOT stored per record.** The PTM zone must be inferred from the province or from the survey plan annotation (e.g., "PTM Zone III").

### Sample Known Coordinates (from external PDF sources, same LMB dataset)

| Monument | Location | PTM Northing (m) | PTM Easting (m) | Notes |
|---|---|---|---|---|
| BLLM 1, LEGAZPI CAD-47 | Legazpi, Albay (Zone 4) | 1,454,486.511 | 581,400.656 | PPCS/Luzon 1911 |
| BLLM 1, DIPOLOG CAD | Dipolog, Zamboanga del Norte | 950,111.895 | 943,875.505 | PPCS/PPCS; zone uncertain |
| BLLM 1, CAPIZ CAD-133 | Capiz (Zone 4) | 1,082,794.520 | 1,260,930.953 | PPCS/Luzon 1911 |
| BLLM 1, CAG.DE ORO CAD-237 | Cagayan de Oro | 553,858.640 | 420,399.146 | PPCS |

### Engine Use

The engine queries this dataset using:
1. Monument name extracted from tech description (e.g., "BLLM 1, LEGAZPI CAD-47")
2. Province/municipality lookup for disambiguation when multiple BLLM 1 records exist
3. Returns Northing/Easting → used as starting coordinate for traverse

---

## Source 2: Geoportal Philippines Lot Plotter

**URL:** https://geoportal.gov.ph/gpapps/lotplotter
**Origin:** Same LMB dataset as TitlePlotterPH; embedded in NAMRIA/Geoportal web app
**Coordinate output:** WGS84 lat/lng (the app converts internally for display)
**Interface:** Web app — Province dropdown → Municipality dropdown → Tie Point Name dropdown
**Limitations:** Same incomplete coverage as LMB source; no bulk download; web UI only

### Relevant Details

- Tie points organized by Province → Municipality → Name hierarchy
- Returns WGS84 coordinates (not PTM Northing/Easting)
- "Not all municipalities have complete tie point data" — explicitly stated in forum support response (Geoportal userecho topic #151)
- 10m discrepancy warnings when using non-NAMRIA basemaps
- Cannot be programmatically queried (no public API documented)

### Engine Use

Not directly usable in automated engine — no bulk download or API. Useful for **manual verification** of computed coordinates during development.

---

## Source 3: GeoIDEx Cadastre Information System

**URL:** cadastre.geoidex.com/index.php/control-points/
**Coverage:** Limited — primarily Region III (Nueva Ecija, Central Luzon) demonstration data
**Note:** "For demonstration purposes only. Official data via DENR R3 LMS Office."

### Data Fields per Record

| Field | Value (BLLM-100 example) |
|---|---|
| Designation | BLLM No. 100 |
| Location | Gapan City, Nueva Ecija, Luzon |
| PRS92 lat/lng | Φ=15.22194556°, λ=120.93101400° |
| WGS84 lat/lng | (blank in demo) |
| PTM Grid Northing | 1,706,822.866 m |
| PTM Grid Easting | 492,272.848 m |
| Ellipsoidal height (WGS84) | 56.145 m |
| Ellipsoidal height (PRS92) | 0 m |
| Established | August 3, 2014 |
| Cadastral Survey | CAD-225 (BLLM-87), CAD-269 (BLLM-154) |

### Additional Samples

| Monument | Province | PRS92 Lat (°) | PRS92 Lng (°) |
|---|---|---|---|
| BLLM-87 | Gapan City, Nueva Ecija | 15.28093399 | 120.96881830 |
| BLLM-100 | Gapan City, Nueva Ecija | 15.22194556 | 120.93101400 |
| BLLM-154 | Sta. Rosa, Nueva Ecija | 15.41223014 | 120.93774460 |

**Key observation:** These GeoIDEx samples provide both PRS92 geographic AND PTM grid coordinates for the same point, enabling cross-check of PTM→PRS92 conversion. However coverage is limited (~200 demonstration records, all Region III).

### Engine Use

Provides independent PRS92 lat/lng coordinates — useful as **Wave 3 test vector ground truth** for monuments where PTM grid coordinates are available.

---

## Source 4: DENR-LMB via FOI / Official Request

**URL:** foi.gov.ph (eFOI portal)
**Coverage:** Complete national BLLM database — the authoritative source
**Access:** FOI request per province, or formal data sharing agreement with LMB
**Format:** Not standardized; historically delivered as PDF tables or Excel files
**Response time:** Variable; some FOI requests fulfilled within days, others months

### Known FOI Responses (from foi.gov.ph)

- "Bureau of Lands Location Monuments (BLLM) Coordinates" — FOI request fulfilled (Lanao del Sur)
- "List of BLLM Coordinates of the Philippines, and some Cadastral Maps" — FOI request filed

### Engine Use

Not integrated programmatically. The engine design should support **caller-provided BLLM coordinates** as an input parameter, covering the case where the BLLM is absent from the embedded dataset but was obtained from LMB.

---

## Coverage Analysis

### What Is Covered (tiepoints.json / Geoportal Lot Plotter)

Based on documented sources, the LMB dataset embedded in TitlePlotterPH contains BLLM data for the following regions (confirmed from published PDF data and forum reports):

| Region | Provinces with Known Coverage |
|---|---|
| NCR | Metro Manila municipalities (partial) |
| Region III | Bulacan (Angat, Baliuag, Bocaue, Calumpit, Hagonoy, Malolos, Marilao, Meycauayan, Norzagaray), Nueva Ecija |
| Region V | Albay (Legazpi, Bacacay, Namanday, Ligao — 100+ monuments) |
| Region VI | Capiz |
| Region VII | Cebu (CAD-12 Ext.) |
| Region VIII | Leyte (from tech-description-samples) |
| Region IX | Zamboanga del Norte (Dipolog) |
| Region X | Cagayan de Oro, Iligan City |
| CARAGA | Agusan del Norte, Surigao del Norte |

### Known Coverage Gaps

1. **Not all municipalities covered** — explicitly stated by Geoportal Philippines. Rural municipalities with few titling transactions are underrepresented.
2. **BARMM (Bangsamoro)** — Historically underserved cadastral surveys; expect significant gaps in Maguindanao, Lanao del Sur, Sulu, Tawi-Tawi.
3. **Mountain Province / Cordillera** — Complex terrain; limited cadastral surveys; gaps expected.
4. **Newer municipalities** — Municipalities created after the LMB dataset snapshot will not appear.
5. **CAR and MIMAROPA** — Coverage patchy; Palawan (Zone 2) especially uncertain.
6. **PTM zone ambiguity** — The dataset stores PTM N/E without zone tag. For monuments near zone boundaries, the zone cannot be determined from coordinates alone.

### Size Estimate

The tiepoints.json file is 15.9 MB. Assuming ~300 bytes per JSON record (with all fields), this suggests approximately **50,000–60,000 records**. However, actual coverage is uneven — densely surveyed provinces (Bulacan, Nueva Ecija) have many records while most of BARMM may have few.

---

## Data Structure for Engine Dataset

For the engine's embedded BLLM dataset, the recommended structure per record:

```json
{
  "name": "BLLM 1, LEGAZPI CAD-47",
  "province": "ALBAY",
  "municipality": "LEGAZPI",
  "northing": 1454486.511,
  "easting": 581400.656,
  "zone": 4,
  "datum": "Luzon1911",
  "source": "LMB-published",
  "confidence": "high"
}
```

**Added fields vs tiepoints.json:**
- `zone`: PTM zone (1–5), inferred from province/longitude or survey plan
- `datum`: "PRS92" or "Luzon1911" — inferred from monument establishment date or explicit source tag
- `source`: provenance for debugging
- `confidence`: "high" (official LMB), "medium" (secondary source), "low" (derived)

---

## Lookup Algorithm for Engine

```
function lookup_bllm(name, province, municipality):
  # 1. Exact match on name (normalized: uppercase, spaces compressed)
  candidates = filter(dataset, name_match=normalize(name))

  # 2. If multiple matches, narrow by province
  if len(candidates) > 1 and province:
    candidates = filter(candidates, province=normalize(province))

  # 3. Further narrow by municipality
  if len(candidates) > 1 and municipality:
    candidates = filter(candidates, municipality_contains=normalize(municipality))

  # 4. Return single match or raise AmbiguousBLLM error
  if len(candidates) == 1: return candidates[0]
  if len(candidates) == 0: raise BLLMNotFound(name, province, municipality)
  raise AmbiguousBLLM(candidates)
```

---

## Wave 2 Handoff Notes

- **bllm-dataset-compilation** (Wave 2): Build on this by extracting the actual tiepoints.json records. Since the raw file is 15.9 MB and not directly fetchable, the Wave 2 analysis should describe the dataset structure, document 20+ sample records from known sources, and characterize coverage by province count and region.
- **Zone inference**: Since tiepoints.json does not store zone per record, the `bllm-dataset-compilation` Wave 2 aspect should document the zone inference logic: use province → map to expected zone(s) → confirm against easting range.
- **Datum inference**: Monuments established before PRS92 adoption (pre-1993 or re-survey date) are Luzon 1911; post-1993 are PRS92. Since tiepoints.json doesn't store datum, the engine must infer from survey plan vintage (covered in luzon1911-to-prs92-transform aspect).
- **Caller-provided override**: Engine API must accept BLLM coordinates as an explicit parameter, bypassing the lookup entirely.

---

## Sources

- [TitlePlotterPH GitHub repo](https://github.com/isaacenage/TitlePlotterPH)
- [TitlePlotterPH dialogs/tie_point_selector_dialog.py](https://github.com/isaacenage/TitlePlotterPH/blob/main/dialogs/tie_point_selector_dialog.py)
- [Geoportal Philippines Lot Plotter](https://geoportal.gov.ph/gpapps/lotplotter)
- [Geoportal userecho: Search for Coordinates by BLLM Number and Locality](https://geoportalphteam.userecho.com/communities/1/topics/151-search-for-coordinates-by-bllm-number-and-locality)
- [GeoIDEx Cadastre Information System — BLLM-100](https://cadastre.geoidex.com/index.php/control-points-2/article/199-bllm-100)
- [GeoIDEx Cadastre Information System — BLLM-154](http://cadastre.geoidex.com/index.php/control-points/article/106-bllm-154)
- [GeoIDEx Survey Control Points — BLLM-87](https://cadastre.geoidex.com/index.php/survey-control-points-library/article/186-bllm-87)
- [BLLM Coordinates PDF (pdfcoffee)](https://pdfcoffee.com/bllm-coordinates-3-pdf-free.html)
- [FOI Request: BLLM Coordinates](https://www.foi.gov.ph/requests/bureau-of-land-location-monuments-bllm-coordinates/)
- [FOI Request: List of BLLM Coordinates of the Philippines](https://www.foi.gov.ph/requests/list-of-bllm-coordinates-of-the-philippines-and-some-cadastral-maps/)
