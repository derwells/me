# Address & Vicinity Pattern Taxonomy

**Wave 2 Analysis** — Systematic extraction and classification of all vicinity descriptors across 31 BIR zonal value workbooks (24 NCR + 7 provincial).

## Extraction Summary

| Metric | Value |
|--------|-------|
| Workbooks parsed | 31 (24 NCR, 7 provincial) |
| Total vicinity records extracted | 28,109 |
| Unique vicinity values | 13,080 |
| Pattern categories identified | 14 (consolidated to 10 semantic types) |
| Noise entries filtered | 171 (legend text, classification descriptions) |

## Two Fundamentally Different Address Models

The most critical finding: NCR and provincial workbooks use **completely different vicinity models**. The parser must detect which model a workbook uses and switch algorithms accordingly.

### NCR Model: Cross-Street Boundary Segments
- **Dominant in**: All 24 NCR RDOs (Revenue Regions 6, 7A, 7B, 8A, 8B)
- **Pattern**: `[Street A] - [Street B]` or `[Street A] TO [Street B]`
- **Meaning**: The property is located on the street column value, between the two cross-streets named in the vicinity column
- **Example**: `SHAW BLVD | EDSA - WACK WACK CREEK | RR | 68,000` = Shaw Blvd frontage between EDSA and Wack Wack Creek, residential, ₱68,000/sqm

### Provincial Model: Road Proximity Hierarchy
- **Dominant in**: All 7 provincial RDOs (Pangasinan, Laguna, Cebu, Davao)
- **Pattern**: Tiered vicinity descriptors indicating distance from roads of different classes
- **Meaning**: Zonal value decreases as property moves from national highway frontage to interior lots
- **Example**: `ALL LOTS | ALONG NATIONAL HIGHWAY | CR | 12,000` = all lots fronting the national highway, commercial, ₱12,000/sqm

### Hybrid Zones
- **RDO 46 (Cainta-Taytay)**: Mix of NCR cross-street and provincial road-proximity within the same workbook — transitional zone
- **RDO 56-57 (Laguna)**: Urban areas (Calamba proper) use NCR cross-street style; rural barangays use provincial road-proximity

## Pattern Category Distribution (Revised)

After noise filtering and reclassification of asterisk-prefixed entries:

| Category | Count | % | Primary Region |
|----------|-------|---|----------------|
| CROSS_STREET_HYPHEN | 11,438 | 40.7% | NCR (85%) |
| SINGLE_LOCATION | 11,911 | 42.4% | Both |
| SUBDIVISION_NAME | 1,001 | 3.6% | Both |
| CROSS_STREET_TO | 835 | 3.0% | NCR (72%) |
| FAR_BASED | 544 | 1.9% | NCR only (RDO 44) |
| INTERIOR_LOT | 509 | 1.8% | Provincial (81%) |
| ALONG_NAMED_ROAD | 321 | 1.1% | Both |
| ALL_OTHER_CATCH | 185 | 0.7% | Both |
| ROAD_PROXIMITY | 163 | 0.6% | Provincial (94%) |
| CONDO_BUILDING | 112 | 0.4% | NCR (29%), Provincial (71%) |
| SITIO | 52 | 0.2% | Provincial (73%) |
| WATERSHED | 37 | 0.1% | Provincial (100%) |
| DISTANCE_INWARD | 26 | 0.1% | Provincial (100%) |

### Regional Breakdown

**NCR (22,569 records):**
- Cross-street (hyphen + TO): 46.0%
- Single location descriptor: 37.5%
- Subdivision/village name: 3.5%
- FAR-based (BGC only): 2.4%
- Along named road: 1.2%

**Provincial (5,540 records):**
- Single location descriptor: 62.4%
- Cross-street (hyphen): 8.3%
- Interior lot: 7.4%
- Cross-street (TO): 4.2%
- Subdivision name: 3.8%
- Road proximity: 2.8%

## Detailed Pattern Taxonomy

### 1. Cross-Street Boundary (NCR Primary Pattern)

