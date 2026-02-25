# BIR Form 2307 — Certificate of Creditable Tax Withheld at Source
## Comprehensive Reference for Philippine Tax Practitioners

**Legal Basis:** Section 57 and 58, National Internal Revenue Code (NIRC); Revenue Regulations No. 2-98 as amended by RR No. 11-2018 (TRAIN Law implementation); RMO No. 38-2018

---

## 1. Purpose and Overview

BIR Form 2307 is the **Certificate of Creditable Tax Withheld at Source**. It is issued by a withholding agent (payor) to the income recipient (payee) as evidence that a portion of the income payment was withheld as tax and remitted to the BIR on the payee's behalf.

The form functions as an **income tax prepayment** in the payee's books — classified under assets — and is creditable against the payee's quarterly and annual income tax liability. Without it, the payee cannot claim the withheld amount as a tax credit.

**Form version:** January 2018 ENCS (Enhanced New Computerized System), v3 — current as of 2026.

---

## 2. Parties Involved

### Withholding Agent (Issuer)
Any person or entity required by law to deduct and withhold tax from income payments, including:
- Corporations paying professional fees, rentals, contractor fees, or services
- Top Withholding Agents (Large Taxpayers, Top 20,000 private corporations, Top 5,000 individual taxpayers) as classified and notified by the BIR Commissioner under RR No. 1-98 and RR No. 6-2009
- Buyers/transferees of real property classified as ordinary assets (who remit via BIR Form 1606)
- Government agencies and GOCCs making income payments to local suppliers
- Any business entity making payments subject to Expanded Withholding Tax (EWT)

### Payee (Recipient)
Any individual or non-individual entity (corporation, partnership, cooperative) receiving income subject to creditable/expanded withholding tax, including:
- Self-employed professionals (lawyers, CPAs, engineers, doctors)
- Real estate service practitioners (brokers, appraisers, consultants)
- Contractors and subcontractors
- Lessors/landlords (individuals or corporations) receiving rental income
- Sellers of real property classified as ordinary assets
- Suppliers of goods and services to Top Withholding Agents

---

## 3. Form Structure and Fields

### Header
- **For the Period From / To:** MM/DD/YYYY format — the taxable quarter covered by the certificate

### Part I — Payee Information
| Field | Description |
|-------|-------------|
| Field 1 | Period covered (MM/DD/YY to MM/DD/YY) |
| Field 2 | Payee's Taxpayer Identification Number (TIN) — format: NNN-NNN-NNN-NNNNN |
| Field 3 | Payee's Name — Last Name, First Name, Middle Name (Individual) OR Registered Name (Non-Individual/Corporation) |
| Field 4 | Registered Address of the Payee |
| Field 4A | ZIP Code |
| Foreign Address | If payee has a foreign address (for non-resident payees) |

Source: BIR Certificate of Registration (Form 2303), DTI/SEC registration documents.

### Part II — Payor / Withholding Agent Information
| Field | Description |
|-------|-------------|
| Field 5 | Payor's/Withholding Agent's TIN |
| Field 6 | Payor's Name (Registered Name for corporations) |
| Field 7 | Payor's Registered Address |
| Field 7A | ZIP Code |

### Part III — Monthly Income Payments and Taxes Withheld
This is the core computation section. It is structured as a **quarterly table** broken down by month (Month 1, Month 2, Month 3 of the quarter).

For each line item (one ATC per line):
| Column | Description |
|--------|-------------|
| ATC | Alphanumeric Tax Code identifying the nature of income payment |
| Nature of Income Payment | Text description matching the ATC |
| Month 1 Amount | Gross income paid in first month of quarter |
| Month 1 Tax Withheld | Tax withheld in first month (Amount × Rate) |
| Month 2 Amount | Gross income paid in second month of quarter |
| Month 2 Tax Withheld | Tax withheld in second month |
| Month 3 Amount | Gross income paid in third month of quarter |
| Month 3 Tax Withheld | Tax withheld in third month |
| Total Amount | Sum of three months' income payments |
| Total Tax Withheld | Sum of three months' taxes withheld |

