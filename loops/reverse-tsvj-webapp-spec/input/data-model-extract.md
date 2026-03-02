# Data Model Extract — TSVJ Backoffice Web App

*Extracted from: `input/process-catalog.md` (14 processes + foundation)*
*Purpose: Unified entity list for Wave 2 database schema design*

---

## Entity Index

| # | Entity | Category | Created By | Consumed By | New/Existing |
|---|--------|----------|-----------|-------------|:------------:|
| 1 | Property | Foundation | F0 | All | Existing (Crispina) |
| 2 | Room | Foundation | F0 | All | Existing (Crispina) |
| 3 | Rentable | Foundation | F0 | P1-P5, P8-P11 | Existing + enhanced |
| 4 | Tenant | Foundation | F0 | All | Existing + enhanced |
| 5 | Lease | Foundation | P8 | P1-P11 | Existing + enhanced |
| 6 | LeaseRentable | Foundation | F0 | P1-P5, P8 | Existing (Crispina M2M) |
| 7 | ChargeType | Foundation | F0 (seed) | P1-P5, P7 | Existing + new types |
| 8 | RecurringCharge | Billing | P1, F0 | P5 | Existing (Crispina) |
| 9 | RecurringChargePeriod | Billing | P1 | P5 | Existing (Crispina) |
| 10 | NHSBCapRate | Billing | P1 (manual entry) | P1 | New |
| 11 | EscalationEvent | Billing | P1 | P1, P10 | New |
| 12 | WaterMeter | Billing | F0/P2 | P2 | New |
| 13 | WaterMeterTenant | Billing | P2 | P2 | New (junction) |
| 14 | WaterMeterReading | Billing | P2 (manual entry) | P2 | New |
| 15 | MayniladBill | Billing | P2 (manual entry) | P2 | New |
| 16 | MayniladRateSchedule | Billing | P2 (manual entry) | P2 | New |
| 17 | WaterBillingRun | Billing | P2 | P2, P5 | New |
| 18 | WaterCharge | Billing | P2 | P5, P11 | New |
| 19 | ElectricMeter | Billing | F0/P3 | P3 | New |
| 20 | ElectricMeterTenant | Billing | P3 | P3 | New (junction) |
| 21 | ElectricMeterReading | Billing | P3 (manual entry) | P3 | New |
| 22 | MeralcoBill | Billing | P3 (manual entry) | P3 | New |
| 23 | ElectricBillingRun | Billing | P3 | P3, P5 | New |
| 24 | ElectricCharge | Billing | P3 | P5, P11 | New |
| 25 | PenaltyLedger | Billing | P4 | P4, P6 | New |
| 26 | DemandRecord | Billing | P4 | P4 | New |
| 27 | BillingRun | Billing | P5 | P5, P6, P13 | New |
| 28 | Charge | Billing | P1-P5, P7 | P6, P11-P13 | Existing + enhanced |
| 29 | CreditMemo | Billing | P5 | P5, P13 | New |
| 30 | Payment | Collection | P6 | P4, P11-P13 | Existing + enhanced |
| 31 | PaymentAllocation | Collection | P6 | P6, P11 | Existing + enhanced |
| 32 | PaymentEvent | Collection | P6 | P6 | New |
| 33 | TenantBalance | Collection | P6 (materialized) | P4, P6, P11 | New (view) |
| 34 | SecurityDeposit | Collection | P7 | P5, P7, P11, P12 | New |
| 35 | DepositInterestAccrual | Collection | P7 | P7 | New |
| 36 | DepositDeduction | Collection | P7 | P7 | New |
| 37 | DepositApplication | Collection | P7 | P5, P7, P12 | New |
| 38 | DepositRefund | Collection | P7 | P7 | New |
| 39 | LeaseTemplate | Contracts | P8 | P8 | New |
| 40 | LeaseClause | Contracts | P8 | P8 | New |
| 41 | BoardResolution | Contracts | P8 | P8 | New |
| 42 | LeaseExecutionMilestone | Contracts | P8 | P8 | New |
| 43 | DSTComputation | Contracts | P8, P9 | P8, P9, P12 | New |
| 44 | LeaseEvent | Contracts | P8, P9, P10 | P1, P4, P5, P7, P10 | New |
| 45 | NonRenewalNotice | Contracts | P9 | P9, P10 | New |
| 46 | Form2307Record | Handoff | P6 | P11, P12 | New |
| 47 | RentRollReport | Handoff | P11 | P11 | New |
| 48 | LISReport | Handoff | P11 | P11 | New |
| 49 | OutputVATSummary | Handoff | P12 | P12 | New |
| 50 | IncomeTaxQuarterlyData | Handoff | P12 | P12 | New |
| 51 | SAWTRecord | Handoff | P12 | P12 | New |
| 52 | EWTWithheldSummary | Handoff | P12 | P12 | New |
| 53 | DSTRegister | Handoff | P12 | P12 | New |
| 54 | DocumentSequence | Handoff | P13 | P5, P6, P13 | New |
| 55 | AuthorityToPrint | Handoff | P13 | P13 | New |
| 56 | IssuedDocument | Handoff | P13 | P5, P6, P12 | New |
| 57 | IssuedDocumentLine | Handoff | P13 | P13 | New |
| 58 | SupplierPayee | Handoff | P14 | P14, P12 | New |
| 59 | ExpenseCategory | Handoff | P14 (seed) | P14 | New |
| 60 | DisbursementVoucher | Handoff | P14 | P12 | New |
| 61 | InputVATRegister | Handoff | P14 | P12, P14 | New |
| 62 | EWTWithheldRegister | Handoff | P14 | P12, P14 | New |
| 63 | FixedAssetRegister | Handoff | P14 | P14 | New |
| 64 | DepreciationScheduleEntry | Handoff | P14 | P14 | New |
| 65 | ComplianceObligation | Cross-cutting | System (seed + events) | All (alert system) | New |

---

## 1. Foundation Entities

### 1.1 Property

Source: F0. Existing Crispina entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| name | text | NOT NULL | e.g., "Building A" |
| address | text | NOT NULL | Full address incl. Las Piñas |
| tin | text | | Corporation TIN (for invoices) |
| rdo_code | text | | BIR Revenue District Office |

**Relationships:** Property 1→N Rentable

### 1.2 Room

Source: F0. Existing Crispina entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| name | text | NOT NULL | e.g., "Unit 201" |
| floor | integer | | Physical floor number |

**Relationships:** Room 1→1 Rentable (or Room 1→N Rentable if subdivided)

### 1.3 Rentable

