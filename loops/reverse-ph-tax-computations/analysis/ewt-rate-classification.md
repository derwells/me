# EWT Rate Classification — Real Estate Subset of RR 2-98

## Verification Status: CONFIRMED (one conflict resolved; documented below)
## Deterministic: YES (once payee classification and gross income level are resolved as preconditions)
## Date: 2026-02-25

---

## Overview

Expanded Withholding Tax (EWT) applies to specific payments made within and around real estate transactions — distinct from CWT on property sales (covered in `cwt-rate-and-timing`). This analysis covers the real estate-adjacent EWT categories: professional fees to real estate service practitioners, rental income, brokerage commissions, and contractor payments.

**Legal basis:**
- NIRC Section 57 (withholding authority)
- RR 2-98 as amended by RR 6-2001, RR 17-2003, RR 11-2018, RR 14-2018, RR 14-2021, RR 15-2022, RR 16-2023
- RMC 11-2024 (PFRS 16 / right-of-use asset — EWT base clarification)
- RR 31-2020 (Top Withholding Agent revision)

**Scope (this aspect):** EWT on payments TO service providers in the real estate ecosystem:
- Real estate service practitioners (RESP) — brokers, appraisers, consultants
- Lessors of commercial/residential real property
- Construction and service contractors
- Note: CWT on ordinary asset property sales (1.5%/3%/5%/6% via Form 1606) is analyzed separately.

---

## Category A: Professional Fees to Real Estate Service Practitioners (RESP)

### Inputs

| Input | Type | Source |
|---|---|---|
| `payee_is_individual` | Boolean | PRC license / business registration |
| `payee_has_prc_license` | Boolean | PRC registry check |
| `payee_gross_income_current_year` | ₱ amount | Payee's sworn declaration |
| `payee_is_vat_registered` | Boolean | BIR VAT registration status |
| `payee_has_single_payor` | Boolean | Payee declaration (Annex B-2) |
| `payee_total_income_if_single_payor` | ₱ amount | Payee declaration |
| `sworn_declaration_submitted` | Boolean | Annex B-1 (individual), B-3 (corporate) |

### Formula / Decision Tree

**Legal basis:** RR 2-98 Section 2.57.2(A) as amended by RR 11-2018 (effective March 2018 onwards).

```
def ewt_rate_resp_professional_fees(payee):

    # Branch A: Individual (natural person) with PRC license
    if payee.is_individual and payee.has_prc_license:

        # Sub-branch: single-income payor exemption
        if payee.has_single_payor and payee.total_income < 250_000:
            return 0%  # exempt (Annex B-2 submitted)

        # VAT registration overrides income threshold
        if payee.is_vat_registered:
            return 10%

        # Income-based bifurcation
        if payee.gross_income_current_year <= 3_000_000 and payee.sworn_declaration_submitted:
            return 5%   # Annex B-1 submitted
        else:
            return 10%  # > ₱3M, OR no declaration submitted

    # Branch B: Non-individual (corporation, partnership, association)
    elif not payee.is_individual:
        if payee.gross_income_current_year <= 720_000 and payee.sworn_declaration_submitted:
            return 10%  # Annex B-3 submitted
        else:
            return 15%  # > ₱720K OR no declaration submitted

    # Branch C: Individual WITHOUT PRC license (unlicensed practitioner)
    elif payee.is_individual and not payee.has_prc_license:
        return 10%  # flat, no income threshold, classified under Sec. 2.57.2(G)
```

### Rate Summary Table — RESP Professional Fees

| Payee Type | Condition | Rate |
|---|---|---|
| Individual, PRC-licensed | Single payor, total income < ₱250K, Annex B-2 | **0% (exempt)** |
| Individual, PRC-licensed | Gross income ≤ ₱3M, Annex B-1 submitted | **5%** |
| Individual, PRC-licensed | Gross income > ₱3M OR VAT-registered | **10%** |
| Individual, PRC-licensed | No sworn declaration submitted | **10%** |
| Non-individual (corp/firm) | Gross income ≤ ₱720K, Annex B-3 submitted | **10%** |
| Non-individual (corp/firm) | Gross income > ₱720K OR no declaration | **15%** |
| Individual, unlicensed | Any amount | **10% flat** |

### TRAIN Law Change History

| Period | Individual RESP Rate | Threshold |
|---|---|---|
| Pre-January 2018 | 10% (≤ ₱720K) / 15% (> ₱720K) | ₱720,000 |
| Jan–Mar 2018 (RMC 1-2018 transitional) | **8% flat** | None |
| March 2018 onwards (RR 11-2018) | **5% (≤ ₱3M) / 10% (> ₱3M)** | ₱3,000,000 |

**Non-individual (corporate) RESP rates were NOT changed by TRAIN** — 10%/15% with ₱720K threshold remains.

