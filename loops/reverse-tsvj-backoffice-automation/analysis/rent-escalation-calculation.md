# Rent Escalation Calculation — Process Analysis & Feature Spec

## Process Description

**What:** Computing annual rent increases for all active leases — residential controlled units (capped by NHSB resolution) and commercial units (contractual rate, no cap).

**When:** At each lease anniversary date. Not calendar year — the increase triggers on the anniversary of the lease start date. The NHSB cap applicable is determined by which calendar year the anniversary falls in.

**Who:** Currently done manually by the property manager. For controlled units, the manager must look up the current NHSB cap and apply it. For commercial units, the manager references the escalation clause in the lease contract.

**Frequency:** Annual per lease. With ~20-100 units, this means 20-100 escalation events spread throughout the year (each on its own anniversary date).

---

## Current Method

**Manual / spreadsheet.** The property manager:
1. Tracks lease anniversary dates in a spreadsheet or calendar
2. Looks up whether the unit is rent-controlled or commercial
3. For controlled: applies the current NHSB cap percentage to the current rent
4. For commercial: reads the escalation clause from the lease contract (fixed %, CPI-linked, or stepped)
5. Updates the billing amount for the next period
6. No systematic check for threshold crossing (controlled unit graduating out of rent control)

**Pain points:** Easy to miss anniversary dates, apply wrong year's cap, or forget to update billing. No audit trail of which rate was applied when.

---

## Regulatory Rules

### A. Residential Controlled Units (RA 9653 + NHSB)

**Coverage:** Residential units ≤ P10,000/month in NCR (Las Piñas), same continuing tenant.

**Two-layer system:**

| Layer | Source | Rule |
|-------|--------|------|
| Cap percentage | NHSB Resolution (calendar year) | 2.3% for 2025, 1% for 2026 (NHSB 2024-01) |
| Frequency | RA 9653 Section 4 | No more than once per 12 months per unit |

**Application:** The cap percentage is set per calendar year by the NHSB. The frequency rule operates per lease cycle. A lease with a July anniversary applies the cap in effect for the calendar year the anniversary falls in — e.g., July 2025 anniversary → 2.3% cap; July 2026 anniversary → 1% cap.

**Base for increase:** The increase applies to the **current monthly rent** (last lawful rate), not the original base rent. This creates compounding over multiple years.

**Formula (controlled):**
```
new_rent = current_rent × (1 + nhsb_cap_rate)
```

**Example — P8,000/month lease starting March 2024:**

| Anniversary | Calendar Year | NHSB Cap | Computation | New Rent |
|-------------|---------------|----------|-------------|----------|
| Mar 2025 | 2025 | 2.3% | 8,000 × 1.023 | P8,184.00 |
| Mar 2026 | 2026 | 1.0% | 8,184 × 1.01 | P8,265.84 |
| Mar 2027 | 2027 | TBD (new NHSB resolution needed) | — | — |

**Vacancy decontrol (RA 9653 Section 4):** When a unit becomes vacant (tenant leaves), the lessor may set any initial rent for the new tenant. Once the new tenant occupies, subsequent increases are capped again.

**Legal citations:**
- RA 9653 Section 4 (escalation cap and vacancy decontrol)
- RA 9653 Section 5 (coverage brackets: NCR ≤ P10,000)
- NHSB Resolution 2024-01 (2.3% for 2025, 1% for 2026)
- Civil Code Art. 1305 (freedom of contract — general principle, but overridden by RA 9653 for covered units)

### B. Commercial Units (Civil Code Only)

**No statutory cap.** Commercial leases are explicitly excluded from RA 9653 (Section 11). Escalation is governed entirely by the lease contract under freedom of contract (Civil Code Art. 1305).

**Common escalation patterns in PH commercial leases:**

| Pattern | Description | Example |
|---------|-------------|---------|
| Fixed percentage | Flat % increase per year | 5% annually |
| Stepped | Different rates for different years | 3% Y1-Y3, 5% Y4-Y5 |
| CPI-linked | Tied to PSA Consumer Price Index | CPI + 2%, floor 3% |
| Market reset | Adjusted to market rate at renewal | Re-negotiated every 3 years |
| Flat (no escalation) | Same rent throughout term | Common for short-term leases |

**CPI-linked escalation:** No Philippine statute mandates CPI-linked increases. CPI linkage is purely contractual. The Philippine Statistics Authority (PSA) publishes monthly CPI data. When a lease specifies CPI-linked escalation, the formula and reference period must be explicitly defined in the contract.

