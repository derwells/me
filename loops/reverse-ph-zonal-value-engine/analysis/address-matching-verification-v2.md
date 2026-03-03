# Address Matching Logic — Independent Verification Report (v2)

**Wave:** 3 — Resolution Logic Deep-Dive (verification subagent)
**Date:** 2026-03-03
**Aspect:** `address-matching-verification` (supplementary cross-check)
**Purpose:** Cross-check 4 specific design decisions in the proposed address matching algorithm against 2+ independent sources per claim
**Method:** Web search across BIR official resources, practitioner blogs, third-party platform analysis, Philippine address standardization references, and CTA legal resources

---

## Design Decision 1: Dual-Mode Matching (NCR Cross-Street vs. Provincial Road-Proximity)

### Question
Do existing platforms (Housal, RealValueMaps, ZonalValueFinderPH) handle NCR and provincial models differently, or use a single approach?

### Finding: CONFIRMED — The dual-mode distinction reflects the actual BIR data structure, but NO existing platform explicitly implements dual-mode matching

**Source 1 — ZonalValueFinderPH (Makati City NCR data):**
The actual ZonalValueFinderPH data for Makati City shows cross-street boundary entries such as "EDSA TO GIL PUYAT" (Ayala Avenue segment), "EDSA - PASAY MAKATI BOUNDARY" (EDSA in Magallanes), and "PRES. SERGIO OSMEÑA SR. HIGHWAY - CHINO ROCES AVE." (Don Chino Roces in Pio del Pilar). Vicinities are defined by named subdivisions ("LEGASPI VILLAGE", "AYALA CENTER", "SAN LORENZO VILLAGE") and cross-street ranges. Critically, there is NO "ALL OTHER STREETS" catch-all in this Makati NCR dataset — entries comprehensively list individual streets with boundary descriptions.
URL: https://zonalvaluefinderph.com/zonal-values/?city=MAKATI+CITY&province=NCR

**Source 2 — La Trinidad, Benguet (RDO 9, provincial example via Slideshare):**
The La Trinidad zonal schedule uses the road-proximity tier model: "Along National Road" at PHP 5,650/sqm, "Along Provincial Road" at PHP 4,250/sqm, and "Interior" at PHP 2,150/sqm — all within the same barangay. Agricultural sub-tiers also follow this pattern (National > Provincial > Interior). This structure is fundamentally different from the NCR cross-street model.
URL: https://www.slideshare.net/slideshow/rdo-no-9-la-trinidad-benguet-bir-zonal-value/136091257

**Source 3 — Housal platform UX (fetched):**
Housal uses a unified search interface accepting text search (building names, streets, barangays, cities) or regional browsing (17 regions). The NCR section has a dedicated page for Metro Manila's 17 cities, while provincial access is organized by 17 regional groupings. However, the matching appears to be a single text-search system — there is no visible distinction between NCR and provincial matching logic. The classification codes displayed (RC, RR, CC, CR, PS) appear universally without mode-switching.
URL: https://www.housal.com/find-zonal-value

**Source 4 — REN.PH platform UX (fetched):**
REN.PH organizes its 105,384 zone records by geographic browsing (province > city > barangay) or direct search. Metro Manila receives dedicated treatment. Classification options show residential, commercial, and industrial — no distinction between NCR and provincial matching modes. The tool returns records showing "residential, commercial, and industrial zonal values per square meter."
URL: https://ren.ph/tools/zonal-value

**Source 5 — ZonalValueFinderPH platform UX (fetched):**
ZonalValueFinderPH uses a 3-step dropdown approach (city/municipality > barangay > street/subdivision/condominium) without any mode distinction between NCR and provincial. The search is based on pre-populated dropdown selection, not free-text matching.
URL: https://zonalvaluefinderph.com/

**Assessment:**
- The dual-mode distinction is **real and structural** — confirmed by actual BIR workbook data (NCR uses cross-street segments; provincial uses road-proximity tiers).
- **No existing platform explicitly implements dual-mode matching.** All surveyed platforms (Housal, REN.PH, ZonalValueFinderPH) use a single unified search model based on geographic hierarchy (city > barangay > street) with dropdown selection. None attempt free-text address matching with mode-specific parsing logic.
- This represents a **competitive gap**: the proposed engine's dual-mode approach would be architecturally superior to existing platforms, which paper over the structural difference with generic dropdown UIs.
- The Makati data confirming no "ALL OTHER STREETS" catch-all entries in dense NCR areas is an important nuance: in NCR, the fallback hierarchy may need to skip directly from "no exact match" to "adjacent barangay" without a barangay-level catch-all step.

