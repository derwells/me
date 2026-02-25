# Highest-of-Three Tax Base Resolution

**Wave:** 2 — Computation Extraction
**Date:** 2026-02-25
**Verification Status:** CONFIRMED (cross-checked against 5+ independent sources)
**Deterministic:** YES (once all three input values are known)

---

## Summary

The "highest-of-three" rule is the central tax base computation for all Philippine real estate transaction taxes. It resolves the taxable value as:

```
Tax Base = max(Gross Selling Price, BIR Zonal Value × Area, Assessor FMV)
```

This is not literally a "three-way max" in statute — the NIRC structures it as two nested comparisons — but the computational result is identical to `max(SP, ZV, AFMV)`.

---

## Statutory Structure

**Step 1 — FMV per Section 6(E):**

> "The Commissioner is hereby authorized to divide the Philippines into different zones or areas and shall … determine the fair market value of real properties located in each zone or area."

BIR zonal values are the Commissioner's prescribed FMV under Section 6(E). However, the NIRC cross-references the assessor's schedule as a floor:

```
FMV_6E = max(BIR Zonal Value × Area, Assessor's Schedule of Market Values)
```

**Step 2 — Transaction tax base:**

Every real property transaction tax provision reads: "gross selling price or fair market value [per Section 6(E)], whichever is higher."

```
Tax Base = max(Gross Selling Price, FMV_6E)
         = max(Gross Selling Price, max(BIR Zonal Value × Area, Assessor FMV))
         = max(Gross Selling Price, BIR Zonal Value × Area, Assessor FMV)
```

---

## Inputs

| Input | Type | Source | Notes |
|---|---|---|---|
| `gross_selling_price` | currency (PHP) | Deed of Sale | Stated consideration |
| `bir_zonal_value_per_sqm` | currency (PHP/sqm) | BIR Zonal Value schedule (by RDO zone) | Multiply by `land_area_sqm` for total |
| `land_area_sqm` | numeric (sqm) | TCT / technical description | |
| `assessor_fmv` | currency (PHP) | LGU assessor's Tax Declaration | Not the AV — this is the declared FMV before assessment level is applied |

**Output:** `tax_base` (PHP) — single value used as base for all transaction taxes

---

## Algorithm

```python
def resolve_tax_base(
    gross_selling_price: float,
    bir_zonal_value_per_sqm: float,
    land_area_sqm: float,
    assessor_fmv: float,
) -> dict:
    """
    Resolves the Philippine real estate tax base per NIRC Sec. 24(D) / 6(E).
    Returns the tax base and which value triggered it.
    """
    zonal_total = bir_zonal_value_per_sqm * land_area_sqm
    fmv_6e = max(zonal_total, assessor_fmv)          # Section 6(E) FMV
    tax_base = max(gross_selling_price, fmv_6e)       # Transaction base

    # Determine triggering value (for audit trail)
    candidates = {
        "selling_price": gross_selling_price,
        "zonal_value": zonal_total,
        "assessor_fmv": assessor_fmv,
    }
    triggering_value = max(candidates, key=candidates.get)

    return {
        "tax_base": tax_base,
        "fmv_6e": fmv_6e,
        "zonal_total": zonal_total,
        "triggering_value": triggering_value,
    }
```

---

## Which Taxes Use This Base

| Tax | Legal Basis | Exact Statutory Language | Base Resolution | Rate |
|---|---|---|---|---|
| Capital Gains Tax | NIRC Sec. 24(D)(1), 27(D)(5) | "gross selling price or current fair market value as determined in accordance with Section 6(E), whichever is higher" | Full three-way max | 6% final |
| Documentary Stamp Tax (conveyance) | NIRC Sec. 196 | "consideration or fair market value, whichever is higher" + Sec. 6(E) FMV | Full three-way max | 1.5% (₱15/₱1,000) |
| Creditable Withholding Tax (ordinary assets) | NIRC Sec. 57 / RR 2-98 Sec. 2.57.2(J) | "higher of gross selling price / total consideration or fair market value per Section 6(E)" | Full three-way max | 1.5–6% (rate varies) |
| VAT on real property | NIRC Sec. 106 / RR 16-2005 Sec. 4.106-4 | "consideration stated in the sales document or the fair market value, whichever is higher" where FMV = higher of zonal and assessed | Full three-way max | 12% |
| Local Transfer Tax | RA 7160 Sec. 135 | "total consideration or fair market value in case the monetary consideration is not substantial, whichever is higher" | Three-way max in practice (FMV = max(zonal, assessed)) | 0.50–0.75% |

