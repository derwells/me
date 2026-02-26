# Pag-IBIG Amortization Schedule — Computation Extraction

**Aspect:** pagibig-amortization (Wave 2)
**Date:** 2026-02-26
**Primary source:** `input/pagibig-housing-loan-circulars.md` (HDMF Circulars 443, 403, 473, 300)
**Verification:** Cross-checked against 15 independent sources (see Section 9)
**Deterministic:** Yes — given approved loan amount, rate, term, borrower age, and insurance parameters, the full amortization schedule is deterministic

---

## 1. Inputs

| Input | Type | Source |
|-------|------|--------|
| `approved_loan_amount` | currency (PHP) | From eligibility computation (pagibig-loan-eligibility) |
| `annual_interest_rate` | float (%) | Lookup by repricing period (Section 4) |
| `repricing_period_years` | enum: 1, 3, 5, 10, 15, 20, 25, 30 | Borrower selection |
| `loan_term_years` | integer (1–30) | Borrower selection; constrained by min(30, 70 − age) |
| `borrower_age_at_takeout` | integer | Borrower DOB vs. loan takeout date |
| `property_appraised_value_improvements` | currency (PHP) | Pag-IBIG accredited appraiser (housing component only) |
| `housing_program` | enum: standard_euf, expanded_4ph, ahp | From eligibility |

### Derived Inputs
| Derived | Formula |
|---------|---------|
| `r` (monthly rate) | `annual_interest_rate / 12 / 100` |
| `n` (total months) | `loan_term_years × 12` |
| `fgi_insured_value` | `min(property_appraised_value_improvements, approved_loan_amount)` |

---

## 2. Core Amortization Formula (Principal + Interest)

**Method:** Standard declining balance (equal monthly installment)

```
M = P × [r(1+r)^n] / [(1+r)^n - 1]
```

Where:
- `M` = monthly amortization (principal + interest only)
- `P` = approved loan principal
- `r` = monthly interest rate
- `n` = total number of monthly payments

### Monthly Breakdown (for month `k`, k = 1..n)

```
interest_k    = outstanding_balance_(k-1) × r
principal_k   = M - interest_k
outstanding_balance_k = outstanding_balance_(k-1) - principal_k
```

Where `outstanding_balance_0 = P`

**Verification status:** CONFIRMED — independently computed and cross-checked against OmniCalculator (exact match to the centavo).

### Worked Examples

| Scenario | P | Rate | Term | Monthly P+I |
|----------|---|------|------|------------|
| Standard EUF, 30-yr fixed | ₱2,000,000 | 9.750% | 30 yr | ₱17,183.09 |
| Standard EUF, 10-yr fixed | ₱1,000,000 | 7.125% | 10 yr | ₱11,675.37 |
| 4PH subsidized | ₱850,000 | 3.000% | 30 yr | ₱3,583.63 |
| Standard EUF, 3-yr fixed | ₱3,000,000 | 6.250% | 25 yr | ₱19,821.89 |

---

## 3. Insurance Premium Computations

### 3.1 Mortgage Redemption Insurance (MRI)

**Coverage:** Outstanding loan balance; pays off remaining debt upon borrower death or total disability.

**Premium structure:** CONFLICT between sources — two models found:

#### Model A: Uniform Rate (current, per official circulars)
Per HDMF Circular 403 and ASSA institutional report, MRI uses a **uniform premium rate**:
```
Annual MRI  = (outstanding_balance / 1,000) × uniform_rate_per_1000
Monthly MRI = Annual MRI / 12
```

Last publicly documented uniform rate: **₱0.23 per ₱1,000/year** (from 2014–2015 Lockton Philippines contract, per ASSA report). This rate may have been updated in subsequent insurance contract rebiddings.

#### Model B: Age-Bracketed Rate (unverified — may be pre-2014)
Widely cited in practitioner guides, attributed to "Circular 428" (but actual Circular 428 covers foreclosed property sales, not MRI):

| Age Bracket | Rate per ₱1,000/year |
|-------------|---------------------|
| ≤30 | ₱0.42 |
| 31–35 | ₱0.57 |
| 36–40 | ₱0.73 |
| 41–45 | ₱1.02 |
| 46–50 | ₱1.50 |
| 51–55 | ₱2.23 |
| 56–60 | ₱3.49 |
| 61–65 | ₱5.54 |

