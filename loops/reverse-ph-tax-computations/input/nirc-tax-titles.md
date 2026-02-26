# NIRC Tax Titles — Computation-Relevant Provisions
## Source: RA 8424 as amended by RA 10963 (TRAIN Law)
## Acquired: 2026-02-25

---

## Title II — Income Tax

### Section 24(D) — Capital Gains Tax on Real Property (Individuals)

**Section 24(D)(1) — In General:**
> "A final tax of **six percent (6%)** based on the **gross selling price or current fair market value as determined in accordance with Section 6(E) of this Code, whichever is higher**, is hereby imposed upon capital gains presumed to have been realized from the sale, exchange, or other disposition of real property located in the Philippines, classified as **capital assets**, including *pacto de retro* sales and other forms of conditional sales, by individuals, including estates and trusts."

- Rate: **6% final tax**
- Base: max(gross selling price, FMV per Section 6(E))
- Section 6(E) FMV = higher of: (a) BIR zonal value, or (b) assessor's schedule of market values
- "Highest of three" in practice = max(selling price, zonal value, assessor FMV)
- Covers: Individuals, estates, trusts
- Form: BIR Form 1706
- Filing deadline: **30 days** following each sale or disposition
- Exception: Sales to government — taxpayer may choose Section 24(A) [ordinary income tax] instead

**Section 24(D)(2) — Principal Residence Exemption:**
- CGT is **exempt** if:
  1. Property sold is the seller's principal residence
  2. Proceeds are **fully utilized** in acquiring/constructing a new principal residence
  3. Reinvestment completed **within 18 calendar months** from date of sale
  4. BIR notified **within 30 days** from date of sale via sworn declaration
  5. Exemption availed **only once every 10 years**
- Partial utilization: proportional exemption applies
- RR 13-99 implements this exemption

**Section 27(D)(5) — CGT on Domestic Corporations:**
> "A final tax of **six percent (6%)** based on the total consideration received or fair market value prevailing at the time of sale, whichever is higher, is hereby imposed upon capital gains presumed to have been realized from the sale, exchange or other disposition of lands and/or buildings which are **not actually used in the business** of a corporation and are treated as capital assets."
- Same 6% rate, same highest-of-three base
- In lieu of normal income tax

---

## Title IV — Value-Added Tax

### Section 106 — VAT on Sale of Goods or Properties

- Rate: **12%** of gross selling price or gross value in money
- "Goods or properties" includes: *real properties held primarily for sale to customers or held for lease in the ordinary course of trade or business*
- Applies to: **ordinary assets** only (not capital assets)
- Base: max(gross selling price, FMV)
- RR 16-2005: FMV for VAT = higher of zonal value and assessed value

### Section 109 — VAT Exemptions (Real Property)

**Key exemptions for real property:**

1. **Non-business real property** — Sale of real property NOT primarily held for sale to customers or held for lease (i.e., capital assets) → NOT subject to VAT; subject to CGT instead

2. **Socialized housing** — Sale of real property utilized for socialized housing as defined by RA 7279 → VAT-exempt

3. **Residential dwelling threshold** — Sale of house and lot and other residential dwellings with selling price **not more than Two million pesos (₱2,000,000)** → VAT-exempt
   - CPI-adjusted every 3 years using PSA Consumer Price Index
   - Current adjusted threshold (last revision): approximately **₱3,199,200** (as of most recent BIR adjustment)
   - Note: Separate residential lot exemption threshold was ₱1,500,000 in original text

4. **Non-VAT registered seller** — Annual gross sales ≤ **₱3,000,000** (post-TRAIN threshold) → not required to register for VAT; subject to percentage tax instead

5. **Lease exemption** — Monthly rental ≤ ₱15,000 for residential units → VAT-exempt

**VAT registration threshold (post-TRAIN):** ₱3,000,000 in annual gross sales/receipts

---

## Title VII — Documentary Stamp Tax

*(Note: PROMPT.md referred to "Title VI (stamp taxes)" — the DST provisions are in Title VII of the NIRC.)*

### Section 195 — Mortgages, Pledges, and Deeds of Trust

DST on instruments whereby property is pledged as security:

| Amount Secured | DST |
|---|---|
| ₱5,000 or less | ₱40.00 flat |
| Each additional ₱5,000 (or fraction) above ₱5,000 | + ₱20.00 |

- For fluctuating accounts / future advances without fixed limit: tax computed on amount actually loaned at execution; additional advances trigger additional DST
- Rate is not a simple percentage — it is a stepped schedule