**Computation formula per line:**
```
Tax Withheld = Gross Income Payment × ATC Rate
Total Tax Withheld (quarter) = Sum of monthly tax withheld amounts
```

For real estate sales (ordinary asset), the tax base is the **higher of**:
- Gross Selling Price (total consideration), or
- Fair Market Value (zonal value per BIR, or assessed value per local government, whichever is higher)

### Signature Section
- Signature of Withholding Agent/Authorized Representative
- Printed Name and Title/Designation
- Date of Issue
- TIN of signatory

---

## 4. ATC Codes Relevant to Real Estate Transactions

### 4.1 Property Rentals (Expanded Withholding Tax)

| ATC | Taxpayer Type | Description | Rate |
|-----|--------------|-------------|------|
| **WI100** | Individual | Rentals: gross rental or lease for continued use/possession of personal property (exceeding PHP 10,000 annually) AND real property used in business — Individual lessor | **5%** |
| **WC100** | Corporation | Same as WI100 but for corporate lessors | **5%** |
| WI110 | Individual | Cinematographic film rentals — Individual | 5% |
| WC110 | Corporation | Cinematographic film rentals — Corporate | 5% |

**Key rule:** The 5% EWT on rentals applies to payments for real property used in business. Purely residential lease payments to individual landlords may be treated differently depending on whether the lessee is a withholding agent.

**Applies to:** Office rentals, commercial space rentals, industrial property rentals, land lease payments, billboard/signage rentals, transmission facility rentals.

### 4.2 Real Estate Service Practitioners (RESPs) — Commissions and Fees

Under RA 9646 (Real Estate Service Act), RESPs include: real estate brokers, real estate appraisers, and real estate consultants.

| ATC | Taxpayer Type | Description | Rate |
|-----|--------------|-------------|------|
| **WI139** | Individual RESP | Gross commissions or service fees of customs, insurance, stock, immigration and commercial brokers, agents of professional entertainers, and **Real Estate Service Practitioners (RESPs)** — if gross income for the current year does NOT exceed **PHP 3,000,000** (or not VAT-registered) | **5%** |
| **WI140** | Individual RESP | Same categories — if gross income **exceeds PHP 3,000,000** OR **VAT-registered** regardless of amount | **10%** |
| **WC139** | Corporate RESP | Gross commissions or service fees of RESPs (corporate entity) — if gross income does NOT exceed **PHP 720,000** | **10%** |
| **WC140** | Corporate RESP | Same — if gross income **exceeds PHP 720,000** | **15%** |

**Note on thresholds:** The PHP 3M threshold for individuals and PHP 720,000 threshold for corporations reflects the TRAIN Law (RR 11-2018) revision from the prior uniform rate. The threshold is measured against the payee's **cumulative gross income for the current taxable year**.

**Commissions included:** Broker commission on sale of real property (typically 3–5% of selling price), appraisal fees, consultancy retainers.

### 4.3 Sale of Real Property Classified as Ordinary Asset

**Legal basis:** Section 2.57.2(J), RR No. 2-98 as amended by RR No. 6-2001 and RR No. 7-2003.

**Governing form for remittance:** BIR Form 1606 (Withholding Tax Remittance Return for Onerous Transfer of Real Property Other than Capital Asset — Including Taxable and Exempt).

**Form 2307 issuance:** After the buyer remits via Form 1606, the buyer (withholding agent) issues Form 2307 to the seller (payee) evidencing the creditable withholding tax.

