# BIR Workbook Provincial Samples — Source Acquisition & Structural Survey

**Wave:** 1 — Source Acquisition
**Date:** 2026-03-02
**Aspect:** `bir-workbook-provincial-samples`

---

## Summary

7 provincial RDO zonal value workbooks were downloaded, extracted, and structurally analyzed, covering 4 geographic regions: Pangasinan (RR1), Laguna (RR9B), Cebu (RR13), and Davao (RR19). This provides a representative sample spanning urban provincial, semi-urban, rural agricultural, and island/Mindanao regions.

**Key finding:** Provincial workbooks are structurally MORE complex than NCR, not less. They are larger (up to 15,272 rows vs NCR max ~6,200), cover multiple municipalities per workbook (up to 16), have heavy agricultural code usage (2,800–3,900 agricultural rows per Pangasinan workbook), and introduce format heterogeneity _within_ a single workbook (different municipality sections use different header casing and punctuation).

---

## Inventory

### Files Downloaded (7 Provincial RDOs)

| RDO | City/Region | Revenue Region | Province | Format | File Size | Latest DO | Effectivity | Municipalities |
|-----|-------------|----------------|----------|--------|-----------|-----------|-------------|---------------|
| 4 | Calasiao, Central Pangasinan | RR1 | Pangasinan | .xls | 4.57 MB | DO 015-2023 | May 7, 2023 | 16 |
| 5 | Alaminos City, West Pangasinan | RR1 | Pangasinan | .xls | 3.14 MB | DO 082-2022 | Nov 29, 2022 | 16 |
| 56 | Calamba City, Central Laguna | RR9B | Laguna | .xls | 1.67 MB | DO 059-2023 | Oct 13, 2023 | 5+ (Calamba, Bay, Calauan, Los Baños, Victoria) |
| 57 | Biñan City, West Laguna | RR9B | Laguna | .xls | 1.58 MB | DO 055-2024 | Jul 4, 2024 | 4 (Biñan, Cabuyao, San Pedro, Sta. Rosa) |
| 81 | Cebu City North | RR13 | Cebu | **.xlsx** | 403 KB | DO 054-2023 | Oct 6, 2023 | 1 (Cebu City only) |
| 83 | Talisay City, Cebu | RR13 | Cebu | .xls | 2.33 MB | DO 060-2022 | Sep 22, 2022 | 2+ (Carcar City, Talisay City, + others) |
| 113A | West Davao City | RR19 | Davao del Sur | **.xlsx** | 678 KB | DO 032-2021 | Dec 22, 2021 | 1 (Davao City, 10 districts) |

### File Format Distribution
- **5 files:** .xls (BIFF8 / legacy Excel)
- **2 files:** .xlsx (OpenXML) — RDO 81 (Cebu City North), RDO 113A (West Davao)

**Also saved:**
- `bir-cms-api-provincial-data.json` — BIR CMS API responses for RR1, RR9B, RR13, RR19
- `RDO-57-Binan-City.pdf` — image-based PDF version (1.80 MB, requires OCR)

---

## Critical Structural Difference: Multi-Municipality Workbooks

The single most important finding is that **provincial workbooks cover multiple municipalities in a single workbook**, unlike NCR where each RDO roughly maps to one city/district.

| RDO | Municipalities Covered | Municipality Headers | Est. Total Data Rows |
|-----|----------------------|---------------------|---------------------|
| RDO-4 | 16 (Dagupan, San Carlos, Calasiao, Mangaldan, San Fabian, Santa Barbara, Laoac, Mapandan, San Jacinto, Alcala, Basista, Bautista, Bayambang, Malasiqui, Manaoag, Urbiztondo) | ~480+ | ~14,000 |
| RDO-5 | 16 (Lingayen, Alaminos, Agno, Aguilar, Anda, Bani, Binmaley, Bolinao, Bugallon, Burgos, Dasol, Infanta, Labrador, Mabini, Mangatarem, Sual) | ~350 | ~14,500 |
| RDO-56 | 5+ (Calamba, Bay, Calauan, Los Baños, Victoria) | ~130+ | ~4,400 |
| RDO-57 | 4 (Biñan City, Cabuyao City, San Pedro City, Sta. Rosa City) | ~100+ | ~3,800 |
| RDO-81 | 1 (Cebu City North — 80+ barangays) | ~80 | ~2,100 |
| RDO-83 | 2+ (Carcar City, Talisay City) | ~70+ | ~3,000 |
| RDO-113A | 1 city / 10 districts (Baguio, Calinan, Marilog, Talomo, Toril, Tugbok, Poblacion A-D) | ~150+ | ~3,700 |

