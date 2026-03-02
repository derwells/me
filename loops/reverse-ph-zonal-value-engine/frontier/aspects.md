# Frontier — Zonal Value Lookup Engine

## Statistics
- Total aspects discovered: 28
- Analyzed: 1
- Pending: 27
- Convergence: 3.6%

## Pending Aspects (ordered by dependency)

### Wave 1: Source Acquisition (7 aspects)
- [x] bir-workbook-ncr-samples — Download 3-4 BIR zonal value Excel workbooks from NCR RDOs (Makati, Taguig, Mandaluyong, QC) — these are high-density, condo-heavy, well-maintained schedules
- [ ] bir-workbook-provincial-samples — Download 3-4 provincial RDO workbooks (mix of urban provincial like Cebu/Davao and rural agricultural like Laguna/Pangasinan) — different format patterns expected
- [ ] rmo-31-2019-annexes — Fetch RMO 31-2019 full text focusing on Annex B (classification codes) and Annex C (standard schedule format) — the normative standard that RDOs should follow
- [ ] rpvara-transition-mechanics — Fetch RA 12001 full text + BLGF MC 001-2025 IRR, extract provisions specific to zonal value transition: SMV format, timeline, dual-source handling, LGU compliance requirements
- [ ] cta-zonal-rulings — Search for CTA cases involving zonal value disputes: classification disagreements, fallback rule application, jurisdiction conflicts, stale schedule challenges
- [ ] third-party-platform-survey — Analyze Housal (1.96M records), RealValueMaps (2.7M records), ZonalValueFinderPH, LandValuePH, REN.PH — document their search UX, data models, coverage claims, limitations
- [ ] prior-analysis-import — Import and annotate the existing analysis from `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md` — identify confirmed findings vs. areas needing deeper investigation

### Wave 2: Data Format Analysis (7 aspects)
Depends on Wave 1 data.
- [ ] workbook-column-layouts — Document exact column layouts across all sampled workbooks: column names, positions, data types, which columns are consistent vs. varying
- [ ] merged-cell-patterns — Map merged cell usage across workbooks: barangay groupings, header hierarchies, multi-row entries — produce a taxonomy of merge patterns a parser must handle
- [ ] sheet-organization — Document sheet naming, structure, and organization across RDOs: data sheets vs. notice sheets vs. revision history sheets, condo vs. land separation
- [ ] address-vicinity-patterns — Catalog the actual vicinity descriptor patterns found in workbooks: "along [Street]", "[Street] from [X] to [Y]", "interior lots", "all other streets in [Barangay]" — build a pattern taxonomy
- [ ] classification-code-usage — Map which classification codes (RR, CR, RC, CC, I, A1-A50, etc.) appear in which RDOs, how they're formatted, and frequency distribution
- [ ] condo-table-structures — Document condo-specific table formats: building name organization, tower/floor range encoding, per-unit vs. per-sqm distinction, parking slot entries
- [ ] data-size-estimation — Estimate total dataset size when normalized: record count, storage in JSON/binary formats, compressed sizes — critical input for WASM bundling decision

### Wave 3: Resolution Logic Deep-Dive (5 aspects)
Depends on Wave 2 data.
- [ ] rdo-jurisdiction-mapping — Formalize the city/municipality → RDO lookup with actual data: complete mapping table, edge cases (boundary disputes, newly created LGUs), update frequency
- [ ] address-matching-algorithms — Design address matching strategy using Wave 2 pattern taxonomy: exact match, fuzzy match, vicinity segment resolution, barangay-level fallback — evaluate NLP/geocoding approaches with worked examples from actual workbook data
- [ ] classification-resolution-logic — Formalize classification code resolution with edge cases: mixed-use properties, predominant use rule, agricultural minimum area thresholds, conversion/reclassification timing — pseudocode suitable for Rust
- [ ] fallback-hierarchy-implementation — Implement the 6-level fallback chain with worked examples from actual RDO data: exact match → barangay general → special use → LGU FMV markup → written inquiry → zonal classification ruling
- [ ] rpvara-dual-source-resolution — Design the dual-source resolution for 2026-2027 transition: when to use BIR ZV vs BLGF SMV, how to detect which regime applies for a given RDO, graceful degradation when SMV data is incomplete

### Wave 4: Competitive & Third-Party Analysis (3 aspects)
Depends on Wave 1 third-party data.
- [ ] housal-data-model — Reverse-engineer Housal's approach: how they organized 1.96M records, search input model, result structure, coverage gaps (which RDOs/classifications are missing), data freshness
- [ ] realvaluemaps-approach — Analyze RealValueMaps' 2.7M records: different approach than Housal? GIS integration? Data model comparison, coverage analysis
- [ ] competitive-gap-synthesis — Synthesize findings across all platforms: what's the state of the art, what everyone gets wrong, where the opportunity lies for an API-first approach

### Wave 5: App Architecture Design (4 aspects)
Depends on Waves 2-4.
- [ ] rust-engine-design — Design Rust data structures and matching engine: property record types, index structures for fast lookup, classification enums, fallback state machine — informed by Wave 2 format analysis and Wave 3 resolution logic
- [ ] wasm-vs-hybrid-tradeoff — Evaluate client-side WASM bundle vs. hybrid (WASM logic + API data) using Wave 2 data size estimates: bundle size limits, lazy loading strategies, privacy implications, offline capability
- [ ] data-pipeline-architecture — Design the ingestion pipeline: Excel parsing (handling merged cells, format variations), normalization, indexing, update monitoring for 124 RDOs, RPVARA data source integration
- [ ] frontend-api-design — Design TypeScript frontend and API contracts: search UX (address input, classification selection, result display with confidence scores), API endpoints, error states, fallback display

### Wave 6: Synthesis & Self-Review (2 aspects)
Depends on all Wave 5 analysis.
- [ ] spec-compilation — Assemble the full two-part spec from all prior analysis: Part 1 (computation & data) from Waves 2-3, Part 2 (architecture) from Wave 5, write to `output/zonal-value-engine-spec.md`
- [ ] spec-self-review — Self-review the compiled spec: verify every complexity driver is addressed, all design decisions trace to data findings, spec is actionable for a forward loop, no gaps in coverage

## Recently Analyzed
- [x] bir-workbook-ncr-samples (Wave 1) — 2026-03-02 — 24 NCR RDO workbooks downloaded and structurally analyzed. 4 column layout patterns, 6 barangay header variants, 5+ date formats identified. Key emergent finding: BGC FAR-based pricing is a unique pattern requiring special handling.
