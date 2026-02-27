# Opportunity Catalog — Philippine Real Estate Computations (Non-Tax)

**Generated:** 2026-02-27
**Loop:** `loops/reverse-ph-realestate-calcs/`
**Scope:** Every deterministic computation in Philippine real estate outside taxation — financing, regulatory compliance, property valuation, fees, and government housing programs.
**Complementary loop:** `loops/reverse-ph-tax-computations/` (covers CGT, DST, VAT, CWT, RPT, transfer tax, withholding) — catalog produced 2026-02-26, cross-referenced below.

---

## How to Read This Catalog

Each entry contains:
- **What it computes** — inputs, outputs, and core logic
- **Legal basis** — RA, circular, or regulation with section numbers
- **Current state** — how practitioners do it today (manual, spreadsheet, partially automated)
- **Complexity estimate** — branching rules, lookup tables, external data dependencies (composite score /20)
- **Competitive gap** — what existing PH tools don't cover
- **Opportunity score** — `automation_gap × market_frequency × moat_defensibility` (each 1–5, composite max 125)
- **Tax loop cross-reference** — where this computation feeds into or depends on tax computations

**Scoring definitions:**
- **Automation gap (A):** 1 = well-served tool exists → 5 = zero tools, fully manual
- **Market frequency (F):** 1 = rare/niche → 5 = every real estate transaction
- **Moat defensibility (M):** 1 = trivial to replicate → 5 = requires LGU-level database + deep regulatory knowledge

---

## Ranked Opportunity Catalog

### Tier 1: High Opportunity (composite ≥ 75)

---

#### #1. Assessment Level Lookup — Composite: 100 (A:4 × F:5 × M:5)

**What it computes:**
- *Inputs:* Property classification (residential/commercial/industrial/agricultural per actual use), land FMV, building FMV (via BUCC × floor area − depreciation), machinery FMV, LGU-specific basic RPT rate (max 2% Metro Manila, 1% province), SEF rate (1%), idle land status
- *Outputs:* Assessment level per classification tier, assessed value (land + building + machinery), annual RPT (basic + SEF + idle land levy), payment penalties (2%/month, max 36 months) or advance discount (max 20%)
- *Core logic:* Graduated lookup across 4 sub-tables (land: 6 flat rates; building: 4 graduated sub-tables with 29 bracket values total; machinery: 4 flat rates; special classes: 5 reduced rates) per LGC Section 218. Total AV = sum of (FMV × assessment level) per component. RPT = AV × (basic rate + SEF 1% + idle land max 5%).

**Legal basis:** RA 7160 (Local Government Code) §§199, 217, 218, 233, 235, 236; DOF Local Assessment Regulations No. 1-92; RA 12001 (RPVARA, 2024) — preserves §218 maximums, adds 6% transition cap per LGU.

**Current state:** Poor tool coverage. TaxCalcPH and OwnPropertyAbroad apply simplified Metro Manila 2% / provincial 1% rates without full §218 bracket implementation. LGU assessor systems (RPTAS/eFAAS) exist internally but are not public-facing. ~60% of LGU Schedule of Market Values are outdated. Radically non-standardized across 1,488+ LGUs.

**Complexity:** 17/20 (highest of all 16). 12 branching rules, 15 lookup tables, 6 external dependencies. LGU-specific SMV/BUCC databases are the dominant data barrier.

**Competitive gap:** No tool implements the full LGC §218 assessment level table with all classification tiers, value brackets, and LGU-specific variations. No tool tracks RA 12001's 6% transition cap per LGU effectivity date.

**Moat:** Whoever builds the LGU data layer (SMV, BUCC schedules, RPT rates across 1,488+ jurisdictions) has a compounding advantage — each additional LGU increases the dataset's value for all users.

**Tax loop cross-reference:** Assessment level determines the RPT tax base. The "higher value rule" (MAX of GSP, BIR zonal, LGU FMV) also determines tax bases for CGT, DST, and transfer tax in the tax loop.

---

#### #2. Socialized Housing Compliance — Composite: 80 (A:5 × F:4 × M:4)

**What it computes:**
- *Inputs:* Selling price, floor area (sqm), building type (horizontal/vertical), number of floors, location (NCR/HUC/other), BIR zonal value, total project area, total project cost
- *Outputs:* Housing category (L1-A/L1-B/L2-Economic/L3-Low-cost/Medium/Open), compliance pass/fail against applicable ceiling, PhilGuarantee guarantee eligibility, balanced housing requirement compliance
- *Core logic:* 5 sub-computations: (1) 6-tier classification by selling price bracket per JMC 2024-001; (2) price ceiling check against JMC 2025-001 matrix (6 base ceilings by building type × height × floor area + zonal add-on for NCR/HUC condos ₱50K–₱200K); (3) government guarantee eligibility (PhilGuarantee ceilings: ₱4.9M low-cost, ₱6.6M medium); (4) balanced housing requirement (15% subdivision / 5% condo per RA 10884, 6 compliance modes); (5) ceiling currency check (3-year validity + 2-year review constraint). Lot-only sub-rule: ceiling = 40% of house-and-lot ceiling.

**Legal basis:** DHSUD-DEPDev JMC 2025-001; DHSUD-NEDA JMC 2024-001; RA 7279 (UDHA); RA 10884 (Balanced Housing); RA 11201 (DHSUD Act); RA 11439 (PhilGuarantee).

**Current state:** Zero tools. Developers and DHSUD staff cross-reference JMC tables manually. No automated compliance checker validates per-unit and per-sqm limits by housing type, zonal add-ons, or balanced housing modes.

