# Monthly Billing Generation

**Wave:** 2 (Process Analysis & Feature Spec)
**Analyzed:** 2026-02-26
**Dependencies:** crispina-models, crispina-services, rent-control-rules, corporate-rental-tax, utility-billing-regulations, accounting-agency-handoff

---

## 1. Process Description

**What:** Generate monthly billing statements for all active tenants, covering rent + utility charges + any other recurring or one-time charges. Each statement becomes a VAT Sales Invoice (the primary BIR document under RR 7-2024). The output is a per-tenant billing document showing line-item charges, VAT breakdown, prior balance, and total amount due.

**When:** Monthly, typically on the 1st of the month (or last business day of the prior month). Rent is due within the first 5 days of the month for RA 9653-covered units (Sec. 7 default), or per contract for commercial units. Invoices must be issued at accrual (when rent becomes due), not at payment.

**Who does it:** Property manager. Currently generates bills manually or via spreadsheet, prints/delivers to each unit.

**Frequency:** Monthly for all active tenants. Ad-hoc for mid-month charges (new tenant move-in, special assessments).

---

## 2. Current Method

**Manual / spreadsheet.** The property manager:
1. Looks up each tenant's current monthly rate (from lease contract or last billing)
2. Computes utility charges from meter readings (see `water-billing` and `electric-billing` aspects)
3. Adds any other charges (parking, common area dues if applicable)
4. Calculates VAT (12% for commercial; exempt for residential ≤ PHP 15,000/mo)
5. Determines prior balance from manual ledger
6. Writes or prints a billing statement per tenant
7. Delivers to tenant (under door, via messaging, or posted on unit)

No automated invoice numbering, no system-generated statements, no digital delivery.

---

## 3. Regulatory Rules

### 3.1 Invoice Issuance Timing (RR 7-2024 — EOPT Act)

Post-April 27, 2024, the billing cycle generates two BIR documents:

1. **VAT Sales Invoice** — issued when rent **becomes due** (accrual basis). This is the primary BIR document. Replaces the former Official Receipt as the document supporting input VAT claims.
2. **Official Receipt** — issued upon **actual payment receipt**. Now supplementary only.

**Implication:** Monthly billing = invoice generation. The system must produce a compliant VAT Sales Invoice at billing time, not at payment time. Output VAT is declared in the quarter the invoice is issued, regardless of collection.

**Legal basis:** RR 7-2024 (effective April 27, 2024); RA 11976 (EOPT Act); confirmed by Grant Thornton PH, PwC PH, KPMG PH advisories.

**Verification:** Confirmed (3 sources)

### 3.2 Default Due Date (RA 9653 Sec. 7)

For RA 9653-covered residential units (NCR, ≤ PHP 10,000/month): rent is due within the **first 5 days of each month**, unless the lease contract specifies a different schedule.

For commercial and non-covered residential units: due date per contract terms. Most commercial leases specify the 1st or 5th of the month.

**Implication:** The billing system must support per-lease due dates, with a default of the 5th for controlled units.

**Verification:** Confirmed (lawphil.net statutory text, Supreme Court E-Library, The Corpus Juris)

### 3.3 VAT Treatment — Residential vs. Commercial

| Tenant Type | Monthly Rent | VAT Treatment | Legal Basis |
|---|---|---|---|
| Residential | ≤ PHP 15,000/unit | **VAT-exempt** (permanent statutory exemption) | NIRC Sec. 109(1)(Q); RR 13-2018 |
| Residential | > PHP 15,000/unit | Combined with commercial for PHP 3M test | NIRC Sec. 109(1)(V); RR 13-2018 |
| Commercial | Any | VAT-able if lessor exceeds PHP 3M aggregate | NIRC Sec. 108; RR 16-2005 |

