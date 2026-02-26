# Crispina Services — Extracted Logic

Source: `tsvjph/crispina` — `/server/src/api/service/`, `/server/src/api/repository/`, `/server/src/api/schema/`, `/server/src/script/seed.py`

---

## 1. `service/math.py` — Financial Calculations

### Type Definitions (from `schema/type.py`)

```python
CurrencyDecimal = Annotated[Decimal, BeforeValidator(round_currency),
    Field(gte=0, max_digits=10, decimal_places=2)]

PercentageDecimal = Annotated[Decimal, BeforeValidator(round_percentage),
    Field(gt=0, max_digits=4, decimal_places=4)]
```

- Currency: non-negative, 2 decimal places, auto-rounded on input
- Percentage: strictly positive (no zero-rate charges), 4 decimal places

### Functions

```python
def round_currency(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

def round_percentage(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.0001"), rounding=ROUND_DOWN)

def calculate_compound_interest(base, rate, years) -> CurrencyDecimal:
    if years == 0:
        return base
    result = base * (Decimal("1.0000") + rate) ** years
    return round_currency(result)
```

**Rounding policy**: ROUND_DOWN throughout — consistently floors, never rounds up. This is tenant-favorable for charges (lessens the bill). For NHSB caps this is the correct direction.

**Compound interest formula**: `base × (1 + rate)^years`
- Year 0: base unchanged
- Year 1: base × (1 + rate)
- Year 2: base × (1 + rate)²
- Applied to rent escalation: a 5% annual increase compounds, not simple addition

**Important note on NHSB compliance**: The compound interest formula is _not_ automatically constrained to NHSB caps. Passing `yearly_increase_percent = 0.023` gives exactly 2.3%, which is the NHSB 2025 cap. But nothing in the math layer enforces that the caller uses the correct rate. The cap enforcement must happen at the application layer (form validation, lease generation logic).

---

## 2. `service/date.py` — Date Range Splitting

```python
@dataclass(frozen=True)
class Period:
    date_start: dt.date
    date_end: dt.date
    # Validates: date_start < date_end

def split_by_year(date_from, date_to) -> list[Period]:
    # Uses rrule.YEARLY anchored to date_from
    # Splits at lease anniversaries, NOT calendar year boundaries
    year_anchors = rrule.rrule(rrule.YEARLY, dtstart=date_from, until=date_to)
    # Each period: starts at anchor (or date_from for first),
    #              ends day before next anchor (or date_to for last)
```

**Key behavior**: Split is by lease anniversary, not calendar year.
- Lease from 2025-03-15 to 2027-03-14 splits as:
  - Period 0: 2025-03-15 → 2026-03-14 (Year 1 rate)
  - Period 1: 2026-03-15 → 2027-03-14 (Year 2 rate)
- This correctly models NHSB's "per lease year" escalation rule

**Edge case**: If `date_from == date_to`, the assert fails (requires strict less-than). Zero-length leases are not supported.

---

## 3. Core Billing Engine — Recurring Charge Generation

Located in `repository/recurring_charge.py`. This is the central computation of rent escalation.

### Input (`schema/recurring_charge.py: RecurringChargeGenerate`)
```python
class RecurringChargeGenerate:
    charge_type_pk: UUID           # Which type of charge (Rent, Water, etc.)
    base_amount: CurrencyDecimal   # Starting rent amount (Year 0)
    yearly_increase_percent: PercentageDecimal  # Annual escalation rate
    date_start: dt.date
    date_end: dt.date
```

### Algorithm (`repository/recurring_charge.py: generate()`)
```python
def generate(params, lease_pk):
    periods = split_by_year(params.date_start, params.date_end)
    recurring_charge_periods = []
    for period_idx, period in enumerate(periods):
        amount = calculate_compound_interest(
            base=params.base_amount,
            rate=params.yearly_increase_percent,
            years=period_idx   # 0 for first year, 1 for second, etc.
        )
        recurring_charge_periods.append(RecurringChargePeriod(
            amount=amount,
            date_start=period.date_start,
            date_end=period.date_end,
        ))
    recurring_charge = RecurringCharge(
        lease_pk=lease_pk,
        charge_type_pk=params.charge_type_pk,
        recurring_charge_periods=recurring_charge_periods,
        date_start=params.date_start,
        date_end=params.date_end,
    )
```