Source: F0 + P1, P2, P3, P5. Existing Crispina entity, enhanced.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| room_id | FK → Room | NOT NULL | |
| property_id | FK → Property | NOT NULL | Denormalized for queries |
| name | text | NOT NULL | Display name |
| **unit_type** | ENUM('RESIDENTIAL', 'COMMERCIAL') | NOT NULL | **New** — needed by P1, P2, P4, P5 |
| **floor_area_sqm** | decimal(8,2) | | **New** — needed by P2, P3 (common area allocation) |
| is_active | boolean | DEFAULT true | |

**Derived field:** `is_rent_controlled` — computed from unit_type + current lease rent amount vs. PHP 10,000 threshold. Not stored; computed at query time.

**Relationships:** Rentable N→1 Room, Rentable N→1 Property, Rentable N→M Lease (via LeaseRentable)

### 1.4 Tenant

Source: F0 + P6, P11, P12, P13. Existing Crispina entity, enhanced.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| name | text | NOT NULL | Individual or company name |
| contact_number | text | | |
| email | text | | |
| address | text | | Permanent/billing address |
| **tin** | text | UNIQUE where NOT NULL | **New** — BIR TIN. Needed by P11, P12, P13. Format: XXX-XXX-XXX-XXX |
| **is_corporate** | boolean | NOT NULL, DEFAULT false | **New** — determines EWT applicability (P4, P6, P12, P13) |
| **is_vat_registered** | boolean | NOT NULL, DEFAULT false | **New** — determines invoice VAT treatment (P5, P13) |
| created_at | timestamp | NOT NULL | |
| updated_at | timestamp | NOT NULL | |

**Relationships:** Tenant 1→N Lease, Tenant 1→N Payment

### 1.5 Lease

Source: F0 + P1, P4, P5, P8, P9, P10. Existing Crispina entity, heavily enhanced.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| tenant_id | FK → Tenant | NOT NULL | |
| date_start | date | NOT NULL | |
| date_end | date | NOT NULL | |
| monthly_rent | decimal(10,2) | NOT NULL | Base monthly rent at lease start |
| **status** | ENUM | NOT NULL, DEFAULT 'DRAFT' | **New** — see state machine below |
| **escalation_type** | ENUM | NOT NULL, DEFAULT 'NONE' | **New** — P1 |
| **escalation_params** | jsonb | | **New** — P1. Structured per escalation_type |
| **penalty_rate_monthly** | decimal(5,4) | | **New** — P4. e.g., 0.0100 = 1%/month |
| **grace_period_days** | integer | DEFAULT 5 | **New** — P4. 5 for controlled (RA 9653 Sec. 7) |
| **lease_regime** | ENUM | NOT NULL | **New** — P1, P4, P7 |
| **custom_due_day** | integer | CHECK 1-31 | **New** — P5. Default 5 for controlled, per contract for commercial |
| **original_lease_id** | FK → Lease | | **New** — P9. For renewal chain |
| deposit_months | decimal(3,1) | | Months of rent as deposit (max 2 for controlled) |
| advance_months | decimal(3,1) | | Months of rent as advance |
| created_at | timestamp | NOT NULL | |
| updated_at | timestamp | NOT NULL | |

**Lease Status ENUM values:** DRAFT, ACTIVE, EXPIRED, MONTH_TO_MONTH, HOLDOVER, TERMINATED, RENEWED

**Lease Regime ENUM values:** CONTROLLED_RESIDENTIAL, NON_CONTROLLED_RESIDENTIAL, COMMERCIAL

**Escalation Type ENUM values:** NHSB_CAP, FIXED_PCT, STEPPED, CPI_LINKED, NONE

**Escalation Params JSONB structure (by type):**
- NHSB_CAP: `{}` (rate looked up from NHSBCapRate table)
- FIXED_PCT: `{ "rate": 0.05 }` (5% per year)
- STEPPED: `{ "steps": [{ "year": 1, "rate": 0.03 }, { "year": 3, "rate": 0.05 }] }`
- CPI_LINKED: `{ "base_cpi": 120.5, "base_date": "2025-01" }`
- NONE: `{}`

**Lease Status State Machine:**
```
DRAFT → ACTIVE (upon execution)
ACTIVE → EXPIRED (date_end reached, no renewal)
EXPIRED → MONTH_TO_MONTH (15 days acquiescence, Art. 1670)
EXPIRED → TERMINATED (notice given within 15 days)
EXPIRED → RENEWED (new lease executed)
MONTH_TO_MONTH → TERMINATED (notice given)
MONTH_TO_MONTH → RENEWED (new lease executed)
HOLDOVER → TERMINATED (ejectment or departure)
HOLDOVER → RENEWED (new lease executed)
```

**Relationships:** Lease N→1 Tenant, Lease N→M Rentable (via LeaseRentable), Lease 1→N Charge, Lease 0→1 Lease (original_lease_id for renewal chain)

### 1.6 LeaseRentable (Junction)

Source: F0. Existing Crispina M2M junction.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| rentable_id | FK → Rentable | NOT NULL | |
| | | UNIQUE(lease_id, rentable_id) | |

### 1.7 ChargeType (Seed Data)

Source: F0. Existing Crispina entity. New types added per process.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| code | text | UNIQUE, NOT NULL | Machine-readable |
| name | text | NOT NULL | Display name |
| default_vat_rate | decimal(4,2) | NOT NULL | e.g., 0.12 or 0.00 |
| is_vatable | boolean | NOT NULL | |
| ewt_rate | decimal(4,2) | | For EWT computation |

**Seed values needed:**
| Code | Name | VAT Rate | EWT Rate | Process |
|------|------|----------|----------|---------|
| RENT | Rent | 0.12* | 0.05 | P1, P5 |
| WATER | Water Pass-through | 0.00 | 0.02 | P2, P5 |
| ELECTRIC | Electric Pass-through | varies | 0.02 | P3, P5 |
| ELECTRIC_ADMIN | Electric Admin Fee | 0.12 | 0.05 | P3, P5 |
| PENALTY | Late Payment Penalty | 0.12 | 0.05 | P4, P5 |
| COMMON_WATER | Common Area Water | 0.00 | 0.02 | P2, P5 |
| COMMON_ELECTRIC | Common Area Electric | varies | 0.02 | P3, P5 |
| DEPOSIT_APPLICATION | Security Deposit Applied | 0.12 | 0.05 | P7 |
| OTHER | Other Charges | 0.12 | 0.05 | — |

*VAT rate for RENT depends on unit_type and rent amount (exempt if residential ≤ PHP 15K/month).

---

## 2. Billing Entities

### 2.1 RecurringCharge

Source: P1, P5. Existing Crispina entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| charge_type_id | FK → ChargeType | NOT NULL | |
| base_amount | decimal(10,2) | NOT NULL | Before VAT |
| vat_rate | decimal(4,2) | NOT NULL | Frozen at creation |
| effective_date | date | NOT NULL | |
| end_date | date | | |

