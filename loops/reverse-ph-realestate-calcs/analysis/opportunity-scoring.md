# Opportunity Scoring — All 16 Computations

**Wave:** 4 (Scoring & Synthesis)
**Date:** 2026-02-27
**Method:** Three-dimensional scoring (automation_gap × market_frequency × moat_defensibility), each 1–5, multiplicative composite (max 125). Informed by Wave 3 analyses: existing-tools-survey, practitioner-workflow (expanded), complexity-scoring.

---

## Scoring Rubric

### Automation Gap (A) — How poorly served by existing tools?
| Score | Definition |
|-------|-----------|
| 1 | Well-served — authoritative tool exists with full coverage |
| 2 | Good coverage — adequate tools exist, minor gaps in edge cases |
| 3 | Partial coverage — tools exist but miss significant PH-specific logic or are SaaS-locked |
| 4 | Poor coverage — generic tools exist but no PH regulatory logic encoded; practitioners use manual/Excel |
| 5 | Zero coverage — no tool of any kind; entirely manual or spreadsheet-based |

### Market Frequency (F) — How often is this computation needed?
| Score | Definition |
|-------|-----------|
| 1 | Rare — niche transaction type, hundreds per year nationally |
| 2 | Infrequent — per-project or one-time setup, low thousands per year |
| 3 | Moderate — common in a major subsegment (e.g., socialized housing defaults, developer project filings) |
| 4 | High — recurring for a large market segment (e.g., all rentals annually, all condo units monthly) |
| 5 | Every transaction — needed for virtually every real estate sale/purchase/loan in the PH |

### Moat Defensibility (M) — How hard to replicate once built?
| Score | Definition |
|-------|-----------|
| 1 | Trivial — single formula, publicly documented, anyone can build in a day |
| 2 | Low — well-documented formulas/tables, moderate effort to compile but no data barriers |
| 3 | Moderate — requires compiling regulatory history, multi-source data, or cross-referencing SC rulings |
| 4 | High — requires proprietary data acquisition (per-developer, per-condo-corp), deep regulatory expertise, or multi-regulation interaction |
| 5 | Very high — requires LGU-level database construction, ongoing maintenance infrastructure, or deep multi-dimensional table systems that create compounding data advantage |

### Composite Formula
`Composite = A × F × M` (range 1–125)

---

## Individual Scoring

### 1. pagibig-loan-eligibility
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 2 | Official Pag-IBIG Affordability Calculator covers core eligibility modes. OmniCalculator, PagibigCalculator.com provide alternatives. Edge cases (loan-on-top-of-loan, co-borrower rules per Circular 396) not exposed in any tool. |
| Market Frequency | 5 | Pag-IBIG is the dominant housing loan provider — ~100K+ housing loans released per year. Every affordable housing buyer checks eligibility. |
| Moat Defensibility | 2 | 7-step decision tree is well-documented in circulars. Contribution-to-loan table for ₱3M–₱6M is the only data gap. Official tool already exists. |
| **Composite** | **20** | |

### 2. pagibig-amortization
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 3 | Basic amortization formula well-covered (5+ tools). However, NO tool computes MRI/FGI premium breakdown separately — practitioners can't see insurance cost impact. MRI age-bracket table has conflicting sources (Circular 428 mismatch). FGI rate last verified at 0.1686% (2018). |
| Market Frequency | 5 | Every Pag-IBIG housing loan needs an amortization schedule. Borrowers, brokers, and loan officers all compute this. |
| Moat Defensibility | 3 | MRI/FGI premium rates not publicly documented since 2014–2018 — whoever obtains current rates has data advantage. Insurance computation adds non-trivial complexity beyond standard amortization. Repricing mechanics (borrower chooses new period) require modeling. |
| **Composite** | **45** | |

### 3. bank-mortgage-amortization
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 2 | Best-covered computation — 11+ tools compute basic amortization. BSP Calculator offers 5 amortization modes. However, every bank calculator is siloed to its own rates. No tool handles: variable rate repricing scenario modeling, early termination penalty formulas, multi-bank comparison in one interface. |
| Market Frequency | 5 | Every bank-financed purchase. Indicative computation at Stage 1 (pre-sale), actual at Stage 4 (loan processing), ongoing at Stage 6 (repricing). |
| Moat Defensibility | 3 | Multi-bank rate database (8+ banks with current rates, promo periods, repricing benchmarks) creates moderate data moat. Daily benchmark feeds (BVAL, T-bill, PHIREF) needed for repricing modeling. Per-bank early termination policies are non-public. |
| **Composite** | **30** | |

