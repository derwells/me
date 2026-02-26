# Expense Tracking

**Wave:** 2 (Process Analysis & Feature Spec)
**Analyzed:** 2026-02-26
**Dependencies:** crispina-models, crispina-services, corporate-rental-tax, accounting-agency-handoff, tax-data-compilation

---

## 1. Process Description

**What:** Record all disbursements (repairs, maintenance, utilities, permits, professional fees, insurance, etc.) with proper documentation for two purposes: (1) claiming itemized deductions from gross income on BIR Form 1702, and (2) fulfilling EWT withholding agent obligations when paying suppliers and service providers.

**When:** Continuously as expenses are incurred. Monthly compilation for accountant handoff by the 5th of the following month. Quarterly aggregation for 1601-EQ and 1702Q. Annual summary for 1702-RT and AFS.

**Who does it:** Property manager records each disbursement, attaches supporting documentation, withholds EWT where applicable, and delivers the compiled expense voucher package to the external accountant.

**Frequency:** Per-transaction (each payment), with monthly/quarterly/annual compilation cycles.

---

## 2. Current Method

**Fully manual / folder-based.** The property manager:

1. Pays suppliers via check or cash
2. Collects the supplier's receipt/invoice (paper)
3. Files receipts chronologically in a physical folder
4. At month-end, delivers the folder to the accountant
5. Accountant categorizes, posts journal entries, and computes EWT

**Pain points:**
- No structured tracking of which expenses require EWT withholding
- Supplier TINs not systematically collected at payment time
- Receipts lost or misfiled — unsubstantiated expenses disallowed on audit
- No input VAT register — creditable input VAT from VAT-registered suppliers missed
- EWT obligations computed retroactively by accountant (risk of late remittance penalties)
- No check voucher numbering system — audit trail gaps
- Capital vs. ordinary expense classification done by accountant after the fact, not at recording time

---

## 3. Regulatory Rules

### 3.1 Allowable Deductions — NIRC Section 34

**Legal basis:** NIRC Section 34(A)(1)(a) as amended by RA 11976 (EOPT Act) and RA 12066 (CREATE MORE Act)

A SEC-registered rental corporation claiming itemized deductions (not OSD) must substantiate each expense. The categories relevant to a rental property corporation:

| Category | NIRC Section | Key Rules |
|---|---|---|
| **Ordinary and necessary business expenses** | 34(A)(1)(a) | Must be ordinary (normal for this business), necessary (appropriate and helpful), reasonable in amount, paid/incurred within the taxable year, directly connected to the business |
| **Interest expense** | 34(B) | Deductible if connected to trade/business. Reduced by 33% of interest income subject to final tax (for 25% RCIT corps). For 20% RCIT corps: 0% reduction (no tax arbitrage). Per RR 13-2000: not between related parties (Sec. 36(B)), not capitalized, not for petroleum ops |
| **Taxes paid** | 34(C) | Real property tax, local business tax, community tax — deductible. NOT deductible: income tax itself, estate/donor's tax, DST (debatable — some practitioners capitalize), special assessments |
| **Losses** | 34(D) | Casualty losses (fire, typhoon) not compensated by insurance. Must file with BIR within 45 days of loss occurrence |
| **Depreciation** | 34(F) | Reasonable allowance for exhaustion, wear and tear of property used in trade/business. Methods: straight-line (SLM), declining balance (DB), sum-of-years-digits, or any method agreed with CIR. No BIR-prescribed useful life schedule — taxpayer's reasonable judgment applies. Change of useful life requires BIR approval. Residual value: minimum 5% of acquisition cost per RR 19-86 (for leased assets; commonly applied as general practice) |
| **Repairs** | 34(A)(1)(a) | Ordinary repairs (maintain existing condition) = immediately deductible. Capital expenditures (enhance value or extend useful life) = must be capitalized and depreciated per Sec. 34(F) |
| **Insurance premiums** | 34(A)(1)(a) | Deductible as ordinary business expense if: insurance covers business property, premium paid within the year, policy is in force during the taxable year |
| **Professional fees** | 34(A)(1)(a) | Accounting, legal, tax advisory, property management — deductible as ordinary expenses. Subject to EWT at applicable rates |

### 3.2 Substantiation Requirements

**Legal basis:** NIRC Section 34(A)(1)(b); RA 11976 (EOPT Act); RMC 60-2024; RMC 81-2025

**The four requisites for deductibility (per BIR jurisprudence and RMC 81-2025):**
1. **Ordinary and necessary** — normal for the rental property business
2. **Paid or incurred within the taxable year** — accrual-basis corps may accrue if liability is established
3. **Directly connected** to the development, management, operation, or conduct of the trade/business
4. **Properly documented** — substantiated with sufficient evidence (official receipts, invoices, contracts, vouchers)

**Documentation requirements per expense type:**

| Expense | Required Supporting Documents |
|---|---|
| Repairs & maintenance | Supplier's BIR-registered invoice/receipt, job order or scope of work, before/after photos (best practice), check voucher |
| Utilities (Meralco, Maynilad) | Utility company statement/bill, proof of payment (OR or bank debit memo) |
| Security services | Service contract, monthly billing statement, supplier's BIR-registered invoice, check voucher |
| Janitorial/cleaning | Service contract, monthly billing, supplier's BIR-registered invoice, check voucher |
| Insurance premiums | Insurance policy, premium notice, OR from insurer |
| Real property tax | Tax declaration, RPT official receipt from LGU Treasurer's Office |
| Professional fees (CPA, lawyer) | Engagement letter or contract, billing statement, supplier's BIR-registered invoice/receipt, check voucher |
| Office supplies | Supplier's BIR-registered invoice/receipt |
| Staff salaries | Payroll register, BIR Form 2316, SSS/PhilHealth/Pag-IBIG remittance confirmations |
| Pest control | Service contract, supplier's BIR-registered invoice |
| Elevator maintenance | Service/maintenance contract, supplier's BIR-registered invoice, monthly service report |
| Fire safety equipment | Supplier's BIR-registered invoice, FSIC (Fire Safety Inspection Certificate) where applicable |
| Business permit fees | Official receipt from LGU, permit application form |
| Association dues (HOA) | Billing statement from HOA, proof of payment |

