# Compliance Calendar

**Wave:** 3 (Handoff & Integration Analysis)
**Analyzed:** 2026-02-27
**Dependencies:** corporate-rental-tax, accounting-agency-handoff, tax-data-compilation, official-receipt-data, lease-contract-requirements, data-flow-mapping, process-dependencies

---

## 1. Overview

This analysis maps every recurring filing, renewal, and compliance deadline for a SEC-registered Las Piñas rental corporation into a unified annual calendar. The calendar covers four regulatory domains:

| Domain | Regulator | # of Recurring Deadlines |
|--------|-----------|--------------------------|
| **BIR (national tax)** | Bureau of Internal Revenue | ~30 per year |
| **SEC (corporate)** | Securities and Exchange Commission | 2 per year |
| **LGU (local)** | Las Piñas City / Barangay | ~8 per year (per property) |
| **Other national** | BFP, DENR, City Health Office | ~3 per year (per property) |

**Critical insight:** BIR deadlines are the most numerous and penalty-heavy. LGU deadlines cluster in January (business permit season). SEC deadlines depend on the ASM date. All three domains must be tracked simultaneously — missing one can cascade (e.g., no FSIC → no business permit → penalty).

---

## 2. Monthly Deadlines

### BIR Monthly Filings

| Day | Filing | Form | Description | Legal Basis | Data Source (Process) |
|-----|--------|------|-------------|-------------|----------------------|
| **10th** | EWT remittance (non-eFPS) | 0619-E | Monthly EWT withheld on supplier payments (1st and 2nd months of each quarter only — quarter-end month is covered by 1601-EQ) | NIRC Sec. 57; RR 2-98 | P14 (Expense Tracking) |
| **15th** | EWT remittance (eFPS) | 0619-E | Same as above, extended deadline for eFPS filers | RR 2-98, as amended | P14 (Expense Tracking) |

**Note:** The 0619-E is filed only for months 1 and 2 of each quarter (Jan, Feb, Apr, May, Jul, Aug, Oct, Nov). Quarter-end months (Mar, Jun, Sep, Dec) are reported via the quarterly 1601-EQ.

### Internal Monthly Close (Not a Filing — Operational Deadline)

| Day | Action | Purpose |
|-----|--------|---------|
| **1st–3rd** | Meter readings, payment reconciliation | Data collection for billing |
| **2nd–3rd** | Utility billing, escalation check, penalty computation, billing generation | Computation and invoice issuance |
| **3rd–5th** | Rent roll, invoice register, expense package compiled | Reporting for accountant handoff |
| **By 5th** | Full monthly data package delivered to external accountant | Accountant needs lead time for BIR filings |

---

## 3. Quarterly Deadlines

### BIR Quarterly Filings

| Deadline Pattern | Form | Description | Legal Basis | Data Source |
|-----------------|------|-------------|-------------|-------------|
| **25th of month after Q-end** | 2550Q | Quarterly VAT Return | NIRC Sec. 114; RR 16-2005 | P11 (Rent Roll) → P12 (Tax Data) |
| **25th of month after Q-end** | SLSP | Summary List of Sales/Purchases (attachment to 2550Q) | RR 1-2012 | P5 (Billing), P14 (Expenses) |
| **Last day of month after Q-end** | 1601-EQ + QAP | Quarterly EWT Return + Quarterly Alphalist of Payees | RR 2-98 | P14 (Expense Tracking) |
| **60th day after Q-end** | 1702Q + SAWT | Quarterly Income Tax Return + Summary Alphalist of Withholding Tax at Source | NIRC Sec. 77; RR 2-2006 | P11 (Rent Roll) → P12 (Tax Data) |

### Quarterly Deadlines by Quarter (Calendar Year)

| Quarter | Period | 2550Q + SLSP | 1601-EQ + QAP | 1702Q + SAWT |
|---------|--------|--------------|----------------|--------------|
| Q1 | Jan–Mar | **April 25** | **April 30** | **May 30** |
| Q2 | Apr–Jun | **July 25** | **July 31** | **August 29** |
| Q3 | Jul–Sep | **October 25** | **October 31** | **November 29** |
| Q4 | Oct–Dec | **January 25** | **January 31** | *(Annual 1702-RT covers Q4)* |

