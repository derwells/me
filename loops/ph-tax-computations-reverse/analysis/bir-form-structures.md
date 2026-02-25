# BIR Form Structures — 2550Q and 1601-EQ

**Wave:** 1 — Source Acquisition
**Date:** 2026-02-25
**Sources:** BIR CDN (official forms/guidelines), Tax and Accounting Center PH, Forvis Mazars PH, CloudCFO, mpm.ph, PwC PH, Ocampo & Suralvo Law, Grant Thornton PH, KPMG PH, ForeclosurePhilippines.com, Taxumo, Juan.tax

---

## Overview

This file covers the official form structure, line-by-line field descriptions, computation logic, and practical filing guidance for two forms central to Philippine real estate tax compliance:

1. **BIR Form 2550Q** — Quarterly Value-Added Tax Return (April 2024 ENCS)
2. **BIR Form 1601-EQ** — Quarterly Remittance Return of Creditable Income Taxes Withheld (Expanded) (January 2019 ENCS)

These two forms interact closely: a real estate developer simultaneously files 2550Q (for output VAT on property sales) and 1601-EQ (for withholding taxes deducted from broker commissions, professional fees, rents, and other service payments). They also interact with Forms 2307, 1606, and 0619-E.

---

## Part 1: BIR Form 2550Q — Quarterly Value-Added Tax Return

### 1.1 Legal Basis and Purpose

- NIRC Section 114(A), as amended by TRAIN Law (RA 10963) and EOPT Act (RA 11976)
- Revenue Memorandum Circular (RMC) No. 05-2023: implemented mandatory quarterly-only VAT filing effective January 1, 2023
- RMC No. 52-2023: authorized optional continuation of monthly filing but kept quarterly return as mandatory
- RMC No. 68-2024: released the April 2024 (ENCS) revised form incorporating EOPT Act fields
- Revenue Regulations (RR) No. 3-2024: operationalized EOPT Act VAT provisions (effective April 27, 2024)

### 1.2 Who Must File

Every VAT-registered individual or entity that:
- Sells goods or properties subject to VAT
- Renders services subject to VAT
- Has registered for VAT (either mandatorily, because annual gross sales exceed ₱3,000,000, or voluntarily)

### 1.3 Abolishment of Monthly Form 2550M

Effective January 1, 2023 (per RMC 05-2023):
- BIR Form 2550M is **no longer mandatory**
- Taxpayers file only 2550Q quarterly
- Optional monthly filing via 2550M still permitted (RMC 52-2023), but if filed monthly it does NOT replace the quarterly 2550Q
- Those who file 2550M monthly must still file 2550Q quarterly, and any monthly payments made under 2550M are credited against the 2550Q liability for the quarter
- **There are no longer prescribed deadlines for monthly 2550M** — the only mandatory deadline is the quarterly 2550Q

### 1.4 Deadline Rules

| Quarter | Covered Period | Deadline |
|---|---|---|
| Q1 | January–March | April 25 |
| Q2 | April–June | July 25 |
| Q3 | July–September | October 25 |
| Q4 | October–December | January 25 (following year) |

Deadline rule: **25th day following the close of each taxable quarter**.

If the 25th falls on a Saturday, Sunday, or legal holiday, the deadline moves to the next working day.

### 1.5 Form Structure — All Parts

#### PART I: Background Information

| Item | Field | Notes |
|---|---|---|
| 1 | Calendar or Fiscal Year | Indicate C (calendar) or F (fiscal) |
| 2 | Year Ended (MM/YYYY) | End of the taxable year |
| 3 | Quarter | 1st / 2nd / 3rd / 4th |
| 4 | Return Period (MM/DD/YYYY) | Last day of the quarter |
| 5 | Amended Return? | Yes/No |
| 6 | Short Period Return? | Yes/No |
| 7 | Taxpayer Identification Number (TIN) | 9-digit TIN + 3-digit branch code |
| 8 | RDO Code | Revenue District Office jurisdiction |
| 9 | Taxpayer's Name | Registered legal name |
| 10 | Registered Address | Use branch address if filing for a branch |
| 11 | Contact Number | |
| 12 | Email Address | |
| 13 | Taxpayer Classification | Micro / Small / Medium / Large (per RR 6-2024) |
| 14 | Tax Relief Availed? | Yes/No — under Special Law or International Tax Treaty |

#### PART II: Total Tax Payable

| Item | Field | Source / Formula |
|---|---|---|
| 15 | Net VAT Payable / (Excess Input Tax) | From Part IV, Item 61 |
| 16 | Creditable VAT Withheld | From Part V, Schedule 3, Column D — sum of all Form 2307 VAT credits for the quarter |
| 17 | Advance VAT Payments | From Part V, Schedule 4 — advance VAT paid by sugar/flour millers |
| 18 | VAT Paid in Return Previously Filed | For amended returns only — VAT paid under the original return being amended |
| 19 | Other Credits/Payments | Miscellaneous credits (e.g., tax credit certificates) |
| 20 | Total Tax Credits/Payments | Sum of Items 16 through 19 |
| 21 | Tax Still Payable / (Excess Credits) | Item 15 minus Item 20 |
| 22 | Surcharge | 25% of Item 21 (if filed late or wrong) |
| 23 | Interest | 12% per annum of deficiency × (days late / 365) |
| 24 | Compromise | Per RMO 7-2015 Annex A schedule |
| 25 | Total Penalties | Sum of Items 22–24 |
| 26 | Total Amount Payable / (Excess Credits) | Item 21 + Item 25 |

