# RDO Jurisdiction Mapping — Analysis

**Wave:** 3 — Resolution Logic Deep-Dive
**Date:** 2026-03-03
**Aspect:** rdo-jurisdiction-mapping
**Sources:** RAO 1-2024 (BIR CDN), RAO 4-2019 (DigestPH, 8box Solutions), BIR RDO directory (philpad, filipiknow, techpilipinas, thepinoyofw), SC decision in Makati v. Taguig (G.R. No. 235316, Dec 1, 2021), RA 11938 (Carmona cityhood), RA 12001 (RPVARA), PSA BARMM municipalities notice, Manila Bulletin BIR reorganization coverage, Scribd RDO documents, BIR CDN zonal value PDFs

---

## Summary

The city/municipality-to-RDO mapping is structurally unstable. Five categories of edge cases break the assumption of a clean 1:1 mapping between LGU and RDO: (1) multi-RDO cities where a single city is split across 2-9 RDOs at the barangay level, (2) recent jurisdiction transfers driven by court decisions, (3) Revenue Region reorganizations that reshuffled RDO groupings, (4) newly created LGUs with ambiguous or inherited RDO assignments, and (5) the RPVARA regime shift that will eventually decouple property valuation from BIR RDO jurisdiction entirely. The engine must model jurisdiction at the **barangay level**, not the city level, and must support temporal versioning of jurisdiction assignments.

---

## 1. Recent Jurisdiction Changes (RAOs 2019-2024)

### RAO 1-2024 — Makati/Taguig EMBO Barangay Transfer

**Issued:** January 5, 2024
**Trigger:** Supreme Court Third Division decision (December 1, 2021) in *Makati v. Taguig* (G.R. No. 235316), declared final September 28, 2022.

