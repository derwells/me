# Data Flow Mapping

**Wave:** 3 (Handoff & Integration Analysis)
**Analyzed:** 2026-02-26
**Dependencies:** All Wave 2 process analyses (14 aspects)

---

## 1. Overview

This analysis maps the complete data pipeline for a SEC-registered Las Piñas rental corporation: from daily operational data entry, through monthly processing and reporting, to quarterly/annual BIR and SEC filings handled by the external accounting agency.

The pipeline has four layers:

1. **Data Entry** — events that create or modify records (lease signing, meter reading, payment receipt, expense disbursement)
2. **Computation** — processes that derive values from entered data (billing, escalation, penalties, deposit interest)
3. **Reporting & Handoff** — outputs assembled from computed data for the accountant (rent roll, invoice log, expense vouchers, 2307 tracker)
4. **Filing** — BIR/SEC forms the accountant produces from the handoff package (2550Q, 1702Q, 1601-EQ, 1604-E, 2000, GIS, AFS)

---

## 2. Data Flow Diagram (Text)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     LAYER 1: DATA ENTRY                             │
│  (Events that create/modify records — human action required)        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Lease Mgmt   │  │ Meter        │  │ Payment Recording        │  │
│  │              │  │ Readings     │  │                          │  │
│  │ • New lease  │  │ • Water      │  │ • Tenant payments        │  │
│  │ • Renewal    │  │ • Electric   │  │ • Payment method         │  │
│  │ • Extension  │  │ • Monthly    │  │ • Allocation to charges  │  │
│  │ • Non-renewal│  │              │  │                          │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────────┘  │
│         │                 │                      │                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Expense      │  │ 2307 Receipt │  │ Deposit Events           │  │
│  │ Disbursement │  │              │  │                          │  │
│  │ • Suppliers  │  │ • Corporate  │  │ • Collection at signing  │  │
│  │ • Repairs    │  │   tenant EWT │  │ • Deduction at end       │  │
│  │ • Permits    │  │   certificates│ │ • Refund/forfeiture      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────────┘  │
│         │                 │                      │                  │
└─────────┼─────────────────┼──────────────────────┼──────────────────┘
          │                 │                      │
          ▼                 ▼                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   LAYER 2: COMPUTATION                              │