### 4. developer-equity-schedule
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 4 | POOR coverage. No tool handles full developer equity computation: TCP composition, reservation fee deduction, spot cash discount tiers, installment penalty/surcharge, turnover balance. Practitioners use developer-provided sample computation sheets or custom Excel. Practitioner-workflow: 5–30 min/instance with high error rate. Breighton Land case: 49 compensation plan variations. |
| Market Frequency | 5 | Sample computation generated for EVERY buyer interaction at pre-selling stage. Largest volume computation in real estate sales. Developer back-office creates initial (7-15 days), restructured (10 days at DMCI). |
| Moat Defensibility | 3 | Requires per-developer/per-project data (discount tables, penalty models, charge percentages). Data is accessible from published terms but fragmented across 4+ major developers × multiple projects. VAT integration (₱3.6M threshold per RR 1-2024), PD 957 constraints, and Maceda qualification add regulatory depth. |
| **Composite** | **60** | |

### 5. ltv-ratio
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 4 | Generic LTV calculators exist (Bankrate) but none encode BSP Circular 1087/855 LTV caps by property type, Pag-IBIG LTV tiers (retail vs buyback, by loan range), appraisal-basis rules, or additional collateral requirements. Banks compute internally; practitioners can't model independently. |
| Market Frequency | 4 | Every bank/Pag-IBIG loan involves LTV determination. Sub-computation within eligibility — not typically computed standalone but essential to loan amount determination. |
| Moat Defensibility | 2 | LTV tables well-documented in BSP/Pag-IBIG circulars. Straightforward min-function logic. 5 lookup tables but stable policies (Pag-IBIG tiers unchanged since 2014). Low data acquisition barrier. |
| **Composite** | **32** | |

### 6. maceda-refund
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 5 | ZERO tools. Despite RA 6552 being >50 years old, no calculator computes cash surrender value (50% + 5%/yr) or grace period (1 month/year). Practitioners compute manually from payment records. Error rate "very high" per workflow analysis — disputes on "total payments" definition, years counting (per Orbe v. Filinvest), and Section 4 notarization requirements. |
| Market Frequency | 3 | Occurs only when installment buyers default. Common in socialized housing (estimated 15–30% default rates) but not every transaction. Lifecycle Stage 3 (equity period defaults). Volume: tens of thousands of cases annually across all developers. |
| Moat Defensibility | 2 | Core formula is simple (statutory since 1972, one lookup table). However, SC rulings add edge case depth: Orbe v. Filinvest (years as divisor), Active Realty v. Daroya (dual cancellation conditions), partial-year pro-rata, RF treatment. 5 unresolved ambiguities documented. Still relatively easy to replicate — the formula is the moat floor. |
| **Composite** | **30** | |

### 7. rent-increase-computation
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 5 | ZERO tools. No rent increase calculator for RA 9653 / NHSB Resolution annual caps. Practitioners manually apply the announced percentage. No tool checks coverage eligibility (rent bracket test, same-tenant rule, HUC determination). Historical rate table (2010–2026, 10 resolution periods) not compiled in any tool. |
| Market Frequency | 4 | Every rental property, annually. Metro Manila alone has millions of rental units. Landlords and tenants both need this computation. But applies to rental market only, not sale transactions. |
| Moat Defensibility | 3 | Requires compiling NHSB resolution history (2010–2026, with the 2018–2020 three-tier correction), coverage determination logic (7-step decision tree), HUC classification list, vacancy reset + 12-month freeze interaction rules. Respicio claims about threshold increases must be verified/rejected. Not trivial to get right despite simple formula. |
| **Composite** | **60** | |

### 8. condo-common-area-pct
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 5 | ZERO tools. No tool computes undivided interest per RA 4726. Formula (unit sqm / total sellable sqm) is straightforward but no tool implements it with master deed parameters, parking CCT denominator correction, or par value method alternative. |
| Market Frequency | 2 | Computed once per condo project at master deed creation. Buyers may verify but it's not per-transaction. Hundreds of new condo projects per year, not millions of computations. |
| Moat Defensibility | 2 | Core formula is straightforward. Method depends on what master deed specifies — project-specific input, not regulatory complexity. RA 7899 voting scope correction and parking slot treatment add some depth but overall low barrier. |
| **Composite** | **20** | |

