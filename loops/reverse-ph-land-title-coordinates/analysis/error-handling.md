# Error Handling — Philippine Land Title Coordinate Engine

**Aspect:** error-handling (Wave 3)
**Date:** 2026-02-26
**Depends on:** text-parser-grammar (W2), traverse-algorithm (W2), prs92-to-wgs84-transform (W2), luzon1911-to-prs92-transform (W2), bllm-dataset-compilation (W2), validation-rules (W2), format-variations (W3)

---

## 1. Overview

This document specifies the engine's error handling strategy across every pipeline stage. It catalogs all known error conditions, defines severity levels, specifies recovery strategies where possible, and establishes the output contract for errors. The design principle: **fail gracefully, report precisely, never silently corrupt**.

### Pipeline Stages

```
[1. Input]     → raw TD text + optional metadata
[2. Parse]     → structured fields (tie point, bearings, distances, area)
[3. BLLM]      → resolve monument coordinates
[4. Traverse]  → compute PRS92 corner coordinates
[5. Validate]  → closure, area, geometry checks
[6. Transform] → PRS92 → WGS84 (or Luzon 1911 → PRS92 → WGS84)
[7. Output]    → WGS84 lat/lng + validation report
```

Each stage can produce errors that block downstream stages or warnings that allow computation to continue with reduced confidence.

---

## 2. Error Severity Levels

| Level | Symbol | Meaning | Pipeline Effect |
|-------|--------|---------|-----------------|
| **FATAL** | `E` | Computation cannot proceed | Stop pipeline; return partial results up to failure point |
| **ERROR** | `E` | Stage output is unreliable but pipeline can attempt to continue | Continue with caveat; flag overall result as `fail` |
| **WARNING** | `W` | Possible issue; output likely usable | Continue; flag as `warn` |
| **INFO** | `I` | Non-standard input handled successfully | Continue; no quality impact |

### Severity escalation rule

When multiple errors accumulate in a single TD:
- 3+ WARNINGs → overall status escalated to `warn`
- 1+ ERROR → overall status = `fail` unless all errors have recovery applied
- 1+ FATAL → overall status = `fatal`; pipeline halts at that stage

---

## 3. Stage 1 — Input Errors

These are errors in the raw input before any parsing begins.

### 3.1 Empty or Null Input

| Code | Severity | Condition | Recovery |
|------|----------|-----------|----------|
| `InputEmpty` | FATAL | TD text is empty string or null | None — return immediately |
| `InputTooShort` | WARNING | TD text < 50 characters | Attempt parse; likely to produce `TieBlockNotFound` downstream |

### 3.2 Encoding Issues

| Code | Severity | Condition | Recovery |
|------|----------|-----------|----------|
| `EncodingNonUTF8` | WARNING | Text contains non-UTF8 bytes | Attempt decode as latin-1; replace undecodable bytes with `?`; log original hex |
| `ControlCharacters` | INFO | Text contains control characters (tab, form feed, etc.) | Strip; normalize to spaces |

### 3.3 Pre-Processing Normalization

The engine normalizes input before parsing. These are always applied and never produce errors:

1. Collapse multiple whitespace (spaces, tabs, newlines) to single space
2. Normalize Unicode quotes (curly → straight: `\u201C`/`\u201D` → `"`, `\u2018`/`\u2019` → `'`)
3. Normalize Unicode degree/minute/second marks (`\u00B0` → °, `\u2032` → ′, `\u2033` → ″)
4. Strip leading/trailing whitespace
5. Normalize en-dash/em-dash to hyphen in plan numbers (but preserve in date ranges)

---

## 4. Stage 2 — Parse Errors

Parse errors arise when the text structure deviates from the expected grammar. The parser is designed to extract as much as possible even from degraded input.

### 4.1 Tie Block Errors

| Code | Severity | Condition | Recovery | Source |
|------|----------|-----------|----------|--------|
| `TieBlockNotFound` | FATAL* | No "Beginning at a point" pattern found | Check for coordinate-based TD format (COORD_CORNER_RE). If found → switch to coordinate pipeline. If not → floating parcel: compute relative polygon only | W2 grammar; W3 format-variations §8 |
| `TieDistanceMissing` | ERROR | Tie point named but distance absent (e.g., "being N. 45° 30' E. from BLLM No. 1") | Cannot compute Corner 1 absolute position. Compute relative polygon from first traverse leg. Output `tie_point.status = "distance_missing"` | W3 format-variations §5 |
| `TieMonumentUnparseable` | ERROR | Monument reference text present but does not match any MONUMENT_RE pattern | Return raw text in `tie_point.raw_name`; attempt fuzzy string match in BLLM database using trigram similarity | New |

*`TieBlockNotFound` is FATAL for the standard pipeline but triggers an alternate code path for coordinate-based TDs.

### 4.2 Bearing Errors