| ATC | Taxpayer Type | Seller Condition | Selling Price Bracket | Rate |
|-----|--------------|------------------|-----------------------|------|
| **WI157** | Individual seller | Habitually engaged in real estate business | SP ≤ PHP 500,000 | **1.5%** |
| **WI157** | Individual seller | Habitually engaged in real estate business | PHP 500,000 < SP ≤ PHP 2,000,000 | **3%** |
| **WI157** | Individual seller | Habitually engaged in real estate business | SP > PHP 2,000,000 | **5%** |
| **WI157** | Individual seller | NOT habitually engaged (includes banks on foreclosed properties) | Any amount | **6%** |
| **WC157** | Corporate seller | Habitually engaged in real estate business | SP ≤ PHP 500,000 | **1.5%** |
| **WC157** | Corporate seller | Habitually engaged in real estate business | PHP 500,000 < SP ≤ PHP 2,000,000 | **3%** |
| **WC157** | Corporate seller | Habitually engaged in real estate business | SP > PHP 2,000,000 | **5%** |
| **WC157** | Corporate seller | NOT habitually engaged | Any amount | **6%** |

**"Ordinary asset" determination (RR No. 7-2003):** Real property is an ordinary asset — not a capital asset — when it is:
- Stock in trade or property held primarily for sale to customers
- Property used in trade/business of the seller
- Real property acquired by a bank through foreclosure (per RR 7-2003, banks are not considered habitually engaged in real estate)
- Property of a real estate developer, dealer, or operator

**Tax base:** Higher of (a) gross selling price/total consideration in deed of sale, or (b) fair market value [higher of BIR zonal value under Section 6(E) of NIRC or assessed value per local government schedule].

**Remittance deadline:** Within **10 days** following the end of the month in which the transaction occurred (BIR Form 1606).

**Note:** Sale of real property classified as a **capital asset** is NOT subject to creditable withholding tax and does NOT generate a Form 2307. Capital asset sales are subject to the 6% Capital Gains Tax via BIR Form 1706 (final tax, not creditable).

### 4.4 Payments by Top Withholding Agents to Real Estate-Related Suppliers

| ATC | Taxpayer Type | Description | Rate |
|-----|--------------|-------------|------|
| **WI158** | Individual | Income payments by top withholding agents to local/resident **suppliers of goods** (including real property as goods) — not covered by other specific rates | **1%** |
| **WC158** | Corporation | Same, for corporate supplier | **1%** |
| **WI160** | Individual | Income payments by top withholding agents to local/resident **suppliers of services** — not covered by other specific rates | **2%** |
| **WC160** | Corporation | Same, for corporate service provider | **2%** |
| WI157 / WC157 | Both | Government and GOCC payments to local suppliers of services | 2% |
| WI640 / WC640 | Both | Government and GOCC payments to local suppliers of goods | 1% |

**Single transaction threshold:** Even for non-regular suppliers, a **single purchase of PHP 10,000 or more** triggers the WI158/WC158 or WI160/WC160 withholding obligation for top withholding agents.

### 4.5 Real Estate Investment Trusts (REITs)

| ATC | Taxpayer Type | Description | Rate |
|-----|--------------|-------------|------|
| WC690 | Corporation | Income payments received by REIT | 1% |
| WC700 | Corporation | Cash or property dividends paid by REIT | 10% (final) |
| WI700 | Individual | Cash or property dividends paid by REIT | 10% (final) |

### 4.6 WE Series Context

The "WE" designation in the Tax Type column (WE_PH) means **Expanded Withholding Tax** — these are creditable (not final) taxes. The WE series are all creditable against the payee's income tax. Contrast with WF_PH (final withholding tax, e.g., dividends, interest from deposits).

**All real estate creditable withholding tax codes are WE_PH type:**
- WI100/WC100 (rentals) — WE_PH
- WI139/WC139, WI140/WC140 (broker commissions) — WE_PH
- WI157/WC157 (sale of ordinary asset) — WE_PH
- WI158/WC158, WI160/WC160 (top withholding agent payments) — WE_PH

---

## 5. Issuance Requirements

### Who is Required to Issue
The **withholding agent/payor** issues the certificate. They are legally obligated under Section 58(B) of the NIRC and Section 2.83 of RR No. 2-98.

