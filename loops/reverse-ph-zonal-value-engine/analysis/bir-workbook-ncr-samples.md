# BIR Workbook NCR Samples — Source Acquisition & Structural Survey

**Wave:** 1 — Source Acquisition
**Date:** 2026-03-02
**Aspect:** `bir-workbook-ncr-samples`

---

## Summary

24 NCR RDO zonal value workbooks were downloaded and extracted from bir.gov.ph, covering all NCR Revenue Regions (RR6-Manila, RR7A-QC, RR7B-East NCR, RR8A-Makati, RR8B-South NCR). This exceeds the original target of 3-4 NCR samples, providing comprehensive coverage of NCR format variations.

**Key finding:** Despite a normative standard (RMO 31-2019 Annex C), NCR workbooks exhibit significant structural heterogeneity — even within the same Revenue Region. A parser cannot assume fixed column positions, row offsets, or merge patterns.

---

## Inventory

### Files Downloaded (24 RDOs + 1 PDF + API metadata)

| RDO | City/District | Revenue Region | Format | File Size | Latest DO | Effectivity |
|-----|---------------|----------------|--------|-----------|-----------|-------------|
| 28 | Novaliches, QC | RR7A | .xls | 1.19 MB | DO 037-2024 | May 1, 2024 |
| 29 | Tondo-San Nicolas | RR6 | .xls | 2.47 MB | DO 027-2019 | — |
| 30 | Binondo | RR6 | .xls | 803 KB | DO 062-2017 | Nov 27, 2017 |
| 31 | Sta. Cruz, Manila | RR6 | .xls | 1.16 MB | DO 077-2018 | — |
| 32 | Quiapo-Sampaloc-San Miguel-Sta Mesa | RR6 | .xls | 2.09 MB | DO 021-2019 | Apr 24, 2019 |
| 33 | Intramuros-Ermita-Malate | RR6 | .xls | 1.33 MB | DO 075-2017 | — |
| 34 | Paco-Pandacan-Sta Ana-San Andres | RR6 | .xls | 1.70 MB | DO 078-2019 | — |
| 38 | North QC | RR7A | .xls | 1.60 MB | DO 033-2024 | Apr 11, 2024 |
| 39 | South QC | RR7A | .xls | 1.47 MB | DO 007-2024 | Feb 17, 2024 |
| 40 | Cubao, QC | RR7A | .xls | 1.41 MB | DO 035-2024 | Apr 19, 2024 |
| 41 | Mandaluyong | RR7B | .xls | 1.04 MB | DO 059-2022 | Sep 9, 2022 |
| 42 | San Juan | RR7B | .xls | 4.35 MB | DO 022-2023 | — |
| 43 | Pasig | RR7B | .xls | 1.54 MB | DO 024-2023 | — |
| 44 | Taguig-Pateros | RR8B | **.xlsx** | 592 KB | DO 005-2024 | Feb 15, 2024 |
| 45 | Marikina | RR7B | .xls | 1.55 MB | DO 006-2023 | — |
| 46 | Cainta-Taytay | RR7B | .xls | 1.50 MB | DO 022-2020 | — |
| 47 | East Makati | RR8A | .xls | 569 KB | DO 037-2021 | Dec 22, 2021 |
| 48 | West Makati | RR8A | .xls | 578 KB | DO 036-2021 | Dec 22, 2021 |
| 49 | North Makati | RR8A | .xls | 895 KB | DO 035-2021 | Jan 8, 2022 |
| 50 | South Makati | RR8A | .xls | 1.12 MB | DO 038-2021 | Dec 22, 2021 |
| 51 | Pasay | RR8B | .xls | 2.03 MB | DO 043-2023 | Sep 2, 2023 |
| 52 | Parañaque | RR8B | .xls | 1.07 MB | DO 049-2023 | Sep 30, 2023 |
| 53A | Las Piñas | RR8B | .xls | 658 KB | DO 004-2021 | — |
| 53B | Muntinlupa | RR8B | .xls | 610 KB | DO 089-2023 | — |
| 57 | Biñan City | (provincial) | **.pdf** | 1.80 MB | — | — |

