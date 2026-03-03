# Address Matching Algorithms — Resolution Logic Deep-Dive

**Wave:** 3 — Resolution Logic Deep-Dive
**Date:** 2026-03-03
**Aspect:** `address-matching-algorithms`
**Depends on:** Wave 2 (address-vicinity-patterns, workbook-column-layouts, merged-cell-patterns, footnote-convention-mapping, classification-code-usage, condo-table-structures), Wave 3 (rdo-jurisdiction-mapping)
**Verification:** Cross-checked against 15+ independent sources (see `address-matching-verification.md`) — BIR RMC 115-2020, RMO 31-2019 preamble, Respicio & Co., CTA rulings, CMU string metrics paper, Filipino NLP research, libpostal, Google Geocoding API docs, OSM Philippines wiki

---

## 1. Problem Statement

Address matching is the **hardest step** (Complexity EXTREME) in the 5-step zonal value resolution pipeline. The engine must resolve a free-text property address into a specific row in one of 124 heterogeneous BIR Excel workbooks, where:

- **28,109** vicinity records exist across 31 sampled workbooks (estimated **~690K** across all 124 RDOs)
- **Two fundamentally different address models** coexist: NCR cross-street boundaries and provincial road-proximity tiers
- **13,080 unique** vicinity values with extensive variation in formatting, abbreviations, and typos
- **No geocoding standard** — BIR uses text-based matching, not GIS coordinates
- **Merged cells, footnote markers, and former-name aliases** obscure the data
- **ONETT processors** themselves do manual Excel Ctrl+F lookup — there is no BIR algorithmic matching reference

The address matcher must achieve **high recall** (never miss a match that exists) with **acceptable precision** (minimize false positives that return wrong ZV). A wrong match is worse than no match — CTA case law (Emiliano/Gamboa) confirms that returning an arbitrary value when no prescribed value exists is legally impermissible.

---

## 2. Input Model

### User Query

The engine receives these inputs from the user:

```rust
struct PropertyQuery {
    // Required
    city_municipality: String,        // "Makati City", "Taguig City"
    barangay: String,                 // "Bel-Air", "Cembo", "Poblacion"

    // Optional but strongly recommended
    street: Option<String>,           // "Ayala Avenue", "Shaw Blvd"
    vicinity_hint: Option<String>,    // "near EDSA", "along National Highway"

    // Required for classification filtering
    classification: ClassificationCode, // RR, CR, RC, CC, etc.

    // Optional
    subdivision: Option<String>,      // "Forbes Park", "BF Homes"
    condo_building: Option<String>,   // "One Rockwell", "Gramercy Residences"
    transaction_date: Option<Date>,   // for effectivity date resolution
    title_type: Option<TitleType>,    // TCT or CCT (for condo bifurcation)

    // BGC-specific
    floor_area_ratio: Option<u8>,     // FAR 1-18 (RDO 44 BGC only)
}
```

### Workbook Record (Normalized)

After the ingestion pipeline normalizes workbook data (documented in Wave 2 analyses):

```rust
struct ZonalRecord {
    rdo_id: u8,                       // 1-114
    municipality_id: u16,             // PSGC city/municipality code
    barangay_name: String,            // normalized uppercase
    street_name: String,              // normalized, footnote markers stripped
    vicinity: String,                 // normalized, footnote markers stripped
    classification: ClassificationCode,
    zv_per_sqm: u32,                  // PHP per sqm (or per unit for condos)
    revision_do: String,              // "DO 037-2024"
    effectivity_date: Date,
    footnote_flags: u16,              // preserved asterisk metadata
    vicinity_type: VicinityType,      // pre-classified during ingestion
    is_catch_all: bool,               // "ALL OTHER STREETS" etc.
    is_condo: bool,                   // RC/CC/PS classification
}
```

### Key Asymmetry

The user query is **unstructured**: a person typing "Ayala Ave near EDSA, Makati" or "lot along provincial road, Brgy San Isidro, Pangasinan."

The workbook record is **structured but inconsistent**: column layouts vary, abbreviations are unstandardized, and the same semantic concept ("along the national highway") has 4+ text variants.

The matching algorithm bridges this gap through progressive normalization and multi-phase candidate filtering.

---

## 3. Architecture Overview — The Matching Pipeline

```
User Query
    │
    ▼
┌─────────────────────────┐
│ Phase 0: Normalization   │  Normalize both query and index
│   - Uppercase            │  (index normalized at ingestion time;
│   - Strip punctuation    │   query normalized at query time)
│   - Expand abbreviations │
│   - Resolve aliases      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Phase 1: RDO Resolution  │  city_municipality + barangay → RDO
│   - Jurisdiction mapping │  (from rdo-jurisdiction-mapping analysis)
│   - Temporal versioning  │  Narrows to 1 RDO (rarely 2 for splits)
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Phase 2: Barangay Filter │  Filter records to matching barangay
│   - Exact match          │  Reduces ~5,500 records/RDO to ~30-200
│   - Fuzzy match          │
│   - Numbered barangay    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ Phase 3: Condo vs Land Fork         │
│   if condo_building.is_some()       │
│   || classification ∈ {RC,CC,PS}    │──→ Condo Matching Path (§8)
│   else                              │
└──────────┬──────────────────────────┘
           │ (land path)
           ▼
┌─────────────────────────┐
│ Phase 4: Street Match    │  Match query street against candidates
│   - Exact normalized     │  Produce ranked candidate list
│   - Alias resolution     │
│   - Fuzzy (Jaro-Winkler) │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Phase 5: Vicinity Match  │  Dual-mode matching:
│   - NCR: cross-street    │    NCR → boundary segment containment
│   - Provincial: road tier │    Provincial → tier hierarchy
│   - Special: BGC FAR     │    BGC → FAR tier lookup
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Phase 6: Classification  │  Filter to matching classification code
│   Filter                 │  Handle multi-entry streets
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Phase 7: Fallback Chain  │  If no exact match:
│   1. Catch-all entry     │    progressive fallback
│   2. Adjacent barangay   │    until match or NULL
│   3. NULL (no match)     │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Phase 8: Confidence      │  Score the match quality
│   Scoring & Result       │  Return result + confidence
└─────────────────────────┘
```

---

## 4. Phase 0: Address Normalization

Both the query and the index undergo normalization. The index is normalized once at ingestion time; the query is normalized at each lookup.

### 4.1 Normalization Pipeline

```rust
fn normalize_address(raw: &str) -> NormalizedAddress {
    let text = raw.to_uppercase();

    // Step 1: Strip footnote markers (index only — query won't have these)
    let text = strip_leading_asterisks(&text);

    // Step 2: Extract parenthetical annotations
    let (text, former_names) = extract_parentheticals(&text);
    // "(formerly VITO CRUZ)" → saves alias, removes from text
    // "(leftside)" → saves as metadata

    // Step 3: Semicolon split (Pasig RDO 43 pattern)
    let (text, barangay_qualifier) = extract_semicolon_barangay(&text);

    // Step 4: Whitespace normalization
    let text = collapse_whitespace(&text).trim();

    // Step 5: Abbreviation expansion
    let text = expand_abbreviations(&text);

    // Step 6: Special character normalization
    let text = normalize_special_chars(&text);
    // - Remove # prefixes from house numbers
    // - Normalize en-dash/em-dash to ASCII hyphen
    // - Remove periods after abbreviations (already expanded)
    // - Remove trailing commas

    // Step 7: Number normalization
    let text = normalize_numbers(&text);
    // - "1ST" → "1ST" (keep ordinals)
    // - "#154" → "154" (strip hash)

    NormalizedAddress {
        text,
        former_names,
        barangay_qualifier,
    }
}
```

