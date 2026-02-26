# Existing Tools Survey — JuanTax, Taxumo, QNE Cloud

## Overview

This analysis maps each Wave 2 computation against the three primary Philippine tax software platforms (JuanTax, Taxumo, QNE Cloud) and generic ERPs, documenting feature coverage, gaps, and technical capabilities.

---

## 1. JuanTax (juan.tax / plus.juan.tax / fastfile.juan.tax)

### Company Profile

- **Founded:** 2017
- **Status:** First BIR-accredited electronic Tax Software Provider (eTSP) under the eTSP Program (2019)
- **Approved:** Operator of Payment System (OPS) by BSP
- **Merger:** Merged with Jaz Philippines in Jan 2025 to form Juan Accounting Software (juan.ac)
- **Ownership history:** Acquired by Beppo (May 2024), then sold to Jaz Philippines; Beppo now operates separately
- **Tax payments processed:** PHP 6.7B ($114.67M) since launch
- **Target market:** Philippine SMBs, freelancers, CPA firms/accounting practitioners

### Product Lines

| Product | Target | Pricing | Model |
|---------|--------|---------|-------|
| **JuanTax Fast File** | Business owners, freelancers | PHP 120/generated form | Pay-per-use |
| **JuanTax Plus** | CPA firms, accounting practitioners | PHP 2,000/org/month (PHP 19,200/yr) | Subscription |
| **Juan Accounting** (Free) | Small businesses, self-employed | PHP 0 | Free tier |
| **Juan Accounting** (Essentials) | Growing businesses | PHP 2,000/month | Subscription |
| **Juan Accounting** (Growth) | Larger SMBs needing CAS | From PHP 10,000/month | Custom |
| **Training** | New JuanTax Plus users | PHP 6,000 initial / PHP 3,000 re-training | One-time |
| **Attorney consultation** | All users | PHP 900/30 days (via Legal Tree) | Add-on |

### Supported BIR Forms (Comprehensive List)

**Percentage Tax:** 2551Q
**VAT:** 2550M, 2550Q
**Withholding Tax (EWT):** 1601-EQ, 1601-FQ, 1604-E, 1604-F, 2306, 2307
**Compensation:** 1601-C, 1604-C, 2316
**Income Tax:** 1701, 1701A, 1701Q, 1702Q, 1702-RT
**Real Estate / General:** 1606 (CWT on real property), 1706 (CGT), 2000 (DST), 2000-OT (one-time DST)
**Payment:** 0619-E, 0619-F, 0605
**DAT Files:** SLSP, SAWT, QAP

### BIR Filing Capabilities

- **Fast File:** E-files to BIR by 9 PM daily; later transmissions sent next business day
- **Fast File vs eFPS restriction:** Taxpayers enrolled in BIR eFPS are NOT permitted to use Fast File (or any third-party platform) unless BIR grants permission via memo or the form is unavailable in eFPS
- **Payment channels:** Credit/debit card, BPI, UnionBank, PayMaya, Coins.ph, GCash, GrabPay, Paymongo

### Technical Capabilities

**API:**
- REST API at `https://api.juan.tax` with developer portal at `https://developer.juan.tax`
- OAuth 2.0 authentication (Client Credentials Flow)
- Sandbox and Live environments
- Rate limit: 60 requests/minute
- JSON responses
- Documented endpoints:
  - `POST/GET/PUT /organizations/` — CRUD for organizations
  - `GET /reports/{org_id}/` — list filed tax reports
  - `POST/PUT /reports/1601C/` — create/update Form 1601-C
  - `POST/GET/PUT /reports/2551Q/` — CRUD for Form 2551Q
- **Notable API gap:** Only 2 form types (1601-C, 2551Q) have documented create/update endpoints; no API coverage for Forms 1706, 1606, 2000-OT, or any real estate transaction forms
- Contact: api@juan.tax for technical, sales@juan.tax for onboarding

**Integrations:**
- Xero (primary; bidirectional sync of tax codes and transactions)
- Juan Accounting Software (built-in; seamless tax form sync)
- Open API keys available on Essentials and Growth plans (Juan Accounting)

**No webhook documentation found.**

---

## 2. JuanTax Coverage Mapped to Wave 2 Computations

### A. Real Estate Transaction Taxes

| Computation | JuanTax Coverage | Detail |
|-------------|-----------------|--------|
| **Highest-of-three base** | PARTIAL — manual input | User must determine and enter the higher value. JuanTax does NOT compare selling price vs zonal value vs assessor FMV automatically. Form 1706: user enters "assessed value of the property based on factors 29 A-D"; Item 30C is pre-populated from user entries. No zonal value lookup. |
| **CGT (6%)** | FORM FILING ONLY | Form 1706 available in Fast File. User enters seller/buyer info, property details, transaction specifics, FMV assessments manually. JuanTax computes the tax due from entered values. Does NOT determine tax base from zonal values. e-Payment NOT available for Form 1706 — must pay via RCO at RDO. |
| **DST on sale (1.5%)** | FORM FILING ONLY | Form 2000-OT available. Same manual-entry pattern. No automated tax base resolution. |
| **DST on mortgage** | FORM FILING ONLY | Form 2000-OT covers one-time DST. Stepped schedule computation not documented as automated. |
| **VAT on real property (12%)** | PARTIAL | VAT computation supported for regular business transactions (2550M/2550Q). Residential threshold exemption check not automated for real property specifically. Form 2550Q filing fully supported. |
| **Installment VAT schedule** | NOT COVERED | No installment VAT per-collection tracking. No 25% initial payment test automation. No multi-period VAT recognition schedule. JuanTax handles VAT as period-based (monthly/quarterly), not per-collection. |
| **CWT rate/timing** | FORM FILING ONLY | Form 1606 available (withholding on real estate transfer). User must determine rate (1.5%/3%/5%/6%) and enter amounts. No "habitually engaged" test automation. No installment timing logic. |
| **Transfer tax** | NOT COVERED | Transfer tax is an LGU-level tax. JuanTax only covers BIR (national) taxes. No LGU tax computation. |
| **Zonal value lookup** | NOT COVERED | No zonal value database, no lookup functionality, no BIR zonal value integration. User must independently obtain zonal values and enter them manually. |

