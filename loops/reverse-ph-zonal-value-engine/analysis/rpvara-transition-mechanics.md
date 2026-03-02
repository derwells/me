# RPVARA Transition Mechanics — Analysis

**Wave:** 1 — Source Acquisition
**Date:** 2026-03-02
**Aspect:** rpvara-transition-mechanics
**Sources:** RA 12001 (LawPhil, SC E-Library), BLGF MC 001-2025, 8 law firm analyses (SRMO, BDB, Cruz Marcelo, Alburo, PwC, Deloitte, Grant Thornton, NDV Law), BLGF website, Itogon Municipality explainer

---

## Summary

RA 12001 (RPVARA), signed June 13, 2024 and effective July 3-5, 2024, fundamentally restructures Philippine real property valuation by replacing BIR zonal values with BLGF-approved Schedules of Market Values (SMVs) as the single valuation base. The transition creates a complex dual-source period (July 2024 through ~mid-2027) where the zonal value engine must simultaneously support BIR zonal values and emerging BLGF SMVs, with per-jurisdiction detection of which regime applies.

---

## 1. The Core Structural Change

### Before RPVARA
Three independent valuation sources determined the tax base for internal revenue taxes on real property:
1. **BIR Zonal Value (ZV)** — determined by the Commissioner of Internal Revenue per NIRC Section 6(E)
2. **LGU Fair Market Value (FMV)** — from local assessor's Schedule of Market Values
3. **Actual Selling Price (SP)** — from the deed of sale or transaction documents

**Tax base = max(ZV, FMV, SP)** — the three-way maximum rule.

### After RPVARA (Post-Transition)
A single valuation source replaces all three:
- **BLGF-approved SMV** — prepared by local assessors, reviewed by BLGF Regional Office, certified by Secretary of Finance

**Tax base = max(SMV, SP)** — the two-way maximum rule (Section 18(c)).

### The Power Transfer
The CIR (BIR Commissioner) **no longer has the power** to determine zonal values for internal revenue tax purposes (multiple sources confirm: SRMO Law, Deloitte, PwC, BDB Law). This authority transfers to:
- **BLGF** — develops PVS, reviews and certifies SMVs
- **Local assessors** — prepare SMVs per PVS standards
- **Secretary of Finance** — final certification authority

---

## 2. Transition Period Mechanics

### Section 29(b) — The Interim Rule
During the transition, while BLGF-approved SMVs are being prepared:

> "In case the SMVs are not yet available or updated, the Commissioner of Internal Revenue shall adopt the existing SMVs, zonal values, or the actual price in consideration as stated in real property transaction documents, **whichever is higher**, for purposes of computing any internal revenue tax."

This means the **three-way maximum continues** during the transition — the old rule persists until BLGF-approved SMVs replace it jurisdiction by jurisdiction.

### Section 31 — Saving Clause (Continuation of Zonal Values)
> "The zonal values, as determined by the BIR and approved by the Secretary of Finance for internal revenue tax purposes... shall **continue to be in force and effect** until repealed, superseded, modified, revised, set aside, or replaced in accordance with Section 16 of this Act, which shall be within two (2) years upon the effectivity of this Act."

**Key implication:** BIR zonal values don't expire automatically. They continue indefinitely until a specific BLGF-approved SMV replaces them for that jurisdiction. The "within two years" language is a mandate for LGUs to update, not an automatic expiration of existing values.

### The Dual-Source Detection Problem
Because rollout is per-LGU (not nationwide simultaneous), the engine must handle three regimes for any given property lookup:

| Regime | When It Applies | Tax Base Rule |
|--------|----------------|---------------|
| **Pre-transition** | LGU has no BLGF-approved SMV (most LGUs, 2024-2026+) | max(SP, ZV, existing_FMV) |
| **Transition year 1** | LGU has newly approved SMV, first year of effectivity | max(SP, SMV) with 6% RPT cap |
| **Post-transition** | LGU has approved SMV, beyond first year | max(SP, SMV) |

