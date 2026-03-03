# Workbook Column Layouts — Data Format Analysis

**Wave:** 2 — Data Format Analysis
**Date:** 2026-03-03
**Aspect:** `workbook-column-layouts`

---

## Summary

All 31 sampled BIR zonal value workbooks (24 NCR + 7 provincial) were parsed to extract exact column positions, header text, and data types from their current-revision sheets. **Six distinct column position patterns** were identified, but a single dominant pattern covers 81% of workbooks. The most important finding for parser design is that **column headers repeat at every barangay block boundary** — meaning the parser can re-detect the layout dynamically rather than relying on a single header scan.

**Key findings:**
1. **6 column position patterns** identified (A–F), but Pattern A (standard 4-column) covers 25 of 31 workbooks (81%)
2. **18 distinct Col 0 (Street) header text variations** across 31 workbooks — no exact string match is reliable
3. **"VICINITY" is rendered as "V I C I N I T Y"** (spaced) in most NCR workbooks — header detection must handle letter-spaced text
4. **Headers repeat per barangay** — the column header row appears at the start of every barangay block (not just once per sheet)
5. **Headers can span 2 rows** — especially the ZV column where the revision ordinal is on row N and "ZV/SQ.M." is on row N+1
6. **Classification header is frequently hyphenated** across a line break: "CLASSIFI-CATION", "CLASSI-FICATION", "CLASS"
7. **Typos exist in official workbooks**: "CLASSSIFICATION" (triple S), "2V/SQ.M" (2 instead of Z), "Effecivity" (misspelling)

---

## Pattern Taxonomy

### Pattern A: Standard 4-Column (25/31 workbooks — 81%)

```
Col 0: STREET/SUBDIVISION [+ CONDOMINIUM/TOWNHOUSE variants]
Col 1: VICINITY [or "V I C I N I T Y"]
Col 2: CLASSIFICATION [or abbreviated/hyphenated variants]
Col 3: ZV/SQ.M. [with revision ordinal prefix]
```

**Workbooks using this pattern:**

| Region | RDOs |
|--------|------|
| NCR – Manila (RR6) | 29, 31, 32, 34 |
| NCR – QC (RR7A) | 28, 40 |
| NCR – East NCR (RR7B) | 41, 43, 45, 46 |
| NCR – Makati (RR8A) | 47, 48, 50 |
| NCR – South NCR (RR8B) | 44, 51, 52, 53A, 53B |
| Provincial – Pangasinan (RR1) | 4, 5 |
| Provincial – Laguna (RR9B) | 56, 57 |
| Provincial – Cebu (RR13) | 83 |
| Provincial – Davao (RR19) | 113A |

**Sample header (RDO 28, Novaliches):**
```
Row 105:
  Col 0: "STREET NAME/SUBDIVISIONS/ TOWNHOUSE/CONDOMINIUM"
  Col 1: "V I C I N I T Y"
  Col 2: "CLASSIFICATION"
  Col 3: "7TH REVISION ZV/SQ.M."
```

**Sample data (RDO 48, West Makati):**
```
Row 112: [Header]
Row 113: "AMORSOLO*"  | "DON BOSCO TO EDSA"  | "CR" | 288000.0
Row 114: ""           | ""                    | "RR" | 232000.0
```

### Pattern B: 5-Column with Split Vicinity (1/31 — 3%)

```
Col 0: STREET NAME/SUBD./CONDOMINIUM
Col 1: VICINITY (first boundary)
Col 2: (second boundary — optional overflow for cross-street references)
Col 3: CLASS
Col 4: ZV/SQ.M. [with revision ordinal prefix]
```

**Workbooks:** RDO 38 (North QC)

**Sample header (RDO 38):**
```
Row 109:
  Col 0: "STREET NAME/SUBD./CONDOMINIUM"
  Col 1: "V I C I N I T Y"
  Col 3: "CLASS"
  Col 4: "7TH REVISION ZV/SQ.M."
```

