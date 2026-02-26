# Bank Mortgage Amortization — Computation Extraction (Wave 2)

**Aspect:** bank-mortgage-amortization
**Date:** 2026-02-26
**Verification:** Cross-checked against 15+ independent sources (BSP circulars, practitioner calculators, bank product pages, legal commentaries, worked examples)
**Verification status:** CONFIRMED with qualifications (see each section)

---

## 1. Standard Amortization Formula

### Formula

```
M = P × [r × (1 + r)^n] / [(1 + r)^n − 1]

where:
  M = Monthly amortization (principal + interest combined)
  P = Principal loan amount (after downpayment)
  r = Monthly interest rate = Annual interest rate / 12
  n = Total number of monthly payments = Loan term in years × 12
```

**Equivalent form (used by some PH practitioners):**

```
M = P × r / [1 − (1 + r)^(−n)]
```

Both are algebraically identical. The second form is more commonly seen in Philippine practitioner guides and is the basis for amortization factor tables.

### Inputs

| Input | Type | Source |
|---|---|---|
| P — Principal loan amount | Currency (PHP) | Loan agreement (TCP minus downpayment) |
| Annual interest rate | Percentage | Loan agreement / bank offer sheet |
| Loan term | Integer (years) | Loan agreement (typically 5–30 years) |

### Output

| Output | Type |
|---|---|
| M — Monthly amortization | Currency (PHP) |

### Verification Status: CONFIRMED

| Source | Status | Notes |
|---|---|---|
| BSP Bank Loan Calculator (bsp.gov.ph/BankCalc.aspx) | Confirmed | BSP's own calculator uses this formula |
| ForeclosurePhilippines.com practitioner guide | Confirmed | Exact formula stated: "Amort factor = I / (1 − (1+I)^−M)" |
| Federal Land Inc. (federalland.ph) | Confirmed | Same formula documented for buyer computation |
| Lumina Homes guide (lumina.com.ph) | Confirmed | Step-by-step worked example matches formula output |
| PSBank Online Amortization Calculator | Confirmed | Calculator results match formula |
| REBAP (Real Estate Brokers Association of the Philippines) | Confirmed | Amortization calculator on rebap.com.ph uses same formula |
| OmniCalculator (used in pagibig-amortization verification) | Confirmed | Exact match to 2 decimal places |

**This is the ONLY method used by Philippine commercial banks for housing loan amortization.** No alternative formula was found in any source.

### Add-On Interest Prohibition: CONFIRMED

**Legal basis:** BSP Circular No. 730 (Series of 2011) — Updated Rules Implementing the Truth in Lending Act (RA 3765)

**Exact rule (from BSP FAQ on Circular 730):**
> "Are entities allowed to charge add-on interest to the principal? Can this be amortized on a straight-line method? **No.** Add-on interest and straight-line methods are prohibited. Interest and service charge directly attributable to the granting of credit shall be amortized using the effective interest method."

**Additional requirement:**
> "Banks may only charge interest based on the outstanding balance of a loan at the beginning of an interest period. For a loan where principal is payable in installments, interest per installment period shall be calculated based on the outstanding balance of the loan at the beginning of each installment period."

**Verification sources:**
1. BSP FAQ on Circular No. 730 (bsp.gov.ph/Regulations/FAQ/FAQ_TNT.pdf) — direct quote
2. RBAP-MABS commentary on Circular 730 — confirms prohibition
3. Respicio & Co. legal commentary — confirms prohibition applies to all bank loans
4. Studocu/CMU analysis of Circular 730 FAQs — confirms

**Note:** The prohibition applies to BSP-regulated entities (banks, quasi-banks, trust entities, lending companies, financing companies). Non-bank, non-BSP-regulated seller financing (e.g., developer in-house financing) is not explicitly covered by Circular 730, though RA 3765 (Truth in Lending Act) applies to all creditors.

### Deterministic: YES

Given principal, annual interest rate, and term, the monthly amortization is fully deterministic with no judgment required.

---

## 2. Repricing Formula

### New Rate Computation

```
New Interest Rate = Benchmark Rate + Bank Spread/Margin
```

### New Amortization After Repricing

```
New M = P_remaining × r_new / [1 − (1 + r_new)^(−n_remaining)]

where:
  P_remaining = Outstanding principal balance at repricing date
  r_new       = New monthly interest rate = New annual rate / 12
  n_remaining = Remaining months in loan term
```

### Inputs

| Input | Type | Source |
|---|---|---|
| P_remaining | Currency (PHP) | Bank statement / amortization schedule |
| New annual interest rate | Percentage | Bank notification (benchmark + spread) |
| Remaining term | Integer (months) | Original term minus elapsed months |

### Benchmark Rates Used by Philippine Banks

