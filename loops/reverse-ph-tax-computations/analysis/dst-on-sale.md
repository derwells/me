# DST on Sale — Documentary Stamp Tax on Conveyance of Real Property

**Wave:** 2 — Computation Extraction
**Date:** 2026-02-25
**Verification status:** CONFIRMED (all core elements; Point 9 reframed for precision)
**Deterministic:** YES — fully deterministic once tax base inputs are resolved

---

## Overview

Documentary Stamp Tax (DST) under NIRC Section 196 is levied on every instrument whereby real property is sold, transferred, or conveyed to another person. Unlike CGT (which distinguishes capital vs. ordinary assets), **DST applies to ALL real property conveyances at the same 1.5% rate** — regardless of whether the property is a capital or ordinary asset of the seller. DST is a transaction tax on the document itself, not on the gain.

**Legal basis:**
- NIRC Section 196 (as amended by RA 10963 / TRAIN Law)
- RA 7660 (1994) — established the ₱15/₱1,000 rate
- RR 4-2018 — TRAIN implementing regulations for DST
- RR 6-2001 — prescribes the 5-day filing deadline
- RMC 67-2024 / RMC 95-2024 — clarified that RR 6-2001's 5-day rule overrides EOPT's 10-day default

---

## Inputs

| Input | Type | Source | Notes |
|---|---|---|---|
| `gross_selling_price` | decimal | Deed of sale | Total consideration stated in instrument |
| `zonal_value_per_sqm` | decimal | BIR RDO zonal schedule | Per Section 6(E); lookup by RDO zone → property type → location |
| `area_sqm` | decimal | Tax Declaration / Title | Land area (and/or building floor area as applicable) |
| `assessed_fmv` | decimal | LGU Tax Declaration | FMV column; from latest Tax Declaration on file |
| `document_date` | date | Notarization date | Triggers month-end deadline; typically the date of notarization |

---

## Core Formula

### Step 1: Determine Tax Base

```
zonal_value = zonal_value_per_sqm × area_sqm
fmv_6e = max(zonal_value, assessed_fmv)               # Section 6(E) FMV
tax_base = max(gross_selling_price, fmv_6e)            # Statutory formulation
         = max(gross_selling_price, zonal_value, assessed_fmv)  # Operationally equivalent
```

This is the same "highest of three" base used for CGT. Example: selling price ₱9M, zonal value ₱10M, assessed FMV ₱1.6M → tax base = ₱10M.

### Step 2: Apply Rate and Round Up

```
# Exact statutory method (ceil to next whole ₱1,000 increment):
dst = ceil(tax_base / 1_000) × 15

# Shortcut (then round up to next multiple of ₱15):
dst_raw = tax_base × 0.015
dst = ceil(dst_raw / 15) × 15
```

DST must always be an exact whole multiple of ₱15. Both formulations are equivalent.

**Worked example:**
```
tax_base = ₱10,000,000
dst = ceil(10,000,000 / 1,000) × ₱15
    = 10,000 × ₱15
    = ₱150,000
```

**Worked example — fractional ₱1,000:**
```
tax_base = ₱10,000,500
ceil(10,000,500 / 1,000) = ceil(10,000.5) = 10,001
dst = 10,001 × ₱15 = ₱150,015
```

### Step 3: Compute Filing Deadline

```
# DST month-end rule (RR 6-2001):
close_of_month = last_day_of_month(document_date)
filing_deadline = close_of_month + 5 calendar days
```

Example: deed notarized March 10 → close of month = March 31 → DST due **April 5**.

**Alternative deadline:** In no case later than the date of registration with the Register of Deeds. This operates as an accelerated outer deadline, not an extension — if the parties attempt to register before the 5-day window closes, DST is due immediately at registration attempt.

**Important:** In practice, DST must be paid before the BIR issues the eCAR, and eCAR is required before Register of Deeds registration. The ROD deadline is therefore largely academic under the current eCAR regime.

---

## Who Files and Pays

**Primary liable party:** Seller (grantor/vendor/transferor) per Section 173 of NIRC and RR 13-2004.

