# Complexity Scoring — Per-Computation Structural Analysis

**Wave:** 3 (Competitive & Automation Gap Analysis)
**Date:** 2026-02-26
**Depends on:** All Wave 2 computation extractions

## Methodology

Each computation is scored on three structural dimensions:

| Dimension | What It Measures | Scale |
|---|---|---|
| **Branching Rules (BR)** | Number of material decision branches, conditional paths, and edge cases | 1 (≤3) → 2 (4–7) → 3 (8–12) → 4 (13–17) → 5 (18+) |
| **Lookup Tables (LT)** | Count of distinct lookup tables, rate schedules, or bracket tables required | 1 (0) → 2 (1) → 3 (2–3) → 4 (4–5) → 5 (6+) |
| **External Data Dependencies (ED)** | Count of data sources outside the computation that must be resolved | 1 (≤1) → 2 (2) → 3 (3) → 4 (4–5) → 5 (6+) |

**Composite Complexity Score** = BR + LT + ED (range: 3–15)

Classification:
- **3–5:** LOW — trivial formula, minimal dependencies
- **6–8:** MEDIUM — moderate branching or data dependencies
- **9–11:** HIGH — significant branching + external dependencies
- **12–15:** VERY HIGH — deep decision trees + multiple lookup tables + many external dependencies

## Per-Computation Scoring

### 1. Highest-of-Three Tax Base Resolution

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 3 (three-way max + 6 edge cases) | 1 | Formula is `max(a,b,c)` — edge cases are input-level, not formula-level |
| Lookup Tables | 0 | 1 | Pure comparison; no rate tables |
| External Dependencies | 3 (zonal value, assessor FMV, selling price) | 3 | ZV is hardest — no API, 124 heterogeneous workbooks |

**Composite: 5 (LOW)**
Formula trivial. All complexity lives in populating the three inputs, particularly zonal value lookup (scored separately).

---

### 2. Capital Gains Tax (CGT)

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 11 | 3 | Standard path, principal residence exemption (full + partial), government sale election, installment (2 options), EOPT penalty tiers (4 size categories), surcharge type |
| Lookup Tables | 2 (EOPT penalty tier table, exemption checklist) | 3 | Penalty rates differ by taxpayer size; exemption has 5 binary conditions |
| External Dependencies | 5 (zonal value, assessor FMV, taxpayer size, capital asset classification, BIR exemption history) | 4 | Capital asset classification is non-deterministic gate |

**Composite: 10 (HIGH)**
Core formula (6% × base) is simple, but 11 material branches and a non-deterministic prerequisite (capital vs. ordinary asset) make this structurally complex. Installment logic and EOPT penalty tiering add depth.

---

### 3. DST on Conveyance (Sale)

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 7 (asset type check, 5 exemption checks, equal-share partition) | 2 | Most branches are binary exemption gates |
| Lookup Tables | 0 | 1 | Fixed rate: 1.5% with ceiling function |
| External Dependencies | 3 (zonal value, assessor FMV, exemption qualification docs) | 3 | Shares ZV dependency with CGT |

**Composite: 6 (MEDIUM)**
Simplest of the real property transfer taxes. One rate, one formula, shared data dependencies. Near-zero marginal complexity once highest-of-three base engine exists.

---

### 4. DST on Mortgage

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 5 (pre/post-TRAIN date gate, ≤₱5K flat, >₱5K stepped, open-end/revolving, OLSA exception) | 2 | Stepped arithmetic with date-gated rate selection |
| Lookup Tables | 1 (pre-TRAIN / post-TRAIN rate schedule) | 2 | Two-row table: base amount + increment per band |
| External Dependencies | 3 (amount secured, instrument date, instrument type classification) | 3 | All from loan documents; no external government data needed |

**Composite: 7 (MEDIUM)**
Self-contained computation. No zonal value dependency. Stepped schedule is slightly more complex than flat-rate DST on sale but still straightforward.

---

### 5. VAT on Real Property

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 8+ (capital/ordinary gate, VAT registration check, socialized housing, residential threshold, bare lot elimination, tax base resolution, VAT-inclusive/exclusive, installment 25% test) | 3 | 4-gate decision tree + installment timing bifurcation |
| Lookup Tables | 2 (residential VAT-exempt threshold history, VAT registration threshold) | 3 | Threshold updated periodically by CPI adjustment |
| External Dependencies | 6 (asset classification, VAT registration status, zonal value, assessor FMV, socialized housing qualification, payment schedule) | 5 | Most external dependencies of any single computation |

**Composite: 11 (HIGH)**
High complexity driven by multiple non-deterministic gates (asset classification, socialized housing) and the most external dependencies. Installment recognition adds multi-period tracking requirement.

