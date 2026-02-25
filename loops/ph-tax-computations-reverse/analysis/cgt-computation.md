# CGT Computation — Capital Gains Tax on Real Property Sale

**Wave:** 2 — Computation Extraction
**Date:** 2026-02-25
**Verification status:** CONFIRMED (core) / CONFLICT documented (partial exemption formula, penalty rates)
**Deterministic:** YES — once capital asset classification is established and all inputs are resolved

---

## Overview

Capital Gains Tax (CGT) on real property is a final tax imposed on the *presumed gain* from the sale, exchange, or other disposition of Philippine-situs real property classified as a **capital asset**. It does NOT apply to ordinary assets (those use CWT and VAT instead). The CGT computation itself is fully deterministic — it requires no professional judgment once the prerequisite classification is resolved.

**Legal basis:**
- NIRC Section 24(D)(1) — individuals, estates, trusts
- NIRC Section 27(D)(5) — domestic corporations (non-business real property)
- NIRC Section 24(D)(2) — principal residence exemption
- RR 13-99 — implementing rules for principal residence exemption
- RA 11976 (EOPT Act, January 22, 2024) — revised penalty rates for micro/small taxpayers

---

## Prerequisite: Capital Asset Classification (NON-DETERMINISTIC)

CGT only applies if the property is a **capital asset**. This determination is made under RR 7-2003 and is non-deterministic (requires facts-and-circumstances judgment).

**Capital asset** = real property NOT:
- Held for sale to customers in the ordinary course of trade/business
- Used in trade/business of the taxpayer (subject to depreciation)
- Held primarily for sale or for lease

All other real properties = capital assets → CGT applies.

> The CGT *computation* module receives `is_capital_asset = True` as a pre-resolved input. The classification determination is a separate (non-deterministic) upstream gate.

---

## Inputs

| Input | Type | Source | Notes |
|---|---|---|---|
| `gross_selling_price` | decimal | Deed of absolute sale | Total consideration; include non-cash components at FMV |
| `zonal_value_per_sqm` | decimal | BIR RDO zonal schedule | Per Sec 6(E); lookup by RDO zone → property type → location |
| `area_sqm` | decimal | Tax Declaration / Title | Land area and/or floor area as applicable |
| `assessed_fmv` | decimal | LGU Tax Declaration | FMV column (NOT assessed value); from latest Tax Declaration |
| `sale_date` | date | Deed notarization date | Triggers 30-day filing deadline |
| `is_principal_residence` | boolean | Seller declaration | Must be actual primary dwelling |
| `proceeds_reinvested` | decimal | Proof of acquisition | Amount used to acquire/construct new principal residence |
| `reinvestment_within_18mo` | boolean | Derived from dates | Measured from `sale_date` |
| `bir_notified_within_30days` | boolean | Sworn declaration file date | Filed at RDO where property is located |
| `last_exemption_date` | date or null | BIR records | Must be 10+ years before `sale_date` |
| `assumed_mortgage` | decimal | Loan documents | Existing mortgage assumed by buyer; included in GSP |
| `taxpayer_size` | enum | Annual gross sales | micro (<₱3M), small (₱3M–₱20M), medium (₱20M–₱1B), large (>₱1B) |

---

## Core Formula

### Step 1: Determine Tax Base

```
zonal_value = zonal_value_per_sqm × area_sqm
fmv_6e = max(zonal_value, assessed_fmv)          # Section 6(E) FMV
tax_base = max(gross_selling_price, fmv_6e)       # Statutory formulation
         = max(gross_selling_price, zonal_value, assessed_fmv)  # Operationally equivalent
```

> Note: `gross_selling_price` includes any assumed mortgage (`gross_selling_price = cash + assumed_mortgage`).

### Step 2: Check Principal Residence Exemption

All five conditions must be met for any exemption to apply:
1. Property is seller's principal residence (primary dwelling)
2. BIR notified via sworn declaration within 30 days of sale
3. Proceeds reinvested within 18 calendar months of sale date
4. Exemption not availed within the past 10 years
5. If `gross_selling_price > ₱5,000,000`: proceeds placed in escrow with authorized agent bank until reinvestment is proven (RR 13-99, Section 4)

**Full exemption** (all conditions met, proceeds fully reinvested):
```
cgt = 0
```

**Partial exemption** (conditions met but proceeds only partially reinvested):
```
# Per RR 13-99 Section 4 method (correct when zonal/assessed value may exceed GSP):
unutilized_ratio = (gross_selling_price - proceeds_reinvested) / gross_selling_price
taxable_base = unutilized_ratio × tax_base      # Uses max(SP, ZV, AFMV) as base
cgt = 0.06 × taxable_base
```

