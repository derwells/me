# Classification Resolution Logic — Deep Dive

**Wave:** 3 — Resolution Logic Deep-Dive
**Date:** 2026-03-03
**Aspect:** `classification-resolution-logic`
**Verification:** Cross-checked against 15+ independent sources via verification subagent. All 8 core claims verified (6 CONFIRMED, 2 PARTIALLY CONFIRMED).
**Prior art:** `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md` Step 4, `analysis/classification-code-usage.md`, `analysis/cta-zonal-rulings.md`, `analysis/rmo-31-2019-annexes.md`

---

## Summary

Classification code resolution determines which of 63+ BIR classification codes applies to a given property for zonal value lookup. This analysis formalizes the resolution logic as a decision tree with 7 resolution paths, 5 special-case rules, and 4 area-threshold gates — all producing Rust-implementable pseudocode.

**Key finding:** The Aquafresh principle (G.R. No. 170389, 2010) dramatically simplifies the engine's classification resolution. The published schedule classification is authoritative — the engine does NOT determine "actual use." Classification resolution is primarily a **selection problem** (user picks from schedule-listed options) rather than a **determination problem** (engine infers from property characteristics). The non-deterministic gate is narrower than originally estimated: only ~5% of lookups require user judgment (mixed-classification streets and condo business-use scenarios).

**7 resolution paths formalized:**
1. **Single-classification match** — street/vicinity has one classification → auto-resolve (estimated 60% of lookups)
2. **Multi-classification selection** — street/vicinity has 2+ classifications → user selects (estimated 30%)
3. **Condo ground floor rule** — RC ground floor → CC + 20% (computed, not from schedule)
4. **Condo business use rule** — RC unit used for business → CC + 20% (user-declared)
5. **PS fallback formula** — no PS in schedule → 60-70% of RC/CC value (RDO-specific)
6. **Institutional fallback** — X code with no value → nearest CR in same barangay/street
7. **GP area threshold gate** — GP requires ≥5,000 sqm → below threshold, reclassify

---

## 1. The Aquafresh Foundation

### Core Principle

**CIR v. Aquafresh Seafoods, Inc.** (G.R. No. 170389, October 20, 2010) established the bedrock rule:

> "Petitioner [BIR] cannot unilaterally change the zonal valuation of such properties to 'commercial' without first conducting a re-evaluation of the zonal values as mandated under Section 6(E) of the NIRC."

**Implication for the engine:** The classification code comes from the published schedule, not from any determination of "actual use." If the schedule says RR for a street, the engine returns the RR value — period.

### Predominant Use Rule — Narrow Scope

The "predominant use" rule from DOF Local Assessment Regulations No. 1-92 has a narrow scope for BIR zonal value purposes:

> "The application of the rule of assigning zonal values based on the 'predominant use of property' only applies when the property is located in an area or zone where the properties are **not yet classified** and their zonal values are **not yet determined**."
> — BIR Ruling No. 041-2001 (cited in Aquafresh)

**When it applies:** Only for areas with NO published classification in the current schedule — a gap-filling mechanism.

**When it does NOT apply:** Any area where the schedule already assigns a classification. The existing classification prevails regardless of actual use.

### Commercial Override Footnote

BIR zonal value schedules contain a standard nationwide footnote:

> "ALL REAL PROPERTIES, REGARDLESS OF ACTUAL USE, LOCATED IN A STREET/BARANGAY/ZONE, THE USE OF WHICH ARE PREDOMINANTLY COMMERCIAL SHALL BE CLASSIFIED AS 'COMMERCIAL' FOR PURPOSES OF ZONAL VALUATION"

**Important:** This footnote is applied by the STCRPV *when establishing* the schedule — it's not a runtime rule for the engine. By the time the schedule is published, streets in predominantly commercial areas are already classified as CR. The engine simply reads the published classification.

**Engine implication:** The commercial override is pre-baked into the published data. No engine logic needed.

---

## 2. Classification Resolution Decision Tree

### Input Model

```rust
/// User-provided classification context
pub struct ClassificationInput {
    /// Property type: Land, Condo, or ParkingSlot
    pub property_type: PropertyType,
    /// Land area in sqm (required for land, optional for condo)
    pub land_area_sqm: Option<f64>,
    /// Floor level (for condo ground floor rule)
    pub floor_level: Option<FloorLevel>,
    /// Is the condo unit used for business? (user-declared)
    pub is_business_use: Option<bool>,
    /// Title type: CCT (Condominium Certificate) or TCT (Transfer Certificate)
    pub title_type: Option<TitleType>,
    /// User-selected classification code (when multiple options exist)
    pub user_selected_code: Option<ClassCode>,
}

pub enum PropertyType {
    Land,
    Condo,
    ParkingSlot,
}

pub enum FloorLevel {
    GroundFloor,
    UpperFloor(u8),
    Penthouse,
}

pub enum TitleType {
    CCT, // Condominium Certificate of Title — land+improvement treated as one
    TCT, // Transfer Certificate of Title — land and improvement valued separately
}
```

### Decision Tree (Full)

