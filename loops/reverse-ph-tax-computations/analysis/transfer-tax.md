# Transfer Tax — LGU Tax on Transfer of Real Property Ownership

**Wave:** 2 (Computation Extraction)
**Date:** 2026-02-26
**Verification status:** Confirmed with corrections (cross-checked against 7+ independent sources)
**Deterministic:** YES — fully deterministic once tax base, LGU, and applicable rate are known

---

## Inputs

| Input | Type | Notes |
|---|---|---|
| `selling_price` | Decimal (₱) | Total consideration stated in deed of sale/conveyance |
| `zonal_value_per_sqm` | Decimal (₱) | BIR zonal value per square meter for property location |
| `lot_area_sqm` | Decimal | Lot area in square meters |
| `assessor_fmv` | Decimal (₱) | Fair market value per local assessor's Schedule of Market Values |
| `improvement_fmv` | Decimal (₱) | FMV of improvements (house/building) per assessor, if any |
| `lgu_type` | Enum | Province / City / Municipality-in-MM / Municipality-outside-MM |
| `lgu_enacted_rate` | Decimal (%) | Locally enacted transfer tax rate (must be ≤ statutory cap for LGU type) |
| `transfer_type` | Enum | Sale / Donation / Barter / Exchange / Other |
| `deed_date` | Date | Date of deed execution/notarization (for deadline computation) |
| `is_carp_transfer` | Boolean | Whether the transfer is pursuant to RA 6657 (CARP) |

---

## Core Formula

```
Tax Base = max(total_consideration, fmv)
  where fmv = max(zonal_value × lot_area + improvement_fmv, assessor_fmv + improvement_fmv)

Transfer Tax = Tax Base × lgu_enacted_rate
```

For donations or transfers without substantial monetary consideration:
```
Tax Base = fmv (since consideration is zero or nominal)
```

**Legal basis:** RA 7160 (Local Government Code) Section 135(a).

### Statutory Text vs. Practice — Important Distinction

**Statutory text (Section 135(a)):** The tax base is "the total consideration involved in the acquisition of the property **or** of the fair market value in case the monetary consideration involved in the transfer is not substantial, **whichever is higher**."

This is literally a **two-value comparison** (consideration vs. FMV). Section 135 does NOT cross-reference NIRC Section 6(E) and does not explicitly define "FMV" as the higher of zonal value and assessor's FMV.

**In practice:** LGU treasurers apply the same **"highest of three"** rule used for national taxes (CGT, DST, CWT). This happens because:
1. The CAR (Certificate Authorizing Registration) — which is a prerequisite for paying transfer tax — is issued based on the NIRC's three-way max
2. LGU treasurers use the CAR-stated value as the minimum transfer tax base
3. Practitioner consensus uniformly applies three-way max for transfer tax

**Net effect:** The three-way max is the de facto computation rule, even though Section 135's statutory text is ambiguous on FMV definition.

---

## Rate Structure

### Rate Caps by LGU Type

| LGU Type | Maximum Rate | Legal Basis |
|---|---|---|
| Provinces | **0.50%** (50% of 1%) | Section 135(a) directly |
| ALL cities (Metro Manila and non-MM) | **0.75%** (75% of 1%) | Section 135 base (0.50%) + Section 151 uplift (+50%) |
| Municipalities within Metro Manila | **0.75%** (75% of 1%) | Section 135 base (0.50%) + Section 144 uplift (+50%) |
| Municipalities outside Metro Manila | **0.50%** (50% of 1%) | Section 135(a) directly |

### How the 0.75% Rate Arises (NOT from RA 9640)

The 0.75% rate for cities and MM municipalities is **not** a direct provision of Section 135. It derives from two separate LGC sections:

1. **Section 151 (Scope of Taxing Powers of Cities):** "The rates of taxes that the city may levy may exceed the maximum rates allowed for the province or municipality by not more than fifty percent (50%) **except the rates of professional and amusement taxes.**" Transfer tax is not among the exceptions → cities can levy 0.50% × 1.50 = **0.75%**.

2. **Section 144 (Rates of Tax within the Metropolitan Manila Area):** Municipalities within Metro Manila may levy taxes at rates up to 50% higher than the maximum rates prescribed → 0.50% × 1.50 = **0.75%**.

**Source conflict documented:** Respicio.ph (transfer-tax-rates-in-manila-philippines) incorrectly states that RA 9640 (2009) "amended Section 135 to raise the maximum rate for Metropolitan Manila LGUs from 0.5% to 0.75%." This is **demonstrably false** — RA 9640 only amends Section 140(a) relating to amusement tax. Confirmed against Official Gazette, LawPhil, ChanRobles, and Supreme Court E-Library full text of RA 9640.

