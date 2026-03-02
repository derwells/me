# Cross-Cutting Concerns Extract — TSVJ Backoffice Web App

*Extracted from: `input/process-catalog.md` (14 processes + foundation)*
*Purpose: Cross-cutting concerns that span multiple processes and must be handled consistently in the web app*

---

## 1. VAT Treatment Matrix

**Affects:** P1, P2, P3, P4, P5, P7, P11, P12, P13, P14
**Core principle:** Every `Charge` record carries a `vat_rate` frozen at creation time. VAT treatment is determined per charge based on three factors: unit type, rent amount, and lessor VAT registration status.

### 1.1 VAT Determination Logic

```
INPUT: charge_type, lease.lease_regime, rentable.unit_type,
       recurring_charge_period.amount (current rent), lessor_vat_status

IF charge_type = WATER_PASSTHROUGH:
    → vat_rate = 0.00  (NOT VATable — landlord as conduit, BIR RR 16-2005)

ELSE IF charge_type = ELECTRIC_PASSTHROUGH:
    → vat_rate = PENDING  (CONFLICTING — requires accountant configuration)
    → See §1.4 Conflicting Rules

ELSE IF unit_type = RESIDENTIAL AND current_monthly_rent ≤ PHP 15,000:
    → vat_rate = 0.00  (permanent VAT exemption, NIRC Sec. 109(1)(Q))

ELSE IF lessor_aggregate_annual_receipts ≤ PHP 3,000,000:
    → vat_rate = 0.00  (below VAT threshold)

ELSE:
    → vat_rate = 0.12  (12% VAT)
```

### 1.2 VAT Scenarios

| # | Scenario | VAT Rate | Legal Basis | Processes | Design Impact |
|---|----------|:--------:|-------------|-----------|---------------|
| V1 | Residential rent ≤ PHP 15K/month | 0% (exempt) | NIRC 109(1)(Q) | P5, P11, P12 | `Charge.is_vat_exempt = true`; excluded from 2550Q VATable sales |
| V2 | Commercial rent (or residential > PHP 15K) | 12% | NIRC Sec. 108 | P5, P7, P11, P12, P13 | Standard VAT; included in 2550Q |
| V3 | Water pass-through | 0% (not VATable) | RR 16-2005 | P2, P5 | `ChargeType.WATER` always 0% regardless of unit type |
| V4 | Electric pass-through | **CONFLICTING** | EOPT Act vs earlier BIR RRs | P3, P5 | Configurable per `AppSettings`; accountant decides |
| V5 | Penalty income | 12% | Part of gross receipts | P4, P12 | Same VAT rule as parent rent charge |
| V6 | Deposit application/forfeiture | 12% | BIR Ruling 118-12; RR 16-2005 | P7, P12 | Tax reclassification at application, not at collection |
| V7 | Input VAT from supplier expenses | Creditable | NIRC Sec. 110 | P14, P12 | Only from VAT-registered suppliers; mixed-operation apportionment |
| V8 | Uncollected receivables adjustment | Deductible | RR 3-2024 | P5, P12 | One-quarter claim window for output VAT deduction from 2550Q |

### 1.3 VAT-Related Data Fields

| Entity | Field | Type | Purpose |
|--------|-------|------|---------|
| Charge | `vat_rate` | decimal(4,2) | Frozen at charge creation; 0.00 or 0.12 |
| Charge | `vat_amount` | decimal(10,2) | `base_amount × vat_rate`, rounded to 2 decimals |
| Charge | `is_vat_exempt` | boolean | True for residential ≤ PHP 15K |
| ChargeType | `default_vat_rate` | decimal(4,2) | Default for this charge type (overridable per scenario) |
| ChargeType | `is_vatable` | boolean | Whether this type is ever subject to VAT |
| Tenant | `is_vat_registered` | boolean | Tenant's own VAT status (for 2307 purposes) |
| SupplierPayee | `is_vat_registered` | boolean | Determines input VAT creditability |
| OutputVATSummary | `vatable_sales`, `exempt_sales`, `output_vat`, `input_vat` | decimal(12,2) | Quarterly VAT summary for 2550Q |
| InputVATRegister | `apportionment_pct` | decimal(5,2) | Mixed-operation: VATable revenue ÷ total revenue |

