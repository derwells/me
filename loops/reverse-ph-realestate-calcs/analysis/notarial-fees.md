# Notarial Fee Computation — Wave 2 Extraction

**Aspect:** notarial-fees (Wave 2)
**Date:** 2026-02-27
**Primary source:** `input/rod-fee-schedules.md` (Part C), web research
**Verification:** Independent subagent cross-checked 8 claims against 25+ secondary sources

---

## Critical Correction from Wave 1

**The Wave 1 source (Part C of `input/rod-fee-schedules.md`) incorrectly cited A.M. No. 19-08-15-SC as a notarial fee amendment effective January 1, 2020.**

A.M. No. 19-08-15-SC is the **2019 Proposed Amendments to the 1989 Revised Rules on Evidence** (effective May 1, 2020). It governs Rules 128-133 on admissibility, burden of proof, presumptions, and testimonial evidence. It contains **zero provisions** about notarial fees, notarization procedures, or fee schedules.

The tiered fee table attributed to this AM number by the Respicio practitioner source (₱300 for ≤₱500K, up to ₱5,000 for ₱9M-₱10M) has **no verified origin** in any Supreme Court issuance. It likely derives from an IBP chapter schedule or is AI-generated content on the Respicio site.

**Severity: HIGH** — affects the regulatory framework analysis and renders the "A.M. No. 19-08-15-SC progressive structure" claim in the Wave 1 source invalid.

---

## Regulatory Stack (Descending Authority)

Philippine notarial fees for real estate documents are governed by **four overlapping regulatory layers**, none of which provides a single deterministic national schedule:

### Layer 1: Rule 141, Section 11 — Statutory Baseline (₱36/act)

**Source:** Rules of Court, as amended by A.M. No. 99-8-01-SC (September 14, 1999), effective March 1, 2000

| Notarial Act | Fee |
|---|---|
| Protests of drafts/bills/notes | ₱36.00 |
| Registration of protest | ₱36.00 |
| Authenticating powers of attorney | ₱36.00 |
| Sworn statements | ₱36.00 |
| Each oath or affirmation | ₱36.00 |
| Certified copy per page | ₱36.00 |
| Depositions per page | ₱36.00 |
| **Acknowledging documents (catch-all)** | **₱36.00** |

**Status:** Still technically in force but effectively superseded by later issuances. No notary charges ₱36 in practice.
**Verification:** CONFIRMED (LawPhil, WIPO Lex, Chan Robles — 3 sources)

### Layer 2: 2004 Rules on Notarial Practice — Fee Delegation

**Source:** A.M. No. 02-8-13-SC, effective August 1, 2004

Rule V, Section 1: "For performing a notarial act, a notary public may charge the maximum fee **as prescribed by the Supreme Court** unless he waives the fee in whole or in part."

**Key provisions:**
- Notary must post a "Schedule of Fees" in a conspicuous place (Rule VI, §1(c))
- No fee beyond those "expressly prescribed and allowed" shall be collected (prohibited fees provision)
- Overcharging = suspension or revocation of notarial commission (Rule XI)

**Important note:** The 2004 Rules text does NOT contain specific peso amounts for acknowledgments. The commonly cited ₱100/₱50 ceilings are widely attributed to this framework but their exact location within the AM text is unclear — they likely come from a companion SC circular.

**Verification:** CORRECTED — Rule VIII cited in Wave 1 governs "Notarial Certificates" (certificate contents), not fees. Fee delegation is in Rule V, §1.

### Layer 3: OCA Circular No. 73-2014 — Current Ceiling

**Source:** Office of the Court Administrator Circular No. 73-2014

| Component | Amount |
|---|---|
| First page of document | ₱200 maximum |
| Each additional page | ₱50 maximum |

**Scope:** Applies to the notarial act itself (acknowledgment, jurat). Does NOT cover professional/drafting fees.

**Verification:** CONFIRMED (2 practitioner sources consistent; primary text not publicly accessible online)

### Layer 4: IBP Chapter Schedules — Local Variation

Executive Judges of Regional Trial Courts approve local fee schedules, typically on recommendation of the local IBP chapter. **Each chapter publishes its own schedule.**

