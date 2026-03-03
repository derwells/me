# BIR Zonal Value Workbook -- Condo Table Pattern Inventory

Generated: 2026-03-03
Source: 10 NCR workbooks (RDO 30, 41, 43, 44, 47, 48, 49, 50, 51, 52)

---

## Summary of Distinct Patterns Found

Six distinct condo table layout patterns were identified across the 10 workbooks:

| Pattern | Workbooks | Columns | Merged Cells | Condo Section Marker |
|---------|-----------|---------|--------------|---------------------|
| A: Flat 4-col, no merges | RDO 43 (Pasig), RDO 44 (Taguig) | C0=Name, C1=Vicinity, C2=Code, C3=ZV | None for condo blocks | "CONDOMINIUM / TOWNHOUSES" or "CONDOMINIUMS:****" |
| B: Flat 5-col, no merges | RDO 47 (East Makati) | C0=Name, C1=Vicinity, C2=Code, C3=ZV | None | Inline with regular streets |
| C: 4-col with block merges | RDO 48 (West Makati), RDO 49 (North Makati), RDO 50 (South Makati), RDO 51 (Pasay), RDO 52 (Paranaque) | C0=Name, C1=Vicinity, C2=Code, C3=ZV | C0:C1 merged across 2-4 rows per building | "LIST OF CONDOMINIUMS" or "CONDOMINIUMS/TOWNHOUSES (CCT)" |
| D: Multi-col with revision history | RDO 30 (Binondo) | C0=Zone, C1=Street, C2=Class, C3-C9=Revisions | C0 merged across blocks | Inline with regular entries |
| E: 4-col flat, Mandaluyong style | RDO 41 (Mandaluyong) | C0=Name, C1=Vicinity, C2=Code, C3=ZV | None | "CONDOMINIUMS:" header |
| F: BGC cluster-based | RDO 44 (Taguig, BGC section) | C0=Name, C1=Vicinity, C2=Code, C3=ZV | None | "CONDOMINIUMS:****" + cluster subheaders |

---

## Pattern A: Flat 4-Column, No Block Merges (Pasig, Taguig non-BGC)

### Workbooks
- RDO No. 43 - Pasig City.xls (5459 rows, 4 cols, 313 merged cells total)
- RDO No. 44 - Taguig-Pateros.xlsx (non-BGC barangays)

### Column Layout
```
C0: STREET NAME/ SUBDIVISION/ CONDOMINIUM
C1: VICINITY
C2: CLASSI-FICATION (split across 2 header rows)
C3: 7TH REV ZV.SQ.M (or 8TH REVISION ZV/SQ M for Taguig)
```

### Header Structure
- Header spans 2 rows via merge: R106:108 C0:1 merges "STREET NAME/ SUBDIVISION/ CONDOMINIUM"
- Classification header split: R106 has "CLASSI-", R107 has "FICATION"

### Condo Entry Format
Each building occupies 1 row per classification code. Building name appears ONLY on the first row (RC row typically). Subsequent rows (PS, CC) have empty C0.

```
R264: C0='ALLEGRA GARDEN PLACE - AMINA'   C1='PASIG BLVD-BAGONG ILOG'  C2='RC'  C3='110000'
R265: C0='ALLEGRA GARDEN PLACE - SORAYA'  C1='PASIG BLVD-BAGONG ILOG'  C2='RC'  C3='110000'
R266: C0='ALLEGRA GARDEN PLACE - AMINA / SORAYA'  C1='PASIG BLVD-BAGONG ILOG'  C2='PS'  C3='77000'
R267: C0='CONTINENTAL VENTURE CONDO'       C1='BAGONG ILOG'             C2='RC'  C3='75000'
R268:                                                                    C2='PS'  C3='52500'
```

### Key Observations
- **Tower differentiation**: Tower names appear in C0 as separate entries (e.g., "SYNC RESIDENCES - S TOWER" and "SYNC RESIDENCES - Y TOWER" on separate rows)
- **Shared parking slots**: Some PS rows reference multiple towers: "ALLEGRA GARDEN PLACE - AMINA / SORAYA" in C0
- **Condo section header**: Non-merged text row "CONDOMINIUM / TOWNHOUSES" precedes condo entries within a barangay
- **Footnotes**: Asterisk-marked notes appear after condo blocks, e.g.: "* Phoenix Heights Condo (RC) - Geographically located at this Bgy but listed also at Bgy Oranbo"
- **No CC entries for most Pasig condos**: Many condos have only RC + PS (no CC)
- **Taguig non-BGC** uses same flat pattern with 4-row blocks: RC, PS(for RC), CC, PS(for CC)

