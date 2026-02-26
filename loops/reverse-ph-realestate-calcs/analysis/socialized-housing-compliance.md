# Socialized Housing Compliance — Computation Extraction

**Wave:** 2 (Computation Extraction)
**Aspect:** socialized-housing-compliance
**Date:** 2026-02-26
**Primary sources:** input/dhsud-price-ceilings.md, analysis/bp220-standards.md
**Verification:** 5 sub-computations verified against 20+ independent sources (PNA, Inquirer, GMA News, Manila Bulletin, PhilStar, SunStar, CREBA, BOI, Supreme Court E-Library, DHSUD official, Orange Magazine, YourHome.ph, Property Report, Jur.ph, Digest.ph, Manila Times)

---

## Overview

DHSUD socialized housing compliance checking determines whether a proposed housing unit meets the regulatory requirements to be classified and sold as socialized housing. This is a prerequisite for:
- Issuance of License to Sell (LTS) by DHSUD
- Access to government housing guarantee programs (PhilGuarantee)
- Pag-IBIG affordable housing program loan eligibility
- Developer balanced housing compliance credit

The computation is **fully deterministic** given the unit's physical parameters and selling price.

---

## Sub-Computation 1: Housing Category Classification

### What It Computes
**Inputs:** selling_price (₱)
**Outputs:** housing_category (enum: L1A, L1B, L2_Economic, L3_LowCost, MediumCost, OpenMarket)

### Decision Tree
```
IF selling_price ≤ 300,000         → Level 1-A (Socialized)
ELIF selling_price ≤ 500,000       → Level 1-B (Socialized upper)
ELIF selling_price ≤ 1,250,000     → Level 2 (Economic)
ELIF selling_price ≤ 3,000,000     → Level 3 (Low-Cost)
ELIF selling_price ≤ 4,000,000     → Medium-Cost
ELSE                               → Open Market
```

### Legal Basis
- DHSUD-DEPDev JMC 2024-001

### Edge Cases
- The labels "Economic" (L2) and "Low-Cost" (L3) are practitioner conventions, not universally standardized in the JMC text. The JMC uses level numbers (1-A, 1-B, 2, 3) as primary identifiers.
- Classification is based solely on selling price — floor area and location are NOT classification factors (they affect the *ceiling* within a classification, not the classification itself).
- Levels 1-A through 2 are collectively called "socialized" in some contexts; Level 3 is sometimes grouped with "socialized" in broader references.

### Verification Status: PARTIALLY CONFIRMED
Price brackets exact across 5+ sources. Label assignment for L2/L3 is plausible but not universally standardized in official JMC text.

### Deterministic: YES

---

## Sub-Computation 2: Selling Price Ceiling Check (JMC 2025-001)

### What It Computes
**Inputs:** selling_price (₱), floor_area (sqm), building_type (horizontal | vertical), building_floors (int), location_type (NCR_HUC | other), zonal_value_per_sqm (₱, if NCR/HUC condo)
**Outputs:** compliant (bool), applicable_ceiling (₱), shortfall_or_headroom (₱)

### Formula / Decision Tree
```
# Step 1: Determine base ceiling
IF building_type == "horizontal":
    IF 24 ≤ floor_area ≤ 26:
        base_ceiling = 844,440
    ELIF floor_area ≥ 27:
        base_ceiling = 950,000
    ELSE:
        FAIL — below minimum floor area (24 sqm)

ELIF building_type == "vertical":
    IF building_floors ≤ 5:  # 3-5 floors
        IF 24 ≤ floor_area ≤ 26:
            base_ceiling = 1,280,000
        ELIF floor_area ≥ 27:
            base_ceiling = 1,500,000
        ELSE:
            FAIL — below minimum floor area (24 sqm)
    ELSE:  # 6+ floors
        IF 24 ≤ floor_area ≤ 26:
            base_ceiling = 1,600,000
        ELIF floor_area ≥ 27:
            base_ceiling = 1,800,000
        ELSE:
            FAIL — below minimum floor area (24 sqm)

# Step 2: Apply zonal value add-on (vertical/NCR-HUC only)
add_on = 0
IF building_type == "vertical" AND location_type == "NCR_HUC":
    IF 20,000 ≤ zonal_value_per_sqm ≤ 24,999:
        add_on = 50,000
    ELIF 25,000 ≤ zonal_value_per_sqm ≤ 29,999:
        add_on = 100,000
    ELIF 30,000 ≤ zonal_value_per_sqm ≤ 39,999:
        add_on = 150,000
    ELIF zonal_value_per_sqm ≥ 40,000:
        add_on = 200,000

# Step 3: Compliance check
applicable_ceiling = base_ceiling + add_on
compliant = (selling_price ≤ applicable_ceiling)
headroom = applicable_ceiling - selling_price
```

