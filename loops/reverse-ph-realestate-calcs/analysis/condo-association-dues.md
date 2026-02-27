# Condominium Association Dues Computation

**Wave:** 2 — Computation Extraction
**Date:** 2026-02-27
**Aspect:** condo-association-dues
**Primary sources:** `analysis/condo-act-common-areas.md` (Wave 1), `analysis/condo-common-area-pct.md` (Wave 2)
**Verification:** 25 sub-claims verified against 22+ independent sources; 3 high-severity corrections, 3 medium-severity issues; see `analysis/condo-association-dues-verification.md`

---

## Computation 1: Monthly Association Dues (HLURB ECR 001-17 §8)

**What it computes:** The monthly dues payable by each unit owner or beneficial user to the condominium corporation for maintenance, administration, and upkeep of common areas.

**Legal basis:**
- RA 4726 Section 9(d) — statutory basis for assessments proportional to undivided interest
- HLURB Executive Committee Resolution No. 001-17 (March 8, 2017) — operational formula
- RA 9904 Section 10(b) — board power to collect dues as approved by majority of members

**Applicability note:** ECR 001-17 was issued for homeowners' associations under RA 9904. It applies directly to HOAs and to associations in condominium projects where management is not vested in a condominium corporation. For condominium corporations proper (organized under RA 4726 + Revised Corporation Code), the ECR formula is not directly mandated but is the de facto industry standard universally adopted. The statutory basis for condo corporation dues is RA 4726 §9(d) — "in proportion to its owner's fractional interest in any common areas."

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `total_annual_gross_expense` | float (₱) | Condo corporation approved annual budget (including admin salaries, utilities, maintenance, insurance, security, management fees, etc.) |
| `contingency_pct` | float | 10% for members, 20% for beneficial users (ECR 001-17 §8.1) |
| `gross_area` | float (sqm) | Total lot and floor area of all members/beneficial users (ECR 001-17 §8.2) |
| `unit_floor_area` | float (sqm) | Individual unit floor area from CCT |

**Formula:**
```
Step 1: gross_expense = average_monthly_expense × 12
        (or, if not feasible: highest_monthly_expense × 12)
        + (gross_expense × contingency_pct)

Step 2: rate_base = gross_expense / gross_area    (₱/sqm/year)

Step 3: monthly_rate = rate_base / 12             (₱/sqm/month)

Step 4: monthly_dues_member = unit_floor_area × monthly_rate × 1.10
        monthly_dues_beneficial_user = unit_floor_area × monthly_rate × 1.20
```

**Equivalence to statutory formula:** When the master deed uses floor-area-proportional allocation:
```
monthly_dues = (unit_floor_area / total_sellable_area) × total_monthly_expenses
             = undivided_interest_pct / 100 × total_monthly_expenses
```
This is algebraically equivalent to the ECR formula (without buffers). The +10%/+20% buffer is an ECR addition not in the statute.

**Rules:**
- "Gross area" per ECR = total lot and floor area attributable to all members and beneficial users — not identical to developer "total saleable area" (though in practice these converge once all units are sold)
- Developer holding unsold units is a "beneficial user" and pays +20% rate on its unsold inventory
- The contingency buffer (10%/20%) is meant to cover collection shortfalls, not a profit margin
- Budget must be prepared annually; board proposes, membership approves
- Budget and explanatory notes must be posted on bulletin boards and delivered to unit owners (DHSUD rules)

**Worked example:**
```
Total annual gross expense:         ₱12,000,000
+ 10% contingency:                  ₱ 1,200,000
Total chargeable:                   ₱13,200,000
Gross area (all saleable):          10,000 sqm
Rate base:                          ₱1,320/sqm/year
Monthly rate:                       ₱110/sqm/month

Unit A (50 sqm, member):            50 × ₱110 × 1.10 = ₱6,050/month
Unit B (30 sqm, beneficial user):   30 × ₱110 × 1.20 = ₱3,960/month
```