The dominant NCR vicinity pattern uses two streets as boundary markers for a segment of the main street.

#### Separator Types
| Separator | Count | Example |
|-----------|-------|---------|
| Spaced hyphen ` - ` | 3,725 | `EDSA - WACK WACK CREEK` |
| Tight hyphen `-` | 2,443 | `BAGBAG-QUIRINO HIGHWAY` |
| Word `TO` | 419 | `CONGRESSIONAL AVE. TO COMMONWEALTH` |
| Word `FROM...TO` | 13 | `FROM FAIRLANE TO OPEL` |
| Slash `/` | 27 | `EDSA/MANDALUYONG BDRY` |

#### Segment Count Distribution
| Segments | Count | Note |
|----------|-------|------|
| 2 segments | 6,454 | Standard A-B cross-street |
| 3 segments | 331 | Multi-intersection or hyphenated street name (ambiguous) |
| 4+ segments | 36 | Complex multi-segment descriptions |

**Critical parser issue**: 3+ segment vicinities create **separator ambiguity** — is `ALABANG - ZAPOTE ROAD - DON JESUS BLVD` three boundaries or is "ZAPOTE ROAD" one name with a hyphen? The parser must use a street name dictionary to disambiguate.

#### Street Type Abbreviations in Cross-Streets
| Abbreviation | Count | Full Form |
|-------------|-------|-----------|
| ST / ST. | 745 | Street |
| AVE / AVE. | 469 | Avenue |
| COR / COR. | 289 | Corner |
| BLVD / BLVD. | 142 | Boulevard |
| RD / RD. | 132 | Road |
| EXT / EXT. | 98 | Extension |
| DR / DR. | 71 | Drive |
| EXTN | 2 | Extension (variant) |

#### Parenthetical Annotations in Cross-Streets
173 cross-street entries contain parenthetical clarifications:

| Type | Count | Example |
|------|-------|---------|
| Former street name | 211 | `(formerly SOUTH SUPERHIGHWAY)` |
| Direction | 4 | `(leftside)`, `(NORTH SIDE)` |
| Type qualifier | 10 | `(EXPORT)`, `(LOCAL)` |
| Barangay qualifier | 4 | `(W/IN BRGY BUCANA)` |

**Parser implication**: Parenthetical content must be preserved for display but stripped for matching. Former-name annotations enable alias resolution (e.g., VITO CRUZ = PABLO OCAMPO SR.).

#### Asterisk-Prefixed Cross-Streets
1,209 unique vicinity values are asterisk-prefixed cross-streets that were initially miscategorized. These are **footnote-marked entries** where `*`, `**`, `***` indicate new, deleted, or modified streets per the region's footnote convention.

Examples:
- `*RIZAL AVE. - END` — newly identified street
- `**E. RODRIGUEZ AVE. - TANAY CEMETERY` — deleted entry
- `*BRGY. BAGUMBAYAN BDRY. - BRGY. QUISAO BDRY` — boundary with asterisk

**Parser must**: Strip leading asterisks before matching, but preserve them as metadata (new/deleted/modified status).

### 2. Road Proximity Hierarchy (Provincial Primary Pattern)

Provincial workbooks use a tiered system based on road class proximity. Extracted 1,080 road-proximity records with ZV values from 5 provincial RDOs.

#### 7-Tier Hierarchy with ZV Ranges

| Tier | Pattern | Records | ZV Range | Median ZV | Primary Classification |
|------|---------|---------|----------|-----------|----------------------|
| T1 | `ALONG NATIONAL HIGHWAY/ROAD` | 74 | ₱300–₱35,000 | ₱12,000 | CR (66%), RR (30%) |
| T2 | `ALONG PROVINCIAL ROAD` | 21 | ₱1,500–₱14,900 | ₱7,000 | RR (48%), CR (38%) |
| T3 | `ALONG MUNICIPAL/CITY ROAD` | 5 | ₱5,000–₱30,000 | ₱6,000 | CR/RR mixed |
| T4 | `ALONG BARANGAY/BRGY ROAD` | 190 | ₱80–₱30,400 | ₱4,000 | CR (48%), RR (36%) |
| T5 | `50 METERS INWARD` / `2ND STRIP` | 33 | ₱900–₱10,200 | ₱2,900 | RR (73%) |
| T6 | `INTERIOR` / `INTERIOR LOT` | 594 | ₱120–₱29,450 | ₱3,500 | RR (80%) |
| T7 | `WATERSHED` / `MOUNTAINOUS` | 34 | ₱100–₱5,800 | ₱500 | A49 (85%), A50 (12%) |