**Parsing implication:** The data model must support a **Province → City/Municipality → Barangay → Street** hierarchy, not just the NCR-style **City → Barangay → Street** hierarchy. The parser must track municipality context transitions within a single sheet.

### Mixed Revision Numbers Within One DO

A single DO can contain different revision numbers for different municipalities. Example from RDO-4 (DO 015-2023):
- Dagupan, San Carlos, Calasiao, etc.: **5th Revision**
- Laoac, Mapandan, San Jacinto: **4th Revision**
- Alcala, Basista, Bautista, etc.: **3rd Revision**

**Parsing implication:** Revision number cannot be assumed constant per DO or per sheet. It must be tracked per municipality.

---

## Structural Analysis: Format Variations (Provincial-Specific)

### Municipality Header Heterogeneity Within Same Workbook

RDO-5 exhibits **4 different header formats for the same field within one sheet** — different municipalities were formatted by different people:

| Pattern | Example | Used For |
|---------|---------|----------|
| Mixed case, single colon | `City/Municipality: LINGAYEN` | Lingayen, Binmaley, Bugallon, Dasol, Sual |
| All caps, double colon | `CITY/MUNICIPALITY:: ALAMINOS CITY` | Alaminos City, Bani |
| All caps, spaced double colon | `CITY/MUNICIPALITY :: BOLINAO` | Bolinao |
| All caps, single colon | `CITY/MUNICIPALITY: INFANTA` | Infanta, Labrador, Mabini, Mangatarem |

**Parsing implication:** Municipality header detection must be case-insensitive and handle variable colon patterns (`:`, `::`, ` :: `).

### Province Header Variations

| Pattern | Example | Used By |
|---------|---------|---------|
| Split across cells | `Province \| PANGASINAN` (col 0 + col 1) | RDO-4, RDO-5, RDO-56, RDO-57 |
| Inline with colon | `PROVINCE                     : CEBU` (all in col 0) | RDO-83 |
| Colon in separate cell | `Province \| : \| CEBU` (col 0 + col 1 + col 2) | RDO-81 |

### Barangay Header Variations (Provincial)

| Pattern | Example | Used By |
|---------|---------|---------|
| `Zone/Barangay` + name | `Zone/Barangay \| POBLACION OESTE` | RDO-4, RDO-5 |
| `ZONE/ BARANGAY` inline | `ZONE/ BARANGAY     : BOLINAWAN` | RDO-83 |
| `Barangay` + colon cell + name | `Barangay \| : \| ADLAWON` | RDO-81 |
| `Zone/Barangay` + colon + numbered | `Zone/Barangay \| : BARANGAY NO. 1` | RDO-113A |
| Continuation marker | `Zone/Barangay \| POBLACION - continued` | RDO-5 |
| Continuation marker (Cebu) | `Barangay \| : \| APAS (continuation)` | RDO-81 |

**Note:** The "continuation" pattern indicates a barangay's data spans across a page break (the BIR header block is re-inserted mid-barangay). This is common in provincial workbooks due to their larger data volumes.

### Davao City District Structure

RDO-113A organizes by **districts** rather than independent municipalities:
```
Province: DAVAO DEL SUR
City/Municipality: DAVAO CITY
District: POBLACION A
Zone/Barangay: BARANGAY NO. 1
```

