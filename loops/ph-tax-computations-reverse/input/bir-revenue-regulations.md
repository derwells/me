# BIR Revenue Regulations — Computation-Relevant Provisions
## Sources: RR 7-2003, RR 2-98 (as amended through RR 11-2018), RR 16-2005 (as amended), RR 4-2018
## Acquired: 2026-02-25

---

## 1. RR 7-2003 — Capital vs. Ordinary Asset Classification

**Issued:** February 11, 2003
**Purpose:** Implementing guidelines for NIRC Section 39(A)(1) — determines whether CGT or ordinary income tax applies

### 1.1 Legal Definition of Ordinary Assets

Real properties classified as **ordinary assets** (i.e., excluded from capital asset definition):

| Category | Description |
|---|---|
| (a) | Stock in trade / inventory held at close of taxable year |
| (b) | Real property held primarily for sale to customers in ordinary course of business |
| (c) | Real property used in trade/business, subject to depreciation allowance under Sec. 34(F) |
| (d) | Real property used in trade or business of the taxpayer |

All other real properties → **capital assets** → subject to 6% CGT.

### 1.2 Classification Rules by Taxpayer Type

**Taxpayer engaged in real estate business (dealer/developer):**
- ALL real properties acquired → ordinary asset (regardless of current use)
- Includes: properties held for development, lease, or sale; inventory; properties used in the business
- Even idle or abandoned properties remain ordinary assets

**Taxpayer NOT engaged in real estate business:**
- Properties used or previously used in the business → ordinary asset
- Properties **not used in business for more than 2 years** prior to the transaction → converted to **capital asset**
  - The 2-year period is measured back from the date of the taxable transaction
  - Taxpayer bears burden of proving non-use (e.g., Barangay Chairman certification)
- Properties never used in business → capital asset from the start

**Change of business (from real estate to non-real estate):**
- Does NOT reclassify previously ordinary assets → remain ordinary assets

**Banks (foreclosure properties):**
- All real properties acquired via foreclosure → ordinary assets
- BUT: banks are NOT considered "habitually engaged" in real estate for CWT rate purposes
  - → CWT rate on bank-sold properties = **6%** (the "not habitually engaged" rate)
  - Despite selling many foreclosed properties, banks do not qualify for the 1.5%/3%/5% tiered rates

**Inherited or donated properties:**
- Heir/donee NOT in real estate business → treated as **capital asset**
- Heir/donee IS in real estate business (e.g., inherited by a developer) → ordinary asset
- Property received in tax-free exchange by a real estate business or business-user → ordinary asset

### 1.3 Evidentiary Support

To rebut ordinary asset presumption, taxpayer may submit:
- Certification from Barangay Chairman or head of administration that property is not used in trade/business
- Relevant business records showing the property has been idle for 2+ years

### 1.4 Implication for Tax Computation

This classification is the **gateway decision** for all downstream computations:

| Classification | Applicable Taxes |
|---|---|
| Capital asset | 6% final CGT (Form 1706); no VAT; no CWT |
| Ordinary asset | CWT 1.5–6% (Form 1606) + VAT 12% (if VAT-registered) + income tax on net gain |

> **Note for Wave 2:** This classification step is NON-DETERMINISTIC in many cases (requires judgment about primary purpose, business engagement, use periods). Document as a prerequisite condition, not as a standalone computation.

---

## 2. RR 2-98 as Amended — Creditable Withholding Tax (EWT) Details

**Original issue:** April 17, 1998
**Key amending regulations:** RR 6-2001, RR 17-2003, RR 11-2018 (TRAIN implementation)

### 2.1 Section 2.57.2(J) — CWT on Sale of Real Property (Ordinary Assets)

**Withholding agent:** Buyer (withholding agent) is required to withhold; buyer is responsible for remittance.

Who must withhold:
- All juridical persons (corporations, partnerships, associations) — always required to withhold
- Individual buyers engaged in trade/business — required to withhold
- Individual buyers NOT in trade/business — also required to withhold on real property purchases

**Tax base:** Higher of:
- (a) Gross selling price / total amount of consideration stated in the deed
- (b) Fair market value per Section 6(E) = higher of (i) BIR zonal value, (ii) assessor's schedule of market values

### 2.2 CWT Rate Schedule (Post-TRAIN via RR 11-2018)

