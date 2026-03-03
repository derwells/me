# Fallback Hierarchy Implementation — Resolution Logic Deep-Dive

**Wave:** 3 — Resolution Logic Deep-Dive
**Date:** 2026-03-03
**Aspect:** `fallback-hierarchy-implementation`
**Depends on:** Wave 2 (address-vicinity-patterns, classification-code-usage, condo-table-structures, data-size-estimation), Wave 3 (address-matching-algorithms, classification-resolution-logic, rdo-jurisdiction-mapping)
**Verification:** Cross-checked against 18+ independent sources via two verification subagents (see `fallback-hierarchy-verification.md`, `fallback-hierarchy-cross-check.md`)
**Prior art:** `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md` §Fallback Rules, `analysis/address-matching-algorithms.md` §10

---

## 1. Summary

The fallback hierarchy is a **7-level decision tree** (not a strict 6-level linear chain as originally proposed) that governs what happens when a property cannot be matched to an exact row in the BIR zonal value schedule. Each level has distinct legal authority, applies to a specific gap scenario, and produces a different confidence score for the engine.

**Key structural finding from verification:** The hierarchy is not strictly linear — Level 5 (institutional fallback) is a **classification-specific branch** that applies only to X-coded properties, while Level 5A (RAMO 2-91) addresses a fundamentally different scenario (no zonal data exists at all for the area). These are parallel branches, not sequential steps.

**Critical engine design principle (from CTA rulings):** The engine MUST return NULL rather than interpolate or compute at fallback levels 5A and beyond. Per *Spouses Emiliano v. CIR* (CTA EB No. 1103, 2015) and *CIR v. Heirs of Gamboa* (CTA Case No. 9720, 2020), the BIR itself cannot substitute arbitrary valuations when no published zonal value exists. An automated engine certainly should not.

**7 levels formalized with legal authority:**

| Level | Scenario | Authority | Engine Computes Value? | Confidence |
|-------|----------|-----------|----------------------|------------|
| 1 | Exact match (street + vicinity + classification) | Section 6(E) NIRC; RMC 115-2020 | YES | 0.90–1.0 |
| 2 | Same street, different vicinity (same barangay + classification) | DOF DO standard footnotes (Rule 3) | YES | 0.65–0.80 |
| 3 | Barangay catch-all ("ALL OTHER STREETS/LOTS") | DOF DO standard footnotes (Rule 3 implementation) | YES | 0.75–0.85 |
| 4 | Adjacent barangay, same classification | DOF DO standard footnotes (Rules 1 & 2) | YES (with flag) | 0.50–0.65 |
| 5 | Institutional (X) → nearest commercial (CR) | DOF DO standard footnotes (X provision) | YES (with flag) | 0.55–0.70 |
| 5A | RAMO 2-91 LGU FMV markup | RAMO 2-91; DOF DO footnotes | **NO** — informational only | N/A |
| 6 | No match (NULL) | CTA Emiliano/Gamboa | **NO** — return NULL | 0.0 |

---

## 2. Authority Attribution Corrections

The prior analysis and original PROMPT.md cited "RMO 31-2019" as the authority for fallback rules. **This is imprecise.** The verification subagents identified the correct attribution:

| Level | Previously Cited | Correct Authority | Correction Detail |
|-------|-----------------|-------------------|-------------------|
| 2 | RMO 31-2019 practice | **DOF Department Order standard footnotes** | The fallback rules appear in DOF DOs (the published schedules), not in RMO 31-2019 body text. RMO 31-2019 governs the *process* for establishing values; DOF DOs contain the actual values and rules. |
| 3 | RMO 31-2019 practice | **DOF DO standard footnotes (Rule 3)** | "ALL OTHER STREETS" entries are the operationalization of the DOF DO Rule 3 footnote. |
| 4 | RMO 31-2019 Rule 2 | **DOF DO standard footnotes (Rules 1 & 2)** | "Rule 2" numbering matches the DOF DO footnotes, not a numbered provision in RMO 31-2019. |
| 5 | RMO 31-2019 / RAMO 2-91 | **DOF DO standard footnotes ONLY** | RAMO 2-91 covers a different scenario (no zonal data at all). The institutional fallback is exclusively a DOF DO footnote provision. |

**Provenance upgrade:** These DOF DO footnotes are DOF Secretary-signed, published per RR 6-01 requirements, and carry full regulatory authority. They are NOT mere "workbook guidelines" — they are regulatory text embedded in the published schedule.

### DOF DO Footnotes — Exact Text (Verified)

From the East Makati 2021 (7th Revision) DOF Department Order, confirmed across RDO 82 (Cebu City South), RDO 83 (Talisay/Minglanilla), and 28+ workbooks in the sample:

**Rule 1 (Classification Gap → Adjacent Barangay):**
> "WHERE IN THE APPROVED LISTING OF ZONAL VALUES (FOR VARIOUS CLASSIFICATIONS OF REAL PROPERTY), NO ZONAL VALUE HAS BEEN PRESCRIBED FOR A PARTICULAR CLASSIFICATION, THE ZONAL VALUE PRESCRIBED FOR THE SAME CLASSIFICATION OF REAL PROPERTY LOCATED IN AN ADJACENT BARANGAY OF SIMILAR CONDITIONS SHALL BE USED."

**Rule 2 (Data Gap → Adjacent Barangay):**
> "IN A BARANGAY WHERE NO SALE, EXCHANGE, OR OTHER DISPOSITION OF LAND HAS BEEN EFFECTED, THE APPROVED ZONAL VALUE OF A SIMILARLY SITUATED PROPERTY IN AN ADJACENT BARANGAY OF SIMILAR CONDITIONS SHALL BE USED."

**Rule 3 (Street Gap → Same Barangay Fallback):**
> "IF THERE IS NO PRESCRIBED ZONAL VALUE FOR A PARTICULAR STREET/SUBDIVISION IN A BARANGAY, THE ZONAL VALUE PRESCRIBED FOR THE SAME CLASSIFICATION OF REAL PROPERTY LOCATED IN THE OTHER STREET/SUBDIVISION WITHIN THE SAME BARANGAY OF SIMILAR CONDITIONS SHALL BE USED."

**Institutional Property (X) Provision:**
> "THESE ARE AREAS FOR SCHOOL, HOSPITAL AND CHURCHES. IF NO ZONAL VALUE HAS BEEN PRESCRIBED, THE COMMERCIAL VALUE OF THE PROPERTY NEAREST TO THE INSTITUTION, WITHIN THE SAME BARANGAY AND STREET SHALL BE USED."

**RAMO 2-91 Reference:**
> "IN THE ABSENCE OF ZONAL VALUATION, PROPERTY SHALL BE VALUED PURSUANT TO RAMO 2-91."

---

## 3. Level-by-Level Implementation with Worked Examples

### 3.1 Level 1: Exact Match

**Scenario:** Street + vicinity + classification found in the schedule.

**Algorithm:** Standard address matching pipeline (Phase 4-6 from `address-matching-algorithms.md`). This is the direct lookup — no fallback logic needed.

