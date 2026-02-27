# Practitioner Workflow Analysis — PH Real Estate Computations (Full Sales Lifecycle + All Categories)

## Summary

This analysis documents the actual workflows practitioners use for ALL 16 computation categories identified in Wave 2, organized across two complementary views: (A) per-computation deep-dives (Sections 1-8) covering who performs each computation, tools, workflows, pain points, and standardization; and (B) full developer sales lifecycle mapping (Appendix A) showing where each computation occurs across the 6 stages from pre-sale through post-turnover. Research synthesized from 130+ web sources including developer guides (DMCI, SMDC, Ayala Land, Megaworld, Federal Land), practitioner platforms (iRealtee, Filipinohomes, HousingInteractive), government portals (Pag-IBIG Fund, BIR, DHSUD, LRA), financial institutions (BDO, BPI, Metrobank, RCBC), legal commentaries (Respicio & Co., ATTYDPLaw), and real estate technology analyses.

**Key finding:** Philippine real estate computations are performed by a fragmented ecosystem of practitioners — brokers, developer sales agents, Pag-IBIG loan processors, property managers, lawyers, and buyers themselves — using predominantly manual methods. The dominant tools are phone calculators, Excel/Google Sheets with custom-built templates (no standardization), developer-provided PDF computation sheets, and a small number of PH-native web calculators (Housal, Clevrr, Pag-IBIG online calculator). No single tool handles the full computation chain for any transaction type. The ecosystem is an "amortization monoculture" — 15+ tools compute basic mortgage amortization while the regulatory compliance layer is completely unserved (8 of 16 computations have ZERO tool coverage).

**Pain point clusters:** (a) no single tool handles the full computation chain, (b) tax and regulatory rules change frequently and practitioners miss updates, (c) multi-variable computations (especially those requiring zonal value lookups or tiered rates) have the highest error rates, (d) pre-sale sample computation generation under time pressure requires maintaining separate templates per developer with no unified tool, (e) equity-to-loan-takeout restructuring handoff takes 10+ working days and blocks deal progression, (f) multi-tier commission splits across 49+ plan variations are error-prone in spreadsheets.

**Strongest automation opportunities (from lifecycle analysis):**
1. Pre-sale computation generation (Stage 1) — every buyer interaction requires it; no unified multi-developer tool
2. Regulatory compliance computations (Stages 3, 5, 6) — zero tool coverage for 8 computations
3. Closing cost aggregation (Stage 5) — 5+ separate fee/tax computations with no single-pass tool

---

## 1. BP 220 Compliance Check Process

### Who Performs It
- **Licensed architects and engineers** during project design
- **DHSUD (formerly HLURB) examiners** during permit review
- **DHSUD inspectors** during periodic site inspections

### Tools/Methods Used
- **Manual checklist against IRR tables** — architects cross-reference floor areas, lot areas, open spaces, setbacks, parking ratios, and ceiling heights against prescribed minimums in the BP 220 Revised IRR (2008)
- **CAD software** for dimensional compliance (AutoCAD, SketchUp) — but compliance checking itself is manual comparison
- **No known automated compliance-check tool** — the architect/engineer must manually verify each parameter
- Submitted plans are **signed and sealed** by the licensed professional who certifies compliance under oath

### Step-by-Step Workflow
1. Architect designs project to BP 220 standards (socialized: 18 sqm min floor area; economic: 22 sqm; lot areas per Table 7; frontages per Table 8)
2. Architect prepares compliance documentation: floor area calculations, open space percentages, parking computations, setback dimensions
3. Developer submits plans + Program of Development (signed/sealed by licensed professional) to DHSUD for Integrated Approval
4. DHSUD examiner reviews plans against IRR parameters — this is a **manual review of submitted documents**
5. If approved, Certificate of Registration (CR) and License to Sell (LTS) are issued
6. Post-approval: DHSUD conducts periodic site inspections verifying road widths, open spaces, drainage, building code compliance
7. Non-compliance triggers show cause orders, CDOs, fines (2% daily), or license revocation

### Pain Points
- **Entirely manual compliance verification** — no software automates the BP 220 parameter check
- **Multiple overlapping codes** — BP 220 compliance must also cross-reference National Building Code, Fire Code, Accessibility Law, Philippine Structural Code, Electrical Code, and Sanitation Code
- **Floor area layering complexity** — JMC updates layer different minimum floor areas (18/24/26/27/28/32 sqm) depending on housing type and vintage of the applicable circular
- **Open space computation ambiguity** — setback percentages differ by lot type (corner, through, bounded by public space) and housing classification
- **No digital submission pipeline** — plans are physical documents reviewed in-person

### Standardization
- Standards are nationally standardized via the BP 220 IRR (2008) and subsequent DHSUD amendments
- However, **compliance checking is not standardized** — each architect/examiner does it manually with no uniform checklist tool
- DHSUD's Integrated Approval System is a process standard, not a computation tool

---

## 2. DHSUD Socialized Housing Price Ceiling Verification

### Who Performs It
- **Developers** when pricing socialized housing units
- **DHSUD** when reviewing License to Sell applications
- **Pag-IBIG Fund** when evaluating loan eligibility for socialized housing
- **Buyers/brokers** when verifying unit classification

### Tools/Methods Used
- **Manual lookup of current JMC** — practitioners reference the latest Joint Memorandum Circular (currently JMC 2025-001) for maximum selling prices
- **No automated tool** — price ceiling verification is a simple comparison but requires knowing the correct circular and the correct housing classification
- Developer pricing teams maintain **internal spreadsheets** mapping unit types to ceiling limits

### Step-by-Step Workflow
1. Developer determines housing classification (socialized Level 1-A/1-B/2/3, low-cost, medium-cost)
2. Developer looks up applicable price ceiling from latest JMC (e.g., JMC 2025-001: horizontal ≤26 sqm at ₱844,440; ≥27 sqm at ₱950,000; vertical at ₱1,800,000)
3. Unit price is set at or below ceiling
4. 30% ATI (Affordability-to-Income) ratio check: monthly amortization must not exceed 30% of target buyer's gross family income
5. DHSUD reviews pricing during LTS application — cross-references declared selling price against current ceiling
6. Post-2025: ceilings are updated every 2-3 years per RA 11201

