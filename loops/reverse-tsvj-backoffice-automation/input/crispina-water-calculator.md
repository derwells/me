# Crispina Water Calculator — Extracted Logic

Source: `tsvjph/crispina` — `/water/` directory (standalone tool, not integrated into main server)
Extracted: 2026-02-26

---

## Overview

The water calculator is a **standalone Python CLI tool** (`water/`) separate from the main Crispina server (`server/`). It was built as an ad-hoc script to compute per-tenant water bills from Maynilad master meter readings and sub-meter readings. It outputs a CSV file (`charge_rows.csv`) with one row per tenant-meter pair, formatted for import into Crispina's charge system.

**Key finding**: The water calculator uses a **pro-rata blended rate method** (total Maynilad bill ÷ total building consumption × tenant consumption), which is the simpler but **legally questionable** billing method. The legally correct method per MWSS regulations is per-tenant tier-based billing (each tenant's consumption starts at the lowest Maynilad tier). See `input/utility-billing-regulations.md` §2.3 for details.

---

## File Structure

```
water/
├── pyproject.toml      # Project metadata (Python ≥3.12.3, pandas + pydantic)
├── src/
│   ├── main.py         # Billing computation engine + CSV export
│   ├── model.py        # Pydantic models (frozen, validated)
│   └── seed.py         # Hardcoded meter readings + tenant assignments + Maynilad bill amounts
├── charge_rows.csv     # Output: per-tenant charge rows for import
└── uv.lock             # Dependency lock file
```

**Dependencies**: `pandas>=2.2.3`, `pydantic>=2.11.7` — no connection to the main server's SQLAlchemy database.

---

## Data Models (`model.py`)

### BillingPeriod
```python
class BillingPeriod(BaseModel):  # frozen
    month: int
    year: int
```
Simple month/year pair. Used as dict key for bill lookups.

### WaterBill
```python
class WaterBill(BaseModel):  # frozen
    billing_period: BillingPeriod
    amount: Decimal  # validated to 2 decimal places
```
Represents the total Maynilad master bill for a billing period.

### Tenant
```python
class Tenant(BaseModel):  # frozen
    name: str
```
Minimal — just a name. No TIN, no tenant type (residential/commercial), no contact info.

### MeterReading
```python
class MeterReading(BaseModel):  # frozen
    billing_period: BillingPeriod
    reading: int  # absolute reading in cubic meters
```
Stores absolute meter reading (not delta). Delta is computed between two billing periods.

### Meter
```python
class Meter(BaseModel):  # frozen
    name: str                     # e.g., "Unit 303", "CR-1"
    tenants: list[Tenant]         # can be empty (vacant/common area) or multiple (shared meter)
    readings: list[MeterReading]  # ordered by billing period

    @computed_field
    def is_subdivided(self) -> bool:
        return len(self.tenants) > 1
```
Key design: a meter can have **multiple tenants** (shared units like "Unit 303" with 2 occupants, or "Unit 307" with 2 co-tenants). When shared, the bill is split equally among co-tenants.

### TenantBill
```python
class TenantBill(BaseModel):  # frozen
    tenant: Tenant
    meter: Meter
    billing_period: BillingPeriod
    amount: Decimal               # validated to 2 decimal places
    previous_reading: int
    current_reading: int
```
The computed bill for one tenant from one meter for one billing period.

### ChargeRow
```python
class ChargeRow(BaseModel):  # frozen
    tenant: str
    property: str                 # meter name (e.g., "Unit 303")
    name: str                     # human-readable charge description
    charge_type: Literal["UTILITIES"] = "UTILITIES"
    due: Decimal
    due_no_vat: Decimal           # always equals `due` (no VAT applied to water)
```
Output format for import into Crispina. Note: `due == due_no_vat` — the water calculator does **not** add VAT to utility pass-throughs, which is correct (pass-through utility billing is not a VATable sale).

---

## Billing Computation Logic (`main.py`)

### Core Algorithm

```
For each tenant:
  For each meter assigned to tenant:
    1. consumption_delta = to_reading - from_reading (for this meter)
    2. total_building_delta = sum of all meters' (to_reading - from_reading)
    3. percentage_of_consumption = consumption_delta / total_building_delta
    4. bill_for_meter = (percentage_of_consumption × total_maynilad_bill) / number_of_co_tenants_on_meter
    5. Round to 2 decimal places (ROUND_HALF_UP, not ROUND_DOWN like main server)
```

### Step-by-Step Walkthrough

1. **Get total building consumption delta** between two billing periods:
   ```python
   total_delta = sum(meter.to_reading - meter.from_reading for all meters)
   ```

2. **For each meter assigned to a tenant**, compute:
   - `meter_delta = to_reading - from_reading`
   - `share = meter_delta / total_delta` (proportion of building consumption)
   - `bill = (share × maynilad_bill) / num_co_tenants`
   - Round to `Decimal("0.01")` using `ROUND_HALF_UP` (via `convert_to_accounting_amount`)

3. **Generate a ChargeRow** with a descriptive name including meter readings (zero-padded to 6 digits).

### Rounding Policy

**Inconsistency with main server**: The water calculator uses `ROUND_HALF_UP` at the final step (in `tenant_bill_to_charge_rows`) but `Decimal.quantize(Decimal("0.01"))` (default `ROUND_HALF_EVEN`) in `convert_to_accounting_amount`. The main Crispina server uses `ROUND_DOWN` throughout. This inconsistency stems from the water calculator being an ad-hoc tool developed independently.

---

## Seed Data Analysis (`seed.py`)

### Property Scale (from hardcoded data)

The seed data reveals the actual property portfolio being managed:

**Total meters defined**: 33 meters across 3 floors + 2 common-area restrooms
- **Floor 1 (100-series)**: Units 101–114 (14 units, mostly commercial — law offices, 7-Eleven)
- **Floor 2 (200-series)**: Units 201–212 (but 204–209 have no water meters — 6 units)
- **Floor 3 (300-series)**: Units 301–312 (12 residential units)
- **Common areas**: CR-1, CR-2 (restroom meters with no assigned tenants)

**Tenant mix (from meter assignments)**:
- Commercial: Philippine Seven Corporation (Units 101, 103), Bilgera Law Office, DB Tax and Accounting Services, several Attorneys, Urban Dwelling Realty Co., Envision Inc.
- Residential: Individual tenants on 3rd floor

**Meters with zero consumption** (from_reading == to_reading): 20 out of 33 meters had zero delta between June–July 2025 billing periods. Only 13 meters showed actual consumption.

**Defective/empty meters**:
- Unit 108 (Junelda A. Lombos): `readings=[]` — flagged as "Defective meter" in code comment
- Unit 113 (Rosalina Pasion): `readings=[]` — no readings
- Unit 114: `readings=[]`, no tenant assigned
- Unit 312: Note in code — "Anthony put 73, not 75. I'm guessing 73 is a typo" — manual reading correction

**Shared meters** (multiple tenants):
- Unit 303: Maribel M. Belmonte + Sam M. Belmonte (2 co-tenants)
- Unit 307: Gian Paolo Barayuga + Joshua Andrei Chioco (2 co-tenants)
- Unit 308: Jean Camille L. Dela Cruz + Joshua A. Gracilla (2 co-tenants)
- Unit 310: Gat Kylle O. Asin + Raul Angelo B. Oida (2 co-tenants)

### Maynilad Bill Amounts

```python
ALL_BILLS = {
    June 2025: Decimal("382.88") + Decimal("8253.20") = Decimal("8636.08"),
    July 2025: Decimal("181.42") + Decimal("7413.86") = Decimal("7595.28"),
}
```

The bill amounts are sums of two components (likely two master meter accounts or two billing line items — possibly water + sewerage, or two separate Maynilad accounts for different sections of the building).

---

## Output Analysis (`charge_rows.csv`)

The CSV output for July 2025 shows:
- **29 rows** (one per tenant-meter pair)
- **19 rows with ₱0.00** (zero consumption meters)
- **10 rows with charges** ranging from ₱56.68 to ₱906.90
- Highest bill: Sarah Sam Libirtenos (Unit 304) — ₱906.90 (8 cu.m. delta)
- Shared meters split equally: Unit 303 → ₱680.17 each for 2 co-tenants (12 cu.m. total, 6 each effectively)
- Unit 307 → ₱396.77 each for 2 co-tenants (7 cu.m. total)

### Verification of Pro-Rata Formula

Total building delta (July): 25 + 4 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 1 + 0 + 2 + 1 + 2 + 12 + 8 + 0 + 1 + 7 + 1 + 1 + 0 + 0 + 0 + 2 = **67 cu.m.**

Per-cu.m. rate: ₱7,595.28 / 67 = **₱113.36/cu.m.**

Spot checks:
- Unit 201 (1 cu.m., 1 tenant): 1/67 × ₱7,595.28 = ₱113.36 ✓
- Unit 304 (8 cu.m., 1 tenant): 8/67 × ₱7,595.28 = ₱906.90 ✓
- Unit 303 (12 cu.m., 2 co-tenants): (12/67 × ₱7,595.28) / 2 = ₱680.17 ✓

Formula verified correct for the pro-rata method.

---

## Gaps & Issues

### 1. Legally Questionable Billing Method (Critical)
The calculator uses **pro-rata blended rate** (total bill ÷ total consumption × tenant share). MWSS regulations require **per-tenant tiered billing** where each tenant's consumption starts at the lowest Maynilad rate tier. The pro-rata method shifts higher-tier costs onto low-consumption tenants. MWSS RO has ordered ₱87M+ in refunds for this practice (see `input/utility-billing-regulations.md` §2.3).

**However**: The practical impact depends on the property's master meter account classification and total consumption. If total building consumption is low enough that even the master meter stays in a low tier, the two methods produce similar results. At 67 cu.m./month total building consumption, the difference may be minimal — but this must be evaluated against Maynilad's actual tier schedule.

### 2. Common Area Water Not Allocated
CR-1 (25 cu.m. delta) and CR-2 (4 cu.m. delta) are common area restrooms with no tenants assigned. Their consumption (29 cu.m. out of 67 total = 43%) is absorbed into the pro-rata calculation, meaning **all tenants implicitly pay for common area water** proportionally to their own consumption. This is one valid allocation method (by consumption share), but:
- It is not disclosed as a separate line item on tenant bills
- Tenants with zero consumption pay ₱0.00 for common area water too (free-rider issue for vacant units)
- The regulations require common area water to appear as a **separate line item**, not blended in

### 3. No VAT Handling
`due == due_no_vat` throughout — water pass-through is correctly not VATable (it's a cost reimbursement, not a sale). But if the landlord adds any markup or admin fee (which is prohibited for water anyway), VAT treatment would change.

### 4. No Maynilad Tier Rate Tables
The calculator doesn't contain Maynilad's per-tier rate schedule. It only takes the total Maynilad bill amount as input. This means it cannot perform the legally correct per-tier billing even if modified — it would need the rate tables added.

### 5. Defective/Missing Meter Handling
- Defective meters (`readings=[]`) are silently skipped with a `print()` warning — the tenant gets no bill
- No mechanism for estimated billing when a meter is defective
- No tracking of which meters need repair/replacement

### 6. No Sewerage Charge Differentiation
Commercial tenants (Philippine Seven, law offices) should pay the 20% Sewerage Charge on their water; residential tenants should not. The calculator doesn't distinguish tenant types and applies the full blended rate to all.

### 7. Hardcoded Data
All meter readings, tenant assignments, and bill amounts are hardcoded in `seed.py`. There is no:
- Database integration
- Import mechanism for Maynilad bill PDFs
- Meter reading input form/API
- Historical billing period tracking

### 8. Rounding Inconsistency
Uses `ROUND_HALF_UP` at final output but default `ROUND_HALF_EVEN` in intermediate `convert_to_accounting_amount`. The main Crispina server uses `ROUND_DOWN`. Should standardize.

### 9. No Tenant-Type Classification
The `Tenant` model is just a name string. No commercial/residential flag, which matters for:
- Sewerage charge applicability (commercial only)
- Rate tier application (Maynilad classifies commercial/residential differently)
- VAT treatment if billing above VAT threshold

### 10. Not Integrated into Main Server
The water calculator is completely standalone. It doesn't read from or write to Crispina's database. The `ChargeRow` CSV output format suggests it was designed to be manually imported, but there's no import endpoint in the server.

---

## Design Patterns Worth Preserving

1. **Meter → Tenant relationship with co-tenancy support**: Multiple tenants can share one meter, with automatic equal splitting. This reflects real-world shared units.

2. **Delta-based consumption**: Using absolute readings and computing deltas prevents data entry errors from accumulating. Each reading is independently verifiable.

3. **ChargeRow as import format**: The concept of generating charges as importable rows for the main billing system is sound — keeps utility billing modular.

4. **Frozen Pydantic models**: All models are frozen (immutable), preventing accidental mutation during computation. Good practice for financial calculations.

5. **Zero-padded meter readings in descriptions**: The charge name format `[Meter Reading: 000142 to 000150]` provides an audit trail directly in the charge description.

---

## Relationship to Main Server Models

| Water Calculator | Main Server | Notes |
|---|---|---|
| `Meter.name` | `Room.name` | Meter names match room/unit naming (e.g., "Unit 303") |
| `Tenant.name` | `Tenant.name` (in Lease model) | Name-based matching only — no foreign key |
| `ChargeRow` | `Charge` model | CSV import target; maps to Charge with charge_type="UTILITIES" |
| `BillingPeriod` | `Transaction` (billing batch) | Transaction is the closest analog — groups charges by period |
| No equivalent | `Rentable` | Water calculator maps to Room, not Rentable — doesn't handle subdivisions |
| No equivalent | `RecurringCharge` / `RecurringChargePeriod` | Water is billed per-occurrence, not as a recurring schedule |

---

## Summary for Wave 2

The water calculator represents a **working but legally non-compliant prototype** of per-tenant water billing. Key decisions for the feature spec:

1. **Must switch to per-tier billing** to comply with MWSS regulations (or document risk if pro-rata is retained)
2. **Must separate common area water** as a distinct line item
3. **Must add tenant-type classification** (commercial vs residential) for sewerage charge differentiation
4. **Must integrate with the main database** rather than using hardcoded seed data
5. **Co-tenancy model is valuable** — preserve the multi-tenant-per-meter pattern
6. **Meter reading workflow needed** — input mechanism for monthly readings (currently hardcoded)
7. **Defective meter handling** — needs estimated billing or at least formal tracking
