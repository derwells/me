# Pag-IBIG Fund Housing Loan Circulars — Extracted Computation Rules

**Sources fetched:** 2026-02-25
**Primary circulars covered:** HDMF Circular No. 273 (original EUF), Circular No. 312 (AHP), Circular No. 403 (Modified AHP), Circular No. 443 (current ₱6M EUF), Circular No. 473 (Expanded EUF for 4PH program)
**Key secondary sources:** respicio.ph/commentaries, legaldex.com, omnicalculator.com/finance/pag-ibig-housing-loan, myhousingloancal.ph

---

## 1. Governing Law & Circulars

- **Republic Act No. 9679** — Home Development Mutual Fund Law of 2009 (authorizing statute)
- **HDMF Circular No. 443** (c. 2022) — Current guidelines for End-User Home Financing (EUF); raised ceiling to ₱6 million
- **HDMF Circular No. 473** — Guidelines for EUF under Expanded 4PH Program (socialized housing)
- **HDMF Circular No. 403** — Modified Guidelines on Pag-IBIG Affordable Housing Program (AHP)
- **HDMF Circular No. 428** — MRI premium rate schedule (referenced by practitioner sources)
- **HDMF Circular No. 300** — Housing loan restructuring; late payment surcharge provisions

**Note on Circular No. 423:** The specific text of Circular No. 423 was not found in publicly accessible sources. Circular No. 443 is the current operative circular for the standard EUF program (₱6M ceiling).

---

## 2. Loan Eligibility — Decision Tree Inputs

### 2.1 Membership Requirements
- Must be an **active Pag-IBIG member**
- Minimum **24 monthly mandated contributions** at time of application
  - Members may make lump-sum contributions to meet the 24-month threshold
  - Self-employed/voluntary members: some sources cite 5-year requirement (needs verification against current circular)

### 2.2 Age Limits
- **Maximum age at application:** 65 years old
- **Maximum age at loan maturity:** 70 years old
- Effective constraint: `max_term = min(30, 70 - age_at_application)` years

### 2.3 Credit/Background Requirements
- No outstanding Pag-IBIG housing loan that is in default
- No prior Pag-IBIG housing loan that was foreclosed, cancelled, or subject to dacion en pago
- Multi-purpose loan (MPL) payments must be current
- Passes background/credit/employment check (Credit Information Corporation database)

### 2.4 Income / Capacity to Pay
- Monthly amortization must not exceed **35–40% of gross monthly income**
  - Circular No. 443 sources say **35%**; original EUF circular says **40% of net disposable income**
  - Practitioner sources most commonly cite 35% of gross
- Member's net take-home pay after all deductions must remain above minimum per GAA/company policy

### 2.5 Loan Entitlement by Contribution Amount (from older EUF circular)
Required monthly contribution scales with loan amount bracket:

| Loan Amount Range | Required Monthly Contribution |
|---|---|
| Up to ₱500,000 | ₱200 |
| ₱500,001–₱600,000 | ₱250 |
| ₱600,001–₱700,000 | ₱300 |
| ₱700,001–₱800,000 | ₱350 |
| ₱800,001–₱900,000 | ₱400 |
| ₱900,001–₱1,000,000 | ₱450 |
| ₱1,000,001–₱1,100,000 | ₱500 |
| ₱1,100,001–₱1,200,000 | ₱550 |
| ₱1,200,001–₱1,300,000 | ₱600 |
| ₱1,300,001–₱1,400,000 | ₱650 |
| ₱1,400,001–₱1,500,000 | ₱700 |
| ₱1,500,001–₱1,600,000 | ₱750 |
| ₱1,600,001–₱1,700,000 | ₱800 |
| ₱1,700,001–₱1,800,000 | ₱850 |
| ₱1,800,001–₱1,900,000 | ₱900 |
| ₱1,900,001–₱2,000,000 | ₱950 |
| ₱2,000,001–₱2,100,000 | ₱1,000 |
| ₱2,100,001–₱2,200,000 | ₱1,050 |
| ₱2,200,001–₱2,300,000 | ₱1,100 |
| ₱2,300,001–₱2,400,000 | ₱1,150 |
| ₱2,400,001–₱2,500,000 | ₱1,200 |
| ₱2,500,001–₱2,600,000 | ₱1,250 |
| ₱2,600,001–₱2,700,000 | ₱1,300 |
| ₱2,700,001–₱2,800,000 | ₱1,350 |
| ₱2,800,001–₱2,900,000 | ₱1,400 |
| ₱2,900,001–₱3,000,000 | ₱1,450 |

*Note: This table is from an earlier circular when the max was ₱3M. The contribution schedule for the current ₱6M ceiling (Circular No. 443) needs verification.*

---

## 3. Loan Amount Limits

### 3.1 Maximum Amounts by Program
| Program | Maximum Loan Amount |
|---|---|
| Standard EUF (Circular 443) | ₱6,000,000 |
| Expanded EUF / 4PH Program (Circular 473) | ₱15,000,000 |
| Affordable Housing Program (AHP) — socialized | ₱580,000 (subdivision) / ₱750,000 (condominium) |
| AHP — for income ≤ ₱17,500 NCR / ≤ ₱14,000 other | ₱750,000 |

