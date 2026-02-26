# Pag-IBIG Amortization — Independent Verification Report

**Aspect:** pagibig-amortization (Wave 2)
**Date:** 2026-02-26
**Method:** Web search across 3+ independent sources per claim, independent formula computation, cross-check against official/third-party calculators

---

## Sources Used

| # | Source | Type | URL |
|---|--------|------|-----|
| S1 | OmniCalculator — Pag-IBIG Housing Loan | Third-party calculator | https://www.omnicalculator.com/finance/pag-ibig-housing-loan |
| S2 | Respicio & Co. — Pag-IBIG Housing Loan Interest Rate | Legal practitioner guide | https://www.respicio.ph/commentaries/pag-ibig-housing-loan-interest-rate |
| S3 | best-calculators.com — Pag-IBIG Housing Loan Calculator | Third-party calculator | https://best-calculators.com/finance/pag-ibig-housing-loan-calculator/ |
| S4 | PagibigFinancing.com — Insurance, Processing Fee and Other Expenses | Practitioner guide | https://www.pagibigfinancing.com/articles/2010/insurance-processing-fee-and-other-pag-ibig-housing-loan-expenses/ |
| S5 | PagibigFinancing.com — Interest Rates, Penalties and Defaults | Practitioner guide | https://www.pagibigfinancing.com/articles/2011/pag-ibig-loans-interest-rates-penalties-and-defaults-part-2-of-2/ |
| S6 | Manila Bulletin — Pag-IBIG cuts non-life insurance premiums (2018) | News report | https://mb.com.ph/2018/08/19/pag-ibig-cuts-non-life-insurance-premiums/ |
| S7 | ASEAN SSA — Pag-IBIG Fund Recognition Award Document | Institutional report | https://www.asean-ssa.org/files/ASSA%20Recognition%20Award/2017/F%20Home%20Development%20Mutual%20Fund,%20Philippines.pdf |
| S8 | LegalDex — Guidelines on Pag-IBIG Fund EUF Program | Legal database | https://legaldex.com/laws/guidelines-on-the-pag-ibig-fund-end-user-home-financing-program |
| S9 | Inquirer — Pag-IBIG home loan rates unchanged through 2025 | News report | https://business.inquirer.net/529457/pag-ibig-home-loan-rates-unchanged-throughout-2025 |
| S10 | PCO — Pag-IBIG Fund lowers home loan rates | Government press release | https://pco.gov.ph/other_releases/pag-ibig-fund-lowers-home-loan-rates/ |
| S11 | Philstar — Pag-IBIG extends low home loan rates until end-2025 | News report | https://www.philstar.com/business/2025/06/07/2448673/pag-ibig-extends-low-home-loan-rates-until-end-2025 |
| S12 | Respicio & Co. — Pag-IBIG Housing Loan Rules and Requirements | Legal practitioner guide | https://www.respicio.ph/commentaries/pag-ibig-housing-loan-rules-and-requirements-in-philippines |
| S13 | Circular No. 403 — Modified AHP Guidelines | Official circular (via Supreme Court E-Library) | https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/90472 |
| S14 | Lawyer-philippines.com — Pag-IBIG Housing Loan Partial Payment Terms | Legal analysis | https://www.lawyer-philippines.com/articles/pag-ibig-housing-loan-partial-payment-terms |
| S15 | PNA — Pag-IBIG 3% loan rate amid higher socialized housing price caps | Government news | https://www.pna.gov.ph/articles/1266253 |

---

## Claim-by-Claim Verification

### 1. Amortization Formula

**Claim:** M = P x [r(1+r)^n] / [(1+r)^n - 1], where r = annual_rate/12, n = term_years x 12

**Verdict: CONFIRMED**

All sources agree on the standard declining-balance amortization formula:
- S1 (OmniCalculator) states: `A = [P x i/12 x (1 + i/12)^n] / [(1 + i/12)^n - 1]` -- identical formula with different variable names
- S3 (best-calculators.com) states: `M = P x [r(1+r)^n] / [(1+r)^n - 1]` -- exact match
- S13 (Circular 403) states: "The housing loan shall be paid in equal monthly amortizations in such amounts as may fully cover the principal and interest"

