# RMO 31-2019 Annexes — Classification Codes & Schedule Format Standard

**Wave:** 1 — Source Acquisition
**Date:** 2026-03-02
**Aspect:** `rmo-31-2019-annexes`

---

## Summary

Revenue Memorandum Order No. 31-2019 (dated June 18, 2019) is the operative procedural order governing how BIR zonal values are established, revised, and published. It superseded RMO 41-2010 and introduced the three-tier committee system (STCRPV/TCRPV/ECRPV). Its annexes define the normative standard for classification codes (Annex B) and schedule format (Annex C) — but **actual compliance with these standards varies significantly across RDOs**, as BLGF itself acknowledged in RMC 06-2021.

**Key findings for the engine spec:**
1. The classification code system has **13 primary codes + 50 agricultural sub-codes** = 63 total codes to support
2. The standard Annex C format is a 4-column layout, but column header text varies significantly
3. Historical workbook revisions (pre-2019) used non-standard A-codes — the parser must handle legacy data
4. DA (Drying Area) appears in some but not all workbooks — it's a 13th primary code
5. Fallback rules are partially codified in the workbooks themselves (embedded implementation guidelines)
6. The RMC 06-2021 compliance gap means no parser can assume standard format — must be format-adaptive

---

## Annex B: Classification Codes — Complete Reference

### Primary Codes (12 standard + 1 optional)

| Code | Classification | Definition | Notes |
|------|---------------|------------|-------|
| RR | Residential Regular | Land/condominium principally devoted to habitation | Most common code in NCR |
| CR | Commercial Regular | Land for commercial purposes / profit | Higher ZV than RR for same location |
| RC | Residential Condominium | Condo units for residential use | Per-unit value (not per sqm of land) |
| CC | Commercial Condominium | Condo units/office for commercial use | Per-unit value |
| I | Industrial | Devoted principally to industry | Less common in NCR |
| X | Institutional | Schools, churches, hospitals | Used with fallback to nearest CR in barangay |
| GL | Government Land | Land owned/used by government | Rarely priced; often footnoted |
| GP | General Purposes | Rawland, undeveloped, ≥5,000 sqm minimum | Area threshold is a resolution rule |
| CL | Cemetery Lot | Cemetery/memorial park lots | Specific to memorial parks |
| APD | Area for Priority Development | Designated priority zones | Regional/policy-specific |
| PS | Parking Slot | Condo parking spaces | Typically ~60% of unit RC/CC value |
| A | Agricultural (generic) | Generic agricultural classification | Used when sub-code not specified |
| DA | Drying Area | Agricultural drying areas | **Not in all workbooks** — present in RDO-4 (Pangasinan 2023), absent from RDO-47 (Makati 2021) |

### Agricultural Sub-Codes (A1–A50)

50 sub-codes covering specific crop/land types. See `input/rmo-31-2019-annexes.md` for complete table. Key observations:

- **Most commonly used in practice:** A1 (Riceland Irrigated), A2 (Riceland Unirrigated), A3 (Upland), A4 (Coco Land), A6 (Fishpond), A14 (Banana), A15 (Pasture Land), A17 (Sugar Land), A47 (Vegetable Land), A48 (Coffee), A50 (Other Agricultural)
- **Rarely or never used:** A9 (Cotton), A29 (Grape Vineyard), A33 (Coal Deposit), A34 (African Oil), A45 (Kangkong), A46 (Zarate) — these exist in the standard but are unlikely to appear in any current workbook
- **Regional specificity:** Mindanao: A21 (Durian), A22 (Rambutan); Visayas: A4 (Coco), A17 (Sugar); Cordillera: A47 (Vegetable); all regions: A1, A2, A3, A50

### Critical Deviation: Legacy Classification Codes

**Finding from actual workbook inspection:** Pre-RMO 31-2019 revisions used **non-standard agricultural sub-codes** that mapped differently:

| RDO | Revision | A1 Meaning | A2 Meaning | Standard A1 | Standard A2 |
|-----|----------|-----------|-----------|-------------|-------------|
| RDO-4 (Pangasinan) | DO 6-90 (1990) | Unirrigated Riceland | Mango Land | Riceland Irrigated | Riceland Unirrigated |
| RDO-4 (Pangasinan) | DO 015-2023 (2023) | Riceland Irrigated | Riceland Unirrigated | ✓ Standard | ✓ Standard |