**Edge cases:**
- Mixed-use (residential + commercial): master deed may specify different rates per use type
- Parking CCTs: if separately titled, floor area included in gross area; owner pays dues on parking CCT separately
- Developer turnover: developer pays beneficial-user-rate dues on all unsold units until majority of units sold
- Multiple units: owner pays per-CCT dues on each unit held

**Deterministic:** Yes — given approved budget, gross area, and unit floor area.

**Verification status:** CONFIRMED — core formula verified across 3 independent sources (Jur.ph, Inquirer Business, Studocu). Minor correction: "gross area" framing refined from "saleable area" to "total lot+floor area of members/beneficial users."

---

## Computation 2: Sinking/Reserve Fund Contribution

**What it computes:** The monthly contribution per unit to the condominium's reserve fund for major capital expenditures, equipment replacement, and emergency repairs.

**Legal basis:**
- RA 4726 Section 9 — declaration of restrictions may provide for reserve fund
- No specific statute or regulation mandates a formula or minimum percentage

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `method` | enum: "flat_per_sqm" / "pct_of_dues" | Board resolution |
| `flat_rate` | float (₱/sqm/month) | Board resolution (if flat method) |
| `pct_of_dues` | float (%) | Board resolution (if percentage method) |
| `unit_floor_area` | float (sqm) | CCT |
| `monthly_dues` | float (₱) | From Computation 1 |

**Formula (flat per-sqm method):**
```
monthly_sinking_fund = unit_floor_area × flat_rate
```

**Formula (percentage of dues method):**
```
monthly_sinking_fund = monthly_dues × pct_of_dues / 100
```

**Typical ranges (Metro Manila, 2025):**
- Flat rate: ₱4–₱15/sqm/month
- Percentage: 5–10% of monthly association dues
- Either method produces similar amounts: at ₱80–₱150/sqm total dues, 5–10% = ₱4–₱15/sqm

**Rules:**
- No statutory formula mandated — amount is board-determined, subject to membership approval for changes
- Typically billed as a separate line item from regular dues (not embedded)
- Funds intended for: elevator modernization, façade repairs, roof replacement, fire safety upgrades, waterproofing, repainting, structural repairs
- Practitioner guidance: low reserve fund is a red flag for buyers; signals future special assessments
- "10% statutory floor" claim for reserve fund level: **UNVERIFIED** — a single commentary source (Respicio & Co.) references this without citing a specific DHSUD issuance; no statutory or regulatory basis found in RA 4726, RA 9904, or published DHSUD circulars. Treat with skepticism.

**Deterministic:** Yes — given board-determined rate and unit floor area. Non-deterministic element: the rate itself (requires board decision + membership approval).

**Verification status:** CONFIRMED (typical ranges and methods). UNVERIFIED (10% statutory floor claim — flagged).

---

## Computation 3: Special Assessment Allocation

**What it computes:** Each unit owner's share of a one-time special assessment for extraordinary or unbudgeted common expenses.

**Legal basis:**
- RA 4726 Section 9(d) — proportional sharing of common expenses
- RA 4726 Section 20 — assessment lien mechanism
- Master deed / declaration of restrictions / by-laws

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `total_special_assessment` | float (₱) | Board resolution + membership approval |
| `undivided_interest_pct` | float (%) | CCT / master deed |
| OR `unit_floor_area` | float (sqm) | CCT |
| AND `total_sellable_area` | float (sqm) | Master deed |

**Formula:**
```
unit_special_assessment = total_special_assessment × undivided_interest_pct / 100

# Equivalent (floor-area basis):
unit_special_assessment = total_special_assessment × (unit_floor_area / total_sellable_area)
```

**Approval requirements (verified):**
1. Board resolution proposing the assessment (majority of board)
2. Written notice to all members at least 15 days before general meeting (per RA 9904 IRR)
3. Simple majority vote (50%+1) of all members in good standing at general meeting
4. Assessment must serve a lawful common-area purpose
5. Funds must be placed in a **separate trust account** from regular dues (commingling is an audit red flag)

