# Merged Cell Patterns — Data Format Analysis

**Wave:** 2 — Data Format Analysis
**Date:** 2026-03-03
**Aspect:** `merged-cell-patterns`

---

## Summary

All 31 sampled BIR zonal value workbooks (24 NCR + 7 provincial) were analyzed for merged cell usage across all sheets and all revisions. **52,327 total merges** were found, with **31,237 in current revision sheets alone**. The critical finding for parser design: **72% of all merges are vertical (single-column, multi-row)**, and these fall into two distinct categories that require fundamentally different handling — header repetition merges (safe to skip) vs. data cell merges (must be resolved to extract values).

**Key findings:**
1. **6 merge categories identified**, with vertical merges dominating at 72% of all current-revision merges
2. **Two distinct vertical merge roles**: header repetition (barangay block boundaries) vs. data row spanning (street/vicinity cells covering multiple classifications)
3. **12 of 31 workbooks have significant data-row vertical merges** — the parser must resolve these to correctly associate street names with classification/ZV values
4. **Pattern E (RDO 33, 81) uses horizontal merges for every data row** — street names span cols 0-2 and vicinity spans cols 3-4 as a core structural element, not just formatting
5. **Pattern D (RDO 30) uses multi-row block merges** for condo entries — building names span 3-4 rows × 4 cols
6. **Merge density correlates with data volume and recency** — newer, larger workbooks have dramatically more merges (RDO 32: 3,929 in current revision)
7. **Preamble merges are cosmetic-only** — the first ~100 rows of every sheet contain full-width merges for legal text, signatory blocks, and classification legends that carry no parseable data

---

## Merge Category Taxonomy

### Category Distribution (Current Revision Sheets)

| Category | Count | % | Description | Parser Impact |
|----------|------:|--:|-------------|---------------|
| **VERT** (vertical) | 22,484 | 72.0% | Single column, ≥2 rows | **HIGH** — must distinguish header vs. data |
| **FULL_H** (full-width horizontal) | 3,489 | 11.2% | ≥4 columns, 1 row | LOW — preamble/footnote text |
| **TRIPLE_H** (3-col horizontal) | 2,803 | 9.0% | 3 columns, 1 row | MEDIUM — Pattern E data rows + footnotes |
| **PAIR_H** (2-col horizontal) | 1,516 | 4.9% | 2 columns, 1 row | MEDIUM — Pattern E vicinity + signatory blocks |
| **BLOCK_H** (multi-row block) | 709 | 2.3% | ≥3 columns, ≥2 rows | MEDIUM — Pattern D condo names + preamble |
| **BLOCK** (block merge) | 236 | 0.8% | ≥2 columns, ≥2 rows | MEDIUM — Pattern D vicinity blocks |
| **TOTAL** | **31,237** | | | |

### Merge Geometry Distribution (All Workbooks, All Sheets)

The 52,327 total merges across all sheets and revisions exhibit 57 unique geometries. Top 10:

| Geometry | Count | Typical Use |
|----------|------:|-------------|
| 2r × 1c | 17,989 | Street name spanning 2 classifications; header cell spanning 2 rows |
| 3r × 1c | 11,357 | Header cell spanning 3 rows (barangay block); street with 3 classifications |
| 1r × 4c | 7,207 | Full-width preamble/footnote text |
| 1r × 3c | 6,030 | Pattern E street names (cols 0-2); 3-col footnotes |
| 1r × 2c | 5,174 | Pattern E vicinity (cols 3-4); signatory blocks; paired cells |
| 1r × 5c | 1,189 | Wide preamble text |
| 4r × 1c | 728 | Street with 4 classifications; Pattern D header cells |
| 2r × 4c | 565 | Preamble multi-row text blocks |
| 2r × 3c | 407 | Pattern D/E block headers |
| 2r × 2c | 180 | Pattern D vicinity blocks |

---

## Vertical Merge Deep Dive

Vertical merges (72% of all merges) serve two fundamentally different purposes:

### Type 1: Header Repetition Merges