Barangays are **numbered** (BARANGAY NO. 1 through NO. 80+) rather than named, which is unique to Davao among our samples.

**Parsing implication:** Must handle numbered barangays and district-level hierarchy.

---

## Column Layout Analysis (Provincial)

### Standard 4-Column (All Provincial Workbooks)

All 7 provincial workbooks use a 4-column layout, but with **variable header text**:

| RDO | Col 0 Header | Col 1 Header | Col 2 Header | Col 3 Header |
|-----|-------------|-------------|-------------|-------------|
| 4 | STREET NAME / SUBDIVISION / CONDOMINIUM | VICINITY | CLASSIFI-CATION | 5TH REV ZV / SQM |
| 5 | STREET NAME /SUBDIVISION / CONDOMINIUM | VICINITY | CLASSI FICATION | 5th REVISION ZV.SQ.M |
| 56 | STREET NAME / SUBDIVISION/CONDOMINIUM | VICINITY | CLASSI- FICATION | 6TH REV ZV.SQ.M. |
| 57 | STREET NAME / SUBDIVISION/CONDOMINIUM | VICINITY | CLASSIFICATION | 6TH REV ZV.SQ.M |
| 81 | STREET NAME / SUBDIVISION/CONDOMINIUM | VICINITY | CLASSIFICATION | 5TH REVISION ZV/SQ.M |
| 83 | STREET NAME/ SUBDIVISION/CONDOMINIUM | VICINITY | CLASSIFICATION | 2ND REVISION ZV/SQ.M |
| 113A | STREET NAME / SUBDIVISION / CONDOMINIUM | VICINITY | CLASSIFICATION | 4TH REVISION ZV/SQ.M |

**Key finding:** The ZV column header embeds the revision number ("5TH REV", "6TH REV", "2ND REVISION", etc.). This varies by DO, not by RDO. A parser cannot assume a fixed header text — must match on "ZV" or "SQ.M" keywords.

**Parsing implication:** No Pattern B (5-column split vicinity) or Pattern D (10-column comparison) observed in provincial workbooks. The 4-column standard is consistent, but header text varies. Column detection must match on keywords, not exact strings.

### RDO-81 Cebu City: Apparent 10-Column But Really 7 Usable

RDO-81 reports 10 columns, but the actual data structure uses merged cells to create visual spacing:
```
Col 1-3: STREET NAME (merged)
Col 4-5: VICINITY (merged)
Col 6: CLASSIFICATION
Col 7: ZV/SQ.M
Col 8-10: empty
```

With 2,518 merges across 2,359 rows (1.07:1 ratio), virtually every row has at least one merged cell. This is the most merge-heavy workbook proportionally.

---

## Agricultural Data Analysis

### Agricultural Code Usage by Region

This is the **dominant difference** between provincial and NCR workbooks. NCR has essentially zero agricultural data; provincial workbooks are 20-40% agricultural.

| RDO | Region | Agri Rows | % of Data | Top Agricultural Codes |
|-----|--------|-----------|-----------|----------------------|
| 4 | Pangasinan | 3,917 | ~28% | A2 (unirrigated rice), A8 (nipa), A12 (orchard) |
| 5 | Pangasinan | 2,871 | ~20% | A2, A12, A50 (other agricultural) |
| 56 | Laguna | moderate | ~15% | A1 (irrigated rice), A50, GP (general purpose) |
| 57 | Laguna | 165 (A50) | ~8% | A50, GP, I (industrial) |
| 81 | Cebu North | 32 (A50) | ~3% | A50 only |
| 83 | Cebu/Talisay | 469+ | ~24% | A50, A49 (mountainous), A4 (coco), A15 (pasture), A16 (corn) |
| 113A | Davao | 1,150+ | ~46% | A14 (banana, 148), A50, A11 (abaca), A19 (cacao), A26 (bamboo) |

