# Data Pipeline Architecture

**Wave 5 | Aspect: data-pipeline-architecture**
**Date:** 2026-03-04

## Overview

This analysis designs the complete data ingestion pipeline: from 124 heterogeneous BIR Excel workbooks to the binary WASM bundle consumed by the Rust engine. The pipeline must handle 6 column layout patterns (Wave 2), 52K+ merged cells (Wave 2), per-RDO footnote conventions (Wave 2), dual address models (Wave 2), 62+ classification codes with normalization (Wave 2), and integrate future BLGF SMV data sources (Wave 3).

**Pipeline output**: The `zv-engine` binary bundle format defined in Wave 5 rust-engine-design — 7 sections (header, strings, DOs, records, location index, codes index, jurisdiction/regime), targeting ~5.0 MB brotli for the full current-revision dataset.

**Design philosophy**: Offline batch pipeline, not a streaming service. Runs on schedule (weekly check, monthly rebuild) or on-demand when BIR publishes new Department Orders. Deterministic: same inputs → identical binary output (content-hash verified).

---

## 1. Pipeline Stages

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│  1. ACQUIRE  │───▶│  2. PARSE    │───▶│ 3. NORMALIZE │───▶│ 4. VALIDATE  │───▶│ 5. INDEX/PACK │───▶│ 6. PUBLISH   │
│  (fetch .xls)│    │  (per-sheet) │    │  (per-record)│    │  (cross-ref) │    │  (binary)     │    │  (CDN)       │
└─────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └───────────────┘    └──────────────┘
       │                  │                   │                   │                    │                    │
       ▼                  ▼                   ▼                   ▼                    ▼                    ▼
  input/bir-       raw/parsed/         raw/normalized/     raw/validation/       output/bundles/      CDN deploy
  workbook-        {rdo}.jsonl         {rdo}.jsonl         report.json           zv-{hash}.bin        + manifest
  samples/                                                                       zv-ncr-{hash}.bin
```

### Stage 1: Acquire

**Purpose**: Download BIR zonal value Excel workbooks for all 124 RDOs, detect changes since last run.

**Source**: `bir.gov.ph/zonal-values` — BIR hosts one `.xls` or `.xlsx` file per RDO, organized by Revenue Region.

```rust
/// Acquisition manifest — tracks download state per RDO.
struct AcquireManifest {
    entries: Vec<AcquireEntry>,
    last_full_run: DateTime<Utc>,
}

struct AcquireEntry {
    rdo_id: u8,                          // 1-125 (excluding 126 Digital Taxation)
    revenue_region: String,              // "RR6", "RR7A", etc.
    source_url: String,                  // BIR CDN URL
    filename: String,                    // e.g., "RDO 47 - North Makati.xls"
    last_downloaded: Option<DateTime<Utc>>,
    last_modified_header: Option<String>, // HTTP Last-Modified for change detection
    etag: Option<String>,                // HTTP ETag
    content_hash: Option<String>,        // SHA-256 of downloaded file
    file_format: FileFormat,             // Xls | Xlsx | Pdf (skip PDFs)
    status: AcquireStatus,              // New | Unchanged | Updated | Failed | PdfSkipped
}

enum FileFormat { Xls, Xlsx, Pdf }
enum AcquireStatus { New, Unchanged, Updated, Failed(String), PdfSkipped }
```

**Change detection strategy**:
1. HTTP conditional GET (`If-Modified-Since` / `If-None-Match`) — BIR CDN supports these inconsistently, so treat as optimization hint only
2. Content hash (SHA-256) comparison against prior download — authoritative
3. If hash matches → `Unchanged`, skip remaining stages for this RDO
4. If hash differs or new → `Updated`/`New`, proceed to Stage 2

**PDF handling**: Wave 1 found 1 PDF among 31 samples (RDO with image-based PDF). PDFs are flagged `PdfSkipped` and logged. They require manual OCR or BIR contact for machine-readable data. Expected: ~2-5 of 124 RDOs may be PDF-only.

**Rate limiting**: BIR CDN is not high-availability. 2s delay between downloads, retry 3× with exponential backoff, 10-minute total timeout per file.

**Design decision trace**: Wave 1 bir-workbook-ncr-samples found 23 .xls + 1 .xlsx + 1 PDF across 24 NCR RDOs. Format detection must be content-based (magic bytes), not extension-based — Wave 1 noted some .xls files are actually .xlsx with wrong extension.

---

### Stage 2: Parse

**Purpose**: Extract structured records from heterogeneous Excel workbooks. This is the most complex stage — it must handle all 6 column patterns (Wave 2 workbook-column-layouts), merged cells (Wave 2 merged-cell-patterns), sheet organization (Wave 2 sheet-organization), and condo structures (Wave 2 condo-table-structures).

#### 2.1 Sheet Discovery

Per Wave 2 sheet-organization, every workbook follows the same top-level pattern:
- Sheet 0: NOTICE (metadata table mapping DO# → municipality → effectivity date)
- Sheets 1+: Revision data sheets, newest first

```rust
/// Parsed from the NOTICE sheet (index 0 in every workbook).
struct NoticeTable {
    entries: Vec<NoticeEntry>,
}

