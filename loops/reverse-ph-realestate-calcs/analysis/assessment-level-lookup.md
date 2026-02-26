# Computation Extraction: Assessment Level Lookup

**Aspect:** assessment-level-lookup (Wave 2)
**Date:** 2026-02-26
**Verification status:** CONFIRMED — all 34 table values verified against 9 independent sources with zero corrections
**Deterministic:** YES (given classification, FMV, and applicable LGU ordinance)

---

## Overview

The assessment level lookup is the core computation in Philippine real property taxation that converts a property's Fair Market Value (FMV) into its Assessed Value (AV). Every real property tax bill in the country depends on this computation. Land, buildings/improvements, and machinery are assessed **separately** using different tables, then summed.

**Legal basis:** RA 7160 (Local Government Code of 1991), Sections 199, 217, 218; DOF Local Assessment Regulations No. 1-92; RA 12001 (RPVARA, 2024) — preserves Section 218 maximums.

---

## Sub-Computations

### 1. Property Classification Determination

**What it computes:** Assigns a property classification (residential, agricultural, commercial, industrial, mineral, timberland, special) based on actual use.

**Inputs:**
- `actual_use: str` — observed/declared use of the property
- `zoning_classification: str` (optional) — may serve as indicator
- `title_classification: str` (optional) — may serve as indicator

**Logic:**
```
classification = classify_by_actual_use(actual_use)
# Section 217: "Real property shall be classified, valued, and assessed
# on the basis of its actual use regardless of where located, whoever
# owns it, and whoever uses it."
# Zoning/title serve only as indicators, NOT determinants.
```

**Legal citation:** RA 7160, Section 217

**Edge cases:**
- Mixed-use property: each portion classified separately (e.g., ground floor commercial, upper floors residential)
- Idle land: classified per underlying classification + subject to additional idle land levy (Section 236)
- Mineral lands: land classified as "mineral" at 50%; buildings on mineral land classified by actual building use (likely commercial/industrial), NOT a separate mineral building table

**Deterministic:** Yes, given actual use declaration. Classification disputes are resolved via LBAA appeal (Section 226).

---

### 2. Land Assessment Level Lookup

**What it computes:** Assessment level percentage for land, by classification.

**Inputs:**
- `land_classification: str` — one of: residential, agricultural, commercial, industrial, mineral, timberland
- `lgu_ordinance_rates: dict` (optional) — LGU may set rates below statutory maximum

**Lookup table (Section 218(a) — statutory MAXIMUMS):**

| Classification | Max Assessment Level |
|---|---|
| Residential | 20% |
| Agricultural | 40% |
| Commercial | 50% |
| Industrial | 50% |
| Mineral | 50% |
| Timberland | 20% |

**Formula:**
```
land_assessment_level = lgu_ordinance_rates.get(land_classification)
                        ?? section_218a_max[land_classification]
# LGU rates must be ≤ statutory maximums
```

**Legal citation:** RA 7160, Section 218(a)

**Note:** These are FLAT rates (not graduated by FMV). LGUs adopt these at or near maximums in Metro Manila; provincial LGUs may use lower rates.

---

### 3. Building Assessment Level Lookup (Graduated by FMV)

**What it computes:** Assessment level percentage for buildings/improvements, graduated by FMV bracket and classification.

