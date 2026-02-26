# Installment VAT Schedule — Output VAT Recognition Per Collection

**Wave:** 2 — Computation Extraction
**Date:** 2026-02-25
**Verification status:** CONFIRMED (with corrections and nuances documented; EOPT invoicing change flagged)
**Deterministic:** YES — given payment schedule as input; formula is fully deterministic per collection period

---

## Overview

When a VAT-registered real estate dealer sells an ordinary asset on an installment plan (initial payments in year of sale ≤ 25% of gross selling price), **output VAT is recognized and remitted per collection received**, not all at once at the time of sale. This aspect covers the full computation of the installment VAT schedule: the gateway test, per-collection formula, recognition timing, and form reporting.

**Primary legal basis:**
- NIRC Section 106 — VAT on sale of goods or properties
- RR 16-2005 as amended by RR 4-2007, Section 4.106-3 — Installment plan rule
- RMC 99-2023 (October 3, 2023) — BIR clarification on taxes on ordinary asset real property sales
- RMC 05-2023 — Quarterly VAT filing (abolished mandatory monthly 2550M)
- RMC 52-2023 — Optional monthly 2550M
- RMC 11-2024 — Reiterates installment sale rules in context of lease-to-conditional-sale

---

## Gate: Installment Plan vs. Deferred Payment Classification

Before computing per-collection VAT, the classification must be resolved:

```
initial_payments_year_of_sale / gross_selling_price ≤ 25%?
  → YES: INSTALLMENT PLAN — VAT recognized per collection
  → NO:  DEFERRED PAYMENT — treated as cash sale; full VAT due in month of sale
```

**Definition of "initial payments" (RR 16-2005 / RR 4-2007):**
- All payments received by seller **before or upon execution** of the instrument of sale
- Plus all payments expected or scheduled to be received **in the same calendar year** of sale
- In cash or property (excluding evidence of indebtedness, i.e., notes/promissory notes)

**Exclusions from initial payments:**
1. **Interest payments** — excluded from the 25% test (but VATable when received; see below)
2. **Assumed mortgage** — the amount of any mortgage assumed by the buyer is excluded from initial payments, **EXCEPT** when the assumed mortgage exceeds the seller's cost/basis in the property, in which case the excess IS included in initial payments

| Included in initial payment test | Excluded from initial payment test |
|---|---|
| Down payment | Interest on unpaid balance |
| Monthly amortizations paid in year of sale | Assumed mortgage ≤ seller's cost/basis |
| Balloon payments in year of sale | Buyer's promissory notes |
| Reservation fees if non-refundable | |

**Legal basis:** RR 16-2005 Section 4.106-3; RR 4-2007 (definitional amendments); confirmed by RMC 99-2023.

---

## Per-Collection VAT Formula

### Scenario A: Contract Price ≥ FMV (Zonal/Assessed Value)

The simple proportional formula applies when the agreed consideration is at least as high as the FMV:

```
Output_VAT_per_collection = collection_received × 12%
```

Where `collection_received` = principal + interest + late payment penalties received in the period.

**Example A:** Contract price ₱5,500,000 (zonal value ₱4,800,000). Monthly installment ₱120,000.
- Output VAT per month = ₱120,000 × 12% = **₱14,400**

### Scenario B: FMV > Contract Price (Zonal Value Exceeds Agreed Consideration)

When the tax base is the FMV (because FMV > contract price), the output VAT per installment is computed using the FMV-ratio formula:

```
VAT_base_total = FMV_tax_base × 12%  (total output VAT for the full sale)

Output_VAT_per_collection = (collection_received / contract_price) × FMV_tax_base × 12%
```

Where:
- `FMV_tax_base` = max(zonal_value, assessor_FMV) — the higher FMV value
- `contract_price` = agreed consideration (excluding VAT)
- `collection_received` = amount actually received in the period (principal + interest + penalties)

**Example B (from RR 4-2007):**
- Contract price: ₱1,000,000
- Zonal value: ₱1,500,000 (FMV > contract price)
- Monthly installment: ₱10,000
- Output VAT per month = (₱10,000 / ₱1,000,000) × ₱1,500,000 × 12% = ₱0.01 × ₱1,500,000 × 12% = **₱1,800**
- Effective rate on collection: 18% (because the VAT base exceeds the cash collected)

