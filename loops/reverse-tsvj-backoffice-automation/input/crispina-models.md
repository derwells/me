# Crispina Codebase — Database Models & API Schemas

Extracted from `tsvjph/crispina` repo, commit: main branch (Feb 2026).

---

## Repository Structure

```
server/
  src/
    db/model/         ← SQLAlchemy ORM models (source of truth for data shapes)
    api/schema/       ← Pydantic schemas (API input/output shapes)
    script/seed.py    ← Initial seed data (reveals intended charge types)
water/                ← Standalone water billing calculator (separate aspect)
```

---

## Data Model Overview

### Hierarchy: Property → Room → Rentable

```
Property (building)
  └─ Room (physical walled space, e.g., "Unit 101")
       └─ Rentable (leasable unit within a room)
            └─ If not subdivided: Rentable.name = NULL (whole room is one unit)
            └─ If subdivided: Rentable.name = "A", "B", "C" (sub-units)
```

**Property** (`server/src/db/model/property.py`):
- `pk` (UUID)
- `name` (String 255)
- `address` (String 255) — single string, not structured
- `miscellaneous` (JSONB, default `{}`) — flexible extra fields
- → rooms (relationship to Room)

**Room** (`server/src/db/model/room.py`):
- `pk`, `name`, `miscellaneous` (JSONB)
- `max_subdivisions` (Integer, default 1)
- `is_subdivided` (Boolean, default False)
- → property (FK → Property)
- → rentables (relationship to Rentable)

**Rentable** (`server/src/db/model/rentable.py`):
- `pk`
- `name` (String 255, **nullable** — null when room is NOT subdivided)
- `miscellaneous` (JSONB)
- → room (FK → Room)
- → leases (M2M via lease_rentable, viewonly)
- → charges (O2M → Charge)

**Seed example:**
- TSVJ Center, Crispina Avenue, Pamplona 3, Las Pinas City → Unit 101 (not subdivided) + Unit 102 (subdivided into A, B, C, D)
- ABCD Land, Quezon City → Unit 101 (not subdivided)

---

### Tenant

**Tenant** (`server/src/db/model/tenant.py`):
- `pk`, `first_name`, `last_name`
- `billing_name` (String 255, nullable) — used for corporate tenants paying under company name (e.g., "ACME Inc.")
- `email`, `mobile_number` (both nullable)
- `miscellaneous` (JSONB) — flexible extra fields
- Hybrid property: `full_name` = `f"{first_name} {last_name}"`
- → leases, charges, payments (relationships)

**Missing fields for PH compliance:**
- No `tin` (BIR Tax Identification Number) — needed for 2307, official receipts
- No `is_corporate` flag — determines EWT applicability
- No `is_vat_registered` flag — affects invoice/receipt format
- No `is_rent_controlled` flag on tenant or rentable
- No `unit_floor_area_sqm` on Rentable — needed for electric apportionment

---

### Lease & Recurring Charges

**Lease** (`server/src/db/model/lease.py`):
- `pk`, `tenant_pk` (FK → Tenant)
- Inherits from `RecurringChargeMixin`: `date_start`, `date_end`
- → tenant, rentables (M2M via lease_rentable), recurring_charges

**Note from model docstring:** *"State table of a lease. Shouldn't be updated directly."* — intent was immutable lease records.

**LeaseRentable** (`server/src/db/model/lease_rentable.py`):
- Junction table: `lease_pk` ↔ `rentable_pk`
- UniqueConstraint(`lease_pk`, `rentable_pk`)
- Allows one tenant to lease multiple rentables under one lease

**RecurringCharge** (`server/src/db/model/recurring_charge.py`):
- `pk`, `lease_pk` (FK → Lease), `charge_type_pk` (FK → ChargeType)
- Inherits `date_start`, `date_end` (full span of this charge on the lease)
- → recurring_charge_periods (ordered by date_start, cascade delete)

