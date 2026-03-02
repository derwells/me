# Back-Office Process Catalog — TSVJ Rental Corporation

*Compiled: 2026-02-27 | Source: 14 process analyses (Wave 2), 3 integration analyses (Wave 3)*
*Target: SEC-registered Las Piñas rental corporation, ~3-10 properties, ~20-100 units, mixed commercial + residential (rent-controlled)*

---

## How to Use This Catalog

Each process entry contains:
- **Description** — what the process does, when, and who currently does it
- **Current method** — how it's done today (manual, spreadsheet, Crispina, outsourced)
- **Regulatory rules** — PH laws governing this process (with legal citations)
- **Automability** — score 1-5 (1 = human judgment required, 5 = purely deterministic)
- **Crispina status** — what the discontinued codebase already built (if anything)
- **Feature spec summary** — key data model entities, core logic, edge cases

**Blank columns for owner scoring** appear in the summary table (Section 1). Pain and frequency are intentionally left empty — the business owner fills these based on operational experience.

---

## 1. Process Registry

| ID | Process | Category | Automability | Pain (1-5) | Frequency | Owner Notes |
|----|---------|----------|:------------:|:----------:|:---------:|-------------|
| **F0** | **Lease & Tenant Master** | Foundation | — | | | Base data all processes depend on |
| P1 | Rent Escalation Calculation | Billing | 4/5 | | | |
| P2 | Water Billing | Billing | 4/5 | | | |
| P3 | Electric Billing | Billing | 4/5 | | | |
| P4 | Late Payment Penalties | Billing | 4/5 | | | |
| P5 | Monthly Billing Generation | Billing | 5/5 | | | |
| P6 | Tenant Payment Tracking | Collection | 4/5 | | | |
| P7 | Security Deposit Lifecycle | Collection | 3/5 | | | |
| P8 | Lease Contract Generation | Contracts | 4/5 | | | |
| P9 | Lease Renewal & Extension | Contracts | 4/5 | | | |
| P10 | Lease Status Visibility | Monitoring | 5/5 | | | |
| P11 | Rent Roll Preparation | Handoff | 5/5 | | | |
| P12 | Tax Data Compilation | Handoff | 4/5 | | | |
| P13 | Official Receipt / Invoice Data | Handoff | 4/5 | | | |
| P14 | Expense Tracking | Handoff | 4/5 | | | |

---

## 2. Foundation: Lease & Tenant Master (F0)

Every process in this catalog depends on a shared set of master data entities. These do not constitute a "process" but are the prerequisite data layer.

**Core entities:** Lease, Tenant, Property, Room, Rentable

**Key fields required across processes (not in Crispina today):**

| Entity | Missing Field | Needed By |
|--------|--------------|-----------|
| Tenant | `tin` (BIR TIN) | P11, P12, P13 |
| Tenant | `is_corporate` | P4, P6, P12, P13 |
| Tenant | `is_vat_registered` | P5, P13 |
| Rentable | `unit_type` (residential/commercial) | P1, P2, P4, P5 |
| Rentable | `floor_area_sqm` | P2, P3 |
| Lease | `status` (active/expired/month_to_month/terminated) | P5, P9, P10 |
| Lease | `escalation_type` + `escalation_params` | P1 |
| Lease | `lease_regime` (controlled/commercial) | P1, P4, P7 |

---

## 3. Billing Processes

### P1 — Rent Escalation Calculation

**Description:** Compute annual rent increases at each lease anniversary. Two regimes: residential controlled (NHSB cap) and commercial (contractual rate).

**Current method:** Manual — property manager tracks anniversary dates in spreadsheet, looks up applicable cap, updates billing amount. No audit trail.

**Regulatory rules:**
- *Residential controlled:* RA 9653 Sec. 4 — max once per 12 months; NHSB Resolution 2024-01 — 2.3% cap (2025), 1% cap (2026). Applied to current rent (compounding). Vacancy decontrol: new tenant = free pricing (RA 9653 Sec. 4).
- *Commercial:* No statutory cap (RA 9653 Sec. 11 excludes commercial). Freedom of contract (Civil Code Art. 1305). Common patterns: fixed %, stepped, CPI-linked.
- *Threshold crossing:* If controlled rent exceeds PHP 10,000/month via lawful increase, unit exits rent control.

**Automability: 4/5** — Core computation is deterministic. Deducted for: manual NHSB rate entry (annual), vacancy decontrol pricing (human judgment), CPI data entry (external data).

**Crispina status:**
- Built: Pre-computed escalation via `RecurringCharge` → `RecurringChargePeriod`; compound interest formula (`math.py`); lease-anniversary date splitting (`date.py`); ROUND_DOWN; VAT rate frozen at charge-time.
- Gaps: No rent-control flag; single fixed rate per lease (no stepped/CPI/NHSB lookup); no NHSB cap enforcement; no threshold crossing detection; no escalation event log.