### 1.4 Conflicting VAT Rules (Require Accountant Configuration)

**Electric pass-through VAT (V4):** The EOPT Act (RA 11976) and CIR v. Tours Specialists case suggest at-cost pass-throughs may be excludable from VAT base. However, earlier BIR RRs (RR 16-2005) treated utility pass-throughs as part of gross receipts. This is an unresolved conflict.

**Web app design:** Provide an `AppSettings.electric_vat_treatment` field with values: `VATABLE` (12%), `EXEMPT` (0%), `PENDING` (flag for review). Default to `PENDING` to force explicit accountant decision. Once set, all future electric charges use this rate. Display a warning banner until configured.

### 1.5 Threshold Crossing

When a controlled residential unit's rent lawfully exceeds PHP 10,000/month via escalation (P1), the unit exits rent control. This may change VAT treatment if rent also exceeds PHP 15,000/month.

**Web app design:** `EscalationEvent.threshold_crossed = true` triggers: (1) lease regime reclassification alert, (2) next billing run uses updated VAT logic for that unit. The `is_rent_controlled` field is **derived** (computed at query time from `unit_type` + current rent), not stored.

### 1.6 VAT Computation Rule

```
vat_amount = ROUND(base_amount × vat_rate, 2)  -- standard banker's rounding
total_amount = base_amount + vat_amount
```

All monetary computations use PostgreSQL `numeric(p,s)` — never `float` or `double`. Drizzle ORM maps this to string-based decimal in JavaScript (use a library like `decimal.js` or `big.js` for client-side arithmetic).

---

## 2. EWT (Expanded Withholding Tax) Rules

**Two distinct EWT contexts in this system:**
1. **EWT on rent (5%)** — corporate tenants withhold on payments to the lessor (§2.1)
2. **EWT on supplier payments (2-15%)** — the corporation withholds on payments to its suppliers (§2.2)

### 2.1 EWT on Rent (5% Creditable Withholding Tax)

**Affects:** P4, P5, P6, P7, P11, P12
**Legal basis:** RR 02-98, Sec. 2.57.2(B)
**Trigger:** `Tenant.is_corporate = true`

**Rule:** Corporate tenants withhold 5% EWT on rental payments. The withholding applies to the **base amount (excluding VAT)** and extends to:

| Income Type | EWT Applies? | Base Amount | Processes |
|-------------|:------------:|-------------|-----------|
| Base rent | Yes — 5% | `Charge.base_amount` (pre-VAT) | P5, P6 |
| Penalty income | Yes — 5% | `PenaltyCharge.final_penalty` | P4, P6 |
| Utility pass-throughs "for lessor's account" | Yes — 2% (reimbursement) | Utility charge amount | P2, P3, P6 |
| Security deposit application | Yes — 5% | Applied amount | P7 |
| RPT paid by lessee for lessor | Yes — varies | RPT amount | P6 |

**Payment reconciliation formula:**
```
invoice_total = base_amount + vat_amount
cash_received + ewt_withheld = invoice_total
WHERE ewt_withheld = base_amount × 0.05
```

**2307 Certificate Tracking:**
- Corporate tenants must issue Form 2307 within 20 days after quarter-end (RR 02-98 Sec. 2.58)
- The system must track: `expected_amount` → `received_date` → `received_amount` → `is_reconciled` → `delivered_to_accountant_date`
- Mismatches between expected and received amounts must be flagged
- Feed into SAWT (Summary Alphalist of Withholding Tax at Source) for 1702Q filing

**EWT-Related Data Fields:**

| Entity | Field | Type | Purpose |
|--------|-------|------|---------|
| Tenant | `is_corporate` | boolean | Determines if EWT applies |
| Payment | `ewt_withheld` | decimal(10,2) | EWT amount deducted by corporate tenant |
| TenantBalance (view) | `total_ewt` | decimal(12,2) | Sum of all EWT withheld by this tenant |
| Form2307Record | `expected_amount`, `received_amount` | decimal(10,2) | Quarterly 2307 tracking |
| SAWTRecord | `tax_withheld` | decimal(10,2) | From collected 2307s, for SAWT attachment |