| Benchmark | Description | Who Uses It |
|---|---|---|
| PHP BVAL Reference Rates | Bloomberg Valuation-based government securities yield curve; replaced PDST-R in October 2018. Administered by Bankers Association of the Philippines (BAP). | Major commercial banks (post-2018 loan agreements) |
| 91-day Treasury Bill Rate | Government securities auction rate | Commonly referenced in older loan agreements |
| BSP Policy Rate (Overnight RRP Rate) | Currently 4.25% (Feb 2026) | Some banks; also indirect influence on all rates |
| PHIREF (Philippine Interbank Reference Rate) | Interbank offered rate | Referenced in some contracts |
| 3-month / 6-month government securities rates | Shorter-tenor reference rates | Bank-specific |

**Key finding:** There is NO single mandated benchmark. Each bank chooses its reference rate in the loan contract. The Supreme Court has ruled that repricing clauses must reference an **external, independently verifiable benchmark** — a clause allowing unilateral rate adjustment without reference to any standard violates the "mutuality of contracts" principle (Article 1308, Civil Code).

### Spread/Margin Determination

The spread is **not regulated**. It is set by each bank based on:
- Internal cost of funds
- Credit risk assessment of the borrower
- Competitive positioning
- Loan product type

**Typical implied spread:** Based on current data (BSP policy rate 4.25%, bank lending rate ~8.03%, housing loan rates 6%–8.78%), the implied bank spread for housing loans is approximately **1.5%–4.0%** above the policy rate.

### Legal Requirements for Repricing

1. **Written stipulation required** — Article 1956, Civil Code: "No interest shall be due unless it has been expressly stipulated in writing"
2. **Clear specification** — Loan documents must state how interest is calculated, including the specific benchmark and formula
3. **Written notice** — Banks must provide advance written notice before each repricing date
4. **Mutuality principle** — Rate cannot be set by absolute discretion of one party
5. **Unconscionability check** — Courts can void rates deemed excessive (Article 1229, Civil Code)

### Verification Status: CONFIRMED (formula) / QUALIFIED (benchmark selection)

| Source | Status | Notes |
|---|---|---|
| Respicio & Co. legal guide (lawyer-philippines.com) | Confirmed | Formula structure and legal constraints confirmed |
| BSP MORB / input file bsp-residential-lending.md | Confirmed | PDST-R/PHIREF/T-bill as benchmarks |
| PDS Group (pds.com.ph) | Confirmed | PHP BVAL Reference Rates are the current standard benchmark |
| Manila Standard (BAP statement) | Confirmed | BVAL methodology confirmed as IOSCO-compliant |
| Rebusel.com practitioner guide | Confirmed | Repricing intervals and fixed-to-variable transition described |
| Tsikot.com forum (practitioner discussion) | Confirmed | Real borrower experiences with 1-year vs 5-year repricing |

**Qualification:** The repricing formula itself is deterministic, but the new rate depends on (a) which benchmark the contract specifies, (b) the bank-determined spread, and (c) the benchmark rate value at the repricing date. All three are external data dependencies.

### Deterministic: PARTIALLY

The amortization recomputation is deterministic given the new rate. However, the new rate determination requires external data (benchmark value at repricing date) and a contractual parameter (spread), making the full repricing pipeline non-deterministic without access to the specific loan agreement and real-time benchmark data.

---

## 3. Early Termination / Prepayment Penalty

### Legal Framework

**Consumer Act (RA 7394), Article 137:**
> "The person to whom credit is extended may prepay in full or in part, at any time without penalty, the unpaid balance of any consumer credit transaction."

**BSP Regulation:**
Prepayment penalties are capped at **3% of the prepaid amount** for consumer loans under BSP prudential guidance.

### Actual Bank Practice: CONFLICT WITH COMMON CLAIM

The common claim of "2–3% of outstanding balance during fixed period, no penalty after" is an **oversimplification**. Actual practice varies significantly by bank:

| Bank | Pre-Termination Fee (Housing Loan) | Lock-In Period |
|---|---|---|
| **BDO** | No pre-termination fee; flat ₱3,500 processing fee. BUT: if promo with waived fees was availed, waived amounts (registration, DST, notarial, fire insurance) are **charged back** during 5-year lock-in period. | 5 years from loan release |
| **Metrobank** | Processing fee (₱5,000 for full payment prior to maturity) + reimbursement of all waived fees (mortgage registration, DST, notarial). During lock-in: borrower must also pay rate difference between board rate and promo rate. | Matches fixed-rate period (e.g., 5 years) |
| **BPI** | Historically ~4% of outstanding balance (per older third-party comparisons). Recent information suggests no prepayment penalty, but specific housing loan terms require direct confirmation. | Matches fixed-rate period |
| **UnionBank** | Personal loan: no penalty, only "Closure Handling Fee." Housing loan specifics not publicly available. | Not publicly documented |
| **Pag-IBIG** | **No prepayment penalty** (RA 7394 explicitly cited). No processing fee for partial or full prepayment. | None |

### Key Findings

1. **The "2–3% of outstanding balance" claim is NOT a standard industry rate.** Each bank sets its own terms.
2. **The Consumer Act technically prohibits prepayment penalties**, but banks circumvent this by:
   - Calling them "processing fees" rather than "penalties"
   - Structuring promo loans with waived fees that get "charged back" on early termination (clawback mechanism)
   - Charging a "break fund cost/fee" for early termination during the fixed-rate period
