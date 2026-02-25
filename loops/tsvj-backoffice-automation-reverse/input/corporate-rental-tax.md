# Corporate Rental Tax Rules — SEC-Registered PH Lessor Corporation

*Fetched and processed: 2026-02-25*
*Applies to: Domestic SEC-registered corporation, Las Piñas commercial + residential properties*
*Legal basis updated through: CREATE Act (RA 11534, 2021), TRAIN (RA 10963, 2018), and subsequent RRs*

---

## 1. Regular Corporate Income Tax (RCIT) and MCIT

### RCIT

**Legal basis:** NIRC Section 27(A); RA 11534 (CREATE Act, 2021)

**Rate:** 25% of net taxable income (permanently reduced from 30% by CREATE Act, effective July 1, 2020).

**20% reduced rate** applies if BOTH:
- Net taxable income ≤ PHP 5,000,000, AND
- Total assets (excluding land where the business is situated) ≤ PHP 100,000,000

A rental corporation holding Las Piñas real estate should assess asset values annually to determine which rate applies. The 20% rate is available only to genuinely small entities.

**Formula:**
```
RCIT = Net Taxable Income × 25% (or 20% for qualifying SMEs)
Net Taxable Income = Gross Income − Allowable Deductions
Gross Income = Gross Rental Receipts + Other Income
```

**Deduction method options:**
- Itemized deductions (actual expenses with receipts)
- Optional Standard Deduction (OSD): 40% of gross income (NIRC Section 34(L))

### MCIT (Minimum Corporate Income Tax)

**Legal basis:** NIRC Section 27(E); RR No. 9-98, amended by RR No. 12-2007

**Rate:** 2% of gross income (reverted from CREATE Act temporary 1% rate after June 30, 2023)

**When MCIT applies:** Beginning the **4th taxable year** from commencement of operations. Each year thereafter, pay whichever is higher: RCIT or MCIT.

**Gross income for MCIT:** Total gross rental receipts + other income subject to normal tax. For a pure rental corporation, this effectively equals total gross rentals (no COGS deduction).

**RCIT vs. MCIT comparison:**

| Scenario | Gross Rentals | Deductions | Net Taxable Income | RCIT (25%) | MCIT (2%) | Tax Due |
|---|---|---|---|---|---|---|
| Profitable year | PHP 10M | PHP 7M | PHP 3M | PHP 750,000 | PHP 200,000 | PHP 750,000 (RCIT) |
| Low-profit year | PHP 10M | PHP 9.8M | PHP 200,000 | PHP 50,000 | PHP 200,000 | PHP 200,000 (MCIT) |

**Carry-forward:** Excess MCIT over RCIT may be carried forward as credit against RCIT for the next 3 taxable years (cannot offset future MCIT).

**BIR Form:** 1702Q (quarterly, first 3 quarters only) / 1702-RT (annual)

**Deadlines (calendar year corporation):**
- Q1: May 15
- Q2: August 15
- Q3: November 15
- Annual (1702-RT): April 15

---

## 2. Value Added Tax (VAT)

**Legal basis:** NIRC Section 108 (VAT on lease of properties); Section 109(1)(V) (residential exemption); Section 236(G) (mandatory registration); RR No. 16-2005 (consolidated VAT regs); RR No. 13-2018 (TRAIN implementing rules for mixed lessors)

### Rate and Threshold

**Rate:** 12% of gross rental receipts.

**Mandatory registration threshold:** PHP 3,000,000 in gross sales/receipts in any 12-month period (Section 236(G)). Must register within 30 days of the month the threshold is exceeded.

### Computing Output VAT

```
Output VAT = Gross Rental Receipts × 12%
VAT Payable = Output VAT − Allowable Input VAT
```

**Invoice breakdown example** (monthly rent PHP 100,000 base):
- Rental base: PHP 100,000
- VAT (12%): PHP 12,000
- Total billed to tenant: PHP 112,000
- EWT withheld by lessee (5% of PHP 100,000): PHP 5,000
- Net cash received by lessor: PHP 107,000