### Parking Slot Organization (Pasig)
- PS appears immediately after its parent RC row
- PS value = 70% of RC value (consistent ratio)
- When no CC exists, only RC + PS appear

### Taguig Non-BGC Condo Blocks (4-row pattern)
```
R301: C0='ALDER RESIDENCES**'        C1='ACACIA ESTATES'  C2='RC'  C3='122000'
R302:                                                      C2='PS'  C3='85400'
R303:                                                      C2='CC'  C3='152000'
R304:                                                      C2='PS'  C3='106400'
```
Each condo = exactly 4 rows: RC, PS(residential), CC, PS(commercial)

---

## Pattern B: Flat 5-Column, No Block Merges (East Makati)

### Workbook
- RDO No. 47 - East Makati.xls (608 rows, 5 cols, 44 merged cells total)

### Column Layout
```
C0: Building name (or zone number + name)
C1: Street/Vicinity
C2: Classification code
C3: Zonal value (ZV/SQ.M)
C4: (appears to be unused/historical)
```

### Condo Entry Format
Condos appear INLINE with regular street entries. No separate condo section. Each building uses 2-3 rows:

```
R214: C0='AMORSOLO CONDOMINIUM'  C1='AMORSOLO ST.'              C2='RC'  C3='85000'
R215:                                                             C2='CC'  C3='100000'
R216:                                                             C2='PS'  C3='70000'
R217: C0='AMORSOLO MANSION'      C1='AMORSOLO - V.A. RUFINO'    C2='RC'  C3='85000'
R218:                                                             C2='CC'  C3='95000'
R219:                                                             C2='PS'  C3='70000'
```

### Key Observations
- **No merged cells for condo blocks**: All values are flat single-cell entries
- **Building name in C0 only on first row** of a multi-row block
- **Zone numbers embedded**: Some building names have zone numbers: "6764 STI HOLDING CENTER*", "6776 SECURITY BANK*"
- **Parenthetical aliases on PS rows**: "C0='(FORMERLY PACIFIC BANK MAKATI CONDO)' C2='PS' C3='140000'" -- the alias text appears in C0 of a subsequent row
- **3-row pattern is dominant**: RC, CC, PS (order: residential, commercial, parking)
- **Some buildings are CC-only**: "CACHO GONZALES" has only CC + PS (no RC)
- **Large condo inventory**: 302 condo entries in a single flat list

### Parking Slot Organization
- PS always follows its parent classification codes
- A single PS value serves the entire building (not separate PS for RC and CC)
- PS value is approximately 70% of RC

---

## Pattern C: 4-Column with Block Merges (West/North/South Makati, Pasay, Paranaque)

### Workbooks
- RDO No. 48 - West Makati.xls (878 rows, 4 cols, 438 merges)
- RDO No. 49 - North Makati City.xls (similar structure)
- RDO No. 50 - South Makati.xls (3385 rows, 4 cols, 1373 merges)
- RDO No. 51 - Pasay City.xls (4987 rows, 4 cols, 3314 merges)
- RDO No. 52 - Paranaque City.xls (2168 rows, 8 cols, 185 merges)

### Column Layout
```
C0: STREET/SUBDIVISION/CONDOMINIUM/TOWNHOUSES (or STREET NAME/ SUBDIVISION/CONDOMINIUM)
C1: VICINITY
C2: CLASSIFICATION
C3: 8TH REV. ZV./SQM (or 9TH REV ZV/SQ.M for Paranaque)
```
Header merges span 2 rows: R111:113 C0:1 etc.

### Condo Section Markers
```
R149: 'LIST OF CONDOMINIUMS'  (South Makati, merged C0:C3)
R441: 'CONDOMINIUMS/TOWNHOUSES (CCT)'  (Pasay, merged C0:C3)
R828: 'CONDOMINIUMS/TOWNHOUSES (CCT)'  (Pasay, another barangay)
```

### Building Block Structure (Merged C0:C1)
The building name and vicinity are MERGED vertically across 2-4 rows:

**South Makati 2-row block (CC + PS only):**
```
R150: C0='139 CORPORATE CENTER'  C1='VALERO'  C2='CC'  C3='155000'   <- MERGE R150:152 C0:1
R151:                                          C2='PS'  C3='108000'   <- same merge
```

**South Makati 4-row block (RC + PS + CC + PS):**
```
R165: C0='ALFARO PLACE'  C1='SALCEDO/V.A.RUFINO'  C2='RC'  C3='175000'  <- MERGE R165:169 C0:1
R166:                                               C2='PS'  C3='122000'
R167:                                               C2='CC'  C3='200000'
R168:                                               C2='PS'  C3='140000'
```