**Critical correction (from verification):** Residential units at or below PHP 15,000/month per unit enjoy a **permanent statutory VAT exemption** under NIRC Section 109(1)(Q). They remain exempt regardless of the lessor's total gross receipts. Only residential units **exceeding** PHP 15,000/month are combined with commercial receipts for the PHP 3M threshold test. The "mixed-use trap" described in `input/corporate-rental-tax.md` Scenario D overstates the scope — the trap applies only to residential units above PHP 15K, not to those at or below.

**Invoice notation requirements:**
- VAT-able invoices: Show base amount, VAT (12%), total. Mark as "VAT-registered" with TIN.
- VAT-exempt invoices: Mark "VAT-EXEMPT SALE" prominently. Do **not** show a VAT line.

**Verification:** Confirmed with correction (Respicio & Co., ReliaBooks, CPA Davao, LMA Law — 4 sources)

### 3.4 Sequential Invoice Numbering (NIRC Sec. 237; RR 18-2012)

- Invoices must be BIR-registered via Authority to Print (ATP) or CAS Permit
- Sequential, gapless numbering per establishment
- Each branch/establishment maintains its own series (head office: "000"; branches: "001", etc.)
- ATP valid for 3 years or until all serial numbers exhausted
- Gaps or duplications create audit risk and potential penalties (PHP 5,000–10,000 per violation)

**Verification:** Confirmed (Tax & Accounting Center Inc., Respicio & Co., RR 18-2012 text)

### 3.5 Mandatory Invoice Fields (RR 7-2024; NIRC Sec. 237)

Every billing statement / VAT Sales Invoice must contain:
1. Lessor corporation name and registered address
2. TIN (with branch code)
3. "VAT-registered" statement (if applicable)
4. Sequential invoice number
5. ATP number and approved serial range
6. Date of transaction (billing date)
7. Tenant name, address, TIN (required if invoice ≥ PHP 1,000 and buyer is VAT-registered)
8. Description: "Monthly Rental — Unit ___, [Property Address], covering [Period]"
9. Base amount (exclusive of VAT)
10. VAT amount (12%) as separate line — OR "VAT-EXEMPT SALE" notation
11. Total amount due (VAT-inclusive)
12. Prior balance (not BIR-required, but standard business practice)
13. Printer's name, address, TIN, accreditation number (on printed forms)

**Verification:** Confirmed (composite of RR 7-2024, NIRC 237, RR 18-2012)

### 3.6 Output VAT Accrual with Uncollected Receivable Credit (RR 3-2024)

- Output VAT must be declared in the quarter the invoice is issued
- If rent is not collected within the agreed credit term (per lease contract), the lessor may claim an **Output VAT Credit on Uncollected Receivables**
- The credit must be claimed in the **immediately following quarter** — one-quarter window only
- The lease contract serves as the "written agreement" establishing the credit term
- If subsequently collected, output VAT must be re-declared

**Implication:** The billing system must track invoice issuance date AND collection date to support the VAT credit claim. Uncollected invoices at quarter-end require flagging for the accountant.

**Legal basis:** RR 3-2024; NIRC Sec. 108; confirmed by PwC PH, Grant Thornton PH, Deloitte PH.

**Verification:** Confirmed (4 sources)

---

## 4. Formula / Decision Tree

### Monthly Billing Generation Algorithm