│  (Deterministic processes that derive values — automatable)         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Lease Mgmt ─────► ┌──────────────────┐                            │
│                     │ Rent Escalation  │ (annual, per lease)        │
│                     │ NHSB cap / CPI / │                            │
│                     │ contractual %    │                            │
│                     └────────┬─────────┘                            │
│                              │                                      │
│  Meter Readings ──► ┌────────┴──────────┐ ┌──────────────────────┐ │
│                     │ Utility Billing    │ │ Late Payment         │ │
│                     │ • Water (per-tier) │ │ Penalties            │ │
│                     │ • Electric (blend) │ │ • Controlled: 1%/mo  │ │
│                     └────────┬───────────┘ │   cap 1mo rent/yr   │ │
│                              │             │ • Commercial: per    │ │
│                              ▼             │   contract           │ │
│                     ┌────────────────────┐ └──────────┬───────────┘ │
│                     │ Monthly Billing    │            │             │
│  Escalated Rent ───►│ Generation         │◄───────────┘             │
│  Utility Charges ──►│                    │                          │
│  Penalties ────────►│ • VAT computation  │                          │
│  Other Charges ────►│ • Invoice issuance │                          │
│                     │ • Statement output │                          │
│                     └────────┬───────────┘                          │
│                              │                                      │
│  Payments ──► ┌──────────────┴───────────────┐                     │
│               │ Payment Allocation &          │                     │
│               │ Balance Tracking              │                     │
│               │ • Art. 1253 interest-first    │                     │
│               │ • Running balance per tenant  │                     │
│               │ • Arrears monitoring          │                     │
│               │ • Receipt issuance            │                     │
│               └──────────────┬───────────────┘                     │
│                              │                                      │
│  Deposit Events ──► ┌────────┴───────────────┐                     │
│                     │ Security Deposit        │                     │
│                     │ Lifecycle               │                     │
│                     │ • Interest accrual      │                     │
│                     │ • Deduction calc        │                     │
│                     │ • Tax reclassification  │                     │
│                     └────────┬───────────────┘                     │
│                              │                                      │
│  Lease Mgmt ──► ┌────────────┴───────────────┐                     │
│                 │ DST Computation             │                     │
│                 │ TRAIN rates: PHP 6/PHP 2    │                     │
│                 │ Per lease execution/renewal  │                     │
│                 └────────────┬───────────────┘                     │
│                              │                                      │
│  Lease Dates ──► ┌───────────┴──────────────┐                      │
│                  │ Lease Status Engine       │                      │
│                  │ ACTIVE→EXPIRED→M2M/       │                      │
│                  │ HOLDOVER/RENEWED/TERMINATED│                     │
│                  │ + Alert system             │                      │
│                  └───────────┬──────────────┘                      │
│                              │                                      │
└──────────────────────────────┼──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│               LAYER 3: REPORTING & HANDOFF                          │
│  (Outputs assembled for accountant — monthly/quarterly)             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────┐  ┌──────────────────────────────┐ │
│  │ Rent Roll (26 cols)         │  │ Invoice Register             │ │
│  │ MONTHLY — by 5th            │  │ MONTHLY                      │ │
│  │                             │  │                              │ │
│  │ Sources:                    │  │ Sources:                     │ │
│  │ • Lease Status Engine       │  │ • Monthly Billing (invoices) │ │
│  │ • Billing Generation        │  │ • Payment Tracking (receipts)│ │
│  │ • Payment Tracking          │  │ • DST Records               │ │
│  │ • Balance Tracking          │  │                              │ │
│  │ • 2307 Tracker              │  │ Feeds:                       │ │
│  │ • Security Deposits         │  │ → Accountant books of accts  │ │
│  │ • Invoice/Receipt Data      │  │ → BIR audit trail            │ │
│  │                             │  │ → EIS (future)               │ │
│  │ Feeds:                      │  └──────────────────────────────┘ │
│  │ → 2550Q (VAT split)        │                                   │
│  │ → 1702Q (gross income)     │  ┌──────────────────────────────┐ │
│  │ → SAWT (2307 data)         │  │ Expense Voucher Package      │ │
│  │ → LIS (9-col subset)       │  │ MONTHLY                      │ │
│  │ → AFS (AR aging, PFRS 16)  │  │                              │ │
│  └─────────────────────────────┘  │ Sources:                     │ │
│                                   │ • Expense Disbursements      │ │
│  ┌─────────────────────────────┐  │ • Supplier invoices/receipts │ │
│  │ 2307 Tracker                │  │ • EWT computation            │ │
│  │ QUARTERLY                   │  │                              │ │
│  │                             │  │ Feeds:                       │ │
│  │ Sources:                    │  │ → 1601-EQ (EWT withheld)     │ │
│  │ • Corporate tenant 2307s   │  │ → 1702Q (deductions)         │ │
│  │ • Rent Roll (expected amts) │  │ → AFS (expense schedules)   │ │
│  │                             │  │ → Input VAT register         │ │
│  │ Feeds:                      │  └──────────────────────────────┘ │
│  │ → SAWT DAT file            │                                   │
│  │ → 1702Q (tax credits)      │  ┌──────────────────────────────┐ │
│  │ → 2550Q (tax credits)      │  │ DST Register                 │ │
│  └─────────────────────────────┘  │ PER-EVENT                    │ │
│                                   │                              │ │
│  ┌─────────────────────────────┐  │ Sources:                     │ │
│  │ Lessee Information          │  │ • Lease Contract Generation  │ │
│  │ Statement (LIS)             │  │ • Lease Renewal/Extension    │ │
│  │ SEMI-ANNUAL                 │  │                              │ │
│  │                             │  │ Feeds:                       │ │
│  │ Sources:                    │  │ → BIR Form 2000             │ │
│  │ • Rent Roll (9-col subset) │  │   (within 5 days after       │ │
│  │ • Lease records             │  │    month-end of execution)   │ │
│  │ • Tenant TINs               │  └──────────────────────────────┘ │
│  │                             │                                   │
│  │ Feeds:                      │                                   │
│  │ → BIR RDO (Jan 31/Jul 31) │                                   │
│  └─────────────────────────────┘                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  LAYER 4: BIR / SEC FILINGS                         │
│  (External accountant produces from Layer 3 data)                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  MONTHLY:                                                           │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 0619-E — Monthly EWT Remittance (1st & 2nd month of quarter)  │ │
│  │ Source: Expense Voucher Package (EWT withheld on suppliers)    │ │
│  │ Due: 10th of following month (non-eFPS); 11th-15th (eFPS)     │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  QUARTERLY:                                                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 2550Q — Quarterly VAT Return                                  │ │
│  │ Source: Rent Roll (VATable/exempt split, output VAT)           │ │
│  │       + Input VAT Register (creditable input from expenses)   │ │
│  │       + SAWT (2307 tax credits)                               │ │
│  │ Due: 25th of month after quarter-end                          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 1702Q — Quarterly Income Tax Return                           │ │
│  │ Source: Rent Roll (gross rental income)                        │ │
│  │       + Expense Voucher Package (deductions)                  │ │
│  │       + SAWT (EWT credits from 2307s)                         │ │
│  │       + MCIT tracker (2% comparison from 4th year)            │ │
│  │ Due: 60th day after quarter-end                               │ │
│  └────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 1601-EQ — Quarterly EWT Return                                │ │
│  │ Source: Expense Voucher Package (all EWT withheld on suppliers)│ │
│  │       + 0619-E reconciliation (monthly → quarterly rollup)    │ │
│  │ Due: Last day of month after quarter-end                      │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  PER-EVENT:                                                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ Form 2000 — DST on Lease Execution/Renewal                   │ │
│  │ Source: DST Register (lease amount × term × TRAIN rates)      │ │
│  │ Due: Within 5 days after close of month of execution          │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  SEMI-ANNUAL:                                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ Lessee Information Statement (LIS) — per RR 12-2011           │ │
│  │ Source: LIS Report (9-column subset from rent roll data)      │ │
│  │ Due: Jan 31 (as of Dec 31) / Jul 31 (as of Jun 30)           │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ANNUAL:                                                            │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 1604-E — Annual Information Return on EWT                     │ │
│  │ Source: Expense Voucher Package (full-year EWT withheld)       │ │
│  │       + Alphalist of payees                                   │ │
│  │ Due: March 1                                                  │ │
│  ├────────────────────────────────────────────────────────────────┤ │
│  │ 1702-RT — Annual Income Tax Return                            │ │
│  │ Source: Full-year Rent Roll summaries + Expense summaries     │ │
│  │       + SAWT (annual 2307 credits) + MCIT comparison          │ │
│  │ Due: April 15 (or 15th day of 4th month after FY-end)        │ │
│  ├────────────────────────────────────────────────────────────────┤ │
│  │ SEC GIS — General Information Sheet                           │ │
│  │ Source: Corporate records (stockholders, directors, officers)  │ │
│  │ Due: 30 days after Annual Stockholders' Meeting               │ │
│  ├────────────────────────────────────────────────────────────────┤ │
│  │ AFS — Audited Financial Statements                            │ │
│  │ Source: Full-year Rent Roll + Expense data                    │ │
│  │       + AR aging (PFRS 9 ECL) + Lease disclosures (PFRS 16)  │ │
│  │       + Security deposit liability schedule                   │ │
│  │       + Fixed asset register + depreciation schedules         │ │
│  │ Due: 120 days after FY-end (SEC); April 15 (BIR attachment)  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Process-to-Filing Traceability Matrix