### 2.2 RecurringChargePeriod

Source: P1. Existing Crispina entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| recurring_charge_id | FK → RecurringCharge | NOT NULL | |
| period_start | date | NOT NULL | |
| period_end | date | NOT NULL | |
| amount | decimal(10,2) | NOT NULL | Computed amount for this period |
| vat_rate | decimal(4,2) | NOT NULL | Frozen |

### 2.3 NHSBCapRate

Source: P1. New entity. Manual entry (annual).

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| year | integer | UNIQUE, NOT NULL | e.g., 2025, 2026 |
| rate | decimal(5,4) | NOT NULL | e.g., 0.0230 = 2.3% |
| resolution_number | text | | e.g., "2024-01" |
| effective_date | date | NOT NULL | |
| notes | text | | |

### 2.4 EscalationEvent

Source: P1. New entity. Audit log for each escalation.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| event_date | date | NOT NULL | Anniversary date |
| escalation_type | ENUM | NOT NULL | Type used for this escalation |
| previous_rent | decimal(10,2) | NOT NULL | |
| rate_applied | decimal(5,4) | NOT NULL | |
| new_rent | decimal(10,2) | NOT NULL | After ROUND_DOWN |
| threshold_crossed | boolean | NOT NULL, DEFAULT false | Crossed PHP 10K → exits rent control |
| recurring_charge_period_id | FK → RecurringChargePeriod | | The period created |
| created_at | timestamp | NOT NULL | |
| notes | text | | |

### 2.5 WaterMeter

Source: P2. New entity. ~33 sub-meters + 2 common area.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| meter_identifier | text | UNIQUE, NOT NULL | e.g., "SM-01", "CR-1" |
| meter_type | ENUM('SUB_METER', 'COMMON_AREA', 'MASTER') | NOT NULL | |
| is_active | boolean | DEFAULT true | |
| notes | text | | |

### 2.6 WaterMeterTenant (Junction)

Source: P2. New entity. Handles co-tenancy (shared meters).

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| water_meter_id | FK → WaterMeter | NOT NULL | |
| tenant_id | FK → Tenant | NOT NULL | |
| lease_id | FK → Lease | NOT NULL | |
| share_pct | decimal(5,2) | DEFAULT 100.00 | For shared meters |
| effective_from | date | NOT NULL | |
| effective_to | date | | |

### 2.7 WaterMeterReading

Source: P2. New entity. Manual entry point.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| water_meter_id | FK → WaterMeter | NOT NULL | |
| reading_date | date | NOT NULL | |
| reading_value | decimal(10,2) | NOT NULL | Cubic meters |
| is_estimated | boolean | DEFAULT false | Defective meter flag |
| entered_by | text | | User who entered |
| created_at | timestamp | NOT NULL | |

**Constraint:** Consumption = current reading − previous reading. If negative → rollover handling.

### 2.8 MayniladBill

Source: P2. New entity. Manual entry from paper/PDF.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| billing_period_start | date | NOT NULL | |
| billing_period_end | date | NOT NULL | |
| total_amount | decimal(10,2) | NOT NULL | Master meter total |
| total_consumption_cu_m | decimal(10,2) | NOT NULL | |
| bill_components | jsonb | NOT NULL | Breakdown: basic, env charge, sewerage, FCDA, MSC, VAT |
| due_date | date | | |
| created_at | timestamp | NOT NULL | |

### 2.9 MayniladRateSchedule

Source: P2. New entity. Updated quarterly (FCDA).

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| effective_date | date | NOT NULL | |
| tiers | jsonb | NOT NULL | Array of {min_cu_m, max_cu_m, rate_per_cu_m} |
| environmental_charge_pct | decimal(5,2) | NOT NULL | e.g., 0.25 (25% of basic) |
| sewerage_charge_pct | decimal(5,2) | NOT NULL | e.g., 0.20 (20% of basic, commercial only) |
| fcda_rate | decimal(8,4) | | Quarterly adjustment |
| msc | decimal(10,2) | | Minimum Service Charge |
| notes | text | | |

### 2.10 WaterBillingRun

Source: P2. New entity. Batch computation.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| maynilad_bill_id | FK → MayniladBill | NOT NULL | |
| billing_period | text | NOT NULL | e.g., "2026-03" |
| status | ENUM('DRAFT', 'FINALIZED') | NOT NULL | |
| total_billed | decimal(10,2) | | Sum of all water charges |
| reconciliation_diff | decimal(10,2) | | total_billed − maynilad_bill.total_amount |
| created_at | timestamp | NOT NULL | |
| finalized_at | timestamp | | |

**Constraint:** total_billed ≤ maynilad_bill.total_amount (no markup).

### 2.11 WaterCharge

Source: P2. New entity. Per-tenant water charge.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| water_billing_run_id | FK → WaterBillingRun | NOT NULL | |
| tenant_id | FK → Tenant | NOT NULL | |
| lease_id | FK → Lease | NOT NULL | |
| water_meter_id | FK → WaterMeter | NOT NULL | |
| consumption_cu_m | decimal(10,2) | NOT NULL | |
| tier_breakdown | jsonb | NOT NULL | Per-tier: {tier, cu_m, rate, amount} |
| basic_charge | decimal(10,2) | NOT NULL | |
| environmental_charge | decimal(10,2) | NOT NULL | |
| sewerage_charge | decimal(10,2) | DEFAULT 0 | Commercial only |
| common_area_share | decimal(10,2) | DEFAULT 0 | Floor area or equal split |
| total_charge | decimal(10,2) | NOT NULL | |
| charge_id | FK → Charge | | Created when finalized → becomes a Charge |

### 2.12 ElectricMeter

Source: P3. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| meter_identifier | text | UNIQUE, NOT NULL | |
| meter_type | ENUM('SUB_METER', 'COMMON_AREA', 'MASTER') | NOT NULL | |
| is_active | boolean | DEFAULT true | |

### 2.13 ElectricMeterTenant (Junction)

Source: P3. New entity. Handles shared meters.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| electric_meter_id | FK → ElectricMeter | NOT NULL | |
| tenant_id | FK → Tenant | NOT NULL | |
| lease_id | FK → Lease | NOT NULL | |
| share_pct | decimal(5,2) | DEFAULT 100.00 | |
| effective_from | date | NOT NULL | |
| effective_to | date | | |

### 2.14 ElectricMeterReading

Source: P3. New entity. Manual entry point.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| electric_meter_id | FK → ElectricMeter | NOT NULL | |
| reading_date | date | NOT NULL | |
| reading_value | decimal(12,2) | NOT NULL | kWh |
| is_estimated | boolean | DEFAULT false | |
| entered_by | text | | |
| created_at | timestamp | NOT NULL | |

