# VAT on Real Property Sales — Computation Extraction

**Wave:** 2 — Computation Extraction
**Date:** 2026-02-25
**Verification status:** CONFIRMED (with corrections noted)
**Deterministic:** YES — once asset classification and seller registration status are resolved as inputs

---

## Overview

12% output VAT applies to sales of real property classified as **ordinary assets** by **VAT-registered sellers**, subject to specific exemptions. The computation follows a multi-gate decision tree before arriving at a deterministic formula.

**Primary legal basis:**
- NIRC Section 106 — VAT on sale of goods or properties
- NIRC Section 109 — Exempt transactions (residential dwelling threshold)
- RR 16-2005 as amended — VAT implementing regulations (Section 4.106-4 for real property base)
- RR 1-2024 — Adjusted VAT-exempt threshold for residential dwellings (effective Jan 1, 2024)
- RMC 99-2023 — BIR clarification on taxes on ordinary asset real property sales

---

## Decision Tree

The full computation requires passing through 4 gates before the formula applies.

### Gate 1: Asset Classification
```
Is the real property a capital asset or ordinary asset?
  → Capital asset:  Subject to 6% CGT (Form 1706); NOT subject to VAT → STOP
  → Ordinary asset: Continue to Gate 2
```
*Note: Asset classification is NON-DETERMINISTIC (see bir-revenue-regulations.md, RR 7-2003). It is a prerequisite INPUT to this computation, not part of the computation itself.*

### Gate 2: VAT Registration Status
```
Is the seller VAT-registered?
  → Yes (annual gross sales > ₱3,000,000 OR voluntary registrant): Continue to Gate 3
  → No (annual gross sales ≤ ₱3,000,000, non-registrant): Subject to 3% Percentage Tax
                                                              under Section 116, NOT VAT → STOP
```
**Threshold (post-TRAIN, RA 10963):** ₱3,000,000 mandatory registration threshold
*(Pre-TRAIN: ~₱1,919,500 CPI-adjusted)*

**Important nuance:** A VAT-registered seller must charge 12% VAT even on sales that would fall below the registration threshold. VAT registration is irrevocable unless BIR grants cancellation.

### Gate 3: Exemption Check
```
Does an exemption apply?
  → Socialized housing (RA 7279): VAT-EXEMPT → STOP
  → Residential dwelling (house & lot / residential unit) with selling price ≤ ₱3,600,000:
      VAT-EXEMPT under Section 109 as adjusted by RR 1-2024 → STOP
  → Bare residential lot: NO SEPARATE EXEMPTION (exemption eliminated Jan 1, 2021)
  → None of the above: Continue to computation
```

**Residential dwelling threshold history:**
| Period | Threshold | Basis |
|--------|-----------|-------|
| Pre-TRAIN (original NIRC) | ₱2,000,000 nominal | NIRC Sec. 109 |
| Post-TRAIN pre-2021 | CPI-adjusted | TRAIN (RA 10963) |
| Jan 1, 2021 – Dec 31, 2023 | ₱3,199,200 | RR 8-2021 |
| Jan 1, 2024 – present | **₱3,600,000** | **RR 1-2024** |

**Bare residential lot (important correction):**
- Pre-2021: separate ₱1,500,000 nominal threshold (≈₱1,919,500 CPI-adjusted pre-TRAIN)
- **Effective January 1, 2021: bare residential lot VAT exemption ELIMINATED under TRAIN Law**
- No separate exemption threshold for bare lots currently exists
- Sale of bare residential lot by VAT-registered seller → subject to 12% VAT (no floor)

**Socialized housing exemption (NIRC Sec. 109(P)):**
- Must qualify as socialized housing per RA 7279 (Urban Development and Housing Act)
- Primarily applies to developer sales to qualified beneficiaries, not open-market sales
- BIR periodically issues administrative determinations on qualification

### Gate 4: Tax Base Determination
```
tax_base = max(gross_selling_price, FMV)
  where:
  FMV = max(BIR_zonal_value, assessor_schedule_of_market_values)

∴ tax_base = max(gross_selling_price, max(BIR_zonal_value, assessor_FMV))
```

