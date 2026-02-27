# Computation Extraction: Improvement Depreciation

**Aspect:** improvement-depreciation (Wave 2)
**Date:** 2026-02-27
**Verification status:** VERIFIED — 7 claims CONFIRMED, 3 CORRECTED, 1 CONFIRMED with corrections, 1 UNVERIFIED (see Verification Summary below)
**Deterministic:** YES (given construction type, age, maintenance degree, and LGU depreciation table)

---

## Overview

Building/improvement depreciation is a critical intermediate computation in Philippine real property tax assessment. It converts a building's Replacement Cost New (RCN) into its Fair Market Value (FMV) by deducting accumulated depreciation. This depreciated FMV then feeds into the assessment level lookup (see `analysis/assessment-level-lookup.md`) to compute assessed value and ultimately RPT.

**Critical distinction:** Building depreciation for RPT assessment is governed by **DOF Local Assessment Regulations No. 1-92** (Sections 40-41), NOT by Sections 224-225 of the LGC — those sections cover **machinery only**.

**Legal basis:**
- DOF Local Assessment Regulations No. 1-92, Sections 40-41 (implementing RA 7160 Sections 201, 219)
- PD 1096 (National Building Code) — construction type classification
- RA 7160 Sections 224-225 — machinery appraisal and depreciation only
- RA 12001 (RPVARA, 2024) — requires depreciation consideration in valuation (Section 14); mandates SMV updates within 2 years of effectivity (by July 2026) in accordance with PVS; principle-based, does not prescribe specific depreciation methodology

---

## Sub-Computations

### 1. Building Construction Type Classification

**What it computes:** Assigns a building construction type based on structural materials, which determines the applicable BUCC rate and depreciation schedule.

**Inputs:**
- `structural_system: str` — primary structural material (wood, mixed, steel, concrete)
- `wall_material: str` — wall construction material
- `roof_material: str` — roof construction material
- `foundation_type: str` — foundation type
- `fire_resistance: str` — fire resistance rating

**CRITICAL: Two distinct classification systems exist with INVERTED numbering:**

**PD 1096 (National Building Code) — 5 types:**

| Type | Description | Primary Material |
|------|-------------|-----------------|
| Type I | Wood construction | Wood/timber |
| Type II | Wood with fire-resistant features, 1-hour fire-resistive | Mixed/wood-fire-resistant |
| Type III | Masonry and wood, incombustible exterior walls | Masonry-wood |
| Type IV | Steel, iron, concrete, or masonry | Steel/concrete/masonry |
| Type V | Fire-resistive (4-hour throughout) | RC/fire-resistive |

**Assessor Practice (BUCC/Depreciation) — inverted numbering:**

| Type | Sub-types | Description | Primary Material |
|------|-----------|-------------|-----------------|
| Type I | A, B | Reinforced concrete, steel (highest quality) | RC/steel |
| Type II | A, B, C | Semi-concrete, mixed | Semi-concrete |
| Type III | A, B, C, D | Wood construction | Wood |
| Type IV | A | Temporary/makeshift (lowest quality) | Light materials |

**Sub-type granularity:** Within each type, sub-types (A, B, C, D) differentiate by quality of finish, structural refinement, and material grade. Local assessors define standard base specifications for each sub-type in their SFMV ordinance. Sub-types are an **assessor convention**, NOT from PD 1096. The Batangas system has approximately 10 sub-classifications (I-A, I-B, II-A, II-B, II-C, III-A, III-B, III-C, III-D, IV-A).

**Legal citation:** PD 1096 Section 401 (NBC types); DOF LAR 1-92 (assessor BUCC classification). The assessor classification is derived from but not identical to PD 1096.

**Edge cases:**
- Mixed construction (e.g., concrete ground floor, wood upper floor): classified by predominant material or worst-case for fire rating
- Renovated buildings: reclassified if renovation changes structural system

**Deterministic:** Yes, given physical inspection data.

---

### 2. Replacement Cost New (RCN) Computation

**What it computes:** The cost of reproducing a new replica of the building using current construction materials and labor costs.

**Inputs:**
- `total_floor_area_sqm: float` — total floor area in square meters
- `construction_type: str` — Type I-A through Type IV
- `bucc_rate: float` — Base Unit Construction Cost per sqm from LGU SFMV (₱/sqm)
- `adjustment_factors: list[float]` — addition/deduction percentages for deviations from standard

