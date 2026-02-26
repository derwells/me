# CWT Rate and Timing — Creditable Withholding Tax on Ordinary Asset Real Property Sales

## Verification Status: CONFIRMED (with nuances documented)
## Deterministic: YES (once seller classification is resolved as a precondition)
## Date: 2026-02-25

---

## Overview

CWT on ordinary asset real property sales is the mechanism by which the buyer withholds a portion of the purchase price and remits it to the BIR on behalf of the seller. It operates as an income tax prepayment creditable against the seller's annual income tax liability.

**Legal basis:**
- NIRC Section 57 (authority to require withholding)
- RR 2-98 Section 2.57.2(J) as amended by RR 6-2001, RR 17-2003, RR 11-2018
- RMO 33-2023 (reiteration of installment withholding rules)
- RMC 31-2025 (April 2025 — updated compliance rules)
- BIR Ruling OT-028-2024 (clarification on installment CWT base)

**Applies to:** Sale of real property classified as **ordinary assets only**.
Capital assets → 6% CGT (Form 1706, final tax, no CWT).

---

## Inputs

| Input | Type | Source |
|---|---|---|
| `seller_habitually_engaged` | Boolean | HLURB/HUDCC registration OR 6+ transactions in prior year |
| `gross_selling_price` | ₱ amount | Deed of sale / contract |
| `zonal_value` | ₱ amount | BIR zonal value schedule (RDO lookup) |
| `assessor_fmv` | ₱ amount | LGU assessor's schedule of market values |
| `initial_payments_year_of_sale` | ₱ amount | All payments received in year of sale (see definition) |
| `buyer_in_trade_or_business` | Boolean | Buyer's registration / business status |
| `mortgage_assumed_by_buyer` | ₱ amount | Mortgage balance transferred to buyer, if any |
| `seller_adjusted_basis` | ₱ amount | Seller's cost basis in property (for mortgage exclusion rule) |

---

## Formula / Decision Tree

### Step 1: Confirm Ordinary Asset Status
CWT applies ONLY if property is an ordinary asset of the seller. Capital assets → exit; apply CGT at 6%.

### Step 2: Determine Tax Base

```
fmv_sec6e = max(zonal_value, assessor_fmv)
tax_base = max(gross_selling_price, fmv_sec6e)
```

This is the "highest of three" base applied identically to CGT, DST (Sec. 196), and VAT.

For installment sales specifically: FMV is determined at the **time of execution of the Contract to Sell**, not at each subsequent collection date (BIR Ruling OT-028-2024).

### Step 3: Determine CWT Rate

**Branch A — Seller habitually engaged in real estate:**
```
if tax_base <= 500_000:      rate = 1.5%
elif tax_base <= 2_000_000:  rate = 3.0%
else:                        rate = 5.0%
```

**Branch B — Seller NOT habitually engaged:**
```
rate = 6.0%
```

**Special case — Socialized housing (RA 7279 HLURB-accredited):**
```
rate = 0%  (exempt)
```

**"Habitually engaged" determination (precondition, not deterministic):**
- CONFIRMED: HLURB or HUDCC registration as dealer/developer → conclusive; OR
- CONFIRMED: At least **6 taxable real estate transactions** in the preceding calendar year
  - **NUANCE (ForeclosurePhilippines):** The 6 transactions may combine both purchase and sale transactions — not exclusively sales. 3 purchases + 3 sales = 6 qualifies.
- CONFIRMED: Banks selling foreclosed properties → always **NOT habitually engaged** → 6% rate (RR 7-2003)

### Step 4: Compute CWT Amount

```
cwt_amount = tax_base × rate
```

### Step 5: Determine Withholding Timing (Installment Sales)

**Step 5a: Compute initial payments**

```
initial_payments = all_payments_received_in_year_of_sale - excluded_mortgage
```

Where `excluded_mortgage`:
- CONFIRMED with precision: Exclude mortgage assumed by buyer, **BUT ONLY UP TO** the seller's adjusted cost/basis
- **NUANCE:** If assumed mortgage > seller's adjusted basis, the excess is INCLUDED in initial payments
- Also exclude: promissory notes or evidence of indebtedness issued by buyer (primary extraction omitted this)

**Step 5b: 25% threshold test**

```
initial_payment_ratio = initial_payments / gross_selling_price
```

**If `initial_payment_ratio > 25%` (cash sale / deferred payment basis):**
- Full CWT withheld and remitted on/before the **first installment payment**
- All tax due upfront at first collection

**If `initial_payment_ratio ≤ 25%` (installment method):**
```
if buyer_in_trade_or_business:
    timing = "withhold on each installment proportionally"
else:
    timing = "withhold on the LAST installment"
```

---

## Filing and Remittance

| Item | Detail |
|---|---|
| Form | BIR Form 1606 (Withholding Tax Remittance Return for Onerous Transfer of Real Property Other Than Capital Asset) |
| Filed by | Buyer (withholding agent) |
| Filed at | Authorized Agent Bank (AAB) at the RDO having jurisdiction over the **location of the property** |
| Deadline | Within **10 days** following the end of the month in which the transaction / installment payment occurred |
| December exception | Taxes withheld in December → deadline is **January 15** of the following year |

---

## Seller's Tax Credit — MATERIAL CONFLICT / UPDATE

**Primary extraction stated:** Form 2307 (Certificate of Creditable Tax Withheld) issued to seller quarterly.

