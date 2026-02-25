# Text Parser Grammar — Philippine Land Title Technical Descriptions

**Aspect:** text-parser-grammar (Wave 2)
**Date:** 2026-02-25
**Depends on:** tech-description-samples, bllm-database-sources (Wave 1)
**Verification:** Cross-checked against TitlePlotterPH source code (title_plotter_dialog.py, llm_ocr_dialog.py) and 8-sample corpus from Wave 1

---

## Overview

A technical description (TD) is a structured prose document embedded in Philippine Transfer Certificates of Title (TCTs), Original Certificates of Title (OCTs), and survey plans. It describes a land parcel's boundary as a closed polygon via:

1. A **starting reference** (BLLM + tie bearing + tie distance → Corner 1)
2. A **traverse sequence** (N bearing-distance pairs, corners 1→2→3→…→1)
3. An **area statement** (sq.m.)
4. A **footer** (bearing type, survey date)

This grammar extracts all computable fields. Non-computable fields (boundary descriptions, monument types, approval dates) are documented but not parsed.

---

## Document Structure (BNF)

```
<technical-description> ::=
    <lot-identification>
    [<boundary-description>]
    <tie-block>
    <traverse-block>
    <area-statement>
    [<footer>]

<lot-identification> ::=
    "A parcel of land" "(" <lot-reference> ")"
    [", being a portion of" <parent-lot>]
    [", L.R.C." <record-ref>]
    ")," "situated in" <location> "."

<boundary-description> ::=
    "Bounded on the" <boundary-clause> (";" <boundary-clause>)* "."

<tie-block> ::=
    "Beginning at a point marked" <corner-label> "on plan,"
    "being" <bearing> "," <distance> "m." "from" <monument-reference> ","
    ["thence" <traverse-leg> ";"]    ; (first leg may follow immediately)

<traverse-block> ::=
    (<traverse-leg> ";")* <closing-leg>

<traverse-leg> ::=
    ["thence"] <bearing> "," <distance> "m." "to" <corner-destination>

<closing-leg> ::=
    ["thence"] <bearing> "," <distance> "m." "to" <point-of-beginning>

<area-statement> ::=
    "containing an area of" <area-words> "(" <area-number> ")" <area-unit>
    | "containing an area of" <area-number> <area-unit>

<footer> ::=
    "Bearings" ("true" | "True" | "Grid" | "grid") ";"?
    ["declination" <bearing> ";"]
    "date of" ["original"] "survey" [","?] <date>
    [";" ["and"] "that of the" <survey-type> "survey" [","] <date>]
    "."
```

---

## Field-Level Grammar and Regex Patterns

### 1. Monument Reference (Tie Point)

The monument reference is the starting anchor. All monument code variants observed in the wild:

| Pattern | Monument Type | Examples |
|---------|--------------|---------|
| `BLLM No. N[, descriptor]` | Bureau of Lands Location Monument | "BLLM No. 1, PLS-1110" |
| `B.L.L.M. N[, descriptor]` | Same with periods | "B.L.L.M. 1, municipality of Malabon" |
| `BLLM. No. N[, descriptor]` | Trailing period variant | "BLLM. No. 1, Pls-793" |
| `BLLM.N[, descriptor]` | No space, no "No." | "BLLM.1, Cad. 652-D" |
| `BLBM No. N[, descriptor]` | Bureau of Lands Barrio Monument | "BLBM No. 1, Makar" |
| `B.B2. No. N[, descriptor]` | Barangay Boundary Monument #2 | "B.B2. No. 42, Angeles Cadastro" |
| `L.W. N[, descriptor]` | Lot Witness monument | "L.W. 22, Piedad Estate" |
| `B.L. Mon.[, descriptor]` | BL Monument (generic) | "B.L. Mon." |
| `MBM No. N[, descriptor]` | Municipal Boundary Monument | via TitlePlotterPH LLM prompt |
| `BLCM[, descriptor]` | Bureau of Lands Control Monument | via TitlePlotterPH LLM prompt |

