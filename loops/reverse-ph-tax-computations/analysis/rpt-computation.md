# RPT Computation — Real Property Tax

**Wave:** 2 (Computation Extraction)
**Date:** 2026-02-26
**Verification status:** Confirmed (with documented conflicts from cross-check)
**Deterministic:** YES — fully deterministic once FMV, LGU, and property class are known

---

## Inputs

| Input | Type | Notes |
|---|---|---|
| `property_fmv_land` | Decimal (₱) | Land fair market value per assessor's Schedule of Market Values |
| `property_fmv_building` | Decimal (₱) | Building/improvement FMV (separate from land) |
| `property_fmv_machinery` | Decimal (₱) | Machinery FMV, if any |
| `land_classification` | Enum | Residential / Agricultural / Commercial / Industrial / Mineral / Timberland |
| `building_classification` | Enum | Residential / Agricultural / Commercial / Industrial |
| `machinery_use_class` | Enum | Agricultural / Residential / Commercial / Industrial |
| `lgu_type` | Enum | Province / City / Municipality-in-MM |
| `lgu_basic_rpt_rate` | Decimal (%) | Locally enacted rate (must be ≤ statutory cap) |
| `is_idle_land` | Boolean | Whether property meets RA 7160 Sec. 237 idle land definition |
| `idle_land_tax_rate` | Decimal (%) | Locally enacted idle land rate (0–5%) |
| `payment_date` | Date | For late penalty computation |
| `due_date` | Date | RPT is due in annual or quarterly installments; first installment due Jan 31 |

---

## Core Formula

```
Assessed Value (AV)  = FMV × Assessment Level (AL)
Basic RPT            = AV × Basic RPT Rate
SEF Levy             = AV × 1%
Total Annual RPT     = Basic RPT + SEF Levy
```

For multi-component properties (land + building + machinery):
```
AV_total = AV_land + AV_building + AV_machinery
Total Annual RPT = (AV_total × Basic RPT Rate) + (AV_total × 1%)
```

**Legal basis:** RA 7160 (Local Government Code) Secs. 199(g), 218, 233, 235.

---

## Assessment Level Tables

### Land (RA 7160 Section 218(a))

| Property Class | Maximum Assessment Level |
|---|---|
| Residential | **20%** |
| Agricultural | **40%** |
| Commercial | **50%** |
| Industrial | **50%** |
| Mineral | **50%** |
| Timberland | **20%** |

These are **statutory maximums**. LGUs may set lower levels by local ordinance. In practice most Metro Manila LGUs apply the maximum residential rate of 20%.

### Residential Buildings (RA 7160 Section 218(b)(1))

Complete 9-tier FMV bracket table, confirmed against LawPhil, DOF Local Assessment Regulations No. 1-92:

| FMV Over | FMV Not Over | Assessment Level |
|---|---|---|
| — | ₱175,000 | 0% |
| ₱175,000 | ₱300,000 | 10% |
| ₱300,000 | ₱500,000 | 20% |
| ₱500,000 | ₱750,000 | 25% |
| ₱750,000 | ₱1,000,000 | 30% |
| ₱1,000,000 | ₱2,000,000 | 35% |
| ₱2,000,000 | ₱5,000,000 | 40% |
| ₱5,000,000 | ₱10,000,000 | 50% |
| ₱10,000,000 | and above | 60% |

### Agricultural Buildings (RA 7160 Section 218(b)(2))

| FMV Over | FMV Not Over | Assessment Level |
|---|---|---|
| — | ₱300,000 | 25% |
| ₱300,000 | ₱500,000 | 30% |
| ₱500,000 | ₱750,000 | 35% |
| ₱750,000 | ₱1,000,000 | 40% |
| ₱1,000,000 | ₱2,000,000 | 45% |
| ₱2,000,000 | and above | 50% |

**Note:** Agricultural buildings max out at 50%, not 80%. The practitioner-guides source stated "50–80%" — this is incorrect. The 80% figure applies to commercial/industrial machinery, not agricultural buildings.

### Commercial/Industrial Buildings (DOF Local Assessment Regulations No. 1-92)