### 2.15 MeralcoBill

Source: P3. New entity. Manual entry from paper/online.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| billing_period_start | date | NOT NULL | |
| billing_period_end | date | NOT NULL | |
| total_amount | decimal(12,2) | NOT NULL | |
| total_kwh | decimal(12,2) | NOT NULL | |
| bill_components | jsonb | | Meralco component breakdown |
| effective_rate_per_kwh | decimal(8,4) | GENERATED | total_amount / total_kwh |
| due_date | date | | |
| created_at | timestamp | NOT NULL | |

### 2.16 ElectricBillingRun

Source: P3. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| meralco_bill_id | FK → MeralcoBill | NOT NULL | |
| billing_period | text | NOT NULL | |
| status | ENUM('DRAFT', 'FINALIZED') | NOT NULL | |
| blended_rate | decimal(8,4) | NOT NULL | total_bill / total_kwh |
| admin_fee_per_kwh | decimal(6,4) | DEFAULT 0 | Configurable, ≤ PHP 1.50 |
| total_billed | decimal(12,2) | | |
| reconciliation_diff | decimal(12,2) | | |
| created_at | timestamp | NOT NULL | |
| finalized_at | timestamp | | |

### 2.17 ElectricCharge

Source: P3. New entity. Per-tenant electric charge.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| electric_billing_run_id | FK → ElectricBillingRun | NOT NULL | |
| tenant_id | FK → Tenant | NOT NULL | |
| lease_id | FK → Lease | NOT NULL | |
| electric_meter_id | FK → ElectricMeter | NOT NULL | |
| consumption_kwh | decimal(12,2) | NOT NULL | |
| blended_rate | decimal(8,4) | NOT NULL | Frozen from run |
| base_charge | decimal(10,2) | NOT NULL | consumption × blended_rate |
| admin_fee | decimal(10,2) | DEFAULT 0 | consumption × admin_fee_per_kwh |
| common_area_share | decimal(10,2) | DEFAULT 0 | |
| vat_treatment | ENUM('VATABLE', 'EXEMPT', 'PENDING') | NOT NULL | CONFLICTING rule — see P3 |
| total_charge | decimal(12,2) | NOT NULL | |
| charge_id | FK → Charge | | Created when finalized |

### 2.18 PenaltyLedger

Source: P4. New entity. Audit trail per penalty computation.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| tenant_id | FK → Tenant | NOT NULL | |
| billing_period | text | NOT NULL | |
| overdue_amount | decimal(10,2) | NOT NULL | Base for penalty |
| rate_applied | decimal(5,4) | NOT NULL | Monthly rate used |
| raw_penalty | decimal(10,2) | NOT NULL | Before caps |
| cap_applied | boolean | DEFAULT false | |
| final_penalty | decimal(10,2) | NOT NULL | After caps |
| ytd_penalty_total | decimal(10,2) | NOT NULL | Year-to-date total for cap check |
| demand_record_id | FK → DemandRecord | | Null = no demand (legal interest may not run) |
| charge_id | FK → Charge | | The Charge created |
| created_at | timestamp | NOT NULL | |
| notes | text | | |

**Constraints (controlled residential):** rate ≤ 1%/month; ytd_penalty_total ≤ 1 month's rent.

### 2.19 DemandRecord

Source: P4. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| tenant_id | FK → Tenant | NOT NULL | |
| date_sent | date | NOT NULL | |
| method | ENUM('LETTER', 'EMAIL', 'PERSONAL') | NOT NULL | |
| arrears_at_demand | decimal(10,2) | NOT NULL | Total outstanding at demand date |
| months_in_arrears | integer | NOT NULL | |
| notes | text | | |
| created_at | timestamp | NOT NULL | |

### 2.20 BillingRun

Source: P5. New entity. Monthly billing batch.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| billing_period | text | NOT NULL | e.g., "2026-03" |
| run_type | ENUM('BATCH', 'INDIVIDUAL') | NOT NULL | |
| status | ENUM('DRAFT', 'FINALIZED') | NOT NULL | |
| total_charges | decimal(12,2) | | |
| total_vat | decimal(12,2) | | |
| charge_count | integer | | |
| created_at | timestamp | NOT NULL | |
| finalized_at | timestamp | | |

### 2.21 Charge

Source: P1-P5, P7. Existing Crispina entity, enhanced.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| tenant_id | FK → Tenant | NOT NULL | |
| charge_type_id | FK → ChargeType | NOT NULL | |
| billing_run_id | FK → BillingRun | | NULL for non-batch charges |
| billing_period | text | NOT NULL | |
| base_amount | decimal(10,2) | NOT NULL | Before VAT |
| vat_rate | decimal(4,2) | NOT NULL | Frozen at creation |
| vat_amount | decimal(10,2) | NOT NULL | GENERATED or computed |
| total_amount | decimal(10,2) | NOT NULL | base + vat |
| **invoice_number** | text | | **New** — sequential, ATP-managed (P5, P13) |
| **invoice_date** | date | | **New** — accrual date (P5) |
| **is_vat_exempt** | boolean | NOT NULL, DEFAULT false | **New** — residential ≤ PHP 15K (P5) |
| due_date | date | NOT NULL | |
| status | ENUM('DRAFT', 'FINALIZED', 'PAID', 'PARTIALLY_PAID', 'CREDITED') | NOT NULL | |
| description | text | | Human-readable line item |
| created_at | timestamp | NOT NULL | |

### 2.22 CreditMemo

Source: P5. New entity. Cannot void BIR invoice — issue credit memo instead.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| original_charge_id | FK → Charge | NOT NULL | |
| credit_memo_number | text | UNIQUE, NOT NULL | Separate sequential series |
| date_issued | date | NOT NULL | |
| amount | decimal(10,2) | NOT NULL | |
| vat_amount | decimal(10,2) | NOT NULL | |
| reason | text | NOT NULL | |
| created_at | timestamp | NOT NULL | |

---

## 3. Collection Entities

### 3.1 Payment

Source: P6. Existing Crispina entity, enhanced.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| tenant_id | FK → Tenant | NOT NULL | |
| amount | decimal(10,2) | NOT NULL | Total payment received |
| date_issued | date | NOT NULL | |
| reference_number | text | | Check#, transfer ref, etc. |
| **payment_method** | ENUM('CASH', 'CHECK', 'BANK_TRANSFER', 'GCASH', 'OTHER') | NOT NULL | **New** |
| **or_number** | text | | **New** — Official Receipt number (P6, P13) |
| **deposited_date** | date | | **New** — date deposited to bank |
| **remarks** | text | | **New** — tenant designation per Art. 1252 |
| **ewt_withheld** | decimal(10,2) | DEFAULT 0 | **New** — EWT amount if corporate tenant |
| created_at | timestamp | NOT NULL | |

