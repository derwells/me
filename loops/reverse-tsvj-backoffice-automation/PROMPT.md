# Back-Office Automation Survey — Reverse Ralph Loop

You are an analysis agent in a ralph loop. Each time you run, you do ONE unit of work, then exit.

## Your Working Directory

You are running from `loops/tsvj-backoffice-automation-reverse/`. All paths below are relative to this directory.

## Your Goal

Survey every back-office task in a medium-scale Las Piñas commercial + residential rental property business (SEC-registered corporation, ~3-10 properties, ~20-100 units), and produce a **process catalog with lightweight feature specs** for automatable tasks.

The business is a SEC-registered PH corporation with board members. An external accounting agency handles BIR filings, but preparing the data for handoff is currently manual. Both commercial and residential (rent-controlled) tenants exist in roughly equal numbers.

### Scope

**Primary — Operational back-office tasks:**
- Rent billing and collection tracking
- Rent escalation calculations (controlled vs commercial)
- Late payment penalty computation
- Utility billing: water meter reading → per-unit bills, electric bill apportionment
- Security deposit tracking (collection, deductions, refund with interest)
- Lease contract generation (new tenants)
- Lease renewal and extension processing
- Payment allocation and balance tracking
- Monthly billing statement generation

**Secondary — Accounting agency handoff:**
- Rent roll preparation (spreadsheet the accountant needs monthly)
- Official receipt data for BIR-registered OR generation
- 2307 certificate tracking (received from corporate tenants quarterly)
- Expense voucher compilation for the accountant
- Data needed for BIR forms: 1702Q, 2550Q/2551Q, 1601-EQ, 1604-E
- DST computation on new/renewed leases
- SEC annual filing data: GIS, AFS support data

**Tertiary — Compliance tracking:**
- Business permit and barangay clearance renewal dates per property
- Real property tax payment tracking and penalty computation
- Fire safety and sanitary permit renewals
- Board resolution tracking for lease authorizations

### Out of Scope
- Building any software — this loop produces the analysis/specs only
- OCR for handwritten receipt encoding (noted as a separate ML problem)
- Tax engine computations (covered by the `ph-tax-computations-reverse` loop)
- Property acquisition, construction, or selling workflows

### Final Output

`output/process-catalog.md` — catalog of all back-office tasks, each entry containing:
- Process name and description
- Inputs and outputs (what data goes in, what comes out)
- Current method (fully manual, spreadsheet, partially in Crispina, outsourced to accountant)
- PH regulatory rules that govern this process (with legal citations)
- Automability score (1-5): 1 = requires human judgment, 5 = purely deterministic
- What Crispina already built (if anything) — based on codebase analysis
- **Lightweight feature spec**: data model sketch, formula/logic, edge cases, inputs/outputs

Pain and frequency scores are intentionally excluded — the business owner will add these based on operational experience.

## Reference Material

### Primary Source: Crispina Codebase
The existing (discontinued) property management system at `tsvjph/crispina` on GitHub. Use `gh` CLI to access. This codebase represents the owner's intent for features — mine it for what was planned and built, but do not treat its calculations as authoritative. The PH regulatory research is the source of truth for correct rules.

**Key areas to examine:**
- `/server/src/db/model/` — SQLAlchemy ORM models (lease, tenant, charge, payment, transaction)
- `/server/src/api/schema/` — Pydantic schemas showing data shapes
- `/server/src/api/service/math.py` — Compound interest calculations
- `/server/src/api/service/date.py` — Date range splitting
- `/water/` — Standalone water utility billing calculator
- `/server/src/script/seed.py` — What charge types are seeded

### PH Regulatory Sources (fetched in Wave 1)
- RA 9653 (Rent Control Act) + latest NHSB resolution for allowable increases
- Civil Code Articles 1654-1688 (lease obligations)
- BIR regulations for corporate rental income (EWT, VAT, percentage tax, DST)
- Meralco and Maynilad rate schedules and sub-metering rules
- SEC corporate filing requirements (GIS, AFS)
- Local Government Code: RPT, business permits

### Cached Sources (after Wave 1)
After Wave 1, all fetched content lives in `input/`. Later waves read from these instead of re-fetching.
- `input/crispina-models.md` — extracted database models and schemas
- `input/crispina-water-calculator.md` — water billing logic from the standalone tool
- `input/crispina-services.md` — math and date service logic
- `input/rent-control-rules.md` — RA 9653 + NHSB resolution rules
- `input/corporate-rental-tax.md` — BIR obligations for SEC-registered rental corporation
- `input/utility-billing-regulations.md` — Meralco/Maynilad sub-metering rules
- `input/security-deposit-rules.md` — PH deposit laws (residential controlled vs commercial)
- `input/lease-contract-requirements.md` — Civil Code lease provisions + corporate requirements
- `input/accounting-agency-handoff.md` — what data the external accountant needs monthly/quarterly/annually

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
6. **Commit**: `git add -A && git commit -m "loop(tsvj-backoffice-automation): {{aspect-name}}"`
7. **Exit**