**Must the supplier's receipt be BIR-registered?**

Yes. Under NIRC Section 237 and RR 18-2012, every person engaged in business is required to issue duly registered receipts or sales invoices for each transaction. The BIR-registered invoice/receipt must bear the supplier's TIN, ATP number, and sequential numbering. Expenses supported only by acknowledgment receipts, handwritten notes, or unregistered receipts are subject to disallowance on audit. Exception: government receipts (RPT, permits) are inherently valid as they are issued by government agencies.

**What happens if an expense lacks proper documentation?**

Per BIR audit practice and RMC 81-2025: the expense is **disallowed as a deduction** from gross income. This increases taxable income and results in a deficiency income tax assessment, plus:
- 25% surcharge (NIRC Section 248)
- 12% annual interest from due date (NIRC Section 249, as amended by EOPT)
- Compromise penalty (per RMO schedule)

### 3.3 EOPT Act — Repeal of Section 34(K) Withholding Requirement

**Legal basis:** RA 11976 Section 6 (repealing Section 34(K)); RR 4-2024 Section 6; RMC 60-2024

**Old rule (pre-January 1, 2024):** If a payment was subject to EWT and the payor failed to withhold, the expense was **disallowed** as a deduction — even if otherwise properly substantiated.

**New rule (effective January 1, 2024):** Section 34(K) repealed. Non-withholding of tax is **no longer grounds for disallowance** of the claimed deduction, provided the expense is ordinary, necessary, and duly substantiated.

**Critical nuance:** The *obligation* to withhold and remit EWT still exists independently. The EOPT only decoupled withholding compliance from deductibility. The withholding agent can still be assessed for failure-to-withhold penalties (25% surcharge + 12% interest on the unremitted EWT). The expense is just no longer disallowed on the income tax side.

**Transitional rule (RMC 60-2024):** Applies only to taxable years from January 1, 2024 onward. Pre-2024 audit years: old rule applies — expenses disallowed if EWT not remitted prior to audit or submission of audit report.

### 3.4 EWT Obligations as Withholding Agent — RR 2-98 as Amended

**Legal basis:** NIRC Section 57(B); RR 2-98 Section 2.57.2, as amended by RR 11-2018, RR 7-2019, RR 31-2020, RR 5-2025, RR 24-2025

When the rental corporation pays suppliers and contractors, it acts as a **withholding agent** and must withhold EWT at the applicable rate.

#### EWT Rate Table by Expense Type

| Expense Category | Payee Type | EWT Rate | ATC (Individual) | ATC (Corporate) | Legal Basis |
|---|---|---|---|---|---|
| **Professional fees** (CPA, lawyer, engineer) | Individual, gross income ≤ P3M | 5% | WI010 | — | RR 11-2018 Sec. 2.57.2(A) |
| **Professional fees** | Individual, gross income > P3M or VAT-registered | 10% | WI011 | — | RR 11-2018 Sec. 2.57.2(A) |
| **Professional fees** | Corporation, gross income ≤ P720K | 10% | — | WC010 | RR 11-2018 Sec. 2.57.2(A) |
| **Professional fees** | Corporation, gross income > P720K | 15% | — | WC011 | RR 11-2018 Sec. 2.57.2(A) |
| **Security/janitorial/messengerial services** | Individual | 2% | WI120 | — | RR 2-98 Sec. 2.57.2(E) |
| **Security/janitorial/messengerial services** | Corporation | 2% | — | WC120 | RR 2-98 Sec. 2.57.2(E) |
| **Contractors** (repairs, maintenance, construction) | Individual | 2% | WI120 | — | RR 2-98 Sec. 2.57.2(E) |
| **Contractors** (repairs, maintenance, construction) | Corporation | 2% | — | WC120 | RR 2-98 Sec. 2.57.2(E) |
| **Rent paid** (if corp leases additional space) | Individual | 5% | WI160 | — | RR 2-98 Sec. 2.57.2(B) |
| **Rent paid** | Corporation | 5% | — | WC160 | RR 2-98 Sec. 2.57.2(B) |
| **Commissions to brokers/agents** | Individual or corporation | 10%/15% | WI010 | WC010/WC011 | RR 11-2018 Sec. 2.57.2(A) |
| **Insurance premiums** | Insurance company (non-life) | 2% | — | WC120 | RR 2-98 Sec. 2.57.2(E) |
| **TWA: purchases of goods** (if designated TWA) | Any local supplier | 1% | WI157 | WC157 | RR 11-2018 Sec. 2.57.2(I) |
| **TWA: purchases of services** (if designated TWA) | Any local supplier | 2% | WI158 | WC158 | RR 11-2018 Sec. 2.57.2(I) |

**Notes on the rate table:**
- The lower rate for professionals requires a sworn declaration from the payee (Annex B-1 for individuals, B-3 for non-individuals per RR 11-2018) plus BIR COR (Form 2303) filed by January 15 each year or before initial payment.
- EWT base: gross payment **excluding VAT** if VAT is separately stated on the invoice. For non-VAT payees, EWT is computed on the gross amount.
- Real property tax, business permits, and government fees are **NOT subject to EWT** — these are paid to government entities, not private payees.
- Utility bills (Meralco, Maynilad) paid directly to the utility company: **NOT subject to EWT** under RR 2-98 (utility companies are already under the final withholding tax system for their own income).