```
classify(input, schedule_matches) → ClassificationResult
│
├─ Is property_type == ParkingSlot?
│  ├─ YES → Path 5: PS Resolution
│  │  ├─ Does schedule have explicit PS entry for this building/location?
│  │  │  ├─ YES → return PS value from schedule
│  │  │  └─ NO → return PS_FALLBACK (60-70% of parent RC/CC value, per RDO rule)
│  │  └─ PS percentage varies by RDO:
│  │     ├─ RDO 47-50 (Makati): 60% of unit sold value
│  │     ├─ RDO 44 (Taguig): 70% of RC or CC, whichever is higher
│  │     ├─ RDO 41 (Mandaluyong): 70% if not in CCT; 100% if in CCT
│  │     └─ Default: 60% of RC/CC value (most conservative)
│  │
├─ Is property_type == Condo?
│  ├─ YES → Condo Classification Path
│  │  ├─ Is floor_level == GroundFloor?
│  │  │  ├─ YES → Path 3: Ground Floor CC Rule
│  │  │  │  └─ return CC with value = RC_value × 1.20
│  │  │  └─ NO → continue
│  │  ├─ Is is_business_use == true?
│  │  │  ├─ YES → Path 4: Business Use Upgrade
│  │  │  │  └─ return CC with value = RC_value × 1.20
│  │  │  └─ NO → continue
│  │  ├─ Is floor_level == Penthouse?
│  │  │  ├─ YES → Penthouse Resolution (3 encoding methods)
│  │  │  │  ├─ PH code in schedule → return PH value
│  │  │  │  ├─ "(Penthouse)" suffix entry → return that value
│  │  │  │  └─ Footnote formula → return CC_value × 1.10 or RC_value × 1.20
│  │  │  └─ NO → continue
│  │  └─ Does schedule have RC/CC entries for this building?
│  │     ├─ YES, single code → Path 1: Auto-resolve
│  │     ├─ YES, both RC and CC → Path 2: User selects
│  │     └─ NO → fall through to land classification logic
│  │
├─ Is property_type == Land?
│  └─ Land Classification Path
│     ├─ How many classification codes does the schedule list for this
│     │  street/vicinity/barangay match?
│     │  ├─ 0 codes → return NO_MATCH (no classification in schedule)
│     │  ├─ 1 code → Path 1: Auto-resolve
│     │  │  └─ Apply area threshold gates before returning:
│     │  │     ├─ If code == GP and area < 5,000 sqm → WARN: below GP threshold
│     │  │     ├─ If code ∈ {A, A1..A50} and area < 1,000 sqm → WARN: below agri threshold
│     │  │     └─ Otherwise → return matched value
│     │  └─ 2+ codes → Path 2: Multi-classification selection
│     │     └─ Present all listed codes to user with values
│     │        ├─ If user_selected_code is set → validate against available codes
│     │        ├─ If not set → return list for UI presentation
│     │        └─ Apply area threshold gates on selected code
│     │
│     └─ Special case: X (Institutional) with no value?
│        └─ Path 6: Institutional Fallback
│           └─ return nearest CR value in same barangay/street
│              (per BIR DO footnotes and RAMO 2-91)
```

---

## 3. Resolution Paths — Detailed Specification

### Path 1: Single-Classification Auto-Resolve (60% of lookups)

**When:** The matched street/vicinity row has exactly one classification code.

**Logic:** Return the value directly. No user input needed.

**Worked example:**
- **Input:** Property at "INTERIOR LOT", Barangay Plainview, Mandaluyong (RDO 41)
- **Schedule data:** INTERIOR LOT / Plainview / RR / ₱32,000
- **Result:** RR, ₱32,000/sqm, confidence HIGH

This is the simplest and most common case. Most barangay catch-all entries ("ALL OTHER STREETS IN [BARANGAY]") have a single classification.

### Path 2: Multi-Classification Selection (30% of lookups)

**When:** The matched street/vicinity has 2+ classification codes listed (e.g., both RR and CR entries for the same street).

**Logic:** Present all options to the user. The user selects based on their Tax Declaration or property actual use.

**Worked example:**
- **Input:** Property on "SHAW BLVD", Barangay Plainview, Mandaluyong (RDO 41)
- **Schedule data:**
  - SHAW BLVD / Plainview / RR / ₱120,000
  - SHAW BLVD / Plainview / CR / ₱150,000
- **Result:** Present both options. User selects based on Tax Declaration classification.
- **If Tax Declaration says "Residential"** → RR, ₱120,000/sqm
- **If Tax Declaration says "Commercial"** → CR, ₱150,000/sqm

**Aquafresh constraint:** The engine presents only classifications that appear in the published schedule for this location. It does NOT offer classifications that don't exist in the schedule, even if the user's Tax Declaration shows a different classification.

**Common multi-classification patterns (from Wave 2 data):**

| Pattern | Example | Frequency |
|---------|---------|-----------|
| RR + CR (land, street frontage vs interior) | Shaw Blvd, Mandaluyong | Very common |
| RC + CC + PS (condo building) | BGC condos, Taguig | Very common |
| RR + CR + I (mixed-use zone) | Industrial-adjacent streets | Occasional |
| RR + CR + X (institutional area) | Near schools/hospitals | Occasional |
| A1 + A2 + A4 + A50 (provincial multi-crop) | Pangasinan barangays | Common in provincial |

### Path 3: Condo Ground Floor CC Rule

**When:** Property is a condo unit on the ground floor of a residential condominium building.

**Rule (from BIR DO footnotes, confirmed across RDO 44, 47-50, 43, 83):**

> "THE GROUND FLOOR OF THE RESIDENTIAL CONDOMINIUM SHALL BE CLASSIFIED AS COMMERCIAL AND TWENTY PERCENT (20%) OF THE ESTABLISHED VALUE SHALL BE ADDED THERETO."

**Logic:**
```rust
fn resolve_ground_floor_condo(rc_value: u32) -> ClassificationResult {
    let cc_value = (rc_value as f64 * 1.20).round() as u32;
    ClassificationResult {
        code: ClassCode::CC,
        value_per_sqm: cc_value,
        source: ValueSource::ComputedFromRule {
            rule: "Ground floor RC → CC + 20%",
            base_code: ClassCode::RC,
            base_value: rc_value,
            markup_pct: 20,
        },
        confidence: Confidence::High,
    }
}
```

**Worked example:**
- **Input:** Ground floor unit, "SHANG RESIDENCES AT WACK WACK", Barangay Addition Hills, Mandaluyong (RDO 41)
- **Schedule data:** RC value for this building = ₱175,000/sqm
- **Result:** CC, ₱210,000/sqm (₱175,000 × 1.20), computed from rule