| Seller Classification | Selling Price / Consideration | CWT Rate |
|---|---|---|
| Habitually engaged in real estate | ≤ ₱500,000 | **1.5%** |
| Habitually engaged in real estate | > ₱500,000 to ₱2,000,000 | **3.0%** |
| Habitually engaged in real estate | > ₱2,000,000 | **5.0%** |
| NOT habitually engaged | Any amount | **6.0%** |
| Exempt (Sec. 2.57.5) | N/A | **0%** |

**"Habitually engaged" criteria** (ANY one of):
1. Registered with HLURB or HUDCC as real estate dealer/developer; OR
2. Consummated at least **6 taxable real estate transactions** in the preceding year

**Special rule — Banks:** Even if selling many foreclosed properties, banks are NOT "habitually engaged" → always applies **6% rate**.

### 2.3 Installment Sale Withholding — The 25% Rule

The timing of withholding on installment sales depends on the **initial payment as a percentage of the total selling price**:

**Scenario A — Initial payments exceed 25% of total selling price:**
- Full CWT is withheld and remitted on or before the **first installment**

**Scenario B — Initial payments do NOT exceed 25% of total selling price:**
- If **buyer is engaged in trade/business**: withhold on **each installment payment** as made
- If **buyer is NOT engaged in trade/business**: withhold upon the **last installment**

> "Initial payments" defined as: all payments received in the year of sale (including down payment and installments in the year of sale), excluding the purchase price of a mortgaged property assumed by the buyer.

This rule mirrors the income recognition rule for installment sales — the 25% threshold determines whether the gain is reportable in the year of sale (>25%) or spread over the collection period (≤25%).

### 2.4 Filing and Remittance

| Item | Details |
|---|---|
| Form | BIR Form 1606 (Withholding Tax Remittance Return for Onerous Transfer of Real Property Other Than Capital Asset) |
| Filing venue | Authorized Agent Bank (AAB) at RDO where property is located |
| Deadline | **Within 10 days after the end of the month** of transaction (e.g., transaction in March → file by April 10) |
| Certificate issued | BIR Form 2307 (Certificate of Creditable Taxes Withheld) — issued to seller as proof |

### 2.5 EWT on Professional Fees — Real Estate Service Practitioners (RESP)

Under RR 11-2018 (TRAIN implementation), fees paid to real estate professionals are subject to EWT:

| Payee | EWT Rate |
|---|---|
| Real estate broker, consultant, appraiser — individual | **5%** |
| Real estate broker, consultant, appraiser — corporation | **5%** |
| Notes: these are professional fee EWT, not property sale CWT | — |

This is distinct from the property sale CWT — it applies to brokerage commissions and appraisal fees, not the property consideration.

---

## 3. RR 16-2005 as Amended — VAT Implementing Regulations

**Issued:** September 1, 2005
**Supersedes:** RR 14-2005
**Purpose:** Implementing Title IV (VAT) of NIRC as amended by RA 9337
**TRAIN amendments:** Various sections amended by RR 13-2018 and subsequent issuances

### 3.1 Section 4.106-4 — VAT Base for Real Property Sales

> "In the case of sale of real property subject to VAT, the gross selling price shall mean the consideration stated in the sales document or the fair market value, **whichever is higher**."

**Fair market value for VAT purposes** = higher of:
- BIR zonal value per Section 6(E)
- Assessor's schedule of market values (assessed value)

This mirrors the CGT and CWT base — the "highest of three" rule.

### 3.2 When Is Real Property Sale Subject to VAT?

| Condition | VAT Treatment |
|---|---|
| Property is ordinary asset of VAT-registered seller | Subject to 12% VAT |
| Property is capital asset | NOT subject to VAT (CGT instead) |
| Property is ordinary asset but seller is non-VAT registered (annual gross sales ≤ ₱3M) | NOT subject to VAT; subject to 3% percentage tax |
| Socialized housing (RA 7279) | VAT-exempt (Sec. 109(P)) |
| Residential dwelling: house & lot ≤ ₱2,000,000 (or adjusted threshold) | VAT-exempt (Sec. 109) |

### 3.3 VAT Exemption Thresholds — Residential Property

Under the TRAIN Law (RA 10963, effective Jan 1, 2018):
- Residential house and lot / other residential dwellings: VAT-exempt if **selling price does not exceed ₱2,000,000**
- This threshold is **CPI-adjusted every 3 years** using the PSA Consumer Price Index
- Most recent BIR administrative adjustment (as of 2024): threshold approximately **₱3,199,200**
- Separate residential lot exemption: approximately **₱1,500,000** (original TRAIN text)

