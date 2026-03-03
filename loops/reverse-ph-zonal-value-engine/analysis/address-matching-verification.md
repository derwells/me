# Address Matching Strategy — Cross-Verification Report

**Verification subagent output** — 6 claims verified against 15+ independent sources (web search, BIR official resources, practitioner accounts, academic papers, open-source projects, Wikipedia).

## Claim 1: BIR ONETT Officers Match by Barangay + Street + Vicinity

**Verdict: CONFIRMED**

### Evidence

**Source 1 — BIR Official Website & RMC 115-2020:**
BIR Revenue Memorandum Circular 115-2020 instructed Revenue District Officers nationwide to get zonal values through the bureau's website rather than requiring separate certificates. The lookup process on bir.gov.ph follows: (1) select the RDO where the property is located, (2) download the ZIP Excel file, (3) search by barangay and street/subdivision. Each line in a zonal value table includes a **location description (barangay, specific condo name, or street)** and the matching entry must correspond to the **exact listing**.

**Source 2 — Respicio & Co. (Philippine law firm commentary):**
"Before consulting the BIR or searching online, make sure you have the property's exact address, land area, and classification. To be precise, you must identify your exact address (tower, unit, building, street) and confirm the correct RDO for that location."

**Source 3 — Existing loop analysis (address-vicinity-patterns.md):**
The loop's own Wave 2 analysis of 31 BIR workbooks confirms the structure: records are organized by barangay header rows, with street column + vicinity column + classification code + zonal value per square meter. 28,109 vicinity records were extracted, confirming the barangay-street-vicinity triplet as the fundamental matching unit.

**Assessment:** The claim is accurate. BIR zonal value schedules are structured as barangay > street > vicinity > classification > value, and ONETT processors use this hierarchy for lookup. The process is manual (Excel Ctrl+F search or visual scan) — there is **no geocoding or GIS system** used by BIR for this purpose.

---

## Claim 2: "Highest of Three" Rule Means Matching Doesn't Need to Be 100% Precise

**Verdict: PARTIALLY CONFIRMED — the rule exists but the inference about imprecision is NUANCED**

### Evidence

**Source 1 — U-Property PH / BIR Practice:**
"When selling, inheriting, or donating a property, the BIR will use the **highest** among selling price, zonal value, and assessor's fair market value as basis for tax computation." This "highest of three" rule is confirmed across 5+ independent practitioner sources.

**Source 2 — Foreclosure Philippines:**
"For newly developed or unzoned areas, the BIR may use the **nearest comparable zone** or require an appraisal." This confirms that approximate matching (nearest comparable) is accepted practice when an exact match is unavailable.

**Source 3 — RMO 31-2019 Annexes (from existing analysis):**
The workbooks embed three fallback rules directly:
1. If no zonal value is prescribed for a particular classification in a subdivision in a barangay, use the same classification in another street/subdivision **within the same barangay of similar conditions**.
2. If no zonal value is prescribed for a classification in one barangay, use the same classification in an **adjacent barangay of similar conditions**.
3. In the absence of zonal valuation entirely, value pursuant to RAMO 2-91.

**Source 4 — CTA Zonal Rulings (from existing analysis, cta-zonal-rulings.md):**
Court cases (Emiliano/Gamboa) established that **BIR cannot substitute arbitrary values** — the fallback must follow prescribed rules, not ONETT officer discretion.

**Assessment:** The "highest of three" rule is confirmed. However, the inference that "matching doesn't need to be precise" is only partially correct. The BIR has **formal fallback rules** (same barangay similar conditions, then adjacent barangay), but these are structured fallbacks, not license for imprecise matching. An engine should implement exact matching first, with the structured fallbacks as documented in BIR guidelines. CTA case law shows that improper substitution is legally challengeable.

---

## Claim 3: Address Matching Should Use the Proposed Fallback Hierarchy

**Verdict: PARTIALLY CONFIRMED — the hierarchy is directionally correct but the exact levels need refinement**

### Proposed hierarchy:
1. Exact street + vicinity + classification match
2. Street match with different vicinity (same barangay, same classification)
3. Barangay "All other streets" / catch-all entry
4. Return NULL (no match found)

