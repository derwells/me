# Process Dependencies

**Wave:** 3 (Handoff & Integration Analysis)
**Analyzed:** 2026-02-27
**Dependencies:** All Wave 2 process analyses (14 aspects), data-flow-mapping

---

## 1. Overview

This analysis formalizes the dependency relationships between all back-office processes identified in Wave 2. While `data-flow-mapping` traced the pipeline from data entry through filing, this document identifies:

- **Which processes generate data consumed by other processes** (producer→consumer)
- **Shared data model entities** that serve as integration points between processes
- **Execution ordering constraints** for both runtime (monthly close) and build-time (automation implementation)
- **Critical paths** that bottleneck the monthly pipeline
- **Feedback loops** where Process A's output eventually cycles back to influence Process A

---

## 2. Process Registry

All 14 Wave 2 processes, grouped by function:

| ID | Process | Category | Automability |
|----|---------|----------|-------------|
| P1 | Rent Escalation Calculation | Billing | 4/5 |
| P2 | Water Billing | Billing | 4/5 |
| P3 | Electric Billing | Billing | 4/5 |
| P4 | Late Payment Penalties | Billing | 4/5 |
| P5 | Monthly Billing Generation | Billing | 5/5 |
| P6 | Tenant Payment Tracking | Collection | 4/5 |
| P7 | Security Deposit Lifecycle | Collection | 3/5 |
| P8 | Lease Contract Generation | Contracts | 4/5 |
| P9 | Lease Renewal & Extension | Contracts | 4/5 |
| P10 | Lease Status Visibility | Monitoring | 5/5 |
| P11 | Rent Roll Preparation | Handoff | 5/5 |
| P12 | Tax Data Compilation | Handoff | 4/5 |
| P13 | Official Receipt Data | Handoff | 4/5 |
| P14 | Expense Tracking | Handoff | 4/5 |

**Foundation entity (not a process but a prerequisite):**

| ID | Entity | Description |
|----|--------|-------------|
| F0 | Lease & Tenant Master | Lease, Tenant, Property, Room, Rentable records — the base data all processes depend on |

---

## 3. Directed Dependency Graph

Each edge means "the producer must have generated its output before the consumer can complete."

### 3.1 Adjacency List (Producer → Consumer)

```
F0  (Lease & Tenant Master)
├──► P1  (Rent Escalation)
├──► P2  (Water Billing)
├──► P3  (Electric Billing)
├──► P4  (Late Payment Penalties)
├──► P5  (Monthly Billing)
├──► P6  (Tenant Payment Tracking)
├──► P7  (Security Deposit)
├──► P8  (Lease Contract Generation)
├──► P9  (Lease Renewal & Extension)
├──► P10 (Lease Status Visibility)
├──► P11 (Rent Roll)
├──► P13 (Official Receipt Data)
└──► P14 (Expense Tracking)

P1  (Rent Escalation)
└──► P5  (Monthly Billing — current period rent amount)

P2  (Water Billing)
└──► P5  (Monthly Billing — per-tenant water charges)

P3  (Electric Billing)
└──► P5  (Monthly Billing — per-tenant electric charges)

P4  (Late Payment Penalties)
└──► P5  (Monthly Billing — penalty charges to include)

P5  (Monthly Billing)
├──► P6  (Tenant Payment Tracking — charges to allocate against)
├──► P11 (Rent Roll — billed amounts, invoice numbers)
├──► P12 (Tax Data Compilation — output VAT, gross receipts)
└──► P13 (Official Receipt Data — invoice register)

P6  (Tenant Payment Tracking)
├──► P4  (Late Payment Penalties — outstanding balances)
├──► P7  (Security Deposit — outstanding at lease-end for deduction)
├──► P11 (Rent Roll — collections, balances, receipt numbers)
├──► P12 (Tax Data Compilation — SAWT data from 2307 tracking)
└──► P13 (Official Receipt Data — receipt register)

P7  (Security Deposit)
├──► P5  (Monthly Billing — when deposit applied, becomes income → charge event)
├──► P11 (Rent Roll — deposit held column)
└──► P12 (Tax Data Compilation — deposit reclassification events)

P8  (Lease Contract Generation)
├──► F0  (Lease & Tenant Master — creates new lease records)
├──► P12 (Tax Data Compilation — DST on new lease)
└──► P10 (Lease Status Visibility — new active lease)

P9  (Lease Renewal & Extension)
├──► F0  (Lease & Tenant Master — creates successor lease records)
├──► P12 (Tax Data Compilation — DST on renewal/extension)
└──► P10 (Lease Status Visibility — status transition EXPIRED→RENEWED)

P10 (Lease Status Visibility)
├──► P5  (Monthly Billing — which leases are ACTIVE to bill)
├──► P9  (Lease Renewal — expiry alerts trigger renewal workflow)
├──► P11 (Rent Roll — lease status column)
└──► P12 (Tax Data Compilation — AFS PFRS 16 maturity analysis)

P11 (Rent Roll)
├──► P12 (Tax Data Compilation — VATable/exempt split, gross income, 2307 credits)
└──► [LIS Report — semi-annual subset]

P13 (Official Receipt Data)
└──► P11 (Rent Roll — invoice/receipt number columns)

P14 (Expense Tracking)
├──► P12 (Tax Data Compilation — deductions, input VAT, EWT withheld on suppliers)
└──► [AFS — expense schedules, fixed assets]
```