This matrix shows exactly which operational processes (Layer 2) feed which filings (Layer 4), through which reports (Layer 3).

| BIR/SEC Filing | Frequency | Layer 3 Report(s) | Layer 2 Process(es) | Layer 1 Data Entry |
|---|---|---|---|---|
| **0619-E** (Monthly EWT) | Monthly (1st, 2nd month/qtr) | Expense Voucher Package | Expense Tracking | Expense Disbursement |
| **2550Q** (VAT) | Quarterly | Rent Roll (VATable/exempt split) + Input VAT Register | Monthly Billing, Expense Tracking | Lease Mgmt, Payments, Expenses |
| **1702Q** (Income Tax) | Quarterly | Rent Roll (gross income) + Expense Package + SAWT | Monthly Billing, Payment Tracking, Expense Tracking, 2307 Tracking | Lease Mgmt, Payments, Expenses, 2307 Receipts |
| **1601-EQ** (EWT Return) | Quarterly | Expense Voucher Package (quarterly rollup) | Expense Tracking | Expense Disbursement |
| **Form 2000** (DST) | Per-event | DST Register | Lease Contract Gen, Lease Renewal | Lease Mgmt |
| **LIS** (Lessee Info) | Semi-annual | LIS Report (9-col subset) | Lease Status Engine | Lease Mgmt |
| **1604-E** (Annual EWT) | Annual | Expense Voucher Package (full-year) + Alphalist | Expense Tracking | Expense Disbursement |
| **1702-RT** (Annual ITR) | Annual | All of above (annual rollup) | All processes | All data entry |
| **SEC GIS** | Annual | Board Resolution Register | Lease Contract Gen (board resolutions) | Lease Mgmt |
| **AFS** | Annual | Rent Roll (AR aging) + Expense data + Deposit schedule + Lease disclosures | All processes | All data entry |

