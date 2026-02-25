# Frontier — PH Land Title Coordinates

## Statistics
- Total aspects discovered: 15
- Analyzed: 0
- Pending: 15
- Convergence: 0%

## Pending Aspects (ordered by dependency)

### Wave 1: Source Acquisition
- [ ] prs92-datum-parameters — Fetch PRS92 zone definitions (EPSG 3121-3125), ellipsoid constants, projection parameters, 7-parameter Helmert shift to WGS84
- [ ] luzon1911-transformation — Fetch Luzon 1911 datum parameters, DENR MC 2010-06 transformation procedures, residual error expectations
- [ ] tech-description-samples — Collect 5-8 real technical description texts spanning different vintages, regions, and survey types as test corpus
- [ ] bllm-database-sources — Identify all publicly accessible BLLM coordinate sources; inspect Title Plotter PH repo and Geoportal Lot Plotter
- [ ] traverse-computation-references — Fetch geodetic traverse computation methods: bearing-distance formulas, closure adjustment

### Wave 2: Core Computation Extraction
Depends on Wave 1 data.
- [ ] text-parser-grammar — Define parsing rules for technical description format: tie point, tie line, bearing/distance sequence, area, survey plan number; cover format variations
- [ ] traverse-algorithm — Specify corner-to-corner traverse computation: polar→rectangular, cumulative coordinates, closed polygon; include worked example
- [ ] prs92-to-wgs84-transform — Full pipeline: PRS92 zone N/E → PRS92 geographic → WGS84 geographic; inverse TM + Helmert formulas; zone selection logic
- [ ] luzon1911-to-prs92-transform — Legacy datum handling: detection, zone mapping, transformation method per DENR MC 2010-06, error bounds
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
(Empty — loop hasn't started yet)
