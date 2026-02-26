# Practitioner Workflow — Manual/Excel Processes for PH Real Estate Transaction Taxes

**Wave:** 3 — Competitive & Automation Gap Analysis
**Date:** 2026-02-26
**Sources:** PwC PH, Grant Thornton PH, Forvis Mazars PH, BIR official issuances (RMO 12-2025, RMC 56-2024, RMC 83-2024), Respicio & Co., AJA Law, ForeclosurePhilippines.com, KeyRealty, FiledocsPhil, practitioner guides, BIR eONETT User Guide, CREBA
**Method:** Web research synthesis of practitioner-facing guides, BIR official documentation, and real estate industry commentary

---

## Overview

This analysis documents the **current manual/Excel workflow** that Philippine real estate tax practitioners follow for transaction taxes (CGT, DST, CWT, VAT). The focus is on the process, not the formulas — what practitioners actually do day-to-day, where time goes, what tools they use, and where the friction lives.

The end-to-end workflow spans four government agencies (BIR, LGU Treasurer, LGU Assessor, Registry of Deeds), involves 10-20+ physical documents per transaction, and takes 2-8 weeks in the common case. No single system covers the full pipeline. The practitioner is the integration layer.

---

## 1. End-to-End ONETT Workflow: Transaction Tax Payment to eCAR

### What "ONETT" Actually Means in Practice

ONETT (One-Time Transaction) is the BIR's processing pipeline for transaction-based taxes on property transfers. Despite the name, it is not one step — it is a multi-week, multi-visit process involving document gathering, tax computation, payment, verification, and certificate issuance.

### Step-by-Step Process (Sale of Real Property)

#### Phase 1: Pre-Filing Document Assembly (1-5 days, practitioner labor)

The practitioner (usually a broker, accountant, or hired "processor") gathers:

| # | Document | Source | Pain Point |
|---|----------|--------|------------|
| 1 | Notarized Deed of Absolute Sale (DOAS) | Notary public | Must be signed and notarized before any tax filing can begin. 1 original + 2 photocopies required. |
| 2 | Certified True Copy of TCT/CCT/OCT | Registry of Deeds | Requires in-person visit to RD; wait times vary by office (hours to days). |
| 3 | Certified True Copy of Tax Declaration (land + improvement) | Local Assessor's Office | Must be "at the time of or nearest to the date of transaction." Another in-person visit. |
| 4 | TIN of Seller(s) and Buyer(s) | BIR / TIN Verification Slip | If either party lacks a TIN, must apply via BIR Form 1904 (manual) or ORUS (online). Duplicate TINs or mismatched names cause delays. |
| 5 | Valid government IDs | Seller and Buyer | Name must match deed, title, and TIN exactly. Even minor discrepancies (middle name, suffix, married name) stall processing. |
| 6 | Location Plan / Vicinity Map | Geodetic engineer or LGU | Required if Tax Declaration does not clearly locate the property for zonal value determination. |
| 7 | Special Power of Attorney (if representative) | Notary public | Must be notarized; if executed abroad, must have Apostille or Philippine Consulate certification. |
| 8 | RPT clearance | LGU Treasurer | Proves real property taxes are current. Another in-person visit. Arrears must be settled first. |

**Key friction:** These documents come from 4+ different offices, each with their own queues and operating hours. Serial processing is the norm — the practitioner visits each office sequentially, not in parallel, because each subsequent office may need outputs from a prior one.

#### Phase 2: Tax Computation (BIR ONETT Desk or eONETT System)

Two paths exist:

**Path A — Walk-in (still common, especially outside Metro Manila):**
1. Practitioner brings complete document folder to RDO having jurisdiction over the property location (per RMC 56-2024).
2. Officer-of-the-Day verifies documents against the Checklist of Documentary Requirements (CDR, Annexes D-1 through D-10).
3. If complete: CDR status set to "CDR COMPLETE" in ONETT Tracking System (OTS). CDR signed by Revenue Officer or Group Supervisor and by the taxpayer/representative.
4. If incomplete: Status set to "PENDING FOR SUBMISSION OF REQUIREMENTS" — practitioner must return with missing docs.
5. ONETT team prepares the **ONETT Computation Sheet (OCS)** — the official tax computation document. Different annexes for different transaction types:
   - Annex B: CGT + DST (capital asset sale)
   - Annex B-4: CWT/EWT + DST (ordinary asset sale)
   - Annex B-2: Estate tax
6. OCS reviewed and approved by Head ONETT Team, then Group Supervisor, then RDO/ARDO/CAS (approval chain per RMO 12-2025).
7. Approved OCS released to taxpayer.

**Path B — eONETT (online, launched 2023, per RMC 56-2023):**
1. Create account at eonett.bir.gov.ph using valid email + 12-digit password.
2. Select transaction type: "+ New CGT & DST Application" (capital asset) or "+ New EWT or DST Application" (ordinary asset).
3. Fill in form fields: seller/buyer details, property description, transaction details, selling price, zonal value, FMV.
4. Upload scanned copies of all documents (DOAS, TCT, Tax Declaration, IDs, etc.).
5. Click "Submit Application" — system assigns transaction number, transmits to RDO.
6. Application evaluated by Revenue Officer, then Group Supervisor, then RDO/ARDO/CAS.
7. Status updates: "Pending" (awaiting approval) or "For Payment" (OCS approved).
8. Pop-up notification when OCS approved.

**Critical note on eONETT:** The computation is NOT self-service. The taxpayer enters data, but the BIR officer computes and approves the OCS. The system is a digitized submission channel, not a computation engine. The practitioner still needs to know what the correct tax should be (to verify the OCS), and the BIR officer still manually reviews and approves.

#### Phase 3: Tax Payment (1-3 days)

1. Based on approved OCS, practitioner fills out:
   - BIR Form 1706 (CGT) or BIR Form 1606 (CWT on real property)
   - BIR Form 2000-OT (DST, one-time transaction)
