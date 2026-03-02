# UI Requirements Extract — TSVJ Backoffice Web App

*Extracted from: `input/process-catalog.md` (14 processes + foundation)*
*Purpose: Every view, form, dashboard, table, export, and report the web app needs, grouped by role*

---

## Role Definitions

| Role | Access Level | Primary Use Cases |
|------|-------------|-------------------|
| **Admin** (Property Manager) | Full CRUD, all processes | Data entry, billing runs, payment recording, lease management, report generation |
| **Accountant** | Read-only views, exports, downloads | Monthly rent roll review, tax data compilation review, expense register, document download |

**Shared:** Both roles see the same dashboard (different scopes), both can export/download reports.

---

## 1. Global Shell & Navigation

### 1.1 App Layout

```
┌─────────────────────────────────────────────────────┐
│  TSVJ Backoffice          [🔔 Alerts (3)]  [User ▾] │
├──────────┬──────────────────────────────────────────┤
│          │                                          │
│ SIDEBAR  │              MAIN CONTENT                │
│          │                                          │
│ Dashboard│  ┌─────────────────────────────────┐     │
│ Tenants  │  │  Page Header + Breadcrumbs      │     │
│ Leases   │  ├─────────────────────────────────┤     │
│ Properties│ │                                 │     │
│ Billing  │  │  Content Area                   │     │
│  ├ Rent  │  │  (tables, forms, dashboards)    │     │
│  ├ Water │  │                                 │     │
│  ├ Electric│ │                                │     │
│  ├ Penalties││                                │     │
│  └ Runs  │  │                                 │     │
│ Payments │  │                                 │     │
│ Deposits │  │                                 │     │
│ Contracts│  └─────────────────────────────────┘     │
│ Reports  │                                          │
│  ├ Rent Roll│                                       │
│  ├ Tax Data │                                       │
│  └ Expenses │                                       │
│ Documents│                                          │
│ Settings │                                          │
│          │                                          │
└──────────┴──────────────────────────────────────────┘
```

### 1.2 Sidebar Navigation Structure

| Section | Sub-items | Admin | Accountant |
|---------|-----------|:-----:|:----------:|
| Dashboard | — | ✅ | ✅ (read-only) |
| Tenants | List, Create, Detail | ✅ | ✅ (read-only) |
| Leases | List, Create, Detail, Status Board | ✅ | ✅ (read-only) |
| Properties | List, Create, Rooms/Rentables | ✅ | ✅ (read-only) |
| Billing | Rent Escalation, Water, Electric, Penalties, Billing Runs | ✅ | ❌ |
| Payments | Payment List, Record Payment | ✅ | ✅ (read-only list) |
| Deposits | Deposit List, Detail/Lifecycle | ✅ | ✅ (read-only) |
| Contracts | Templates, Generate, Milestones | ✅ | ❌ |
| Reports | Rent Roll, Tax Data, Expenses | ✅ | ✅ (read + export) |
| Documents | Invoice Register, Receipt Register, ATP Management | ✅ | ✅ (read + download) |
| Settings | Users, Company Info, Charge Types, Rate Tables | ✅ | ❌ |

### 1.3 Alert Bell / Notification Center

Persistent top-right bell icon. Clicking opens dropdown with categorized alerts:

```
┌──────────────────────────────────────┐
│ Notifications                   [All]│
├──────────────────────────────────────┤
│ 🔴 OVERDUE                          │
│   RPT payment — Las Piñas (2 days)  │
│                                      │
│ 🟠 URGENT (5 days)                  │
│   0619-E filing deadline Mar 10      │
│   ATP INV-2024 nearing exhaustion    │
│                                      │
│ 🟡 WARNING (15 days)                │
│   Lease #42 expiring Apr 15          │
│   2307 missing: TenantCorp Q1        │
│                                      │
│ 🔵 INFO                             │
│   NHSB anniversary: Unit 3B (May 1) │
│   Quarterly VAT return due Apr 25   │
├──────────────────────────────────────┤
│              View All →              │
└──────────────────────────────────────┘
```

**Alert levels** (from process catalog Sec. 9):
- 🔵 Info: 30 days before deadline
- 🟡 Warning: 15 days before deadline
- 🟠 Urgent: 5 days before deadline
- 🔴 Overdue: Past deadline (with penalty computation)

**Sources:** Compliance calendar (P12), lease expiry (P10), ATP exhaustion (P13), 2307 tracking (P6/P12), NHSB anniversaries (P1)

---

## 2. Dashboard (Both Roles)

### 2.1 Admin Dashboard