3. **After the fixed/lock-in period:** Most banks do not charge penalties or fees for prepayment. This part of the common claim is generally accurate.
4. **Pag-IBIG is the clear exception:** Truly penalty-free prepayment at any time.

### Verification Status: PARTIALLY CONFIRMED / CONFLICT

The common claim is directionally correct (penalties during fixed period, none after) but the specific "2–3% of outstanding balance" figure is NOT a standard rate. The actual mechanism is more complex (processing fee + clawback of waived fees + rate difference, varying by bank).

| Source | Status | Notes |
|---|---|---|
| Consumer Act RA 7394 Art. 137 | Confirmed | Prohibits prepayment penalties on consumer credit |
| BSP prudential guidance | Confirmed | 3% cap on prepayment penalties for bank loans |
| BDO loan terms (bdo.com.ph) | Confirmed | No pre-termination fee; ₱3,500 processing fee; clawback mechanism |
| Metrobank rates/fees page | Confirmed | ₱5,000 processing fee; clawback of waived fees during lock-in |
| Lamudi.com.ph Q&A | Confirmed | Describes "break fund cost/fee" concept |
| Respicio & Co. legal commentary | Confirmed | Consumer Act prohibition; lender workarounds documented |
| MoneySense.com.ph | Confirmed | Documents practice of "processing fees" as penalty substitute |
| Inquirer Business (2018 article) | Confirmed | Discusses lender workarounds for prepayment prohibition |

### Deterministic: PARTIALLY

Whether a penalty/fee applies: deterministic (check if within lock-in period). The amount: bank-specific, requires individual loan agreement terms, making it non-deterministic without the contract.

---

## 4. Capacity-to-Pay / DTI Rule

### The 35% Rule

**Common claim:** Monthly amortization must not exceed 35% of gross monthly income.

### Finding: NOT A BSP REGULATION — it is Pag-IBIG policy and bank practice

**Pag-IBIG:** The 35% of gross monthly income (GMI) threshold is a **Pag-IBIG Fund policy** (referenced in various Pag-IBIG circulars including Circular 402). Pag-IBIG also uses a 40% Net Disposable Income (NDI) test.

**BSP:** The BSP does **not** mandate a specific DTI percentage for housing loans. The BSP's Manual of Regulations for Banks (MORB) requires banks to have "sound credit risk management practices" (Circular 855) including capacity-to-pay assessment, but does not prescribe a specific DTI ratio.

**Bank practice:**
- Most commercial banks use **30%–40%** of gross monthly income as their internal DTI threshold
- Some banks use **Net Disposable Income (NDI)** rather than gross income: NDI = Gross Income − Statutory Deductions (SSS/GSIS, PhilHealth, Pag-IBIG contributions) − Existing Monthly Obligations
- Banks may apply **stress testing**: add +200–400 basis points to the projected repriced rate and check if DTI still passes under the stressed scenario
- The specific threshold varies by bank, borrower profile, and loan product

**No specific BSP circular number could be identified** that mandates 35% DTI for all banks. The claim that this is "BSP-mandated" appears to be a common misconception, likely stemming from:
1. Pag-IBIG's 35% GMI rule being attributed to BSP
2. The 30%–40% range being common enough to seem regulatory
3. BSP Circular 855's credit risk management requirements being interpreted as implying a specific threshold

### Formula (as practiced)

```
DTI Test (Gross Income Method):
  Monthly Amortization ≤ 35% × Gross Monthly Income

DTI Test (Net Disposable Income Method):
  Monthly Amortization ≤ 40% × NDI
  where NDI = Gross Monthly Income − SSS/GSIS − PhilHealth − Pag-IBIG − Existing Monthly Obligations

Maximum Loanable Amount (working backward):
  Max Amortization = Threshold% × Income Metric
  Max P = Max Amortization × [(1+r)^n − 1] / [r × (1+r)^n]
```

### Verification Status: PARTIALLY CONFIRMED / QUALIFIED

| Source | Claim | Finding |
|---|---|---|
| ForeclosurePhilippines.com mortgage calculator | 35% GMI | Confirmed — uses 35% as default |
| Pag-IBIG circulars | 35% GMI | Confirmed — Pag-IBIG policy |
| Respicio & Co. legal guide | 30%–40% range | Confirmed — bank-specific, not BSP-mandated |
| Tonik Bank DTI guide | 30% or lower recommended | Confirmed — general guidance, not regulatory mandate |
| FinScore.ph DTI guide | 30%–40% healthy range | Confirmed — industry practice |
| BSP Circular 855 | Sound credit risk management | Confirmed — no specific DTI percentage mandated |

### Deterministic: YES (given the bank's DTI threshold)

The pass/fail test is deterministic given: gross income, existing obligations, statutory deductions, and the bank's DTI threshold percentage.

---

## 5. LTV Limits

### BSP Circular 688 (Series of 2010)

**Status:** Circular 688 exists (PDF at bsp.gov.ph/Regulations/Issuances/2010/c688.pdf). However, the full text was not accessible via web search (scanned PDF). Based on the Wave 1 input file and multiple secondary sources:

**Claimed LTV caps under Circular 688:**
- 60% for non-residential (commercial) real estate loans
- 80% for residential real estate loans secured by the financed property

**CRITICAL CLARIFICATION — BSP Circular 855 (2014) supersedes the collateral treatment:**

The 60% figure most commonly cited is from **Circular 855 (2014)**, which caps the **collateral value** of real estate at 60% of appraised value for loan classification and provisioning purposes. This is NOT the same as an LTV limit.

**From BSP FAQ on Circular 855:**
> "The cap on REM collateral value is not the same as a loan-to-value ratio limit imposed in some jurisdictions for real estate lending, which is synonymous to a minimum borrower equity requirement."
> "Under both existing and revised rules, the minimum borrower equity requirement is bank-determined internal policy."
> "Current industry practice is a minimum equity requirement reportedly averaging around 20 percent."
> "This [circular] will not preclude FIs from granting loans with loan to collateral value ratios in excess of 60% as long as the FI has determined that the borrower has the capacity."

### Actual Practice vs. Regulatory Limits

| Scenario | Regulatory Treatment | Actual Bank Practice |
|---|---|---|
| Primary residence, top-tier developer | 60% collateral value for classification | Banks lend up to **90%** LTV |
| Primary residence, standard | 60% collateral value for classification | Banks lend up to **80%** LTV |
| Condo (own occupancy) | 60% collateral value for classification | Banks lend **60–80%** LTV |
| Vacant lot | 60% collateral value for classification | Banks lend up to **60%** LTV |
| Non-residential/commercial | 60% collateral value for classification | Banks lend up to **60%** LTV |
| BDO foreclosed properties | Internal policy | Requires **40% equity** (60% LTV) |
| Pag-IBIG housing loan | Separate regulatory framework | LTV up to **100%** (retail, lowest tier) |

### Key Takeaway

The Philippines does **not impose a hard regulatory LTV cap** in the way many Asian jurisdictions (Singapore, Hong Kong, South Korea) do. The 60% figure is a **prudential collateral valuation rule** for bank regulatory reporting, not a lending restriction. Banks that lend above 60% simply face higher provisioning requirements for the unsecured portion.

### Verification Status: CONFIRMED (with important nuance)

| Source | Status | Notes |
|---|---|---|
| BSP FAQ on Circular 855 (bsp.gov.ph) | Confirmed | 60% is collateral cap, NOT LTV limit |
| ForeclosurePhilippines.com analysis | Confirmed | Banks still lend 80%+; 60% is misunderstood |
| MORB Section 303 | Confirmed | Collateral valuation rules |
| BIS Paper No. 110 (bis.org) | Confirmed | Philippines LTV policy discussed in context of macroprudential tools |
| General Banking Act Sec. 37 | Reference | Statutory max: 75% of RE security + 60% of insured improvements |

### Deterministic: YES

LTV computation is deterministic: `Max Loan = LTV% × min(Appraised Value, Selling Price)`. The LTV percentage itself is bank-determined policy (not a single regulatory number), creating an external parameter dependency.

---

## 6. Amortization Factor Tables

### What They Are

Pre-computed lookup tables where:
```
Monthly Amortization = Loan Amount × Amortization Factor
```

### How Factors Are Computed

The amortization factor IS the standard formula expressed as a per-peso multiplier:

```
Amortization Factor = r / [1 − (1 + r)^(−n)]

where:
  r = Annual interest rate / 12 (monthly rate)
  n = Loan term in years × 12 (total months)
```

This is mathematically identical to dividing the standard amortization formula by P (the principal):
```
Factor = M / P = [r × (1 + r)^n] / [(1 + r)^n − 1]
```

**They are NOT a separate calculation method.** They are pre-computed values of the standard diminishing balance formula, expressed as a multiplier per peso of principal.

### Table Structure

Typical PH amortization factor tables have:
- **Columns:** Annual interest rates (1% to 20%, in 0.25% or 0.5% increments)
- **Rows:** Loan terms (1 to 30 years)
- **Cell values:** The factor (typically 7–10 decimal places)

### Example (verified)

For a 20-year term at 7% annual interest:
- Monthly rate r = 7% / 12 = 0.005833...
- n = 20 × 12 = 240 months
- Factor = 0.005833 / [1 − (1.005833)^(−240)] = **0.007753**
- For a ₱3,000,000 loan: 3,000,000 × 0.007753 = **₱23,259**

### Pag-IBIG Variation

Pag-IBIG factor tables are sometimes expressed per ₱1,000 of loan amount:
```
Monthly Amortization = (Loan Amount × Factor) / 1,000
```
Example: Factor of 7.32719 for 30-year term → M = 880,000 × 7.32719 / 1,000 = ₱6,448

### Are They Still Commonly Used?

**Yes.** Multiple sources confirm continued widespread use:

1. **ForeclosurePhilippines.com** — maintains full factor tables (1%–20%, 1–30 years) with online calculator
2. **BahayCentral.com** — publishes factor rate tables including Pag-IBIG-specific rates
3. **Real estate seminars** — Urban Institute of Real Estate (Engr. Enrico Cruz) teaches factor method
4. **Practitioner workflow** — brokers carry printed factor tables for quick field computations
5. **REBAP** — Real Estate Brokers Association of the Philippines provides factor-based calculator