**Key patterns:**
1. **Mindanao (Davao) has the most diverse agricultural codes** — 20+ distinct A-codes used, with A14 (banana) being the most common, reflecting Davao's agricultural economy.
2. **Pangasinan** is dominated by A2 (unirrigated riceland) and A12 (orchard).
3. **Cebu North** barely uses agricultural codes (urban), while **Talisay** (semi-rural Cebu) has heavy agricultural data.
4. **Laguna** shows a transition: Biñan/Sta. Rosa (industrializing cities near NCR) have low agricultural, while Calamba/Bay/Calauan have more.

### Agricultural ZV Values

| Code | Description | ZV Range (PHP/sqm) | Typical Range |
|------|-------------|-------------------|---------------|
| A1 | Riceland Irrigated | 400 – 2,000 | 800 – 1,500 |
| A2 | Riceland Unirrigated | 300 – 1,800 | 400 – 1,000 |
| A4 | Coco Land | 500 – 1,000 | 600 – 900 |
| A12 | Orchard | 500 – 1,000 | 550 – 800 |
| A14 | Banana Land | 200 – 1,200 | 400 – 800 |
| A15 | Pasture Land | 200 – 900 | 300 – 600 |
| A24 | Mangrove | 500 – 1,300 | 800 – 1,200 |
| A39 | Seashore | 500 – 2,000 | 700 – 1,700 |
| A42 | Prawn Pond | 1,000 – 3,600 | 1,500 – 3,000 |
| A49 | Mountainous/Hilly | 75 – 500 | 100 – 300 |
| A50 | Other Agricultural | 100 – 4,100 | 500 – 2,000 |

**Parsing implication:** Agricultural ZVs are 1-3 orders of magnitude lower than urban RR/CR values. The parser must handle ZV values from PHP 25 to PHP 2,160,000 (a 5-order-of-magnitude range).

---

## Vicinity Pattern Taxonomy (Provincial)

Provincial workbooks use fundamentally different vicinity descriptors than NCR:

### NCR Pattern: Cross-Street Boundaries
```
SHAW BLVD | EDSA-WACK WACK CREEK | RR | 68,000
```

### Provincial Pattern: Road Proximity + Distance
```
ALL LOTS | ALONG NATIONAL HIGHWAY | CR | 12,000
         | ALONG PROVINCIAL ROAD  | CR |  8,000
         | ALONG BARANGAY ROAD    | RR |  4,000
         | 50 METERS INWARD       | RR |  3,000
         | INTERIOR LOT           | RR |  2,500
         | WATERSHED              | A50|    170
```

### Provincial Vicinity Hierarchy (observed patterns)

| Level | Pattern | Typical ZV Multiplier vs Interior |
|-------|---------|----------------------------------|
| 1 | `ALONG NATIONAL HIGHWAY` / `NATIONAL ROAD` | 2.0–3.0x |
| 2 | `ALONG PROVINCIAL ROAD` | 1.5–2.0x |
| 3 | `ALONG MUNICIPAL/CITY ROAD` | 1.2–1.5x |
| 4 | `ALONG BARANGAY ROAD` | 1.0–1.3x |
| 5 | `50 METERS INWARD` / `50 METERS AWAY FROM` | 0.7–1.0x |
| 6 | `INTERIOR` / `INTERIOR LOT` | 0.5–0.8x |
| 7 | `WATERSHED` / `MOUNTAINOUS AREA` | 0.1–0.3x |

**Parsing implication:** The address matching algorithm needs two modes:
1. **NCR mode:** Match specific street name + cross-street vicinity boundaries
2. **Provincial mode:** Match general area + road proximity class (national/provincial/barangay/interior)

### "SITIO" Location Specifier

Provincial workbooks (especially Cebu and Laguna) use "SITIO [name]" entries extensively:
```
SITIO CAMBUNTAN  |           | RR | 6,000
SITIO DUNGGOAN   |           | RR | 3,400
SITIO TUGAS      |           | RR | 2,000
SITIO PANABANG   |           | RR | 28,388
SITIO MAHAYAHAY  |           | RR | 23,725
```