### External Inflows (from Corporate Tenants)

| Deadline Pattern | Document | From Whom | Legal Basis |
|-----------------|----------|-----------|-------------|
| **Within 20 days after Q-end** | Form 2307 (Certificate of Creditable Tax Withheld) | Corporate tenants who withheld 5% EWT | RR 2-98, Sec. 2.58 |

**2307 receipt tracking deadlines:**

| Quarter | Expected Receipt By | Action Required |
|---------|-------------------|-----------------|
| Q1 | April 20 | Log, reconcile, deliver to accountant |
| Q2 | July 20 | Log, reconcile, deliver to accountant |
| Q3 | October 20 | Log, reconcile, deliver to accountant |
| Q4 | January 20 | Log, reconcile, deliver to accountant |

---

## 4. Semi-Annual Deadlines

### BIR Semi-Annual Filings

| Deadline | Filing | Description | Legal Basis | Data Source |
|----------|--------|-------------|-------------|-------------|
| **January 31** | LIS (2nd semester, Jul–Dec) | Lessee Information Statement — 9-column Excel filed with RDO | RR 12-2011; RMC 69-2009 | P11 (Rent Roll subset) |
| **July 31** | LIS (1st semester, Jan–Jun) | Same as above, for first half | RR 12-2011; RMC 69-2009 | P11 (Rent Roll subset) |

---

## 5. Annual Deadlines

### BIR Annual Filings

| Deadline | Filing | Form | Description | Legal Basis | Data Source |
|----------|--------|------|-------------|-------------|-------------|
| **January 15** | Loose-leaf books (bound copies) | N/A (ORUS submission) | Bind, register via ORUS with QR stamp | RMC 3-2023; NIRC Sec. 232 | All books of accounts |
| **January 25** | Q4 2550Q + SLSP | 2550Q | Quarterly VAT for Oct–Dec | NIRC Sec. 114 | P12 (Tax Data) |
| **January 30** | CAS soft copy submission | N/A (ORUS/physical media) | Computerized books of accounts for prior year | RMC 3-2023; NIRC Sec. 232 | All books of accounts |
| **January 30** | Inventory list (if applicable) | N/A | Nil filing if pure rental corporation | RMC 57-2015; NIRC Sec. 232 | N/A (rental corps may file nil) |
| **January 31** | Q4 1601-EQ + QAP | 1601-EQ | Quarterly EWT for Oct–Dec | RR 2-98 | P14 (Expense Tracking) |
| **January 31** | LIS (2nd semester) | Per RR 12-2011 | Lessee Information Statement (Jul–Dec) | RR 12-2011 | P11 (Rent Roll) |
| **March 1** | Annual EWT Information Return | 1604-E + Alphalist | Full-year summary of all EWT withheld on suppliers, in DAT format | NIRC Sec. 58; RR 2-98 | P14 (Expense Tracking) |
| **April 15** | Annual Corporate ITR | 1702-RT | Full-year income tax return + AFS + SAWT + all 2307s | NIRC Sec. 77 | P12 (Tax Data, full year) |

### SEC Annual Filings

| Deadline | Filing | Description | Legal Basis | Data Source |
|----------|--------|-------------|-------------|-------------|
| **30 days after ASM** | GIS | General Information Sheet (stockholders, directors, officers, beneficial owners) — filed via SEC eFAST | RA 11232 Sec. 177; SEC MC 01-2025 | Corporate records, board resolutions |
| **120 days after FY-end (April 30 for calendar-year corps)** | AFS | Audited Financial Statements — filed via SEC eFAST, must be BIR-stamped. Audit mandatory if assets/liabilities ≥ PHP 600K | SEC Rules; NIRC Sec. 232 | All processes → CPA auditor |