**Worked Example 1 — NCR Cross-Street:**
```
Input:
  City: Mandaluyong
  Barangay: Addition Hills
  Street: Shaw Boulevard
  Vicinity: "near EDSA"
  Classification: RR

Matching Process:
  1. RDO resolution: Mandaluyong → RDO 41
  2. Barangay match: "Addition Hills" → exact match (confidence 1.0)
  3. Street match: "Shaw Boulevard" → normalize → "SHAW BOULEVARD" → exact match
  4. Vicinity match: NCR cross-street mode — workbook has:
     "SHAW BLVD | EDSA - WACK WACK CREEK | RR | 68,000"
     "SHAW BLVD | WACK WACK CREEK - SAN MIGUEL AVE | RR | 60,000"
     User said "near EDSA" → first segment matches (confidence 0.85)
  5. Classification: RR → exact match in first record

Result:
  Value: ₱68,000/sqm
  Fallback Level: 1 (Exact Match)
  Confidence: 0.85
  Source: RDO 41, DO 059-2022 (6th Revision), Effectivity 2022-09-12
```

**Worked Example 2 — Provincial Road-Proximity:**
```
Input:
  Province: Pangasinan
  City/Municipality: Calasiao
  Barangay: Poblacion East
  Vicinity: "along MacArthur Highway"
  Classification: CR

Matching Process:
  1. RDO resolution: Calasiao, Pangasinan → RDO 4
  2. Barangay match: "Poblacion East" → exact match
  3. Street match: N/A (provincial mode uses road-tier, not street names)
  4. Vicinity mode: ProvincialRoadTier
     "along MacArthur Highway" → detect "HIGHWAY" → RoadTier::T1National
     Workbook: "ALONG NATIONAL HIGHWAY | CR | 5,000"
  5. Classification: CR → exact match

Result:
  Value: ₱5,000/sqm
  Fallback Level: 1 (Exact Match)
  Confidence: 0.95
  Source: RDO 4, DO 015-2023 (8th Revision)
```

### 3.2 Level 2: Same Street, Different Vicinity

**Scenario:** The property's street exists in the schedule, but the specific vicinity segment doesn't match. The engine falls back to another vicinity on the same street with the same classification.

**Legal basis:** DOF DO Rule 3 — "the zonal value prescribed for the same classification of real property located in the other street/subdivision within the same barangay of similar conditions shall be used."

**Algorithm:**
```rust
fn fallback_same_street(
    query: &PropertyQuery,
    street_matches: &[ZonalRecord],
) -> Option<FallbackResult> {
    // Filter to same classification, different vicinity
    let same_class_diff_vicinity: Vec<_> = street_matches.iter()
        .filter(|r| r.classification == query.classification)
        .filter(|r| !vicinity_matches(&r.vicinity, &query.vicinity))
        .collect();

    if same_class_diff_vicinity.is_empty() {
        return None;
    }

    // For NCR: return the segment with the lowest ZV (conservative — "of similar conditions")
    // For provincial: return the tier closest to the query tier
    let best = match query.vicinity_mode {
        VicinityMode::NcrCrossStreet => {
            // Multiple segments exist — return all for disambiguation
            // If only 1 alternative exists, use it directly
            if same_class_diff_vicinity.len() == 1 {
                Some(FallbackResult {
                    record: same_class_diff_vicinity[0].clone(),
                    confidence: 0.75,
                    fallback_level: FallbackLevel::SameStreetDiffVicinity,
                    note: format!(
                        "No exact vicinity match. Using same street, different segment: '{}'",
                        same_class_diff_vicinity[0].vicinity
                    ),
                })
            } else {
                // Multiple alternatives — return range + disambiguation
                let min_zv = same_class_diff_vicinity.iter().map(|r| r.zv).min()?;
                let max_zv = same_class_diff_vicinity.iter().map(|r| r.zv).max()?;
                Some(FallbackResult {
                    record: same_class_diff_vicinity[0].clone(), // lowest ZV (conservative)
                    confidence: 0.65,
                    fallback_level: FallbackLevel::SameStreetDiffVicinity,
                    note: format!(
                        "No exact vicinity match. {} segments found for this street ({} classification). \
                         ZV range: ₱{}-₱{}/sqm. Select the correct segment.",
                        same_class_diff_vicinity.len(),
                        query.classification,
                        min_zv, max_zv
                    ),
                })
            }
        }
        VicinityMode::ProvincialRoadTier => {
            // Fall through to the next available tier
            // Handled by match_provincial_tier() in address-matching-algorithms.md §8.3
            let target_tier = resolve_road_tier(&query.vicinity_hint)?;
            match_next_available_tier(target_tier, &same_class_diff_vicinity)
        }
        _ => None,
    };

    best
}
```

**Worked Example 3 — NCR Same Street Different Vicinity:**
```
Input:
  City: Makati
  Barangay: Bel-Air
  Street: Ayala Avenue
  Vicinity: "between EDSA and Paseo de Roxas" (no exact segment match)
  Classification: CR

Workbook has 12 Ayala Avenue segments:
  "AYALA AVE | EDSA - PASEO DE ROXAS | CR | 300,000"     ← exists but
  "AYALA AVE | PASEO DE ROXAS - MAKATI AVE | CR | 280,000"  user's text doesn't match
  "AYALA AVE | MAKATI AVE - GIL PUYAT | CR | 250,000"       any segment perfectly

Matching Process:
  1. Street match: "Ayala Avenue" → "AYALA AVE" → match (Tier 1: exact after normalization)
  2. Vicinity match: "between EDSA and Paseo de Roxas" →
     Parse cross-streets: A="EDSA", B="PASEO DE ROXAS"
     Try match against segment "EDSA - PASEO DE ROXAS" → cross-street match (confidence 0.90)
  3. Actually, this IS an exact match (Level 1, not Level 2)

Better Level 2 example:
Input:
  Vicinity: "near Greenbelt" (NO cross-streets provided)

  1. Street match: "AYALA AVE" → exact
  2. Vicinity match: "near Greenbelt" → no cross-street pair parseable
  3. Fallback to Level 2: 12 segments exist for Ayala Ave CR
     ZV range: ₱150,000 - ₱350,000/sqm
     Return: all 12 segments for user disambiguation

Result:
  Value: ₱150,000 - ₱350,000/sqm (range)
  Fallback Level: 2 (Same Street, Different Vicinity)
  Confidence: 0.65
  Note: "12 segments found for AYALA AVE (CR). Please select the correct cross-street segment."
```

**Worked Example 4 — Provincial Tier Fallback:**
```
Input:
  Province: Laguna
  Municipality: Cabuyao
  Barangay: Marinig
  Vicinity: "along provincial road"
  Classification: RR

Workbook has for Marinig:
  "ALONG NATIONAL HIGHWAY | RR | 7,000"
  "INTERIOR | RR | 3,000"
  (no "ALONG PROVINCIAL ROAD" entry for this barangay)

Matching Process:
  1. Vicinity parse: "along provincial road" → RoadTier::T2Provincial
  2. Search Marinig records for T2Provincial + RR → not found
  3. Fallback: next lower tier = T3Municipal → not found
  4. Fallback: T4Barangay → not found
  5. Fallback: T5FiftyMeters → not found
  6. Fallback: T6Interior → found! "INTERIOR | RR | 3,000"

Result:
  Value: ₱3,000/sqm
  Fallback Level: 2 (Same Street/Barangay, Different Vicinity — tier downgrade)
  Confidence: 0.60 (penalized for 4 tiers of downgrade)
  Note: "No provincial road entry found for Marinig. Fell back to interior lot rate."
```

### 3.3 Level 3: Barangay Catch-All

**Scenario:** The property's street doesn't exist in the schedule at all. The barangay has an "ALL OTHER STREETS" or "ALL OTHER LOTS" catch-all entry.