> **Key issue for Wave 2:** The adjustable threshold creates a lookup dependency — the exact threshold in effect at the date of sale must be determined from BIR issuances.

### 3.4 VAT on Installment Sales of Real Property

For installment sales, VAT recognition follows the collection schedule:
- VAT is recognized and remitted **upon each collection** (proportional to amount received)
- Full output VAT is NOT due all at once on signing of deed
- Governed by RMC 99-2023 (detailed treatment in `installment-vat-schedule` aspect)

### 3.5 VAT on Lease of Real Property

Separate from sale:
- Commercial lease: 12% VAT on gross rental receipts if landlord is VAT-registered
- Residential lease: VAT-exempt if monthly rental per unit does not exceed **₱15,000**
- Above ₱15,000/month: 12% VAT

---

## 4. RR 4-2018 — TRAIN Law DST Amendments

**Issued:** December 19, 2018; effective February 2, 2018 (15 days after publication in Manila Bulletin, January 18, 2018)
**Purpose:** Implementing RA 10963 (TRAIN) DST rate changes

### 4.1 DST Rate Changes Under TRAIN

TRAIN Law increased most DST rates by **100%** (doubling). Key exceptions:

| NIRC Section | Instrument | Pre-TRAIN Rate | Post-TRAIN Rate | Changed? |
|---|---|---|---|---|
| Section 195 | Mortgages, pledges, deeds of trust | ₱20 per ₱5,000 | ₱40 per ₱5,000 | **Doubled** |
| Section 195 | First ₱5,000 bracket | ₱20 flat | ₱40 flat | **Doubled** |
| Section 196 | Sale/conveyance of real property | ₱15 per ₱1,000 (1.5%) | ₱15 per ₱1,000 (1.5%) | **UNCHANGED** |
| Section 196 | Donations of real property | Not covered | ₱15 per ₱1,000 (1.5%) | **New coverage** |
| Section 197 | Charters | — | Increased | Yes |

> **Critical finding:** Section 196 (the main DST on real property transfers) was NOT changed by TRAIN. The rate was already at ₱15 per ₱1,000 (1.5%) before TRAIN, and remains unchanged.

> **What TRAIN DID change for Section 196:** Added donations of real property to the taxable scope — previously, gratuitous transfers of real property were not covered by Section 196 DST.

### 4.2 DST on Mortgages — Updated Formula (Post-TRAIN)

Section 195, post-TRAIN:

| Amount Secured | DST |
|---|---|
| ₱5,000 or less | **₱40.00** flat |
| Each additional ₱5,000 (or fraction) above ₱5,000 | **+ ₱40.00** |

**Computation formula (post-TRAIN):**
```
DST_195 = ₱40 + ceil((amount - ₱5,000) / ₱5,000) × ₱40    [for amounts > ₱5,000]
DST_195 = ₱40                                                [for amounts ≤ ₱5,000]
```

**Effective rate approximation:** ~0.8% for amounts in the ₱1M–₱10M range (decreasing step function, not linear)

---

## 5. RR 11-2018 — TRAIN Income Tax and EWT Implementation

**Issued:** January 31, 2018
**Purpose:** Implementing TRAIN changes to income tax rates and withholding provisions

### 5.1 Key Changes Relevant to Real Property

1. **CWT rates on real property (Sec. 2.57.2(J)):** Rates retained at 1.5%/3%/5%/6%; income classification thresholds and "habitually engaged" definition clarified
2. **Professional fee EWT for RESP:** Real estate service practitioners (brokers, appraisers, consultants) subject to 5% EWT on professional fees
3. **EWT on rental income:** Separate EWT on rent paid to individual lessor; 5% on gross rental

### 5.2 Section References in RR 2-98 as Amended by RR 11-2018

| Provision | Section | Subject |
|---|---|---|
| CWT on real property sale (ordinary asset) | 2.57.2(J) | Rates 1.5%–6%; tax base; installment timing |
| CWT on professional fees (RESP) | 2.57.2(A) | 5% on broker/appraiser/consultant fees |
| EWT on rent | 2.57.2(C) | 5% if payee is individual; different rate for corp |
| Final withholding on non-residents | 2.57.1 | Different regime |
| Withholding agent obligations | 2.58 | Who must withhold, deadlines |
| Filing and remittance | 2.58.1 | Form 1606, 10-day deadline |

---

## 6. Cross-Reference: Which Regulations Govern Which Computations

