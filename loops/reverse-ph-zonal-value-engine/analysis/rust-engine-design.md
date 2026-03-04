# Rust Engine Design — Zonal Value Lookup Engine

**Wave 5 | Aspect: rust-engine-design**
**Date: 2026-03-04**

## Overview

This document defines the complete Rust engine architecture for the Zonal Value Lookup Engine: module organization, core data structures, index design, matching algorithms, classification resolution, fallback state machine, RPVARA regime handling, and the public API surface. Every design decision traces to specific findings from Waves 2-4.

The engine is designed as a `no_std`-compatible library crate (`zv-engine`) that compiles to both native (for server-side pipeline and CLI tools) and `wasm32-unknown-unknown` (for client-side browser execution).

---

## 1. Module Structure

```
zv-engine/
├── Cargo.toml
├── src/
│   ├── lib.rs                    # Public API surface, feature gates
│   ├── types/
│   │   ├── mod.rs
│   │   ├── classification.rs     # ClassCode enum, ClassifiedCode, LandUseCategory
│   │   ├── location.rs           # RdoId, MunicipalityId, BarangayId, PropertyLocation
│   │   ├── record.rs             # ZonalValueRecord, ValuationRecord, DataSource
│   │   ├── regime.rs             # Regime, SmvStatus, LguRegimeEntry
│   │   ├── confidence.rs         # ConfidenceScore, ConfidenceTier, ConfidenceBreakdown
│   │   └── result.rs             # LookupResult, FallbackStep, AddressMatchResult
│   ├── data/
│   │   ├── mod.rs
│   │   ├── store.rs              # ZonalValueStore — the primary data container
│   │   ├── string_table.rs       # Interned string storage with normalized lookup
│   │   ├── index.rs              # RdoIndex, BarangayIndex, StreetIndex, VicinityIndex
│   │   └── jurisdiction.rs       # JurisdictionMap, RDO→barangay resolution
│   ├── matching/
│   │   ├── mod.rs
│   │   ├── address.rs            # 8-phase address matching pipeline
│   │   ├── street.rs             # 5-tier street matching cascade
│   │   ├── vicinity.rs           # NCR cross-street & provincial road-proximity parsers
│   │   ├── condo.rs              # Condo building name matching + PS association
│   │   └── normalize.rs          # Address normalization (uppercase, diacritics, alias)
│   ├── resolution/
│   │   ├── mod.rs
│   │   ├── classification.rs     # 7-path classification resolution
│   │   ├── fallback.rs           # 7-level fallback decision tree
│   │   └── regime.rs             # RPVARA regime detection + tax base formula selection
│   ├── scoring/
│   │   ├── mod.rs
│   │   └── confidence.rs         # Confidence computation from match components
│   └── serde/
│       ├── mod.rs
│       ├── binary.rs             # Binary format serialization/deserialization
│       └── json.rs               # JSON format (for API responses, debugging)
```

**Design rationale:** Module boundaries follow the resolution pipeline stages: data loading → jurisdiction resolution → address matching → classification resolution → fallback → regime detection → confidence scoring → result assembly. Each module is independently testable with fixtures from actual RDO data (Wave 2).

---

## 2. Core Data Types

### 2.1 Classification (`types/classification.rs`)

```rust
/// All 63 BIR Annex B classification codes + 6 non-standard regional codes.
/// Fits in u8 (0-69 range). Discriminants match binary format encoding.
///
/// Source: Wave 2 classification-code-usage analysis — 62 unique codes
/// found across 31 workbooks (76,577 classified rows).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
#[repr(u8)]
pub enum ClassCode {
    // === Primary codes (13) — present in 100% of RDOs ===
    RR  = 0,   // Residential Regular
    CR  = 1,   // Commercial Regular (universal: 31/31 RDOs)
    RC  = 2,   // Residential Condominium
    CC  = 3,   // Commercial Condominium
    I   = 4,   // Industrial
    X   = 5,   // Institutional/Exempt
    GL  = 6,   // Government Lot
    GP  = 7,   // Government Property (≥5,000 sqm threshold)
    CL  = 8,   // Communal Lot
    APD = 9,   // Ancestral Property Domain
    PS  = 10,  // Parking Slot
    DA  = 11,  // Drying Area (provincial only)
    A   = 12,  // Agricultural (generic)

    // === Agricultural sub-codes (50) — A1 through A50 ===
    // A1=Riceland Irrigated ... A50=Other Agricultural
    // Only 43 of 50 observed in sample; all 50 defined per Annex B.
    A1  = 13, A2  = 14, A3  = 15, A4  = 16, A5  = 17,
    A6  = 18, A7  = 19, A8  = 20, A9  = 21, A10 = 22,
    A11 = 23, A12 = 24, A13 = 25, A14 = 26, A15 = 27,
    A16 = 28, A17 = 29, A18 = 30, A19 = 31, A20 = 32,
    A21 = 33, A22 = 34, A23 = 35, A24 = 36, A25 = 37,
    A26 = 38, A27 = 39, A28 = 40, A29 = 41, A30 = 42,
    A31 = 43, A32 = 44, A33 = 45, A34 = 46, A35 = 47,
    A36 = 48, A37 = 49, A38 = 50, A39 = 51, A40 = 52,
    A41 = 53, A42 = 54, A43 = 55, A44 = 56, A45 = 57,
    A46 = 58, A47 = 59, A48 = 60, A49 = 61, A50 = 62,

    // === Non-standard regional codes (6) ===
    // Source: Wave 2 — found in actual workbooks, not in Annex B.
    // Mapped to standard equivalents for resolution but preserved for audit.
    WC  = 63,  // → CR (Water Commercial, Cebu)
    AR  = 64,  // → A  (Agricultural Regular, Laguna)
    PC  = 65,  // → PS (Parking Commercial, Cebu)
    PH  = 66,  // → RC (Penthouse, Parañaque) — no value, formula-derived
    R   = 67,  // → RR (shorthand, legacy)
    A0  = 68,  // → A50 (legacy numbering)
}

impl ClassCode {
    /// Number of defined variants.
    pub const COUNT: usize = 69;

    /// Map non-standard codes to their Annex B equivalent.
    /// Source: Wave 2 classification-code-usage, "6 non-standard codes mapped."
    pub const fn standard_equivalent(self) -> ClassCode {
        match self {
            Self::WC => Self::CR,
            Self::AR => Self::A,
            Self::PC => Self::PS,
            Self::PH => Self::RC,
            Self::R  => Self::RR,
            Self::A0 => Self::A50,
            other => other,
        }
    }

    /// Broad land use category for cross-taxonomy normalization.
    /// Source: Wave 3 rpvara-dual-source-resolution — needed because BIR Annex B
    /// and LGU SMV tiers are structurally incompatible (no automatic crosswalk).
    pub const fn land_use(self) -> LandUseCategory {
        match self.standard_equivalent() {
            Self::RR => LandUseCategory::Residential,
            Self::CR => LandUseCategory::Commercial,
            Self::RC | Self::CC | Self::PS | Self::PH => LandUseCategory::Condominium,
            Self::I => LandUseCategory::Industrial,
            Self::X | Self::GL | Self::GP | Self::CL | Self::APD => LandUseCategory::Institutional,
            Self::DA | Self::A | Self::A1 ..= Self::A50 | Self::AR | Self::A0 => {
                LandUseCategory::Agricultural
            }
            _ => LandUseCategory::Commercial, // WC, R fallthrough
        }
    }

    /// Whether this is an agricultural sub-code (A1-A50).
    pub const fn is_agricultural_sub(self) -> bool {
        matches!(self.standard_equivalent(), Self::A1 ..= Self::A50)
    }

    /// Parse from raw workbook text after normalization.
    /// Handles asterisk stripping, revision number removal, slash splitting.
    /// Source: Wave 2 — 2,739+ rows have footnote-embedded classifications.
    pub fn parse(raw: &str) -> Option<(ClassCode, u8)> {
        // Returns (code, asterisk_count) after normalization pipeline:
        // 1. Strip leading/trailing asterisks → count them
        // 2. Strip embedded revision numbers (e.g., "A50 23*" → "A50")
        // 3. Split on "/" for dual-classification cells
        // 4. Collapse whitespace
        // 5. Lookup in static map
        // (Implementation elided — see parsing pipeline in §6)
        todo!()
    }
}

/// Normalized land use — common denominator across BIR Annex B and LGU SMV.
/// Source: Wave 3 rpvara-dual-source-resolution.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum LandUseCategory {
    Residential,
    Commercial,
    Industrial,
    Agricultural,
    Institutional,
    Condominium,
}
```