**Formula:**
```python
def replacement_cost_new(floor_area_sqm, bucc_rate, adjustment_factors=None):
    base_rcn = floor_area_sqm * bucc_rate
    if adjustment_factors:
        total_adjustment = sum(adjustment_factors)  # can be positive or negative
        rcn = base_rcn * (1 + total_adjustment)
    else:
        rcn = base_rcn
    return rcn
```

**BUCC rates:** LGU-specific, derived from DPWH construction cost data. Example ranges (vary widely by LGU and year):
- Type IV (RC residential): ₱15,000–₱25,000/sqm
- Type III (semi-concrete): ₱8,000–₱15,000/sqm
- Type II (mixed): ₱5,000–₱10,000/sqm
- Type I (wood): ₱3,000–₱7,000/sqm

**Adjustment factors** (DOF LAR 1-92): Account for deviations from the standard classification — expressed as percentage of BUCC. Examples include:
- Quality of finish (above/below standard)
- Number of floors
- Special features (elevator, central air conditioning)
- Building condition at time of assessment

**Legal citation:** DOF LAR 1-92, Sections 38-39 (BUCC schedule preparation); "Quantitative analysis method of the reproduction cost (new) approach"

**External data dependency:** BUCC schedule is LGU-specific, updated with each general revision (target: every 3 years per RA 12001). No national centralized database.

**Deterministic:** Yes, given BUCC rate and adjustment factors.

---

### 3. Physical Depreciation — Age-Life Method

**What it computes:** The depreciation deduction from RCN based on the building's effective age relative to its total economic life.

**Inputs:**
- `rcn: float` — Replacement Cost New
- `effective_age: int` — effective age in years (may differ from actual age)
- `economic_life: int` — total economic life in years (by construction type)

**Formula:**
```python
def physical_depreciation_age_life(rcn, effective_age, economic_life):
    depreciation_rate = effective_age / economic_life
    depreciation_rate = min(depreciation_rate, 1.0)  # cannot exceed 100%
    depreciation = rcn * depreciation_rate
    return depreciation
```

**Economic life by construction type (commonly used by Philippine assessors):**

| Construction Type | Economic Life (Years) | Source |
|---|---|---|
| Type IV — Reinforced Concrete | 50–60 | Assessor practice, Colliers PH |
| Type III-D — Steel Frame | 30–40 | Assessor practice |
| Type III (A-C) — Semi-concrete | 25–35 | Assessor practice |
| Type II — Mixed/wood-fire-resistant | 20–30 | Assessor practice |
| Type I — Wood/timber | 20–25 | Assessor practice |

**Note:** These are NOT statutory values. The LGC does not prescribe economic life for buildings. Each LGU's assessor determines economic life based on local conditions, construction quality, and climate factors (typhoons, earthquakes in PH). The values above are practitioner consensus.

**Comparison: COA useful life for government accounting (COA Circular 2003-007):**

| Building Type | COA Useful Life | Assessment Useful Life |
|---|---|---|
| Reinforced Concrete | 30 years | 50–60 years |
| Steel | 25–30 years | 30–40 years |
| Semi-concrete | 15–20 years | 25–35 years |
| Wood | 10–15 years | 20–25 years |

COA figures are for **accounting depreciation** (book value write-off) and are consistently shorter than assessor economic life estimates (physical life for tax assessment).

**Legal citation:** DOF LAR 1-92 Section 40 ("combined observed depreciation and effective age method")

**Edge cases:**
- Building at or beyond economic life: depreciation rate = 100%, but LGU tables may still show positive percent good
- Well-maintained old buildings: effective age < actual age (see Sub-computation 4)
- Building with renovations: effective age adjusted downward

**Deterministic:** Yes, given effective age and economic life parameters.

---

### 4. Effective Age Determination

**What it computes:** The effective age of a building, which may differ from its actual (chronological) age based on renovation history and maintenance condition.

**Inputs:**
- `actual_age: int` — chronological age of building in years
- `renovation_portions: list[dict]` — list of {portion_pct: float, age_after_renovation: int} for renovated portions
- `maintenance_degree: str` — "excellent", "average", or "poor" (for table-based method)

**Method A — Weighted Effective Age (renovation-based):**
```python
def effective_age_weighted(actual_age, renovation_portions):
    """
    Example: 20-year-old building, 30% renovated 5 years ago
    unrenovated: 70% at actual_age=20, renovated: 30% at age=5
    effective_age = (0.70 × 20) + (0.30 × 5) = 14 + 1.5 = 15.5
    """
    remaining_pct = 1.0
    effective_age = 0
    for portion in renovation_portions:
        effective_age += portion['portion_pct'] * portion['age_after_renovation']
        remaining_pct -= portion['portion_pct']
    effective_age += remaining_pct * actual_age
    return effective_age
```