**South Makati 3-row block (CC + RC + PS or CC + PS + variant):**
```
R245: C0='CITIBANK TOWER **'  C1='PASEO DE ROXAS'  C2='CC'  C3='220000'  <- MERGE R245:248 C0:1
R246:                                                C2='RC'  C3='180000'
R247:                                                C2='PS'  C3='155000'
```

### Pasay Under-Construction Section
A special section header exists:
```
R256: 'CONDOMINIUMS (CCT) UNDER CONSTRUCTION'  (merged C0:C3)
R838: 'CONDOMINIUMS (CCT) UNDER CONSTRUCTION'  (another barangay)
R1158: 'CONDOMINIUMS (CCT) UNDER CONSTRUCTION'
```

Under-construction condos use the SAME 4-row merged block format:
```
R257: C0='LA VIDA'  C1='F. B. HARRISON - GOTAMCO'  C2='RC'  C3='155000'  <- MERGE R257:261
R258:                                                C2='PS'  C3='107000'
R259:                                                C2='CC'  C3='200000'
R260:                                                C2='PS'  C3='126000'
```

### Paranaque PH (Penthouse) Code
Paranaque introduces the PH classification code, unique among all workbooks examined:
```
R496: C0='LANCRIS'        C2='RC'  C3='87000'
R497:                     C2='CC'  C3='109000'
R498: C0='*'              C2='PH'  C3=''       <- NO value provided, asterisk only
R499:                     C2='PS'  C3='75000'
```
The PH row has NO zonal value -- it is a placeholder indicating penthouse exists. The asterisk (*) in C0 links to a footnote. The Paranaque file uses 4 columns (C0-C3) but the header reference shows 8 cols in the sheet.

### Paranaque Condo Column Layout (8-col sheet)
```
C0: STREET NAME/ SUBDIVISION/CONDOMINIUM
C1: VICINITY
C2: CLASSIFI-CATION (split across 2 header rows)
C3: 9TH REV ZV/SQ.M
C4-C7: Historical revision columns (mostly empty for condos)
```

### Penthouse Footnotes (South Makati)
The South Makati workbook has explicit penthouse rules in footnotes:
```
'3) If no zonal value has been prescribed for Penthouse, the value should be 110% of CC,
    and in the absence thereof, 120% of RC.'
'4) The ground floor of the Residential Condominium shall be classified as commercial
    and twenty percent (20%) of the established value shall be added thereto.'
```

### Penthouse Entries (South Makati)
South Makati has explicit penthouse entries with separate merged blocks:
```
R3242:3244 C0:1 = 'ONE ROXAS TRIANGLE CONDO (Penthouse)'
R3257:3259 C0:1 = 'PARK CENTRAL(Penthouse) *'
R3277:3279 C0:1 = 'TWO ROXAS(Penthouse) *'
```

### Parking Slot Organization
- PS appears IMMEDIATELY after its parent classification (RC -> PS_for_RC, CC -> PS_for_CC)
- PS values are consistently ~70% of their parent classification value
- When building has both RC and CC, there are TWO separate PS entries
- Default rule from footnotes: "If no zonal value has been prescribed for parking slots, the value should be 60% of the amount of the unit sold"

### Developer/New Building Notes
Every barangay section ends with a boilerplate note (merged across C0:C3):
```
'Developer/Owner of condominium project built after the effectivity of this revision
 shall request for an assignment of values from the Technical Committee on Real Property
 Valuation.'
```

### Footnote Asterisk System
```
*      New building identified in the 8th revision
**     New building identified in the 8th revision
***    For this 7th Revision - Parking Slot (PS) is 60% of the unit
****   Existing buildings with updated values
*****  Existing in the 7th Revision. Penthouse is added in the 8th Revision.
****** Added per TCRPV Resolution (e.g., Levitown Villas)
```

---

## Pattern D: Multi-Column with Revision History (Binondo)

### Workbook
- RDO No. 30 - Binondo.xls (526 rows, 10 cols)

### Column Layout
```
C0: ZONE NO.
C1: STREET/BARANGAY/SUBDIVISION
C2: CLASSIFICATION
C3: ZONAL VALUE (earliest revision)
C4: (empty or revision column)
C5: ZONAL VALUE (later revision)
C6: ZONAL VALUE
C7: 4th REVISION
C8: 5th REVISION
C9: (empty)
```

### Header Structure (R105-107)
Header spans 3 rows with complex merging:
```
R105:107 C7:8 = '4th REVISION'   (2r x 1c)
R105:107 C8:9 = '5th REVISION'   (2r x 1c)
```

### Condo Entry Format
Condos appear mixed with regular land entries. They use the CLASSIFICATION column (C2) with RC/CC/PS codes but building names appear in the STREET column (C1):