#### PART III: Details of Payment

| Item | Field |
|---|---|
| 27 | Cash / Bank Debit Advice — amount and drawee bank |
| 28 | Check — check number, bank, branch |
| 29 | Tax Debit Memo — TDM number and amount |
| 30 | Others — specify payment type and amount |

Machine validation or Revenue Official Receipt details if not filed through an Authorized Agent Bank.

#### PART IV: Details of VAT Computation

This is the computational core. Two columns throughout:
- **Column A:** Sales for the Quarter (VAT-exclusive peso amounts)
- **Column B:** Output/Input Tax peso amounts

**Section A — Output Tax (Sales and Receipts)**

| Item | Field | Column A | Column B |
|---|---|---|---|
| 31 | VATable Sales | Gross sales exclusive of VAT | Output tax = Col A × 12% |
| 32 | Zero-Rated Sales | Gross sales of zero-rated transactions | Output tax = 0 |
| 33 | Exempt Sales | Gross sales of VAT-exempt transactions | Output tax = 0 |
| 34 | Total Sales / Output Tax Due | Sum of Items 31A–33A | Item 31B only (VATable only) |
| 35 | Less: Output VAT on Uncollected Receivables | — | Deduction per EOPT Act (post-April 27, 2024 transactions on credit terms not yet collected) |
| 36 | Add: Output VAT on Recovered Uncollected Receivables Previously Deducted | — | Reversal when previously deducted receivables are subsequently collected |
| 37 | Total Adjusted Output Tax Due | — | Item 34B − Item 35B + Item 36B |

**Notes on Items 35 and 36 (EOPT Act):**
- Applies only to sales on credit made **after April 27, 2024**
- Requires a written agreement specifying credit terms with VAT shown separately
- The agreed payment period must have lapsed and the amount must remain uncollected
- If the receivable is subsequently collected, it must be reversed via Item 36
- eFPS/eBIRForms filers with amounts in Items 35 or 36 must use the manual PDF form (electronic systems not yet updated as of RMC 68-2024)

**Section B — Allowable Input Tax**

| Item | Field | Notes |
|---|---|---|
| 38 | Input Tax Carried Over from Previous Quarter | Ending balance of allowable input tax from prior quarter's Item 60 |
| 39 | Input Tax Deferred on Capital Goods > ₱1M from Previous Quarter | Balance of unamortized input VAT on capital goods carried forward |
| 40 | Transitional Input Tax | For taxpayers newly VAT-registered converting from non-VAT status: 2% of beginning inventory value or actual VAT paid on inventory, whichever is higher |
| 41 | Presumptive Input Tax | For sardine/mackerel processors, refined sugar, cooking oil, instant noodle manufacturers: 4% of primary agricultural product purchases |
| 42 | Others | Specify |
| 43 | Total Prior Period Input Tax | Sum of Items 38–42 |

**Current Quarter Purchases (Input Tax on Current Transactions):**

| Item | Field | Notes |
|---|---|---|
| 44 | Purchase of Capital Goods Not Exceeding ₱1M | Input VAT fully creditable in current quarter |
| 45 | Purchase of Capital Goods Exceeding ₱1M | Input VAT amortized — amount entered here is the **allowable portion for the quarter** (from Schedule 1 computation) |
| 46 | Domestic Purchases of Goods Other Than Capital Goods | Regular goods/materials for business operations |
| 47 | Importation of Goods Other Than Capital Goods | VAT paid on importation |
| 48 | Domestic Purchase of Services | VAT on service providers, contractors |
| 49 | Services Rendered by Non-Residents | VAT self-assessed on cross-border services |
| 50 | Others | Specify |
| 51 | Total Current Input Tax | Sum of Items 44–50 |
| 52 | Total Available Input Tax | Item 43 + Item 51 |

**Input Tax Deductions (amounts NOT creditable):**

| Item | Field | Notes |
|---|---|---|
| 53 | Input Tax Attributable to VAT-Exempt Sales | From Schedule 2 — computed as direct attribution plus ratable portion |
| 54 | Input Tax Attributable to Sales to Government | Direct attribution plus ratable portion of mixed-use input VAT |
| 55 | Input VAT on Unpaid Payables | New EOPT field — deduction for input VAT on purchases not yet paid (mirror of Item 35 logic) |
| 56 | Others | Specify |
| 57 | Total Deductions from Input Tax | Sum of Items 53–56 |
| 58 | Add: Input VAT on Settled Unpaid Payables Previously Deducted | Reversal when unpaid payables deducted under Item 55 are subsequently paid |
| 59 | Adjusted Deductions from Input Tax | Item 57 − Item 58 |
| 60 | Total Allowable Input Tax | Item 52 − Item 59 |
| 61 | Net VAT Payable / (Excess Input Tax) | Item 37B − Item 60 → carried to **Part II, Item 15** |

**If Item 61 is positive:** VAT is owed to BIR.
**If Item 61 is negative:** Excess input tax — may be carried forward to next quarter or used as basis for refund claim.

#### PART V: Schedules

**Schedule 1 — Amortized Input Tax from Capital Goods Exceeding ₱1M**

For each capital good costing more than ₱1,000,000 (inclusive of VAT), the input VAT is amortized rather than claimed immediately.

| Column | Description |
|---|---|
| A | Date Purchased |
| B | Description of Capital Good |
| C | Source Code: D (Domestic Purchase) or I (Importation) |
| D | Amount of Capital Good (VAT-exclusive) |
| E | Total Input Tax (Amount D × 12%) |
| F | Input Tax Recognized in Previous Periods |
| G | Estimated Useful Life in Months (cap: 60 months; use actual life if shorter) |
| H | Allowable Input Tax for the Quarter (E ÷ G × number of months in use this quarter) |
| I | Balance of Input Tax to Carry to Next Period (E − F − H) |