```
┌─────────────────────────────────────────────────────────┐
│  Dashboard                                    Mar 2026  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────────┐  │
│  │ Active  │ │ Expiring│ │ Month-to│ │   Vacant     │  │
│  │ Leases  │ │ (90 day)│ │ -Month  │ │   Units      │  │
│  │   47    │ │    3    │ │    5    │ │     8        │  │
│  └─────────┘ └─────────┘ └─────────┘ └──────────────┘  │
│                                                         │
│  ┌──────────────────────┐ ┌──────────────────────────┐  │
│  │ Revenue This Month   │ │  Collection Rate          │  │
│  │ Total Billed: ₱245K  │ │  Feb 2026: 87%           │  │
│  │ Collected:    ₱213K  │ │  ████████░░  87%          │  │
│  │ Outstanding:  ₱ 32K  │ │  Prior month: 91%         │  │
│  └──────────────────────┘ └──────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Upcoming Deadlines (next 30 days)                │   │
│  │ Mar 5  — Accountant handoff package              │   │
│  │ Mar 10 — 0619-E filing (EWT remittance)          │   │
│  │ Mar 15 — Lease #42 expiry (Tenant: Santos)       │   │
│  │ Mar 25 — 2550Q + SLSP (Q1 VAT return)           │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Arrears Alerts                                   │   │
│  │ 🔴 Tenant Cruz — 3 months overdue (ejectment)   │   │
│  │ 🟡 Tenant Reyes — 2 months overdue              │   │
│  │ 🟡 Tenant Lim Corp — ₱15K balance, 45 days      │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Monthly Close Progress                           │   │
│  │ ☑ Meter readings entered                         │   │
│  │ ☑ Water billing run complete                     │   │
│  │ ☑ Electric billing run complete                  │   │
│  │ ☐ Penalty assessment                             │   │
│  │ ☐ Monthly billing generation                     │   │
│  │ ☐ Payment reconciliation                         │   │
│  │ ☐ Rent roll export                               │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Widgets:**
1. **KPI Cards** — Active leases, expiring (90-day), month-to-month, vacant units
2. **Revenue Summary** — Total billed, collected, outstanding for current/prior month
3. **Collection Rate** — % collected, bar chart, trend vs prior month
4. **Upcoming Deadlines** — Next 30 days from compliance calendar (P12, Sec. 9)
5. **Arrears Alerts** — Tenants approaching/exceeding 3-month threshold (P4/P6)
6. **Monthly Close Checklist** — Execution order progress (Sec. 8.3)

### 2.2 Accountant Dashboard

Same layout but:
- No "Monthly Close Progress" (accountant doesn't manage the close)
- Adds "Pending Handoff Items" widget (what the admin needs to deliver)
- Adds "Missing 2307 Certificates" widget
- Revenue summary is read-only
- All action buttons hidden

---

## 3. Foundation Views (F0)

### 3.1 Tenant List

```
┌──────────────────────────────────────────────────────────┐
│  Tenants                              [+ New Tenant]     │
├──────────────────────────────────────────────────────────┤
│ Search: [________________]  Filter: [All ▾] [Active ▾]   │
├──────────────────────────────────────────────────────────┤
│ Name          │ TIN        │ Type      │ Units │ Balance │
│───────────────│────────────│───────────│───────│─────────│
│ Juan Cruz     │ 123-456-78 │ Individual│  1    │ ₱15,200 │
│ Santos Corp   │ 987-654-32 │ Corporate │  3    │ ₱ 0     │
│ Maria Reyes   │ —          │ Individual│  1    │ ₱ 8,400 │
│ LimTech Inc.  │ 456-789-01 │ Corporate │  2    │ ₱32,100 │
│ ...           │            │           │       │         │
├──────────────────────────────────────────────────────────┤
│ Showing 1-20 of 47               [< 1 2 3 >]            │
└──────────────────────────────────────────────────────────┘
```

**Columns:** Name, TIN, Type (Individual/Corporate), VAT Registered, Units (count), Current Balance
**Filters:** Type (All/Individual/Corporate), Status (Active/Inactive), Balance (Has Balance/Zero/Credit)
**Actions (Admin):** Create, Edit, View Detail
**Actions (Accountant):** View Detail only

### 3.2 Tenant Create/Edit Form (Admin only)

```
┌──────────────────────────────────────────────────┐
│  New Tenant                                      │
├──────────────────────────────────────────────────┤
│                                                  │
│  Name*:         [________________________]       │
│  TIN:           [___-___-___-___]                │
│  Type*:         (●) Individual  (○) Corporate    │
│  VAT Registered: [ ] Yes                         │
│                                                  │
│  ── Contact ──                                   │
│  Email:         [________________________]       │
│  Phone:         [________________________]       │
│  Address:       [________________________]       │
│                 [________________________]       │
│                                                  │
│  ── Corporate Only ──  (shown if Type=Corporate) │
│  Authorized Rep:  [________________________]     │
│  SEC Reg No:      [________________________]     │
│                                                  │
│            [Cancel]  [Save Tenant]               │
└──────────────────────────────────────────────────┘
```

**Validation:**
- Name: required, min 2 chars
- TIN: format validation (###-###-###-### or ###-###-###), unique per tenant
- Type: required
- If corporate: TIN required (EWT applies), authorized rep recommended

### 3.3 Tenant Detail View

Tabbed layout showing tenant master data + related information:

```
┌──────────────────────────────────────────────────────────┐
│  ← Tenants / Juan Cruz                    [Edit] [...]   │
├──────────────────────────────────────────────────────────┤
│  [Overview] [Leases] [Billing] [Payments] [Documents]    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ── Overview Tab ──                                      │
│  Name: Juan Cruz                                         │
│  TIN: 123-456-789                                        │
│  Type: Individual │ VAT Registered: No                   │
│  Contact: juan@email.com │ +63-917-XXX-XXXX              │
│                                                          │
│  ┌── Active Leases ──────────────────────────────┐       │
│  │ Unit 3B │ Residential │ Active │ ₱8,500/mo    │       │
│  │ Start: Jan 2024 │ End: Dec 2025               │       │
│  └───────────────────────────────────────────────┘       │
│                                                          │
│  ┌── Balance Summary ────────────────────────────┐       │
│  │ Total Billed: ₱102,000  │ Total Paid: ₱86,800│       │
│  │ Outstanding:  ₱ 15,200  │ Days Overdue: 45    │       │
│  │ Months in Arrears: 2    │ Status: ⚠️ Warning  │       │
│  └───────────────────────────────────────────────┘       │
│                                                          │
│  ┌── Deposit ────────────────────────────────────┐       │
│  │ Amount: ₱17,000 │ Status: Held                │       │
│  │ Bank: BDO SA #1234 │ Interest: ₱423           │       │
│  └───────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────┘
```

**Tabs:**
- **Overview:** Master data, active leases summary, balance summary, deposit status
- **Leases:** All leases (current + historical) with status, term, rate
- **Billing:** Charge history table (date, type, amount, VAT, invoice#, status)
- **Payments:** Payment history (date, amount, method, OR#, allocation)
- **Documents:** Invoices, receipts, contracts, 2307s linked to this tenant

### 3.4 Property List & Detail

```
┌──────────────────────────────────────────────────────────┐
│  Properties                          [+ New Property]    │
├──────────────────────────────────────────────────────────┤
│ Property Name   │ Address           │ Units │ Occupancy  │
│─────────────────│───────────────────│───────│────────────│
│ TSVJ Building A │ 123 Real St, LP   │  30   │ 87% (26)   │
│ TSVJ Building B │ 125 Real St, LP   │  20   │ 90% (18)   │
│ ...             │                   │       │            │
└──────────────────────────────────────────────────────────┘
```

**Property Detail** shows:
- Property info (name, address, RPT reference)
- Room list with floor/area breakdown
- Rentable units within each room (unit_type, floor_area_sqm, current lease status)
- Meter assignments (water meters, electric meters per rentable)
- Occupancy summary

### 3.5 Property Create/Edit Form (Admin only)

Fields: Name, Address, City, RPT TDP Number, Notes

### 3.6 Room / Rentable Management (Admin only)

Nested within Property Detail:
- Add Room: floor, label, total_area_sqm
- Add Rentable within Room: unit_label, unit_type (RESIDENTIAL/COMMERCIAL), floor_area_sqm, is_rent_controlled (derived from unit_type + lease regime)
- Assign meters to rentable: water meter ID, electric meter ID

### 3.7 Lease List

```
┌──────────────────────────────────────────────────────────────┐
│  Leases                                   [+ New Lease]      │
├──────────────────────────────────────────────────────────────┤
│ Filter: [All Statuses ▾]  [All Properties ▾]  [Search____]  │
├──────────────────────────────────────────────────────────────┤
│ Tenant       │ Unit(s)    │ Status      │ Term          │Rate│
│──────────────│────────────│─────────────│───────────────│────│
│ Juan Cruz    │ 3B         │ 🟢 Active   │ Jan24-Dec25   │8.5K│
│ Santos Corp  │ G1,G2,G3   │ 🟡 Expiring │ Mar24-Mar26   │45K │
│ Maria Reyes  │ 2A         │ 🔵 M-to-M   │ (since Aug25) │7.2K│
│ Kim Lee      │ 5C         │ 🔴 Holdover │ Exp Dec25     │12K │
│ ...          │            │             │               │    │
├──────────────────────────────────────────────────────────────┤
│ Active: 35  Expiring: 3  M-to-M: 5  Holdover: 2  Vacant: 8 │
└──────────────────────────────────────────────────────────────┘
```

**Status badges:**
- 🟢 ACTIVE — current term
- 🟡 EXPIRING — within 90 days of end date
- 🔵 MONTH_TO_MONTH — tacit reconduction
- 🔴 HOLDOVER — expired, no reconduction, no renewal
- ⚫ TERMINATED — ended
- 🟣 DRAFT — not yet activated
- 🔄 RENEWED — linked to successor lease

### 3.8 Lease Create/Edit Form (Admin only)

```
┌──────────────────────────────────────────────────────────────┐
│  New Lease                                                   │
├──────────────────────────────────────────────────────────────┤
│  Tenant*:        [Select tenant... ▾]                        │
│  Rentable(s)*:   [Select units... ▾] (multi-select)          │
│  Lease Regime*:  (●) Controlled Residential                  │
│                  (○) Commercial                              │
│                  (○) Non-Controlled Residential              │
│                                                              │
│  ── Term ──                                                  │
│  Start Date*:    [____-__-__]                                │
│  End Date*:      [____-__-__]                                │
│  Custom Due Day: [5] (default: 5 for controlled, per contract│
│                       for commercial)                        │
│                                                              │
│  ── Rent ──                                                  │
│  Monthly Rate*:  [₱__________]                               │
│  VAT Treatment:  Auto-determined by unit type + rate         │
│    Display: "VAT-exempt (residential ≤ ₱15K)"               │
│             or "12% VAT applicable"                          │
│                                                              │
│  ── Escalation ──                                            │
│  Type*:          [NHSB Cap ▾]                                │
│    Options: NHSB Cap / Fixed % / Stepped / CPI-Linked / None│
│  Params:         (depends on type)                           │
│    NHSB Cap: (no params — uses published rate)               │
│    Fixed %:  Rate: [___]%                                    │
│    Stepped:  Year 1: [___]%, Year 2: [___]%, ...             │
│    CPI:      Base month: [____-__], Spread: [___]%           │
│                                                              │
│  ── Penalty ──                                               │
│  Penalty Rate:   [1]% / month                                │
│  Grace Period:   [5] days                                    │
│                                                              │
│  ── Deposit ──                                               │
│  Security Deposit: [₱__________]                             │
│  Advance Rent:     [₱__________]                             │
│                                                              │
│            [Cancel]  [Save as Draft]  [Activate Lease]       │
└──────────────────────────────────────────────────────────────┘
```

**Validation:**
- Tenant + Rentable: required
- Lease regime: required, auto-suggested based on unit_type
- Dates: start < end, term ≥ 1 month
- Rate: required, positive decimal
- Escalation type: required for leases > 1 year
- Deposit: if controlled residential, validate ≤ 2 months' rent
- Advance: if controlled residential, validate ≤ 1 month's rent

### 3.9 Lease Detail View

Tabbed: Overview, Escalation History, Charges, Payments, Deposit, Events, Contract

---

## 4. Billing Views

### 4.1 Rent Escalation (P1) — Admin Only

#### Escalation Dashboard

```
┌──────────────────────────────────────────────────────────┐
│  Rent Escalation                                         │
├──────────────────────────────────────────────────────────┤
│  ┌── Upcoming Anniversaries (next 90 days) ──────────┐   │
│  │ Lease    │ Tenant    │ Anniversary │ Type     │ Est │  │
│  │──────────│───────────│─────────────│──────────│─────│  │
│  │ #12      │ Cruz      │ Apr 1       │ NHSB Cap │+1%  │  │
│  │ #24      │ Santos    │ Apr 15      │ Fixed 5% │+5%  │  │
│  │ #31      │ Park      │ May 1       │ Stepped  │+7%  │  │
│  │          │           │             │      [Apply All] │  │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌── NHSB Rate Table ────────────────────────────────┐   │
│  │ Year │ Cap Rate │ Resolution    │ Entered   │ By   │  │
│  │──────│──────────│───────────────│───────────│──────│  │
│  │ 2026 │ 1.0%     │ NHSB 2024-01 │ Jan 2026  │ Admin│  │
│  │ 2025 │ 2.3%     │ NHSB 2024-01 │ Jan 2025  │ Admin│  │
│  │                              [+ Add Rate]         │   │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌── Escalation History ─────────────────────────────┐   │
│  │ Date     │ Lease │ Old Rate │ New Rate │ Type     │   │
│  │──────────│───────│──────────│──────────│──────────│   │
│  │ Jan 2026 │ #12   │ ₱8,415  │ ₱8,500   │ NHSB 1% │   │
│  │ Jan 2026 │ #24   │ ₱42,857 │ ₱45,000  │ Fixed 5% │  │
│  └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

