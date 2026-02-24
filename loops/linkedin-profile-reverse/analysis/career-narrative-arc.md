# Career Narrative Arc — derwells

**Analyzed**: 2026-02-24
**Sources**: `analysis/monorepo-project-inventory.md`, `analysis/org-work-analysis.md`, `analysis/github-profile-cross-ref.md`, `analysis/reference-formula-extraction.md`, `analysis/current-profile-snapshot.md`

---

## The Central Insight

The career arc is not a pivot — it's a **deepening**. Every phase added a lower-level understanding of the same problem: how do you make computation reliable at scale?

University: numerical methods (solvers, convergence), HPC (CUDA, parallel algorithms), systems (C, MIPS, concurrency).
Research: ML paper implementations, benchmark comparisons, rigorous evaluation.
Production: AI orchestration infrastructure — the layer that makes LLMs reliable, observable, and composable.

The person who builds Temporal.io durable workflows and a protocol-level MCP registry is the **same person** who wrote blocked Floyd-Warshall in CUDA and implemented Runge-Kutta from scratch. The later work is not a departure — it's what you get when someone with that foundation encounters LLMs.

---

## Chronological Arc (Oldest to Most Recent)

### Phase 1: Foundation — Systems, Numerical Computing, Low-Level (2020–2022)

**What happened:**
- First code output: PHP web apps (`tsvjhub`, `tsvj_dorm`, `property_hub`), Vue.js site — earliest full-stack signal
- Discord bot (`shalltear`) — early systems/community tooling interest
- MIPS implementations in Python/C/Assembly — CS fundamentals, OS coursework
- Halley's comet: 4th-order Runge-Kutta orbital simulation
- Lotka-Volterra: predator-prey dynamics using Regula-Falsi root finding
- `multithreaded-fileserver` (C): concurrent fileserver with linked lists, thread synchronization
- `blocked-floyd-warshall-gpu` (CUDA): blocked Floyd-Warshall, GPU-parallel, all-pairs shortest path

**What this phase demonstrates:**
Goes below the abstraction. Uses numerical methods when scipy would suffice. Writes CUDA when a CPU would work. Implements fileserver from scratch in C. This isn't coursework compliance — it's orientation. The pattern is: *I want to understand the layer below.*

**Narrative function:** This is the foundation that explains everything that comes after. The Temporal.io choice, the protocol-level MCP registry, the FCIS architecture — all of these make more sense when you know the person's instinct is to go one layer deeper than required.

---

### Phase 2: Research — ML/CV, Rigorous Evaluation (2022)

**What happened:**
- `crowNNs`: Tree crown detection in airborne RGB imagery. Replaced DeepForest's RetinaNet backbone with FCOS; benchmarked against DeepForest and lidR on GCP T4 GPU. Compared methods with a results table.
- `LPRNet`: Keras implementation of a license plate recognition ArXiv paper. Self-directed paper reproduction.
- Ethereum/blockchain exploration (Besu, Quorum, Geth) — distributed systems and consensus mechanisms
- Dagster starter, Docker benchmarks — data engineering tooling

**What this phase demonstrates:**
Research rigor. Doesn't just "train a model" — benchmarks against SOTA and presents a comparison table. Reads papers and reproduces them. Evaluates distributed consensus mechanisms. This is the scientific method applied to software: hypothesis → implementation → comparison.

**Narrative function:** This phase bridges the low-level systems foundation with production work. ML research taught *how to evaluate*, not just *how to build*. The blockchain/Dagster work seeded early interest in distributed coordination and reliability — concepts that resurface in Temporal.io and the three-layer session persistence of Decision Orchestrator.

---

### Phase 3: Language Theory / Compiler Work (2023)

**What happened:**
- `cs155-bf-to-mips`: Brainfuck-to-MIPS compiler in Rust (Yacc/Lex)
- Compiler coursework — language theory, parsing, code generation

**What this phase demonstrates:**
Understanding abstraction layers from first principles. A compiler is the quintessential "layer between" — it takes one representation and transforms it into another while preserving semantics. MCP is a protocol that transforms tool calls into executable actions. The conceptual pattern is the same.

