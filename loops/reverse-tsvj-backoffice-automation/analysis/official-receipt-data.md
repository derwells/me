# Official Receipt & Invoice Data

**Wave:** 2 (Process Analysis & Feature Spec)
**Analyzed:** 2026-02-26
**Dependencies:** crispina-models, crispina-services, corporate-rental-tax, accounting-agency-handoff, monthly-billing-generation, tenant-payment-tracking

---

## 1. Process Description

**What:** Generate and manage the BIR-mandated documents for each rental transaction: (1) a **VAT Sales Invoice** at billing/accrual, and (2) a **supplementary receipt** (Official Receipt, Collection Receipt, or Payment Receipt) upon payment collection. This is a **dual-document system** introduced by the EOPT Act (RA 11976, effective April 27, 2024).

**CRITICAL CORRECTION from `input/corporate-rental-tax.md`:** Section 7 of that input file describes OR requirements that are now **partially outdated**. Under the pre-EOPT regime, the Official Receipt was the primary document for services/leases. Under RR 7-2024, the **Invoice replaces the OR** as the primary BIR document. ORs are now supplementary payment confirmation only — they cannot support input VAT claims by tenants. The invoice is where VAT is declared and recorded.

**When:**
- **Invoice:** Issued at billing (accrual basis) — when rent becomes due, not when payment is received
- **Supplementary receipt:** Issued upon actual receipt of payment (cash, check, bank transfer)
- Both documents are generated for each billing-and-collection cycle

**Who does it:** Property manager issues both documents. Currently manual — handwritten ORs from BIR-registered booklets; no invoice generation system.

**Frequency:** Monthly for each active tenant (invoice at billing + receipt upon payment). Ad-hoc for security deposit application/forfeiture, advance rent receipt, and penalty collections.

---

## 2. Current Method

**Fully manual.** The property manager:
1. Writes official receipts from pre-printed BIR-registered booklets when rent is collected
2. Manually fills in: tenant name, amount, period covered, date
3. OR booklets purchased from BIR-accredited printers with Authority to Print (ATP)
4. No separate invoice issued (pre-EOPT, OR was the sole document)
5. Carbon copies retained in the booklet; stubs accumulated in a box for the accountant
6. No digital record — the accountant re-keys OR data at month-end
7. Sequential numbering by booklet page, but gaps occur (voided ORs, skipped pages)

**Compliance gap as of 2026:** The business should have transitioned to the invoice-as-primary-document system by April 27, 2024. If still issuing ORs without invoices, this constitutes non-compliance with RR 7-2024 (penalty: PHP 1,000–50,000 per violation under NIRC Sec. 264(a)).

---

## 3. Regulatory Rules

### 3.1 EOPT Dual-Document Framework (RR 7-2024; RA 11976)

The Ease of Paying Taxes Act (RA 11976) eliminated the distinction between goods (invoice) and services (OR). **All sellers of goods and services — including lessors — now issue Invoices as the primary document.**

| Document | Role | When Issued | VAT Basis? | Input Tax Claim? |
|---|---|---|---|---|
| **VAT Sales Invoice** | Primary evidence of sale/lease | At accrual (when rent becomes due) | Yes — output VAT declared here | Yes — tenant claims input VAT from this |
| **Official Receipt / Collection Receipt** | Supplementary proof of payment | Upon actual receipt of payment | No | No — "THIS DOCUMENT IS NOT VALID FOR CLAIM OF INPUT TAX" |

**Key change for rental corporations:** Prior to EOPT, the OR was the basis for both VAT declaration and input VAT claims. Now the **invoice** triggers VAT obligations at accrual, and the receipt merely acknowledges payment.

**Legal basis:** RR 7-2024 Sec. 6 (invoice requirements); RR 7-2024 Sec. 8 (supplementary documents); RR 11-2024 (transitional amendments); RA 11976 Sec. 6 (amending NIRC Sec. 237)

**Verification:** Confirmed — Grant Thornton PH, PwC PH, KPMG PH, InCorp Philippines, MTF Counsel, Taxumo

### 3.2 Invoice Required Fields (RR 7-2024 Sec. 6(B))

Every VAT Sales Invoice for rent must contain:

1. Lessor corporation registered name (as on BIR Certificate of Registration)
2. TIN with branch code
3. Registered business address
4. "VAT-Registered" statement (or non-VAT statement if applicable)
5. The word "Invoice" clearly printed
6. Date of transaction (billing date)
7. Sequential serial number (gapless, per establishment)
8. ATP number and approved serial range
9. Buyer/tenant name, address, TIN (required if amount ≥ PHP 500 and buyer is VAT-registered; ≥ PHP 1,000 per RR 18-2012)
10. Description: nature of service, unit/property address, period covered
11. Quantity, unit cost (i.e., monthly rent amount)
12. Total sale amount (VAT-inclusive)
13. VAT amount as separate line item (12% if VATable)
14. For mixed transactions: breakdown into VATable Sales, VAT Amount, Zero-Rated Sales, VAT-Exempt Sales
15. "VAT-EXEMPT SALE" notation for qualifying residential units (≤ PHP 15K/mo)
16. BIR-accredited printer's name, TIN, and accreditation number (for manual/loose-leaf)

**Note on the PHP 500 threshold:** Under RR 7-2024, invoices are required for transactions ≥ PHP 500 (adjusted from the pre-EOPT PHP 100 threshold). All rental transactions will exceed this. VAT-registered persons must issue invoices regardless of amount.

**Verification:** Confirmed — RR 7-2024 full text (offshore-management.com.ph, grantthornton.com.ph), Tax & Accounting Center, Philippine CPA Blog

### 3.3 Supplementary Receipt Required Fields

ORs/Collection Receipts, now supplementary, should contain:

1. Lessor corporation name, TIN, address
2. "THIS DOCUMENT IS NOT VALID FOR CLAIM OF INPUT TAX" (mandatory stamp)
3. Sequential serial number (separate series from invoices)
4. Date of payment receipt
5. Payor/tenant name
6. Amount received
7. Payment mode (cash, check, bank transfer) and reference number
8. Description: "Payment for Invoice No. [XXX] — Monthly Rental, Unit [X], [Period]"
9. Cross-reference to the invoice being paid

**Note:** RR 7-2024 does not prescribe detailed field requirements for supplementary receipts (since they are no longer primary documents). The fields above reflect best practice for audit trail and accountant needs.

**Verification:** Confirmed with nuance — RR 7-2024 Sec. 8 establishes the supplementary status but does not prescribe specific fields beyond the "NOT VALID FOR INPUT TAX" stamp. Field list derived from accounting best practice (Grant Thornton PH, CloudCFO, Business Registration Philippines)

### 3.4 Separate Numbering Series

Invoices and receipts must maintain **separate sequential numbering series**, each with its own ATP:

- **Invoice series:** e.g., INV-2026-000001, INV-2026-000002, ...
- **Receipt series:** e.g., OR-2026-000001, OR-2026-000002, ...
- Each requires a separate ATP application (BIR Form 1906)
- Each establishment maintains its own series (head office "000", branches "001", etc.)
- Gapless numbering required — voided documents must be retained with "CANCELLED" marking

**Verification:** Confirmed — RR 7-2024 Sec. 6, RR 18-2012, Tax & Accounting Center, Grant Thornton PH

### 3.5 When to Issue Each Document

| Event | Invoice? | Receipt? | Notes |
|---|---|---|---|
| Monthly rent becomes due (1st of month) | **Yes** — accrual | No | VAT declared here |
| Tenant pays monthly rent | No (already invoiced) | **Yes** | Acknowledges payment |
| Advance rent collected at lease start | **Yes** — immediate | **Yes** — simultaneous | Both at same time (accrual = receipt for advance) |
| Security deposit collected | No — liability, not income | **Yes** — proof of receipt | Deposit is not revenue at collection |
| Security deposit applied to unpaid rent | **Yes** — now becomes rental income | **Yes** — internal application | VAT + EWT triggered |
| Security deposit forfeited | **Yes** — income recognition | **Yes** — internal application | VAT triggered |
| Late penalty charged | **Yes** — at billing | **Yes** — at collection | Penalty = gross receipts (VAT + RCIT) |
| Utility pass-through billed | **Yes** — at billing | **Yes** — at collection | VAT treatment per accountant decision |

**Verification:** Confirmed — RR 7-2024, RR 3-2024, Grant Thornton PH, Respicio & Co., Taxumo

### 3.6 Authority to Print (ATP)

**Legal basis:** NIRC Sec. 238; RR 18-2012; RR 6-2022

- File **BIR Form 1906** at RDO (Las Piñas: Revenue Region No. 8) for each document type
- Only **BIR-accredited printers** may print invoices/receipts
- ATP validity: **5 years** from issuance per RR 6-2022 (extended from the previous 3-year ATP validity under RMC 123-2022; note: `input/corporate-rental-tax.md` stated 3 years — this is now outdated)
- Renewal via ORUS portal, at least 60 days before expiry
- Separate ATP required for: (a) VAT Sales Invoices, (b) Official Receipts/Collection Receipts
- ATP specifies approved serial number range