Amortization formula: `Quarterly allowable = Total input VAT ÷ Estimated life in months × months in quarter`
The amortization period is **60 months maximum** (5 years) or the actual estimated useful life, whichever is shorter.
Column H total flows to Part IV, Item 45.
Column I total flows to Part IV, Item 39 of the next quarter's return.

**Schedule 2 — Input Tax Attributable to VAT-Exempt Sales**

Used to compute the portion of input VAT that must be deducted because it relates to exempt sales.

| Line | Description | Formula |
|---|---|---|
| A | Input Tax directly attributable to VAT-Exempt Sales | Direct identification |
| B | Ratable portion of common input tax | (Exempt Sales ÷ Total Sales) × Input Tax not directly attributable |
| C | Total Input Tax Attributable to Exempt Sales (A + B) | → flows to Part IV, Item 53 |

**Schedule 3 — Creditable VAT Withheld (Form 2307 Credits)**

| Column | Description |
|---|---|
| A | Period Covered (month/year of withholding) |
| B | Name of Withholding Agent (government entity that withheld VAT) |
| C | Income Payment Subject to VAT Withholding |
| D | Total VAT Tax Withheld (ATC WV010 or WV020 amounts from Form 2307) |

Column D total → flows to Part II, Item 16.

This schedule is populated from BIR Form 2307 certificates received by the taxpayer from government agency buyers who withheld VAT under the creditable VAT withholding system (Form 1600-VT filing by the government agency; ATC WV010 for goods, WV020 for services).

**Schedule 4 — Advance VAT Payment (Sugar/Flour Mill Industry)**

| Column | Description |
|---|---|
| A | Period Covered |
| B | Name of Miller |
| C | Name of Taxpayer (agricultural producer) |
| D | Official Receipt Number |
| E | Amount of Advance VAT Paid |

Column E total → flows to Part II, Item 17. Applies primarily to sugar and flour industries where advance VAT is collected at the milling stage.

### 1.6 VAT Computation — Step-by-Step Logic

```
Step 1: Compute Output Tax
  Output Tax = 12% × VATable Sales (Item 31A)
  Adjust for EOPT if applicable:
    Adjusted Output Tax = Output Tax − Item 35B + Item 36B (= Item 37B)

Step 2: Aggregate Input Tax
  Prior period input tax (carried forward + deferred capital goods) = Item 43
  Current quarter input tax (purchases + imports + services) = Item 51
  Total Available Input Tax = Item 52 = Item 43 + Item 51

Step 3: Deduct Non-Creditable Input Tax
  Remove: input tax on exempt sales (Sched 2)
  Remove: input tax on government sales (allocated)
  Remove: input VAT on unpaid payables (EOPT, if applicable)
  Add back: input VAT on settled previously-unpaid payables (EOPT reversal)
  Total Allowable Input Tax = Item 60

Step 4: Compute Net VAT
  Net VAT = Item 37B (Adjusted Output Tax) − Item 60 (Allowable Input Tax)
  = Item 61 → to Part II Item 15

Step 5: Apply Credits
  Subtract creditable VAT withheld (Sched 3 → Item 16)
  Subtract advance VAT payments (Sched 4 → Item 17)
  Subtract prior payments if amended return (Item 18)
  Subtract other credits (Item 19)
  Total Credits = Item 20

Step 6: Determine Amount Payable
  Tax Still Payable = Item 15 − Item 20 = Item 21
  Add penalties if late (Items 22–25)
  Final amount = Item 26
```

### 1.7 Real Estate Transactions on Form 2550Q

**Determining VAT vs. Exempt:**

| Property Type | Condition | 2550Q Treatment |
|---|---|---|
| Residential dwelling (house and lot) | Selling price ≤ ₱3,600,000 (threshold as of Jan 1, 2024) | Exempt — Item 33 |
| Residential dwelling (house and lot) | Selling price > ₱3,600,000 | Taxable — Item 31 (12% VAT) |
| Residential lot only | Selling price ≤ ₱1,919,500 (historical; may be adjusted) | Exempt — Item 33 |
| Socialized housing | Any selling price under RA 7279 | Exempt — Item 33 |
| Commercial property | Any selling price | Taxable — Item 31 (12% VAT) |
| Industrial property | Any selling price | Taxable — Item 31 (12% VAT) |

The ₱3,600,000 residential dwelling threshold (effective January 1, 2024) is adjusted every three years using the Consumer Price Index (CPI) published by the Philippine Statistics Authority. The next adjustment is due in 2027. This is a Section 109(P) NIRC exemption.

**VAT Base:**
```
Output VAT = 12% × max(Gross Selling Price, Fair Market Value)
  where FMV = max(BIR Zonal Value, Assessed FMV per LGU)
```

If the selling price is stated VAT-inclusive: Net = GSP ÷ 1.12; VAT = GSP − Net.
If stated VAT-exclusive: VAT = GSP × 12%.

**Sales Classification in Part IV:**
- All VATable property sales → Item 31
- Zero-rated sales (e.g., export of services, PEZA-zone sales) → Item 32
- VAT-exempt property sales → Item 33
- Both VATable and exempt sales in the same quarter → split entries; Schedule 2 required to apportion input VAT