### Sworn Declaration Filing Mechanics

| Annex | Who Files | When | Entitlement |
|---|---|---|---|
| B-1 | Individual with multiple payors | January 15 each year OR before first payment | 5% rate (instead of 10%) |
| B-2 | Individual with only ONE payor | January 15 OR before first payment | 0% exemption (up to ₱250K) |
| B-3 | Non-individual / corporation | January 15 OR before first payment | 10% rate (instead of 15%) |

---

## Category B: EWT on Rental Income from Real Property

### Inputs

| Input | Type | Source |
|---|---|---|
| `gross_rental_paid_or_accrued` | ₱ amount | Lease contract / payment voucher |
| `lessee_is_in_trade_or_business` | Boolean | Business registration / nature of lessee |
| `lessee_is_juridical_entity` | Boolean | SEC registration / legal status |

### Formula

**Legal basis:** RR 2-98 Section 2.57.2(B) as amended; RMC 11-2024.

```
EWT_rental = gross_rental × 5%
```

**No distinction between individual lessor and corporate lessor** — the 5% rate applies uniformly regardless of whether the property owner is a natural person or a juridical entity.

**No distinction between commercial and residential lease** for the EWT rate itself — the 5% applies to both. The VAT exemption for residential leases ≤ ₱15,000/month is a separate (VAT) provision that does not alter EWT obligations.

**PFRS 16 clarification (RMC 11-2024):** For lessees applying PFRS 16 (right-of-use asset accounting), EWT base is the **actual rental paid or accrued only** — not the depreciation component of the ROU asset, nor the implied interest component. Accounting treatment under PFRS 16 does not change the EWT base.

### Rate Table — Rental

| Lessor Type | Condition | EWT Rate |
|---|---|---|
| Individual | Any | **5%** |
| Corporate / juridical | Any | **5%** |

Note: Rate is UNCHANGED before and after TRAIN.

### Withholding Agent Obligation (Critical Condition)

EWT on rental is only withheld when the **lessee** is a withholding agent. See Category E (Who Must Withhold) below. Private individuals NOT in trade/business are not withholding agents for EWT purposes — a purely personal residential lease (individual person renting an apartment) produces no EWT withholding obligation, even though the lessor's rental income may still be taxable income.

---

## Category C: EWT on Commissions (Brokerage, Referral Fees)

### Classification

Under RR 11-2018 (effective March 2018), **commissions paid to independent sales representatives and marketing agents** are expressly treated under the **same rates and rules as professional fees (Section 2.57.2(A))**.

This was a structural change — pre-TRAIN, commissions payable to brokers/agents had a separate treatment under the "brokers and agents" subsection.

### Rate Table — Commissions

| Payee Type | Condition | Rate |
|---|---|---|
| Licensed RESP individual | Gross income ≤ ₱3M, Annex B-1 | **5%** |
| Licensed RESP individual | Gross income > ₱3M, or VAT-registered, or no declaration | **10%** |
| Corporate brokerage firm | Gross income ≤ ₱720K, Annex B-3 | **10%** |
| Corporate brokerage firm | Gross income > ₱720K, or no declaration | **15%** |
| Unlicensed individual agent | Any | **10% flat** (Sec. 2.57.2(G)) |

### Employment vs. Independent Contractor Distinction

**Independent real estate agent** (commission-based, no employment contract, renders services to multiple principals) → EWT treatment (rates above).

**Employed sales agent** (regular employee, fixed salary + commission, employment contract) → Withholding on compensation (graduated income tax rates, BIR Form 1601-C), NOT EWT. The employer files substituted filing or regular compensation returns.

Classification as independent vs. employed is a judgment call (economic reality test) that falls outside deterministic computation.

### Referral Fees to Non-Licensed Non-RESP Individuals

Referral fees paid to persons who are neither PRC-licensed RESP nor accredited agents: potentially classifiable under Section 2.57.2(G) (other brokers) at **10% flat**, or if payments are for general services, the payor's TWA obligations may apply at **2%**. The classification is ambiguous in practice; the conservative approach is 10%.

---

## Category D: EWT on Payments to Contractors

### Inputs

| Input | Type | Source |
|---|---|---|
| `gross_payment_to_contractor` | ₱ amount | Contract / payment voucher |
| `contractor_type` | Enum | Contract description |

### Formula

**Legal basis:** RR 2-98 Section 2.57.2(E) as amended; UNCHANGED by TRAIN/RR 11-2018.

```
EWT_contractor = gross_payment × 2%
```

**All contractor types — uniform 2% rate:**

| Contractor Category | Rate |
|---|---|
| General engineering contractor | **2%** |
| General building contractor | **2%** |
| Specialty contractor | **2%** |
| Subcontractor | **2%** |
| Other contractors (demolition, janitorial, security, etc.) | **2%** |

### No ₱150,000 Threshold