> **FORMULA CONFLICT NOTE:** An alternative (incorrect) formulation circulates:
> `cgt = 0.06 × tax_base × (1 - proceeds_reinvested / gross_selling_price)`
> This is algebraically identical to the RR 13-99 method ONLY when `tax_base = gross_selling_price`. When zonal value or assessed FMV is highest (common in practice), the RR 13-99 formula produces a higher taxable base and higher tax. Use the RR 13-99 formulation.

### Step 3: Standard CGT Computation

No exemption applies:
```
cgt = 0.06 × tax_base
```

### Step 4: Compute Filing Deadline

```
filing_deadline = sale_date + 30 calendar days
```

The taxable event is the date of **notarization** of the Deed of Absolute Sale (or public instrument), not the date of payment, possession transfer, or registration.

---

## Penalty Computation (Late Filing/Payment)

### Standard Taxpayers (medium/large: gross sales > ₱20M)

| Penalty | Rate | Notes |
|---|---|---|
| Surcharge | 25% of tax due | For late/negligent filing |
| Surcharge | 50% of tax due | For willful neglect or fraudulent return |
| Interest | 12% per annum | From filing deadline to payment date; double BSP legal rate per NIRC Sec 249 as amended by TRAIN |
| Compromise penalty | Per BIR schedule | Up to ₱25,000/year per failure |

### Micro/Small Taxpayers (RA 11976 EOPT Act, effective January 22, 2024)

| Taxpayer Size | Annual Gross Sales | Surcharge | Interest | Compromise Penalty Cap |
|---|---|---|---|---|
| Micro | < ₱3,000,000 | 10% | 6% p.a. | ₱12,500/year |
| Small | ₱3M – ₱20M | 10% | 6% p.a. | ₱12,500/year |
| Medium/Large | > ₱20M | 25% | 12% p.a. | ₱25,000/year |

> For 50% fraudulent return surcharge: applies to all taxpayer sizes regardless of EOPT tiers.

**Interest computation:**
```
days_late = payment_date - filing_deadline
interest = tax_due × annual_rate × (days_late / 365)
total_due = tax_due + surcharge + interest + compromise_penalty
```

---

## Special Rules and Edge Cases

### 1. Sale to Government — Election Option

When a **capital asset** is sold to the national government or any of its political subdivisions/agencies, the individual seller may **elect** between:
- **Section 24(D):** 6% CGT on gross tax base (no deductions allowed)
- **Section 24(A):** Graduated ordinary income tax on net gain (cost and selling expenses deductible)

This election is a statutory exception — for all other sales, CGT is mandatory and no election exists.

### 2. Installment Sales of Capital Assets

When a capital asset is sold on installment (initial payments in year of sale ≤ 25% of total selling price):

**Option A — Full upfront CGT payment:**
- Pay 100% of CGT within 30 days of deed notarization
- BIR issues eCAR immediately
- Seller bears financing cost of early tax payment

**Option B — Proportional installment CGT:**
- File a separate BIR Form 1706 within 30 days of **each collection**
- Each return covers the proportional CGT on that installment
- eCAR issued only after full CGT is paid

> The 25% initial payment test for installment eligibility mirrors the income tax installment method (NIRC Sec 49) but the CGT timing rule is separate.

**Assumed mortgage and constructive down payment:**
```
initial_payments = down_payment + all_collections_in_year_of_sale
constructive_down_payment = max(0, assumed_mortgage - seller_cost_basis)
initial_payments_for_25pct_test = initial_payments + constructive_down_payment
installment_eligible = (initial_payments_for_25pct_test / gross_selling_price) <= 0.25
```

### 3. Non-Resident Sellers

Non-resident alien individuals and foreign entities selling Philippine real property are subject to the same 6% CGT regime. Some bilateral tax treaties may provide relief, but most PH tax treaties do not override the final withholding tax on real property gains. Tax treaty eligibility is a separate determination.

### 4. Pacto de Retro and Conditional Sales

Section 24(D) explicitly covers:
- *Pacto de retro* sales (sale with retained right of repurchase)
- Other forms of conditional sales

CGT is triggered at execution of the instrument, not at expiry of the redemption period. If the right of repurchase is subsequently exercised, BIR rulings govern the treatment of the CGT already paid.

### 5. Foreclosure Sales

When a mortgaged property is sold via foreclosure:
- The **mortgagor** (original property owner/borrower) remains the CGT taxpayer
- Tax base: bid price at foreclosure sale or FMV per Sec 6(E), whichever is higher
- Mortgagor must file Form 1706 within 30 days of the foreclosure sale date

### 6. Inherited Property

