# Zonal Value Lookup Engine — Reverse Ralph Loop

You are an analysis agent in a ralph loop. Each time you run, you do ONE unit of work, then exit.

## Your Working Directory

You are running from `loops/reverse-ph-zonal-value-engine/`. All paths below are relative to this directory.

## Your Goal

Produce a **two-part specification** for a Zonal Value Lookup Engine — the highest-leverage data infrastructure component in Philippine real estate taxation (scored 125/125 in the [PH Tax Computations Survey](../reverse-ph-tax-computations/output/opportunity-catalog.md)).

### Part 1: Computation & Data Spec
Exhaustive documentation of how zonal values work across all 124 RDOs:
- Every Excel workbook format variation (column layouts, merged cells, headers, sheet structures)
- Address matching rules and ambiguity patterns
- Classification code usage across regions
- Fallback hierarchy implementation with worked examples
- Condo table structures (per-unit vs per-sqm)
- RPVARA transition mechanics (BIR ZV → BLGF SMV dual-source handling)
- Edge cases from CTA rulings and BIR rulings on zonal disputes

### Part 2: App Architecture Spec
Full-stack Rust + TypeScript application design:
- **Rust engine**: Data structures, matching algorithms, classification resolution, fallback logic
- **WASM bridge**: Client-side computation for privacy (property details never leave the browser)
- **Data pipeline**: Ingestion of 124 heterogeneous BIR Excel workbooks, normalization, indexing
- **Frontend**: TypeScript/React UI for property lookup
- **Data size analysis**: Can the full dataset (~1.96M records) fit in a WASM bundle, or does it need a hybrid (WASM logic + API data)?
- **RPVARA-ready**: Dual-source architecture for the 2026-2027 transition period

### Prior Art

This loop builds on the existing analysis in `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md` — a 400-line spec covering the 5-step resolution pipeline, 10 complexity drivers, fallback rules, RPVARA transition, and third-party platform survey. That analysis is the starting point, not the finish line.

### Scope

**In scope:**
- All 124 RDO zonal value schedules (sampled, not exhaustive parsing of every single one)
- Address matching and normalization strategies
- Classification code resolution
- Fallback hierarchy
- Condo/parking/special property handling
- RPVARA transition (RA 12001, BLGF MC 001-2025)
- Third-party platform reverse-engineering (Housal, RealValueMaps, ZonalValueFinderPH)
- Rust + WASM + TypeScript architecture
- Privacy model (client-side vs hybrid computation)

**Out of scope:**
- Building the engine (this loop produces the spec only)
- Downstream tax computations (CGT, DST, CWT, VAT — covered by separate loops)
- LGU assessor FMV data (separate data source, not part of BIR zonal values)
- Mobile app design

### Final Output