**Computation formula (effective rate approximation):**
- DST = ₱40 + [ceil((amount - ₱5,000) / ₱5,000) × ₱20] for amounts > ₱5,000

### Section 196 — Deeds of Sale and Conveyances of Real Property

DST on deeds of sale, conveyances, and other instruments transferring real property:

- Rate: **₱15.00 for every ₱1,000** (or fraction thereof) = **1.5%**
- Base: consideration or FMV per Section 6(E), **whichever is higher**
- Government transactions: use actual consideration
- Undervalued consideration: assessors may use assessment roll values
- Round-up rule: if DST is not a multiple of ₱15, round up to next higher multiple of ₱15

**Computation formula:**
- DST = ceil(tax_base / 1,000) × ₱15.00
- Or equivalently: DST = tax_base × 0.015 (rounded up to next multiple of ₱15)

Primary liable party: **Seller** (grantor/vendor/transferor) per RR 13-2004
Form: BIR Form 2000-OT (one-time transactions)

### Section 198 — Assignments and Renewals
- Same DST rate as original instrument applies to each assignment/transfer of mortgage, lease, or policy

### Section 200 — Filing Deadline

DST returns must be filed **within five (5) days after the close of the month** in which the taxable document was made, signed, accepted, or transferred.

- Practical example: Deed notarized March 10 → DST due **April 5** (5 days after March 31)
- In no case later than the date of registration with the Register of Deeds
- Monthly filers (banks, regular issuers): within 10 days after end of month

---

## Section 6(E) — Authority of Commissioner to Prescribe Real Property Values (Zonal Values)

> The Commissioner is hereby authorized to divide the Philippines into different zones or areas and shall, upon consultation with competent appraisers both from the private and public sectors, determine the fair market value of real properties located in each zone or area.

- These values = **BIR Zonal Values**
- Used as minimum tax base for CGT, CWT, DST, VAT
- Updated periodically via Revenue Regulations / Revenue Memorandum Orders
- Published in Official Gazette or newspaper of general circulation; takes effect 15 days after publication
- **RPVARA (RA 12001, signed June 2024):** New law transferring valuation authority away from BIR to a unified market-value-based system under the Department of Finance / local assessors. Transition period ongoing — zonal values still in use as of 2025 pending full implementation.

---

## "Highest of Three" Tax Base Rule