**Nuances:**
- Both parties may be jointly and severally liable if both sign the instrument (Section 173)
- BIR Form 2000-OT instructions state the return "shall be filed by either of the parties"
- In Philippine real estate practice, DST is frequently shifted to the buyer by contractual agreement (buyer-absorbed closing cost arrangements); this contractual shifting is valid under Civil Code Article 1306 but does not release the seller from statutory BIR liability if DST is not remitted
- Filing venue: Authorized Agent Bank (AAB) at the RDO where the property is located; eFPS; or under EOPT reforms, at any RDO

**Form:** BIR Form 2000-OT (Documentary Stamp Tax Declaration/Return — One-Time Transactions)

---

## Special Rules and Edge Cases

### 1. DST Applies to Both Capital and Ordinary Assets

Unlike CGT (capital assets only) and CWT (ordinary assets only), DST under Section 196 applies to **all real property conveyances** regardless of asset classification. A property sale triggers DST whether the seller pays 6% CGT or 1.5%–6% CWT.

**Full tax stack by asset type:**

| Asset Classification | CGT | CWT | VAT | DST |
|---|---|---|---|---|
| Capital asset | 6% | None | None | 1.5% |
| Ordinary asset (VAT-registered) | None | 1.5%–6% | 12% | 1.5% |
| Ordinary asset (non-VAT) | None | 1.5%–6% | 3% Pct Tax | 1.5% |

### 2. Installment Sales — DST Due on Full DOAS Value at Execution

DST accrues on the full contract value stated in the Deed of Absolute Sale (DOAS) at the time of notarization, not on each installment collection.

```
# Installment sale: DOAS executed for ₱5,000,000 payable over 5 years
dst_base = ₱5,000,000    # Full consideration at execution
dst = ceil(5,000,000 / 1,000) × ₱15 = ₱75,000    # Due within 5 days of month-end
```

This is confirmed by BIR Ruling No. OT-028-2024. Contrast with VAT (recognized per collection) and CWT (timing depends on 25% rule) — DST does not follow the installment schedule.

### 3. TRAIN Law Amendments (RR 4-2018)

- **Rate:** Section 196 rate was **NOT changed** by TRAIN. It remains at ₱15/₱1,000 (1.5%), the same rate established by RA 7660 (1994).
- **New scope:** TRAIN (effective January 1, 2018) added **donations of real property** to the Section 196 taxable scope. Previously, gratuitous transfers were not covered by Section 196 DST.
  - Exception: Donations exempt from donor's tax under Section 101(A) and (B) are also DST-exempt.

### 4. EOPT Act (RA 11976) — 5-Day Deadline Preserved

The Ease of Paying Taxes Act (RA 11976, 2024) amended Section 200(B) to establish a default 10-day post-month-end deadline for DST returns. However, RMC 67-2024 (June 2024) and RMC 95-2024 clarified that because the Secretary of Finance had already exercised authority to set a shorter deadline via RR 6-2001, the **5-day rule continues to govern DST on real property transfers**. Practitioners must track this regulatory carve-out — the EOPT 10-day default does NOT apply to Section 196 transactions.

### 5. Exemptions from Section 196 DST

The following conveyances are exempt from Section 196 DST:

| Exemption | Basis |
|---|---|
| Original grants, patents, OCTs issued by the Government (homestead, free, sales patents) | Section 196 itself |
| Socialized housing transactions — NHA and qualifying developers | RA 7279; BIR RR 9-93 |
| Donations exempt from donor's tax under Section 101(A) and (B) | NIRC Section 101 (via TRAIN amendment) |
| Government-to-government deed of assignment (non-sale; confirmation of ownership) | BIR Ruling No. 061-2024 |
| REIT share-for-property exchanges — qualifying conditions | RA 9856 (REIT Act) |

**No exemption for:**
- Principal residence exchanges (CGT exemption does not carry over to DST)
- CARP-awarded lands upon resale by ARB (standard DST applies)
- Sales to government (standard computation; actual consideration is simply one prong of the two-prong "higher of" test)

