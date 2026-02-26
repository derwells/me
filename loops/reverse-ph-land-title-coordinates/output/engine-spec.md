# Philippine Land Title Coordinate Engine — Computation Spec

**Version:** 1.1 (2026-02-26)
**Purpose:** Convert Philippine land title technical descriptions into WGS84 latitude/longitude coordinates.
**Audience:** Developer implementing the computation engine.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Stage 1: Text Parser](#2-stage-1-text-parser)
3. [Stage 2: BLLM Resolution](#3-stage-2-bllm-resolution)
4. [Stage 3: Traverse Computation](#4-stage-3-traverse-computation)
5. [Stage 4: Datum Transformation](#5-stage-4-datum-transformation)
6. [Stage 5: Validation](#6-stage-5-validation)
7. [Error Handling](#7-error-handling)
8. [Test Vectors](#8-test-vectors)
9. [Appendix A: Ellipsoid & Projection Constants](#appendix-a-ellipsoid--projection-constants)
10. [Appendix B: Survey Plan Prefix Registry](#appendix-b-survey-plan-prefix-registry)
11. [Appendix C: Province-to-Zone Mapping](#appendix-c-province-to-zone-mapping)
12. [Appendix D: BLLM Dataset Reference](#appendix-d-bllm-dataset-reference)

---

## 1. Architecture Overview

### 1.1 Pipeline

```
Input: Raw TD text + optional metadata (caller-provided BLLM coords, zone, datum)
  │
  ▼
[Stage 1: PARSE]     Extract structured fields from prose TD text
  │
  ▼
[Stage 2: BLLM]      Resolve tie point monument → PRS92 grid coordinates
  │
  ▼
[Stage 3: TRAVERSE]   Compute corner coordinates from bearing/distance pairs
  │
  ▼
[Stage 4: TRANSFORM]  PRS92 grid → WGS84 geographic (inverse TM + Helmert)
  │                    (or Luzon 1911 → PRS92 → WGS84 for legacy titles)
  ▼
[Stage 5: VALIDATE]   Closure error, area cross-check, geometry sanity
  │
  ▼
Output: WGS84 lat/lng per corner + validation report + confidence score
```

### 1.2 Input Assumptions

- Pre-transcribed technical description text (no OCR stage)
- BLLM coordinates either from compiled dataset or provided by caller
- UTF-8 text encoding (with fallback to latin-1)

### 1.3 Graceful Degradation

When the full pipeline cannot complete, the engine degrades:

| Level | Output | Trigger |
|-------|--------|---------|
| 1 (full) | WGS84 corner coordinates + validation | All stages succeed |
| 2 (no WGS84) | PRS92 grid coordinates only | Zone unknown or inverse TM fails |
| 3 (relative) | Relative polygon (Corner 1 at origin) | BLLM not found |
| 4 (coordinate-based) | Direct WGS84 from text | TD has lat/lng per corner instead of traverse |
| 5 (parse only) | Parsed fields, no coordinates | Too few legs or fatal parse errors |
| 6 (failure) | Error report only | Empty input or total parse failure |

---

## 2. Stage 1: Text Parser

### 2.1 Input Pre-Processing

Always applied before parsing, never produces errors:

1. Collapse multiple whitespace (spaces, tabs, newlines) to single space
2. Normalize Unicode quotes (`\u201C`/`\u201D` → `"`, `\u2018`/`\u2019` → `'`)
3. Normalize Unicode degree/minute/second marks (`\u00B0` → `°`, `\u2032` → `′`, `\u2033` → `″`)
4. Strip leading/trailing whitespace
5. Normalize en-dash/em-dash to hyphen in plan numbers

### 2.2 Parser Output Schema

```json
{
  "lot_id": {
    "lot_number": "1",
    "block": null,
    "survey_plan": {
      "raw": "PLS-1110",
      "prefix": "PLS",
      "qualifier": null,
      "region_code": null,
      "sequence": "1110",
      "suffix": null,
      "lrc_prefix": false
    },
    "parent_lot": null,
    "location": {
      "barangay": null,
      "municipality": "Alilem",
      "province": "Ilocos Sur",
      "island": "Luzon"
    }
  },
  "tie_point": {
    "raw_name": "BLLM No. 1, PLS-1110",
    "monument_type": "BLLM",
    "monument_number": 1,
    "descriptor": "PLS-1110"
  },
  "tie_bearing": {
    "ns": "S", "deg": 65, "min": 2, "sec": 0,
    "ew": "E",
    "azimuth_deg": 114.966667
  },
  "tie_distance_m": 348.29,
  "legs": [
    {
      "index": 0,
      "bearing": {
        "ns": "N", "deg": 77, "min": 42, "sec": 0, "ew": "W",
        "azimuth_deg": 282.300000
      },
      "distance_m": 16.41,
      "to_point": "2",
      "closing": false
    }
  ],
  "stated_area_sqm": 485.0,
  "bearing_type": "grid",
  "survey_dates": {
    "original": "April-May, 1983",
    "original_year": 1983,
    "subdivision": null
  },
  "corner_count": 4,
  "metadata": {
    "survey_origin": "numerical",
    "conversion_note": null,
    "monument_type_desc": "BL cyl. conc. mons. 15x40 cms."
  }
}
```

### 2.3 Parsing Grammar

The technical description follows a canonical structure. Each section is extracted by regex.

#### 2.3.1 Lot Identification Block

```
LOT_ID_RE:
  "A parcel of land"
  "(" <lot-designation> ")"
  optional: "being a portion of" <parent-lot>
  "situated in" <location>

LOT_DESIGNATION:
  "Lot" optional("No.") <lot-number>
  optional: ", Block" <block-number>
  optional: "of the" ("subdivision"|"consolidation"|"consolidation-subdivision") "plan"
  <survey-plan-reference>
```

**Lot number patterns:**
- Simple: `Lot 1`, `Lot 9755`
- Compound subdivision: `Lot 457-A-12-B-2-B-2-A`
- Block-qualified: `Lot 28, Block 7`

#### 2.3.2 Survey Plan Number

```python
SURVEY_PLAN_RE = re.compile(r"""
    (?:
        (?:\(LRC\)\s*)?
        (Psd|Psu|Csd|Cad|Mr|Bp|PLS|Pls|Ccs|Mcs|Pcs|Bsd|FP|Ts|Ms|Ap|Cadm|PCadm|Gss|H)
        (?:-\(af\)|-\(ct\)|-\(if\))?     # optional qualifier
        -?(\d{2})?                         # optional 2-digit region code
        [-\u2013]?(\d+)                    # sequence number
        ([A-Z])?                           # optional suffix letter
        (?:\s*\(AR\))?                     # optional agrarian reform tag
        |
        Cad\.?\s+(\d+)([A-Z-]*)           # Cadastral: "Cad. 407" or "Cad. 652-D"
    )
""", re.IGNORECASE | re.VERBOSE)
```

#### 2.3.3 Location Clause

```python
LOCATION_RE = re.compile(r"""
    situated\s+in\s+
    (?:(?:Barangay|Brgy\.?|Bo\.?)\s+(?P<barangay>[^,]+),\s*)?
    (?:(?:Municipality|Mun\.?)\s+of\s+)?
    (?P<municipality>[^,]+),\s*
    (?:(?:Province|Prov\.?)\s+of\s+)?
    (?P<province>[^,]+),\s*
    (?:Island\s+of\s+)?
    (?P<island>Luzon|Visayas|Mindanao|[^.]+)
""", re.IGNORECASE | re.VERBOSE)
```

#### 2.3.4 Tie Block

```python
TIE_BLOCK_RE = re.compile(r"""
    [Bb]eginning\s+at\s+a\s+point\s+marked\s+[""']?1[""']?
    .*?on\s+plan\s*,?\s*
    being\s+
    (?P<tie_bearing>.+?),\s*
    (?P<tie_distance>[\d,.]+)\s*(?:m\.?|meters?|metres?)\s*
    from\s+
    (?P<monument>.+?)
    (?:\s*[,;]\s*thence|\s*[.])
""", re.IGNORECASE | re.DOTALL | re.VERBOSE)
```

**Monument name extraction:**

```python
MONUMENT_RE = re.compile(r"""
    (?P<type>B\.?L\.?L\.?M\.?|BLLM|B\.?B\.?\d*\.?|BBM|MBM|L\.?W\.?)
    \s*(?:No\.?\s*)?
    (?P<number>\d+)
    (?:\s*,\s*(?P<descriptor>.+))?
""", re.IGNORECASE | re.VERBOSE)
```

Monument type normalization:
| Raw Pattern | Normalized |
|-------------|-----------|
| `B.L.L.M.` | `BLLM` |
| `BLLM.` | `BLLM` |
| `B.B2.` | `BBM` (type 2) |
| `L.W.` | `LW` (Liwasan) |
| `MBM` | `MBM` |

#### 2.3.5 Bearing Parser

```python
BEARING_RE = re.compile(r"""
    (?:
        [Dd]ue\s+(?P<cardinal>North|South|East|West)
    |
        (?P<ns>[NS])\.?\s*
        (?P<deg>\d{1,3})\s*(?:deg\.?|\u00B0|°)\s*
        (?:(?P<min>\d{1,2})\s*(?:['′]\s*)?)?
        (?:(?P<sec>\d{1,2}(?:\.\d+)?)\s*(?:["″]\s*)?)?
        (?P<ew>[EW])\.?
    |
        (?P<deg_only>\d{1,3})\s*(?:deg\.?|\u00B0|°)\s*
        (?:(?P<min_only>\d{1,2})\s*(?:['′]\s*)?)?
        (?P<ew_only>[EW])\.?
    )
""", re.IGNORECASE | re.VERBOSE)
```

**Azimuth conversion from quadrant bearing:**

```python
def bearing_to_azimuth(ns: str, deg: float, min: float, sec: float, ew: str) -> float:
    """Convert quadrant bearing to azimuth (0-360, clockwise from North)."""
    angle = deg + min / 60.0 + sec / 3600.0

    if ns == 'N' and ew == 'E':
        return angle               # NE quadrant: 0-90
    elif ns == 'S' and ew == 'E':
        return 180.0 - angle       # SE quadrant: 90-180
    elif ns == 'S' and ew == 'W':
        return 180.0 + angle       # SW quadrant: 180-270
    elif ns == 'N' and ew == 'W':
        return 360.0 - angle       # NW quadrant: 270-360
```

**Due-cardinal bearings:**

| Text | Azimuth |
|------|---------|
| Due North | 0° |
| Due East | 90° |
| Due South | 180° |
| Due West | 270° |

#### 2.3.6 Traverse Legs

```python
LEG_RE = re.compile(r"""
    (?:thence\s+)?
    (?P<bearing>
        [Dd]ue\s+(?:North|South|East|West)
        |
        [NS]\.?\s*\d{1,3}\s*(?:deg\.?|°)\s*(?:\d{1,2}\s*['′]\s*)?(?:\d{1,2}(?:\.\d+)?\s*["″]\s*)?[EW]\.?
    )
    \s*,?\s*
    (?P<distance>[\d,.]+)\s*(?:m\.?|meters?|metres?)
    \s*(?:to\s+(?:the\s+)?(?P<to_point>point\s*(?:of\s+beginning|["'"]?\d+["'"]?)|
                              the\s+point\s+of\s+beginning|
                              the\s+starting\s+point|
                              the\s+place\s+of\s+beginning|
                              point\s+["'"]?1["'"]?\s*,?\s*point\s+of\s+beginning))?
""", re.IGNORECASE | re.VERBOSE)
```

**Closing leg detection:**

```python
CLOSING_PHRASES = [
    r'to\s+the\s+point\s+of\s+beginning',
    r'to\s+point\s+of\s+beginning',
    r'to\s+point\s+\d+\s*,?\s*point\s+of\s+beginning',
    r'to\s+the\s+starting\s+point',
    r'to\s+point\s+1\s*$',
    r'to\s+the\s+place\s+of\s+beginning',
]
```

#### 2.3.7 Area Statement

```python
AREA_WORDS_RE = re.compile(
    r'containing\s+an\s+area\s+of\s+'
    r'(?P<words>[A-Z][A-Z\s,\-]+?)\s*'
    r'\(\s*(?P<number>[\d,.]+)\s*\)\s*'
    r'(?:SQUARE\s+METERS?|SQ\.?\s*M\.?)',
    re.IGNORECASE
)

AREA_SIMPLE_RE = re.compile(
    r'(?:containing\s+)?(?:an\s+)?area\s+of\s+'
    r'(?P<number>[\d,.]+)\s*'
    r'(?:square\s+met(?:er|re)s?|sq\.?\s*m\.?)',
    re.IGNORECASE
)
```

**Area number parsing:** Remove commas, replace comma-as-decimal with period, parse as float. When both spelled-out words and parenthetical numeral are present, prefer the numeral.

#### 2.3.8 Footer

```python
FOOTER_RE = re.compile(r"""
    [Bb]earings?\s*:?\s*
    (?P<bearing_type>true|grid|magnetic)\s*
    (?:;\s*declination\s+(?P<declination>[^;.]+))?\s*
    (?:;\s*date\s+of\s+(?:original\s+)?survey\s*:?\s*(?:was\s+)?(?P<orig_date>[^;.]+))?
    (?:;\s*(?:date\s+of\s+)?(?:that\s+of\s+)?(?:the\s+)?
        (?:subdivision|consolidation|consolidation-subdivision)\s+survey\s*:?\s*
        (?P<sub_date>[^;.]+))?
""", re.IGNORECASE | re.VERBOSE)
```

#### 2.3.9 Coordinate-Based TD Detection

Some modern TDs provide direct geographic coordinates per corner (no traverse):

```python
COORD_CORNER_RE = re.compile(r"""
    Corner\s+(\d+)\s+at\s+
    (\d+)[°]\s*(\d+)[′']\s*(\d+(?:\.\d+)?)[″"]\s*([NS])\s*,?\s*
    (\d+)[°]\s*(\d+)[′']\s*(\d+(?:\.\d+)?)[″"]\s*([EW])
""", re.IGNORECASE | re.VERBOSE)
```

If `TIE_BLOCK_RE` fails and `COORD_CORNER_RE` matches, the TD is coordinate-based and bypasses the traverse pipeline entirely.

#### 2.3.10 Distance Parsing

```python
def parse_distance(raw: str) -> float:
    """Parse distance string to meters."""
    s = raw.strip().rstrip('.')
    s = s.replace(' ', '')
    # Handle comma as thousands separator vs decimal
    # Philippine convention: comma = thousands (e.g., "4,317.52")
    # European convention: comma = decimal (e.g., "936,15")
    if ',' in s and '.' in s:
        s = s.replace(',', '')       # "4,317.52" -> "4317.52"
    elif ',' in s:
        # Ambiguous: "936,15" could be decimal comma
        # Heuristic: if exactly 2 digits after comma, treat as decimal
        parts = s.split(',')
        if len(parts) == 2 and len(parts[1]) <= 2:
            s = s.replace(',', '.')  # decimal comma
        else:
            s = s.replace(',', '')   # thousands separator
    return float(s)
```

### 2.4 Format Variations

All survey types (Psd, Csd, Pcs, Ccs, Psu, PLS, Cad, FP, H, Bsd, etc.) use the same canonical TD format. The differences are metadata only — the bearing/distance traverse, tie point, and computational pipeline are structurally identical.

Key findings:
- **Subdivision TDs** always reference a geodetic monument (BLLM/BBM) as tie point, NOT parent lot corners
- **Consolidation TDs** describe the outer boundary only; internal boundaries dissolved
- **LRC-prefixed plans** `(LRC) Psd-NNNNNNN` have no format difference from regular Psd
- **Reconstituted titles** may have degraded data (missing prefix/suffix, transposed digits) — handled via error codes
- **Graphical-origin TDs** (from `Cadm`/`PCadm` surveys) have lower precision distances

---

## 3. Stage 2: BLLM Resolution

### 3.1 Purpose

Resolve the tie point monument name from the parsed TD to absolute PRS92 grid coordinates (Northing, Easting, Zone).

### 3.2 Data Source

The primary BLLM dataset is derived from the Title Plotter PH QGIS plugin's `tiepoints.json` file (GitHub: `isaacenage/TitlePlotterPH`).

**Dataset structure (actual `tiepoints.json` field names):**

| Field | Description | Example |
|-------|-------------|---------|
| Tie Point Name | Monument short name | `"BLLM 1"` |
| Description | Monument full description (used for datum inference) | `"BLLM No. 1, Cad 614-D, Municipality of Botolan, Province of Zambales"` |
| Northing | PRS92 grid Northing (m) | `1691760.514` |
| Easting | PRS92 grid Easting (m) | `394854.244` |
| Province | Province name (ALL CAPS) | `"ZAMBALES"` |
| Municipality | Municipality name (ALL CAPS) | `"BOTOLAN"` |

**Coverage statistics (from analysis):**
- **85,303 total records** across 117 provinces (15.9 MB JSON file)
- Record types: 19,568 BLLMs, 26,155 BBMs, 15,609 PRS92 control points, 9,174 MBMs, 4,850 BLBMs, 1,085 triangulation stations, 788 PBMs, ~8,074 other
- Datum inference from Description field: 18.4% PRS92, 66% Luzon 1911, 15.5% unknown
- Strongest coverage: NCR, Region III, Region IV-A, Region VII (Iloilo 4,618 records, Pangasinan 4,363)
- Weakest coverage: BARMM, CAR, MIMAROPA, post-2006 provinces
- 2,907 records have null Municipality

### 3.3 Lookup Algorithm

Five-tier progressive matching:

```
Tier 1: Exact normalized name match
  Normalize input: strip periods, collapse whitespace, uppercase
  "BLLM NO. 1, PLS-1110" → exact match in "Tie Point Name" or "Description" field

Tier 2: Monument code + number only (drop descriptor)
  "BLLM 1" → match across all records with monument type BLLM, number 1

Tier 3: Monument code + number + province filter
  "BLLM 1" + province "ILOCOS SUR" → filtered match

Tier 4: Trigram similarity (threshold >= 0.6)
  Handles typos: "BLM 1" → "BLLM 1" (similarity 0.75)

Tier 5: Caller-provided coordinates
  Bypass database entirely; accept (N, E, zone, datum) from caller
```

### 3.4 Zone Inference from BLLM

When the BLLM record includes a province, use the province-to-zone mapping (Appendix C) to determine the PRS92 zone. This is the primary method of zone determination.

### 3.5 Datum of BLLM Coordinates

The `tiepoints.json` dataset stores coordinates as PRS92 grid values. For Luzon 1911-era titles tied to these PRS92 BLLMs, the engine computes the traverse in PRS92 and flags a datum mismatch warning. The relative corner positions are accurate; absolute position has ~7-13m uncertainty due to the datum mixing.

---

## 4. Stage 3: Traverse Computation

### 4.1 Overview

Given a starting point (Corner 1, from BLLM + tie line) and a sequence of bearing/distance pairs, compute PRS92 grid coordinates for every corner of the lot polygon.

### 4.2 Corner 1 Computation (Tie Line)

```
Corner1_N = BLLM_N + tie_distance × cos(tie_azimuth_rad)
Corner1_E = BLLM_E + tie_distance × sin(tie_azimuth_rad)
```

Where `tie_azimuth_rad = radians(tie_azimuth_deg)`.

### 4.3 Subsequent Corners (Polar to Rectangular)

For each leg `i` (from corner `i` to corner `i+1`):

```
azimuth_rad = radians(legs[i].azimuth_deg)

ΔN_i = distance_i × cos(azimuth_rad)
ΔE_i = distance_i × sin(azimuth_rad)

Corner(i+1)_N = Corner(i)_N + ΔN_i
Corner(i+1)_E = Corner(i)_E + ΔE_i
```

This is a plane (grid) traverse. No curvature correction is needed for the lot sizes encountered in Philippine titles (typically < 50 ha). The PRS92 grid distortion at Philippine latitudes is < 1 ppm for distances up to several km from the central meridian.

### 4.4 Closure Computation

After computing all corners, the misclosure is the gap between the last computed point and Corner 1:

```
eN = Corner(last+1)_N - Corner1_N    (residual in Northing)
eE = Corner(last+1)_E - Corner1_E    (residual in Easting)
e  = sqrt(eN² + eE²)                 (linear misclosure, metres)

perimeter = sum of all leg distances
precision_ratio = perimeter / e       (e.g., 1:13,061)
```

### 4.5 Area Computation (Shoelace Formula)

```python
def shoelace_area(corners: list[tuple[float, float]]) -> float:
    """
    Compute polygon area using the shoelace formula.
    corners: list of (N, E) tuples, in traverse order, closed polygon.

    IMPORTANT: Shift coordinates before summation to avoid
    catastrophic cancellation with large PRS92 values.
    """
    n = len(corners)
    # Shift to local origin
    n_min = min(c[0] for c in corners)
    e_min = min(c[1] for c in corners)
    shifted = [(c[0] - n_min, c[1] - e_min) for c in corners]

    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += shifted[i][0] * shifted[j][1]
        area -= shifted[j][0] * shifted[i][1]
    return abs(area) / 2.0
```

**Critical implementation note:** PRS92 Northing values are ~1,000,000-2,200,000 m. Without the coordinate shift, the cross-products in the shoelace formula lose ~7 significant digits, making area unreliable for small lots. Always shift to a local origin first.

### 4.6 Worked Example

**Input:** Sample 1 (TV-1) — Lot 1, PLS-1110, Alilem, Ilocos Sur

BLLM coordinates (PRS92 Zone 3): N = 1,882,450.000 m, E = 447,320.000 m

**Tie line:** Az = 114.967°, dist = 348.29 m
- ΔN = 348.29 × cos(114.967° × π/180) = -147.010 m
- ΔE = 348.29 × sin(114.967° × π/180) = +315.744 m
- Corner 1: N = 1,882,302.990, E = 447,635.744

**Leg 1→2:** Az = 282.300°, dist = 16.41 m
- ΔN = 16.41 × cos(282.3° × π/180) = +3.496 m
- ΔE = 16.41 × sin(282.3° × π/180) = -16.033 m
- Corner 2: N = 1,882,306.486, E = 447,619.710

**Leg 2→3:** Az = 10.450°, dist = 30.59 m
- ΔN = +30.083 m, ΔE = +5.548 m
- Corner 3: N = 1,882,336.568, E = 447,625.259

**Leg 3→4:** Az = 110.183°, dist = 16.76 m
- ΔN = -5.783 m, ΔE = +15.731 m
- Corner 4: N = 1,882,330.786, E = 447,640.989

**Leg 4→1 (closing):** Az = 190.700°, dist = 28.29 m
- ΔN = -27.798 m, ΔE = -5.253 m
- Computed return: N = 1,882,302.988, E = 447,635.737

**Closure:** eN = -0.002 m, eE = -0.007 m, e = 0.007 m
- Precision = 92.05 / 0.007 = 1:13,061 → **PASS**

**Area:** Shoelace = 484.65 m², Stated = 485.0 m², Discrepancy = 0.07% → **PASS**

---

## 5. Stage 4: Datum Transformation

### 5.1 Overview

Two transformation paths exist depending on the title's datum era:

```
Path A (PRS92 titles, post-1993):
  PRS92 N/E → inverse TM (Clarke 1866) → PRS92 geographic → Helmert → WGS84

Path B (Luzon 1911 titles, pre-1993):
  Option 1: If BLLM is PRS92 → compute traverse in PRS92 → Path A
  Option 2: If BLLM is Luzon 1911 → compute in Luzon 1911 → 3-param shift to WGS84
```

### 5.2 Datum Detection

The engine determines which datum the title uses:

```python
def detect_datum(survey_year: int | None, bearing_type: str,
                 plan_prefix: str, explicit_datum: str | None) -> str:
    """
    Returns: "PRS92", "Luzon1911", or "ambiguous"
    """
    if explicit_datum:
        return explicit_datum

    if survey_year:
        if survey_year >= 2006:
            return "PRS92"       # post-DENR MC 2010-06 transition
        elif survey_year <= 1992:
            return "Luzon1911"   # pre-PRS92 adoption
        else:
            return "ambiguous"   # 1993-2005 transition era

    # Fallback heuristics
    if bearing_type == "grid":
        return "ambiguous"       # grid bearings used in both eras
    elif bearing_type == "true":
        return "Luzon1911"       # true bearings more common pre-PRS92

    return "ambiguous"
```

For ambiguous cases (1993-2005), default to PRS92 with a `DatumAmbiguous` warning.

### 5.3 PRS92 Zone Parameters

All five zones share these projection parameters:

| Parameter | Value |
|-----------|-------|
| Ellipsoid | Clarke 1866 |
| Semi-major axis (a) | 6,378,206.4 m |
| Semi-minor axis (b) | 6,356,583.8 m |
| First eccentricity squared (e²) | 0.006768657997 |
| Second eccentricity squared (e'²) | 0.006814784945 |
| Scale factor (k₀) | 0.99995 |
| False Easting (E₀) | 500,000 m |
| False Northing (N₀) | 0 m |
| Latitude of origin | 0° (Equator) |

| Zone | EPSG | Central Meridian |
|------|------|-----------------|
| 1 | 3121 | 117°E |
| 2 | 3122 | 119°E |
| 3 | 3123 | 121°E |
| 4 | 3124 | 123°E |
| 5 | 3125 | 125°E |

**Zone selection cascade:**

```
1. Caller-provided zone → use directly
2. BLLM database record → province → province-zone lookup
3. TD location clause → parse province → province-zone lookup
4. Survey plan region code → region-zone mapping (approximate)
5. Easting value range check (sanity only)
6. Give up → ZoneUnknown error
```

### 5.4 Inverse Transverse Mercator (PRS92 N/E → Geographic)

Converts PRS92 projected coordinates to geographic coordinates on the Clarke 1866 ellipsoid.

**Method:** Snyder/Redfearn series expansion (USGS PP1395, Chapter 8). Non-iterative, 6th-order in normalized easting. Sub-millimetre accuracy within PTM zone widths.

#### Stage 1: Meridional Arc Distance

```
x = Easting - 500000          (remove false easting)
y = Northing - 0              (remove false northing; N₀ = 0)
M = y / k₀ = y / 0.99995     (eq. 8-20)
```

**CRITICAL:** The formula is `M = y / k₀`, NOT `M = y`. Omitting the k₀ divisor causes ~94 m latitude error at typical Philippine northings. Verified by round-trip tests.

#### Stage 2: Footpoint Latitude

Derived constants for Clarke 1866:

```
e1 = (1 - sqrt(1 - e²)) / (1 + sqrt(1 - e²)) = 0.001697916

A0 = 1 - e²/4 - 3e⁴/64 - 5e⁶/256 = 0.9983056819

J1 = 3e1/2 - 27e1³/32      = 0.002546870
J2 = 21e1²/16 - 55e1⁴/32   = 0.000003784
J3 = 151e1³/96              = 0.000000008
J4 = 1097e1⁴/512            ≈ 0 (negligible)
```

Compute:

```
μ = M / (a × A0)                                      (eq. 7-19)
φ₁ = μ + J1·sin(2μ) + J2·sin(4μ) + J3·sin(6μ) + J4·sin(8μ)   (eq. 3-26)
```

#### Stage 3: Auxiliary Quantities at Footpoint

```
T1 = tan²(φ₁)                                         (eq. 8-22)
C1 = e'² × cos²(φ₁)                                   (eq. 8-21)
N1 = a / sqrt(1 - e² × sin²(φ₁))                      (eq. 8-23)
R1 = a(1 - e²) / (1 - e² × sin²(φ₁))^(3/2)           (eq. 8-24)
D  = x / (N1 × k₀)                                    (eq. 8-25)
```

#### Stage 4: Geographic Coordinates

**Latitude (eq. 8-17):**

```
φ = φ₁ - (N1 × tan(φ₁) / R1) × [
    D²/2
  - (5 + 3T1 + 10C1 - 4C1² - 9e'²) × D⁴/24
  + (61 + 90T1 + 298C1 + 45T1² - 252e'² - 3C1²) × D⁶/720
]
```

**Longitude (eq. 8-18):**

```
λ = λ₀ + [
    D
  - (1 + 2T1 + C1) × D³/6
  + (5 - 2C1 + 28T1 - 3C1² + 8e'² + 24T1²) × D⁵/120
] / cos(φ₁)
```

Where λ₀ is the central meridian of the zone (in radians).

#### Complete Implementation

```python
import math

def inverse_tm(easting: float, northing: float, zone_cm_deg: float,
               a: float = 6378206.4, e2: float = 0.006768657997,
               k0: float = 0.99995, fe: float = 500000.0) -> tuple[float, float]:
    """
    Inverse Transverse Mercator: PRS92 N/E → geographic (φ,λ) on Clarke 1866.

    Returns: (latitude_deg, longitude_deg)
    """
    ep2 = e2 / (1.0 - e2)
    e1 = (1.0 - math.sqrt(1.0 - e2)) / (1.0 + math.sqrt(1.0 - e2))

    e4 = e2 * e2
    e6 = e4 * e2
    A0 = 1.0 - e2/4.0 - 3.0*e4/64.0 - 5.0*e6/256.0

    e1_2 = e1 * e1
    e1_3 = e1_2 * e1
    e1_4 = e1_3 * e1
    J1 = 3.0*e1/2.0 - 27.0*e1_3/32.0
    J2 = 21.0*e1_2/16.0 - 55.0*e1_4/32.0
    J3 = 151.0*e1_3/96.0
    J4 = 1097.0*e1_4/512.0

    lam0 = math.radians(zone_cm_deg)

    x = easting - fe
    y = northing  # fn = 0

    M = y / k0

    mu = M / (a * A0)
    phi1 = (mu + J1 * math.sin(2*mu) + J2 * math.sin(4*mu)
            + J3 * math.sin(6*mu) + J4 * math.sin(8*mu))

    sin_phi1 = math.sin(phi1)
    cos_phi1 = math.cos(phi1)
    tan_phi1 = math.tan(phi1)

    T1 = tan_phi1 * tan_phi1
    C1 = ep2 * cos_phi1 * cos_phi1
    N1 = a / math.sqrt(1.0 - e2 * sin_phi1 * sin_phi1)
    R1 = a * (1.0 - e2) / (1.0 - e2 * sin_phi1 * sin_phi1)**1.5
    D = x / (N1 * k0)

    D2, D3, D4, D5, D6 = D*D, D**3, D**4, D**5, D**6

    phi = phi1 - (N1 * tan_phi1 / R1) * (
        D2/2.0
        - (5.0 + 3.0*T1 + 10.0*C1 - 4.0*C1*C1 - 9.0*ep2) * D4/24.0
        + (61.0 + 90.0*T1 + 298.0*C1 + 45.0*T1*T1
           - 252.0*ep2 - 3.0*C1*C1) * D6/720.0
    )

    lam = lam0 + (
        D - (1.0 + 2.0*T1 + C1) * D3/6.0
        + (5.0 - 2.0*C1 + 28.0*T1 - 3.0*C1*C1
           + 8.0*ep2 + 24.0*T1*T1) * D5/120.0
    ) / cos_phi1

    return math.degrees(phi), math.degrees(lam)
```

### 5.5 PRS92 → WGS84 Helmert Transformation

**EPSG:15708** — 7-parameter Helmert, **Coordinate Frame rotation** convention (EPSG method 9607):

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| X translation | dx | -127.62 | metres |
| Y translation | dy | -67.24 | metres |
| Z translation | dz | -47.04 | metres |
| X rotation | rx | +3.068 | arc-seconds |
| Y rotation | ry | -4.903 | arc-seconds |
| Z rotation | rz | -1.578 | arc-seconds |
| Scale | ds | -1.06 | ppm |

**Accuracy:** 0.05 m (EPSG stated)

**Pipeline:**

1. **Geographic → Geocentric** (Clarke 1866):

```python
def geographic_to_geocentric(phi_rad, lam_rad, h=0.0,
                              a=6378206.4, e2=0.006768657997):
    """Clarke 1866 geographic → geocentric cartesian (X,Y,Z)."""
    sin_phi = math.sin(phi_rad)
    cos_phi = math.cos(phi_rad)
    N = a / math.sqrt(1.0 - e2 * sin_phi * sin_phi)

    X = (N + h) * cos_phi * math.cos(lam_rad)
    Y = (N + h) * cos_phi * math.sin(lam_rad)
    Z = (N * (1.0 - e2) + h) * sin_phi
    return X, Y, Z
```

2. **Apply Helmert** (Coordinate Frame rotation):

```python
def helmert_cf(X, Y, Z,
               dx=-127.62, dy=-67.24, dz=-47.04,
               rx_as=3.068, ry_as=-4.903, rz_as=-1.578,
               ds_ppm=-1.06):
    """7-parameter Helmert, Coordinate Frame rotation convention."""
    # Convert rotation from arc-seconds to radians
    rx = rx_as * math.pi / (180 * 3600)
    ry = ry_as * math.pi / (180 * 3600)
    rz = rz_as * math.pi / (180 * 3600)
    s = 1.0 + ds_ppm * 1e-6

    Xw = dx + s * ( X     + rz*Y  - ry*Z)
    Yw = dy + s * (-rz*X  + Y     + rx*Z)
    Zw = dz + s * ( ry*X  - rx*Y  + Z   )
    return Xw, Yw, Zw
```

3. **Geocentric → Geographic** (WGS84, Bowring iterative):

```python
def geocentric_to_geographic(X, Y, Z,
                              a=6378137.0,      # WGS84
                              e2=0.00669437999014):
    """WGS84 geocentric cartesian → geographic (lat, lon in radians)."""
    lam = math.atan2(Y, X)

    p = math.sqrt(X*X + Y*Y)
    # Bowring initial approximation (parametric latitude)
    b = a * math.sqrt(1.0 - e2)
    theta = math.atan2(Z * a, p * b)

    phi = math.atan2(
        Z + (e2 * a * a / b) * math.sin(theta)**3,
        p - e2 * a * math.cos(theta)**3
    )

    # One iteration for sub-mm accuracy
    N = a / math.sqrt(1.0 - e2 * math.sin(phi)**2)
    phi = math.atan2(Z + e2 * N * math.sin(phi), p)

    return phi, lam  # radians
```

**Sign Convention Warning:** EPSG:15708 uses Coordinate Frame rotation. Position Vector convention negates all three rotations. Using the wrong convention causes ~0.1-0.3m error.

### 5.6 Luzon 1911 → WGS84 Transformation

For pre-1993 titles on the Luzon 1911 datum:

**Path A (Global 3-parameter, recommended):**

EPSG:1161 (Luzon 1911 Luzon → WGS84):
- dx = -133, dy = -77, dz = -51 (metres)
- Accuracy: ~25 m

EPSG:1162 (Luzon 1911 Visayas/Mindanao → WGS84):
- dx = -133, dy = -79, dz = -72 (metres)
- Accuracy: ~25 m

**Selection:** Use EPSG:1161 for Luzon island, EPSG:1162 for Visayas/Mindanao. The island is determined from the TD location clause.

**Path B (DENR MC 2010-06 conformal, higher accuracy):**

Per DENR MC 2010-06, a conformal transformation with 4 parameters per zone provides ~2-5m accuracy. However, the specific parameters are not available in the public domain. If the caller provides DENR MC 2010-06 zone-specific parameters, the engine should use them. Otherwise, fall back to Path A.

**Practical note:** When the BLLM coordinates are stored as PRS92 (which is the case for the Title Plotter PH dataset), and the title is Luzon 1911, the engine computes the traverse in PRS92 and applies the PRS92→WGS84 pipeline (Section 5.5). The datum mismatch is flagged as a warning. Absolute accuracy is ~7-13m; relative corner positions within the lot are accurate.

### 5.7 Luzon 1911 PTM Zone Mapping

Luzon 1911 used Philippine Transverse Mercator (PTM) zones with the same structure as PRS92 but different naming:

| Luzon 1911 | PRS92 | Central Meridian |
|------------|-------|-----------------|
| PTM Zone I | PRS92 Zone 1 | 117°E |
| PTM Zone II | PRS92 Zone 2 | 119°E |
| PTM Zone III | PRS92 Zone 3 | 121°E |
| PTM Zone IV | PRS92 Zone 4 | 123°E |
| PTM Zone V | PRS92 Zone 5 | 125°E |

Same Clarke 1866 ellipsoid, same projection parameters (k₀, E₀, N₀). Only the datum differs.

---

## 6. Stage 5: Validation

### 6.1 Linear Closure

| Precision Ratio | Status | Interpretation |
|-----------------|--------|----------------|
| ≥ 1:5,000 | PASS | Normal for well-surveyed lots |
| 1:3,000 – 1:5,000 | WARN | Acceptable for older/rural surveys |
| 1:1,000 – 1:3,000 | FLAG | Poor closure; possible parsing error |
| < 1:1,000 | FAIL | Catastrophic; traverse does not close |

**Relaxed thresholds:** For graphical-origin surveys (detected by `Cadm`/`PCadm` prefix or conversion note), use 1:1,000 as the PASS threshold.

**Short-perimeter edge case:** For lots with perimeter < 100 m, precision ratios are sensitive to rounding. If absolute misclosure e < 0.05 m and k ≥ 1,000, override to PASS regardless of ratio. Always include both the ratio (1:k) and the absolute misclosure (e in metres) in output.

### 6.2 Area Cross-Check

Compare computed shoelace area against stated area:

| Discrepancy | Status | Interpretation |
|-------------|--------|----------------|
| ≤ 0.5% | PASS | Normal rounding |
| 0.5% – 2% | WARN | Acceptable for older surveys |
| 2% – 5% | FLAG | Possible missing leg or wrong bearing |
| > 5% | FAIL | Likely parsing error |

**Small-lot absolute floor:** For lots with stated area < 100 m², if the absolute difference is ≤ 1 m², override to PASS regardless of percentage (avoids false flags from percentage amplification on tiny lots).

### 6.3 Angular Closure

For n-sided polygon, theoretical angular sum = (n - 2) × 180°.

**Interior angle computation from sequential azimuths:**

```python
def compute_interior_angles(azimuths_deg: list[float]) -> list[float]:
    """
    Compute interior angles from sequential traverse azimuths.
    azimuths_deg: list of azimuth for each leg, in traverse order.
    Returns: list of interior angles in degrees (one per corner).
    """
    n = len(azimuths_deg)
    angles = []
    for i in range(n):
        incoming_az = azimuths_deg[(i - 1) % n]
        outgoing_az = azimuths_deg[i]
        angle = incoming_az - outgoing_az + 180.0
        angle = angle % 360.0  # normalize to [0, 360)
        angles.append(angle)
    return angles
```

**Angular misclosure:**

```
θ_measured = sum(interior_angles)
θ_theoretical = (n - 2) × 180°
angular_misclosure = |θ_measured - θ_theoretical|   (in arc-seconds for comparison)
```

| Angular Error | Status |
|--------------|--------|
| ≤ 30″√n | PASS |
| 30″√n – 60″√n | WARN |
| 60″√n – 120″√n | FLAG |
| > 120″√n | FAIL |

Where n is the number of corners. Note: since the engine computes angles from the same bearings used for the traverse, angular closure is primarily a cross-check for parsing errors (e.g., flipped quadrant), missing legs, or concave polygon detection (any interior angle > 180°).

### 6.4 Geometry Sanity

- **Self-intersection test:** O(n²) edge-pair intersection check. If non-adjacent edges intersect → `SelfIntersection` ERROR
- **Area bounds:** Computed area < 1 m² → WARNING (possible unit error); > 10,000,000 m² (1,000 ha) → WARNING (unusual, verify)
- **Philippine territory check:** WGS84 lat outside 4°-21°N or lon outside 116°-128°E → `CoordinateClampWarning`

### 6.5 Validation Output Schema

```json
{
  "closure": {
    "eN_m": -0.002,
    "eE_m": -0.007,
    "e_m": 0.007,
    "perimeter_m": 92.05,
    "precision_denom": 13061,
    "status": "pass",
    "threshold_used": "1:5000"
  },
  "area_check": {
    "computed_sqm": 484.65,
    "stated_sqm": 485.0,
    "discrepancy_pct": 0.072,
    "status": "pass",
    "threshold_used": "0.5%"
  },
  "angular_closure": {
    "computed_sum_deg": 360.003,
    "expected_sum_deg": 360.0,
    "error_arcsec": 10.8,
    "threshold_arcsec": 60.0,
    "status": "pass"
  },
  "geometry": {
    "self_intersecting": false,
    "winding": "clockwise",
    "corner_count": 4
  },
  "overall_status": "pass"
}
```

---

## 7. Error Handling

### 7.1 Design Principles

- **Accumulate, never throw.** Errors are collected in a list; the pipeline continues as far as possible.
- **Never auto-correct silently.** All recoveries are logged with the original value and the recovery method.
- **Deterministic.** Same input always produces same output, same errors in same order.

### 7.2 Severity Levels

| Level | Effect |
|-------|--------|
| FATAL | Pipeline halts at this stage; return partial results |
| ERROR | Stage output unreliable; continue with caveat |
| WARNING | Possible issue; output likely usable |
| INFO | Non-standard input handled successfully |

### 7.3 Error Code Registry (42 codes)

#### Parse Stage

| Code | Severity | Description |
|------|----------|-------------|
| `InputEmpty` | FATAL | TD text is empty/null |
| `InputTooShort` | WARNING | TD text < 50 characters |
| `EncodingNonUTF8` | WARNING | Non-UTF8 bytes detected |
| `ControlCharacters` | INFO | Control characters stripped |
| `TieBlockNotFound` | FATAL* | No "Beginning at a point" pattern (*triggers coordinate-based check) |
| `TieDistanceMissing` | ERROR | Tie point named but distance absent |
| `TieMonumentUnparseable` | ERROR | Monument reference doesn't match patterns |
| `BearingMissingPrefix` | WARNING | No N/S before degrees |
| `BearingMissingSuffix` | WARNING | No E/W after minutes |
| `BearingUnparseable` | ERROR | Neither prefix nor suffix found |
| `BearingOutOfRange` | WARNING | Degrees > 90 for quadrant bearing |
| `BearingMinutesOutOfRange` | WARNING | Minutes > 59 |
| `BearingSecondsDetected` | INFO | Non-standard seconds in bearing |
| `DueCardinalAmbiguous` | WARNING | Cardinal direction without "Due" prefix |
| `DistanceZero` | ERROR | Distance = 0 |
| `DistanceMissing` | ERROR | No distance after bearing |
| `DistanceUnreasonable` | WARNING | Distance > 50,000 m |
| `DistanceNegative` | ERROR | Negative distance parsed |
| `DistanceDecimalComma` | INFO | Comma as decimal separator |
| `MissingClosingLeg` | ERROR | No "point of beginning" destination |
| `MissingCorners` | WARNING | Gap in corner numbering |
| `DuplicateCorner` | WARNING | Same corner number twice |
| `NoLegsFound` | FATAL | Zero traverse legs extracted |
| `SingleLeg` | ERROR | Only 1 leg (can't form polygon) |
| `TwoLegs` | ERROR | Only 2 legs (degenerate polygon) |
| `AreaNotFound` | WARNING | No area statement matched |
| `AreaWordsNumMismatch` | WARNING | Spelled area ≠ numeral area |
| `AreaZero` | ERROR | Parsed area = 0 |
| `FooterNotFound` | WARNING | No footer detected |
| `BearingTypeUnknown` | WARNING | Bearing type not "true" or "grid" |
| `SurveyDateUnparseable` | INFO | Date text can't be parsed to year |
| `SurveyPlanUnparseable` | INFO | Plan number doesn't match regex |

#### BLLM Stage

| Code | Severity | Description |
|------|----------|-------------|
| `BLLMNotFound` | FATAL* | Monument not in database (*allows relative polygon) |
| `AmbiguousBLLM` | ERROR | Multiple matches after filtering |
| `BLLMDatumMismatch` | WARNING | BLLM datum ≠ title datum |
| `BLLMCoordinateInvalid` | ERROR | Non-numeric/impossible coordinates |
| `BLLMZoneInferFailed` | ERROR | Province not in zone mapping |
| `BLLMMonumentTypeUnsupported` | WARNING | Non-BLLM type with sparse DB coverage |

#### Traverse Stage

| Code | Severity | Description |
|------|----------|-------------|
| `TraverseOverflow` | FATAL | Coordinate exceeds valid PRS92 range |
| `ClosureFail` | ERROR | Precision < 1:1,000 |
| `ClosureWarn` | WARNING | Precision 1:3,000 – 1:5,000 |
| `AreaDiscrepancyFail` | ERROR | Area discrepancy > 5% |
| `SelfIntersection` | ERROR | Polygon edges cross |
| `DegeneratePolygon` | ERROR | All corners collinear |

#### Transform Stage

| Code | Severity | Description |
|------|----------|-------------|
| `DatumAmbiguous` | WARNING | 1993-2005 survey, no explicit datum |
| `ZoneUnknown` | ERROR | Cannot determine PRS92 zone |
| `ZoneBoundaryAmbiguous` | WARNING | Province straddles two zones |
| `HelmertParamConflict` | ERROR | Parameter sources disagree |
| `Luzon1911PathBFailed` | WARNING | DENR MC 2010-06 params gave unreasonable result |
| `EllipsoidalHeightMissing` | INFO | No h provided; using h=0 |
| `InverseTMConvergenceFail` | FATAL | Inverse TM didn't converge |

#### Output Stage

| Code | Severity | Description |
|------|----------|-------------|
| `PartialResult` | INFO | Some stages succeeded, not all |
| `CoordinateClampWarning` | WARNING | WGS84 outside Philippine bounds |

### 7.4 Confidence Scoring

```python
def compute_confidence(errors: list[dict]) -> dict:
    score = 1.0
    for err in errors:
        if err["severity"] == "FATAL":
            return {"confidence": "unusable", "score": 0.0}
        elif err["severity"] == "ERROR":
            score -= 0.3
        elif err["severity"] == "WARNING":
            score -= 0.1

    score = max(0.0, score)
    if score >= 0.8:   confidence = "high"
    elif score >= 0.5: confidence = "medium"
    elif score >= 0.2: confidence = "low"
    else:              confidence = "unusable"

    return {"confidence": confidence, "score": round(score, 2)}
```

### 7.5 Closure Failure Diagnostics

When closure fails, provide hints:

```python
def diagnose_closure(eN, eE, legs):
    e = math.sqrt(eN**2 + eE**2)
    hints = []

    # Predominant direction suggests quadrant flip
    if abs(eN) > 0.8 * e:
        hints.append("Misclosure predominantly N/S — check N↔S quadrant error")
    if abs(eE) > 0.8 * e:
        hints.append("Misclosure predominantly E/W — check E↔W quadrant error")

    # Check if flipping any single leg's quadrant fixes closure
    for i, leg in enumerate(legs):
        az_rad = math.radians(leg["azimuth_deg"])
        dN = leg["distance_m"] * math.cos(az_rad)
        dE = leg["distance_m"] * math.sin(az_rad)
        residual = math.sqrt((eN + 2*dN)**2 + (eE + 2*dE)**2)
        if residual < 0.1 * e:
            hints.append(f"Flipping leg {i+1} direction improves closure")

    return hints
```

### 7.6 Error Output Schema

```json
{
  "code": "BearingMissingPrefix",
  "severity": "WARNING",
  "stage": "parse",
  "leg_index": 0,
  "field": "tie_bearing",
  "message": "Tie bearing '50 deg. 50' E.' missing N/S prefix",
  "raw_value": "50 deg. 50' E.",
  "recovery_applied": true,
  "recovery_method": "Assumed 'N' prefix",
  "recovered_value": "N. 50 deg. 50' E.",
  "alternatives": [{"value": "S. 50 deg. 50' E.", "azimuth": 129.167}]
}
```

---

## 8. Test Vectors

### TV-1: Full Pipeline — PLS-1110, Alilem, Ilocos Sur

**Input:**
```
A parcel of land (Lot 1, PLS-1110, Alilem Public Land Subdivision), situated in Alilem,
Ilocos Sur, Island of Luzon. Bounded on the S. along line 1-2 by Guis-it St. (10.00 m.
wide); on the W. along line 2-3 by Lot-167, PLS-1110; on the N. along line 3-4 by Lot-164,
PLS-1110; and on the E. along line 4-1 by Lot-2 of the consolidation and subd. plan.

Beginning at a point marked "1" of Lot-1 on plan, being S. 65° 02' E., 348.29 m. from BLLM
No. 1, PLS-1110, Alilem Public Land Subd., thence N. 77° 42' W., 16.41 m. to point 2;
thence N. 10° 27' E., 30.59 m. to point 3; thence S. 69° 49' E., 16.76 m. to point 4;
thence S. 10° 42' W., 28.29 m. to point 1, point of beginning, containing an area of FOUR
HUNDRED EIGHTY FIVE (485) SQUARE METERS.

All points referred to are indicated on the plan and were marked on the ground with BL cyl.
conc. mons. 15x40 cms.
Bearings: Grid; date of original survey was April-May, 1983.
```

**BLLM (hypothetical, PRS92 Zone 3):** N = 1,882,450.000 m, E = 447,320.000 m

**Expected corners (PRS92 Zone 3):**

| Corner | Northing (m) | Easting (m) |
|--------|-------------|------------|
| 1 | 1,882,302.990 | 447,635.744 |
| 2 | 1,882,306.486 | 447,619.710 |
| 3 | 1,882,336.568 | 447,625.259 |
| 4 | 1,882,330.786 | 447,640.989 |

**Expected WGS84:**

| Corner | Latitude | Longitude |
|--------|----------|-----------|
| 1 | 17.017654819° | 120.509491642° |
| 2 | 17.017686040° | 120.509340976° |
| 3 | 17.017957993° | 120.509392369° |
| 4 | 17.017906101° | 120.509540248° |

**Validation:** Closure 1:13,061 PASS. Area 484.65 vs 485.0 m² (0.07%) PASS.

---

### TV-2: Full Pipeline — Mr-1018-D, Malabon, Rizal (Luzon 1911 era)

**Input:**
```
Beginning at a point marked "1" on plan, being S. 44° 36' W., 90.02 meters from B.L.L.M. 1,
municipality of Malabon, Rizal, thence N. 68° 44' E., 5.81 meters to point 2; thence S. 23°
11' E., 32.85 meters to point 3; thence S. 23° 11' E., 47.00 meters to point 4; thence S.
23° 34' E., 15.33 meters to point 5; thence S. 22° 59' E., 17.24 meters to point 6; thence
S. 61° 37' W., 5.99 meters to point 7; thence N. 23° 08' W., 113.14 meters to the point of
beginning, containing an area of 664 square meters, more or less.

All points referred to are indicated on the plan and are marked on the ground.
Bearings true; declination 0° 56' E.; date of survey, May 15, 1950 and that of the approval,
January 17, 1951.
```

**BLLM (hypothetical, PRS92 Zone 3):** N = 1,620,500.000, E = 501,200.000

**Key tests:**
- `B.L.L.M.` with periods → normalizes to BLLM
- True bearings, 1950 survey → Luzon 1911 datum
- 7 corners (heptagon)
- Two legs share identical bearing (S 23° 11' E)

**Validation:** Closure 1:9,789 PASS. Area 663.52 vs 664.0 m² (0.07%) PASS.
**Datum note:** BLLM is PRS92, title is Luzon 1911 → `BLLMDatumMismatch` warning. Absolute accuracy ~7-13m.

---

### TV-3: Full Pipeline + Due North — Psu-02-001767, Peñablanca, Cagayan

**Input:**
```
A parcel of land (Lot No. 1, Plan Psu-(af)-02-001767) situated in Barangay Patagueleg,
Municipality of Peñablanca, Province of Cagayan, Island of Luzon.

Beginning at a point marked "1" on plan, being N. 11 deg. 05' W., 4,317.52 m. from BLLM.
No. 1, Pls-793; thence S. 36 deg. 43' E., 98.73 m. to point 2; thence S. 83 deg. 12' E.,
519.94 m. to point 3; thence S. 83 deg. 16' E., 196.00 m. to point 4; thence S. 00 deg. 06'
W., 5.55 m. to point 5; thence N. 83 deg. 04' W., 247.07 m. to point 6; thence N. 83 deg.
04' W., 236.00 m. to point 7; thence N. 83 deg. 04' W., 239.99 m. to point 8; thence N. 35
deg. 56' W., 94.00 m. to point 9; thence N. 80 deg. 13' W., 180.26 m. to point 10; thence
Due North 5.64 m. to point 11; thence S. 80 deg. 27' E., 183.16 m. to point of beginning,
containing an area of FOUR THOUSAND NINE HUNDRED TWENTY-SIX (4,926) SQUARE METERS, more or
less.

Bearings true; date of survey 01 March 2011.
```

**BLLM (hypothetical, PRS92 Zone 3):** N = 1,990,000.000, E = 480,000.000

**Key tests:**
- `Due North` bearing → azimuth 0°
- Near-zero bearing: S 00° 06' W → azimuth 180.1°
- Three consecutive identical bearings (N 83° 04' W)
- Long tie line (4,317.52 m)
- 11 corners
- `Psu-(af)-02-001767` plan number with qualifier and region code

**Validation:** Closure 1:47,063 PASS. Area 4,924.13 vs 4,926.0 m² (0.04%) PASS.

---

### TV-4: Error Detection — Psd-55969, Angeles, Pampanga

**Input:**
```
Beginning at a point marked "1" on plan, being S. 29° 48' E., 393.43 m. from B.B2. No. 42,
Angeles Cadastro, thence S. 9° 35' E., 27.99 m. to point "2"; thence S. 45° 36' W., 16.95
m. to point "3"; thence S. 86° 15' W., 5.95 m. to point "4"; thence N. 51° W., 24.01 m. to
point "5"; thence N. 45° 07' E., 21.99 m. to the point of beginning.

Bearings true; date of original survey: January-July, 1916; date of subdivision survey:
July 15-18, 1958.
```

**Key tests:**
- `B.B2.` monument type (non-BLLM) → likely `BLLMNotFound`
- Degrees-only bearing: `N. 51° W.` (no minutes)
- Quoted corner numbers: `point "2"`
- Pre-1993 dates → Luzon 1911

**Expected result:** Closure 1:5 **FAIL**. The traverse does not close. Engine should:
1. Parse successfully
2. Compute traverse (relative polygon)
3. Detect catastrophic closure failure
4. Report diagnostic hints
5. Set degradation level 3 (relative polygon)

---

### TV-5: Inverse TM Round-Trip Verification

Synthetic test points across multiple zones. All use Clarke 1866 ellipsoid.

| ID | Zone | CM | Input φ (°) | Input λ (°) | Forward N (m) | Forward E (m) | Round-trip error |
|----|------|----|------------|------------|---------------|---------------|-----------------|
| A | 3 | 121° | 17.020000 | 120.510000 | 1,882,377.500 | 447,828.825 | < 0.05 mm |
| B | 3 | 121° | 18.030000 | 120.805000 | 1,994,093.279 | 479,352.725 | < 0.05 mm |
| C | 5 | 125° | 11.178000 | 124.960000 | 1,236,016.792 | 495,631.306 | < 0.03 mm |
| D | 4 | 123° | 10.310000 | 123.890000 | 1,140,150.584 | 597,485.123 | < 0.03 mm |

---

### TV-6: Bearing Parser Unit Tests

| ID | Input | Expected Azimuth (°) | Format |
|----|-------|---------------------|--------|
| B1 | `S. 65° 02' E.` | 114.966667 | Standard |
| B2 | `N. 11 deg. 05' W.` | 348.916667 | Spelled degrees |
| B3 | `N. 51° W.` | 309.000000 | No minutes |
| B4 | `Due North` | 0.000000 | Cardinal |
| B5 | `Due West` | 270.000000 | Cardinal |
| B6 | `S. 00 deg. 06' W.` | 180.100000 | Near-zero |
| B7 | `N. 83 deg. 04' W.` | 276.933333 | NW bearing |
| B8 | `S. 80 deg. 27' E.` | 99.550000 | Near 90° |
| B9 | `N 77° 42' W` | 282.300000 | No periods |

**Error cases:**

| ID | Input | Error Code |
|----|-------|------------|
| E1 | `50 deg. 50' E.` | BearingMissingPrefix |
| E2 | `N. 22 deg. 40'` | BearingMissingSuffix |
| E3 | `S. 95° 10' W.` | BearingOutOfRange |

---

## Appendix A: Ellipsoid & Projection Constants

### Clarke 1866 (PRS92 and Luzon 1911)

| Constant | Value |
|----------|-------|
| Semi-major axis (a) | 6,378,206.4 m |
| Semi-minor axis (b) | 6,356,583.8 m |
| Inverse flattening (1/f) | 294.978698213898 |
| First eccentricity squared (e²) | 0.006768657997 |
| Second eccentricity squared (e'²) | 0.006814784945 |
| e1 = (1-√(1-e²))/(1+√(1-e²)) | 0.001697916 |

### WGS84

| Constant | Value |
|----------|-------|
| Semi-major axis (a) | 6,378,137.0 m |
| Semi-minor axis (b) | 6,356,752.314245 m |
| Inverse flattening (1/f) | 298.257223563 |
| First eccentricity squared (e²) | 0.00669437999014 |

### PRS92 Transverse Mercator

| Parameter | Value |
|-----------|-------|
| Scale factor (k₀) | 0.99995 |
| False Easting | 500,000 m |
| False Northing | 0 m |
| Latitude of origin | 0° (Equator) |

### Inverse TM Derived Constants (Clarke 1866)

| Constant | Value |
|----------|-------|
| A0 | 0.9983056819 |
| J1 | 0.002546870 |
| J2 | 0.000003784 |
| J3 | 0.000000008 |
| J4 | ≈ 0 |

### Helmert Parameters (EPSG:15708, Coordinate Frame)

| Parameter | Value | Unit |
|-----------|-------|------|
| dx | -127.62 | m |
| dy | -67.24 | m |
| dz | -47.04 | m |
| rx | +3.068 | arc-seconds |
| ry | -4.903 | arc-seconds |
| rz | -1.578 | arc-seconds |
| ds | -1.06 | ppm |

### Luzon 1911 → WGS84 (3-parameter)

| Region | dx | dy | dz | EPSG |
|--------|----|----|----|----|
| Luzon | -133 | -77 | -51 | 1161 |
| Visayas/Mindanao | -133 | -79 | -72 | 1162 |

---

## Appendix B: Survey Plan Prefix Registry

| Prefix | Type | Region Code? | Notes |
|--------|------|-------------|-------|
| Psd | Private Subdivision | Yes (new) / No (old) | Most common subdivision type |
| (LRC) Psd | LRC-approved Subdivision | No | Higher sequential numbers |
| Csd | Cadastral Subdivision | Yes | Untitled parent lot |
| Bsd | Bureau Subdivision | Yes | Government-conducted |
| Psu | Private Survey (original) | Yes | Judicial titling |
| PLS/Pls | Public Land Subdivision | No | Original survey |
| Cad | Cadastral Survey | No | Original cadastral |
| Cadm | Cadastral Mapping | No | Graphical, lower precision |
| PCadm | Photo-Cadastral Mapping | No | Graphical from aerial photo |
| Mr | Municipal Registration | No | — |
| Bp | Bureau of Lands Plan | No | — |
| FP | Free Patent | Yes (newer) | Agricultural/residential |
| H | Homestead Patent | No | Agricultural |
| Ccs | Consolidation Survey | Yes | Merge only |
| Pcs | Consolidation-Subdivision | Yes | Merge + re-subdivide |
| Mcs | — | — | — |
| Ts | Townsite Survey | Yes | — |
| Ms | Miscellaneous Sales | No | Residential sales patent |
| Gss | Group Settlement Subdivision | No | Settler colonies |
| Ap | Advanced Plan | No | Rare |

**Qualifiers:** `(af)` = as-found, `(ct)` = court-titled, `(if)` = in-force
**Suffixes:** `(AR)` = Agrarian Reform (CARP-related)

---

## Appendix C: Province-to-Zone Mapping

### Zone 1 (CM 117°E) — EPSG:3121
Palawan (western portion)

### Zone 2 (CM 119°E) — EPSG:3122
Palawan (eastern portion), Calamian Islands, Busuanga

### Zone 3 (CM 121°E) — EPSG:3123
**NCR:** Metro Manila
**Region I:** Ilocos Norte, Ilocos Sur, La Union, Pangasinan
**Region II:** Batanes, Cagayan, Isabela (western municipalities), Nueva Vizcaya, Quirino
**Region III:** Aurora, Bataan, Bulacan, Nueva Ecija, Pampanga, Tarlac, Zambales
**Region IV-A:** Batangas, Cavite, Laguna, Rizal, Quezon
**Region IV-B:** Marinduque, Mindoro Occidental, Mindoro Oriental, Romblon
**CAR:** Abra, Apayao, Benguet, Ifugao, Kalinga, Mountain Province

### Zone 4 (CM 123°E) — EPSG:3124
**Region II:** Isabela (eastern municipalities)
**Region V:** Albay, Camarines Norte, Camarines Sur, Catanduanes, Masbate, Sorsogon
**Region VI:** Aklan, Antique, Capiz, Guimaras, Iloilo, Negros Occidental
**Region VII:** Cebu, Negros Oriental, Siquijor, Bohol (western)
**Region IX:** Zamboanga del Norte, Zamboanga del Sur, Zamboanga Sibugay
**Region X:** Bukidnon, Lanao del Norte, Misamis Occidental, Misamis Oriental, Camiguin
**BARMM:** Lanao del Sur, Maguindanao, Basilan, Sulu, Tawi-Tawi

### Zone 5 (CM 125°E) — EPSG:3125
**Region VII:** Bohol (eastern)
**Region VIII:** Biliran, Eastern Samar, Leyte, Northern Samar, Samar, Southern Leyte
**Region X:** (eastern edge)
**Region XI:** Davao del Norte, Davao del Sur, Davao Oriental, Davao de Oro, Davao Occidental
**Region XII:** Cotabato, Sarangani, South Cotabato, Sultan Kudarat
**Region XIII:** Agusan del Norte, Agusan del Sur, Dinagat Islands, Surigao del Norte, Surigao del Sur

**Note:** Some provinces straddle zone boundaries (e.g., Isabela, Bohol). For these, municipality-level resolution is needed. When municipality is unknown, return `ZoneBoundaryAmbiguous` warning with both candidate zones.

---

## Appendix D: BLLM Dataset Reference

### Data Source

Primary: Title Plotter PH QGIS plugin (`tiepoints.json`)
- GitHub: `isaacenage/TitlePlotterPH`
- File: `resources/tiepoints.json` (15.9 MB, 85,303 records)
- Coordinates: PRS92 grid (Northing, Easting)
- Fields: `Tie Point Name`, `Description`, `Northing`, `Easting`, `Province`, `Municipality`

Supplementary: Geoportal Philippines Lot Plotter (embedded BLLM database)
- Web application with BLLM lookup functionality
- Coverage overlaps with but may extend beyond tiepoints.json

### Coverage Gaps

The BLLM database has uneven coverage:

| Coverage Level | Regions |
|---------------|---------|
| Good (many records) | NCR, Region III, Region IV-A, Region VII |
| Moderate | Region I, Region II, Region V, Region VIII |
| Sparse | CAR, MIMAROPA, Region IX, BARMM |

### Monument Types in Dataset

| Type | Count | Notes |
|------|-------|-------|
| BBM (Barangay Boundary Monument) | 26,155 | Largest category |
| BLLM (Bureau of Lands Location Monument) | 19,568 | Primary tie point type |
| PRS92 Control Points | 15,609 | Explicit PRS92 datum |
| MBM (Municipal Boundary Monument) | 9,174 | — |
| BLBM (Bureau of Lands Barrio Monument) | 4,850 | — |
| General Monuments (MON) | 1,372 | — |
| Triangulation Stations (TS) | 1,085 | C&GS stations |
| PBM (Provincial Boundary Monument) | 788 | — |
| Other (P-points, misc) | 6,702 | — |

### Data Quality Notes

- Some records may have transcription errors in coordinates
- GeoIDEx-sourced cross-reference points showed data quality issues (duplicate northings for distinct monuments)
- When multiple records match the same monument name, use the one from the same province/municipality as the TD's location clause
- If coordinates produce traverses with closure > 1:100, the BLLM record itself may be erroneous

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-26 | Initial complete spec assembled from 14 analysis iterations |
| 1.1 | 2026-02-26 | Spec review fixes: corrected BLLM dataset counts (85,303 records, not ~1,200), fixed JSON field names to match tiepoints.json, removed dead code in Bowring function, added angular closure computation formula, added short-perimeter and small-lot edge case thresholds, updated TV-1 WGS84 to full precision |

## Source Analyses

This spec was assembled from the following analyses (in `analysis/`):

| Wave | Analysis | Content |
|------|----------|---------|
| 1 | prs92-datum-parameters | Ellipsoid constants, zone definitions, Helmert params |
| 1 | luzon1911-transformation | Legacy datum parameters, DENR MC 2010-06 |
| 1 | tech-description-samples | 8-sample corpus spanning vintages and regions |
| 1 | bllm-database-sources | BLLM data source inventory |
| 1 | traverse-computation-references | Geodetic traverse methods |
| 2 | text-parser-grammar | BNF grammar, regex patterns, output schema |
| 2 | traverse-algorithm | Formulas, worked example, closure computation |
| 2 | prs92-to-wgs84-transform | Full inverse TM + Helmert pipeline |
| 2 | inverse-tm-formulas | Snyder/Redfearn and EPSG Krueger methods |
| 2 | luzon1911-to-prs92-transform | Datum detection, transformation paths |
| 2 | bllm-dataset-compilation | Dataset extraction, coverage analysis |
| 2 | validation-rules | Tolerance thresholds, validation output schema |
| 3 | format-variations | Survey types, reconstituted titles, edge cases |
| 3 | error-handling | 42 error codes, severity levels, diagnostics |
| 3 | test-vectors | 6 test vectors with computed coordinates |