### Verdict: CONFIRMED with competitive advantage noted

---

## Design Decision 2: Fallback Hierarchy

### Question
Is the proposed fallback order (exact street+vicinity match -> barangay catch-all "ALL OTHER STREETS" -> LGU FMV + markup -> written inquiry) confirmed by BIR practice? Do ONETT processors follow this hierarchy?

### Finding: PARTIALLY CONFIRMED — BIR prescribes a formal fallback chain, but the proposed hierarchy has gaps

**Source 1 — BIR RMO 31-2019 (zonal value schedule preamble, confirmed via multiple sources):**
The BIR-prescribed fallback chain embedded in workbook preambles is:
1. Exact match (street/subdivision + classification in barangay)
2. Same classification, other street/subdivision **within same barangay of similar conditions**
3. Same classification, **adjacent barangay of similar conditions**
4. RAMO 2-91 (terminal fallback for absence of any zonal valuation)
URL: https://blgf.gov.ph/wp-content/uploads/2015/09/BIR-RMO_No.-31-2019-SMV.pdf

**Source 2 — BIR ONETT practitioner guidance (Respicio & Co.):**
"ONETT examiners will compute the FMV themselves. Having the exact zonal line and assessor's market values ready significantly speeds up issuance of the eCAR." When the address cannot be determined from documents, a "Location Plan/Vicinity map is required if the Tax Declaration does not indicate the exact location of the property and the zonal value cannot be readily determined from the documents submitted." This confirms that when automated matching fails, the fallback involves human-assisted resolution with supporting documents.
URL: https://www.respicio.ph/commentaries/how-to-compute-zonal-value-of-property-in-the-philippines

**Source 3 — BIR ONETT Annex D1-D10 documentary requirements:**
The official ONETT documentary checklist (Annex D-1 for Capital Gains Tax) lists "Location Plan/Vicinity map if the Tax Declaration of the property does not indicate its exact location and the zonal value cannot be determined from the submitted documents" as a conditional requirement. This confirms the human-in-the-loop fallback when algorithmic matching is insufficient.
URL: https://bir-cdn.bir.gov.ph/BIR/pdf/Annex%20D1%20to%20D10%20(Updated).pdf

**Source 4 — ZonalValuesPH "All Other Streets" evidence:**
Actual BIR zonal value data confirms "ALL OTHER STREETS" as a specific entry type. Examples: "ALL OTHER STREETS, BARANGAY UPPER BICUTAN" (RDO 44 Taguig), "ALL OTHER SUBDIVISION, BARANGAY PINAGBUHATAN" (RDO 43B West Pasig), "ALL OTHER STREETS, BARANGAY 183 ZONE 20, PASAY CITY." These serve as explicit barangay-level catch-all entries with assigned zonal values.
URLs:
- https://whereisit.altervista.org/zonal-value-all-other-streets-barangay-upper-bicutan-residential-regular-land-rdo-no-44-taguig-pateros-157388/
- https://whereisit.altervista.org/zonal-value-all-other-subdivision-barangay-pinagbuhatan-residential-regular-land-rdo-no-43b-west-pasig-153206/
- http://homeguide.altervista.org/bir-zonal-value-of-all-other-streets-barangay-183-zone-20-pasay-city-27058/

**Source 5 — BIR Mandaluyong workbook (carlacalleja.com):**
In some Mandaluyong barangays, the "All Other Streets (RR and CR)" entries have been **deleted** because all streets in the barangay were individually identified — annotated as "No recommended values both for 6th & 7th Revision hence, caption deleted." This means the "ALL OTHER STREETS" catch-all is NOT universally present — some barangays have exhaustive street listings without a catch-all.
URL: https://carlacalleja.com/2020/02/08/bir-zonal-value-mandaluyong-2019/

**Source 6 — Foreclosure Philippines (practitioner site):**
"For newly developed or unzoned areas, the BIR may use the nearest comparable zone or require an appraisal." Also: "Where no zonal value exists (typically in rural barangays), the RDO uses the LGU FMV plus 20% or adopts the nearest comparable zone."
URL: https://www.foreclosurephilippines.com/what-you-need-to-know-about-bir-zonal-values/