**Correction:** The `input/corporate-rental-tax.md` states ATP validity is 3 years. Per RR 6-2022 and RMC 123-2022, the 5-year validity period was removed effective July 15, 2022 — ATPs now have **no expiry** as long as the business registration is active. The "3 years" referred to in RR 18-2012 was superseded. However, RR 7-2024 Sec. 6 references ATP validity without specifying a fixed period. **Practical guidance:** Check with Las Piñas RDO for current ATP validity rule; system should track ATP details regardless.

**Verification:** Partially conflicting — RR 18-2012 (3 years), RR 6-2022/RMC 123-2022 (removal of expiry), RR 7-2024 (references ATP but doesn't specify validity period). Documented as conflict.

### 3.7 Transitional Provisions (RR 11-2024)

For the transition from OR-as-primary to invoice-as-primary:

1. **Option A — Use ORs as supplementary:** Stamp "THIS DOCUMENT IS NOT VALID FOR CLAIM OF INPUT TAX" on remaining OR booklets. Continue using until consumed.
2. **Option B — Convert ORs to Invoices:** Strike through "Official Receipt", stamp "Invoice". Must add all Section 6(B) required fields. Valid until fully consumed (RR 11-2024 extended this from the Dec 31, 2024 cutoff in RR 7-2024).
3. **Inventory report** of unused ORs was due July 31, 2024, to the BIR
4. Must obtain newly printed Invoices with ATP before converted ORs are fully consumed
5. No BIR/RDO approval needed for stamping — taxpayer self-executes

**Post-December 31, 2024:** Any remaining ORs (whether converted or not) can only serve as supplementary documents. New invoices with proper ATP must be in use.

**Verification:** Confirmed — RR 11-2024 (BIR PDF), MPM.ph, Grant Thornton PH, PwC PH, InCorp Philippines

### 3.8 Electronic Invoicing System (EIS)

**Legal basis:** RR 11-2025 (EIS framework); RR 26-2025 (deadline extension)

- Mandatory EIS compliance deadline extended to **December 31, 2026** per RR 26-2025
- Applies to: large taxpayers, e-commerce businesses, CAS/CBA users, EOPT-covered entities
- **For a mid-size Las Piñas rental corporation:** Likely falls under "EOPT-covered entities" or "medium taxpayer" — should prepare for EIS compliance by end of 2026
- Technical requirement: structured JSON invoices transmitted to BIR via API within 3 days of transaction
- Electronic Sales Reporting System (ESRS) — separate future requirement; BIR to issue rules when infrastructure is ready
- Commissioner may further extend deadline (RR 26-2025 Sec. 3)

**Verification:** Confirmed — KPMG US (PH tax flash), Sovos, PNA (Philippine News Agency), PwC PH Tax Alert 29, Aureada Law, EDICOM

### 3.9 Penalties for Non-Compliance

| Violation | Penalty | Legal Basis |
|---|---|---|
| Non-issuance of invoice (using OR as primary post-April 27, 2024) | PHP 1,000–50,000 + 2–4 years imprisonment | NIRC Sec. 264(a) |
| Printing without BIR authority (no valid ATP) | PHP 500,000–10,000,000 + 6–10 years imprisonment | NIRC Sec. 264(b) |
| Using expired/unregistered receipts | PHP 20,000 first offense; PHP 50,000 subsequent | RMC 123-2022 |
| Missing required fields on invoice | Subject to compromise penalties per RMO 56-2000 | NIRC Sec. 264 |
| Failure to issue invoice → unreported income | 25% surcharge + 12% p.a. interest on tax deficiency | NIRC Sec. 248-249 |
| Business closure risk | "Oplan Kandado" temporary closure | NIRC Sec. 115 |

**Verification:** Confirmed — Respicio & Co., BIR RMC 77-2024, RMO 56-2000 (SC E-Library), Grant Thornton PH

---

## 4. Formula / Decision Tree

### Document Generation Decision Tree

```
ON BILLING EVENT (monthly rent, utility, penalty):
  1. Generate VAT Sales Invoice
     - Assign next sequential invoice number (from InvoiceSequence)
     - Determine VAT treatment:
       IF unit_type == RESIDENTIAL AND base_rent <= 15000:
         Mark "VAT-EXEMPT SALE"
         vat_amount = 0
       ELSE IF lessor.is_vat_registered:
         vat_amount = base_amount × 0.12
       ELSE:
         vat_amount = 0  (OPT applies separately)
     - Record invoice in billing system
     - Output VAT accrues in this quarter's 2550Q

ON PAYMENT RECEIPT EVENT:
  1. Generate Supplementary Receipt (OR / Collection Receipt)
     - Assign next sequential receipt number (from ReceiptSequence)
     - Cross-reference: invoice number(s) being paid
     - Record payment mode and reference
     - Stamp: "THIS DOCUMENT IS NOT VALID FOR CLAIM OF INPUT TAX"
  2. Link receipt to payment record in payment tracking system

ON SECURITY DEPOSIT COLLECTION:
  1. Generate Supplementary Receipt only (deposit is a liability, not income)
     - No invoice (no revenue recognition)
     - Receipt cross-references lease, not an invoice

ON SECURITY DEPOSIT APPLICATION/FORFEITURE:
  1. Generate VAT Sales Invoice (revenue recognition event)
     - Invoice for the amount applied/forfeited
     - VAT triggered (if VAT-registered)
     - EWT triggered (if corporate tenant)
  2. Generate Supplementary Receipt (internal application — no cash received)
     - Cross-references invoice and original deposit receipt

ON ADVANCE RENT COLLECTION:
  1. Generate VAT Sales Invoice (advance rent = immediate revenue under EOPT accrual)
  2. Generate Supplementary Receipt (cash received)
  Both issued simultaneously at collection
```

### Invoice Number Assignment (Atomic)

```
FUNCTION next_invoice_number(document_type: INVOICE | RECEIPT):
  -- Separate sequence per document type
  sequence = get_sequence(document_type, establishment_code='000')

  -- Atomic increment with range check
  UPDATE document_sequence
  SET current_number = current_number + 1
  WHERE document_type = $document_type
    AND establishment_code = '000'
    AND current_number < series_end
  RETURNING current_number

  IF no row updated:
    RAISE "ATP series exhausted for {document_type} — renew Authority to Print"

  RETURN format_number(sequence.prefix, current_number)
```

---

## 5. Edge Cases and Special Rules

### 5.1 Invoice Without Payment (Accrual Basis)

Under EOPT, the invoice is issued when rent becomes due — even if the tenant hasn't paid. The receipt is only issued when payment is actually collected. If a tenant never pays, there will be an invoice with no corresponding receipt. The uncollected receivables VAT adjustment (RR 3-2024) addresses the VAT consequence.

### 5.2 Payment Without Invoice (Deposit Collection)

Security deposits collected at lease start generate a receipt but no invoice (the deposit is a liability, not revenue). The invoice is only generated when the deposit is applied to rent or forfeited.

### 5.3 Partial Payment — Single Receipt

If a tenant pays PHP 15,000 against a PHP 25,000 invoice, one receipt is issued for PHP 15,000 referencing the invoice number. No new invoice. The balance remains on the original invoice until fully paid or written off.

### 5.4 Overpayment / Payment Covering Multiple Invoices

A single receipt may reference multiple invoices. The receipt should list each invoice paid and the amount allocated to each. This maps to the PaymentAllocation model in Crispina.

### 5.5 Voided Documents

If an invoice or receipt is issued in error:
- **Invoices:** Cannot be voided — must issue a **Credit Memo** (separate sequential series; see `monthly-billing-generation` analysis)
- **Receipts:** Can be marked "CANCELLED" — retain all copies, do not destroy. Write brief reason.

### 5.6 Non-Cash Payments

For check payments: receipt issued at check receipt date, not clearance date. If check bounces, the receipt remains valid (acknowledges receipt of check, not funds). A reversal entry handles the dishonored check.

### 5.7 GCash / Bank Transfer Payments

Electronic payments: receipt issued when payment notification is received and verified. Reference number = transaction ID from payment platform. No physical handoff needed — digital receipt may be issued.

### 5.8 Multiple Tenants Paying for One Unit (Co-tenancy)

If a unit has co-tenants (e.g., Crispina water calculator's co-tenancy model), one invoice is issued per the lease (to the primary tenant/billing entity), but separate receipts may be issued to each paying party if they pay independently.

### 5.9 ATP Exhaustion Mid-Period

If the approved serial number range runs out:
- System must alert well before exhaustion (e.g., at 80% consumption)
- File Form 1906 for new ATP before current range is consumed
- New ATP = new serial range. No overlap with previous range.
- System must support transitioning to new ATP seamlessly (track which ATP applies to which number range)

---

## 6. What Crispina Built

### Built

| Component | Status | Relevance to OR/Invoice |
|---|---|---|
| Charge (base_amount, vat_rate_used) | Built | Provides the data for invoice line items |
| Transaction (billing batch) | Built | Maps 1:1 to invoice (one transaction = one invoice) |
| Payment (amount, reference_number) | Built | Receipt basis — but missing critical fields |
| PaymentAllocation (payment ↔ transaction) | Built | Supports multi-invoice payment receipts |
| ChargeType (VAT configuration) | Built | Determines VAT treatment on invoice |

### Not Built (Key Gaps)

| Gap | Impact |
|---|---|
| **No invoice numbering system** | Cannot generate BIR-compliant invoices — no sequence, no ATP tracking |
| **No receipt numbering system** | Cannot generate supplementary receipts — no sequence |
| **No invoice_number/invoice_date on Charge** | No link from billing data to physical document |
| **No or_number on Payment** | No link from payment data to physical receipt |
| **No payment_method on Payment** | Cannot record mode of payment on receipt |
| **No TIN on Tenant** | Invoices require buyer TIN for VAT-registered tenants |
| **No is_corporate flag on Tenant** | Cannot determine EWT applicability shown on invoice |
| **No document template/generation** | No PDF/print output for either document |
| **No ATP tracking model** | Cannot validate serial ranges or alert on exhaustion |
| **No Credit Memo model** | Cannot handle invoice corrections |
| **No dual-document linking** | No mechanism to link invoice → receipt(s) for the same billing event |

### Design Patterns Worth Preserving

1. **Charge.base_amount + vat_rate_used** — directly maps to invoice line items (base + VAT separate)
2. **Transaction as billing batch** — one transaction naturally maps to one invoice
3. **PaymentAllocation** — supports the receipt → invoice cross-reference pattern
4. **CurrencyDecimal (10,2)** — matches BIR precision requirements

---

## 7. Lightweight Feature Spec

### 7.1 Data Model Additions

Models from other Wave 2 specs that this process depends on:

```
Tenant (enhanced — from tenant-payment-tracking)
  + tin: String(20), nullable
  + is_corporate: Boolean, default False
  + is_vat_registered: Boolean, default False

Charge (enhanced — from monthly-billing-generation)
  + invoice_number: String(50), nullable
  + invoice_date: Date, nullable
  + is_vat_exempt: Boolean, default False

Payment (enhanced — from tenant-payment-tracking)
  + payment_method: Enum(CASH, CHECK, BANK_TRANSFER, GCASH, OTHER)
  + receipt_number: String(50), nullable       -- Supplementary receipt number
  + receipt_date: Date, nullable               -- Date receipt issued
  + check_number: String(50), nullable
  + deposited_date: Date, nullable             -- For bank reconciliation
```

**New models specific to official receipt / invoice data:**

```
NEW: DocumentSequence
  pk: UUID
  document_type: Enum(INVOICE, RECEIPT, CREDIT_MEMO), NOT NULL
  establishment_code: String(3), default "000"
  current_number: BigInteger, NOT NULL, default 0
  prefix: String(20), nullable              -- e.g., "INV-2026-", "OR-2026-"
  atp_pk: UUID (FK → AuthorityToPrint), NOT NULL
  + UNIQUE(document_type, establishment_code)

NEW: AuthorityToPrint
  pk: UUID
  document_type: Enum(INVOICE, RECEIPT, CREDIT_MEMO), NOT NULL
  atp_number: String(50), NOT NULL
  series_start: BigInteger, NOT NULL
  series_end: BigInteger, NOT NULL
  date_issued: Date                          -- ATP issuance date
  date_expiry: Date, nullable                -- May be null per RR 6-2022
  printer_name: String(255), NOT NULL
  printer_tin: String(20), NOT NULL
  printer_accreditation: String(50), NOT NULL
  status: Enum(ACTIVE, EXHAUSTED, EXPIRED, CANCELLED)
  current_consumption: BigInteger, default 0 -- Track usage
  alert_threshold_pct: Integer, default 80   -- Alert at 80% consumed
  created_at: DateTime

NEW: IssuedDocument
  pk: UUID
  document_type: Enum(INVOICE, RECEIPT, CREDIT_MEMO)
  document_number: String(50), NOT NULL, UNIQUE
  atp_pk: UUID (FK → AuthorityToPrint)
  date_issued: Date, NOT NULL
  tenant_pk: UUID (FK → Tenant)
  tenant_name: String(255)                   -- Denormalized for document
  tenant_tin: String(20), nullable
  tenant_address: String(500), nullable
  description: Text                          -- "Monthly Rental — Unit X, Period"
  subtotal_vatable: CurrencyDecimal          -- Sum of VATable line items
  subtotal_exempt: CurrencyDecimal           -- Sum of VAT-exempt line items
  vat_amount: CurrencyDecimal                -- 12% on VATable portion
  total_amount: CurrencyDecimal              -- Grand total
  payment_method: Enum(...), nullable        -- Only for receipts
  payment_reference: String(100), nullable   -- Check #, transfer ref
  linked_invoice_pk: UUID, nullable          -- Receipt → Invoice link
  linked_receipt_pks: JSONB, nullable        -- Invoice → Receipt(s) link
  transaction_pk: UUID (FK → Transaction), nullable
  payment_pk: UUID (FK → Payment), nullable
  status: Enum(ISSUED, CANCELLED)
  cancellation_reason: Text, nullable
  created_at: DateTime

  -- For receipts: "THIS DOCUMENT IS NOT VALID FOR CLAIM OF INPUT TAX"
  -- auto-added to print template when document_type = RECEIPT

NEW: IssuedDocumentLine
  pk: UUID
  issued_document_pk: UUID (FK → IssuedDocument)
  line_number: Integer
  charge_pk: UUID (FK → Charge), nullable    -- Links to specific charge
  description: String(500)
  quantity: Integer, default 1
  unit_cost: CurrencyDecimal                 -- Pre-VAT amount
  vat_rate: PercentageDecimal
  vat_amount: CurrencyDecimal
  total_amount: CurrencyDecimal              -- VAT-inclusive
  is_vat_exempt: Boolean, default False
```

### 7.2 Invoice Generation Logic

```
FUNCTION generate_invoice(transaction: Transaction, tenant: Tenant,
                          charges: list[Charge]) -> IssuedDocument:

  -- 1. Get active invoice ATP and sequence
  atp = get_active_atp(document_type=INVOICE)
  IF atp.status != ACTIVE:
    RAISE "No active ATP for invoices — renew Authority to Print"

  -- 2. Atomic number assignment
  doc_number = next_document_number(INVOICE)

  -- 3. Classify charges
  vatable_charges = [c for c in charges if not c.is_vat_exempt]
  exempt_charges = [c for c in charges if c.is_vat_exempt]

  -- 4. Create document
  invoice = IssuedDocument(
    document_type=INVOICE,
    document_number=doc_number,
    atp_pk=atp.pk,
    date_issued=transaction.date_issued,
    tenant_pk=tenant.pk,
    tenant_name=tenant.billing_name or tenant.full_name,
    tenant_tin=tenant.tin,
    description=f"Monthly Rental — {transaction.description}",
    subtotal_vatable=sum(c.base_amount for c in vatable_charges),
    subtotal_exempt=sum(c.base_amount for c in exempt_charges),
    vat_amount=sum(c.base_amount * c.vat_rate_used for c in vatable_charges),
    total_amount=sum(c.amount for c in charges),
    transaction_pk=transaction.pk,
    status=ISSUED
  )

  -- 5. Create line items
  FOR i, charge in enumerate(charges):
    IssuedDocumentLine(
      issued_document_pk=invoice.pk,
      line_number=i+1,
      charge_pk=charge.pk,
      description=charge.charge_type.billing_name + " — " + charge.period_description,
      quantity=1,
      unit_cost=charge.base_amount,
      vat_rate=charge.vat_rate_used,
      vat_amount=charge.base_amount * charge.vat_rate_used,
      total_amount=charge.amount,
      is_vat_exempt=(charge.vat_rate_used == 0)
    )

  -- 6. Update charge records with invoice reference
  FOR each charge in charges:
    charge.invoice_number = doc_number
    charge.invoice_date = transaction.date_issued

  -- 7. Check ATP consumption and alert
  atp.current_consumption += 1
  IF atp.current_consumption >= atp.series_end * (atp.alert_threshold_pct / 100):
    create_alert("ATP nearing exhaustion — renew Form 1906")

  RETURN invoice
```

### 7.3 Receipt Generation Logic

```
FUNCTION generate_receipt(payment: Payment, allocations: list[PaymentAllocation],
                          tenant: Tenant) -> IssuedDocument:

  -- 1. Get active receipt ATP and sequence
  doc_number = next_document_number(RECEIPT)

  -- 2. Resolve which invoices are being paid
  invoice_refs = []
  FOR each alloc in allocations:
    transaction = alloc.transaction
    invoice = get_invoice_for_transaction(transaction)
    IF invoice:
      invoice_refs.append(invoice.document_number)

  -- 3. Create receipt document
  receipt = IssuedDocument(
    document_type=RECEIPT,
    document_number=doc_number,
    date_issued=payment.date_issued,
    tenant_pk=tenant.pk,
    tenant_name=tenant.billing_name or tenant.full_name,
    tenant_tin=tenant.tin,
    description=f"Payment received — {', '.join(invoice_refs)}",
    subtotal_vatable=0,     -- Receipt doesn't repeat VAT computation
    subtotal_exempt=0,
    vat_amount=0,
    total_amount=payment.amount,
    payment_method=payment.payment_method,
    payment_reference=payment.reference_number or payment.check_number,
    linked_invoice_pk=invoices[0].pk if len(invoices) == 1 else None,
    payment_pk=payment.pk,
    status=ISSUED
  )

  -- 4. Update payment record
  payment.receipt_number = doc_number
  payment.receipt_date = payment.date_issued

  -- 5. Update linked invoice(s)
  FOR each invoice in resolved_invoices:
    invoice.linked_receipt_pks = (invoice.linked_receipt_pks or []) + [receipt.pk]

  RETURN receipt
```

### 7.4 Document Templates

**Invoice template (VATable):**
```
┌──────────────────────────────────────────────────────────┐
│  [LESSOR CORPORATION NAME]                  VAT SALES    │
│  [Registered Address]                       INVOICE      │
│  TIN: [XXX-XXX-XXX-000]    VAT-Registered               │
│  ATP No.: [XXXXXXXXXX]     Series: [XXXXXX–XXXXXX]      │
├──────────────────────────────────────────────────────────┤
│  Invoice No.: INV-2026-000042                            │
│  Date: March 1, 2026                                     │
├──────────────────────────────────────────────────────────┤
│  SOLD TO: [Tenant Name / Business Name]                  │
│  TIN: [XXX-XXX-XXX-XXX]                                 │
│  Address: [Tenant Address]                               │
│  Unit: [Unit Reference]  Property: [Property Name]       │
├──────────────────────────────────────────────────────────┤
│  Qty  Description              Unit Cost    Amount       │
│  ─────────────────────────────────────────────────────── │
│   1   Monthly Rent Mar 2026   ₱25,000.00  ₱25,000.00   │
│   1   Water — Feb 2026           ₱525.00     ₱525.00   │
│   1   Electric — Feb 2026      ₱1,573.74   ₱1,573.74   │
│  ─────────────────────────────────────────────────────── │
│  VATable Sales:                           ₱27,098.74    │
│  VAT (12%):                                ₱3,251.85    │
│  VAT-Exempt Sales:                             ₱0.00    │
│  TOTAL AMOUNT DUE:                       ₱30,350.59    │
├──────────────────────────────────────────────────────────┤
│  Printed by: [Printer name, TIN, Accreditation #]        │
└──────────────────────────────────────────────────────────┘
```

**Receipt template (supplementary):**
```
┌──────────────────────────────────────────────────────────┐
│  [LESSOR CORPORATION NAME]                  OFFICIAL     │
│  [Registered Address]                       RECEIPT      │
│  TIN: [XXX-XXX-XXX-000]                                 │
├──────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐   │
│  │ THIS DOCUMENT IS NOT VALID FOR CLAIM OF INPUT TAX│   │
│  └──────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────┤
│  OR No.: OR-2026-000042                                  │
│  Date: March 5, 2026                                     │
├──────────────────────────────────────────────────────────┤
│  RECEIVED FROM: [Tenant Name]                            │
│  THE SUM OF: Thirty Thousand Three Hundred Fifty         │
│              Pesos and 59/100 (₱30,350.59)              │
│  IN PAYMENT OF: Invoice No. INV-2026-000042              │
│                 Monthly Rental + Utilities, Mar 2026     │
│  MODE OF PAYMENT: Bank Transfer                          │
│  REFERENCE: TRN-20260305-ABCD1234                        │
├──────────────────────────────────────────────────────────┤
│  Printed by: [Printer name, TIN, Accreditation #]        │
└──────────────────────────────────────────────────────────┘
```

### 7.5 Downstream Data Consumers

| Consumer | Data Provided | From Which Document |
|---|---|---|
| Rent roll — Invoice Number column | Invoice serial number | Invoice |
| Rent roll — Amount Collected column | Receipt amount | Receipt |
| Accountant — Invoice Log | Full invoice register (sequential) | Invoice |
| BIR 2550Q — Output VAT | VAT amounts from invoices | Invoice |
| BIR 1702Q — Gross Income | Subtotals from invoices | Invoice |
| SAWT — 2307 reconciliation | Invoice amounts vs. 2307 tax base | Invoice |
| Bank reconciliation | Receipt reference numbers | Receipt |
| Cash receipts journal | Receipt amounts + dates | Receipt |
| EIS transmission (future) | Structured JSON invoice data | Invoice |

### 7.6 ATP Management Workflow

```
ATP LIFECYCLE:
  1. APPLY: File Form 1906 at RDO for each document type
     - Specify: document type (Invoice/Receipt), serial range, printer details
  2. RECEIVE: BIR issues ATP → enter into system (AuthorityToPrint record)
  3. USE: System assigns numbers from approved range
  4. MONITOR: Alert at configurable threshold (default 80% consumed)
  5. RENEW: File Form 1906 for new ATP before current range exhausted
  6. TRANSITION: Switch DocumentSequence to new ATP; mark old as EXHAUSTED

REORDER ALERT:
  IF atp.current_consumption >= (atp.series_end - atp.series_start) * 0.80:
    create_alert(
      type=ATP_LOW,
      message=f"{atp.document_type} ATP {atp.atp_number}: "
              f"{remaining} numbers remaining. Reorder from BIR-accredited printer."
    )
```

---

## 8. Automability Score: 4 / 5

**Justification:** Invoice and receipt generation is **largely deterministic** — given billing data (from monthly billing generation) and payment data (from payment tracking), both documents can be auto-generated with correct numbering, VAT computation, and formatting.

**Why 4 and not 5:**
- **ATP management requires human action:** Applying for ATP (Form 1906 at RDO), selecting a printer, and physical receipt of printed booklets are manual processes
- **Physical document handling:** If using manual/loose-leaf forms, someone must physically prepare and deliver documents. Digital generation reduces but doesn't eliminate this.
- **Security deposit application decision:** The decision to apply a deposit to unpaid rent is human judgment — but once decided, the invoice/receipt generation is automatic
- **EIS compliance (future):** System registration, API certification, and JSON format validation will require technical setup and BIR coordination

**Why not 3:**
- All VAT computations are deterministic (unit type + rent threshold)
- Sequential numbering is a simple counter
- Template population is mechanical
- Cross-referencing invoices ↔ receipts ↔ payments is a data operation
- ATP monitoring is automatable (alert thresholds)

---

## 9. Verification Status

| Rule | Status | Sources |
|------|--------|---------|
| Invoice replaces OR as primary document (RR 7-2024) | **Confirmed** | Grant Thornton PH, PwC PH, KPMG PH, InCorp Philippines, MTF Counsel |
| RR 11-2024 transitional provisions (stamp/convert) | **Confirmed** | RR 11-2024 (BIR PDF), MPM.ph, Grant Thornton PH, PwC PH, InCorp Philippines |
| Invoice required fields (Sec. 6(B)) | **Confirmed** | RR 7-2024 full text, Tax & Accounting Center, Grant Thornton PH, Philippine CPA Blog |
| Separate numbering series (Invoice ≠ Receipt) | **Confirmed** | RR 7-2024, RR 18-2012, Tax & Accounting Center, Grant Thornton PH |
| When to issue invoice vs. receipt | **Confirmed** | RR 7-2024, RR 3-2024, Grant Thornton PH, Respicio & Co., Taxumo |
| ATP validity period | **Conflicting** | RR 18-2012 (3 years), RR 6-2022/RMC 123-2022 (removal of expiry), RR 7-2024 (unspecified) |
| EIS deadline Dec 31, 2026 (RR 26-2025) | **Confirmed** | KPMG, Sovos, PNA, PwC PH, Aureada Law, EDICOM |
| Penalties for non-issuance (Sec. 264) | **Confirmed** | Respicio & Co., BIR RMC 77-2024, RMO 56-2000, Grant Thornton PH |
| Supplementary receipt fields (best practice) | **Confirmed with nuance** | RR 7-2024 Sec. 8 (status only); field list from accounting best practice |
| Security deposit — receipt only, no invoice at collection | **Confirmed** | RR 7-2024, BIR Ruling DA-334-2004, RMC 11-2024 |

9/10 rules confirmed; 1 conflicting (ATP validity — documented). 0 unverified.
