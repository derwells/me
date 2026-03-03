# Classification Code Usage — Data Format Analysis

**Wave:** 2 — Data Format Analysis
**Date:** 2026-03-03
**Aspect:** `classification-code-usage`

---

## Summary

All 31 sampled BIR zonal value workbooks (24 NCR + 7 provincial) were parsed to extract every classification code value from current-revision sheets. **76,577 classified data rows** were analyzed, yielding **62 unique classification codes**: 13 primary codes (all 13 defined in Annex B), 43 of 50 agricultural sub-codes, and 6 non-standard codes. The data reveals a **stark NCR/Provincial divide**: NCR workbooks use 5-10 codes (almost exclusively primary), while provincial workbooks use 24-43 codes (heavily agricultural). The top 3 codes (RR, CR, RC) account for 67.7% of all rows.

**Key findings for the engine spec:**
1. All 13 primary classification codes from RMO 31-2019 Annex B are present in the dataset — none can be omitted
2. 43 of 50 agricultural sub-codes (A1-A50) appear in actual data — the 7 missing ones (A29 Grape Vineyard, A30, A32, A33 Coal, A34 African Oil, A37 Horticultural, A46 Zarate) may exist in un-sampled RDOs
3. NCR is essentially a 7-code system: {RR, CR, RC, CC, PS, X, I} = 98.5% of NCR rows
4. Provincial is a 59-code system dominated by agricultural sub-codes (42.3% of provincial rows)
5. **6 non-standard codes** found: WC, AR, PC, PH, R, A0 — regional/RDO-specific codes not in Annex B
6. Footnote markers (asterisks) are heavily embedded in classification values — 2,739+ rows have `CODE*`, `*CODE`, or `CODE***` variants requiring normalization
7. Classification legends are embedded in the workbook preamble (rows ~79-120) and vary per revision — the parser must read these to interpret legacy codes correctly

---

## Code Inventory: Complete Classification Code Census

### Primary Codes (13/13 found — 100% coverage)

| Code | Classification | Total Rows | % of All | # RDOs | NCR Rows | Prov Rows | ZV Range (₱/sqm) |
|------|---------------|-----------|----------|--------|----------|-----------|-------------------|
| RR | Residential Regular | 29,235 | 38.2% | 30 | 20,885 | 8,350 | 300 – 350,000 |
| CR | Commercial Regular | 18,735 | 24.5% | 31 | 13,985 | 4,750 | 700 – 2,160,000 |
| RC | Residential Condo | 3,851 | 5.0% | 30 | 3,673 | 178 | 8,500 – 550,000 |
| PS | Parking Slot | 3,378 | 4.4% | 29 | 3,199 | 179 | 4,320 – 413,000 |
| CC | Commercial Condo | 2,483 | 3.2% | 30 | 2,347 | 136 | 10,000 – 590,000 |
| X | Institutional | 2,394 | 3.1% | 29 | 1,525 | 869 | 600 – 2,160,000 |
| GP | General Purposes | 1,540 | 2.0% | 10 | 205 | 1,335 | 200 – 17,000 |
| I | Industrial | 1,376 | 1.8% | 22 | 662 | 714 | 600 – 415,000 |
| A | Agricultural (generic) | 170 | 0.2% | 2 | 63 | 107 | 150 – 1,000 |
| GL | Government Land | 153 | 0.2% | 8 | 104 | 49 | 32,000 – 286,000 |
| APD | Area Priority Dev. | 82 | 0.1% | 6 | 78 | 4 | 600 – 27,900 |
| CL | Cemetery Lot | 11 | 0.0% | 4 | 3 | 8 | 30,000 – 115,000 |
| DA | Drying Area | 3 | 0.0% | 1 | 3 | 0 | 21,000 – 60,000 |

**Observations:**
- **CR is the only code present in all 31 RDOs** — RR is missing from RDO 30 (Binondo, purely commercial)
- **PS appears in 29 RDOs** — absent only from RDO 4 and 5 (Pangasinan, no condos)
- **DA (Drying Area) is extremely rare**: only 3 rows in 1 RDO (Las Piñas, RDO 53A)
- **GL is NCR-dominant**: 8 RDOs, mostly Manila (NCR has Malacañang, government offices)
- **GP is provincial-dominant**: 87% of GP rows are provincial (raw undeveloped land)
- **X (Institutional) has the same max ZV as CR** (₱2,160,000/sqm) — Makati schools/hospitals in premium locations

