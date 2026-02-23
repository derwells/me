# Monorepo Deep Scan — derwells

**Analyzed**: 2026-02-23
**Sources**: `../../projects/`, `../../loops/`, `../../CLAUDE.md`, `../../.github/workflows/`, `../../.claude/skills/`

---

## Summary

The private `me` monorepo is the real portfolio — and it's invisible. Two production AI systems (Cheerful, Decision Orchestrator), a CI-driven iterative analysis engine (ralph loops), and a custom Claude Code skills framework (~2,975 lines of agent programming) live here. A stranger looking at the public GitHub profile sees 11 academic repos. The actual work: building AI infrastructure that other builders run on, proven across two domains, with a coherent architectural thesis.

---

## Tier 1: Production Professional Work

### 1. Cheerful — Nuts and Bolts AI

**What it is**: Full-stack influencer marketing automation platform. Three apps in one repo.

| Metric | Value |
|--------|-------|
| Source files | ~2,170 |
| LOC | ~13,100 |
| Total commits | ~5,570 |
| Apps | 3 (backend, webapp, context-engine) |
| Team size | 5 |

**The three apps**:
- **Backend API** — Python/FastAPI, core campaign engine with durable Temporal.io workflows
- **Web App** — Next.js 16+ / React 19, campaign management UI with multi-step wizard
- **Context Engine** — Slack bot built on Claude Agent SDK + MCP tool orchestration + Onyx RAG

**What's technically impressive**:
1. **Temporal.io durable workflows** — Campaign pipelines that survive crashes, handle retries, maintain state. Most SaaS apps don't bother. This is reliability engineering.
2. **AI-personalized outreach at scale** — Claude generates tailored emails per creator. Not mail-merge templates. Per-recipient personalization.
3. **Waterfall creator enrichment pipeline** — Multi-source bio crawling and website parsing to build creator profiles from scratch.
4. **Multi-account Gmail OAuth** — Manages email threading and tracking across multiple accounts simultaneously.
5. **MCP tool orchestration** — The internal Slack bot uses Claude Agent SDK + custom MCP tools + Onyx RAG for team context retrieval.

**Full tech stack**: Python, FastAPI, Temporal.io, Claude Agent SDK, Gmail API, Composio, Supabase, Langfuse, Next.js 16+, React 19, TanStack Query, Zustand, Tailwind, Radix/shadcn, Slack Bolt, Onyx RAG

---

### 2. Decision Orchestrator — PyMC Labs

**What it is**: Discord-based organizational OS. A programmable orchestration layer where the LLM is the routing engine, not the product.

| Metric | Value |
|--------|-------|
| Python files | ~285 |
| LOC | ~36,400 |
| Direct dependencies | 24 |
| Database tables | 5+ |

**How it works**:
1. Team member sends Discord message
2. Intelligent classifier analyzes intent
3. Workflow engine selects database-driven workflow (scoped to server/channel)
4. Tool assembler dynamically provisions the right MCP tools
5. Claude Agent SDK executes with injected context and scoped credentials
6. Results flow back into Discord thread with full session persistence

**What's technically impressive**:
1. **Custom MCP tool registry — protocol-level** — Not FastMCP, not a wrapper. Hand-built protocol implementation with `@tool` decorator, context injection, scope-based credential gating (tools only access credentials scoped to their server/channel). This is infrastructure design.
2. **Dynamic tool assembly** — Each request gets a custom-assembled tool set based on workflow + context. Not plug-and-play.
3. **Thread session persistence across three layers** — Claude context, Langfuse traces, Supabase records. Sessions survive crashes and produce full audit trails.
4. **FCIS architecture** (Functional Core, Imperative Shell) — Deliberate architectural discipline. Pure functional logic at core, side effects pushed to edges.
5. **Multi-platform integrations**: Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io.

**Context**: PyMC Labs is the professional services arm of the PyMC project — widely used probabilistic programming library. This system is trusted by people who build statistical modeling frameworks for production.

**Full tech stack**: Python 3.12+, discord.py, Claude Agent SDK, Composio, SQLAlchemy 2.0, FastAPI, Supabase, Langfuse, Fly.io

---

## Tier 2: Meta-Systems (Personal Infrastructure)

### 3. Ralph Loop Engine

**What it is**: A self-designed iterative analysis pattern. Breaks any analysis task into a frontier of aspects organized in dependency waves. Each run does one unit of work, writes findings to disk, commits, and exits. Converges when all aspects pass self-review.

**Current loops**:
- `github-profile-reverse` — GitHub profile audit → profile spec (this loop)
- `linkedin-profile-reverse` — Mine repos + work projects → LinkedIn profile spec

**CI runner** (`.github/workflows/ralph-loops.yml`):
- Runs on schedule (every 30 minutes) via cron
- Discovers active loops from `loops/_registry.yaml` (YAML-driven, matrix strategy)
- Per-loop: checks convergence/paused state, runs one iteration via `claude --print`, commits results, creates GitHub issue on convergence
- Timeout: 1800s per iteration, `timeout-minutes: 35` at job level
- Bot identity: `ralph-loop[bot]`
- Supports `workflow_dispatch` for manual override of specific loops

