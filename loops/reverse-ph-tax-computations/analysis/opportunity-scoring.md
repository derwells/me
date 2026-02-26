# Opportunity Scoring — PH Tax Computation Automation Catalog

**Wave:** 4 (Scoring & Synthesis)
**Date:** 2026-02-26
**Depends on:** All Wave 2 computation extractions + Wave 3 gap analysis (existing-tools-survey, practitioner-workflow, complexity-scoring)

---

## Methodology

Each of the 12 surveyed computations is scored on three dimensions (1–5 each):

| Dimension | What It Measures | Scale |
|---|---|---|
| **Automation Gap (AG)** | How poorly existing tools cover this computation | 1 = fully covered by existing tools → 5 = fully manual, zero tool coverage |
| **Market Frequency (MF)** | How often this computation is needed | 1 = rare transaction type → 5 = every real estate deal or annual obligation |
| **Moat Defensibility (MD)** | How hard for a competitor to replicate once built | 1 = trivial formula, no data advantage → 5 = massive data/knowledge barrier |

**Composite Score** = AG × MF × MD (range: 1–125)

Classification:
- **80–125:** TIER 1 — Highest opportunity (wide gap, high frequency, strong moat)
- **50–79:** TIER 2 — Strong opportunity (meaningful gap with frequency or moat advantage)
- **25–49:** TIER 3 — Moderate opportunity (gap exists but limited moat or frequency)
- **1–24:** TIER 4 — Low priority (covered by existing tools or low defensibility)

---

## Per-Computation Scoring

### 1. Zonal Value Lookup

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **5** | ABSOLUTE GAP. No tool provides API-accessible zonal value lookup integrated into tax computation. Data exists fragmented: RealValueMaps (2.7M records), Housal (1.96M), REN.PH (233K) — but all are web-only, no API. BIR publishes 124 heterogeneous Excel/PDF workbooks with no standard format. |
| **Market Frequency** | **5** | Prerequisite for 5 other computations (CGT, DST on sale, CWT, VAT, transfer tax). Every single real estate transaction requires zonal value resolution. Infrastructure component, not standalone. |
| **Moat Defensibility** | **5** | Massive data engineering moat: 124 heterogeneous workbooks requiring format normalization, address parsing/geocoding, OCR for image-based PDFs, and ongoing update monitoring (BIR revises schedules on 3–5 year cycles; 38% outdated per DOF 2024). 6-level fallback hierarchy (RAMO 2-91). RPVARA transition (BIR ZV → BLGF SMV by mid-2026) adds dual-source handling. First-mover data advantage compounds over time. |

**Composite: 125 (TIER 1)**
Highest possible score. Single highest-leverage component in the entire catalog — resolving this bottleneck unlocks automation for 5 downstream tax computations. The data moat is durable and grows with coverage.

---

### 2. RPT Computation (Real Property Tax)

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **5** | ABSOLUTE GAP for full-LGU coverage. Online RPT payment portals exist in ~10 cities (Manila, Makati, QC) but are payment-only, not computation engines. No tool covers all 1,700+ LGUs with correct assessment levels and locally-enacted rates. |
| **Market Frequency** | **5** | Annual obligation for every real property owner in the Philippines. Most frequent computation in the catalog — recurring, not transaction-triggered. Multi-property owners (developers, REITs, HNWIs) compute this hundreds of times per year. |
| **Moat Defensibility** | **5** | 1,700-LGU rate database is the dominant moat: each LGU enacts its own tax rate (up to statutory caps), assessment levels follow 6 property classifications with multi-tier bracket tables (9-tier residential building, 8-tier commercial/industrial, etc.), and 7 distinct lookup tables are needed. Database requires ongoing maintenance as LGUs amend ordinances. RPVARA (RA 12001) introduces standardized SMV + 6% first-year RPT cap, adding a transition-period branch. |

**Composite: 125 (TIER 1)**
Tied with zonal value for highest score. The annual recurrence drives massive aggregate demand. The LGU rate database is the hardest dataset to compile and maintain — no single source exists. Fully deterministic once inputs resolved.

---

