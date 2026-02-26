# Rent Roll Preparation

**Wave:** 2 (Process Analysis & Feature Spec)
**Analyzed:** 2026-02-26
**Dependencies:** crispina-models, crispina-services, corporate-rental-tax, accounting-agency-handoff, tenant-payment-tracking, monthly-billing-generation

---

## 1. Process Description

**What:** Compile a monthly rent roll — a spreadsheet with one row per unit showing tenant identity, lease details, billing amounts, VAT breakdown, collections, outstanding balances, EWT/2307 status, and invoice references. This is the single most important document in the monthly data package delivered to the external accounting agency. It also serves as the master data source for the BIR Lessee Information Statement (LIS), quarterly VAT returns (2550Q), quarterly income tax returns (1702Q), and SAWT generation.

**When:** Monthly, completed by the **5th of the following month** (operational best practice, not regulatory). This gives the external accountant lead time for:
- 0619-E monthly EWT remittance (due 10th for non-eFPS / 11th–15th for eFPS filers — first 2 months of quarter only)
- 2550Q quarterly VAT return (due 25th of month after quarter-end)
- 1702Q quarterly income tax return (due 60th day after quarter-end, i.e., ~15th of 2nd month)
- 1601-EQ quarterly EWT return (due last day of month after quarter-end)

**Who does it:** Property manager. Currently compiled manually in Excel from individual tenant ledgers, lease contracts, and payment records.

**Frequency:** Monthly. A subset of the rent roll data is also used for the semi-annual LIS (January 31 and July 31).

---

## 2. Current Method

**Fully manual / spreadsheet.** The property manager:
1. Opens previous month's rent roll Excel file as template
2. Updates monthly rates where escalation applies (checks lease contracts)
3. Enters payment amounts received per tenant from manual ledger
4. Computes outstanding balances manually (prior balance + billed − collected)
5. Checks which corporate tenants have submitted 2307 certificates for the quarter
6. Fills in invoice/receipt numbers manually from booklets
7. Notes any vacancies, holdovers, or disputes in the remarks column
8. Delivers file (USB/email) to accountant by 5th of month

**Pain points:**
- Data re-entry from multiple sources (lease contracts, payment log, 2307 pile)
- Balance computation errors (running totals drift over months)
- Missing 2307 certificates not tracked systematically
- No VAT/exempt split computed — accountant must re-derive from unit type
- No connection between invoice numbers and billing system
- LIS preparation is a separate manual effort using similar data

---

## 3. Regulatory Rules

### 3.1 Lessee Information Statement (RR 12-2011 / RMC 69-2009)

The BIR requires lessors to file a semi-annual LIS with their RDO:
- **January 31** — as of December 31 of previous year
- **July 31** — as of June 30 of current year

**Prescribed columns** (per RR 12-2011):

| # | Column |
|---|--------|
| 1 | Floor/Unit Number |
| 2 | Name of Tenant |
| 3 | Total Leased Area (sqm) |
| 4 | Monthly Rental |
| 5 | Start of Lease |
| 6 | Duration/Period of Lease |
| 7 | TIN |
| 8 | Authority to Print (ATP) number for Invoices/ORs |
| 9 | POS/CRM Permit (where applicable) |

**Filing requirements:** Hard copy + soft copy (Excel on CD-R), submitted under oath to the RDO. Must also include building/space layout and certified true copies of lease contracts.

**Verification:** Confirmed — BIR RR 12-2011 PDF, PhilTaxation Blog, Clemente Aquino & Co. CPAs

### 3.2 Rent Roll as VAT Return Source (BIR 2550Q)

The rent roll provides the data for computing quarterly output VAT:
- **Output VAT declared on accrual basis** — when invoice is issued, not when payment is collected (RR 3-2024, implementing RA 11976 EOPT Act, effective April 27, 2024)
- **RR 7-2024** governs invoicing requirements: VAT Sales Invoice replaces Official Receipt as primary document
- Rent roll must distinguish **VATable sales** (commercial + residential > PHP 15K) from **VAT-exempt sales** (residential ≤ PHP 15K per NIRC Sec. 109(1)(Q))
- **Output VAT Credit on Uncollected Receivables** — if rent is not collected within agreed credit term, lessor may deduct output VAT from next quarter's return (one-quarter claim window)