**Detection mechanism:** For each property, the engine must check whether the jurisdiction (city/municipality) has a BLGF-approved SMV in effect. If yes → use Section 18(c) rule. If no → use Section 29(b) rule.

---

## 3. Timeline Analysis

### Statutory Deadlines

| Milestone | Date | Status (as of March 2026) |
|-----------|------|--------------------------|
| RA 12001 signed | June 13, 2024 | Done |
| RA 12001 effective | July 3-5, 2024 | Done |
| IRR deadline (3 months) | October 3-5, 2024 | Missed by ~2 months |
| IRR signed (BLGF MC 001-2025) | December 10, 2024 | Done |
| IRR effective | January 11, 2025 | Done |
| LGU SMV update deadline (2 years) | July 3-5, 2026 | ~4 months away |
| Tax amnesty deadline | July 5, 2026 | ~4 months away |
| Expected RPT on new SMVs | January 1, 2027 | ~10 months away |
| First 3-year revision cycle | ~mid-2029 | Future |

### Realistic Assessment of the July 2026 Deadline

Given that only 37-42% of LGUs had compliant SMVs even under the old system (which had the same 3-year revision mandate), meeting the July 2026 deadline for all ~1,700 LGUs is extremely unlikely. Evidence:
- 62 of 80 provinces had outdated SMVs as of 2014
- 116 of 143 cities had outdated SMVs as of 2014
- 97 cities and 40 provinces were non-compliant as of 2024
- The BLGF is still conducting "Skills Enhancement Training" sessions for assessors
- PVS development/adoption is still in progress (PVS 2nd Edition recently launched)
- The IRR itself was delayed by ~2 months

**Practical implication for engine design:** The dual-source period will likely extend well beyond July 2026. Some jurisdictions may not have BLGF-approved SMVs until 2028 or later. The engine must support BIR zonal values as a first-class data source for the foreseeable future, not just as a legacy holdover.

---

## 4. SMV Format and Preparation Process

### The New SMV Preparation Pipeline (IRR Chapter 3)

```
BLGF issues notice to all local assessors
    ↓
Local assessors prepare proposed SMVs per PVS (12-month window)
    ↓
Proposed SMV published (at least 2 weeks before public consultation)
    ↓
2 mandatory public consultations (within 60 days before submission)
    ↓
Proposed SMV submitted to BLGF Regional Office
    ↓
BLGF Regional Office reviews
    ↓
If compliant → endorsed to BLGF Head
    ↓
BLGF Head reviews for PVS compliance
    ↓
If compliant → endorsed to Secretary of Finance
    ↓
Secretary of Finance certifies
    ↓
Certified SMV published → effective 15 days after complete publication
```

### SMV Format (What We Know and Don't Know)

**Known:**
- SMVs will be prepared "for the different classes of real property" situated within each LGU
- Must follow PVS (based on International Valuation Standards)
- Must cover "all kinds of real property, whether taxable or exempt"
- For properties not in the SMV: "shall be appraised at its current market value, and shall be assessed for taxation purposes by applying the prescribed assessment level based on its actual use" (Section 4(p))

**Unknown / Not Yet Specified:**
- Column layout and format of BLGF-approved SMVs (will they follow the BIR Annex C format? Likely not — PVS will define a new format)
- Property classification codes under PVS (will they map to the BIR Annex B codes RR/CR/RC/CC/I/A1-A50, or use a different taxonomy?)
- How vicinity/address descriptors will be structured in the new SMVs
- Whether SMVs will be published as Excel workbooks, PDFs, or via RPIS digital platform
- Whether condo tables will follow the same per-unit convention as BIR zonal schedules

**Data format risk:** If the new BLGF-approved SMVs use a different format than BIR zonal value workbooks, the engine's parser must support two format families. However, the early indication is that BLGF may define a standardized digital format (via RPIS), which would actually be easier to parse than the heterogeneous BIR Excel workbooks.