**Additional tier**: TX = `ALONG [named road]` (128 records) — specific named roads like "ALONG THE ROAD", "ALONG RIZAL BLVD" — treated as contextual T1-T4 equivalent depending on road class.

#### Vicinity Text Variations Within Tiers

**T1 National Highway variants:**
- `ALONG NATIONAL HIGHWAY`
- `ALONG NATIONAL ROAD`
- `ALONG NAT'L HIGHWAY`
- `ALONG NATL HIGHWAY`

**T4 Barangay Road variants:**
- `ALONG BARANGAY ROAD`
- `ALONG BRGY ROAD`
- `ALONG BARANGAY ROADS`
- `ALONG BRGY/SUBD ROAD`
- `ALONG BARANGAY OR SUBD ROAD`
- `ALONG BARANGAY OR SUBD  ROAD` (double space)

**T5 Distance Inward variants (Davao-specific):**
- `50 METERS INWARD`
- `50 METERS AWAY FROM PROV'L`
- `2ND STRIP NEXT 50 METERS AWAY`
- `2ND STRIP- NEXT 50 METERS AWAY`
- `2ND  STRIP NEXT 50 METERS AWAY` (double space)
- `2ND STRIP NECT 50 METERS AWAY` (**typo**: NECT for NEXT)
- `INT. AREA 50 METERS AWAY FROM`
- `INT AREAS 50 METERS AWAY FROM NAT'L ROAD`

**T6 Interior variants:**
- `INTERIOR` (bare)
- `INTERIOR LOT`
- `INTERIOR LOTS`
- `INTERIOR LOTS WITHIN THIS BARANGAY`
- `ALL LOTS W/IN THE INTERIOR OF THE BRGY`
- `ALL OTHER STREETS AND INTERIOR LOTS`
- `INTERIOR AREA`
- `INTERIOR RD NEAR DUPAX ST` (NCR: interior with reference)
- `INTERIOR EUSEBIO ST.` (NCR: interior + named street)
- `INTERIOR STREET GOING TO BRGY. PAG-ASA` (NCR: directional)
- `INTERIOR ADDITION HILLS BROOKSIDE` (NCR: subdivision reference)

**T7 Watershed variants:**
- `WATERSHED`
- `WATERSHED AREAS/ OTHER AGRICULTURAL LANDS`
- `MOUNTAINOUS / HILLY AREAS`
- `MOUNTAINOUS/HILLY LANDS`
- `MOUNTAINOUS**` (with footnote)
- `MOUNTAINOUS*` (with footnote)
- `MOUNTAINOUS/ HILLY AREAS`

**Parser design**: Keyword matching with normalization — `NATIONAL` + `HIGHWAY|ROAD` → T1, `PROVINCIAL` + `ROAD` → T2, etc. Must handle abbreviations (BRGY, NAT'L, PROV'L), typos (NECT), and whitespace variation.

### 3. Single Location Descriptor (Both Regions)

The second-largest category (42.4%) contains vicinity values that are **single reference points** rather than boundary pairs. Subcategory analysis of 12,909 unique values:

| Subcategory | Count | Example |
|-------------|-------|---------|
| Street name reference | 1,653 | `EDSA`, `AURORA BLVD`, `#154 N. DOMINGO ST.` |
| Area/place name | 1,248 | `A BONIFACIO`, `MAKATI CINEMA SQUARE` |
| Generic descriptor | 725 | `(50 M INWARD)`, `(ALL OTHER LOTS)` |
| Corner/intersection | 148 | `COR. MAKATI AVE`, `CORNER MINDANAO AVE.` |
| Near landmark | 110 | `NEAR KINGSPOINT SUBD`, `NEAR CREEK` |
| Barangay reference | 84 | `POBLACION DISTRICT A`, `BRGY ROSARIO` |
| Direction-based | 76 | `NORTH SIDE`, `SOUTH ENTRANCE` |
| Numbered prefix | 68 | `100METERS FR JUNC`, `#7829 Makati Ave` |
| Compound | 27 | `ESGUERRA COMPOUND` |
| Beside | 15 | `BESIDE ALABANG HILLS` |
| Purok | 6 | `PUROK 1`, `PUROK 7` |

**Key insight**: Many SINGLE_LOCATION entries are not errors — they're legitimate vicinity descriptors used when:
1. The property is in a subdivision/compound with a single name
2. The street segment doesn't have two bounding cross-streets
3. The vicinity is relative to a landmark
4. The barangay itself is the most specific location (provincial)

### 4. FAR-Based Vicinity (BGC Special Case)

544 records from **RDO 44 (Taguig-Pateros) only**. Bonifacio Global City uses Floor Area Ratio tiers instead of street boundaries.

```
BONIFACIO GLOBAL CITY (BGC) | ALL LOTS WITHIN GLOBAL CITY
  FAR 1  | CR | 205,000
  FAR 2  | CR | 295,000
  FAR 3  | CR | 385,000
  ...
  FAR 18 | CR | 2,160,000
```

- **Range**: FAR 1 through FAR 18
- **Meaning**: Higher FAR = more buildable area = higher land value
- **Classification**: All CR (commercial)
- **Scope**: Applies to BGC, McKinley West, Arca South, FTI Compound

**Parser design**: Detect `FAR \d+` regex in vicinity column → switch to FAR-based pricing mode. This is the only area in all 124 RDOs known to use this model.

### 5. Subdivision/Village Name Vicinity

1,001 records where the vicinity is a named residential development.

**Keyword frequency:**
| Keyword | Count |
|---------|-------|
| SUBD / SUBDIVISION | 277 |
| PARK | 111 |
| VILLAGE | 79 |
| HOMES | 50 |
| HEIGHTS | 22 |
| ESTATE | 20 |
| GARDEN | 9 |
| TOWNHOMES | 6 |

**Pattern**: The vicinity names the subdivision/village/compound where the property is located, rather than cross-streets. Common in both NCR residential areas and provincial developments.

**Example**: `QUEENS PI SUBD | ENTRY NEAR KINGSPOINT SUBD.` = Queens Pi Subdivision near the entry to Kingspoint Subdivision.

### 6. All-Other / Catch-All Patterns

185 records serve as **barangay-level fallback entries** — the value that applies when no more specific match exists.

| Subtype | Count | Example |
|---------|-------|---------|
| ALL LOTS IN [area] | 30 | `ALL LOTS WITHIN GLOBAL CITY` |
| Other ALL | 24 | `ALL STRETCH OF SOUTH SUPER HIGHWAY` |
| ALL OTHER [generic] | 9 | `ALL OTHER TOWN HOUSE` |
| ALL OTHER STREETS/LOTS | 2 | `ALL OTHER STREETS` |
| ALL STREETS IN [area] | 1 | `ALL STREETS` |
| ALL AROUND | 1 | `ALL AROUND` (plaza) |

**Critical for fallback logic**: These entries are the **barangay-level catch-all** — the parser's fallback when no specific street/vicinity match is found within a barangay.

### 7. Corner/Intersection Patterns

499 entries reference intersections rather than segments:

| Format | Count | Example |
|--------|-------|---------|
| Inline `COR` / `COR.` | 184 | `BATAAN - COR. MINDANAO AVE.` |
| Prefix `COR` | 168 | `COR. MAKATI AVE` |
| Full `CORNER` | 89 | `ALONG DON JESUS BLVD CORNER WEST SERVICE RD.` |
| Mixed with cross-street | 58 | `A.H. LACSON-COR.P. FLORENTINO` |