**Complexity:** 11/20. 12 branching rules but only 2–3 lookup tables and 2 external dependencies (BIR zonal values, JMC ceiling updates every 2–3 years).

**Competitive gap:** Socialized housing is the largest market segment by unit volume. Zero tools despite being mandatory for every socialized/economic housing project. Also relevant for BOI incentive applications and PhilGuarantee eligibility.

**Moat:** Requires JMC ceiling database integration, BIR zonal value cross-reference, 6-tier housing classification, and 6 balanced housing compliance modes (per RA 10884). PIC/IC compliance modes lack clear statutory basis per CREBA — deep regulatory knowledge required.

**Tax loop cross-reference:** Socialized housing (≤₱2M per RA 7279) is VAT-exempt under NIRC §109(P). Housing classification feeds into CGT/DST base determination for subsidized transactions.

---

#### #3. Condo Association Dues — Composite: 80 (A:5 × F:4 × M:4)

**What it computes:**
- *Inputs:* Board-approved annual budget, contingency rate (10% members / 20% beneficial users per ECR 001-17 §8), unit floor area (sqm), total gross area, sinking fund rate (flat per-sqm or % of dues), special assessment amount, delinquency interest rate (12% p.a. max per ECR §8.5), overdue months, current vs. proposed dues rate
- *Outputs:* Monthly dues per unit, sinking fund contribution, special assessment allocation, delinquency penalty amount, assessment lien amount (RA 4726 §20), dues increase compliance status, tax treatment determination
- *Core logic:* Monthly rate = (annual_budget × contingency_multiplier) / gross_area / 12; dues = unit_sqm × monthly_rate. Sinking fund: ₱4–₱15/sqm or 5–10% of dues. Special assessment: pro-rata by undivided interest %. Delinquency: principal × (rate/12) × months. Assessment lien: accumulation per RA 4726 §20, priority only over liens registered after assessment notice. Dues increase ≥10% requires membership vote per RA 9904 IRR.

**Legal basis:** RA 4726 §§9(d), 20; HLURB ECR 001-17 §8; RA 9904 IRR; *BIR v. First E-Bank Tower Condominium Corp.* (GR 215801, Jan 15, 2020); NIRC §109(1)(Y) per TRAIN Law.

**Current state:** Zero tools. Condo corporations use internal spreadsheets with no standardization. SC GR 215801 tax treatment (dues exempt from IT/VAT/WT) still widely misapplied — many condo corps still withhold taxes per the invalidated RMC 65-2012.

**Complexity:** 15/20. 11 branching rules, 5 lookup tables, 5 external dependencies (board budget, master deed, by-laws, DHSUD guidance, BIR tax treatment). Annual budget cycles drive update frequency.

**Competitive gap:** No tool computes monthly dues via ECR 001-17 formula. No sinking fund calculator. No delinquency penalty computation. No assessment lien tracker. Growing market — hundreds of thousands of condo units in Metro Manila with rapid vertical development.

**Moat:** Per-condo-corp budget data requirement, multi-regulation interaction (RA 4726, RA 9904, ECR 001-17, TRAIN Law, SC rulings), ECR contingency buffer engine, and SC GR 215801 tax treatment create significant regulatory depth.

**Tax loop cross-reference:** SC GR 215801 invalidated RMC 65-2012 — association dues are exempt from income tax, VAT, and withholding tax. Only commercial income (parking rentals, function hall fees) is subject to VAT with separate accounting required. TRAIN Law §109(1)(Y) codifies the exemption.

---

#### #4. BP 220 Lot Compliance — Composite: 75 (A:5 × F:3 × M:5)

**What it computes:**
- *Inputs:* Housing type (single detached/duplex/row house/multi-family), classification (socialized/economic), lot area, lot frontage, floor area, project density (lots/ha), number of stories, total project area, selling price
- *Outputs:* Pass/fail for each of 12+ compliance checks, required vs. actual values, shortfalls, overall project compliance status
- *Core logic:* 12-step deterministic decision tree: (1) project classification → (2) lot area check (Table 7: 6 minimums) → (3) frontage check (Table 8: 12 minimums) → (4) floor area check (18/22 sqm base + JMC layering to 24 sqm) → (5) open space (Table 1: density-based 3.5%–9%+ with +1%/10 units formula) → (6) community facility (Table 3: 3 density brackets) → (7) road ROW (Table 5: 6×6 matrix) → (8) setback (1.5/1.5/2.0m single; 2.0m+0.3m/storey multi) → (9) building separation (4m/6m/10m by height) → (10) parking (1:8 ratio) → (11) row house limits (20 units, 100m) → (12) house-to-lot price ratio (40% lot maximum). Plus 10 additional checks identified: firewall, drainage type, road pavement, block length, completion level, tree planting, elevator, fire suppression, roof eave clearance, water supply.

**Legal basis:** BP 220 (1982); HLURB Resolution R-824 (2008 Revised IRR); DHSUD JMC 2025-001 (ceiling integration); National Building Code for >12 storey buildings.

**Current state:** Zero tools. Entirely manual — architects cross-reference IRR tables against CAD plans, DHSUD examiners do manual document review. 30–60 min per compliance check with medium error rate. No automated compliance-check tool exists anywhere.

**Complexity:** 14/20. Deepest branching of all 16 computations (15 decision points), 6 lookup tables, but only 2 external dependencies (JMC ceilings, NBC for tall buildings) and medium update frequency (IRR stable since 2008).

