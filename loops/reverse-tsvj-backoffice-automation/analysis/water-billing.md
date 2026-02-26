# Water Billing

**Wave:** 2 (Process Analysis & Feature Spec)
**Analyzed:** 2026-02-26
**Dependencies:** crispina-water-calculator, crispina-models, utility-billing-regulations

---

## 1. Process Description

**What:** Convert monthly Maynilad master meter bill + individual sub-meter readings into per-tenant water charges. Each tenant receives a water bill based on their actual sub-metered consumption, computed at the correct Maynilad tier rate. Common area water (restrooms, cleaning) is allocated separately as a distinct line item.

**When:** Monthly, after the Maynilad bill for the billing period is received and all sub-meter readings are collected. Typically 5-15 days after the Maynilad billing cycle ends (Maynilad bills are issued monthly, cycle varies by area).

**Who does it:** Property manager (or designated staff). Currently: reads sub-meters manually, records readings, uses the standalone Crispina water calculator (or manual spreadsheet) to compute per-tenant shares, then prepares water charge lines for the monthly billing statement.

**Frequency:** Monthly for all metered tenants. The TSVJ Center property has 33 sub-meters across 3 floors plus 2 common area restrooms.

---

## 2. Current Method

**Standalone script + manual data entry.** The property manager:

1. Receives the Maynilad master bill (paper or PDF)
2. Physically reads each of the 33 sub-meters in the building, recording the absolute reading
3. Enters readings into the Crispina water calculator's `seed.py` file (hardcoded Python)
4. Enters the total Maynilad bill amount into `seed.py`
5. Runs the calculator: `uv run python src/main.py`
6. Gets a CSV output (`charge_rows.csv`) with one row per tenant-meter pair
7. Manually imports these charges into the billing flow (or transfers to spreadsheet)

**Method used:** Pro-rata blended rate — total Maynilad bill / total building consumption x tenant's consumption share. This is the **legally non-compliant** method (see Regulatory Rules below).

**Known pain points from seed data analysis:**
- 20 of 33 meters showed zero consumption in the June-July 2025 period
- 3 meters have empty readings (defective or uninstalled)
- Manual reading corrections noted in code comments ("Anthony put 73, not 75")
- Common area water (CR-1 + CR-2) consumed 43% of total building water, blended into all tenants' bills invisibly

---

## 3. Regulatory Rules

### 3.1 No-Markup Rule (Strict Pass-Through)

Landlords may NOT charge tenants more than the actual cost billed by Maynilad for the tenant's consumption. Unlike electricity (where a reasonable admin fee is permitted if contractually agreed), **no administrative or service fee is permitted on water bills** — not even to cover the cost of maintaining sub-meters.

**Legal basis:**
- MWSS Charter (RA 6234) — landlord is "mere conduit" beyond the master meter
- MWSS RO Resolution No. 2016-010 — "at-cost" billing requirement
- RA 7581 (Price Act) — profiteering on water (basic necessity) is criminal: fine PHP 5,000-2,000,000 and/or 5 months-15 years imprisonment
- RA 7394 (Consumer Act) Art. 50 — overcharging = unfair trade practice
- Civil Code Arts. 19-21 — prohibits unjust enrichment

**Verification:** CONFIRMED — 3 independent sources (see verification report)

### 3.2 Per-Tier Billing Method (Critical — Current Method Is Non-Compliant)

Each tenant's individual sub-metered consumption **must start at the lowest Maynilad tier bracket**, regardless of the building's aggregate master meter consumption level. The "pro-rata blended rate" method (total bill / total consumption x tenant share) is **prohibited** because it shifts higher-tier costs from heavy consumers and common areas onto light consumers.

**Example (correct vs. incorrect):**
- Maynilad Tier 1: first 10 cu.m. at PHP 10/cu.m. = PHP 100
- Maynilad Tier 2: next 10 cu.m. at PHP 30/cu.m. = PHP 300
- Building total: 40 cu.m. → master bill = PHP 700 (10 @ PHP 10 + 10 @ PHP 30 + 20 @ PHP 35)
- Tenant A uses 5 cu.m., Tenant B uses 15 cu.m.