### Pain Points
- **Ceiling updates are infrequent but irregular** — practitioners often work with outdated figures
- **Multiple classification tiers** with overlapping boundaries — Level 1-A (≤₱300K), 1-B (₱300K-₱500K), Level 2 (₱500K-₱1.25M), Level 3 (₱1.25M-₱3M), low-cost (to ₱4.9M), medium-cost (to ₱6.6M)
- **Floor area-price interaction** — the 2025 JMC introduced floor-area-dependent ceilings (different caps for ≤26 sqm vs ≥27 sqm), adding a computation dimension
- **No single authoritative lookup tool** — practitioners must track JMC publication dates and effectivity

### Standardization
- Nationally standardized via JMC issuances
- However, practitioners must manually track which JMC is current — no digital tool provides this automatically

---

## 3. Property Assessment Level Computation (LGU Assessor)

### Who Performs It
- **Municipal/City Assessor** — primary computation authority
- **Provincial Assessor** — technical supervision and coordination
- **Property owners** — compute their own RPT for budgeting (using published rates)

### Tools/Methods Used
- **Manual/spreadsheet computation** in most LGUs — assessor manually applies FMV × Assessment Level
- **RPTAS (Real Property Tax Administration System)** — a specialized LGU software product from Infoman Inc., adopted by some LGUs but far from universal
- **eFAAS (Electronic Field Appraisal and Assessment Sheet)** — BLGF-developed computerized system for low-income LGUs, replacing manual tax declarations
- **Paper-based records** — many LGUs still maintain property records manually with physical tax declarations
- **Schedule of Market Values (SMV)** — LGU-published tables (land per sqm by location; buildings per sqm by type)

### Step-by-Step Workflow
1. Property owner files sworn declaration with assessor within 60 days of acquisition/improvement
2. Assessor classifies property (residential, agricultural, commercial, industrial, mineral, timberland, special)
3. Assessor determines FMV using the LGU's Schedule of Market Values (SMV):
   - **Land**: Market Data Approach, Income Capitalization, or Cost Approach
   - **Buildings**: Replacement Cost New method (floor area × unit construction cost from DPWH tables)
4. Assessor applies classification-specific assessment level (percentage set by Sanggunian ordinance, within LGC Section 218 maximums)
5. Assessed Value = FMV × Assessment Level
6. Tax Declaration is issued to property owner
7. RPT = Assessed Value × Basic Rate (1% province / 2% Metro Manila) + SEF (1%)

### Pain Points
- **~60% of SMVs are outdated** across the country — some not revised in 10+ years
- **No comprehensive electronic database** — LGUs lack unified property information systems
- **Political interference** in property valuation — assessors face pressure to keep values low
- **Limited technical capacity** — many assessors lack formal appraisal training
- **Fragmented systems** — each LGU has its own SMV, assessment levels, and (often incompatible) software or paper systems
- **Three valuation bases never align** — BIR zonal value, LGU FMV, and actual market price are often vastly different
- **Assessment level brackets in LGC Section 218 haven't been inflation-adjusted since 1991** — the ₱175K/₱300K/₱500K/₱750K residential thresholds are frozen

### Standardization
- Legal framework is nationally standardized (LGC RA 7160, DOF LAR 1-92)
- **Implementation is radically non-standardized** — each LGU sets its own SMV, rates, and processes
- RA 12001 (RPVARA, signed June 2024) aims to create the Real Property Valuation Service (RPVS) with uniform Philippine Valuation Standards and a centralized RPIS database — but implementation is still in early stages

---

## 4. Building Depreciation Computation (Assessor)

### Who Performs It
- **Municipal/City Assessor** during improvement appraisal
- **Licensed appraisers** for bank collateral valuation
- **Assessor's office staff** when processing new declarations or general revisions

### Tools/Methods Used
- **Manual computation** using the straight-line (economic age-life) method
- **Assessor-prepared depreciation tables** — each LGU assessor is required to prepare a depreciation schedule for buildings by construction type
- **BLGF Manual on Real Property Appraisal and Assessment Operations** — provides methodology but each assessor implements it independently
- **DPWH unit construction cost data** — basis for Replacement Cost New per sqm
- **No known automated tool** for depreciation computation specific to Philippine assessor practice

### Step-by-Step Workflow
1. Determine building construction type (reinforced concrete, wood, mixed, etc.)
2. Look up Unit Construction Cost (per sqm) from assessor's building cost schedule (derived from DPWH data)
3. Calculate RCN = Total Floor Area × Unit Construction Cost
4. Determine effective age and economic life of building:
   - Economic life typically 35-50 years for reinforced concrete; less for wood/mixed
   - Effective age may differ from actual age based on maintenance/renovation
5. Calculate depreciation: Depreciation Rate = Effective Age ÷ Economic Life
   - Depreciation is normally **capped at 80%** (20% residual value)
6. FMV = RCN × (1 - Depreciation Rate)
7. Apply assessment level to get Assessed Value

### Pain Points
- **Depreciation tables vary by LGU** — no national standard table, each assessor prepares their own
- **Effective age vs. actual age confusion** — assessors often default to actual age rather than properly determining effective age based on condition
- **Economic life assumptions vary** — some LGUs use 20 years for buildings, others 50 years, depending on local practice
- **Unit construction costs often outdated** — derived from DPWH data that may lag behind actual construction costs by years
- **Three types of depreciation** (physical, functional, economic) are supposed to be considered, but in practice assessors typically only apply physical (age-based) depreciation
- **Government property special rules** add complexity — e.g., water districts assessed at 10% of depreciated value