| FMV Over | FMV Not Over | Assessment Level |
|---|---|---|
| — | ₱300,000 | 30% |
| ₱300,000 | ₱500,000 | 35% |
| ₱500,000 | ₱750,000 | 40% |
| ₱750,000 | ₱1,000,000 | 50% |
| ₱1,000,000 | ₱2,000,000 | 60% |
| ₱2,000,000 | ₱5,000,000 | 70% |
| ₱5,000,000 | ₱10,000,000 | 75% |
| ₱10,000,000 | and above | 80% |

Full range is 30–80%. Describing this as "70–80%" (as some practitioner guides do) is accurate only for high-value properties.

### Machinery (RA 7160 Section 218(c))

Fixed rates by use class (not bracketed by FMV):

| Machinery Class | Assessment Level |
|---|---|
| Agricultural | 40% |
| Residential | 50% |
| Commercial | 80% |
| Industrial | 80% |

Machinery depreciation allowance: up to 5% per year, minimum assessable value = 20% of original/replacement cost regardless of age.

---

## Tax Rate Caps (RA 7160 Section 233)

| LGU Type | Maximum Basic RPT Rate |
|---|---|
| Provinces | 1% of AV |
| **All cities** (Metro Manila and non-MM) | 2% of AV |
| Municipalities within Metro Manila | 2% of AV |

**CRITICAL NOTE — Confirmed conflict in secondary sources:** Many practitioner guides state that cities outside Metro Manila are capped at 1% like provinces. This is incorrect. Section 233 of RA 7160 explicitly distinguishes only "province" (1%) from "city or municipality within the Metropolitan Manila Area" (2%). All cities — whether in Metro Manila, Cebu, Davao, or anywhere else — are authorized to levy up to 2% basic RPT. Only provinces and non-MM municipalities are capped at 1%.

**SEF Levy (Section 235):** 1% of AV, universal in practice. Statute uses permissive "may" language but no documented case of a Philippine LGU electing not to impose SEF. Proceeds are remitted directly to local school boards.

**Combined effective rates:**
- Province: Basic 1% + SEF 1% = **2% of AV**
- City (anywhere in PH): Basic up to 2% + SEF 1% = **up to 3% of AV**
- Municipality in Metro Manila: Basic up to 2% + SEF 1% = **up to 3% of AV**

---

## Additional Levies

### Idle Land Tax (RA 7160 Section 236)
- Rate: up to **5% of AV** (LGU discretion)
- Maximum combined burden: 2% basic + 1% SEF + 5% idle = **8% of AV** (cities)

**Idle land definition (Section 237):**
- Agricultural land: more than 1 hectare, at least half uncultivated/unimproved
- Non-agricultural land in city/municipality: more than 1,000 sq.m., at least half unutilized/unimproved
- Exceptions: land with ≥50 trees/hectare of permanent crops; grazing lands

### Special Assessment Levies (RA 7160 Section 240)
- For lands benefited by public works projects (e.g., flood control, road widening)
- Specific rate range not confirmed in sources reviewed; exists as an authorized levy

---

## Payment Schedule and Filing

| Period | Payment Deadline |
|---|---|
| Annual (full) | January 31 |
| 1st quarter | March 31 |
| 2nd quarter | June 30 |
| 3rd quarter | September 30 |
| 4th quarter | December 31 |

Discounts of up to 20% are authorized for prompt payment if the LGU grants them by ordinance.

---

## Late Payment Penalty (RA 7160 Section 255)

```
Monthly interest = 2% × unpaid RPT amount (per month or fraction)
Maximum total interest = 36 months × 2% = 72%
```

- Even one day late = 1 full month of interest
- Interest is simple (not compound)
- The 36-month cap is absolute — no further interest accrues beyond that

**Separate surcharge:** Section 168 provides a separate surcharge (up to 25%) for failure to declare real property. This is distinct from the Section 255 delinquency interest and applies to undeclared properties, not standard late payment.

---

## Worked Examples

### Example 1 — Metro Manila Residential Property (City Rate 2%)

**Inputs:**
- Land FMV: ₱3,000,000 (residential land)
- Building FMV: ₱2,000,000 (residential building)
- LGU: Quezon City (city, 2% basic rate)

