# Condo Table Structures — Analysis

**Wave:** 2 — Data Format Analysis
**Date:** 2026-03-03
**Aspect:** `condo-table-structures`
**Sources:** 31 BIR zonal value workbooks (24 NCR + 7 provincial), condo_pattern_inventory.md (83K-line extraction)

---

## Summary

Condo table formats across BIR zonal value workbooks are significantly more complex than land entries. Analysis of 31 workbooks identified **6 distinct NCR condo layout patterns** and **2 provincial variants**, with cross-cutting differences in:
- Building name encoding (flat vs. merged blocks vs. inline)
- Classification code ordering (RC-first vs. CC-first)
- Parking slot pairing (dual-PS vs. single-PS)
- Section demarcation (dedicated headers vs. inline mixing)
- Special entry types (penthouse, under-construction, storey-based tiers)

**Key finding:** ALL zonal values are **per square meter** — no per-unit pricing exists in any workbook. The "per-unit" claim in some references (including RMO 31-2019 Annex B notes) refers to the fact that condo ZVs combine land and improvement value into a single composite rate, unlike land-only ZVs. The header column universally reads "ZV/SQ.M" or equivalent.

**Condo data volume:** ~9,712 condo-classified rows (RC + CC + PS) across 31 workbooks = 12.7% of total NCR data and 1.7% of provincial data. Estimated ~15,000-20,000 condo rows across all 124 RDOs.

---

## NCR Condo Layout Patterns (6 Patterns)

### Pattern A: Flat 4-Column, No Block Merges
**Workbooks:** RDO 43 (Pasig), RDO 44 (Taguig non-BGC)
**Coverage:** 2 of 24 NCR workbooks (8%)

| Column | Content |
|--------|---------|
| C0 | Building name (first row only) |
| C1 | Vicinity / street location |
| C2 | Classification code (RC/CC/PS) |
| C3 | Zonal value per sqm |

**Building block structure:** Each condo = 2-4 rows, no merged cells. Building name appears ONLY on the first row; subsequent classification rows have empty C0.

```
R264: C0='ALLEGRA GARDEN PLACE - AMINA'   C1='PASIG BLVD-BAGONG ILOG'  C2='RC'  C3='110000'
R265: C0='ALLEGRA GARDEN PLACE - SORAYA'  C1='PASIG BLVD-BAGONG ILOG'  C2='RC'  C3='110000'
R266: C0='ALLEGRA GARDEN PLACE - AMINA / SORAYA'  C1='PASIG BLVD-BAGONG ILOG'  C2='PS'  C3='77000'
R267: C0='CONTINENTAL VENTURE CONDO'       C1='BAGONG ILOG'             C2='RC'  C3='75000'
R268:                                                                    C2='PS'  C3='52500'
```

**Distinct features:**
- Tower differentiation via name suffixes: "SYNC RESIDENCES - S TOWER" / "SYNC RESIDENCES - Y TOWER"
- Shared parking: PS row references multiple towers: "ALLEGRA GARDEN PLACE - AMINA / SORAYA"
- Section marker: "CONDOMINIUM / TOWNHOUSES" (non-merged text row)
- Taguig non-BGC uses strict 4-row blocks: RC, PS(residential), CC, PS(commercial)
- Footnote cross-references: "* Phoenix Heights Condo (RC) - Geographically located at this Bgy but listed also at Bgy Oranbo"

---

### Pattern B: Flat 5-Column, No Block Merges
**Workbooks:** RDO 47 (East Makati)
**Coverage:** 1 of 24 NCR workbooks (4%)

| Column | Content |
|--------|---------|
| C0 | Building name (or zone number + name) |
| C1 | Street/Vicinity |
| C2 | Classification code |
| C3 | Zonal value per sqm |
| C4 | Historical/unused |

**Unique characteristics:**
- Condos appear **INLINE** with regular street entries — no separate condo section
- 3-row blocks dominate: RC, CC, PS (order: residential, commercial, parking)
- **Single PS per building** — one parking value serves entire building (not separate PS for RC and CC)
- Zone numbers embedded in building names: "6764 STI HOLDING CENTER*"
- Parenthetical aliases on PS rows: "(FORMERLY PACIFIC BANK MAKATI CONDO)" appears in C0 of a PS row
- Some buildings are CC-only: "CACHO GONZALES" has only CC + PS (no RC)
- Largest flat condo inventory: 302 entries in a single list