2. Payment made at Authorized Agent Bank (AAB), Revenue Collection Officer (RCO), or via ePayment channels (GCash, BPI, UnionBank, LANDBANK Link.Biz, etc.).
3. P50 convenience fee for eONETT transactions.
4. **Important per RMC 83-2024:** Tax returns generated from eONETT do NOT need a "TIN Verified" stamp from the RDO before payment at AABs — this was a friction point that had been causing unnecessary trips back to the RDO.

**Timing constraint:** CGT must be paid within 30 days of notarization. DST within 5 days after end of the month of signing. Late filing triggers 25% surcharge + 12% annual interest + compromise penalties.

**Lumping prohibition:** BIR prohibits "lumping" multiple real estate CWT transactions into a single return. Each property sale requires its own separate Form 1606 filing. This is a major burden for developers with hundreds of units.

#### Phase 4: Payment Verification (1-3 working days per RMO 12-2025)

1. Practitioner submits proof of payment (bank-validated return, deposit slip, ePayment confirmation) to RDO.
2. ONETT Payment Verifier (OPV) verifies payment against BIR internal systems.
3. Per RMO 12-2025: Verification must happen within 3 working days of receipt of proof.
4. In practice: Delays if payment was made at an AAB outside the RDO's jurisdiction (a confusion point created by the Ease of Paying Taxes Act, which allowed filing/payment anywhere, but eCAR processing still requires the RDO with jurisdiction over the property location).

#### Phase 5: eCAR Generation and Release (target: 7 working days per RMO 12-2025)

1. After payment verification, ONETT Encoder enters case data into eCAR system.
2. eCAR generated, printed on security paper.
3. Signed by RDO or ARDO (or CAS if both absent).
4. Claim slip issued.
5. To claim eCAR: Practitioner presents physical copies of all documents + downloaded BIR forms + claim slip. Documents must match those uploaded in eONETT.
6. Taxpayer completes ONETT Customer Satisfaction Survey Form (CSSF).
7. eCAR released.

**Per RMO 12-2025 processing targets:**

| Transaction Classification | OCS Processing | eCAR Processing |
|---|---|---|
| **Simple** (1-3 properties, no inspection) | Same-day to 3 working days | 7 working days |
| **Complex** (>3 properties or inspection needed) | 7 working days | 7 working days |
| **Highly Technical** (estate tax only) | 20 working days | 7 working days |

**Performance targets (RMO 12-2025):**
- 75% of OCS approvals within prescribed timeframes
- 75% of eCAR approvals within 7 working days
- 75% of payment verifications within 3 working days
- 80% minimum customer satisfaction rating

**Reality vs. target:** Practitioners report 5-15 working days for simple sales, 15-30 days for donations, 3-6+ weeks for estates or complex cases. Backlogs, valuation disputes, staff shortages, and document deficiencies extend timelines far beyond the Citizen's Charter standards.

#### Phase 6: Post-BIR Processing (separate from ONETT)

After eCAR, the practitioner must still:
1. Pay Local Transfer Tax at LGU Treasurer's Office (0.5-0.75%)
2. Register at Registry of Deeds (separate fee schedule)
3. Get new Tax Declaration at Local Assessor's Office
4. Get new title (TCT/CCT) from Registry of Deeds

Each step is a separate visit, separate queue, separate set of documents. Total end-to-end from deed signing to new title: typically 4-12 weeks.

---

## 2. Excel/Spreadsheet Usage in Tax Computation

### How Practitioners Currently Compute Taxes

There is **no standard industry Excel template** that all practitioners use. Instead, the landscape is fragmented:

#### A. The BIR's Own "Template": ONETT Computation Sheet (OCS)

- The official form is a **PDF** (Annex B series from RMO 15-03), not an Excel workbook.
- Available from lawphil.net, BIR website, and third-party fillable form platforms (pdfFiller, DocHub, airSlate SignNow).
- US Legal Forms advertises an "ONETT Computation Sheet Excel" fillable version — these are third-party digitizations of the official PDF, not BIR-issued.
- The OCS is filled out by BIR ONETT officers, not by the taxpayer — though practitioners pre-compute to verify.

#### B. Practitioner-Built Excel Spreadsheets

Practitioners (brokers, accountants, tax agents) typically build their own Excel templates:

**Common template structure:**
1. **Input cells:** Selling price, zonal value (looked up separately), assessed FMV (from Tax Declaration), land area in sqm, property classification
2. **Tax base determination:** `=MAX(selling_price, zonal_value, assessed_fmv)` — the "highest-of-three" logic
3. **CGT computation:** `=tax_base * 6%`
4. **DST computation:** `=tax_base * 1.5%`
5. **CWT computation:** `=tax_base * rate` (where rate is manually selected from 1.5-6% based on seller type and price bracket)
6. **Penalty calculator:** Surcharge (25%) + interest (12% p.a. prorated) if filing is late
7. **Summary sheet:** Total taxes due, payment deadlines, responsible party (buyer vs. seller)

**Manual data entry involved:**
- Selling price: typed in from the Deed of Sale
- Zonal value: looked up separately (see Section 4), manually entered
- Assessed FMV: copied from the Tax Declaration
- Property details: manually transcribed from TCT
- Dates: manually entered to compute deadlines and penalty periods

**No integration** with BIR systems, zonal value databases, or document management. Each transaction starts from a blank template or a copied previous computation.

#### C. Online Calculators

- **Housal.com** offers a public real estate closing costs calculator (CGT, VAT, DST, transfer tax, registration fees, broker commission) — web-based, free, but limited to simple scenarios.
- **ForeclosurePhilippines.com** provides worked examples and tutorials, not interactive calculators.
- **TaxCalculatorPhilippines.online** offers RPT computation.
- None of these handle the full ONETT workflow, installment VAT schedules, or multi-property transactions.

#### D. What Developers Use

Large real estate developers (Ayala Land, SMDC, Megaworld, etc.) typically use:
- **ERP systems:** SAP (via Fasttrack Solutions PH), Oracle NetSuite, In4Suite (India-based, PH presence)
- **PH-specific platforms:** NOAH Business Applications ("only end-to-end property management system in the Philippines"), iRealtee, Jinisys Software, Centra REMS (Focus Softnet)
- **Accounting software:** QuickBooks Philippines (VAT tracking), Xero (via JuanTax integration)