### 3. Installment VAT Schedule

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **5** | ABSOLUTE GAP. Zero tools handle multi-period output VAT recognition with dual formula paths (simple collection-based vs. FMV-ratio). QNE/JuanTax/Taxumo handle quarterly VAT filing but not the per-project, per-unit installment schedule that real estate developers need. |
| **Market Frequency** | **3** | Applies to developer installment sales only — a significant but specialized subset. A 500-unit project generates 500 individual VAT schedules spanning 5–30 years. High volume per developer but limited number of developers vs. total RE transactions. |
| **Moat Defensibility** | **5** | Deepest operational complexity in the catalog: multi-period tracking (2–30 years per contract), dual formula paths (collection × 12% vs. (collection/contract_price) × FMV × 12%), constructive receipt rules, cancellation/default reversal, mortgage excess-over-basis exception, EOPT invoicing transition. 9 complexity drivers documented. Requires zonal value snapshot at sale date (not current value). Getting all edge cases correct requires deep regulatory expertise. |

**Composite: 75 (TIER 2)**
Highest moat of any individual computation. Frequency is the limiting factor — but each developer client generates massive per-unit volume. Natural fit for a dedicated deep-dive loop (comparable to the inheritance engine).

---

### 4. VAT on Real Property

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **4** | JuanTax/Taxumo handle quarterly VAT filing (Form 2550Q) for regular business operations, and eONETT assesses VAT on property sales. But no tool handles the full RE-specific 4-gate decision tree: (1) capital vs. ordinary gate, (2) VAT registration check, (3) residential threshold (₱3.6M, CPI-adjusted), (4) socialized housing exemption, plus installment 25% recognition test. |
| **Market Frequency** | **4** | Every ordinary asset sale — developers, habitually-engaged sellers, banks disposing foreclosed properties. Excludes most individual sales (capital assets → CGT path instead). Still very high volume. |
| **Moat Defensibility** | **4** | 4-gate decision tree with CPI-adjusted threshold tracking (₱3.6M as of Jan 2024, updated periodically), installment recognition bifurcation (≤25% initial → per-collection; >25% → full at sale), EOPT invoicing changes, bare lot exemption elimination history. Multiple non-deterministic gates (asset classification, socialized housing) require careful user-input handling. |

**Composite: 64 (TIER 2)**
Strong opportunity driven by high complexity and meaningful automation gap. The 4-gate decision tree is the most intricate classification logic of any single tax computation.

---

### 5. CWT Rate and Timing

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **5** | ABSOLUTE GAP. No tool handles the tiered CWT rates (1.5%/3%/5% for habitually engaged sellers at ₱500K/₱2M thresholds; 6% flat for non-habitually-engaged and banks) with installment timing bifurcation (>25% initial → full CWT on first installment; ≤25% → per-installment or at-last-installment depending on buyer type). eONETT computes CWT but is officer-mediated (2–8 week turnaround). |
| **Market Frequency** | **4** | Every ordinary asset sale. Buyer is the withholding agent — mandatory filing on Form 1606. Per RMC 31-2025, Form 1606 paid copy is seller's sole CWT credit document (Form 2307 no longer accepted). |
| **Moat Defensibility** | **3** | Rate table is compact (4 rates, 2 thresholds) but the habitually-engaged determination (6-transaction test, HLURB registration), installment timing bifurcation (3 branches by buyer type), and Form 1606 filing mechanics add meaningful depth. Zonal value dependency adds data moat (shared with CGT/DST). |

**Composite: 60 (TIER 2)**
Strong automation gap driven by the complete absence of CWT computation tools. The tiered rate selection + installment timing create enough complexity to prevent trivial replication. Shares zonal value infrastructure with CGT and DST.

---

### 6. Transfer Tax

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **4** | No tool computes transfer tax with correct per-LGU rates. Web calculators use generic 0.5–0.75% estimates. The correct rate depends on LGU type (province, city, municipality) and locally-enacted ordinances (some LGUs are below cap). Currently requires in-person LGU visit. |
| **Market Frequency** | **5** | Every real property sale. Sequential bottleneck in the ONETT pipeline — requires eCAR first, then transfer tax payment, then title transfer at Registry of Deeds. |
| **Moat Defensibility** | **3** | Formula is simple (base × rate), but the LGU rate database is the moat — same database needed for RPT. Shares LGU infrastructure with RPT (marginal build cost near zero once RPT engine exists). CARP exemption and LGU-specific exemptions add modest branching. |

**Composite: 60 (TIER 2)**
Score driven by frequency and automation gap. Critical note: marginal moat drops to ~1 once RPT engine (with its LGU database) is built. Best viewed as a free add-on to the RPT engine rather than a standalone opportunity.