A "sitio" is a sub-village/hamlet within a barangay — a level of geographic specificity below barangay that NCR workbooks don't use. Cebu City North (RDO-81) has extensive sitio entries.

---

## Merged Cell Analysis (Provincial)

| RDO | Current Sheet Merges | Rows | Merge Ratio | Severity |
|-----|---------------------|------|-------------|----------|
| 81 (Cebu City North) | 2,518 | 2,359 | **1.07** | **Extreme** |
| 5 (Alaminos) | 4,130 | 15,272 | 0.27 | Moderate |
| 4 (Calasiao) | 2,100 | 14,608 | 0.14 | Low-Moderate |
| 83 (Talisay) | 28 | 3,306 | 0.01 | Minimal |
| 57 (Biñan) | 371 | 4,166 | 0.09 | Low |
| 56 (Calamba) | 610 | 4,742 | 0.13 | Low-Moderate |
| 113A (Davao) | 197 | 3,991 | 0.05 | Low |

**Key finding:** RDO-81 (Cebu City North) has the worst merge ratio of ANY workbook in our entire sample (NCR + provincial). With 1.07 merges per row, virtually every data row involves a merged cell. This appears to be from a systematic visual formatting approach where street names, vicinities, and headers are all merged across multiple columns for display purposes.

---

## Condominium Handling in Provincial Workbooks

Provincial condo coverage is sparse compared to NCR, but notable patterns emerge:

### RDO-57 (Biñan/Cabuyao/Sta. Rosa)
Most condo-heavy provincial workbook. Specific named condos found:
- PROMENADE CONDOMINIUM
- PROMENADE MASTERPIECE CONDOMINIUM
- MERIDIAN CONDOMINIUM
- HOLLAND PARK CONDOMINIUM (with separate parking entry)
- MY CUBE CONDOMINIUM (marked `****NEWLY CREATED`)
- "ALL OTHER CONDOMINIUMS" catch-all entries

**Notes section at bottom (row 4110+):**
```
ZONAL VALUES OF CONDOMINIUM UNIT/TOWNHOUSE:
IF THE TITLE OF A PARTICULAR CONDOMINIUM UNIT/TOWNHOUSE IS -
A.) A CONDOMINIUM CERTIFICATE OF TITLE (CCT), THE ZONAL VALUE OF THE LAND AND THE
    BUILDING ARE ALREADY COMBINED IN THE UNIT PRICE.
B.) THE GROUND FLOOR OF THE RESIDENTIAL CONDOMINIUM SHALL BE CLASSIFIED AS COMMERCIAL (CC)
```

### RDO-81 (Cebu City North)
Urban barangays (Apas, Banilad, Capitol Site) have RC/CC/PS entries:
- RC: 53 entries, CC: 33 entries, PS: 54 entries
- Pattern follows NCR convention (condo name → RC/CC/PS rows)

### RDO-83 (Talisay/Carcar)
No RC/CC/PS codes found. Purely land-based classifications.

### RDO-113A (Davao)
No RC/CC/PS codes found. Davao's zonal values are entirely land-based.

**Parsing implication:** Condo data is concentrated in urban provincial areas (CALABARZON, Cebu City). Most rural/agricultural RDOs have zero condo entries. The parser must handle workbooks with no condo section at all.

---

## Data Quality Issues (Provincial)

### "A*" Classification Code (Unspecified Agricultural)

RDO-83 uses `A*` as a classification code with no ZV value:
```
50 METERS INWARD | RR | 4,700
                 | A* |
                 | A16| 1,400
```

This appears to indicate "agricultural (subtype pending assignment)" — a placeholder that was never resolved. Found only in RDO-83.

**Parsing implication:** Must handle `A*` as a valid but empty agricultural classification. Do not confuse with footnote markers.

### Footnote Convention Differences

| Convention | RDO-4/5/56/57/81 | RDO-83/NCR |
|-----------|-------------------|------------|
| `*` | Newly identified street/vicinity/classification | Deleted/removed property |
| `**` | Deleted / no longer exists | — |
| `***` | — | Newly added/identified |
| `****` | Newly created (per ocular inspection) | — |

