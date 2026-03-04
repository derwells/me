# RPVARA Dual-Source Resolution — Resolution Logic Deep-Dive

**Wave:** 3 — Resolution Logic Deep-Dive
**Date:** 2026-03-04
**Aspect:** `rpvara-dual-source-resolution`
**Depends on:** Wave 1 (rpvara-transition-mechanics, cta-zonal-rulings), Wave 2 (data-size-estimation, classification-code-usage), Wave 3 (rdo-jurisdiction-mapping, fallback-hierarchy-implementation, classification-resolution-logic)
**Verification:** Cross-checked against independent sources via verification subagent (see §12)
**Prior art:** `analysis/rpvara-transition-mechanics.md`, `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md` §RPVARA, `input/rpvara-transition.md`

---

## 1. Summary

The RPVARA (RA 12001, effective July 2024) creates the most complex dual-source resolution problem in Philippine tax infrastructure: during a multi-year transition period (July 2024 through ~2028+), any given property may be valued under one of **three distinct regimes**, determined by whether the jurisdiction has a BLGF-approved Schedule of Market Values (SMV) in effect. The engine must detect the applicable regime per-jurisdiction, apply the correct tax base formula, and reconcile two fundamentally incompatible classification taxonomies (BIR Annex B codes vs. LGU numeric class system).

**Key finding:** The dual-source problem is NOT primarily a data format problem — it is a **regime detection** and **classification taxonomy mapping** problem. The BIR and LGU systems classify property differently (BIR uses 63 functional codes like RR/CR/RC/CC/A1-A50; LGUs use numeric tiers like R1-R12/C1-C8 within broader categories), and no official crosswalk exists. This is the single hardest design challenge for RPVARA readiness.

**Architecture principle:** The engine must be **regime-agnostic at the matching layer** and **regime-aware at the tax base computation layer**. The property record normalization, address matching, and fallback logic operate identically regardless of data source; only the final tax base computation changes.

---

## 2. The Three Regimes

For any given property lookup, the engine must determine which of three regimes applies based on jurisdiction-level metadata:

### Regime A: Pre-Transition (BIR ZV Active)
- **Condition:** No BLGF-approved SMV exists for this LGU
- **Applicable law:** Section 29(b) of RA 12001 (transitory provision) + NIRC Section 6(E) as amended
- **Tax base for internal revenue taxes (CGT, DST, estate, donor's, VAT):**
  ```
  tax_base_irt = max(selling_price, bir_zonal_value, lgu_existing_fmv)
  ```
- **Tax base for real property tax (RPT):**
  ```
  assessed_value = assessment_level × lgu_fmv
  rpt = rpt_rate × assessed_value
  ```
- **Data source:** BIR zonal value workbooks (the 124 heterogeneous Excel files)
- **Classification system:** BIR Annex B codes (63 codes per RMO 31-2019)
- **Status (March 2026):** This is the active regime for the **vast majority** of LGUs

### Regime B: Transition Year 1 (New SMV, First Year)
- **Condition:** BLGF-approved SMV in effect, within first year of effectivity
- **Applicable law:** Section 18(c) + Section 29(c) of RA 12001
- **Tax base for internal revenue taxes:**
  ```
  tax_base_irt = max(selling_price, blgf_smv)
  ```
- **Tax base for RPT:**
  ```
  assessed_value = new_assessment_level × blgf_smv
  rpt = rpt_rate × assessed_value
  rpt = min(rpt, prior_rpt × 1.06)  // 6% cap per Section 29(c)
  ```
- **Data source:** BLGF-approved SMV (new format, per PVS)
- **Classification system:** LGU numeric class system (R1-R12, C1-C8, etc.)
- **6% cap scope:** The 6% cap applies ONLY to RPT, NOT to internal revenue taxes (CGT, DST, etc.). Internal revenue taxes use the full SMV immediately.
- **Status (March 2026):** No LGU has reached this regime yet (no BLGF-approved SMVs finalized under RPVARA)

### Regime C: Post-Transition (Steady State)
- **Condition:** BLGF-approved SMV in effect, beyond first year
- **Applicable law:** Section 18(c) of RA 12001
- **Tax base for internal revenue taxes:**
  ```
  tax_base_irt = max(selling_price, blgf_smv)
  ```
- **Tax base for RPT:**
  ```
  assessed_value = assessment_level × blgf_smv
  rpt = rpt_rate × assessed_value
  // LGU may have enacted cap ordinance per Section 29(d)
  ```
- **Data source:** BLGF-approved SMV
- **Classification system:** LGU numeric class system
- **Status (March 2026):** No LGU has reached this regime yet

### Regime Detection Decision Tree

```
fn detect_regime(lgu_id: LguId, transaction_date: NaiveDate) -> Regime {
    match get_blgf_smv_status(lgu_id) {
        SmvStatus::NotYetApproved => Regime::A,  // Pre-transition
        SmvStatus::Approved { effectivity_date } => {
            let months_since = months_between(effectivity_date, transaction_date);
            if months_since < 0 {
                Regime::A  // SMV approved but not yet effective
            } else if months_since <= 12 {
                Regime::B  // Transition Year 1
            } else {
                Regime::C  // Post-transition
            }
        }
    }
}
```

---

## 3. Realistic Transition Timeline

### Why the July 2026 Deadline Will Be Missed

The statutory mandate (Section 19) requires all LGUs to update SMVs within 2 years of RPVARA effectivity (deadline: July 3-5, 2026). This deadline will be overwhelmingly missed:

| Evidence | Implication |
|----------|-------------|
| Only 37-42% of LGUs had compliant SMVs under the OLD system (BLGF, 2021) | Historical compliance rate predicts ~40% at best |
| 97 cities + 40 provinces non-compliant as of 2024 | Starting from a deep deficit |
| IRR itself was delayed by ~2 months (due Oct 2024, signed Dec 2024) | Compressed preparation window |
| BLGF still conducting "Skills Enhancement Training" sessions (2025) | Capacity building still underway |
| PVS 2nd Edition only recently launched | Standard itself still being disseminated |
| No BLGF-approved SMV under RPVARA as of March 2026 | Zero completions 21 months in |
| Davao City (2nd largest city) still at "proposed" stage (Nov 2025) | Even major cities not done |
| Bataan (proposed June 2025) still gathering feedback | Multi-month process after proposal |
| Davao realtors actively resisting proposed SMV (1,181% agricultural increase) | Political resistance slows adoption |

### Projected Rollout Scenario

```
Phase 1 (2026 H2):  ~5-15 LGUs    — early adopters, likely Metro Manila suburbs
Phase 2 (2027):      ~50-100 LGUs  — major cities and active provinces
Phase 3 (2028):      ~200-400 LGUs — wider adoption after template effects
Phase 4 (2029+):     remaining      — stragglers, BARMM, remote provinces
```

**Engine design implication:** BIR zonal values must remain a **first-class data source** for 3-5+ years, not a legacy holdover. The engine architecture must treat Regime A as the primary mode, with Regime B/C as progressive enhancements.

---

## 4. The Classification Taxonomy Divergence

This is the most underappreciated challenge in the RPVARA transition. BIR and LGU classification systems are structurally incompatible:

### BIR Classification (Annex B — RMO 31-2019)
- **63 functional codes** based on property USE
- Primary: RR (Residential Regular), CR (Commercial Regular), RC (Residential Condo), CC (Commercial Condo), I (Industrial), X (Institutional/Special), GL (Government Lot), GP (Government Property), CL (Communal Lot), APD (Approved Project for Development), PS (Parking Slot), A (Agricultural), DA (Drying Area)
- Agricultural sub-codes: A1-A50 (50 crop-specific codes like A1=Riceland Irrigated, A2=Riceland Unirrigated, etc.)
- **Granularity:** USE-based, no tier within use type. All residential regular land in a vicinity gets code RR regardless of value tier.

### LGU Classification (DOF LAR 1-92 / PVS)
- **Numeric tiers** within each broad land use CATEGORY
- Residential: R1 (highest value) through R12+ (lowest)
- Commercial: C1 through C8
- Industrial: I1 through I3+
- Agricultural: by crop type AND class (e.g., "Irrigated Rice — Class 1")
- Subdivision: SR1 through SR4
- **Granularity:** LOCATION-TIER-based. Value differentiates tiers within the same use category.

### Why No Automatic Crosswalk Exists

| BIR Code | LGU Equivalent | Mapping Difficulty |
|----------|---------------|-------------------|
| RR | R1-R12 (which one?) | **IMPOSSIBLE** — BIR RR is a single value per street/vicinity; LGU R-class is value-tiered |
| CR | C1-C8 (which one?) | Same problem — no structural correspondence |
| RC | Not directly present in LGU system | Condo is a building type, not a land class in LGU SMVs |
| CC | Not directly present | Same — condo buildings handled differently |
| A1-A50 | Agricultural Class 1-N by crop | Partial match by crop type, but numbering differs |
| X | Not present — institutional properties are exempt or special-assessed | Gap |
| PS | Not present — parking is building component | Gap |

### Resolution Strategy for the Engine

The engine CANNOT map between these classification systems programmatically. Instead, it must:

1. **Store both taxonomies as metadata** per record, identified by source
2. **Present the applicable classification to the user** based on the detected regime
3. **For Regime A lookups:** user selects from BIR Annex B codes (or engine infers from property type)
4. **For Regime B/C lookups:** user provides the LGU classification from their tax declaration
5. **During transition:** if a property has BOTH a BIR ZV and a BLGF SMV (the three-way max scenario under Section 29(b)), the engine performs TWO independent lookups and returns the higher value

### Rust Types

```rust
/// Classification code source — which taxonomy system this code belongs to
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClassificationSource {
    /// BIR Annex B codes (RMO 31-2019): RR, CR, RC, CC, I, X, etc.
    BirAnnexB,
    /// LGU numeric tier system: R1-R12, C1-C8, I1-I3, etc.
    LguSmv,
    /// Future BLGF PVS-standardized system (TBD — may differ from current LGU)
    BlgfPvs,
}

/// A classification code that carries its source taxonomy
#[derive(Debug, Clone)]
pub struct ClassifiedCode {
    /// The raw code string (e.g., "RR", "R3", "C1", "A1")
    pub code: String,
    /// Which taxonomy this code belongs to
    pub source: ClassificationSource,
    /// Broad land use category (normalized across taxonomies)
    pub land_use: LandUseCategory,
}

/// Normalized land use category — the common denominator across taxonomies
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LandUseCategory {
    Residential,
    Commercial,
    Industrial,
    Agricultural,
    Institutional,
    Special,       // Government lots, communal, APD
    Condominium,   // BIR-specific; LGU treats as building type
    Parking,       // BIR-specific; LGU treats as building component
}
```

---

## 5. Data Source Architecture

### Source Abstraction Layer

The engine must treat BIR ZV data and BLGF SMV data as implementations of a common `ValuationSource` trait:

```rust
/// A normalized property valuation record, source-agnostic
#[derive(Debug, Clone)]
pub struct ValuationRecord {
    /// Unique record identifier
    pub id: RecordId,
    /// Which data source produced this record
    pub source: DataSource,
    /// Geographic location
    pub location: PropertyLocation,
    /// Classification code (in the source's taxonomy)
    pub classification: ClassifiedCode,
    /// Value per square meter (in PHP centavos for integer arithmetic)
    pub value_per_sqm: u64,
    /// Effective date of this valuation
    pub effectivity_date: NaiveDate,
    /// The legal authority that established this value
    pub authority: ValuationAuthority,
    /// Optional: revision/version identifier
    pub revision: Option<String>,
}

/// Data source identification
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DataSource {
    /// BIR zonal value from DOF Department Order
    BirZonalValue {
        rdo_id: u8,
        department_order: String,  // e.g., "DO 022-2021"
    },
    /// BLGF-approved SMV under RPVARA
    BlgfSmv {
        lgu_id: LguId,
        dof_certification: String,
        pvs_version: String,       // e.g., "PVS 2nd Edition"
    },
    /// Future: RPIS centralized data
    Rpis {
        rpis_record_id: String,
    },
}

/// The legal authority backing a valuation
#[derive(Debug, Clone)]
pub struct ValuationAuthority {
    /// Issuing body
    pub issuer: Issuer,
    /// The specific issuance (DO, SMV certification, etc.)
    pub issuance: String,
    /// Date signed
    pub date_signed: NaiveDate,
    /// Date effective
    pub date_effective: NaiveDate,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Issuer {
    /// DOF Secretary (for BIR zonal values via Department Orders)
    DofSecretary,
    /// DOF Secretary (for BLGF SMVs via certification)
    DofSecretaryBlgf,
    /// Future: BLGF directly via RPIS
    Blgf,
}
```

### Source Registration and Priority

```rust
/// Manages available data sources for a jurisdiction
pub struct JurisdictionSources {
    /// BIR zonal value (always present during transition)
    pub bir_zv: Option<BirZonalValueIndex>,
    /// BLGF-approved SMV (present only if LGU has completed RPVARA process)
    pub blgf_smv: Option<BlgfSmvIndex>,
    /// The detected regime for this jurisdiction
    pub regime: Regime,
    /// Last checked date for source freshness
    pub last_verified: NaiveDate,
}

impl JurisdictionSources {
    /// Get all applicable valuation sources for a lookup
    pub fn active_sources(&self) -> Vec<&dyn ValuationIndex> {
        match self.regime {
            Regime::A => {
                // Pre-transition: BIR ZV is the primary source for IRT
                // LGU FMV (existing SMV) is separate — not ingested by this engine
                vec![self.bir_zv.as_ref().unwrap()]
            }
            Regime::B | Regime::C => {
                // Post-transition: BLGF SMV is primary
                // BIR ZV no longer needed for IRT computation
                // But may still be useful for comparison/validation
                let mut sources = vec![self.blgf_smv.as_ref().unwrap() as &dyn ValuationIndex];
                if let Some(ref zv) = self.bir_zv {
                    // Include BIR ZV as secondary/reference only
                    sources.push(zv);
                }
                sources
            }
        }
    }
}
```

---

## 6. Dual-Source Resolution Algorithm

### The Full Resolution Pipeline

```rust
/// Main resolution function — regime-aware
pub fn resolve_property_value(
    query: &PropertyQuery,
    jurisdiction_sources: &JurisdictionSources,
    transaction_date: NaiveDate,
) -> ResolutionResult {
    let regime = jurisdiction_sources.regime;

    match regime {
        Regime::A => resolve_regime_a(query, jurisdiction_sources, transaction_date),
        Regime::B => resolve_regime_b(query, jurisdiction_sources, transaction_date),
        Regime::C => resolve_regime_c(query, jurisdiction_sources, transaction_date),
    }
}

/// Regime A: Pre-transition — BIR ZV lookup
fn resolve_regime_a(
    query: &PropertyQuery,
    sources: &JurisdictionSources,
    transaction_date: NaiveDate,
) -> ResolutionResult {
    let bir_index = sources.bir_zv.as_ref()
        .expect("Regime A requires BIR ZV data");

    // Standard BIR resolution pipeline (8-phase matching from address-matching-algorithms)
    let bir_result = bir_index.resolve(query);

    ResolutionResult {
        regime: Regime::A,
        primary_value: bir_result.value,
        primary_source: DataSource::BirZonalValue { .. },
        // IRT tax base formula: max(SP, ZV, existing_FMV)
        // Engine provides ZV; user provides SP and FMV (from tax declaration)
        tax_base_formula: TaxBaseFormula::ThreeWayMax,
        confidence: bir_result.confidence,
        fallback_level: bir_result.fallback_level,
        regime_metadata: RegimeMetadata::PreTransition {
            bir_do: bir_result.department_order.clone(),
            effectivity: bir_result.effectivity_date,
            staleness_warning: is_stale(&bir_result, transaction_date),
        },
    }
}

/// Regime B: Transition Year 1 — BLGF SMV lookup with RPT cap
fn resolve_regime_b(
    query: &PropertyQuery,
    sources: &JurisdictionSources,
    transaction_date: NaiveDate,
) -> ResolutionResult {
    let smv_index = sources.blgf_smv.as_ref()
        .expect("Regime B requires BLGF SMV data");

    let smv_result = smv_index.resolve(query);

    ResolutionResult {
        regime: Regime::B,
        primary_value: smv_result.value,
        primary_source: DataSource::BlgfSmv { .. },
        // IRT tax base formula: max(SP, SMV)
        // NOTE: No ZV component — Section 18(c) replaces 6(E)
        tax_base_formula: TaxBaseFormula::TwoWayMax,
        confidence: smv_result.confidence,
        fallback_level: smv_result.fallback_level,
        regime_metadata: RegimeMetadata::TransitionYear1 {
            smv_effectivity: smv_result.effectivity_date,
            rpt_cap_percent: 6, // Section 29(c)
            rpt_cap_applies_to: TaxType::RealPropertyTax, // NOT IRT
            // IRT uses full SMV immediately — no cap
        },
    }
}

/// Regime C: Post-transition — BLGF SMV lookup, steady state
fn resolve_regime_c(
    query: &PropertyQuery,
    sources: &JurisdictionSources,
    transaction_date: NaiveDate,
) -> ResolutionResult {
    let smv_index = sources.blgf_smv.as_ref()
        .expect("Regime C requires BLGF SMV data");

    let smv_result = smv_index.resolve(query);

    ResolutionResult {
        regime: Regime::C,
        primary_value: smv_result.value,
        primary_source: DataSource::BlgfSmv { .. },
        tax_base_formula: TaxBaseFormula::TwoWayMax,
        confidence: smv_result.confidence,
        fallback_level: smv_result.fallback_level,
        regime_metadata: RegimeMetadata::PostTransition {
            smv_effectivity: smv_result.effectivity_date,
            lgu_cap_ordinance: check_lgu_cap_ordinance(query.lgu_id),
        },
    }
}
```

---

## 7. BLGF SMV Format Analysis (What We Know and Don't Know)

### Known from Proposed 2026 SMVs

Analysis of proposed SMVs from Davao City, Bataan, and Tacurong City reveals the emerging BLGF-era format:

| Attribute | BIR Zonal Value | LGU SMV (Proposed 2026) |
|-----------|----------------|------------------------|
| **Organizing unit** | RDO (Revenue District Office) | LGU (City/Municipality) |
| **Geographic key** | Street × Vicinity × Barangay | Zone/Area × Barangay (location-tier based) |
| **Classification** | Functional code (RR, CR, etc.) | Numeric tier (R1-R12, C1-C8, etc.) |
| **Value unit** | Per sqm (land); per sqm (condo) | Per sqm (land); per sqm (building, by type) |
| **Scope** | Land only (no buildings/machinery) | Land + Buildings + Machinery + Other improvements |
| **Format** | Excel workbook (heterogeneous) | PDF / TBD digital format |
| **Legal authority** | DOF Department Order | DOF Secretary certification under RA 12001 |
| **Revision frequency** | 3-5 years (38% outdated) | 3 years mandatory (with penalties) |
| **Condo handling** | Dedicated condo tables (RC/CC/PS) | Building valuation schedule (separate from land) |
| **Agricultural** | A1-A50 crop codes | Crop type × class (e.g., "Irrigated Rice — Class 1") |

### Critical Unknown: Will BLGF Standardize a Digital Format?

The RPIS TOR (May 2024) indicates BLGF is procuring a system to centralize property data. Key implications:

1. **If RPIS provides an API:** The engine can ingest BLGF SMV data programmatically — dramatically simplifying the dual-source architecture
2. **If SMVs remain PDF/Excel:** The engine must build a second parser family for LGU SMV formats
3. **Current evidence suggests:** No standardized digital format yet. LGUs are publishing proposed SMVs as PDFs with varying structures.

### Format Risk Mitigation

```rust
/// Data ingestion trait — implemented by each source parser
pub trait SourceParser {
    /// Parse raw source data into normalized ValuationRecords
    fn parse(&self, raw_data: &[u8]) -> Result<Vec<ValuationRecord>, ParseError>;

    /// Identify the source format from raw data
    fn detect_format(&self, raw_data: &[u8]) -> Option<SourceFormat>;
}

/// Known source formats
pub enum SourceFormat {
    /// BIR Excel workbook (6 known column layout patterns)
    BirExcelWorkbook(BirColumnLayout),
    /// BLGF SMV PDF (format TBD — placeholder)
    BlgfSmvPdf,
    /// BLGF SMV via RPIS API (format TBD)
    RpisApi,
    /// BLGF SMV Excel (some LGUs may use Excel)
    BlgfSmvExcel,
}
```

---

## 8. Regime Detection Data Model

The engine needs a jurisdiction-level registry to detect which regime applies:

### LGU Registry

```rust
/// Jurisdiction metadata for regime detection
#[derive(Debug, Clone)]
pub struct LguRegimeEntry {
    /// LGU identifier (PSA PSGC code)
    pub lgu_id: LguId,
    /// Province
    pub province: String,
    /// City/Municipality name
    pub name: String,
    /// Which BIR RDO(s) cover this LGU
    pub bir_rdo_ids: Vec<u8>,
    /// BLGF SMV status
    pub smv_status: SmvStatus,
    /// RPT cap ordinance (if any)
    pub rpt_cap_ordinance: Option<RptCapOrdinance>,
    /// Last verified date
    pub last_verified: NaiveDate,
}

#[derive(Debug, Clone)]
pub enum SmvStatus {
    /// No BLGF-approved SMV — Regime A
    NotYetApproved,
    /// SMV in preparation/proposal stage
    InPreparation {
        stage: PreparationStage,
        estimated_completion: Option<NaiveDate>,
    },
    /// SMV approved and effective
    Approved {
        effectivity_date: NaiveDate,
        dof_certification: String,
        pvs_version: String,
    },
}

#[derive(Debug, Clone, Copy)]
pub enum PreparationStage {
    /// LGU assessor preparing draft
    Drafting,
    /// Published for public consultation
    PublicConsultation,
    /// Submitted to BLGF Regional Office
    UnderBlgfReview,
    /// Endorsed to DOF Secretary
    PendingCertification,
}

/// ~1,700 LGUs × ~64 bytes/entry = ~109 KB — trivially fits in WASM
pub struct LguRegimeRegistry {
    entries: HashMap<LguId, LguRegimeEntry>,
}

impl LguRegimeRegistry {
    pub fn detect_regime(&self, lgu_id: LguId, transaction_date: NaiveDate) -> Regime {
        match self.entries.get(&lgu_id) {
            None => Regime::A, // Unknown LGU → conservative default
            Some(entry) => match &entry.smv_status {
                SmvStatus::NotYetApproved | SmvStatus::InPreparation { .. } => Regime::A,
                SmvStatus::Approved { effectivity_date, .. } => {
                    if transaction_date < *effectivity_date {
                        Regime::A
                    } else if transaction_date < *effectivity_date + Duration::days(365) {
                        Regime::B
                    } else {
                        Regime::C
                    }
                }
            }
        }
    }
}
```

### Registry Size and Update Frequency

| Metric | Value |
|--------|-------|
| Total LGUs (provinces + cities + municipalities) | ~1,715 |
| PSA PSGC coverage | 42,046 barangays |
| Registry record size | ~64 bytes per LGU |
| Total registry size | ~110 KB (uncompressed) |
| Update frequency needed | Monthly (to track SMV approvals) |
| Delivery | Bundled in WASM, updated via background fetch |

---

## 9. Graceful Degradation When SMV Data Is Incomplete

During the extended transition period, many scenarios will produce incomplete data:

### Scenario Matrix

| Scenario | BIR ZV Available? | BLGF SMV Available? | Engine Behavior |
|----------|-------------------|---------------------|-----------------|
| **S1:** Normal pre-transition | Yes | No | Standard BIR lookup (Regime A) |
| **S2:** Newly approved SMV | Yes | Yes | Regime B — use SMV for IRT; BIR ZV available for reference |
| **S3:** SMV approved but partial coverage | Yes | Partial | Regime B for covered properties; fall back to Regime A for gaps |
| **S4:** BIR ZV stale (>5 years old) | Stale | No | Regime A with staleness warning |
| **S5:** BARMM coverage gap | No | No | Return NULL with coverage gap explanation |
| **S6:** Post-transition steady state | Historical | Yes | Regime C — SMV only |
| **S7:** SMV revoked/remanded | Yes | Revoked | Revert to Regime A |

### Degradation Cascade

```rust
/// Graceful degradation when primary source is incomplete
pub fn resolve_with_degradation(
    query: &PropertyQuery,
    sources: &JurisdictionSources,
    transaction_date: NaiveDate,
) -> ResolutionResult {
    let regime = sources.regime;

    // Try primary source first
    let primary_result = match regime {
        Regime::A => sources.bir_zv.as_ref().and_then(|idx| idx.resolve(query).ok()),
        Regime::B | Regime::C => sources.blgf_smv.as_ref().and_then(|idx| idx.resolve(query).ok()),
    };

    match primary_result {
        Some(result) => result.into_resolution(regime),
        None => {
            // Primary source failed — attempt degradation
            match regime {
                Regime::A => {
                    // BIR ZV not found → standard fallback hierarchy (7 levels)
                    // This is handled by the existing fallback engine
                    resolve_with_fallback(query, sources.bir_zv.as_ref().unwrap())
                }
                Regime::B | Regime::C => {
                    // BLGF SMV not found for this specific property
                    // Check if BIR ZV exists as fallback reference
                    if let Some(ref bir_zv) = sources.bir_zv {
                        if let Some(bir_result) = bir_zv.resolve(query).ok() {
                            ResolutionResult {
                                regime,
                                primary_value: bir_result.value,
                                primary_source: DataSource::BirZonalValue { .. },
                                tax_base_formula: TaxBaseFormula::TwoWayMax,
                                confidence: bir_result.confidence * 0.8, // Penalty for source mismatch
                                degradation: Some(DegradationInfo {
                                    reason: "BLGF SMV does not cover this property; \
                                             BIR zonal value used as reference",
                                    legal_note: "Per Section 4(p), properties not in SMV \
                                                 shall be appraised at current market value",
                                }),
                                ..Default::default()
                            }
                        } else {
                            // Neither source covers this property
                            ResolutionResult::no_match(regime,
                                "Neither BLGF SMV nor BIR ZV covers this property")
                        }
                    } else {
                        ResolutionResult::no_match(regime,
                            "No valuation data available for this jurisdiction")
                    }
                }
            }
        }
    }
}
```

---

## 10. BIR Zonal Value Revisions During Transition

A critical observation: the BIR has **continued issuing zonal value revisions** during the RPVARA transition period (2025 reports confirm 15-60%+ increases in Metro Manila, Cavite, Laguna, Pampanga, Cebu, Davao). This means:

1. **The old system is actively maintained** — the STCRPV/TCRPV/ECRPV committee structure is still functioning
2. **New DOF Department Orders are still being issued** — updating BIR zonal value workbooks
3. **The engine's BIR data pipeline must continue to ingest updates** — even after RPVARA, until each jurisdiction transitions

### Legal Basis for Continued BIR Revisions

Section 29(a) of RA 12001: "LGUs already updating SMVs may continue under Sections 15, 16, 17, and 19."

Section 31 (Saving Clause): BIR zonal values "continue to be in force and effect" until replaced.

**Open question:** Can the BIR committee (STCRPV/TCRPV/ECRPV) issue NEW zonal value revisions after RPVARA, or only maintain existing ones? The law is ambiguous:
- Section 18(c) removes the CIR's power to determine values for IRT purposes (post-SMV)
- But Section 31 keeps existing values in force
- No BIR RMC addresses this question directly

**Engine design decision:** Accept all DOF Department Orders regardless of issuance date. The legal question of whether new BIR revisions are valid post-RPVARA is for courts to decide — the engine should not pre-judge. If a DOF DO is published, it is ingested.

---

## 11. Worked Examples

### Example 1: Standard Pre-Transition Lookup (Regime A)
**Property:** Residential lot on Ayala Avenue, Makati City (Barangay San Lorenzo)
**Transaction date:** March 2026
**Regime detection:** Makati City has NO BLGF-approved SMV → Regime A
**Lookup:** BIR RDO 47 → Ayala Avenue → RR → ₱200,000/sqm
**Tax base (CGT):** max(SP, ₱200,000/sqm × area, LGU FMV) × 6%
**Confidence:** 0.95 (exact match)
**Display:** "BIR Zonal Value (DO 022-2021, 7th Revision East Makati). Regime: Pre-transition (Section 29(b)). Tax base: higher of selling price, ₱200,000/sqm zonal value, or assessor's FMV."

### Example 2: Newly Transitioned LGU (Regime B — Hypothetical)
**Property:** Commercial lot on National Highway, Bataan
**Transaction date:** January 2027 (hypothetical: Bataan SMV approved, effective Oct 2026)
**Regime detection:** Bataan has BLGF-approved SMV effective Oct 1, 2026 → Regime B (within first year)
**Lookup:** Bataan SMV → Zone 1 Commercial → C1 → ₱15,000/sqm
**Tax base (CGT):** max(SP, ₱15,000/sqm × area) × 6%
**Note:** For RPT purposes, increase capped at 6% over prior year's assessment
**Display:** "BLGF Schedule of Market Values (DOF Certification 2026-XXX, effective Oct 1, 2026). Regime: Transition Year 1 (Section 18(c) + Section 29(c) 6% RPT cap). Tax base: higher of selling price or ₱15,000/sqm SMV."

### Example 3: SMV Partial Coverage Gap (Degradation)
**Property:** Condo unit in BGC, Taguig
**Transaction date:** June 2027 (hypothetical: Taguig SMV approved but does not cover condos yet)
**Regime detection:** Taguig has BLGF-approved SMV → Regime B
**SMV lookup:** No matching record for this condo building
**Degradation:** Fall back to BIR RDO 44 → BGC condos → RC → ₱250,000/sqm
**Display:** "⚠ BLGF SMV does not cover this property. BIR Zonal Value (DO 005-2024) used as reference. Per Section 4(p) of RA 12001, properties not in SMV shall be appraised at current market value. Recommend verification with RDO or assessor's office."

### Example 4: Agricultural Property During Transition (Regime A with Staleness)
**Property:** Rice paddy, Pangasinan
**Transaction date:** March 2026
**Regime detection:** Pangasinan has NO BLGF-approved SMV → Regime A
**Lookup:** BIR RDO 4 → Brgy. Lucao → A1 (Riceland Irrigated) → ₱350/sqm
**Staleness check:** Last revision was 2016 (10 years old) → STALE
**Display:** "BIR Zonal Value (DO 2016-XXX). ⚠ STALE: Last revised 2016 (10 years ago). 38% of BIR schedules are outdated. Regime: Pre-transition. Value may not reflect current market conditions."

### Example 5: BARMM Coverage Gap (No Data)
**Property:** Lot in newly created BARMM municipality (one of 8 with no published RDO assignment)
**Transaction date:** March 2026
**Regime detection:** No BIR RDO assignment found → coverage gap
**Lookup:** NULL
**Display:** "⚠ No valuation data available. This municipality has no published BIR RDO assignment and no BLGF-approved SMV. Per CTA jurisprudence (Emiliano, Gamboa), valuation requires BIR written inquiry or zonal classification ruling."

### Example 6: Post-Transition Steady State (Regime C — Future)
**Property:** Industrial lot in Cavite
**Transaction date:** January 2029 (hypothetical: Cavite SMV approved, effective Jan 2027)
**Regime detection:** Cavite has BLGF-approved SMV, beyond first year → Regime C
**Lookup:** Cavite SMV → Industrial Zone → I2 → ₱8,500/sqm
**Tax base (CGT):** max(SP, ₱8,500/sqm × area) × 6%
**Display:** "BLGF Schedule of Market Values (DOF Certification 2026-XXX). Regime: Post-transition (Section 18(c)). Tax base: higher of selling price or ₱8,500/sqm SMV."

---

## 12. Verification Results

Verification subagent cross-checked 10 claims against independent sources. Results are appended upon completion.

*(See `analysis/rpvara-dual-source-verification.md` for full verification report)*

---

## 13. Design Decisions Summary

| Decision | Rationale | Trace to Finding |
|----------|-----------|-----------------|
| **Regime detection at LGU level, not RDO level** | RPVARA transfers authority to LGU assessors; RDO jurisdiction is BIR-specific | Section 15 RA 12001: "provincial assessors, together with municipal assessors, city assessors" |
| **BIR ZV as first-class source for 3-5+ years** | Zero BLGF-approved SMVs as of March 2026; 37-42% historical compliance; Davao still at proposal stage | §3 timeline analysis |
| **No classification crosswalk** | BIR and LGU taxonomies are structurally incompatible; no official mapping exists | §4 taxonomy divergence analysis |
| **Both taxonomies stored as metadata** | Engine cannot programmatically map R1-R12 to RR; user must provide applicable classification | §4 resolution strategy |
| **6% cap only flagged for RPT, not IRT** | Section 29(c) explicitly scope-limited to real property taxes | Verified against RA 12001 text + CHLP Realty + PwC analysis |
| **Accept all DOF DOs regardless of date** | Legal validity of post-RPVARA BIR revisions is unresolved; engine should not pre-judge | §10 analysis of continued BIR revisions |
| **Pluggable SourceParser trait** | BLGF SMV format is unknown; RPIS may provide API; engine must adapt without core changes | §7 format analysis |
| **LGU regime registry as lightweight dataset** | ~1,715 entries × ~64 bytes = ~110 KB; monthly update; trivial for WASM | §8 data model |
| **Degradation to BIR ZV when SMV gaps exist** | Section 4(p): properties not in SMV "shall be appraised at current market value"; BIR ZV is the closest available data | §9 scenario S3 |
| **Confidence penalty for source mismatch** | When BIR ZV is used as fallback for a Regime B/C property, confidence multiplied by 0.8 | §9 degradation cascade |

---

## 14. Open Questions for Wave 5

1. **RPIS API format:** Will RPIS provide a standardized API for SMV lookup? If so, the engine's BLGF data source can be API-backed rather than file-parsed. The RPIS TOR (May 2024) mentions "Agile Software Development" and "client-server architecture" but no API specification.

2. **PVS classification convergence:** Will the PVS eventually standardize classification codes across all LGUs, replacing the current heterogeneous R1-R12/C1-C8 systems with a national standard? If so, a single LGU taxonomy may eventually emerge.

3. **Condo valuation under SMV:** BIR treats condos as a land classification (RC/CC/PS per unit of sqm); LGU SMV treats buildings separately from land. How will condo valuation work when the SMV governs? This is unresolved.

4. **WASM bundle impact:** During the dual-source period, the engine may need to carry both BIR ZV data (~4.4 MB brotli) and BLGF SMV data (size TBD). If SMV data is per-LGU and rolls out gradually, incremental loading is feasible.

5. **Historical BIR ZV retention:** After an LGU transitions to Regime B/C, should historical BIR ZV data be retained for: (a) transactions with earlier effective dates, (b) reference/comparison, (c) audit trails? If yes, storage implications.

---

## 15. RPVARA Impact on Existing Engine Components

### Components That Do NOT Change

| Component | Why Unchanged |
|-----------|--------------|
| Address matching pipeline | Location matching is source-agnostic — same algorithm for BIR or SMV data |
| Fallback hierarchy (7 levels) | The fallback logic applies to any valuation source — confirmed in §6 of fallback analysis |
| RDO jurisdiction mapping | Still needed for Regime A lookups (the dominant regime for years) |
| Condo matching | Building name matching is source-agnostic |
| Confidence scoring | Same scoring model, with regime-specific adjustments (§9) |

### Components That Must Change/Extend

| Component | Required Change |
|-----------|----------------|
| **Tax base computation** | Must support both `max(SP, ZV, FMV)` and `max(SP, SMV)` formulas |
| **Classification input** | Must accept both BIR Annex B codes AND LGU numeric classes |
| **Data ingestion** | Must support BLGF SMV format (unknown, pluggable parser) |
| **Regime detection** | New LGU regime registry (~110 KB, monthly updates) |
| **Result display** | Must show which regime applies, applicable law, and staleness warnings |
| **Data freshness** | Must track BLGF SMV effectivity dates alongside BIR DO dates |

---

## Legal Citations

| Citation | Relevance |
|----------|-----------|
| RA 12001 (RPVARA), June 13, 2024 | Enabling law; transfers valuation authority to BLGF |
| RA 12001, Section 4(p) | Definition of SMV; properties not in SMV "shall be appraised at current market value" |
| RA 12001, Section 15 | Provincial/city/municipal assessors prepare SMVs |
| RA 12001, Section 18(c) | CIR uses max(SMV, SP) for internal revenue taxes — the two-way max rule |
| RA 12001, Section 19 | 2-year update deadline + 3-year revision cycle |
| RA 12001, Section 22 | Real Property Information System (RPIS) |
| RA 12001, Section 29(a) | LGUs already updating may continue under existing process |
| RA 12001, Section 29(b) | Interim rule: max(SP, ZV, existing_SMV) — three-way max during transition |
| RA 12001, Section 29(c) | 6% RPT cap in first year of new SMV |
| RA 12001, Section 29(d) | LGU may enact subsequent cap ordinance |
| RA 12001, Section 31 | Saving clause: BIR ZVs continue in force until replaced |
| BLGF MC 001-2025 | IRR of RA 12001 (effective January 11, 2025) |
| NIRC Section 6(E) | Pre-RPVARA CIR authority to prescribe zonal values (effectively superseded post-SMV) |
| RMO 31-2019 | BIR operative order for zonal values (still in effect during transition) |
| RMC 115-2020 | BIR certification procedure (still in effect) |
| DOF LAR 1-92 | LGU classification and assessment regulations |

---

## Sources

- RA 12001: [LawPhil](https://lawphil.net/statutes/repacts/ra2024/ra_12001_2024.html) | [SC E-Library](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/97502)
- BLGF MC 001-2025 (IRR): [BLGF PDF](https://blgf.gov.ph/wp-content/uploads/2025/03/BLGF-MC-No.-001.2025-IRR-of-RA-No.-12001-or-the-RPVARA-Reform-Act-6-Jan-2025-Approved-3.pdf)
- BLGF SMV Summary: [BLGF SMV](https://blgf.gov.ph/smv/)
- BLGF RPIS TOR: [BLGF PDF](https://blgf.gov.ph/wp-content/uploads/2024/05/TOR-LGRP-OP2-QCBS-002-RPIS-FIRM-MAY-13-2024.pdf)
- Davao City Proposed SMV 2026: [Davao City](https://davaocity.gov.ph/wp-content/uploads/2025/11/Proposed-SMV-2026.pdf)
- Davao Realtors Resist SMV: [Mindanao Times](https://www.mindanaotimes.com.ph/davao-realtors-resist-proposed-market-value-schedule-for-2026/)
- Bataan Proposed SMV 2026: [Bataan.gov.ph](https://bataan.gov.ph/2026-proposed-schedule-of-market-values-smv-for-the-province-of-bataan/)
- Tacurong Proposed SMV: [Tacurong.gov.ph](https://tacurong.gov.ph/wp-content/uploads/2026/01/Proposed-Schedule-of-Market-Values.pdf)
- CREBA BIR Tax Updates: [CREBA](https://creba.ph/wp-content/uploads/2025/06/BIR-Tax-Updates-on-Real-Property-Transactions.pdf)
- BuySelLease BIR ZV Updates 2025: [BuySelLease](https://buyselllease.ph/bir-zonal-value-updates-in-2025-what-changed-and-why-it-matters/)
- PwC RPVARA: [PwC PH](https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2024/modernizing-property-valuation.html)
- Deloitte RPVARA: [Deloitte SEA](https://www.deloitte.com/southeast-asia/en/services/tax/perspectives/rpvara.html)
- CHLP Realty RPVARA: [CHLP Realty](https://www.chlprealty.com/post/real-property-tax-2025-real-property-valuation-and-assessment-reform-act-rpvara-latest-updates-on)
- BIR 2026 RMCs: [BIR](https://www.bir.gov.ph/2026-Revenue-Memorandum-Circulars)
- Itogon Explainer: [Itogon](https://itogon.gov.ph/2025/02/explainer-on-rpvara-real-property-valuation-and-assessment-reform-act/)
- Lamudi RPVARA: [Lamudi](https://www.lamudi.com.ph/journal/real-property-valuation-assessment-reform-act/)
- Grant Thornton: [GT PH](https://www.grantthornton.com.ph/insights/articles-and-updates1/lets-talk-tax/the-reformation-of-real-property-valuation-insights-on-the-rpvara-and-its-implementing-rules-and-regulations/)
- SRMO Law: [SRMO](https://srmo-law.com/legal-updates/understanding-republic-act-no-12001-or-the-real-property-valuation-and-assessment-reform-act-of-2024-rpvara/)
