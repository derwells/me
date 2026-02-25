# Accounting Agency Handoff — PH Rental Corporation

Source acquired: 2026-02-25
Applicable to: SEC-registered rental property corporation, Las Piñas, mixed commercial/residential, ~20-100 units, VAT-registered (exceeds PHP 3M threshold).

---

## Overview

The property management team prepares raw data; the external accounting agency uses it to:
1. Maintain books of accounts (journal entries, ledgers)
2. File BIR monthly/quarterly/annual returns
3. Prepare and audit financial statements for SEC filing
4. Issue 2307-based tax credit documentation

Deliver monthly data package by **5th of following month** to allow accountant to file by the 10th–25th deadlines.

---

## 1. Monthly Data Package (Property Manager → Accountant)

### A. Rent Roll (Collections Report)
One row per unit. See Section 4 for full column specification.

### B. Sales Invoice Log (formerly OR Stubs)
**Key rule:** Under **RR 7-2024** (effective April 27, 2024), the **VAT Sales Invoice** is now the primary BIR document for rental income. Official Receipts are now supplementary payment confirmation only (cannot support input VAT claims). Unused ORs may be stamped "INVOICE" per RR 11-2024 until consumed.

Per-invoice log fields:
- Invoice number (sequential, gapless)
- Date issued
- Tenant name and TIN (required if invoice ≥ PHP 1,000)
- Description: "Monthly rental for Unit [X], [Property Address], covering [Period]"
- Gross rent exclusive of VAT
- VAT amount (12%) or "VAT-EXEMPT SALE" notation
- Total amount VAT-inclusive
- ATP (Authority to Print) number or CAS Permit reference

### C. 2307 Register (EWT Certificates Received from Corporate Tenants)
Spreadsheet columns:
- Tenant name and TIN
- Quarter covered
- Gross rental per 2307
- 5% EWT per 2307
- Invoice/OR number referenced

### D. Expense Voucher Package
Per disbursement:
- Disbursement/Check Voucher number
- Date
- Payee name and TIN
- Nature of expense (repairs, utilities, professional fees, supplies, insurance, RPT, etc.)
- Amount
- Supporting receipt (must be BIR-registered invoice from supplier)
- Whether input VAT is creditable (from VAT-registered suppliers)

### E. Bank Reconciliation Data
- Bank statement per account (PDF)
- Checkbook register / payment log
- Deposit slips reconciled to rent collections
- Uncleared checks list
- Accountant prepares formal Bank Rec; property manager provides raw data

### F. Payroll Summary (if in-house staff)
- Gross salaries per employee
- SSS, PhilHealth, Pag-IBIG contributions (employee + employer shares)
- Withholding tax on compensation
- Net pay disbursed

### G. New Lease Contracts / Amendments
Any lease signed or renewed during the month → triggers DST computation (Form 2000) and LIS update.

---

## 2. Quarterly Data Package

Quarter closes: March 31, June 30, September 30, December 31.

### A. BIR Form 1601-EQ — Quarterly EWT Remittance
*Filed by corporation as withholding agent*
*Deadline: Last day of month following the quarter (e.g., April 30 for Q1)*

Client data needed:
- All payments to suppliers/contractors subject to EWT during the quarter
- Per payment: payee TIN, payee name, ATC (e.g., WC010 = professional fees 10%, WC158 = contractors 2%), amount paid, EWT withheld
- Monthly 0619-E remittance receipts
- Accountant generates QAP (Quarterly Alphalist of Payees) from this data

### B. BIR Form 2550Q — Quarterly VAT Return
*Deadline: 25th day of month following quarter*
*(Monthly 2550M abolished effective Jan 1, 2023 per RR 13-2018)*

Client data needed:
- Total output VAT collected (12% on VATable rents: commercial + residential > PHP 15,000/mo)
- Total creditable input VAT (purchases from VAT-registered suppliers)
- Input VAT on capital expenditures (if any)
- Carry-forward input VAT from prior quarter
- Breakdown: VAT-exempt sales (qualifying residential unit rentals)

### C. BIR Form 2551Q — Quarterly Percentage Tax (only if non-VAT-registered)
*Deadline: 25th day of month following quarter, ATC: PT010 at 3%*

At 20-100 units, virtually certain to exceed PHP 3M → VAT-registered → 2551Q not applicable. Data if needed: total gross rental receipts for quarter.

### D. BIR Form 1702Q — Quarterly Corporate Income Tax Return
*Deadline: 60th day after each of first 3 quarters*

