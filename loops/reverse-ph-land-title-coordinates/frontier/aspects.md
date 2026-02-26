# Frontier — PH Land Title Coordinates

## Statistics
- Total aspects discovered: 15
- Analyzed: 9
- Pending: 6
- Convergence: 60%

## Pending Aspects (ordered by dependency)

### Wave 1: Source Acquisition
- [x] prs92-datum-parameters — Fetch PRS92 zone definitions (EPSG 3121-3125), ellipsoid constants, projection parameters, 7-parameter Helmert shift to WGS84
- [x] luzon1911-transformation — Fetch Luzon 1911 datum parameters, DENR MC 2010-06 transformation procedures, residual error expectations
- [x] tech-description-samples — Collect 5-8 real technical description texts spanning different vintages, regions, and survey types as test corpus
- [x] bllm-database-sources — Identify all publicly accessible BLLM coordinate sources; inspect Title Plotter PH repo and Geoportal Lot Plotter
- [x] traverse-computation-references — Fetch geodetic traverse computation methods: bearing-distance formulas, closure adjustment

### Wave 2: Core Computation Extraction
Depends on Wave 1 data.
- [x] text-parser-grammar — Define parsing rules for technical description format: tie point, tie line, bearing/distance sequence, area, survey plan number; cover format variations
- [x] traverse-algorithm — Specify corner-to-corner traverse computation: polar→rectangular, cumulative coordinates, closed polygon; include worked example
- [x] prs92-to-wgs84-transform — Full pipeline: PRS92 zone N/E → PRS92 geographic → WGS84 geographic; inverse TM + Helmert formulas; zone selection logic
- [x] luzon1911-to-prs92-transform — Legacy datum handling: detection, zone mapping, transformation method per DENR MC 2010-06, error bounds
- [ ] bllm-dataset-compilation — Extract and compile BLLM coordinates from identified sources; structure as dataset with coverage analysis
- [ ] validation-rules — Closure error computation, area cross-check (shoelace vs stated), bearing consistency, tolerance thresholds

### Wave 3: Edge Cases & Test Vectors
Depends on Wave 2 data.
- [ ] format-variations — Catalog format variations: cardinal directions, curved boundaries, natural features, subdivision vs original survey
- [ ] error-handling — Error handling spec: typos, missing corners, impossible bearings, BLLM not found, ambiguous zone
- [ ] test-vectors — Build 5+ test cases with known input/output; verify against Geoportal or Title Plotter PH

### Wave 4: Synthesis
Depends on all prior waves.
- [ ] engine-spec-draft — Assemble complete spec at output/engine-spec.md
- [ ] spec-review — Self-review for completeness, correctness, implementability

## Recently Analyzed
- prs92-datum-parameters (Wave 1, 2026-02-25) — All 5 PTM zone definitions, Clarke 1866 constants, 7-parameter Helmert EPSG:15708 confirmed. Key finding: sign convention is Coordinate Frame (EPSG:9607), accuracy 0.05m.
- luzon1911-transformation (Wave 1, 2026-02-25) — EPSG:1161/1162 3-param Helmert (17m/44m accuracy); DENR MC 2010-06 4-param local transform (<1m residuals); typical 10–30m grid shift Luzon 1911→PRS92; detection via explicit datum label on plan.
- tech-description-samples (Wave 1, 2026-02-25) — 8 real samples collected (1916–2015) from Luzon, Visayas (Leyte), and Mindanao (GenSan). Key findings: 7 bearing format variants, 7 tie point monument code variants, Grid bearings pre-1993=Luzon 1911 PTM / post-1993=PRS92; "Due North" and degrees-only bearings require special casing; datum never explicit in TD body text.
- bllm-database-sources (Wave 1, 2026-02-25) — 4 sources identified: tiepoints.json (TitlePlotterPH, 15.9 MB, ~50k records, fields: Name/Province/Municipality/Northing/Easting); Geoportal Lot Plotter (same LMB data, WGS84 output, web UI only); GeoIDEx (demonstration data, Region III only, PRS92 lat/lng + PTM grid); DENR-LMB via FOI. Key gaps: no zone tag per record, no datum tag, rural municipalities and BARMM severely underrepresented. Engine must support caller-provided BLLM coordinates.
- traverse-computation-references (Wave 1, 2026-02-25) — Core formulas confirmed: ΔN=dist×cos(az), ΔE=dist×sin(az); shoelace area with floating-point note; Bowditch closure adjustment (for validation only, not applied to title data); Philippine tolerance 1:5000 (urban)/1:3000 (rural) from DAO 2007-29. Key finding: convert bearing→azimuth before all computation to avoid quadrant sign tables.
- text-parser-grammar (Wave 2, 2026-02-25) — BNF grammar + regex for all 9 fields (monument, bearing, distance, tie block, traverse legs, area, footer, survey plan, lot ID). Covers all 7 bearing variants incl. Due-cardinal and degrees-only. Verified against TitlePlotterPH source (4 regex strategies in plugin; area regex is engine addition not in plugin). Monument normalization 3-tier lookup documented. 14 error/warning codes defined.
- traverse-algorithm (Wave 2, 2026-02-26) — Full algorithm spec: tie-line (BLLM→C1), traverse loop, closure metrics, shoelace area with FP precision fix. Complete pseudocode + worked example (Sample 1: 4-corner lot, closure e=0.014m at 1:6,575, area=484.85m² vs stated 485m²). All 7 formulas verified ≥2 independent sources (Jerrymahun Ch. A/D/E/F/G/I + John D. Cook + ArcGIS Esri). Bowditch as non-default optional documented.
- prs92-to-wgs84-transform (Wave 2, 2026-02-26) — Complete 3-stage pipeline: geographic→geocentric (Clarke 1866) + Helmert 7-param (EPSG:15708 Coordinate Frame) + geocentric→geographic (WGS84 via Bowring 1976). h=0 convention for 2D confirmed by OS Guide, RDNAPTRANS, PROJ push/pop. Three reverse methods compared (Bowring/EPSG closed-form/OS iterative); Bowring recommended (single iteration, sub-mm, ~30% faster). All 6 formula sets verified ≥2 independent sources. Full pseudocode with inline constants.
- luzon1911-to-prs92-transform (Wave 2, 2026-02-26) — Two transform paths: Path A (global 3-param EPSG:1161/1162, 17–44m accuracy) always available; Path B (DENR MC 2010-06 4-param conformal, ~10cm) requires caller-provided CE/CN. Datum detection via plan metadata (regex + era heuristics). Zone mapping 1:1 (same ellipsoid/projection). BLLM datum mismatch handling documented. Regional split logic (Luzon/Visayas vs Mindanao). All params verified ≥2 sources (EPSG.io, EPSG.org, PROJ DB, ESRI, DMA TR8350.2). Worked example: Zone III Manila area, shift ≈ −5.4" lat / +5.1" lon.
