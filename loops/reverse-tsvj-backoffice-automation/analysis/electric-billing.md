# Electric Billing

**Wave:** 2 (Process Analysis & Feature Spec)
**Analyzed:** 2026-02-26
**Dependencies:** crispina-models, crispina-services, utility-billing-regulations, corporate-rental-tax

---

## 1. Process Description

**What:** Apportion the monthly Meralco master meter bill across tenants using individual sub-meter readings. Each tenant receives an electricity charge based on their actual kWh consumption multiplied by the effective per-kWh rate from the master bill. Common area electricity (hallways, lobby, water pumps, landscaping lights) is allocated separately.

**When:** Monthly, after the Meralco bill for the billing period is received and all sub-meter readings are collected. Meralco billing cycles are monthly; bill typically arrives 5-10 days after the meter reading date.

**Who does it:** Property manager (or designated staff). Currently: reads sub-meters, records readings on paper or spreadsheet, manually divides the Meralco bill proportionally among tenants, prepares electric charge lines for the monthly billing statement.

**Frequency:** Monthly for all sub-metered tenants. The TSVJ property has mixed commercial (Floor 1) and residential (Floor 3) tenants, all served by a single Meralco master meter.

---

## 2. Current Method

**Manual spreadsheet.** The property manager:

1. Receives the Meralco master bill (paper or online via Meralco.com.ph)
2. Physically reads each tenant's sub-meter, recording the reading
3. Computes each tenant's kWh consumption (current reading - previous reading)
4. Computes the effective blended rate: Meralco total bill / total kWh on master meter
5. Multiplies each tenant's kWh by the blended rate
6. Manually adds a common area share (method varies — sometimes blended in, sometimes separate)
7. Transfers charges to billing statements or collection sheets

**No Crispina code exists for electric billing** — zero search results for "electric", "meralco", "kwh", "electricity", or "submeter" in the tsvjph/crispina codebase. This is entirely a manual spreadsheet process.

---

## 3. Regulatory Rules

### 3.1 No-Markup Rule (Strict Pass-Through)

Landlords may only charge tenants the actual per-kWh cost billed by Meralco. No markup, surcharge, or profit margin is permitted.

**Legal basis:**
- **EPIRA (RA 9136), Section 43** — ERC has exclusive authority to regulate electricity rates; non-utility entities cannot charge beyond ERC-allowed rates
- **ERC Resolution No. 12, Series of 2009** — primary regulation governing sub-metering; emphasizes pass-through principle
- **ERC Resolution No. 21, Series of 2010** — updated guidelines reinforcing the no-markup rule for sub-metered electricity (corrected citation; ERC Res. 08 Series of 2022 covers transmission wheeling rates, not sub-metering)
- **RA 7394 (Consumer Act), Article 52** — unconscionable pricing is an unfair trade practice
- **Civil Code Arts. 19-21** — prohibits abusive conduct and unjust enrichment

**Verification:** CONFIRMED with citation correction — ERC Res. 08/2022 is not the correct sub-metering regulation; ERC Res. 21/2010 is. Core no-markup principle confirmed across 3+ sources (Respicio & Co., Lawyer-Philippines.com, ERC official resolutions).

### 3.2 Billing Method: Blended Rate (Accepted for Electricity)

The legally accepted billing method for sub-metered electricity is:

```
Tenant's Bill = (Tenant's kWh consumption) × (Total Meralco Bill ÷ Total Master Meter kWh)
```

This "blended rate" method is the **standard and accepted** approach for electricity — critically different from water, where the per-tier method is mandatory. The difference exists because:
- Meralco's rate is already a blended all-in rate (generation + transmission + distribution + taxes) applied uniformly per kWh to the master meter
- There is no equivalent of Maynilad's progressive block-rate tiers that would disadvantage light consumers under a blended approach
- ERC sub-metering guidelines endorse the pass-through of the actual per-kWh cost