**Edge case:** If the building already has explicit CC entries for ground floor units, use the schedule value instead of computing. The rule is a fallback for when ground floor CC is not explicitly listed.

### Path 4: Condo Business Use Upgrade

**When:** A unit in a residential condo (RC) project is used for business purposes.

**Rule (from BIR DO footnotes):**

> "Any unit in a purely Residential Condominium (RC) project found to be used in business shall be classified as Commercial Condominium (CC) and twenty percent (20%) of the established value shall be added thereto."

**Logic:** Identical to Path 3 computation. The trigger is different: user declares `is_business_use = true` for an RC-classified unit.

**Engine design note:** The engine should prompt "Is this unit used for business/commercial purposes?" when the user selects an RC classification for a condo unit. This is the one case where "actual use" matters — but it's user-declared, not engine-determined.

**Aquafresh reconciliation:** This rule does NOT contradict Aquafresh. The ground floor and business-use rules are published in the schedule itself (as footnotes). They are part of the "published classification system," not unilateral BIR reclassification. The user self-declares the business use; the BIR does not inspect and override.

### Path 5: PS Fallback Formula

**When:** No explicit PS (Parking Slot) zonal value exists in the schedule for a building/location.

**Rule (from BIR DO footnotes, varies by RDO):**

| RDO | PS Fallback Rule | Source |
|-----|-----------------|--------|
| RDO 47-50 (Makati) | 60% of unit sold value | "IF NO ZONAL VALUE HAS BEEN PRESCRIBED FOR PARKING SLOTS, THE VALUE SHOULD BE 60% OF THE AMOUNT OF THE UNIT SOLD" |
| RDO 44 (Taguig) | 70% of RC or CC value, whichever is higher | "All parking slots of condominiums are valued at 70% of Residential or Commercial value, whichever is higher" |
| RDO 41 (Mandaluyong) | 70% if not in CCT; 100% if in CCT | CCT-incorporated PS uses full condo unit value |
| Default | 60% of RC/CC value | Conservative default |

**Logic:**
```rust
fn resolve_ps_fallback(
    rdo_id: u8,
    parent_rc_value: Option<u32>,
    parent_cc_value: Option<u32>,
    title_type: Option<TitleType>,
) -> ClassificationResult {
    let ps_pct = match rdo_id {
        44 => 70,  // Taguig: 70% of higher of RC/CC
        41 => match title_type {
            Some(TitleType::CCT) => 100,  // Mandaluyong CCT: full value
            _ => 70,                       // Mandaluyong non-CCT: 70%
        },
        _ => 60,  // Default: 60%
    };

    let base_value = match rdo_id {
        44 => parent_rc_value.max(parent_cc_value),  // Taguig: higher of RC/CC
        _ => parent_rc_value.or(parent_cc_value),     // Others: RC preferred
    };

    let ps_value = base_value
        .map(|v| (v as f64 * ps_pct as f64 / 100.0).round() as u32);

    ClassificationResult {
        code: ClassCode::PS,
        value_per_sqm: ps_value.unwrap_or(0),
        source: ValueSource::ComputedFromRule {
            rule: &format!("PS fallback: {}% of parent RC/CC", ps_pct),
            base_code: ClassCode::RC,
            base_value: base_value.unwrap_or(0),
            markup_pct: -(100 - ps_pct as i32),
        },
        confidence: Confidence::Medium,
    }
}
```

**Note on Makati's "unit sold" formula:** The East Makati rule uses "60% of the amount of the unit sold" — this requires the selling price as input, not the zonal value. The engine should use the zonal value (RC/CC) as the base in the absence of selling price data.

### Path 6: Institutional Fallback

**When:** Property has X (Institutional) classification but no X zonal value exists in the schedule for that location.

**Rule (from BIR DO footnotes and RAMO 2-91):**

> "IF NO ZONAL VALUE HAS BEEN PRESCRIBED, THE COMMERCIAL VALUE OF THE PROPERTY NEAREST TO THE INSTITUTION, WITHIN THE SAME BARANGAY AND STREET SHALL BE USED."

**Logic:**
```rust
fn resolve_institutional_fallback(
    barangay_id: u16,
    street_idx: u32,
    index: &ZonalIndex,
) -> ClassificationResult {
    // Step 1: Find CR value for same street in same barangay
    if let Some(cr_value) = index.find_cr_value(barangay_id, Some(street_idx)) {
        return ClassificationResult {
            code: ClassCode::X,
            value_per_sqm: cr_value,
            source: ValueSource::InstitutionalFallback {
                fallback_code: ClassCode::CR,
                same_street: true,
            },
            confidence: Confidence::Medium,
        };
    }

    // Step 2: Find nearest CR value in same barangay (any street)
    if let Some(cr_value) = index.find_nearest_cr_value(barangay_id) {
        return ClassificationResult {
            code: ClassCode::X,
            value_per_sqm: cr_value,
            source: ValueSource::InstitutionalFallback {
                fallback_code: ClassCode::CR,
                same_street: false,
            },
            confidence: Confidence::Low,
        };
    }

    // Step 3: No CR value in barangay → return NO_MATCH
    ClassificationResult::no_match("X classification — no CR value available in barangay")
}
```

**Worked example:**
- **Input:** Church property in Barangay San Antonio, Makati (RDO 47)
- **Schedule data:** San Antonio has X entries with values → use directly
- **Alternative:** If San Antonio had no X value → use the CR value for the nearest street in San Antonio

**CR universality guarantees this works:** Per Wave 2 analysis, CR is the only code present in all 31 sampled RDOs (31/31). Every barangay with any zonal data has a CR value. The institutional fallback to CR will always find a value at the barangay level.

### Path 7: GP Area Threshold Gate

**When:** Property matches a GP (General Purpose) classification, but the land area is below 5,000 sqm.