This is the same "highest of three" comparison used for CGT, DST, CWT.

**Legal basis:** RR 16-2005, Section 4.106-4:
> "In the case of sale of real property subject to VAT, the gross selling price shall mean the consideration stated in the sales document or the fair market value, whichever is higher."

---

## VAT Formula

Once all gates are passed:

```
Output VAT = tax_base × 12%
```

**VAT-exclusive (price stated without VAT):**
```
Output VAT = consideration × 12%
```

**VAT-inclusive (price stated inclusive of VAT):**
```
Net = GSP ÷ 1.12
Output VAT = GSP − Net = GSP × (12/112)
```

---

## Installment Sale VAT Recognition

### The 25% Initial Payment Test (RMC 99-2023)

The timing of VAT recognition depends on the **initial payment as % of gross selling price**:

**Defined:** "Initial payments" = down payment + all principal amortization payments received during the year of sale (NOT including interest; interest is separately VATable)

**Scenario A — Installment Plan (initial payments ≤ 25% of GSP):**
- Output VAT recognized **per installment/collection received**
- Each collection = proportional VAT recognition
- Seller issues **VAT Official Receipts** on each installment
- Full **Sales Invoice** for total contract price issued only upon full payment and deed execution
- Buyer claims input VAT in the same period seller recognizes output VAT

**Scenario B — Deferred-Payment / Cash Basis (initial payments > 25% of GSP):**
- Treated as a **cash sale** for VAT purposes
- Full output VAT recognized in the **month of sale** on entire selling price
- Subsequent payments do not trigger additional VAT
- Input VAT accrues to buyer at time of sale

| Initial Payment | VAT Recognition | Document Issued |
|----------------|-----------------|-----------------|
| > 25% of GSP | Full VAT in month of sale | Sales Invoice (full amount) |
| ≤ 25% of GSP | Per collection received | VAT OR per installment; Sales Invoice on full payment |

---

## Invoicing Requirements (Post-EOPT Act)

- Under the Ease of Paying Taxes (EOPT) Act and BIR implementing rules, the document that creates input VAT for the buyer is the **Sales Invoice** (not Official Receipt)
- For installment sales: VAT Official Receipts are issued per collection during the installment period
- Final Sales Invoice for total contract price issued upon final payment/deed execution
- This is a substantive compliance requirement — wrong document type can invalidate input VAT claims

---

## Edge Cases

### 1. Deemed Sale on Donation
- If a VAT-registered person **donates** real property classified as an ordinary asset → treated as "deemed sale" under Section 106(B)
- Subject to 12% VAT based on FMV at time of donation
- Confirmed by RMC 99-2023 (explicitly addressed)

### 2. Banks and Foreclosed Properties
- Foreclosed real properties held by banks = ordinary assets for VAT purposes
- Sale of foreclosed property by VAT-registered bank → subject to 12% VAT
- Consistent with bank ordinary asset treatment under RR 7-2003
- Confirmed by RMC 99-2023

### 3. Non-Real Estate Business Selling Incidental Property
- If seller's registered business is NOT real estate but sells a business-use property (ordinary asset):
  - VAT applies the same way (ordinary asset + VAT-registered = 12% VAT)
  - ITR treatment differs: gain reported as "other taxable income," not gross sales
  - VAT invoicing and payment same as real estate developer

### 4. Partial Socialized Housing
- Mixed development (part socialized, part open market) requires allocation
- Socialized portion = VAT-exempt; open market portion = 12% VAT
- Allocation typically by floor area or unit count per BIR approved schedule

### 5. Input VAT on Capital Goods
- Capital goods ≥ ₱1,000,000: input VAT amortized over useful life or 60 months, whichever is shorter
- This affects the developer's VAT reconciliation schedule (not buyer computation)
- Relevant for Wave 2 `installment-vat-schedule` aspect

---

## Worked Examples