**Data:** 185 catch-all entries documented across 31 sampled workbooks (from Wave 2). Universal pattern — every well-populated barangay has one.

**Algorithm:**
```rust
fn fallback_barangay_catch_all(
    classification: ClassCode,
    barangay_records: &[ZonalRecord],
) -> Option<FallbackResult> {
    // Catch-all patterns (from address-vicinity-patterns.md)
    let catch_all_patterns = [
        "ALL OTHER STREETS",
        "ALL OTHER LOTS",
        "ALL LOTS",
        "INTERIOR LOTS",
        "ALL OTHER SUBDIVISIONS",
        "ALL OTHER AREAS",
        "ALL OTHER CONDOMINIUMS",  // Cebu condo catch-all
    ];

    // Find catch-all entry matching the target classification
    let catch_all = barangay_records.iter()
        .filter(|r| {
            let upper = r.street_name.to_uppercase();
            catch_all_patterns.iter().any(|p| upper.contains(p))
                || r.vicinity.to_uppercase().contains("ALL OTHER")
        })
        .filter(|r| r.classification == classification)
        .next();

    match catch_all {
        Some(record) => {
            // Check if catch-all has an actual value (some are empty/deleted)
            if record.zv == 0 {
                // Empty catch-all — "No value recommended; all streets identified"
                // (documented for some Mandaluyong barangays)
                return Some(FallbackResult {
                    record: record.clone(),
                    confidence: 0.0,
                    fallback_level: FallbackLevel::BarangayCatchAll,
                    note: "Barangay catch-all entry exists but has no recommended value \
                           (all streets are individually enumerated). \
                           The property's street may be listed under a different name.",
                });
            }

            Some(FallbackResult {
                record: record.clone(),
                confidence: 0.80,
                fallback_level: FallbackLevel::BarangayCatchAll,
                note: format!(
                    "Street not found in schedule. Using barangay catch-all rate: '{}'",
                    record.street_name
                ),
            })
        }
        None => None,
    }
}
```

**Important caveat from verification:** Some fully-enumerated barangays have "ALL OTHER STREETS" entries with **zero or deleted values** — meaning all streets are individually listed, and the catch-all is vestigial. The Mandaluyong 2019 schedule documents this explicitly: "No value recommended; all streets in the barangay were already identified."

**Worked Example 5 — Catch-All:**
```
Input:
  City: Quezon City
  Barangay: Tandang Sora
  Street: "Kamagong Street" (a small interior street)
  Classification: RR

Workbook: Kamagong Street is NOT individually listed.
Barangay has: "ALL OTHER STREETS | RR | 22,000"

Result:
  Value: ₱22,000/sqm
  Fallback Level: 3 (Barangay Catch-All)
  Confidence: 0.80
  Note: "Street 'KAMAGONG STREET' not found in Tandang Sora schedule. \
         Using catch-all rate 'ALL OTHER STREETS IN TANDANG SORA' (RR)."
  Source: RDO 40, current revision
```

**Worked Example 6 — Provincial Catch-All:**
```
Input:
  Province: Pangasinan
  Municipality: Mangaldan
  Barangay: Poblacion
  Street: N/A (no specific street)
  Vicinity: "interior lot, 200 meters from municipal road"
  Classification: A1 (Riceland Irrigated)

Workbook has:
  "ALL LOTS | ALONG NATIONAL HIGHWAY | A1 | 250"
  "ALL LOTS | ALONG PROVINCIAL ROAD | A1 | 200"
  "ALL LOTS | ALONG MUNICIPAL ROAD | A1 | 170"
  "ALL LOTS | INTERIOR | A1 | 120"

Matching Process:
  1. Vicinity: "interior lot, 200 meters from municipal road"
     → hybrid: contains "interior" AND mentions "municipal road"
     → primary parse: "INTERIOR" → T6Interior
  2. Match T6Interior + A1 → found "INTERIOR | A1 | 120"

Result:
  Value: ₱120/sqm
  Fallback Level: 1 (exact match in provincial road-tier mode)
  Confidence: 0.90
```

### 3.4 Level 4: Adjacent Barangay

**Scenario:** No zonal value exists for the target classification in the entire barangay — neither specific streets nor catch-all entries have the classification. The engine searches adjacent barangays for the same classification.

**Legal basis:** DOF DO Rules 1 and 2 — "the zonal value prescribed for the same classification of real property located in an adjacent barangay of similar conditions shall be used."

**Two distinct sub-scenarios:**
- **Rule 1 (Classification gap):** Barangay has zonal values but not for the queried classification (e.g., barangay has CR and RR but not I). → Same classification from adjacent barangay.
- **Rule 2 (Data gap):** Barangay has NO sales data at all, resulting in no zonal values for any classification. → Similarly situated property from adjacent barangay. (Relevant mainly during schedule creation, rare at runtime.)

**Algorithm:**
```rust
fn fallback_adjacent_barangay(
    target_brgy_idx: usize,
    classification: ClassCode,
    rdo_data: &RdoData,
) -> Option<FallbackResult> {
    // Build adjacency from workbook ordering (approximation)
    // Consecutive barangays in the workbook are geographically adjacent
    let prev = target_brgy_idx.checked_sub(1);
    let next = if target_brgy_idx + 1 < rdo_data.barangays.len() {
        Some(target_brgy_idx + 1)
    } else {
        None
    };

    // Search adjacent barangays: try immediate neighbors first
    let neighbors: Vec<usize> = [prev, next].iter()
        .filter_map(|&n| n)
        .collect();

    for &neighbor_idx in &neighbors {
        let neighbor_records = rdo_data.get_barangay_records(neighbor_idx);
        let neighbor_name = &rdo_data.barangays[neighbor_idx].name;

        // First try: catch-all entry in adjacent barangay
        if let Some(catch_all) = find_catch_all_for_classification(
            &neighbor_records, classification
        ) {
            return Some(FallbackResult {
                record: catch_all.clone(),
                confidence: 0.55,
                fallback_level: FallbackLevel::AdjacentBarangay,
                note: format!(
                    "No {} value found in target barangay. Using adjacent barangay \
                     '{}' catch-all rate (per DOF DO standard footnote Rule 1).",
                    classification, neighbor_name
                ),
            });
        }

        // Second try: any entry with same classification in adjacent barangay
        // Use the lowest value (conservative — "of similar conditions")
        let same_class: Vec<_> = neighbor_records.iter()
            .filter(|r| r.classification == classification && r.zv > 0)
            .collect();

        if let Some(min_record) = same_class.iter().min_by_key(|r| r.zv) {
            return Some(FallbackResult {
                record: (*min_record).clone(),
                confidence: 0.50,
                fallback_level: FallbackLevel::AdjacentBarangay,
                note: format!(
                    "No {} value found in target barangay. Using lowest {} value from \
                     adjacent barangay '{}': ₱{}/sqm (per DOF DO Rule 1).",
                    classification, classification, neighbor_name, min_record.zv
                ),
            });
        }
    }

    // Expand search to 2nd-order neighbors (neighbors of neighbors)
    // Only if immediate neighbors also lack the classification
    for &neighbor_idx in &neighbors {
        let prev2 = neighbor_idx.checked_sub(1).filter(|&n| n != target_brgy_idx);
        let next2 = (neighbor_idx + 1 < rdo_data.barangays.len())
            .then_some(neighbor_idx + 1)
            .filter(|&n| n != target_brgy_idx);

        for second_neighbor in [prev2, next2].iter().filter_map(|&n| n) {
            let records = rdo_data.get_barangay_records(second_neighbor);
            if let Some(catch_all) = find_catch_all_for_classification(
                &records, classification
            ) {
                return Some(FallbackResult {
                    record: catch_all.clone(),
                    confidence: 0.45,
                    fallback_level: FallbackLevel::AdjacentBarangay,
                    note: format!(
                        "No {} value in target or adjacent barangay. Using 2nd-adjacent \
                         barangay '{}' (per DOF DO Rule 1).",
                        classification,
                        rdo_data.barangays[second_neighbor].name
                    ),
                });
            }
        }
    }

    None
}
```

