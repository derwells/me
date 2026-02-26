# Lease Status Visibility — Process Analysis & Feature Spec

*Analyzed: 2026-02-26 | Wave 2 | Depends on: crispina-models, crispina-services, lease-contract-requirements, rent-control-rules, lease-contract-generation, lease-renewal-extension, rent-escalation-calculation*

---

## 1. Process Description

**What:** A centralized dashboard showing the real-time status of every lease in the portfolio: which tenants are active, which leases are expiring soon, which are in month-to-month holdover, what the current rent and escalation schedule is, and what needs attention. This is the operational cockpit for a property manager overseeing 20-100 units across multiple properties.

**When:** Consulted daily by the property manager. Specific triggers: monthly billing prep, renewal negotiations, board meeting prep, accountant handoff (rent roll generation), and ad-hoc tenant inquiries.

**Who does it:** Property manager is the primary user. Board members may need periodic summary views. External accountant needs the lease data for PFRS 16 disclosures and rent roll preparation.

**Frequency:** Continuous — the dashboard is always-on. Alerts fire at specific intervals: 90/60/30/15 days before lease expiry, at expiry, and at the 15-day tacit reconduction trigger.

---

## 2. Current Method

**Fully manual / spreadsheet / memory.** The property manager currently:
1. Maintains a spreadsheet or paper file with lease details per unit
2. Relies on memory or calendar reminders for upcoming expirations
3. No consolidated view of lease statuses across the portfolio
4. No distinction between active, expired, month-to-month, or holdover leases in any system
5. Crispina had no lease status field — only `date_start` and `date_end` with no state machine
6. No alert system for approaching expirations or tacit reconduction risk
7. Board receives ad-hoc verbal reports on lease status — no structured portfolio view

**Pain points:**
- Missed lease expirations leading to unintentional tacit reconduction (especially problematic for controlled units — creates an ejectment trap per RA 9653 Sec. 12)
- No visibility into which leases are in month-to-month status vs. formally active
- No proactive renewal pipeline — renewal negotiations start late or not at all
- Accountant must manually compile lease data for PFRS 16 maturity analysis
- No aggregate portfolio metrics (occupancy rate, weighted average lease term, revenue concentration)
- Board has no structured view for governance oversight of the property portfolio

---

## 3. Regulatory Rules with Legal Citations

### Rule 1: Lease Status State Machine — Legal Basis for Each State

PH law defines distinct legal consequences for each phase of a lease lifecycle. The system must track these to apply the correct rules:

| Status | Legal State | Citation | Key Consequence |
|--------|------------|----------|-----------------|
| **DRAFT** | Contract exists but not yet executed | Art. 1306 (freedom of contract) | No obligations yet; DST not yet triggered |
| **ACTIVE** | Within stipulated term; both parties bound | Art. 1654 (lessor), Art. 1657 (lessee) | Full rights and obligations in effect |
| **EXPIRED** | Past date_end, within 15-day window | Art. 1670 (pre-reconduction window) | Liminal state; outcome depends on notice and continued occupancy |
| **MONTH_TO_MONTH** | Tacit reconduction triggered (15+ days, no notice, acquiescence) | Art. 1670 + Art. 1687 (monthly rent = month-to-month) | Implied lease; original terms survive except period and guaranty (Art. 1672) |
| **HOLDOVER** | Tenant continues against lessor's objection | Art. 1671 | Tenant = bad-faith possessor; liable for damages |
| **TERMINATED** | Ended by mutual agreement, ejectment, or breach | Art. 1673 (ejectment grounds), Art. 1191 (rescission), RA 9653 Sec. 9 (controlled) | Lease no longer in force; deposit return process begins |
| **RENEWED** | Replaced by successor lease | Art. 1306 + NIRC Sec. 194 (new DST on successor) | Old lease archived; new lease is the active record |

**Verification:** CONFIRMED — all six operational statuses map to specific Civil Code articles. Art. 1670 (reconduction), Art. 1671 (holdover), Art. 1673 (ejectment), Art. 1191 (rescission). See verification section.

### Rule 2: Tacit Reconduction Timeline (Art. 1670)

Three cumulative elements (*Buce v. Sps. Galeon*, G.R. No. 222785, Mar. 2, 2020):
1. Original lease term has expired
2. Lessor has NOT given notice to vacate (before or during the 15-day window)
3. Lessee continued enjoying the property for 15 days with lessor's acquiescence