```
R150: C0='0059' C1='GOTESCO CONDO' C2='CC' C5='23000' C6='23000' C7='28000' C8='42000'
R151:            C1=''              C2='PS' C5='16000' C6='16000' C7='20000' C8='29000'
```

### Key Observations
- **Zone numbers in C0**: Each entry has a zone number (4-digit)
- **Building names in C1**: The street column doubles as the building name column
- **Multiple revision values**: Zonal values appear in C5, C6, C7, C8 for different revision periods
- **No merged cells for condo blocks**: All condo entries are flat
- **Minimal condo inventory**: Only a few condos (Gotesco Condo, etc.) exist in Binondo
- **PS follows CC directly**: Parking always follows commercial classification

---

## Pattern E: 4-Column Flat, Mandaluyong Style

### Workbook
- RDO No. 41 - Mandaluyong City.xls

### Column Layout
```
C0: STREET/SUBDIVISION/CONDOMINIUM/ TOWNHOUSES
C1: V I C I N I T Y
C2: CLASSIFICATION
C3: 8TH REVISION ZV/SQ M
```

### Header Structure
```
R324: C0='STREET/SUBDIVISION/CONDOMINIUM/ TOWNHOUSES'  C1='V I C I N I T Y'  C2='CLASSIFICATION'  C3='8TH REVISION ZV/SQ M'
```

### Condo Section Header
```
R300: C0='CONDOMINIUMS:****'
```

### Condo Entry Format
4-row blocks, NO merges, flat layout:
```
R301: C0='ALDER RESIDENCES**'   C1='ACACIA ESTATES'  C2='RC'  C3='122000'
R302:                                                  C2='PS'  C3='85400'
R303:                                                  C2='CC'  C3='152000'
R304:                                                  C2='PS'  C3='106400'
R305: C0='CEDAR CREST CONDO'   C1='ACACIA ESTATES'   C2='RC'  C3='115000'
R306:                                                  C2='PS'  C3='80500'
R307:                                                  C2='CC'  C3='140000'
R308:                                                  C2='PS'  C3='98000'
```

### Key Observations
- **Strict 4-row blocks**: Every condo has exactly RC, PS, CC, PS
- **PS values paired**: PS for RC appears after RC, PS for CC appears after CC
- **"ALL OTHER EXISTING CONDOMINIUMS"** catch-all entry at end of section:
  ```
  R326: C0='ALL OTHER EXISTING CONDOMINIUMS'  C2='RC'  C3='114000'
  R327:                                        C2='PS'  C3='79800'
  R328:                                        C2='CC'  C3='139000'
  R329:                                        C2='PS'  C3='97300'
  ```
- **Footnote system**:
  ```
  * Added Institutional (X) Values to Identified Streets/Villages/Subdivisions
  ** Added Newly Identified Streets/Villages/Subdivisions
  *** Agricultural Value (A50) on All other Street was removed
  **** The CONDOMINIUMS header marker itself
  ```

---

## Pattern F: BGC Cluster-Based (Taguig BGC section)

### Workbook
- RDO No. 44 - Taguig-Pateros.xlsx (BGC section, starting around row 834)

### Column Layout (same as Pattern A)
```
C0: STREET/SUBDIVISION/CONDOMINIUM/ TOWNHOUSES
C1: V I C I N I T Y
C2: CLASSIFICATION
C3: 8TH REVISION ZV/SQ M
```

### Unique Feature: BGC Cluster Sub-Headers
BGC condos are organized under named "clusters":
```
R834: C0='CONDOMINIUMS:********'
R835: C0='BONIFACIO CENTER CLUSTER (BC)'     <- cluster sub-header, no code/value
R836: C0='ALVEO PARK TRIANGLE*****'          C2='CC'  C3='345000'
R837:                                         C2='PS'  C3='241500'
R838: C0='EAST GALLERY PLACE*****'  C1='26TH ST. CORNER 9TH ST., BONIFACIO CENTER'  C2='RC'  C3='348000'
R839:                                         C2='PS'  C3='243600'
R840:                                         C2='CC'  C3='395000'
R841:                                         C2='PS'  C3='276500'
```

### BGC Condos with Vicinity Addresses
Unlike other patterns, BGC condos have detailed street addresses in C1:
```
C0='F1 CITY CENTER / FORT ONE'  C1='32ND ST. CORNER LANE A'
C0='HIGH STREET SOUTH CORPORATE PLAZA (CORPLAZA TOWER)'  C1='26TH ST. CORNER 9TH ST., BONIFACIO CENTER'
C0='ONE MARIDIEN'  C1='26TH ST. CORNER 9TH ST., BONIFACIO CENTER'
C0='VERVE RESIDENCES TOWER 2'  C1='26TH ST. CORNER 7TH AVENUE BC, BGC'
```

