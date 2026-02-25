# Rent Control Act — RA 9653 + NHSB Extensions

**Source acquisition for Wave 1 aspect: rent-control-act**
**Date:** 2026-02-25
**Primary legal basis:** Republic Act No. 9653 (2009), HUDCC/NHSB extension resolutions through 2026

---

## 1. Primary Statute: RA 9653

### Section 4 — Limit on Increases in Rent (Verbatim)

> "For a period of one (1) year from its effectivity, no increase shall be imposed upon the rent of any residential unit covered by this Act: **Provided**, That after such period until December 31, 2013, the rent of any residential unit covered by this Act shall not be increased by more than **seven percent (7%) annually** as long as the unit is **occupied by the same lessee**: Provided, further, That when the residential unit becomes vacant, the lessor may set the initial rent for the next lessee: Provided, however, That in the case of boarding houses, dormitories, rooms and bedspaces offered for rent to students, no increase in rental more than once per year shall be allowed."

**Key computation triggers from Section 4:**
1. **Freeze test:** Is the unit in its first year of the current lease? → If yes, increase = 0
2. **Same-lessee test:** Is the current occupant the same lessee as during the preceding period? → If no, cap does not apply (lessor may set any new rate)
3. **Property-type test:** Boarding house/dormitory/bedspace for students → increase allowed once per year maximum
4. **Applicable cap (2010–2013):** 7% of current monthly rent

### Section 5 — Coverage

- **NCR and other highly urbanized cities (HUCs):** monthly rent ₱1.00 to ₱10,000.00
- **All other areas:** monthly rent ₱1.00 to ₱5,000.00
- Coverage assessed as of the effective date of the Act (or current NHSB resolution period)
- "Total monthly rent" excludes utilities and other charges

### Section 6 — HUDCC (now NHSB/DHSUD) Authority

HUDCC/NHSB may:
- Continue regulation beyond the statutory period
- Adjust the allowable limit on rental increases per annum
- Adjust coverage thresholds

**Adjustment factors the board must consider:**
- PSA/NSO census on rental units
- Prevailing rental rates
- Monthly inflation rate on rentals of the immediately preceding year
- Rental price index

### Section 7 — Advance Rent and Deposit

- Rent due: within first 5 days of current month
- Max advance rent: 1 month
- Max deposit: 2 months
- Deposit held in bank account under lessor's name
- Accrued deposit interest returned to lessee at lease expiration
- Deposit forfeiture: allowed for unpaid rent, utilities, or property damage

### Section 11 — Rent-to-Own Exemption

Units subject to a written rent-to-own agreement (resulting in ownership transfer) are **exempt from Section 5 coverage** (the increase cap applies to the new rent but the arrangement itself is not subject to coverage thresholds).

### Penalty (Section 13)

Fine of ₱25,000–₱50,000, or imprisonment of 1 month 1 day to 6 months, or both.

---

## 2. Extension History and Current Caps

### HUDCC Extension Resolutions (2013–2017)

| Period | Resolution | Increase Cap |
|--------|-----------|-------------|
| 2010–2013 | RA 9653 (original) | 7% for all covered units |
| 2014–2015 | HUDCC Res. No. 2, Series of 2013 | 7% (status quo) |
| 2016–2017 | HUDCC Res. No. 1, Series of 2015 | 4% (≤₱3,999/mo); 7% (₱4,000–₱10,000/mo) |
| 2018–2020 | HUDCC Res. No. 1, Series of 2017 | Extended at prevailing rates |

**Basis for 4% (2016–2017):** Average inflation rate in 2014 was 4.1%; HUDCC applied this to protect the lowest-income bracket renters.

### NHSB Extension Resolutions (2021–2026)

After RA 11201 (2019) created DHSUD, NHSB assumed HUDCC's regulatory authority.

| Period | Resolution | Increase Cap | Brackets |
|--------|-----------|-------------|----------|
| 2021 | NHSB Res. No. 2020-04 | 2%/7%/11% tiered | See below |
| 2022 | NHSB Res. No. 2021-02 | 2%/7%/11% tiered | See below |
| 2023 | NHSB Res. No. 2022-01 | 2%/7%/11% tiered | See below |
| 2024 | NHSB Res. No. 2023-03 | 4% uniform | All ≤₱10,000 |
| 2025 | NHSB Res. No. 2024-01 | **2.3% uniform** | All ≤₱10,000 |
| 2026 | NHSB Res. No. 2024-01 | **1% uniform** | All ≤₱10,000 |

**2021–2023 Tiered Structure (NHSB Res. No. 2022-01 — verbatim brackets):**
- ₱1 – ₱4,999/month → max **2%** p.a.
- ₱5,000 – ₱8,999/month → max **7%** p.a.
- ₱9,000 – ₱10,000/month → max **11%** p.a.

**2024 Single Rate (NHSB Res. No. 2023-03):** 4% uniform cap based on NEDA recommendation using upper bound of inflation target.

**2025 Single Rate (NHSB Res. No. 2024-01):** 2.3% uniform cap — significantly reduced from 4%. Covers same-lessee units ≤₱10,000 as of 2024 who continue in 2025.

**2026 Single Rate (NHSB Res. No. 2024-01):** 1% uniform cap — near-sunset rate. Covers same-lessee units ≤₱10,000 as of 2025 who continue in 2026. This is intended as a two-year transition program before a regulation-free market (per Section 16 of RA 9653).

---

## 3. Computation Formula