**Primary monument regex** (matches BLLM and its punctuation variants):

```python
MONUMENT_RE = re.compile(
    r"""
    (?:
        B\.?L\.?L\.?M\.?   # BLLM with optional periods between and/or after letters
        |B\.?L\.?B\.?M\.?  # BLBM
        |B\.?B\d?\.?       # BB2 etc.
        |L\.?W\.?          # LW (Lot Witness)
        |B\.?L\.?\s*Mon\.? # BL Mon.
        |MBM               # Municipal Boundary Monument
        |BLCM              # BL Control Monument
    )
    [\s.]*                 # optional whitespace or dot after code
    (?:No\.?\s*)?          # optional "No." prefix
    (\d+)                  # monument number
    (?:\s*,\s*(.+?))?      # optional descriptor (project, municipality, etc.)
    (?=\s*[,;.])           # lookahead: ends before comma/semicolon/period
    """,
    re.IGNORECASE | re.VERBOSE
)
```

**Fuzzy normalization** for database lookup (per TitlePlotterPH pattern):

```python
def normalize_monument_name(raw: str) -> str:
    """Strip punctuation variants, collapse spaces, uppercase for DB lookup."""
    s = raw.strip()
    # Normalize "B.L.L.M." → "BLLM"
    s = re.sub(r'B\.L\.L\.M\.?', 'BLLM', s, flags=re.IGNORECASE)
    s = re.sub(r'B\.L\.B\.M\.?', 'BLBM', s, flags=re.IGNORECASE)
    # Normalize "No." → "No." (standardize spacing)
    s = re.sub(r'\bNo\.?\s*', 'No. ', s, flags=re.IGNORECASE)
    # Collapse whitespace
    s = re.sub(r'\s+', ' ', s).strip().upper()
    return s
```

**Lookup strategy** (three-tier, per Wave 1 bllm-database-sources analysis):

```
1. Exact name match (normalized)
2. If multiple → narrow by province
3. If still multiple → narrow by municipality (substring)
4. If zero → raise BLLMNotFound
5. If still multiple → raise AmbiguousBLLM
```

### 2. Bearing

Bearings encode the compass direction of a traverse leg as: `<NS_prefix> <angle> <EW_suffix>`.

**Canonical DMS bearing regex** (handles all 7 variants from Wave 1 corpus):

