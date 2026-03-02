# TSVJ Backoffice Web App — Reverse Ralph Loop

You are an analysis agent in a ralph loop. Each time you run, you do ONE unit of work, then exit.

## Your Working Directory

You are running from `loops/reverse-tsvj-webapp-spec/`. All paths below are relative to this directory.

## Your Goal

Produce a **web application specification** for the TSVJ backoffice automation system. The business processes are already defined in `input/process-catalog.md` (from the completed `reverse-tsvj-backoffice-automation` loop). This loop translates that process catalog into a buildable web app spec.

**Two outputs:**
1. `output/architecture.md` — Stack decisions, project structure, data model, API surface, auth, deployment
2. `output/feature-specs/F0.md` through `P14.md` — One implementation spec per process, each self-contained enough for a forward loop to pick up independently

**Target stack:** Next.js + tRPC + Drizzle ORM + Zod + Supabase (Postgres) + Turborepo monorepo

**Users:** Two roles — Admin (property manager, full access) and Accountant (read-only views, export/download)

**Backpressure constraint:** Each feature spec must include deterministic verification that the forward loop agent runs before marking the task complete. The forward loop cannot advance to the next feature until all verification commands exit 0 and all acceptance criteria are checked. This prevents drift, hallucination, and compounding errors across iterations.

## Reference Material

### Primary Input
- `input/process-catalog.md` — The converged process catalog (14 processes + foundation, ~95 regulatory rules, dependency graph, MVP pipeline, compliance calendar)

### Source Analysis (from prior loop)
The process catalog references detailed analysis files. If you need deeper context on any process, check `../reverse-tsvj-backoffice-automation/analysis/` for the full analysis per aspect.

### Cached Sources (after Wave 1)
After Wave 1, these files will exist in `input/`:
- `input/process-catalog.md` — already present (copied from prior loop)
- `input/data-model-extract.md` — entities and relationships extracted from process catalog
- `input/ui-requirements-extract.md` — UI-relevant requirements (views, forms, dashboards, exports) extracted from process catalog
- `input/cross-cutting-extract.md` — cross-cutting concerns (VAT, EWT, tenant type, numbering, lease events) extracted

## What To Do This Iteration

1. **Read the frontier**: Open `frontier/aspects.md`
2. **Find the first unchecked `- [ ]` aspect** in dependency order (Wave 1 before Wave 2 before Wave 3...)
   - If a later-wave aspect depends on data that doesn't exist yet, skip to an earlier-wave aspect
   - If ALL aspects are checked `- [x]`: write convergence summary to `status/converged.txt` and exit
3. **Analyze that ONE aspect** using the appropriate method (see below)
4. **Write findings** to the appropriate location:
   - Wave 1 extractions → `input/` files
   - Wave 2 architecture decisions → `analysis/` files
   - Wave 3 feature specs → `output/feature-specs/` files
   - Wave 4 synthesis → `output/architecture.md` and review
5. **Update the frontier**:
   - Mark the aspect as `- [x]` in `frontier/aspects.md`
   - Update Statistics (increment Analyzed, decrement Pending, update Convergence %)
   - If you discovered new aspects worth analyzing, add them to the appropriate Wave
   - Add a row to `frontier/analysis-log.md`
6. **Commit**: `git add -A && git commit -m "loop(reverse-tsvj-webapp-spec): <aspect-name>"`
7. **Exit**

## Analysis Methods By Wave

### Wave 1: Source Extraction
Read `input/process-catalog.md` and extract structured summaries into `input/` files. Each extraction focuses on one dimension of the catalog:
- **Data model extract:** All entities, fields, relationships, and constraints mentioned across all processes. Normalize into a unified entity list.
- **UI requirements extract:** Every view, form, dashboard, table, export, and report mentioned. Group by user role (admin vs accountant). Include ASCII mockups for key screens.
- **Cross-cutting extract:** VAT treatment matrix, EWT rules, tenant type bifurcation, sequential numbering, lease lifecycle events — as they affect the web app design.

### Wave 2: Architecture Decisions
Depends on Wave 1 data. For each architectural concern, make a concrete decision with rationale. Write to `analysis/`.
- Evaluate options, pick one, explain why
- Reference the extracted data to justify decisions
- Keep decisions concrete: specific library versions, specific patterns, specific folder structures
- For UI views: use ASCII art to show layout, not code. Describe what each section shows and how the user interacts with it.

