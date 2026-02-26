# Condominium Common Area / Undivided Interest Computation

**Wave:** 2 — Computation Extraction
**Date:** 2026-02-26
**Aspect:** condo-common-area-pct
**Primary source:** `analysis/condo-act-common-areas.md` (Wave 1)
**Verification:** 16 independent sources; 1 critical correction, 3 high-severity, 6 medium, 6 low

---

## Computation 1: Undivided Interest % — Default Statutory Rule

**What it computes:** Each unit owner's percentage interest in common areas when the master deed is silent.

**Legal basis:** RA 4726 Section 6(c); Civil Code Article 485 (co-ownership presumption)

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `total_units` | integer | Master deed / condominium plan (count of all CCTs including parking if separately titled) |

**Formula:**
```
unit_interest_pct = 1 / total_units × 100
```

**Rules:**
- Applies ONLY when master deed does not specify a different allocation method
- "Per unit of ownership" — not per owner (an owner with 3 units gets 3 shares)
- Sum of all interests = 100%
- Civil Code Art. 485 independently supports equal-shares presumption for co-ownership
- Parking slots with separate CCTs: each parking CCT counts as a separate "unit" under this default
- This default is almost never used in modern practice — virtually all master deeds specify floor-area-proportional

**Edge cases:**
- Developer's unsold units: developer holds interest % for all unsold units
- Unit merger: requires master deed amendment + DHSUD approval + CCT reissuance; merged unit gets combined share

**Deterministic:** Yes — trivially so given unit count.

**Verification status:** CONFIRMED — all 16 sources agree. Civil Code basis independently confirmed.

---

## Computation 2: Undivided Interest % — Floor-Area Proportional (Industry Standard)

**What it computes:** Each unit owner's percentage interest in common areas based on floor area ratio. This is the dominant method used by Philippine condominium projects.

**Legal basis:** RA 4726 Section 4 ("exact nature of interest" stated in master deed) — not a statutory formula but the universal industry practice. Must be expressly stated in master deed to override Section 6(c) default.

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `unit_floor_area` | float (sqm) | Condominium Certificate of Title (CCT) |
| `total_sellable_floor_area` | float (sqm) | Master deed — sum of all individually-titled unit floor areas |

**Formula:**
```
unit_interest_pct = unit_floor_area / total_sellable_floor_area × 100
```

**Rules:**
- Denominator includes ALL separately-titled areas: residential units + commercial units + separately-titled parking CCTs
- Denominator EXCLUDES common areas (corridors, lobbies, amenities, elevators, stairs) — these are the subject of the interest, not part of the divisor
- Sum of all unit interests must = 100%
- This percentage appears on each unit's CCT

**CORRECTION (high severity):** Denominator must include separately-titled parking slot CCTs. In Metro Manila, parking is commonly issued as separate CCTs, which materially affects the denominator and thus every residential unit's interest %.

**Example:**
| Unit | Floor Area | Total Sellable (incl. parking) | Undivided Interest |
|------|-----------|-------------------------------|-------------------|
| Residential A | 50 sqm | 1,200 sqm | 4.17% |
| Residential B | 75 sqm | 1,200 sqm | 6.25% |
| Parking P1 | 12 sqm | 1,200 sqm | 1.00% |

Without parking CCTs in denominator (1,000 sqm): Residential A would be 5.00% — a significant difference.

**Alternative method — Par Value / Assigned Value (third recognized method):**
```
unit_interest_pct = assigned_value_of_unit / sum_of_all_assigned_values × 100
```
Permitted under the "unless otherwise provided" clause. Used where units vary greatly in value (e.g., penthouse vs studio with similar sqm). Less common but legally valid. Some mixed-use master deeds use this or a hybrid approach.

**Edge cases:**
- Limited common areas (balconies, assigned parking without separate CCT): ownership is common but use is exclusive; may or may not carry separate interest allocation depending on master deed
- Storage units: if separately titled, included in denominator; if part of a unit, already in unit floor area
- Unit subdivision: splits the original interest proportionally; requires master deed amendment
- Rounding: no regulation specifies rounding convention when interest percentages don't divide evenly; practice varies (2–4 decimal places)

