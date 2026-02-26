# Tax Data Compilation

**Wave:** 2 (Process Analysis & Feature Spec)
**Analyzed:** 2026-02-26
**Dependencies:** crispina-models, crispina-services, corporate-rental-tax, accounting-agency-handoff, rent-roll-preparation, monthly-billing-generation, tenant-payment-tracking, lease-contract-generation

---

## 1. Process Description

**What:** Prepare structured data packages for BIR quarterly and annual filings. This is NOT the filing itself (that's the external accountant's job), but the systematic compilation of raw data from operations into formats the accountant can directly use. Six distinct data compilation sub-processes:

| Sub-Process | BIR Form(s) Fed | Role | Frequency |
|---|---|---|---|
| Output VAT summary | 2550Q | Taxpayer | Quarterly |
| Income tax data | 1702Q / 1702-RT | Taxpayer | Quarterly / Annual |
| SAWT from received 2307s | Attachment to 1702Q, 2550Q | Tax credit recipient | Quarterly |
| EWT withheld on suppliers | 0619-E, 1601-EQ, 1604-E | Withholding agent | Monthly / Quarterly / Annual |
| DST register | 2000 | Taxpayer | Per-event (lease execution) |
| 2307 tracking & reconciliation | SAWT → 1702Q | Tax credit claimant | Quarterly |

**When:** Monthly data accumulates; compilation runs at quarter-end and year-end. Specific deadlines drive the urgency:

| Compilation | Deadline Trigger |
|---|---|
| Output VAT (2550Q) | 25th of month after quarter-end |
| Income tax (1702Q) | 60th day after quarter-end (~May 30, Aug 29, Nov 29) |
| EWT remittance (0619-E) | 10th of following month (first 2 months of quarter) |
| EWT return (1601-EQ) | Last day of month after quarter-end |
| DST (Form 2000) | Within 5 days after close of month of lease execution |
| Annual EWT (1604-E) | March 1 |
| Annual ITR (1702-RT) | April 15 |

**Who does it:** Property manager compiles raw data; delivers to external accountant who uses it to file returns.

**Frequency:** Continuous accumulation; quarterly and annual compilation events.

---

## 2. Current Method

**Mostly manual / spreadsheet-based.** The property manager:

1. **Monthly**: Tallies rental collections in a ledger or spreadsheet. Files away supplier receipts in a folder.
2. **Quarterly**: Manually aggregates 3 months of data. Gathers 2307 certificates from corporate tenants (physically — paper documents). Compiles an ad hoc list of supplier payments subject to EWT. Delivers the physical bundle to the accountant.
3. **Annually**: Accountant requests missing data — back-and-forth over phone/email to fill gaps.

**Pain points:**
- No systematic 2307 tracking — certificates lost or received late without follow-up
- Supplier EWT data compiled at quarter-end instead of recorded at payment time
- DST obligations sometimes missed for lease renewals (not systematically tracked)
- VAT-exempt vs. VATable split not pre-computed — accountant must re-derive from unit types
- No structured input VAT tracking — supplier receipts in a folder, not a register
- SAWT data preparation is entirely manual — accountant re-keys 2307 data into BIR module
- Missing or delayed data causes late filing penalties (25% surcharge + 12% annual interest)

---

## 3. Regulatory Rules

### 3.1 Quarterly VAT Return — 2550Q

**Legal basis:** NIRC Sec. 114; RR 16-2005 (consolidated VAT regs); RR 3-2024 (EOPT implementing rules); RR 7-2024 (invoice reform)

**What the accountant needs from the property manager:**

| Data Point | Source | Notes |
|---|---|---|
| Total VATable sales (gross rent excl. VAT) | Billing/Invoice log | Commercial + residential > PHP 15K/mo |
| Total VAT-exempt sales | Billing/Invoice log | Residential ≤ PHP 15K/mo (NIRC Sec. 109(1)(Q)) |
| Total output VAT collected/accrued | 12% × VATable sales | Declared at INVOICE issuance (accrual), not payment receipt |
| Total creditable input VAT | Supplier invoice register | From VAT-registered suppliers only |
| Input VAT on capital goods (> PHP 1M) | Capital expenditure register | Amortized over 60 months (NIRC Sec. 110(A)) |
| Carry-forward input VAT | Prior quarter 2550Q | Excess input over output carried forward |
| Uncollected receivables adjustment | Aging report | Under RR 3-2024: if invoice not collected within agreed credit term, output VAT deductible from NEXT quarter's return (one-quarter claim window) |

**Key rule — accrual basis (RR 3-2024):** Output VAT is declared when the invoice is issued (i.e., when rent becomes due), NOT when payment is collected. This means VAT liability arises at billing, and the uncollected receivables adjustment is the mechanism for relief if the tenant doesn't pay.

**Key rule — uncollected receivables (RR 3-2024 + RMC 65-2024):** If a billed invoice remains uncollected past the credit term, the lessor may claim back the output VAT in the immediately following quarter's 2550Q. The claim window is ONE quarter only. **Eight requisites per RMC 65-2024:**
1. Sale occurred after April 27, 2024 (EOPT effective date)
2. Sale was on credit / on account
3. Written agreement specifying payment period exists (can be in invoice or lease contract)
4. VAT is separately shown on the invoice
5. Sale is specifically reported in the Summary List of Sales (not lumped under "various sales")
6. Output VAT was declared in 2550Q for the applicable period
7. The agreed-upon payment period has lapsed
8. The VAT component has NOT been claimed as bad debt deduction under NIRC Sec. 34(E)

**Documentation:** Seller must stamp "Claimed Output VAT Credit" on duplicate/triplicate invoice copies and furnish to buyer. Buyer's corresponding input VAT is reversed. On subsequent recovery, stamp "Recovered" and declare output VAT in recovery quarter.

**Key rule — VAT-exempt residential:** Per NIRC Sec. 109(1)(Q), residential units at or below PHP 15,000/month are permanently VAT-exempt regardless of the lessor's total gross receipts. These are excluded from VATable sales and from the PHP 3M threshold computation (per RR 13-2018, qualifying residential receipts are carved out).