**Rules:**
- Pro-rata allocation by undivided interest % unless governing documents specify otherwise
- One-time or time-bounded — not for recurring operational expenses
- Tax treatment: EXEMPT from VAT per NIRC §109(1)(Y) as amended by TRAIN Law
- Must be tied to legitimate common area costs (structural repairs, elevator modernization, disaster recovery, fire safety upgrades, etc.)
- Some by-laws allow board to impose small special assessments (below a threshold) without membership vote
- Hierarchical authority: law → master deed → by-laws → house rules (if conflict)

**Edge cases:**
- Limited common area repairs (e.g., balcony waterproofing): may be allocated only to units with that limited common area per master deed
- Emergency assessments: some by-laws allow board to act first with ratification within 30–60 days

**Deterministic:** Yes — given total assessment amount and unit's undivided interest percentage.

**Verification status:** CONFIRMED — dual approval mechanism, separate trust account, pro-rata allocation all verified. "3-week notice + 2-week posting" timeframes from earlier source UNVERIFIED — standard is 15 days per RA 9904 IRR.

---

## Computation 4: Delinquency Interest/Penalty on Unpaid Dues

**What it computes:** Interest and penalties accruing on overdue association dues, special assessments, or other charges.

**Legal basis:**
- HLURB ECR 001-17 Section 8.5 — 12% p.a. maximum
- RA 4726 Section 20 — assessment lien (interest "as may be provided for in the declaration of restrictions")
- Condominium by-laws (specific rates must be stated)

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `overdue_amount` | float (₱) | Unpaid dues/assessments |
| `annual_interest_rate` | float (%) | By-laws (max 12% p.a. per ECR 001-17) |
| `months_delinquent` | integer | Calendar months since due date |

**Formula:**
```
# Simple interest (most common per-month computation)
monthly_rate = annual_interest_rate / 12
penalty = overdue_amount × monthly_rate / 100 × months_delinquent

# Running balance (if compound per by-laws)
balance = overdue_amount × (1 + monthly_rate / 100) ^ months_delinquent
penalty = balance - overdue_amount
```

**Rules:**
- Maximum rate: **12% per annum** (ECR 001-17 §8.5) — this is a ceiling, not a prescribed rate
- Rate must be **authorized in the by-laws** to be enforceable (no by-law authority = no penalty)
- Typical practice: 2–4% per month (within the 12% p.a. ceiling? — **conflict**: 3%/month = 36% p.a., which exceeds 12% ceiling; some by-laws may predate ECR 001-17 or not comply)
- Penalty computation starts after grace period (typically 15–30 days after due date per by-laws)
- By-laws may suspend voting rights of delinquent members
- Unpaid amount + penalty may constitute basis for assessment lien (Computation 5)

**Edge cases:**
- Pre-ECR-001-17 by-laws with higher rates: ECR ceiling should supersede, but enforceability may require by-laws amendment
- Partial payment: applied to oldest outstanding balance first (typical by-laws provision)
- Interest vs. penalty: some by-laws distinguish between interest (compensatory) and penalty (deterrent); ECR 12% cap appears to cover both

**Deterministic:** Yes — given overdue amount, rate (from by-laws), and delinquency period.

**Verification status:** CONFIRMED — 12% p.a. cap verified across 3 sources; by-laws authorization requirement confirmed. Potential conflict between common practice (2–4%/month) and ECR ceiling flagged.

---

## Computation 5: Assessment Lien Amount (RA 4726 §20)

**What it computes:** The total lien amount registrable against a delinquent unit owner's condominium certificate of title.

**Legal basis:**
- RA 4726 Section 20
- Act No. 3135 (extrajudicial foreclosure procedure)
- *First Marbella Condominium v. Gatmaytan* (G.R. No. 163196, July 4, 2008)
- *Concorde Condominium v. PNB* (G.R. No. 228354)

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `unpaid_assessment` | float (₱) | Overdue dues + special assessments |
| `accrued_interest` | float (₱) | From Computation 4 |
| `penalties` | float (₱) | Per by-laws/declaration of restrictions |
| `attorney_fees` | float (₱) | Per declaration of restrictions |
| `other_costs` | float (₱) | Filing/registration costs |

**Formula:**
```
lien_amount = unpaid_assessment + accrued_interest + penalties + attorney_fees + other_costs
```