### Evidence

**Source 1 — BIR RMO 31-2019 (from Makati zonal value schedule preamble):**
The actual BIR-prescribed fallback chain is:
1. Exact match (street/subdivision + classification in barangay)
2. Same classification, **other street/subdivision within same barangay of similar conditions**
3. Same classification, **adjacent barangay of similar conditions**
4. (For institutional properties) Commercial value of nearest property in same barangay
5. (If no zonal value exists at all) RAMO 2-91

**Source 2 — Existing analysis (address-vicinity-patterns.md):**
185 records serve as **barangay-level catch-all entries** ("ALL OTHER STREETS", "ALL LOTS") — confirming that Level 3 of the proposed hierarchy exists in the actual data. The analysis documents these explicitly.

**Source 3 — CTA Rulings (from existing analysis):**
The Emiliano/Gamboa cases confirm that fallback must return NULL rather than interpolate when no prescribed value exists. This validates Level 4.

**Assessment:** Levels 1, 3, and 4 are confirmed. Level 2 needs refinement: the BIR rule is not just "different vicinity in same barangay" but specifically "same classification in another street/subdivision **of similar conditions** within same barangay." The "similar conditions" qualifier is important — it's not any random street but one the RDO deems comparable. The proposed hierarchy is also **missing** the adjacent-barangay fallback (BIR's actual Level 3). The institutional-property special case and the RAMO 2-91 terminal fallback are also missing.