### Agricultural Sub-Codes (43/50 found — 86% coverage)

| Code | Classification | Total Rows | # RDOs | ZV Range (₱/sqm) | Primary Regions |
|------|---------------|-----------|--------|-------------------|-----------------|
| A50 | Other Agricultural | 3,062 | 9 | 40 – 9,250 | All provincial + Taguig, Cainta |
| A1 | Riceland Irrigated | 2,244 | 6 | 80 – 8,300 | Pangasinan, Laguna, Davao, Cebu |
| A2 | Riceland Unirrigated | 2,175 | 6 | 70 – 6,000 | Pangasinan, Laguna, Davao, Cebu |
| A23 | Corn Land | 1,082 | 3 | 80 – 1,120 | Pangasinan, Davao |
| A4 | Coco Land | 590 | 5 | 80 – 3,200 | Pangasinan, Laguna, Cebu, Davao |
| A16 | Mango Land | 537 | 4 | 70 – 3,200 | Pangasinan, Cebu, Davao |
| A6 | Fishpond | 507 | 5 | 80 – 4,500 | Pangasinan, Laguna, Cebu, Davao |
| A26 | Bamboo Land | 321 | 3 | 80 – 1,120 | Pangasinan, Davao |
| A15 | Pasture Land | 276 | 5 | 200 – 2,750 | All major provincial |
| A14 | Banana | 260 | 4 | 80 – 1,140 | Pangasinan, Laguna, Davao |
| A12 | Orchard | 247 | 5 | 70 – 2,700 | All major provincial |
| A3 | Upland | 175 | 2 | — | Pangasinan only |
| A10 | Fruit Land | 158 | 4 | 280 – 5,800 | Pangasinan, Cebu, Davao |
| A49 | Nipa | 135 | 4 | 75 – 5,800 | Pangasinan, Laguna, Cebu |
| A40 | Idle Land | 129 | 5 | 1,000 – 12,300 | All major provincial |
| A39 | Fish Cage/Pen | 113 | 4 | 400 – 10,000 | Pangasinan, Cebu, Davao, Cainta |
| A36 | Root Crop | 103 | 3 | 75 – 1,800 | Pangasinan, Cebu, Davao |
| A47 | Vegetable Land | 103 | 2 | 70 – 1,070 | Pangasinan, Davao |
| A20 | Citrus | 93 | 2 | 80 – 1,100 | Laguna, Davao |
| A48 | Coffee | 79 | 2 | 80 – 1,120 | Laguna, Davao |
| A19 | Rubber | 77 | 2 | 80 – 1,120 | Cebu, Davao |
| A11 | Cassava | 76 | 1 | 70 – 1,120 | Davao only |
| A43 | Sorghum | 75 | 1 | 70 – 1,120 | Davao only |
| A35 | Palm Oil | 74 | 1 | 80 – 1,120 | Davao only |
| A44 | Abaca/Manila Hemp | 74 | 1 | 80 – 1,120 | Davao only |
| A21 | Durian | 69 | 1 | 90 – 1,120 | Davao only |
| A17 | Sugar Land | 65 | 5 | 80 – 2,700 | Pangasinan, Laguna, Cebu, Davao |
| A8 | Salt Beds | 48 | 3 | 410 – 420 | Pangasinan, Davao |
| A27 | Peanut Land | 31 | 2 | 70 – 420 | Pangasinan, Davao |
| A22 | Rambutan | 29 | 2 | 80 – 1,000 | Laguna, Davao |
| A5 | Timber Land | 27 | 4 | 280 – 700 | Pangasinan, Laguna, Davao |
| A25 | Camote/Cassava | 25 | 2 | 70 – 610 | Pangasinan, Davao |
| A38 | Flower Garden | 24 | 1 | — | Pangasinan only |
| A18 | Tobacco Land | 18 | 2 | 80 – 200 | Pangasinan, Davao |
| A31 | Quarry | 16 | 2 | 200 – 6,000 | Pangasinan, Cebu |
| A13 | Nursery | 9 | 2 | 120 – 1,100 | Laguna, Davao |
| A42 | Rattan | 7 | 2 | 300 – 4,500 | Cebu, Davao |
| A41 | Forest Land | 6 | 2 | 200 – 410 | Cebu, Davao |
| A7 | Mangrove | 5 | 1 | — | Pangasinan only |
| A24 | Pineapple | 4 | 3 | 1,300 – 2,000 | Pangasinan, Cebu |
| A28 | Onion/Garlic | 3 | 1 | 70 – 100 | Davao only |
| A45 | Kangkong | 3 | 1 | 280 – 410 | Davao only |
| A9 | Cotton | 3 | 1 | — | Pangasinan only |