### Base Ceiling Lookup Table

| Building Type | Floors | Floor Area | Max Selling Price |
|---|---|---|---|
| Horizontal | — | 24–26 sqm | ₱844,440 |
| Horizontal | — | 27+ sqm | ₱950,000 |
| Vertical | 3–5 | 24–26 sqm | ₱1,280,000 |
| Vertical | 3–5 | 27+ sqm | ₱1,500,000 |
| Vertical | 6+ | 24–26 sqm | ₱1,600,000 |
| Vertical | 6+ | 27+ sqm | ₱1,800,000 |

### Zonal Value Add-On Table (Vertical/NCR-HUC Only)

| Zonal Value per sqm | Add-On |
|---|---|
| ₱20,000–₱24,999 | +₱50,000 |
| ₱25,000–₱29,999 | +₱100,000 |
| ₱30,000–₱39,999 | +₱150,000 |
| ₱40,000+ | +₱200,000 |

### Lot-Only Ceiling (Sub-Rule)
For lot-only sales (no house component): max selling price = 40% of the applicable house-and-lot ceiling.
```
lot_only_ceiling = applicable_ceiling × 0.40
```
*Discovered in verification; confirmed by Property Report and SunStar sources.*

### Key Rules
- **Minimum floor area:** 24 sqm (raised from 22 sqm by JMC 2025-001). Total floor area covers all levels/rooms, **excluding lofts and mezzanines**.
- **Selling price is inclusive of:** land acquisition + land development + construction costs.
- **VAT:** Socialized housing is VAT-exempt (Section 109(P) NIRC as amended; RA 7279). The ceiling need not account for VAT.
- **Validity:** JMC 2025-001 effective December 23, 2025; valid for 3 years.
- **Zonal value add-on** is new in JMC 2025-001 (did not exist in JMC 2023-003).
- **Building height tier simplification:** JMC 2023-003 used 4-story / 5-9 story / 10+ story. JMC 2025-001 simplified to 3-5 floors / 6+ floors.

### Previous Ceilings (JMC 2023-003, for Reference)
- Horizontal: ₱850,000 (28+ sqm with loft or 32+ sqm total)
- Condo 4-story: ₱933,320 (22 sqm) to ₱1,145,438 (27 sqm)
- Condo 5-9 story: ₱1,000,000 (22 sqm) to ₱1,227,273 (27 sqm)
- Condo 10+ story: ₱1,320,000 (22 sqm) to ₱1,620,000 (27 sqm)
- Max with land dev cost: ₱1,800,000

### Legal Basis
- DHSUD-DEPDev JMC 2025-001 (signed Dec 1, 2025; IRR effective Dec 23, 2025)
- DHSUD-NEDA JMC 2023-003 (superseded, October 2023)
- RA 11201 (DHSUD Act) — authority to set ceilings
- RA 7279 (UDHA) — defines socialized housing

### Verification Status: CONFIRMED
All 6 base ceiling amounts, minimum floor area change, zonal add-on table, lot-only 40% rule, and VAT exemption verified across PNA, Inquirer, GMA News, Manila Bulletin, PhilStar, SunStar, DHSUD official, and Property Report.

### Deterministic: YES

---

## Sub-Computation 3: Government Housing Guarantee Eligibility

### What It Computes
**Inputs:** housing_category (from Sub-Computation 1), total_loan_package_value (₱)
**Outputs:** guarantee_eligible (bool), applicable_guarantee_ceiling (₱)

### Decision Tree
```
IF housing_category IN [L1A, L1B, L2_Economic, L3_LowCost]:
    guarantee_ceiling = 4,900,000
    guarantee_eligible = (total_loan_package_value ≤ 4,900,000)
ELIF housing_category == MediumCost:
    guarantee_ceiling = 6,600,000
    guarantee_eligible = (total_loan_package_value ≤ 6,600,000)
ELSE:
    guarantee_eligible = FALSE  # Open market — no government guaranty
```

### Key Rules
- **Guarantee ceiling ≠ selling price ceiling.** The guarantee ceiling is the max loan/housing package value that PhilGuarantee (formerly HGC, merged into PhilGuarantee in 2019 under RA 11439) will guarantee. It is set higher than the selling price ceiling to cover total financing costs (interest, insurance, etc.).
- **Previous ceilings:** Low-cost ₱2,500,000 → ₱4,900,000 (+96%); Medium-cost ₱4,000,000 → ₱6,600,000 (+65%).
- **Set jointly by:** DHSUD and DEPDev (formerly NEDA), implemented by PhilGuarantee.
- **"Total loan package"** includes the loan principal plus insurance premiums, processing fees, and other financing costs bundled into the guaranty.