**Formula (commercial — fixed %):**
```
new_rent = current_rent × (1 + contractual_rate)
```

**Formula (commercial — CPI-linked, typical clause):**
```
cpi_increase = (CPI_current_month / CPI_base_month) - 1
escalation_rate = max(cpi_increase + spread, floor_rate)
new_rent = current_rent × (1 + escalation_rate)
```

**Legal citations:**
- RA 9653 Section 11 (commercial exclusion)
- Civil Code Art. 1305 (freedom of contract)
- Civil Code Art. 1306 (stipulations not contrary to law, morals, public order)
- Civil Code Art. 1159 (obligations from contracts have force of law)

### C. Threshold Crossing (Controlled → Uncontrolled)

**Critical edge case:** If lawful NHSB increases push a residential unit's rent above P10,000/month, the unit **exits rent control**. Future increases are no longer capped.

**Example:**
- Unit at P9,900/month in 2024
- 2025: P9,900 × 1.023 = P10,127.70 → **above P10,000 threshold**
- 2026: No NHSB cap applies — lessor may increase per contract terms

**Automation implication:** The system must flag units approaching the P10,000 threshold and track when they cross over.

### D. Boarding Houses / Dormitories

NHSB 2024-01 and RA 9653 Section 4 limit boarding houses to **one rent adjustment per calendar year**, even if the cap has not been fully utilized. Vacancy decontrol is limited — cannot re-price at vacancy if the annual adjustment has already been used.

---

## Edge Cases and Special Rules

1. **Mid-year NHSB resolution change:** If the NHSB publishes a new resolution mid-year, the new cap applies only from its stated effective date. Leases with anniversaries before the effective date use the old cap.

2. **No NHSB resolution for a given year:** If no resolution exists for a future year (e.g., 2027), the last published cap continues. RA 9653 Section 6 delegates this to the NHSB; absence of a resolution arguably freezes the last published rate (subject to legal interpretation).

3. **Tacit reconduction (month-to-month):** After a fixed-term lease expires and converts to month-to-month via Art. 1670, annual escalation still applies at the original anniversary date. The 12-month frequency rule still governs.

4. **Multiple rentables under one lease:** If a single lease covers multiple units (e.g., a tenant leasing 2 adjacent rooms), the escalation applies to the total lease rent. For rent control assessment, each unit's imputed rent should be checked against the P10,000 threshold individually.

5. **Rounding:** Crispina uses ROUND_DOWN (tenant-favorable). NHSB does not specify rounding direction. ROUND_DOWN is the defensible choice — it ensures the increase never exceeds the cap.

6. **Fractional peso amounts:** After escalation, rent may have centavo fractions (e.g., P8,265.84). Some lessors round to nearest peso for billing simplicity. The system should store the precise amount and allow optional display rounding.

7. **Retroactive escalation:** If the property manager misses an anniversary date, the new rate should apply from the anniversary date forward. Back-billing for the difference (between old and new rate) for months already billed at the old rate is a manual decision.

8. **Contractual escalation below NHSB cap:** A lease may specify 1% annual increase for a controlled unit when the NHSB cap is 2.3%. The contractual rate governs — the NHSB cap is a ceiling, not a floor.

---

## What Crispina Built

### Implemented ✅

| Feature | Implementation | Notes |
|---------|---------------|-------|
| Pre-computed escalation | `RecurringCharge` → `RecurringChargePeriod` | Periods created at lease start; rate per period stored permanently |
| Compound interest formula | `math.py: calculate_compound_interest()` | `base × (1 + rate)^years`, ROUND_DOWN |
| Lease anniversary splitting | `date.py: split_by_year()` | Uses `rrule.YEARLY` anchored to lease start date — correctly per-anniversary, not calendar year |
| Single escalation rate input | `RecurringChargeGenerate.yearly_increase_percent` | One fixed percentage for entire lease term |
| DB-enforced non-overlapping periods | `ExcludeConstraint` on `RecurringChargePeriod` | PostgreSQL GiST index prevents date range overlap |

### Design Strengths

1. **Pre-computed periods** = full audit trail. Every rate change is a permanent record.
2. **Lease-anniversary splits** correctly model NHSB's "per lease year" timing.
3. **ROUND_DOWN** is tenant-favorable and defensible.
4. **VAT rate stored at charge-time** — if VAT rules change, historical charges remain correct.

### Gaps ❌