### Key Observations
- **Very high ZV values**: BGC condos have ZV values 2-5x higher than other NCR areas (e.g., 345000 vs 85000)
- **CC-first for some buildings**: Some BGC buildings start with CC instead of RC (e.g., ALVEO PARK TRIANGLE)
- **4-row blocks**: RC, PS, CC, PS pattern (or CC, PS, RC, PS for commercial-first)
- **Tower differentiation**: "VERVE RESIDENCES" and "VERVE RESIDENCES TOWER 2" are separate entries
- **Cluster grouping**: BGC condos are organized by cluster (e.g., "BONIFACIO CENTER CLUSTER (BC)")
- **No merged cells**: All entries are flat single-row per classification

---

## Cross-Cutting Findings

### 1. Classification Code Usage Across All Workbooks

| Code | Meaning | Present In |
|------|---------|-----------|
| RC | Residential Condominium | All 10 workbooks |
| CC | Commercial Condominium | All 10 workbooks |
| PS | Parking Slot | All 10 workbooks |
| PH | Penthouse | Only RDO 52 (Paranaque) as explicit code |
| PC | (not found in any workbook) | None |

### 2. Parking Slot Pairing Rules

**Two-PS pattern** (most common in Pattern C, E, F):
```
Building Name    RC    value_rc
                 PS    ~70% of RC    <- parking for residential unit
                 CC    value_cc
                 PS    ~70% of CC    <- parking for commercial unit
```

**Single-PS pattern** (Pattern B, some Pattern A):
```
Building Name    RC    value_rc
                 CC    value_cc
                 PS    ~70% of RC    <- single parking value for entire building
```

### 3. Default Calculation Rules (from footnotes)

- **Parking slot default**: 60% of the unit value (when no specific PS value prescribed)
- **Penthouse default**: 110% of CC, or 120% of RC if no CC
- **Ground floor RC**: Classified as commercial + 20% premium on established value
- **Specific parking valuations**: When workbook footnote says "*Valuation for parking spaces were made specific for each type of condominium", each PS row has its own explicit value

### 4. Catch-All Entries

Several workbooks have catch-all condo entries:
```
"ALL OTHER EXISTING CONDOMINIUMS"  (Mandaluyong R326, Taguig R326)
"ALL OTHER CONDOMINIUMS"           (South Makati R1618, R1687)
```
These provide default ZV values for condos not individually listed.

### 5. Building Name Patterns

- **Tower numbering**: "TOWER 1", "TOWER 2", "TOWER I", "TOWER II" as suffixes
- **Phase naming**: "PHASE 1", separate entries per phase
- **Parenthetical aliases**: "(formerly Cityland Condo VII)", "(now FIRST E-BANK CONDO CORP.)"
- **Penthouse suffix**: "(Penthouse)" appended to building name as separate merged block (South Makati)
- **Tower+Building combined**: "BAY GARDEN CLUB & RESIDENCES (18-STOREY BUILDING)" vs "BAY GARDEN CLUB & RESIDENCES (3-TOWER RESIDENTIAL)"
- **Under construction indicator**: Special section header, NOT a per-building flag

### 6. Per-Unit vs Per-SQM Indicators

ALL zonal values in ALL workbooks are **per square meter (per SQ.M.)**. This is indicated by:
- Header column: "ZV./SQM", "ZV/SQ.M", "ZV.SQ.M", "ZV/SQ M"
- No per-unit pricing was found in any workbook

### 7. Merged Cell Patterns Summary

| Pattern | Merge Style | Rows per Building | Merge Scope |
|---------|------------|-------------------|-------------|
| A (Pasig, Taguig) | None | 2-4 rows | No merges |
| B (East Makati) | None | 2-3 rows | No merges |
| C (West/North/South Makati, Pasay, Paranaque) | C0:C1 vertical | 2-4 rows | Building name + vicinity merged vertically |
| D (Binondo) | C0 for zone blocks | Varies | Zone number merged across multiple streets |
| E (Mandaluyong) | None | 4 rows | No merges |
| F (BGC) | None | 2-4 rows | No merges |

### 8. Special Condo Footnotes Found

**South Makati (RDO 50)**:
```
'* New building identified in the 8th revision'
'***** Existing in the 7th Revision. Penthouse is added in the 8th Revision.'
'2) Specific value is provided for RC and CC in the 8th Revision.
    If no zonal value has been prescribed for parking slots,
    the value should be 60% of the amount of the unit sold'
'3) If no zonal value has been prescribed for Penthouse,
    the value should be 110% of CC, and in the absence thereof, 120% of RC.'
'4) The ground floor of the Residential Condominium shall be classified as
    commercial and twenty percent (20%) of the established value shall be added thereto.'
'Note: Developer/Owner of condominium project and townhouse in all Barangays
    built after the effectivity of this revision shall request for assignment
    of zonal values (ZVG) from the Technical Committee of Real Property Valuation (TCRPV).'
```