**Key finding:** Every real property transaction tax uses the same base. A single `tax_base` computation serves all five taxes simultaneously.

---

## Worked Examples

**Example A — Selling Price is Highest:**
- Gross Selling Price: ₱8,000,000
- BIR Zonal Value: ₱5,000/sqm × 1,200 sqm = ₱6,000,000
- Assessor FMV: ₱5,500,000
- FMV_6E = max(₱6,000,000, ₱5,500,000) = ₱6,000,000
- Tax Base = max(₱8,000,000, ₱6,000,000) = **₱8,000,000** (SP triggers)
- CGT = 6% × ₱8,000,000 = ₱480,000
- DST = 1.5% × ₱8,000,000 = ₱120,000

**Example B — Zonal Value is Highest:**
- Gross Selling Price: ₱3,800,000
- BIR Zonal Value: ₱4,500/sqm × 1,000 sqm = ₱4,500,000
- Assessor FMV: ₱3,200,000
- FMV_6E = max(₱4,500,000, ₱3,200,000) = ₱4,500,000
- Tax Base = max(₱3,800,000, ₱4,500,000) = **₱4,500,000** (zonal triggers)
- CGT = 6% × ₱4,500,000 = ₱270,000
- Note: Seller receives ₱3,800,000 but pays CGT on ₱4,500,000

**Example C — Assessor FMV is Highest (rare):**
- Gross Selling Price: ₱5,000,000
- BIR Zonal Value: ₱3,000/sqm × 1,200 sqm = ₱3,600,000
- Assessor FMV: ₱5,800,000 (fresh appraisal for premium improvements)
- FMV_6E = max(₱3,600,000, ₱5,800,000) = ₱5,800,000
- Tax Base = max(₱5,000,000, ₱5,800,000) = **₱5,800,000** (assessor triggers)

---

## Edge Cases and Special Rules

### Condominiums — Unit vs. Building Classification
- Zonal value for condos is per **unit** (RC or CC code), not per sqm of land
- Unit zonal value is pulled directly from the condo table (no area multiplication)
- Building assessment levels apply to the unit's FMV for RPT, but not for transactional tax base

### Improvements / Buildings on Land
- Separate assessor values exist for land and building
- For transactional taxes, the tax base covers both land AND improvements together
- Assessor FMV input = Total Tax Declaration value (land + building combined)

### Partial Interest / Fractional Ownership
- Tax base is prorated proportionally to the fraction of ownership being transferred
- e.g., 50% undivided share → Tax Base = 50% × max(SP, ZV, AFMV)

### "Not Substantial" Consideration — Transfer Tax Only
- RA 7160 Sec. 135 language "in case the monetary consideration is not substantial" suggests FMV substitution applies only when SP is artificially low
- In practice: BIR and LGU both apply the highest-of-three regardless of whether SP is "substantial"
- No formal BIR ruling defines "not substantial" threshold — treated as always applying to any declared price below FMV

### Installment Sales — Tax Base Timing
- The tax base is determined at the **time of sale** (date of notarization of the deed / Contract to Sell)
- Subsequent installment payments use the same pre-determined tax base, not the value at time of each payment
- Confirmed by BIR Ruling OT-028-2024

### RPVARA Transition (RA 12001, June 2024)
- New law transfers BIR zonal value authority to LGU assessors under DOF/BLGF approval
- Transition period target: ~mid-2026
- During transition: BIR zonal values remain operative
- Post-transition: three-way max collapses to two-way max (SP vs. unified SMV)
- **Automation implication:** Any engine built now must be designed to handle both the current three-source model and the post-RPVARA two-source model