---

## 5. Impact on Specific Tax Types

### Capital Gains Tax (CGT)
- **Pre-RPVARA:** 6% × max(SP, ZV, AFMV)
- **Transition:** 6% × max(SP, ZV, existing_SMV) per Section 29(b)
- **Post-RPVARA:** 6% × max(SP, SMV) per Section 18(c)

### Documentary Stamp Tax (DST)
- **Pre-RPVARA:** ₱15 per ₱1,000 of max(SP, ZV, AFMV)
- **Transition:** Same three-way max per Section 29(b)
- **Post-RPVARA:** ₱15 per ₱1,000 of max(SP, SMV)

### Donor's Tax
- **Pre-RPVARA:** 6% × max(ZV, AFMV) for the donated property
- **Transition:** Same per Section 29(b) — ZV/existing SMV/actual value
- **Post-RPVARA:** 6% × SMV (or appraised value if not in SMV)

### Estate Tax
- **Pre-RPVARA:** 6% of net estate, with property valued at max(ZV, AFMV)
- **Transition:** Same per Section 29(b)
- **Post-RPVARA:** 6% of net estate, with property valued at SMV

### Value-Added Tax (VAT)
- **Pre-RPVARA:** 12% × max(SP, ZV, AFMV) (for ordinary assets exceeding ₱3.199M threshold)
- **Transition:** Same per Section 29(b)
- **Post-RPVARA:** 12% × max(SP, SMV)

### Real Property Tax (RPT)
- **Pre-RPVARA:** Based on LGU assessed value (assessment level × LGU FMV)
- **Post-RPVARA:** Based on LGU assessed value derived from BLGF-approved SMV
- **First year cap:** 6% maximum increase in RPT over pre-RPVARA assessment
- **Subsequent years:** LGU may enact cap ordinance

---

## 6. The Real Property Information System (RPIS)

### What RPIS Will Be
A centralized electronic database maintained by BLGF containing:
- All real property transactions (sale, exchange, lease, mortgage, donation, transfer)
- All real property declarations
- Construction/renovation costs
- Plant, machinery, and equipment prices

### Data Flow Into RPIS
Quarterly electronic reporting from:
- Registers of Deeds (title transfers)
- BIR (tax return data)
- Notaries public (notarized deeds)
- Building permit officials (construction data)
- Geodetic engineers (survey data)

### Data Access From RPIS
- Free for all LGUs and national government agencies
- Available to CIR for tax computation
- Private sector access subject to BLGF guidelines (potential for API access)
- Subject to Data Privacy Act (RA 10173)

### RPIS Status (March 2026)
- Not yet operational
- BLGF + DICT tasked with full automation within 2 years from effectivity (deadline: July 2026)
- No public information on RPIS technical architecture, API specifications, or data format
- Given the July 2026 deadline and current pace, operational RPIS by 2027-2028 is more realistic

### Implications for Engine Architecture
- **Near-term (2024-2027):** Engine must parse BIR Excel workbooks (existing pipeline)
- **Medium-term (2026-2028):** Engine must also ingest BLGF-approved SMVs (format TBD)
- **Long-term (2028+):** RPIS may provide a centralized data source (potentially API-accessible)
- **Architecture requirement:** Data ingestion layer must be pluggable — support BIR workbooks, BLGF SMVs, and eventually RPIS integration, without engine core changes

---

## 7. Key Uncertainties and Gaps

### What We Don't Know Yet

1. **BLGF SMV format specification** — No published standard for the format of BLGF-approved SMVs. Will they use the same column structure as BIR Annex C? Will they have digital/structured formats? This is critical for parser design.

2. **Property classification under PVS** — Will PVS maintain the BIR Annex B classification codes (RR, CR, RC, CC, I, A1-A50, etc.) or introduce a new taxonomy? The BIR codes are deeply embedded in existing workbooks and tax practice.