- Estate tax (not CGT) applies at succession/death
- When the **heir subsequently sells** the inherited property: full 6% CGT applies
- No step-up in basis, no exemption by reason of inheritance alone
- The heir's cost basis for any ordinary income tax calculations = FMV at date of inheritance (for estate tax purposes)

### 7. Non-Cash and Mixed Consideration

If the consideration includes non-cash property (e.g., property exchange, assumption of obligations):
- Non-cash components valued at FMV for tax base purposes
- `gross_selling_price = cash_received + FMV_of_non_cash_received + liabilities_assumed_by_buyer`

### 8. Partial Interest Transfers

Sale of a fractional undivided interest or grant of an easement:
- CGT computed on FMV of the interest conveyed, not the full property value
- `tax_base = max(GSP_for_partial_interest, fractional_share × full_property_FMV)`

### 9. Principal Residence Exemption — Additional Procedural Requirements (RR 13-99)

Beyond the 5 conditions listed above:
- **Cost basis carry-over:** The historical cost of the old principal residence carries over as the cost basis of the new one. No separate computation in CGT, but a documentation requirement with downstream tax consequences.
- **Escrow mechanism (GSP > ₱5M):** The full CGT is paid and placed in escrow with an authorized agent bank. BIR releases the escrow amount back to the seller upon proof of reinvestment. Any unutilized amount is released to BIR.
- **Oath/sworn declaration format:** Filed at the RDO where the property is located, typically accompanied by Form 1706 showing ₱0 tax due.

---

## Worked Examples

### Example A — Standard Sale (Zonal Value Highest)

- Gross selling price: ₱4,000,000
- Zonal value: ₱4,800,000 (800 sqm × ₱6,000/sqm)
- Assessed FMV: ₱3,500,000
- Deed notarized: March 15, 2025

```
tax_base = max(4,000,000; 4,800,000; 3,500,000) = ₱4,800,000
cgt = 6% × 4,800,000 = ₱288,000
filing_deadline = April 14, 2025
```

### Example B — Principal Residence, Partial Reinvestment

- Gross selling price: ₱6,000,000
- BIR zonal value: ₱7,000,000
- Assessed FMV: ₱5,500,000
- Proceeds reinvested: ₱4,200,000
- All other exemption conditions met

```
tax_base = max(6,000,000; 7,000,000; 5,500,000) = ₱7,000,000
unutilized_ratio = (6,000,000 - 4,200,000) / 6,000,000 = 0.30
taxable_base = 0.30 × 7,000,000 = ₱2,100,000
cgt = 6% × 2,100,000 = ₱126,000
```

Note: Escrow required since GSP > ₱5M.

### Example C — Corporate Seller (Non-Business Capital Asset)

- Domestic corporation selling idle land (not used in business)
- Selling price: ₱20,000,000
- Zonal value: ₱18,000,000; Assessed FMV: ₱15,000,000

```
Legal basis: NIRC Section 27(D)(5) — same 6% rate and "highest of" base
tax_base = max(20,000,000; 18,000,000; 15,000,000) = ₱20,000,000
cgt = 6% × 20,000,000 = ₱1,200,000
```

### Example D — Late Payment Penalty (Micro Taxpayer, EOPT)

- CGT due: ₱60,000
- Filing deadline: March 30, 2025
- Payment made: June 28, 2025 (89 days late)
- Taxpayer gross annual sales: ₱2,500,000 (micro taxpayer)

```
surcharge = 10% × 60,000 = ₱6,000      # Reduced rate under EOPT
interest = 60,000 × 6% × (89/365) = ₱879.45
total_due = 60,000 + 6,000 + 879.45 ≈ ₱66,879
```

Same scenario for medium/large taxpayer:
```
surcharge = 25% × 60,000 = ₱15,000
interest = 60,000 × 12% × (89/365) = ₱1,758.90
total_due = 60,000 + 15,000 + 1,758.90 ≈ ₱76,759
```

---

## BIR Form 1706 — Filing Summary

| Item | Details |
|---|---|
| Form | BIR Form 1706 — Final Capital Gains Tax Return |
| Filed by | Seller (or buyer on behalf of seller in some cases) |
| Filing venue | Authorized Agent Bank (AAB) at RDO where property is located; eFPS; or per EOPT, at any BIR office |
| Deadline | Within 30 days of sale/disposition (date of notarization) |
| Attachment | Deed of Sale, Tax Declaration, Zonal Value certification, BIR Form 2317 (if installment) |
| eCAR trigger | eCAR issued by BIR after confirming full CGT payment; required before Register of Deeds processes title transfer |

---

## eCAR Process Gate