### 2.2 Location (`types/location.rs`)

```rust
/// Revenue District Office identifier. 1-125 for geographic RDOs.
/// RDO 126 (Digital Taxation) is function-based and excluded.
/// Source: Wave 3 rdo-jurisdiction-mapping — 124 geographic RDOs confirmed.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct RdoId(pub u8);

/// Municipality/city index. Maps to PSGC 9-digit code externally.
/// u16 sufficient for ~1,913 cities/municipalities.
/// Source: Wave 4 competitive-gap-synthesis — PSGC codes adopted from
/// RealValueMaps' API design (validated pattern).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct MunicipalityId(pub u16);

/// Barangay index. u16 sufficient for ~42,000 barangays nationwide.
/// Source: Wave 3 rdo-jurisdiction-mapping — ~42K entries, ~400 KB.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct BarangayId(pub u16);

/// Interned string index into the StringTable.
/// u32 covers the ~83K unique strings in the dataset.
/// Using u32 (not u16) to allow growth for historical data and RPVARA additions.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct StringIdx(pub u32);

impl StringIdx {
    pub const NONE: Self = Self(u32::MAX);
}
```

### 2.3 Records (`types/record.rs`)

```rust
/// The core zonal value record in binary-indexed form.
/// 20 bytes per record (expanded from Wave 2's 17-byte estimate to accommodate
/// u32 string indices for forward compatibility with RPVARA data growth).
///
/// Source: Wave 2 data-size-estimation — ~690K current records,
/// 12.6 MB raw / 4.4 MB brotli at 17 B/record.
/// At 20 B/record: 13.8 MB raw / ~4.8 MB brotli — still within 5 MB budget.
#[derive(Debug, Clone, Copy)]
#[repr(C, packed)]
pub struct PackedRecord {
    pub rdo_id: u8,            // 1 byte  — RDO (1-125)
    pub municipality: u16,     // 2 bytes — municipality index
    pub barangay: u16,         // 2 bytes — barangay index
    pub street_idx: u32,       // 4 bytes — StringTable index (was 3B, promoted for safety)
    pub vicinity_idx: u32,     // 4 bytes — StringTable index
    pub classification: u8,    // 1 byte  — ClassCode discriminant
    pub zv_centavos: u32,      // 4 bytes — ZV in PHP centavos (max ₱42.9M/sqm)
    pub footnote: u8,          // 1 byte  — asterisk count (0-11; Wave 2: 1-11 observed)
    pub do_idx: u8,            // 1 byte  — index into per-RDO DO table (max 17 revisions)
}
// Total: 20 bytes per record

/// Rich record used in resolution pipeline and API responses.
/// Unpacked from PackedRecord + StringTable + DOTable lookups.
#[derive(Debug, Clone)]
pub struct ZonalValueRecord {
    pub rdo: RdoId,
    pub municipality: MunicipalityId,
    pub barangay: BarangayId,
    pub street: String,
    pub vicinity: String,
    pub classification: ClassCode,
    pub zv_per_sqm_centavos: u64,
    pub footnote_count: u8,
    pub department_order: DepartmentOrder,
}

/// Department Order metadata — stored per-RDO in a compact table.
/// Source: Wave 2 sheet-organization — 30 DOs shared across RDO clusters,
/// unique key is (RDO, DO#), max 17 revisions per RDO.
#[derive(Debug, Clone)]
pub struct DepartmentOrder {
    pub number: String,          // e.g., "DO 022-2021"
    pub effectivity_date: u32,   // Days since epoch (compact date)
    pub status: DoStatus,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DoStatus {
    Current,
    Superseded,
}

/// Data source discriminant for RPVARA dual-source support.
/// Source: Wave 3 rpvara-dual-source-resolution.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DataSource {
    BirZonalValue { rdo_id: RdoId, do_number: String },
    BlgfSmv { lgu_id: MunicipalityId, pvs_version: String },
    Rpis { record_id: String },
}
```

### 2.4 Regime (`types/regime.rs`)

```rust
/// RPVARA transition regime.
/// Source: Wave 3 rpvara-dual-source-resolution — three regimes formalized:
/// - Regime A: BIR ZV active (Section 29(b), three-way max)
/// - Regime B: First year of BLGF SMV (Section 29(c), 6% RPT cap)
/// - Regime C: Post-transition steady state (Section 18(c), two-way max)
///
/// Key finding: zero BLGF-approved SMVs as of March 2026 — virtually all
/// LGUs remain in Regime A.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Regime {
    PreTransition,       // Regime A
    TransitionYear1,     // Regime B
    PostTransition,      // Regime C
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TaxBaseFormula {
    /// Regime A: max(selling_price, zonal_value, existing_fmv)
    ThreeWayMax,
    /// Regime B/C: max(selling_price, smv)
    TwoWayMax,
}

/// Per-LGU regime status. ~1,715 entries × ~64 bytes = ~110 KB.
/// Source: Wave 3 rpvara-dual-source-resolution — trivially fits in WASM.
#[derive(Debug, Clone)]
pub struct LguRegimeEntry {
    pub municipality: MunicipalityId,
    pub smv_status: SmvStatus,
    pub bir_rdo_ids: Vec<RdoId>,
    pub last_verified_days: u32,   // Days since epoch
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SmvStatus {
    NotYetApproved,
    InPreparation(PreparationStage),
    Approved { effectivity_days: u32 },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PreparationStage {
    Drafting,
    PublicConsultation,
    UnderBlgfReview,
    PendingCertification,
}
```

### 2.5 Results (`types/result.rs`, `types/confidence.rs`)