**Why they persist:** Before ubiquitous smartphone calculators, computing `(1+r)^n` in the field was impractical. The factor table reduced mortgage estimation to a single multiplication. Even now, factors remain convenient for quick mental estimates and are embedded in broker training materials.

### Verification Status: CONFIRMED

| Source | Status | Notes |
|---|---|---|
| ForeclosurePhilippines.com factor table | Confirmed | Formula stated, tables published, examples verified |
| ForeclosurePhilippines.com "how to calculate" guide | Confirmed | Exact formula: Amort factor = I / (1 − (1+I)^−M) |
| BahayCentral.com | Confirmed | Factor tables including Pag-IBIG rates |
| Federal Land Inc. (federalland.ph) | Confirmed | Factor method documented |
| PhilippineProperties101.com (Pag-IBIG guide) | Confirmed | Per-₱1,000 factor variant documented |
| REBAP amortization calculator | Confirmed | Factor-based computation |

### Deterministic: YES

Factor computation is purely mathematical — same formula as standard amortization, just pre-computed and tabulated.

---

## Edge Cases and Special Rules

### 1. Leap Year / Day Count
Philippine bank mortgages use a **30/360 day count convention** (i.e., monthly rate = annual rate / 12, regardless of actual days in month). No adjustment for leap years.

### 2. First Payment Date
First amortization is typically due **one month after loan release date**. Interest accrual starts from release date. If release is mid-month, the first payment may include a "broken period" interest adjustment.

### 3. Principal vs. Interest Split Per Month
Within each constant monthly payment M:
```
Interest portion = Outstanding balance × r
Principal portion = M − Interest portion
New balance = Outstanding balance − Principal portion
```
Early payments are interest-heavy; later payments are principal-heavy (standard amortization characteristic).

### 4. Rounding
Philippine bank systems round monthly amortization to **two decimal places (centavo precision)**. The final payment may be adjusted slightly to zero out the balance exactly.

### 5. Insurance Premiums
MRI (Mortgage Redemption Insurance) and fire/hazard insurance are **NOT included** in the standard amortization formula. They are either:
- Deducted from loan proceeds at disbursement (Pag-IBIG first-year practice)
- Billed separately on an annual basis (most commercial banks)
- Added on top of the monthly amortization as a separate line item

### 6. Multiple Fixed-Rate Periods
Some banks offer "step-up" or "graduated" rate structures (e.g., BPI Step-Up PayPlan) where the fixed rate changes at predetermined intervals even before repricing. Each rate change triggers a recalculation using the repricing formula on the remaining balance.

---

## Legal Citations Summary

| Regulation | Relevance |
|---|---|
| **BSP Circular 730 (2011)** | Prohibits add-on interest; mandates diminishing balance; requires EIR disclosure |
| **RA 3765 (Truth in Lending Act, 1963)** | Requires full disclosure of credit terms to borrowers |
| **BSP Circular 855 (2014)** | 60% collateral valuation cap (for classification, NOT lending limit) |
| **BSP Circular 688 (2010)** | Introduced macroprudential LTV monitoring (text not fully accessible) |
| **RA 7394 (Consumer Act), Art. 137** | Prohibits prepayment penalties on consumer credit transactions |
| **Civil Code Art. 1308** | Mutuality of contracts — repricing cannot be unilateral |
| **Civil Code Art. 1956** | Interest must be expressly stipulated in writing |
| **Civil Code Art. 1229** | Courts may reduce unconscionable penalties/interest |
| **BSP Circular 799 (2013)** | Default legal interest rate = 6% per annum |
| **General Banking Act (RA 8791), Sec. 37** | Statutory RE loan cap: 75% of RE value + 60% of insured improvements |
| **Pag-IBIG Circular 402** | 35% GMI capacity-to-pay test (Pag-IBIG, not BSP) |

---

## 7. Bank-Specific Rate Schedules (2025-2026)

This section documents the actual interest rate schedules offered by major Philippine commercial banks, sourced from official bank websites and comparison platforms in February 2026.

### 7.1 BPI (Bank of the Philippine Islands)

**Source:** BPI official website (bpi.com.ph/personal/loans/housing-loan/buy), fetched February 2026

| Fixing Period | Rate p.a. (new applications) |
|---------------|------------------------------|
| 1 year | 7.00% |
| 2 years | 7.25% |
| 3 years | 7.75% |
| 4 years | 8.00% |
| 5 years | 8.00% |
| 10 years | 10.25% |
| 15 years | 10.50% |
| 20 years | 12.00% |

**Key terms:**
- LTV: Up to 90% (house & lot), 60% (vacant lot/condo)
- Loan term: 1-20 years (house & lot), max 10 years (vacant lot/condo)
- Minimum loan: PHP 400,000
- Minimum household income: PHP 40,000/month
- Down payment: as low as 10%
- Age: 18-70 at maturity

