# Pag-IBIG Housing Loan Eligibility — Computation Extraction

**Aspect:** pagibig-loan-eligibility (Wave 2)
**Date:** 2026-02-26
**Primary source:** `input/pagibig-housing-loan-circulars.md` (HDMF Circular No. 443, Circular No. 403, Circular No. 473)
**Verification:** Cross-checked against 10 independent sources (see Section 11)
**Deterministic:** Yes — given all inputs, eligibility is a binary pass/fail with a deterministic loan ceiling

---

## 1. Inputs

| Input | Type | Source |
|-------|------|--------|
| `is_active_member` | boolean | Pag-IBIG membership records |
| `monthly_contributions_count` | integer | HDMF contribution ledger |
| `last_contribution_within_6_months` | boolean | HDMF contribution ledger |
| `monthly_contribution_amount` | currency (PHP) | HDMF contribution ledger |
| `age_at_application` | integer (years) | Borrower DOB |
| `gross_monthly_income` | currency (PHP) | Employment certificate / ITR |
| `has_outstanding_pagibig_loan_in_default` | boolean | HDMF records (as principal OR co-borrower) |
| `has_prior_foreclosed_pagibig_loan` | boolean | HDMF records (foreclosed/cancelled/bought-back/surrendered/dacion) |
| `has_stl_in_arrears` | boolean | HDMF Short-Term Loan records |
| `passes_cic_credit_check` | boolean | CIC + CMAP + courts + HDMF internal systems |
| `desired_loan_amount` | currency (PHP) | Borrower input |
| `property_appraised_value` | currency (PHP) | Pag-IBIG accredited appraiser |
| `property_selling_price` | currency (PHP) | Contract to sell |
| `property_type` | enum: lot, house_and_lot, townhouse, condo | Property documents |
| `lot_area_sqm` | float | Title / survey |
| `loan_purpose` | enum: purchase, construction, improvement, completion, refinancing | Application |
| `desired_term_years` | integer (1–30) | Borrower input |
| `has_buyback_guaranty` | boolean | Developer accreditation |
| `co_borrowers` | list (max 2 additional) | Application |
| `co_borrower_relationship` | enum per co-borrower | Within 2nd degree consanguinity/affinity (or non-relative with conditions) |
| `housing_program` | enum: standard_euf, expanded_4ph, ahp | Application |
| `is_ofw` | boolean | OEC / employment docs |

---

## 2. Eligibility Decision Tree

```
STEP 1: Membership Check
├── is_active_member == false → REJECT("Must be an active Pag-IBIG Fund member")
├── monthly_contributions_count < 24 → REJECT("Minimum 24 monthly contributions required")
│   Note: Lump-sum contributions allowed to meet 24-month threshold.
│   Note: 24-month rule applies to ALL member types (employed, self-employed, OFW, voluntary).
├── last_contribution_within_6_months == false → REJECT("Must have at least 1 contribution in last 6 months")
└── PASS → Step 2

STEP 2: Age Check
├── age_at_application > 65 → REJECT("Maximum age at application is 65")
├── max_allowable_term = min(30, 70 - age_at_application)
├── desired_term_years > max_allowable_term → REJECT("Loan maturity would exceed age 70")
└── PASS → Step 3

STEP 3: Loan History Check
├── has_outstanding_pagibig_loan_in_default == true → REJECT("Outstanding Pag-IBIG loan in default")
│   Note: Applies whether member is principal borrower or co-borrower on the defaulted loan.
├── has_prior_foreclosed_pagibig_loan == true → REJECT("Prior foreclosed/cancelled/bought-back/surrendered/dacion Pag-IBIG loan")
├── has_stl_in_arrears == true → REJECT("Short-Term Loan in arrears")
└── PASS → Step 4

STEP 4: Credit Check
├── passes_cic_credit_check == false → REJECT("Failed credit/background check")
│   Note: Check is broader than CIC — includes CMAP (court cases), CIC (credit bureau),
│   court records, and HDMF internal systems.
└── PASS → Step 5

STEP 5: Property Check
├── property_type == lot AND lot_area_sqm > 1000 → REJECT("Lot exceeds 1,000 sqm limit")
├── loan_purpose NOT IN [purchase, construction, improvement, completion, refinancing]
│   → REJECT("Invalid loan purpose")
├── IF loan_purpose == refinancing:
│   ├── existing mortgage < 2 years repayment history → REJECT("Minimum 2-year repayment for refinancing")
│   └── any payment > 30 days past due in last 6 months → REJECT("Refinancing requires current payments")
└── PASS → Step 6

STEP 6: Co-Borrower Check (if applicable)
├── len(co_borrowers) > 2 → REJECT("Maximum 3 total borrowers (1 primary + 2 co-borrowers)")
├── For each co-borrower:
│   ├── NOT active Pag-IBIG member → REJECT("Co-borrower not an active member")
│   ├── contributions < 24 → REJECT("Co-borrower has < 24 monthly contributions")
│   └── relationship check:
│       ├── IF within 2nd degree consanguinity/affinity → PASS
│       └── IF non-relative:
│           ├── loan_purpose != purchase → REJECT("Non-relative co-borrowing only for purchase")
│           ├── property not in ALL borrowers' names → REJECT("Non-relative: title must include all borrowers")
│           └── PASS (with conditions: all execute REM, release only upon full payment)
└── PASS → Step 7

STEP 7: Loan Amount Determination
├── max_by_program = lookup(housing_program, PROGRAM_LIMITS_TABLE)    [Section 3]
├── max_by_contribution = lookup(monthly_contribution_amount, CONTRIBUTION_TABLE)  [Section 4]
├── collateral_value = min(property_appraised_value, property_selling_price)
├── ltv_cap = lookup(collateral_value, LTV_TABLE[has_buyback_guaranty])  [Section 5]
├── max_by_ltv = collateral_value × ltv_cap
├── total_gmi = sum(gross_monthly_income for all borrowers)
├── max_monthly_amort = total_gmi × 0.35
├── rate = get_interest_rate(housing_program, desired_term_years, loan_amount_bracket)  [Section 6]
├── r = rate / 12; n = desired_term_years × 12
├── max_by_capacity = max_monthly_amort × [(1+r)^n - 1] / [r × (1+r)^n]
├── max_loan = min(max_by_program, max_by_contribution, max_by_ltv, max_by_capacity)
│
├── desired_loan_amount > max_loan → OFFER REDUCED AMOUNT (max_loan)
└── ELIGIBLE: approved_amount = min(desired_loan_amount, max_loan)
```