### Example 1 — Developer Selling Condo Unit (Above Threshold)
- Seller: VAT-registered real estate developer
- Property: Condominium unit, ordinary asset
- Selling price: ₱5,500,000 (above ₱3.6M threshold)
- BIR zonal value: ₱4,800,000
- Assessor FMV: ₱5,200,000
- Tax base: max(₱5,500,000, max(₱4,800,000, ₱5,200,000)) = **₱5,500,000**
- Output VAT = ₱5,500,000 × 12% = **₱660,000**
- Price to buyer (VAT-exclusive contract): ₱5,500,000 + ₱660,000 = ₱6,160,000

### Example 2 — Developer Selling Below Threshold (VAT-Exempt)
- Selling price: ₱3,200,000
- BIR zonal value: ₱3,100,000
- → Selling price ≤ ₱3,600,000 → **VAT-EXEMPT**
- Developer still subject to DST (1.5%) and CWT by buyer (1.5–5%)

### Example 3 — Non-VAT Registered Individual Selling Condo (Ordinary Asset)
- Seller: Individual, NOT VAT-registered, annual gross sales < ₱3,000,000
- Property: Condo, ordinary asset (used in business)
- → **3% Percentage Tax** applies, NOT 12% VAT
- → Buyer still withholds CWT (1.5–6% per habitually-engaged status)

### Example 4 — Installment Plan (₱10M Unit, 10% Down)
- Contract price: ₱10,000,000 (VAT-exclusive)
- Down payment year 1: ₱1,000,000 (10% of GSP < 25%) → **Installment plan**
- Monthly amortization: ₱150,000 for 60 months
- VAT per payment:
  - Down payment: ₱1,000,000 × 12% = ₱120,000
  - Monthly OR: ₱150,000 × 12% = ₱18,000
- Seller issues VAT OR for each payment; Sales Invoice for full ₱10M on final payment

---

## Legal Citations

| Item | Legal Basis |
|------|------------|
| 12% VAT rate on ordinary asset real property | NIRC Section 106 |
| VAT-exempt: capital assets | NIRC Section 109(B) |
| VAT-exempt: socialized housing | NIRC Section 109(P) |
| VAT-exempt: residential dwelling ≤ ₱3,600,000 | NIRC Section 109 + RR 1-2024 |
| VAT registration threshold ₱3,000,000 | NIRC Section 236(G) as amended by TRAIN (RA 10963) |
| Tax base = max(consideration, FMV) | RR 16-2005, Section 4.106-4 |
| FMV = higher of zonal value and assessor's schedule | RR 16-2005 (implementing NIRC Section 6(E)) |
| Installment VAT recognition per collection | NIRC Section 106 + RMC 99-2023 |
| Deferred payment = full VAT at sale (25% test) | RMC 99-2023 |
| Deemed sale on donation | NIRC Section 106(B)(4) |
| 3% percentage tax for non-VAT registered sellers | NIRC Section 116 |

---

## Inputs and Outputs (Mini-Spec)

### Inputs
| Input | Type | Source |
|-------|------|--------|
| `asset_classification` | enum: capital / ordinary | Non-deterministic prerequisite (RR 7-2003) |
| `seller_vat_registered` | boolean | BIR registration records |
| `property_type` | enum: house_and_lot / condo / bare_lot / commercial / socialized | Deed / assessor records |
| `gross_selling_price` | ₱ decimal | Deed of Sale |
| `bir_zonal_value` | ₱ decimal | BIR zonal value schedule (RDO lookup) |
| `assessor_fmv` | ₱ decimal | Tax Declaration / assessor's office |
| `payment_structure` | enum: cash / deferred / installment | Contract |
| `initial_payments_year_1` | ₱ decimal | Payment schedule |
| `vat_inclusive` | boolean | Contract |
| `qualifies_socialized` | boolean | BIR determination |

