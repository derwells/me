<!-- Run via: ralph run reverse-pymc-website-spec | or interactively in Claude Code -->
# PyMC Labs Website Spec — Reverse Ralph Loop

You are an analysis agent in a ralph loop. Each time you run, you do ONE unit of work, then exit.

## Your Working Directory

You are running from `loops/reverse-pymc-website-spec/`. All paths below are relative to this directory.

## Your Goal

Analyze both PyMC Labs website repositories and produce a unified as-is specification:

1. **`pymc-labs/pymc-labs-website-source`** — Current production Lektor static site (Python/Jinja2, `.lr` content files, GitHub Pages + Netlify)
2. **`pymc-labs/pymc-rebranded-website`** — In-progress Next.js + Strapi rewrite (React, REST API, Stripe/Mailchimp integrations)

The final output is a single unified spec document covering:
- Full architecture of both sites (tech stack, routing, build/deploy)
- Data models and content schemas
- API endpoints and integrations
- Component structure (templates/flowblocks for Lektor, React components for Next.js)
- Complete content inventory (every blog post, team member, client, course, page, media asset)
- Dependency audit with EOL/vulnerability status

This spec serves as the factual baseline for an architecture redesign that will split the site into Framer (marketing) + focused Next.js app (enrollment) + Hugo blog.

## Reference Material

### Repos (clone in Wave 1)
- `pymc-labs/pymc-labs-website-source` — clone to `input/pymc-labs-website-source/`
- `pymc-labs/pymc-rebranded-website` — clone to `input/pymc-rebranded-website/`

### Context
- `input/redesign-plan.md` — The architecture redesign plan (fetched in Wave 1 for cross-reference, not a constraint on the spec)

### Cached Sources (after Wave 1)
- `input/pymc-labs-website-source/` — full repo clone
- `input/pymc-rebranded-website/` — full repo clone
- `input/redesign-plan.md` — redesign plan markdown
- `raw/source-file-tree.txt` — file tree of source repo
- `raw/rebranded-file-tree.txt` — file tree of rebranded repo

## What To Do This Iteration

1. **Read the frontier**: Open `frontier/aspects.md`
2. **Find the first unchecked `- [ ]` aspect** in dependency order (Wave 1 before Wave 2 before Wave 3 before Wave 4...)
   - If a later-wave aspect depends on data that doesn't exist yet, skip to an earlier-wave aspect
   - If ALL aspects are checked `- [x]`: write convergence summary to `status/converged.txt` and exit
3. **Analyze that ONE aspect** using the appropriate method (see below)
4. **Write findings** to `analysis/{{aspect-name}}.md`
5. **Update the frontier**:
   - Mark the aspect as `- [x]` in `frontier/aspects.md`
   - Update Statistics (increment Analyzed, decrement Pending, update Convergence %)
   - If you discovered new aspects worth analyzing, add them to the appropriate Wave
   - Add a row to `frontier/analysis-log.md`
6. **Commit**: `git add -A && git commit -m "loop(reverse-pymc-website-spec): {{aspect-name}}"`
7. **Exit**

## Analysis Methods By Wave

### Wave 1: Data Acquisition
Clone both repos and cache reference material. Save file trees to `raw/` for later waves.

- Use `gh repo clone pymc-labs/<repo> input/<repo> -- --depth 1` for cloning (shallow clone to save space, but use full clone if git history is needed for content dating)
- Use `find input/<repo> -type f | sort > raw/<repo>-file-tree.txt` for file trees
- Fetch the redesign plan via `gh api` and save to `input/redesign-plan.md`

### Wave 2: Architecture Analysis
Deep dive into each repo's internals. Read source files directly from `input/` clones.

- For Lektor: examine `*.lektorproject`, `models/*.ini`, `templates/*.html`, `databags/*.json`, `flowblocks/*.ini`, `packages/`
- For Next.js: examine `package.json`, `next.config.*`, `src/app/` or `pages/`, `src/components/`, middleware
- For Strapi: examine `src/api/*/`, content-types, controllers, routes, `config/`
- For integrations: grep for API keys, service URLs, SDK imports (Stripe, Mailchimp, analytics)
- For dependencies: parse `package.json`, `requirements.txt`, check versions against known EOL dates

### Wave 3: Content Audit
Catalog every piece of content by reading the actual content files.

- For Lektor: parse `.lr` files in `content/` — extract frontmatter fields
- For Next.js/Strapi: check seed data, API fixtures, hardcoded content in components
- For media: list images/PDFs with file sizes, identify optimization opportunities
- Produce structured catalogs with counts, dates, and metadata

### Wave 4: Synthesis
Combine all analysis into the final unified spec.

- Read all `analysis/*.md` files
- Write unified spec to `output/pymc-website-spec.md`
- Self-review for completeness: every aspect's findings should be represented
- Cross-reference against the redesign plan to flag any discrepancies discovered

## Available Tools

- **`gh` CLI** — authenticated GitHub access. Use for repos, issues, PRs, releases, API queries.
  - `gh repo clone pymc-labs/<repo>` — clone repos
  - `gh api repos/pymc-labs/<repo>/...` — raw GitHub API access
  - `gh pr list`, `gh issue list` — structured queries
  - Prefer `gh api` with `--jq` for precise data extraction
  - Save raw API responses to `raw/` for later-wave analysis

## Rules

- Do ONE aspect per run, then exit. Do not analyze multiple aspects.
- Always check if required source files exist before starting a later-wave aspect.
- Write findings in markdown with specific numbers, examples, and citations.
- When you discover a new aspect worth analyzing, add it to the frontier in the appropriate wave.
- Keep analysis files focused. One aspect = one file.
- Reference specific file paths in the cloned repos (e.g., `input/pymc-labs-website-source/models/page.ini`).
- For content catalogs, use markdown tables with consistent columns.
- Note anything surprising or undocumented — these are valuable for the redesign baseline.