**Promo (valid through mid-2025):** "5678" -- 6.7% for 5-year fixing, up to PHP 80,000 in fees waived

**Fees:**
- Processing and handling fee: PHP 10,000
- Appraisal fee: PHP 5,000 (inclusive of title verification)
- Notarial fee: PHP 1,300
- DST: PHP 1.50 per PHP 200 of loan amount (~0.75%)
- Group Financial Security Plan (MRI): varies by age and loan amount
- Fire insurance: varies
- BPI offers "All-In Financing" that rolls bank fees into the loan amount

### 7.2 BDO Unibank

**Source:** BDO official website (bdo.com.ph/personal/loans/home-loan/interest-rate), rate sheet PDF, MoneySense

| Fixing Period | Rate p.a. (existing clients) | Rate p.a. (new clients) |
|---------------|------------------------------|------------------------|
| 1 year | ~6.75% | ~7.00% |
| 2 years | ~7.00% | ~7.25% |
| 3 years | ~7.50% | ~7.75% |
| 5 years | ~8.00% | ~8.25% |
| 10 years | Available | Available |

*BDO distinguishes rates for existing vs. new clients, with existing clients receiving lower rates.*

**Key terms:**
- LTV: Up to 80% of appraised value
- Loan term: up to 25 years
- Grace period option: 60-day grace OR interest-only for first 6 months

**Repricing formula (specific to BDO, from official rate sheet):**
```
New rate = HIGHEST of:
  (1) Latest awarded 364-day Treasury Bill 1-year Reference Rate + 4.00%
  (2) Latest available 1-year BVAL rate or Benchmark Rate + 3.00%
  (3) Board Rate at time of repricing
```

**BDO Fees:**
- Appraisal: PHP 5,000 (within 30km), PHP 5,500 (outside 30km)
- Handling fee: PHP 3,000
- Notarial fee: PHP 100-200 per document
- DST: ~0.75% of loan amount
- CLI premium: PHP 4.75 per PHP 1,000 of loan (ages up to 49); PHP 6.50 per PHP 1,000 (ages 50-69)
- Fire insurance: variable, based on appraised value of improvements
- Pre-termination processing fee: PHP 3,500

**Promo (Jan 15 - Mar 31, 2026):** Low rates, waived fees, free fire insurance. 5-year lock-in; pre-termination triggers chargeback of waived fees and fire insurance premium.

### 7.3 Metrobank

**Source:** Metrobank official rates page (metrobank.com.ph/articles/loan-rates-and-fees), fetched February 2026. Rates effective as of June 26, 2025.

| Fixing Period | Rate p.a. |
|---------------|-----------|
| 1 year | 6.25% |
| 2 years | 7.25% |
| 3 years | 7.75% |
| 4 years | 8.00% |
| 5 years | 8.25% |

*Additional 1% for Home Equity products.*

**Key terms:**
- LTV: 70-80% of evaluated value
- Loan term: up to 25 years (house & lot), 20 years (renovation), 15 years (refinancing/OFWs), 10 years (vacant lot)
- Minimum loan: PHP 500,000
- Minimum income: PHP 40,000/month
- Payment: strictly via ADA (Automatic Debit Arrangement)

**Metrobank Fees:**
- Handling fee: PHP 5,000
- Takeout/refinancing processing: PHP 15,000
- Appraisal (in-town): PHP 4,000; (out-of-town): PHP 4,500; re-appraisal: PHP 2,000
- Notarial: PHP 400 per document (notarized); PHP 300 (non-notarized)
- Late penalty: 3% per month
- Full prepayment processing: PHP 5,000
- Collateral modifications: PHP 5,000

**Promos:** "Goals Made Real" (2025): 6.75% with up to PHP 60,000 in waived fees. Later promo: 6.50% with up to PHP 100,000 waived.

### 7.4 RCBC

**Source:** RCBC official website (rcbc.com/home-loans), comparison sites

| Fixing Period | Rate p.a. (indicative) |
|---------------|----------------------|
| 1 year | ~6.38% |
| 2-3 years | ~6.50% |
| 5 years | ~6.50-7.00% (promo dependent) |

**Key terms:**
- LTV: up to 80% of appraised value
- Loan term: up to 20 years
- Minimum loan: PHP 300,000 (construction/renovation), PHP 1,000,000 (purchase)
- Fixing options: 1 year up to 20 years
- Approval: as fast as 3 days

**Promos (2025-2026):**
- "Home for the Holidays" (Nov 2025 - Jan 2026): 6.5% fixed 1-5 yr (Tier 1-2 developers); 7.0% (Tier 3-4)
- Online promo: as low as 5.25% fixed 1-5 yr (with 5-year lock-in)
- "Home Loan Switch" (refinancing, Sep 2025 - Aug 2026): 8% fixed 5 yr

### 7.5 Security Bank

**Source:** Security Bank official website (securitybank.com), PhilNews

| Fixing Period | Rate p.a. |
|---------------|-----------|
| 1 year | Starting at 6.50-7.00% |
| 3 years | ~8.25% (from comparison sources) |
| 5 years | ~6.75-6.80% (promo rate; board rate likely higher) |

