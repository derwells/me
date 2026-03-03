# Sheet Organization — Data Format Analysis

**Wave:** 2 — Data Format Analysis
**Date:** 2026-03-03
**Aspect:** `sheet-organization`

---

## Summary

All 31 sampled BIR zonal value workbooks (24 NCR + 7 provincial) were analyzed for sheet-level organization: naming conventions, sheet types, revision history structure, and content separation patterns. The most critical finding is that **every workbook follows the same organizational pattern**: a NOTICE sheet followed by numbered revision sheets in descending chronological order — but with pervasive naming inconsistencies that a parser must tolerate.

**Key findings:**
1. **294 total sheets** across 31 workbooks: 31 NOTICE sheets, 261 revision (data) sheets, 2 empty artifacts
2. **Universal pattern**: NOTICE sheet at index 0, followed by `Sheet N (DO NNN-YY)` in descending order (newest first)
3. **No condo/land separation** — condos, land, and agricultural data all coexist within each revision sheet (no workbook uses separate condo sheets)
4. **No hidden sheets** in any workbook — all data is visible
5. **Shared DO numbers** across RDOs: 30 Department Orders cover multiple RDOs, sharing the same DO# in different workbooks
6. **Extensive naming inconsistencies**: 25 anomalies including unclosed parentheses, missing DO prefix, leading/trailing whitespace, and one duplicate DO number within the same workbook
7. **Provincial NOTICE sheets** include a "City/Municipalities Covered" column that maps which revision covers which municipalities — a critical metadata source
8. **5–17 revision sheets per workbook** (avg 8.4), spanning 1987–2024 — full revision history is preserved

---

## Sheet Type Taxonomy

### Type 1: NOTICE Sheet (31/31 workbooks — 100%)

Every workbook has exactly one NOTICE sheet at index 0. It contains:

1. **RDO identification**: Revenue Region, RDO number, jurisdiction name
2. **Barangay/municipality listing**: Complete enumeration of covered areas
3. **Revision history table**: Maps each Department Order to its sheet, effectivity dates, and (in provincial workbooks) covered municipalities

**NOTICE sheet structure:**
```
Row 0:   "NOTICE" or "N O T I C E" (letter-spaced variant)
Row 1:   "RR [N] - [REGION NAME]"
Row 2-5: RDO jurisdiction description + barangay/municipality listing
Row 6+:  Revision table header + data rows

Revision table columns:
  | DO NO. | Revision | Effectivity Dates (From | To) | [City/Municipalities Covered] | See Details on |
```

**Two NOTICE table formats:**

| Format | Count | Description |
|--------|-------|-------------|
| With municipality column | 25/31 (81%) | Includes "City/Municipalities Covered" column — found in both NCR and provincial |
| Standard (no municipality) | 6/31 (19%) | Only Manila RR6 district RDOs (29, 30, 31, 32, 33, 34) |

**Parser value**: The NOTICE sheet is the **authoritative source** for:
- Which sheet contains the current revision (highest Sheet N)
- Effectivity date ranges per revision (From/To)
- DO number per revision
- Municipality coverage per revision (provincial workbooks)

**Effectivity date format variation:**

| Format | Occurrences | Example |
|--------|-------------|---------|
| Excel serial number | 78 | `43066.0` |
| ISO datetime | 8 | `2023-10-06 00:00:00` |
| Human date | 5 | `16-Feb-23` |

The parser must handle all three date representations. Excel serial dates dominate (86%).

### Type 2: Revision Data Sheet (261 total across 31 workbooks)

Numbered sheets containing the actual zonal value data for one Department Order revision. All land, condo, and agricultural classifications coexist in a single sheet — no workbook separates them.

**Naming convention:**
```
Sheet N (DO NNN-YY)
```
Where N = sequential revision number, NNN = Department Order number, YY = year (2 or 4 digit).

### Type 3: Empty/Artifact Sheets (2 total)

| Workbook | Sheet Name | Description |
|----------|------------|-------------|
| RDO-30 | `Sheet1` | 0 rows × 0 cols — empty placeholder |
| RDO-4 | `Recovered_Sheet1` | 0 rows × 0 cols — file recovery artifact |
| RDO-5 | `Recovered_Sheet1` | 0 rows × 0 cols — file recovery artifact |

Parser should skip sheets with 0 rows.

---

## Sheet Naming Inconsistencies

The dominant naming pattern `Sheet N (DO NNN-YY)` covers 93% (242/261) of revision sheets, but 25 naming anomalies were found across 14 workbooks:

### Anomaly Types

| Type | Count | Examples |
|------|-------|---------|
| Trailing whitespace | 8 | `'Sheet 4 (DO 57-96) '` (RDO-34) |
| Leading whitespace | 4 | `' Sheet 1 (DO 138-87)'` (RDO-28) |
| Unclosed parenthesis | 7 | `'Sheet 2 (DO 1-91'` (RDO-34), `'Sheet 9 (DO 059-2022'` (RDO-41) |
| Missing DO prefix | 4 | `'Sheet 1 (138-87)'` (RDO-38), `'Sheet 8(060-22)'` (RDO-83) |
| Double space | 1 | `'Sheet  5 (DO 127-91)'` (RDO-56) |
| Duplicate DO in same workbook | 1 | RDO-57 has both `Sheet 7 (DO 11-15)` and `Sheet 6 (DO 11-15)` — likely covers different municipalities |

### Parser implications

The sheet name parser must:
1. **Trim whitespace** before processing
2. **Use regex extraction** rather than exact string matching
3. **Handle missing `DO` prefix** — extract digits-dash-digits pattern regardless
4. **Handle missing closing parenthesis**
5. **Handle the RDO-57 duplicate** — two sheets can share the same DO number (different municipalities within same RDO)

**Recommended regex for sheet name parsing:**
```
Sheet\s*(\d+)\s*\(?(?:DO\s*[-#]?\s*)?(\d+)\s*[-]\s*(\d{2,4})\)?
```
- Group 1: Sheet number (revision sequence)
- Group 2: Department Order number
- Group 3: Year (2 or 4 digit)

---

## Revision History Depth

### Distribution

| Revision Count | Workbooks | Examples |
|----------------|-----------|---------|
| 5 | 1 | RDO-113A (Davao) |
| 6 | 6 | RDO-30, 31, 32, 33, 34, 81 |
| 7 | 4 | RDO-29, 46, 49, 51 |
| 8 | 7 | RDO-28, 38, 39, 40, 42, 47, 83 |
| 9 | 6 | RDO-39, 41, 43, 44, 48, 53A |
| 10 | 3 | RDO-50, 52, 53B, 57 |
| 11 | 2 | RDO-5, 45 |
| 12 | 1 | RDO-4 (Pangasinan) |
| 17 | 1 | RDO-56 (Laguna — 17 revisions!) |

**Aggregate:**
- Year range: **1987–2024** (37 years of revision history preserved)
- Revision counts: min=5, max=17, avg=8.4
- Total data sheets: **261** across 31 workbooks

### Maximum depth: RDO-56 (Calamba, Laguna) — 17 revisions

RDO-56 has the most revision sheets of any sampled workbook, with Department Orders spanning 1989 to 2023. This implies some provincial RDOs revise individual municipalities' schedules independently, creating many more sheets than NCR workbooks where the entire RDO is revised together.

---

## Shared Department Orders Across RDOs

A critical finding: **30 Department Orders** are shared across multiple RDOs. This means a single DO can appear in 2–4 different workbooks, each containing only the data relevant to that RDO's jurisdiction.

**Largest shared DO clusters:**

| Department Order | RDOs | Pattern |
|------------------|------|---------|
| DO 51-87 | 47, 48, 49, 50 | All 4 Makati RDOs share earliest revision |
| DO 19-90 | 47, 48, 49, 50 | All 4 Makati RDOs |
| DO 135-91 | 47, 48, 49, 50 | All 4 Makati RDOs |
| DO 85-87 | 52, 53A, 53B | South NCR cluster (Parañaque/Las Piñas/Muntinlupa) |
| DO 53-90 | 52, 53A, 53B | Same cluster |
| DO 22-93 | 52, 53A, 53B | Same cluster |
| DO 1-89 | 52, 53A, 53B | Same cluster |
| DO 138-87 | 28, 39, 40 | QC cluster |
| DO 86-87 | 43, 44 | Pasig/Taguig cluster |
| DO 90-88 | 41, 42 | Mandaluyong/San Juan cluster |

**Interpretation**: Historically, these RDO clusters were a single district that was later split. The shared early DOs reflect the pre-split era. Splitting typically happened in the 1990s–2000s (via RAOs), after which each new RDO gets its own DO numbers.

**Parser implication**: DO number alone is NOT a unique key for a zonal value schedule. The unique key is **(RDO, DO number)** — or more precisely, the sheet within a specific workbook.

---

## Data Growth Across Revisions

The number of data rows per revision sheet generally grows over time as properties are subdivided and new developments are built.