**Narrative function:** This is the last piece of the foundation before the professional pivot. Compilers teach you that abstraction layers must have formal contracts — the same insight that drives building an MCP registry with scope-based credential gating rather than ad-hoc tool calls.

---

### Phase 4: Transition — First Private AI Work (2023–2024)

**What happened:**
- `qabot` (private, Python/AI): First AI-focused private work. Marks the beginning of the LLM engineering turn.
- University graduation (inferred ~2023 from repo timeline, based on 2019 start date of academic work)

**What this phase demonstrates:**
The pivot to LLM engineering. Not a hard left turn — a natural extension of the systems/research foundation applied to a new layer. This is the private work that connects Phase 3 to Phase 5.

**Narrative function:** This transition period is invisible on the public profile, which creates a apparent gap. The LinkedIn narrative should treat this as "the moment the foundation met the new stack" rather than acknowledging an obscure private repo. The academic arc flows directly into production AI work; qabot is the bridge.

---

### Phase 5: Production AI Infrastructure (2024–2026)

**What happened:**

**PyMC Labs — Decision Orchestrator:**
- Discord-based organizational OS. Discord message → intent classification → workflow selection → dynamic MCP tool assembly → Claude Agent SDK execution → thread-persistent response.
- Custom MCP tool registry at **protocol level** (not FastMCP, not a wrapper) — `@tool` decorator, runtime context injection, scope-based credential gating per server/channel.
- Dynamic tool assembly — each request gets a custom-assembled tool set based on workflow + context.
- Three-layer session persistence (Claude context + Langfuse traces + Supabase records) — agents survive crashes, full audit trails.
- FCIS (Functional Core, Imperative Shell) architecture applied deliberately to ~36,400 LOC Python codebase.
- 7 platform integrations: Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io.

**Nuts and Bolts AI — Cheerful:**
- Full-stack influencer marketing automation: 3 apps (FastAPI backend, Next.js/React 19 frontend, Slack AI context engine).
- Durable campaign execution with **Temporal.io** — pipelines survive crashes, retry intelligently. 5,570 commits.
- AI-personalized creator outreach: Claude generates unique emails per creator (not mail-merge).
- Multi-account Gmail orchestration: threading, tracking, sending across OAuth accounts simultaneously.
- Internal Slack AI assistant: Claude Agent SDK + custom MCP server + Onyx RAG.
- Frontend: Next.js 16+, React 19, TanStack Query, Zustand, Radix/shadcn.

**Phase 6: Meta-Systems (2026)**
- Ralph loop engine: iterative analysis pipeline with convergence detection, wave-based dependency frontier, CI integration, GitHub issue creation. Shows systems-level thinking extended beyond code into process itself.

---

## The Through-Line: One Layer Deeper

Every phase of this career shows the same orientation: **go one layer deeper than required**.

| Phase | What most people do | What derwells did |
|-------|--------------------|--------------------|
| Numerical computing | Import scipy solvers | Implemented Runge-Kutta from scratch |
| Graph algorithms | Use a library | Wrote blocked Floyd-Warshall in CUDA |
| C systems | Use POSIX abstractions | Built concurrent fileserver with linked lists |
| ML | Use pretrained models | Implemented from ArXiv papers, benchmarked against SOTA |
| Distributed systems | Use managed queues | Implemented Temporal.io durable workflows |
| AI tools | Use FastMCP wrapper | Built protocol-level MCP registry with credential gating |
| AI observability | Log to console | Langfuse traces + Supabase + Claude context (3-layer persistence) |
| AI architecture | Monolith | FCIS (Functional Core, Imperative Shell) discipline |

The through-line is not a coincidence. It's a way of thinking. It explains why someone who graduated with ML/CV research experience ends up building production AI infrastructure — and building it **seriously**, with durability, observability, and architectural discipline that most AI engineers skip.

---

## The PyMC Labs Connection Is Earned

The connection between a person with Runge-Kutta, Lotka-Volterra, and numerical dynamics work and PyMC Labs (the probabilistic programming organization) is not random. It's earned:

- Numerical methods → mathematical computing → probabilistic modeling: conceptually adjacent domains
- CUDA GPU work → scientific computing community: PyMC's world
- Research rigor (benchmark comparisons, paper implementations) → the standard PyMC Labs holds internally
- Statistical computing orientation (all that dynamical systems work) → natural fit for Bayesian inference ecosystem

This is not a lucky hire. The academic arc explains the fit. LinkedIn should surface this connection explicitly.

---

## Narrative Gap and How to Bridge It

**The gap**: No LinkedIn presence for 2024–2026. The profile shows nothing after university. Two full production systems, 50,000+ LOC, and a platform proven across two domains are completely invisible.

**How to bridge it**: The LinkedIn narrative doesn't need to explain qabot or the transition year. The story writes itself:
1. University: rigorous technical foundation (ML research, HPC, numerical methods, systems)
2. Professional: built production AI infrastructure at two companies using a deliberate platform (Claude Agent SDK + MCP + Temporal.io + Supabase + Langfuse)
3. The arc is coherent: the foundation explains why the production work looks the way it does

The narrative doesn't need to say "then I pivoted" — it can say "with that foundation, I built..." and the progression is obvious.

---

## Narrative Frame for LinkedIn

**The one-sentence version of the whole arc:**

> "Built the computational foundation in university (CUDA, numerical methods, ML research), then applied it to production AI infrastructure — the layer that makes LLM agents reliable, observable, and composable — proven at two companies with the same deliberate platform."

**The about section arc (structural):**

```
HOOK: The thing that makes me different from "AI developer" (first 2 lines)
ACT 1: Where this started — the foundation (2 sentences)
ACT 2: What I built — the two production systems (3-4 sentences, name specific things)
ACT 3: The pattern — same platform, two domains, what that means (2 sentences)
CLOSE: What I'm looking for or what comes next (optional 1-2 sentences)
```

**What each section must do:**
- Hook: Immediately separates from "I am an experienced AI developer"
- Act 1: The scientific computing arc earns the claim — not a bootcamp story, not a tutorial story
- Act 2: Specific systems with specific names (Temporal.io, MCP registry, Langfuse) — not generic "AI applications"
- Act 3: The platform thesis — this is the thing that no one else can say
- Close: Forward-looking or open-ended — invites conversation

---

## Chronological Order for LinkedIn Experience Section

LinkedIn shows most-recent-first. Recommended order:

1. **Nuts and Bolts AI** — AI Engineer (current, 2024/2025–present)
   - Cheerful: AI-personalized influencer marketing automation
   - Lead: Temporal.io durable workflows + Claude Agent SDK outreach

2. **PyMC Labs** — AI Infrastructure Engineer (current or prior, 2024/2025–present/past)
   - Decision Orchestrator: Discord organizational OS
   - Lead: Protocol-level MCP registry + three-layer session persistence

3. **University** — B.S. Computer Science (approximate 2019–2023)
   - Anchor for the ML research work (crowNNs, LPRNet)
   - Skills: Python, CUDA, C, numerical methods, computer vision

**Date note:** Exact start/end dates for both professional roles are unknown from available data. Derick must fill these in. The career-narrative-arc analysis treats them as approximately 2024–2026 based on when projects appear in the monorepo.

---

## What the Narrative Must NOT Do

1. **Lead with "AI Developer"** — too generic, fails the swap test
2. **List skills without naming specific systems** — "proficient in Python, ML, AI" is invisible
3. **Frame early work as irrelevant** — the foundation is the differentiator
4. **Hide the platform thesis** — it's the single most compelling fact in the entire story
5. **Present two roles as unrelated** — the shared architecture is the whole point
6. **Be chronological in the About section** — lead with the present, then earn the hook by explaining the arc

---

## Summary

The arc is: **rigorous scientific computing foundation → ML research discipline → production AI infrastructure engineering → platform thesis proven across two domains**.

This is a coherent story of deepening, not scattering. Every phase explains the next. The through-line — "goes one layer deeper than required" — makes sense of the CUDA kernels, the paper implementations, the Temporal.io choice, and the protocol-level MCP registry as expressions of the same underlying orientation.

**The LinkedIn narrative is already written by the data. The profile just has to say it.**
