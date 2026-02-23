# GitHub Profile Cross-Reference — derwells

**Analyzed**: 2026-02-23
**Sources**: `../../loops/github-profile-reverse/analysis/` — all three analysis files (monorepo-deep-scan, profile-snapshot, repo-inventory)

---

## Status of GitHub Profile Loop

The github-profile-reverse loop has completed 3 of 12 aspects (25%):
- `repo-inventory` — catalogued all 11 public repos
- `profile-snapshot` — documented blank-slate profile state
- `monorepo-deep-scan` — surfaced all hidden private work

Wave 2 (clustering, identity synthesis, narrative gaps) has not run yet. This cross-ref extracts what's already been found and draws LinkedIn-specific conclusions.

---

## Core Finding: Enormous Public/Private Gap

The GitHub profile loop's central discovery is a gap so large it almost defines the narrative:

| Visible on public GitHub | Reality |
|--------------------------|---------|
| 11 repos, mostly old ML/CS projects | 2 production AI systems with 50,000+ total LOC |
| Last meaningful public commit: 2023 | Active production work in 2026 |
| No bio, no README, no pinned repos | Custom MCP registry, Temporal.io, 14-skill AI framework |
| Stranger reads: "inactive student" | Actually: AI infrastructure engineer at two companies |

**LinkedIn implication**: The story the public profile tells is completely wrong. LinkedIn is the primary place to tell the right story — GitHub can't, because the work is private. LinkedIn experience entries are the fix.

---

## Thematic Clusters (Inferred Before Formal Clustering)

The github-profile-reverse loop hasn't formally run `repo-clustering` yet, but from the repo inventory the themes are clear:

### Cluster 1: Computer Vision / ML Research (university era)
- `crowNNs` — Tree crown detection, benchmarked against SOTA (DeepForest), GPU on GCP T4
- `LPRNet` — License plate recognition, Keras implementation of ArXiv paper
- Assessment: Strongest public signal. Shows research ability, can implement from papers, benchmarks rigorously.

### Cluster 2: Numerical Computing / Scientific Simulation (university era)
- `halleys-comet` — 4th-order Runge-Kutta orbital simulation
- `lotka-volterra` — Predator-prey dynamics, Regula-Falsi root finding
- Assessment: Shows mathematical depth, physics thinking. Links to PyMC Labs work (probabilistic modeling org).

### Cluster 3: Systems / HPC Programming (university era)
- `multithreaded-fileserver` — Concurrent fileserver in C, linked list data structure
- `blocked-floyd-warshall-gpu` — GPU implementation of blocked Floyd-Warshall (CUDA), no description/README
- Assessment: Low-level, high-performance orientation. Predicts the reliability/infrastructure thinking in current production work.

### Cluster 4: Production AI Systems (current, private)
- `Cheerful` — Full-stack influencer marketing automation: Python/FastAPI, Temporal.io, Claude Agent SDK, MCP, Gmail API, Composio, Supabase, Langfuse, Next.js, React. 5,570 commits, 3 apps, team of 5.
- `Decision Orchestrator` — Discord-based organizational OS: discord.py, Claude Agent SDK, custom protocol-level MCP registry with scope-based credential gating, FCIS architecture, Supabase, Langfuse, Fly.io. 36,400 LOC.
- Assessment: The real work. None of this is public. LinkedIn is the only place to surface it.

### Cluster 5: Meta-Systems (current, private)
- Ralph loop engine — iterative analysis pattern, runs in CI every 30 minutes, convergence detection, GitHub issue creation
- Claude Code skills framework — 14 skills, ~2,975 lines, meta-level AI agent programming
- Assessment: Shows a builder who builds *for* builders. Framework-level thinking.

---

## Key Signals Extracted From GitHub Loop (LinkedIn-Relevant)

### 1. The Platform Thesis

**Finding from monorepo-deep-scan**: Both production systems share identical architectural DNA:

| Component | Choice |
|-----------|--------|
| AI orchestration | Claude Agent SDK |
| Tool protocol | Custom MCP servers (built, not consumed) |
| Database | Supabase (PostgreSQL) |
| Observability | Langfuse (LLM tracing) |
| Integrations | Composio |

Same stack deployed across two completely different domains (influencer marketing automation + organizational coordination OS). This is deliberate. It's a platform thesis, not opportunism.

**LinkedIn translation**: "Built the same AI agent infrastructure stack across two orgs in different industries" → shows intentionality, depth, transferable architecture knowledge.

### 2. The MCP Registry Differentiator

**Finding from monorepo-deep-scan**: The Decision Orchestrator uses a protocol-level custom MCP implementation — not FastMCP, not a wrapper. Hand-built with `@tool` decorator, context injection, and scope-based credential gating (each tool only accesses credentials scoped to its server/channel).