**Design decision**: Escalation is **pre-computed at lease creation** and stored as a series of `RecurringChargePeriod` records. The system does NOT recompute rent monthly — it looks up which period the billing month falls in, then uses that period's pre-stored amount.

**Architectural implications**:
- Auditable: the rate used for each period is stored permanently
- Inflexible: mid-lease rate changes require creating a new RecurringCharge (or deleting + recreating)
- One lease can have multiple RecurringCharges (e.g., Rent + Water + Electric as separate lines)
- No built-in support for NHSB rule-based capping vs contractual commercial rates

---

## 4. Lease Generation Flow

`schema/lease.py: LeaseGenerate` → `repository/lease.py: generate()`

```python
class LeaseGenerate:
    tenant_pk: UUID
    rentable_pks: list[UUID]                           # Min 1
    recurring_charge_generators: list[RecurringChargeGenerate]  # Min 1
```

**Flow**:
1. Derive `date_start` = min of all recurring charge start dates
2. Derive `date_end` = max of all recurring charge end dates
3. Create `Lease` record
4. Create `LeaseRentable` associations (many-to-many, one lease can cover multiple units)
5. For each `RecurringChargeGenerate`: call `generate()` → creates `RecurringCharge` + `RecurringChargePeriod` records

**Gaps vs business need**:
- No `status` field on Lease — can't distinguish active/expired/terminated
- No separate deposit handling at lease creation
- No board resolution linkage (corporate requirement)
- No rent control flag — no way to track which leases are NHSB-covered vs commercial
- Lease date derived from charges, not explicitly set — fragile if charge generators have different ranges

---

## 5. Transaction and Charge Architecture

### Charge (`schema/charge.py`)
```python
class Charge:
    pk: UUID
    base_amount: CurrencyDecimal   # Pre-VAT rent
    vat_rate_used: PercentageDecimal  # VAT rate at time of issuance (stored for audit)
    date_due: dt.date
    date_issued: dt.date
    amount: CurrencyDecimal        # VAT-inclusive total (hybrid computed field)
    # Also: charge_type_pk, tenant_pk, rentable_pk, lease_pk, transaction_pk
```

**VAT computation** (inferred from seed data + is_vat_inclusive flag):
- `vat_rate_used = 0.1200` means 12% VAT
- `base_amount = 100.00`, `amount = 112.00` (VAT-inclusive)
- The `amount` hybrid property likely computes: `base_amount * (1 + vat_rate_used)`

### Transaction
```python
class Transaction:
    pk: UUID
    description: str       # e.g., "Rent for January 2025"
    date_issued: dt.date
```

```python
class TransactionDetail(Transaction):
    total_amount_due: CurrencyDecimal   # sum(Charges.amount)
    total_amount_paid: CurrencyDecimal  # sum(PaymentAllocations.amount)
    total_balance: CurrencyDecimal      # due - paid
```

**Transaction = billing batch**: One transaction groups all charges issued together. Monthly billing generates one transaction per billing run, containing multiple charge records.

### Payment and PaymentAllocation
```python
class Payment:
    pk: UUID
    amount: CurrencyDecimal
    reference_number: str
    date_issued: dt.date
    tenant_pk: UUID        # Payer identity

class PaymentAllocation:
    pk: UUID
    amount: CurrencyDecimal
    payment_pk: UUID       # Which payment
    transaction_pk: UUID   # Which transaction (NOT charge-level)
```