**Note on ASM timing:** Most small/mid-size corporations hold their ASM in Q2 (April–June). GIS is due 30 days after. If ASM is April 15, GIS deadline is May 15. The corporation should schedule the ASM early to avoid GIS and AFS deadlines colliding.

### BIR Special Annual Deadlines (Abolished / Changed)

| Former Deadline | Status | Legal Basis |
|-----------------|--------|-------------|
| ~~January 31: BIR Annual Registration Fee (Form 0605, PHP 500)~~ | **ABOLISHED** effective January 22, 2024 | RA 11976 (EOPT Act); RMC 14-2024 |
| ~~ATP renewal (5-year validity)~~ | **Receipts/invoices no longer expire** per RR 6-2022. ATP document itself still carries 5-year validity. | RR 6-2022; RMC 123-2022 |

---

## 6. Per-Event Deadlines (Non-Calendar)

### BIR Per-Event Filings

| Trigger | Filing | Form | Deadline | Legal Basis | Data Source |
|---------|--------|------|----------|-------------|-------------|
| Lease contract executed or renewed | DST Declaration | 2000 | Within **5 days after close of month** of execution | NIRC Sec. 194, 200 | P8 (Lease Contract Gen), P9 (Renewal) |
| ATP serial range exhausted | New ATP application | 1906 | Before issuing next receipt/invoice — apply via e-ATP portal or ORUS | NIRC Sec. 237; RR 18-2012 | P13 (Official Receipt Data) |
| VAT threshold crossed (PHP 3M in any 12-month period) | VAT registration | 1905 | Within **30 days** from close of month threshold exceeded | NIRC Sec. 236(G) | Revenue monitoring |

---

## 7. LGU Deadlines (Las Piñas City)

**Critical note:** Per-property permits are required. A corporation with 3–10 properties in different barangays needs separate barangay clearances and may need separate business permits per location (if the BPLO treats each property as a separate business establishment).

### Annual LGU Renewal Calendar

| Deadline | Permit/Filing | Issuing Agency | Prerequisite For | Legal Basis |
|----------|--------------|----------------|------------------|-------------|
| **December (prior year)** | Begin gathering renewal documents | — | — | — |
| **December 1–15** | RPT advance payment (highest discount ~20%) | City Treasurer | — | RA 7160 Sec. 250–251 |
| **December 16–31** | RPT advance payment (mid discount ~16%) | City Treasurer | — | RA 7160 Sec. 250–251 |
| **Early January** | Barangay Business Clearance renewal | Punong Barangay | Business Permit | RA 7160 Sec. 152, 389(b)(9) |
| **Early January** | Fire Safety Inspection Certificate (FSIC) renewal | Bureau of Fire Protection (BFP) | Business Permit | RA 9514 Sec. 5(g), 7(a) |
| **Early January** | Sanitary Permit renewal | City Health Office | Business Permit | PD 856 Sec. 14 |
| **By January 20** | Business Permit / Mayor's Permit renewal (full payment or Q1 installment) | Business Permits and Licensing Office (BPLO) | Legal operation | RA 7160 Sec. 143–153 |
| **January 31** | RPT lump-sum payment (with ~10% discount) | City Treasurer | — | RA 7160 Sec. 250 |

### RPT Quarterly Installment Schedule

| Installment | Deadline | Legal Basis |
|-------------|----------|-------------|
| Q1 | **March 31** | RA 7160 Sec. 250 |
| Q2 | **June 30** | RA 7160 Sec. 250 |
| Q3 | **September 30** | RA 7160 Sec. 250 |
| Q4 | **December 31** | RA 7160 Sec. 250 |

### Business Permit Quarterly Installments (if not paid in full)

| Installment | Deadline |
|-------------|----------|
| Q1 | January 20 |
| Q2 | April 20 |
| Q3 | July 20 |
| Q4 | October 20 |

### LGU Penalty Rates

