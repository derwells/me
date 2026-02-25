# PH Land Title Coordinates — Reverse Ralph Loop

You are an analysis agent in a ralph loop. Each time you run, you do ONE unit of work, then exit.

## Your Working Directory

You are running from `loops/ph-land-title-coordinates-reverse/`. All paths below are relative to this directory.

## Your Goal

Produce a **computation engine spec** for converting Philippine land title technical descriptions into WGS84 latitude/longitude coordinates. The spec should be detailed enough to hand to a developer and build from.

### What It Covers

1. **Text parser** — grammar/rules for extracting structured data from technical description text (tie point, tie line, bearing/distance sequence, area, survey plan number)
2. **Traverse computation** — corner-to-corner coordinate computation from bearing/distance pairs
3. **Datum transformation** — PRS92 Northing/Easting → WGS84 lat/lng (7-parameter Helmert); legacy Luzon 1911 → PRS92 → WGS84
4. **BLLM coordinate dataset** — compiled from publicly available sources, with coverage gap analysis
5. **Validation** — closure error, area cross-check, bearing consistency
6. **Edge cases** — format variations, error handling, legacy titles

### Input Assumptions

- Pre-transcribed technical description text (no OCR)
- BLLM coordinates either from compiled dataset or provided by caller

### Final Output

`output/engine-spec.md` — containing:
- Text parser grammar with format variation handling
- Traverse computation formulas with worked examples
- PRS92 → WGS84 transformation with zone selection logic
- Luzon 1911 legacy handling with error bounds
- BLLM coordinate dataset + coverage analysis
- Validation rules and error detection
- 5+ test vectors with known input/output pairs

## Reference Material

### Primary Sources
- PRS92 zone definitions: EPSG 3121–3125 (5 zones, Clarke 1866 ellipsoid, Transverse Mercator)
- PRS92→WGS84 7-parameter Helmert shift: `TOWGS84[-127.62, -67.24, -47.04, 3.068, -4.903, -1.578, -1.06]`
- Luzon 1911 datum: EPSG 4253, with transformation per DENR MC 2010-06
- DENR Manual on Land Survey Procedures
- Title Plotter PH QGIS plugin source: github.com/isaacenage/TitlePlotterPH

### BLLM Data Sources
- Geoportal Philippines Lot Plotter (embedded BLLM database)
- Title Plotter PH plugin (bundled tie point data)
- LMB/NAMRIA geodetic control point publications

### Cached Sources (after Wave 1)
After Wave 1, all fetched content lives in `input/`. Later waves read from these instead of re-fetching.

## What To Do This Iteration

1. **Read the frontier**: Open `frontier/aspects.md`
2. **Find the first unchecked `- [ ]` aspect** in dependency order (Wave 1 before Wave 2 before Wave 3...)
   - If a later-wave aspect depends on data that doesn't exist yet, skip to an earlier-wave aspect
   - If ALL aspects are checked `- [x]`: write convergence summary to `status/converged.txt` and exit
3. **Analyze that ONE aspect** using the appropriate method (see below)
4. **Write findings** to `analysis/{{aspect-name}}.md`
5. **Update the frontier**:
   - Mark the aspect as `- [x]` in `frontier/aspects.md`
   - Update Statistics (increment Analyzed, decrement Pending, update Convergence %)
   - If you discovered new aspects worth analyzing, add them to the appropriate Wave
   - Add a row to `frontier/analysis-log.md`
6. **Commit**: `git add -A && git commit -m "loop(ph-land-title-coordinates): {{aspect-name}}"`
7. **Exit**

## Analysis Methods By Wave

### Wave 1: Source Acquisition
Fetch and cache reference data. For each aspect:
1. Use web search and web fetch to locate authoritative sources
2. Extract relevant parameters, formulas, datasets — not full documents
3. Save processed content to `input/{{source-name}}.md`
4. Note what's available vs what's missing for Wave 2

Aspects:
- **prs92-datum-parameters**: Fetch all 5 PRS92 zone definitions, ellipsoid constants, projection parameters, and the 7-parameter Helmert shift to WGS84. Save as structured reference.
- **luzon1911-transformation**: Fetch Luzon 1911 datum parameters, DENR MC 2010-06 transformation procedures, zone mappings, expected residual errors.
- **tech-description-samples**: Collect 5-8 real technical description texts spanning different vintages (pre-1993 Luzon 1911, post-1993 PRS92), regions (Luzon/Visayas/Mindanao), and survey types (Psd, Csd, Psu, Cad). These are the test corpus.
- **bllm-database-sources**: Identify and catalog all publicly accessible BLLM coordinate sources. Inspect Title Plotter PH GitHub repo for embedded data. Check Geoportal Lot Plotter. Document coverage.
- **traverse-computation-references**: Fetch geodetic traverse computation methods — bearing-distance to rectangular offset formulas, cumulative traverse, polygon closure computation.