---

## 4. Monthly Close Pipeline (Sequenced)

The monthly close is the critical recurring workflow. Steps must run in order due to data dependencies:

```
Day 1-3: DATA COLLECTION
├── 1. Meter readings taken (water + electric)
│     └── Requires: physical access to meters
├── 2. Payments received in prior month reconciled
│     └── Requires: bank statement, payment records
└── 3. 2307 certificates received (if quarter-end month)
      └── Requires: corporate tenants issue within 20 days of Q-end

Day 1-3: COMPUTATION (can run in parallel once data is in)
├── 4a. Water billing computed ──────────────────────────────┐
│     └── Input: meter readings + Maynilad bill              │
│     └── Output: per-tenant water charges                   │
├── 4b. Electric billing computed ───────────────────────────┤
│     └── Input: meter readings + Meralco bill               │
│     └── Output: per-tenant electric charges                │
├── 4c. Rent escalation checked (if anniversary month) ──────┤
│     └── Input: lease dates, NHSB cap / contractual rate    │
│     └── Output: updated rent amount for new period         │
└── 4d. Late penalties computed ─────────────────────────────┤
      └── Input: outstanding balances, penalty rules         │
      └── Output: penalty charges per delinquent tenant      │
                                                             │
                                                             ▼
Day 2-3: BILLING (depends on 4a-4d)
├── 5. Monthly billing generated for all active tenants
│     └── Input: escalated rent + utilities + penalties + other
│     └── Output: VAT Sales Invoices (per EOPT)
│     └── Output: Billing statements delivered to tenants
│
├── 6. Payment allocation finalized for prior month
│     └── Input: payments received + Art. 1253 rules
│     └── Output: updated tenant balances, receipts issued
│
└── 7. Expense vouchers compiled
      └── Input: disbursement records + supplier docs
      └── Output: categorized expense package with EWT

Day 3-5: REPORTING (depends on 5-7)
├── 8. Rent roll generated (26 columns)
│     └── Input: billing + collections + balances + 2307s + deposits
│     └── Output: Excel file for accountant
│
├── 9. Invoice register compiled
│     └── Input: all invoices + receipts issued in period
│     └── Output: sequential register for accountant
│
├── 10. 2307 tracker updated (if quarter-end)
│      └── Input: received 2307s vs. expected
│      └── Output: reconciliation for SAWT generation
│
└── 11. Package delivered to accountant
       └── Contents: rent roll + invoice register + expense
           vouchers + 2307 originals + bank statements

QUARTER-END ADDITIONS (on top of monthly close):
├── 12. Output VAT summary for 2550Q
│      └── Input: rent roll VATable/exempt split (3 months)
├── 13. Income summary for 1702Q
│      └── Input: rent roll gross income (3 months) + expenses
├── 14. EWT summary for 1601-EQ
│      └── Input: expense vouchers EWT withheld (3 months)
└── 15. SAWT data prepared from 2307s
       └── Input: 2307 tracker (reconciled amounts)
```

---

## 5. Cross-Process Data Dependencies

These are the concrete data relationships between Wave 2 processes — what each process needs from other processes.

### 5.1 Upstream Dependencies (what each process reads)