**Verification:** Confirmed — accrual basis rule (3 sources: Grant Thornton PH, KPMG PH, BIR 2550Q April 2024 guidelines). Uncollected receivables adjustment confirmed (RR 3-2024 Sec. 4). Residential exemption confirmed (NIRC Sec. 109(1)(Q), RR 13-2018 Sec. 4).

### 3.2 Quarterly Income Tax — 1702Q

**Legal basis:** NIRC Sec. 77 (quarterly returns); Sec. 27(A) (RCIT 25%); Sec. 27(E) (MCIT 2%); RA 11534 (CREATE Act); RR 2-2006 (SAWT attachment)

**Deadline:** 60 days after close of each of the first 3 quarters (NIRC Sec. 77). For a calendar-year corporation:
- Q1 (Jan-Mar): **May 30**
- Q2 (Apr-Jun): **August 29**
- Q3 (Jul-Sep): **November 29**

**Note:** The earlier `input/corporate-rental-tax.md` listed deadlines as May 15 / Aug 15 / Nov 15 — these are INCORRECT and should be corrected to the 60-day rule per NIRC Sec. 77. The rent-roll-preparation analysis already flagged this correction.

**What the accountant needs:**

| Data Point | Source |
|---|---|
| Gross rental income (commercial vs. residential) | Rent roll / billing log |
| Utility pass-through income (if any) | Billing log |
| Interest income | Bank statements |
| Allowable deductions (itemized): | |
| — Salaries of building staff | Payroll register |
| — Repairs and maintenance | Expense voucher log |
| — Property insurance | Policy documents |
| — Depreciation | Fixed asset register |
| — Real property tax | RPT receipts |
| — Professional fees | Expense voucher log |
| — Common area utilities | Utility bills |
| — Interest expense on loans | Loan statements |
| EWT credits (from 2307s received) | 2307 tracker → SAWT |
| Prior quarterly payments | 1702Q confirmation receipts |
| MCIT computation (if 4th+ year) | Gross income × 2% vs. RCIT |

**RCIT vs. MCIT determination:**
```
IF year_of_operations >= 4:
    rcit = net_taxable_income × 0.25  (or 0.20 for SMEs)
    mcit = gross_income × 0.02
    income_tax_due = MAX(rcit, mcit)
    IF mcit > rcit:
        excess_mcit = mcit - rcit  → carry forward as credit vs RCIT for 3 years
ELSE:
    income_tax_due = net_taxable_income × 0.25
```

**SME qualification (20% RCIT rate):** Both conditions must be met:
- Net taxable income ≤ PHP 5,000,000
- Total assets (excl. land where business is situated) ≤ PHP 100,000,000

**SAWT attachment (RR 2-2006):** The Summary Alphalist of Withholding Tax at Source must be attached to every 1702Q. This lists all 2307 certificates received from corporate tenants. Filed as DAT file via BIR Alphalist Data Entry module.

**Verification:** Confirmed — 60-day deadline (NIRC Sec. 77, MPM.ph, BIR eFPS guidelines). RCIT/MCIT computation (CREATE Act, Sec. 27(A)/(E)). SAWT requirement (RR 2-2006).

### 3.3 EWT as Withholding Agent — 0619-E / 1601-EQ / 1604-E

**Legal basis:** NIRC Sec. 57-58; RR 2-98 (EWT regulations, as amended by RR 11-2018); RR 2-2006 (alphalist requirements)

The rental corporation is also a **withholding agent** when it pays suppliers/contractors subject to EWT. This is a SEPARATE obligation from receiving 2307s from tenants.

**Common EWT-subject payments by a rental corporation:**

| Payee | Nature | ATC | EWT Rate |
|---|---|---|---|
| Licensed professionals (lawyers, CPAs) | Professional fees | WC010 | 10% (if gross income > PHP 3M) or 15% |
| Contractors (plumber, electrician, painter) | Contractor's payments | WC158 | 2% |
| Security agency | Service fees | WC158 | 2% |
| Other service providers | Services in general | WC100 | 2% |
| Suppliers of goods | Purchase of goods | WI010 | 1% |
| Rent paid TO others (if corp rents office) | Rental | WC160 | 5% |

**Filing structure:**

| Form | Frequency | Content | Deadline |
|---|---|---|---|
| 0619-E | Monthly (first 2 months of each quarter) | EWT remittance for the month | 10th of following month (non-eFPS); 11th-15th (eFPS) |
| 1601-EQ | Quarterly | Quarterly EWT return + QAP (Quarterly Alphalist of Payees) | Last day of month after quarter-end |
| 1604-E | Annual | Annual Information Return of EWT + alphalist | March 1 |

**QAP (Quarterly Alphalist of Payees):** Attached to 1601-EQ. Lists every payee to whom the corporation made EWT-subject payments during the quarter, with: TIN, registered name, ATC, income payment amount, EWT withheld.

**Data the property manager must compile per payment event:**
1. Payee name (per BIR registration)
2. Payee TIN
3. Payee registered address
4. Nature of payment / ATC code
5. Gross amount paid
6. EWT rate applied
7. EWT amount withheld
8. Date of payment
9. Check/reference number
10. Supporting invoice from payee (must be BIR-registered)

**2307 issuance to payees:** The corporation must issue Form 2307 to each payee within 20 days after quarter-end (NIRC Sec. 58(A)). The issued 2307 data must match the QAP.

**Verification:** Confirmed — filing structure (RR 2-98, BIR eFPS filing calendar). QAP requirement (RR 2-2006). 2307 issuance deadline (NIRC Sec. 58(A), 20 days).

### 3.4 SAWT Generation — Form 2307 as Tax Credit Claimant

**Legal basis:** RR 2-2006 (SAWT as mandatory attachment); NIRC Sec. 57(B) (creditable withholding tax)

The SAWT is filed by the corporation AS RECIPIENT of rental income on which corporate tenants withheld 5% EWT. This is distinct from the 1601-EQ filing (where the corporation files as withholding agent).