---

## 3. Maximum Loan by Program

| Program | Max Loan Amount | Key Conditions |
|---------|----------------|----------------|
| Standard EUF (Circular 443) | ₱6,000,000 | Default program for most borrowers |
| Expanded 4PH (Circular 473) | ₱15,000,000 | Socialized housing; subsidized 3% rate; first-time homebuyers |
| AHP — Socialized horizontal (24–26 sqm) | ₱844,440 | Per DHSUD JMC 2025-001 (Dec 2025, valid 3 yrs) |
| AHP — Socialized horizontal (27+ sqm) | ₱950,000 | Per DHSUD JMC 2025-001 |
| AHP — Socialized condo 3-5F (24–26 sqm) | ₱1,280,000 | Per DHSUD JMC 2025-001 |
| AHP — Socialized condo 3-5F (27+ sqm) | ₱1,500,000 | Per DHSUD JMC 2025-001 |
| AHP — Socialized condo 6F+ (24–26 sqm) | ₱1,600,000 | Per DHSUD JMC 2025-001 |
| AHP — Socialized condo 6F+ (27+ sqm) | ₱1,800,000 | Per DHSUD JMC 2025-001 |

**Note:** AHP ceilings were updated by DHSUD-DEPDev JMC 2025-001 (effective Dec 2025). The older ₱580K/₱750K figures from Circular 403 are superseded. HUC add-on of ₱50K–₱200K applies based on zonal value band.

---

## 4. Maximum Loan by Contribution Amount (Lookup Table)

Step function: `monthly_contribution_amount → max_loan_entitlement`

| Monthly Contribution | Max Loan Entitlement |
|---------------------|---------------------|
| ₱200 | ₱500,000 |
| ₱250 | ₱600,000 |
| ₱300 | ₱700,000 |
| ₱350 | ₱800,000 |
| ₱400 | ₱900,000 |
| ₱450 | ₱1,000,000 |
| ₱500 | ₱1,100,000 |
| ₱550 | ₱1,200,000 |
| ₱600 | ₱1,300,000 |
| ₱650 | ₱1,400,000 |
| ₱700 | ₱1,500,000 |
| ₱750 | ₱1,600,000 |
| ₱800 | ₱1,700,000 |
| ₱850 | ₱1,800,000 |
| ₱900 | ₱1,900,000 |
| ₱950 | ₱2,000,000 |
| ₱1,000 | ₱2,100,000 |
| ₱1,050 | ₱2,200,000 |
| ₱1,100 | ₱2,300,000 |
| ₱1,150 | ₱2,400,000 |
| ₱1,200 | ₱2,500,000 |
| ₱1,250 | ₱2,600,000 |
| ₱1,300 | ₱2,700,000 |
| ₱1,350 | ₱2,800,000 |
| ₱1,400 | ₱2,900,000 |
| ₱1,450 | ₱3,000,000 |