**Parser design**: `COR\.?` and `CORNER` indicate intersection points. These may appear within cross-street entries or as standalone vicinity descriptors. For matching, corner references indicate the property is at or near the named intersection.

### 8. Near/Proximity Reference Patterns

162 entries use proximity to a landmark:

| Format | Count | Example |
|--------|-------|---------|
| `NEAR [landmark]` prefix | 124 | `NEAR KINGSPOINT SUBD` |
| Inline `NEAR` | 25 | `SUMULONG HIGHWAY - INTERIOR NEAR HALANG CREEK` |

**Examples**:
- `NEAR TWIN TOWER I AND PERMALINE HOUSING`
- `NEAR CREEK` (proximity to water feature)
- `**W/IN A RADIUS OF 500 M FR. PUBLIC MARKET` (distance from market)
- `INTERIOR NEAR HALANG CREEK` (compound: interior + near)

### 9. Sitio (Sub-Barangay Addressing)

52 entries use the Filipino `SITIO` designation — a sub-village/hamlet within a barangay.

**Distribution**:
- NCR: 14 entries (RDO 28, 38, 44, 45)
- Provincial: 38 entries (RDO 81 Cebu, RDO 83 Cebu, RDO 113A Davao)

**Examples**:
- `SITIO PUGOT` (NCR, RDO 28)
- `SITIO MAHAYAHAY` (Cebu)
- `SITIO TAL-UT - SITIO ABUNO` (compound: two sitios as boundary)
- `SITIO SIKAP (CALLEJON ST)-SAN ISIDRO ST` (sitio + cross-street)

**Parser design**: `SITIO` entries represent sub-barangay geographic units. They may appear in:
1. The street column (as a location name)
2. The vicinity column (as a proximity descriptor)
3. Combined with cross-streets (sitio boundary pairs)

### 10. Semicolon-Delimited Barangay Qualifiers (Pasig Pattern)

248 unique vicinities contain semicolons, predominantly from **RDO 43 (Pasig City)**. The pattern is:

```
[cross-street or location] ; [barangay name]
```

**Examples**:
- `ADB AVENUE-SAN MIGUEL AVE ; SAN ANTONIO`
- `AMETHYST - PEARL DRIVE ; SAN ANTONIO`
- `A. RODRIGUEZ ; MANGGAHAN`
- `INTERIOR EUSEBIO ST. ; MAYBUNGA`
- `ALONG FLOODWAY ; SANTA LUCIA`

**Meaning**: Pasig embeds the barangay name directly in the vicinity column using `;` as separator. This is unique to Pasig — other RDOs track barangay in header rows.

**Parser design**: When `;` is detected in vicinity, split and extract the trailing barangay name as a barangay qualifier. The part before `;` is the actual vicinity descriptor.

## Cross-Cutting Patterns

### Footnote Markers on Vicinity Values

Vicinity entries frequently carry footnote markers (`*`, `**`, `***`, `****`) whose meaning is **reversed between regions** (documented in merged-cell-patterns analysis):

- **NCR/Cebu**: `*` = deleted/removed, `***` = newly added
- **Pangasinan/Laguna**: `*` = newly identified, `**` = deleted

1,209 unique vicinities have asterisk prefixes. Parser must:
1. Strip asterisks before matching
2. Preserve asterisk count as metadata
3. Resolve meaning using per-region footnote convention

### Former Name Aliases

211 vicinity values contain `(formerly ...)` annotations:
- `1209 PABLO OCAMPO SR. ( formerly VITO CRUZ )`
- `ALEJO AQUINO - PRESIDENT SERGIO OSMEÑA, SR HIGHWAY (formerly SOUTH SUPERHIGHWAY)`
- `(FORMERLY MAGSAYSAY AVE-PUB MKT)`