---

## Data Dependencies

This computation is deterministic ONLY if the following inputs can be resolved:

1. **BIR Zonal Value lookup** → Requires:
   - Property address → RDO jurisdiction mapping
   - Barangay + street + vicinity descriptor matching in BIR Excel workbook
   - Property classification code (RR, CR, RC, CC, I, A1–A50)
   - For unlisted properties: fallback rules (see `zonal-value-lookup` aspect)

2. **Assessor FMV** → Requires:
   - Current Tax Declaration from LGU Assessor's Office
   - Note: This is the FMV column in the Tax Declaration, NOT the "Assessed Value" (which is FMV × assessment level)

3. **Gross Selling Price** → From deed of sale (user-provided)

**Automation classification of data dependencies:**
- Gross Selling Price: user input (deterministic)
- Assessor FMV: document upload (Tax Declaration) — deterministic once obtained
- BIR Zonal Value: requires lookup engine → **the hardest data dependency** (no API; 127 RDOs; heterogeneous formats)

---

## Verification Summary

**Primary sources used:**
- NIRC Sec. 24(D)(1), 27(D)(5), 6(E) — statutory text
- RR 2-98 Sec. 2.57.2(J) — CWT base definition
- RR 16-2005 Sec. 4.106-4 — VAT base definition
- RA 7160 Sec. 135 — Transfer Tax base

**Verification subagent findings:**
- Rule confirmed across CGT, DST, CWT, VAT, Transfer Tax by PwC PH, Respicio & Co., ForeclosurePhilippines.com, Ocampo & Suralvo Law, Forvis Mazars PH, Grant Thornton PH
- No source contradicts the three-way max outcome
- Structural nuance confirmed: legally it's two nested comparisons (SP vs. FMV_6E; FMV_6E = max(ZV, AFMV)) but computationally equivalent to three-way max
- Transfer Tax: RA 7160 Sec. 135 technically reads "SP or FMV if consideration is not substantial" but BIR and practitioners universally apply three-way max
- BIR Ruling OT-028-2024 confirms installment sale tax base fixed at time of sale

**Verdict: CONFIRMED — no conflicts between sources**

---

## Legal Citations

| Citation | Relevance |
|---|---|
| NIRC Section 24(D)(1) as amended by RA 10963 (TRAIN) | CGT base for individual sellers |
| NIRC Section 27(D)(5) | CGT base for corporate sellers |
| NIRC Section 6(E) | FMV definition: higher of zonal vs. assessor |
| NIRC Section 196 | DST on conveyance base |
| NIRC Section 57; RR 2-98 Sec. 2.57.2(J) as amended by RR 11-2018 | CWT base |
| NIRC Section 106; RR 16-2005 Sec. 4.106-4 | VAT base |
| RA 7160 Section 135 | Transfer Tax base |
| RA 12001 (RPVARA, June 2024) | Future: collapses three-way to two-way |
| BIR Ruling OT-028-2024 | Installment sale timing: tax base fixed at sale date |

---

## Automation Implications

**Complexity assessment:** Low formula complexity, high data-dependency complexity.

The formula itself (`max(a, b, c)`) is trivial. The hard problem is populating the three inputs:

| Component | Automation Feasibility | Key Barrier |
|---|---|---|
| Gross Selling Price | Trivial (user input) | None |
| Assessor FMV | Moderate (OCR/upload Tax Declaration) | Non-standardized Tax Declaration formats |
| BIR Zonal Value | Hard | No API; 127 heterogeneous Excel workbooks; OCR edge cases; 38% of schedules outdated |

**Once built, this engine unlocks all five transaction taxes simultaneously** — a single input resolution pipeline feeds CGT, DST, CWT, VAT, and Transfer Tax calculations. This makes it a high-leverage infrastructure component.

**Competitive landscape:** No current PH tax software (JuanTax, Taxumo, QNE) automates the zonal value lookup from real address inputs. Users must look up zonal values manually and enter them. This is the core automation gap.