**Verification status: CONFLICT**
- Official circular language (Circular 403): explicitly says "uniform premium rate"
- ASSA report: confirms single rate of ₱0.23/₱1,000 (post-reform)
- The age-bracket table source cannot be verified; the claimed circular number is incorrect
- **Recommendation for automation:** Default to uniform rate model; allow user override with age-bracket table for legacy loans or if Pag-IBIG reverts to age-based pricing

**MRI renewal:** Yearly renewable term insurance, renewed on the anniversary of the loan takeout date. Premium recalculated annually on the outstanding balance at renewal.

### 3.2 Fire and Allied Perils Insurance (FAPI/FGI)

**Coverage:** Structural damage from fire and allied perils on the housing improvements.

```
insured_value = min(appraised_value_of_improvements, loan_amount)
Annual FGI    = insured_value × fgi_rate
Monthly FGI   = Annual FGI / 12
```

**Rate:** CONFLICT between sources:
- Primary claim: **0.076% p.a.** (₱0.76 per ₱1,000/year) — source unverified
- Most recent public data: **0.1686% p.a.** (₱1.686 per ₱1,000/year) — Manila Bulletin, Aug 2018, citing official Pag-IBIG announcement of rate reduction from 0.40%
- No source was found confirming the 0.076% figure

**Verification status: CONFLICT** — use 0.1686% as conservative default; allow user override.

**FGI insured value basis: CONFIRMED** — `min(appraised improvements, loan amount)` per Circular 403, PagibigFinancing, Manila Bulletin.

### 3.3 First-Year Insurance Deduction

**CONFIRMED:** First-year MRI and FAPI premiums are **deducted from loan proceeds** at takeout.
```
net_disbursement = approved_loan_amount - first_year_mri - first_year_fapi
```
Subsequent years: premiums collected monthly alongside the P+I amortization.

---

## 4. Interest Rate Lookup Table

### 4.1 Standard EUF — By Repricing Period (current as of 2025)

Rates set by Pag-IBIG Board under Full Risk-Based Pricing (FRBP), established via Board Resolution 2940-2012. Current rates effective July 1, 2023, maintained through end-2025.

| Repricing Period | Rate p.a. |
|------------------|-----------|
| 1-year | 5.750% |
| 3-year | 6.250% |
| 5-year | 6.500% |
| 10-year | 7.125% |
| 15-year | 7.750% |
| 20-year | 8.500% |
| 25-year | 9.125% |
| 30-year | 9.750% |

**Verification status: CONFIRMED** — PCO government press release, Inquirer, Philstar, Respicio & Co. all agree on exact values. Pre-July 2023 rates were slightly higher (e.g., 3-year was 6.375%).

### 4.2 Subsidized Programs

| Program | Rate | Fixed Period | Post-Fixed |
|---------|------|-------------|------------|
| 4PH socialized (income ≤₱47,856 NCR) | 3.0% | 5 years (10 yrs early-bird) | Prevailing Pag-IBIG rates |
| AHP socialized (income ≤₱17,500 NCR) | 3.0% | 5 years | Repriced to Board rate |
| AHP low-cost (₱17,501–₱30,000) | 4.5% | — | — |

### 4.3 Loan-Amount-Based Rates — REJECTED

Some third-party calculators cite rates by loan amount bracket (5.5%/6.375%/7.375%). This structure:
- Appears only on unofficial calculator sites with no circular reference
- Is contradicted by all government press releases and news sources
- Is NOT the current rate structure (the repricing-period table is)
- May reflect a transitional/promotional table from ~2022–2023 or a misinterpretation of older circulars

**The older circulars** (pre-FRBP) did use loan-amount-based rates, but at different values (6%–11.5%).

---

## 5. Total Monthly Payment Formula

```
total_monthly_payment = monthly_amortization_PI + monthly_mri + monthly_fgi
```

Where:
```
monthly_amortization_PI = P × [r(1+r)^n] / [(1+r)^n - 1]
monthly_mri             = (outstanding_balance / 1,000) × mri_rate / 12
monthly_fgi             = (insured_value × fgi_rate_pct) / 12
```