**Land AL:** Residential land maximum = 20%
- Land AV = ₱3,000,000 × 20% = **₱600,000**

**Building AL:** FMV ₱2,000,000 → bracket ₱1,000,001–₱2,000,000 → 35% (per Section 218(b)(1))
- Building AV = ₱2,000,000 × 35% = **₱700,000**

**Total AV = ₱1,300,000**

- Basic RPT = ₱1,300,000 × 2% = **₱26,000**
- SEF = ₱1,300,000 × 1% = **₱13,000**
- **Annual Total = ₱39,000**

*Note: The practitioner-guides example used 15% AL for the building (yielding ₱300,000 AV and ₱27,000 annual total). This 15% does not appear in the statutory bracket table. The correct statutory AL for a ₱2M residential building is 35%, yielding ₱39,000 total. The practitioner example likely uses a locally enacted rate below the statutory maximum.*

### Example 2 — Provincial Agricultural Property

**Inputs:**
- Land FMV: ₱500,000 (agricultural land)
- LGU: Rural province (1% basic rate)

**Land AL:** Agricultural land maximum = 40%
- Land AV = ₱500,000 × 40% = **₱200,000**

- Basic RPT = ₱200,000 × 1% = **₱2,000**
- SEF = ₱200,000 × 1% = **₱2,000**
- **Annual Total = ₱4,000**

### Example 3 — Commercial Building in Makati City

**Inputs:**
- Land FMV: ₱10,000,000 (commercial land)
- Building FMV: ₱8,000,000 (commercial building)
- LGU: Makati City (city, assume 2% basic rate)

**Land AL:** Commercial land maximum = 50%
- Land AV = ₱10,000,000 × 50% = **₱5,000,000**

**Building AL:** FMV ₱8,000,000 → bracket ₱5,000,001–₱10,000,000 → 75%
- Building AV = ₱8,000,000 × 75% = **₱6,000,000**

**Total AV = ₱11,000,000**

- Basic RPT = ₱11,000,000 × 2% = **₱220,000**
- SEF = ₱11,000,000 × 1% = **₱110,000**
- **Annual Total = ₱330,000**

### Example 4 — Late Payment Penalty

Annual RPT of ₱39,000, unpaid for 7 months:
- Monthly interest = 2% × ₱39,000 = ₱780
- Total interest = 7 × ₱780 = **₱5,460**
- Total due = ₱39,000 + ₱5,460 = **₱44,460**

At 36 months delinquency: interest capped at 72% = ₱28,080 → Total ₱67,080

---

## Edge Cases and Special Rules

### Multi-Use Properties
- Classify by predominant use
- Some LGUs may assess land and building under different classifications if use differs

### Properties with Multiple Classifications
- Government-owned property used for commercial purposes: commercial assessment levels apply
- Mixed-use (e.g., ground floor commercial, upper floors residential): split assessment or classify by predominant use per LGU ordinance

### Condominium Units
- Assessed separately from common areas
- Each unit's FMV is the assessed value per tax declaration
- Common areas owned by condominium corporation are taxed collectively

### Machinery Depreciation
- Applies to machinery only (not land or buildings)
- Minimum assessable value = 20% of original cost regardless of age
- Formula: `assessable_value = max(0.20 × original_cost, original_cost × (1 - 0.05 × years_in_service))`

### RPVARA Transition (RA 12001, June 2024)
- Mandates replacement of LGU Schedule of Fair Market Values with a standardized Schedule of Market Values (SMV) prepared under Philippine Valuation Standards and approved by DOF Secretary
- SMV update cycle: every 2–3 years (versus previous 3–5 years)
- **6% cap on first-year RPT increases** after new SMV takes effect (prevents sudden tax spikes)
- Section 218 of RA 7160 is amended by RA 12001; specific changes to AL tables not yet fully published in accessible sources
- **Tax amnesty:** 2-year window for penalties/surcharges/interest on RPT accrued before RA 12001's effectivity (June 2024)
- Implementing rules and regulations (IRR) issued December 10, 2024
- Transition period: BIR zonal values and LGU FMV schedules currently remain operative pending BLGF-approved SMV adoption

---

## Legal Citations