However, even developers with ERPs often have a **separate Excel layer** for:
- Pre-computation of taxes before submitting to BIR
- Reconciliation of BIR Form 2307 certificates
- Tracking of CWT remittances per unit (since lumping is prohibited)
- Installment VAT schedule tracking per buyer

Small-to-mid developers and individual practitioners overwhelmingly rely on Excel.

---

## 3. BIR eONETT System — User Experience Details

### What eONETT Actually Is

Launched in 2023 (RMC 56-2023), eONETT is a **web-based submission portal** that digitizes the document submission and status tracking portions of the ONETT workflow. It is NOT a computation engine — the BIR officer still computes and approves the OCS.

### User Experience Walkthrough

1. **Account creation:** Email-based registration at eonett.bir.gov.ph. Password is 12 digits.
2. **Home screen:** Two buttons — "+ New CGT & DST Application" (capital asset) and "+ New EWT or DST Application" (ordinary asset).
3. **Application form:** Multi-step form requiring:
   - Seller/buyer information (TIN, name, address)
   - Property details (location, area, classification, TCT/CCT number)
   - Transaction details (selling price, date of deed, notarization date)
   - Tax amounts (the practitioner must still pre-compute these)
4. **Document upload:** Scanned copies of all CDR documents (DOAS, TCT, Tax Declaration, IDs, SPA, etc.)
5. **Submission:** System assigns transaction number, transmits to jurisdictional RDO.
6. **Status tracking:** "Pending" → "For Payment" (OCS approved) → "For Verification" → "For Release"
7. **Payment:** Download BIR forms from eONETT, pay at AAB/ePayment, upload proof of payment.
8. **Claim:** In-person at RDO with physical documents + claim slip. Must match uploaded documents exactly.

### What Is Self-Service vs. Officer-Mediated

| Step | Self-Service? | Notes |
|------|---------------|-------|
| Account creation | Yes | Email-based |
| Application form filling | Yes | Practitioner enters data |
| Document upload | Yes | Scanned copies |
| Tax computation (OCS) | **No — BIR officer** | Officer computes and approves |
| OCS approval | **No — BIR officer chain** | RO → GS → RDO/ARDO/CAS |
| Tax payment | Yes | AAB or ePayment |
| Payment verification | **No — BIR officer** | OPV verifies within 3 days |
| eCAR generation | **No — BIR officer** | Encoder + signatory |
| eCAR claim | **In-person required** | Physical documents + claim slip |

### Pain Points Reported by Practitioners

1. **Not truly end-to-end digital.** Even after online submission, the practitioner must physically visit the RDO to claim the eCAR with original documents. The "e" in eONETT is a submission digitization, not a process digitization.

2. **Computation is still officer-dependent.** The system does not auto-compute taxes from the uploaded documents. The practitioner enters amounts, but the BIR officer independently computes and may arrive at a different figure (especially if zonal values differ from what the practitioner looked up).

3. **Payment jurisdiction confusion.** The Ease of Paying Taxes Act (RA 11976) allowed filing anywhere, but eCAR processing remains tied to the RDO with jurisdiction over the property location (per RMC 56-2024). Payments made at AABs outside the jurisdictional RDO can cause verification delays.

4. **Birth pains and turnaround uncertainty.** PwC Philippines noted: "we have yet to see how the implementation of this system would improve the turnaround time." The system launched in 2023, and practitioners still report inconsistent processing times.

5. **Currently limited to real property sales.** Share transfers, donations, and estate settlements have limited or no eONETT coverage. PwC advocates for expansion.

6. **Duplicate physical document requirement.** All documents uploaded digitally must also be presented physically at claim time. This negates much of the efficiency gain from online submission.

7. **System was designed for the BIR's workflow, not the practitioner's.** The eONETT system mirrors the internal BIR processing steps (CDR check → OCS computation → approval chain → payment verification → eCAR encoding). It does not help the practitioner with their upstream work (document gathering, tax pre-computation, zonal value lookup, deadline tracking).

---

## 4. Zonal Value Lookup Workflow

### The Current Process (Step by Step)

This is the single most time-consuming data lookup in PH real estate tax computation:

1. **Go to bir.gov.ph** and find the "Zonal Values" link (under Quick Links or eServices).
2. **Select the Revenue Region** containing the property.
3. **Find the specific RDO** having jurisdiction over the property's city/municipality.
4. **Download the ZIP file** for that RDO's zonal schedule.
5. **Unzip the file** — requires software that can handle .zip compression (the BIR site explicitly notes this may require "special free software").
6. **Open the Excel workbook** (.xls or .xlsx format, varies by RDO).
7. **Navigate the workbook structure:**
   - First sheet is typically a NOTICE sheet with navigation instructions.
   - Second sheet may be a revision history (multiple revisions with effectivity dates and Department Order numbers).
   - Subsequent sheets contain the actual zonal values, organized by city/municipality, then by barangay, then by street/subdivision.
   - Property classification codes (RR = Residential Regular, CR = Commercial Regular, etc.) appear as column headers.
8. **Find the correct row** for the property's barangay + street/subdivision. This requires manual scrolling or Ctrl+F search.
9. **Find the correct column** for the property classification (must match the classification on the Tax Declaration).
10. **Read the zonal value per sqm**, then multiply by land area to get total zonal value.

### Why This Is Painful

- **124 separate workbooks** — no consolidated national database, no search across RDOs.
- **Heterogeneous formats** — each RDO's Excel file has different structure, column naming, sheet organization. Some use .xls (legacy), some .xlsx.
- **No API** — the BIR provides no programmatic access. Every lookup is a manual download-unzip-open-search cycle.
- **Address matching is fuzzy** — street names in the zonal schedule may not match the exact address on the deed or title. Barangay boundaries and names change. Subdivisions may or may not be listed.
- **Classification ambiguity** — the correct classification code must match the Tax Declaration, but the Tax Declaration may use different terminology than the zonal schedule column headers.
- **Revision history complicates lookups** — practitioners must check which revision was effective at the transaction date. Using the wrong revision produces the wrong zonal value and therefore the wrong tax.
- **BIR site notes that "basic Excel understanding" is recommended** — an implicit acknowledgment that the process is not accessible to all taxpayers.
- **Third-party tools exist but with caveats:**
  - zonalvalue.com — searchable interface, but disclaimers about accuracy.
  - zonalvaluefinderph.com — "2025 BIR Zonal Values in 3-easy-clicks" — but still relies on the same underlying BIR data.
  - FileDocsPhil sells curated zonal value Excel files for PHP 560.
