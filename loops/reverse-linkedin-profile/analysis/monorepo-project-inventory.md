# Monorepo Project Inventory — derwells

**Analyzed**: 2026-02-23
**Sources**: `../../projects/`, `../../loops/`, `../../CLAUDE.md`, `../../loops/github-profile-reverse/input/github-repos.md`, `../../loops/github-profile-reverse/analysis/repo-inventory.md`

---

## The Central Observation

The public GitHub profile shows 11 repos, mostly old university projects. The real picture — two production AI systems, a custom-built analysis engine, and a coherent platform thesis — is entirely invisible. LinkedIn is the primary surface where this gap can be closed.

---

## Tier 1: Production Professional Work

### 1. Cheerful — Nuts and Bolts AI (current)

**What it is**: Full-stack influencer marketing automation platform. Three apps in one repo: a FastAPI campaign engine, a Next.js/React 19 frontend, and an AI Slack bot for internal team operations.

**The impressive parts (to a stranger)**:
- Built durable campaign workflows with Temporal.io — pipelines that survive crashes and retry intelligently. This is reliability engineering most SaaS apps don't bother with.
- AI-personalized outreach at scale: Claude generates tailored emails per creator, not mail-merge templates with variable insertion.
- Multi-account Gmail OAuth — manages email threading, tracking, and sending across multiple accounts simultaneously.
- Waterfall creator enrichment pipeline — multi-source bio crawling and profile building from scratch.
- Built the internal AI assistant (Slack bot) on Claude Agent SDK + MCP tool orchestration + Onyx RAG.

**Scale signal**: ~13,100 LOC, ~5,570 commits, 5-person team, 3 apps.

**Tech stack worth naming**: Python, FastAPI, Temporal.io, Claude Agent SDK, Next.js 16+, React 19, Supabase, Langfuse, Composio, Gmail API, TanStack Query, Zustand.

**LinkedIn placement**: Primary experience entry (most recent role). Bullets should lead with Temporal + AI personalization as the differentiated engineering story.

---

### 2. Decision Orchestrator — PyMC Labs (current/recent)

**What it is**: Discord-based organizational OS. When a team member sends a message, an intelligent classifier routes it through a workflow engine, dynamically assembles the right MCP tools, and executes with injected context via Claude Agent SDK. The agent's output flows back into Discord with full session persistence.

**The impressive parts (to a stranger)**:
- Built a custom MCP tool registry at protocol level — not FastMCP, not a wrapper, but the actual protocol implementation. Includes a `@tool` decorator, context injection, scope-based credential gating (tools only access credentials scoped to their server/channel).
- Dynamic tool assembly — each request gets a custom-assembled tool set based on workflow + context. This is not plug-and-play; it's infrastructure design.
- Thread session persistence spanning three layers simultaneously: Claude context, Langfuse traces, Supabase records. Sessions survive crashes and produce full audit trails.
- FCIS architecture (Functional Core, Imperative Shell) — deliberate architectural discipline, not just "it works."
- Multi-platform integrations: Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io.

**Scale signal**: ~36,400 LOC, 24 direct dependencies, deployed on Fly.io.

**Context that matters**: PyMC Labs is the professional services arm of the PyMC project — widely used probabilistic programming library. This system is trusted by people who build statistical modeling frameworks for production use.

**Tech stack worth naming**: Python 3.12+, discord.py, Claude Agent SDK, Composio, SQLAlchemy 2.0, FastAPI, Supabase, Langfuse, Fly.io.

**LinkedIn placement**: Second experience entry (or concurrent with Cheerful if overlapping). Headline this as "AI infrastructure" or "agent orchestration" — the MCP registry is the story.

---

## Tier 2: Meta-System (Personal Infrastructure)

### 3. Ralph Loop Engine — Personal (2026)

**What it is**: A self-designed iterative analysis pattern. The system breaks any analysis task into a frontier of aspects organized in dependency waves. Each run does one unit of work, writes findings to disk, commits, and exits. State lives on the filesystem. The loop converges when all aspects pass self-review.

**Why this is worth noting**: Most people build apps. This person builds systems *for building* things — analysis pipelines, self-audit tooling, structured convergence mechanisms. It's meta-cognition made into code.

**Current loops running**: GitHub profile audit, LinkedIn profile spec (this very loop).

**Tech**: TypeScript monorepo, bash runner with timeout/failure detection, file-system state.

**LinkedIn placement**: Featured section or About section mention. Not an experience entry — this is a signal of a certain kind of thinker, best surfaced as a "also built my own analysis engine" aside in the About or a Featured post/link.

---

## Tier 3: Notable Public Repos (Academic → Research)

### 4. crowNNs (2022)

**What it is**: Tree crown detection in airborne RGB imagery. Replaced the RetinaNet-based DeepForest (SOTA) backbone with FCOS. Benchmarked against DeepForest and lidR on a custom GCP T4 GPU workflow.

**Impressive**: Benchmarked against state-of-the-art. Actual ML research framing, not just "I trained a model." Results table comparing methods.

**LinkedIn placement**: Could appear in an "Independent Projects" section or education-adjacent work. Best surfaced via GitHub link in Featured.

---

### 5. LPRNet (2022)