**Feature spec summary:**
- New entities: `NHSBCapRate` (year, rate, resolution#), `EscalationEvent` (audit log per escalation)
- Enhanced: `Lease` + `escalation_type` (ENUM: nhsb_cap, fixed_pct, stepped, cpi_linked, none) + `escalation_params` (JSONB)
- Enhanced: `Rentable` + `unit_type` + `is_rent_controlled` (derived)
- Core logic: Look up rate by type → `new_rent = current_rent × (1 + rate)` → ROUND_DOWN → threshold check → create new `RecurringChargePeriod` + audit event
- Edge cases: Mid-year NHSB change, tacit reconduction (escalation continues at anniversary), multiple rentables under one lease, contractual rate below NHSB cap, retroactive escalation for missed anniversaries

*Full analysis: `analysis/rent-escalation-calculation.md`*

---

### P2 — Water Billing

**Description:** Convert monthly Maynilad master meter bill + sub-meter readings into per-tenant water charges. Per-tier billing (each tenant starts at lowest bracket). Common area water allocated as separate line item.

**Current method:** Standalone Crispina water calculator (`water/` directory) — readings hardcoded in `seed.py`, uses prohibited blended-rate method. 33 sub-meters, 2 common area (CR-1, CR-2). Common area water (43% of building total) blended into tenant bills.

**Regulatory rules:**
- *No-markup:* Strict pass-through — landlord cannot charge above actual Maynilad cost (MWSS Charter RA 6234; RA 7581 Price Act — criminal penalties PHP 5K-2M).
- *Per-tier billing mandatory:* MWSS IRR No. 2008-02 — each tenant's consumption starts at lowest tier. Blended rate method is PROHIBITED. MWSS RO ordered PHP 87M+ in refunds (2021-2024).
- *Common area:* Must be separate line item (not blended into per-cu.m. rate). Allocated by floor area or equal split.
- *Bill components:* Basic Charge (per-tier), Environmental Charge (25% of Basic, 2025+), Sewerage Charge (20% of Basic, commercial only), FCDA (quarterly adjustment), MSC, VAT.
- *Statement requirements:* Initial/final readings, per-tier breakdown, Maynilad bill copy within 5 days, 3-year record retention.
- *VAT:* Water pass-through is NOT VATable (landlord as conduit, BIR RR 16-2005).

**Automability: 4/5** — Per-tier computation, surcharges, allocation, reconciliation are deterministic. Deducted for: physical meter reading, defective meter decisions, anomaly resolution, quarterly rate updates.

**Crispina status:**
- Built (standalone): Meter model with co-tenancy, delta-based consumption, ChargeRow CSV export, frozen Pydantic models.
- Gaps: Uses prohibited blended rate; no Maynilad tier rate tables; no tenant type classification; no common area separation; no environmental/sewerage breakdown; no FCDA; no reconciliation check; no DB integration; no meter status tracking.

**Feature spec summary:**
- New entities: `WaterMeter`, `WaterMeterTenant` (junction), `WaterMeterReading`, `MayniladBill`, `MayniladRateSchedule` (JSONB tiers), `WaterBillingRun`, `WaterCharge`
- Core logic: Per-tier rate computation (tenant starts at tier 1) → surcharges → common area allocation (by floor area or equal split) → reconciliation check (total billed ≤ Maynilad master bill)
- Edge cases: Shared meters (4 co-tenancy situations), defective meters (estimated billing), negative readings (rollover), vacant units (landlord cost), lifeline rate inapplicability, Maynilad rate changes (quarterly FCDA)

*Full analysis: `analysis/water-billing.md`*

---

### P3 — Electric Billing

**Description:** Apportion monthly Meralco master meter bill across tenants using sub-meter readings and blended rate (total bill / total kWh). Common area electricity allocated separately.

**Current method:** Fully manual spreadsheet. No Crispina code exists for electric billing (zero search results for electric/meralco/kwh).

**Regulatory rules:**
- *No-markup:* Strict pass-through at actual per-kWh cost (EPIRA RA 9136 Sec. 43; ERC Res. 12/2009).
- *Blended rate accepted:* Unlike water, the blended formula (total bill / total kWh × tenant kWh) IS the standard method for electricity.
- *Admin fees:* Permitted if contractual, reasonable, and transparent. No published cap; informal ERC reference ~PHP 1.00-1.50/kWh. Must be separate line item.
- *Common area:* Separate line item or absorbed by landlord. Cannot embed as per-kWh markup.
- *VAT:* CONFLICTING — at-cost pass-throughs may be excludable from VAT per EOPT Act (RA 11976) and CIR v. Tours Specialists; but earlier BIR RRs treated as part of gross receipts. Flag for accountant decision.

**Automability: 4/5** — Blended-rate computation is simpler than water's per-tier method. Deducted for: physical meter reading, defective meters, admin fee configuration, VAT treatment decision, common area allocation method choice.

**Crispina status:**
- Built: Nothing — entirely greenfield.
- Relevant existing: `ChargeType` model (extensible), `Charge` model (base_amount + vat_rate), `Transaction` (billing batch), `Rentable` (needs floor_area_sqm).

**Feature spec summary:**
- New entities: `ElectricMeter`, `ElectricMeterTenant`, `ElectricMeterReading`, `MeralcoBill` (with component breakdown), `ElectricBillingRun`, `ElectricCharge`
- Core logic: `effective_rate = total_bill / total_kwh` → `tenant_charge = consumption × effective_rate` → common area allocation → reconciliation check
- Edge cases: Mixed-use master meter classification (commercial vs. residential), Meralco rate fluctuations (monthly), shared meters, admin fee design, power outage adjustments

*Full analysis: `analysis/electric-billing.md`*

---

### P4 — Late Payment Penalties

**Description:** Compute penalty charges on overdue rent. Two regimes: residential controlled (safe harbour: 1%/month, max 1 month's rent/year) and commercial (contractual, subject to Art. 1229 unconscionability review).

**Current method:** Manual — property manager reviews payment records, identifies overdue tenants, computes penalty amount. No cap enforcement, no audit trail.

**Regulatory rules:**
- *Residential controlled:* RA 9653 Sec. 7 (5-day payment window); Civil Code Art. 2209 (legal interest = 6% p.a. per BSP Circular 799 if no contractual rate); Art. 1229 (unconscionable penalties reducible). Safe harbour: ≤1%/month, total ≤1 month's rent/year, simple interest only.
- *Commercial:* Freedom of contract (Art. 1305). No statutory cap (Usury Law ceilings suspended by CB Circular 905). Common range: 2-3%/month. Rates >3%/month face judicial scrutiny; >5%/month almost certainly struck down (Medel v. CA, Solangon v. Salazar).
- *Compounding:* Art. 2212 — interest on interest only from judicial demand. System should not auto-compound pre-demand.
- *Demand requirement:* Legal interest (6% p.a.) runs only from date of extrajudicial/judicial demand, not automatically.
- *3-month arrears:* RA 9653 Sec. 9(b) — cumulative 3 months unpaid = ejectment ground for controlled units.
- *Tax:* Penalty income is gross receipts — 12% VAT (if VAT-registered), 5% EWT, subject to RCIT.

**Automability: 4/5** — Computation is formulaic once rates/caps are configured. Deducted for: unconscionability determination (human judgment), demand letter decision, safe harbour caps are advisory (not statutory), arrears classification for partial payments.

**Crispina status:**
- Built: Nothing — no penalty charge type, no penalty rate on Lease, no grace period field, no demand tracking.
- Relevant existing: `calculate_compound_interest()` (designed for escalation, not penalties), `Charge`/`ChargeType` models (extensible).

**Feature spec summary:**
- New entities: `PenaltyLedger` (audit trail per penalty computation), `DemandRecord` (date sent, method, arrears at demand)
- Enhanced: `Lease` + `penalty_rate_monthly` + `grace_period_days` + `is_rent_controlled`; new `ChargeType`: "Late Payment Penalty"
- Core logic: Determine rate (contractual or legal interest) → compute raw penalty → apply caps for controlled (1%/month, 1 month's rent/year) → check demand requirement → create Charge + PenaltyLedger
- Edge cases: No contractual rate + no demand = no penalty; partial payment reduces base (Art. 1229); penalty on penalties requires demand (Art. 2212); vacancy decontrol shifts regime

*Full analysis: `analysis/late-payment-penalties.md`*

---

### P5 — Monthly Billing Generation

**Description:** Generate monthly billing statements (VAT Sales Invoices under RR 7-2024) for all active tenants. Aggregates: rent + water + electric + penalties + other recurring charges. Produces per-tenant invoice document with line items, VAT breakdown, prior balance, and total due.

**Current method:** Manual — property manager looks up each tenant's rate, adds utility charges, prints statements. No invoice numbering, no digital delivery, no automated generation.

**Regulatory rules:**
- *Invoice at accrual:* RR 7-2024 (EOPT Act) — VAT Sales Invoice issued when rent becomes due (accrual), not at payment. Output VAT declared at invoice issuance.
- *VAT treatment:* Residential ≤ PHP 15,000/month = permanent VAT exemption (NIRC Sec. 109(1)(Q)). Commercial = 12% VAT if lessor exceeds PHP 3M aggregate.
- *Sequential numbering:* NIRC Sec. 237; RR 18-2012 — BIR-registered ATP, gapless sequential numbers per establishment.
- *Mandatory fields:* 13 required fields per RR 7-2024 (lessor TIN, invoice#, ATP#, tenant TIN, line-item amounts, VAT).
- *Default due date:* RA 9653 Sec. 7 — 5th of month for controlled units; per contract for commercial.
- *Uncollected receivables:* RR 3-2024 — if invoice not collected within credit term, output VAT deductible from next quarter's 2550Q (one-quarter claim window).
- *Credit memos:* Cannot void BIR invoice — must issue credit memo with own sequential series (RR 16-2005 Sec. 4.113-5).

**Automability: 5/5** — Purely deterministic given lease data, escalation periods, utility charges, and prior balance. No human judgment required — all inputs are structured, all formulas defined, output format specified by regulation.

**Crispina status:**
- Built: `RecurringCharge` + `RecurringChargePeriod` (pre-computed escalation); `Charge` model (base_amount + vat_rate); `Transaction` (billing batch); `ChargeType` with VAT config; multi-rentable lease (LeaseRentable M2M).
- Gaps: No invoice numbering; no billing statement template/generation; only 1 ChargeType seeded ("Rent"); no unit_type on Rentable; no batch billing endpoint; no credit memo model; no prior balance rollup; no advance rent tracking; no pro-ration logic.

**Feature spec summary:**
- New entities: `InvoiceSequence` (ATP-managed, atomic increment), `BillingRun` (batch/individual, draft/finalized), `CreditMemo`
- Enhanced: `Charge` + `invoice_number` + `invoice_date` + `is_vat_exempt`; `Lease` + `custom_due_day`
- Core logic: For each active lease → aggregate charges (rent from RecurringChargePeriod + utilities + penalties + other) → determine VAT rate per charge → assign sequential invoice number → render billing statement → record for VAT accrual
- Edge cases: Pro-rated first/last month, tacit reconduction (continue billing at same rate), multiple rentables per lease, billing before utility readings available (separate billing runs recommended), VAT status change mid-year, corporate tenant EWT, advance rent application in final month

*Full analysis: `analysis/monthly-billing-generation.md`*

---

## 4. Collection Processes

### P6 — Tenant Payment Tracking

**Description:** Record payments, allocate against outstanding charges following Civil Code hierarchy, maintain running balance per tenant, and provide dashboard visibility into payment status across all units.

**Current method:** Fully manual ledger/spreadsheet — monthly billings, payments received, running balance per tenant. No automated balance computation, no aging analysis, no dashboard.

**Regulatory rules:**
- *Payment allocation order:* Civil Code Art. 1252 (debtor designates), Art. 1253 (interest/penalties before principal — mandatory), Art. 1254 (most onerous first if no designation).
- *Arrears ejectment:* RA 9653 Sec. 9(b) — cumulative 3 months total unpaid = ejectment ground for controlled units. Partial payments do not automatically reset count; accepting without reservation risks waiver/estoppel.
- *Invoice/receipt:* RR 7-2024 — invoice at accrual (billing), receipt at payment. Both document numbers tracked per charge per payment.
- *EWT components:* Base rent = 5% EWT; utility pass-throughs at-cost = potentially 2% (reimbursement); penalties = 5% (additional rental). Per RR 02-98, RMC 11-2024.
- *Consignation:* RA 9653 Sec. 9(b) — if lessor refuses payment, lessee may deposit at court/city treasurer/barangay/bank. Resets arrears.
- *Prescription:* 10 years for written leases (Art. 1144); 6 years for oral (Art. 1145). Each monthly installment prescribes independently.

**Automability: 4/5** — Balance computation, allocation rules, aging analysis, and dashboard are deterministic. Deducted for: tenant payment designation (human intent), bounced check handling, partial payment waiver risk decision, consignation verification, corporate EWT matching.

**Crispina status:**
- Built: `Payment` (pk, amount, reference_number, date_issued, tenant_pk); `PaymentAllocation` (payment → transaction junction); partial payment support; `TransactionDetail` computes per-transaction balance.
- Gaps: No tenant-level balance rollup; no payment_method; no OR/invoice numbers; no deposited_date; no charge-level allocation; no penalty model; no is_corporate/tin on Tenant; no arrears alert; no payment remarks field.

**Feature spec summary:**
- Enhanced: `Tenant` + `tin` + `is_corporate` + `is_vat_registered`; `Payment` + `payment_method` + `or_number` + `deposited_date` + `remarks`; `PaymentAllocation` + `charge_pk` (charge-level granularity)
- New: `TenantBalance` (materialized view: total_billed, total_paid, balance, oldest_unpaid, months_in_arrears, arrears_alert); `PaymentEvent` (audit log)
- Core logic: Record payment → if tenant designates (Art. 1252), allocate to designated charges; else apply Art. 1253 (penalties first) then Art. 1254 (most onerous, then FIFO) → update TenantBalance → check arrears threshold
- Edge cases: Overpayment (credit balance = liability), corporate EWT partial payment, bounced check reversal, security deposit application, multiple charge types in one transaction, consigned payments, post-dated checks, advance rent recognition

*Full analysis: `analysis/tenant-payment-tracking.md`*

---

### P7 — Security Deposit Lifecycle

**Description:** Track deposits through collection, holding (with interest for controlled residential), deductions at lease end, and refund/forfeiture with tax reclassification.

**Current method:** Fully manual — Excel ledger, co-mingled bank accounts, handwritten deduction lists. Interest not tracked, tax reclassification missed, return deadline not monitored.

**Regulatory rules:**
- *Controlled residential (RA 9653 Sec. 7):* Max 2 months' rent deposit + 1 month advance. Bank-holding mandatory. ALL bank interest returned to lessee. Return within 1 month of lease expiry AND turnover. Violation: PHP 25K-50K fine + imprisonment for repeat.
- *Commercial (Civil Code Art. 1306):* No cap on deposit/advance. Bank-hold not mandated. Interest per contract only. Return: reasonable time (~30 days benchmark).
- *Deductions:* Only for damages beyond normal wear and tear (Arts. 1657, 1658). Itemized with receipts. Burden of proof on landlord. "Automatic forfeiture" clauses void (Art. 1306/1409).
- *Tax — at receipt:* NOT taxable (liability). BIR Ruling DA-334-2004; RMC 11-2024.
- *Tax — at application/forfeiture:* BECOMES gross receipts. 12% VAT (if VAT-registered, rent > PHP 15K); 5% EWT; RCIT. Per BIR Ruling 118-12; RR 16-2005; RR 02-98.
- *Delay penalty:* 6% p.a. legal interest from demand (Nacar v. Gallery Frames; BSP Circular 799).

**Automability: 3/5** — Bookkeeping, computation, compliance tracking, and alerts are automatable. Score limited by: premises inspection (subjective — normal wear vs. damage), deduction amount estimation (quotation-based), regime classification (human assessment), interest rate entry (bank passbook), demand letter decision.

**Crispina status:**
- Built: Nothing — no SecurityDeposit, DepositDeduction, DepositRefund models. No deposit-related ChargeType.
- Relevant existing: `Charge` model (adaptable for deposit application charges), `Payment`/`PaymentAllocation` (for refund tracking), `CurrencyDecimal(10,2)`.

**Feature spec summary:**
- New entities: `SecurityDeposit` (amount, bank_ref, lease_regime, status), `DepositInterestAccrual`, `DepositDeduction` (itemized with supporting docs), `DepositApplication` (tax reclassification: VAT + EWT amounts), `DepositRefund` (method, deadline, overdue flag)
- Core logic: Collection → validate caps (controlled: ≤2 months) → hold with interest tracking → at lease end: inspection → itemized deductions → refund = deposit − deductions + interest (controlled) → tax reclassification journal entries
- Edge cases: Vacancy decontrol (deposit rules change per lease, not per unit), tacit reconduction (deposit carries forward, no top-up right without new agreement), partial application, deposit application order (Art. 1252-1254), advance rent vs. deposit substance test (BIR refundability test)

*Full analysis: `analysis/security-deposit-lifecycle.md`*

---

## 5. Contract Processes

### P8 — Lease Contract Generation

**Description:** Generate new lease contracts from templates with variable substitution, incorporating mandatory PH clauses, corporate authorization references, and SEC-registered corporation requirements. Produce signed-ready documents with DST computation.

**Current method:** Manual Word template — fill in tenant/unit details, print 3+ copies, arrange notarization, manually compute DST and file BIR Form 2000. No tracking of execution milestones.

**Regulatory rules:**
- *Writing requirement:* Civil Code Art. 1403(2)(e) — leases > 1 year must be in writing (Statute of Frauds).
- *Notarization:* Not required for validity between parties, but needed for RD registration, court admissibility, and practical enforceability. 2004 Rules on Notarial Practice (A.M. No. 02-8-13-SC).
- *Corporate authorization:* RA 11232 (Revised Corporation Code) Sec. 39 — board resolution required. Secretary's Certificate must certify resolution.
- *DST:* NIRC Sec. 194 (TRAIN-amended) — PHP 6 on first PHP 2,000 + PHP 2 per additional PHP 1,000 of annual rent, multiplied by lease term in years. Filed on BIR Form 2000 within 5 days after close of month of execution.
- *Mandatory clauses (residential controlled):* RA 9653 terms — deposit cap (2+1), escalation cap (NHSB), grace period, ejectment grounds. Including prohibited clauses = void and potential fine.
- *Lease registration:* RD registration to bind third parties. Optional but advisable for long-term leases.

**Automability: 4/5** — Template system, variable substitution, DST computation, clause selection, and milestone tracking are deterministic. Deducted for: negotiation of commercial terms (human), notarization logistics (physical), board resolution timing (governance process).

**Crispina status:**
- Built: `Lease`, `LeaseRentable` (M2M junction), `RecurringCharge` creation. Basic lease data model.
- Gaps: No contract template system; no DST computation; no clause library; no board resolution tracking; no notarization milestone tracking; no document generation (PDF/print).

**Feature spec summary:**
- New entities: `LeaseTemplate` (per unit type, with clause library), `LeaseClause` (mandatory/optional per regime), `BoardResolution` (resolution#, date, scope, authorized signatory), `LeaseExecutionMilestone` (draft → signed → notarized → registered → DST filed), `DSTComputation` (annual rent, term, computed amount, Form 2000 filing date)
- Core logic: Select template by regime → substitute variables (tenant, unit, term, rate, deposit, escalation) → include mandatory clauses per regime → compute DST → generate PDF → track execution milestones
- Edge cases: Lease covering "all or substantially all" corporate assets (requires 2/3 stockholder approval), multiple rentables under one lease, DST computation for partial-year terms

*Full analysis: `analysis/lease-contract-generation.md`*

---

### P9 — Lease Renewal & Extension

**Description:** Manage lease continuity — formal renewal (new contract), extension (addendum), and tacit reconduction (implied month-to-month after 15-day holdover). Includes deposit adjustment, escalation application, DST filing, and board resolution.

**Current method:** Fully manual/ad hoc. No systematic tracking of upcoming expirations. Leases drift into tacit reconduction without awareness. DST on renewal frequently missed.

**Regulatory rules:**
- *Three scenarios:* (1) Renewal = new contract, full DST, all terms negotiable. (2) Extension = addendum, DST on extension period only. (3) Tacit reconduction = no document, no DST (NIRC Sec. 194 taxes the document).
- *Tacit reconduction (Art. 1670):* Three elements — term expired + no notice to vacate + 15 days continued enjoyment. Creates month-to-month lease. Original terms revived except period and guaranty (Art. 1672 — guarantor released).
- *Notice to prevent reconduction:* 15 days written notice before expiry for leases with fixed period (Art. 1670). For controlled units, only RA 9653 Sec. 9 ejectment grounds apply.
- *DST on renewal:* Full DST for new term (NIRC Sec. 194). Extension: DST on additional period only. Tacit reconduction: no DST (no document).
- *Deposit adjustment:* On renewal with escalated rent, lessor may request top-up to maintain ratio. New agreement required.
- *Holdover penalty:* Commercial leases often stipulate 150-200% of last rent for unauthorized holdover. For controlled units, landlord cannot charge holdover premium absent ejectment grounds.

**Automability: 4/5** — Expiration tracking, reconduction detection, DST computation, document generation are deterministic. Deducted for: renewal negotiation (human), holdover management decisions (business judgment), notice timing (logistics).

**Crispina status:**
- Built: `Lease` with `date_start`/`date_end`; basic lease lifecycle.
- Gaps: No `status` field (active/expired/month_to_month); no reconduction detection; no expiry alerting; no renewal/extension document generation; no DST tracking for renewals; no deposit top-up workflow.

**Feature spec summary:**
- Enhanced: `Lease` + `status` ENUM (DRAFT, ACTIVE, EXPIRED, MONTH_TO_MONTH, HOLDOVER, TERMINATED, RENEWED) + `original_lease_pk` (FK for renewal chain)
- New entities: `LeaseEvent` (audit log: created, activated, expired, renewed, reconduccion_started, terminated), `NonRenewalNotice` (date_sent, method, is_within_deadline)
- Core logic: Daily job → check expiring leases → alert at 90/60/30/15 days → at expiry: if no notice + 15 days continued enjoyment → auto-transition to MONTH_TO_MONTH → if renewal executed → create new Lease linked to original → compute DST on new term
- Edge cases: Tacit reconduction for controlled units (only RA 9653 Sec. 9 ejectment grounds valid), guaranty release (Art. 1672), holdover penalty rates (commercial only), deposit carry-forward vs. top-up, DST on extension vs. renewal

*Full analysis: `analysis/lease-renewal-extension.md`*

---

### P10 — Lease Status Visibility

**Description:** Dashboard showing all active leases across the portfolio — tenant, unit, term dates, monthly rate, escalation schedule, upcoming renewals, and expiring lease alerts.

**Current method:** Manual — property manager checks lease files periodically. No portfolio-wide view. Tacit reconduction often undetected.

**Regulatory rules:**
- *Tacit reconduction detection:* Civil Code Art. 1670 — auto-triggers after expiry + 15 days acquiescence. System must detect and flag.
- *PFRS 16 maturity analysis:* Corporate tenants may request lease maturity schedule for right-of-use asset accounting.

**Automability: 5/5** — Purely data-driven. All inputs (lease dates, status, rates) are structured. Dashboard generation, alert computation, and status transitions are entirely deterministic.

**Crispina status:**
- Built: `Lease` with date_start/date_end; `LeaseRentable` for unit assignment.
- Gaps: No lease status field; no event log; no alerting system; no reconduction detection; no dashboard/views.

**Feature spec summary:**
- Lease status state machine: DRAFT → ACTIVE → EXPIRED → MONTH_TO_MONTH / HOLDOVER → TERMINATED / RENEWED
- Alert system: 90/60/30/15-day expiry warnings + reconduction countdown (15-day window) + NHSB anniversary reminders
- Views: `TenantLeaseView` (per-tenant: unit, status, term, rate, next escalation), `PortfolioSummary` (aggregate: active/expiring/month_to_month/vacant counts, total monthly revenue, weighted average remaining term)
- Data model: `LeaseEvent` (audit log), `NonRenewalNotice`, status transition logic

*Full analysis: `analysis/lease-status-visibility.md`*

---

## 6. Handoff Processes

### P11 — Rent Roll Preparation

**Description:** Generate the monthly rent roll spreadsheet — the central report the external accountant needs for BIR filings. 26-column specification cross-referenced to BIR forms (LIS, 2550Q, 1702Q, SAWT).

**Current method:** Manual spreadsheet compiled from ledger, payment records, and collection sheets. Error-prone, time-consuming, inconsistent format.

**Regulatory rules:**
- *LIS (List of Income Sources):* RR 12-2011 — semi-annual filing of 9 prescribed columns (payor TIN, name, address, amount of income payment, tax withheld). Due within 15 days after close of semester (Jul 15, Jan 15).
- *2307 tracking:* RR 02-98 Sec. 2.58 — corporate tenants must issue Form 2307 within 20 days after quarter-end. Lessor must track expected vs. received certificates.
- *SAWT:* Summary Alphalist of Withholding Tax at Source — filed as attachment to 1702Q. Generated from collected 2307s.

**Automability: 5/5** — Rent roll is purely an aggregation of data from upstream processes. All 26 columns are deterministic given billing, payment, and lease data.

**Crispina status:**
- Built: Basic Charge and Payment models provide raw data.
- Gaps: No TIN on Tenant; no unit_type on Rentable; no invoice numbering; no 2307 tracking; no rent roll report generator; no LIS report.

**Feature spec summary:**
- 26-column rent roll: Tenant, TIN, Unit, Type, Lease Term, Monthly Rate, Escalation Date, VAT Status, Gross Rent Billed (base), VAT Billed, Total Billed, Amount Collected (cash), EWT Withheld, Net Collected, Prior Balance, Current Balance, Invoice#, Receipt#, 2307 Status, Deposit Held, Lease Status, Days Overdue, Notes, LIS Flag, SAWT Flag, Adjustment Flag
- New entities: `Form2307Record` (expected, received, delivered, reconciled workflow), `RentRollReport` (monthly snapshot), `LISReport` (semi-annual)
- Core logic: For each active lease → pull current period charges, payments, balances, 2307 status → assemble row → cross-reference flags for downstream forms
- Edge cases: Vacant units, multi-unit leases, mid-month move-in/out, tacit reconduction entries, 2307 mismatch, advance rent recognition, deposit movements

*Full analysis: `analysis/rent-roll-preparation.md`*

---

### P12 — Tax Data Compilation

**Description:** Prepare structured data packages for BIR quarterly and annual filings. Six sub-processes: Output VAT summary (2550Q), Income tax data (1702Q/1702-RT), SAWT from 2307s, EWT withheld on suppliers (0619-E/1601-EQ/1604-E), DST register (Form 2000), 2307 tracking & reconciliation.

**Current method:** Mostly manual/spreadsheet — quarterly aggregation, ad hoc 2307 collection (paper), supplier EWT compiled at quarter-end instead of payment time. Missing data causes late filing penalties (25% surcharge + 12% interest).

**Regulatory rules:**
- *Output VAT (2550Q):* NIRC Sec. 114; RR 16-2005; RR 3-2024. Accrual basis — declared at invoice issuance. Uncollected receivables adjustment: one-quarter claim window (RMC 65-2024, 8 requisites).
- *Income tax (1702Q):* NIRC Sec. 77. Quarterly, with SAWT attachment. Annual 1702-RT by April 15.
- *EWT on suppliers (0619-E):* NIRC Sec. 57; RR 02-98. Monthly (months 1-2 of quarter), quarterly summary (1601-EQ). Annual alphalist (1604-E) by March 1.
- *DST (Form 2000):* NIRC Sec. 194, 200. Per-event, within 5 days after close of month of lease execution.
- *SAWT:* RR 02-2006. Filed with 1702Q and 2550Q. Generated from collected 2307 certificates.
- *2307 reconciliation:* Match received certificates against expected EWT. Follow up missing certificates.
- *SLSP (Summary List of Sales/Purchases):* RR 1-2012 — VAT-registered corporations must file quarterly alongside 2550Q. Sales list extracted from P5 (billing); purchases list from P14 (expenses). Adds 4 deadlines/year.

**Automability: 4/5** — Data aggregation and summary computation are deterministic. Deducted for: 2307 receipt is external (depends on tenant compliance), VAT-exempt vs. VATable split requires unit type data, input VAT creditability assessment (mixed-operation apportionment), DST is event-driven (depends on lease execution tracking).

**Crispina status:**
- Built: Nothing specific to tax compilation.
- Relevant: Charge and Payment data (raw material for VAT and income tax summaries).

**Feature spec summary:**
- New entities: `OutputVATSummary` (quarterly: VATable sales, exempt sales, output VAT, input VAT, net payable), `IncomeTaxQuarterlyData`, `SAWTRecord` (from 2307s), `EWTWithheldSummary` (on supplier payments), `DSTRegister` (per lease execution)
- 7 compilation workflows: (1) Output VAT → 2550Q, (2) Income → 1702Q, (3) SAWT → attachment, (4) EWT → 0619-E/1601-EQ/1604-E, (5) DST → Form 2000, (6) 2307 tracking, (7) SLSP → quarterly attachment to 2550Q (sales from P5, purchases from P14; RR 1-2012)
- Feeds directly from: P5 (billing → output VAT), P6 (payments → collections), P11 (rent roll → comprehensive summary), P14 (expenses → input VAT, EWT withheld on suppliers)

*Full analysis: `analysis/tax-data-compilation.md`*

---

### P13 — Official Receipt / Invoice Data

**Description:** Manage the EOPT dual-document framework — VAT Sales Invoice (primary, at accrual) and Official Receipt (supplementary, at payment). Track Authority to Print (ATP), sequential numbering, and upcoming EIS compliance.

**Current method:** No systematic numbering or ATP tracking. Receipts/invoices prepared manually.

**Regulatory rules:**
- *EOPT dual-document:* RA 11976 (EOPT Act); RR 7-2024 — Invoice is primary (supports input VAT claims), issued at accrual. Receipt is supplementary, issued at payment.
- *Invoice requirements:* RR 7-2024 Sec. 6(B) — 16 mandatory fields. Sequential numbering per ATP.
- *Separate numbering:* Invoices and receipts maintain SEPARATE sequential series.
- *ATP management:* RR 6-2022 — 5-year validity (extended from 3-year under RR 18-2012; validity period is CONFLICTING — RMC 123-2022 removed expiry entirely, but later RRs are silent). Printer accreditation required.
- *EIS compliance:* RR 26-2025 — Electronic Invoicing System deadline December 31, 2026. Large taxpayers first; smaller entities phased in.
- *Penalties:* PHP 1,000-50,000 for non-issuance; up to PHP 10M for printing without ATP.

**Automability: 4/5** — Document generation, numbering, ATP tracking are deterministic. Deducted for: ATP renewal logistics (physical BIR interaction), EIS migration planning, printer accreditation management.

**Crispina status:**
- Built: Nothing — no invoice/receipt numbering, no ATP tracking, no TIN on Tenant.

**Feature spec summary:**
- New entities: `DocumentSequence` (type: INVOICE/RECEIPT, current_number, ATP ref, series range), `AuthorityToPrint` (ATP#, valid dates, series range, printer info, exhaustion alerts), `IssuedDocument` + `IssuedDocumentLine`
- Core logic: At billing → generate Invoice (sequential from invoice series) → at payment → generate Receipt (sequential from receipt series) → track ATP utilization → alert at 80%/90%/100% exhaustion
- ASCII template mockups for both invoice and receipt in analysis
- EIS preparation: API-ready document data model for eventual electronic submission

*Full analysis: `analysis/official-receipt-data.md`*

---

### P14 — Expense Tracking

**Description:** Record all property disbursements (repairs, maintenance, utilities, permits, supplies) with proper EWT withholding, input VAT tracking, and depreciation for fixed assets. Compile into formats the accountant needs for books of accounts.

**Current method:** Paper receipts in a folder. No systematic recording at payment time. Accountant receives a physical bundle at quarter-end and re-keys everything.

**Regulatory rules:**
- *Deduction substantiation:* NIRC Sec. 34 — requires supporting documentation (OR/invoice from supplier, proof of payment, withholding compliance). EOPT Act repealed Sec. 34(K) — non-withholding no longer disallows deduction.
- *EWT as withholding agent:* RR 02-98 — corporation must withhold EWT on payments to suppliers. 14 expense categories with rates 2-15% depending on payee type (individual/corporate, VAT-registered or not, large taxpayer or not).
- *Input VAT:* NIRC Sec. 110 — creditable input VAT from VAT-registered suppliers only. Mixed-operation apportionment required (rental income = VATable + exempt). Capital goods > PHP 1M: amortize over 60 months.
- *Depreciation:* No BIR-prescribed useful life; 5% residual value floor. Capital vs. ordinary repair distinction.
- *Filing:* 0619-E (monthly), 1601-EQ (quarterly), 1604-E + QAP (annual alphalist) for EWT withheld. Form 2307 issued to suppliers.

**Automability: 4/5** — EWT computation, input VAT tracking, depreciation scheduling are deterministic once expense is classified. Deducted for: expense classification (human judgment — which ATC code?), capital vs. repair distinction, receipt validation, payee type determination.

**Crispina status:**
- Built: Nothing — entire expense side was out of scope for Crispina.

**Feature spec summary:**
- New entities: `SupplierPayee` (TIN, name, type, VAT status, large taxpayer flag), `ExpenseCategory` (ATC code, EWT rate by payee type, deductibility rules), `DisbursementVoucher` (amount, VAT, EWT withheld, net payment, supporting doc), `InputVATRegister`, `EWTWithheldRegister`, `FixedAssetRegister`, `DepreciationScheduleEntry`
- 9 generated reports: expense register, input VAT register, EWT summary, Form 2307 data (to suppliers), QAP data, annual alphalist, fixed asset schedule, depreciation schedule, expense summary by category
- Core logic: Record expense → classify by category → auto-compute EWT based on payee type × category rate → check input VAT creditability → for fixed assets: create depreciation schedule → generate 2307 for supplier

*Full analysis: `analysis/expense-tracking.md`*

---

## 7. Cross-Cutting Concerns

Five concerns that span multiple processes and must be handled consistently:

### 7.1 VAT Treatment

**Affects:** P1, P2, P3, P4, P5, P7, P11, P12, P13, P14

| Scenario | VAT Treatment | Processes Affected |
|----------|--------------|-------------------|
| Residential rent ≤ PHP 15K/month | Permanent VAT exemption (NIRC 109(1)(Q)) | P5, P11, P12 |
| Commercial rent / residential > PHP 15K | 12% VAT if lessor > PHP 3M aggregate | P5, P7, P11, P12, P13 |
| Water pass-through | NOT VATable (conduit) | P2, P5 |
| Electric pass-through | CONFLICTING — depends on billing structure | P3, P5 |
| Penalty income | 12% VAT (part of gross receipts) | P4, P12 |
| Deposit application/forfeiture | 12% VAT when reclassified as income | P7, P12 |
| Input VAT from suppliers | Creditable if from VAT-registered supplier | P14, P12 |

**Design implication:** Every `Charge` record must carry a `vat_rate_used` frozen at creation time. The billing system must determine VAT treatment per charge based on unit type, tenant type, and lessor VAT status.

### 7.2 EWT 5% (Creditable Withholding Tax on Rent)

**Affects:** P4, P5, P6, P7, P11, P12

Corporate tenants withhold 5% EWT on rental payments (RR 02-98, Sec. 2.57.2(B)). The withholding applies to base rent (excluding VAT) and extends to: penalty income, utility pass-throughs "for lessor's account," security deposit applications, and RPT paid by lessee for lessor.

**Design implication:** `Tenant.is_corporate` flag determines EWT applicability. Payment tracking must reconcile: invoice amount = cash received + EWT withheld + VAT. Form 2307 certificates must be tracked (expected → received → reconciled → delivered to accountant).

### 7.3 Tenant Type Bifurcation

**Affects:** P1, P2, P3, P4, P5, P6, P7, P8, P9, P10

Almost every process has different rules for residential controlled vs. commercial tenants:

| Process | Residential Controlled | Commercial |
|---------|----------------------|------------|
| P1 Escalation | NHSB cap (1-2.3%/year) | Contractual (typically 3-10%) |
| P2 Water | No sewerage charge | Sewerage 20% of Basic |
| P4 Penalties | Safe harbour 1%/month, max 1mo rent/year | Contractual, up to ~3%/month |
| P5 Billing | VAT-exempt if ≤ PHP 15K; 5-day default due | 12% VAT; due per contract |
| P7 Deposit | Max 2+1, bank-hold, interest return | No cap, contractual interest |
| P8/P9 Contracts | Mandatory RA 9653 clauses | Freedom of contract |

**Design implication:** `Rentable.unit_type` (RESIDENTIAL/COMMERCIAL) and `Lease.lease_regime` (CONTROLLED_RESIDENTIAL/COMMERCIAL/NON_CONTROLLED_RESIDENTIAL) must be set at lease creation and propagated to all downstream computations.

### 7.4 Invoice / Receipt Sequential Numbering

**Affects:** P5, P6, P7, P13

Under the EOPT Act (RA 11976) + RR 7-2024, the corporation must maintain:
- **VAT Sales Invoice** series — issued at billing (accrual)
- **Official Receipt** series — issued at payment
- **Credit Memo** series — for billing corrections

Each series is ATP-managed with gapless sequential numbering. Shared across all processes that issue documents.

**Design implication:** Centralized `DocumentSequence` with atomic increment (PostgreSQL `UPDATE ... RETURNING`). ATP exhaustion monitoring. Separate series per document type per establishment.

### 7.5 Lease Lifecycle Events

**Affects:** P1, P4, P5, P7, P8, P9, P10

Lease status transitions (creation → active → expiry → reconduction/renewal/termination) trigger cascading effects:

| Event | Processes Triggered |
|-------|-------------------|
| Lease created | P8 (contract generation), P7 (deposit collection), P5 (first billing) |
| Lease anniversary | P1 (escalation), P10 (alert) |
| Lease expiring (90/60/30 days) | P10 (alert), P9 (renewal initiation) |
| Lease expired + 15 days | P9 (reconduction detection), P10 (status change) |
| Lease renewed | P8 (new contract), P1 (new escalation params), P7 (deposit top-up) |
| Lease terminated | P7 (deposit deduction/refund), P4 (final penalty assessment), P6 (final balance) |

**Design implication:** `LeaseEvent` audit log captures every transition. Event-driven triggers initiate downstream processes. State machine enforces valid transitions.

---

## 8. Process Dependencies

### 8.1 Dependency Graph

```
F0 (Lease & Tenant Master)
├──► P1  (Rent Escalation)        ──► P5  (Monthly Billing)
├──► P2  (Water Billing)          ──► P5
├──► P3  (Electric Billing)       ──► P5
├──► P4  (Late Payment Penalties) ──► P5
│                                      │
│                                      ▼
├──► P6  (Payment Tracking)  ◄──── P5 (charges to track)
│    ├──► P4  (outstanding balances → penalties)
│    ├──► P7  (outstanding at lease-end → deductions)
│    ├──► P11 (collections, balances)
│    ├──► P12 (SAWT from 2307 tracking)
│    └──► P13 (receipt register)
│
├──► P7  (Security Deposit)
│    ├──► P5  (deposit applied → income charge)
│    ├──► P11 (deposit held column)
│    └──► P12 (reclassification events)
│
├──► P8  (Lease Contract Gen)     ──► P12 (DST computation)
├──► P9  (Lease Renewal)          ──► P8, P12
├──► P10 (Lease Status)           ──► P9 (expiry alerts trigger renewal)
│
├──► P11 (Rent Roll)  ◄──── P5, P6, P7
│    └──► P12 (Tax Data Compilation)
│
├──► P13 (Official Receipt Data)  ◄──── P5, P6
│    └──► P12
│
└──► P14 (Expense Tracking)
     └──► P12 (EWT on suppliers, input VAT)
```

### 8.2 Feedback Loops

Four circular dependencies exist (resolved by temporal ordering — each cycle runs once per month):

1. **P4 ↔ P6:** Penalties depend on outstanding balances (P6); payments reduce those balances and trigger new penalty recalculation.
2. **P5 ↔ P6:** Billing generates charges (P5) that payment tracking allocates against (P6); prior balance from P6 feeds back into next month's billing statement.
3. **P7 ↔ P5:** Security deposit application creates an income charge (fed to P5 as a charge event); billing tracks the resulting charge.
4. **P9 ↔ P10:** Lease status alerts (P10) trigger renewal process (P9); renewal changes lease status (P10).

### 8.3 Monthly Close Execution Order (Topological Sort)

**Layer 0 — Prerequisites (Day 1-2):**
- Meter readings entered (input to P2, P3)
- Payments recorded (input to P6)
- Lease anniversaries checked (input to P1)

**Layer 1 — Independent Computations (Day 2):**
- P1: Rent escalation (if anniversary this month)
- P2: Water billing (from readings)
- P3: Electric billing (from readings)
- P4: Late payment penalties (from prior month's balances)

**Layer 2 — Aggregation (Day 2-3):**
- P5: Monthly billing generation (consumes P1-P4 outputs)

**Layer 3 — Collection Tracking (Day 3-4):**
- P6: Payment tracking (allocates against P5 charges)
- P13: Invoice/receipt issuance (documents for P5 charges and P6 payments)

**Layer 4 — Reporting (Day 4-5):**
- P11: Rent roll preparation (aggregates P5, P6, P7)
- P14: Expense tracking compilation

**Layer 5 — Tax Handoff (Day 5):**
- P12: Tax data compilation (aggregates P11, P13, P14)
- Deliver monthly package to external accountant

### 8.4 Minimum Viable Pipeline (MVP)

The smallest set of processes that delivers immediate value:

**F0 + P1 + P5 + P6 + P11 = Automated Rent Roll**

This covers: lease master data → rent escalation → monthly billing → payment tracking → rent roll for accountant. Adds the most value by automating the monthly handoff bottleneck.

**Phase 2 add:** P2 + P3 (utility billing) + P4 (penalties)
**Phase 3 add:** P8 + P9 + P10 (contract lifecycle)
**Phase 4 add:** P7 + P12 + P13 + P14 (full compliance pipeline)

---

## 9. Compliance Calendar Summary

The corporation faces ~43 recurring compliance deadlines per year across four regulatory domains:

| Domain | Regulator | Annual Deadlines |
|--------|-----------|:----------------:|
| BIR (national tax) | Bureau of Internal Revenue | ~30 |
| SEC (corporate) | Securities and Exchange Commission | 2 |
| LGU (local) | Las Piñas City / Barangay | ~8 per property |
| Other national | BFP, DENR, City Health Office | ~3 per property |

### Key Monthly Deadlines

| Day | Filing | Form | Data Source |
|-----|--------|------|-------------|
| 10th (non-eFPS) / 15th (eFPS) | EWT remittance | 0619-E | P14 (expenses) |
| By 5th | Accountant handoff package | — | P11, P13, P14 |

### Key Quarterly Deadlines

| Deadline | Filing | Data Source |
|----------|--------|-------------|
| 25th after Q-end | VAT Return (2550Q + SLSP) | P11 → P12 |
| Last day after Q-end | EWT Return (1601-EQ + QAP) | P14 → P12 |
| 60th day after Q-end | Income Tax (1702Q + SAWT) | P11 → P12 |
| 20 days after Q-end | 2307 receipt from corporate tenants | P6 → P12 |

### Key Annual Deadlines

| Deadline | Filing | Data Source |
|----------|--------|-------------|
| January 20-31 | Business permit renewal (LGU) | LGU permits |
| January 31 | Annual RPT (Las Piñas 25% discount if paid by Jan 31) | LGU |
| March 1 | Annual EWT alphalist (1604-E) | P14 → P12 |
| April 15 | Annual ITR (1702-RT) | P12 |
| 30 days after ASM | SEC GIS + AFS | Corporate governance |
| January 31 / July 31 | LIS (semi-annual) | P11 |
| December 31, 2026 | EIS compliance deadline (RR 26-2025) | P13 |

### Alert System

| Level | Trigger | Action |
|-------|---------|--------|
| Info (blue) | 30 days before deadline | Add to upcoming deadlines dashboard |
| Warning (yellow) | 15 days before deadline | Notify property manager |
| Urgent (orange) | 5 days before deadline | Escalate to all stakeholders |
| Overdue (red) | Past deadline | Flag with penalty computation |

*Full analysis: `analysis/compliance-calendar.md`*

---

## 10. Data Pipeline Summary

### Four-Layer Architecture

```
Layer 1: DATA ENTRY (human action)
  Lease management, meter readings, payment recording,
  expense disbursement, 2307 receipt, deposit events
          │
          ▼
Layer 2: COMPUTATION (automatable)
  Rent escalation, water billing (per-tier), electric billing (blended),
  late penalties, monthly billing generation, payment allocation,
  security deposit lifecycle, DST computation, lease status transitions
          │
          ▼
Layer 3: REPORTING & HANDOFF
  Rent roll (26 columns), invoice/receipt register, expense package,
  2307 tracker, aging schedule, deposit liability schedule
          │
          ▼
Layer 4: FILING (accountant)
  2550Q (VAT), 1702Q/1702-RT (income tax), 1601-EQ/1604-E (EWT),
  0619-E (monthly EWT), Form 2000 (DST), SAWT, LIS, GIS, AFS
```

### Irreducible Manual Entry Points (9)

These are physical-world events that cannot be automated away:

1. Water meter readings (33 physical meters)
2. Electric meter readings (physical sub-meters)
3. Maynilad master bill data entry (from paper/PDF)
4. Meralco master bill data entry (from paper/online)
5. Payment recording (tenant pays → record amount, method, date)
6. Expense recording (supplier invoice → disbursement voucher)
7. 2307 certificate receipt (physical paper from corporate tenants)
8. Premises inspection results (lease-end, subjective assessment)
9. NHSB cap rate entry (annual, from published resolution)

Everything downstream of these 9 entry points is computable.

---

## 11. Shared Data Model Entities

Entities that serve as integration points between multiple processes:

| Entity | Created By | Consumed By |
|--------|-----------|-------------|
| `Lease` | P8 (contract gen) | P1, P2, P3, P4, P5, P6, P7, P9, P10, P11 |
| `Charge` | P1-P5, P7 | P6, P11, P12, P13 |
| `Payment` + `PaymentAllocation` | P6 | P4, P11, P12, P13 |
| `WaterCharge` / `ElectricCharge` | P2, P3 | P5 |
| `SecurityDeposit` | P7 | P5, P11, P12 |
| `RecurringChargePeriod` | P1 | P5 |
| `DisbursementVoucher` | P14 | P12 |
| `Form2307Record` | P6 (receipt tracking) | P11, P12 |
| `IssuedDocument` (Invoice/Receipt) | P13 | P5, P6, P12 |
| `LeaseEvent` | P8, P9, P10 | P1, P4, P5, P7 |
| `ComplianceObligation` | Compliance calendar | All (alert system) |

---

## 12. Crispina Coverage Summary

| Process | Crispina Built | Crispina Gaps |
|---------|:-------------:|:-------------:|
| P1 Rent Escalation | Partial | No NHSB lookup, no multi-type escalation |
| P2 Water Billing | Partial (standalone) | Uses prohibited blended method |
| P3 Electric Billing | Nothing | Entirely greenfield |
| P4 Late Penalties | Nothing | No penalty model |
| P5 Monthly Billing | Partial | No invoice numbering, no statement generation |
| P6 Payment Tracking | Partial | No tenant balance rollup, no aging |
| P7 Security Deposit | Nothing | Entirely greenfield |
| P8 Lease Contract Gen | Minimal | No template system, no DST |
| P9 Lease Renewal | Minimal | No status tracking, no reconduction detection |
| P10 Lease Status | Minimal | No dashboard, no alerts |
| P11 Rent Roll | Nothing | No report generator |
| P12 Tax Data | Nothing | No tax compilation |
| P13 Official Receipt | Nothing | No numbering, no ATP |
| P14 Expense Tracking | Nothing | Entirely greenfield |

**Summary:** Crispina provides a partial foundation for billing (P1, P5, P6) and basic lease data. 8 of 14 processes have zero Crispina coverage. The water calculator exists but uses a non-compliant billing method. The entire handoff/compliance layer (P11-P14) is greenfield.

---

## Appendix A: Regulatory Citation Index

| Citation | Full Name | Processes |
|----------|-----------|-----------|
| RA 9653 | Rent Control Act of 2009 | P1, P4, P6, P7, P8, P9 |
| NHSB 2024-01 | NHSB Resolution (2.3%/1% caps) | P1 |
| Civil Code Art. 1252-1254 | Payment allocation rules | P6, P7 |
| Civil Code Art. 1305-1306 | Freedom of contract | P1, P4, P8, P9 |
| Civil Code Art. 1403(2)(e) | Statute of Frauds (leases) | P8 |
| Civil Code Art. 1670 | Tacit reconduction | P9, P10 |
| Civil Code Art. 1672 | Guaranty release on reconduction | P9 |
| Civil Code Art. 2209 | Legal interest on delay | P4 |
| Civil Code Art. 2212 | Interest on interest (from demand) | P4 |
| BSP Circular 799 | Legal interest rate = 6% p.a. | P4, P7 |
| NIRC Sec. 108 | VAT on services (lease) | P5, P12 |
| NIRC Sec. 109(1)(Q) | VAT exemption: residential ≤ PHP 15K | P5, P12 |
| NIRC Sec. 110 | Input VAT credits | P14, P12 |
| NIRC Sec. 114 | Quarterly VAT return | P12 |
| NIRC Sec. 194 | DST on lease contracts | P8, P9, P12 |
| NIRC Sec. 237 | Invoice requirements | P5, P13 |
| RA 11976 (EOPT Act) | Invoice/receipt reform | P5, P6, P13 |
| RR 7-2024 | EOPT implementing rules (invoices) | P5, P13 |
| RR 3-2024 | Output VAT on uncollected receivables | P5, P12 |
| RR 16-2005 | Consolidated VAT regulations | P5, P12, P14 |
| RR 02-98 | EWT regulations | P6, P12, P14 |
| RR 12-2011 | LIS requirements | P11 |
| RR 18-2012 | Invoice printing/numbering | P13 |
| RR 26-2025 | Electronic Invoicing System | P13 |
| RA 11232 | Revised Corporation Code | P8 |
| RA 10963 (TRAIN Law) | Tax reform (DST rates, etc.) | P8, P12 |
| RA 12066 (CREATE MORE) | Corporate income tax rates | P12 |
| MWSS IRR 2008-02 | Per-tier water billing mandate | P2 |
| EPIRA (RA 9136) | Electric rate regulation | P3 |
| ERC Res. 12/2009 | Sub-metering guidelines | P3 |
| BIR Ruling DA-334-2004 | Deposit not taxable at receipt | P7 |
| BIR Ruling 118-12 | Deposit taxable at application | P7 |
| Nacar v. Gallery Frames | Legal interest framework | P4, P7 |

---

## Appendix B: Verification Status Summary

| Status | Count | Description |
|--------|:-----:|-------------|
| CONFIRMED | ~95 rules | Verified against 2+ independent sources |
| CONFIRMED WITH CORRECTION | ~8 rules | Verified but initial source contained errors; corrected |
| CONFLICTING | 3 rules | Authoritative sources disagree; flagged for advisor |
| UNVERIFIED | 1 rule | No authoritative source found (defective meter estimated billing) |

**Conflicting rules requiring advisor determination:**
1. VAT on electricity pass-throughs — EOPT Act exclusion vs. earlier BIR RRs (P3)
2. Specific ERC cap on electric admin fees — no published regulation, informal reference ranges only (P3)
3. ATP validity period — RR 18-2012 (3 years) vs. RR 6-2022/RMC 123-2022 (5 years / removal of expiry) vs. RR 7-2024 (silent) (P13)

**Hallucinated citations corrected:**
- "Radiowealth Finance v. Palacol" — no such PH SC case exists (P7, from Wave 1 input)
- "RA 11571" as rent control extension — actually the JCEC Enhancement Act (P4, from secondary sources)

---

*Generated from 14 Wave 2 process analyses and 3 Wave 3 integration analyses. Each analysis cross-checked regulatory rules against 2+ independent sources using verification subagents. Self-reviewed (Wave 4) with 3 corrections applied: ATP validity updated, LIS deadlines corrected, SLSP added to P12. Full analyses available in `analysis/` directory.*