### 9. socialized-housing-compliance
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 5 | ZERO tools. No compliance checker for DHSUD socialized/economic housing price ceilings. No tool validates per-unit and per-sqm limits by housing type, zonal value add-ons for NCR/HUC condos, lot-only sub-rule (40% of house-and-lot ceiling), or balanced housing requirement (6 compliance modes). Developers and DHSUD staff cross-reference JMC tables manually. |
| Market Frequency | 4 | Every socialized/economic housing project requires compliance (mandatory). Socialized housing is the largest market segment by volume. Also relevant for PhilGuarantee government guarantee eligibility (₱4.9M low-cost, ₱6.6M medium). BOI and DHSUD permitting depend on it. |
| Moat Defensibility | 4 | Requires: JMC ceiling database (JMC 2025-001 with 6 base ceilings by building type/height/floor area), zonal value add-on table integration, 6-tier housing category classification, 6 balanced housing compliance modes (per RA 10884), PhilGuarantee ceiling tracking. JMCs update every 2–3 years. Cross-references BIR zonal values and DHSUD issuances. PIC/IC compliance modes lack clear statutory basis per CREBA — deep regulatory knowledge required. |
| **Composite** | **80** | |

### 10. bp220-lot-compliance
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 5 | ZERO tools. BP 220 compliance is entirely manual — architects cross-reference IRR tables against CAD plans, DHSUD examiners do manual document review. Practitioner-workflow: 30–60 min per compliance check, medium error rate. No automated compliance-check tool exists anywhere. |
| Market Frequency | 3 | Every socialized/economic housing project development (mandatory for DHSUD permit). Volume: hundreds to low thousands of projects filed annually. Per-project, not per-unit — but each project may require multiple compliance iterations during design. |
| Moat Defensibility | 5 | Deepest branching of all 16 computations (15 decision points). 6 lookup tables. 12+ compliance checks verified. JMC floor area layering (18→32→28→24 sqm) across different issuances. Multi-regulation interaction (BP 220 IRR + JMC 2025-001 + NBC for >12 storeys). 10 additional deterministic checks identified. Requires deep knowledge of 2008 IRR tables, pre-2008 vs post-2008 value distinctions, recent DO 2024-020 TWG review status. Very hard to replicate correctly. |
| **Composite** | **75** | |

### 11. assessment-level-lookup
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 4 | POOR coverage. Simplified RPT tools exist (TaxCalcPH, OwnPropertyAbroad) but apply Metro Manila 2% / provincial 1% flat rates without full LGC Section 218 assessment level implementation. No tool has all 34 bracket values across 4 building sub-tables, machinery rates, special class rates, or LGU-specific variations. LGU assessor systems (RPTAS/eFAAS) exist internally but are not public. |
| Market Frequency | 5 | Assessment level determines the tax base for ALL properties. Every property owner in the Philippines is affected (RPT is annual). Also feeds into property transaction pricing — buyers evaluate RPT burden. RA 12001 (RPVARA) implementation will drive reassessments nationwide. |
| Moat Defensibility | 5 | 15 lookup tables, 6 external dependencies, 1,488+ LGU jurisdictions. LGU-specific SMV/BUCC databases are the dominant data barrier. RA 12001 adds 6% transition cap tracking (per-LGU effectivity dates). Building FMV pipeline (BUCC × floor area − depreciation) requires BUCC schedules per LGU. Whoever builds the LGU data layer has a compounding advantage — each additional LGU increases the dataset's value for all users. |
| **Composite** | **100** | |

### 12. improvement-depreciation
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 5 | ZERO tools. No PH-specific tool for building improvement depreciation. Generic depreciation calculators exist but none with PH assessor parameters (construction type classification, BUCC rates, economic life by type, LGU-specific depreciation tables). Practitioner-workflow: part of assessor's internal process, not exposed to property owners. |
| Market Frequency | 3 | Feeds into RPT assessment pipeline for every property with improvements (buildings). But computed by LGU assessors as part of their workflow, not directly by buyers/sellers/brokers. Property owners occasionally need it when disputing assessments or evaluating acquisition costs. |
| Moat Defensibility | 5 | Per-LGU BUCC rates, per-LGU depreciation tables (age × construction type × maintenance level), dual classification systems, machinery residual value floors. RA 12001 mandates 3-year SMV/BUCC revision cycle. DPWH construction cost data integration. Same LGU database moat as assessment-level-lookup — shares data infrastructure. |
| **Composite** | **75** | |

