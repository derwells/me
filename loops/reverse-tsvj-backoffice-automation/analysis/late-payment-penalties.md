# Late Payment Penalty Computation — Process Analysis & Feature Spec

## Process Description

**What:** Computing penalty charges (interest/surcharges) on overdue rent and other charges for tenants who fail to pay by the due date. Two distinct regimes: residential controlled units (penalty-capped) and commercial units (contractual, subject to judicial review).

**When:** Assessed each billing cycle (monthly). Penalty accrues from the day after the due date and continues until the unpaid balance is settled. Penalty charges appear as separate line items on the next billing statement.

**Who:** Currently done manually by the property manager. The manager checks which tenants are overdue, looks up the applicable penalty rate (contract or default), and computes the penalty amount. No systematic automation in Crispina.

**Frequency:** Monthly per tenant with overdue balances. With ~20-100 units, potentially 5-30 penalty computations per month (assuming 20-30% delinquency rate common in PH rental operations).

---

## Current Method

**Manual / spreadsheet.** The property manager:
1. Reviews payment records against due dates each month
2. Identifies tenants with outstanding balances past the grace period
3. Looks up the penalty rate from the lease contract (if stipulated)
4. Computes penalty amount: `unpaid_balance x penalty_rate`
5. Adds penalty as additional charge on the next billing statement
6. No systematic cap enforcement for controlled units
7. No audit trail of which rate was applied and what the running penalty total is

**Pain points:** Easy to apply wrong rate, miss the residential/commercial distinction, over-charge controlled tenants (legal risk), or under-charge commercial tenants. No visibility into cumulative penalties or whether the annual cap for controlled units has been reached.

---

## Regulatory Rules

### A. Residential Controlled Units (RA 9653 Regime)

#### A.1 Does RA 9653 impose specific limits on late payment penalties?

**RA 9653 itself does not contain an explicit penalty rate provision.** The statute addresses rent payment timing (Section 7), deposit limits (Section 7), grounds for ejectment (Section 9), and rent increase caps (Section 4/6), but does not prescribe a specific late payment penalty rate or cap.

However, a composite legal framework governs penalties for controlled units:

| Source | Rule |
|--------|------|
| RA 9653 Sec. 7 | Rent due within first 5 days of each month (statutory payment window) |
| Civil Code Art. 2209 | If debtor delays, indemnity = stipulated interest; if none stipulated, legal interest applies |
| Civil Code Art. 1229 | Courts must reduce unconscionable penalties; mandatory for partial compliance |
| BSP Circular 799 (2013) | Legal interest rate = 6% per annum |
| Jurisprudence (multiple) | For residential leases, safe harbour is 1% of unpaid rent per month, total not exceeding 1 month's rent per year |

**Legal citation:** RA 9653, Section 7 (Republic Act No. 9653, July 14, 2009); Civil Code of the Philippines (RA 386), Articles 1226-1230, 2209, 2212.

**Source:** https://lawphil.net/statutes/repacts/ra2009/ra_9653_2009.html

#### A.2 Grace Period

**RA 9653 Section 7** states: *"Rent shall be paid in advance within the first five (5) days of every current month or the beginning of the lease agreement unless the contract of lease provides for a later date of payment."*

This 5-day window is the statutory payment period, not technically a "grace period" (the statute does not use that term). However, in practice:
- Rent paid within the first 5 days = timely under the statute
- Rent paid after day 5 = late, unless contract provides for a later date
- Many lease contracts add an additional contractual grace period of 3-7 days beyond the statutory window
- One appellate case (*Spouses Abella v. Abella*) criticized immediate penalty enforcement without any grace period as unconscionable

**For automation:** The system should track two dates:
1. `date_due` — per contract (default: 5th of month per RA 9653 Sec. 7)
2. `date_penalty_starts` — `date_due` + contractual grace period (if any)

#### A.3 Three Months Arrears — RA 9653 Section 9(b)

**RA 9653 Section 9** provides ejectment grounds for controlled units, including: *"Arrears in payment of rent for a total of three (3) months."*

