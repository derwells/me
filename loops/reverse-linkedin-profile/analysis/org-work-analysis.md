# Org Work Analysis — derwells

**Analyzed**: 2026-02-23
**Sources**: `../../projects/nutsandbolts--cheerful.md`, `../../projects/pymc--decision-orchestrator.md`, GitHub API (live), `analysis/monorepo-project-inventory.md`, `loops/github-profile-reverse/analysis/repo-inventory.md`

---

## Discovery Method

`gh api /user/orgs` returned no accessible org data in this environment. The public GitHub API (`/users/derwells/orgs`) returns an empty array — org memberships are private (standard for professional work). The project context cards in `../../projects/` are the authoritative source and contain full tech stack, feature, and scale detail.

The `pymc-examples` fork (updated Feb 2026) on the public profile corroborates active work with PyMC Labs.

---

## Org 1: Nuts and Bolts AI

**Project**: Cheerful — email automation platform for influencer marketing
**Role context**: Full-stack engineer on a 5-person team
**Repo visibility**: Private (not on GitHub public profile)
**LinkedIn alignment**: Primary experience entry (current role)

### What they built

Three apps in one codebase:
1. **Backend API** — Python/FastAPI campaign engine with durable Temporal.io workflows
2. **Web App** — Next.js 16+ / React 19 frontend with multi-step campaign wizard
3. **Context Engine** — Internal Slack bot: Claude Agent SDK + MCP tool orchestration + Onyx RAG

### Tech stack (full)

| Layer | Technologies |
|-------|-------------|
| Backend | Python, FastAPI, Temporal.io |
| AI/Agent | Claude Agent SDK, MCP servers |
| Integrations | Gmail API (OAuth multi-account), Composio (50+ connectors) |
| Data | Supabase (PostgreSQL) |
| Observability | Langfuse |
| Frontend | Next.js 16+, React 19, TanStack Query, Zustand, Tailwind, Radix/shadcn |

### Domain and differentiation

**Domain**: Influencer marketing automation — creator discovery, AI-personalized outreach, campaign execution at scale.

**What makes it technically impressive (to a stranger)**:
- **Temporal.io for durable workflows**: Campaign execution pipelines survive crashes and retry intelligently. This is reliability engineering most SaaS apps skip.
- **Individualized AI outreach**: Claude generates a unique email per creator, not mail-merge with variable insertion. This is a meaningful distinction.
- **Multi-account Gmail orchestration**: Threading, tracking, and sending across multiple accounts simultaneously.
- **Waterfall enrichment pipeline**: Multi-source bio crawling to build creator profiles from scratch.
- **Internal AI assistant**: Built the team's internal tool (Slack bot) from scratch using Agent SDK + MCP + RAG. Not just using a product — building the infrastructure.

### Scale signals

- ~13,100 LOC, ~5,570 commits
- 3 apps, 5-person team
- Production system

### How to frame on LinkedIn

**Title**: Full-Stack AI Engineer (or Software Engineer — AI Systems)
**Company**: Nuts and Bolts AI
**Location**: Remote / Philippines (or Remote)

**Bullet framing order** (most impressive first):
1. Durable campaign execution engine (Temporal.io) — reliability story
2. AI-personalized creator outreach at scale (Claude SDK) — AI story
3. Multi-account Gmail orchestration — integration story
4. Internal Slack AI assistant (MCP + RAG) — platform story
5. Full-stack: Next.js 16+ / React 19 frontend with campaign wizard UX — breadth signal

---

## Org 2: PyMC Labs

**Project**: Decision Orchestrator — Discord-based organizational OS
**Role context**: Engineer building internal AI infrastructure
**Repo visibility**: Private
**LinkedIn alignment**: Second experience entry (concurrent or sequential with Cheerful)

### What they built

A programmable agent orchestration layer: Discord message → intent classification → workflow selection → dynamic MCP tool assembly → Claude Agent SDK execution → thread-persistent response.

This is infrastructure, not an app. The LLM is the routing engine, not the product.

### Tech stack (full)

| Layer | Technologies |
|-------|-------------|
| Core | Python 3.12+, discord.py |
| AI/Agent | Claude Agent SDK |
| MCP System | Custom protocol-level implementation (NOT FastMCP) |
| Integrations | Composio (Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io) |
| Data | Supabase (PostgreSQL), SQLAlchemy 2.0 |
| Infrastructure | FastAPI (webhooks), Fly.io (deployment) |
| Observability | Langfuse |
| Architecture | FCIS (Functional Core, Imperative Shell) |