The eCAR (Electronic Certificate Authorizing Registration) is issued by the BIR as proof of tax clearance on the transaction. It is required before:
- Register of Deeds processes Deed of Sale for title transfer
- Transfer of title to buyer

eCAR is issued only after:
1. Full CGT payment (or approved exemption) — Form 1706
2. Full DST payment — Form 2000-OT
3. BIR verifies all payments and supporting documents
4. eCAR jurisdiction: the RDO where the property is located (per RMC 56-2024)

---

## Verification Status

**Primary sources:** NIRC Sections 24(D), 27(D)(5), 24(D)(2), 6(E); RR 13-99; RA 11976 (EOPT 2024)

**Secondary source verification (subagent, 2026-02-25):**

| Element | Status | Sources |
|---|---|---|
| 6% CGT rate | Confirmed | Respicio & Co., PwC Tax Summaries, Tax & Accounting Center PH |
| Tax base: max of 3 values | Confirmed | All sources; proposed 10% hike was withdrawn April 2025 |
| 30-day filing deadline | Confirmed | All sources; triggered by notarization date |
| 25% / 50% surcharge | Confirmed | With EOPT tier nuance |
| 12% interest | Confirmed | Standard rate; 6% for micro/small per EOPT |
| Principal residence: 5 conditions | Confirmed | Escrow (>₱5M) and cost basis carry-over added from RR 13-99 |
| Partial exemption formula | Conflict | RR 13-99 method diverges from alternative formula when ZV/AFMV > GSP; RR 13-99 method used above |
| Sale to government election | Confirmed | Sec 24(A) vs Sec 24(D) |
| eCAR gate | Confirmed | |
| Installment CGT regime | Added | Not in original extraction; two-option regime documented |
| EOPT 2024 penalty tiers | Added | RA 11976 material; applicable to most individual sellers |

**Sources consulted:**
- [Respicio & Co. — CGT Computation and Legal Basis](https://www.respicio.ph/commentaries/capital-gains-tax-on-real-property-sales-proper-computation-and-legal-basis-philippines)
- [Respicio & Co. — CGT Rates and Deadlines](https://www.respicio.ph/commentaries/capital-gains-tax-on-sale-of-real-property-in-the-philippines-rates-deadlines-and-who-pays)
- [Respicio & Co. — Installment Sale CGT](https://www.respicio.ph/commentaries/determining-capital-gains-tax-liability-in-real-estate-installment-sales)
- [PwC Philippines — Tax Summaries](https://taxsummaries.pwc.com/philippines/individual/taxes-on-personal-income)
- [Tax and Accounting Center Philippines — CGT Overview](https://taxacctgcenter.ph/overview-of-capital-gains-tax-in-the-philippines/)
- [PwC Philippines — EOPT Act Alert](https://www.pwc.com/ph/en/tax/tax-alerts/2024/pwc-ph-ease-of-paying-taxes-2024.pdf)
- [Grant Thornton Philippines — EOPT Comparative Summary](https://www.grantthornton.com.ph/contentassets/2208a706d6c743e0a9a6c4f6d89d81b1/eopt-act-comparative-summary.pdf)
- [Siguion Reyna — EOPT Act Salient Features](https://srmo-law.com/legal-updates/salient-features-of-the-republic-act-no-11976-or-the-ease-of-paying-taxes-act/)

---

## Automation Assessment Notes (for Wave 4)

**Deterministic subcomputations (fully automatable):**
1. Tax base = max(SP, ZV×area, AFMV) — pure comparison, once ZV is resolved
2. CGT = 6% × tax_base — single multiplication
3. Deadline = sale_date + 30 days — date arithmetic
4. Penalty computation — tiered arithmetic once taxpayer size and days_late are known
5. Partial exemption formula — arithmetic once all inputs provided

**Key data dependencies (automation blockers):**
- Zonal value lookup: no BIR API, 127+ heterogeneous Excel workbooks per RDO (covered in `zonal-value-lookup` aspect)
- Assessed FMV: requires Tax Declaration document processing (LGU-issued; inconsistent format)
- Taxpayer size determination: requires knowledge of seller's annual gross sales (internal data)
- Capital asset classification: non-deterministic prerequisite (RR 7-2003 judgment)

**Branching rules count:**
- Standard/partial/full exemption: 3 branches
- Sale to government election: 2 branches
- Installment vs. cash sale: 2 branches (then 2 sub-branches for Option A/B)
- Taxpayer size for penalties: 4 tiers
- Total material branches: ~11

**Complexity estimate:** Medium-high. The formula is simple; the complexity lies in (1) zonal value lookup, (2) Tax Declaration processing, (3) installment logic, and (4) EOPT penalty tiering. A working CGT calculator requires the zonal value database as a prerequisite.