**Sample data:**
```
Row 150: "ANTONETTE"  | "PARKWAY VILLAGE" | "A. SAMSON" | "RR" | 40000.0
Row 151: "APACIBLE"   | "GRACE AVENUE"    | "J. AQUINO CRUZ" | "RR" | 46000.0
Row 152: "B. OLIVEROS" | "OLIVEROS DRIVE" | ""          | "RR" | 46000.0
```

**Parser note:** Col 2 contains the second cross-street when a vicinity spans two boundaries (e.g., "PARKWAY VILLAGE" to "A. SAMSON"). When Col 2 is empty, the vicinity is a single reference. The parser should concatenate Col 1 and Col 2 with a separator (e.g., " - ") when both are non-empty.

### Pattern C: 5-Column with Offset Gap (1/31 — 3%)

```
Col 0: STREET NAME / SUBDIVISION / CONDOMINIUM
Col 1: (empty gap — unused in data rows)
Col 2: VICINITY [as "V I C I N I T Y"]
Col 3: CLASSIFICATION
Col 4: ZV/SQ.M. [with revision ordinal prefix]
```

**Workbooks:** RDO 39 (South QC)

**Sample header (RDO 39):**
```
Row 105:
  Col 0: "STREET NAME / SUBDIVISION / CONDOMINIUM"
  Col 2: "V I C I N I T Y"
  Col 3: "CLASSIFICATION"
  Col 4: "7TH REVISION"
Row 106:
  Col 4: "ZV/SQ.M."
```

**Sample data:**
```
Row 157: "AGHAM/BIR ROAD"  | "" | "QUEZON AVE.-EAST AVE." | "GL" | 99000.0
Row 158: "ELIPTICAL CIRCLE" | "" | "EAST AVE.-KALAYAAN"   | "GL" | 76000.0
Row 159: ""                 | "" | ""                      | "X"  | 78000.0
```

**Parser note:** Col 1 is always empty in data rows. This appears to be a formatting artifact — the column exists in the spreadsheet but carries no data. The header also shows the ZV column split across two rows (revision ordinal on row N, "ZV/SQ.M." on row N+1).

### Pattern D: Side-by-Side Comparison (1/31 — 3%)

```
Col 0: STREET/SUBDIVISION (name — merged across cols 0-3 in display)
Col 4: VICINITY (merged across cols 4-5)
Col 6: CLASSIFICATION
Col 7: Previous revision ZV/SQ.M.
Col 8: Current revision ZV/SQ.M.
```

**Workbooks:** RDO 30 (Binondo)

**Sample data (RDO 30):**
```
Row 109: "(List of Streets)" ... Col 7: "(Previous Revision)"
Row 110: "DASMARINAS" | | | | "M DE BINONDO - Q. PAREDES" | | "CR" | 56000.0 | 132400.0
Row 111: "ESTRAUDE"   | | | | "M DE BINONDO - J. LUNA"    | | "CR" | 17000.0 | 55550.0
```

**Critical feature:** This is the only pattern with **two ZV columns** — the previous revision value and the current revision value side by side. The parser must identify which column holds the current ZV. The "Previous Revision" label in the header row at Col 7 serves as the discriminator.

**Additional note:** "NEW" appears as a string value in Col 7 when a property has no previous ZV (newly added in this revision). The parser must handle this as a null/absent previous value.

### Pattern E: Wide-Gap Merged (2/31 — 6%)

```
Col 0: STREET/SUBDIVISION (merged across cols 0-2)
Col 3: VICINITY (merged across cols 3-4)
Col 5: CLASSIFICATION
Col 6: ZV/SQ.M.
```

**Workbooks:** RDO 33 (Intramuros-Ermita-Malate), RDO 81 (Cebu City North)

**Sample header (RDO 33):**
```
Row 83:
  Col 0: "STREET/SUBDIVISION"
  Col 3: "V I C I N I T Y"
  Col 5: "CLASS"
  Col 6: "ZV/SQ.M."
```