Best practice is to itemize the Meralco bill components (generation, distribution, transmission, etc.) on the tenant's billing statement for transparency, but the single blended per-kWh rate is legally sufficient.

**Verification:** CONFIRMED — blended rate formula is correct and lawful for electricity sub-metering

### 3.3 Administrative / Service Fees

Landlords **may** charge a reasonable administrative/service fee for the sub-metering setup, **only if**:
- Explicitly agreed upon in the rental contract
- The fee is "reasonable and transparent"
- It does not result in an effective per-kWh charge materially above Meralco's actual rate

**Important nuances (from verification):**
- No published ERC regulation establishes a specific peso per-kWh cap
- However, informal ERC reference ranges of approximately PHP 1.00-1.50/kWh exist in adjudicated cases
- A draft cap of PHP 0.50/kWh has been under ERC consideration
- The ERC has penalized specific admin fee arrangements (ERC Case 2013-091)
- In practice, any fee that results in a materially higher effective rate is treated as profiteering

**Legal basis:** ERC Resolution No. 12 (2009), contractual freedom under Civil Code Art. 1306 (subject to reasonableness)

**Verification:** CONFIRMED with nuance — admin fees are permissible but the "no cap" characterization overstates; informal reference ranges exist and the ERC has penalized excessive fees

### 3.4 Common Area Electricity

Common area electricity (hallways, lobby, water pumps, landscaping lights, parking lights) is a **landlord cost**. Options:

**Option A: Absorb as operating expense** — include in base rent. Simplest approach; no monthly allocation needed.