## Analysis Methods By Wave

### Wave 1: Source Acquisition
Fetch and cache reference material. For each aspect:
1. Use `gh` CLI to fetch Crispina codebase files, or web search for PH regulatory sources
2. Extract relevant sections — focus on rules, formulas, and data structures
3. Save processed content to `input/{{source-name}}.md`
4. Note which specific laws, articles, or code patterns are most relevant for Wave 2

**For Crispina aspects:** Use `gh api repos/tsvjph/crispina/contents/<path> --jq '.content' | base64 -d` to read files. Focus on extracting: model fields, relationships, business logic in services, schema shapes.

**For regulatory aspects:** Use web search to find authoritative sources (lawphil.net, bir.gov.ph, respicio.ph, etc.). Extract the specific rules applicable to a Las Piñas SEC-registered rental corporation.

### Wave 2: Process Analysis & Feature Specs
For each back-office task, produce a process analysis + lightweight feature spec. **Verification is mandatory:**
1. Read relevant `input/` files from Wave 1
2. Document the current process (how it's done manually or in spreadsheets)
3. Extract the formula/logic/rules from regulatory sources
4. **Spawn a verification subagent** to cross-check extracted rules against 2-3 secondary sources
5. Document what Crispina already built for this process (from `input/crispina-*.md`)
6. Write a lightweight feature spec: inputs, outputs, data model sketch, formula, edge cases
7. Score automability (1-5): 1 = requires human judgment, 5 = purely deterministic/formulaic

Write to `analysis/{{process-name}}.md` with:
- Process description (what, when, who does it)
- Current method (manual, spreadsheet, Crispina, outsourced)
- Regulatory rules with legal citations
- Formula / decision tree / lookup table
- Edge cases and special rules
- What Crispina built (model fields, endpoints, gaps)
- Lightweight feature spec (inputs, outputs, data model, logic)
- Automability score with justification
- Verification status (confirmed / conflict / unverified)

### Wave 3: Handoff & Integration Analysis
For tasks that produce data for the accounting agency or interact with BIR/SEC:
1. Map the data flow: property manager → accountant → BIR/SEC
2. Identify format requirements (what the accountant specifically needs)
3. Document which BIR forms each data point feeds into
4. Identify automation opportunities in the handoff itself
5. Note which processes should generate data for other processes (dependencies)

### Wave 4: Synthesis & Catalog
1. Compile all process analyses into `output/process-catalog.md`
2. Group by category: billing, compliance, contracts, handoff
3. Identify cross-cutting concerns (e.g., VAT affects billing, handoff, and compliance)
4. Map process dependencies (what feeds what)
5. Leave columns for owner-scored pain and frequency (blank for owner to fill)
6. Self-review for completeness

## Available Tools

- **`gh` CLI** — authenticated GitHub access for the Crispina codebase at `tsvjph/crispina`
  - `gh api repos/tsvjph/crispina/contents/<path>` — read files
  - `gh api -X GET 'https://api.github.com/search/code?q=<term>+repo:tsvjph/crispina'` — search code
- **Web search & fetch** — for PH regulatory sources, utility rate schedules, BIR guidelines
- **Subagents** — spawn for verification cross-checks in Wave 2 and regulatory research
  - Always use subagents to verify extracted rules against secondary sources
  - Subagents can web search independently

## Rules

- Do ONE aspect per run, then exit. Do not analyze multiple aspects.
- Always check if required source files exist before starting a later-wave aspect.
- **Verification protocol**: Every Wave 2 process analysis MUST cross-check regulatory rules against at least 2 independent sources using a subagent. Single-source extractions are not acceptable.
- If sources conflict, document the conflict with full citations — do not resolve by guessing.
- Mark any process requiring significant human judgment as low-automability with explanation.
- Write findings in markdown with specific rules, formulas, examples, and legal citations.
- When you discover a new back-office task worth analyzing, add it to the frontier in the appropriate wave.
- Keep analysis files focused. One process = one file.
- Save raw fetched content to `raw/`, processed analysis to `analysis/`.
- **Crispina is reference, not truth**: Use the codebase to understand intent, but verify all calculations against PH law.
- **This is a SEC-registered corporation**: All tax, compliance, and documentation rules should reflect corporate (not individual) requirements.
