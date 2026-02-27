# Existing Tools Survey — PH Real Estate Computation Landscape

**Wave:** 3 (Competitive & Automation Gap Analysis)
**Date:** 2026-02-27
**Method:** Web search across 50+ queries; manual tool review; mapping against 16 Wave 2 computations

---

## Summary

28 tools were identified across 5 categories: generic international calculators, Philippine bank calculators, PH-native aggregator/calculator sites, government tools, and professional/broker platforms. No single tool covers more than 4 of the 16 Wave 2 computations. The deepest coverage is in mortgage amortization (11+ tools) and Pag-IBIG loan computation (8+ tools). Zero tools were found for Maceda refund computation, BP 220 compliance checking, socialized housing compliance, condo common area percentage, assessment level lookup, improvement depreciation, or rent increase computation.

---

## PH-Specificity Rating Definitions

| Rating | Definition |
|--------|-----------|
| **Generic** | No PH rules embedded. Uses universal mortgage/amortization math. User must supply all PH-specific parameters manually. |
| **PH-adapted** | Basic PH parameters preset (PHP currency, PH bank rate ranges) but no regulatory logic. |
| **PH-native** | Built specifically for PH regulations; encodes PH-specific rules, rate tiers, or government program logic. |

---

## Tool-by-Tool Analysis

### CATEGORY 1: Generic International Calculators

#### 1. Calculator.net — Amortization Calculator
- **URL:** https://www.calculator.net/amortization-calculator.html
- **Type:** Web calculator
- **PH-Specificity:** Generic
- **What it covers:** Standard amortization schedule generation (principal + interest breakdown), extra payment scenarios, mortgage payoff modeling.
- **Computations covered:** bank-mortgage-amortization (partial — math only, no repricing/variable rate logic)
- **Key gaps:** No PH bank rate presets. No Pag-IBIG logic. No LTV computation. No regulatory compliance. No Philippine fees/taxes. No variable rate repricing mechanics. US-centric (PMI, HOA, US property tax escrow fields).

#### 2. Calculator.net — Mortgage Calculator
- **URL:** https://www.calculator.net/mortgage-calculator.html
- **Type:** Web calculator
- **PH-Specificity:** Generic
- **What it covers:** Monthly payment, total cost of ownership, amortization schedule with PMI/HOA/tax options.
- **Computations covered:** bank-mortgage-amortization (partial)
- **Key gaps:** Same as above. US tax/PMI assumptions baked in.

#### 3. Bankrate — Mortgage Calculator
- **URL:** https://www.bankrate.com/mortgages/mortgage-calculator/
- **Type:** Web calculator
- **PH-Specificity:** Generic
- **What it covers:** Monthly payment estimation, loan term comparison, down payment scenarios, extra payments, 28/36 rule guidance.
- **Computations covered:** bank-mortgage-amortization (partial), ltv-ratio (implicit — down payment vs. home value)
- **Key gaps:** US-specific (PMI, US property tax, US homeowner insurance). No PH interest rate tiers. No Pag-IBIG. No Philippine regulatory compliance. 28/36 rule differs from PH 30-40% DTI guidelines.

#### 4. Bankrate — LTV Calculator
- **URL:** https://www.bankrate.com/mortgages/ltv-loan-to-value-ratio-calculator/
- **Type:** Web calculator
- **PH-Specificity:** Generic
- **What it covers:** Loan-to-value ratio computation, CLTV for second mortgages.
- **Computations covered:** ltv-ratio (math only — no BSP circular logic)
- **Key gaps:** No BSP Circular 1087/855 LTV caps by property type. No appraisal-basis rules. No Filipino housing program LTV tiers.

#### 5. OmniCalculator — Mortgage Calculator
- **URL:** https://www.omnicalculator.com/finance/mortgage
- **Type:** Web calculator
- **PH-Specificity:** Generic
- **What it covers:** Mortgage payment estimation, interest comparison, ARM modeling, biweekly payment scenarios.
- **Computations covered:** bank-mortgage-amortization (partial)
- **Key gaps:** No PH parameters. No regulatory logic. Universal math only.

#### 6. OmniCalculator — Home Mortgage Calculator
- **URL:** https://www.omnicalculator.com/finance/home-mortgage
- **Type:** Web calculator
- **PH-Specificity:** Generic
- **What it covers:** Monthly payment, affordability check, amortization schedule with chart.
- **Computations covered:** bank-mortgage-amortization (partial)
- **Key gaps:** Same as #5.