**Why Scenario B occurs so frequently:** BIR zonal values in prime areas of Metro Manila, Cebu, and Davao typically exceed developer contract prices for socialized and affordable housing units sold in early project stages. Any time the contract-price-to-zonal-value ratio is less than 1, Scenario B applies.

---

## Treatment of Interest and Penalties

**Interest payments received:** Subject to 12% VAT when received, included in the collection-period total.

**Late payment penalties/surcharges:** Subject to 12% VAT when received (RR 16-2005, Section 4.106-3 explicit language: "including interest and penalties").

**Note on interest vs. principal in the formula:** For purposes of the ratio formula (Scenario B), the ratio (collection / contract_price) uses the total collection received (inclusive of interest and penalties), not just the principal portion. Interest is not stripped out before applying the formula.

**Income tax treatment of interest:** Interest income is separately declared as ordinary income under the ITR (not capital gain). This is distinct from the VAT treatment.

---

## Deferred Payment / Cash Sale Treatment (>25%)

When initial payments exceed 25% of GSP:
1. **Full output VAT** is due in the **month of sale** on the **entire tax base**
2. Tax base = max(contract_price, FMV_tax_base) as usual
3. Full VAT = tax_base × 12%
4. Subsequent collections do **not** generate additional VAT
5. Buyer claims full input VAT at time of sale (not per collection)
6. Seller declares full output VAT on the 2550Q for the quarter of sale

---

## VAT Form Filing and Remittance Timeline

### Current regime (effective January 1, 2023):

**Mandatory:** BIR Form 2550Q (Quarterly VAT Return)
- Due: **25 days after the close of the taxable quarter** when the collection occurred
- The taxable quarter follows the taxpayer's income tax accounting period (calendar or fiscal)
- Covers all collections received during the quarter

**Optional:** BIR Form 2550M (Monthly VAT Declaration)
- Available for first two monthly periods of the quarter (months 1 and 2)
- **No prescribed deadline** for optional 2550M filing (per RMC 52-2023)
- Non-filing of 2550M does not create a BIR open case if 2550Q is timely filed
- Filing 2550M does not eliminate the obligation to file 2550Q

### Pre-2023 regime (for reference):
- Monthly 2550M was mandatory: due 20th day of following month (electronic filers)
- Quarterly 2550Q: due 25th day following close of quarter

| Period | Form | Mandatory | Deadline |
|---|---|---|---|
| Each calendar quarter (2023+) | 2550Q | YES | 25 days after quarter-end |
| First two months of quarter (2023+) | 2550M | NO (optional) | No prescribed deadline |

---

## Buyer's Input VAT Claim Timing

**Rule:** Buyer can claim input VAT in the **same period** the seller recognized the output VAT.