struct NoticeEntry {
    sheet_index: usize,                // Which sheet in the workbook
    sheet_name: String,                // Raw sheet tab name (may have anomalies)
    do_number: String,                 // e.g., "DO 35-2021" (extracted, not raw)
    municipalities_covered: Vec<String>, // From "City/Municipalities Covered" column
    effectivity_date: NaiveDate,       // Parsed from 3 possible formats
    is_current: bool,                  // Most recent DO for each municipality
}
```

**NOTICE parsing algorithm**:
1. Read sheet at index 0
2. Scan rows 0-20 for header row containing "DEPARTMENT ORDER" or "D.O." keywords
3. Extract columns: DO#, sheet reference, municipalities, effectivity date
4. Parse effectivity dates using 3-format cascade:
   - Excel serial number (86% of workbooks): `days_since_1900_to_date()`
   - ISO datetime string (9%): standard parse
   - Human date string (5%): regex patterns ("January 1, 2024", "01/01/2024")
5. Determine current revision per municipality: latest effectivity date per municipality name
6. Handle shared DOs: Wave 2 found 30 DOs shared across RDO clusters (e.g., Makati 4-way split). Unique key is `(rdo_id, do_number)`, not `do_number` alone.

**Sheet name anomaly handling** (25 anomalies across 14 workbooks per Wave 2):
- Strip leading/trailing whitespace
- Handle unclosed parentheses: `"Sheet 5 (DO 123-24"` → extract `"DO 123-24"`
- Handle missing DO prefix: `"Sheet 3 (123-24)"` → infer DO prefix
- Regex extraction: `DO\s*(\d{1,3}[-–]\d{2,4})` with fallback to numeric-only pattern

#### 2.2 Merge Map Construction

Per Wave 2 merged-cell-patterns, 39% of workbooks use data-level merged cells (not just headers). The merge map must be constructed **before** reading any data rows.

```rust
/// O(1) merge resolution map. Built per-sheet before data extraction.
/// Source: Wave 2 merged-cell-patterns — 52K merges across 31 workbooks.
struct MergeMap {
    /// Key: (row, col) of any cell within a merge range.
    /// Value: (top_row, left_col) — the anchor cell containing the actual value.
    cell_to_anchor: HashMap<(u32, u16), (u32, u16)>,
}

impl MergeMap {
    /// Build from Excel library's merge range list.
    fn from_merge_ranges(ranges: &[(u32, u16, u32, u16)]) -> Self {
        let mut map = HashMap::new();
        for &(top_row, left_col, bottom_row, right_col) in ranges {
            for row in top_row..=bottom_row {
                for col in left_col..=right_col {
                    if row != top_row || col != left_col {
                        map.insert((row, col), (top_row, left_col));
                    }
                }
            }
        }
        MergeMap { cell_to_anchor: map }
    }

    /// Resolve a cell to its actual value location.
    fn resolve(&self, row: u32, col: u16) -> (u32, u16) {
        self.cell_to_anchor.get(&(row, col)).copied().unwrap_or((row, col))
    }
}
```

**Merge density considerations**: RDO 32 has 2,533 data merges in current revision, RDO 34 has 2,187. The HashMap approach handles this efficiently — ~31K entries across all current-revision sheets for a typical full pipeline run, consuming ~1.5 MB RAM.

#### 2.3 Column Layout Detection

Per Wave 2 workbook-column-layouts, 6 patterns exist. Headers repeat at every barangay boundary (10-20× per sheet), enabling per-block re-detection.

```rust
/// The 4 semantic columns every workbook normalizes to.
/// Source: Wave 2 workbook-column-layouts — all 6 patterns map to these 4 fields.
struct ColumnMapping {
    street_col: u16,          // "STREET NAME" / "SUBDIVISION" etc. (18 header variants)
    vicinity_col: u16,        // "VICINITY" / "V I C I N I T Y" (letter-spaced in 61% NCR)
    classification_col: u16,  // "CLASSIFICATION" / "CLASSSIFICATION" (triple-S typo)
    zv_col: u16,              // "ZV/SQ.M." / "FINAL" / "2V/SQ.M" (typo)
}