```
R214: C0='AMORSOLO CONDOMINIUM'  C1='AMORSOLO ST.'  C2='RC'  C3='85000'
R215:                                                 C2='CC'  C3='100000'
R216:                                                 C2='PS'  C3='70000'
```

---

### Pattern C: 4-Column with Vertical Block Merges
**Workbooks:** RDO 48 (West Makati), RDO 49 (North Makati), RDO 50 (South Makati), RDO 51 (Pasay), RDO 52 (Parañaque)
**Coverage:** 5 of 24 NCR workbooks (21%) — the dominant merge-based pattern

| Column | Content |
|--------|---------|
| C0 | Building name (merged vertically across all classification rows) |
| C1 | Vicinity (merged with C0) |
| C2 | Classification code |
| C3 | Zonal value per sqm |

**Merge geometry:** C0:C1 merged vertically across 2-4 rows per building. Building name and vicinity are locked together in a single merged region.

```
R165: C0='ALFARO PLACE'  C1='SALCEDO/V.A.RUFINO'  C2='RC'  C3='175000'  ← MERGE R165:169 C0:1
R166:                                               C2='PS'  C3='122000'
R167:                                               C2='CC'  C3='200000'
R168:                                               C2='PS'  C3='140000'
```

**Section markers (merged across C0:C3, full row):**
- "LIST OF CONDOMINIUMS" (South Makati)
- "CONDOMINIUMS/TOWNHOUSES (CCT)" (Pasay)
- "CONDOMINIUMS (CCT) UNDER CONSTRUCTION" (Pasay — unique marker)

**Under-construction section (Pasay-specific):**
Pasay is the only workbook with a dedicated under-construction condo section. These condos use the same 4-row merged block format as completed condos but appear under a separate header. Under-construction condos still have assigned ZVs.

```
R256: 'CONDOMINIUMS (CCT) UNDER CONSTRUCTION'  (merged C0:C3)
R257: C0='LA VIDA'  C1='F. B. HARRISON - GOTAMCO'  C2='RC'  C3='155000'  ← MERGE R257:261
R258:                                                C2='PS'  C3='107000'
R259:                                                C2='CC'  C3='200000'
R260:                                                C2='PS'  C3='126000'
```

**Penthouse entries (South Makati — unique):**
South Makati has explicit penthouse entries as separate merged blocks with "(Penthouse)" appended to the building name:
```
R3242:3244 C0:1 = 'ONE ROXAS TRIANGLE CONDO (Penthouse)'
R3257:3259 C0:1 = 'PARK CENTRAL(Penthouse) *'
R3277:3279 C0:1 = 'TWO ROXAS(Penthouse) *'
```

**PH (Penthouse) classification code (Parañaque — unique):**
Parañaque introduces the PH code as an explicit classification, but with **no zonal value assigned**:
```
R496: C0='LANCRIS'  C2='RC'  C3='87000'
R497:               C2='CC'  C3='109000'
R498: C0='*'        C2='PH'  C3=''       ← UNIQUE: PH code, no value
R499:               C2='PS'  C3='75000'
```

**Parañaque asterisk-reference pattern:**
Subsequent classification rows use asterisks in C0 to reference the building name:
```
R500: C0='LEVITOWN VILLAS******'  C2='RC'  C3='70000'
R501: C0='******'                  C2='CC'  C3='88000'
R502: C0='******'                  C2='PS'  C3='61000'
```

**Developer/new building boilerplate:**
Every barangay condo section ends with (merged C0:C3):
```
'Developer/Owner of condominium project built after the effectivity of this revision
 shall request for an assignment of values from the Technical Committee on Real Property
 Valuation.'
```

---

### Pattern D: Multi-Column with Revision History
**Workbooks:** RDO 30 (Binondo)
**Coverage:** 1 of 24 NCR workbooks (4%)