**What happened:** The SC ruled that the EMBO (Enlisted Men's Barrio) barangays and Fort Bonifacio belong to Taguig City, not Makati City, resolving a 29-year territorial dispute. RAO 1-2024 redefined the jurisdiction of:
- **RDO 50 (South Makati)** — removed EMBO barangays
- **RDO 44 (Taguig-Pateros)** — absorbed EMBO barangays

**10 barangays transferred from RDO 50 to RDO 44:**
Cembo, Comembo, East Rembo, West Rembo, Pembo, Pitogo, South Cembo, Rizal, Post Proper Northside, Post Proper Southside

**Engine implications:**
- RDO 50 jurisdiction changed mid-cycle — zonal value workbooks issued before RAO 1-2024 list these barangays under RDO 50; after, they fall under RDO 44
- The LRA transferred property transactions effective January 1, 2024 (LRA Administrative Order 2024-23)
- Zonal values themselves may not have changed (same physical properties), but the authoritative RDO for lookup purposes shifted
- Temporal awareness: a query for Cembo pre-2024 resolves to RDO 50; post-2024 resolves to RDO 44
- This is the highest-impact jurisdiction change in recent BIR history given BGC's economic significance (729 hectares)

### RAO 4-2019 — Revenue Region 7 and 8 Split

**Issued:** June 19, 2019
**What happened:** Both Revenue Regions 7 (Quezon City) and 8 (Makati City) were split into two regions each, creating four new Revenue Regions:

| Old Region | New Regions | RDOs |
|-----------|------------|------|
| RR 7 (Quezon City) | **RR 7A (Quezon City)**: RDOs 28, 38, 39, 40 | Quezon City proper |
| | **RR 7B (East NCR)**: RDOs 41, 42, 43, 45, 46 | Mandaluyong, San Juan, Pasig, Marikina, Cainta-Taytay |
| RR 8 (Makati City) | **RR 8A (Makati City)**: RDOs 47, 48, 49, 50 | Makati City proper |
| | **RR 8B (South NCR)**: RDOs 44, 51, 52, 53A, 53B | Taguig-Pateros, Pasay, Paranaque, Las Pinas, Muntinlupa |

**Rationale:** Combined tax collection target of P402 billion required closer supervision. Makati region alone was tasked with P229 billion; Quezon City P173 billion.

**Engine implications:**
- RDO numbers and jurisdiction boundaries did NOT change — only the Revenue Region grouping above them changed
- However, Revenue Region is the level at which zonal value workbooks are published (workbook headers reference "RR 8A" not "RR 8")
- Workbooks published before July 2019 reference RR 7/RR 8; after, they reference RR 7A/7B/8A/8B
- The split reveals shared Department Order patterns: Makati's 4 RDOs (47-50) share DOs, South NCR's 3 RDOs share DOs, QC's RDOs share DOs (confirmed in sheet-organization analysis)

### RDO 126 — Digital Taxation Service (New, 2024)

**Created by:** RMO 04-2024
**What it is:** A new RDO dedicated to "significant digital platforms" — not geographically bounded but function-based.
**Location:** BIR Main Office, Agham Road, Quezon City
**Classification:** Large Taxpayer category (alongside RDOs 116-125)

**Engine implications:**
- RDO 126 is NOT relevant for zonal value lookup (it handles income/VAT for digital platforms, not property tax)
- However, it demonstrates that the RDO numbering system is not purely geographic — function-based RDOs exist
- The engine's RDO lookup should filter to geographic RDOs only (RDOs 1-114, roughly) for property jurisdiction purposes

---

## 2. Multi-District Cities — Barangay-Level Mapping

### Makati City: 4 RDOs (47, 48, 49, 50)

All under Revenue Region 8A. Makati is the most granularly split city in the BIR system.

| RDO | Name | Barangays |
|-----|------|-----------|
| **47** | East Makati | San Lorenzo (incl. Legazpi Village, Makati CBD, Greenbelt). Bounded by Sen. Gil Puyat Ave (N), Ayala Ave (E), EDSA (S), Pasong Tamo Extension (W). |
| **48** | West Makati | Bangkal, Magallanes, Palanan, Pio del Pilar, San Isidro. Includes South Superhighway frontage from Palanan to Magallanes Village. |
| **49** | North Makati | Bel-Air (I-IV, **excluding Salcedo Village**), Carmona, Guadalupe Viejo, Kasilawan, La Paz, Olympia, Poblacion (incl. Palm Village & San Miguel Village), San Antonio, Singkamas, Sta. Cruz, Tejeros, Valenzuela. |
| **50** | South Makati | Salcedo Village, Dasmariñas, Forbes Park, Guadalupe Nuevo, Urdaneta, Pinagkaisahan. **Post-RAO 1-2024: EMBO barangays removed** (Cembo, Comembo, East Rembo, West Rembo, Pembo, Pitogo, South Cembo, Rizal → RDO 44). |

**Critical edge case:** Bel-Air barangay is split — Bel-Air goes to RDO 49, but Salcedo Village (which is part of the Bel-Air barangay complex) goes to RDO 50. Boundary lines run along specific streets (Sen. Gil Puyat, Ayala Ave, EDSA, Pasong Tamo Extension), and buildings ON these boundary streets may fall under the adjacent RDO.

### Quezon City: 4 RDOs (28, 38, 39, 40)

All under Revenue Region 7A.

| RDO | Name | Barangays |
|-----|------|-----------|
| **28** | Novaliches | Capri, Sta. Monica, Sta. Lucia, San Bartolome, San Agustin, Sauyo, Kaligayahan, Gulod, Novaliches Proper, Nagkaisang Nayon, Talipapa, Pasong Putik, Bagbag, **Commonwealth (westside only)**, **Culiat (northside only)**, Fairview, Holy Spirit, Pasong Tamo, Sangandaan, **Tandang Sora (northside only)**, New Era, Binuksuk, Damong Maliit |
| **38** | North QC | Vasra, Project 6, Bagong Pag-asa, Sto. Cristo, Ramon Magsaysay, San Antonio, Veterans Village, Bungad, Philam, West Triangle, Alicia, Sta. Cruz, Bahay Toro, Nayong Kaunlaran, Katipunan, Paltok, Paraiso, Paang Bundok, Mariblo, Salvacion, Damayan, Gintong Silahis, Del Monte, Maharlika, Masambong, Lourdes, Talayan, Baesa, Sto. Domingo, Apolonio Samson, Siena, Balon Bato, St. Peter, Unang Sigaw, San Jose, Sta. Teresita, Manresa, Balingasa, Damar, San Isidro Labrador, Pag-ibig sa Nayon, **Culiat (southside only)**, **Tandang Sora (southside only)** |
| **39** | South QC | Bagong Silangan, Batasan Hills, Botocan, **Central Commonwealth (eastside only)**, Damayang Lagi, Don Manuel, Dona Aurora, Dona Josefa, Kalusugan, Kamuning, Kristong Hari, Krus na Ligas, Laging Handa, Loyola Heights, Mariana-New Manila, Matandang Balara, Obrero, Old Capitol Site, Paligsahan, Pansol, Pinyahan, Payatas, Roxas, Sacred Heart, San Isidro, San Vicente, Santol, Sto. Nino, Sikatuna, South Triangle, Tatalon, Teacher's Village East/West, UP Campus, UP Village |
| **40** | Cubao | Amihan, Masagana, Project 3, San Roque, Quirino 2, Libis, East Kamias, Villa Ma. Clara, Duyan Duyan, Pinagkaisahan, Quirino 3, Cubao, Marilag, Bagumbayan, Silangan, Santolan, Bagumbuhay, Immaculate Conception, Escopa, Socorro, West Kamias, Murphy, Manga, Kanluran, Milagrosa, San Martin, Project 4, Talampas, Tagumpay, Bagong Lipunan, E. Rodriguez, Horse Shoe, Bayanihan, Ugong Norte, Dioquino, N. Valencia |

**Critical edge case — intra-barangay splits:** Three barangays in Quezon City are split across two RDOs based on road boundaries:
1. **Barangay Commonwealth** — westside of Don Mariano Marcos Ave/Litex Road goes to RDO 28; eastside goes to RDO 39
2. **Barangay Culiat** — northside of Tandang Sora Ave goes to RDO 28; southside goes to RDO 38
3. **Barangay Tandang Sora** — northside of Tandang Sora Ave goes to RDO 28; southside goes to RDO 38

This is the most extreme edge case: the same barangay name maps to DIFFERENT RDOs depending on street address. A barangay-only lookup is insufficient for these 3 cases — the engine must resolve to the street level.

### Manila: 6 RDOs (29-34) + 3 island RDOs (35-37)

All under Revenue Region 6. Manila's RDO boundaries follow the city's historical district structure.

| RDO | Name | Coverage |
|-----|------|----------|
| **29** | San Nicolas-Tondo | Tondo, San Nicolas districts |
| **30** | Binondo | Binondo district |
| **31** | Sta. Cruz | Sta. Cruz district |
| **32** | Quiapo-Sampaloc-Sta. Mesa-San Miguel | Quiapo, Sampaloc, Sta. Mesa, San Miguel districts |
| **33** | Intramuros-Ermita-Malate | Intramuros, Ermita, Malate districts (zone-based breakdown: Zones 68-70 Intramuros, Zones 77-79 Malate) |
| **34** | Paco-Pandacan-Sta. Ana-San Andres | Paco, Pandacan, Sta. Ana, San Andres districts |
| **35** | Romblon | Island district (NOT Manila) |
| **36** | Puerto Princesa | Island district (NOT Manila) |
| **37** | San Jose, Occidental Mindoro | Island district (NOT Manila) |

**Critical note:** RDOs 35, 36, 37 are numbered sequentially after Manila's RDOs but cover geographically distant island districts (Romblon, Palawan, Occidental Mindoro). This is a historical artifact of Revenue Region 6's broad jurisdiction. The engine must NOT assume RDO number ranges imply geographic proximity.

Manila uses a zone-based sub-barangay addressing system. Barangays are numbered (e.g., Barangay 165, 271, 289) and grouped into zones (e.g., Zone 27, Zone 68). Zonal value workbooks reference specific barangay numbers and zones, making Manila's address resolution more structured than other multi-RDO cities but requiring a barangay-number-to-zone-to-district mapping.

### Other Multi-RDO Cities

| City | RDOs | Revenue Region |
|------|------|---------------|
| Cebu City | 83, 84 | RR 13 |
| Davao City | 113A, 113B | RR 19 |

These follow simpler geographic splits (north/south or east/west) without the intra-barangay splits seen in QC.

---

## 3. Newly Created LGUs and RDO Impact

### City of Carmona, Cavite (2023) — Municipality-to-City Upgrade

**Legal basis:** RA 11938, signed February 23, 2023; ratified by plebiscite July 8, 2023
**Status:** Carmona became the 149th city in the Philippines, first under the amended cityhood rules (RA 11683, 2022)
**Previous RDO:** RDO 54A (Trece Martires City - South Cavite), Revenue Region 9A (CABAMIRO)
**Current RDO:** **Same — RDO 54A**. No RDO reassignment occurred. Carmona remains grouped with Alfonso, Amadeo, GMA, Gen. Aguinaldo, Imus, Indang, Mendez, Silang, Tagaytay, and Trece Martires under RDO 54A.

**Engine implication:** Municipality-to-city conversion does NOT trigger RDO reassignment. The engine's LGU-to-RDO mapping should use the geographic territory, not the LGU classification (city vs. municipality).

### BARMM Newly Created Municipalities (2024)

**Legal basis:** Bangsamoro Autonomous Acts 41-48 (September 2022); ratified by plebiscite April 13, 2024
**8 new municipalities:** Pahamuddin, Kadayangan, Nabalawag, Old Kaabakan, Kapalawan, Malidegao, Tugunan, Ligawasan
**Origin:** Carved from barangays of existing North Cotabato municipalities (Pigcawayan, Midsayap, Aleosan, Kaabakan, Carmen, Pikit) that joined BARMM's Special Geographic Area in 2019

**RDO assignment: UNKNOWN.** No BIR Revenue Memorandum Order or RAO has been publicly identified assigning these 8 new municipalities to specific RDOs. The parent municipalities were under:
- **RDO 107 (Cotabato City)** — Revenue Region 18
- **RDO 108 (Kidapawan City)** — Revenue Region 18

**Complicating factor:** Under the Bangsamoro Organic Law, BARMM is expected to establish its own Bangsamoro Revenue Office (BRO) with revenue-raising powers. The interaction between BIR RDOs and eventual BARMM revenue administration is uncharted. These municipalities may straddle two tax regimes.

**Engine implication:** The 8 new BARMM municipalities present a coverage gap. The engine should:
1. Default them to parent municipality RDOs until explicit assignment is published
2. Flag them as "jurisdiction pending confirmation"
3. Monitor for BIR issuances formalizing their RDO status

### RA 11683 Pipeline — Future Cityhood Conversions

RA 11683 (2022) lowered cityhood requirements. Pending/proposed conversions include: Liloan (Cebu), Talavera (Nueva Ecija), Manolo Fortich (Bukidnon), Labo (Camarines Norte), Daraga (Albay), La Trinidad (Benguet), Mexico (Pampanga), Malay (Aklan, home of Boracay), Alabel (Sarangani). Based on the Carmona precedent, none of these would trigger RDO reassignment upon conversion.

---

## 4. Historical Revenue Region Reorganizations

### The 2019 RR7/RR8 Split (RAO 4-2019)

This is the most significant recent Revenue Region reorganization. Full details in Section 1 above.

**Key structural insight:** The split did not create new RDOs or change RDO jurisdiction boundaries. It only reorganized which RDOs report to which Regional Director. However, because zonal value Department Orders are issued at the Revenue Region level, this created a versioning break:
- Pre-2019 DOs reference "RR 7" or "RR 8"
- Post-2019 DOs reference "RR 7A", "RR 7B", "RR 8A", or "RR 8B"
- Parser must normalize both naming conventions to the same RDO identifiers

**Historical regionalization timeline:**
- 1955: First 2 regional offices (Cebu, Davao)
- 1957: Expanded to 10 regional offices
- Various expansions through the 1990s-2000s
- 2019: RR7 → RR7A/7B, RR8 → RR8A/8B
- Current: ~19 Revenue Regions, 124 RDOs

### Revenue Region Structure (Current, 2025)

| Revenue Region | Designation | Key RDOs |
|---------------|-------------|----------|
| RR 1 | Calasiao, Pangasinan | 1-5 (Ilocos/Pangasinan) |
| RR 2 | Tuguegarao, Cagayan | 6-8 (Cagayan Valley) |
| RR 3 | Pampanga | 9-12 (Central Luzon north) |
| RR 4 | San Fernando, Pampanga | 13-16 (Central Luzon south) |
| RR 5 | Caloocan City | 17-27 (North NCR + Bulacan) |
| RR 6 | City of Manila | 29-37 (Manila + islands) |
| RR 7A | Quezon City | 28, 38-40 (QC proper) |
| RR 7B | East NCR | 41-43, 45-46 (Mandaluyong-Marikina corridor) |
| RR 8A | Makati City | 47-50 (Makati proper) |
| RR 8B | South NCR | 44, 51-53B (Taguig-Muntinlupa corridor) |
| RR 9A | CABAMIRO | 54A-57 (Cavite-Batangas-Mindoro-Romblon) |
| RR 9B | Calabarzon South | 58-60 (Laguna-Quezon) |
| RR 10 | Legazpi, Albay | 61-64 (Bicol) |
| RR 11 | Iloilo City | 65-72 (Western Visayas) |
| RR 12 | Bacolod City | 73-78 (Negros-Siquijor) |
| RR 13 | Cebu City | 79-86 (Central Visayas) |
| RR 14 | Tacloban | 87-91 (Eastern Visayas) |
| RR 16 | Cagayan de Oro | 92-98 (Northern Mindanao) |
| RR 17 | Butuan City | 99-101 (Caraga) |
| RR 18 | Cotabato City | 102-111 (Central/Southern Mindanao) |
| RR 19 | Davao City | 112-114 (Davao region) |
| LTS | Large Taxpayers | 115-127 (function-based, not geographic) |

---

## 5. RPVARA Impact on the Jurisdiction Model

### The Fundamental Shift

Under the pre-RPVARA system:
- **BIR RDOs** are the authoritative jurisdiction for zonal values
- Property is valued by the RDO covering the geographic location
- Jurisdiction = BIR RDO

Under RPVARA (post-transition):
- **BLGF + local assessors** are the authoritative jurisdiction for SMVs
- Property is valued by the LGU assessor where the property is located
- Jurisdiction = city/municipality/province assessor

This is a **structural decoupling.** BIR RDOs will still exist (they handle income tax, VAT, etc.), but they will no longer be the authority for property valuation. The jurisdiction for valuation shifts from ~124 RDOs to ~1,700 LGU assessors.

### Implications for the Engine

**Near-term (2024-2027):** BIR RDO jurisdiction mapping remains essential because:
- BIR zonal values are still operative for most jurisdictions (Section 31 saving clause)
- The engine must know which RDO's workbook contains the zonal values for a given property
- RDO → workbook → sheet → barangay → classification is the lookup path

**Medium-term (2027-2029):** Dual jurisdiction model:
- For jurisdictions with BLGF-approved SMVs: LGU assessor jurisdiction is authoritative for property values
- For jurisdictions without: BIR RDO jurisdiction still applies (Section 29(b))
- The engine must maintain both mapping systems and detect which applies

**Long-term (2029+):** If RPVARA succeeds:
- BIR RDO-to-property jurisdiction mapping becomes irrelevant for valuation
- LGU assessor jurisdiction (city/municipality) becomes the sole mapping
- This is actually simpler — 1 city = 1 assessor = 1 SMV, no multi-RDO splits

**Transition risk:** During the dual period, a property in Quezon City might have:
- BIR zonal value from RDO 39 (South QC) for the specific barangay
- BLGF SMV from the Quezon City Assessor for the same barangay
- The two values may differ significantly
- The engine must apply the correct regime rule: Section 29(b) three-way max if no BLGF SMV exists; Section 18(c) two-way max if BLGF SMV exists

---

## 6. Complete Edge Case Taxonomy

### Category A: Intra-Barangay Splits (Street-Level Resolution Required)

| City | Barangay | Split Between | Boundary |
|------|----------|--------------|----------|
| Quezon City | Commonwealth | RDO 28 / RDO 39 | Don Mariano Marcos Ave / Litex Road |
| Quezon City | Culiat | RDO 28 / RDO 38 | Tandang Sora Avenue |
| Quezon City | Tandang Sora | RDO 28 / RDO 38 | Tandang Sora Avenue |
| Makati City | Bel-Air complex | RDO 49 / RDO 50 | Salcedo Village carved out to RDO 50 |

**Resolution strategy:** For these 4 cases, the engine needs a secondary lookup by street address or sub-barangay (village) name. A hardcoded exception table is appropriate given the small number.

### Category B: Multi-RDO Cities (Barangay-Level Resolution Required)

| City | RDO Count | Barangay Count | Notes |
|------|----------|---------------|-------|
| Manila | 6 (29-34) | 897 | Zone-based numbering system |
| Quezon City | 4 (28, 38-40) | 142 | 3 barangays split (see Cat. A) |
| Makati City | 4 (47-50) | ~33 | EMBO barangays transferred to RDO 44 in 2024 |
| Cebu City | 2 (83, 84) | 80 | North/south split |
| Davao City | 2 (113A, 113B) | 182 | Geographic split |

**Resolution strategy:** Full barangay-to-RDO mapping table required. ~1,334 barangay-to-RDO entries for these 5 cities alone.

### Category C: Temporal Jurisdiction Changes

| Event | Date | RDO Affected | Change |
|-------|------|-------------|--------|
| RAO 4-2019 (RR split) | June 2019 | All NCR RDOs | Revenue Region renumbering (not RDO boundary change) |
| RAO 1-2024 (EMBO transfer) | January 2024 | RDO 44, RDO 50 | 10 barangays transferred |
| RMO 04-2024 (RDO 126) | 2024 | None geographic | New function-based RDO |

**Resolution strategy:** Jurisdiction mapping must be date-aware. A `valid_from` / `valid_until` field on each barangay-to-RDO entry enables temporal queries.

### Category D: Ambiguous/Pending Assignments

| LGU | Issue | Suggested Resolution |
|-----|-------|---------------------|
| 8 BARMM municipalities (2024) | No published RDO assignment | Default to parent municipality RDO; flag as pending |
| Carmona City (2023) | Converted from municipality | No change — remains RDO 54A |
| Future cityhood conversions | RA 11683 pipeline | No RDO change expected (Carmona precedent) |

### Category E: Non-Geographic RDOs (Exclude from Property Lookup)

| RDO | Type | Exclude? |
|-----|------|---------|
| 115-125 | Large Taxpayers Service | Yes |
| 126 | Digital Taxation Service | Yes |
| 127 | Other LTS | Yes |

---

## 7. Mapping Table Design

### Recommended Schema

```
jurisdiction_map:
  - barangay_id: u32         // PSA PSGC code (9-digit)
  - rdo_code: u8             // 1-114 (geographic only)
  - revenue_region: string   // "7A", "8B", etc.
  - city_municipality: string
  - province: string
  - valid_from: date         // effective date of this mapping
  - valid_until: date | null // null = current
  - source: string           // RAO number, e.g., "RAO 1-2024"
  - split_qualifier: string | null  // for Cat. A cases: "westside of Don Mariano Marcos Ave"
```

### Size Estimate

- ~42,000 barangays nationwide
- With temporal versioning for the ~10 known boundary changes: ~42,050 rows
- At ~64 bytes per row: ~2.7 MB uncompressed, ~400 KB compressed
- Trivially fits in WASM bundle alongside zonal value data

### Data Sources for Populating

1. **PSA Philippine Standard Geographic Code (PSGC)** — authoritative barangay list with codes
2. **BIR RDO directory** — lists cities/municipalities per RDO (but NOT barangays for most RDOs)
3. **BIR zonal value workbooks** — contain barangay names per RDO (most granular source)
4. **RAO documents** — for temporal boundary changes
5. **Manual compilation** — required for the 5 multi-RDO cities where barangay-to-RDO mapping is not published in a single source

### Known Data Gaps

1. **No single BIR publication** lists the complete barangay-to-RDO mapping for all 124 RDOs
2. **Provincial RDOs** often cover 5-16 municipalities — the workbook itself is the most reliable mapping source
3. **BARMM municipalities** (8 new, 2024) have no confirmed RDO assignment
4. **PSGC codes for BARMM municipalities** may not yet be assigned by PSA

---

## 8. Design Recommendations for the Engine

### R1: Model jurisdiction at barangay level, not city level
The existence of multi-RDO cities and intra-barangay splits makes city-level mapping insufficient. Use PSGC barangay codes as the primary key.

### R2: Implement a 3-tier jurisdiction lookup
1. **Exact barangay match** — resolves 99%+ of cases
2. **Street-level disambiguation** — for the 4 known intra-barangay splits (QC Commonwealth, Culiat, Tandang Sora; Makati Bel-Air/Salcedo)
3. **City-level fallback** — if barangay not found, return all RDOs for the city with a disambiguation prompt

### R3: Add temporal versioning to jurisdiction entries
Critical for the EMBO transfer (RAO 1-2024). Each mapping entry should carry `valid_from` and optionally `valid_until`. Default queries use the current mapping; historical queries resolve by date.

### R4: Exclude non-geographic RDOs from property lookup
RDOs 115+ are function-based (Large Taxpayers, Digital Taxation). The property jurisdiction lookup should filter to RDOs 1-114 only.

### R5: Build the RPVARA regime detection layer
For each LGU, track whether a BLGF-approved SMV exists. This determines which tax base formula applies:
- No BLGF SMV → use BIR ZV, apply Section 29(b) three-way max
- BLGF SMV exists → use BLGF SMV, apply Section 18(c) two-way max

### R6: Use zonal value workbooks as the authoritative barangay-to-RDO mapping source
The workbooks themselves are the most reliable mapping source — they list every barangay covered by each RDO. During the data ingestion pipeline, extract the barangay-to-RDO mapping as a side effect of parsing workbooks.

---

## Sources

- RAO 1-2024: [BIR CDN PDF](https://bir-cdn.bir.gov.ph/BIR/pdf/Digest%20RAO%201-2024.pdf)
- RAO 4-2019: [DigestPH](https://www.digest.ph/taxation/splitting-of-revenue-region-no-7-quezon-city-and-revenue-region-no-8-makati-city-and-redefining-their-areas-of-jurisdiction) | [8box Solutions](https://8box.solutions/rao-no-4-2019/)
- SC Makati v. Taguig: [SC Press Release](https://sc.judiciary.gov.ph/sc-writes-finis-to-makati-city-taguig-city-land-dispute/) | [Manila Bulletin](https://mb.com.ph/2023/4/3/sc-declares-final-2021-decision-on-taguig-city-makati-city-land-dispute)
- RR7/8 Split Coverage: [Manila Bulletin](https://mb.com.ph/2019/06/20/bir-forms-two-regions-in-metro-manila-to-monitor-more-than-p400-b-taxes/)
- Makati RDO Barangays: [FilipiKnow North Makati](https://filipiknow.net/rdo-code-north-makati/) | [FilipiKnow South Makati](https://filipiknow.net/rdo-code-south-makati/) | [FilipiKnow East Makati](https://filipiknow.net/rdo-code-east-makati/) | [FilipiKnow West Makati](https://filipiknow.net/rdo-code-west-makati/)
- QC RDO Barangays: [FilipiKnow North QC](https://filipiknow.net/rdo-code-north-quezon-city/) | [FilipiKnow South QC](https://filipiknow.net/rdo-code-south-quezon-city/) | [TomTax Blog](https://tomtax.blogspot.com/2012/05/rdo-28-novaliches-and-rdo-38-north.html)
- Manila RDO Structure: [Scribd RDO Directory](https://www.scribd.com/document/709683349/BIR-RDO-Directory) | [PhilipineCPA](https://www.philippinecpa.com/2011/07/revenue-district-office-directory.html)
- Carmona Cityhood: [RA 11938](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/96362) | [Rappler](https://www.rappler.com/philippines/luzon/carmona-cavite-officially-becomes-city-after-plebiscite-july-2023/)
- BARMM Municipalities: [PSA](https://www.psa.gov.ph/content/eight-new-municipalities-bangsamoro-autonomous-region-muslim-mindanao) | [PNA](https://www.pna.gov.ph/articles/1222583)
- BIR RDO Codes (2025): [PhilPad](https://philpad.com/bir-rdo-codes-updated-list/) | [FilipiKnow](https://filipiknow.net/rdo-code/) | [TechPilipinas](https://techpilipinas.com/bir-rdo-codes/)
- RPVARA: [RA 12001 (LawPhil)](https://lawphil.net/statutes/repacts/ra2024/ra_12001_2024.html) | [BLGF MC 001-2025 IRR](https://blgf.gov.ph/wp-content/uploads/2025/03/BLGF-MC-No.-001.2025-IRR-of-RA-No.-12001-or-the-RPVARA-Reform-Act-6-Jan-2025-Approved-3.pdf)
- BIR History: [Wikipedia](https://en.wikipedia.org/wiki/Bureau_of_Internal_Revenue)
