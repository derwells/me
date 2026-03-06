# Architecture Redesign Plan — PyMC Labs Website

> **Status:** No standalone plan document was found in either GitHub repository
> (`pymc-labs/pymc-labs-website-source` or `pymc-labs/pymc-rebranded-website`),
> their issues, PRs, wikis, or related org repos. The plan exists as an intent
> described in the loop prompt but has not been published as a formal document.

## Known Intent (from loop context)

The redesign will split the current website into three separate systems:

1. **Framer** — Marketing site (landing pages, about, services, clients)
2. **Next.js app (focused)** — Enrollment system (courses, workshops, payments, certificates)
3. **Hugo** — Blog (static site generator for the ~329 blog posts)

## Current State Being Replaced

| System | Stack | Role |
|--------|-------|------|
| Production site | Lektor (Python/Jinja2) + GitHub Pages/Netlify | Everything: marketing, blog, team, courses |
| In-progress rewrite | Next.js 16 + Strapi CMS + Stripe/Mailchimp | Unified replacement (not yet live) |

## What This Means for the Spec

This spec documents the **as-is state** of both existing systems. The redesign plan
is a downstream consumer of this spec — it uses the factual baseline to inform
architecture decisions. The spec itself is not constrained by the redesign plan.

## Searched Locations

- `pymc-labs/pymc-rebranded-website` issues (#8–#107): No redesign/architecture plan found
- `pymc-labs/pymc-labs-website-source` issues: No redesign/migration plan found
- Both repo READMEs: No plan references
- `pymc-labs/pymc-rebranded-website/draft/` directory: Contains UI draft pages (industries, services, solutions) — no architecture plan
- Monorepo `projects/pymc--decision-orchestrator.md`: Covers Decision Orchestrator, not the website redesign