3. **BIR operational guidance** — No BIR RMC has been issued specifically addressing how ONETT officers should handle transactions during the transition. The existing RMO 31-2019 and RMC 115-2020 remain operative, but their interaction with RPVARA is unclear.

4. **RPIS technical specifications** — No published technical architecture, API design, or data schema for the RPIS. It's unclear whether it will be a web portal, an API, or both.

5. **Pace of LGU compliance** — How many LGUs will meet the July 2026 deadline? Given historical compliance rates (37-42%), the dual-source period could extend significantly.

6. **Interaction with pending BIR zonal value revisions** — Several RDOs have pending zonal value revisions that were in progress when RPVARA was enacted. Section 29(a) allows LGUs already updating to continue, but what about BIR-initiated revisions under the old committee structure?

7. **Condo valuation under new system** — Will BLGF-approved SMVs maintain the per-unit condo valuation convention, or switch to per-sqm? This affects the engine's computation logic.

---

## 8. Design Implications for the Zonal Value Engine

### Must-Have Capabilities

| Capability | Rationale |
|-----------|-----------|
| **Dual-source resolution** | Engine must support both BIR ZV and BLGF SMV simultaneously during transition |
| **Per-jurisdiction regime detection** | Must determine whether a given LGU has a BLGF-approved SMV in effect |
| **Three-way vs two-way max** | Section 29(b) three-way max during transition → Section 18(c) two-way max post-transition |
| **Pluggable data ingestion** | Must support BIR Excel workbooks, BLGF SMV format (TBD), and eventually RPIS |
| **Data source metadata** | Each value must carry provenance: source (BIR ZV / BLGF SMV), effectivity date, revision number |
| **Staleness tracking** | Flag jurisdictions where no BLGF-approved SMV exists and BIR ZV is outdated |

### Architecture Principles

1. **Separation of data source from resolution logic** — The matching/resolution engine should be agnostic to whether the data comes from BIR workbooks or BLGF SMVs. Data is normalized into a common internal format at ingestion time.

2. **Regime-aware tax base computation** — The tax base formula (three-way vs two-way max) is parameterized by the regime in effect for the jurisdiction, not hardcoded.

3. **Forward-compatible data model** — The internal property record format should accommodate fields that BLGF SMVs may introduce (PVS-based classification, potentially different granularity).

4. **RPIS integration readiness** — Design the data ingestion layer with a clean interface that can add an RPIS data source when it becomes available, without restructuring.

5. **Effectivity date tracking** — Every data record must carry its effectivity date and the authority that established it (DOF Department Order for BIR ZVs, DOF Secretary certification for BLGF SMVs).

---

## 9. What This Means for the Current Engine Spec

The RPVARA transition does NOT change the immediate engineering problem:
- BIR zonal values are still the operative data source for most jurisdictions
- The 124 heterogeneous Excel workbooks are still the primary data to ingest
- The address matching, classification resolution, and fallback hierarchy logic remains the same

What it DOES change is the architecture requirements:
- The engine must be designed for **data source extensibility** from day one
- The resolution logic must support **per-jurisdiction regime switching**
- The data model must accommodate **provenance and effectivity metadata**
- The frontend must display **which regime applies** and **data freshness warnings**

The good news: building for RPVARA-readiness makes the architecture cleaner, not more complex. A well-abstracted data layer that can accept normalized property value records from any source (BIR workbook, BLGF SMV, RPIS API) is the right design regardless.

---

## Legal Citations

