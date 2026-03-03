# Footnote Convention Mapping

**Wave**: 2 — Data Format Analysis
**Date**: 2026-03-03
**Source**: 16 workbooks parsed (10 NCR, 6 provincial) from `input/bir-workbook-samples/`
**Raw data**: `raw/footnote_extraction_raw.json` (3.5 MB, 138K lines)
**Extraction script**: `raw/footnote_extraction.py`

## Executive Summary

BIR zonal value workbooks use asterisk-based footnote markers (`*`, `**`, `***`, etc.) to annotate revision status of streets, vicinities, classifications, and zonal values. **There is no universal footnote schema.** Marker meaning is locally scoped — varying by Revenue Region, by RDO, and sometimes by barangay section within a single revision sheet. The parser must strip markers for data extraction but preserve them as metadata for audit trail and revision tracking.

## 1. Marker Inventory

### 1.1 Asterisk Counts by Region

| Marker | NCR occurrences | Provincial occurrences | Total |
|--------|----------------:|----------------------:|------:|
| `*` | 831 | 2,641 | 3,472 |
| `**` | 209 | 1,170 | 1,379 |
| `***` | 91 | 170 | 261 |
| `****` | 17 | 56 | 73 |
| `*****` | 133 | 37 | 170 |
| `******` | 40 | 4 | 44 |
| `*******` | 10 | 2 | 12 |
| `********` | 4 | 0 | 4 |
| `*********` | 2 | 0 | 2 |
| `***********` | 1 | 0 | 1 |

**Total annotated cells**: ~5,418 across 16 workbooks (current revision sheets only).

**Extremes**: RDO 44 Taguig reaches 11 asterisks. RDO 30 Binondo has **zero** footnotes — demonstrating the convention is entirely optional.

### 1.2 Regional Density

| Region | Median annotated cells/workbook | Range |
|--------|-------------------------------:|------:|
| NCR | ~60 | 0–1,126 |
| Provincial | ~900 | 62–3,412 |

Provincial workbooks are **15× more footnote-dense** than NCR workbooks on average.

## 2. The Reversal Problem

The most critical finding: **identical markers have opposite meanings across regions.**

| Marker | Pangasinan/Laguna Convention | NCR/Cebu Convention |
|--------|------------------------------|---------------------|
| `*` | Newly identified street/vicinity/classification | Deleted / does not exist per ocular inspection |
| `**` | Deleted / no longer exists | Newly added (in some RDOs) |
| `***` | — | Newly identified (in some RDOs) |
| `****` | Newly created (per ocular inspection) | Reclassified (in some RDOs) |

**This is not a clean binary split.** Some RDOs within the same Revenue Region use different conventions, and some use ad hoc meanings that don't fit either pattern. The only reliable approach is per-workbook legend parsing.

## 3. Semantic Categories

Across all workbooks, footnote markers encode 10 distinct semantic categories:

| Category | NCR count | Provincial count | Example |
|----------|----------:|----------------:|---------|
| **Deleted/inexistent** | 52 | 198 | "RATZAR HAS BEEN DELETED, DOES NOT EXIST PER OCULAR INSPECTION" |
| **Newly identified** | 1 | 204 | "CR* = newly identified classification" |
| **New subdivision/condo** | 0 | 103 | "**New subdivision" |
| **Non-standard classification** | 0 | 54 | "* not among the standard classification code" (Cebu) |
| **Redefined vicinity** | 0 | 56 | "**redefined"; "*REDEFINED FROM PREVIOUS VICINITY" |
| **Renamed street** | 38 | 44 | "S. Osmena Sr. St. formerly Poloyapoy St" |
| **Transferred location** | 2 | 37 | "*** Values transferred to (Barangay Name)" |
| **Reclassification** | 2 | 10 | "****Reclassified from S* to CR" |
| **Corrected entry** | 2 | 3 | "*Corrected vicinity (combined)" |
| **New road/classification** | 21 | 2 | "** NEW — New road/property classification introduced" |

**NCR footnotes are dominated by deletions and renames.** Provincial footnotes are dominated by new identifications and classification additions.

## 4. Column Position Analysis

Footnote markers appear in **all four semantic columns**, with dramatically different distributions by region:

| Column | NCR total | Provincial total | Key insight |
|--------|----------:|----------------:|-------------|
| Street/zone name (Col A) | 941 | 406 | NCR primary annotation target |
| Vicinity (Col B) | 137 | 572 | Provincial annotates vicinities more |
| Classification (Col C) | 1 | 2,687 | **Provincial almost exclusively** |
| Zonal value (Col D+) | 259 | 415 | Both regions; value-as-footnote pattern |