### 13. rod-registration-fees
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 2 | GOOD coverage. Official LRA ERCF tool is authoritative. ForeclosurePH has a registration fee calculator. However, neither computes: annotation fees (separate mortgage/lien schedules), total title transfer cost pipeline, or the 25% late filing surcharge. The effective rate analysis (showing "0.25%" approximation understates actual 0.46–0.51%) is not in any tool. |
| Market Frequency | 5 | Every property transfer requires registration at the Registry of Deeds. Universal computation. |
| Moat Defensibility | 2 | National fee table, well-documented (LRA Circular 13-2016). Two-tier formula is straightforward. Annotation fee schedules add moderate complexity. Last comprehensive revision was 2002; updates are rare. Low data acquisition barrier. |
| **Composite** | **20** | |

### 14. notarial-fees
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 5 | ZERO tools. However, this score requires context: 2 of 5 sub-computations are fully deterministic (OCA per-page ceiling ₱200/₱50, foreclosure fee 5%/2.5% + ₱100K cap), 1 is conditional (IBP-based, deterministic given chapter table), and 2 are non-deterministic (market heuristic 1–2%, professional fee). The zero-tool gap is real but the automatable portion is limited. |
| Market Frequency | 5 | Every real estate transaction requires notarization. However, practitioners rarely "compute" notarial fees — they receive a quote from the notary. The computation is most valuable for: foreclosure proceedings (fee is formula-based), fee verification (is the quoted fee within statutory bounds), and closing cost estimation. |
| Moat Defensibility | 2 | Deterministic portions are trivial (OCA ceiling is 2 numbers; foreclosure fee is a simple formula). IBP chapter variation adds locality-specific data but the tables are accessible. Non-deterministic portions inherently can't create moat. Low barrier overall. |
| **Composite** | **50** | |

### 15. broker-commission
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 3 | PARTIAL coverage. iRealtee (Jan 2026) has multi-tier split + EWT deduction — best coverage found. But it's embedded in a full SaaS platform (not standalone). Clevrr and Housal compute flat commission only. Gaps: MLS co-broke splits, lease commission, rent-to-own conversion commission, EWT rates may not match RR 11-2018 (iRealtee shows 10%/15% at ₱3M, our verified rates are 5%/10%), 8% flat tax option for sub-₱3M brokers. |
| Market Frequency | 5 | Every brokered transaction. Lifecycle Stage 1 (pre-sale). Breighton Land case: 49 compensation plan variations across one brokerage. High volume. |
| Moat Defensibility | 3 | Multi-tier split engine, EWT/VAT computation with annual sworn declaration tracking, MLS co-broke rules (CEREBMLS), finder's fee vs. commission legal distinction. Requires maintaining: contractual rate benchmarks by property type, multi-tier distribution models (iRealtee 20%/60/15/10), and BIR compliance form integration (8 forms documented). Moderate data maintenance but accessible. |
| **Composite** | **45** | |

### 16. condo-association-dues
| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| Automation Gap | 5 | ZERO tools. No tool computes monthly dues via ECR 001-17 formula (gross_expense / gross_area × unit_sqm). No sinking fund calculator, no special assessment allocation, no delinquency penalty computation (12% p.a. max per ECR §8.5), no assessment lien amount per RA 4726 §20. Condo corporations use internal spreadsheets with no standardization. SC GR 215801 tax treatment still misapplied by many. |
| Market Frequency | 4 | Every condo unit, monthly. Hundreds of thousands of condo units in Metro Manila alone. Growing rapidly with vertical development trend. Relevant to: condo corporations (computation), property managers (billing), unit owners (verification), and prospective buyers (cost estimation). |
| Moat Defensibility | 4 | ECR 001-17 formula engine with contingency buffers. Per-condo-corp data requirement (board-approved annual budget, master deed allocations, by-law penalty rates). SC GR 215801 tax treatment (invalidated RMC 65-2012; TRAIN §109(1)(Y) exemption). Assessment lien priority rules (First Marbella foreclosure limits). Dues increase compliance (10% cap per RA 9904 IRR). Multi-regulation interaction (RA 4726, RA 9904, ECR 001-17, TRAIN Law, SC rulings). Significant regulatory depth. |
| **Composite** | **80** | |