### When to Issue
| Income Payment Type | Issuance Deadline |
|--------------------|-------------------|
| Expanded Withholding Tax (EWT) payments | On or before the **20th day of the month following the close of the taxable quarter** in which the income was earned |
| Percentage taxes / VAT withholding | On or before the **10th day of the month** following the month of withholding |
| Upon payee's request | **Simultaneously with the income payment** — payor must furnish on demand |

**Quarterly issuance schedule (EWT):**
- Q1 (Jan–Mar) → Issue by **April 20**
- Q2 (Apr–Jun) → Issue by **July 20**
- Q3 (Jul–Sep) → Issue by **October 20**
- Q4 (Oct–Dec) → Issue by **January 20** (of following year)

### Number of Copies
Four (4) copies:
- Original — for the BIR (attached by payee to tax return)
- Duplicate — for the payee
- Triplicate — retained by the withholding agent
- Quadruplicate — additional copy

### Retention
Both the withholding agent and the payee must retain copies for at least **3 years** for audit purposes.

---

## 6. How the Recipient Uses Form 2307 as a Tax Credit

### In the Payee's Books
Form 2307 amounts are recorded in the payee's chart of accounts as **Income Tax Pre-payments** (an asset account), not as an expense.

### On Quarterly Income Tax Returns
Payees accumulate all received Form 2307 certificates within the quarter and report the total tax withheld in the **Schedule of Taxes Withheld** section of:
- **BIR Form 1701Q** — Quarterly Income Tax Return for Individuals
- **BIR Form 1702Q** — Quarterly Income Tax Return for Corporations

The credit is claimed provisionally each quarter, reducing the quarterly income tax due.

### On Annual Income Tax Returns
At year-end, all Form 2307 received during the year are consolidated and claimed as credits on:
- **BIR Form 1701** — Annual ITR for Individuals (self-employed, professionals)
- **BIR Form 1701A** — Annual ITR for Individuals (purely compensation or purely business)
- **BIR Form 1702-RT/EX/MX** — Annual ITR for Corporations

**Claiming procedure:**
1. Gather all Form 2307 received for the full year
2. Compute total creditable withholding taxes per ATC
3. Enter aggregate amount in the "Tax Credits/Payments" section of the ITR
4. Attach original copies of all Form 2307 to the filed return
5. If total credits exceed tax due, the excess may be carried forward or applied for refund

**Effect:** If total creditable taxes withheld (from all Form 2307s) ≥ income tax liability, no additional tax payment is due. If taxes withheld > income tax liability, the excess is either refunded or carried over as a tax credit to the next year.

### Documentary Requirement
For online filers via eFPS or eBIRForms, **scanned copies (soft copies)** of Form 2307 must be submitted via the **Electronic Audited Financial Statement (eAFS)** system. Physical originals are still retained by the taxpayer.

---

## 7. Related Remittance and Filing Forms

| Form | Purpose | Filed By | Deadline |
|------|---------|----------|----------|
| **BIR Form 0619-E** | Monthly Remittance Return of Creditable Income Tax Withheld (Expanded) — for non-eFPS filers | Withholding Agent | On or before the **10th day** of the following month (non-eFPS); varies for eFPS by group |
| **BIR Form 1601-EQ** | Quarterly Remittance Return of Creditable Income Taxes Withheld (Expanded) | Withholding Agent | On or before the **last day of the month** following the close of the quarter |
| **BIR Form 1606** | Withholding Tax Remittance Return — onerous transfer of real property (ordinary asset) | Buyer/transferee | Within **10 days** following end of month of transaction |
| **BIR Form 1604-E** | Annual Information Return of Creditable Income Taxes Withheld (Expanded) | Withholding Agent | On or before **March 1** of the following year |

---

## 8. Reconciliation Requirement — BIR Form 1604-E and Alphalist

