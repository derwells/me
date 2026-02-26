# LinkedIn Profile Spec — derwells (Derick Wells)

**Generated**: 2026-02-24
**Sources**: All Wave 1 + Wave 2 analysis files
**Status**: Ready to paste — all fields copy-paste ready except where marked [FILL IN]

---

## How to Use This Spec

Work through the execution checklist at the bottom. Every section is ready to paste. Fields marked `[FILL IN]` require information only Derick has (exact dates, employment type, university name). Everything else is final.

---

## 1. Headline

**Copy this exactly:**

```
AI Infrastructure Engineer | Claude Agent SDK · Temporal.io · MCP | Nuts & Bolts AI · PyMC Labs
```

**Character count**: 97 / 220 ✓

**Why**: "AI Infrastructure Engineer" signals a layer below "AI Developer." The stack keywords (Claude Agent SDK, Temporal.io, MCP) are niche enough to stand out in search with low competition — no bootcamp teaches this stack. Named orgs provide instant credibility anchors. Passes the swap test: no other developer on LinkedIn has this combination.

**Alternate headline** (if you want to lead with concept over title):
```
Building the reliability layer for AI agents | Temporal.io · Claude Agent SDK · MCP · Langfuse | Nuts & Bolts AI · PyMC Labs
```
(125 chars — use this once you're publishing content and people click through from posts rather than search)

---

## 2. About / Summary Section

**Copy this exactly (1,520 chars / 2,600 limit ✓):**

```
Most AI apps sit on top of LLMs. I build the layer that makes them reliable.

I've proven it twice: the same AI agent infrastructure stack, deployed at two production companies in completely different domains.

At Nuts & Bolts AI, I'm an AI engineer on Cheerful — an influencer marketing automation platform. I architected durable campaign workflows with Temporal.io (pipelines that survive crashes and retry intelligently), built a Claude Agent SDK outreach engine that generates unique emails per creator at scale, and shipped an internal Slack AI assistant backed by custom MCP tooling and Onyx RAG. ~5,570 commits across three production apps.

At PyMC Labs, I built Decision Orchestrator — a Discord-based organizational OS. A message arrives, an intent classifier routes it, the system dynamically assembles the right MCP tools for that request, Claude Agent SDK executes, and the response persists across sessions. The MCP tool registry is built at protocol level: not FastMCP, not a wrapper — the actual protocol, with scope-based credential gating, runtime context injection, and a @tool decorator. ~36,400 LOC, deployed on Fly.io.

Same stack across both: Claude Agent SDK · custom MCP · Supabase · Langfuse · Composio. That didn't happen by accident.

It happened because of a background in systems and scientific computing: CUDA GPU kernels, Runge-Kutta orbital simulations, ML/CV research benchmarked against state-of-the-art (tree crown detection, FCOS vs. RetinaNet), Brainfuck-to-MIPS compiler in Rust. That foundation is why my production AI systems have Temporal.io, three-layer session persistence, and deliberate architecture — not just "it works."

Based in the Philippines, working remotely. Open to conversations about AI infrastructure, agent reliability, and what it actually takes to run LLM agents in production.
```

**Mobile check (first ~200 chars visible before "See More"):**
> "Most AI apps sit on top of LLMs. I build the layer that makes them reliable.\n\nI've proven it twice: the same AI agent infrastructure stack, deployed at two production companies in..."

The hook and social proof both land before the fold. ✓

---

## 3. Experience Entries

List most-recent-first. Both current roles should appear. If they overlap in time, LinkedIn supports concurrent date ranges — list both with "Present."

---

### Entry 1: Nuts and Bolts AI

**Title**: `AI Engineer`
**Company**: `Nuts and Bolts AI` *(search for the exact LinkedIn company page)*
**Employment type**: `[FILL IN — Full-time or Contract?]`
**Start date**: `[FILL IN — Month, Year]`
**End date**: `Present`
**Location**: `Philippines (Remote)` or `Remote`

**Description (copy-paste ready, ~1,350 chars / 2,000 limit ✓):**

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

---

### Entry 2: PyMC Labs

**Title**: `AI Infrastructure Engineer`
**Company**: `PyMC Labs` *(search for exact LinkedIn company page)*
**Employment type**: `[FILL IN — Full-time or Contract?]`
**Start date**: `[FILL IN — Month, Year]`
**End date**: `[FILL IN — Present, or Month + Year if ended]`
**Location**: `Philippines (Remote)` or `Remote`

**Description (copy-paste ready, ~1,270 chars / 2,000 limit ✓):**

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

---

### Entry 3: Education

**School**: `[FILL IN — your university name, search for the LinkedIn school page]`
**Degree**: `Bachelor of Science`
**Field of study**: `Computer Science` *(or confirm exact field)*
**Start date**: `[FILL IN — e.g., 2019]`
**End date**: `[FILL IN — e.g., 2023]`
**Grade / GPA**: *(optional — include only if strong)*
**Activities and societies**: *(optional)*

**Description (copy-paste ready, ~870 chars / 2,000 limit ✓):**

```
Studied computer science with emphasis on numerical computing, high-performance computing, machine learning, and systems programming.

• ML Research — Replaced SOTA object detection backbone (RetinaNet → FCOS) for tree crown detection in airborne imagery; benchmarked against DeepForest and lidR on GCP T4 GPUs (crowNNs).
• Implemented LPRNet license plate recognition architecture from ArXiv paper in Keras — paper reproduction and disciplined evaluation.
• HPC — Blocked Floyd-Warshall all-pairs shortest path implemented in CUDA; GPU-parallel algorithm on custom kernel.
• Numerical methods — 4th-order Runge-Kutta orbital simulation (Halley's comet); Regula-Falsi predator-prey dynamics (Lotka-Volterra).
• Systems — Concurrent fileserver in C with linked list data structure and thread synchronization.
• Compiler theory — Brainfuck-to-MIPS compiler in Rust using Yacc/Lex.
```

---

### Entry 4: Optional — Independent ML Research

**Include if**: You want to surface the ML research work more prominently, separate from coursework. Skip if three entries feels sufficient.

**Title**: `Research Engineer (ML/CV)`
**Company**: `Independent`
**Employment type**: `Self-employed`
**Start date**: `[2022]`
**End date**: `[2022]`

**Description:**

```
ML/CV research projects. Emphasis on implementing from papers, benchmarking against state-of-the-art, and rigorous evaluation.

• crowNNs — Replaced DeepForest's RetinaNet backbone with FCOS for tree crown detection in airborne RGB imagery; benchmarked against SOTA (DeepForest) and lidR on GCP T4 GPUs. Presented results table comparing methods.
• LPRNet — Keras implementation of license plate recognition architecture from ArXiv. Self-directed paper reproduction; trained on CCPD-Base dataset.

Tools: Python · Keras · PyTorch · GCP (T4 GPU) · OpenCV · NumPy
```

---

## 4. Featured Section

**Purpose**: Proof-of-work. Not indexed by search — purely for human engagement. Show 3–5 items.

### Minimum Viable (can do today)

| Order | Type | Item | Action |
|-------|------|------|--------|
| 1 | Link | GitHub profile | Add link: `https://github.com/derwells` — title: "GitHub — derwells", description: "Public repos, ML research (crowNNs), and open source work." |
| 2 | Link | crowNNs repo | Add link: `https://github.com/derwells/crowNNs` — title: "crowNNs — Tree Crown Detection Research", description: "ML/CV research: replaced SOTA (RetinaNet) backbone with FCOS for tree crown detection in airborne imagery. Benchmarked against DeepForest and lidR." |

### Enhanced (if you write one LinkedIn post first)

Write a post — recommended topic: *"What Temporal.io gave me that async Python couldn't"* or *"Why I built an MCP tool registry from protocol level instead of using FastMCP."* 500–700 words. Then:

| Order | Type | Item | Action |
|-------|------|------|--------|
| 1 | LinkedIn Post | "What it actually takes to run AI agents in production" | Write + publish, then pin to Featured |
| 2 | Link | GitHub profile | `https://github.com/derwells` |
| 3 | Link | crowNNs repo | `https://github.com/derwells/crowNNs` |

**Why post first**: A pinned LinkedIn post demonstrates you can explain your work, not just do it. Technical builders who can write are rare. A single good post outperforms any link in Featured.

---

## 5. Skills

**Pin first 3.** All 30 skills below are ready to add.

### Tier 1 — Pin these (most differentiated, lowest search competition)

1. **Claude Agent SDK** — pin
2. **Model Context Protocol (MCP)** — pin
3. **Temporal.io** — pin
4. Langfuse
5. AI Agent Architecture

### Tier 2 — Core stack

6. Python
7. FastAPI
8. Next.js
9. React
10. TypeScript
11. Supabase
12. PostgreSQL
13. SQLAlchemy
14. Composio
15. Large Language Models (LLMs)

### Tier 3 — Breadth / depth signals

16. CUDA
17. Computer Vision
18. Machine Learning
19. Distributed Systems
20. discord.py
21. OpenCV
22. Keras
23. PyTorch
24. NumPy
25. Docker
26. Fly.io
27. Rust
28. C
29. JavaScript
30. Git

---

## 6. Custom URL

**Recommended**: `linkedin.com/in/derwells`

**How to set**: Profile → Edit public profile & URL (top right) → Edit custom URL → type `derwells`

**Check first**: If `derwells` is taken, try `derick-wells` or `derick-wells-ph`. The current URL (`wfo-wells`) is opaque and untypeable from memory — change it regardless.

---

## 7. Profile Photo and Banner

**Profile photo**:
- Use a clear, high-contrast headshot. Face visible and centered. Professional but not stiff — a candid photo that looks like you is better than a posed corporate shot.
- If you don't have one: take one with your phone, good natural light, clean background. No avatar, no illustration.

**Banner**:
- Optional, but a banner communicates intentionality.
- Recommended: solid dark background with your headline or a short phrase in white text. "AI Infrastructure Engineer" or "Building the reliability layer for AI agents." Can be made in Figma or Canva in 20 minutes.
- Dimensions: 1584 × 396 pixels.
- Alternatively: leave blank — a blank banner is invisible; a bad banner is distracting. Only add one if it's clean.

---

## 8. Contact / Location

- **Location**: Set to Philippines (or your specific city/region)
- **Open to work**: If actively looking — turn on. If not — leave off. "Open to work" changes the audience finding you.
- **Contact info**: Add your email if you want inbound. Add GitHub URL under "websites."

---

## 9. Execution Checklist

Work top to bottom. Each item is independent — you can stop and resume without losing progress.

- [ ] **Custom URL** — Change from `wfo-wells` to `derwells` (or best available alternative). Do this first — it takes effect immediately and changes your shareable profile link.

- [ ] **Headline** — Paste: `AI Infrastructure Engineer | Claude Agent SDK · Temporal.io · MCP | Nuts & Bolts AI · PyMC Labs`

- [ ] **About / Summary** — Paste the full About section text from Section 2. Click the pencil icon on your profile → scroll to "About" → replace or add text.

- [ ] **Experience: Nuts and Bolts AI** — Add new experience entry. Fill in all header fields (title, company, dates, employment type, location). Paste description from Entry 1 above.

- [ ] **Experience: PyMC Labs** — Add new experience entry. Fill in all header fields. Paste description from Entry 2 above.

- [ ] **Education** — Edit or add your university entry. Fill in school name, degree, dates. Paste education description from Entry 3 above.

- [ ] **Skills** — Add all 30 skills from Section 5. Pin: Claude Agent SDK, Model Context Protocol (MCP), Temporal.io.

- [ ] **Featured: GitHub** — Click "Add profile section" → Featured → Add a link → paste `https://github.com/derwells`. Add title and description.

- [ ] **Featured: crowNNs** — Add second featured link → `https://github.com/derwells/crowNNs`. Add title and description.

- [ ] **Profile photo** — Upload headshot if not current.

- [ ] **Banner** — Add banner (optional — see Section 7).

- [ ] **Location** — Confirm Philippines is set correctly.

- [ ] **Contact info** — Add email and GitHub URL under "websites."

- [ ] **Review on mobile** — After updating, view your profile on mobile. Confirm the About section hook and experience entry openings all look good before "See More."

- [ ] **(Optional) Write + pin LinkedIn post** — Write "What Temporal.io gave me that async Python couldn't" or "Why I built protocol-level MCP instead of using FastMCP." Publish, then pin to Featured at position 1.

---

## What Derick Must Fill In

| Field | Notes |
|-------|-------|
| Nuts and Bolts AI: start date | Exact month + year of joining |
| Nuts and Bolts AI: employment type | Full-time or Contract |
| PyMC Labs: start date | Exact month + year |
| PyMC Labs: end date | "Present" if ongoing; or month + year if ended |
| PyMC Labs: employment type | Full-time or Contract |
| University: school name | Must match LinkedIn school page for the degree association to work |
| University: degree field | Confirm "Computer Science" is correct |
| University: start/end years | Confirm exact years |
| Profile photo | Any clear headshot |

Everything else in this spec is final and ready to paste.

---

## Signal Summary (What This Profile Communicates)

A stranger reading this profile for 30 seconds will understand:

1. **The claim**: Builds the infrastructure layer that makes AI agents reliable — not just "builds AI apps"
2. **The proof**: Two production systems at two named companies; 50,000+ LOC; protocol-level MCP registry; Temporal.io durable workflows
3. **The differentiator**: Same deliberate platform (Claude Agent SDK + custom MCP + Supabase + Langfuse) proven across completely different domains — this didn't happen by accident
4. **The depth**: The foundation (CUDA, numerical methods, ML research, compiler theory) explains why the production work looks the way it does
5. **The person**: Based in Philippines; works remotely; has opinions about abstraction levels; explains their work without hustle-porn

This is not a generic "AI developer" profile. It is the profile of someone who builds the layer below, has done it twice, and has the foundation to explain why.