| Violation | Penalty | Cap | Legal Basis |
|-----------|---------|-----|-------------|
| Late RPT payment | 2% per month on unpaid amount | 36 months (72% max) | RA 7160 Sec. 255 |
| Late business permit renewal | 25% surcharge + 2%/month interest | 36 months | RA 7160 Sec. 168 |
| Operating without FSIC | Monetary fines + suspension/closure | Criminal liability if fire incident | RA 9514 |
| Operating without sanitary permit | PHP 1,000–5,000 per violation | Closure for repeat violations | PD 856 |

### Business Permit Required Documents

A complete renewal package for a SEC-registered rental corporation:

1. Previous year's Business Permit
2. SEC Certificate of Registration
3. Barangay Business Clearance (obtained first)
4. Community Tax Certificate (CTC / Cedula)
5. Audited Financial Statements
6. BIR Certificate of Registration (Form 2303)
7. Fire Safety Inspection Certificate (FSIC)
8. Sanitary Permit
9. Zoning / Locational Clearance
10. Latest Income Tax Return (ITR) or Sworn Declaration of Gross Receipts

---

## 8. EIS Compliance Deadline (One-Time Transition)

| Deadline | Obligation | Legal Basis | Applicability |
|----------|-----------|-------------|---------------|
| **December 31, 2026** | Electronic Invoicing System (EIS) compliance | RR 11-2025; RR 26-2025; RA 12066 (CREATE MORE Act) | Covered if using CAS with invoicing software. Structured JSON + JWS format. Transmit to BIR within 3 calendar days of transaction. |

**Assessment for this corporation:** If the automated system generates invoices via a CAS, EIS compliance will be triggered. The system should be designed with EIS-ready structured invoice output from the start.

---

## 9. Complete Annual Calendar (Month-by-Month)

### January

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 1–10 | Barangay clearance + FSIC + Sanitary permit renewals | LGU | 30 days |
| 10/15 | 0619-E (December EWT — but Dec is Q4 end, covered by 1601-EQ) | BIR | N/A |
| 15 | Loose-leaf books bound + registered via ORUS | BIR | 30 days |
| 20 | Business Permit renewal (or Q1 installment) | LGU | 60 days |
| 20 | 2307 certificates from corporate tenants (Q4) due | External | 15 days |
| 25 | 2550Q (Q4 Oct–Dec) + SLSP | BIR | 10 days |
| 30 | CAS soft copy submission | BIR | 15 days |
| 30 | Inventory list (nil filing if pure rental) | BIR | 15 days |
| 31 | 1601-EQ + QAP (Q4 Oct–Dec) | BIR | 10 days |
| 31 | LIS (2nd semester Jul–Dec) | BIR | 15 days |
| 31 | RPT lump-sum (with discount) | LGU | 30 days |

### February

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 10/15 | 0619-E (January EWT) | BIR | 5 days |

### March

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 1 | 1604-E + Alphalist (Annual EWT Information Return) | BIR | 30 days |
| 10/15 | 0619-E (February EWT) | BIR | 5 days |
| 31 | RPT Q1 installment | LGU | 15 days |

### April

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 15 | 1702-RT (Annual ITR) + AFS (BIR-stamped copy) | BIR | 60 days |
| 20 | 2307 certificates from corporate tenants (Q1) due | External | 15 days |
| 20 | Business Permit Q2 installment (if quarterly) | LGU | 10 days |
| 25 | 2550Q (Q1 Jan–Mar) + SLSP | BIR | 10 days |
| 30 | 1601-EQ + QAP (Q1 Jan–Mar) | BIR | 10 days |
| 30 | SEC AFS (120 days after Dec 31 FY-end) | SEC | 60 days |

### May

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 10/15 | 0619-E (April EWT) | BIR | 5 days |
| ~15 | SEC GIS (if ASM held mid-April; 30 days after ASM) | SEC | 15 days |
| 30 | 1702Q (Q1 Jan–Mar) + SAWT | BIR | 15 days |

### June

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 10/15 | 0619-E (May EWT) | BIR | 5 days |
| 30 | RPT Q2 installment | LGU | 15 days |