### 4.2 Abbreviation Expansion Table

Built from analysis of 31 workbooks (address-vicinity-patterns §5):

| Abbreviation | Expansion | Frequency in workbooks |
|-------------|-----------|----------------------|
| ST. / ST | STREET | 745 |
| AVE. / AVE | AVENUE | 469 |
| COR. / COR | CORNER | 289 |
| BLVD. / BLVD | BOULEVARD | 142 |
| RD. / RD | ROAD | 132 |
| EXT. / EXT / EXTN | EXTENSION | 100 |
| DR. / DR | DRIVE | 71 |
| BRGY. / BRGY | BARANGAY | 190+ |
| NAT'L / NATL | NATIONAL | 74 |
| PROV'L / PROVL | PROVINCIAL | 21 |
| SR. / SR | SENIOR | 50+ |
| JR. / JR | JUNIOR | 30+ |
| GEN. / GEN | GENERAL | 20+ |
| SUBD. / SUBD | SUBDIVISION | 277 |
| HWY | HIGHWAY | 30+ |
| SQ. / SQ | SQUARE | 10+ |

**Critical rule**: Abbreviation expansion must be **word-boundary aware**. "ESTRA" should NOT match the "ST" → "STREET" rule. Use regex `\bST\.?\b` patterns.

### 4.3 Letter-Spaced Header Normalization

NCR workbooks use "V I C I N I T Y" (letter-spacing) in 61% of cases. This appears in column headers, not data cells. Handled during ingestion, not query normalization.

```rust
fn collapse_letter_spacing(text: &str) -> String {
    // Detect pattern: single char + space + single char + space + ...
    // "V I C I N I T Y" → "VICINITY"
    let chars: Vec<char> = text.chars().collect();
    if chars.len() >= 5 && chars.iter().step_by(2).all(|c| c.is_alphabetic())
        && chars.iter().skip(1).step_by(2).all(|c| *c == ' ') {
        return chars.iter().step_by(2).collect();
    }
    text.to_string()
}
```

---

## 5. Phase 1: RDO Resolution

Covered in detail by the `rdo-jurisdiction-mapping` analysis. Summary of the 3-tier lookup:

1. **Exact barangay match** → resolves to 1 RDO (99%+ of cases)
2. **Street-level disambiguation** → for 4 known intra-barangay splits (QC Commonwealth/Culiat/Tandang Sora, Makati Bel-Air/Salcedo)
3. **City-level fallback** → returns all RDOs for the city + disambiguation prompt

The jurisdiction mapping table (~42K entries, ~400 KB compressed) is small enough for WASM. Temporal versioning handles the RAO 1-2024 EMBO transfer and future boundary changes.

---

## 6. Phase 2: Barangay Resolution

### 6.1 Barangay Matching Strategy

Barangay names in BIR workbooks are **section headers** (merged cells spanning full row width), not data column values. During ingestion, each data row inherits its barangay from the last-seen header above it.

Matching challenges:

| Challenge | Example | Frequency |
|-----------|---------|-----------|
| Exact match | "POBLACION" = "POBLACION" | ~80% |
| Abbreviation | "BGY. 165" vs "BARANGAY 165" | ~5% (Manila) |
| Numbered barangay | "BARANGAY 37" (Manila has ~897 numbered barangays) | ~5% |
| District prefix | "DISTRICT I - POBLACION" (Davao) | ~3% |
| Spelling variation | "STA. CRUZ" vs "SANTA CRUZ" | ~3% |
| Zone-based | "ZONE 68" (Manila Intramuros) | ~2% |
| Compound names | "NEW ZANIGA" vs "ZANIGA" | ~2% |

### 6.2 Barangay Matching Algorithm

```rust
fn match_barangay(
    query_barangay: &str,
    rdo_barangays: &[BarangayIndex],
) -> Vec<(usize, f64)> {  // (barangay_idx, confidence)
    let normalized = normalize_barangay(query_barangay);
    let mut candidates = Vec::new();

    for (idx, brgy) in rdo_barangays.iter().enumerate() {
        // Tier 1: Exact normalized match
        if brgy.normalized_name == normalized {
            candidates.push((idx, 1.0));
            continue;
        }

        // Tier 2: Numbered barangay matching
        // "Brgy 165" matches "BARANGAY 165" matches "BGY. 165"
        if let (Some(q_num), Some(b_num)) = (
            extract_barangay_number(&normalized),
            extract_barangay_number(&brgy.normalized_name),
        ) {
            if q_num == b_num {
                candidates.push((idx, 0.95));
                continue;
            }
        }

        // Tier 3: District-qualified matching
        // "DISTRICT I - POBLACION" matches "POBLACION"
        if let Some(stripped) = strip_district_prefix(&brgy.normalized_name) {
            if stripped == normalized {
                candidates.push((idx, 0.90));
                continue;
            }
        }

        // Tier 4: Zone-based matching (Manila)
        // "ZONE 68" matches "BARANGAY 649" if zone_mapping[649] == 68
        if let Some(zone) = extract_zone_number(&normalized) {
            if brgy.zone_id == Some(zone) {
                candidates.push((idx, 0.85));
                continue;
            }
        }

        // Tier 5: Fuzzy match (Jaro-Winkler)
        let similarity = jaro_winkler(&normalized, &brgy.normalized_name);
        if similarity >= 0.88 {
            candidates.push((idx, similarity * 0.85));
        }
    }

    candidates.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    candidates
}

fn normalize_barangay(name: &str) -> String {
    let mut s = name.to_uppercase();
    // "STA." → "SANTA", "STO." → "SANTO"
    s = s.replace("STA.", "SANTA").replace("STA ", "SANTA ");
    s = s.replace("STO.", "SANTO").replace("STO ", "SANTO ");
    // "BRGY." → "BARANGAY", "BGY." → "BARANGAY"
    s = regex_replace(&s, r"\bBRGY\.?\b", "BARANGAY");
    s = regex_replace(&s, r"\bBGY\.?\b", "BARANGAY");
    // Remove "BARANGAY" prefix for matching (but keep for numbered)
    if !has_number(&s) {
        s = regex_replace(&s, r"^BARANGAY\s+", "");
    }
    collapse_whitespace(&s).trim().to_string()
}
```

### 6.3 Manila Zone-to-Barangay Mapping

Manila uses a unique zone-based addressing system. Barangays are numbered (1-905) and grouped into zones (1-100+). The engine needs a static lookup table:

```rust
// Manila zone mapping (partial — full table from PSA PSGC + Manila ordinances)
// Zone 68 = Barangay 649, 650, 651 (Intramuros)
// Zone 77 = Barangay 712, 713, 714 (Malate north)
static MANILA_ZONE_MAP: &[(u16, u16)] = &[
    // (zone_number, barangay_number)
    (68, 649), (68, 650), (68, 651),  // Intramuros
    (77, 712), (77, 713), (77, 714),  // Malate
    // ... ~900 entries
];
```

---

## 7. Phase 4: Street Matching

After barangay resolution narrows candidates to ~30-200 records, street matching identifies the correct street(s).

### 7.1 Street Matching Strategy

Street matching uses a **tiered cascade** — try the most precise method first, fall through to fuzzier methods:

```
Tier 1: Exact normalized match (confidence 1.0)
    ↓ (no match)
Tier 2: Alias resolution match (confidence 0.95)
    ↓ (no match)
Tier 3: Substring containment match (confidence 0.85)
    ↓ (no match)
Tier 4: Token-set match (confidence 0.75)
    ↓ (no match)
Tier 5: Fuzzy Jaro-Winkler match (confidence 0.65)
    ↓ (no match)
Tier 6: No street match → fall to catch-all
```