**Lien creation procedure:**
1. Management body prepares Notice of Assessment stating: amount, charges, unit description, registered owner name
2. Notice signed by authorized representative
3. Notice registered with Register of Deeds
4. Lien attaches upon registration

**CORRECTED — Lien priority (HIGH-SEVERITY correction from verification):**
```
Priority hierarchy:
1. Real property tax liens (always superior)
2. Liens registered BEFORE the assessment notice (maintain their priority — e.g., existing mortgages)
3. Assessment lien (registered per §20)
4. Liens registered AFTER the assessment notice (subordinate to assessment lien)

Exception: Declaration of restrictions may voluntarily subordinate the assessment lien
to other specified encumbrances.
```

The Wave 1 analysis and the `condo-common-area-pct` analysis (Computation 4) overstated the lien priority as "superior to all except RPT liens." The actual statutory text says "superior to all other liens **registered subsequent to the registration of said notice of assessment** except real property tax liens." This means pre-existing mortgages retain their priority — a critical distinction for lenders and buyers.

**Foreclosure (confirmed via *First Marbella*, GR 163196):**
- Section 20 authorizes enforcement via judicial or extrajudicial foreclosure
- However, **Section 20 does not ipso facto authorize foreclosure** — the management body must have:
  - Express authority in the declaration of restrictions / master deed (a "special power of attorney" clause), OR
  - A court order for judicial foreclosure
- Act No. 3135 procedural requirements must be followed for extrajudicial foreclosure
- Unit owner has right of redemption (same as mortgage foreclosure)

**Release:** Upon full payment, management body registers a release of lien with the Register of Deeds.

**Rules:**
- Lien attaches to the **unit**, not the person — buyers of resale units may inherit unpaid liens
- Prescription: 10-year period under Civil Code Article 1144 (written contracts)
- Charges must be "as may be provided for in the declaration of restrictions" — overcharging beyond what's authorized in the declaration is unenforceable

**Deterministic:** Yes — given the component amounts per declaration of restrictions.

**Verification status:** CONFIRMED with HIGH-SEVERITY CORRECTION on lien priority. First Marbella holding confirmed across 3 sources.

---

## Computation 6: Dues Increase Compliance Check

**What it computes:** Whether a proposed dues increase requires membership approval and/or regulatory filing.

**Legal basis:**
- RA 9904 IRR — 10% annual cap without membership vote (applies to HOAs; de facto standard for condo corps)
- RA 4726 — no specific cap (governed by master deed / by-laws / Revised Corporation Code)
- DHSUD/HSAC regulatory oversight

**Inputs:**
| Input | Type | Source |
|-------|------|--------|
| `current_monthly_dues` | float (₱) | Existing approved rate |
| `proposed_monthly_dues` | float (₱) | Board proposal |

**Formula:**
```
increase_pct = (proposed_monthly_dues - current_monthly_dues) / current_monthly_dues × 100

IF increase_pct <= 10:
    → Board may approve without general membership vote
    → No regulatory filing required
ELSE:
    → Requires majority vote (50%+1) of total membership at general meeting
    → Written notice at least 15 days before meeting with justification
    → Budget and explanatory notes must be posted on bulletin boards and delivered to unit owners
    → Filing with DHSUD for monitoring (per practitioner guidance; exact regulatory basis unclear)
```

**CORRECTION (MEDIUM-SEVERITY from verification):**
The original extraction characterized this as "HSAC regulatory clearance." This mischaracterizes the mechanism:
- HSAC is a quasi-judicial body (adjudicates disputes), not a regulatory pre-approval body
- The 10% threshold triggers a **membership vote requirement**, not HSAC pre-clearance
- DHSUD handles regulatory oversight and monitoring
- One source claims HSAC regulatory clearance is "compulsory" (Respicio & Co.), but this appears to describe a filing/monitoring requirement rather than a pre-approval gate
- "Proposed increase to 15% threshold" per draft HSAC circular: **UNVERIFIED** — single source only