**Extreme growth cases:**

| RDO | First Revision | Latest Revision | Growth |
|-----|----------------|-----------------|--------|
| RDO-4 (Pangasinan) | 795 rows (1990) | 14,609 rows (2023) | **25.7x** |
| RDO-5 (Pangasinan) | 1,226 rows (1994) | 15,272 rows (2022) | **12.5x** |
| RDO-57 (Laguna) | 417 rows (1991) | 4,166 rows (2024) | **10.0x** |
| RDO-44 (Taguig) | 681 rows (1987) | 6,218 rows (2024) | **9.1x** |
| RDO-46 (Cainta-Taytay) | 727 rows (1991) | 5,015 rows (2020) | **6.9x** |

**Shrinkage (anomaly)**: RDO-33 (Intramuros-Ermita-Malate) shrank from 3,771 rows (1989) to 2,322 rows (2017) — 0.6x — likely due to data consolidation or barangay restructuring in this historic district.

**Growth driver**: Provincial RDOs (Pangasinan, Laguna) show the most dramatic growth because they cover multiple municipalities, and each municipality gets progressively finer-grained zonal classifications over time.

---

## Column Count Variation Across Revisions

**Every workbook** (31/31) shows column count variation across its revision sheets. Column counts range from 4 to 34 within a single workbook. The extreme cases (254–16384 columns) are xlrd/openpyxl artifacts from stray cell formatting, not actual data columns.

**Implication**: The parser cannot assume a fixed column layout for the entire workbook. Each revision sheet must be parsed independently with its own column detection pass. This reinforces the finding from `workbook-column-layouts` that headers repeat per barangay block and must be dynamically detected.

---

## Content Mixing: No Condo/Land/Agri Separation

Content type analysis of all 31 current-revision sheets confirms that **all workbooks mix land, condo, and agricultural data in a single sheet**:

- **31/31** workbooks have land classification data (RR, CR, RC, CC, I) in the current revision sheet
- **31/31** workbooks have condo/townhouse entries in the same sheet
- **29/31** workbooks have agricultural code entries (A1–A50) in the same sheet (the 2 NCR Manila RDOs without agri data are expected — purely urban areas)

No workbook uses separate sheets for condos vs. land vs. agriculture. The separation is purely structural within the sheet: condos appear in a "CONDOMINIUM AND TOWNHOUSES" section, typically at the end of each barangay block or at the end of the sheet.

---

## Provincial Multi-Municipality Organization

Provincial workbooks (RDOs covering multiple cities/municipalities) have a distinctive organization pattern compared to NCR:

### Provincial pattern
Each revision sheet covers one or more municipalities within the RDO's jurisdiction. The NOTICE sheet maps which revision covers which municipalities:

**Example — RDO-56 (Calamba, Laguna):**
```
DO 059-2023 (6th revision) → Calamba City → Sheet 17
DO 56-17 (5th revision)    → [multiple municipalities] → Sheet 16
...
```

**Example — RDO-57 (Biñan, Laguna):**
- DO 055-2024: Biñan, Cabuyao, San Pedro, Sta. Rosa City → Sheet 10
- DO 88-19: San Pedro → Sheet 9 (separate revision for one municipality)
- DO 32-19: Biñan, Cabuyao, Sta. Rosa City → Sheet 8

This creates a **non-uniform revision timeline**: different municipalities within the same RDO can be on different DO revisions. This is why RDO-56 has 17 revision sheets — many are municipality-specific updates.

### NCR pattern
NCR RDOs typically cover a single city or district. Revisions cover the entire jurisdiction at once. No per-municipality column needed in the NOTICE table.

### Parser implication for provincial workbooks
1. **The NOTICE sheet is essential** — it's the only way to determine which sheet to use for which municipality
2. **Multiple current-revision sheets may exist** — e.g., municipality A's latest is Sheet 17 while municipality B's latest is Sheet 15
3. **Parser must build a municipality → sheet mapping** from the NOTICE table before reading data
4. **The "current revision" for an RDO is municipality-dependent**, not a single sheet

---

## Parser Design Recommendations

### Sheet Discovery Algorithm

```
1. Open workbook
2. Read NOTICE sheet (always index 0)
3. Parse revision table from NOTICE:
   - Extract DO number, revision number, effectivity dates, sheet reference
   - For provincial: also extract municipality coverage
4. Build sheet map: municipality → [(sheet_name, do_number, from_date, to_date)]
5. For each data sheet:
   a. Skip if rows == 0 (empty/artifact)
   b. Parse sheet name: extract sheet_num, do_number, do_year
   c. Run column detection (per-barangay-block, as per workbook-column-layouts findings)
   d. Parse data rows
```