| Provision | Content |
|---|---|
| RA 7160, Sec. 199(g) | Definition: assessed value = FMV × assessment level |
| RA 7160, Sec. 218(a) | Maximum assessment levels for land by classification |
| RA 7160, Sec. 218(b) | Maximum assessment levels for buildings (bracketed FMV schedule) |
| RA 7160, Sec. 218(c) | Assessment levels for machinery (fixed by use class) |
| RA 7160, Sec. 233 | Basic RPT rate caps: provinces 1%, cities 2%, MM municipalities 2% |
| RA 7160, Sec. 235 | SEF levy: 1% of AV (additional to basic RPT) |
| RA 7160, Sec. 236 | Idle land tax: up to 5% of AV |
| RA 7160, Sec. 237 | Definition of idle land |
| RA 7160, Sec. 240 | Special assessment levy for public works projects |
| RA 7160, Sec. 250 | Payment dates for RPT (annual and quarterly installments) |
| RA 7160, Sec. 255 | Delinquency interest: 2% per month, 36-month cap |
| DOF Local Assessment Regulations No. 1-92 | Implementing rules for assessment levels (complete tables) |
| RA 12001 (RPVARA), June 2024 | Real Property Valuation and Assessment Reform Act — amends Sec. 218, mandates SMV, 6% first-year RPT cap, tax amnesty |
| RA 12001 IRR, December 2024 | Implementing rules for RPVARA |

---

## Verification Status

**Method:** Independent cross-check by subagent against LawPhil (RA 7160 full text), DOF Local Assessment Regulations No. 1-92, Respicio & Co. practitioner commentary, CPBRD Policy Brief 2016-02, SEPO Senate policy brief, and RA 12001.

**Status: CONFIRMED WITH DOCUMENTED CONFLICTS**

| Claim | Status |
|---|---|
| Core formula | CONFIRMED |
| Land assessment levels | CONFIRMED |
| Residential building bracket table (complete 9-tier) | CONFIRMED |
| Agricultural building max AL = 50% (not 80%) | CONFLICT — practitioner-guides.md incorrectly states 50–80% |
| Commercial/industrial building full range 30–80% | CONFIRMED (partial conflict: "70–80%" descriptor inaccurate for lower-value properties) |
| Machinery AL (40–80%) | CONFIRMED |
| Province RPT cap = 1% | CONFIRMED |
| All cities (not just MM) = 2% cap | CONFLICT — many sources incorrectly limit 2% to MM cities only |
| SEF = 1% | CONFIRMED (permissive statutory language noted) |
| Late penalty 2%/month, 36-month cap | CONFIRMED |
| Idle land tax up to 5% | CONFIRMED |
| RPVARA 2024 amendment | CONFIRMED — significant pending change not in practitioner-guides.md |

---

## Automation Complexity Notes

### Branching rules:
- LGU type determination (province / city / MM municipality) → 3 branches for rate cap
- Property class for land → 6 categories
- Property class for building → 4 categories with separate FMV bracket tables
- Building FMV bracket lookup → 6–9 tiers depending on category
- Machinery use class → 4 categories
- Idle land eligibility → 2 branches
- Late payment timing → continuous computation with 36-month cap

### Lookup tables required:
- Land assessment levels by property class (6-row table)
- Residential building FMV brackets (9-tier table)
- Agricultural building FMV brackets (6-tier table)
- Commercial/industrial building FMV brackets (8-tier table)
- Machinery assessment levels by use class (4-row table)
- LGU basic RPT rate by municipality (requires LGU ordinance database — 1,700+ LGUs)
- LGU idle land tax rate (if applicable) by municipality

### External data dependencies:
- LGU tax rate ordinances (requires a database; not centrally published by BLGF)
- Property FMV from LGU assessor's Schedule of Market Values (RPVARA mandates this becomes a national-standard SMV)
- RPVARA transition status per LGU (ongoing through 2026+)

### Deterministic block:
Once inputs (FMV, LGU type, enacted rates, property class) are resolved, RPT computation is **fully deterministic** — no judgment required. The non-deterministic part is acquiring FMV and LGU-enacted rates, which are external data, not computation logic.