### 3.2 PaymentAllocation

Source: P6. Existing Crispina entity, enhanced.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| payment_id | FK → Payment | NOT NULL | |
| **charge_id** | FK → Charge | NOT NULL | **Enhanced** — charge-level (was transaction-level) |
| amount | decimal(10,2) | NOT NULL | Amount allocated to this charge |
| allocation_rule | ENUM('TENANT_DESIGNATED', 'ART_1253_PENALTY_FIRST', 'ART_1254_MOST_ONEROUS', 'FIFO') | | |
| created_at | timestamp | NOT NULL | |

### 3.3 PaymentEvent

Source: P6. New entity. Audit log.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| payment_id | FK → Payment | NOT NULL | |
| event_type | ENUM('CREATED', 'ALLOCATED', 'REVERSED', 'BOUNCED') | NOT NULL | |
| details | jsonb | | |
| created_by | text | | |
| created_at | timestamp | NOT NULL | |

### 3.4 TenantBalance (Materialized View)

Source: P6. New. Derived from Charge + Payment + PaymentAllocation.

| Column | Type | Notes |
|--------|------|-------|
| tenant_id | FK → Tenant | PK |
| total_billed | decimal(12,2) | Sum of all charges |
| total_paid | decimal(12,2) | Sum of all payments |
| total_ewt | decimal(12,2) | Sum of all EWT withheld |
| balance | decimal(12,2) | total_billed − total_paid − total_ewt |
| oldest_unpaid_date | date | Oldest charge with remaining balance |
| months_in_arrears | integer | Count of unpaid monthly periods |
| arrears_alert | boolean | True if months_in_arrears ≥ 3 (controlled) |
| last_payment_date | date | |
| last_refreshed | timestamp | |

### 3.5 SecurityDeposit

Source: P7. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| tenant_id | FK → Tenant | NOT NULL | |
| amount | decimal(10,2) | NOT NULL | |
| date_collected | date | NOT NULL | |
| bank_reference | text | | Required for controlled residential |
| lease_regime | ENUM | NOT NULL | CONTROLLED_RESIDENTIAL / COMMERCIAL |
| status | ENUM('HELD', 'PARTIALLY_APPLIED', 'FULLY_APPLIED', 'REFUNDED') | NOT NULL | |
| created_at | timestamp | NOT NULL | |

**Constraint (controlled residential):** amount ≤ 2 × monthly_rent.

### 3.6 DepositInterestAccrual

Source: P7. New entity. For controlled residential (mandatory bank interest return).

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| security_deposit_id | FK → SecurityDeposit | NOT NULL | |
| accrual_period | text | NOT NULL | e.g., "2026-Q1" |
| interest_rate | decimal(6,4) | NOT NULL | From bank passbook |
| interest_amount | decimal(10,2) | NOT NULL | |
| created_at | timestamp | NOT NULL | |

### 3.7 DepositDeduction

Source: P7. New entity. Itemized deductions at lease end.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| security_deposit_id | FK → SecurityDeposit | NOT NULL | |
| description | text | NOT NULL | e.g., "Broken window pane — Unit 201" |
| amount | decimal(10,2) | NOT NULL | |
| supporting_doc_ref | text | | Receipt/quotation reference |
| created_at | timestamp | NOT NULL | |

**Constraint:** "Automatic forfeiture" clauses are void (Art. 1306/1409). Deductions must be itemized.

### 3.8 DepositApplication

Source: P7. New entity. Tax reclassification when deposit becomes income.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| security_deposit_id | FK → SecurityDeposit | NOT NULL | |
| application_date | date | NOT NULL | |
| amount_applied | decimal(10,2) | NOT NULL | |
| vat_amount | decimal(10,2) | NOT NULL | 12% if VAT-registered + rent > PHP 15K |
| ewt_amount | decimal(10,2) | NOT NULL | 5% EWT |
| charge_id | FK → Charge | | Corresponding income charge created |
| created_at | timestamp | NOT NULL | |

### 3.9 DepositRefund

Source: P7. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| security_deposit_id | FK → SecurityDeposit | NOT NULL | |
| refund_amount | decimal(10,2) | NOT NULL | deposit − deductions + interest (controlled) |
| refund_method | ENUM('CASH', 'CHECK', 'BANK_TRANSFER') | NOT NULL | |
| refund_date | date | | |
| deadline_date | date | NOT NULL | 1 month from lease expiry + turnover (controlled) |
| is_overdue | boolean | GENERATED | refund_date IS NULL AND current_date > deadline_date |
| penalty_interest_rate | decimal(5,4) | DEFAULT 0.06 | 6% p.a. legal interest if overdue |
| created_at | timestamp | NOT NULL | |

---

## 4. Contract Entities

### 4.1 LeaseTemplate

Source: P8. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| name | text | NOT NULL | |
| unit_type | ENUM('RESIDENTIAL', 'COMMERCIAL') | NOT NULL | |
| template_content | text | NOT NULL | Markdown/HTML with {{variables}} |
| is_active | boolean | DEFAULT true | |
| created_at | timestamp | NOT NULL | |
| updated_at | timestamp | NOT NULL | |

### 4.2 LeaseClause

Source: P8. New entity. Clause library.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| code | text | UNIQUE, NOT NULL | e.g., "RA9653_DEPOSIT_CAP" |
| title | text | NOT NULL | |
| content | text | NOT NULL | Clause text |
| is_mandatory | boolean | NOT NULL | |
| applicable_regime | ENUM('CONTROLLED_RESIDENTIAL', 'COMMERCIAL', 'ALL') | NOT NULL | |
| sort_order | integer | | |

### 4.3 BoardResolution

Source: P8. New entity. For corporate tenants.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| tenant_id | FK → Tenant | NOT NULL | |
| resolution_number | text | NOT NULL | |
| resolution_date | date | NOT NULL | |
| scope | text | NOT NULL | e.g., "Authorize lease of Unit 201" |
| authorized_signatory | text | NOT NULL | |
| secretary_certificate_date | date | | |
| created_at | timestamp | NOT NULL | |

### 4.4 LeaseExecutionMilestone

Source: P8. New entity. Track contract execution stages.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| milestone | ENUM('DRAFT', 'SIGNED', 'NOTARIZED', 'REGISTERED', 'DST_FILED') | NOT NULL | |
| date_completed | date | | |
| notes | text | | |
| created_at | timestamp | NOT NULL | |
| | | UNIQUE(lease_id, milestone) | |