### 3.2 Loan Amount Determination (takes the lowest of)
1. Member's actual need
2. Loan entitlement based on contributions (per table above)
3. Loan-to-collateral value cap (see LTV section)
4. Capacity to pay cap (35% of gross income × term months)

### 3.3 Minimum Loan Amount
- ₱400,000 (some practitioner sources; to be verified in Circular 443)

---

## 4. Loan-to-Value (LTV) Ratios

### 4.1 Current (Circular No. 443 era) — Per practitioner sources
| Property Value | LTV Cap |
|---|---|
| Up to ₱400,000 | 100% |
| ₱400,001–₱1,250,000 | 90% |
| ₱1,250,001–₱6,000,000 | 80% |

### 4.2 Older EUF Circular — With Buyback Guaranty
| Loan Amount | LTV Ratio |
|---|---|
| Up to ₱400,000 | 100% |
| ₱400,001–₱750,000 | 100% |
| ₱750,001–₱1,250,000 | 95% |
| ₱1,250,001–₱3,000,000 | 90% |

### 4.3 Older EUF Circular — Without Buyback Guaranty (Retail)
| Loan Amount | LTV Ratio |
|---|---|
| Up to ₱400,000 | 100% |
| ₱400,001–₱750,000 | 90% |
| ₱750,001–₱1,250,000 | 85% |
| ₱1,250,001–₱3,000,000 | 80% |

**Note:** The LTV ratio for properties above ₱2.5M is sometimes cited as 90% in some practitioner sources. There is inconsistency that needs to be reconciled in Wave 2 verification.

---

## 5. Interest Rate Tables

### 5.1 Standard EUF — By Repricing Period (as of May 2025)
Source: respicio.ph citing Pag-IBIG Board rates effective through 2025

| Fixing/Repricing Period | Nominal Rate p.a. |
|---|---|
| 1-year | 5.75% |
| 3-year | 6.25% |
| 5-year | 6.50% |
| 10-year | 7.125% |
| 15-year | 7.75% |
| 20-year | 8.50% |
| 25-year | 9.125% |
| 30-year | 9.75% |

*The 3-year rate was extended through June 30, 2025 per Board action March 27, 2025.*

### 5.2 Alternative Rate Table (2024 — slightly different source)
Source: myhousingloancal.ph

| Loan Term (fixed) | Rate |
|---|---|
| 1-Year | 5.750% |
| 3-Year | 6.375% |
| 5-Year | 6.625% |
| 10-Year | 7.375% |
| 15-Year | 8.000% |
| 20-Year | 8.625% |
| 25-Year | 9.375% |
| 30-Year | 10.000% |

**Note:** Rate variations between these tables reflect different effective dates. The respicio.ph table (May 2025) is more current.

### 5.3 Interest Rate by Loan Amount Bracket (2024 era)
Source: multiple practitioner guides referencing Circular 443

| Loan Amount | Rate |
|---|---|
| ₱400,000–₱3,000,000 | 5.5% |
| ₱3,000,001–₱4,500,000 | 6.375% |
| ₱4,500,001–₱6,000,000 | 7.375% |

**Note:** This appears to be an alternative or older rate schedule. The repricing-period-based table above may be the primary current structure. Needs Wave 2 reconciliation.

### 5.4 Affordable Housing Program (AHP) Rates
| Income Bracket | Rate | Conditions |
|---|---|---|
| ≤₱17,500/mo NCR; ≤₱14,000/mo other regions | 3.0% fixed | For socialized housing ceiling amounts; 5-year fixed then repriced |
| Same members, amounts above socialized ceiling | 6.5% fixed | 10-year fixed period |
| ₱17,501–₱30,000/mo | 4.5% | Low-cost housing program |

### 5.5 Historical / Older Rate Structure (from original EUF circular, now superseded)
| Loan Amount | Initial Rate | Max Repriced Rate |
|---|---|---|
| Up to ₱400,000 | 6% | Cannot exceed original rate |
| ₱400,001–₱750,000 | 7% | 9% |
| ₱750,001–₱1,000,000 | 8.5% | 10.5% |
| ₱1,000,001–₱1,250,000 | 9.5% | 11.5% |
| ₱1,250,001–₱2,000,000 | 10.5% | 12.5% |
| ₱2,000,001–₱3,000,000 | 11.5% | 13.5% |

*Repricing occurred every 3 years under this structure.*

---

## 6. Amortization Formula

**Standard mortgage amortization (declining balance):**

```
M = P × [r(1+r)^n] / [(1+r)^n - 1]
```

Where:
- `M` = monthly amortization (principal + interest only, before insurance)
- `P` = loan principal
- `r` = monthly interest rate = annual_rate / 12
- `n` = number of months = years × 12

**Payment application priority (per EUF circular):**
1. Penalties (1/20 of 1% per day of delay = 0.05% per day)
2. Upgraded membership contributions
3. Insurance premiums (MRI + FGI)
4. Interest
5. Principal

**First payment:** Commences on the month immediately following loan takeout/final loan release.