### BIR Form 1604-E Overview
The **Annual Information Return of Creditable Income Taxes Withheld (Expanded)** consolidates all EWT data from January through December. It summarizes the monthly remittances made on BIR Form 1601-E/0619-E throughout the year.

**Filer:** Every withholding agent (individual or non-individual) who withholds EWT during the year.

**Deadline:** On or before **March 1** of the following year.

**Filing method:** Mandatory electronic filing — via eFPS or eBIRForms, with alphalist DAT file emailed to esubmission@bir.gov.ph.

### Alphalist of Payees (Required Attachment to 1604-E)
The Alphalist is a detailed listing of every payee from whom EWT was withheld during the year. It is submitted as a **DAT file** generated by the BIR Alphalist Data Entry and Validation Module.

**Schedule 3 (Alphalist attachment to 1604-E):** Alphalist of Other Payees whose income payments are **exempt from withholding tax but subject to income tax** (declared/certified using Form 2307).

**Schedule 4 (Alphalist attachment to 1604-E):** Alphalist of Payees **subjected to Expanded Withholding Tax** (declared/certified using Form 2307).

Each alphalist entry includes:
- Payee's registered name
- Payee's TIN
- Nature of income payment (ATC)
- Gross amount of income paid
- Amount of tax withheld
- Month/period

### Quarterly Alphalist of Payees (QAP)
Attached to **BIR Form 1601-EQ** (quarterly remittance return). Also submitted as a DAT file to esubmission@bir.gov.ph. Filed on the same deadline as 1601-EQ.

### The Reconciliation Chain
```
Form 0619-E (monthly)
    → Form 1601-EQ (quarterly) + QAP
        → Form 1604-E (annual) + Annual Alphalist
            = Must reconcile with all issued Form 2307s
```

**BIR TIN-matching validation:** The BIR cross-checks amounts on Form 2307 certificates (as filed by payees in their ITRs) against the withholding agent's QAP and Form 1604-E alphalist. Discrepancies trigger audit notices.

**Consequences of mismatches:**
- BIR letter of authority for tax audit
- Disallowance of tax credits claimed by payee
- Surcharges and interest on withholding agent for under-remittance
- Penalties for failure to file correct alphalist

---

## 9. Relationship Between Forms 1604-C and 1604-E

### BIR Form 1604-C
- Full name: Annual Information Return of **Income Taxes Withheld on Compensation**
- The "C" stands for **Compensation** — employer-employee relationship payments
- Covers: salaries, wages, allowances, bonuses subject to withholding tax on compensation
- Accompanying document: **Alphalist of Employees** (Schedule 1 and Schedule 2)
- Deadline: **January 31** of the following year
- Related certificate: **BIR Form 2316** (Certificate of Compensation Payment/Tax Withheld) — issued to each employee
- No payment form attached (taxes already remitted monthly via Form 1601-C)

### BIR Form 1604-E
- Full name: Annual Information Return of **Creditable Income Taxes Withheld (Expanded)**
- The "E" stands for **Expanded** withholding tax
- Covers: professional fees, rentals, contractor payments, commissions, sale of ordinary assets, and all other EWT-subject payments
- Accompanying document: **Alphalist of Payees** (Schedules 3 and 4)
- Deadline: **March 1** of the following year
- Related certificate: **BIR Form 2307** (Certificate of Creditable Tax Withheld at Source)

### Summary Comparison

| Feature | Form 1604-C | Form 1604-E |
|---------|-------------|-------------|
| Withholding type | Compensation (salary) | Expanded (EWT) |
| Related certificate | Form 2316 | Form 2307 |
| Alphalist content | Employees | Payees/suppliers/contractors |
| Deadline | January 31 | March 1 |
| Monthly basis | Form 1601-C | Form 0619-E |
| Quarterly basis | Form 1601-C | Form 1601-EQ |
| Payee's ITR use | Form 2316 (substituted filing or attachment) | Form 2307 attached to 1701/1702 |

---