**What they are:** Column header cells (STREET, VICINITY, CLASSIFICATION, ZV) merged across 2-3 rows at the start of each barangay block. Every workbook uses them.

**Example (RDO 28, Row 3107-3109, Pattern A):**
```
Row 3107: [Col 0] "STREET NAME/SUBDIVISIONS/ TOWNHOUSE/CONDOMINIUM" ─┐ merged 3r
Row 3108:                                                            │
Row 3109: ────────────────────────────────────────────────────────────┘
```
All 4 columns (Street, Vicinity, Classification, ZV) are merged at the same starting row, creating a visually taller header row at each barangay boundary.

**Parser handling:** Detect by checking if all 4 semantic columns are merged at the same row start AND contain header keywords. These merges are **informational only** — the parser already handles header row detection via keyword matching (see `workbook-column-layouts` analysis). The vertical merge just means the header occupies 2-3 physical rows instead of 1. Read the top-left cell value only.

**Frequency by workbook (current revision):**

| Workbook | Header Repetition Merges | Barangay Blocks (approx.) |
|----------|------------------------:|---------------------------|
| RDO 4 (Pangasinan) | 1,860 | ~465 headers × 4 cols |
| RDO 5 (Pangasinan) | 1,834 | ~458 headers × 4 cols |
| RDO 32 (Quiapo) | 1,174 | ~293 headers × 4 cols |
| RDO 29 (Tondo) | 1,034 | ~258 headers × 4 cols |
| RDO 34 (Paco) | 962 | ~240 headers × 4 cols |
| RDO 51 (Pasay) | 806 | ~201 headers × 4 cols |
| RDO 46 (Cainta) | 576 | ~144 headers × 4 cols |
| RDO 56 (Calamba) | 588 | ~147 headers × 4 cols |
| RDO 44 (Taguig) | 452 | ~113 headers × 4 cols |
| RDO 57 (Biñan) | 356 | ~89 headers × 4 cols |

### Type 2: Data Row Vertical Merges

**What they are:** Street name and/or vicinity cells merged vertically to span multiple rows where a single property has multiple classifications. Instead of using the "empty Col 0 = continuation row" pattern, these workbooks explicitly merge the street name cell across all classification rows.

**Example (RDO 48, West Makati):**
```
Row 114: [Col 0] "A. APOLINARIO ST." ─┐ merged 2r    [Col 1] "DALLAS ST. - EDSA" ─┐ merged 2r
Row 115:                               │                                             │
         [Col 2] "CR"    [Col 3] 288000  ← Row 114
         [Col 2] "RR"    [Col 3] 232000  ← Row 115
```

The street name "A. APOLINARIO ST." and vicinity "DALLAS ST. - EDSA" each occupy a single merged cell spanning 2 rows, while Classification and ZV have separate values per row.

**This is semantically identical to the continuation row pattern** (empty Col 0), but structurally different — the parser cannot rely on "empty Col 0 means continuation" when the cell is actually part of a merge range.

**Data vertical merge counts (current revision):**

| Workbook | Street Merges | Vicinity Merges | Total Data Vert | Pattern |
|----------|-------------:|----------------:|----------------:|---------|
| RDO 32 (Quiapo) | 1,266 | 1,267 | 2,533 | Every multi-class street merged |
| RDO 34 (Paco) | 1,095 | 1,092 | 2,187 | Every multi-class street merged |
| RDO 51 (Pasay) | 969 | 970 | 1,939 | Every multi-class street merged |
| RDO 50 (S. Makati) | 619 | 372 | 991 | Condo entries heavily merged |
| RDO 5 (Pangasinan) | 256 | 325 | 581 | Agricultural + rural |
| RDO 44 (Taguig) | 416 | 160 | 576 | Partial merge usage |
| RDO 48 (W. Makati) | 208 | 210 | 418 | Uniformly merged in data |
| RDO 53B (Muntinlupa) | 137 | 146 | 283 | Including 1 x 17-row merge |
| RDO 113A (Davao) | 70 | 66 | 136 | Provincial pattern |
| RDO 29 (Tondo) | 74 | 89 | 163 | Partial merge usage |
| RDO 4 (Pangasinan) | 75 | 113 | 188 | Agricultural entries |
| RDO 31 (Sta. Cruz) | 36 | 36 | 72 | Moderate usage |