```rust
/// The top-level result returned by the engine for a property lookup.
pub struct LookupResult {
    /// Primary zonal value in PHP centavos per sqm.
    /// None if no value found (Level 6 fallback — per CTA Emiliano/Gamboa).
    pub zv_per_sqm_centavos: Option<u64>,

    /// Which regime applies and the corresponding tax base formula.
    pub regime: Regime,
    pub tax_base_formula: TaxBaseFormula,

    /// Confidence score with component breakdown.
    pub confidence: ConfidenceScore,

    /// The matched record(s) with full metadata.
    pub matched_records: Vec<ZonalValueRecord>,

    /// Classification resolution path taken.
    pub classification_path: ClassificationPath,

    /// Fallback level reached.
    pub fallback_level: FallbackLevel,

    /// Address match details for transparency.
    pub address_match: AddressMatchDetail,

    /// Warnings and legal notes.
    pub warnings: Vec<Warning>,

    /// Data source and authority.
    pub source: DataSource,
    pub department_order: Option<DepartmentOrder>,
}

/// Confidence score: continuous 0.0-1.0 with discrete UI tier.
/// Source: Wave 3 address-matching-algorithms — 5-tier model:
/// HIGH (≥0.85), MEDIUM (0.65-0.84), LOW (0.50-0.64), VERY LOW (<0.50), NO MATCH (0.0).
#[derive(Debug, Clone)]
pub struct ConfidenceScore {
    pub overall: f32,
    pub tier: ConfidenceTier,
    pub breakdown: ConfidenceBreakdown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConfidenceTier {
    High,     // ≥ 0.85
    Medium,   // 0.65–0.84
    Low,      // 0.50–0.64
    VeryLow,  // < 0.50
    NoMatch,  // 0.0
}

#[derive(Debug, Clone)]
pub struct ConfidenceBreakdown {
    pub address_match: f32,        // Street/vicinity match quality
    pub classification: f32,       // Single-code vs multi-code resolution
    pub fallback_penalty: f32,     // Decreases with each fallback level
    pub data_freshness: f32,       // Penalty if DO is >5 years old (38% of schedules)
    pub regime_penalty: f32,       // 0.8x if using BIR ZV in Regime B/C (source mismatch)
}

/// Source: Wave 3 fallback-hierarchy-implementation — 7-level decision tree.
/// Key: this is NOT a linear chain. Level 5 is X-only, Level 5A is separate.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum FallbackLevel {
    /// Exact street + vicinity + classification match. Authority: §6(E) NIRC.
    ExactMatch            = 0,
    /// Same street, different vicinity segment. Authority: DOF DO Rule 3.
    SameStreetDiffVicinity = 1,
    /// Fuzzy/alias street match in same barangay.
    FuzzyStreetMatch       = 2,
    /// "ALL OTHER STREETS" catch-all in barangay. Authority: DOF DO Rule 3.
    BarangayCatchAll       = 3,
    /// Adjacent barangay, same classification. Authority: DOF DO Rules 1 & 2.
    AdjacentBarangay       = 4,
    /// X (Institutional) → nearest CR in same barangay/street. Classification-specific.
    InstitutionalToCR      = 5,
    /// No value found. Engine returns None. Authority: CTA Emiliano/Gamboa.
    NoMatch                = 6,
}

impl FallbackLevel {
    /// Maximum confidence score achievable at this fallback level.
    /// Source: Wave 3 fallback-hierarchy-implementation.
    pub const fn confidence_ceiling(self) -> f32 {
        match self {
            Self::ExactMatch             => 1.0,
            Self::SameStreetDiffVicinity => 0.95,
            Self::FuzzyStreetMatch       => 0.85,
            Self::BarangayCatchAll       => 0.75,
            Self::AdjacentBarangay       => 0.65,
            Self::InstitutionalToCR      => 0.70,
            Self::NoMatch                => 0.0,
        }
    }
}

/// Classification resolution path.
/// Source: Wave 3 classification-resolution-logic — 7 paths.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClassificationPath {
    /// 60% of lookups: only one classification at matched location.
    SingleCode,
    /// 30% of lookups: user selected from multiple available codes.
    UserSelected,
    /// Condo ground floor → CC + 20% per DOF DO footnote.
    CondoGroundFloorCC,
    /// Condo business use → CC upgrade.
    CondoBusinessCC,
    /// PS formula: 60-70% of parent RC/CC, varies by RDO.
    ParkingSlotFormula,
    /// X → nearest CR in same barangay (overlap with FallbackLevel::InstitutionalToCR).
    InstitutionalFallback,
    /// GP with ≥5,000 sqm area threshold gate.
    GovernmentProperty,
}

/// Address match detail for transparency.
#[derive(Debug, Clone)]
pub struct AddressMatchDetail {
    pub mode: AddressMode,
    pub matched_street: Option<String>,
    pub matched_vicinity: Option<String>,
    pub street_match_method: StreetMatchMethod,
    pub pipeline_phase_reached: u8,   // 1-8
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AddressMode {
    /// NCR: cross-street boundary segments (40.7% of records).
    CrossStreet,
    /// Provincial: 7-tier road-proximity hierarchy.
    RoadProximity,
    /// BGC: FAR 1-18 tier matching (544 records, RDO 44 only).
    BgcFarTier,
    /// Condo: building name matching (separate from land).
    CondoBuilding,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StreetMatchMethod {
    ExactNormalized,
    AliasResolution,      // 211+ BIR annotations + Wikipedia renamed streets
    SubstringContainment,
    TokenSetJaccard,
    FuzzyJaroWinkler,     // Threshold 0.90
    CatchAll,             // "ALL OTHER STREETS" (185 entries)
    NoMatch,
}

/// Engine warnings surfaced to the user.
#[derive(Debug, Clone)]
pub enum Warning {
    /// ZV schedule is >5 years old (38% of RDOs per DOF 2024).
    StaleSchedule { do_number: String, years_old: u8 },
    /// RPVARA regime mismatch: using BIR ZV when BLGF SMV should apply.
    RegimeSourceMismatch { expected: Regime, actual_source: DataSource },
    /// Multiple classifications available — user selection required.
    MultipleClassifications { available: Vec<ClassCode> },
    /// Agricultural area threshold: ≥1,000 sqm soft warning (not formally codified).
    AgriculturalAreaThreshold,
    /// Intra-barangay RDO split — street-level disambiguation applied.
    IntraBarangaySplit { barangay: String, rdo_a: RdoId, rdo_b: RdoId },
    /// BARMM LGU with no published RDO assignment.
    NoCoverageBarmmLgu { municipality: String },
    /// Using non-standard classification code (mapped to standard equivalent).
    NonStandardCode { original: String, mapped_to: ClassCode },
}
```

---

## 3. Data Store & Index Design

### 3.1 ZonalValueStore (`data/store.rs`)

The primary data container holds the full current-revision dataset in memory. Designed for O(1) record access by location and O(b + s×k) matching per lookup (Wave 3 performance target: <10ms on mobile WASM).

```rust
/// The primary in-memory data store. Loaded from binary bundle at startup.
/// Source: Wave 2 data-size-estimation — ~690K records, ~4.6 MB brotli total.
pub struct ZonalValueStore {
    /// All current-revision records, sorted by (rdo, municipality, barangay, street_idx).
    records: Vec<PackedRecord>,

    /// Interned strings for streets, vicinities, barangays, municipalities.
    strings: StringTable,

    /// Per-RDO Department Order tables.
    do_tables: Vec<DoTable>,

    /// Hierarchical index: RDO → Municipality → Barangay → record range.
    /// Enables binary search to narrow 690K records to ~160 per barangay.
    location_index: LocationIndex,

    /// Street name index for fuzzy matching within a barangay.
    street_index: StreetIndex,

    /// Per-RDO available classification codes for UI filtering.
    /// Source: Wave 2 classification-code-usage — RDO 113A has 43 codes,
    /// RDO 30 has 5 codes. UI must show only available codes.
    available_codes: AvailableCodesIndex,

    /// Jurisdiction map: barangay → RDO with temporal versioning.
    jurisdiction: JurisdictionMap,

    /// LGU regime registry for RPVARA detection.
    regime_registry: RegimeRegistry,
}
```

### 3.2 StringTable (`data/string_table.rs`)

```rust
/// Interned string storage. Deduplicates the ~83K unique strings across
/// all records. Supports both index→string and normalized-string→index lookup.
///
/// Source: Wave 2 data-size-estimation:
/// - ~23,800 unique streets (~281 KB)
/// - ~16,100 unique vicinities (~280 KB)
/// - ~42,000 unique barangays (~870 KB)
/// - ~1,913 unique municipalities (~28 KB)
/// Total: ~1.46 MB raw.
pub struct StringTable {
    /// Concatenated string data. Individual strings referenced by offset+length.
    data: Vec<u8>,

    /// (offset, length) pairs for each string index.
    offsets: Vec<(u32, u16)>,

    /// Normalized string → index for lookup during matching.
    /// Normalization: uppercase, strip diacritics, collapse whitespace,
    /// remove "ST.", "AVE.", etc. prefixes.
    normalized_map: HashMap<u64, Vec<StringIdx>>,  // FxHash of normalized form
}

impl StringTable {
    pub fn get(&self, idx: StringIdx) -> &str { /* ... */ }

    /// Lookup by normalized form. Returns all matching indices.
    /// Used by the street matching cascade (§4.2).
    pub fn lookup_normalized(&self, normalized: &str) -> &[StringIdx] { /* ... */ }
}
```

### 3.3 LocationIndex (`data/index.rs`)