**System transition:** On day 16 post-expiry, if no `NonRenewalNotice` recorded → auto-transition from EXPIRED → MONTH_TO_MONTH, log `LeaseEvent(TACIT_RECONDUCTION)`.

**Critical for controlled units:** Once a controlled lease enters month-to-month (indefinite period), RA 9653 Sec. 12 suspension of Art. 1673(1) applies — lessor cannot eject on period expiry alone. Must invoke a specific Sec. 9 ground.

**Verification:** CONFIRMED — *Paterno v. Court of Appeals* (G.R. No. 115763), *Samelo v. Manotok* (G.R. No. 170509).

### Rule 3: Alert Timing — Legal vs Operational

| Alert | Legal Mandate? | Practical Purpose |
|-------|---------------|-------------------|
| 90 days before expiry | NO — operational best practice | Start renewal negotiation |
| 60 days before expiry | NO — operational best practice | Escalate if no action |
| 30 days before expiry | NO — operational best practice | Urgent: decide renew/non-renew |
| 15 days before expiry | NO — operational best practice | Final window to prepare notice if not renewing |
| At expiry (day 0) | YES — status transition: ACTIVE → EXPIRED | Lease term has ended per contract |
| Day 1-14 post-expiry | YES — Art. 1670 notice window | Last chance to prevent tacit reconduction |
| Day 15 post-expiry | YES — Art. 1670 triggers reconduction | System must transition: EXPIRED → MONTH_TO_MONTH |
| 3 months before planned owner-use repossession | **YES** — RA 9653 Sec. 9(c) mandatory | Formal written notice required for controlled units |

**Verification:** CONFIRMED — RA 9653 Sec. 9(c) mandates 3-month notice for owner-use only. No other pre-expiry notice mandate. *Buce v. Galeon* confirms notice within 15-day window still prevents reconduction.

### Rule 4: Data Privacy (RA 10173) for Dashboard Display

An internal property management dashboard displaying tenant personal information is covered by the Data Privacy Act.

| Requirement | Rule | Citation |
|------------|------|----------|
| Lawful basis for processing | Contract performance (lease agreement) | RA 10173 Sec. 12(b) |
| Proportionate data | Name, unit, rent, balance, contact: **proportionate** | NPC Advisory Opinion 2018-027 |
| Excessive data | Birthday, profession, last address: **not proportionate** for dashboard | NPC Advisory Opinion 2018-027 |
| Access control | Role-based; authorized staff only | RA 10173 Sec. 20 (security measures) |
| NPC registration threshold | 1,000+ data subjects for mandatory registration | NPC Circular 2022-04 |

**Verification:** CONFIRMED — NPC Advisory Opinion 2018-027 directly addresses tenant data collection proportionality for property management. Contract performance under Sec. 12(b) is the primary lawful basis.

### Rule 5: PFRS 16 Disclosure Requirements for Lessors

The lease dashboard must be capable of producing data for the external accountant's PFRS 16 disclosures:

| Disclosure | PFRS 16 Reference | System Data Needed |
|-----------|-------------------|-------------------|
| Lease classification (operating vs finance) | Paras. 61-66 | Lease type flag (virtually all will be operating for a rental property business) |
| Maturity analysis of undiscounted lease payments | Para. 97 (operating) | Per-lease: remaining term, monthly rent, escalation schedule → project 5 years forward |
| Lease income by type | Paras. 90-91 | Total rent income, variable lease payments, sublease income |
| Risk management qualitative disclosure | Para. 92 | Portfolio concentration, weighted average lease term, renewal rates |

**Verification:** CONFIRMED — IFRS 16 (= PFRS 16) paras. 89-97. No explicit "lease register" mandate, but the maturity analysis is impossible without per-lease tracking of terms and payment schedules.

### Rule 6: Corporate Records Obligation (RA 11232)

**RA 11232 Sec. 73** requires every corporation to maintain "a record of all business transactions" at its principal office. While no specific lease register is mandated, the broad record-keeping obligation encompasses lease agreements as business transactions. PFRS 16 disclosures and rent roll requirements effectively mandate a structured lease inventory.

**Verification:** CONFIRMED — RA 11232 Sec. 73 text. No SEC Memorandum Circular found requiring a specific lease register. UNVERIFIED for SEC MC specifically.

---

## 4. Formula / Decision Tree

### Lease Status Transition State Machine