/// Column detection keywords (case-insensitive, space-normalized).
const STREET_KEYWORDS: &[&str] = &["STREET", "SUBDIVISION", "CONDOMINIUM", "NAME"];
const VICINITY_KEYWORDS: &[&str] = &["VICINITY", "LOCATION"];
const CLASS_KEYWORDS: &[&str] = &["CLASSIFICATION", "CLASS"];
const ZV_KEYWORDS: &[&str] = &["ZV", "ZONAL", "VALUE", "SQ.M", "FINAL"];
```

**Detection algorithm**:
1. For each row in the sheet, normalize cell text (collapse spaces, uppercase, strip letter-spacing)
2. Score each cell against keyword lists
3. When a row scores ≥3 of 4 keyword matches → column mapping detected
4. Apply mapping to subsequent rows until next header row detected (barangay boundary)
5. Handle multi-row headers: if row N has "REVISED" and row N+1 has "ZV/SQ.M.", combine before scoring

**Pattern-specific handling**:
| Pattern | Column positions | Workbooks | Special handling |
|---------|-----------------|-----------|-----------------|
| A (standard) | 0,1,2,3 | 25/31 (81%) | None — direct 4-col mapping |
| B (split vicinity) | 0,1,2,3,4 | RDO 38 | Vicinity spans 2 columns; concatenate cols 1+2 |
| C (offset gap) | 0,1,3,4 | RDO 39 | Empty col 2; skip in mapping |
| D (comparison) | 0,1,2,3 + prev cols | RDO 30 | 10-col layout with prev/curr ZV; take "CURRENT" ZV column |
| E (wide-gap merged) | 0,3,5,6 | RDO 33, 81 | Horizontal merges: street merged cols 0-2, vicinity cols 3-4 |
| F (gap-at-2-3) | 0,1,4,5 | RDO 42 | Empty cols 2-3; "FINAL" replaces "ZV" in header |

#### 2.4 Barangay Block Detection

Data within each sheet is organized into barangay blocks. Each block starts with a barangay name header (typically in a merged cell spanning all columns, or in bold/larger font in the first data column).

```rust
/// Barangay block boundary detection.
struct BarangayBlock {
    barangay_name: String,       // Raw name from header row
    start_row: u32,              // First data row after header
    end_row: u32,                // Last data row before next block
    column_mapping: ColumnMapping, // May differ from previous block
    footnote_legend: Option<FootnoteLegend>, // Per-block legend if present
}
```

**Detection heuristics** (ordered by reliability):
1. Full-row horizontal merge (cols 0-N, 1 row) → barangay header
2. Cell value matches known barangay name from PSGC database (~42K entries)
3. Cell in bold with no classification/ZV data in same row
4. Column headers re-appear (indicating new block with repeated headers)

#### 2.5 Data Row Extraction

For each barangay block, extract raw records:

```rust
/// Raw parsed record — before normalization.
struct RawRecord {
    rdo_id: u8,
    do_number: String,
    sheet_index: usize,
    row_number: u32,
    barangay_raw: String,
    street_raw: String,              // May be empty (continuation row / merged cell)
    vicinity_raw: String,            // May be empty (same)
    classification_raw: String,      // May contain asterisks, revision numbers
    zv_raw: String,                  // May be numeric, text, or formula result
    municipalities_covered: Vec<String>, // From NOTICE table
    effectivity_date: NaiveDate,
    is_current_revision: bool,
}
```

**Continuation row handling**: When `street_raw` is empty and the cell is NOT within a merge range, the street inherits from the previous non-empty row in the same barangay block. This is the unmerged equivalent of vertical merges — both produce identical normalized output (Wave 2 merged-cell-patterns).

**ZV extraction**:
- Numeric cell → direct conversion to centavos (multiply by 100, round)
- Text cell → regex extraction: `(\d[\d,]*\.?\d*)` → parse as float → centavos
- Formula cell → read cached result (not formula text)
- Non-integer ZVs exist (Wave 1 bir-workbook-provincial-samples noted Cebu has non-integer ZVs)
- Zero or empty → flag for validation (may be legitimate for DA/watershed or may be parsing error)

**Condo block handling** (per Wave 2 condo-table-structures):
- Detect condo section markers: "CONDOMINIUMS", "LIST OF CONDOMINIUMS", etc.
- Within condo section: building name in street column, tower/floor in vicinity column
- Parking slot entries: "PARKING SLOT" as explicit text, or PS classification code
- Track condo vs. land context for downstream classification resolution

---

### Stage 3: Normalize

**Purpose**: Transform raw records into the canonical schema consumed by the Rust engine. Every normalization rule traces to Wave 2 findings.

#### 3.1 Classification Code Normalization

Source: Wave 2 classification-code-usage — 62 unique codes, 6 non-standard, 2,739+ footnote-embedded.

```rust
/// Classification normalization pipeline.
/// Input: raw classification string from Excel cell.
/// Output: ClassCode enum variant + footnote metadata.
fn normalize_classification(raw: &str) -> (ClassCode, FootnoteMarker) {
    // Step 1: Count and strip asterisks (both prefix and suffix)
    let (stripped, asterisk_count, position) = strip_asterisks(raw);
    // "CR***" → ("CR", 3, Suffix)
    // "*RR"  → ("RR", 1, Prefix)

    // Step 2: Strip embedded revision numbers (Cebu RDO 83: "A50 23*")
    let stripped = strip_revision_numbers(&stripped);
    // "A50 23" → "A50"

    // Step 3: Collapse whitespace and uppercase
    let normalized = stripped.split_whitespace().collect::<Vec<_>>().join(" ").to_uppercase();
    // "a 1" → "A1", "R R" → "RR" (letter-spaced)

    // Step 4: Split slash-delimited dual codes
    // "A41/A49" → ["A41", "A49"] → emit 2 records
    // (Only 1 instance found in 31 workbooks, but handle for correctness)

    // Step 5: Map non-standard codes to Annex B equivalents
    let code = match normalized.as_str() {
        "WC" => ClassCode::CR,   // Water-Commercial → Commercial
        "AR" => ClassCode::A,    // Agricultural-Residential → Agricultural
        "PC" => ClassCode::PS,   // Parking Commercial → Parking Slot
        "PH" => ClassCode::RC,   // Penthouse → Residential Condo (value computed separately)
        "R"  => ClassCode::RR,   // Residential shorthand
        "A0" => ClassCode::A50,  // Agricultural catch-all variant
        other => ClassCode::from_str(other)?, // Standard lookup
    };

    let footnote = FootnoteMarker { count: asterisk_count, position };
    (code, footnote)
}
```

#### 3.2 Address/Vicinity Normalization

Source: Wave 2 address-vicinity-patterns — 28,109 records, 14 pattern categories consolidated to 10 semantic types.

```rust
/// Vicinity normalization pipeline.
fn normalize_vicinity(raw: &str, rdo_id: u8) -> NormalizedVicinity {
    // Step 1: Strip leading asterisks (1,209 footnote-prefixed entries)
    let stripped = strip_leading_asterisks(raw);

    // Step 2: Extract parenthetical content
    // "VITO CRUZ (formerly PABLO OCAMPO SR.)" → alias: "PABLO OCAMPO SR."
    let (main, aliases) = extract_parentheticals(&stripped);

    // Step 3: Handle Pasig semicolon barangay qualifiers (RDO 43 specific, 248 entries)
    let (vicinity, barangay_qualifier) = if rdo_id == 43 {
        split_semicolon_barangay(&main)
    } else {
        (main, None)
    };

    // Step 4: Abbreviation expansion
    let expanded = expand_abbreviations(&vicinity);
    // ST. → STREET, AVE. → AVENUE, BLVD. → BOULEVARD, RD. → ROAD,
    // COR. → CORNER, BRGY. → BARANGAY, NAT'L → NATIONAL, PROV'L → PROVINCIAL

    // Step 5: Whitespace normalization
    let normalized = collapse_whitespace(&expanded).to_uppercase();

    // Step 6: Detect vicinity type
    let vicinity_type = classify_vicinity(&normalized, rdo_id);

    NormalizedVicinity {
        original: raw.to_string(),
        normalized,
        vicinity_type,
        aliases,
        barangay_qualifier,
    }
}

