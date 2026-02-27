# Practitioner Workflow Analysis — PH Real Estate Regulatory & Fee Computations

## Summary

This analysis documents the actual workflows practitioners use for each computation category identified in Wave 2, covering who performs each computation, what tools/methods they use, the step-by-step process, pain points, and standardization status. Research synthesized from 40+ web sources including government portals, practitioner guides, PropTech platforms, and industry blogs.

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