**Verification finding — CONFIRMED CONFLICT:** As of RMC 99-2023 and definitively per **RMC 31-2025 (April 2025)**:
- Form 2307 has been **discontinued** as the credit instrument for ordinary asset real property CWT
- The seller's evidence of income tax credit is now the **BIR Form 1606 itself** (with proof of payment / bank stamp)
- The seller attaches the Form 1606 (paid copy) to their ITR to claim the CWT as a creditable tax
- Sources: AJA Law analysis of RMC 31-2025; PwC Philippines Tax Alert No. 28 (2023); Ocampo & Suralvo on BIR Ruling OT-028-2024

> **Flag for automation:** Any CWT computation engine must use Form 1606 (not Form 2307) as the output document for the seller's credit. Prior to RMC 31-2025, Form 2307 was issued; after April 2025, Form 1606 is the sole instrument.

---

## Edge Cases

| Scenario | Treatment |
|---|---|
| Capital asset sold by individual | No CWT; CGT at 6% via Form 1706 |
| Capital asset sold by corporation (not used in business) | No CWT; CGT at 6% via Form 1706 |
| Bank selling foreclosed property | Ordinary asset; CWT at 6% (never "habitually engaged") |
| Socialized housing (RA 7279) | CWT at 0% (exempt) |
| Seller switching from real estate to non-real estate business | Properties remain ordinary assets; CWT still applies |
| Inherited property, heir NOT in real estate business | Capital asset; no CWT; CGT applies |
| Property not used in business for 2+ consecutive years prior to sale | Converts to capital asset; no CWT |
| Initial payment > 25% | Full CWT on first installment |
| Initial payment ≤ 25%, individual buyer | CWT withheld at last installment |
| Initial payment ≤ 25%, corporate/business buyer | CWT withheld on each installment |
| Assumed mortgage | Excluded from initial payments (up to seller's basis); excess over basis included |
| Promissory note from buyer | Excluded from initial payments |

---

## Worked Examples

### Example 1: Habitually Engaged Seller, Cash Sale, ₱3.5M property

```
gross_selling_price = ₱3,500,000
zonal_value = ₱4,000,000
assessor_fmv = ₱2,800,000
seller_habitually_engaged = True

tax_base = max(3_500_000, max(4_000_000, 2_800_000)) = max(3_500_000, 4_000_000) = ₱4,000,000
rate = 5.0%  (tax_base > ₱2,000,000, habitually engaged)
cwt_amount = ₱4,000,000 × 5% = ₱200,000
timing = cash sale → withhold at closing / first payment
```

### Example 2: Not Habitually Engaged, Installment Sale ≤ 25%, Individual Buyer

```
gross_selling_price = ₱2,000,000
initial_payments = ₱300,000  (15% of SP)
seller_habitually_engaged = False
buyer_in_trade_or_business = False

tax_base = ₱2,000,000  (assuming SP is highest)
rate = 6.0%
cwt_amount = ₱2,000,000 × 6% = ₱120,000
timing = initial_payment_ratio = 15% ≤ 25%, buyer NOT in trade/business
         → withhold full ₱120,000 on LAST installment
```

### Example 3: Habitually Engaged, Installment ≤ 25%, Corporate Buyer

```
gross_selling_price = ₱5,000,000
initial_payments = ₱1,000,000  (20% of SP)
seller_habitually_engaged = True
buyer_in_trade_or_business = True  (corporate buyer)

tax_base = ₱5,000,000
rate = 5.0%
cwt_amount = ₱5,000,000 × 5% = ₱250,000
timing = initial_payment_ratio = 20% ≤ 25%, buyer in trade/business
         → withhold proportionally on each installment payment
```

---

## Legal Citations

| Provision | Citation |
|---|---|
| General withholding authority | NIRC Section 57 |
| CWT on ordinary asset real property (rates) | RR 2-98 Sec. 2.57.2(J) as amended by RR 6-2001, RR 11-2018 |
| Installment CWT timing (25% rule) | RR 17-2003 Sec. 3.J; reiterated by RMO 33-2023 |
| Asset classification (ordinary vs. capital) | RR 7-2003 |
| Bank/foreclosure special rule | RR 7-2003; RR 2-98 |
| FMV definition (zonal vs. assessed) | NIRC Section 6(E) |
| Installment sale base — time of CTS | BIR Ruling OT-028-2024 |
| Form 1606 as sole credit instrument | RMC 31-2025; RMC 99-2023 |

---

## Verification Summary

**Verified against:** ForeclosurePhilippines.com, BDB Law, Grant Thornton PH (installment sales article), BDB Law November 2023 Insights (RMO 33-2023), PwC PH Tax Alert No. 28 (2023), AJA Law (RMC 31-2025 analysis), Ocampo & Suralvo (BIR Ruling OT-028-2024), Tax and Accounting Center, BusinessWorld (Sept 2024), NTRC RMO 33-2023 Digest.

**Confirmed:** Rate table, thresholds (₱500K/₱2M), habitually engaged criteria, bank special rule, 25% installment timing bifurcation, Form 1606, 10-day deadline, December exception.

**Nuances added from verification:**
1. "6 transactions" may combine purchases and sales (not exclusively sales)
2. Mortgage exclusion is conditional — excess over seller's basis is included in initial payments
3. Promissory notes from buyer also excluded from initial payments
4. December exception (January 15 deadline) documented
5. **Material update:** Form 2307 discontinued per RMC 31-2025; Form 1606 is now the seller's credit instrument

**Unresolved:** CREBA-accreditation grandfathering clause (one-source mention only; not confirmed by cross-reference).