### Missing Agricultural Sub-Codes (7/50 — not found in 31 sampled workbooks)

| Code | Classification | Likely Absent Because |
|------|---------------|----------------------|
| A29 | Grape Vineyard | Minimal grape cultivation in PH |
| A30 | (Unassigned/Unknown) | May not be defined |
| A32 | (Unassigned/Unknown) | May not be defined |
| A33 | Coal Deposit | Very rare; mining areas |
| A34 | African Oil Palm | Covered by A35 (Palm Oil) in practice |
| A37 | Horticultural Land | May appear in Benguet/Cordillera RDOs (not sampled) |
| A46 | Zarate | Unknown classification; may be obsolete |

**Note:** These 7 codes may exist in the 93 un-sampled RDOs (particularly A37 in Cordillera, A33 in Mindanao mining areas). The engine must support all 50 codes regardless of current sample presence.

### Non-Standard Codes (6 codes — not in Annex B)

| Code | Rows | RDO | Context | Likely Meaning | Parser Handling |
|------|------|-----|---------|----------------|-----------------|
| WC | 2 | 29 (Tondo) | ZV ₱35,000 each, no street name | Warehouse/Commercial? | Map to closest standard (CR or I) |
| AR | 2 | 81 (Cebu North) | Row label "AGRICULTURAL AREAS" with `**` | Agricultural Residential | Map to A (generic agricultural) |
| PC | 2 | 81 (Cebu North) | ZV ₱29,500 and ₱78,000, condo context | Parking Commercial | Map to PS |
| PH | 1 | 52 (Parañaque) | Between RC and PS rows for condo | Penthouse | Map to RC with metadata flag |
| R | 1 | 4 (Pangasinan) | Between I and CR rows, ZV ₱11,300 | Truncated "RR" (data entry error) | Map to RR |
| A0 | 1 | 4 (Pangasinan) | Between A23 and A50, ZV ₱55 | Typo for A50 or legacy code | Map to A50 or flag for manual review |

**Engine implication:** The parser must have a `non_standard_code_map` lookup that maps these regional codes to their standard Annex B equivalents. New non-standard codes discovered during bulk ingestion should be flagged for manual review rather than silently dropped.

---

## NCR vs Provincial Distribution — The Two-Code-System Problem

### NCR Classification Profile (24 RDOs, 47,003 rows)

The NCR is essentially a **7-code system** with rare exceptions:

| Rank | Code | Rows | Cumulative % |
|------|------|------|-------------|
| 1 | RR | 20,885 (44.4%) | 44.4% |
| 2 | CR | 13,985 (29.8%) | 74.2% |
| 3 | RC | 3,673 (7.8%) | 82.0% |
| 4 | PS | 3,199 (6.8%) | 88.8% |
| 5 | CC | 2,347 (5.0%) | 93.8% |
| 6 | X | 1,525 (3.2%) | 97.1% |
| 7 | I | 662 (1.4%) | 98.5% |
| 8+ | 12 others | 727 (1.5%) | 100.0% |