**Input VAT on Development Costs:**
- Land acquisition: no input VAT (land is exempt; no VAT on bare land)
- Construction materials and contractor services: subject to 12% input VAT — creditable
- Professional fees (architects, engineers): 12% VAT if provider is VAT-registered — creditable
- Capital equipment > ₱1M: input VAT amortized per Schedule 1
- Mixed-use costs (attributable to both exempt and taxable projects): Schedule 2 apportionment required

**Installment Sales — Output VAT Recognition:**
- Initial payments in year of sale ≤ 25% of gross selling price → **installment method**: output VAT recognized per collection received
- Initial payments > 25% → **cash sale method**: full output VAT recognized in the quarter of sale
- "Initial payments" = down payment + all principal amortizations received during the year of sale (excludes interest)

**Government Sales VAT Withholding:**
When selling to a government agency, the agency withholds a creditable VAT (currently 5%) and remits via Form 1600-VT, issuing the developer a Form 2307 (ATC WV010 for goods/property, WV020 for services). The developer enters this on Schedule 3 and claims it as a credit in Part II, Item 16. The full output VAT must still be reported in Item 31.

### 1.8 Relationship Between Form 2550M (Monthly) and 2550Q (Quarterly)

Post-January 1, 2023:

| Feature | Form 2550M | Form 2550Q |
|---|---|---|
| Filing status | Optional only (no fixed deadline) | Mandatory; due 25th after quarter close |
| Tax period | Monthly | Quarterly |
| Replaces the other? | No — monthly filers still must file 2550Q | Yes — 2550Q is the sole mandatory return |
| Monthly payments credit | VAT paid via 2550M in months 1–2 of the quarter credited in 2550Q Item 18 (if treated as prior payments) | Consolidates full quarter |

In practice, for developers who no longer file 2550M (most, post-2023): the quarter is reported once in 2550Q, no monthly credits to track. For those who still optionally file monthly 2550M: the payments become "VAT paid in return previously filed" entered in Item 18 of the 2550Q.

### 1.9 Form 2307 — How It Is Used on Form 2550Q

BIR Form 2307 (Certificate of Creditable Tax Withheld at Source) is used in two different ways on 2550Q:

**A. For EWT (Income Tax Withholding) on the Developer's Revenue:**
- Not directly on 2550Q. EWT withheld from the developer's income (e.g., withholding by corporate clients on commissions or service fees) flows to the developer's income tax return, not to 2550Q.
- Exception: When the developer provides services to Top Withholding Agents, the 1%/2% creditable tax withheld is creditable against income tax, not VAT.

**B. For VAT Withholding (Government Buyers):**
- When a government agency (GOCCs, instrumentalities, LGUs) buys property from the developer, it withholds a creditable VAT.
- The agency files Form 1600-VT and issues Form 2307 to the developer using ATC **WV010** (goods/property) or **WV020** (services).
- Developer enters these 2307s on **Part V, Schedule 3** of Form 2550Q.
- Total VAT withheld per Schedule 3, Column D → entered at **Part II, Item 16**.
- This reduces the net VAT payable.

**C. Form 2306 is NOT issued for VAT withholding:**
Under the VAT withholding shift to creditable (from final), Form 2306 is no longer used for government VAT withholding. Only Form 2307 is issued. Form 2306 was used under the old final withholding VAT system.

### 1.10 Required Attachments

- Summary List of Sales (SLS) — part of SLSPI submitted via BIR eSubmission/RELIEF system
- Summary List of Purchases (SLP) — same
- Summary List of Importations (SLI) — if applicable
- Quarterly Alphalist of Sales (QAS)
- Form 2307 certificates received (for Schedule 3 claims) — submit copies to BIR with return
- For amended returns: original return and proof of prior payment

### 1.11 Penalties

| Penalty Type | Rate / Amount |
|---|---|
| Surcharge (late filing) | 25% of tax due (or unpaid tax) |
| Interest (deficiency) | 12% per annum × (days late ÷ 365) |
| Compromise | Per RMO 7-2015 Annex A; reduced 50% for Micro/Small taxpayers under RR 6-2024 |
| Using wrong form | Penalties under Section 250 of the NIRC (up to ₱25,000) |

---

## Part 2: BIR Form 1601-EQ — Quarterly Remittance Return of Creditable Income Taxes Withheld (Expanded)

### 2.1 Legal Basis and Purpose

- Revenue Memorandum Circular (RMC) No. 27-2018: introduced Form 1601-EQ as part of the TRAIN Law withholding tax form revamp
- Revenue Regulations (RR) No. 11-2018: amended RR 2-98; updated EWT rates and categories effective January 1, 2018
- Revenue Regulations (RR) No. 2-98 (as amended): the master regulation governing expanded withholding tax, including Section 2.57.2 on specific EWT rates and Section 2.57.5 on exemptions
- RMC No. 31-2025: clarified Form 1606 as sole proof for real property CWT credit claims

Form 1601-EQ is filed by every withholding agent who deducts and withholds creditable income taxes (Expanded Withholding Tax / EWT) from income payments to vendors, service providers, professionals, lessors, and others. It consolidates the three months of a quarter.

### 2.2 Who Must File

- All withholding agents (businesses, individuals in trade/profession) who make payments subject to EWT
- Real estate developers file 1601-EQ for EWT deducted from:
  - Real estate broker/agent commissions
  - Professional fees (lawyers, architects, engineers, accountants)
  - Rental payments on office/equipment
  - Construction contractor fees
  - Other service providers

Note: Real estate developers do NOT report the CWT withheld by buyers on property sales on Form 1601-EQ. That withholding is remitted by buyers using **Form 1606** (per-transaction), not 1601-EQ.