**SAWT DAT file format (per RR 2-2006):**

| Field | Description | Source |
|---|---|---|
| Sequence number | Auto-increment | System-generated |
| TIN + branch code | Of the withholding agent (corporate tenant) | 2307 certificate |
| Registered name | Of the withholding agent | 2307 certificate |
| Tax type | Income tax | Fixed: "IC" |
| Period covered | Quarter (MMYYYY-MMYYYY) | 2307 certificate |
| Nature of income | Rental | Fixed: "Rental" |
| ATC | WC160 | Fixed |
| Tax base | Gross rent (net of VAT) | 2307 certificate / rent roll |
| Rate | 5% | Fixed: 0.05 |
| Amount of tax withheld | EWT amount | 2307 certificate |

**Critical reconciliation requirement:** The amounts on each 2307 must match what the tenant reported on their QAP (filed with their 1601-EQ). BIR rejects the tax credit claim if there's a mismatch. The system must support comparison of 2307 amounts against rent roll totals.

**How EWT credits offset income tax:**
```
Income Tax Due = MAX(RCIT, MCIT)
Less: Total EWT credits (sum of all 2307s for the year)
Less: Quarterly income tax payments already remitted
= Balance due (or overpayment → claim for refund or carry-forward)
```

**Verification:** Confirmed — SAWT format (RR 2-2006, Triple-i Consulting, Respicio & Co.). Tax credit mechanism (NIRC Sec. 57(B), RR 2-98 Sec. 2.58.3).

### 3.5 DST Register — Form 2000

**Legal basis:** NIRC Sec. 194 (as amended by RA 10963 TRAIN Law); Sec. 173 (liability); Sec. 201 (inadmissibility of unstamped documents)

**Rate (TRAIN Law, effective Jan 1, 2018):**
- **PHP 6.00** for the first PHP 2,000 (or fractional part) of annual rent
- **PHP 2.00** for every PHP 1,000 (or fractional part) in excess of PHP 2,000
- Computed **per year** of lease term

**Formula:**
```
Annual DST = PHP 6.00 + CEILING((Annual Rent − PHP 2,000) / PHP 1,000) × PHP 2.00
Total DST = Annual DST × Years of Lease Term
```

**Example — Monthly rent PHP 50,000, 3-year lease:**
- Annual rent = PHP 600,000
- Annual DST = PHP 6.00 + CEILING((600,000 − 2,000) / 1,000) × PHP 2.00
- = PHP 6.00 + 598 × PHP 2.00 = **PHP 1,202.00**
- Total DST = PHP 1,202.00 × 3 = **PHP 3,606.00**

**Filing:** BIR Form 2000, within 5 days after close of the month in which the lease was executed.
- Example: Contract executed March 15 → DST due by **April 5**

**DST-triggering events:**
- New lease execution
- Lease renewal (treated as new contract)
- Lease extension (DST on extended period only)
- Amendments increasing rent or extending term

**Note:** `input/corporate-rental-tax.md` contains pre-TRAIN rates (PHP 3/PHP 1). The correct TRAIN-amended rates are PHP 6/PHP 2 as confirmed in the lease-contract-generation analysis.

**Penalty for non-compliance:** Unstamped document is inadmissible in court (NIRC Sec. 201). Additionally: 25% surcharge + 12% annual interest + compromise penalties.

**Verification:** Confirmed — TRAIN rates (PHP 6/PHP 2) confirmed in lease-contract-generation analysis (NIRC Sec. 194 as amended by RA 10963). Filing deadline (5 days after month-end, NIRC Sec. 200).

### 3.6 Annual Filings — 1702-RT and 1604-E

**1702-RT (Annual Corporate ITR):**
- **Deadline:** April 15 (15th day of 4th month after fiscal year-end)
- Full-year aggregation of all quarterly 1702Q data plus Q4
- All 2307 certificates received for the year → annual SAWT
- Complete expense ledger, depreciation schedule, fixed asset register
- MCIT carry-forward credits (if applicable)
- CPA audit required if gross receipts > PHP 3M (NIRC Sec. 232) — all operating rental corps meet this

**1604-E (Annual Information Return of EWT):**
- **Deadline:** March 1 (or last day of February)
- Filed as **withholding agent** — lists ALL payees from whom EWT was withheld during the year
- Schedule 4: Alphalist of all payees subject to EWT
- Schedule 3: Alphalist of payees exempt from withholding but subject to income tax
- Must reconcile with all 12 monthly 0619-E + 4 quarterly 1601-EQ remittances
- Filed in DAT format via eFPS or esubmission portal

**Verification:** Confirmed — 1702-RT deadline (NIRC Sec. 77). 1604-E deadline (RR 2-98, BIR filing calendar).

### 3.7 Input VAT on Capital Expenditures

**Legal basis:** NIRC Sec. 110(A) as amended by RA 10963 (TRAIN Law); RR 16-2005 Sec. 4.110; RMC 21-2022

For building renovations, major repairs, and capital improvements purchased from VAT-registered suppliers:
- Input VAT is creditable against output VAT

**CRITICAL — 60-month amortization SUNSET:** The prior rule requiring amortization of input VAT on capital goods exceeding PHP 1,000,000 over 60 months was **eliminated effective January 1, 2022** under the TRAIN Law phase-in schedule. Since January 1, 2022, **all input VAT on capital goods is claimable in full in the month of purchase/payment**, regardless of amount.

**Current rule (post-Jan 1, 2022):** Full immediate credit. No amortization.

**Transitional rule:** Taxpayers with unutilized input VAT on capital goods purchased **before** January 1, 2022 may continue amortizing the remaining balance until fully utilized.

**Example — PHP 5M building renovation (2026):**
- Input VAT = PHP 5,000,000 × 12% = PHP 600,000
- Full PHP 600,000 claimable as input VAT in the quarter of purchase
- No amortization schedule needed