**There is no ₱150,000 minimum threshold** for triggering the 2% EWT obligation on contractor payments. The ₱150,000 figure appears only as a worked-example payment amount in practitioner guides — it is not a regulatory trigger. The 2% applies on all gross payments to contractors.

The only threshold-like mechanism is the **payee-level lone-income-payor exemption** (Annex B-2): if the contractor's total income for the year is < ₱250,000 and they have only one payor, they can file Annex B-2 to obtain EWT exemption. This is a payee election, not a payor-level threshold.

### Labor-Only Contracting Note

"Labor-only contracting" is prohibited under DOLE rules (Labor Code). If a contractor is reclassified as a labor-only contractor, the principal is deemed the direct employer, shifting the tax obligation from EWT (2%) to withholding on compensation (graduated rates). For tax purposes, the payment is withheld at 2% until a DOLE/NLRC reclassification occurs — the risk is downstream, not at the time of payment.

---

## Category E: Who Must Withhold EWT (Withholding Agent Obligations)

**Legal basis:** RR 2-98 Section 2.57.3 as amended; RR 31-2020 (TWA threshold revision).

### Decision Tree — Withholding Agent Obligation

```
def must_withhold_ewt(payor):

    # Always required — juridical entities
    if payor.is_juridical_entity:  # corp, partnership, association
        return True

    # Always required — government entities
    if payor.is_government_entity:  # national govt, LGU, GOCC
        return True

    # Individuals — only if in trade or business
    if payor.is_individual:
        return payor.is_in_trade_or_business

    # Default
    return False
```

### Special Carve-Out for Real Property Sales (Contextual Note)

For CWT on ordinary asset real property sales (Form 1606), **individual buyers NOT in trade/business ARE constituted as withholding agents** — this is a specific exception to the general rule above, carved out by RR 2-98 Sec. 2.57.2(J). This exception applies to the real property sale CWT only; it does NOT extend to professional fees, rental, or contractor EWT.

### Top Withholding Agents (TWA) — Expanded Scope

Businesses classified as TWA (gross sales/receipts or gross purchases ≥ ₱12M for Groups A/B RDOs; ≥ ₱5M for Groups C–E) must additionally withhold **1% on purchases of goods** and **2% on purchases of services** from any regular supplier — even where no specific EWT category applies. This is a catch-all over and above the specific EWT categories in this analysis.

---

## Filing and Remittance

**Note:** These forms are for EWT on professional fees, rent, and contractor payments — NOT for CWT on property sales (Form 1606).

| Item | Detail |
|---|---|
| Monthly advance remittance | BIR Form 0619-E — 10th day after month-end (manual) / 15th day (eFPS) |
| Quarterly EWT return | BIR Form 1601-EQ — last day of month following close of quarter |
| Form 2307 to payee | Within 20 days after end of each quarter |
| Annual information return | BIR Form 1604-E (Alphalist of payees) — January 31 of following year |

**Note:** For EWT (professional fees, rent, contractors), Form 2307 IS still issued to the payee. This is different from the CWT on property sales (Form 1606) where Form 2307 was discontinued by RMC 31-2025.

---

## Edge Cases

| Scenario | Treatment |
|---|---|
| VAT-registered individual RESP, gross income ≤ ₱3M | 10% (VAT registration overrides income test — treated as high-income) |
| Individual RESP with single payor, total income < ₱250K (Annex B-2) | 0% exempt |
| Corporate RESP who forgot to submit Annex B-3 | 15% (no declaration = higher bracket rate) |
| GPP (General Professional Partnership) distributing to partners | Partners' shares treated at individual rates, but with **₱720K threshold** (not ₱3M) |
| Commission to individual agent employed by developer | Withholding on compensation (not EWT) if employment relationship exists |
| Rent paid to individual lessor by individual private lessee (not in business) | No EWT withholding obligation (lessee is not a withholding agent) |
| Rent paid to corporate lessor by any corporate lessee | 5% EWT applies |
| Construction contractor with lone-income payor + income < ₱250K (Annex B-2) | 0% exempt on payments to that contractor |
| PFRS 16 ROU asset — depreciation and interest components | Not subject to EWT; only actual rental payments are EWT base (RMC 11-2024) |
| Ease of Paying Taxes Act (RA 11976, effective 2024) | Deductibility of EWT-subject expenses is now allowed even if EWT not withheld; but withholding obligation and penalties remain unchanged |

---

## Worked Example

### Example 1: Individual Licensed Broker Commission