### 4.5 DSTComputation

Source: P8, P9. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| annual_rent | decimal(12,2) | NOT NULL | |
| lease_term_years | decimal(4,1) | NOT NULL | |
| dst_amount | decimal(10,2) | NOT NULL | PHP 6 on first PHP 2K + PHP 2 per add'l PHP 1K × years |
| form_2000_filing_date | date | | Within 5 days after close of month of execution |
| is_filed | boolean | DEFAULT false | |
| created_at | timestamp | NOT NULL | |

### 4.6 LeaseEvent

Source: P8, P9, P10. New entity. Audit log for lease lifecycle.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| event_type | ENUM('CREATED', 'ACTIVATED', 'EXPIRED', 'RENEWED', 'RECONDUCTION_STARTED', 'TERMINATED', 'NOTICE_SENT', 'ANNIVERSARY') | NOT NULL | |
| event_date | date | NOT NULL | |
| details | jsonb | | Additional context |
| created_by | text | | |
| created_at | timestamp | NOT NULL | |

### 4.7 NonRenewalNotice

Source: P9. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| lease_id | FK → Lease | NOT NULL | |
| date_sent | date | NOT NULL | |
| method | ENUM('LETTER', 'EMAIL', 'PERSONAL') | NOT NULL | |
| is_within_deadline | boolean | NOT NULL | Must be within 15 days before expiry (Art. 1670) |
| notes | text | | |
| created_at | timestamp | NOT NULL | |

---

## 5. Handoff / Reporting Entities

### 5.1 Form2307Record

Source: P6, P11. New entity. Track expected → received → reconciled.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| tenant_id | FK → Tenant | NOT NULL | Corporate tenants only |
| quarter | text | NOT NULL | e.g., "2026-Q1" |
| expected_amount | decimal(10,2) | NOT NULL | 5% of base rent billed |
| received_date | date | | |
| received_amount | decimal(10,2) | | |
| is_reconciled | boolean | DEFAULT false | |
| delivered_to_accountant_date | date | | |
| notes | text | | |
| created_at | timestamp | NOT NULL | |

### 5.2 RentRollReport

Source: P11. New entity. Monthly snapshot.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| billing_period | text | NOT NULL | e.g., "2026-03" |
| generated_at | timestamp | NOT NULL | |
| report_data | jsonb | NOT NULL | 26-column rows per tenant |
| total_billed | decimal(12,2) | NOT NULL | |
| total_collected | decimal(12,2) | NOT NULL | |
| total_outstanding | decimal(12,2) | NOT NULL | |

**26 columns:** Tenant, TIN, Unit, Type, Lease Term, Monthly Rate, Escalation Date, VAT Status, Gross Rent Billed (base), VAT Billed, Total Billed, Amount Collected (cash), EWT Withheld, Net Collected, Prior Balance, Current Balance, Invoice#, Receipt#, 2307 Status, Deposit Held, Lease Status, Days Overdue, Notes, LIS Flag, SAWT Flag, Adjustment Flag

### 5.3 LISReport

Source: P11. New entity. Semi-annual (RR 12-2011).

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| semester | text | NOT NULL | e.g., "2026-H1" |
| generated_at | timestamp | NOT NULL | |
| report_data | jsonb | NOT NULL | 9 prescribed columns per payor |
| filing_deadline | date | NOT NULL | Jul 15 / Jan 15 |
| is_filed | boolean | DEFAULT false | |

### 5.4 OutputVATSummary

Source: P12. New entity. Quarterly.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| quarter | text | NOT NULL | |
| vatable_sales | decimal(12,2) | NOT NULL | |
| exempt_sales | decimal(12,2) | NOT NULL | |
| zero_rated_sales | decimal(12,2) | DEFAULT 0 | |
| output_vat | decimal(12,2) | NOT NULL | |
| input_vat | decimal(12,2) | NOT NULL | From P14 |
| net_vat_payable | decimal(12,2) | NOT NULL | |
| uncollected_adjustment | decimal(12,2) | DEFAULT 0 | RR 3-2024 |
| generated_at | timestamp | NOT NULL | |

### 5.5 IncomeTaxQuarterlyData

Source: P12. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| quarter | text | NOT NULL | |
| gross_rental_income | decimal(12,2) | NOT NULL | |
| other_income | decimal(12,2) | DEFAULT 0 | Penalties, deposit forfeitures, etc. |
| deductible_expenses | decimal(12,2) | NOT NULL | From P14 |
| taxable_income | decimal(12,2) | NOT NULL | |
| ewt_credits | decimal(12,2) | NOT NULL | From 2307s |
| generated_at | timestamp | NOT NULL | |

### 5.6 SAWTRecord

Source: P12. New entity. From collected 2307s.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| form_2307_id | FK → Form2307Record | NOT NULL | |
| quarter | text | NOT NULL | |
| payor_tin | text | NOT NULL | |
| payor_name | text | NOT NULL | |
| income_payment | decimal(10,2) | NOT NULL | |
| tax_withheld | decimal(10,2) | NOT NULL | |
| atc_code | text | NOT NULL | e.g., "WC157" |

### 5.7 EWTWithheldSummary

Source: P12. New entity. On supplier payments.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| period | text | NOT NULL | Monthly or quarterly |
| total_payments | decimal(12,2) | NOT NULL | |
| total_ewt_withheld | decimal(12,2) | NOT NULL | |
| form_filed | text | | 0619-E / 1601-EQ / 1604-E |
| generated_at | timestamp | NOT NULL | |

### 5.8 DSTRegister

Source: P12. New entity. Per lease execution.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| dst_computation_id | FK → DSTComputation | NOT NULL | |
| lease_id | FK → Lease | NOT NULL | |
| event_type | ENUM('NEW_LEASE', 'RENEWAL', 'EXTENSION') | NOT NULL | |
| dst_amount | decimal(10,2) | NOT NULL | |
| form_2000_number | text | | |
| filing_date | date | | |
| filing_deadline | date | NOT NULL | |
| is_filed | boolean | DEFAULT false | |

### 5.9 DocumentSequence

Source: P13. New entity. Centralized sequential numbering.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| document_type | ENUM('INVOICE', 'RECEIPT', 'CREDIT_MEMO') | NOT NULL | |
| property_id | FK → Property | NOT NULL | Per establishment |
| current_number | bigint | NOT NULL | Atomic increment |
| prefix | text | NOT NULL | e.g., "INV-", "OR-", "CM-" |
| atp_id | FK → AuthorityToPrint | | |
| series_start | bigint | NOT NULL | |
| series_end | bigint | NOT NULL | |
| | | UNIQUE(document_type, property_id) | |