**Adjacency approximation:** True geographic adjacency requires GIS boundary data (e.g., from PSA PSGC or OpenStreetMap). For MVP, workbook ordering provides a reasonable approximation — barangays appear in the workbook in semi-geographic order (verified across 31 workbooks). The engine can be upgraded to true GIS adjacency in a later iteration.

**Worked Example 7 — Adjacent Barangay Classification Gap:**
```
Input:
  City: Mandaluyong
  Barangay: Plainview
  Street: any
  Classification: I (Industrial)

Workbook: Plainview has entries for RR, CR only. No I (Industrial) entries.

Adjacent barangays in workbook order:
  - Namayan: has RR, CR (no I)
  - Highway Hills: has RR, CR, I (has I!)
    "ALL OTHER STREETS | I | 40,000"

Result:
  Value: ₱40,000/sqm
  Fallback Level: 4 (Adjacent Barangay)
  Confidence: 0.55
  Note: "No Industrial (I) value found in Plainview. Using adjacent barangay \
         Highway Hills catch-all rate (per DOF DO standard footnote Rule 1)."
```

### 3.5 Level 5: Institutional → Commercial (Branch — X Only)

**Scenario:** Property is classified as X (Institutional — school, hospital, church) but no X code entry exists in the schedule for this location. The engine falls back to the nearest commercial (CR) value on the same street within the same barangay.

**Legal basis:** DOF DO standard footnote: "THESE ARE AREAS FOR SCHOOL, HOSPITAL AND CHURCHES. IF NO ZONAL VALUE HAS BEEN PRESCRIBED, THE COMMERCIAL VALUE OF THE PROPERTY NEAREST TO THE INSTITUTION, WITHIN THE SAME BARANGAY AND STREET SHALL BE USED."

**Key precision from verification:** The DOF DO text says "within the same barangay **and street**" — this is more restrictive than "within the same barangay." The fallback looks for CR on the same street first, not any CR in the barangay.

**Algorithm:**
```rust
fn fallback_institutional_to_commercial(
    query: &PropertyQuery,
    barangay_records: &[ZonalRecord],
) -> Option<FallbackResult> {
    // Only applies to X (Institutional) classification
    if query.classification != ClassCode::X {
        return None;
    }

    // Step 1: Look for CR on the SAME STREET (DOF DO text: "same barangay and street")
    let same_street_cr: Vec<_> = barangay_records.iter()
        .filter(|r| r.classification == ClassCode::CR)
        .filter(|r| street_matches(&r.street_name, &query.street))
        .collect();

    if let Some(cr_record) = same_street_cr.first() {
        return Some(FallbackResult {
            record: cr_record.clone(),
            confidence: 0.70,
            fallback_level: FallbackLevel::InstitutionalCommercial,
            note: format!(
                "No Institutional (X) value found. Per DOF DO footnote: using nearest \
                 commercial (CR) value on same street within same barangay: ₱{}/sqm.",
                cr_record.zv
            ),
        });
    }

    // Step 2: If no CR on same street, try CR catch-all in the barangay
    // (slightly broader than DOF DO text — flagged as lower confidence)
    let catch_all_cr = find_catch_all_for_classification(
        barangay_records, ClassCode::CR
    );

    if let Some(cr_record) = catch_all_cr {
        return Some(FallbackResult {
            record: cr_record.clone(),
            confidence: 0.55,
            fallback_level: FallbackLevel::InstitutionalCommercial,
            note: format!(
                "No Institutional (X) value found on same street. Using barangay-level \
                 commercial (CR) catch-all: ₱{}/sqm. Note: DOF DO text specifies \
                 'within the same barangay AND street' — this is a broader fallback.",
                cr_record.zv
            ),
        });
    }

    // Step 3: No CR at all in barangay — agricultural-only barangay
    // (flagged in verification: purely agricultural barangays may lack CR)
    None
}
```

**Edge case — rural barangay without CR:**
The verification cross-check (§Claim 2) found that CR is present in all 31 sampled RDOs (100%) but this is NOT verified at the individual barangay level. Purely agricultural provincial barangays may have only A1-A50 classifications and no CR entry. In this case, the institutional fallback fails and the engine falls through to Level 5A/6.

**Worked Example 8 — Institutional Fallback:**
```
Input:
  City: Makati
  Barangay: San Lorenzo
  Street: Chino Roces Avenue
  Classification: X (school property)

Workbook: San Lorenzo has extensive CR data but no X entries.
  "CHINO ROCES AVE | MAKATI AVE - PASONG TAMO | CR | 180,000"

Result:
  Value: ₱180,000/sqm
  Fallback Level: 5 (Institutional → Commercial)
  Confidence: 0.70
  Note: "No Institutional (X) value found. Per DOF DO footnote: using nearest \
         commercial (CR) value on same street (CHINO ROCES AVE) within same \
         barangay (San Lorenzo): ₱180,000/sqm."
```

### 3.6 Level 5A: RAMO 2-91 LGU FMV Markup (NOT COMPUTED)

**Scenario:** No zonal value exists at all for the area — no street entries, no catch-all, no adjacent barangay with any matching classification. The entire area is a zonal data gap.

**Legal basis:** RAMO 2-91 (Revenue Administrative Memorandum Order No. 2-91, February 18, 1991), referenced by DOF DO footnotes: "IN THE ABSENCE OF ZONAL VALUATION, PROPERTY SHALL BE VALUED PURSUANT TO RAMO 2-91."

**RAMO 2-91 exact text (verified from SC E-Library):**
> "When the zonal value of land has NOT been established, there shall be added to the market value per latest tax declaration ONE HUNDRED PERCENT (100%) thereof. PROVIDED, that if the property is classified as commercial, industrial and agricultural devoted to fishpond/prawn farm, ONE HUNDRED FIFTY PERCENT (150%) shall be added thereto."

Translation:
- Residential/General: Tax Declaration FMV × 2.0 (FMV + 100%)
- Commercial/Industrial/Fishpond: Tax Declaration FMV × 2.5 (FMV + 150%)

**Critical discrepancy documented:** Respicio & Co. (2025) cites "LGU FMV plus 20%" as current RDO practice. No formal BIR issuance modifying the 100%/150% percentages was found. The 20% figure likely reflects informal operational practice at some RDOs where LGU tax declaration values have been updated closer to market values, making the 1991-era 100% markup excessive.

**Engine design decision:** The engine does NOT compute the RAMO 2-91 markup value. Per CTA rulings (Emiliano, Gamboa), generating a zonal value that does not exist in the published schedule crosses into territory where the BIR must follow Section 6(F) appraisal procedures. The engine returns an informational result only.