| Column | Content |
|--------|---------|
| C0 | Zone number (4-digit) |
| C1 | Street/building name |
| C2 | Classification code |
| C3-C4 | Early revision ZVs |
| C5-C6 | Mid revision ZVs |
| C7 | 4th revision ZV |
| C8 | 5th revision ZV |

**Unique characteristics:**
- Condos appear mixed inline with regular land entries
- Building names occupy the STREET column (C1) — no separate condo identifier
- Zone numbers in C0 enable zone-based lookup (unique to Binondo)
- Multiple revision values visible side-by-side (historical comparison)
- Minimal condo inventory (Binondo is predominantly commercial land)
- Block merges: 3-4 row × 4-col blocks for condo names (unique merge geometry)

```
R150: C0='0059' C1='GOTESCO CONDO' C2='CC' C5='23000' C7='28000' C8='42000'
R151:                               C2='PS' C5='16000' C7='20000' C8='29000'
```

---

### Pattern E: 4-Column Flat, Mandaluyong Style
**Workbooks:** RDO 41 (Mandaluyong)
**Coverage:** 1 of 24 NCR workbooks (4%)

Same column layout as Pattern A but with distinct organizational features:
- **Strict 4-row blocks:** Every condo has exactly RC → PS → CC → PS (no exceptions)
- **"CONDOMINIUMS:****" section header** with quadruple asterisk
- **"ALL OTHER EXISTING CONDOMINIUMS" catch-all** at end of section — provides default ZVs for unlisted condos

```
R300: C0='CONDOMINIUMS:****'
R301: C0='ALDER RESIDENCES**'   C1='ACACIA ESTATES'  C2='RC'  C3='122000'
R302:                                                  C2='PS'  C3='85400'
R303:                                                  C2='CC'  C3='152000'
R304:                                                  C2='PS'  C3='106400'
...
R326: C0='ALL OTHER EXISTING CONDOMINIUMS'  C2='RC'  C3='114000'
R327:                                        C2='PS'  C3='79800'
R328:                                        C2='CC'  C3='139000'
R329:                                        C2='PS'  C3='97300'
```

---

### Pattern F: BGC Cluster-Based
**Workbooks:** RDO 44 (Taguig — BGC section only)
**Coverage:** 1 of 24 NCR workbooks (4%), but within a workbook that also uses Pattern A for non-BGC areas

**Unique characteristics:**
- **Cluster sub-headers:** BGC condos organized by named clusters (e.g., "BONIFACIO CENTER CLUSTER (BC)")
- **Very high ZVs:** 2-5× higher than other NCR areas (₱345,000 vs ₱85,000 typical)
- **Detailed vicinity addresses:** Unlike other patterns, BGC condos have full street addresses: "26TH ST. CORNER 9TH ST., BONIFACIO CENTER"
- **CC-first for some buildings:** "ALVEO PARK TRIANGLE" starts with CC, not RC
- **Tower differentiation:** "VERVE RESIDENCES" and "VERVE RESIDENCES TOWER 2" as separate entries

```
R834: C0='CONDOMINIUMS:********'
R835: C0='BONIFACIO CENTER CLUSTER (BC)'          ← cluster sub-header
R836: C0='ALVEO PARK TRIANGLE*****'  C2='CC'  C3='345000'
R837:                                 C2='PS'  C3='241500'
R838: C0='EAST GALLERY PLACE*****'   C1='26TH ST. CORNER 9TH ST.'  C2='RC'  C3='348000'
R839:                                 C2='PS'  C3='243600'
R840:                                 C2='CC'  C3='395000'
R841:                                 C2='PS'  C3='276500'
```

---

## Provincial Condo Patterns (2 Variants)

### Variant G: Cebu Urban (CC-First, Storey-Based Tiers)
**Workbooks:** RDO 81 (Cebu City North)
**Condo-classified rows:** 117 (of ~2,359 total rows)

**Key differences from NCR:**
1. **CC-first ordering is dominant:** 88 CC-first blocks vs 68 RC-first blocks (56% vs 44%). NCR overwhelmingly uses RC-first.
2. **"PARKING SLOT" as explicit building name:** 21 of 50 PS entries have "PARKING SLOT" written in the building name column (C0) instead of leaving it empty. This is a Cebu-specific convention.