**Key terms:**
- LTV: up to 90% selling price (top-tier developer primary), 80% appraised (individual seller), 60% (investment/equity/vacant lot)
- Loan term: max 25 years (house & lot), 20 years (townhouse/duplex/condo), 15 years (vacant lot)
- Minimum loan: PHP 1,000,000
- Minimum joint gross monthly income: PHP 50,000
- Maximum loan: PHP 20,000,000
- Other fees: estimated 2.5-3% of approved loan amount

### 7.6 UnionBank

**Source:** UnionBank website (unionbankph.com/homeloan), comparison sites

| Fixing Period | Rate p.a. (indicative) |
|---------------|----------------------|
| 1 year | ~6.75% |
| 1-5 years | 6.0-11.0% range |

**Key terms:**
- LTV: up to 99% of property value (highest in Philippine market)
- Loan term: up to 20 years
- Minimum loan: PHP 200,000
- 100% digital application; AI-driven evaluation
- Accredited developers: Avida, Ayala, Camella, Filinvest, Megaworld, SMDC

### 7.7 Chinabank (China Banking Corporation)

**Source:** Chinabank website (chinabank.ph/loans-homeplus), EasyPropertyMatch comparison

| Fixing Period | Rate p.a. (from comparison sources) |
|---------------|--------------------------------------|
| 3 years | ~7.50% |
| 5 years | ~8.00% |

*Rates not publicly listed on website; provided upon application.*

**Key terms:**
- Rate fixing options: 1, 3, 5 years
- Terms: vacant lot/renovation/refinancing up to 10 yr; condo up to 15 yr; house & lot up to 20 yr
- Payment via ADA on Chinabank account

### 7.8 PSBank

**Source:** EasyPropertyMatch comparison table

| Fixing Period | Rate p.a. |
|---------------|-----------|
| 3 years | 7.25% |
| 5 years | 7.50% |
| 10 years | 9.25% |
| 15 years | 10.00% |
| 20 years | 10.50% |

### 7.9 Consolidated Rate Comparison (Board/Regular Rates)

| Bank | 1-yr Fixed | 3-yr Fixed | 5-yr Fixed | 10-yr Fixed | Max Term | Max LTV |
|------|-----------|-----------|-----------|------------|----------|---------|
| **BPI** | 7.00% | 7.75% | 8.00% | 10.25% | 20 yr | 90% |
| **BDO** | ~7.00% | ~7.75% | ~8.25% | Available | 25 yr | 80% |
| **Metrobank** | 6.25% | 7.75% | 8.25% | N/A | 25 yr | 80% |
| **RCBC** | ~6.38% | ~6.50% | ~6.50-7.00% | N/A | 20 yr | 80% |
| **Security Bank** | ~7.00% | ~8.25% | ~6.75%* | N/A | 25 yr | 90%** |
| **UnionBank** | ~6.75% | N/A | N/A | N/A | 20 yr | 99% |
| **Chinabank** | N/A | ~7.50% | ~8.00% | N/A | 20 yr | N/A |
| **PSBank** | N/A | 7.25% | 7.50% | 9.25% | 20 yr | N/A |

*Security Bank 5-yr rate is promo; board rate likely higher
**90% only for primary acquisition from top-tier developers

**Market context:** Despite BSP cutting rates by 225 bps (from 6.50% to 4.25% between Aug 2024 and Feb 2026), housing loan rates remain "sticky" at 6-8%+ (Bloomberg, Nov 2025).

---

## 8. Mortgage Redemption Insurance (MRI) / Credit Life Insurance (CLI)

### 8.1 Requirement
MRI is **mandatory** for all Philippine housing loans. It is a term life insurance naming the bank as beneficiary. Upon borrower death or total permanent disability, the insurer pays off the remaining loan balance.

### 8.2 Types
1. **Declining MRI** -- coverage decreases as loan balance decreases; lower premiums
2. **Level MRI** -- coverage remains at original loan amount throughout; higher premiums

### 8.3 Bank-Specific Rates

**BDO (documented):**
```
Annual CLI = (loan_amount / 1,000) * rate_per_1000

Rate per PHP 1,000:
  Ages up to 49:   PHP 4.75 (annualized: 0.475% of loan)
  Ages 50 to 69:   PHP 6.50 (annualized: 0.650% of loan)
```
BDO offers "Built-In Insurance" (BII): annual premium split into 12 monthly installments at 0% interest.

**Other banks:** Premium rates are generally not publicly listed. Factors: borrower age, loan amount, insurer.

**Comparison with Pag-IBIG:**
| Feature | Commercial Bank CLI/MRI | Pag-IBIG MRI |
|---------|----------------------|-------------|
| Documented rate | PHP 4.75-6.50/PHP 1,000 (BDO) | PHP 0.23/PHP 1,000 (uniform) |
| Annualized | 0.475%-0.650% | 0.023% |
| Payment | Annual lump sum or monthly BII | Monthly as part of amortization |
| Age factor | Yes (50+ pays more) | Unclear (conflict: uniform vs. age-bracket) |