### 3.2 Dependency Matrix

Read as: row **depends on** column (✓ = direct dependency).

|        | F0 | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 | P11 | P12 | P13 | P14 |
|--------|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|-----|-----|
| **P1** | ✓  |    |    |    |    |    |    |    |    |    |     |     |     |     |     |
| **P2** | ✓  |    |    |    |    |    |    |    |    |    |     |     |     |     |     |
| **P3** | ✓  |    |    |    |    |    |    |    |    |    |     |     |     |     |     |
| **P4** | ✓  |    |    |    |    |    | ✓  |    |    |    |     |     |     |     |     |
| **P5** | ✓  | ✓  | ✓  | ✓  | ✓  |    |    | △  |    |    | ✓   |     |     |     |     |
| **P6** | ✓  |    |    |    |    | ✓  |    |    |    |    |     |     |     |     |     |
| **P7** | ✓  |    |    |    |    |    | ✓  |    |    |    |     |     |     |     |     |
| **P8** |    |    |    |    |    |    |    |    |    |    |     |     |     |     |     |
| **P9** | ✓  |    |    |    |    |    |    |    |    |    | ✓   |     |     |     |     |
| **P10**| ✓  |    |    |    |    |    | ✓  |    | ✓  | ✓  |     |     |     |     |     |
| **P11**| ✓  |    |    |    |    | ✓  | ✓  | ✓  |    |    | ✓   |     |     | ✓   |     |
| **P12**|    |    |    |    |    | ✓  | ✓  | ✓  | ✓  | ✓  | ✓   | ✓   |     |     | ✓   |
| **P13**| ✓  |    |    |    |    | ✓  | ✓  |    |    |    |     |     |     |     |     |
| **P14**|    |    |    |    |    |    |    |    |    |    |     |     |     |     |     |

△ = conditional dependency (P7→P5 only when deposit is applied to rent)

---

## 4. Feedback Loops

Three feedback loops exist in the graph. These are **not** circular deadlocks — they operate across time periods.

### 4.1 Payment ↔ Penalty Loop
```
P6 (Payment Tracking) ──[outstanding balances]──► P4 (Late Penalties) ──[penalty charges]──► P5 (Monthly Billing) ──[charges]──► P6
```
**Resolution:** Operates across months. Month N balances → Month N+1 penalties → Month N+1 billing → Month N+1 balances. No intra-month circularity.

### 4.2 Lease Status ↔ Monthly Billing Loop
```
P10 (Lease Status) ──[active leases]──► P5 (Monthly Billing) ──[billing data]──► P11 (Rent Roll) ──[rent roll]──► P12 (Tax Data) ──[PFRS 16]──► P10 (Lease Status projections)
```
**Resolution:** P10's active lease filter runs at billing time; PFRS 16 maturity projections are a separate reporting concern computed at AFS preparation, not at billing time. No runtime circularity.