**Algorithm:**
```rust
fn fallback_ramo_291(
    classification: ClassCode,
) -> FallbackResult {
    let markup_type = if classification.is_commercial()
        || classification.is_industrial()
        || classification == ClassCode::A6  // Fishpond
    {
        "commercial/industrial/fishpond (RAMO 2-91: LGU FMV + 150%)"
    } else {
        "residential/general (RAMO 2-91: LGU FMV + 100%)"
    };

    FallbackResult {
        record: ZonalRecord::empty(),
        confidence: 0.0,  // No engine-computed value
        fallback_level: FallbackLevel::Ramo291,
        note: format!(
            "NO PUBLISHED ZONAL VALUE exists for this area.\n\
             Per DOF DO standard footnote: valued pursuant to RAMO 2-91.\n\
             Formula: Tax Declaration FMV + markup ({}).\n\
             NOTE: The engine does not compute this value. The RDO/ONETT examiner \
             will apply RAMO 2-91 during transaction processing.\n\
             NOTE: Some RDOs may apply a lower markup (~20%) as operational practice \
             (Respicio & Co., 2025), though RAMO 2-91 (100%/150%) is the formal rule.\n\
             Action: Submit documents to the RDO with jurisdiction over the property.",
            markup_type
        ),
    }
}
```

**When Level 5A applies:**
- Newly platted subdivisions in areas without prior zonal coverage
- Remote rural barangays that were never surveyed for zonal valuation
- Newly created barangays (e.g., post-2019 barangay splits) not yet covered
- BARMM municipalities with no published RDO assignment (8 identified in Wave 3 `rdo-jurisdiction-mapping`)

### 3.7 Level 6: No Match (NULL)

**Scenario:** All fallback levels have been exhausted. No value can be returned.

**Legal basis:** *Spouses Emiliano v. CIR* (CTA EB No. 1103, 2015): "CGT cannot be based on BIR's unilaterally adopted valuation absent a published zonal value; due process in fixing ZV is essential." *CIR v. Heirs of Gamboa* (CTA Case No. 9720, 2020): "BIR cannot simply adopt a bank's appraised value; must follow Section 6(F) appraisal procedures."

**Algorithm:**
```rust
fn no_match_result(query: &PropertyQuery) -> FallbackResult {
    FallbackResult {
        record: ZonalRecord::empty(),
        confidence: 0.0,
        fallback_level: FallbackLevel::NoMatch,
        note: format!(
            "NO PUBLISHED ZONAL VALUE found through any fallback level.\n\
             Per CTA rulings (Emiliano, CTA EB 1103, 2015; Gamboa, CTA 9720, 2020): \
             the BIR cannot substitute arbitrary valuations.\n\
             The applicable tax base will be determined by the RDO through:\n\
             1. Section 6(F) appraisal procedures, or\n\
             2. RAMO 2-91 (if the area lacks zonal coverage entirely), or\n\
             3. STCRPV → TCRPV → ECRPV escalation (per RMO 31-2019) for \
                boundary disputes or classification gaps.\n\
             Action: Submit a written inquiry to RDO {} ({}).",
            query.rdo_id, query.rdo_name
        ),
    }
}
```

---

## 4. Complete Fallback Decision Tree (Rust)

The full orchestration combining all 7 levels:

```rust
/// Fallback level enum with ordering
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FallbackLevel {
    ExactMatch,                // Level 1
    SameStreetDiffVicinity,    // Level 2
    BarangayCatchAll,          // Level 3
    AdjacentBarangay,          // Level 4
    InstitutionalCommercial,   // Level 5 (branch — X only)
    Ramo291,                   // Level 5A (informational only)
    NoMatch,                   // Level 6
}

/// Result of the fallback resolution
#[derive(Debug, Clone)]
pub struct FallbackResult {
    pub record: ZonalRecord,
    pub confidence: f64,         // 0.0 = no value, 1.0 = exact match
    pub fallback_level: FallbackLevel,
    pub note: String,
    pub value_is_computed: bool,  // false for Level 5A and 6
}

/// Main fallback resolution pipeline
pub fn resolve_with_full_fallback(
    query: &PropertyQuery,
    rdo_data: &RdoData,
) -> FallbackResult {
    let barangay_idx = match resolve_barangay(&query.barangay, &rdo_data.barangays) {
        Some(idx) => idx,
        None => {
            // Cannot even find the barangay — skip to RAMO 2-91 / NULL
            if rdo_data.has_any_data_for_municipality(&query.municipality) {
                return no_match_result(query);
            } else {
                return fallback_ramo_291(query.classification);
            }
        }
    };

    let barangay_records = rdo_data.get_barangay_records(barangay_idx);

    // === Level 1: Exact Match ===
    if let Some(result) = match_exact(query, &barangay_records) {
        return result;
    }

    // === Level 2: Same Street, Different Vicinity ===
    let street_records: Vec<_> = barangay_records.iter()
        .filter(|r| street_matches(&r.street_name, &query.street))
        .cloned()
        .collect();

    if !street_records.is_empty() {
        if let Some(result) = fallback_same_street(query, &street_records) {
            return result;
        }
    }

    // === Level 3: Barangay Catch-All ===
    if let Some(result) = fallback_barangay_catch_all(
        query.classification, &barangay_records
    ) {
        return result;
    }

    // === Level 5 (Branch): Institutional → Commercial ===
    // (Checked BEFORE Level 4 because the DOF DO text specifies
    //  "within the same barangay and street" — a same-barangay lookup)
    if query.classification == ClassCode::X {
        if let Some(result) = fallback_institutional_to_commercial(
            query, &barangay_records
        ) {
            return result;
        }
    }

    // === Level 4: Adjacent Barangay ===
    if let Some(result) = fallback_adjacent_barangay(
        barangay_idx, query.classification, rdo_data
    ) {
        return result;
    }

    // === Level 5A: RAMO 2-91 ===
    // Only if the area genuinely has no zonal data at all
    if barangay_records.is_empty() {
        return fallback_ramo_291(query.classification);
    }

    // === Level 6: NULL ===
    no_match_result(query)
}
```

**Ordering note on Levels 4 and 5:** The implementation checks Level 5 (institutional → commercial) BEFORE Level 4 (adjacent barangay) because:
1. The DOF DO text says "within the same barangay and street" — this is explicitly a same-barangay lookup
2. Institutional properties are typically in urban areas where the same barangay will have CR values
3. Adjacent barangay (Level 4) is a more aggressive fallback (lower confidence) and should be tried after same-barangay options are exhausted

This reordering from the original proposal is validated by the cross-check verification report.

---

## 5. Edge Cases and Special Handling

### 5.1 Condo Fallback Path

Condominiums follow a parallel fallback chain that differs at Levels 2 and 3:

```
Level 1: Exact building name + classification match
Level 2C: Same building, different classification (e.g., RC when user needs CC)
Level 3C: Condo catch-all ("ALL OTHER CONDOMINIUMS")
  → Cebu: storey-based split (≤7 vs ≥8, 44-78% premium)
  → Regular: generic catch-all
Level 4C: Adjacent barangay condos (same classification)
Level 6: NULL
```

**Note:** Level 5 (institutional → commercial) does NOT apply to condos. Condos are never X-classified. RAMO 2-91 (Level 5A) is also unlikely for condos — if a condo exists, the area has zonal coverage.

### 5.2 Parking Slot (PS) Fallback

