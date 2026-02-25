# Practitioner Guides — PH Real Estate Tax Computations

**Wave:** 1 — Source Acquisition
**Date:** 2026-02-25
**Sources:** Grant Thornton PH, PwC PH, BDB Law, Respicio & Co., Forvis Mazars PH, ForeclosurePhilippines.com

---

## Overview

This file synthesizes computation-relevant content from Philippine tax practitioner guides and commentaries. Sources are organized by computation topic. Primary legal sources (NIRC, RRs) are already cached from Wave 1; this file captures the practitioner-layer interpretation, worked examples, and edge-case handling that supplements the statutory text.

---

## 1. Capital Gains Tax (CGT) on Capital Asset Sales

**Sources:** P&A Grant Thornton (Oct 2024), Respicio & Co., PwC PH Tax Summaries

### Formula
```
CGT = 6% × max(Gross Selling Price, BIR Zonal Value, Assessed FMV)
```

### Key Rules
- Rate: **6% final tax** (NIRC Sec 24(D), as amended by TRAIN/RA 10963)
- Tax base: highest of (1) actual selling price, (2) BIR zonal value, (3) assessed fair market value
- **No deductions** for acquisition cost, improvements, or outstanding mortgages — the levy applies to presumed gain on the higher valuation
- **Capital asset** = real property NOT used in the ordinary course of trade or business and not held for sale to customers

### Worked Examples
**Example A (Selling Price > Zonal Value):**
- Selling price: ₱5,000,000
- BIR zonal value: ₱4,500,000
- CGT = 6% × ₱5,000,000 = **₱300,000**
- DST = 1.5% × ₱5,000,000 = **₱75,000**

**Example B (Zonal Value > Selling Price):**
- Deed price: ₱3,800,000
- BIR zonal FMV: ₱4,200,000
- CGT = 6% × ₱4,200,000 = **₱252,000**

**Example C (Simple):**
- Selling price: ₱1,000,000
- CGT = 6% × ₱1,000,000 = **₱60,000**

### Deadlines & Filing
- **Form:** BIR Form 1706 (Final Capital Gains Tax Return)
- **Deadline:** Within **30 days** from date of notarization of the Deed of Sale
- **Payment channels:** Authorized Agent Bank (AAB), eFPS, GCash, LANDBANK Link.Biz

### Principal Residence Exemption
- One-time exemption per **10-year period**
- Proceeds must be reinvested in a new principal residence within **18 months**
- If proceeds fully reinvested: 100% exemption
- If partial reinvestment: proportional CGT applies

### Penalties for Late Filing
- 25% surcharge on unpaid tax
- 20% annual interest (or prevailing BSP rate) on deficiency
- Possible compromise penalties

### Asset Classification Note
Capital asset vs. ordinary asset classification is **non-deterministic** (requires judgment per RR 7-2003). Once classification is resolved, CGT computation itself is fully deterministic.

---

## 2. Documentary Stamp Tax (DST) on Real Property Transfers

**Sources:** Grant Thornton PH (DST deadline article), PwC PH, BDB Law

### Formula (Section 196 — Conveyance)
```
DST = 1.5% × max(Gross Selling Price, FMV)
```

### Key Rules
- Rate: **1.5%** of the higher of selling price or FMV (unchanged by TRAIN)
- **Form:** BIR Form 2000-OT
- **Deadline:** Within **5 days after the end of the month** in which the deed was signed
  - e.g., Deed signed Feb 15 → pay DST by March 5
- Either buyer or seller may file (negotiable by contract)
- RMC 67-2024 issued to clarify DST deadline computation

### Mortgage DST (Section 195 — doubled by TRAIN)
- ₱20 on first ₱5,000 secured, or fractional part thereof
- **+₱10 for each additional ₱5,000** (or fractional part)
- Pre-TRAIN: ₱10 on first ₱5,000 + ₱5/₱5,000
- TRAIN doubled the rate (effective Jan 1, 2018)