**LinkedIn translation**: "Built custom MCP tool registry from protocol level" distinguishes from "used MCP tools." Most people are consumers; this person built infrastructure. This belongs in the Decision Orchestrator experience entry as a specific callout.

### 3. Temporal.io for Production Reliability

**Finding from monorepo-deep-scan**: Cheerful uses Temporal.io durable workflows for campaign orchestration — pipelines that survive crashes, handle retries, maintain state across async operations.

**LinkedIn translation**: Using Temporal.io signals production reliability thinking that most SaaS builders skip. It's a mark of engineering seriousness. Should be in the Cheerful experience entry.

### 4. Scale Indicators

From the GitHub loop analysis, concrete numbers available for LinkedIn:
- Cheerful: ~5,570 commits, ~13,100 LOC, 3 apps (backend, webapp, context-engine), 5-person team
- Decision Orchestrator: ~36,400 LOC, ~285 Python files, 24 direct dependencies, 5+ database tables
- Ralph loops: running on 30-minute CI cron, 1800s timeout per iteration, convergence detection

These are LinkedIn bullet metrics. "Led development of AI platform with 5,570 commits across 3 production apps" is more compelling than "built an AI platform."

### 5. Academic-to-Production Arc

The chronological trajectory is clear from GitHub:
1. **University phase**: ML research (crowNNs, LPRNet), numerical methods (Runge-Kutta, Lotka-Volterra), systems (C fileserver, CUDA)
2. **Transition**: PyMC Labs connection (pymc-examples fork, Feb 2026), statistical modeling domain
3. **Current phase**: Production AI systems with Claude Agent SDK, MCP, Temporal.io, across two companies

The arc is "rigorous academic/scientific computing → production AI agent infrastructure." This is a coherent story — it's not random. The scientific computing background explains *why* someone ends up at PyMC Labs and *why* they think in terms of durable workflows and formal architecture (FCIS).

---

## Narrative Gaps (LinkedIn-Specific)

Things the GitHub loop identified that need to appear on LinkedIn because they can't appear on GitHub:

| Invisible asset | LinkedIn home |
|-----------------|---------------|
| Cheerful — 3-app AI automation platform | Experience entry: Nuts and Bolts AI |
| Decision Orchestrator — custom MCP registry | Experience entry: PyMC Labs |
| Ralph loop engine — autonomous CI analysis | About section or featured |
| 14-skill Claude Code framework | Skills / about |
| FCIS architecture discipline | Bullet in Decision Orchestrator entry |
| Temporal.io durable workflows | Bullet in Cheerful entry |
| Platform thesis (same stack, two domains) | About section hook |
| Scientific computing foundation (Runge-Kutta, CUDA, C) | Skills, possibly about |

---

## Identity Signals (Pre-Synthesis)

The GitHub loop's monorepo-deep-scan surfaced an identity that the profile loop will later formalize. From the raw data, the identity is:

**What this person does**: Builds AI agent infrastructure — the layer between LLM APIs and real-world systems. Not AI chatbots. Not prompt wrappers. The orchestration engine, the tool registry, the durable workflow layer.

**Who trusts them**: PyMC Labs (probabilistic programming organization) + Nuts and Bolts AI (influencer marketing automation startup). Different domains = trust is transferable.

**How they think**: Platform-first. Same architecture applied deliberately across domains. FCIS discipline. Convergence mechanics in analysis tooling. This is a systems thinker.

**What differentiates them**: Most AI engineers use MCP tools. This person built a protocol-level MCP registry with scope-based credential gating. Most AI engineers reach for ad-hoc solutions. This person chose Temporal.io for durable workflows. Most AI engineers build one thing. This person built the *same thing* twice in different domains, confirming it wasn't accidental.

---

## Recommendations for LinkedIn (Carried Forward to Wave 2)

1. **LinkedIn must tell the story GitHub cannot** — The public GitHub reads "inactive student." LinkedIn experience entries are the correction. This is highest priority.

2. **Lead with the platform thesis** — "Built the same AI agent infrastructure stack across two orgs" is the hook. It's rare. It's verifiable (two employers). It shows intentionality.

3. **Name specific technologies in bullets** — Temporal.io, Claude Agent SDK, custom MCP registry, Langfuse, Supabase, FCIS — these are searchable, differentiated, and signal that this isn't generic "AI development."

4. **Use the academic arc as context** — Scientific computing background (CUDA, Runge-Kutta, PyMC) explains the PyMC Labs connection and the infrastructure thinking. Don't hide it — it's the origin story.

5. **crowNNs is the best public proxy** — Benchmarked against SOTA, CV research, GPU. If LinkedIn features section can link GitHub repos, this is the one to feature. It's the strongest public signal of technical depth.

6. **The ralph loop engine is a story asset** — Even without a public repo, describing "autonomous AI analysis pipelines running in CI with convergence detection" signals a particular kind of builder. Use it in the About section.