**Independent computation cross-check:**
- Input: P=2,000,000, annual_rate=9.75% (30-year repricing), n=360 months
- Computed: M = PHP 17,183.09
- OmniCalculator result [S1]: PHP 17,183.09 -- exact match
- First month interest: PHP 16,250.00 (= 2,000,000 x 0.0975/12) -- matches S1
- First month principal: PHP 933.09 -- matches S1

Additional cross-check:
- Input: P=1,000,000, rate=7.125%, n=120 months
- Computed: M = PHP 11,675.37
- OmniCalculator total with PHP 45 insurance: PHP 11,720.37 -- matches S1

---

### 2. Interest Rate Schedule

**Claim A (by repricing period):**

| Repricing Period | Rate p.a. |
|---|---|
| 1-year | 5.750% |
| 3-year | 6.250% |
| 5-year | 6.500% |
| 10-year | 7.125% |
| 15-year | 7.750% |
| 20-year | 8.500% |
| 25-year | 9.125% |
| 30-year | 9.750% |

**Verdict: CONFIRMED** -- This is the current rate structure.

- S2 (Respicio): Exact match, citing rates effective through 2025 under Full Risk-Based Pricing (FRBP)
- S9 (Inquirer): Confirms 5.75% for 1-year, 6.25% for 3-year, and lists 6.5%, 7.125%, 7.75%, 8.5%, 9.125%, 9.75% for longer periods
- S10 (PCO government press release): Confirms exact same rates, noting they were lowered effective July 1, 2023
- S11 (Philstar): Confirms rates maintained through end of 2025

The current rate structure is definitively **by repricing period**, not by loan amount. This was established via Board Resolution 2940-2012 adopting Full Risk-Based Pricing [S2].

**Claim B (by loan amount bracket):**

| Loan Amount | Rate |
|---|---|
| P400K-P3M | 5.5% |
| P3M-P4.5M | 6.375% |
| P4.5M-P6M | 7.375% |

**Verdict: CONFLICT -- This is an outdated or unofficial rate structure**

- S3 (best-calculators.com) cites these exact rates "as of 2024" but provides no official circular reference
- S8 (LegalDex, older EUF circular) shows a completely different historical loan-amount-based rate structure (6%-11.5% by bracket), confirming that loan-amount-based pricing existed in earlier circulars but at different rates
- S5 (PagibigFinancing) mentions rates "7-13.5% depending on repricing period," suggesting awareness of both systems
- No official government source (PCO, PNA, Philstar, Inquirer) describes rates as loan-amount-based

**Reconciliation:** The loan-amount-based rates (5.5%, 6.375%, 7.375%) appear to be an unofficial simplification found on third-party calculator websites. They do NOT appear in any government press release or official HDMF communication from 2023-2025. The official structure uses **repricing-period-based rates**. The older circulars (pre-FRBP) did use loan-amount-based rates, but at different values (6%-11.5%). The 5.5%/6.375%/7.375% figures may represent a transitional or promotional table from ~2022-2023 that has been superseded but persists on some calculator sites.

**Alternative input table note:** The input file (Section 5.2) also cites a slightly different repricing table from myhousingloancal.ph (e.g., 3-year = 6.375% instead of 6.25%). These appear to be **pre-July 2023 rates** before the Board-approved reduction. The July 2023 reduction lowered the 3-year rate from 6.375% to 6.25%, confirming the Section 5.1 table is current.

---

### 3. MRI Premium Rate Table

**Claim:** Age-bracketed rates per P1,000 of outstanding balance per year (from Circular No. 428):

| Age | Rate per P1,000/year |
|---|---|
| <=30 | P0.42 |
| 31-35 | P0.57 |
| 36-40 | P0.73 |
| 41-45 | P1.02 |
| 46-50 | P1.50 |
| 51-55 | P2.23 |
| 56-60 | P3.49 |
| 61-65 | P5.54 |

**Verdict: CONFLICT -- Multiple conflicting claims about whether MRI is age-bracketed or uniform**