### Full Transaction Cost Example
For a ₱5,000,000 property:
- CGT: ₱300,000 (seller pays)
- DST: ₱75,000 (buyer pays, often)
- Transfer Tax: ₱25,000 (buyer)
- Registration: ₱8,000 (buyer)
- Notarial: ₱50,000 (split)
- **Total transaction taxes ≈ ₱458,000**

---

## 3. Creditable Withholding Tax (CWT/EWT) on Ordinary Asset Sales

**Sources:** BDB Law, Respicio & Co., Forvis Mazars PH, P&A Grant Thornton

### Formula
```
CWT = Rate × max(Gross Selling Price, FMV)
```

### Rate Table (RR 2-98, as amended by RR 11-2018)
| Seller Status | Selling Price | Rate |
|---|---|---|
| Habitually engaged in RE business | Any | 6% |
| Not habitually engaged; SP > ₱500,000 | >₱500K | 6% |
| Not habitually engaged; SP ₱500,000 or less | ≤₱500K | 1.5% |

*(Rates from RR 2-98 Sec 2.57.2(J) — see bir-revenue-regulations.md for full rate table)*

### Who Withholds
- **Buyer** is constituted as the withholding agent
- Buyer deducts CWT from payment to seller and remits to BIR
- Form: **BIR Form 1606** (Withholding Tax Return on Onerous Transfer of Real Property)
- Payee receives **BIR Form 2307** (Certificate of Creditable Tax Withheld)

### Timing of Withholding — The 25% Rule
- **If initial payments in year of sale exceed 25%** of gross selling price → CWT withheld on **first installment**
- **If initial payments ≤ 25%**:
  - Buyer is engaged in trade/business → CWT withheld **on each installment**
  - Buyer is NOT in trade/business → CWT withheld on **last installment** (or earlier if last installment insufficient to cover tax)
- For individual buyers not engaged in trade/business: **no withholding required** on periodic installment payments; withheld on the last installment

### Important: CWT vs. CGT Never Overlap
- Capital asset → **CGT applies** (no CWT)
- Ordinary asset → **CWT applies** (no CGT)
- CWT is creditable against seller's income tax liability (not final)

---

## 4. VAT on Real Property (Ordinary Assets)

**Sources:** PwC PH, Forvis Mazars PH (RMC 99-2023 alert), Respicio & Co., BIR RMC 99-2023

### Formula
```
Output VAT = 12% × max(Gross Selling Price, FMV)
  where FMV = max(BIR Zonal Value, Assessed FMV)
```

### Who Is Subject to VAT
- **VAT-registered sellers** with annual gross sales exceeding ₱3,000,000 (registration threshold)
- Corporations and developers selling real estate as ordinary assets
- **Exempt:** sellers below the threshold; non-VAT registered persons

### VAT Exemption Threshold
- Sale of residential dwellings priced **≤ ₱3,199,200** (periodically adjusted by DOF/BIR)
  - This is the Section 109(P) NIRC threshold
  - Historically ₱2M; adjusted upward by TRAIN-era guidelines

### The 25% Rule — Installment vs. Deferred Payment (RMC 99-2023)
**Installment Sale** (initial payments in year of sale ≤ 25% of GSP):
- Output VAT recognized **per installment/collection** received
- Input VAT claimable by buyer in same period as seller recognizes output tax
- Only **VAT Official Receipts** issued during installment period
- **VAT Sales Invoice** for full contract price issued only upon full payment and execution of Deed of Absolute Sale

**Deferred Payment / Cash Basis** (initial payments > 25% of GSP):
- Treated as **cash sale**
- Output VAT recognized on **entire selling price in month of sale**
- Subsequent payments: no additional VAT
- Input tax accrues to buyer at time of sale

**"Initial payments" defined:**
= Down payment + all amortization payments (principal only) received during year of sale
(Does NOT include interest; installment interest has separate VAT treatment)