**Known variations:**
- IBP Leyte Chapter: Flat 2% of transaction value, minimum ₱2,000, no cap
- Metro Manila (representative rates from practitioner compilation, not official):
  - DOAS: ≤₱500K → ₱1,000 flat; ₱500K-₱5M → 0.2% (min ₱2K, max ₱10K); ₱5M+ → 0.1% (min ₱10K, max ₱20K)
  - Real Estate Mortgage: ≤₱500K → 0.1% (min ₱1,500); ₱500K-₱5M → 0.15% (max ₱15K); ₱5M+ → 0.1% (max ₱25K)
- Provincial chapters: approximately 10-20% lower than Metro Manila

**Verification:** Confirmed as market data, NOT verified as official IBP publications.

---

## Extracted Computations

### Computation 1: Notarial Act Fee (Per OCA Circular 73-2014)

**Deterministic: YES (trivially)**

**Inputs:**
- `page_count` (integer): number of pages in the document

**Formula:**
```
notarial_act_fee = min(200, page_count > 0 ? 200 : 0) + max(0, (page_count - 1)) × 50
```

**Example:** 5-page DOAS: ₱200 + (4 × ₱50) = **₱400**

**Practical note:** This is the *ceiling* for the notarial act itself. In practice, notaries bundle this into a higher "professional fee" package.

### Computation 2: Notarial Foreclosure Fee (Rule 141, §9(1)(e))

**Deterministic: YES**

**Inputs:**
- `mortgage_amount` (₱): total indebtedness or mortgagee's claim

**Formula:**
```
if mortgage_amount <= 4000:
    fee = mortgage_amount × 0.05
else:
    fee = 200 + (mortgage_amount - 4000) × 0.025

fee = min(fee, 100000)  # Cap per A.M. No. 99-10-05-0
```

**Examples:**
- ₱1,000,000 mortgage: ₱200 + (₱996,000 × 0.025) = ₱200 + ₱24,900 = **₱25,100**
- ₱5,000,000 mortgage: ₱200 + (₱4,996,000 × 0.025) = ₱200 + ₱124,900 → capped at **₱100,000**
- Cap triggers at mortgage_amount = ₱4,000 + (₱100,000 - ₱200) / 0.025 = ₱4,000 + ₱3,992,000 = **₱3,996,000**

**Legal basis:** Rule 141, Section 9(1)(e) (A.M. No. 00-2-01-SC); cap per A.M. No. 99-10-05-0 (Procedure in Extra-Judicial Foreclosure, as amended August 7, 2001)

**Verification:** CONFIRMED (4 sources: WIPO Lex, LawPhil, SC E-Library, ForeclosurePhilippines)

### Computation 3: IBP-Based Notarial Fee Estimation (Metro Manila Model)