### Domain and differentiation

**Domain**: Internal organizational infrastructure for PyMC Labs — AI-powered coordination layer across teams.

**PyMC Labs context**: Professional services and product arm of the PyMC probabilistic programming project — a widely used open-source framework for Bayesian statistical modeling. The people this system serves build production statistical software. High trust bar.

**What makes it technically impressive (to a stranger)**:
- **Custom MCP registry (protocol level)**: Not FastMCP, not a wrapper. Hand-built protocol implementation with `@tool` decorator, context injection at runtime, and scope-based credential gating. Each tool only accesses credentials scoped to its server/channel context.
- **Dynamic tool assembly**: Each incoming request gets a custom-assembled tool set based on workflow + context. This is not plug-and-play configuration — it's infrastructure design.
- **Three-layer session persistence**: Sessions span Claude context windows, Langfuse traces, and Supabase records simultaneously. Survive crashes. Produce full audit trails.
- **FCIS architecture**: Functional Core, Imperative Shell. Deliberate architectural discipline, not "it works." Shows systems design literacy.
- **7 platform integrations**: Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io — a real integration surface, not demo-ware.

### Scale signals

- ~36,400 LOC
- 24 direct dependencies
- 5+ database tables
- Deployed on Fly.io (production)

### How to frame on LinkedIn

**Title**: AI Infrastructure Engineer (or Software Engineer — Agent Systems)
**Company**: PyMC Labs
**Location**: Remote / Philippines (or Remote)

**Bullet framing order** (most impressive first):
1. Custom MCP tool registry (protocol level) — the differentiating technical story
2. Dynamic tool assembly + scope-based credential gating — the architecture story
3. Three-layer session persistence (Claude + Langfuse + Supabase) — reliability story
4. Discord-based organizational OS powering PyMC Labs operations — product story
5. 7 platform integrations (Toggl, Google Workspace, Xero, Fly.io, and more) — breadth signal

---

## Cross-Org Pattern: The Platform Thesis

Both orgs show the same architectural DNA:

| Shared component | Used in |
|-----------------|---------|
| Claude Agent SDK (core orchestration layer) | Both |
| Custom MCP servers (built, not consumed) | Both |
| Supabase (PostgreSQL) | Both |
| Langfuse (LLM observability) | Both |
| Composio (integration framework) | Both |
| Python backend | Both |

**What this means for LinkedIn**: This isn't coincidence — it's deliberate platform-level thinking. The person isn't learning the stack twice; they're applying a proven architecture to new domains. This is the LinkedIn story: **an AI infrastructure builder who owns a coherent technical platform, not just a set of job skills.**

This cross-org consistency is rare and worth surfacing explicitly in the About section.

---

## LinkedIn Role Sequencing

**Critical question**: Are these roles concurrent or sequential?

From the project cards, both are described as "current" work. The honest framing is to list them as potentially overlapping:
- If concurrent: list both with overlapping date ranges (acceptable on LinkedIn)
- If sequential: list most recent first, other second

Both should appear as experience entries. Neither is a freelance gig or side project — these are production systems at real companies.

**Recommended order on LinkedIn** (most recent first):
1. Nuts and Bolts AI — Cheerful (if current)
2. PyMC Labs — Decision Orchestrator (if prior or concurrent)

Date ranges will need to be filled in by Derick (exact start/end dates unknown from available data).

---

## What's Currently Missing on LinkedIn

Based on the GitHub profile snapshot (functionally invisible, no bio, no company field), neither of these roles is currently on the LinkedIn profile:

| Org | On LinkedIn? | Cost of gap |
|-----|-------------|------------|
| Nuts and Bolts AI (Cheerful) | No | Biggest gap — most recent production work |
| PyMC Labs (Decision Orchestrator) | No | Second gap — strongest technical story |

Both need to be added as experience entries. This is the highest-ROI update.

---

## Summary

Derick works with two orgs:

1. **Nuts and Bolts AI**: Full-stack AI engineering on an influencer marketing automation platform. Story: durable AI workflows at scale (Temporal + Claude SDK) + internal platform tooling.

2. **PyMC Labs**: AI infrastructure engineering for an internal organizational OS. Story: protocol-level MCP registry design + multi-layer session persistence. Trusted by a team that builds production probabilistic programming tools.

Both roles together make the LinkedIn story: **"I build the infrastructure layer that makes AI agents reliable, observable, and composable — and I've proven it across two different production domains."**

Neither org appears on the current LinkedIn profile. Adding them is the most urgent LinkedIn update.
