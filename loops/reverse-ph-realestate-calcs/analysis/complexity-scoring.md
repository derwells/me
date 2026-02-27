# Complexity Scoring — All 16 Wave 2 Computations

Wave 3 analysis. Scores each computation across four complexity dimensions to inform Wave 4 opportunity scoring.

## Scoring Rubric

Each dimension scored 1–5. Composite = sum of four dimensions (max 20).

### Branching Rules (decision points in the computation logic)
| Score | Raw Count | Description |
|-------|-----------|-------------|
| 1 | 1–3 | Linear formula, minimal branching |
| 2 | 4–5 | A few conditional paths |
| 3 | 6–8 | Moderate decision tree |
| 4 | 9–12 | Complex multi-step decision tree |
| 5 | 13+ | Deep decision forest with cascading conditions |

### Lookup Tables (static or quasi-static reference tables required)
| Score | Raw Count | Description |
|-------|-----------|-------------|
| 1 | 0–1 | No tables or a single trivial table |
| 2 | 2–3 | A few small tables |
| 3 | 4–5 | Multiple tables, some with graduated brackets |
| 4 | 6–8 | Heavy table dependency, some LGU-specific |
| 5 | 9+ | Massive table infrastructure, multi-dimensional lookups |

### External Data Dependencies (inputs that change independently of computation logic)
| Score | Raw Count | Description |
|-------|-----------|-------------|
| 1 | 0–1 | Self-contained or single external input |
| 2 | 2 | Two external data sources |
| 3 | 3 | Three sources, manageable update burden |
| 4 | 4–5 | Multiple external sources, some non-public or LGU-specific |
| 5 | 6+ | Extensive external dependencies, multi-jurisdictional |

### Update Frequency (how often underlying rules/rates/tables change)
| Score | Frequency | Description |
|-------|-----------|-------------|
| 1 | 5+ years | Statutory, near-permanent |
| 2 | 3–5 years | Regulatory cycle, infrequent revision |
| 3 | 1–3 years | Periodic revision, predictable schedule |
| 4 | Quarterly–yearly | Market-driven, annual resolutions |
| 5 | Daily–monthly | Benchmark-rate-driven, promotional |

## Raw Counts

Data extracted from all 16 Wave 2 analysis files.