Client data needed:
- **Revenue**: Gross rents collected, broken down by commercial vs. residential, VATable vs. exempt
- **Direct costs**: Salaries of building staff, direct repairs, property insurance
- **Operating expenses**: Admin salaries, professional fees, common area utilities, office expenses
- **Depreciation**: Updates for any new acquisitions or disposals
- **Interest expense**: Loan statements for the quarter
- **RPT payments made** (deductible)
- **2307 certificates received**: Sum becomes EWT tax credit; supports SAWT attachment

### E. SAWT — Summary Alphalist of Withholding Tax at Source
Attachment to 1702Q (and 2550Q if applicable). Filed as *recipient* of income on which tenants withheld EWT.

Format: DAT file via BIR Alphalist Data Entry module.

Per-entry fields (per RR 2-2006):
1. TIN + branch code of withholding agent (the corporate tenant who issued 2307)
2. Registered name of withholding agent
3. Tax type
4. Period covered
5. Nature of income payment (rental)
6. ATC: WC160
7. Tax base (gross rent)
8. Applicable rate (5%)
9. Amount of tax withheld
10. Total income payment

**Mismatch risk**: 2307 amounts must exactly match amounts on the tenant's QAP. BIR will reject the tax credit claim on mismatch.

---

## 3. Annual Data Package

### BIR Annual Filings

#### BIR Form 1604-E — Annual Information Return of EWT
*Deadline: March 1 of following year*
*Filed as withholding agent for EWT paid to suppliers*

Required:
- Schedule 4: Alphalist of all EWT-subject payees (full year, all suppliers)
- Schedule 3: Alphalist of payees exempt from withholding but subject to income tax
- All 12 monthly 0619-E + 4 quarterly 1601-EQ remittance confirmations
- Alphalist in DAT format via eFPS or esubmission@bir.gov.ph
- Per-payee: TIN, registered name, address, ATC, total income payment, total EWT remitted, references to 2307s issued

#### BIR Form 1702 — Annual Corporate Income Tax Return
*Deadline: April 15 (15th day of 4th month after fiscal year-end)*

Supporting data:
- Full year rent roll summary by tenant
- Complete expense ledger with substantiation
- Depreciation schedule (building, improvements, equipment)
- Bank interest earned
- Gain/loss on asset disposals (if any)
- SAWT for Q4 + annual SAWT compilation
- All 2307 certificates received for the year (sum = EWT tax credit on annual ITR)
- Carry-forward MCIT credits (if applicable)
- RPT official receipts

#### BIR Form 2000 — Documentary Stamp Tax
*Filed within 5 days after month-end when lease contracts are executed*
*Section 194, NIRC*

Per new lease: executed contract + annual rent + term → DST computation:
- PHP 3.00 for first PHP 2,000 of annual rent
- PHP 1.00 per additional PHP 1,000 of annual rent
- Multiply by years of term

Example: PHP 30,000/mo × 12 = PHP 360,000/yr, 1-year lease
DST = PHP 3 + ((360,000 − 2,000) / 1,000 × 1) = PHP 3 + PHP 358 = **PHP 361**

Renewals and extensions each trigger new DST.

#### Lessee Information Statement (LIS)
*Deadlines: January 31 (as of Dec 31) and July 31 (as of Jun 30)*
*Anchored in RMC 69-2009 and RR 12-2011*

Submitted in Excel to RDO. Columns (per RR 12-2011):
- Floor/Unit Number
- Name of Tenant
- Total Leased Area (sqm)
- Monthly Rental
- Start of Lease
- Duration/Period of Lease
- TIN
- Authority to Print number for Invoices/ORs
- POS/CRM Permit (where applicable)

### SEC Annual Filings

#### General Information Sheet (GIS)
*Deadline: 30 calendar days from date of actual annual stockholders' meeting*
*Filed via SEC eFAST*

Property manager provides:
- Date of annual stockholders' meeting
- Updated stockholder list: full name, TIN, nationality, shares, % ownership
- Directors and officers list: name, TIN, nationality, address, position
- Beneficial ownership: natural person owning 25%+ of voting shares
- Corporate Secretary prepares and certifies; notarization required

#### Audited Financial Statements (AFS)
*Deadline: 120 calendar days from fiscal year-end (April 30 for calendar-year corps)*
*Filed via SEC eFAST; must also be BIR-stamped*

External CPA audits and prepares. Property manager/management provides:

**Financial statements data:**
- Income Statement: Rental income (commercial vs. residential), all operating expenses, depreciation, interest, income tax expense
- Balance Sheet: Cash, accounts receivable (outstanding rents), security deposits held, PP&E (land, buildings, improvements, furniture, equipment), accumulated depreciation, payables, accrued expenses, income tax payable, security deposits liability, long-term loans
- Cash Flow Statement: Operating, investing, financing
- Statement of Changes in Equity

**Notes and schedules:**
- Fixed asset schedule: beginning balance, additions, disposals, depreciation, accumulated depreciation, NBV — per asset
- All active lease contracts (for disclosure)
- Loan agreements and amortization schedules
- RPT assessments and official receipts
- Insurance policies
- Security deposit register (received per tenant, returned)
- Aging of receivables (outstanding rent as of year-end)
- Related party transaction details
- Board resolutions authorizing significant transactions

**Financial soundness indicators** (required per SEC): liquidity ratios, D/E, asset-to-equity, interest coverage, profitability — computed by CPA from trial balance.

**Threshold**: AFS must be audited by independent CPA if total assets or liabilities ≥ PHP 600,000 (all operating rental corporations will meet this threshold).

---

## 4. Rent Roll Column Specification

| Column | Notes |
|--------|-------|
| Unit Number / Floor-Unit Reference | Per LIS (RR 12-2011) |
| Unit Type | Commercial / Residential |
| Tenant Name (Registered Business Name or Full Legal Name) | Per LIS and 2307 matching |
| Tenant TIN | Required for LIS and SAWT reconciliation |
| Lease Start Date | Per LIS |
| Lease End Date / Duration | Per LIS and DST computation |
| Total Leased Area (sqm) | Per LIS |
| Contractual Monthly Rent (Base, excl. VAT) | Base rent excluding VAT |
| CUSA / Association Dues (if billed separately) | May have separate VAT treatment |
| Other Charges (parking, utility pass-through) | For invoice completeness |
| VAT Status | VAT-able / VAT-exempt (residential ≤ PHP 15k/mo) |
| VAT Amount (12% if applicable) | Output VAT for 2550Q |
| Total Amount Billed (VAT-inclusive) | For invoice |
| Invoice Number Issued | Sequential; tied to invoice log |
| Invoice Date | |
| Amount Collected this Month | Actual cash received |
| Date Collected | |
| Mode of Payment | Cash / Check / Bank transfer |
| Check Number / Reference | For bank reconciliation |
| Outstanding Balance (prior + billed − collected) | Aging receivable |
| Security Deposit Held | For balance sheet notes |
| 2307 Received (Yes/No) | Corporate tenants only |
| 2307 Quarter Covered | |
| Amount per 2307 | EWT tax credit |
| Authority to Print (ATP) Number | Per RR 12-2011 LIS |
| POS/CRM Permit | Per RR 12-2011 LIS |
| Remarks | Vacancies, holdovers, disputes |

---

## 5. Form 2307 Tracking Workflow

### Who Issues 2307
Any corporate or business tenant who is a registered withholding agent: withholds 5% EWT (ATC: WC160) from each rental payment and issues 2307 to the landlord within 20 days after each quarter-end.

### 2307 Certificate Fields
- Payor (tenant) TIN and name
- Payee (landlord corporation) TIN and name
- Nature of income: rent
- ATC: WC160
- Quarter covered
- Gross rental payments
- EWT withheld (5%)

### Landlord's Obligations on Receiving 2307
1. Acknowledge receipt to tenant
2. Log in 2307 tracker (part of monthly data package)
3. Deliver originals to accountant quarterly
4. Accountant prepares SAWT for 1702Q attachment; 2307 sum = EWT tax credit

### Timing Summary

| Party | Action | Deadline |
|-------|--------|----------|
| Corporate Tenant | Remit EWT monthly (0619-E) | 10th of following month |
| Corporate Tenant | File 1601-EQ quarterly | Last day of month after quarter |
| Corporate Tenant | Issue 2307 to landlord | Within 20 days after quarter-end |
| Property Manager | Log 2307, deliver to accountant | By 5th of month after quarter-end |
| Accountant | Attach SAWT to 1702Q | With 1702Q (60th day after quarter) |

---

## 6. BIR Form Summary: Client Data Perspective