**Pattern:** ₱50 increment per ₱100K of loan entitlement.

**DATA GAP:** Table confirmed up to ₱3M only (from Circular 247-09). Extension for ₱3M–₱6M under Circular 443 is **not publicly documented**. The pattern suggests continuation (₱1,500 → ₱3.1M, ..., ₱2,950 → ₱6M) but this is extrapolation. Automation should treat the ₱3M+ range as requiring manual verification or allow user override.

**Context:** Pag-IBIG doubled maximum contribution (₱100 → ₱200 per party, ₱400 total) effective Feb 2024 when Fund Salary cap raised from ₱5K to ₱10K. This may have restructured the entitlement table.

---

## 5. Maximum Loan by LTV Ratio

### 5.1 Retail / No Buyback Guaranty (individual borrowers — most common)

| Collateral Value | LTV Cap |
|-----------------|---------|
| Up to ₱400,000 | 100% |
| ₱400,001–₱1,250,000 | 90% |
| ₱1,250,001–₱6,000,000 | 80% |

### 5.2 Developer-Assisted / With Buyback Guaranty

| Collateral Value | LTV Cap |
|-----------------|---------|
| Up to ₱400,000 | 100% |
| ₱400,001–₱750,000 | 100% |
| ₱750,001–₱1,250,000 | 95% |
| ₱1,250,001–₱3,000,000 | 90% |

### 5.3 AHP / Socialized Housing

| Collateral Value | LTV Cap |
|-----------------|---------|
| Up to socialized ceiling | 100% |

**Formula:**
```
collateral_value = min(property_appraised_value, property_selling_price)
ltv_cap = lookup(collateral_value, LTV_TABLE[has_buyback_guaranty])
max_by_ltv = collateral_value × ltv_cap
```

**Conflict note:** Some calculators cite 95%/90% LTV thresholds at ₱2.5M boundary (economic housing). This likely reflects a specific program variant or promotional offering, not the standard schedule. The retail table (100%/90%/80%) is the conservative baseline confirmed by multiple sources.

---

## 6. Interest Rate Determination (for capacity-to-pay calculation)

The interest rate used in the capacity computation depends on the program and repricing period chosen.

### Standard EUF — By Repricing Period (as of 2025, per Pag-IBIG Board)

| Repricing Period | Rate p.a. |
|-----------------|-----------|
| 1-year | 5.750% |
| 3-year | 6.250% |
| 5-year | 6.500% |
| 10-year | 7.125% |
| 15-year | 7.750% |
| 20-year | 8.500% |
| 25-year | 9.125% |
| 30-year | 9.750% |

### AHP / 4PH Subsidized Rates

| Program | Rate | Fixed Period |
|---------|------|-------------|
| 4PH socialized (income ≤₱47,856 NCR) | 3.0% | 5 years (10 years for early-bird first 30,000) |
| AHP socialized (income ≤₱17,500 NCR) | 3.0% | 5 years, then repriced |
| AHP low-cost (income ₱17,501–₱30,000) | 4.5% | — |
| 4PH higher-tier (₱1.8M) | 4.5% | For first 11,000 borrowers |

**Note:** For capacity-to-pay computation, use the initial rate. After repricing, the new rate is set by the Pag-IBIG Board and the amortization is recomputed.

---

## 7. Capacity-to-Pay Formula

```
max_monthly_amortization = total_gross_monthly_income × 0.35
```

Inverse amortization to solve for max principal:
```
max_by_capacity = max_monthly_amortization × [(1+r)^n - 1] / [r × (1+r)^n]
```

Where:
- `r` = annual_rate / 12
- `n` = term_years × 12
- `total_gross_monthly_income` = sum of all borrowers' GMI

**Rules:**
- **35% of gross monthly income** is the current threshold (Circular 443 / 403). The older 40% of NDI (Circular 247-09) is superseded.
- For the lowest rate tier (5.5%), a stricter **30% of GMI** may apply.
- For government employees, net take-home pay after deduction must remain above GAA minimum.

---

## 8. Edge Cases and Special Rules

1. **Lump-sum contributions:** Members with <24 months can pay lump-sum to meet the threshold. System must accept both cumulative and lump-sum contribution counts.

2. **Co-borrower income stacking:** Combined GMI of all borrowers used for the 35% capacity test, but each co-borrower must independently meet membership/contribution requirements.