### B. Business Tax Compliance (Real Estate Adjacent)

| Computation | JuanTax Coverage | Detail |
|-------------|-----------------|--------|
| **EWT rate classification** | COVERED (with caveats) | Full ATC code library. EWT Analysis feature (Plus only) allows viewing withholding per vendor and comparing EWT vs VAT return. Tax code automation: transactions tagged with ATCs auto-populate forms. However, rate SELECTION still depends on user correctly classifying the payee — JuanTax does not auto-determine whether a payee is individual/corporate, licensed/unlicensed, or whether ₱3M/₱720K threshold is breached. |
| **VAT reconciliation (2550M/2550Q)** | PARTIALLY COVERED | EWT Analysis report cross-checks EWT vs VAT numbers. 2550Q filing supported with all schedules. Known limitation: partial payment recognition issue for service companies (Xero integration) — VAT not recognized until FULLY PAID, causing reconciliation discrepancies. 2550M effectively deprecated (RMC 05-2023) but still available as optional filing. |
| **Form 2307 generation** | COVERED | Automated generation from transactions. Enter or upload transaction once, Form 2307 populated automatically. SAWT auto-generated as attachment. RMC 14-2025 digital copies supported. |
| **Alphalist generation (1604-C/E/F)** | COVERED | Forms 1604-C, 1604-E, 1604-F all supported. QAP (Quarterly Alphalist of Payees) auto-generated from 1601-EQ/1601-FQ data. Annual alphalist for 1604-E and 1604-F simplified — pulls from quarterly alphalists without re-encoding. 1604-C requires employee schedule population (11 schedules; manual entry or CSV import). |

### C. Real Property Tax

| Computation | JuanTax Coverage | Detail |
|-------------|-----------------|--------|
| **RPT computation** | NOT COVERED | RPT is a local government tax (RA 7160). JuanTax is exclusively a BIR (national) compliance platform. No LGU tax computation, no assessment level tables, no RPT filing. |

---

## 3. Taxumo (taxumo.com)

### Company Profile