/// Vicinity types — determines which matching algorithm applies.
/// Source: Wave 2 address-vicinity-patterns — 10 semantic types.
enum VicinityType {
    CrossStreet {                       // NCR: "AYALA AVE - PASEO DE ROXAS"
        streets: Vec<String>,           // Parsed cross-street names
        separator: Separator,           // SpacedHyphen | TightHyphen | To | Slash
    },
    RoadProximity {                     // Provincial: "ALONG NATIONAL HIGHWAY"
        tier: RoadTier,                 // T1-T7 hierarchy
    },
    FarTier(u8),                        // BGC only (RDO 44): FAR 1-18
    CatchAll,                           // "ALL OTHER STREETS IN [BARANGAY]"
    Corner(Vec<String>),                // "COR. JUPITER ST"
    NearLandmark(String),               // "NEAR MARKET", "BESIDE CHURCH"
    Sitio(String),                      // "SITIO PUGOT" (52 records)
    SingleStreet(String),               // Named street without cross-reference
    Interior,                           // "INTERIOR LOT", "INTERIOR"
    Unclassified(String),               // Fallback for unparseable entries
}

enum RoadTier { National, Provincial, Municipal, Barangay, FiftyMeters, Interior, Watershed }
enum Separator { SpacedHyphen, TightHyphen, To, Slash }
```

**Cross-street separator disambiguation** (Wave 2: 331 three-segment entries):
- Build street dictionary from all Col 0 values in workbook (~13K entries per Wave 3)
- For `A - B - C`: check if `A-B` is a known street name → separator is between `A-B` and `C`
- If ambiguous, emit all interpretations as candidates with reduced confidence

#### 3.3 Street Name Normalization

```rust
fn normalize_street(raw: &str) -> NormalizedStreet {
    // Step 1: Strip footnote markers (asterisks)
    let stripped = strip_asterisks(raw).0;

    // Step 2: Extract section markers
    // "CONDOMINIUMS:****" → section_type: Condo, stripped: "CONDOMINIUMS"
    let (name, section_type) = detect_section_marker(&stripped);

    // Step 3: Abbreviation expansion (same as vicinity)
    let expanded = expand_abbreviations(&name);

    // Step 4: Whitespace/case normalization
    let normalized = collapse_whitespace(&expanded).to_uppercase();

    // Step 5: Build tokens for Jaccard matching
    let tokens: Vec<String> = tokenize(&normalized);

    NormalizedStreet { original: raw.to_string(), normalized, tokens, section_type }
}
```

#### 3.4 Barangay Name Normalization

```rust
fn normalize_barangay(raw: &str) -> String {
    // Step 1: Strip "BARANGAY" / "BRGY." prefix
    // Step 2: Strip parenthetical district/zone qualifiers
    // Step 3: Normalize to PSGC canonical name where possible
    //         (Wave 4 realvaluemaps-approach validated PSGC as canonical key)
    // Step 4: Handle Manila numbered barangays: "897" → "BARANGAY 897"
    // Step 5: Handle multi-word: "SAN ISIDRO" stays as-is
    todo!()
}
```

#### 3.5 Footnote Legend Parsing

Source: Wave 2 footnote-convention-mapping — NO universal schema; meaning is locally scoped.

```rust
/// Per-section footnote legend. Parsed from inline legend blocks.
struct FootnoteLegend {
    rdo_id: u8,
    do_number: String,
    barangay: Option<String>,          // None = sheet-wide legend
    entries: Vec<FootnoteLegendEntry>,
}

struct FootnoteLegendEntry {
    marker: String,                    // "*", "**", "***", "(NEW)", etc.
    meaning: FootnoteMeaning,
}

enum FootnoteMeaning {
    Deleted,             // Street/classification removed from schedule
    NewlyIdentified,     // Added in this revision
    Transferred,         // Moved to different barangay/RDO
    Redefined,           // Vicinity boundaries changed
    Reclassified,        // Classification code changed
    Renamed,             // Street renamed (alias created)
    NonStandard,         // Code not in Annex B
    Corrected,           // Value or data corrected
    NewRoad,             // New road/development
    CalculationRule,     // PS/PH formula (condo-specific)
    Unknown(String),     // Unparseable legend text
}
```

**Legend detection heuristics**:
1. Row with `"*"` in first data column and descriptive text spanning remaining columns
2. Row starting with `"Note:"` (Cebu convention)
3. Row with numbered footnote format `"6*"` (Cebu unique)
4. Legends are NOT inherited across revision sheets — each sheet's legend is independent context

**Critical**: The asterisk meaning reversal (Wave 2 footnote-convention-mapping: `*` = "newly identified" in Pangasinan/Laguna but "deleted" in some NCR RDOs) means the parser MUST parse legends before interpreting footnote markers. If no legend is found for a section, footnote markers are preserved as raw metadata without semantic interpretation.

---

### Stage 4: Validate

**Purpose**: Cross-reference normalized records against invariants and flag anomalies. Validation does NOT reject records — it annotates them with warnings for manual review.

```rust
struct ValidationReport {
    rdo_id: u8,
    total_records: usize,
    warnings: Vec<ValidationWarning>,
    summary: ValidationSummary,
}

struct ValidationWarning {
    record_index: usize,
    row_number: u32,
    severity: Severity,       // Info | Warn | Error
    category: WarningCategory,
    message: String,
}

enum WarningCategory {
    // Classification warnings
    UnknownClassCode,          // Code not in 69-variant enum
    CodeNotInRdoHistory,       // Code absent from RDO's prior revisions
    // Value warnings
    ZvOutlier,                 // ZV outside 2σ of regional distribution for same code
    ZvZero,                    // ZV = 0 (may be legitimate for DA/watershed)
    CrLessThanRr,              // CR < RR in same barangay (unexpected)
    PsGreaterThanRc,           // PS > RC in same block (violates formula)
    // Address warnings
    EmptyVicinity,             // Non-catch-all record with empty vicinity
    EmptyStreet,               // Record with no street name (not within merge/continuation)
    UnparseableVicinity,       // Vicinity couldn't be classified into any type
    DuplicateRecord,           // Same (barangay, street, vicinity, class) in same DO
    // Structural warnings
    NoNoticeSheet,             // Workbook lacks NOTICE sheet (manual sheet mapping needed)
    ColumnDetectionFailed,     // Could not detect all 4 semantic columns in block
    MergeResolutionOrphan,     // Cell outside any known merge range but empty
    // Freshness warnings
    StaleSchedule,             // Current revision >3 years old (mandate = 3-year cycle)
    // RPVARA warnings
    RpvaraTransitioned,        // LGU has approved SMV — flag for dual-source handling
}