The 2550Q form (April 2024 ENCS) includes separate lines for VATable Sales, Zero-Rated Sales, Exempt Sales, and the new Uncollected Receivables adjustment.

**Verification:** Confirmed — Grant Thornton PH (RR 7-2024), KPMG PH (EOPT clarifications), BIR 2550Q April 2024 guidelines

### 3.3 Rent Roll as Income Tax Return Source (BIR 1702Q)

The rent roll provides gross rental income breakdown for quarterly income tax:
- **Commercial vs. residential** — different disclosure categories
- **RCIT 25%** (or 20% for SMEs: net income ≤ PHP 5M AND assets ≤ PHP 100M excl. land)
- **MCIT 2%** of gross income — applicable from 4th taxable year; pay whichever is higher
- Excess MCIT carried forward as credit against RCIT for 3 years

The accountant uses the rent roll's gross amounts (by tenant type) to compute quarterly income tax. Deductions (expenses) come from the expense voucher package, not the rent roll.

**Verification:** Confirmed — BIR 1702Q guidelines, Acclime PH, Grant Thornton PH

### 3.4 Form 2307 Tracking and SAWT (RR 2-2006)

Corporate tenants who withhold 5% EWT issue Form 2307 to the landlord within 20 days of quarter-end:
- Rent roll tracks: which corporate tenants owe 2307s, whether received, amounts
- 2307 sums become **tax credits** against RCIT on the 1702Q
- The accountant generates a **SAWT (Summary Alphalist of Withholding Tax at Source)** from 2307 data
- SAWT is filed as a DAT file (per RR 2-2006) attached to 1702Q and 2550Q

**SAWT DAT file fields** (per RR 2-2006):
1. Sequence number
2. TIN + branch code of withholding agent (the corporate tenant)
3. Registered name of withholding agent
4. Tax type
5. Period covered
6. Nature of income payment (rental)
7. ATC: WC160
8. Tax base (gross rent, net of VAT for VAT-registered lessors)
9. Applicable rate (5%)
10. Amount of tax withheld

**Mismatch risk:** 2307 amounts must exactly match amounts on the tenant's Quarterly Alphalist of Payees (QAP). BIR rejects tax credit claims on mismatch — the rent roll must enable reconciliation.

**Verification:** Confirmed — SC E-Library (RR 2-2006), Triple-i Consulting, Respicio & Co.

### 3.5 AFS Disclosure Support (PFRS/PAS)

The rent roll feeds Audited Financial Statements notes:
- **Accounts receivable aging** — current, 31-60 days, 61-90 days, 90+ days (standard buckets for PFRS 9 Expected Credit Loss provision matrix)
- **Lease disclosure (PFRS 16)** — lessor accounting largely unchanged from PAS 17 (operating lease classification retained for rental properties); enhanced disclosures include: maturity analysis of undiscounted lease payments receivable (5-year forward projection per PFRS 16 para. 97), lease income recognized in the period, variable lease payments
- **Security deposits held** — liability disclosure with per-tenant detail

**Verification:** Confirmed — Grant Thornton PH (PFRS 16), PwC PH disclosure checklist. Nuance: PFRS 16 impact on lessor is modest (primarily enhanced disclosures); PFRS 9 ECL aging is the more impactful requirement.

### 3.6 Filing Deadline Calendar

| Filing | Form | Deadline | Rent Roll Data Needed |
|--------|------|----------|----------------------|
| Monthly EWT remittance (as W/H agent) | 0619-E | 10th (non-eFPS) / 11th-15th (eFPS) of following month; first 2 months of quarter only | Supplier EWT withheld (not rent roll) |
| Quarterly VAT | 2550Q | 25th of month after quarter-end | Output VAT by category |
| Quarterly income tax | 1702Q | 60th day after quarter-end (~15th of 2nd month) | Gross rental income breakdown |
| Quarterly EWT return | 1601-EQ | Last day of month after quarter-end | EWT withheld on supplier payments |
| Semi-annual LIS | Per RR 12-2011 | Jan 31 / Jul 31 | Tenant, unit, area, rent, lease term, TIN, ATP |