**Capital goods register still recommended** — tracks: acquisition date, supplier, asset description, cost, input VAT claimed, supporting invoice number. Useful for audit trail even though amortization is no longer required.

**Verification:** **Corrected** — 60-month amortization rule sunset Jan 1, 2022 per TRAIN Law phase-in (Grant Thornton PH, KPMG PH, Forvis Mazars PH / RMC 21-2022). Previous analysis incorrectly stated the 60-month rule still applies.

---

## 4. Data Flow: Operations → Compilation → Accountant → BIR

```
DAILY OPERATIONS
  ├── Invoice issued (billing) ─────────┐
  ├── Payment received ─────────────────┤
  ├── Supplier paid (with EWT) ─────────┤
  └── Lease executed/renewed (DST) ─────┤
                                        ▼
MONTHLY ACCUMULATION
  ├── Invoice log (all invoices issued)
  ├── Collection log (all payments received)
  ├── Expense voucher log (all disbursements)
  └── DST event log (any lease events)
                                        │
                                        ▼
QUARTERLY COMPILATION (property manager)
  ├── Output VAT summary ──────────────→ 2550Q data
  ├── Income/expense summary ──────────→ 1702Q data
  ├── 2307 certificates received ──────→ SAWT DAT
  ├── EWT withheld on suppliers ───────→ 0619-E / 1601-EQ data
  └── DST register ────────────────────→ Form 2000 data
                                        │
                                        ▼
ACCOUNTANT PROCESSES
  ├── Files 2550Q (with input VAT calc)
  ├── Files 1702Q (with SAWT attached)
  ├── Files 1601-EQ (with QAP)
  ├── Remits 0619-E monthly
  └── Files Form 2000 per event
                                        │
                                        ▼
ANNUAL COMPILATION
  ├── Full-year data ──────────────────→ 1702-RT
  ├── Full-year EWT payee alphalist ───→ 1604-E
  └── AFS supporting schedules ────────→ SEC filing
```

---

## 5. What Crispina Built

### Directly Relevant

| Component | Status | Tax Data Utility |
|---|---|---|
| Charge (base_amount, vat_rate_used) | Built | Provides VATable/exempt split for 2550Q |
| ChargeType (is_vat_inclusive, vat_rate) | Built | Enables charge categorization |
| Payment (amount, reference_number) | Built | Provides collection data |
| Transaction (billing batch) | Built | Groups charges for reconciliation |

### Not Built (Critical Gaps)

| Gap | Tax Forms Affected | Impact |
|---|---|---|
| No invoice numbering | 2550Q, LIS | Cannot generate invoice log for accountant |
| No TIN on Tenant | SAWT, 2307 reconciliation, LIS | Cannot produce SAWT DAT file |
| No is_corporate flag | SAWT, 2307 tracking | Cannot identify which tenants should issue 2307s |
| No unit_type on Rentable | 2550Q (VATable/exempt split) | Cannot auto-classify VAT treatment |
| No 2307 tracking model | SAWT, 1702Q | Cannot track received certificates or flag missing ones |
| No supplier/payee register | 1601-EQ, 0619-E, 1604-E | No structured data for EWT as withholding agent |
| No expense voucher model | 1702Q (deductions), 1601-EQ | Expense data is unstructured |
| No DST tracking | Form 2000 | Cannot auto-compute DST or flag filing deadlines |
| No input VAT register | 2550Q (input VAT claims) | Cannot track creditable input VAT from suppliers |
| No capital goods register | 2550Q (amortized input VAT) | Cannot compute 60-month amortization |
| No MCIT tracking | 1702Q | Cannot determine RCIT vs. MCIT or carry-forward excess |
| No payment_method on Payment | 0619-E (bank rec) | Cannot match payments to remittances |

### Design Patterns Worth Preserving

1. **Charge.vat_rate_used stored at charge-time** — audit trail of which VAT rate was applied; directly feeds output VAT computation
2. **ChargeType extensibility** — adding ChargeTypes for DST, penalties, etc. without model changes
3. **CurrencyDecimal (10,2)** — matches BIR precision requirements

---

## 6. Lightweight Feature Spec

### 6.1 Data Model Additions

**Models from other Wave 2 specs that tax compilation depends on:**

```
Tenant (enhanced — from tenant-payment-tracking, rent-roll-preparation)
  + tin: String(20), nullable
  + is_corporate: Boolean, default False
  + is_vat_registered: Boolean, default False

Rentable (enhanced — from monthly-billing-generation)
  + unit_type: Enum(COMMERCIAL, RESIDENTIAL), NOT NULL
  + is_rent_controlled: Boolean, default False

Charge (enhanced — from monthly-billing-generation)
  + invoice_number: String(50), nullable
  + invoice_date: Date, nullable

Form2307Record (from rent-roll-preparation)
  + pk, tenant_pk, quarter, year, gross_rental_per_2307
  + ewt_amount, date_received, status, mismatch_notes
```

**New models specific to tax data compilation:**