| Code | Severity | Condition | Recovery | Source |
|------|----------|-----------|----------|--------|
| `BearingMissingPrefix` | WARNING | No N/S before degrees (e.g., "50 deg. 50' E.") | Attempt both N and S; if context suggests one (tie bearing → common quadrant patterns), use it with warning. Otherwise flag both options for caller | W2 grammar; Sample 4 |
| `BearingMissingSuffix` | WARNING | No E/W after minutes (e.g., "N. 22 deg. 40'") | Attempt both E and W; if the subsequent leg's starting direction provides context, use it. Otherwise flag both options | W2 grammar; Sample 4 |
| `BearingUnparseable` | ERROR | Neither quadrant prefix nor suffix, and not a Due-cardinal | Skip this leg. If it's a polygon leg, the resulting polygon will have a gap (detected by `MissingCorners`). Return raw text in warnings | W2 grammar |
| `BearingOutOfRange` | WARNING | Degrees > 90 for a quadrant bearing (e.g., "N. 120° 30' E.") | Possible azimuth stated directly (not quadrant). Attempt reinterpretation: if 90 < deg ≤ 180, treat as direct azimuth. If > 180, flag as `BearingUnparseable` | W2 grammar; W2 validation-rules §5.2 |
| `BearingSecondsDetected` | INFO | Bearing includes seconds (e.g., "N 35° 44' 24" W") | Include seconds in azimuth calculation: az = deg + min/60 + sec/3600. Log that this is non-standard for PH TDs | W2 traverse-algorithm §2 |
| `DueCardinalAmbiguous` | WARNING | "North" or "South" without "Due" prefix in bearing position | Check context: if it follows "thence" and precedes a distance, interpret as Due-cardinal. Otherwise flag | W2 grammar |

#### Bearing recovery algorithm

For `BearingMissingPrefix` and `BearingMissingSuffix`, the engine attempts smart recovery:

```python
def recover_bearing(raw_text: str, leg_index: int, context: dict) -> dict:
    """
    Attempt to recover a bearing with missing prefix or suffix.

    context contains:
        prev_bearing: previous leg's bearing (if any)
        next_bearing: next leg's bearing (if any, for look-ahead)
        polygon_winding: expected winding direction (CW for PH convention)

    Returns: {bearing: dict, confidence: str, alternatives: list[dict]}
    """
    # Strategy 1: If only prefix (N/S) is missing, try both
    # and pick the one that keeps the polygon non-self-intersecting
    candidates = []
    for prefix in ['N', 'S']:
        b = parse_bearing_with_override(raw_text, ns=prefix)
        if b:
            candidates.append(b)

    # Strategy 2: If only suffix (E/W) is missing, try both
    for suffix in ['E', 'W']:
        b = parse_bearing_with_override(raw_text, ew=suffix)
        if b:
            candidates.append(b)

    if len(candidates) == 1:
        return {"bearing": candidates[0], "confidence": "recovered", "alternatives": []}
    elif len(candidates) > 1:
        # Heuristic: pick candidate that minimizes closure error
        # (requires forward-computing remaining traverse — expensive)
        # Simpler: pick candidate that preserves polygon winding
        return {"bearing": candidates[0], "confidence": "ambiguous",
                "alternatives": candidates[1:]}
    return {"bearing": None, "confidence": "failed", "alternatives": []}
```

### 4.3 Distance Errors

| Code | Severity | Condition | Recovery | Source |
|------|----------|-----------|----------|--------|
| `DistanceZero` | ERROR | Parsed distance = 0.0 m | Skip leg. Flag corner as collapsed (two corners at same point). Proceed with remaining legs | W2 validation-rules §5.3 |
| `DistanceMissing` | ERROR | No distance found after bearing | Skip leg. Flag as `MissingCorners` downstream | New |
| `DistanceUnreasonable` | WARNING | Distance > 50,000 m (50 km) | Likely parse error (e.g., thousands comma misinterpreted). Log but proceed; traverse will likely fail closure | New |
| `DistanceNegative` | ERROR | Parsed distance < 0 (shouldn't happen with regex, but defensive check) | Take absolute value; warn | W2 validation-rules §5.3 |
| `DistanceDecimalComma` | INFO | Comma used as decimal separator (e.g., "936,15 m.") | Automatically converted via `.replace(',', '.')` per TitlePlotterPH pattern | W2 grammar §3 |

### 4.4 Traverse Structure Errors

| Code | Severity | Condition | Recovery | Source |
|------|----------|-----------|----------|--------|
| `MissingClosingLeg` | ERROR | No leg destination contains "point of beginning" | Last leg may still close geometrically. Compute closure error from last computed corner to Corner 1. If closure is within tolerance, treat last leg as closing | W2 grammar §4 |
| `MissingCorners` | WARNING | Gap in sequential corner numbering (e.g., point 3 → point 7) | The parser already extracts legs by regex, not by corner numbering. Corner numbers are metadata. This warning is informational: the traverse computation uses all extracted legs in order regardless of numbering gaps | W3 format-variations §5 |
| `DuplicateCorner` | WARNING | Same corner number appears twice with different bearing/distance | Use first occurrence; report second in warnings. If bearings differ significantly (> 5°), escalate to ERROR | W3 format-variations §5 |
| `NoLegsFound` | FATAL | Regex found zero traverse legs in the text | Cannot compute polygon. Return parse result with empty legs array | New |
| `SingleLeg` | ERROR | Only 1 traverse leg found (minimum 3 needed for a polygon) | Cannot form polygon. Return the single leg as a line segment if tie point available | New |
| `TwoLegs` | ERROR | Only 2 legs found (degenerate polygon) | Cannot form area polygon. Return as line segments | New |

### 4.5 Area Statement Errors

| Code | Severity | Condition | Recovery | Source |
|------|----------|-----------|----------|--------|
| `AreaNotFound` | WARNING | No area statement matched by either regex | Skip area cross-check validation. Traverse computation still proceeds; computed area reported without comparison | W2 grammar §7 |
| `AreaWordsNumMismatch` | WARNING | Words-spelled-out area and numeral-in-parentheses disagree | Use numeral (more reliable — words may have OCR/transcription errors). Log discrepancy | New |
| `AreaZero` | ERROR | Parsed area = 0 | Flag as parse error; skip area cross-check | New |

### 4.6 Footer/Metadata Errors

| Code | Severity | Condition | Recovery | Source |
|------|----------|-----------|----------|--------|
| `FooterNotFound` | WARNING | No footer (bearing type, survey date) detected | Default bearing_type to "grid" (most common). Default datum to caller-provided or auto-detect from era heuristics | W2 grammar §8 |
| `BearingTypeUnknown` | WARNING | Footer present but bearing type is neither "true" nor "grid" | Default to "grid" with warning | W2 grammar §8 |
| `SurveyDateUnparseable` | INFO | Survey date text present but cannot be parsed to year | Datum auto-detection cannot use era heuristic; relies on other signals | W2 luzon1911-to-prs92-transform §1 |
| `SurveyPlanUnparseable` | INFO | Plan number text present but does not match SURVEY_PLAN_RE | Return raw text; zone/region inference from plan number unavailable | W2 grammar §9 |

---

## 5. Stage 3 — BLLM Resolution Errors

These errors arise when looking up the tie point monument in the BLLM database.

| Code | Severity | Condition | Recovery | Source |
|------|----------|-----------|----------|--------|
| `BLLMNotFound` | FATAL* | Monument name not found after 3-tier lookup (exact → province → municipality) | Cannot determine absolute position. Two options: (1) caller provides coordinates, (2) compute relative polygon | W2 grammar §1; W2 bllm-dataset-compilation §lookup |
| `AmbiguousBLLM` | ERROR | Multiple records match after all filters applied | Return all candidates with coordinates. Let caller select. If only 2 candidates and they're within 50m of each other, use centroid with warning | W2 grammar §1; W2 bllm-dataset-compilation §lookup |
| `BLLMDatumMismatch` | WARNING | BLLM datum (from dataset) ≠ inferred title datum | If BLLM is Luzon 1911 and title is PRS92: use BLLM as-is (shift ~7-13m on grid, within BLLM coordinate uncertainty). Document the mismatch. If reversed: same approach | W2 luzon1911-to-prs92-transform §BLLM handling |
| `BLLMCoordinateInvalid` | ERROR | BLLM record has non-numeric or obviously wrong coordinates (e.g., Northing = " ") | Skip record; try next match or return `BLLMNotFound` | W2 bllm-dataset-compilation §1.2 |
| `BLLMZoneInferFailed` | ERROR | Province not found in province→zone mapping table | Cannot assign PTM zone to BLLM coordinates. Require caller to provide zone explicitly | W2 bllm-dataset-compilation §2 |
| `BLLMMonumentTypeUnsupported` | WARNING | Monument type (e.g., L.W., MBM) found in text but type is not in tiepoints.json | Return `BLLMNotFound`; recommend caller-provided coordinates. Log that non-BLLM monument types have limited database coverage | W2 grammar §1 |

*`BLLMNotFound` is FATAL for absolute positioning but allows relative polygon computation.

### BLLM fuzzy matching strategy

When exact match fails, the engine applies progressively relaxed matching:

```
Tier 1: Exact normalized name match
  "BLLM NO. 1, PLS-1110" → exact string match in Name field

Tier 2: Monument code + number only (drop descriptor)
  "BLLM NO. 1" → match across all records with BLLM 1

Tier 3: Monument code + number + province filter
  "BLLM 1" in province "ILOCOS SUR" → match BLLM 1 records in Ilocos Sur

Tier 4: Trigram similarity (threshold ≥ 0.6)
  Handles typos: "BLM 1" → "BLLM 1" (similarity 0.75)
  "BLLM NO. 1, PLS-110" → "BLLM NO. 1, PLS-1110" (similarity 0.95)

Tier 5: Caller-provided coordinates (external API input)
  Bypass database entirely; accept (N, E, zone, datum) from caller
```

---

## 6. Stage 4 — Traverse Computation Errors

These errors occur during the mathematical computation of corner coordinates.

| Code | Severity | Condition | Recovery | Source |
|------|----------|-----------|----------|--------|
| `TraverseOverflow` | FATAL | Computed coordinate exceeds valid PRS92 range (N: 0–2,500,000 m; E: 0–1,000,000 m) | Stop computation. Likely a bearing or distance parse error accumulated over many legs. Report last valid corner and offending leg index | New |
| `ClosureFail` | ERROR | Linear closure precision < 1:1,000 | Compute and return all corners, but flag overall result as unreliable. Include misclosure vector (eN, eE) so caller can assess | W2 validation-rules §2 |
| `ClosureWarn` | WARNING | Closure precision between 1:3,000 and 1:5,000 | Normal for older/rural surveys. Proceed with quality note | W2 validation-rules §2 |
| `AreaDiscrepancyFail` | ERROR | Computed area differs from stated area by > 5% | Likely a parsing error (missing leg, wrong bearing quadrant). Return both areas and discrepancy % | W2 validation-rules §3 |
| `SelfIntersection` | ERROR | Polygon edges cross (non-adjacent edges intersect) | Compute and return coordinates, but flag polygon as invalid. Most common cause: wrong quadrant in one bearing | W2 validation-rules §5.5 |
| `DegeneratePolygon` | ERROR | All corners are collinear (zero area polygon) | Return corners but no area. Likely data error | New |

### Traverse error diagnostics

When closure fails (k < 1,000), the engine should provide diagnostic hints:

```python
def diagnose_closure_failure(eN: float, eE: float, legs: list) -> list[str]:
    """Suggest probable causes of large misclosure."""
    hints = []

    # Hint 1: Large single-direction error suggests quadrant flip
    e = math.sqrt(eN**2 + eE**2)
    if abs(eN) > 0.8 * e:
        hints.append("Misclosure is predominantly N/S — check for N↔S quadrant error in a bearing")
    if abs(eE) > 0.8 * e:
        hints.append("Misclosure is predominantly E/W — check for E↔W quadrant error in a bearing")

    # Hint 2: Misclosure ≈ 2× a single leg's delta suggests one leg traversed wrong direction
    for i, leg in enumerate(legs):
        az_rad = math.radians(leg["azimuth_deg"])
        dN = leg["distance_m"] * math.cos(az_rad)
        dE = leg["distance_m"] * math.sin(az_rad)
        # If flipping this leg's sign would improve closure:
        residual_N = eN + 2 * dN  # removing leg's contribution and adding reverse
        residual_E = eE + 2 * dE
        residual = math.sqrt(residual_N**2 + residual_E**2)
        if residual < 0.1 * e:
            hints.append(f"Flipping leg {i+1} (bearing {leg.get('raw', '?')}) dramatically improves closure — possible quadrant error")

    # Hint 3: Misclosure roughly equals a distance in the leg table
    for i, leg in enumerate(legs):
        if abs(e - leg["distance_m"]) < 0.1 * e:
            hints.append(f"Misclosure ≈ leg {i+1} distance ({leg['distance_m']} m) — possible duplicate or missing leg")

    return hints
```

---

## 7. Stage 5 — Validation Errors

Validation errors are already fully specified in `analysis/validation-rules.md`. This section documents only the error *handling* behavior — what happens when a validation check fails.

### Validation failure matrix

| Check | PASS → | WARN → | FLAG → | FAIL → |
|-------|--------|--------|--------|--------|
| Linear closure | Proceed | Proceed; add warning | Proceed; add quality caveat | Output coords with `reliability: "low"` |
| Area cross-check | Proceed | Proceed; add warning | Proceed; suggest re-check parse | Add error to output |
| Angular closure | Proceed | Proceed | Investigate bearing parse | Add error; suggest quadrant check |
| Geometry sanity | Proceed | Proceed | — | Block output if self-intersecting |
| BLLM confidence | Proceed | Proceed | Proceed with caveat | Block: no absolute coords |
| Datum consistency | Proceed | Proceed | — | Block datum transform |

### Validation does not block traverse

All validation checks run *after* the traverse is complete. Even FAIL-level validation results do not prevent the engine from returning corner coordinates — they add metadata indicating unreliability. The single exception: `BLLMNotFound` prevents absolute coordinate computation (no tie point = no absolute position).

---

## 8. Stage 6 — Datum Transformation Errors

| Code | Severity | Condition | Recovery | Source |
|------|----------|-----------|----------|--------|
| `DatumAmbiguous` | WARNING | Survey date 1993–2005 and no explicit datum label | Default to PRS92 per detection algorithm. Add warning: "Datum assumed PRS92 for transition-era survey (1993–2005). Verify from plan metadata." | W2 luzon1911-to-prs92-transform §1.3 |
| `ZoneUnknown` | ERROR | Cannot determine PRS92/PTM zone from any source (province, plan number, caller input) | Cannot perform inverse Transverse Mercator projection. Return grid coordinates (N, E) without WGS84 conversion. Tag as `zone_unknown` | W2 prs92-datum-parameters; W2 bllm-dataset-compilation §2 |
| `ZoneBoundaryAmbiguous` | WARNING | Province straddles two zones (e.g., Isabela: some municipalities in Zone III, others in Zone IV) | Require municipality-level resolution. If municipality unknown, return both possible WGS84 results | W2 bllm-dataset-compilation §2.3 |
| `HelmertParamConflict` | ERROR | (Theoretical) Helmert parameters from different sources disagree beyond tolerance | Use EPSG:15708 (canonical). Log conflict with source citations | W2 prs92-to-wgs84-transform §Helmert |
| `Luzon1911PathBFailed` | WARNING | Caller provided DENR MC 2010-06 conformal parameters but they produce unreasonable shift (> 100m) | Fall back to Path A (3-param global). Log: "DENR MC 2010-06 parameters produced unreasonable result; using EPSG:1161/1162 global transform" | W2 luzon1911-to-prs92-transform §Path B |
| `EllipsoidalHeightMissing` | INFO | No ellipsoidal height provided (default h=0) | Standard for 2D land survey work. Use h=0; the resulting horizontal error from ignoring geoidal undulation is < 0.1 mm for the Helmert rotation at PH latitudes | W2 prs92-to-wgs84-transform §h=0 |
| `InverseTMConvergenceFail` | FATAL | Inverse Transverse Mercator iteration does not converge after 20 iterations | Extremely unlikely for valid PRS92 grid coordinates. If hit: coordinates are outside the valid projection zone range | New |

### Zone determination cascade

When the zone is not directly known, the engine attempts these sources in order:

```
1. Caller-provided zone → use directly
2. BLLM database record → inferred zone from province
3. TD location clause → parse province name → province-zone lookup
4. Survey plan region code → region-zone mapping (approximate — not 1:1)
5. Easting value → if >> 600,000 or << 400,000, flag as out-of-zone
6. Give up → ZoneUnknown error
```

---

## 9. Stage 7 — Output Assembly Errors

| Code | Severity | Condition | Recovery |
|------|----------|-----------|----------|
| `PartialResult` | INFO | Some pipeline stages succeeded but not all | Return all successful results; null out missing fields; set `overall_status` to the worst severity |
| `CoordinateClampWarning` | WARNING | WGS84 latitude outside 4°–21°N or longitude outside 116°–128°E (Philippine bounds) | Coordinates are technically valid but outside expected PH territory. Likely a zone error or BLLM coordinate error | New |

---

## 10. Typographical Error Detection and Recovery

Typographical errors in TDs are the most common real-world failure mode, especially in reconstituted titles, OCR'd documents, and court filings. This section catalogs specific typo patterns and recovery strategies.

### 10.1 Common Bearing Typos

| Typo Pattern | Example | Detection | Recovery |
|-------------|---------|-----------|----------|
| N↔S swap | "N. 10° 42' W." should be "S. 10° 42' W." | Large closure error predominantly in N/S direction; diagnostic hint identifies the offending leg | Suggest flipped bearing; do NOT auto-correct |
| E↔W swap | "S. 69° 49' W." should be "S. 69° 49' E." | Large closure error predominantly in E/W direction | Suggest flipped bearing |
| Missing prefix | "50 deg. 50' E." | `BearingMissingPrefix` detected at parse time | Offer N/S alternatives with closure impact |
| Missing suffix | "N. 22 deg. 40'" | `BearingMissingSuffix` detected at parse time | Offer E/W alternatives |
| Transposed digits | "N. 76° 42' W." should be "N. 77° 42' W." | Hard to detect automatically; results in small closure degradation | Not recoverable without external reference |
| Degree-minute swap | "N. 42° 77' W." (minutes > 59) | Minutes value > 59 is syntactically invalid | Flag as `BearingMinutesOutOfRange`; attempt to swap deg↔min |

### 10.2 Common Distance Typos

| Typo Pattern | Example | Detection | Recovery |
|-------------|---------|-----------|----------|
| Missing decimal | "3429 m." should be "342.9 m." or "34.29 m." | Closure fails; distance is 10× or 100× expected | Suggest decimal insertions; compare with area-implied perimeter |
| Extra digit | "1641 m." should be "16.41 m." | Same as above | Same |
| Swapped digits | "16.41 m." as "16.14 m." | Small closure degradation | Not auto-detectable |
| Comma vs decimal | "936,15 m." | Handled automatically by `.replace(',', '.')` | No error |

### 10.3 Structural Typos

| Typo Pattern | Example | Detection | Recovery |
|-------------|---------|-----------|----------|
| Merged legs | "thence N. 77° 42' W., 16.41 m. to point 2 thence N. 10° 27' E." (missing semicolon) | LEG_RE findall still extracts both legs — semicolons are optional separators | No error; handled by regex design |
| Missing "thence" | "to point 2; N. 10° 27' E., 30.59 m." | LEG_RE handles optional "thence" | No error |
| Truncated TD | TD ends mid-sentence (e.g., "thence S. 69° 49' E., 16.7") | `MissingClosingLeg` detected; last leg has no destination | Parse what's available; report as truncated |
| Repeated leg | Same bearing/distance appears twice consecutively | `DuplicateCorner` detected | Use first occurrence |
| "Point of beginning" variant | "to the starting point" instead of "to the point of beginning" | `MissingClosingLeg` if CLOSING_RE doesn't match | Add common variants to CLOSING_RE |

### 10.4 Closing phrase variants (extend CLOSING_RE)

The parser should recognize these additional closing phrases:

```python
CLOSING_PHRASES_EXTENDED = [
    r'to\s+the\s+point\s+of\s+beginning',
    r'to\s+point\s+of\s+beginning',
    r'to\s+point\s+\d+\s*,?\s*point\s+of\s+beginning',
    r'to\s+the\s+starting\s+point',               # variant
    r'to\s+point\s+1\s*$',                         # implicit close to point 1
    r'to\s+point\s+["\'"]?1["\'"]?\s*$',           # quoted "1"
    r'to\s+the\s+place\s+of\s+beginning',          # archaic variant
]
```

---

## 11. "Impossible State" Scenarios

These are scenarios where the input is technically valid but the geometry is physically impossible or the data is internally contradictory.

### 11.1 Impossible Bearings

| Condition | Detection | Handling |
|-----------|-----------|---------|
| Quadrant bearing angle > 90° | `BearingOutOfRange` at parse time | If ≤ 180°: reinterpret as azimuth. If > 180°: flag as error |
| Minutes > 59 | `BearingMinutesOutOfRange` at parse time | Flag; attempt degree↔minute swap recovery |
| Consecutive bearings identical | Two legs with same bearing + different distances | WARNING: unusual but valid (straight boundary segment). Not an error |
| All bearings in same quadrant | All bearings NE, for example | WARNING: unusual — most lots have bearings in multiple quadrants. May indicate systematic parse error |

### 11.2 Impossible Geometry

| Condition | Detection | Handling |
|-----------|-----------|---------|
| Self-intersecting polygon | O(n²) edge intersection test (validation stage) | ERROR: polygon is topologically invalid. Return coordinates but flag. Common cause: one bearing's quadrant is wrong |
| Zero-area polygon | Shoelace formula returns 0 (or near-zero relative to perimeter²) | ERROR: all corners are collinear. Likely missing a bearing component |
| Enormous lot | Computed area > 1,000 hectares (10 km²) | WARNING: valid in principle (large agricultural/forest lands exist) but unusual. Check for distance parse errors |
| Tiny lot | Computed area < 1 sq m | WARNING: possible distance unit error (meters vs centimeters) or missing decimal |

---

## 12. Error Accumulation and Confidence Scoring

### 12.1 Error Accumulation Model

Each TD processed accumulates a list of errors/warnings. The engine computes an overall confidence score:

```python
def compute_confidence(errors: list[dict]) -> dict:
    """
    Compute overall confidence from accumulated errors.

    Returns: {
        confidence: "high" | "medium" | "low" | "unusable",
        score: float (0.0–1.0),
        reasons: list[str]
    }
    """
    score = 1.0
    reasons = []

    for err in errors:
        if err["severity"] == "FATAL":
            return {"confidence": "unusable", "score": 0.0,
                    "reasons": [err["message"]]}
        elif err["severity"] == "ERROR":
            score -= 0.3
            reasons.append(err["message"])
        elif err["severity"] == "WARNING":
            score -= 0.1
            reasons.append(err["message"])
        # INFO does not reduce score

    score = max(0.0, score)

    if score >= 0.8:
        confidence = "high"
    elif score >= 0.5:
        confidence = "medium"
    elif score >= 0.2:
        confidence = "low"
    else:
        confidence = "unusable"

    return {"confidence": confidence, "score": round(score, 2), "reasons": reasons}
```

### 12.2 Source Quality Heuristics

Beyond individual errors, the engine infers overall source quality:

| Signal | Quality Inference |
|--------|------------------|
| 0 errors, 0 warnings | `source_quality: "clean"` |
| 1-2 warnings only | `source_quality: "good"` — standard rounding artifacts |
| 3+ warnings or 1 error | `source_quality: "degraded"` — possible reconstituted title or OCR artifact |
| 2+ errors | `source_quality: "poor"` — likely significant transcription damage |
| `TieDistanceMissing` or `BearingMissingPrefix` | `source_quality: "reconstituted_likely"` — these patterns are characteristic of titles reconstructed from secondary sources |

---

## 13. Error Output Schema

Every engine response includes an `errors` array with uniform structure:

```json
{
  "result": {
    "corners_wgs84": [...],
    "corners_prs92": [...],
    "validation": {...}
  },
  "errors": [
    {
      "code": "BearingMissingPrefix",
      "severity": "WARNING",
      "stage": "parse",
      "leg_index": 0,
      "field": "tie_bearing",
      "message": "Tie bearing '50 deg. 50' E.' missing N/S prefix",
      "raw_value": "50 deg. 50' E.",
      "recovery_applied": true,
      "recovery_method": "Assumed 'N' prefix (most common for tie bearings)",
      "recovered_value": "N. 50 deg. 50' E.",
      "alternatives": [
        {"value": "S. 50 deg. 50' E.", "azimuth": 129.167}
      ]
    }
  ],
  "confidence": {
    "confidence": "medium",
    "score": 0.7,
    "reasons": ["Tie bearing missing N/S prefix — recovery applied with assumption"]
  },
  "source_quality": "degraded"
}
```

### Error schema fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | Yes | Machine-readable error code (from tables above) |
| `severity` | string | Yes | `FATAL`, `ERROR`, `WARNING`, `INFO` |
| `stage` | string | Yes | Pipeline stage: `input`, `parse`, `bllm`, `traverse`, `validate`, `transform`, `output` |
| `leg_index` | int | No | 0-based index of the offending traverse leg (null for non-leg errors) |
| `field` | string | No | Specific field: `tie_bearing`, `bearing`, `distance`, `monument`, `area`, `footer` |
| `message` | string | Yes | Human-readable description |
| `raw_value` | string | No | The original text that caused the error |
| `recovery_applied` | bool | Yes | Whether the engine applied automatic recovery |
| `recovery_method` | string | No | Description of recovery if applied |
| `recovered_value` | string | No | The value used after recovery |
| `alternatives` | array | No | Other possible interpretations (for ambiguous errors) |

---

## 14. Complete Error Code Registry

### Parse Stage (17 codes)

| Code | Severity | Recoverable? |
|------|----------|-------------|
| `InputEmpty` | FATAL | No |
| `InputTooShort` | WARNING | Yes (attempt parse) |
| `EncodingNonUTF8` | WARNING | Yes (decode fallback) |
| `ControlCharacters` | INFO | Yes (strip) |
| `TieBlockNotFound` | FATAL* | Yes (coordinate-based or relative) |
| `TieDistanceMissing` | ERROR | Partial (relative polygon) |
| `TieMonumentUnparseable` | ERROR | Partial (fuzzy match) |
| `BearingMissingPrefix` | WARNING | Yes (heuristic) |
| `BearingMissingSuffix` | WARNING | Yes (heuristic) |
| `BearingUnparseable` | ERROR | No |
| `BearingOutOfRange` | WARNING | Yes (reinterpret as azimuth) |
| `BearingSecondsDetected` | INFO | Yes (include seconds) |
| `BearingMinutesOutOfRange` | WARNING | Yes (attempt deg↔min swap) |
| `DueCardinalAmbiguous` | WARNING | Yes (context inference) |
| `DistanceZero` | ERROR | No (skip leg) |
| `DistanceMissing` | ERROR | No (skip leg) |
| `DistanceUnreasonable` | WARNING | Yes (proceed with caution) |
| `DistanceNegative` | ERROR | Yes (abs value) |
| `DistanceDecimalComma` | INFO | Yes (automatic) |
| `MissingClosingLeg` | ERROR | Partial (geometric close) |
| `MissingCorners` | WARNING | Yes (informational) |
| `DuplicateCorner` | WARNING | Yes (use first) |
| `NoLegsFound` | FATAL | No |
| `SingleLeg` | ERROR | No (line only) |
| `TwoLegs` | ERROR | No (line only) |
| `AreaNotFound` | WARNING | Yes (skip cross-check) |
| `AreaWordsNumMismatch` | WARNING | Yes (use numeral) |
| `AreaZero` | ERROR | No (skip cross-check) |
| `FooterNotFound` | WARNING | Yes (defaults applied) |
| `BearingTypeUnknown` | WARNING | Yes (default grid) |
| `SurveyDateUnparseable` | INFO | Yes (skip era heuristic) |
| `SurveyPlanUnparseable` | INFO | Yes (skip plan metadata) |

### BLLM Stage (6 codes)

| Code | Severity | Recoverable? |
|------|----------|-------------|
| `BLLMNotFound` | FATAL* | Partial (caller-provided or relative) |
| `AmbiguousBLLM` | ERROR | Partial (return candidates) |
| `BLLMDatumMismatch` | WARNING | Yes (proceed with note) |
| `BLLMCoordinateInvalid` | ERROR | No (try next match) |
| `BLLMZoneInferFailed` | ERROR | Partial (caller-provided zone) |
| `BLLMMonumentTypeUnsupported` | WARNING | Partial (caller-provided coords) |

### Traverse Stage (6 codes)

| Code | Severity | Recoverable? |
|------|----------|-------------|
| `TraverseOverflow` | FATAL | No |
| `ClosureFail` | ERROR | Yes (output with caveat) |
| `ClosureWarn` | WARNING | Yes |
| `AreaDiscrepancyFail` | ERROR | Yes (output with caveat) |
| `SelfIntersection` | ERROR | Yes (output with flag) |
| `DegeneratePolygon` | ERROR | No |

### Transform Stage (7 codes)

| Code | Severity | Recoverable? |
|------|----------|-------------|
| `DatumAmbiguous` | WARNING | Yes (default PRS92) |
| `ZoneUnknown` | ERROR | Partial (return grid coords only) |
| `ZoneBoundaryAmbiguous` | WARNING | Partial (return both results) |
| `HelmertParamConflict` | ERROR | Yes (use EPSG canonical) |
| `Luzon1911PathBFailed` | WARNING | Yes (fall back to Path A) |
| `EllipsoidalHeightMissing` | INFO | Yes (h=0 default) |
| `InverseTMConvergenceFail` | FATAL | No |

### Output Stage (2 codes)

| Code | Severity | Recoverable? |
|------|----------|-------------|
| `PartialResult` | INFO | Yes (return available fields) |
| `CoordinateClampWarning` | WARNING | Yes (proceed) |

**Total: 42 error codes across 5 pipeline stages.**

---

## 15. Graceful Degradation Hierarchy

When the full pipeline cannot complete, the engine degrades gracefully:

```
Level 1 (full success):
  WGS84 corner coordinates + validation report + confidence "high"

Level 2 (datum uncertain):
  PRS92 corner coordinates (no WGS84 output)
  Triggered by: ZoneUnknown, InverseTMConvergenceFail

Level 3 (BLLM missing):
  Relative polygon only (Corner 1 at origin, other corners as offsets)
  Triggered by: BLLMNotFound, BLLMCoordinateInvalid

Level 4 (coordinate-based TD):
  Direct WGS84 corners from text (no traverse computation)
  Triggered by: TieBlockNotFound + COORD_CORNER_RE match

Level 5 (parse partial):
  Parsed fields only (bearings, distances, area) — no coordinates
  Triggered by: NoLegsFound, or multiple FATAL errors

Level 6 (total failure):
  Error report only
  Triggered by: InputEmpty, InputTooShort → parse yields nothing
```

### Output for each degradation level

```json
{
  "degradation_level": 3,
  "degradation_reason": "BLLMNotFound: 'BLLM NO. 1, PLS-1110' not in database",
  "available_output": {
    "corners_wgs84": null,
    "corners_prs92": null,
    "corners_relative": [
      {"index": 1, "dN_m": 0.0, "dE_m": 0.0},
      {"index": 2, "dN_m": 3.496, "dE_m": -16.034},
      {"index": 3, "dN_m": 33.579, "dE_m": -10.487},
      {"index": 4, "dN_m": 27.796, "dE_m": 5.245}
    ],
    "polygon_shape": "valid",
    "computed_area_sqm": 484.85,
    "stated_area_sqm": 485.0,
    "closure": {"e_m": 0.014, "precision_denom": 6575}
  }
}
```

---

## 16. Implementation Notes

### 16.1 Error collection pattern

Use an accumulator pattern — never throw exceptions mid-pipeline:

```python
class EngineResult:
    def __init__(self):
        self.errors: list[dict] = []
        self.stage_results: dict = {}

    def add_error(self, code: str, severity: str, stage: str, **kwargs):
        self.errors.append({
            "code": code, "severity": severity, "stage": stage,
            "recovery_applied": False, **kwargs
        })

    def has_fatal(self) -> bool:
        return any(e["severity"] == "FATAL" for e in self.errors)

    def worst_severity(self) -> str:
        severities = ["INFO", "WARNING", "ERROR", "FATAL"]
        worst = 0
        for e in self.errors:
            idx = severities.index(e["severity"])
            worst = max(worst, idx)
        return severities[worst] if self.errors else "INFO"
```

### 16.2 Do not auto-correct silently

The engine must NEVER modify bearing or distance values without explicit caller consent. All recoveries are reported in the error list. When an ambiguous recovery is applied (e.g., assumed N prefix), the alternatives are provided so the caller can override.

### 16.3 Deterministic behavior

Given the same input, the engine must always produce the same output — including the same errors in the same order. Error recovery heuristics must not depend on random or environmental state.

### 16.4 Log verbosity levels

| Context | What to log |
|---------|-------------|
| Production API | Errors and warnings only (INFO suppressed) |
| Debug mode | All severity levels + raw values + recovery attempts |
| Batch processing | Error codes + confidence scores (for aggregate analysis) |

---

## Sources

- Wave 2: `analysis/text-parser-grammar.md` — parser error codes (14 originally defined; extended here to 31)
- Wave 2: `analysis/validation-rules.md` — validation thresholds and output schema
- Wave 2: `analysis/traverse-algorithm.md` — closure computation and tolerance
- Wave 2: `analysis/bllm-dataset-compilation.md` — BLLM lookup algorithm and data quality issues
- Wave 2: `analysis/luzon1911-to-prs92-transform.md` — datum detection and transformation paths
- Wave 2: `analysis/prs92-to-wgs84-transform.md` — Helmert parameters and inverse TM
- Wave 3: `analysis/format-variations.md` — reconstituted title degradation patterns, floating parcels, coordinate-based TDs
- Wave 1: `analysis/tech-description-samples.md` — real-world error examples (Sample 4: missing prefix/suffix)
- TitlePlotterPH source — `.replace(',', '.')` distance handling, `bearing_to_azimuth()` quadrant logic
- DENR DAO 2007-29 §28(b), §29, §30 — tolerance thresholds
- CREBA: "Technical Errors in Land Titles: Detection & Correction" (2025) — reconstituted title patterns
- RA 26 (1946), RA 6732 (1989) — reconstituted title governance