```
DRAFT ──[contract executed]──→ ACTIVE
  │                              │
  │                              ├──[date_end reached]──→ EXPIRED
  │                              │                          │
  │                              │                          ├──[15 days + no notice + tenant stays]──→ MONTH_TO_MONTH
  │                              │                          │                                            │
  │                              │                          │                                            ├──[new contract executed]──→ RENEWED
  │                              │                          │                                            ├──[mutual termination]──→ TERMINATED
  │                              │                          │                                            └──[ejectment (RA 9653 Sec. 9)]──→ TERMINATED
  │                              │                          │
  │                              │                          ├──[notice sent within 15 days + tenant stays]──→ HOLDOVER
  │                              │                          │
  │                              │                          ├──[renewal contract executed]──→ RENEWED
  │                              │                          │
  │                              │                          └──[tenant vacates]──→ TERMINATED
  │                              │
  │                              ├──[mutual early termination]──→ TERMINATED
  │                              ├──[ejectment ordered]──→ TERMINATED
  │                              └──[renewal before expiry]──→ RENEWED
  │
  └──[cancelled before execution]──→ (deleted / VOIDED)
```

### Auto-Transition Rules (System-Driven)

```python
def daily_lease_status_check():
    today = date.today()

    # 1. ACTIVE → EXPIRED (auto)
    for lease in Lease.filter(status='ACTIVE', date_end__lt=today):
        lease.status = 'EXPIRED'
        LeaseEvent.create(lease, 'STATUS_CHANGE', f'Lease expired on {lease.date_end}')

    # 2. EXPIRED → MONTH_TO_MONTH (auto, if no notice and 15 days passed)
    for lease in Lease.filter(status='EXPIRED'):
        days_post_expiry = (today - lease.date_end).days
        if days_post_expiry >= 15:
            has_notice = NonRenewalNotice.exists(lease_pk=lease.pk)
            if not has_notice:
                lease.status = 'MONTH_TO_MONTH'
                LeaseEvent.create(lease, 'TACIT_RECONDUCTION',
                    f'Art. 1670: 15 days post-expiry, no notice, tenant continuing')
                if lease.has_guarantor:
                    Alert.create('WARNING',
                        f'Guarantor obligation extinguished per Art. 1672 — '
                        f'lease {lease.pk} entered tacit reconduction')

    # 3. EXPIRED → HOLDOVER (auto, if notice sent AND tenant still occupying)
    for lease in Lease.filter(status='EXPIRED'):
        days_post_expiry = (today - lease.date_end).days
        if days_post_expiry >= 15:
            has_notice = NonRenewalNotice.exists(lease_pk=lease.pk)
            tenant_still_present = not TurnoverRecord.exists(lease_pk=lease.pk)
            if has_notice and tenant_still_present:
                lease.status = 'HOLDOVER'
                LeaseEvent.create(lease, 'HOLDOVER_STARTED',
                    f'Art. 1671: tenant continuing over lessor objection')
```

### Alert Generation Rules

```python
def generate_lease_alerts():
    today = date.today()
    alerts = []

    for lease in Lease.filter(status='ACTIVE'):
        days_to_expiry = (lease.date_end - today).days

        if days_to_expiry == 90:
            alerts.append(Alert('INFO', lease, 'Lease expires in 90 days — initiate renewal discussion'))
        elif days_to_expiry == 60:
            alerts.append(Alert('INFO', lease, 'Lease expires in 60 days'))
        elif days_to_expiry == 30:
            if not RenewalRecord.pending(lease):
                alerts.append(Alert('WARNING', lease, 'Lease expires in 30 days — no renewal initiated'))
        elif days_to_expiry == 15:
            if not RenewalRecord.pending(lease):
                alerts.append(Alert('WARNING', lease, 'Lease expires in 15 days — decide renew or non-renew'))
            if lease.has_guarantor:
                alerts.append(Alert('WARNING', lease,
                    'Guarantor at risk: if lease enters reconduction, guaranty extinguished (Art. 1672)'))

    for lease in Lease.filter(status='EXPIRED'):
        days_post_expiry = (today - lease.date_end).days
        remaining = 15 - days_post_expiry

        if remaining > 0 and not NonRenewalNotice.exists(lease_pk=lease.pk):
            severity = 'CRITICAL' if remaining <= 5 else 'WARNING'
            alerts.append(Alert(severity, lease,
                f'Day {days_post_expiry}/15 post-expiry — tacit reconduction in {remaining} days'))
            if lease.is_rent_controlled:
                alerts.append(Alert('CRITICAL', lease,
                    'CONTROLLED UNIT: reconduction creates ejectment trap (RA 9653 Sec. 12)'))

    return alerts
```