## 10. Electronic Filing Rules — eBIRForms and eFPS

### Who Must Use eFPS (Electronic Filing and Payment System)
Mandatory eFPS users include (per RR No. 9-2001 and subsequent amendments):
- Large Taxpayers (as classified under RR No. 1-98)
- Top 20,000 Private Corporations (RR No. 6-2009)
- Top 5,000 Individual Taxpayers (RR No. 6-2009, RMO No. 26-2018)
- Taxpayer Account Management Program (TAMP) taxpayers
- PEZA/BOI and other fiscal incentive registered enterprises
- Corporations with paid-up capital of PHP 10 million and above
- Corporations with a complete Computerized Accounting System (CAS)
- Insurance companies and stockbrokers
- National Government Agencies and GOCCs
- Licensed Local Contractors
- Procuring government agencies and government bidders

**eFPS group filing deadlines:** Large taxpayers and eFPS enrollees file in staggered groups (Group A through E) with deadlines differing by 1–5 days from the base deadline. For non-group-specific forms, the standard deadline applies.

### Who Uses eBIRForms
Non-eFPS filers — including smaller corporations, self-employed individuals, freelancers, and professionals — use the **Offline eBIRForms Package** downloadable from the BIR website. The EOPT Act (2024) broadened mandatory electronic filing to cover most taxpayers.

**Manual filing** remains available only for:
- Individual business taxpayers classified as Micro and Small enterprises (BIR Form 1701-MS filers)
- Taxpayers with lack of internet access (with BIR approval)
- Cases of system unavailability covered by BIR advisory

### Electronic Submission of Form 2307 Data
Form 2307 itself is a **certificate issued to the payee** — it is not filed directly with BIR as a standalone electronic form. However:

1. **Withholding agent:** Reports all Form 2307 data through:
   - QAP (DAT file) attached to 1601-EQ, emailed to esubmission@bir.gov.ph
   - Annual Alphalist (DAT file) attached to 1604-E, same email
   - Summary Alphalist of Withholding Taxes (SAWT) — system-generated acknowledgement receipt required

2. **Payee (claiming credits):** Must submit **scanned copies of original Form 2307** electronically via:
   - **eAFS (Electronic Audited Financial Statement)** system
   - Required when attaching Form 2307 as support for tax credits in ITR filings
   - Hard copy originals are retained by the taxpayer; the BIR electronic system receives the scanned copies

3. **QAP submission:** DAT file must be emailed to **esubmission@bir.gov.ph** no later than the 1601-EQ filing deadline. Penalty for non-submission: PHP 1,000 to PHP 25,000 per RMO No. 7-2015.

### eFPS Unavailability Fallback
If eFPS is unavailable (system downtime covered by BIR advisory, enrollment still in process, or form not yet available in eFPS), mandatory eFPS filers may use eBIRForms as a fallback without penalty, provided the BIR advisory is documented.

### Form Substitution
There is no "substitution" of Form 2307 itself. However, related concepts:
- **Substituted Filing (Form 2316):** Applies only to Form 2316 (compensation withholding) — employees with a single employer may have their employer file Form 2316 with the BIR in lieu of filing an individual ITR. This does NOT apply to Form 2307.
- Form 2307 must always be issued by the withholding agent and retained/attached by the payee — no substitution mechanism exists for EWT certificates.

---

## 11. Penalties for Non-Compliance

### Failure to Withhold
- The withholding agent becomes **personally liable** for the unwithheld tax
- 25% surcharge on deficiency
- 12% annual interest (post-TRAIN; was 20% prior to TRAIN Law)
- Possible criminal liability under Section 255 of the NIRC

### Failure to Issue Form 2307
- Civil penalty: PHP 1,000 per failure to issue, up to PHP 25,000 per year (Section 250, NIRC)
- Criminal penalties: Fine of PHP 5,000 to PHP 50,000 and/or imprisonment of 1–10 years for willful violations (Section 255, NIRC)