**Rule (from Annex B, RMO 31-2019):**

> "General Purpose (GP): Rawland, undeveloped and underdeveloped area which has potential for development... **Must not be less than 5,000 square meters.**"

**Logic:**
```rust
fn apply_area_threshold_gate(
    code: ClassCode,
    area_sqm: Option<f64>,
) -> ThresholdResult {
    match code {
        ClassCode::GP => {
            match area_sqm {
                Some(area) if area < 5000.0 => ThresholdResult::BelowThreshold {
                    code,
                    threshold_sqm: 5000.0,
                    actual_sqm: area,
                    recommendation: "Property below 5,000 sqm GP threshold. \
                        Classify based on actual/predominant use (typically RR or CR).",
                },
                None => ThresholdResult::AreaUnknown {
                    code,
                    threshold_sqm: 5000.0,
                    warning: "GP classification requires ≥5,000 sqm. \
                        Provide land area to validate.",
                },
                _ => ThresholdResult::Passes,
            }
        }
        ClassCode::A | ClassCode::A1 ..= ClassCode::A50 => {
            // Agricultural 1,000 sqm threshold — operational practice,
            // NOT formally codified in Annex B. Warn but don't block.
            match area_sqm {
                Some(area) if area < 1000.0 => ThresholdResult::SoftWarning {
                    code,
                    threshold_sqm: 1000.0,
                    actual_sqm: area,
                    warning: "Property below 1,000 sqm. Some RDOs reclassify \
                        small agricultural parcels as residential. \
                        The published schedule classification still governs \
                        (Aquafresh principle).",
                },
                _ => ThresholdResult::Passes,
            }
        }
        _ => ThresholdResult::Passes,
    }
}
```

**Verification note on the 1,000 sqm agricultural threshold:** The verification subagent found this threshold referenced in practitioner sources but could NOT locate it in any primary BIR issuance, the NIRC, or RMO 31-2019 Annex B. It appears to be operational practice used by RDOs and local assessors rather than a formally codified rule. The engine should issue a soft warning but NOT block the lookup — the Aquafresh principle means the published schedule classification governs regardless.

---

## 4. Edge Cases

### 4.1 Mixed-Use Properties — DOF LAR 1-92 Analysis

DOF Local Assessment Regulations No. 1-92 establishes the predominant use rule for mixed-use areas:

> "In an area of mixed land uses, such as residential with commercial or industrial, the predominant use of the lands in that area shall govern the classification, valuation and assessment thereof."

And for dual-use buildings:

> "A building used both for residential and commercial or industrial purposes shall be classified and valued... on the basis of the predominant use of the building."

**Critical distinction (from CBAA jurisprudence):**
- **"Predominant use" of the area** → governs classification and valuation (determines which code applies)
- **"Actual use" of the specific property** → determines assessment level (percentage applied to market value for RPT)

These are two different concepts. For BIR zonal value purposes, **predominant use is pre-baked into the published schedule**. The STCRPV applies the predominant use rule when establishing classifications. By the time the engine reads the schedule, mixed-use areas have already been classified.

**Engine implication:** No mixed-use resolution logic needed at runtime. The published classification already reflects predominant use. If a property is on a street with both RR and CR entries, the user selects based on their specific property's Tax Declaration — this is Path 2 (multi-classification selection), not a predominant use determination.

### 4.2 Agricultural Conversion/Reclassification Timing

**Scenario:** An LGU reclassifies agricultural land to residential/commercial (via DAR conversion). The BIR zonal schedule still shows the agricultural classification.

**Ruling (Aquafresh principle applied):**
- The BIR classification does NOT change automatically upon LGU reclassification
- The BIR schedule change requires a formal revision via STCRPV → TCRPV → ECRPV → DOF DO → publication → 15-day effectivity
- Until the revision is published, the existing agricultural classification governs
- With 38% of schedules outdated (DOF 2024), this lag is common

**Engine logic:**
```rust
fn handle_conversion_scenario(
    schedule_code: ClassCode,  // What the published schedule says (e.g., A1)
    user_claims_converted: bool,
) -> ClassificationResult {
    // Always return the published schedule classification
    let mut result = ClassificationResult::from_schedule(schedule_code);

    if user_claims_converted && schedule_code.is_agricultural() {
        result.add_advisory(
            "The published BIR schedule classifies this property as agricultural. \
             If the property has been converted by the LGU/DAR, the higher \
             classification (residential/commercial) will apply at the next \
             BIR zonal schedule revision. For current tax computation, \
             the published classification governs (CIR v. Aquafresh, G.R. 170389)."
        );
    }

    result
}
```

**Practical impact:** The tax delta can be massive. Agricultural ZVs range ₱40-₱9,250/sqm while RR in the same area might be ₱5,000-₱35,000/sqm. Conversion creates a timing gap where the taxpayer may benefit from the lower agricultural rate until the next BIR revision — this is legally correct behavior, not a bug.

### 4.3 Legacy Code Mapping (Historical Revisions)

Pre-RMO 31-2019 revisions used non-standard agricultural sub-codes with different meanings:

| Code | 1990 Pangasinan (DO 6-90) | 2023 Standard (DO 015-2023) |
|------|---------------------------|----------------------------|
| A1 | Unirrigated Riceland | Riceland Irrigated |
| A2 | Mango Land | Riceland Unirrigated |

**Engine logic:** For historical revision lookups (matching transaction date to older DOs), the engine must read the per-sheet classification legend and map codes contextually.