**Competitive gap:** No tool automates any of the 12+ compliance checks. Multi-regulation interaction (BP 220 IRR + JMC 2025-001 + NBC) and JMC floor area layering (18→32→28→24 sqm across different issuances) are very hard to replicate correctly.

**Moat:** Deep regulatory knowledge required — pre-2008 vs. post-2008 value distinctions, VIZCODE legacy, JMC layering across issuance vintages, and ongoing DHSUD TWG review (DO 2024-020). Very hard to replicate correctly.

**Tax loop cross-reference:** BP 220 compliance is prerequisite for DHSUD Certificate of Registration and License to Sell. Socialized housing classification (confirmed by BP 220 compliance) triggers VAT exemption under NIRC §109(P).

---

#### #5. Improvement Depreciation — Composite: 75 (A:5 × F:3 × M:5)

**What it computes:**
- *Inputs:* Floor area (sqm), construction type (RC/steel/mixed/wood with A–D sub-types), BUCC rate (per LGU), adjustment factors, building age, maintenance degree (good/fair/poor), economic life (assessor judgment: RC 50–60yr, mixed 25–35yr, wood 20–25yr), LGU depreciation table
- *Outputs:* Replacement Cost New (RCN), percent good, depreciation rate, building FMV, machinery FMV (separate computation with 20% residual floor)
- *Core logic:* RCN = floor_area × BUCC_rate × adjustment_factors. Depreciation via age-life method: rate = effective_age / economic_life; or LGU table method: lookup(construction_type, age, maintenance_degree) → percent_good. Building FMV = RCN × percent_good. Machinery: straight-line with 20% minimum residual value (statutory per LGC §225).

**Legal basis:** DOF LAR 1-92 §§40–41 (buildings); LGC §§224–225 (machinery); PD 1096 (NBC construction types); RA 12001 (RPVARA — requires Philippine Valuation Standards-aligned methodology).

**Current state:** Zero tools. Part of LGU assessor internal workflow (RPTAS/eFAAS for those LGUs that have digitized). Property owners cannot independently verify assessor computations. Per-LGU BUCC rates and depreciation tables are not centrally published.

**Complexity:** 14/20. 8 branching rules, 8+ lookup tables (all LGU-specific), 5 external dependencies (BUCC schedule, LGU depreciation table, adjustment factors, DPWH data, RA 12001 PVS). Critical: assessor numbering is INVERTED from PD 1096 (Type I = RC in assessor practice, but wood in NBC).

**Competitive gap:** No PH-specific depreciation tool exists. Generic depreciation calculators lack PH assessor parameters (construction type classification, BUCC rates, LGU-specific tables). Primarily serves government assessors — may need to target LGU modernization market.

**Moat:** Shares the LGU data moat with assessment-level-lookup. Per-LGU BUCC rates, per-LGU depreciation tables, dual classification systems, and RA 12001's 3-year BUCC revision mandate create deep data acquisition barriers.

**Tax loop cross-reference:** Building FMV (output of depreciation) feeds directly into assessed value computation, which determines RPT base. DPWH construction cost data integration relevant for BIR zonal value methodology.

---

### Tier 2: Medium Opportunity (composite 45–60)

---

#### #6. Developer Equity Schedule — Composite: 60 (A:4 × F:5 × M:3)

**What it computes:**
- *Inputs:* List price, other charges % (by developer: Ayala 7.5%, SMDC 6–8%, DMCI varies), VAT applicability (threshold ₱3.6M per RR 1-2024), DP percentage (10–35%), reservation fee, payment term (months), spot cash discount schedule (per developer), in-house financing rate
- *Outputs:* Total Contract Price (TCP = list + charges + VAT), monthly equity installment ((TCP × DP% − RF) / months), net spot cash price (TCP × (1 − discount)), turnover balance (TCP − equity paid − RF, 3 discount-application variants), late payment penalty (simple or DMCI escalating at 3%/month)
- *Core logic:* 8 sub-computations covering full developer payment lifecycle. TCP composition varies by developer (SMDC model: LP + miscellaneous + move-in + VAT). Spot cash discount: Avida 7–9%, ALP 15–17%, SMDC 10–32%, DMCI 10–16% + 2% PDC bonus. Late penalty: 2%/month (Avida), 3%/month (SMDC/DMCI), DMCI progressive tiers up to 36%/year.