```
NEW: SupplierPayee
  pk: UUID
  name: String(255)                      -- BIR-registered name
  tin: String(20), NOT NULL
  address: Text, nullable
  payee_type: Enum(PROFESSIONAL, CONTRACTOR, SERVICE_PROVIDER, GOODS_SUPPLIER, OTHER)
  default_atc: String(10)               -- Default ATC code (e.g., WC010, WC158)
  default_ewt_rate: PercentageDecimal   -- Default EWT rate for this payee type
  is_vat_registered: Boolean, default False
  created_at: DateTime

NEW: ExpenseVoucher
  pk: UUID
  voucher_number: String(50), UNIQUE     -- Sequential: DV-2026-001
  supplier_pk: UUID (FK → SupplierPayee)
  date_paid: Date
  nature_of_expense: String(255)         -- "Plumbing repair Unit 201"
  gross_amount: CurrencyDecimal
  vat_amount: CurrencyDecimal            -- Input VAT (if supplier is VAT-reg'd)
  net_of_vat: CurrencyDecimal            -- gross - vat
  ewt_rate: PercentageDecimal
  ewt_amount: CurrencyDecimal            -- EWT withheld by our corporation
  net_amount_paid: CurrencyDecimal       -- net_of_vat - ewt_amount
  atc_code: String(10)                   -- ATC for this specific payment
  payment_method: Enum(CASH, CHECK, BANK_TRANSFER)
  check_number: String(50), nullable
  property_pk: UUID (FK → Property), nullable  -- Which property this expense relates to
  is_capital_expenditure: Boolean, default False
  supporting_invoice_number: String(50), nullable
  supporting_invoice_date: Date, nullable
  remarks: Text, nullable
  created_at: DateTime

  COMPUTED:
    input_vat_creditable: Boolean = supplier.is_vat_registered AND vat_amount > 0

NEW: InputVATRegister
  pk: UUID
  expense_voucher_pk: UUID (FK → ExpenseVoucher)
  vat_amount: CurrencyDecimal
  quarter: String(7)                     -- "2026-Q1"
  is_capital_good: Boolean, default False
  claim_month: Date                      -- Month when input VAT is claimable (full amount)
  claimed: Boolean, default False
  -- NOTE: 60-month amortization was SUNSET Jan 1, 2022 (TRAIN Law).
  -- All input VAT on capital goods now claimable in full in month of purchase.
  -- Legacy fields below only for pre-2022 transitional balances:
  is_legacy_amortization: Boolean, default False
  amortization_months: Integer, nullable
  monthly_amortized_amount: CurrencyDecimal, nullable
  total_claimed: CurrencyDecimal, default 0
  total_remaining: CurrencyDecimal, nullable

NEW: DSTRecord (enhanced from lease-contract-generation spec)
  pk: UUID
  lease_pk: UUID (FK → Lease), nullable
  event_type: Enum(NEW_LEASE, RENEWAL, EXTENSION, AMENDMENT)
  annual_rent: CurrencyDecimal
  lease_years: Integer
  dst_per_year: CurrencyDecimal          -- Computed
  total_dst: CurrencyDecimal             -- Computed
  contract_execution_date: Date
  filing_deadline: Date                  -- 5 days after month-end
  filed_date: Date, nullable
  form_2000_confirmation: String(50), nullable
  status: Enum(PENDING, FILED, OVERDUE)
  created_at: DateTime

NEW: EWTRemittanceRecord
  pk: UUID
  period_type: Enum(MONTHLY, QUARTERLY)
  period_start: Date
  period_end: Date
  form_type: Enum(0619_E, 1601_EQ)
  total_ewt_remitted: CurrencyDecimal
  filing_date: Date, nullable
  confirmation_number: String(50), nullable
  status: Enum(PENDING, FILED, OVERDUE)

NEW: TaxFilingRecord
  pk: UUID
  form_type: Enum(2550Q, 1702Q, 1702_RT, 1601_EQ, 1604_E, 2551Q, FORM_2000, LIS)
  period: String(20)                     -- "2026-Q1" or "2026" or "2026-H1"
  filing_deadline: Date
  filed_date: Date, nullable
  tax_amount: CurrencyDecimal, nullable
  confirmation_number: String(50), nullable
  file_path: String, nullable            -- Path to exported data file
  status: Enum(PENDING, DATA_READY, FILED, OVERDUE)
  notes: Text, nullable

NEW: MCITTracker
  pk: UUID
  taxable_year: Integer
  year_of_operations: Integer            -- 1st, 2nd, ... (MCIT from 4th year)
  gross_income: CurrencyDecimal
  net_taxable_income: CurrencyDecimal
  rcit_amount: CurrencyDecimal           -- net × 25% (or 20%)
  mcit_amount: CurrencyDecimal           -- gross × 2%
  tax_method_used: Enum(RCIT, MCIT)
  excess_mcit: CurrencyDecimal, default 0  -- MCIT - RCIT if MCIT was used
  excess_mcit_year1_applied: CurrencyDecimal, default 0
  excess_mcit_year2_applied: CurrencyDecimal, default 0
  excess_mcit_year3_applied: CurrencyDecimal, default 0
  excess_mcit_expired: CurrencyDecimal, default 0
  total_ewt_credits: CurrencyDecimal     -- Sum of 2307s
  quarterly_payments_made: CurrencyDecimal
  final_tax_due: CurrencyDecimal         -- After credits and payments
```

### 6.2 Output VAT Compilation Logic (2550Q)

```
FUNCTION compile_vat_data(quarter: Quarter) -> VATQuarterlyData:
  -- quarter = (year, q_number) e.g., (2026, 1) for Jan-Mar

  months = get_months_in_quarter(quarter)  -- [Jan, Feb, Mar]

  -- 1. Output VAT: from all invoices issued during the quarter
  invoices = query_charges(
    invoice_date BETWEEN quarter.start AND quarter.end
  )

  vatable_sales = SUM(c.base_amount FOR c IN invoices
                      WHERE c.rentable.unit_type = COMMERCIAL
                      OR (c.rentable.unit_type = RESIDENTIAL
                          AND c.base_amount > 15000))
  exempt_sales = SUM(c.base_amount FOR c IN invoices
                     WHERE c.rentable.unit_type = RESIDENTIAL
                     AND c.base_amount <= 15000)
  output_vat = SUM(c.base_amount × c.vat_rate_used FOR c IN invoices
                   WHERE c.vat_rate_used > 0)

  -- 2. Uncollected receivables adjustment (RR 3-2024)
  -- Invoices from PRIOR quarter that remain uncollected past credit term
  prior_uncollected = query_charges(
    invoice_date BETWEEN prior_quarter.start AND prior_quarter.end,
    NOT fully_paid,
    days_past_credit_term > 0
  )
  uncollected_vat_adjustment = SUM(c.base_amount × c.vat_rate_used
                                   FOR c IN prior_uncollected)

  -- 3. Input VAT: from expense vouchers with creditable input VAT
  current_input = SUM(ev.vat_amount FOR ev IN expense_vouchers
                      WHERE ev.date_paid BETWEEN quarter.start AND quarter.end
                      AND ev.input_vat_creditable = True
                      AND ev.is_capital_expenditure = False)

  -- 4. Input VAT on capital goods (full claim — 60-month amortization sunset Jan 2022)
  capital_input = SUM(ev.vat_amount FOR ev IN expense_vouchers
                      WHERE ev.date_paid BETWEEN quarter.start AND quarter.end
                      AND ev.input_vat_creditable = True
                      AND ev.is_capital_expenditure = True)

  -- 4b. Legacy amortized input (pre-2022 transitional only)
  legacy_amortized = SUM(ivr.monthly_amortized_amount × 3
                         FOR ivr IN input_vat_register
                         WHERE ivr.is_legacy_amortization = True
                         AND ivr.total_remaining > 0)

  -- 5. Carry-forward from prior quarter
  carry_forward = get_prior_quarter_excess_input(quarter)

  -- 6. Compute
  total_input = current_input + capital_input + legacy_amortized + carry_forward
  vat_payable = output_vat - uncollected_vat_adjustment - total_input

  RETURN VATQuarterlyData(
    vatable_sales=vatable_sales,
    exempt_sales=exempt_sales,
    output_vat=output_vat,
    uncollected_adjustment=uncollected_vat_adjustment,
    current_input_vat=current_input,
    amortized_input_vat=amortized_input,
    carry_forward_input_vat=carry_forward,
    total_input_vat=total_input,
    vat_payable=vat_payable  -- Negative = excess input → carry forward
  )
```