```rust
/// Per-revision classification legend
pub struct ClassificationLegend {
    /// DO number this legend applies to
    pub department_order: String,
    /// Map from raw code string to (standardized ClassCode, local description)
    pub code_map: HashMap<String, (ClassCode, String)>,
}

fn resolve_legacy_code(
    raw_code: &str,
    legend: Option<&ClassificationLegend>,
    do_date: NaiveDate,
) -> ClassCode {
    // For post-2019 revisions: standard Annex B mapping
    if do_date >= NaiveDate::from_ymd(2019, 6, 18) {
        return normalize_standard_code(raw_code);
    }

    // For pre-2019: use per-sheet legend if available
    if let Some(legend) = legend {
        if let Some((code, _desc)) = legend.code_map.get(raw_code) {
            return *code;
        }
    }

    // Fallback: standard mapping with LOW confidence warning
    normalize_standard_code(raw_code)
}
```

**Scope limitation:** Legacy code mapping is only relevant for historical transaction date lookups. For current-revision lookups (the primary use case), all sampled workbooks (31/31) use standard Annex B codes consistently.

### 4.4 Non-Standard Code Resolution

Six non-standard codes were found in actual workbook data (from Wave 2 `classification-code-usage.md`):

```rust
/// Non-standard code mapping table
const NON_STANDARD_CODE_MAP: &[(&str, ClassCode, &str)] = &[
    ("WC", ClassCode::CR, "Warehouse/Commercial — RDO 29 Tondo"),
    ("AR", ClassCode::A,  "Agricultural Residential — RDO 81 Cebu North"),
    ("PC", ClassCode::PS, "Parking Commercial — RDO 81 Cebu North"),
    ("PH", ClassCode::RC, "Penthouse — RDO 52 Parañaque (metadata flag: penthouse=true)"),
    ("R",  ClassCode::RR, "Truncated RR — RDO 4 Pangasinan (data entry error)"),
    ("A0", ClassCode::A50,"Typo for A50 — RDO 4 Pangasinan"),
];

fn resolve_non_standard(raw: &str) -> Option<(ClassCode, &'static str)> {
    NON_STANDARD_CODE_MAP.iter()
        .find(|(code, _, _)| *code == raw)
        .map(|(_, standard, reason)| (*standard, *reason))
}
```

**Discovery protocol for ingestion:** During bulk workbook ingestion, any code not in the 63-code Annex B standard should be:
1. Checked against `NON_STANDARD_CODE_MAP`
2. If found → map to standard code, log the mapping
3. If NOT found → flag for manual review, do NOT silently drop

### 4.5 Cebu Storey-Based Condo Classification

Cebu (RDO 81, 83) introduces catch-all condo tiers based on building height:

- "ALL OTHER CONDOMINIUMS (7 storeys and below)" — lower ZV
- "ALL OTHER CONDOMINIUMS (8 storeys and above)" — 44-78% premium over ≤7 tier

**Engine implication:** For Cebu condo lookups without a specific building match, the engine must ask for building height to select the correct catch-all tier.

```rust
fn resolve_cebu_condo_catchall(
    rdo_id: u8,
    building_storeys: Option<u8>,
    barangay_id: u16,
    index: &ZonalIndex,
) -> ClassificationResult {
    if !is_cebu_rdo(rdo_id) {
        return ClassificationResult::not_applicable();
    }

    match building_storeys {
        Some(s) if s <= 7 => {
            index.find_condo_catchall(barangay_id, CatchallTier::SevenAndBelow)
        }
        Some(s) if s >= 8 => {
            index.find_condo_catchall(barangay_id, CatchallTier::EightAndAbove)
        }
        None => ClassificationResult::needs_input(
            "Building height (storeys) required for Cebu condo catch-all classification"
        ),
        _ => unreachable!(),
    }
}
```

### 4.6 RDO 30 (Binondo) — No RR Code

RDO 30 is the only sampled RDO with NO residential (RR) classification. Binondo is purely commercial. Every lookup returns CR, CC, RC, PS, or X.

**Engine implication:** The classification UI must not assume RR exists everywhere. The `available_codes_per_rdo` index (from Wave 2) handles this automatically — the UI only shows codes that exist in the selected RDO.

### 4.7 Slash-Delimited Dual Codes

One instance found: `A41/A49*` (RDO 83 Cebu) — Forest Land / Nipa dual-classified parcel.

**Engine logic:** Split on `/`, create two separate classification entries for the same row, strip asterisks from each.

```rust
fn split_dual_codes(raw: &str) -> Vec<String> {
    raw.split('/')
        .map(|s| strip_footnote_markers(s.trim()).0)
        .collect()
}
```

### 4.8 CCT vs TCT Bifurcation

The title type affects classification resolution for condominiums:

**CCT (Condominium Certificate of Title):**
> "THE ZONAL VALUE OF THE LAND AND THE IMPROVEMENTS SHALL BE TREATED AS ONE"

The composite condo ZV (RC/CC) applies. No separate land valuation needed.

**TCT (Transfer Certificate of Title):**
> "THE LAND AND IMPROVEMENT SHALL BE GIVEN SEPARATE VALUES"

Requires: (1) land ZV lookup using the underlying land classification (typically RR or CR for the lot), (2) building/improvement FMV from the City Assessor's Schedule of Market Values.

**Engine logic:**
```rust
fn resolve_condo_title_type(
    title_type: TitleType,
    condo_zv: u32,        // RC/CC value from schedule
    land_code: ClassCode,  // Underlying land classification
    land_zv: Option<u32>,  // Land ZV if TCT
) -> ValuationResult {
    match title_type {
        TitleType::CCT => {
            // Single composite value — condo ZV covers everything
            ValuationResult::Composite {
                value_per_sqm: condo_zv,
                note: "CCT: land + improvement treated as one",
            }
        }
        TitleType::TCT => {
            // Split valuation required
            ValuationResult::Split {
                land_value_per_sqm: land_zv,
                land_code,
                improvement_value: None,  // From City Assessor, out of scope
                note: "TCT: land and improvement valued separately. \
                       Improvement FMV from City Assessor's Schedule of Market Values.",
            }
        }
    }
}
```

---

## 5. Classification Code Normalization Pipeline