**Rules:**
- 10% cap per annum is from RA 9904 IRR — applies directly to HOAs; condo corporations adopt this standard in practice
- For condo corporations organized under RA 4726 + Revised Corporation Code, the by-laws govern increase procedures
- Justification must be based on verifiable needs (inflation, tariff increases, new regulations)
- Regional arbiters have granted accelerated approvals where utility tariffs jumped >15%

**Deterministic:** Yes — given current and proposed rates, and the applicable threshold.

**Verification status:** CONFIRMED (10% threshold, membership vote requirement). CORRECTED (mechanism is membership vote, not HSAC pre-clearance). UNVERIFIED (proposed 15% threshold change).

---

## Computation 7: Tax Status Determination for Condo Corporation Income

**What it computes:** Whether specific income streams of the condominium corporation are subject to income tax, VAT, or percentage tax.

**Legal basis:**
- **BIR v. First E-Bank Tower Condominium Corp.** (G.R. Nos. 215801/218924, January 15, 2020) — SC invalidated RMC 65-2012
- **NIRC Section 109(1)(Y)** as amended by TRAIN Law (RA 10963) — express VAT exemption for association dues
- NIRC Sections 105, 108 — VAT on services (commercial income)
- NIRC Section 109(1)(BB) — ₱3M threshold exemption

**CRITICAL CORRECTION to Wave 1 and condo-common-area-pct analyses:**

The Wave 1 analysis (`condo-act-common-areas.md` line 98) stated: "Association dues are subject to 12% VAT if the condominium corporation's annual receipts exceed the VAT threshold." The `condo-common-area-pct` analysis (Computation 4) stated: "VAT: 12% on association dues if condo corporation's annual receipts exceed ₱3M VAT threshold (RMC 65-2012)."

**Both are WRONG.** RMC 65-2012 has been invalidated by the Supreme Court. Association dues are NOT subject to VAT under current law.

**Decision tree:**
```
INPUT: income_type, annual_gross_receipts_commercial

IF income_type == "association_dues" OR
   income_type == "membership_fees" OR
   income_type == "special_assessments":
    → EXEMPT from income tax (SC: "do not constitute profit or gain")
    → EXEMPT from VAT (NIRC §109(1)(Y); SC: "not from sale/barter/exchange")
    → EXEMPT from withholding tax (SC: no income tax → no withholding basis)
    → No BIR form filing required for these amounts

ELSE IF income_type == "commercial_income":
    # e.g., rooftop lease to telco, event space rental, commercial unit lease
    IF annual_gross_receipts_commercial > 3,000,000:
        → Subject to 12% VAT (NIRC §108)
        → Must register as VAT taxpayer within 10 days of crossing threshold
        → Subject to income tax (corporate rate or 8% flat if eligible)
    ELSE:
        → Exempt from VAT (NIRC §109(1)(BB))
        → Subject to 3% percentage tax (NIRC §116, payable via BIR Form 2551Q)
        → Subject to income tax

    # CWT on commercial lease:
    IF lessee is a top withholding agent (per RR 14-2019):
        → 5% creditable withholding tax on gross lease payments
```

**Rules:**
- Association dues and commercial income are treated as **completely separate** income streams
- The ₱3M threshold applies only to commercial income, not to total receipts including dues
- Optional VAT registration available even below ₱3M (irrevocable for 3 years per RR 9-2011)
- Condo corporation must maintain separate accounting for dues vs. commercial income

**Deterministic:** Yes — given income type and annual commercial gross receipts.

**Verification status:** CONFIRMED — SC ruling verified (GR 215801, Jan 15, 2020). TRAIN Law §109(1)(Y) confirmed. Commercial income treatment confirmed. **CORRECTED: subsection is (Y) not (L)** — Section 109(1)(L) covers agricultural cooperative transactions.

---

## Summary Table