### 4.1 Classification Column: The Critical Case

**2,739+ rows** across 19 RDOs have asterisk-embedded classification values. This is the highest-impact parsing concern because classification codes are used for matching.

| Pattern | Example | Count | RDOs |
|---------|---------|------:|------|
| `CODE*` (suffix) | `CR*` | 1,200+ | 57, 81, 53B, 41, 42, 45, 83 |
| `*CODE` (prefix) | `*RR` | 700+ | 56, 53A, 48 |
| `CODE**` | `RR**` | 400+ | 57, 81, 53B, 56 |
| `CODE***` | `CR***` | 200+ | 81, 40, 53B, 56 |
| `CODE****` | `RR****` | 50+ | 53B, 81 |
| `CODE*****` | `CR*****` | 30+ | 48, 81 |
| `*****CODE` | `*****CR` | 7 | 48 |
| Full footnote text | `** APD under Resolution...` | 30+ | 34, 42, 52 |

**Regional position preference**:
- Laguna (RDO 56, 57): Predominantly **prefix** (`*RR`, `**CR`)
- NCR (RDO 40, 41, 53B): Predominantly **suffix** (`CR*`, `RR***`)
- Cebu (RDO 81, 83): Predominantly **suffix** (`PS*`, `RC****`)

### 4.2 Vicinity Column

1,209 unique vicinity values are asterisk-annotated. Examples:
- `*RIZAL AVE. - END` — asterisk-prefixed cross-street
- `200M ALONG BRGY ROAD**` — asterisk-suffixed road-proximity
- `MOUNTAINOUS**` — watershed/terrain with annotation

### 4.3 ZV Column

ZV cells sometimes contain pure footnote markers instead of numeric values:
- `"*"` or `"***"` → ZV is null/pending (footnote marker only)
- `"RR****"` → Classification + footnote marker in wrong column (RDO 53B)

### 4.4 Street Name Column

941 NCR street/zone names carry asterisk annotations, typically indicating:
- New streets added since prior revision
- Streets renamed (often with `(formerly ...)` annotation)
- Streets deleted from schedule

## 5. Legend Placement Patterns

All footnote legends are **inline** — not in separate header/footer sections. Three placement patterns:

### Pattern A: Per-Barangay Legend Block (Most Common)

Legend appears immediately after each barangay's data rows:
```
[Barangay data rows]
Row N+1: * Newly identified street/subdivision/condominium/vicinity/classification
Row N+2: ** Deleted/inexistent property
Row N+3: *** Values transferred to [Barangay Name]
[Next barangay header]
```

Found in: Pangasinan, Laguna, most NCR RDOs.

### Pattern B: "Note:" Prefix Convention (Cebu)

Uses explicit `Note:` prefix:
```
Row 1915: Note:   * 50 Meters is omitted and renamed
Row 1916:         **Previously "A" would mean Other Agricultural Lands, hence A50
```

Found in: RDO 83 Talisay, RDO 38 North QC, RDO 56 Calamba.

### Pattern C: Numbered Footnotes (Cebu Unique)

Numeric prefixes combined with asterisks form indexed footnotes:
```
Row 1841: 6*  Fronting Libre St. changed to vicinity of Libre St.
Row 1842: 7*  Renamed Tubod Landahan Road to Magsaysay Junction
Row 1845: 10* St. John St. of Sahagun Drive formerly Sinakit St.
```

These reference specific numbered zones/vicinities in the data rows above. Found only in RDO 83 Talisay Cebu.

### Legend Detection Heuristics

A legend row can be identified by:
1. Starts with `*` followed by a word (not a number or classification code)
2. Starts with `Note:` or `LEGEND:` or `FOOTNOTE:`
3. Single-cell row (all text in Col A, other columns empty)
4. Contains phrases: "newly identified", "deleted", "does not exist", "transferred", "redefined", "reclassified", "formerly"
5. Length > 30 characters with asterisk prefix (data rows with asterisks are typically shorter)

## 6. Cross-Revision Consistency

Footnote conventions are **NOT inherited across revision sheets** within the same workbook:

| Workbook | Current sheet markers | Prior sheet markers | Consistent? |
|----------|----------------------:|--------------------:|-------------|
| RDO 30 Binondo | 0 | 0 | Yes (none) |
| RDO 38 North QC | 11 | 0 | No — new in latest |
| RDO 47 East Makati | 16 | 158 | No — massive reduction |
| RDO 49 North Makati | 31 | 38 | ~Yes |
| RDO 51 Pasay | 66 | 0 | No — new in latest |
| RDO 42 San Juan | 261 | 22 | No — 12× increase |
| RDO 56 Calamba | 1,110 | 414 | ~Yes (both heavy) |
| RDO 83 Talisay | 677 | 1,148 | ~Yes (prior heavier) |