```rust
/// Hierarchical index for narrowing search scope.
/// Records in `ZonalValueStore::records` are sorted by (rdo, municipality, barangay).
/// This index stores range boundaries for O(1) barangay-level access.
///
/// Source: Wave 3 address-matching-algorithms — pipeline needs to narrow
/// 690K records to ~160/barangay average before string matching begins.
pub struct LocationIndex {
    /// RDO → (start, end) range in sorted records vec.
    rdo_ranges: [RecordRange; 128],  // Indexed by RdoId.0

    /// (RDO, Municipality) → (start, end).
    municipality_ranges: HashMap<(u8, u16), RecordRange>,

    /// (RDO, Municipality, Barangay) → (start, end).
    /// This is the primary lookup: narrows to ~160 records on average.
    barangay_ranges: HashMap<(u8, u16, u16), RecordRange>,
}

#[derive(Debug, Clone, Copy)]
pub struct RecordRange {
    pub start: u32,
    pub end: u32,
}

impl LocationIndex {
    /// Get all records for a specific barangay.
    pub fn records_for_barangay(
        &self, rdo: RdoId, muni: MunicipalityId, brgy: BarangayId,
    ) -> RecordRange { /* ... */ }

    /// Get all records for an entire municipality (for adjacent-barangay fallback).
    pub fn records_for_municipality(
        &self, rdo: RdoId, muni: MunicipalityId,
    ) -> RecordRange { /* ... */ }
}
```

### 3.4 StreetIndex (`data/index.rs`)

```rust
/// Per-barangay street name index for the 5-tier matching cascade.
///
/// Source: Wave 3 address-matching-algorithms:
/// - Tier 1: exact normalized match
/// - Tier 2: alias resolution (211+ annotations)
/// - Tier 3: substring containment
/// - Tier 4: token-set Jaccard
/// - Tier 5: fuzzy Jaro-Winkler (threshold 0.90)
///
/// Index size: ~17.8 MB raw → ~5.2 MB brotli (within WASM budget).
pub struct StreetIndex {
    /// Barangay → list of (normalized_street, record_indices).
    /// Normalized: uppercase, no diacritics, collapsed whitespace.
    by_barangay: HashMap<(u8, u16, u16), Vec<StreetEntry>>,

    /// Global alias table: alternative name → canonical name.
    /// Source: Wave 2 address-vicinity-patterns — 211 former-name annotations.
    /// Augmented with Wikipedia renamed streets database.
    aliases: HashMap<String, Vec<String>>,

    /// Catch-all entries per barangay. "ALL OTHER STREETS" and variants.
    /// Source: Wave 2 — 185 catch-all entries across 31 workbooks.
    catch_alls: HashMap<(u8, u16, u16), Vec<u32>>,  // record indices
}

pub struct StreetEntry {
    pub normalized: String,
    pub tokens: Vec<String>,   // Pre-tokenized for Jaccard
    pub record_indices: Vec<u32>,
}
```

### 3.5 AvailableCodesIndex (`data/index.rs`)

```rust
/// Per-location available classification codes.
/// Source: Wave 2 classification-code-usage — NCR is a 7-code system
/// (98.5% coverage), provincial is a 59-code system.
/// Used for: (1) UI filtering, (2) classification resolution path selection.
pub struct AvailableCodesIndex {
    /// Codes present per RDO. RDO 30 (Binondo): 5 codes. RDO 113A (Davao): 43.
    per_rdo: HashMap<u8, ClassCodeSet>,

    /// Codes present per (RDO, barangay). More granular for resolution.
    per_barangay: HashMap<(u8, u16, u16), ClassCodeSet>,
}

/// Bitset of ClassCode variants. 69 codes fit in a u128.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ClassCodeSet(u128);

impl ClassCodeSet {
    pub fn contains(&self, code: ClassCode) -> bool {
        self.0 & (1u128 << code as u8) != 0
    }
    pub fn insert(&mut self, code: ClassCode) {
        self.0 |= 1u128 << code as u8;
    }
    pub fn iter(&self) -> impl Iterator<Item = ClassCode> { /* ... */ }
    pub fn count(&self) -> u32 { self.0.count_ones() }
}
```

### 3.6 JurisdictionMap (`data/jurisdiction.rs`)

```rust
/// Barangay → RDO jurisdiction mapping with temporal versioning.
/// Source: Wave 3 rdo-jurisdiction-mapping:
/// - ~42K entries, ~400 KB compressed
/// - Multi-RDO cities: Makati (4), QC (4), Manila (6), Cebu (2), Davao (2)
/// - 4 intra-barangay splits requiring street-level disambiguation
/// - RAO 1-2024: 10 EMBO barangays transferred RDO 50 → RDO 44
pub struct JurisdictionMap {
    /// Primary lookup: barangay PSGC → RDO assignment(s).
    /// Most barangays have exactly 1 entry; multi-RDO splits have 2.
    primary: HashMap<u16, SmallVec<[JurisdictionEntry; 1]>>,

    /// Intra-barangay split rules. Only 4 cases exist:
    /// QC: Commonwealth, Culiat, Tandang Sora; Makati: Bel-Air/Salcedo.
    /// Requires street-level disambiguation.
    splits: HashMap<u16, SplitRule>,

    /// BARMM LGUs with no published RDO assignment (8 municipalities, 2024).
    /// Returns Warning::NoCoverageBarmmLgu.
    uncovered: HashSet<u16>,
}

#[derive(Debug, Clone)]
pub struct JurisdictionEntry {
    pub rdo: RdoId,
    pub valid_from: u32,           // Days since epoch
    pub valid_until: Option<u32>,  // None = still current
    pub source: u8,                // Index into static RAO table
}

pub struct SplitRule {
    pub barangay_id: u16,
    pub rdo_a: RdoId,
    pub rdo_b: RdoId,
    /// Street names that fall in rdo_a; all others default to rdo_b.
    pub rdo_a_streets: HashSet<String>,
}
```

### 3.7 RegimeRegistry (`resolution/regime.rs`)

```rust
/// Per-LGU RPVARA regime tracker.
/// Source: Wave 3 rpvara-dual-source-resolution:
/// - ~1,715 LGUs × ~64 bytes = ~110 KB
/// - Zero BLGF-approved SMVs as of March 2026
/// - Updated monthly via data pipeline
pub struct RegimeRegistry {
    entries: HashMap<u16, LguRegimeEntry>,
}

impl RegimeRegistry {
    /// Detect which regime applies for a given municipality and transaction date.
    pub fn detect_regime(
        &self, municipality: MunicipalityId, transaction_date: u32,
    ) -> (Regime, TaxBaseFormula) {
        let entry = self.entries.get(&municipality.0);
        match entry.map(|e| &e.smv_status) {
            Some(SmvStatus::Approved { effectivity_days }) => {
                let days_since = transaction_date.saturating_sub(*effectivity_days);
                if days_since < 365 {
                    (Regime::TransitionYear1, TaxBaseFormula::TwoWayMax)
                } else {
                    (Regime::PostTransition, TaxBaseFormula::TwoWayMax)
                }
            }
            _ => (Regime::PreTransition, TaxBaseFormula::ThreeWayMax),
        }
    }
}
```

---

## 4. Matching Engine

### 4.1 Public API (`lib.rs`)