| BIR Form | Filed As | Frequency | Primary Client Data |
|----------|----------|-----------|---------------------|
| 0619-E | W/H agent | Monthly | EWT withheld on supplier payments; payee TINs, amounts |
| 2550Q | Taxpayer | Quarterly | Output VAT, creditable input VAT, carry-forward |
| 2551Q | Taxpayer | Quarterly (non-VAT only) | Total gross rental receipts |
| 1601-EQ + QAP | W/H agent | Quarterly | All EWT-subject supplier payments; payee data |
| 1702Q + SAWT | Taxpayer | Quarterly | Gross income, deductions, depreciation, 2307s received |
| 2000 | Taxpayer | Per-event (monthly filing) | Executed lease contracts, annual rent, term |
| 1604-E + Alphalist | W/H agent | Annual (March 1) | Full year payee EWT summary; all remittance records |
| 1702 | Taxpayer | Annual (April 15) | Full P&L, balance sheet, full year 2307s, SAWT annual, depreciation |
| LIS | Lessor | Semi-annual (Jan 31, Jul 31) | Rent roll data per RR 12-2011 |

---

## 7. Books of Accounts Requirements

### Legal Basis
NIRC Section 232 (mandatory); BIR RR 9-2009 (electronic records and CAS).

### Mandatory Books for VAT-registered Rental Corporation (minimum 6):
1. General Journal
2. General Ledger
3. Cash Receipts Book
4. Cash Disbursements Book
5. Subsidiary Sales Journal (output VAT tracking)
6. Subsidiary Purchases Journal (input VAT tracking)

### Permissible Formats

**Manual Books**: BIR-stamped at registration, posted within 5 days of transaction. Register with RDO before use.

**Loose-Leaf**: Computer-printed, hardbound and submitted within 15 days of calendar year-end.

**Computerized Accounting System (CAS)**: BIR Permit to Use required. Soft copies submitted by January 30 of following year via ORUS or BIR RDO. Unregistered systems risk expense disallowance on audit.

### Retention
10 years from last entry date.

---

## 8. Invoice / Billing Document Requirements (RR 7-2024)

### Mandatory Fields on a Rental Sales Invoice
1. "VAT-registered" statement and TIN with branch code
2. Total amount due (VAT-inclusive) with VAT as a separate line item
3. Date of transaction
4. Description: nature of rental, property address, period covered
5. Buyer's name, address, TIN (if invoice ≥ PHP 1,000 and buyer is VAT-registered)
6. Sequential unique invoice number (gapless)
7. "VAT-exempt sale" notation for qualifying residential units
8. ATP or CAS Permit number

### Sample VAT Breakdown

Commercial unit:
```
Monthly Rent (excl. VAT):   PHP 25,000.00
VAT (12%):                  PHP  3,000.00
Total Amount Due:           PHP 28,000.00
```

VAT-exempt residential unit (≤ PHP 15,000/mo):
```
Monthly Rent:               PHP 12,000.00
VAT-EXEMPT SALE
Total Amount Due:           PHP 12,000.00
```

---

## Key Regulatory Citations

| Regulation | Subject |
|-----------|---------|
| RR 12-2011 | Lessee Information Statement — format, columns, deadlines |
| RMC 69-2009 | Original LIS requirement |
| RR 9-2009 | Books of accounts — electronic records and CAS requirements |
| RR 2-2006 | SAWT and MAP as mandatory attachments |
| RR 7-2024 | Invoicing reform — VAT Invoice as primary document (eff. April 27, 2024) |
| RR 11-2024 | Transitional provisions for unused Official Receipts |
| Section 194, NIRC | DST on lease contracts |
| Section 232, NIRC | Books of accounts and CPA audit requirement above PHP 3M gross |
| RA 11232 | GIS filing obligation (Revised Corporation Code) |
| SEC MC 01-2025 | AFS and GIS filing schedule for FY2024 |

---

## Key Automation Opportunities Identified

1. **Rent roll generation**: If payment tracking is automated, the rent roll is a report — not manual work
2. **Invoice log**: Sequential auto-numbering, VAT computation, per-tenant invoice generation
3. **2307 tracker**: Digital log with quarterly status tracking per corporate tenant
4. **SAWT data preparation**: Structured 2307 data → DAT file generation
5. **DST computation**: Deterministic formula; triggered on contract execution
6. **LIS semi-annual report**: Subset of rent roll data in required Excel format
7. **Expense voucher log**: Structured input → accountant-ready export
8. **Fixed asset register**: Track additions, disposals, compute depreciation