**Deterministic: CONDITIONALLY** (deterministic given a specific IBP chapter's rate table)

**Inputs:**
- `transaction_value` (₱): selling price or FMV, whichever is higher
- `document_type` (enum): DOAS, REM, CTS, SPA, EJS

**DOAS (Deed of Absolute Sale) — Metro Manila Representative:**
```
if transaction_value <= 500000:
    fee = 1000
elif transaction_value <= 5000000:
    fee = max(2000, min(10000, transaction_value × 0.002))
else:
    fee = max(10001, min(20000, transaction_value × 0.001))
```

**REM (Real Estate Mortgage) — Metro Manila Representative:**
```
if transaction_value <= 500000:
    fee = max(1500, transaction_value × 0.001)
elif transaction_value <= 5000000:
    fee = min(15000, transaction_value × 0.0015)
else:
    fee = min(25000, transaction_value × 0.001)
```

**Examples (DOAS):**
- ₱500,000 property: **₱1,000** (flat)
- ₱2,000,000 property: ₱2M × 0.002 = **₱4,000**
- ₱5,000,000 property: ₱5M × 0.002 = **₱10,000** (hits cap)
- ₱10,000,000 property: ₱10M × 0.001 = **₱10,001** (hits floor, effectively)
- ₱20,000,000 property: ₱20M × 0.001 = **₱20,000** (hits cap)

**Verification:** Confirmed as representative market data from Respicio compilation. NOT an official IBP publication. Actual rates vary by locality and IBP chapter.

### Computation 4: Market Heuristic Fee Estimate

**Deterministic: NO (estimation only)**

**Inputs:**
- `transaction_value` (₱): property value

**Heuristic:**
```
estimated_fee = transaction_value × rate
where rate ∈ [0.01, 0.02] (1-2% of property value)
```

This is the common market practice figure cited by Metrobank, RE/MAX Philippines, and practitioner guides. It bundles:
- Notarial act fee (₱200-₱400, per OCA Circular)
- Document drafting fee (₱1,000-₱5,000, varies by complexity)
- Professional consultation fee (negotiable)
- Sometimes: liaison/processing assistance

**Verification:** 1-2% range CONFIRMED across 4 sources (Metrobank, RE/MAX PH, BuySellLease, Respicio).

**Important corrections from verification:**
- The Wave 1 estimate of "₱1,000-₱10,000 for most residential transactions" is **too low** for typical Metro Manila residential properties (₱2M-₱10M → 1% = ₱20,000-₱100,000 all-in). The ₱1,000-₱10,000 range applies only to the notarial act component excluding professional fees, or to very low-value properties.

### Computation 5: Unattributed Tiered Table (Circulated as "A.M. 19-08-15-SC")

**Deterministic: YES (if adopted as a model)**
**Regulatory basis: NONE VERIFIED**

| Property Value | Fee |
|---|---|
| ≤₱500,000 | ₱300 |
| ₱500,001 - ₱1,000,000 | ₱500 |
| ₱1,000,001 - ₱2,000,000 | ₱1,000 |
| ₱2,000,001 - ₱3,000,000 | ₱1,500 |
| ₱3,000,001 - ₱4,000,000 | ₱2,000 |
| ₱4,000,001 - ₱5,000,000 | ₱2,500 |
| ₱5,000,001 - ₱6,000,000 | ₱3,000 |
| ₱6,000,001 - ₱7,000,000 | ₱3,500 |
| ₱7,000,001 - ₱8,000,000 | ₱4,000 |
| ₱8,000,001 - ₱9,000,000 | ₱4,500 |
| ₱9,000,001 - ₱10,000,000 | ₱5,000 |
| Each additional ₱1,000,000 (or fraction) above ₱10M | +₱500 |

**Formula (if modeled):**
```
if transaction_value <= 500000:
    fee = 300
elif transaction_value <= 10000000:
    bracket = ceil(transaction_value / 1000000)
    fee = bracket × 500
else:
    fee = 5000 + ceil((transaction_value - 10000000) / 1000000) × 500
```

**Status:** Widely circulated online (Respicio attributes to A.M. No. 19-08-15-SC). Attribution is **definitively incorrect** — A.M. No. 19-08-15-SC is the Rules on Evidence. The table may originate from an IBP chapter schedule or may be AI-generated content. **Should NOT be cited as regulatory authority** but may be useful as a market reference point.

**Verification:** CORRECTED — misattribution confirmed. Table has no verified statutory origin.

---

## Edge Cases and Special Rules

### 1. Seller Pays Convention
By default, the seller pays the notarial fee (they execute the deed). However, this is a negotiable convention, not a legal requirement. Buyer-pays or split arrangements are equally valid.

### 2. Professional Fee vs. Notarial Fee
The notarial act fee (₱200/₱50 ceiling per OCA 73-2014) covers ONLY the notarization itself (stamping, signing, recording). The "professional fee" covering document drafting, legal review, and consultation is separate and unregulated — this is where the 1-2% market rate applies.

### 3. VAT on Notarial Services
If the notary's gross annual income exceeds ₱3,000,000, VAT of 12% applies to the total fee charged. Below the threshold, the notary charges 3% percentage tax instead (or 8% flat rate for mixed-income professionals under TRAIN law).

### 4. Multiple Documents per Transaction
A typical real estate sale involves notarization of:
- Deed of Absolute Sale (primary document)
- Secretary's Certificate (if corporate seller)
- Special Power of Attorney (if representative signs)
- Affidavit of Non-Tenancy
- Affidavit of Relationship (if applicable)

Each is a separate notarial act. Notaries typically quote a package price for the full set.

### 5. Electronic Notarization (2025 Amendment)
Per the March 4, 2025 amendment to A.M. No. 02-8-13-SC (effective June 21, 2025), notaries must submit monthly PDF copies of notarial entries and duplicate originals via email to the Clerk of Court. Notaries may NOT charge any additional fees for this digitization. No fee changes were introduced.

---

## Verification Summary

| Claim | Verdict | Notes |
|---|---|---|
| Rule 141 §11 ₱36/act baseline | CONFIRMED | 3 sources (LawPhil, WIPO, Chan Robles) |
| 2004 RNP ₱100/₱50 ceilings | CORRECTED | Widely cited but NOT in Rule VIII; fee delegation is Rule V §1; exact peso amounts' statutory home unclear |
| OCA Circular 73-2014 ₱200/₱50 ceiling | CONFIRMED | 2 consistent secondary sources; primary text inaccessible |
| A.M. 19-08-15-SC tiered table | **CRITICAL CORRECTION** | A.M. is Rules on Evidence; attribution fabricated; no verified SC origin for tiered table |
| Foreclosure fees 5%/2.5% + ₱100K cap | CONFIRMED | 4 sources (WIPO, LawPhil, SC E-Library, ForeclosurePhilippines) |
| Metro Manila IBP DOAS schedule | CONFIRMED as market data | Not official IBP; Respicio compilation |
| Market rate 1-2% | CONFIRMED | 4 sources (Metrobank, RE/MAX, BuySellLease, Respicio) |
| 2025 amendments (digitization only) | CONFIRMED | 3 sources (SC PIO, eLegal, Aureada Law) |

---

## Determinism Assessment

| Computation | Deterministic? | Reason |
|---|---|---|
| OCA Circular per-page ceiling | YES | Fixed schedule, trivial arithmetic |
| Notarial foreclosure fee | YES | Value-based formula with ₱100K cap, fully specified |
| IBP-based fee (given specific chapter table) | CONDITIONAL | Deterministic once a locality's IBP schedule is provided; but schedule selection is non-deterministic (depends on where notarization occurs) |
| Market heuristic (1-2%) | NO | Range, not a formula; actual fee is negotiated |
| Tiered table (unattributed) | ORPHANED | Mechanically deterministic but no verified regulatory basis |
| Professional/drafting fee | NO | Negotiable between attorney and client |

**Overall assessment:** Notarial fees are **partially deterministic**. Two fully deterministic computations exist (OCA ceiling, foreclosure fees). The IBP-based computation becomes deterministic when parameterized with a specific chapter's rate table. The dominant cost component in practice (professional/drafting fee) is non-deterministic.

---

## Automation Opportunity Assessment

**For the Wave 4 catalog:**

1. **Notarial foreclosure fee** — HIGH automation value. Fully deterministic, value-based, every extrajudicial foreclosure needs it. Formula is simple but the ₱100K cap and the two-tier structure are not widely known.

2. **IBP-based notarial fee estimator** — MEDIUM automation value. Would require maintaining a database of IBP chapter fee schedules (high data acquisition cost but high utility). Could offer "Metro Manila estimate" as default with locality override.

3. **OCA Circular per-page ceiling** — LOW standalone automation value. Trivial computation. Useful only as a component of a comprehensive closing cost calculator.

4. **Market heuristic estimator** — LOW standalone value, but HIGH value as part of a total closing cost calculator. The 1-2% range is useful for rough budgeting.

**Cross-reference:** Notarial fees interact with the ROD registration fee computation (analysis/rod-registration-fees.md) and broker commission computation (pending) as components of total transaction closing costs. The notarial foreclosure fee interacts with Pag-IBIG/bank mortgage default computations (analysis/pagibig-amortization.md, analysis/bank-mortgage-amortization.md).

---

## Legal Citations

| Citation | Description |
|---|---|
| Rule 141, §11 (A.M. No. 00-2-01-SC) | Statutory notarial fee schedule (₱36/act) |
| A.M. No. 02-8-13-SC | 2004 Rules on Notarial Practice |
| OCA Circular No. 73-2014 | Current notarial fee ceiling (₱200/₱50) |
| Rule 141, §9(1)(e) | Notarial foreclosure fee (5%/2.5%) |
| A.M. No. 99-10-05-0 | Extrajudicial foreclosure procedure; ₱100K fee cap |
| A.M. No. 02-8-13-SC (Mar 4, 2025 amendment) | 2025 digitization requirements; no fee changes |
| Civil Code Art. 1358 | Requires public instrument for real property sales >₱5,000 |

**NOT a valid citation for notarial fees:**
- A.M. No. 19-08-15-SC (this is the 2019 Rules on Evidence amendment)
- SC Circular No. 73-2014 (this appears to be the same as OCA Circular 73-2014; sources use both names interchangeably)