Key rules:
- The 3 months need not be consecutive — "a total of" means cumulative
- If the lessor refuses to accept payment, the lessee may consign the amount (deposit in court, with city/municipal treasurer, barangay chairman, or bank in the lessor's name with notice)
- Lessee must deposit the rental within 10 days of each current month after consignation begins
- Failure to consign for 3 months also constitutes grounds for ejectment
- Formal demand is mandatory before filing an ejectment suit; tenant has 15 days to pay after demand before suit can be filed

**For automation:** The system should track:
- Cumulative months of arrears per tenant (not just current month)
- Alert threshold at 2 months (warning) and 3 months (ejectment-eligible)
- Whether formal demand has been issued

#### A.4 Penalty Interest on Top of Unpaid Rent for Controlled Units

**Yes, the lessor can charge penalty interest, but with constraints:**

1. **Must be in writing:** Civil Code Art. 1956 requires that any stipulation on interest must be in writing. No written penalty clause = no penalty interest.

2. **If contract specifies penalty rate:** Enforceable, subject to Art. 1229 unconscionability review.

3. **If contract is silent on penalties:** Only legal interest (6% per annum per BSP Circular 799) from the date of extrajudicial or judicial demand. The lessor cannot unilaterally impose penalty interest without contractual basis.

4. **Safe harbour for residential leases:** Based on the composite legal analysis from multiple secondary sources (Respicio & Co.), the practical safe harbour for residential controlled units is:
   - Maximum **1% of unpaid rent per month**
   - Total penalties **never exceeding 1 month's rent** for any single delay period
   - **Simple interest only** — no compounding
   - No additional surcharges (processing fees, notice fees, etc.)

**Important caveat:** The 1%/month cap and 1-month-rent ceiling are derived from legal commentary synthesizing RA 9653's protective intent with Art. 1229 unconscionability doctrine, not from an explicit statutory provision. They represent the "safe harbour" that legal practitioners advise will survive judicial review for controlled residential units. Higher rates are not prohibited per se but invite challenge.

**Source:** https://www.respicio.ph/commentaries/rent-late-fee-legality-philippines

---

### B. Civil Code Provisions on Penalty Clauses

#### B.1 Articles 1226-1230 — Penal Clauses / Liquidated Damages

**Article 1226 — Penalty as Substitute for Damages:**
> "In obligations with a penal clause, the penalty shall substitute the indemnity for damages and the payment of interests in case of noncompliance, if there is no stipulation to the contrary. Nevertheless, damages shall be paid if the obligor refuses to pay the penalty or is guilty of fraud in the fulfillment of the obligation."

Implication: If the lease has a penalty clause for late payment, the landlord collects the stipulated penalty in lieu of proving actual damages. The landlord cannot demand both actual damages AND the penalty unless the contract expressly allows it.

**Article 1227 — No Double Recovery:**
The creditor must choose between demanding performance (paying the overdue rent) and satisfaction of the penalty — not both — unless the contract clearly grants the right to both. However, if performance becomes impossible after demand, the penalty can still be enforced.

**Critical for lease penalties:** Most lease contracts stipulate that the penalty is *in addition to* the overdue rent. This is permissible under Art. 1226's "if there is no stipulation to the contrary" clause and Art. 1227's "unless this right has been clearly granted." A well-drafted penalty clause should explicitly state the penalty is additional to, not a substitute for, rent payment.

**Article 1228 — No Need to Prove Actual Damages:**
> "Proof of actual damages suffered by the creditor is not necessary in order that the penalty may be demanded."

The landlord need not prove lost rental income, opportunity cost, or other actual harm to collect the contractual penalty.

**Article 1229 — Judicial Reduction of Unconscionable Penalties:**
> "The judge shall equitably reduce the penalty when the principal obligation has been partly or irregularly complied with by the debtor. Even if there has been no performance, the penalty may also be reduced by the courts if it is iniquitous or unconscionable."

Two distinct rules:
1. **Mandatory reduction** when the tenant has partially paid (e.g., paid 2 of 3 months): the judge "shall" reduce — this is not discretionary.
2. **Discretionary reduction** when the penalty itself is unconscionable: the judge "may" reduce — even if the tenant paid nothing.

The "iniquitous or unconscionable" standard has been interpreted by Philippine courts based on:
- Proportionality to the actual harm suffered
- The type, extent, and purpose of the penalty
- The nature of the obligation and the mode of breach
- The supervening realities and socio-economic context
- The standing and relationship of the parties (*Ligutan v. CA*, G.R. No. 138677, Feb. 12, 2002)

**Article 1230 — Severability:**
Nullity of the penal clause does not affect the principal obligation (the tenant still owes rent). But nullity of the principal obligation voids the penalty.

**Source:** Civil Code of the Philippines (RA 386), Book IV, Title I, Chapter 3, Section 6. https://chanrobles.com/civilcodeofthephilippinesbook4.htm

#### B.2 Article 2209 — Legal Interest on Unpaid Obligations

> "If the obligation consists in the payment of a sum of money, and the debtor incurs in delay, the indemnity for damages, there being no stipulation to the contrary, shall be the payment of the interest agreed upon, and in the absence of stipulation, the legal interest."

Application to rent: Unpaid rent is a monetary obligation. When the tenant is in delay (past due date + demand), the lessor is entitled to:
1. The contractually stipulated interest/penalty (if any), OR
2. The legal interest rate (6% p.a. per BSP Circular 799), if no contractual stipulation exists.

**Source:** Civil Code Art. 2209; https://lawphil.net/statutes/repacts/ra1949/ra_386_1949.html

#### B.3 Article 2212 — Compound Interest (Interest on Interest)

> "Interest due shall earn legal interest from the time it is judicially demanded, although the obligation may be silent upon this point."

Application: Once accrued interest is judicially (or extrajudicially per *Nacar*) demanded, that interest itself begins earning 6% per annum. This creates compounding, but only after demand.

**Important limitation for automation:** Compounding applies only after formal demand (judicial or extrajudicial). The system should not auto-compound penalties monthly without a demand event. Pre-demand penalties accrue as simple interest.

---

### C. Legal Interest Rate Framework

#### C.1 BSP Circular No. 799, Series of 2013

**Effective date:** July 1, 2013
**Key change:** Reduced the legal interest rate from 12% to 6% per annum for:
- Loans or forbearance of money, goods, or credits (in the absence of contractual stipulation)
- Judgments involving monetary awards

**Before July 1, 2013:** 12% per annum (loans/forbearance); 6% per annum (non-loan obligations)
**From July 1, 2013 onward:** Uniform 6% per annum for all categories

#### C.2 Nacar v. Gallery Frames (G.R. No. 189871, August 13, 2013)

This Supreme Court en banc decision updated the interest rate guidelines from *Eastern Shipping Lines v. CA* (1994) to incorporate BSP Circular 799.

**Modified guidelines (the "Nacar framework"):**

| Scenario | Interest Rate | Accrual Start |
|----------|--------------|---------------|
| Monetary obligation (loan/forbearance) with written stipulation | Stipulated rate | Per contract |
| Monetary obligation (loan/forbearance) without stipulation | 6% p.a. | From default or demand |
| Non-loan obligation (damages, etc.) | 6% p.a. (discretionary) | From judicial/extrajudicial demand, or from date of judgment if amount was uncertain |
| Final and executory judgment | 6% p.a. | From finality until full satisfaction |
| Interest on interest (Art. 2212) | 6% p.a. | From judicial demand |

**Split-rate computation** (for obligations spanning the July 1, 2013 threshold):
- Up to June 30, 2013: 12% p.a.
- From July 1, 2013 onward: 6% p.a.

**Application to rent penalties:** Unpaid rent is a monetary obligation (payment of a sum of money). If the lease does not stipulate a penalty rate, the legal interest of 6% per annum applies from the date of demand.

**Legal citation:** Nacar v. Gallery Frames, G.R. No. 189871, August 13, 2013 (Supreme Court En Banc).
**Sources:**
- https://lawphil.net/judjuris/juri2013/aug2013/gr_189871_2013.html
- https://chanrobles.com/cralaw/2013augustdecisions.php?id=637

#### C.3 Current Legal Interest Rate (as of February 2026)

**6% per annum.** No subsequent BSP circular has changed the rate established by Circular 799. This rate remains in effect.

---

### D. Commercial Lease Penalties

#### D.1 Freedom of Contract (Art. 1305/1306)

**Article 1305:** "A contract is a meeting of minds between two persons whereby one binds himself, with respect to the other, to give something or to render some service."

**Article 1306:** "The contracting parties may establish such stipulations, clauses, terms and conditions as they may deem convenient, provided they are not contrary to law, morals, good customs, public order, or public policy."

Commercial leases are explicitly excluded from RA 9653 (Section 11). Penalty rates are entirely contractual, limited only by the Art. 1306 constraint (not contrary to law/morals/public policy) and the Art. 1229 unconscionability safety valve.

**Source:** Civil Code of the Philippines, Book IV; https://chanrobles.com/civilcodeofthephilippinesbook4.htm

#### D.2 No Statutory Cap on Commercial Lease Penalties

There is **no Philippine statute setting a maximum penalty rate for commercial leases**. The Usury Law (Act No. 2655) interest rate ceilings were effectively suspended by CB Circular No. 905, Series of 1982, leaving parties free to stipulate rates. However:

- Courts retain equitable power under Art. 1229 to reduce unconscionable penalties
- Rates exceeding ~3% per month (36% per annum) face heightened judicial scrutiny
- Rates exceeding ~5% per month (60% per annum) are almost certainly going to be struck down

#### D.3 Article 1229 Applicability to Commercial Penalties

The same Art. 1229 unconscionability standard applies to commercial leases. The difference is in judicial tolerance:

| Context | Likely Judicial Treatment |
|---------|--------------------------|
| Residential controlled (vulnerable tenant) | Aggressive reduction; safe harbour ~1%/month |
| Commercial (sophisticated parties) | More deference to contract; rates up to 2-3%/month generally upheld |
| Large commercial (institutional parties) | Greatest deference; but even 5%/month faces scrutiny |

#### D.4 Common Industry Practice in PH Commercial Rentals

Based on actual SEC-filed leases and government lease contracts:

| Penalty Rate | Context | Source |
|-------------|---------|--------|
| 1%/month (interest) + 1%/month (penalty) | Government leases (CPA Memorandum Circular 02-99) | elibrary.judiciary.gov.ph |
| 2%/month | Common "safe" practice in mid-market commercial leases | Industry surveys |
| 3%/month | SEC-filed commercial lease (Makati City) | sec.gov (EDGAR filing) |
| 5%/month surcharge | For accounts 60+ days past due (escalating penalty) | SEC-filed lease |
| 5% flat surcharge per late payment | PhilHealth office lease (2012) | philhealth.gov.ph |

**Most common range:** 2-3% per month of the unpaid amount, with a grace period of 5-15 days.

**Source:** https://www.sec.gov/Archives/edgar/data/1378950/000119312510055854/dex1056.htm; http://www.philhealth.gov.ph/about_us/bidsNprojects/2012/Regional/GoodsAndServices/PRO6/Office_Space/Contract.pdf

---

### E. Tax Treatment of Penalties

#### E.1 Late Payment Penalties as Taxable Income for the Lessor

**Yes.** Late payment penalties and interest charges collected from tenants are part of the lessor's **gross receipts** and are taxable as business income for a SEC-registered rental corporation. They are not treated as a separate income category — they are subsumed into rental/business income.

**Income tax:** Subject to Regular Corporate Income Tax (RCIT) at 25% or Minimum Corporate Income Tax (MCIT) at 2% of gross income, whichever is higher (for SEC-registered corporation with net taxable income above P5 million; 20% for those at or below P5 million under CREATE Act).

#### E.2 VAT Treatment

**Late payment penalties received by a VAT-registered lessor are subject to 12% VAT.**

Per RMC No. 11-2024 and RR 16-2005, for installment transactions: *"VAT shall be recognized on the installment payments, including interest and penalties, actually and/or constructively received by the seller."*

Penalty income forms part of gross receipts subject to VAT because it arises from the lease transaction (a sale of service). The penalty is not a separate supply but an ancillary charge on the primary lease service.

**For non-VAT lessors** (annual gross receipts ≤ P3 million): Penalty income is subject to **3% percentage tax** under Section 116, NIRC.

**VAT-exempt residential rental exception:** If the residential unit's monthly rent does not exceed P15,000, the lease is VAT-exempt (Section 109(1)(P), NIRC). Penalties from such leases would also be exempt from VAT but still subject to income tax.

#### E.3 Expanded Withholding Tax (EWT)

Penalty amounts collected as part of rental receipts are subject to **5% EWT** (same rate as the underlying rental income), per RR No. 02-98 Section 2.57.2(B), as amended.

The lessee/withholding agent should withhold 5% on the total amount paid, including any penalty component. In practice, many tenants do not separately withhold on penalty amounts, creating a compliance gap.

**For conditional sale (not a true lease):** Interest on installments is subject to 15% EWT as interest income from debt instruments. But for operating leases, the 5% EWT rate applies to the entire payment including penalties.

#### E.4 BIR Treatment Summary

| Tax Type | Treatment of Penalty Income | Rate | Legal Basis |
|----------|---------------------------|------|-------------|
| Income Tax (Corporate) | Part of gross business income | 25% RCIT / 20% (≤P5M) | NIRC Sec. 27 |
| VAT | Part of gross receipts from lease service | 12% (if VAT-registered) | NIRC Sec. 108; RR 16-2005 |
| Percentage Tax | Part of gross receipts (if non-VAT) | 3% | NIRC Sec. 116 |
| EWT | Withhold on total payment including penalties | 5% | RR 02-98 Sec. 2.57.2(B) |

**Source:** https://bir-cdn.bir.gov.ph/BIR/pdf/RMC%20No.%2011-2024%20Final.pdf; https://bir-cdn.bir.gov.ph/BIR/pdf/26116rr16-2005.pdf

---

### F. Jurisprudence — Unconscionable Penalty Rates

#### F.1 Medel v. Court of Appeals (G.R. No. 131622, November 27, 1998)

**Facts:** Loan of P500,000 with stipulated interest of 5.5% per month (66% per annum).

**Holding:** The Supreme Court declared the 5.5%/month rate "iniquitous or unconscionable, and hence contrary to morals ('contra bonos mores'), if not against the law." The rate was voided and replaced with 12% per annum (the legal interest rate at that time) plus 1% per month penalty as liquidated damages.

**Key quote:** The Court cannot consider the rate "usurious" because CB Circular No. 905 removed Usury Law ceilings. But unconscionability is a separate ground — rates can be struck down even though technically not "usurious."

**Significance:** Established that the suspension of usury ceilings does not give "carte blanche" to impose excessive rates. Courts retain equitable power to void unconscionable rates under Art. 1229 and Art. 1306.

**Source:** https://www.chanrobles.com/scdecisions/jurisprudence1998/nov1998/gr_131622_1998.php

#### F.2 Spouses Solangon v. Salazar (G.R. No. 125944, June 29, 2001)

**Facts:** Loan with stipulated interest of 6% per month (72% per annum).

**Holding:** The Supreme Court found 72% per annum "definitely outrageous and inordinate." Citing *Medel*, the Court held that CB Circular No. 905 "grants [no] lenders carte blanche authority to raise interest rates to levels which will either enslave their borrowers or lead to a hemorrhaging of their assets." The rate was reduced to 12% per annum.

**Significance:** Reinforced *Medel* and extended the unconscionability doctrine. Rates at or above 6%/month are presumptively unconscionable.

**Source:** https://chanrobles.com/scdecisions/jurisprudence2001/jun2001/gr_125944_2001.php

#### F.3 Ligutan v. Court of Appeals (G.R. No. 138677, February 12, 2002)

**Facts:** Loan with 15.189% annual interest and **5% monthly penalty** on outstanding principal and interest in case of default.

**Holding:** The Court of Appeals reduced the penalty from 5%/month to **3%/month** (36% per annum), considering partial compliance by the debtor. The Supreme Court upheld this reduction.

**Significance:** Established the multi-factor test for assessing penalty reasonableness: "the type, extent and purpose of the penalty, the nature of the obligation, the mode of breach and its consequences, the supervening realities, the standing and relationship of the parties."

**Source:** https://lawphil.net/judjuris/juri2002/feb2002/gr_138677_2002.html

#### F.4 Other Relevant Cases

| Case | Rate Struck Down | Rate Substituted | Notes |
|------|-----------------|-----------------|-------|
| *Chua v. Timan* (2008) | 7%/month (84% p.a.) | Reduced | Excessive for private loan |
| *Chua v. CA* (2004) | 10%/month | 2%/month | Severe reduction |
| *Lo v. CA* (2005) | 3%/month | Upheld | Within acceptable range |
| *Spouses Morada v. Racho* (G.R. No. 211499, Jan 10, 2018) | 3%/day | 6%/year | Extreme penalty voided |
| *Spouses Abellera v. Delfin* (CA-G.R. CV 101521, 2017) | 4%/day (~1,460% p.a.) | Voided | Unconscionable |
| *PSBank v. CA* | 3%/month | Reduced | Even bank penalties not immune |
| *Solidbank v. CA* | >2x market rate | Reduced | Proportionality test |

#### F.5 Judicial Threshold Summary

| Rate Range (per month) | Judicial Treatment |
|------------------------|-------------------|
| ≤1% (≤12% p.a.) | Almost always upheld, even for residential |
| 1-2% (12-24% p.a.) | Generally upheld for commercial; scrutinized for residential |
| 2-3% (24-36% p.a.) | Upheld for commercial with sophisticated parties; reduced for vulnerable parties |
| 3-5% (36-60% p.a.) | High risk of reduction; context-dependent |
| >5% (>60% p.a.) | Almost always reduced or voided |
| Daily penalties | Voided in every reported case |

---

## Formula / Decision Tree

### Penalty Computation Logic

```
INPUT:
  unpaid_balance       # Total overdue amount
  days_overdue         # Days past due (after grace period)
  lease_type           # "controlled" or "commercial"
  contractual_rate     # Penalty rate per month (if stipulated, else NULL)
  contractual_cap      # Maximum penalty amount (if stipulated, else NULL)
  ytd_penalty_total    # Year-to-date penalties already charged for this tenant

STEP 1: Determine applicable penalty rate
  IF contractual_rate IS NOT NULL:
    rate = contractual_rate
  ELSE:
    rate = 0.06 / 12    # Legal interest: 6% p.a. → 0.5% per month
    # Note: legal interest only applies from date of demand

STEP 2: Compute raw penalty
  monthly_penalty = unpaid_balance × rate
  prorated_penalty = monthly_penalty × (days_overdue / 30)  # If partial month

STEP 3: Apply caps (controlled units only)
  IF lease_type == "controlled":
    # Safe harbour: max 1% per month, total ≤ 1 month's rent per year
    rate_cap = 0.01  # 1% per month
    IF rate > rate_cap:
      rate = rate_cap
      monthly_penalty = unpaid_balance × rate_cap

    annual_cap = current_monthly_rent  # 1 month's rent
    IF ytd_penalty_total + monthly_penalty > annual_cap:
      monthly_penalty = MAX(0, annual_cap - ytd_penalty_total)

STEP 4: Apply compounding rules
  # Simple interest only — no compounding UNLESS:
  #   (a) Contract explicitly provides for compounding, AND
  #   (b) Formal demand (judicial/extrajudicial) has been made (Art. 2212)
  # For controlled units: simple interest always (safe harbour)

STEP 5: Output
  penalty_charge = ROUND_DOWN(monthly_penalty, 2)  # Tenant-favorable rounding
```

### Penalty Rate Lookup Table

| Lease Type | Contract Stipulates Rate? | Applicable Rate | Annual Cap | Legal Basis |
|-----------|--------------------------|----------------|------------|-------------|
| Controlled | Yes (≤1%/month) | Contractual rate | 1 month's rent/year | Art. 1226 + safe harbour |
| Controlled | Yes (>1%/month) | Cap at 1%/month | 1 month's rent/year | Art. 1229 + safe harbour |
| Controlled | No | 6% p.a. (from demand) | None (legal interest) | Art. 2209 + BSP Circ. 799 |
| Commercial | Yes (≤3%/month) | Contractual rate | Per contract | Art. 1306 + Art. 1226 |
| Commercial | Yes (>3%/month) | Flag for review | Per contract | Art. 1229 risk |
| Commercial | No | 6% p.a. (from demand) | None | Art. 2209 + BSP Circ. 799 |

---

## Edge Cases and Special Rules

### 1. Demand Requirement
Legal interest (6% p.a.) only runs from the date of extrajudicial or judicial demand, not automatically from the due date. The system must record when a demand letter was sent/received to correctly compute legal interest accrual.

**Exception:** If the contract stipulates a penalty rate, the penalty runs from the due date (or end of grace period) per the contract terms, without requiring separate demand.

### 2. Partial Payment
Art. 1229 mandates equitable reduction of penalties when the debtor has partially complied. A tenant who pays 80% of rent on time should not be penalized the same as one who pays nothing.

**Suggested approach:** Compute penalty only on the unpaid balance, not the full rent amount.

### 3. Leap Year / Month Length
Penalty computation should use actual days in month or a 30-day standardized month. For consistency, 30-day months are more common in PH lease practice.

### 4. Penalty on Penalties (Compounding)
Art. 2212 allows interest on interest only from judicial demand. For controlled units, compounding should never be applied (safe harbour = simple interest). For commercial units, compounding is permissible only if:
- The contract explicitly provides for it, AND
- Demand has been made (for the Art. 2212 compound layer)

### 5. Vacancy Decontrol and Penalty Regime
When a controlled unit becomes vacant and re-leases above P10,000/month, it exits rent control. The penalty regime shifts from "controlled safe harbour" to "commercial freedom of contract." The system must track this transition.

### 6. Multiple Overdue Months
When a tenant has multiple months of arrears, penalties should be computed per overdue invoice, each with its own accrual start date. The 3-month arrears ejectment threshold (RA 9653 Sec. 9(b)) should trigger an alert.

### 7. Tax on Penalty Amounts
Penalty charges collected are part of gross receipts:
- 12% VAT (if lessor is VAT-registered and lease is not VAT-exempt residential ≤P15,000/month)
- 5% EWT (to be withheld by tenant/payor)
- The penalty line item should show VAT component separately on the invoice

### 8. Prescription
Actions to collect unpaid rent and penalties prescribe in:
- 10 years for written contracts (Civil Code Art. 1144)
- 6 years for oral contracts (Civil Code Art. 1145)

---

## What Crispina Built

**Late penalty calculation: NOT BUILT.** (From `input/crispina-services.md`, Gap #8)

The Crispina codebase has:
- `calculate_compound_interest()` — could theoretically be used for penalty compounding, but it was designed for rent escalation
- `Charge` and `ChargeType` models — extensible to penalty charges
- Only 1 `ChargeType` seeded: "Rent" — no penalty charge type exists
- No penalty rate field on `Lease` or `LeaseRentable`
- No `date_demand_sent` tracking
- No concept of grace period in the data model
- No controlled vs. commercial flag on lease or rentable

**What would be needed to add penalty computation:**
1. New `ChargeType`: "Late Payment Penalty" (is_vat_inclusive=True, vat_rate=0.12)
2. Penalty rate field on `Lease` (or derived from lease type + contract)
3. Grace period field on `Lease` (default: 0 days for contracts specifying due date; 5 days if relying on RA 9653 Sec. 7)
4. `is_rent_controlled` flag on `Lease` (to enforce safe harbour caps)
5. `date_demand_sent` on overdue tracking (for legal interest accrual)
6. Year-to-date penalty accumulator per tenant-lease (to enforce annual cap for controlled)
7. Monthly penalty computation service that reads overdue charges and generates penalty Charge records

---

## Lightweight Feature Spec

### Data Model Additions

```
Lease (existing — add fields):
  + penalty_rate_monthly: PercentageDecimal (nullable — NULL = use legal interest)
  + grace_period_days: Integer (default 0)
  + is_rent_controlled: Boolean (default False)

ChargeType (new seed):
  + "Late Payment Penalty" (billing_name, is_vat_inclusive=True, vat_rate=0.12)

PenaltyLedger (new model):
  pk: UUID
  lease_pk: FK → Lease
  charge_pk: FK → Charge (the overdue charge that triggered this penalty)
  penalty_charge_pk: FK → Charge (the penalty charge generated)
  unpaid_amount: CurrencyDecimal
  rate_applied: PercentageDecimal
  days_overdue: Integer
  penalty_amount: CurrencyDecimal
  date_computed: Date
  computation_basis: Enum("contractual", "legal_interest", "safe_harbour_cap")

DemandRecord (new model):
  pk: UUID
  tenant_pk: FK → Tenant
  lease_pk: FK → Lease
  date_sent: Date
  method: Enum("letter", "email", "barangay", "judicial")
  total_arrears_at_demand: CurrencyDecimal
  months_in_arrears: Integer
```

### Inputs
- Overdue charges (from Charge table where date_due < today AND balance > 0)
- Lease metadata (penalty_rate_monthly, grace_period_days, is_rent_controlled)
- Year-to-date penalty total per lease (from PenaltyLedger)
- Current monthly rent (from RecurringChargePeriod for current period)
- Demand records (date_demand_sent for legal interest accrual)

### Outputs
- Penalty `Charge` record (linked to the original overdue charge via PenaltyLedger)
- Updated PenaltyLedger entry (full audit trail of computation)
- Arrears alert (warning at 2 months, ejectment-eligible at 3 months for controlled)
- Penalty line item on billing statement (VAT-inclusive, showing breakdown)

### Logic Flow
```
FOR each tenant WITH overdue charges:
  FOR each overdue Charge:
    days_overdue = today - MAX(charge.date_due + lease.grace_period_days, demand_date if no contractual rate)
    IF days_overdue <= 0: SKIP

    IF lease.penalty_rate_monthly IS NOT NULL:
      rate = lease.penalty_rate_monthly
    ELSE:
      IF demand_record EXISTS for this lease:
        rate = 0.005  # 6% p.a. / 12 = 0.5% per month
        days_overdue = today - demand_record.date_sent  # Interest runs from demand
      ELSE:
        rate = 0  # No penalty without contractual rate or demand
        SKIP

    raw_penalty = charge.balance × rate × (days_overdue / 30)

    IF lease.is_rent_controlled:
      # Enforce safe harbour
      rate = MIN(rate, 0.01)  # Cap at 1%/month
      raw_penalty = charge.balance × rate × (days_overdue / 30)
      annual_cap = current_monthly_rent
      ytd_total = SUM(PenaltyLedger.penalty_amount WHERE year = current_year AND lease_pk = lease.pk)
      raw_penalty = MIN(raw_penalty, MAX(0, annual_cap - ytd_total))

    penalty_amount = ROUND_DOWN(raw_penalty, 2)

    IF penalty_amount > 0:
      CREATE Charge(type="Late Payment Penalty", amount=penalty_amount, ...)
      CREATE PenaltyLedger(...)

  # Check arrears threshold
  months_overdue = COUNT(distinct months with unpaid rent charges)
  IF months_overdue >= 3 AND lease.is_rent_controlled:
    TRIGGER ejectment_alert(tenant, lease, months_overdue)
  ELIF months_overdue >= 2 AND lease.is_rent_controlled:
    TRIGGER warning_alert(tenant, lease, months_overdue)
```

---

## Automability Score: 4 / 5

**Justification:**
- Penalty computation for known rates is purely formulaic (score 5)
- Deducted 1 point because:
  - Determining whether a contractual rate is "unconscionable" requires human judgment — the system can flag rates exceeding safe harbour thresholds but cannot make a legal determination
  - Deciding whether/when to send a demand letter is a business decision
  - The controlled unit safe harbour caps are derived from legal commentary, not explicit statute — the business owner should confirm the policy with counsel
  - Determining cumulative months of arrears for ejectment purposes may require judgment on partial payments (does 60% payment count as a "month of arrears"?)

---

## Verification Status

### Confirmed Rules
- RA 9653 Section 7 (5-day payment window) — Confirmed via lawphil.net full text
- RA 9653 Section 9(b) (3-month arrears ejectment) — Confirmed via lawphil.net full text
- BSP Circular 799 (6% p.a. legal interest) — Confirmed via Nacar v. Gallery Frames and multiple secondary sources
- Civil Code Arts. 1226-1230 (penalty clause regime) — Confirmed via chanrobles.com and lawphil.net
- Civil Code Art. 2209 (legal interest on delay) — Confirmed via chanrobles.com
- Civil Code Art. 2212 (interest on interest from demand) — Confirmed via chanrobles.com
- Medel v. CA (66% p.a. struck down) — Confirmed via chanrobles.com
- Solangon v. Salazar (72% p.a. struck down) — Confirmed via chanrobles.com
- Ligutan v. CA (5%/month reduced to 3%/month) — Confirmed via lawphil.net
- Tax treatment (penalty = gross receipts, 12% VAT, 5% EWT) — Confirmed via RMC 11-2024 and RR 16-2005

### Source Conflicts Documented

1. **Residential penalty safe harbour (1%/month, max 1 month's rent/year):** This is cited by Respicio & Co. as a practical guideline synthesized from RA 9653's protective intent + Art. 1229 doctrine. It is NOT found as an explicit statutory provision in RA 9653 or the Civil Code. Other sources (respicio.ph commentary variants) cite slightly different formulations. The safe harbour should be treated as a *risk-management recommendation*, not a hard legal rule. **Recommendation:** Use the 1%/month / 1-month-cap as the default for controlled units but allow override with counsel's approval.

2. **RA 11571 confusion:** Some AI-generated legal commentary incorrectly references "RA 11571" as a rent control extension. RA 11571 is actually the JCEC Enhancement Act (energy regulation). The rent control framework continues through NHSB resolutions under RA 9653 Section 6, not through a separate RA.

3. **"Lapsed" RA 9653:** Multiple sources claim RA 9653 "lapsed after 2020." This is incorrect — NHSB resolutions under Section 6 maintain continuous regulatory authority. As of February 2026, NHSB Resolution 2024-01 is in effect through December 31, 2026.

4. **Penalty fine upper limit in RA 9653 Sec. 13:** Some sources cite P100,000 upper fine; the correct figure per lawphil.net is P50,000. (This is the penalty for *lessors violating the Act*, not for tenants.)

---

## Sources

### Primary Legal Sources
- RA 9653 (Rent Control Act): https://lawphil.net/statutes/repacts/ra2009/ra_9653_2009.html
- Civil Code of the Philippines (RA 386): https://lawphil.net/statutes/repacts/ra1949/ra_386_1949.html
- Civil Code Book IV (penalties, damages): https://chanrobles.com/civilcodeofthephilippinesbook4.htm
- BSP Circular 799: Referenced in Nacar v. Gallery Frames

### Jurisprudence
- Nacar v. Gallery Frames, G.R. No. 189871 (Aug. 13, 2013): https://lawphil.net/judjuris/juri2013/aug2013/gr_189871_2013.html
- Medel v. CA, G.R. No. 131622 (Nov. 27, 1998): https://www.chanrobles.com/scdecisions/jurisprudence1998/nov1998/gr_131622_1998.php
- Solangon v. Salazar, G.R. No. 125944 (Jun. 29, 2001): https://chanrobles.com/scdecisions/jurisprudence2001/jun2001/gr_125944_2001.php
- Ligutan v. CA, G.R. No. 138677 (Feb. 12, 2002): https://lawphil.net/judjuris/juri2002/feb2002/gr_138677_2002.html

### Regulatory / Administrative
- NHSB Resolution 2024-01: https://dhsud.gov.ph/wp-content/uploads/Laws_Issuances/07_NHSB/NHSB%20Resolution%202024-01%20(Rent%20Control%202025-2026).pdf
- RMC No. 11-2024 (BIR): https://bir-cdn.bir.gov.ph/BIR/pdf/RMC%20No.%2011-2024%20Final.pdf
- RR 16-2005 (VAT): https://bir-cdn.bir.gov.ph/BIR/pdf/26116rr16-2005.pdf

### Secondary / Commentary
- Respicio & Co. (rent late fee legality): https://www.respicio.ph/commentaries/rent-late-fee-legality-philippines
- Respicio & Co. (penalties for late rent): https://www.respicio.ph/commentaries/penalties-for-late-rent-payment-philippines
- Respicio & Co. (legal penalties): https://www.respicio.ph/commentaries/legal-penalties-for-late-rent-payments-in-the-philippines