**Verification:** Confirmed with correction — 1702Q deadline is 60 days (not 25th); 0619-E only covers first 2 months per quarter. Sources: MPM.ph, BIR eFPS guidelines, Juan.tax, Davao Accountants.

---

## 4. Rent Roll Column Specification

Based on the accounting-agency-handoff research (Section 4), the rent roll requires 26 columns:

| # | Column | Source | LIS? | 2550Q? | 1702Q? | SAWT? |
|---|--------|--------|------|--------|--------|-------|
| 1 | Unit Number / Floor-Unit Reference | Lease/Rentable | Yes | | | |
| 2 | Unit Type (Commercial / Residential) | Rentable.unit_type | | Yes | Yes | |
| 3 | Tenant Name (Registered/Legal) | Tenant | Yes | | | |
| 4 | Tenant TIN | Tenant.tin | Yes | | | Yes |
| 5 | Lease Start Date | Lease.date_start | Yes | | | |
| 6 | Lease End Date / Duration | Lease.date_end | Yes | | | |
| 7 | Total Leased Area (sqm) | Rentable.floor_area_sqm | Yes | | | |
| 8 | Contractual Monthly Rent (base, excl. VAT) | RecurringChargePeriod.amount | Yes* | Yes | Yes | |
| 9 | CUSA / Association Dues | Other RecurringCharge | | Yes | Yes | |
| 10 | Other Charges (parking, utility pass-through) | Charge by type | | Yes | Yes | |
| 11 | VAT Status (VATable / VAT-Exempt) | derived from unit_type + rent | | Yes | | |
| 12 | VAT Amount (12% if applicable) | Charge.vat_rate_used × base | | Yes | | |
| 13 | Total Amount Billed (VAT-inclusive) | Charge.amount (sum) | | | | |
| 14 | Invoice Number Issued | Charge.invoice_number | | | | |
| 15 | Invoice Date | Charge.invoice_date | | | | |
| 16 | Amount Collected this Month | Payment.amount (sum) | | | | |
| 17 | Date Collected | Payment.date_issued | | | | |
| 18 | Mode of Payment | Payment.payment_method | | | | |
| 19 | Check Number / Reference | Payment.reference_number | | | | |
| 20 | Outstanding Balance | TenantBalance.total_balance | | | | |
| 21 | Security Deposit Held | SecurityDeposit.amount | | | | |
| 22 | 2307 Received (Yes/No) | Form2307.received | | | | Yes |
| 23 | 2307 Quarter Covered | Form2307.quarter | | | | Yes |
| 24 | Amount per 2307 | Form2307.ewt_amount | | | | Yes |
| 25 | ATP Number | InvoiceSequence.atp_number | Yes | | | |
| 26 | Remarks | free text | | | | |

*LIS shows "Monthly Rental" — may include VAT in the LIS amount depending on RDO practice.

**Cross-reference flags:**
- Columns 1-7, 8, 25: Used for LIS generation (9 of 26 columns)
- Columns 2, 8-12: Used for 2550Q VAT computation
- Columns 2, 8-10: Used for 1702Q income tax
- Columns 3-4, 22-24: Used for SAWT DAT file generation

---

## 5. What Crispina Built

### Directly Relevant

| Component | Status | Notes |
|-----------|--------|-------|
| Property → Room → Rentable | Built | Provides unit hierarchy for Column 1 |
| Tenant (first_name, last_name, billing_name) | Built | Provides Column 3 |
| Lease (date_start, date_end) | Built | Provides Columns 5-6 |
| RecurringChargePeriod.amount | Built | Provides Column 8 (base rent for period) |
| Charge (base_amount, vat_rate_used, amount) | Built | Provides Columns 8-13 |
| Payment (amount, reference_number, date_issued) | Built | Provides Columns 16-17, 19 |
| PaymentAllocation | Built | Enables balance computation (Column 20) |
| TransactionDetail (balance) | Built | Per-transaction balance only — not tenant-level |

### Not Built (Key Gaps)

