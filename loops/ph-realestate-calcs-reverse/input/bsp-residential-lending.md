# BSP Residential Real Estate Lending — Regulatory Source

**Fetched:** 2026-02-25
**Primary source:** BSP Manual of Regulations for Banks (MORB), BSP Circulars
**Key sections:** MORB Section 363-A, Section 303, Appendix 36; Circular 855, 688, 799, 730

---

## 1. Real Estate Loan (REL) Portfolio Limit — MORB Section 363-A

**Rule:** Real estate loans of universal banks (UBs) and commercial banks (KBs) must not exceed **25% of total loan portfolio**, net of interbank loans.
(Raised from 20% to 25% in August 2020 — Circular raising authorized by Monetary Board.)

**Definition of "real estate loans" for REL limit purposes:**
- Loans to land developers, construction companies, other borrowers for:
  - Land acquisition and development
  - Building/structure construction (including housing for sale/lease)
  - Income-generating purposes
- Purchases of receivables from real estate developers (with recourse)

**Excluded from the 25% REL limit:**
1. Loans to individual households for acquisition, construction, or improvement of housing units **for own occupancy** (regardless of amount)
2. Loans to developers for **socialized and low-cost residential properties** under government housing programs (HUDCC)
3. Loans guaranteed by the **Philippine Guarantee Corporation (PGC, formerly HGC)**
4. Loans collateralized by non-risk assets (cash, government securities, deposits)
5. Loans to finance **infrastructure projects for public use** (highways, bridges, ports, airports, power plants, water systems, telecom/IT networks, government buildings)

**Coverage:** UBs and KBs only.
Thrift banks, rural banks, and cooperative banks are **not subject** to the 25% portfolio limit (their traditional market includes residential real estate lending).

---

## 2. Real Estate Stress Test (REST) — MORB Section 363-A(b)

**Methodology:** Assume a **25% write-off rate** on the bank's real estate exposures (REEs) and other real estate property (OREO). Stress-test the resulting capital position against prudential limits.

**REST prudential limits (must be maintained at all times):**
- Common Equity Tier I (CET1) capital ratio: **≥ 6%** (UBs/KBs and their subsidiary thrift banks)
- Risk-based Capital Adequacy Ratio (CAR): **≥ 10%** (all covered banks)
- Applies on solo and consolidated basis.

**Exclusions from REST computation (revised methodology):**
- Residential real estate loans to individuals for **own occupancy** are excluded
- Foreclosed real estate property is excluded

**REST scope — what counts as "real estate exposure":**
- Commercial real estate loans
- Loans to land developers and real estate entities
- Debt securities and equity investments in real estate companies

---

## 3. Collateral Valuation Rules — MORB Section 303 (Circular 855, 2014)

**Rule:** Maximum collateral value of real estate mortgage (REM) for classification/provisioning purposes = **60% of appraised value** (BSP Circular 855, October 29, 2014).

**Practical effect:** This collateral cap determines whether a loan is classified as "secured" or "unsecured" for regulatory reporting and provisioning. It does NOT cap the LTV ratio for loan origination.

**Lending above 60% is permitted:** Banks may grant loans with LTV ratios exceeding 60% provided the bank has determined the borrower has capacity and willingness to pay. Non-performing loans will not be reclassified solely due to the collateral cap — classification depends on loan performance, not collateral coverage.

**Appraisal requirements:**
- Appraisal by an **independent appraisal company acceptable to BSP**
- Reappraised every year after restructuring
- Independent appraisal thresholds:
  - Commercial banks: loans **> ₱5 million**
  - Thrift banks: loans **> ₱1 million**
  - Rural banks: loans **> ₱500,000**
- Appraisal must use the **Market Data / Sales Comparison approach** for determining market value

---

## 4. LTV Ratio Limits — Computation

**LTV formula:**
```
LTV Ratio = Loan Amount ÷ Appraised Value × 100
Maximum Loanable Amount = LTV% × min(Appraised Value, Selling Price)
```

**Key rule:** Always base loanable amount on the **lower of appraised value or selling price**.

**Market practice LTV limits by property type (commercial banks, 2023–2024):**

| Property Type | Purpose | LTV Limit |
|---|---|---|
| House and lot | Primary residence from top-tier developer | Up to 90% of selling price |
| House and lot | Primary from individual seller / non-top-tier developer | Up to 80% of appraised value |
| Residential condo | Own occupancy | Up to 60–80% |
| Vacant lot | Any | Up to 60% |
| Investment/secondary home | Any | Up to 60% |
| Home equity loan | Any | Up to 60% |

**Computation example:**
- Property selling price: ₱5,000,000
- BSP appraisal: ₱4,500,000
- LTV applies to: ₱4,500,000 (lower)
- At 80% LTV → Maximum loan = ₱3,600,000

**BSP Circular 688 (Series of 2010):** Introduced macroprudential LTV ceilings. Known provisions (text not directly accessible — scanned PDF):
- 60% LTV for **non-residential (commercial)** real estate loans
- 80% LTV for **residential** real estate loans secured by the financed property
(These are the original regulatory caps; actual bank practice and Pag-IBIG programs may exceed these for specific housing tiers.)

**Rediscounting cap (MORB Appendix 36):** Total cumulative BSP rediscounting availments against a mortgaged property shall not exceed **80% of collateral value**.

---

## 5. Bank Mortgage Repricing — Computation Rules

**Fixed-rate period:** Rate is locked for initial term (common: 1, 3, 5, 10 years). After this period, the loan is **repriced**.