### Wave 3: Feature Specs
Depends on Wave 2 decisions. For each process (F0, P1-P14), write a self-contained implementation spec to `output/feature-specs/`. Each spec includes:
- **Summary:** What this feature does (1-2 sentences)
- **Data model:** Drizzle schema (tables, columns, types, relations) — reference shared entities from F0
- **API surface:** tRPC router procedures (queries, mutations) with Zod input/output schemas described
- **UI views:** ASCII mockups of each screen/component. Describe layout, data displayed, user actions. Mark which role can access each view.
- **Business logic:** Core computation rules, edge cases, regulatory constraints (reference process catalog for full rules)
- **Validation rules:** Zod schemas for all user inputs
- **Dependencies:** Which other features must exist first (always F0 at minimum)

#### Backpressure Sections (REQUIRED in every feature spec)

Every feature spec MUST include these three sections at the end. These are what the forward loop uses to verify its work before advancing:

- **Verification Commands:** Exact shell commands the forward loop agent runs after implementing the feature. Each command must have a deterministic pass/fail (exit code 0 = pass). Include:
  - `pnpm run build` — TypeScript compiles without errors
  - `pnpm run test -- <test-file-pattern>` — feature-specific tests pass
  - `pnpm run lint` — no lint errors introduced
  - Smoke test commands where applicable (e.g., `curl` against dev server to verify API responses)
  - Database verification (e.g., `pnpm drizzle-kit check` for schema consistency)

- **Acceptance Criteria:** Checkboxes (`- [ ]`) that the forward loop marks `[x]` ONLY after running verification commands. Each criterion must be binary (pass/fail) and testable — no subjective criteria like "looks good" or "works correctly." Format: `- [ ] <what to verify> — <how to verify it>`

  Examples of GOOD criteria:
  - `- [ ] Tenant CRUD — POST /api/trpc/tenant.create with valid payload returns tenant object with id`
  - `- [ ] TIN validation — POST with invalid TIN format returns ZodError with path ["tin"]`
  - `- [ ] Accountant role blocked — GET /api/trpc/tenant.create with accountant session returns UNAUTHORIZED`

  Examples of BAD criteria (do not write these):
  - `- [ ] The form works correctly`
  - `- [ ] Data is properly validated`
  - `- [ ] UI looks good`

- **Done Signal:** The exact string the forward loop outputs after all criteria pass: `<task-complete>{spec-id}</task-complete>` (e.g., `<task-complete>F0</task-complete>`). The forward loop must NOT output this string if any verification command failed or any acceptance criterion is unchecked.

### Wave 4: Synthesis
Depends on all Wave 3 specs.
- **Architecture doc compilation:** Combine Wave 2 decisions into `output/architecture.md`
- **Self-review:** Verify all 14 processes + F0 are covered, cross-cutting concerns are consistent, feature specs are independently actionable, and the forward loop has everything it needs

## Available Tools

- **`gh` CLI** — authenticated GitHub access for any repo research needed
- **Web search/fetch** — for checking latest library versions, API docs, etc.
- **File system** — read/write to this loop's directories

## Rules

- Do ONE aspect per run, then exit. Do not analyze multiple aspects.
- Always check if required source files exist before starting a later-wave aspect.
- Write findings in markdown with specific, concrete decisions — not "consider using X" but "use X because Y."
- When you discover a new aspect worth analyzing, add it to the frontier in the appropriate wave.
- Keep analysis files focused. One aspect = one file.
- For UI mockups, use ASCII art. Show layout structure, not pixel-perfect design. Label sections with what data they show and what actions are available.
- Feature specs must be self-contained: a developer (or forward loop) should be able to implement the feature from the spec alone + the architecture doc + the process catalog.
- Reference the process catalog for regulatory rules — don't duplicate the full rule text, just cite the process ID and rule name.
- The forward loop will implement features in the MVP order from the process catalog: F0 → P1 → P5 → P6 → P11, then P2+P3+P4, then P8+P9+P10, then P7+P12+P13+P14.
- **Backpressure is non-negotiable.** Every feature spec must have Verification Commands, Acceptance Criteria, and Done Signal sections. Without these, the forward loop has no way to confirm its work and errors will compound. Write verification that catches the specific failure modes for each feature (wrong computation, missing validation, broken auth, etc.), not just generic "build passes."
- Acceptance criteria should cover: (1) happy path works, (2) validation rejects bad input, (3) role-based access is enforced, (4) edge cases from the process catalog are handled, (5) data model constraints are enforced at the DB level.