**Also saved:** `bir-cms-api-ncr-data.json` — BIR CMS API response mapping Revenue Regions to RDOs with CDN download URLs.

### File Format Distribution
- **23 files:** .xls (BIFF8 / legacy Excel) — read with `xlrd`
- **1 file:** .xlsx (OpenXML) — RDO 44 Taguig-Pateros — read with `openpyxl`
- **1 file:** .pdf (image-based) — RDO 57 Biñan City — requires OCR

---

## Structural Analysis: Universal Patterns

### Workbook Anatomy (consistent across all 24)

Every workbook follows this pattern:

1. **Sheet 0 = NOTICE** — Navigation index listing all Department Orders, revision numbers, effectivity date ranges, and which sheet contains each revision
2. **Sheets 1..N** — One sheet per Department Order, newest first (highest sheet number = current revision)
3. **Sheet count:** 7–12 sheets per workbook (7–10 revisions spanning 1987–2024)

### Data Sheet Internal Structure

Each data sheet follows this layout (row ranges vary):

| Section | Typical Rows | Content |
|---------|-------------|---------|
| DO Preamble | 0–35 | Legal text, signatories, authority citation |
| Definition of Terms | 35–60 | Classification code definitions |
| Classification Legend | 60–75 | RR, CR, RC, CC, PS, I, X, GL, GP, CL, APD, DA |
| Agricultural Codes | 75–100 | A01–A50 subtype table |
| Data Section Marker | ~100–105 | "BUREAU OF INTERNAL REVENUE" / Revenue Region |
| Barangay Blocks | 105+ | Repeating per-barangay data sections |

### Barangay Block Pattern (repeating)

```
[Metadata]
  Province: NCR
  City/Municipality: [NAME]    D.O. NO.    [number]
  Barangay: [NAME]             Effectivity Date    [date]
[Column Headers]
  STREET/SUBDIVISION | VICINITY | CLASSIFICATION | ZV/SQ.M.
[Data Rows]
  Land entries (RR, CR, I, X, GL, GP classifications)
  Subdivision entries
  [Condo sub-section] — RC, CC, PS classifications
  "ALL OTHER STREETS" catch-all row
  "ALL OTHER CONDOMINIUMS" catch-all row
[NOTES]
  Footnotes, boundary descriptions, asterisk legends
```

### Multi-Row Entry Pattern (universal)

A single street/condo commonly spans multiple rows:
```
SHAW BLVD    | EDSA-WACK WACK CREEK | RR | 68,000
             |                      | CR | 83,000
```
When column 0 (street name) is empty, the row is a continuation with a different classification code. The parser must carry forward the street name.

### Classification Codes (universal across all workbooks)

| Code | Classification | Usage |
|------|---------------|-------|
| RR | Residential Regular | Land principally for habitation |
| CR | Commercial Regular | Land principally for commercial use |
| RC | Residential Condominium | Condo units for residential use |
| CC | Commercial Condominium | Condo units for commercial use |
| PS | Parking Slot | Typically 60–70% of unit ZV |
| I | Industrial | Land for industrial use |
| X | Institutional | Schools, churches, hospitals |
| GL | Government Land | Government-owned property |
| GP | General Purpose | Raw/undeveloped land (min 5,000 sqm) |
| CL | Cemetery Lot | Cemetery/memorial park lots |
| APD | Area for Priority Development | Designated priority zones |
| DA | Drying Area | Agricultural drying areas |
| A1–A50 | Agricultural subtypes | 50 categories (riceland, coconut, fishpond, etc.) |

---

## Structural Analysis: Format Variations

### Critical Finding: Column Layout Heterogeneity

Even within the same Revenue Region, column layouts differ. Four distinct patterns identified:

#### Pattern A: Standard 4-Column (most common)
```
Col 0: STREET/SUBDIVISION
Col 1: VICINITY
Col 2: CLASSIFICATION
Col 3: ZV/SQ.M.
```
**Used by:** RDO 28 (Novaliches), RDO 40 (Cubao), RDO 41 (Mandaluyong), RDO 47–50 (Makati), RDO 51 (Pasay), RDO 52 (Parañaque)