**Repricing formula:**
```
New Interest Rate = Benchmark Rate + Bank Spread/Margin
```

**Benchmark reference rates:**
- Philippine Dealing System Treasury Reference Rate (PDST-R / PHIREF)
- 91-day Treasury bill rate
- BSP policy rate (Target Reverse Repurchase Rate)
- 3-month or 6-month government securities rates

**After repricing — recomputing amortization:**
```
New Monthly Amortization = P_remaining × r_new / [1 − (1 + r_new)^−n_remaining]
where:
  P_remaining = outstanding loan balance at repricing date
  r_new       = new monthly interest rate (new annual rate ÷ 12)
  n_remaining = remaining months in loan term
```

**Legal constraints on repricing (BSP Circulars 730, 754; Civil Code):**
- Repricing method must be clearly stated in the contract
- Cannot be left to **absolute discretion** of lender alone — must reference an external benchmark
- Rates deemed "unconscionable or patently excessive" may be judicially reduced (Article 1229, Civil Code)
- Banks must provide **written notice to borrowers** before each repricing date
- Early termination/refinancing typically subject to a **2–3% break fee**

**Common repricing periods and rate structure (higher fixed rate for longer certainty):**
- 1-year repricing: lowest initial rate (e.g., Pag-IBIG 5.75% as of 2026)
- 3-year repricing: mid-tier rate (e.g., Pag-IBIG 7.25%)
- 5-year repricing: higher rate
- 30-year fixed: highest rate (e.g., Pag-IBIG 9.75%)

---

## 6. Monthly Amortization Formula (Standard)

```
M = P × [r × (1 + r)^n] / [(1 + r)^n − 1]
where:
  M = Monthly amortization
  P = Principal loan amount
  r = Monthly interest rate = Annual rate ÷ 12
  n = Total number of monthly payments = Years × 12
```

**Alternative (amortization factor method):** Many Philippine practitioners use a lookup table of amortization factor rates. Monthly payment = P × factor, where factors are pre-computed per interest rate and term.

**Add-on interest is prohibited** (BSP Truth-in-Lending regulations). Only declining balance (actuarial) method is allowed.

---

## 7. Capacity-to-Pay Test

**Standard rule (BSP prudential guidance / Pag-IBIG Circular 402):**
- Monthly amortization must not exceed **35% of gross monthly income**
- Some banks apply Net Disposable Income (NDI) metric: net of statutory deductions (SSS/GSIS, PhilHealth, Pag-IBIG) then apply 35% test

**Borrower stress test (bank practice):** Some banks apply a rate shock of +200–400 basis points to the repriced rate and test whether DTI still remains ≤ 35% under the stressed scenario.

---

## 8. Interest Rate Disclosure — Effective Interest Rate (EIR)

**BSP requirement (Circulars 730, 754, 799):** All lenders must disclose the **Effective Interest Rate (EIR)**, which includes:
- Nominal interest
- Processing fees
- Service charges
- Other charges incident to credit extension

EIR is higher than the nominal rate because it includes all fees amortized over the loan term.

**Default interest:** If loan becomes non-performing, bank may charge additional default interest (commonly nominal rate × 2, e.g., 6% regular → 12% default). Must be stipulated in loan agreement and not unconscionable.

---

## 9. Green Mortgage Incentive — BSP Circular 1152 (2024)

**Rule:** BSP Circular 1152 s. 2024 provides a lower risk-weight of **50%** for certified EDGE/Berde (green-certified) residential properties (standard residential risk weight is 100%). This allows banks to extend larger loanable amounts for eco-friendly properties within capital adequacy constraints.

---

## 10. Key Circular Reference Table

| Circular / Regulation | Year | Key Provision |
|---|---|---|
| BSP Circular 688 | 2010 | Introduced LTV ratio ceilings (60% non-residential, 80% residential) |
| MORB Section 303 | ongoing | Real estate collateral value capped at 60% of appraised value for classification |
| BSP Circular 855 | 2014 | Sound credit risk management; codified 60% REM collateral cap |
| MORB Section 363-A | ongoing | 25% real estate loan portfolio limit for UBs/KBs |
| BSP Circular 799 | 2013 | Legal interest rate 6% per annum when not stipulated |
| BSP Circulars 730, 754 | 2012–2013 | Truth-in-lending, EIR disclosure requirements |
| MORB Appendix 36 | ongoing | BSP rediscounting: max 80% LTV on collateral |
| BSP Circular 1152 | 2024 | Green mortgage 50% risk weight for EDGE/Berde certified properties |

---

## Computation-Relevant Aspects for Wave 2

Key computations to extract in Wave 2:
1. **LTV ratio computation** (inputs: loan amount, appraised value, selling price, property type → output: LTV%, maximum loanable amount)
2. **Bank mortgage amortization** (standard declining-balance formula; amortization factor table method)
3. **Repricing computation** (benchmark + spread → new rate; recompute amortization on remaining balance)
4. **Capacity-to-pay test** (monthly amortization ÷ gross monthly income ≤ 35%)
5. **REST computation** (bank-level, not borrower-facing — low automation opportunity for end users)
6. **EIR computation** (nominal rate + fees amortized over term — disclosure-driven)

Conflicts/gaps to verify in Wave 2:
- BSP Circular 688 LTV caps (60% non-residential, 80% residential) vs. market practice (banks lending up to 90% for primary residence from top-tier developers) — need to verify whether 688 was superseded or whether it applies differently
- The 35% DTI rule — precise regulatory citation needed (appears in Pag-IBIG Circular 402; unclear if BSP mandates the same for banks)
