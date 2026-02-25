# Analysis Frontier — PH Tax Computations Survey

## Statistics
- Total aspects discovered: 24
- Analyzed: 2
- Pending: 22
- Convergence: 8%

## Pending Aspects (ordered by dependency)

### Wave 1: Source Acquisition
- [x] nirc-tax-titles — Fetch NIRC Title II (income tax on real property), Title IV (VAT), Title VI (stamp taxes); extract computation-relevant provisions
- [x] bir-revenue-regulations — Fetch key RRs: RR 7-2003 (asset classification criteria), RR 2-98 as amended (EWT rates), RR 16-2005 (withholding on real property), TRAIN law amendments to real property taxation
- [ ] practitioner-guides — Fetch worked examples from Grant Thornton PH, PwC PH, BDB Law, Respicio & Co. tax alerts covering real estate tax computations
- [ ] bir-form-structures — Fetch BIR form instructions for Forms 1706 (CGT), 2000-OT (DST), 2550Q (VAT), 1601-EQ (EWT), 2307 (withholding certificate)
- [ ] zonal-value-samples — Fetch sample zonal value schedules from 3-4 RDOs to understand format, structure, and lookup resolution logic

### Wave 2: Computation Extraction
Depends on Wave 1 data.
- [ ] highest-of-three-base — Tax base resolution: max(selling price, zonal value, assessed FMV); lookup sources, comparison logic, which taxes use this base
- [ ] cgt-computation — 6% capital gains tax on real property sale (BIR Form 1706); inputs, formula, deadline rules, surcharge/interest computation
- [ ] dst-on-sale — 1.5% documentary stamp tax on conveyance (NIRC Section 196); base, rate, deadline (5 days post-notarization)
- [ ] dst-on-mortgage — DST on mortgage instruments (NIRC Section 195); separate rate schedule, triggers, computation
- [ ] vat-real-property — 12% VAT on real property; ₱3.6M threshold test, ordinary asset determination, exempt vs taxable classification
- [ ] installment-vat-schedule — Output VAT recognition per collection on installment sales (RMC 99-2023); payment schedule tracking, recognition timing
- [ ] cwt-rate-and-timing — CWT rate selection (1.5-6%) based on seller type and price; 25%-of-price threshold test for installment withholding timing
- [ ] ewt-rate-classification — Real estate subset of 80+ EWT categories under RR 2-98; decision tree for rate selection on rent, commissions, professional fees, contractor payments
- [ ] rpt-computation — Real property tax: FMV × assessment level × tax rate; per-LGU variation, property classification tiers, SEF levy
- [ ] transfer-tax — LGU-level transfer tax on real property sale; rate variation by locality, base computation
- [ ] form-2307-issuance — Who withholds, when to issue, amount computation, reconciliation logic (issued vs received for tax credit claims)
- [ ] zonal-value-lookup — Resolution logic for BIR zonal values by location; RDO jurisdiction mapping, format parsing, update frequency

### Wave 3: Competitive & Automation Gap Analysis
Depends on Wave 2 data.
- [ ] existing-tools-survey — Map each Wave 2 computation against JuanTax, Taxumo, QNE Cloud, generic ERPs; document feature coverage
- [ ] practitioner-workflow — Document current manual/Excel workflows per computation; interview-style synthesis from practitioner guide examples
- [ ] complexity-scoring — Score each computation by number of branching rules, lookup tables, external data dependencies

### Wave 4: Scoring & Synthesis
Depends on Wave 3 data.
- [ ] opportunity-scoring — Score each computation: automation_gap × market_frequency × moat_defensibility (1-5 each)
- [ ] catalog-draft — Produce ranked opportunity catalog at output/opportunity-catalog.md
- [ ] catalog-review — Self-review for completeness, actionability, and correctness of scoring

## Recently Analyzed
- nirc-tax-titles (Wave 1, 2026-02-25)
- bir-revenue-regulations (Wave 1, 2026-02-25)