Commercial bank MRI premiums are approximately **20-28x higher** than Pag-IBIG's documented rate.

### 8.4 MRI Alternatives
Borrowers may substitute an existing life insurance policy (assigned to bank as beneficiary) if coverage is sufficient per the loan amount. Providers like Pru Life UK and Sun Life offer assignable policies.

---

## 9. Effective Interest Rate (EIR) Computation

### 9.1 BSP Circular 730 Requirement
All lenders must compute and disclose the EIR, defined as:
> "The rate that exactly discounts estimated future cash flows through the life of the loan to the net amount of loan proceeds." (per Philippine Accounting Standards)

### 9.2 What Is Included in EIR
**Finance charge** includes ALL of:
- Nominal interest
- Processing/handling fees
- Service charges
- Appraisal fees
- Any other charges incident to credit extension

EIR is always >= nominal rate because upfront fees reduce net proceeds.

### 9.3 EIR Computation Formula
The EIR is the rate `i` that solves:
```
Net_Proceeds = sum(Payment_k / (1 + i)^k for k = 1..n)

Where:
  Net_Proceeds = loan_amount - all_upfront_fees_deducted
  Payment_k    = monthly payment for month k
  i            = monthly EIR (annualize: EIR_annual = (1 + i)^12 - 1)
```

This is the IRR (Internal Rate of Return) of the borrower's cash flow series.

### 9.4 EIR Disclosure Requirements
- Must appear in loan disclosure statement
- Must appear in loan amortization schedule
- Must appear in marketing materials
- Must be consistent across all loan documents
- May be quoted annually (term > 1 year) or monthly (term <= 1 year)

### 9.5 Worked Example
Scenario: PHP 3,000,000 loan, 6.25% nominal, 25 years, PHP 30,000 upfront fees deducted.
```
Net proceeds: PHP 2,970,000
Monthly P+I at 6.25%: PHP 19,821.89
Solving for monthly EIR: i_monthly ~= 0.5260%
EIR_annual = (1.005260)^12 - 1 = 6.494%
```
EIR (6.494%) exceeds nominal rate (6.25%) due to upfront fees.

---

## 10. Processing Fees Comparison

| Fee | BPI | BDO | Metrobank |
|-----|-----|-----|-----------|
| **Processing/handling** | PHP 10,000 | PHP 3,000 | PHP 5,000 + PHP 15,000 (takeout) |
| **Appraisal** | PHP 5,000 | PHP 5,000-5,500 | PHP 4,000-4,500 |
| **Notarial** | PHP 1,300 | PHP 100-200/doc | PHP 400/doc |
| **DST on mortgage** | ~0.75% of loan | ~0.75% of loan | ~0.75% of loan |
| **CLI/MRI (annual)** | Varies | 0.475%-0.650% | Varies |
| **Fire insurance** | Varies | Varies | Varies |
| **Late penalty** | Not published | Not published | 3%/month |
| **Pre-termination** | Not published | PHP 3,500 | PHP 5,000 |

Fees are NOT standardized across banks. DST is the only statutory (uniform) charge.

Fee waiver promos are a major competitive tool: BPI waives up to PHP 80,000; Metrobank up to PHP 60,000-100,000; BDO waives fees + free fire insurance.

---

## 11. BSP Policy Rate Context (February 2026)

- BSP target reverse repurchase rate: **4.25%** (after 25 bps cut on Feb 19, 2026)
- Total easing since August 2024: **225 basis points** (from 6.50% to 4.25%)
- Metrobank Research projects terminal rate of **4.00%** by end-2026
- Philippine economy grew 4.4% in 2025 (below expectations)
- Housing loan rates remain "sticky" at 6-8%+ despite aggressive easing

---

## Summary of Verification Results

| Computation | Claim | Verdict | Key Qualification |
|---|---|---|---|
| Standard amortization formula | M = P × r(1+r)^n / [(1+r)^n − 1] | **CONFIRMED** | Only method used; add-on interest prohibited by BSP Circular 730 |
| Repricing formula | New Rate = Benchmark + Spread; recompute M on remaining balance | **CONFIRMED** | No single mandated benchmark; bank chooses reference rate in contract (BVAL, T-bill, BSP RRP) |
| Early termination penalty | 2–3% of outstanding balance during fixed period | **PARTIALLY CONFIRMED** | Oversimplified; actual mechanism is processing fee + clawback of waived fees, varies by bank; Consumer Act technically prohibits penalties |
| 35% DTI rule | BSP regulation | **PARTIALLY CONFIRMED / CORRECTED** | 35% is Pag-IBIG policy, NOT a BSP regulation; BSP requires capacity assessment but does not mandate specific DTI %; banks use 30%–40% range |
| LTV limits (Circular 688: 60%/80%) | Hard regulatory caps | **CORRECTED** | 60% is Circular 855 collateral valuation cap for classification, not a lending cap; banks lend up to 90% in practice; no hard LTV cap exists |
| Amortization factor tables | Pre-computed values of standard formula | **CONFIRMED** | Factor = r / [1 − (1+r)^(−n)]; still widely used by PH practitioners; mathematically identical to standard formula |