### 2.3 Deadline Rules

| Quarter | Covered Period | Deadline |
|---|---|---|
| Q1 | January–March | April 30 (last day of following month) |
| Q2 | April–June | July 31 |
| Q3 | July–September | October 31 |
| Q4 | October–December | January 31 (following year) |

Deadline rule: **Last day of the month following the close of the quarter.**
This is later than the 2550Q deadline (25th vs. last day of the following month).

### 2.4 Relationship with Monthly Form 0619-E

| Form | Period | Purpose |
|---|---|---|
| Form 0619-E | Monthly (months 1 and 2 of each quarter only) | Remit EWT withheld in the first and second months |
| Form 1601-EQ | Quarterly (covers all 3 months) | Consolidated return; shows total EWT for the quarter and credits monthly payments |

Monthly 0619-E deadlines:
- For over-the-counter filers: 10th day following the end of the month
- For eFPS filers: 15th day following the end of the month

The third month of each quarter has **no separate monthly 0619-E**. All three months are consolidated in 1601-EQ.

How credits work on 1601-EQ:
- Item 20: enter EWT remitted via 0619-E for month 1 of the quarter
- Item 21: enter EWT remitted via 0619-E for month 2 of the quarter
- Item 19 minus Items 20 + 21 = EWT still due (for month 3) = Item 22, net amount to pay

### 2.5 Form Structure — All Items

#### PART I: Background Information

| Item | Field | Notes |
|---|---|---|
| 1 | Year | Calendar year of filing |
| 2 | Quarter | Q1 / Q2 / Q3 / Q4 |
| 3 | Amended Return? | Yes/No |
| 4 | Any amount to be paid? | Yes/No — if No, file as "No Transaction" return |
| 5 | TIN | Withholding agent's TIN |
| 6 | RDO Code | Withholding agent's RDO |
| 7 | Taxpayer's Name | Registered name of withholding agent |
| 8 | Registered Address | |
| 9 | Zip Code | |
| 10 | Contact Number | |
| 11 | Email Address | |
| 12 | Taxpayer Classification | Micro / Small / Medium / Large |

#### PART II: Computation of Tax

| Item | Field | Notes |
|---|---|---|
| 13–18 | ATC Entry Lines | Each line: (a) select ATC from dropdown, (b) enter tax base for the quarter, (c) tax rate auto-populates, (d) withholding tax auto-computed. Multiple lines available for multiple ATCs. |
| 19 | Total Withholding Tax for the Quarter | Sum of withholding taxes across all ATC lines |
| 20 | Less: EWT Remitted for First Month of Quarter (0619-E, Month 1) | Amount from 0619-E filed for month 1 |
| 21 | Less: EWT Remitted for Second Month of Quarter (0619-E, Month 2) | Amount from 0619-E filed for month 2 |
| 22 | Net Tax Still Due | Item 19 − Item 20 − Item 21 |

#### PART III: Over-Remittance

| Item | Field | Notes |
|---|---|---|
| 23 | Over-Remittance from Previous Quarter | Only same calendar-year over-remittances may be credited; prior-year carryovers are prohibited |
| 24 | Net Tax Payable / (Over-Remittance) | Item 22 − Item 23 |

#### PART IV: Tax Still Due / (Over-Remittance) Options

| Item | Field | Notes |
|---|---|---|
| 25 | Surcharge | 25% if filed/paid late |
| 26 | Interest | 12% per annum |
| 27 | Compromise | Per RMO 7-2015 |
| 28 | Total Penalties | Sum of Items 25–27 |
| 29 | Total Amount Payable / (Over-Remittance) | Item 24 + Item 28 |

#### PART V: Details of Payment

| Item | Field |
|---|---|
| 30 | Cash / Bank Debit Advice |
| 31 | Check |
| 32 | Tax Debit Memo |
| 33 | Others |

#### OVER-REMITTANCE DISPOSITION (Item 31 area)

If there is an over-remittance, the withholding agent may:
1. **Carry forward** to next quarter of the same year
2. **Apply for refund** (via formal claim to RDO)
3. **Apply for a Tax Credit Certificate (TCC)**

Over-remittances cannot be carried forward across calendar years — a refund claim must be filed instead.

**Important obligation:** If over-remittance results from excess withholding, the withholding agent must correct any Form 2307 issued to the payee so the payee does not claim a credit for taxes not actually withheld.

### 2.6 ATC Codes — Schedule of Alphanumeric Tax Codes

The ATC schedule is on Page 2 of Form 1601-EQ. Prefix convention:
- **WI** = Individual payee
- **WC** = Non-individual / Corporate payee

#### Professional Fees (Section 2.57.2(A), RR 2-98 as amended by RR 11-2018)

| ATC | Description | Rate |
|---|---|---|
| WI010 | Professional fees — individual; gross income for current year ≤ ₱3,000,000 | 5% |
| WI011 | Professional fees — individual; gross income > ₱3,000,000 or VAT-registered | 10% |
| WC010 | Professional fees — corporation; gross income ≤ ₱720,000 | 10% |
| WC011 | Professional fees — corporation; gross income > ₱720,000 | 15% |

Applicable to: lawyers, CPAs, engineers, architects, consultants, doctors in professional practice.

#### Entertainers, Directors, Producers

