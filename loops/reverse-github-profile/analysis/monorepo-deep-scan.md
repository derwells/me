# Monorepo Deep Scan — derwells

**Analyzed**: 2026-02-25
**Sources**: `../../CLAUDE.md`, `../../projects/`, `../../loops/_registry.yaml`, `../../.github/workflows/ralph-loops.yml`, `../../loops/linkedin-profile-reverse/analysis/`

---

## Summary

The private monorepo (`me`) is the single most revealing artifact about what derwells actually does. Behind the hollow public GitHub profile — 11 repos, no topics, stale student website — is a coherent meta-system: two production AI platforms, a self-authored iterative analysis engine running on GitHub Actions CI, and domain-specific loop work (PH real estate computation, rental business back-office automation) that shows an applied builder instinct well beyond "LLM hobbyist." None of this is visible on the public profile.

---

## What's Inside the Monorepo

### 1. The Ralph Loop Engine — Custom Analysis Infrastructure

The monorepo IS the ralph loop system. Not just a place to store code — an operational pattern for turning unstructured problems into structured outputs.

**How it works**:
- Each "loop" breaks an analysis task into a **wave-based frontier of aspects** (dependency-ordered checklist)
- Each iteration: read frontier → pick one unchecked aspect → analyze → write findings → commit → exit
- State is filesystem-based — survives crashes, restarts, CI interruptions
- Convergence is explicit: all aspects complete + self-review passes → `status/converged.txt`

**What's impressive to a technical person**:
- Designed for autonomous operation — Claude Code processes run headlessly, no human needed per iteration
- GitHub Actions CI is the outer loop: runs every 30 minutes, discovers active loops from `_registry.yaml`, parallelizes with fail-fast=false matrix strategy
- Failure detection built in (3 consecutive failures → stop). Timeout per iteration (1800s). Auto-rebase and push.
- Auto-creates GitHub issues on convergence with iteration count and summary
- The `@tool decorator` analogy: this is an engineering pattern, not just a script. It's a system for building systems.

**CI/CD automation details** (`ralph-loops.yml`):
- Triggers: cron every 30 min (offset from :00/:30 to avoid GitHub Actions stampede)
- `workflow_dispatch` with `loop` parameter for manual override
- Uses `yq` for YAML parsing of registry
- `timeout-minutes: 35` per job, `timeout 1800s` per iteration
- Authenticated git push with GH_PAT
- Convergence hook: creates labeled GitHub issue, updates registry with `converged_at`

### 2. Projects: Two Production AI Systems

**Project 1: Cheerful — Nuts and Bolts AI**
- Full-stack influencer marketing automation platform (3 apps in one private org repo)
- **Backend API**: Python/FastAPI + Temporal.io for durable workflow orchestration
- **Web App**: Next.js 16+ / React 19 + TanStack Query + Zustand + Tailwind/shadcn
- **Context Engine**: Slack bot — Claude Agent SDK + MCP tool orchestration + Onyx RAG
- AI-personalized email drafting (not mail-merge — per-creator custom text via Claude)
- Waterfall creator enrichment pipeline: multi-source bio crawling, website parsing, profile building
- Gmail OAuth multi-account: threading, tracking, sending at scale
- Scale: ~13,100 LOC, ~5,570 commits, 5-person team, 3 apps

**Project 2: Decision Orchestrator — PyMC Labs**
- Discord-based organizational OS: message → classifier → workflow selection → dynamic tool assembly → Claude Agent SDK execution → Discord thread with session persistence
- **The differentiator**: custom hand-built MCP tool registry. Not FastMCP, not a wrapper — actual protocol implementation with `@tool` decorator, context injection, scope-based credential gating
- FCIS architecture (Functional Core, Imperative Shell) — deliberate discipline
- Thread session persistence spanning Claude context + Langfuse + Supabase simultaneously
- Multi-platform integrations: Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io
- Scale: ~36,400 LOC, ~285 Python files, 24 direct dependencies, deployed on Fly.io
- Context: PyMC Labs is the professional services arm of the PyMC project (widely used probabilistic programming library)

**Shared architectural DNA (both projects)**:
- Claude Agent SDK as core orchestration layer
- MCP tool servers (built, not consumed)
- Supabase (PostgreSQL)
- Langfuse LLM observability
- Composio integration framework

### 3. Active Loops (Loop Registry)

6 loops tracked in `_registry.yaml`:

| Loop | Type | Status | Description |
|------|------|--------|-------------|
| `github-profile-reverse` | reverse | active | This very loop |
| `linkedin-profile-reverse` | reverse | **converged** | LinkedIn profile spec (12 analysis files) |
| `ph-tax-computations-reverse` | reverse | active | PH real estate tax computations catalog |
| `ph-land-title-coordinates-reverse` | reverse | active | PH land title → WGS84 coordinates engine spec |
| `ph-realestate-calcs-reverse` | reverse | active | PH non-tax real estate calculations catalog |
| `tsvj-backoffice-automation-reverse` | reverse | active | SEC rental business back-office automation spec |

**Scale of loop work**: 5 active reverse loops across different domains. The LinkedIn loop already converged (12 analysis files). The PH real estate loops show a pattern of domain-specific technical research — building computation engine specs for Philippine real estate (tax, land title coordinate conversion, financing/amortization calculations, regulatory compliance). The `tsvj-backoffice-automation-reverse` loop is scanning a Las Piñas SEC-registered rental property business for automatable back-office processes.

**What this signals**: This person builds research infrastructure AND does domain research with it. The loops aren't demo content — they're real work products being used for real decisions (LinkedIn profile, real estate automation tools, business process specs).

---

## What Would Impress a Technical Person (If They Could See Inside)

1. **The ralph loop engine itself** — a self-authored iterative analysis system with CI automation, convergence detection, failure handling, and auto-issue creation. Most engineers would use Notion or a spreadsheet. This person built a structured convergence machine.

2. **Production MCP implementation (Decision Orchestrator)** — building MCP at the protocol level (not FastMCP) while most of the ecosystem is still using wrappers. Scope-based credential gating per server/channel is a real security architecture decision.

3. **Temporal.io for AI workflows (Cheerful)** — most SaaS apps don't bother with durable execution. Using Temporal for campaign pipelines signals reliability-first engineering instinct, uncommon in the current LLM-tooling ecosystem.

4. **Platform thesis proven twice** — same architectural stack (Claude Agent SDK + MCP + Supabase + Langfuse + Composio) deployed across two entirely different domains (marketing automation, organizational OS). This is deliberate and shows a framework-builder mindset, not a one-off builder.

5. **Domain breadth of loop work** — PH real estate tax computation engines, land title coordinate transformation (PRS92 → WGS84 Helmert), rental business back-office automation. These aren't toy demos; they're computation engine specs ready to be handed to a developer.

---

## Capabilities Completely Invisible From the GitHub Profile

| Capability | Evidence | Visibility |
|------------|----------|------------|
| Claude Agent SDK orchestration | Cheerful, Decision Orchestrator | Zero |
| Temporal.io durable workflows | Cheerful project card | Zero |
| Custom MCP protocol implementation | Decision Orchestrator project card | Zero |
| Production system debugging (OOM postmortems) | Public gists (Feb 2026) | Near-zero (gists, no links) |
| GitHub Actions CI design | `ralph-loops.yml` | Zero (private repo) |
| Self-authored analysis engine (ralph loops) | This monorepo | Zero |
| Langfuse LLM observability | Both project cards | Zero |
| Philippine real estate domain research | 4 active loops | Zero |
| Next.js 16+ / React 19 frontend | Cheerful project card | Zero |
| SQLAlchemy async ORM | Decision Orchestrator | Zero |

---

## Spec Implications

1. **The profile README must name the invisible work explicitly** — "What I build" section should describe Cheerful and Decision Orchestrator in plain language. Not as "some work I can't show you" but as concrete systems with named tech.

2. **The ralph loop engine is a showcase-worthy project** — even if the private monorepo can't be linked, describing it in the README ("I built an iterative analysis engine that runs on GitHub Actions CI") is a strong signal of meta-level engineering thinking.

3. **The crash postmortem gist is gold** — link it directly from the README or pin it as a gist. It proves production systems experience in a way no repo listing can.

4. **Stack keywords to include in bio/topics**: Claude Agent SDK, Temporal.io, MCP protocol, Langfuse, Supabase, FastAPI, discord.py, Fly.io. None of these appear anywhere on the current profile.

5. **Two-line identity frame** (from LinkedIn loop convergence): "AI infrastructure engineer who builds the reliability layer for AI agents." Platform thesis: same stack (Claude Agent SDK + MCP + Langfuse + Supabase) proven across two production orgs in different domains.

6. **Domain research loops (PH real estate)** — these don't belong on the GitHub profile as repos (too specific), but they validate a pattern: this person builds *for* real problems, not demo repos.

7. **PyMC Labs contribution** — one public PR to `pymc-devs/pymc-examples` (Feb 2026) is the only public trace. Should be noted: contributing to open-source Bayesian stats tooling demonstrates breadth.
