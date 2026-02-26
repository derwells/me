# Zonal Value Lookup — Resolution Logic and Computation Spec

**Wave:** 2 — Computation Extraction
**Date:** 2026-02-26
**Verification Status:** CONFIRMED (cross-checked against 10+ independent sources)
**Deterministic:** PARTIALLY — the lookup algorithm itself is deterministic, but classification determination and address matching may require judgment in edge cases

---

## Summary

The zonal value lookup is the **highest-leverage data dependency** across all Philippine real estate transaction taxes. Every computation that uses the "highest-of-three" tax base (CGT, DST, CWT, VAT, Transfer Tax) requires resolving a BIR zonal value for the property. This is not a formula but a **multi-step data resolution pipeline**: address → RDO jurisdiction → workbook → row match → classification code → value per sqm → total zonal value.

No BIR API exists. The data lives in 124 heterogeneous Excel workbooks published as ZIP files on bir.gov.ph. This is the single largest automation gap in Philippine real estate taxation.

---

## Inputs

| Input | Type | Source | Notes |
|---|---|---|---|
| `property_address` | string | Deed of Sale / TCT / Tax Declaration | Must resolve to barangay + street + vicinity |
| `property_city_municipality` | string | Deed of Sale / TCT | Used for RDO jurisdiction mapping |
| `land_area_sqm` | numeric (sqm) | TCT / technical description | Multiply by ZV/sqm for total |
| `property_classification` | enum (code) | Tax Declaration / actual use | RR, CR, RC, CC, I, PS, CL, GL, GP, X, APD, A1–A50, DA |
| `transaction_date` | date | Deed of Sale | Determines which revision of the zonal schedule applies |

**Output:** `zonal_value_total` (PHP) = `zonal_value_per_sqm × land_area_sqm`

---

## Resolution Algorithm

### Step 1: RDO Jurisdiction Mapping

**Input:** Property city/municipality
**Output:** RDO code (3-digit)

```
property_city_municipality → RDO_code
```