### VAT-Inclusive vs. VAT-Exclusive
- If price is stated VAT-inclusive: Net = GSP ÷ 1.12; VAT = GSP − Net
- If price is stated VAT-exclusive: VAT = GSP × 12%

### Input VAT on Capital Goods
- Capital goods exceeding ₱1,000,000 → input VAT amortized over **useful life or 60 months, whichever is shorter**
- This creates the "72-month amortization rule" cited in practitioner guides (though technically 60-month cap applies)

---

## 5. Real Property Tax (RPT) + SEF

**Sources:** Respicio & Co., Emerhub, ForeclosurePhilippines.com, LegalClarity.org

### Formula
```
Assessed Value (AV) = FMV × Assessment Level (AL)
Basic RPT = AV × Basic Tax Rate
SEF = AV × 1%
Total Annual RPT = Basic RPT + SEF
```

### Assessment Level Table (RA 7160 — per LGU ordinance)
| Property Class | Assessment Level Range |
|---|---|
| Residential land | 0–20% |
| Agricultural land | 0–40% |
| Commercial/Industrial land | 0–50% |
| Mineral land | 0–50% |
| Timberland | 0–20% |
| Residential buildings | 0–60% (stepped by FMV bracket) |
| Agricultural buildings | 50–80% |
| Commercial/Industrial buildings | 70–80% |
| Machinery | 40–80% |

**Building assessment levels (residential) — stepped by FMV:**
- Up to ₱175,000: 0%
- Above ₱10,000,000: 60%
- (Various intermediate tiers between these extremes)

### Tax Rate Caps (RA 7160)
| Location | Maximum RPT Rate |
|---|---|
| Provinces | 1% of AV |
| Cities/Municipalities (non-MM) | 1% of AV |
| Cities/Municipalities in Metro Manila | 2% of AV |

Plus **SEF: 1%** of AV (uniform nationwide, mandatory)

Effective combined minimum rate:
- Non-Metro Manila: **2%** of AV (1% RPT + 1% SEF)
- Metro Manila: **3%** of AV (2% RPT + 1% SEF)

### Additional Levies
- Idle Land Tax: up to **5% of AV** (LGU discretion)
- Special assessment levies for public works: 2–5%
- Maximum possible burden in Metro Manila: **8% of AV** (2% + 1% SEF + 5% idle land)

### Worked Examples

**Example A — Residential, Metro Manila (2% rate):**
- Land FMV: ₱3,000,000 × 20% AL = AV ₱600,000
- Building FMV: ₱2,000,000 × 15% AL = AV ₱300,000
- Total AV: ₱900,000
- Basic RPT (2%): ₱18,000
- SEF (1%): ₱9,000
- **Annual Total: ₱27,000**
- Late penalty (5 months): ₱27,000 × (2% × 5) = ₱2,700 → **Total ₱29,700**

**Example B — Agricultural, Province (1% rate):**
- Land FMV: ₱500,000 × 10% AL = AV ₱50,000
- Basic RPT (1%): ₱500
- SEF (1%): ₱500
- **Annual Total: ₱1,000**

**Example C — Residential, Manila (Respicio worked example):**
- FMV: ₱5,000,000 × 40% AL = AV ₱2,000,000
- Base RPT (2%): ₱40,000
- SEF (1%): ₱20,000
- **Annual Total: ₱60,000**

### RPVARA (RA 12001, June 2024) — Emerging Change
- New law transfers zonal value authority from BIR to local assessors
- Mandates adoption of **Philippine Valuation Standard (PVS)**
- Market value becomes the single valuation base (eliminates multi-source inconsistency)
- **Transition period:** BIR zonal values still in use pending LGU schedule adoption
- Will affect "highest of three" base computation once fully implemented

### Late Payment Penalty
- 2% per month on unpaid RPT + SEF
- Capped at **36 months** (72% total)
- Certificate of Full Payment required before Register of Deeds can transfer title

---

## 6. Local Transfer Tax

