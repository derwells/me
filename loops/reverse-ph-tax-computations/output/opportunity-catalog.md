# Opportunity Catalog — Philippine Real Estate Tax Computation Automation

**Produced by:** PH Tax Computations Survey (reverse ralph loop)
**Date:** 2026-02-26
**Status:** Draft (pending self-review)
**Methodology:** 12 deterministic computations surveyed across 4 waves — source acquisition, computation extraction with mandatory verification, competitive/workflow gap analysis, and composite scoring (automation_gap × market_frequency × moat_defensibility, each 1–5, composite 1–125).

---

## How to Read This Catalog

Each entry contains:
- **What it computes** — inputs, outputs, and core formula
- **Legal basis** — specific NIRC sections, Revenue Regulations, and Revenue Memorandum Circulars
- **Current state** — how practitioners do it today (manual, spreadsheet, partially automated)
- **Complexity estimate** — branching rules, lookup tables, external data dependencies
- **Competitive gap** — what JuanTax, Taxumo, QNE Cloud, and other tools don't cover
- **Scores** — automation gap (AG), market frequency (MF), moat defensibility (MD), composite

Entries are ranked by composite score (descending). Tier classification:
- **TIER 1 (80–125):** Highest opportunity — wide gap, high frequency, strong moat
- **TIER 2 (50–79):** Strong opportunity — meaningful gap with frequency or moat advantage
- **TIER 3 (25–49):** Moderate opportunity — gap exists but limited moat or frequency
- **TIER 4 (1–24):** Low priority — covered by existing tools or low defensibility

---

## Summary Rankings

| Rank | Computation | AG | MF | MD | Score | Tier | Deep-Dive? |
|---:|---|:---:|:---:|:---:|---:|---|:---:|
| 1 | Zonal Value Lookup | 5 | 5 | 5 | **125** | TIER 1 | P0 |
| 1 | RPT Computation | 5 | 5 | 5 | **125** | TIER 1 | P1 |
| 3 | Installment VAT Schedule | 5 | 3 | 5 | **75** | TIER 2 | P3 |
| 4 | VAT on Real Property | 4 | 4 | 4 | **64** | TIER 2 | — |
| 5 | CWT Rate and Timing | 5 | 4 | 3 | **60** | TIER 2 | — |
| 5 | Transfer Tax | 4 | 5 | 3 | **60** | TIER 2 | — |
| 7 | CGT Computation | 3 | 5 | 3 | **45** | TIER 3 | — |
| 8 | Highest-of-Three Base | 4 | 5 | 2 | **40** | TIER 3 | — |
| 8 | DST on Mortgage | 5 | 4 | 2 | **40** | TIER 3 | — |
| 10 | EWT Rate Classification | 2 | 5 | 2 | **20** | TIER 4 | — |
| 10 | Form 2307 Issuance | 2 | 5 | 2 | **20** | TIER 4 | — |
| 12 | DST on Conveyance | 2 | 5 | 1 | **10** | TIER 4 | — |