### 2.2 EWT on Supplier Payments (Corporation as Withholding Agent)

**Affects:** P14, P12
**Legal basis:** RR 02-98
**Trigger:** Any payment to a supplier/payee

**EWT Rate Matrix (14 categories, by payee type):**

| Payee Type | EWT Rate Range | Determination |
|------------|:--------------:|---------------|
| Individual, non-VAT | 2-15% by ATC code | `ExpenseCategory.ewt_rate_individual` |
| Individual, VAT-registered | 2-15% by ATC code | Same rates, but input VAT also creditable |
| Corporate, non-large taxpayer | 2-15% by ATC code | `ExpenseCategory.ewt_rate_corporate` |
| Corporate, large taxpayer | Same rates | `SupplierPayee.is_large_taxpayer` flag |

**Common rental property expense ATC codes:**

| ATC Code | Description | Individual Rate | Corporate Rate |
|----------|-------------|:--------------:|:--------------:|
| WC100 | Professional fees | 10% | 10% |
| WC120 | Contractor services | 2% | 2% |
| WC157 | Rental of property | 5% | 5% |
| WC158 | Rental of personal property | 5% | 5% |
| WC160 | Payments to suppliers of services | 2% | 2% |

**EWT Computation:**
```
ewt_amount = ROUND(gross_amount × ewt_rate, 2)
net_payment = gross_amount - ewt_amount + vat_amount  (VAT is NOT withheld)
```

**Filing obligations generated:**
- Monthly: Form 0619-E (remittance)
- Quarterly: Form 1601-EQ + QAP (Quarterly Alphalist of Payees)
- Annual: Form 1604-E + annual alphalist
- Per-supplier: Form 2307 (certificate of tax withheld)

**EWT Supplier Data Fields:**

| Entity | Field | Type | Purpose |
|--------|-------|------|---------|
| SupplierPayee | `type` | ENUM(INDIVIDUAL, CORPORATE) | Determines rate column |
| SupplierPayee | `is_vat_registered` | boolean | Determines input VAT creditability |
| SupplierPayee | `is_large_taxpayer` | boolean | May affect EWT rate |
| ExpenseCategory | `ewt_rate_individual` | decimal(4,2) | Rate for individual payees |
| ExpenseCategory | `ewt_rate_corporate` | decimal(4,2) | Rate for corporate payees |
| DisbursementVoucher | `ewt_withheld` | decimal(10,2) | Auto-computed from category × payee type |
| EWTWithheldRegister | `ewt_amount` | decimal(10,2) | Per-supplier, per-period record |

---

## 3. Tenant Type Bifurcation