**Note:** The total monthly payment is NOT constant over the life of the loan:
- P+I component is constant (within a repricing period)
- MRI decreases annually as outstanding balance decreases (and may increase if age-bracket model applies and borrower ages into higher bracket)
- FGI is effectively constant (insured value = min(improvements, loan) — improvements don't change; loan balance decreases but insured value is set at origination)

---

## 6. Repricing Mechanics

At the end of the chosen fixed-rate period:

```
1. Pag-IBIG Board announces new rate schedule (at least 30 days advance notice)
2. Borrower selects new repricing period from available options
3. New rate = Board_rate_for_selected_period
4. Remaining balance = outstanding_balance at repricing date
5. Remaining term = original_term - elapsed_months
6. New M = remaining_balance × [r_new(1+r_new)^n_remaining] / [(1+r_new)^n_remaining - 1]
```

**Additional rules:**
- **Early conversion:** Borrower may switch to a new repricing period before current one expires (via Virtual Pag-IBIG)
- **No rate caps** under FRBP system (unlike pre-FRBP which had ceiling rates per bracket)
- Insurance premiums recalculated separately at the repricing/renewal date

**Verification status: CONFIRMED** — Respicio, PagibigFinancing, LegalDex all agree.

---

## 7. Payment Application Priority

When a payment is received, it is applied in this order:

1. **Penalties** (0.05%/day on overdue amounts)
2. **Upgraded membership contributions** (if member owes contribution top-ups)
3. **Insurance premiums** (MRI + FAPI)
4. **Interest**
5. **Principal**

**Implication for schedule computation:** If a borrower is in arrears, payments first cover penalties and insurance before touching interest or principal, which can cause negative amortization (balance grows).

**Verification status: CONFIRMED** — LegalDex (EUF circular), Circular 403 (Supreme Court E-Library), Respicio.

---

## 8. Penalty and Prepayment Rules

### 8.1 Late Payment Penalty
```
daily_penalty = unpaid_amount × 0.0005  (i.e., 1/20 of 1% per day)
```
- Annualized: 18.25% p.a. simple interest on overdue amounts
- Accrues from first day of delay until payment is applied
- Applied before all other payment components (see priority order)

**Verification status: CONFIRMED** — 5 independent sources agree, including Circulars 300 and 403.

### 8.2 Default Trigger
- **3 consecutive missed monthly amortizations** → entire obligation becomes immediately due and demandable
- Foreclosure proceedings initiated after default declaration
- TAV (Total Accumulated Value of member savings) may be applied to outstanding balance

### 8.3 Prepayment
- **No prepayment penalty** (legal basis: RA 7394, Consumer Act of the Philippines)
- Subject only to a **service fee** (amount set by Fund, not publicly documented)
- Minimum prepayment: at least 1 monthly amortization equivalent for principal application
- **Excess payment treatment:** Applied as advance amortizations by default; applied to principal reduction only upon explicit written request from borrower (noted on Pag-IBIG receipt)

**Verification status: CONFIRMED** — Circular 403, Respicio, lawyer-philippines.com.

---

## 9. Restructuring (Existing Delinquent Loans)

Applicable when borrower is 3+ months past due:
```
restructured_rate = 6.375% p.a. (3-year fixed)
penalty_condonation = up to 100% of accrued penalties
required_downpayment = 10% (most categories)
new_term = min(extended_term, 30 years, 70 - current_age)
```

- One-time restructuring limit (except force majeure)
- Post-restructuring default: 6 monthly arrearages triggers automatic foreclosure/cancellation
- All prior payments remain credited; only forward schedule resets

**Verification status: CONFIRMED** — multiple practitioner sources.

---

## 10. Processing Fees (Upfront)

| Fee | Amount | When |
|-----|--------|------|
| Application processing fee | ₱1,000 | At application |
| Loan takeout fee | ₱2,000 | At disbursement |
| **Total Pag-IBIG fees** | **₱3,000** | |

Third-party costs (NOT Pag-IBIG fees, but part of total transaction cost):
- Documentary stamp tax on mortgage (1.5% of loan amount) — covered in ph-tax-computations-reverse
- Registry of Deeds annotation fee — covered in rod-registration-fees
- Notarial fee — covered in notarial-fees

---

## 11. Edge Cases and Special Rules

1. **First payment timing:** Commences the month immediately following loan takeout/final release. No grace period on first payment.

2. **Joint borrower MRI:** Each co-borrower covered proportionally to their share of the obligation. If one co-borrower dies, their portion of the outstanding balance is paid by MRI; remaining co-borrowers continue paying their share.

3. **Subsidized-to-market rate transition (4PH/AHP):** After the 3%/4.5% fixed period ends, amortization recomputed at prevailing Board rates on remaining balance/term. This can cause a significant payment shock — e.g., ₱850K loan going from ₱3,584/mo (3%) to ~₱5,303/mo (6.375%).

4. **Net disbursement:** First-year insurance premiums deducted from loan proceeds. For a ₱2M loan:
   - If MRI uniform rate ₱0.23/₱1,000: first-year MRI ≈ ₱460
   - If FGI rate 0.1686%: first-year FGI ≈ ₱3,372 (on ₱2M insured)
   - Net disbursement ≈ ₱1,996,168

5. **Repricing with shorter remaining term:** If original term was 30 years and repricing happens at year 3, borrower has 27 years remaining. New amortization uses 27-year remaining term at the new rate.

6. **Prepayment principal application:** Borrower must explicitly request principal reduction. Without explicit request, excess payments are treated as advance amortizations (covering future months), NOT as principal reduction.

7. **Annual insurance recalculation:** MRI premium recalculated each year on the outstanding balance at the takeout anniversary date. FGI effectively constant (insured value set at origination).

8. **Medical questionnaire trigger:** Required if borrower >60 years old OR loan >₱2,000,000 — affects MRI underwriting, not the premium formula itself.

---

## 12. Pseudocode Implementation

```python
def compute_pagibig_amortization_schedule(
    loan_amount: float,
    annual_rate_pct: float,
    term_years: int,
    borrower_age: int,
    improvements_appraised_value: float,
    mri_rate_per_1000: float = 0.23,    # uniform rate; override if age-bracketed
    fgi_rate_pct: float = 0.1686,       # conservative default
) -> dict:
    """
    Returns full amortization schedule including insurance.
    """
    r = annual_rate_pct / 100 / 12  # monthly rate
    n = term_years * 12             # total months

    # Core P+I monthly payment
    monthly_pi = loan_amount * (r * (1 + r)**n) / ((1 + r)**n - 1)

    # FGI (constant)
    insured_value = min(improvements_appraised_value, loan_amount)
    annual_fgi = insured_value * fgi_rate_pct / 100
    monthly_fgi = annual_fgi / 12

    # First-year insurance deduction from proceeds
    annual_mri_yr1 = (loan_amount / 1000) * mri_rate_per_1000
    net_disbursement = loan_amount - annual_mri_yr1 - annual_fgi

    # Build monthly schedule
    schedule = []
    balance = loan_amount
    for month in range(1, n + 1):
        interest = balance * r
        principal = monthly_pi - interest

        # MRI (recalculated annually at takeout anniversary)
        if month == 1 or month % 12 == 1:
            annual_mri = (balance / 1000) * mri_rate_per_1000
            monthly_mri = annual_mri / 12

        total_payment = monthly_pi + monthly_mri + monthly_fgi

        schedule.append({
            'month': month,
            'principal': principal,
            'interest': interest,
            'mri': monthly_mri,
            'fgi': monthly_fgi,
            'total_payment': total_payment,
            'ending_balance': balance - principal,
        })
        balance -= principal

    return {
        'monthly_pi': monthly_pi,
        'monthly_fgi': monthly_fgi,
        'net_disbursement': net_disbursement,
        'schedule': schedule,
        'total_interest': sum(row['interest'] for row in schedule),
        'total_mri': sum(row['mri'] for row in schedule),
        'total_fgi': sum(row['fgi'] for row in schedule),
        'total_cost': sum(row['total_payment'] for row in schedule),
    }


def compute_repriced_schedule(
    remaining_balance: float,
    new_annual_rate_pct: float,
    remaining_term_years: int,
    borrower_age: int,
    improvements_appraised_value: float,
    mri_rate_per_1000: float = 0.23,
    fgi_rate_pct: float = 0.1686,
) -> dict:
    """
    Recomputes amortization after repricing event.
    Same formula, applied to remaining balance and remaining term.
    """
    return compute_pagibig_amortization_schedule(
        loan_amount=remaining_balance,
        annual_rate_pct=new_annual_rate_pct,
        term_years=remaining_term_years,
        borrower_age=borrower_age,
        improvements_appraised_value=improvements_appraised_value,
        mri_rate_per_1000=mri_rate_per_1000,
        fgi_rate_pct=fgi_rate_pct,
    )


def compute_penalty(unpaid_amount: float, days_overdue: int) -> float:
    """Late payment penalty: 1/20 of 1% per day."""
    return unpaid_amount * 0.0005 * days_overdue
```

---

## 13. Verification Summary

Cross-checked against 15 independent sources including:
- Official government press releases (PCO, PNA)
- Supreme Court E-Library (Circular 403 full text)
- News outlets (Inquirer, Philstar, Manila Bulletin)
- Legal practitioner guides (Respicio & Co., LegalDex)
- Third-party calculators (OmniCalculator, best-calculators.com)
- ASSA institutional report (for MRI rate history)

| Component | Status | Confidence |
|-----------|--------|------------|
| Amortization formula (declining balance) | **CONFIRMED** | High — exact match with independent computation |
| Interest rate table (by repricing period) | **CONFIRMED** | High — 4+ official/news sources agree |
| Interest rate by loan amount bracket | **REJECTED** | High — unofficial, contradicted by all government sources |
| MRI premium — uniform vs. age-bracket | **CONFLICT** | Low — official circulars say "uniform"; age table source unverifiable |
| MRI uniform rate (₱0.23/₱1,000) | **UNVERIFIED** | Low — last public data from 2014; may be updated |
| FGI rate (0.076% claimed) | **UNVERIFIED** | Low — no source confirms; 0.1686% is last documented (2018) |
| FGI insured value basis | **CONFIRMED** | High — Circular 403 + news sources |
| Total payment = P+I + MRI + FGI | **CONFIRMED** | High |
| Payment priority (5-item order) | **CONFIRMED** | High |
| Penalty rate 0.05%/day | **CONFIRMED** | High — 5 sources including official circulars |
| Prepayment without penalty | **CONFIRMED** | High — RA 7394 legal basis |
| Repricing mechanics | **CONFIRMED** | High — multiple sources with detail |
| First-year insurance deduction | **CONFIRMED** | Medium — practitioner sources |
| Processing fees ₱3,000 | **CONFIRMED** | Medium — multiple practitioner sources |
| Default at 3 missed payments | **CONFIRMED** | High — official circulars |
| Restructuring at 6.375% | **CONFIRMED** | Medium — practitioner sources |

---

## 14. Legal Citations

| Rule | Legal Basis |
|------|------------|
| Amortization method (equal monthly P+I) | HDMF Circular No. 443; Circular No. 403 Sec. IX |
| Interest rate schedule (FRBP by repricing period) | Pag-IBIG Board Resolution 2940-2012; Board action July 2023 |
| Rate maintenance through 2025 | Pag-IBIG Board action March 2025 (Philstar, Inquirer) |
| MRI coverage (death/total disability) | HDMF Circular No. 443; Circular No. 403 Sec. IX.A |
| MRI uniform premium rate | HDMF Circular No. 403 (explicit "uniform" language) |
| FGI coverage and basis | HDMF Circular No. 403 Sec. IX.A; Manila Bulletin Aug 2018 |
| FGI rate reduction to 0.1686% | Manila Bulletin Aug 19, 2018 citing Pag-IBIG announcement |
| Payment priority order | HDMF EUF Circular (via LegalDex); Circular 403 |
| Late penalty 1/20 of 1%/day | HDMF Circular No. 300; Circular No. 403 |
| Default at 3 consecutive misses | HDMF Circular No. 443; Circular No. 403 |
| Prepayment without penalty | RA 7394 (Consumer Act); HDMF Circular No. 403 Sec. IX.C |
| Repricing mechanics (30-day notice, borrower choice) | HDMF FRBP guidelines; Respicio commentary |
| Restructuring terms (6.375%, 3-yr fixed) | HDMF Special Housing Loan Restructuring guidelines |
| Processing fees (₱1,000 + ₱2,000) | HDMF standard fee schedule; practitioner sources |

---

## 15. Data Dependencies for Automation

| Dependency | Type | Update Frequency | Risk |
|-----------|------|-----------------|------|
| Interest rate table (repricing periods) | External lookup | Board resolution (~annually) | Medium — stable since July 2023 |
| MRI premium rate | External (Pag-IBIG insurance contract) | Every few years (contract rebidding) | **High** — current rate unverifiable |
| FGI/FAPI premium rate | External (Pag-IBIG insurance contract) | Every few years (contract rebidding) | **High** — current rate unverifiable |
| 4PH/AHP subsidized rates | External (program guidelines) | Per circular amendment | Low — 3% rate stable since launch |
| Repricing schedule (new Board rates) | External announcement | Per repricing event | Medium — Board announces 30 days in advance |

---

## 16. Cross-References

- **pagibig-loan-eligibility** (Wave 2, complete): Provides the approved loan amount, rate selection, and term — direct upstream dependency
- **ltv-ratio** (Wave 2, pending): Pag-IBIG LTV determines maximum loan, which becomes the principal for this computation
- **rod-registration-fees** (Wave 2, pending): Mortgage annotation fee applies on the Pag-IBIG mortgage registration
- **broker-commission** (Wave 2, pending): Not directly related but Pag-IBIG loans affect developer commission timing
- **ph-tax-computations-reverse**: Documentary stamp tax (1.5% of loan amount) on the mortgage document is a transaction cost alongside the amortization