**Sample data (RDO 33):**
```
Row 85: "ATLANTA STREET" | | | "7TH STREET- 8TH STREET" | | "CR" | 90100.0
Row 86: "BONIFACIO DRIVE" | | | "PASIG RIVER- 11TH STREET" | | "CR" | 90100.0
```

**Parser note:** This pattern arises from merged cells creating visual column widths wider than a single Excel column. Cols 1-2 are subsumed by the Street merge; Col 4 is subsumed by the Vicinity merge. The parser should detect the pattern by finding CLASSIFICATION at Col 5 rather than Col 2.

### Pattern F: Gap-at-2-3 (1/31 — 3%)

```
Col 0: STREET NAME / SUBDIVISION / CONDOMINIUM
Col 1: VICINITY
Col 2-3: (empty gap)
Col 4: CLASSIFICATION
Col 5: ZV/SQ.M. [with revision ordinal prefix]
```

**Workbooks:** RDO 42 (San Juan)

**Sample header (RDO 42):**
```
Row 106:
  Col 0: "STREET NAME / SUBDIVISION / CONDOMINIUM"
  Col 1: "VICINITY"
  Col 4: "CLASSIFICATION"
  Col 5: "7TH REVISION ZV/SQ.M."
```

**Sample data:**
```
Row 109: "A MABINI"  | "WILSON-ARAULLO" | | | "RR" | 70000.0
Row 110: "ARAULLO"   | "A. MABINI-CREEK" | | | "RR" | 67000.0
```

**Additional note:** In later barangays within the same workbook, the header text changes to "FINAL" instead of "7TH REVISION ZV/SQ.M." — confirming that header text can vary *within a single workbook* across barangay blocks.

---

## Column Position Summary Table

| Pattern | Col 0 | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 | Col 7 | Col 8 | Workbooks | % |
|---------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-----------|---|
| A | Street | Vicinity | Class | ZV | — | — | — | — | — | 25 | 81% |
| B | Street | Vicinity₁ | Vicinity₂ | Class | ZV | — | — | — | — | 1 | 3% |
| C | Street | _(gap)_ | Vicinity | Class | ZV | — | — | — | — | 1 | 3% |
| D | Street | _(merge)_ | _(merge)_ | _(merge)_ | Vicinity | _(merge)_ | Class | Prev ZV | Curr ZV | 1 | 3% |
| E | Street | _(merge)_ | _(merge)_ | Vicinity | _(merge)_ | Class | ZV | — | — | 2 | 6% |
| F | Street | Vicinity | _(gap)_ | _(gap)_ | Class | ZV | — | — | — | 1 | 3% |

---

## Column Header Text Variations

### Col 0: Street/Subdivision (18 distinct variants observed)

| # | Exact Header Text | RDO(s) |
|---|------------------|--------|
| 1 | `STREET NAME/SUBDIVISIONS/ TOWNHOUSE/CONDOMINIUM` | 28 |
| 2 | `STREET NAME / SUBDIVISION` | 29 |
| 3 | `STREET/SUBDIVISION` | 31, 45 |
| 4 | `STREET/SUBDIVISION/CONDOMINIUM` | 32 |
| 5 | `STREET/SUBDIVISION/ CONDOMINIUM` | 34 |
| 6 | `STREET NAME/SUBD./CONDOMINIUM` | 38 |
| 7 | `STREET NAME / SUBDIVISION / CONDOMINIUM` | 39, 42, 4, 5 |
| 8 | `STREETS/SUBDIVISIONS/ CONDOMINIUMS/TOWNHOUSES` | 40, 53B |
| 9 | `STREET NAME/ SUBDIVISION/ CONDOMINIUM/TOWNHOUSE` | 41 |
| 10 | `STREET NAME/ SUBDIVISION/ CONDOMINIUM` | 43, 52 |
| 11 | `STREET/SUBDIVISION/CONDOMINIUM/ TOWNHOUSES` | 44 |
| 12 | `STREET/SUBDIVISION/` + newline + `TOWNHOUSES/CONDOMINIUMS` | 47 |
| 13 | `STREET NAME / SUBDIVISION` | 48 |
| 14 | `STREET/SUBDIVISION/CONDOMINIUM/TOWNHOUSES` | 50 |
| 15 | `STREET/SUBDIVISION` | 51, 53A |
| 16 | `STREET NAME / SUBDIVISION/CONDOMINIUM` | 56, 57, 81 |
| 17 | `STREET NAME/ SUBDIVISION/CONDOMINIUM` | 83 |
| 18 | `STREET NAME/SUBDIVISION/CONDOMINIUM` | 113A |