---

### 7. CGT Computation (Capital Gains Tax)

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **3** | Partially covered: JuanTax supports Form 1706 filing; eONETT computes CGT (officer-mediated); web calculators (Housal, ForeclosurePhilippines) compute basic 6% × max(SP,ZV,AFMV). GAPS: installment CGT (2-option regime), principal residence exemption (partial computation with escrow), EOPT tiered penalties, surcharge/interest calculation. |
| **Market Frequency** | **5** | Every capital asset sale — the majority of individual property sales in the Philippines. Highest-volume individual transaction tax. |
| **Moat Defensibility** | **3** | 11 material decision branches including installment (2 options), principal residence exemption (5 binary conditions + escrow for GSP > ₱5M), EOPT penalty tiers (4 taxpayer size categories). Not trivial to get all edge cases right, but the law is public and the formula is well-documented. |

**Composite: 45 (TIER 3)**
Large market but moderate gap (basic computation already exists in multiple tools). The opportunity is in the advanced features — installment handling, exemptions, and penalty computation — which existing tools omit. Natural extension once highest-of-three base engine exists.

---

### 8. Highest-of-Three Tax Base Resolution

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **4** | No tool automates the full three-value comparison with live zonal value lookup. Web calculators require manual input of all three values. eONETT resolves it but is officer-mediated. The gap is specifically in automated zonal value integration. |
| **Market Frequency** | **5** | Prerequisite for every transaction tax (CGT, DST, CWT, VAT, transfer tax). Functionally part of the zonal value lookup pipeline. |
| **Moat Defensibility** | **2** | Formula is `max(a, b, c)`. Trivial once inputs are available. Zero algorithmic moat — all moat resides in the zonal value data pipeline (scored separately under Zonal Value Lookup). |

**Composite: 40 (TIER 3)**
High frequency and meaningful gap, but near-zero standalone moat. Best understood as the integration layer between zonal value lookup and downstream tax computations — valuable as architecture but not as a defensible product.

---

### 9. DST on Mortgage

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **5** | ABSOLUTE GAP. Zero tools compute the Section 195 stepped schedule (₱40 base + ₱20 per ₱5,000 band). No web calculator, no BIR tool, no accounting software. Even practitioner guides frequently get the rate wrong (Wave 2 found source conflict between ₱20 and ₱40 incremental). |
| **Market Frequency** | **4** | Every mortgage, deed of trust, or loan secured by real property. Most financed RE purchases (majority of market). Also applies to refinancing, restructuring, and supplemental mortgages. |
| **Moat Defensibility** | **2** | Stepped arithmetic is unique among PH taxes (not a flat rate) but straightforward once Section 195 is correctly read. Pre-TRAIN/post-TRAIN date gate adds one branch. No external data dependencies (amount from loan document, date from instrument). Low knowledge barrier for a competent developer. |

**Composite: 40 (TIER 3)**
Maximum automation gap (literally zero coverage) but low moat — anyone reading Section 195 can replicate. Value is in being the first to offer it at all. Quick win for a tax engine: implementable in hours, immediately differentiated from all existing tools.

---

### 10. EWT Rate Classification

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **2** | Best-covered computation in the catalog. QNE Cloud has predefined ATC codes with auto-compute. JuanTax and Taxumo both handle Form 1601-EQ with rate selection. Form 2307 generation integrated. The decision tree is already encoded in commercial software. |
| **Market Frequency** | **5** | Every business making professional fees, rental, commission, or contractor payments. 13 filing obligations per year (monthly 0619-E + quarterly 1601-EQ). Extremely frequent. |
| **Moat Defensibility** | **2** | Deepest decision tree (15+ branches across 4 categories) but already implemented by multiple competitors. No unique data advantage — all rates are from publicly available RR 2-98 and amendments. |

**Composite: 20 (TIER 4)**
High frequency but low opportunity — existing tools already do this well. Building this adds table-stakes capability but no differentiation. Include in a comprehensive engine but don't lead with it.

---