**Sources:** Respicio & Co., ForeclosurePhilippines.com, Bamboo Routes

### Formula
```
Transfer Tax = max(Selling Price, Zonal Value, Assessed FMV) × Rate
```

### Rate Caps (RA 7160 Sec 135)
| LGU Type | Maximum Rate |
|---|---|
| Provinces | 0.50% (50% of 1%) |
| Cities and MM municipalities | 0.75% (75% of 1%) |

### LGU-Specific Rates (examples)
| LGU | Rate |
|---|---|
| Quezon City | 0.75% |
| BGC (Taguig) | 0.60% |
| Santa Rosa, Laguna | 0.60% |
| Cebu | 0.50% |
| Manila | 0.75% |
| Provincial (generic) | 0.50% |

### Worked Examples
**Example A — Provincial (0.5%):**
- Selling price: ₱4,000,000; Zonal: ₱3,500,000; Assessed: ₱3,800,000
- Tax base: ₱4,000,000 (highest)
- Transfer Tax = 0.5% × ₱4,000,000 = **₱20,000**

**Example B — Metro Manila City (0.75%):**
- Selling price: ₱10,000,000; Zonal: ₱12,000,000; Assessed: ₱11,000,000
- Tax base: ₱12,000,000 (zonal is highest)
- Transfer Tax = 0.75% × ₱12,000,000 = **₱90,000**

### Deadline
- Typically within **60 days** from execution of Deed of Sale (varies by LGU)
- Who pays: **buyer** (by default; negotiable)
- Must be settled before title transfer at Register of Deeds

---

## 7. EWT on Real Estate-Related Payments (Non-Sale)

**Sources:** Respicio & Co., Forvis Mazars PH

### Broker/Agent Commissions
| Broker Type | Income Level | EWT Rate |
|---|---|---|
| Individual broker | ₱3M or below annually | 5% |
| Individual broker | Above ₱3M OR VAT-registered | 10% |
| Corporate broker | Any | 10% |

**Classification:** Professional fees, talent fees, etc. (not property sale CWT)

### Rental Payments on Commercial Property
- EWT rate: **5%** of gross rental
- Applies to real property used in business where payor has not taken title or has no equity

### Top Withholding Agents (TWAs)
- TWAs withhold **1%** (goods) and **2%** (services) on local purchases not covered by other EWT rates
- Applies to all expenses except: credit card payments, GPP payments, cooperative payments, tax-exempt entities

---

## 8. Installment Sale — Cross-Regime Summary

**Sources:** Grant Thornton PH (RMO 33-2023 alert), BDB Law, Respicio & Co., RMC 99-2023/RMC 11-2024

The 25% threshold triggers different treatment across three separate tax regimes:

| Test | Income Tax | VAT | CWT |
|---|---|---|---|
| **> 25% initial payment** | Recognize full gain in year of sale | Recognize full output VAT in month of sale | Withhold CWT on first installment |
| **≤ 25% initial payment** | Installment method: recognize proportionally | Per-collection recognition | Withhold on last installment (individual buyer, non-business) or per installment (corporate buyer) |

### "Initial Payments" Definition (RMC 99-2023)
= Down payment + all amortization collections (principal only) during year of sale
≠ Total contract price; ≠ includes interest

---

## 9. eCAR (Electronic Certificate Authorizing Registration)

**Sources:** Grant Thornton PH, RMC 56-2024 reference

- Required before title can be transferred at Registry of Deeds
- BIR issues eCAR after verifying CGT/CWT + DST payment
- RMC 56-2024: eCAR jurisdiction clarification (which RDO has authority based on property location)
- All taxes (CGT or CWT, DST, and certifications) must be settled before eCAR is issued

---

## Key Cross-References for Wave 2 Computation Extraction