- **Common workaround:** Call the RDO directly and ask the officer for the zonal value. This is faster but creates a dependency on officer availability and correctness.

### Time Estimate for One Lookup

- Experienced practitioner who knows the RDO and has the ZIP cached: **5-15 minutes**.
- First-time lookup for an unfamiliar area: **30-60 minutes** (finding the right RDO, downloading, navigating the workbook, resolving address ambiguity).
- Disputed/ambiguous cases (multiple possible classifications, street not listed): **requires RDO visit/call**, add **hours to days**.

---

## 5. Installment Sale Tracking — Developer VAT/CWT Workflow

### The Scale of the Problem

A mid-size Philippine real estate developer selling a 500-unit condominium project on 5-year installment plans must track:
- **500 individual VAT schedules** — output VAT recognized per installment payment received, monthly
- **500 individual CWT filings** — each unit's CWT must be filed separately (no lumping allowed per BIR policy)
- **Monthly VAT returns** (2550M, optional) and **quarterly VAT returns** (2550Q) aggregating all collections
- **Quarterly CWT returns** (1601-EQ) with attached alpha lists
- **BIR Form 2307** issuance per buyer per payment
- Cross-matching: CWT remittances in 1601-EQ must tie with input VAT listings in 2550Q (SAWT)

### How Developers Currently Track This

#### Small-to-Mid Developers: Excel-Based

**Typical Excel structure:**
- **Master spreadsheet** with one row per unit: unit number, buyer name, TIN, contract price, down payment, monthly amortization, start date, end date, classification (installment vs. deferred)
- **Collection tracker sheet:** Per unit, columns for each month. When payment is received, the amount is entered. Output VAT = collection x 12%.
- **VAT summary sheet:** Aggregates all collections per month/quarter for 2550M/2550Q filing.
- **CWT tracker sheet:** Per unit, tracks when CWT is due (on each installment if buyer is in trade/business; on last installment otherwise), amount withheld, BIR Form 1606 filing date.
- **2307 tracker sheet:** Tracks which Form 2307 certificates have been issued to which buyers for which periods.

**Pain points with Excel tracking:**
- **Manual data entry** for every collection received — no integration with bank systems or payment processors.
- **Error-prone reconciliation** — tying hundreds of individual unit collections to aggregate VAT returns requires manual cross-checking.
- **Versioning issues** — multiple staff editing the same workbook leads to data conflicts.
- **No automated alerts** for overdue payments, missed CWT filings, or approaching deadlines.
- **Scale breaks Excel** — a 1,000-unit project with 60 monthly payments = 60,000 individual data points per tracking dimension.
- **BIR audit exposure** — manual tracking increases risk of mismatches between SLSP (Summary List of Sales/Purchases), SAWT (Summary Alphalist of Withholding Taxes), and the aggregate returns.

#### Large Developers: ERP + Excel Hybrid

Large developers use ERP systems for the core accounting but supplement with Excel for BIR-specific compliance:

| System | What It Handles | What Still Needs Excel |
|--------|-----------------|----------------------|
| **SAP/Fasttrack** | Booking, payment schedule, AR aging, general ledger | BIR form generation, SAWT/SLSP preparation, CWT per-unit tracking |
| **Oracle NetSuite** | CWT withholding tax type auto-created per Philippine rules, AP/AR, VAT tracking | Reconciliation of 1601-EQ with 2550Q (SAWT matching) |
| **In4Suite** | Booking form, payment schedule, receipts, demand letters, collection aging | BIR-specific form generation, ONETT processing |
| **NOAH Business Applications** | End-to-end property management + financials | May still need manual SAWT/SLSP extraction |
| **QuickBooks PH** | VAT tracking, automatic tax calculations | Not designed for per-unit real estate installment tracking |

**The gap:** No ERP natively handles the BIR's per-unit, no-lumping CWT filing requirement combined with installment VAT recognition and SAWT/SLSP generation. This is always a custom configuration or Excel sidecar.

### Filing Cadence for a Developer

| Return | Frequency | Content | Tool Used |
|--------|-----------|---------|-----------|
| BIR Form 2550M (optional) | Monthly | All output VAT on collections received | ERP/Excel aggregate |
| BIR Form 2550Q | Quarterly | Full VAT return with SAWT attachment | eFPS/eBIRForms + Excel SAWT |
| BIR Form 1606 | Per transaction | CWT on each real property sale | Per-unit filing (manual or batch via eFPS) |
| BIR Form 1601-EQ | Quarterly | Aggregate EWT/CWT with alpha list | ERP/Excel + eFPS |
| BIR Form 2307 | Per payment period | Certificate of creditable tax withheld | Per-buyer generation (manual or ERP) |
| SLSP DAT file | Quarterly | Summary list of sales/purchases | Excel → DAT converter or JuanTax |
| SAWT DAT file | Quarterly | Summary alphalist of withholding taxes | Excel → DAT converter or JuanTax |

---

## 6. Real Property Tax (RPT) Payment Workflow

### How RPT Is Computed and Paid

The computation is straightforward (`AV = FMV × Assessment Level; RPT = AV × rate + AV × 1% SEF`), but the workflow is fragmented across 1,700+ LGUs with no standardization.

#### Current Process

1. Property owner receives (or fails to receive) an assessment notice from the LGU Assessor.
2. Owner or property manager checks the amount against the Tax Declaration's FMV column and the LGU's enacted assessment level and rate.
3. Payment at the LGU Treasurer's Office (in-person) or via online portal (limited to select Metro Manila cities).

#### Online Payment Portals (Metro Manila)