| Gap | Columns Affected | Impact |
|-----|-----------------|--------|
| No `tin` on Tenant | 4 | Cannot generate LIS or SAWT without TIN |
| No `is_corporate` flag on Tenant | 22-24 | Cannot determine which tenants should issue 2307s |
| No `unit_type` on Rentable | 2, 11 | Cannot split VATable vs exempt |
| No `floor_area_sqm` on Rentable | 7 | Cannot populate LIS leased area |
| No `invoice_number` / `invoice_date` on Charge | 14-15 | Cannot populate invoice columns |
| No `payment_method` on Payment | 18 | Cannot populate mode of payment |
| No security deposit model | 21 | Cannot track deposit held |
| No 2307 tracking model | 22-24 | Cannot track EWT certificates |
| No InvoiceSequence | 25 | Cannot populate ATP number |
| No tenant-level balance rollup | 20 | Must aggregate across all transactions manually |
| No lease status field | — | Cannot filter to "active" leases for rent roll |
| No `is_rent_controlled` flag | 2, 11 | Cannot determine VAT treatment automatically |
| **No rent roll report/export** | all | No query or endpoint to generate the rent roll |

### Design Patterns Worth Preserving

1. **Charge.base_amount + vat_rate_used** — pre-VAT storage maps directly to rent roll columns 8 and 12
2. **RecurringChargePeriod.amount** — pre-computed escalation means the rent roll's "contractual monthly rent" is a simple period lookup
3. **PaymentAllocation junction** — enables computing "amount collected this month" per tenant
4. **CurrencyDecimal (10,2)** — matches BIR precision requirements

---

## 6. Lightweight Feature Spec

### 6.1 Data Model Additions

Models from other Wave 2 feature specs that the rent roll depends on:

```
Tenant (enhanced — from tenant-payment-tracking)
  + tin: String(20), nullable
  + is_corporate: Boolean, default False
  + is_vat_registered: Boolean, default False

Rentable (enhanced — from monthly-billing-generation)
  + unit_type: Enum(COMMERCIAL, RESIDENTIAL), NOT NULL
  + is_rent_controlled: Boolean, default False
  + floor_area_sqm: Decimal(8,2), nullable

Lease (enhanced — from lease-status-visibility)
  + status: Enum(DRAFT, ACTIVE, EXPIRED, MONTH_TO_MONTH, HOLDOVER, RENEWED, TERMINATED)

Charge (enhanced — from monthly-billing-generation)
  + invoice_number: String(50), nullable
  + invoice_date: Date, nullable

Payment (enhanced — from tenant-payment-tracking)
  + payment_method: Enum(CASH, BANK_TRANSFER, CHECK, GCASH, OTHER)
  + or_number: String(50), nullable
  + check_number: String(50), nullable

InvoiceSequence (from monthly-billing-generation)
  + atp_number: String(50)

TenantBalance (materialized view — from tenant-payment-tracking)
  + total_billed, total_paid, total_balance, months_in_arrears
```

**New models specific to rent roll:**

```
NEW: Form2307Record
  pk: UUID
  tenant_pk: UUID (FK → Tenant)          -- The corporate tenant who issued it
  quarter: String(7)                       -- e.g., "2026-Q1"
  year: Integer
  gross_rental_per_2307: CurrencyDecimal   -- Tax base per certificate
  ewt_amount: CurrencyDecimal             -- 5% EWT per certificate
  date_received: Date, nullable            -- When landlord received original
  date_delivered_to_accountant: Date, nullable
  invoice_numbers_referenced: Text, nullable  -- Invoice/OR numbers cited on 2307
  status: Enum(EXPECTED, RECEIVED, DELIVERED, RECONCILED, DISPUTED)
  mismatch_notes: Text, nullable           -- If amounts don't match rent roll
  created_at: DateTime

NEW: RentRollReport
  pk: UUID
  report_month: Date (1st of month)
  generated_at: DateTime
  generated_by: String
  total_units: Integer
  total_billed: CurrencyDecimal
  total_collected: CurrencyDecimal
  total_outstanding: CurrencyDecimal
  total_vat_output: CurrencyDecimal
  total_vat_exempt: CurrencyDecimal
  file_path: String, nullable              -- Path to exported file (Excel/CSV)
  status: Enum(DRAFT, FINALIZED, DELIVERED)

NEW: LISReport
  pk: UUID
  report_date: Date                        -- As-of date (Jun 30 or Dec 31)
  filing_deadline: Date                    -- Jan 31 or Jul 31
  filed_date: Date, nullable
  total_tenants: Integer
  file_path: String, nullable
  status: Enum(DRAFT, FILED)
```