### 4.3 Lease Creation ↔ Lease Master Loop
```
P8 (Lease Contract Gen) ──[new lease record]──► F0 (Lease Master) ──[lease data]──► P8 (template population)
```
**Resolution:** P8 reads existing master data to populate templates, then writes new records. Sequential within a single lease creation operation.

### 4.4 Deposit ↔ Billing Loop
```
P7 (Security Deposit) ──[deposit applied → income event]──► P5 (Monthly Billing) ──[charges]──► P6 (Payment) ──[balance at lease-end]──► P7
```
**Resolution:** Deposit application is a terminal event (lease ending). It generates a one-time income recognition that flows through billing as a charge event. The return flow (P6→P7) happens only once at lease termination. No recurring circularity.

---

## 5. Topological Sort — Execution Layers

Processes grouped by dependency layer. All processes within a layer can execute in parallel; each layer requires the prior layer to complete.

### 5.1 Monthly Close Execution Order

```
Layer 0: PREREQUISITES (persistent, not per-cycle)
├── F0  Lease & Tenant Master
├── P10 Lease Status Visibility (active lease determination)
└── P14 Expense Tracking (ongoing recording)

Layer 1: DATA COLLECTION + COMPUTATION (parallelizable)
├── P1  Rent Escalation (if anniversary month)
├── P2  Water Billing (from meter readings)
├── P3  Electric Billing (from meter readings)
└── P4  Late Payment Penalties (from prior-month balances via P6)

Layer 2: BILLING (depends on all Layer 1)
└── P5  Monthly Billing Generation

Layer 3: COLLECTION (depends on Layer 2)
├── P6  Tenant Payment Tracking (allocate against Layer 2 charges)
└── P13 Official Receipt Data (receipts issued at payment)

Layer 4: REPORTING (depends on Layers 2-3)
├── P11 Rent Roll Preparation
└── P7  Security Deposit Lifecycle (ongoing; end-of-lease events)

Layer 5: TAX HANDOFF (depends on Layer 4)
└── P12 Tax Data Compilation

EVENT-DRIVEN (not layer-bound):
├── P8  Lease Contract Generation (on new tenant signing)
└── P9  Lease Renewal & Extension (on approaching expiry)
```

### 5.2 Critical Path (Monthly Close)

The longest dependency chain determines the minimum time to close a month:

```
Meter Readings (human)
    → P2/P3 Water+Electric Billing [Layer 1]
        → P5 Monthly Billing [Layer 2]
            → P6 Payment Tracking [Layer 3, spans billing period]
                → P11 Rent Roll [Layer 4]
                    → P12 Tax Data Compilation [Layer 5]
                        → Accountant Handoff
```

**Estimated minimum pipeline latency:** 3-5 business days from meter readings to accountant delivery (per monthly close pipeline in data-flow-mapping).

**Bottleneck:** P6 (Payment Tracking) introduces a calendar dependency — payments trickle in throughout the month. The rent roll can only be finalized when a cutoff date is established for that period's collections.

---

## 6. Shared Data Model Entities

These database tables/entities are **written by one or more processes and read by others**. They are the integration points in the system.

### 6.1 Core Entities (Written Once, Read by Many)

| Entity | Written By | Read By | Key Fields |
|--------|-----------|---------|------------|
| **Tenant** | F0 (master data) | P1-P14 (all) | name, tin, is_corporate, contact |
| **Property / Room / Rentable** | F0 (master data) | P2, P3, P5, P10, P11 | address, unit_number, unit_type, floor_area |
| **Lease** | P8 (new), P9 (renewal) | P1, P4, P5, P6, P7, P10, P11 | tenant_id, rentable_id, date_start, date_end, lease_type, status |
| **NHSBCapRate** | Manual entry (annual) | P1 | year, max_increase_pct |

### 6.2 Transactional Entities (Written Per-Period, Read by Downstream)