**RecurringChargePeriod**:
- `pk`, `recurring_charge_pk` (FK → RecurringCharge)
- `amount` (CurrencyDecimal) — rate for this period
- `date_start`, `date_end`
- **ExcludeConstraint** (PostgreSQL GiST): prevents overlapping date ranges per recurring_charge_pk — enforced at DB level

**How escalation works in Crispina:**
```
RecurringCharge (Rent, Jan 2025 – Dec 2026)
  RecurringChargePeriod (Jan 2025 – Dec 2025, amount=100.00)
  RecurringChargePeriod (Jan 2026 – Dec 2026, amount=150.00)
```
Rate changes are modeled as new periods, not updates to the parent record.

**LeaseGenerate schema** (`server/src/api/schema/lease.py`):
- `tenant_pk`, `rentable_pks` (list, min 1)
- `recurring_charge_generators` (list of `RecurringChargeGenerate`, min 1)

**RecurringChargeGenerate schema**:
- `charge_type_pk`, `base_amount`, `date_start`, `date_end`
- **`yearly_increase_percent`** (PercentageDecimal) — semi-automated escalation input

**Gap:** No explicit `LeaseEvent` model for tracking extensions, cancellations, tacit reconduction. The model file has a TODO comment for this.

---

### ChargeType

**ChargeType** (`server/src/db/model/charge_type.py`):
- `pk`, `name` (unique), `billing_name`, `description`
- `is_vat_inclusive` (Boolean, default True)
- `vat_rate` (PercentageDecimal, nullable)
- **CheckConstraint:** `(is_vat_inclusive AND vat_rate IS NOT NULL) OR (NOT is_vat_inclusive AND vat_rate IS NULL)`

**Seeded charge types** (`server/src/script/seed.py`):
```
Name: "Rent"
billing_name: "Monthly Rent"
is_vat_inclusive: True
vat_rate: 0.12 (12%)
```

**Only one charge type seeded.** The system is designed for multiple, but only Rent was implemented. No seed data for:
- Water utility billing
- Electric utility billing
- Late payment penalties
- Security deposit (collection/deduction/refund)
- DST (Documentary Stamp Tax)
- Association dues / common area charges
- Advance rent

---

### Charge

**Charge** (`server/src/db/model/charge.py`):
- `pk`
- `base_amount` (CurrencyDecimal) — **pre-VAT amount stored**
- `vat_rate_used` (PercentageDecimal) — VAT rate at time of billing
- `date_issued`, `date_due` (Date)
- FK: `charge_type_pk`, `tenant_pk`, `rentable_pk`, `transaction_pk`
- FK: `lease_pk` (nullable) — optional link to specific lease
- Hybrid property: `amount` = `base_amount × (1 + vat_rate_used)` — VAT-inclusive total

**Index:** `(tenant_pk, rentable_pk, charge_type_pk, date_due)` — optimized for per-tenant/unit charge lookups

**Key design:** Stores pre-VAT amount. Total is computed. This aligns with BIR requirement to show VAT separately on invoices.

---

### Transaction

**Transaction** (`server/src/db/model/transaction.py`):
- `pk`, `description` (String 255), `date_issued` (Date)
- → payment_allocations (viewonly), charges (viewonly)

**TransactionDetail schema**: adds computed:
- `total_amount_due` — sum of all charges
- `total_amount_paid` — sum of all payment allocations
- `total_balance` — due minus paid