#### Payee Sworn Declaration Tracking

For professional fee payees, the system must track:
- Whether payee has filed a sworn declaration (Annex B-1/B-3)
- Payee's gross income bracket (determines 5%/10% for individuals, 10%/15% for corps)
- BIR COR (Form 2303) on file
- Default to higher rate if no declaration received

#### Form 2307 Issuance to Payees

**Legal basis:** RR 2-98 Section 2.58

The rental corporation, as withholding agent, must issue **BIR Form 2307** (Certificate of Creditable Tax Withheld at Source) to each payee:

| Requirement | Detail |
|---|---|
| **Issuance deadline** | Within 20 days after the close of the taxable quarter |
| **Frequency** | Quarterly (per taxable quarter in which payments were made) |
| **Content** | Payor TIN/name, payee TIN/name, ATC, nature of income, quarter, gross payment, EWT withheld |
| **Copies** | Original to payee; duplicate retained by withholding agent; triplicate to BIR (via QAP) |

**Practical implication:** The system must generate 2307 data per payee per quarter, ready for printing on BIR Form 2307 blanks or electronic filing.

#### Withholding Agent Filing Obligations

| BIR Form | Purpose | Frequency | Deadline |
|---|---|---|---|
| **0619-E** | Monthly remittance of EWT withheld | Monthly (1st and 2nd month of each quarter) | 10th of following month (eFPS: 15th) |
| **1601-EQ** | Quarterly EWT return + QAP (Quarterly Alphalist of Payees) | Quarterly (3rd month of each quarter) | Last day of month following quarter-end |
| **1604-E** | Annual information return of EWT withheld + Annual Alphalist | Annual | March 1 (or February 28/29) |

**0619-E and 1601-EQ interaction:** Monthly forms cover the first 2 months of each quarter. The 1601-EQ covers the entire quarter (3 months). Monthly payments (0619-E) are credited against the quarterly total (1601-EQ), so only the incremental 3rd-month amount is paid with 1601-EQ.

**QAP (Quarterly Alphalist of Payees):** DAT file generated via BIR Alphalist Data Entry module, submitted via esubmission@bir.gov.ph. Per-payee fields: TIN, registered name, ATC, gross income payment, tax withheld.

### 3.5 Input VAT on Purchases — NIRC Section 110

**Legal basis:** NIRC Section 110(A) and (B), as amended by RA 10963 (TRAIN Law); RR 13-2018; RMC 21-2022

#### Which Expenses Generate Creditable Input VAT?

Input VAT is creditable **only** from purchases supported by a **VAT-registered supplier's invoice** (not OR, per RR 7-2024) showing the supplier's TIN-V (VAT registration indicator) and a separate VAT line item.

| Expense | Input VAT Creditable? | Condition |
|---|---|---|
| Building repairs/maintenance (from VAT-registered contractor) | **Yes** | Supplier must be VAT-registered; invoice shows 12% VAT |
| Security services (from VAT-registered agency) | **Yes** | Same |
| Janitorial services (from VAT-registered agency) | **Yes** | Same |
| Professional fees (from VAT-registered CPA/lawyer) | **Yes** | Same |
| Insurance premiums (from VAT-registered insurer) | **Yes** | Same |
| Office supplies (from VAT-registered retailer) | **Yes** | Same |
| Elevator maintenance (from VAT-registered contractor) | **Yes** | Same |
| Pest control (from VAT-registered provider) | **Yes** | Same |
| Fire safety equipment (from VAT-registered supplier) | **Yes** | Same |
| Real property tax (government) | **No** | Government — not a VAT transaction |
| Business permit fees (government) | **No** | Government — not a VAT transaction |
| Utility bills (Meralco, Maynilad) | **Yes** | Utility companies are VAT-registered; VAT is shown on their bills |
| Association dues (to HOA) | **Depends** | Only if the HOA is VAT-registered and issues a VAT invoice |
| Purchases from non-VAT suppliers | **No** | No VAT was charged; nothing to credit |
| Staff salaries | **No** | Not a sale of goods/services subject to VAT |

**Crediting mechanism:** Input VAT is credited against **output VAT** on the quarterly 2550Q return. If input VAT exceeds output VAT, the excess carries forward to the next quarter.

#### Capital Goods Input VAT — Amortization Sunset Confirmed

**Legal basis:** NIRC Section 110(A)(1) as amended by RA 10963 Section 35; RMC 21-2022