#### 7. Google Sheets / Excel Templates (Curb Hero, Someka, Simple Sheets, etc.)
- **URLs:** Various (curbhe.ro, someka.net, simplesheets.co)
- **Type:** Spreadsheet templates
- **PH-Specificity:** Generic
- **What they cover:** Customizable amortization schedules, rental property analysis, commission tracking, pro-forma models.
- **Computations covered:** bank-mortgage-amortization (partial), broker-commission (partial — no PH rates/splits preset)
- **Key gaps:** Require manual customization for PH. No Pag-IBIG logic. No Philippine tax/fee formulas. No regulatory compliance. Widely used by PH brokers but each broker maintains their own customized version with no standardization.

---

### CATEGORY 2: Philippine Bank Calculators

#### 8. BDO — Home Loan Calculator
- **URL:** https://www.bdo.com.ph/personal/loans/home-loan/home-loan-calculator
- **Type:** Bank-specific web calculator
- **PH-Specificity:** PH-adapted
- **What it covers:** Monthly amortization for BDO home loans. BDO-specific interest rates (~6% APR). CLI premium computation (P4.75 or P6.50 per P1,000 by age bracket).
- **Computations covered:** bank-mortgage-amortization (BDO-specific only)
- **Key gaps:** Locked to BDO rates/terms. No comparison across banks. No Pag-IBIG. No LTV calculation. No fees/taxes. No regulatory compliance. No variable rate repricing logic exposed.

#### 9. BPI — Home Loan Calculator
- **URL:** https://online.bpiloans.com/housingcompute/bpi-family-housing-loan/
- **Type:** Bank-specific web calculator
- **PH-Specificity:** PH-adapted
- **What it covers:** Monthly amortization for BPI housing loans. BPI rates (6.5%-8.5%). Multiple loan types (purchase, construction, renovation, equity).
- **Computations covered:** bank-mortgage-amortization (BPI-specific only)
- **Key gaps:** Same silo problem as BDO. No cross-bank comparison. No fees/taxes. No regulatory compliance. Does not expose repricing mechanics or early termination penalty formulas.

#### 10. Metrobank — Online Loan Calculator
- **URL:** https://web.metrobank.com.ph/OnlineLoanCalculator/Default.aspx
- **Type:** Bank-specific web calculator
- **PH-Specificity:** PH-adapted
- **What it covers:** Monthly amortization for Metrobank home loans. Min loan P500K, min income P40K/month. Current promo rate 6.75% (until Jul 2025). Terms up to 25 years.
- **Computations covered:** bank-mortgage-amortization (Metrobank-specific only)
- **Key gaps:** Same silo problem. No comparison. No fees/taxes. No regulatory compliance.

#### 11. Security Bank — Home Loan Calculator
- **URL:** https://www.securitybank.com/personal/loans/home-loan-housing-mortgage/calculator/
- **Type:** Bank-specific web calculator
- **PH-Specificity:** PH-adapted
- **What it covers:** Loanable amount based on income. Monthly amortization. LTV up to 80% of appraised value. Rates from 6.75%-7.00%.
- **Computations covered:** bank-mortgage-amortization (Security Bank-specific), ltv-ratio (implicit — caps at 80%)
- **Key gaps:** Same silo problem. No cross-bank comparison. No fees/taxes. No regulatory compliance.

#### 12. UnionBank — Home Loan Calculator
- **URL:** https://www.unionbankph.com/loans/home-loan/calculator
- **Type:** Bank-specific web calculator
- **PH-Specificity:** PH-adapted
- **What it covers:** Monthly amortization for UnionBank home loans.
- **Computations covered:** bank-mortgage-amortization (UnionBank-specific only)
- **Key gaps:** Same silo problem. Minimal feature exposure.

#### 13. PNB — Mortgage Calculator
- **URL:** https://www.pnb.com.ph/index.php/loan/mortgage-calculator
- **Type:** Bank-specific web calculator
- **PH-Specificity:** PH-adapted
- **What it covers:** Monthly amortization for PNB mortgages.
- **Computations covered:** bank-mortgage-amortization (PNB-specific only)
- **Key gaps:** Same silo problem.

#### 14. PSBank — Home Loan Calculator
- **URL:** https://www.psbank.com.ph/psbank-online-loan-amortization-calculator/HomeLoan/Calculator
- **Type:** Bank-specific web calculator
- **PH-Specificity:** PH-adapted
- **What it covers:** Monthly amortization for PSBank home loans.
- **Computations covered:** bank-mortgage-amortization (PSBank-specific only)
- **Key gaps:** Same silo problem.