**What it is**: Keras implementation of LPRNet (license plate recognition). Trained on CCPD-Base dataset. Self-directed learning project.

**Impressive**: Paper implementation discipline (not just tutorials). Shows ability to read and reproduce research.

**LinkedIn placement**: Minor mention. Shows ML research literacy.

---

### 6. blocked-floyd-warshall-gpu (2022)

**What it is**: CUDA implementation of the blocked Floyd-Warshall all-pairs shortest path algorithm. High-performance parallel computing.

**Impressive**: Writing CUDA is uncommon. Floyd-Warshall is a classic but the blocked/GPU variant shows real HPC knowledge.

**LinkedIn placement**: Background signal, not a headline item. Useful in Skills (CUDA, parallel computing). The repo has no README — completely invisible as a signal currently.

---

### 7. multithreaded-fileserver (2022)

**What it is**: Concurrent fileserver in C with a linked list. Handles write/read/empty operations with thread synchronization.

**Impressive**: Systems programming in C. Demonstrates low-level fundamentals.

**LinkedIn placement**: Background signal only.

---

### 8. halleys-comet + lotka-volterra (2021)

**What it is**: Numerical simulation work. Halley's comet using 4th-order Runge-Kutta; Lotka-Volterra predator-prey using Regula-Falsi root finding.

**Impressive**: Shows mathematical computing depth, numerical methods beyond "import scipy."

**LinkedIn placement**: Background signal. Could be mentioned in a "computational science" framing if needed.

---

## Tier 4: Historical Breadth (Pattern, Not Portfolio)

These aren't LinkedIn items but reveal the full arc:

| Period | Work | What it shows |
|--------|------|---------------|
| 2020-2021 | PHP web apps (tsvjhub, tsvj_dorm, property_hub), Vue site (tsvj-website) | Full-stack web, earliest output |
| 2020 | Discord bot (shalltear) | Community tooling interest, early |
| 2021 | MIPS implementations in Python/C/Assembly | Deep CS fundamentals, OS coursework |
| 2022 | Ethereum/blockchain work (besu, eth1-quorum, eth1-geth) | Explored blockchain/distributed infra |
| 2022 | Dagster starter, Docker benchmarks | Data engineering tooling |
| 2023 | Compilers (cs155-bf-to-mips in Rust, Yacc/Lex work) | Language theory + systems |
| 2024-2025 | qabot (private Python/AI), current AI agent work | Sharp pivot to LLM engineering |

**The arc**: Academic computational science (numerical methods, systems, HPC) → ML/CV research (paper implementations, benchmark comparisons) → Blockchain/distributed systems exploration → AI agent engineering (production, at scale). Not scattered — iterative depth-seeking.

---

## The Private Work Problem

The most impressive work is private or invisible:

| Work | Visibility | Fix |
|------|------------|-----|
| Cheerful (Nuts and Bolts AI) | Not on LinkedIn (outdated profile) | Add as experience entry |
| Decision Orchestrator (PyMC Labs) | Not on LinkedIn | Add as experience entry |
| Ralph Loop Engine | Private repo, not mentioned anywhere | Surface in About/Featured |
| qabot | Private GitHub repo | Describe in LinkedIn if worth it |
| CUDA/Floyd-Warshall | No README or description | Add desc + README |

---

## Cross-Reference: Platform Thesis

Both production systems share architectural DNA:
- Claude Agent SDK as core orchestration layer
- Custom MCP servers (built, not consumed)
- Supabase (PostgreSQL)
- Langfuse observability
- Composio integrations

This isn't coincidence — it's a deliberate platform approach. This is the LinkedIn story: **building AI infrastructure that other builders run on**, proven across two different domains (marketing automation and organizational coordination).

---

## Summary for LinkedIn Strategy

**What this person actually does** (not the outdated profile version):
Builds AI agent infrastructure. Two production systems at two companies. Custom protocol-level tooling (MCP registry). Durable workflows (Temporal). Real observability (Langfuse). Full-stack when needed (Next.js/React 19). Deep enough in systems (CUDA, C, Temporal internals) to build the layer below, not just the layer on top.

**The narrative thread**: Systems thinker who doesn't just use AI APIs — builds the infrastructure that makes AI agents reliable, observable, and composable. Background in numerical computing and ML research; pivot to production LLM engineering.

**What to emphasize on LinkedIn**:
1. Cheerful + Decision Orchestrator as the centerpiece (two production AI systems)
2. Platform thesis (same architecture, different domains) as the hook
3. Technical specifics that signal real depth: Temporal.io, custom MCP registry, FCIS, Langfuse
4. Academic background arc as credibility foundation (not the headline)

**What NOT to emphasize**:
- Old PHP work
- Forks (moodle, shalltear)
- Generic coursework repos

**Sections this feeds**:
- About section: Platform thesis, arc story, range signal
- Experience: Cheerful (Nuts and Bolts AI), Decision Orchestrator (PyMC Labs)
- Featured: crowNNs or ralph loop engine or a post about building MCP infrastructure
- Skills: Python, FastAPI, Claude Agent SDK, Temporal.io, Next.js, React, Supabase, Langfuse, CUDA, PostgreSQL, MCP, TypeScript