### 6. Equal-Share Partition — Potential ₱15 Flat Treatment

A partition deed distributing property strictly in proportion to exact legal/co-ownership shares (no consideration, no gain element) may qualify for a nominal ₱15 flat DST on the theory that no sale or transfer of new rights has occurred. This is a practitioner-recognized but litigated position — the BIR may challenge it. Any departure from strict equal-share distribution triggers the full 1.5% rate.

### 7. eCAR Prerequisite Chain

DST payment is mandatory before eCAR issuance. The chain:
1. Pay DST (Form 2000-OT) and CGT/CWT → obtain validated official receipts
2. File ONETT documents at RDO with jurisdiction over property location (per RMC 56-2024)
3. BIR issues eCAR within 7 working days of complete submission (per RMO 12-2025)
4. Present eCAR to Register of Deeds → title transfer processed

Under RR 12-2024, eCARs no longer expire and remain valid indefinitely.

### 8. RPVARA Transition (RA 12001, June 2024)

The Real Property Valuation and Assessment Reform Act is phasing out the separate BIR zonal value and assessor schedule systems in favor of a single DoF-approved Schedule of Market Values (SMV) per Philippine Valuation Standards. During the transition period (through approximately mid-2026), existing zonal values and assessor FMVs remain operative. Once new SMVs are adopted, the tax base computation simplifies to `max(gross_selling_price, unified_SMV)` — the three-value comparison reduces to two values. The 1.5% rate is unaffected.

---

## Worked Examples

### Example A — Standard Residential Sale (Zonal Value Highest)

- Gross selling price: ₱5,000,000
- Zonal value: ₱6,000,000 (500 sqm × ₱12,000/sqm)
- Assessed FMV: ₱4,200,000
- Deed notarized: March 10, 2025

```
fmv_6e = max(6,000,000; 4,200,000) = ₱6,000,000
tax_base = max(5,000,000; 6,000,000) = ₱6,000,000
dst = ceil(6,000,000 / 1,000) × ₱15 = 6,000 × ₱15 = ₱90,000
filing_deadline = April 5, 2025
```

### Example B — Selling Price Highest

- Gross selling price: ₱12,500,000
- Zonal value: ₱10,000,000; Assessed FMV: ₱8,000,000
- Deed notarized: June 25, 2025

```
fmv_6e = max(10,000,000; 8,000,000) = ₱10,000,000
tax_base = max(12,500,000; 10,000,000) = ₱12,500,000
dst = ceil(12,500,000 / 1,000) × ₱15 = 12,500 × ₱15 = ₱187,500
filing_deadline = August 5, 2025
```

### Example C — Installment Sale

- DOAS total selling price: ₱8,000,000 (paid ₱1M down, balance over 7 years)
- Zonal value: ₱7,500,000; Assessed FMV: ₱6,000,000
- DOAS notarized: November 15, 2025

```
tax_base = max(8,000,000; 7,500,000; 6,000,000) = ₱8,000,000
dst = ceil(8,000,000 / 1,000) × ₱15 = ₱120,000    # Full amount due now
filing_deadline = December 5, 2025
# Note: DST is NOT spread across installments; full ₱120,000 due by Dec 5
```

---

## Verification Status

**Primary source:** NIRC Section 196 (as amended by RA 10963); RR 4-2018; RR 6-2001

**Secondary source verification (subagent, 2026-02-25):**