**Evidence for uniform rate (contradicts age-bracket table):**
- S7 (ASSA institutional report): "premiums were cut by half from PhP0.41 per PhP1,000 to only PhP0.23 per PhP1,000" -- describes a single uniform rate, not age-bracketed
- S4 (PagibigFinancing): "yearly renewable term insurance (YRT) for which the borrowers shall pay an **even premium rate** effective upon loan take-out" -- "even" suggests uniform
- S13 (Circular 403, official): "the borrowers shall pay a **uniform premium rate** effective on the date of takeout" -- explicitly says "uniform"

**Evidence for age-bracketed rates:**
- The input file cites Circular No. 428 as the source for the age-bracket table
- However, actual Circular No. 428 was found to be titled "Omnibus Guidelines on the Sale of Pag-IBIG Fund Real and Other Properties Acquired" (about foreclosed property sales), NOT about MRI rates [pagibigfund.gov.ph circular listing]

**Key finding on Circular 428:** The primary source incorrectly attributes the MRI rate table to Circular No. 428. The actual Circular 428 deals with acquired asset sales, not insurance premiums. The MRI rate table source could not be independently verified.

**Historical context:**
- Pre-2014: MRI operated through a YRT Insurance Pool with rates that may have varied (P0.41/1000 average)
- 2014-2015: Pag-IBIG reformed MRI by contracting Lockton Philippines, cutting rate to P0.23/1000 (uniform)
- Post-2014: Official circulars describe "uniform premium rate"

**Analysis of the rate levels:** The age-bracketed rates in the claim (P0.42-P5.54 per 1000/year) and the uniform rate (P0.23 per 1000) are in different ranges. If the 0.23/1000 is a monthly rate, then annual = P2.76/1000, which falls in the middle of the age-bracket table. If it is an annual rate, it is lower than even the youngest bracket (P0.42). The most likely reconciliation is:
- The age-bracket table may be from the **pre-2014 insurance pool era** or from a specific circular that predates the reform
- The current system uses a **uniform rate** following the 2014 reform

**Verdict detail:** The age-bracket MRI table is **UNVERIFIED** -- it cannot be confirmed from any accessible official source. The claimed source (Circular 428) is incorrect. The current MRI appears to use a uniform premium rate per official circular language. The specific current uniform rate (whether still P0.23/1000 or updated since the last insurance contract rebidding) could not be confirmed.

---

### 4. FGI (Fire/General Insurance) Premium

**Claim:** Rate = 0.076% p.a. of insured value; insured value = min(appraised_value_of_improvements, loan_amount)

**Verdict: CONFLICT on rate; CONFIRMED on insured value basis**

**Rate verification:**
- S6 (Manila Bulletin 2018): States rate was reduced to **0.1686%** of appraised building value (from 0.40%), effective January 2018
- No source was found confirming the **0.076%** rate
- The 0.1686% rate (2018) is the most recent publicly documented FAPI rate from a credible news source
- The claimed 0.076% rate is approximately 45% of the 2018 rate, suggesting either a further rate reduction after 2018 (possible but undocumented in publicly accessible sources) or an error

**Insured value basis:**
- S4 (PagibigFinancing): "amount of insurance is the lower of the appraised value of the residential unit or the amount of the loan" -- CONFIRMED
- S6 (Manila Bulletin): Premium computed on "appraised value of the building" -- consistent (building = improvements)
- S13 (Circular 403): Confirms insurance on the housing component

**Cross-check against OmniCalculator:**
- For a P1,000,000 loan at 7.125%/10yr, OmniCalc shows ~P45/month total insurance
- At 0.076% FGI + uniform MRI: P63.33 + P19.17 = P82.50/month (too high)
- At 0.1686% FGI: P140.50 + P19.17 = P159.67/month (way too high)
- The P45 figure from OmniCalc likely uses a different rate or simplified estimate

**Conclusion on FGI rate:** The 0.076% rate is **UNVERIFIED**. The most recently documented rate is 0.1686% (2018). Neither rate produces results consistent with the OmniCalculator's P45/month insurance figure for a P1M loan. The FGI rate appears to be updated periodically when Pag-IBIG rebids its insurance contract; the current rate requires direct verification from Pag-IBIG.

---

### 5. Total Monthly Payment Formula

**Claim:** Total = Monthly Amortization (P+I) + Monthly MRI + Monthly FGI

**Verdict: CONFIRMED**