| # | Computation | Inputs | Deterministic | Verification | Legal Basis |
|---|------------|--------|---------------|-------------|-------------|
| 1 | Monthly association dues | budget, gross_area, unit_sqm | Yes | Confirmed | RA 4726 §9(d), ECR 001-17 §8 |
| 2 | Sinking/reserve fund | rate (board-set), unit_sqm | Yes (given rate) | Confirmed (rates); Unverified (10% floor) | RA 4726 §9, by-laws |
| 3 | Special assessment allocation | total_assessment, interest_pct | Yes | Confirmed | RA 4726 §§9, 20 |
| 4 | Delinquency interest/penalty | overdue_amt, rate, months | Yes | Confirmed | ECR 001-17 §8.5 (12% cap) |
| 5 | Assessment lien amount | unpaid + interest + costs | Yes | Confirmed w/ correction | RA 4726 §20, First Marbella |
| 6 | Dues increase compliance | current, proposed rates | Yes | Confirmed w/ correction | RA 9904 IRR (10% cap) |
| 7 | Tax status determination | income_type, gross_receipts | Yes | Confirmed w/ correction | GR 215801, NIRC §109(1)(Y) |

**All 7 computations are fully deterministic** given the required inputs (approved budget, by-laws parameters, contractual/regulatory inputs).

---

## Corrections Applied (from verification against 22+ sources)

### Critical (3)
1. **VAT on association dues — WRONG in Wave 1/Wave 2.** RMC 65-2012 invalidated by SC (GR 215801, Jan 15, 2020). Association dues exempt from income tax, VAT, and withholding tax. TRAIN Law §109(1)(Y) independently confirms. Prior analyses' statements that dues are subject to 12% VAT if receipts exceed ₱3M are incorrect — only commercial income is subject to VAT.
2. **TRAIN Law subsection is §109(1)(Y), not §109(1)(L).** Section 109(1)(L) covers agricultural cooperative transactions.
3. **Assessment lien priority overstated.** Lien is superior only to liens registered *subsequent* to the assessment notice, not to all liens. Pre-existing mortgages retain priority. The "registered subsequent" qualifier is legally critical.

### High Severity (1)
4. **DHSUD 10% statutory floor for reserve fund — UNVERIFIED.** No DHSUD department order, circular, or statutory provision could be independently located. Single-source claim (Respicio & Co.) without regulatory citation. Flagged as potentially fabricated.

### Medium Severity (3)
5. **"HSAC regulatory clearance"** mischaracterizes the dues increase mechanism. The 10% threshold triggers membership vote, not HSAC pre-approval.
6. **"3-week notice + 2-week posting"** timeframes for special assessments not found in statute. Standard is 15 days written notice per RA 9904 IRR.
7. **"Proposed 15% threshold increase"** per draft HSAC circular — single source only, unverifiable.

### Low Severity (2)
8. **"Gross area" framing** — ECR 001-17 defines as "total lot and floor area of members/beneficial users," not "total saleable area" (though practically equivalent once all units are sold).
9. **Economy condo dues range** — ₱50–₱100/sqm/month (not ₱50–₱80 as initially stated).

---

## Unresolved Ambiguities

1. **ECR 001-17 applicability to condo corporations** — The ECR was issued for HOAs under RA 9904. RA 9904 does NOT apply to condominium corporations (confirmed per multiple sources). The ECR formula is the industry standard for condo corps but has no direct statutory mandate for them. Whether DHSUD can enforce the ECR formula against a condo corporation organized under RA 4726 is unclear.

2. **Penalty rate practice vs. ECR ceiling** — Many by-laws prescribe 2–4%/month penalty, which = 24–48% p.a. — far exceeding the ECR 001-17 cap of 12% p.a. Whether the ECR ceiling supersedes pre-existing by-laws for condo corporations is untested.

3. **Sinking fund minimum** — No verified regulatory minimum exists. The claimed "10% statutory floor" from one source could not be confirmed. Whether any DHSUD internal policy establishes such a floor is unknown.

4. **Compound vs. simple interest for penalties** — ECR 001-17 caps at "12% per annum" but does not specify whether this is simple or compound. Practice varies by by-laws.

5. **Developer control period dues** — Developer pays beneficial-user-rate dues (+20%) on unsold units but controls the board. Whether the developer can effectively set its own dues rate during this period (self-dealing risk) is a governance issue, not a computation issue, but affects input parameters.

---

## Cross-References