### July

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 20 | 2307 certificates from corporate tenants (Q2) due | External | 15 days |
| 20 | Business Permit Q3 installment (if quarterly) | LGU | 10 days |
| 25 | 2550Q (Q2 Apr–Jun) + SLSP | BIR | 10 days |
| 31 | 1601-EQ + QAP (Q2 Apr–Jun) | BIR | 10 days |
| 31 | LIS (1st semester Jan–Jun) | BIR | 15 days |

### August

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 10/15 | 0619-E (July EWT) | BIR | 5 days |
| 29 | 1702Q (Q2 Apr–Jun) + SAWT | BIR | 15 days |

### September

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 10/15 | 0619-E (August EWT) | BIR | 5 days |
| 30 | RPT Q3 installment | LGU | 15 days |

### October

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 20 | 2307 certificates from corporate tenants (Q3) due | External | 15 days |
| 20 | Business Permit Q4 installment (if quarterly) | LGU | 10 days |
| 25 | 2550Q (Q3 Jul–Sep) + SLSP | BIR | 10 days |
| 31 | 1601-EQ + QAP (Q3 Jul–Sep) | BIR | 10 days |

### November

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 10/15 | 0619-E (October EWT) | BIR | 5 days |
| 29 | 1702Q (Q3 Jul–Sep) + SAWT | BIR | 15 days |
| Late Nov | Begin preparing January renewal documents (permits, FSIC, sanitary) | LGU | 60 days |

### December

| Day | Obligation | Category | Alert Lead |
|-----|-----------|----------|-----------|
| 1–15 | RPT advance payment for next year (maximum discount ~20%) | LGU | Announced Nov |
| 10/15 | 0619-E (November EWT) | BIR | 5 days |
| 16–31 | RPT advance payment for next year (mid discount ~16%) | LGU | — |
| 31 | RPT Q4 installment (current year) | LGU | 15 days |
| 31 | EIS compliance deadline (one-time, 2026 only) | BIR | 90 days |

### Ad Hoc (Any Month)

| Trigger | Deadline | Filing | Category |
|---------|----------|--------|----------|
| Lease contract executed/renewed | 5 days after month-end of execution | Form 2000 (DST) | BIR |
| ATP serial range exhausted | Before next issuance | Form 1906 (new ATP) | BIR |
| VAT threshold crossed | 30 days from month-end of crossing | Form 1905 (VAT registration) | BIR |
| Building renovation started | Before construction | Building Permit (OBO) | LGU |
| New signage installed | Before installation | Signboard Permit (OBO) | LGU |

---

## 10. Alert System Specification

### Alert Levels

| Level | Lead Time | Color | Action |
|-------|-----------|-------|--------|
| **ADVANCE** | 60–90 days before | Blue | Begin preparation (gather documents, compile data) |
| **WARNING** | 15–30 days before | Yellow | Data package must be ready; accountant notified |
| **URGENT** | 5–10 days before | Orange | Filing must be submitted; escalate if data not ready |
| **OVERDUE** | Past deadline | Red | Penalty accruing; immediate action required |

### Alert Configuration by Filing Type

| Filing Type | ADVANCE | WARNING | URGENT | Penalty Rate |
|------------|---------|---------|--------|-------------|
| BIR quarterly (2550Q, 1601-EQ) | 30 days | 10 days | 3 days | 25% surcharge + 12%/year interest |
| BIR quarterly (1702Q) | 30 days | 15 days | 5 days | 25% surcharge + 12%/year interest |
| BIR annual (1702-RT, 1604-E) | 60 days | 30 days | 10 days | 25% surcharge + 12%/year interest + compromise |
| SEC GIS | 15 days after ASM | 20 days after ASM | 25 days after ASM | PHP 500/day (late filing) |
| SEC AFS | 60 days | 30 days | 10 days | PHP 500/day + possible suspension |
| LGU business permit | 60 days (Nov) | 30 days (Dec) | 10 days (Jan 10) | 25% surcharge + 2%/month |
| LGU RPT | 30 days | 15 days | 5 days | 2%/month (max 72%) |
| DST (Form 2000) | At lease execution | 3 days before month-end | Day of month-end | 25% surcharge + 12%/year interest |
| LIS | 15 days | 7 days | 3 days | PHP 1,000 per failure |
| SLSP | 15 days | 7 days | 3 days | PHP 1,000 per failure |