**Pre-January 1, 2022:** Input VAT on capital goods exceeding P1,000,000 aggregate acquisition cost (excluding VAT) in a calendar month was amortized over 60 months (or the asset's shorter useful life).

**Post-January 1, 2022 (TRAIN phase-in sunset):** The 60-month amortization requirement **CEASED**. All input VAT on capital goods purchased on or after January 1, 2022 is recognized **outright** in the month/quarter of purchase. No amortization schedule required.

**Transitional:** Taxpayers with unamortized input VAT from pre-2022 capital goods continue amortizing as scheduled until fully utilized.

**Practical impact for a rental corporation:** Major building renovations or equipment purchases in 2022 onward generate full input VAT credit immediately — a significant cash flow benefit compared to the prior 5-year spread.

### 3.6 Depreciation Rules

**Legal basis:** NIRC Section 34(F); RR 19-86 (leasing transactions); RMC 70-2010 (depreciation basis)

**Methods allowed:**
- Straight-Line Method (SLM) — most common for rental property
- Declining Balance (DB)
- Sum-of-Years-Digits (SYD)
- Any other method agreed with the CIR

**Useful life:** Philippine tax law does **not** prescribe mandatory useful life periods by asset class (unlike US MACRS). The taxpayer exercises reasonable judgment. Common practice for rental property:

| Asset Class | Common Useful Life | Basis |
|---|---|---|
| Reinforced concrete building | 20-30 years | Industry practice; no BIR mandate |
| Building improvements / renovations | 5-10 years | Shorter of improvement's useful life or remaining building life |
| Elevator/escalator | 15-20 years | Manufacturer guidance |
| Electrical/plumbing systems | 10-15 years | Engineering estimates |
| Office furniture and equipment | 5-10 years | Industry practice |
| Computer equipment | 3-5 years | Industry practice |
| Motor vehicles | 5 years | Common practice |
| Fire safety equipment | 5-10 years | Industry practice |

**Residual value:** Per RR 19-86 Section 4.03, the residual value shall be not less than **5% of the lessor's acquisition cost** of the leased asset. While RR 19-86 technically applies to leasing transactions, this 5% floor is commonly applied as general practice.

**Depreciation basis:** Acquisition cost only — NOT reappraised value (Supreme Court: *Basilan Estates, Inc. v. CIR*). Per RMC 70-2010, impairment adjustments do not affect the tax depreciation basis.

**Capital vs. ordinary repair distinction:**

| Factor | Ordinary Repair (Deductible) | Capital Expenditure (Capitalize + Depreciate) |
|---|---|---|
| Purpose | Restore to original condition | Enhance value or extend useful life |
| Effect | Maintains current utility | Adds new capability or prolongs life |
| Examples | Repainting, fixing leaks, replacing broken tiles, rewiring a single outlet | New roof, elevator installation, building extension, HVAC system |
| Tax treatment | Full deduction in year paid/incurred (Sec. 34(A)(1)(a)) | Added to asset cost, depreciated over useful life (Sec. 34(F)) |
| Test | "Would the building function the same without this work?" If yes → ordinary repair | "Does this add something new or make it last significantly longer?" If yes → capital expenditure |

### 3.7 Specific Deduction Rules for Common Rental Property Expenses

#### Interest Expense — NIRC Section 34(B)

**The 33% interest arbitrage reduction (RMC 19-2024):**

```
Deductible Interest = Interest Paid − (33% × Interest Income Subject to Final Tax)
```

**Exception for 20% RCIT corporations:** If the corp qualifies for the 20% RCIT rate (net taxable income ≤ P5M AND total assets ≤ P100M), the reduction is **0%** because the RCIT rate equals the final tax rate on interest income (20%). No arbitrage exists.

**Conditions per RR 13-2000:**
1. Indebtedness must be connected to trade/business
2. Not between related taxpayers (Sec. 36(B))
3. Not incurred for petroleum operations
4. Not elected to be treated as capital expenditure
5. Supported by loan agreement, bank statements, and official receipts for interest paid

#### Real Property Tax — NIRC Section 34(C)

Deductible in the year paid (not accrued). Supported by: tax declaration + RPT Official Receipt from City Treasurer's Office. Las Pinas City RPT rate: 2% for commercial, 1% for residential (per Local Government Code Section 233).

**Not subject to EWT** — paid to LGU, not a private payee.

#### Insurance Premiums — NIRC Section 34(A)(1)(a)

Deductible if: covers business property (building, CGL), paid within the taxable year, policy in force during the year. Multi-year premiums prorated: only the current-year portion is deductible.

Subject to **2% EWT** (WC120) when paid to a non-life insurance company.

### 3.8 Check Voucher / Disbursement Voucher Requirements

**Legal basis:** NIRC Section 232 (books of accounts); RR 9-2009 (record-keeping); COA Circular 92-389 (government DV — used as best-practice reference for private corporations)

**BIR-prescribed format?** No. The BIR does **not** prescribe a specific disbursement voucher format for private corporations. The requirement is to maintain adequate books of accounts with supporting documentation. However, best practice (and what auditors expect) follows the COA DV format adapted for private sector use.

**Recommended fields for a check/disbursement voucher:**

| Field | Purpose |
|---|---|
| **Voucher Number** | Sequential, gapless — audit trail |
| **Date** | Date voucher is prepared |
| **Payee Name** | Full registered name of supplier/contractor |
| **Payee TIN** | Required for EWT (2307 issuance) and expense substantiation |
| **Payee Address** | For 2307 and alphalist |
| **Particulars / Description** | Nature of expense: "Repair of 2nd floor plumbing — Unit 205" |
| **Account Code / Category** | Chart of accounts classification (repairs, professional fees, etc.) |
| **Amount (Gross)** | Total amount per supplier invoice |
| **VAT Amount** | Input VAT component (if from VAT-registered supplier) |
| **EWT Rate and Amount** | Applicable EWT withheld |
| **ATC Code** | For 0619-E / 1601-EQ / 2307 filing |
| **Net Amount Payable** | Gross − EWT withheld |
| **Mode of Payment** | Check / bank transfer / cash |
| **Check Number / Reference** | For bank reconciliation |
| **Bank Account** | Which corporate bank account |
| **Supporting Documents** | List of attached receipts/invoices |
| **Prepared By** | Property manager or staff |
| **Approved By** | Authorized signatory (per board resolution) |
| **Received By** | Payee acknowledgment + date |

#### Cash vs. Check Payment Threshold

**Old rule — NIRC Section 34(A)(1)(b):** Payments exceeding **P1,000** were historically required to be made by check for the expense to qualify as a deductible expense.

**Current status (post-EOPT Act, RA 11976):** The EOPT Act modernized substantiation requirements, focusing on proper documentation rather than mode of payment. However, the prudent practice remains:

- **Petty cash fund:** Payments up to a set threshold (commonly P1,000-P5,000 per company policy) for minor/routine items
- **Check or bank transfer:** All payments above the petty cash threshold — creates a bank-verified audit trail
- **Best practice:** Use checks for ALL supplier payments subject to EWT, regardless of amount. The cancelled check + voucher + receipt creates a triple-layered audit trail that the BIR expects.

**No statutory prohibition** on cash payments above P1,000 under the current framework, but cash payments are harder to substantiate on audit. The BIR may question the legitimacy of large cash payments lacking a bank paper trail.

---

## 4. What Crispina Built

**Nothing.** The Crispina codebase has **no expense-related models, schemas, or endpoints**. There is:
- No `Expense` or `Disbursement` table
- No `Supplier` or `Payee` table
- No `CheckVoucher` table
- No `InputVAT` register
- No `EWTWithheld` tracking
- No chart of accounts or expense categorization

The entire expense side of the business was out of scope for Crispina's initial build, which focused exclusively on the revenue side (rent billing, payment collection, tenant management).

The `tax-data-compilation` analysis identified the need for `SupplierPayee`, `ExpenseVoucher`, and `InputVATRegister` models — this analysis provides the detailed specification for those.

---

## 5. Edge Cases and Special Rules

### 5.1 Mixed VAT-Exempt and VATable Operations — Input VAT Apportionment

**Legal basis:** NIRC Section 110(A)(1); RR 16-2005 Section 4.110-5

If the rental corporation has both VATable income (commercial rents) and VAT-exempt income (residential rents ≤ P15,000/month), input VAT on **common expenses** (e.g., building insurance covering both commercial and residential units) must be **apportioned**:

```
Creditable Input VAT = Total Input VAT × (VATable Sales / Total Sales)
```

Only the portion attributable to VATable operations is creditable. The non-creditable portion becomes part of the cost/expense (added to the deductible amount for income tax purposes).

**Direct attribution first:** If an expense is directly attributable to a specific income stream (e.g., repair of a specific commercial unit), the full input VAT is creditable (or not) based on that unit's VAT status. Apportionment applies only to shared/common expenses.

### 5.2 Expense Disallowance for Passive Income Linkage

**Legal basis:** RMC 81-2025

The BIR has clarified that **only expenses directly tied to the generation of active income** may be deducted. Expenses related to passive income (e.g., interest income, dividend income) are NOT deductible against gross business income. For a rental corporation, rental income is generally classified as **active income** (the corporation actively manages properties), so this distinction primarily affects interest expense (see Section 3.7 above re: interest arbitrage).

### 5.3 Related Party Transactions

**Legal basis:** NIRC Section 36(B); RR 2-98 Section 2.58

Interest expense between related parties is non-deductible. Professional fees paid to directors or shareholders must be at arm's length. Management fees paid to a related management company are subject to transfer pricing scrutiny.

### 5.4 Timing: Cash vs. Accrual Method

The rental corporation likely operates on **accrual basis** (standard for corporations in the Philippines). Under accrual:
- Expenses are deductible when **all events have occurred to establish the fact of liability** and the amount can be determined with reasonable accuracy
- Not when actually paid (that's cash basis)
- However, EWT must be withheld at the time income has become **payable** (Sec. 57, as amended by EOPT)

### 5.5 Year-End Accruals

Accrued expenses at year-end (e.g., December professional fees billed in January) are deductible in the year accrued, provided:
1. All events establishing liability have occurred by December 31
2. Amount is determinable with reasonable accuracy
3. Economic performance has occurred (service rendered)

---

## 6. Lightweight Feature Spec

### 6.1 New Data Models

```
SupplierPayee
├── pk (UUID)
├── name (String 255)                    -- Registered business name
├── tin (String 20)                      -- BIR TIN (for 2307 issuance)
├── address (String 500)                 -- Registered address (for 2307)
├── supplier_type (Enum)                 -- INDIVIDUAL / CORPORATION
├── is_vat_registered (Boolean)          -- Determines input VAT creditability
├── professional_gross_income_bracket    -- BELOW_3M / ABOVE_3M (individuals)
│                                           BELOW_720K / ABOVE_720K (corps)
├── has_sworn_declaration (Boolean)      -- Annex B-1/B-3 on file
├── sworn_declaration_year (Integer)     -- Year of latest declaration
├── bir_cor_on_file (Boolean)            -- Form 2303 received
├── default_ewt_rate (Decimal)           -- Pre-computed from type + bracket
├── default_atc_code (String 10)         -- Pre-computed ATC
├── default_expense_category (Enum)      -- PROFESSIONAL_FEE / CONTRACTOR / etc.
├── contact_person (String 255)
├── contact_number (String 50)
├── notes (Text)
├── is_active (Boolean, default True)
└── created_at, last_updated_at

ExpenseCategory (Enum or lookup table)
├── REPAIRS_AND_MAINTENANCE
├── PROFESSIONAL_FEES
├── SECURITY_SERVICES
├── JANITORIAL_SERVICES
├── INSURANCE_PREMIUMS
├── REAL_PROPERTY_TAX
├── BUSINESS_PERMITS
├── OFFICE_SUPPLIES
├── UTILITIES_ELECTRIC
├── UTILITIES_WATER
├── STAFF_SALARIES
├── PEST_CONTROL
├── ELEVATOR_MAINTENANCE
├── FIRE_SAFETY
├── ASSOCIATION_DUES
├── INTEREST_EXPENSE
├── DEPRECIATION  (system-generated, not manual voucher)
├── MISCELLANEOUS
└── (extensible)

DisbursementVoucher
├── pk (UUID)
├── voucher_number (String 20, unique)   -- Sequential, gapless (e.g., DV-2026-0001)
├── date_prepared (Date)
├── date_paid (Date, nullable)           -- Actual payment date (may differ from prepared)
├── supplier_payee_pk (FK → SupplierPayee)
├── property_pk (FK → Property, nullable) -- Which property this expense relates to
├── expense_category (Enum)              -- From ExpenseCategory
├── is_capital_expenditure (Boolean)     -- If true, capitalize; if false, expense
├── description (Text)                   -- Detailed nature of expense
├── gross_amount (CurrencyDecimal)       -- Total per supplier invoice
├── vat_amount (CurrencyDecimal)         -- Input VAT component (0 if non-VAT supplier)
├── ewt_rate (PercentageDecimal)         -- Applicable EWT rate
├── ewt_amount (CurrencyDecimal)         -- Computed: gross_amount × ewt_rate (excl. VAT)
├── net_payable (CurrencyDecimal)        -- gross_amount − ewt_amount
├── atc_code (String 10)                 -- ATC for 0619-E / 1601-EQ / 2307
├── payment_mode (Enum)                  -- CHECK / BANK_TRANSFER / CASH / PETTY_CASH
├── check_number (String 50, nullable)
├── bank_account (String 100, nullable)
├── status (Enum)                        -- DRAFT / APPROVED / PAID / VOIDED
├── supporting_docs (JSONB)              -- List of attached document references
├── approved_by (String 255, nullable)
├── prepared_by (String 255)
├── remarks (Text, nullable)
├── vat_creditable (Boolean)             -- Is this input VAT creditable?
├── vat_apportionment_pct (PercentageDecimal, nullable)
│                                        -- If mixed operations, portion creditable
└── created_at, last_updated_at

InputVATRegister (view or materialized from DisbursementVoucher)
├── period (Month/Quarter)
├── supplier_tin
├── supplier_name
├── invoice_number
├── invoice_date
├── gross_purchase
├── input_vat
├── is_creditable (Boolean)
├── creditable_amount
├── non_creditable_amount (becomes part of expense)
└── capital_goods_flag (Boolean)

EWTWithheldRegister (view or materialized from DisbursementVoucher)
├── period (Month/Quarter)
├── payee_tin
├── payee_name
├── atc_code
├── gross_payment
├── ewt_rate
├── ewt_amount
├── voucher_number
├── form_2307_generated (Boolean)
├── form_2307_issued_date (Date, nullable)
└── form_2307_received_by_payee (Boolean)

FixedAssetRegister
├── pk (UUID)
├── asset_description (String 500)
├── property_pk (FK → Property)          -- Which property
├── date_acquired (Date)
├── acquisition_cost (CurrencyDecimal)
├── residual_value (CurrencyDecimal)     -- Minimum 5% of acquisition cost
├── useful_life_months (Integer)
├── depreciation_method (Enum)           -- SLM / DB / SYD / OTHER
├── accumulated_depreciation (CurrencyDecimal)
├── net_book_value (CurrencyDecimal)     -- Computed: cost − accum. depr.
├── asset_class (Enum)                   -- BUILDING / IMPROVEMENT / EQUIPMENT / VEHICLE / etc.
├── is_active (Boolean)
├── disposal_date (Date, nullable)
├── disposal_proceeds (CurrencyDecimal, nullable)
├── gain_loss_on_disposal (CurrencyDecimal, nullable)
├── source_voucher_pk (FK → DisbursementVoucher, nullable) -- Links capital expenditure
└── created_at, last_updated_at

DepreciationScheduleEntry
├── pk (UUID)
├── fixed_asset_pk (FK → FixedAssetRegister)
├── period (Date — month/year)
├── depreciation_amount (CurrencyDecimal)
├── accumulated_total (CurrencyDecimal)
├── remaining_book_value (CurrencyDecimal)
└── is_posted (Boolean)
```

### 6.2 Core Logic

#### Voucher Numbering
```
Pattern: DV-{YYYY}-{NNNN}
Sequential per calendar year, gapless
Reset counter each January 1
Atomic increment (DB sequence)
```

#### EWT Auto-Computation
```python
def compute_ewt(voucher):
    supplier = voucher.supplier_payee

    # Government payees: no EWT
    if supplier.supplier_type == 'GOVERNMENT':
        return 0, None

    # Utilities paid directly: no EWT
    if voucher.expense_category in ['UTILITIES_ELECTRIC', 'UTILITIES_WATER']:
        return 0, None

    # EWT base: gross amount EXCLUDING VAT
    ewt_base = voucher.gross_amount - voucher.vat_amount

    # Rate from supplier profile (pre-computed from type + bracket)
    rate = supplier.default_ewt_rate
    atc = supplier.default_atc_code

    ewt_amount = round(ewt_base * rate, 2)
    return ewt_amount, atc
```

#### Input VAT Creditability Check
```python
def check_input_vat(voucher):
    supplier = voucher.supplier_payee

    # Non-VAT supplier: no input VAT
    if not supplier.is_vat_registered:
        return 0, False

    # Government: no VAT
    if voucher.expense_category in ['REAL_PROPERTY_TAX', 'BUSINESS_PERMITS']:
        return 0, False

    # Salaries: not a sale of goods/services
    if voucher.expense_category == 'STAFF_SALARIES':
        return 0, False

    # If corp has mixed operations (VATable + exempt):
    if has_mixed_operations():
        # Direct attribution first
        if voucher.property_pk and is_directly_attributable(voucher):
            pct = 1.0 if is_vatable_unit(voucher) else 0.0
        else:
            pct = vatable_sales_ratio()  # VATable / Total for the quarter

        creditable = voucher.vat_amount * pct
        return creditable, True

    # Pure VATable operations: full credit
    return voucher.vat_amount, True
```

#### Capital vs. Ordinary Classification
```
User selects is_capital_expenditure on voucher entry.
System enforces:
  - If is_capital_expenditure = True:
      - Creates FixedAssetRegister entry
      - Generates DepreciationScheduleEntry records
      - Expense NOT included in current-year deductions
  - If is_capital_expenditure = False:
      - Full amount included as deductible expense
      - No depreciation schedule
  - Accountant reviews classification monthly
```

### 6.3 Reports Generated

| Report | Frequency | Consumer | Format |
|---|---|---|---|
| **Expense Voucher Register** | Monthly | Accountant | Excel — all vouchers for the period, sorted by date |
| **Input VAT Register** | Quarterly | Accountant (for 2550Q) | Excel — creditable input VAT by supplier |
| **EWT Withheld Summary** | Monthly/Quarterly | Accountant (for 0619-E / 1601-EQ) | Excel — grouped by ATC code |
| **Form 2307 Data** | Quarterly | Payees (suppliers) | Print-ready 2307 per payee per quarter |
| **QAP Data** | Quarterly | Accountant (for 1601-EQ attachment) | DAT file per BIR Alphalist Data Entry format |
| **Annual Alphalist** | Annual | Accountant (for 1604-E) | DAT file — full year payee summary |
| **Fixed Asset Schedule** | Annual | Accountant (for AFS) | Excel — beginning balance, additions, disposals, depreciation, NBV |
| **Depreciation Schedule** | Monthly | Accountant (for journal entries) | Excel — monthly depreciation by asset |
| **Expense Summary by Category** | Monthly/Annual | Management, accountant | Excel — grouped by expense category with totals |

### 6.4 Workflow

```
1. RECORD: Property manager enters disbursement voucher
   - Selects supplier (auto-fills TIN, EWT rate, ATC)
   - Enters amount, attaches receipt photo/scan
   - System auto-computes: VAT amount, EWT amount, net payable
   - System flags: capital vs. ordinary (default from category, overridable)
   - Status: DRAFT

2. APPROVE: Authorized person reviews and approves
   - Checks: receipt attached, amount matches invoice, correct category
   - Status: APPROVED

3. PAY: Treasury/manager issues check or bank transfer
   - Records check number / transfer reference
   - Status: PAID
   - Date_paid populated

4. COMPILE: Monthly batch
   - System generates: expense register, input VAT register, EWT summary
   - Exports to accountant by 5th of following month

5. QUARTERLY:
   - System generates: QAP data, Form 2307 per payee
   - EWT summary by ATC for 1601-EQ
   - Input VAT summary for 2550Q

6. ANNUAL:
   - System generates: annual alphalist (1604-E), fixed asset schedule, depreciation summary
   - All data feeds into accountant's preparation of 1702-RT and AFS
```

---

## 7. Common Expense Categories for a Las Pinas Rental Property Corporation

| # | Expense Category | Typical Frequency | EWT Applicable? | EWT Rate / ATC | Input VAT? | Capital or Ordinary? | Substantiation |
|---|---|---|---|---|---|---|---|
| 1 | Building repairs & maintenance | As needed | Yes (contractor) | 2% / WC120 | Yes (if VAT supplier) | Ordinary (unless extends life) | Contractor invoice + job order |
| 2 | Common area utilities — electricity | Monthly | No (utility co.) | N/A | Yes (Meralco VAT) | Ordinary | Meralco bill + payment proof |
| 3 | Common area utilities — water | Monthly | No (utility co.) | N/A | Yes (Maynilad VAT) | Ordinary | Maynilad bill + payment proof |
| 4 | Security services | Monthly | Yes | 2% / WC120 | Yes (if VAT agency) | Ordinary | Contract + monthly invoice |
| 5 | Janitorial/cleaning | Monthly | Yes | 2% / WC120 | Yes (if VAT agency) | Ordinary | Contract + monthly invoice |
| 6 | Insurance — building | Annual | Yes | 2% / WC120 | Yes (if VAT insurer) | Ordinary | Policy + premium OR |
| 7 | Insurance — CGL | Annual | Yes | 2% / WC120 | Yes (if VAT insurer) | Ordinary | Policy + premium OR |
| 8 | Real property tax | Annual/Quarterly | No (government) | N/A | No | Ordinary | RPT OR from City Treasurer |
| 9 | Business permit renewal | Annual | No (government) | N/A | No | Ordinary | LGU OR + permit |
| 10 | Professional fees — accountant | Monthly/Quarterly | Yes | 10-15% / WC010-WC011 (corp) or 5-10% / WI010-WI011 (indiv) | Yes (if VAT) | Ordinary | Engagement letter + invoice |
| 11 | Professional fees — lawyer | As needed | Yes | Same as accountant | Yes (if VAT) | Ordinary | Engagement letter + invoice |
| 12 | Office supplies | As needed | No (unless TWA) | N/A (or 1% WC157 if TWA) | Yes (if VAT supplier) | Ordinary | Supplier invoice |
| 13 | Property management staff salaries | Semi-monthly | N/A (compensation) | Withholding on comp | No | Ordinary | Payroll register + BIR 2316 |
| 14 | Pest control | Monthly/Quarterly | Yes | 2% / WC120 | Yes (if VAT) | Ordinary | Contract + invoice |
| 15 | Elevator maintenance | Monthly | Yes | 2% / WC120 | Yes (if VAT) | Ordinary (routine); Capital (major overhaul) | Contract + service report + invoice |
| 16 | Fire safety equipment | Annual/As needed | Yes | 2% / WC120 | Yes (if VAT) | Capital (new equipment); Ordinary (refills/inspections) | Invoice + FSIC |
| 17 | Association/HOA dues | Monthly | Depends | Depends on HOA status | Depends on HOA VAT status | Ordinary | HOA billing + payment proof |

---

## 8. Automability Score

**Score: 4/5**

**Justification:**
- **Deterministic (automatable):** Voucher numbering, EWT auto-computation from supplier profile, input VAT creditability check, net payable calculation, report generation (expense register, QAP, 2307), depreciation schedule computation, filing deadline alerts
- **Requires human judgment:** Capital vs. ordinary expense classification (borderline cases), supplier TIN verification and sworn declaration collection, reasonableness of expense amounts, approval workflow, new supplier onboarding, receipt verification (matching invoice to actual delivery of goods/services), VAT apportionment ratio determination

---

## 9. Verification Status

| Rule | Sources | Status |
|---|---|---|
| NIRC Section 34 deduction categories | NIRC text (chanrobles.com), PWC Philippines, taxacctgcenter.ph, unicapital-inc.com | **Confirmed** |
| Four requisites for deductibility | RMC 81-2025 (bir-cdn.bir.gov.ph), Grant Thornton PH, accountaholicsph.com | **Confirmed** |
| EOPT repeal of Section 34(K) | RA 11976 text, RR 4-2024, RMC 60-2024, PWC PH, KPMG PH, Forvis Mazars PH | **Confirmed** |
| EWT rates by expense type (RR 11-2018) | RR 2-98/11-2018 (bir.gov.ph), Forvis Mazars PH, tripleiconsulting.com, n-pax.com | **Confirmed** |
| Form 2307 issuance timeline (20 days after quarter) | RR 2-98 Section 2.58, taxumo.com, omnihr.co, getthera.com | **Confirmed** |
| 0619-E / 1601-EQ / 1604-E filing requirements | BIR Form instructions, efps.bir.gov.ph, taxacctgcenter.ph, mpm.ph | **Confirmed** |
| Input VAT crediting rules (NIRC Section 110) | NIRC text, Grant Thornton PH, Forvis Mazars PH, Dumlao & Co. | **Confirmed** |
| Capital goods 60-month amortization sunset Jan 1, 2022 | TRAIN Law (RA 10963) Section 35, RMC 21-2022, PWC PH Tax Alert 10/2022 | **Confirmed** |
| 33% interest arbitrage reduction (RMC 19-2024) | RMC 19-2024 (bir-cdn.bir.gov.ph), Grant Thornton PH, SunStar, gppcpas.com.ph | **Confirmed** |
| No BIR-prescribed useful life schedule | taxacctgcenter.ph, mpca.com.ph, Grant Thornton PH, PWC Philippines | **Confirmed** |
| 5% residual value floor (RR 19-86) | Scribd (BIR Rulings on Useful Life), mpca.com.ph | **Confirmed** — though technically applies to leasing transactions, widely applied as general practice |
| Cash vs. check payment threshold (old P1,000 rule) | NIRC Section 34(A)(1)(b), EOPT Act commentary | **Confirmed** — threshold exists in statute; EOPT modernized substantiation focus |
| No BIR-prescribed DV format for private corps | COA circular references, BIR form listing | **Confirmed** — BIR prescribes books of accounts, not voucher format |

**Source conflicts documented:** None for this analysis. All rules cross-verified against 2+ independent sources.

---

## Key Citations Summary

| Citation | Subject |
|---|---|
| **NIRC Section 34(A)(1)(a)** | Ordinary and necessary business expenses |
| **NIRC Section 34(A)(1)(b)** | Substantiation requirement; check payment rule |
| **NIRC Section 34(B)** | Interest expense deduction |
| **NIRC Section 34(C)** | Taxes paid (RPT, local taxes) |
| **NIRC Section 34(F)** | Depreciation allowance |
| **NIRC Section 57(B)** | Obligation to withhold EWT |
| **NIRC Section 110(A)(1)** | Input VAT on purchases / capital goods |
| **NIRC Section 232** | Books of accounts requirement |
| **NIRC Section 237** | Invoice/receipt issuance requirement |
| **RA 11976 (EOPT Act)** | Repeal of Sec. 34(K); modernized substantiation |
| **RA 10963 (TRAIN Law)** | Capital goods input VAT amortization sunset |
| **RA 12066 (CREATE MORE Act)** | 20% RCIT for qualifying corps; interest arbitrage |
| **RR 2-98** | EWT rates and withholding agent obligations |
| **RR 11-2018** | Amended EWT rates (professional fees tiers) |
| **RR 5-2025** | Latest EWT rate amendments (CREATE MORE) |
| **RR 13-2000** | Interest expense deduction implementation |
| **RR 19-86** | Leasing transaction rules; 5% residual value |
| **RR 7-2024** | VAT Invoice as primary document (EOPT implementation) |
| **RMC 19-2024** | Interest expense/arbitrage clarification |
| **RMC 21-2022** | Capital goods input VAT — outright claim post-2022 |
| **RMC 60-2024** | Sec. 34(K) repeal applies from Jan 1, 2024 only |
| **RMC 70-2010** | Depreciation basis = acquisition cost only |
| **RMC 81-2025** | Deductibility: active income expenses only |