3. **Non-relative co-borrowing (Circular 396):** Allowed ONLY for purchase purpose; property must be in all borrowers' names; all must execute the REM; mortgage released only upon full payment.

4. **Age boundary examples:**
   - 64-year-old: passes ≤65 check; max term = min(30, 70-64) = 6 years
   - 65-year-old: passes ≤65 check; max term = min(30, 70-65) = 5 years
   - 66-year-old: REJECTED (exceeds age 65 limit)

5. **Lot-only LTV:** Some sources cite a lower 70% LTV for lot-only purchases. The standard LTV table doesn't distinguish by property type — this may be a specific program variant. Flagged as conflict.

6. **OFW-specific:** Must have valid OEC + designate Philippine-based attorney-in-fact via SPA. Same 24-month contribution rule.

7. **Mixed-use property:** Residential use must comprise ≥60% of floor area (≤40% for business use).

8. **Medical questionnaire:** Required if borrower >60 years old or loan >₱2,000,000 (for MRI underwriting).

9. **Minimum loan amount:** ₱400,000 cited by one practitioner source but not confirmed in circular text. Treat as soft constraint.

---

## 9. Pseudocode Implementation

```python
def check_pagibig_eligibility(borrower, co_borrowers, property, loan_request):
    """
    Returns: (eligible: bool, max_loan: float, rejection_reason: str | None)
    """
    all_borrowers = [borrower] + co_borrowers

    # Step 1: Membership
    if not borrower.is_active_member:
        return (False, 0, "Not an active Pag-IBIG member")
    if borrower.monthly_contributions_count < 24:
        return (False, 0, "Less than 24 monthly contributions")
    if not borrower.last_contribution_within_6_months:
        return (False, 0, "No contribution in last 6 months")

    # Step 2: Age
    if borrower.age > 65:
        return (False, 0, "Exceeds maximum application age of 65")
    max_term = min(30, 70 - borrower.age)
    if loan_request.term_years > max_term:
        return (False, 0, f"Term exceeds max {max_term} years (maturity beyond age 70)")

    # Step 3: Loan history
    if borrower.has_outstanding_default:
        return (False, 0, "Outstanding Pag-IBIG loan in default")
    if borrower.has_prior_foreclosure:
        return (False, 0, "Prior foreclosed/cancelled Pag-IBIG loan")
    if borrower.has_stl_arrears:
        return (False, 0, "Short-Term Loan in arrears")

    # Step 4: Credit
    if not borrower.passes_credit_check:
        return (False, 0, "Failed credit/background check")

    # Step 5: Property
    if property.type == "lot" and property.area_sqm > 1000:
        return (False, 0, "Lot exceeds 1,000 sqm")
    if loan_request.purpose not in VALID_PURPOSES:
        return (False, 0, "Invalid loan purpose")
    if loan_request.purpose == "refinancing":
        if property.existing_mortgage_years < 2:
            return (False, 0, "Refinancing requires 2-year repayment history")

    # Step 6: Co-borrowers
    if len(co_borrowers) > 2:
        return (False, 0, "Maximum 3 borrowers total")
    for cb in co_borrowers:
        if not cb.is_active_member or cb.monthly_contributions_count < 24:
            return (False, 0, "Co-borrower not qualified")
        if not cb.is_relative_within_2nd_degree:
            if loan_request.purpose != "purchase":
                return (False, 0, "Non-relative co-borrowing only for purchase")

    # Step 7: Loan amount caps
    max_by_program = PROGRAM_LIMITS[loan_request.program]

    max_by_contribution = CONTRIBUTION_TABLE.lookup(borrower.monthly_contribution)

    collateral = min(property.appraised_value, property.selling_price)
    ltv = LTV_TABLE[loan_request.has_buyback].lookup(collateral)
    max_by_ltv = collateral * ltv

    total_gmi = sum(b.gross_monthly_income for b in all_borrowers)
    max_monthly = total_gmi * 0.35
    rate = get_interest_rate(loan_request.program, loan_request.repricing_period)
    r = rate / 12
    n = loan_request.term_years * 12
    max_by_capacity = max_monthly * ((1 + r)**n - 1) / (r * (1 + r)**n)

    max_loan = min(max_by_program, max_by_contribution, max_by_ltv, max_by_capacity)

    if loan_request.amount > max_loan:
        return (True, max_loan, f"Approved at reduced amount: ₱{max_loan:,.2f}")

    return (True, loan_request.amount, None)
```

---

## 10. Legal Citations