- Installment plan: buyer claims input VAT **per collection period** (same quarter as seller's output)
- Deferred/cash sale: buyer claims full input VAT in the **quarter of sale**
- Buyer's input VAT documentation: the invoice/receipt issued by the seller per collection

**Legal basis:** RR 16-2005 Section 4.106-3; reiterated by RMC 11-2024.

---

## Invoicing Requirements

### Pre-EOPT Framework (before January 22, 2024)
- During installment period: **VAT Official Receipt (OR)** issued per collection
- Upon full payment + Deed of Absolute Sale executed: **principal VAT Sales Invoice** for full contract price

### Post-EOPT Framework (EOPT Act / RA 11976, effective January 22, 2024; RR 7-2024, effective April 27, 2024)

**CRITICAL CHANGE:** RA 11976 restructured the entire invoice/receipt regime:
- **Invoice** (formerly Sales Invoice or Service Invoice) → now primary VAT document for ALL transactions
- **Official Receipt** → reclassified as supplementary document only (proof of payment, not VAT document)
- ORs issued after December 31, 2024 must be stamped: *"THIS DOCUMENT IS NOT VALID FOR CLAIM OF INPUT TAX"*

**Practical impact on installment real property sales:**
- The per-collection document that supports the buyer's input VAT claim must now be a **VAT Invoice**, not an OR
- BIR has **not yet issued** a specific circular updating the installment property invoicing protocol under EOPT (as of Q1 2026)
- Emerging practitioner consensus: issue a **partial VAT Invoice** per collection covering the installment amount, rather than the pre-EOPT practice of issuing ORs
- The full/final VAT Invoice for the entire contract price is issued upon deed execution (retained from pre-EOPT practice)

**⚠ Flag for automation:** Any engine handling installment VAT schedule should track the EOPT transition date and apply the correct invoicing rules by transaction date. Transactions post-April 27, 2024 operate under the new RR 7-2024 framework.

---

## Payment Schedule Tracking Model

The installment VAT schedule requires tracking a running payment schedule across multiple accounting periods:

### Required Inputs Per Schedule:
| Input | Type | Description |
|---|---|---|
| `contract_price` | ₱ decimal | Agreed consideration (ex-VAT) |
| `fmv_tax_base` | ₱ decimal | max(zonal_value, assessor_FMV) |
| `year_of_sale` | int | Calendar year sale was made |
| `initial_payments_year_0` | ₱ decimal | Payments in year of sale (principal only) |
| `payment_schedule` | array of {date, principal, interest, penalty} | Full amortization schedule |
| `asset_classification` | enum: ordinary | Must be ordinary (pre-condition) |
| `seller_vat_registered` | boolean | Must be true (pre-condition) |

### Per-Collection Record:
| Field | Type | Description |
|---|---|---|
| `collection_date` | date | When payment was received |
| `principal_collected` | ₱ decimal | Principal portion |
| `interest_collected` | ₱ decimal | Interest portion |
| `penalty_collected` | ₱ decimal | Late fees/surcharges |
| `total_collected` | ₱ decimal | Sum of above |
| `output_vat` | ₱ decimal | Computed per formula (A or B) |
| `reporting_quarter` | string | e.g., "Q1-2025" |
| `invoice_number` | string | Reference to VAT Invoice issued |

### Computed Schedule Outputs:
| Output | Description |
|---|---|
| `recognition_method` | `installment` or `cash_sale` (based on 25% test) |
| `total_vat_base` | max(contract_price, fmv_tax_base) |
| `total_output_vat_lifetime` | total_vat_base × 12% |
| `quarterly_vat_summary` | {quarter: Q, collections: ₱X, output_vat: ₱Y}[] |
| `cumulative_vat_recognized` | Running total across all quarters |
| `remaining_vat_balance` | total_output_vat_lifetime − cumulative_vat_recognized |

---

## Edge Cases

### 1. Accelerated/Prepayment
If a buyer on installment plan pays off the full balance early, all remaining output VAT is recognized in the period of full payment. No retroactive reclassification to deferred/cash sale treatment — the classification was established at the time of sale based on year-of-sale initial payments.

### 2. Default / Cancellation of Contract to Sell
If the contract is cancelled (buyer defaults, seller rescissions), previously recognized output VAT may be claimed as VAT credit or refund through the appropriate BIR process. The seller reverses the uncollected installments; output VAT on uncollected amounts is not due. Detailed BIR procedure requires a VAT Credit/Refund application.

### 3. Mid-Sale Reclassification
**BIR position: UNVERIFIED.** There is no published BIR ruling specifically addressing a scenario where the classification changes mid-sale (e.g., buyer pays extra in year 2 that would have exceeded 25% if made in year 1). The general principle is that classification is fixed at year of sale based on initial payments in that year. No retroactive reclassification applies.

### 4. Constructive Receipt
Output VAT is triggered on payments "actually AND/OR constructively received." Constructive receipt occurs when the payment is available to the seller (e.g., credited to seller's bank account, offset against seller's receivable, available in escrow). Post-dated checks: recognized upon actual encashment or maturity date, whichever is earlier.

### 5. Mortgage Assumption Exceeding Seller's Basis
When the assumed mortgage > seller's cost/basis, the excess is counted as an initial payment for the 25% test. This can unexpectedly push a transaction from installment to deferred/cash sale treatment. This nuance requires knowledge of the seller's tax basis (cost) in the property.

### 6. VAT on Penalty Charges
Late payment penalties and surcharges charged to the buyer are subject to 12% VAT when collected. These are included in `penalty_collected` in the per-collection record and generate additional output VAT beyond the amortization schedule.

---

## Mini-Spec Summary

### Full Inputs
| Input | Type | Source |
|---|---|---|
| `contract_price` | ₱ decimal | Contract to Sell |
| `fmv_tax_base` | ₱ decimal | BIR zonal value / assessor records (max) |
| `initial_payments_year_0` | ₱ decimal | Payment schedule, year of sale only, principal only |
| `assumed_mortgage` | ₱ decimal | Deed of Sale / financing terms |
| `seller_cost_basis` | ₱ decimal | Seller's books (for mortgage excess test) |
| `payment_schedule` | array | {date, principal, interest, penalty} |
| `transaction_date` | date | For EOPT regime determination |

### Computation Steps
1. Compute adjusted initial payments:
   - `adj_initial_payments = initial_payments_year_0`
   - If `assumed_mortgage > seller_cost_basis`: `adj_initial_payments += (assumed_mortgage − seller_cost_basis)`
2. Test: `adj_initial_payments / contract_price ≤ 25%?`
   - YES → installment plan; NO → cash sale (proceed to Step 6)
3. Determine formula scenario:
   - If `contract_price ≥ fmv_tax_base`: use Scenario A (simple × 12%)
   - If `fmv_tax_base > contract_price`: use Scenario B (ratio × fmv_tax_base × 12%)
4. For each collection in payment schedule:
   - `total_collected = principal + interest + penalty`
   - Scenario A: `output_vat = total_collected × 12%`
   - Scenario B: `output_vat = (total_collected / contract_price) × fmv_tax_base × 12%`
   - Assign to reporting quarter
5. Aggregate by quarter for 2550Q reporting
6. Cash sale path: `output_vat = fmv_tax_base × 12%` due in month/quarter of sale; subsequent collections → no VAT

### Outputs
| Output | Type |
|---|---|
| `recognition_method` | enum: installment / cash_sale |
| `quarterly_schedule` | array: {quarter, output_vat, cumulative_vat} |
| `total_output_vat_lifetime` | ₱ decimal |
| `invoicing_regime` | enum: pre_eopt / post_eopt |

---

## Verification Status

| Claim | Status | Source(s) |
|---|---|---|
| 25% threshold test (installment vs. cash/deferred) | CONFIRMED | RMC 99-2023; RR 16-2005 Sec. 4.106-3; RMC 11-2024; Grant Thornton; Forvis Mazars; PwC |
| Initial payments exclude interest | CONFIRMED | RR 4-2007; RR 16-2005; Respicio |
| Initial payments exclude assumed mortgage (with excess exception) | CONFIRMED WITH NUANCE | RR 4-2007; Ocampo & Suralvo BIR Ruling OT-028-2024 |
| Simple per-collection formula (collection × 12%) | CONFIRMED (when contract price ≥ FMV) | RR 16-2005; RMC 99-2023 |
| FMV-ratio formula when zonal > contract price | CONFIRMED | RR 4-2007 worked example; philtax.blogspot.com RR 4-2007 text |
| Interest VATable at 12% per collection | CONFIRMED | RR 16-2005 Sec. 4.106-3 ("including interest and penalties"); Grant Thornton; RMC 99-2023 |
| Penalties/surcharges VATable at 12% per collection | CONFIRMED | RR 16-2005 Sec. 4.106-3 explicit language |
| Buyer claims input VAT in same period as seller's output | CONFIRMED | RR 16-2005 Sec. 4.106-3; RMC 11-2024 |
| Mandatory quarterly 2550Q (abolished monthly 2550M) | CONFIRMED | RMC 05-2023; PwC Tax Alert 4; KPMG |
| Optional monthly 2550M (no prescribed deadline) | CONFIRMED | RMC 52-2023; Forvis Mazars; Grant Thornton; Ocampo & Suralvo |
| Pre-EOPT: OR per collection, Sales Invoice at deed | CONFIRMED | Respicio; RMC 99-2023 |
| Post-EOPT: OR reclassified as supplementary document | CONFIRMED | RA 11976; RR 7-2024; KPMG; BDB Law |
| Mid-sale installment-to-deferred reclassification | UNVERIFIED (no BIR ruling found) | — |

---

## Legal Citations

| Item | Legal Basis |
|---|---|
| 25% installment test | NIRC Section 49 (installment method); RR 16-2005 Sec. 4.106-3 |
| Initial payment definition (incl. mortgage exclusion) | RR 4-2007 (amending RR 16-2005 Sec. 4.106-3) |
| Per-collection VAT recognition | NIRC Section 106; RR 16-2005 Sec. 4.106-3 |
| FMV-ratio formula for zonal > contract | RR 4-2007 Section 4.106-3 worked example |
| Interest and penalty VAT treatment | RR 16-2005 Sec. 4.106-3 ("including interest and penalties") |
| Buyer input VAT timing | RR 16-2005 Sec. 4.106-3; RMC 11-2024 |
| Cash sale / deferred treatment | RR 16-2005 Sec. 4.106-3 |
| Quarterly 2550Q filing | RMC 05-2023 (NIRC Sec. 114(A) as amended by TRAIN) |
| Optional 2550M filing | RMC 52-2023 |
| Invoicing (pre-EOPT) | RMC 99-2023; NIRC Section 237 |
| Invoicing (post-EOPT) | RA 11976 (EOPT Act); RR 7-2024 |

---

## Key Automation Complexity Drivers

1. **Dual formula paths** — Simple vs. FMV-ratio formula depending on contract price vs. zonal value; requires zonal value data
2. **Initial payment test** — Must aggregate all year-of-sale collections (principal only, excluding interest) and apply the mortgage-excess exception
3. **Multi-period tracking** — Schedule spans 2–30+ years; must map each collection to a reporting quarter
4. **Interest and penalty tracking** — Contract-level interest schedule + late payment surcharges must be tracked separately then included in VAT base
5. **Quarterly 2550Q aggregation** — Collections must be bucketed by BIR taxable quarter (not calendar month)
6. **EOPT invoicing regime** — Transaction date determines which invoicing rules apply; transition management required
7. **Constructive receipt** — Post-dated check encashment, escrow releases, and credit offsets all trigger VAT; requires event tracking
8. **Cancellation/default handling** — Output VAT reversal logic on contract cancellations
9. **Zonal value at date of sale** — The zonal value applicable is the one at the date of sale, not at each collection date; must snapshot the zonal value at contract signing

---

## Sources

**Primary:**
- NIRC (RA 8424 as amended by TRAIN): Section 106 (VAT on properties), Section 49 (installment method)
- RR 16-2005, Section 4.106-3 (VAT implementing regulations — installment plan rule)
- RR 4-2007 (amendment to RR 16-2005, with worked example on FMV-ratio formula)
- RMC 99-2023 (October 3, 2023) — BIR clarification on ordinary asset real property taxes
- RMC 05-2023 (January 13, 2023) — Abolished mandatory monthly 2550M
- RMC 52-2023 (May 2023) — Optional monthly 2550M
- RMC 11-2024 — Reiteration of installment sale rules (lease-to-conditional-sale context)
- RA 11976 (EOPT Act) — Restructured invoice vs. OR framework (effective January 22, 2024)
- RR 7-2024 — EOPT implementing regulations (effective April 27, 2024)

**Verification sources:**
- PwC PH Tax Alert No. 28 — RMC 99-2023 summary
- PwC PH Tax Alert No. 4 — RMC 05-2023 summary
- Grant Thornton PH — Taxes on Sale of Real Property; Reiteration of Withholding Taxes on Installment Sales
- Forvis Mazars PH — RMC 99-2023, RMC 05-2023, RMC 52-2023 alerts
- KPMG PH — "2550-M No More?" (February 2023); InTAX July 2024 (RR 7-2024)
- Ocampo & Suralvo — RMC 52-2023; BIR Ruling OT-028-2024 (installment sale CWT/DST basis)
- BDB Law — Taxation of Sale of Real Properties; Invoicing under EOPT
- Respicio & Co. — When to Issue Sales Invoices for Installment Sale
- philtax.blogspot.com — RR 16-2005 text; RR 4-2007 text
- BusinessWorld — Taxes on the sale of real property (September 2024)
- BIR Official — RMC No. 99-2023 PDF (bir-cdn.bir.gov.ph)