### Portfolio Metrics Formulas

```python
def compute_portfolio_metrics(leases):
    active = [l for l in leases if l.status in ('ACTIVE', 'MONTH_TO_MONTH')]
    total_units = Rentable.count()

    return {
        'occupancy_rate': len(active) / total_units,
        'total_monthly_revenue': sum(l.current_rent for l in active),
        'weighted_avg_lease_term_months': (
            sum(l.remaining_months * l.current_rent for l in active) /
            sum(l.current_rent for l in active)
        ),
        'controlled_count': len([l for l in active if l.is_rent_controlled]),
        'commercial_count': len([l for l in active if not l.is_rent_controlled]),
        'expiring_30_days': len([l for l in active if l.days_to_expiry <= 30]),
        'month_to_month_count': len([l for l in active if l.status == 'MONTH_TO_MONTH']),
        'holdover_count': len([l for l in leases if l.status == 'HOLDOVER']),
        'arrears_3_months': len([l for l in active if l.months_in_arrears >= 3]),
    }
```

### PFRS 16 Maturity Analysis (for Accountant)

```python
def generate_maturity_analysis(leases, as_of_date):
    """Produces the undiscounted lease payment maturity analysis
    required by PFRS 16 para. 97 (operating leases)."""
    buckets = {1: Decimal(0), 2: Decimal(0), 3: Decimal(0),
               4: Decimal(0), 5: Decimal(0), 'thereafter': Decimal(0)}

    for lease in leases:
        if lease.status not in ('ACTIVE', 'MONTH_TO_MONTH'):
            continue
        for year_offset in range(1, 20):  # project up to 20 years
            year_start = as_of_date + timedelta(days=365 * (year_offset - 1))
            year_end = as_of_date + timedelta(days=365 * year_offset)
            payments_in_year = lease.projected_payments(year_start, year_end)
            if year_offset <= 5:
                buckets[year_offset] += payments_in_year
            else:
                buckets['thereafter'] += payments_in_year

    return buckets
```

---

## 5. Edge Cases and Special Rules

1. **Controlled unit tacit reconduction trap:** The most critical alert scenario. A definite-term controlled lease CAN be terminated at expiry (RA 9653 Sec. 12 exception: "except when the lease is for a definite period"). But once it enters month-to-month via tacit reconduction, Art. 1673(1) suspension applies and the lessor needs a specific Sec. 9 ground. The dashboard must make the 15-day countdown prominently visible for controlled units.

2. **Multi-unit leases:** One lease covering multiple rentables (e.g., tenant leasing Units 101A + 101B). The dashboard should show the lease once in the lease list but cross-reference all occupied units. Status transitions apply to the entire lease, not individual units.

3. **Stale MONTH_TO_MONTH leases:** Leases that have been in tacit reconduction for years. The dashboard should flag these with duration (e.g., "Month-to-month since Mar 2023 — 35 months"). These represent risk: no guarantor protection (Art. 1672), possible missed escalation events, no formal contract for the current arrangement.

4. **Concurrent lease for same unit:** If a renewal is executed before the old lease expires (e.g., new lease starts April 1, old lease ends March 31), both leases may briefly appear "active." The system should handle successor-predecessor linkage to prevent double-counting in occupancy metrics.

5. **Holdover with no clear resolution:** A lease in HOLDOVER status may persist indefinitely if the lessor doesn't pursue ejectment. The dashboard should flag holdover leases older than 30 days with an escalating alert.

6. **Vacancy tracking:** When a lease is TERMINATED and the unit is vacant, the dashboard should show the unit as available. For controlled units, vacancy resets pricing freedom (RA 9653 Sec. 4 — vacancy decontrol).

7. **Board meeting portfolio summary:** Board members need an aggregate view: total units, occupancy rate, revenue by property, upcoming expirations by quarter, and compliance status (DST filings, permits). This is a filtered/aggregated view of the same underlying data, not a separate process.

8. **Month-to-month leases and maturity analysis:** Tacit reconduction leases have no definite end date. For PFRS 16 maturity analysis, the system should project month-to-month payments as ongoing until the end of the current fiscal year (conservative) or 12 months (practical). The accountant determines the appropriate assumption.

