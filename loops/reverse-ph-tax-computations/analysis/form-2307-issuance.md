# Form 2307 Issuance Logic — Certificate of Creditable Tax Withheld at Source

## Verification Status: CONFIRMED (2 corrections applied; 10 additions from verification)
## Deterministic: YES (once ATC code, rate, and gross payment are known)
## Date: 2026-02-26

---

## Overview

BIR Form 2307 is the Certificate of Creditable Tax Withheld at Source. It is the primary document enabling payees (income recipients) to claim withheld EWT as a tax credit against income tax. The issuance, computation, and reconciliation of Form 2307 constitutes a deterministic multi-party workflow with three computational components:

1. **Amount computation** — per ATC rate applied to gross income payment
2. **Issuance timing** — deadline-driven by quarter-end
3. **Reconciliation** — bilateral cross-matching between withholding agent filings and payee credit claims

**Legal basis:**
- NIRC Section 57 (withholding authority), Section 58(B) (certificate issuance obligation)
- RR 2-98 as amended by RR 11-2018 (EWT rates, ATC codes, withholding agent obligations)
- RR 2-2006 (SAWT requirement for payee-side reconciliation)
- RMC 31-2025 (Form 2307 discontinued for real property CWT — Form 1606 replaces it)
- RMC 14-2025 (digital copies acceptable for credit claims)
- RA 11976 / EOPT Act (Section 34(K) repeal; simplified withholding timing)

**Scope:** This analysis covers EWT Form 2307 issuance only. CWT on ordinary asset real property sales is now handled via Form 1606 (see `cwt-rate-and-timing.md`).

---

## Inputs

| Input | Type | Source |
|---|---|---|
| `payor_is_withholding_agent` | Boolean | See withholding agent decision tree below |
| `payee_tin` | String (NNN-NNN-NNN-NNNNN) | BIR COR (Form 2303) |
| `payee_name` | String | Registration documents |
| `payee_address` | String | BIR COR |
| `payor_tin` | String | BIR COR |
| `payor_name` | String | Registration documents |
| `atc_code` | Enum | Nature of income payment → ATC lookup |
| `gross_income_payment` | ₱ amount per month | Payment voucher / invoice |
| `ewt_rate` | Percentage | ATC rate table (see `ewt-rate-classification.md`) |
| `quarter` | Enum (Q1/Q2/Q3/Q4) | Calendar quarter |
| `month_within_quarter` | 1, 2, or 3 | Month position within quarter |

---

## Formula / Decision Tree

### Step 1: Determine Withholding Agent Obligation

```
def is_withholding_agent(payor):
    if payor.is_juridical_entity:         # corporation, partnership, association
        return True
    if payor.is_government_entity:        # NGA, LGU, GOCC
        return True
    if payor.is_individual:
        return payor.is_in_trade_or_business
    return False
```

**Special carve-out (NOT applicable to Form 2307 EWT):** For CWT on real property sales (Form 1606), even individual buyers NOT in trade/business must withhold. This exception applies only to property sale CWT, not to EWT on professional fees, rent, or contractor payments.

**Top Withholding Agents (TWA):** Businesses with gross sales/receipts or gross purchases ≥ ₱12M (Groups A/B RDOs) or ≥ ₱5M (Groups C–E RDOs) must additionally withhold 1% on goods purchases and 2% on services purchases from any regular supplier — even where no specific EWT category applies.

### Step 2: Determine ATC Code and Rate

Select the applicable ATC code based on nature of payment and payee classification. See `ewt-rate-classification.md` for the full decision tree. Summary of real estate-adjacent ATCs:

| ATC | Description | Rate |
|---|---|---|
| WI010/WI011 | Professional fees — individual (≤₱3M / >₱3M) | 5% / 10% |
| WC010/WC011 | Professional fees — corporate (≤₱720K / >₱720K) | 10% / 15% |
| WI040/WI041 | Broker commissions — individual (≤₱3M / >₱3M) | 10% / 15% |
| WC040/WC041 | Broker commissions — corporate (≤₱720K / >₱720K) | 10% / 15% |
| WI100/WC100 | Real property rentals — individual / corporate | 5% / 5% |
| WI120/WC120 | Contractor payments — individual / corporate | 2% / 2% |
| WI158/WC158 | TWA → goods supplier — individual / corporate | 1% / 1% |
| WI160/WC160 | TWA → services supplier — individual / corporate | 2% / 2% |

### Step 3: Compute Tax Withheld Per Month

```
tax_withheld_month = gross_income_payment_month × ewt_rate
```

### Step 4: Populate Form 2307 — Quarterly Certificate

Form 2307 is structured as a quarterly document with monthly columns:

```
For each (atc_code, payee) combination in the quarter:
    month_1_amount = gross_income_payment[month_1]
    month_1_tax    = month_1_amount × ewt_rate
    month_2_amount = gross_income_payment[month_2]
    month_2_tax    = month_2_amount × ewt_rate
    month_3_amount = gross_income_payment[month_3]
    month_3_tax    = month_3_amount × ewt_rate

    total_amount   = month_1_amount + month_2_amount + month_3_amount
    total_tax      = month_1_tax + month_2_tax + month_3_tax
```

Multiple ATC codes per payee → multiple line items on the same Form 2307.

### Step 5: Determine Issuance Deadline

```
def issuance_deadline(quarter):
    # EWT certificates: 20 days after quarter close (NIRC Section 58(B))
    deadlines = {
        'Q1': 'April 20',
        'Q2': 'July 20',
        'Q3': 'October 20',
        'Q4': 'January 20 (following year)'
    }
    return deadlines[quarter]

# Upon-request provision: payee may request Form 2307 at any time;
# withholding agent must furnish simultaneously with income payment if requested.
```

### Step 6: Issue Copies

