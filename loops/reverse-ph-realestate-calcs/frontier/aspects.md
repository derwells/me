# Analysis Frontier — PH Real Estate Calculations Survey

## Statistics
- Total aspects discovered: 29
- Analyzed: 14
- Pending: 15
- Convergence: 48%

## Pending Aspects (ordered by dependency)

### Wave 1: Source Acquisition
- [x] pagibig-housing-loan-circulars — Fetch Pag-IBIG Fund Circular No. 423 and amendments; extract loan eligibility rules, loan limits, interest rates, MRI/FGI rates
- [x] bsp-residential-lending — Fetch BSP circulars on residential real estate lending; LTV limits, stress test requirements, repricing rules
- [x] maceda-law-text — Fetch RA 6552 full text + key Supreme Court rulings (Rillo v. CA, Active Realty v. Daroya); extract refund/grace period computation rules
- [x] rent-control-act — Fetch RA 9653 + DHSUD implementing rules; extract allowable rent increase formula and coverage thresholds
- [x] condo-act-common-areas — Fetch RA 4726 (Condominium Act) + HLURB/DHSUD rules; extract common area percentage computation requirements
- [x] dhsud-price-ceilings — Fetch current DHSUD issuances on socialized/economic/low-cost housing price ceilings and lot size standards
- [x] bp220-standards — Fetch BP 220 implementing rules; extract minimum lot area, floor area, and open space standards per housing type
- [x] rod-fee-schedules — Fetch Registry of Deeds fee schedules for title registration and annotation
- [x] prc-broker-regulations — Fetch PRC and RESA (RA 9646) rules on real estate broker commission structures and splits
- [x] developer-payment-terms — Fetch published payment computation terms from 3-4 major developers (Ayala Land, SMDC, DMCI, Megaworld) to identify common equity schedule patterns

### Wave 2: Computation Extraction
Depends on Wave 1 data.
- [x] pagibig-loan-eligibility — Eligibility decision tree: contribution months, age limits, salary cap, property type, loan-on-top-of-loan rules
- [x] pagibig-amortization — Amortization schedule: declining balance method, interest rate tiers by loan amount, MRI premium computation, FGI premium computation
- [x] bank-mortgage-amortization — Standard bank mortgage amortization: fixed vs variable rate, repricing mechanics, early termination penalty formulas
- [x] developer-equity-schedule — Developer equity/downpayment computation: spot cash discount, installment penalty/surcharge, reservation fee deduction, turnover balance
- [ ] ltv-ratio — Loan-to-value ratio computation per BSP circular: appraisal basis, LTV caps by property type, additional collateral rules
- [ ] maceda-refund — Maceda Law refund computation: 2-year threshold test, 50% + 5%/yr formula, surrender value, grace period calculation
- [ ] rent-increase-computation — Rent Control Act: allowable annual increase percentage by unit rental value bracket, coverage determination (residential ≤ ₱10K/month)
- [ ] condo-common-area-pct — Condominium common area allocation: percentage computation, undivided interest formula, master deed requirements
- [ ] socialized-housing-compliance — DHSUD price ceiling compliance check: per-unit and per-sqm limits by housing type, annual escalation rules
- [ ] bp220-lot-compliance — BP 220 standards compliance: minimum lot area, floor area ratio, open space percentage by development type
- [ ] assessment-level-lookup — Property assessment level by classification and LGU: residential/commercial/industrial/agricultural tiers per Local Government Code
- [ ] improvement-depreciation — Depreciation schedule for building improvements: straight-line method, useful life by construction type, residual value rules per local assessor
- [ ] rod-registration-fees — Registry of Deeds fee computation: fee schedule by property value bracket, annotation fees, additional charges
- [ ] notarial-fees — Notarial fee computation: fee schedule per notarial rules, percentage-of-value basis for real estate documents
- [ ] broker-commission — Real estate broker commission: standard rates, split computation (listing broker vs selling broker), VAT implications on commission
- [ ] condo-association-dues — HLURB-prescribed monthly condo dues computation: rate base = gross expense / gross area; dues per unit = unit sqm × monthly rate; VAT implications; discovered in condo-act-common-areas analysis

### Wave 3: Competitive & Automation Gap Analysis
Depends on Wave 2 data.
- [ ] existing-tools-survey — Map each Wave 2 computation against existing PH tools: Pag-IBIG online calculator, Lamudi, Hoppler, developer portals, generic mortgage calculators, PropTech startups
- [ ] practitioner-workflow — Document current manual/Excel workflows per computation; synthesis from practitioner guides and developer sales processes
- [ ] complexity-scoring — Score each computation by branching rules, lookup tables, external data dependencies, update frequency

### Wave 4: Scoring & Synthesis
Depends on Wave 3 data.
- [ ] opportunity-scoring — Score each computation: automation_gap × market_frequency × moat_defensibility (1-5 each)
- [ ] catalog-draft — Produce ranked opportunity catalog at output/opportunity-catalog.md; cross-reference with ph-tax-computations-reverse catalog
- [ ] catalog-review — Self-review for completeness, actionability, and correctness of scoring

## Recently Analyzed
- pagibig-housing-loan-circulars (Wave 1, 2026-02-25)
- bsp-residential-lending (Wave 1, 2026-02-25)
- maceda-law-text (Wave 1, 2026-02-25)
- rent-control-act (Wave 1, 2026-02-25)
- condo-act-common-areas (Wave 1, 2026-02-25)
- dhsud-price-ceilings (Wave 1, 2026-02-25)
- bp220-standards (Wave 1, 2026-02-26)
- prc-broker-regulations (Wave 1, 2026-02-26)
- developer-payment-terms (Wave 1, 2026-02-26)
- pagibig-loan-eligibility (Wave 2, 2026-02-26)
- pagibig-amortization (Wave 2, 2026-02-26) — verified via 15 independent sources + independent computation
- bank-mortgage-amortization (Wave 2, 2026-02-26) — verified via 15+ sources; 3 key corrections to common claims
- developer-equity-schedule (Wave 2, 2026-02-26) — 8 core computations verified via 25+ sources; 3 critical corrections (VAT threshold, BSP 957 attribution, PD 957 escalation cap)