**Implementation:** PostgreSQL `UPDATE document_sequence SET current_number = current_number + 1 ... RETURNING current_number` for atomic, gapless increment.

### 5.10 AuthorityToPrint

Source: P13. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| atp_number | text | UNIQUE, NOT NULL | |
| document_type | ENUM('INVOICE', 'RECEIPT', 'CREDIT_MEMO') | NOT NULL | |
| valid_from | date | NOT NULL | |
| valid_to | date | | Conflicting — may not expire |
| series_start | bigint | NOT NULL | |
| series_end | bigint | NOT NULL | |
| printer_name | text | NOT NULL | BIR-accredited printer |
| printer_tin | text | NOT NULL | |
| utilization_pct | decimal(5,2) | GENERATED | (used / total) × 100 |
| created_at | timestamp | NOT NULL | |

**Alerts:** At 80%, 90%, 100% utilization.

### 5.11 IssuedDocument

Source: P13. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| document_type | ENUM('INVOICE', 'RECEIPT') | NOT NULL | |
| document_number | text | UNIQUE, NOT NULL | Sequential |
| date_issued | date | NOT NULL | |
| tenant_id | FK → Tenant | NOT NULL | |
| lease_id | FK → Lease | | |
| total_amount | decimal(12,2) | NOT NULL | |
| vat_amount | decimal(12,2) | NOT NULL | |
| atp_id | FK → AuthorityToPrint | NOT NULL | |
| charge_id | FK → Charge | | Invoice → at billing |
| payment_id | FK → Payment | | Receipt → at payment |
| created_at | timestamp | NOT NULL | |

**16 mandatory fields per RR 7-2024:** lessor TIN, lessor name, lessor address, invoice/receipt number, date, ATP number, tenant TIN, tenant name, tenant address, description, quantity, unit price, amount, VAT amount, total amount, authorized signatory.

### 5.12 IssuedDocumentLine

Source: P13. New entity. Line items on invoice/receipt.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| issued_document_id | FK → IssuedDocument | NOT NULL | |
| description | text | NOT NULL | |
| quantity | decimal(10,2) | DEFAULT 1 | |
| unit_price | decimal(10,2) | NOT NULL | |
| amount | decimal(10,2) | NOT NULL | |
| vat_amount | decimal(10,2) | NOT NULL | |
| charge_id | FK → Charge | | Link to specific charge |

### 5.13 SupplierPayee

Source: P14. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| tin | text | | Supplier TIN |
| name | text | NOT NULL | |
| address | text | | |
| payee_type | ENUM('INDIVIDUAL', 'CORPORATE') | NOT NULL | |
| is_vat_registered | boolean | NOT NULL, DEFAULT false | |
| is_large_taxpayer | boolean | NOT NULL, DEFAULT false | |
| created_at | timestamp | NOT NULL | |

### 5.14 ExpenseCategory

Source: P14. New entity. Seed data — 14+ BIR ATC categories.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| code | text | UNIQUE, NOT NULL | ATC code |
| name | text | NOT NULL | |
| ewt_rate_individual | decimal(4,2) | NOT NULL | |
| ewt_rate_corporate | decimal(4,2) | NOT NULL | |
| is_deductible | boolean | NOT NULL, DEFAULT true | |
| is_depreciable | boolean | NOT NULL, DEFAULT false | |

### 5.15 DisbursementVoucher

Source: P14. New entity. Record of each expense payment.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| supplier_id | FK → SupplierPayee | NOT NULL | |
| expense_category_id | FK → ExpenseCategory | NOT NULL | |
| date_paid | date | NOT NULL | |
| description | text | NOT NULL | |
| gross_amount | decimal(10,2) | NOT NULL | |
| vat_amount | decimal(10,2) | NOT NULL | |
| ewt_withheld | decimal(10,2) | NOT NULL | Auto-computed from category × payee type |
| net_payment | decimal(10,2) | NOT NULL | gross − ewt + vat |
| supporting_doc_ref | text | | OR/invoice from supplier |
| form_2307_issued | boolean | DEFAULT false | 2307 issued to this supplier |
| form_2307_date | date | | |
| created_at | timestamp | NOT NULL | |

### 5.16 InputVATRegister

Source: P14. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| disbursement_voucher_id | FK → DisbursementVoucher | NOT NULL | |
| supplier_tin | text | NOT NULL | |
| invoice_number | text | | Supplier's invoice # |
| invoice_date | date | NOT NULL | |
| vat_amount | decimal(10,2) | NOT NULL | |
| is_creditable | boolean | NOT NULL | Only from VAT-registered suppliers |
| apportionment_pct | decimal(5,2) | | Mixed-operation (VATable ÷ total revenue) |
| creditable_amount | decimal(10,2) | NOT NULL | vat_amount × apportionment_pct (if mixed) |
| quarter | text | NOT NULL | For 2550Q filing |

### 5.17 EWTWithheldRegister

Source: P14. New entity. EWT withheld on supplier payments.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| disbursement_voucher_id | FK → DisbursementVoucher | NOT NULL | |
| supplier_id | FK → SupplierPayee | NOT NULL | |
| atc_code | text | NOT NULL | |
| income_payment | decimal(10,2) | NOT NULL | |
| ewt_amount | decimal(10,2) | NOT NULL | |
| period | text | NOT NULL | Monthly for 0619-E |

### 5.18 FixedAssetRegister

Source: P14. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| property_id | FK → Property | NOT NULL | |
| disbursement_voucher_id | FK → DisbursementVoucher | | |
| description | text | NOT NULL | |
| date_acquired | date | NOT NULL | |
| cost | decimal(12,2) | NOT NULL | |
| useful_life_months | integer | NOT NULL | No BIR-prescribed life |
| residual_value | decimal(12,2) | NOT NULL | 5% floor |
| accumulated_depreciation | decimal(12,2) | DEFAULT 0 | |
| net_book_value | decimal(12,2) | GENERATED | cost − accumulated_depreciation |
| status | ENUM('ACTIVE', 'DISPOSED', 'FULLY_DEPRECIATED') | NOT NULL | |

**Constraint:** Capital goods > PHP 1M → input VAT amortized over 60 months.

### 5.19 DepreciationScheduleEntry

Source: P14. New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| fixed_asset_id | FK → FixedAssetRegister | NOT NULL | |
| period | text | NOT NULL | Monthly |
| depreciation_amount | decimal(10,2) | NOT NULL | |
| accumulated_total | decimal(12,2) | NOT NULL | |

---

## 6. Cross-Cutting Entities

### 6.1 ComplianceObligation