**Deterministic:** Yes — given unit floor area and total sellable floor area from master deed/CCTs.

**Verification status:** CONFIRMED with corrections (parking CCT denominator impact, par value alternative method identified).

---

## Computation 3: Common Area RPT Share

**What it computes:** Each unit owner's share of real property tax assessed on the condominium's common areas.

**Legal basis:** RA 4726 Section 6(c) + Local Government Code (RA 7160) Sections 233, 235, 236

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `undivided_interest_pct` | float (%) | From Computation 1 or 2 per master deed |
| `assessed_value_common_areas` | float (₱) | LGU assessor's office |
| `basic_rpt_rate` | float | 1% (provinces) or 2% (cities/Metro Manila) per LGC |
| `sef_rate` | float | 1% (universal — Special Education Fund) |

**Formula:**
```
Step 1: total_rpt = assessed_value_common_areas × (basic_rpt_rate + sef_rate)
Step 2: unit_rpt_share = undivided_interest_pct / 100 × total_rpt
```

**Rules:**
- RPT liability is **ownership-based regardless of actual usage** — a ground-floor unit owner pays RPT for rooftop common areas they never use
- LGU rate varies: basic rate is 1% (provinces) or 2% (cities/Metro Manila), plus 1% SEF universally
- Metro Manila municipalities may levy additional ad valorem tax
- Condominium corporation may pay RPT collectively and apportion to unit owners via dues
- Penalty for late RPT payment: 2%/month up to 72% maximum (LGC Sec. 255)
- Some LGU assessors embed common area RPT into each unit's individual tax declaration (proportionally allocated); others bill common areas separately

**Edge cases:**
- Developer retains RPT obligation on unsold units
- Exempt common areas (if project has government/charitable component) — rare

**Deterministic:** Yes — given interest %, assessed value, and LGU rate schedule.

**Verification status:** CONFIRMED with refinements on two-step RPT rate structure and assessor practice variation.

---

## Computation 4: Common Expense Assessment Share

**What it computes:** Each unit owner's share of common expenses — the statutory basis for association dues computation.

**Legal basis:** RA 4726 Section 9(d); Civil Code Articles 485 and 490 (supplementary basis)

**Inputs (statutory formula):**
| Input | Type | Source |
|-------|------|--------|
| `undivided_interest_pct` | float (%) | From Computation 1 or 2 |
| `total_common_expenses` | float (₱) | Condominium corporation's approved annual budget |

**Inputs (HLURB operational formula — equivalent):**
| Input | Type | Source |
|-------|------|--------|
| `unit_floor_area` | float (sqm) | CCT |
| `total_annual_gross_expense` | float (₱) | Condo corporation approved budget |
| `total_gross_saleable_area` | float (sqm) | Master deed |
| `vat_applicable` | boolean | True if condo corporation's annual receipts > ₱3M |

**Formula (statutory):**
```
unit_expense_share = undivided_interest_pct / 100 × total_common_expenses
```

**Formula (HLURB operational — industry standard, equivalent when using floor-area-proportional interest):**
```
Step 1: annual_rate_per_sqm = total_annual_gross_expense / total_gross_saleable_area
Step 2: monthly_rate_per_sqm = annual_rate_per_sqm / 12
Step 3: monthly_dues = unit_floor_area × monthly_rate_per_sqm
Step 4: monthly_dues_with_vat = monthly_dues × 1.12  (if vat_applicable)
```

These two formulas produce identical results when the master deed uses floor-area-proportional allocation. The per-sqm method is the operational standard used by property managers. Typical rates (Metro Manila, 2025):
- Economy/socialized: ₱50–₱80/sqm/month
- Mid-market: ₱80–₱150/sqm/month
- High-end/luxury: ₱150–₱250+/sqm/month