**Assessment:**
The proposed hierarchy is **directionally correct** but needs refinement:

| Level | Proposed | BIR-Prescribed | Gap |
|-------|----------|----------------|-----|
| 1 | Exact street+vicinity match | Exact match (street/subdivision + classification) | Aligned |
| 2 | (missing) | Same classification, other street in same barangay of similar conditions | **MISSING** |
| 3 | Barangay catch-all "ALL OTHER STREETS" | (implicit in the data, not in the formal rule chain) | Catch-all is data-driven, not rule-prescribed |
| 4 | (missing) | Same classification, adjacent barangay of similar conditions | **MISSING** |
| 5 | LGU FMV + markup | LGU FMV (used when ZV < assessor's FMV per "highest of three" rule) | Different mechanism |
| 6 | Written inquiry | RAMO 2-91 / RDO human resolution | Aligned in spirit |

Critical gaps:
1. **Missing "same barangay, similar conditions" fallback** (BIR Level 2) between exact match and catch-all
2. **Missing "adjacent barangay" fallback** (BIR Level 3/4)
3. **"ALL OTHER STREETS" is not universally present** — some dense NCR barangays have deleted their catch-all entries
4. **LGU FMV + markup** is not a true fallback in the BIR chain — LGU FMV operates in parallel via the "highest of three" rule, not as a sequential fallback

### Verdict: PARTIALLY CONFIRMED — hierarchy needs expansion from 4 to 6 levels

---

## Design Decision 3: Street Name Normalization

### Question
How do ONETT processors handle address mismatches in practice? Is the proposed normalization approach (former names, abbreviation expansion, Filipino patterns) aligned with practice?

### Finding: CONFIRMED — The normalization approach is well-aligned with BIR practice and real-world needs

**Source 1 — BIR workbook data (confirmed via Housal, Makati City entries):**
The BIR workbooks themselves use the naming convention `CURRENT NAME (formerly OLD NAME)`. The specific example cited in the design (VITO CRUZ -> PABLO OCAMPO SR.) is confirmed in the BIR City of Manila data, which lists: "PABLO OCAMPO SR. (formerly VITO CRUZ)". Other examples: "A.H. LACSON (formerly GOV FORBES)". This is systematic across NCR workbooks.
URL: https://www.housal.com/find-zonal-value/City%20of%20Manila

**Source 2 — Republic Act 6731 / Wikipedia confirmation:**
The Vito Cruz to Pablo Ocampo Sr. renaming is established by law: Republic Act No. 6731, signed by President Corazon C. Aquino. Wikipedia documents this and hundreds of other Metro Manila street renamings. The street spans two cities (Manila and Makati), meaning the alias must map correctly to both jurisdictions.
URL: https://en.wikipedia.org/wiki/Pablo_Ocampo_Street

**Source 3 — BIR ONETT practitioner guidance on street name mismatches:**
When the address on a tax declaration does not match the BIR zonal schedule, ONETT requires: (a) a Location Plan/Vicinity map, (b) the taxpayer/representative to identify the correct zonal line. The examiner resolves the mismatch manually — "ONETT examiners will compute the FMV themselves." Supporting documents may include a barangay certification of the renamed street, or an Affidavit of One and the Same Person for name discrepancies.
URL: https://www.respicio.ph/commentaries/how-to-compute-zonal-value-of-property-in-the-philippines

**Source 4 — Philippine address system characteristics (PostGrid, Wikipedia):**
Filipino addresses commonly include informal components like SITIO (a territorial enclave/hamlet within a barangay), PUROK (an informal zone/district within a barangay), and COMPOUND (a cluster of houses within a shared lot). These are sub-barangay designations that do NOT appear in BIR zonal value schedules. The practical resolution for SITIO/PUROK/COMPOUND addresses is to resolve up to the barangay level and use the barangay's general classification.
URLs:
- https://www.postgrid.com/global-address-format/philippines-address-format/
- https://en.wikipedia.org/wiki/Postal_addresses_in_the_Philippines

**Source 5 — PSGC (Philippine Standard Geographic Code):**
The PSA maintains the PSGC with 10-digit codes for all administrative divisions down to barangay level. The PSGC API is publicly available. However, PSGC does NOT include street-level data — it stops at barangay. This means PSGC is useful for city/municipality/barangay normalization but cannot help with street-level matching.
URL: https://psgc.gitlab.io/api/

**Source 6 — PhilPost address format:**
PhilPost prescribes the format: house number, street name, subdivision, barangay, city/municipality, postal code, province. However, "most residents do not use, let alone know how to use ZIP codes" and "following these guidelines is difficult because some streets have multiple names, residents might only use the barangay name instead of the complete address, and people still use landmarks in rural areas." This confirms the need for robust normalization.
URL: https://en.wikipedia.org/wiki/Postal_addresses_in_the_Philippines

**Assessment:**
The proposed normalization pipeline is well-supported:

| Normalization Rule | Status | Evidence |
|---|---|---|
| Former name -> current name (VITO CRUZ -> PABLO OCAMPO SR.) | CONFIRMED | BIR workbooks use `(formerly ...)` annotation; RA 6731; Wikipedia list |
| Abbreviation expansion (ST. -> STREET, AVE. -> AVENUE) | CONFIRMED | Practitioner guides note inconsistent abbreviation usage; PhilPost standard requires full English |
| BRGY. -> BARANGAY | CONFIRMED | Universal abbreviation in Philippine addressing |
| SITIO/PUROK/COMPOUND handling | CONFIRMED as requiring special treatment | These are sub-barangay designations absent from BIR schedules; resolve to barangay level |
| Uppercase normalization | CONFIRMED | BIR workbooks are consistently uppercase |
| Punctuation stripping | CONFIRMED | Footnote markers (*, **, ***) require stripping per Wave 2 analysis |

Additional normalization needs discovered:
- **Spanish-era street names**: Some BIR entries use Spanish ("CALLE", "AVENIDA") while modern usage is English
- **Numeric suffixes**: "1ST STREET" vs "FIRST STREET" vs "1 ST."
- **Directional prefixes**: "NORTH", "SOUTH", "EAST", "WEST" may be abbreviated or omitted
- **Multi-part honorific names**: "PRESIDENT SERGIO OSMENA SR. HIGHWAY" has 5 tokens — any subset might be used as a shorthand

### Verdict: CONFIRMED — normalization approach is sound and well-evidenced

---

## Design Decision 4: Classification Resolution Timing (Before vs. After Address Matching)

### Question
Is classification resolved BEFORE or AFTER address matching in BIR practice?

### Finding: CLASSIFICATION IS RESOLVED IN PARALLEL WITH ADDRESS MATCHING — the same street can have multiple ZV entries for different classifications, and the BIR schedule treats (street, vicinity, classification) as a composite key

**Source 1 — BIR workbook structure (confirmed via multiple workbook analyses):**
The BIR Excel workbook column layout is: STREET/SUBDIVISION | VICINITY | CLASSIFICATION | ZONAL VALUE/SQ.M. Each row is a unique (street, vicinity, classification) tuple. A single street can appear on multiple consecutive rows with different classification codes. For example, in La Trinidad, Benguet: "Along National Road, Cruz-Alapang Boundary" appears with CR at PHP 1,900/sqm AND RR at PHP 1,200/sqm — two separate rows for the same location, different classification.
URL: https://www.slideshare.net/slideshow/rdo-no-9-la-trinidad-benguet-bir-zonal-value/136091257

**Source 2 — BIR RMO 31-2019 definition of "vicinity" and schedule format:**
RMO 31-2019 defines the schedule format as having the columns: STREET/SUBDIVISION, VICINITY, CLASSIFICATION, REVISION, ZV/SQ.M. The STCRPV is tasked with "identifying and securing lists of all streets with respective vicinities of all the barangays." Classification is a column within the schedule, not a separate pre-filter. The definition of "Vicinity" is "an area, locality, neighborhood, or district about, near, adjacent, proximate, or contiguous to a street being located."
URL: https://blgf.gov.ph/wp-content/uploads/2015/09/BIR-RMO_No.-31-2019-SMV.pdf

**Source 3 — BIR "predominantly commercial" street classification rule:**
"All real properties, regardless of actual use, located in a street/barangay/zone, the use of which are predominantly commercial, shall be classified as 'commercial' for purposes of zonal valuation." This means the BIR's published classification is based on the **street/zone character**, not the individual property's actual use. The published schedule is authoritative (per CTA Aquafresh ruling from the existing analysis).
URL: https://www.respicio.ph/commentaries/determining-zonal-values-for-real-estate-in-the-philippines

**Source 4 — Housal platform classification codes:**
Housal displays 5 classification types (RC, RR, CC, CR, PS) alongside address results. The user does not need to pre-select a classification before searching — classifications appear as attributes of the results. This suggests classification is resolved as part of the result set, not as a pre-filter.
URL: https://www.housal.com/find-zonal-value

**Source 5 — BIR ONETT process (Respicio & Co.):**
"Match the exact location to the correct zonal line and classification." The word "and" here is significant — location and classification are matched together, not sequentially. ONETT processors identify the zonal line first (street + vicinity) and then select the appropriate classification row within that line.
URL: https://www.respicio.ph/commentaries/how-to-compute-zonal-value-of-property-in-the-philippines

**Source 6 — CTA Aquafresh ruling (from existing cta-zonal-rulings.md analysis):**
The Aquafresh case established that the **published classification prevails over actual property use**. This means classification is not something the user decides — it is determined by the BIR schedule. A residential property on a commercially-classified street gets the commercial zonal value.

**Assessment:**
The answer to "before or after" is **neither** — classification is resolved **simultaneously** with address matching as part of a composite key lookup. The practical implication for engine design:

1. **Address matching narrows to a set of candidate rows** (same barangay, same street, same or compatible vicinity)
2. **Classification filters within that candidate set** to produce the final match
3. The user should provide classification as an input, but the engine should also **return all classification entries** for a matched location so the user can see all applicable values
4. In cases where a street has ONLY a CR entry (no RR), the engine must NOT interpret this as "no residential zonal value" — it means the BIR has classified that entire street as commercial regardless of actual use

This is consistent with the existing `address-matching-algorithms.md` design, which uses classification as a filter in Phase 2 (Candidate Selection) after Phase 1 (Normalization).

### Verdict: CONFIRMED — classification and address matching are parallel/simultaneous, not sequential; existing design is correct

---

## Cross-Cutting Finding: How Existing Platforms Structure Their Search

None of the surveyed platforms implement what the proposed engine designs. Here is a comparison:

| Platform | Search Model | Address Matching | Classification Handling | Fallback Logic | Mode Distinction |
|----------|-------------|-----------------|------------------------|----------------|-----------------|
| **Housal** | Text search + hierarchical browse (17 regions) | Keyword-based search over 1.97M records | Shows RC/RR/CC/CR/PS in results | None visible | NCR has dedicated section, but no mode switching |
| **REN.PH** | Geographic hierarchy browse | Province > city > barangay drill-down; direct search over 105K records | Residential/commercial/industrial tabs | None visible | Metro Manila treated separately in navigation |
| **ZonalValueFinderPH** | 3-step dropdown (city > barangay > street) | Pre-populated dropdown selection, no free-text matching | Referenced as separate resource | None visible | No distinction |
| **ZonalValue.com** | Province-level page organization | Browse by province subdomain | Not detailed | None visible | No distinction |
| **LandValuePH** | BIR data + 8 market factors | City-level lookup, instant valuation | BIR classification + market analysis | Uses market factors as supplement | No distinction |

**Key competitive gaps confirmed:**
1. NO platform does free-text address matching with fuzzy logic
2. NO platform implements the BIR-prescribed fallback hierarchy
3. NO platform distinguishes between NCR cross-street and provincial road-proximity models
4. NO platform handles street name aliases or former-name resolution
5. NO platform provides confidence scores or multiple match candidates
6. NO platform prepares for RPVARA dual-source transition

---

## Cross-Cutting Finding: ONETT Processor Behavior in Practice

Based on multiple practitioner sources, the actual ONETT processor workflow is:

1. **Identify the correct RDO** based on property location (title or tax declaration indicates jurisdiction)
2. **Download/open the Excel workbook** for that RDO from bir.gov.ph
3. **Navigate to the correct sheet** (current revision for the municipality)
4. **Ctrl+F search for the barangay name** to find the barangay section
5. **Visual scan within the barangay** for the matching street/subdivision
6. **If the exact street is found**, read across to the classification column and identify the correct row
7. **If the exact street is NOT found**, look for "ALL OTHER STREETS" catch-all within the same barangay
8. **If no barangay match**, may reference adjacent barangay entries or request a location plan/vicinity map
9. **Select the classification** (RR, CR, RC, CC, etc.) based on what appears in the schedule for that street
10. **Read the zonal value** per square meter from the row

This manual process confirms that:
- The matching is **text-based, not geocoded** — processors use Ctrl+F or visual scan
- **Classification is read from the schedule**, not pre-determined by the user
- The **"ALL OTHER STREETS" catch-all** is the primary fallback before escalation
- **Location plans/vicinity maps** are the human-in-the-loop fallback when text matching fails

---

## Summary Table

| Design Decision | Verdict | Confidence | Confirms | Contradicts | Sources |
|----------------|---------|------------|----------|-------------|---------|
| 1. Dual-mode matching (NCR vs Provincial) | **CONFIRMED** | High | Real structural difference in BIR data; no competitor implements it | None | ZonalValueFinderPH, La Trinidad RDO 9, Housal, REN.PH, ZonalValueFinderPH |
| 2. Fallback hierarchy (4 levels) | **PARTIALLY CONFIRMED** | Medium-High | Levels 1, 3, 6 aligned; catch-all entries confirmed | Missing BIR levels 2 and 4; catch-all not universally present | RMO 31-2019, ZonalValuesPH, Mandaluyong workbook, Foreclosure Philippines |
| 3. Street name normalization | **CONFIRMED** | High | Former names, abbreviations, Filipino patterns all validated | None (additional patterns discovered) | BIR workbooks, RA 6731, Wikipedia, PostGrid, PSGC, PhilPost |
| 4. Classification timing | **CONFIRMED** | High | Parallel resolution confirmed; composite key (street, vicinity, classification) | Not sequential "before" or "after" | RMO 31-2019, La Trinidad RDO 9, Aquafresh CTA ruling, Housal, Respicio |

## Actionable Corrections for the Engine Design

### Must-Fix (from this verification):
1. **Expand fallback hierarchy to 6 levels**: Add "same barangay, similar conditions" (BIR Level 2) and "adjacent barangay, similar conditions" (BIR Level 3/4) between catch-all and LGU FMV
2. **Handle missing catch-all entries**: Some dense NCR barangays have deleted their "ALL OTHER STREETS" entries — the engine must not assume this fallback always exists
3. **LGU FMV is not a sequential fallback**: It operates in parallel via the "highest of three" rule — restructure the fallback to distinguish between "no BIR ZV found" (returns NULL) and "BIR ZV found but assessor's FMV is higher" (parallel comparison)

### Should-Refine:
4. **SITIO/PUROK/COMPOUND handling**: Strip these sub-barangay designations during normalization and resolve to barangay level — they never appear in BIR schedules
5. **Return all classification entries for a matched location**: Don't just return the single classification the user specified — show all available classifications so the user can verify the BIR's published classification matches their expectation
6. **Flag "predominantly commercial" streets**: Where a street has ONLY CR entries and no RR, surface a note explaining the BIR's predominant-use classification rule

### Competitive Advantage Confirmed:
7. The proposed dual-mode matching, fuzzy address matching, alias resolution, fallback hierarchy, and confidence scoring are features that **no existing platform offers** — this represents a clear differentiation opportunity

## Sources

### BIR Official Resources
- [BIR Zonal Values Portal](https://www.bir.gov.ph/zonal-values)
- [RMO 31-2019 Full Text (BLGF mirror)](https://blgf.gov.ph/wp-content/uploads/2015/09/BIR-RMO_No.-31-2019-SMV.pdf)
- [RMC 06-2021 (Compliance clarification)](https://blgf.gov.ph/wp-content/uploads/2015/09/RMC-06-2021-RMO-31-2019-Zonal-Values.pdf)
- [BIR ONETT Annex D1-D10 Requirements](https://bir-cdn.bir.gov.ph/BIR/pdf/Annex%20D1%20to%20D10%20(Updated).pdf)
- [RMC 115-2020 (via Manila Bulletin)](https://mb.com.ph/2020/10/27/payment-of-capital-gains-tax-no-longer-requires-zonal-value-certificate-bir/)
- [RDO 57 Binan City Zonal Values (PDF)](https://bir-cdn.bir.gov.ph/BIR/pdf/RDO%20No.%2057%20-%20Bi%C3%B1an%20City,%20West%20Laguna%20(website).pdf)
- [BIR Land Classification Definitions](https://zonalvaluefinderph.com/BIR_Land_Classifications)

### Third-Party Platforms
- [Housal — Find Zonal Value](https://www.housal.com/find-zonal-value)
- [REN.PH — Zonal Value Tool](https://ren.ph/tools/zonal-value)
- [ZonalValueFinderPH](https://zonalvaluefinderph.com/)
- [ZonalValueFinderPH — Makati NCR Data](https://zonalvaluefinderph.com/zonal-values/?city=MAKATI+CITY&province=NCR)
- [LandValuePH](https://www.landvalueph.com/)
- [ZonalValue.com](https://zonalvalue.com/)

### Practitioner and Legal Sources
- [Respicio & Co. — How to Compute Zonal Value](https://www.respicio.ph/commentaries/how-to-compute-zonal-value-of-property-in-the-philippines)
- [Respicio & Co. — Determining Zonal Values](https://www.respicio.ph/commentaries/determining-zonal-values-for-real-estate-in-the-philippines)
- [Foreclosure Philippines — BIR Zonal Values Guide](https://www.foreclosurephilippines.com/what-you-need-to-know-about-bir-zonal-values/)
- [FileDocsPhil — How to Look for BIR Zonal Value](https://www.filedocsphil.com/how-to-look-for-bir-zonal-value/)
- [Digest.ph — RMC 115-2020 Summary](https://www.digest.ph/taxation/issuance-of-certificate-of-zonal-values-of-real-properties)
- [BIR Zonal Value East Makati (carlacalleja.com)](https://carlacalleja.com/2022/01/03/bir-zonal-value-east-makati-2021/)
- [BIR Zonal Value Mandaluyong (carlacalleja.com)](https://carlacalleja.com/2020/02/08/bir-zonal-value-mandaluyong-2019/)
- [CTA Aquafresh ruling — per existing cta-zonal-rulings.md analysis]

### "All Other Streets" Evidence
- [ZonalValuesPH — All Other Streets, Marikina](https://zonalvaluesph.altervista.org/zonal-value-of-all-other-streets-along-marikina-city-whereisit-137402689/)
- [WhereIsIt — All Other Streets, Barangay Upper Bicutan](https://whereisit.altervista.org/zonal-value-all-other-streets-barangay-upper-bicutan-residential-regular-land-rdo-no-44-taguig-pateros-157388/)
- [WhereIsIt — All Other Subdivision, Barangay Pinagbuhatan](https://whereisit.altervista.org/zonal-value-all-other-subdivision-barangay-pinagbuhatan-residential-regular-land-rdo-no-43b-west-pasig-153206/)
- [HomeGuide — All Other Streets, Barangay 183 Zone 20, Pasay](http://homeguide.altervista.org/bir-zonal-value-of-all-other-streets-barangay-183-zone-20-pasay-city-27058/)

### Address Standardization
- [PSGC API](https://psgc.gitlab.io/api/)
- [PostGrid — Philippines Address Format](https://www.postgrid.com/global-address-format/philippines-address-format/)
- [Wikipedia — Postal Addresses in the Philippines](https://en.wikipedia.org/wiki/Postal_addresses_in_the_Philippines)
- [Wikipedia — Pablo Ocampo Street (renaming evidence)](https://en.wikipedia.org/wiki/Pablo_Ocampo_Street)
- [Wikipedia — Purok (sub-barangay definition)](https://en.wikipedia.org/wiki/Purok)
- [GitHub — ph-address (PSGC data package)](https://github.com/kosinix/ph-address)
- [RDO 9 La Trinidad Benguet Zonal Values (Slideshare)](https://www.slideshare.net/slideshow/rdo-no-9-la-trinidad-benguet-bir-zonal-value/136091257)

### Workbook Structure References
- [BIR Zonal Valuation Bulacan (Scribd)](https://www.scribd.com/document/414843960/BIR-Zonal-Value-Bulacan)
- [BIR Classification Codes (Scribd)](https://www.scribd.com/document/491836053/BIR-Classification-Codes)
- [Housal — BIR Zonal Values 2M+ Records](https://www.housal.com/bir)
- [REN.PH — Teresa, Rizal Zonal Values](https://ren.ph/tools/zonal-value/rizal/teresa)