```rust
/// The primary lookup function. Takes a property query and returns a result.
///
/// Pipeline:
/// 1. Jurisdiction resolution (§4.2)
/// 2. Address matching (§4.3)
/// 3. Classification resolution (§4.4)
/// 4. Fallback hierarchy (§4.5)
/// 5. Regime detection (§4.6)
/// 6. Confidence scoring (§4.7)
/// 7. Result assembly
pub fn lookup(store: &ZonalValueStore, query: &LookupQuery) -> LookupResult {
    // Step 1: Resolve jurisdiction
    let (rdo, jurisdiction_warnings) = resolve_jurisdiction(
        &store.jurisdiction, &query.municipality, &query.barangay, query.street.as_deref(),
    );

    // Step 2: Match address
    let candidates = match_address(
        store, rdo, &query.municipality_id, &query.barangay_id,
        &query.street, query.vicinity.as_deref(),
    );

    // Step 3: Resolve classification
    let classified = resolve_classification(
        &candidates, &query.classification, &query.property_type,
        &store.available_codes,
    );

    // Step 4: Apply fallback hierarchy if needed
    let (record, fallback_level) = apply_fallback(
        store, rdo, &query, &classified,
    );

    // Step 5: Detect RPVARA regime
    let (regime, formula) = store.regime_registry.detect_regime(
        query.municipality_id, query.transaction_date,
    );

    // Step 6: Compute confidence
    let confidence = compute_confidence(
        &candidates, &classified, fallback_level,
        &record, regime,
    );

    // Step 7: Assemble result
    assemble_result(record, regime, formula, confidence, fallback_level, /* ... */)
}

/// Query input from the frontend.
pub struct LookupQuery {
    /// Municipality name or PSGC code.
    pub municipality: String,
    pub municipality_id: Option<MunicipalityId>,

    /// Barangay name or PSGC code.
    pub barangay: String,
    pub barangay_id: Option<BarangayId>,

    /// Street name (optional — if omitted, catch-all match).
    pub street: Option<String>,

    /// Cross-street or road proximity (optional).
    pub vicinity: Option<String>,

    /// Desired classification (optional — if omitted, return all available).
    pub classification: Option<ClassCode>,

    /// Property type for condo-specific resolution.
    pub property_type: PropertyType,

    /// Transaction date for RPVARA regime detection and DO effectivity.
    pub transaction_date: u32,  // Days since epoch
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PropertyType {
    Land,
    Condo { title_type: TitleType },
    ParkingSlot,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TitleType {
    /// Condominium Certificate of Title — composite ZV.
    CCT,
    /// Transfer Certificate of Title — separate land + improvement.
    TCT,
}
```

### 4.2 Jurisdiction Resolution

```rust
/// Resolve municipality + barangay → RDO.
/// Handles: multi-RDO cities, intra-barangay splits, RAO temporal versioning.
/// Source: Wave 3 rdo-jurisdiction-mapping.
fn resolve_jurisdiction(
    map: &JurisdictionMap,
    municipality: &str,
    barangay: &str,
    street: Option<&str>,
) -> (RdoId, Vec<Warning>) {
    let brgy_id = map.lookup_barangay(municipality, barangay);

    // Check for intra-barangay split (4 cases)
    if let Some(split) = map.splits.get(&brgy_id) {
        if let Some(street) = street {
            let normalized = normalize_street(street);
            if split.rdo_a_streets.contains(&normalized) {
                return (split.rdo_a, vec![Warning::IntraBarangaySplit { /* ... */ }]);
            }
        }
        // Default to rdo_b if no street or street not in rdo_a set
        return (split.rdo_b, vec![Warning::IntraBarangaySplit { /* ... */ }]);
    }

    // Standard lookup with temporal versioning
    let entries = &map.primary[&brgy_id];
    let current = entries.iter().find(|e| e.valid_until.is_none())
        .expect("Every barangay must have a current RDO assignment");
    (current.rdo, vec![])
}
```

### 4.3 Address Matching Pipeline

```rust
/// 8-phase address matching pipeline.
/// Source: Wave 3 address-matching-algorithms.
/// Performance: O(b + s×k), <10ms on mobile WASM.
///
/// Phases:
/// 1. Detect address mode (NCR cross-street vs provincial road-proximity vs BGC FAR)
/// 2. Barangay scope reduction (690K → ~160 records)
/// 3. Street matching cascade (5 tiers)
/// 4. Vicinity matching (cross-street boundary or road tier)
/// 5. Condo building matching (separate path)
/// 6. Classification filtering
/// 7. Candidate ranking
/// 8. Result selection
fn match_address(
    store: &ZonalValueStore,
    rdo: RdoId,
    municipality: &MunicipalityId,
    barangay: &BarangayId,
    street: &Option<String>,
    vicinity: Option<&str>,
) -> MatchCandidates {
    // Phase 1: Detect mode
    let mode = detect_address_mode(rdo, vicinity);

    // Phase 2: Scope to barangay
    let range = store.location_index.records_for_barangay(rdo, *municipality, *barangay);
    let records = &store.records[range.start as usize..range.end as usize];

    // Phase 3: Street matching
    let street_matches = match street {
        Some(s) => match_street(&store.street_index, &store.strings, rdo, municipality, barangay, s),
        None => StreetMatchResult::AllStreets(range),
    };

    // Phase 4-8: Vicinity, condo, classification, ranking, selection
    // (Detailed in matching/address.rs, matching/vicinity.rs, matching/condo.rs)
    todo!()
}

/// 5-tier street matching cascade.
/// Source: Wave 3 address-matching-algorithms:
/// Tier 1: exact normalized → Tier 2: alias → Tier 3: substring →
/// Tier 4: token-set Jaccard → Tier 5: Jaro-Winkler (0.90 threshold).
///
/// High threshold prevents false positives among similar Filipino street names:
/// SAN ANTONIO vs SAN AGUSTIN vs SAN ISIDRO.
fn match_street(
    index: &StreetIndex,
    strings: &StringTable,
    rdo: RdoId,
    muni: &MunicipalityId,
    brgy: &BarangayId,
    query_street: &str,
) -> StreetMatchResult {
    let normalized = normalize_street(query_street);
    let key = (rdo.0, muni.0, brgy.0);

    let entries = match index.by_barangay.get(&key) {
        Some(e) => e,
        None => return StreetMatchResult::NoRecords,
    };

    // Tier 1: Exact normalized match
    for entry in entries {
        if entry.normalized == normalized {
            return StreetMatchResult::Exact(entry.record_indices.clone());
        }
    }

    // Tier 2: Alias resolution
    if let Some(aliases) = index.aliases.get(&normalized) {
        for alias in aliases {
            for entry in entries {
                if entry.normalized == *alias {
                    return StreetMatchResult::Alias {
                        records: entry.record_indices.clone(),
                        original: query_street.to_string(),
                        resolved_to: alias.clone(),
                    };
                }
            }
        }
    }

    // Tier 3: Substring containment
    for entry in entries {
        if entry.normalized.contains(&normalized) || normalized.contains(&entry.normalized) {
            return StreetMatchResult::Substring(entry.record_indices.clone());
        }
    }

    // Tier 4: Token-set Jaccard similarity
    let query_tokens: HashSet<&str> = normalized.split_whitespace().collect();
    let mut best_jaccard = 0.0f32;
    let mut best_entry = None;
    for entry in entries {
        let entry_tokens: HashSet<&str> = entry.tokens.iter().map(|s| s.as_str()).collect();
        let intersection = query_tokens.intersection(&entry_tokens).count();
        let union = query_tokens.union(&entry_tokens).count();
        let jaccard = intersection as f32 / union as f32;
        if jaccard > best_jaccard {
            best_jaccard = jaccard;
            best_entry = Some(entry);
        }
    }
    if best_jaccard >= 0.5 {
        if let Some(entry) = best_entry {
            return StreetMatchResult::TokenSet {
                records: entry.record_indices.clone(),
                similarity: best_jaccard,
            };
        }
    }

    // Tier 5: Jaro-Winkler fuzzy match (threshold 0.90)
    let mut best_jw = 0.0f32;
    let mut best_jw_entry = None;
    for entry in entries {
        let jw = jaro_winkler(&normalized, &entry.normalized);
        if jw > best_jw {
            best_jw = jw;
            best_jw_entry = Some(entry);
        }
    }
    if best_jw >= 0.90 {
        if let Some(entry) = best_jw_entry {
            return StreetMatchResult::Fuzzy {
                records: entry.record_indices.clone(),
                similarity: best_jw,
            };
        }
    }

    // No street match — will fall through to catch-all in fallback
    StreetMatchResult::NoMatch
}

enum StreetMatchResult {
    Exact(Vec<u32>),
    Alias { records: Vec<u32>, original: String, resolved_to: String },
    Substring(Vec<u32>),
    TokenSet { records: Vec<u32>, similarity: f32 },
    Fuzzy { records: Vec<u32>, similarity: f32 },
    AllStreets(RecordRange),
    NoRecords,
    NoMatch,
}
```