Three (3) copies per regulatory standard:
1. **Original** — for the payee (for tax credit claims on ITR)
2. **Duplicate** — for the BIR (filed with payee's tax return)
3. **Triplicate** — retained by the withholding agent

Per RMC 14-2025: digital/electronic copies are now acceptable for credit/refund claims; original hard copies no longer required if verifiable against SAWT.

---

## Reconciliation Logic — The Bilateral Cross-Matching System

### Withholding Agent Side (Payor)

```
Monthly:   0619-E         → remit EWT for months 1 and 2 of each quarter
Quarterly: 1601-EQ        → consolidated quarterly EWT return (all 3 months)
           + QAP (DAT)    → Quarterly Alphalist of Payees emailed to esubmission@bir.gov.ph
           + Form 2307    → issued to each payee within 20 days after quarter-end
Annual:    1604-E          → Annual Information Return of Creditable Income Taxes Withheld
           + Alphalist (DAT) → Annual Alphalist of Payees (Schedules 3 and 4)
```

**Reconciliation requirement:**
```
Sum of all Form 2307 issued in quarter
  = Total EWT on Form 1601-EQ (Item 19)
  = Sum of monthly 0619-E remittances (Items 20+21) + month 3 payment (Item 22)

Sum of all Form 2307 issued in year
  = Total EWT on Form 1604-E
  = Sum of four quarterly 1601-EQ totals
```

### Payee Side (Income Recipient)

```
Quarterly: Receive Form 2307 from each withholding agent
           → Record as "Income Tax Pre-payments" (asset account)
           → Prepare SAWT (Summary Alphalist of Withholding Taxes) per RR 2-2006
           → Attach SAWT to quarterly ITR (1701Q or 1702Q)
           → Claim total withheld as tax credit on ITR

Annual:    Consolidate all Form 2307 received during the year
           → Prepare annual SAWT
           → Claim total on annual ITR (1701 or 1702-RT/EX/MX)
           → Attach original Form 2307 copies (or digital copies per RMC 14-2025)
           → Upload scanned 2307s to eAFS within 15 days of e-filing ITR
```

**Tax credit claiming formula:**
```
income_tax_due = computed_tax_from_ITR
total_credits  = sum(all Form 2307 received in period)

if total_credits <= income_tax_due:
    tax_payable = income_tax_due - total_credits
elif total_credits > income_tax_due:
    excess = total_credits - income_tax_due
    # Options: carry forward to next year OR apply for refund/TCC
```

### BIR Cross-Matching Validation

The BIR performs automated TIN-matching between:
- **Withholding agent's QAP / 1604-E Alphalist** (amounts withheld and reported)
- **Payee's SAWT / ITR** (amounts claimed as credits)

```
BIR_validation:
    for each (payee_tin, atc_code, period):
        agent_reported = QAP[payee_tin][atc_code][period]
        payee_claimed  = SAWT[payee_tin][atc_code][period]

        if agent_reported != payee_claimed:
            trigger_audit_notice()
            # Consequences: disallowance of credit, surcharges, interest
```

Mismatches trigger: BIR Letter of Authority for audit, potential disallowance of tax credits, surcharges (25%) and interest (12% p.a.) on under-remittance.

---

## Form 1606 Carve-Out — Real Property CWT (NOT Form 2307)

**Effective RMC 99-2023, formalized by RMC 31-2025 (April 2025):**

Form 2307 is **NO LONGER issued** for CWT on ordinary asset real property sales. The workflow is:

```
OLD (pre-RMC 99-2023):
  Buyer withholds CWT → files Form 1606 → issues Form 2307 to seller
  Seller claims Form 2307 on ITR

NEW (post-RMC 31-2025):
  Buyer withholds CWT → files Form 1606 (one per transaction)
  Seller receives Form 1606 copy with proof of payment
  Seller claims Form 1606 on ITR (under "Other Tax Credits/Payments")
  Form 2307 NOT issued for this purpose
```

**ITR presentation per RMC 31-2025:**
- EWT credits (from Form 2307) → "Creditable Tax Withheld for the Year" line on ITR
- CWT credits (from Form 1606) → "Other Tax Credits/Payments" line on ITR
- These are separate ITR line items, not combined

**One transaction per Form 1606:** RMC 31-2025 explicitly prohibits combining multiple real estate sales into a single Form 1606.

---

## Edge Cases

| Scenario | Treatment |
|---|---|
| Capital asset sale | No Form 2307; no CWT; CGT at 6% via Form 1706 (final tax) |
| Ordinary asset sale (post-RMC 31-2025) | No Form 2307; CWT via Form 1606; seller credits 1606 on ITR |
| Government agency buys property from developer | Government withholds creditable VAT → files Form 1600-VT → issues Form 2307 (ATC WV010/WV020) to developer → developer enters on 2550Q Schedule 3, Item 16 |
| Payee cannot obtain Form 2307 from withholding agent | Cannot claim tax credit; may demand issuance or seek BIR intervention; risk of double taxation |
| Over-remittance by withholding agent | Agent must correct Form 2307 to payee; carry forward to next quarter (same year only) or claim refund |
| Multiple ATCs to same payee in same quarter | Multiple line items on single Form 2307 |
| Zero-amount month | Enter ₱0 in that month's columns; still issue if other months have amounts |
| Withholding agent fails to remit but issues Form 2307 | Payee may still claim credit; withholding agent bears liability for un-remitted tax |
| EOPT — expense disallowance repealed | Pre-EOPT: payor's expense disallowed if EWT not withheld (Sec. 34(K)). Post-EOPT: disallowance repealed; penalties still apply but expense deductibility preserved |
| EOPT — withholding timing simplified | Obligation arises "at time income becomes payable" (not earlier of payment/accrual/recording) |
| Socialized housing (RA 7279) | CWT exempt; no Form 2307 generated for property sale |
| Digital 2307 copies (RMC 14-2025) | Scanned/electronic copies acceptable for credit claims if verifiable against SAWT |

---

## Worked Examples

### Example 1: Developer Issues Form 2307 to Licensed Broker (Q2)

```
Payor: ABC Development Corp (withholding agent: YES — juridical entity)
Payee: Maria Santos, PRC-licensed real estate broker (individual)
ATC: WI040 (broker commission, individual, ≤₱3M)
Rate: 10%
Commission payments:
  April: ₱150,000
  May: ₱200,000
  June: ₱0

Form 2307:
  Month 1 (April): Amount = ₱150,000; Tax = ₱15,000
  Month 2 (May):   Amount = ₱200,000; Tax = ₱20,000
  Month 3 (June):  Amount = ₱0;       Tax = ₱0
  Total:           Amount = ₱350,000;  Tax = ₱35,000

Issuance deadline: July 20 (20 days after Q2 close)

Developer side:
  → Files 0619-E for April (by May 10) remitting ₱15,000
  → Files 0619-E for May (by June 10) remitting ₱20,000
  → Files 1601-EQ for Q2 (by July 31): Item 19 = ₱35,000 (+ other payees)
  → Submits QAP (DAT file) to esubmission@bir.gov.ph by July 31

Broker side:
  → Records ₱35,000 as "Income Tax Pre-payment" (asset)
  → Prepares SAWT for Q2 showing ₱35,000 from ABC Development Corp
  → Claims ₱35,000 credit on Form 1701Q (quarterly ITR) filed by Aug 15
```

### Example 2: Corporate Lessee Issues Form 2307 to Individual Lessor (Q3)

```
Payor: XYZ Holdings Inc. (withholding agent: YES)
Payee: Juan dela Cruz (individual lessor)
ATC: WI100 (real property rental, individual)
Rate: 5%
Monthly rent: ₱100,000

Form 2307:
  Month 1 (July):      Amount = ₱100,000; Tax = ₱5,000
  Month 2 (August):    Amount = ₱100,000; Tax = ₱5,000
  Month 3 (September): Amount = ₱100,000; Tax = ₱5,000
  Total:               Amount = ₱300,000; Tax = ₱15,000

Issuance deadline: October 20

Lessor (payee):
  → Receives Form 2307 showing ₱15,000 withheld for Q3
  → Attaches to SAWT when filing quarterly/annual ITR
  → Claims ₱15,000 against income tax liability
```

### Example 3: Year-End Reconciliation Chain

```
ABC Development Corp — Full Year EWT Summary:
  Q1: Form 1601-EQ total = ₱450,000; QAP submitted; Form 2307s issued to 15 payees
  Q2: Form 1601-EQ total = ₱520,000; QAP submitted; Form 2307s issued to 18 payees
  Q3: Form 1601-EQ total = ₱380,000; QAP submitted; Form 2307s issued to 12 payees
  Q4: Form 1601-EQ total = ₱610,000; QAP submitted; Form 2307s issued to 20 payees

Annual reconciliation:
  Form 1604-E total = ₱1,960,000 (must equal sum of 4 quarterly 1601-EQ totals)
  Annual Alphalist: lists all payees by TIN, ATC, amounts — DAT file to esubmission@bir.gov.ph
  Deadline: March 1 of following year

BIR cross-match:
  Each payee's SAWT claim → compared against ABC's Alphalist
  Maria Santos (broker) claims ₱35,000 from Q2 → ABC's Alphalist shows ₱35,000 → MATCH ✓
  If mismatch → audit trigger for both parties
```

---

## Penalties

| Violation | Penalty | Legal Basis |
|---|---|---|
| Failure to issue Form 2307 | ₱1,000 per failure, max ₱25,000/year | NIRC Section 250 |
| Same — Micro/Small taxpayer (EOPT) | ₱500 per failure, max ₱12,500/year | RR 6-2024 (50% reduction) |
| Willful failure to withhold/issue | ₱10,000–₱100,000 fine and/or 1–10 years imprisonment | NIRC Section 255 |
| Late filing of QAP/Alphalist | ₱1,000–₱25,000 per instance | RMO 7-2015 |
| Non-withholding — expense disallowance | **REPEALED** under EOPT (Sec. 34(K) no longer operative) | RA 11976 |
| Non-withholding — withholding agent liability | Agent personally liable for un-withheld tax + 25% surcharge + 12% interest | NIRC Sec. 251, 248, 249 |

---

## Legal Citations

| Provision | Citation |
|---|---|
| Withholding authority | NIRC Section 57 |
| Certificate issuance obligation | NIRC Section 58(B) |
| EWT rates and categories | RR 2-98 as amended by RR 11-2018 |
| SAWT requirement | RR 2-2006 |
| QAP submission | RMO 7-2015; RMC 15-2025 (Alphalist Module v7.4) |
| Annual alphalist (1604-E) | RR 1-2014 (electronic submission mandate) |
| Form 2307 discontinued for property CWT | RMC 99-2023; RMC 31-2025 |
| Digital copies acceptable | RMC 14-2025 |
| EOPT — Section 34(K) repeal | RA 11976 (EOPT Act) |
| EOPT — simplified withholding timing | RA 11976 Section 57 amendment |
| Compromise penalty reduction | RR 6-2024 (Micro/Small taxpayer 50% reduction) |
| Penalties for non-issuance | NIRC Section 250 (administrative), Section 255 (criminal) |

---

## Automation Assessment

**Complexity:** MEDIUM

| Dimension | Score | Notes |
|---|---|---|
| Formula complexity | LOW | Simple multiplication: gross × rate |
| Branching rules | MEDIUM | 8 real estate-adjacent ATC categories with threshold/declaration gates |
| Lookup tables | LOW | ATC rate table is static; updated only on RR amendments |
| External data dependencies | MEDIUM | Payee TIN validation, payee gross income declaration, VAT registration status |
| Multi-period tracking | HIGH | Monthly amounts per payee per ATC → quarterly aggregation → annual reconciliation |
| Filing chain complexity | HIGH | 0619-E → 1601-EQ + QAP → 1604-E + Alphalist → must all reconcile |
| Bilateral reconciliation | HIGH | Payor QAP vs. payee SAWT — BIR cross-matching requires both sides |

**Key automation opportunities:**
1. **Form 2307 auto-generation** from payment records — compute EWT per payment, aggregate monthly per payee per ATC, generate quarterly certificate
2. **QAP DAT file generation** — structure payee data into BIR-compliant DAT format for esubmission
3. **SAWT auto-compilation** (payee side) — aggregate all received 2307s into SAWT attachment for ITR
4. **Reconciliation engine** — cross-check issued 2307 totals against 0619-E / 1601-EQ / 1604-E before filing
5. **Deadline tracking** — 20-day post-quarter issuance, monthly 0619-E, quarterly 1601-EQ, annual 1604-E

**Automation blockers:**
- Payee gross income declaration (Annex B-1/B-2/B-3) is a payee-provided input — requires intake workflow
- ATC code selection for edge cases (e.g., referral fees to unlicensed agents) may require judgment
- BIR DAT file format specifications change with each Alphalist Module version

---

## Verification Summary

**Verified against:** JuanTax (BIR Form 2307 guide), Taxumo (comprehensive 2307 guide), Respicio & Co. (understanding 2307 issues), Philippine Business Tools (2307 Q&A), MPM Consulting (QAP guide), Forvis Mazars PH (RMC 99-2023), PwC PH (Tax Alert 28), AJA Law (RMC 31-2025), BIR CDN (RMC 31-2025 official digest), Omni HR (2307 explained), Grant Thornton PH (QAP submission), Triple-i Consulting (SAWT guide), Chan Robles (NIRC Sec 250 codal text).

**Confirmed (8 of 10 points):** Withholding agent determination, 20-day quarterly issuance deadline, amount computation formula, payee ITR credit mechanism, reconciliation chain (0619-E → 1601-EQ + QAP → 1604-E + Alphalist), RMC 31-2025 Form 1606 carve-out, penalty structure (Sec. 250 + Sec. 255), QAP DAT file submission to esubmission@bir.gov.ph.

**Corrections applied (2 conflicts):**
1. **VAT withholding certificate deadline:** Primary source said "10 days"; corrected to match the standard 20-day rule. The 10-day figure conflates the 0619-E remittance deadline with the certificate issuance deadline. (Medium confidence — precise VAT withholding certificate deadline warrants further verification against RR 10-93.)
2. **Number of copies:** Primary source said "4 copies"; corrected to **3 copies** per regulatory standard (original/payee, duplicate/BIR, triplicate/withholding agent). Multiple secondary sources confirm triplicate.

**Key additions from verification:**
1. SAWT (Summary Alphalist of Withholding Taxes) — mandatory payee-side attachment under RR 2-2006
2. EOPT repealed Section 34(K) — non-withholding no longer triggers expense disallowance
3. EOPT simplified withholding timing — obligation arises "at time income becomes payable"
4. RMC 14-2025 — digital copies acceptable for credit/refund claims
5. RMC 31-2025 — separate ITR line items for EWT credits (Form 2307) vs CWT credits (Form 1606)
6. One transaction per Form 1606 (RMC 31-2025)
7. Compromise penalty 50% reduction for Micro/Small taxpayers (RR 6-2024)
8. eAFS upload — scanned 2307 PDFs within 15 days of e-filing ITR
9. Alphalist Data Entry and Validation Module v7.4 (RMC 15-2025)
10. e-2307 Mobile QR Verification pilot (RMC 87-2025) — signals BIR direction toward real-time digital verification

## Sources

- [JuanTax — BIR Form 2307](https://juan.tax/blog/bir-form-2307/)
- [Taxumo — Guide BIR Form 2307](https://www.taxumo.com/blog/comprehensible-guide-bir-form-2307/)
- [Respicio & Co. — Understanding BIR Form 2307](https://www.respicio.ph/commentaries/understanding-bir-form-2307-tax-withholding-issues)
- [Philippine Business Tools — Form 2307 Answered](https://philippinebusinesstools.com/bir/forms/form-2307/)
- [MPM Consulting — QAP for 1601EQ](https://mpm.ph/quarterly-alphalist-of-payees-qap/)
- [Forvis Mazars — RMC 99-2023](https://www.forvismazars.com/ph/en/insights/tax-alerts/bir-rmc-99-2023)
- [PwC PH — Tax Alert 28](https://www.pwc.com/ph/en/tax/tax-publications/tax-alerts/2023/tax-alert-28.html)
- [AJA Law — RMC 31-2025](https://www.ajalaw.ph/bir-rmc-31-2025-ordinary-assets-tax/)
- [BIR CDN — RMC 31-2025 Digest](https://bir-cdn.bir.gov.ph/BIR/pdf/RMC%20No.%2031-2025%20Digest.pdf)
- [Omni HR — BIR Form 2307 Explained](https://www.omnihr.co/blog/bir-2307-form)
- [Grant Thornton PH — Submitting QAP](https://www.grantthornton.com.ph/insights/articles-and-updates1/tax-notes/submitting-the-quarterly-alphabetical-list-of-payees-qap/)
- [Triple-i Consulting — SAWT](https://www.tripleiconsulting.com/how-submit-sawt-with-philippines-bir/)
- [Forvis Mazars — EOPT Act IRR](https://www.forvismazars.com/ph/en/insights/tax-alerts/ease-of-paying-taxes-act/implementing-rules-and-regulations-of-the-eopt-act)