The full normalization pipeline (from Wave 2 `classification-code-usage.md`) with resolution logic applied:

```rust
pub fn normalize_and_resolve(
    raw_cell: &str,
    rdo_id: u8,
    do_date: NaiveDate,
    legend: Option<&ClassificationLegend>,
) -> Vec<(ClassCode, Option<FootnoteMarker>)> {
    let trimmed = raw_cell.trim();

    // Step 0: Full-text footnote check (cell contains explanation, not a code)
    if trimmed.len() > 15 && !trimmed.chars().all(|c| c.is_alphanumeric() || c == '*' || c == ' ' || c == '/') {
        return vec![];  // Not a classification code — skip
    }

    // Step 1: Split slash-delimited dual codes ("A41/A49*" → ["A41", "A49*"])
    let parts: Vec<&str> = trimmed.split('/').collect();

    parts.iter().filter_map(|part| {
        let p = part.trim();
        if p.is_empty() { return None; }

        // Step 2: Strip leading asterisks
        let (prefix_stars, rest) = strip_prefix_asterisks(p);

        // Step 3: Strip trailing asterisks
        let (code_part, suffix_stars) = strip_suffix_asterisks(rest);

        // Step 4: Strip revision numbers (Cebu pattern: "A50 23" → "A50")
        let code_no_rev = strip_revision_numbers(code_part);

        // Step 5: Collapse spaces ("A 1" → "A1")
        let collapsed = collapse_spaces(code_no_rev);

        // Step 6: Uppercase
        let upper = collapsed.to_uppercase();

        // Step 7: Non-standard code mapping
        let standard_code = if let Some((code, _reason)) = resolve_non_standard(&upper) {
            code
        } else if do_date < NaiveDate::from_ymd(2019, 6, 18) {
            resolve_legacy_code(&upper, legend, do_date)
        } else {
            ClassCode::from_str(&upper)?
        };

        // Step 8: Combine footnote markers
        let footnote_count = prefix_stars.max(suffix_stars);
        let footnote = if footnote_count > 0 {
            Some(FootnoteMarker::Stars(footnote_count))
        } else {
            None
        };

        Some((standard_code, footnote))
    }).collect()
}
```

---

## 6. Rust Data Structures — Complete Classification Module

```rust
/// Classification code enum — 63 standard + NonStandard catch-all
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[repr(u8)]
pub enum ClassCode {
    // Primary codes (13)
    RR = 0, CR = 1, RC = 2, CC = 3, I = 4, X = 5,
    GL = 6, GP = 7, CL = 8, APD = 9, PS = 10, DA = 11, A = 12,
    // Agricultural sub-codes (50)
    A1 = 13, A2 = 14, A3 = 15, A4 = 16, A5 = 17, A6 = 18,
    A7 = 19, A8 = 20, A9 = 21, A10 = 22, A11 = 23, A12 = 24,
    A13 = 25, A14 = 26, A15 = 27, A16 = 28, A17 = 29, A18 = 30,
    A19 = 31, A20 = 32, A21 = 33, A22 = 34, A23 = 35, A24 = 36,
    A25 = 37, A26 = 38, A27 = 39, A28 = 40, A29 = 41, A30 = 42,
    A31 = 43, A32 = 44, A33 = 45, A34 = 46, A35 = 47, A36 = 48,
    A37 = 49, A38 = 50, A39 = 51, A40 = 52, A41 = 53, A42 = 54,
    A43 = 55, A44 = 56, A45 = 57, A46 = 58, A47 = 59, A48 = 60,
    A49 = 61, A50 = 62,
}
// Total: 63 variants, fits in u8 (0-62)
// NonStandard codes are mapped to standard during ingestion, never stored

impl ClassCode {
    pub fn is_agricultural(&self) -> bool {
        matches!(self, ClassCode::A | ClassCode::A1 ..= ClassCode::A50)
    }

    pub fn is_condo(&self) -> bool {
        matches!(self, ClassCode::RC | ClassCode::CC | ClassCode::PS)
    }

    pub fn is_land(&self) -> bool {
        !self.is_condo()
    }

    /// Area threshold for this classification (if any)
    pub fn area_threshold_sqm(&self) -> Option<f64> {
        match self {
            ClassCode::GP => Some(5000.0),
            _ => None,
        }
    }

    /// Soft area threshold (operational practice, not codified)
    pub fn soft_area_threshold_sqm(&self) -> Option<f64> {
        if self.is_agricultural() {
            Some(1000.0)
        } else {
            None
        }
    }
}

/// Classification resolution result
#[derive(Debug)]
pub struct ClassificationResult {
    /// Resolved classification code
    pub code: ClassCode,
    /// Zonal value per sqm
    pub value_per_sqm: u32,
    /// How the value was determined
    pub source: ValueSource,
    /// Confidence level
    pub confidence: Confidence,
    /// Advisory messages (area threshold warnings, conversion notes, etc.)
    pub advisories: Vec<String>,
    /// Footnote metadata from workbook
    pub footnote: Option<FootnoteMarker>,
}

#[derive(Debug)]
pub enum ValueSource {
    /// Directly from the published schedule
    DirectFromSchedule {
        rdo_id: u8,
        department_order: String,
        effectivity_date: NaiveDate,
    },
    /// Computed from a rule (ground floor CC, business use upgrade, PS fallback)
    ComputedFromRule {
        rule_name: &'static str,
        base_code: ClassCode,
        base_value: u32,
        adjustment_pct: i32,  // +20 for CC upgrade, -40 for PS 60%
    },
    /// Institutional fallback to nearest CR
    InstitutionalFallback {
        fallback_code: ClassCode,
        same_street: bool,
    },
}

#[derive(Debug, Clone, Copy)]
pub enum Confidence {
    High,   // Direct schedule match, single classification
    Medium, // User-selected from multiple, computed from rule, or institutional fallback
    Low,    // Fallback to different street/barangay, legacy code mapping
}

/// Per-RDO PS pricing rules
pub struct PsPricingRule {
    pub rdo_id: u8,
    pub percentage: u8,          // 60, 70, or 100
    pub base: PsBase,
    pub cct_override_pct: Option<u8>,  // Some RDOs use different % for CCT
}

pub enum PsBase {
    RcValue,                // Most RDOs: PS = X% of RC
    HigherOfRcCc,           // RDO 44: PS = X% of max(RC, CC)
    UnitSoldValue,          // RDO 47-50: PS = X% of selling price (if available)
}

/// Available codes index — pre-computed during ingestion
pub struct AvailableCodesIndex {
    /// Codes per RDO (for UI dropdown filtering)
    pub codes_per_rdo: HashMap<u8, Vec<ClassCode>>,
    /// Codes per (RDO, barangay) (for fine-grained filtering)
    pub codes_per_location: HashMap<(u8, u16), Vec<ClassCode>>,
    /// PS pricing rule per RDO
    pub ps_rules: HashMap<u8, PsPricingRule>,
}
```