### 6.3 SAWT Generation Logic

```
FUNCTION generate_sawt(quarter: Quarter) -> SAWTData:
  -- Collect all RECEIVED 2307 certificates for this quarter
  certificates = query_form2307(
    quarter=quarter,
    status IN (RECEIVED, DELIVERED, RECONCILED)
  )

  sawt_entries = []
  FOR seq, cert IN enumerate(certificates, start=1):
    sawt_entries.append(SAWTEntry(
      sequence_number=seq,
      tin_branch=cert.tenant.tin + "000",    -- + branch code
      registered_name=cert.tenant.billing_name OR cert.tenant.full_name,
      tax_type="IC",                         -- Income tax - creditable
      period_covered=format_period(quarter),  -- "012026-032026"
      nature_of_income="Rental",
      atc="WC160",
      tax_base=cert.gross_rental_per_2307,
      rate=Decimal("0.05"),
      tax_withheld=cert.ewt_amount
    ))

  -- Validate: total EWT in SAWT = sum of 2307 amounts
  total_ewt = SUM(e.tax_withheld FOR e IN sawt_entries)

  RETURN SAWTData(
    entries=sawt_entries,
    total_tax_base=SUM(e.tax_base FOR e IN sawt_entries),
    total_tax_withheld=total_ewt,
    certificate_count=len(sawt_entries)
  )

  -- Export to DAT file format per BIR Alphalist Data Entry specification
```

### 6.4 EWT Withholding Agent Compilation (1601-EQ)

```
FUNCTION compile_ewt_agent_data(quarter: Quarter) -> EWTAgentData:
  -- All expense vouchers with EWT during the quarter
  vouchers = query_expense_vouchers(
    date_paid BETWEEN quarter.start AND quarter.end,
    ewt_amount > 0
  )

  -- Group by payee for QAP
  qap_entries = []
  FOR payee IN DISTINCT(v.supplier FOR v IN vouchers):
    payee_vouchers = [v FOR v IN vouchers WHERE v.supplier == payee]
    qap_entries.append(QAPEntry(
      tin=payee.tin,
      name=payee.name,
      address=payee.address,
      atc=payee_vouchers[0].atc_code,  -- Assuming same ATC per payee
      total_income_payment=SUM(v.gross_amount FOR v IN payee_vouchers),
      total_ewt_withheld=SUM(v.ewt_amount FOR v IN payee_vouchers)
    ))

  -- Monthly breakdown for 0619-E reconciliation
  monthly_totals = {}
  FOR month IN quarter.months:
    month_vouchers = [v FOR v IN vouchers WHERE v.date_paid.month == month]
    monthly_totals[month] = SUM(v.ewt_amount FOR v IN month_vouchers)

  RETURN EWTAgentData(
    qap_entries=qap_entries,
    total_ewt=SUM(e.total_ewt_withheld FOR e IN qap_entries),
    monthly_breakdown=monthly_totals,
    payee_count=len(qap_entries)
  )

  -- Also triggers: 2307 certificate generation for each payee
```

### 6.5 DST Computation and Tracking

```
FUNCTION compute_and_track_dst(lease: Lease) -> DSTRecord:
  monthly_rent = get_base_rent(lease)  -- From RecurringChargePeriod
  annual_rent = monthly_rent × 12
  years = lease_term_years(lease)      -- Ceiling for partial years

  -- TRAIN Law rates (RA 10963)
  dst_per_year = Decimal("6.00") + \
    CEILING((annual_rent - Decimal("2000")) / Decimal("1000")) * Decimal("2.00")

  IF annual_rent <= Decimal("2000"):
    dst_per_year = Decimal("6.00")

  total_dst = dst_per_year × years

  -- Filing deadline: 5 days after close of month of execution
  execution_month_end = last_day_of_month(lease.contract_execution_date)
  filing_deadline = execution_month_end + timedelta(days=5)

  record = DSTRecord(
    lease_pk=lease.pk,
    event_type=determine_event_type(lease),  -- NEW_LEASE, RENEWAL, etc.
    annual_rent=annual_rent,
    lease_years=years,
    dst_per_year=dst_per_year,
    total_dst=total_dst,
    contract_execution_date=lease.contract_execution_date,
    filing_deadline=filing_deadline,
    status=PENDING
  )

  -- Alert if filing deadline is approaching (< 3 days)
  IF today + timedelta(days=3) >= filing_deadline AND record.status == PENDING:
    create_alert("DST_FILING_DUE", record)

  RETURN record
```

### 6.6 Income Tax Quarterly Compilation (1702Q)

