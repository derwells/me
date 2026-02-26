# Tenant Payment Tracking

**Wave:** 2 (Process Analysis & Feature Spec)
**Analyzed:** 2026-02-26
**Dependencies:** crispina-models, crispina-services, rent-control-rules, corporate-rental-tax, accounting-agency-handoff

---

## 1. Process Description

**What:** Track which tenants have paid, which haven't, running balances per tenant, and partial payment allocation across charges. Provide a dashboard view of payment status across all units.

**When:** Continuous — payments arrive throughout the month (mostly first 5 days per RA 9653 Sec. 7 default due date). Reconciliation happens monthly before accountant handoff (by 5th of following month).

**Who does it:** Property manager records payments as they arrive. Currently manual ledger or spreadsheet per tenant.

**Frequency:** Daily during collection period (1st–10th of month); monthly reconciliation; quarterly for 2307 matching.

---

## 2. Current Method

**Fully manual / spreadsheet.** The property manager maintains a ledger (physical or Excel) tracking:
- Monthly billings per tenant
- Payments received (date, amount, mode)
- Running balance per tenant

No automated balance computation, no aging analysis, no dashboard. The rent roll (see `accounting-agency-handoff.md`) is manually compiled monthly from this data.

---

## 3. Regulatory Rules

### 3.1 Payment Allocation Order (Civil Code Art. 1252–1254)

When a tenant owes multiple debts (e.g., multiple months of rent, penalties, utilities):

1. **Debtor designates** which debt the payment applies to at the time of payment (Art. 1252)
2. **Interest/penalties before principal** — mandatory, not suppletory (Art. 1253). If a balance includes both unpaid rent and accrued penalties, payments reduce the penalty component first
3. **If no designation by either party** — most onerous debt first; if debts are of same nature and burden, applied proportionately (Art. 1254)
4. **Creditor's receipt controls** — if tenant pays without designating and landlord issues a receipt attributing payment to a specific month, the tenant is bound

**Verification:** Confirmed via lawphil.net (Civil Code Book IV) and Respicio & Co. Status: **Confirmed**

### 3.2 Arrears Ejectment Threshold (RA 9653 Sec. 9(b)) — Residential Controlled Only

- Ejectment ground: arrears of **3 months total** (cumulative, not consecutive)
- "Total" means the accumulated unpaid amount equals 3 months' rent, even if partial payments were made
- Partial payments do **not** automatically reset the count
- However, accepting partial payments without written reservation risks a **waiver/estoppel defense** from the tenant
- **Demand is jurisdictional prerequisite** — must issue demand to pay and vacate before filing suit
- Applies only to RA 9653-covered units (residential, ≤ P10,000/month in NCR)

**Verification:** Confirmed via lawphil.net (RA 9653 Sec. 9) and Respicio & Co. ejectment commentary. Status: **Confirmed with nuance** — "total of 3 months" is cumulative per secondary sources.

### 3.3 Invoice and Receipt Issuance (RR 7-2024 / EOPT Act)

Post-April 27, 2024 two-document system:
1. **VAT Sales Invoice** — issued when rent **becomes due** (accrual basis). This is now the primary BIR document.
2. **Official Receipt** — issued upon **actual payment receipt**. Now supplementary only (cannot support input VAT claims).

**Implication for payment tracking:** Every billing event generates an invoice; every payment event generates a receipt. The system must track both document numbers per charge per payment.

**VAT on accrual basis:** Output VAT must be declared when invoice is issued, not when payment is received. RR 3-2024 provides an Output VAT Credit on Uncollected Receivables if rent is not collected within the agreed credit term.

**Verification:** Confirmed via Grant Thornton PH (RR 7-2024 clarification) and PwC PH (EOPT invoicing). Status: **Confirmed**

### 3.4 EWT Treatment of Payment Components