| Gap | Impact | Priority |
|-----|--------|----------|
| No rent-control flag on Lease/Rentable | Cannot distinguish NHSB-capped vs commercial escalation | High |
| Single fixed escalation rate for entire term | Cannot model: stepped rates, CPI-linked, or year-by-year NHSB caps that change between resolution periods | High |
| No NHSB cap enforcement | Application layer does not validate that the rate ≤ NHSB cap for controlled units | High |
| No threshold crossing detection | System doesn't flag when controlled rent crosses P10,000 | Medium |
| No escalation schedule visibility | No dashboard showing upcoming anniversaries and expected new rates | Medium |
| No vacancy decontrol tracking | No mechanism to mark a unit as vacant (free-pricing) vs occupied (capped) | Medium |
| No CPI data integration | CPI-linked commercial leases would need manual rate entry each year | Low |
| No support for boarding house one-adjustment rule | No unit type classification for boarding house | Low |
| No lease event log | Cannot track when escalation was applied, missed, or overridden | Medium |

---

## Lightweight Feature Spec

### Data Model Additions

```
Rentable (existing — add fields):
  + unit_type: ENUM('residential', 'commercial', 'boarding_house')
  + is_rent_controlled: BOOLEAN (derived: residential AND current_rent ≤ P10,000)
  + floor_area_sqm: DECIMAL (needed for other processes)

Lease (existing — add fields):
  + escalation_type: ENUM('nhsb_cap', 'fixed_pct', 'stepped', 'cpi_linked', 'none')
  + escalation_params: JSONB  -- flexible storage for type-specific parameters
    -- fixed_pct: {"rate": 0.05}
    -- stepped: {"schedule": [{"year": 1, "rate": 0.03}, {"year": 4, "rate": 0.05}]}
    -- cpi_linked: {"spread": 0.02, "floor": 0.03, "base_period": "2025-01"}
    -- nhsb_cap: {} (rate looked up from NHSBCapRate table at computation time)
  + status: ENUM('active', 'expired', 'month_to_month', 'terminated')

NHSBCapRate (new table):
  pk: UUID
  year: INTEGER (UNIQUE)
  cap_rate: PercentageDecimal
  resolution_number: VARCHAR  -- e.g., "NHSB 2024-01"
  effective_date: DATE
  notes: TEXT

RecurringChargePeriod (existing — add fields):
  + escalation_applied: BOOLEAN (default FALSE)
  + escalation_source: VARCHAR  -- e.g., "NHSB 2024-01 @ 2.3%", "Contract @ 5%"
  + previous_amount: CurrencyDecimal  -- rate before this escalation (audit trail)

EscalationEvent (new table — audit log):
  pk: UUID
  lease_pk: FK → Lease
  recurring_charge_pk: FK → RecurringCharge
  event_date: DATE (anniversary date)
  previous_rate: CurrencyDecimal
  new_rate: CurrencyDecimal
  escalation_type: VARCHAR  -- 'nhsb_cap', 'fixed_pct', 'cpi_linked', etc.
  escalation_rate_applied: PercentageDecimal
  nhsb_cap_rate_pk: FK → NHSBCapRate (nullable)
  threshold_crossed: BOOLEAN (default FALSE)
  notes: TEXT
  created_by: VARCHAR  -- 'system' or user identifier
```

### Escalation Logic (Pseudocode)

```python
def compute_escalation(lease, anniversary_date):
    current_rent = get_current_period_amount(lease)

    if lease.escalation_type == 'nhsb_cap':
        # Look up NHSB cap for the calendar year of the anniversary
        cap = NHSBCapRate.get(year=anniversary_date.year)
        if cap is None:
            raise EscalationError("No NHSB cap rate for {anniversary_date.year}")
        rate = cap.cap_rate

        # Check if contractual rate is lower (contract can be below cap)
        if lease.escalation_params.get('max_rate'):
            rate = min(rate, lease.escalation_params['max_rate'])

    elif lease.escalation_type == 'fixed_pct':
        rate = lease.escalation_params['rate']

    elif lease.escalation_type == 'stepped':
        lease_year = compute_lease_year(lease.date_start, anniversary_date)
        schedule = lease.escalation_params['schedule']
        rate = lookup_stepped_rate(schedule, lease_year)

    elif lease.escalation_type == 'cpi_linked':
        params = lease.escalation_params
        cpi_rate = fetch_cpi_change(params['base_period'], anniversary_date)
        rate = max(cpi_rate + params['spread'], params['floor'])

    elif lease.escalation_type == 'none':
        return current_rent  # No escalation

    new_rent = round_down(current_rent * (1 + rate))

    # Threshold crossing check (residential only)
    threshold_crossed = False
    if lease.unit_type == 'residential' and current_rent <= 10000 and new_rent > 10000:
        threshold_crossed = True
        # Flag for review — unit exits rent control

    # Create audit record
    EscalationEvent.create(
        lease=lease,
        event_date=anniversary_date,
        previous_rate=current_rent,
        new_rate=new_rent,
        escalation_rate_applied=rate,
        threshold_crossed=threshold_crossed,
    )

    # Create new RecurringChargePeriod
    create_new_period(lease, anniversary_date, new_rent,
                      source=f"{escalation_type} @ {rate}")

    return new_rent
```

