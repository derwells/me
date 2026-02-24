# Identity Synthesis — derwells

**Analyzed**: 2026-02-24
**Sources**: All Wave 1 files + `analysis/reference-formula-extraction.md`, `analysis/career-narrative-arc.md`, `analysis/experience-entry-design.md`

---

## The Core Identity Frame

Before drafting anything, the anchor: **derwells is not an "AI developer." He is an AI infrastructure engineer who builds the layer that makes agents reliable.**

The three things that make this identity stick and fail the swap test:
1. Protocol-level MCP registry (not a user of MCP — builder of MCP infrastructure)
2. Platform thesis proven across two production orgs (same stack, different domains, deliberately)
3. Temporal.io for durable AI workflows (reliability-first instinct, not common in SaaS)

Every element below reinforces this frame. Nothing contradicts it.

---

## 1. Headline Drafts

**Constraint**: 220 chars (desktop), truncated on some mobile viewports. No truncation — every char shows.

**Formula used** (from reference-formula-extraction): Hybrid — Specific what + Stack keywords (SEO) + Named org anchors (social proof)

### Option A — Recommended

```
AI Infrastructure Engineer | Claude Agent SDK · Temporal.io · MCP | Nuts & Bolts AI · PyMC Labs
```

**Character count**: 97 chars ✓ (well under 220, room to expand if desired)
**Why this works**:
- "AI Infrastructure Engineer" is differentiated from "AI Developer" — signals a layer below
- Stack keywords (Claude Agent SDK, Temporal.io, MCP) are niche enough to stand out in search; low competition
- Named orgs (Nuts & Bolts AI, PyMC Labs) provide immediate credibility anchors
- Passes the swap test — no other developer on LinkedIn has this exact combination

### Option B — Concept-forward

```
Building the reliability layer for AI agents | Temporal.io · Claude Agent SDK · MCP · Langfuse | Nuts & Bolts AI · PyMC Labs
```

**Character count**: 125 chars ✓
**Why this works**: The phrase "reliability layer" owns a concept, not just a role category. Resonates with technical readers. SEO weaker (less exact keywords) but human impression stronger.

**Tradeoff**: Less SEO-optimized (verb phrase vs. noun title), but more memorable in person-to-person contexts (conference, DM, word-of-mouth).

### Option C — Mission-forward (most memorable, least SEO)

```
I build the layer that makes AI agents reliable. Temporal.io · MCP (protocol) · Claude SDK | Nuts & Bolts AI · PyMC Labs
```

**Character count**: 120 chars ✓
**Why this works**: The first clause is the hook from the About section, giving instant coherence between headline and profile. "MCP (protocol)" signals the depth immediately. Most human, least keyword-stuffed.

**Tradeoff**: First-person headlines are unconventional on LinkedIn; some recruiters may find it unusual.

### Option D — Role-stacked (most SEO)

```
AI Engineer | AI Agent Infrastructure · MCP · Temporal.io · Claude Agent SDK · Langfuse | Nuts & Bolts AI · PyMC Labs
```

**Character count**: 117 chars ✓
**Why this works**: Highest keyword density. "AI Agent Infrastructure" is a searchable phrase. Langfuse adds a distinctive long-tail keyword.

**Tradeoff**: Reads more like a keyword string than a headline. Better for recruiters searching than humans browsing.

### Recommendation

**Use Option A as the default**. It balances SEO keyword density with human readability and avoids the risks of Options B/C (non-standard structure) or D (pure keyword list).

If Derick ever writes a LinkedIn post that generates organic impressions, switch to Option B or C — the human-first framing becomes more valuable once people are clicking through from content rather than search.

---

## 2. About Section Draft

**Constraint**: 2,600 chars. First ~200 chars visible on mobile before "See More." Hook must work as a standalone.

**Structure applied** (from career-narrative-arc + reference-formula-extraction):
```
HOOK (line 1-2): Contrast that creates immediate distinction
PROOF (paragraph 2-3): The two systems — named, specific, scale signals
PATTERN (paragraph 4): Platform thesis — same stack, two domains
ORIGIN (paragraph 5): Arc — where this came from, what it explains
CLOSE (paragraph 6): Forward-looking, invites conversation
```

### About Section (copy-paste ready)

