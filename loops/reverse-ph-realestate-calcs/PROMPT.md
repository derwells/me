# PH Real Estate Calculations Survey — Reverse Ralph Loop

You are an analysis agent in a ralph loop. Each time you run, you do ONE unit of work, then exit.

## Your Working Directory

You are running from `loops/ph-realestate-calcs-reverse/`. All paths below are relative to this directory.

## Your Goal

Survey every deterministic computation in Philippine real estate **outside taxation** — financing, regulatory compliance, property valuation, fees, and government housing programs — and produce a **ranked opportunity catalog** for building automation engines.

The catalog scores each computation by automation potential, competitive gap, and moat defensibility — so we can decide which ones deserve their own dedicated deep-dive loop.

**Complementary to:** `loops/ph-tax-computations-reverse/` — that loop covers all tax computations (CGT, DST, VAT, CWT, RPT, transfer tax, withholding). This loop covers everything else.

### Scope

**Primary — Financing & Amortization:**
- Pag-IBIG housing loan eligibility (contribution months, salary cap, loan limits by term)
- Pag-IBIG amortization schedule (declining balance, MRI/FGI computation)
- Bank mortgage amortization (fixed/variable rate, repricing schedules)
- Developer equity/downpayment schedules (spot cash discount, installment penalty)
- Loan-to-value ratio computation per BSP circular

**Primary — Regulatory Compliance:**
- Maceda Law (RA 6552) refund/grace period computation (2+ years paid → 50% refund + 5%/yr)
- DHSUD socialized/economic housing price ceilings (updated periodically)
- Rent Control Act (RA 9653) — allowable annual increase computation
- BP 220 minimum lot/unit size standards (compliance check)
- Condominium common area percentage computation (RA 4726)

**Primary — Valuation & Assessment:**
- Fair market value estimation formulas (income approach capitalization rate, comparable sales per-sqm)
- Assessment level by property classification (residential, commercial, industrial, agricultural — per LGC)
- Depreciation schedules for improvements (straight-line, per local assessor rules)

**Secondary — Fees & Dues:**
- Title registration fees (Registry of Deeds fee schedule)
- Notarial fee schedule
- Real estate broker commission computation (PRC-regulated splits)
- Condominium/subdivision association dues computation

### Out of Scope
- All tax computations (covered by ph-tax-computations-reverse)
- OCR / document parsing
- Non-deterministic judgments (e.g., "is this property a good investment")
- Property listing/marketplace features
- Payroll, lending (non-housing), banking, securities

### Final Output

`output/opportunity-catalog.md` — ranked list of 15-40 deterministic computations, each entry containing:
- What it computes (inputs → outputs)
- Legal basis (RA/circular/regulation numbers)
- Current state (manual, spreadsheet, partially automated)
- Complexity estimate (branching rules, lookup tables, data dependencies)
- Competitive gap (what existing PH tools don't cover)
- Moat score (how hard to replicate once built)
- Cross-reference to ph-tax-computations-reverse catalog where relevant

## Reference Material

### Primary Legal Sources (fetched in Wave 1)
- Pag-IBIG Fund Circular No. 423 (housing loan guidelines) and amendments
- BSP Circulars on residential real estate lending (LTV limits, stress testing)
- RA 6552 (Maceda Law) — realty installment buyer protection
- RA 9653 (Rent Control Act of 2009) + DHSUD implementing rules
- RA 4726 (Condominium Act) + HLURB/DHSUD rules on common areas
- DHSUD issuances on socialized/economic housing price ceilings
- BP 220 (socialized housing standards) implementing rules
- Local Government Code (RA 7160) — assessment level schedules
- Registry of Deeds fee schedules
- PRC real estate broker regulations

### Secondary Sources (practitioner guides)
- Pag-IBIG Fund official calculator documentation
- Major developer (Ayala Land, SMDC, DMCI) published payment computation terms
- Real estate practitioner blogs and guides with worked examples
- BSP published data on housing loan terms

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
6. **Commit**: `git add -A && git commit -m "loop(ph-realestate-calcs): {{aspect-name}}"`
7. **Exit**

## Analysis Methods By Wave

### Wave 1: Source Acquisition
Fetch and cache legal/regulatory sources. For each aspect:
1. Use web search and web fetch to locate authoritative sources
2. Extract relevant sections (not full documents — focus on computation-relevant provisions)
3. Save processed content to `input/{{source-name}}.md`
4. Note which specific articles, sections, or circular numbers are most relevant for Wave 2

### Wave 2: Computation Extraction
For each computation, produce a mini-spec. **Verification is mandatory:**
1. Extract the formula/logic from the primary legal/regulatory source in `input/`
2. **Spawn a verification subagent** to independently cross-check the extracted logic against 2-3 secondary sources (practitioner guides, official calculators, worked examples from `input/`)
3. If sources conflict: document both versions with citations, flag for manual review
4. If the computation requires judgment (not purely deterministic): mark as "non-deterministic", document why, exclude from final scoring
5. Write to `analysis/{{computation-name}}.md` with:
   - Inputs (with types)
   - Formula / decision tree / lookup table
   - Edge cases and special rules
   - Legal citations (RA + circular + section numbers)
   - Verification status (confirmed / conflict / unverified)
   - Deterministic: yes/no

### Wave 3: Competitive & Automation Gap Analysis
For each aspect:
1. Web search for existing Philippine real estate tools (Pag-IBIG calculator, Lamudi, Hoppler, developer portals, generic mortgage calculators, PropTech startups)
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
4. Cross-reference with `loops/ph-tax-computations-reverse/output/opportunity-catalog.md`
5. Self-review for completeness

## Available Tools

- **Web search & fetch** — for sourcing legal texts, government circulars, practitioner guides
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