### 6.2 Rent Roll Generation Logic

```
FUNCTION generate_rent_roll(report_month: Date) -> RentRollReport:
  -- report_month = first day of the month being reported

  -- 1. Get all active leases (ACTIVE, MONTH_TO_MONTH, HOLDOVER)
  active_leases = query_leases(
    status IN (ACTIVE, MONTH_TO_MONTH, HOLDOVER),
    date_start <= last_day(report_month)
  )

  rows = []
  FOR each lease in active_leases:
    FOR each rentable in lease.rentables:
      row = RentRollRow()

      -- Identity columns (1-7)
      row.unit_reference = rentable_path(rentable)     -- "Unit 101" or "A Unit 102"
      row.unit_type = rentable.unit_type               -- COMMERCIAL / RESIDENTIAL
      row.tenant_name = lease.tenant.billing_name OR lease.tenant.full_name
      row.tenant_tin = lease.tenant.tin
      row.lease_start = lease.date_start
      row.lease_end = lease.date_end
      row.leased_area_sqm = rentable.floor_area_sqm

      -- Billing columns (8-15)
      rent_period = find_active_period(lease.rent_recurring_charge, report_month)
      row.base_rent = rent_period.amount               -- Pre-VAT monthly rent
      row.cusa = sum_charges(lease, rentable, report_month, type=CUSA)
      row.other_charges = sum_charges(lease, rentable, report_month,
                                      type NOT IN (RENT, CUSA))
      row.vat_status = determine_vat_status(rentable, row.base_rent)
      row.vat_amount = compute_vat(row, rentable)      -- 12% or 0
      row.total_billed = row.base_rent + row.cusa + row.other_charges + row.vat_amount
      row.invoice_number = get_invoice_number(lease, rentable, report_month)
      row.invoice_date = get_invoice_date(lease, rentable, report_month)

      -- Collection columns (16-19)
      payments = get_payments_for_period(lease.tenant, report_month)
      row.amount_collected = sum(p.amount for p in payments)
      row.date_collected = latest(p.date_issued for p in payments)
      row.payment_mode = payments[0].payment_method if len(payments) == 1
                         else "MULTIPLE"
      row.check_reference = payments[0].reference_number if applicable

      -- Balance column (20)
      row.outstanding_balance = get_tenant_balance(lease.tenant).total_balance

      -- Deposit column (21)
      row.security_deposit_held = get_security_deposit(lease)

      -- 2307 columns (22-24)
      IF lease.tenant.is_corporate:
        form2307 = get_latest_2307(lease.tenant, report_month)
        row.form2307_received = form2307.status != EXPECTED if form2307 else False
        row.form2307_quarter = form2307.quarter if form2307 else None
        row.form2307_amount = form2307.ewt_amount if form2307 else None
      ELSE:
        row.form2307_received = N/A  -- Individual tenants don't issue 2307

      -- ATP and remarks (25-26)
      row.atp_number = get_active_atp()
      row.remarks = compile_remarks(lease, rentable)  -- vacancies, holdovers, disputes

      rows.append(row)

  -- Generate report
  report = RentRollReport(
    report_month=report_month,
    total_units=len(rows),
    total_billed=sum(r.total_billed for r in rows),
    total_collected=sum(r.amount_collected for r in rows),
    total_outstanding=sum(r.outstanding_balance for r in rows),
    total_vat_output=sum(r.vat_amount for r in rows WHERE vat_status=VATABLE),
    total_vat_exempt=sum(r.base_rent for r in rows WHERE vat_status=EXEMPT),
    status=DRAFT
  )

  RETURN report, rows
```

### 6.3 LIS Generation Logic

