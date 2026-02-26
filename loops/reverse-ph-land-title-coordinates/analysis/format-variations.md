# Format Variations — Philippine Land Title Technical Descriptions

**Aspect:** format-variations (Wave 3)
**Date:** 2026-02-26
**Depends on:** tech-description-samples, text-parser-grammar, traverse-algorithm, validation-rules (Waves 1–2)
**Sources:** CREBA, DENR DAO 98-12, DAO 2007-29, DMC 2010-06, DMC 2010-13, RA 26, RA 6732, RA 10023, Supreme Court E-Library, cadastraltemplate.org, LMB eSurveyPlan Manual, Geoportal Lot Plotter, TitlePlotterPH source

---

## Overview

This document catalogs all known format variations in Philippine land title technical descriptions beyond those already covered in the Wave 1 corpus analysis (`tech-description-samples.md`) and Wave 2 parser grammar (`text-parser-grammar.md`). It focuses on structural differences across survey types, plan approval pathways, datum eras, and title issuance methods — and their implications for the parser.

---

## 1. Subdivision Plans (Psd, Csd) vs. Original Survey Plans

### 1.1 Original Survey Plans

Original surveys — **Psu** (Private Survey, Upland), **PLS/Pls** (Public Land Subdivision), **Cad** (Cadastral), **FP** (Free Patent), **H** (Homestead) — are the first surveys ever conducted on a parcel. They create the initial lot boundary and generate the **Original Certificate of Title (OCT)**.

**Key TD characteristics of original surveys:**
- Tie point is always a **primary monument** (BLLM, BBM, MBM, or other Bureau of Lands control point)
- Tie line runs directly from the monument to Corner 1
- All bearing/distance data comes from the **original ground survey**
- Lot number is simple (e.g., "Lot 1, PLS-1110" or "Lot 9755, Cad. 407")
- No parent lot reference
- Footer references only one survey date

**Example (Sample 1 — original survey):**
```
A parcel of land (Lot 1, PLS-1110, Alilem Public Land Subdivision), situated in Alilem, Ilocos Sur...
Beginning at a point marked "1" on plan, being S. 65° 02' E., 348.29 m. from BLLM No. 1, PLS-1110...
Bearings: Grid; date of original survey was April–May, 1983.
```

### 1.2 Private Subdivision Plans (Psd)

A **Psd** is a subdivision of already-titled land. It divides a parent ("mother") lot into child lots. All Psd surveys are conducted by private geodetic engineers.

**Key TD characteristics of subdivision lots:**
- Lot identification includes **"being a portion of" clause** referencing the parent lot
- Lot number is compound, reflecting the subdivision hierarchy (e.g., "Lot 457-A-12-B-2-B-2-A")
- Tie point is **still a primary monument** (BLLM or equivalent) — NOT a parent lot corner
- The tie line references the same BLLM network as the parent survey
- Footer references **two survey dates**: "date of original survey" AND "that of the subdivision survey"
- Boundary descriptions reference sibling lots and road lots within the same subdivision

**Example (Sample 2 — subdivision):**
```
A parcel of land (Lot 28, Block 7 of the subdivision plan Psd-55969, being a portion of Lot 653-3
described on plan Bp-10253, L.R.C. Cad. Rec. No. 224)...
Beginning at a point marked "1" on plan, being S. 29° 48' E., 393.43 m. from B.B2. No. 42, Angeles Cadastro...
Bearings true; date of original survey: January–July, 1916; date of subdivision survey: July 15–18, 1958.
```

**Critical parser finding:** The tie point in a subdivision lot TD references a geodetic monument, NOT the parent lot's Corner 1. The parser does not need special handling for "parent lot corner references" as tie points. The "being a portion of" clause is metadata only — it does not affect the computational pipeline.

### 1.3 Cadastral Subdivision Plans (Csd)

A **Csd** is a subdivision of a cadastral lot that is not yet titled. The distinction from Psd:
- **Psd** = subdivision of titled land
- **Csd** = subdivision of untitled cadastral lot

**TD format difference:** The lot identification references the parent cadastral survey and may append a suffix letter to the plan number (e.g., "Csd-03-012562-D" where "-D" distinguishes the cadastral subdivision from the parent cadastral lot).

**Example (Sample 7):**
```
Csd-03-012562-D (Cadastral Subdivision, Region 03)
Cad. 652-D, Masinloc Cadastre
Beginning at a point marked "1" on plan being N. 39 deg. 35' E., 12.05 m. from BLLM.1, Cad. 652-D...
Bearings true; date of original survey: Sept. 1927–July 1928, and that of the subdivision survey: July 22, 1999.
```