- **Zero agricultural sub-codes** in pure NCR RDOs (RDO 28-53B), except:
  - RDO 44 (Taguig): A50 appears in Pateros barangays (still semi-rural)
  - RDO 45 (Marikina): Generic "A" used (no sub-code)
  - RDO 46 (Cainta-Taytay): A1, A2, A39, A50 — eastern NCR fringe is agricultural
- **GL exists only in Manila RDOs** (28, 31, 33, 34, 38, 39, 40) — government land in the national capital
- **APD exists in 6 RDOs** — priority development zones in Manila and Makati
- The condo codes (RC, CC, PS) collectively = 19.6% of NCR rows — every 5th row is a condo entry

### Provincial Classification Profile (7 RDOs, 29,574 rows)

Provincial is a **59-code system** dominated by agricultural land:

| Category | Codes | Rows | % of Provincial |
|----------|-------|------|-----------------|
| Primary (RR, CR, I, X, GP) | 5 | 16,018 | 54.2% |
| Condo (RC, CC, PS) | 3 | 493 | 1.7% |
| Agricultural (A + A1-A50) | 48 | 12,517 | 42.3% |
| Special (GL, APD, CL, DA) | 4 | 61 | 0.2% |
| Non-standard | 5 | 6 | 0.0% |

- **Agricultural codes are 42.3% of provincial data** — nearly half of all rows
- **Top 5 agricultural codes** (A50, A1, A2, A23, A4) = 33.3% of provincial rows
- **A50 (Other Agricultural)** is a catch-all used when specific crop type isn't classified — it's the 3rd most common code in provincial data
- **RDO 113A (Davao)** uses 36 of the 43 observed agricultural codes — Davao is the most code-diverse RDO
- **Condo codes are rare**: only 1.7% of provincial rows (vs. 19.6% in NCR)

### Per-RDO Code Count Distribution

| Code Count | RDOs | Regions |
|-----------|------|---------|
| 5-7 | 14 | Core NCR (Makati, Manila, QC) |
| 8-10 | 8 | Outer NCR (Novaliches, Paco, Marikina) |
| 11 | 1 | Cainta-Taytay (NCR fringe) |
| 24 | 1 | Calamba, Laguna |
| 29 | 2 | Talisay Cebu, Alaminos Pangasinan |
| 36 | 1 | Calasiao, Pangasinan |
| 43 | 1 | West Davao City |

**Engine implication:** The classification dropdown/filter in the UI must adapt to the selected RDO. Showing all 63 codes for a Makati lookup is noise; showing only 7 for a Davao lookup is data loss. The engine should pre-compute `available_codes_per_rdo` during ingestion.

---

## Code Formatting Variations

### Footnote Markers in Classification Column

Asterisks are pervasively used as footnote markers in the classification column. **2,739+ rows** across 19 RDOs have asterisk-embedded classification values:

| Pattern | Example | Meaning | Count | RDOs |
|---------|---------|---------|-------|------|
| `CODE*` | `CR*` | Single footnote (newly identified) | 1,200+ | 57, 81, 53B, 41, 42, 45, 83 |
| `*CODE` | `*RR` | Prefix footnote (same meaning) | 700+ | 56, 53A, 48 |
| `CODE**` | `RR**` | Double footnote (different meaning per RDO) | 400+ | 57, 81, 53B, 56 |
| `CODE***` | `CR***` | Triple footnote | 200+ | 81, 40, 53B, 56 |
| `CODE****` | `RR****` | Quad footnote | 50+ | 53B, 81 |
| `CODE*****` | `CR*****`, `RC*****` | Five+ asterisks | 30+ | 48, 81 |
| `*****CODE` | `*****CR` | Five prefix asterisks | 7 | 48 |
| `CODE ` with text | `** APD under Resolution...` | Full footnote text in classification cell | 30+ | 34, 42, 52 |

**Critical finding:** The footnote marker position (prefix vs suffix) varies by region:
- **Laguna (RDO 56, 57):** Predominantly prefix (`*RR`, `**CR`)
- **NCR (RDO 40, 41, 53B):** Predominantly suffix (`CR*`, `RR***`)
- **Cebu (RDO 81, 83):** Predominantly suffix (`PS*`, `RC****`)

This is consistent with the footnote-convention-mapping Wave 2 aspect — the reversed convention makes it impossible to use a single regex pattern without context.