#### 15. HSBC PH — Borrowing Calculator
- **URL:** https://www.hsbc.com.ph/mortgages/borrowing-calculator/
- **Type:** Bank-specific web calculator
- **PH-Specificity:** PH-adapted
- **What it covers:** Affordability calculator — how much you can borrow based on income. PHP-denominated.
- **Computations covered:** bank-mortgage-amortization (HSBC-specific only)
- **Key gaps:** Same silo problem.

---

### CATEGORY 3: PH-Native Aggregator/Calculator Sites

#### 16. Housal — Real Estate Closing Costs Calculator
- **URL:** https://www.housal.com/calculators/sales-closing-fees
- **Type:** PH-native closing cost calculator
- **PH-Specificity:** PH-native
- **What it covers:** CGT (6%), EWT (6%), VAT (12%), DST (1.5%), transfer tax (0.5-0.75%), registration fees (tiered), broker commission (3-5%). Seller vs. buyer cost separation. Individual vs. corporate seller distinction. Net selling price computation for VAT-inclusive transactions.
- **Computations covered:** broker-commission (partial — uses standard 3-5% but no split computation), rod-registration-fees (partial — tiered but unclear if uses exact LRA schedule)
- **Key gaps:** This is primarily a TAX tool (CGT, DST, VAT are out-of-scope for this loop). For non-tax computations: no Pag-IBIG, no mortgage amortization, no Maceda, no regulatory compliance, no assessment levels, no depreciation, no association dues. Commission computation is flat rate only — no broker-agent split, no multi-tier, no EWT on commission.

#### 17. ForeclosurePhilippines.com — Calculator Suite
- **URL:** https://www.foreclosurephilippines.com/resources/
- **Type:** PH-native calculator collection
- **PH-Specificity:** PH-native
- **Tools available:**
  - **Home Loan Calculator:** Selling price, DP%, loan term, interest rate -> monthly amortization + required income (40% DTI rule)
  - **Amortization Table Calculator:** Full amortization schedule with monthly P&I breakdown. Supports Contract-to-Sell installments.
  - **Amortization Factor Rate Calculator:** Factor rate tables for 1-20% rates, 1-30 year terms.
  - **ARV Calculator:** After-repair-value using replacement cost approach (for foreclosed property investing).
  - **Gross Rental Yield Calculator:** Monthly/annual yield from selling price + rent.
  - **Registry of Deeds Fee Calculator:** Computes LRA registration fees by property value bracket.
- **Computations covered:** bank-mortgage-amortization (good — generic PH, not bank-locked), rod-registration-fees (direct match — uses LRA fee schedule), developer-equity-schedule (partial — CTS installment support)
- **Key gaps:** No Pag-IBIG specific logic (rate tiers, MRI/FGI). No LTV computation. No Maceda refund. No rent increase. No condo dues. No BP 220 compliance. No assessment levels. No depreciation. No notarial fees. No broker commission split. The mortgage calculator is generic (user supplies rate) — no bank-specific rate presets or comparison.

#### 18. LoanCalculatorOnline.org — Philippine Loan Calculators
- **URL:** https://loancalculatoronline.org/ph/loan-calculator-philippines
- **Type:** PH-adapted aggregator
- **PH-Specificity:** PH-adapted
- **Tools available:**
  - Bank-specific home loan calculators (BDO, BPI, Metrobank, Security Bank, PNB, etc.)
  - Pag-IBIG housing/MPL/calamity loan calculators
  - Car loan calculator
  - BSP guideline compliance check (30-35% DTI)
  - Salary-based eligibility
  - Excel/CSV export of amortization schedules
- **Computations covered:** bank-mortgage-amortization (multi-bank, with rate presets), pagibig-amortization (partial — standard formula, Pag-IBIG rate tiers), pagibig-loan-eligibility (partial — salary-based check)
- **Key gaps:** Pag-IBIG calculator does not compute MRI/FGI premiums. No LTV per BSP circular. No Maceda. No rent control. No regulatory compliance. No fees/taxes. No association dues. Third-party site — accuracy of bank rates not guaranteed.