---

### 6. Installment VAT Schedule

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 7 (25% test, simple vs. FMV-ratio formula, cash sale path, mortgage excess, pre/post-EOPT invoicing) | 2 | Two formula paths + invoicing regime |
| Lookup Tables | 0 | 1 | All rates fixed at 12%; no lookup tables |
| External Dependencies | 5 (zonal value snapshot at sale date, assessor FMV, seller's cost basis, full payment schedule, transaction date) | 4 | Multi-period tracking is the core challenge |

**Composite: 7 (MEDIUM)**
Formula branches are few, but 9 complexity drivers (multi-period tracking over 2–30+ years, constructive receipt, cancellation reversal) make this operationally demanding despite a low structural score. **Operational complexity exceeds structural complexity.**

---

### 7. CWT Rate and Timing

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 10 (capital/ordinary gate, 3-tier rate for habitually engaged, flat rate for non-habitual, socialized housing exemption, 3-branch installment timing by buyer type, bank exception) | 3 | Rate selection + installment timing bifurcation |
| Lookup Tables | 1 (3-tier CWT rate schedule: ₱500K / ₱2M thresholds) | 2 | Simple bracket table |
| External Dependencies | 5 (zonal value, assessor FMV, habitually-engaged status, buyer trade/business status, seller's cost basis) | 4 | Habitually-engaged determination has non-deterministic aspects |

**Composite: 9 (HIGH)**
Rate selection requires seller classification (habitually engaged test), and installment timing depends on buyer classification — two external determinations. Combined with zonal value dependency, this is structurally complex.

---

### 8. EWT Rate Classification

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 15+ (7 professional fee paths, 2 rental paths, commission alignment, contractor flat rate, 4 withholding agent obligation paths) | 4 | Deepest decision tree of all computations |
| Lookup Tables | 3 (EWT rate table by payee type/income, sworn declaration mechanics, TWA threshold table) | 3 | Multiple interacting tables |
| External Dependencies | 4 (PRC license status, payee gross income, VAT registration, employment classification) | 4 | Employment vs. contractor is non-deterministic |

**Composite: 11 (HIGH)**
Most branching rules of any computation. 15+ material decision branches across 4 payment categories. However, all data dependencies are payee-provided (no government database lookups), so implementation is more about decision tree encoding than data pipeline.

---

### 9. Real Property Tax (RPT)

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 20+ (LGU type, 6 land classes, 9-tier residential building brackets, 6-tier agricultural, 8-tier commercial/industrial, 4 machinery classes, idle land, late penalty) | 5 | Most branching rules of any computation |
| Lookup Tables | 7 (land AL table, 3 building bracket tables, machinery AL table, LGU rate database, idle land rate) | 5 | Most lookup tables of any computation |
| External Dependencies | 3 (LGU ordinance rates, assessor FMV/SMV, RPVARA transition status) | 3 | LGU database is massive (1,700+ LGUs) but static once built |

**Composite: 13 (VERY HIGH)**
Structurally the most complex computation. 20+ branches across multiple property classifications, 7 distinct lookup tables, and a 1,700-LGU rate database. However, the formula itself is fully deterministic once inputs are resolved — no judgment calls needed.

---

### 10. Transfer Tax

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 8 (4 LGU type/rate branches, CARP exemption, transfer type, installment flag, LGU-specific exemptions) | 3 | Moderate branching, mostly LGU-type based |
| Lookup Tables | 3 (LGU rate database, zonal value, assessor FMV) | 3 | Shares LGU database with RPT |
| External Dependencies | 3 (LGU rate ordinances, zonal value, assessor FMV) | 3 | Same shared dependencies |

**Composite: 9 (HIGH)**
Score inflated by shared infrastructure dependencies (LGU database, zonal value). Marginal complexity is LOW once RPT and CGT engines exist — the formula itself is `base × rate` with minimal branching.

---

### 11. Form 2307 Issuance Logic

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 8+ (withholding agent determination, 8 ATC categories with threshold/declaration gates) | 3 | ATC-level branching with payee classification |
| Lookup Tables | 2 (ATC code-to-rate mapping, EOPT penalty tier table) | 3 | Static tables; updated only on RR amendments |
| External Dependencies | 4 (payee TIN, gross income declaration, VAT registration, DAT file format specs) | 4 | Multi-period tracking + bilateral reconciliation chain |

**Composite: 10 (HIGH)**
Formula is trivial (`gross_payment × rate`) but the filing chain complexity (0619-E → 1601-EQ + QAP → 1604-E + Alphalist) and bilateral reconciliation (payor vs. payee SAWT) make this operationally demanding. DAT file generation is a significant implementation challenge.

---

### 12. Zonal Value Lookup

| Dimension | Raw Count | Score | Notes |
|---|---|---|---|
| Branching Rules | 10+ (RDO mapping, effectivity date, address matching hierarchy, 16+ classification codes, land/condo bifurcation, 6-level fallback chain) | 3 | Not a formula — a data resolution pipeline |
| Lookup Tables | 5+ (RDO jurisdiction table, 124 Excel workbooks, classification code reference, effectivity date registry, fallback rules) | 5 | 124 heterogeneous workbooks is the dominant challenge |
| External Dependencies | 5 (BIR Excel workbooks, property address, DOF Department Orders, Tax Declaration classification, third-party data) | 4 | No API; format inconsistency across 124 RDOs |

**Composite: 12 (VERY HIGH)**
Not a tax computation per se — it's a data infrastructure component. Highest leverage in the entire catalog: resolving zonal value unlocks CGT, DST on Sale, CWT, VAT, and Transfer Tax simultaneously. RPVARA transition (BIR ZV → BLGF SMV by mid-2026) adds dual-source handling requirement.

---

## Summary Ranking by Composite Complexity Score

| Rank | Computation | BR | LT | ED | Composite | Classification |
|---:|---|:---:|:---:|:---:|:---:|---|
| 1 | RPT Computation | 5 | 5 | 3 | **13** | VERY HIGH |
| 2 | Zonal Value Lookup | 3 | 5 | 4 | **12** | VERY HIGH |
| 3 | EWT Rate Classification | 4 | 3 | 4 | **11** | HIGH |
| 3 | VAT on Real Property | 3 | 3 | 5 | **11** | HIGH |
| 5 | CGT Computation | 3 | 3 | 4 | **10** | HIGH |
| 5 | Form 2307 Issuance | 3 | 3 | 4 | **10** | HIGH |
| 7 | CWT Rate and Timing | 3 | 2 | 4 | **9** | HIGH |
| 7 | Transfer Tax | 3 | 3 | 3 | **9** | HIGH |
| 9 | Installment VAT Schedule | 2 | 1 | 4 | **7** | MEDIUM |
| 9 | DST on Mortgage | 2 | 2 | 3 | **7** | MEDIUM |
| 11 | DST on Conveyance | 2 | 1 | 3 | **6** | MEDIUM |
| 12 | Highest-of-Three Base | 1 | 1 | 3 | **5** | LOW |

## Key Observations

### 1. Structural vs. Operational Complexity Divergence
Three computations have **operational complexity that significantly exceeds structural complexity**:
- **Installment VAT Schedule** (structural: 7/MEDIUM) — multi-period tracking over 2–30 years, dual formula paths, cancellation reversal, constructive receipt rules make this operationally HIGH despite few branching rules
- **Form 2307 Issuance** (structural: 10/HIGH) — the filing chain (monthly → quarterly → annual) and bilateral reconciliation (payor QAP vs. payee SAWT) create workflow complexity beyond the formula
- **Zonal Value Lookup** (structural: 12/VERY HIGH) — the challenge isn't algorithmic complexity but data pipeline engineering (124 heterogeneous workbooks, address normalization, OCR)

### 2. Shared Infrastructure Amplification
Two infrastructure components unlock multiple computations:
- **Zonal Value Engine** → enables CGT, DST on Sale, CWT, VAT on Real Property, Transfer Tax (5 computations)
- **LGU Rate Database** → enables RPT + Transfer Tax (2 computations, but affects all 1,700+ LGUs)

Marginal complexity of downstream computations drops dramatically once shared infrastructure exists:
- Transfer Tax drops from HIGH (9) to effectively LOW (~4) once LGU database + zonal value engine exist
- DST on Conveyance drops from MEDIUM (6) to effectively LOW (~3) once highest-of-three base engine exists

### 3. Non-Deterministic Gates
Four computations have non-deterministic prerequisites that must be resolved before the deterministic computation can execute:
- **CGT / CWT / VAT**: Capital vs. ordinary asset classification (RR 7-2003 — requires judgment)
- **EWT**: Employment vs. independent contractor classification (economic reality test)
- **VAT**: Socialized housing qualification
- **CWT**: Habitually-engaged seller determination (partially deterministic — HLURB registration is conclusive; 6-transaction test is countable)

These gates are **out of scope** for automation engines (per PROMPT.md) but must be handled as user inputs with clear branching.

### 4. RPVARA Transition Impact
RA 12001 (June 2024) will affect complexity scores post-implementation (~mid-2026):
- Highest-of-Three Base: 3-way max → 2-way max (simpler)
- Zonal Value Lookup: dual-source handling during transition (temporarily more complex)
- RPT: standardized SMV + 6% first-year cap (new branch, but long-term simplification)