9. **Data privacy — tenant view restriction:** If the system has a tenant-facing portal in the future, the tenant should only see their own lease data. The internal dashboard shows all tenants but must implement role-based access control per RA 10173 Sec. 20.

10. **Escalation schedule visibility:** The dashboard should show the escalation timeline for each lease — next anniversary date, expected new rate, NHSB cap (if controlled), and threshold proximity. This data comes from `RecurringChargePeriod` records and the `NHSBCapRate` table.

---

## 6. What Crispina Built

### Exists

| Feature | Implementation | Notes |
|---------|---------------|-------|
| Lease model | `pk`, `tenant_pk`, `date_start`, `date_end` | Basic record with term dates |
| LeaseRentable M2M | Junction table for multi-unit leases | Supports one lease → multiple rentables |
| RecurringCharge + Periods | Pre-computed escalation as date-bounded rate periods | Can derive current rent from period lookup |
| TransactionDetail | `total_amount_due`, `total_amount_paid`, `total_balance` | Per-transaction balance (not per-tenant rollup) |
| Rentable path query | `case(Room.name, Rentable.name + Room.name)` | Display path for unit identification |
| Tenant model | `first_name`, `last_name`, `billing_name`, `email`, `mobile_number` | Basic contact info |

### NOT Built (Gaps)

| Feature | Status | Impact on Dashboard |
|---------|--------|-------------------|
| **Lease status field** | NOT BUILT | Cannot distinguish active/expired/month-to-month/holdover — the foundational gap |
| Lease event log | NOT BUILT (TODO in code) | No audit trail of status transitions |
| Expiry alerting | NOT BUILT | No proactive warnings for approaching expirations |
| Tacit reconduction detection | NOT BUILT | No 15-day countdown, no auto-transition |
| NonRenewalNotice tracking | NOT BUILT | Cannot determine if notice was sent (needed for reconduction logic) |
| Tenant-level balance rollup | NOT BUILT | Must aggregate across all transactions per tenant manually |
| Rent control flag | NOT BUILT | Cannot filter controlled vs commercial leases |
| Unit type classification | NOT BUILT | No RESIDENTIAL_CONTROLLED / COMMERCIAL distinction on Rentable |
| Portfolio metrics | NOT BUILT | No occupancy rate, revenue totals, or aggregate computations |
| PFRS 16 maturity export | NOT BUILT | Cannot produce the 5-year maturity analysis for the accountant |
| Predecessor-successor linkage | NOT BUILT | Cannot trace lease renewal history |
| Guarantor tracking | NOT BUILT | Cannot alert about Art. 1672 risk at reconduction |
| HoldoverRecord | NOT BUILT | No holdover status tracking |
| Corporate/TIN flags on Tenant | NOT BUILT | Cannot identify corporate tenants for EWT, 2307, or lessee board resolution requirements |
| Floor area on Rentable | NOT BUILT | Missing from dashboard data for property description |

### Design Observation

Crispina's data model has the raw building blocks (Lease with dates, RecurringChargePeriod with rates, Tenant with names, Rentable with units) but lacks the **status layer** needed for a functioning dashboard. The Lease model docstring ("State table of a lease. Shouldn't be updated directly") suggests the architects intended immutable lease records — but without a status field, the system cannot distinguish a current lease from an expired one without performing date arithmetic on every query.

---

## 7. Lightweight Feature Spec

### Data Model Additions