**Parser recommendation:** Match on `STREET` keyword in the cell text. All 18 variants contain "STREET" as the first word. The additional qualifiers (SUBDIVISION, CONDOMINIUM, TOWNHOUSE) are informational and do not affect parsing.

### Col 1/2/3: Vicinity (2 variants)

| Variant | RDOs | Frequency |
|---------|------|-----------|
| `VICINITY` | Provincial (4, 5, 56, 57, 81, 83, 113A), NCR (29, 42, 46) | 10/31 (32%) |
| `V I C I N I T Y` (letter-spaced) | NCR (28, 31, 32, 33, 34, 38, 39, 40, 41, 43, 44, 45, 47, 48, 50, 51, 52, 53A, 53B) | 19/31 (61%) |
| Not labeled (comparison layout) | 30 | 1/31 (3%) |
| Labeled as `(List of Streets)` (comparison) | 30 | (same) |

**Critical finding:** The letter-spaced "V I C I N I T Y" is the *majority* variant in NCR. The parser must normalize this by collapsing spaces before keyword matching: `text.replace(" ", "")` → `"VICINITY"`.

### Col 2/3/5: Classification (7 variants)

| Variant | RDOs | Notes |
|---------|------|-------|
| `CLASSIFICATION` | 28, 39, 44, 48, 50, 57, 81, 83, 113A | Ideal form |
| `CLASS` | 32, 33, 38 | Abbreviated |
| `CLASSIFI-CATION` | 52 | Hyphenated (narrow column) |
| `CLASSI-FICATION` | 56 | Alternative hyphenation |
| `CLASSIFI- CATION` | 41 | Hyphen with space |
| `CLASSSIFICATION` | 34 | Typo (triple S) |
| `FICATION` | (multi-row split) | Only second half visible |

**Parser recommendation:** Match on `CLASS` prefix (covers all 7 variants) or `FICATION` suffix (catches multi-row splits). Combined regex: `/CLASS|FICATION/i`.

### Col 3/4/5/6: Zonal Value (12+ variants)

| Variant | RDOs | Notes |
|---------|------|-------|
| `ZV/SQ.M.` | 31, 33 (early rev) | Plain, no revision |
| `INITIAL ZV/SQ.M.` | (1st revisions) | First-ever revision |
| `[N]TH REVISION ZV/SQ.M.` | 44, 51, 83 | Full ordinal + full text |
| `[N]TH REV ZV/SQ.M.` | 52 | Abbreviated "REV" |
| `[N]TH REV ZV / SQM` | 47 | Spaces, no dots |
| `[N]TH REV ZV.SQ.M.` | 56, 57 | Dots instead of slashes |
| `[N]th REV. ZV / SQM` | 47 | Mixed case |
| `[N]TH REVISION Z.V./SQ.M.` | 48 | Dots in Z.V. |
| `[N]TH REVISION ZV/SQ.M.` | 28 | Standard with dots |
| `[N]TH REVISION ZV/SQM` | 29, 40, 51 | No dot after SQ |
| `[N]TH REV ZV/SQ. M` | 32 | Space before M |
| `FINAL` | 42 (some barangays) | Replaces revision ordinal |
| `4TH REVISION 2V/SQ.M` | 113A (Davao) | **Typo: "2V" instead of "ZV"** |
| `[N]th REVISION ZV.SQ.M` | 5 | Mixed case, dots |

**Parser recommendation:** Match on `ZV` or `SQ` or `REVISION` or `REV` as keywords. Must also handle "2V" typo (Davao) and "FINAL" (San Juan). The revision ordinal can be extracted with regex `/(\d+)\w*\s*REV/i` but is optional — the parser should not require it.