### 7.2 Tier 1: Exact Normalized Match

After both query and index are normalized (uppercase, abbreviations expanded, punctuation stripped):

```rust
fn exact_street_match(query: &str, record_street: &str) -> bool {
    normalize_street(query) == normalize_street(record_street)
}

fn normalize_street(name: &str) -> String {
    let mut s = name.to_uppercase();
    s = expand_abbreviations(&s);          // ST. → STREET
    s = strip_leading_asterisks(&s);       // *RIZAL → RIZAL
    s = remove_periods(&s);                // remove all periods
    s = collapse_whitespace(&s);
    s.trim().to_string()
}
```

**Expected hit rate**: ~60-70% of queries where the user provides the correct current street name.

### 7.3 Tier 2: Alias Resolution

The alias table bridges former/current street names and known equivalences. Three seed sources (confirmed by verification subagent):

1. **BIR workbook `(formerly ...)` annotations**: 211+ entries extracted in Wave 2
2. **BIR workbook footnote equivalences**: "BRIDAL BOUQUET is the same as BRIDAL" (RDO 50)
3. **Wikipedia "List of renamed streets in Metro Manila"**: 100+ entries with legal authority (Republic Acts, presidential proclamations)

```rust
struct AliasTable {
    // Bidirectional: both old→new and new→old
    aliases: HashMap<String, Vec<AliasEntry>>,
}

struct AliasEntry {
    canonical_name: String,      // current official name
    alias_name: String,          // former/alternative name
    source: AliasSource,         // BIR_WORKBOOK | WIKIPEDIA | FOOTNOTE
    valid_from: Option<Date>,    // when the rename took effect
    rdo_scope: Option<u8>,       // None = nationwide; Some(rdo) = RDO-specific
}

// Example entries:
// "VITO CRUZ" → "PABLO OCAMPO SENIOR" (RA 6731, nationwide)
// "SOUTH SUPERHIGHWAY" → "PRESIDENT SERGIO OSMENA SENIOR HIGHWAY"
// "BRIDAL BOUQUET" → "BRIDAL" (RDO 50 specific equivalence)
// "BATANES" → "BATANGAS" (RDO 50 footnote correction)
```

**Matching**: When Tier 1 fails, look up the query street in the alias table. If found, re-try Tier 1 with the canonical name.

### 7.4 Tier 3: Substring Containment

Handles cases where the user provides a partial name or the workbook uses a longer form:

```rust
fn substring_match(query: &str, record: &str) -> Option<f64> {
    let q = normalize_street(query);
    let r = normalize_street(record);

    // Query is substring of record
    if r.contains(&q) && q.len() >= 4 {
        return Some(0.85 * (q.len() as f64 / r.len() as f64));
    }
    // Record is substring of query
    if q.contains(&r) && r.len() >= 4 {
        return Some(0.85 * (r.len() as f64 / q.len() as f64));
    }
    None
}
```

**Example**: User queries "AYALA" → matches workbook entry "AYALA AVENUE" (confidence 0.85 × 5/12 = 0.35 — too low alone, but combined with vicinity match becomes usable).

### 7.5 Tier 4: Token-Set Match

For multi-word street names where word order may differ or extra words are present:

```rust
fn token_set_match(query: &str, record: &str) -> f64 {
    let q_tokens: HashSet<&str> = normalize_street(query).split_whitespace().collect();
    let r_tokens: HashSet<&str> = normalize_street(record).split_whitespace().collect();

    let intersection = q_tokens.intersection(&r_tokens).count();
    let union = q_tokens.union(&r_tokens).count();

    if union == 0 { return 0.0; }
    let jaccard = intersection as f64 / union as f64;

    // Bonus: if all query tokens are found in record
    if q_tokens.is_subset(&r_tokens) {
        return 0.75 + (0.15 * jaccard);
    }

    jaccard * 0.75
}
```

**Example**: "GENERAL LUNA STREET" matches "GEN. LUNA ST." after normalization → both become {"GENERAL", "LUNA", "STREET"} → perfect token match.

### 7.6 Tier 5: Fuzzy Match (Jaro-Winkler)

Last resort for typos and minor variations. Per verification (CMU paper, Filipino NLP research), Jaro-Winkler is preferred for short strings like street names due to its prefix-matching bonus.

```rust
fn fuzzy_street_match(query: &str, record: &str) -> f64 {
    let q = normalize_street(query);
    let r = normalize_street(record);

    let jw = jaro_winkler_similarity(&q, &r);

    // Only accept high-confidence fuzzy matches
    if jw >= 0.90 {
        jw * 0.65  // max confidence = 0.65 for fuzzy
    } else {
        0.0
    }
}
```

**Threshold 0.90** chosen because Filipino street names often have similar prefixes (SAN ANTONIO, SAN AGUSTIN, SAN ISIDRO) — lower thresholds produce false positives.

### 7.7 Street Name Dictionary for Separator Disambiguation

The Wave 2 analysis identified **331 cross-street vicinities with 3+ segments**, creating separator ambiguity. Is `ALABANG - ZAPOTE ROAD - DON JESUS BLVD` three boundaries or is "ZAPOTE ROAD" one hyphenated name?

**Solution**: Build a street name dictionary from the street column (Col 0) across all workbooks:

```rust
struct StreetDictionary {
    // All known street names extracted from Col 0 of all workbooks
    names: HashSet<String>,           // ~13,000 unique normalized names
    // For disambiguation: which multi-word names contain hyphens?
    hyphenated_names: HashSet<String>, // "ZAPOTE ROAD", "WACK WACK CREEK"
}

fn disambiguate_cross_street(
    vicinity: &str,
    dict: &StreetDictionary,
) -> Vec<String> {
    let parts: Vec<&str> = vicinity.split(" - ").collect();
    if parts.len() <= 2 {
        return parts.iter().map(|s| s.trim().to_string()).collect();
    }

    // For 3+ parts, try all possible groupings
    // "A - B - C" could be:
    //   ["A", "B - C"]  if "B - C" is a known street name
    //   ["A - B", "C"]  if "A - B" is a known street name
    //   ["A", "B", "C"] if none are compound names (3-way intersection)

    // Greedy: try longest known name first
    for i in 1..parts.len() {
        let left = parts[..i].join(" - ").trim().to_string();
        let right = parts[i..].join(" - ").trim().to_string();

        if dict.hyphenated_names.contains(&normalize_street(&right)) {
            return vec![left, right];
        }
        if dict.hyphenated_names.contains(&normalize_street(&left)) {
            return vec![left, right];
        }
    }

    // Default: treat as 2-part (first vs rest)
    vec![
        parts[0].trim().to_string(),
        parts[1..].join(" - ").trim().to_string(),
    ]
}
```

---

## 8. Phase 5: Vicinity Matching (Dual-Mode)

This is the core algorithmic challenge. The engine must detect which vicinity model applies and use the appropriate matching strategy.

### 8.1 Mode Detection

The vicinity model is determined per RDO, not per record. During ingestion, each RDO is tagged with its primary mode:

```rust
#[derive(Clone, Copy)]
enum VicinityMode {
    NcrCrossStreet,      // 24 NCR RDOs — cross-street boundaries
    ProvincialRoadTier,  // ~93 provincial RDOs — road proximity tiers
    Hybrid,              // RDO 46 (Cainta-Taytay), RDO 56-57 (Laguna urban)
    BgcFar,              // RDO 44 BGC area only — FAR-tier pricing
}

fn detect_vicinity_mode(rdo_id: u8, barangay: &str) -> VicinityMode {
    // BGC special case: RDO 44, specific barangays
    if rdo_id == 44 && is_bgc_barangay(barangay) {
        return VicinityMode::BgcFar;
    }

    // Hybrid zones
    if rdo_id == 46 { return VicinityMode::Hybrid; }
    if rdo_id == 56 || rdo_id == 57 {
        // Urban municipalities use cross-street; rural use road-tier
        if is_urban_municipality(barangay) {
            return VicinityMode::NcrCrossStreet;
        }
        return VicinityMode::ProvincialRoadTier;
    }

    // NCR RDOs (Revenue Regions 5, 6, 7A, 7B, 8A, 8B)
    if is_ncr_rdo(rdo_id) {
        return VicinityMode::NcrCrossStreet;
    }

    VicinityMode::ProvincialRoadTier
}
```

### 8.2 NCR Cross-Street Boundary Matching

**Problem**: Given a user's property address on street X, find the segment of street X defined by cross-streets A-B that contains the property.

**Approach**: The user either provides cross-street references (ideal) or a general location (requires fuzzy resolution).

#### Case A: User Provides Cross-Street Reference

```
User: "Shaw Blvd, between EDSA and Wack Wack Creek"
Workbook: "SHAW BLVD | EDSA - WACK WACK CREEK | RR | 68000"
```

**Algorithm**:
1. Match query street against records (Phase 4)
2. From matched street records, find the record whose cross-street pair contains the query's cross-streets

```rust
fn match_ncr_vicinity_with_crossstreets(
    query_cross_a: &str,
    query_cross_b: &str,
    candidates: &[ZonalRecord],
    dict: &StreetDictionary,
) -> Vec<(usize, f64)> {
    let q_a = normalize_street(query_cross_a);
    let q_b = normalize_street(query_cross_b);

    let mut matches = Vec::new();

    for (idx, record) in candidates.iter().enumerate() {
        if let Some((rec_a, rec_b)) = parse_cross_street_pair(
            &record.vicinity, dict
        ) {
            let a_match = street_similarity(&q_a, &rec_a);
            let b_match = street_similarity(&q_b, &rec_b);

            // Also try reversed order (A-B vs B-A)
            let a_rev = street_similarity(&q_a, &rec_b);
            let b_rev = street_similarity(&q_b, &rec_a);

            let score = f64::max(
                f64::min(a_match, b_match),    // forward
                f64::min(a_rev, b_rev),        // reversed
            );

            if score >= 0.80 {
                matches.push((idx, score));
            }
        }
    }

    matches
}
```

#### Case B: User Provides Only General Location / Landmark

```
User: "Ayala Avenue, near Greenbelt, Makati"
Workbook has 12 segments of Ayala Avenue with different cross-streets
```

**Strategy**: Return all matching street segments with a prompt for disambiguation. The engine cannot determine which segment contains "near Greenbelt" without geocoding.

```rust
struct MatchResult {
    records: Vec<ScoredRecord>,
    disambiguation_needed: bool,
    disambiguation_options: Vec<String>,  // cross-street descriptions
}

fn match_ncr_vicinity_no_crossstreets(
    query_street: &str,
    candidates: &[ZonalRecord],
    classification: ClassificationCode,
) -> MatchResult {
    let street_matches: Vec<_> = candidates.iter()
        .enumerate()
        .filter(|(_, r)| street_matches(query_street, &r.street_name))
        .filter(|(_, r)| r.classification == classification)
        .collect();

    if street_matches.len() == 1 {
        // Single match — no disambiguation needed
        return MatchResult {
            records: vec![scored(street_matches[0], 0.90)],
            disambiguation_needed: false,
            disambiguation_options: vec![],
        };
    }

    if street_matches.len() > 1 {
        // Multiple segments — return all with disambiguation
        return MatchResult {
            records: street_matches.iter().map(|m| scored(*m, 0.70)).collect(),
            disambiguation_needed: true,
            disambiguation_options: street_matches.iter()
                .map(|(_, r)| format!("{} ({})", r.vicinity, r.zv_per_sqm))
                .collect(),
        };
    }

    // No match — fall to catch-all
    MatchResult {
        records: vec![],
        disambiguation_needed: false,
        disambiguation_options: vec![],
    }
}
```

### 8.3 Provincial Road-Proximity Tier Matching

**Problem**: Given a property location relative to a road, determine which road-proximity tier applies.

**Approach**: Parse the user's vicinity hint into a road tier, then match against the barangay's available tiers.

#### 7-Tier Road-Proximity Hierarchy

From Wave 2 address-vicinity-patterns analysis:

```rust
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
enum RoadTier {
    T1National = 1,    // Along national highway/road
    T2Provincial = 2,  // Along provincial road
    T3Municipal = 3,   // Along municipal/city road
    T4Barangay = 4,    // Along barangay/subdivision road
    T5FiftyMeters = 5, // 50 meters inward / 2nd strip
    T6Interior = 6,    // Interior lot
    T7Watershed = 7,   // Watershed / mountainous area
}
```

#### Tier Resolution from User Input

```rust
fn resolve_road_tier(vicinity_hint: &str) -> Option<RoadTier> {
    let t = normalize_address(vicinity_hint).text;

    // Ordered from most specific to least
    if contains_any(&t, &["WATERSHED", "MOUNTAINOUS", "HILLY"]) {
        return Some(RoadTier::T7Watershed);
    }
    if contains_any(&t, &["50 METER", "2ND STRIP", "SECOND STRIP"]) {
        return Some(RoadTier::T5FiftyMeters);
    }
    if contains_any(&t, &["INTERIOR"]) {
        return Some(RoadTier::T6Interior);
    }
    if contains_any(&t, &["NATIONAL HIGHWAY", "NATIONAL ROAD"]) {
        return Some(RoadTier::T1National);
    }
    if contains_any(&t, &["PROVINCIAL ROAD", "PROVINCIAL HIGHWAY"]) {
        return Some(RoadTier::T2Provincial);
    }
    if contains_any(&t, &["MUNICIPAL ROAD", "CITY ROAD"]) {
        return Some(RoadTier::T3Municipal);
    }
    if contains_any(&t, &["BARANGAY ROAD", "SUBDIVISION ROAD"]) {
        return Some(RoadTier::T4Barangay);
    }

    // Named road — cannot determine tier without additional context
    if t.starts_with("ALONG ") {
        return None; // ambiguous — could be any tier
    }

    None
}
```

#### Tier Fallback Logic

When the exact tier doesn't have an entry for the requested classification, fall through to the next available tier:

```rust
fn match_provincial_tier(
    target_tier: RoadTier,
    classification: ClassificationCode,
    barangay_records: &[ZonalRecord],
) -> Option<(usize, f64)> {
    // Tier-ordered search: exact → next lower → next lower → ...
    let tier_order = match target_tier {
        RoadTier::T1National => vec![T1, T2, T3, T4, T5, T6, T7],
        RoadTier::T2Provincial => vec![T2, T3, T4, T5, T6, T7],
        RoadTier::T3Municipal => vec![T3, T4, T5, T6, T7],
        RoadTier::T4Barangay => vec![T4, T5, T6, T7],
        RoadTier::T5FiftyMeters => vec![T5, T6, T7],
        RoadTier::T6Interior => vec![T6, T7],
        RoadTier::T7Watershed => vec![T7],
    };

    for (priority, tier) in tier_order.iter().enumerate() {
        for (idx, record) in barangay_records.iter().enumerate() {
            if record.vicinity_type == VicinityType::RoadProximityTier
                && resolve_record_tier(&record.vicinity) == Some(*tier)
                && record.classification == classification
            {
                let confidence = if priority == 0 { 0.95 } else {
                    0.80 - (priority as f64 * 0.10) // decreasing confidence
                };
                return Some((idx, confidence));
            }
        }
    }

    None
}
```