**12 of 31 workbooks (39%)** use data vertical merges. The remaining 19 use the continuation row pattern exclusively.

### Vertical Merge Span Distribution (Data Merges Only)

| Span | Meaning | Frequency |
|------|---------|-----------|
| 2 rows | Street with 2 classifications (e.g., RR + CR) | ~75% of data merges |
| 3 rows | Street with 3 classifications (e.g., RR + CR + I) | ~20% |
| 4 rows | Street with 4 classifications (e.g., RR + CR + RC + CC) | ~4% |
| 5-8 rows | Street/condo with many codes (often condo with RC+CC+PS per tower) | ~1% |
| 10-17 rows | Extreme: "ALL OTHER LOTS" catch-all with many agricultural sub-codes | <0.1% (RDO 4, 53B) |

**Extreme case — RDO 53B:** One merge spans **17 rows** for a single "EAST SERVICE ROAD" entry with 17 different classifications.

**Extreme case — RDO 4 (Pangasinan):** Agricultural catch-all entries ("ALL OTHER LOTS") merge up to 14 rows covering A1 through A14 sub-codes.

---

## Horizontal Merge Patterns

### Pattern E: Data Row Horizontal Merges (RDO 33, 81)

Pattern E workbooks use horizontal merges as a **core data structure**, not just formatting. Every data row contains:
- Street name merged across cols 0-2 (3-column span)
- Vicinity merged across cols 3-4 (2-column span)
- Classification at col 5 (unmerged)
- ZV at col 6 (unmerged)

**Example (RDO 33, Intramuros, Row 85):**
```
[Col 0-2 merged] "ATLANTA STREET"     [Col 3-4 merged] "7TH STREET- 8TH STREET"    [Col 5] "CR"    [Col 6] 90100.0
```

**RDO 33 has 347 horizontal merges in the data zone** — virtually every data row is horizontally merged. This is unique among all sampled workbooks.

**RDO 81 (Cebu City North) has 2,381 horizontal merges** in its data zone:
- 2,051 are empty-value pair/triple merges (blank cells between data columns)
- 193 are column header repetitions
- 130 are condo name labels
- 5 are barangay markers

The RDO 81 pattern shows that even when the 4 semantic columns map to cols 0, 3, 5, 6 (Pattern E), the intervening columns 1-2 and 4 contain merged empty cells.

**Parser implication:** For Pattern E workbooks, the parser must read values from cols 0, 3, 5, 6 (not 0, 1, 2, 3). The column layout detection algorithm from `workbook-column-layouts` already handles this by detecting the column where each header keyword appears, regardless of intervening empty/merged columns.

### Pattern D: Block Merges for Comparison Layout (RDO 30)

Pattern D uses multi-row, multi-column block merges for both headers and condo entries:

**Header block (repeating at each barangay):**
```
Row 105-108: [Col 0-3 merged, 4r×4c] "S T R E E T  N A M E / SUBDIVISION..."
             [Col 4-5 merged, 4r×2c] "V I C I N I T Y"
             [Col 6 merged, 4r×1c]   "CLASS"
             [Col 7 merged, 2r×1c]   "4th REVISION"
             [Col 8 merged, 2r×1c]   "5th REVISION"
```

**Condo name blocks:**
```
Row 136-138: [Col 0-3 merged, 3r×4c] "COHER REALTY DEVT CORP"
             [Col 4-5 merged, 3r×2c] "JUAN LUNA STREET"
```
Each condo building name and its vicinity are block-merged to span all 3 classification rows (RC, CC, PS).