#### 19. CalculatorPH.com — Housing Loan Calculator
- **URL:** https://calculatorph.com/housing-loan-calculator.html
- **Type:** PH-adapted aggregator
- **PH-Specificity:** PH-adapted
- **What it covers:** Housing loan estimates for Pag-IBIG, BDO, BPI, Metrobank. Amortization chart. Full payment table.
- **Computations covered:** bank-mortgage-amortization (multi-bank), pagibig-amortization (basic)
- **Key gaps:** Same as #18 but fewer features. No MRI/FGI. No regulatory compliance. No fees.

#### 20. Clevrr.ph — Real Estate Calculators
- **URL:** https://clevrr.ph/calculators
- **Type:** PH-native calculator collection
- **PH-Specificity:** PH-native
- **Tools available:**
  - Commission Calculator (individual sales)
  - Rental Yield Calculator
  - ROI Calculator
  - Square Meter Calculator (area conversion)
  - Buy and Sell Calculator
  - BIR Zonal Values lookup
- **Computations covered:** broker-commission (partial — flat rate, no split/multi-tier)
- **Key gaps:** Commission calculator is for individual sales only. No split computation. No EWT on commission. No Pag-IBIG. No amortization. No regulatory compliance. No fees. Zonal values lookup is useful context but not a computation per se.

#### 21. PhilPropertyExpert — Financing Calculator
- **URL:** https://philpropertyexpert.com/financing-calculator/
- **Type:** PH-adapted simple calculator
- **PH-Specificity:** PH-adapted
- **What it covers:** Basic monthly amortization estimate. Notes that banks/Pag-IBIG may use different factor rates.
- **Computations covered:** bank-mortgage-amortization (basic)
- **Key gaps:** Very basic. No bank presets. No Pag-IBIG specifics. No fees/taxes. No regulatory compliance.

#### 22. Dot Property PH — Loan Calculator
- **URL:** https://www.dotproperty.com.ph/loan-calculator
- **Type:** PH-adapted simple calculator
- **PH-Specificity:** PH-adapted
- **What it covers:** Monthly mortgage payment estimation with multiple rates, fixed monthly payments, extra payments.
- **Computations covered:** bank-mortgage-amortization (basic)
- **Key gaps:** Listing platform first, calculator second. Basic amortization only.

#### 23. Investing.com PH — Mortgage Calculator
- **URL:** https://ph.investing.com/tools/mortgage-calculator
- **Type:** PH-adapted
- **PH-Specificity:** PH-adapted
- **What it covers:** Monthly payment estimation in PHP context.
- **Computations covered:** bank-mortgage-amortization (basic)
- **Key gaps:** Generic calculator localized for PH currency. No PH regulatory logic.

---

### CATEGORY 4: Government Tools

#### 24. Pag-IBIG Fund — Housing Loan Affordability Calculator (Official)
- **URL:** https://www.pagibigfundservices.com/ac/
- **Type:** Official government calculator
- **PH-Specificity:** PH-native
- **What it covers:** Three modes: (a) loanable amount from income, (b) income required for target loan, (c) loanable amount from property value. Uses official Pag-IBIG interest rate tiers (5.5%/6.375%/7.375% by loan bracket). 35% DTI cap. Max P6M loan. Age + term <= 70 constraint.
- **Computations covered:** pagibig-loan-eligibility (direct match — official source), pagibig-amortization (partial — computes monthly payment but may not expose full schedule with MRI/FGI breakdown)
- **Key gaps:** Does not display detailed MRI/FGI premium computation separately. Does not generate downloadable amortization schedule. No comparison with bank options. No other computations.

#### 25. OmniCalculator — Pag-IBIG Housing Loan Calculator
- **URL:** https://www.omnicalculator.com/finance/pag-ibig-housing-loan
- **Type:** Third-party PH-native calculator
- **PH-Specificity:** PH-native
- **What it covers:** Three functions matching official Pag-IBIG calculator: loanable amount, monthly amortization, required income. Max P6M cap. Pag-IBIG rate tiers.
- **Computations covered:** pagibig-loan-eligibility (good), pagibig-amortization (good — but still no MRI/FGI breakdown)
- **Key gaps:** No MRI/FGI premium computation. No full amortization schedule with yearly breakdown. No bank comparison. Supplementary tool — defers to official calculator for definitive answers.

#### 26. PagibigCalculator.com — Suite
- **URL:** https://pagibigcalculator.com/
- **Type:** Third-party PH-native calculator
- **PH-Specificity:** PH-native
- **What it covers:** Housing loan calculator, MP2 savings calculator, contribution calculator, multi-purpose loan calculator.
- **Computations covered:** pagibig-loan-eligibility (partial), pagibig-amortization (partial)
- **Key gaps:** Same as OmniCalculator Pag-IBIG — no MRI/FGI. No other real estate computations.