```
FUNCTION compile_income_tax_data(quarter: Quarter) -> IncomeTaxData:
  -- Revenue side (from rent roll / billing)
  gross_rental = SUM(c.base_amount FOR c IN charges_in_quarter)
  -- Split by type for disclosure
  commercial_revenue = SUM(...WHERE rentable.unit_type = COMMERCIAL)
  residential_revenue = SUM(...WHERE rentable.unit_type = RESIDENTIAL)
  other_income = get_interest_income(quarter)  -- Bank statements

  gross_income = gross_rental + other_income

  -- Expense side (from expense vouchers)
  expenses = query_expense_vouchers(quarter)
  deductions = {
    'salaries': SUM(WHERE nature LIKE 'salary%'),
    'repairs_maintenance': SUM(WHERE nature LIKE 'repair%'),
    'depreciation': get_quarterly_depreciation(),
    'rpt': SUM(WHERE nature = 'real_property_tax'),
    'insurance': SUM(WHERE nature = 'insurance'),
    'professional_fees': SUM(WHERE nature LIKE 'professional%'),
    'utilities_common': SUM(WHERE nature LIKE 'utility%'),
    'interest_expense': get_loan_interest(quarter),
    'other': SUM(remaining)
  }
  total_deductions = SUM(deductions.values())
  net_taxable_income = gross_income - total_deductions

  -- Tax computation (cumulative year-to-date)
  ytd_gross = cumulative_gross_through(quarter)
  ytd_net = cumulative_net_through(quarter)

  rcit = ytd_net × rcit_rate()  -- 25% or 20% for SMEs
  mcit = ytd_gross × Decimal("0.02") IF year_of_operations >= 4 ELSE 0

  tax_due = MAX(rcit, mcit)

  -- Credits
  ewt_credits = SUM(2307s received year-to-date)
  prior_quarterly_payments = SUM(1702Q payments for prior quarters this year)
  excess_mcit_credits = get_applicable_mcit_carryforward()

  balance_due = tax_due - ewt_credits - prior_quarterly_payments - excess_mcit_credits

  RETURN IncomeTaxData(
    gross_income=gross_income,
    commercial_revenue=commercial_revenue,
    residential_revenue=residential_revenue,
    total_deductions=total_deductions,
    deduction_breakdown=deductions,
    net_taxable_income=net_taxable_income,
    rcit=rcit,
    mcit=mcit,
    tax_method=RCIT if rcit >= mcit else MCIT,
    tax_due=tax_due,
    ewt_credits=ewt_credits,
    prior_payments=prior_quarterly_payments,
    excess_mcit_applied=excess_mcit_credits,
    balance_due=balance_due
  )
```

### 6.7 Tax Filing Calendar and Alert System

```
FUNCTION generate_filing_calendar(year: int) -> list[TaxFilingRecord]:
  records = []

  FOR q IN [1, 2, 3, 4]:
    quarter_end = date(year, q*3, last_day)

    -- 0619-E: months 1 and 2 of each quarter
    FOR month_offset IN [0, 1]:  -- First 2 months only
      m = (q-1)*3 + month_offset + 1
      records.append(TaxFilingRecord(
        form_type='0619_E',
        period=f"{year}-{m:02d}",
        filing_deadline=date(year, m+1, 10)  -- 10th of following month
      ))

    -- 1601-EQ: last day of month after quarter
    records.append(TaxFilingRecord(
      form_type='1601_EQ',
      period=f"{year}-Q{q}",
      filing_deadline=last_day(date(year, q*3+1, 1))
    ))

    -- 2550Q: 25th of month after quarter
    records.append(TaxFilingRecord(
      form_type='2550Q',
      period=f"{year}-Q{q}",
      filing_deadline=date(year, q*3+1, 25) if q < 4
                      else date(year+1, 1, 25)
    ))

    -- 1702Q: 60 days after quarter-end (Q1-Q3 only)
    IF q <= 3:
      records.append(TaxFilingRecord(
        form_type='1702Q',
        period=f"{year}-Q{q}",
        filing_deadline=quarter_end + timedelta(days=60)
      ))

  -- Annual filings
  records.append(TaxFilingRecord(
    form_type='1604_E', period=str(year),
    filing_deadline=date(year+1, 3, 1)))
  records.append(TaxFilingRecord(
    form_type='1702_RT', period=str(year),
    filing_deadline=date(year+1, 4, 15)))

  -- LIS (semi-annual)
  records.append(TaxFilingRecord(
    form_type='LIS', period=f"{year}-H1",
    filing_deadline=date(year, 7, 31)))
  records.append(TaxFilingRecord(
    form_type='LIS', period=f"{year}-H2",
    filing_deadline=date(year+1, 1, 31)))

  RETURN records

-- Alert system: flag filings due within 7 days
-- Overdue detection: mark as OVERDUE if deadline passed and status != FILED
```

### 6.8 Edge Cases

1. **Mid-year VAT registration crossing:** If the corporation crosses the PHP 3M threshold mid-year, all commercial invoices after the registration date include 12% VAT. Historical invoices (pre-registration) remain non-VAT. The 2550Q must reflect the correct period only (from registration date).

2. **2307 mismatch with tenant's QAP:** Common problem — the tenant's 2307 shows a different gross amount than the rent roll. Causes: timing differences (tenant accrues differently), adjustments for credit memos, computational errors. The system must flag mismatches for human review. The accountant decides whether to claim the full amount, the lesser amount, or exclude the certificate.

3. **MCIT carry-forward expiry:** Excess MCIT from Year N can only offset RCIT in Years N+1, N+2, N+3. If not fully used in 3 years, the excess expires. Carry-forward credits offset RCIT only (not future MCIT). System must track: year of origin, amount, years applied, remaining, expiry date.

4. **Mixed-use input VAT proration:** If a building renovation serves both VATable and exempt units, input VAT must be prorated. Only the portion attributable to VATable sales is creditable. Proration method: ratio of VATable sales to total sales for the quarter. (Note: 60-month amortization no longer applies — the prorated amount is fully claimable in the quarter of purchase.)