**Transaction pattern:** Transactions group charges (what's owed). Payments are then allocated against transactions. This enables partial payment tracking.

---

### Payment & PaymentAllocation

**Payment** (`server/src/db/model/payment.py`):
- `pk`, `amount` (CurrencyDecimal), `reference_number` (String 255), `date_issued` (Date)
- FK: `tenant_pk` → Tenant
- → transactions (M2M via payment_allocation, viewonly)

**PaymentAllocation** (`server/src/db/model/payment_allocation.py`):
- Junction: `payment_pk` ↔ `transaction_pk`
- `amount` (CurrencyDecimal) — portion of payment allocated to this transaction
- UniqueConstraint(`payment_pk`, `transaction_pk`)

**Seed example:** Payment of ₱120.00 allocated ₱90.00 to one transaction — demonstrating partial allocation.

**Missing fields on Payment:**
- No `payment_method` (cash, bank transfer, GCash, check)
- No `or_number` (BIR official receipt number)
- No `deposited_date` (for bank reconciliation)
- No `remarks`

---

## Type System

**`server/src/db/model/type.py`:**
```python
CurrencyDecimal = DECIMAL(precision=10, scale=2, asdecimal=True)
PercentageDecimal = DECIMAL(precision=4, scale=4, asdecimal=True)
```
- Currency: 10 digits total, 2 decimal places (centavo precision)
- Percentage: 4 digits total, 4 decimal places (e.g., 0.1200 = 12.00%)
- Constants: ZERO/ONE versions for computation

**`server/src/api/schema/type.py`:**
- `CurrencyDecimal`: Annotated Decimal with `BeforeValidator(round_currency)`, gte=0
- `PercentageDecimal`: Annotated Decimal with `BeforeValidator(round_percentage)`, gt=0
- Pydantic validators apply rounding on input

---

## Base Model

**All models inherit from `Base` (`server/src/db/model/base.py`):**
- `created_at` (DateTime with TZ, server_default=now())
- `last_updated_at` (DateTime with TZ, server_default=now(), server_onupdate=now())

---

## What Crispina Built — Summary

| Feature | Model Exists | Status |
|---------|-------------|--------|
| Property/Room/Rentable hierarchy | ✅ | Complete |
| Tenant management | ✅ | Missing TIN, corporate flag |
| Lease with multiple rentables | ✅ | Complete |
| Recurring charge with rate periods | ✅ | Well-designed |
| Rent escalation (yearly %) | ✅ | Via RecurringChargePeriod |
| Charge generation (VAT-inclusive) | ✅ | Base amount + VAT rate stored |
| Transaction grouping | ✅ | Complete |
| Payment recording | ✅ | Missing payment method, OR number |
| Partial payment allocation | ✅ | Via PaymentAllocation |
| Payment balance tracking | ✅ | Computed in TransactionDetail |
| ChargeType taxonomy | ✅ | Extensible, only Rent seeded |
| Security deposit tracking | ❌ | No model |
| Late payment penalty | ❌ | No model |
| Water utility billing | ❌ | No model (see water/ calculator) |
| Electric utility billing | ❌ | No model |
| Official receipt (OR) numbering | ❌ | No model |
| 2307 certificate tracking | ❌ | No model |
| Lease event log | ❌ | TODO in code |
| Lease status (active/expired/terminated) | ❌ | No status field |
| Unit floor area | ❌ | Missing from Rentable |
| Rent control flag | ❌ | Missing from Tenant/Rentable |

---

## Key Gaps for PH Compliance

1. **TIN on Tenant** — required for official receipts and 2307 certificates
2. **Corporate flag on Tenant** — determines EWT (5%) applicability
3. **Rent control flag** — determines RA 9653 vs Civil Code rules for escalation
4. **Floor area on Rentable** — needed for electric bill apportionment
5. **OR number on Payment** — BIR-mandated sequential numbering
6. **Security deposit tracking** — separate liability until applied/forfeited
7. **Late fee computation** — no penalty model
8. **DST on lease creation** — no stamp duty tracking
9. **Lease status field** — no way to distinguish active vs expired vs month-to-month

---

## Relationship Map

```
Property
  └─ Room (many)
       └─ Rentable (many)
            ├─ LeaseRentable → Lease ← Tenant
            │                    └─ RecurringCharge (many, cascade delete)
            │                         └─ RecurringChargePeriod (many, no overlap)
            └─ Charge ─────────────────────────── ChargeType
                  └─ Transaction
                        └─ PaymentAllocation ← Payment ← Tenant
```

---

*Source: `tsvjph/crispina`, `server/src/db/model/` and `server/src/api/schema/`, main branch, extracted Feb 2026.*