### 4.4 Classification Resolution

```rust
/// 7-path classification resolution.
/// Source: Wave 3 classification-resolution-logic.
/// Foundation: Aquafresh principle (G.R. 170389) — published classification
/// is authoritative; engine does NOT determine "actual use."
fn resolve_classification(
    candidates: &MatchCandidates,
    requested: &Option<ClassCode>,
    property_type: &PropertyType,
    available_codes: &AvailableCodesIndex,
) -> ClassificationResult {
    let available = candidates.available_codes();

    match (requested, available.count(), property_type) {
        // Path 1: User specified a code and it's available → auto-resolve (60%)
        (Some(code), _, _) if available.contains(*code) => {
            ClassificationResult {
                path: ClassificationPath::SingleCode,
                code: *code,
                confidence: 1.0,
                alternatives: vec![],
            }
        }

        // Path 3: Condo ground floor → CC + 20%
        (_, _, PropertyType::Condo { .. }) if /* ground floor indicator */ false => {
            ClassificationResult {
                path: ClassificationPath::CondoGroundFloorCC,
                code: ClassCode::CC,
                confidence: 0.95,
                alternatives: vec![],
            }
        }

        // Path 5: Parking slot → RDO-specific PS formula
        (_, _, PropertyType::ParkingSlot) => {
            // PS formula varies: 60% Makati, 70% Taguig, 70/100% Mandaluyong
            ClassificationResult {
                path: ClassificationPath::ParkingSlotFormula,
                code: ClassCode::PS,
                confidence: 0.90,
                alternatives: vec![],
            }
        }

        // Path 7: GP with area threshold
        (Some(ClassCode::GP), _, PropertyType::Land) => {
            // Requires area ≥ 5,000 sqm; if not met, downgrade to GL
            ClassificationResult {
                path: ClassificationPath::GovernmentProperty,
                code: ClassCode::GP,
                confidence: 0.85,
                alternatives: vec![ClassCode::GL],
            }
        }

        // Path 1 variant: Only one code at this location → auto-resolve
        (None, 1, _) => {
            let code = available.iter().next().unwrap();
            ClassificationResult {
                path: ClassificationPath::SingleCode,
                code,
                confidence: 1.0,
                alternatives: vec![],
            }
        }

        // Path 2: Multiple codes → return all for user selection (30%)
        (None, n, _) if n > 1 => {
            let codes: Vec<ClassCode> = available.iter().collect();
            ClassificationResult {
                path: ClassificationPath::UserSelected,
                code: codes[0],  // Default to first (RR if available)
                confidence: 0.80,
                alternatives: codes[1..].to_vec(),
            }
        }

        // No matching classification
        _ => ClassificationResult {
            path: ClassificationPath::SingleCode,
            code: requested.unwrap_or(ClassCode::RR),
            confidence: 0.0,
            alternatives: vec![],
        }
    }
}

struct ClassificationResult {
    path: ClassificationPath,
    code: ClassCode,
    confidence: f32,
    alternatives: Vec<ClassCode>,
}
```

### 4.5 Fallback Hierarchy

```rust
/// 7-level fallback decision tree.
/// Source: Wave 3 fallback-hierarchy-implementation.
/// Key: NOT a linear chain. Level 5 (InstitutionalToCR) is X-only branch.
/// Engine NEVER generates values at Level 5A (RAMO 2-91) or Level 6+.
/// Authority: CTA Emiliano (EB 1103), Gamboa (9720).
fn apply_fallback(
    store: &ZonalValueStore,
    rdo: RdoId,
    query: &LookupQuery,
    classified: &ClassificationResult,
) -> (Option<ZonalValueRecord>, FallbackLevel) {
    let muni = query.municipality_id.unwrap();
    let brgy = query.barangay_id.unwrap();

    // Level 0: Exact match (street + vicinity + classification)
    if let Some(record) = find_exact_match(store, rdo, muni, brgy, query, classified.code) {
        return (Some(record), FallbackLevel::ExactMatch);
    }

    // Level 1: Same street, different vicinity segment
    if let Some(record) = find_same_street_any_vicinity(store, rdo, muni, brgy, query, classified.code) {
        return (Some(record), FallbackLevel::SameStreetDiffVicinity);
    }

    // Level 2: Fuzzy/alias street match
    if let Some(record) = find_fuzzy_street(store, rdo, muni, brgy, query, classified.code) {
        return (Some(record), FallbackLevel::FuzzyStreetMatch);
    }

    // Level 3: Barangay catch-all ("ALL OTHER STREETS")
    if let Some(record) = find_catch_all(store, rdo, muni, brgy, classified.code) {
        return (Some(record), FallbackLevel::BarangayCatchAll);
    }

    // Level 4: Adjacent barangay, same classification
    if let Some(record) = find_adjacent_barangay(store, rdo, muni, brgy, classified.code) {
        return (Some(record), FallbackLevel::AdjacentBarangay);
    }

    // Level 5: Institutional (X) → nearest CR (classification-specific branch)
    if classified.code == ClassCode::X {
        if let Some(record) = find_institutional_cr_fallback(store, rdo, muni, brgy, query) {
            return (Some(record), FallbackLevel::InstitutionalToCR);
        }
    }

    // Level 6: No match — return None per CTA Emiliano/Gamboa
    (None, FallbackLevel::NoMatch)
}

/// Adjacent barangay lookup using workbook-ordering heuristic.
/// Source: Wave 3 fallback-hierarchy-implementation — workbook order
/// approximates geographic adjacency for MVP. GIS upgrade path via
/// PSA PSGC boundaries / OpenStreetMap for v2.
fn find_adjacent_barangay(
    store: &ZonalValueStore,
    rdo: RdoId,
    muni: MunicipalityId,
    current_brgy: BarangayId,
    code: ClassCode,
) -> Option<ZonalValueRecord> {
    // Get all barangays in same municipality, ordered by workbook appearance
    let muni_range = store.location_index.records_for_municipality(rdo, muni);
    let records = &store.records[muni_range.start as usize..muni_range.end as usize];

    // Find records in adjacent barangays (±1 in workbook order) with matching classification
    // Priority: same classification in nearest barangay
    for record in records {
        if record.barangay != current_brgy.0
            && record.classification == code as u8
        {
            // Check if this barangay is "adjacent" (within ±2 positions in workbook order)
            // This is the MVP heuristic; GIS boundary check replaces this in v2
            return Some(unpack_record(store, record));
        }
    }
    None
}
```

### 4.6 Confidence Scoring

```rust
/// Compute composite confidence score from match components.
/// Source: Wave 3 address-matching-algorithms + fallback-hierarchy-implementation.
///
/// Formula: overall = min(
///     fallback_level.confidence_ceiling(),
///     address_score × classification_score × freshness_score × regime_score
/// )
fn compute_confidence(
    candidates: &MatchCandidates,
    classified: &ClassificationResult,
    fallback_level: FallbackLevel,
    record: &Option<ZonalValueRecord>,
    regime: Regime,
) -> ConfidenceScore {
    let address_score = match candidates.street_method {
        StreetMatchMethod::ExactNormalized => 1.0,
        StreetMatchMethod::AliasResolution => 0.95,
        StreetMatchMethod::SubstringContainment => 0.85,
        StreetMatchMethod::TokenSetJaccard => 0.75,
        StreetMatchMethod::FuzzyJaroWinkler => 0.70,
        StreetMatchMethod::CatchAll => 0.60,
        StreetMatchMethod::NoMatch => 0.0,
    };

    let classification_score = classified.confidence;

    // Data freshness penalty: Wave 2 found 38% of schedules are >5 years old.
    let freshness_score = match record {
        Some(r) => {
            let age_years = /* compute from DO effectivity date */ 0u8;
            if age_years <= 3 { 1.0 }
            else if age_years <= 5 { 0.95 }
            else if age_years <= 10 { 0.85 }
            else { 0.75 }
        }
        None => 0.0,
    };

    // Regime mismatch penalty: using BIR ZV in Regime B/C gets 0.8x.
    // Source: Wave 3 rpvara-dual-source-resolution.
    let regime_score = match regime {
        Regime::PreTransition => 1.0,
        _ => 0.8,  // BIR ZV as fallback in post-transition
    };

    let raw = address_score * classification_score * freshness_score * regime_score;
    let capped = raw.min(fallback_level.confidence_ceiling());

    let tier = match capped {
        x if x >= 0.85 => ConfidenceTier::High,
        x if x >= 0.65 => ConfidenceTier::Medium,
        x if x >= 0.50 => ConfidenceTier::Low,
        x if x > 0.0   => ConfidenceTier::VeryLow,
        _               => ConfidenceTier::NoMatch,
    };

    ConfidenceScore {
        overall: capped,
        tier,
        breakdown: ConfidenceBreakdown {
            address_match: address_score,
            classification: classification_score,
            fallback_penalty: fallback_level.confidence_ceiling(),
            data_freshness: freshness_score,
            regime_penalty: regime_score,
        },
    }
}
```