### LGU-Enacted Rates (Observed)

| LGU | Rate | LGU Type | Key Ordinance |
|---|---|---|---|
| Manila | 0.75% | City (MM) | Manila Revenue Code (Ord. No. 7795, as amended) |
| Quezon City | 0.75% | City (MM) | QC Revenue Code (Ord. SP-91, S-1993, as amended) |
| Taguig | 0.75% | City (MM) | Taguig Revenue Code |
| Makati | 0.50% | City (MM) | Revised Makati Revenue Code (Ord. No. 2004-A-025) |
| Santa Rosa, Laguna | 0.60% | City (non-MM) | City since 2004 (RA 9264); within 0.75% cap per Section 151 |
| Cebu City | 0.50% | City (non-MM) | Per LGC base rate (has not enacted Section 151 uplift) |
| Davao City | ~0.50% | City (non-MM) | Davao City Revenue Tax Code |

**Key observation:** Many non-MM cities (Cebu, Davao) have not enacted the Section 151 uplift and remain at the 0.50% provincial base rate. The 0.75% cap is permissive, not mandatory.

### Section 191 — Periodic Rate Adjustment

Section 191 of RA 7160 authorizes LGUs to adjust tax rates **not more often than once every 5 years**, with each adjustment not exceeding **10% of the current rate**. This is:
- Discretionary, not mandatory
- Applies to adjustments within an existing rate ordinance
- Must stay within the statutory ceiling (0.50% for provinces/non-MM municipalities; 0.75% for cities/MM municipalities)
- Example: A city at 0.50% could adjust to 0.55% (10% of 0.50%); a city enacting a new tax ordinance could set any rate up to 0.75% under Section 151

---

## Exemptions

### Statutory Exemption (Section 135 only)

Only **ONE** exemption is expressly stated in Section 135:

> "The sale, transfer or other disposition of real property pursuant to R.A. No. 6657 shall be exempt from this tax."

This is the **CARP (Comprehensive Agrarian Reform Program) exemption** — transfers of agricultural land under the agrarian reform program.

### Other Claimed Exemptions — Status

| Claimed Exemption | In Section 135? | Actual Status |
|---|---|---|
| CARP transfers (RA 6657) | **YES** | Statutory exemption in Section 135(a) |
| Government transfers for public use | **NO** | May be covered under RA 7160 Sec. 133 (common limitations on taxing powers); varies by LGU ordinance |
| Corporate mergers without realized gain | **NO** | NIRC Sec. 40(C)(2) applies to CGT/DST only; transfer tax requires separate LGU ordinance exemption |
| Inheritance/extrajudicial settlement | **NO — NOT EXEMPT** | Transfer tax IS payable on estate transfers including via extrajudicial settlement. Multiple sources confirm heirs must pay transfer tax before title transfer. |
| Conjugal property partition | **ARGUABLE** | Not in Section 135; however, partition to surviving spouse may not constitute a "transfer" since spouse already owns their share |

**Critical correction:** The practitioner-guides.md source listed "inheritance via extrajudicial settlement" as exempt from transfer tax. This is **incorrect** — transfer tax applies to all modes of transferring real property ownership, including inheritance. Confirmed by NDV Law and LawyerPhilippines.org.

### LGU-Specific Exemptions (Local Ordinances)

Individual LGUs may enact additional exemptions by local ordinance:
- **Quezon City:** Ordinance No. SP-2378, S-2014 — exempts registered senior citizens (60+, QC residents registered with OCOSCA) from transfer tax on sale of **principal residential property** held for at least 10 years. One-time exemption per 10-year period. Proceeds must be reinvested in new principal residence within 18 months.

---

## Filing and Payment

| Aspect | Rule |
|---|---|
| **Where to pay** | City/Municipal Treasurer's Office where property is located |
| **Deadline** | Within **60 days** from execution of the deed of sale or instrument of transfer |
| **Liable party** | Seller, donor, transferor, executor, or administrator (Section 135(a)) |
| **In practice** | Buyer typically pays by contractual agreement |
| **Prerequisite** | Must be paid before Registry of Deeds will register the deed of transfer |
| **Required documents** | CAR from BIR, realty tax clearance from Treasurer's Office, BIR DST official receipt |
| **Form** | LGU-specific form (no standardized BIR form — each LGU has its own) |

### eCAR Prerequisite Chain

Transfer tax payment sits in a serialized prerequisite chain:
1. Pay CGT or CWT + DST to BIR → obtain eCAR
2. Pay transfer tax to LGU Treasurer's Office (using eCAR as required document)
3. Pay registration fees to Registry of Deeds → title transfer