**Paranaque (RDO 52)**:
```
'*** Newly added/identified, condominium and classification'
'***** Landco Condo is renamed / the same as Alexcy One Building.'
'****** Levitown Villas was added per (TCRPV) Resolution No. 04-2019 dated August 6, 2019.'
'NOTE: DEVELOPERS/OWNERS OF CONDOMINIUM PROJECTS IN THIS BARANGAY BUILT AFTER THE
 EFFECTIVITY OF THIS REVISION SHALL REQUEST FOR AN ASSIGNMENT OF ZONAL VALUES (ZVS)
 FROM THE TECHNICAL COMMITTEE ON REAL PROPERTY VALUATION (TCRPV)'
```

**Pasay (RDO 51)**:
```
'*Newly identified condominium'
'*Valuation for parking spaces were made specific for each type of condominium'
```

---

## Raw Data Samples by Workbook

### RDO 30 - Binondo (Pattern D)

Sheet: 'Sheet 6 (DO 62-17)', 526 rows x 10 cols
Headers at R105-107 (3-row merged header)
```
R105: C0='ZONE NO' C1='STREET / BARANGAY / SUBDIVISION' C2='CLASSIFICATION' C7='4th REVISION' C8='5th REVISION'
```

Sample condo entry:
```
R150: C0='0059' C1='GOTESCO CONDO' C2='CC' C5='23000' C6='23000' C7='28000' C8='42000'
R151:                               C2='PS' C5='16000' C6='16000' C7='20000' C8='29000'
```

### RDO 41 - Mandaluyong (Pattern E)

Sheet: 'Sheet 8 (DO 40-2023)', 4 cols
Header at R324:
```
C0='STREET/SUBDIVISION/CONDOMINIUM/ TOWNHOUSES'
C1='V I C I N I T Y'
C2='CLASSIFICATION'
C3='8TH REVISION ZV/SQ M'
```

Condo section starts with:
```
R300: C0='CONDOMINIUMS:****'
```

Full condo listing (all entries are 4-row RC/PS/CC/PS blocks):
```
ALDER RESIDENCES** (ACACIA ESTATES) - RC=122000, PS=85400, CC=152000, PS=106400
CEDAR CREST CONDO (ACACIA ESTATES) - RC=115000, PS=80500, CC=140000, PS=98000
IVORY WOOD CONDO (ACACIA ESTATES) - RC=115000, PS=80500, CC=140000, PS=98000
MULBERRY PLACE** (ACACIA ESTATES) - RC=115000, PS=80500, CC=140000, PS=98000
ALL OTHER EXISTING CONDOMINIUMS - RC=114000, PS=79800, CC=139000, PS=97300
```

### RDO 43 - Pasig (Pattern A)

Sheet: 'Sheet 9 (DO 24-2023)', 5459 rows x 4 cols, 313 merged cells
Header at R106-108:
```
C0='STREET NAME/ SUBDIVISION/ CONDOMINIUM'
C1='VICINITY'
C2='CLASSI-' (R106) / 'FICATION' (R107)
C3='7TH REV' (R106) / 'ZV.SQ.M' (R107)
```

Sample condo entries per barangay:
```
Bagong Ilog:
  ALLEGRA GARDEN PLACE - AMINA (RC=110000), -SORAYA (RC=110000), shared PS=77000
  CONTINENTAL VENTURE CONDO (RC=75000, PS=52500)
  DONA FELISA I CONDO (RC=85000, PS=59500)
  HILLCREST RESIDENCES (RC=90000, PS=63000)
  LUMIERE RESIDENCES PASIG (RC=100000, PS=70000)
  PHOENIX HEIGHTS CONDO (RC=90000, PS=63000)
  PRISMA RESIDENCES (RC=110000, PS=77000)
  SYNC RESIDENCES - S TOWER (RC=135000)
  SYNC RESIDENCES - Y TOWER (RC=135000)
```

### RDO 44 - Taguig-Pateros (Patterns A + F)

Sheet: 'Sheet 8 (DO 40-2023)' (.xlsx), 4 cols

Non-BGC section header/pattern:
```
R300: C0='CONDOMINIUMS:****'
R301: C0='ALDER RESIDENCES**' C1='ACACIA ESTATES' C2='RC' C3='122000'
R302: C2='PS' C3='85400'
R303: C2='CC' C3='152000'
R304: C2='PS' C3='106400'
```