### Dashboard / Visibility Features

1. **Upcoming Escalations View:** List all leases with anniversaries in the next 30/60/90 days, showing current rent, escalation type, expected new rate, and threshold proximity.

2. **Threshold Proximity Alert:** Flag residential units where current rent is within 5% of P10,000 (i.e., ≥ P9,500). These may exit rent control at next escalation.

3. **Escalation History:** Per-lease log of all rate changes with dates, rates applied, and source (NHSB resolution number, contract clause).

4. **NHSB Rate Management:** Admin interface to enter new NHSB cap rates when resolutions are published. System alerts when a new calendar year has no NHSB rate configured.

### Inputs and Outputs

**Inputs:**
- Lease record (start date, escalation type, escalation params)
- Current rent amount (from latest RecurringChargePeriod)
- NHSB cap rate table (for controlled units)
- CPI data from PSA (for CPI-linked commercial leases — manual entry or API)

**Outputs:**
- New RecurringChargePeriod record with updated amount
- EscalationEvent audit record
- Threshold crossing alert (if applicable)
- Updated billing amount for next month's statement generation

---

## Automability Score: 4/5

**Justification:**

| Component | Automability | Notes |
|-----------|-------------|-------|
| Fixed % escalation (commercial) | 5/5 | Purely deterministic: current_rent × (1 + rate) |
| NHSB-capped escalation (residential) | 4/5 | Deterministic formula, but requires manual entry of new NHSB cap rates each resolution cycle |
| Stepped escalation | 5/5 | Deterministic lookup from schedule |
| CPI-linked escalation | 3/5 | Requires external CPI data (manual entry or PSA API); formula is deterministic once CPI is available |
| Threshold crossing detection | 5/5 | Purely arithmetic comparison |
| Anniversary date tracking | 5/5 | Date arithmetic |
| Vacancy decontrol pricing | 2/5 | Lessor sets rate — human judgment required |

**Overall: 4/5** — The core computation is fully deterministic. The two human-judgment elements are: (1) entering new NHSB cap rates when published (annual, low-effort), and (2) setting initial rent for vacancy decontrol units. CPI data entry is a data availability issue, not a judgment issue.

---

## Verification Status

**All regulatory rules verified against 2+ independent sources.** ✅

| Rule | Status | Sources |
|------|--------|---------|
| NHSB 2024-01 caps (2.3% / 1%) | Confirmed | PNA, Tribune, DHSUD PDF, Respicio |
| Escalation on current rent (compounding) | Confirmed | Respicio (2 articles), Salenga Law |
| Two-layer system (calendar cap + lease frequency) | Confirmed with nuance | Respicio, Lamudi |
| Threshold crossing exits rent control | Confirmed | Respicio, JLP Law |
| Commercial: no cap, Art. 1305 | Confirmed | Respicio, RichestPH |
| CPI-linkage: purely contractual | Confirmed | Respicio, RichestPH, LawPhil |
| Vacancy decontrol: new tenant = free pricing | Confirmed | PNA, LawPhil (RA 9653 §4), PIDS |
| Boarding house: one adjustment/year | Confirmed | SC E-Library, PNA, GMA News |

**Correction applied:** The correct Civil Code article for freedom of contract is **Art. 1305** (not Art. 1306 as cited in some earlier analysis files). Art. 1306 addresses validity of stipulations; Art. 1305 defines the principle of autonomy in contracts.

---

*Analyzed: 2026-02-26 | Sources: input/rent-control-rules.md, input/crispina-models.md, input/crispina-services.md, input/corporate-rental-tax.md + verification subagent (8 claims, 2-4 sources each)*