| City | Portal | Method | Notes |
|---|---|---|---|
| Manila | Go Manila App | App-based (E-Government > RPTAX) | SMS confirmation; scanned OR emailed |
| Makati | makationlinepayments.com | Web (GCash/Online Banking) | Requires tax declaration number |
| Quezon City | qceservices.quezoncity.gov.ph | Web (RPT Payment section) | Delinquent taxpayers must visit in-person |
| Taguig | taguig.gov.ph (limited) | In-person primarily | Online payment under development |

Each portal is completely independent — no cross-LGU portal exists.

#### Multi-Property Pain Points

1. **No unified tracker across LGUs.** Property managers with holdings across Manila, Makati, QC, and Taguig must navigate separate portals with different interfaces, payment channels, and tax declaration formats.
2. **Different discount schedules.** QC offers 20% advance discount (pay 2026 by Dec 31, 2025) and 10% prompt discount (pay by March 31). Other LGUs have different percentages and cutoffs. Missing a city's unique deadline means lost savings.
3. **SPA/authorization complexity.** Different LGUs have different requirements for property managers paying on behalf of owners (notarized SPA, management contracts, etc.).
4. **Double assessment risk.** Properties near jurisdictional boundaries may be assessed by two LGUs. Ignoring either triggers penalty accumulation.
5. **No consolidated receipt tracking.** Official receipts come in different formats per LGU. Reconciliation for multi-property portfolios is fully manual.

#### Time Estimate

For a property manager with 10-20 properties across 3-4 Metro Manila LGUs: **1-3 full days** per annual payment cycle.

---

## 7. EWT Compliance Workflow (Rent, Commissions, Contractor Payments)

### The Recurring Compliance Cycle

Companies making real-estate-adjacent payments face **13 filing obligations per year** for EWT alone:

| Obligation | Form | Frequency | Deadline |
|---|---|---|---|
| Monthly remittance (months 1, 2 of each quarter) | 0619-E | 8×/year | 10th of following month (15th for eFPS) |
| Quarterly return + QAP attachment | 1601-EQ | 4×/year | Last day of month after quarter |
| Annual information return + Alphalist | 1604-E | 1×/year | March 1 |
| Certificate to payees | Form 2307 | Quarterly | 20th of month after quarter close |

Even zero-transaction periods require zero-return filing.

### Rate Selection — The Core Pain Point

EWT rate selection for real-estate-adjacent payments requires navigating a multi-step decision tree:

| Payment Type | Individual Payee | Corporate Payee |
|---|---|---|
| Professional fees (brokers, agents) | 5% (≤₱3M) / 10% (>₱3M or VAT-registered) | 10% (≤₱720K) / 15% (>₱720K) |
| Rental of real property | 5% | 5% |
| Contractor payments | 2% | 2% |
| TWA purchases (goods) | 1% | 1% |
| TWA purchases (services) | 2% | 2% |

Common errors:
1. Applying 5% instead of 10% when the payee is VAT-registered (regardless of income threshold)
2. Wrong ATC code — must match exact transaction nature; cross-matching failures trigger BIR audit
3. Failing to exclude VAT from EWT base for VAT-registered payees
4. Not verifying whether payee is individual vs. corporate

### How It Is Done in Practice

- **QNE/N3 AI Accounting:** ATC selected during transaction encoding; system auto-computes withholding; generates 1601-EQ and QAP DAT file.
- **JuanTax/Taxumo:** Transactions entered once; forms auto-generated and e-filed.
- **Xero:** No native BIR form generation. Philippine users must supplement with manual processes.
- **NetSuite:** PH localization module with CWT codes and withholding tax reports (enterprise pricing).
- **Excel/manual:** SMEs manually look up ATC and rate, compute amounts, fill forms by hand or through eFPS.

### Time Estimate (monthly cycle, 20-50 vendors)

- Rate lookup and classification: **2-4 hours** (manual) vs. **minutes** (configured software)
- Monthly 0619-E: **1-2 hours**
- Quarterly 1601-EQ + QAP: **4-8 hours** (manual) vs. **1-2 hours** (automated)
- Ledger tie-out: **1-2 hours/month**

---

## 8. Form 2307 Issuance Workflow

### How Companies Generate Form 2307

**Approach 1 — Excel template + manual fill (most common for SMEs):**
- Download BIR Excel template from bir.gov.ph, DocHub, pdfFiller, or Scribd.
- Fill payee TIN, name, address, income breakdown by month, ATC code, computed tax.
- Print in triplicate (original for payee, duplicate for payor, triplicate for BIR).

**Approach 2 — BIR Online Tools (bir-online-tools.com):**
- Excel template with batch processing (fill data rows, generate multiple 2307s at once).
- Direct email delivery to vendors. Avoids PDF format rejection errors.

**Approach 3 — Accounting software (QNE, JuanTax, Taxumo):**
- QNE: auto-generated from billing statements, purchase invoices, or payment vouchers.
- JuanTax: transactions entered once; 2307 automated.
- Taxumo: withholding certificates tracked; SAWT auto-created for ITR filing.

**Approach 4 — BIR Excel Uploader (bir-excel-uploader.com):**
- Converts Excel data into DAT files; also supports printing Form 2307 from Excel template.
- Browser-based, works offline. Free for ≤20 rows; registration required beyond.

### Reconciliation Pain Points

1. **TIN-matching strictness.** BIR cross-matching requires amounts on issued 2307s to perfectly align with QAP submitted with 1601-EQ. Any discrepancy triggers audit.
2. **Scale.** A mid-size company issuing 50-100 Form 2307s per quarter must reconcile each against subsidiary ledger, 0619-E monthly remittances, and 1601-EQ quarterly return.
3. **Common errors:** wrong ATC code, TIN typos, incorrect period breakdown, missing certificates, late issuance.
4. **SAWT reconciliation (payee side).** Payees must compile SAWT from all 2307s received from various payors — must chase every customer/client for their certificate.
5. **Penalties:** ₱1,000 per violation (non-issuance, late issuance, incorrect completion) under NIRC Section 250, up to ₱25,000 annually. Expenses may be disallowed if withholding was not properly done.

### Time Estimate