**RDO 30 has 402 total merges in the current revision** — 142 full-width, 111 pair, 58 block headers, 58 blocks, 33 vertical. The comparison layout (with previous + current ZV columns) makes this the most structurally complex workbook.

**Parser implication:** The parser for Pattern D must:
1. Detect the pattern via `"(List of Streets)"` marker or `"(Previous Revision)"` text
2. Read street names from the top-left cell of 4-column block merges (cols 0-3)
3. Read vicinity from the top-left cell of 2-column block merges (cols 4-5)
4. Read classification from col 6, previous ZV from col 7, current ZV from col 8

### Full-Width Horizontal Merges (Preamble/Footnotes)

Every workbook contains full-width horizontal merges (4+ columns) for:
1. **DO preamble** (rows 0-60): Legal text, committee members, authority citations
2. **Classification legend** (rows 60-100): Code definitions, agricultural sub-code tables
3. **Barangay metadata** (repeating): "REVENUE REGION [N] - [CITY]", "RDO NO. [N] - [DISTRICT]"
4. **Footnotes** (end of data zone): Asterisk legends, fallback rules, special provisions
5. **Guideline appendix** (end of sheet): "CERTAIN GUIDELINES IN THE IMPLEMENTATION..."

These are uniformly ignorable by the data parser — they contain no zonal value records.

---

## Merge Density Analysis

### Current Revision Merge Counts (All 31 Workbooks)

| Tier | Workbooks | Merge Range | Characteristics |
|------|-----------|-------------|-----------------|
| **Extreme** (>2,000) | RDO 5, 32, 34, 51, 81 | 2,518–4,130 | Every multi-class entry merged; large data volumes |
| **Heavy** (1,000–2,000) | RDO 4, 29, 42, 44, 50 | 1,028–2,100 | Most multi-class entries merged |
| **Moderate** (300–999) | RDO 30, 31, 33, 39, 40, 43, 45, 46, 48, 53B, 56, 57 | 313–644 | Mix of header and data merges |
| **Light** (<300) | RDO 28, 38, 41, 47, 49, 52, 53A, 83, 113A | 28–287 | Primarily header repetition merges |

### Merge-to-Row Ratio

| Workbook | Data Rows | Merges | Ratio | Interpretation |
|----------|----------:|-------:|------:|----------------|
| RDO 81 (Cebu) | 2,359 | 2,518 | 1.07 | >1 merge per data row (Pattern E) |
| RDO 42 (San Juan) | 1,750 | 1,154 | 0.66 | High footnote merge count |
| RDO 48 (W. Makati) | 878 | 438 | 0.50 | Nearly every street merged |
| RDO 32 (Quiapo) | 5,866 | 3,929 | 0.67 | Massive data + merge volume |
| RDO 34 (Paco) | 4,728 | 3,171 | 0.67 | Similar to RDO 32 |
| RDO 51 (Pasay) | 4,987 | 3,314 | 0.66 | Dense urban data |
| RDO 52 (Parañaque) | 2,168 | 185 | 0.09 | Mostly header repetition |
| RDO 83 (Talisay) | 3,306 | 28 | 0.008 | Almost merge-free |

### Evolution Across Revisions

Merge usage has escalated dramatically over time:

| Era | Typical Merges per Sheet | Observation |
|-----|------------------------:|-------------|
| 1987–1997 (Sheets 1-4) | 8–46 | Minimal: preamble text only |
| 1998–2014 (Sheets 5-6) | 27–302 | Growing: header repetition begins |
| 2015–2019 (Sheets 7-8) | 175–3,929 | Explosion: data vertical merges become common |
| 2020–2024 (Sheets 8-10) | 28–4,130 | Wide variance: some RDOs adopt, others don't |

This suggests that data vertical merging is a relatively recent stylistic choice by individual RDO schedulers, not a mandated standard. The parser must support both patterns (merged vs. continuation-row) regardless of workbook era.

---

## Parser Design Implications

### Merge-Aware Parsing Strategy

The parser must handle merged cells in two phases:

**Phase 1: Merge Map Construction**
Before reading any data, build a merge map from the spreadsheet library's merge range data:
```
MergeMap: HashMap<(row, col), MergeInfo>
  where MergeInfo = {
    top_left_row: usize,
    top_left_col: usize,
    row_span: usize,
    col_span: usize,
    value: CellValue
  }
```
For any cell (r, c) that falls within a merge range, `MergeMap[(r,c)]` returns the merge info with the value stored in the top-left cell.

**Phase 2: Merge-Transparent Reading**
When reading a cell at (row, col):
1. Check if (row, col) is in the merge map
2. If yes: return the value from the top-left cell of the merge
3. If no: return the cell's own value (which may be empty for continuation rows)

This makes the parser agnostic to whether a workbook uses vertical merges or continuation rows — both produce the same result.

### Critical Rules

1. **Never read empty cells within a merge range as "empty"** — they contain the merged value from the top-left cell. Libraries like `xlrd` and `openpyxl` return empty/None for non-top-left cells in a merge; the parser must override this.

2. **Header row detection must account for multi-row headers** — a header merge spanning rows 105-107 means rows 106 and 107 are NOT data rows, even though they appear in the data zone.

3. **Row iteration must skip merge interior rows** — when processing a vertically merged street name, only process the first row of the merge as the "primary" data row. Subsequent rows within the merge are continuation classifications.

4. **Pattern E requires column remapping** — horizontal merges at cols 0-2 and 3-4 mean the parser reads street from col 0, vicinity from col 3, class from col 5, ZV from col 6 (not the standard 0,1,2,3).

5. **Pattern D requires block merge awareness** — 4-row × 4-column block merges contain a single street name; the parser must detect these and read only the top-left cell value.

### Recommended Data Structure (Rust)

```rust
struct MergeRange {
    row_start: u32,
    row_end: u32,    // inclusive
    col_start: u16,
    col_end: u16,    // inclusive
}

struct MergeMap {
    // Maps (row, col) of any cell in a merge to the range info
    cell_to_range: HashMap<(u32, u16), usize>,
    ranges: Vec<MergeRange>,
    // Pre-computed: value for each range (from top-left cell)
    values: Vec<CellValue>,
}

impl MergeMap {
    fn resolve(&self, row: u32, col: u16) -> Option<&CellValue> {
        self.cell_to_range.get(&(row, col))
            .map(|&idx| &self.values[idx])
    }

    fn is_merge_interior(&self, row: u32, col: u16) -> bool {
        // Returns true if this cell is inside a merge but NOT the top-left
        if let Some(&idx) = self.cell_to_range.get(&(row, col)) {
            let range = &self.ranges[idx];
            row != range.row_start || col != range.col_start
        } else {
            false
        }
    }
}
```

### Test Cases for Merge Handling

| Scenario | Workbook | Row | Expected Behavior |
|----------|----------|-----|-------------------|
| 2-row street merge | RDO 48, Row 114-115 | Read "A. APOLINARIO ST." from row 114; row 115 inherits same street |
| 3-row header merge | RDO 28, Row 3107-3109 | Detect as header row; skip rows 3108-3109 |
| Pattern E data row | RDO 33, Row 85 | Read street from col 0 (merged 0-2), vicinity from col 3 (merged 3-4) |
| Pattern D block merge | RDO 30, Row 136-138 | Read condo name "COHER REALTY" from top-left of 3r×4c block |
| 17-row extreme merge | RDO 53B, Row 111-127 | "EAST SERVICE ROAD" spans 17 classification rows |
| 14-row agricultural | RDO 4, Row ~11129 | "ALL OTHER LOTS" spans A1-A14 |
| Empty merge interior | RDO 48, Row 115, Col 0 | Must resolve to "A. APOLINARIO ST.", NOT empty |

---

## Workbook-Specific Notes

### RDO 42 (San Juan) — Footnote Merge Density