- Philippines' #1 online tax filing platform for freelancers, small business owners, and self-employed professionals
- Web-based platform for income/expense tracking and BIR form auto-population
- Higher web traffic ranking than JuanTax (ranked #71 in Legal category per SimilarWeb)
- Target market: individual taxpayers, freelancers, micro-enterprises

### Coverage Assessment

- **Core focus:** Income tax (1701/1701A/1701Q), percentage tax (2551Q), VAT (2550Q), withholding remittance
- **Real estate transaction taxes:** No documented support for Forms 1706, 1606, 2000-OT for real property transactions
- **Zonal value lookup:** Not available
- **ONETT processing:** Not covered
- **LGU taxes (transfer tax, RPT):** Not covered
- **Installment VAT tracking:** Not documented
- **CWT on real property:** Not documented

**Assessment:** Taxumo is narrower than JuanTax, focused on recurring tax compliance (monthly/quarterly/annual) for freelancers and small businesses. No real estate transaction tax features.

---

## 4. QNE Cloud / QNE Optimum / N3 AI Accounting (qne.cloud/ph)

### Company Profile

- **Full name:** QNE Software Philippines, Inc. (est. December 2007)
- **Parent:** QnE Software Sdn. Bhd. (Malaysia); legacy spanning 20+ years
- **Product evolution:** QNE Desktop → QNE Optimum (hybrid) → QNE AI Cloud → N3 AI Accounting (rebranded 2025)
- **Merger:** Merged with JAZ Technologies in 2025
- **Employee count:** 11–50
- **Client base:** 1,000+ clients across Philippines and Southeast Asia
- **Target market:** SMEs primarily; also startups, mid-market firms, large enterprises, accounting/bookkeeping firms
- **Industries served:** Retail, construction, real estate (as a business sector), law firms, manufacturing, agriculture, accounting, healthcare, energy, telecommunications, transportation
- **BIR accreditation:** CAS-ready (Computerized Accounting Software)

### Pricing

| Plan | Monthly (Annual) | Monthly (Monthly) | Users | Notes |
|------|-----------------|-------------------|-------|-------|
| Basic | PHP 900/mo | PHP 1,080/mo | 3 + 1 accountant | Basic bookkeeping, BIR-ready |
| Essential | PHP 1,300/mo | — | — | — |
| Enterprise | up to PHP 12,000/mo | — | — | Full feature set |
| On-premise | — | — | — | One-time license from ~$100 |

30-day free trial available (no credit card required).

### Modules

- **Financial Accounting:** General Ledger, Cash Receipts/Disbursements Journals, Sales/Purchase Journals, Trial Balance, Income Statement, Balance Sheet, Cash Flows
- **Customer Module:** AR, billing, invoicing
- **Supplier Module:** AP, purchase orders, payment vouchers
- **Inventory Module:** Stock management (no auto-FIFO for batch numbers)
- **Payroll Module:** Monthly/daily/hourly rates, payslips, payroll registers, tax annualization, SSS/PhilHealth/Pag-IBIG/BIR tax tables (TRAIN-updated), BIR 2316/1601-C/1604-C generation, direct link to BIR Alphalist System
- **POS Module:** Barcode scanner integration
- **Sales/Purchase Distribution**
- **Bank Reconciliation**

### BIR Forms Generated

| Form | Description | Module |
|------|-------------|--------|
| 2550Q | Quarterly VAT Return | VAT Module |
| 2550M | Monthly VAT Declaration (abolished Jan 2023, still generatable) | VAT Module |
| 1601-EQ | Quarterly EWT Remittance Return | W/Tax Module |
| 0619-E | Monthly EWT Remittance | W/Tax Module |
| 1604-E | Annual EWT Information Return | W/Tax Module |
| 1604-C | Annual Compensation Withholding Return | Payroll Module |
| 2307 | Certificate of Creditable Tax Withheld | W/Tax Module (auto-generated from transactions) |
| 2316 | Certificate of Compensation Payment/Tax Withheld | Payroll Module |
| 1601-C | Monthly Compensation Remittance | Payroll Module |

### DAT File Generation

- **SAWT** (Summary Alphalist of Withholding Taxes) — auto-generated from journal entries
- **QAP** (Quarterly Alphalist of Payees) — attachment for 1601-EQ/1601-FQ
- **SLSP** (Summary List of Sales/Purchases)
- **VAT Relief data files**

Key user praise: "In just one entry to the journals, you can generate data in the ledger, trial balance, income statement, balance sheet, cash flows, and most importantly SAWT, VAT relief, and QAP DAT files that can be readily downloaded and submitted to the BIR."

### Withholding Tax Automation (Detail)

- W/Tax Codes predefined based on BIR Alphanumeric Tax Codes (ATC) and corresponding rates
- Each code must be activated and assigned to a GL account before use
- Once enabled, codes applied to suppliers, customers, or transactions
- Auto-computes withholding amount on bills, payment vouchers, and invoices
- Example: Payment voucher with WC 158 (1% EWT) → auto-computes tax → posts to W/Tax Payable account
- Covers: Professional fees (WI010/WI011/WC010/WC011), brokers (WI040/WI041/WC040/WC041), rentals (WI100/WC100), contractors (WI120/WC120), TWA codes (WI158/WC158, WI160/WC160)
- Generates accurate EWT and FWT summaries for BIR submission

### Technical Capabilities

**API:**
- Integrates with QNE Cloud Payroll, QNE Digital Portal, POS machines, barcode scanners
- Microsoft Azure integration
- API access available (details not publicly documented)
- No public REST API documentation found (unlike JuanTax)

**BIR Filing:**
- Generates DAT files compatible with BIR electronic submission
- Does NOT directly file via eFPS (no such public API exists)
- DAT files must be manually uploaded to BIR eFPS or emailed to esubmission@bir.gov.ph

**AI Features (N3 AI Accounting):**
- QBot AI assistant for task automation
- OCR (Optical Character Recognition) for automated data entry / receipt scanning
- Quinny AI Virtual CFO: Report Analyzer (plain-English queries), Financial Advisor (industry benchmarking)
- QuickScan for attachment upload and conversion

**Mobile:** Android/iOS app

### Known Limitations (User Reviews)

1. Cloud version expensive for small businesses
2. Learning curve for beginners ("complicated to use at first")
3. No invoice lock feature after finalization
4. No auto-FIFO for batch number management
5. Limited report customization
6. Internet-dependent for some functions
7. Occasional bugs during updates (files take longer to generate)
8. English-only interface
9. Access rights/permissions unclear to configure
10. No Excel import for manual journal vouchers
11. Windows compatibility issues with some updates
12. User lock issues (shows logged in after logout)
13. Generic training ("feels too generic")
14. Limited scalability for larger enterprises (concurrent user caps)

### Coverage Mapped to Wave 2 Computations

#### A. Real Estate Transaction Taxes

| Computation | QNE Coverage | Detail |
|-------------|-------------|--------|
| **Highest-of-three base** | NOT COVERED | No zonal value lookup. No tax base comparison engine. Not within QNE's feature scope. |
| **CGT (6%)** | NOT COVERED | No Form 1706 generation. No ONETT computation. CGT is a one-time transaction tax outside QNE's recurring compliance model. |
| **DST on sale (1.5%)** | NOT COVERED | No Form 2000-OT generation. No DST conveyance computation. |
| **DST on mortgage** | NOT COVERED | No Section 195 stepped schedule computation. |
| **VAT on real property (12%)** | PARTIAL | General VAT module handles standard 12% output VAT. BUT: no real-estate-specific decision tree (residential ≤₱3.6M threshold, bare lot exclusion, deemed sale, 25% installment test). VAT computed as standard rate on transaction amount. |
| **Installment VAT schedule** | NOT COVERED | No per-collection VAT recognition tracking. No multi-period schedule. VAT module is period-based, not transaction-based. |
| **CWT rate/timing** | NOT COVERED | No Form 1606. No "habitually engaged" test. No 1.5%/3%/5%/6% rate tiering for property sales. |
| **Transfer tax** | NOT COVERED | LGU-level tax outside QNE's BIR-focused scope. |
| **Zonal value lookup** | NOT COVERED | No zonal value database. No BIR zonal value integration. |

#### B. Business Tax Compliance (Real Estate Adjacent)

| Computation | QNE Coverage | Detail |
|-------------|-------------|--------|
| **EWT rate classification** | COVERED (with manual payee classification) | Predefined ATC codes auto-compute withholding on transactions. User must select correct ATC code (classify payee type and income threshold). No automated decision tree for rate selection. |
| **VAT reconciliation (2550Q)** | COVERED | VAT Declaration Form auto-calculates monthly/quarterly values. BIR 2550Q generation with field-level auto-population from journals. VAT Module supports deferred VAT posting per code. |
| **Form 2307 generation** | COVERED | Auto-generated from billing statements, purchase invoices, payment vouchers. Captures BIR classifications from transaction encoding. |
| **Alphalist (1604-C/E/F)** | COVERED | 1604-E via W/Tax module. 1604-C via Payroll module. QAP auto-generated as attachment to 1601-EQ. SAWT auto-generated. DAT files downloadable for BIR submission. |

#### C. Real Property Tax

| Computation | QNE Coverage | Detail |
|-------------|-------------|--------|
| **RPT computation** | NOT COVERED | LGU tax. No assessment level tables, no FMV database, no RPT filing. |

**Assessment:** QNE is a comprehensive general business accounting platform with strong BIR recurring compliance features (VAT, EWT, withholding tax, alphalists, Form 2307). Its competitive advantage is the multifunction output — single journal entry generates multiple reports and DAT files. However, QNE's architecture is fundamentally **period-based** (monthly/quarterly accounting cycles) and does not address **one-time real property transaction taxes** (CGT, DST, CWT on property, transfer tax). The ONETT workflow is entirely outside QNE's product scope. No evidence of zonal value lookup, real estate tax computation, or Form 1706/1606/2000-OT generation in any QNE product line.

---

## 5. BIR eONETT (Electronic One-Time Transaction System)

### System Profile

- **Operator:** Bureau of Internal Revenue (government)
- **URL:** https://eonett.bir.gov.ph/
- **Legal basis:** RMC 10-2023
- **Type:** Web-based government workflow system for processing real property transfer taxes

### Capabilities

**Application types:**
- "+ New CGT & DST Application" — for sale of real property classified as **capital assets**
- "+ New EWT or DST Application" — for sale of real property classified as **ordinary assets**

**Workflow (6 steps):**
1. Account creation and application submission on eONETT portal
2. Document upload (tax declaration, deed of sale, etc.)
3. BIR ONETT Officer-of-the-Day reviews and generates ONETT Computation Sheet (OCS) — **officer computes, not the system self-service**
4. Taxpayer pays through authorized channels (online or over-the-counter)
5. Taxpayer uploads proof of payment
6. System generates claim slip for eCAR; taxpayer claims eCAR at RDO

**What it computes (officer-mediated):**
- CGT (6%) on capital asset sales
- DST on sale (1.5%) on all property transfers
- EWT/CWT on ordinary asset sales (rate determined by officer)
- Donor's Tax on gratuitous transfers

**Key limitation:** eONETT is a **BIR workflow system**, not a self-service computation engine. The taxpayer submits documents; the BIR officer reviews, looks up zonal values internally, determines the tax base, and generates the OCS. There is no public-facing computation logic, no API, and no self-service calculator.

**eONETT does NOT cover:**
- Self-service tax computation (taxpayer cannot see or verify computation before officer review)
- Public zonal value lookup (officer accesses internal BIR database)
- Installment VAT schedule tracking
- RPT computation (LGU jurisdiction)
- Transfer tax (LGU jurisdiction)
- Form 2307 generation (different workflow)
- EWT rate classification for non-property transactions
- DST on mortgage (separate filing)

**Process timeline:** eONETT applications are automatically transmitted to BIR systems — taxpayers no longer need to file through eBIRForms for ONETT transactions. However, officer review introduces unpredictable delay (practitioners report 2–8 weeks).

### Coverage Mapped to Wave 2 Computations

| Computation | eONETT Coverage | Detail |
|-------------|----------------|--------|
| **Highest-of-three base** | YES (internal) | Officer resolves internally; taxpayer cannot verify |
| **CGT (6%)** | YES (officer-computed) | Officer generates OCS with CGT amount |
| **DST on sale (1.5%)** | YES (officer-computed) | Included in OCS |
| **DST on mortgage** | NOT COVERED | Separate Form 2000-OT filing |
| **VAT on real property** | NOT COVERED | Separate 2550Q filing workflow |
| **Installment VAT schedule** | NOT COVERED | No multi-period tracking |
| **CWT rate/timing** | YES (officer-computed) | Officer determines rate and amount |
| **EWT rate classification** | N/A | Not within ONETT scope |
| **RPT computation** | NOT COVERED | LGU jurisdiction |
| **Transfer tax** | NOT COVERED | LGU jurisdiction |
| **Form 2307 generation** | N/A | Different workflow |
| **Zonal value lookup** | YES (internal only) | Officer accesses BIR database; no public access |

**Assessment:** eONETT digitized the paper-based ONETT process but did NOT automate the computation. The bottleneck shifted from physical queuing to officer review queuing. For practitioners, the key gap is the inability to **pre-compute and verify** tax amounts before submission — they must submit blind and wait for officer review.

---

## 5.5. BIR ORUS (Online Registration and Update System)

- **URL:** Launched October 2, 2025
- **Purpose:** Centralized digital platform for taxpayer registration, TIN issuance, COR generation, ATP applications
- **Integration:** Feeds data to eFPS, eAFS, eONETT; ORUS-updated address auto-syncs to returns
- **Impact:** Reduced registration processing by 70%; 1M+ accounts since launch
- **Relevance to this survey:** Infrastructure only — no tax computation features. Relevant as data source for eONETT (taxpayer profile, RDO assignment) but not a computation tool.
- **Future:** Mobile app planned Q4 2026; AI-powered document validation; e-invoicing integration; 90% digital target by 2028

---

## 5.6. ETAR — Estate Tax Amnesty Return

**Note:** ETAR stands for **Estate Tax Amnesty Return**, not "Electronic Tax Assessment Return." It refers to BIR Form No. 2118-EA filed under RA 11213 (Tax Amnesty Act) for estates of decedents who died on or before May 31, 2022. This is a one-time amnesty program, not a computation tool. Filing deadline: June 30, 2025. Not relevant to real estate transaction tax computation.

---

## 5.7. Housal (housal.com) — Real Estate Closing Cost Calculator

### Profile

- **URL:** https://www.housal.com/calculators/sales-closing-fees
- **Type:** Free web-based calculator
- **Zonal value data:** 1.96M records (per Wave 2 zonal-value-lookup analysis)

### Capabilities

**Inputs required:**
1. Seller type: Individual (capital asset) / Individual-Rented (ordinary asset) / Corporation/Developer (ordinary asset)
2. Property value: Gross selling price OR desired net proceeds
3. BIR Zonal Value (optional, with lookup capability)
4. Broker commission percentage (selectable 3–8% range)

**Outputs computed:**
- CGT: 6% (capital assets)
- VAT: 12% (ordinary assets — rented or corporate)
- EWT/CWT: 6% (ordinary assets — simplified flat rate)
- DST: 1.5%
- Transfer tax: 0.5% (provincial) / 0.75% (Metro Manila)
- Registration fees and notarial fees (~1%)
- Broker commission
- Separate seller/buyer cost breakdowns
- Estimated net proceeds

**Strengths:**
- Best-in-class UI for simple closing cost estimation
- Correctly distinguishes capital vs ordinary asset tax treatment
- Separate seller/buyer breakdowns
- Some zonal value data available

**Limitations:**
- No CWT rate tiering (uses flat 6%; misses 1.5%/3%/5% tiers for habitually engaged sellers)
- No installment sale handling (25% test, per-collection schedules)
- No DST on mortgage (Section 195)
- No RPT computation
- No Form 2307/1706/1606/2000-OT generation
- No alphalist/DAT file generation
- No EWT rate classification for non-property payments
- No principal residence exemption calculation
- Zonal value lookup appears manual (not automated comparison with assessor FMV and selling price)
- No BIR filing integration
- No API

**Assessment:** Best simple calculator available for Philippine real estate closing costs. Adequate for ballpark estimates on straightforward cash sales. Inadequate for complex transactions (installments, tiered CWT, mortgage DST, VAT recognition schedules, exemptions).

---

## 5.8. REN.PH (Real Estate Network Philippines)

### Profile

- **URL:** https://ren.ph/tools/zonal-value
- **Type:** Free web-based real estate toolkit

### Capabilities

**BIR Zonal Value Lookup:**
- 73 provinces, 1,441 cities, 33,633 barangays, 233,307 zone records
- Search by city or barangay
- Shows residential, commercial, and industrial values per sqm
- Most comprehensive free zonal value lookup tool found (by barangay count)

**Transfer Tax Calculator:**
- CGT: 6%
- DST: 1.5%
- Transfer tax: 0.5–0.75% (LGU-dependent)

**Due Diligence Checklist:**
- Property verification guide resource

**Limitations:**
- No CWT computation or rate tiering
- No installment sale/VAT schedule
- No DST on mortgage
- No RPT computation
- No EWT classification
- No Form 2307/alphalist generation
- No API (web-only)
- Zonal value data may not be current (BIR updates every 3–5 years)

**Assessment:** Strong zonal value lookup (233K records with barangay-level resolution). Basic transfer tax calculator. No computation depth. No API. Primary value is as a data source for the foundational zonal value input.

---

## 5.9. LandValuePH (landvalueph.com)

### Profile

- **URL:** https://www.landvalueph.com/
- **Type:** Web-based property valuation and tax tool
- **Coverage:** 200+ cities
- **Pricing:** Freemium; services from PHP 399

### Capabilities

- Zonal value lookup (BIR-sourced data)
- Selling Cost Calculator
- Capital Gains Tax Calculator
- Estate Tax Calculator
- Market value estimation (zonal + 8 market factors)
- "How Much Is My Land Worth?" tool

**Limitations:** No CWT tiering, no installment VAT, no DST on mortgage, no RPT with LGU database, no EWT classification, no BIR form generation, no API.

**Assessment:** Property valuation focus with tax computation as secondary feature. Useful for estate tax and market value estimation. Not a compliance tool.

---

## 5.10. RealValueMaps (realvaluemaps.com)

### Profile

- **URL:** https://realvaluemaps.com/calculator
- **Type:** Zonal value database + property tax calculator
- **Coverage:** 2.7M+ property records, 42,011 barangays, 121 RDOs — **largest zonal value database found**

### Capabilities

- BIR zonal value lookup (most comprehensive)
- Property tax calculator (details limited in public documentation)

**Limitations:** No API documented. No complex computation engine. Web-only.

**Assessment:** Most comprehensive zonal value data source by record count (2.7M vs REN.PH's 233K vs LandValuePH's 200+ cities). Primary value is data, not computation.

---

## 5.11. FileDocs Phil (filedocsphil.com)

### Profile

- **URL:** https://www.filedocsphil.com/
- **Type:** Full-service document processing agency (human-mediated, not software)
- **Contact:** (+63) 917 149 2337

### Services

- Title transfer processing
- eCAR processing
- CGT and DST filing assistance (BIR Form 1706, Form 2000-OT)
- Real property tax payment assistance
- Property due diligence
- Cancellation of encumbrance
- Correction and annotation of property titles
- Issuance of lost titles
- Zonal value information (blog/educational content)

**Assessment:** This is a **services company**, not a software tool. They handle the manual computation, filing, and compliance on behalf of clients. No self-service computation tools, no API, no automation exposed to end users. Competes with law firms and title facilitation agencies, not with software products.

---

## 6. Generic ERPs (Xero, QuickBooks, SAP)

- **Xero:** Used in Philippines via JuanTax integration for BIR compliance. No native PH tax computation. Xero handles bookkeeping; JuanTax handles tax forms. Partial payment VAT recognition issue documented.
- **QuickBooks:** Philippines edition exists but no BIR eTSP accreditation. Basic VAT/withholding tax codes. No real estate transaction tax features.
- **SAP:** Enterprise-grade but requires extensive PH localization. Large companies (e.g., Ayala Land, SM) likely have custom SAP modules for real estate taxes, but these are proprietary and not commercially available.

---

## 7. Additional Niche / Emerging Tools

| Tool | Focus | Real Estate Tax Coverage |
|------|-------|------------------------|
| **ZonalValueFinderPH** (zonalvaluefinderph.com) | Zonal value lookup | Database of zonal values. Lookup interface only — no API, no computation engine. |
| **OwnPropertyAbroad** (ownpropertyabroad.com) | Expat property investment | CGT calculator, RPT calculator. Basic web tools for foreigners. |
| **TaxCalculatorPhilippines.online** | General PH tax info | Income tax, RPT guides. Blog-style educational, not computation engine. |
| **Clevrr.ph** (clevrr.ph/calculators) | Real estate investment | Commission, rental yield, ROI, sqm conversion. Investment metrics, not tax compliance. |
| **ForeclosurePhilippines** | Foreclosed property listings | Has CGT/CWT calculators as blog tools. Basic web calculators only. |
| **BIR Withholding Tax Calculator** (bir.gov.ph/wtcalculator) | Compensation withholding | Official BIR tool. Salary/compensation-focused, not EWT/CWT on property. |
| **JuanTax Academy** | Education | Webinars on estate tax, transfer tax. No computation tools. |
| **AutoCount** | BIR-accredited POS + CAS | Dual BIR accreditation (POS + CAS). Strong in Visayas/Mindanao retail/F&B. No real estate tax features. |

---

## 8. Feature Coverage Gap Matrix (Expanded)

**Legend:** FULL = automated computation + filing; FORM = filing only (user computes); PARTIAL = some automation; CALC = simple calculator (no filing, no edge cases); INTERNAL = BIR officer uses internally (not self-service); NONE = not available; N/A = not within tool's purpose

| Computation | JuanTax | Taxumo | QNE Cloud | eONETT | Housal | REN.PH | LandValuePH | RealValueMaps | Gap Severity |
|-------------|---------|--------|-----------|--------|--------|--------|-------------|---------------|-------------|
| Highest-of-three base | PARTIAL (manual input) | NONE | NONE | INTERNAL | PARTIAL (user inputs) | NONE | NONE | NONE | **VERY HIGH** |
| CGT (6%) | FORM | NONE | NONE | INTERNAL | CALC | CALC | CALC | NONE | **HIGH** |
| DST on sale (1.5%) | FORM | NONE | NONE | INTERNAL | CALC | CALC | NONE | NONE | **HIGH** |
| DST on mortgage (Sec 195) | FORM | NONE | NONE | NONE | NONE | NONE | NONE | NONE | **VERY HIGH** |
| VAT on real property | PARTIAL | NONE | PARTIAL (general VAT) | NONE | CALC (toggle) | NONE | NONE | NONE | **HIGH** |
| Installment VAT schedule | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | **VERY HIGH** |
| CWT rate/timing (1.5-6%) | FORM | NONE | NONE | INTERNAL | NONE | NONE | NONE | NONE | **VERY HIGH** |
| EWT rate classification | FULL (manual ATC) | PARTIAL | FULL (manual ATC) | N/A | NONE | NONE | NONE | NONE | **LOW** |
| VAT reconciliation (2550Q) | PARTIAL (EWT Analysis) | PARTIAL | FULL | N/A | NONE | NONE | NONE | NONE | **LOW** |
| Form 2307 generation | FULL | PARTIAL | FULL | N/A | NONE | NONE | NONE | NONE | **LOW** |
| Alphalist (1604-C/E/F) | FULL | NONE | FULL (DAT files) | N/A | NONE | NONE | NONE | NONE | **LOW** |
| SAWT generation | FULL | PARTIAL | FULL (DAT files) | N/A | NONE | NONE | NONE | NONE | **LOW** |
| QAP generation | FULL | PARTIAL | FULL (DAT files) | N/A | NONE | NONE | NONE | NONE | **LOW** |
| RPT computation | NONE | NONE | NONE | NONE | NONE | NONE | NONE | NONE | **VERY HIGH** |
| Transfer tax | NONE | NONE | NONE | NONE | CALC (0.5-0.75%) | CALC | NONE | NONE | **HIGH** |
| Zonal value lookup | NONE | NONE | NONE | INTERNAL | PARTIAL (1.96M records) | YES (233K records) | YES (200+ cities) | YES (2.7M records) | **HIGH** (data exists; no API) |

---

## 9. Key Findings

### What JuanTax Does Well
1. **Recurring BIR compliance** — monthly/quarterly/annual forms for VAT, EWT, compensation, income tax are well-automated
2. **Form 2307 / SAWT / QAP / Alphalist generation** — strong automation from transaction entry to form population
3. **EWT analysis** — cross-check EWT vs VAT for reconciliation (Plus only)
4. **E-filing and e-payment** — direct BIR submission with multiple payment channels
5. **Xero integration** — bidirectional sync for tax code automation
6. **API exists** — REST API with OAuth 2.0, sandbox environment; though endpoint coverage is very limited (only 1601-C and 2551Q documented)

### What JuanTax Does NOT Do (Critical Gaps)

1. **No zonal value lookup** — the foundational data dependency for all real estate tax computations. User must independently source zonal values.
2. **No "highest-of-three" tax base resolution** — user determines which value (SP, ZV, AFMV) is highest and enters it. No automated comparison.
3. **No installment VAT per-collection tracking** — the 25% initial payment test and multi-period VAT recognition schedule are completely unaddressed by any tool.
4. **No ONETT workflow automation** — Forms 1706, 1606, 2000-OT are available for filing, but the computation logic (tax base determination, rate selection, deadline calculation) is entirely manual.
5. **No LGU tax computation** — RPT and transfer tax are outside scope entirely (BIR-only platform).
6. **No CWT rate auto-determination** — "habitually engaged" test (6-transaction rule), tiered rate selection (1.5%/3%/5%/6%), and installment timing logic are not automated.
7. **No e-payment for Form 1706** — CGT must still be paid via RCO at RDO, even when filed through Fast File.
8. **Partial payment VAT recognition bug** — Xero-integrated service companies cannot properly recognize VAT on partial payments (documented user complaint).

### The Competitive Landscape Has a Massive Structural Hole

**No Philippine tax software automates real estate transaction tax computation.** The ecosystem splits cleanly into three tiers, none of which serve the full need:

**Tier 1 — Accounting/Compliance Software (QNE, JuanTax, Taxumo):**
- Built around **recurring business tax compliance** (monthly VAT, quarterly EWT, annual income tax)
- Period-based architecture (monthly/quarterly/annual filing cycles)
- Strong on Form 2307, SAWT, QAP, alphalists, 2550Q — the recurring compliance stack
- Zero coverage of one-time real property transaction taxes (CGT, DST on property, CWT on property, transfer tax)
- QNE has the best multifunction output (single entry → ledger + trial balance + BIR forms + DAT files)
- JuanTax has the best tax filing capability (eFPS-equivalent direct BIR submission) and the only documented public API

**Tier 2 — BIR eONETT:**
- The government's own ONETT workflow system
- Handles CGT, DST, CWT computation — but **officer-mediated, not self-service**
- Taxpayer submits documents and waits for BIR officer review (2–8 weeks reported)
- No public computation logic, no API, no way for practitioner to pre-compute and verify
- Key value: it IS the authoritative computation — but it is a bottleneck, not a tool

**Tier 3 — Web Calculators (Housal, REN.PH, LandValuePH):**
- Simple flat-rate arithmetic (6%, 1.5%, 0.5–0.75%)
- Housal is the best-in-class closing cost estimator
- REN.PH has the best free zonal value lookup (233K zone records at barangay level)
- RealValueMaps has the largest zonal database (2.7M records) but limited computation
- None handle: installment sales, CWT rate tiering, mortgage DST, multi-period VAT, exemptions
- No BIR filing capability, no API, no form generation

**The gap between tiers is enormous.** There is no tool that:
1. Resolves the highest-of-three tax base automatically (with zonal value lookup)
2. Fans out to 4–5 taxes with correct rates, deadlines, and forms
3. Handles installment sale complexity (25% test, per-collection schedules, FMV-ratio VAT)
4. Generates BIR forms (1706, 1606, 2000-OT) with correct data
5. Tracks the eCAR prerequisite chain (CGT + DST + CWT paid → eCAR application)

### Zonal Value: The Infrastructure Bottleneck

Zonal value lookup is the foundational dependency for all real estate transaction taxes. Current state:
- **BIR:** No public API. 124 heterogeneous Excel workbooks published as ZIP files. Format inconsistency across RDOs. 38% of schedules outdated (DOF 2024 estimate). Image-based PDFs in some RDOs requiring OCR.
- **RealValueMaps:** 2.7M records, 42,011 barangays, 121 RDOs — largest database. No API documented.
- **REN.PH:** 233,307 zone records across 33,633 barangays — best free lookup. No API.
- **Housal:** 1.96M records. No API.
- **LandValuePH:** 200+ cities. No API.
- **RPVARA transition (RA 12001):** BIR zonal values will transition to BLGF Standard Market Values by mid-2026. Three-way max will collapse to two-way max. This creates both disruption risk and first-mover opportunity for any tool that tracks the transition.

**Key insight:** The data exists in fragmented third-party databases but no one offers a programmatic API. Whoever builds a comprehensive, API-accessible zonal value database creates the foundational infrastructure layer for all real estate tax computation.

### What ZERO Tools Cover (Absolute Gaps)

1. **DST on mortgage** (Section 195 stepped schedule) — 0 tools compute the post-TRAIN stepped rate
2. **Installment VAT schedule** (multi-period per-collection recognition with dual formula) — 0 tools
3. **CWT rate tiering** (1.5/3/5/6% based on seller classification + installment timing + buyer type) — 0 self-service tools
4. **RPT with full LGU database** (assessment levels + enacted rates for 1,700+ LGUs) — 0 comprehensive tools
5. **Automated highest-of-three resolution** (with zonal lookup + assessor FMV + selling price comparison) — 0 fully automated tools

### Platform Architecture Implications

All existing platforms (QNE, JuanTax, Taxumo) are **period-based** — they organize work around monthly/quarterly/annual filing cycles. Real estate tax computation requires a **transaction-centric** engine:

1. **Single transaction → multiple taxes:** One property sale triggers CGT (or CWT+VAT), DST, transfer tax — each with different rates, forms, deadlines, and payers
2. **Tax base computed once, consumed five times:** The highest-of-three resolution feeds all transaction taxes
3. **Multi-period tracking:** Installment sales create per-collection VAT and CWT schedules spanning months or years
4. **Prerequisite chain:** CGT/CWT → DST → eCAR → Transfer Tax → Registry of Deeds — sequential dependencies with different agencies
5. **Buyer/seller/broker trilateral:** Different parties responsible for different taxes in the same transaction

This is a fundamentally different product architecture than what any Philippine competitor has built. The closest analog is the BIR's own eONETT system, but eONETT is officer-mediated with no self-service computation.

---

## Sources

### JuanTax
- [JuanTax Official Site](https://juan.tax/)
- [JuanTax Plus Features](https://plus.juan.tax/features/)
- [JuanTax Plus Pricing](https://plus.juan.tax/pricing/)
- [JuanTax Fast File Pricing](https://fastfile.juan.tax/pricing/)
- [Juan Accounting Pricing](https://www.juan.ac/pricing)
- [JuanTax Developer Portal](https://developer.juan.tax/)
- [JuanTax Help Center - EWT Analysis](https://help.juan.tax/en/articles/128-ewt-analysis)
- [JuanTax Help Center - Form 1706](https://help.juan.tax/en/articles/57-generating-bir-form-1706-in-fast-file)
- [JuanTax Help Center - Form 1606](https://help.juan.tax/en/articles/56-generating-bir-form-1606-in-fast-file)
- [JuanTax Help Center - Form 2000-OT](https://help.juan.tax/en/articles/5465494-generating-bir-form-2000-ot-in-fast-file)
- [JuanTax Blog - BIR Form 1604-C](https://juan.tax/blog/bir-form-1604-c-annual-information-return-of-income-taxes-withheld-on-compensation/)
- [JuanTax Blog - BIR Form 2307](https://juan.tax/blog/bir-form-2307/)
- [JuanTax Blog - Fast File vs eFPS](https://juan.tax/blog/tax-compliance-e-solutions-juantax-fast-file-vs-bir-efps/)
- [JuanTax Blog - Revenue Regulations No. 21-2020](https://juan.tax/blog/revenue-regulations-no-21-2020/)
- [JuanTax Xero App Store Reviews](https://apps.xero.com/ph/app/juan-tax/reviews)
- [Juan Accounting Features](https://www.juan.ac/features)
- [Wavemaker Ventures - JuanTax/Jaz Merger Announcement](https://wavemaker.vc/juantax-and-jaz-philippines-merge-to-launch-first-ai-driven-accounting-software-in-the-philippines/)

### QNE Cloud / QNE Optimum
- [QNE Cloud Philippines](https://qne.cloud/ph/)
- [QNE BIR Accounting Software](https://qne.cloud/ph/bir-accounting-software/)
- [QNE Support Solutions](https://support.qne.com.ph/support/solutions)
- [QNE Withholding Tax Setup](https://support.qne.com.ph/support/solutions/articles/35000214030-how-to-set-up-withholding-tax-codes-in-qne-ai-cloud)
- [QNE BIR SAWT](https://qne.cloud/ph/bir-sawt/)
- [QNE VAT and WTAX Modules](https://support.qne.com.ph/support/solutions/folders/35000230823)
- [QNE BIR Form 1601-EQ](https://support.qne.com.ph/support/solutions/articles/35000199957-how-to-generate-bir-1601-eq-form)
- [QNE BIR Form 2550](https://support.qne.com.ph/support/solutions/articles/35000183307-how-to-generate-bir-2550)
- [QNE Quarterly Alphalist of Payees](https://qne.cloud/ph/quarterly-alphalist-of-payees/)
- [QNE Expanded Withholding Tax](https://qne.cloud/ph/expanded-withholding-tax-philippines/)
- [QNE eBIR Forms](https://qne.cloud/ph/ebir-forms-latest-version/) (redirected from qne.com.ph)
- [QNE eFPS Guide](https://qne.cloud/ph/bir-efps/)
- [QNE BIR Monthly Deadline](https://qne.cloud/ph/bir-monthly-deadline/) (redirected from qne.com.ph)
- [QNE Accounting Software Philippines Price](https://qne.cloud/ph/accounting-software-philippines-price/) (redirected from qne.com.ph)
- [QNE Business Software for SMEs](https://qne.cloud/ph/business-software-smes/) (redirected from qne.com.ph)
- [QNE Top 5 Accounting Software Philippines 2026](https://qne.cloud/ph/top-5-accounting-software-philippines-for-2026/)
- [QNE Tax Software Philippines](https://qne.cloud/ph/tax-software-philippines/)

### QNE Reviews
- [HashMicro - QNE Accounting Review 2025](https://www.hashmicro.com/ph/blog/qne-accounting-review/)
- [GetApp - QNE Accounting Software 2026](https://www.getapp.com/finance-accounting-software/a/qne-software/)
- [Capterra - QNE Accounting Software](https://www.capterra.com/p/180077/QNE-Accounting-Software/)
- [SoftwareAdvice - QNE Accounting Software 2026](https://www.softwareadvice.com/accounting/qne-accounting-profile/)
- [SoftwareSuggest - QNE Accounting](https://www.softwaresuggest.com/qne)
- [SoftwareFinder - QNE Accounting](https://softwarefinder.com/accounting-software/qne-accounting)

### BIR Systems
- [BIR eONETT Portal](https://eonett.bir.gov.ph/)
- [BIR eONETT User Guide](https://eonett.bir.gov.ph/Guide/User-Guide-TP.pdf)
- [AJA Law - BIR Digital Transformation: eONETT and ORUS](https://www.ajalaw.ph/bir-digital-transformation-eonett-orus/)
- [PwC - eONETT Convenient Way to Secure eCAR](https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2023/eonett-a-more-convenient-way-to-secure-an-ecar.html)
- [Forvis Mazars - BIR RMC 10-2023 eONETT](https://www.forvismazars.com/ph/en/insights/tax-alerts/bir-rmc-10-2023)
- [BIR eBIRForms](https://www.bir.gov.ph/ebirforms)
- [BIR Withholding Tax Calculator](https://www.bir.gov.ph/wtcalculator)
- [BIR Zonal Values](https://www.bir.gov.ph/zonal-values)
- [Global Law Experts - BIR ORUS Available](https://globallawexperts.com/birs-orus-is-now-available/)
- [Triple-i Consulting - Mastering BIR ORUS](https://www.tripleiconsulting.com/mastering-bir-orus-streamlined-tax-registration-for-philippine-businesses/)

### Real Estate Tax Tools
- [Housal Closing Cost Calculator](https://www.housal.com/calculators/sales-closing-fees)
- [REN.PH Zonal Value Lookup](https://ren.ph/tools/zonal-value)
- [LandValuePH](https://www.landvalueph.com/)
- [LandValuePH Zonal Value Directory](https://www.landvalueph.com/zonal-value)
- [RealValueMaps Calculator](https://realvaluemaps.com/calculator)
- [OwnPropertyAbroad CGT Calculator](https://ownpropertyabroad.com/philippines/capital-gains-tax-calculator-philippines/)
- [OwnPropertyAbroad RPT Calculator](https://ownpropertyabroad.com/philippines/philippines-real-property-tax-calculator-rpt/)
- [ZonalValueFinderPH](https://zonalvaluefinderph.com/bir-zonal-values)

### Service Companies
- [FileDocs Phil - CGT vs DST](https://www.filedocsphil.com/capital-gains-tax-cgt-vs-documentary-stamp-tax-dst/)
- [FileDocs Phil - Real Property Tax](https://www.filedocsphil.com/real-property-tax-philippines/)
- [FileDocs Phil - BIR Zonal Value](https://www.filedocsphil.com/how-to-look-for-bir-zonal-value/)

### Other
- [Manila Bookkeepers - Top Accounting and Tax Software 2025](https://manilabookkeepers.com/blog/top-accounting-tax-software-in-2025/)
- [Manila Bookkeepers - Digital Tax Filing Philippines](https://manilabookkeepers.com/blog/digital-tax-filing-philippines/)
- [Opulent Business - Cloud Accounting for Small Businesses Philippines](https://opulentbiz.com/ph/cloud-accounting-software-for-small-businesses-in-the-philippines/)
- [AutoCount BIR Accreditation](https://www.macaubusiness.com/autocount-pos-achieves-bir-accreditation-simplifying-tax-for-philippine-smes-and-driving-growth/)
- [Taxumo Blog - Philippine Tax Calculator 2025](https://www.taxumo.com/blog/philippine-tax-calculator-2025-updated-tax-rates-and-how-to-compute/)
- [ACE Consulting - QNE Software](https://ace-cis.com/qne-software/)