### VAT on Deposits and Advance Rent

- **Security deposits (refundable):** NOT subject to VAT upon receipt. Treated as a liability. Becomes subject to VAT (and income) **only upon forfeiture or application to unpaid rent** — issue VAT OR at that point.
- **Advance rent (non-refundable / earmarked for last month):** Subject to VAT upon receipt. Issue VAT OR immediately.

### BIR Forms

- **2550Q** — Quarterly VAT Return. Due **25th day after close of each taxable quarter**.
- **2550M** — Monthly VAT Return. As of RMC No. 52-2023, quarterly-only filing (2550Q) is now standard. 2550M is no longer required for most taxpayers.

### Optional VAT Registration

Lessor below PHP 3M threshold may voluntarily register for VAT (NIRC Section 236(H)). Irrevocable for **3 years** after election (RR No. 9-2011). Beneficial if significant input VAT from renovation/construction.

---

## 3. Percentage Tax (OPT — Other Percentage Tax)

**Legal basis:** NIRC Section 116; CREATE Act Section 4 (temporary reduction); RR No. 4-2021

**Rate:** 3% of gross quarterly receipts (reverted to 3% from CREATE Act temporary 1% after June 30, 2023).

**Who is covered:** Non-VAT-registered lessors with annual gross receipts **≤ PHP 3,000,000**.

**Formula:**
```
OPT Payable = Gross Quarterly Receipts × 3%
```

OPT is NOT passed on to tenants — the lessor absorbs it directly.

**BIR Form:** 2551Q — Quarterly Percentage Tax Return

**Deadlines (calendar year):**
- Q1 (Jan-Mar): April 25
- Q2 (Apr-Jun): July 25
- Q3 (Jul-Sep): October 25
- Q4 (Oct-Dec): January 25 (following year)

---

## 4. Expanded Withholding Tax (EWT) — The Lessor Receives Form 2307

**Legal basis:** NIRC Section 57; RR No. 2-98, Section 2.57.2(B), amended by RR No. 11-2018

### Overview

EWT on rent is imposed on the **lessee** (the withholding agent). The lessee withholds 5% and remits to BIR. From the lessor's perspective, EWT is a creditable prepayment of income tax.

**Rate:** 5% of gross rental EXCLUDING VAT (if VAT is separately stated on invoice).

**ATC Codes:**
- WR010: Rentals paid to individual lessors
- WR020: Rentals paid to corporate/non-individual lessors ← applicable here

### Who Must Withhold

Corporate lessees, partnerships, government agencies, PEZA-registered firms. Individual lessees renting for purely personal purposes are NOT withholding agents.

### EWT on Deposits / Advance Rent

- **Security deposits:** NOT subject to EWT at receipt. EWT applies when deposit is applied to rent or forfeited.
- **Advance rent:** Subject to 5% EWT at the time of payment, including advances covering periods beyond 12 months.

### Lessee's Compliance Timeline (affects what 2307s the lessor can expect to receive)

| BIR Form | Purpose | Deadline |
|---|---|---|
| 0619-E | Monthly EWT remittance (non-quarter-end months) | 15th day following month (eFPS) |
| 1601-EQ | Quarterly EWT Return + QAP | Last day of month following quarter close |
| 1604-E | Annual EWT Information Return | March 1 (or last day of February) |
| 2307 | Certificate of Creditable Tax Withheld (issued to lessor) | Within 20 days after close of taxable quarter |

### How the Lessor Claims the Credit

The lessor collects Form 2307 from each withholding lessee. Two conditions to claim the credit (RR 2-98, Section 2.58.3):
1. Rental income must be declared as gross income in the ITR.
2. Fact of withholding established by original Form 2307.

```
Income Tax Due = RCIT or MCIT (whichever is higher)
Less: EWT Credits (Form 2307s received from lessees)
Less: Quarterly income tax payments already made
= Balance due (or overpayment)
```