| Computation | Primary Legal Basis | Key RR/RMC |
|---|---|---|
| Capital vs. ordinary asset classification | NIRC Sec. 39(A)(1) | RR 7-2003 |
| CGT on capital asset | NIRC Sec. 24(D), 27(D)(5) | [No specific RR — direct statutory] |
| CGT principal residence exemption | NIRC Sec. 24(D)(2) | RR 13-99 |
| CWT on ordinary asset sale | NIRC Sec. 57 | RR 2-98 Sec. 2.57.2(J), as amended by RR 11-2018 |
| Installment CWT timing (25% rule) | NIRC Sec. 49 (installment method) | RR 2-98; also see RMC 99-2023 for VAT parallel |
| VAT on ordinary asset sale | NIRC Sec. 106 | RR 16-2005 Sec. 4.106-4 |
| VAT exemption thresholds | NIRC Sec. 109 | RR 16-2005 as amended; BIR administrative adjustments |
| VAT on installment sales | NIRC Sec. 106 | RMC 99-2023 |
| DST on conveyance | NIRC Sec. 196 | RR 4-2018 |
| DST on mortgage | NIRC Sec. 195 | RR 4-2018 (doubled rate) |
| EWT on RESP professional fees | NIRC Sec. 57 | RR 2-98 Sec. 2.57.2(A), as amended by RR 11-2018 |
| Transfer Tax | RA 7160 Sec. 135 | Local ordinances |
| RPT + SEF | RA 7160 Secs. 232–242 | Local assessment ordinances |

---

## 7. Key Computationally-Relevant Details for Wave 2

### 7.1 The "25% Rule" — Two Separate Applications

The 25% threshold appears in **two distinct computation contexts**:

1. **CWT timing (RR 2-98 Sec. 2.57.2(J)):**
   - If initial payments > 25% of SP → withhold full CWT on first installment
   - If ≤25% → withhold per installment or at last installment

2. **Income tax installment method (NIRC Sec. 49):**
   - If initial payments > 25% → gain reportable in full in year of sale
   - If ≤25% → gain spread proportionally over collection period (installment method)

These two 25% rules use the same threshold but trigger different consequences in different computations.

### 7.2 "Habitually Engaged" as a Binary Input

For CWT rate selection, the computation branches on a binary:
- Input: `habitually_engaged` = True/False
- If True: use 1.5%/3%/5% tiered rate based on price
- If False: use flat 6%

The determination of `habitually_engaged` requires checking:
- HLURB/HUDCC registration (lookup/documentation check), OR
- Transaction count in prior year (>= 6 transactions)

This determination is the non-deterministic gate before the deterministic CWT computation.

### 7.3 Section 6(E) FMV — The Zonal Value Lookup

The "higher of" base for all real property taxes requires:
1. Gross selling price (from deed)
2. BIR Zonal Value (lookup by: RDO zone → street/area → property type)
3. Assessor's Schedule of Market Values (from LGU assessor's office)

The computation `max(SP, zonal_value, assessor_FMV)` is deterministic once the lookup values are resolved, but the lookup itself (especially zonal value) is a data dependency that requires external lookup tables.

---

## Key Sources

- RR 7-2003 full text: https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/40237 ; https://8box.solutions/rr-no-7-2003/
- RR 2-98 consolidated (through RR 15-2022): https://syciplawresources.com/wp-content/uploads/2023/05/Revenue-Regulations-No.-2-98-as-amended-up-to-RR-15-2022.pdf
- RR 11-2018 (TRAIN EWT implementation): https://juan.tax/wp-content/uploads/2018/03/RR-No.-11-2018.pdf
- RR 16-2005 (VAT implementing rules): https://bir-cdn.bir.gov.ph/BIR/pdf/26116rr16-2005.pdf
- RR 4-2018 (TRAIN DST implementing rules): https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/89753
- NTRC Tax Research Journal Vol. XXXII.6 (2020) on DST rates: https://www.ntrc.gov.ph/images/journal/2020/j20201112a.pdf
- BDB Law — Taxation of Sale of Real Properties: https://bdblaw.com.ph/index.php/newsroom/articles/tax-law-for-business/1061-taxation-of-sale-of-real-properties
- Respicio & Co. — Capital Gains Tax and VAT on residential property: https://www.lawyer-philippines.com/articles/capital-gains-tax-and-vat-on-residential-property-sale-philippines
- ForeclosurePhilippines — CWT in real estate: https://www.foreclosurephilippines.com/creditable-withholding-tax-in-real/