### Legal Basis
- DHSUD-DEPDev JMC 2024-001
- RA 11439 (PhilGuarantee Charter, 2019) — merged HGC into PhilGuarantee
- RA 11201 (DHSUD Act) — joint determination authority

### Verification Status: CONFIRMED
Both ceiling amounts verified across PhilStar, Orange Magazine, SunStar, YourHome.ph. Entity correction: HGC → PhilGuarantee confirmed.

### Deterministic: YES

---

## Sub-Computation 4: Balanced Housing Development Requirement

### What It Computes
**Inputs:** project_type (subdivision | condominium | boi_registered), total_project_area (sqm), total_project_cost (₱), total_floor_area (sqm, if vertical + BOI), compliance_mode (area_basis | cost_basis)
**Outputs:** required_socialized_amount (sqm or ₱), compliance_met (bool)

### Formula
```
IF project_type == "subdivision":
    IF compliance_mode == "area_basis":
        required = total_project_area × 0.15
    ELSE:  # cost_basis
        required = total_project_cost × 0.15

ELIF project_type == "condominium":
    IF compliance_mode == "area_basis":
        required = total_project_area × 0.05
    ELSE:  # cost_basis
        required = total_project_cost × 0.05

ELIF project_type == "boi_registered":
    # Separate SHR (Socialized Housing Requirement) — BOI incentive condition
    IF building_type == "horizontal":
        required = total_project_area × 0.20  # or total_project_cost × 0.20
    ELSE:  # vertical
        required = total_floor_area_saleable × 0.20

# Developer chooses basis (area or cost)
compliance_met = (actual_socialized_delivered ≥ required)
```

### Compliance Modes (6 Total)
Four statutory modes per RA 10884 Section 18:
1. **On-site development** — build socialized housing within the same project or city/municipality
2. **New settlement development** — develop a new socialized housing settlement
3. **Joint venture** — with LGU, housing agencies, other developers, or accredited NGOs
4. **Community Mortgage Program (CMP)** — participate in a CMP project

Two additional IRR-introduced modes (HLURB AO No. 02, S. 2018):
5. **Percentage of Investment Compliance (PIC)** — contribute 25% of required compliance cost
6. **Incentivized Compliance (IC)** — contribute ≥20% of required compliance cost to BALAI Program or LGU projects

*Note: CREBA has argued PIC/IC lack explicit statutory basis under RA 10884. Proposed legislation (HB 5754, HB 10772) for direct cash-in-lieu mode is not yet enacted as of Feb 2026.*

### Key Rules
- **Developer chooses** whether to compute on area basis or cost basis.
- **Original RA 7279 requirement was 20%**, reduced to 15% (subdivision) / 5% (condo) by RA 10884.
- **BOI 20% is a separate requirement** — the Socialized Housing Requirement (SHR) is a condition for availing BOI income tax holiday and incentives. It is distinct from the balanced housing requirement per se.
- **"Project cost" definition** is not precisely defined in statute. In practice (per BOI/HLURB), it is the total development cost as declared in the developer's project documentation submitted to DHSUD.

### Legal Basis
- RA 7279 (UDHA) Section 18 — original balanced housing requirement
- RA 10884 — amended RA 7279; reduced percentage, added condo requirement
- HLURB AO No. 02, Series of 2018 — IRR introducing PIC and IC compliance modes
- BOI registration requirements — separate 20% SHR

### Verification Status: PARTIALLY CONFIRMED
15%/5% split verified across Supreme Court E-Library, CREBA, Jur.ph, Digest.ph. BOI 20% verified via BOI FAQs. Correction: BOI 20% is a separate SHR condition for incentive eligibility, not the same as the RA 10884 balanced housing requirement.

### Deterministic: YES (given compliance mode selection and project cost declaration)

---

## Sub-Computation 5: Socialized Housing Selling Price Ceiling Update Tracking

### What It Computes
**Inputs:** current_date, jmc_effectivity_date, jmc_validity_years
**Outputs:** ceiling_current (bool), expected_review_date

### Formula
```
ceiling_expiry = jmc_effectivity_date + jmc_validity_years
ceiling_current = (current_date < ceiling_expiry)
# Ceilings may be reviewed "not more than once every two years" per RA 11201
expected_review_window_start = jmc_effectivity_date + 2 years
```