**Why this is impressive**: Most people build apps. This person builds systems *for building* things — analysis pipelines with convergence mechanics, self-audit tooling, structured frontier-based reasoning. The loop runs autonomously in CI. It's meta-cognition made into code.

---

### 4. Claude Code Skills System

**What it is**: A custom library of 14 skills for Claude Code agents — prompting frameworks for how the AI should behave in complex engineering scenarios.

**Skills built** (in `.claude/skills/superpowers:*/`):
- `brainstorming` — Creative feature design workflow
- `dispatching-parallel-agents` — Parallel task orchestration
- `executing-plans` — Plan-to-implementation handoff
- `finishing-a-development-branch` — Branch completion decision tree
- `receiving-code-review` — Technical rigor in review response
- `requesting-code-review` — Structured review request
- `subagent-driven-development` — Multi-agent coordination
- `systematic-debugging` — Root cause tracing methodology
- `test-driven-development` — TDD process with anti-patterns reference
- `using-git-worktrees` — Safe isolated feature development
- `using-superpowers` — Meta-skill: how to discover and invoke other skills
- `verification-before-completion` — Evidence-first completion gate
- `writing-plans` — Spec to plan translation
- `writing-skills` — Meta-skill for creating new skills

**Scale**: ~2,975 lines across all SKILL.md files, plus supporting reference docs, examples, test scenarios.

**Why this is impressive**: This is prompt engineering at framework level. Not one-off prompts — a coherent system for making AI agents more reliable, disciplined, and self-aware. The `writing-skills` meta-skill for creating new skills is especially recursive.

---

## Shared Architectural DNA (Platform Thesis)

Both production systems (Cheerful and Decision Orchestrator) share identical infrastructure choices:

| Component | Choice | Why it matters |
|-----------|--------|----------------|
| AI orchestration | Claude Agent SDK | Consistent, production-grade |
| Tool protocol | Custom MCP servers | Built, not just consumed |
| Database | Supabase (PostgreSQL) | Same data layer |
| Observability | Langfuse | LLM tracing across both |
| Integrations | Composio | 50+ external connectors |

This is not coincidence — it's a deliberate platform approach across two different domains (marketing automation and organizational coordination). The same architectural decisions applied twice = a platform thesis, not just "I used Claude once."

---

## What Would Impress a Technical Person

If someone could see inside the monorepo:

1. **The custom MCP registry** in Decision Orchestrator — protocol-level implementation with scope-based credential gating is not something most people build. It's architecture.
2. **Temporal.io usage** in Cheerful — using Temporal for campaign orchestration shows production reliability thinking that most developers skip.
3. **Scale of Cheerful**: 5,570 commits, 3 apps, 5-person team. This is a shipped product, not a toy.
4. **The ralph loop engine running in CI** — autonomous AI analysis pipelines on a 30-minute cron. Convergence detection. Bot identity. GitHub issue creation. This is genuinely novel.
5. **14 Claude Code skills** — a framework for disciplined AI agent behavior. Most people use AI tools; this person built tooling *for* AI tools.
6. **The platform thesis** — two production systems with shared architectural DNA. Intentional, not accidental.

---

## What's Completely Invisible From the Public GitHub Profile

| Hidden asset | Why it matters |
|-------------|----------------|
| Cheerful (private) | Production full-stack AI platform, 5,570 commits |
| Decision Orchestrator (private) | 36,400 LOC, custom MCP registry, PyMC Labs infra |
| Ralph loop engine (private) | Novel analysis pattern running in CI |
| Claude Code skills system (private) | 14-skill AI agent framework, ~2,975 lines |
| Platform thesis | Same architecture across two domains — shows intentionality |
| FCIS architecture | Deliberate engineering discipline, invisible without code access |
| Temporal.io usage | Durable workflows show production reliability mindset |

**The delta is enormous**: Public profile reads "scattered old university repos." Actual work: production AI infrastructure at two companies, a custom MCP registry built at protocol level, a self-running analysis engine, and a skills framework for AI agents.

---

## Spec Implications

1. **Profile README must name the private work** — Can't link private repos, but can describe them: "building AI agent infrastructure at [company]." The story lives in the README, not the repo list.
2. **The platform thesis is the hook** — "Same architecture, two different domains" is the punchy technical identity. This is rarer than it sounds.
3. **MCP registry = the differentiator** — Most people use MCP tools; this person built the registry layer. Lead with that.
4. **Ralph loops deserve a mention** — Even if the repo is private, describing "I built an iterative analysis engine that runs in CI" signals a certain kind of thinker.
5. **crowNNs is the best public proxy** — It's the most technically impressive visible repo (benchmarked SOTA), so it should be pinned and well-described as a signal of technical depth.
6. **The GitHub site (`derwells.github.io`) should be the bridge** — Update it to tell the real story; the profile bio can link to it.