### Parsing Strategy for Footnote-Embedded Codes

```
fn extract_classification(raw: &str) -> (ClassCode, Option<FootnoteMarker>) {
    let trimmed = raw.trim();

    // Step 1: Check if entire cell is a footnote explanation (long text)
    if trimmed.len() > 15 { return (None, Some(FullText(trimmed))); }

    // Step 2: Strip leading asterisks
    let (prefix_stars, rest) = strip_prefix_asterisks(trimmed);

    // Step 3: Strip trailing asterisks
    let (code_part, suffix_stars) = strip_suffix_asterisks(rest);

    // Step 4: Normalize the code
    let code = normalize_code(code_part);

    // Step 5: Combine footnote markers
    let footnote = max(prefix_stars, suffix_stars); // count of asterisks

    (Some(code), if footnote > 0 { Some(Stars(footnote)) } else { None })
}
```

### Space-Embedded Codes

Some codes have internal spaces that must be normalized:

| Raw Value | RDO | Normalized |
|-----------|-----|-----------|
| `A *` | 83 (Cebu) | `A` |
| `A 50 23*` | 83 (Cebu) | `A50` (with revision annotation) |
| `RR    23*` | 83 (Cebu) | `RR` (with revision annotation) |
| `A4 **` | 83 (Cebu) | `A4` |
| `CR **` | 57 (Laguna) | `CR` |
| `A 1` | Various | `A1` |

**Cebu-specific pattern:** RDO 83 (Talisay) embeds revision numbers *within* the classification cell: `A50 23*` means "A50, new in 23rd revision". The parser must strip numeric suffixes after the code before asterisk removal.

### Slash-Delimited Dual Codes

One instance found of dual classification in a single cell:

| Raw Value | RDO | Meaning |
|-----------|-----|---------|
| `A41/A49*` | 83 (Cebu) | Forest Land / Nipa — dual-classified parcel |

The parser should split on `/` and treat as two separate classification entries for the same row.

---

## Classification Legend Structures

### Embedded Legends in Workbook Preamble

Every workbook includes a classification legend in the preamble section (rows ~60-120, before the first data row). The legend structure varies:

**Pattern 1: Two-column code-description pairs (Pangasinan, RDO 4)**
```
Row 79: "CLASSIFICATION LEGEND:"
Row 81: "CODE              CLASSIFICATION" | "CODE                  CLASSIFICATION"
Row 82: "RR                     Residential Regular" | "GL                         Government Land"
Row 83: "CR                     Commercial Regular" | "GP                          General Purposes"
...
Row 90: "AGRICULTURAL LANDS"
Row 92: "A1    Riceland Irrigated" | "A26  Bamboo Land"
Row 93: "A2    Riceland Unirrigated" | "A27  Peanut Land"
```

**Pattern 2: Inline text definitions (NCR, various)**
```
Row 58: "RESIDENTIAL" | "LAND/CONDOMINIUM PRINCIPALLY DEVOTED TO HABITATION."
Row 60: "COMMERCIAL" | "LAND DEVOTED PRINCIPALLY TO COMMERCIAL..."
Row 63: "INDUSTRIAL" | "DEVOTED PRINCIPALLY TO INDUSTRY..."
```

**Pattern 3: No explicit legend (some NCR RDOs)**
Smaller NCR workbooks sometimes omit the full legend, relying on the implicit Annex B standard.

**Engine implication:** The parser should extract the classification legend from the preamble when available. This is critical for:
1. **Legacy code mapping** — pre-2019 revisions where A1="Unirrigated Riceland" instead of standard "Riceland Irrigated"
2. **Non-standard code resolution** — mapping WC, AR, PC, PH to standard codes
3. **Validation** — cross-checking extracted codes against the workbook's declared legend

---

## Barangay-Level Code Combination Patterns

### Most Common Barangay Classification Profiles

