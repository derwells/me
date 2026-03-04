# Zonal Value Lookup Engine — Full Specification

**Version:** 1.0
**Date:** 2026-03-04
**Status:** Complete (assembled from 27 analyses across 6 waves)
**Target:** Forward loop using [fullstack-rust-wasm template](https://github.com/clsandoval/monorepo/tree/main/loops/_templates/fullstack-rust-wasm)

---

## Table of Contents

**Part 1: Computation & Data Spec**
1. [Executive Summary](#1-executive-summary)
2. [Data Landscape](#2-data-landscape)
3. [BIR Workbook Format Variations](#3-bir-workbook-format-variations)
4. [Address Matching & Normalization](#4-address-matching--normalization)
5. [Classification Code System](#5-classification-code-system)
6. [Fallback Hierarchy](#6-fallback-hierarchy)
7. [Condo & Special Property Handling](#7-condo--special-property-handling)
8. [RDO Jurisdiction Mapping](#8-rdo-jurisdiction-mapping)
9. [RPVARA Transition Mechanics](#9-rpvara-transition-mechanics)
10. [Legal Framework & Edge Cases](#10-legal-framework--edge-cases)

**Part 2: App Architecture Spec**
11. [Architecture Overview](#11-architecture-overview)
12. [Rust Engine Design](#12-rust-engine-design)
13. [WASM Bridge & Privacy Model](#13-wasm-bridge--privacy-model)
14. [Data Pipeline](#14-data-pipeline)
15. [Frontend Design](#15-frontend-design)
16. [Public REST API](#16-public-rest-api)
17. [Data Size & Bundling](#17-data-size--bundling)
18. [Competitive Context](#18-competitive-context)
19. [Open Questions](#19-open-questions)
20. [Design Decision Traceability](#20-design-decision-traceability)

---

# PART 1: COMPUTATION & DATA SPEC

---

## 1. Executive Summary

This specification documents a **Zonal Value Lookup Engine** for the Philippine real estate tax system — the highest-leverage data infrastructure component in Philippine real estate taxation (scored 125/125 in the opportunity catalog).

**The problem:** BIR publishes zonal values across 124 Revenue District Offices in heterogeneous Excel workbooks. There is no API, no standardized format, and no address matching. Tax practitioners manually search Excel files with Ctrl+F. Seven existing platforms (Housal, RealValueMaps, ZonalValueFinderPH, REN.PH, LandValuePH, ZonalValue.com, FileDocsPhil) present this data as browseable tables with no resolution intelligence, no legal metadata, and zero readiness for the RPVARA (RA 12001) transition from BIR to BLGF valuation authority.

**The solution:** A Rust + WASM + TypeScript engine that:
- Ingests all 124 BIR Excel workbooks (6 column patterns, 52K+ merged cells, 5,418+ footnote annotations)
- Resolves property addresses via an 8-phase matching pipeline with 5-tier street matching cascade
- Implements a 7-level fallback hierarchy grounded in DOF Department Order rules and CTA jurisprudence
- Resolves 63+ classification codes across 7 resolution paths
- Detects 3 RPVARA regimes per jurisdiction with pluggable dual-source architecture
- Runs entirely client-side via WASM (~4.8 MB brotli bundle) — property details never leave the browser
- Exposes a public REST API for downstream integrators

**Key numbers:**
- ~690,000 current-revision records across 124 RDOs
- ~2.97M total records including all historical revisions
- 63 BIR classification codes + 6 non-standard regional codes
- 28,109 vicinity records with 13,080 unique values
- 52,327 merged cells across 31 sampled workbooks
- 42,000+ barangays in jurisdiction mapping
- 4.8 MB brotli compressed = full current dataset + engine in browser

---

## 2. Data Landscape

### 2.1 Dataset Scale

| Metric | Value | Source |
|--------|-------|--------|
| Total RDOs | 124 (geographic, excluding LTS 115-127) | BIR RDO directory |
| Revenue Regions | 19 (post-2019 split: RR7→7A/7B, RR8→8A/8B) | RAO 4-2019 |
| Current-revision records | ~690,000 (range 550K-850K) | 31-workbook sample extrapolated |
| Historical records (all revisions) | ~2.97M (4.3x multiplier) | 5-workbook growth analysis |
| Unique street names | ~23,800 | Extrapolated from 6,789 in 31-workbook sample |
| Unique vicinity values | ~16,100 | Extrapolated from 4,872 in sample |
| Barangays (national) | ~42,000 | PSA PSGC |
| Cities/municipalities | ~1,913 | PSA PSGC |

### 2.2 Workbook Acquisition

BIR publishes workbooks at `bir.gov.ph/zonal-values`. Key characteristics:
- **Format:** 23 .xls (BIFF8) + 1 .xlsx (OOXML) in 24-workbook NCR sample; 5 .xls + 2 .xlsx in 7-workbook provincial sample. ~2-5 RDOs publish image-only PDFs (not parseable).
- **Size:** Average 1.47 MB per workbook; estimated 182 MB total for all 124.
- **Update frequency:** Quarterly to annually per RDO. 38% of schedules are outdated (>3 years since last revision).
- **Rate limiting:** HTTP conditional GET with 2-second rate limiting between requests.
- **Content-hash change detection:** SHA-256 hash per workbook for pipeline idempotency.

### 2.3 Zonal Value Ranges

| Range | Context |
|-------|---------|
| ₱1/sqm | Minimum (remote agricultural) |
| ₱350/sqm | Typical irrigated riceland (Pangasinan) |
| ₱4,000-12,000/sqm | Provincial road-proximity tiers |
| ₱40,000-100,000/sqm | NCR residential (non-CBD) |
| ₱200,000-395,000/sqm | Makati CBD / BGC condos |
| ₱2,160,000/sqm | Maximum observed (Ayala Avenue commercial) |

All values fit in u32 (max 4.29B). 4.6% of records have non-integer values (concentrated in Cebu).

---

## 3. BIR Workbook Format Variations

### 3.1 Column Layout Patterns (6 patterns)

All workbooks normalize to 4 semantic columns: **Street, Vicinity, Classification, ZV/sqm.**

| Pattern | Physical Cols | Description | Workbooks | Coverage |
|---------|-------------|-------------|-----------|----------|
| **A** | 0,1,2,3 | Standard 4-column | 25/31 | 81% |
| **B** | 0,1,2,3,4 | Split vicinity (two cross-street columns) | RDO 38 | 3% |
| **C** | 0,_,2,3,4 | Offset gap (col 1 empty) | RDO 39 | 3% |
| **D** | 0,_,_,_,4,_,6,7,8 | Side-by-side comparison (prev + curr ZV) | RDO 30 | 3% |
| **E** | 0-2(merged),3-4(merged),5,6 | Wide-gap merged columns | RDO 33, 81 | 6% |
| **F** | 0,1,_,_,4,5 | Gap at columns 2-3 | RDO 42 | 3% |

**Structural invariants** (true across all 31 sampled workbooks):
1. Street is always column 0 (leftmost)
2. ZV is always the rightmost data column
3. Classification always immediately precedes ZV
4. Headers repeat at every barangay block boundary (10-20x per sheet)
5. Headers can span 2 rows (revision ordinal on row N, "ZV/SQ.M." on row N+1)
6. Continuation rows (empty col 0, classification+ZV filled) encode multi-classification streets

**Column detection algorithm:**
```
For each row in sheet:
  1. Normalize text: collapse spaces, remove hyphens, strip newlines, uppercase
  2. Find STREET keyword in cell → street_col
  3. Find VICINITY keyword → vicinity_col
  4. Find CLASS or FICATION keyword → class_col
  5. Find ZV or SQ or REVISION or REV or FINAL → zv_col
  6. If ≥3 keywords found in same row → valid header row
  7. Combine with next row if ZV split across two rows
```

### 3.2 Header Text Variations

| Column | Variants Found | Key Normalization |
|--------|---------------|-------------------|
| Street | 18 distinct texts | Match on "STREET" keyword |
| Vicinity | "VICINITY" (32%), "V I C I N I T Y" (61%), unlabeled (3%) | Collapse spaces → "VICINITY" |
| Classification | 7 variants incl. "CLASSSIFICATION" (triple-S typo) | Match on "CLASS" prefix |
| ZV | 12+ variants incl. "2V/SQ.M" (Z→2 typo, RDO 113A) | Match on "ZV", "SQ", "REV" |

### 3.3 Merged Cell Patterns (6 categories)

52,327 total merges across 31 workbooks (31,237 in current-revision sheets).

| Category | % | Count | Description |
|----------|---|-------|-------------|
| VERT | 72% | 22,484 | Vertical: street/vicinity spanning multiple classification rows |
| FULL_H | 11.2% | 3,489 | Full horizontal: barangay headers spanning all columns |
| TRIPLE_H | 9.0% | 2,803 | 3-column horizontal merges |
| PAIR_H | 4.9% | 1,516 | 2-column horizontal merges |
| BLOCK_H | 2.3% | 709 | Wide horizontal blocks |
| BLOCK | 0.8% | 236 | Multi-row, multi-column blocks (condo building names) |

**Critical distinction:** Header repetition merges (~60% of vertical merges, safe to skip) vs. data row merges (~40%, must resolve). 12/31 workbooks use data vertical merges; RDO 32 has 2,533 data merges.

**Extreme cases:** 17-row merge (RDO 53B, "EAST SERVICE ROAD" with 17 classifications), 14-row agricultural merge (RDO 4).

**Parser requirement:** Build a `MergeMap` (HashMap) before reading data for O(1) cell resolution. Both merged-cell and continuation-row workbooks must produce identical normalized output.

### 3.4 Sheet Organization

294 total sheets across 31 workbooks: 31 NOTICE + 261 revision data + 2 empty artifacts.

**Universal pattern:**
1. NOTICE sheet at index 0 (contains DO → sheet → municipality → effectivity date mapping)
2. Revision data sheets in descending order (Sheet N = newest revision)
3. No condo/land separation — all data types coexist in every sheet
4. No hidden sheets

**NOTICE sheet is authoritative:** Different municipalities within the same RDO can be on different current revisions. The NOTICE table determines the correct sheet per municipality.

**Effectivity date formats:** Excel serial (86%), ISO datetime (9%), human date (5%). Three-format cascade parser required.

**Sheet naming anomalies:** 25 across 14 workbooks (7 unclosed parens, 12 whitespace, 4 missing DO prefix, 1 duplicate DO number).

**Unique key:** (RDO, DO number), NOT DO number alone — the same DO number can appear in different RDOs or even within the same workbook (RDO 57).

### 3.5 Footnote Conventions

5,418+ annotated cells across 16 workbooks. **No universal footnote schema** — marker meaning is locally scoped per RDO, per revision sheet, sometimes per barangay section.

**Critical reversal:** `*` = "newly identified" in Pangasinan/Laguna, but "deleted" in some NCR RDOs.

| Characteristic | Value |
|---------------|-------|
| Asterisk range | 1–11 asterisks documented |
| Position | Both prefix (`*RR`) and suffix (`CR*`) |
| Provincial density | 15x more than NCR (median 900 vs 60 cells/workbook) |
| Provincial targets | Classification codes (2,687 instances) |
| NCR targets | Street names (941 instances) |
| Legend inheritance | NOT inherited across revision sheets |
| Semantic categories | 10: deleted, newly identified, transferred, redefined, reclassified, renamed, non-standard, corrected, new road, calculation rule |

**Condo computation rules embedded as footnotes:** PS=60-70% of parent, PH=110-120% of CC/RC, ground floor +20%, business use +20%.

**Special patterns:** `(NEW)` vicinity marker (RDO 57), embedded revision numbers in classification cells ("A50 23*" in RDO 83), zero-footnote workbooks (RDO 30).

**Parser strategy:** Strip markers before matching, preserve as u16 metadata per record (~110 KB for 8% annotation rate). Parse legends per-section with heuristic detection. Mandatory legend-first processing to handle asterisk meaning reversal.

---

## 4. Address Matching & Normalization

### 4.1 The Core Problem

Address matching is the hardest step (Complexity: EXTREME) in the resolution pipeline. The engine must resolve a free-text property address into a specific row in one of 124 heterogeneous workbooks where:
- 28,109 vicinity records exist with 13,080 unique values
- Two fundamentally different address models coexist (NCR cross-street vs. provincial road-proximity)
- No geocoding standard exists — BIR uses text-based matching
- ONETT processors themselves do manual Ctrl+F lookup

### 4.2 Dual-Mode Address Models

**NCR Cross-Street Boundary Model** (40.7% of records, 11,438 entries):
- Format: `STREET_A - STREET_B` (boundary defined by two cross-streets)
- Separator variants: spaced hyphen (3,725), tight hyphen (2,443), "TO" (419)
- 331 entries with 3+ segments create separator ambiguity requiring a ~13K-entry street name dictionary

**Provincial Road-Proximity Hierarchy** (7 tiers with descending ZV):

| Tier | Description | Median ZV |
|------|-------------|-----------|
| T1 | Along National Highway | ₱12,000/sqm |
| T2 | Along Provincial Road | ₱7,000/sqm |
| T3 | Along Municipal Road | ₱6,000/sqm |
| T4 | Along Barangay Road | ₱4,000/sqm |
| T5 | 50 Meters Inward | ₱2,900/sqm |
| T6 | Interior Lots | ₱3,500/sqm |
| T7 | Watershed/Timberland | ₱500/sqm |

### 4.3 Eight-Phase Matching Pipeline

```
Phase 1: Input Normalization
  → Uppercase, strip diacritics, expand abbreviations (ST.→STREET, AVE.→AVENUE, BRGY.→BARANGAY)
  → Collapse whitespace, remove punctuation except hyphens

Phase 2: Address Mode Detection
  → If input contains cross-street separators (-, TO, AND) → NCR_CROSS_STREET
  → If input matches road tier keywords → PROVINCIAL_ROAD_PROXIMITY
  → If input is building name → CONDO_PATH
  → If input matches FAR tier pattern → BGC_FAR (RDO 44 only)
  → Default → GENERAL_MATCH

Phase 3: Jurisdiction Resolution
  → Municipality → RDO(s) via jurisdiction map
  → Barangay → narrow to specific RDO
  → 4 intra-barangay splits require street-level disambiguation (hardcoded table)

Phase 4: Street Matching (5-tier cascade)
  1. Exact normalized match (case-insensitive, whitespace-collapsed)
  2. Alias resolution (211+ BIR "formerly..." annotations + Wikipedia renamed streets)
  3. Substring containment (input is substring of record OR vice versa)
  4. Token-set Jaccard similarity (threshold 0.70)
  5. Fuzzy Jaro-Winkler (threshold 0.90 — high to prevent SAN ANTONIO/SAN AGUSTIN false positives)

Phase 5: Vicinity Matching
  → NCR mode: Parse cross-street boundaries, check if query address falls within segment
  → Provincial mode: Match road tier keyword → resolve to appropriate tier level
  → Catch-all: "ALL OTHER STREETS IN [BARANGAY]" entries (185 across 31 workbooks)

Phase 6: Classification Resolution
  → See Section 5 (7 resolution paths)

Phase 7: Fallback Hierarchy
  → See Section 6 (7-level decision tree)

Phase 8: Confidence Scoring
  → 5-component model: address_match × classification × fallback_penalty × data_freshness × regime_penalty
  → 0.0–1.0 scale, mapped to 5 UI tiers (HIGH ≥0.85, MEDIUM 0.65-0.84, LOW 0.50-0.64, VERY LOW <0.50, NO MATCH 0.0)
```

### 4.4 Special Address Cases

| Case | Description | Handling |
|------|-------------|---------|
| **BGC FAR tiers** | 544 records in RDO 44 use Floor Area Ratio (1-18) instead of streets | Dedicated FAR matching path; requires user to provide FAR value |
| **Pasig semicolons** | 248 entries in RDO 43 use semicolon-delimited barangay qualifiers in vicinity column | Parse semicolons as barangay scope qualifiers |
| **Manila zones** | ~897 numbered barangays grouped into zones → districts | Barangay number → zone → district mapping |
| **Cebu storey-based** | Condo catch-all: "≤7 storeys" vs "≥8 storeys" with 44-78% premium | Requires building height input for condo resolution |
| **Separator ambiguity** | 331 cross-streets with 3+ segments (e.g., "A - B - C") | Street name dictionary (~13K entries from col 0) to identify valid street names |
| **Former names** | 211 BIR annotations: "VITO CRUZ (formerly PABLO OCAMPO SR.)" | Alias table for bidirectional resolution |

### 4.5 Performance Requirements

| Operation | Target | Method |
|-----------|--------|--------|
| Exact match | <1 ms | LocationIndex O(1) scoping |
| Fuzzy match (5-tier cascade) | <10 ms | Per-barangay ~160 records |
| Full fallback (7-level tree) | <50 ms | Adjacent barangay scan |
| Index size | ~17.8 MB raw / ~5.2 MB brotli | Within WASM budget |

---

## 5. Classification Code System

### 5.1 BIR Annex B Codes (RMO 31-2019)

**13 primary codes:**

| Code | Name | NCR Frequency | Provincial Frequency |
|------|------|--------------|---------------------|
| RR | Residential Regular | 38.2% | Present |
| CR | Commercial Regular | 24.5% (only universal code: 31/31 RDOs) | Present |
| RC | Residential Condominium | 5.0% | Rare |
| CC | Commercial Condominium | Present | Rare |
| I | Industrial | Present | Present |
| X | Institutional/Special | Present | Present |
| GL | Government Lot | Present | Rare |
| GP | Government Property | Present | Rare |
| CL | Communal Lot | Present | Rare |
| APD | Approved Project for Development | Present | Rare |
| PS | Parking Slot | Present | Rare |
| A | Agricultural (parent) | Absent in pure NCR | Present |
| DA | Drying Area | Absent in NCR | Present |

**50 agricultural sub-codes (A1-A50):** A1=Riceland Irrigated, A2=Riceland Unirrigated, ..., A50=Open Grassland. 43/50 observed in sample.

**NCR/Provincial divide:** NCR is a 7-code system ({RR, CR, RC, CC, PS, X, I} = 98.5% of 47K rows). Provincial is a 59-code system (agricultural = 42.3% of 29.5K rows).

**6 non-standard regional codes:**

| Non-Standard | Maps To | Found In |
|-------------|---------|----------|
| WC (Warehouse/Commercial) | CR | Cebu |
| AR (Agricultural Riceland) | A | Cebu |
| PC (Parking Commercial) | PS | Cebu |
| PH (Penthouse) | RC | Parañaque |
| R (Residential) | RR | Cebu |
| A0 | A50 (Open Grassland) | Pangasinan |

### 5.2 Classification Normalization Pipeline

```
1. Strip asterisks (prefix and suffix): "*RR***" → "RR"
2. Strip embedded revision numbers: "A50 23*" → "A50"
3. Split slash-separated codes: "RR/CR" → ["RR", "CR"]
4. Collapse whitespace: "R  R" → "RR"
5. Map non-standard codes via 6-entry lookup table
6. Validate against 69-variant enum (63 standard + 6 non-standard)
7. Store footnote marker count as u8 metadata
```

### 5.3 Seven Resolution Paths

**Key legal principle — Aquafresh (G.R. 170389):** The published schedule classification is authoritative. The engine does NOT determine "actual use." Classification resolution is a **selection problem** (user picks from options), not a **determination problem** (engine infers from characteristics). ~5% of lookups require user judgment.

| Path | Trigger | Action | Estimated % |
|------|---------|--------|------------|
| 1. Single-classification | Street/vicinity has one code | Auto-resolve | 60% |
| 2. Multi-classification | Street/vicinity has 2+ codes | User selects from available codes | 30% |
| 3. Condo ground floor | RC at ground floor | Apply CC + 20% rule | <5% |
| 4. Condo business use | RC with business use | Upgrade to CC + 20% | <2% |
| 5. Parking slot (PS) | PS code present | Apply RDO-specific formula (60-70% of parent RC/CC) | <5% |
| 6. Institutional (X) | X code, no ZV published | Fall back to nearest CR in same barangay/street | <1% |
| 7. Government property (GP) | GP ≥5,000 sqm | Area threshold gate (requires user input) | <1% |

**PS pricing formulas vary by RDO:** 60% of parent in Makati, 70% in Taguig, 70%/100% in Mandaluyong.

**CCT/TCT bifurcation:** CCT (Condominium Certificate of Title) = composite condo ZV; TCT (Transfer Certificate of Title) = separate land + improvement valuation. Title type determines which resolution path applies.

### 5.4 Rust Type Design

```rust
#[repr(u8)]
pub enum ClassCode {
    RR = 0, CR = 1, RC = 2, CC = 3, I = 4, X = 5,
    GL = 6, GP = 7, CL = 8, APD = 9, PS = 10, A = 11, DA = 12,
    A1 = 13, A2 = 14, /* ... */ A50 = 62,
    // Non-standard (mapped)
    WC = 63, AR = 64, PC = 65, PH = 66, R = 67, A0 = 68,
}

impl ClassCode {
    pub fn standard_equivalent(&self) -> ClassCode {
        match self {
            Self::WC => Self::CR, Self::AR => Self::A,
            Self::PC => Self::PS, Self::PH => Self::RC,
            Self::R => Self::RR, Self::A0 => Self::A50,
            other => *other,
        }
    }
}

// Per-location available codes as u128 bitset (69 codes fit in 128 bits)
pub type ClassCodeSet = u128;
```

---

## 6. Fallback Hierarchy

### 6.1 Seven-Level Decision Tree

The fallback hierarchy is a **decision tree** (not a linear chain). Level 5 is an X-only branch; Level 5A addresses a different scenario (no zonal data at all).

**Critical design principle (CTA Emiliano EB 1103, Gamboa 9720):** The engine MUST return NULL rather than interpolate at Levels 5A and 6. The BIR itself cannot substitute arbitrary valuations.

```
Level 1: Exact Match
  └─ Street + vicinity + classification found → return value
  └─ Authority: Section 6(E) NIRC
  └─ Confidence ceiling: 1.0

Level 2: Same Street, Different Vicinity
  └─ Street found but vicinity differs → return same-street value
  └─ Authority: DOF DO standard footnote Rule 3
  └─ Confidence ceiling: 0.85

Level 3: Barangay Catch-All ("ALL OTHER STREETS")
  └─ No street match → use catch-all entry (185 entries across 31 workbooks)
  └─ Authority: DOF DO Rule 3 operationalized
  └─ Confidence ceiling: 0.75

Level 4: Adjacent Barangay
  └─ No catch-all available → nearest barangay with same classification
  └─ Authority: DOF DO Rules 1 & 2 ("adjacent barangay of similar conditions")
  └─ Confidence ceiling: 0.65
  └─ Adjacency model: workbook-ordering approximation for MVP; GIS upgrade path

Level 5: Institutional Fallback (X-only branch)
  └─ X-coded property, no ZV → nearest CR in same barangay/street
  └─ Authority: DOF DO X provision
  └─ Confidence ceiling: 0.70

Level 5A: RAMO 2-91 (informational only)
  └─ No zonal data exists for the area at all
  └─ Rule: LGU FMV + 100%/150% markup (or 20% per current RDO practice — discrepancy documented)
  └─ ENGINE DOES NOT COMPUTE THIS — returns informational message only
  └─ Authority: RAMO 2-91

Level 6: NULL
  └─ No published zonal value exists after exhausting all levels
  └─ Return explicit NULL with CTA citations and BIR written inquiry guidance
  └─ Authority: CTA Emiliano (EB 1103, 2015), Gamboa (9720, 2020)
  └─ This is NOT a UX failure — it is the legally correct result
```

**Authority correction:** All fallback rules derive from DOF Department Order standard footnotes (DOF Secretary-signed regulatory text), NOT from RMO 31-2019 body text as originally assumed. RMO 31-2019 governs the process; DOF DOs contain the actual rules.

### 6.2 Edge Cases

- **Empty catch-all:** Mandaluyong enumerates all streets individually — no "ALL OTHER STREETS" entry exists. Level 3 skips to Level 4.
- **Agricultural barangays:** May lack CR classification entirely — Level 5 (institutional → commercial fallback) could fail. Engine returns NULL with explanation.
- **Parking slot formulas:** PS value = 60-70% of parent RC/CC. Formula varies by RDO (60% Makati, 70% Taguig). Engine must carry per-RDO PS pricing rules.
- **Cebu storey-based catch-all:** "ALL OTHER CONDOMINIUMS (≤7 storeys)" vs "(≥8 storeys)" with 44-78% premium. Building height is a required input for condo resolution in Cebu.

---

## 7. Condo & Special Property Handling

### 7.1 Condo Table Structure

9,712+ condo-classified rows across 31 workbooks. **ALL values are per-sqm** (no per-unit pricing found).

**6 NCR layout patterns:**

| Pattern | Description | RDOs |
|---------|-------------|------|
| A | Standard rows: building name → RC/CC/PS sequential | Most NCR |
| B | Merged building blocks: name merged vertically across 2-4 rows | 5/24 NCR |
| C | Inline mixed: condos interspersed with land entries | Scattered |
| D | Block merges: 3-4 row × 4-col blocks for building names | RDO 30 |
| E | Tower/floor ranges: separate entries per tower or floor range | BGC |
| F | Under-construction section | RDO 51 (Pasay) only |

**2 Provincial variants:**
- Cebu reverses NCR ordering: 56% CC-first (NCR: RC-first)
- Cebu storey-based catch-all tiers: "≤7 storeys" vs "≥8 storeys"

### 7.2 Parking Slot Models (4 variants)

| Model | Structure | Example RDOs |
|-------|-----------|-------------|
| Dual-PS | RC + PS + CC + PS (separate PS per classification) | Makati |
| Single-PS | PS after all condo entries | Some NCR |
| RC+PS only | PS associated with RC only | Provincial |
| CC+PS only | PS associated with CC only | Rare |

### 7.3 Penthouse Encoding (3 methods)

| Method | Example | RDOs |
|--------|---------|------|
| PH classification code | Separate PH row (no value published) | Parañaque |
| "(Penthouse)" name suffix | Separate block with own values | South Makati |
| Footnote formula | "PH = 110% of CC" or "PH = 120% of RC" | Various |

### 7.4 Special Codes

| Code | Meaning | Notes |
|------|---------|-------|
| PS | Parking Slot | Formula-based: 60-70% of parent RC/CC |
| PH | Penthouse | Non-standard; maps to RC |
| PC | Parking Commercial | Cebu only (2 barangays); maps to PS |
| "PARKING SLOT" (C0 text) | Explicit text in col 0 instead of code | 21 Cebu entries |

---

## 8. RDO Jurisdiction Mapping

### 8.1 Multi-RDO Cities

| City | RDO Count | Barangays | Notes |
|------|----------|-----------|-------|
| Manila | 6 (29-34) | 897 | Zone-based numbered barangays |
| Quezon City | 4 (28, 38-40) | 142 | 3 intra-barangay splits |
| Makati | 4 (47-50) | ~33 | EMBO transfer (RAO 1-2024) |
| Cebu City | 2 (83, 84) | 80 | North/south split |
| Davao City | 2 (113A, 113B) | 182 | Geographic split |

### 8.2 Intra-Barangay Splits (4 cases requiring street-level disambiguation)

| City | Barangay | Split | Boundary |
|------|----------|-------|----------|
| QC | Commonwealth | RDO 28 / RDO 39 | Don Mariano Marcos Ave / Litex Road |
| QC | Culiat | RDO 28 / RDO 38 | Tandang Sora Avenue |
| QC | Tandang Sora | RDO 28 / RDO 38 | Tandang Sora Avenue |
| Makati | Bel-Air complex | RDO 49 / RDO 50 | Salcedo Village carved out |

### 8.3 Recent Jurisdiction Changes

- **RAO 1-2024:** 10 EMBO barangays transferred from RDO 50 (South Makati) to RDO 44 (Taguig) per SC decision in Makati v. Taguig (G.R. 235316). Highest-impact change given BGC's economic significance.
- **RAO 4-2019:** RR7→7A/7B, RR8→8A/8B. Revenue Region renumbering only — no RDO boundary changes. Workbook headers reference new RR names.
- **8 BARMM municipalities (2024):** No published RDO assignment. Default to parent municipality RDO; flag as pending.

### 8.4 Mapping Table Design

```
Schema:
  barangay_id: u32 (PSA PSGC 9-digit code)
  rdo_code: u8 (1-114, geographic only)
  revenue_region: String
  city_municipality: String
  valid_from: Date
  valid_until: Option<Date>
  split_qualifier: Option<String>  // for intra-barangay splits
```

~42,000 entries, ~400 KB compressed. Trivially fits in WASM. 3-tier lookup: exact barangay → street disambiguation → city fallback.

---

## 9. RPVARA Transition Mechanics

### 9.1 Three-Regime Model

RA 12001 (RPVARA, effective July 2024) transfers property valuation authority from BIR to BLGF over a multi-year transition period.

**Regime A: Pre-Transition (BIR ZV Active)**
- Condition: No BLGF-approved SMV for this LGU
- Tax base (IRT): `max(selling_price, bir_zonal_value, lgu_existing_fmv)` — three-way max
- Data source: BIR zonal value workbooks
- Classification: BIR Annex B codes (63 codes)
- **Status (March 2026): Active for the vast majority of LGUs**

**Regime B: Transition Year 1 (New SMV)**
- Condition: BLGF-approved SMV in effect, within first year
- Tax base (IRT): `max(selling_price, blgf_smv)` — two-way max
- Tax base (RPT): capped at 6% increase over prior year (Section 29(c))
- Data source: BLGF-approved SMV
- Classification: LGU numeric tier system (R1-R12, C1-C8, I1-I3)
- **Status: Zero LGUs have reached this regime as of March 2026**

**Regime C: Post-Transition (Steady State)**
- Condition: BLGF-approved SMV, beyond first year
- Tax base: `max(selling_price, blgf_smv)` — two-way max, no cap
- **Status: No LGU has reached this regime yet**

### 9.2 Why the July 2026 Deadline Will Be Missed

| Evidence | Implication |
|----------|-------------|
| Only 37-42% of LGUs had compliant SMVs under old system | Historical compliance ~40% |
| Zero BLGF-approved SMVs as of March 2026 | Zero completions 21 months in |
| Davao City (2nd largest) still at "proposed" stage | Major cities not done |
| Davao realtors actively resisting (1,181% agricultural increase) | Political resistance |
| BIR continues updating zonal values (15-60% increases in 2025) | Old system still active |

**Projected rollout:**
- H2 2026: ~5-15 LGUs (early adopters)
- 2027: ~50-100 LGUs
- 2028: ~200-400 LGUs
- 2029+: remaining

**Engine design implication:** BIR zonal values must remain a first-class data source for 3-5+ years.

### 9.3 Classification Taxonomy Divergence

BIR and LGU systems are **structurally incompatible** — no automatic crosswalk exists.

| BIR (Annex B) | LGU (SMV) | Mapping |
|---------------|-----------|---------|
| RR (single code per vicinity) | R1-R12 (value-tiered within residential) | IMPOSSIBLE |
| CR (single code) | C1-C8 (value-tiered within commercial) | IMPOSSIBLE |
| RC/CC (condo-specific) | Not present (condo = building type, not land class) | Gap |
| A1-A50 (crop-based) | Agricultural Class 1-N by crop | Partial by crop type |
| X (institutional) | Not present | Gap |
| PS (parking) | Not present (building component) | Gap |

**Resolution strategy:** Store both taxonomies as metadata per record. Present applicable classification based on detected regime. No automatic mapping between taxonomies.

### 9.4 Regime Detection

```rust
pub struct LguRegimeRegistry {
    // ~1,715 LGUs × ~64 bytes = ~110 KB
    entries: HashMap<LguId, LguRegimeEntry>,
}

pub enum SmvStatus {
    NotYetApproved,                          // → Regime A
    InPreparation { stage: PreparationStage }, // → Regime A
    Approved { effectivity_date: NaiveDate },  // → Regime B or C
}

fn detect_regime(lgu_id: LguId, transaction_date: NaiveDate) -> Regime {
    match get_smv_status(lgu_id) {
        NotYetApproved | InPreparation => Regime::A,
        Approved { effectivity_date } => {
            if transaction_date < effectivity_date { Regime::A }
            else if months_since(effectivity_date) <= 12 { Regime::B }
            else { Regime::C }
        }
    }
}
```

### 9.5 Graceful Degradation (7 Scenarios)

| Scenario | BIR ZV? | BLGF SMV? | Engine Behavior |
|----------|---------|-----------|-----------------|
| S1: Normal pre-transition | Yes | No | Standard BIR lookup (Regime A) |
| S2: Newly approved SMV | Yes | Yes | Regime B — SMV primary, BIR for reference |
| S3: SMV partial coverage | Yes | Partial | Regime B for covered properties; Regime A fallback for gaps (0.8x confidence penalty) |
| S4: BIR ZV stale (>5 yr) | Stale | No | Regime A with staleness warning |
| S5: BARMM coverage gap | No | No | NULL with coverage gap explanation |
| S6: Post-transition | Historical | Yes | Regime C — SMV only |
| S7: SMV revoked | Yes | Revoked | Revert to Regime A |

---

## 10. Legal Framework & Edge Cases

### 10.1 Key Court Rulings

| Case | Principle | Engine Implication |
|------|-----------|-------------------|
| **CIR v. Aquafresh** (G.R. 170389) | Published classification prevails over actual use | Engine uses schedule classification only; does NOT determine "actual use" |
| **Spouses Emiliano v. CIR** (CTA EB 1103) | BIR cannot substitute arbitrary valuations when no ZV exists | Engine returns NULL at Level 6, never interpolates |
| **CIR v. Heirs of Gamboa** (CTA 9720) | Same principle confirmed | Reinforces NULL mandate |
| **DPWH v. Mirandilla** (SC) | ZV is "merely one index" of FMV; court awarded 6.5x | ZV ≠ FMV; engine warns about this distinction |
| Various SC decisions | Stale schedules remain in force until formally revised | Track schedule vintage; warn when >3 years old |

### 10.2 BIR Regulatory Framework

| Issuance | Role |
|----------|------|
| RMO 31-2019 | Operative order for zonal value establishment: committee structure, valuation methodology (avg of 2 highest of 3), Annex B (63 codes), Annex C (4-column format), 3-year revision mandate |
| RMC 115-2020 | Certification procedure for ONETT (no longer required as of 2020) |
| DOF Department Orders | The actual regulatory instruments containing fallback rules, classification provisions, and zonal value schedules |
| RMC 30-2025 | Circularizes RPVARA IRR but provides NO ONETT operational guidance for dual-source lookup |
| BIR Ruling OT-028-2024 | Installment sale timing: zonal value fixed at date of agreement (not closing), per RR 17-2003 §3(J). Engine uses `transaction_date` input accordingly. |

### 10.3 Edge Cases from CTA Rulings

1. **Classification disputes:** Published classification governs until schedule revision (Aquafresh). A property zoned RR cannot be reclassified to CR by BIR unilaterally — 3.08x tax delta (₱650 vs ₱2,000/sqm).
2. **Missing zonal values:** Engine must return NULL per CTA mandate. BIR's own practice of substituting bank appraisals was rejected.
3. **Procedural defects:** Section 6(E) consultation is mandatory. Schedules published without proper consultation can be challenged.
4. **Stale schedules:** 38% of schedules are outdated per DOF 2024 findings. Existing values remain in force until formally revised — engine flags vintage but does not adjust.
5. **ZV vs. just compensation:** For expropriation, courts consistently value properties well above ZV (1.5x-6.5x). Engine should include caveat that ZV ≠ FMV.

---

# PART 2: APP ARCHITECTURE SPEC

---

## 11. Architecture Overview

### 11.1 System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                           │
│                                                                 │
│  ┌──────────────────┐    postMessage    ┌────────────────────┐  │
│  │   React 19 PWA   │◄════════════════►│   Web Worker        │  │
│  │   (TypeScript)    │                  │   ┌──────────────┐  │  │
│  │                   │                  │   │  zv-engine    │  │  │
│  │  • Input form     │                  │   │  (Rust/WASM)  │  │  │
│  │  • Result card    │                  │   │              │  │  │
│  │  • Confidence     │                  │   │  • Matching   │  │  │
│  │    badge          │                  │   │  • Fallback   │  │  │
│  │  • Legal metadata │                  │   │  • Scoring    │  │  │
│  │  • RPVARA regime  │                  │   │  • Data store │  │  │
│  └──────────────────┘                  │   └──────────────┘  │  │
│           │                             └────────────────────┘  │
│           │ Service Worker                                      │
│           ▼                                                     │
│  ┌──────────────────┐                                          │
│  │  Cache Storage    │  Content-hash versioned chunks           │
│  │  • engine.wasm    │  CacheFirst (immutable)                  │
│  │  • zv-ncr.bin     │  NetworkFirst (manifest.json)            │
│  │  • zv-rr01.bin    │                                          │
│  │  • ...            │                                          │
│  └──────────────────┘                                          │
└─────────────────────────────────────────────────────────────────┘
                    ▲
                    │ Static files (CDN ~$20/mo)
                    │ No property data transmitted
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OPTIONAL: REST API (axum)                     │
│                                                                 │
│  POST /v1/lookup         — Primary lookup (uses same engine)    │
│  POST /v1/lookup/bulk    — Batch queries (Pro/Enterprise)       │
│  POST /v1/lookup/historical — Server-side 2.97M records         │
│  GET  /v1/classifications  — Available codes                    │
│  GET  /v1/locations/*      — Municipality/barangay lists        │
│  GET  /v1/data/version     — Current data version               │
└─────────────────────────────────────────────────────────────────┘
                    ▲
                    │ Weekly check + monthly full rebuild
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PIPELINE (zv-pipeline)                   │
│                                                                 │
│  1. ACQUIRE  → HTTP fetch 124 .xls workbooks from bir.gov.ph   │
│  2. PARSE    → Per-sheet: MergeMap, column detection, NOTICE    │
│  3. NORMALIZE → Classification + vicinity + footnote pipelines  │
│  4. VALIDATE → 12 cross-reference rules at 3 severity levels   │
│  5. INDEX/PACK → String interning, PackedRecord, binary format  │
│  6. PUBLISH  → Atomic CDN deployment with manifest.json         │
└─────────────────────────────────────────────────────────────────┘
```

### 11.2 Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Engine | Rust (`no_std` compatible) | Compiles to native + wasm32; type safety for 69-variant ClassCode |
| WASM bridge | wasm-bindgen | Standard Rust→WASM binding |
| Worker | Dedicated Web Worker | Privacy isolation; extensions can't access WASM memory |
| Frontend | React 19 + TypeScript + Vite 6 | Dominant PH dev ecosystem; component model fits cascading input |
| Styling | Tailwind CSS 4 | Utility-first, small bundle |
| State | Zustand | 3 stores: engine lifecycle, query, result |
| API server | axum (Rust) | Shares `zv-engine` crate with WASM |
| Pipeline | Rust + calamine | Both .xls (BIFF8) and .xlsx (OOXML) parsing |
| CI/CD | GitHub Actions | Weekly check + monthly full rebuild (~10 min) |
| Hosting | CDN (static files) | ~$20/mo; optional API at ~$50/mo |

### 11.3 Crate Structure

```
zv-engine/          — Core engine library (compiles to native + WASM)
  src/types/        — ClassCode, record types, confidence, regime
  src/data/         — ZonalValueStore, StringTable, indexes
  src/matching/     — 8-phase pipeline, street cascade, vicinity
  src/resolution/   — Classification, fallback, RPVARA
  src/scoring/      — 5-component confidence model
  src/serde/        — Custom binary format reader/writer

zv-engine-types/    — Shared types between pipeline and engine

zv-pipeline/        — Data ingestion pipeline
  src/acquire/      — HTTP fetch, change detection
  src/parse/        — NOTICE, merge map, column detection, condo
  src/normalize/    — Classification, vicinity, footnote
  src/validate/     — 12 cross-reference rules
  src/pack/         — Binary format writer, Revenue Region chunking
  src/monitor/      — Weekly change detection
  src/rpvara/       — BLGF SMV source parser (pluggable)

zv-web/             — React frontend + Web Worker
zv-api/             — axum REST API server
```

---

## 12. Rust Engine Design

### 12.1 Core Data Structures

```rust
// 20-byte packed record (expanded from 17 for u32 string indices)
#[repr(C, packed)]
pub struct PackedRecord {
    pub rdo_id: u8,           // 1 byte
    pub municipality_id: u16,  // 2 bytes
    pub barangay_id: u16,      // 2 bytes
    pub street_idx: u32,       // 4 bytes (index into StringTable)
    pub vicinity_idx: u32,     // 4 bytes
    pub classification: u8,    // 1 byte (ClassCode enum)
    pub zv_per_sqm: u32,      // 4 bytes (PHP, fits ₱2,160,000 max)
    pub do_idx: u16,           // 2 bytes (index into DOTable)
}

// Rich unpacked form for API/frontend
pub struct ZonalValueRecord {
    pub location: PropertyLocation,
    pub street: String,
    pub vicinity: String,
    pub classification: ClassCode,
    pub zv_per_sqm: u64,      // centavos for exact arithmetic
    pub department_order: DepartmentOrder,
    pub footnote: FootnoteMetadata,
    pub source: DataSource,
}

// Lookup result
pub struct LookupResult {
    pub value: Option<u64>,    // centavos; None = Level 6 NULL
    pub classification: ClassCode,
    pub confidence: ConfidenceBreakdown,
    pub fallback_level: FallbackLevel,
    pub regime: Regime,
    pub department_order: DepartmentOrder,
    pub warnings: Vec<Warning>,
    pub alternatives: Vec<AlternativeMatch>,
    pub match_explanation: MatchExplanation,
}
```

### 12.2 Index Design

| Index | Purpose | Structure |
|-------|---------|-----------|
| **LocationIndex** | Hierarchical scoping: RDO→Municipality→Barangay→record range | Sorted records + binary search; narrows 690K → ~160 per barangay |
| **StreetIndex** | Per-barangay street entries with pre-tokenized forms | HashMap<BarangayId, Vec<StreetEntry>> for Jaccard/Jaro-Winkler |
| **AvailableCodesIndex** | Per-location classification bitset | u128 ClassCodeSet per (RDO, barangay) |
| **StringTable** | Interned string storage | ~83K strings, ~1.46 MB, with normalized lookup variant |
| **DOTable** | Department Order metadata | DO#, effectivity date, revision ordinal per RDO |
| **JurisdictionMap** | Barangay→RDO with temporal versioning | ~42K entries, ~400 KB |
| **LguRegimeRegistry** | Per-LGU RPVARA regime status | ~1,715 entries, ~110 KB |

### 12.3 Matching Pipeline Detail

The 8-phase pipeline operates on a `PropertyQuery`:

```rust
pub struct PropertyQuery {
    pub municipality: String,
    pub barangay: String,
    pub street: Option<String>,
    pub vicinity: Option<String>,
    pub classification: Option<ClassCode>,
    pub property_type: PropertyType,   // Land | Condo | Parking
    pub transaction_date: NaiveDate,
    pub title_type: Option<TitleType>, // CCT | TCT
    pub area_sqm: Option<f64>,
    pub building_height: Option<u8>,   // Cebu storey-based
    pub far_value: Option<u8>,         // BGC FAR 1-18
}
```

### 12.4 Confidence Scoring

5-component multiplicative model:

```
overall = address_match × classification × fallback_penalty × data_freshness × regime_penalty

address_match:    0.0–1.0 (street + vicinity match quality)
classification:   1.0 (exact) | 0.9 (mapped non-standard) | 0.8 (user-selected)
fallback_penalty: Level-dependent ceiling (L1=1.0, L2=0.85, L3=0.75, L4=0.65, L5=0.70)
data_freshness:   1.0 (<3yr) | 0.9 (3-5yr) | 0.8 (5-10yr) | 0.7 (>10yr)
regime_penalty:   1.0 (primary source) | 0.8 (source mismatch degradation)
```

Mapped to 5 UI tiers: HIGH (≥0.85, green), MEDIUM (0.65-0.84, amber), LOW (0.50-0.64, orange), VERY LOW (<0.50, red), NO MATCH (0.0, gray).

### 12.5 WASM Exports

```rust
#[wasm_bindgen]
pub fn init(metadata: &[u8]) -> Result<(), JsValue>;

#[wasm_bindgen]
pub fn add_chunk(region_data: &[u8]) -> Result<u32, JsValue>;

#[wasm_bindgen]
pub fn lookup(query_json: &str) -> String; // JSON LookupResult

#[wasm_bindgen]
pub fn available_codes(rdo: u8, barangay: u16) -> String;

#[wasm_bindgen]
pub fn municipalities_for_rdo(rdo: u8) -> String;
```

### 12.6 Binary Bundle Format (Custom v1)

```
Header (32 bytes):
  magic: [u8; 4]     = b"ZV01"
  version: u32        = 1
  record_count: u32
  string_count: u32
  do_count: u16
  region_id: u8
  flags: u8
  reserved: [u8; 14]

Section 1: StringTable     (offset table + UTF-8 data)
Section 2: DOTable         (fixed-size DO metadata entries)
Section 3: PackedRecords   (sorted by location for binary search)
Section 4: LocationIndex   (RDO→municipality→barangay→record range)
Section 5: CodesIndex      (u128 bitsets per location)
Section 6: JurisdictionMap (barangay→RDO with temporal versioning)
Section 7: RegimeRegistry  (LGU→SmvStatus)
```

---

## 13. WASM Bridge & Privacy Model

### 13.1 Architecture Decision: Tiered Client-Side WASM

After evaluating 4 architectures (full client-side, hybrid WASM+API, tiered client-side, server-only), **tiered client-side WASM** was selected.

**3-phase loading strategy:**

| Phase | Content | Size (brotli) | Time (4G 30Mbps) |
|-------|---------|--------------|-------------------|
| 1 | Engine WASM + jurisdiction metadata + NCR data | 585 KB | ~280 ms |
| 2 | Full 690K dataset (19 Revenue Region chunks, background) | 4.8 MB total | ~1.3 s |
| 3 | Historical data (2.97M records, optional API only) | ~18 MB | N/A (server) |

**Revenue Region chunking:** 19+1 chunks (NCR pre-loaded, 19 provincial × ~230 KB avg brotli). Content-hash versioned filenames for immutable CDN caching. Only changed chunk re-downloaded on BIR updates.

### 13.2 Philippine Context Validation

| Factor | Value | Assessment |
|--------|-------|-----------|
| Median 4G download | 30-35 Mbps | 4.8 MB in ~1.3s — acceptable |
| Data cost (5 MB) | ₱0.05 (0.007% of daily minimum wage) | Negligible |
| Chrome mobile share | 90.1% | WASM universal |
| Budget device RAM | 4-6 GB | 25 MB runtime = 1.25% of free RAM |
| iOS Safari WASM ceiling | 256 MB | Our 25 MB = 10% of limit |

### 13.3 Privacy Model

**Property details NEVER leave the browser.**

```
Main Thread (React UI)
  ↕ postMessage (serialized query / result only)
Web Worker (isolated context)
  ↕ WASM FFI (typed values)
WASM Engine (linear memory private to Worker)
```

Privacy guarantees:
1. Extension content scripts cannot access Worker globals → WASM memory isolated
2. Main thread communicates only via postMessage → no shared memory
3. No third-party script can read WASM linear memory
4. Recent lookups stored in-memory only → never persisted to disk (shared device safety)
5. POST (not GET) for API lookups → query not in URL/CDN/browser logs

### 13.4 Offline-First PWA

After initial cache, the application works entirely offline — unique among all 7 surveyed competitors.

```
Service Worker strategy:
  CacheFirst  → content-hash versioned data chunks (immutable)
  NetworkFirst → manifest.json (short TTL for update detection)

Update flow:
  1. BIR publishes new DO for RDO 47
  2. Pipeline rebuilds NCR chunk → new content hash
  3. manifest.json updated → SW detects on next visit
  4. Only changed chunk re-downloaded (~230 KB, not full 4.8 MB)
  5. 30-day grace period for old chunks
```

### 13.5 Performance Projections

| Scenario | Time | Notes |
|----------|------|-------|
| First visit, NCR functional (4G) | ~280 ms | Engine + NCR chunk loaded |
| First visit, full data (4G) | ~1.3 s | All chunks streamed in background |
| First visit (rural 5 Mbps) | ~1.7 s NCR, ~7.6 s full | Tiered loading mitigates |
| Repeat visit (warm cache) | ~35 ms | V8 code cache + Cache API, zero network |
| Lookup latency | <100 ms | 10ms engine + 50ms Worker postMessage + 40ms React render |

---

## 14. Data Pipeline

### 14.1 Six-Stage Pipeline

```
Stage 1: ACQUIRE
  └─ HTTP conditional GET + content-hash change detection per RDO
  └─ 2s rate limiting, PDF-skip for ~2-5 image-only RDOs
  └─ Fallback to cached workbooks on download failure

Stage 2: PARSE
  └─ NOTICE sheet parser: DO → sheet → municipality → effectivity mapping
  └─ 3 date format cascade: Excel serial (86%) → ISO (9%) → human (5%)
  └─ Per-sheet MergeMap construction (HashMap for O(1) cell resolution)
  └─ Per-barangay-block column detection (keyword scoring, 6 patterns)
  └─ Condo section detection and CondoBlock assembly

Stage 3: NORMALIZE
  └─ Classification pipeline:
     strip asterisks → strip revision numbers → collapse whitespace
     → map 6 non-standard codes → validate 69-variant enum
  └─ Vicinity pipeline:
     detect address mode (10 semantic types) → parse cross-street separators
     → resolve road-proximity tiers → expand abbreviations
     → 331 three-segment disambiguation via street dictionary
     → Pasig semicolon handling → BGC FAR tier extraction
  └─ Footnote pipeline:
     mandatory legend-first processing (reversal handling)
     → strip markers → preserve as u16 metadata

Stage 4: VALIDATE
  └─ 12 cross-reference rules at 3 severity levels:
     Error: unknown classification code, duplicate record
     Warn: ZV outlier >2σ, CR<RR anomaly, PS>RC anomaly
     Info: empty vicinity, stale schedule >3yr
  └─ Never silently drops records

Stage 5: INDEX & PACK
  └─ String interning (~83K strings, ~1.46 MB)
  └─ PackedRecord sorting by (rdo, municipality, barangay, street_idx)
  └─ LocationIndex + StreetIndex + CodesIndex construction
  └─ Custom v1 binary format (7 sections)
  └─ Revenue Region chunking (NCR + 19 provincial)
  └─ Content-hash filenames for immutable CDN caching

Stage 6: PUBLISH
  └─ Atomic CDN deployment with manifest.json
  └─ Short TTL on manifest, infinite TTL on chunk files
  └─ 30-day grace period for old chunks
```

### 14.2 Pipeline Crate Structure

```
zv-pipeline/
  src/
    acquire/mod.rs        — HTTP client, change detection, rate limiter
    parse/
      notice.rs           — NOTICE sheet parser (DO→sheet→municipality)
      merge_map.rs        — MergeMap construction (O(1) cell resolution)
      columns.rs          — Per-barangay-block column detection (6 patterns)
      barangay.rs         — Barangay block boundary detection
      condo.rs            — Condo section detection + block assembly
      data_rows.rs        — Data row extraction with merge resolution
    normalize/
      classification.rs   — 7-step normalization pipeline
      vicinity.rs         — 10-type vicinity parser
      footnote.rs         — Per-section legend parsing
      address.rs          — Street name normalization + alias resolution
      codes.rs            — ClassCode enum + non-standard mapping
    validate/mod.rs       — 12 rules, 3 severity levels
    pack/
      strings.rs          — String interning
      records.rs          — PackedRecord creation
      index.rs            — LocationIndex + StreetIndex + CodesIndex
      binary.rs           — Custom v1 format writer
      chunks.rs           — Revenue Region chunking + manifest
    monitor/mod.rs        — Weekly HTTP header check
    rpvara/mod.rs         — SourceParser trait + BLGF SMV integration
    main.rs               — CLI entry point
```

### 14.3 RPVARA Pipeline Integration

```rust
/// Data ingestion trait — each source type implements this
pub trait SourceParser {
    fn parse(&self, raw_data: &[u8]) -> Result<Vec<ValuationRecord>, ParseError>;
    fn detect_format(&self, raw_data: &[u8]) -> Option<SourceFormat>;
}

pub enum SourceFormat {
    BirExcelWorkbook(BirColumnLayout),  // 6 known patterns
    BlgfSmvPdf,                         // Format TBD
    RpisApi,                            // Format TBD
    BlgfSmvExcel,                       // Some LGUs may use Excel
}
```

Separate `zv-smv-{lgu}.bin` chunks for BLGF SMV data. LguRegimeRegistry updated monthly.

### 14.4 CI/CD

- **Weekly check (~2 min):** HTTP HEAD requests to 124 BIR workbook URLs; content-hash comparison
- **Monthly full rebuild (~10 min on GitHub Actions):** Re-parse all workbooks, rebuild binary bundles
- **Independent per-RDO failure isolation:** One workbook parse failure doesn't block other RDOs
- **Idempotent:** Same inputs → identical binary output (SHA-256 verified)

---

## 15. Frontend Design

### 15.1 Input Form (Progressive Disclosure)

```
City/Municipality  [Cascading dropdown, PSGC-backed, ~1,913 entries]
                    ↓ (filters barangay list)
Barangay           [Cascading dropdown, ~42K entries]
                    ↓ (filters available classifications)
Street (optional)  [Free-text input — NO server-side autocomplete (privacy)]
Vicinity (optional)[Free-text input]
Classification     [Dropdown filtered to per-location available codes]
                    (NCR: ~7 codes, Provincial: ~59, Binondo: 5, Davao: 43)
Property Type      [Radio: Land | Condo | Parking]
Transaction Date   [Date picker, defaults to today]

Conditional fields:
  If Condo:  Building Name, Title Type (CCT/TCT)
  If BGC:    FAR Tier (1-18)
  If Provincial: Road Proximity (7-tier dropdown)
  If Cebu Condo: Building Height (storeys)
```

### 15.2 Result Card

```
┌─────────────────────────────────────────────┐
│  ₱200,000 /sqm                    [HIGH ✓]  │
│  Residential Regular (RR)                    │
│                                              │
│  ▸ Match Explanation                         │
│    Address mode: NCR cross-street            │
│    Street match: Exact (tier 1/5)            │
│    Fallback level: 1 (exact match)           │
│    Confidence: 0.95 (5 components)           │
│                                              │
│  ▸ Legal Metadata                            │
│    DO# 022-2021 (7th Revision East Makati)   │
│    Effectivity: January 15, 2021             │
│    RDO 47 (East Makati)                      │
│    Regime: Pre-transition (Section 29(b))    │
│    Tax base: max(SP, ZV, FMV) × rate        │
│                                              │
│  ⚠ Schedule last revised 2021 (5 years ago)  │
│                                              │
│  Alternative classifications at this location:│
│    CR: ₱288,000/sqm                         │
│    RC: ₱250,000/sqm                         │
└─────────────────────────────────────────────┘
```

**Level 6 NULL result:** Explicit gray card with "No published zonal value" message, CTA case citations, and BIR written inquiry guidance. Legally correct — not a UX failure.

**RPVARA display:** Regime-aware banner, dual-source comparison panel during transition period.

### 15.3 State Management (Zustand)

3 stores:
1. **Engine store:** WASM lifecycle (loading, ready, error), loaded regions, record count
2. **Query store:** Current form inputs, validation state
3. **Result store:** Latest lookup result, history (in-memory only — never persisted)

### 15.4 Worker Protocol

8 typed postMessage message types:

```typescript
type WorkerMessage =
  | { type: 'init'; chunks: ArrayBuffer[] }
  | { type: 'loadChunk'; region: string; data: ArrayBuffer }
  | { type: 'lookup'; id: number; query: LookupQuery }
  | { type: 'availableCodes'; id: number; rdo: number; barangay: number }
  | { type: 'municipalities'; id: number; rdo: number }
  | { type: 'barangays'; id: number; municipality: number }
  | { type: 'dataVersion'; id: number };

type WorkerResponse =
  | { type: 'ready'; recordCount: number; regionsLoaded: string[] }
  | { type: 'chunkLoaded'; region: string; recordsAdded: number }
  | { type: 'result'; id: number; result: LookupResult }
  | { type: 'codes'; id: number; codes: string[] }
  | { type: 'error'; id: number; message: string };
```

No SharedArrayBuffer — avoids COOP/COEP header complexity.

### 15.5 Performance Targets

| Metric | Target |
|--------|--------|
| NCR-interactive on 4G | <1 s |
| Lookup latency (engine + Worker + render) | <100 ms |
| Repeat visit cold start | <100 ms |
| Lighthouse score | >90 |
| Accessibility | WCAG 2.1 AA (labels, keyboard nav, ARIA live regions, colorblind-safe) |

---

## 16. Public REST API

### 16.1 Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/v1/lookup` | Primary lookup (POST for privacy — no query in URL) | API key |
| POST | `/v1/lookup/bulk` | Batch queries (max 100-10K) | Pro/Enterprise |
| POST | `/v1/lookup/historical` | Server-side 2.97M records | Pro/Enterprise |
| GET | `/v1/classifications` | Available classification codes | Public |
| GET | `/v1/locations/municipalities` | Municipality list | Public |
| GET | `/v1/locations/barangays?municipality={id}` | Barangay list | Public |
| GET | `/v1/data/version` | Current data version + last update | Public |

### 16.2 Response Format

```json
{
  "zonal_value": {
    "amount": 200000.00,
    "amount_centavos": 20000000,
    "currency": "PHP",
    "per_unit": "sqm"
  },
  "classification": {
    "code": "RR",
    "name": "Residential Regular",
    "source": "BIR_ANNEX_B"
  },
  "confidence": {
    "overall": 0.95,
    "tier": "HIGH",
    "breakdown": {
      "address_match": 1.0,
      "classification": 1.0,
      "fallback_penalty": 1.0,
      "data_freshness": 0.95,
      "regime_penalty": 1.0
    }
  },
  "legal_metadata": {
    "department_order": "DO 022-2021",
    "revision": "7th Revision East Makati",
    "effectivity_date": "2021-01-15",
    "rdo": "RDO 47",
    "regime": "PRE_TRANSITION",
    "tax_base_formula": "max(SP, ZV, FMV)",
    "applicable_law": "Section 29(b) RA 12001 + Section 6(E) NIRC"
  },
  "fallback": {
    "level": 1,
    "description": "Exact match",
    "authority": "Section 6(E) NIRC"
  },
  "warnings": [],
  "alternatives": [
    { "classification": "CR", "zonal_value": 288000.00 }
  ],
  "match_explanation": {
    "address_mode": "NCR_CROSS_STREET",
    "street_match_method": "EXACT",
    "street_match_tier": 1
  }
}
```

Integer centavos alongside float amounts for exact downstream tax computation.

### 16.3 Error Codes

| Code | Meaning |
|------|---------|
| 400 | Invalid query parameters |
| 401 | Invalid or missing API key |
| 404 | Location not found in dataset |
| 429 | Rate limit exceeded |
| 500 | Internal engine error |

### 16.4 Pricing

| Tier | Price | Rate Limit | Features |
|------|-------|-----------|----------|
| Free | $0 | 100 req/day | Single lookup, current data |
| Pro | $49/mo | 10K req/day | Bulk, historical, webhooks |
| Enterprise | Custom | Unlimited | SLA, dedicated support |

---

## 17. Data Size & Bundling

### 17.1 Bundle Size Summary

| Component | Raw | Brotli |
|-----------|-----|--------|
| WASM engine | ~500 KB | ~200 KB |
| String table (~83K strings) | ~1.46 MB | ~500 KB |
| NCR data (24 RDOs, 40K records) | ~1.1 MB | ~385 KB |
| Jurisdiction map (~42K entries) | ~800 KB | ~400 KB |
| **NCR-first bundle (Phase 1)** | **~2.4 MB** | **~585 KB** |
| Remaining 19 Revenue Region chunks | ~12.3 MB | ~3.7 MB |
| **Full current dataset** | **~14.7 MB** | **~4.8 MB** |
| Historical (all revisions, API-only) | ~51.8 MB | ~18.1 MB |

### 17.2 Comparison to Production WASM Deployments

| Application | Compressed Size | Status |
|-------------|----------------|--------|
| SQLite WASM | ~600 KB-1.2 MB | Massive adoption |
| DuckDB WASM | ~3.2 MB | Observable, MotherDuck |
| **Our engine (full)** | **~4.8 MB** | Within production norms |
| Figma | ~3-5 MB | Millions of users |
| AutoCAD Web | 15+ MB (lazy) | Autodesk production |

### 17.3 RPVARA Scaling Impact

| Scenario | Additional Brotli | Total |
|----------|-------------------|-------|
| No LGUs transitioned (current) | 0 | 4.8 MB |
| 10% transitioned | ~480 KB | 5.3 MB |
| 50% transitioned | ~2.4 MB | 7.2 MB |
| 100% dual-source (worst case) | ~4.4 MB | 9.2 MB |
| Post-transition (BIR retired) | 0 | ~4.8 MB |

Tiered loading handles all scenarios gracefully. BLGF SMV data delivered as separate per-LGU chunks.

---

## 18. Competitive Context

### 18.1 Market State

7 platforms surveyed. **Market is structurally immature:** every platform is a closed web app with no API, no address matching, no legal metadata, zero RPVARA readiness.

| Platform | Records | API | Address Matching | Legal Metadata | RPVARA | Privacy |
|----------|---------|-----|-----------------|---------------|--------|---------|
| Housal | ~2M | Internal only | No | DO# in DB, not API | No | Server |
| RealValueMaps | 2.7M claimed | Non-functional | No | Planned | No | Server |
| REN.PH | 336K | No | No | No | No | Server |
| ZonalValueFinderPH | ~30K+ | No | No | No | No | Server |
| LandValuePH | Unknown | No | No | No | No | Server |
| **Our Engine** | **690K current** | **Public, documented** | **8-phase pipeline** | **Per-record** | **3-regime model** | **Client-side** |

### 18.2 Five Systemic Failures

1. Treating ZV lookup as table browsing, not address resolution
2. Ignoring legal metadata (DO#, effectivity dates)
3. Building for current regulatory regime only
4. Assuming address matching is simple
5. Neglecting data quality (Housal: 95% null vicinities; RealValueMaps: wrong taxonomy)

### 18.3 Competitive Moats

| Capability | Replication Time |
|-----------|-----------------|
| 8-phase address matching | 2-3 years |
| RPVARA three-regime model | 3-5 years |
| 124-RDO workbook parser | 2+ years |
| 7-level fallback with CTA citations | 2+ years |
| WASM client-side engine | ~1 year (architectural, not domain) |

### 18.4 First-Mover Windows

- **RPVARA dual-source (12-18 months):** Opens H2 2026 when first BLGF SMVs are approved
- **API-first infrastructure (6-12 months):** No public ZV API exists anywhere
- **Privacy (ongoing):** Permanent architectural advantage — competitors cannot incrementally migrate

### 18.5 Threat Assessment

No platform within 12 months of matching planned capabilities. Most credible future threat: BIR's own RPIS (under procurement, 2-4 year timeline, poor PH government IT track record).

---

## 19. Open Questions

### 19.1 Implementation Phase Questions

| # | Question | Impact | Mitigation |
|---|----------|--------|------------|
| 1 | BIR workbook URL stability — will URLs change? | Pipeline acquisition | HTTP 404 fallback to cached; monitor with weekly checks |
| 2 | BLGF SMV digital format — will RPIS provide an API? | RPVARA data ingestion | Pluggable SourceParser trait; design for worst case (PDF) |
| 3 | Incremental bundle updates — can we diff-update chunks? | Update bandwidth | Content-hash versioning already minimizes to per-RR chunks |
| 4 | PSGC integration depth — should we use PSA codes directly? | Location indexing | Yes — adopt PSGC as canonical (RealValueMaps validates) |
| 5 | PDF OCR for outlier RDOs — worth the effort for 2-5 image-only files? | Coverage | Defer to v2; flag as coverage gap |
| 6 | Location search ranking — how to order autocomplete results? | UX | Population-weighted + recent-query frequency |
| 7 | Map integration — GIS layer for v2? | UX | Leaflet + CARTO tiles; viewport-based barangay polygons |
| 8 | Shareable result URLs — encode query in URL? | UX | Privacy concern — keep optional, warn user |
| 9 | Webhook notifications for BIR updates | API feature | Pro/Enterprise feature; monitor-based trigger |
| 10 | Embed mode for third-party sites | Distribution | iframe + postMessage API; v2 feature |

### 19.2 Legal/Regulatory Unknowns

| # | Question | Status |
|---|----------|--------|
| 1 | Can BIR issue NEW ZV revisions post-RPVARA? | Ambiguous — accept all DOF DOs regardless |
| 2 | Will PVS standardize classification across all LGUs? | Unknown — design for heterogeneity |
| 3 | How will condo valuation work under BLGF SMV? | Unresolved — building vs. land split differs from BIR |
| 4 | Will RPIS launch on time (July 2026)? | Unlikely — procurement still underway |
| 5 | RAMO 2-91: is 100%/150% or 20% the current practice? | Discrepancy documented — engine doesn't compute |

---

## 20. Design Decision Traceability

Every architecture decision traces to specific wave findings. This table maps the 30 most significant decisions.

| # | Decision | Rationale | Wave Source |
|---|----------|-----------|------------|
| 1 | Full client-side WASM primary architecture | 4.8 MB brotli fits mobile; privacy is moat | W2 data-size-estimation |
| 2 | Tiered loading (NCR-first 585 KB) | ~80% tax transactions are NCR; rural mitigation | W2 data-size-estimation §6.2 |
| 3 | Revenue Region chunking (19+1) | Natural admin boundary; avg ~230 KB; independent update | W3 rdo-jurisdiction-mapping |
| 4 | Web Worker for WASM isolation | Extensions can't access Worker memory → privacy | W4 competitive-gap-synthesis |
| 5 | Custom binary format (not JSON/Protobuf) | 7x smaller than JSON, 3.4x smaller than Protobuf | W2 data-size-estimation §4.1 |
| 6 | Keyword-based column detection (not position) | 6 column patterns; headers repeat per barangay | W2 workbook-column-layouts |
| 7 | MergeMap before data reading | 52K+ merges; O(1) resolution required | W2 merged-cell-patterns |
| 8 | Per-section footnote legend parsing | Asterisk meaning reversal between regions | W2 footnote-convention-mapping |
| 9 | Dual-mode address matching (NCR + provincial) | 40.7% cross-street vs. 7-tier road-proximity | W2 address-vicinity-patterns |
| 10 | 5-tier street cascade (exact → Jaro-Winkler) | 13,080 unique vicinities; fuzzy needed but high threshold | W3 address-matching-algorithms |
| 11 | 0.90 Jaro-Winkler threshold | Prevent SAN ANTONIO/SAN AGUSTIN false positives | W3 address-matching-algorithms |
| 12 | ~13K street dictionary for separator disambiguation | 331 three-segment cross-streets | W2 address-vicinity-patterns |
| 13 | Aquafresh principle: published classification only | CIR v. Aquafresh G.R. 170389 | W1 cta-zonal-rulings |
| 14 | 7-level fallback tree (not linear chain) | Level 5 is X-only branch; Level 5A is separate scenario | W3 fallback-hierarchy-implementation |
| 15 | NULL at Level 6 (never interpolate) | CTA Emiliano EB 1103, Gamboa 9720 | W1 cta-zonal-rulings |
| 16 | DOF DO as fallback authority (not RMO 31-2019) | Verification corrected authority attribution | W3 fallback-hierarchy-implementation |
| 17 | BIR ZV as first-class source for 3-5+ years | Zero BLGF SMVs; 37% historical compliance | W3 rpvara-dual-source-resolution §3 |
| 18 | No classification crosswalk (BIR ↔ LGU) | Taxonomies structurally incompatible | W3 rpvara-dual-source-resolution §4 |
| 19 | LguRegimeRegistry (~110 KB, monthly updates) | Per-LGU regime detection; trivial WASM size | W3 rpvara-dual-source-resolution §8 |
| 20 | Pluggable SourceParser trait | BLGF SMV format unknown; RPIS may provide API | W3 rpvara-dual-source-resolution §7 |
| 21 | 0.8x confidence penalty for source mismatch | BIR ZV used for Regime B/C property = degraded | W3 rpvara-dual-source-resolution §9 |
| 22 | ClassCode enum with 69 variants (u8) | 63 Annex B + 6 non-standard; fits in u8 | W2 classification-code-usage |
| 23 | u128 ClassCodeSet bitsets | 69 codes fit; per-location available codes filter | W5 rust-engine-design |
| 24 | PackedRecord at 20 bytes | u32 string indices for >65K unique strings | W5 rust-engine-design |
| 25 | POST for lookups (not GET) | Privacy: query not in URL/CDN/browser logs | W5 frontend-api-design |
| 26 | Integer centavos in API responses | Exact downstream tax computation (no float drift) | W5 frontend-api-design |
| 27 | PSGC codes as canonical location keys | RealValueMaps validates; unambiguous identification | W4 realvaluemaps-approach |
| 28 | API-first design (frontend = reference impl) | No public ZV API exists; infrastructure gap | W4 competitive-gap-synthesis |
| 29 | 3-tier pricing (Free/Pro/Enterprise) | RealValueMaps validates market at PHP 2,999-9,999/mo | W4 competitive-gap-synthesis |
| 30 | Accept all DOF DOs regardless of post-RPVARA date | Legal validity unresolved; engine doesn't pre-judge | W3 rpvara-dual-source-resolution §10 |

---

## Appendix A: Verified Claims

All Wave 3 resolution logic was cross-checked against 2+ independent sources per the verification protocol.

| Domain | Claims Checked | Confirmed | Partially Confirmed | Contradictions |
|--------|---------------|-----------|--------------------|-|
| Fallback hierarchy | 7 levels + authority | 7/7 | 0 | 0 |
| Classification resolution | 8 core claims | 6 | 2 | 0 |
| Address matching | Pipeline design | Confirmed against 15+ sources | Geocoding confirmed insufficient | 0 |
| RPVARA dual-source | 12 claims | 10 | 2 | 0 |

Partial confirmations:
- Agricultural 1,000 sqm threshold: operational practice, NOT formally codified in Annex B
- Zero BLGF-approved SMV: unprovable negative, but strongly evidenced across multiple sources

---

## Appendix B: Source Material Index

### Legal Sources
- RA 12001 (RPVARA): [LawPhil](https://lawphil.net/statutes/repacts/ra2024/ra_12001_2024.html)
- BLGF MC 001-2025 (IRR): [BLGF](https://blgf.gov.ph/wp-content/uploads/2025/03/BLGF-MC-No.-001.2025-IRR-of-RA-No.-12001-or-the-RPVARA-Reform-Act-6-Jan-2025-Approved-3.pdf)
- RMO 31-2019: BIR operative order for zonal values
- RMC 115-2020: ONETT certification procedure
- CIR v. Aquafresh (G.R. 170389): Classification authority
- Spouses Emiliano v. CIR (CTA EB 1103): NULL mandate
- CIR v. Heirs of Gamboa (CTA 9720): NULL mandate confirmed

### Data Sources
- 31 BIR zonal value workbooks (24 NCR + 7 provincial) in `input/bir-workbook-samples/`
- PSA Philippine Standard Geographic Code (PSGC): 42,000+ barangays
- BIR RDO directory: 124 geographic RDOs

### Analysis Files (27 total)
- Wave 1 (7): bir-workbook-ncr-samples, bir-workbook-provincial-samples, rmo-31-2019-annexes, rpvara-transition-mechanics, cta-zonal-rulings, third-party-platform-survey, prior-analysis-import
- Wave 2 (8): workbook-column-layouts, merged-cell-patterns, sheet-organization, address-vicinity-patterns, classification-code-usage, condo-table-structures, data-size-estimation, footnote-convention-mapping
- Wave 3 (5): rdo-jurisdiction-mapping, address-matching-algorithms, classification-resolution-logic, fallback-hierarchy-implementation, rpvara-dual-source-resolution
- Wave 4 (3): housal-data-model, realvaluemaps-approach, competitive-gap-synthesis
- Wave 5 (4): rust-engine-design, wasm-vs-hybrid-tradeoff, data-pipeline-architecture, frontend-api-design

---

*This specification was assembled from 27 analyses across 6 waves of the reverse-ph-zonal-value-engine ralph loop. Every design decision traces to specific data findings, legal citations, or competitive analysis. The spec is intended to be directly actionable for a forward implementation loop.*