**Multi-row headers:** The ZV column header frequently splits across two rows:
- Row N: `"5TH REVISION"` or `"7TH REV"` or `"CLASSI-"`
- Row N+1: `"ZV/SQ.M."` or `"ZV.SQ.M"` or `"FICATION"`

The parser should combine header rows when detecting column layouts.

---

## Header Row Position Analysis

### Header Row Location (first occurrence in current revision sheet)

| Row Range | Count | RDOs |
|-----------|-------|------|
| 80–100 | 1 | 33 (Intramuros) |
| 100–110 | 16 | 28, 29, 31, 32, 34, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 53B |
| 110–120 | 8 | 38, 50, 51, 52, 53A, 81, 83, 113A |
| 120–130 | 4 | 4, 5, 56, 57 |
| Not found (comparison) | 1 | 30 (Binondo) |

**Typical layout:** The first ~80-120 rows contain the DO preamble (legal text, committee members, definitions, classification legend), followed by the first barangay header block and column headers.

### Header Repetition Pattern

**Critical finding:** Column headers are **not a one-time occurrence**. They repeat at the start of every barangay block. In a single workbook:

| RDO | Total Header Row Occurrences | Barangays |
|-----|------------------------------|-----------|
| 29 (Tondo) | 20 | ~20 |
| 32 (Quiapo-Sampaloc) | 12+ | ~300 numbered |
| 40 (Cubao) | 15+ | ~37 |
| 41 (Mandaluyong) | 12+ | 27 |
| 43 (Pasig) | 13 | ~38 |
| 45 (Marikina) | 12+ | ~16 |
| 46 (Cainta-Taytay) | 14 | ~20 |
| 51 (Pasay) | 19 | ~67 |
| 52 (Parañaque) | 10 | 16 |
| 83 (Talisay) | 19 | ~40 |
| 56 (Calamba) | 14 | ~130 |

**Parser implication:** Each barangay block starts with a metadata header (Province/City/Barangay/DO/Date) followed by the column header row. The parser can use the column header repetition as a **barangay block boundary detector**. This also means the parser can re-validate the column layout at each boundary — if it changes mid-workbook (unlikely but possible), the parser adapts.

### RDO 30 Binondo: No Standard Header

RDO 30 uses the comparison layout (Pattern D) and has **no standard column header row**. Instead:
- Row 109: `"(List of Streets)"` ... `"(Previous Revision)"`
- Data starts immediately at Row 110 with values in cols 0, 4, 6, 7, 8

The parser must detect this pattern by the presence of `"(List of Streets)"` or `"(Previous Revision)"` markers.

---

## Data Type Analysis

### ZV Column Data Types

| Type | RDOs | Handling |
|------|------|---------|
| Float (e.g., `77000.0`) | Most .xls workbooks | Cast to number, round if artifact |
| Integer (e.g., `41000`) | .xlsx workbooks (44, 81, 113A) | Use directly |
| String `"*"` or `"***"` | Various | Footnote marker — ZV is null/pending |
| String `"NEW"` | 30 (comparison column) | Previous ZV absent |
| String `"RR****"` | 53B | Classification + footnote marker in wrong column |
| Float with decimals (e.g., `28387.5`) | 81 (Cebu) | Genuine non-integer ZV — preserve |
| Float artifact (e.g., `118999.99999999999`) | 50, 41 | Round to nearest integer |
| Empty | Various | Continuation row (carry forward street name) |

**Parser logic:**
1. If numeric → use value (round to nearest integer if within 0.01 of integer; preserve otherwise)
2. If string starting with `*` → null ZV, extract footnote marker
3. If `"NEW"` → null previous ZV
4. If empty → continuation row (inherit street name from above)

### Classification Column Data Types