- Manual 2307 issuance (50 vendors/quarter): **1-2 full days/quarter**
- Reconciliation against QAP/1601-EQ: **4-8 hours/quarter** (manual); **1-2 hours** (automated)
- Chasing missing 2307s from payors (payee side): **ongoing, highly variable**

---

## 9. Alphalist / DAT File Generation

### The Three Paths

**Path 1 — BIR Alphalist Data Entry and Validation Module (official BIR tool):**
- Current version: 7.4 (per RMC No. 015-2025, February 2025).
- **Requires Java SE 8** — newer Java versions cause crashes.
- Workflow: manual data entry → validate → generate DAT file → submit via eAFS portal or email.
- For eFPS users, generates appended key for DAT file.

**Path 2 — BIR Excel Uploader (bir-excel-uploader.com, third-party, free):**
- Converts Excel templates directly into BIR-compliant DAT files.
- Supports: Form 2307, RELIEF, Alphalist, QAP, MAP, SAWT, SRS.
- Registration required for >20 rows. Browser-based, offline capable.

**Path 3 — Accounting software with DAT export:**
- QNE: generates DAT files from transaction data (SAWT, QAP, alphalist).
- JuanTax: end-to-end filing including DAT generation.
- Taxumo: auto-generates DAT files for submission.

### Pain Points (widely regarded as worst government software tool)

1. **Java dependency hell.** Requires Java SE 8 specifically. Many machines have Java 11+ or no Java. Managing installations causes recurring crashes.
2. **Cryptic validation errors:** "Invalid character on field Registered Name" (hidden Unicode), "Invalid Length" on Branch Code (enforces 4-char codes when legitimate codes may be 3 or 5).
3. **Version migration headaches.** Upgrading from older versions loses data. Skipping intermediate versions causes additional issues.
4. **No undo/rollback.** Manual one-by-one entry with no easy way to batch-correct errors.
5. **Submission rejection risk.** Small mistakes (wrong TIN, mismatched totals, improperly named file) lead to rejected submissions, penalties, or audit triggers.

### Time Estimate

- Manual entry into BIR Module (50 payees): **4-8 hours** including troubleshooting
- BIR Excel Uploader (50 payees): **2-3 hours** (prep + conversion + validation)
- QNE/JuanTax/Taxumo with DAT export: **30 min to 1 hour**
- Annual 1604-E + full alphalist (200+ payees): **1-3 full days** (manual) vs. **half a day** (automated)

---

## 10. Transfer Tax Payment Workflow

### Step-by-Step Process

1. Secure notarized Deed of Sale/Donation/Transfer
2. Obtain certified true copy of title (TCT/CCT/OCT) from Register of Deeds
3. Get latest tax declarations from the Assessor's Office
4. Obtain eCAR from BIR (CGT and DST must already be paid)
5. Get RPT clearance from LGU Treasurer (no unpaid RPT arrears)
6. Present all documents to LGU Treasurer's Office
7. Treasurer computes transfer tax
8. Pay and secure Official Receipt
9. Present receipt to Register of Deeds for title transfer

**Deadline:** Within 60 days of deed execution or notarization.

### Pain Points

1. **No standardization across LGUs.** Each of 1,700+ LGUs sets its own rate within the legal ceiling. No centralized rate registry.
2. **Rate lookup requires calling or visiting the Treasurer's Office.** No comprehensive online database.
3. **In-person only (mostly).** Unlike RPT which has online portals in some cities, transfer tax payment is predominantly in-person.
4. **Sequential bottleneck.** Cannot be paid until BIR issues eCAR — delays at BIR cascade into LGU transfer tax delays.
5. **RPT clearance prerequisite.** Any unpaid RPT arrears must be settled before transfer tax is accepted.
6. **Varying processing times.** Some offices process in 30 minutes; others take days.

### Time Estimate

- Per transaction (in-person): **2-4 hours** (queuing + processing + payment)
- If RPT arrears exist: add **1-3 days** for back tax settlement
- If documents incomplete: add return trips (each 2-4 hours)

---

## 11. Consolidated Pain Point Map

### By Workflow Phase — Transaction Taxes (ONETT)

| Phase | Time | Key Pain Points |
|-------|------|-----------------|
| **Document gathering** | 1-5 days | Serial visits to 4+ offices; name mismatches; missing TINs; RPT arrears |
| **Zonal value lookup** | 15-60 min per property | No API; 124 heterogeneous Excel files; fuzzy address matching; revision ambiguity |
| **Tax pre-computation** | 15-30 min per transaction | Manual Excel; no standard template; must determine highest-of-three base; rate selection for CWT requires judgment |
| **ONETT submission** | 1-2 hours (eONETT) or half-day (walk-in) | eONETT is submission-only, not computation; walk-in queues; document completeness check |
| **OCS approval** | 1-3 days (simple) to 20 days (estate) | BIR officer computes independently; may disagree with practitioner's computation; approval chain |
| **Tax payment** | Same day | Low friction — ePayment channels available |
| **Payment verification** | 1-3 days (target) | Jurisdiction confusion post-EOPT Act; AAB payment may not be visible to RDO |
| **eCAR issuance** | 7 days (target); 5-30 days (actual) | Staffing shortages; backlogs; valuation disputes; still requires physical claim visit |
| **Post-BIR (LGU + RD)** | 2-6 weeks additional | Separate agencies; separate queues; serial processing |

### By Workflow Phase — Recurring Compliance (EWT/VAT/RPT)

| Phase | Time | Key Pain Points |
|-------|------|-----------------|
| **EWT rate selection** | 2-4 hours/month (manual) | 80+ ATC codes; individual vs corporate bifurcation; VAT-inclusive vs exclusive confusion |
| **Monthly 0619-E filing** | 1-2 hours | Must reconcile with subsidiary ledger; zero returns required even for no-activity periods |
| **Quarterly 1601-EQ + QAP** | 4-8 hours (manual) | QAP DAT file generation; cross-matching with monthly remittances |
| **Form 2307 issuance** | 1-2 days/quarter (50 vendors) | TIN matching; triplicate printing; monthly breakdown accuracy |
| **Form 2307 reconciliation** | 4-8 hours/quarter | Must tie: 2307 ↔ QAP ↔ 1601-EQ ↔ 0619-E; payee-side SAWT collection |
| **Alphalist/DAT generation** | 4-8 hours (manual, 50 payees) | BIR Module Java crashes; cryptic validation errors; version migration |
| **RPT payment (multi-property)** | 1-3 days/year | No cross-LGU portal; different discount schedules; SPA requirements |
| **Transfer tax payment** | 2-4 hours per transaction | In-person only; rate not published centrally; RPT clearance prerequisite |