### Failure to Remit Withheld Taxes
- 25% surcharge (or 50% if fraudulent)
- 12% per annum interest
- Criminal liability

### Failure to File QAP / Alphalist
- PHP 1,000 to PHP 25,000 per instance (RMO No. 7-2015)
- Payee's tax credits may be disallowed during BIR audit if not validated by alphalist

### Payee's Risk Without Form 2307
If the payee cannot produce Form 2307 from the withholding agent:
- Cannot claim the tax credit in ITR
- Risk of double taxation on amounts already withheld
- May need to demand issuance from payor or seek BIR intervention

---

## 12. Special Rules for Real Estate Transactions

### Ordinary Asset vs. Capital Asset Determination
The classification drives the entire tax treatment:

| Characteristic | Ordinary Asset | Capital Asset |
|---------------|----------------|---------------|
| Who holds it | Real estate dealer/developer; property used in business | Individual holding private residential property not used in business |
| Tax on sale | Income Tax + CWT (creditable) via EWT | Capital Gains Tax (6%, final) — no CWT, no Form 2307 |
| Filing form | Form 1606 (buyer remits), Form 2307 (issued to seller) | Form 1706 (seller pays CGT directly) |
| VAT | 12% VAT on sale (if seller is VAT-registered or threshold exceeded) | Exempt from VAT |
| DST | 1.5% Documentary Stamp Tax on deed of sale | 1.5% DST also applies |

### Installment Sales of Ordinary Assets
Per **BIR Ruling No. OT-028-2024**: The CWT base for installment sales is each **installment payment** as it is received, not the full contract price. Each installment payment triggers:
- A Form 1606 filing by the buyer within 10 days of month-end
- Issuance of a corresponding Form 2307 by the buyer to the seller

### HLURB Socialized Housing Exemption
Real property registered with the Housing and Land Use Regulatory Board (HLURB) as a **Socialized Housing project** is exempt from creditable withholding tax on sale. No Form 2307 is generated for such transactions.

### Bank Foreclosure Sales
Banks selling foreclosed properties are subject to **6% CWT** (ATC WC157) regardless of selling price, because under RR No. 7-2003, banks are NOT considered habitually engaged in the real estate business. The foreclosed property is classified as an ordinary asset of the bank.

---

## 13. Official Sources and References

**BIR Official Website:** https://www.bir.gov.ph

**Revenue Regulations:**
- RR No. 2-98 — Consolidated Withholding Tax Regulations (as amended)
- RR No. 6-2001 — Amended rates on sale of real property
- RR No. 7-2003 — Rules on ordinary vs. capital asset classification
- RR No. 11-2018 — TRAIN Law implementation; updated ATC rates and thresholds
- RR No. 9-2001 — eFPS mandatory filing coverage
- RR No. 1-2014 — Electronic submission of alphalists

**Revenue Memorandum Orders:**
- RMO No. 38-2018 — Updated ATC codes effective January 1, 2018
- RMO No. 7-2015 — Penalties for failure to submit alphalists
- RMO No. 26-2018 — Top 5,000 individual taxpayers

**BIR Circulars:**
- RMC No. 99-2023 — Clarification on real property tax rules
- RMC No. 31-2025 — Tax rules on sale of real property as ordinary assets

**Key Forms Referenced:**
- BIR Form 2307 (Jan 2018 ENCS v3): https://bir-cdn.bir.gov.ph/local/pdf/2307%20Jan%202018%20ENCS%20v3.pdf
- BIR Form 1604-E (Jan 2018 ENCS): https://bir-cdn.bir.gov.ph/local/pdf/1604E%20Jan%202018%20ENCS%20Final2.pdf

---

*Compiled 2026-02-25 from BIR official sources, Oracle NetSuite PH tax documentation, Grant Thornton PH, PwC PH Tax Alerts, Ocampo & Suralvo Law Offices, and Philippine tax practitioner resources.*
