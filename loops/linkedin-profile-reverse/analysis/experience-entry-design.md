# Experience Entry Design — derwells

**Analyzed**: 2026-02-24
**Sources**: `analysis/monorepo-project-inventory.md`, `analysis/org-work-analysis.md`, `analysis/career-narrative-arc.md`, `analysis/reference-formula-extraction.md`, `analysis/linkedin-format-research.md`, `analysis/github-profile-cross-ref.md`

---

## Design Principles Applied

**From the formula extraction**:
- First 3-4 lines visible before "See More" on mobile — these are the hook, not setup
- Action verb + specific what + result/scale (STAR bullets)
- Lead with the most differentiating claim per entry, not chronologically
- Unicode bullets (•) — LinkedIn renders no markdown
- Swap test: every bullet must be specific enough to be false about any other developer

**Entry priority order** (most recent first, as LinkedIn requires):
1. Nuts and Bolts AI (Cheerful) — current, most recent
2. PyMC Labs (Decision Orchestrator) — concurrent or prior
3. University education — foundation entry
4. Optional: stand-alone research entry (see note below)

---

## Entry 1: Nuts and Bolts AI

### Header Fields

| Field | Value | Notes |
|-------|-------|-------|
| **Title** | AI Engineer | Clean, 11 chars. Alt: "Software Engineer — AI Systems" (30 chars) |
| **Company** | Nuts and Bolts AI | Must match LinkedIn company page (or free-text) |
| **Employment type** | [Full-time or Contract] | Derick to confirm |
| **Start date** | [Month, Year] | Derick to fill |
| **End date** | Present | Ongoing |
| **Location** | Remote | Or "Philippines (Remote)" |

### Description (copy-paste ready)

```
AI engineer on Cheerful — influencer marketing automation platform built for creator outreach at scale. One of five engineers across three production apps: Python/FastAPI campaign backend, Next.js/React 19 web app, and an internal Slack AI assistant.

• Architected durable campaign execution workflows with Temporal.io — pipelines that survive crashes and retry intelligently. ~5,570 commits shipped across three production apps.
• Built AI-personalized creator outreach engine using Claude Agent SDK — unique email generated per creator based on multi-source profile enrichment, not mail-merge templates.
• Implemented waterfall creator enrichment pipeline: bio crawling, social profile aggregation, and structured creator profile assembly from multiple sources.
• Engineered multi-account Gmail orchestration: OAuth thread management, delivery tracking, and coordinated sending across multiple accounts simultaneously.
• Built the team's internal Slack AI assistant using Claude Agent SDK + custom MCP server + Onyx RAG — operational AI infrastructure for internal team coordination.
• Delivered full-stack web frontend: Next.js 16+, React 19, TanStack Query, Zustand, Radix/shadcn — multi-step campaign wizard with real-time state management.

Stack: Python · FastAPI · Temporal.io · Claude Agent SDK · MCP · Next.js · React 19 · Supabase · Langfuse · Composio · Gmail API · TypeScript
```

**Estimated character count**: ~1,350 (well under 2,000 limit) ✓

### What Shows Before "See More" (~200–300 chars visible on mobile)

Mobile users see:
> "AI engineer on Cheerful — influencer marketing automation platform built for creator outreach at scale. One of five engineers across three production apps: Python/FastAPI campaign backend..."

Desktop users see approximately:
> "AI engineer on Cheerful — influencer marketing automation platform built for creator outreach at scale. One of five engineers across three production apps: Python/FastAPI campaign backend, Next.js/React 19 web app, and an internal Slack AI assistant.
>
> • Architected durable campaign execution..."

**Assessment**: The opening establishes scale (5 engineers, 3 apps, production) and the first bullet (Temporal.io durable workflows) kicks in just as the "See More" would hit. Strong hook. ✓

### Design Decisions