---

## Composite Ranking

| Rank | Computation | A | F | M | Composite | Tier |
|------|-------------|:-:|:-:|:-:|:---------:|------|
| 1 | assessment-level-lookup | 4 | 5 | 5 | **100** | Tier 1 |
| 2 | socialized-housing-compliance | 5 | 4 | 4 | **80** | Tier 1 |
| 3 | condo-association-dues | 5 | 4 | 4 | **80** | Tier 1 |
| 4 | bp220-lot-compliance | 5 | 3 | 5 | **75** | Tier 1 |
| 5 | improvement-depreciation | 5 | 3 | 5 | **75** | Tier 1 |
| 6 | developer-equity-schedule | 4 | 5 | 3 | **60** | Tier 2 |
| 7 | rent-increase-computation | 5 | 4 | 3 | **60** | Tier 2 |
| 8 | notarial-fees | 5 | 5 | 2 | **50** | Tier 2 |
| 9 | pagibig-amortization | 3 | 5 | 3 | **45** | Tier 2 |
| 10 | broker-commission | 3 | 5 | 3 | **45** | Tier 2 |
| 11 | ltv-ratio | 4 | 4 | 2 | **32** | Tier 3 |
| 12 | bank-mortgage-amortization | 2 | 5 | 3 | **30** | Tier 3 |
| 13 | maceda-refund | 5 | 3 | 2 | **30** | Tier 3 |
| 14 | pagibig-loan-eligibility | 2 | 5 | 2 | **20** | Tier 3 |
| 15 | rod-registration-fees | 2 | 5 | 2 | **20** | Tier 3 |
| 16 | condo-common-area-pct | 5 | 2 | 2 | **20** | Tier 3 |

---

## Tier Analysis

### Tier 1: High-Opportunity (composite ≥ 75) — 5 computations

**Unserved regulatory computations with deep data moats.**

These share two properties: (a) zero or poor tool coverage, and (b) data acquisition barriers that create compounding advantage once built.

| Computation | Why It's Top-Tier | Key Risk |
|-------------|-------------------|----------|
| assessment-level-lookup (100) | Every property, nationwide. LGU database moat across 1,488+ jurisdictions. RA 12001 creates regulatory tailwind. Shares data layer with improvement-depreciation. | LGU data acquisition cost: SMVs, BUCC schedules, RPT rates are non-standardized, some paper-only. ~60% of SMVs outdated. |
| socialized-housing-compliance (80) | Mandatory for every socialized housing project. Deep regulatory knowledge (JMC + zonal values + 6 compliance modes). Zero tools despite being the largest housing market segment. | JMC updates every 2–3 years require monitoring. Cross-reference with BIR zonal values adds external dependency. |
| condo-association-dues (80) | Monthly computation for every condo unit. Growing market. SC GR 215801 creates regulatory complexity that most condo corps still get wrong. | Requires per-condo-corp budget data — distribution model must solve for this (SaaS per-corp vs. estimation engine). |
| bp220-lot-compliance (75) | Deepest branching logic of all 16 computations. Entirely manual today. Very hard to replicate correctly (multi-IRR interaction, JMC layering). | Niche audience (architects, developers, DHSUD examiners). Lower market frequency (per-project, not per-transaction). |
| improvement-depreciation (75) | Zero tools. Shares LGU data moat with assessment-level-lookup. RA 12001 mandates 3-year BUCC revision cycle. | Primarily serves government assessors — may need to target LGU modernization market rather than consumer/broker market. |