### 8.4 BGC FAR-Based Matching (RDO 44 Special Case)

544 records from RDO 44 use Floor Area Ratio tiers (FAR 1 through FAR 18). This requires a specific input from the user.

```rust
fn match_bgc_far(
    far_tier: u8,  // 1-18
    classification: ClassificationCode,
    bgc_records: &[ZonalRecord],
) -> Option<(usize, f64)> {
    let target = format!("FAR {}", far_tier);

    for (idx, record) in bgc_records.iter().enumerate() {
        if record.vicinity.contains(&target)
            && record.classification == classification {
            return Some((idx, 1.0));  // FAR is deterministic
        }
    }

    // Fallback: closest available FAR tier
    let mut best = None;
    let mut best_distance = u8::MAX;
    for (idx, record) in bgc_records.iter().enumerate() {
        if let Some(rec_far) = extract_far_number(&record.vicinity) {
            if record.classification == classification {
                let dist = (far_tier as i16 - rec_far as i16).unsigned_abs() as u8;
                if dist < best_distance {
                    best_distance = dist;
                    best = Some((idx, 0.80 - (dist as f64 * 0.05)));
                }
            }
        }
    }

    best
}
```

### 8.5 Pasig Semicolon Pattern (RDO 43 Special Case)

248 vicinity entries in Pasig embed barangay qualifiers after a semicolon:

```
"ADB AVENUE-SAN MIGUEL AVE ; SAN ANTONIO"
```

Handled during normalization (Phase 0, Step 3). The barangay qualifier is extracted and used to validate/override the user's barangay input, while the pre-semicolon part is treated as the actual vicinity for cross-street matching.

### 8.6 Hybrid Zone Matching (RDO 46, 56-57)

For hybrid zones mixing NCR and provincial patterns:

```rust
fn match_hybrid(
    query: &PropertyQuery,
    candidates: &[ZonalRecord],
    dict: &StreetDictionary,
) -> MatchResult {
    // Try NCR cross-street matching first
    let ncr_result = match_ncr_vicinity(query, candidates, dict);
    if ncr_result.has_matches() {
        return ncr_result;
    }

    // Fall back to provincial road-tier matching
    let prov_result = match_provincial_tier(
        resolve_road_tier(&query.vicinity_hint.unwrap_or_default())
            .unwrap_or(RoadTier::T6Interior),
        query.classification,
        candidates,
    );

    if let Some((idx, conf)) = prov_result {
        return MatchResult::single(candidates[idx].clone(), conf * 0.90);
    }

    MatchResult::empty()
}
```

---

## 9. Phase 6: Classification Filtering

Classification filtering happens in conjunction with vicinity matching. A single street may have multiple entries with different classifications:

```
SHAW BLVD | EDSA - WACK WACK CREEK | RR | 68,000
SHAW BLVD | EDSA - WACK WACK CREEK | CR | 85,000
```

**Rules** (confirmed by CTA rulings — Aquafresh, G.R. 170389):

1. **Published classification prevails** — the engine uses the classification from the BIR schedule, not a reinterpretation
2. **User's classification code determines which row to return** — if user says CR, return the CR row
3. **If user's classification doesn't exist for that street** → check if any catch-all entry has that classification → fallback

```rust
fn filter_by_classification(
    candidates: &[(usize, f64)],
    target: ClassificationCode,
    records: &[ZonalRecord],
) -> Vec<(usize, f64)> {
    let exact: Vec<_> = candidates.iter()
        .filter(|(idx, _)| records[*idx].classification == target)
        .copied()
        .collect();

    if !exact.is_empty() {
        return exact;
    }

    // Classification not found for this street — signal for fallback
    vec![]
}
```

---

## 10. Phase 7: Fallback Hierarchy

When no exact match is found, the engine follows the BIR-prescribed fallback chain. This hierarchy was refined by the verification subagent against RMO 31-2019 preamble text (embedded in workbook headers), CTA rulings, and Respicio & Co. practitioner guidance.

### 10.1 The 5-Level Fallback Chain

```rust
fn resolve_with_fallback(
    query: &PropertyQuery,
    rdo_records: &[ZonalRecord],
    rdo_barangays: &[BarangayIndex],
    dict: &StreetDictionary,
) -> MatchResult {
    let barangay_matches = match_barangay(&query.barangay, rdo_barangays);

    if barangay_matches.is_empty() {
        return MatchResult::no_match(FallbackLevel::NoBrgy);
    }

    for (brgy_idx, brgy_conf) in &barangay_matches {
        let brgy_records = get_barangay_records(*brgy_idx, rdo_records);

        // Level 1: Exact street + vicinity + classification match
        let exact = match_exact(query, &brgy_records, dict);
        if let Some(result) = exact {
            return result.with_fallback_level(FallbackLevel::ExactMatch);
        }

        // Level 2: Same street, different vicinity, same classification
        // (same barangay, "of similar conditions" per RMO 31-2019)
        let same_street = match_same_street_different_vicinity(
            query, &brgy_records, dict
        );
        if let Some(result) = same_street {
            return result.with_fallback_level(FallbackLevel::SameStreetDiffVicinity);
        }

        // Level 3: Barangay catch-all entry with same classification
        // "ALL OTHER STREETS", "ALL LOTS", "INTERIOR LOTS" etc.
        let catch_all = find_catch_all(&brgy_records, query.classification);
        if let Some(result) = catch_all {
            return result.with_fallback_level(FallbackLevel::BarangayCatchAll);
        }
    }

    // Level 4: Adjacent barangay of similar conditions
    // (BIR-prescribed: "same classification in adjacent barangay")
    let adjacent = find_adjacent_barangay_match(
        &barangay_matches[0].0,
        query.classification,
        rdo_records,
        rdo_barangays,
    );
    if let Some(result) = adjacent {
        return result.with_fallback_level(FallbackLevel::AdjacentBarangay);
    }

    // Level 5: Special case — institutional properties
    // Schools, hospitals, churches with no X code entry:
    // "Commercial value of nearest property in same barangay"
    if query.classification == ClassificationCode::X {
        let commercial_fallback = find_nearest_commercial(
            &barangay_matches[0].0, rdo_records
        );
        if let Some(result) = commercial_fallback {
            return result.with_fallback_level(FallbackLevel::InstitutionalCommercial);
        }
    }

    // Level 6: No match — return NULL
    // Per CTA Emiliano/Gamboa: engine MUST NOT interpolate or guess
    // Defer to assessor's FMV or manual RDO inquiry
    MatchResult::no_match(FallbackLevel::NoMatch)
}
```

### 10.2 Fallback Level Descriptions

| Level | Name | BIR Authority | Confidence | Action |
|-------|------|---------------|------------|--------|
| 1 | Exact match | Standard lookup | 0.90-1.0 | Use matched value directly |
| 2 | Same street, different vicinity | RMO 31-2019 Rule 1: "same classification in another street/subdivision within same barangay of similar conditions" | 0.65-0.80 | Use value, flag as approximate |
| 3 | Barangay catch-all | Universal practice ("ALL OTHER STREETS" entries) | 0.75-0.85 | Use catch-all value |
| 4 | Adjacent barangay | RMO 31-2019 Rule 2: "same classification in adjacent barangay of similar conditions" | 0.50-0.65 | Use value, flag as adjacent-brgy fallback |
| 5 | Institutional → commercial | RMO 31-2019 / RAMO 2-91: "commercial value of nearest property in same barangay" | 0.55-0.70 | Use commercial value, flag as institutional fallback |
| 6 | No match (NULL) | CTA Emiliano/Gamboa: BIR cannot substitute | 0.0 | Return NULL, suggest manual RDO inquiry |