### Per-Property Alert Multiplier

For a corporation with N properties:
- RPT alerts fire N times (once per property)
- Business permit alerts fire per establishment (may be < N if consolidated under one BPLO registration)
- Barangay clearance alerts fire per barangay (may be < N if multiple properties in same barangay)
- FSIC and sanitary permit alerts fire per property

---

## 11. Compliance Dependencies (Prerequisite Chain)

Some filings are prerequisites for others. Missing an upstream filing blocks downstream compliance:

```
Barangay Business Clearance ──┐
Fire Safety Inspection Cert ──┤──► Business Permit / Mayor's Permit
Sanitary Permit ──────────────┤
Zoning Clearance ─────────────┘

Business Permit ──────────────────► Legal operation (all year)

Monthly 0619-E (×8/year) ────────► Quarterly 1601-EQ (×4)
Quarterly 1601-EQ (×4) ──────────► Annual 1604-E (×1)

Quarterly 2550Q + SLSP ──────────► Annual 1702-RT (VAT data)
Quarterly 1702Q + SAWT ──────────► Annual 1702-RT (income + credits)
All 2307s received ───────────────► SAWT ──► 1702Q/1702-RT tax credits

Rent Roll (monthly) ─────────────► 2550Q data + 1702Q data + LIS data + AFS data
Expense Voucher Package ──────────► 1601-EQ data + 1702Q deductions + AFS expenses

AFS (audited by CPA) ────────────► SEC AFS filing
                      ────────────► BIR 1702-RT attachment
```

---

## 12. Lightweight Feature Spec — Compliance Calendar Module

### Data Model

```
ComplianceObligation
├── id: UUID
├── name: str                      -- e.g., "2550Q Q1 2026"
├── category: enum                 -- BIR_MONTHLY | BIR_QUARTERLY | BIR_ANNUAL | BIR_SEMI_ANNUAL |
│                                     BIR_PER_EVENT | SEC | LGU_ANNUAL | LGU_QUARTERLY
├── form_number: str?              -- "2550Q", "1601-EQ", "GIS", etc.
├── legal_basis: str               -- "NIRC Sec. 114; RR 16-2005"
├── frequency: enum                -- MONTHLY | QUARTERLY | SEMI_ANNUAL | ANNUAL | PER_EVENT
├── property_id: FK?               -- NULL for corp-level filings; FK for per-property (RPT, FSIC, etc.)
├── period_start: date?            -- Start of covered period
├── period_end: date?              -- End of covered period
├── deadline: date                 -- Filing/payment due date
├── alert_advance_days: int        -- ADVANCE alert lead time
├── alert_warning_days: int        -- WARNING alert lead time
├── alert_urgent_days: int         -- URGENT alert lead time
├── prerequisite_ids: [UUID]       -- Filing IDs that must be completed first
├── data_source_processes: [str]   -- Which Wave 2 processes generate the data
├── status: enum                   -- UPCOMING | IN_PROGRESS | FILED | OVERDUE | NOT_APPLICABLE
├── filed_date: date?
├── filed_by: str?
├── confirmation_number: str?      -- BIR/SEC confirmation/reference number
├── penalty_accrued: Decimal?
├── notes: str?
└── created_at / updated_at

ComplianceTemplate
├── id: UUID
├── name: str                      -- "Quarterly VAT Return"
├── form_number: str               -- "2550Q"
├── category: enum
├── frequency: enum
├── legal_basis: str
├── deadline_rule: str             -- "25th of month after quarter-end"
├── alert_advance_days: int
├── alert_warning_days: int
├── alert_urgent_days: int
├── per_property: bool             -- True for RPT, FSIC, business permit
├── prerequisite_template_ids: [UUID]
├── data_source_processes: [str]
└── active: bool

ComplianceCalendarGeneration (service logic)
├── generate_year(year: int) → [ComplianceObligation]
│   -- From templates, expand all obligations for a fiscal year
│   -- Per-property templates generate N obligations (one per property)
│   -- Per-event templates (DST) are created ad hoc
├── check_overdue() → [ComplianceObligation]
│   -- Return all obligations past deadline with status != FILED
├── get_upcoming(days: int) → [ComplianceObligation]
│   -- Return obligations due within N days
└── get_blocked() → [ComplianceObligation]
    -- Return obligations whose prerequisites are not yet FILED
```