**Parser implication**: Each revision sheet must be treated as an independent footnote context. A marker `*` in Sheet 6 (DO 032-24) may have a different meaning than `*` in Sheet 7 (DO 015-21).

## 7. Special Annotation Patterns

### 7.1 "(NEW)" Vicinity Marker (RDO 57)

RDO 57 uses `(NEW)` as a vicinity-column annotation instead of asterisks:
```
LAGUNA BEL AIR |         | RR  | 17,100
               | (NEW)   | CR* | 22,200
               | INTERIOR LOT | RR | 10,800
```

Functions as both a footnote ("newly created classification") and a vicinity modifier.

### 7.2 Embedded Revision Numbers (RDO 83 Cebu)

Classification cells embed revision numbers alongside asterisks: `"A50 23*"` — the `23` is a revision reference, `*` is the footnote marker. Parser must strip both.

### 7.3 Calculation Footnotes (Condo Sections)

Condo sections embed **calculation rules** as footnotes that are critical for value derivation:

| Rule | Source RDO | Formula |
|------|-----------|---------|
| Parking slot default | General | PS = 60% of unit value |
| Parking slot (Taguig) | RDO 44 | PS = 70% of condo value |
| Penthouse | South Makati | PH = 110% of CC, or 120% of RC |
| Ground floor upgrade | South Makati, RDO 57 | Ground floor RC = CC + 20% |
| Business use upgrade | RDO 42 | CC = 120% of RC when used for leasing |
| Specific PS values | RDO 51 Pasay | "Valuation for parking spaces were made specific" — use explicit PS rows |

**These are not mere annotations — they are computation rules.** The engine must store per-RDO/per-revision footnote rules and apply them when explicit values are missing.

### 7.4 Building Name Asterisks

Condo building names carry asterisk annotations: `"ALDER RESIDENCES**"` — references footnotes. Parser must strip before building name matching.

## 8. Parser Design

### 8.1 Marker Stripping Pipeline

```
fn strip_footnote_markers(raw: &str) -> (String, FootnoteMarker) {
    // 1. Count and strip leading asterisks
    let leading = count_leading_asterisks(raw);
    // 2. Count and strip trailing asterisks
    let trailing = count_trailing_asterisks(raw);
    // 3. Determine marker position (prefix vs suffix)
    let position = if leading > 0 && trailing == 0 {
        MarkerPosition::Prefix
    } else if trailing > 0 && leading == 0 {
        MarkerPosition::Suffix
    } else if leading > 0 && trailing > 0 {
        MarkerPosition::Both  // rare but exists
    } else {
        MarkerPosition::None
    };
    // 4. Strip embedded revision numbers (Cebu pattern: "A50 23*")
    let cleaned = strip_revision_number(stripped);
    // 5. Trim whitespace
    let cleaned = cleaned.trim().to_string();

    (cleaned, FootnoteMarker { count: max(leading, trailing), position })
}
```

### 8.2 Legend Row Detection

```
fn is_legend_row(row: &[Cell]) -> bool {
    // Single-cell rows (all content in Col A, rest empty)
    let non_empty = row.iter().filter(|c| !c.is_empty()).count();
    if non_empty != 1 { return false; }

    let text = row[0].as_str();
    // Starts with asterisk(s) followed by space and word
    if LEGEND_PATTERN.is_match(text) { return true; }  // r"^\*{1,11}\s+[A-Za-z]"
    // Starts with "Note:" or "LEGEND:" or "FOOTNOTE:"
    if text.starts_with("Note:") || text.starts_with("LEGEND:") { return true; }
    // Numbered footnote pattern (Cebu): "6* text..."
    if NUMBERED_FOOTNOTE.is_match(text) { return true; }  // r"^\d+\*\s+"
    false
}
```

### 8.3 Legend Parsing

```
struct FootnoteLegend {
    marker_count: u8,          // Number of asterisks (1-11)
    marker_position: MarkerPosition,
    semantic: FootnoteSemantic, // Deleted, NewlyIdentified, Transferred, etc.
    raw_text: String,          // Original legend text
    scope: LegendScope,        // Barangay, Sheet, or Workbook level
}

enum FootnoteSemantic {
    Deleted,              // "deleted", "does not exist", "inexistent"
    NewlyIdentified,      // "newly identified", "new"
    Transferred,          // "transferred to/from"
    Redefined,            // "redefined"
    Reclassified,         // "reclassified from X to Y"
    Renamed,              // "formerly", "previously named"
    NonStandard,          // "not among the standard classification code"
    Corrected,            // "corrected"
    CalculationRule,      // PS/PH/CC computation formulas
    Other(String),        // Unparseable — preserve raw text
}
```