| Entity | Written By | Read By | Frequency |
|--------|-----------|---------|-----------|
| **EscalationEvent** | P1 | P5 | Annual per lease |
| **RecurringChargePeriod** | P1, P8 | P5 | At lease creation / escalation |
| **WaterMeterReading** | Human entry | P2 | Monthly |
| **WaterCharge** | P2 | P5 | Monthly per tenant |
| **ElectricMeterReading** | Human entry | P3 | Monthly |
| **ElectricCharge** | P3 | P5 | Monthly per tenant |
| **PenaltyLedger** | P4 | P5 | Monthly per delinquent tenant |
| **Charge** (rent + utility + penalty + other) | P5 | P6, P11, P12, P13 | Monthly per tenant per charge type |
| **Invoice** (VAT Sales Invoice) | P5 | P6, P11, P12, P13 | Monthly per tenant |
| **Payment** | Human entry | P6 | As received |
| **PaymentAllocation** | P6 | P4 (balance), P11, P12 | Per payment |
| **TenantBalance** (materialized) | P6 | P4, P5, P7, P11 | Updated per payment event |
| **Receipt** (Official Receipt) | P6/P13 | P11, P12 | Per payment |
| **SecurityDeposit** | P7 | P5 (at application), P11, P12 | Per lease lifecycle |
| **DSTRecord** | P8, P9 | P12 | Per lease execution |
| **BoardResolution** | P8, P9 | P12 (SEC GIS) | Per authorization |
| **LeaseEvent** | P8, P9, P10 | P9, P10, P11 | Per status transition |
| **NonRenewalNotice** | P9 | P10 | Per lease expiry decision |
| **DisbursementVoucher** | P14 | P12 | Per expense |
| **EWTWithheldRegister** | P14 | P12 | Per supplier payment |
| **InputVATRegister** | P14 | P12 | Per VAT-registered supplier invoice |
| **Form2307Record** | P6 (receipt from tenant) | P11, P12 | Quarterly per corporate tenant |
| **DocumentSequence** | P5 (invoice), P6/P13 (receipt) | P5, P6, P11, P13 | Atomic counter |

### 6.3 Integration Points — Entity Fan-Out

The entities with the highest fan-out (read by the most processes) are the most critical to get right:

| Entity | Fan-Out (# readers) | Implication |
|--------|---------------------|-------------|
| **Lease** | 10 processes | Single most connected entity. Schema must accommodate both controlled and commercial regimes from day 1. |
| **Tenant** | 14 processes (all) | Must include is_corporate, tin, unit_type flags — these propagate to VAT, EWT, penalty, deposit, and reporting logic. |
| **Charge** | 4 processes | Central billing artifact. Must carry VAT treatment, charge_type, invoice reference, and lease linkage. |
| **TenantBalance** | 4 processes | Must be a reliably-updated materialized view, not a computed-on-read aggregate. Stale balances cascade errors to penalties, billing, rent roll. |
| **DocumentSequence** | 4 processes | Atomic, gapless numbering shared across billing and collection. Race conditions here = BIR compliance violations. |

---

## 7. Process-to-Process Data Contracts

For each producer→consumer relationship, this section specifies the exact data exchanged. This serves as the interface contract for automation.

### 7.1 Billing Pipeline Contracts

| Producer | Consumer | Data Contract |
|----------|----------|---------------|
| P1 → P5 | Rent Escalation → Monthly Billing | `{ lease_id, period_start, period_end, base_rent_amount, vat_rate }` — the current-period rent for each lease |
| P2 → P5 | Water Billing → Monthly Billing | `{ tenant_id, billing_period, water_consumption_m3, water_charge_amount, common_area_share, sewerage_charge }` |
| P3 → P5 | Electric Billing → Monthly Billing | `{ tenant_id, billing_period, electric_consumption_kwh, electric_charge_amount, common_area_share, admin_fee }` |
| P4 → P5 | Late Penalties → Monthly Billing | `{ tenant_id, penalty_amount, penalty_type (controlled/commercial), source_charges[], cap_applied }` |
| P10 → P5 | Lease Status → Monthly Billing | `{ lease_id, status (ACTIVE/MONTH_TO_MONTH/HOLDOVER), current_rate, vat_treatment }` — filter for billable leases |

### 7.2 Collection Pipeline Contracts

| Producer | Consumer | Data Contract |
|----------|----------|---------------|
| P5 → P6 | Monthly Billing → Payment Tracking | `{ invoice_id, tenant_id, charges[{ charge_id, amount, vat, charge_type }], total_due, prior_balance }` |
| P6 → P4 | Payment Tracking → Late Penalties | `{ tenant_id, outstanding_balance, oldest_unpaid_charge_date, months_in_arrears }` |
| P6 → P7 | Payment Tracking → Security Deposit | `{ tenant_id, lease_id, balance_at_termination, unpaid_charges[] }` — at lease end only |

### 7.3 Reporting Pipeline Contracts

| Producer | Consumer | Data Contract |
|----------|----------|---------------|
| P5 → P11 | Monthly Billing → Rent Roll | `{ tenant_id, unit, invoice_no, gross_rent, vat_amount, other_charges, total_billed }` |
| P6 → P11 | Payment Tracking → Rent Roll | `{ tenant_id, amount_collected, receipt_no, payment_date, ewt_withheld_2307, running_balance }` |
| P7 → P11 | Security Deposit → Rent Roll | `{ tenant_id, deposit_held, deposit_applied_this_period }` |
| P10 → P11 | Lease Status → Rent Roll | `{ lease_id, status, term_start, term_end, monthly_rate }` |
| P13 → P11 | Official Receipt Data → Rent Roll | `{ invoice_no, receipt_no, document_date }` — cross-reference columns |
| P11 → P12 | Rent Roll → Tax Data | `{ period, total_vatable_sales, total_exempt_sales, total_output_vat, ewt_credits_2307, gross_rental_income }` |
| P14 → P12 | Expense Tracking → Tax Data | `{ period, deductible_expenses_by_category[], input_vat_total, ewt_withheld_on_suppliers_by_atc[] }` |

### 7.4 Event-Driven Contracts

| Producer | Consumer | Trigger | Data Contract |
|----------|----------|---------|---------------|
| P8 → F0 | Lease Contract Gen → Lease Master | New lease signed | `{ lease record with all fields }` |
| P8 → P12 | Lease Contract Gen → Tax Data | New lease executed | `{ lease_id, annual_rent, term_years, dst_amount, execution_date }` |
| P9 → F0 | Lease Renewal → Lease Master | Renewal/extension signed | `{ new lease record, predecessor_lease_id }` |
| P9 → P12 | Lease Renewal → Tax Data | Renewal executed | `{ lease_id, annual_rent, extension_years, dst_amount }` |
| P10 → P9 | Lease Status → Lease Renewal | Expiry approaching | `{ lease_id, expiry_date, days_remaining, alert_level (90/60/30/15) }` |
| P7 → P5 | Security Deposit → Billing | Deposit applied to rent | `{ tenant_id, amount_applied, vat_on_applied, trigger (forfeiture/deduction) }` |

---

## 8. Automation Implementation Order

The dependency graph constrains implementation sequencing. You cannot automate a downstream process until its upstream producers exist. This ordering minimizes the number of manual data bridges needed during incremental deployment.

### 8.1 Implementation Phases

```
Phase 1: FOUNDATION (no process dependencies)
┌─────────────────────────────────────────────────────┐
│ F0: Lease & Tenant Master Data                       │
│  • Tenant (with is_corporate, tin, unit_type)        │
│  • Property / Room / Rentable (with floor_area)      │
│  • Lease (with lease_type, status, escalation_type)  │
│  • NHSBCapRate                                       │
│ VALUE: All 14 processes depend on this.               │
│ RISK: Get the schema wrong and everything downstream │
│        inherits the error.                           │
└─────────────────────────────────────────────────────┘
           │
           ▼
Phase 2: BILLING INPUTS (depends on Phase 1 only; parallelizable)
┌────────────────────┐  ┌────────────────────┐  ┌───────────────────┐
│ P1: Rent Escalation│  │ P2: Water Billing  │  │ P3: Electric      │
│ + P10: Lease Status│  │                    │  │    Billing        │
│                    │  │                    │  │                   │
│ Can deploy together│  │ Standalone with    │  │ Standalone with   │
│ (escalation needs  │  │ meter reading UI   │  │ meter reading UI  │
│ lease status check)│  │                    │  │                   │
└────────┬───────────┘  └────────┬───────────┘  └─────────┬─────────┘
         │                       │                         │
         ▼                       ▼                         ▼
Phase 3: BILLING ENGINE (depends on all Phase 2 outputs)
┌──────────────────────────────────────────────────────┐
│ P5: Monthly Billing Generation                        │
│  + P13: Official Receipt Data (invoice numbering)     │
│  + DocumentSequence (atomic counter)                  │
│                                                       │
│ VALUE: Generates the primary BIR document (invoice).  │
│ Can operate with stub penalty data (P4) initially.    │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
Phase 4: COLLECTION (depends on Phase 3)
┌──────────────────────────────────────────────────────┐
│ P6: Tenant Payment Tracking                           │
│  + PaymentAllocation (Art. 1253 logic)               │
│  + TenantBalance (materialized view)                  │
│  + Form2307Record (2307 receipt tracking)             │
│  + P13: Receipt issuance (receipt numbering)          │
│                                                       │
│ VALUE: Enables running balances, arrears monitoring.  │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
Phase 5: PENALTY + DEPOSIT (depends on Phase 4 for balances)
┌────────────────────────┐  ┌──────────────────────────┐
│ P4: Late Payment       │  │ P7: Security Deposit     │
│     Penalties          │  │     Lifecycle            │
│                        │  │                          │
│ Needs TenantBalance    │  │ Needs balance-at-end     │
│ from Phase 4           │  │ from Phase 4             │
└────────┬───────────────┘  └────────┬─────────────────┘
         │                           │
         ▼                           ▼
Phase 6: CONTRACTS (can run parallel with Phases 3-5)
┌──────────────────────────────────────────────────────┐
│ P8: Lease Contract Generation                         │
│ P9: Lease Renewal & Extension                         │
│                                                       │
│ Event-driven, not part of monthly pipeline.            │
│ Can be implemented independently after Phase 1.       │
│ However, DST records feed P12, so complete before     │
│ Phase 7.                                              │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
Phase 7: REPORTING HUB (depends on Phases 3-6)
┌──────────────────────────────────────────────────────┐
│ P11: Rent Roll Preparation                            │
│                                                       │
│ HIGHEST LEVERAGE. Aggregates ALL upstream processes.   │
│ Cannot be fully automated until Phases 2-6 are live.  │
│ Partial automation possible: generate from whatever   │
│ upstream data exists, with manual fill for gaps.       │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
Phase 8: TAX HANDOFF (depends on Phase 7)
┌──────────────────────────────────────────────────────┐
│ P12: Tax Data Compilation                             │
│ P14: Expense Tracking (can also start at Phase 1)     │
│                                                       │
│ P14 has no upstream process dependency — only needs   │
│ F0 master data. Can be deployed early (Phase 2+).     │
│ However, its output feeds P12, which needs the rent   │
│ roll from Phase 7.                                    │
└──────────────────────────────────────────────────────┘
```

### 8.2 Parallel Tracks

Two implementation tracks can proceed simultaneously after Phase 1:

**Track A: Monthly Pipeline (critical path)**
```
Phase 1 → Phase 2 (P1+P10, P2, P3) → Phase 3 (P5+P13) → Phase 4 (P6) → Phase 5 (P4, P7) → Phase 7 (P11) → Phase 8 (P12)
```

**Track B: Event-Driven Processes**
```
Phase 1 → Phase 6 (P8, P9) → connects to Track A at Phase 7
Phase 1 → P14 (Expense Tracking) → connects to Track A at Phase 8
```

Track B processes have no monthly-cadence dependencies and can be built as standalone features that plug into the main pipeline when Phase 7 is reached.

### 8.3 Minimum Viable Pipeline

The smallest set of processes that delivers meaningful automation (eliminates the #1 pain point — manual rent roll):

```
F0 + P1 + P5 + P6 + P11 = automated rent roll
```

This requires: lease master data, rent escalation, billing, payment tracking, and the rent roll report. Water/electric billing (P2, P3) can be entered as manual charge line items initially, without full meter reading automation.

---

## 9. Cross-Process Invariants

Rules that must hold across multiple processes simultaneously. Violation of any invariant indicates a system bug.

### 9.1 Financial Invariants

| ID | Invariant | Processes Involved | Verification |
|----|-----------|--------------------|--------------|
| INV-1 | **Balance equation**: Prior balance + billed charges − payments received = current balance (per tenant per period) | P5, P6, P11 | Rent roll balance column must equal TenantBalance materialized view |
| INV-2 | **VAT consistency**: A charge's VAT treatment must match the Rentable's unit_type and the Lease's vat_treatment at time of billing | P5, P11, P12 | Sum of VATable + exempt in rent roll = total billed |
| INV-3 | **EWT reconciliation**: 2307 certificates received ≤ EWT expected from corporate tenant billings | P5, P6, P11, P12 | 2307 tracker expected amount = 5% × VAT-exclusive rent billed to corporate tenants |
| INV-4 | **Document sequence gapless**: No gaps in invoice or receipt numbering series | P5, P6, P13 | MAX(sequence) − MIN(sequence) + 1 = COUNT(documents) per series |
| INV-5 | **Utility reconciliation**: Sum of tenant water/electric charges ≤ master meter bill | P2, P3, P5 | Total billed to tenants + common area ≈ utility company bill (tolerance for rounding) |
| INV-6 | **Deposit cap (controlled)**: Security deposit held ≤ 2 months' current rent for RA 9653-covered units | P7, P1 | On escalation event, check deposit adequacy |
| INV-7 | **Penalty cap (controlled)**: Annual penalty charges ≤ 1 month's rent for RA 9653-covered units | P4 | Sum of penalty charges per lease per 12-month period ≤ monthly rent |

### 9.2 Temporal Invariants

| ID | Invariant | Processes Involved |
|----|-----------|--------------------|
| INV-8 | **Accrual before collection**: Invoice date ≤ receipt date for the same charge | P5, P6, P13 |
| INV-9 | **Escalation frequency**: At most one rent increase per 12-month lease cycle for controlled units | P1 |
| INV-10 | **Reconduction timing**: Lease status cannot transition to MONTH_TO_MONTH until 15 days after date_end with no NonRenewalNotice | P10 |
| INV-11 | **DST filing window**: DST record filing_date ≤ 5 days after close of month of lease execution_date | P8, P9, P12 |

---

## 10. Summary

### Key Findings

1. **The dependency graph is a DAG within any single month** — no intra-month circular dependencies. All feedback loops operate across time periods (Month N balances → Month N+1 penalties).

2. **The Rent Roll (P11) is the highest fan-in node** — it reads from 6 upstream processes (P5, P6, P7, P10, P13, plus F0). This confirms data-flow-mapping's conclusion that the rent roll is the central hub and highest-leverage automation target — but also the hardest to fully automate because it requires all upstream processes to be feeding data.

3. **The critical path for monthly close runs 5 layers deep**: meter readings → utility billing → monthly billing → payment tracking → rent roll → tax data. The calendar bottleneck is payment tracking (P6), which must wait for the billing period's payments to come in.

4. **Phase 1 (Lease & Tenant Master) is the single blocking prerequisite** for all 14 processes. Getting the schema right — particularly `is_corporate`, `unit_type`, `lease_type`, `status`, and `floor_area` — is the highest-risk decision in the entire project.

5. **Five shared entities require special care**: Lease (10 readers), Tenant (14 readers), Charge (4 readers), TenantBalance (4 readers), DocumentSequence (4 readers). These are the integration contracts — changes to their schema ripple through the entire system.

6. **Expense Tracking (P14) is the most independent process** — it depends only on F0 (master data) and feeds only P12 (tax compilation). It can be built and deployed at any time after Phase 1, making it a good candidate for parallel implementation.

7. **Seven cross-process invariants** must be enforced at the system level, not within individual processes. The balance equation (INV-1) and document sequence gapless rule (INV-4) are the most critical for BIR compliance.