### 10.3 Adjacent Barangay Resolution

"Adjacent barangay of similar conditions" requires a barangay adjacency graph. This can be constructed from:

1. **PSGC geographic ordering** — barangays within a municipality are roughly geographically ordered
2. **Workbook ordering** — barangays appear in the workbook in a semi-geographic order
3. **Manual adjacency data** — for the 5 multi-RDO cities, adjacency is well-known

```rust
struct BarangayAdjacency {
    // For each barangay, list of adjacent barangay indices
    neighbors: HashMap<usize, Vec<usize>>,
}

fn find_adjacent_barangay_match(
    target_brgy_idx: &usize,
    classification: ClassificationCode,
    rdo_records: &[ZonalRecord],
    adjacency: &BarangayAdjacency,
) -> Option<MatchResult> {
    if let Some(neighbors) = adjacency.neighbors.get(target_brgy_idx) {
        for neighbor_idx in neighbors {
            let neighbor_records = get_barangay_records(*neighbor_idx, rdo_records);

            // Look for catch-all with same classification
            if let Some(catch_all) = find_catch_all(&neighbor_records, classification) {
                return Some(catch_all.with_confidence(0.55));
            }
        }
    }
    None
}
```

**Practical note**: Barangay adjacency data is not published by BIR. For MVP, the engine can approximate adjacency using workbook ordering (consecutive barangays in the workbook are likely geographically adjacent). Full GIS-based adjacency can be added later using OpenStreetMap boundary data.

---

## 11. Phase 8: Condo Matching Path

Condominiums follow a separate matching path because:
1. The organizational unit is **building name**, not street/vicinity
2. Values are **per-sqm** (all, per Wave 2 condo-table-structures analysis — no per-unit found)
3. Additional inputs needed: tower, floor range, parking type (PS), title type (CCT/TCT)

```rust
fn match_condo(
    query: &PropertyQuery,
    barangay_records: &[ZonalRecord],
) -> MatchResult {
    let building_name = query.condo_building.as_ref()?;
    let normalized = normalize_condo_name(building_name);

    // Step 1: Filter to condo-classified records (RC, CC, PS)
    let condo_records: Vec<_> = barangay_records.iter()
        .filter(|r| r.is_condo)
        .collect();

    // Step 2: Match building name
    // Condo names in workbooks use merged cells (Pattern C/D from Wave 2)
    // Names are pre-extracted during ingestion
    let building_matches: Vec<_> = condo_records.iter()
        .filter(|r| {
            let rec_name = normalize_condo_name(&r.street_name);
            exact_or_fuzzy_match(&normalized, &rec_name, 0.85)
        })
        .collect();

    if building_matches.is_empty() {
        // No building match — try catch-all condo entries
        // Cebu uses: "ALL OTHER CONDOMINIUMS (7 storeys and below)"
        //            "ALL OTHER CONDOMINIUMS (8 storeys and above)"
        return match_condo_catch_all(query, &condo_records);
    }

    // Step 3: Filter by classification (RC vs CC vs PS)
    let classified: Vec<_> = building_matches.iter()
        .filter(|r| r.classification == query.classification)
        .collect();

    if classified.len() == 1 {
        return MatchResult::single(classified[0], 0.95);
    }

    // Step 4: Handle parking slots
    // PS entries may appear as separate blocks or within the building block
    // Association rules (from condo-table-structures analysis):
    // - Dual-PS model: RC+PS and CC+PS are separate entries
    // - PS values are 60-70% of parent classification
    if query.classification == ClassificationCode::PS {
        return match_parking_slot(&building_matches, query);
    }

    // Step 5: Penthouse resolution
    // 3 encoding methods (from condo-table-structures):
    // 1. PH classification code (Paranaque — separate row, may have no value)
    // 2. "(Penthouse)" name suffix (South Makati — separate block)
    // 3. Footnote formula (110% CC or 120% RC)
    if query.is_penthouse() {
        return match_penthouse(&building_matches, query);
    }

    // Multiple matches — return with disambiguation
    MatchResult::multiple(classified, true)
}

fn normalize_condo_name(name: &str) -> String {
    let mut s = name.to_uppercase();
    // Remove common suffixes that may be inconsistent
    s = regex_replace(&s, r"\b(TOWER|TWR|BLDG|BUILDING)\b", "");
    s = regex_replace(&s, r"\b(RESIDENCES?|CONDO(MINIUM)?)\b", "");
    s = collapse_whitespace(&s).trim().to_string();
    s
}
```

### Cebu Storey-Based Catch-All

Cebu introduces a unique condo catch-all requiring building height:

```
ALL OTHER CONDOMINIUMS (7 storeys and below) | RC | 42,000
ALL OTHER CONDOMINIUMS (8 storeys and above) | RC | 62,000
```

The 44-78% premium for taller buildings means this is not a minor detail.

```rust
fn match_condo_catch_all(
    query: &PropertyQuery,
    condo_records: &[ZonalRecord],
) -> MatchResult {
    let catch_alls: Vec<_> = condo_records.iter()
        .filter(|r| r.vicinity.contains("ALL OTHER CONDOMINIUM"))
        .filter(|r| r.classification == query.classification)
        .collect();

    if catch_alls.len() <= 1 {
        return MatchResult::from_optional(catch_alls.first(), 0.80);
    }

    // Multiple catch-alls (Cebu storey-based) — need building height
    // If user provided floor count, resolve automatically
    if let Some(storeys) = query.building_storeys {
        let target = if storeys <= 7 { "below" } else { "above" };
        let matched = catch_alls.iter()
            .find(|r| r.vicinity.to_lowercase().contains(target));
        return MatchResult::from_optional(matched, 0.85);
    }

    // No storey info — return both with disambiguation
    MatchResult::multiple_with_note(
        catch_alls,
        "Building height required: ≤7 storeys or ≥8 storeys"
    )
}
```

---

## 12. Confidence Scoring Model

Every match result carries a confidence score [0.0, 1.0] that reflects how reliable the match is. The score combines multiple factors:

```rust
struct MatchConfidence {
    score: f64,             // 0.0 - 1.0
    fallback_level: FallbackLevel,  // which level resolved the match
    factors: ConfidenceFactors,
}

struct ConfidenceFactors {
    barangay_match: f64,    // 0.0 - 1.0 (how well barangay matched)
    street_match: f64,      // 0.0 - 1.0 (street matching tier)
    vicinity_match: f64,    // 0.0 - 1.0 (vicinity resolution quality)
    classification_exact: bool,  // exact classification match?
}

fn compute_confidence(factors: &ConfidenceFactors, fallback: FallbackLevel) -> f64 {
    let base = match fallback {
        FallbackLevel::ExactMatch => 0.95,
        FallbackLevel::SameStreetDiffVicinity => 0.75,
        FallbackLevel::BarangayCatchAll => 0.80,
        FallbackLevel::AdjacentBarangay => 0.55,
        FallbackLevel::InstitutionalCommercial => 0.60,
        FallbackLevel::NoMatch => 0.0,
    };

    let street_factor = factors.street_match;       // 0.65-1.0
    let vicinity_factor = factors.vicinity_match;   // 0.65-1.0
    let class_factor = if factors.classification_exact { 1.0 } else { 0.85 };

    base * street_factor * vicinity_factor * class_factor
}
```

### Confidence Thresholds for UI Display