**Rules:**
- "Unless otherwise provided" — master deed may specify a different allocation (e.g., weighted by unit type)
- **Lien enforcement (Section 20):** Unpaid assessments constitute a lien on the unit upon registration with the Register of Deeds. This lien is:
  - Superior to all subsequently registered liens (including mortgages)
  - Subordinate only to real property tax liens
  - Enforceable through judicial or extrajudicial foreclosure
  - Confirmed in *Concorde Condominium v. PNB* (G.R. No. 228354)
- **VAT:** 12% on association dues if condominium corporation's annual receipts exceed ₱3M VAT threshold (RMC 65-2012)
- **Sinking fund:** Typically a separate line item (₱4–₱15/sqm/month), authorized under Section 9 but computed separately from regular dues
- **Delinquency interest:** Max 12% per annum if authorized by by-laws

**Edge cases:**
- Developer control period: developer pays dues on unsold units but controls the board until majority of units are sold
- Shortfall buffer: +10% for members, +20% for beneficial users (non-member occupants) per some DHSUD guidelines
- Commercial vs residential units in mixed-use: may have different rates per master deed
- Special assessments for capital improvements: same proportional basis unless otherwise voted

**Deterministic:** Yes — given interest %, total expenses, and VAT status.

**Verification status:** CONFIRMED with significant expansion (HLURB operational formula, Section 20 lien, VAT, sinking fund, Civil Code supplementary basis).

---

## Computation 5: Voting Power Computation (RA 7899)

**What it computes:** The weight of each unit owner's vote for specific governance decisions under RA 7899.

**Legal basis:** RA 7899 (amending RA 4726 Sections 4 and 16)

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `project_type` | enum: "residential_only" / "commercial_only" / "mixed_use" | Master deed |
| `units_owned` | integer | CCT count (for residential/commercial-only projects) |
| `unit_floor_area` | float (sqm) | CCT (for mixed-use projects) |
| `total_floor_area` | float (sqm) | Master deed (for mixed-use projects) |

**Formula:**
```
IF project_type IN ("residential_only", "commercial_only"):
    vote_weight = units_owned  (per unit of ownership)
    simple_majority = > 50% of total units
ELSE IF project_type == "mixed_use":
    vote_weight = total_floor_area_owned
    simple_majority = > 50% of total floor area
```

**CRITICAL CORRECTION:** RA 7899's voting rules apply **only** to:
- **Master deed amendments** (Section 4) — requires simple majority consent
- **Disposition/destruction of common areas** (Section 16) — requires simple majority consent

For ALL OTHER governance votes (board elections, budget approval, rule changes), voting follows:
1. The condominium corporation's **by-laws** and **declaration of restrictions**
2. The **Revised Corporation Code** (for condominium corporations organized as stock or non-stock corporations)

Multiple practitioner sources incorrectly imply RA 7899 voting rules apply universally. The statute itself is narrow in scope.

**Rules:**
- "Per unit of ownership" means per CCT — an owner of 3 units gets 3 votes, not 1
- Developer retains voting rights for ALL unsold units (confirmed in *Respicio & Co.* commentary; developer controls governance until majority sold)
- By-laws may suspend voting rights for owners delinquent in association dues (common and enforceable provision)
- No statutory limit on developer control period in RA 4726

**Deterministic:** Yes — given project type, units owned, and floor areas.

**Verification status:** PARTIALLY CONFIRMED — scope corrected from "all governance" to "Sections 4 and 16 only." "Per unit of ownership" clarified.

---

## Computation 6: Dissolution/Partition Proceeds Distribution

**What it computes:** Each unit owner's share of proceeds when the condominium project is dissolved or partitioned.

**Legal basis:** RA 4726 Section 8

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `undivided_interest_pct` | float (%) | From Computation 1 or 2 |
| `total_net_proceeds` | float (₱) | From sale/partition of common areas |

**Formula:**
```
unit_proceeds = undivided_interest_pct / 100 × total_net_proceeds
```