### 11. Form 2307 Issuance Logic

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **2** | JuanTax, QNE, and Taxumo all generate Form 2307. BIR Online Tools and BIR Excel Uploader provide free alternatives. The computation (gross_payment × ATC_rate) is trivial. Gaps exist in: bilateral reconciliation (payor QAP vs. payee SAWT), DAT file generation for alphalist, and multi-period credit tracking. |
| **Market Frequency** | **5** | Every withholding transaction. Quarterly certificate issuance + annual alphalist. "Most frustrating part of PH tax compliance" per practitioner interviews (reconciliation, not computation). |
| **Moat Defensibility** | **2** | Formula is trivial. Filing chain (0619-E → 1601-EQ → 1604-E) is well-documented. DAT file format is BIR-specified. Reconciliation automation is a workflow differentiator but not a defensible moat. |

**Composite: 20 (TIER 4)**
Same as EWT — high frequency, low gap. The opportunity is not in the computation but in the reconciliation workflow (payor-payee matching, SAWT automation). Workflow automation ≠ computation engine.

---

### 12. DST on Conveyance (Sale)

| Dimension | Score | Justification |
|---|---|---|
| **Automation Gap** | **2** | Multiple tools cover this: JuanTax supports Form 2000-OT; web calculators compute 1.5% readily; eONETT includes DST in its assessment. The formula is `base × 1.5%` with a ceiling-to-nearest-₱15 rule. |
| **Market Frequency** | **5** | Every real property conveyance (sale, donation, exchange). Applies to both capital and ordinary assets — broadest applicability of any transaction tax. |
| **Moat Defensibility** | **1** | `base × 0.015` with a ceiling function. Trivially replicable by any developer in minutes. Zero knowledge barrier, zero data requirement beyond the shared highest-of-three base. |

**Composite: 10 (TIER 4)**
Lowest-opportunity computation. Fully covered by existing tools, zero moat. Include in any comprehensive engine (marginal build cost is near zero once highest-of-three base exists) but never lead with it.

---

## Composite Score Rankings

| Rank | Computation | AG | MF | MD | Composite | Tier | Strategic Role |
|---:|---|:---:|:---:|:---:|---:|---|---|
| 1 | **Zonal Value Lookup** | 5 | 5 | 5 | **125** | TIER 1 | Infrastructure foundation — unlocks 5 downstream computations |
| 1 | **RPT Computation** | 5 | 5 | 5 | **125** | TIER 1 | Highest standalone demand — annual, recurring, all property owners |
| 3 | **Installment VAT Schedule** | 5 | 3 | 5 | **75** | TIER 2 | Deepest complexity — developer-focused, high per-client volume |
| 4 | **VAT on Real Property** | 4 | 4 | 4 | **64** | TIER 2 | Most intricate decision tree — 4-gate classification |
| 5 | **CWT Rate and Timing** | 5 | 4 | 3 | **60** | TIER 2 | Complete gap — no tools, moderate complexity |
| 5 | **Transfer Tax** | 4 | 5 | 3 | **60** | TIER 2 | Free add-on to RPT engine (shared LGU database) |
| 7 | **CGT Computation** | 3 | 5 | 3 | **45** | TIER 3 | Largest market — advanced features are the gap |
| 8 | **Highest-of-Three Base** | 4 | 5 | 2 | **40** | TIER 3 | Integration layer — connects zonal lookup to all taxes |
| 8 | **DST on Mortgage** | 5 | 4 | 2 | **40** | TIER 3 | Quick win — zero coverage, low build cost |
| 10 | **EWT Rate Classification** | 2 | 5 | 2 | **20** | TIER 4 | Table stakes — already covered by competitors |
| 10 | **Form 2307 Issuance** | 2 | 5 | 2 | **20** | TIER 4 | Workflow opportunity — computation is trivial |
| 12 | **DST on Conveyance** | 2 | 5 | 1 | **10** | TIER 4 | Zero moat — include but never lead with |

---

## Strategic Clusters

The 12 computations naturally cluster into four build strategies:

### Cluster A: Data Infrastructure (Build First)
**Components:** Zonal Value Lookup + Highest-of-Three Base
**Composite:** 125 + 40 = 165
**Rationale:** Zonal value is the bottleneck for 5 downstream computations. Building the data pipeline first creates maximum leverage and a durable data moat. The highest-of-three base is the trivial integration layer that connects zonal data to every tax formula.
**Deep-dive loop candidate:** YES — comparable to inheritance engine in scope (data normalization across 124 RDOs, address parsing, OCR, fallback logic, RPVARA dual-source handling).