BGC section with cluster headers:
```
R834: 'CONDOMINIUMS:********'
R835: 'BONIFACIO CENTER CLUSTER (BC)'
R836: ALVEO PARK TRIANGLE***** -> CC=345000, PS=241500
R838: EAST GALLERY PLACE***** -> RC=348000, PS=243600, CC=395000, PS=276500
R842: F1 CITY CENTER / FORT ONE -> RC=250000, PS=175000, CC=295000, PS=206500
R846: HIGH STREET SOUTH CORPORATE PLAZA (CORPLAZA TOWER) -> CC=338000, PS=236600
R848: ONE MARIDIEN -> RC=256000, PS=179200, CC=300000, PS=210000
R852: TWO MARIDIEN -> RC=256000, PS=179200, CC=300000, PS=210000
R856: VERVE RESIDENCES -> RC=253000, PS=177100, CC=300000, PS=210000
R860: VERVE RESIDENCES TOWER 2 -> RC=253000, PS=177100, CC=300000, PS=210000
```

### RDO 47 - East Makati (Pattern B)

Sheet: 'Sheet 8 (DO 37-2021)', 608 rows x 5 cols, 44 merged cells

Condos inline with streets, 3-row blocks (RC/CC/PS):
```
R206: C0='6764  STI HOLDING CENTER*' C1='AYALA AVE' C2='CC' C3='150000'
R207: C2='PS' C3='105000'
R208: C0='6776   SECURITY BANK*' C1='AYALA AVE.' C2='CC' C3='200000'
R209: C0='(FORMERLY PACIFIC BANK MAKATI CONDO)' C2='PS' C3='140000'
R214: C0='AMORSOLO CONDOMINIUM' C1='AMORSOLO ST.' C2='RC' C3='85000'
R215: C2='CC' C3='100000'
R216: C2='PS' C3='70000'
R220: C0='ASIA TOWER' C1='PASEO DE ROXAS' C2='RC' C3='170000'
R221: C2='CC' C3='205000'
R222: C2='PS' C3='145000'
R280: C0='ETON PARKVIEW GREENBELT' C1='GAMBOA ST.' C2='RC' C3='195000'
R281: C2='CC' C3='225000'
R282: C2='PS' C3='160000'
R306: C0='GARDEN TOWER I' C1='EAST ST., AYALA CENTER' C2='RC' C3='240000'
```

### RDO 48 - West Makati (Pattern C)

Sheet: 'Sheet 9 (DO 36-2021)', 878 rows x 4 cols, 438 merged cells

Condo blocks with vertical merges:
```
R193:196 C0:1 = 'GLOBAL TOWER CONDO' / 'M REYES COR MASCARDO'  (3r merge)
  R193: RC=98000
  R194: CC=120000
  R195: PS=84000

R202:205 C0:1 = 'THE ASPEN RESIDENCES'  (3r merge)
R207:210 C0:1 = 'THE MANCHESTER PLACE'  (3r merge)
R222:225 C0:1 = 'WEST TOWER CONDOMINIUM *****'  (3r merge)
R552:555 C0:1 = 'AIC BURGUNDY CORPORATE TOWER'  (3r merge)
R588:591 C0:1 = 'LAUREANO DE TREVI TOWER I, II and III'  (3r merge)
```

### RDO 50 - South Makati (Pattern C)

Sheet: 'Sheet 9 (DO 38-2021)', 3385 rows x 4 cols, 1373 merged cells
Largest condo inventory in all workbooks examined.

LIST OF CONDOMINIUMS section starts at R149.

Sample merged condo blocks:
```
R150:152 C0:1 = '139 CORPORATE CENTER' / 'VALERO' (2r) -> CC=155000, PS=108000
R152:154 C0:1 = '6797 AYALA AVE. CONDO (SLC Building)' / 'AYALA AVE.' (2r)
R165:169 C0:1 = 'ALFARO PLACE (formerly Cityland Condo VII)' (4r) -> RC=175000, PS=122000, CC=200000, PS=140000
R269:273 C0:1 = 'CLASSICA TOWER' (4r)
R275:279 C0:1 = 'CORDOVA CONDOMINIUM' (4r)
```

Penthouse entries (separate merged blocks):
```
R3239:3242 C0:1 = 'ONE ROXAS TRIANGLE CONDO****' (3r) -> CC, RC, PS
R3242:3244 C0:1 = 'ONE ROXAS TRIANGLE CONDO (Penthouse)*****' (2r) -> separate penthouse block
R3257:3259 C0:1 = 'PARK CENTRAL(Penthouse) *' (2r)
R3277:3279 C0:1 = 'TWO ROXAS(Penthouse) *' (2r)
```