**Parser implication:** The `-D` suffix on plan numbers should be captured but does not affect computation. The Csd lot structure is otherwise identical to Psd.

### 1.4 Bureau of Lands Subdivision (Bsd)

A **Bsd** is a subdivision of government-titled land conducted by a government geodetic engineer. If a private titled land is surveyed by a government engineer through court order, the result is also a Bsd.

**TD format:** Structurally identical to Psd. The only difference is the plan prefix `Bsd-` instead of `Psd-`. No bearing/distance format changes.

### 1.5 Parser Implications for Subdivision vs. Original Survey

| Feature | Original Survey | Subdivision (Psd/Csd/Bsd) |
|---------|----------------|---------------------------|
| "being a portion of" | Absent | Present |
| Lot number complexity | Simple (Lot N) | Compound (Lot N-A-B-C-D) |
| Tie point type | BLLM or equivalent | BLLM or equivalent (same) |
| Footer survey dates | One date | Two dates (original + subdivision) |
| Plan number prefix | Psu, PLS, Cad, FP, H | Psd, Csd, Bsd |
| Bearing/distance format | Standard | Standard (no difference) |
| Computational pipeline | Standard | Standard (no difference) |

**Conclusion:** The parser does NOT need a separate code path for subdivision vs. original survey TDs. The bearing/distance data, tie point, and traverse computation are structurally identical. The only differences are in metadata fields (lot identification, parent lot reference, survey dates).

---

## 2. Consolidation Plans (Ccs, Pcs)

### 2.1 What They Are

A **consolidation plan** merges two or more titled parcels into a single larger parcel. A **consolidation-subdivision plan** (designated **Pcs** or **Ccs**) merges multiple parcels and then subdivides the merged parcel into new lots.

Survey plan prefix meanings:
- **Ccs** — Consolidation survey (merge only)
- **Pcs** — Consolidation-Subdivision plan (merge then re-subdivide)

### 2.2 TD Format

The consolidation/consolidation-subdivision TD follows the **same structural format** as other TDs:

```
A parcel of land (Lot 8 of the consolidation-subdivision plan Pcs-11-000142,
being a portion of Lots 1, 2 and 3, all of Pcs-11-000102, and Lot 3, of Pcs-11-000083, LRC Cad.)...
Beginning at a point marked "1" on plan, being S. 54 deg. 42' W., 615.49 m. from BBM No. 15, Tagum Cad-276...
```

**Key TD characteristics:**
- The "being a portion of" clause references **multiple parent lots** (e.g., "Lots 1, 2 and 3, all of Pcs-11-000102, and Lot 3, of Pcs-11-000083")
- The tie point is a geodetic monument (BBM, BLLM, etc.) — same as any other TD
- The traverse describes the **outer boundary** of the consolidated parcel (or the new subdivided child lot), NOT the internal boundaries between the original parcels
- Bearings and distances follow standard format
- Footer references two dates: original survey + consolidation(-subdivision) survey
- Monument markers may include "Old PS" (pre-existing monuments from parent lots) alongside new "PS cyl. conc. mons."

**Example (Sample 8 — consolidation):**
```
Beginning at a point marked "1" on plan, being S. 05 deg. 58' W., 3,123.14 m. from BLLM No. 1, Makar;
thence [5 corners, bearings, distances]...
Bearings: True. Date of original survey: 20-11 July 1962; consolidation survey: 07 October 2015.
```

### 2.3 How the Traverse is Described

The traverse in a consolidation plan describes **the outer boundary of the resulting lot only**. The surveyor:
1. Establishes control from PRS92 reference monuments
2. Traverses the outer perimeter of the consolidated parcel
3. Computes bearings and distances for each boundary line
4. Reports closure error (must be <= 1:10,000 per DENR standards)

Internal boundaries (where the original parcels met) are **NOT described** in the resulting TD — they are dissolved.

### 2.4 Parser Implications

| Feature | Standard TD | Consolidation TD |
|---------|-----------|-----------------|
| Lot identification | "being a portion of [one lot]" | "being a portion of [multiple lots]" |
| "being a portion of" clause | References one parent | References multiple parents |
| Tie point | BLLM/BBM | BLLM/BBM (same) |
| Traverse | Outer boundary | Outer boundary (same) |
| Bearing/distance format | Standard | Standard (no difference) |
| Footer dates | Original + subdivision | Original + consolidation |
| Monuments | PS cyl. conc. mons. | May mix "Old PS" + new PS |