```
# Enhancements to existing models

Lease (enhanced)
├── + status: ENUM (DRAFT, ACTIVE, EXPIRED, MONTH_TO_MONTH,
│                   HOLDOVER, TERMINATED, RENEWED, VOIDED)
├── + is_rent_controlled: Boolean
├── + predecessor_lease_pk: FK → Lease (nullable)
├── + has_guarantor: Boolean (default False)
├── + guarantor_name: String (nullable)
├── + lease_classification: ENUM (OPERATING, FINANCE)  # PFRS 16; default OPERATING

Tenant (enhanced, if not already from other specs)
├── + tin: String (nullable)
├── + is_corporate: Boolean (default False)

Rentable (enhanced, if not already from other specs)
├── + unit_type: ENUM (RESIDENTIAL_CONTROLLED, RESIDENTIAL_UNCONTROLLED, COMMERCIAL)
├── + floor_area_sqm: Decimal (nullable)

# New models (if not already spec'd in lease-renewal-extension)

LeaseEvent (audit log)
├── pk: UUID
├── lease_pk: FK → Lease
├── event_type: ENUM (CREATED, ACTIVATED, EXPIRED, TACIT_RECONDUCTION,
│       HOLDOVER_STARTED, NOTICE_SENT, RENEWED, TERMINATED, VOIDED, STATUS_CHANGE)
├── event_date: Date
├── description: Text
├── related_lease_pk: FK → Lease (nullable)  # for RENEWED: successor
├── metadata: JSONB
└── created_by: String  # 'system' or user

NonRenewalNotice (from lease-renewal-extension spec)
├── ... (see lease-renewal-extension.md)

# New: Dashboard-specific views/queries (not tables)

TenantLeaseView (materialized view or query)
├── tenant_pk, tenant_name, billing_name
├── lease_pk, lease_status
├── unit_designation (Rentable path)
├── property_name
├── is_rent_controlled
├── current_monthly_rent (from latest RecurringChargePeriod)
├── lease_start, lease_end
├── days_to_expiry (computed: lease_end - today)
├── days_since_expiry (computed: today - lease_end, if expired)
├── next_escalation_date (next anniversary)
├── next_escalation_rate (from escalation params + NHSB cap)
├── total_balance (sum of unpaid charges)
├── months_in_arrears (computed from outstanding charges)
├── unit_type
├── has_guarantor

PortfolioSummary (computed aggregate)
├── total_units, occupied_units, vacant_units
├── occupancy_rate
├── total_monthly_revenue
├── controlled_count, commercial_count
├── expiring_next_30_days, expiring_next_90_days
├── month_to_month_count
├── holdover_count
├── arrears_3_months_count (ejectment-eligible per RA 9653 Sec. 9(b))
├── weighted_avg_remaining_term_months
```

### Dashboard Sections

**1. Lease Status Summary (top bar)**
- Counts by status: Active | Month-to-Month | Expired | Holdover | Vacant
- Occupancy rate (%)
- Total monthly revenue
- Count of leases requiring attention (alerts)

**2. Alert Panel (priority-sorted)**
- CRITICAL: Controlled leases in 15-day reconduction window
- WARNING: Leases expiring within 30 days, no renewal initiated
- WARNING: Guarantor at risk of extinction (Art. 1672)
- INFO: Leases expiring within 90 days
- INFO: Upcoming escalation anniversaries (next 30 days)
- INFO: 3-month arrears threshold reached (ejectment ground per RA 9653 Sec. 9(b))

**3. Lease Table (main view)**

| Column | Source | Notes |
|--------|--------|-------|
| Unit | Rentable path (Room.name + Rentable.name) | Sortable/filterable by property |
| Tenant | Tenant.full_name or billing_name | RA 10173 proportionate |
| Status | Lease.status | Color-coded: green=active, yellow=expiring, orange=month-to-month, red=holdover |
| Type | Rentable.unit_type | Controlled / Commercial |
| Monthly Rent | Latest RecurringChargePeriod.amount | VAT-inclusive |
| Lease Term | date_start → date_end | Shows "M-T-M" for month-to-month |
| Days to Expiry | Computed | Negative = days since expiry |
| Next Escalation | Anniversary date + expected rate | "Mar 15 @ 2.3% NHSB" |
| Balance | Sum of unpaid charges | Red if > 0 |
| Arrears (months) | Count of unpaid monthly rent charges | Red if ≥ 3 |

Filters: by property, by status, by unit type (controlled/commercial), by expiry range.

**4. Expiry Timeline View**
- Calendar/Gantt-style view showing lease terms and expirations over the next 12 months
- Groups by property
- Color-coded by status and unit type
- Highlights: renewal pipeline status (pending, in-progress, completed)

**5. PFRS 16 Export (for accountant)**
- Maturity analysis: annual undiscounted lease payments for years 1-5 + thereafter
- Lease classification summary (operating vs finance — virtually all operating)
- Total lease income by type (fixed rent, variable, utilities)
- One-click export to Excel/CSV format the accountant expects

### Inputs and Outputs

**Inputs (system reads):**
- Lease records (dates, status, rent control flag, guarantor flag)
- RecurringChargePeriod (current rent amounts, escalation schedule)
- NonRenewalNotice records (for reconduction logic)
- Charge + PaymentAllocation records (for balance/arrears computation)
- NHSBCapRate table (for escalation preview)
- Tenant records (name, contact, corporate flag)
- Rentable records (unit designation, type, property)