**Parser implication:** When parsing historical revisions, the engine **cannot assume A-codes have consistent meanings across all DOs within a single workbook**. The code meaning is tied to the DO's classification legend, not a universal standard. A parser must read the classification legend from each DO/sheet and map codes contextually.

For current/latest revisions (post-2019), all sampled workbooks (31 total) use the standard Annex B codes consistently.

---

## Annex C: Schedule Format — Standard vs Reality

### Standard Format (Normative)

The standard Annex C template specifies a per-barangay block structure with:

**Header block:**
```
BUREAU OF INTERNAL REVENUE
SCHEDULE OF [APPROVED/RECOMMENDED] ZONAL VALUES OF REAL PROPERTIES
REVENUE REGION NO. [X] - [NAME]
REVENUE DISTRICT OFFICE NO. [XX] - [NAME]

Province:           [PROVINCE]
City/Municipality:  [CITY/MUNICIPALITY]     D.O. NO.          [NUMBER]
Zone/Barangay:      [BARANGAY NAME]         Effectivity Date   [DATE]
```

**Data columns (4):**

| Position | Standard Header | Content |
|----------|----------------|---------|
| Col 0 | STREET/SUBDIVISION | Street name, subdivision, condo building |
| Col 1 | VICINITY | Boundary descriptors, cross-streets, landmarks |
| Col 2 | CLASSIFICATION | Annex B code |
| Col 3 | ZV/SQ.M. | Zonal value in PHP per square meter |

### Observed Deviations Across 31 Workbooks

#### Column Header Text Variations (Col 0)

| Variant | Workbooks |
|---------|-----------|
| `STREET/SUBDIVISION` | Most early revisions (1987-2010) |
| `STREET NAME / SUBDIVISION / CONDOMINIUM` | RDO-4, RDO-5 (Pangasinan, 2023) |
| `STREET/SUBDIVISION/TOWNHOUSES/CONDOMINIUMS` | RDO-47 (Makati, 2021) |
| `STREET/SUBDIVISION/CONDOMINIUM/TOWNHOUSE` | Some Manila RDOs |

#### Column Header Text Variations (Col 2 — Classification)

| Variant | Frequency |
|---------|-----------|
| `CLASSIFICATION` | Rare (ideal) |
| `CLASSI-FICATION` | Very common (narrow column forces hyphenation) |
| `CLASSIFI-CATION` | Common alternative hyphenation |

#### Column Header Text Variations (Col 3 — ZV)

| Variant | Context |
|---------|---------|
| `INITIAL ZV/SQ.M.` | First revision (DO from 1987-1990) |
| `[Nth] REVISION ZV/SQ.M.` | Subsequent revisions, pre-2019 |
| `[Nth] REV. ZV / SQM` | Post-2019 format |
| `[Nth] REV          ZV / SQM` | Wide spacing variant (Pangasinan, Laguna) |

**Key insight:** The revision number is **embedded in the column 3 header**, not a separate column. This is contrary to what some web sources describe as a "Revision" column — there is no standalone revision column in any sampled workbook.

#### Header Field Variations (see `analysis/bir-workbook-provincial-samples.md`)

| Field | Variants Observed |
|-------|------------------|
| Province label | `Province:`, `PROVINCE:`, `Province` (no colon), split across cells |
| Municipality label | `City/Municipality:`, `CITY/MUNICIPALITY:`, `CITY/MUNICIPALITY::`, `CITY/MUNICIPALITY ::` |
| Barangay label | `BARANGAY:`, `Zone/Barangay:`, `Zone/Barangay`, `ZONE/ BARANGAY:`, `Barangay` |
| DO Number label | `D.O. No.`, `D.O. NO.`, split across cells |
| Effectivity Date label | `Effectivity Date`, `Effecivity Date` (typo), split across cells |

---

## Committee Process and Valuation Methodology

### STCRPV Composition and Procedures

| Role | Person |
|------|--------|
| Chairman | Revenue District Officer (RDO) |
| Vice-Chairman | Assistant Revenue District Officer (ARDO) |
| Member | Municipal/Assistant City Assessor |
| Member | Local Development Officer (Office of the Mayor) |
| Members (2) | Licensed and competent appraisers from reputable association |

**Valuation method:**
1. Three independent valuations: BIR, private appraisers, local assessor
2. Final recommended value = **average of the 2 highest** of 3 recommended values
3. Based on "accepted appraisal methods, most recent sales records, and other data"

**If members absent:**
- Chair proceeds with average of 2 highest available or best data/values available
- Must document: invitation letters with waiver, Affidavit, Maps, Minutes of Meeting