**Sections:**
1. Upcoming anniversaries (next 90 days) — shows leases due for escalation, estimated new rate
2. NHSB rate table — manual entry of annual cap rates (Admin action: add new year's rate)
3. Escalation history — audit log of all applied escalations

**Actions:**
- Apply escalation (per lease or batch "Apply All")
- Add NHSB rate
- View escalation detail (shows computation breakdown)

#### Apply Escalation Modal (Admin)

```
┌─────────────────────────────────────────────┐
│  Apply Rent Escalation                      │
├─────────────────────────────────────────────┤
│  Lease: #12 — Juan Cruz (Unit 3B)          │
│  Anniversary Date: April 1, 2026           │
│  Escalation Type: NHSB Cap                 │
│                                             │
│  Current Rent:     ₱ 8,415.00              │
│  NHSB Rate (2026): 1.0%                    │
│  Increase:         ₱    84.15              │
│  Rounded (DOWN):   ₱    84.00              │
│  New Rent:         ₱ 8,499.00              │
│                                             │
│  Threshold Check:  ₱8,499 < ₱10,000       │
│  Status: Still under rent control           │
│                                             │
│  Effective From: [2026-04-01]              │
│                                             │
│       [Cancel]  [Confirm Escalation]        │
└─────────────────────────────────────────────┘
```

### 4.2 Water Billing (P2) — Admin Only

#### Meter Reading Entry

```
┌──────────────────────────────────────────────────────────┐
│  Water Billing — Meter Readings          Period: Mar 2026│
├──────────────────────────────────────────────────────────┤
│  Maynilad Master Bill                                    │
│  Bill Date: [____-__-__]  Total Amount: [₱__________]    │
│  Total Cu.M.: [______]    Bill Period: [____] to [____]  │
│  [Upload Bill Image]                                     │
├──────────────────────────────────────────────────────────┤
│  Sub-Meter Readings                                      │
│  Meter  │ Tenant(s)    │ Previous │ Current │ Cu.M.│ Stat│
│─────────│──────────────│──────────│─────────│──────│─────│
│  W-01   │ Cruz (3B)    │ 1,234    │ [_____] │ auto │ OK  │
│  W-02   │ Santos (G1)  │ 5,678    │ [_____] │ auto │ OK  │
│  W-03   │ Santos/Reyes │ 2,345    │ [_____] │ auto │ ⚠️  │
│  ...    │ (shared)     │          │         │      │     │
│  CR-1   │ Common Area  │ 890      │ [_____] │ auto │ —   │
│  CR-2   │ Common Area  │ 456      │ [_____] │ auto │ —   │
├──────────────────────────────────────────────────────────┤
│  Reconciliation: Total sub-meters [____] vs Master [____]│
│  Difference: [____] cu.m. (unaccounted)                  │
│                                                          │
│           [Save Readings]  [Run Water Billing]           │
└──────────────────────────────────────────────────────────┘
```

**Features:**
- Maynilad bill data entry (top section)
- Per-meter reading entry with auto-computed consumption (current - previous)
- Shared meter indicator (⚠️ for co-tenancy situations)
- Reconciliation check: sum of sub-meters vs. master meter
- Anomaly flags: negative readings, >200% increase from prior month

#### Water Billing Run Result

After running billing, shows per-tenant charge breakdown:

```
┌──────────────────────────────────────────────────────────┐
│  Water Billing Run — Mar 2026               Status: Draft│
├──────────────────────────────────────────────────────────┤
│ Tenant  │ Cu.M.│ Basic  │ Env.  │ Sewer.│ FCDA │ Total  │
│─────────│──────│────────│───────│───────│──────│────────│
│ Cruz    │  12  │ ₱156.00│₱39.00 │   —   │₱2.40 │₱197.40│
│ Santos  │  45  │ ₱892.00│₱223.00│₱178.40│₱9.00 │₱1,302 │
│ (shared)│      │        │       │       │      │        │
│─────────│──────│────────│───────│───────│──────│────────│
│ Common  │  89  │        │       │       │      │₱1,245 │
│  → alloc│      │ by floor area: Cruz ₱124, Santos ₱498..│
│─────────│──────│────────│───────│───────│──────│────────│
│ TOTAL   │ 234  │        │       │       │      │₱8,456 │
│ Master  │ 240  │        │       │       │      │₱8,900 │
│ Diff    │   6  │        │       │       │      │  ₱444 │
├──────────────────────────────────────────────────────────┤
│ ✅ Total billed (₱8,456) ≤ Maynilad master (₱8,900)     │
│                                                          │
│        [Edit Readings]  [Finalize Billing Run]           │
└──────────────────────────────────────────────────────────┘
```

**Key features:**
- Per-tier breakdown per tenant (expandable row)
- Common area allocation display (by floor area)
- Reconciliation: total billed ≤ master bill (compliance check)
- Draft → Finalize workflow (no changes after finalization)

### 4.3 Electric Billing (P3) — Admin Only

Similar to water but simpler (blended rate, not per-tier):

#### Meter Reading Entry

Same structure as water. Fields: MeralcoBill (total amount, total kWh, component breakdown), per-meter readings.

#### Electric Billing Run Result

```
┌──────────────────────────────────────────────────────────┐
│  Electric Billing Run — Mar 2026            Status: Draft│
├──────────────────────────────────────────────────────────┤
│  Blended Rate: ₱12.45/kWh (₱124,500 / 10,000 kWh)      │
│  Admin Fee: ₱1.00/kWh (per contract)                    │
├──────────────────────────────────────────────────────────┤
│ Tenant  │ kWh  │ Electric │Admin Fee│ VAT*  │ Total     │
│─────────│──────│──────────│─────────│───────│───────────│
│ Cruz    │  150 │ ₱1,867.50│ ₱150.00│   TBD │ ₱2,017.50│
│ Santos  │  800 │ ₱9,960.00│ ₱800.00│   TBD │₱10,760.00│
│ ...     │      │          │         │       │           │
│─────────│──────│──────────│─────────│───────│───────────│
│ Common  │1,200 │          │         │       │ ₱14,940   │
│  → alloc│      │ by floor area                          │
├──────────────────────────────────────────────────────────┤
│ * VAT treatment: CONFLICTING — flagged for accountant    │
│                                                          │
│        [Edit Readings]  [Finalize Billing Run]           │
└──────────────────────────────────────────────────────────┘
```

### 4.4 Late Payment Penalties (P4) — Admin Only

#### Penalty Assessment View

```
┌──────────────────────────────────────────────────────────┐
│  Late Payment Penalties — Assessment for Mar 2026        │
├──────────────────────────────────────────────────────────┤
│ Tenant    │Regime  │Overdue│ Base   │Rate │Raw Pen│ Cap  │
│───────────│────────│───────│────────│─────│───────│──────│
│ Cruz      │Control │₱15.2K│₱15,200 │1%/mo│₱152   │₱8.5K │
│ Kim Corp  │Commerc │₱32.1K│₱32,100 │3%/mo│₱963   │ None │
│ Reyes     │Control │₱ 8.4K│₱ 8,400 │1%/mo│₱ 84   │₱7.2K │
├──────────────────────────────────────────────────────────┤
│ ⚠️ Cruz: 2 months arrears (ejectment at 3 per RA 9653)  │
│ ℹ️ Kim Corp: No demand letter on file — legal interest   │
│   only (6% p.a.) until demand issued                     │
│                                                          │
│    [Preview Penalties]  [Apply Selected]  [Apply All]    │
└──────────────────────────────────────────────────────────┘
```

**Features:**
- Auto-computed penalties per overdue tenant
- Cap enforcement for controlled residential (1%/month, max 1 month's rent/year)
- Demand requirement flag: if no DemandRecord exists, only legal interest applies
- Arrears counter with ejectment warning (3 months)

### 4.5 Monthly Billing Run (P5) — Admin Only

#### Billing Run Wizard

Step-by-step process:

```
Step 1: Select Period
┌──────────────────────────────────────────┐
│  Billing Period: March 2026              │
│  Billing Date:   [2026-03-01]            │
│  Due Date:       [2026-03-05] (default)  │
│                                          │
│  Scope: (●) All active leases           │
│         (○) Selected tenants             │
│                                          │
│               [Next →]                   │
└──────────────────────────────────────────┘

Step 2: Review Charges
┌──────────────────────────────────────────────────────────┐
│  Billing Preview — March 2026                            │
├──────────────────────────────────────────────────────────┤
│ Tenant    │ Rent   │ Water│ Elec │ Penalty│ Other│ Total │
│───────────│────────│──────│──────│────────│──────│───────│
│ Cruz      │₱8,500  │₱197  │₱2,018│ ₱152   │  —   │₱10,867│
│ Santos    │₱45,000 │₱1,302│₱10.8K│  —     │  —   │₱57,102│
│ ...       │        │      │      │        │      │       │
│───────────│────────│──────│──────│────────│──────│───────│
│ TOTAL     │₱187.5K │₱8.5K│₱42K  │₱1,199  │  —   │₱239.2K│
├──────────────────────────────────────────────────────────┤
│ VAT Summary: Exempt: ₱68K  │  VATable: ₱171.2K          │
│ Output VAT: ₱20.5K                                      │
│                                                          │
│ ⚠️ 3 tenants have no water reading — exclude from util   │
│ ⚠️ Electric VAT treatment: using "no VAT" (confirm w/    │
│    accountant)                                           │
│                                                          │
│      [← Back]  [Generate Invoices]                       │
└──────────────────────────────────────────────────────────┘

Step 3: Confirmation
┌──────────────────────────────────────────┐
│  ✅ Billing Run Complete                  │
│                                          │
│  Invoices generated: 47                  │
│  Invoice range: INV-2026-0341 to 0387    │
│  Total billed: ₱239,200                  │
│  Output VAT accrued: ₱20,544             │
│                                          │
│  [View Invoice List]  [Download All PDF] │
└──────────────────────────────────────────┘
```

### 4.6 Maynilad / Meralco Rate Tables (Settings, Admin Only)

```
┌──────────────────────────────────────────────────────────┐
│  Maynilad Rate Schedule                  [+ New Schedule]│
├──────────────────────────────────────────────────────────┤
│ Effective   │ Tier 1     │ Tier 2     │ Tier 3     │FCDA│
│ Date        │ 0-10 cu.m. │ 11-20      │ 21-30      │    │
│─────────────│────────────│────────────│────────────│────│
│ 2026-01-01  │ ₱8.56      │ ₱16.12     │ ₱24.89     │0.3%│
│ 2025-10-01  │ ₱8.32      │ ₱15.87     │ ₱24.15     │0.2%│
│ ...         │            │            │            │    │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Payment Views (P6)

### 5.1 Payment List

```
┌──────────────────────────────────────────────────────────┐
│  Payments                             [+ Record Payment] │
├──────────────────────────────────────────────────────────┤
│ Filter: [All ▾]  Date: [From____] [To____]  [Search___]  │
├──────────────────────────────────────────────────────────┤
│ Date    │ Tenant    │ Amount   │ Method│ OR#     │ Alloc │
│─────────│───────────│──────────│───────│─────────│───────│
│ Mar 3   │ Santos    │ ₱57,102  │ Check │ OR-0234 │  Full │
│ Mar 3   │ Cruz      │ ₱ 5,000  │ Cash  │ OR-0235 │Partial│
│ Mar 2   │ LimTech   │ ₱32,100  │ Txfer │ OR-0233 │  Full │
│ ...     │           │          │       │         │       │
├──────────────────────────────────────────────────────────┤
│ Total collected (Mar): ₱94,202                           │
└──────────────────────────────────────────────────────────┘
```

**Columns:** Date, Tenant, Amount, Method (Cash/Check/Transfer/Online), OR Number, Allocation Status (Full/Partial/Unallocated)
**Filters:** Date range, tenant, method, allocation status

### 5.2 Record Payment Form (Admin only)

```
┌──────────────────────────────────────────────────────────┐
│  Record Payment                                          │
├──────────────────────────────────────────────────────────┤
│  Tenant*:        [Select tenant... ▾]                    │
│  Amount*:        [₱__________]                           │
│  Date Received*: [____-__-__]                            │
│  Date Deposited: [____-__-__]                            │
│  Method*:        [Cash ▾]                                │
│  Reference#:     [________________________]              │
│  Remarks:        [________________________]              │
│                                                          │
│  ── EWT (Corporate Tenants) ──                           │
│  (shown if tenant.is_corporate)                          │
│  EWT Withheld:   [₱__________]                           │
│  2307 Received:  [ ] Yes  (if yes, show upload)          │
│                                                          │
│  ── Payment Allocation ──                                │
│  Outstanding charges for Cruz:                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │ [x] Feb Penalty — ₱84.00 (oldest, Art. 1253)     │  │
│  │ [x] Feb Rent    — ₱8,500 (most onerous)          │  │
│  │ [ ] Feb Water   — ₱197.40                         │  │
│  │ [ ] Feb Electric — ₱2,017.50                      │  │
│  │ [ ] Mar Rent    — ₱8,500                          │  │
│  │                                                    │  │
│  │ Auto-allocation: Art. 1253 (penalties first) then  │  │
│  │ Art. 1254 (most onerous). Override: click charges.│  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  Payment: ₱5,000  │ Allocated: ₱5,000  │ Remaining: ₱0  │
│                                                          │
│           [Cancel]  [Record Payment]                     │
└──────────────────────────────────────────────────────────┘
```

**Key features:**
- Auto-allocation per Civil Code Art. 1252-1254 (penalties first, then most onerous)
- Override: admin can manually check/uncheck charges to allocate
- EWT section appears for corporate tenants (5% withholding)
- 2307 receipt tracking integrated
- Receipt (OR) number auto-assigned from DocumentSequence

### 5.3 Tenant Balance Dashboard

```
┌──────────────────────────────────────────────────────────┐
│  Tenant Balances                        [Export CSV]      │
├──────────────────────────────────────────────────────────┤
│ Filter: [All ▾] [Has Balance ▾]  Sort: [Oldest First ▾]  │
├──────────────────────────────────────────────────────────┤
│ Tenant    │ Billed  │ Paid    │Balance │Days│ Months│Flag│
│───────────│─────────│─────────│────────│────│───────│────│
│ Kim Corp  │ ₱432K   │ ₱400K   │₱32.1K  │ 45 │  2    │ ⚠️ │
│ Cruz      │ ₱102K   │ ₱86.8K  │₱15.2K  │ 45 │  2    │ ⚠️ │
│ Reyes     │ ₱86.4K  │ ₱78.0K  │₱ 8.4K  │ 30 │  1    │    │
│ Santos    │ ₱540K   │ ₱540K   │₱  0    │  0 │  0    │ ✅ │
│ ...       │         │         │        │    │       │    │
├──────────────────────────────────────────────────────────┤
│ TOTALS    │₱1.2M    │₱1.1M    │₱95.7K  │              │  │
│                                                          │
│ 🔴 0 tenants at 3-month ejectment threshold              │
│ ⚠️ 2 tenants at 2-month warning                          │
└──────────────────────────────────────────────────────────┘
```

---

## 6. Security Deposit Views (P7)

### 6.1 Deposit List

```
┌──────────────────────────────────────────────────────────┐
│  Security Deposits                                       │
├──────────────────────────────────────────────────────────┤
│ Tenant    │ Amount  │ Regime  │ Status    │ Interest│Bank│
│───────────│─────────│─────────│───────────│─────────│────│
│ Cruz      │ ₱17,000 │Controlled│ Held      │ ₱423    │BDO │
│ Santos    │₱135,000 │Commercial│ Held      │  —      │ —  │
│ Lee (old) │ ₱24,000 │Controlled│ Refunding │ ₱156    │BDO │
│ ...       │         │         │           │         │    │
├──────────────────────────────────────────────────────────┤
│ Total deposits held: ₱876,000                            │
└──────────────────────────────────────────────────────────┘
```

### 6.2 Deposit Detail / Lifecycle View

```
┌──────────────────────────────────────────────────────────┐
│  Security Deposit — Juan Cruz (Lease #12)                │
├──────────────────────────────────────────────────────────┤
│  Amount: ₱17,000 (2 months' rent)                       │
│  Regime: Controlled Residential                          │
│  Bank: BDO SA #1234-5678                                │
│  Accrued Interest: ₱423.00                              │
│  Status: HELD                                            │
│                                                          │
│  ── Lifecycle Timeline ──                                │
│  ● Jan 2024 — Collected (₱17,000)                       │
│  ● Jul 2024 — Interest accrued (₱112)                   │
│  ● Jan 2025 — Interest accrued (₱156)                   │
│  ● Jul 2025 — Interest accrued (₱155)                   │
│  ○ (pending) — Lease end: deduction + refund             │
│                                                          │
│  ── Actions (at lease end) ──                            │
│  [Record Deductions]  [Process Refund]  [Forfeit]        │
└──────────────────────────────────────────────────────────┘
```

### 6.3 Deposit Deduction Form (Admin, at lease end)

```
┌──────────────────────────────────────────────────────────┐
│  Record Deductions — Cruz (Lease #12)                    │
├──────────────────────────────────────────────────────────┤
│  Deposit: ₱17,000  │  Interest: ₱423  │  Total: ₱17,423│
│                                                          │
│  Deductions:                                             │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Description              │ Amount   │ Receipt      │  │
│  │──────────────────────────│──────────│──────────────│  │
│  │ Wall paint damage (3B)   │ ₱3,500   │ [Upload]     │  │
│  │ Broken fixture, bathroom │ ₱1,200   │ [Upload]     │  │
│  │                    [+ Add Deduction]                │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  Total Deductions: ₱4,700                                │
│  Refund Amount:    ₱12,723 (₱17,423 − ₱4,700)          │
│                                                          │
│  Tax Reclassification (on applied amount):               │
│  Applied to income: ₱4,700                               │
│  VAT (12%):         ₱564.00                              │
│  EWT (5%):          ₱235.00                              │
│                                                          │
│  Refund Deadline: 1 month from turnover (controlled)     │
│                                                          │
│         [Cancel]  [Process Deductions & Refund]          │
└──────────────────────────────────────────────────────────┘
```

---

## 7. Contract Views (P8, P9)

### 7.1 Contract Template Manager (Admin only)

List of templates by lease regime (Controlled Residential, Commercial). Each template has:
- Base document structure
- Mandatory clauses (auto-included per regime)
- Optional clauses (selectable)
- Variable placeholders ({{tenant_name}}, {{unit}}, {{monthly_rate}}, etc.)

### 7.2 Contract Generation Wizard (Admin only)

```
Step 1: Select lease → Step 2: Choose template → Step 3: Review clauses
→ Step 4: Preview → Step 5: Generate PDF

Step 4 Preview:
┌──────────────────────────────────────────────────────────┐
│  Contract Preview — Lease #48                            │
├──────────────────────────────────────────────────────────┤
│  Template: Controlled Residential Standard               │
│  Tenant: Maria Reyes │ Unit: 2A │ Term: 1 year          │
│  Monthly Rent: ₱7,200 │ Deposit: ₱14,400 │ Advance: ₱7,200│
│                                                          │
│  Mandatory Clauses Included:                             │
│  ✅ RA 9653 deposit cap (2+1)                            │
│  ✅ NHSB escalation cap                                  │
│  ✅ 5-day grace period                                   │
│  ✅ Ejectment grounds (Sec. 9 only)                      │
│                                                          │
│  DST Computation:                                        │
│  Annual rent: ₱86,400                                    │
│  DST: ₱6 + (84 × ₱2) = ₱174.00                        │
│  Filing deadline: 5 days after close of execution month  │
│                                                          │
│  [← Back]  [Download PDF]  [Mark as Generated]          │
└──────────────────────────────────────────────────────────┘
```

### 7.3 Execution Milestone Tracker

```
┌──────────────────────────────────────────────────────────┐
│  Contract Milestones — Lease #48                         │
├──────────────────────────────────────────────────────────┤
│  ● Draft Generated       │ Mar 1, 2026                  │
│  ● Signed by Tenant      │ Mar 5, 2026                  │
│  ● Signed by Lessor      │ Mar 5, 2026                  │
│  ○ Notarized             │ (pending)                     │
│  ○ RD Registered         │ (pending)                     │
│  ○ DST Filed (Form 2000) │ Deadline: Apr 5, 2026        │
│                                                          │
│  [Update Milestone]                                      │
└──────────────────────────────────────────────────────────┘
```

---

## 8. Lease Status & Portfolio Views (P10)

### 8.1 Portfolio Dashboard (Lease Status Board)

```
┌──────────────────────────────────────────────────────────┐
│  Lease Portfolio                                         │
├──────────────────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────────┐   │
│  │ 🟢 Active│ │🟡 Expiring││🔵 M-to-M│ │ 🔴 Holdover  │   │
│  │   35    │ │    3     │ │    5    │ │     2        │   │
│  └─────────┘ └─────────┘ └─────────┘ └──────────────┘   │
│  ┌─────────┐ ┌─────────┐                                │
│  │ ⚫ Ended │ │ 🟣 Draft │                                │
│  │    12   │ │    1    │                                 │
│  └─────────┘ └─────────┘                                │
│                                                          │
│  ┌── Expiring Soon (90 days) ────────────────────────┐   │
│  │ Lease  │ Tenant    │ Unit │ Expires │ Action Needed│  │
│  │────────│───────────│──────│─────────│──────────────│  │
│  │ #24    │ Santos    │ G1-3 │ Mar 26  │ Renew/Notify│  │
│  │ #36    │ Tan Corp  │ 4A   │ Apr 15  │ Renew/Notify│  │
│  │ #41    │ Gomez     │ 2C   │ May 30  │ 90-day alert│  │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌── Reconduction Watch ─────────────────────────────┐   │
│  │ Lease #30 — Kim Lee (5C): Expired Dec 25,         │  │
│  │ Day 12 of 15-day window. If no notice by Dec 30,  │  │
│  │ auto-transitions to MONTH_TO_MONTH.               │  │
│  │ [Send Non-Renewal Notice]  [Allow Reconduction]    │  │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌── Monthly Revenue by Status ──────────────────────┐   │
│  │ Active:  ₱175,000/mo  │  M-to-M: ₱36,000/mo      │  │
│  │ Total:   ₱211,000/mo  │  Vacancy loss: ₱48,000/mo │  │
│  └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

### 8.2 Lease Event Log (within Lease Detail)

```
┌──────────────────────────────────────────────────────┐
│  Lease Events — #12 (Cruz)                           │
├──────────────────────────────────────────────────────┤
│ Date       │ Event                │ By    │ Details  │
│────────────│──────────────────────│───────│──────────│
│ Jan 1, 24  │ CREATED (Draft)      │ Admin │          │
│ Jan 5, 24  │ ACTIVATED            │ Admin │ Signed   │
│ Jan 1, 25  │ ESCALATION_APPLIED   │ System│ +2.3%    │
│ Jan 1, 26  │ ESCALATION_APPLIED   │ System│ +1.0%    │
│ Oct 1, 25  │ EXPIRY_ALERT_90D     │ System│          │
│ ...        │                      │       │          │
└──────────────────────────────────────────────────────┘
```

---

## 9. Rent Roll & Reporting Views (P11)

### 9.1 Rent Roll Generator

```
┌──────────────────────────────────────────────────────────┐
│  Rent Roll — March 2026                    [Export XLSX]  │
│                                            [Export CSV]   │
├──────────────────────────────────────────────────────────┤
│  (Horizontal scroll — 26 columns)                        │
│                                                          │
│ Tenant│TIN  │Unit│Type│Term    │Rate │Esc.│VAT │Gross│VAT│
│───────│─────│────│────│────────│─────│────│────│─────│───│
│ Cruz  │123..│3B  │Res │Jan24-  │8.5K │1%  │Expt│8.5K │ 0 │
│       │     │    │    │Dec25   │     │    │    │     │   │
│ Santos│987..│G1  │Com │Mar24-  │15K  │5%  │12% │15K  │1.8│
│       │     │G2  │Com │Mar26   │15K  │5%  │12% │15K  │1.8│
│       │     │G3  │Com │        │15K  │5%  │12% │15K  │1.8│
│ ...   │     │    │    │        │     │    │    │     │   │
│───────│─────│────│────│────────│─────│────│────│─────│───│
│                                                          │
│ (continued: Total Billed, Collected, EWT, Net, Balance,  │
│  Invoice#, OR#, 2307 Status, Deposit, Lease Status,      │
│  Days Overdue, Notes, LIS Flag, SAWT Flag, Adj Flag)    │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ TOTALS: Billed ₱239.2K │ Collected ₱213K │ Balance ₱26.2K│
│ VAT Exempt: ₱68K │ VATable: ₱171.2K │ Output VAT: ₱20.5K│
└──────────────────────────────────────────────────────────┘
```

**26 columns** (from process catalog Sec. P11):
1. Tenant Name
2. TIN
3. Unit
4. Unit Type (Res/Com)
5. Lease Term
6. Monthly Rate
7. Escalation Date
8. VAT Status
9. Gross Rent Billed (base)
10. VAT Billed
11. Total Billed
12. Amount Collected (cash)
13. EWT Withheld
14. Net Collected
15. Prior Balance
16. Current Balance
17. Invoice #
18. Receipt #
19. 2307 Status
20. Deposit Held
21. Lease Status
22. Days Overdue
23. Notes
24. LIS Flag
25. SAWT Flag
26. Adjustment Flag

**Both roles** can view and export. This is the primary accountant deliverable.

### 9.2 LIS Report (Semi-annual)

```
┌──────────────────────────────────────────────────────────┐
│  LIS Report — H1 2026 (Jan-Jun)           [Export XLSX]  │
├──────────────────────────────────────────────────────────┤
│ Payor TIN │ Name    │ Address  │ Income  │ Tax Withheld │
│───────────│─────────│──────────│─────────│──────────────│
│ 987-654.. │ Santos  │ Makati   │ ₱270,000│ ₱13,500      │
│ 456-789.. │ LimTech │ Pasay    │ ₱192,600│ ₱ 9,630      │
│ ...       │         │          │         │              │
├──────────────────────────────────────────────────────────┤
│ 9 prescribed columns per RR 12-2011                      │
│ Filing deadline: Jul 15, 2026                            │
└──────────────────────────────────────────────────────────┘
```

---

## 10. Tax Data Views (P12)

### 10.1 Tax Data Compilation Dashboard (Admin + Accountant)

```
┌──────────────────────────────────────────────────────────┐
│  Tax Data — Q1 2026 (Jan-Mar)                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌── Output VAT (for 2550Q) ─────────────────────────┐   │
│  │ VATable Sales:     ₱513,600                       │   │
│  │ Exempt Sales:      ₱204,000                       │   │
│  │ Output VAT:        ₱ 61,632                       │   │
│  │ Input VAT Credits: ₱  8,456                       │   │
│  │ Net VAT Payable:   ₱ 53,176                       │   │
│  │                               [Export 2550Q Data]  │   │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌── Income Tax (for 1702Q) ─────────────────────────┐   │
│  │ Gross Rental Income: ₱717,600                     │   │
│  │ Deductible Expenses: ₱124,500                     │   │
│  │ Taxable Income:      ₱593,100                     │   │
│  │ RCIT (25%):          ₱148,275                     │   │
│  │                               [Export 1702Q Data]  │   │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌── EWT Summary ────────────────────────────────────┐   │
│  │ EWT on suppliers (remitted):     ₱ 6,225          │   │
│  │ EWT from tenants (certificates): ₱18,750          │   │
│  │ 2307s received: 8/10 expected                     │   │
│  │ Missing: TenantCorp (Q1), LimTech (Q1)            │   │
│  │                    [Export 0619-E] [Export 1601-EQ] │   │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌── DST Register ──────────────────────────────────┐    │
│  │ Lease #48 — Reyes: ₱174 (filed Mar 5)            │   │
│  │ Lease #49 — Park:  ₱312 (due Apr 5)              │   │
│  │                                    [Export DST]    │   │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌── SLSP (Sales/Purchases) ────────────────────────┐    │
│  │ Sales list: 47 entries (from P5 billing)          │   │
│  │ Purchases: 23 entries (from P14 expenses)         │   │
│  │                                   [Export SLSP]    │   │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  Filing Deadlines:                                       │
│  🟡 2550Q + SLSP: Apr 25 (23 days)                      │
│  🔵 1601-EQ + QAP: Apr 30 (28 days)                     │
│  🔵 1702Q + SAWT: May 30 (58 days)                      │
└──────────────────────────────────────────────────────────┘
```

### 10.2 2307 Tracking View

```
┌──────────────────────────────────────────────────────────┐
│  2307 Certificate Tracking — Q1 2026                     │
├──────────────────────────────────────────────────────────┤
│ Tenant    │ Expected│ Received │ Amount  │ Reconciled│Act│
│───────────│─────────│──────────│─────────│───────────│───│
│ Santos    │ ₱6,750  │ ₱6,750   │ Match   │ ✅        │   │
│ LimTech   │ ₱4,815  │ —        │ Missing │ ❌        │ ⚡│
│ TenantCorp│ ₱5,625  │ —        │ Missing │ ❌        │ ⚡│
│ Kim Corp  │ ₱1,560  │ ₱1,560   │ Match   │ ✅        │   │
├──────────────────────────────────────────────────────────┤
│ Expected: ₱18,750  │ Received: ₱14,310  │ Gap: ₱4,440  │
│ Deadline: 20 days after Q-end (Apr 20)                   │
│                                                          │
│ ⚡ = Follow-up needed                                     │
└──────────────────────────────────────────────────────────┘
```

---

## 11. Document Views (P13)

### 11.1 Invoice Register

```
┌──────────────────────────────────────────────────────────┐
│  Invoice Register                        [Download All]  │
├──────────────────────────────────────────────────────────┤
│ Invoice #   │ Date    │ Tenant  │ Amount  │ VAT   │Stat  │
│─────────────│─────────│─────────│─────────│───────│──────│
│ INV-2026-341│ Mar 1   │ Cruz    │ ₱10,867 │ ₱0    │Issued│
│ INV-2026-342│ Mar 1   │ Santos  │ ₱57,102 │₱6,160 │Issued│
│ INV-2026-343│ Mar 1   │ Reyes   │ ₱ 9,234 │ ₱0    │Issued│
│ ...         │         │         │         │       │      │
├──────────────────────────────────────────────────────────┤
│ Series: INV-2026 │ ATP: ATP-2024-00123                   │
│ Range: 001–500   │ Used: 343/500 (69%)                   │
│ ⚠️ 80% exhaustion alert at INV-2026-400                   │
└──────────────────────────────────────────────────────────┘
```

### 11.2 Receipt Register

Same structure but for Official Receipts (OR series), issued at payment.

### 11.3 ATP Management (Admin only)

```
┌──────────────────────────────────────────────────────────┐
│  Authority to Print (ATP) Management                     │
├──────────────────────────────────────────────────────────┤
│ ATP #         │ Type    │ Series Range│ Used │ Remaining │
│───────────────│─────────│─────────────│──────│───────────│
│ ATP-2024-00123│ Invoice │ 001–500     │ 343  │ 157 (31%) │
│ ATP-2024-00124│ Receipt │ 001–500     │ 235  │ 265 (53%) │
│ ATP-2024-00125│ CrMemo  │ 001–100     │   4  │  96 (96%) │
├──────────────────────────────────────────────────────────┤
│ Alert Thresholds: 80% → Warning, 90% → Urgent           │
│                                                          │
│ [+ Register New ATP]                                     │
└──────────────────────────────────────────────────────────┘
```

### 11.4 Invoice / Receipt Detail (PDF Preview + Download)

Clicking an invoice/receipt opens a detail view with:
- All 16 mandatory fields per RR 7-2024
- Line items with VAT breakdown
- PDF preview (rendered)
- Download button

---

## 12. Expense Views (P14)

### 12.1 Expense List

```
┌──────────────────────────────────────────────────────────┐
│  Expenses                            [+ New Disbursement]│
├──────────────────────────────────────────────────────────┤
│ Date    │ Payee        │ Category  │ Amount │ EWT  │Net  │
│─────────│──────────────│───────────│────────│──────│─────│
│ Mar 2   │ ABC Plumbing │ Repairs   │ ₱15,000│₱750  │₱14.3│
│ Mar 1   │ Meralco      │ Utilities │ ₱124.5K│₱2,490│₱122K│
│ Feb 28  │ Guard Agency │ Security  │ ₱45,000│₱2,250│₱42.8│
│ ...     │              │           │        │      │     │
├──────────────────────────────────────────────────────────┤
│ Month total: ₱234,500 │ EWT withheld: ₱11,725           │
└──────────────────────────────────────────────────────────┘
```

### 12.2 Disbursement Voucher Form (Admin only)

```
┌──────────────────────────────────────────────────────────┐
│  New Disbursement Voucher                                │
├──────────────────────────────────────────────────────────┤
│  Payee*:         [Select or create... ▾]                 │
│  Date*:          [____-__-__]                            │
│  Category*:      [Select category... ▾]                  │
│                  (shows ATC code + EWT rate)              │
│  Description*:   [________________________]              │
│                                                          │
│  Amount (gross)*: [₱__________]                          │
│  VAT (input):     [₱__________] (auto if VAT-reg payee) │
│  EWT Rate:        [5%] (auto from category × payee type) │
│  EWT Amount:      ₱750.00 (computed)                     │
│  Net Payment:     ₱14,250.00 (computed)                  │
│                                                          │
│  Supporting Doc:  [Upload Receipt/Invoice]               │
│                                                          │
│  ── Fixed Asset? ──                                      │
│  [ ] This is a capital expenditure (> ₱1M threshold)     │
│  If checked:                                             │
│    Useful Life:   [___] years                            │
│    Residual (5%): ₱750.00 (computed)                     │
│    Annual Depr:   ₱2,850.00 (computed)                   │
│                                                          │
│           [Cancel]  [Save Voucher]                       │
└──────────────────────────────────────────────────────────┘
```

### 12.3 Expense Reports (Admin + Accountant)

Available exports:
1. **Expense Register** — all disbursements, chronological
2. **Input VAT Register** — VAT from supplier invoices
3. **EWT Summary** — EWT withheld on suppliers, grouped by ATC code
4. **Form 2307 Data** — generated 2307s for suppliers (to issue)
5. **QAP Data** — quarterly alphalist of payees
6. **Fixed Asset Schedule** — all capital items with depreciation
7. **Depreciation Schedule** — monthly/annual depreciation entries
8. **Expense Summary by Category** — totals per expense type
9. **SLSP Purchases** — purchases list for quarterly SLSP filing

---

## 13. Settings Views (Admin only)

### 13.1 Company Settings

- Company name, TIN, RDO code, SEC registration
- VAT registration status, aggregate threshold tracking
- Fiscal year settings

### 13.2 User Management

- List users (admin, accountant)
- Invite user (email, role assignment)
- Deactivate user

### 13.3 Charge Type Configuration

```
┌──────────────────────────────────────────────────────────┐
│  Charge Types                            [+ New Type]    │
├──────────────────────────────────────────────────────────┤
│ Code │ Name              │ VAT Default │ Category       │
│──────│───────────────────│─────────────│────────────────│
│ RENT │ Monthly Rent       │ Per unit    │ Billing        │
│ WATR │ Water Charge       │ Non-VATable │ Utility        │
│ ELEC │ Electric Charge    │ Configurable│ Utility        │
│ PNTY │ Late Penalty       │ 12% VAT    │ Penalty        │
│ DPST │ Deposit Application│ 12% VAT    │ Deposit        │
│ ADMN │ Admin Fee (Electric)│ Configurable│ Fee           │
│ ...  │                   │             │                │
└──────────────────────────────────────────────────────────┘
```

### 13.4 Expense Category Configuration

- ATC code, description, EWT rates by payee type (individual/corporate, VAT/non-VAT, large taxpayer)
- 14 categories from RR 02-98

### 13.5 Supplier/Payee Management

- Name, TIN, type (individual/corporate), VAT status, large taxpayer flag

---

## 14. Cross-Cutting UI Patterns

### 14.1 Data Tables

Every list view uses a consistent table component:
- **Search:** Full-text across visible columns
- **Filters:** Dropdowns per relevant column
- **Sort:** Click column header (ascending/descending)
- **Pagination:** 20 rows default, configurable
- **Export:** CSV, XLSX buttons where applicable
- **Row click:** Navigate to detail view

### 14.2 Forms

- **Required fields** marked with *
- **Real-time validation** (Zod schemas) — show error below field
- **Auto-computation** — derived fields update as inputs change (e.g., EWT, VAT, net amount)
- **Conditional sections** — show/hide based on tenant type, lease regime, etc.
- **Confirmation modals** for destructive/irreversible actions (finalize billing, apply penalties)

### 14.3 Wizard / Multi-Step Flows

Used for: Billing Run (P5), Contract Generation (P8), Deposit Processing (P7)
- Step indicator at top
- Back/Next navigation
- Summary/preview before final action
- Success confirmation with next-action links

### 14.4 Detail Views (Entity Detail Pages)

Consistent tabbed layout:
- **Header:** Entity name, key identifiers, status badge, action buttons
- **Tabs:** Contextual sections (Overview, Related Records, History, Documents)
- **Related records:** Inline tables within tabs (e.g., charges within lease detail)

### 14.5 Dashboard Widgets

- **KPI Cards:** Large number + label + trend indicator
- **Tables:** Compact, 5-10 rows, "View All" link
- **Alerts:** Color-coded by severity (Info/Warning/Urgent/Overdue)
- **Progress Checklist:** Monthly close workflow tracker

### 14.6 Exports & Downloads

| Export Type | Format | Role | Source |
|-------------|--------|------|--------|
| Rent Roll | XLSX, CSV | Both | P11 |
| LIS Report | XLSX | Both | P11 |
| SAWT | XLSX | Both | P12 |
| 2550Q Data | XLSX | Both | P12 |
| 1702Q Data | XLSX | Both | P12 |
| EWT Summary | XLSX | Both | P12 |
| DST Register | XLSX | Both | P12 |
| SLSP | XLSX | Both | P12 |
| Expense Register | XLSX, CSV | Both | P14 |
| Input VAT Register | XLSX | Both | P14 |
| Fixed Asset Schedule | XLSX | Both | P14 |
| Depreciation Schedule | XLSX | Both | P14 |
| Invoice PDF | PDF | Both | P13 |
| Receipt PDF | PDF | Both | P13 |
| Contract PDF | PDF | Admin | P8 |
| Billing Statement PDF | PDF | Both | P5 |
| 2307 for Supplier | PDF | Admin | P14 |
| Tenant Balance Report | CSV | Both | P6 |

---

## 15. Role-Based Access Matrix

### 15.1 Page-Level Access

| Page/View | Admin | Accountant |
|-----------|:-----:|:----------:|
| Dashboard | ✅ Full | ✅ Read-only (no close checklist) |
| Tenant List/Detail | ✅ CRUD | ✅ Read |
| Lease List/Detail | ✅ CRUD | ✅ Read |
| Property/Room/Rentable | ✅ CRUD | ✅ Read |
| Rent Escalation | ✅ Full | ❌ |
| Water Billing | ✅ Full | ❌ |
| Electric Billing | ✅ Full | ❌ |
| Late Penalties | ✅ Full | ❌ |
| Billing Runs | ✅ Full | ❌ |
| Record Payment | ✅ Full | ❌ |
| Payment List | ✅ Full | ✅ Read |
| Tenant Balances | ✅ Full | ✅ Read + Export |
| Security Deposits | ✅ Full | ✅ Read |
| Contract Templates | ✅ Full | ❌ |
| Contract Generation | ✅ Full | ❌ |
| Rent Roll | ✅ Full | ✅ Read + Export |
| Tax Data Compilation | ✅ Full | ✅ Read + Export |
| 2307 Tracking | ✅ Full | ✅ Read |
| Invoice/Receipt Register | ✅ Full | ✅ Read + Download |
| ATP Management | ✅ Full | ❌ |
| Expense Entry | ✅ Full | ❌ |
| Expense Reports | ✅ Full | ✅ Read + Export |
| Settings | ✅ Full | ❌ |

### 15.2 Action-Level Access

| Action | Admin | Accountant |
|--------|:-----:|:----------:|
| Create/Edit entities | ✅ | ❌ |
| Delete entities | ✅ | ❌ |
| Run billing | ✅ | ❌ |
| Finalize billing run | ✅ | ❌ |
| Record payments | ✅ | ❌ |
| Apply escalation | ✅ | ❌ |
| Apply penalties | ✅ | ❌ |
| Process deposits | ✅ | ❌ |
| Generate contracts | ✅ | ❌ |
| Update milestones | ✅ | ❌ |
| Export reports | ✅ | ✅ |
| Download PDFs | ✅ | ✅ |
| View dashboards | ✅ | ✅ |
| View detail pages | ✅ | ✅ |
| Manage settings | ✅ | ❌ |
| Manage users | ✅ | ❌ |

---

## 16. View Inventory Summary

| Category | Views | Forms | Tables | Exports | Dashboards |
|----------|:-----:|:-----:|:------:|:-------:|:----------:|
| Foundation (F0) | 9 | 4 | 5 | — | — |
| Billing (P1-P5) | 8 | 5 | 6 | — | 1 |
| Payments (P6) | 3 | 1 | 3 | 1 | 1 |
| Deposits (P7) | 3 | 1 | 2 | — | — |
| Contracts (P8-P9) | 4 | 2 | 2 | 1 | — |
| Lease Status (P10) | 2 | — | 2 | — | 1 |
| Rent Roll (P11) | 2 | — | 2 | 2 | — |
| Tax Data (P12) | 2 | — | 3 | 6 | 1 |
| Documents (P13) | 4 | 1 | 3 | 2 | — |
| Expenses (P14) | 3 | 1 | 3 | 9 | — |
| Settings | 5 | 4 | 4 | — | — |
| Global | 2 | — | — | — | 2 |
| **TOTAL** | **~47** | **~19** | **~35** | **~21** | **~6** |

---

*Extracted from 14 process descriptions, cross-cutting concerns (Sec. 7), and data pipeline summary (Sec. 10). ASCII mockups represent layout intent — actual implementation will use component library (shadcn/ui or similar). All views designed for desktop-first; responsive layout is secondary priority given back-office context.*