**Method B — Table-Based (maintenance degree lookup):**
Most LGU depreciation tables bypass explicit effective age calculation by directly providing percent depreciated or percent good based on:
- Actual age bracket (e.g., 0-2, 2-5, 5-8, ..., 50-55 years)
- Degree of maintenance (Excellent, Average, Poor)

This implicitly adjusts for maintenance condition without computing effective age.

**Legal citation:** DOF LAR 1-92 Section 40 (effective age method); appraiserph.com practitioner guidance

**Deterministic:** Method B (table-based) is fully deterministic. Method A requires renovation data that may involve assessor judgment.

---

### 5. Maintenance-Adjusted Depreciation Lookup (LGU Table Method)

**What it computes:** Percent good (or percent depreciated) from the LGU's building depreciation table, based on age bracket, construction type, and maintenance degree.

**Inputs:**
- `actual_age: int` — building age in years
- `construction_type: str` — Type I through IV
- `maintenance_degree: str` — "excellent", "average", or "poor"
- `lgu_depreciation_table: dict` — LGU-specific depreciation lookup table

**Representative table (Mamburao, Occidental Mindoro — RC/mixed concrete buildings):**

| Age (Years) | Excellent % Dep | Excellent % Good | Average % Dep | Average % Good | Poor % Dep | Poor % Good |
|---|---|---|---|---|---|---|
| 0–2 | 3% | 97% | 3% | 97% | 4% | 96% |
| 2–5 | 5% | 95% | 5% | 95% | 7% | 93% |
| 5–8 | 8% | 92% | 9% | 91% | 11% | 89% |
| 8–12 | 11% | 89% | 14% | 86% | 16% | 84% |
| 12–16 | 15% | 85% | 18% | 82% | 20% | 80% |
| 16–20 | 18% | 82% | 22% | 78% | 24% | 76% |
| 20–25 | 21% | 79% | 25% | 75% | 29% | 71% |
| 25–30 | 25% | 75% | 28% | 72% | 33% | 67% |
| 30–35 | 28% | 72% | 31% | 69% | 37% | 63% |
| 35–40 | 31% | 69% | 34% | 66% | 41% | 59% |
| 40–45 | 34% | 66% | 37% | 63% | 45% | 55% |
| 45–50 | 36% | 64% | 40% | 60% | 49% | 51% |
| 50–55 | 39% | 61% | 43% | 57% | 51% | 49% |

**Formula:**
```python
def depreciation_table_lookup(actual_age, construction_type, maintenance_degree,
                               lgu_table):
    bracket = find_age_bracket(actual_age, lgu_table[construction_type])
    percent_good = bracket[maintenance_degree]['percent_good']
    return percent_good / 100  # as decimal
```

**Key observations:**
- Depreciation is NOT linear — the table shows decelerating depreciation rates (more depreciation in early years, slower later)
- At age 50-55 with excellent maintenance: 39% depreciated (61% good) — building retains substantial value
- At age 50-55 with poor maintenance: 51% depreciated (49% good)
- The table implies buildings never reach 0% good, even at advanced ages — no statutory minimum residual is needed because the tables effectively prevent full depreciation
- This table applies to RC/mixed concrete; separate tables exist for wood, semi-concrete, etc. with faster depreciation

**Note on format variation:** The Excellent/Average/Poor three-column format is **common and widely used** but NOT universal across all LGUs. Some LGUs (e.g., Batangas Province) use a distinctly different format — depreciation by construction sub-type and age without separate maintenance condition columns, with approximately 10 sub-classifications (I-A through IV-A) and age ranges up to 80-85 years:
- Type I-A at 0-2 years: 2% depreciation
- Type I-A at 20-25 years: 20% depreciation
- Type IV-A at 0-2 years: 6% depreciation
The BLGF inspection framework actually contemplates five condition levels (Excellent, Good, Average, Fair, Poor), though operational tables often simplify to three.

**Legal citation:** DOF LAR 1-92 Section 40; individual LGU SFMV ordinances

**External data dependency:** Table is LGU-specific. No national standard table exists.

**Deterministic:** Yes, given the LGU's depreciation table.

---

### 6. Building FMV Computation (RCNLD)

**What it computes:** The Fair Market Value of a building for RPT assessment purposes.