`output/zonal-value-engine-spec.md` — two-part spec (computation + architecture) actionable enough to feed into a forward loop using the [fullstack-rust-wasm template](https://github.com/clsandoval/monorepo/tree/main/loops/_templates/fullstack-rust-wasm).

## Reference Material

### Primary Sources (fetched in Wave 1)
- **BIR zonal value workbooks**: Download samples from bir.gov.ph/zonal-values — target 8-10 RDOs across NCR, provincial, condo-heavy, and agricultural regions
- **RMO No. 31-2019**: Annex B (classification codes) and Annex C (standard schedule format)
- **RMC 115-2020**: Certification procedure and data authority
- **RA 12001 / RPVARA**: Full text + IRR (BLGF MC 001-2025) — transition mechanics
- **CTA rulings**: Cases involving zonal value disputes (classification, fallback, jurisdiction)
- **Third-party platforms**: Housal, RealValueMaps, ZonalValueFinderPH, LandValuePH, REN.PH — data models and coverage

### Prior Analysis (available immediately)
- `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md` — 5-step resolution pipeline, classification codes, fallback rules, RPVARA transition, third-party survey
- `../reverse-ph-tax-computations/output/opportunity-catalog.md` — strategic context and scoring

### Cached Sources (after Wave 1)
After Wave 1, all fetched content lives in `input/`. Later waves read from these instead of re-fetching.
- `input/bir-workbook-samples/` — downloaded Excel workbooks (one per sampled RDO)
- `input/rmo-31-2019-annexes.md` — classification codes and format standard
- `input/rpvara-transition.md` — RA 12001 + IRR provisions relevant to zonal values
- `input/cta-zonal-rulings.md` — CTA cases on zonal value disputes
- `input/third-party-platforms.md` — data models and coverage analysis of existing platforms

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
6. **Commit**: `git add -A && git commit -m "loop(reverse-ph-zonal-value-engine): {{aspect-name}}"`
7. **Exit**

## Analysis Methods By Wave

### Wave 1: Source Acquisition
Fetch and cache raw materials. For each aspect:
1. Use web search and web fetch to locate authoritative sources
2. For BIR workbooks: download actual Excel files from bir.gov.ph, save to `input/bir-workbook-samples/`
3. For legal sources: extract relevant sections, save to `input/`
4. For third-party platforms: document observable data models, API behavior (or lack thereof), coverage claims
5. Note what's available vs. what's missing — gaps inform later waves

### Wave 2: Data Format Analysis
Parse and document the actual data. For each aspect:
1. Open the cached BIR workbooks from `input/bir-workbook-samples/`
2. Document the exact structure: column names, header rows, merged cell patterns, sheet organization
3. Compare across RDOs — what's consistent vs. what varies
4. Produce format schemas/examples that a parser could target
5. Flag anomalies (image PDFs, missing columns, non-standard layouts)

### Wave 3: Resolution Logic Deep-Dive
Formalize each step of the resolution pipeline. For each aspect:
1. Start from the prior analysis in `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md`
2. Deepen with worked examples using actual data from Wave 1-2
3. **Spawn a verification subagent** to cross-check logic against 2+ independent sources
4. Document edge cases with specific examples (real streets, real RDOs, real classification conflicts)
5. Produce pseudocode/decision trees suitable for Rust implementation

### Wave 4: Competitive & Third-Party Analysis
Reverse-engineer existing solutions. For each aspect:
1. Web search for the platform's approach to data ingestion and matching
2. Document observable data model (search inputs, result structure, coverage gaps)
3. Identify what they solved well and what they missed
4. Assess data freshness and accuracy where possible

### Wave 5: App Architecture Design
Design the engine. For each aspect:
1. Reference all prior wave analysis — every design decision should trace to data findings
2. Evaluate tradeoffs (e.g., client-side data bundling vs. API — use actual data size from Wave 2)
3. Produce concrete designs: data structures (Rust types), API contracts, component diagrams
4. Consider the RPVARA transition — architecture must support dual-source without rewrites
5. Address privacy model explicitly: what data leaves the client, what stays local

### Wave 6: Synthesis & Self-Review
Compile and validate. For each aspect:
1. Assemble the full spec from all prior analysis
2. Cross-reference computation spec against architecture spec for completeness
3. Verify every complexity driver from the prior analysis is addressed in the architecture
4. Self-review: is this spec actionable enough for a forward loop?

## Available Tools

- **Web search & fetch** — for sourcing legal texts, BIR workbooks, third-party platforms
- **`gh` CLI** — authenticated GitHub access (if needed for reference repos)
- **Subagents** — spawn for verification cross-checks and parallel research
  - Use subagents to verify resolution logic against independent sources (Wave 3)
  - Use subagents to survey multiple third-party platforms in parallel (Wave 4)
- **Excel/file parsing** — read downloaded workbook contents to analyze format variations

## Rules

- Do ONE aspect per run, then exit. Do not analyze multiple aspects.
- Always check if required source files exist before starting a later-wave aspect.
- **Verification protocol**: Every Wave 3 resolution logic formalization MUST be cross-checked against at least 2 independent sources using a subagent. Single-source extractions are not acceptable.
- If sources conflict, document the conflict with full citations — do not resolve by guessing.
- Write findings in markdown with specific numbers, examples, and citations.
- When you discover a new aspect worth analyzing, add it to the frontier in the appropriate wave.
- Keep analysis files focused. One aspect = one file.
- Save raw fetched content to `raw/`, processed analysis to `analysis/`.
- **Build on prior art**: The existing `zonal-value-lookup.md` analysis is your starting point. Don't re-derive what's already confirmed — deepen it with actual data and implementation-level detail.
- **Trace design decisions**: Every architecture choice in Wave 5 should reference specific findings from Waves 2-4. No hand-waving.
