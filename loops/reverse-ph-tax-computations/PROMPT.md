# PH Tax Computations Survey — Reverse Ralph Loop

You are an analysis agent in a ralph loop. Each time you run, you do ONE unit of work, then exit.

## Your Working Directory

You are running from `loops/ph-tax-computations-reverse/`. All paths below are relative to this directory.

## Your Goal

Survey every deterministic computation in Philippine real estate taxation (plus adjacent business tax compliance and real property tax), and produce a **ranked opportunity catalog** for building automation engines.

The catalog scores each computation by automation potential, competitive gap, and moat defensibility — so we can decide which ones deserve their own dedicated deep-dive loop (like the [inheritance-reverse loop](https://github.com/clsandoval/monorepo/tree/main/loops/inheritance-reverse) that produced a 1,500-line engine spec).

### Scope

**Primary — Real estate transaction taxes:**
- Capital gains tax (CGT), documentary stamp tax (DST), VAT on real property, creditable withholding tax (CWT), transfer tax
- "Highest of three" tax base resolution (selling price vs zonal value vs assessed FMV)
- Zonal value lookup and resolution

**Secondary — Business tax compliance (real estate adjacent):**
- Expanded withholding tax (EWT) rate classification
- VAT reconciliation (2550M vs 2550Q vs ITR)
- Form 2307 issuance logic
- Alphalist generation (1604-C/E/F)

**Secondary — Real property tax:**
- RPT computation across LGUs (FMV × assessment level × rate)
- Special Education Fund (SEF) levy

### Out of Scope
- Non-deterministic computations (e.g., ordinary vs capital asset classification — requires judgment)
- Building any engine — this loop produces the map only
- Payroll, lending, banking, securities

### Final Output

`output/opportunity-catalog.md` — ranked list of 15-30 deterministic computations, each entry containing:
- What it computes (inputs → outputs)
- Legal basis (article/RR/RA numbers)
- Current state (manual, spreadsheet, partially automated)
- Complexity estimate (branching rules, lookup tables, data dependencies)
- Competitive gap (what JuanTax/Taxumo/QNE don't cover)
- Moat score (how hard to replicate once built)

## Reference Material

### Primary Legal Sources (fetched in Wave 1)
- NIRC (RA 8424 as amended by TRAIN/RA 10963): Title II (income tax), Title IV (VAT), Title VI (stamp taxes)
- BIR Revenue Regulations: RR 7-2003, RR 2-98, RR 16-2005, RR 11-2025 (e-invoicing)
- BIR Revenue Memorandum Circulars: RMC 99-2023 (installment VAT), RMC 56-2024 (eCAR jurisdiction)
- Local Government Code (RA 7160): RPT provisions

### Secondary Sources (practitioner guides)
- Grant Thornton PH, PwC PH, BDB Law, Respicio & Co. tax alerts with worked examples
- BIR form instructions: Forms 1706, 2000-OT, 2550Q, 1601-EQ, 2307

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
6. **Commit**: `git add -A && git commit -m "loop(ph-tax-computations): {{aspect-name}}"`
7. **Exit**

## Analysis Methods By Wave

### Wave 1: Source Acquisition
Fetch and cache legal/regulatory sources. For each aspect:
1. Use web search and web fetch to locate authoritative sources
2. Extract relevant sections (not full documents — focus on computation-relevant provisions)
3. Save processed content to `input/{{source-name}}.md`
4. Note which specific articles, sections, or RR numbers are most relevant for Wave 2

### Wave 2: Computation Extraction
For each computation, produce a mini-spec. **Verification is mandatory:**
1. Extract the formula/logic from the primary legal source in `input/`
2. **Spawn a verification subagent** to independently cross-check the extracted logic against 2-3 secondary sources (practitioner alerts, BIR form instructions, worked examples from `input/`)
3. If sources conflict: document both versions with citations, flag for manual review
4. If the computation requires judgment (not purely deterministic): mark as "non-deterministic", document why, exclude from final scoring
5. Write to `analysis/{{computation-name}}.md` with:
   - Inputs (with types)
   - Formula / decision tree / lookup table
   - Edge cases and special rules
   - Legal citations (article + RR + section numbers)
   - Verification status (confirmed / conflict / unverified)
   - Deterministic: yes/no

### Wave 3: Competitive & Automation Gap Analysis
For each aspect:
1. Web search for existing Philippine tax tools (JuanTax, Taxumo, QNE Cloud, etc.)
2. Check feature lists and documentation for coverage of each Wave 2 computation
3. Document current practitioner workflow (fully manual, Excel, partially automated)
4. Score complexity: count branching rules, lookup tables, external data dependencies

### Wave 4: Scoring & Synthesis
1. Score each computation: `automation_gap × market_frequency × moat_defensibility`
   - automation_gap: 1 (existing tools cover it) to 5 (fully manual, no tools)
   - market_frequency: 1 (rare transaction type) to 5 (every real estate deal)
   - moat_defensibility: 1 (trivial to replicate) to 5 (requires deep regulatory knowledge + data)
2. Rank by composite score
3. Write catalog to `output/opportunity-catalog.md`
4. Self-review for completeness

## Available Tools

- **Web search & fetch** — for sourcing legal texts, BIR regulations, practitioner guides
- **`gh` CLI** — authenticated GitHub access (if needed for reference repos)
- **Subagents** — spawn for verification cross-checks in Wave 2 and competitive research in Wave 3
  - Always use subagents to verify extracted computations against secondary sources
  - Subagents can web search independently

## Rules

- Do ONE aspect per run, then exit. Do not analyze multiple aspects.
- Always check if required source files exist before starting a later-wave aspect.
- **Verification protocol**: Every Wave 2 computation extraction MUST be cross-checked against at least 2 independent sources using a subagent. Single-source extractions are not acceptable.
- If sources conflict, document the conflict with full citations — do not resolve by guessing.
- Mark any computation requiring human judgment as "non-deterministic" and exclude from scoring.
- Write findings in markdown with specific numbers, examples, and citations.
- When you discover a new computation worth analyzing, add it to the frontier in the appropriate wave.
- Keep analysis files focused. One aspect = one file.
- Save raw fetched content to `raw/`, processed analysis to `analysis/`.