BGC condos in South Makati (added entries):
```
R2800:2802 C0:1 = 'VERVE RESIDENCES (Added)' (2r)
R2808:2810 C0:1 = 'VERVE RESIDENCES TOWER 2 (Added)' (2r)
R2811:2813 C0:1 = 'ARYA RESIDENCES TOWER 1 (Added)' (2r)
R2813:2815 C0:1 = 'ARYA RESIDENCES TOWER 2 (Added)' (2r)
R2839:2841 C0:1 = 'AVIDA TOWERS TURF BGC TOWER 1 (Added)' (2r)
R2866:2868 C0:1 = 'PARK TRIANGLE RESIDENCES (Added)' (2r)
R2871:2873 C0:1 = 'UPTOWN PARKSUITES (Added)' (2r)
R2875:2877 C0:1 = 'UPTOWN RITZ RESIDENCES (Added)' (2r)
```

### RDO 51 - Pasay City (Pattern C)

Sheet: 'Sheet 7 (DO 43-2023)', 4987 rows x 4 cols, 3314 merged cells

Condo section header pattern:
```
'CONDOMINIUMS/TOWNHOUSES (CCT)'  (merged C0:C3, 1r)
'CONDOMINIUMS (CCT) UNDER CONSTRUCTION'  (merged C0:C3, 1r) -- UNIQUE TO PASAY
```

Under construction condos (same block format as completed):
```
R257:261 = 'LA VIDA' / 'F. B. HARRISON - GOTAMCO' (4r) -> RC=155000, PS=107000, CC=200000, PS=126000
```

Completed condos:
```
R284:288 = 'SOMERSET MANSION CONDOMINIUM' / 'LEVERIZA STREET' (4r) -> RC=68000, PS=48000, CC=78000, PS=55000
R337:341 = 'BREEZE RESIDENCES' / 'ROXAS BLVD. cor. BUENDIA' (4r) -> RC=159000, PS=112000, CC=205000, PS=144000
R442:446 = 'ALEN (ALIN) CONDOMINIUM I' (4r)
R683:687 = 'FEROSA CONDOMINIUM' (4r)
R839:843 = '2201 RESIDENCES' (4r)
R873:877 = 'GRAND VIEW TOWER CONDOMINIUM' (4r)
R1094:1098 = 'SUNVAR CONDO' (4r)
R1603:1607 = 'BUENDIA TOWER' (4r)
R2295:2299 = 'MACTAN TOWER' (4r)
R2327:2331 = 'SEA RESIDENCES (SMDC)' (4r)
R2523:2527 = 'PARK AVENUE MANSION' (4r)
R3380:3384 = 'ZAMORA SKY TOWER*' (4r)
R4399:4403 = 'DASMAN RESIDENCES' (4r)
R4678:4682 = 'BELMONT CONDO' (4r)
```

### RDO 52 - Paranaque City (Pattern C variant)

Sheet: 'Sheet 10 (DO 049-23)', 2168 rows x 8 cols, 185 merged cells

Column header:
```
C0: STREET NAME/ SUBDIVISION/CONDOMINIUM
C1: VICINITY
C2: CLASSIFI- / CATION (split across 2 rows)
C3: 9TH REV / ZV/SQ.M
```

PH (Penthouse) code usage:
```
R496: C0='LANCRIS'  C2='RC'  C3='87000'
R497:               C2='CC'  C3='109000'
R498: C0='*'        C2='PH'  C3=''       <- UNIQUE: PH code with no value
R499:               C2='PS'  C3='75000'
```

Regular condos:
```
R488: C0='BLUE GEM CONDO'  C2='RC'  C3='62000'
R489:                       C2='CC'  C3='78000'
R490:                       C2='PS'  C3='54000'
R491: C0='CITY HOMES RITZ TOWER'  C2='RC'  C3='62000'
R492:                              C2='CC'  C3='78000'
R493:                              C2='PS'  C3='54000'
R500: C0='LEVITOWN VILLAS******'  C2='RC'  C3='70000'
R501: C0='******'                  C2='CC'  C3='88000'
R502: C0='******'                  C2='PS'  C3='61000'
```

Note: Paranaque uses asterisk references in the C0 column for subsequent classification rows (e.g., '******' in C0 for CC and PS rows of LEVITOWN VILLAS).

---

## Extraction Script Reference

The extraction was performed by `/home/runner/work/me/me/loops/reverse-ph-zonal-value-engine/input/bir-workbook-samples/extract_condo_v2.py`.
Full raw output (83K lines): `/home/runner/work/me/me/loops/reverse-ph-zonal-value-engine/input/bir-workbook-samples/condo_extraction_results.txt`.