#### Pattern B: 5-Column with Split Vicinity
```
Col 0: STREET/SUBDIVISION
Col 1: VICINITY (first cross-street)
Col 2: (second cross-street)
Col 3: CLASSIFICATION
Col 4: ZV/SQ.M.
```
**Used by:** RDO 38 (North QC) — 1,193 of ~2,691 data rows use the third vicinity column

#### Pattern C: 5-Column with Offset Gap
```
Col 0: STREET/SUBDIVISION
Col 1: (empty in data rows, only used in NOTES)
Col 2: VICINITY
Col 3: CLASSIFICATION
Col 4: ZV/SQ.M.
```
**Used by:** RDO 39 (South QC) — column 1 is effectively unused in data rows

#### Pattern D: 10-Column Side-by-Side Comparison
```
Cols 0–3: STREET/SUBDIVISION (merged across 4 cols)
Cols 4–5: VICINITY (merged across 2 cols)
Col 6: CLASSIFICATION
Col 7: Previous revision ZV/SQ.M.
Col 8: Current revision ZV/SQ.M.
Col 9: (empty)
```
**Used by:** RDO 30 (Binondo, current revision), RDO 52 8th revision

**Parsing implication:** A robust parser must detect the column layout dynamically by scanning for header keywords ("STREET", "VICINITY", "CLASS", "ZV") rather than assuming fixed positions.

### Phantom Columns

Several workbooks report far more columns than actually contain data:

| Workbook | Reported Cols | Actual Data Cols | Cause |
|----------|--------------|-----------------|-------|
| RDO 32 (DO 21-19) | 19 | 4 | Formatting artifacts |
| RDO 51 (DO 38-09) | 252 | 4 | Stray data/formatting |
| RDO 47 (DO 23-12) | 254 | 4 | Stray data/formatting |
| RDO 44 Sheet 8 | 16,384 (XFD) | 4 | OpenXML formatting artifacts |

**Parsing implication:** Never trust `sheet.ncols` / `sheet.max_column`. Detect actual data occupancy by scanning header rows.

### Barangay Header Variations

Six distinct patterns observed:

| Pattern | Format | Used By |
|---------|--------|---------|
| 1 | `BARANGAY: [name]` in separate cells | RDO 47, 49, 50 (Makati) |
| 2 | `BARANGAY` / `:  [name]` (colon in col 1) | RDO 48 (West Makati) |
| 3 | `BARANGAY : [name]` inline in single cell | RDO 38 (North QC) |
| 4 | `Zone/Barangay` / `:  [name]` | RDO 39 (South QC), RDO 41 (Mandaluyong), RDO 52 (Parañaque) |
| 5 | `Barangay : Barangay [NNN]  Zone [NN]` | RDO 30 (Binondo, numbered) |
| 6 | `BARANGAY` / `[name]` (no colon) | RDO 28 (Novaliches), RDO 40 (Cubao) |

**Parsing implication:** Must match on "BARANGAY" or "Zone/Barangay" keyword in col 0, then extract the name from either the same cell or col 1, stripping colons and whitespace.

### Effectivity Date Format Variations

| Format | Example | Used By |
|--------|---------|---------|
| Excel serial date (float) | `44826` → Sep 9, 2022 | RDO 28, 38, 41 (.xls files) |
| Python datetime object | `datetime(2024, 2, 15)` | RDO 44 (.xlsx file) |
| Text string (M/D/YYYY) | `2/17/2024` | RDO 39 |
| Text string (Month D, YYYY) | `April 19, 2024` | RDO 40 |
| Text string (Abbrev) | `Sept. 30, 2023` | RDO 52 |

**Parsing implication:** Must handle all date formats: serial-to-date conversion for .xls, native datetime for .xlsx, and multiple text date formats.

### Sheet Name Inconsistencies

| Issue | Example | RDO |
|-------|---------|-----|
| Missing closing parenthesis | `Sheet 9 (DO 059-2022` | RDO 41 (truncated by .xls 31-char limit) |
| Leading space | ` Sheet 7 (100-2014)` | RDO 41 |
| Missing "DO" prefix | `Sheet 7 (100-2014)` | RDO 41 |
| Inconsistent spacing | `Sheet 8 (DO 40-19)` vs `Sheet 9 (DO 005-24)` | RDO 44 |