### Wave 2: Core Computation Extraction
Depends on Wave 1 data. For each computation, produce a detailed mini-spec with formulas, inputs, outputs, and worked examples.

**Verification protocol**: Every extracted formula or transformation MUST be cross-checked against at least 2 independent sources using a subagent. If sources conflict, document both with citations.

Aspects:
- **text-parser-grammar**: Define parsing rules for the technical description format. Cover: tie point identification (BLLM name + cadastral reference), tie line extraction (bearing + distance to Corner 1), bearing/distance sequence, area statement, survey plan number parsing. Document format variations across eras.
- **traverse-algorithm**: Specify the full traverse computation: bearing/distance → delta-N/delta-E (polar to rectangular), cumulative corner coordinates, closed polygon construction. Include formulas and a worked example.
- **prs92-to-wgs84-transform**: Specify the complete pipeline: PRS92 zone Easting/Northing → PRS92 geographic (lat/lng on Clarke 1866) → WGS84 geographic (lat/lng on WGS84 ellipsoid). Include inverse Transverse Mercator + Helmert formulas. Document zone selection logic.
- **luzon1911-to-prs92-transform**: Specify legacy datum handling: how to detect Luzon 1911 titles, zone mapping (PTM zones → PRS92 zones), transformation method per DENR MC 2010-06, expected error bounds.
- **bllm-dataset-compilation**: Extract and compile BLLM coordinates from all sources identified in Wave 1. Structure as a dataset (monument ID, coordinates, source, confidence). Document coverage by region/province.
- **validation-rules**: Define validation computations: polygon closure error (linear misclosure), area cross-check (computed shoelace area vs stated area), bearing consistency, and acceptable tolerance thresholds.

### Wave 3: Edge Cases & Test Vectors
Depends on Wave 2 data.

Aspects:
- **format-variations**: Catalog all known format variations in technical descriptions: old-style cardinal directions, curved boundaries (arcs), natural feature references, subdivision vs original survey differences, missing tie points.
- **error-handling**: Define error handling for: typographical errors, missing corners, impossible bearings, BLLM not in database, ambiguous PRS92 zone, Luzon 1911 vs PRS92 ambiguity.
- **test-vectors**: Build 5+ test cases using tech descriptions from the Wave 1 corpus. For each: input text, expected parsed structure, expected corner coordinates (PRS92), expected WGS84 output. Verify against Geoportal Lot Plotter or Title Plotter PH where possible.

### Wave 4: Synthesis
Depends on all prior waves.

Aspects:
- **engine-spec-draft**: Assemble the complete engine spec at `output/engine-spec.md`. Organize by pipeline stage (parse → resolve BLLM → traverse → transform → validate). Include all formulas, worked examples, test vectors, and the BLLM dataset reference.
- **spec-review**: Self-review for completeness: Can a developer build this without asking questions? Are all formulas specified with units? Are edge cases covered? Are test vectors verifiable?

## Available Tools

- **Web search & fetch** — for sourcing geodetic parameters, DENR regulations, sample titles, BLLM data
- **`gh` CLI** — authenticated GitHub access (for Title Plotter PH repo inspection)
- **Subagents** — spawn for verification cross-checks in Wave 2
  - Always use subagents to verify extracted formulas against secondary sources
  - Subagents can web search independently

## Rules

- Do ONE aspect per run, then exit. Do not analyze multiple aspects.
- Always check if required source files exist before starting a later-wave aspect.
- **Verification protocol**: Every Wave 2 formula extraction MUST be cross-checked against at least 2 independent sources using a subagent. Single-source extractions are not acceptable.
- If sources conflict, document the conflict with full citations — do not resolve by guessing.
- Write findings in markdown with specific numbers, formulas, and citations.
- When you discover a new aspect worth analyzing, add it to the frontier in the appropriate wave.
- Keep analysis files focused. One aspect = one file.
- Save raw fetched content to `raw/`, processed analysis to `analysis/`.
- All coordinates in examples must include units (meters, degrees) and reference system (PRS92 Zone X, WGS84).
