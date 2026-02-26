# Identity Synthesis — derwells

**Analyzed**: 2026-02-26
**Sources**: All Wave 2 analysis files (`repo-clustering.md`, `signal-vs-noise.md`, `fork-audit.md`, `narrative-gaps.md`), all Wave 1 files (`repo-inventory.md`, `profile-snapshot.md`, `monorepo-deep-scan.md`, `repo-readme-scan.md`, `org-contributions.md`)

---

## Summary

Derick Wells is an AI infrastructure engineer who builds the reliability layer for AI agents — production MCP servers, durable AI workflows, autonomous analysis systems. The public GitHub profile says none of this. The identity synthesis below is derived entirely from what was actually built (49,500+ LOC across two production systems, a self-authored analysis engine, BFT consensus research, GPU/HPC work, ML/CV projects), not from aspirational framing. The profile must be rebuilt around this identity.

---

## Primary Archetype

**"AI infrastructure engineer who builds the reliability layer for AI agents"**

This is not a marketing tagline — it's the literal description of the work:
- **Reliability layer**: Temporal.io durable execution for AI pipelines (Cheerful), crash-resilient session persistence spanning three systems (Decision Orchestrator), OOM postmortems and failure mode analysis
- **AI agents**: Claude Agent SDK orchestration in both production systems, custom MCP tool registry at protocol level
- **Infrastructure**: Not building chatbots or demos — building the plumbing that makes AI agents work in production (MCP servers, tool registries, credential gating, observability via Langfuse)

### Why this archetype works

1. **It's specific** — "AI infrastructure" is narrower than "AI engineer" and more accurate than "full-stack engineer"
2. **It differentiates** — most people building with LLMs in 2026 are building applications on top of APIs. Building the infrastructure layer (MCP protocol, Temporal workflows, observability) is a different skill set
3. **It's provable** — the two production systems, the gists, the OOM postmortem, and the meta-engineering (ralph loops) all validate this label independently
4. **It has an arc** — systems programming (C, CUDA) → distributed systems (BFT consensus) → ML/CV → AI infrastructure. Each layer built on the last

### What the archetype is NOT

- Not "ML engineer" — the ML work (crowNNs, LPRNet) is real but 2023-vintage and not the current focus
- Not "full-stack developer" — there's frontend work (Next.js in Cheerful) but it's not the story
- Not "DevOps/platform engineer" — the CI/CD work (GitHub Actions, Fly.io) is a means, not the identity
- Not "blockchain engineer" — the BFT consensus research is impressive but 2022-era context, not current identity

---

## One-Line Bio

**Draft options** (max 160 chars for GitHub bio field):

1. `Building production AI agent infrastructure — MCP servers, durable workflows, autonomous analysis systems` (104 chars)
2. `AI infrastructure engineer. I build the reliability layer for AI agents in production.` (87 chars)
3. `Building the plumbing that makes AI agents work in production. MCP, Temporal.io, Claude Agent SDK.` (99 chars)
4. `I build production AI infrastructure — custom MCP servers, durable workflows, observability pipelines.` (103 chars)

**Recommended**: Option 2. It's the cleanest statement of identity. Concrete without being a keyword dump. "Reliability layer" is distinctive and accurate.

**Current bio for comparison**: "Engineer, sometimes Product. Really into LLMs right now!" — vague, hedging ("sometimes Product"), and positions as hobbyist ("really into X right now") rather than builder.

---

## Narrative Bullets (3–5)

These are the identity pillars — what the profile README and pin selection must collectively communicate:

### 1. Production AI systems at scale
Two deployed AI platforms across two different orgs, 49,500+ combined LOC. Same architectural stack (Claude Agent SDK + MCP + Supabase + Langfuse) proven in two domains — not a one-off. Platform thesis.

**Evidence**: Cheerful (Nuts & Bolts AI), Decision Orchestrator (PyMC Labs). Both private, but describable.

### 2. Infrastructure-layer builder, not application-layer consumer
Custom MCP protocol implementation (not FastMCP). Temporal.io for durable AI workflows. Scope-based credential gating. This is the person who builds the tools other engineers use to build AI apps.

**Evidence**: Decision Orchestrator's MCP registry, Cheerful's Temporal pipelines.