---

## Merged Cell Analysis

### Severity by Era

| Era | Typical Merged Ranges | Parse Difficulty |
|-----|----------------------|-----------------|
| 1987–1997 (Sheets 1–4) | 8–13 | Trivial |
| 1998–2014 (Sheets 5–6) | 50–200 | Low |
| 2015–2019 (Sheets 7–8) | 200–500 | Moderate |
| 2020–2024 (Sheets 8–10) | 185–3,929 | Moderate to Extreme |

### Most Merge-Heavy Workbooks (current revision)

| RDO | Merged Ranges | Context |
|-----|--------------|---------|
| RDO 32 (Quiapo-Sampaloc) | 3,929 | Multi-district, 5,866 rows |
| RDO 51 (Pasay, 5th rev) | 3,836 | Dense urban |
| RDO 51 (Pasay, 6th rev) | 3,314 | Dense urban |
| RDO 44 (Taguig) | 1,063 | Largest barangay count |
| RDO 48 (West Makati) | 438 | Data rows use vertical merges |
| RDO 30 (Binondo) | 402 | 10-column comparison layout |
| RDO 39 (South QC) | 353 | — |
| RDO 40 (Cubao) | 347 | — |
| RDO 28 (Novaliches) | 287 | — |
| RDO 49 (North Makati) | 219 | — |
| RDO 38 (North QC) | 199 | — |
| RDO 52 (Parañaque) | 185 | Cleanest modern layout |
| RDO 41 (Mandaluyong) | 175 | — |

**Key insight:** Merge complexity correlates with both recency and data volume. RDO 32 (Quiapo-Sampaloc, 4 Manila districts, ~5,800 rows) is the hardest to parse.

### Merge Usage Patterns

1. **Full-width title merges** — DO preamble text spans all columns (universal)
2. **Barangay section headers** — Province/City/Barangay metadata merged across row (universal)
3. **Vertical merges in data rows** — street name spanning 2+ rows where multiple classifications exist (RDO 48 heavily; others less)
4. **Condo name merges** — condo building names merged across columns in comparison layouts (RDO 30)

---

## Condominium Section Patterns

### Condo Section Labeling Variations

| Label | Used By |
|-------|---------|
| `CONDOMINIUMS AND TOWNHOUSES` | RDO 48, 49 (Makati) |
| `CONDOMINIUMS/TOWNHOUSES:` | RDO 41 (Mandaluyong) |
| `CONDOMINIUMS:****` | RDO 44 (Taguig) |
| `CONDOMINIUMS:` | RDO 52 (Parañaque) |
| `(List of Condominiums / Townhouses)` | RDO 30 (Binondo) |
| `CONDOMINIUM/S:` | RDO 32 (Quiapo) |
| `CONDOMINIUMS/TOWNHOUSES (CCT)` | RDO 51 (Pasay) |
| `LIST OF CONDOMINIUMS` | RDO 50 (South Makati) |
| Inline (no separate header) | RDO 47 (East Makati) |

### Condo Data Structure

Each condo entry typically occupies 2–3 rows:
```
AMORSOLO CONDOMINIUM    | AMORSOLO ST.  | RC | 85,000
                        |               | CC | 105,000
                        |               | PS | 73,000
```

### Condo-Specific Rules (embedded in workbooks)

1. **RC → CC upgrade:** "Any unit in a purely residential condominium (RC) project found to be used in business shall be classified CC and 20% of the established value shall be added thereto."
2. **New condo assignment:** "Developer/Owner of condominium project built after the effectivity of this revision shall request for an assignment of values from the TCRPV."
3. **PS value rule:** Parking Slot (PS) value is typically 70% of the condo unit's ZV (stated in RDO 44 notes; ~60% observed in Makati data).

### Special: BGC FAR-Based Pricing (RDO 44)

Bonifacio Global City uses a unique Floor Area Ratio (FAR)-based zonal value system:
```
BONIFACIO GLOBAL CITY (BGC)*    | ALL LOTS WITHIN GLOBAL CITY
  FAR 1  | CR | 205,000
  FAR 2  | CR | 295,000
  FAR 3  | CR | 390,000
  ...
  FAR 18 | CR | 2,160,000
```
FAR values range from 1–18, with both CR and X (Institutional) classifications. The highest value in the entire NCR dataset is **PHP 2,160,000/sq.m.** at FAR 18 in BGC.