When no PS value exists for a specific condo:
1. Check if the building has an explicit PS entry → use it (Level 1)
2. If no PS entry, apply the RDO-specific PS formula:
   - RDO 47 (East Makati): PS = 60% of parent (RC or CC)
   - RDO 44 (Taguig): PS = 70% of parent
   - RDO 41 (Mandaluyong): PS = 70% (residential), 100% (commercial)
3. These formulas are embedded in DOF DO footnotes (from `condo-table-structures.md`)

```rust
fn compute_parking_slot_fallback(
    parent_value: u32,
    parent_class: ClassCode,
    rdo_id: u8,
) -> Option<FallbackResult> {
    let ratio = match (rdo_id, parent_class) {
        (47, _) => 0.60,                          // East Makati: 60%
        (48, _) => 0.60,                          // West Makati: 60%
        (44, _) => 0.70,                          // Taguig: 70%
        (41, ClassCode::RC) => 0.70,              // Mandaluyong residential: 70%
        (41, ClassCode::CC) => 1.00,              // Mandaluyong commercial: 100%
        _ => 0.65,                                 // Default: 65% (conservative midpoint)
    };

    let ps_value = (parent_value as f64 * ratio) as u32;

    Some(FallbackResult {
        record: ZonalRecord { zv: ps_value, ..ZonalRecord::empty() },
        confidence: 0.85,
        fallback_level: FallbackLevel::ExactMatch, // PS formula IS part of the schedule
        note: format!(
            "PS value computed from {} parent (₱{}/sqm × {}% = ₱{}/sqm) \
             per DOF DO footnote for RDO {}.",
            parent_class, parent_value, (ratio * 100.0) as u32, ps_value, rdo_id
        ),
    })
}
```

### 5.3 Multi-Municipality Workbooks (Provincial)

In provincial RDOs, a single workbook covers multiple municipalities (up to 16 per workbook, from Wave 2 `sheet-organization.md`). Different municipalities within the same RDO may be on different current revisions.

**Fallback implications:**
- Level 4 (adjacent barangay) should stay within the same municipality first
- Cross-municipality fallback is a Level 4 extension but with lower confidence
- The NOTICE sheet determines the correct revision per municipality

```rust
fn adjacent_barangay_within_municipality(
    target_brgy_idx: usize,
    classification: ClassCode,
    rdo_data: &RdoData,
) -> Option<FallbackResult> {
    let target_municipality = rdo_data.barangays[target_brgy_idx].municipality_id;

    // Only search within the same municipality first
    let same_muni_neighbors: Vec<usize> = rdo_data.get_adjacent_barangays(target_brgy_idx)
        .filter(|&idx| rdo_data.barangays[idx].municipality_id == target_municipality)
        .collect();

    for neighbor_idx in same_muni_neighbors {
        if let Some(result) = search_barangay_for_classification(
            neighbor_idx, classification, rdo_data
        ) {
            return Some(result.with_confidence(0.55));
        }
    }

    // Cross-municipality fallback (lower confidence)
    let cross_muni_neighbors: Vec<usize> = rdo_data.get_adjacent_barangays(target_brgy_idx)
        .filter(|&idx| rdo_data.barangays[idx].municipality_id != target_municipality)
        .collect();

    for neighbor_idx in cross_muni_neighbors {
        if let Some(result) = search_barangay_for_classification(
            neighbor_idx, classification, rdo_data
        ) {
            return Some(result.with_confidence(0.40).with_note(
                "Cross-municipality fallback — value from a different municipality \
                 within the same RDO. Verify applicability."
            ));
        }
    }

    None
}
```

### 5.4 Empty/Deleted Catch-All Entries

From the Mandaluyong 2019 analysis: some barangays have "ALL OTHER STREETS" entries with **no recommended value** because all streets are individually enumerated. The engine must not return a ₱0 value.

```rust
fn is_valid_catch_all(record: &ZonalRecord) -> bool {
    record.zv > 0
        && !record.footnote_markers.contains(&FootnoteSemantic::Deleted)
        && !record.street_name.contains("NO VALUE RECOMMENDED")
}
```

### 5.5 Agricultural Minimum Area Threshold and Fallback

For GP (General Purpose) classification requiring ≥5,000 sqm:
- If property is < 5,000 sqm and user requests GP → reject classification, suggest RR
- If barangay has no GP entry → Level 3 catch-all unlikely (GP catch-alls are rare)
- Fall through to Level 4 → adjacent barangay GP

For Agricultural codes (A1-A50) with the operational 1,000 sqm threshold:
- The 1,000 sqm threshold is NOT formally codified (from `classification-resolution-logic.md` verification)
- Engine issues a soft warning but does NOT block the lookup (Aquafresh: published classification governs)

### 5.6 RPVARA Transition and Fallback

During the RPVARA transition (2024-2027+), the fallback hierarchy gains an additional branch:

```
Pre-transition: Standard 7-level fallback against BIR zonal values
Transition: Same 7-level fallback, BUT:
  - After Level 6 (NULL from BIR ZV): check if BLGF-approved SMV exists for the LGU
  - If yes: use SMV (different data source, same matching logic)
  - If no: return NULL (both sources exhausted)
Post-transition: Same 7-level fallback against BLGF SMVs (BIR ZVs deprecated)
```

The fallback hierarchy itself doesn't change — it's the **data source** that changes. The engine's fallback state machine is data-source-agnostic.

---

## 6. Confidence Scoring Integration

The fallback level directly determines the confidence score floor:

```rust
fn confidence_for_fallback(level: FallbackLevel, match_quality: f64) -> f64 {
    let level_ceiling = match level {
        FallbackLevel::ExactMatch => 1.0,
        FallbackLevel::SameStreetDiffVicinity => 0.80,
        FallbackLevel::BarangayCatchAll => 0.85,  // higher than Level 2 for single-match
        FallbackLevel::AdjacentBarangay => 0.65,
        FallbackLevel::InstitutionalCommercial => 0.70,
        FallbackLevel::Ramo291 => 0.0,   // no value computed
        FallbackLevel::NoMatch => 0.0,    // no value
    };

    // Overall confidence = min(match_quality, level_ceiling)
    f64::min(match_quality, level_ceiling)
}
```

**UI tier mapping (from `address-matching-algorithms.md` §12):**

| Confidence | UI Tier | Color | Action |
|-----------|---------|-------|--------|
| ≥ 0.85 | HIGH | Green | Direct use |
| 0.65–0.84 | MEDIUM | Yellow | Verify with RDO |
| 0.50–0.64 | LOW | Orange | Use with caution |
| < 0.50 | VERY LOW | Red | Manual verification required |
| 0.0 | NO MATCH | Gray | No value — consult RDO |

---

## 7. Worked Examples — Complete Pipeline

### Example A: Full pipeline — urban NCR, exact match found

```
Input: 123 Jupiter Street, Bel-Air, Makati City, Classification: RR
  → RDO 47 (East Makati)
  → Barangay: Bel-Air (exact)
  → Street: Jupiter Street (exact)
  → Classification: RR (exact)
  → Value: ₱100,000/sqm
  → Level 1, Confidence: 0.95
```

### Example B: Full pipeline — provincial, catch-all used

```
Input: Interior lot in Barangay Malued, Dagupan City, Pangasinan, Classification: RR
  → RDO 5 (Dagupan)
  → Barangay: Malued (exact)
  → Vicinity: "interior lot" → T6Interior
  → No T6Interior RR entry for Malued
  → Level 2: tier downgrade T6→T5→T4... → found T4 Barangay RR at ₱2,000
  → Confidence: 0.65
  OR
  → Level 3: "ALL OTHER LOTS | RR | 1,500" catch-all found
  → Confidence: 0.80

Engine returns Level 3 (higher confidence): ₱1,500/sqm
```