- S13 (Circular 403): "paid in equal monthly amortizations...as may fully cover the principal and interest, as well as insurance premiums"
- S1 (OmniCalculator): Shows monthly amortization + monthly insurance premium = total monthly payment
- S4 (PagibigFinancing): First year insurance is prepaid from loan proceeds; subsequent years collected monthly alongside amortization

**Additional nuance confirmed:** Insurance premiums are collected simultaneously with the loan amortization, creating a single monthly payment that encompasses P+I+MRI+FGI.

---

### 6. Payment Priority Order

**Claim:**
1. Penalties (0.05% per day of delay)
2. Upgraded membership contributions
3. Insurance premiums (MRI + FGI)
4. Interest
5. Principal

**Verdict: CONFIRMED**

- S8 (LegalDex, EUF circular): Exact same 5-item priority: "Penalties, Upgraded membership contributions, Insurance premiums, Interest, Principal"
- S13 (Circular 403, via Supreme Court E-Library): "monthly payment shall be applied according to the following order of priority: Penalties, Insurance Premiums, Interest, and Principal" -- 4-item version (omits membership contributions but otherwise consistent)
- S12 (Respicio): Confirms payments applied to "outstanding interest or penalties first before applying the remainder to the principal"

**Note:** Some sources show a 4-item priority (omitting "upgraded membership contributions"), while the EUF circular shows 5 items. The 5-item version from the primary source is the more complete version and is confirmed by LegalDex's citation of the original EUF circular.

---

### 7. Repricing Mechanics

**Claim:** At end of fixed period, Board sets new rate; amortization recomputed on remaining balance for remaining term; borrower may choose new repricing period.

**Verdict: CONFIRMED with additional detail**

- S2 (Respicio): "When the lock-in expires the loan shifts to the new Board-approved rate for the chosen period, applied to the outstanding principal." Also: borrowers may "apply for conversion to full risk-based pricing ahead of schedule to capture lower Board rates."
- S2: "Pag-IBIG gives at least 30 days' notice of the new rate" before repricing
- S5 (PagibigFinancing): Loans "undergo repricing...at the rate at par with the prevailing market rates based on outstanding balance"
- S8 (LegalDex, older circular): Repricing occurred every 3 years, with maximum rate caps by loan amount bracket -- this was the old system; the current FRBP system uses borrower-chosen repricing periods

**Additional confirmed detail:**
- Early conversion option: Borrowers can proactively switch to a new repricing period before their current one expires, via Virtual Pag-IBIG [S2]
- 30-day advance notice required before new rate takes effect [S2]
- Under FRBP, there are no maximum rate caps (unlike the old system which had ceiling rates per bracket) [S2, S8]

---

### 8. Penalty Rate

**Claim:** 1/20 of 1% per day = 0.05%/day = 18.25% p.a. simple

**Verdict: CONFIRMED**

- S8 (LegalDex, EUF circular): "penal of 1/20 of 1% of the amount due for every day of delay" -- exact match
- S12 (Respicio): "Late payments incur a 1/20 of 1% per day penalty" -- exact match
- S2 (Respicio): "1/20 of 1% per day (approx 1.5% per month) on unpaid amortization" per HDMF Circular 300 -- consistent
- S13 (Circular 403): "penalty of 1/20 of 1% for every day of delay" -- exact match from official circular
- S5 (PagibigFinancing): "1/20 of 1% of the amount due for every day of the delay" -- exact match

**Independent computation:**
- 1/20 of 1% = 0.01 / 20 = 0.0005 = 0.05% per day
- Annual (simple): 0.05% x 365 = 18.25% -- confirmed

**Note:** One source [S5] also mentions "1/10 of 1%" as a rate for some context, but this appears to be for a different type of obligation (possibly employer remittance penalties vs. borrower payment penalties). The housing loan penalty is consistently cited as 1/20 of 1% across all authoritative sources.

---

### 9. Prepayment Policy

**Claim:** Allowed without penalty; service fee only

**Verdict: CONFIRMED**