| Confidence | Label | UI Action |
|-----------|-------|-----------|
| ≥ 0.85 | HIGH | Display value directly, green indicator |
| 0.65-0.84 | MEDIUM | Display value with "approximate" warning, yellow indicator |
| 0.50-0.64 | LOW | Display value with fallback explanation, orange indicator |
| < 0.50 | VERY LOW | Show value but recommend manual verification, red indicator |
| 0.0 | NO MATCH | No value returned, suggest manual RDO inquiry |

---

## 13. Worked Examples

### Example 1: NCR Exact Match (Happy Path)

**Query**:
- City: Mandaluyong
- Barangay: Addition Hills
- Street: Shaw Blvd
- Vicinity hint: between EDSA and Wack Wack Creek
- Classification: RR

**Resolution**:
1. Phase 1: Mandaluyong → RDO 41 (exact city match)
2. Phase 2: "ADDITION HILLS" barangay found in RDO 41 workbook (exact match, confidence 1.0)
3. Phase 4: "SHAW BLVD" → "SHAW BOULEVARD" → exact match in workbook (confidence 1.0)
4. Phase 5 (NCR mode): Cross-street "EDSA - WACK WACK CREEK" → exact match (confidence 1.0)
5. Phase 6: RR classification → row found with ₱68,000/sqm
6. **Result**: ₱68,000/sqm, confidence 0.95, FallbackLevel::ExactMatch

### Example 2: Former Street Name Alias Resolution

**Query**:
- City: Manila
- Barangay: Zone 79
- Street: Vito Cruz
- Classification: CR

**Resolution**:
1. Phase 1: Manila RDO 33 (Intramuros-Ermita-Malate, Zone 79 falls here)
2. Phase 2: "ZONE 79" → zone-based matching → maps to Malate barangays (confidence 0.85)
3. Phase 4: "VITO CRUZ" → Tier 1 (exact): no match → Tier 2 (alias): lookup finds "VITO CRUZ" → "PABLO OCAMPO SENIOR" → re-match → found (confidence 0.95)
4. Phase 5: NCR cross-street matching against Pablo Ocampo Sr. entries
5. Phase 6: CR classification filter
6. **Result**: Matched via alias resolution, confidence 0.85, FallbackLevel::ExactMatch

### Example 3: Provincial Road-Tier Fallback

**Query**:
- City: Calamba, Laguna
- Barangay: Bucal
- Vicinity hint: "interior lot"
- Classification: RR

**Resolution**:
1. Phase 1: Calamba → RDO 56 (Laguna)
2. Phase 2: "BUCAL" barangay found in RDO 56 workbook
3. Phase 5 (Provincial mode): "interior lot" → RoadTier::T6Interior
4. Check T6 Interior for RR classification: found → ₱2,500/sqm
5. **Result**: ₱2,500/sqm, confidence 0.90, FallbackLevel::ExactMatch

### Example 4: Provincial Road-Tier with Tier Fallback

**Query**:
- City: Calamba, Laguna
- Barangay: Bucal
- Vicinity hint: "along municipal road"
- Classification: A1 (Irrigated Riceland)

**Resolution**:
1. Phase 1-2: Same as Example 3
2. Phase 5: "along municipal road" → RoadTier::T3Municipal
3. Check T3 Municipal for A1: NOT FOUND (only CR and RR entries at T3)
4. Tier fallback: T4 Barangay for A1 → found → ₱800/sqm
5. **Result**: ₱800/sqm, confidence 0.70, FallbackLevel::SameStreetDiffVicinity (tier approximation)

### Example 5: Catch-All Fallback

**Query**:
- City: Makati
- Barangay: Bel-Air
- Street: Nicanor Garcia St (a small interior street)
- Classification: RR

**Resolution**:
1. Phase 1: Makati → RDO 49 (North Makati, Bel-Air I-IV)
2. Phase 2: "BEL-AIR" barangay found
3. Phase 4: "NICANOR GARCIA STREET" → no exact match, no alias, no fuzzy match above 0.90
4. Phase 7 Level 3: Catch-all "ALL OTHER STREETS" entry for Bel-Air with RR classification → ₱175,000/sqm
5. **Result**: ₱175,000/sqm, confidence 0.75, FallbackLevel::BarangayCatchAll

### Example 6: BGC FAR-Based Lookup

**Query**:
- City: Taguig
- Barangay: Fort Bonifacio (BGC)
- Classification: CR
- Floor Area Ratio: 8

**Resolution**:
1. Phase 1: Taguig → RDO 44
2. Phase 2: "FORT BONIFACIO" → BGC area detected
3. Mode: BgcFar
4. Phase 5: FAR 8 + CR → deterministic lookup → ₱1,000,000/sqm (estimated)
5. **Result**: Direct FAR-based value, confidence 1.0

### Example 7: Condo with Storey-Based Catch-All

**Query**:
- City: Cebu City
- Barangay: Lahug
- Condo: "Some New Condo" (not in workbook)
- Classification: RC
- Building storeys: 12

**Resolution**:
1. Phase 1: Cebu City → RDO 83 or 84 (north/south split)
2. Phase 2: "LAHUG" barangay found
3. Phase 3: Condo path triggered (building name provided + RC classification)
4. Building name match: "SOME NEW CONDO" → no match in workbook
5. Condo catch-all: "ALL OTHER CONDOMINIUMS (8 storeys and above)" → 12 > 7 → match
6. **Result**: Catch-all condo value, confidence 0.80

### Example 8: No Match → NULL

**Query**:
- City: Pahamuddin (new BARMM municipality, 2024)
- Barangay: any
- Classification: RR