#### 27. LRA — Estimate Registration Computation Fees (ERCF)
- **URL:** https://lra.gov.ph/ercf/
- **Type:** Official government calculator
- **PH-Specificity:** PH-native
- **What it covers:** Official LRA registration fee computation by property value. Used by Registry of Deeds cashiers.
- **Computations covered:** rod-registration-fees (direct match — authoritative source)
- **Key gaps:** Registration fees only. No other computations. Interface is basic. No annotation fee computation (which is separate).

#### 28. BSP — Bank Loan Calculator
- **URL:** https://www.bsp.gov.ph/SitePages/BankCalc.aspx
- **Type:** Official government calculator
- **PH-Specificity:** PH-native
- **What it covers:** Five amortization modes: fixed equal amortization, fixed principal amortization, with grace period, balloon payment at maturity, weekly installments. Loan amount, start date, term inputs.
- **Computations covered:** bank-mortgage-amortization (good — multiple amortization structures)
- **Key gaps:** Generic bank loan calculator — not housing-specific. No LTV computation. No bank rate presets. No Pag-IBIG. No fees/taxes. No regulatory compliance.

#### 29. HGC (Home Guaranty Corporation) — Amortization Calculator
- **URL:** http://www.hgc.gov.ph/compute.html
- **Type:** Government calculator
- **PH-Specificity:** PH-native
- **What it covers:** Monthly amortization computation for government-guaranteed housing loans.
- **Computations covered:** bank-mortgage-amortization (basic — government housing context)
- **Key gaps:** Limited functionality. HGC is now PhilGuarantee. Site may be outdated.

---

### CATEGORY 5: Professional/Broker Tools

#### 30. iRealtee — Brokerage Operating System
- **URL:** https://irealtee.com
- **Type:** SaaS platform for PH brokerages
- **PH-Specificity:** PH-native
- **Launched:** January 2026
- **What it covers:** Full brokerage management: CRM, property inventory, agent profiles, commission calculator, accounting/balance sheet, audit trail, LMS training. Commission calculator auto-applies EWT (10% under P3M / 15% over P3M — note: our Wave 2 analysis found these rates are from RR 11-2018: 5%/10% at P3M threshold). Multi-tier commission split computation. PRC license management.
- **Computations covered:** broker-commission (best coverage found — includes split, multi-tier, EWT deduction, net commission)
- **Key gaps:** Commission-focused. No amortization. No Pag-IBIG. No regulatory compliance (Maceda, rent control, BP 220). No closing cost computation. No association dues. No assessment levels. EWT rates may not match current RR 11-2018 schedule (their page says 10%/15% at P3M which differs from our verified 5%/10%).

#### 31. REBAP — Amortization Calculator
- **URL:** https://www.rebap.com.ph/amortization
- **Type:** Professional association tool
- **PH-Specificity:** PH-adapted
- **What it covers:** Basic amortization computation for REBAP member brokers.
- **Computations covered:** bank-mortgage-amortization (basic)
- **Key gaps:** Very basic. No Pag-IBIG. No fees. No regulatory compliance.

#### 32. TaxCalculatorPhilippines.online — RPT Tools
- **URL:** https://taxcalculatorphilippines.online/real-property-tax-philippines/
- **Type:** PH-native tax calculator
- **PH-Specificity:** PH-native
- **What it covers:** RPT computation (rate x assessed value), assessment level guidance, payment deadline tracking, penalty computation, exemption guidance. Metro Manila (2%) vs. provincial (1%) rates. SEF (1%) add-on.
- **Computations covered:** assessment-level-lookup (partial — explains levels but unclear if has full lookup by classification/bracket)
- **Key gaps:** Primarily content/guidance rather than interactive calculator. No LGU-specific rate database. No building depreciation. No other computations. RPT is technically out-of-scope for this loop (covered by ph-tax-computations-reverse) but assessment-level-lookup bridges both.

#### 33. OwnPropertyAbroad — RPT Calculator
- **URL:** https://ownpropertyabroad.com/philippines/philippines-real-property-tax-calculator-rpt/
- **Type:** PH-native RPT calculator
- **PH-Specificity:** PH-native
- **What it covers:** RPT computation from property value and location (Metro Manila vs. province).
- **Computations covered:** assessment-level-lookup (partial)
- **Key gaps:** Simplified — may not handle all classification tiers. No full LGC Section 218 bracket table. No depreciation.