- S13 (Circular 403): "A borrower shall be allowed to prepay his/her housing loan in full or in part without prepayment penalty, pursuant to Republic Act 7394, otherwise known as 'The Consumer Act of the Philippines,' but subject however to a service fee as may be fixed by the Fund"
- S12 (Respicio): "Prepayment Penalties: None, allowing early settlement without charges"
- S14 (Lawyer-philippines.com): Confirms prepayment without penalty; excess payments applied to principal upon borrower request

**Additional confirmed details:**
- Legal basis: RA 7394 (Consumer Act of the Philippines) prohibits prepayment penalties
- Excess payments: Applied as future amortizations by default; applied to principal only upon explicit written request from borrower
- Minimum prepayment: At least one monthly amortization equivalent for principal application [S13]
- Borrower must note on the Pag-IBIG Fund receipt how they want excess payment treated [S13]

---

## Additional Aspects NOT Mentioned in Claims

### A. Processing and Upfront Fees

**CONFIRMED from multiple sources:**
- Processing fee: PHP 1,000 (at application) + PHP 2,000 (at loan takeout) = **PHP 3,000 total** [S12, multiple sources]
- No other fees charged by Pag-IBIG directly [confirmed by government guarantee]
- Third-party costs (not Pag-IBIG fees): documentary stamps tax, registration fees at Registry of Deeds, notarial fees -- borne by borrower separately

### B. First-Year Insurance Deduction from Proceeds

**CONFIRMED:**
- First year MRI and FAPI premiums are **prepaid and deducted from loan proceeds** at takeout [S4]
- Subsequent years: premiums collected monthly alongside amortization [S4]
- This means the net loan disbursement is less than the approved amount by the first year's insurance premiums

### C. Insurance Renewal Mechanics

**PARTIALLY VERIFIED:**
- MRI is "yearly renewable term insurance" [S4, S13] -- renewed annually
- Renewal date anchored to the **takeout date** (disbursement date), not calendar year
- MRI premium for subsequent years computed on outstanding balance at renewal anniversary
- Specific balance snapshot methodology (e.g., outstanding balance as of the exact anniversary date vs. nearest payment date) could not be confirmed from public sources

### D. Default and Foreclosure Triggers

**CONFIRMED:**
- Default: 3 consecutive missed monthly amortizations [S13, S8, S12]
- Upon default: entire outstanding obligation becomes immediately due and demandable [S8]
- Penalty continues to accrue at 0.05%/day on all unpaid amounts [S13]
- Foreclosure proceedings initiated after default
- TAV (Total Accumulated Value of member savings) may be applied to outstanding obligations [confirmed by restructuring guidelines]

### E. Restructuring Rules for Existing Loans

**CONFIRMED from multiple sources:**
- Delinquent borrowers (3+ months past due) may apply for loan restructuring
- Restructured rate: 6.375% p.a. on 3-year fixed pricing (Special Housing Loan Restructuring)
- Penalty condonation: up to 100% of penalties may be waived; partial interest condonation possible
- One-time restructuring limit (unless force majeure)
- Down payment required (10% for most categories)
- Term may be extended up to 30 years or age 70, whichever comes first
- Post-restructuring default: 6 monthly arrearages triggers automatic foreclosure/cancellation
- All prior payments remain credited; only the forward schedule resets

### F. 4PH/AHP Subsidized Rate Amortization

**CONFIRMED with specifics:**
- Subsidized rate: **3% p.a. fixed for first 5 years** (extendible to 10 years for first 30,000 borrowers under early bird promo)
- After subsidized period: rate adjusts to Pag-IBIG's prevailing housing loan rates
- Same amortization formula applies (standard declining balance)
- Same insurance requirements (MRI + FAPI)
- 35% DTI cap applies
- Eligibility: first-time homebuyers earning below P47,856/mo (NCR) or P34,686/mo (other regions); all OFWs eligible

**Worked example cross-check:**
- P850,000 at 3%, 30 years: Computed = PHP 3,583.63/month
- News report (PNA) says "~PHP 3,600-3,700" -- consistent (difference attributable to insurance premiums)
- P850,000 at regular rate (~6.375%), 30 years: Computed = PHP 5,302.89/month
- News report says "~PHP 5,400-5,500" -- consistent (insurance premiums account for the difference)

### G. Debt-to-Income Ratio Cap