5. **DST on extension vs. renewal:** Extension: DST computed on the extension period's annual rent × extension years. Renewal: DST computed on the renewed term's annual rent × full renewed years. A lease renewal with a higher rent pays more DST than a simple extension at the same rate.

6. **Zero-EWT tenants:** Individual tenants renting for personal use are NOT withholding agents — no 2307 expected. The system must not flag them as "missing 2307."

7. **Partial quarter operations:** Corporation starts or stops operating mid-quarter. Quarterly filings cover only the operational period. Prorated thresholds may apply.

8. **Late 2307 receipt:** If a corporate tenant issues 2307 late (after 20 days post-quarter), the corporation can still claim the EWT credit on the 1702Q for that quarter. But if it arrives after the 1702Q filing deadline, the credit shifts to the next quarter. The system must track the "claim quarter" separately from the "certificate quarter."

9. **Uncollected receivables timing:** The one-quarter claim window for output VAT adjustment (RR 3-2024) starts from the quarter the invoice becomes delinquent, not from the quarter of issuance. If invoice is issued in Q1 with 30-day terms and remains unpaid on day 31 (still in Q1), the adjustment is claimable on Q2's 2550Q.

10. **Withholding agent obligations — dual role:** The corporation is BOTH a tax credit claimant (receives 2307 from tenants) AND a withholding agent (issues 2307 to suppliers). These are tracked separately. The SAWT (attached to 1702Q) is for received 2307s. The QAP (attached to 1601-EQ) is for issued 2307s.

---

## 7. Automability Score: 4 / 5

**Justification:** The majority of tax data compilation is deterministic — aggregating structured data into prescribed formats. However, several points require human judgment:

**Automatable (5/5 components):**
- Output VAT summary (aggregate invoices by VAT status)
- SAWT generation from 2307 records (mechanical format conversion)
- DST computation (pure formula)
- Filing calendar generation and alerts (deterministic dates)
- EWT computation on supplier payments (rate × base)
- MCIT vs. RCIT determination (compare two numbers)

**Requires human judgment (lowering to 4/5):**
- **2307 mismatch resolution** — when certificate amounts don't match rent roll, human must decide whether to claim, adjust, or dispute
- **Expense categorization** — determining the correct ATC code for unusual payments, deciding whether an expense qualifies as deductible
- **Capital goods classification** — distinguishing capital expenditure from revenue expenditure for input VAT amortization
- **Input VAT proration** — for mixed-use expenses, determining the VATable/exempt sales ratio is mechanical, but deciding which expenses serve both is judgment-based
- **Uncollected receivables assessment** — determining whether non-collection is genuine (for VAT adjustment) vs. timing issue
- **SME qualification assessment** — annual evaluation of whether the corporation qualifies for 20% RCIT requires asset valuation

**Net assessment:** 4/5 — High automability for data aggregation and report generation, but the classification and edge-case decisions require human involvement.

---

## 8. Verification Status

| Rule | Status | Sources |
|------|--------|---------|
| VAT accrual basis (RR 3-2024 / RA 11976) | **Confirmed** | Grant Thornton PH, KPMG PH, BIR 2550Q guidelines |
| Uncollected receivables VAT adjustment | **Confirmed** | RR 3-2024 Sec. 4, RMC 65-2024, PwC PH, Deloitte SEA |
| Residential VAT exemption (NIRC Sec. 109(1)(Q)) | **Confirmed** | NIRC text, RR 13-2018 Sec. 4, Acclime PH |
| 1702Q deadline — 60 days (NIRC Sec. 77) | **Confirmed with correction** | NIRC Sec. 77, MPM.ph, BIR eFPS guidelines |
| SAWT requirement (RR 2-2006) | **Confirmed** | SC E-Library (RR 2-2006), Triple-i Consulting |
| EWT withholding agent filing structure | **Confirmed** | RR 2-98, BIR eFPS filing calendar |
| DST TRAIN rates (PHP 6/PHP 2) | **Confirmed** | NIRC Sec. 194 as amended by RA 10963, lease-contract-generation verification |
| Input VAT capital goods — immediate full credit | **Corrected** | 60-month rule sunset Jan 1, 2022 per TRAIN phase-in. Grant Thornton PH, KPMG PH, RMC 21-2022 |
| MCIT carry-forward (3 years, RCIT only) | **Confirmed** | NIRC Sec. 27(E), CREATE Act implementing rules |
| 1604-E deadline (March 1) | **Confirmed** | RR 2-98, BIR filing calendar |

All 10 rules verified against 2+ independent sources. Two corrections carried forward from prior analyses: (1) 1702Q deadline is 60 days after quarter-end, not May 15 / Aug 15 / Nov 15; (2) DST rates are TRAIN-amended PHP 6/PHP 2, not pre-TRAIN PHP 3/PHP 1. One new correction discovered: (3) 60-month input VAT amortization on capital goods was sunset January 1, 2022 — full immediate credit now applies.

---

## 9. Corrections to Prior Source Documents

The following corrections should be applied to `input/corporate-rental-tax.md`:

1. **Section 1 (RCIT) — 1702Q Deadlines:** Table shows May 15, Aug 15, Nov 15. Should be **~May 30, ~Aug 29, ~Nov 29** per NIRC Sec. 77 (60 days after quarter-end). The exact dates vary based on month-end day count.

2. **Section 5 (DST) — Rates:** Formula shows PHP 3.00 / PHP 1.00. Should be **PHP 6.00 / PHP 2.00** per TRAIN Law (RA 10963, effective Jan 1, 2018). The example computation (PHP 601 per year for PHP 600K annual rent) should be **PHP 1,202 per year**.

3. **New — Input VAT on Capital Goods:** Any reference to 60-month amortization of input VAT on capital goods exceeding PHP 1M is **outdated**. The TRAIN Law sunset this rule effective January 1, 2022. Full input VAT is now claimable immediately in the month of purchase regardless of amount (per RMC 21-2022).
