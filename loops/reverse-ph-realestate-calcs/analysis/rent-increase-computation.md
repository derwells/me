# Rent Increase Computation — Rent Control Act (RA 9653)

**Wave 2 — Computation Extraction**
**Date:** 2026-02-26
**Source:** `input/rent-control-act.md` (Wave 1)
**Verification:** 12 independent sources across 5 categories; 1 critical correction, 1 moderate, 2 nuanced claims
**Deterministic:** YES (given current year's NHSB resolution rate)

---

## 1. Computations Extracted

### Computation 1: Coverage Determination

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `unit_type` | enum: `residential` / `commercial` / `mixed` | Lease contract |
| `monthly_rent` | decimal (₱) | Current lease terms |
| `location_type` | enum: `NCR_HUC` / `other` | LGU classification |
| `lessee_changed` | boolean | Lease history |
| `is_newly_constructed` | boolean | Building permit / TCT date |
| `current_year` | integer | System clock |

**Decision Tree:**
```
1. IF unit_type == "commercial" → NOT COVERED (exit)
2. IF unit_type == "mixed" AND NOT principally_dwelling → NOT COVERED (exit)
3. IF is_hotel_motel_tourist_inn → NOT COVERED (exit)
4. IF is_newly_constructed AND first_time_offered → NOT COVERED (exit)
   [HUDCC Res. 01-17; carried forward in subsequent resolutions]
5. IF has_written_rent_to_own_agreement → NOT COVERED by Sec 5 thresholds
   [RA 9653 Sec 11; ambiguity flag — see Edge Cases]
6. DETERMINE threshold:
   IF location_type == "NCR_HUC": threshold = ₱10,000
   ELSE: threshold = ₱5,000
7. IF monthly_rent > threshold → NOT COVERED (exit)
8. IF lessee_changed → NOT COVERED for this period
   [Vacancy exception: lessor may set any initial rent for new lessee]
9. IF current_year NOT in active regulation period → NOT COVERED
10. → COVERED: proceed to Computation 2
```

**Legal basis:** RA 9653 Sections 3–5, 11; NHSB/HUDCC extending resolutions

**Notes:**
- The ₱5,000 threshold for non-HUC areas has NEVER been adjusted since 2009 (confirmed across all sources)
- "Highly Urbanized City" list: ~33 HUCs in PH; classification changes per LGU reclassification
- "Same lessee" encompasses renewals, extensions, and month-to-month continuations — vacancy exception triggers only on physical vacatur + different lessee

---

### Computation 2: Allowable Rent Increase

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `current_monthly_rent` | decimal (₱) | Current lease |
| `current_year` | integer | System clock |

**Step 1 — Determine cap percentage by year and bracket:**

**Complete Historical Rate Table (2010–2026):**

| Period | Resolution | Bracket 1 | Bracket 2 | Bracket 3 |
|--------|-----------|-----------|-----------|-----------|
| 2010–2013 | RA 9653 Sec 4 | 7% (all ≤₱10K) | — | — |
| 2014–2015 | HUDCC Res. No. 2, s.2013 | 7% (all ≤₱10K) | — | — |
| 2016–2017 | HUDCC Res. No. 1, s.2015 | 4% (₱1–₱3,999) | 7% (₱4,000–₱10,000) | — |
| **2018–2020** | **HUDCC Res. No. 01-17** | **2% (₱1–₱4,999)** | **7% (₱5,000–₱8,999)** | **11% (₱9,000–₱10,000)** |
| 2021 | NHSB Res. 2020-04 | 2% (₱1–₱4,999) | 7% (₱5,000–₱8,999) | 11% (₱9,000–₱10,000) |
| 2022 | NHSB Res. 2021-02 | 2% (₱1–₱4,999) | 7% (₱5,000–₱8,999) | 11% (₱9,000–₱10,000) |
| 2023 | NHSB Res. 2022-01 | 2% (₱1–₱4,999) | 7% (₱5,000–₱8,999) | 11% (₱9,000–₱10,000) |
| 2024 | NHSB Res. 2023-03 | 4% (all ≤₱10K) | — | — |
| 2025 | NHSB Res. 2024-01 | 2.3% (all ≤₱10K) | — | — |
| 2026 | NHSB Res. 2024-01 | 1% (all ≤₱10K) | — | — |

**Tiered bracket lookup (2016–2023):**
```python
def get_cap_pct(year: int, monthly_rent: float) -> float:
    if year in range(2010, 2016):
        return 0.07  # uniform
    elif year in range(2016, 2018):
        # Two-tier (HUDCC Res. No. 1, s.2015)
        return 0.04 if monthly_rent <= 3999 else 0.07
    elif year in range(2018, 2024):
        # Three-tier (HUDCC Res. 01-17, carried forward by NHSB)
        if monthly_rent <= 4999:
            return 0.02
        elif monthly_rent <= 8999:
            return 0.07
        else:
            return 0.11
    elif year == 2024:
        return 0.04  # uniform (NHSB Res. 2023-03)
    elif year == 2025:
        return 0.023  # uniform (NHSB Res. 2024-01)
    elif year == 2026:
        return 0.01  # uniform (NHSB Res. 2024-01)
    else:
        raise ValueError("No active regulation or rate not yet published")
```

**Step 2 — Compute allowable increase:**
```
max_increase_amount = current_monthly_rent × cap_pct
max_new_rent = current_monthly_rent + max_increase_amount
           = current_monthly_rent × (1 + cap_pct)
```

**Compounding rule:** Each year's cap applies to the **immediately preceding rent**, not the original/base rent. Year 3 increase is computed on Year 2's actual rent.

**Worked Example (2025, ₱8,000/month):**
```
cap_pct = 0.023 (2025 uniform)
max_increase = ₱8,000 × 0.023 = ₱184
max_new_rent = ₱8,184
```

**Worked Example (2023 tiered, ₱9,500/month):**
```
cap_pct = 0.11 (₱9,000–₱10,000 bracket)
max_increase = ₱9,500 × 0.11 = ₱1,045
max_new_rent = ₱10,545
NOTE: If new rent > ₱10,000, unit exits coverage for future years
```

**Legal basis:** RA 9653 Sec 4; HUDCC/NHSB resolutions per period (see table above)

---

### Computation 3: First-Year Freeze Check

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `lease_start_date` | date | Lease contract |
| `proposed_increase_date` | date | Lessor notice |

**Formula:**
```
months_elapsed = (proposed_increase_date - lease_start_date) in months
IF months_elapsed < 12 → FREEZE: no increase allowed
ELSE → proceed to cap computation
```

**Legal basis:** RA 9653 Sec 4 ("For a period of one (1) year from its effectivity, no increase shall be imposed")

---

### Computation 4: Advance Rent / Deposit Compliance Check

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `advance_rent_months` | integer | Lease contract |
| `deposit_months` | integer | Lease contract |

**Rules:**
```
IF advance_rent_months > 1 → VIOLATION (RA 9653 Sec 7)
IF deposit_months > 2 → VIOLATION (RA 9653 Sec 7)
```

**Legal basis:** RA 9653 Sec 7

---

### Computation 5: Deposit Interest Return

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `deposit_amount` | decimal (₱) | Lease contract |
| `savings_rate` | decimal (annual %) | Bank prevailing rate |
| `tenure_months` | integer | Lease duration |

**Formula:**
```
accrued_interest = deposit_amount × (savings_rate / 12) × tenure_months
amount_due_to_lessee = deposit_amount + accrued_interest - deductions
  where deductions = unpaid_rent + unpaid_utilities + documented_damage
```

**Legal basis:** RA 9653 Sec 7 ("deposit shall be kept in a bank under the name of the lessor"; "accrued interest shall be returned to the lessee")

---

### Computation 6: Multi-Year Rent Projection

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `starting_rent` | decimal (₱) | Current lease |
| `location_type` | enum | LGU classification |
| `years_forward` | integer | Projection horizon |
| `cap_schedule` | list[(year, rate)] | Published NHSB schedule |

**Formula (compounding):**
```
rent[0] = starting_rent
for i in 1..years_forward:
    cap_pct = lookup_cap(year + i, rent[i-1])
    rent[i] = rent[i-1] × (1 + cap_pct)
    # Check: does rent[i] exit coverage?
    threshold = 10000 if location_type == "NCR_HUC" else 5000
    if rent[i] > threshold:
        # Unit exits coverage; no further cap applies
        break
```

**Note:** Projection is only deterministic for years with published cap rates. Beyond current NHSB resolution period (2026), rates are unknown.

---

## 2. Edge Cases and Special Rules

### 2.1 Coverage Exit via Rent Increase
If a tiered increase pushes rent above ₱10,000 (or ₱5,000 for non-HUC), the unit exits coverage. The 2023 example above (₱9,500 → ₱10,545) demonstrates this. Once exited, the lessor can set any rent going forward.

### 2.2 Vacancy Reset
When a covered unit becomes vacant:
1. Lessor may set any initial rent for the new lessee (no cap on initial amount)
2. The first 12 months of the new tenancy are a freeze period (no further increase)
3. After 12 months, the cap applies based on the new initial rent as base
4. If new initial rent > threshold, unit is outside coverage entirely

### 2.3 Student Boarding Houses / Dormitories
Cap rate applies same as residential, but with additional constraint: increases may occur at most **once per year** (no mid-year adjustments).

### 2.4 Subletting
- Subletting requires written lessor consent (RA 9653 Sec 8(a))
- Unauthorized subletting is grounds for judicial ejectment (Sec 9)
- Subletting does NOT change "same lessee" status — original lessee remains the covered party
- Sublessee has no direct rent control relationship with lessor

### 2.5 Escalation Clause Prohibition
Lease contracts with automatic escalation clauses (tied to inflation, CPI, etc.) are prohibited for covered units. The only permissible increase is the NHSB-published cap rate.

### 2.6 Newly Constructed Units Exemption
Per HUDCC Res. 01-17 (carried forward): newly constructed residential units offered for lease **for the first time** are exempt from rent control. This exemption applies only to the initial offering; once a first lease is established, subsequent renewals/re-lettings are subject to coverage.

### 2.7 Rent-to-Own Ambiguity (FLAG: MANUAL REVIEW)
RA 9653 Sec 11 exempts rent-to-own units from Sec 5 coverage thresholds. However, it is ambiguous whether the Sec 4 increase cap still applies to lease payments during the rent-to-own period. If the unit is exempt from coverage, it is arguably also exempt from the cap. This requires legal interpretation — flagged as non-deterministic for this specific edge case.

### 2.8 "Same Lessee" Interpretation
- **Renewal** (new contract, same person): still "same lessee" → cap applies
- **Extension** (contract extended): still "same lessee" → cap applies
- **Month-to-month holdover**: still "same lessee" → cap applies
- **Assignment of lease** (with consent): new lessee → vacancy exception may apply (unsettled)
- **Death of lessee**: heirs may continue occupancy under Civil Code succession rules; "same lessee" status is arguable — flag for manual review

---

## 3. Verification Status

### Sources Consulted (12)
1. RA 9653 full text (LawPhil)
2. NHSB Res. 2024-01 (DHSUD PDF)
3. PNA news article (Jan 2025)
4. Manila Tribune (Jan 2025)
5. DHSUD official news (Dec 2023)
6. NHSB Res. 2022-01 (DHSUD PDF)
7. Aranas Cruz Law firm explainer
8. Salenga Law Firm explainer
9. HUDCC Res. 01-17 (Legaldex)
10. Respicio & Co. commentary (partially unreliable — see below)
11. Philippine Star (Dec 2023)
12. HUDCC Q&A

### Verification Matrix
| Claim | Status |
|-------|--------|
| Coverage thresholds (₱10K/₱5K) | **CONFIRMED** (all 12 sources) |
| Same-lessee requirement | **CONFIRMED** (statute + all resolutions) |
| Allowable increase formula | **CONFIRMED** (compound on preceding rent) |
| 2010–2015 rates (7% uniform) | **CONFIRMED** |
| 2016–2017 rates (4%/7% two-tier) | **CONFIRMED** |
| 2018–2020 rates | **CORRECTED**: 2%/7%/11% three-tier (not "prevailing rates") |
| 2021–2023 rates (2%/7%/11%) | **CONFIRMED** |
| 2024 rate (4% uniform) | **CONFIRMED** |
| 2025 rate (2.3% uniform) | **CONFIRMED** |
| 2026 rate (1% uniform) | **CONFIRMED** |
| Vacancy exception | **CONFIRMED with nuance** (interacts with 12-month freeze) |
| Advance rent/deposit limits | **CONFIRMED** |
| First-year freeze | **CONFIRMED** |
| Student boarding rule | **CONFIRMED** |
| Post-2026 deregulation mandate | **CONFIRMED but never triggered** in practice |

### Corrections Applied
1. **CRITICAL**: 2018–2020 period rates specified as three-tier (2%/7%/11%) from HUDCC Res. 01-17. Primary Wave 1 extraction was vague ("extended at prevailing rates").
2. **MODERATE**: Bracket boundaries clarified — resolutions use inclusive peso ranges (₱1–₱4,999, ₱5,000–₱8,999, ₱9,000–₱10,000). Integer peso amounts make `<=` boundaries equivalent to `<` next tier.
3. **MINOR**: Added newly constructed units exemption (HUDCC Res. 01-17, carried forward).
4. **REJECTED**: Respicio & Co. claims about Joint Resolution No. 1 (Dec 2024) raising thresholds to ₱12K/₱8K and setting 5% cap through 2027 — could NOT be verified against any government or news source. Likely AI-generated or speculative content.

### Unresolved Ambiguities
1. **Rent-to-own cap applicability**: Sec 11 exempts from Sec 5 thresholds; unclear if Sec 4 cap still binds
2. **Lease assignment "same lessee" status**: When lease is assigned with consent, does vacancy exception apply?
3. **Death of lessee**: Do heirs inherit "same lessee" status?
4. **Post-2026 framework**: Section 16 transition program has never been implemented despite statutory mandate; unclear what happens after NHSB Res. 2024-01 expires

---

## 4. Data Dependencies

| Dependency | Type | Update Frequency |
|------------|------|-----------------|
| Cap percentage | External (NHSB resolution) | Annual or biennial |
| HUC list | External (PSA/DILG) | Irregular (LGU reclassification) |
| Coverage thresholds | External (NHSB; never changed) | Potentially per resolution |
| Prevailing savings rate | External (BSP/bank) | Quarterly |

**Critical dependency:** The cap percentage is NOT embedded in statute — it is set by NHSB resolution, typically published in December for the following year. Any automation engine must maintain a lookup table of cap rates by year, updated annually when new resolutions are published.

---

## 5. Cross-Reference

- **Tax implications on rental income:** See `loops/ph-tax-computations-reverse/` — landlord income tax, VAT on rental income (>₱3M threshold), withholding tax on rental payments
- **Deposit interest computation** connects to BSP prevailing savings rate data
- **Maceda Law (analysis/maceda-refund.md):** Distinct statute, but both protect lessees/buyers against excessive charges by lessors/sellers

---

## 6. Automation Potential (preliminary)

**6 sub-computations identified:**
1. Coverage determination — fully deterministic decision tree
2. Allowable rent increase — simple formula with annual lookup table
3. First-year freeze check — date arithmetic
4. Advance rent/deposit compliance — trivial comparison
5. Deposit interest return — standard interest calculation
6. Multi-year rent projection — iterative application of cap schedule

**Complexity:** LOW to MODERATE. The main complexity is the external data dependency (annual NHSB rates) and the tiered bracket lookup for historical years. The computation itself is straightforward arithmetic.

**High automation value:** Coverage determination + allowable increase + multi-year projection form a natural calculator product. The vacancy reset logic and coverage exit tracking add differentiation over simple percentage calculators.