| Component | EWT 5%? | Notes |
|---|---|---|
| Base rent | Yes | RR 02-98, Sec. 2.57.2(B) |
| Advance rent | Yes, at payment | Full amount immediately |
| Security deposit (at receipt) | No | Liability, not income |
| Security deposit (applied to rent) | Yes | Reclassified as rental income |
| Utility pass-throughs (for lessor's account) | Yes, 5% | "Additional rental" per BIR |
| Utility pass-throughs (direct to utility co.) | Separate 2% | Not rental; services EWT |
| Late penalties | Likely yes, 5% | Treated as additional rental income |
| RPT paid by lessee for lessor | Yes, 5% | Specifically cited as additional rental |

**Verification:** Confirmed via PwC Tax Alert 7 (RMC 11-2024) and Forvis Mazars PH withholding guide. Status: **Confirmed with component rules**

### 3.5 Consignation (RA 9653 Sec. 9(b))

If lessor refuses payment, lessee may deposit by consignation at:
1. Court (judicial)
2. City/municipal treasurer
3. Barangay chairman
4. Bank in the name of and with notice to the lessor

Timeline: within 1 month of refusal; then within 10 days of each subsequent month. Valid consignation = valid payment (resets arrears). Applies only to RA 9653-covered units; commercial leases use Civil Code Art. 1256–1261 (court only).

**Verification:** Confirmed via lawphil.net (RA 9653) and Respicio & Co. consignation commentary. Status: **Confirmed**

### 3.6 Statute of Limitations on Unpaid Rent

| Lease Type | Article | Prescriptive Period |
|---|---|---|
| Written lease | Art. 1144 | **10 years** |
| Oral lease | Art. 1145 | 6 years |

- Each monthly installment prescribes independently from its due date
- Tacit reconduction preserves the 10-year period (Muller v. PNB, G.R. No. 215922)
- Interrupted by: court filing, written extrajudicial demand, written acknowledgment/partial payment (Art. 1155)

**Verification:** Confirmed via Supreme Court E-Library (Muller v. PNB) and Respicio & Co. prescription commentary. Status: **Confirmed** — corrected from initial 6-year hypothesis to 10 years for written leases.

---

## 4. What Crispina Built

### Payment Recording
- **Payment model:** `pk`, `amount`, `reference_number`, `date_issued`, `tenant_pk`
- **PaymentAllocation model:** junction between Payment and Transaction — `payment_pk`, `transaction_pk`, `amount`
- Supports partial payments: one payment can be split across multiple transactions
- Demo seed: P120 payment, P90 allocated → P30 balance remaining

### Transaction / Balance Architecture
- **Transaction** groups charges into billing batches (one transaction per billing run)
- **TransactionDetail** computes: `total_amount_due`, `total_amount_paid`, `total_balance`
- Balance = `sum(Charge.amount) - sum(PaymentAllocation.amount)` per transaction
- **Allocation is transaction-level only** — cannot specify "apply to water but not rent"

### Charge Model
- Stores `base_amount` (pre-VAT) + `vat_rate_used` (12%)
- Hybrid `amount` = VAT-inclusive total
- Indexed on `(tenant_pk, rentable_pk, charge_type_pk, date_due)`

### Key Gaps
| Gap | Impact |
|---|---|
| No tenant-level balance rollup | Cannot query "how much does Tenant X owe total?" without aggregating all transactions |
| No `payment_method` on Payment | Cash, bank transfer, GCash, check — needed for bank reconciliation |
| No `or_number` / `invoice_number` on Payment/Charge | BIR sequential numbering not tracked |
| No `deposited_date` on Payment | Bank reconciliation requires knowing when deposit cleared |
| No charge-level allocation | Cannot apply payment to specific charge type within a transaction |
| No late penalty model | No penalty computation, no ChargeType for penalties |
| No `is_corporate` flag on Tenant | Cannot determine EWT applicability |
| No `tin` on Tenant | Cannot generate 2307 tracking or invoices |
| No arrears alert / aging | No 3-month threshold monitoring for RA 9653 |
| No remarks/notes field on Payment | Cannot record tenant's payment designation (Art. 1252) |
| No consignation tracking | Cannot distinguish regular payments from consigned deposits |

### Design Patterns Worth Preserving
1. **Transaction as billing batch** — clean grouping of charges
2. **PaymentAllocation junction** — supports partial payments well
3. **VAT stored at charge-time** — correct for audit trail
4. **CurrencyDecimal (10,2) + ROUND_DOWN** — consistent, tenant-favorable

---

## 5. Lightweight Feature Spec

### 5.1 Data Model

```
Tenant (enhanced)
  + tin: String(20), nullable              -- BIR TIN for invoices/2307
  + is_corporate: Boolean, default False   -- Determines EWT applicability
  + is_vat_registered: Boolean, default False

Payment (enhanced)
  + payment_method: Enum(CASH, BANK_TRANSFER, CHECK, GCASH, OTHER)
  + or_number: String(50), nullable        -- Official Receipt number
  + check_number: String(50), nullable     -- For check payments
  + deposited_date: Date, nullable         -- Bank clearing date
  + remarks: Text, nullable                -- Tenant's payment designation (Art. 1252)

Charge (enhanced)
  + invoice_number: String(50), nullable   -- VAT Sales Invoice number
  + invoice_date: Date, nullable           -- Date invoice issued (accrual)

PaymentAllocation (enhanced)
  + charge_pk: UUID, nullable              -- Optional charge-level granularity
  -- If charge_pk is set: allocation is to a specific charge
  -- If charge_pk is null: allocation is to the transaction (legacy behavior)

NEW: TenantBalance (materialized view or computed)
  tenant_pk: UUID
  total_billed: CurrencyDecimal            -- sum of all Charge.amount
  total_paid: CurrencyDecimal              -- sum of all PaymentAllocation.amount
  total_balance: CurrencyDecimal           -- billed - paid
  oldest_unpaid_date: Date                 -- for aging
  months_in_arrears: Integer               -- count of unpaid billing periods
  arrears_alert: Boolean                   -- true if ≥ 3 months (RA 9653)

NEW: PaymentEvent (audit log)
  pk: UUID
  payment_pk: UUID
  event_type: Enum(RECEIVED, ALLOCATED, REVERSED, REFUNDED)
  amount: CurrencyDecimal
  notes: Text
  created_at: DateTime
```

### 5.2 Payment Recording Logic

```
FUNCTION record_payment(tenant_pk, amount, method, reference, date, designation):
  1. Create Payment record
  2. If designation provided (Art. 1252 — tenant specifies which debt):
     - Validate designated charges exist and belong to tenant
     - Allocate to designated charges in order specified
  3. Else (no designation — apply Art. 1253–1254 rules):
     a. Fetch all unpaid charges for tenant, ordered by:
        - Penalty/interest charges first (Art. 1253: interest before principal)
        - Then by most_onerous_score DESC (Art. 1254):
          * Secured charges > unsecured
          * Higher interest/penalty rate > lower
        - Then by date_due ASC (oldest first — standard FIFO within same class)
     b. Allocate payment amount across charges until exhausted
  4. For each allocated charge:
     - Create PaymentAllocation record
     - If charge fully paid: check if containing Transaction is now fully settled
  5. Update TenantBalance materialized view
  6. If tenant.arrears_alert was true and now months_in_arrears < 3:
     - Log arrears resolution event
  7. Return allocation summary (for receipt generation)
```

### 5.3 Balance Query Logic

```
FUNCTION get_tenant_balance(tenant_pk):
  -- Per-tenant rollup across all transactions
  SELECT
    t.pk as tenant_pk,
    SUM(c.amount) as total_billed,
    COALESCE(SUM(pa.amount), 0) as total_paid,
    SUM(c.amount) - COALESCE(SUM(pa.amount), 0) as balance,
    MIN(CASE WHEN c.amount > COALESCE(paid_per_charge, 0) THEN c.date_due END)
      as oldest_unpaid_date,
    COUNT(DISTINCT CASE WHEN c.amount > COALESCE(paid_per_charge, 0)
      THEN DATE_TRUNC('month', c.date_due) END) as months_in_arrears
  FROM charge c
  LEFT JOIN (allocation subquery) ...
  WHERE c.tenant_pk = tenant_pk
```

### 5.4 Dashboard Views

**Property-wide payment status (monthly):**

| Unit | Tenant | Monthly Due | Paid This Month | Balance | Months Arrears | Status |
|---|---|---|---|---|---|---|
| 101 | Santos, J. | P12,000 | P12,000 | P0 | 0 | Current |
| 102-A | Reyes Corp | P28,000 | P0 | P56,000 | 2 | Overdue |
| 102-B | Cruz, M. | P8,500 | P5,000 | P12,000 | 1 | Partial |

**Color coding:**
- Green: fully current (balance = 0)
- Yellow: partial payment or 1 month arrears
- Orange: 2 months arrears (warning)
- Red: 3+ months arrears (ejectment threshold for controlled units)

**Aging schedule (for accountant / AFS receivables note):**

| Tenant | Current | 1–30 days | 31–60 days | 61–90 days | 90+ days | Total |
|---|---|---|---|---|---|---|

### 5.5 Edge Cases

1. **Overpayment:** Payment exceeds total balance. Options: (a) hold as credit balance (apply to next billing), (b) refund. Must track credit balances separately — they are liabilities, not income.

2. **Partial payment by corporate tenant with EWT:** Corporate tenant pays P95,000 + P5,000 EWT withheld on P100,000 base rent. The payment record should reflect P95,000 cash received + P5,000 EWT credit. The charge is considered fully paid (P112,000 VAT-inclusive = P95,000 cash + P5,000 EWT + P12,000 VAT charged). Need to track the P5,000 EWT as a receivable from BIR (via 2307 matching).

3. **Bounced check:** Payment recorded, then reversed. Must support payment reversal that restores the original charge balances and creates an audit trail.

4. **Security deposit application:** When deposit is applied to unpaid rent at lease end, it triggers: (a) reclassification from liability to income, (b) VAT on the applied amount, (c) EWT on the applied amount (if corporate tenant). See `security-deposit-lifecycle` aspect.

5. **Multiple charge types in one transaction:** A single billing period may include rent + water + electric. If tenant pays a partial amount and doesn't designate, Art. 1253 applies (penalties first), then Art. 1254 (most onerous — likely the charge with the highest penalty rate).

6. **Consigned payments (RA 9653 units):** Must distinguish regular payments from consigned deposits. Consigned payments have a different verification workflow (joint affidavit for withdrawal). Track consignation venue and status.

7. **Post-dated checks (PDCs):** Common in PH commercial leases. Payment is recorded at check date, not receipt date. If PDC bounces, treatment is same as bounced check. Track check date separately from deposit date.

8. **GCash/bank transfer reconciliation:** Electronic payments may have transaction fees deducted. Must reconcile net amount received vs. gross amount paid by tenant.

9. **Advance rent (last month's rent):** Paid at lease start, recognized as income in the applicable month. Must track as deferred income until the month it covers, then reclassify.

10. **Payment during tacit reconduction:** After lease expiry + 15 days acquiescence (Art. 1670), month-to-month lease begins. Payments continue at the same rate (terms revived except period). The 10-year prescription applies per installment (Muller v. PNB).

### 5.6 Downstream Data Consumers

This process produces data consumed by:
- **Rent roll preparation** — "Amount Collected this Month" column, outstanding balance
- **Invoice log** — Invoice/receipt numbers issued per payment
- **2307 tracking** — EWT amounts to match against 2307 certificates received
- **Bank reconciliation** — Payment amounts, dates, check numbers, deposit dates
- **Aging receivables** — For AFS notes and accountant
- **Arrears monitoring** — For RA 9653 compliance (3-month threshold)
- **VAT return (2550Q)** — Output VAT on accrual; credit on uncollected receivables

---

## 6. Automability Score: 4 / 5

**Justification:** Payment recording is mostly deterministic — the data inputs (amount, date, method, reference) are straightforward, and allocation rules follow a clear legal hierarchy (Art. 1252–1254). Balance computation is purely formulaic. Dashboard generation and aging analysis are entirely automatable.

**Why not 5:**
- Tenant payment designation (Art. 1252) requires capturing human intent at payment time
- Bounced check / disputed payment handling requires human judgment
- Deciding whether to accept partial payment with or without reservation (waiver risk) is a business decision
- Consignation verification (did the tenant properly consign?) may require human review
- Corporate EWT matching (does the 2307 match what was actually withheld?) sometimes requires follow-up with the tenant

---

## 7. Verification Status

| Rule | Status | Sources |
|---|---|---|
| Payment allocation order (Art. 1252–1254) | **Confirmed** | lawphil.net (Civil Code Book IV), Respicio & Co. |
| 3-month arrears (RA 9653 Sec. 9(b)) | **Confirmed with nuance** | lawphil.net (RA 9653), Respicio & Co. ejectment commentary |
| Invoice/receipt timing (RR 7-2024) | **Confirmed** | Grant Thornton PH, PwC PH |
| EWT scope by component | **Confirmed** | PwC Tax Alert 7 (RMC 11-2024), Forvis Mazars PH |
| Consignation options | **Confirmed** | lawphil.net (RA 9653), Respicio & Co. |
| Prescriptive period | **Confirmed (corrected)** | SC E-Library (Muller v. PNB, G.R. 215922), Respicio & Co. |

All 6 rules verified against 2+ independent sources. No unresolved conflicts.