```
FUNCTION generate_lis(as_of_date: Date) -> LISReport:
  -- as_of_date = June 30 or December 31

  -- LIS is a SUBSET of rent roll data — only 9 columns
  active_leases = query_leases(
    status IN (ACTIVE, MONTH_TO_MONTH, HOLDOVER),
    date_start <= as_of_date,
    -- Include leases active as of the as-of date
  )

  lis_rows = []
  FOR each lease in active_leases:
    FOR each rentable in lease.rentables:
      lis_rows.append(LISRow(
        unit_number=rentable_path(rentable),
        tenant_name=lease.tenant.billing_name OR lease.tenant.full_name,
        leased_area_sqm=rentable.floor_area_sqm,
        monthly_rental=get_current_rent(lease, as_of_date),  -- Current rate as of date
        lease_start=lease.date_start,
        lease_duration=format_duration(lease.date_start, lease.date_end),
        tin=lease.tenant.tin,
        atp_number=get_active_atp(),
        pos_crm_permit=None  -- POS/CRM permit if applicable
      ))

  -- Export to prescribed Excel format
  export_lis_excel(lis_rows, as_of_date)

  RETURN LISReport(
    report_date=as_of_date,
    filing_deadline=date(as_of_date.year + (1 if as_of_date.month == 12 else 0),
                         1 if as_of_date.month == 12 else 7, 31),
    total_tenants=len(lis_rows),
    status=DRAFT
  )
```

### 6.4 Export Formats

**Rent Roll — Excel export for accountant:**
- One worksheet per property (if multiple properties)
- 26 columns per the specification in Section 4
- Summary row at bottom: totals for billed, collected, balance, VAT
- Sub-totals by unit type (commercial / residential / exempt)
- Separate summary tab: VATable vs. exempt sales totals (for 2550Q input)
- 2307 summary tab: expected vs. received 2307s by corporate tenant (for SAWT)

**LIS — BIR-prescribed Excel format:**
- 9 columns per RR 12-2011
- No summary rows (raw data for BIR)
- Submitted on CD-R alongside hard copy and supporting documents

**SAWT DAT input — structured export for accountant:**
- Extract from rent roll + Form2307Record
- Per-2307 row: sequence, tenant TIN, name, WC160, quarter, gross rent (net of VAT), 5%, EWT amount
- Accountant feeds into BIR Alphalist Data Entry module to generate DAT file

### 6.5 2307 Tracking Workflow

```
AT LEASE CREATION (if tenant.is_corporate):
  -- Pre-create expected 2307 records for lease duration
  FOR each quarter in lease term:
    create Form2307Record(
      tenant_pk=tenant.pk,
      quarter=quarter_label,
      year=quarter_year,
      gross_rental_per_2307=quarterly_rent_total,  -- 3 months × base rent
      ewt_amount=quarterly_rent_total × 0.05,
      status=EXPECTED
    )

AT EACH QUARTER END:
  -- Dashboard shows: expected 2307s vs received
  -- Alert for overdue 2307s (> 20 days past quarter-end)

ON 2307 RECEIPT:
  1. Property manager logs date_received
  2. Cross-check: gross amount on 2307 vs. rent roll totals for that quarter
  3. If match → status = RECEIVED
  4. If mismatch → status = DISPUTED, log mismatch_notes
  5. Deliver original to accountant → status = DELIVERED

ON SAWT GENERATION (quarterly with 1702Q):
  -- Accountant reconciles all RECEIVED 2307s
  -- If reconciled: status = RECONCILED
  -- Sum of EWT = tax credit on 1702Q
```

### 6.6 Edge Cases

1. **Vacant unit:** Include in rent roll with blank tenant columns, "VACANT" in remarks. Exclude from LIS (no tenant). Include in occupancy metrics.

2. **Multi-unit lease:** One tenant leasing Units 102-A and 102-B under single lease. Show as separate rows (one per rentable) with same tenant/lease info. Both rows reference the same invoice number if billed on a single invoice.

3. **Mid-month move-in/move-out:** Pro-rated rent in "base rent" column. Rent roll shows the actual billed amount for that month, not the full monthly rate. Add note in remarks.

4. **Tacit reconduction tenant:** Lease status = MONTH_TO_MONTH. Lease end date may be blank or show original end date with "(m-t-m)" notation. Include in rent roll at last applicable rate.

5. **Holdover tenant:** Lease status = HOLDOVER. Include at the holdover rate (150-200% if contractually specified). Flag in remarks.

6. **2307 partial-quarter:** Corporate tenant moves in mid-quarter. Expected 2307 amount covers only the months occupied. Gross rental on 2307 should match invoices issued during those months.