**MCIT + CWT interaction:** Per RR No. 12-2007, when MCIT > RCIT, only current-year EWT, current-year quarterly payments, and prior-year excess EWT can offset MCIT. Excess MCIT from prior years offsets future RCIT only, not future MCIT.

---

## 5. Documentary Stamp Tax (DST) on Lease Contracts

**Legal basis:** NIRC Section 194 (Stamp Tax on Leases); Section 173 (liability); Section 201 (inadmissibility of unstamped documents)

### Rate (NIRC Section 194)

- **PHP 3.00** for the first PHP 2,000 (or fractional part) of the **annual rent**
- **PHP 1.00** for every PHP 1,000 (or fractional part) in excess of PHP 2,000

**Computation is PER YEAR of the lease term.** A 3-year lease computes DST three times.

**Formula:**
```
DST per year = PHP 3.00 + ⌈(Annual Rent − PHP 2,000) / PHP 1,000⌉ × PHP 1.00
Total DST = DST per year × Number of years of term
```

**Example — Monthly rent PHP 50,000 (Annual rent = PHP 600,000), 3-year lease:**
- First PHP 2,000: PHP 3.00
- Remaining PHP 598,000 ÷ PHP 1,000 = 598 units × PHP 1.00 = PHP 598.00
- DST per year = PHP 601.00
- Total DST for 3-year lease = PHP **1,803.00**

> **Note on rate variants:** Some older BIR references cite PHP 15 / PHP 3 per PHP 2,000 / PHP 1,000. The NIRC Section 194 text as published states PHP 3 / PHP 1. Verify with the applicable RDO upon execution — TRAIN or subsequent legislation may have amended specific DST amounts.

### BIR Form

**BIR Form 2000** — Documentary Stamp Tax Declaration Return.

### Filing Deadline

**Within 5 days after the close of the month** in which the lease was made, signed, issued, accepted, or transferred.
- Example: Contract executed March 15 → DST due by **April 5**

### Who Pays

NIRC Section 173: The party making, signing, issuing, accepting, or transferring the document. In practice, typically the **lessor** (who prepares the contract). Parties may agree to split, but both remain jointly exposed to BIR assessment.

### Renewals

Lease renewals are treated as **new contracts** — subject to new DST computation based on the renewed annual rent for each year of the renewed term. No exemption for renewals.

### Penalties

Unstamped document is **inadmissible as evidence in court** until DST + 25% surcharge paid (Section 201). Additional: 25% surcharge + 12% annual interest + compromise penalties.

---

## 6. Mixed-Use Lessors: VAT vs. OPT Determination (Commercial + Residential)

**Legal basis:** RR No. 13-2018 (TRAIN Law implementing rules); NIRC Section 109(1)(V) (residential exemption at PHP 15,000)

### The Four Scenarios Under RR 13-2018

| Scenario | Unit Type | Rent/Unit/Month | Combined Receipts | Tax Treatment |
|---|---|---|---|---|
| A | Pure residential | ≤ PHP 15,000 | Any | **Exempt from VAT and OPT** |
| B | Pure residential | > PHP 15,000 | ≤ PHP 3M | **3% OPT** (not VAT) |
| C | Mixed: commercial + residential (resi ≤ PHP 15K) | Commercial: any; Resi: ≤ PHP 15K | Commercial > PHP 3M | Commercial: **12% VAT**; Residential: **Exempt** (carved out) |
| D | Mixed: commercial + residential (resi > PHP 15K) | Both commercial and resi > PHP 15K | Combined > PHP 3M | **Both streams: 12% VAT** ← the "trap" |

### Practical Implication for Las Piñas Lessor

**If residential rents are PHP 15,000 or below/unit:** Those units are carved out entirely. Do not count toward VAT threshold. Commercial units assessed separately on their own receipts.