| Method | Tenant A (5 cu.m.) | Tenant B (15 cu.m.) |
|---|---|---|
| **Correct (per-tier)** | 5 @ PHP 10 = **PHP 50** | 10 @ PHP 10 + 5 @ PHP 30 = **PHP 250** |
| **Incorrect (blended)** | 5/40 x PHP 700 = **PHP 87.50** | 15/40 x PHP 700 = **PHP 262.50** |

Tenant A is overcharged by 75% under the blended method.

**Enforcement:** MWSS RO ordered **PHP 87M+ in refunds** from landlords and building administrators during 2021-2024 for water overbilling using the blended method.

**Legal basis:**
- **MWSS IRR No. 2008-02** — "Billing Scheme and Rate Classification for High-Rise and Other Multiple Dwellings" — the authoritative regulation mandating per-tier individual unit billing. Each unit's first 10 cu.m. is charged at the first-tier rate, next 10 cu.m. at the second-tier rate, etc., regardless of total building consumption.
- MWSS RO Customer Service Regulations
- MWSS RO Resolution No. 2016-010
- RA 7394 Art. 50 (unfair trade practice)

**Verification:** CONFIRMED — MWSS IRR No. 2008-02 (full text at ro.mwss.gov.ph), MWSS RO refund orders (₱87M+ in 2021-2024), Respicio & Co. legal commentary, news coverage

### 3.3 Common Area Water — Separate Line Item Required

Common area water (hallways, restrooms, gardens, cleaning) **must appear as a separate line item** on tenant bills. It cannot be blended into the per-cu.m. unit rate.

**Allocation methods:**
- **Option A (preferred):** Separate sub-meter for common areas → actual cost apportioned by floor area ratio or equal division
- **Option B:** Fixed peso amount pre-disclosed in the lease agreement, listed as separate line item

**Key constraint:** Total recovery from all tenants (unit consumption + common area allocation) must **never exceed** the total Maynilad master bill for the same period.

**Current TSVJ status:** CR-1 and CR-2 are common area restroom meters (25 + 4 = 29 cu.m. in July 2025, or 43% of total building consumption). Currently blended into all tenants' bills proportionally — non-compliant.

**Verification:** CONFIRMED — MWSS RO regulations, legal commentary

### 3.4 Bill Component Breakdown

Each tenant's water bill must include these Maynilad bill components:

| Component | Calculation | Applicability |
|---|---|---|
| **Basic Charge** | Per-tier rate x consumption (cu.m.) | All tenants |
| **Environmental Charge** | 25% of Basic Charge (effective Jan 2025, up from 20%) | All tenants |
| **Sewerage Charge** | 20% of Basic Charge | **Commercial/Industrial only** (if connected to sewer) — NOT Residential/Semi-Business |
| **FCDA** | Quarterly adjustment (+ or -) | All tenants (proportional) |
| **MSC (Maintenance Service Charge)** | Fixed monthly amount | Split proportionally or per-unit |
| **Government Taxes (VAT 12%)** | On applicable components | Per Maynilad bill structure |

**Critical differentiation:** Sewerage Charge applies ONLY to Commercial/Industrial accounts. The TSVJ property has both commercial (Floor 1: 7-Eleven, law offices) and residential (Floor 3: apartments) tenants. The water calculator must classify tenants by type to apply Sewerage Charge correctly.

**Verification:** CONFIRMED — Maynilad official rate schedule, MWSS RO

### 3.5 Billing Statement Requirements

Each water billing statement must include:
1. Initial sub-meter reading (start of period)
2. Final sub-meter reading (end of period)
3. Consumption in cubic meters
4. **Per-tier rate breakdown** (cu.m. billed at each rate level)
5. Basic Charge, Environmental Charge, Sewerage Charge (if applicable), MSC, Taxes
6. Total amount due
7. Computation showing how tenant's share derives from the master bill