```
FOR each active_lease:
  tenant = lease.tenant
  rentables = lease.rentables

  FOR each rentable in rentables:
    charges = []

    -- 1. RENT CHARGE
    period = find_active_recurring_charge_period(lease, billing_month)
    base_rent = period.amount  -- pre-VAT, from pre-computed escalation
    vat_rate = determine_vat_rate(rentable, tenant, base_rent)
    charges.append(Charge(
      type=RENT,
      base_amount=base_rent,
      vat_rate=vat_rate,
      date_due=determine_due_date(lease, rentable),
      date_issued=billing_date
    ))

    -- 2. WATER CHARGE (if metered — see water-billing aspect)
    IF rentable.has_water_meter AND water_reading_available(rentable, billing_month):
      water_charge = compute_water_bill(rentable, billing_month)
      charges.append(water_charge)

    -- 3. ELECTRIC CHARGE (if metered — see electric-billing aspect)
    IF rentable.has_electric_meter AND electric_reading_available(rentable, billing_month):
      electric_charge = compute_electric_bill(rentable, billing_month)
      charges.append(electric_charge)

    -- 4. OTHER RECURRING CHARGES (common area dues, parking, etc.)
    FOR each other_recurring in lease.recurring_charges WHERE type != RENT:
      other_period = find_active_period(other_recurring, billing_month)
      IF other_period:
        charges.append(compute_charge(other_recurring, other_period))

  -- 5. CREATE TRANSACTION (billing batch)
  transaction = Transaction(
    description="Billing for {billing_month_label}",
    date_issued=billing_date,
    charges=all_charges_for_this_lease
  )

  -- 6. COMPUTE PRIOR BALANCE
  prior_balance = get_tenant_balance(tenant) - sum(charges in this transaction)

  -- 7. GENERATE INVOICE
  invoice = generate_invoice(
    invoice_number=next_sequential_number(),
    tenant=tenant,
    transaction=transaction,
    prior_balance=prior_balance,
    charges=charges
  )

  -- 8. RECORD INVOICE
  store_invoice(invoice)  -- triggers output VAT accrual for the quarter
```

### VAT Rate Determination

```
FUNCTION determine_vat_rate(rentable, tenant, base_rent):
  IF rentable.unit_type == RESIDENTIAL AND base_rent <= 15000.00:
    RETURN 0.0000  -- Permanent VAT exemption (NIRC Sec. 109(1)(Q))
  ELSE IF lessor.is_vat_registered:
    RETURN 0.1200  -- 12% VAT
  ELSE:
    RETURN 0.0000  -- Non-VAT (OPT applies separately, not on invoice)
```

### Due Date Determination

```
FUNCTION determine_due_date(lease, rentable):
  IF lease.custom_due_day IS NOT NULL:
    RETURN date(billing_year, billing_month, lease.custom_due_day)
  ELSE IF rentable.is_rent_controlled:
    RETURN date(billing_year, billing_month, 5)  -- RA 9653 Sec. 7 default
  ELSE:
    RETURN date(billing_year, billing_month, 1)  -- Business convention
```

---

## 5. Edge Cases and Special Rules

### 5.1 Pro-rated First/Last Month

New tenant moves in mid-month. Rent must be pro-rated:
- **Calendar-day method:** `monthly_rent × (days_remaining / days_in_month)`
- **30-day method:** `monthly_rent × (days_remaining / 30)` — common in PH leases
- Method should be specified in the lease contract. Default to calendar-day if unspecified.
- Pro-rated billing generates a partial-month invoice. The system needs a flag for pro-rated charges.

### 5.2 Lease Expired — Tacit Reconduction (Art. 1670)

After lease expiry + 15 days acquiescence, month-to-month lease begins. Billing continues at the same rate (terms revived except period). The system should:
- Continue generating monthly bills at the last applicable rate
- Flag the lease as "month-to-month" for visibility
- Not auto-escalate (no pre-computed periods exist for tacit reconduction)

### 5.3 Vacancy / Move-out Mid-Month

Unit vacated mid-month:
- Final billing should pro-rate rent to move-out date
- Utility charges based on final meter reading
- Security deposit deductions applied (see `security-deposit-lifecycle` aspect)
- No invoice generated for months after move-out

### 5.4 Multiple Rentables per Lease

One tenant leasing multiple sub-units (e.g., "Unit 102-A" and "Unit 102-B") under a single lease. Crispina's LeaseRentable M2M supports this. Billing options:
- **Single invoice** listing each unit's charges as separate line items (preferred for tenant convenience)
- **Separate invoices** per unit (required if units have different VAT treatment)

### 5.5 Billing Before Utility Readings Available