| Citation | Relevance |
|----------|-----------|
| RA 12001 (RPVARA), June 13, 2024 | The enabling law; transfers valuation authority to BLGF |
| RA 12001, Section 4(p) | Definition of SMV |
| RA 12001, Section 13 | Philippine Valuation Standards mandate |
| RA 12001, Section 18 | Use of SMV for all tax purposes; the two-way max rule |
| RA 12001, Section 18(c) | CIR uses max(SMV, SP) for internal revenue taxes |
| RA 12001, Section 19 | 2-year update deadline + 3-year revision cycle |
| RA 12001, Section 22 | Real Property Information System (RPIS) |
| RA 12001, Section 24 | Quarterly electronic data transmission to BLGF |
| RA 12001, Section 29 | Transitory guidelines — three-way max during transition |
| RA 12001, Section 29(b) | Interim rule: max(SP, ZV, existing_SMV) |
| RA 12001, Section 29(c) | 6% RPT increase cap in first year |
| RA 12001, Section 30 | Tax amnesty through July 2026 |
| RA 12001, Section 31 | Saving clause — ZVs continue in force until replaced |
| RA 12001, Section 32 | Repealing clause — inconsistent laws repealed |
| BLGF MC 001-2025 | IRR of RA 12001, effective January 11, 2025 |
| BLGF MC 003-2025 | Tax amnesty implementation guidance |
| NIRC Section 6(E) | Pre-RPVARA CIR authority to prescribe zonal values (now superseded) |
| RMO 31-2019 | BIR operative order for zonal values (still in effect during transition) |
| RMC 115-2020 | BIR certification procedure (still in effect) |

---

## Sources

- RA 12001: [LawPhil](https://lawphil.net/statutes/repacts/ra2024/ra_12001_2024.html) | [SC E-Library](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/97502)
- BLGF MC 001-2025 (IRR): [BLGF PDF](https://blgf.gov.ph/wp-content/uploads/2025/03/BLGF-MC-No.-001.2025-IRR-of-RA-No.-12001-or-the-RPVARA-Reform-Act-6-Jan-2025-Approved-3.pdf)
- SRMO Law: [Analysis](https://srmo-law.com/legal-updates/understanding-republic-act-no-12001-or-the-real-property-valuation-and-assessment-reform-act-of-2024-rpvara/)
- PwC PH: [Modernizing Property Valuation](https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2024/modernizing-property-valuation.html)
- Deloitte SEA: [Real Property Valuations](https://www.deloitte.com/southeast-asia/en/services/tax/perspectives/real-property-valuations.html) | [RPVARA](https://www.deloitte.com/southeast-asia/en/services/tax/perspectives/rpvara.html)
- Cruz Marcelo: [RPVARA Analysis](https://cruzmarcelo.com/modernizing-and-standardizing-the-valuation-of-real-property-in-the-philippines-the-real-property-valuation-and-assessment-reform-act/)
- BDB Law: [Real Property Valuation Law](https://www.bdblaw.com.ph/index.php/newsroom/articles/tax-law-for-business/1173-real-property-valuation-law)
- Grant Thornton PH: [Tax Impacts](https://www.grantthornton.com.ph/insights/articles-and-updates1/lets-talk-tax/tax-impacts-from-the-new-property-valuation-law/)
- Itogon Explainer: [RPVARA](https://itogon.gov.ph/2025/02/explainer-on-rpvara-real-property-valuation-and-assessment-reform-act/)
- BLGF SMV Data: [BLGF SMV](https://blgf.gov.ph/smv/)
- BLGF PVS: [PVS 2nd Edition Launch](https://blgf.gov.ph/launching-of-the-philippine-valuation-standards-2nd-edition/)
- BLGF Training: [SMV Skills Enhancement](https://blgf.gov.ph/blgf-holds-skills-enhancement-training-on-the-updating-of-schedule-of-market-values-smv-and-conduct-of-general-revision-gr-of-real-property-assessments/)
- BIR 2025 RMCs: [BIR](https://www.bir.gov.ph/2025-Revenue-Memorandum-Circulars)
- PIDS Study: [LGU SMV Compliance](https://serp-p.pids.gov.ph/publication/public/view?slug=local-government-units-compliance-in-the-mandated-revision-of-the-schedule-of-market-values-smvs)