```
Payor: Ayala Land (corporation, withholding agent: YES)
Payee: Juan dela Cruz, PRC-licensed real estate broker (individual)
Commission amount: ₱500,000
Annex B-1 submitted: YES (gross income estimate ≤ ₱3M)
VAT-registered: NO

Decision tree:
  → Individual + PRC-licensed → Branch A
  → Not single-payor exemption scenario (multiple payors)
  → Not VAT-registered
  → Gross income ≤ ₱3M AND Annex B-1 submitted
  → Rate = 5%

EWT = ₱500,000 × 5% = ₱25,000
Net payment to broker = ₱500,000 - ₱25,000 = ₱475,000
Form 2307 issued to broker for ₱25,000
```

### Example 2: Corporate Property Management Firm (Rent Collection)

```
Payor: XYZ Corporation (corporate lessee, withholding agent: YES)
Payee: ABC Realty Corp (corporate lessor)
Monthly rent: ₱200,000
Annual rent paid in quarter: ₱600,000

EWT rate = 5% (flat, corporate lessor — no distinction)
EWT per month = ₱200,000 × 5% = ₱10,000
EWT per quarter = ₱600,000 × 5% = ₱30,000

Filed via Form 0619-E monthly; summarized in Form 1601-EQ quarterly
Form 2307 for ₱30,000 issued to ABC Realty Corp within 20 days after quarter end
```

### Example 3: Construction Contractor Payment

```
Payor: Megaworld Corporation (corporate, withholding agent: YES)
Payee: BuildRight Construction Co. (general contractor, corporate)
Progress billing payment: ₱10,000,000

EWT rate = 2% (contractor, corporate, no sworn declaration available)
EWT = ₱10,000,000 × 2% = ₱200,000
Net payment = ₱9,800,000
Form 0619-E filed within 10 days after month-end
Form 2307 issued to BuildRight quarterly
```

---

## Legal Citations

| Provision | Citation |
|---|---|
| General EWT authority | NIRC Section 57 |
| Professional fees EWT rates (post-TRAIN) | RR 2-98 Sec. 2.57.2(A) as amended by RR 11-2018 |
| Transitional rates (Jan–Mar 2018) | RMC 1-2018 |
| Rental income EWT | RR 2-98 Sec. 2.57.2(B) as amended |
| EWT on ROU assets (PFRS 16) | RMC 11-2024 |
| Contractor payments EWT | RR 2-98 Sec. 2.57.2(E) |
| Commissions aligned to professional fees | RR 11-2018 (amending Sec. 2.57.2) |
| Unlicensed broker/agent rate | RR 2-98 Sec. 2.57.2(G) |
| Withholding agent obligations | RR 2-98 Sec. 2.57.3 |
| Sworn declaration mechanics | RR 11-2018 Annexes B-1, B-2, B-3 |
| TWA thresholds | RR 31-2020 |
| Ease of Paying Taxes Act (deductibility change) | RA 11976 Sec. 34(K) repeal |

---

## Conflict Documented

| Issue | Source A (incorrect) | Source B (correct) | Resolution |
|---|---|---|---|
| Corporate RESP EWT rate | Respicio.ph EWT for brokers: "Corporations — flat 10% regardless of amount" | Tax and Accounting Center, CloudCFO, Conventus Law TRAIN Series Part 4: "10% if gross ≤ ₱720K; 15% if > ₱720K" | **Use Source B (bifurcated 10%/15%).** Respicio.ph article omits the 15% tier. The 10%/15% corporate structure is unchanged from pre-TRAIN and confirmed by multiple authoritative sources. |
| RR 2-98 section number for rental EWT | Pre-RR-11-2018 numbering: "Sec. 2.57.2(A)(8)" | Post-RR-11-2018 numbering: "Sec. 2.57.2(B)" | Same provision; numbering shifted when RR 11-2018 consolidated the EWT list from 29 items to 21 items. Use Sec. 2.57.2(B) for citations under the current RR. |

---

## Verification Summary

**Verified against:** Tax and Accounting Center (professional fees TRAIN guide, RESP guide, 21 EWT items), Respicio & Co. (commercial lease guide, broker EWT rates — rates confirmed, 15% omission flagged), Roque Law (TRAIN professional fees/commissions guide), Conventus Law TRAIN Series Part 4, CloudCFO (EWT guide), RMC 11-2024 (PFRS 16 EWT base), BIR RR 11-2018 official digest.

**Confirmed:** 5%/10% individual RESP rates, 10%/15% corporate RESP rates, 5% flat rental EWT (no lessor-type distinction), 2% flat contractor EWT (no contractor-type distinction), commissions now aligned to professional fee rates (post-TRAIN), sworn declaration mechanics (Annex B-1/B-2/B-3), withholding agent obligation limited to juridical entities + individuals in trade/business.

**Conflicts found:** Corporate RESP rate (Respicio.ph 10% flat vs. 10%/15% bifurcated — bifurcated is correct). Documented above.

**Non-deterministic gate:** Whether the payee is an employee or independent contractor is a judgment call (economic reality test) — not captured in this deterministic EWT tree. The tree assumes the payment is already classified as independent contractor compensation.