RDO 42 has **1,154 merges** in its current revision, but **964 are TRIPLE_H (3-col horizontal)**. Analysis shows these are primarily vicinity cell merges in Pattern F layout (gap at cols 2-3). The vicinity column at col 1 is merged with the empty cols 2-3, creating a 3-column span for every vicinity entry. This is a visual formatting choice, not a data structure issue — the parser reads col 1 for vicinity.

Additionally, RDO 42 has 62 BLOCK_H merges that are legal/guideline text blocks embedded after the last barangay — "THE ZONAL VALUES ESTABLISHED HEREIN SHALL APPLY..." spanning 3-8 rows × 5 columns.

### RDO 81 (Cebu City North) — Pattern E with Maximum Density

RDO 81 has **2,518 merges** in its current revision — the second-highest count in the sample. Despite using Pattern E (same as RDO 33), RDO 81 has 3× more merges because:
1. More barangays (58 blocks vs. RDO 33's ~15)
2. Empty intermediate columns also merged (creating 2,051 "blank" pair/triple merges)
3. Column header repetition at every block boundary

### RDO 5 (Pangasinan) — Provincial Maximum

RDO 5 has **4,130 merges** — the absolute highest in the sample. This is driven by:
1. 15,272 rows (largest workbook)
2. ~458 barangay blocks with 3-row header merges (1,834 header merges)
3. Agricultural entries with 5-8 row vertical merges for catch-all lots
4. 1,707 FULL_H merges (mostly barangay boundary markers in provincial multi-municipality format)

### RDO 53B (Muntinlupa) — Extreme Vertical Span

Contains a single 17-row vertical merge for "EAST SERVICE ROAD" at rows 111-127. This entry has 17 different classifications — the maximum observed span in any workbook. The parser's merge-transparent reading handles this correctly by treating row 111 as the primary row and rows 112-127 as continuation.

---

## Implications for Downstream Waves

### For Wave 2 (Other Aspects)
- **sheet-organization**: The preamble zone (rows 0-100) is consistently merge-heavy with cosmetic merges. The data zone merge style varies per RDO. Merge analysis confirms the preamble/data boundary is at the first column header row.
- **condo-table-structures**: Condo entries in Pattern D (RDO 30) use 3-row block merges for building names. In other patterns, condos use the same vertical merge pattern as streets. BGC FAR entries (RDO 44) are also vertically merged.
- **data-size-estimation**: Merge-aware parsing will produce the same normalized output regardless of whether merges are present — the record count is determined by unique (barangay, street, vicinity, classification, ZV) tuples, not by row count.

### For Wave 3 (Resolution Logic)
- **address-matching-algorithms**: Merged vicinity cells confirm that vicinity descriptions are always per-street, not per-classification — a single street segment always has the same vicinity regardless of how many classification codes apply.
- **classification-resolution-logic**: Vertical merges confirm the 1:N relationship between (street, vicinity) and classification codes — one location can have multiple valid classifications.

### For Wave 5 (Architecture)
- **data-pipeline-architecture**: The Excel parser must construct a merge map as the first step of sheet processing. This is O(n) in the number of merge ranges and requires no data reading — just the merge range metadata.
- **rust-engine-design**: The `MergeMap` data structure (see above) should be part of the parser module. It adds ~50KB overhead for the largest workbook (RDO 5, 4,130 ranges × 12 bytes per range).
- **Performance**: Building a merge map for a 4,130-range workbook is sub-millisecond. The actual cell resolution lookup is O(1) via HashMap. No performance concern.

---

## Sources

- 31 BIR zonal value workbooks (24 NCR + 7 provincial) analyzed from `input/bir-workbook-samples/extracted/` and `input/bir-workbook-samples/extracted-provincial/`
- Raw extraction data: `raw/merged-cell-extraction.json` (52,327 merge records with geometry, position, and value preview)
- Prior analysis: `analysis/workbook-column-layouts.md` (column pattern taxonomy)
- Prior analysis: `analysis/bir-workbook-ncr-samples.md` (initial merge severity observations)
- Prior analysis: `analysis/bir-workbook-provincial-samples.md` (provincial merge patterns)