### Revision Frequency

- **Mandate:** Every 3 years (per TRAIN Law amendment to NIRC Section 6(E))
- **Reality:** 38% of schedules are outdated (per DOF 2024 data)
- **Engine implication:** Must track effectivity dates per RDO and flag stale schedules

---

## Fallback Rules (Codified in Workbooks)

Three fallback rules are embedded in the workbooks as "Implementation Guidelines" (likely derived from Annex E and earlier RAMO 2-91):

### Rule 1: No Value for Specific Classification
> Where no zonal value has been prescribed for a particular classification, use the value for the **same classification in an adjacent barangay of similar conditions**.

### Rule 2: No Value for Any Classification in Barangay
> Where no sale/exchange/disposition has been effected in a barangay, use the value for a **similarly situated property in an adjacent barangay of similar conditions**.

### Rule 3: No Value for Specific Street
> Where a street does not appear in the approved list, use the value of the **nearest street of similar conditions within the same barangay**.

**Note:** These are simpler than the 6-level fallback hierarchy documented in the prior analysis (`../reverse-ph-tax-computations/analysis/zonal-value-lookup.md`). The prior analysis includes additional fallback levels (LGU FMV markup, written inquiry, zonal classification ruling) that are administrative practices rather than workbook-embedded rules.

---

## RMC 06-2021 Compliance Gap

The BLGF formally noted non-compliance with RMO 31-2019 format at the ECRPV level:

- Schedules presented were **not compliant** with the standard format
- Issues that should have been resolved at STCRPV/TCRPV levels were being escalated
- Assessors enjoined to actively participate in preparation
- Assessors directed to inform BLGF of significant unresolved issues

**Engine implication:** The compliance gap confirmed by BLGF validates our Wave 1 finding — a parser cannot assume the Annex C standard format. It must be format-adaptive, detecting column layouts, header patterns, and classification legends dynamically per workbook per revision.

---

## Implications for Engine Architecture

### Classification Code Resolution

1. **Support 63 codes** (12-13 primary + 50 agricultural sub-codes)
2. **DA code optionality** — must be in the enum but may not appear in all RDOs
3. **Legacy code mapping** — for historical revision parsing, must read the per-sheet classification legend rather than assuming standard codes
4. **GP area threshold** — the 5,000 sqm minimum for GP is a resolution rule, not just a classification label

### Format Detection

1. **4-column invariant** — all sampled workbooks use 4 columns (street, vicinity, classification, ZV). This is the one reliable structural constant.
2. **Header detection must be fuzzy** — column headers vary in text, casing, hyphenation, and spacing
3. **Barangay block detection** — must handle 6+ label variants for the barangay header
4. **No separate "revision" column** — revision number is embedded in the ZV column header

### Data Validation

1. **Cross-check classification codes** against the per-sheet legend when available
2. **Flag non-standard codes** that don't match Annex B
3. **Track effectivity dates** per barangay block (they vary within a single DO for provincial workbooks with mixed revision numbers)

---

## Sources

- BIR CDN: [Rev Annex B - Classification Codes](https://bir-cdn.bir.gov.ph/BIR/pdf/Rev%20Annex%20B%20-%20Classification%20Codes%20(1).doc)
- BLGF: [BIR-RMO_No.-31-2019-SMV.pdf](https://blgf.gov.ph/wp-content/uploads/2015/09/BIR-RMO_No.-31-2019-SMV.pdf) (403 at time of fetch)
- BLGF: [RMC-06-2021-RMO-31-2019-Zonal-Values.pdf](https://blgf.gov.ph/wp-content/uploads/2015/09/RMC-06-2021-RMO-31-2019-Zonal-Values.pdf) (403 at time of fetch)
- Scribd: [Revenue Memorandum Order No 31-2019](https://www.scribd.com/document/653558790/REVENUE-MEMORANDUM-ORDER-NO-31-2019)
- ZonalValueFinderPH: [BIR Land Classifications](https://zonalvaluefinderph.com/BIR_Land_Classifications)
- ForeclosurePhilippines: [BIR revision schedule](https://www.foreclosurephilippines.com/bir-revision-schedule-of-zonal-values-real-properties/)
- BIR Official: [Zonal Values page](https://www.bir.gov.ph/zonal-values)
- Cross-validated against actual workbooks: RDO-47 (East Makati, DO 37-2021), RDO-4 (Calasiao Pangasinan, DO 015-2023 and DO 6-90)
- Prior analysis: `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md`