**Inputs:**
- `total_floor_area_sqm: float`
- `construction_type: str`
- `bucc_rate: float` (from LGU SFMV)
- `adjustment_factors: list[float]` (optional)
- `actual_age: int`
- `maintenance_degree: str` ("excellent"/"average"/"poor")
- `lgu_depreciation_table: dict`

**Formula (table-based method — most common in practice):**
```python
def building_fmv_rcnld(floor_area_sqm, bucc_rate, adjustment_factors,
                        actual_age, construction_type, maintenance_degree,
                        lgu_depreciation_table):
    # Step 1: Compute RCN
    rcn = replacement_cost_new(floor_area_sqm, bucc_rate, adjustment_factors)

    # Step 2: Look up percent good from LGU depreciation table
    percent_good = depreciation_table_lookup(
        actual_age, construction_type, maintenance_degree,
        lgu_depreciation_table
    )

    # Step 3: Compute FMV
    building_fmv = rcn * percent_good
    return building_fmv
```

**Formula (age-life method — used when no LGU table available):**
```python
def building_fmv_age_life(floor_area_sqm, bucc_rate, adjustment_factors,
                           effective_age, economic_life):
    rcn = replacement_cost_new(floor_area_sqm, bucc_rate, adjustment_factors)
    depreciation_rate = min(effective_age / economic_life, 1.0)
    building_fmv = rcn * (1 - depreciation_rate)
    return building_fmv
```

**Worked example:**
```
Given: 2-storey RC residential, 240 sqm, BUCC ₱20,000/sqm, age 10 years, average maintenance
  RCN = 240 × ₱20,000 = ₱4,800,000
  Percent good (from table, age 8-12, average) = 86%
  Building FMV = ₱4,800,000 × 0.86 = ₱4,128,000

Alternative (age-life): economic life = 50 years
  Depreciation rate = 10/50 = 20%
  Building FMV = ₱4,800,000 × 0.80 = ₱3,840,000

Note: Table-based yields higher FMV (₱4,128,000 vs ₱3,840,000) because
table accounts for non-linear depreciation patterns.
```

**Legal citation:** DOF LAR 1-92 Sections 38-41; RA 7160 Section 201

**Deterministic:** Yes, given all inputs and LGU-specific data.

---

### 7. Machinery Depreciation (for completeness — per LGC Sections 224-225)

**What it computes:** Depreciated FMV of machinery for RPT assessment. Included here for completeness as machinery is an "improvement" assessed alongside buildings.

**Inputs:**
- `is_brand_new: bool`
- `acquisition_cost: float` (if brand new)
- `replacement_cost: float`
- `estimated_economic_life: int`
- `remaining_economic_life: int`
- `years_of_use: int`

**FMV Formula (Section 224):**
```python
def machinery_fmv(is_brand_new, acquisition_cost, replacement_cost,
                   remaining_economic_life, estimated_economic_life):
    if is_brand_new:
        return acquisition_cost
    else:
        return (remaining_economic_life / estimated_economic_life) * replacement_cost
```

**Depreciation Formula (Section 225):**
```python
def machinery_depreciation(original_cost, years_of_use):
    max_annual_rate = 0.05  # 5% per year maximum
    min_residual_pct = 0.20  # 20% minimum residual

    depreciation = original_cost * max_annual_rate * years_of_use
    depreciated_value = original_cost - depreciation
    floor_value = original_cost * min_residual_pct

    return max(depreciated_value, floor_value)
```

**Key rules:**
- Max 5% annual depreciation of original/replacement/reproduction cost
- Minimum residual value: 20% (while machinery is useful and in operation)
- Imported machinery: acquisition cost includes freight, insurance, duties, taxes, handling, installation
- Foreign currency converted at Central Bank exchange rates

**Legal citation:** RA 7160 Sections 224, 225

**Deterministic:** Yes.

---

## Decision Tree: Full Building Depreciation Pipeline