---

## 7. Worked Examples from Actual Data

### Example 1: Single Classification — Provincial Agricultural (Path 1)

**Input:** 500 sqm riceland in Barangay Poblacion, Calasiao, Pangasinan (RDO 4)
**Schedule data:** A1 / ₱1,200/sqm
**Resolution:**
1. Single classification match → auto-resolve to A1
2. Area threshold check: 500 sqm < 1,000 sqm soft threshold → SOFT WARNING
3. Aquafresh principle: published classification governs regardless
**Result:** A1, ₱1,200/sqm, confidence HIGH, advisory: "Property below 1,000 sqm agricultural threshold. Published classification still governs."

### Example 2: Multi-Classification Selection — NCR Street (Path 2)

**Input:** Property on "EDSA", Barangay Wack-Wack Greenhills, Mandaluyong (RDO 41)
**Schedule data:**
- EDSA / Wack-Wack / RR / ₱120,000
- EDSA / Wack-Wack / CR / ₱150,000
- EDSA / Wack-Wack / X / ₱150,000
**Resolution:**
1. Three classifications found → present all three
2. User selects based on Tax Declaration
3. If residential property → RR ₱120,000/sqm
4. If commercial property → CR ₱150,000/sqm
5. If school/hospital → X ₱150,000/sqm
**Result:** User-selected code with value, confidence MEDIUM (user judgment involved)

### Example 3: Condo Ground Floor (Path 3)

**Input:** Ground floor unit, "ONE SHANGRI-LA PLACE", Barangay Wack-Wack, Mandaluyong (RDO 41)
**Schedule data:** RC for this building = ₱175,000/sqm
**Resolution:**
1. Property type = Condo, floor = ground
2. Ground floor CC rule applies: CC = ₱175,000 × 1.20 = ₱210,000/sqm
**Result:** CC, ₱210,000/sqm, source: ComputedFromRule("Ground floor RC → CC + 20%"), confidence HIGH

### Example 4: RC Business Use Upgrade (Path 4)

**Input:** Residential condo unit on 15th floor used as AirBnb, BGC, Taguig (RDO 44)
**Schedule data:** RC = ₱250,000/sqm (BGC FAR tier)
**Resolution:**
1. Property type = Condo, is_business_use = true
2. Business use upgrade: CC = ₱250,000 × 1.20 = ₱300,000/sqm
**Result:** CC, ₱300,000/sqm, source: ComputedFromRule("RC business use → CC + 20%"), confidence HIGH

### Example 5: GP Below Threshold (Path 7)

**Input:** 2,000 sqm vacant lot, Barangay San Isidro, Davao (RDO 113A)
**Schedule data:** GP / ₱3,000/sqm
**Resolution:**
1. Single classification match → GP
2. Area threshold: 2,000 sqm < 5,000 sqm GP threshold → BELOW THRESHOLD
3. Advisory: classify based on actual/predominant use instead
**Result:** GP, ₱3,000/sqm, confidence LOW, advisory: "Below 5,000 sqm GP minimum. Consider RR or CR classification based on actual use."

### Example 6: Agricultural Conversion Timing (Edge Case 4.2)

**Input:** 10,000 sqm lot in Biñan, Laguna (RDO 57). LGU approved conversion from agricultural to residential 2 years ago. BIR schedule still shows A50.
**Schedule data:** A50 / ₱1,500/sqm (published schedule), RR / ₱15,000/sqm (same barangay)
**Resolution:**
1. Published schedule says A50 → return A50, ₱1,500/sqm
2. Aquafresh principle: published classification governs
3. Advisory: conversion will be reflected in next BIR revision
**Result:** A50, ₱1,500/sqm, confidence HIGH, advisory: "Property may have been converted by LGU. Published BIR classification governs until next schedule revision."

### Example 7: Institutional Fallback (Path 6)

**Input:** Church property in a barangay where X has no explicit value, Pangasinan (RDO 4)
**Schedule data:** No X entry. Nearest CR in same barangay = ₱2,500/sqm
**Resolution:**
1. X classification requested but no value in schedule
2. Institutional fallback: use nearest CR = ₱2,500/sqm
**Result:** X (resolved via CR fallback), ₱2,500/sqm, source: InstitutionalFallback, confidence MEDIUM

### Example 8: Cebu Condo Catch-All (Edge Case 4.5)

**Input:** Unit in unnamed 12-storey condo, Cebu City (RDO 83)
**Schedule data:**
- "ALL OTHER CONDOMINIUMS (7 storeys and below)" / RC / ₱45,000
- "ALL OTHER CONDOMINIUMS (8 storeys and above)" / RC / ₱65,000
**Resolution:**
1. No specific building match → catch-all
2. 12 storeys ≥ 8 → use "8 storeys and above" tier
**Result:** RC, ₱65,000/sqm, confidence MEDIUM