| ATC | Description | Rate |
|---|---|---|
| WI020 | Professional entertainers — individual; gross income ≤ ₱3,000,000 | 5% |
| WI021 | Professional entertainers — individual; gross income > ₱3,000,000 | 10% |
| WI030 | Professional athletes | 5% or 10% (per threshold) |
| WI040 | All directors and producers (movies, stage, radio, TV, music) — individual; ≤ ₱3M | 5% |
| WI041 | Same — individual; > ₱3M | 10% |

#### Brokers and Agents (Including Real Estate Brokers)

| ATC | Description | Rate |
|---|---|---|
| WI040 | Gross commissions — real estate, insurance, commercial brokers & agents — individual; ≤ ₱3,000,000 | 10% |
| WI041 | Same — individual; > ₱3,000,000 or VAT-registered | 15% |
| WC040 | Gross commissions — corporate broker/agent; ≤ ₱720,000 | 10% |
| WC041 | Same — corporate; > ₱720,000 | 15% |

Note: The ATC code WI040 is shared across directors, producers, and brokers in some versions of the form — the applicable description is determined by the nature of the payment, not just the code.

#### Management and Technical Consultants

| ATC | Description | Rate |
|---|---|---|
| WI050 | Individual management/technical consultant; ≤ ₱3M | 5% |
| WI051 | Individual; > ₱3M or VAT-registered | 10% |
| WC050 | Corporate management/technical consultant; ≤ ₱720K | 10% |
| WC051 | Corporate; > ₱720K | 15% |

#### Rentals (Real and Personal Property)

| ATC | Description | Rate |
|---|---|---|
| WI100 | Real property rentals — individual lessor | 5% |
| WC100 | Real property rentals — corporate lessor | 5% |
| WI110 | Cinematographic film rentals — individual | 5% |
| WC110 | Cinematographic film rentals — corporate | 5% |

Applicable to: rent paid on office space, land, equipment, commercial premises. Rate is 5% of gross rental payment.

Separate ATC codes (WI160/WC160) are also sometimes used for rentals depending on context; refer to the current form's ATC schedule for the operative codes.

#### Contractors and Subcontractors

| ATC | Description | Rate |
|---|---|---|
| WI120 | Payments to general and specialty contractors — individual | 2% |
| WC120 | Payments to general and specialty contractors — corporate | 2% |

Applicable to: construction contractors, subcontractors, civil works, renovation contractors.

#### Top Withholding Agents (TWAs)

Certain large taxpayers designated by BIR as Top Withholding Agents must withhold on all purchases of goods and services:

| ATC | Description | Rate |
|---|---|---|
| WI158 | TWA — income payment to local/resident supplier of **goods** — individual | 1% |
| WC158 | TWA — income payment to local/resident supplier of **goods** — corporate | 1% |
| WI160 | TWA — income payment to local/resident supplier of **services** — individual | 2% |
| WC160 | TWA — income payment to local/resident supplier of **services** — corporate | 2% |

These apply broadly to all TWA purchases not covered by higher specific EWT rates.

#### Agricultural Products

| ATC | Description | Rate |
|---|---|---|
| WI610 | Agricultural products — individual seller; cumulative annual purchases > ₱300,000 | 1% |
| WC610 | Agricultural products — corporate seller | 1% |

#### Other Notable ATCs

| ATC | Description | Rate |
|---|---|---|
| WI130 | Income distributed to beneficiaries of estates and trusts | 15% |
| WI515 | Independent sales representatives / marketing agents | 10% |
| WC515 | Same — corporate | 10% |

### 2.7 Real Estate Transactions and Form 1601-EQ

**What DOES go on Form 1601-EQ for real estate businesses:**

| Payment Type | ATC | Rate | Notes |
|---|---|---|---|
| Broker/agent commission (individual, ≤ ₱3M) | WI040 | 10% | Most individual brokers fall here |
| Broker/agent commission (individual, > ₱3M or VAT-reg) | WI041 | 15% | High-volume brokers |
| Broker/agent commission (corporate) | WC040/WC041 | 10% or 15% | Brokerage firms |
| Architect/engineer professional fees (individual, ≤ ₱3M) | WI010 | 5% | Design, supervision fees |
| Architect/engineer professional fees (individual, > ₱3M) | WI011 | 10% | |
| Lawyer fees (individual, ≤ ₱3M) | WI010 | 5% | Legal counsel for transactions |
| CPA/accounting fees (individual, ≤ ₱3M) | WI010 | 5% | |
| Management consultant (individual, ≤ ₱3M) | WI050 | 5% | Property management contracts |
| Construction contractor (individual) | WI120 | 2% | Civil works, construction |
| Construction contractor (corporate) | WC120 | 2% | |
| Office/equipment rental (individual lessor) | WI100 | 5% | Rent on developer's own office space |
| Office/equipment rental (corporate lessor) | WC100 | 5% | |

**What does NOT go on Form 1601-EQ for real estate businesses:**