### Example C: Full pipeline — institutional fallback

```
Input: Church property on P. Burgos Street, San Lorenzo, Makati, Classification: X
  → RDO 49 (South Makati)
  → Barangay: San Lorenzo (exact)
  → Street: P. Burgos Street (exact match after normalization)
  → Classification: X → not found in San Lorenzo schedule
  → Level 3: no "ALL OTHER STREETS | X" catch-all
  → Level 5 (institutional branch):
    → Same street CR: "P. BURGOS ST | ... | CR | 250,000" found!
  → Value: ₱250,000/sqm (from CR)
  → Level 5, Confidence: 0.70
  → Note: "Per DOF DO footnote: using nearest CR value on same street."
```

### Example D: Full pipeline — NULL result

```
Input: Property in Barangay Lamitan, Basilan (BARMM)
  → RDO resolution: Basilan municipalities → no published RDO assignment
    (8 BARMM municipalities identified as coverage gap in rdo-jurisdiction-mapping)
  → Level 5A: RAMO 2-91 informational
  → Level 6: NULL
  → Note: "No published zonal value. BARMM coverage gap. Consult RDO."
  → Confidence: 0.0
```

### Example E: Full pipeline — adjacent barangay

```
Input: Property on Sampaguita Street, Barangay Pag-asa, QC, Classification: I
  → RDO 39 (Quezon City)
  → Barangay: Pag-asa (exact)
  → Pag-asa has RR, CR entries but no I (Industrial)
  → Level 3: no "ALL OTHER STREETS | I" catch-all
  → Level 5: N/A (not X classification)
  → Level 4: adjacent barangays (Bungad, Damayang Lagi)
    → Bungad has no I
    → Damayang Lagi has "ALL OTHER STREETS | I | 35,000"
  → Value: ₱35,000/sqm (from Damayang Lagi catch-all)
  → Level 4, Confidence: 0.55
  → Note: "No Industrial value in Pag-asa. Using adjacent Barangay Damayang Lagi."
```

---

## 8. Rust Type Definitions

```rust
/// Complete fallback state machine types
pub mod fallback {
    use super::*;

    /// Fallback level with branch discriminant
    #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
    pub enum FallbackLevel {
        /// Level 1: Exact match on street + vicinity + classification
        ExactMatch,
        /// Level 2: Same street, different vicinity segment (same classification)
        SameStreetDiffVicinity,
        /// Level 3: Barangay catch-all ("ALL OTHER STREETS/LOTS")
        BarangayCatchAll,
        /// Level 4: Adjacent barangay, same classification
        AdjacentBarangay,
        /// Level 5 (BRANCH): Institutional (X) → nearest CR, same barangay+street
        InstitutionalCommercial,
        /// Level 5A: RAMO 2-91 LGU FMV markup (informational only, no value computed)
        Ramo291,
        /// Level 6: No match — NULL
        NoMatch,
    }

    impl FallbackLevel {
        /// Whether the engine computes a value at this level
        pub fn computes_value(&self) -> bool {
            match self {
                Self::ExactMatch
                | Self::SameStreetDiffVicinity
                | Self::BarangayCatchAll
                | Self::AdjacentBarangay
                | Self::InstitutionalCommercial => true,
                Self::Ramo291 | Self::NoMatch => false,
            }
        }

        /// Maximum confidence ceiling for this level
        pub fn confidence_ceiling(&self) -> f64 {
            match self {
                Self::ExactMatch => 1.0,
                Self::SameStreetDiffVicinity => 0.80,
                Self::BarangayCatchAll => 0.85,
                Self::AdjacentBarangay => 0.65,
                Self::InstitutionalCommercial => 0.70,
                Self::Ramo291 => 0.0,
                Self::NoMatch => 0.0,
            }
        }

        /// Legal authority citation
        pub fn authority(&self) -> &'static str {
            match self {
                Self::ExactMatch => "Section 6(E) NIRC; RMC 115-2020",
                Self::SameStreetDiffVicinity =>
                    "DOF DO standard footnote Rule 3",
                Self::BarangayCatchAll =>
                    "DOF DO standard footnote Rule 3 (operationalized)",
                Self::AdjacentBarangay =>
                    "DOF DO standard footnotes Rules 1 & 2",
                Self::InstitutionalCommercial =>
                    "DOF DO standard footnote (X provision)",
                Self::Ramo291 =>
                    "RAMO 2-91 (Feb 18, 1991); DOF DO footnote reference",
                Self::NoMatch =>
                    "CTA Emiliano (EB 1103, 2015); CTA Gamboa (9720, 2020)",
            }
        }
    }

    /// The result of a fallback resolution
    #[derive(Debug, Clone)]
    pub struct FallbackResult {
        /// The matched record (empty if Level 5A/6)
        pub record: Option<ZonalRecord>,
        /// Confidence score [0.0, 1.0]
        pub confidence: f64,
        /// Which fallback level was used
        pub level: FallbackLevel,
        /// Human-readable explanation
        pub note: String,
        /// Source barangay (if different from query barangay)
        pub source_barangay: Option<String>,
        /// Whether the value is engine-computed (false for 5A, 6)
        pub value_is_computed: bool,
    }

    /// Adjacency model for barangay fallback
    #[derive(Debug, Clone)]
    pub struct BarangayAdjacency {
        /// Workbook-order adjacency (MVP)
        pub workbook_neighbors: HashMap<u16, Vec<u16>>,
        /// GIS-based adjacency (future upgrade)
        pub gis_neighbors: Option<HashMap<u16, Vec<u16>>>,
        /// Municipality boundaries (for provincial multi-municipality workbooks)
        pub municipality_boundaries: HashMap<u16, Vec<u16>>,
    }

    impl BarangayAdjacency {
        /// Get adjacent barangays, preferring GIS data if available
        pub fn get_neighbors(&self, brgy_id: u16) -> Vec<u16> {
            self.gis_neighbors
                .as_ref()
                .and_then(|gis| gis.get(&brgy_id))
                .or_else(|| self.workbook_neighbors.get(&brgy_id))
                .cloned()
                .unwrap_or_default()
        }

        /// Get neighbors within the same municipality only
        pub fn get_same_municipality_neighbors(
            &self,
            brgy_id: u16,
            municipality_id: u16,
        ) -> Vec<u16> {
            self.get_neighbors(brgy_id)
                .into_iter()
                .filter(|n| {
                    self.municipality_boundaries
                        .get(&municipality_id)
                        .map_or(true, |brgys| brgys.contains(n))
                })
                .collect()
        }
    }
}
```

---

## 9. Verification Summary

### Verification Protocol Compliance

Per Wave 3 rules: "Every Wave 3 resolution logic formalization MUST be cross-checked against at least 2 independent sources using a subagent."

**Two verification subagents were deployed:**

1. **`fallback-hierarchy-verification.md`** — 18+ sources consulted across legal databases, BIR issuances, CTA decisions, and practitioner commentaries. All 6 levels and 3 embedded workbook rules verified.

2. **`fallback-hierarchy-cross-check.md`** — Independent re-verification with DOF DO footnote text extraction. Identified authority attribution corrections and the RAMO 2-91 separate-level finding.