---

## 8. Verification Summary

All 8 core classification resolution claims were cross-checked by a verification subagent against 15+ independent sources:

| Claim | Verdict | Key Sources |
|-------|---------|-------------|
| Aquafresh principle (published classification is authoritative) | **CONFIRMED** | G.R. No. 170389 (SC E-Library, Lawphil, ChanRobles) |
| Agricultural 1,000 sqm threshold | **PARTIALLY CONFIRMED** | Practitioner sources confirm operational practice; NOT in Annex B or NIRC |
| GP 5,000 sqm threshold | **CONFIRMED** | BIR Annex B Classification Codes (official document) |
| LGU reclassification ≠ automatic BIR change | **CONFIRMED** | Aquafresh corollary + RMO 31-2019 revision process |
| Ground floor RC → CC + 20% | **CONFIRMED** | BIR DO footnotes (Makati, Taguig, Pasig, Cebu) |
| RC business use → CC + 20% | **CONFIRMED** | BIR DO footnotes (Makati, Taguig, Rockwell) |
| PS = 60-70% of RC/CC (varies by RDO) | **CONFIRMED** | BIR DO footnotes (60% Makati, 70% Taguig, 70/100% Mandaluyong) |
| CR ≥ RR in same barangay | **PARTIALLY CONFIRMED** | Empirically true in all 31 workbooks; not a formal codified rule |

**Conflicts found:** None material. The agricultural 1,000 sqm threshold was the only claim where the primary source could not be identified — downgraded from "hard gate" to "soft warning" in the engine design accordingly.

---

## 9. UI/UX Implications

### Classification Selection UI Flow

```
1. User enters property address
2. Engine matches street/vicinity → retrieves all classification codes for that match
3. If 1 code → auto-select, display value
4. If 2+ codes → show dropdown with all available codes + their values
   └─ Sort by: user's Tax Declaration classification first (if provided), then by frequency
5. If condo:
   a. Ask: "Floor level?" (Ground / Upper / Penthouse)
   b. If ground floor → auto-apply CC + 20% rule
   c. Ask: "Is this unit used for business?" (Yes / No)
   d. If yes → apply CC + 20% rule
   e. Ask: "Title type?" (CCT / TCT)
   f. If TCT → show split valuation advisory
6. If GP → check area threshold, warn if below 5,000 sqm
7. If agricultural → soft warn if below 1,000 sqm
```

### Codes Dropdown Filtering

The `AvailableCodesIndex` enables progressive filtering:
1. **RDO selected** → show only codes that exist in that RDO (5-43 codes depending on RDO)
2. **Barangay selected** → further filter to codes in that barangay (typically 2-10)
3. **Street matched** → show only codes listed for that specific street/vicinity (typically 1-3)

This prevents users from selecting invalid classifications and reduces cognitive load.

---

## 10. Complexity Assessment

| Aspect | Complexity | Rationale |
|--------|-----------|-----------|
| Auto-resolve (single code) | **LOW** | Direct lookup, no logic |
| Multi-classification selection | **LOW** | UI problem, not logic problem |
| Ground floor / business use rules | **MEDIUM** | Computation from rule, needs floor/use input |
| PS fallback | **MEDIUM** | RDO-specific percentage lookup |
| Institutional fallback | **MEDIUM** | Spatial query (nearest CR) |
| GP/Agricultural thresholds | **LOW** | Simple area comparison |
| Non-standard code mapping | **LOW** | Static lookup table |
| Legacy code mapping | **HIGH** | Per-sheet legend parsing for historical data |
| Cebu storey-based catch-all | **MEDIUM** | RDO-specific, needs building height |
| CCT/TCT bifurcation | **MEDIUM** | Title type input, advisory text |

**Overall classification resolution complexity: MEDIUM** — significantly reduced from prior estimate by the Aquafresh principle. The engine's role is primarily selection assistance and special-case rule application, not property classification determination.

---

## Sources

### Primary Legal
- CIR v. Aquafresh Seafoods, Inc. (G.R. No. 170389, Oct 20, 2010) — [Supreme Court E-Library](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/1/54589), [Lawphil](https://lawphil.net/judjuris/juri2010/oct2010/gr_170389_2010.html)
- BIR Ruling No. 041-2001 — cited in Aquafresh re: predominant use limitation
- DOF Local Assessment Regulations No. 1-92 — [Supreme Court E-Library](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/47045), [BLGF](https://blgf.gov.ph/local-assessment-regulations-no-1-92/)
- CBAA Case No. L-97 — "actual use" vs "predominant use" distinction
- RAMO 2-91 — tax base markup rules

### BIR Regulatory
- RMO No. 31-2019 Annex B — Classification codes (63 total)
- RMO No. 31-2019 Annex C — Schedule format standard
- RMC 06-2021 — Format non-compliance acknowledgment
- BIR DO footnotes — Ground floor CC rule, business use upgrade, PS fallback, commercial override

### Workbook Data (Wave 1-2)
- 31 BIR zonal value workbooks (24 NCR + 7 provincial)
- 76,577 classified data rows analyzed
- 62 unique classification codes found
- 2,739+ footnote-embedded classification values
- RDO-specific PS rules: Makati (60%), Taguig (70%), Mandaluyong (70/100%)

### Secondary / Commentary
- [Respicio & Co.](https://www.lawyer-philippines.com/articles/meaning-of-ps-classification-in-zonal-valuation-philippines) — PS classification, fallback rules
- [ForeclosurePhilippines](https://www.foreclosurephilippines.com/what-you-need-to-know-about-bir-zonal-values/) — Agricultural threshold (practitioner source)
- [ZonalValueFinderPH](https://zonalvaluefinderph.com/BIR_Land_Classifications) — Annex B reproduction
- [JPATAG](https://www.jpatag.com/) — BIR zonal value schedules, RDO footnotes