```
R1093: C0='GOLDEN PEAK CONDO'  C2='CC'  C3='112000'
R1094: C0='PARKING SLOT'       C2='PS'  C3='74000'
```

3. **Storey-based catch-all tiers — UNIQUE to Cebu:** Catch-all entries are split by building height:
```
R568: C0='ALL OTHER CONDOMINIUMS'                    C2='CC*'  C3='91000'
R569: C0='(small and medium, 7 storeys and below)'   C2='RC*'  C3='74000'
R570:                                                 C2='PS*'  C3='37000'
R571: C0='ALL OTHER CONDOMINIUMS'                    C2='CC*'  C3='131500'
R572: C0='(8 storeys and above)'                     C2='RC*'  C3='112500'
R573:                                                 C2='PS*'  C3='75500'
```

The storey threshold varies slightly: "7 Storeys and below" vs "8 storeys and above" in most barangays, but some use "small and medium" qualifier. This creates a **two-tier pricing system** with significant premiums (44-78% higher for taller buildings).

4. **PC (Parking Commercial) code:** Used in 2 barangays instead of PS, with lower values:
```
R1155: C0='ALL OTHER CONDOMINIUM'                    C2='CC'  C3='81000'
R1156: C0='(small and medium, 7 storeys and below)'  C2='RC'  C3='59000'
R1157:                                                C2='PC'  C3='29500'  ← PC not PS
```

5. **CR/RR used instead of CC/RC:** One barangay (R1461-1463) uses CR* and RR* codes for its "ALL OTHER CONDOMINIUMS" catch-all instead of the standard CC/RC:
```
R1461: C0='ALL OTHER CONDOMINIUMS'  C2='CR*'  C3='117500'  ← CR not CC
R1462:                               C2='RR*'  C3='112500'  ← RR not RC
R1463:                               C2='PS*'  C3='72500'
```

6. **Per-barangay ALL OTHER CONDOMINIUMS:** Nearly every barangay has its own catch-all entry (confirmed in 25+ barangays). This is far more pervasive than NCR where only some workbooks have it.

7. **Section marker:** Simple "CONDOMINIUMS" text (no asterisks, no "LIST OF", no "CCT" qualifier)

### Variant H: Provincial Suburban (CALABARZON)
**Workbooks:** RDO 57 (Biñan/Sta. Rosa/Cabuyao, Laguna)
**Condo-classified rows:** 13 (of ~4,166 total rows — <0.3%)

**Key differences:**
1. **Inline with subdivisions:** Condos appear mixed with subdivision entries, no separate section
2. **RC-only entries common:** Many condos have only RC (no CC or PS)
3. **Named condos with catch-all notes:** "PROMENADE CONDOMINIUM" (RC=₱102,000), "PROMENADE MASTERPIECE CONDOMINIUM" (RC=₱144,500), "MERIDIAN CONDOMINIUM" (RC=₱102,000) — each with PS entries added in newer revisions marked with asterisks
4. **CCT valuation note (row 4110+):** Explicit rule text embedded in workbook:

```
ZONAL VALUES OF CONDOMINIUM UNIT/TOWNHOUSE:
IF THE TITLE OF A PARTICULAR CONDOMINIUM UNIT/TOWNHOUSE IS -
A.) A CONDOMINIUM CERTIFICATE OF TITLE (CCT), THE ZONAL VALUE OF THE LAND AND THE
    IMPROVEMENTS SHALL BE TREATED AS ONE; OR
B.) A TRANSFER CERTIFICATE OF TITLE (TCT), THE LAND AND IMPROVEMENT SHALL BE GIVEN
    SEPARATE VALUES
THE GROUND FLOOR OF THE RESIDENTIAL CONDOMINIUM SHALL BE CLASSIFIED AS COMMERCIAL AND
TWENTY PERCENT (20%) OF THE ESTABLISHED VALUE SHALL BE ADDED THERETO.
```

This rule is **critical for the engine**: CCT-based transfers use the composite condo ZV directly, but TCT-based transfers require separate land + improvement valuation (the condo ZV does not directly apply).