**If ANY residential rents exceed PHP 15,000/unit:** Combined receipts (commercial + residential) are measured against the PHP 3,000,000 threshold. If combined > PHP 3M, ALL receipts (both commercial and residential) become VAT-able at 12%.

**Threshold timing:** The PHP 3M threshold is computed on receipts in any **preceding 12-month period**, not just the calendar year. Cross the threshold mid-year → mandatory VAT registration within 30 days from close of that month.

---

## 7. Official Receipts (OR) Requirements

**Legal basis:** NIRC Section 237; RR No. 18-2012 (ATP rules); RR No. 6-2022 (ATP validity); RR No. 8-2022 (EIS mandate); RA 11976 (EOPT Act, 2024)

### Authority to Print (ATP)

Before printing ORs, file **BIR Form 1906** at the jurisdiction RDO (Las Piñas: Revenue Region No. 8). Only **BIR-accredited printers** may print ORs.

**ATP validity:** 3 years from issuance or until all serial numbers exhausted (whichever comes first). Renewal via ORUS portal, at least 60 days before expiry.

### Required Fields on Every OR

1. Lessor-corporation name and business style
2. Registered address
3. TIN
4. BIR VAT number (if VAT-registered)
5. Date of transaction
6. Serial number (sequential, unique per establishment)
7. ATP number and approved series range
8. Client/tenant name and address
9. Description: "Monthly Rental — Unit ___ for the period ___"
10. Amount breakdown (base + VAT if applicable)
11. If non-VAT: "THIS DOCUMENT IS NOT VALID FOR CLAIM OF INPUT TAX" (prominently displayed)
12. Printer's name, address, TIN, accreditation number

### Sequential Numbering

Each establishment maintains its own independent series (head office: "000"; branches: "001", "002", etc.). Gaps or duplications create audit risk.

### When to Issue an OR (Rental Corporation)

- On receipt of each monthly rental payment
- On receipt of advance rent (entire advance amount triggers OR)
- On application of security deposit to unpaid rent (becomes income)
- On forfeiture of a security deposit

### E-Receipts (EIS) Status as of 2026

- Mandatory EIS participation for: Large Taxpayers, exporters, e-commerce businesses
- **For typical mid-size rental corporation in Las Piñas:** Not yet mandatory as of early 2026. Extended deadline: **December 31, 2026** (per RR 026-2025)
- Voluntary enrollment available via ORUS portal
- E-ORs satisfy Section 237 if: tenant can download/print human-readable copy AND XML acknowledged by EIS (Acknowledgement Reference Number)

### Penalties for Non-Compliance

| Violation | Penalty |
|---|---|
| ORs without BIR ATP | PHP 10,000 (first); PHP 20,000 (subsequent) |
| Double/multiple receipt sets | Non-compoundable; criminal liability |
| Missing required fields | PHP 5,000 (first); PHP 10,000 (subsequent) |
| Failure to issue OR | Compromise penalty + surcharge/interest on unrecorded income; Section 115 closure risk |

---

## 8. Books of Accounts

**Legal basis:** NIRC Section 232; RR No. 17-2013 (retention); RR No. 5-2014 (electronic preservation)

### Mandatory Books (minimum)

1. General Journal
2. General Ledger

### Recommended Subsidiary Books for Rental Corporation

3. Cash Receipts Journal — all cash collected (rents, advances, deposits applied/forfeited)
4. Cash Disbursements Journal — all outflows (maintenance, repairs, taxes)
5. Sales/Rental Journal — rental billings per unit per tenant per period
6. Purchase/Expense Journal — credit purchases for maintenance and operations
7. Subsidiary Ledger — Accounts Receivable (per-tenant aging)
8. Subsidiary Ledger — Security Deposits (per-tenant, as a liability)
9. Fixed Assets Register — real property, improvements, depreciation schedule

### Book Types Permitted