**Critical finding:** The footnote marker convention is **reversed** between Pangasinan/Laguna and NCR/Cebu. `*` means "new" in provincial Pangasinan but "deleted" in NCR. The parser must determine the convention per workbook (or per Revenue Region) and cannot assume a universal meaning.

### Floating-Point Values

RDO-81 (Cebu City North) has fractional ZV values:
```
SITIO PANABANG   | RR | 28,387.5
SITIO MAHAYAHAY  | RR | 23,725
```

PHP 28,387.50 per sq.m. — this is NOT a floating-point artifact (unlike NCR's `118999.99999999999`). Cebu actually assigns non-integer ZVs. The parser must preserve decimal values, not blindly round to integers.

### "(NEW)" Vicinity Marker

RDO-57 uses "(NEW)" in the vicinity column:
```
LAGUNA BEL AIR |         | RR  | 17,100
               | (NEW)   | CR* | 22,200
               | INTERIOR LOT | RR | 10,800
```

This indicates a newly created classification for an existing street. It functions as both a footnote and a vicinity modifier.

---

## Zonal Value Ranges by Region

| RDO | Region | Min ZV (PHP/sqm) | Max ZV (PHP/sqm) | Spread Factor | Character |
|-----|--------|------------------|------------------|---------------|-----------|
| 5 (Alaminos) | Pangasinan | **25** | 29,900 | 1,196x | Rural agricultural + coastal |
| 4 (Calasiao) | Pangasinan | ~400 | ~40,000 | ~100x | Mixed urban/agricultural |
| 83 (Talisay) | Cebu | **75** | 150,000 | 2,000x | Semi-rural to urban |
| 113A (Davao) | Davao | **40** | 117,500 | 2,938x | Urban + extensive agricultural |
| 81 (Cebu North) | Cebu | ~170 | 95,000 | ~559x | Urban (barangay variation) |
| 56 (Calamba) | Laguna | ~900 | ~60,000 | ~67x | Transitional urban |
| 57 (Biñan) | Laguna | **900** | **255,000** | 283x | Industrializing CALABARZON |

**Comparison with NCR:** PHP 3,000 to 2,160,000 (720x spread).

**Key finding:** The lowest ZV in any workbook is **PHP 25/sqm** in Alaminos, Pangasinan — mountainous/hilly agricultural land. The highest provincial value is **PHP 255,000/sqm** in Sta. Rosa, Laguna (CALABARZON industrial corridor). The total range across all 124 RDOs is likely **PHP 10–2,160,000/sqm** — a range exceeding 200,000x that the data model must accommodate.

---

## Data Volume Analysis

### Row Counts (current revision sheets only)

| RDO | Current Sheet Rows | Est. Data Rows | Barangay Blocks | Municipalities |
|-----|-------------------|----------------|-----------------|---------------|
| 5 (Alaminos) | 15,272 | ~14,500 | ~350+ | 16 |
| 4 (Calasiao) | 14,608 | ~14,000 | ~480+ | 16 |
| 56 (Calamba) | 4,742 | ~4,400 | ~130+ | 5+ |
| 57 (Biñan) | 4,166 | ~3,800 | ~100+ | 4 |
| 113A (Davao) | 3,991 | ~3,700 | ~150+ | 1 (10 districts) |
| 83 (Talisay) | 3,306 | ~3,000 | ~70+ | 2+ |
| 81 (Cebu North) | 2,359 | ~2,100 | ~80 | 1 |

**Estimated provincial total (current revisions, 7 RDOs):** ~45,500 data rows.

**Extrapolation:** If these 7 RDOs average ~6,500 rows and there are ~100 provincial RDOs (124 total minus ~24 NCR), the full provincial dataset is approximately **650,000 data rows** for current revisions alone. Combined with NCR's ~35,000–40,000, the total across all 124 RDOs is estimated at **~690,000 current-revision rows**.

### Historical Revision Depth

| RDO | Sheet Count | Revisions | Oldest DO | Span |
|-----|------------|-----------|-----------|------|
| 56 (Calamba) | **18** | 17 | DO 47-89 (1989) | **35 years** |
| 4 (Calasiao) | 14 | 13 | DO 6-90 (1990) | 33 years |
| 5 (Alaminos) | 13 | 12 | DO 25-94 (1994) | 28 years |
| 57 (Biñan) | 11 | 10 | DO 8-91 (1991) | 33 years |
| 83 (Talisay) | 9 | 8 | DO 21-93 (1993) | 29 years |
| 81 (Cebu North) | 7 | 6 | DO 26-89 (1989) | 34 years |
| 113A (Davao) | 6 | 5 | DO 53-92 (1992) | 29 years |

RDO-56 (Calamba, Laguna) holds the record for most revisions at 17, spanning 35 years from 1989 to 2023.

---

## Key Findings for Downstream Waves

### For Wave 2 (Data Format Analysis)
1. **Multi-municipality structure is the primary parsing challenge** — provincial workbooks contain multiple municipality sections with independent header blocks, creating a nested Province → Municipality → Barangay → Street hierarchy
2. **Municipality header detection must handle 4+ casing/punctuation patterns** — even within a single workbook
3. **"Continuation" barangay blocks** break the assumption that a barangay header always starts a new barangay
4. **RDO-81's extreme merge ratio (1.07:1)** requires special handling — standard merge-aware parsing may not be sufficient
5. **ZV column header embeds revision number** — cannot match on exact text, must use keyword detection

### For Wave 3 (Resolution Logic)
1. **Two distinct vicinity resolution models** needed: NCR (cross-street boundaries) vs Provincial (road proximity hierarchy)
2. **"SITIO" sub-barangay granularity** adds a level to the address hierarchy not present in NCR
3. **Agricultural fallback hierarchy** — when no specific agricultural subtype matches, fallback to A50 (Other Agricultural)
4. **Footnote marker conventions are regionally variable** — `*` can mean "new" or "deleted" depending on Revenue Region
5. **Non-integer ZV values** are valid in Cebu — rounding logic must be conditional

### For Wave 5 (Architecture)
1. **Total dataset estimate: ~690,000 current-revision rows** across all 124 RDOs — significantly smaller than third-party claims of 1.96M/2.7M (those likely include historical revisions)
2. **File format: 5 .xls + 2 .xlsx** in this sample; extrapolating across 124 RDOs, expect ~80% .xls and ~20% .xlsx, with occasional PDFs
3. **Agricultural code support is critical** — 20-46% of provincial data uses A1-A50 codes, which are absent from NCR
4. **Province-level metadata** must be part of the data model — it's present in every provincial workbook but absent from NCR
5. **Address hierarchy is 4 levels in provincial** (Province/City/Barangay/Street) vs 3 in NCR (City/Barangay/Street)

### Emergent Aspects Discovered
- **"SITIO" sub-barangay addressing** — a location specifier unique to provincial workbooks that adds a geographic granularity level below barangay. Needs treatment in the address matching algorithm.
- **Road proximity hierarchy** — provincial ZV values are strongly correlated with road class proximity (national > provincial > barangay > interior). This is a different resolution dimension than NCR's street-specific matching.
- **Footnote convention variability** — per-region footnote meanings create a parsing ambiguity that must be resolved. May need a per-Revenue-Region configuration table.
- **Non-integer ZVs** — Cebu assigns fractional values (e.g., PHP 28,387.50/sqm), which challenges the NCR assumption that all ZVs are whole numbers.

---

## Sources

- BIR CMS API: `bir-cdn.bir.gov.ph` (structured JSON response with download URLs)
- BIR Zonal Values page: `bir.gov.ph/zonal-values`
- 7 downloaded workbooks in `input/bir-workbook-samples/extracted-provincial/`
- API metadata in `input/bir-workbook-samples/bir-cms-api-provincial-data.json`