**Inputs:**
- `building_classification: str` — one of: residential, agricultural, commercial/industrial, timberland
- `building_fmv: float` — fair market value of the building (from assessor's BUCC schedule)
- `lgu_ordinance_rates: dict` (optional)

**Lookup tables (Section 218(b) — statutory MAXIMUMS):**

#### (b)(1) Residential Buildings

| FMV Over | FMV Not Over | Max Assessment Level |
|---|---|---|
| — | ₱175,000 | 0% |
| ₱175,000 | ₱300,000 | 10% |
| ₱300,000 | ₱500,000 | 20% |
| ₱500,000 | ₱750,000 | 25% |
| ₱750,000 | ₱1,000,000 | 30% |
| ₱1,000,000 | ₱2,000,000 | 35% |
| ₱2,000,000 | ₱5,000,000 | 40% |
| ₱5,000,000 | ₱10,000,000 | 50% |
| ₱10,000,000 | — | 60% |

#### (b)(2) Agricultural Buildings

| FMV Over | FMV Not Over | Max Assessment Level |
|---|---|---|
| — | ₱300,000 | 25% |
| ₱300,000 | ₱500,000 | 30% |
| ₱500,000 | ₱750,000 | 35% |
| ₱750,000 | ₱1,000,000 | 40% |
| ₱1,000,000 | ₱2,000,000 | 45% |
| ₱2,000,000 | — | 50% |

#### (b)(3) Commercial/Industrial Buildings

| FMV Over | FMV Not Over | Max Assessment Level |
|---|---|---|
| — | ₱300,000 | 30% |
| ₱300,000 | ₱500,000 | 35% |
| ₱500,000 | ₱750,000 | 40% |
| ₱750,000 | ₱1,000,000 | 50% |
| ₱1,000,000 | ₱2,000,000 | 60% |
| ₱2,000,000 | ₱5,000,000 | 70% |
| ₱5,000,000 | ₱10,000,000 | 75% |
| ₱10,000,000 | — | 80% |

#### (b)(4) Timberland Buildings

| FMV Over | FMV Not Over | Max Assessment Level |
|---|---|---|
| — | ₱300,000 | 45% |
| ₱300,000 | ₱500,000 | 50% |
| ₱500,000 | ₱750,000 | 55% |
| ₱750,000 | ₱1,000,000 | 60% |
| ₱1,000,000 | ₱2,000,000 | 65% |
| ₱2,000,000 | — | 70% |

**Formula:**
```python
def building_assessment_level(classification, fmv, lgu_rates=None):
    table = BUILDING_TABLES[classification]  # select table by classification
    for bracket in table:
        if bracket.lower < fmv <= bracket.upper:
            statutory_max = bracket.rate
            break
    if lgu_rates:
        return min(lgu_rates[classification][bracket_index], statutory_max)
    return statutory_max
```

**Edge cases:**
- FMV exactly at bracket boundary: falls into the lower bracket ("over X" means strictly >X)
- No separate table for mineral buildings — classified by actual building use per Section 217 (typically commercial/industrial)
- Buildings valued ≤₱175,000 (residential): 0% assessment = effectively tax-exempt

**Legal citation:** RA 7160, Section 218(b)

---

### 4. Machinery Assessment Level Lookup

**What it computes:** Assessment level percentage for machinery, by classification.

**Inputs:**
- `machinery_classification: str` — one of: agricultural, residential, commercial, industrial
- `lgu_ordinance_rates: dict` (optional)

**Lookup table (Section 218(c) — statutory MAXIMUMS):**

| Classification | Max Assessment Level |
|---|---|
| Agricultural | 40% |
| Residential | 50% |
| Commercial | 80% |
| Industrial | 80% |

**Legal citation:** RA 7160, Section 218(c)

**Note:** Machinery depreciates per Section 225 — max 5% annual depreciation, minimum 20% residual value. This affects FMV, not the assessment level.

---

### 5. Special Classes Assessment Level

**What it computes:** Reduced assessment levels for properties with special public-interest uses.

**Inputs:**
- `property_use: str` — one of: cultural, scientific, hospital, local_water_district, gocc_water_power

**Lookup table (Section 218(d) — statutory MAXIMUMS):**

| Use | Max Assessment Level |
|---|---|
| Cultural | 15% |
| Scientific | 15% |
| Hospital | 15% |
| Local water districts | 10% |
| GOCCs (water/power) | 10% |

**Legal citation:** RA 7160, Section 218(d)

---

### 6. Total Assessed Value Computation

**What it computes:** Combined assessed value for a property with multiple components.

**Inputs:**
- `land_fmv: float`
- `land_classification: str`
- `building_fmv: float` (0 if bare land)
- `building_classification: str`
- `machinery_fmv: float` (0 if none)
- `machinery_classification: str`
- `lgu_rates: dict` (optional)

**Formula:**
```python
def total_assessed_value(land_fmv, land_class, building_fmv, building_class,
                         machinery_fmv, machinery_class, lgu_rates=None):
    land_av = land_fmv * land_assessment_level(land_class, lgu_rates)
    building_av = building_fmv * building_assessment_level(building_class, building_fmv, lgu_rates)
    machinery_av = machinery_fmv * machinery_assessment_level(machinery_class, lgu_rates)
    return land_av + building_av + machinery_av
```

**Legal citation:** RA 7160, Sections 199(h), 218

---

### 7. RPT Computation (Full Pipeline)

**What it computes:** Annual real property tax due.

**Inputs:**
- All inputs from Sub-computation 6 (assessed value)
- `lgu_type: str` — "province" or "city_metro_manila"
- `lgu_basic_rpt_rate: float` — basic RPT rate set by LGU ordinance
- `sef_rate: float` — always 1% (Section 235)
- `idle_land: bool` — whether property is idle
- `idle_land_rate: float` — idle land levy rate per LGU ordinance (max 5%)

**Formula:**
```python
def compute_rpt(assessed_value, lgu_basic_rpt_rate, lgu_type,
                idle_land=False, idle_land_rate=0):
    # Validate rate against statutory caps
    max_basic_rate = 0.02 if lgu_type == "city_metro_manila" else 0.01
    assert lgu_basic_rpt_rate <= max_basic_rate

    basic_rpt = assessed_value * lgu_basic_rpt_rate
    sef = assessed_value * 0.01  # always 1% (Section 235)
    idle_levy = assessed_value * idle_land_rate if idle_land else 0  # max 5% (Section 236)

    total_rpt = basic_rpt + sef + idle_levy
    return total_rpt
```

**Rate caps:**
- Province: max 1% basic RPT (Section 233(a))
- City / municipality within Metro Manila: max 2% basic RPT (Section 233(b))
- SEF: additional 1% (Section 235)
- Idle land: additional max 5% (Section 236, optional per LGU ordinance)

**Legal citation:** RA 7160, Sections 233, 235, 236

---

### 8. Payment Penalties and Discounts

**What it computes:** Adjusted RPT amount for early/late payment.

**Inputs:**
- `total_rpt: float`
- `payment_date: date`
- `due_date: date`
- `lgu_discount_rate: float` — advance payment discount (max 20%)

**Formula:**
```python
def adjusted_rpt(total_rpt, payment_date, due_date, lgu_discount_rate=0):
    if payment_date <= january_deadline:  # advance/prompt full-year payment
        return total_rpt * (1 - lgu_discount_rate)  # max 20% discount
    elif payment_date > due_date:
        months_late = ceil((payment_date - due_date).days / 30)
        months_late = min(months_late, 36)  # max 36 months
        penalty = total_rpt * 0.02 * months_late  # 2% per month
        return total_rpt + penalty
    else:
        return total_rpt
```

**Legal citation:** RA 7160, Section 251 (discount), Section 255 (penalty)

**Notes:**
- Quarterly payment: RPT may be paid in 4 equal installments (March 31, June 30, Sep 30, Dec 31)
- Advance payment discount: up to 20% per Section 251, set by LGU
- Penalty: 2% per month of delinquency, max 36 months = 72% maximum surcharge

---

## Building FMV Determination Pipeline (Context for Assessment)

While assessment levels are deterministic lookup tables, the **FMV input** to those tables depends on a semi-deterministic pipeline controlled by local assessors:

1. **Land FMV:** Determined from LGU's Schedule of Market Values (SMV) — a table of ₱/sqm values by zone/street/barangay
   - `land_fmv = lot_area_sqm × unit_market_value_per_sqm`

2. **Building FMV:** Determined from Schedule of Base Unit Construction Cost (BUCC)
   - `replacement_cost_new = total_floor_area × bucc_rate_per_sqm`
   - `building_fmv = replacement_cost_new × (1 - depreciation_rate)`
   - BUCC rates vary by: construction type (reinforced concrete, wood, steel, etc.), number of floors, LGU

3. **Machinery FMV:** Original cost minus depreciation (Section 225)
   - Max annual depreciation: 5% of original/replacement/reproduction cost
   - Minimum residual value: 20% of cost while still useful/operational
   - `machinery_fmv = max(cost × (1 - 0.05 × age), cost × 0.20)`

**Note:** SMV and BUCC schedules are LGU-specific. Under RA 12001 (RPVARA), these will be standardized via DOF-approved Philippine Valuation Standards within 2 years of the law's effectivity (July 2024).

---

## RA 12001 (RPVARA) Impact

RA 12001, signed June 13, 2024, reforms the valuation framework but **explicitly preserves Section 218 assessment level maximums**:

- **Section 29 of RA 12001:** "the maximum assessment levels in Section 218 of RA No. 7160 shall be observed"
- **Valuation reform:** Replaces the three-base system (BIR zonal, LGU SMV, actual price) with a single DOF-approved Schedule of Market Values (SMV)
- **Transition 6% cap:** "For the first year of effectivity of the approved SMV...any increase in real property taxes shall be limited to a maximum of six percent (6%) of the real property taxes assessed...prior to the effectivity of this Act"
  - Triggers on approved SMV effectivity, NOT law effectivity
- **Sections repealed:** 199(e), (g), (o); 212; 219 of RA 7160
- **Sections amended:** 19, 135(a), 138, 201, 218, 220, 472(b)(8) of RA 7160 — "insofar as inconsistent"
- **General revision:** Every 3 years after initial 2-year update (replaces old Section 219)
- **Tax amnesty:** 2-year amnesty on penalties/surcharges/interest for unpaid RPT prior to RPVARA effectivity

**Automation implication:** Assessment level lookup tables remain valid and unchanged. The reform affects how FMV is determined (input), not how assessment levels are applied (computation). However, the 6% transition cap on RPT increases adds a new computation layer.

---

## Decision Tree: Full Assessment Level Lookup

```
INPUT: property components (land, building, machinery), FMV of each, classification, LGU

For each component:
  1. Determine classification (Section 217: by actual use)
  2. Check if special class (Section 218(d)) → use special rates
  3. If LAND → flat rate lookup from Section 218(a) by classification
  4. If BUILDING → graduated rate lookup from Section 218(b) by classification + FMV bracket
     - Select sub-table: residential / agricultural / commercial-industrial / timberland
     - Find FMV bracket (strictly "over X, not over Y")
     - Return rate
  5. If MACHINERY → flat rate lookup from Section 218(c) by classification
  6. Compute: component_AV = component_FMV × assessment_level

TOTAL_AV = sum of all component AVs

RPT = TOTAL_AV × basic_rpt_rate + TOTAL_AV × 0.01 (SEF) [+ idle land levy if applicable]

Adjust for: early payment discount (max 20%) OR late penalty (2%/month, max 36 months)
```

---

## Worked Examples

### Example 1: House and Lot in Metro Manila (City)

**Given:**
- Land: 200 sqm residential, FMV ₱4,000,000
- Building: residential, FMV ₱2,000,000
- LGU basic RPT rate: 2% (Metro Manila max)

**Computation:**
```
Land AV = ₱4,000,000 × 20% (residential land) = ₱800,000
Building AV = ₱2,000,000 × 40% (residential bldg ₱2M-₱5M bracket) = ₱800,000
Total AV = ₱800,000 + ₱800,000 = ₱1,600,000

Basic RPT = ₱1,600,000 × 2% = ₱32,000
SEF = ₱1,600,000 × 1% = ₱16,000
Total annual RPT = ₱48,000
```

### Example 2: Commercial Building in Province

**Given:**
- Land: 500 sqm commercial, FMV ₱10,000,000
- Building: commercial, FMV ₱15,000,000
- Machinery: commercial, FMV ₱500,000
- LGU basic RPT rate: 1%

**Computation:**
```
Land AV = ₱10,000,000 × 50% (commercial land) = ₱5,000,000
Building AV = ₱15,000,000 × 80% (commercial bldg >₱10M bracket) = ₱12,000,000
Machinery AV = ₱500,000 × 80% (commercial machinery) = ₱400,000
Total AV = ₱5,000,000 + ₱12,000,000 + ₱400,000 = ₱17,400,000

Basic RPT = ₱17,400,000 × 1% = ₱174,000
SEF = ₱17,400,000 × 1% = ₱174,000
Total annual RPT = ₱348,000
```

### Example 3: Agricultural Land (No Improvements)

**Given:**
- Land: 10,000 sqm agricultural, FMV ₱500,000
- LGU basic RPT rate: 0.75% (below max)

**Computation:**
```
Land AV = ₱500,000 × 40% (agricultural land) = ₱200,000

Basic RPT = ₱200,000 × 0.75% = ₱1,500
SEF = ₱200,000 × 1% = ₱2,000
Total annual RPT = ₱3,500
```

---

## External Data Dependencies

| Dependency | Source | Update Frequency | Automation Impact |
|---|---|---|---|
| LGU assessment level ordinances | Individual LGU sanggunian | Irregular (many LGUs adopt statutory max) | Must track per-LGU; default to Section 218 max |
| LGU basic RPT rate | Individual LGU tax ordinance | Rarely changed | Must store per-LGU |
| Schedule of Market Values (land) | LGU assessor → BLGF (under RPVARA) | Every 3 years (target) | LGU-specific; will be standardized |
| Schedule of BUCC (buildings) | LGU assessor → BLGF | Every 3 years (target) | LGU-specific; will be standardized |
| NHSB idle land classification | NHSB | Irregular | Binary: idle or not |
| RA 12001 transition cap | DOF/BLGF | One-time per LGU SMV approval | Adds computation layer for first year |

---

## Unresolved Ambiguities

1. **RA 12001 "insofar as inconsistent" amendment scope:** The exact interplay between the new SMV-based system and Section 218 brackets is unclear. If new SMVs produce very different FMVs, the bracket thresholds (e.g., ₱175,000 residential building threshold) may become effectively meaningless (most buildings would fall in highest bracket). Congress has not updated the bracket amounts since 1991.
2. **LGU assessment level ordinances below statutory max:** No centralized database exists. Automation must either default to Section 218 maximums or maintain per-LGU lookups.
3. **Mixed-use allocation methodology:** No statutory formula for how to split a mixed-use property between classifications. Practice varies by LGU.
4. **Building FMV bracket boundary treatment:** "Over ₱175,000" — does a building valued at exactly ₱175,000 fall in the 0% or 10% bracket? Standard interpretation: exactly ₱175,000 is in the ≤₱175,000 bracket (0%).
5. **1991 bracket thresholds vs. 2025 property values:** With inflation, virtually all Metro Manila residential buildings now exceed the ₱10M bracket (60% rate). The brackets have never been inflation-adjusted.

---

## Verification Summary

All 34 individual table values across 7 tables verified against 9 independent sources with **zero numerical corrections needed**. See `analysis/assessment-level-lookup-verification.md` for full verification report.

Key verification findings:
- All land rates (6 classifications): CONFIRMED across all sources
- All building brackets (29 values across 4 sub-tables): CONFIRMED
- All machinery rates (4 classifications): CONFIRMED
- All special class rates (5 categories): CONFIRMED
- RPT rate caps (1%/2%): CONFIRMED (Section 233)
- SEF additional 1%: CONFIRMED (Section 235)
- Idle land max 5%: CONFIRMED (Section 236)
- Section 225 depreciation (machinery only): CONFIRMED
- RA 12001 preservation of Section 218: CONFIRMED
- Mineral land buildings: no separate table; classified by actual use (likely commercial/industrial)

**Structural clarification:** The 6% transition cap in RA 12001 applies to the first year of effectivity of the approved SMV per LGU, NOT the first year of the law itself.