enum Severity { Info, Warn, Error }
```

**Validation rules** (ordered by severity):

| Rule | Category | Severity | Source |
|------|----------|----------|--------|
| Unknown classification code | `UnknownClassCode` | Error | Wave 2 classification-code-usage |
| ZV = 0 for non-DA/non-watershed | `ZvZero` | Warn | Wave 2 data-size-estimation |
| ZV > ₱10M/sqm | `ZvOutlier` | Warn | BGC max observed: ~₱900K |
| CR < RR same barangay | `CrLessThanRr` | Warn | Wave 3 classification-resolution-logic |
| PS > 70% of parent RC/CC | `PsGreaterThanRc` | Warn | Wave 2 condo-table-structures |
| Vicinity empty, not catch-all | `EmptyVicinity` | Info | Wave 2 address-vicinity-patterns |
| Schedule > 3 years old | `StaleSchedule` | Info | Wave 1 cta-zonal-rulings (38% outdated per DOF 2024) |
| Duplicate (brgy, street, vicinity, class) | `DuplicateRecord` | Warn | Data quality |

**Outlier detection**: Compute per-RDO, per-classification median and σ. Flag records > 2σ from median. Known exception: BGC (RDO 44) legitimately has ZVs 2-3× higher than rest of Taguig — use per-barangay distribution within BGC.

---

### Stage 5: Index & Pack

**Purpose**: Build the binary bundle consumed by the WASM engine. This stage transforms normalized records into the exact data structures defined in Wave 5 rust-engine-design.

#### 5.1 String Interning

```rust
/// Build the StringTable from all unique strings across all records.
/// Source: Wave 2 data-size-estimation — ~83K unique strings, ~1.46 MB.
struct StringTableBuilder {
    strings: Vec<String>,                    // Canonical strings
    index: HashMap<String, u32>,             // Dedup lookup
    normalized_index: HashMap<String, Vec<u32>>, // Normalized → all originals
}

impl StringTableBuilder {
    fn intern(&mut self, s: &str) -> u32 {
        if let Some(&idx) = self.index.get(s) {
            return idx;
        }
        let idx = self.strings.len() as u32;
        self.index.insert(s.to_string(), idx);
        // Also index normalized form for fuzzy lookup
        let normalized = normalize_for_search(s);
        self.normalized_index.entry(normalized).or_default().push(idx);
        self.strings.push(s.to_string());
        idx
    }
}
```

#### 5.2 Record Packing

Convert normalized records to 20-byte `PackedRecord` format (per Wave 5 rust-engine-design):

```rust
fn pack_record(
    record: &NormalizedRecord,
    strings: &StringTableBuilder,
    municipality_map: &HashMap<String, u16>,
    barangay_map: &HashMap<String, u16>,
) -> PackedRecord {
    PackedRecord {
        rdo_id: record.rdo_id,
        municipality: municipality_map[&record.municipality],
        barangay: barangay_map[&record.barangay],
        street_idx: strings.index[&record.street_normalized],
        vicinity_idx: strings.index[&record.vicinity_normalized],
        classification: record.class_code as u8,
        zv_centavos: record.zv_centavos,
        footnote: record.footnote_count,
    }
}
```

**Sort order**: Records sorted by `(rdo_id, municipality, barangay, street_idx)` for locality in the LocationIndex binary search.

#### 5.3 Index Construction

Build all indexes defined in rust-engine-design:

1. **LocationIndex**: RDO → Municipality → Barangay → record range (from sorted order)
2. **StreetIndex**: Per-barangay pre-tokenized street entries for 5-tier matching cascade
3. **AvailableCodesIndex**: Per-RDO `u128` ClassCodeSet bitsets
4. **DOTable**: Per-RDO Department Order metadata (DO#, effectivity date, municipality coverage)
5. **JurisdictionMap**: Barangay → RDO mapping with temporal versioning (Wave 3 rdo-jurisdiction-mapping: ~42K entries)
6. **LguRegimeRegistry**: Per-LGU RPVARA regime status (Wave 3 rpvara-dual-source-resolution: ~1,715 entries)

#### 5.4 Binary Serialization

Per Wave 5 rust-engine-design, custom v1 format with 7 sections:

```
┌──────────────────────────────────────────────┐
│ Section 0: Header (16 bytes)                 │
│   magic: [u8; 4] = b"ZVBF"                  │
│   version: u16 = 1                           │
│   flags: u16                                 │
│   record_count: u32                          │
│   string_count: u32                          │
├──────────────────────────────────────────────┤
│ Section 1: StringTable                       │
│   For each string: length (u16) + UTF-8 data │
├──────────────────────────────────────────────┤
│ Section 2: DOTable                           │
│   Per-RDO DO metadata                        │
├──────────────────────────────────────────────┤
│ Section 3: Records (sorted)                  │
│   N × PackedRecord (20 bytes each)           │
├──────────────────────────────────────────────┤
│ Section 4: LocationIndex                     │
│   RDO ranges + Municipality ranges + Bgy     │
├──────────────────────────────────────────────┤
│ Section 5: AvailableCodesIndex               │
│   Per-RDO u128 bitsets                       │
├──────────────────────────────────────────────┤
│ Section 6: JurisdictionMap + RegimeRegistry  │
│   Barangay→RDO + LGU regime status           │
└──────────────────────────────────────────────┘
```

**Output artifacts**:
- `zv-full-{content_hash}.bin` — full dataset (~17.7 MB raw, ~5.0 MB brotli)
- `zv-ncr-{content_hash}.bin` — NCR-only for Phase 1 loading (~2.1 MB raw, ~585 KB brotli)
- `zv-rr{N}-{content_hash}.bin` — per-Revenue Region chunks (19 × ~230 KB brotli avg)
- `manifest.json` — content hashes, sizes, build timestamp, RDO versions

**Content-hash versioning**: SHA-256 of uncompressed bundle bytes. Same inputs → identical hash. Enables immutable CDN caching with infinite TTL (per Wave 5 wasm-vs-hybrid-tradeoff).

#### 5.5 Revenue Region Chunking

Per Wave 5 wasm-vs-hybrid-tradeoff, tiered loading strategy:

```rust
/// Chunk the full dataset into Revenue Region segments.
/// Phase 1: NCR chunk (RR6 + RR7A + RR7B + RR8A + RR8B) — covers ~80% of tax transactions.
/// Phase 2: 19 provincial RR chunks loaded on-demand or background-streamed.
struct ChunkManifest {
    ncr_chunk: ChunkEntry,
    provincial_chunks: Vec<ChunkEntry>,  // 19 entries
    smv_chunks: Vec<SmvChunkEntry>,      // RPVARA: per-LGU when available
}

