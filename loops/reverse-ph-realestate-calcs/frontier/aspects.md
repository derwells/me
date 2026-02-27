# Analysis Frontier — PH Real Estate Calculations Survey

## Statistics
- Total aspects discovered: 29
- Analyzed: 32
- Pending: 0
- Convergence: 100% (all waves complete)

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
- [x] ltv-ratio — Loan-to-value ratio computation per BSP circular: appraisal basis, LTV caps by property type, additional collateral rules
- [x] maceda-refund — Maceda Law refund computation: 2-year threshold test, 50% + 5%/yr formula, surrender value, grace period calculation
- [x] rent-increase-computation — Rent Control Act: allowable annual increase percentage by unit rental value bracket, coverage determination (residential ≤ ₱10K/month)
- [x] condo-common-area-pct — Condominium common area allocation: percentage computation, undivided interest formula, master deed requirements
- [x] socialized-housing-compliance — DHSUD price ceiling compliance check: per-unit and per-sqm limits by housing type, annual escalation rules
- [x] bp220-lot-compliance — BP 220 standards compliance: minimum lot area, floor area ratio, open space percentage by development type
- [x] assessment-level-lookup — Property assessment level by classification and LGU: residential/commercial/industrial/agricultural tiers per Local Government Code
- [x] improvement-depreciation — Depreciation schedule for building improvements: straight-line method, useful life by construction type, residual value rules per local assessor
- [x] rod-registration-fees — Registry of Deeds fee computation: fee schedule by property value bracket, annotation fees, additional charges
- [x] notarial-fees — Notarial fee computation: fee schedule per notarial rules, percentage-of-value basis for real estate documents
- [x] broker-commission — Real estate broker commission: standard rates, split computation (listing broker vs selling broker), VAT implications on commission
- [x] condo-association-dues — HLURB-prescribed monthly condo dues computation: rate base = gross expense / gross area; dues per unit = unit sqm × monthly rate; VAT implications; discovered in condo-act-common-areas analysis

### Wave 3: Competitive & Automation Gap Analysis
Depends on Wave 2 data.
- [x] existing-tools-survey — Map each Wave 2 computation against existing PH tools: Pag-IBIG online calculator, Lamudi, Hoppler, developer portals, generic mortgage calculators, PropTech startups
- [x] practitioner-workflow — Document current manual/Excel workflows per computation; synthesis from practitioner guides and developer sales processes
- [x] complexity-scoring — Score each computation by branching rules, lookup tables, external data dependencies, update frequency