1. Manual (handwritten, BIR-registered bookstore)
2. Loose-leaf (computer-printed; requires Permit-to-Use + annual submission of bound copies)
3. Computerized accounting system (CAS) (requires BIR CAS registration; mandatory for Large Taxpayers)

### CPA Audit Requirement

Annual gross sales/receipts/output exceeding **PHP 3,000,000** → mandatory CPA audit → Audited Financial Statements (AFS) attached to annual 1702-RT by April 15. Aligns with VAT registration threshold.

### Retention Period (RR No. 17-2013)

- **10 years** from the day following the filing deadline of the return for that taxable year
- Years 1–5: Hard copy required (electronic may supplement)
- Years 6–10: Electronic preservation sufficient; hard copies may be discarded

> Critical for rental corporations: BIR can assess up to 10 years from fraud discovery (Section 222, NIRC). Retain all lease contracts, ORs, vouchers, and records through the full period.

---

## 9. BIR Forms Calendar (Calendar-Year Rental Corporation)

### Annual Deadlines Summary

| Form | Description | Deadline |
|---|---|---|
| 1702-RT | Annual Corporate ITR (full year) | April 15 |
| 1604-E | Annual EWT Information Return | March 1 (or Feb 28) |

### Quarterly Deadlines

| Quarter | Period | 1702Q | 2550Q (VAT) | 2551Q (OPT) | 1601-EQ (EWT) |
|---|---|---|---|---|---|
| Q1 | Jan-Mar | May 15 | April 25 | April 25 | April 30 |
| Q2 | Apr-Jun | August 15 | July 25 | July 25 | July 31 |
| Q3 | Jul-Sep | November 15 | October 25 | October 25 | October 31 |
| Q4 | Oct-Dec | *(no 1702Q — covered by annual 1702-RT)* | January 25 | January 25 | January 31 |

### DST (Ad Hoc per Contract)

**BIR Form 2000** — Within 5 days after close of the month in which the lease was executed.

### 2307 Certificates

The lessor receives 2307 from each corporate lessee within 20 days after each quarter close. Lessor attaches originals to 1702Q and 1702-RT.

---

## 10. Quick Reference: Tax Type Selector for Rental Corp

| Question | Answer | Tax/Action |
|---|---|---|
| Are gross annual receipts > PHP 3M? | Yes | Register for VAT; charge 12% on billings |
| Are gross annual receipts > PHP 3M? | No | Pay 3% OPT quarterly (2551Q) |
| Is at least one residential unit's monthly rent > PHP 15K? | No | Those residential units are exempt entirely |
| Is at least one residential unit's monthly rent > PHP 15K AND combined receipts > PHP 3M? | Yes | ALL receipts (commercial + residential) are VAT-able |
| Is the corporation in its 4th+ operating year? | Yes | Compute MCIT (2%) and compare to RCIT (25%); pay higher |
| Is a new or renewed lease being executed? | Yes | Compute DST; file Form 2000 within 5 days of month-end |
| Does a corporate tenant pay rent? | Yes | Expect 5% EWT withheld; collect Form 2307 each quarter |

---

## Key Sources

- NIRC Sections: 27(A), 27(E), 57, 108, 109(1)(V), 116, 173, 194, 201, 232, 236(G/H), 237
- RA 11534 (CREATE Act, 2021)
- RA 10963 (TRAIN Law, 2018)
- RA 11976 (Ease of Paying Taxes Act / EOPT, 2024)
- RR No. 2-98 (EWT); RR No. 9-98 (MCIT); RR No. 16-2005 (VAT); RR No. 13-2018 (TRAIN VAT for lessors); RR No. 17-2013 (records retention); RR No. 18-2012 (ATP); RR No. 6-2022 (ATP validity); RR No. 8-2022 (EIS); RR 026-2025 (EIS extended deadline)
- RMC No. 52-2023 (quarterly VAT filing as standard)
- taxacctgcenter.ph; respicio.ph; cloudcfo.ph; taxsummaries.pwc.com/philippines