| # Barangays | Code Combination | Profile |
|-------------|-----------------|---------|
| 15 | CR, RR, X | Basic NCR residential (no condo) |
| 7 | CC, CR, PS, RC, RR, X | Standard NCR with condos |
| 5 | CR, RR | Minimal (just residential + commercial) |
| 5 | CC, CR, I, PS, RC, RR, X | Full NCR with industrial |
| 2 | APD, CC, CR, GL, GP, I, PS, RC, RR, X | Maximum NCR (10 codes, Manila government areas) |

**Observations:**
- The most common pattern is just `{CR, RR, X}` — confirming that most NCR barangays have only residential, commercial, and institutional land
- Only 12 of 55+ barangay profiles include agricultural codes
- Pangasinan RDOs have single-barangay profiles with 29-36 codes because the barangay-level extraction groups all municipalities together (a limitation of the multi-municipality workbook format)

### Minimum Code Set per Barangay

Every barangay with data has at least **CR** (commercial). The minimum observed set is `{CR, RR}` (5 barangays). This makes CR the universal anchor code for the fallback system — if a barangay has any zonal value at all, it has a CR value.

---

## ZV Value Analysis by Classification Code

### ZV Range Overlap and Ordering

| ZV Range Category | Codes | Typical ZV/sqm |
|-------------------|-------|----------------|
| Ultra-high (>₱500K) | CR, CC, RC, PS, X | ₱500K – ₱2,160,000 (Makati CBD) |
| High (₱100K-500K) | CR, CC, RC, PS, RR, X, I | ₱100K – ₱500K (NCR general) |
| Medium (₱10K-100K) | All primary codes | ₱10K – ₱100K (outer NCR, urban provincial) |
| Low (₱1K-10K) | GP, A-codes, RR | ₱1K – ₱10K (rural provincial) |
| Ultra-low (<₱1K) | A-codes | ₱40 – ₱1,000 (agricultural) |

**Key insight:** The ZV ranges for different classification codes **overlap significantly**. A CR lot in rural Pangasinan (₱700/sqm) is valued lower than an RR lot in Makati (₱350,000/sqm). This means classification code alone does not determine value bracket — it must be combined with location.

### CR > RR Rule

In every barangay where both CR and RR exist, **CR ≥ RR**. The typical ratio:

| Region | CR:RR Ratio |
|--------|-------------|
| Makati CBD | 1.0x – 1.25x |
| Manila | 1.0x – 1.5x |
| QC | 1.1x – 1.3x |
| Outer NCR | 1.1x – 1.5x |
| Provincial urban | 1.2x – 2.0x |
| Provincial rural | 1.0x – 1.3x |

This is consistent with the San Juan (RDO 42) footnote: *"If condominium/townhouse is used in business (leasing), considered as Commercial; Commercial is 120% of the residential value."*

### PS Pricing Rule

The PS (Parking Slot) value typically follows a formulaic relationship to the RC/CC value:

| RDO | Stated Rule | Observed Range |
|-----|-------------|----------------|
| RDO 44 (Taguig) | "PS = 70% of Condominium Value" (footnote in workbook) | 60-75% of RC |
| RDO 47-50 (Makati) | Not stated but consistent | 55-70% of RC |
| General | No published rule | 40-80% of RC |

**Engine implication:** The PS pricing formula is not universal but can serve as a reasonableness check during validation.

---

## RDO-Specific Anomalies

### RDO 30 (Binondo) — No RR Code

RDO 30 is the only sampled RDO with **no RR (Residential Regular) code**. Binondo is a purely commercial district — the entire area is classified as either CR, CC, RC, PS, or X. This is architecturally significant: the fallback chain cannot assume every barangay has an RR value.

### RDO 81 (Cebu North) — Non-Standard AR and PC

RDO 81 uses two codes not in Annex B:
- **AR** (Agricultural Residential): Appears next to "AGRICULTURAL AREAS" label with `**` footnote. Likely a regional Cebu convention for mixed-use agricultural/residential land.
- **PC** (Parking Commercial): Two entries with ZVs of ₱29,500 and ₱78,000 — in the condo section, suggesting commercial parking as distinct from residential parking (PS).

### RDO 44 (Taguig) — BGC FAR-Based Classification