struct ChunkEntry {
    revenue_region: String,
    content_hash: String,
    raw_size: u64,
    brotli_size: u64,
    record_count: u32,
    rdo_ids: Vec<u8>,
}
```

---

### Stage 6: Publish

**Purpose**: Deploy binary bundles to CDN with atomic updates.

**Deployment strategy**:
1. Upload all new chunk files to CDN (content-hash filenames → never overwrite existing)
2. Upload new `manifest.json` pointing to latest chunks
3. Service Worker on client checks manifest periodically → downloads only changed chunks
4. Old chunk files remain accessible for clients with cached manifests (grace period: 30 days)

**CDN requirements** (per Wave 5 wasm-vs-hybrid-tradeoff: ~$20/mo):
- Brotli pre-compression support (all bundles uploaded pre-compressed)
- Content-hash-based filenames with immutable cache headers (`Cache-Control: public, max-age=31536000, immutable`)
- Manifest file with short TTL (`Cache-Control: public, max-age=3600`)
- CORS headers for WASM/Web Worker fetch

---

## 2. RPVARA Data Source Integration

Per Wave 3 rpvara-dual-source-resolution, the pipeline must support BLGF Schedule of Market Values (SMV) as a second data source alongside BIR zonal values.

### 2.1 Data Source Abstraction

```rust
/// Trait for parsing any valuation data source into normalized records.
/// BIR Excel workbooks and future BLGF SMV documents implement this.
trait SourceParser {
    fn parse(&self, input: &[u8]) -> Result<Vec<NormalizedRecord>, ParseError>;
    fn source_type(&self) -> DataSourceType;
}

enum DataSourceType {
    BirZonalValue,    // Current: 124 RDO Excel workbooks
    BlgfSmv,          // Future: BLGF-approved Schedule of Market Values
    Rpis,             // Future: Real Property Information System (under procurement)
}

/// BIR Excel parser — implements all 6 column patterns, merge handling, etc.
struct BirExcelParser { /* ... */ }
impl SourceParser for BirExcelParser { /* Stages 2-3 above */ }

/// BLGF SMV parser — format unknown as of March 2026.
/// Placeholder: will be implemented when first BLGF-approved SMV is published.
struct BlgfSmvParser { /* ... */ }
impl SourceParser for BlgfSmvParser {
    fn parse(&self, _input: &[u8]) -> Result<Vec<NormalizedRecord>, ParseError> {
        // Wave 3 rpvara-dual-source-resolution:
        // Zero BLGF-approved SMVs exist as of March 2026.
        // Classification taxonomy is structurally incompatible (R1-R12 vs RR/CR).
        // Parser will be implemented when first SMV format is observed.
        Err(ParseError::FormatNotYetSupported("BLGF SMV format TBD"))
    }
    fn source_type(&self) -> DataSourceType { DataSourceType::BlgfSmv }
}
```

### 2.2 Dual-Source Bundle Strategy

When BLGF SMVs begin appearing (projected: H2 2026 for 5-15 LGUs per Wave 3):

1. SMV records stored in separate chunk files: `zv-smv-{lgu_psgc}-{hash}.bin`
2. Only loaded for transitioned LGUs (LguRegimeRegistry determines which)
3. Worst-case dual-source: ~9.2 MB brotli (exceeds 5 MB mobile, fits 10 MB desktop) — per Wave 5 wasm-vs-hybrid-tradeoff, this scenario is unlikely to occur simultaneously across all LGUs
4. Bundle format Section 6 includes regime registry updates

### 2.3 LGU Regime Registry Updates

```rust
/// Monthly update: check BLGF announcements for newly approved SMVs.
/// Source: Wave 3 rpvara-dual-source-resolution — ~37% historical compliance rate
/// predicts most LGUs will miss July 2026 deadline.
fn update_regime_registry() -> LguRegimeRegistry {
    // 1. Scrape BLGF website for SMV approval announcements
    // 2. Cross-reference against existing registry
    // 3. Update status: NotYetApproved → InPreparation → Approved(date)
    // 4. When Approved: trigger SMV parser + chunk generation for that LGU
    todo!()
}
```

---

## 3. Update Monitoring & Scheduling

### 3.1 BIR Workbook Change Detection

BIR publishes new Department Orders irregularly. Monitoring strategy:

```
┌─────────────────────────────────────────────────────┐
│                    CRON SCHEDULE                     │
│                                                     │
│  Weekly:  Check bir.gov.ph/zonal-values for         │
│           HTTP header changes (ETag/Last-Modified)   │
│                                                     │
│  Monthly: Full re-download of all 124 workbooks      │
│           + content-hash comparison                  │
│                                                     │
│  On-demand: Manual trigger when BIR news announces  │
│             new Department Orders                    │
└─────────────────────────────────────────────────────┘
```

**Weekly check** (~2 minutes):
- HEAD request to each of 124 workbook URLs
- Compare ETag/Last-Modified against stored values
- If any changed → trigger full pipeline for that RDO only
- Log results to `raw/monitoring/check-{date}.json`

**Monthly full rebuild** (~30 minutes):
- Re-download all 124 workbooks regardless of headers
- Content-hash comparison (SHA-256) catches silent updates where headers don't change
- Full pipeline: parse → normalize → validate → pack → publish
- Validation report diff against previous month

### 3.2 BIR News Monitoring

BIR announces new RMCs and Department Orders on `bir.gov.ph/bir-news`. Supplementary monitoring:
- Weekly scrape of BIR news page for keywords: "zonal value", "Department Order", "schedule of values"
- Alert on match → manual review → on-demand pipeline trigger if relevant

### 3.3 Pipeline Run Manifest

```rust
/// Tracks the state and outcome of each pipeline run.
struct PipelineRun {
    run_id: String,                     // UUID
    started_at: DateTime<Utc>,
    completed_at: Option<DateTime<Utc>>,
    trigger: PipelineTrigger,
    rdos_processed: Vec<RdoPipelineResult>,
    bundles_produced: Vec<BundleArtifact>,
    validation_summary: ValidationSummary,
}