### Dashboard Views

1. **Calendar view** — month-by-month grid showing all deadlines, color-coded by alert level
2. **List view** — sortable table of upcoming obligations with status, deadline, days remaining
3. **Overdue view** — red-flagged items past deadline with penalty computation
4. **Per-property view** — filter by property for LGU-specific deadlines
5. **Prerequisite view** — show blocked filings (can't file X until Y is done)

### Alert Delivery

- **Dashboard badge** — count of URGENT + OVERDUE items
- **Email digest** — weekly summary of upcoming deadlines (configurable: owner, accountant, or both)
- **Lease event trigger** — new lease execution → auto-create DST obligation with 5-day deadline

### Automability: 5/5

The compliance calendar is purely deterministic:
- All deadlines are known in advance (calculated from fiscal year, quarter-end dates, and ASM date)
- Per-event deadlines (DST) are triggered by lease execution events already tracked in P8/P9
- Alert rules are fixed mathematical lead times
- Status tracking is CRUD on a single table
- No human judgment required (the deadlines are the law)

**Only human actions:** Actually performing the filing, obtaining confirmation numbers, and entering the filed date.

---

## 13. Cross-Process Integration

The compliance calendar module integrates with other Wave 2 processes:

| Process | Integration Point |
|---------|-------------------|
| P5 (Monthly Billing) | Billing run triggers data readiness check for monthly 0619-E |
| P8 (Lease Contract Gen) | New lease execution creates a DST obligation (Form 2000) |
| P9 (Lease Renewal) | Renewal/extension creates a DST obligation |
| P11 (Rent Roll) | Rent roll completion triggers "data ready" status for 2550Q, 1702Q, LIS |
| P12 (Tax Data Compilation) | Tax data compilation marks quarterly filings as "data ready" |
| P14 (Expense Tracking) | Expense package completion triggers "data ready" for 1601-EQ, 1604-E |

---

## 14. Key Findings

1. **January is the most deadline-dense month** — 11+ obligations clustering: Q4 BIR filings, LGU permit renewals (business permit, barangay, FSIC, sanitary), books of accounts, LIS, RPT. The corporation should begin preparation in November.

2. **~43 recurring compliance deadlines per year** (BIR ~30, LGU ~8 per property, SEC ~2, semi-annual LIS ×2, SLSP ×4). Per-property LGU deadlines multiply: a 5-property corporation faces ~70+ deadlines/year.

3. **Filing chains create cascade risk** — missing the barangay clearance blocks the business permit; missing monthly 0619-E corrupts quarterly 1601-EQ; missing quarterly 1702Q data (from rent roll) blocks annual 1702-RT. The alert system must track prerequisites.

4. **BIR Annual Registration Fee (Form 0605) is abolished** — per RA 11976 (EOPT Act), effective January 22, 2024. No longer a compliance obligation.

5. **SLSP is a separate quarterly obligation** not covered in earlier Wave 2 analyses — VAT-registered corporations must file Summary List of Sales/Purchases alongside 2550Q. This adds 4 deadlines/year and requires structured sales/purchase data extraction from P5 (billing) and P14 (expenses).

6. **EIS compliance (December 31, 2026)** is a one-time transition deadline but has significant system design implications — structured JSON invoices with JWS signatures must be transmitted to BIR within 3 calendar days. Any automated invoicing system should be EIS-ready from inception.

7. **RPT early payment discounts (up to 20%)** represent meaningful savings for a multi-property portfolio. The system should alert in November when Las Piñas announces the discount schedule.

8. **2307 receipt tracking has a tight window** — corporate tenants must issue within 20 days of quarter-end; the property manager must log, reconcile, and deliver to accountant in time for the SAWT attachment to 1702Q (60 days after quarter-end). Late or missing 2307s = lost tax credits.

---

## 15. Verification Status

| Rule | Sources Checked | Status |
|------|-----------------|--------|
| BIR quarterly filing deadlines | NIRC, RR 16-2005, RR 2-98, corporate-rental-tax.md, accounting-agency-handoff.md | **Confirmed** |
| 1702Q deadline = 60 days after Q-end | NIRC Sec. 77, corrected in tax-data-compilation.md | **Confirmed** (correction from earlier "25th" claim) |
| LIS semi-annual deadlines | RR 12-2011, RMC 69-2009, accounting-agency-handoff.md | **Confirmed** |
| RPT penalty rate 2%/month, max 72% | RA 7160 Sec. 255, Lamudi, Manila Bulletin | **Confirmed** |
| Business permit deadline Jan 20 | RA 7160 Sec. 143-153, Aureada Law, FilePino | **Confirmed** |
| FSIC required before business permit | RA 9514 Sec. 5(g), BFP Citizen's Charter | **Confirmed** |
| BIR ARF abolished | RA 11976, RMC 14-2024, Alas Oplas, Grant Thornton | **Confirmed** |
| SLSP quarterly (for VAT-registered) | RR 1-2012, taxacctgcenter.ph, Juan Tax | **Confirmed** |
| EIS deadline Dec 31, 2026 | RR 26-2025, KPMG, PNA, Aureada Law | **Confirmed** |
| Loose-leaf books deadline Jan 15 | RMC 3-2023, CloudCFO, Aureada Law | **Confirmed** |
| CAS soft copy Jan 30 | RMC 3-2023, MPM | **Confirmed** |
| ATP no longer expires (receipts) | RR 6-2022, RMC 123-2022, PwC, Grant Thornton | **Confirmed** (ATP document itself still has 5-year validity) |
| RPT Las Piñas early discount ~10-20% | Manila Bulletin, Manila Times, Philstar (2024 articles) | **Confirmed** (2026 schedule TBD) |

**Discovery:** SLSP obligation not previously tracked in any Wave 2 analysis. Added to compliance calendar. This is a quarterly data extraction requirement (sales + purchases) that the automated system must support.

---

## Key Legal Citations

| Citation | Subject |
|----------|---------|
| NIRC Sec. 57, 58 | EWT obligations (withholding agent) |
| NIRC Sec. 77 | Quarterly/annual income tax return |
| NIRC Sec. 114 | Quarterly VAT return |
| NIRC Sec. 194, 200 | DST on leases |
| NIRC Sec. 232 | Books of accounts |
| NIRC Sec. 237 | Invoice/receipt requirements, ATP |
| RA 7160 Sec. 143–153, 168 | LGU business permit and taxes |
| RA 7160 Sec. 232–283 (esp. 246, 250, 255) | Real property tax |
| RA 9514 Sec. 5(g), 7(a) | Fire Safety Inspection Certificate |
| RA 11232 Sec. 177 | SEC GIS filing |
| RA 11976 (EOPT Act) | Abolished ARF; invoice reform |
| RA 12066 (CREATE MORE Act) | EIS mandate |
| PD 856 Sec. 14 | Sanitary permit |
| RR 1-2012 | SLSP (Summary List of Sales/Purchases) |
| RR 2-98 | EWT administration |
| RR 6-2022 | ATP validity (receipts no longer expire) |
| RR 12-2011 | Lessee Information Statement (LIS) |
| RR 16-2005 | VAT regulations |
| RR 11-2025 | EIS rules |
| RR 26-2025 | EIS deadline extension to Dec 31, 2026 |
| RMC 3-2023 | ORUS-based book registration |
| RMC 14-2024 | ARF abolition implementation |
| RMC 57-2015 | Inventory list submission |
| RMC 123-2022 | ATP clarifications |