**Parsing implication:** The VICINITY column contains "FAR N" instead of street boundaries — requires special handling.

---

## Data Volume Analysis

### Row Counts (current revision sheets only)

| RDO | Current Sheet Rows | Data Rows (est.) | Barangays |
|-----|-------------------|------------------|-----------|
| 44 (Taguig-Pateros) | 6,218 | ~5,800 | ~38 |
| 32 (Quiapo-Sampaloc) | 5,866 | ~5,500 | ~300+ (numbered) |
| 51 (Pasay) | 4,987 | ~4,600 | ~67 (numbered zones) |
| 50 (South Makati) | 3,385 | ~3,100 | 16 |
| 28 (Novaliches) | ~2,800 | ~2,500 | ~22 |
| 38 (North QC) | ~2,700 | ~2,400 | ~35 |
| 39 (South QC) | ~2,600 | ~2,300 | ~33 |
| 40 (Cubao) | ~2,600 | ~2,300 | ~37 |
| 52 (Parañaque) | 2,168 | ~1,900 | 16 |
| 41 (Mandaluyong) | 1,689 | ~1,500 | 27 |
| 49 (North Makati) | 1,633 | ~1,400 | 13 |
| 48 (West Makati) | 878 | ~700 | 5 |
| 47 (East Makati) | 608 | ~480 | 1 |
| 30 (Binondo) | 526 | ~400 | ~10 (numbered) |

**Estimated NCR total (current revisions only):** ~35,000–40,000 data rows across 24 RDOs.

### Historical Revision Depth

| RDO | Revision Count | Oldest DO | Newest DO | Span |
|-----|---------------|-----------|-----------|------|
| 52 (Parañaque) | 10 | DO 85-87 (1987) | DO 049-2023 | 36 years |
| 48 (West Makati) | 9 | DO 51-87 (1987) | DO 036-2021 | 34 years |
| 50 (South Makati) | 9 | DO 51-87 (1987) | DO 038-2021 | 34 years |
| 41 (Mandaluyong) | 9 | DO 90-88 (1988) | DO 059-2022 | 34 years |
| Most others | 7–8 | DO 113/138-87/88 | 2019–2024 | 35–37 years |
| 30 (Binondo) | 6 | DO 113-88 (1989) | DO 062-2017 | 28 years |

**All QC RDOs** share the same initial 3 DOs (DO 138-87, DO 43/44-90, DO 28/29-93) and diverge from the 3rd revision onward. **All Makati RDOs** share the same initial DO (DO 51-87).

---

## Data Quality Issues

### Floating-Point Artifacts
- RDO 50 (South Makati): `118999.99999999999` instead of `119000`
- RDO 41 (Mandaluyong): `62999.99999999999` instead of `63000`
- **Fix:** Round all ZV values to nearest integer (all legitimate ZVs are whole numbers)

### Zero Values
- RDO 47 (East Makati), row 114: `AYALA AVENUE*` with ZV = `0` — indicates a newly identified street awaiting TCRPV assignment

### Jurisdiction Annotations
- RDO 41: `HARVARD*` and `REYES*` have ZV = `0.0` with footnotes "not within the barangay's jurisdiction"

### Multiple DOs in Single Sheet
- RDO 44 (Taguig): Sheet 9 contains barangays from **two different DOs** — DO 005-2024 (original Taguig barangays) and DO 038-2021 (formerly-South-Makati barangays transferred per RAO 1-2024). Different effectivity dates within the same sheet.

### "Under Construction" Category
- RDO 51 (Pasay): Has a dedicated `CONDOMINIUMS (CCT) UNDER CONSTRUCTION` section — condos with assigned ZVs but not yet completed.

### Footnote Markers
- `*` — Deleted/removed property
- `***` — Newly added/identified property or classification
- `*****` — Renamed property (e.g., "Landco Condo is renamed / the same as Alexcy One Building")
- `NOTE:` — Boundary descriptions, special rules
- Must be stripped from property names during parsing but preserved as metadata.