- **Bullet order (most → least differentiating)**:
  1. Temporal.io (reliability engineering that most SaaS apps skip — the differentiator)
  2. Claude Agent SDK + personalized outreach (the AI story)
  3. Creator enrichment pipeline (unique domain problem)
  4. Multi-account Gmail orchestration (integration complexity)
  5. Internal Slack AI assistant (platform/MCP story)
  6. Full-stack frontend (breadth signal — goes last because it's table stakes)

- **"not mail-merge templates"** in bullet 2 is intentional — the contrast is what makes it memorable. The swap test: this is specific enough to be false about other AI developers who do use mail-merge.

- **"~5,570 commits"** in bullet 1 is included because it's a concrete scale signal available from the repo data. It implies sustained production velocity, not a weekend project.

- **Stack line at the bottom** serves LinkedIn SEO — the keywords get indexed even if a reader doesn't read down. Temporal.io and Claude Agent SDK are differentiated enough to stand out in search.

---

## Entry 2: PyMC Labs

### Header Fields

| Field | Value | Notes |
|-------|-------|-------|
| **Title** | AI Infrastructure Engineer | 26 chars. Alt: "Software Engineer — Agent Systems" (32 chars) |
| **Company** | PyMC Labs | Must match LinkedIn company page |
| **Employment type** | [Full-time or Contract] | Derick to confirm |
| **Start date** | [Month, Year] | Derick to fill |
| **End date** | [Month, Year or Present] | Derick to fill |
| **Location** | Remote | Or "Philippines (Remote)" |

### Description (copy-paste ready)

```
Built Decision Orchestrator — Discord-based organizational OS for PyMC Labs. Intent classification → dynamic tool assembly → Claude Agent SDK execution → thread-persistent response. ~36,400 LOC, deployed on Fly.io.

PyMC Labs is the professional services org behind PyMC, a widely used probabilistic programming library for Bayesian modeling — a high trust bar.

• Built custom MCP tool registry at protocol level — not FastMCP, not a wrapper. Includes @tool decorator, runtime context injection, and scope-based credential gating (each tool accesses only credentials authorized for its server/channel).
• Designed dynamic tool assembly: each incoming request receives a custom-assembled tool set based on workflow context and intent classification — not static configuration.
• Implemented three-layer session persistence (Claude context windows + Langfuse traces + Supabase records) — agents survive crashes with full audit trails across every session.
• Applied FCIS (Functional Core, Imperative Shell) architecture to a 36,400 LOC Python codebase — deliberate design discipline in a domain that rarely uses any.
• Integrated 7 external platforms: Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io.

Stack: Python 3.12+ · discord.py · Claude Agent SDK · SQLAlchemy 2.0 · FastAPI · Supabase · Langfuse · Fly.io · Composio
```

**Estimated character count**: ~1,270 (well under 2,000 limit) ✓

### What Shows Before "See More" (~200 chars visible on mobile)

Mobile users see:
> "Built Decision Orchestrator — Discord-based organizational OS for PyMC Labs. Intent classification → dynamic tool assembly → Claude Agent SDK execution → thread-persistent response. ~36..."

**Assessment**: Within 200 chars, the reader has: the product name, what it does (organizational OS), the client (PyMC Labs), the pipeline summary (intent → tools → execute), and a LOC scale signal is starting. Dense and specific — fails the swap test immediately. ✓

### Design Decisions

- **Pipeline notation in opening** (`intent classification → dynamic tool assembly → Claude Agent SDK execution → thread-persistent response`) gives a stranger the architecture at a glance without requiring technical background. It reads as precise and intentional.

- **"not FastMCP, not a wrapper"** in bullet 1 is deliberate. Without this contrast, a reader might assume "custom MCP" means "used the SDK." This makes explicit that protocol-level is different from wrapper-level. Critical for technical readers.

- **Scope-based credential gating** is a security/architecture detail that signals this was built with production concerns in mind — not just "it works."

- **"deliberate design discipline in a domain that rarely uses any"** in the FCIS bullet provides the contrast that makes it impressive. FCIS on a Discord bot is unusual — the contrast earns the claim.

- **PyMC Labs context paragraph** is important: a stranger reading "PyMC Labs" might not know what it is. The one-sentence gloss (probabilistic programming library, Bayesian modeling, high trust bar) earns the credibility claim without requiring prior knowledge.

- **Bullet order (most → least differentiating)**:
  1. Protocol-level MCP registry (the single most technically differentiated claim in the entire profile)
  2. Dynamic tool assembly (the architectural story)
  3. Three-layer session persistence (the reliability story)
  4. FCIS architecture (the discipline signal)
  5. 7 platform integrations (breadth/surface area)

---

## Entry 3: Education

### Header Fields

| Field | Value | Notes |
|-------|-------|-------|
| **School** | [University name — Derick to fill] | Must match LinkedIn school page |
| **Degree** | Bachelor of Science | |
| **Field of Study** | Computer Science | Or Computer Engineering — Derick to confirm |
| **Start date** | [2019 or 2020] | Approximate — Derick to confirm |
| **End date** | [2023 or 2024] | Approximate — Derick to confirm |

### Description (copy-paste ready)

```
Studied computer science with emphasis on numerical computing, high-performance computing, machine learning, and systems programming.

• ML Research — Replaced SOTA object detection backbone (RetinaNet → FCOS) for tree crown detection in airborne imagery; benchmarked against DeepForest and lidR on GCP T4 GPUs (crowNNs).
• Implemented LPRNet license plate recognition architecture from ArXiv paper in Keras — paper reproduction and disciplined evaluation.
• HPC — Blocked Floyd-Warshall all-pairs shortest path implemented in CUDA; GPU-parallel algorithm on custom kernel.
• Numerical methods — 4th-order Runge-Kutta orbital simulation (Halley's comet); Regula-Falsi predator-prey dynamics (Lotka-Volterra).
• Systems — Concurrent fileserver in C with linked list data structure and thread synchronization.
• Compiler theory — Brainfuck-to-MIPS compiler in Rust using Yacc/Lex.
```

**Estimated character count**: ~870 (well under 2,000 limit) ✓

### Design Decisions

- The opening sentence front-loads the themes that will resonate: numerical computing, HPC, ML, systems. These connect the academic foundation to the production work narrative.

- **crowNNs is named** and identified as SOTA comparison work — this is the highest-signal public repo. Anyone who looks at the GitHub profile will find this; the LinkedIn education entry should reference it.

- **"paper reproduction and disciplined evaluation"** in the LPRNet bullet signals research literacy (reads papers, implements from scratch, knows how to evaluate). This is different from "trained a model."

- **FCIS in production + CUDA in university** — the educational background explains why the production work has architectural discipline. This is the coherence that makes the arc make sense.

- No need to mention PHP web apps, MIPS simulator, or Discord bot `shalltear` — these are table stakes and add noise without signal.

---

## Entry 4: Optional — Research / Independent Projects

**Should this be a separate entry?** Possibly yes, if Derick wants to elevate the crowNNs work beyond an education bullet. A stand-alone entry for "Independent Research" or "Academic Research" signals that the ML work was intentional, not just coursework.

### If included:

| Field | Value |
|-------|-------|
| **Title** | Research Engineer (ML/CV) |
| **Company** | Independent / Self-directed |
| **Employment type** | Self-employed |
| **Dates** | [2022] — [2022] or similar |

### Description:

```
ML/CV research projects during university. Emphasis on implementing from papers, benchmarking against state-of-the-art, and rigorous evaluation.

• crowNNs — Replaced DeepForest's RetinaNet backbone with FCOS for tree crown detection in airborne RGB imagery; benchmarked against SOTA (DeepForest) and lidR on GCP T4 GPUs. Presented results table comparing methods.
• LPRNet — Keras implementation of license plate recognition architecture from ArXiv. Self-directed paper reproduction; trained on CCPD-Base dataset.

Tools: Python · Keras · PyTorch · GCP (T4 GPU) · OpenCV · NumPy
```

**Recommendation**: Include only if the experience section feels thin without it, or if Derick specifically wants to highlight the research arc. The education description already covers this work; a separate entry is optional.

---

## What Derick Must Fill In

The following fields require information not available in the monorepo or public data:

| Field | Status | Action required |
|-------|--------|----------------|
| Nuts and Bolts AI: start date | Unknown | Fill in exact month/year |
| Nuts and Bolts AI: employment type | Unknown | Full-time or Contract? |
| PyMC Labs: start date | Unknown | Fill in exact month/year |
| PyMC Labs: end date | Unknown | Still active? If so, "Present" |
| PyMC Labs: employment type | Unknown | Full-time or Contract? |
| University: school name | Unknown | Must match LinkedIn school page |
| University: degree field | Inferred as CS | Confirm "Computer Science" is correct |
| University: start/end dates | ~2019–2023 | Confirm exact years |

---

## Entry Ordering and Overlap Handling

**If both roles are concurrent**: LinkedIn allows overlapping date ranges. List both with "Present" end date. Readers understand simultaneous roles. No need to choose one as "primary" — the overlap tells the platform thesis story structurally (two jobs, same stack).

**If PyMC Labs ended before Nuts and Bolts AI started**: List Nuts and Bolts AI first (most recent), PyMC Labs second with an end date.

**Either way**: Both entries should appear. The two-entry combination is the platform thesis made visible.

---

## Cross-Entry Platform Thesis Connection

The two entries should feel like the same person building the same thing in two different contexts. The shared signal:
- Both mention Claude Agent SDK
- Both mention MCP (in different ways — custom registry vs. custom server)
- Both mention Supabase and Langfuse
- Both use "custom" — not wrapping, building

A reader who scans both entries and notices the overlap will correctly conclude: "this person has a deliberate platform approach." That's the impression to create. The Stack lines at the bottom of each entry reinforce this structurally.

---

## Character Count Summary

| Entry | Description chars | Limit | Status |
|-------|------------------|-------|--------|
| Nuts and Bolts AI | ~1,350 | 2,000 | ✓ Under limit |
| PyMC Labs | ~1,270 | 2,000 | ✓ Under limit |
| Education | ~870 | 2,000 | ✓ Under limit |
| Optional research | ~400 | 2,000 | ✓ Under limit |

All entries have room to expand if Derick has additional context or metrics to add.