### Zero-Condo Workbooks
**RDO 4, 5 (Pangasinan), RDO 83 (Talisay/Cebu), RDO 113A (Davao):** Zero RC/CC/PS entries. Entirely land-based classifications (RR, CR, agricultural). The parser must handle workbooks with no condo section at all.

---

## Cross-Cutting Findings

### 1. Classification Code Usage in Condo Entries

| Code | Meaning | Rows (31 WBs) | % of Condo Rows | Present In |
|------|---------|---------------|-----------------|-----------|
| RC | Residential Condo | 3,851 | 39.7% | 30/31 RDOs |
| PS | Parking Slot | 3,378 | 34.8% | 29/31 RDOs |
| CC | Commercial Condo | 2,483 | 25.5% | 30/31 RDOs |
| PH | Penthouse | ~1 | <0.1% | RDO 52 only (explicit code) |
| PC | Parking Commercial | ~4 | <0.1% | RDO 81 only |

**Total condo-classified rows:** 9,712+ across 31 workbooks.
**RC/CC ratio:** 1.55:1 — residential condos outnumber commercial.
**PS absent from:** RDO 4, 5 (Pangasinan — no condos at all).

### 2. Parking Slot Pairing Models

**Model 1: Dual-PS (4-row block)** — Most common in Patterns C, E, F
```
Building Name    RC    value_rc
                 PS    ~70% of RC     ← parking for residential unit
                 CC    value_cc
                 PS    ~70% of CC     ← parking for commercial unit
```

**Model 2: Single-PS (3-row block)** — Pattern B, some Pattern A
```
Building Name    RC    value_rc
                 CC    value_cc
                 PS    ~70% of RC     ← single parking value for entire building
```

**Model 3: RC+PS only (2-row block)** — Some Pattern A (Pasig), provincial
```
Building Name    RC    value_rc
                 PS    ~70% of RC     ← no CC exists
```

**Model 4: CC+PS only (2-row block)** — Commercial-only buildings
```
Building Name    CC    value_cc
                 PS    ~70% of CC     ← no RC exists
```

### 3. Default Calculation Rules (From Workbook Footnotes)

These rules are embedded in workbook footnotes and vary by RDO:

| Rule | Source | Formula |
|------|--------|---------|
| **Parking slot default** | South Makati, general | PS = 60% of the unit value |
| **Parking slot (Taguig)** | RDO 44 footnote | PS = 70% of condominium value |
| **Penthouse default** | South Makati footnote | PH = 110% of CC, or 120% of RC if no CC |
| **Ground floor RC → CC** | South Makati, RDO 57 | Ground floor of residential condo = CC + 20% premium |
| **CC from RC (San Juan)** | RDO 42 footnote | If condo used for business (leasing), CC = 120% of RC |
| **Specific PS values** | Pasay footnote | When footnote says "Valuation for parking spaces were made specific for each type of condominium" — use explicit PS row values |

**Engine implication:** The engine must store per-RDO/per-revision footnote rules and apply them as fallback calculation when explicit values are missing.

### 4. Catch-All Entries

| Pattern | Text | Found In |
|---------|------|----------|
| Standard NCR | "ALL OTHER EXISTING CONDOMINIUMS" | RDO 41 (Mandaluyong), RDO 44 (Taguig) |
| South Makati | "ALL OTHER CONDOMINIUMS" | RDO 50 |
| Cebu per-barangay | "ALL OTHER CONDOMINIUMS" | RDO 81 (25+ barangays) |
| Cebu storey-tiered | "ALL OTHER CONDOMINIUMS (small and medium, 7 storeys and below)" + "ALL OTHER CONDOMINIUMS (8 storeys and above)" | RDO 81 (6+ barangays) |

**Engine implication:** Catch-all entries serve as fallback when a specific building is not listed. The storey-based tiers in Cebu require the engine to accept a building height input (or default to the lower tier) for accurate resolution.

### 5. Building Name Patterns