**Affects:** P1, P2, P3, P4, P5, P6, P7, P8, P9, P10 (all processes except P11-P14 which consume but don't differentiate)
**Core principle:** Almost every business rule has a different version for residential controlled vs. commercial tenants.

### 3.1 Classification Hierarchy

```
Rentable.unit_type: RESIDENTIAL | COMMERCIAL
    │
    └─► Lease.lease_regime: CONTROLLED_RESIDENTIAL | NON_CONTROLLED_RESIDENTIAL | COMMERCIAL
            │
            └─► Derived: is_rent_controlled
                  = (unit_type = RESIDENTIAL) AND (current_rent ≤ PHP 10,000/month)
```

**Three regimes:**

| Regime | When | Governing Law |
|--------|------|---------------|
| CONTROLLED_RESIDENTIAL | unit_type = RESIDENTIAL, rent ≤ PHP 10K | RA 9653 (Rent Control Act) |
| NON_CONTROLLED_RESIDENTIAL | unit_type = RESIDENTIAL, rent > PHP 10K (lawful increase or new tenant) | Civil Code (freedom of contract) |
| COMMERCIAL | unit_type = COMMERCIAL | Civil Code Art. 1305-1306 |

**Vacancy decontrol:** When a controlled unit becomes vacant and is re-leased, the landlord may set any rate (RA 9653 Sec. 4). If the new rate is > PHP 10K, the unit exits rent control. If ≤ PHP 10K, it remains controlled.

### 3.2 Per-Process Bifurcation Rules

| Process | Residential Controlled | Commercial | Design Impact |
|---------|----------------------|------------|---------------|
| **P1 Escalation** | NHSB cap (1-2.3%/year), max once per 12 months, compounding, ROUND_DOWN | Contractual rate (fixed %, stepped, CPI-linked), per contract terms | `Lease.escalation_type` ENUM: `NHSB_CAP`, `FIXED_PERCENT`, `STEPPED`, `CPI_LINKED`, `NONE` |
| **P2 Water** | No sewerage charge | Sewerage 20% of Basic Charge | `WaterCharge.sewerage_charge` = 0 when `unit_type = RESIDENTIAL` |
| **P3 Electric** | Same blended rate formula | Same blended rate formula + sewerage allocation in water context only | No electric-specific bifurcation |
| **P4 Penalties** | Safe harbour: ≤1%/month simple interest, total ≤1 month's rent/year; grace period = 5 days (RA 9653 Sec. 7) | Contractual rate (up to ~3%/month before unconscionability risk); grace period per contract | `Lease.penalty_rate_monthly`, `Lease.grace_period_days`; cap logic in computation engine |
| **P5 Billing** | VAT-exempt if rent ≤ PHP 15K/month; default due day = 5th of month (RA 9653 Sec. 7) | 12% VAT; due day per contract | `Lease.custom_due_day` defaults based on regime |
| **P6 Payment** | Art. 1252-1254 allocation; 3-month arrears = ejectment ground (RA 9653 Sec. 9(b)) | Same allocation rules; no statutory arrears limit for ejectment | `TenantBalance.months_in_arrears`; arrears alert at 3 months for controlled |
| **P7 Deposit** | Max 2 months rent + 1 month advance; bank-hold mandatory; ALL interest returned to lessee; return within 1 month of expiry + turnover | No cap on deposit/advance; bank-hold not mandated; interest per contract; return = reasonable time (~30 days) | `SecurityDeposit.lease_regime` determines rules; `Lease.deposit_months` CHECK ≤ 2 for controlled |
| **P8 Contract** | Must include RA 9653 mandatory clauses (deposit cap, escalation cap, grace period, ejectment grounds); prohibited clauses = void | Freedom of contract (Art. 1305-1306); no mandatory clauses | `LeaseTemplate.applicable_regime` → clause selection |
| **P9 Renewal** | Only RA 9653 Sec. 9 ejectment grounds valid for non-renewal; tacit reconduction continues existing terms; no holdover premium | 15-day notice to prevent reconduction (Art. 1670); commercial holdover penalty (150-200% of last rent) | `LeaseEvent` triggers differ by regime |
| **P10 Status** | Reconduction detection; limited ejectment grounds; no holdover penalty | Standard expiry → reconduction or termination; holdover penalty rates | Alert messages and available actions differ by regime |

### 3.3 Regime Propagation

When a lease is created, `Lease.lease_regime` is set based on `Rentable.unit_type` and the initial rent. This regime propagates to:

1. **Charge creation** — determines VAT rate, penalty caps
2. **Deposit collection** — determines max months, bank-hold requirement
3. **Contract generation** — determines mandatory clauses
4. **Billing generation** — determines due day default, VAT treatment
5. **Payment allocation** — determines arrears alert threshold
6. **Renewal/expiry** — determines available actions and notice requirements

**Regime can change** when:
- Escalation crosses the PHP 10K threshold (`EscalationEvent.threshold_crossed = true`)
- Vacancy decontrol (new tenant, new lease, may re-price)
- These transitions are tracked via `LeaseEvent` with appropriate event types

### 3.4 UI Implications

- Lease creation forms must adapt required fields based on `unit_type` selection
- Penalty configuration must show safe harbour limits for controlled leases
- Deposit entry must enforce max 2+1 rule for controlled leases
- Contract template must include/exclude clauses based on regime
- Dashboard should visually distinguish controlled vs. commercial leases (badge or color)
- Alerts use different language and thresholds per regime

---

## 4. Sequential Numbering (Invoice / Receipt / Credit Memo)

**Affects:** P5, P6, P7, P13
**Legal basis:** NIRC Sec. 237; RR 18-2012; RR 7-2024; RA 11976 (EOPT Act)
**Core principle:** BIR-mandated gapless sequential numbering per document type per establishment, managed through Authority to Print (ATP).

### 4.1 Document Types and Series

Under the EOPT Act (RA 11976) + RR 7-2024, the corporation maintains three independent numbering series:

| Series | Document | Issued When | Trigger Process | Purpose |
|--------|----------|-------------|-----------------|---------|
| **VAT Sales Invoice** | Invoice | At billing (accrual basis) | P5 (billing run) | Primary document; supports tenant's input VAT claim |
| **Official Receipt** | Receipt | At payment | P6 (payment recording) | Supplementary document; acknowledges collection |
| **Credit Memo** | Credit memo | At billing correction | P5 (adjustment) | Cannot void a BIR invoice — must issue credit memo |

### 4.2 Numbering Rules

1. **Gapless:** No gaps in the sequence. If a draft invoice is discarded, the number is still consumed (marked as CANCELLED, not deleted).
2. **Sequential:** Strictly ascending. No out-of-order issuance.
3. **Per-establishment:** Each branch/establishment has its own series (TSVJ likely has one establishment; design for multi-establishment extensibility).
4. **ATP-bounded:** Each series operates within a range assigned by the ATP (e.g., Invoice #0001 – #5000).

### 4.3 ATP (Authority to Print) Management

**Entity: `AuthorityToPrint`**

| Field | Type | Purpose |
|-------|------|---------|
| id | uuid/serial | PK |
| document_type | ENUM(INVOICE, RECEIPT, CREDIT_MEMO) | Which series |
| atp_number | text | BIR-issued ATP number |
| series_start | integer | First number in range (e.g., 0001) |
| series_end | integer | Last number in range (e.g., 5000) |
| current_number | integer | Next number to issue |
| valid_from | date | ATP validity start |
| valid_to | date | ATP validity end (CONFLICTING — see §4.5) |
| printer_name | text | BIR-accredited printer |
| printer_tin | text | |
| utilization_pct | decimal(5,2) | GENERATED: (current_number - series_start) / (series_end - series_start + 1) × 100 |
| is_active | boolean | Only one active ATP per document type |

**Entity: `DocumentSequence`**

| Field | Type | Purpose |
|-------|------|---------|
| id | uuid/serial | PK |
| document_type | ENUM(INVOICE, RECEIPT, CREDIT_MEMO) | Series identifier |
| atp_id | FK → AuthorityToPrint | Current active ATP |
| last_issued_number | integer | Last successfully issued number |
| prefix | text | Optional prefix (e.g., "INV-", "OR-") |

### 4.4 Atomic Number Assignment

**Critical: Number assignment must be atomic to prevent gaps or duplicates under concurrent access.**

```sql
-- PostgreSQL atomic increment pattern
UPDATE document_sequence
SET last_issued_number = last_issued_number + 1
WHERE document_type = $1
RETURNING last_issued_number;
```

In Drizzle ORM / tRPC context:
- Use a database transaction with `SELECT ... FOR UPDATE` on `DocumentSequence`
- Increment `last_issued_number`, check it does not exceed ATP `series_end`
- If it would exceed, fail with an error (ATP exhausted)
- Format the number with zero-padding and optional prefix

### 4.5 ATP Exhaustion Alerts

| Utilization | Alert Level | Action |
|:-----------:|:-----------:|--------|
| 80% | Info | Dashboard notification: "ATP nearing exhaustion" |
| 90% | Warning | Email/in-app alert to admin |
| 100% | Critical | Block document issuance; require new ATP registration |

### 4.6 ATP Validity Period (CONFLICTING)

Three regulatory sources disagree:
- RR 18-2012: 3-year validity
- RR 6-2022 / RMC 123-2022: 5-year validity (or possibly removed entirely)
- RR 7-2024: Silent on validity

**Web app design:** Store `valid_from` and `valid_to` dates on each ATP. Allow admin to set these based on accountant/BIR guidance. Alert when approaching expiry. Do not hard-code a validity period.

### 4.7 Mandatory Invoice Fields (RR 7-2024)

Every VAT Sales Invoice must include these 13+ fields (RR 7-2024 Sec. 6(B)):

1. Registered name of seller (TSVJ)
2. Business name/style (if any)
3. TIN of seller
4. Business address
5. Invoice serial number (from ATP sequence)
6. Date of transaction
7. Registered name of buyer (tenant)
8. TIN of buyer (tenant)
9. Business address of buyer
10. Description of goods/services
11. Quantity (if applicable)
12. Unit price
13. Total sales amount
14. VAT amount (if VATable)
15. Total amount due
16. ATP number

**Web app design:** All 16 fields must be populated on the `IssuedDocument` + `IssuedDocumentLine` entities. Tenant TIN is required for invoice generation — warn if `Tenant.tin` is null.

### 4.8 EIS Compliance (Future)

RR 26-2025 mandates Electronic Invoicing System (EIS) compliance by December 31, 2026. This will require:
- API integration with BIR EIS
- Real-time reporting of issued invoices
- Digital document format

**Web app design:** Design the `IssuedDocument` entity with an `eis_submission_status` field (PENDING, SUBMITTED, ACCEPTED, REJECTED) for future EIS integration. Leave the actual API integration out of MVP but ensure the data model supports it.

---

## 5. Lease Lifecycle Events

**Affects:** P1, P4, P5, P7, P8, P9, P10
**Core principle:** Lease state transitions trigger cascading effects across multiple processes. A centralized `LeaseEvent` audit log captures every transition.

### 5.1 Lease State Machine

```
                ┌──────────────────────────┐
                │                          │
                ▼                          │
    ┌────────┐     ┌────────┐     ┌──────────────┐
    │  DRAFT │────►│ ACTIVE │────►│   EXPIRED    │
    └────────┘     └────────┘     └──────────────┘
                       │               │    │    │
                       │               │    │    │
                       │    ┌──────────┘    │    └──────────┐
                       │    │               │               │
                       │    ▼               ▼               ▼
                       │ ┌──────────────┐ ┌───────────┐ ┌─────────┐
                       │ │MONTH_TO_MONTH│ │ TERMINATED│ │ RENEWED │
                       │ └──────────────┘ └───────────┘ └─────────┘
                       │         │    │
                       │         │    └──────────┐
                       │         ▼               ▼
                       │  ┌───────────┐   ┌─────────┐
                       │  │ TERMINATED│   │ RENEWED │
                       │  └───────────┘   └─────────┘
                       │
                       └──► HOLDOVER (commercial only, unauthorized stay)
                               │
                               ▼
                          TERMINATED
```

**Valid transitions:**

| From | To | Trigger | Auto/Manual |
|------|----|---------|:-----------:|
| DRAFT | ACTIVE | Lease signed + notarized | Manual (P8) |
| ACTIVE | EXPIRED | `date_end` reached, no renewal action | **Auto** (daily job) |
| EXPIRED | MONTH_TO_MONTH | 15 days acquiescence after expiry (Art. 1670) | **Auto** (daily job, 15-day countdown) |
| EXPIRED | TERMINATED | Notice given within 15-day window | Manual (admin action) |
| EXPIRED | RENEWED | New lease executed before or during expiry | Manual (P9) |
| MONTH_TO_MONTH | TERMINATED | Notice given (any time for commercial; RA 9653 grounds for controlled) | Manual |
| MONTH_TO_MONTH | RENEWED | New lease executed | Manual (P9) |
| ACTIVE | HOLDOVER | Term ended + no reconduction (commercial) | Manual or auto |
| HOLDOVER | TERMINATED | Eviction or voluntary exit | Manual |

### 5.2 Event-Triggered Cascades

Each lifecycle event triggers downstream processes:

| Event | LeaseEventType | Cascading Effects |
|-------|---------------|-------------------|
| **Lease created** | `CREATED` | → P8: contract generation queued; → P7: deposit collection required; → P5: first billing scheduled |
| **Lease activated** | `ACTIVATED` | → P5: billing starts from `date_start`; → P10: appears on active portfolio dashboard |
| **Lease anniversary** | `ANNIVERSARY` | → P1: escalation calculation triggered; → P10: anniversary alert |
| **Lease expiring (90 days)** | `NOTICE_SENT` (alert, not actual notice) | → P10: 90/60/30/15-day countdown alerts; → P9: renewal initiation prompt |
| **Lease expired** | `EXPIRED` | → P9: 15-day reconduction countdown starts; → P4: final penalty assessment; → P10: status change |
| **Tacit reconduction** | `RECONDUCTION_STARTED` | → P9: month-to-month transition; → P10: status = MONTH_TO_MONTH; → P1: escalation continues at anniversary; → Art. 1672: guarantor released (if any) |
| **Lease renewed** | `RENEWED` | → P8: new contract; → P1: new escalation params; → P7: deposit top-up calculation; → P12: DST on new term |
| **Lease terminated** | `TERMINATED` | → P7: deposit deduction/refund workflow; → P4: final penalty assessment; → P6: final balance computation; → P5: billing stops |

### 5.3 LeaseEvent Entity

| Field | Type | Purpose |
|-------|------|---------|
| id | uuid/serial | PK |
| lease_id | FK → Lease | |
| event_type | ENUM(CREATED, ACTIVATED, EXPIRED, RENEWED, RECONDUCTION_STARTED, TERMINATED, NOTICE_SENT, ANNIVERSARY) | State transition type |
| event_date | date | When the event occurred |
| triggered_by | text | User ID or "SYSTEM" for auto-transitions |
| metadata | jsonb | Additional context (e.g., notice method, penalty amount) |
| created_at | timestamp | Audit timestamp |

### 5.4 Daily Scheduled Job Logic

A background job (cron or Supabase Edge Function) runs daily to detect and process lifecycle events:

```
FOR EACH lease WHERE status = 'ACTIVE':
    IF date_end < today:
        → INSERT LeaseEvent(EXPIRED)
        → UPDATE lease.status = 'EXPIRED'

FOR EACH lease WHERE status = 'EXPIRED':
    days_since_expiry = today - date_end
    IF days_since_expiry >= 15 AND no_notice_sent:
        → INSERT LeaseEvent(RECONDUCTION_STARTED)
        → UPDATE lease.status = 'MONTH_TO_MONTH'

FOR EACH lease WHERE status = 'ACTIVE':
    days_until_expiry = date_end - today
    IF days_until_expiry IN (90, 60, 30, 15):
        → Create alert (not a LeaseEvent — just a notification)
        → Optionally insert NOTICE_SENT if admin sends actual notice

FOR EACH lease WHERE status IN ('ACTIVE', 'MONTH_TO_MONTH'):
    IF today = lease_anniversary_date:
        → INSERT LeaseEvent(ANNIVERSARY)
        → Trigger P1 escalation check
```

### 5.5 Alert Generation from Lifecycle Events

| Alert Window | Type | Audience | Channel |
|:------------:|------|----------|---------|
| 90 days before expiry | Info | Admin | In-app dashboard |
| 60 days before expiry | Warning | Admin | In-app + optional email |
| 30 days before expiry | Urgent | Admin | In-app + email |
| 15 days before expiry | Critical | Admin | In-app + email (action required: renew or issue notice) |
| At reconduction | Notice | Admin, Accountant | In-app (guarantor released, terms continue) |
| At anniversary | Info | Admin | In-app (escalation due) |

---

## 6. Decimal Handling and Rounding Rules

**Applies to all monetary computations across all processes.**

### 6.1 Storage

- All monetary amounts: `numeric(10,2)` minimum; `numeric(12,2)` for aggregate columns
- Rates: `numeric(4,2)` for percentages (0.12 = 12%), `numeric(5,4)` for precision rates (0.0230 = 2.3%)
- Per-kWh rates: `numeric(8,4)` (4 decimal places)
- PostgreSQL `numeric` (arbitrary precision) — NEVER `float` or `double precision`
- Drizzle ORM maps `numeric` to string. Use `decimal.js` or `big.js` for client-side arithmetic.

### 6.2 Rounding Rules by Context

| Context | Rule | Precision | Source |
|---------|------|:---------:|--------|
| Rent escalation (NHSB) | ROUND_DOWN (truncate) | 2 decimals | P1 (Crispina `math.py` precedent) |
| Water per-tier billing | Standard rounding (HALF_UP) | 2 decimals | P2 |
| Electric blended rate | Standard rounding | 4 decimals (rate), 2 decimals (charge) | P3 |
| VAT computation | Standard rounding | 2 decimals | All |
| EWT computation | Standard rounding | 2 decimals | P6, P14 |
| DST computation | Specific formula, no rounding needed | 2 decimals | P8 |
| Penalty computation | Standard rounding, then cap check | 2 decimals | P4 |

### 6.3 DST Special Formula

```
annual_rent = monthly_rent × 12
dst = 6.00 (on first PHP 2,000) + CEIL((annual_rent × lease_term_years - 2000) / 1000) × 2.00
```

Per NIRC Sec. 194, as amended by RA 10963 (TRAIN Law).

---

## 7. Compliance Deadlines as Cross-Cutting Data

**Affects:** P5, P6, P11, P12, P13, P14 (any process that generates data for tax filings)

### 7.1 Compliance Calendar Summary

The corporation faces **~43 recurring compliance deadlines per year** across:
- **BIR (national tax):** ~30 deadlines (monthly EWT, quarterly VAT/income tax, annual alphalists)
- **SEC (corporate):** 2 deadlines (GIS + AFS)
- **LGU (local):** ~8 per property (business permit, RPT)
- **Other national:** ~3 per property (BFP, DENR, City Health)

### 7.2 Entity: ComplianceObligation

| Field | Type | Purpose |
|-------|------|---------|
| id | uuid/serial | PK |
| name | text | e.g., "VAT Return (2550Q)" |
| form_number | text | e.g., "2550Q" |
| frequency | ENUM(MONTHLY, QUARTERLY, SEMI_ANNUAL, ANNUAL, EVENT_DRIVEN) | |
| deadline_rule | text | e.g., "25th day after quarter-end" |
| source_processes | text[] | Which processes provide the data |
| alert_days_before | integer[] | e.g., [30, 15, 5] — when to alert |

### 7.3 Alert System (Applies to Both Compliance and Lease Events)

| Level | Color | Trigger | |
|-------|:-----:|---------|---|
| Info | Blue | 30 days before deadline | Dashboard widget only |
| Warning | Yellow | 15 days before deadline | In-app notification |
| Urgent | Orange | 5 days before deadline | In-app + email |
| Overdue | Red | Past deadline | Persistent banner + penalty computation hint |

This alert system is shared between compliance deadlines (§7) and lease lifecycle alerts (§5.5). Both feed into the same unified alert/notification system in the web app.

---

## 8. Summary: Cross-Cutting Design Decisions for Wave 2

These are the key design constraints that Wave 2 architecture decisions must respect:

| Concern | Key Design Constraint | Impacts |
|---------|----------------------|---------|
| VAT treatment | Per-charge `vat_rate` frozen at creation; determination logic centralized in shared computation package | database-schema, shared-computations, spec-F0, spec-P5 |
| EWT on rent | `Tenant.is_corporate` flag; payment reconciliation: cash + EWT = invoice total; 2307 tracking workflow | database-schema, api-layer, spec-P6, spec-P12 |
| EWT on suppliers | Rate matrix by payee type × expense category; Form 2307 issuance | shared-computations, spec-P14 |
| Tenant type bifurcation | `Rentable.unit_type` + `Lease.lease_regime` propagated everywhere; forms adapt per regime | ui-framework, api-layer, every spec |
| Sequential numbering | Atomic increment (Postgres `UPDATE ... RETURNING`); ATP exhaustion monitoring; gapless guarantee | database-schema, api-layer, spec-P5, spec-P13 |
| Lease lifecycle | State machine with auto-transitions via daily job; `LeaseEvent` audit log; cascading triggers | database-schema, compliance-alerts, spec-P9, spec-P10 |
| Decimal handling | `numeric` columns only; `decimal.js` on client; context-specific rounding rules | database-schema, shared-computations |
| Compliance alerts | Unified alert system for deadlines + lease events; 4-level severity | compliance-alerts, ui-framework |

---

*Extracted: 2026-03-02 | 5 cross-cutting concerns + decimal handling + compliance calendar | Ready for Wave 2 architecture decisions*