### Key Rules
- JMC 2025-001: effective Dec 23, 2025; valid for 3 years → expires ~Dec 23, 2028.
- Ceilings may be reviewed at any time, but not more than once every 2 years (RA 11201).
- Each new JMC supersedes the previous one entirely.

### Legal Basis
- RA 11201 Section 6(b) — review frequency constraint

### Verification Status: CONFIRMED (statutory text)

### Deterministic: YES

---

## Cross-Computation Integration

### How These Sub-Computations Chain Together

```
                    ┌──────────────────┐
                    │  Unit Parameters │
                    │ (price, area,    │
                    │  type, location) │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ SC1: Classify    │──→ housing_category
                    │ by Selling Price │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───────┐ ┌───▼──────────┐ ┌▼────────────────┐
     │ SC2: Price     │ │ SC3: Govt    │ │ SC4: Balanced   │
     │ Ceiling Check  │ │ Guarantee    │ │ Housing Check   │
     │ (JMC 2025-001)│ │ Eligibility  │ │ (Developer)     │
     └────────┬───────┘ └───┬──────────┘ └┬────────────────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼─────────┐
                    │ SC5: Ceiling     │──→ is_ceiling_current?
                    │ Currency Check   │
                    └──────────────────┘
```

### Cross-Reference to Related Computations
- **bp220-lot-compliance** (Wave 2, pending): Physical standards compliance (lot area, floor area, setbacks) — complementary to this price-based compliance check. A unit must pass BOTH price ceiling AND physical standards to qualify as socialized housing.
- **pagibig-loan-eligibility** (Wave 2, done): Pag-IBIG affordable housing program (AHP) loan ceilings are pegged to DHSUD socialized housing price ceilings. AHP eligible amounts updated to JMC 2025-001 values.
- **ph-tax-computations-reverse loop**: Socialized housing has specific tax implications — VAT exempt (NIRC 109(P)), may qualify for CGT/DST exemptions under RA 7279 for certain beneficiaries.
- **assessment-level-lookup** (Wave 2, pending): Property assessed value classification (residential, commercial, etc.) is a separate system from the DHSUD housing category classification.

---

## Complexity Assessment

| Dimension | Score | Notes |
|---|---|---|
| Branching rules | ~12 | 6 price brackets + 6 ceiling tiers (2 building types × 2 height ranges × 2 floor area ranges) + 4 zonal add-on bands |
| Lookup tables | 3 | Base ceiling table, zonal add-on table, classification table |
| External data dependencies | 2 | BIR zonal values (for add-on), JMC validity/update cycle |
| Update frequency | Medium | JMCs updated every 2-3 years; zonal values updated periodically by BIR |
| Total rule count | ~25 | Including balanced housing modes, lot-only sub-rule, guarantee eligibility |

---

## Unresolved Ambiguities

1. **Floor area measurement standard:** JMC 2025-001 says "total floor area" excluding lofts and mezzanines. But the precise measurement methodology (gross vs. net, inclusion/exclusion of walls) is not defined in the JMC itself — likely defers to National Building Code or DHSUD guidelines.
2. **Zonal value below ₱20,000:** The add-on table starts at ₱20,000/sqm. For NCR/HUC condos on land zoned below ₱20,000/sqm, no add-on applies (implied but not explicit).
3. **Mixed-use building classification:** If a building contains both socialized and open-market units, the ceiling check applies per-unit. But the building height tier (3-5 vs 6+) applies to the entire structure — a socialized unit on the 2nd floor of a 10-story mixed building uses the 6+ floor ceiling.
4. **"Project cost" for balanced housing cost basis:** No statutory definition. Declared by developer, subject to DHSUD review. Potential for dispute.
5. **PIC/IC compliance modes** lack clear statutory basis per CREBA's position — legal risk for developers relying solely on these modes.

---

## Legal Citations Summary

| Citation | Relevance |
|---|---|
| DHSUD-DEPDev JMC 2025-001 | Socialized housing selling price ceilings (current) |
| DHSUD-NEDA JMC 2024-001 | Housing category classification brackets; guarantee ceilings |
| DHSUD-NEDA JMC 2023-003 | Previous socialized ceilings (superseded) |
| RA 11201 (DHSUD Act, 2019) | Authority to set/review ceilings; review frequency |
| RA 7279 (UDHA, 1992) | Defines socialized housing; balanced housing requirement |
| RA 10884 (2016) | Amended RA 7279; 15%/5% balanced housing |
| RA 11439 (PhilGuarantee Charter, 2019) | Merged HGC into PhilGuarantee |
| HLURB AO No. 02, S. 2018 | IRR for balanced housing (PIC/IC modes) |
| NIRC Section 109(P) | VAT exemption for socialized housing |