```
Most AI apps sit on top of LLMs. I build the layer that makes them reliable.

I've proven it twice: the same AI agent infrastructure stack, deployed at two production companies in completely different domains.

At Nuts & Bolts AI, I'm an AI engineer on Cheerful — an influencer marketing automation platform. I architected durable campaign workflows with Temporal.io (pipelines that survive crashes and retry intelligently), built a Claude Agent SDK outreach engine that generates unique emails per creator at scale, and shipped an internal Slack AI assistant backed by custom MCP tooling and Onyx RAG. ~5,570 commits across three production apps.

At PyMC Labs, I built Decision Orchestrator — a Discord-based organizational OS. A message arrives, an intent classifier routes it, the system dynamically assembles the right MCP tools for that request, Claude Agent SDK executes, and the response persists across sessions. The MCP tool registry is built at protocol level: not FastMCP, not a wrapper — the actual protocol, with scope-based credential gating, runtime context injection, and a @tool decorator. ~36,400 LOC, deployed on Fly.io.

Same stack across both: Claude Agent SDK · custom MCP · Supabase · Langfuse · Composio. That didn't happen by accident.

It happened because of a background in systems and scientific computing: CUDA GPU kernels, Runge-Kutta orbital simulations, ML/CV research benchmarked against state-of-the-art (tree crown detection, FCOS vs. RetinaNet), Brainfuck-to-MIPS compiler in Rust. That foundation is why my production AI systems have Temporal.io, three-layer session persistence, and deliberate architecture — not just "it works."

Based in the Philippines, working remotely. Open to conversations about AI infrastructure, agent reliability, and what it actually takes to run LLM agents in production.
```

**Character count**: ~1,520 chars ✓ (under 2,600 limit — room to expand)

### Mobile Truncation Check (~200 chars visible)

> "Most AI apps sit on top of LLMs. I build the layer that makes them reliable.\n\nI've proven it twice: the same AI agent infrastructure stack, deployed at two production companies in..."

After "in", the "See More" appears. The reader has seen:
1. The contrast claim ("reliability layer")
2. The "proven twice" social proof

Both are strong enough to earn the click. ✓

### What Each Paragraph Does

| Paragraph | Function | Key move |
|-----------|----------|----------|
| Hook | Distinction — "not just another AI developer" | Contrast between LLM apps and the layer beneath |
| "I've proven it twice" | Social proof structure | Two orgs = deliberate, not lucky |
| Nuts & Bolts AI | Proof 1 — specifics | Temporal.io, Claude SDK, commit count |
| PyMC Labs | Proof 2 — specifics | Protocol-level MCP, architecture, LOC |
| "Same stack" | Platform thesis | The deliberateness is the differentiator |
| Background | Arc — earns the claim | Explains why the infra has depth |
| Close | Forward-looking | Invites conversation without begging for a job |

### Alternative Hook Options (if A/B testing)

**Hook B — Platform thesis first**:
> "I've shipped the same AI agent infrastructure stack at two production companies. Different domains, same deliberate platform: Temporal.io, protocol-level MCP, Claude Agent SDK, Langfuse."
> (~185 chars — fits mobile)

**Hook C — Arc first**:
> "It started with CUDA kernels and Runge-Kutta solvers. Now I build the infrastructure that makes AI agents reliable — and I've proven it works at two production companies."
> (~170 chars — fits mobile; best for humans who read past the first line)

**Recommendation**: Use Hook A (contrast) for the live profile. It's the most immediate, creates the strongest cognitive distinction, and leads with the claim not the biography.

---

## 3. Featured Section Recommendations

**Constraint**: Not indexed by search — purely human engagement. Show proof of work. Keep to 3–5 items.

### Minimum Viable Featured (can do today)

| Order | Item | Type | URL/Description |
|-------|------|------|-----------------|
| 1 | GitHub profile | Link | github.com/derwells |
| 2 | crowNNs repo | Link | github.com/derwells/crowNNs |

**Why these**: GitHub profile is the primary portfolio surface. crowNNs is the strongest public technical signal — SOTA benchmark comparison, ML research framing, verifiable.

### Enhanced Featured (requires writing one LinkedIn post first)

| Order | Item | Type | Description |
|-------|------|------|-------------|
| 1 | LinkedIn post: "What it actually takes to run AI agents in production" | LinkedIn Post | Write once, then pin. 500–700 words about Temporal.io vs. naive async, crash recovery, audit trails. Demonstrates thinking, not just doing. |
| 2 | GitHub profile | Link | github.com/derwells |
| 3 | crowNNs repo | Link | github.com/derwells/crowNNs |

**Why the post first**: A pinned post is the highest-trust Featured item for a builder — it shows you can explain your work, not just do it. A post about "why I built an MCP registry from protocol level instead of using FastMCP" or "what Temporal.io gave me that async Python didn't" would resonate exactly with the audience Derick wants to reach.

### Optional Additions

- **Personal site** — if one exists or is built
- **Decision Orchestrator writeup** — if a public case study is ever written
- **A blog post or article** — any external link with substantive content

---

## 4. Skills List (Ordered by Strategic Priority)

**Constraint**: Up to 50 skills. First 3 pinned. Indexed for search — order affects discoverability.

**Ordering principle**: Most differentiated and currently strategic first. Generic/table-stakes skills last.

### Tier 1: High-differentiation, low search competition (pin these first)