**Rules:**
- Dissolution requires partition of common areas per Section 8
- Individual unit titles remain with owners
- Common area proceeds distributed by undivided interest %
- Partition may be triggered by destruction (if >50% value destroyed and not rebuilt within reasonable time)

**Deterministic:** Yes

**Verification status:** CONFIRMED — straightforward application of ownership shares.

---

## Additional Sub-Computation: Parking Slot Interest Treatment

**What it computes:** Whether and how parking slots affect undivided interest calculations.

**Legal basis:** RA 4726 (parking CCTs as condominium units); master deed

**Decision tree:**
```
IF parking_slot has separate CCT:
    → It IS a condominium unit under RA 4726
    → Carries its own undivided interest %
    → Floor area included in denominator (Computation 2)
    → Count included in unit count (Computation 1)
    → Owner pays association dues on parking CCT separately
    → Counts toward 40% foreign ownership cap (RA 7899)
ELSE IF parking is part of common areas:
    → No separate interest
    → All unit owners share parking area proportionally
    → Governed by house rules / declaration of restrictions
ELSE IF parking is limited common area (assigned but not titled):
    → Use rights transfer only with principal unit
    → No separate interest computation
    → Maintenance may be separately allocated per declaration of restrictions
```

**Significance:** This is the single most important input variable for any Philippine condominium interest computation tool. Getting the denominator wrong (by excluding or including parking CCTs) changes every unit owner's interest percentage.

**Deterministic:** Yes — the master deed and title structure determine the treatment.

**Verification status:** CONFIRMED across multiple sources (Respicio & Co., U-Property PH).

---

## Summary Table

| # | Computation | Inputs | Deterministic | Verification | Legal Basis |
|---|------------|--------|---------------|-------------|-------------|
| 1 | Default interest % (equal shares) | total_units | Yes | Confirmed | RA 4726 §6(c), CC Art. 485 |
| 2 | Floor-area interest % (industry std) | unit_sqm, total_sellable_sqm | Yes | Confirmed w/ corrections | RA 4726 §4 (master deed) |
| 3 | Common area RPT share | interest_%, assessed_value, RPT_rate | Yes | Confirmed | RA 4726 + LGC §233 |
| 4 | Common expense assessment | interest_%, total_expenses | Yes | Confirmed w/ expansion | RA 4726 §9(d), RMC 65-2012 |
| 5 | RA 7899 voting power | project_type, units, sqm | Yes | Corrected (scope limited) | RA 7899 §§4, 16 only |
| 6 | Dissolution proceeds share | interest_%, total_proceeds | Yes | Confirmed | RA 4726 §8 |
| — | Parking slot treatment | CCT structure, master deed | Yes | Confirmed | RA 4726 + master deed |

All 6 computations + parking treatment are **fully deterministic** given master deed parameters and CCT data.

---

## Corrections Applied (from verification against 16 sources)

### Critical (1)
1. **RA 7899 voting scope overstated** — applies only to master deed amendments (§4) and common area disposition (§16), NOT all governance votes.

### High Severity (3)
1. **Parking CCT denominator impact** — separately-titled parking CCTs must be included in total sellable floor area denominator, materially changing all residential unit interest percentages.
2. **Missing par value allocation method** — a third method (proportional to unit assigned/par value) exists and is permitted.
3. **"Per unit of ownership" not "per owner"** — multi-unit owners get proportionally more votes/shares.

### Medium Severity (6)
1. **HLURB operational formula** — per-sqm rate base is the practical equivalent of statutory proportional formula.
2. **Section 20 lien supremacy** — unpaid assessments create super-priority lien (above mortgages), enforceable by foreclosure.
3. **VAT on association dues** — 12% applies if condo corporation exceeds ₱3M annual receipts (RMC 65-2012).
4. **Developer control period** — developer pays dues on unsold units but retains board control until majority sold.
5. **Civil Code Art. 485/490** — independent statutory basis for equal-shares presumption and building expense sharing.
6. **Developer unsold unit obligations** — must pay pro-rata share of all expenses and RPT.