For real property transactions, the tax base is determined by the **highest** of three values:
1. **Gross selling price** (as stated in the deed of sale)
2. **BIR Zonal Value** (per Section 6(E), by RDO zone)
3. **Assessed FMV** (per provincial/city assessor's schedule of market values)

**Which taxes use this base:**
- CGT (Section 24(D)): highest of all three
- CWT on ordinary assets (RR 2-98, Sec. 2.57.2(J)): highest of all three
- DST on conveyance (Section 196): highest of selling price and FMV (where FMV = higher of zonal value and assessed value)
- VAT on ordinary assets (Section 106, RR 16-2005): highest of selling price and FMV
- Transfer Tax (RA 7160, Section 135): highest of consideration and FMV

---

## Section 57 / Revenue Regulations No. 2-98 — Creditable Withholding Tax (CWT)

**Legal basis:** Section 57 of NIRC; implemented by RR 2-98 (as amended by RR 6-2001, RR 17-2003, RR 11-2018)

**Section 2.57.2(J) — CWT on Sale of Real Property Classified as Ordinary Asset:**

Tax base: **higher of** (a) gross selling price / total consideration, or (b) FMV per Section 6(E)

**Rate Table:**

| Seller Category | Selling Price | CWT Rate |
|---|---|---|
| Habitually engaged in real estate | ≤ ₱500,000 | **1.5%** |
| Habitually engaged in real estate | > ₱500,000 to ₱2,000,000 | **3.0%** |
| Habitually engaged in real estate | > ₱2,000,000 | **5.0%** |
| NOT habitually engaged in real estate | Any amount | **6.0%** |
| Exempt under Sec. 2.57.5 | N/A | **0% (exempt)** |

**"Habitually engaged" criteria:**
- Registered with HLURB or HUDCC as real estate dealer/developer; OR
- Consummated at least **6 taxable real estate transactions** in the preceding year; OR
- Registered as habitually engaged with LGU or BIR

**Special rule:** Banks are NOT considered habitually engaged even if they sell many foreclosed properties → always 6%

**Withholding agent:** Buyer (must withhold and remit)
- All juridical persons regardless of business status
- Individual buyers in trade/business (for ordinary assets)
- Individual buyers NOT in trade/business: also required to withhold for real property sales

**Filing:** BIR Form 1606, filed with AAB at RDO where property is located, **within 10 days after end of month** of transaction
**Certificate to seller:** BIR Form 2307

**Important:** CWT applies ONLY to ordinary assets. Capital assets → final 6% CGT (no CWT).

---

## Related Local Government Code Provisions (RA 7160)

### Section 135 — Transfer Tax

- Rate: not more than **50% of 1% = 0.50%** (provinces)
- Rate: not more than **75% of 1% = 0.75%** (cities and municipalities within Metro Manila)
- Base: total consideration or FMV, **whichever is higher**
- Paid to: LGU Treasurer's Office where property is located
- Deadline: **60 days** from signing of deed / execution of instrument
- Payer: Buyer (negotiable, but buyer is typically responsible)

### Sections 232–242 — Real Property Tax (RPT)

**Formula:**
1. Assessed Value (AV) = FMV × Assessment Level
2. Basic RPT = AV × RPT Rate
3. SEF Levy = AV × 1%
4. Total Annual Tax = Basic RPT + SEF

**RPT Rates:**
- Provinces: not exceeding **1%** of AV
- Cities / Municipalities in Metro Manila: not exceeding **2%** of AV

**Special Education Fund (SEF):** Additional **1%** of AV (Section 235 of LGC) — collected alongside RPT

**Assessment Levels** (Section 218 of LGC) — by property class and value bracket:
- Residential land: from ~20% (lower values) to 50% (over ₱10M)
- Commercial/industrial land: 30–50%
- Agricultural land: 15–40%
- Residential buildings: 10% (≤₱175,000) up to 60% (higher values)
- Machinery: generally 80%
- (Exact brackets set by Sangguniang Panlalawigan/Panlungsod ordinances — vary per LGU)

**Idle Land Tax** (Section 236): up to **5%** of AV — additional levy on undeveloped/idle land

**Payment deadlines:** Annually by January 31; quarterly by Jan 31, Mar 31, Jun 30, Sep 30
**Discounts:** Up to 20% for advance full-year payment by January 31
**Penalties:** 2% per month on unpaid amount, maximum 36 months (= 72% total cap)

---

## Key References

- RA 8424 (NIRC of 1997): https://www.officialgazette.gov.ph/1997/12/11/republic-act-no-8424/
- RA 10963 (TRAIN Law): https://www.icnl.org/wp-content/uploads/RA10963.pdf
- RR 2-98 (consolidated as amended through RR 15-2022): https://syciplawresources.com/wp-content/uploads/2023/05/Revenue-Regulations-No.-2-98-as-amended-up-to-RR-15-2022.pdf
- RR 13-99 (principal residence exemption): https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/48006
- RR 7-2003 (ordinary vs capital asset classification): https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/40237
- RPVARA (RA 12001, June 2024): New real property valuation law — transition from zonal values to market-value-based system
- RA 7160 (Local Government Code): RPT provisions Sections 232–242; Transfer Tax Section 135

---

## Computation-Relevant Sections Summary

| Tax | NIRC/LGC Section | Rate | Base | Form | Deadline |
|---|---|---|---|---|---|
| CGT (capital asset, individual) | Section 24(D)(1) | 6% final | max(SP, zonal, assessed FMV) | 1706 | 30 days from sale |
| CGT (capital asset, corporation) | Section 27(D)(5) | 6% final | max(SP, FMV) | 1706 | 30 days from sale |
| CWT (ordinary asset) | Sec. 57 / RR 2-98 Sec. 2.57.2(J) | 1.5–6% creditable | max(SP, FMV per Sec. 6(E)) | 1606 | 10 days after month-end |
| VAT (ordinary asset) | Section 106 | 12% | max(SP, FMV) | 2550Q/M | Monthly/Quarterly |
| DST on conveyance | Section 196 | 1.5% (₱15/₱1,000) | max(consideration, FMV) | 2000-OT | 5 days after month-end |
| DST on mortgage | Section 195 | Stepped (₱40 + ₱20/₱5K) | Amount secured | 2000-OT | 5 days after month-end |
| Transfer Tax | RA 7160 Sec. 135 | 0.5–0.75% | max(consideration, FMV) | LGU form | 60 days from signing |
| RPT basic | RA 7160 Secs. 232–242 | ≤1% or ≤2% | Assessed Value (FMV × level) | LGU form | Jan 31 annually |
| SEF levy | RA 7160 Sec. 235 | 1% | Assessed Value | LGU form | Jan 31 annually |
| CGT exemption | Section 24(D)(2) | 0% | N/A | 1706 + sworn decl. | 30-day notice; 18-month reinvestment |