| Type | Example | RDOs | Notes |
|------|---------|------|-------|
| Clean code | `"CR"`, `"RR"`, `"RC"` | Most | Standard |
| Code + footnote | `"CR*"`, `"RR***"`, `"RR****"` | Various | Strip asterisks, preserve as metadata |
| Code + space | `"CR "`, `" RR"` | Occasional | Trim whitespace |
| Multi-line code | (merged cell spans) | 48 | Vertical merge — code in merged range |
| `"A*"` | 83 (Cebu) | Placeholder for unassigned agricultural subtype |

---

## Structural Constants (reliable across all 31 workbooks)

Despite significant variation, these structural elements are **invariant**:

1. **Four semantic columns exist**: Street, Vicinity, Classification, ZV — regardless of physical column positions
2. **Street is always Col 0** (leftmost column contains street/property names in all 6 patterns)
3. **ZV is always the rightmost data column** (or rightmost-1 in comparison Pattern D)
4. **Classification always immediately precedes ZV** (no gap between Class and ZV columns)
5. **Header rows contain detectable keywords**: "STREET" (Col 0), "VICINITY"/"V I C I N I T Y" (Vicinity), "CLASS"/"FICATION" (Classification), "ZV"/"SQ"/"REV" (ZV)
6. **Headers repeat per barangay** — providing continuous re-detection opportunities
7. **Continuation rows** (multi-classification per street) always have Col 0 empty with Classification and ZV filled
8. **"ALL OTHER STREETS"** catch-all row exists in every barangay block

---

## Parser Design Recommendations

### Column Detection Algorithm

```
fn detect_column_layout(row: &[CellValue]) -> ColumnLayout {
    // 1. Find Street column: first cell containing "STREET" keyword
    let street_col = find_keyword(row, ["STREET", "SUBDIVISION"]);

    // 2. Find Vicinity column: cell containing "VICINITY" (normalize spaces first)
    let vicinity_col = find_keyword(row, ["VICINITY"]);  // after collapsing spaces

    // 3. Find Classification column: cell containing "CLASS" or "FICATION"
    let class_col = find_keyword(row, ["CLASS", "FICATION"]);

    // 4. Find ZV column: cell containing "ZV", "SQ", "REV", or "FINAL"
    let zv_col = find_keyword(row, ["ZV", "SQ.M", "REVISION", "REV", "FINAL"]);

    // 5. Pattern D detection: check for "(Previous Revision)" marker
    let prev_zv_col = find_keyword(row, ["Previous Revision"]);

    // 6. If ZV column not found, check next row (multi-row header)
    // 7. Validate: street_col < vicinity_col < class_col < zv_col

    ColumnLayout { street_col, vicinity_col, class_col, zv_col, prev_zv_col }
}
```

### Keyword Normalization

Before matching header keywords, normalize cell text:
1. Collapse multiple spaces: `"V I C I N I T Y"` → `"VICINITY"`
2. Remove hyphens at line breaks: `"CLASSIFI-CATION"` → `"CLASSIFICATION"`
3. Strip newlines: `"STREET NAME/\nSUBDIVISION"` → `"STREET NAME/SUBDIVISION"`
4. Uppercase for comparison

### Barangay Block Detection

Each barangay block begins with:
1. Metadata rows (Province/City/Barangay/DO/Date) — detect by `"BARANGAY"`, `"Zone/Barangay"`, or `"City/Municipality"` keyword
2. Column header row — detect by Street + Vicinity/Classification keywords in same row
3. Data rows — until the next barangay block or end of sheet

### Handling Pattern D (Comparison)