**Deep-Dive column** = recommended for a dedicated reverse loop (comparable to the [inheritance engine](https://github.com/clsandoval/monorepo/tree/main/loops/inheritance-reverse)). P0/P1/P2/P3 = priority order. P2 is a unified ONETT engine covering CGT + CWT + VAT + DST + Transfer Tax (entries #4–8).

---

## TIER 1 — Highest Opportunity

---

### #1. Zonal Value Lookup Engine

**Composite Score: 125 (AG 5 × MF 5 × MD 5)**
**Structural Complexity: 12/15 (VERY HIGH)**
**Deep-dive priority: P0**

#### What It Computes

| | |
|---|---|
| **Inputs** | Property address (barangay, street, vicinity), city/municipality, land area (sqm), property classification code (RR/CR/RC/CC/I/A1–A50), transaction date |
| **Output** | `zonal_value_total` (PHP) = `zonal_value_per_sqm × land_area_sqm` |
| **Algorithm** | 5-step resolution pipeline: (1) address → RDO jurisdiction mapping, (2) RDO + date → applicable schedule revision, (3) address matching in heterogeneous Excel workbook, (4) classification code resolution, (5) value extraction × area |

This is not a tax formula — it is a **data infrastructure component**. Resolving it unlocks 5 downstream computations (CGT, DST on sale, CWT, VAT, transfer tax) that all share the same "highest-of-three" tax base.

#### Legal Basis

- NIRC Section 6(E) — Commissioner's authority to prescribe zonal values
- RMO No. 31-2019 — Annex B (classification codes) and Annex C (schedule format)
- RMC 115-2020 — Certification no longer required for ONETT
- RAMO 2-91 — 6-level fallback hierarchy when exact match fails
- RA 12001 / RPVARA (June 2024) — Transfers authority from BIR to BLGF; 2-year transition through mid-2026

#### Current State

**Fully manual.** Practitioners download ZIP files from bir.gov.ph, unzip heterogeneous Excel workbooks (124 RDOs), manually search for the property street/barangay, and read the value. Takes 15–60 minutes per property. Common workaround: call the RDO directly. Third-party platforms (Housal: 1.96M records, RealValueMaps: 2.7M records, REN.PH: 233K records) have digitized the data but offer **no API** and no integration with tax computation workflows.

#### Complexity Estimate

| Dimension | Score | Detail |
|---|---|---|
| Branching rules | 3/5 | 10+ branches: RDO mapping, effectivity dates, 16+ classification codes, land/condo bifurcation, 6-level fallback chain |
| Lookup tables | 5/5 | 124 heterogeneous Excel workbooks, RDO jurisdiction table, classification code reference, effectivity date registry |
| External data | 4/5 | BIR Excel workbooks (no API), property address, DOF Department Orders, Tax Declaration classification |

**Key complexity drivers:** (1) 124 heterogeneous workbooks with different column layouts, merged cells, header structures; (2) address matching ambiguity — vicinity descriptors like "Ayala Avenue from EDSA to Gil Puyat" require geocoding; (3) image-based PDFs for some RDOs requiring OCR; (4) RPVARA dual-source transition (BIR ZV + BLGF SMV simultaneously during 2026–2027).

#### Competitive Gap

**ABSOLUTE GAP.** No Philippine tax tool — JuanTax, Taxumo, QNE Cloud, or any ERP — provides API-accessible zonal value lookup integrated into tax computation. BIR eONETT resolves zonal values internally but is officer-mediated (2–8 week turnaround). All existing web calculators require manual zonal value entry.

#### Moat

**Maximum defensibility.** Data engineering moat: parsing 124 heterogeneous workbooks, address normalization (Filipino/Spanish names, abbreviations), OCR pipeline, ongoing update monitoring (38% of schedules outdated per DOF 2024), and 6-level fallback hierarchy. First-mover data advantage compounds over time. RPVARA transition creates a time-limited window — builders who establish pipelines before mid-2026 capture both regimes.

---

### #1. RPT Computation Engine (Real Property Tax)

**Composite Score: 125 (AG 5 × MF 5 × MD 5)**
**Structural Complexity: 13/15 (VERY HIGH)**
**Deep-dive priority: P1**

#### What It Computes

| | |
|---|---|
| **Inputs** | Property FMV (land, building, machinery separately), property classification (6 land classes, 4 building classes, 4 machinery classes), LGU type, LGU-enacted basic RPT rate, idle land status, payment/due dates |
| **Output** | `Annual RPT = (AV × basic_rate) + (AV × 1% SEF)` where `AV = FMV × assessment_level` |
| **Formula** | For each component: `AV = FMV × AL(class, FMV_bracket)`; sum components; apply `basic_rate + SEF_1%`; add idle land tax if applicable; compute late penalty (2%/month, 36-month cap) |

#### Legal Basis

- RA 7160 Secs. 199, 218 (assessment levels), 233 (rate caps), 235 (SEF), 236–237 (idle land), 255 (late penalty)
- DOF Local Assessment Regulations No. 1-92 — Complete assessment level bracket tables
- RA 12001 / RPVARA (June 2024) — Standardized SMV, 6% first-year RPT cap, 2-year amnesty

#### Current State

**Manual to semi-automated.** Online RPT payment portals exist in ~10 cities (Manila, Makati, QC) but are **payment-only**, not computation engines. No tool computes RPT across all 1,700+ LGUs with correct locally-enacted rates and assessment levels. Property managers with multi-LGU portfolios use custom Excel spreadsheets. RPT payment typically requires 1–3 days/year for multi-property owners including in-person visits.

#### Complexity Estimate

| Dimension | Score | Detail |
|---|---|---|
| Branching rules | 5/5 | 20+ branches: 6 land classes, 9-tier residential building brackets, 6-tier agricultural, 8-tier commercial/industrial, 4 machinery classes, idle land, late penalty with 36-month cap |
| Lookup tables | 5/5 | 7 distinct tables: land AL, 3 building bracket tables, machinery AL, LGU rate database (1,700+ LGUs), idle land rate |
| External data | 3/5 | LGU ordinance rates, assessor FMV/SMV, RPVARA transition status |

**Critical correction confirmed in analysis:** ALL cities (not just Metro Manila) can levy up to 2% basic RPT (Section 233). Many practitioner guides incorrectly state non-MM cities are capped at 1%. Agricultural building max AL is 50% (not 80% as some guides state).

#### Competitive Gap

**ABSOLUTE GAP for full-LGU coverage.** No tool covers all 1,700+ LGUs with correct locally-enacted rates. Existing online portals are city-specific and payment-only. No centralized LGU rate database exists — each LGU enacts its own rate by ordinance.

#### Moat

**Maximum defensibility.** The 1,700-LGU rate database is the dominant moat: compiling locally-enacted rates across every Philippine city, municipality, and province, each with its own tax ordinance, assessment level schedule, and rate adjustments. Database requires ongoing maintenance as LGUs amend ordinances. RPVARA (RA 12001) introduces standardized SMV + 6% first-year RPT cap, adding a transition-period branch.

---

## TIER 2 — Strong Opportunity

---

### #3. Installment VAT Schedule Engine

**Composite Score: 75 (AG 5 × MF 3 × MD 5)**
**Structural Complexity: 7/15 (MEDIUM structurally; HIGH operationally)**
**Deep-dive priority: P3**

#### What It Computes

| | |
|---|---|
| **Inputs** | Contract price, FMV tax base (max of zonal/assessor), initial payments in year of sale, assumed mortgage, seller's cost basis, full payment schedule (date + principal + interest + penalty per period), transaction date |
| **Output** | Per-collection output VAT schedule across 2–30+ years: `{quarter, collections, output_vat, cumulative_vat, remaining_balance}` with recognition method (installment vs. cash sale) |
| **Formula** | **Gate:** `adjusted_initial_payments / contract_price ≤ 25%?` → installment plan (per-collection VAT) or cash sale (full VAT at sale). **Scenario A** (contract ≥ FMV): `output_vat = collection × 12%`. **Scenario B** (FMV > contract): `output_vat = (collection / contract_price) × FMV × 12%` |

#### Legal Basis

- NIRC Section 106; RR 16-2005 Sec. 4.106-3 as amended by RR 4-2007
- RMC 99-2023 — BIR clarification on installment VAT recognition
- RMC 05-2023 — Abolished mandatory monthly 2550M
- RA 11976 / EOPT Act — Restructured invoice/receipt framework (OR reclassified as supplementary)

#### Current State

**Fully manual.** No tool handles multi-period output VAT recognition with dual formula paths. QNE/JuanTax/Taxumo handle quarterly VAT filing (Form 2550Q) but not the per-project, per-unit installment schedule that developers need. A 500-unit project generates 500 individual VAT schedules spanning 5–30 years. Large developers use ERP+Excel hybrid (SAP/NetSuite + Excel sidecar for BIR-specific compliance). SMEs use Excel master spreadsheets with manual quarterly aggregation.

#### Complexity Estimate

| Dimension | Score | Detail |
|---|---|---|
| Branching rules | 2/5 | 7 branches: 25% test, simple vs. FMV-ratio formula, cash sale path, mortgage excess, pre/post-EOPT invoicing |
| Lookup tables | 1/5 | No rate tables — fixed at 12% |
| External data | 4/5 | Zonal value snapshot at sale date, assessor FMV, seller's cost basis, full payment schedule, transaction date |

**Structural vs. operational divergence:** Structurally simple (few branches, no rate tables), but 9 operational complexity drivers make this the most demanding computation to implement correctly: multi-period tracking (2–30 years), dual formula paths requiring zonal value snapshot, constructive receipt rules, cancellation/default reversal, interest and penalty VAT treatment, EOPT invoicing transition, quarterly 2550Q aggregation.

#### Competitive Gap

**ABSOLUTE GAP.** Zero tools handle the per-collection installment VAT schedule with dual formula paths. This is the highest-moat individual computation in the catalog.

#### Moat

**Maximum defensibility.** Getting all edge cases correct requires deep regulatory expertise (RR 4-2007 FMV-ratio formula, mortgage excess-over-basis exception, constructive receipt, cancellation reversal). Multi-period state management over decades creates implementation complexity that deters casual replication. Requires zonal value snapshot at sale date (historical data, not just current values).

---

### #4. VAT on Real Property

**Composite Score: 64 (AG 4 × MF 4 × MD 4)**
**Structural Complexity: 11/15 (HIGH)**

#### What It Computes

| | |
|---|---|
| **Inputs** | Asset classification (capital/ordinary), seller VAT registration status, property type (house & lot, condo, bare lot, commercial, socialized), gross selling price, BIR zonal value, assessor FMV, payment structure, initial payments in year 1, socialized housing qualification |
| **Output** | `vat_applies` (boolean), `tax_base`, `output_vat_total` (12% × base), `recognition_method` (full at sale / per collection), per-installment VAT schedule if applicable |
| **Formula** | 4-gate decision tree: (1) capital vs. ordinary → CGT if capital, (2) VAT registered? → 3% percentage tax if not, (3) exemption check → residential ≤ ₱3,600,000 or socialized housing exempt, (4) `output_vat = max(GSP, ZV, AFMV) × 12%` + installment 25% recognition test |

#### Legal Basis

- NIRC Sections 106, 109; RR 16-2005 Sec. 4.106-4; RR 1-2024 (threshold updated to ₱3,600,000 effective Jan 1, 2024)
- RMC 99-2023 — Deemed sale on donation; bank foreclosed property treatment

#### Current State

**Partially automated for filing, not for decision logic.** JuanTax and Taxumo handle quarterly 2550Q filing. eONETT assesses VAT on property sales but is officer-mediated. No tool implements the full 4-gate RE-specific decision tree (asset classification, registration check, residential threshold with CPI adjustment, socialized housing exemption) integrated with the 25% installment recognition test.

#### Complexity Estimate

| Dimension | Score | Detail |
|---|---|---|
| Branching rules | 3/5 | 8+ branches across 4 gates + installment timing |
| Lookup tables | 3/5 | Residential VAT-exempt threshold history (CPI-adjusted), VAT registration threshold |
| External data | 5/5 | 6 dependencies — asset classification, VAT registration, zonal value, assessor FMV, socialized housing, payment schedule |

Most external dependencies of any single computation. CPI-adjusted threshold tracking (₱3,600,000 as of Jan 2024, updated periodically) and bare lot exemption elimination (Jan 2021) add historical branching.

#### Competitive Gap

JuanTax/Taxumo handle VAT filing but not RE-specific decision logic. No tool handles the residential threshold with historical CPI adjustments, bare lot vs. house-and-lot distinction, or installment recognition integrated with 4-gate classification.

#### Moat

Strong but not maximum — 4-gate decision tree is the most intricate classification logic, but the law is public. CPI-threshold tracking and EOPT invoicing changes add ongoing maintenance depth. Two non-deterministic gates (asset classification, socialized housing) require careful user-input handling.

---

### #5. CWT Rate and Timing (Creditable Withholding Tax)

**Composite Score: 60 (AG 5 × MF 4 × MD 3)**
**Structural Complexity: 9/15 (HIGH)**

#### What It Computes

| | |
|---|---|
| **Inputs** | Seller habitually-engaged status, gross selling price, zonal value, assessor FMV, initial payments in year of sale, buyer trade/business status, assumed mortgage, seller's adjusted basis |
| **Output** | CWT amount, applicable rate (1.5%/3%/5%/6%), withholding timing (upfront / per-installment / at-last-installment) |
| **Formula** | `tax_base = max(GSP, ZV, AFMV)`; rate by seller classification: habitually engaged → 1.5% (≤₱500K) / 3% (≤₱2M) / 5% (>₱2M); not habitually engaged → 6% flat; banks → 6%. Timing: >25% initial → full at first installment; ≤25% + buyer in business → per-installment; ≤25% + individual buyer → at last installment |

#### Legal Basis

- RR 2-98 Sec. 2.57.2(J) as amended by RR 11-2018 — Rate table and thresholds
- RR 17-2003; RMO 33-2023 — 25% installment timing rule
- RMC 31-2025 — Form 2307 discontinued; Form 1606 is now seller's sole credit instrument
- BIR Ruling OT-028-2024 — Tax base fixed at date of sale for installment transactions

#### Current State

**Fully manual.** eONETT computes CWT but is officer-mediated (2–8 week turnaround). No self-service tool handles the tiered rates with installment timing bifurcation. Practitioners manually determine rate based on seller classification and compute timing based on buyer type.

#### Complexity Estimate

| Dimension | Score | Detail |
|---|---|---|
| Branching rules | 3/5 | 10 branches: 3-tier rate for habitually engaged, flat rate for non-habitual, socialized exemption, 3-branch installment timing by buyer type, bank exception |
| Lookup tables | 2/5 | Simple 3-tier rate schedule (₱500K/₱2M thresholds) |
| External data | 4/5 | Zonal value, assessor FMV, habitually-engaged status, buyer trade/business status, seller's cost basis |

#### Competitive Gap

**ABSOLUTE GAP.** No tool handles CWT rate tiering (1.5/3/5/6%) or installment timing bifurcation. Material RMC 31-2025 update: Form 1606 replaces Form 2307 as seller's credit instrument — no tool has adapted to this yet.

#### Moat

Moderate — rate table is compact (4 rates, 2 thresholds) but the habitually-engaged determination (6-transaction test combining buys and sells), installment timing bifurcation (3 branches by buyer type), and zonal value dependency add meaningful depth. Shares data infrastructure with CGT/DST.

---

### #5. Transfer Tax

**Composite Score: 60 (AG 4 × MF 5 × MD 3)**
**Structural Complexity: 9/15 (HIGH, but LOW marginal once shared infra exists)**

#### What It Computes

| | |
|---|---|
| **Inputs** | Selling price, zonal value, assessor FMV, improvement FMV, LGU type, LGU-enacted rate, transfer type, deed date, CARP exemption status |
| **Output** | `transfer_tax = max(consideration, FMV) × lgu_enacted_rate` |
| **Formula** | `tax_base = max(SP, zonal × area + improvements, assessor_FMV + improvements)`; `transfer_tax = tax_base × rate` (0.50% provinces/non-MM municipalities; up to 0.75% cities/MM municipalities via Sections 144/151 uplift) |

#### Legal Basis

- RA 7160 Sec. 135(a) — Transfer tax authority; CARP exemption
- RA 7160 Sec. 144 (MM municipality uplift) and Sec. 151 (city uplift) — Derive 0.75% cap
- RA 7160 Sec. 168 — Late penalty: 25% surcharge + 2%/month interest, 36-month cap

**Source conflict resolved:** Respicio.ph incorrectly attributes 0.75% rate to RA 9640 — confirmed false; RA 9640 only amends Section 140 (amusement tax). Inheritance/extrajudicial settlement confirmed NOT exempt (contradicts some practitioner guides).

#### Current State

**Fully manual, in-person only.** Paid at LGU Treasurer's Office. No centralized rate database. Sequential bottleneck in ONETT pipeline — requires eCAR first, then transfer tax, then title transfer at Registry of Deeds. Each LGU has its own form.

#### Complexity Estimate

| Dimension | Score | Detail |
|---|---|---|
| Branching rules | 3/5 | 8 branches: 4 LGU types, CARP exemption, transfer type, installment flag, LGU-specific exemptions |
| Lookup tables | 3/5 | LGU rate database (shared with RPT), zonal value, assessor FMV |
| External data | 3/5 | LGU rate ordinances, zonal value, assessor FMV |

#### Competitive Gap

No tool computes transfer tax with correct per-LGU rates. Web calculators use generic 0.5–0.75% estimates. The correct rate depends on LGU type and locally-enacted ordinance.

#### Moat

Formula is simple (`base × rate`), but LGU rate database is the moat — **same database needed for RPT**. Marginal build cost approaches zero once RPT engine (with its 1,700-LGU database) exists. Best viewed as a free add-on to RPT, not a standalone opportunity.

---

## TIER 3 — Moderate Opportunity

---

### #7. CGT Computation (Capital Gains Tax)

**Composite Score: 45 (AG 3 × MF 5 × MD 3)**
**Structural Complexity: 10/15 (HIGH)**

#### What It Computes

| | |
|---|---|
| **Inputs** | Gross selling price, zonal value/sqm, area, assessor FMV, sale date, principal residence status (5 conditions), proceeds reinvested, taxpayer size (micro/small/medium/large), installment payment details |
| **Output** | CGT amount (6% of tax base), filing deadline (30 days from notarization), penalty computation (tiered by taxpayer size under EOPT) |
| **Formula** | `tax_base = max(GSP, ZV × area, AFMV)`; `CGT = 6% × tax_base`. Principal residence partial exemption: `taxable = (1 - reinvested/GSP) × tax_base`. Installment: Option A (upfront full) or Option B (proportional per collection) |

#### Legal Basis

- NIRC Secs. 24(D)(1), 27(D)(5), 24(D)(2); RR 13-99 (principal residence exemption)
- RA 11976 / EOPT Act — Tiered penalties: micro/small get 10% surcharge + 6% interest vs. standard 25%/12%

#### Current State

**Partially automated.** JuanTax supports Form 1706 filing. eONETT computes CGT (officer-mediated). Web calculators (Housal, ForeclosurePhilippines) compute basic 6% × max(SP,ZV,AFMV). **Gaps:** installment CGT (2-option regime), principal residence exemption (partial computation with escrow for GSP > ₱5M), EOPT tiered penalties.

#### Complexity Estimate

11 material decision branches including installment (2 options), principal residence exemption (5 binary conditions + escrow), EOPT penalty tiers (4 categories). 2 lookup tables (EOPT tier table, exemption checklist). 5 external data dependencies (zonal value, assessor FMV, taxpayer size, capital asset classification, exemption history).

**Non-deterministic prerequisite:** Capital vs. ordinary asset classification (RR 7-2003) — requires judgment; handled as user input.

#### Competitive Gap

Basic computation covered by multiple tools. The gap is in advanced features: installment handling, partial exemption formula (RR 13-99 method diverges when ZV > GSP), EOPT penalty tiering. Partial exemption formula conflict documented — RR 13-99 uses `unutilized_ratio × tax_base`, not `unutilized_ratio × GSP`.

#### Moat

Moderate. Law is public and well-documented. 11 branches and EOPT tiering add depth but are replicable by a competent developer reading the regulations. Value is in getting edge cases right (escrow mechanics, installment options, correct partial exemption formula).

---

### #8. Highest-of-Three Tax Base Resolution

**Composite Score: 40 (AG 4 × MF 5 × MD 2)**
**Structural Complexity: 5/15 (LOW)**

#### What It Computes

| | |
|---|---|
| **Inputs** | Gross selling price (PHP), BIR zonal value per sqm (PHP), land area (sqm), assessor FMV (PHP) |
| **Output** | `tax_base = max(GSP, ZV × area, AFMV)` — single value feeding all 5 transaction taxes |
| **Formula** | Statutory two-step: `FMV_6E = max(ZV, AFMV)`; `tax_base = max(GSP, FMV_6E)` — computationally equivalent to `max(a, b, c)` |

#### Legal Basis

- NIRC Sec. 6(E) — FMV = higher of zonal and assessor; Sec. 24(D), 196, 57, 106 — Each tax references "SP or FMV, whichever higher"
- BIR Ruling OT-028-2024 — Tax base fixed at date of sale for installment transactions
- RA 12001 / RPVARA — Three-way max will collapse to two-way max (SP vs. unified SMV) post-transition

#### Current State

Computed manually in every real estate tax calculation. Web calculators require manual input of all three values. eONETT resolves it internally but is officer-mediated. No tool integrates automated zonal value lookup into this comparison.

#### Complexity Estimate

Formula is `max(a, b, c)` — trivially low. All complexity resides in acquiring the inputs, particularly the zonal value (scored separately). RPVARA will simplify to `max(a, b)` post-transition.

#### Competitive Gap

Meaningful gap in **automated integration** (no tool connects zonal value lookup → three-way comparison → tax computation). Near-zero gap in the comparison formula itself.

#### Moat

Near-zero standalone moat. This is an **integration layer**, not a defensible computation. All moat resides in the zonal value data pipeline (entry #1). Valuable as architecture but not as a product.

---

### #8. DST on Mortgage (Section 195)

**Composite Score: 40 (AG 5 × MF 4 × MD 2)**
**Structural Complexity: 7/15 (MEDIUM)**

#### What It Computes

| | |
|---|---|
| **Inputs** | Amount secured (PHP), instrument date, instrument type (regular/open-end/OLSA) |
| **Output** | DST amount using stepped schedule |
| **Formula** | Post-TRAIN (≥ Jan 1, 2018): `DST = ₱40 + ceil((amount - ₱5,000) / ₱5,000) × ₱20` for amounts > ₱5,000; `DST = ₱40` for amounts ≤ ₱5,000. Pre-TRAIN: base ₱20, incremental ₱10. Effective rate: ~0.40% asymptote for large amounts |

#### Legal Basis

- NIRC Section 195 as amended by RA 10963 (TRAIN) / RR 4-2018 — Rate doubling
- NIRC Section 200 — Filing deadline (5 days after month-end)
- RR 9-94 — OLSA single-instrument exception (use Section 179 rate instead)

**Source conflict resolved:** Wave 1 cache incorrectly stated post-TRAIN incremental as ₱40; verified correct incremental is ₱20 against 5+ sources (NTRC Tax Research Journal, SC E-Library RA 10963, RR 4-2018 full text).

#### Current State

**Fully manual.** Zero tools compute the Section 195 stepped schedule. Even practitioner guides frequently get the rate wrong. Banks and financial institutions compute this internally but no public-facing calculator exists.

#### Complexity Estimate

| Dimension | Score | Detail |
|---|---|---|
| Branching rules | 2/5 | 5 branches: pre/post-TRAIN date gate, ≤₱5K flat, >₱5K stepped, open-end/revolving, OLSA exception |
| Lookup tables | 2/5 | Pre-TRAIN and post-TRAIN rate schedules (simple 2-row tables) |
| External data | 3/5 | Amount from loan documents, instrument date, instrument type classification |

Self-contained computation — **no zonal value dependency**. All rates are statutory constants.

#### Competitive Gap

**ABSOLUTE GAP.** Literally zero tools compute this. Maximum gap score of any computation.

#### Moat

Low — stepped arithmetic is unique among PH taxes but straightforward once Section 195 is correctly read. Any competent developer can replicate in hours. Value is in being the **first to offer it at all**. Quick win for differentiation at near-zero build cost.

---

## TIER 4 — Low Priority (Include for Completeness)

---

### #10. EWT Rate Classification

**Composite Score: 20 (AG 2 × MF 5 × MD 2)**
**Structural Complexity: 11/15 (HIGH)**

#### What It Computes

EWT decision tree for real estate-adjacent payments: professional fees to RESP (5%/10%/15% tiered by income and license status), rental income (5% flat), commissions (aligned with professional fee rates post-RR 11-2018), contractor payments (2% flat). 15+ material decision branches across 4 payment categories.

#### Legal Basis

RR 2-98 as amended by RR 11-2018 — Post-TRAIN rates; RMC 11-2024 — PFRS 16 ROU asset EWT clarification.

#### Current State

**Best-covered computation.** QNE Cloud has predefined ATC codes with auto-compute. JuanTax and Taxumo handle Form 1601-EQ with rate selection and Form 2307 generation.

#### Competitive Gap

Minimal. Existing tools already encode the full ATC rate table. Include in a comprehensive engine for table-stakes capability but no differentiation.

---

### #10. Form 2307 Issuance Logic

**Composite Score: 20 (AG 2 × MF 5 × MD 2)**
**Structural Complexity: 10/15 (HIGH)**

#### What It Computes

Withholding agent determination, amount computation (`gross_payment × ATC_rate` with monthly breakdown), issuance timing (20 days after quarter-end), and bilateral reconciliation chain (payor: 0619-E → 1601-EQ → 1604-E + Alphalist + DAT file; payee: Form 2307 → SAWT → ITR credit claim).

#### Legal Basis

NIRC Sec. 57, 58(B); RR 2-98 as amended; RR 2-2006 (SAWT); RMC 31-2025 (Form 2307 discontinued for CWT — Form 1606 replaces); RMC 14-2025 (digital copies acceptable).

#### Current State

**Partially automated.** JuanTax, QNE, Taxumo all generate Form 2307. BIR Online Tools and BIR Excel Uploader provide free alternatives. Reconciliation is "most frustrating part of PH tax compliance" per practitioners — but this is a **workflow problem**, not a computation problem.

#### Competitive Gap

Minimal for computation. Opportunity exists in bilateral reconciliation automation (payor-payee matching, SAWT attachment, DAT file generation for alphalist) — but this is workflow automation, not tax computation.

---

### #12. DST on Conveyance (Sale)

**Composite Score: 10 (AG 2 × MF 5 × MD 1)**
**Structural Complexity: 6/15 (MEDIUM)**

#### What It Computes

`DST = max(GSP, ZV, AFMV) × 1.5%` with ceiling-to-nearest-₱15 rule. Form 2000-OT, 5 days after month-end. Applies to ALL real property conveyances (both capital and ordinary assets).

#### Legal Basis

NIRC Section 196 (rate unchanged since RA 7660 in 1994; TRAIN only added donations to scope); RR 6-2001 / RMC 67-2024 (5-day filing deadline).

#### Current State

Multiple tools cover this. JuanTax supports Form 2000-OT. Web calculators compute 1.5% readily. eONETT includes DST in its assessment.

#### Competitive Gap

Near-zero. Formula is `base × 0.015` with a ceiling function.

#### Moat

Zero. Trivially replicable by any developer in minutes. Include in any comprehensive engine (marginal build cost is zero once highest-of-three base exists) but never lead with it.

---

## Strategic Build Clusters

The 12 computations naturally cluster into four build strategies with infrastructure dependencies:

### Cluster A: Data Infrastructure (Build First)
**Components:** Zonal Value Lookup (#1) + Highest-of-Three Base (#8)
**Aggregate Score:** 125 + 40 = 165
**Why first:** Zonal value is the bottleneck for 5 downstream computations. Maximum leverage. Durable data moat.
**Deep-dive loop:** YES (P0) — comparable to inheritance engine in scope.

### Cluster B: ONETT Transaction Tax Engine (Build Second)
**Components:** CGT (#7) + DST on Sale (#12) + CWT (#5) + VAT (#4) + Transfer Tax (#5) + DST on Mortgage (#8)
**Aggregate Score:** 45 + 10 + 60 + 64 + 60 + 40 = 279
**Why second:** Once Cluster A provides the zonal value engine, all transaction taxes share the same tax base. Build as a unified engine: input a transaction → output all applicable taxes (CGT or CWT+VAT depending on asset type, plus DST, transfer tax). DST on mortgage is a standalone add-on (no zonal dependency).
**Deep-dive loop:** YES (P2) — ~50 decision branches, 6 tax types, shared infrastructure.

### Cluster C: Developer Tools (Build Third)
**Components:** Installment VAT Schedule (#3) + Installment CGT (within #7)
**Aggregate Score:** 75 (installment VAT alone)
**Why third:** Highest moat computation. Multi-period tracking over decades. Narrow market (developers only) but massive per-client volume. Best positioned as premium tier.
**Deep-dive loop:** YES (P3) — 9 complexity drivers, multi-period state management.

### Cluster D: Recurring Compliance (Parallel Track)
**Components:** RPT (#1) + Transfer Tax (#5, shared LGU DB) + EWT (#10) + Form 2307 (#10)
**Aggregate Score:** 125 + 60 + 20 + 20 = 225
**Why parallel:** RPT is independent of zonal value (uses assessor FMV). LGU rate database serves both RPT and transfer tax. EWT and Form 2307 are table-stakes inclusions.
**Deep-dive loop:** RPT YES (P1); EWT/Form 2307 NO (already well-served).

### Recommended Deep-Dive Priority

| Priority | Target | Estimated Scope | Time-Sensitivity |
|---|---|---|---|
| **P0** | Zonal Value Lookup Engine | 124 RDO workbooks, address normalization, OCR, fallback logic, RPVARA dual-source | HIGH — RPVARA transition creates first-mover window through mid-2026 |
| **P1** | RPT Computation Engine | 1,700-LGU database, 7 lookup tables, assessment level encoding, RPVARA handling | MEDIUM — annual cycle, steady demand |
| **P2** | ONETT Transaction Tax Engine | ~50 decision branches, 6 tax types, installment handling, penalty tiers | MEDIUM — eONETT improving but still officer-mediated |
| **P3** | Installment VAT Schedule Engine | Multi-period (2–30yr) tracking, dual formula paths, cancellation reversal | LOW — niche but deep moat |

---

## Key Findings

1. **Two infrastructure components dominate:** Zonal Value Lookup and RPT Computation both score 125/125. They represent different moat types (data pipeline vs. LGU rate database) and serve different markets (transaction vs. recurring). Build both.

2. **The automation gap is binary, not gradual.** Computations are either well-covered (EWT, Form 2307, DST on sale — AG score 2/5) or completely uncovered (CWT, installment VAT, RPT, zonal value, DST on mortgage — AG score 5/5). No middle ground. This is greenfield vs. competitive, not incremental improvement.

3. **Shared infrastructure creates compounding value.** The zonal value engine unlocks 5 computations; the LGU database unlocks 2. Total catalog value far exceeds the sum of individual computations. Build infrastructure first, domain computations second.

4. **Frequency is uniformly high — moat is the differentiator.** 9 of 12 computations score 4–5 on market frequency. The ranking is determined by automation gap × moat. Data-intensive, regulation-deep computations (zonal value, RPT, installment VAT) are the highest-value targets.

5. **RPVARA creates a time-limited first-mover window.** RA 12001 (June 2024, effective ~mid-2026) transfers zonal value authority from BIR to BLGF and introduces standardized SMV. Builders who establish data pipelines before the transition capture the dual-source period and lock in coverage as the new system stabilizes.

6. **Four non-deterministic gates bound automation scope.** Capital/ordinary asset classification, employment vs. contractor test, socialized housing qualification, and habitually-engaged seller determination all require judgment. These are handled as user inputs with clear branching, not automated classification.

---

## Appendix: Source Summary

All computations verified against 2+ independent sources per the loop's verification protocol. Primary legal sources: NIRC (RA 8424 as amended by TRAIN/RA 10963 and EOPT/RA 11976), RA 7160 (Local Government Code), RA 12001 (RPVARA). Key BIR issuances: RR 2-98, RR 7-2003, RR 16-2005, RR 4-2007, RR 4-2018, RR 11-2018, RR 1-2024, RMC 99-2023, RMC 05-2023, RMC 31-2025, RMC 56-2024, RMO 31-2019. Secondary sources: PwC PH, Grant Thornton PH, Forvis Mazars PH, KPMG PH, BDB Law, Respicio & Co., Ocampo & Suralvo, AJA Law, Tax & Accounting Center PH, ForeclosurePhilippines.com, NTRC Tax Research Journal. Full citations in individual analysis files under `analysis/`.