```
INPUT: building physical data (floor area, construction type, age, maintenance)
       + LGU-specific data (BUCC schedule, depreciation table, adjustment factors)

1. CLASSIFY building construction type (Type I-A through IV)
   → Determines BUCC rate tier and depreciation table to use

2. LOOK UP BUCC rate (₱/sqm) from LGU SFMV by construction type

3. COMPUTE RCN = floor_area × bucc_rate
   → Apply adjustment factors if deviations from standard

4. DETERMINE depreciation using ONE of:
   a. TABLE METHOD (preferred): Look up percent_good from LGU depreciation table
      by (age bracket, construction type, maintenance degree)
   b. AGE-LIFE METHOD (fallback): depreciation_rate = effective_age / economic_life
      → If renovated: compute weighted effective_age first

5. COMPUTE Building FMV = RCN × percent_good (table) OR RCN × (1 - depreciation_rate) (age-life)

6. FEED Building FMV into assessment level lookup (→ assessment-level-lookup.md)
   → building_assessment_level = graduated rate by classification + FMV bracket
   → building_AV = building_FMV × assessment_level

OUTPUT: Building FMV (for assessment), percent_good, RCN
```

---

## Relationship Between Building Depreciation and RPT

```
Building Physical Data → Construction Type → BUCC rate → RCN
                                                          ↓
Building Age + Maintenance → LGU Depreciation Table → % Good
                                                          ↓
                                            Building FMV = RCN × % Good
                                                          ↓
                              Assessment Level Lookup (Section 218(b)) → AV
                                                          ↓
                                            RPT = AV × (basic rate + SEF)
```

This computation is a PREREQUISITE for the assessment-level-lookup computation documented in `analysis/assessment-level-lookup.md`.

---

## External Data Dependencies

| Dependency | Source | Update Frequency | Automation Impact |
|---|---|---|---|
| BUCC schedule (₱/sqm by type) | LGU SFMV ordinance | Every general revision (target 3 years) | Must track per-LGU; no central database |
| Depreciation table (% good by age/type/maintenance) | LGU SFMV ordinance | Every general revision | Must track per-LGU; no national standard |
| Adjustment factors | LGU assessor guidelines | Irregular | LGU-specific; may not be publicly available |
| DPWH construction cost data | DPWH | Annual | Input to LGU BUCC preparation |
| Economic life by construction type | Assessor judgment/LGU guidelines | Stable (rarely changes) | Not nationally standardized |
| Philippine Valuation Standards (PVS) | DOF/BLGF under RA 12001 | New — being developed | Will standardize methodology nationally |

---

## Unresolved Ambiguities

1. **No national standard depreciation table:** Each LGU prepares its own table. Tables from Mamburao, Batangas, and other LGUs show different formats and values. Annex "J" of DOF LAR 1-92 provides a template format but no standard values.

2. **Economic life not statutory:** The LGC does not prescribe economic life for buildings. Assessors determine this locally. Practitioner consensus exists (50-60 years for RC) but is not legally binding.

3. **Effective age vs. actual age ambiguity:** When and how to adjust for renovations is assessor judgment. The weighted method (described in Sub-computation 4) is practitioner guidance, not statutory.

4. **Table method vs. age-life method discrepancy:** As shown in the worked example, the two methods can yield different results (₱4,128,000 vs. ₱3,840,000 for the same building). Which method prevails depends on the LGU.

5. **No minimum residual value for buildings:** Unlike machinery (20% floor per Section 225), buildings have no statutory minimum residual. LGU tables effectively prevent full depreciation, but the floor depends on the specific table values.

6. **BUCC rate transparency:** Many LGUs do not publish BUCC schedules online. Obtaining current rates requires visiting the assessor's office.

7. **RA 12001 transition:** RPVARA mandates national Philippine Valuation Standards (PVS) within 2 years of effectivity (by July 2026). This may standardize depreciation methodology, but implementing rules are not yet published.

8. **Multi-building properties:** How to handle properties with multiple buildings of different types/ages is not explicitly addressed — assessors value each building separately and sum the FMVs.

---

## Key Distinctions

### Building Depreciation vs. Machinery Depreciation

| Aspect | Buildings | Machinery |
|---|---|---|
| Legal basis | DOF LAR 1-92 Sections 40-41 | LGC Sections 224-225 |
| Method | RCNLD with depreciation tables or age-life | Cost × (remaining life / economic life) |
| Annual rate cap | None (table-driven) | 5% per year maximum |
| Minimum residual | None statutory (tables prevent 0%) | 20% of original/replacement cost |
| Depreciation format | Percent good tables by age + maintenance | Straight declining percentage |
| LGU variation | High (different tables) | Low (statutory formula) |

### RPT Building Depreciation vs. Income Tax Depreciation