| Element | Status | Sources |
|---|---|---|
| 1.5% rate (₱15/₱1,000) | CONFIRMED | Respicio & Co., Tax & Accounting Center PH, PwC Tax Summaries, Grant Thornton PH |
| Three-value "highest of" tax base | CONFIRMED | All sources; identical to CGT base |
| Ceiling/round-up formula | CONFIRMED | Tax & Accounting Center (explicit mechanics); Respicio & Co. |
| 5-day month-end deadline | CONFIRMED | RR 6-2001; RMC 67-2024; Respicio & Co.; Ocampo & Suralvo |
| EOPT 10-day default overridden | CONFIRMED | PwC Tax Alert 28; Ocampo & Suralvo — 5-day rule preserved |
| ROD registration as alt deadline | CONFIRMED | RR 9-2000 / Form 2000-OT instructions; Respicio & Co. |
| Primary liability: seller | CONFIRMED (with joint-and-several nuance) | Respicio & Co.; Tax & Accounting Center; BIR Ruling 045-2012 |
| Form 2000-OT | CONFIRMED | BIR.gov.ph; all secondary sources |
| TRAIN: rate unchanged, donations added | CONFIRMED | Tax & Accounting Center TRAIN article; RR 4-2018 |
| Pre-TRAIN rate: same 1.5% | CONFIRMED | Tax & Accounting Center; RA 7660 (1994) |
| DST on both capital and ordinary assets | CONFIRMED (explicit) | Ocampo & Suralvo BIR clarification on ordinary assets |
| Installment DST on full DOAS value | CONFIRMED | BIR Ruling No. OT-028-2024 (Ocampo & Suralvo) |
| eCAR prerequisite chain | CONFIRMED | Respicio & Co. eCAR process; RMO 12-2025; RR 12-2024 |
| Original grants exemption | CONFIRMED | Section 196 text; Respicio & Co. |
| Socialized housing exemption | CONFIRMED | RA 7279; BIR RR 9-93; Grant Thornton |
| Donation-of-real-property rule | CONFIRMED | Tax & Accounting Center; Section 101(A)(B) carve-out |
| RPVARA transition | CONFIRMED | Deloitte Philippines; Grant Thornton RPVARA analysis |
| CMEPA — no Section 196 impact | CONFIRMED | Grant Thornton CMEPA alert (July 1, 2025) |

**No conflicts discovered.** Point 9 (government transactions) reframed: there is no special "actual consideration only" rule for government transactions. The standard "higher of consideration or FMV per Section 6(E)" applies, unless a specific statutory exemption covers the specific transaction type.

---

## Automation Assessment Notes (for Wave 4)

**Deterministic subcomputations (fully automatable):**
1. Tax base = max(SP, ZV×area, AFMV) — pure comparison; shared with CGT engine
2. DST = ceil(tax_base / 1,000) × ₱15 — single ceiling arithmetic operation
3. Filing deadline = close_of_month(document_date) + 5 days — date arithmetic

**Key data dependencies (automation blockers):**
- Zonal value lookup: shared blocker with CGT (no BIR API; heterogeneous RDO workbooks)
- Assessed FMV: Tax Declaration document processing (LGU-issued; inconsistent format)
- Exemption determination: whether socialized housing, CARP, donation → requires document classification (partially non-deterministic)

**Branching rules count:**
- Asset type check (capital vs. ordinary): 1 branch (only for co-tax selection; DST itself has no branch)
- Exemption checks (government grant, socialized housing, donation exemption, REIT): ~5 binary checks
- Installment vs. lump-sum: 1 branch (but result is same — full DOAS value both cases)
- Equal-share partition special treatment: 1 branch (litigated; risky to automate)
- Total material branches: ~7

**Complexity estimate:** LOW. The DST formula itself is the simplest of all real property transfer taxes — one comparison, one ceiling multiplication. The complexity lies entirely in (1) zonal value lookup (shared with CGT engine) and (2) exemption classification (partially non-deterministic for socialized housing and CARP edge cases). Once the zonal value database is built for CGT, DST rides on it for free.

**Reuse opportunity:** DST shares 100% of its tax base inputs and lookup dependencies with CGT. A unified "tax base resolver" (Step 1 in both computations) would serve both. The DST computation module is then a trivial add-on — 3 lines of arithmetic.

**Key deadline distinction vs. CGT:**
- CGT: 30-day deadline from notarization date
- DST: 5-day post-month-end deadline from notarization month
- DST deadline arrives first if deed is notarized early in the month; CGT deadline arrives first if deed is notarized near end of month. An automated system should flag which deadline comes first for any given transaction date.