**Recommended revised hierarchy:**
1. Exact street + vicinity + classification match
2. Street match with different vicinity (same barangay, same classification)
3. Barangay catch-all entry ("ALL OTHER STREETS") with same classification
4. Same classification in adjacent barangay of similar conditions
5. Return NULL (no match — defer to assessor's FMV or manual RDO inquiry)

---

## Claim 4: Street Name Aliases Handled by Bidirectional Alias Table

**Verdict: CONFIRMED**

### Evidence

**Source 1 — Wikipedia "List of renamed streets in Metro Manila":**
Comprehensive documented list of renamed streets exists, including the specific example cited (Vito Cruz -> Pablo Ocampo Sr. via Republic Act No. 6731). The list includes hundreds of entries with old name, new name, location, and legal authority. Street renaming is regulated by the National Historical Commission of the Philippines (NHCP) and enacted through Republic Acts, presidential proclamations, or municipal ordinances.

**Source 2 — Existing analysis (address-vicinity-patterns.md):**
211 vicinity values in the actual BIR workbooks contain `(formerly ...)` annotations:
- `1209 PABLO OCAMPO SR. ( formerly VITO CRUZ )`
- `ALEJO AQUINO - PRESIDENT SERGIO OSMEÑA, SR HIGHWAY (formerly SOUTH SUPERHIGHWAY)`
These annotations are already in the BIR data itself, providing a seed dataset for the alias table.

**Source 3 — BIR South Makati (RDO 50) workbook (via carlacalleja.com):**
The BIR workbooks explicitly note aliases: "BRIDAL BOUQUET is the same as BRIDAL", "BATANES is formerly named BATANGAS", "SENIA is the same as ZENIA". This confirms that BIR itself maintains alias information within its workbooks.

**Source 4 — Top Gear Philippines (street renaming explainer):**
Street renaming follows the Local Government Code of 1991. Local roads can be renamed by LGUs; national roads require presidential or congressional action. Despite official renamings, locals and even LRT stations continue using old names (e.g., "Vito Cruz Station" on LRT-1 still commonly used despite the street being officially "Pablo Ocampo Sr.").

**Assessment:** The bidirectional alias table approach is confirmed as both necessary and feasible. Three sources provide seed data: (a) the 211+ `(formerly ...)` annotations already in BIR workbooks, (b) the Wikipedia list of renamed Metro Manila streets, and (c) per-workbook footnotes noting equivalences. The bidirectional nature is essential because BIR workbooks use the **current official name** as primary but annotate former names, while users may search using either old or new names.

---

## Claim 5: Edit Distance / Levenshtein Is Preferable to Token-Based Approaches for Filipino Addresses

**Verdict: PARTIALLY CONFIRMED — edit distance is appropriate for individual components but a HYBRID approach is superior**

### Evidence

**Source 1 — Babel Street (drawbacks of Levenshtein):**
"Levenshtein and Damerau-Levenshtein distances struggle to match information that is out of order." For full addresses where tokens may appear in different orders, pure edit distance produces high false-positive rates or misses valid matches.

**Source 2 — CMU String Distance Metrics paper (Cohen, Ravikumar, Fienberg):**
The SoftTFIDF metric (a hybrid of token-based and edit-based) performs best overall for name matching tasks. It "performs slightly better than either Jaro-Winkler or TFIDF on average, and occasionally performs much better."

**Source 3 — Flagright / Medium (Jaro-Winkler vs Levenshtein comparison):**
For **short strings like street names**, Jaro-Winkler is often preferred over Levenshtein because of its prefix-matching bonus and O(m+n) complexity vs O(m*n). However, for fields where every character position matters equally (like street numbers), Levenshtein is preferred.

**Source 4 — Filipino NLP research (EMNLP 2022, N-Gram + Damerau-Levenshtein):**
Academic work on Filipino text normalization specifically uses **Damerau-Levenshtein** distance combined with N-gram rules. The NLP-Filipino-Words-Normalization project uses Damerau-Levenshtein + Double Metaphone (modified for Filipino).

**Source 5 — libpostal (multilingual address parsing):**
libpostal achieves 99.45% full-parse accuracy globally using statistical NLP trained on OpenStreetMap data. It supports the Philippines but no Philippine-specific benchmarks exist. The approach is fundamentally different from simple edit distance — it uses machine learning on tokenized address components.

**Assessment:** The claim is partially correct. For **individual street name components** (short strings), edit distance (specifically Damerau-Levenshtein or Jaro-Winkler) is indeed effective and validated by Filipino NLP research. However, for the **full address matching problem** involving:
- Abbreviated forms (Brgy., St., Ave.)
- Multi-part names (President Sergio Osmena Sr. Highway)
- Hyphenated compounds (Alabang-Zapote Road)
- Spanish-derived names

...a **hybrid approach** is superior: normalize abbreviations first (token-level), then apply edit distance on individual components. The best practice from multiple sources is: (1) parse/tokenize, (2) normalize abbreviations and expand contractions, (3) apply Jaro-Winkler or Damerau-Levenshtein on individual components, (4) use token-set-ratio for order-independent matching when needed.

The existing analysis already proposes an abbreviation expansion pipeline (ST. -> STREET, AVE. -> AVENUE, etc.) in `address-vicinity-patterns.md`, which is the right preprocessing step before applying edit distance.

---

## Claim 6: Geocoding APIs Are Insufficient for Zonal Value Matching

**Verdict: CONFIRMED**

### Evidence

**Source 1 — Google Maps Geocoding API documentation:**
Google acknowledges that "the accuracy of geocoded locations may vary per country" and "the availability of geocoding data depends on contracts with data providers." For the Philippines, the API returns `location_type` values that may be `APPROXIMATE` or `GEOMETRIC_CENTER` rather than `ROOFTOP` precision. The API "is not designed to cope with ambiguous queries" — a critical limitation given Filipino address format inconsistencies.

**Source 2 — OpenStreetMap Philippines wiki:**
"The current focus of mapping is Metro Manila" and the community is "expanding coverage to other provinces." Address-level data is a work in progress — road networks are prioritized before address data. This confirms that even the most comprehensive open-source geographic data for the Philippines has incomplete address coverage outside Metro Manila.

**Source 3 — PhilGIS defunct status:**
PhilGIS (the Philippine GIS Data Clearinghouse at philgis.org), which was the primary national source for free Philippine geospatial data, **is no longer operational** — the domain redirects to an unrelated gambling site. This confirms the "fragmented and incomplete" characterization of PhilGIS data.

**Source 4 — BIR's address model vs geocoding model (from existing analysis):**
The BIR's NCR model uses **cross-street boundary segments** (e.g., "Shaw Blvd from EDSA to Wack Wack Creek") which represents a linear segment, not a point. Geocoding APIs return point coordinates (latitude/longitude), not street segments between intersections. This is a fundamental model mismatch — confirmed by the loop's Wave 2 analysis of 11,438 cross-street-hyphen entries (40.7% of all vicinity records).

**Source 5 — Precisely API Philippines documentation:**
Even commercial geocoding providers note that "postal geocoding is not available with Philippines" and the country "does not consider postal codes in addresses" — confirming reduced geocoding capability compared to countries with robust postal infrastructure.

**Source 6 — Google Plus Codes:**
Google itself promotes Plus Codes as an alternative "for places that don't have their own street address" in the Philippines, implicitly acknowledging the limitations of traditional geocoding for Philippine addresses.

**Assessment:** All three sub-claims are confirmed:
1. **BIR's segment model vs geocoding point model**: Confirmed. 40.7% of BIR vicinity records are cross-street segments that have no 1:1 mapping to geocoding point results.
2. **Limited Philippine coverage in international geocoding**: Confirmed. Even Google's own documentation hedges on Philippine accuracy, postal geocoding is unavailable, and PhilGIS is defunct.
3. **PhilGIS fragmented/incomplete**: Confirmed. PhilGIS is not just incomplete — it no longer exists. Alternative sources (OSM, Geofabrik, HDX) provide varying but incomplete coverage, especially outside Metro Manila.

The geocoding approach is not entirely useless (it could help with RDO/city-level resolution or as a preprocessing step), but it cannot replace the text-based matching needed for street-level + vicinity-level zonal value lookup.

---

## Summary Table

| Claim | Verdict | Confidence | Sources Used |
|-------|---------|------------|--------------|
| 1. ONETT matches by barangay+street+vicinity | CONFIRMED | High | BIR.gov.ph, RMC 115-2020, Respicio & Co., Loop Wave 2 analysis |
| 2. Highest-of-three means imprecise matching OK | PARTIALLY CONFIRMED | Medium | BIR practitioner sites, RMO 31-2019, CTA rulings |
| 3. Fallback hierarchy (4 levels) | PARTIALLY CONFIRMED | Medium-High | RMO 31-2019 preamble, address-vicinity-patterns.md, CTA rulings |
| 4. Bidirectional alias table for renamed streets | CONFIRMED | High | Wikipedia, BIR workbook annotations (211 entries), Top Gear PH, BIR RDO 50 |
| 5. Edit distance preferable to token-based | PARTIALLY CONFIRMED | Medium | CMU paper, Babel Street, Filipino NLP research, libpostal |
| 6. Geocoding APIs insufficient | CONFIRMED | High | Google Geocoding docs, OSM PH wiki, PhilGIS status, Precisely API, Loop Wave 2 analysis |

## Corrections and Refinements for the Engine Design

### Must-fix:
1. **Claim 3 — Add adjacent-barangay fallback**: The proposed 4-level hierarchy is missing BIR's prescribed "adjacent barangay of similar conditions" fallback. This should be Level 4 (pushing NULL to Level 5).
2. **Claim 3 — Add institutional-property special case**: When the property is a school/hospital/church, BIR prescribes using the commercial value of the nearest property in the same barangay.

### Should-refine:
3. **Claim 2 — "Similar conditions" qualifier**: The fallback from exact match to same-barangay alternative is not unrestricted — it requires "similar conditions." The engine should implement this as classification-constrained matching (same classification code required).
4. **Claim 5 — Use hybrid approach**: Don't rely on pure edit distance. Implement: (a) abbreviation expansion normalization, (b) Jaro-Winkler on individual parsed components, (c) token-set-ratio for order-independent compound name matching.

### Nice-to-have:
5. **Claim 4 — Three seed sources for alias table**: Combine (a) BIR workbook `(formerly ...)` annotations (211+ entries), (b) Wikipedia renamed streets list, (c) per-workbook footnote equivalences. The alias table should be bidirectional and versioned (some streets have been renamed multiple times).
6. **Claim 6 — Geocoding as preprocessing**: While geocoding cannot drive the core lookup, it could be used for (a) city/municipality -> RDO resolution and (b) user input normalization (autocomplete). Consider exposing it as an optional enhancement layer.

## Sources

- [BIR Official Zonal Values Portal](https://www.bir.gov.ph/zonal-values)
- [FileDocsPhil — 2026 Updated BIR Zonal Value](https://www.filedocsphil.com/how-to-look-for-bir-zonal-value/)
- [Respicio & Co. — How to Compute Zonal Value](https://www.respicio.ph/commentaries/how-to-compute-zonal-value-of-property-in-the-philippines)
- [Respicio & Co. — Determining Zonal Values](https://www.respicio.ph/commentaries/determining-zonal-values-for-real-estate-in-the-philippines)
- [U-Property PH — How to Compute FMV](https://upropertyph.com/2023/09/10/how-to-compute-the-fair-market-value-of-your-property-in-the-philippines/)
- [ForeclosurePhilippines — BIR Zonal Values](https://www.foreclosurephilippines.com/what-you-need-to-know-about-bir-zonal-values/)
- [BIR Zonal Value East Makati (RMO 31-2019 preamble)](https://carlacalleja.com/2022/01/03/bir-zonal-value-east-makati-2021/)
- [Wikipedia — List of renamed streets in Metro Manila](https://en.wikipedia.org/wiki/List_of_renamed_streets_in_Metro_Manila)
- [Top Gear PH — Street Renaming Explainer](https://www.topgear.com.ph/features/feature-articles/street-renaming-philippines-explainer-a4682-20231215-lfrm)
- [BIR South Makati Zonal Values (RDO 50)](https://carlacalleja.com/2018/07/27/bir-zonal-value-in-makati/)
- [Babel Street — Drawbacks of Levenshtein](https://www.babelstreet.com/blog/drawbacks-of-levenshtein-distance-algorithms-for-name-matching)
- [CMU — Comparison of String Distance Metrics](https://www.cs.cmu.edu/~wcohen/postscript/ijcai-ws-2003.pdf)
- [Flagright — Jaro-Winkler vs Levenshtein](https://www.flagright.com/post/jaro-winkler-vs-levenshtein-choosing-the-right-algorithm-for-aml-screening)
- [EMNLP 2022 — Filipino Spelling Normalization](https://github.com/ljyflores/efficient-spelling-normalization-filipino)
- [GitHub — libpostal](https://github.com/openvenues/libpostal)
- [Google Geocoding API Best Practices](https://developers.google.com/maps/documentation/geocoding/best-practices)
- [Precisely APIs — Philippines Geocoding](https://docs.precisely.com/docs/sftw/precisely-apis/main/en-us/webhelp/apis/Geocode/Countries/Philippines/PHL.html)
- [OpenStreetMap — Philippines Addressing](https://wiki.openstreetmap.org/wiki/Philippines/Addressing)
- [OpenStreetMap — Philippines Data Sources](https://wiki.openstreetmap.org/wiki/Philippines/Data_sources)
- [PhilGIS (defunct) — via GitHub Gist](https://gist.github.com/mapmakerdavid/71f6fa6c6ebf6055c4336926daac5290)
- [PSA — Philippine Standard Geographic Code](https://psa.gov.ph/classification/psgc)
- [DILG — Masterlist of Barangays](https://www.dilg.gov.ph/page/Masterlist-of-Barangays/77)
- [Manila Bulletin — RMC 115-2020](https://mb.com.ph/2020/10/27/payment-of-capital-gains-tax-no-longer-requires-zonal-value-certificate-bir/)
- [Studylib — Cebu City Zonal Values (RDO 81)](https://studylib.net/doc/8149042/rdo81-cebu-ct-north---mac-realty-services)
- [ZonalValuesPH — Marikina All Other Streets](https://zonalvaluesph.altervista.org/zonal-value-of-all-other-streets-along-marikina-city-whereisit-137402689/)