---

## 5. Binary Serialization Format

### 5.1 Bundle Format

The WASM bundle uses a custom binary format optimized for compact size and fast deserialization. No schema evolution needed — version changes rebuild the full bundle.

```
ZV Bundle Format v1
====================

Header (16 bytes):
  magic: [u8; 4]       = b"ZVPH"
  version: u16          = 1
  flags: u16            = 0 (reserved)
  record_count: u32     = ~690,000
  string_count: u32     = ~83,000

Section 1: String Table
  For each string:
    length: u16
    data: [u8; length]   (UTF-8)

Section 2: DO Table
  For each RDO (0-124):
    do_count: u8
    For each DO:
      number_idx: u32     (StringIdx)
      effectivity: u32    (days since epoch)
      status: u8          (0=Current, 1=Superseded)

Section 3: Records (sorted by rdo, municipality, barangay, street_idx)
  For each record:
    PackedRecord: [u8; 20]

Section 4: Location Index
  rdo_count: u8
  For each RDO:
    municipality_count: u16
    For each municipality:
      municipality_id: u16
      barangay_count: u16
      For each barangay:
        barangay_id: u16
        record_start: u32
        record_end: u32

Section 5: Available Codes Index
  For each (RDO, barangay):
    codes_bitset: u128

Section 6: Jurisdiction Map
  entry_count: u32
  For each entry:
    barangay_id: u16
    rdo_id: u8
    valid_from: u32
    valid_until: u32  (0 = current)

Section 7: Regime Registry
  entry_count: u16
  For each LGU:
    municipality_id: u16
    smv_status: u8
    effectivity: u32  (if approved)
    rdo_count: u8
    rdo_ids: [u8; rdo_count]
```

### 5.2 Size Budget

Source: Wave 2 data-size-estimation, updated with u32 string indices.

| Component | Raw Size | Brotli | Notes |
|-----------|----------|--------|-------|
| Records (690K × 20B) | 13.8 MB | ~4.0 MB | Increased from 17B to 20B |
| String Table | 1.46 MB | ~0.4 MB | 83K unique strings |
| DO Table | ~15 KB | ~5 KB | ~450 DOs across 124 RDOs |
| Location Index | ~1.0 MB | ~0.2 MB | HashMap serialized as sorted arrays |
| Codes Index | ~0.5 MB | ~0.1 MB | u128 bitsets |
| Jurisdiction Map | ~0.3 MB | ~0.1 MB | ~42K entries |
| Regime Registry | ~0.1 MB | ~0.04 MB | ~1,715 LGUs |
| WASM Engine | ~0.5 MB | ~0.2 MB | Rust → wasm32, optimized |
| **Total** | **~17.7 MB** | **~5.0 MB** | Tight but within budget |

The 5.0 MB brotli estimate is at the edge of the mobile budget. Mitigation strategies:

1. **Tiered loading** (primary): Load NCR-only on first paint (~40K records, ~385 KB brotli), then lazy-load remaining RDOs by Revenue Region (19 chunks × ~230 KB).
2. **String table compression**: Apply dictionary-based compression to the string table specifically (Filipino street names have high substring repetition).
3. **Record pruning**: Strip superseded revisions from the bundle (only keep current DO per municipality).

---

## 6. Special Case Handling

### 6.1 Condo Matching (`matching/condo.rs`)

```rust
/// Condo-specific matching path. Separate from land matching because:
/// 1. Organized by building name, not street address
/// 2. PS (parking) values derive from parent RC/CC via formula
/// 3. Penthouse has 3 different encoding methods across RDOs
/// 4. CCT vs TCT bifurcation changes resolution semantics
///
/// Source: Wave 2 condo-table-structures — 6 NCR patterns + 2 provincial.
fn match_condo(
    store: &ZonalValueStore,
    rdo: RdoId,
    muni: MunicipalityId,
    brgy: BarangayId,
    building_name: &str,
    title_type: TitleType,
) -> CondoMatchResult {
    // 1. Normalize building name (uppercase, strip "TOWER", "RESIDENCES" suffixes)
    // 2. Search condo records in barangay
    // 3. Match by building name (fuzzy — developers use varying names)
    // 4. Resolve PS association (60-70% of parent, varies by RDO)
    // 5. Handle Cebu storey-based catch-all (≤7 vs ≥8 storeys, 44-78% premium)
    // 6. Apply CCT/TCT bifurcation:
    //    - CCT: composite condo ZV directly from schedule
    //    - TCT: separate land + improvement valuation (more complex)
    todo!()
}

/// Per-RDO parking slot formula.
/// Source: Wave 3 classification-resolution-logic:
/// Makati: 60%, Taguig: 70%, Mandaluyong: 70%/100%.
pub struct PsPricingRule {
    pub rdo: RdoId,
    pub formula: PsFormula,
}

pub enum PsFormula {
    /// Single percentage of parent RC or CC value.
    Percentage(u8),  // 60, 70, etc.
    /// Dual percentage: one for RC-associated, another for CC-associated.
    DualPercentage { rc_pct: u8, cc_pct: u8 },
    /// Explicit value in schedule (no formula needed).
    Explicit,
}
```

### 6.2 NCR Cross-Street Parsing (`matching/vicinity.rs`)

```rust
/// Parse NCR cross-street boundary segments.
/// Source: Wave 2 address-vicinity-patterns:
/// - 3 separator types: spaced hyphen (3,725), tight hyphen (2,443), "TO" (419)
/// - 331 cross-streets with 3+ segments create ambiguity
/// - Street name dictionary (~13K entries from Col 0) resolves ambiguity
///
/// Example: "PASONG TAMO - DON BOSCO" → (PASONG TAMO, DON BOSCO)
/// Ambiguous: "SAN ANTONIO - SAN JOSE - RIZAL" → need dictionary to determine
/// if "SAN JOSE" is a middle boundary or part of "SAN JOSE - RIZAL" street.
fn parse_cross_street(
    vicinity: &str,
    street_dictionary: &HashSet<String>,
) -> CrossStreetParsed {
    // 1. Normalize separators: " - " / "-" / " TO " → canonical " - "
    // 2. Split on canonical separator
    // 3. If 2 segments: straightforward (from, to)
    // 4. If 3+ segments: consult street dictionary to find valid street names
    //    among the segment combinations
    // 5. Return parsed boundaries for geometric containment check
    todo!()
}
```

### 6.3 BGC FAR Tier Matching