### By Practitioner Type

| Practitioner | Primary Pain | Secondary Pain |
|---|---|---|
| **Individual seller/buyer** | Overwhelming complexity; don't know where to start; hire a "processor" | Late filing penalties from not knowing deadlines |
| **Real estate broker** | Document coordination between buyer and seller; zonal value lookup; deadline tracking across multiple concurrent transactions | Commission withholding computation (10/15% EWT on their own income) |
| **Tax accountant/CPA** | Multi-client ONETT tracking; each client has different documents in different states of completion | SAWT/SLSP preparation; Form 2307 reconciliation; alphalist DAT file generation |
| **Real estate developer** | Scale — hundreds of units, each requiring individual CWT filing; installment VAT schedule tracking; SAWT/SLSP volume | ERP-to-BIR integration gap; no lumping of CWT; per-unit Form 2307 generation |
| **Property manager** | Multi-LGU RPT tracking; no unified portal; different discount schedules per city | SPA/authorization complexity; penalty accumulation across properties |
| **"Processor" (informal fixer)** | Knowledge lives in their head, not in systems; each RDO has slightly different practices | Risk of incorrect computation without formal training |

### Top 10 Automation Opportunities (Workflow-Based, Ranked by Impact)

1. **Zonal value lookup automation** — Replace the download-unzip-search cycle with an instant API/search. Highest-leverage single improvement because it feeds into every tax computation.

2. **Tax pre-computation engine** — Auto-compute CGT/DST/CWT/VAT from inputs (selling price, zonal value, FMV, property classification, seller type, payment terms). Eliminate manual Excel.

3. **Installment VAT/CWT schedule generator** — Given a payment schedule and contract terms, auto-generate the monthly/quarterly VAT recognition schedule and per-unit CWT filing calendar. Critical for developers.

4. **Form 2307 batch generation + reconciliation** — Auto-generate Form 2307 certificates from transaction records; auto-reconcile against QAP/1601-EQ/0619-E. Replace the most error-prone manual compliance step.

5. **SAWT/SLSP/DAT file generator** — Auto-generate the BIR-required summary lists and DAT files from transaction records. Eliminate BIR Alphalist Module dependency and its Java-hell UX.

6. **EWT rate classification engine** — Decision tree that takes payee type (individual/corporate), registration status (VAT/non-VAT), income level, and payment nature → outputs correct ATC code and rate. Prevents the most common compliance errors.

7. **Document readiness tracker** — Track which documents are gathered, which are outstanding, which offices need to be visited. Auto-compute deadlines (30 days for CGT, 5 days for DST) from deed date.

8. **Multi-LGU RPT tracker** — Unified dashboard for RPT across LGUs: due dates, discount deadlines, amounts, payment status, receipt tracking.

9. **DST on mortgage calculator** — Automate the stepped-schedule computation (Section 195). Currently zero tools cover this. Trivial to build, immediate value for lending/mortgage practitioners.

10. **Transfer tax rate database** — Centralized, maintained database of transfer tax rates across LGUs. Currently no such resource exists — practitioners must call each LGU.

---

## 12. Summary: Current Automation Level by Workflow

| Workflow | Primary Tool Today | Automation Level | Key Gap |
|---|---|---|---|
| ONETT transaction taxes (CGT/DST/CWT) | Excel + eONETT submission portal | Low | No self-service computation; BIR officer computes |
| Zonal value lookup | BIR ZIP/Excel files + phone calls | Very Low | No API; 124 heterogeneous workbooks |
| Installment VAT/CWT tracking | Excel (SME) / ERP+Excel (large dev) | Low-Medium | No tool handles per-unit BIR compliance at scale |
| EWT rate selection & filing | QNE, JuanTax, Taxumo (if adopted) | Medium | Rate selection still error-prone; ATC complexity |
| Form 2307 issuance | Excel template / QNE / JuanTax | Medium | Reconciliation across payor-payee chain is manual |
| Alphalist/DAT file generation | BIR Module v7.4 (Java) / BIR Excel Uploader | Low-Medium | BIR Module has severe UX issues; Java dependency |
| RPT computation & payment | In-person at LGU / Excel | Low | No cross-LGU portal; no multi-property tracker |
| Transfer tax payment | In-person at LGU Treasurer | Very Low | No online payment; no centralized rate database |
| DST on mortgage | Manual computation | Very Low | Zero tools cover Section 195 stepped schedule |

---

## Sources