### Outputs
| Output | Type | Description |
|--------|------|-------------|
| `vat_applies` | boolean | True if all gates pass |
| `vat_exempt_reason` | string or null | Capital asset / below threshold / socialized housing / non-VAT seller |
| `tax_base` | ₱ decimal | max(GSP, max(zonal, assessor)) |
| `output_vat_total` | ₱ decimal | tax_base × 12% |
| `recognition_method` | enum: full_at_sale / per_collection | Based on 25% test |
| `vat_per_installment` | array of {date, amount, vat} | If per_collection |

---

## Verification Status

| Claim | Status | Source |
|-------|--------|--------|
| 12% VAT rate | Confirmed | NIRC Section 106; multiple practitioner sources |
| Decision tree (asset → registration → exemption → formula) | Confirmed | RMC 99-2023; PwC PH; BDB Law |
| Residential dwelling threshold = ₱3,600,000 | Confirmed | RR 1-2024 (effective Jan 1, 2024) — **corrected from ₱3,199,200** |
| Bare residential lot exemption eliminated | Confirmed | TRAIN Law; MTF Counsel; CREBA commentary |
| VAT registration threshold = ₱3,000,000 | Confirmed | NIRC Section 236(G); Respicio & Co. |
| 3% percentage tax for non-VAT sellers | Confirmed | NIRC Section 116; Ocampo & Suralvo (Dec 2023) |
| Tax base formula | Confirmed | RR 16-2005 Sec 4.106-4; RMC 99-2023 |
| Installment VAT per collection (25% test) | Confirmed | RMC 99-2023; PwC Tax Alert 28; Grant Thornton |
| Deemed sale on donation | Confirmed | RMC 99-2023 (explicitly addressed) |

---

## Determinism Assessment

**Deterministic: YES** — once the prerequisite inputs are resolved.

The computation itself (after Gates 1–3) is fully deterministic:
- Formula is fixed (12%, tax base = max of three values)
- Thresholds are published by BIR (₱3,600,000 per RR 1-2024)
- 25% installment test is arithmetic

**Non-deterministic prerequisites (excluded from scoring):**
1. `asset_classification` — capital vs. ordinary asset requires judgment (RR 7-2003)
2. `qualifies_socialized` — socialized housing qualification requires BIR determination
3. `bir_zonal_value` — requires external lookup table (addressed in `zonal-value-lookup` aspect)

---

## Key Automation Complexity Drivers

1. **Residential threshold CPI adjustment** — threshold changes every ~3 years; must track RR issuances
2. **Bare lot vs. house-and-lot distinction** — different VAT treatment; requires property classification
3. **25% installment test** — requires payment schedule modeling across time periods
4. **VAT-inclusive vs. VAT-exclusive** — contract review required to determine basis
5. **Invoicing compliance** — Sales Invoice vs. VAT OR distinction; EOPT Act changes
6. **Zonal value lookup** — external data dependency (see `zonal-value-lookup` aspect)
7. **RPVARA transition** — RA 12001 may collapse zonal/assessor distinction once implemented

---

## Sources

**Primary:**
- NIRC (RA 8424 as amended by RA 10963 / TRAIN): Sections 106, 109, 236(G)
- RR 16-2005 (VAT implementing regulations), Section 4.106-4
- RR 1-2024 (VAT-exempt threshold adjustment, effective Jan 1, 2024)
- RMC 99-2023 (BIR clarification on taxes on ordinary asset real property sales)

**Verification sources:**
- Grant Thornton PH — VAT-exempt threshold increased to P3.6M (2024 alert)
- Grant Thornton PH — BIR guide on real estate transactions classified as ordinary assets
- PwC PH — Tax Alert No. 28 on RMC 99-2023
- BDB Law — Taxation of Sale of Real Properties
- Ocampo & Suralvo — BIR Clarifies Taxes on Ordinary Asset Sale (Dec 2023)
- MTF Counsel — VAT Exempt Threshold on Sale of Real Properties
- CREBA — VAT exemption ceiling raised to P3.6M; BIR Amends VAT Exemption Rule
- BusinessWorld — Taxes on the sale of real property (Sep 2024)
- Philippine News Agency — BIR hikes VAT exemption to P3.6M