```rust
/// BGC (Fort Bonifacio, Taguig) uses Floor Area Ratio tiers instead of streets.
/// Source: Wave 2 address-vicinity-patterns — 544 records, RDO 44 only.
/// FAR tiers: 1-18, each with different ZV per classification.
///
/// The user must know their property's FAR to get a precise lookup.
/// If unknown, return all FAR tiers for the barangay with a warning.
fn match_bgc_far(
    store: &ZonalValueStore,
    brgy: BarangayId,
    far: Option<u8>,
    code: ClassCode,
) -> Vec<ZonalValueRecord> {
    // Filter records where vicinity matches "FAR {n}" pattern
    todo!()
}
```

### 6.4 Provincial Road-Proximity Matching

```rust
/// Provincial road-proximity tier matching.
/// Source: Wave 2 address-vicinity-patterns:
/// 7 tiers: National Highway → Provincial Road → Municipal Road →
/// Barangay Road → 50m Inward → Interior → Watershed.
/// ZV ranges: ₱100–₱35,000.
///
/// Matching: user specifies road type or proximity; engine maps to tier.
/// If unspecified, return all tiers with ZV range.
fn match_road_proximity(
    records: &[PackedRecord],
    store: &ZonalValueStore,
    road_type: Option<RoadTier>,
) -> Vec<(RoadTier, Vec<ZonalValueRecord>)> {
    todo!()
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum RoadTier {
    NationalHighway = 1,
    ProvincialRoad  = 2,
    MunicipalRoad   = 3,
    BarangayRoad    = 4,
    FiftyMeterInward = 5,
    Interior        = 6,
    Watershed       = 7,
}
```

---

## 7. WASM Interface (`lib.rs` with `#[cfg(target_arch = "wasm32")]`)

```rust
#[cfg(target_arch = "wasm32")]
mod wasm {
    use wasm_bindgen::prelude::*;

    /// Initialize the engine from a binary bundle.
    /// Called once on page load. Deserializes ~5 MB brotli bundle.
    #[wasm_bindgen]
    pub fn init(bundle: &[u8]) -> Result<(), JsValue> {
        let store = ZonalValueStore::from_binary(bundle)
            .map_err(|e| JsValue::from_str(&e.to_string()))?;
        // Store in thread-local or static
        Ok(())
    }

    /// Perform a zonal value lookup. Input/output as JSON strings
    /// for TypeScript interop. No property data leaves the browser.
    #[wasm_bindgen]
    pub fn lookup(query_json: &str) -> String {
        let query: LookupQuery = serde_json::from_str(query_json)
            .expect("Invalid query JSON");
        let result = crate::lookup(&STORE, &query);
        serde_json::to_string(&result).unwrap()
    }

    /// Get available classifications for a location.
    /// Used by frontend to populate dropdown before lookup.
    #[wasm_bindgen]
    pub fn available_codes(rdo: u8, municipality: u16, barangay: u16) -> String {
        let codes = STORE.available_codes.for_barangay(rdo, municipality, barangay);
        serde_json::to_string(&codes.iter().collect::<Vec<_>>()).unwrap()
    }

    /// Get list of municipalities for an RDO.
    #[wasm_bindgen]
    pub fn municipalities_for_rdo(rdo: u8) -> String {
        // Used for cascading dropdowns in UI
        todo!()
    }

    /// Get list of barangays for a municipality.
    #[wasm_bindgen]
    pub fn barangays_for_municipality(rdo: u8, municipality: u16) -> String {
        todo!()
    }
}
```

---

## 8. Design Decision Traceability

Every major design decision traces to specific wave findings:

| # | Decision | Source | Finding |
|---|----------|--------|---------|
| 1 | u8 ClassCode enum (69 variants) | Wave 2 classification-code-usage | 62 unique codes in 31 workbooks + 6 non-standard + 1 spare |
| 2 | 20-byte PackedRecord (up from 17) | Wave 2 data-size-estimation | u32 string indices for RPVARA growth headroom; still within 5 MB brotli |
| 3 | Dual address mode (NCR cross-street vs provincial road-proximity) | Wave 2 address-vicinity-patterns | 40.7% cross-street, 59.3% road-proximity — fundamentally different models |
| 4 | 0.90 Jaro-Winkler threshold | Wave 3 address-matching-algorithms | Prevents SAN ANTONIO/SAN AGUSTIN false positives among Filipino street names |
| 5 | 7-level fallback decision tree (not linear chain) | Wave 3 fallback-hierarchy-implementation | Level 5 is X-only branch; engine returns None at Level 6 per CTA rulings |
| 6 | Three-regime RPVARA model | Wave 3 rpvara-dual-source-resolution | Regime A (BIR ZV), B (SMV year 1), C (SMV steady state) — zero approved SMVs as of March 2026 |
| 7 | ClassCodeSet as u128 bitset | Wave 2 classification-code-usage | 69 codes fit in u128; O(1) contains/insert; NCR is 7-code vs provincial 59-code |
| 8 | Workbook-order barangay adjacency (MVP) | Wave 3 fallback-hierarchy-implementation | GIS boundary data not reliably available (PhilGIS defunct, OSM PH incomplete outside NCR) |
| 9 | Separate condo matching path | Wave 2 condo-table-structures | 6 NCR + 2 provincial layout patterns; PS formula varies 60-70% by RDO; 3 penthouse encodings |
| 10 | PSGC codes as canonical location identifier | Wave 4 realvaluemaps-approach | RealValueMaps' planned PSGC integration validated as architecturally sound |
| 11 | No automatic BIR↔LGU classification crosswalk | Wave 3 rpvara-dual-source-resolution | BIR Annex B (63 functional codes) and LGU SMV (numeric tier R1-R12) are structurally incompatible |
| 12 | Tiered bundle loading (NCR first) | Wave 2 data-size-estimation | NCR = 40K records (~385 KB brotli); prioritized because highest demand |
| 13 | API-first design (WASM for privacy, API for integrators) | Wave 4 competitive-gap-synthesis | Zero platforms offer API; identified as 6-12 month first-mover window |
| 14 | Integer arithmetic (centavos) | Wave 2 data-size-estimation | BIR data is inherently integer; avoids floating-point rounding in tax computation |
| 15 | Per-section footnote legend parsing | Wave 2 footnote-convention-mapping | Legends NOT inherited across revision sheets; `*` meaning reverses between regions |
| 16 | Street alias table (211+ entries) | Wave 2 address-vicinity-patterns | BIR workbooks contain "(formerly ...)" annotations enabling alias resolution |
| 17 | Pluggable SourceParser trait | Wave 3 rpvara-dual-source-resolution | BLGF SMV format unknown; RPIS may provide API; parser must be source-agnostic |
| 18 | DO effectivity tracking per record | Wave 4 housal-data-model | Housal shows DO# but no effectivity date — legal gap we solve; CTA rulings require date tracking |

---

## 9. Performance Targets

| Metric | Target | Basis |
|--------|--------|-------|
| Exact match latency | < 1 ms | O(1) index lookup + O(~160) barangay scan |
| Fuzzy match latency | < 10 ms | 5-tier cascade over ~160 records per barangay |
| Full fallback (7 levels) | < 50 ms | Worst case: all 7 levels, adjacent barangay scan |
| Bundle deserialization | < 500 ms | 5 MB brotli → ~17 MB in-memory parse |
| Bundle download (4G) | < 10 s | ~5 MB brotli, or ~400 KB NCR-first tier |
| Memory footprint | < 30 MB | Records + indices + string table + WASM heap |

---

## 10. Open Questions for Implementation

1. **String table encoding**: Should normalized forms be stored alongside originals (2× space but avoids re-normalization at query time), or computed on-the-fly?
2. **Barangay adjacency v2**: When GIS data becomes available (PSA PSGC boundaries or OSM), how to integrate without bundle size explosion?
3. **Incremental updates**: Can the binary bundle support delta updates (new DOs only) or must it be rebuilt entirely? Monthly full rebuild is acceptable for v1.
4. **WASM threading**: Can the street matching cascade benefit from `wasm-bindgen-rayon` for parallel barangay scans? Likely unnecessary given <10ms single-threaded target.
5. **Historical data API**: Server-side historical queries (2.97M records, 18 MB brotli) need a separate API design — not part of the WASM bundle.