**Conclusion:** The parser needs **no special handling** for consolidation TDs. The "being a portion of" clause regex should already handle multiple lot references (it's metadata). The computational pipeline is identical.

**Regex update for lot identification to handle multiple parent lots:**
The existing lot identification regex should handle this via the general `<parent-lot>` capture, but should be tested against patterns like:
```
being a portion of Lots 1, 2 and 3, all of Pcs-11-000102, and Lot 3, of Pcs-11-000083
```

---

## 3. Old-Format vs. New-Format Survey Plan Numbers

### 3.1 The Transition

Philippine survey plan numbers underwent a format change from **centralized numbering** (no region code) to **regionalized numbering** (with 2-digit region code):

| Format | Example | Era | Approving Authority |
|--------|---------|-----|-------------------|
| Old (no region code) | Psd-55969 | Pre-~1998 | Central (Manila) — LRC/LRA or BL/DENR |
| New (with region code) | Psd-04-222222 | Post-~1998 | Regional — DENR-LMS Regional Office |

The region code is a **2-digit DENR administrative region number** (01–17, plus NCR, CAR, BARMM codes):
- 01 = Region I (Ilocos)
- 02 = Region II (Cagayan Valley)
- 03 = Region III (Central Luzon)
- 04 = Region IV-A (CALABARZON)
- ... etc.

### 3.2 When Did the Transition Happen?

The transition was formalized by **DAO 98-12** (1998 Revised Manual of Land Surveying Regulations), which devolved survey approval from central offices to regional offices and required region codes in plan numbers to prevent duplication. The region code was introduced specifically so that "a particular [survey] number shall pertain to a particular municipality/city in the country" and prevent number collisions when surveys were approved at the regional level.

**Practical timeline:**
- Pre-1998: Old format universal (e.g., Psd-55969, (LRC) Psd-2114428)
- 1998–~2002: Transition period — both formats coexist
- Post-~2002: New format standard for DENR-approved plans (e.g., Psd-04-222222, Csd-03-012562-D)
- LRC-approved plans continued the old format longer because LRA used its own numbering

### 3.3 Bearing/Datum Implications

**There is NO bearing or datum implication from the plan number format itself.** The plan number format change was purely administrative (preventing number collisions across regions). The datum used (Luzon 1911 vs. PRS92) depends on:
1. The survey date (pre/post 1993)
2. The explicit datum declaration on the plan (if any)

However, the **region code is useful metadata** for:
- Inferring the PRS92/PTM zone (region code maps to provinces, which map to zones)
- Validating that the province in the location clause matches the expected region

### 3.4 Parser Implications

The existing `SURVEY_PLAN_RE` regex in `text-parser-grammar.md` already handles both formats:
```
(Psd|Psu|Csd|Cad|...)
(?:-\(af\)|-\(ct\)|-\(if\))?   # optional qualifier
-?(\d{2})?                       # optional region code (2 digits)
[-–]?(\d+)                       # sequence number
([A-Z])?                         # optional suffix letter
```

**Enhancement:** When a region code is present, extract it and use it for:
1. Zone inference validation (cross-check with province → zone mapping)
2. Datum-era inference (if region-coded, likely post-1998, but not necessarily PRS92)

**New survey plan regex field in output schema:**
```json
{
  "survey_plan": {
    "raw": "Psd-04-222222",
    "prefix": "Psd",
    "qualifier": null,
    "region_code": "04",
    "sequence": "222222",
    "suffix": null,
    "lrc_prefix": false
  }
}
```

---

## 4. LRC-Approved Plans: (LRC) Psd

### 4.1 What is LRC?

The **Land Registration Commission (LRC)** was the agency responsible for land registration in the Philippines from 1954 (RA 1151) until its reorganization. Its lineage:
- **1903:** Court of Land Registration (established)
- **1936:** General Land Registration Office (GLRO)
- **1954:** Land Registration Commission (LRC) — created by RA 1151
- **1978:** National Land Titles and Deeds Registration Administration (NALTDRA) — PD 1529
- **Present:** Land Registration Authority (LRA) — now under DOTC/DOJ

### 4.2 (LRC) Psd vs. Regular Psd

When a plan number is preceded by **(LRC)**, it means the subdivision plan was **approved by the LRC (now LRA)**, rather than by DENR. This typically applies to subdivision plans of registered land under the Torrens system.

| Feature | (LRC) Psd | Regular Psd |
|---------|----------|-------------|
| Approving authority | LRA (formerly LRC) | DENR-LMS |
| Numbering | Sequential, no region code: (LRC) Psd-2114428 | Region-coded: Psd-04-222222 |
| Land type | Already-registered Torrens land | Any titled land |
| TD format | **Identical** | **Identical** |
| Where to request copy | LRA Subdivision & Consolidation Division | DENR Regional Office |

### 4.3 TD Format Differences

**There is NO structural difference in the technical description format between (LRC) Psd and regular Psd plans.** The TD follows the same canonical structure:
- Lot identification with "being a portion of" clause
- Tie point (BLLM or equivalent)
- Bearing/distance traverse
- Area statement
- Footer with bearing type and survey dates

**Example (Sample 4 — LRC plan):**
```
A parcel of land (Lot 457-A-12-B-2-B-2-A of the subdivision plan (LRC) Psd-2114428,
being a portion of Lot 457-A-12-B-2-B-2 (LRC) Psd-1774344 L.R.C. Record No. 3563)...
Beginning at a point marked "1" on plan, being 50 deg. 50' E., 457.01 m. from L.W. 22, Piedad Estate...
```

### 4.4 Parser Implications

The "(LRC)" prefix must be handled as an optional element in the lot identification regex. The existing `SURVEY_PLAN_RE` already includes `(?:\(LRC\)\s*)?` as an optional prefix.

**Additional consideration:** LRC plan numbers typically have **no region code** and use higher sequential numbers (6-7 digits). The parser should not require a region code when `(LRC)` prefix is detected.

**L.R.C. Record reference:** Many (LRC) Psd plans include an `L.R.C. Record No.` or `L.R.C. Cad. Rec. No.` reference. This is metadata (a land registration case number) and does not affect computation. The parser should capture it but not require it.

---

## 5. Reconstituted Titles

### 5.1 What They Are

A **reconstituted title** is a replacement certificate of title issued when the original was lost or destroyed (fire, flood, war, theft). The reconstitution process is governed by:
- **RA 26** (1946) — judicial reconstitution
- **RA 6732** (1989) — administrative reconstitution

### 5.2 TD Format in Reconstituted Titles

The legal standard requires that the reconstituted title **reproduce the original in the same form**. Per Supreme Court jurisprudence, "reconstitution denotes a restoration of the instrument which is supposed to have been lost or destroyed in its original form or condition."

**In theory:** The TD in a reconstituted title should be byte-for-byte identical to the original.

**In practice:** Reconstituted titles commonly suffer from:

1. **Transcription errors:** When the TD is recopied from secondary sources (owner's duplicate, co-owner's duplicate, tax declarations, court records), typographical errors are introduced. Common errors include:
   - Swapped bearing directions (W vs. E, N vs. S)
   - Transposed digits in bearings or distances
   - Missing corners (entire traverse legs omitted)
   - Truncated area statements

2. **Incomplete technical descriptions:** Per RA 26 Section 6, "in all cases where the reconstituted certificate of title does not contain the full technical description of the land, except where such technical description is contained in a prior certificate of title which is available, the registered owner shall, within two years from the date of the reconstitution, file a plan of such land." This means some reconstituted titles may have **partial or missing TDs**.

3. **Section 7 annotation:** Reconstituted titles carry a Section 7 encumbrance warning that annotations from the original may not have been carried over. While this doesn't directly affect the TD format, it signals that the title was reconstructed from secondary sources.

4. **Source degradation chain:** The reconstitution sources, in order of reliability (per RA 26 Section 2/3), are:
   - (a) Owner's duplicate certificate of title
   - (b) Co-owner's, mortgagee's, or lessee's duplicate
   - (c) Certified copy from the LRA
   - (d) An authenticated copy of the decree of registration
   - (e) A document or instrument previously issued to the owner
   - (f) Any other document the court deems sufficient

   Sources (d)–(f) are most prone to TD degradation because they may be handwritten notes, secondary transcriptions, or partial records.

### 5.3 Known Degradation Patterns

| Degradation Type | Example | Parser Impact |
|-----------------|---------|---------------|
| Missing N/S or E/W | "50 deg. 50' E." (Sample 4) | `BearingMissingPrefix` / `BearingMissingSuffix` warning |
| Truncated corner sequence | Legs jump from "point 3" to "point 7" | `MissingCorners` error — gap detection in corner numbering |
| Missing tie point | No "Beginning at a point" clause | `TieBlockNotFound` error |
| Missing tie line distance | "being N. 45° 30' E. from BLLM No. 1" (distance omitted) | `TieDistanceMissing` error — new error code |
| Garbled monument reference | "BLM No. 1" instead of "BLLM No. 1" | Monument normalization handles via fuzzy match |
| Missing area statement | TD ends abruptly after last corner | `AreaNotFound` error |
| Duplicate/conflicting bearings | Same corner described twice with different values | New: `DuplicateCorner` warning |

### 5.4 Parser Implications

1. **Reconstituted titles are more likely to trigger parser errors/warnings** than original titles. The parser should track the number of errors per TD and report an overall confidence score.

2. **New error codes needed:**
   - `TieDistanceMissing` — tie point named but no distance given
   - `MissingCorners` — gap in sequential corner numbering
   - `DuplicateCorner` — same corner number appears twice

3. **No special code path:** The parser does not need to detect whether a title is reconstituted. It should handle all format degradation gracefully via the existing error/warning system.

4. **Recommendation:** When multiple errors are detected in a single TD, the parser should flag the output with a `source_quality: "low"` metadata field and note "possible reconstituted or re-transcribed title."

---

## 6. Free Patent and Homestead Patent Titles

### 6.1 Survey Plan Types

| Patent Type | Survey Prefix | Land Type | Max Area | Approving Authority |
|-------------|--------------|-----------|----------|-------------------|
| Free Patent (agricultural) | FP | Agricultural public land | 5 ha (12 ha under CA 141) | DENR (administrative) |
| Free Patent (residential) | FP or Psu | Residential public land | varies | DENR (RA 10023) |
| Homestead Patent | H | Agricultural public land | 24 ha | DENR (administrative) |

### 6.2 TD Format

**The technical description in a Free Patent or Homestead Patent OCT uses exactly the same metes-and-bounds format as any other Philippine land title.** There is no structural difference.

The TD includes:
- Lot identification (Lot N, FP-NNNNN or H-NNNNN)
- Tie point (BLLM) and tie line (bearing + distance to Corner 1)
- Bearing/distance traverse
- Area statement
- Footer (bearing type, survey date)

**The only difference is in the title document itself, not the TD:**
- An OCT issued via patent shows the patent number and governing law (e.g., "Free Patent No. 04-2021-001234, RA 10023")
- The title form is **Judicial Form No. 108-D** (OCT) vs. **109-D** (TCT)
- The Administrator + Registrar both sign OCTs; only the Registrar signs TCTs

### 6.3 Potential Precision Differences

Free patent surveys (FP) cover agricultural land, often in rural or remote areas. In practice, these surveys may have:
- **Longer tie lines** (the nearest BLLM may be far from rural agricultural parcels)
- **Lower precision** in older surveys (pre-GPS era, transit and tape measurements)
- **Larger lot areas** (up to 5-24 ha vs. typical residential lots of 200-500 sqm), meaning more corners and longer perimeters

However, these are **practical considerations, not format differences**. The TD format is identical.

### 6.4 Parser Implications

**No parser changes needed for free patent / homestead patent TDs.** The parser should:
1. Recognize `FP-NNNNN` and `H-NNNNN` as valid survey plan prefixes (add to `SURVEY_PLAN_RE`)
2. Handle potentially larger coordinate values (longer distances, more corners)
3. Apply rural tolerance thresholds (1:3,000 per engine convention vs. 1:5,000 urban) — already covered in `validation-rules.md`

**Survey plan prefix additions to SURVEY_PLAN_RE:**
```
FP    # Free Patent
H     # Homestead Patent
```

---

## 7. Graphical vs. Numerical Technical Descriptions

### 7.1 Background

The Philippines historically used two cadastral survey methods:

**Numerical Cadastre (Cad):**
- Bearings and distances computed from **actual ground survey**
- Lot corners directly observed (transit, EDM, later GPS)
- Area computed mathematically (to hundredths of a meter)
- Produces a full metes-and-bounds TD with precise numerical data

**Graphical Cadastre (Cadm/PCadm):**
- Survey control executed on ground, but lot corners determined by **plane table and alidade** or **transit and stadia**
- Distances derived by **scaling from maps**
- Area determined by **planimeter or graphical estimation**
- Produces lot shape descriptions but with lower-precision distances
- Discontinued in the **late 1970s**

### 7.2 Conversion from Graphical to Numerical

**Conversion surveys** are conducted to transform lots from approved graphical cadastral surveys into numerical cadastral lots. Per DENR MC 2010-06 and MC 2010-13:

1. **Resurvey required:** "Lot data computations for cadastral survey projects under the graphical cadastre system shall be generated after a resurvey of the affected lots have been conducted."
2. **PRS92 compliance:** "The new survey shall already be PRS92-compliant and referenced to existing PRS92 control points."
3. **Digital conversion:** The resulting lot data computation is converted for incorporation into the digital cadastral database.

**Sample 6 reference:** The Cad. 407 Palo, Leyte lot (surveyed 1972, graphical) has the note: "Conversion computation into numerical technical description was approved May 22, 1984."

### 7.3 Format Differences

| Feature | Graphical TD (pre-conversion) | Numerical TD (post-conversion) |
|---------|------------------------------|-------------------------------|
| Precision of distances | Rounded to nearest meter or 0.1 m | To hundredths (0.01 m) |
| Precision of bearings | Degrees only or degrees + rough minutes | Degrees and minutes (sometimes seconds) |
| Area precision | Rounded (e.g., "32,156 square meters") | Computed to hundredths (e.g., "32,156.45 sq.m.") |
| Datum | Typically Luzon 1911, old PTM zone | Post-conversion may be PRS92 or retained Luzon 1911 |
| Source of data | Scaled from plan/map | Computed from field observations |
| Notation in footer | May note "graphical" or have no special note | "Conversion computation into numerical technical description was approved [date]" |

### 7.4 How to Detect Graphical vs. Numerical Origin

There is no reliable way to detect from the TD text alone whether the data was originally graphical. Indicators include:

1. **Footer note:** "Conversion computation" or "Cadm" (cadastral mapping) in the plan reference
2. **Survey era:** Graphical cadastre was discontinued in the late 1970s; lots surveyed before ~1980 under cadastral mapping projects (Cadm-NNN or PCadm-NNN plan prefixes) may be graphical
3. **Precision clues:** All distances rounded to whole meters or 0.1 m (vs. 0.01 m for numerical)
4. **Plan prefix:** `Cadm` (Cadastral Mapping) or `PCadm` (Photo-Cadastral Mapping) indicates graphical origin

### 7.5 Parser Implications

1. **No separate parsing path needed.** Post-conversion numerical TDs use the standard format. The parser already handles these.

2. **Pre-conversion graphical TDs** may have:
   - Lower-precision distances (whole meters)
   - Larger closure errors (due to scaling rather than computation)
   - Area statements that are less precise

3. **New survey plan prefixes to add:**
   ```
   Cadm    # Cadastral Mapping (graphical)
   PCadm   # Photo-Cadastral Mapping (graphical)
   ```

4. **Footer parsing enhancement:** Capture "conversion computation" notes as metadata:
   ```python
   CONVERSION_NOTE_RE = re.compile(
       r'[Cc]onversion\s+computation\s+into\s+numerical\s+technical\s+description'
       r'\s+was\s+approved\s+(.+?)\.?$',
       re.IGNORECASE
   )
   ```

5. **Validation adjustment:** When a graphical-origin lot is detected (by plan prefix or conversion note), the closure tolerance should be relaxed. Graphical lots typically have poorer closure than numerical lots. The validation should use a wider tolerance tier (e.g., 1:1,000 instead of 1:5,000).

6. **Confidence flag:** Output should include:
   ```json
   {
     "survey_origin": "graphical_converted",
     "conversion_date": "May 22, 1984",
     "precision_note": "Distances may be derived from map scaling; expect larger closure errors"
   }
   ```

---

## 8. "Floating Parcels" — TDs Without Tie Points

### 8.1 What They Are

Some titles — particularly very old ones or those from incomplete records — lack a tie point and/or tie line. The CREBA describes this as a "floating parcel": "The property cannot be mapped or plotted, nor located on the ground — unless reference is made to the titles or survey records of the indicated bounding properties."

### 8.2 When They Occur

- Very old Spanish-era titles or US-era reconstitutions
- Reconstituted titles where the tie point data was lost
- Some subdivision lots where the TD was truncated

### 8.3 Modern Exception: Coordinate-Based Descriptions

Some modern surveys (particularly post-2010) provide **direct geographic coordinates** for each corner instead of a tie point + bearing/distance traverse:
```
Corner 1 at 9° 17' 49" N, 119° 47' 42" E
Corner 2 at 9° 17' 48" N, 119° 47' 44" E
...
```

In this case, no tie point/tie line is needed because the corners are georeferenced directly.

### 8.4 Parser Implications

1. **`TieBlockNotFound` is already defined** as an error condition. No new code needed.

2. **When no tie point is found**, the parser should still attempt to extract the traverse legs. The output should include `tie_point: null` and all corners expressed as **relative offsets** from an unknown origin.

3. **Coordinate-based descriptions** require a separate parsing path:
   ```python
   COORD_CORNER_RE = re.compile(
       r'Corner\s+(\d+)\s+at\s+'
       r'(\d+)°\s*(\d+)[′\']\s*(\d+(?:\.\d+)?)[″"]\s*([NS])\s*,?\s*'
       r'(\d+)°\s*(\d+)[′\']\s*(\d+(?:\.\d+)?)[″"]\s*([EW])',
       re.IGNORECASE
   )
   ```
   This is a **distinct TD format** that bypasses the entire traverse computation pipeline — corners are already in geographic coordinates.

4. **Detection logic:** If `TIE_BLOCK_RE` fails AND `COORD_CORNER_RE` succeeds, the TD is coordinate-based. If both fail, it's a floating parcel.

---

## 9. Additional Survey Plan Prefixes Not in Original Corpus

The following survey plan prefixes were discovered during research but were not represented in the Wave 1 sample corpus:

| Prefix | Full Name | Notes |
|--------|-----------|-------|
| FP | Free Patent | Original survey for free patent titling; ≤5 ha agricultural |
| H | Homestead Patent | Original survey for homestead titling; ≤24 ha agricultural |
| Bsd | Bureau [of Lands] Subdivision | Government-conducted subdivision of government land |
| Ts | Townsite Survey | Survey of townsite areas |
| Ms | Miscellaneous Sales Survey | Original survey on residential lots for sales patent |
| Ap | Advanced Plan | Not commonly seen on titles |
| Cadm | Cadastral Mapping | Graphical cadastre |
| PCadm | Photo-Cadastral Mapping | Graphical cadastre from aerial photography |
| Gss | Group Settlement Subdivision | Public land subdivision for settlers |
| (AR) suffix | Agrarian Reform | CARP-related survey, e.g., "Psd-03-002416 (AR)" |

**Parser update:** Add these prefixes to `SURVEY_PLAN_RE`:
```python
SURVEY_PLAN_RE = re.compile(
    r"""
    (?:
        (?:\(LRC\)\s*)?
        (Psd|Psu|Csd|Cad|Mr|Bp|PLS|Pls|Ccs|Mcs|Pcs|Bsd|FP|Ts|Ms|Ap|Cadm|PCadm|Gss|H)
        (?:-\(af\)|-\(ct\)|-\(if\))?   # optional qualifier
        -?(\d{2})?                       # optional region code
        [-–]?(\d+)                       # sequence number
        ([A-Z])?                         # optional suffix letter
        (?:\s*\(AR\))?                   # optional agrarian reform tag
        |
        Cad\.?\s+(\d+)([A-Z-]*)         # Cadastral: "Cad. 407" or "Cad. 652-D"
    )
    """,
    re.IGNORECASE | re.VERBOSE
)
```

---

## 10. LRA Electronic Technical Description (eTD) System

### 10.1 What It Is

Since 2020, the LRA has implemented an **electronic Technical Description (eTD)** system. Under this system, technical descriptions for new subdivision lots are:
- Encoded and uploaded by accredited geodetic engineers
- Generated electronically for new TCTs
- Expected to be free of common clerical errors

### 10.2 Format Implications

The eTD system does not change the **structure** of the technical description — it still follows the canonical metes-and-bounds format. However:
- Precision may be higher (electronically computed, no manual transcription)
- Formatting may be more consistent (standardized templates)
- Special characters (°, ′, ²) may be Unicode rather than typewriter approximations

### 10.3 Parser Implications

No parser changes needed. The eTD output conforms to the same structural format already covered by the parser grammar.

---

## 11. DENR LAMS e-Survey Plan and DLSD Format

### 11.1 What It Is

DENR Administrative Order No. 2016-01 mandated the **Digital Land Survey Data (DLSD)** format for electronic submission of survey plans. The **e-Survey Plan** software generates XML files compliant with DLSD specifications.

### 11.2 Relevance to Parser

The DLSD/XML format is a **separate data format** from the prose technical description. It is used for:
- Survey submission to DENR
- Lot data computation exchange
- Integration into the Land Administration and Management System (LAMS)

**The parser in this engine spec deals with prose TDs embedded in titles, NOT DLSD XML.** However, future engine extensions might ingest DLSD data as a higher-fidelity alternative input format.

---

## 12. Summary: Complete Survey Plan Prefix Registry

| Prefix | Type | Region Code? | Title Type | TD Format |
|--------|------|-------------|-----------|-----------|
| Psd | Private Subdivision | Yes (new) / No (old) | TCT | Standard |
| (LRC) Psd | LRC-approved Subdivision | No | TCT | Standard |
| Csd | Cadastral Subdivision | Yes | TCT | Standard |
| Bsd | Bureau Subdivision | Yes | TCT | Standard |
| Psu | Private Survey (original) | Yes | OCT (judicial) | Standard |
| PLS/Pls | Public Land Subdivision | No | OCT | Standard |
| Cad | Cadastral Survey | No | OCT | Standard |
| Cadm | Cadastral Mapping (graphical) | No | OCT | Lower precision |
| PCadm | Photo-Cadastral Mapping | No | OCT | Lower precision |
| Mr | Municipal Registration | No | OCT | Standard |
| Bp | Bureau of Lands Plan | No | Various | Standard |
| FP | Free Patent | Yes (newer) | OCT | Standard |
| H | Homestead Patent | No | OCT | Standard |
| Ccs | Consolidation Survey | Yes | TCT | Standard |
| Pcs | Consolidation-Subdivision | Yes | TCT | Standard |
| Ts | Townsite Survey | Yes | OCT | Standard |
| Ms | Miscellaneous Sales | No | OCT | Standard |
| Gss | Group Settlement Subdivision | No | OCT | Standard |

---

## 13. Key Findings for Parser Design

1. **No separate code paths needed for survey type.** All survey types (Psd, Csd, Pcs, Ccs, Psu, PLS, Cad, FP, H, etc.) use the same canonical TD format: tie point + tie line + traverse + area + footer. The differences are in metadata fields only.

2. **The tie point is ALWAYS a geodetic monument** (BLLM, BBM, MBM, L.W., etc.) — even in subdivision lots. Subdivision TDs do NOT reference parent lot corners as tie points.

3. **Consolidation TDs** describe the outer boundary only. The "being a portion of" clause may reference multiple parent lots, but this is metadata that does not affect computation.

4. **Old-format vs. new-format plan numbers** have NO bearing or datum implications. The region code is useful for zone validation.

5. **Reconstituted titles** are more likely to have degraded TD data. The parser should handle this via existing error/warning codes plus new ones (TieDistanceMissing, MissingCorners, DuplicateCorner).

6. **Free patent and homestead patent TDs** are structurally identical to regular TDs. No parser changes needed beyond adding FP and H to the plan prefix registry.

7. **Graphical-origin TDs** (from Cadm/PCadm surveys) have lower precision and should trigger relaxed validation tolerances. The "conversion computation" footer note is the key detection signal.

8. **Floating parcels** (no tie point) cannot be geolocated but the traverse polygon can still be computed relative to an unknown origin.

9. **Coordinate-based TDs** (modern, with lat/lng per corner) bypass the traverse pipeline entirely. A separate detection regex is needed.

10. **The (LRC) prefix** does not affect TD format — it only indicates the approving authority.

---

## Sources

- [CREBA: Technical Errors in Land Titles: Detection & Correction](https://creba.ph/technical-errors-in-land-titles-detection-correction/) (2025)
- [Philippine Cadastral System — cadastraltemplate.org](https://cadastraltemplate.org/philippines.php) (CSDILA/University of Melbourne)
- [DENR MC 2010-06: Manual on PRS92 Transformation](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/49164)
- [DENR DAO 2007-29: Revised Regulations on Land Surveys](https://legaldex.com/laws/revised-regulations-on-land-surveys)
- [DENR DAO 2010-17: IRR on IVAS in PRS92](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/52040)
- [LMB eSurveyPlan Manual](https://lmb.gov.ph/wp-content/uploads/2023/06/eSurveyPlanManual.pdf)
- [LRA History and Functions](https://lra.gov.ph/history/)
- [RA 26 — Reconstitution of Torrens Certificates](https://lawphil.net/statutes/repacts/ra1946/ra_26_1946.html)
- [RA 6732 — Administrative Reconstitution](https://lawphil.net/statutes/repacts/ra1989/ra_6732_1989.html)
- [RA 10023 — Residential Free Patent Act](https://lawphil.net/statutes/repacts/ra2010/ra_10023_2010.html)
- [Respicio & Co. — Geodetic Survey Requirement for Lot Partition](https://www.respicio.ph/commentaries/geodetic-survey-requirement-for-lot-partition-registration-philippines)
- [Respicio & Co. — Reconstitution of Title](https://www.respicio.ph/bar/2025/civil-law/land-titles-and-deeds/reconstitution-of-title)
- [Real Estate Matter: Survey Meanings](http://cy-realestatematter.blogspot.com/2011/01/survey-meanings.html)
- [Proclamation No. 1127 — Pcs-11-000142 Example](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/7/64232)
- [DENR Manual on Land Survey Procedures (FAO copy)](https://faolex.fao.org/docs/pdf/phi152415.pdf)
- [Geoportal Lot Plotter Manual](https://www.geoportal.gov.ph/resources/lotplotter.pdf)
- [DENR-DAR JAO 06-91 — Survey numbering for CARP](http://lis.dar.gov.ph/documents/418)
- Wave 1: `analysis/tech-description-samples.md` — 8-sample corpus
- Wave 2: `analysis/text-parser-grammar.md` — BNF grammar and regex patterns
- Wave 2: `analysis/validation-rules.md` — closure and area tolerance thresholds