| Pattern | Example | Implication |
|---------|---------|-------------|
| Tower numbering | "TOWER 1", "TOWER 2", "TOWER I", "TOWER II" | Separate entries per tower |
| Phase naming | "PHASE 1" | Separate entries per phase |
| Parenthetical aliases | "(formerly Cityland Condo VII)" | Alias resolution needed |
| Penthouse suffix | "(Penthouse)" after building name | Separate merged block (South Makati only) |
| Tower+type combined | "BAY GARDEN (18-STOREY)" vs "BAY GARDEN (3-TOWER)" | Multiple building types |
| Under construction | Separate section header, not per-building flag | Section-level indicator (Pasay) |
| Cluster grouping | "BONIFACIO CENTER CLUSTER (BC)" | BGC sub-header |
| Zone numbers | "6764 STI HOLDING CENTER" | Embedded zone numbers (East Makati) |
| Former names | "(formerly X)" or "(now Y)" | Name change tracking |
| Asterisk annotations | "ALDER RESIDENCES**" | Footnote references |
| Slash-combined towers | "ALLEGRA GARDEN PLACE - AMINA / SORAYA" | Shared resources across towers |

### 6. Per-SQM vs Per-Unit Resolution

**ALL zonal values in ALL workbooks are per square meter (ZV/SQ.M).** The header column variants across 31 workbooks:
- "ZV./SQM" / "ZV/SQ.M" / "ZV.SQ.M" / "ZV/SQ M" / "FINAL ZV/SQ.M" / "ZV PER SQMS"

**No per-unit pricing was found.** However, the RDO 57 CCT/TCT note clarifies that:
- CCT (Condominium Certificate of Title): The composite ZV/SQ.M already includes land + improvements — it IS the unit value basis (multiply by floor area)
- TCT (Transfer Certificate of Title): Land and improvements are valued separately — the condo ZV may not directly apply

### 7. CC/RC Ordering Variation

| Region | RC-first blocks | CC-first blocks | Dominant |
|--------|----------------|-----------------|----------|
| NCR (10 workbooks) | ~75% | ~25% | RC-first |
| Cebu (RDO 81) | 44% (68) | 56% (88) | CC-first |

The CC-first ordering in Cebu is significant: it reverses the NCR convention. The parser must not assume RC always precedes CC.

---

## Parser Design Implications

### 1. Condo Section Detection

```
CONDO_SECTION_MARKERS = [
    "CONDOMINIUMS",
    "CONDOMINIUM / TOWNHOUSES",
    "CONDOMINIUMS/TOWNHOUSES (CCT)",
    "LIST OF CONDOMINIUMS",
    "CONDOMINIUMS (CCT) UNDER CONSTRUCTION",
    "CONDOMINIUMS:****",
    "CONDOMINIUMS:********",
]
```

**Algorithm:** Scan C0 for any marker. If found, all subsequent rows until the next barangay header are condo entries. Some workbooks (Pattern B, D) have NO section marker — condos are inline.

### 2. Building Block Assembly

```rust
struct CondoBlock {
    building_name: String,
    vicinity: Option<String>,
    tower: Option<String>,          // Parsed from name suffix
    cluster: Option<String>,        // BGC clusters only
    entries: Vec<CondoEntry>,
    is_under_construction: bool,    // From section header
    is_catch_all: bool,             // "ALL OTHER CONDOMINIUMS"
    storey_tier: Option<StoreyTier>, // Cebu only
}

struct CondoEntry {
    classification: CondoClassification,  // RC, CC, PS, PH, PC
    zv_per_sqm: Option<f64>,             // None for PH placeholder
    footnote_markers: Vec<String>,
}

enum CondoClassification {
    ResidentialCondo,    // RC
    CommercialCondo,     // CC
    ParkingSlot,         // PS
    Penthouse,           // PH
    ParkingCommercial,   // PC (Cebu only)
}

enum StoreyTier {
    Low,    // "7 storeys and below" / "small and medium"
    High,   // "8 storeys and above"
    None,   // No tier distinction
}
```

### 3. Block Assembly Algorithm