| Process | Reads From | Specific Data |
|---|---|---|
| **Rent Escalation** | Lease records | current rent, escalation type, anniversary date |
| | NHSB Cap Rate table | year → allowable % (controlled only) |
| **Water Billing** | Meter Readings | current + previous reading per meter |
| | Maynilad Bill | master meter total, rate schedule |
| | Lease/Tenant | tenant↔meter mapping, tenant type (residential/commercial) |
| **Electric Billing** | Meter Readings | current + previous reading per meter |
| | Meralco Bill | total kWh, total amount |
| | Lease/Tenant | tenant↔meter mapping, floor area (for common area split) |
| **Late Penalties** | Tenant Balance | outstanding amounts per tenant |
| | Lease | controlled vs. commercial, grace period, penalty rate |
| | Demand Records | demand date (interest runs from demand per Art. 2209) |
| **Monthly Billing** | Rent Escalation | current period rent amount |
| | Water Billing | per-tenant water charges |
| | Electric Billing | per-tenant electric charges |
| | Late Penalties | penalty charges to include |
| | Lease Status Engine | active leases to bill |
| | Invoice Sequence | next invoice number |
| **Payment Tracking** | Monthly Billing | charges to allocate payments against |
| | Receipt Sequence | next receipt number |
| | Tenant Balance | prior balance for allocation context |
| **Security Deposit** | Lease | deposit amount, controlled flag, bank details |
| | Tenant Balance | outstanding at lease end (for deduction) |
| **Lease Contract Gen** | Board Resolution | authorized signatory for corporate lessor |
| | Rent Escalation | initial rate + escalation terms |
| | DST computation | tax due on new lease |
| **Lease Status Engine** | Lease records | date_start, date_end, renewal records |
| | NonRenewalNotice | whether notice was issued (reconduction check) |
| | Payment Tracking | arrears level (3-month alert) |
| **Rent Roll** | ALL operational processes | see Section 4 in rent-roll-preparation analysis |
| **Tax Data Compilation** | Rent Roll | VATable/exempt split, gross income |
| | Expense Tracking | deductions, input VAT, EWT withheld |
| | 2307 Tracker | EWT credits for SAWT |
| | DST Register | per-event DST filings |
| | MCIT Tracker | 2% comparison from 4th year |

### 5.2 Downstream Consumers (what each process feeds)

| Process | Feeds Into | Specific Data |
|---|---|---|
| **Lease Management** | Rent Escalation, Monthly Billing, Lease Status, Security Deposit, Contract Gen, Rent Roll, LIS | Tenant/unit/term/rate records |
| **Rent Escalation** | Monthly Billing | Updated rent for current period |
| **Water Billing** | Monthly Billing | Per-tenant water charges |
| **Electric Billing** | Monthly Billing | Per-tenant electric charges |
| **Late Penalties** | Monthly Billing | Penalty charges |
| **Monthly Billing** | Payment Tracking (charges to allocate against), Rent Roll (billed amounts), Invoice Register, 2550Q (output VAT) | Invoices + charges |
| **Payment Tracking** | Rent Roll (collections), Receipt Register, Tenant Balance, 2550Q (uncollected adj.) | Payments + receipts + balances |
| **Security Deposit** | Rent Roll (deposit held column), AFS (liability disclosure), Monthly Billing (at application → income event) | Deposit records |
| **Expense Tracking** | 0619-E, 1601-EQ, 1604-E (EWT withheld), 1702Q (deductions), 2550Q (input VAT), AFS (expense schedules) | Vouchers + EWT + input VAT |
| **2307 Tracking** | SAWT → 1702Q + 2550Q (tax credits), Rent Roll (2307 status columns) | Reconciled 2307 records |
| **DST Computation** | Form 2000 (per-event filing) | DST amount per lease |
| **Lease Status Engine** | Monthly Billing (which leases to bill), Rent Roll (status column), Lease Renewal (expiry alerts), AFS (PFRS 16 maturity) | Lease states + alerts |
| **Rent Roll** | 2550Q, 1702Q, SAWT, LIS, AFS | The central reporting hub |

---

## 6. The Rent Roll as Central Hub

The rent roll is the single most critical report in the data pipeline. It aggregates data from **every** upstream operational process and feeds **every** downstream filing:

```
                Lease Status ──┐
             Rent Escalation ──┤
              Monthly Billing ──┤
           Payment Tracking ──┤
        Security Deposits ──┤──► RENT ROLL (26 cols) ──┬──► 2550Q (VAT)
            2307 Tracker ──┤                           ├──► 1702Q (Income)
      Invoice/Receipt Data ──┤                           ├──► SAWT (EWT credits)
           Expense Tracking ──┘                           ├──► LIS (semi-annual)
                                                         ├──► AFS (AR aging, PFRS 16)
                                                         └──► Accountant monthly pkg
```

**Implication for automation:** Automating the rent roll has the highest leverage because it sits at the bottleneck between operations and compliance. However, the rent roll is only as good as its upstream data sources — if billing, payments, or 2307 tracking are not automated, the rent roll cannot be auto-generated.

**Recommended automation sequence (dependency-ordered):**

1. **Foundation:** Lease management + tenant master data (everything depends on this)
2. **Billing pipeline:** Rent escalation → water/electric billing → monthly billing generation
3. **Collection pipeline:** Payment recording → payment allocation → balance tracking → receipt issuance
4. **Penalty pipeline:** Late payment penalties (depends on balances from step 3)
5. **Deposit pipeline:** Security deposit lifecycle (depends on lease + payment data)
6. **Contract pipeline:** Lease contract generation → renewal/extension → DST computation
7. **Reporting hub:** Rent roll (depends on all of steps 1-6)
8. **Tax handoff:** 2307 tracking → tax data compilation → expense tracking
9. **Compliance:** LIS, filing calendar, lease status dashboard

Steps 2-6 can proceed in parallel once step 1 is complete. Step 7 requires all of 2-6. Steps 8-9 can proceed in parallel with step 7 for the parts that don't depend on the rent roll.

---

## 7. Data Entry Points Requiring Human Action

These are the irreducible manual steps — data that must be entered by a human because it originates from physical reality or external parties:

| Data Entry | Source | Frequency | Cannot Be Eliminated Because |
|---|---|---|---|
| **Meter readings** | Physical sub-meters | Monthly | Requires physical access; no IoT integration in scope |
| **Payment receipt** | Bank notification, cash, check | As received | External event; bank API integration possible but out of scope |
| **2307 certificate receipt** | Corporate tenant delivers paper | Quarterly | External party action; cannot be automated for the landlord |
| **Supplier invoice/receipt** | Physical document from vendor | Per expense | External document; could be photo-captured but OCR out of scope |
| **Lease terms negotiation** | Business decision | Per lease | Requires human judgment |
| **Deposit deduction assessment** | Property inspection | At lease end | Requires physical inspection + judgment |
| **NHSB rate update** | DHSUD publication | Annual | Regulatory change; manual entry once/year |
| **Meralco/Maynilad rate update** | Utility company notice | Periodic | External rate change; manual entry when announced |
| **Board resolution** | Board meeting | As needed | Corporate governance act |

Everything else in the pipeline is deterministic given these inputs.

---

## 8. Accountant Handoff Package (Monthly)

The external accountant receives the following package by the 5th of each month:

| Document | Contents | Source Processes | Format |
|---|---|---|---|
| **Rent Roll** | 26-column report per Section 4 of rent-roll-preparation | All billing + collection processes | Excel (.xlsx) |
| **Invoice Register** | Sequential list of all invoices issued | Monthly Billing, Deposit Application | Excel |
| **Receipt Register** | Sequential list of all receipts issued | Payment Tracking | Excel |
| **Expense Vouchers** | Categorized disbursements with supporting docs | Expense Tracking | Excel + scanned docs |
| **Bank Statements** | Raw bank transaction data for reconciliation | External (bank) | PDF |
| **2307 Originals** | Physical certificates from corporate tenants | 2307 Tracking | Paper (quarterly) |

### Quarter-End Additions

| Document | Contents | Filing It Feeds | Deadline |
|---|---|---|---|
| **VAT Summary** | VATable sales, exempt sales, output VAT, input VAT | 2550Q | 25th of month after Q-end |
| **EWT Summary** | EWT withheld on suppliers (by ATC code) | 1601-EQ | Last day of month after Q-end |
| **SAWT Data** | 2307 amounts per corporate tenant for DAT file | 1702Q + 2550Q attachment | 60th day after Q-end |
| **Income Summary** | Gross rental income by type, deductions | 1702Q | 60th day after Q-end |

### Annual Additions