Taguig's BGC area uses FAR (Floor Area Ratio) tiers instead of street-based vicinity. Classification codes in BGC are standard (RR, CR, RC, CC, PS, I, X), but the **value is determined by FAR tier, not by street**. This creates an additional axis for the lookup engine: in BGC, the key is (barangay, FAR_tier, classification) rather than (barangay, street, classification).

### RDO 46 (Cainta-Taytay) — NCR/Provincial Hybrid

RDO 46 uses 11 codes including agricultural sub-codes (A1, A2, A39, A50), making it a hybrid between the NCR 7-code and provincial 40+ code systems. This is consistent with its geography — it's the eastern boundary of NCR where urban meets agricultural land.

### RDO 42 (San Juan) — CC 120% Rule

San Juan's workbook explicitly states in footnotes: *"If condominium/townhouse is used in business (leasing), considered as Commercial; Commercial is 120% of the residential value."* This is an RDO-specific pricing rule that may apply more broadly but is only documented here.

---

## Implications for Engine Architecture

### Classification Code Enum Design (Rust)

```rust
/// All classification codes from Annex B + observed non-standard codes
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum ClassCode {
    // Primary codes (13)
    RR, CR, RC, CC, I, X, GL, GP, CL, APD, PS, DA, A,
    // Agricultural sub-codes (50, even if not all observed)
    A1, A2, A3, A4, A5, A6, A7, A8, A9, A10,
    A11, A12, A13, A14, A15, A16, A17, A18, A19, A20,
    A21, A22, A23, A24, A25, A26, A27, A28, A29, A30,
    A31, A32, A33, A34, A35, A36, A37, A38, A39, A40,
    A41, A42, A43, A44, A45, A46, A47, A48, A49, A50,
    // Non-standard (mapped from regional variants)
    NonStandard(String),
}
```

Total enum variants: 63 standard + `NonStandard` catch-all = 64 variants. All 50 agricultural codes should be in the enum even if not observed in our sample.

### Classification Normalization Pipeline

```
raw_cell_value
  → strip_whitespace()
  → strip_asterisks() → (code, footnote_count)
  → strip_revision_numbers()  // "A50 23*" → "A50"
  → split_slashes()           // "A41/A49*" → ["A41", "A49"]
  → collapse_spaces()         // "A 1" → "A1"
  → uppercase()
  → lookup_standard_map()     // "R" → "RR", "WC" → "CR", etc.
  → validate_against_enum()
  → (ClassCode, Option<FootnoteMarker>)
```

### Available Codes Index

Pre-compute during ingestion:

```rust
pub struct AvailableCodesIndex {
    /// Which codes appear in each RDO (for UI filtering)
    codes_per_rdo: HashMap<RdoId, HashSet<ClassCode>>,
    /// Which codes appear in each barangay (for fine-grained filtering)
    codes_per_barangay: HashMap<(RdoId, BarangayId), HashSet<ClassCode>>,
    /// Global frequency distribution (for default sort ordering)
    global_frequency: HashMap<ClassCode, u32>,
}
```

### Validation Rules

1. **Code must be in enum** — reject unrecognized codes with error log
2. **Code must exist in RDO context** — warn if code is absent from the RDO's historical data
3. **ZV reasonableness** — flag if ZV for a code is outside 2 standard deviations of its regional range
4. **CR ≥ RR invariant** — flag barangays where RR > CR (data quality issue)
5. **PS ≤ RC invariant** — flag where PS > RC (parking shouldn't exceed condo value)

---

## Sources

- 31 BIR zonal value workbooks (24 NCR + 7 provincial) parsed from `input/bir-workbook-samples/extracted/` and `input/bir-workbook-samples/extracted-provincial/`
- Raw extraction data saved to `raw/classification-code-extraction.json` (76,577 rows analyzed)
- RMO 31-2019 Annex B: `analysis/rmo-31-2019-annexes.md`
- Prior analysis: `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md`
- RDO 42 (San Juan) footnotes: workbook cell annotations documenting CC 120% rule
- RDO 44 (Taguig) footnotes: PS 70% rule and FAR-based classification
- RDO 4 (Pangasinan) classification legend: embedded in workbook preamble rows 79-120