Source: Compliance calendar (Section 9 of process catalog). New entity.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| code | text | UNIQUE, NOT NULL | e.g., "BIR_0619E_MONTHLY" |
| name | text | NOT NULL | |
| description | text | | |
| frequency | ENUM('MONTHLY', 'QUARTERLY', 'SEMI_ANNUAL', 'ANNUAL', 'EVENT_DRIVEN') | NOT NULL | |
| regulator | ENUM('BIR', 'SEC', 'LGU', 'OTHER') | NOT NULL | |
| form_number | text | | e.g., "0619-E", "2550Q" |
| data_source_processes | text[] | | e.g., ["P14", "P12"] |
| deadline_rule | jsonb | NOT NULL | e.g., {"day": 10, "relative_to": "month_end"} |
| is_active | boolean | DEFAULT true | |

### 6.2 ComplianceDeadline (Instance)

Generated from ComplianceObligation for each period.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | uuid / serial | PK | |
| obligation_id | FK → ComplianceObligation | NOT NULL | |
| period | text | NOT NULL | e.g., "2026-03", "2026-Q1" |
| deadline_date | date | NOT NULL | |
| status | ENUM('UPCOMING', 'IN_PROGRESS', 'FILED', 'OVERDUE') | NOT NULL | |
| alert_level | ENUM('INFO', 'WARNING', 'URGENT', 'OVERDUE') | GENERATED | Based on days until deadline |
| filed_date | date | | |
| notes | text | | |

---

## 7. Relationship Summary

### Key Foreign Key Chains

```
Property → Rentable → LeaseRentable → Lease → Tenant
                                         ↓
                                    Charge → PaymentAllocation → Payment
                                         ↓
                                    IssuedDocument (Invoice/Receipt)
```

### Many-to-Many Relationships

| Junction Table | Left Entity | Right Entity | Notes |
|---------------|-------------|--------------|-------|
| LeaseRentable | Lease | Rentable | One lease can cover multiple units |
| WaterMeterTenant | WaterMeter | Tenant/Lease | Shared meters with % split |
| ElectricMeterTenant | ElectricMeter | Tenant/Lease | Shared meters with % split |
| PaymentAllocation | Payment | Charge | One payment → multiple charges |

### Renewal Chain

```
Lease(original) ← Lease(renewal1) ← Lease(renewal2)
  └── original_lease_id = NULL    └── original_lease_id = renewal1.id
```

### Entity Counts

| Category | New Entities | Enhanced Existing | Total |
|----------|:-----------:|:-----------------:|:-----:|
| Foundation | 0 | 5 (Rentable, Tenant, Lease, Charge, ChargeType) | 7 |
| Billing | 16 | 0 | 16 |
| Collection | 8 | 2 (Payment, PaymentAllocation) | 10 |
| Contracts | 7 | 0 | 7 |
| Handoff/Reporting | 18 | 0 | 18 |
| Cross-cutting | 2 | 0 | 2 |
| **Total** | **51** | **7** | **60+** |

---

## 8. Decimal Handling & Rounding Rules

Source: Cross-cutting concerns, P1, P2, P3.

| Context | Rule | Source |
|---------|------|--------|
| Monetary amounts | decimal(10,2) minimum; decimal(12,2) for aggregates | All |
| Rent escalation | ROUND_DOWN (truncate) | P1 (Crispina `math.py`) |
| Water per-tier billing | Round to 2 decimal places | P2 |
| Electric blended rate | 4 decimal places for rate, round charge to 2 | P3 |
| VAT computation | base_amount × vat_rate, round to 2 | All |
| EWT computation | base_amount × ewt_rate, round to 2 | P6, P14 |
| DST computation | PHP 6 on first PHP 2K + PHP 2 per additional PHP 1K × years | P8 |

**PostgreSQL type:** Use `numeric(p,s)` (arbitrary precision) not `float` or `double`. Drizzle ORM maps this to string-based decimal.

---

## 9. Enumeration Summary

| Enum Name | Values | Used By |
|-----------|--------|---------|
| UnitType | RESIDENTIAL, COMMERCIAL | Rentable |
| LeaseStatus | DRAFT, ACTIVE, EXPIRED, MONTH_TO_MONTH, HOLDOVER, TERMINATED, RENEWED | Lease |
| LeaseRegime | CONTROLLED_RESIDENTIAL, NON_CONTROLLED_RESIDENTIAL, COMMERCIAL | Lease, SecurityDeposit |
| EscalationType | NHSB_CAP, FIXED_PCT, STEPPED, CPI_LINKED, NONE | Lease |
| MeterType | SUB_METER, COMMON_AREA, MASTER | WaterMeter, ElectricMeter |
| BillingRunStatus | DRAFT, FINALIZED | BillingRun, WaterBillingRun, ElectricBillingRun |
| ChargeStatus | DRAFT, FINALIZED, PAID, PARTIALLY_PAID, CREDITED | Charge |
| PaymentMethod | CASH, CHECK, BANK_TRANSFER, GCASH, OTHER | Payment |
| AllocationRule | TENANT_DESIGNATED, ART_1253_PENALTY_FIRST, ART_1254_MOST_ONEROUS, FIFO | PaymentAllocation |
| DepositStatus | HELD, PARTIALLY_APPLIED, FULLY_APPLIED, REFUNDED | SecurityDeposit |
| DocumentType | INVOICE, RECEIPT, CREDIT_MEMO | DocumentSequence, IssuedDocument |
| LeaseEventType | CREATED, ACTIVATED, EXPIRED, RENEWED, RECONDUCTION_STARTED, TERMINATED, NOTICE_SENT, ANNIVERSARY | LeaseEvent |
| LeaseExecMilestone | DRAFT, SIGNED, NOTARIZED, REGISTERED, DST_FILED | LeaseExecutionMilestone |
| PayeeType | INDIVIDUAL, CORPORATE | SupplierPayee |
| ComplianceFrequency | MONTHLY, QUARTERLY, SEMI_ANNUAL, ANNUAL, EVENT_DRIVEN | ComplianceObligation |
| AlertLevel | INFO, WARNING, URGENT, OVERDUE | ComplianceDeadline |
| VATTreatment | VATABLE, EXEMPT, PENDING | ElectricCharge (conflicting rule) |
| DSTEventType | NEW_LEASE, RENEWAL, EXTENSION | DSTRegister |
| FixedAssetStatus | ACTIVE, DISPOSED, FULLY_DEPRECIATED | FixedAssetRegister |
| PaymentEventType | CREATED, ALLOCATED, REVERSED, BOUNCED | PaymentEvent |
| DemandMethod | LETTER, EMAIL, PERSONAL | DemandRecord, NonRenewalNotice |

---

*Extracted: 2026-03-02 | 65 entities, 20 enums, ~300 fields | Ready for Wave 2 database-schema aspect*