7. **VAT status change:** If lessor crosses PHP 3M threshold mid-year, all commercial invoices after VAT registration date show 12% VAT. Rent roll must reflect the correct VAT treatment per-month, not retroactively.

8. **Multiple payments in one month:** A tenant may pay current month + arrears. "Amount Collected" column shows total collected in the report month, not just current-month rent. Outstanding balance column reflects post-collection position.

9. **Advance rent applied in final month:** Show as a credit line: "Less: Advance rent applied — PHP X". Net amount billed may be zero. Invoice still issued (VAT was already declared on advance at receipt under pre-EOPT rules; under post-EOPT rules, VAT declared when service rendered).

10. **2307 amount mismatch:** Common issue — tenant's QAP amount doesn't match rent roll. System should flag mismatches for manual resolution before SAWT generation. Unresolved mismatches → accountant must decide whether to claim or exclude.

### 6.7 Downstream Data Consumers

| Consumer | Data Extracted | Frequency |
|----------|---------------|-----------|
| External accountant — monthly package | Full 26-column rent roll | Monthly |
| BIR 2550Q — VAT return | VATable/exempt sales totals + output VAT | Quarterly |
| BIR 1702Q — income tax | Gross rental income by type | Quarterly |
| SAWT — withholding tax credit | 2307 amounts per corporate tenant | Quarterly |
| BIR LIS — lessee information | 9-column subset | Semi-annually |
| AFS — accounts receivable aging | Outstanding balance + aging buckets | Annually |
| AFS — lease disclosure (PFRS 16) | Lease terms, undiscounted future payments | Annually |
| AFS — security deposit disclosure | Deposits held per tenant | Annually |
| Compliance calendar | LIS filing due dates | Semi-annually |

---

## 7. Automability Score: 5 / 5

**Justification:** The rent roll is a **pure reporting process**. Given:
- Active lease data (tenant, unit, rate, dates) — structured
- Charge and invoice data (from billing generation) — structured
- Payment data (from payment tracking) — structured
- 2307 records (from 2307 tracking) — structured
- Balance computations (from TenantBalance view) — deterministic

...the entire rent roll can be generated without any human judgment. Every column is either a direct field lookup or a deterministic computation (sum, filter, format). The rent roll is downstream of processes that involve human judgment (payment recording, 2307 receipt), but the rent roll itself is purely a report.

**Why 5 and not 4:**
- No allocation decisions (those happen upstream in payment tracking)
- No regulatory interpretation (VAT status is deterministic from unit type + rent amount)
- No disputed amounts to resolve (2307 mismatches are flagged, not resolved, by the rent roll)
- The LIS is a strict subset — even simpler
- Export formatting is mechanical (column → cell mapping)

**The rent roll is the highest-leverage automation target** — it sits at the center of the data flow, consumes data from 5+ upstream processes, and feeds 8+ downstream consumers. Automating the rent roll eliminates the most time-consuming manual compilation step in the monthly close.

---

## 8. Verification Status

| Rule | Status | Sources |
|------|--------|---------|
| LIS requirements (RR 12-2011 / RMC 69-2009) | **Confirmed** | BIR RR 12-2011 PDF, PhilTaxation Blog, Clemente Aquino & Co. CPAs |
| VAT accrual basis for 2550Q (RR 3-2024) | **Confirmed** | Grant Thornton PH, KPMG PH, BIR 2550Q April 2024 guidelines |
| Income tax computation for 1702Q (CREATE Act) | **Confirmed** | BIR 1702Q guidelines, Acclime PH, Grant Thornton PH |
| 2307 tracking / SAWT format (RR 2-2006) | **Confirmed** | SC E-Library (RR 2-2006), Triple-i Consulting, Respicio & Co. |
| AFS disclosures (PFRS 16/PFRS 9) | **Confirmed** | Grant Thornton PH (PFRS 16 disclosure), PwC PH disclosure checklist |
| Filing deadline calendar | **Confirmed with correction** | MPM.ph, BIR eFPS guidelines, Juan.tax, Davao Accountants |

All 6 rules verified against 2+ independent sources. One correction applied: 1702Q deadline is 60 days after quarter-end (not 25th of following month); 0619-E applies only to first 2 months of each quarter.