### Wave 4: Scoring & Synthesis
Depends on Wave 3 data.
- [x] opportunity-scoring — Score each computation: automation_gap × market_frequency × moat_defensibility (1-5 each)
- [x] catalog-draft — Produce ranked opportunity catalog at output/opportunity-catalog.md; cross-reference with ph-tax-computations-reverse catalog
- [x] catalog-review — Self-review for completeness, actionability, and correctness of scoring

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
- ltv-ratio (Wave 2, 2026-02-26) — verified via 24+ sources across 5 categories; 5 corrections to primary extraction (wrong circular number, outdated tiers, missing bracket value, LTV cap oversimplification, Circular 688 characterization)
- maceda-refund (Wave 2, 2026-02-26) — verified via 8 independent sources; 3 corrections (interest exclusion too broad, years counting is value-based per Orbe v. Filinvest, Section 4 notice must be notarized); 6 computations extracted
- rent-increase-computation (Wave 2, 2026-02-26) — verified via 12 independent sources; 1 critical correction (2018-2020 three-tier rates); 6 sub-computations extracted; Respicio Joint Resolution claims rejected as unverifiable
- condo-common-area-pct (Wave 2, 2026-02-26) — verified via 16 independent sources; 1 critical correction (RA 7899 voting scope overstated); 3 high-severity corrections (parking CCT denominator, missing par value method, multi-unit voting); 6 additional sub-computations discovered
- socialized-housing-compliance (Wave 2, 2026-02-26) — 5 sub-computations verified via 20+ sources; all ceiling figures confirmed; labeling discrepancy for L2/L3 classification noted; lot-only ceiling sub-rule discovered (40% of house-and-lot); HGC→PhilGuarantee entity correction; BOI 20% SHR distinguished from balanced housing requirement
- bp220-lot-compliance (Wave 2, 2026-02-26) — 12 compliance checks verified against 9 independent sources; all 12 CONFIRMED with zero corrections needed; 10 additional deterministic checks identified (firewall, drainage, road pavement, block length, completion level, tree planting, elevator, fire suppression, roof eave clearance, water supply); full decision tree with 12-step compliance algorithm produced; VIZCODE pre-2008 values flagged as outdated; JMC floor area layering (18→32→28→24 sqm) fully documented
- assessment-level-lookup (Wave 2, 2026-02-26) — 8 sub-computations extracted (classification, land/building/machinery/special assessment levels, total AV, RPT pipeline, payment penalties); all 34 table values verified against 9 sources with zero corrections; RA 12001 impact analyzed (preserves Section 218 maximums, adds 6% transition cap); 5 unresolved ambiguities (1991 bracket thresholds unadjusted, mixed-use allocation, LGU rate database gap)
- notarial-fees (Wave 2, 2026-02-27) — 5 computations extracted (OCA per-page ceiling, notarial foreclosure fee, IBP-based DOAS/REM fee, market heuristic, unattributed tiered table); CRITICAL CORRECTION: A.M. No. 19-08-15-SC is Rules on Evidence, NOT a notarial fee amendment — tiered table attribution fabricated; OCA Circular 73-2014 ₱200/₱50 ceiling confirmed; foreclosure fee 5%/2.5% + ₱100K cap confirmed; 2 fully deterministic, 1 conditional, 2 non-deterministic
- broker-commission (Wave 2, 2026-02-27) — 11 computations extracted (sale/lease/commercial commission, broker-agent split, multi-tier distribution, MLS co-broke, EWT, VAT, net commission, finder's fee, rent-to-own); verified via 22+ sources; 2 CRITICAL CORRECTIONS: EWT rates superseded by RR 11-2018 (5%/10% at ₱3M, not 10%/15% at ₱720K); SMDC 4.75% UNVERIFIED; 8 BIR forms documented; finder's fee vs. commission legal distinction mapped
- condo-association-dues (Wave 2, 2026-02-27) — 7 computations extracted (monthly dues via ECR 001-17, sinking fund, special assessment allocation, delinquency penalty, assessment lien per RA 4726 §20, dues increase compliance check, tax status determination); verified via 22+ sources; 3 CRITICAL CORRECTIONS: RMC 65-2012 invalidated by SC (GR 215801) — dues exempt from IT/VAT/WT; TRAIN Law subsection is §109(1)(Y) not §109(1)(L); assessment lien priority overstated (only superior to subsequent liens); DHSUD 10% reserve fund floor UNVERIFIED
- existing-tools-survey (Wave 3, 2026-02-27) — 34 tools surveyed across 5 categories; mapped against 16 Wave 2 computations; 8 ZERO coverage, 3 POOR, 3 PARTIAL, 2 GOOD; ecosystem is "amortization monoculture" — regulatory compliance layer completely unserved
- practitioner-workflow (Wave 3, 2026-02-27, EXPANDED) — 8 computation workflows + full 6-stage developer sales lifecycle documented from 130+ sources; BP 220 compliance entirely manual; LGU assessment radically non-standardized; notarial fees non-deterministic; broker commission newly tooled (iRealtee Jan 2026); end-to-end closing has no single integrated tool. LIFECYCLE ADDITIONS: pre-sale sample computation (5-30 min/instance, high error rate, no multi-developer unified tool), equity-to-loan-takeout restructuring (10+ working days gating document at DMCI), Maceda refund (ZERO tools, very high error rate), closing cost aggregation (5+ fees, no single-pass tool), PDC schedule preparation as friction point, Pag-IBIG 20-30 day evaluation timeline, bank appraisal 3-15 day range, LOG 90-day validity window. Summary table mapping all 16 computations to lifecycle stages + error rates produced.
- complexity-scoring (Wave 3, 2026-02-27) — all 16 computations scored on 4 dimensions (1–5 scale each); composite ranking: assessment-level-lookup (17) leads; 7 heavy-infrastructure (≥14), 8 moderate (10–12), 1 light (maceda-refund at 6); LGU variability is dominant complexity driver; shared data layer opportunity identified across BIR zonal values, LGU assessment data, DHSUD JMC ceilings. Wave 3 COMPLETE.
- opportunity-scoring (Wave 4, 2026-02-27) — all 16 computations scored on 3 dimensions (A×F×M, 1–5 each, multiplicative composite max 125); TOP 5: assessment-level-lookup (100), socialized-housing-compliance (80), condo-association-dues (80), bp220-lot-compliance (75), improvement-depreciation (75); 3 tiers identified; 6 data layer clusters; 6 deep-dive loop recommendations produced; quick wins vs infrastructure plays strategy documented.
- catalog-draft (Wave 4, 2026-02-27) — Ranked opportunity catalog produced at output/opportunity-catalog.md; 16 entries with full inputs/outputs/legal basis/scoring; 3 tiers (5 high-opportunity, 5 medium, 6 lower); 6 shared data layers mapped; 6 deep-dive loop recommendations; 8 tax loop cross-references documented; ph-tax-computations-reverse catalog not yet produced (noted for future reconciliation).
- catalog-review (Wave 4, 2026-02-27) — Self-review PASSED: 16/16 completeness, 16/16 scoring consistency across all 3 dimensions, 16/16 arithmetic confirmed, 8/8 tax loop cross-references verified against now-available tax loop catalog. Catalog updated with reconciliation findings. ALL WAVES COMPLETE — LOOP CONVERGED.