### 8.4 Data Structure: Per-Record Footnote Metadata

```
struct ZonalRecord {
    // ... core fields (street, vicinity, classification, zv) ...

    // Footnote metadata (stripped during parsing, preserved for audit)
    street_footnote: Option<FootnoteMarker>,
    vicinity_footnote: Option<FootnoteMarker>,
    classification_footnote: Option<FootnoteMarker>,
    zv_footnote: Option<FootnoteMarker>,
}

struct FootnoteMarker {
    count: u8,              // 1-11
    position: MarkerPosition, // Prefix, Suffix, Both
}
```

### 8.5 Computation Rule Extraction

Condo calculation footnotes require a separate extraction pass:

```
struct CondoComputationRule {
    rdo_id: u8,
    revision_do: String,
    rule_type: CondoRuleType,
    formula: String,        // "PS = 0.60 * parent_zv"
    source_text: String,    // Original footnote text
}

enum CondoRuleType {
    ParkingSlotPercentage(f32),   // 0.60 or 0.70
    PenthouseMultiplier(f32),     // 1.10 or 1.20
    GroundFloorUpgrade(f32),      // 1.20
    BusinessUseUpgrade(f32),      // 1.20
    ExplicitValues,               // Use row-specific PS values
}
```

## 9. Implications for Engine Design

### 9.1 Data Pipeline

1. **Strip markers before normalization**: All asterisks must be removed from classification codes, street names, vicinities, and ZV cells before data enters the matching engine.
2. **Preserve markers as metadata**: The `FootnoteMarker` fields enable audit trail and revision tracking without polluting the matching logic.
3. **Parse legends per-section**: Each barangay block within each revision sheet may have its own legend. Legends must be scoped correctly.
4. **Handle ZV-as-footnote**: When ZV cell contains only asterisks (`"*"`, `"***"`), the record's zonal value is `None` — it's a deletion or pending entry.

### 9.2 Matching Engine

1. **Ignore footnote markers during matching**: `CR*` matches `CR`. `*RR` matches `RR`. The marker count is metadata, not part of the classification code.
2. **Deleted entries**: Records marked as deleted (per legend parsing) should be excluded from current-value queries but available for historical queries.
3. **Transferred entries**: Records marked as transferred should redirect to the target barangay.

### 9.3 RPVARA Transition

Footnote conventions in future BLGF SMV schedules are unknown. The engine must support:
- BIR footnote conventions (documented here)
- A separate, potentially different BLGF footnote system
- Graceful handling when BLGF schedules use no footnotes at all

### 9.4 Data Size Impact

Footnote metadata adds ~2 bytes per record (marker count + position, packed into u16):
- 690K records × 2 bytes = 1.38 MB additional
- With typical footnote density (~8% of records annotated): ~110 KB actual
- **Negligible impact on WASM bundle size**

## 10. Emergent Discoveries

1. **Numbered footnote indexing** (Cebu Pattern C) — a third annotation system beyond asterisks and `(NEW)`. Only found in 1 RDO but may exist in unsampled workbooks.
2. **Computation rules as footnotes** — these are not just annotations but active calculation directives. Must be stored in a structured `ComputationRule` table, not just preserved as text.
3. **Zero-footnote workbooks** (RDO 30 Binondo) — parser must handle gracefully when no legends exist.

## 11. Summary Table

| Dimension | Finding |
|-----------|---------|
| **Universal schema?** | No — locally scoped per RDO, per revision, sometimes per barangay |
| **Marker types** | 1–11 asterisks, prefix or suffix, `(NEW)`, numbered (`6*`) |
| **Meaning reversal** | `*` = "new" in Pangasinan/Laguna, "deleted" in some NCR RDOs |
| **Column targets** | All 4 columns; provincial = classification, NCR = street name |
| **Legend placement** | Inline, per-barangay; 3 patterns (block, Note:, numbered) |
| **Cross-revision** | NOT consistent; each sheet is independent |
| **Annotated records** | ~8% of all rows have at least one footnote marker |
| **Computation rules** | 6+ condo calculation rules embedded as footnotes |
| **WASM impact** | ~110 KB additional (negligible) |
| **Parser strategy** | Strip for matching, preserve as metadata, parse legends per-section |
