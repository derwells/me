# Condo Act Common Areas — Source Acquisition

**Wave:** 1
**Date:** 2026-02-25
**Aspect:** condo-act-common-areas
**Sources consulted:** RA 4726 (lawphil.net), IRR of PD 957 (HLURB/DHSUD), practitioner guides

---

## Legal Framework

### Primary Statute: RA 4726 (Condominium Act, 1966)

**Key provisions for computation:**

**Section 2 (Definition):**
A condominium is "a separate interest in a unit... and an undivided interest in common, directly or indirectly, in the land on which it is located and in other common areas." Title to common areas may be held by a condominium corporation "in proportion to the appurtenant interest of their respective units in the common areas."

**Section 4 (Master Deed requirements):**
The master deed must describe:
- All common areas (identification)
- "The exact nature of the interest acquired in such common areas" (but *no specific formula is mandated* — delegated to the master deed)

**Section 6(c) (Default rule):**
> "The common areas are held in common by the holders of units, **in equal shares, one for each unit**"
> — unless the master deed provides otherwise.

This is critical: the statutory *default* is equal shares per unit (not floor-area-proportional). Floor-area-proportional allocation is optional and must be expressly stated in the master deed.

**Section 9(d) (Assessments):**
Each unit owner contributes to common expenses "in proportion (unless otherwise provided) to its owner's fractional interest in any common areas." Still no formula — loops back to the master deed definition.

**RA 7899 (Amendment to RA 4726) — Voting/Majority Computation:**
- Residential/commercial-only projects: majority on **per unit** basis (1 unit = 1 vote)
- Mixed-use projects: majority on **floor area of ownership** basis
- This affects governance but not directly the interest % computation.

---

### Secondary Regulation: PD 957 + IRR (HLURB/DHSUD)

**PD 957 scope:** "Subdivision and Condominium Buyers' Protective Decree" — primarily protects buyers from developer abuse, not a design/computation standard.

**IRR of PD 957 (HLURB):**
Condominium projects must conform to the **National Building Code** for:
- Lot occupancy limits
- Open space
- Parking
- Building setbacks

The IRR itself does not specify a formula for common area percentage allocation among unit owners. For subdivisions (≥1 ha), 30% of gross area must be reserved for open space — but this applies to land area, not to the computation of individual unit owners' shares.

**HLURB Master Deed requirement (IRR Rule):**
Developer must submit "Master Deed with Declaration of Registration and Declaration of Restrictions" — annotated in the title — as a pre-condition for the Certificate of Registration and License to Sell. The percentage of interest per unit must appear in the master deed but HLURB does not prescribe the formula.

---

## De Facto Industry Formula (Not Statutory)

Despite the statutory silence, the uniform industry practice in the Philippines is:

```
Undivided Interest % = Unit Floor Area (sqm) / Total Sellable Floor Area (sqm) × 100
```

- Sum of all unit interest percentages = 100%
- Common areas (corridors, lobbies, pools, etc.) are excluded from the denominator (they are the subject of the interest, not included in it)
- This percentage governs: real property tax on common areas, voting rights (in mixed-use), dues allocation, and any sale/dissolution proceeds

**Example:**
| Unit | Floor Area | Total Sellable Area | Undivided Interest |
|------|-----------|--------------------|--------------------|
| A    | 50 sqm    | 1,000 sqm          | 5.00%              |
| B    | 75 sqm    | 1,000 sqm          | 7.50%              |
| C    | 30 sqm    | 1,000 sqm          | 3.00%              |

---

## Association Dues Computation (HLURB-Defined Formula)

HLURB issued implementing rules defining the dues computation method. This IS a prescribed formula:

```
Step 1: Rate Base = Total Annual Gross Expense / Total Gross Floor Area (sqm)
Step 2: Monthly Rate = Rate Base / 12
Step 3: Monthly Dues per Unit = Unit Floor Area (sqm) × Monthly Rate
```

**Current typical ranges (Metro Manila, 2025):**
- Economy/socialized condos: ₱50–₱80/sqm/month
- Mid-market condos: ₱80–₱150/sqm/month
- High-end/luxury condos: ₱150–₱250+/sqm/month

**Example (One Serendra, Taguig):**
Rate = ₱96/sqm/month (excl. VAT)
70 sqm unit → ₱6,720/month + 12% VAT = ₱7,526.40

**Coverage:** Association dues are subject to 12% VAT if the condominium corporation's annual receipts exceed the VAT threshold.

---

## Key Findings for Wave 2

### What is Deterministic
1. **Association dues computation** — fully deterministic given: (a) unit floor area, (b) total gross expense budget, (c) total gross floor area. Formula is prescribed by HLURB.
2. **Real property tax on common areas** — each unit owner's share = undivided interest % × assessed value of common areas. Deterministic once the undivided interest % is known.

### What is NOT Deterministic
1. **Undivided Interest %** — no statutory formula. The master deed chooses the basis (equal per unit vs. floor-area-proportional vs. custom). Most PH condos use floor-area-proportional in practice, but this is not mandated.
2. **Common area size/boundary** — determined by architect/developer in the master deed, not computed from a formula.

### Regulatory Gaps Found
- RA 4726 contains no formula for undivided interest computation — entirely delegated to master deeds
- The 30% open space rule from PD 957 IRR applies to *subdivisions*, not to condominium buildings per se (condominiums follow the National Building Code for open space)
- No DHSUD circular mandates a specific minimum percentage of floor area that must be common areas in a condominium

---

## Wave 2 Implications

Two separate computations to extract:
1. **`condo-common-area-pct`** — Undivided Interest % computation (note: de facto formula exists, statutory default is different; both must be modeled; master deed is the authoritative input)
2. **`condo-association-dues`** — Monthly dues computation (HLURB prescribed formula; add to Wave 2 frontier if not already captured under secondary fees)

### New Aspects to Add to Frontier
- **`condo-association-dues`** — the HLURB-prescribed formula for computing monthly condo dues per unit (not currently in the frontier as a standalone computation; currently bundled under "association dues computation" in secondary scope). This is highly automatable.

---

## Sources

- [RA 4726 Full Text — lawphil.net](https://lawphil.net/statutes/repacts/ra1966/ra_4726_1966.html)
- [RA 4726 — chanrobles.com](https://chanrobles.com/republicactno4726.html)
- [IRR of PD 957 — DHSUD](https://dhsud.gov.ph/wp-content/uploads/Laws_Issuances/02_IRR/IRRPD957.pdf)
- [DHSUD Developer Registration Requirements](https://dhsud.gov.ph/services/housing-and-real-estate-development-regulation/developer/)
- [Condominium Act Explained — U-Property PH](https://upropertyph.com/2025/11/18/the-condominium-act-of-the-philippines-ra-4726-explained-for-buyers-and-investors/)
- [Lamudi — 15 Things About the Condominium Act](https://www.lamudi.com.ph/journal/15-things-you-need-to-know-about-the-condominium-act/)
- [RichestPH — Decode Condo Association Dues](https://richestph.com/decode-condo-association-dues-in-the-philippines/)
- [ZipMatch — Condo Association Dues FAQs](https://www.zipmatch.com/blog/condo-association-dues-faqs/)