The CWT withheld by the **buyer** on property sales (ordinary assets) is remitted using **Form 1606** (one return per transaction), NOT Form 1601-EQ. The developer/seller receives the Form 1606 copy (or the buyer's 1606 with proof of payment) and uses it as a credit against income tax in the ITR. Form 2307 is no longer issued for these real property sales per RMC 99-2023 and RMC 31-2025 — Form 1606 with proof of payment is the sole acceptable credit instrument.

Summary:
```
Developer AS PAYOR → withholds EWT from commissions/fees/rent → remits via 1601-EQ
Developer AS PAYEE (property seller) → buyer withholds CWT → buyer remits via Form 1606
                                                              → developer receives Form 1606 copy
                                                              → credits Form 1606 against income tax
                                                              → does NOT use Form 2307 for this purpose
```

### 2.8 EWT Rates for Sale of Real Property (Ordinary Assets) — Filed via Form 1606, Not 1601-EQ

For completeness, since these are creditable withholding taxes on real property sales (reported on 1606, not 1601-EQ):

**Seller habitually engaged in real estate business** (registered with HLURB/HUDCC, or made ≥ 6 taxable realty transactions in the preceding year):

| Gross Selling Price or FMV (whichever is higher) | Rate | ATC |
|---|---|---|
| Up to ₱500,000 | 1.5% | WI040 |
| Over ₱500,000 to ₱2,000,000 | 3% | WI500 |
| Over ₱2,000,000 | 5% | WI510 |

**Seller NOT habitually engaged in real estate business** (e.g., banks selling foreclosed properties, individuals selling one property):

| Condition | Rate | ATC |
|---|---|---|
| Not habitually engaged | 6% | WI160 (individual) / WC160 (corporate) |

**Corporation selling ordinary asset** (any amount, habitually engaged):

| Condition | Rate | ATC |
|---|---|---|
| Corporate seller, habitually engaged | 6% | WC530 |

These rates apply to the **higher of** gross selling price or FMV (where FMV = higher of BIR zonal value or assessed FMV per LGU assessor).

Legal basis: Section 2.57.2(J) of RR 2-98 as amended by RR 6-2001, RR 17-2003, and RR 11-2018.

### 2.9 Form 2307 — How It Is Issued and Used

**Developer as withholding agent (payor of commissions/fees/rent):**
- Developer deducts EWT from payment to broker/professional/lessor
- Developer remits EWT via 0619-E (months 1–2) and 1601-EQ (quarterly consolidation)
- Developer **issues Form 2307** to each payee (broker, professional, lessor)
- Form 2307 fields: payee name and TIN, withholding agent name and TIN, ATC, income payment amount, amount withheld, tax period covered
- Form 2307 is issued in quadruplicate; two copies go to the payee for their own tax credit claims against income tax

**Payee (broker, professional) receiving Form 2307:**
- Attaches Form 2307 to their own ITR to claim EWT as a tax credit
- Sum of all 2307s received ≤ income tax due → offset; if >  income tax due → refund claim or carryover

**QAP (Quarterly Alphalist of Payees):**
- The list of all payees from whom EWT was withheld, submitted with 1601-EQ
- Required to be submitted in DAT file format via BIR eSubmission (esubmission@bir.gov.ph)
- Deadline same as 1601-EQ
- Fields in QAP: payee TIN, name, address, ATC, income payment, tax withheld, quarter covered

### 2.10 Required Attachments for Form 1601-EQ

1. **Quarterly Alphalist of Payees (QAP)** — mandatory; submitted as DAT file via eSubmission
   - Retention of BIR eSubmission validation report as proof of submission
2. Form 0619-E receipts/confirmations for months 1 and 2 (for reconciliation of Items 20–21)
3. Copies of issued Form 2307 certificates retained for records

### 2.11 Penalties

| Penalty | Rate / Amount |
|---|---|
| Late filing surcharge | 25% of EWT due |
| Interest | 12% per annum |
| Compromise | ₱1,000 to ₱25,000 per RMO 7-2015; reduced 50% for Micro/Small taxpayers under RR 6-2024 (₱500–₱12,500) |
| QAP late/non-submission | Same penalty schedule as late filing |

---

## Part 3: Interaction Between 2550Q and 1601-EQ in Real Estate Operations

### 3.1 Parallel Filing Obligations

A VAT-registered real estate developer filing for Q2 (April–June):

| Form | Deadline | What It Covers |
|---|---|---|
| 2550Q | July 25 | VAT on property sales; input VAT on construction/development costs; net VAT payable |
| 1601-EQ | July 31 | EWT on commissions, fees, rent paid to brokers/professionals/lessors |
| 0619-E (April) | Filed in May (10th/15th) | EWT remittance for April — credited in July 1601-EQ Item 20 |
| 0619-E (May) | Filed in June | EWT remittance for May — credited in July 1601-EQ Item 21 |
| Form 1606 | Within 10 days of month end of each sale | CWT on each property sale (filed by buyer; developer receives copy) |

### 3.2 Information Flows

```
Property Sale Transaction (Ordinary Asset):
  Buyer → withholds CWT (1.5%/3%/5%) → files Form 1606
  Buyer → issues Form 1606 copy to Developer/Seller
  Developer → reports full selling price in 2550Q Item 31 (output VAT)
  Developer → claims Form 1606 as credit on annual ITR (not on 2550Q)

Commission Payment to Broker:
  Developer → deducts 10% EWT from commission
  Developer → remits via 0619-E (months 1–2) and 1601-EQ (Q summary)
  Developer → issues Form 2307 to broker
  Broker → claims Form 2307 credit on own ITR

Government Agency Buys Property:
  Government → withholds 5% creditable VAT → files Form 1600-VT
  Government → issues Form 2307 (ATC WV010) to Developer
  Developer → enters Form 2307 in 2550Q Part V Schedule 3
  Developer → credits withheld VAT in 2550Q Part II Item 16
```

### 3.3 Key Regulatory Timeline

| Date | Event |
|---|---|
| Jan 1, 2018 | TRAIN Law: EWT rates and ATC codes updated (RR 11-2018) |
| Jan 1, 2023 | Monthly 2550M filing becomes optional; 2550Q mandatory quarterly only (RMC 05-2023) |
| Oct 3, 2023 | RMC 99-2023: clarified ordinary asset real property tax procedures; Form 2307 in lieu of Form 1606 discontinued |
| Jan 1, 2024 | EOPT Act (RA 11976) takes effect; VAT-exempt residential threshold adjusted to ₱3,600,000 |
| Apr 27, 2024 | RR 3-2024 effective: operationalizes EOPT cash-basis VAT provisions (Items 35, 36, 55, 58 on 2550Q) |
| Jun 19, 2024 | RMC 68-2024: April 2024 ENCS version of Form 2550Q released |
| Apr 7, 2025 | RMC 31-2025: Form 1606 confirmed as sole proof of CWT credit for real property ordinary asset sales |

---

## Part 4: Filing Systems

### 4.1 Electronic Filing and Payment System (eFPS)

- Mandatory for Large Taxpayers and certain top withholding agents
- File and pay within same portal
- Payment via eFPS-linked AABs (online banking)
- eFPS does not yet support Items 35, 36, 55, 58 of the April 2024 2550Q — manual PDF required for those fields

### 4.2 eBIRForms (Offline Package)

- For non-eFPS filers
- Current version: v7.9.4.2 (as of RMC 68-2024)
- Same limitation as eFPS for EOPT fields — manual PDF required for Items 35, 36, 55, 58
- Payment via: LandBank LinkBizPortal, DBP PayTax Online, UnionBank Online, Maya, MyEG, Authorized Agent Banks

### 4.3 Manual PDF Filing

- Required for taxpayers needing EOPT fields (Items 35, 36, 55, 58) on Form 2550Q
- Download from bir.gov.ph or bir-cdn.bir.gov.ph
- File at RDO or AAB under RDO jurisdiction

---

## Sources

- [BIR Official Form 2550Q (April 2024 ENCS)](https://bir-cdn.bir.gov.ph/BIR/pdf/2550Q%20%20April%202024%20ENCS_Final.pdf)
- [BIR Guidelines for Form 2550Q (April 2024)](https://bir-cdn.bir.gov.ph/BIR/pdf/2550Q%20guidelines%20April%202024_final.pdf)
- [BIR Official Form 1601-EQ (January 2019 ENCS)](https://bir-cdn.bir.gov.ph/local/pdf/1601-EQ%20January%202019%20ENCS%20final.pdf)
- [BIR eFPS Guidelines for Form 1601-EQ](https://efps.bir.gov.ph/efps-war/EFPSWeb_war/forms2018Version/1601EQ/1601eq_guidelines.html)
- [Forvis Mazars PH — RMC 68-2024 (Form 2550Q April 2024)](https://www.forvismazars.com/ph/en/insights/tax-alerts/bir-rmc-68-2024)
- [Tax and Accounting Center — How to File Form 2550Q](https://taxacctgcenter.ph/how-to-file-bir-form-2550q-quarterly-vat-return/)
- [Tax and Accounting Center — How to File Form 1601-EQ](https://taxacctgcenter.ph/how-to-file-bir-form-1601-eq/)
- [mpm.ph — BIR Form 1601EQ Guide](https://mpm.ph/bir-form-1601eq/)
- [CloudCFO — Form 2550Q April 2024 Update](https://cloudcfo.ph/blog/important-update-revised-bir-form-no-2550q-quarterly-vat-return-for-april-2024/)
- [PwC PH — Tax Alert 28 (RMC 99-2023)](https://www.pwc.com/ph/en/tax/tax-publications/tax-alerts/2023/tax-alert-28.html)
- [Ocampo & Suralvo — Ordinary Asset Real Property Taxes](https://www.ocamposuralvo.com/2023/12/22/bir-clarifies-the-applicable-taxes-due-on-sale-of-real-property-considered-as-ordinary-assets-of-the-seller/)
- [Ocampo & Suralvo — From Final to Creditable VAT Withholding](https://www.ocamposuralvo.com/2021/03/15/from-final-to-creditable-shift-of-the-vat-withholding-system-on-sales-to-the-government/)
- [Grant Thornton PH — VAT-Exempt Threshold ₱3.6M](https://www.grantthornton.com.ph/alerts-and-publications/technical-alerts/tax-alert/2024/vat-exempt-threshold-for-sale-of-house-and-lot-and-other-residential-dwellings-increased-to-p36m/)
- [Forvis Mazars PH — RMC 99-2023 Real Property](https://www.forvismazars.com/ph/en/insights/tax-alerts/bir-rmc-99-2023)
- [Tax and Accounting Center — 21 EWT Items under TRAIN](https://taxacctgcenter.ph/items-subject-expanded-withholding-tax-train-ra-10963-philippines/)
- [Taxumo — Making Sense of EWT Forms](https://www.taxumo.com/blog/making-sense-expanded-withholding-tax-forms-2307-0619e-1601eq-qap/)
- [ForeclosurePhilippines — Creditable Withholding Tax Real Estate](https://www.foreclosurephilippines.com/creditable-withholding-tax-in-real/)
- [PwC PH — Navigating VAT Recovery under EOPT Act](https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2024/navigating-vat-recovery-under-the-eopt-act.html)
- [Inquirer Business — Taxability of Ordinary Asset Real Property](https://business.inquirer.net/425418/taxability-of-sale-of-real-property-classified-as-ordinary-asset)
- [RMC 99-2023 Official PDF](https://bir-cdn.bir.gov.ph/local/pdf/RMC%20No.%2099-2023.pdf)
- [RMC 31-2025 Digest](https://bir-cdn.bir.gov.ph/BIR/pdf/RMC%20No.%2031-2025%20Digest.pdf)