Pattern D (RDO 30 Binondo) requires special handling:
- No standard header → detect via `"(List of Streets)"` marker
- Two ZV columns → use Col 8 (current) as the ZV, Col 7 as previous
- Street names at Col 0, Vicinity at Col 4, Classification at Col 6
- This pattern may appear in other comparison-format workbooks (observed in RDO 52's 8th revision as well)

---

## Anomalies and Edge Cases

### 1. Header Text Changes Within Same Workbook (RDO 42)
The ZV column header changes from `"7TH REVISION ZV/SQ.M."` to `"FINAL"` in later barangay blocks within the same sheet. This doesn't affect the column position — only the text label changes.

### 2. Phantom Columns
Several workbooks report far more columns than actually used:

| RDO | Reported Cols | Actual Data Cols | Cause |
|-----|--------------|-----------------|-------|
| 32 (DO 21-19) | 19 | 4 | Stray formatting |
| 44 (Sheet 9) | 16,384 (XFD) | 4 | OpenXML artifacts |
| 51 (DO 38-09) | 252 | 4 | Stray data |
| 47 (DO 23-12) | 254 | 4 | Stray data |

**Rule:** Never use `sheet.ncols` / `sheet.max_column` to determine data width. Detect from header row.

### 3. RDO 49 (North Makati) False Header
Row 205 of RDO 49 contains a footnote that matches header keywords:
```
"***STREET AND VICINITY PERTAINS TO RDO 50 JURISDICTION; THUS, UPDATED BASED ON RDO NO. 49"
```
This is a note, not a column header. The parser should require **multiple keyword matches** in the same row (Street + at least one of Vicinity/Classification/ZV) to avoid false positives.

### 4. "VILLAGES/SUBDIVISIONS:" Section Headers
Several workbooks (44, 53A) have a `"VILLAGES/SUBDIVISIONS:"` label row that could be misidentified as a Street header since it contains "SUBDIVISION". The parser should reject rows where only Col 0 contains keyword text — a valid header row must have keywords in multiple columns.

### 5. Notes/Footnotes Containing Keywords
Workbooks frequently embed footnotes that contain keywords like "street", "classification", "vicinity":
```
"*Newly identified street, subdivision, condominium, vicinity or classification"
"**All streets are identified in the 5th Revision..."
"*****Values have been aligned pursuant to the provision of RMO 31-2019..."
```
These are single-cell rows (all text in Col 0) — the multi-column keyword requirement prevents false matches.

### 6. "2V/SQ.M" Typo (RDO 113A Davao)
The ZV column header reads `"4TH REVISION 2V/SQ.M"` — a typo where "Z" was typed as "2". The keyword matcher should include `"2V"` as an alternative for `"ZV"`, or the parser should fall back to positional detection when keyword matching fails.

---

## Data Implications for Downstream Waves

### For Wave 2 (Other Aspects)
- **merged-cell-patterns**: Patterns D and E are *caused* by merged cells — the column positions reflect the unmerged cell grid, not the visual layout
- **sheet-organization**: Pattern D (comparison) appears in specific revision sheets, not universally — confirming that sheet parsing must be pattern-aware
- **data-size-estimation**: The 4 semantic columns (Street, Vicinity, Class, ZV) are the normalized output regardless of the 4-10 physical columns — normalization compresses Pattern D/E/F into Pattern A

### For Wave 3 (Resolution Logic)
- The **continuation row pattern** (empty Col 0 with Classification/ZV filled) is universal — the address matching engine must track "current street name" state as it processes rows
- **"ALL OTHER STREETS"** catch-all rows confirm the barangay-level fallback mechanism — every barangay has at least one

### For Wave 5 (Architecture)
- **Column detection is a runtime operation**, not a configuration — the parser must auto-detect the layout for each workbook (and potentially each barangay block)
- **6 patterns** can be reduced to a single normalized schema: `(street: String, vicinity: String, classification: String, zv: Option<f64>, prev_zv: Option<f64>)`
- The pattern detection can be implemented as a state machine that triggers on barangay block boundaries and re-validates at each header row repetition

---

## Sources

- 31 BIR zonal value workbooks (24 NCR + 7 provincial) parsed from `input/bir-workbook-samples/extracted/` and `input/bir-workbook-samples/extracted-provincial/`
- Raw extraction data saved to `raw/column-layout-extraction.json` and `raw/column-layout-current-revision.json`
- Prior analysis: `analysis/bir-workbook-ncr-samples.md`, `analysis/bir-workbook-provincial-samples.md`
- Normative standard: `analysis/rmo-31-2019-annexes.md` (Annex C)