**Payment allocation model**:
- One payment → many transactions (partial payment across multiple months)
- One transaction → many payments (overpayment or split payment)
- Allocation is at transaction level, NOT charge level
- Cannot specify "apply this payment to the water charge but not rent" — only transaction-level granularity
- Balance query: `sum(Charge.amount WHERE transaction_pk=X) - sum(PaymentAllocation.amount WHERE transaction_pk=X)`

---

## 6. Repository Query Patterns

### Balance computation (`repository/transaction.py`)
```python
_TOTAL_CHARGES = func.sum(Charge.amount)
_TOTAL_PAYMENTS = func.sum(PaymentAllocation.amount)
_BALANCE = _TOTAL_CHARGES - _TOTAL_PAYMENTS
```

This computes balance per transaction, not per tenant. To get tenant-level balance, one would need to sum across all transactions for that tenant — **this query is not built**.

### Rentable path (`repository/util.py`)
```python
RENTABLE_PATH_QUERY = case(
    (Rentable.name.is_(None), func.concat(Room.name)),
    else_=func.concat(Rentable.name, " ", Room.name),
)
```

Display path: if subdivided, shows "A Unit 101"; if not subdivided, shows "Unit 101".

---

## 7. Seeded Data — Authoritative Business Intent

From `script/seed.py`:

**Only 1 ChargeType seeded**: `Rent` (billing_name="Monthly Rent", is_vat_inclusive=True, vat_rate=0.12)
- **Gap**: No Water, Electric, Association Dues, or penalty charge types
- **Gap**: No charge type for security deposit receipts or refunds

**Property**: "TSVJ Center" at "Crispina Avenue, Pamplona 3, Las Piñas City"

**Room subdivision model**:
- Unit 101: not subdivided (1 rentable)
- Unit 102: subdivided into A, B, C (3 rentables from 2 max_subdivisions — seed exceeds max_subdivisions for testing)

**Demo lease**: 2 years (2025-01-01 to 2026-12-31), 2 RecurringChargePeriods manually created (not via generate()):
- Period 1: P100/month (2025)
- Period 2: P150/month (2026)
- 50% manual increase — demonstration data, not regulatory

**Demo payment**: P120.00, allocated P90.00 to transaction → leaving P30 balance (demonstrates partial payment)

---

## 8. Gaps and Missing Service Logic

| Capability | Status |
|---|---|
| Rent escalation (compound interest, pre-computed) | ✅ Built |
| Annual period splitting (lease-anniversary based) | ✅ Built |
| VAT computation on charges | ✅ Built (stored rate approach) |
| Partial payment allocation | ✅ Built (transaction-level) |
| Tenant-level balance rollup | ❌ Not built |
| NHSB cap enforcement | ❌ Not built (caller responsibility) |
| Late penalty calculation | ❌ Not built |
| Security deposit tracking | ❌ Not built |
| Water meter → bill computation | ❌ Not built (separate water/ tool) |
| Electric apportionment | ❌ Not built |
| DST computation | ❌ Not built |
| OR sequential numbering | ❌ Not built |
| 2307 certificate tracking | ❌ Not built |
| Rent roll generation | ❌ Not built |
| Lease status management | ❌ Not built (no status field) |
| Rent control flag per lease | ❌ Not built |
| Board resolution linkage | ❌ Not built |
| Corporate tenant TIN storage | ❌ Not built |
| Charge-level payment allocation | ❌ Not built (transaction-level only) |

---

## 9. Design Patterns Worth Preserving

1. **Pre-computed escalation with period storage** — excellent audit trail; each billing period's rate is permanent record
2. **VAT rate stored at charge-time** — protects against rate changes retroactively affecting historical charges
3. **ROUND_DOWN throughout** — tenant-favorable, defensible if disputed
4. **Transaction as billing batch** — groups related charges cleanly
5. **RecurringCharge → multiple ChargeTypes** — extensible to water/electric by adding charge types
6. **Lease anniversary splits, not calendar year** — correctly models how NHSB caps work in practice
