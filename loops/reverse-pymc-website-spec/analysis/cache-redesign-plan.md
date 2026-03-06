# Analysis: cache-redesign-plan

**Wave:** 1 (Data Acquisition)
**Date:** 2026-03-06
**Status:** Completed with caveat — no formal plan document exists

## Summary

The architecture redesign plan referenced in the loop prompt does not exist as a published document in either PyMC Labs website repository, their issues, PRs, or related locations. The plan exists only as an intent described in the loop configuration.

## What Was Searched

| Location | Method | Result |
|----------|--------|--------|
| `pymc-labs/pymc-rebranded-website` issues (all, #8–#107) | `gh api` | No redesign/architecture issues found |
| `pymc-labs/pymc-labs-website-source` issues (all) | `gh api` | No redesign/migration issues found |
| Rebranded repo README | `gh api` contents | Merge-conflicted README, no plan references |
| Rebranded repo `draft/` directory | `gh api` contents | UI draft pages only (industries, services, solutions) |
| Source repo PRs | `gh api` | No PRs found |
| Monorepo project cards | filesystem | `pymc--decision-orchestrator.md` — unrelated |

## Known Redesign Intent

From the loop prompt, the redesign will split the site into:

1. **Framer** — Marketing pages
2. **Focused Next.js app** — Enrollment (courses, workshops, payments, certificates)
3. **Hugo** — Blog (static generation for ~329 posts)

## Impact on Later Waves

- **Wave 2–3 (Analysis/Content Audit):** No impact. These analyze the as-is state of both repos.
- **Wave 4 (Synthesis):** The unified spec can reference the redesign intent for context, but the spec is a factual baseline document — not constrained by the plan.
- Cross-referencing against the redesign plan (mentioned in Wave 4 synthesis task) will be limited to the high-level intent documented in `input/redesign-plan.md`.

## Output

- Saved `input/redesign-plan.md` documenting the known intent and search results