| Document | Contents | Filing It Feeds | Deadline |
|---|---|---|---|
| **Full-Year Summaries** | Annual rollup of all quarterly data | 1702-RT, AFS | April 15 |
| **EWT Alphalist** | Per-supplier EWT withheld (full year) | 1604-E | March 1 |
| **AR Aging Schedule** | Receivable aging buckets (PFRS 9 ECL) | AFS | 120 days after FY-end |
| **Lease Schedule** | All leases with PFRS 16 maturity projection | AFS | 120 days after FY-end |
| **Deposit Schedule** | Security deposits held per tenant | AFS | 120 days after FY-end |
| **Fixed Asset Register** | Property, equipment, depreciation | AFS | 120 days after FY-end |
| **DST Register** | All DST payments for the year | 1702-RT attachment | April 15 |
| **GIS Data** | Stockholders, directors, officers | SEC GIS | 30 days after ASM |

---

## 9. Cross-Cutting Concerns

These regulatory or operational concerns affect multiple processes simultaneously:

### 9.1 VAT (affects 6 processes)

VAT treatment cascades through: **Monthly Billing** (output VAT on invoices) → **Payment Tracking** (VAT on accrual, not payment) → **Rent Roll** (VATable/exempt split) → **Tax Data Compilation** (2550Q) → **Security Deposit** (VAT triggered at application) → **Late Penalties** (VAT on penalty as gross receipts).

The VAT status determination (residential ≤ PHP 15K = exempt; else if lessor > PHP 3M aggregate = 12%) must be computed once at the Rentable level and propagated to all downstream processes.

### 9.2 EWT 5% (affects 5 processes)

EWT flows through: **Monthly Billing** (5% withheld by corporate tenants) → **Payment Tracking** (net payment = 95% of base) → **2307 Tracking** (certificate receipt) → **Rent Roll** (2307 columns) → **Tax Data Compilation** (SAWT for 1702Q credit).

Additionally, **Expense Tracking** handles the mirror side: the corporation as withholding agent withholds EWT from suppliers (various rates) → **0619-E** → **1601-EQ** → **1604-E**.

### 9.3 Tenant Type (affects 8 processes)

The `is_corporate` and `unit_type` (RESIDENTIAL/COMMERCIAL) flags on tenant/rentable records propagate to: rent control applicability, VAT treatment, EWT withholding, 2307 expectations, deposit rules, penalty caps, sewerage charges (water billing), and LIS reporting. Getting this classification right at the master data level is critical.

### 9.4 Invoice/Receipt Numbering (affects 4 processes)

Sequential numbering touches: **Monthly Billing** (invoice at accrual), **Payment Tracking** (receipt at collection), **Rent Roll** (invoice/receipt columns), and **Official Receipt Data** (ATP management). The numbering system must be atomic and gapless across all processes that issue documents.

### 9.5 Lease Lifecycle Events (affects 7 processes)

A lease state transition (e.g., ACTIVE → EXPIRED → MONTH_TO_MONTH) affects: **Monthly Billing** (which leases to bill), **Rent Escalation** (when to trigger), **Security Deposit** (deduction/refund at TERMINATED), **Late Penalties** (regime changes at reconduction), **Lease Status Dashboard** (alerts), **Rent Roll** (active lease filter), and **AFS** (PFRS 16 maturity projections).

---

## 10. Identified Data Pipeline Gaps

Issues in the current manual workflow that a system must address:

| Gap | Affected Flows | Impact |
|---|---|---|
| **No shared tenant master** | All processes | Tenant name, TIN, corporate flag entered multiple times inconsistently |
| **No lease status tracking** | Billing → Rent Roll → LIS | Cannot determine which tenants to bill or report on |
| **No invoice numbering** | Billing → Receipt → Rent Roll → Accountant | BIR compliance risk; audit trail broken |
| **No balance rollup** | Payments → Penalties → Rent Roll → AFS | Running balances computed manually; drift errors |
| **No 2307 tracking** | Payments → SAWT → 1702Q | Tax credits not claimed or claimed incorrectly |
| **No expense categorization** | Expenses → 1601-EQ → 1702Q → AFS | EWT under/over-remitted; deductions disallowed |
| **No filing calendar** | All handoff processes | Deadlines missed; penalties incurred |
| **Manual rent roll** | Rent Roll → all filings | Highest single time-cost; error-prone aggregation |