#### 34. LandValuePH
- **URL:** https://www.landvalueph.com/
- **Type:** PH-native valuation tool
- **PH-Specificity:** PH-native
- **What it covers:** BIR zonal data lookup for 200+ cities. Property appraisal. Tax computation.
- **Computations covered:** assessment-level-lookup (contextual — zonal value is an input, not the assessment level computation itself)
- **Key gaps:** Zonal value lookup is useful context but does not compute assessment levels per LGC Section 218.

---

## Coverage Matrix

Mapping all tools against the 16 Wave 2 computations:

| # | Computation | Tools with ANY coverage | Best available tool | Coverage quality |
|---|------------|------------------------|--------------------|--------------------|
| 1 | pagibig-loan-eligibility | Pag-IBIG Official (#24), OmniCalc PagIBIG (#25), PagibigCalculator (#26), LoanCalcOnline (#18) | Pag-IBIG Official (#24) | **GOOD** — official tool covers eligibility modes but does not expose decision tree for edge cases (loan-on-top-of-loan, property type restrictions) |
| 2 | pagibig-amortization | Pag-IBIG Official (#24), OmniCalc (#25), PagibigCalculator (#26), LoanCalcOnline (#18), CalculatorPH (#19) | OmniCalc Pag-IBIG (#25) | **PARTIAL** — standard amortization computed correctly but NO tool computes MRI/FGI premium separately; no tool generates full schedule with insurance breakdown |
| 3 | bank-mortgage-amortization | 11+ tools (all bank calculators, generics, ForeclosurePH, BSP, etc.) | BSP Calculator (#28) + ForeclosurePH (#17) | **GOOD for basic amortization** — well-covered. BUT no tool handles: variable rate repricing mechanics, early termination penalty formulas, bank-specific promotional rate transitions, or multi-bank comparison in one interface |
| 4 | developer-equity-schedule | ForeclosurePH (#17, partial CTS support) | ForeclosurePH (#17) | **POOR** — no tool computes full developer equity schedule (reservation fee deduction, spot cash discount tiers, installment penalty/surcharge, turnover balance, PD 957 escalation cap). This is universally done via developer-provided sample computations or broker Excel sheets. |
| 5 | ltv-ratio | Bankrate LTV (#4, generic), Security Bank (#11, implicit 80% cap) | None adequate | **POOR** — generic LTV calculators exist but none encode BSP Circular 1087/855 LTV caps by property type, appraisal basis rules, or additional collateral requirements. PH practitioners rely on bank-side computation. |
| 6 | maceda-refund | NONE | NONE | **ZERO** — no online calculator found for Maceda Law (RA 6552) cash surrender value / refund computation. The 50% + 5%/yr formula is simple but no tool implements it. Grace period computation (1 month per year paid) also not automated. |
| 7 | rent-increase-computation | NONE | NONE | **ZERO** — no rent increase calculator found for RA 9653 / NHSB Resolution annual caps. Practitioners manually apply the announced percentage (2.3% for 2025, 1% for 2026). No tool checks coverage eligibility (rent bracket, same-tenant rule). |
| 8 | condo-common-area-pct | NONE | NONE | **ZERO** — no tool computes undivided interest in common areas per RA 4726. The formula (unit floor area / total sellable area) is straightforward but no tool implements it with master deed parameters. |
| 9 | socialized-housing-compliance | NONE | NONE | **ZERO** — no compliance checker for DHSUD socialized/economic housing price ceilings. No tool validates per-unit and per-sqm limits by housing type or checks annual escalation. Developers and DHSUD staff do this manually against current circulars. |
| 10 | bp220-lot-compliance | NONE | NONE | **ZERO** — no tool validates BP 220 minimum lot areas (64/48/28 sqm socialized; 72/54/36 sqm economic), floor area ratios, open space percentages, or community facility allocations. Architects and developers reference the IRR manually. |
| 11 | assessment-level-lookup | TaxCalcPH (#32, partial), OwnPropertyAbroad (#33, partial) | TaxCalcPH (#32) | **POOR** — existing tools explain the concept and handle simple cases (apply Metro Manila 2% or provincial 1% RPT rate) but none implement the FULL LGC Section 218 assessment level table with all classification tiers, value brackets, and LGU-specific variations. |
| 12 | improvement-depreciation | NONE | NONE | **ZERO** — no PH-specific tool for building improvement depreciation computation (straight-line method with construction-type useful life, residual value per local assessor schedules). Generic depreciation calculators exist but none with PH assessor parameters. |
| 13 | rod-registration-fees | LRA ERCF (#27, official), ForeclosurePH (#17) | LRA ERCF (#27) | **GOOD** — the official LRA tool is authoritative. ForeclosurePH provides a convenient alternative. However, neither computes annotation fees (separate schedule) or total title transfer cost pipeline. |
| 14 | notarial-fees | NONE | NONE | **ZERO** — no calculator for notarial fees. Practitioners use rule-of-thumb (1-2% of selling price) or negotiate directly. The OCA Circular 73-2014 per-page ceiling (P200/P50) is statutory but not widely computed. IBP-based fee guidance varies by chapter. |
| 15 | broker-commission | iRealtee (#30), Clevrr (#20), Housal (#16, partial) | iRealtee (#30) | **PARTIAL** — iRealtee has the best coverage (multi-tier split + EWT deduction) but is embedded in a full SaaS platform, not a standalone calculator. Clevrr and Housal compute flat commission only. No tool handles: MLS co-broke splits, lease commission (1 month), rent-to-own conversion commission, or full BIR form generation. |
| 16 | condo-association-dues | NONE | NONE | **ZERO** — no tool computes monthly condo dues using the ECR 001-17 formula (gross expense / gross area x unit sqm). No sinking fund calculator. No special assessment allocation tool. No delinquency penalty computation. Condo corporations use internal spreadsheets. |

---

## Gap Summary by Severity

### ZERO COVERAGE (no tool exists) — 7 computations
1. **maceda-refund** — RA 6552 cash surrender value (50% + 5%/yr), grace period computation
2. **rent-increase-computation** — RA 9653 / NHSB annual cap application, coverage eligibility check
3. **condo-common-area-pct** — RA 4726 undivided interest formula
4. **socialized-housing-compliance** — DHSUD price ceiling validation
5. **bp220-lot-compliance** — BP 220 minimum standards compliance check (12+ deterministic checks)
6. **improvement-depreciation** — Building depreciation per local assessor schedules
7. **notarial-fees** — OCA Circular per-page ceiling + IBP-based fee guidance
8. **condo-association-dues** — ECR 001-17 dues formula, sinking fund, delinquency penalty

### POOR COVERAGE (tools exist but miss PH-specific logic) — 3 computations
1. **developer-equity-schedule** — No tool handles full developer computation (spot cash, penalty, turnover)
2. **ltv-ratio** — Generic LTV exists but no BSP circular logic encoded
3. **assessment-level-lookup** — Simplified RPT tools exist but no full LGC Section 218 implementation

### PARTIAL COVERAGE (some tools, significant gaps remain) — 3 computations
1. **pagibig-amortization** — Good basic amortization but NO MRI/FGI premium breakdown
2. **broker-commission** — iRealtee covers splits/EWT but is SaaS-locked; no standalone tool
3. **bank-mortgage-amortization** — Well-covered for basic computation; gaps in repricing, penalties, comparison

### GOOD COVERAGE (adequate tools exist) — 2 computations
1. **pagibig-loan-eligibility** — Official Pag-IBIG tool + 3rd party calculators cover core eligibility
2. **rod-registration-fees** — Official LRA ERCF tool + ForeclosurePH calculator

---

## Key Observations

### 1. The Amortization Monoculture
The PH real estate calculator ecosystem is overwhelmingly focused on one computation: basic mortgage amortization. At least 11 tools compute this. Yet the ecosystem drops to ZERO tools for 7 of 16 computations that practitioners actually need.

### 2. Bank Calculator Siloing
Every major PH bank (BDO, BPI, Metrobank, Security Bank, UnionBank, PNB, PSBank, HSBC) has its own calculator, but each is locked to that bank's rates and terms. No tool enables cross-bank comparison. LoanCalculatorOnline.org comes closest but uses pre-set rates that may not match current offerings.

### 3. The Missing Regulatory Layer
Not a single tool encodes Philippine real estate regulatory compliance logic:
- No Maceda Law refund calculator despite RA 6552 being >50 years old
- No rent control calculator despite RA 9653 being actively enforced
- No BP 220 compliance checker despite being mandatory for all socialized housing
- No DHSUD price ceiling validator
These computations are purely deterministic with clear statutory formulas — they are prime automation candidates.

### 4. Professional Tools Gap
Philippine brokers overwhelmingly use:
- Developer-provided sample computation sheets (PDF/Excel)
- Personal Excel/Google Sheets templates (no standardization)
- Basic online calculators for quick amortization checks
- Manual computation for fees, taxes, and regulatory compliance

iRealtee (launched Jan 2026) is the first PH-native brokerage platform but focuses on operations management rather than computation engines. Its commission calculator is the most sophisticated found but still has gaps (EWT rate accuracy, MLS splits).

### 5. No Integrated Pipeline
No tool covers the full real estate transaction computation pipeline: eligibility check -> amortization schedule -> equity computation -> closing costs (fees + taxes) -> regulatory compliance. Every practitioner assembles this from 4-6 different tools/spreadsheets.

---

## Sources

- [REBAP Amortization Calculator](https://www.rebap.com.ph/amortization)
- [ForeclosurePhilippines.com Resources](https://www.foreclosurephilippines.com/resources/)
- [ForeclosurePhilippines.com ROD Fee Calculator](https://www.foreclosurephilippines.com/how-to-compute-registration-fees/)
- [Housal Closing Costs Calculator](https://www.housal.com/calculators/sales-closing-fees)
- [OmniCalculator Pag-IBIG Housing Loan](https://www.omnicalculator.com/finance/pag-ibig-housing-loan)
- [OmniCalculator Mortgage Calculator](https://www.omnicalculator.com/finance/mortgage)
- [Bankrate Mortgage Calculator](https://www.bankrate.com/mortgages/mortgage-calculator/)
- [Bankrate LTV Calculator](https://www.bankrate.com/mortgages/ltv-loan-to-value-ratio-calculator/)
- [Calculator.net Amortization Calculator](https://www.calculator.net/amortization-calculator.html)
- [BDO Home Loan Calculator](https://www.bdo.com.ph/personal/loans/home-loan/home-loan-calculator)
- [BPI Home Loan Calculator](https://online.bpiloans.com/housingcompute/bpi-family-housing-loan/)
- [Metrobank Online Loan Calculator](https://web.metrobank.com.ph/OnlineLoanCalculator/Default.aspx)
- [Security Bank Home Loan Calculator](https://www.securitybank.com/personal/loans/home-loan-housing-mortgage/calculator/)
- [UnionBank Home Loan Calculator](https://www.unionbankph.com/loans/home-loan/calculator)
- [PNB Mortgage Calculator](https://www.pnb.com.ph/index.php/loan/mortgage-calculator)
- [PSBank Home Loan Calculator](https://www.psbank.com.ph/psbank-online-loan-amortization-calculator/HomeLoan/Calculator)
- [HSBC PH Borrowing Calculator](https://www.hsbc.com.ph/mortgages/borrowing-calculator/)
- [Pag-IBIG Official Affordability Calculator](https://www.pagibigfundservices.com/ac/)
- [PagibigCalculator.com](https://pagibigcalculator.com/)
- [Pinoy Benefits Pag-IBIG Calculator](https://pinoybenefits.com/calculators/pagibig-housing-loan/)
- [LoanCalculatorOnline.org PH](https://loancalculatoronline.org/ph/loan-calculator-philippines)
- [CalculatorPH.com](https://calculatorph.com/housing-loan-calculator.html)
- [Clevrr.ph Calculators](https://clevrr.ph/calculators)
- [PhilPropertyExpert Financing Calculator](https://philpropertyexpert.com/financing-calculator/)
- [Dot Property PH Loan Calculator](https://www.dotproperty.com.ph/loan-calculator)
- [Investing.com PH Mortgage Calculator](https://ph.investing.com/tools/mortgage-calculator)
- [LRA ERCF](https://lra.gov.ph/ercf/)
- [BSP Bank Loan Calculator](https://www.bsp.gov.ph/SitePages/BankCalc.aspx)
- [HGC Amortization Calculator](http://www.hgc.gov.ph/compute.html)
- [iRealtee](https://irealtee.com)
- [iRealtee Commission Calculator](https://irealtee.com/features/commission-calculator)
- [TaxCalculatorPhilippines.online RPT](https://taxcalculatorphilippines.online/real-property-tax-philippines/)
- [OwnPropertyAbroad RPT Calculator](https://ownpropertyabroad.com/philippines/philippines-real-property-tax-calculator-rpt/)
- [LandValuePH](https://www.landvalueph.com/)