### Consolidated Verification Results

| Level | Verdict | Source Count | Key Finding |
|-------|---------|-------------|-------------|
| 1 (Exact Match) | **FULLY CONFIRMED** | 5 | Primary authority: Section 6(E) NIRC |
| 2 (Same Street) | **FULLY CONFIRMED** | 4 | Authority: DOF DO footnotes (corrected from RMO 31-2019) |
| 3 (Catch-All) | **FULLY CONFIRMED** | 5 | Catch-all may be empty in fully-enumerated barangays |
| 4 (Adjacent) | **FULLY CONFIRMED** | 4 | Authority: DOF DO footnotes Rules 1 & 2 |
| 5 (Institutional) | **CONFIRMED** | 3 | Scope: "same barangay **and street**" (more restrictive than original) |
| 5A (RAMO 2-91) | **CONFIRMED (formal); DISCREPANCY on 20%** | 4 | 100%/150% confirmed; 20% is single-source informal practice |
| 6 (NULL) | **FULLY CONFIRMED** | 4 | CTA Emiliano + Gamboa correctly cited |

**Remaining single-source items:**
1. LGU FMV + 20% markup (Respicio & Co. only — no formal issuance found)
2. "Nearest comparable zone" exact phrase (practitioner shorthand, not DOF DO language)
3. "Zonal Classification Ruling" as a named instrument (Respicio only; no formal BIR issuance)

---

## 10. Implications for Engine Architecture

### Design Principles Derived from Fallback Analysis

1. **Fallback is a state machine, not a linear chain.** Level 5 is a branch (X classification only). RAMO 2-91 (5A) is a parallel terminal. The implementation must use a decision tree, not a simple loop.

2. **Engine never generates values.** At Levels 5A and 6, the engine returns informational/advisory results only. This is a legal constraint (CTA rulings), not just a UX choice.

3. **Confidence scoring must compound match quality × fallback level.** A fuzzy street match (0.70) at Level 4 (ceiling 0.65) produces overall confidence 0.65 — the level caps the score.

4. **Adjacent barangay requires addressable adjacency data.** MVP: use workbook ordering. Future: GIS boundary polygons from PSA PSGC or OpenStreetMap.

5. **Provincial multi-municipality workbooks require municipality-scoped adjacency.** Adjacent barangay fallback must respect municipality boundaries first before crossing them.

6. **RPVARA doesn't change the fallback structure.** The same 7-level hierarchy applies regardless of whether the data comes from BIR zonal values or BLGF SMVs. The data source is abstracted away from the fallback logic.

### Data Requirements for Fallback

| Data | Source | Size | WASM Feasibility |
|------|--------|------|-----------------|
| Barangay adjacency (workbook-order) | Derived during ingestion | ~42K entries, ~200 KB | YES |
| Catch-all index | Pre-computed at ingestion | ~185 entries × 3 fields | YES |
| Municipality boundaries | PSGC / NOTICE sheet | ~1,700 LGUs × ~50 barangays avg | YES |
| PS formula table | DOF DO footnotes (hardcoded) | <50 entries | YES |
| GIS adjacency (future) | OpenStreetMap / PSA | ~42K × ~5 neighbors avg = ~210K edges | YES (~1.2 MB) |

---

## Legal Citations

| Citation | Relevance to Fallback |
|----------|----------------------|
| Section 6(E) NIRC, as amended by TRAIN (RA 10963) | Level 1: statutory authority for published zonal values |
| RMC 115-2020 | Level 1: published schedule is authoritative source |
| DOF DO standard footnotes (East Makati 2021, RDO 82 Cebu South, RDO 83 Talisay, 28+ workbooks) | Levels 2-5: all fallback rules derive from these regulatory footnotes |
| RAMO 2-91 (Feb 18, 1991) | Level 5A: LGU FMV + 100%/150% formula |
| CIR v. Aquafresh Seafoods (G.R. No. 170389, SC 2010) | Published classification prevails; engine uses schedule, not "actual use" |
| Spouses Emiliano v. CIR (CTA EB No. 1103, 2015) | Level 6: BIR cannot substitute valuations absent published ZV |
| CIR v. Heirs of Gamboa (CTA Case No. 9720, 2020) | Level 6: bank appraisals are not a valid substitute |
| RMO 31-2019 | Committee structure (STCRPV/TCRPV/ECRPV) for escalation |
| DOF Local Assessment Regulations No. 1-92 | Predominant use rule — pre-baked into schedule, not runtime |

---

## Sources

### Primary Legal/Regulatory
- [Section 6(E) NIRC](https://www.bir.gov.ph/index.php/tax-code.html)
- [RAMO 2-91 — SC E-Library](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/49658)
- [CIR v. Aquafresh Seafoods, G.R. 170389 — LawPhil](https://lawphil.net/judjuris/juri2010/oct2010/gr_170389_2010.html)
- [RMO 31-2019 — BLGF PDF](https://blgf.gov.ph/wp-content/uploads/2015/09/BIR-RMO_No.-31-2019-SMV.pdf)
- [RMC 115-2020 — BIR CDN](https://bir-cdn.bir.gov.ph/local/pdf/RMC%20No.%20115-2020.pdf)

### DOF Department Orders (Fallback Rules Source)
- [DOF DO — East Makati 2021 (7th Revision)](https://carlacalleja.com/2022/01/03/bir-zonal-value-east-makati-2021/)
- [DOF DO — RDO 82 Cebu City South](http://macrealtyservices.com/wp-content/uploads/2014/07/RDO82-CebuCTSouth.pdf)
- [DOF DO — RDO 83 Talisay/Minglanilla](http://macrealtyservices.com/wp-content/uploads/2014/07/RDO-83-Talisay-CT-Minglanilla.pdf)
- [DOF DO — RDO 93B Zamboanga Sibugay](https://bir-cdn.bir.gov.ph/BIR/pdf/RDO%20NO.%2093B%20-ZAMBOANGA%20SIBUGAY.pdf)

### Practitioner/Legal Commentary
- [Respicio & Co. — Capital Gains Tax Based on ZV](https://www.lawyer-philippines.com/articles/capital-gains-tax-based-on-zonal-value-philippines)
- [Respicio & Co. — Basis for Zonal Valuation](https://www.respicio.ph/commentaries/basis-for-zonal-valuation-of-properties-in-the-philippines)
- [Grant Thornton PH — Certificate of Zonal Values](https://www.grantthornton.com.ph/insights/articles-and-updates1/tax-notes/issuance-of-certificate-of-zonal-values-of-real-properties/)

### Internal Analysis References
- `analysis/address-matching-algorithms.md` — §10 Fallback Hierarchy (5-level chain), §12 Confidence Scoring
- `analysis/classification-resolution-logic.md` — §4 Edge Cases (institutional, agricultural, CCT/TCT)
- `analysis/cta-zonal-rulings.md` — Categories 1-2 (classification disputes, missing ZV)
- `analysis/rmo-31-2019-annexes.md` — §Fallback Rules (3 embedded workbook rules)
- `analysis/condo-table-structures.md` — PS formula variations, Cebu storey-based catch-all
- `analysis/rdo-jurisdiction-mapping.md` — BARMM coverage gaps, multi-RDO cities
- `analysis/fallback-hierarchy-verification.md` — First verification pass (18+ sources)
- `analysis/fallback-hierarchy-cross-check.md` — Second verification pass with corrections