Water/electric meter readings may not be available when rent billing runs (e.g., Maynilad bill arrives mid-month). Options:
- **Separate billing runs:** Rent invoiced on the 1st; utility charges invoiced when readings are available. Separate invoice numbers.
- **Delayed combined bill:** Wait for all readings before generating the combined statement. Risk: invoice issued after due date.
- **Estimated billing:** Bill based on prior month's consumption; true-up on next bill. Common in practice but creates reconciliation complexity.

Recommendation: Separate billing runs — rent invoice on the 1st (deterministic), utility invoice when readings are in (data-dependent). This aligns with the two-document system and avoids delayed rent invoices.

### 5.6 VAT Status Change Mid-Year

If the lessor crosses the PHP 3M threshold mid-year:
- Must register for VAT within 30 days of the month the threshold is exceeded
- All invoices issued after VAT registration must include 12% VAT
- Invoices issued before registration remain non-VAT (3% OPT applied separately)
- The billing system must support a "VAT effective date" on the lessor entity

### 5.7 Corporate Tenant with EWT

For corporate tenants who withhold 5% EWT:
- Invoice shows gross amount (base + VAT)
- Tenant pays: `base_amount - (base_amount × 5%) + VAT`
- Example: PHP 100,000 base + PHP 12,000 VAT = PHP 112,000 invoice
  - Tenant pays: PHP 95,000 + PHP 12,000 = PHP 107,000 cash
  - Tenant withholds: PHP 5,000 (remits to BIR via 0619-E)
- The invoice itself does NOT show the EWT deduction — it shows the full amount. The EWT is a payment mechanism, not a billing adjustment.

### 5.8 Advance Rent Applied