| # | Skill | Why first |
|---|-------|-----------|
| 1 | Claude Agent SDK | Niche, growing demand, low supply — no bootcamp teaches this |
| 2 | Model Context Protocol (MCP) | Emerging protocol, protocol-level builder = rare signal |
| 3 | Temporal.io | Very low LinkedIn supply, high signal for reliability engineering |
| 4 | Langfuse | Niche observability tool — signals production discipline |
| 5 | AI Agent Architecture | Searchable phrase for the growing "agent engineer" hiring category |

### Tier 2: Core stack, medium differentiation

| # | Skill |
|---|-------|
| 6 | Python |
| 7 | FastAPI |
| 8 | Next.js |
| 9 | React |
| 10 | TypeScript |
| 11 | Supabase |
| 12 | PostgreSQL |
| 13 | SQLAlchemy |
| 14 | Composio |
| 15 | Large Language Models (LLMs) |

### Tier 3: Breadth signals (academic + systems depth)

| # | Skill |
|---|-------|
| 16 | CUDA |
| 17 | Computer Vision |
| 18 | Machine Learning |
| 19 | Distributed Systems |
| 20 | Discord.py |
| 21 | OpenCV |
| 22 | Keras |
| 23 | PyTorch |
| 24 | NumPy |
| 25 | Docker |
| 26 | Fly.io |
| 27 | Rust |
| 28 | C |
| 29 | JavaScript |
| 30 | Git |

**Total: 30 skills** — solid coverage, no padding. Add more only if Derick has real experience with additional tools.

**Pin choices**: Skills 1, 2, 3 (Claude Agent SDK, MCP, Temporal.io). These are the most differentiated and the top three are what most viewers will see.

---

## 5. Tone Calibration

### The Voice

**Confident and specific, not boastful.** The profile uses specifics to make its claims — numbers (5,570 commits, 36,400 LOC), named tools (Temporal.io, not "workflow orchestration"), named patterns (FCIS, not "clean architecture"), named contrasts ("not FastMCP, not a wrapper"). The claims are verifiable in principle; the confidence comes from the specificity.

**Technical but accessible.** When a technical concept appears (MCP, FCIS, session persistence), it's immediately followed by what it means: "scope-based credential gating, runtime context injection, @tool decorator." The reader doesn't need to know what MCP is — the explanation creates the impression of depth without requiring the reader to already have context.

**Builder-first, not resume-first.** The framing is always about what was built, not about what the person can do. "I build the layer that makes them reliable" vs. "experienced in AI infrastructure." "Built Decision Orchestrator" vs. "worked on AI orchestration systems." Named things with verifiable existence > category claims.

**Slightly opinionated.** The profile has convictions: "not FastMCP, not a wrapper." "That didn't happen by accident." "Not just 'it works.'" These are editorial choices that signal someone who thinks about their work, not just does it. This matches the career-narrative-arc finding that the through-line is "goes one layer deeper than required" — a person with that orientation has opinions about abstraction levels.

**Not hustle-porn.** The About section doesn't mention grind, late nights, passion, or love of code. It mentions what was built and why it's interesting. This is the tone of someone who does serious work, not someone who wants credit for effort.

### Anti-patterns to avoid

| ❌ Avoid | ✓ Use instead |
|---------|--------------|
| "Passionate AI developer" | "I build the layer that makes AI agents reliable" |
| "Proven track record" | "~5,570 commits across three production apps" |
| "Strong experience in Python and ML" | "CUDA GPU kernels, Runge-Kutta simulations, FCOS vs. RetinaNet benchmark" |
| "Team player with excellent communication" | (omit — says nothing) |
| "Experienced in AI/ML" | "Protocol-level MCP tool registry, not FastMCP" |
| "Results-driven" | "Pipelines that survive crashes and retry intelligently" |

### Reference Persona Anchors

The tone is closest to:
- **Simon Willison**: Named things, verifiable specifics, explains context for non-experts, confident without being grandiose
- **swyx**: Intellectual ownership language, concept-coining, willing to make claims about what's important

Not like:
- **Pieter Levels**: Hustle/revenue-obsessed, self-promotional
- **Generic developer LinkedIn profiles**: Adjective-heavy, experience-light, swap-test-passing

---

## Summary: What Wave 3 Needs

The Wave 3 `linkedin-profile-spec` can pull directly from:

| Spec section | Source |
|-------------|--------|
| Headline | Use Option A (`AI Infrastructure Engineer | Claude Agent SDK · Temporal.io · MCP | Nuts & Bolts AI · PyMC Labs`) |
| About section | Copy-paste the full About draft above |
| Experience entries | Pull directly from `analysis/experience-entry-design.md` (entries are already copy-paste ready) |
| Featured section | Minimum: GitHub + crowNNs repo. Enhanced: post first, then pin |
| Skills | Use the 30-skill ordered list above; pin Claude Agent SDK, MCP, Temporal.io |
| Tone guidance | Confident + specific + builder-first + slightly opinionated |
| URL recommendation | `derwells` (check availability) |
| Execution checklist | Wave 3 to compile |