**Resolution**:
1. Phase 1: Pahamuddin → RDO assignment UNKNOWN (8 BARMM municipalities gap)
2. Default to parent municipality RDO (RDO 107 Cotabato City)
3. Search RDO 107 workbook: Pahamuddin barangays not found (municipality didn't exist when workbook was published)
4. Adjacent barangay search: inconclusive
5. **Result**: NULL, confidence 0.0, FallbackLevel::NoMatch, with note: "Newly created municipality — no published zonal values. Recommend manual RDO inquiry."

---

## 14. Rust Data Structures

### Index Structure

The matching engine operates on a pre-built index for O(1) barangay lookup and O(n) within-barangay search (where n is small, ~30-200 records):

```rust
/// Primary index structure for zonal value lookup
struct ZonalIndex {
    /// RDO → list of barangay indices
    rdo_barangays: HashMap<u8, Vec<BarangayEntry>>,

    /// All records, stored contiguously per barangay
    records: Vec<ZonalRecord>,

    /// Street name dictionary (for cross-street disambiguation)
    street_dict: StreetDictionary,

    /// Street alias table (former → current name mappings)
    alias_table: AliasTable,

    /// Barangay adjacency graph (for Level 4 fallback)
    adjacency: BarangayAdjacency,

    /// RDO jurisdiction mapping (city/barangay → RDO)
    jurisdiction: JurisdictionMap,
}

struct BarangayEntry {
    name: String,              // normalized uppercase
    normalized_name: String,   // further normalized (STA→SANTA, etc.)
    zone_id: Option<u16>,      // Manila zone number
    record_range: Range<usize>, // index into records[]
    vicinity_mode: VicinityMode,
    has_catch_all: bool,       // whether "ALL OTHER STREETS" exists
    has_condo_entries: bool,
}
```

### Memory Layout for WASM

From Wave 2 data-size-estimation:
- **Records**: 690K × 17 bytes = 11.7 MB
- **String table**: 1.46 MB (deduplicated)
- **Barangay index**: ~42K entries × ~32 bytes = 1.3 MB
- **Street dictionary**: ~13K entries × ~24 bytes = 312 KB
- **Alias table**: ~500 entries × ~64 bytes = 32 KB
- **Adjacency graph**: ~42K × ~8 bytes = 336 KB
- **Jurisdiction map**: ~42K × ~64 bytes = 2.7 MB
- **Total index**: ~17.8 MB raw → **~5.2 MB brotli** (within WASM budget)

### Query Execution Flow

```rust
impl ZonalIndex {
    pub fn lookup(&self, query: &PropertyQuery) -> MatchResult {
        // Phase 0: Normalize query
        let norm_query = normalize_query(query);

        // Phase 1: RDO resolution
        let rdo = self.jurisdiction.resolve(
            &norm_query.city_municipality,
            &norm_query.barangay,
            norm_query.transaction_date,
        )?;

        // Phase 2: Barangay filter
        let barangay_candidates = match_barangay(
            &norm_query.barangay,
            &self.rdo_barangays[&rdo],
        );

        // Phase 3: Condo fork
        if norm_query.is_condo() {
            return self.match_condo(&norm_query, &barangay_candidates);
        }

        // Phases 4-7: Land matching with fallback
        self.resolve_with_fallback(
            &norm_query, &barangay_candidates, &self.street_dict,
        )
    }
}
```

---

## 15. Edge Cases Catalog

### 15.1 Input Edge Cases

| Case | Example | Resolution |
|------|---------|-----------|
| No street provided | "Brgy Poblacion, Makati" | Skip Phase 4, go directly to catch-all (Level 3) |
| No barangay provided | "Ayala Ave, Makati" | Search all barangays in RDO for street match; return with lower confidence |
| No classification | Property use unknown | Return all classification entries for the matched street; require user selection |
| Misspelled barangay | "Bel Air" instead of "Bel-Air" | Fuzzy match catches this (Jaro-Winkler 0.92) |
| Former city name | "Pasig" when barangay is now in Taguig | Jurisdiction map handles EMBO transfer temporally |

### 15.2 Data Edge Cases

| Case | Example | Resolution |
|------|---------|-----------|
| Multiple ZVs same street/classification | Different DO revision sheets have different values | Use effectivity date to select correct revision |
| Street appears in multiple barangays | "RIZAL AVENUE" in 5+ barangays | Barangay filter resolves this (Phase 2 before Phase 4) |
| Blank vicinity (continuation row) | Inherited from merged cell above | Resolved during ingestion (carry-forward) |
| Footnote-marked street | "*RIZAL AVE" (newly identified) | Strip asterisks during normalization, preserve as metadata |
| Non-integer ZV | ₱1,500.50 in Cebu workbooks | Use f64 or fixed-point arithmetic |
| Embedded revision numbers | "A50 23*" in RDO 83 Cebu | Strip during normalization (regex: strip trailing `\d+\*?`) |

### 15.3 Structural Edge Cases

| Case | Example | Resolution |
|------|---------|-----------|
| Intra-barangay RDO split | QC Commonwealth (west=RDO 28, east=RDO 39) | Street-level disambiguation in Phase 1 |
| Different municipalities on different revisions | RDO 56 Laguna: Calamba on DO X, Bay on DO Y | Per-municipality effectivity tracking |
| Duplicate DO numbers | RDO 57: "DO 11-15" appears twice for different municipalities | Unique key is (RDO, DO#, municipality), not DO# alone |
| Under-construction section | RDO 51 Pasay has dedicated condo section | Treat as separate condo catch-all pool |
| CCT/TCT bifurcation | CCT uses composite condo ZV; TCT requires land+improvement | Require title_type input for condo lookups |

---

## 16. Performance Considerations for WASM

### Query Latency Target

**< 10ms** per lookup on mobile devices (ARM64, 2GB RAM).

### Algorithmic Complexity

| Phase | Complexity | Typical n |
|-------|-----------|-----------|
| Phase 0 (normalize) | O(len(query)) | ~50 chars |
| Phase 1 (RDO) | O(1) hash lookup | 1 |
| Phase 2 (barangay) | O(b) where b = barangays in RDO | ~50-200 |
| Phase 4 (street) | O(s) where s = records in barangay | ~30-200 |
| Phase 5 (vicinity) | O(s) | ~30-200 |
| Phase 6 (classification) | O(s) | ~30-200 |
| Phase 7 (fallback) | O(s × neighbors) | ~200-1000 |

**Total**: O(b + s × k) where k is the number of fallback attempts. In practice, < 1000 comparisons per lookup. Well within 10ms budget.

### String Comparison Optimization

Jaro-Winkler is O(m+n) per comparison. For fuzzy matching across ~200 records:
- ~200 × O(50) = ~10,000 character operations
- At ~1 GHz WASM throughput: < 1ms

No special optimization needed. The algorithm is inherently fast for this data size.

---

## 17. Open Questions for Wave 5 Architecture

1. **Autocomplete vs batch lookup**: Should the frontend expose typeahead search (requires streaming partial matches) or form-based lookup (simpler)?
2. **Confidence threshold for auto-accept**: At what confidence level should the UI accept a match without user confirmation?
3. **Offline-first**: Should the WASM bundle include ALL data for offline use, or lazy-load per-RDO?
4. **History/audit trail**: Should the engine log every query with its match path for tax compliance documentation?
5. **Adjacent barangay approximation**: Use workbook ordering (simple) or OSM boundary data (accurate but heavyweight)?

---

## 18. Verification Summary

Cross-checked against the verification report (`address-matching-verification.md`), which validated 6 claims against 15+ independent sources:

| Design Decision | Verification Status | Sources |
|----------------|-------------------|---------|
| Barangay+street+vicinity matching hierarchy | CONFIRMED | BIR RMC 115-2020, Respicio & Co., Loop Wave 2 |
| 5-level fallback chain (refined from 4-level) | CONFIRMED with refinements | RMO 31-2019 preamble, CTA rulings, BIR practice |
| Bidirectional alias table for renamed streets | CONFIRMED | Wikipedia, BIR workbook annotations, Top Gear PH |
| Hybrid matching (normalize + Jaro-Winkler) | CONFIRMED as best practice | CMU paper, Filipino NLP research, Babel Street |
| Geocoding insufficient for core matching | CONFIRMED | Google Geocoding docs, OSM PH wiki, PhilGIS defunct |
| NULL return (not interpolation) for no match | CONFIRMED | CTA Emiliano/Gamboa rulings |

**Key refinement from verification**: Original 4-level fallback was missing "adjacent barangay of similar conditions" (BIR's prescribed Level 3 from RMO 31-2019 Rule 2) and the institutional-property special case. Both added to the final design.

---

## Sources

- **BIR RMC 115-2020** — confirms ONETT processors use published schedules for lookup
- **RMO 31-2019 preamble** (embedded in workbook headers) — prescribes 3-rule fallback chain
- **CTA cases** (Emiliano/Gamboa, Aquafresh) — NULL return mandate, published classification prevails
- **Respicio & Co.** — practitioner guidance on address resolution
- **CMU Cohen/Ravikumar/Fienberg 2003** — SoftTFIDF hybrid approach for name matching
- **Filipino NLP research (EMNLP 2022)** — Damerau-Levenshtein + N-gram for Filipino text
- **Wikipedia "List of renamed streets in Metro Manila"** — alias table seed data
- **Wave 2 analyses**: address-vicinity-patterns, workbook-column-layouts, merged-cell-patterns, footnote-convention-mapping, classification-code-usage, condo-table-structures, data-size-estimation
- **Wave 3 analysis**: rdo-jurisdiction-mapping
- **Verification report**: address-matching-verification.md (15+ sources cross-checked)