| Computation | Primary Practitioner Source | Input File |
|---|---|---|
| CGT computation | Grant Thornton "Taxes on Sale" (Oct 2024), Respicio & Co. | analysis/cgt-computation.md |
| DST on sale | Grant Thornton DST deadline article, BDB Law | analysis/dst-on-sale.md |
| DST on mortgage | bir-revenue-regulations.md (RR 4-2018) | analysis/dst-on-mortgage.md |
| CWT rate and timing | BDB Law, Grant Thornton (RMO 33-2023) | analysis/cwt-rate-and-timing.md |
| VAT installment | Forvis Mazars (RMC 99-2023), Respicio & Co. | analysis/installment-vat-schedule.md |
| RPT computation | Respicio & Co., Emerhub | analysis/rpt-computation.md |
| Transfer tax | Respicio & Co., ForeclosurePhilippines | analysis/transfer-tax.md |
| EWT broker rates | Respicio & Co. | analysis/ewt-rate-classification.md |

---

## Gaps and Notes for Wave 2

1. **CWT exact rate table:** Practitioner guides confirm 1.5%/3%/5%/6% brackets but don't uniformly state the ₱500K and ₱2M thresholds. Need cross-check against RR 2-98 full text (already in `input/bir-rr-2-98.md`).

2. **VAT residential threshold:** Cited as ₱3,199,200 in most sources, but this is periodically adjusted. RMC 99-2023 should confirm current figure. Needs Wave 2 verification.

3. **RPVARA transition:** RA 12001 (June 2024) is a major pending change affecting the zonal value lookup computation. BIR zonal values remain operative pending LGU adoption. Flag this as a complexity driver for `zonal-value-lookup`.

4. **DST Deadline Clarification:** RMC 67-2024 provides additional guidance on DST filing deadlines — worth fetching in Wave 2.

5. **eCAR Workflow:** Not a standalone computation but a process gate that serializes tax payments. May be worth a separate frontier aspect if building an end-to-end automation engine.

---

## Sources

- [Grant Thornton PH — Taxes on Sale of Real Property](https://www.grantthornton.com.ph/insights/articles-and-updates1/lets-talk-tax/taxes-on-sale-of-real-property/)
- [Grant Thornton PH — Withholding on Installment Sales](https://www.grantthornton.com.ph/insights/articles-and-updates1/tax-notes/reiteration-of-withholding-taxes-on-installment-sales-of-real-property/)
- [BDB Law — Taxation of Sale of Real Properties](https://bdblaw.com.ph/index.php/newsroom/articles/tax-law-for-business/1061-taxation-of-sale-of-real-properties)
- [Respicio & Co. — CGT Rates and Calculation](https://www.respicio.ph/commentaries/capital-gains-tax-in-the-philippines-rates-and-calculation)
- [Respicio & Co. — EWT Rates for Brokers](https://www.respicio.ph/commentaries/expanded-withholding-tax-in-the-philippines-current-ewt-rates-for-brokers)
- [Respicio & Co. — RPT Rates, Assessment, and Exemptions](https://www.respicio.ph/commentaries/real-property-tax-in-the-philippines-rates-assessment-and-exemptions-explained)
- [Respicio & Co. — Transfer Tax](https://www.respicio.ph/commentaries/calculating-property-transfer-tax-for-deed-of-sale-in-the-philippines)
- [PwC PH — Tax Alert 28 (RMC 99-2023)](https://www.pwc.com/ph/en/tax/tax-publications/tax-alerts/2023/tax-alert-28.html)
- [Forvis Mazars PH — RMC 99-2023 Alert](https://www.forvismazars.com/ph/en/insights/tax-alerts/bir-rmc-99-2023)
- [Forvis Mazars PH — Withholding Taxes Guide](https://www.forvismazars.com/ph/en/insights/tax-alerts/withholding-taxes-in-the-philippines-transactions)
- [ForeclosurePhilippines — Transfer Tax](https://www.foreclosurephilippines.com/what-is-transfer-tax/)
- [PwC PH — Philippines Tax Summaries](https://taxsummaries.pwc.com/philippines)