### Current Revision Identification

**For NCR (single-city) RDOs:**
- Current revision = Sheet with highest number (index 1, right after NOTICE)
- Verify against NOTICE table: effectivity `To` should be "Present"

**For provincial (multi-city) RDOs:**
- Current revision varies by municipality
- Must read NOTICE table to find the latest sheet for each municipality
- A query for "Calamba City" in RDO-56 should use Sheet 17, but a query for "Bay" might need a different sheet

### Sheet Filtering

A robust parser should:
1. **Always skip**: NOTICE, empty sheets (0 rows), Recovered_Sheet* artifacts
2. **Parse all revision sheets** if historical data is needed, or
3. **Parse only current revision sheet(s)** for current-value-only mode

### Data Model for Sheet Metadata

```rust
struct SheetMeta {
    sheet_index: usize,
    sheet_name: String,
    sheet_number: u32,        // The N in "Sheet N"
    do_number: String,        // e.g., "059-23"
    do_year: u16,             // Normalized to 4-digit year
    revision_ordinal: u8,     // 1st, 2nd, ..., 17th
    effectivity_from: Option<NaiveDate>,
    effectivity_to: Option<NaiveDate>,  // None = "Present"
    municipalities: Vec<String>,         // Empty for NCR single-city RDOs
    row_count: usize,
    col_count: usize,
}

struct WorkbookMeta {
    rdo_number: String,       // e.g., "56"
    revenue_region: String,   // e.g., "RR 9B"
    jurisdiction_name: String, // e.g., "Calamba City, Central Laguna"
    barangays: Vec<String>,
    sheets: Vec<SheetMeta>,
}
```

---

## Anomalies and Edge Cases

### 1. RDO-57 Duplicate DO Number
RDO-57 has two sheets with the same DO number: `Sheet 7 (DO 11-15)` and `Sheet 6 (DO 11-15)`. This likely covers different municipalities under the same Department Order. The NOTICE table should disambiguate.

### 2. Wide Column Artifacts
12 sheets across 8 workbooks show column counts of 107–16,384 — these are xlrd/openpyxl artifacts from stray cell formatting or protection settings, not actual data columns. The actual data occupies 4–10 columns. Parser should detect actual data column range rather than trusting `max_column`.

### 3. N O T I C E (Letter-Spaced Title)
14 of 31 workbooks (45%) use `N O T I C E` (letter-spaced) instead of `NOTICE`. Parser should match on `NOTICE` after removing spaces.

### 4. RDO Splitting History
The shared DO numbers across RDOs reveal the RDO splitting timeline:
- **Makati**: Originally one RDO, split into 4 (47, 48, 49, 50) — shared DOs from 1987–1991
- **South NCR**: RDO 53 split into 53A (Las Piñas) and 53B (Muntinlupa) in 2008 per RAO 2-2008
- **QC**: Multiple splits creating RDOs 28, 38, 39, 40
- **Davao**: RDO 113 split into 113A and 113B per RAO 12-2009
- **Pasig**: RDOs 43A and 43B merged back into RDO 43 per RAO 2-2016

This means the workbook's barangay listings in the NOTICE sheet reflect the **current** RDO boundaries, not the historical ones. Early revision sheets may contain data for barangays now in a different RDO.

### 5. RDO-34 Misidentified Revenue Region
RDO-34 NOTICE says "RR 5 - MANILA" but other Manila district RDOs say "RR 6 - MANILA". This is a data entry error — RDO-34 is part of RR 6.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total workbooks analyzed | 31 |
| Total sheets | 294 |
| NOTICE sheets | 31 (100% of workbooks) |
| Revision data sheets | 261 |
| Empty/artifact sheets | 3 |
| Hidden sheets | 0 |
| Sheet number range | Sheet 1 – Sheet 17 |
| DO year range | 1987 – 2024 |
| Avg revisions per workbook | 8.4 |
| Max revisions (RDO-56) | 17 |
| Min revisions (RDO-113A) | 5 |
| Naming anomalies | 25 across 14 workbooks |
| Shared DOs across RDOs | 30 Department Orders |
| Workbooks with condo+land mixed | 31/31 (100%) |
| Provincial with muni-per-sheet mapping | 7/7 (100%) |
| Effectivity date formats | 3 (Excel serial 86%, ISO 9%, human 5%) |