**Worked example** (at 9.75%, ₱2,000,000, 30 years):
- Monthly amortization = ₱17,183.09
- First month interest = ₱16,250.00
- First month principal = ₱933.09

---

## 7. Mortgage Redemption Insurance (MRI) Premium

### 7.1 Coverage
- Covers outstanding debt in event of borrower's **death or total disability**
- Non-medical yearly renewable insurance
- Takes effect on date of Notice of Approval (NOA) / Letter of Guaranty (LOG)
- For joint borrowers: each co-borrower covered to extent of their corresponding obligation

### 7.2 MRI Premium Rate Table
Source: Circular No. 428 (referenced in practitioner sources)

| Age Bracket at Renewal | Annual Rate per ₱1,000 of Outstanding Balance |
|---|---|
| ≤ 30 years old | ₱0.42 |
| 31–35 years old | ₱0.57 |
| 36–40 years old | ₱0.73 |
| 41–45 years old | ₱1.02 |
| 46–50 years old | ₱1.50 |
| 51–55 years old | ₱2.23 |
| 56–60 years old | ₱3.49 |
| 61–65 years old | ₱5.54 |

### 7.3 MRI Premium Computation Formula

```
Annual MRI Premium = (Outstanding Loan Balance ÷ 1,000) × MRI Rate (age bracket)
Monthly MRI Premium = Annual MRI Premium ÷ 12
```

**Example:**
- Borrower age: 40 → rate = ₱0.73 per ₱1,000
- Outstanding balance: ₱1,000,000
- Annual MRI = (1,000,000 ÷ 1,000) × 0.73 = ₱730.00
- Monthly MRI = ₱730 ÷ 12 = **₱60.83**

**Key behavior:** MRI rate increases each year as the borrower ages into a higher bracket, but the outstanding balance decreases — net effect on monthly premium varies.

---

## 8. Fire and General/Allied Perils Insurance (FGI/FAPI)

### 8.1 Coverage Amount
- Insured value = **lower of** (appraised value of housing component) OR (loan amount)
- Insures against fire and allied perils

### 8.2 FGI Premium Rate
```
Annual FGI Premium = Insured Value × 0.076%
                   = Insured Value × 0.00076
Monthly FGI Premium = Annual FGI Premium ÷ 12
```

Rate: **0.076% per annum** (₱0.76 per ₱1,000 of insured value per year)

**Example:**
- Appraised value: ₱1,200,000; Loan: ₱1,000,000 → Insured value = ₱1,000,000
- Annual FGI = ₱1,000,000 × 0.00076 = ₱760.00
- Monthly FGI = ₱760 ÷ 12 = **₱63.33**

---

## 9. Total Monthly Payment Formula

```
Total Monthly Payment = Monthly Amortization (P+I) + Monthly MRI Premium + Monthly FGI Premium
```

**Note:** The amortization decreases over time as principal is paid down, but MRI also decreases (lower outstanding balance) while the rate may increase (as borrower ages). FGI rate stays constant but insured value may step down. The schedule is re-computed annually.

---

## 10. Loan Term and Prepayment Rules

- **Maximum term:** 30 years
- **Hard constraint:** Must not exceed `70 - age_at_application` years
- **Prepayment:** Allowed without penalty; subject only to a service fee
- **Early termination:** Allowed
- **Default threshold:** 3 consecutive missed monthly amortizations triggers default
- **Penalty rate:** 1/20 of 1% per day on unpaid amounts (= 0.05%/day = 18.25% p.a.)

---

## 11. Collateral Requirements

- Primary: **First Real Estate Mortgage (REM)** on the property
- Title must be free of prior encumbrances
- Property types: residential lot (≤1,000 sqm), house-and-lot, townhouse, condominium unit
- Loan purposes: purchase, construction, improvement, completion, refinancing

---

## 12. Co-Borrower Rules

- Maximum **3 qualified Pag-IBIG members** in a single loan
- Must be related within **second degree of consanguinity or affinity**
- All are joint and severally liable
- Each co-borrower covered by MRI proportionally

---

## 13. Key Data Gaps for Wave 2

1. **Circular No. 443 full text** — contribution schedule table for ₱3M–₱6M range; exact LTV table; exact eligibility rules for the ₱6M tier
2. **Current MRI rate table confirmation** — Circular No. 428 rates widely cited but need confirmation against any newer circular
3. **FGI rate confirmation** — 0.076% is widely cited but source circular not identified
4. **Repricing vs. loan-amount rate structure** — whether the current program uses repricing-period-based rates (Section 5.1) or loan-amount-based rates (Section 5.3), or both as alternatives
5. **4PH/Expanded program LTV and rate** — Circular No. 473 specific details not accessible (Scribd document blocked)
6. **Self-employed member contribution requirements** — 5-year vs. 24-month discrepancy

---

## 14. Relevant Sections for Wave 2 Computation Extraction

- **pagibig-loan-eligibility**: Sections 2, 3, 12
- **pagibig-amortization**: Sections 4, 5, 6, 7, 8, 9, 10
- **ltv-ratio**: Section 4 (cross-reference with BSP circulars for bank loans)