### Coverage Determination (Inputs → Decision)

```
INPUTS:
  unit_type: residential (apartment/house/room/bedspace/dorm)
  monthly_rent: decimal (₱)
  location_type: "NCR_HUC" | "other"
  lessee_change: boolean (has lessee changed since prior period?)
  current_year: integer

COVERAGE THRESHOLD:
  if location_type == "NCR_HUC": threshold = 10,000
  else: threshold = 5,000

COVERED if:
  unit_type == residential
  AND monthly_rent <= threshold
  AND NOT lessee_change
  AND current_year is in an active regulation period
```

### Allowable Increase Formula

**Step 1: Determine applicable cap % by year and (if tiered) bracket**

For 2025 (uniform): `cap_pct = 0.023`
For 2026 (uniform): `cap_pct = 0.010`

For 2021–2023 (tiered):
```
if monthly_rent < 5000: cap_pct = 0.02
elif monthly_rent < 9000: cap_pct = 0.07
else: cap_pct = 0.11
```

**Step 2: Compute max allowable new rent**
```
max_new_rent = current_monthly_rent × (1 + cap_pct)
max_increase_amount = current_monthly_rent × cap_pct
```

**Example (2025, ₱8,000/month):**
- cap_pct = 0.023
- max_increase = ₱8,000 × 0.023 = ₱184
- max_new_rent = ₱8,184

**Compounding:** Each year's increase is on the immediately preceding rent (not original rent).

**Student boarding/dormitory rule:** If unit is a room/bedspace offered to students, increase allowed max once per year regardless of cap %. Cap % still applies to the amount.

### Advance Rent / Deposit Compliance Check

```
INPUTS:
  advance_rent_demanded: integer (months)
  deposit_demanded: integer (months)

VIOLATIONS:
  advance_rent_demanded > 1 → violation
  deposit_demanded > 2 → violation
```

---

## 4. Edge Cases and Special Rules

### Vacancy Exception
- When a covered unit becomes vacant, the lessor may set **any new initial rent** for the incoming lessee.
- The cap applies only once the new tenancy begins (i.e., next year relative to the new initial rate).
- After vacancy: if new rate is set above ₱10,000/month, unit exits coverage entirely.

### Mixed-Use Units
- Units used for home industries, retail stores, or business purposes are **covered** only if the owner and family actually live there and use it **principally for dwelling**.
- Purely commercial/industrial units: exempt.

### Rent-to-Own
- Written rent-to-own agreements: exempt from coverage thresholds (Section 11).
- Cap computation still applies to the lease payments during the rent-to-own period.

### Hotels, Motels, Tourist Inns
- Explicitly excluded from coverage regardless of nightly/monthly rate.

### Short-Term / Month-to-Month
- Same cap applies; "same lessee" and "occupied" test still governs.
- First 12 months: no increase allowed (interpreted as full 12-month freeze, even on monthly renewals).

---

## 5. Data Dependencies and Update Requirements

- **Cap % is set annually by NHSB resolution** → external data dependency; not embedded in statute.
- Current regulation period: Jan 1, 2025–Dec 31, 2026 (NHSB Res. No. 2024-01).
- After 2026: RA 9653 Section 16 mandates a 2-year transition program before deregulation.
- New bills (S.B. 2278 / H.B. 9805) in 2024 proposed inflation-indexed schedule — not yet law.

---

## 6. Gaps and Uncertainties

- NHSB Res. No. 2024-01 full text inaccessible (403); rate data confirmed through multiple news sources (PNA, Manila Tribune, Inquirer) — treat as verified.
- 2026 rate of 1% confirmed by same sources; appears to be final year of current regulation.
- The ₱5,000 threshold for non-HUC areas has not been updated since 2009; unclear if it was ever adjusted by NHSB resolution (likely not — all news focuses only on ₱10,000 threshold).
- "Highly Urbanized City" classification: current list has ~33 HUCs in PH; LGU classification can change and affects coverage.

---

## 7. Source Citations

- RA 9653 full text: [LawPhil](https://lawphil.net/statutes/repacts/ra2009/ra_9653_2009.html), [The Corpus Juris](https://thecorpusjuris.com/legislative/republic-acts/ra-no-9653.php), [SC E-Library](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/25956)
- NHSB Res. No. 2024-01 (2025–2026): [DHSUD PDF](https://dhsud.gov.ph/wp-content/uploads/Laws_Issuances/07_NHSB/NHSB%20Resolution%202024-01%20(Rent%20Control%202025-2026).pdf) (403 at time of fetch), rates confirmed via:
  - [Philippine News Agency](https://www.pna.gov.ph/articles/1241056)
  - [Manila Tribune, Jan 5 2025](https://tribune.net.ph/2025/01/05/2025-cap-for-p10k-below-rent-hike-set-at-23)
  - [Philippine Daily Inquirer](https://newsinfo.inquirer.net/2021978/govt-cuts-rent-cap-for-units-leased-at-p10000-and-below)
- NHSB Res. No. 2022-01 tiered rates: [Aranas Cruz Law](https://aranaslawph.com/allowable-rent-increases-rates/)
- Extension history: [HUDCC PR, May 2016](https://hudcc.gov.ph/pr010516), [HUDCC Q&A](https://hudcc.gov.ph/QandA)
- PIDS research paper on rent control: [PIDS DPS 1640](https://pidswebs.pids.gov.ph/CDN/PUBLICATIONS/pidsdps1640.pdf)