**Parser design**: Extract former names to build an alias table. When a user searches for "VITO CRUZ", the engine should match entries listed under the current name "PABLO OCAMPO SR."

### Empty/Blank Vicinity (Implicit Catch-All)

Provincial workbooks frequently have entries where the vicinity column is blank — particularly for `ALL LOTS` street entries where the vicinity is implied by position within the road-proximity hierarchy:

```
ALL LOTS | ALONG NATIONAL HIGHWAY | CR | 12,000
         | ALONG PROVINCIAL ROAD  | CR |  8,000   ← blank vicinity inherited from "ALL LOTS"
         | INTERIOR LOT           | RR |  2,500
```

**Parser must**: Carry forward the last non-empty street value to continuation rows (identical to the merged-cell resolution logic).

### Address Number Prefixes

68 entries begin with house/lot numbers: `#154 N. DOMINGO ST.`, `1209 PABLO OCAMPO SR.`, `#7829 Makati Ave`. These are specific property addresses embedded as vicinity descriptors — typically for condominiums or notable buildings with unit-level zonal values.

## Parser Design Recommendations

### 1. Vicinity Type Detection (O(1) per record)

```
fn detect_vicinity_type(text: &str) -> VicinityType {
    let normalized = normalize_whitespace(strip_asterisks(text));

    if normalized.starts_with("FAR ") && is_digit(normalized[4..]) {
        return VicinityType::FarBased;
    }
    if contains_keyword(&normalized, &["WATERSHED", "MOUNTAINOUS"]) {
        return VicinityType::Watershed;
    }
    if starts_with(&normalized, "ALONG") {
        if contains_road_class(&normalized) {
            return VicinityType::RoadProximityTier;
        }
        return VicinityType::AlongNamedRoad;
    }
    if starts_with(&normalized, "INTERIOR") || normalized == "INTERIOR LOT" {
        return VicinityType::Interior;
    }
    if contains(&normalized, "50 METER") || contains(&normalized, "2ND STRIP") {
        return VicinityType::DistanceInward;
    }
    if starts_with(&normalized, "ALL ") {
        return VicinityType::CatchAll;
    }
    if starts_with(&normalized, "SITIO") {
        return VicinityType::Sitio;
    }
    if contains(&normalized, " - ") || contains(&normalized, " TO ") {
        return VicinityType::CrossStreet;
    }
    if contains(&normalized, "NEAR ") {
        return VicinityType::NearLandmark;
    }
    if contains(&normalized, "COR") || contains(&normalized, "CORNER") {
        return VicinityType::Intersection;
    }
    VicinityType::SingleLocation
}
```

### 2. Cross-Street Boundary Parsing

```
fn parse_cross_street(text: &str) -> Option<(String, String)> {
    // Try " TO " first (unambiguous)
    if let Some((a, b)) = split_once(text, " TO ") {
        return Some((normalize_street(a), normalize_street(b)));
    }
    // Try " FROM ... TO "
    if let Some((_, rest)) = split_once(text, "FROM ") {
        if let Some((a, b)) = split_once(rest, " TO ") {
            return Some((normalize_street(a), normalize_street(b)));
        }
    }
    // Try spaced hyphen " - " (prefer over tight hyphen)
    if let Some((a, b)) = split_once(text, " - ") {
        return Some((normalize_street(a), normalize_street(b)));
    }
    // Tight hyphen: must disambiguate against hyphenated names
    // Use street name dictionary for disambiguation
    None
}
```

### 3. Road Proximity Tier Resolution

```
fn resolve_road_tier(text: &str) -> Option<RoadTier> {
    let t = normalize(text);
    match () {
        _ if contains(&t, "NATIONAL") => Some(RoadTier::National),   // T1
        _ if contains(&t, "PROVINCIAL") => Some(RoadTier::Provincial), // T2
        _ if contains(&t, "MUNICIPAL") || contains(&t, "CITY ROAD") => Some(RoadTier::Municipal), // T3
        _ if contains(&t, "BARANGAY") || contains(&t, "BRGY") => Some(RoadTier::Barangay), // T4
        _ if contains(&t, "50 METER") || contains(&t, "2ND STRIP") => Some(RoadTier::FiftyMeters), // T5
        _ if contains(&t, "INTERIOR") => Some(RoadTier::Interior),  // T6
        _ if contains(&t, "WATERSHED") || contains(&t, "MOUNTAINOUS") => Some(RoadTier::Watershed), // T7
        _ => None, // Named road — resolve from context
    }
}
```