### Standardization
- Methodology is standardized via BLGF Manual and DOF LAR 1-92
- **Actual depreciation tables are NOT standardized** — each LGU/assessor creates their own
- Philippine Valuation Standards (under development per RA 12001) will eventually standardize this

---

## 5. Registry of Deeds Registration Fee Computation

### Who Performs It
- **Registry of Deeds (RD) cashiering staff** — official computation
- **Lawyers/paralegals** handling title transfers — pre-compute to advise clients
- **Real estate brokers** — estimate during closing cost projections
- **Buyers** — self-compute using online tools

### Tools/Methods Used
- **LRA graduated fee table** — a fixed lookup table with brackets and incremental rates
- **LRA ERCF (Estimate Registration Computation Fees)** — official online tool at [lra.gov.ph/ercf](https://lra.gov.ph/ercf) that takes selling price input and returns estimated registration fee
- **Laminated tariff cards** at RD cashiering windows — for manual fee lookup
- **ForeclosurePhilippines.com calculator** — third-party online tool implementing the LRA fee table
- **Manual lookup** — RD staff consult the fee schedule and compute using calculator/spreadsheet

### Step-by-Step Workflow
1. Determine the tax base: higher of selling price, BIR zonal value, or LGU FMV
2. Secure Certificate Authorizing Registration (eCAR) from BIR (requires CGT and DST paid first)
3. Submit complete documents to Registration Information Officer (RIO) at RD
4. RD staff computes registration fee using the LRA graduated table
5. Claim Assessment Slip (CAS) is issued with computed fee
6. Pay at RD cashier; receive Official Receipt
7. Entry Clerk processes the transfer; new TCT is issued

### Pain Points
- **Sequential dependency** — registration fees can only be paid AFTER BIR taxes are paid and eCAR is issued, creating bottlenecks
- **eCAR issuance delays** — BIR processing of eCAR can take weeks to months, blocking the entire registration process
- **2-year eCAR validity** — if RD registration is delayed beyond 2 years from eCAR issuance, it expires (per RMO 23-2010)
- **Fee computation itself is straightforward** — the pain point is the surrounding process, not the arithmetic
- **Original receipts required** — RD withholds title release if any original OR is missing
- **LRA online tools are limited** — ERCF gives estimates only; actual fees may vary slightly

### Standardization
- **Highly standardized** — the LRA fee table is national, used by all RDs
- The computation is deterministic and simple (graduated lookup table)
- Online tools exist (LRA ERCF, third-party calculators) making this one of the **more accessible** computations

---

## 6. Notarial Fee Computation

### Who Performs It
- **Notary public (lawyer)** — sets and charges the fee
- **Real estate broker/lawyer** — advises client on expected costs
- **Buyer/seller** — negotiate and verify fee reasonableness

### Tools/Methods Used
- **No standard computation tool** — fees are negotiated per transaction
- **OCA Circular 73-2014** ceiling (₱200 for first 4 pages + ₱50/page thereafter) is the statutory maximum per notarial act, but this is widely supplemented by "professional fees"
- **IBP local chapter fee guidelines** — some chapters publish recommended fee schedules, but these are advisory only
- **Market convention** — most practitioners use 0.1%-1.5% of property value as a rough heuristic
- **Package pricing** — notaries commonly bundle document preparation, notarization, and liaison services into a single quote (₱1,500-₱5,000 for land transactions; higher for complex deals)

### Step-by-Step Workflow
1. Notary public reviews the transaction (property value, number of documents, complexity)
2. Notary quotes a fee — typically a combination of:
   - Statutory notarial fee (₱100-₱200 per act per OCA circular)
   - Professional/drafting fee (negotiated, often 0.1%-1.5% of property value)
   - Travel/after-hours surcharge (if applicable)
3. Parties accept or negotiate the quote
4. Documents are notarized; notary issues Official Receipt with separate lines for notarial fee vs. professional fee
5. Entry is made in the Notarial Register

### Pain Points
- **No transparent, standardized fee schedule** — the statutory ₱100-₱200/act ceiling is trivial; real costs come from bundled professional fees that vary wildly
- **Overcharging is common** — some notaries charge 1-2% of property value with no justification; enforcement of fee ceilings is weak
- **Value-based "convenience" charging** — some notaries scale fees to property value but report only the statutory minimum on the OR
- **IBP guidelines are advisory only** — no binding national fee schedule
- **Buyer vs. seller payment disputes** — no clear default; convention varies by locality
- **Non-deterministic** — the actual fee depends on negotiation, not computation

### Standardization
- **Poorly standardized** — statutory ceiling exists but is irrelevant to actual practice
- Each notary sets their own rates within broad bounds
- This is the **least standardizable** computation in the survey — it is inherently a negotiated professional fee, not a deterministic computation

---

## 7. Real Estate Broker Commission Computation

### Who Performs It
- **Broker/brokerage firm** — computes and distributes commission
- **Developer sales team** — sets commission structure for project sales
- **Selling agent** — tracks expected earnings
- **BIR** — computes withholding tax on commission

### Tools/Methods Used
- **Internal brokerage spreadsheets** — most brokerages use Excel to track commissions, splits, and payouts
- **iRealtee** — newly launched (January 2026) Philippine-built brokerage operating system with automated commission calculation, multi-tier split configuration, and developer-specific scheme management
- **Developer portals** — some major developers (Ayala Land, DMCI, SMDC) have internal systems for commission tracking
- **Manual computation** — for independent brokers handling resale transactions, commission is typically hand-computed

### Step-by-Step Workflow

#### Developer Project Sale
1. Buyer reserves a unit; developer records the sale
2. Developer applies project-specific commission rate (typically 3-5% of TCP)
3. Gross commission is computed: TCP × Commission Rate
4. Brokerage retains its share (typically 15-20%)
5. Remaining commission is distributed per the brokerage's split matrix:
   - Selling agent: 50-80%
   - Unit manager override: 5-15%
   - Division manager override: 5-10%
6. Commission payout is triggered by buyer payment milestones (reservation, equity, lump sum, bank release)
7. EWT (5% or 10% per RR 11-2018 at ₱3M threshold) is withheld by developer
8. BIR Form 2307 (Certificate of CWT) is issued to broker

#### Resale Transaction
1. Broker and seller agree on commission rate (typically 3-5% of gross selling price)
2. Commission = Selling Price × Agreed Rate
3. If co-brokered (listing broker + buyer's broker), commission splits 50/50 or per MLS agreement
4. Broker issues OR; commission is subject to income tax reporting

### Pain Points
- **Developer-specific commission structures are complex** — each developer has different rates, split rules, tranche triggers, and payout schedules
- **Multi-tier splits are error-prone in spreadsheets** — overrides, adjustments, and hierarchy changes create calculation errors
- **Commission release delays** — especially for Pag-IBIG and bank-financed sales, where payout depends on loan release timing
- **Tax withholding complexity** — EWT rates recently changed (RR 11-2018); many brokers use outdated rates
- **No industry-standard tool until recently** — iRealtee launched in January 2026 as the first PH-specific brokerage OS
- **Dual agency disclosure requirements** — ethically required but often ignored in practice

### Standardization
- Commission rates are **not legally standardized** — RESA (RA 9646) governs professional conduct but does not set rates
- Industry convention (3-5%) provides de facto standardization
- Developer commission structures are entirely developer-specific — no two are identical
- iRealtee represents the first attempt at tooling-level standardization for commission computation

---

## 8. End-to-End Closing Workflow (Where Each Computation Happens)

### The Full Transaction Timeline

| Step | Actor | Computation | Tools Used |
|------|-------|-------------|------------|
| 1. Agreement | Buyer + Seller + Broker | Negotiate price; broker estimates closing costs | Mental math, Housal calculator, or broker's spreadsheet |
| 2. Due Diligence | Lawyer/Broker | Title verification, encumbrance check | Manual RD records search; some RDs have limited online lookup |
| 3. Deed Preparation | Lawyer/Notary | Draft DOAS; determine notarial fee | Word processor; fee is negotiated |
| 4. Notarization | Notary Public | Notarial fee computation | Manual/negotiated |
| 5. BIR Tax Computation | BIR RDO staff / Lawyer | CGT (6%), DST (1.5%); zonal value lookup | BIR zonal value PDFs (downloaded per-RDO); manual computation or BIR calculator |
| 6. BIR Tax Payment | Buyer/Seller at AAB | File BIR Forms 1706 (CGT) and 2000-OT (DST) | Manual form filling; some BIR eFPS for DST |
| 7. eCAR Issuance | BIR | Verify tax payments, issue eCAR | BIR internal system; **weeks to months processing** |
| 8. Transfer Tax | LGU Treasurer | Local transfer tax (0.5-0.75%) | Manual computation by treasurer's office |
| 9. Registration | Registry of Deeds | Registration fee (LRA table lookup) | LRA ERCF tool or manual tariff card |
| 10. New TCT Issuance | Registry of Deeds | Title transfer processing | LRA LTCP system (partial digitization) |
| 11. New Tax Declaration | LGU Assessor | Assessment level computation, RPT | Assessor's manual/RPTAS system |

### Critical Pain Points in the End-to-End Flow

1. **BIR Zonal Value Lookup is cumbersome** — must download per-RDO Excel/PDF files, search by barangay/street, check revision effectivity dates. No API. No unified database. Third-party tools (ZonalValueFinderPH, REN.PH, ForeclosurePhilippines) provide better UX but depend on manually scraped BIR data.

2. **"Higher value" rule creates computation confusion** — the tax base for CGT, DST, and transfer tax is the HIGHEST of (selling price, BIR zonal value, LGU FMV). Practitioners must look up three separate values from three separate sources and compare. No tool automates this three-way comparison.

3. **Sequential dependencies create bottlenecks** — eCAR must be obtained before RD registration; taxes must be paid before eCAR. The entire pipeline is serial, with each step requiring physical documents from the previous step.

4. **Processing time is dominated by BIR** — eCAR issuance takes weeks to months. All other steps depend on it.

5. **No single tool covers the full workflow** — Housal covers tax estimation; LRA ERCF covers registration fees; ForeclosurePhilippines covers individual calculators; iRealtee covers broker commission. But nothing chains them together into an end-to-end closing cost computation.

6. **Paper-based throughout** — despite individual digital tools, the actual transaction requires physical documents at every stage (notarized deed, original ORs, physical eCAR, stamped tax clearance).

---

## Cross-Cutting Findings

### Tools Landscape (as of February 2026)

| Tool/Platform | Coverage | Type |
|--------------|----------|------|
| **LRA ERCF** | Registration fees only | Government (online calculator) |
| **BIR Zonal Values** | Zonal value lookup only | Government (downloadable PDFs) |
| **BIR eFPS** | Tax form filing | Government (e-filing portal) |
| **Housal** | CGT, VAT, DST, transfer tax, registration, notarial, broker commission | Third-party web calculator |
| **ForeclosurePhilippines** | RD fees, home loan amortization, ARV, rental yield | Third-party web calculators |
| **iRealtee** | Broker commission + multi-tier splits + developer scheme management | SaaS brokerage OS (launched Jan 2026) |
| **Infoman RPTAS** | RPT assessment and records management | LGU software product |
| **BLGF eFAAS** | Field appraisal and assessment | Government LGU tool |
| **Pag-IBIG Online Calculator** | Pag-IBIG loan amortization | Government calculator |
| **ZonalValueFinderPH / REN.PH** | BIR zonal value lookup | Third-party lookup tools |

### Standardization Spectrum

| Computation | Standardization Level | Notes |
|------------|----------------------|-------|
| Registration fees (RD) | **HIGH** | National LRA fee table; online tool exists |
| BP 220 compliance parameters | **HIGH** | National IRR standards; but checking is manual |
| Price ceiling verification | **HIGH** | National JMC; but no automated lookup |
| Assessment levels (LGC maxima) | **HIGH** | National law; but LGU-specific rates within ranges |
| Building depreciation methodology | **MEDIUM** | National methodology (BLGF Manual); LGU-specific tables |
| Broker commission rates | **MEDIUM** | Industry convention (3-5%); developer-specific structures |
| Assessment level implementation | **LOW** | Each LGU sets own SMV, rates, and systems |
| Notarial fees | **LOW** | Statutory ceiling irrelevant; practice-based negotiation |

### Common Error Patterns

1. **Outdated reference data** — using old price ceilings, old zonal values, old SMVs, or superseded circulars
2. **Wrong tax base** — failing to compare all three values (selling price, zonal, FMV) and use the highest
3. **Misclassified property** — wrong assessment level applied due to classification error
4. **Wrong depreciation parameters** — using actual age instead of effective age; wrong economic life assumption
5. **Superseded EWT rates** — brokers using pre-RR 11-2018 withholding rates
6. **Expired eCAR** — exceeding the 2-year validity window and having to re-file

---

## Sources

- [BP 220 Revised IRR (DHSUD)](https://dhsud.gov.ph/wp-content/uploads/Laws_Issuances/02_IRR/Revised_IRR_BP220_2008.pdf)
- [BP 220 Revised IRR (LawPhil)](https://lawphil.net/statutes/repacts/ra2008/irr_bp220_2008.html)
- [Enforcement of Housing Regulations by DHSUD (Respicio)](https://www.respicio.ph/commentaries/enforcement-of-housing-regulations-by-dhsud)
- [DHSUD/DEPDev Socialized Housing Price Ceiling Update (GMA)](https://www.gmanetwork.com/news/topstories/nation/968277/dhsud-depdev-update-price-ceilings-for-socialized-housing/story/)
- [2025 Socialized Housing Price Ceiling Update (CHLP Realty)](https://www.chlprealty.com/post/2025-socialized-housing-price-ceiling-update-dhsud-what-homebuyers-need-to-know)
- [BLGF Summary of Approved SMVs and Assessment Levels](https://blgf.gov.ph/smv/)
- [BLGF Manual on Real Property Appraisal and Assessment](https://blgf.gov.ph/wp-content/uploads/2015/08/ManualRPAandAO.pdf)
- [DOF LAR 1-92 (Supreme Court E-Library)](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/47045)
- [Senate SEPO Policy Brief on Real Property Valuation (2024)](https://legacy.senate.gov.ph/publications/SEPO/PB_Real%20Property%20Valuation_02April2024.pdf)
- [RA 12001 / RPVARA Analysis (PwC)](https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2024/modernizing-property-valuation.html)
- [LRA ERCF Tool](https://lra.gov.ph/ercf/)
- [ForeclosurePhilippines RD Fee Calculator](https://www.foreclosurephilippines.com/how-to-compute-registration-fees/)
- [Notarial Fee Schedule for DOAS (Respicio)](https://www.lawyer-philippines.com/articles/notarial-fee-schedule-for-deed-of-sale-in-the-philippines)
- [Notarial Fees DOAS (Respicio Commentary)](https://www.respicio.ph/commentaries/notarial-fees-for-deed-of-absolute-sale-in-the-philippines-typical-rates-bases-and-requirements)
- [IBP Professional Fees and Notarial Rates (Scribd)](https://www.scribd.com/document/428067621/356668422-IBP-Recommended-Fees)
- [Real Estate Broker Commission (Verizon PH)](https://www.verizonph.com/understanding-real-estate-broker-commission-in-the-philippines)
- [iRealtee Commission Calculator](https://irealtee.com/features/commission-calculator)
- [iRealtee Commission Scheme Configuration](https://irealtee.com/features/commission-scheme-configuration)
- [iRealtee Launch (Manila Times)](https://www.manilatimes.net/2026/01/19/tmt-newswire/irealteecom-launches-for-ph-real-estate-brokerage-operating-system/2260757)
- [Housal Closing Costs Calculator](https://www.housal.com/calculators/sales-closing-fees)
- [BIR Zonal Values Portal](https://www.bir.gov.ph/zonal-values)
- [BIR Zonal Value Lookup Guide (FileDocsPhil)](https://www.filedocsphil.com/how-to-look-for-bir-zonal-value/)
- [ZonalValueFinderPH](https://zonalvaluefinderph.com/bir-zonal-values)
- [REN.PH Zonal Value Tool](https://ren.ph/tools/zonal-value)
- [Philippine Real Estate Transaction Flow (Philippine Island Properties)](https://philippine-islandproperties.com/purchasing-a-property-in-the-philippines-transaction-flow/)
- [Title Transfer Process (FileDocsPhil)](https://www.filedocsphil.com/transfer-land-title-in-the-philippines-a-complete-guide/)
- [LRA Common Issues and Challenges (Respicio)](https://www.lawyer-philippines.com/articles/common-issues-and-challenges-faced-by-the-land-registration-authority-in-the-philippines)
- [Infoman RPTAS Software](https://www.infomaninc.com/infoman/products/rptas.php)
- [Simplifying PH Tax System Through AI (Medium)](https://medium.com/@crmlmcchia2/simplifying-the-philippine-tax-system-through-ai-and-automation-d862c408b14e)
- [VIZCODE BP 220 Reference](https://vizcodeph.com/code-library/bp-220-housing-and-land-use/)
- [Amilyar Guide (ForeclosurePhilippines)](https://www.foreclosurephilippines.com/real-property-tax-rpt-philippines/)
- [Real Property Taxes (Grant Thornton PH)](https://www.grantthornton.com.ph/insights/articles-and-updates1/lets-talk-tax/taxes-on-sale-of-real-property/)

---

## APPENDIX A: Developer Sales Lifecycle — Computation Points by Stage

*Added 2026-02-27 via web research across 60+ additional sources covering the full developer sales agent workflow.*

This appendix maps where each of the 16 Wave 2 computations occurs in the developer sales lifecycle, from the sales agent's perspective. It documents the specific tools, timelines, and bottlenecks at each stage that are not captured in the per-computation views above.

### Stage 1: Pre-Sale (Property Selection & Inquiry)

**Duration:** Days to weeks (buyer-driven)

**Computation: Sample Computation Sheet Generation**
- **Who:** Sales agent / broker
- **What:** TCP breakdown showing reservation fee, DP/equity, monthly equity installment, loanable balance, and estimated monthly amortization under 2-3 payment scheme options (spot cash, deferred cash, bank financing)
- **Tools:** Developer-supplied Excel templates or PDF computation sheets. Each developer has proprietary templates with pricing, discount structures, and payment terms pre-loaded. Agents for smaller developers use personal Excel files.
- **Process:**
  1. Agent selects unit (block/lot/floor/unit) from developer inventory
  2. Looks up TCP from developer's price list (updated per project phase/promo)
  3. Applies payment scheme options:
     - Spot cash: TCP x (1 - discount%). Discounts 7-32% depending on developer/promo.
     - Deferred cash: TCP / months (24-36 months), 0% interest, less RF.
     - Installment + bank financing: TCP x equity% = equity; equity - RF = net equity; net equity / months = monthly; TCP x (1 - equity%) = loanable; estimated bank amortization at indicative rate.
  4. Prints or sends PDF/image to buyer
- **Time:** 5-30 minutes (instant with configured portal; 15-30 min if computing manually from price list)
- **Errors:** Wrong TCP (outdated price list), incorrect discount (promo expired), VAT threshold errors (units >PHP 3.6M should include 12% VAT), unrealistically low indicative bank rates
- **Key bottleneck:** Agents managing properties across multiple developers must maintain separate templates/systems per developer. No unified computation tool exists.
- **Wave 2 computations involved:** developer-equity-schedule, broker-commission, bank-mortgage-amortization (indicative), pagibig-amortization (indicative)

**Computation: Buyer Qualification Pre-Screen**
- **Who:** Sales agent (informal), developer credit department (formal)
- **What:** Monthly amortization vs. 30-40% of gross monthly income (GMI). Pag-IBIG: 35% GMI. Banks: 30-40% internally.
- **Tools:** Mental math or simple calculator. No standardized tool.
- **Time:** 2-5 min (informal); 1-3 days (formal credit check)
- **Errors:** Agents overestimate capacity to avoid losing deal; failure to account for existing obligations
- **Key bottleneck:** Informal qualification leads to applications that fail at loan stage 3-6 months later

**Computation: Commission Estimation**
- **Who:** Sales agent (self), broker/team leader (network)
- **What:** TCP x commission_rate x agent_share, less EWT and deductions
- **Tools:** Excel, personal calculators, or iRealtee (rare). Multi-tier splits are the complexity driver.
- **Time:** 5-15 min manual; near-instant with iRealtee
- **Errors:** Breighton Land case: 49 compensation plan variations, manual Excel tracking "arduous and time-consuming." Errors in multi-tier splits delay payouts.
- **Key bottleneck:** Developer payment cycles span 30-90 days. Commission release differs by financing type (7 different schedules at some brokerages).

### Stage 2: Reservation (Days 1-30)

**Duration:** 1-30 days

**Computation: Reservation Fee Processing**
- **Who:** Sales agent collects; developer treasury records
- **What:** RF amount (PHP 20K-500K), deduction from DP or TCP
- **Time:** Same-day collection; 1-7 days system recording
- **Errors:** RF not correctly deducted from first equity payment; currency conversion for OFW buyers
- **Key bottleneck:** 30-day document submission deadline; forfeiture if missed

**Computation: Payment Scheme Finalization**
- **Who:** Sales agent prepares; developer DIC department finalizes
- **What:** Final computation sheet locked to chosen scheme: exact monthly amounts, due dates, penalty rates, bank financing due date, turnover balance
- **Tools:** Developer internal system (Excel to proprietary ERP, varies)
- **Time:** 7-15 days from reservation
- **Errors:** Mismatch between agent's sample computation and developer's official computation (different TCP, VAT treatment, promo validity)
- **Key bottleneck:** Manual reconciliation between agent computation and back-office computation

**Computation: PDC Schedule Preparation**
- **Who:** Buyer, guided by agent
- **What:** Number of PDCs (min 50 at DMCI), amounts, due dates
- **Time:** Within 15 days of CTS receipt
- **Errors:** Wrong amounts, wrong dates, insufficient checks. Payment scheme changes require full PDC replacement.
- **Wave 2 computations involved:** developer-equity-schedule (primary)

### Stage 3: Equity Period (Months 1-60)

**Duration:** 6-60 months

**Computation: Monthly Equity Tracking & Penalty**
- **Who:** Developer Credit & Collection department
- **What:** Monthly equity amount, running balance, penalty (2-3%/month; DMCI escalating 3%/30-day tiers up to 36% p.a.)
- **Tools:** Developer internal accounting system
- **Errors:** Late penalties inconsistently applied; posting delays for international remittances (24+ hours)
- **Key bottleneck:** OFW remittance timing

**Computation: Account Restructuring / Recomputation**
- **Who:** Developer Remedial Department
- **What:** New computation sheet for changed circumstances (unit transfer, scheme change, LOG-triggered)
- **Time:** 10 working days for DMCI restructured computation sheet
- **Key bottleneck:** This is a gating document — loan cannot proceed without it. 5-day conformity deadline after issuance.

**Computation: Financing Reminder Timeline**
- **Who:** Developer Financing Department
- **What:** 1-year reminder before bank financing due date; 4-month deadline for loan application
- **Key bottleneck:** No buyer response triggers bulk bank endorsement — buyer loses lender choice

**Computation: Maceda Law (if buyer defaults)**
- **Who:** Developer legal/remedial, or buyer's counsel
- **What:** CSV = 50% of total payments + 5%/yr after yr 5 (max 90%); grace = 1 month/year, once per 5 years
- **Tools:** Manual from payment records. **Zero automated tools exist.**
- **Time:** 15-30 min computation; months for dispute resolution
- **Errors:** "Total payments" definition disputes; years counting methodology (per Orbe v. Filinvest); Section 4 notarization requirement
- **Wave 2 computations involved:** maceda-refund, developer-equity-schedule

### Stage 4: Loan Processing (1-6 months before turnover)

**Computation: Loan Eligibility Assessment**
- **Who:** Bank loan officer or Pag-IBIG assessor
- **What:** Pag-IBIG: 7-step tree (24mo contributions, age, credit, 35% GMI, LTV). Banks: DTI 30-40%, credit scoring, employment stability.
- **Tools:** Bank internal system; Virtual Pag-IBIG; Pag-IBIG Affordability Calculator
- **Time:** Pag-IBIG: 20-30 days. Banks: 5-10 working days.
- **Key bottleneck:** Documentation completeness. "Almost every stuck loan involves incomplete titles, unpaid taxes, or clarifications."

**Computation: Property Appraisal**
- **Who:** Accredited appraiser
- **What:** FMV via income/comparable/cost approach. Determines LTV x appraised = max loanable.
- **Fees:** BDO: PHP 5,000 (<30km) / PHP 5,500 (>30km)
- **Time:** 3-10 days (Pag-IBIG); 5-15 days (banks)
- **Errors:** Appraisal < TCP forces buyer to cover gap
- **Wave 2 computations involved:** ltv-ratio, bank-mortgage-amortization, pagibig-amortization

**Computation: LOG / Loan Approval**
- **Who:** Pag-IBIG or bank
- **What:** Approved amount, rate, term, conditions
- **Key bottleneck:** Pag-IBIG LOG 90-day validity. Title transfer must start immediately or re-appraisal required.

**Computation: Loan Release / Takeout**
- **Who:** Bank/Pag-IBIG treasury
- **What:** Release = approved loan - deductions (processing, insurance, DST on mortgage, appraisal). DMCI: 5-7 working days from conformed LOG.
- **Errors:** Shortfall between release and turnover balance; PDCs within 30 days of LOG still deposited (DMCI)

### Stage 5: Turnover

**Duration:** 1-6 weeks

**Computation: Turnover Fee Breakdown**
- **Who:** Developer turnover/admin department
- **What:** Move-in/joining fee + Meralco deposit + water deposit + first association dues + storage fee + closing fee component
- **Key bottleneck:** Must be settled upon unit acceptance — no deferral

**Computation: Closing Cost Aggregation**
- **Who:** Developer documentation or buyer's lawyer
- **What:** DST (1.5%) + transfer tax (0.5-0.75%) + registration fee (LRA graduated) + notarial (1-1.5%) + assurance fund (0.25%) + admin fees. Total: 4-7% of property value.
- **Tools:** Developer estimate at reservation; actual at transfer. Mostly manual/Excel.
- **Key bottleneck:** No single tool computes all closing costs. BIR zonal value verification is manual.
- **Wave 2 computations involved:** rod-registration-fees, notarial-fees, condo-association-dues

### Stage 6: Post-Turnover (months to 1+ year)

**Computation: Title Transfer**
- **Who:** Developer docs + BIR + RD + Assessor (serial pipeline)
- **Time:** Approximately 1 year total
- **Key bottleneck:** Serial dependency — each office must complete before next begins

**Computation: RPT Assessment**
- **Who:** Local Assessor
- **What:** AV = FMV x Assessment Level; RPT = AV x Rate + SEF
- **Key bottleneck:** No centralized LGU rate database

**Computation: Association Dues (Ongoing)**
- **Who:** Condo Corp / HOA
- **What:** Monthly dues = unit_sqm x rate_base (per ECR 001-17)
- **Errors:** SC GR 215801 invalidated prior VAT guidance; many still apply wrong tax treatment

**Computation: Mortgage Tracking (Ongoing)**
- **Who:** Buyer + bank/Pag-IBIG
- **What:** Amortization, repricing, prepayment
- **Key bottleneck:** No tool shows repricing scenario impact in advance; bank calculators are siloed

---

## APPENDIX B: Practitioner Workflow Summary Table (All 16 Computations)

| # | Computation | Current Workflow | Primary Tool | Time/Instance | Error Rate | Lifecycle Stage |
|---|-------------|-----------------|-------------|---------------|------------|-----------------|
| 1 | pagibig-loan-eligibility | Online portal or branch visit | Virtual Pag-IBIG | 20-30 days (full) | Low | Stage 4 |
| 2 | pagibig-amortization | Official calculator | Pag-IBIG Calculator | Minutes | Low | Stage 4 |
| 3 | bank-mortgage-amortization | Bank calculator or generic tool | Bank portal / calculator.net | Minutes | Low (basic), High (repricing) | Stage 1 (indicative), 4 (actual), 6 (ongoing) |
| 4 | developer-equity-schedule | Developer back-office | Developer internal ERP/Excel | 7-15 days (initial), 10 days (restructure) | Low (systemic) | Stage 2, 3 |
| 5 | ltv-ratio | Bank internal process | Bank internal only | Part of evaluation | Low | Stage 4 |
| 6 | maceda-refund | Manual from payment records | **None** | 15-30 min + dispute months | Very High | Stage 3 (default) |
| 7 | rent-increase-computation | Manual (if done at all) | **None** | 5-10 min | High (rate lookup) | Stage 6 (rental) |
| 8 | condo-common-area-pct | Manual from master deed | **None** | 10-20 min | Medium | Stage 5-6 |
| 9 | socialized-housing-compliance | Manual from DHSUD tables | **None** | 15-30 min | Medium | Stage 1 (developer) |
| 10 | bp220-lot-compliance | Manual from IRR tables | **None** | 30-60 min | Medium | Stage 1 (developer) |
| 11 | assessment-level-lookup | Manual from LGU schedule | Some LGU calculators | 10-20 min | Medium | Stage 6 |
| 12 | improvement-depreciation | Assessor process | Assessor internal | Part of assessment | Low | Stage 6 |
| 13 | rod-registration-fees | Manual from LRA table | LRA ERCF (limited) | 10-15 min | Medium | Stage 5-6 |
| 14 | notarial-fees | Negotiation/market rate | **None** (non-deterministic) | N/A | N/A | Stage 5 |
| 15 | broker-commission | Excel with custom formulas | iRealtee or personal Excel | 5-15 min | High (multi-tier) | Stage 1 |
| 16 | condo-association-dues | Condo management or Excel | Varies by condo corp | Monthly auto | Medium | Stage 6 |

---

## APPENDIX C: Additional Sources (Developer Sales Lifecycle Research)

- [DMCI Homes Buyer's Guide](https://www.dmcihomes.com/guides/buyers-guide)
- [SMDC Payment Guide](https://smdc.com/payment/)
- [Filipinohomes — Real Estate Buying Process](https://filipinohomes.com/blog/real-estate-buying-process-developer/)
- [iRealtee Client Management](https://irealtee.com/features/client-management)
- [iRealtee Property Management](https://irealtee.com/features/property-management)
- [iRealtee Terms & Conditions Management](https://irealtee.com/features/terms-conditions-management)
- [iRealtee Agent Profiles](https://irealtee.com/features/agent-profiles)
- [HousingInteractive — Bank Financing Guide](https://housinginteractive.com.ph/blog/step-by-step-guide-to-buying-property-with-bank-financing-in-the-philippines/)
- [GreatDay HR — Pag-IBIG Housing Loan Guide 2025](https://greatdayhr.ph/blog/complete-pag-ibig-housing-loan-application-guide-in-the-philippines-2025/)
- [BPI Housing Loan Requirements](https://www.bpi.com.ph/personal/loans/housing-loan/requirements)
- [BDO Home Loan](https://www.bdo.com.ph/personal/loans/home-loan)
- [Metrobank Home Loan](https://www.metrobank.com.ph/loans/home-loan)
- [RCBC Home Loans](https://www.rcbc.com/home-loans)
- [Respicio — CTS Timeline](https://www.respicio.ph/commentaries/timeline-for-receiving-contract-to-sell-after-condo-reservation-fee-philippines)
- [Respicio — Delayed Turnover](https://www.lawyer-philippines.com/articles/legal-remedies-for-delayed-turnover-of-real-estate-properties)
- [Respicio — Closing Costs](https://www.respicio.ph/commentaries/condominium-title-transfer-in-the-philippines-closing-fees-and-taxes-that-buyers-must-pay)
- [RichestPH — Closing Costs](https://richestph.com/understanding-closing-costs-in-philippine-real-estate/)
- [RichestPH — Payment Methods](https://richestph.com/your-guide-to-real-estate-payment-methods-in-the-philippines/)
- [Federal Land — Condo Financing 101](https://federalland.ph/articles/condo-financing-101/)
- [Filipinohomes — Down Payment vs Equity](https://filipinohomes.com/blog/truth-payment-equity/)
- [Cebu House Finder — Down Payment Guide](https://cebuhousefinder.wixsite.com/cebuhousefinder/post/understanding-home-equity-and-related-issues)
- [Condo Arena — How Long to Buy a Condo](https://condoarena.com/blog/how-long-buy-condo)
- [Presello — Documentation Guide](https://www.presello.com/a-guide-on-documentation-of-real-estate-transactions-in-the-philippines/)
- [Housal — Closing Fees Calculator](https://www.housal.com/calculators/sales-closing-fees)
- [Visdum — Commission Plan Template / Breighton Land Case](https://www.visdum.com/template-library/real-estate-commission-plan-template)
- [OmniCalculator — Pag-IBIG Housing Loan](https://www.omnicalculator.com/finance/pag-ibig-housing-loan)
- [Pag-IBIG Mortgage Loan Calculator](https://pagibigmortgageloancalculator.com/)
- [PhilPropertyExpert — CTS vs DOAS](https://philpropertyexpert.com/contract-to-sell-v-contract-of-sale/)
- [PhilPropertyExpert — Maceda Law](https://philpropertyexpert.com/defaulting-payments-know-your-rights-under-republic-act-6552/)
- [Mandani Bay — Real Estate Laws](https://www.mandanibay.com/blog/real-estate-laws-in-the-philippines/)
- [ATTYDPLaw — CTS vs DOAS](https://www.attydplaw.com/post/understanding-contract-to-sell-vs-deed-of-sale-in-real-estate-transactions-philippines)
- [Studocu — Sample Condo Computation](https://www.studocu.com/ph/document/rizal-technological-university/bs-architecture/condominium-estimated-price-per-unit/36240921)
- [Condopinas — Sample Computation](https://condopinas.weebly.com/sample-computation.html)
- [Lilian Real Estate — Condo Cost Guide](https://lilianrealestate.com/how-much-do-you-need-to-own-a-condo-in-metro-manila/)
- [Pag-IBIG 2025 Rate Stability (Inquirer)](https://business.inquirer.net/529457/pag-ibig-home-loan-rates-unchanged-throughout-2025)
- [Pag-IBIG 2025 Releases (PNA)](https://www.pna.gov.ph/articles/1267430)
- [DBP CTS Financing Program](https://www.dbp.ph/developmental-banking/social-services-community-development/contract-to-sell-financing-facility-cts-program/)
- [iRealtee Sales Wizard](https://irealtee.com/features/sales-wizard)
- [Phinma Properties — Understanding RE Contracts](https://phinmaproperties.com/blogs-articles/phinma-properties/real-estate-philippines-guide-understanding-contracts/)