### Low Severity (6)
1. Two-step RPT rate structure (basic + SEF)
2. Ownership-based (not usage-based) RPT liability
3. LGU assessor practice variation (embedded vs separate billing)
4. Sinking fund as separate line item
5. By-law suspension of delinquent owner voting
6. Unit merger/subdivision recalculation rules

---

## Unresolved Ambiguities

1. **Parking CCT floor area measurement** — how is parking slot "floor area" measured for denominator purposes? Some master deeds assign nominal area (e.g., 12 sqm), others use actual stall dimensions.
2. **Rounding convention** — no regulation specifies rounding when interest percentages don't divide evenly; practice varies (2–4 decimal places).
3. **Limited common area allocation** — exclusive-use areas (balconies, gardens) may carry separate interest allocation in some master deeds; no standard formula.
4. **Sinking fund mandatory minimum** — no DHSUD regulation specifies a mandatory sinking fund percentage; purely board-determined.
5. **No minimum common area requirement** — no statutory minimum percentage of floor area must be common areas; ratio determined by developer design and National Building Code lot occupancy limits.

---

## Cross-References

- **`condo-association-dues`** (Wave 2, pending) — the HLURB operational formula for monthly dues is documented here as part of Computation 4 but will be analyzed in full as a standalone aspect
- **`assessment-level-lookup`** (Wave 2, pending) — the RPT rate tiers referenced in Computation 3 depend on this aspect's analysis
- **`ph-tax-computations-reverse`** — VAT on association dues (12% if >₱3M) crosses into the tax loop's domain

## Sources

### Primary Statutes
- [RA 4726](https://lawphil.net/statutes/repacts/ra1966/ra_4726_1966.html) — Condominium Act
- [RA 7899](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/2928) — RA 4726 Amendment (voting)
- [Civil Code Book II, Art. 485](https://chanrobles.com/civilcodeofthephilippinesbook2.htm) — co-ownership
- [Local Government Code](https://lawphil.net/statutes/repacts/ra1991/ra_7160_1991.html) — RPT (§§218, 233, 235, 236)

### Jurisprudence
- *Concorde Condominium v. PNB*, G.R. No. 228354 — Section 20 lien superiority

### Government Sources
- [IRR of PD 957 (DHSUD)](https://dhsud.gov.ph/wp-content/uploads/Laws_Issuances/02_IRR/IRRPD957.pdf)
- RMC 65-2012 — VAT on condominium corporation receipts

### Practitioner & Secondary Sources
- [U-Property PH — RA 4726 Explained](https://upropertyph.com/2025/11/18/the-condominium-act-of-the-philippines-ra-4726-explained-for-buyers-and-investors/)
- [Respicio & Co. — RPT on Common Areas](https://www.lawyer-philippines.com/articles/obligation-of-unit-owners-to-pay-real-property-taxes-on-common-areas-in-philippine-condominiums)
- [Respicio & Co. — Parking & Common Area](https://www.respicio.ph/commentaries/condominium-parking-and-common-area-ownership-philippines)
- [Respicio & Co. — Association Dues Multiple Titles](https://www.respicio.ph/commentaries/condominium-association-dues-for-multiple-titles-in-the-philippines)
- [Respicio & Co. — Voting Rights](https://www.respicio.ph/commentaries/voting-rights-based-on-acquired-interest-in-condominiums)
- [DivinaLaw — Pay Dues or Lose Unit](https://www.divinalaw.com/dose-of-law/pay-association-dues-or-lose-your-condo-unit/)
- [3D Academy — Condo Dues Guide](https://3d-universal.com/en/blogs/understanding-condo-dues-and-monthly-fees-in-the-philippines.html)
- [Inquirer — Condo Dues Conundrum](https://business.inquirer.net/345709/biz-buzz-condo-dues-conundrum)