**Legal basis:** PD 957 (Subdivision and Condominium Buyers' Protective Decree); RA 6552 (Maceda Law — triggers at 2+ years); BIR RR 1-2024 (VAT threshold ₱3.6M).

**Current state:** Poor coverage. No tool handles full developer equity computation. Practitioners use developer-provided sample computation sheets (PDF/Excel) or custom broker spreadsheets. 5–30 min per instance with high error rate. Breighton Land case: 49 compensation plan variations automated by Visdum with 6× improvement.

**Complexity:** 14/20. 8 branching rules, 4 lookup tables (per-developer), 4 external dependencies (discount rates, financing rates, charges %, association dues), high update frequency (project-specific, promotional).

**Competitive gap:** Highest-frequency unserved computation — sample computation generated for every buyer interaction at pre-selling stage. No multi-developer unified tool. Key differentiator: unified interface across Ayala Land, SMDC, DMCI, Megaworld.

**Moat:** Moderate. Requires per-developer/per-project data (discount tables, penalty models, charge percentages). Data is accessible from published terms but fragmented across developers × projects.

**Tax loop cross-reference:** VAT computation (12% on TCP above ₱3.6M) is tax-loop territory. Developer equity schedule determines the base for VAT inclusion. TCP composition feeds into CGT/DST base via the "higher value rule."

---

#### #7. Rent Increase Computation — Composite: 60 (A:5 × F:4 × M:3)

**What it computes:**
- *Inputs:* Unit type (residential), current monthly rent, location (NCR/HUC/other), lessee tenure continuity, lease start date, vacancy status, deposit amount, prevailing savings rate
- *Outputs:* Coverage determination (7-step decision tree), maximum allowable increase percentage, new rent ceiling, deposit interest due to lessee, compliance status
- *Core logic:* 6 sub-computations: (1) coverage determination (residential, ≤₱10K NCR/HUC or ≤₱5K other); (2) allowable increase = current_rent × (1 + cap_pct) where cap_pct from annual NHSB resolution lookup; (3) first-year freeze check; (4) advance rent/deposit compliance (max 1 month advance, 2 months deposit); (5) deposit interest return (prevailing savings rate); (6) multi-year rent projection. Historical cap rates: 7% (2010–2013), 2%/7%/11% three-tier (2018–2020), 4% (2024), 2.3% (2025), 1% (2026).

**Legal basis:** RA 9653 (Rent Control Act of 2009); NHSB Resolutions (annual cap rate setting, 2010–2026); HUDCC Resolution 01-2017 (2018–2020 three-tier rates).

**Current state:** Zero tools. No rent increase calculator for RA 9653 / NHSB annual caps despite 16+ years of active enforcement. Practitioners manually apply the announced percentage. Millions of rental units in Metro Manila alone.

**Complexity:** 11/20. 6 branching rules, 2 lookup tables (cap rate history, HUC list), 2 external dependencies (annual NHSB resolution, savings rate). Low build complexity.

**Competitive gap:** Zero tools for 16+ years of an actively enforced law. No tool checks coverage eligibility (rent bracket test, same-tenant rule, HUC determination). NHSB historical rate table (2010–2026, 10 resolution periods) not compiled in any accessible tool.

**Moat:** Moderate. Requires compiling NHSB resolution history with the 2018–2020 three-tier correction, 7-step coverage decision tree, HUC classification, and vacancy reset + 12-month freeze interaction. Not trivial to get right despite simple formula.

**Tax loop cross-reference:** Rental income is subject to income tax (graduated rates or 8% flat for sub-₱3M). Withholding tax on rent (5% CWT) applies per RR 2-98. Lease commission computation (this loop) and lease income taxation (tax loop) are complementary.

---

#### #8. Notarial Fees — Composite: 50 (A:5 × F:5 × M:2)

**What it computes:**
- *Inputs:* Page count, mortgage amount (for foreclosure), transaction value, document type (DOAS/REM/CTS/SPA), notary annual income, IBP chapter
- *Outputs:* Notarial act fee (per-page ceiling), foreclosure fee, IBP-based fee estimate, market heuristic range
- *Core logic:* 5 sub-computations of varying determinism: (1) OCA per-page ceiling: ₱200 first page + ₱50/additional (trivially deterministic); (2) notarial foreclosure fee: 5% of first ₱4K + 2.5% of excess, cap ₱100K (fully deterministic); (3) IBP chapter-based fee estimation (deterministic given chapter table); (4) market heuristic 1–2% of transaction value (non-deterministic); (5) unattributed tiered table ₱300–₱5K (mechanically deterministic but NO verified regulatory basis).

**Legal basis:** A.M. No. 02-8-13-SC (2004 Rules on Notarial Practice); OCA Circular 73-2014 (₱200/₱50 ceiling); Rule 141 §9(1)(e) (foreclosure fee). CRITICAL: A.M. No. 19-08-15-SC cited in some sources is actually the 2019 Rules on Evidence — contains zero provisions about notarial fees.

**Current state:** Zero tools. Practitioners receive a quote from the notary and negotiate. The computation is most valuable for foreclosure proceedings (formula-based), fee verification, and closing cost estimation.

**Complexity:** 12/20. 7 branching rules, 4 tables, 4 external dependencies (IBP chapter schedules, notary income, document complexity, SC amendments). But stable — OCA ceiling unchanged since 2014.

**Competitive gap:** Zero tools, every-transaction frequency. However, limited by partial non-determinism — only 2 of 5 sub-computations are fully automatable. Best positioned as a closing cost aggregation component, not standalone.

**Moat:** Low. Deterministic portions are trivial (OCA ceiling = 2 numbers; foreclosure fee = 1 formula). IBP chapter variation adds locality-specific data but tables are accessible.

**Tax loop cross-reference:** Notarial fees are a deductible expense for sellers. VAT applies to notarial services if notary's annual gross exceeds ₱3M.

---

#### #9. Pag-IBIG Amortization — Composite: 45 (A:3 × F:5 × M:3)

**What it computes:**
- *Inputs:* Approved loan amount, annual interest rate (5.75%–9.75% by repricing period under FRBP, or fixed for AHP), loan term (years), borrower age (for MRI), improvements value (for FGI/FAPI), repricing period choice
- *Outputs:* Monthly payment (principal + interest + MRI + FGI/FAPI), full amortization schedule (declining balance), total interest paid, total insurance cost, repricing schedule
- *Core logic:* Standard formula M = P × [r(1+r)^n] / [(1+r)^n − 1] (confirmed exact match with OmniCalculator). MRI premium: CONFLICT — official circulars state "uniform premium rate" but practitioner guides cite age-bracketed table (₱0.42–₱5.54 per ₱1,000); claimed source Circular 428 is actually about foreclosed property sales. FGI/FAPI rate: 0.076% cited but last documented rate is 0.1686% (Manila Bulletin 2018). Payment priority: MRI → FGI → interest → principal → penalty.

**Legal basis:** HDMF Circular 403 (amortization schedule rules); Circular 443/amendments (FRBP rate structure); RA 7394 (Consumer Act — no prepayment penalty).

**Current state:** Partial coverage. 5+ tools compute basic Pag-IBIG amortization (official calculator, OmniCalculator, PagibigCalculator.com). However, NO tool computes MRI/FGI premium breakdown separately — practitioners can't see insurance cost impact on total payment.

**Complexity:** 10/20. 4 branching rules, 3 lookup tables, 3 external dependencies (interest rates, MRI premium rate, FGI rate). Moderate — main risk is stale insurance rate data (last public data 2014–2018).

**Competitive gap:** Key differentiator over existing tools: MRI/FGI line-item breakdown. Insurance transparency is the unserved niche. Repricing mechanics (borrower chooses new period) also not modeled in any existing tool.

**Moat:** Moderate. MRI/FGI premium rates not publicly documented since 2014–2018 — whoever obtains current rates has data advantage. Insurance computation adds non-trivial complexity beyond standard amortization.

**Tax loop cross-reference:** MRI/FGI premiums may be deductible as insurance expense. Pag-IBIG interest payments are potentially deductible (subject to BIR rules for housing loan interest deduction).

---

#### #10. Broker Commission — Composite: 45 (A:3 × F:5 × M:3)

**What it computes:**
- *Inputs:* Transaction type (sale/lease), property value, contractual commission rate (3–5% sale, 1 month/year residential lease, 3–6% commercial lease), split arrangement (50/50, 60/40, 80/20), broker annual gross income, EWT sworn declaration status
- *Outputs:* Gross commission, broker-agent split amounts, multi-tier distribution (firm/agent/unit mgr/div mgr), EWT withholding (5% or 10% at ₱3M threshold per RR 11-2018), VAT (12% if >₱3M annual), net commission after all deductions
- *Core logic:* 11 sub-computations: sale/lease/commercial commission, split, multi-tier distribution (iRealtee model: 20% firm retention, then 60/15/10), MLS co-broke (50/50 per CEREBMLS), EWT, VAT, net commission, finder's fee (1–2%), rent-to-own conversion. CRITICAL: EWT rates were updated by RR 11-2018 / TRAIN Law to 5% (≤₱3M) / 10% (>₱3M) for individuals — supersedes the pre-TRAIN 10%/15% at ₱720K still cited by many sources.

**Legal basis:** RA 9646 (RESA); Civil Code Art. 1306 (freedom of contract); RR 11-2018 (EWT, post-TRAIN); RA 10963 (TRAIN Law); NIRC §§105–109 (VAT).

**Current state:** Partial coverage. iRealtee (launched Jan 2026) has multi-tier split + EWT deduction — best coverage found. But SaaS-locked (not standalone). Clevrr and Housal compute flat commission only. iRealtee may still use pre-TRAIN EWT rates (shows 10%/15% at ₱3M, vs. verified 5%/10%).

**Complexity:** 15/20. 10 branching rules, 5 lookup tables, 4 external dependencies (contractual rate, gross income, sworn declaration, market conventions). Annual update driven by market shifts and sworn declaration cycle.

**Competitive gap:** Open-access standalone commission calculator with correct post-TRAIN EWT rates. MLS co-broke splits, lease commission, rent-to-own conversion, and 8% flat tax option for sub-₱3M brokers not covered by any tool.

**Moat:** Moderate. Multi-tier split engine, EWT/VAT computation with annual declaration tracking, and BIR form integration (8 forms documented) create moderate data maintenance requirements.

**Tax loop cross-reference:** EWT (5%/10%) and VAT (12%) on commission are tax computations. BIR Forms 2307, 1601-EQ, 2550M/Q, 2551Q, 1701, 1701Q documented. 8% flat tax option for sub-₱3M brokers is a tax-loop decision.

---

### Tier 3: Lower Opportunity (composite ≤ 32)

---

#### #11. LTV Ratio — Composite: 32 (A:4 × F:4 × M:2)

**What it computes:**
- *Inputs:* Appraised value, selling price, property type (condo/house-and-lot/lot-only), lender type (Pag-IBIG/bank), loan program (retail/buyback/AHP), loan amount range
- *Outputs:* Collateral value (min of appraised and selling), applicable LTV cap, maximum loanable amount, required equity/down payment
- *Core logic:* Collateral_value = min(appraised, selling_price). Max_loan = LTV_cap × collateral_value. LTV caps: Pag-IBIG retail 100%/90%/80% by loan range, buyback 100%/100%/95%/90%; banks 80–90% in practice (no hard BSP regulatory cap — Circular 855's 60% is classification measure, not lending limit). AHP socialized: 100%.

**Legal basis:** RA 8791 (General Banking Act) §37; BSP Circular 855 (collateral valuation); BSP Circular 1087; Pag-IBIG Circulars 402/473.

**Current state:** Poor coverage. Generic LTV calculators (Bankrate) exist but none encode BSP circular logic, Pag-IBIG tiered LTV caps, or appraisal-basis rules. Banks compute internally.

**Complexity:** 10/20. 6 branching rules, 5 lookup tables, 2 external dependencies. Stable policies (Pag-IBIG tiers unchanged since 2014).

**Competitive gap:** Sub-computation within loan eligibility — not typically standalone. Best built as module within integrated loan comparison engine.

**Tax loop cross-reference:** Minimal direct tax connection. LTV determines loan amount, which affects DST on mortgage (tax loop).

---

#### #12. Bank Mortgage Amortization — Composite: 30 (A:2 × F:5 × M:3)

**What it computes:**
- *Inputs:* Principal (after down payment), annual interest rate, loan term, repricing period, benchmark rate at repricing, bank spread, early termination trigger
- *Outputs:* Monthly amortization (P+I), full schedule, repriced payment after rate change, effective interest rate (EIR per BSP Circular 730), early termination fee estimate
- *Core logic:* Standard declining balance: M = P × [r(1+r)^n] / [(1+r)^n − 1]. Repricing: new_rate = benchmark + spread; recompute M on remaining balance/term. Add-on interest prohibited by BSP Circular 730. Early termination: processing fee (₱3,500–₱5,000) + clawback of waived fees (varies by bank). Capacity check: monthly amortization ≤ 30–40% gross income (bank-specific, NOT BSP-mandated).

**Legal basis:** BSP Circular 730 (add-on prohibition, EIR disclosure); RA 3765 (Truth in Lending Act); RA 7394 (Consumer Act — prepayment rights).

**Current state:** Good coverage for basic computation — 11+ tools. Every major PH bank has its own calculator. BSP Calculator offers 5 amortization modes. However, every bank calculator is siloed. No tool handles variable rate repricing scenario modeling, multi-bank comparison, or early termination penalty formulas.

**Complexity:** 14/20. High update frequency (daily benchmark rates, quarterly bank rate changes, monthly promos) but algorithmically straightforward.

**Competitive gap:** Multi-bank comparison + repricing scenario modeling is the unserved niche. Build as enhancement to existing coverage, not greenfield.

**Tax loop cross-reference:** Housing loan interest may be deductible (subject to BIR rules). DST on mortgage document (tax loop).

---

#### #13. Maceda Law Refund — Composite: 30 (A:5 × F:3 × M:2)

**What it computes:**
- *Inputs:* Property type (real property on installment), financing mode (must be developer-financed, not bank), total payments made (includes DP/deposits, excludes penalty interest), monthly amortization amount, contract duration, notarized notice status, CSV payment status
- *Outputs:* Coverage determination (yes/no), applicable section (3 or 4), grace period (Section 3: 1 month per year paid, once per 5-year window), cash surrender value (Section 3: 50% of total payments + 5%/year after year 5, max 90%), cancellation validity (dual conditions: notarized notice AND CSV payment)
- *Core logic:* 6 sub-computations. Key formula: years_paid = total_payments ÷ lowest_monthly_amortization (value-based per *Orbe v. Filinvest*, NOT payment count). If years_paid ≥ 2: CSV = total_payments × (50% + 5% × max(0, years_paid − 5)), capped at 90%. Grace = floor(years_paid) months, once per 5-year window. If years_paid < 2: 60-day grace, no refund.

**Legal basis:** RA 6552 (Maceda Law, 1972); *Orbe v. Filinvest* (G.R. 208185, 2017 — years as value-based divisor); *Active Realty v. Daroya* (G.R. 141205 — dual cancellation conditions); *Rillo v. CA* — <2yr = no refund.

**Current state:** Zero tools. Despite being >50 years old, no calculator computes CSV or grace period. Practitioners compute manually from payment records. Error rate "very high" per workflow analysis — disputes on "total payments" definition and years-counting methodology.

**Complexity:** 6/20 (lowest of all 16). 6 branching rules, 1 lookup table (CSV % by years — 13 rows), 1 external dependency (payment history). Near-pure statutory. Unchanged since 1972.

**Competitive gap:** Zero tools, very high error rate. Trivial to build — the simplest computation with the largest coverage gap. "Highest impact per line of code."

**Moat:** Low. Core formula is straightforward. SC rulings add edge case depth but the formula itself is easily replicated. Value is in correctness (SC ruling compliance) rather than data barriers.

**Tax loop cross-reference:** Maceda refund/CSV may trigger tax events — treatment of returned payments for income tax purposes. Cancellation of contract may affect CGT computation on the developer side.

---

#### #14. Pag-IBIG Loan Eligibility — Composite: 20 (A:2 × F:5 × M:2)

**What it computes:**
- *Inputs:* Membership status, contribution months (24 minimum, lump-sum OK), age, loan history (no existing outstanding housing loan), creditworthiness, property type, co-borrower details, monthly gross income
- *Outputs:* Eligible (yes/no with rejection reason), maximum approved loan amount (min of: program cap, contribution entitlement, LTV × collateral, capacity-based limit), applicable interest rate tier, applicable program (EUF ≤₱6M, Expanded ≤₱15M, AHP)
- *Core logic:* 7-step sequential gate: membership → contributions → age (≤65 maturity, ≤70 special) → loan history → credit → property → co-borrowers → loan amount. Capacity: amortization ≤ 35% GMI. LTV: retail 100%/90%/80%, buyback varies.

**Legal basis:** HDMF Circulars 443, 402, 473; RA 9679 (Pag-IBIG Fund Law); Circular 396 (co-borrower rules).

**Current state:** Good coverage. Official Pag-IBIG Affordability Calculator covers core eligibility. OmniCalculator and PagibigCalculator.com provide alternatives. Edge cases (loan-on-top-of-loan, non-relative co-borrowing per Circular 396) not exposed.

**Complexity:** 12/20. 7 branching rules, 4 tables, 3 dependencies. Well-documented in circulars.

**Competitive gap:** Official tool exists. Value only in edge case coverage and integration with broader loan comparison engine.

**Moat:** Low. Decision tree well-documented. Contribution-to-loan table gap for ₱3M–₱6M is the only data advantage.

**Tax loop cross-reference:** Pag-IBIG contributions are tax-deductible (up to ₱200/month employee share). Housing loan interest potentially deductible.

---

#### #15. ROD Registration Fees — Composite: 20 (A:2 × F:5 × M:2)

**What it computes:**
- *Inputs:* Property value (MAX of GSP, BIR zonal, LGU FMV), mortgage amount (for annotation), document type, number of titles
- *Outputs:* Registration fee (17-tier table for ≤₱1.7M; formula ₱8,796 + CEIL((value−₱1.7M)/₱20K) × ₱90 for >₱1.7M), additional charges (entry ₱50, owner's duplicate ₱330, CTC ₱150+₱20/pg, LRF 1%, IT ₱20–₱100, assurance fund 0.25%), mortgage annotation fee (3-tier percentage), other annotation fees (7 types)
- *Core logic:* Two-tier registration fee computation + 6 additional charge components + tiered mortgage annotation formula (₱500+0.5% up to ₱100K; ₱1K+0.3% ₱100K–₱500K; ₱2K+0.2% over ₱500K) + ₱200/title. Release = half of annotation fee.

**Legal basis:** PD 1529 §117; LRA Circular 61 (1993), Circular 11-2002, Circular 13-2016 (operative fee schedule).

**Current state:** Good coverage. Official LRA ERCF tool is authoritative. ForeclosurePH has a registration fee calculator. Gaps: annotation fees (separate schedules), total title transfer cost pipeline, 25% late filing surcharge.

**Complexity:** 12/20. 9 fee components, 4 tables. Stable — last comprehensive revision was 2002; updates rare.

**Competitive gap:** Minimal — official tool exists. Value as component of closing cost aggregation pipeline, not standalone.

**Moat:** Low. National fee table, well-documented. Two-tier formula is straightforward.

**Tax loop cross-reference:** The "higher value rule" (MAX of GSP, BIR zonal, LGU FMV) used for registration fee base is the same rule that determines CGT, DST, and transfer tax bases. Registration fee is a cost of transfer, not a tax, but often confused with taxes by practitioners.

---

#### #16. Condo Common Area Percentage — Composite: 20 (A:5 × F:2 × M:2)

**What it computes:**
- *Inputs:* Total units, unit floor area (sqm), total sellable area (sqm), allocation method (equal shares or floor-area proportional per master deed), parking CCT status (separate or included)
- *Outputs:* Undivided interest percentage per unit, common area RPT share, voting weight per RA 7899, dissolution proceeds share
- *Core logic:* Default (RA 4726 §6(c)): equal shares = 1/total_units. Industry de facto: interest_pct = unit_sqm / total_sellable_sqm × 100 (must be stated in master deed to override default). Parking CCT correction: if parking slots have separate titles, their area is included in total sellable area denominator.

**Legal basis:** RA 4726 §§6(c), 9(d), 20; RA 7899 (voting power — applies only to §4 and §16 matters); Civil Code Arts. 485, 490.

**Current state:** Zero tools. No tool computes undivided interest. Formula is straightforward but project-specific (depends on master deed parameters).

**Complexity:** 10/20. 8 branching rules (across 6 sub-computations), 3 tables, 3 dependencies. Low update frequency (master deed set at inception).

**Competitive gap:** Zero tools but very low market frequency — computed once per condo project at master deed creation.

**Moat:** Low. Core formula is straightforward. Method depends on master deed — project-specific input, not regulatory complexity.

**Tax loop cross-reference:** Common area RPT allocation affects individual unit owner tax burden. Undivided interest percentage determines pro-rata share of common area taxes.

---

## Strategic Analysis

### Three Build Strategies

| Strategy | Target Computations | Build Effort | Time to Value | Data Moat |
|----------|-------------------|-------------|--------------|-----------|
| **Quick Wins** | Maceda refund (#13), Rent increase (#7), Condo common area (#16) | Low | Weeks | Low |
| **High-Frequency Engines** | Developer equity (#6), Broker commission (#10), Pag-IBIG amortization (#9) | Medium | 1–2 months | Medium |
| **Infrastructure Plays** | Assessment level (#1) + Depreciation (#5), Socialized housing (#2) + BP 220 (#4), Condo dues (#3) | High | 3–6 months | Very high |

### Shared Data Layer Opportunities

Six data layers serve multiple computations. Building these once creates bundle economics:

| Data Layer | Computations Served | Total Composite Points |
|-----------|---------------------|----------------------|
| LGU assessment database (SMV, BUCC, RPT rates) | #1 assessment-level-lookup, #5 improvement-depreciation | 175 |
| BIR zonal values | #1 assessment-level, #2 socialized-housing, #15 rod-registration + tax loop (CGT, DST, transfer tax) | 200+ (cross-loop) |
| DHSUD JMC ceilings | #2 socialized-housing, #4 bp220-lot, #14 pagibig-eligibility | 175 |
| Developer payment terms | #6 developer-equity, #13 maceda-refund | 90 |
| NHSB resolutions | #7 rent-increase | 60 |
| EWT/VAT thresholds | #10 broker-commission, #3 condo-dues, #8 notarial-fees + tax loop | 175+ (cross-loop) |

**BIR zonal values are the highest-leverage shared data asset** — they serve computations in both this loop and the tax computations loop, with a combined composite score exceeding 200 points.

### Recommended Deep-Dive Loops

Based on scoring, the following computations warrant dedicated reverse loops for full specification:

| Priority | Loop Name | Computations Bundled | Composite Sum | Rationale |
|----------|----------|---------------------|---------------|-----------|
| 1 | PH Property Assessment Engine | assessment-level-lookup + improvement-depreciation | 175 | Shared LGU data layer. Highest single composite (100). RA 12001 regulatory tailwind. |
| 2 | DHSUD Compliance Engine | socialized-housing-compliance + bp220-lot-compliance | 155 | Shared JMC/ceiling data. Mandatory compliance with zero tools. |
| 3 | Condo Management Computation | condo-association-dues + condo-common-area-pct | 100 | Growing vertical market. SC GR 215801 creates regulatory complexity. |
| 4 | Developer Payment Engine | developer-equity-schedule | 60 | Highest frequency. Every buyer interaction. Multi-developer unification. |
| 5 | Rent Control Compliance | rent-increase-computation | 60 | Quick build. Millions of rental units. 16+ years of zero tools. |
| 6 | Maceda Law Calculator | maceda-refund | 30 | Simplest build. Highest impact per line of code. Zero tools despite 50+ year statute. |

### Ecosystem Gaps Summary

```
Coverage:  ████████████████░░░░░░░░░░░░░░░░  8 of 16 = ZERO tools
           ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  3 of 16 = POOR
           ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  3 of 16 = PARTIAL
           ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  2 of 16 = GOOD

Pattern:   "Amortization monoculture" — 11+ tools compute basic
           mortgage amortization. Regulatory compliance layer
           is completely unserved.

Key stat:  EVERY high-moat computation is also underserved.
           No "defended but covered" quadrant exists.
           This is a wide-open market.
```

### Cross-Reference: Tax Computations Loop

The `loops/reverse-ph-tax-computations/` loop covers 12 tax computations (CGT, DST, VAT, CWT, RPT, transfer tax, EWT, etc.). Its opportunity catalog was produced 2026-02-26 and has been cross-referenced in the catalog-review self-review. Key bridge points:

| This Loop's Computation | Tax Loop Entry (Score) | Bridge | Shared Data |
|------------------------|----------------------|--------|-------------|
| assessment-level-lookup (100) | RPT Computation (125) | Assessment level IS the RPT tax base. This loop covers §218 lookup; tax loop covers rate application + SEF + penalty. | LGU assessment database (SMV, BUCC, RPT rates) |
| rod-registration-fees (20) | Highest-of-Three Base (40), CGT (45), Transfer Tax (60) | "Higher value rule" max(GSP, ZV, AFMV) is shared tax base | BIR zonal values |
| broker-commission (45) | CWT Rate and Timing (60) | EWT on commission (individual brokers 5%/10% per RR 11-2018; sellers habitually engaged 1.5/3/5/6%) | EWT/VAT thresholds |
| condo-association-dues (80) | N/A — SC settled as exempt | SC GR 215801 invalidated RMC 65-2012; TRAIN §109(1)(Y) | BIR tax treatment |
| socialized-housing-compliance (80) | VAT on Real Property (64) | Socialized housing exemption is a VAT decision gate | Housing classification |
| developer-equity-schedule (60) | VAT on Real Property (64) | VAT on TCP above ₱3.6M threshold (RR 1-2024) | VAT threshold |
| notarial-fees (50) | VAT on Real Property (64) | VAT on notarial services if notary gross >₱3M | VAT threshold |
| rent-increase-computation (60) | CWT Rate and Timing (60) | CWT 5% on rental income | Withholding rates |

**Cross-loop reconciliation findings (catalog-review, 2026-02-27):**
- All 8 bridge points verified against tax loop catalog — confirmed accurate
- **BIR zonal values** are the highest-leverage shared data asset: 200+ composite points in this loop + 125 (ZV lookup #1 in tax loop) = **325+ combined**
- **LGU assessment database** is the second-highest: 175 in this loop + 185 in tax loop (RPT 125 + Transfer Tax 60) = **360+ combined**
- Assessment-level-lookup (this loop) and RPT Computation (tax loop) have a clean scope boundary: valuation vs. taxation. A deep-dive loop should coordinate both scopes.

---

## Methodology

- **16 computations** surveyed across financing (6), regulatory compliance (5), valuation/assessment (2), and fees/dues (3)
- **Wave 1** (source acquisition): 10 primary legal sources fetched and processed
- **Wave 2** (computation extraction): Each computation independently verified against 8–25+ sources via subagent cross-checking; 3+ critical corrections per computation on average
- **Wave 3** (competitive analysis): 50+ tools surveyed; 16 practitioner workflows documented from 130+ sources; 4-dimensional complexity scoring
- **Wave 4** (scoring): Three-dimensional multiplicative scoring (A×F×M), composite range 1–125
- **Scoring calibration**: Relative within the set of 16, not absolute. Multiplicative formula intentionally penalizes weakness on any single dimension.
- **Deterministic status**: 14 of 16 fully deterministic; 2 partially (notarial-fees, condo-common-area-pct method-dependent)
- **Verification**: All computations verified against minimum 2 independent sources. 19 critical corrections documented across the corpus.

---

*Generated by ralph loop `reverse-ph-realestate-calcs`, Wave 4. Self-reviewed 2026-02-27 (catalog-review): all 16 entries verified for completeness, scoring correctness (16/16 consistent across all 3 dimensions), and tax loop cross-reference reconciliation. See `analysis/catalog-review.md` for full review findings.*