**Tier 1 strategic insight:** Three of five (#1, #5, #2) share the BIR zonal value / LGU assessment data layer. Building this shared data infrastructure once serves all three computations and creates a compounding data moat that grows with each LGU added.

### Tier 2: Medium-Opportunity (composite 45–60) — 5 computations

**High-frequency computations with moderate gaps — either partially served or moderate moats.**

| Computation | Why It's Mid-Tier | Best Angle |
|-------------|-------------------|------------|
| developer-equity-schedule (60) | Highest-frequency unserved computation (every buyer interaction). High error rate. But moat is moderate — developer data is accessible. | Multi-developer sample computation engine. Key differentiator: unified interface across Ayala Land, SMDC, DMCI, Megaworld. Lifecycle value: feeds into Maceda refund, loan takeout. |
| rent-increase-computation (60) | Zero tools for 16+ years of an actively enforced law. Millions of rental units. | Tenant/landlord compliance tool. NHSB historical rate database is the key data asset. Low build complexity but requires annual NHSB resolution tracking. |
| notarial-fees (50) | Zero tools, every-transaction frequency. But limited by partial non-determinism — only 2 of 5 sub-computations are fully automatable. | Foreclosure fee computation (fully deterministic) + fee verification/benchmarking. Closing cost aggregation component rather than standalone tool. |
| pagibig-amortization (45) | Universal need but partially served. MRI/FGI premium gap is the key differentiator. | Full amortization schedule with insurance premium transparency. Key differentiator over existing tools: MRI/FGI line-item breakdown. |
| broker-commission (45) | Partially served by iRealtee (SaaS-locked). Standalone calculator gap. | Open-access multi-tier commission calculator with correct RR 11-2018 EWT rates (5%/10%, not 10%/15%). MLS co-broke and lease commission. |

**Tier 2 strategic insight:** Developer-equity-schedule and rent-increase-computation are the strongest candidates for dedicated deep-dive loops — high frequency, zero/poor coverage, and clear user need. Notarial-fees should be built as a component of closing cost aggregation, not standalone.

### Tier 3: Lower-Opportunity (composite ≤ 32) — 6 computations

**Either adequately served, low frequency, or low moat.**

| Computation | Why It's Lower-Tier | Still Worth Building? |
|-------------|--------------------|-----------------------|
| ltv-ratio (32) | Poor coverage but sub-computation, not standalone need. Low moat. | Yes — as module within eligibility/loan comparison engine. |
| bank-mortgage-amortization (30) | Already well-served for basic computation. Gaps only in repricing/comparison. | Yes — multi-bank comparison + repricing scenario modeling is unserved. Build as enhancement, not greenfield. |
| maceda-refund (30) | Zero tools and high error rate, but low frequency and low moat. | Yes — trivial to build (composite complexity 6). "Quick win" that delivers high practitioner value relative to build cost. |
| pagibig-loan-eligibility (20) | Official tool exists. Low moat. | Only as part of integrated loan comparison engine. |
| rod-registration-fees (20) | Official LRA ERCF tool exists. Low moat. | Only as component of closing cost aggregation pipeline. |
| condo-common-area-pct (20) | Zero tools but very low frequency. Simple formula. | Only as module within condo management suite. |

**Tier 3 strategic insight:** Maceda-refund deserves attention despite low composite — it's the highest automation gap × lowest build complexity computation. Zero tools, very high error rate (per workflow analysis), and trivial to implement. A "low-hanging fruit" quick win.

---

## Cross-Dimensional Insights

### 1. The Moat-Gap Matrix

Plotting automation_gap (x) against moat_defensibility (y) reveals four quadrants:

**High Gap + High Moat (top-right) — Build These First:**
- assessment-level-lookup (A:4, M:5)
- socialized-housing-compliance (A:5, M:4)
- condo-association-dues (A:5, M:4)
- bp220-lot-compliance (A:5, M:5)
- improvement-depreciation (A:5, M:5)

**High Gap + Low Moat (bottom-right) — Quick Wins:**
- maceda-refund (A:5, M:2)
- rent-increase-computation (A:5, M:3)
- condo-common-area-pct (A:5, M:2)
- notarial-fees (A:5, M:2)

**Low Gap + High Moat (top-left) — Moat Exists but Served:**
- (none — all high-moat computations are also underserved)

**Low Gap + Low Moat (bottom-left) — Skip/Commodity:**
- pagibig-loan-eligibility (A:2, M:2)
- rod-registration-fees (A:2, M:2)
- bank-mortgage-amortization (A:2, M:3)

### 2. Data Layer Clustering

Shared data infrastructure creates bundle economics:

| Data Layer | Computations Served | Build-Once Value |
|-----------|---------------------|-----------------|
| LGU assessment database (SMV, BUCC, RPT rates) | assessment-level-lookup, improvement-depreciation | 2 Tier-1 computations. ~₱100 composite points. |
| BIR zonal values | assessment-level-lookup, socialized-housing-compliance, rod-registration-fees | 1 Tier-1 + 1 Tier-1 + 1 Tier-3. Cross-loop: also serves ph-tax-computations (CGT, DST). |
| DHSUD JMC ceilings | socialized-housing-compliance, bp220-lot-compliance, pagibig-loan-eligibility | 2 Tier-1 + 1 Tier-3. |
| Developer payment terms | developer-equity-schedule, maceda-refund | 1 Tier-2 + 1 Tier-3. |
| NHSB resolutions | rent-increase-computation | 1 Tier-2. Single-purpose but simple to maintain. |
| EWT/VAT thresholds | broker-commission, condo-association-dues, notarial-fees | 1 Tier-2 + 1 Tier-1 + 1 Tier-2. Cross-loop: serves ph-tax-computations. |

### 3. Quick Win vs. Infrastructure Play

Two distinct build strategies emerge:

**Infrastructure plays** (high composite, high moat, requires data layer):
- assessment-level-lookup + improvement-depreciation (shared LGU data)
- socialized-housing-compliance + bp220-lot-compliance (shared DHSUD/JMC data)
- condo-association-dues (per-condo-corp data)

**Quick wins** (zero tools, low complexity, high practitioner pain):
- maceda-refund (composite complexity 6, zero tools, very high error rate)
- rent-increase-computation (simple annual formula, zero tools, millions of rental units)
- condo-common-area-pct (simple formula, zero tools)

Optimal sequencing: quick wins first (prove concept, build user base, demonstrate regulatory expertise), then infrastructure plays (leverage user base to crowdsource LGU data).

### 4. Frequency × Gap Sweet Spot

The highest-value computations balance high frequency with high gap:

| Computation | A × F | Why It Matters |
|-------------|:-----:|---------------|
| developer-equity-schedule | 20 | Every buyer interaction, no tools |
| socialized-housing-compliance | 20 | Every socialized project, no tools |
| rent-increase-computation | 20 | Every rental annually, no tools |
| condo-association-dues | 20 | Every condo monthly, no tools |
| notarial-fees | 25 | Every transaction, no tools (but partially non-deterministic) |
| assessment-level-lookup | 20 | Every property, poor tools |
| improvement-depreciation | 15 | Every improved property, no tools |
| bp220-lot-compliance | 15 | Every socialized project, no tools |

### 5. Cross-Reference to ph-tax-computations-reverse

Several computations bridge both loops:
- **assessment-level-lookup** → determines assessed value → feeds into RPT computation (tax loop)
- **rod-registration-fees** → registration is a fee, but the "higher value rule" (MAX of GSP, BIR zonal, LGU FMV) also determines tax bases for CGT, DST, transfer tax
- **broker-commission EWT/VAT** → withholding and VAT computations are tax-loop territory
- **BIR zonal values** → shared data dependency across both loops (zonal value feeds: CGT base, DST base, transfer tax base, registration fee base, socialized housing ceiling add-on)

---

## Recommendations for Deep-Dive Loops

Based on scoring, the following computations warrant their own dedicated reverse loops:

### Priority 1 (Tier 1, composite ≥ 80)
1. **assessment-level-lookup** (100) — bundled with improvement-depreciation as "PH Property Assessment Engine" loop
2. **socialized-housing-compliance** (80) — bundled with bp220-lot-compliance as "DHSUD Compliance Engine" loop
3. **condo-association-dues** (80) — standalone "Condo Management Computation" loop

### Priority 2 (Tier 2, highest A×F)
4. **developer-equity-schedule** (60) — "Developer Payment Computation Engine" loop
5. **rent-increase-computation** (60) — "Rent Control Compliance Engine" loop (can be a quick build given low complexity)

### Priority 3 (Quick Wins)
6. **maceda-refund** (30) — "Maceda Law Calculator" loop (simplest build, highest impact per line of code)

---

## Methodology Notes

- Automation gap derived from existing-tools-survey coverage matrix (ZERO/POOR/PARTIAL/GOOD → 5/4/3/2 mapping with adjustments for edge case coverage)
- Market frequency estimated from practitioner-workflow lifecycle analysis: transaction volumes (sale/loan/rental), computation instances per transaction, and recurring vs. one-time nature
- Moat defensibility assessed from complexity-scoring dimensions (branching, tables, external deps) plus data acquisition barriers, regulatory depth, and replication difficulty
- Multiplicative formula intentionally penalizes computations weak on any single dimension — a computation needs breadth across all three to rank highly
- Scores calibrated relative to each other within the set of 16, not absolute