| Rule | Legal Basis |
|------|------------|
| Membership & 24-month contributions | RA 9679 (HDMF Law of 2009); HDMF Circular No. 443 |
| Age limits (65 application / 70 maturity) | HDMF Circular No. 443 |
| Capacity to pay (35% GMI) | HDMF Circular No. 443; Circular No. 403 (AHP) |
| Standard EUF ceiling ₱6M | HDMF Circular No. 443 |
| Expanded 4PH ceiling ₱15M | HDMF Circular No. 473 |
| AHP socialized ceilings (2025) | DHSUD-DEPDev JMC 2025-001 |
| LTV ratios | HDMF Circular No. 443 (current); Circular 247-09 (older with/without buyback) |
| Contribution-to-loan table (≤₱3M) | HDMF Circular No. 247-09 |
| Interest rate schedule | Pag-IBIG Board resolution (unchanged through 2025 per Inquirer/PIA) |
| Co-borrower rules | HDMF Circular No. 443; Circular No. 396 (non-relative exception) |
| Default penalty (0.05%/day) | HDMF Circular No. 300 |
| Lot size limit (1,000 sqm) | HDMF EUF standard terms |
| 6-month active contribution recency | HDMF membership rules |

---

## 11. Verification Status

**Overall: CONFIRMED with noted data gaps**

Cross-checked against 10 independent sources:
1. Official Pag-IBIG Fund website (pagibigfund.gov.ph)
2. GreatDay HR — Complete Pag-IBIG Housing Loan Guide (2025)
3. Respicio & Co. law firm commentary
4. LegalDex — HDMF Circular No. 247-09 full text
5. FilipiKnow financial guide
6. OmniCalculator Pag-IBIG housing loan calculator
7. Supreme Court E-Library — Circular 403 full text
8. PIA — Expanded 4PH Program announcement
9. Inquirer — Pag-IBIG home loan rates unchanged 2025
10. Coins.ph — How Much Can You Borrow guide

| Rule | Status |
|------|--------|
| 24-month contribution minimum | **Confirmed** — all 10 sources agree |
| Active contribution recency (6 months) | **Confirmed** — official Pag-IBIG site |
| Age 65/70 limits | **Confirmed** — all sources agree |
| 35% GMI capacity to pay | **Confirmed** — 40% NDI (Circular 247-09) is superseded |
| Program loan ceilings (₱6M / ₱15M) | **Confirmed** |
| Contribution lookup table (≤₱3M) | **Confirmed** — matches Circular 247-09 exactly |
| Contribution table (₱3M–₱6M range) | **DATA GAP** — not publicly documented |
| LTV ratios (retail 100%/90%/80%) | **Confirmed** — retail/no-buyback schedule |
| LTV ratios (buyback 100%/100%/95%/90%) | **Confirmed** — developer-assisted schedule |
| Self-employed 5-year requirement | **REJECTED** — no source supports; 24 months applies uniformly |
| Minimum loan ₱400K | **Unverified** — single practitioner source only |
| AHP ceilings | **Updated** — JMC 2025-001 replaces older Circular 403 amounts |
| Non-relative co-borrower exception | **Confirmed** — per Circular 396, with conditions |
| Co-borrower default restriction applies to co-borrowers too | **Confirmed** — "as principal or co-borrower" |
| Refinancing conditions (2-year + 6-month current) | **Confirmed** — practitioner sources |
| Interest rates unchanged through 2025 | **Confirmed** — Inquirer business reporting |

---

## 12. Data Dependencies for Automation

| Dependency | Type | Update Frequency | Risk |
|-----------|------|-----------------|------|
| Pag-IBIG interest rate table | External lookup | Board resolution (~annually) | Medium — rates held steady 2024-2025 |
| DHSUD housing price ceilings | External lookup | Every 3 years (JMC 2025-001 valid ~2028) | Low |
| Contribution-to-loan entitlement table | External lookup | Per circular amendment (irregular) | High — ₱3M+ range undocumented |
| LTV ratio schedule | External lookup | Per circular amendment (irregular) | Low — stable since Circular 443 |
| CIC credit check result | External API / manual | Real-time | N/A (binary input) |
| Property appraised value | Manual input | Per transaction | N/A (user-provided) |

---

## 13. Cross-References

- **pagibig-amortization** (Wave 2, pending): Uses interest rate from eligibility; MRI/FGI computed on approved amount; shares repricing period input
- **ltv-ratio** (Wave 2, pending): Pag-IBIG has its own LTV schedule (this file); BSP has separate bank LTV rules
- **socialized-housing-compliance** (Wave 2, pending): AHP eligibility ties into DHSUD price ceiling compliance; ceiling lookup table shared
- **ph-tax-computations-reverse**: Documentary stamp tax (1.5% or ₱1.50/₱200) applies on the mortgage document; transfer tax applies on the sale
