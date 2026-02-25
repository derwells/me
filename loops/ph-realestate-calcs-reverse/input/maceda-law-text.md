# Maceda Law (RA 6552) — Source Extraction

**Source:** Republic Act No. 6552, "Realty Installment Buyer Protection Act"
**Approved:** August 26, 1972
**Named after:** Senator Ernesto Maceda
**Primary sources:**
- Full text: https://lawphil.net/statutes/repacts/ra1972/ra_6552_1972.html
- SC E-Library: https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/1688
- DHSUD FAQs: https://dhsud.gov.ph/maceda-law-ra-6552-legal-faqs/

---

## Coverage (Section 2)

Applies to **all transactions or contracts involving the sale or financing of real estate on installment payments**, including residential condominium apartments.

**Excluded:**
- Industrial lots
- Commercial buildings
- Sales to tenants under RA 3844 (agrarian reform), as amended by RA 6389

**Practical exclusion:** When a buyer uses bank financing, the developer receives full payment upfront from the bank. Maceda Law does not apply to the bank-buyer relationship (that is governed by separate banking/mortgage law). The law applies only to direct developer-to-buyer installment arrangements.

---

## Section 3: Buyer with AT LEAST 2 Years of Installments

### 3(a) — Grace Period Right

> "one month grace period for every one year of installment payments made"

- **Trigger:** Buyer in default who has paid ≥ 2 years of installments
- **Formula:** Grace months = years of installments paid (integer, rounded down)
- **Frequency limit:** May be exercised **once every 5 years** of contract life
- **Cost:** No additional interest during grace period

**Examples:**
- 3 years paid → 3 months grace
- 7 years paid → 7 months grace
- 12 years paid → 12 months grace

### 3(b) — Cash Surrender Value (CSV) Upon Cancellation

> "the seller shall refund to the buyer the cash surrender value of the payments on the property equivalent to fifty per cent (50%) of the total payments made and, after five years of installments, an additional five per cent (5%) every year but not to exceed ninety per cent (90%) of the total payments made"

**Formula:**
```
if years_paid <= 5:
    CSV_pct = 50%
else:
    CSV_pct = min(50% + (years_paid - 5) × 5%, 90%)

CSV = Total_Payments_Made × CSV_pct
```

**Lookup table:**

| Years of Installments Paid | CSV % of Total Payments |
|---|---|
| 2 | 50% |
| 3 | 50% |
| 4 | 50% |
| 5 | 50% |
| 6 | 55% |
| 7 | 60% |
| 8 | 65% |
| 9 | 70% |
| 10 | 75% |
| 11 | 80% |
| 12 | 85% |
| 13+ | 90% (maximum) |

### 3(b) — Cancellation Procedure

Cancellation is effective only **after both conditions are met**:
1. 30 days from buyer's receipt of **notarized notice of cancellation** (or notarial demand for rescission)
2. **Full payment of CSV** to the buyer

Both conditions are mandatory (Active Realty v. Daroya ruling). A cancellation without notarized notice and/or without CSV payment is **invalid** — the contract continues to subsist.

---

## Section 4: Buyer with LESS THAN 2 Years of Installments

> "the seller shall give the buyer a grace period of not less than sixty days from the date the installment became due"

- **Grace period:** Minimum 60 days from due date
- **Refund:** None mandated by law
- **Cancellation:** 30 days after written notice to buyer

---

## Section 5: Right to Sell, Assign, or Reinstate

Buyer may:
1. **Sell/assign** their rights under the contract to another person (by notarial act)
2. **Reinstate** the contract by updating the account during the grace period and **before actual cancellation**

---

## Section 6: Right to Pay in Advance

Buyer may pay any installment or the **full unpaid balance at any time without interest**. Full payment must be annotated on the certificate of title.

---

## Section 7: Non-Waiver

Any contract stipulation contrary to Sections 3, 4, 5, or 6 is **null and void**.

---

## "Total Payments Made" — Definition

**Included:**
- Down payments
- Deposits
- Options on the contract
- Monthly amortization installments

> Section 3 text: "Down payments, deposits or options on the contract shall be included in the computation of the total number of installment payments made."

**Excluded (per practitioner consensus and HLURB decisions):**
- Interest charges
- Penalty charges
- Administrative fees
- Notarial charges (if not part of the installment payment)

**Contested:** Whether delinquency charges and penalties paid as part of periodic payments are included in "total payments." Majority view: exclude penalties; compute on principal installments only.

---

## "Years of Installments" — Counting Method

- Counted by **number of monthly installments paid**, not calendar months elapsed
- 24 monthly payments = 2 years of installments (regardless of time span)
- Partial years: the law uses whole years ("5 years of installments"); fractional years beyond 5 do **not** trigger the additional 5% increment
- E.g., 5 years and 8 months paid → CSV still 50% (not 55%); 6 full years → 55%

**Note:** Some practitioners argue partial years count pro-rata, but the statutory text ("every year") implies whole-year counting. This is an unresolved ambiguity.

---

## Key Supreme Court Rulings

### Rillo v. Court of Appeals (G.R. No. 125347, June 19, 1997)

**Facts:** Buyer defaulted on condominium installments; had paid less than 2 years. Developer cancelled contract.
**Ruling:** Section 4 (< 2 years) applies. No refund due. Confirmed Maceda Law governs installment sales (not Civil Code rescission provisions).
**Key point:** CA's order to refund 50% of ₱158,184 was deleted — no refund when < 2 years paid.

### Active Realty and Development Corp. v. Daroya (G.R. No. 141205, 382 SCRA 152 [2002])

**Facts:** Buyer paid 4 years on residential lot, missed 3 payments. Developer cancelled without notarized notice and without paying CSV; then resold the property.
**Ruling:** Cancellation **invalid**. Both conditions (notarized notice + CSV payment) are mandatory and concurrent. Contract subsisted; buyer entitled to either:
- Delivery of lot upon payment of outstanding balance, OR
- Refund equal to actual value of resold lot (₱875,000) + 12% p.a. interest, OR
- Substitute lot of equal value

**Key precedent:** Sets the two mandatory conditions for valid cancellation. Developer cannot self-help cancel without fulfilling CSV obligation.

---

## Computation Complexity Assessment (for Wave 2)

**Inputs required:**
1. `total_payments_made` (₱) — sum of all qualifying payments
2. `years_of_installments_paid` (integer) — count of full years of monthly installments
3. `contract_type` — to determine coverage (residential vs. excluded types)
4. `financing_mode` — direct vs. bank-financed (bank-financed: law does not apply to buyer-bank relationship)

**Outputs:**
1. `coverage_determination` — covered/not covered
2. `section_applicable` — Section 3 (≥2 years) or Section 4 (<2 years)
3. `grace_period_months` — months buyer has to cure default
4. `csv_percentage` — % of total payments refundable
5. `cash_surrender_value` (₱) — actual refund amount
6. `cancellation_procedure_checklist` — notarized notice + CSV payment sequencing

**Branching rules:**
- Coverage check (residential/condo vs. excluded)
- Financing mode check (direct vs. bank)
- 2-year threshold test
- CSV lookup by years (table with 13 rows, max cap at 90%)
- Grace period once-every-5-years constraint (requires contract history)

**Data dependencies:**
- Payment history records
- Contract start date and terms
- Current market value (if seeking alternative remedy per Daroya precedent)

**Verdict:** Fully deterministic given complete payment records. Medium complexity (branching + lookup table). Legal knowledge required for coverage determination.
