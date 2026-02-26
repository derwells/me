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

## 4. QNE Cloud (qne.cloud/ph)

### Company Profile

- Full accounting software (not tax-filing-only) with BIR compliance module
- Targets companies needing integrated bookkeeping + tax filing
- Supports BIR CAS (Computerized Accounting Software) registration
- Philippine-localized

### Coverage Assessment

- **Core focus:** General ledger, AP/AR, inventory, payroll, BIR compliance
- **Tax forms:** Standard BIR forms for recurring compliance (VAT, EWT, compensation)
- **Real estate transaction taxes:** No specific real property transaction modules documented
- **Zonal value lookup:** Not available
- **ONETT/one-time transactions:** Not documented as a feature
- **LGU taxes:** Not covered
- **RPT computation:** Not covered

**Assessment:** QNE is a broader accounting platform with tax compliance as a module. Its competitive advantage is in full-cycle accounting (GL → trial balance → BIR forms), not in real estate transaction tax computation. No evidence of ONETT, zonal value, or real property tax features.

---

## 5. Generic ERPs (Xero, QuickBooks, SAP)

- **Xero:** Used in Philippines via JuanTax integration for BIR compliance. No native PH tax computation. Xero handles bookkeeping; JuanTax handles tax forms. Partial payment VAT recognition issue documented.
- **QuickBooks:** Philippines edition exists but no BIR eTSP accreditation. Basic VAT/withholding tax codes. No real estate transaction tax features.
- **SAP:** Enterprise-grade but requires extensive PH localization. Large companies (e.g., Ayala Land, SM) likely have custom SAP modules for real estate taxes, but these are proprietary and not commercially available.

---

## 6. Niche / Emerging Tools

| Tool | Focus | Real Estate Tax Coverage |
|------|-------|------------------------|
| **Housal** (housal.com) | Real estate closing cost calculator | Computes CGT, DST, transfer tax, agent commission. Has some zonal value data (1.96M records). Web calculator only — no API, no filing, no BIR integration. |
| **ZonalValueFinderPH** | Zonal value lookup | Database of zonal values. Lookup interface only — no API, no computation engine. |
| **LandValuePH** (landvalueph.com) | BIR zonal value reference | Per-city/barangay zonal value display. No API. |
| **ForeclosurePhilippines** | Foreclosed property listings | Has CGT/CWT calculators as blog tools. Basic web calculators only. |
| **JuanTax Academy** | Education | Webinars on estate tax, transfer tax. No computation tools. |

---

## 7. Feature Coverage Gap Matrix

**Legend:** FULL = automated computation + filing; FORM = filing only (user computes); PARTIAL = some automation; NONE = not available

| Computation | JuanTax | Taxumo | QNE Cloud | Housal | Gap Severity |
|-------------|---------|--------|-----------|--------|-------------|
| Highest-of-three base | PARTIAL (manual input) | NONE | NONE | PARTIAL (basic calc) | **HIGH** |
| CGT (6%) | FORM | NONE | NONE | PARTIAL (calc only) | **HIGH** |
| DST on sale (1.5%) | FORM | NONE | NONE | PARTIAL (calc only) | **HIGH** |
| DST on mortgage | FORM | NONE | NONE | NONE | **MEDIUM** |
| VAT on real property | PARTIAL | NONE | NONE | NONE | **HIGH** |
| Installment VAT schedule | NONE | NONE | NONE | NONE | **VERY HIGH** |
| CWT rate/timing | FORM | NONE | NONE | NONE | **HIGH** |
| EWT rate classification | FULL (with manual payee classification) | PARTIAL | PARTIAL | NONE | **LOW** |
| VAT reconciliation | PARTIAL (EWT Analysis) | PARTIAL | PARTIAL | NONE | **MEDIUM** |
| Form 2307 generation | FULL | PARTIAL | PARTIAL | NONE | **LOW** |
| Alphalist (1604-C/E/F) | FULL | NONE | PARTIAL | NONE | **LOW** |
| RPT computation | NONE | NONE | NONE | NONE | **VERY HIGH** |
| Transfer tax | NONE | NONE | NONE | PARTIAL (calc only) | **HIGH** |
| Zonal value lookup | NONE | NONE | NONE | PARTIAL (data, no API) | **VERY HIGH** |

---

## 8. Key Findings

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

### The Competitive Landscape Has a Massive Hole

**No Philippine tax software automates real estate transaction tax computation.** All existing tools (JuanTax, Taxumo, QNE) are built around recurring business tax compliance (monthly VAT, quarterly EWT, annual income tax). The one-time transaction (ONETT) workflow — which involves CGT, DST, CWT, VAT, transfer tax, and the zonal value lookup that feeds them all — is entirely unserved by automation.

The closest competitor is Housal's closing cost calculator, which does basic arithmetic but:
- Has no BIR filing capability
- Has no API
- Has no installment tracking
- Does not handle edge cases (exemptions, installment CWT timing, FMV-ratio VAT)
- Cannot generate Form 1706/1606/2000-OT

### Platform Architecture Implications

JuanTax's architecture is fundamentally **period-based** (monthly/quarterly/annual filing cycles), not **transaction-based** (one-time event → multi-form → multi-deadline). Real estate tax computation requires a transaction-centric engine that:
1. Resolves the tax base once (highest-of-three)
2. Fans out to 4-5 taxes with different rates, deadlines, and forms
3. Tracks installment schedules over multiple periods
4. Produces the eCAR package (CGT + DST + CWT paid → eCAR application)

This is a fundamentally different product architecture than what JuanTax (or any Philippine competitor) has built.

---

## Sources

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
- [Housal Closing Cost Calculator](https://www.housal.com/calculators/sales-closing-fees)
- [Manila Bookkeepers - Top Accounting and Tax Software 2025](https://manilabookkeepers.com/blog/top-accounting-tax-software-in-2025/)