### 4. Semicolon Barangay Extraction (Pasig)

```
fn extract_semicolon_barangay(text: &str) -> (String, Option<String>) {
    if let Some(idx) = text.find(';') {
        let vicinity = text[..idx].trim();
        let barangay = text[idx+1..].trim();
        if !barangay.is_empty() {
            return (vicinity.to_string(), Some(barangay.to_string()));
        }
    }
    (text.to_string(), None)
}
```

### 5. Normalization Pipeline

Every vicinity value should pass through this normalization pipeline before matching:

1. **Strip footnote markers**: Remove leading `*`, `**`, `***`, `****`
2. **Extract parentheticals**: Pull out `(formerly ...)` into alias table, `(leftside)` into metadata
3. **Semicolon split**: Extract trailing barangay qualifier if present
4. **Whitespace normalization**: Collapse multiple spaces, trim
5. **Abbreviation expansion**: ST. → STREET, AVE. → AVENUE, BLVD. → BOULEVARD, RD. → ROAD, DR. → DRIVE, COR. → CORNER, BRGY. → BARANGAY, NAT'L → NATIONAL, PROV'L → PROVINCIAL
6. **Case normalization**: Convert to uppercase
7. **Special character handling**: Remove `#` prefixes, normalize hyphens (en-dash, em-dash → ASCII hyphen)

## Implications for Wave 3 (Address Matching)

1. **Dual-mode matching required**: NCR cross-street matching is fundamentally different from provincial road-proximity matching. The engine must detect which mode applies per RDO.

2. **Separator ambiguity in 3+ segment cross-streets**: 331 entries have 3+ hyphen-separated segments. A **street name dictionary** (extracted from the street column across all workbooks) is needed to disambiguate `A - B - C` as `(A) - (B-C)` vs `(A-B) - (C)`.

3. **Former name alias table**: 211+ former-name annotations provide a seed for street alias resolution. This should be expanded with external data (MMDA street renaming records).

4. **Fallback hierarchy**: The catch-all entries (`ALL OTHER STREETS`, `ALL LOTS`, etc.) form the bottom of the matching hierarchy. When no specific match exists, the parser should fall through to these entries.

5. **Pasig special case**: RDO 43 requires semicolon-aware parsing to extract embedded barangay qualifiers.

6. **BGC special case**: RDO 44 requires FAR-tier parsing for Bonifacio Global City entries.

7. **Provincial tier ordering**: The 7-tier road proximity hierarchy has a defined ordering (T1 > T2 > ... > T7) that can be used for fallback: if a property's exact tier isn't found, try the next lower tier.

## Data Quality Issues Discovered

1. **Typos in vicinity values**: `NECT` for `NEXT` (RDO 113A Davao), `CLASSSIFICATION` (triple S, RDO 34), double spaces throughout
2. **Inconsistent abbreviation**: Same RDO uses both `BRGY` and `BARANGAY` in different rows
3. **Inconsistent formatting within single workbook**: RDO-5 Pangasinan uses 4 different colon patterns for municipality headers across different municipalities
4. **Blank vicinity with implicit meaning**: Provincial continuation rows inherit vicinity from the "ALL LOTS" header above
5. **Mixed models in hybrid zones**: RDO 46 intermixes NCR and provincial patterns in the same sheet

## Emergent Aspects for Later Waves

None discovered — the findings here deepen existing Wave 2-3 aspects rather than creating new ones. The address-matching-algorithms aspect (Wave 3) should reference this taxonomy extensively for its dual-mode matching design.