| Aspect | RPT Assessment | Income Tax (BIR) |
|---|---|---|
| Purpose | Determine FMV for real property tax | Deductible expense against income |
| Method | RCNLD with LGU tables | Straight-line (most common); also SYD, declining balance, units of production |
| Useful life | 50-60 years (RC, assessor practice) | 20-50 years (taxpayer election) |
| Residual value | Table-implied (no statutory) | Taxpayer-determined |
| Land | Never depreciated | Never depreciated |
| Governing law | RA 7160 + DOF LAR 1-92 | NIRC Sections 34(F), RR 12-2012 |

---

## Verification Summary

Verified against 17+ independent sources including DOF LAR 1-92 (SC E-Library), LawPhil RA 7160 full text, PD 1096 (DPWH + Official Gazette), COA Circular 2003-007, BLGF Manual on RP Assessment, BLGF Estimated Useful Life of PPE, Mamburao BUCC schedule, Batangas Province 2010 RPT Code, RA 12001 full text (LawPhil), SRMO Law analysis, PwC Philippines analysis, Muntinlupa City BUCC schedule, CBAA Case No. L-11, Respicio & Co. commentary.

| # | Claim | Verdict | Key Finding |
|---|---|---|---|
| 1 | Economic life figures are assessor practice, not statutory | **CONFIRMED** | No statutory prescription in LGC or DOF LAR 1-92; 50-year RC figure consistent across practitioner sources |
| 2 | COA useful life figures (RC=30, Steel=25-30, etc.) | **CONFIRMED** | Base values confirmed at RC=30, Steel=25, Mixed=20, Wood=15; ranges in analysis slightly broader than single-point COA values |
| 3 | Three maintenance degrees as universal format | **CORRECTED** | Common and widely used (Mamburao confirmed) but NOT universal; Batangas uses different format without maintenance columns; BLGF framework has 5 levels |
| 4 | No statutory minimum residual for buildings | **CONFIRMED** | Section 225's 20% floor is machinery-only; no equivalent for buildings anywhere in LGC or DOF LAR 1-92 |
| 5 | Mamburao depreciation table values | **CONFIRMED** | Values match source document exactly (ages 0-2: 3/3/4%; ages 50-55: 39/43/51%) |
| 6 | Batangas Type I-A through IV-A classification | **CONFIRMED with corrections** | System confirmed with age ranges to 80-85 years; but has ~10 sub-types (not 8); assessor numbering INVERTED from PD 1096 |
| 7 | Adjustment factors methodology | **CONFIRMED** | Directly supported by DOF LAR 1-92 Section 39; Muntinlupa BUCC shows examples (carport 60%, mezzanine 40%) |
| 8 | DOF LAR 1-92 Sections 40-41 govern buildings, not LGC 224-225 | **CONFIRMED** | LGC 224-225 are explicitly titled "Appraisal and Assessment of Machinery" / "Depreciation Allowance for Machinery" |
| 9 | Building construction types per PD 1096 (4 types, sub-types A-D) | **CORRECTED** | PD 1096 has FIVE types (I-V), not four; sub-types are assessor convention, NOT from PD 1096; assessor numbering is INVERTED from PD 1096 |
| 10 | BUCC rate ranges | **UNVERIFIED** | Plausible given PSA construction cost data, but BUCC schedules are LGU-specific and mostly not publicly available online |
| 11 | Machinery depreciation per Section 225 (5% annual, 20% residual) | **CONFIRMED** | Verbatim from statutory text of LGC Section 225 |
| 12 | RA 12001 mandates PVS-aligned depreciation methodology | **CORRECTED** | Law requires depreciation consideration (Section 14) and SMV updates within 2 years per PVS, but is principle-based — does not mandate specific depreciation methodology |

### Critical Discovery: Assessor vs. PD 1096 Numbering Inversion

The most significant finding is a **systematic numbering inversion** between two classification systems:
- **PD 1096:** Type I = Wood (lowest) → Type V = Fire-resistive (highest)
- **Assessor practice:** Type I = RC/steel (highest) → Type IV = Temporary (lowest)

This inversion is widespread in Philippine assessor practice. The original analysis conflated these systems; corrections applied above in Sub-computation 1.

### Corrections Applied to Primary Extraction
1. **Sub-computation 1 (Construction Type Classification):** Rewritten to clearly distinguish PD 1096 (5 types) from assessor convention (4 types, inverted numbering, with sub-types)
2. **Sub-computation 3 (Maintenance degrees):** Note added that three-column format is common but not universal
3. **Batangas reference:** Sub-classification count corrected from 8 to ~10
4. **RA 12001 legal basis:** Corrected to reflect principle-based mandate, not prescriptive methodology