### Cluster B: Transaction Tax Engine (Build Second)
**Components:** CGT + DST on Sale + CWT + VAT on Real Property + Transfer Tax + DST on Mortgage
**Composite:** 45 + 10 + 60 + 64 + 60 + 40 = 279 (aggregate)
**Rationale:** Once Cluster A provides the zonal value engine, all transaction taxes share the same tax base. Build as a unified ONETT computation engine: input a transaction → output all applicable taxes (CGT or CWT+VAT depending on asset type, plus DST on sale, transfer tax). DST on mortgage is a standalone add-on (no zonal value dependency).
**Deep-dive loop candidate:** YES — the unified engine is the core product. 6 computations, ~50 material decision branches total, shared infrastructure amortization.

### Cluster C: Developer Tools (Build Third)
**Components:** Installment VAT Schedule + Installment CGT (already in CGT)
**Composite:** 75 (installment VAT alone)
**Rationale:** Highest moat computation in the catalog. Multi-period tracking (2–30 years) with dual formula paths is operationally complex and poorly served. But narrow market (developers only). Best positioned as premium tier of the transaction tax engine.
**Deep-dive loop candidate:** YES — 9 complexity drivers, multi-period state management, EOPT transition. Comparable to inheritance engine in regulatory depth.

### Cluster D: Recurring Compliance (Parallel Track)
**Components:** RPT Computation + Transfer Tax (LGU database) + EWT + Form 2307
**Composite:** 125 + 60 + 20 + 20 = 225 (aggregate)
**Rationale:** RPT is a standalone opportunity (annual, recurring, no dependency on zonal value engine since it uses assessor FMV not BIR zonal value). The LGU rate database required for RPT also serves transfer tax. EWT and Form 2307 are table-stakes features already covered by competitors — include for completeness but not for differentiation.
**Deep-dive loop candidate:** RPT YES (1,700-LGU database, 7 lookup tables, RPVARA transition). EWT/Form 2307 NO (already well-served).

---

## Recommended Deep-Dive Loop Priority

Based on composite scores, strategic clustering, and infrastructure dependencies:

| Priority | Target | Why | Estimated Scope |
|---|---|---|---|
| **P0** | Zonal Value Lookup Engine | Highest leverage — unlocks 5 computations; durable data moat; RPVARA transition creates first-mover window | Data pipeline: 124 RDO workbooks, address normalization, classification codes, fallback logic, RPVARA dual-source |
| **P1** | RPT Computation Engine | Highest standalone demand; independent of zonal value (uses assessor FMV); 1,700-LGU database is massive moat | LGU rate database compilation, 7 lookup tables, assessment level encoding, RPVARA transition handling |
| **P2** | ONETT Transaction Tax Engine | Largest market; depends on P0 (zonal value); unified CGT/CWT/VAT/DST computation | ~50 decision branches, 6 tax types, installment handling, penalty tiers, Form 1706/1606/2000-OT output |
| **P3** | Installment VAT Schedule Engine | Highest moat; depends on P0 + P2; developer-focused premium feature | Multi-period (2–30yr) tracking, dual formula paths, constructive receipt, cancellation reversal |

---

## Key Findings

1. **Two infrastructure components dominate the catalog:** Zonal Value Lookup and RPT Computation both score 125/125 — maximum possible. They represent different types of moats (data pipeline vs. LGU rate database) and serve different markets (transaction vs. recurring).

2. **The automation gap is binary, not gradual:** Computations are either well-covered (EWT, Form 2307, DST on sale — score 2/5) or completely uncovered (CWT, installment VAT, RPT — score 5/5). There is no middle ground. This suggests a "greenfield vs. competitive" dichotomy rather than incremental improvement.

3. **Shared infrastructure amplifies downstream value:** Building the zonal value engine makes 5 downstream computations immediately feasible. Building the LGU rate database makes both RPT and transfer tax available. The total catalog value far exceeds the sum of individual computations.

4. **Frequency is uniformly high — moat is the differentiator:** 9 of 12 computations score 4–5 on market frequency. The ranking is ultimately determined by automation gap × moat. This confirms that data-intensive, regulation-deep computations (zonal value, RPT, installment VAT) are the highest-value targets.

5. **RPVARA transition creates a time-limited first-mover window:** RA 12001 (June 2024, effective ~mid-2026) transfers zonal value authority from BIR to BLGF and introduces standardized SMV. Builders who establish data pipelines before the transition can capture the dual-source period and lock in coverage as the new system stabilizes.