```python
BEARING_RE = re.compile(
    r"""
    ([NS])            # N or S prefix (required except for Due-cardinal)
    [\s.]*            # optional separator (period in "N. 45° 30' E.")
    (\d{1,3})         # degrees: 1–3 digits (0–180 for quadrant bearings)
    \s*               # optional whitespace
    (?:°|deg\.?|°)?   # degree mark: ° or "deg." or "deg" (optional if followed by space)
    \s*               # optional whitespace
    (?:               # optional minutes group
        (\d{1,2})     # minutes: 1–2 digits
        \s*           # optional whitespace
        [''′`\u2019\u2018]?  # minute mark: ', ', ′, `, Unicode apostrophes (optional)
    )?                # minutes are optional (degrees-only bearings exist: "N. 51° W.")
    \s*               # optional whitespace
    ([EW])            # E or W suffix (required except for Due-cardinal)
    [\s.]*            # optional trailing separator
    """,
    re.IGNORECASE | re.VERBOSE
)

# Special case: Due North / Due South / Due East / Due West
DUE_CARDINAL_RE = re.compile(
    r'\bDue\s+(North|South|East|West)\b',
    re.IGNORECASE
)

# Special case: seconds (if present, silently dropped)
# Some older titles include seconds: "N. 45° 30' 15" E."
# The bearing regex above does not capture seconds — they are ignored.
```

**Bearing parsing function** (with error recovery):

```python
def parse_bearing(text: str) -> dict | None:
    """
    Parse one bearing expression. Returns dict with keys:
      ns (str): 'N' or 'S'
      deg (int): degrees 0–180
      min (int): minutes 0–59 (default 0 if absent)
      ew (str): 'E' or 'W'
      azimuth (float): computed azimuth 0–360°
      raw (str): original text matched

    Returns None if no bearing found.
    Special case: Due North/South/East/West → returns fixed azimuth.
    """
    # Try Due-cardinal first
    m = DUE_CARDINAL_RE.search(text)
    if m:
        cardinal = m.group(1).capitalize()
        az = {'North': 0.0, 'East': 90.0, 'South': 180.0, 'West': 270.0}[cardinal]
        return {'ns': 'N' if az in (0.0, 90.0) else 'S',
                'deg': int(az) % 90, 'min': 0,
                'ew': 'E' if az in (0.0, 90.0) else 'W',
                'azimuth': az, 'raw': m.group(0)}

    # Try standard quadrant bearing
    m = BEARING_RE.search(text)
    if not m:
        return None

    ns = m.group(1).upper()
    deg = int(m.group(2))
    min_ = int(m.group(3)) if m.group(3) else 0
    ew = m.group(4).upper()
    azimuth = bearing_to_azimuth(ns, deg, min_, ew)
    return {'ns': ns, 'deg': deg, 'min': min_, 'ew': ew,
            'azimuth': azimuth, 'raw': m.group(0)}
```

**Bearing-to-azimuth conversion** (confirmed against TitlePlotterPH `bearing_to_azimuth()`):

```python
def bearing_to_azimuth(ns: str, deg: int, min_: int, ew: str) -> float:
    """Convert quadrant bearing to azimuth (0–360°, measured clockwise from North)."""
    angle = deg + min_ / 60.0
    if   ns == 'N' and ew == 'E': return angle           # NE quadrant: 0–90
    elif ns == 'S' and ew == 'E': return 180.0 - angle   # SE quadrant: 90–180
    elif ns == 'S' and ew == 'W': return 180.0 + angle   # SW quadrant: 180–270
    elif ns == 'N' and ew == 'W': return 360.0 - angle   # NW quadrant: 270–360
    raise ValueError(f"Invalid bearing: {ns}{deg}°{min_}'{ew}")
```

**Due-cardinal fixed azimuths:**

| Phrase | Azimuth |
|--------|---------|
| Due North | 0.0° |
| Due East | 90.0° |
| Due South | 180.0° |
| Due West | 270.0° |

**Error / partial bearing detection:**

- Missing N/S prefix: `"50 deg. 50' E."` — no leading N/S; flag as `BearingMissingPrefix`
- Missing E/W suffix: `"N. 22 deg. 40'"` — no trailing E/W; flag as `BearingMissingSuffix`
- Both missing → `BearingUnparseable`
- These errors appear in transcription artifacts (Sample 4). Parser should attempt regex with one direction assumed; if ambiguous, raise and ask caller for correction.

### 3. Distance

```python
DISTANCE_RE = re.compile(
    r"""
    ([\d,]+(?:[.,]\d+)?)  # integer or decimal, possibly with comma thousands or decimal comma
    \s*
    m\.?                  # meter suffix (required in most titles)
    """,
    re.VERBOSE
)

def parse_distance(text: str) -> float:
    """Parse distance in metres. Handles decimal comma (European style)."""
    m = DISTANCE_RE.search(text)
    if not m:
        raise ValueError(f"No distance found in: {text!r}")
    raw = m.group(1).replace(',', '.')  # "936,15" → "936.15"
    # If still has period for thousands (unlikely in PH titles), strip it
    return float(raw)
```

Note: TitlePlotterPH explicitly handles the comma-as-decimal case (`.replace(',', '.')`). This appears in some digitized documents.

### 4. Traverse Leg (Combined Bearing + Distance)

A traverse leg is `[thence] <bearing>, <distance> m. to <corner-destination>`.

**Leg extraction regex** (finds each leg in the full TD text):

```python
LEG_RE = re.compile(
    r"""
    (?:thence\s+)?                          # optional "thence" keyword
    (?P<bearing>
        (?:Due\s+(?:North|South|East|West)) # Due-cardinal alternative
        |
        [NS][\s.]*\d{1,3}[\s°.deg]*(?:\d{1,2}[\s''`′]*)?[EW][\s.]*
    )
    \s*[,;]?\s*                             # comma or semicolon separator
    (?P<distance>[\d,]+(?:[.,]\d+)?)\s*m\.? # distance in metres
    (?:\s+to\s+                             # "to" keyword
        (?P<destination>
            (?:the\s+)?point\s+of\s+beginning  # closing leg
            |point\s+[\d"]+(?:\s*,\s*point\s+of\s+beginning)?  # point N, [closing]
            |[\d"]+                                             # bare point number
        )
    )?
    """,
    re.IGNORECASE | re.VERBOSE
)
```

**Corner label extraction:**

```python
CORNER_LABEL_RE = re.compile(
    r"""
    (?:to\s+)?                     # optional "to"
    (?:the\s+)?point\s+            # "point"
    (?:
        of\s+beginning             # closing phrase
        |
        "?(\d+)"?                  # corner number (with optional surrounding quotes)
        (?:\s*,\s*point\s+of\s+beginning)?  # optional close appended
    )
    """,
    re.IGNORECASE | re.VERBOSE
)
```

**Closing leg detection:**

```python
CLOSING_PHRASES = [
    r'to\s+the\s+point\s+of\s+beginning',
    r'to\s+point\s+of\s+beginning',           # no "the"
    r'to\s+point\s+\d+\s*,\s*point\s+of\s+beginning',  # "to point 1, point of beginning"
]
CLOSING_RE = re.compile('|'.join(CLOSING_PHRASES), re.IGNORECASE)
```

### 5. Corner Label at Beginning

```python
# "Beginning at a point marked "1" on plan"
# Variants: "1", '1', 1 (no quotes)
BEGINNING_LABEL_RE = re.compile(
    r'Beginning\s+at\s+a\s+point\s+marked\s+["\']?(\d+)["\']?\s+on\s+plan',
    re.IGNORECASE
)
```

### 6. Tie Block (Full)

The tie block combines the corner label, bearing, distance, and monument reference:

```python
TIE_BLOCK_RE = re.compile(
    r"""
    Beginning\s+at\s+a\s+point\s+marked\s+["\']?(\d+)["\']?\s+on\s+plan,?\s+
    being\s+
    (?P<tie_bearing>
        (?:Due\s+(?:North|South|East|West))
        |
        [NS][\s.]*\d{1,3}[\s°deg.]*(?:\d{1,2}[\s''`′]*)?[EW][\s.]*
    )
    \s*[,;]?\s*
    (?P<tie_distance>[\d,]+(?:[.,]\d+)?)\s*m\.?\s+
    from\s+
    (?P<monument>.+?)
    (?=[,;.]|thence|\Z)   # end: comma/semicolon/period, or "thence", or end of string
    """,
    re.IGNORECASE | re.VERBOSE
)
```

### 7. Area Statement

Area appears as the last substantive field before the footer. Multiple formats:

```python
# Words-spelled-out with numerals in parentheses:
# "FOUR HUNDRED EIGHTY FIVE (485) SQUARE METERS"
# "One Thousand Twenty-Four Square Meters (1,024 m²)"
AREA_WORDS_NUM_RE = re.compile(
    r"""
    containing\s+an\s+area\s+of\s+
    (?P<area_words>[A-Z][A-Z\s\-]+?)     # spelled-out number in ALL CAPS or Title Case
    \s*\((?P<area_num>[\d,]+(?:\.\d+)?)\)\s*  # numeral in parentheses
    (?:sq(?:uare)?\.?\s*m(?:eters?|\.)?|m²)   # unit: "sq. m.", "square meters", "m²"
    """,
    re.IGNORECASE | re.VERBOSE
)

# Numerals only:
# "664 square meters"
AREA_NUM_ONLY_RE = re.compile(
    r"""
    containing\s+an\s+area\s+of\s+
    (?P<area_num>[\d,]+(?:\.\d+)?)       # numeral (with optional thousands comma)
    \s*
    (?:sq(?:uare)?\.?\s*m(?:eters?|\.)?|m²)
    """,
    re.IGNORECASE | re.VERBOSE
)
```

**Area suffix variants** (per Wave 1 corpus):

| Suffix | Meaning |
|--------|---------|
| (none) | No qualifier |
| `, more or less` | Approximate |
| `, only` | Exact (rare; appears in older Visayas cadastrals) |

### 8. Footer / Survey Metadata

```python
FOOTER_RE = re.compile(
    r"""
    Bearings\s*[:]?\s*                    # "Bearings:" or "Bearings"
    (?P<bearing_type>true|grid)\s*[;,.]?\s*  # "true" or "Grid" (case-insensitive)
    (?:declination\s+(?P<declination>.+?)\s*[;.])?  # optional declination
    (?:date\s+of\s+(?:original\s+)?survey\s*[,:]?\s*(?P<survey_date>[^;.]+))?
    (?:[;,]\s*(?:and\s+)?that\s+of\s+the\s+(?P<subd_type>\w+)\s+survey\s*[,:]?\s*(?P<subd_date>[^;.]+))?
    """,
    re.IGNORECASE | re.VERBOSE
)
```

**Bearing type values:**
- `"true"` → geographic north reference (True North)
- `"grid"` → PTM/PRS92 zone north reference

**Declination field** (only in some older titles): `"0° 56′ E."` — this is the magnetic declination stated for information; grid/true bearings do NOT require declination correction.

### 9. Survey Plan Number

Survey plan numbers encode the survey type, region, and sequence number.

```python
SURVEY_PLAN_RE = re.compile(
    r"""
    (?:
        (?:\(LRC\)\s*)?           # optional LRC prefix
        (Psd|Psu|Csd|Cad|Mr|Bp|PLS|Pls|Ccs|Mcs)  # survey type code
        (?:-\(af\)|-\(ct\)|-\(if\))?   # optional parenthetical qualifier
        -?(\d{2})?                # optional region code (2 digits)
        [-–]?(\d+)                # sequence number
        ([A-Z])?                  # optional suffix letter (A, B, C, D...)
        |
        Cad\.?\s+(\d+)([A-Z]?)   # Cadastral: "Cad. 407" or "Cad. 652-D"
    )
    """,
    re.IGNORECASE | re.VERBOSE
)
```

**Survey plan prefix registry:**

| Prefix | Full name | Region code? | Notes |
|--------|-----------|-------------|-------|
| Psd | Private Subdivision Survey | Optional (new format) | Old: Psd-NNNNN; New: Psd-RR-NNNNNN |
| Psu | Private Survey (upland) | Yes | Often has qualifier: Psu-(af)-, Psu-(ct)- |
| Csd | Cadastral Subdivision | Yes | Region in 2nd segment |
| Cad | Cadastral Survey | No | Often "Cad. NNN" with period and space |
| PLS/Pls | Public Land Survey | No | PLS-NNNNN or Pls-NNN |
| Mr | Municipal Registration | No | Mr-NNNN-X |
| Bp | Bureau of Lands Plan | No | Bp-NNNNN |
| Ccs | Consolidation Survey | Optional | |
| (LRC) Psd | LRC-approved subdivision | Optional | Prefix in parentheses |

---

## Full Parsing Pipeline

```
INPUT: raw technical description text (string)

STEP 1: Normalize whitespace
  - Collapse multiple spaces/newlines to single space
  - Standardize curly quotes to straight quotes
  - Preserve line structure for context

STEP 2: Extract lot identification
  - Find: "A parcel of land (..."
  - Extract: lot number, block number, survey plan number, parent lot, location

STEP 3: Extract tie block
  - Apply TIE_BLOCK_RE
  - If match: extract corner_label, tie_bearing, tie_distance, monument_ref
  - If no match: raise TieBlockNotFound

STEP 4: Resolve monument coordinates
  - Normalize monument_ref using normalize_monument_name()
  - Lookup in BLLM database (three-tier match)
  - Return: northing (m), easting (m), zone (1–5), datum

STEP 5: Extract traverse legs
  - Apply LEG_RE globally to text (findall)
  - For each match: parse bearing, parse distance, identify destination
  - Filter: exclude any match overlapping with the tie block position
  - Result: ordered list of (bearing_dict, distance_m)
  - The tie line is the first entry; subsequent entries are polygon legs

STEP 6: Detect closing leg
  - Scan each leg's destination text for CLOSING_RE
  - Flag that leg as closing; confirm it is the last leg
  - If closing leg not found: raise MissingClosingLeg

STEP 7: Extract area
  - Try AREA_WORDS_NUM_RE first (preferred — numeral in parens is unambiguous)
  - Fall back to AREA_NUM_ONLY_RE
  - Parse numeral → float (remove thousands commas)
  - Return: stated_area_sqm (float)

STEP 8: Extract footer
  - Apply FOOTER_RE
  - Return: bearing_type ('true'|'grid'), survey_date (string), declination (if present)

STEP 9: Assemble output structure
  - {
      lot_id: {...},
      tie_point: { raw_name, normalized_name, northing, easting, zone, datum },
      tie_bearing: { ns, deg, min, ew, azimuth },
      tie_distance_m: float,
      legs: [ { bearing: {...}, distance_m: float }, ... ],  # corners 1→2→...→close
      stated_area_sqm: float,
      bearing_type: 'true'|'grid',
      survey_date: string,
      corner_count: int
    }
```

---

## Output Data Structure (Schema)

```json
{
  "lot_id": {
    "lot_number": "1",
    "block_number": null,
    "survey_plan": "PLS-1110",
    "parent_lot": null,
    "lrc_record": null,
    "location": {
      "barangay": null,
      "municipality": "Alilem",
      "province": "Ilocos Sur",
      "island": "Luzon"
    }
  },
  "tie_point": {
    "raw_name": "BLLM No. 1, PLS-1110, Alilem Public Land Subd.",
    "normalized_name": "BLLM NO. 1, PLS-1110",
    "northing_m": null,
    "easting_m": null,
    "zone": null,
    "datum": null,
    "lookup_status": "pending"
  },
  "tie_bearing": {
    "ns": "S",
    "deg": 65,
    "min": 2,
    "ew": "E",
    "azimuth": 114.967
  },
  "tie_distance_m": 348.29,
  "legs": [
    { "bearing": {"ns": "N", "deg": 77, "min": 42, "ew": "W", "azimuth": 282.3}, "distance_m": 16.41 },
    { "bearing": {"ns": "N", "deg": 10, "min": 27, "ew": "E", "azimuth": 10.45}, "distance_m": 30.59 },
    { "bearing": {"ns": "S", "deg": 69, "min": 49, "ew": "E", "azimuth": 110.183}, "distance_m": 16.76 },
    { "bearing": {"ns": "S", "deg": 10, "min": 42, "ew": "W", "azimuth": 190.7}, "distance_m": 28.29, "closing": true }
  ],
  "stated_area_sqm": 485.0,
  "bearing_type": "grid",
  "survey_date": "April–May 1983",
  "corner_count": 4
}
```

---

## Worked Parsing Example: Sample 1 (PLS-1110, Alilem, Ilocos Sur)

**Input text (excerpt):**
```
Beginning at a point marked "1" of Lot-1 on plan, being S. 65° 02' E., 348.29 m. from BLLM No. 1,
PLS-1110, Alilem Public Land Subd., thence N. 77° 42' W., 16.41 m. to point 2; thence N. 10° 27' E.,
30.59 m. to point 3; thence S. 69° 49' E., 16.76 m. to point 4; thence S. 10° 42' W., 28.29 m.
to point 1, point of beginning, containing an area of FOUR HUNDRED EIGHTY FIVE (485) SQUARE METERS.
Bearings: Grid; date of original survey was April–May, 1983.
```

**Step 2 — Lot ID:** Lot 1, PLS-1110, Alilem, Ilocos Sur, Luzon

**Step 3 — Tie block match:**
- corner_label = "1"
- tie_bearing raw = "S. 65° 02' E."
  - ns="S", deg=65, min=2, ew="E" → azimuth = 180 - 65.033 = 114.967°
- tie_distance = 348.29 m
- monument_ref = "BLLM No. 1, PLS-1110, Alilem Public Land Subd."

**Step 4 — Monument lookup:**
- normalized_name = "BLLM NO. 1, PLS-1110"
- database lookup → returns Northing, Easting (if present), zone, datum

**Step 5 — Traverse legs (4 legs parsed):**

| # | raw | ns | deg | min | ew | azimuth (°) | dist (m) |
|---|-----|----|-----|-----|----|-------------|---------|
| 1 | N. 77° 42' W. | N | 77 | 42 | W | 360−77.7 = 282.300 | 16.41 |
| 2 | N. 10° 27' E. | N | 10 | 27 | E | 10.450 | 30.59 |
| 3 | S. 69° 49' E. | S | 69 | 49 | E | 180−69.817 = 110.183 | 16.76 |
| 4 | S. 10° 42' W. | S | 10 | 42 | W | 180+10.7 = 190.700 | 28.29 |

**Step 6 — Closing leg:** Leg 4 destination = "point 1, point of beginning" → closing=True ✓

**Step 7 — Area:** AREA_WORDS_NUM_RE matches → numeral group = "485" → 485.0 sq.m.

**Step 8 — Footer:** bearing_type = "grid", survey_date = "April–May, 1983"

---

## Worked Parsing Example: Sample 5 (Due North case, Psu-(af)-02-001767)

**Leg containing "Due North"** (10th leg of 12):
```
thence Due North 5.64 m. to point 11;
```

- `DUE_CARDINAL_RE` matches "Due North"
- azimuth = 0.0°
- distance = 5.64 m
- destination = "point 11"
- delta_N = 5.64 × cos(0°) = 5.640 m, delta_E = 5.64 × sin(0°) = 0.000 m

---

## Degrees-Only Bearing (Sample 2: "N. 51° W.")

```
thence N. 51° W., 24.01 m. to point "5";
```

- BEARING_RE matches: ns="N", deg=51, min=None (group 3 absent) → default min=0
- azimuth = 360 - 51.0 = 309.0°
- distance = 24.01 m
- destination = `"5"` (quoted numeral — strip quotes)

---

## "deg." Format Bearing (Sample 4: "50 deg. 50' E.")

```
being 50 deg. 50' E., 457.01 m. from L.W. 22, Piedad Estate;
```

- BEARING_RE does NOT match (no N/S prefix) → `BearingMissingPrefix` error
- Recovery: infer prefix from quadrant and context (E → could be NE or SE)
- Flag to caller: "Tie bearing missing N/S prefix — possibly N. 50° 50' E. (transcription error)"
- Default recovery: assume N (most common case for tie bearings pointing away from an urban monument)
- Record in `parse_warnings` list

---

## Format Variation Handling Summary

| Variation | Handling |
|-----------|---------|
| `°` vs `deg.` vs `deg` | BEARING_RE handles all via `(?:°\|deg\.?\|deg)?` |
| Minutes present vs absent | Minutes group in BEARING_RE is optional `(?:...)?` |
| "Due North/South/East/West" | DUE_CARDINAL_RE, fixed azimuth table |
| Quoted point numbers `"2"` | Strip double quotes in CORNER_LABEL_RE |
| `thence` present vs absent | Optional `(?:thence\s+)?` in LEG_RE |
| Area words + numerals | AREA_WORDS_NUM_RE |
| Area numerals only | AREA_NUM_ONLY_RE fallback |
| Comma thousands separator in area | Remove commas before `float()` |
| Decimal comma in distance | `.replace(',', '.')` (TitlePlotterPH pattern) |
| `more or less` suffix | Captured in area suffix; does not affect numeric value |
| `, only` suffix | Same — captured, ignored numerically |
| Missing N/S prefix | `BearingMissingPrefix` warning, attempt recovery |
| Missing E/W suffix | `BearingMissingSuffix` warning, attempt recovery |
| Seconds in DMS | Silently dropped (only degrees + minutes used) |
| B.L.L.M. periods | Normalized to BLLM in `normalize_monument_name()` |
| BLBM vs BLLM code | Both handled in MONUMENT_RE alternation |
| L.W. (Lot Witness) | Handled in MONUMENT_RE; not in tiepoints.json |
| Survey plan with qualifier | Psu-(af)-, (LRC) Psd- patterns in SURVEY_PLAN_RE |

---

## Error and Warning Codes

| Code | Type | Condition |
|------|------|-----------|
| `BearingMissingPrefix` | Warning | No N/S before degrees; recovery attempted |
| `BearingMissingSuffix` | Warning | No E/W after minutes; recovery attempted |
| `BearingUnparseable` | Error | Neither prefix nor suffix found |
| `TieBlockNotFound` | Error | "Beginning at a point" phrase absent |
| `MissingClosingLeg` | Error | No leg ends with "point of beginning" |
| `BLLMNotFound` | Error | Monument not in database |
| `AmbiguousBLLM` | Error | Multiple records match after province+municipality filter |
| `AreaNotFound` | Error | No area statement matched |
| `BearingOutOfRange` | Warning | Degrees > 90 (invalid for quadrant bearing) |
| `DistanceZero` | Error | Parsed distance = 0.0 m |
| `DueCardinalAmbiguous` | Warning | "North" or "South" without "Due" prefix |

---

## Key Findings and Design Notes

1. **TitlePlotterPH treats the tie line as the first bearing row**, not a separate structure. The computation engine should follow the same model: tie_bearing + tie_distance is Leg 0; all subsequent legs are polygon edges.

2. **Seconds are universally dropped** in Philippine TD practice — TitlePlotterPH has no seconds field, and the DENR standard uses DMS with minutes only. Engine should warn if seconds are detected (suggests unusual source document).

3. **"Due North" and variants are real**, appearing in post-PRS92 surveys (Sample 5, 2011). The parser must handle these before the standard BEARING_RE to avoid a false non-match.

4. **Area cross-validation is deferred to validation-rules** (Wave 2). The parser returns `stated_area_sqm`; the traverse algorithm returns `computed_area_sqm`; the validator compares them.

5. **Monument types beyond BLLM** (L.W., B.B2., MBM) are real and must be parsed as valid tie points. However, they will not be in the BLLM database — the engine must support caller-provided coordinates for these.

6. **Survey plan number prefix** encodes region (for post-region-code surveys) and survey type. For datum inference, the survey date in the footer is more reliable than plan number alone.

7. **Datum is NEVER explicit in the TD body text**. Datum inference lives in the luzon1911-to-prs92-transform spec (Wave 2), not in the parser.

---

## Sources

- Wave 1: `analysis/tech-description-samples.md` — 8-sample corpus (all 7 bearing variants, 7 monument code variants)
- Wave 1: `analysis/bllm-database-sources.md` — monument normalization and lookup algorithm
- TitlePlotterPH `dialogs/title_plotter_dialog.py` — `bearing_to_azimuth()`, `calculate_deltas()`, `generate_coordinates()`, `parse_bearings_legacy()`, `parse_text_bearings()` (verified 2026-02-25)
- TitlePlotterPH `dialogs/llm_ocr_dialog.py` — LLM prompt structure, JSON schema, monument type list (verified 2026-02-25)
- Cross-check: BEARING_RE covers all variants identified independently by TitlePlotterPH (matching: degree symbol variants, Unicode apostrophes, optional minutes)
- Conflict: TitlePlotterPH uses LLM-first for area parsing (no regex); this spec adds explicit AREA_WORDS_NUM_RE and AREA_NUM_ONLY_RE for deterministic parsing without LLM dependency