### 3. Systems depth from the ground up
Concurrent file server in C with hand-over-hand locking. GPU parallel algorithms in CUDA. BFT consensus protocol with BLS threshold signatures in Go. The AI infrastructure work is credible because it sits on top of genuine systems engineering foundations.

**Evidence**: `multithreaded-fileserver`, `blocked-floyd-warshall-gpu`, BHS-GQ org repos.

### 4. Meta-engineering instinct
Built a self-authored iterative analysis system (ralph loops) that runs autonomously on GitHub Actions CI — frontier-based convergence, failure detection, auto-issue creation. This profile was assembled by it.

**Evidence**: The monorepo, this loop, the CI workflow.

### 5. Open-source contributor (emerging)
Contributing to PyMC's ecosystem — ZeroSumNormal example notebook PR to pymc-devs/pymc-examples. Production debugging artifacts published as gists (OOM postmortem).

**Evidence**: `pymc-examples` fork + PR #844, public gists.

---

## What to Emphasize vs. Downplay

### Emphasize (these tell the story)

| Signal | Why | Where |
|--------|-----|-------|
| Production AI systems (Cheerful, Decision Orchestrator) | Core identity — builds real AI infra | Profile README (described, not linked) |
| Custom MCP implementation | Strongest technical differentiator in 2026 | Profile README, bio keywords |
| Temporal.io for AI workflows | Unusual reliability instinct | Profile README |
| Systems foundations (C, CUDA, Go) | Validates infrastructure credibility | Pins (multithreaded-fileserver, blocked-floyd-warshall-gpu) |
| Meta-engineering (ralph loops) | Memorable hook, shows builder instinct | Profile README opener or featured mention |
| OOM postmortem gist | Proves production systems experience | Profile README link |
| ML/CV benchmarking (crowNNs) | Best visible public work | Pin |
| PyMC open-source contribution | Only public professional trace | Profile README mention |

### Downplay (don't hide, just don't feature)

| Signal | Why | Treatment |
|--------|-----|-----------|
| Blockchain/BFT work (BHS-GQ) | 2022-era, not current identity | One-line mention as "distributed systems research" context |
| Scientific computing (halleys-comet, lotka-volterra) | Generic coursework signal | Keep repos, don't pin, minimal description updates |
| LPRNet | Weaker ML project, self-deprecating README | Keep, improve description, don't pin |
| Philippines location | Not relevant to narrative but keep for honesty | Keep, don't highlight |
| "Product" angle | Dilutes the engineering signal | Remove from bio entirely |

### Hide (archive or don't mention)

| Signal | Why | Action |
|--------|-----|--------|
| derwells.github.io | Stale "graduating student" site, actively harmful | Archive repo |
| wordhack | 6-year-old CS11 coursework | Archive repo |
| moodle fork | Empty PHP clone | Archive repo |
| shalltear fork | Empty Discord bot clone | Archive repo |
| stocksbot/tusvi contributions | Coursework noise | Don't mention |

---

## Tone Calibration

### Target tone: Confident, specific, not performative

The profile should read like an engineer writing for engineers. No:
- Badges, GitHub stats widgets, visitor counters, or animated GIFs
- "Passionate about..." or "I love building..." phrasing
- Self-deprecation ("just a hobby project", "not production-ready")
- Keyword stuffing without context
- Emojis used as section markers

Yes:
- Named systems with real numbers ("49,500 LOC across two production orgs")
- Named technologies with why, not just what ("Temporal.io for durable AI workflows — because AI agents fail and need to recover")
- The meta-hook (this profile was assembled by an analysis engine I built)
- Direct, active voice ("I build X" not "X was built")
- Selective personality — one well-placed aside is better than forced humor throughout

### Voice references

The OOM postmortem gist is the best sample of the natural voice — technical, structured, no posturing. The profile README should read like a shorter, curated version of that same voice.

---

## Pin Strategy (6 slots)

Based on the identity pillars, the 6 pins should span the arc from systems foundations → AI infrastructure:

| Slot | Repo | What it signals | Pillar |
|------|------|----------------|--------|
| 1 | `crowNNs` | ML/CV with real benchmarks, GPU training | Pillar 1+3 |
| 2 | `multithreaded-fileserver` | Systems programming, concurrency in C | Pillar 3 |
| 3 | `blocked-floyd-warshall-gpu` | GPU/CUDA, parallel algorithms, HPC | Pillar 3 |
| 4 | `LPRNet` | ML breadth, license plate recognition | Pillar 1 |
| 5 | `halleys-comet` | Numerical methods, scientific computing | Pillar 3 (breadth) |
| 6 | `lotka-volterra` | Numerical methods, root-finding approach | Pillar 3 (breadth) |

**Notes**:
- Slots 1-3 are the critical SHOWCASE repos. Non-negotiable.
- Slots 4-6 are weaker (KEEP-tier) but are the only remaining owned repos after archiving 4. There simply aren't 6 strong candidates — the real work is in private repos.
- `pymc-examples` (fork) can't be pinned via GitHub's standard pin mechanism. Mention it in the README instead.
- Gists can't be pinned in repo pin slots. The OOM postmortem must be linked from the README.
- If the `blocked-floyd-warshall-gpu` README isn't written before pinning, swap it to slot 5 or 6.

**Alternative**: If a `ralph-loops` public repo is created (extracting the loop engine), it would take slot 4 and be the strongest possible "show don't tell" artifact for Pillar 4 (meta-engineering). This is a forward-ralph decision.

---

## Profile README Structure

The README should follow this information hierarchy (detailed content is for the profile-spec aspect):

1. **Hook** (1 line) — who is this person, in one punchy sentence. The meta-hook ("I built an analysis system that assembled this profile") or the identity statement ("I build the reliability layer for AI agents")
2. **What I build** (3-4 lines) — the two production systems, named with tech and scale. Not vague "I work on AI" — specific.
3. **Featured projects** (3-5 items) — pinned repos + the PyMC PR + OOM postmortem gist. One-line descriptions.
4. **Background** (2-3 lines) — the systems foundation context. Brief: "Before AI infra, I built BFT consensus protocols in Go, GPU algorithms in CUDA, and concurrent systems in C." Links to BHS-GQ org.
5. **Currently** (1-2 lines) — contributing to PyMC ecosystem, building with Claude Agent SDK + MCP + Temporal.io
6. **No footer cruft** — no badges, no stats, no "how to reach me" section with 5 social links

---

## The Sparse Contribution Graph

The profile README should address this directly and factually:

> Most of my work lives in private org repos — two production AI systems across two companies. My public repos are the foundations work (systems programming, GPU algorithms, ML/CV) and my open-source contributions are just getting started.

This prevents the wrong inference ("inactive") and signals the right one ("professional, production-focused"). Don't over-explain. One sentence.

---

## Spec Implications

1. **Bio**: Replace "Engineer, sometimes Product. Really into LLMs right now!" with "AI infrastructure engineer. I build the reliability layer for AI agents in production." (87 chars)

2. **Profile README**: Must be written by the profile-spec aspect with complete, final markdown content. Structure above. The README is the single most important artifact — it's where the invisible work becomes visible.

3. **Pin order**: crowNNs → multithreaded-fileserver → blocked-floyd-warshall-gpu → LPRNet → halleys-comet → lotka-volterra. First 3 are the story; last 3 fill slots.

4. **Archive 4 repos**: derwells.github.io, wordhack, moodle, shalltear. This brings the visible repo count from 11 to 7. Quality over quantity.

5. **Topics batch**: All 7 remaining repos get topics. Zero → meaningful discoverability in one batch.

6. **Tone**: engineer-to-engineer, no performative enthusiasm, named systems with real numbers, the OOM postmortem voice as the reference.

7. **The meta-hook**: Whether to use "this profile was assembled by an analysis engine I built" as the README opener is a profile-spec decision. It's memorable and true. Risk: might come across as gimmicky. Benefit: it's the most distinctive possible opener and immediately demonstrates meta-engineering instinct.

8. **Forward-ralph consideration**: Extracting the ralph loop engine as a public repo would be the single highest-impact addition to the profile. It turns Pillar 4 (meta-engineering) from "described in README" to "shown in code." This is a decision for the profile-spec or the forward ralph, not this analysis.