enum PipelineTrigger {
    WeeklyCheck,
    MonthlyRebuild,
    OnDemand { reason: String },
    RdoUpdate { rdo_ids: Vec<u8> },
}

struct RdoPipelineResult {
    rdo_id: u8,
    status: RdoStatus,
    records_parsed: usize,
    warnings: usize,
    errors: usize,
    content_hash: String,
}

enum RdoStatus { Unchanged, Updated, New, Failed(String), PdfSkipped }
```

---

## 4. Implementation Technology

### 4.1 Language: Rust

The pipeline is implemented in Rust (same language as the engine) for three reasons:
1. **Shared types**: `PackedRecord`, `ClassCode`, `StringTable`, etc. are defined once and used in both pipeline and engine — no serialization boundary between build and runtime
2. **Correctness**: The normalization rules (classification stripping, vicinity parsing) are complex enough that type safety matters
3. **Performance**: Parsing 124 Excel workbooks with 690K+ records should complete in <5 minutes on a single CI machine

### 4.2 Excel Parsing Library

**`calamine`** (Rust): The de facto Rust Excel parser. Supports both .xls (BIFF8) and .xlsx (OOXML). Provides merge range information. Handles formula result caching.

Limitations to work around:
- Calamine returns merged cells as empty in non-anchor positions → MergeMap resolves this
- Date cells may return as floats (Excel serial dates) → explicit date format detection needed
- No style information (bold/font) → barangay header detection uses heuristics, not formatting

### 4.3 CI/CD Pipeline

```yaml
# .github/workflows/zv-pipeline.yml
name: Zonal Value Pipeline
on:
  schedule:
    - cron: '0 2 * * 1'    # Weekly Monday 2AM UTC (10AM PHT)
    - cron: '0 2 1 * *'    # Monthly 1st at 2AM UTC
  workflow_dispatch:          # Manual trigger
    inputs:
      rdo_ids:
        description: 'Comma-separated RDO IDs (empty = all)'
        required: false

jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - name: Run pipeline
        run: cargo run --release -p zv-pipeline -- --mode ${{ github.event.schedule && 'full' || 'targeted' }}
      - name: Upload bundles
        # Upload to CDN (R2/S3/Cloudflare)
      - name: Commit manifest
        # Commit updated manifest.json to repo