---

## Late Payment Penalty (RA 7160 Section 168)

```
Surcharge = 25% of unpaid transfer tax (one-time)
Monthly interest = 2% of (unpaid tax + surcharge) per month
Maximum total interest = 36 months × 2% = 72%
```

- Surcharge is assessed immediately upon late payment
- Interest accrues monthly on the combined unpaid tax + surcharge amount
- 36-month cap on interest is absolute

---

## Worked Examples

### Example 1 — Metro Manila City Sale (0.75%)

**Inputs:**
- Selling price: ₱10,000,000
- BIR zonal value: ₱12,000,000 (₱60,000/sqm × 200 sqm)
- Assessor FMV: ₱11,000,000

**Tax base:** max(₱10,000,000, ₱12,000,000, ₱11,000,000) = **₱12,000,000**

**Transfer Tax** = ₱12,000,000 × 0.75% = **₱90,000**

### Example 2 — Provincial Sale (0.50%)

**Inputs:**
- Selling price: ₱4,000,000
- BIR zonal value: ₱3,500,000
- Assessor FMV: ₱3,800,000

**Tax base:** max(₱4,000,000, ₱3,500,000, ₱3,800,000) = **₱4,000,000**

**Transfer Tax** = ₱4,000,000 × 0.50% = **₱20,000**

### Example 3 — Donation in Makati (0.50%)

**Inputs:**
- Consideration: ₱0 (donation)
- BIR zonal value: ₱8,000,000
- Assessor FMV: ₱7,500,000

**Tax base:** ₱8,000,000 (highest FMV; consideration not substantial)

**Transfer Tax** = ₱8,000,000 × 0.50% = **₱40,000**

### Example 4 — Late Payment

Transfer tax of ₱90,000, paid 4 months late:
- Surcharge: 25% × ₱90,000 = ₱22,500
- Monthly interest: 2% × ₱112,500 = ₱2,250/month
- Total interest (4 months): 4 × ₱2,250 = ₱9,000
- **Total due: ₱90,000 + ₱22,500 + ₱9,000 = ₱121,500**

---

## Edge Cases and Special Rules

### Donations
- Transfer tax applies to donations of real property (Section 135(a) explicitly covers "donation")
- Tax base = FMV since monetary consideration is zero
- Donor is the liable party

### Barter/Exchange
- Transfer tax applies to barter or exchange (Section 135(a) covers "barter, or on any other mode of transferring ownership")
- Tax base = higher of the consideration (value of property received in exchange) or FMV of the property transferred

### Foreclosure Sales
- Transfer tax applies when foreclosed property is consolidated in the buyer/bank's name
- Base = highest of judicial/extrajudicial sale price, zonal value, assessor FMV
- Paid by the winning bidder/mortgagee bank

### Installment Sales
- Transfer tax is computed on the **full consideration** at the time of deed execution — not per installment
- Same as DST treatment (full amount at sale, not per collection)

### Condominium Units
- Transfer tax assessed on each unit separately
- Tax base = max(unit sale price, zonal value for condo classification, assessor FMV of the unit)

### Estate Transfers (Inheritance)
- Transfer tax IS payable on estate transfers, including:
  - Extrajudicial settlement (EJS)
  - Judicial settlement
  - Will-based transfers
- Tax base = FMV at the time of transfer/partition
- Liable party = executor or administrator of the estate

### RPVARA Impact (RA 12001, June 2024)
- When RPVARA is fully implemented, the standardized Schedule of Market Values (SMV) will replace both BIR zonal values and LGU assessor FMV schedules
- Transfer tax base will simplify to: max(consideration, SMV value)
- Transition period ongoing through 2026+

---

## Legal Citations

| Provision | Content |
|---|---|
| RA 7160, Sec. 135(a) | Transfer tax authority: provinces up to 0.50% of max(consideration, FMV) |
| RA 7160, Sec. 135(b) | Payment: within 60 days from deed execution; paid at Treasurer's Office |
| RA 7160, Sec. 135(c) | Single statutory exemption: CARP transfers per RA 6657 |
| RA 7160, Sec. 144 | Metro Manila municipalities: rates may exceed standard by up to 50% |
| RA 7160, Sec. 151 | City taxing powers: rates may exceed provincial max by up to 50% (except professional and amusement taxes) |
| RA 7160, Sec. 168 | Late payment: 25% surcharge + 2%/month interest, 36-month cap |
| RA 7160, Sec. 191 | Periodic rate adjustment: up to 10% increase per 5-year cycle |
| RA 6657 | Comprehensive Agrarian Reform Law (basis for CARP exemption) |
| RA 9264 | Santa Rosa, Laguna city charter (2004) — explains 0.60% rate legality |
| QC Ord. SP-2378, S-2014 | Senior citizen transfer tax exemption in Quezon City |
| RA 12001 (RPVARA) | Future impact: unified SMV will simplify tax base determination |