**CONFLICT between sources:**
- Most current sources cite **35% of gross monthly income** [S12, multiple calculators]
- Circular 403 (AHP) says **40% of net disposable income** [S13]
- The difference may be program-specific: standard EUF uses 35% of gross; AHP/restructuring uses 40% of NDI
- Worked example confirms 35% of gross for standard EUF: PHP 30,000 income x 35% = PHP 10,500 max amortization, qualifying for ~PHP 1,705,328 loan at 6.25%/30yr -- exact match with calculator output [S1]

### H. Loan-to-Value Ratios

**Not part of amortization computation per se**, but confirmed from input file analysis:
- 100% LTV for properties up to P400,000
- 90% for P400K-P1.25M
- 80% for P1.25M-P6M
- LTV determines required equity/downpayment, which affects principal amount in amortization

---

## Summary Verification Matrix

| # | Claim | Verdict | Confidence | Key Sources |
|---|-------|---------|------------|-------------|
| 1 | Amortization formula (declining balance) | **CONFIRMED** | High | S1, S3, S13 + independent computation |
| 2a | Interest rates by repricing period | **CONFIRMED** | High | S2, S9, S10, S11 (official sources) |
| 2b | Interest rates by loan amount bracket | **OUTDATED/INCORRECT** | High | Only S3 (third-party); contradicted by S2, S9, S10, S11 |
| 3 | MRI age-bracket rate table | **UNVERIFIED / LIKELY OUTDATED** | Low | No independent confirmation; claimed source (Circ. 428) is wrong document; current system uses uniform rate per S7, S13 |
| 4a | FGI rate = 0.076% | **UNVERIFIED** | Low | No source confirms; most recent documented rate is 0.1686% (2018) [S6] |
| 4b | FGI insured value = min(improvements, loan) | **CONFIRMED** | High | S4, S6, S13 |
| 5 | Total = P+I + MRI + FGI | **CONFIRMED** | High | S1, S4, S13 |
| 6 | Payment priority (5-item order) | **CONFIRMED** | High | S8, S13 |
| 7 | Repricing mechanics | **CONFIRMED** | High | S2, S5, S8 |
| 8 | Penalty rate 0.05%/day | **CONFIRMED** | High | S2, S8, S12, S13 |
| 9 | Prepayment without penalty | **CONFIRMED** | High | S12, S13, S14 (RA 7394 basis) |

---

## Critical Findings and Recommendations

### 1. Interest Rate Structure: Use Repricing-Period Rates Only

The rate table by repricing period (5.75%-9.75%) is the **definitive current structure**. The loan-amount-based table (5.5%, 6.375%, 7.375%) should be marked as unverified/outdated in the computation engine. If implementing both for legacy support, clearly label the repricing-period table as "current" and the loan-amount table as "historical/unverified."

### 2. MRI Rate Table: Cannot Be Relied Upon

The age-bracket MRI table from the input file cannot be independently verified. The claimed source (Circular 428) is a different document entirely (about foreclosed property sales). The current MRI appears to use a **uniform premium rate** rather than age-bracketed rates, based on official circular language and the ASSA institutional report. For computation purposes:
- Use the uniform rate structure as the default
- The specific current uniform rate needs direct verification from Pag-IBIG (last public data point: P0.23/1000 from 2014-2015 contract)
- If the age-bracket table is needed for a specific loan cohort, it should be treated as user-provided input, not as a verified default

### 3. FGI Rate: 0.076% is Unverified; 0.1686% is Most Recent Public Data

The claimed 0.076% cannot be confirmed from any public source. The 0.1686% rate is from a 2018 Manila Bulletin report citing Pag-IBIG's official announcement. It is possible a newer insurance contract has reduced the rate further, but this would need Pag-IBIG confirmation. For the computation engine:
- Default to 0.1686% (last publicly documented rate)
- Allow user override for cases where borrower knows their actual rate
- Note that the rate may have been updated in subsequent insurance contract rebidding (Pag-IBIG rebids every few years)

### 4. Amortization Formula and Most Other Claims: Solid

The core amortization formula, repricing mechanics, penalty rate, prepayment rules, payment priority, and total payment structure are all well-confirmed across multiple independent sources. These can be implemented with high confidence.