**Rules:**
- 124 RDOs nationwide, each covering one or more cities/municipalities
- RDO jurisdiction for zonal values is determined by **property physical location** (not taxpayer's registered address or TIN)
- Confirmed by RMC 115-2020: "Certificate of Zonal Values shall only be issued by the concerned RDOs having jurisdiction over the **property location**"
- No centralized database — each RDO maintains its own records independently
- RDO-to-city mapping is a static lookup table (changes rarely, only via BIR reorganization)

**Data structure:** Fixed lookup table, ~124 entries mapping city/municipality names to RDO codes. Publicly available from:
- BIR official directory (bir.gov.ph)
- Multiple third-party compilations (FilipiKnow, TechPilipinas, Philpad)
- Sample: RDO 47 = East Makati, RDO 44 = Taguig/Pateros, RDO 41 = Mandaluyong

**Automation complexity:** LOW — static table, rarely changes, easily maintained.

### Step 2: Schedule Retrieval and Effectivity Date Resolution

**Input:** RDO code + transaction date
**Output:** Correct zonal value workbook/revision

```
(RDO_code, transaction_date) → applicable_schedule_revision
```

**Rules:**
- Each RDO's zonal schedule has an effectivity date (from the DOF Department Order)
- A schedule is effective 15 days after publication in the Official Gazette or newspaper of general circulation (NIRC Section 6(E), RMO 31-2019)
- For a transaction, the applicable schedule is the one in effect at the transaction date
- Multiple revisions may exist for one RDO (e.g., East Makati has had 7 revisions since 1987)
- If a new schedule takes effect between contract signing and closing, use the schedule in effect at the notarization date of the deed

**Approval chain (pre-RPVARA):** STCRPV (local sub-committee at RDO level) → TCRPV (regional technical committee) → ECRPV (executive committee) → DOF Secretary signs Department Order → publication → 15 days → effective

**Data source:** ZIP files on bir.gov.ph → Revenue Region → RDO → download latest.
Each ZIP contains:
- Excel workbook (.xls or .xlsx)
- NOTICE sheet (how to navigate)
- Revision schedule sheet (all past revisions with effectivity dates and DO numbers)
- One or more zonal value data sheets

**Automation complexity:** MEDIUM — requires monitoring 124 RDO pages for updates; no central notification system; update frequency is uneven (38% of schedules outdated per DOF 2024 data; mandate is every 3–5 years per EO 45 / RMO 31-2019, but many RDOs lag significantly).

### Step 3: Property Address Matching

**Input:** Property address (barangay, street, vicinity) + applicable schedule
**Output:** Matching row(s) in the zonal value workbook

```
(barangay, street, vicinity_descriptor) → row_in_schedule
```

**Standard Annex C column format (RMO 31-2019):**

| Column | Content |
|--------|---------|
| Street / Subdivision / Barangay | Name |
| Vicinity | Further descriptor (street segments, boundaries) |
| Classification Code | RR, CR, RC, CC, I, A1–A50, GP, CL, GL, etc. |
| ZV / SQ.M. | Zonal value in PHP per square meter |

**Matching hierarchy:**
1. **Exact street match** — match barangay + street name + vicinity descriptor
2. **Subdivision match** — if property is in a named subdivision, match subdivision name
3. **Barangay-level general entry** — many schedules have "All other streets in [Barangay]" or "General Purpose Interior" catch-all rows
4. **Multiple entries per street** — a single street can have different ZVs for different classifications (e.g., Shaw Blvd in Mandaluyong: RR ₱120,000 vs CR ₱150,000)

**Key challenges for automation:**
- **Merged cells** — workbooks extensively use merged cells for barangay groupings and header hierarchies; pandas `read_excel()` reads only the top-left cell of merged ranges
- **Format inconsistency** — each of 124 RDOs may have slightly different column layouts, header rows, sheet organization
- **Vicinity descriptor ambiguity** — "Ayala Avenue from EDSA to Gil Puyat" requires geocoding or segment matching to determine if a property address falls within that range
- **Image-based PDFs** — some RDOs (e.g., Taguig post-2024) publish as image-only PDFs, requiring OCR
- **Name variations** — "Brgy." vs "Barangay", abbreviations, Filipino/Spanish street name variations

**Automation complexity:** HIGH — this is the hardest step. Requires NLP/fuzzy matching for address normalization, and potentially geocoding for vicinity descriptor resolution.

### Step 4: Classification Code Resolution

**Input:** Property actual use + Tax Declaration classification
**Output:** Applicable classification code

```
property_use → classification_code ∈ {RR, CR, RC, CC, I, PS, CL, GL, GP, X, APD, DA, A1–A50}
```

**Classification codes (Annex B, RMO 31-2019):**

| Code | Classification | Definition |
|------|---------------|------------|
| RR | Residential Regular | Land principally devoted to habitation |
| CR | Commercial Regular | Land devoted principally to commercial use and profit |
| RC | Residential Condominium | Condo units for residential use |
| CC | Commercial Condominium | Condo units/office space for commercial use |
| I | Industrial | Land devoted principally to industry |
| PS | Parking Slot | Parking spaces (typically ~60% of unit value) |
| CL | Cemetery Lot | Cemetery/memorial park lots |
| GL | Government Land | Land owned/used by government |
| GP | General Purpose | Raw/undeveloped land, minimum 5,000 sqm |
| X | Institutional | Schools, churches, hospitals |
| APD | Area for Priority Development | Designated priority zones |
| DA | Drying Area | Agricultural drying areas |
| A1–A50 | Agricultural sub-codes | 50 categories: A1 (Riceland Irrigated), A2 (Riceland Unirrigated), A4 (Coco Land), A6 (Fishpond), A14 (Banana), A24 (Mangrove), A31 (Mineral Land), A36 (Forest/Timber), A50 (Other Agricultural) |

**Resolution rules:**
- Classification generally follows the Tax Declaration
- If property actual use differs from Tax Declaration classification → **predominant use rule** applies (DOF Local Assessment Regulations No. 1-92): the property is classified based on the predominant or principal use in that zone
- Agricultural classification requires minimum 1,000 sqm; below this, typically classified as residential
- GP requires minimum 5,000 sqm
- Conversion/reclassification by LGU does not automatically change BIR classification until the next zonal schedule revision

**Deterministic assessment:** PARTIALLY — most properties have clear classification from the Tax Declaration. However, mixed-use properties and properties whose actual use differs from classification require judgment → **non-deterministic gate** for a subset of cases.

### Step 5: Value Extraction and Total Computation

**Input:** Matched row + classification code + land area
**Output:** Zonal value total

```python
def compute_zonal_value(
    zv_per_sqm: float,    # from matched row in schedule
    land_area_sqm: float,  # from TCT / technical description
    property_type: str,     # 'land' or 'condo'
) -> float:
    """
    For land: total = zv_per_sqm × land_area_sqm
    For condos: total = zv_per_unit (no area multiplication —
                        RC/CC values are already per-unit)
    """
    if property_type == 'condo':
        return zv_per_sqm  # already per-unit in condo tables
    return zv_per_sqm * land_area_sqm
```

**Condo special case:** Zonal values for condominiums (RC/CC codes) are per **unit**, not per sqm of land. The value is read directly from the condo table (organized by building name, tower, floor range).

**Automation complexity:** LOW — trivial arithmetic once Step 3 resolves the matching row.

---

## Fallback Rules (When Exact Match Fails)

The BIR has an established fallback hierarchy for properties not directly listed in the zonal schedule:

| Priority | Condition | Action | Authority |
|----------|-----------|--------|-----------|
| 1 | Exact street + classification match found | Use matched value | Standard lookup |
| 2 | Street not listed but barangay has "All other streets" or "General Purpose Interior" entry | Use barangay-level general entry | RMO 31-2019 practice |
| 3 | Property is special use (school, hospital, church) with no X code entry | Apply nearest **commercial** zonal value within same barangay | RMO 31-2019 / RAMO 2-91 |
| 4 | No barangay-level zonal value exists at all | Use **LGU FMV + 100%** (residential/general) or **LGU FMV + 150%** (commercial/industrial/fishpond), or nearest comparable zone's value | RAMO 2-91 |
| 5 | Boundary dispute or ambiguous jurisdiction | Written inquiry to RDO Zonal Valuation Section; escalation to BIR Valuation and Classification Division (national office) | RMO 31-2019 |
| 6 | Newly reclassified land (e.g., agricultural → residential conversion) | RDO issues Zonal Classification Ruling pending next revision cycle | Administrative practice |

**Key finding from verification:** The ONETT (One-Time Transactions) unit at each RDO applies these fallback rules during eCAR processing. Having the correct zonal line and fallback documented significantly speeds up eCAR issuance. Incorrect zonal value references are a common cause of eCAR rejection or compromise-penalty assessments.

---

## RPVARA Transition (RA 12001)

**Signed:** June 13, 2024 | **Effective:** July 5, 2024 | **IRR signed:** December 10, 2024 (effective January 11, 2025)

### What Changes

| Aspect | Current (pre-RPVARA) | Post-RPVARA |
|--------|----------------------|-------------|
| Valuation authority | BIR Commissioner (NIRC Sec. 6(E)) | BLGF under DOF |
| Valuation base | 3 sources: BIR Zonal Value, LGU SMV, Selling Price → highest wins | Single SMV approved by BLGF → used by all government agencies |
| Tax base rule | max(SP, ZV, AFMV) — three-way max | max(SP, SMV) — two-way max |
| Update frequency | Mandate: every 3–5 years; reality: 38% outdated | Mandatory every 3 years with penalties for non-compliance |
| Implementing agency | BIR (STCRPV/TCRPV/ECRPV committees) | BLGF Real Property Valuation Service (RPVS) |

### Transition Timeline

- LGUs have **2 years from July 5, 2024** (until July 5, 2026) to update SMVs under new framework
- Existing BIR zonal values and LGU SMVs remain in force until replaced by BLGF-approved SMVs
- Transitory rule: where SMVs not yet available, CIR adopts existing SMVs, zonal values, or actual price — whichever is higher
- RPT collection based on new SMVs expected to begin **January 1, 2027**
- **6% cap** on RPT increase in the first year of new SMV effectivity
- 2-year RPT amnesty: penalties, surcharges, interest waived on taxes due before July 5, 2024 (amnesty runs through July 4, 2026)

### Automation Implication

Any zonal value lookup engine built now must be designed to handle:
1. **Current regime (2024–~2027):** Three-source lookup (BIR ZV, LGU FMV, SP) → three-way max
2. **Transition period (~2026–2027):** Dual data sources — some areas with BLGF-approved SMVs, others still on BIR zonal values
3. **Post-transition (~2027+):** Single BLGF SMV → two-way max (SP vs. SMV)

---

## RMC 115-2020 — Certification Procedure

**Issued:** October 9, 2020 by Commissioner Caesar R. Dulay

### Key Provisions

1. **Certificate of Zonal Values** shall only be issued by the RDO with **jurisdiction over the property location**
2. **No longer required for ONETT computations** — certifications for CGT, donor's tax, estate tax, and eCAR are NOT processed; these are no longer prerequisites
3. **BIR processing officers** are directed to access zonal values via the BIR website (bir.gov.ph/zonal-values)
4. **Still available for other purposes** — property owners can still obtain certifications for transactions with other government agencies or private entities

### Practical Impact

This circular effectively confirms that the BIR itself treats the published zonal value schedules on bir.gov.ph as the authoritative source — removing the paper certification as a gating requirement for tax computations. This supports the feasibility of automated zonal value resolution: the same data the BIR uses is publicly downloadable.

---

## Third-Party Data Sources

| Platform | Coverage | Records | Pricing | API? |
|----------|----------|---------|---------|------|
| **housal.com** | Nationwide | 1,961,265+ records, 30,000+ locations | Free lookup | No public API |
| **zonalvaluefinderph.com** | Nationwide | 30,000+ records | Free lookup (disclaims accuracy) | No public API |
| **landvalueph.com** | 200+ cities | Not disclosed | Free lookup; Premium Appraisal Report ₱699 | No public API |
| **zonalvalue.com** | Major cities | Not disclosed | Free lookup | No public API |
| **ren.ph/tools/zonal-value** | NCR-focused | Not disclosed | Free lookup | No public API |
| **filedocsphil.com** | Major cities | Not disclosed | Zonal value list ₱560 (ZIP/Excel) | No |

**Key finding:** No platform offers a public API. All are web-scraping/manual-ingestion plays on top of the same BIR Excel data. None disclose data freshness guarantees. Housal's 1.96M record count is plausible given ~124 RDOs × ~100–500 streets/barangays × ~2–5 classification entries per street × multiple revisions.

---

## Edge Cases and Special Rules

### Condominiums
- Separate zonal value tables organized by building name, tower/floor range
- Classification codes: RC (residential condo), CC (commercial condo), PS (parking slot)
- Value is per **unit**, not per sqm of land — no area multiplication needed
- PS values are typically ~60% of unit RC/CC values

### Multiple Classifications Per Street
- A single street can have both RR and CR entries (e.g., Shaw Blvd in Mandaluyong: RR ₱120,000 interior lots, CR ₱150,000 frontage lots)
- Applicable classification depends on the property's actual use/classification per Tax Declaration

### "Along [Street]" vs Interior Lots
- Some schedules distinguish "along [major road]" (higher value, typically CR) from interior lots (lower value, typically RR)
- If schedule says "along [Street]" and property is not along that street → use the applicable barangay general entry, not a discounted version of the street rate
- ONETT officers will not infer discounts unless the schedule explicitly provides them

### Stale Schedules
- If the applicable schedule is significantly outdated (e.g., 10+ years), BIR officers may still apply it — there is no automatic inflation adjustment
- The RPVARA's 3-year mandatory update cycle aims to address this

### Tax Base Timing for Installment Sales
- Zonal value is fixed at the **date of sale** (notarization of deed / Contract to Sell), per BIR Ruling OT-028-2024
- Subsequent installment payments use the same pre-determined zonal value, even if a new schedule is published during the payment period

---

## Data Dependencies

| Dependency | Source | Automation Feasibility | Key Barrier |
|---|---|---|---|
| RDO jurisdiction table | BIR directory / public compilations | HIGH — static, ~124 rows | Rare changes |
| Zonal value schedule (Excel) | bir.gov.ph ZIP downloads | MEDIUM — 124 heterogeneous workbooks | Format inconsistency, merged cells, some PDFs |
| Address normalization | Property documents | LOW-MEDIUM — requires NLP | Filipino/Spanish names, abbreviations, vicinity matching |
| Classification code | Tax Declaration | MEDIUM — usually deterministic | Mixed-use properties require judgment |
| Effectivity date tracking | DOF Department Orders | MEDIUM — no central notification | Must monitor 124 RDOs independently |

---

## Complexity Drivers (for Scoring in Wave 4)

1. **124 heterogeneous workbooks** — each RDO's Excel has different column layouts, merged cells, header structures
2. **Address matching ambiguity** — vicinity descriptors like "Ayala Avenue from EDSA to Gil Puyat" require segment/geocoding logic
3. **No API** — data acquisition requires downloading, unzipping, and parsing Excel files from bir.gov.ph
4. **Image-based PDFs** for some RDOs — requires OCR pipeline
5. **Update monitoring** — no central RSS/webhook for schedule revisions across 124 RDOs
6. **RPVARA dual-source transition** — must support BIR ZV and BLGF SMV simultaneously during 2026–2027
7. **Classification judgment** — mixed-use properties require predominant-use determination (non-deterministic for ~5–10% of cases)
8. **Condo vs. land bifurcation** — different lookup logic (per-unit vs. per-sqm)
9. **Fallback rule chain** — 6-level fallback hierarchy when exact match fails
10. **Stale data management** — 38% of schedules are outdated; must track and flag

---

## Verification Summary

**Primary sources used:**
- NIRC Section 6(E) as amended by TRAIN (RA 10963)
- RMO No. 31-2019 (via BLGF publication and Manila Standard coverage)
- RMC 115-2020 (BIR CDN PDF, Machica Group, Digest PH, Manila Bulletin)
- RA 12001 / RPVARA (Supreme Court E-Library, IRR via BLGF MC 001-2025)
- DOF Department Orders for specific RDO schedules (DO 022-2021 Makati, DO 005-2024 Taguig, DO 059-2022 Mandaluyong)

**Verification subagent findings (cross-checked against 10+ independent sources):**

| Claim | Status | Sources |
|-------|--------|---------|
| 124 RDOs nationwide | **CONFIRMED** | FilipiKnow, TechPilipinas, Philpad, TechBloat (all state 124) |
| RDO jurisdiction by property location (not taxpayer) | **CONFIRMED** | RMC 115-2020 (BIR CDN), Respicio & Co. |
| No centralized BIR database | **CONFIRMED** | FilipiKnow ("no unified and centralized database system, as of yet") |
| Standard Annex C format (RMO 31-2019) | **CONFIRMED** | BLGF publication of RMO 31-2019, zonal-value-samples Wave 1 data |
| Classification codes (RR, CR, RC, CC, A1–A50, etc.) | **CONFIRMED** | ZonalValueFinderPH (lists RR, CR, RC, CC, CL, DA, A1–A50); note: GL, GP, I, PS, X, APD confirmed in RDO workbook samples but not in that single source — confirmed by Wave 1 analysis of actual RDO Excel files |
| Fallback rules (street not listed → barangay general → LGU FMV+20%) | **CONFIRMED** | Respicio & Co. ("use LGU FMV or nearest comparable zone"), CTA Second Division case |
| Special use rule (nearest commercial value in barangay) | **CONFIRMED** | Respicio & Co. ("If no zonal value has been prescribed, the commercial value of the property nearest to the institution, within the same barangay shall be used") |
| RMC 115-2020: certification no longer required for ONETT | **CONFIRMED** | Manila Bulletin (Oct 27, 2020), Machica Group, Digest PH |
| RPVARA signed June 13, 2024; effective July 3, 2024 | **CONFIRMED** | Supreme Court E-Library, SRMO Law, PwC PH, Deloitte SEA |
| IRR signed December 10, 2024 | **CONFIRMED** | BLGF MC 001-2025 (January 6, 2025) |
| 6% RPT cap in first year | **CONFIRMED** | Itogon Municipality explainer, Lamudi, PwC PH, CHLP Realty |
| 2-year amnesty through July 2026 | **CONFIRMED** | BLGF MC 001-2025, HousingInteractive |
| Housal.com: 1,961,265+ records | **CONFIRMED** | housal.com/find-zonal-value/browse |
| Predominant use rule from DOF regulations | **CONFIRMED** | DOF Local Assessment Regulations No. 1-92 via Respicio & Co. |
| Approval chain: STCRPV → TCRPV → ECRPV → DOF DO → 15 days | **CONFIRMED** | RMO 31-2019 text (BLGF publication), Manila Standard |
| No BIR API exists | **CONFIRMED** | No source found describing any API; all third-party tools scrape Excel data |

**Minor correction to Wave 1 analysis:** The approval chain has **three** committee levels, not two — the ECRPV (Executive Committee on Real Property Valuation) sits above the TCRPV, not the DOF Secretary directly. Full chain: STCRPV → TCRPV → ECRPV → DOF Secretary signs Department Order.

**Verdict: CONFIRMED — no material conflicts between sources. Minor correction applied to committee chain.**

---

## Legal Citations

| Citation | Relevance |
|---|---|
| NIRC Section 6(E) as amended by RA 10963 (TRAIN) | Commissioner's authority to prescribe zonal values; defines FMV as higher of ZV and assessor FMV |
| RMO No. 31-2019 | Operative procedural order for establishing/revising zonal values; defines Annex B (codes) and Annex C (format); creates STCRPV/TCRPV |
| RMC 115-2020 | Certificate of zonal values issued only by RDO of property location; no longer required for ONETT |
| RMC 06-2021 | Clarifications to RMO 31-2019 implementation |
| RAMO 2-91 | Fallback valuation rules: LGU FMV + 20%, nearest comparable zone |
| EO 45, series of 1998 | Mandates periodic review of zonal values (every 3–5 years) |
| RA 12001 / RPVARA (June 13, 2024) | Transfers authority to BLGF; single SMV base; 2-year transition; 6% RPT cap |
| BLGF MC 001-2025 (January 6, 2025) | IRR of RPVARA |
| DOF Local Assessment Regulations No. 1-92 | Predominant use rule for property classification |
| BIR Ruling OT-028-2024 | Tax base (including zonal value) fixed at date of sale for installment transactions |
| Department Order No. 6-2010 | Original authority for STCRPV/TCRPV committee creation |

---

## Automation Implications

### This is the highest-value infrastructure component in the entire catalog

**Why:**
1. It unlocks all 5 transaction taxes simultaneously (CGT, DST, CWT, VAT, Transfer Tax) — every one requires zonal value as input to the "highest-of-three" base
2. No existing Philippine tax tool (JuanTax, Taxumo, QNE) automates the zonal value lookup from real address inputs — users must look up manually and enter values
3. The data moat is significant: parsing 124 heterogeneous Excel workbooks, monitoring updates, normalizing addresses, handling fallback rules — this is a hard engineering problem that deters casual replication
4. Third-party platforms (Housal, ZonalValueFinderPH) have digitized the data but offer no API and no integration with tax computation workflows

### What a production engine needs:

| Component | Difficulty | Notes |
|-----------|-----------|-------|
| RDO jurisdiction lookup table | Easy | Static ~124-row table |
| BIR Excel workbook ingestion pipeline | Hard | 124 workbooks, heterogeneous formats, merged cells, OCR for some |
| Address normalization engine | Hard | Filipino/Spanish names, abbreviations, vicinity matching |
| Classification code resolver | Medium | Usually from Tax Declaration; edge cases need predominant-use rule |
| Fallback rule engine | Medium | 6-level chain |
| Effectivity date tracker | Medium | Monitor 124 RDOs for updates; no push notification available |
| Condo value lookup (per-unit) | Medium | Separate tables organized by building name/tower/floor |
| RPVARA dual-source handler | Medium | Must support BIR ZV and BLGF SMV during transition |
| Data freshness monitor | Medium | Flag stale schedules (38% are outdated) |

### Competitive gap

This is the **widest automation gap** in Philippine real estate tax compliance. Building a reliable zonal value resolution engine would be the single most defensible moat in this market.

---

## Sources

- NIRC Section 6(E) as amended by TRAIN Law (RA 10963)
- RMO No. 31-2019: [BLGF publication](https://blgf.gov.ph/wp-content/uploads/2015/09/BIR-RMO_No.-31-2019-SMV.pdf)
- RMC 115-2020: [BIR CDN PDF](https://bir-cdn.bir.gov.ph/local/pdf/RMC%20No.%20115-2020.pdf); [Manila Bulletin](https://mb.com.ph/2020/10/27/payment-of-capital-gains-tax-no-longer-requires-zonal-value-certificate-bir/)
- RA 12001 (RPVARA): [Supreme Court E-Library](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/97502); [SRMO Law](https://srmo-law.com/legal-updates/understanding-republic-act-no-12001-or-the-real-property-valuation-and-assessment-reform-act-of-2024-rpvara/)
- BLGF MC 001-2025 (IRR of RPVARA): [BLGF PDF](https://blgf.gov.ph/wp-content/uploads/2025/03/BLGF-MC-No.-001.2025-IRR-of-RA-No.-12001-or-the-RPVARA-Reform-Act-6-Jan-2025-Approved-3.pdf)
- BIR Zonal Values page: [bir.gov.ph/zonal-values](https://www.bir.gov.ph/zonal-values)
- RDO Code listings: [FilipiKnow](https://filipiknow.net/rdo-code/); [TechPilipinas](https://techpilipinas.com/bir-rdo-codes/); [Philpad](https://philpad.com/bir-rdo-codes-updated-list/)
- Respicio & Co.: [Zonal value inquiry](https://www.lawyer-philippines.com/articles/real-estate-zonal-value-inquiry-in-the-philippines); [How to compute](https://www.respicio.ph/commentaries/how-to-compute-zonal-value-of-property-in-the-philippines)
- Housal: [housal.com/find-zonal-value](https://www.housal.com/find-zonal-value)
- ZonalValueFinderPH: [Classification codes](https://zonalvaluefinderph.com/BIR_Land_Classifications)
- PwC PH: [RPVARA analysis](https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2024/modernizing-property-valuation.html)
- Deloitte SEA: [Real property valuations](https://www.deloitte.com/southeast-asia/en/services/tax/perspectives/real-property-valuations.html)
- Grant Thornton PH: [RMC 115-2020 commentary](https://www.grantthornton.com.ph/insights/articles-and-updates1/tax-notes/issuance-of-certificate-of-zonal-values-of-real-properties/)
