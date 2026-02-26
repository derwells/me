# Frontier — PH Land Title Coordinates

## Statistics
- Total aspects discovered: 15
- Analyzed: 14
- Pending: 1
- Convergence: 93%

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
- [x] bllm-dataset-compilation — Extract and compile BLLM coordinates from identified sources; structure as dataset with coverage analysis
- [x] validation-rules — Closure error computation, area cross-check (shoelace vs stated), bearing consistency, tolerance thresholds

### Wave 3: Edge Cases & Test Vectors
Depends on Wave 2 data.
- [x] format-variations — Catalog format variations: cardinal directions, curved boundaries, natural features, subdivision vs original survey
- [x] error-handling — Error handling spec: typos, missing corners, impossible bearings, BLLM not found, ambiguous zone
- [x] test-vectors — Build 5+ test cases with known input/output; verify against Geoportal or Title Plotter PH

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
- bllm-dataset-compilation (Wave 2, 2026-02-26) — 85,303 records from tiepoints.json: 19,568 BLLMs + 26,155 BBMs + 15,609 PRS92 control points + others. Zone inference via DAO 98-12 province lookup (verified ≥4 sources). Datum inference from Description field: 18.4% PRS92, 66% Luzon 1911, 15.5% unknown. Luzon1911→PRS92 grid shift empirically confirmed ~7–13m (corrected from 100–300m claim). Coverage: 117 provinces, gaps in BARMM/CAR/post-2006 provinces. BBM corrected to Barangay Boundary Monument. 3-tier lookup algorithm. 3 GeoIDEx cross-reference points for test vectors.
- validation-rules (Wave 2, 2026-02-26) — 6 validation checks: linear closure (1:5,000 tertiary per DAO 2007-29 §28b, engine tiers 5k/3k/1k), area cross-check (shoelace vs stated, ≤0.5%/2%/5%), angular closure ((n-2)×180°, 30″√n), geometry sanity (self-intersection, bearing range, winding), BLLM confidence (5-tier), datum consistency (6 rules). Key correction: 1:3,000 rural NOT in DAO 2007-29 (engine-defined). Control tiers corrected: Primary=1:20,000, Secondary=1:10,000, Tertiary=1:5,000. All formulas verified ≥2 sources via subagent.
- format-variations (Wave 3, 2026-02-26) — 13-section catalog of TD format variations across survey types. Key findings: (1) subdivision/consolidation/free-patent TDs all use identical canonical format — no separate code paths needed; (2) tie point is ALWAYS a geodetic monument even in subdivisions (NOT parent lot corners); (3) old vs new plan numbers have NO bearing/datum implications; (4) reconstituted titles more likely to have degraded data — 3 new error codes (TieDistanceMissing, MissingCorners, DuplicateCorner); (5) graphical-origin TDs (Cadm/PCadm) have lower precision and need relaxed validation; (6) "floating parcels" (no tie point) can compute relative polygon only; (7) coordinate-based modern TDs (lat/lng per corner) bypass traverse pipeline entirely. 18 survey plan prefixes cataloged (up from 10). New regex for conversion computation footer note and coordinate-based corner detection.
- error-handling (Wave 3, 2026-02-26) — Comprehensive error handling spec across all 5 pipeline stages. 42 error codes defined (31 parse, 6 BLLM, 6 traverse, 7 transform, 2 output). 4 severity levels (FATAL/ERROR/WARNING/INFO). Key additions: (1) closure failure diagnostics with quadrant-flip detection heuristic; (2) bearing recovery algorithm for missing prefix/suffix (try both, pick by closure impact); (3) BLLM 5-tier fuzzy matching (exact → code+number → province filter → trigram similarity → caller-provided); (4) 6-level graceful degradation hierarchy (full WGS84 → PRS92-only → relative polygon → coordinate-based → parsed fields → total failure); (5) confidence scoring model (1.0 base, −0.3/error, −0.1/warning); (6) source quality inference (clean/good/degraded/poor/reconstituted_likely); (7) typo catalog with specific recovery strategies for N↔S swap, E↔W swap, missing decimal, minutes>59. New error codes: BearingMinutesOutOfRange, TieMonumentUnparseable, DistanceUnreasonable, TraverseOverflow, DegeneratePolygon, CoordinateClampWarning, InverseTMConvergenceFail.