**Additional obligations:**
- Provide photocopy or digital copy of Maynilad master bill to tenants **within 5 days** of receiving it
- Maintain **3 years** of billing and meter reading records
- Tenants may inspect and photograph both master meter and sub-meter at any reasonable time
- Over-collections refunded within **1 billing cycle** with **6% p.a.** interest

**Verification:** CONFIRMED — MWSS Customer Service Regulations, Respicio & Co.

### 3.6 Sub-Meter Installation Requirements

- Sub-meters must be **PNS/BPS certified** and regularly calibrated
- Installation requires **Maynilad/MWSS approval** (application at Business Area office covering Las Pinas)
- Uncalibrated or tampered meters = criminal liability under anti-pilferage laws

**Verification:** CONFIRMED — MWSS RO regulations

### 3.7 VAT Treatment of Water Pass-Through

Water utility pass-through billing (pure cost reimbursement) is **NOT a VATable sale** — the landlord acts as a conduit, not a vendor of water. The Crispina water calculator correctly sets `due == due_no_vat`.

However, for the purposes of the landlord's VAT return:
- Water charges passed through to tenants are **not gross receipts** for VAT/OPT threshold computation
- The Maynilad bill paid by the landlord is a **non-deductible input VAT** (it's a reimbursement, not a purchase for resale)
- If the landlord adds ANY markup (which is prohibited for water), the entire water charge becomes a VATable service

**Legal basis:** BIR RR 16-2005; NIRC Sec. 108 (services subject to VAT); general pass-through doctrine

**Verification:** CONFIRMED — multiple tax advisory sources

### 3.8 Defective Meter Handling

No specific MWSS regulation prescribes estimated billing for defective sub-meters in landlord-tenant contexts. Industry practice:
- If sub-meter is defective, use the average of the last 3 months' consumption as estimated billing
- Flag the meter as defective and schedule replacement
- Once replaced, true-up against the new meter's baseline reading

The Crispina water calculator silently skips defective meters (empty readings), resulting in no bill for the tenant — which means their water consumption gets absorbed into other tenants' bills via the blended rate.

**Verification:** UNVERIFIED — no authoritative source found for estimated billing rules in sub-metering context

---

## 4. Formula / Decision Tree

### 4.1 Per-Tier Water Billing Algorithm (Legally Correct Method)

```
FUNCTION compute_water_bill(tenant, billing_period):

  -- 1. GET READINGS
  current_reading = get_sub_meter_reading(tenant.meter, billing_period)
  previous_reading = get_sub_meter_reading(tenant.meter, billing_period - 1)
  consumption_cu_m = current_reading - previous_reading

  IF consumption_cu_m < 0:
    RAISE "Negative consumption — possible meter rollover or reading error"
  IF consumption_cu_m == 0:
    RETURN zero_charge(tenant, billing_period)  -- Still generate a statement showing 0

  -- 2. DETERMINE TENANT TYPE (for rate tier and sewerage)
  tenant_type = tenant.lease.rentable.unit_type  -- RESIDENTIAL or COMMERCIAL

  -- 3. COMPUTE BASIC CHARGE USING MAYNILAD TIERS
  -- Each tenant starts at the lowest tier
  basic_charge = Decimal("0.00")
  remaining = consumption_cu_m

  FOR each tier IN maynilad_rate_table(tenant_type, billing_period):
    -- tier = { bracket_start, bracket_end, rate_per_cu_m }
    tier_consumption = min(remaining, tier.bracket_end - tier.bracket_start)
    basic_charge += tier_consumption * tier.rate_per_cu_m
    remaining -= tier_consumption
    IF remaining <= 0: BREAK

  -- 4. COMPUTE SURCHARGES
  environmental_charge = basic_charge * Decimal("0.25")  -- 25% of Basic (2025+)

  IF tenant_type == COMMERCIAL AND property.is_sewered:
    sewerage_charge = basic_charge * Decimal("0.20")  -- 20% of Basic
  ELSE:
    sewerage_charge = Decimal("0.00")

  -- 5. FCDA (Foreign Currency Differential Adjustment)
  -- Quarterly rate from MWSS — can be + or -
  fcda_amount = consumption_cu_m * fcda_rate_per_cu_m(billing_period)

  -- 6. MSC (Maintenance Service Charge)
  -- Fixed monthly amount from Maynilad, split per-unit
  msc_share = maynilad_msc_total / active_tenant_count

  -- 7. GOVERNMENT TAXES (as on Maynilad bill)
  taxable_amount = basic_charge + environmental_charge + sewerage_charge + fcda_amount
  vat_amount = taxable_amount * Decimal("0.12")

  -- 8. TOTAL
  total = basic_charge + environmental_charge + sewerage_charge
        + fcda_amount + msc_share + vat_amount

  -- 9. ROUND (use ROUND_DOWN consistent with main server)
  total = round_currency(total)  -- Decimal("0.01"), ROUND_DOWN

  RETURN WaterCharge(
    tenant=tenant,
    billing_period=billing_period,
    consumption_cu_m=consumption_cu_m,
    basic_charge=basic_charge,
    environmental_charge=environmental_charge,
    sewerage_charge=sewerage_charge,
    fcda=fcda_amount,
    msc_share=msc_share,
    vat=vat_amount,
    total=total,
    previous_reading=previous_reading,
    current_reading=current_reading
  )
```

### 4.2 Common Area Water Allocation

```
FUNCTION allocate_common_area_water(billing_period):

  -- 1. GET COMMON AREA CONSUMPTION
  common_meters = [CR-1, CR-2, ...]  -- meters with no assigned tenant
  common_consumption = sum(current - previous FOR each meter IN common_meters)

  -- 2. COMPUTE COMMON AREA WATER COST (same tier method)
  common_area_cost = compute_tiered_cost(common_consumption, RESIDENTIAL)
  -- Use residential rates for common area (conservative — no sewerage)

  -- 3. ALLOCATE TO TENANTS
  allocation_method = property.common_area_allocation_method
  -- Options: BY_FLOOR_AREA, EQUAL_SPLIT, BY_CONSUMPTION_SHARE

  IF allocation_method == BY_FLOOR_AREA:
    FOR each tenant IN active_tenants:
      share = tenant.rentable.floor_area_sqm / total_rentable_floor_area
      tenant_common_charge = common_area_cost * share

  ELSE IF allocation_method == EQUAL_SPLIT:
    per_unit_share = common_area_cost / active_unit_count
    FOR each tenant: tenant_common_charge = per_unit_share

  -- 4. RETURN AS SEPARATE LINE ITEMS
  RETURN [CommonAreaWaterCharge(tenant, amount, billing_period) FOR each tenant]
```

### 4.3 Reconciliation Check (Mandatory)

```
FUNCTION verify_total_recovery(billing_period):
  -- Total billed to all tenants MUST NOT exceed Maynilad master bill

  total_tenant_charges = sum(all tenant water charges + common area allocations)
  maynilad_master_bill = get_maynilad_bill(billing_period).amount

  IF total_tenant_charges > maynilad_master_bill:
    RAISE "Over-recovery: billed tenants PHP {total_tenant_charges} " +
          "but Maynilad charged PHP {maynilad_master_bill}. " +
          "Difference must be absorbed by landlord."

  -- Under-recovery is normal (vacant units, zero-consumption units)
  -- The landlord absorbs the difference as an operating cost
  under_recovery = maynilad_master_bill - total_tenant_charges
  LOG "Under-recovery for {billing_period}: PHP {under_recovery}"
```

---

## 5. Edge Cases and Special Rules

### 5.1 Shared Meters (Co-Tenancy)

The TSVJ property has 4 shared-meter situations (Units 303, 307, 308, 310 — each with 2 co-tenants). When a meter serves multiple tenants:
- Compute total bill for the meter using per-tier method
- Divide equally among co-tenants (or per co-tenancy agreement)
- Each co-tenant's statement shows the meter reading + their share

The Crispina water calculator already supports this pattern — preserve it.

### 5.2 Defective or Missing Meters

3 meters had empty readings in the seed data (Units 108, 113, 114). Options:
- **Estimated billing:** Average of last 3 months' consumption (industry standard)
- **Zero billing:** No charge issued — but consumption absorbed into blended rate penalizes others
- **Fixed charge:** Lease may specify a fixed water allowance for defective-meter periods

Recommended: Estimated billing with clear notation on statement. Flag meter for repair. Track meter status in the system.

### 5.3 Negative or Implausible Readings

Meter rollover (reading counter resets to 0) or data entry error can produce negative deltas. The system should:
- Reject negative deltas and flag for manual review
- For rollovers: compute as `(max_meter_value - previous_reading) + current_reading`
- For implausibly high readings (> 3x previous month): flag for confirmation before billing

### 5.4 Vacant Units

Units with no active lease should not be billed for water, but their meters should still be read:
- Track vacancy consumption (possible leak detection)
- Vacant-unit consumption is a landlord cost, not redistributed to other tenants
- Under the per-tier method, vacant-unit water is simply not billed (unlike blended method where it's invisible)

### 5.5 New Tenant Mid-Month

If a tenant moves in mid-billing-cycle:
- Take a move-in meter reading
- First billing period: from move-in reading to next regular reading
- Pro-rate any fixed charges (MSC share) to the partial month

### 5.6 Maynilad Rate Changes

Maynilad adjusts rates quarterly (FCDA) and annually (RAL). The system needs:
- A rate table (`MayniladRateSchedule`) that stores per-tier rates by effective date
- Quarterly FCDA rate updates
- The ability to apply the correct rate table for each billing period

### 5.7 Master Bill Received Late

If the Maynilad bill arrives after the monthly billing run:
- Water charges are billed in the next statement (one month lag)
- The billing statement should indicate which Maynilad billing period the water charge covers
- This is standard practice and aligns with the recommendation in the monthly-billing-generation analysis to run utility billing separately from rent billing

### 5.8 Lifeline Rate Inapplicability

Individual sub-metered tenants consuming <= 10 cu.m. **cannot** claim the Maynilad lifeline rate (41.3% discount) because eligibility attaches to the Maynilad account (master meter), not sub-metered units. The master meter's aggregate consumption always exceeds 10 cu.m., disqualifying the account.

The system should use the **full (non-lifeline) per-tier rates** for all sub-meter billing. If the master meter bill includes a lifeline discount (it won't for a commercial building), the discount flows through the reconciliation.

---

## 6. What Crispina Built

### Built (Standalone Water Calculator — `water/`)

| Component | Status | Notes |
|---|---|---|
| Meter model with co-tenancy | **Built** | `Meter.tenants: list[Tenant]` — multiple tenants per meter with equal split |
| Delta-based consumption | **Built** | Absolute readings → delta computation. Prevents cumulative errors. |
| ChargeRow CSV export | **Built** | Output format for import into main billing system |
| Frozen Pydantic models | **Built** | Immutable computation — good for financial calculations |
| Zero-padded reading descriptions | **Built** | `[Meter Reading: 000142 to 000150]` — audit trail in charge name |
| Billing period tracking | **Built** | `BillingPeriod(month, year)` — simple but functional |

### Not Built (Key Gaps)

| Gap | Impact |
|---|---|
| **Per-tier billing** | Uses prohibited pro-rata blended rate. Must be replaced with per-tier computation. |
| **Maynilad tier rate tables** | No rate schedule embedded — only takes total bill amount. Cannot do per-tier billing without rate data. |
| **Tenant type classification** | No commercial/residential flag → cannot differentiate Sewerage Charge applicability |
| **Common area separation** | CR-1/CR-2 consumption (43% of total) blended into tenant bills, not shown as separate line |
| **Environmental/Sewerage charge breakdown** | Not computed — only total bill passed through |
| **FCDA tracking** | Quarterly adjustment not modeled |
| **Maynilad bill storage** | Master bill amount hardcoded — no database storage or history |
| **Meter status tracking** | Defective meters silently skipped with `print()` — no formal status |
| **Estimated billing** | No fallback for defective meters |
| **Database integration** | Standalone script — no connection to main server DB |
| **Meter reading input workflow** | Readings hardcoded in `seed.py` — no input form/API |
| **Reconciliation check** | No validation that total tenant charges <= Maynilad master bill |
| **Billing statement generation** | CSV only — no formatted per-tenant statement with tier breakdown |
| **Rounding consistency** | Uses ROUND_HALF_UP (some places ROUND_HALF_EVEN) vs. main server's ROUND_DOWN |

### Design Patterns Worth Preserving

1. **Meter → Tenant with co-tenancy** — multi-tenant-per-meter pattern with automatic equal split
2. **Delta-based readings** — absolute readings prevent cumulative data entry errors
3. **ChargeRow as import format** — modular utility billing that integrates with main billing system
4. **Frozen Pydantic models** — immutable computation for financial correctness
5. **Reading descriptions in charge name** — built-in audit trail

---

## 7. Lightweight Feature Spec

### 7.1 Data Model

```
NEW: WaterMeter
  pk: UUID
  name: String(50)                    -- e.g., "Unit 303", "CR-1"
  meter_serial: String(50), nullable  -- physical meter serial number
  property_pk: UUID (FK → Property)
  room_pk: UUID (FK → Room), nullable -- link to room (null for common area meters)
  meter_type: Enum(UNIT, COMMON_AREA)
  status: Enum(ACTIVE, DEFECTIVE, DECOMMISSIONED)
  max_reading: Integer, default 999999  -- for rollover detection
  installed_date: Date, nullable
  last_calibration_date: Date, nullable
  notes: Text, nullable

NEW: WaterMeterTenant (junction for co-tenancy)
  meter_pk: UUID (FK → WaterMeter)
  tenant_pk: UUID (FK → Tenant)
  share_ratio: Decimal(3,2), default 1.00  -- 0.50 for 2 co-tenants
  effective_from: Date
  effective_until: Date, nullable
  UNIQUE(meter_pk, tenant_pk, effective_from)

NEW: WaterMeterReading
  pk: UUID
  meter_pk: UUID (FK → WaterMeter)
  billing_period: Date (1st of month)
  reading: Integer                    -- absolute meter reading (cu.m.)
  reading_date: Date                  -- when physically read
  read_by: String(100), nullable
  photo_url: String(500), nullable    -- evidence photo of meter
  is_estimated: Boolean, default False  -- true if meter was defective
  estimation_method: String(50), nullable  -- "3-month average" etc.
  created_at: DateTime

NEW: MayniladBill
  pk: UUID
  property_pk: UUID (FK → Property)
  billing_period: Date (1st of month)
  account_number: String(50)
  bill_date: Date
  due_date: Date
  total_amount: CurrencyDecimal       -- total master meter bill
  total_consumption_cu_m: Integer     -- master meter consumption
  basic_charge: CurrencyDecimal
  environmental_charge: CurrencyDecimal
  sewerage_charge: CurrencyDecimal
  fcda_amount: CurrencyDecimal
  msc_amount: CurrencyDecimal
  vat_amount: CurrencyDecimal
  scan_url: String(500), nullable     -- scanned copy for tenant requests

NEW: MayniladRateSchedule
  pk: UUID
  effective_from: Date
  effective_until: Date, nullable
  customer_type: Enum(RESIDENTIAL, SEMI_BUSINESS, COMMERCIAL, INDUSTRIAL)
  tiers: JSONB                        -- array of { bracket_start, bracket_end, rate_per_cu_m }
  environmental_charge_pct: Decimal(4,4)  -- 0.2500 = 25%
  sewerage_charge_pct: Decimal(4,4)       -- 0.2000 = 20% (commercial only)
  fcda_rate_per_cu_m: CurrencyDecimal     -- quarterly adjustment
  msc_amount: CurrencyDecimal             -- fixed monthly service charge

NEW: WaterBillingRun
  pk: UUID
  property_pk: UUID (FK → Property)
  billing_period: Date (1st of month)
  maynilad_bill_pk: UUID (FK → MayniladBill)
  rate_schedule_pk: UUID (FK → MayniladRateSchedule)
  run_date: DateTime
  status: Enum(DRAFT, FINALIZED)
  total_billed: CurrencyDecimal
  maynilad_total: CurrencyDecimal
  under_recovery: CurrencyDecimal     -- landlord absorbs
  common_area_consumption_cu_m: Integer
  common_area_cost: CurrencyDecimal
  allocation_method: Enum(BY_FLOOR_AREA, EQUAL_SPLIT)

NEW: WaterCharge (extends Charge or separate table)
  pk: UUID
  charge_pk: UUID (FK → Charge)       -- links to main billing Charge
  water_billing_run_pk: UUID (FK → WaterBillingRun)
  meter_pk: UUID (FK → WaterMeter)
  consumption_cu_m: Integer
  previous_reading: Integer
  current_reading: Integer
  basic_charge: CurrencyDecimal
  environmental_charge: CurrencyDecimal
  sewerage_charge: CurrencyDecimal
  fcda_amount: CurrencyDecimal
  msc_share: CurrencyDecimal
  is_common_area_allocation: Boolean, default False
  co_tenant_share_ratio: Decimal(3,2), default 1.00

Rentable (enhanced — if not already added)
  + unit_type: Enum(COMMERCIAL, RESIDENTIAL), NOT NULL
  + floor_area_sqm: Decimal(8,2), nullable  -- for common area allocation

Property (enhanced)
  + is_sewered: Boolean, default False
  + common_area_water_allocation: Enum(BY_FLOOR_AREA, EQUAL_SPLIT)
```

### 7.2 Rate Table Structure (JSONB)

```json
{
  "tiers": [
    { "bracket_start": 0,  "bracket_end": 10, "rate_per_cu_m": "10.00" },
    { "bracket_start": 10, "bracket_end": 20, "rate_per_cu_m": "17.46" },
    { "bracket_start": 20, "bracket_end": 30, "rate_per_cu_m": "30.80" },
    { "bracket_start": 30, "bracket_end": 40, "rate_per_cu_m": "45.50" },
    { "bracket_start": 40, "bracket_end": null, "rate_per_cu_m": "52.00" }
  ]
}
```

**Note:** Actual Maynilad per-tier rates must be extracted from the official Maynilad tariff PDF at ro.mwss.gov.ph. The rates above are illustrative. Rate tables need quarterly updates (FCDA) and annual updates (RAL adjustments).

### 7.3 Water Billing Run Flow

```
1. PRECONDITIONS
   - MayniladBill for billing_period exists and is recorded
   - MayniladRateSchedule for billing_period exists (correct tier rates)
   - WaterMeterReadings for billing_period exist for all active meters

2. CREATE WaterBillingRun (status=DRAFT)

3. FOR each WaterMeter WHERE status=ACTIVE AND meter_type=UNIT:
   a. Get current + previous readings
   b. Compute consumption delta
   c. Validate: delta >= 0, delta < 3x previous month
   d. Apply per-tier rate computation (Section 4.1 algorithm)
   e. Apply co-tenant split if shared meter
   f. Create WaterCharge record
   g. Create corresponding Charge record (charge_type=WATER, vat_rate=0.0000)

4. COMPUTE COMMON AREA
   a. Sum all COMMON_AREA meter consumption
   b. Compute cost using per-tier method
   c. Allocate to active tenants (by floor area or equal split)
   d. Create WaterCharge records with is_common_area_allocation=True
   e. Create corresponding Charge records as separate line items

5. RECONCILIATION CHECK
   a. total_billed = sum(all WaterCharges)
   b. ASSERT total_billed <= maynilad_bill.total_amount
   c. Record under_recovery = maynilad_total - total_billed

6. FINALIZE
   a. Set WaterBillingRun.status = FINALIZED
   b. WaterCharges now appear in monthly billing statements
   c. Store Maynilad bill scan URL for tenant requests
```

### 7.4 Meter Reading Input Workflow

```
1. Property manager opens meter reading form (mobile-friendly)
2. Select billing period
3. For each meter:
   a. Display: meter name, previous reading, previous consumption
   b. Input: current reading (integer)
   c. Optional: photo upload of meter face
   d. Validation:
      - current >= previous (flag rollover if not)
      - delta < 3x last month's delta (flag outlier)
      - Defective meter: mark as estimated, enter estimate
4. Submit all readings
5. System computes consumption deltas and flags anomalies
6. Manager reviews flagged meters, confirms or corrects
7. Readings are locked for billing
```

### 7.5 Integration with Monthly Billing

Water charges integrate into the monthly billing flow (see `analysis/monthly-billing-generation.md`):
- Water charges are created as `Charge` records with `charge_type=WATER`
- Common area water charges are `Charge` records with `charge_type=COMMON_AREA_WATER`
- Both appear as line items on the tenant's monthly billing statement
- VAT: water pass-through is NOT VATable (`vat_rate=0.0000`)
- Water billing typically runs 5-15 days after rent billing (waiting for Maynilad bill)
- Separate invoice number series not needed — water charges join the same invoice as rent

---

## 8. Automability Score: 4 / 5

**Justification:** Water billing is **highly automatable** once readings are entered — the per-tier computation, surcharge calculations, common area allocation, and reconciliation are purely deterministic. However, it falls short of a perfect 5 due to:

**Human judgment required:**
- **Meter reading entry** — physical meters must be read by a person (until smart meters are installed)
- **Defective meter decisions** — choosing between estimated billing, zero billing, or fixed charge requires judgment
- **Anomaly resolution** — flagged readings (negative, implausible) require human investigation
- **Rate table updates** — Maynilad rate changes must be manually entered (quarterly FCDA, annual RAL)
- **Co-tenancy changes** — updating meter-tenant assignments when co-tenants change

**Fully automatable components (score 5 within themselves):**
- Per-tier rate computation from readings
- Environmental/Sewerage charge calculation
- Common area allocation (deterministic formula)
- Reconciliation check (total <= master bill)
- Charge record creation and billing statement generation
- Reading validation and anomaly detection

---

## 9. Verification Status

| Rule | Status | Sources |
|---|---|---|
| No-markup rule (strict pass-through) | **CONFIRMED** | MWSS RO Res. 2016-010, RA 7581, RA 7394, Respicio & Co. |
| Per-tier billing method required | **CONFIRMED** | MWSS RO Customer Service Regulations, Respicio & Co., MWSS RO refund orders |
| Common area as separate line item | **CONFIRMED** | MWSS regulations, legal commentary |
| Environmental Charge 25% (2025+) | **CONFIRMED** | Maynilad official rate notice (Dec 2024), GMA News, Philstar |
| Sewerage 20% Commercial only | **CONFIRMED** | Maynilad rate schedule, MWSS RO |
| Billing statement content requirements | **CONFIRMED** | MWSS Customer Service Regulations, legal commentary |
| Master bill copy within 5 days | **CONFIRMED** | MWSS regulations, legal commentary |
| Refund within 1 cycle + 6% interest | **CONFIRMED** | Civil Code Art. 2154, BSP Circular 799, MWSS |
| Sub-meter PNS/BPS certification | **CONFIRMED** | MWSS RO regulations |
| VAT on water pass-through (not VATable) | **CONFIRMED** | BIR RR 16-2005, tax advisory sources |
| Defective meter estimated billing | **UNVERIFIED** | No authoritative source for sub-metering context; industry practice only |

10 of 11 rules confirmed against 2+ independent sources. 1 rule (estimated billing for defective meters) unverified — documented as industry practice without regulatory backing.