| # | Computation | Branching Rules | Lookup Tables | External Deps | Update Frequency |
|---|-------------|-----------------|---------------|---------------|------------------|
| 1 | pagibig-loan-eligibility | 7 (7-step sequential check: membership → age → loan history → credit → property → co-borrowers → loan amount) | 4 (program caps, contribution-to-loan, LTV by category, interest rates by repricing period) | 3 (interest rate table, DHSUD price ceilings, contribution entitlement table) | Medium: annually to every 3 years |
| 2 | pagibig-amortization | 4 (insurance model choice, FGI rate selection, repricing mechanics, payment priority) | 3 (EUF rates by repricing period, subsidized program rates, MRI/FGI rate selection) | 3 (interest rate table, MRI premium rate, FGI/FAPI premium rate) | Medium-High: rates stable since 2023 but insurance rates potentially outdated (last public data 2014–2018) |
| 3 | bank-mortgage-amortization | 5 (repricing formula, early termination, DTI test, LTV limits, amortization factor) | 4 (benchmark rates, bank-specific rate schedules, prepayment fee schedules, LTV by bank/property) | 5 (benchmark rate at repricing, bank spread, prepayment structure, DTI threshold, MRI/CLI premiums) | High: benchmark rates daily/weekly, bank rates quarterly, promos monthly |
| 4 | developer-equity-schedule | 8 (TCP composition, payment option selection, discount application order, late penalty, VAT aggregation, Maceda qualification, penalty cap, HomeReady credit) | 4 (other charges % by developer, scaled discount tables, reservation fee schedule, lump-sum rates) | 4 (spot cash discount rates, in-house financing rates, developer charges %, association dues rates) | High: project-specific and promotional |
| 5 | ltv-ratio | 6 (collateral value selection, Pag-IBIG LTV lookup, bank LTV lookup, property type branching, buyback distinction, lender type distinction) | 5 (Pag-IBIG current LTV, Pag-IBIG older LTV, bank LTV by property, BSP Section 37 ceiling, AHP socialized) | 2 (bank-specific LTV policy, property appraisal value) | Low-Medium: Pag-IBIG tiers stable since 2014; bank policies annual review |
| 6 | maceda-refund | 6 (coverage determination, section applicability, grace period eligibility, CSV tier lookup, cancellation validity, invalid cancellation remedy) | 1 (CSV percentage by years — 13 rows) | 1 (payment history/contract terms — static per contract) | Very Low: statute unchanged since 1972; interpretation evolves via SC rulings every 5–7 years |
| 7 | rent-increase-computation | 6 (coverage determination 9-step tree, tiered bracket lookup, first-year freeze, advance rent compliance, vacancy reset, coverage exit) | 2 (cap rate % table by year/bracket, HUC classification list) | 2 (NHSB annual cap rate resolution, bank savings rate) | Medium-High: cap rates published annually by NHSB |
| 8 | condo-common-area-pct | 8 (default statutory rule, floor-area proportional, par value method, common area RPT, common expense assessment, voting power, dissolution/partition, parking slot treatment) | 3 (RPT rate brackets by LGU type, sinking fund/delinquency rates, setback calculations) | 3 (master deed allocation, LGU RPT rate schedule, condo corp annual budget) | Low: master deed set at inception; RPT rates change infrequently |
| 9 | socialized-housing-compliance | 12 (housing category classification, base ceiling lookup, zonal value add-on, lot-only sub-rule, government guarantee eligibility, balanced housing requirement × 6 compliance modes, ceiling currency check) | 3 (selling price brackets, base price ceiling matrix, zonal value add-on table) | 2 (BIR zonal values, JMC validity/update cycle) | Medium-High: JMCs updated every 2–3 years; zonal values updated periodically |
| 10 | bp220-lot-compliance | 15 (project classification, lot area, lot frontage, floor area, open space, community facility, road ROW, setback, building separation, parking, row house block limits, price ratio — each with sub-conditions) | 6 (lot area minimums, lot frontage minimums, open space by density, community facility by density, road ROW matrix, multi-family setback by storey) | 2 (selling price ceilings per JMC, National Building Code for >12 storeys) | Medium: JMCs every 2–3 years; BP 220 IRR (2008) stable; DHSUD TWG reviewing but no amendments as of Feb 2026 |
| 11 | assessment-level-lookup | 12 (classification by actual use, special class check, land/building/machinery branching, land classification lookup, 5 building FMV bracket sub-tables, machinery classification, total AV summation, RPT tier computation) | 15 (6 land rates + 4 building sub-tables with 29 brackets + 4 machinery rates + 5 special class rates + penalty/discount tables) | 6 (LGU assessment ordinances, LGU basic RPT rate, Schedule of Market Values, BUCC schedule, NHSB idle land classification, RA 12001 transition cap) | Irregular: Section 218 maximums unchanged since 1991; LGU SMV/BUCC target every 3 years per RA 12001; LGU rates irregular |
| 12 | improvement-depreciation | 8 (construction type classification, BUCC rate lookup, RCN computation, depreciation method selection, effective age determination, LGU depreciation table lookup, percent good application, machinery depreciation) | 8+ (construction type table, economic life by type, BUCC rates by type, 3+ depreciation tables by type/maintenance, machinery residual value floor, adjustment factors) | 5 (BUCC schedule, LGU depreciation table, adjustment factors, DPWH construction cost data, Philippine Valuation Standards under RA 12001) | Medium: BUCC schedules and depreciation tables target 3-year revision per RA 12001 |
| 13 | rod-registration-fees | 9 (value basis determination, bracket selection ≤₱1.7M vs >₱1.7M, CEIL vs integer division, entry fee, ODT fee, CTC fee variant, legal research fee, assurance fund, IT fee) | 4 (17-tier registration fee table, mortgage annotation tiers, other annotation fees, CTC page-rate structure) | 3 (LRA fee schedule, property valuation, document type/complexity) | Rare: last comprehensive revision LRA Circular 11-2002; Circular 13-2016 operative; no post-2016 amendments |
| 14 | notarial-fees | 7 (document type, OCA ceiling, foreclosure fee tiers, IBP chapter selection, VAT applicability, income threshold for tax option, page count) | 4 (OCA ceiling table, foreclosure fee formula/brackets, IBP chapter schedules by locality, unattributed tiered table) | 4 (IBP chapter fee schedules, notary annual gross income, document drafting complexity, SC amendments) | Stable: OCA Circular 73-2014 current since 2014; IBP schedules vary; VAT threshold stable since TRAIN (2018) |
| 15 | broker-commission | 10 (property type, transaction type, commission rate selection, split type, referral fee, multi-tier distribution, co-brokerage, EWT rate, VAT threshold, finder's fee distinction) | 5 (commission rate benchmarks by property type, split ratio presets, EWT tier table per RR 11-2018, multi-tier distribution model, VAT/tax options) | 4 (contractual commission rate, brokerage split conventions, payee annual gross income, sworn declaration status) | Yearly: commission rates market-driven; EWT rates per RR 11-2018 (stable since 2018); sworn declaration annual |
| 16 | condo-association-dues | 11 (member vs beneficial user, sinking fund method, special assessment trigger, delinquency penalty, assessment lien registration, lien priority, commercial income VAT, dues VAT exemption, increase compliance, tax status streams, SC ruling impact) | 5 (contingency buffer by member type, sinking fund ranges, delinquency rates, lien components, commercial income tax tiers) | 5 (board-approved annual budget, master deed/restrictions, condo corp by-laws, DHSUD/HSAC guidance, BIR tax treatment per SC ruling) | Annual: budget yearly; penalty rates stable unless by-laws amended; SC GR 215801 now settled law |

## Normalized Scores (1–5)

| # | Computation | Branching (B) | Tables (T) | Ext Deps (D) | Update Freq (U) | Composite |
|---|-------------|:---:|:---:|:---:|:---:|:---:|
| 1 | pagibig-loan-eligibility | 3 | 3 | 3 | 3 | **12** |
| 2 | pagibig-amortization | 2 | 2 | 3 | 3 | **10** |
| 3 | bank-mortgage-amortization | 2 | 3 | 4 | 5 | **14** |
| 4 | developer-equity-schedule | 3 | 3 | 4 | 4 | **14** |
| 5 | ltv-ratio | 3 | 3 | 2 | 2 | **10** |
| 6 | maceda-refund | 3 | 1 | 1 | 1 | **6** |
| 7 | rent-increase-computation | 3 | 2 | 2 | 4 | **11** |
| 8 | condo-common-area-pct | 3 | 2 | 3 | 2 | **10** |
| 9 | socialized-housing-compliance | 4 | 2 | 2 | 3 | **11** |
| 10 | bp220-lot-compliance | 5 | 4 | 2 | 3 | **14** |
| 11 | assessment-level-lookup | 4 | 5 | 5 | 3 | **17** |
| 12 | improvement-depreciation | 3 | 4 | 4 | 3 | **14** |
| 13 | rod-registration-fees | 4 | 3 | 3 | 2 | **12** |
| 14 | notarial-fees | 3 | 3 | 4 | 2 | **12** |
| 15 | broker-commission | 4 | 3 | 4 | 4 | **15** |
| 16 | condo-association-dues | 4 | 3 | 4 | 4 | **15** |

## Composite Ranking

| Rank | Computation | Composite | Complexity Tier | Primary Driver |
|------|-------------|:---------:|-----------------|----------------|
| 1 | assessment-level-lookup | 17 | Heavy | 15 lookup tables × 6 external deps — LGU-dependent multi-dimensional tables |
| 2 | broker-commission | 15 | Heavy | 10 branch points × 4 external deps × annual market shifts |
| 3 | condo-association-dues | 15 | Heavy | 11 branches × 5 external deps × annual budget cycles |
| 4 | bank-mortgage-amortization | 14 | Heavy | Daily benchmark volatility (score-5 update freq) × 5 external deps |
| 5 | developer-equity-schedule | 14 | Heavy | 8 branches × 4 project-specific external deps × promotional churn |
| 6 | bp220-lot-compliance | 14 | Heavy | Deepest branching (15 decision points) × 6 lookup tables |
| 7 | improvement-depreciation | 14 | Heavy | 8+ LGU-specific depreciation tables × 5 external deps |
| 8 | pagibig-loan-eligibility | 12 | Moderate | 7-step sequential gate × 4 tables — balanced across all dimensions |
| 9 | rod-registration-fees | 12 | Moderate | 9 fee components but stable tables and rare updates |
| 10 | notarial-fees | 12 | Moderate | 4 external deps (IBP locality-specific) but infrequent changes |
| 11 | rent-increase-computation | 11 | Moderate | Annual NHSB cap rate dependency drives update score |
| 12 | socialized-housing-compliance | 11 | Moderate | 12 branches but only 2 external deps and 3 simple tables |
| 13 | pagibig-amortization | 10 | Moderate | Low branching, but MRI/FGI rate data risk (last public data 2014–2018) |
| 14 | ltv-ratio | 10 | Moderate | 5 lookup tables but low external deps and stable policies |
| 15 | condo-common-area-pct | 10 | Moderate | Moderate branching, low update frequency, project-specific master deed |
| 16 | maceda-refund | 6 | Light | Near-pure statutory computation — 1 table, 1 dep, unchanged since 1972 |

## Complexity Profile Clusters

### Heavy Infrastructure (composite ≥ 14) — 7 computations

These require one or more of: LGU-specific database maintenance, external rate feeds, deep table infrastructure, or frequent data updates.

| Computation | Key Infrastructure Need |
|-------------|------------------------|
| assessment-level-lookup | LGU SMV/BUCC database (1,488+ LGUs), Section 218 table engine, RA 12001 transition tracking |
| broker-commission | Contractual rate benchmarks, multi-tier split engine, EWT/VAT computation with annual declaration tracking |
| condo-association-dues | Per-condo-corp budget data, by-law penalty rates, ECR 001-17 formula engine, SC ruling compliance |
| bank-mortgage-amortization | Daily benchmark rate feed (BVAL, T-bill, PHIREF), per-bank rate/policy database (8+ banks) |
| developer-equity-schedule | Per-developer/per-project discount tables, promotional rate tracking, penalty model variants |
| bp220-lot-compliance | 6 lookup tables × 12+ compliance checks, JMC ceiling integration, density-based formula engine |
| improvement-depreciation | Per-LGU BUCC rates, per-LGU depreciation tables (age × type × maintenance), dual classification systems |

**Automation implication:** High barrier to entry — requires significant data acquisition and maintenance infrastructure. Strong moat potential for whoever builds and maintains the data layer.

### Moderate (composite 10–12) — 8 computations

Deterministic with manageable data dependencies. Periodic updates on predictable schedules.

| Computation | Key Characteristic |
|-------------|-------------------|
| pagibig-loan-eligibility | Well-documented 7-step gate; data from government circulars; contribution-to-loan gap for ₱3M–₱6M |
| rod-registration-fees | Most standardized computation — national fee table, LRA ERCF tool exists but limited |
| notarial-fees | Partially deterministic — 2 fully deterministic (OCA ceiling, foreclosure), 1 conditional (IBP-based) |
| rent-increase-computation | Single annual external dependency (NHSB cap rate); historical rate table compilable |
| socialized-housing-compliance | Deep branching but few tables/deps; JMC ceilings update every 2–3 years |
| pagibig-amortization | Standard amortization formula; main risk is stale insurance rate data |
| ltv-ratio | Table-heavy but stable; straightforward min-function logic |
| condo-common-area-pct | Per-project master deed determines method; low update burden once set |

**Automation implication:** Moderate build effort, lower maintenance burden. Good candidates for standalone calculators or modules within a larger system.

### Light (composite ≤ 9) — 1 computation

| Computation | Key Characteristic |
|-------------|-------------------|
| maceda-refund | Pure statutory formula from 1972; 1 lookup table; nearly zero external dependencies; interpretation evolves only via rare SC decisions |

**Automation implication:** Trivial to build, trivial to maintain. Low moat but high utility — zero existing tools cover it (per existing-tools-survey).

## Cross-Cutting Insights

### 1. Complexity ≠ Opportunity

The simplest computation (maceda-refund, composite 6) has **zero** tool coverage while the most complex (assessment-level-lookup, composite 17) has partial coverage via LGU assessor systems. Complexity scoring feeds into Wave 4 but does NOT directly determine automation priority — that requires combining complexity with automation gap and market frequency.

### 2. LGU Variability Is the Dominant Complexity Driver

Three of the seven "heavy" computations (assessment-level-lookup, improvement-depreciation, bp220-lot-compliance) derive their complexity primarily from LGU-specific data variation rather than algorithmic difficulty. The core formulas are straightforward; the data layer is the barrier.

### 3. Update Frequency Separates Two Worlds

- **Market-driven computations** (bank-mortgage-amortization, developer-equity-schedule, broker-commission) require near-real-time data feeds or frequent manual updates.
- **Regulatory computations** (maceda-refund, bp220-lot-compliance, socialized-housing-compliance, rod-registration-fees) change on multi-year cycles, making them durable once built.

This suggests different product architectures: regulatory computations suit static engines with periodic batch updates; market-driven computations need live data integration.

### 4. Partial Determinism Matters

Not all 16 computations are equally automatable:
- **Fully deterministic given inputs** (14 of 16): formula + table lookups only
- **Partially deterministic** (2 of 16): notarial-fees (2 of 5 sub-computations are non-deterministic — market heuristic and professional fee), condo-common-area-pct (method depends on master deed which varies by project)

### 5. Data Acquisition Clusters

Several computations share external data sources, creating build-once-use-many-times opportunities:
- **BIR zonal values**: used by assessment-level-lookup, socialized-housing-compliance, rod-registration-fees
- **LGU assessment data** (SMV, BUCC, RPT rates): used by assessment-level-lookup, improvement-depreciation
- **DHSUD JMC ceilings**: used by socialized-housing-compliance, bp220-lot-compliance, pagibig-loan-eligibility
- **Pag-IBIG interest/LTV tables**: used by pagibig-loan-eligibility, pagibig-amortization, ltv-ratio
- **EWT/VAT thresholds**: used by broker-commission, condo-association-dues, notarial-fees

A shared data layer serving these clusters would reduce marginal complexity for each additional computation engine.

## Methodology Notes

- Branching rules counted from Wave 2 analysis decision trees (each distinct conditional path or check = 1 branch)
- Lookup tables counted as distinct reference structures (a graduated table with multiple brackets = 1 table; related tables for different property types = separate tables)
- External dependencies counted as distinct data sources that change independently of the computation's legal basis
- Update frequency assessed from documented revision history and regulatory cycle patterns noted in Wave 2 verification
- All counts are conservative — edge cases and sub-conditions within each branch are not double-counted