If advance rent (last month's rent) was collected at lease start:
- In the final month of the lease, the advance rent is recognized as income
- The billing statement should show: "Less: Advance rent applied — PHP X"
- VAT was already declared on the advance at receipt (RR 7-2024). No double-counting.
- OR was already issued at receipt. No new OR for the applied advance.

### 5.9 Batch Billing Run vs. Individual

Two operational modes:
- **Batch run:** Generate all tenant invoices for the month in one operation. Preferred for monthly close.
- **Individual:** Generate a single tenant's invoice ad-hoc (for new tenants, corrections, or mid-month charges).

The system should support both. Batch run = iterate over all active leases. Individual = single lease.

### 5.10 Credit Notes / Billing Adjustments

If an invoice is issued in error (wrong amount, wrong tenant, duplicate):
- Cannot void a BIR-registered invoice — must issue a **Credit Memo** (Section 4.113-5 of RR 16-2005)
- Credit memo has its own sequential series
- Must reference the original invoice number
- Adjusts output VAT in the quarter the credit memo is issued

---

## 6. What Crispina Built

### Built

| Component | Status | Notes |
|---|---|---|
| RecurringCharge + RecurringChargePeriod | **Built** | Pre-computed escalation per lease year; lookup which period covers billing month |
| Charge model | **Built** | `base_amount` + `vat_rate_used` → hybrid `amount` (VAT-inclusive). Indexed on `(tenant_pk, rentable_pk, charge_type_pk, date_due)` |
| Transaction as billing batch | **Built** | Groups charges into transactions with description and date |
| ChargeType with VAT configuration | **Built** | `is_vat_inclusive`, `vat_rate` per charge type. Extensible to water/electric |
| VAT stored at charge-time | **Built** | Correct — rate frozen at issuance for audit trail |
| Multi-rentable lease | **Built** | LeaseRentable M2M junction supports one lease covering multiple units |

### Not Built (Key Gaps)

| Gap | Impact on Billing |
|---|---|
| **No invoice numbering** | Cannot generate BIR-compliant invoices without sequential numbering |
| **No billing statement template/generation** | No way to produce a formatted billing document |
| **Only 1 ChargeType seeded (Rent)** | Cannot bill water, electric, penalties, or other charges |
| **No `unit_type` on Rentable** | Cannot determine VAT treatment (commercial vs. residential) |
| **No `is_rent_controlled` flag** | Cannot apply RA 9653 default due date or escalation caps |
| **No invoice_date / invoice_number on Charge** | Invoice issuance not tracked (needed for VAT accrual timing) |
| **No batch billing run endpoint** | No way to generate all bills in one operation |
| **No billing statement delivery tracking** | No record of when/how statement was delivered to tenant |
| **No credit memo model** | Cannot issue corrections to erroneous invoices |
| **No prior balance on statement** | TransactionDetail computes per-transaction balance, not tenant-level running balance |
| **No advance rent tracking** | Cannot apply advance rent to final month's billing |
| **No pro-ration logic** | Cannot compute partial-month charges |
| **No billing schedule / due_day on Lease** | Cannot determine per-lease due date |

### Design Decisions Worth Preserving

1. **Pre-computed escalation via RecurringChargePeriod** — at billing time, simply look up the active period for the billing month. No recomputation needed.
2. **Base amount + VAT rate stored separately** — BIR-compliant, shows VAT as separate line.
3. **Transaction grouping** — one transaction per billing run per tenant maps cleanly to one invoice.
4. **ChargeType extensibility** — adding Water, Electric, Penalty charge types requires only seed data, not schema changes.

---

## 7. Lightweight Feature Spec

### 7.1 Data Model Additions

```
Rentable (enhanced)
  + unit_type: Enum(COMMERCIAL, RESIDENTIAL), NOT NULL
  + is_rent_controlled: Boolean, default False
  + floor_area_sqm: Decimal(8,2), nullable  -- for electric/common area apportionment

Lease (enhanced)
  + custom_due_day: Integer, nullable, CHECK(1..28)  -- per-lease due date override
  + status: Enum(ACTIVE, EXPIRED, MONTH_TO_MONTH, TERMINATED), NOT NULL

Charge (enhanced)
  + invoice_number: String(50), nullable   -- BIR sequential invoice number
  + invoice_date: Date, nullable           -- When invoice was issued (VAT accrual date)
  + is_vat_exempt: Boolean, default False  -- Flag for "VAT-EXEMPT SALE" notation

NEW: InvoiceSequence
  pk: UUID
  establishment_code: String(3), default "000"  -- BIR establishment code
  current_number: BigInteger, NOT NULL
  prefix: String(20), nullable         -- e.g., "INV-2026-"
  atp_number: String(50), NOT NULL     -- BIR Authority to Print reference
  atp_valid_from: Date
  atp_valid_until: Date
  series_start: BigInteger             -- First number in ATP-approved range
  series_end: BigInteger               -- Last number in ATP-approved range
  + UNIQUE(establishment_code)

NEW: BillingRun
  pk: UUID
  billing_month: Date (1st of month)   -- Period covered
  run_date: DateTime                    -- When the run was executed
  run_type: Enum(BATCH, INDIVIDUAL)
  status: Enum(DRAFT, FINALIZED, VOIDED)
  total_invoices: Integer
  total_amount: CurrencyDecimal
  created_by: String                   -- Who initiated the run

NEW: CreditMemo
  pk: UUID
  credit_memo_number: String(50), NOT NULL
  original_invoice_number: String(50), NOT NULL
  original_charge_pk: UUID (FK → Charge)
  reason: Text
  amount: CurrencyDecimal              -- Amount credited (base)
  vat_amount: CurrencyDecimal          -- VAT credited
  date_issued: Date
```

### 7.2 Billing Run Logic

```
FUNCTION run_monthly_billing(billing_month, run_type=BATCH):
  -- 1. Create BillingRun record (status=DRAFT)
  billing_run = create_billing_run(billing_month, run_type)

  -- 2. Get all active leases (ACTIVE or MONTH_TO_MONTH status)
  active_leases = query_leases(status IN (ACTIVE, MONTH_TO_MONTH))

  -- 3. For each lease, determine if already billed for this month
  FOR each lease in active_leases:
    IF exists_charge(lease, billing_month):
      SKIP  -- Already billed, prevent duplicates

    charges = generate_charges_for_lease(lease, billing_month)

    -- 4. Create Transaction grouping
    transaction = Transaction(
      description=f"Billing — {billing_month.strftime('%B %Y')}",
      date_issued=billing_run.run_date,
      billing_run_pk=billing_run.pk
    )

    -- 5. Assign invoice number (atomic increment)
    invoice_num = next_invoice_number()

    -- 6. Attach invoice metadata to each charge
    FOR each charge in charges:
      charge.invoice_number = invoice_num
      charge.invoice_date = billing_run.run_date
      charge.transaction_pk = transaction.pk

    -- 7. Generate billing statement document (PDF/email)
    statement = render_billing_statement(lease, transaction, charges, prior_balance)

  -- 8. Finalize billing run
  billing_run.status = FINALIZED
  billing_run.total_invoices = count
  billing_run.total_amount = sum
```

### 7.3 Invoice Number Generation (Atomic)

```
FUNCTION next_invoice_number():
  -- Must be atomic to prevent gaps/duplicates under concurrent access
  -- PostgreSQL: UPDATE ... RETURNING with row-level lock

  UPDATE invoice_sequence
  SET current_number = current_number + 1
  WHERE establishment_code = '000'
    AND current_number < series_end  -- ATP range check
  RETURNING current_number

  IF current_number >= series_end:
    RAISE "ATP series exhausted — renew Authority to Print"

  RETURN format_invoice_number(prefix, current_number)
  -- e.g., "INV-2026-000001"
```

### 7.4 Billing Statement Template

```
┌──────────────────────────────────────────────────────────┐
│  [LESSOR CORPORATION NAME]                               │
│  [Registered Address]                                    │
│  TIN: [XXX-XXX-XXX-000]    VAT-Registered               │
│  ATP No.: [XXXXXXXXXX]     Series: [XXXXXX–XXXXXX]      │
├──────────────────────────────────────────────────────────┤
│  BILLING STATEMENT / VAT SALES INVOICE                   │
│  Invoice No.: INV-2026-000042                            │
│  Date: March 1, 2026                                     │
│  Billing Period: March 2026                              │
│  Due Date: March 5, 2026                                 │
├──────────────────────────────────────────────────────────┤
│  TENANT: [Tenant Name / Business Name]                   │
│  TIN: [XXX-XXX-XXX-XXX]                                 │
│  Unit: [Unit Reference]  Property: [Property Name]       │
├──────────────────────────────────────────────────────────┤
│  Description                  Base Amount    VAT    Total │
│  ─────────────────────────────────────────────────────── │
│  Monthly Rent — Mar 2026     ₱25,000.00  ₱3,000  ₱28,000│
│  Water — Feb 2026 (8 cu.m.)    ₱525.00    ₱63.00   ₱588│
│  Electric — Feb 2026 (120 kWh) ₱1,573.74 ₱188.85 ₱1,763│
│  Common Area Water (pro-rata)   ₱150.00   ₱18.00   ₱168│
│  ─────────────────────────────────────────────────────── │
│  Subtotal (excl. VAT)       ₱27,248.74                  │
│  VAT (12%)                                    ₱3,269.85 │
│  TOTAL CURRENT CHARGES                       ₱30,518.59 │
│  ─────────────────────────────────────────────────────── │
│  Previous Balance                             ₱5,000.00 │
│  ─────────────────────────────────────────────────────── │
│  TOTAL AMOUNT DUE                           ₱35,518.59 │
├──────────────────────────────────────────────────────────┤
│  [For VAT-exempt units: "VAT-EXEMPT SALE" in place of   │
│   VAT column; no VAT line in totals]                     │
├──────────────────────────────────────────────────────────┤
│  Printed by: [BIR-accredited printer name, TIN, accred#]│
└──────────────────────────────────────────────────────────┘
```

### 7.5 Billing Statement for VAT-Exempt Residential Unit

```
│  Description                              Amount         │
│  ─────────────────────────────────────────────────────── │
│  Monthly Rent — Mar 2026                ₱8,500.00       │
│  Water — Feb 2026 (5 cu.m.)              ₱327.50       │
│  ─────────────────────────────────────────────────────── │
│  VAT-EXEMPT SALE                                         │
│  TOTAL CURRENT CHARGES                  ₱8,827.50       │
│  Previous Balance                            ₱0.00      │
│  TOTAL AMOUNT DUE                       ₱8,827.50       │
```

### 7.6 Downstream Data Flow

This process generates data consumed by:

| Consumer | Data Provided |
|---|---|
| **Tenant payment tracking** | Charges + transactions for payment allocation |
| **Rent roll preparation** | Invoice numbers, amounts billed, VAT breakdown per tenant |
| **Invoice log (for accountant)** | Sequential invoice register with per-invoice detail |
| **VAT return (2550Q)** | Output VAT totals per quarter (accrual basis) |
| **Uncollected receivable tracking** | Invoices unpaid past credit term → VAT credit claim |
| **SAWT / 2307 matching** | Invoice amounts as cross-reference for EWT certificates |
| **LIS (semi-annual)** | Monthly rental and unit data per RR 12-2011 format |

---

## 8. Automability Score: 5 / 5

**Justification:** Monthly billing generation is **purely deterministic**. Given:
- Active lease data (tenant, unit, rate period)
- Utility meter readings (when available)
- Prior balance (from payment tracking)
- VAT rate rules (unit type + rent amount)
- Invoice numbering sequence

...the system can generate every billing statement without human judgment. All inputs are structured, all formulas are defined, and the output format is specified by regulation.

**Why 5 and not 4:**
- Unlike payment tracking (which requires human intent for allocation), billing has no judgment calls
- The lease data and escalation periods are pre-computed
- VAT determination is a simple lookup (unit type + rent threshold)
- Invoice numbering is a monotonic counter
- Even edge cases (pro-ration, advance rent application) follow deterministic formulas
- The only human input needed is: "run billing for Month X" (or automate on schedule)

**Potential human touchpoints** (not reducing the score because they are upstream of this process):
- Utility meter readings must be entered before utility charges can be computed (input to this process, not part of it)
- A new tenant's lease must be created first (upstream process)
- Corrections require human decision to issue a credit memo (separate process)

---

## 9. Verification Status

| Rule | Status | Sources |
|---|---|---|
| Invoice at accrual (RR 7-2024) | **Confirmed** | Grant Thornton PH, PwC PH, KPMG PH |
| Default due date 5 days (RA 9653 Sec. 7) | **Confirmed** | lawphil.net (statutory text), SC E-Library, The Corpus Juris |
| VAT exemption ≤ PHP 15K residential (NIRC 109(1)(Q)) | **Confirmed with correction** | Respicio & Co., ReliaBooks, CPA Davao, LMA Law |
| Sequential invoice numbering (NIRC 237, RR 18-2012) | **Confirmed** | Tax & Accounting Center, Respicio & Co., RR 18-2012 text |
| Utility billing statement content | **Confirmed with nuance** | MWSS RO, ERC Res. 12 (2009), Respicio & Co. |
| Output VAT credit on uncollected receivables (RR 3-2024) | **Confirmed** | PwC PH, Grant Thornton PH, Deloitte PH, BIR RR 3-2024 |

All 6 rules verified against 2+ independent sources. One correction applied (Rule 3: residential ≤ PHP 15K is permanent exemption, not affected by aggregate receipts).

**Note:** The `input/corporate-rental-tax.md` Scenario D ("mixed-use trap") should be amended — the trap applies only to residential units **above** PHP 15,000/month, not to those at or below the threshold. Units ≤ PHP 15K are carved out entirely per NIRC Sec. 109(1)(Q).