```

**Estimated CI runtime**:
- Download 124 workbooks: ~5 minutes (rate-limited)
- Parse + normalize: ~3 minutes (I/O bound on Excel parsing)
- Validate: ~30 seconds
- Pack + compress: ~1 minute
- Total: ~10 minutes for full rebuild

### 4.4 Crate Structure

```
zv-pipeline/
├── Cargo.toml
├── src/
│   ├── main.rs              # CLI entry point
│   ├── acquire.rs           # Stage 1: Download workbooks
│   ├── parse/
│   │   ├── mod.rs
│   │   ├── notice.rs        # NOTICE sheet parser
│   │   ├── merge_map.rs     # Merge resolution
│   │   ├── columns.rs       # Column layout detection (6 patterns)
│   │   ├── barangay.rs      # Barangay block detection
│   │   ├── rows.rs          # Data row extraction
│   │   └── condo.rs         # Condo section handling
│   ├── normalize/
│   │   ├── mod.rs
│   │   ├── classification.rs # Code normalization pipeline
│   │   ├── vicinity.rs      # Address/vicinity normalization
│   │   ├── street.rs        # Street name normalization
│   │   ├── barangay.rs      # Barangay name normalization
│   │   └── footnote.rs      # Footnote legend parsing
│   ├── validate.rs          # Stage 4: Validation rules
│   ├── pack/
│   │   ├── mod.rs
│   │   ├── strings.rs       # String table builder
│   │   ├── records.rs       # Record packing + sorting
│   │   ├── indexes.rs       # Index construction
│   │   ├── binary.rs        # Binary serialization (v1 format)
│   │   └── chunks.rs        # Revenue Region chunking
│   ├── publish.rs           # Stage 6: CDN deployment
│   ├── monitor.rs           # Change detection + scheduling
│   └── rpvara.rs            # BLGF SMV integration (placeholder)
├── tests/
│   ├── fixtures/            # Sample workbook excerpts for testing
│   ├── parse_tests.rs       # Per-pattern parser tests
│   ├── normalize_tests.rs   # Normalization rule tests
│   └── integration_tests.rs # Full pipeline tests with sample data
```

**Shared crate dependency**: `zv-engine-types` (shared between `zv-pipeline` and `zv-engine`) defines `ClassCode`, `PackedRecord`, `StringIdx`, and other types that must be identical in pipeline and runtime.

---

## 5. Error Handling & Recovery

### 5.1 Partial Failure Strategy

The pipeline processes 124 RDOs independently. A failure in one RDO does not block others.

```rust
enum RdoOutcome {
    Success(RdoPipelineResult),
    PartialSuccess {
        result: RdoPipelineResult,
        sheets_skipped: Vec<(usize, String)>,  // (sheet_index, reason)
    },
    Failed(String),
    Skipped(String),  // PDF, unchanged, etc.
}
```

**Recovery rules**:
- If an RDO fails to download → use previously cached workbook (if available)
- If a sheet within a workbook fails to parse → skip that sheet, parse remaining sheets, log warning
- If column detection fails for a barangay block → skip block, continue to next barangay
- If normalization fails for a record → emit record with `Severity::Error` warning, include in output with zero confidence
- Never: silently drop records. Every input row either becomes a record or appears in the validation report.

### 5.2 Idempotency

Pipeline runs are idempotent: same input workbooks → identical binary output (verified by content hash). This is ensured by:
- Deterministic sort order in record packing
- Deterministic string interning order (alphabetical within each category)
- No timestamps or random IDs in the binary format
- Content hash computed on uncompressed bytes (brotli compression is deterministic for same input + same quality level)

---

## 6. Historical Data Pipeline

Per Wave 5 wasm-vs-hybrid-tradeoff, historical data (~2.97M records, ~18 MB brotli) is served via API only, not bundled in WASM.

**Historical pipeline variant**:
- Same parse + normalize stages, but processes ALL revision sheets (not just current)
- Packs into a server-side database (PostgreSQL with JSONB or SQLite)
- API serves queries by (location, date) → returns applicable ZV as of that date
- Optional: separate CI job on monthly schedule
- Not required for v1 launch — current-revision WASM bundle is the priority

---

## 7. Design Decision Traceability

| # | Decision | Source | Finding |
|---|----------|--------|---------|
| 1 | Merge map built per-sheet before data reading | Wave 2 merged-cell-patterns | 39% of workbooks use data merges; O(1) resolution needed |
| 2 | Column detection per-barangay-block (not per-sheet) | Wave 2 workbook-column-layouts | Headers repeat 10-20× per sheet; column positions can shift |
| 3 | 3-format date parser (serial/ISO/human) | Wave 2 sheet-organization | 86% serial, 9% ISO, 5% human in effectivity dates |
| 4 | Per-section footnote legend parsing | Wave 2 footnote-convention-mapping | Asterisk meaning reverses between regions; legends not inherited |
| 5 | PSGC codes as canonical location identifiers | Wave 4 realvaluemaps-approach | Only standard geographic code system; enables cross-source joins |
| 6 | SourceParser trait for data source abstraction | Wave 3 rpvara-dual-source-resolution | BLGF SMV format unknown; must be pluggable |
| 7 | Content-hash versioning on bundles | Wave 5 wasm-vs-hybrid-tradeoff | Immutable CDN caching; only changed chunks re-downloaded |
| 8 | Revenue Region chunking (NCR first + 19 provincial) | Wave 5 wasm-vs-hybrid-tradeoff | Phase 1 NCR at 585 KB serves ~80% of tax transactions |
| 9 | Shared Rust types between pipeline and engine | Wave 5 rust-engine-design | PackedRecord, ClassCode, StringTable used in both build and runtime |
| 10 | Calamine for Excel parsing | Wave 1 bir-workbook-ncr-samples | 23 .xls + 1 .xlsx; need both BIFF8 and OOXML support with merge info |
| 11 | Weekly + monthly monitoring schedule | Wave 1 cta-zonal-rulings | BIR revises schedules every ~3 years; new DOs are event-driven |
| 12 | Never silently drop records | Wave 1 cta-zonal-rulings | "Existing values remain in force until revised" — every record is legally material |
| 13 | Separate historical pipeline (API, not WASM) | Wave 5 wasm-vs-hybrid-tradeoff | 2.97M records at 18 MB brotli exceeds client-side budget |
| 14 | Independent per-RDO failure isolation | Wave 1 bir-workbook-provincial-samples | Format heterogeneity means some RDOs may fail; others must not be blocked |

---

## 8. Open Questions for Implementation

1. **BIR URL stability**: Are the workbook download URLs stable across BIR website redesigns? The CDN path structure (`bir.gov.ph/zonal-values/...`) should be monitored for URL pattern changes. Consider building a URL registry with fallback search.
2. **BLGF SMV format**: When the first BLGF-approved SMV is published (projected H2 2026), the BlgfSmvParser must be implemented. The format is entirely unknown — could be Excel, PDF, database export, or API. The SourceParser trait isolates this uncertainty.
3. **Incremental bundle updates**: v1 rebuilds the full bundle on any change. Delta updates (adding only new DO records) would reduce CI time and CDN bandwidth. Worth investigating for v2 if update frequency increases under RPVARA.
4. **PSGC integration depth**: Should the pipeline validate barangay names against the PSA PSGC database and auto-correct common spelling variations? This would improve cross-source joining but adds a dependency on PSGC data freshness.
5. **PDF OCR for outlier RDOs**: The ~2-5 estimated PDF-only RDOs represent a coverage gap. OCR (Tesseract + table detection) could recover data, but quality would need validation. Manual transcription may be more practical for v1.

---

## 9. Emergent Findings

No new aspects discovered — all pipeline design elements trace to existing Wave 2-5 findings. The architecture is a direct synthesis of the parsing challenges documented across 8 Wave 2 analyses and the target data structures from Wave 5 rust-engine-design.