---

## Source Conflicts Documented

| Conflict | Sources | Resolution |
|---|---|---|
| RA 9640 attributed as amending Section 135 | Respicio.ph (transfer-tax-rates-in-manila-philippines) | **INCORRECT.** RA 9640 only amends Section 140 (amusement tax). Confirmed against Official Gazette, LawPhil, ChanRobles. The 0.75% rate derives from Sections 144/151, not RA 9640. |
| Inheritance/EJS claimed as exempt from transfer tax | practitioner-guides.md (ForeclosurePhilippines) | **INCORRECT.** Transfer tax IS payable on estate transfers. Confirmed by NDV Law, LawyerPhilippines.org. |
| Santa Rosa described as "municipality" | ForeclosurePhilippines.com | **INCORRECT.** Santa Rosa has been a city since 2004 (RA 9264). Its 0.60% rate is within the 0.75% Section 151 city cap. |
| Tax base described as "highest of three" in Section 135 | Multiple practitioner sources | **TECHNICALLY IMPRECISE.** Section 135 text provides two-way comparison (consideration vs. FMV); three-way max is a practice convention imported via the CAR prerequisite. |

---

## Verification Status

**Method:** Independent cross-check by subagent against LawPhil (RA 7160 full text), Official Gazette (RA 9640), ChanRobles, Supreme Court E-Library, NDV Law (extrajudicial settlement guide), Respicio & Co. (multiple articles), ForeclosurePhilippines.com, Jur.ph (QC ordinance), GoSupra (Section 135 text), NTRC journal articles.

**Status: CONFIRMED WITH CORRECTIONS**

| Claim | Status |
|---|---|
| Core formula (rate × max of consideration vs FMV) | CONFIRMED |
| Provincial rate cap 0.50% | CONFIRMED |
| City rate cap 0.75% via Section 151 | CONFIRMED |
| MM municipality rate cap 0.75% via Section 144 | CONFIRMED |
| Non-MM municipality rate cap 0.50% | CONFIRMED |
| RA 9640 does NOT amend Section 135 | CONFIRMED (Respicio.ph is wrong) |
| Tax base = three-way max in practice | CONFIRMED (practice); statutory text is two-way |
| CARP is sole statutory exemption in Section 135 | CONFIRMED |
| Inheritance/EJS is NOT exempt | CONFIRMED (practitioner-guides.md was wrong) |
| 60-day deadline | CONFIRMED |
| 25% surcharge + 2%/month + 36-month cap | CONFIRMED |
| QC senior citizen exemption (SP-2378) | CONFIRMED |
| Section 191 periodic 10% adjustment | CONFIRMED |
| LGU rate variation (Manila 0.75%, Makati 0.50%, etc.) | CONFIRMED |

---

## Automation Complexity Notes

### Branching rules:
- LGU type determination (province / city / MM municipality / non-MM municipality) → 4 branches for rate cap
- CARP exemption check → 1 branch
- Transfer type (sale / donation / barter / exchange / estate) → affects base computation (consideration vs. FMV-only)
- Installment sale flag → transfer tax computed on full consideration at deed execution (no per-collection complexity)

### Lookup tables required:
- LGU enacted transfer tax rate by municipality/city (requires LGU ordinance database — same 1,700+ LGU database needed for RPT)
- BIR zonal value (shared dependency with CGT/DST/CWT engines)
- Assessor FMV (shared dependency with RPT engine)

### External data dependencies:
- LGU transfer tax rate ordinances (not centrally published; varies by locality)
- BIR zonal value (no API; shared challenge across all transaction tax computations)
- Assessor FMV / Tax Declaration (document-level input; requires parsing or manual entry)

### Deterministic block:
Once inputs (consideration, FMV values, LGU type, enacted rate) are resolved, transfer tax computation is **fully deterministic** — no judgment required. The formula is simpler than most other real property taxes (single multiplication, no tiered rates or bracket lookups). The primary automation challenge is **LGU rate lookup** — acquiring the locally enacted rate for 1,700+ LGUs.

### Shared infrastructure with other computations:
- Zonal value lookup → shared with CGT, DST, CWT, VAT (zero marginal cost)
- Assessor FMV → shared with RPT computation
- LGU database → shared with RPT computation (rates + LGU type classification)
- Transfer tax engine is LOW incremental effort once the CGT/DST/RPT engines are built