**Option B: Apportion at cost** — allocate among tenants proportionally as a **separate line item**. Methods:
- By floor area ratio: `tenant floor area / total rentable area × common area kWh cost`
- By equal split per unit (if units are similarly sized)
- By consumption share (tenant's kWh / total tenant kWh × common area cost)

**Key constraint:** Common area electricity **cannot be embedded as a per-kWh markup** on unit consumption — must be segregated as a separate line item.

**Total recovery check:** Sum of all tenant charges (unit consumption + common area share) **must not exceed** the total Meralco master bill for the period. Any surplus from rounding/vacancy must be absorbed by the landlord.

**Verification:** CONFIRMED — fully supported by multiple sources

### 3.5 Lifeline Rate Disqualification

Individual sub-metered tenants consuming ≤100 kWh **cannot** claim Meralco's lifeline rate (up to 5% discount). This is for three distinct reasons:

1. **Customer-of-record requirement** — lifeline eligibility attaches to the Meralco account holder (the landlord/corporation), not individual sub-metered occupants
2. **RA 11552 exclusion** — condominium and subdivision dwellings are excluded from lifeline subsidies
3. **Means-testing** — lifeline programs increasingly require 4Ps membership or below-poverty-threshold proof, which is assessed at the account level

The master meter's aggregate consumption (always >>100 kWh for a multi-unit building) further ensures disqualification, but this is not the primary legal basis.

**Verification:** CONFIRMED with correction — conclusion is correct but reasoning should cite customer-of-record and RA 11552 rather than consumption threshold alone

### 3.6 VAT Treatment of Electricity Pass-Throughs

**CONFLICTING — requires careful handling.**

The initial input claimed that utility pass-throughs are subject to 12% VAT as part of gross receipts, with 5% EWT also applying. Verification revealed this is **materially incorrect as a blanket rule**:

- **EOPT Act (RA 11976)** and **Supreme Court jurisprudence (CIR v. Tours Specialists, Inc.)** establish that at-cost reimbursements, properly documented and segregated from rent, are **excluded** from VATable gross receipts
- The exclusion requires: (a) separate billing/documentation from rent, (b) amounts exactly matching the utility bill, (c) landlord acting purely as conduit
- If the landlord adds ANY markup or admin fee, the entire electricity charge may become a VATable service

**Practical implications for billing system design:**
- Support **segregated invoicing**: separate line items (or separate OR) for rent vs. utilities
- If electricity is billed strictly at cost with transparent derivation from the Meralco bill, it is excludable from VAT
- If electricity is bundled into "all-in rent" or includes admin fees, the entire amount becomes VATable
- **EWT treatment** also depends on billing structure: at-cost pass-throughs may attract only 2% EWT (WC170 — reimbursement) rather than 5% EWT (WC160 — rental)

**Legal basis:** RA 11976 (EOPT Act), CIR v. Tours Specialists Inc. (G.R. No. 183933), BIR RR 16-2005

**Verification:** CONFLICTING — blanket VAT claim contradicted by EOPT Act and SC jurisprudence. The billing system should support both treatments and let the accountant/tax advisor determine the correct approach for this specific corporation.

### 3.7 System Loss Cap

ERC has capped recoverable system losses at **8.5% of total kWh purchased/generated** per ERC Resolution No. 17, Series of 2008 (reduced from the previous 9.5% under RA 7832). This affects the total Meralco bill but is transparent to the sub-metering calculation — it's already embedded in the master bill.

**Verification:** CONFIRMED — straightforwardly confirmed; cap is on kWh percentage, not peso amount

### 3.8 Prohibited Practices

- Charging a fixed monthly flat rate disconnected from actual consumption
- Using the highest tier rate when the building's consumption doesn't justify it
- Adding admin fees that inflate the effective per-kWh rate materially above Meralco's published rate
- Using uncalibrated or unsealed sub-meters
- Disconnecting a tenant's power for non-payment of rent (separate from electric charges)

### 3.9 Tenant Rights

- Right to inspect the sub-meter at reasonable times
- Right to request a copy of the Meralco master bill
- Right to contest readings and request meter testing
- **Refund** of over-collected amounts with **6% per annum** interest (solutio indebiti, Civil Code Art. 2154; BSP Circular 799)
- File complaints with: ERC Consumer Affairs Service (administrative), DTI (consumer protection), Small Claims Court up to PHP 1M

**Landlord penalties for overcharging:**
- ERC administrative fines
- Court-ordered refunds with 6% p.a. interest
- LGU business permit revocation
- Estafa under the Revised Penal Code if fraudulent intent and meter fabrication (People v. Isidoro, G.R. No. 188576)

---

## 4. Formula / Decision Tree

### 4.1 Blended-Rate Electric Billing Algorithm

```
FUNCTION compute_electric_bill(tenant, billing_period):

  -- 1. GET READINGS
  current_reading = get_sub_meter_reading(tenant.electric_meter, billing_period)
  previous_reading = get_sub_meter_reading(tenant.electric_meter, billing_period - 1)
  consumption_kwh = current_reading - previous_reading

  IF consumption_kwh < 0:
    RAISE "Negative consumption — possible meter rollover or reading error"
  IF consumption_kwh == 0:
    RETURN zero_charge(tenant, billing_period)

  -- 2. GET MERALCO BILL DATA
  meralco_bill = get_meralco_bill(billing_period)
  master_kwh = meralco_bill.total_kwh
  master_amount = meralco_bill.total_amount  -- VAT-inclusive total billed by Meralco

  -- 3. COMPUTE EFFECTIVE PER-KWH RATE
  effective_rate = master_amount / master_kwh
  -- This automatically captures all components: generation, transmission,
  -- distribution, system loss, universal charges, FIT-All, VAT, franchise tax

  -- 4. COMPUTE TENANT'S ELECTRICITY CHARGE
  unit_charge = consumption_kwh * effective_rate

  -- 5. ADMIN FEE (if contractually agreed)
  IF lease.has_electric_admin_fee:
    admin_fee = lease.electric_admin_fee_per_month  -- fixed peso, NOT per-kWh
  ELSE:
    admin_fee = Decimal("0.00")

  -- 6. TOTAL
  total = unit_charge + admin_fee

  -- 7. ROUND (ROUND_DOWN consistent with main server)
  total = round_currency(total)

  RETURN ElectricCharge(
    tenant=tenant,
    billing_period=billing_period,
    consumption_kwh=consumption_kwh,
    effective_rate_per_kwh=effective_rate,
    unit_charge=unit_charge,
    admin_fee=admin_fee,
    total=total,
    previous_reading=previous_reading,
    current_reading=current_reading,
    meralco_bill_pk=meralco_bill.pk
  )
```

### 4.2 Common Area Electricity Allocation

```
FUNCTION allocate_common_area_electricity(billing_period):

  -- 1. COMPUTE COMMON AREA CONSUMPTION
  total_tenant_kwh = sum(consumption_kwh FOR each tenant meter)
  meralco_total_kwh = get_meralco_bill(billing_period).total_kwh
  common_area_kwh = meralco_total_kwh - total_tenant_kwh
  -- Includes: hallways, lobby, pumps, parking, landscaping, any unmetered space

  IF common_area_kwh < 0:
    RAISE "Sub-meter total exceeds master meter — calibration issue"

  -- 2. COMPUTE COMMON AREA COST
  effective_rate = meralco_bill.total_amount / meralco_bill.total_kwh
  common_area_cost = common_area_kwh * effective_rate

  -- 3. ALLOCATE TO TENANTS
  allocation_method = property.common_area_electric_allocation

  IF allocation_method == BY_FLOOR_AREA:
    FOR each tenant IN active_tenants:
      share = tenant.rentable.floor_area_sqm / total_rentable_floor_area
      tenant_common_charge = common_area_cost * share

  ELSE IF allocation_method == EQUAL_SPLIT:
    per_unit_share = common_area_cost / active_unit_count
    FOR each tenant: tenant_common_charge = per_unit_share

  ELSE IF allocation_method == ABSORBED:
    -- Landlord absorbs; no allocation to tenants
    RETURN []

  -- 4. RETURN AS SEPARATE LINE ITEMS
  RETURN [CommonAreaElectricCharge(tenant, amount, billing_period) FOR each tenant]
```

### 4.3 Reconciliation Check

```
FUNCTION verify_electric_recovery(billing_period):

  total_tenant_charges = sum(all unit charges + common area allocations + admin fees)
  meralco_master_bill = get_meralco_bill(billing_period).total_amount

  -- Total from unit + common area (excluding admin fees) must not exceed master bill
  total_pass_through = total_tenant_charges - total_admin_fees
  IF total_pass_through > meralco_master_bill:
    RAISE "Over-recovery: billed tenants PHP {total_pass_through} " +
          "but Meralco charged PHP {meralco_master_bill}."

  under_recovery = meralco_master_bill - total_pass_through
  LOG "Under-recovery for {billing_period}: PHP {under_recovery}"
  -- Under-recovery from vacant units, rounding is landlord cost
```

---

## 5. Edge Cases and Special Rules

### 5.1 No Equivalent of Water's Per-Tier Issue

Unlike water billing, electricity sub-metering does **not** have a per-tier vs. blended rate controversy. The blended rate (total bill / total kWh) is the accepted method. This is because Meralco applies a uniform rate structure to the master meter — there is no progressive block-rate that would shift higher-tier costs unfairly.

### 5.2 Rate Classification: Residential vs. Commercial Master Meter

If the TSVJ property has both commercial (Floor 1) and residential (Floor 3) tenants, the master meter may be classified as **commercial** by Meralco. This affects:
- The distribution charge rate (commercial rates differ from residential)
- The per-kWh blended rate passed through to all tenants

The rate classification does **not** change the sub-metering rules — the blended formula (total bill / total kWh) remains the same regardless. However, residential tenants effectively pay at the commercial rate if the master meter is commercially classified. This is a known issue with no regulatory remedy — it is inherent to mixed-use properties on a single master meter.

**Mitigation:** If the property could obtain **separate master meters** (one commercial, one residential), each group would get its correct rate classification. This is a capital decision, not a billing system feature.

### 5.3 Meralco Rate Fluctuations

Meralco rates fluctuate monthly based on generation charge movements (PHP 12.29-13.47/kWh across 2025). The blended rate method automatically captures these fluctuations because it's computed fresh each month from the actual bill. No rate table maintenance is needed (unlike water, which requires Maynilad tier rate updates).

### 5.4 Shared Meters (Co-Tenancy)

If a sub-meter serves multiple tenants (e.g., subdivided units):
- Compute total bill for the meter using blended rate
- Divide among co-tenants per co-tenancy agreement (typically equal split or by floor area)
- Each co-tenant's statement shows the meter reading + their share

### 5.5 Defective or Missing Sub-Meters

When a sub-meter is defective, non-functional, or absent:
- **Estimated billing:** Use the average of the last 3 months' consumption (no specific ERC regulation, but standard industry practice — same as water)
- **Fixed allowance:** Lease may specify a fixed monthly kWh allowance for estimating during defective-meter periods
- **Zero billing:** Unacceptable — the tenant's unmetered consumption gets absorbed into the blended rate, unfairly increasing costs for other tenants
- Flag meter as defective and schedule replacement/calibration

### 5.6 Negative or Implausible Readings

- Reject negative deltas (current < previous) — flag for meter rollover or data entry error
- For rollovers: `(max_meter_value - previous_reading) + current_reading`
- For implausibly high readings (> 3x previous month): flag for confirmation before billing

### 5.7 Vacant Units

- Vacant units are not billed for electricity, but sub-meters should still be monitored
- Any consumption on vacant units (e.g., left-on appliances) is a landlord cost
- Under the blended rate method, vacant-unit consumption is part of the common area remainder

### 5.8 New Tenant Mid-Month

- Take a move-in sub-meter reading
- First billing period: from move-in reading to next regular reading
- Pro-rate admin fee (if applicable) to the partial month

### 5.9 Admin Fee Design Choices

Given the regulatory sensitivity around admin fees:
- Recommended: **fixed peso amount per month** (not per-kWh), contractually agreed
- Amount should be modest (< PHP 200/month for residential) to avoid ERC scrutiny
- Must be shown as a separate line item, never blended into the per-kWh rate
- Alternatively: absorb sub-metering costs into base rent (simplest, safest)

### 5.10 Power Outages and Meralco Adjustments

- Meralco occasionally issues billing adjustments (refunds for overcharging, corrections)
- The system should support recording Meralco adjustments and passing them through to tenants proportionally
- A negative-amount electric charge row handles refunds

---

## 6. What Crispina Built

### Built: Nothing

**No electric billing code exists in the Crispina codebase.** Searches for "electric", "meralco", "kwh", "electricity", and "submeter" all returned zero results. Electric billing was not implemented, not even as a standalone tool (unlike water, which has the `water/` directory).

### Relevant Existing Infrastructure

While no electric-specific code exists, several Crispina patterns are directly applicable:

| Crispina Component | Applicability to Electric Billing |
|---|---|
| `ChargeType` model | Add "Electric" and "Common Area Electric" charge types |
| `Charge` model (base_amount + vat_rate_used) | Electric charges stored same way; vat_rate_used = 0.0000 for at-cost pass-throughs |
| `Transaction` (billing batch) | Electric charges join the same monthly billing transaction |
| `Rentable` model | Needs `floor_area_sqm` for common area allocation by floor area |
| `Property` model | Needs common area allocation method preference |
| Water calculator patterns | Delta-based readings, co-tenancy, ChargeRow format all reusable |

### Key Gap: No Sub-Meter Infrastructure

Unlike water (which has 33 meters modeled in the water calculator), there is no electric meter registry, no reading storage, no billing computation. Everything is greenfield.

---

## 7. Lightweight Feature Spec

### 7.1 Data Model

```
NEW: ElectricMeter
  pk: UUID
  name: String(50)                       -- e.g., "Unit 101", "Common Area F1"
  meter_serial: String(50), nullable     -- physical meter serial number
  property_pk: UUID (FK -> Property)
  room_pk: UUID (FK -> Room), nullable   -- null for common area meters (if separately metered)
  meter_type: Enum(UNIT, COMMON_AREA)    -- COMMON_AREA only if dedicated sub-meter exists
  status: Enum(ACTIVE, DEFECTIVE, DECOMMISSIONED)
  max_reading: Integer, default 99999    -- for rollover detection
  installed_date: Date, nullable
  last_calibration_date: Date, nullable
  notes: Text, nullable

NEW: ElectricMeterTenant (junction for co-tenancy / subdivided units)
  meter_pk: UUID (FK -> ElectricMeter)
  tenant_pk: UUID (FK -> Tenant)
  share_ratio: Decimal(3,2), default 1.00  -- 0.50 for 2 co-tenants
  effective_from: Date
  effective_until: Date, nullable
  UNIQUE(meter_pk, tenant_pk, effective_from)

NEW: ElectricMeterReading
  pk: UUID
  meter_pk: UUID (FK -> ElectricMeter)
  billing_period: Date (1st of month)
  reading_kwh: Integer                   -- absolute meter reading (kWh)
  reading_date: Date                     -- when physically read
  read_by: String(100), nullable
  photo_url: String(500), nullable
  is_estimated: Boolean, default False
  estimation_method: String(50), nullable  -- "3-month average" etc.
  created_at: DateTime

NEW: MeralcoBill
  pk: UUID
  property_pk: UUID (FK -> Property)
  billing_period: Date (1st of month)
  account_number: String(50)
  service_address: String(255)
  bill_date: Date
  due_date: Date
  total_amount: CurrencyDecimal          -- total master meter bill (VAT-inclusive)
  total_kwh: Integer                     -- total master meter consumption
  effective_rate_per_kwh: CurrencyDecimal(10,6)  -- computed: total_amount / total_kwh
  -- Bill component breakdown (optional, for transparency):
  generation_charge: CurrencyDecimal, nullable
  transmission_charge: CurrencyDecimal, nullable
  system_loss_charge: CurrencyDecimal, nullable
  distribution_charge: CurrencyDecimal, nullable
  supply_charge: CurrencyDecimal, nullable
  metering_charge: CurrencyDecimal, nullable
  universal_charges: CurrencyDecimal, nullable
  fit_all: CurrencyDecimal, nullable
  vat_amount: CurrencyDecimal, nullable
  franchise_tax: CurrencyDecimal, nullable
  adjustment_amount: CurrencyDecimal, default 0  -- Meralco corrections
  scan_url: String(500), nullable        -- scanned copy for tenant requests

NEW: ElectricBillingRun
  pk: UUID
  property_pk: UUID (FK -> Property)
  billing_period: Date (1st of month)
  meralco_bill_pk: UUID (FK -> MeralcoBill)
  run_date: DateTime
  status: Enum(DRAFT, FINALIZED)
  total_billed: CurrencyDecimal
  meralco_total: CurrencyDecimal
  under_recovery: CurrencyDecimal        -- landlord absorbs
  common_area_kwh: Integer
  common_area_cost: CurrencyDecimal
  allocation_method: Enum(BY_FLOOR_AREA, EQUAL_SPLIT, ABSORBED)
  total_admin_fees: CurrencyDecimal

NEW: ElectricCharge (extends Charge or separate table)
  pk: UUID
  charge_pk: UUID (FK -> Charge)         -- links to main billing Charge
  electric_billing_run_pk: UUID (FK -> ElectricBillingRun)
  meter_pk: UUID (FK -> ElectricMeter)
  consumption_kwh: Integer
  previous_reading: Integer
  current_reading: Integer
  effective_rate_per_kwh: CurrencyDecimal(10,6)
  unit_charge: CurrencyDecimal           -- consumption x rate
  admin_fee: CurrencyDecimal, default 0
  is_common_area_allocation: Boolean, default False
  co_tenant_share_ratio: Decimal(3,2), default 1.00

ENHANCED: Rentable (if not already added by water-billing)
  + floor_area_sqm: Decimal(8,2), nullable  -- for common area allocation

ENHANCED: Lease (admin fee configuration)
  + electric_admin_fee: CurrencyDecimal, nullable  -- monthly fixed fee, null = no fee

ENHANCED: Property
  + common_area_electric_allocation: Enum(BY_FLOOR_AREA, EQUAL_SPLIT, ABSORBED)
  + meralco_account_number: String(50), nullable
  + meralco_account_classification: Enum(RESIDENTIAL, COMMERCIAL), nullable
```

### 7.2 Electric Billing Run Flow

```
1. PRECONDITIONS
   - MeralcoBill for billing_period exists and is recorded
   - ElectricMeterReadings for billing_period exist for all active meters
   - effective_rate_per_kwh is computed (total_amount / total_kwh)

2. CREATE ElectricBillingRun (status=DRAFT)

3. FOR each ElectricMeter WHERE status=ACTIVE AND meter_type=UNIT:
   a. Get current + previous readings
   b. Compute consumption delta (kWh)
   c. Validate: delta >= 0, delta < 3x previous month
   d. Apply blended rate: unit_charge = consumption × effective_rate
   e. Apply co-tenant split if shared meter
   f. Add admin fee (if lease specifies)
   g. Create ElectricCharge record
   h. Create corresponding Charge record:
      - charge_type = ELECTRIC
      - vat_rate_used = 0.0000 (at-cost pass-through, not VATable)
        OR vat_rate_used = 0.1200 (if accountant determines pass-throughs
        should be VATable for this corporation)
      - base_amount = unit_charge + admin_fee

4. COMPUTE COMMON AREA (if not ABSORBED)
   a. common_area_kwh = master_kwh - sum(all unit meter consumption)
   b. common_area_cost = common_area_kwh × effective_rate
   c. Allocate to active tenants (by floor area or equal split)
   d. Create ElectricCharge records with is_common_area_allocation=True
   e. Create corresponding Charge records as separate line items

5. RECONCILIATION CHECK
   a. total_pass_through = sum(all unit_charges + common_area_allocations)
   b. ASSERT total_pass_through <= meralco_bill.total_amount
   c. Record under_recovery = meralco_total - total_pass_through
   d. Admin fees are EXCLUDED from reconciliation (they're above the Meralco bill)

6. FINALIZE
   a. Set ElectricBillingRun.status = FINALIZED
   b. Electric charges now appear in monthly billing statements
   c. Store Meralco bill scan URL for tenant requests
```

### 7.3 Meter Reading Input Workflow

Identical pattern to water meter readings (see `analysis/water-billing.md` Section 7.4):

```
1. Property manager opens meter reading form (mobile-friendly)
2. Select billing period
3. For each electric meter:
   a. Display: meter name, previous reading, previous consumption
   b. Input: current reading (integer, kWh)
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

### 7.4 Billing Statement Content

Each tenant's electric billing line should show:
1. Sub-meter previous reading and current reading
2. Consumption (kWh)
3. Meralco effective rate per kWh for the period
4. Unit electricity charge
5. Common area electricity share (if applicable, as separate line)
6. Admin fee (if applicable, as separate line)
7. Total electricity charge

Optional transparency items (from Meralco bill components):
- Generation, transmission, distribution charge breakdown
- Reference to Meralco bill date and period

### 7.5 Integration with Monthly Billing

Electric charges integrate into the monthly billing flow (see `analysis/monthly-billing-generation.md`):
- Electric charges are `Charge` records with `charge_type=ELECTRIC`
- Common area electric charges are `Charge` records with `charge_type=COMMON_AREA_ELECTRIC`
- Admin fees are included in the Electric charge amount (not a separate charge type)
- VAT treatment: configurable — either 0% (at-cost pass-through) or 12% (if accountant determines VATable); **flag for accountant decision**
- Electric billing can run on same cycle as rent (unlike water, which often lags)

---

## 8. Comparison: Electric vs. Water Billing

| Dimension | Electric | Water |
|---|---|---|
| **Billing method** | Blended rate (total / kWh) | Per-tier (each tenant starts at lowest bracket) |
| **Rate complexity** | Simple — one effective rate/month | Complex — tiered progressive rates, quarterly updates |
| **Rate table needed** | No — computed from each Meralco bill | Yes — MayniladRateSchedule with tier brackets |
| **Admin fees** | Permitted if contractual | Prohibited |
| **Common area** | By floor area, equal split, or absorbed | By floor area or equal split (not absorbed — must separate) |
| **Surcharges** | None (all embedded in blended rate) | Environmental 25%, Sewerage 20% (commercial only) |
| **VAT on pass-through** | Conflicting — depends on billing structure | Not VATable (pure conduit) |
| **Tenant type differentiation** | None for billing (rate classification at master meter level) | Required (Sewerage Charge for commercial only) |
| **Crispina code** | None | Standalone calculator (non-compliant method) |
| **Key regulatory risk** | Admin fee overcharging, profiteering | Per-tier method violation, PHP 87M+ in MWSS refunds |

---

## 9. Automability Score: 4 / 5

**Justification:** Electric billing is **highly automatable** once readings are entered — the blended-rate computation is simpler than water's per-tier method. A perfect score of 5 is precluded by:

**Human judgment required:**
- **Meter reading entry** — physical meters must be read by a person (until smart meters)
- **Defective meter decisions** — choosing between estimated billing or fixed allowance
- **Anomaly resolution** — flagged readings require human investigation
- **Admin fee configuration** — initial setup and amount require business decision
- **VAT treatment decision** — accountant must determine whether pass-throughs are VATable for this corporation
- **Common area allocation method** — initial choice of BY_FLOOR_AREA vs. EQUAL_SPLIT vs. ABSORBED

**Fully automatable components (score 5 within themselves):**
- Blended rate computation from Meralco bill
- Per-tenant charge calculation from readings
- Common area allocation (deterministic formula once method is chosen)
- Reconciliation check (total ≤ master bill)
- Charge record creation and billing statement generation
- Reading validation and anomaly detection
- Co-tenant share splitting

---

## 10. Verification Status

| Rule | Status | Sources |
|---|---|---|
| No-markup rule (strict pass-through) | **CONFIRMED** (citation corrected) | ERC Res. 12/2009, ERC Res. 21/2010, Respicio & Co., Lawyer-Philippines |
| Blended rate method accepted for electricity | **CONFIRMED** | ERC sub-metering guidelines, multiple legal commentaries |
| Admin fees permissible with contract | **CONFIRMED** (nuanced) | ERC Res. 12/2009, ERC Case 2013-091, Respicio & Co. |
| Common area as separate line item | **CONFIRMED** | ERC regulations, legal commentary |
| Lifeline disqualification for sub-metered units | **CONFIRMED** (reasoning corrected) | Meralco FAQs, RA 11552, Manila Bulletin |
| VAT on electricity pass-throughs | **CONFLICTING** | EOPT Act (RA 11976) vs. earlier BIR RRs; CIR v. Tours Specialists |
| System loss cap 8.5% | **CONFIRMED** | ERC Res. 17/2008, RA 7832, Philstar |
| Refund of over-collection + 6% interest | **CONFIRMED** | Civil Code Art. 2154, BSP Circular 799 |
| Estafa liability for fabricated readings | **CONFIRMED** | People v. Isidoro (G.R. No. 188576) |

8 of 9 rules confirmed against 2+ independent sources. 1 rule (VAT on pass-throughs) has conflicting authoritative sources — flagged for accountant/tax advisor determination. Detailed verification in `analysis/regulatory-verification-electric-billing.md`.