- **`condo-common-area-pct`** (Wave 2, completed) — Computation 4 in that analysis covers the statutory proportional-share formula; this analysis expands on the HLURB operational formula, special assessments, delinquency, liens, increases, and tax status
- **`assessment-level-lookup`** (Wave 2, completed) — RPT rates relevant to Computation 5 (lien includes RPT delinquency in some cases)
- **`ph-tax-computations-reverse`** — The VAT/income tax exemption of association dues and the commercial income VAT threshold are tax topics; this analysis documents them for cross-reference but the tax loop should capture the full NIRC §109(1)(Y) treatment
- **`broker-commission`** (Wave 2, completed) — EWT rate corrections in that analysis (RR 11-2018 TRAIN rates) are analogous to the tax corrections here

## Sources

### Primary Statutes
- [RA 4726 — Condominium Act](https://lawphil.net/statutes/repacts/ra1966/ra_4726_1966.html) — Sections 9(d), 20
- [RA 9904 — Magna Carta for Homeowners](https://lawphil.net/statutes/repacts/ra2010/ra_9904_2010.html) — Sections 9, 10(b), 20
- [NIRC Section 109 as amended by TRAIN Law](https://lawphil.net/statutes/repacts/ra2017/ra_10963_2017.html) — §109(1)(Y)

### Regulations
- [HLURB Executive Committee Resolution No. 001-17](https://legaldex.com/laws/guidelines-in-the-kinds-of-dues-fees-and-contributions-that) — §§7, 8
- [DHSUD Department Order No. 2021-007](https://lpr.adb.org/resource/2021-revised-implementing-rules-and-regulations-magna-carta-homeowners-and-homeowners) — Revised IRR of RA 9904

### Jurisprudence
- *BIR v. First E-Bank Tower Condominium Corp.*, [G.R. Nos. 215801/218924](https://lawphil.net/judjuris/juri2020/jan2020/gr_215801_2020.html), January 15, 2020 — RMC 65-2012 invalidated; dues exempt from IT/VAT/WT
- *First Marbella Condominium v. Gatmaytan*, G.R. No. 163196, July 4, 2008 — §20 does not ipso facto authorize foreclosure
- *Concorde Condominium v. PNB*, G.R. No. 228354 — lien enforcement

### Practitioner & Secondary Sources
- [Jur.ph — ECR 001-17 Summary](https://jur.ph/laws/summary/guidelines-in-the-kinds-of-dues-fees-and-contributions-that-may-be-collected-by-homeowners-associations)
- [Inquirer Business — Homeowners Associations' Dues](https://business.inquirer.net/230348/homeowners-associations-dues)
- [Respicio & Co. — Special Assessment Fees](https://www.respicio.ph/commentaries/special-assessment-fees-in-condominiums-legal-requirements-philippines)
- [Respicio & Co. — Dues Increase Limits](https://www.respicio.ph/commentaries/homeowners-association-dues-increase-limits-philippines)
- [DivinaLaw — Pay Dues or Lose Unit](https://www.divinalaw.com/dose-of-law/pay-association-dues-or-lose-your-condo-unit/)
- [3D Academy — Condo Dues 2025 Guide](https://3d-universal.com/en/blogs/understanding-condo-dues-and-monthly-fees-in-the-philippines.html)
- [RichestPH — Decode Condo Association Dues](https://richestph.com/decode-condo-association-dues-in-the-philippines/)
- [PwC Philippines — Tax Landscape of Condominiums](https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2020-taxwise-or-otherwise/transforming-the-tax-landscape-of-condominiums.html)
- [Grant Thornton PH — Reconciling Condo Act and NIRC](https://www.grantthornton.com.ph/insights/articles-and-updates1/lets-talk-tax/reconciling-the-condominium-act-and-the-nirc-for-tax-exemption/)
- [KPMG Philippines — InTAX June 2020](https://kpmg.com/ph/en/home/insights/2020/06/special-intax-june-2020-issue1-volume5.html)
- [Manila Times — VAT on Condominium Dues](https://www.manilatimes.net/2026/01/13/legal-advice/propriety-of-imposition-of-vat-on-condominium-association-dues/2257342)