---

## Legal Authority Evolution

| Era | Authority Cited |
|-----|----------------|
| 1987–1997 | Section 16(e) of the Tax Code, as amended by PD 1994 |
| 1997–2018 | Section 6(E) of RA 8424 ("Tax Reform Act of 1997") |
| 2018–present | Section 4 of RA 10963 ("TRAIN Law"), amending Section 6(E) of NIRC 1997 |

**Signatory evolution (DOF Secretary):**
- Pre-2022: Various (Dominguez, Purisima, etc.)
- 2022–early 2024: Benjamin E. Diokno
- Mid-2024: Ralph G. Recto (RDOs 28, 38, 40)

---

## Zonal Value Ranges (Current Revisions)

| RDO | Min ZV (PHP/sqm) | Max ZV (PHP/sqm) | Notes |
|-----|------------------|------------------|-------|
| 28 (Novaliches) | 3,000 | 218,000 | Lowest floor — suburban/peripheral |
| 38 (North QC) | 26,000 | 350,000 | — |
| 39 (South QC) | 29,000 | 350,000 | — |
| 40 (Cubao) | 30,000 | 350,000 | — |
| 44 (Taguig) | 19,000 | **2,160,000** | BGC FAR 18 — highest in NCR |
| 47 (East Makati) | — | 750,000 | Ayala Center CR |
| 48 (West Makati) | 83,000 | — | — |
| 49 (North Makati) | — | — | Poblacion area |
| 51 (Pasay) | — | 203,000 | Roxas Blvd condos |
| 52 (Parañaque) | — | 203,000 | — |

**Overall NCR range:** PHP 3,000/sqm (Novaliches agricultural/peripheral) to PHP 2,160,000/sqm (BGC FAR 18).

---

## Key Findings for Downstream Waves

### For Wave 2 (Data Format Analysis)
1. **Column detection must be dynamic** — at least 4 distinct column layout patterns exist
2. **Merged cell handling is critical** — up to 3,929 merged ranges per sheet
3. **Phantom columns are common** — reported column counts are unreliable
4. **Effectivity dates use 5+ different formats**
5. **BGC's FAR-based pricing is structurally unique** and must be special-cased

### For Wave 3 (Resolution Logic)
1. **"ALL OTHER STREETS" / "ALL OTHER CONDOMINIUMS" catch-all entries** are present in every barangay — confirms the barangay-level fallback mechanism
2. **Multi-classification per street** is universal — parser must maintain street context across continuation rows
3. **RC → CC upgrade rule** (20% markup for business use in residential condo) is embedded in workbook notes
4. **Zero-value entries** indicate pending TCRPV assignments, not actual zero values
5. **Multiple DOs per sheet** (RDO 44) means effectivity date tracking must be per-barangay, not per-sheet

### For Wave 5 (Architecture)
1. **Estimated NCR dataset:** ~35,000–40,000 data rows (current revisions only)
2. **File format mix:** 23 .xls + 1 .xlsx + 1 PDF — parser needs both xlrd and openpyxl
3. **Historical data depth:** 7–10 revisions per RDO, spanning 34–37 years
4. **BIR CDN API** (`bir-cms-api-ncr-data.json`) provides structured download URLs organized by Revenue Region

### Emergent Aspects Discovered
- **Revenue Region reorganization** — historical RDO boundaries have shifted (RR8 split into RR8A/RR8B; Parañaque/Las Piñas/Muntinlupa were once a single RDO; South Makati barangays transferred to Taguig per RAO 1-2024). This affects jurisdiction mapping.
- **BGC FAR-based pricing** — a unique pattern not covered in the prior analysis. Needs its own treatment in resolution logic.
- **"Under construction" condo entries** — condos with assigned ZVs but not yet completed. Need to decide how to surface these.

---

## Sources

- BIR CMS API: `bir-cdn.bir.gov.ph` (structured JSON response with download URLs)
- BIR Zonal Values page: `bir.gov.ph/zonal-values`
- 24 downloaded workbooks in `input/bir-workbook-samples/extracted/`
- API metadata in `input/bir-workbook-samples/bir-cms-api-ncr-data.json`