```
1. IF merged cells present (Pattern C):
   - Read building name + vicinity from merge anchor (top-left cell)
   - Read classification + ZV from each row within the merge span
   - Group into CondoBlock

2. IF flat layout (Patterns A, B, E, F):
   - Read C0: if non-empty and not a section marker → new building block
   - Read C2: classification code
   - Read C3: zonal value
   - Continue reading rows until next non-empty C0 (new building)

3. SPECIAL CASES:
   - "PARKING SLOT" in C0 (Cebu): treat as PS classification, inherit building from previous block
   - "ALL OTHER CONDOMINIUMS" + storey qualifier in next row: parse tier
   - "(Penthouse)" suffix in building name: set is_penthouse flag
   - PH code with no value: apply penthouse formula (110% CC or 120% RC)
   - Asterisks in C0 for non-first rows (Parañaque): strip, inherit building name
```

### 4. Parking Slot Association

```
1. IF dual-PS (4-row block RC/PS/CC/PS):
   - PS[0] → associated with RC
   - PS[1] → associated with CC

2. IF single-PS (3-row block RC/CC/PS):
   - PS → associated with building (not specific classification)

3. IF PS only (standalone):
   - "PARKING SLOT" in C0 → associate with previous condo block

4. DEFAULT FORMULA (when no explicit PS):
   - RDO 44: PS = 70% of condo ZV
   - General: PS = 60% of unit ZV
   - Formula is RDO-specific — stored in per-RDO metadata
```

### 5. Penthouse Resolution

```
IF explicit PH code with value → use value
IF explicit PH code without value (Parañaque) → calculate:
   PH = 110% of CC (if CC exists)
   PH = 120% of RC (if CC absent)
IF "(Penthouse)" building name variant (South Makati) → separate entry with own ZVs
IF no penthouse data → calculate from formula (if footnote present) or NULL
```

### 6. CCT/TCT Bifurcation

The engine must distinguish between CCT and TCT transactions:
- **CCT:** Use composite condo ZV directly (RC/CC per sqm × floor area)
- **TCT:** Separate land + improvement valuation required — condo ZV does not apply directly
- The title type is a **user input**, not parseable from the zonal value schedule

---

## ZV Range Analysis (Condo Entries)

| Classification | Min ZV/SQM | Max ZV/SQM | Median | Notes |
|---------------|-----------|-----------|--------|-------|
| RC (NCR) | ₱8,500 | ₱550,000 | ~₱115,000 | BGC top, Manila bottom |
| CC (NCR) | ₱10,000 | ₱590,000 | ~₱135,000 | BGC peak |
| PS (NCR) | ₱4,320 | ₱413,000 | ~₱80,000 | 55-70% of parent |
| RC (Cebu) | ₱59,000 | ₱190,500 | ~₱112,500 | Lower than NCR |
| CC (Cebu) | ₱72,500 | ₱243,000 | ~₱125,000 | Closer to RC than NCR |
| RC (Laguna) | ₱27,200 | ₱144,500 | ~₱102,000 | Sparse data |

**BGC premium:** BGC condos command ₱250,000-₱395,000/sqm vs ₱85,000-₱175,000 in rest of Makati — a 2-3× premium.

---

## Emergent Aspects

1. **Storey-based tier resolution** — Cebu's two-tier catch-all (≤7 storeys vs ≥8 storeys) requires building height as an input parameter. This was not anticipated in the prior analysis and affects the engine's input model. → Added to address-matching-algorithms consideration.

2. **CCT/TCT input requirement** — The engine needs to know the title type (CCT vs TCT) to determine whether composite condo ZVs apply or separate land/improvement valuation is needed. → Impacts frontend-api-design.

---

## Sources

- 31 BIR zonal value workbooks (24 NCR + 7 provincial) — raw data in `input/bir-workbook-samples/`
- Condo extraction script: `input/bir-workbook-samples/extract_condo_v2.py`
- Raw extraction output (83K lines): `input/bir-workbook-samples/condo_extraction_results.txt`
- Condo pattern inventory: `input/bir-workbook-samples/condo_pattern_inventory.md`
- RMO 31-2019 Annex B: classification code definitions
- Prior analysis: `analysis/classification-code-usage.md`, `analysis/merged-cell-patterns.md`, `analysis/bir-workbook-provincial-samples.md`