**Outputs (system produces):**
- Real-time dashboard display (web UI)
- Alert notifications (email, SMS, or in-app — property manager configurable)
- Portfolio summary PDF (for board meetings)
- PFRS 16 maturity analysis export (for accountant, quarterly/annually)
- Rent roll data feed (consumed by the rent-roll-preparation process)
- Lease status change audit log (LeaseEvent records)

---

## 8. Automability Score: 5/5

**Justification:**

| Component | Automability | Notes |
|-----------|-------------|-------|
| Status determination from dates + notices | 5/5 | Purely deterministic date arithmetic + record existence checks |
| Status transitions (auto-expiry, auto-reconduction) | 5/5 | Rule-based state machine, no human judgment |
| Alert generation (90/60/30/15-day) | 5/5 | Date arithmetic against lease end dates |
| Balance/arrears computation | 5/5 | Sum of charges minus sum of payments |
| Portfolio metrics (occupancy, revenue, averages) | 5/5 | Aggregate queries on structured data |
| PFRS 16 maturity analysis | 5/5 | Projection from lease terms + rent amounts |
| Escalation schedule preview | 5/5 | Lookup from RecurringChargePeriod + NHSBCapRate |
| Rent control classification | 5/5 | Unit type + rent threshold check |
| Reconduction detection | 5/5 | date_end + 15 days + absence of NonRenewalNotice |
| Alert delivery (email/SMS) | 5/5 | Triggered by rule engine, no human judgment |

**Overall: 5/5** — This is a pure reporting/monitoring/alerting process. All inputs are structured data already in the system. All rules are deterministic (date arithmetic, threshold checks, state machine transitions). No human judgment is required for the visibility layer itself — human judgment enters only in the *response* to what the dashboard shows (e.g., deciding whether to renew a lease).

---

## 9. Verification Status

| # | Rule | Status | Sources |
|---|------|--------|---------|
| 1 | Lease status state machine (6 statuses) | **CONFIRMED** | Art. 1654/1657 (active), Art. 1670 (reconduction), Art. 1671 (holdover), Art. 1673 (ejectment), Art. 1191 (rescission), Art. 1306 (renewal) |
| 2 | Tacit reconduction timeline (15 days) | **CONFIRMED** | Art. 1670; *Buce v. Galeon* (G.R. 222785); *Paterno v. CA* (G.R. 115763) |
| 3 | Art. 1672 — guaranty extinguished on reconduction | **CONFIRMED** | Art. 1672 text (lawphil.net, chanrobles.com) |
| 4 | RA 9653 Sec. 12 — ejectment trap for controlled month-to-month | **CONFIRMED** | RA 9653 Sec. 12 (lawphil.net); per lease-renewal-extension.md analysis |
| 5 | RA 9653 Sec. 9(c) — 3-month notice for owner-use | **CONFIRMED** | RA 9653 Sec. 9(c) (lawphil.net, Salenga Law Firm) |
| 6 | No general pre-expiry notice mandate (RA 9653) | **CONFIRMED** | RA 9653 Sec. 9 — expiry is standalone ground, no advance notice required |
| 7 | RA 10173 — dashboard covered, contract performance basis | **CONFIRMED** | RA 10173 Sec. 12(b); NPC Advisory 2018-027 |
| 8 | NPC proportionality — name/unit/rent/balance OK | **CONFIRMED** | NPC Advisory 2018-027 (tenant data proportionality) |
| 9 | PFRS 16 — 5-year maturity analysis required for lessors | **CONFIRMED** | IFRS 16 para. 97 (operating leases); Grant Thornton guidance |
| 10 | RA 11232 Sec. 73 — broad corporate records obligation | **CONFIRMED** | RA 11232 Sec. 73 (no specific lease register, but "all business transactions") |
| 11 | No Las Piñas local ordinance on tenant notification | **UNVERIFIED** | No online source found; would require contacting Sangguniang Panlungsod |

**11 rules examined. 10 confirmed, 1 unverified (local ordinance — low risk as national law governs lease obligations). No source conflicts.**

---

*Analyzed: 2026-02-26 | Sources: input/crispina-models.md, input/crispina-services.md, input/lease-contract-requirements.md, input/rent-control-rules.md, analysis/lease-renewal-extension.md, analysis/rent-escalation-calculation.md + verification subagent (21 claims verified across RA 11232, RA 10173, PFRS 16, Civil Code, RA 9653; 2-3 sources each)*
