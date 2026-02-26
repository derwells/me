# Engine Spec Draft — Assembly Notes

**Aspect:** engine-spec-draft (Wave 4)
**Date:** 2026-02-26
**Depends on:** All Wave 1, 2, and 3 analyses (14 prior iterations)

---

## What Was Assembled

The complete engine spec was written to `output/engine-spec.md`. It synthesizes all 14 prior analyses into a single implementable document organized by pipeline stage.

## Structure

The spec is organized as follows:

1. **Architecture Overview** — Pipeline diagram, input assumptions, graceful degradation hierarchy (6 levels)
2. **Stage 1: Text Parser** — Pre-processing, output schema, full regex grammar (10 subsections covering lot ID, survey plan, location, tie block, bearings, traverse legs, area, footer, coordinate-based TDs, distance parsing)
3. **Stage 2: BLLM Resolution** — 5-tier lookup algorithm, zone inference, datum mismatch handling
4. **Stage 3: Traverse Computation** — Polar-to-rectangular formulas, closure computation, shoelace area with coordinate-shift technique, full worked example (TV-1)
5. **Stage 4: Datum Transformation** — Datum detection algorithm, inverse TM (Snyder/Redfearn with complete Python implementation), Helmert transformation (geographic → geocentric → Helmert → geographic), Luzon 1911 paths
6. **Stage 5: Validation** — Linear closure, area cross-check, angular closure, geometry sanity checks with threshold tables
7. **Error Handling** — 42 error codes across 5 pipeline stages, severity levels, confidence scoring, closure failure diagnostics
8. **Test Vectors** — 6 test vectors (3 full pipeline, 1 error detection, 1 inverse TM round-trip, 1 parser unit tests)
9. **Appendices** — Ellipsoid constants, survey plan prefix registry, province-to-zone mapping, BLLM dataset reference

## Coverage Assessment

| Spec Requirement | Covered? | Section |
|-----------------|----------|---------|
| Text parser grammar with format variations | Yes | §2 |
| Traverse computation with worked examples | Yes | §4 |
| PRS92→WGS84 with zone selection | Yes | §5 |
| Luzon 1911 legacy handling with error bounds | Yes | §5.6-5.7 |
| BLLM dataset + coverage analysis | Yes | §3, Appendix D |
| Validation rules and error detection | Yes | §6, §7 |
| 5+ test vectors | Yes | §8 (6 vectors) |

## Key Design Decisions

1. **Snyder/Redfearn method** chosen for inverse TM over EPSG Krueger — simpler, non-iterative, sufficient accuracy for PTM zones
2. **Coordinate Frame rotation** convention for Helmert (EPSG:9607), not Position Vector — matches EPSG:15708 canonical definition
3. **Coordinate-shift technique** for shoelace area — prevents catastrophic cancellation with large PRS92 northing values
4. **M = y / k₀** (not M = y) for inverse TM — critical correctness note, ~94m error if omitted
5. **42 error codes** with accumulator pattern — comprehensive coverage of all failure modes across all pipeline stages
6. **6-level graceful degradation** — engine always returns something useful, from full WGS84 coordinates down to error report only

## What Remains

- **spec-review** aspect (Wave 4): Self-review for completeness, answering "Can a developer build this without asking questions?"

## Sources

All 14 analysis files in `analysis/` directory (see spec §Source Analyses for full listing).