- [PwC PH — eONETT: A More Convenient Way to Secure an eCAR](https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2023/eonett-a-more-convenient-way-to-secure-an-ecar.html)
- [Grant Thornton PH — BIR Clarifies eCAR Issuance for ONETT](https://www.grantthornton.com.ph/insights/articles-and-updates1/tax-notes/bir-clarifies-issuance-of-ecar-relative-to-one-time-transaction-onett/)
- [Grant Thornton PH — EOPT Updates on CAR Application](https://www.grantthornton.com.ph/insights/articles-and-updates1/lets-talk-tax/eopt-is-here-updates-on-car-application/)
- [Forvis Mazars PH — BIR RMC 56-2024](https://www.forvismazars.com/ph/en/insights/tax-alerts/bir-rmc-56-2024)
- [Forvis Mazars PH — BIR RMC 10-2023 (eONETT announcement)](https://www.forvismazars.com/ph/en/insights/tax-alerts/bir-rmc-10-2023)
- [Reyes Tacandong — RMO No. 12-2025](https://www.reyestacandong.com/bir-issuances-rmo-no-12-2025/)
- [Reyes Tacandong — RMC 56-2024](https://www.reyestacandong.com/bir-issuances-rmc-56-2024/)
- [AJA Law — BIR Digital Transformation: eONETT and ORUS](https://www.ajalaw.ph/bir-digital-transformation-eonett-orus/)
- [Respicio & Co. — BIR eCAR Processing Time](https://www.respicio.ph/commentaries/bir-ecar-processing-time-after-tax-payment-how-long-does-it-take-philippines)
- [Respicio & Co. — Where to Find BIR Zonal Values](https://www.respicio.ph/commentaries/where-to-find-bir-zonal-values-for-real-property-philippines)
- [Respicio & Co. — Delays in Processing Deed Transfer Applications](https://www.lawyer-philippines.com/articles/delays-in-processing-deed-transfer-applications)
- [FiledocsPhil — BIR Zonal Value Lookup Guide](https://www.filedocsphil.com/how-to-look-for-bir-zonal-value/)
- [FiledocsPhil — Transfer Land Title Complete Guide](https://www.filedocsphil.com/transfer-land-title-in-the-philippines-a-complete-guide/)
- [BIR Official — eONETT Portal](https://eonett.bir.gov.ph/)
- [BIR Official — Zonal Values Page](https://www.bir.gov.ph/zonal-values)
- [BIR Official — CDR Checklist (PDF)](https://web-services.bir.gov.ph/eappointment/files/checklist_of_documentary_requirements.pdf)
- [BIR Official — ONETT OCS Annexes (PDF)](https://bir-cdn.bir.gov.ph/BIR/pdf/Annex%20D1%20to%20D10%20(Updated).pdf)
- [CREBA — Real Estate Sales VAT Remittance](https://creba.ph/real-estate-sales-vat-remittance-status-quo-remains-says-bir/)
- [KeyRealty — Common Problems in Title Transfers](https://keyrealty.ph/common-problems-in-title-transfers/)
- [ForeclosurePhilippines — CWT in Real Estate](https://www.foreclosurephilippines.com/creditable-withholding-tax-in-real/)
- [ForeclosurePhilippines — VAT on Real Estate Sales](https://www.foreclosurephilippines.com/value-added-tax-vat-on-the-sale-of-real-estate/)
- [Housal — Real Estate Closing Costs Calculator](https://www.housal.com/calculators/sales-closing-fees)
- [In4Velocity — In4Suite ERP Philippines](https://www.in4velocity.com/in4suite-erp/philippines/)
- [Oracle — NetSuite CWT for Philippines](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N1960490.html)
- [ZonalValue.com](https://zonalvalue.com/)
- [ZonalValueFinderPH.com](https://zonalvaluefinderph.com/)
- [Quezon City RPT Payment Schedule](https://quezoncity.gov.ph/payment-of-real-property-tax-schedule/)
- [Makati Online Payments](https://www.makati.gov.ph/content/events/22036)
- [Emerhub — Guide to Real Property Tax](https://emerhub.com/philippines/guide-to-real-property-tax-in-the-philippines/)
- [QNE — How to Generate BIR 1601-EQ](https://support.qne.com.ph/support/solutions/articles/35000199957-how-to-generate-bir-1601-eq-form)
- [QNE — How to Generate BIR 2307](https://support.qne.com.ph/support/solutions/articles/35000199952-how-to-generate-bir-2307-form)
- [QNE — Fix Invalid Length Error in DAT File](https://support.qne.com.ph/support/solutions/articles/35000122686-how-to-fix-invalid-length-error-when-validating-bir-dat-file)
- [BIR Excel Uploader](https://bir-excel-uploader.com/)
- [BIR Online Tools — First Excel Conversion](https://bir-online-tools.com/how-to/first-excel-conversion/)
- [JuanTax — Form 2307](https://juan.tax/form-2307/)
- [Taxumo — BIR Form 2307 Guide](https://www.taxumo.com/blog/comprehensible-guide-bir-form-2307/)
- [Taxumo — Making Sense of EWT](https://www.taxumo.com/blog/making-sense-expanded-withholding-tax-forms-2307-0619e-1601eq-qap/)
- [Taxumo — How to Make a BIR DAT File](https://www.taxumo.com/blog/how-to-make-a-bir-dat-file-without-using-the-bir-excel-uploader/)
- [Grant Thornton PH — Alphalist Module v7.4](https://www.grantthornton.com.ph/technical-alerts/tax-alert/2025/availability-of-the-alphalist-data-entry-and-validation-module-version-7.4/)
- [CPA Davao — Mastering BIR Alphalist](https://www.cpadavao.com/2025/05/Mastering-the-BIR-Alphalist-Data-Entry-A-Complete-Guide-for-Accurate-and-Timely-Tax-Compliance.html)
- [Taguig City Transfer Tax Citizen's Charter](https://taguig.gov.ph/assets/pdfform/citizens_charter/city_treasurers_office/(2)PAYMENT_OF_TRANSFER_TAX.pdf)
- [BLGF — DC No. 001-2019 Transfer Tax](https://blgf.gov.ph/wp-content/uploads/2021/02/DC-No-001-2019-Transfer-Tax-on-Real-Property.pdf)
- [NTRC — Real Property Tax Online Payments](https://www.ntrc.gov.ph/images/journal/2024/j20240506a.pdf)
- [PwC PH — Withholding Taxes: Are You On Top?](https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2019-taxwise-or-otherwise/witholding-taxes-are-you-on-top.html)
- [CloudCFO — EWT Guide for Non-TAMP](https://cloudcfo.ph/blog/common-transactions-subject-to-expanded-withholding-tax-ewt-under-rr-11-2018-for-non-tamp-companies/)
- [Xero Product Ideas — PH BIR Compliance](https://productideas.xero.com/forums/939198-for-small-businesses/suggestions/45245053-xero-reporting-for-philippines-bir-compliance)
- [Omni HR — BIR Form 2307 Explained](https://www.omnihr.co/blog/bir-2307-form)
- [MPM — Quarterly Alphalist of Payees](https://mpm.ph/quarterly-alphalist-of-payees-qap/)
