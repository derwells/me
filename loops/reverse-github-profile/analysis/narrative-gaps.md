# Narrative Gaps — derwells

**Analyzed**: 2026-02-26
**Sources**: `analysis/monorepo-deep-scan.md`, `analysis/repo-clustering.md`, `analysis/org-contributions.md`, `analysis/signal-vs-noise.md`, `analysis/fork-audit.md`

---

## Summary

The gap between "what derwells has built" and "what their GitHub profile shows" is not a small discrepancy — it's a near-total misrepresentation. The public profile presents a university-project-era engineer with stale repos and no narrative. The reality is a production AI infrastructure engineer with two deployed systems (49,500+ combined LOC), a self-authored autonomous analysis engine, protocol-level MCP implementations, and serious distributed systems research. Every high-signal piece of work is invisible. The profile README is the critical missing container.

---

## Invisible Work Inventory

### Tier 1: "Holy Shit" Invisibles

These would cause a meaningful recalibration of how a technical person views this engineer.

#### 1. Two Production AI Systems — Zero Visibility

| System | Where | LOC | Key Tech | Visibility |
|--------|-------|-----|----------|------------|
| Decision Orchestrator | PyMC Labs (private org) | ~36,400 | Custom MCP protocol, FCIS, 7 integrations, Fly.io | **Zero** |
| Cheerful | Nuts & Bolts AI (private org) | ~13,100 | Temporal.io, Claude Agent SDK, Next.js 16+, FastAPI | **Zero** |

**Why this is "holy shit"**:
- Combined scale: 49,500 LOC across two separate production orgs
- Decision Orchestrator's custom MCP implementation is a genuine differentiator: building at the protocol layer (not FastMCP) while most engineers are still figuring out how to consume existing MCP servers. Scope-based credential gating per channel/server is a real security architecture decision.
- Temporal.io for AI workflows: using durable execution for a production AI pipeline demonstrates reliability engineering instinct that's genuinely uncommon in the current "vibe code everything" LLM tooling era.
- Same architectural stack proven across two different domains: not a one-off. Platform thesis.

#### 2. The Ralph Loop Engine — Zero Visibility

A self-authored iterative analysis system running autonomously on GitHub Actions CI:
- Wave-based frontier with dependency resolution
- Convergence detection (`status/converged.txt`)
- Failure detection (3 consecutive → stop)
- Auto-creates labeled GitHub issues on convergence
- CI matrix strategy: parallelizes loops with `fail-fast: false`
- The system is running right now — **this very loop is the engine analyzing itself**

**Why this matters to a technical reader**: Most engineers document their work in Notion or a spreadsheet. This person built a structured convergence machine that runs headless on GitHub Actions. It's meta-engineering: a system for building analytical systems.

**The meta-story**: This loop is the ralph loop engine describing itself. That's a hook worth using in the profile README.

#### 3. Production Debugging Track Record — Near-Zero Visibility

The public gists (Feb 2026) include an OOM postmortem and design documents. These are genuine production artifacts — incident reports with root cause analysis — but they live in GitHub gists with zero discoverability. No links from the profile. Nobody looks at gists without being pointed there.

**Why this matters**: An OOM postmortem proves production systems experience in a way that no repo listing can. It says: "I run things in production and debug them methodically." This is rare and valuable signal.

---

### Tier 2: Strong Signal, Currently Buried

#### 4. BFT Consensus Research — Linkable but Unlinked

5 merged PRs across BHS-GQ org repos (`quorum-hotstuff`, `emnet`, `bls-key-generator`). Contributions include:
- Integrating BLS threshold signatures into a HotStuff BFT implementation
- Overhauling the core HotStuff consensus implementation in GoQuorum
- Building a Hyperledger Caliper benchmarking emulated network

The repos are **public**. The org is **linkable**. Zero connection to the profile.

**The gap**: A stranger visiting `github.com/derwells` sees no evidence of any of this. The BHS-GQ repos exist, have documentation, and are not disreputable work. They're just completely disconnected from the profile.

#### 5. The blocked-floyd-warshall-gpu README Gap

This is a concrete, measurable gap with a concrete fix:
- CUDA implementation of blocked Floyd-Warshall APSP with systematic benchmarks (100–10K matrices)
- Scores 7/12 on signal-vs-noise (SHOWCASE if README exists)
- **No README exists**
- CUDA repos are rare on GitHub profiles. This is one of the most distinctive repos on the profile in potential — and completely invisible in practice.

**What a README enables**: Topics (`cuda`, `gpu`, `parallel-computing`, `hpc`, `algorithms`), discoverability, and a third SHOWCASE-tier pin slot.

---

### Tier 3: Moderate Signal, Partly Visible

#### 6. PyMC Open-Source Contribution — Near-Zero Visibility

Open PR to `pymc-devs/pymc-examples` adding a `ZeroSumNormal` example notebook (Feb 2026). This is:
- A genuine open-source contribution to a widely-used library
- The only public trace of current professional engagement
- Evidence of statistical computing depth (ZeroSumNormal is used in Bayesian hierarchical models)
- Associated with a credible project (PyMC has real academic adoption)

**The gap**: The fork (`derwells/pymc-examples`) exists publicly, but has no topics, no featured placement. The PR is not mentioned anywhere on the profile.

---

## The Delta: Built vs. Shown

| Capability | What's Built | What GitHub Shows | Delta |
|------------|-------------|-------------------|-------|
| Production AI systems | 2 deployed systems, 49,500 LOC | 0 repos | Critical |
| Custom MCP protocol | Full implementation, scope-gated | 0 | Critical |
| Temporal.io workflows | In production | 0 | Critical |
| Autonomous analysis engine | 6 active loops, CI/CD | 0 | Critical |
| Production debugging | OOM postmortem gists | ~0 (unlinked gists) | Critical |
| BFT consensus (Go) | 5 merged PRs, protocol-level | 0 linked from profile | High |
| GPU/CUDA algorithms | Blocked Floyd-Warshall APSP | Repo exists, no README | High |
| PyMC open source | Active PR, Feb 2026 | Fork, no topics | Medium |
| ML/CV (crowNNs, LPRNet) | Real benchmark work | 2 repos visible, no topics | Low |
| Systems (multithreaded-fileserver) | Hand-over-hand locking in C | Repo exists, undersold description | Low |

**Bottom line**: Every high-signal item is invisible. The low-signal items are the only things a visitor sees, and even those are undersold.

---

## What Would Make Someone Say "Holy Shit"

If a technical hiring manager could see inside the monorepo and private orgs, the recalibration would happen at these moments:

1. **"They built MCP at the protocol layer, not with FastMCP"** — in 2026, most engineers are still just consuming MCP tools. Building the registry, the `@tool` decorator, and scope-based credential gating is a different level.

2. **"They used Temporal.io for an AI pipeline"** — the instinct to add durable execution to an LLM workflow is unusual. It says: "I think about failure modes, not just happy paths."

3. **"The analysis engine is running right now, on itself"** — the ralph loop engine describing itself (this loop) is a compelling piece of meta-engineering. It's the kind of thing that makes engineers stop and think.

4. **"36,400 lines of Python for a Discord bot? That's an org OS."** — the Decision Orchestrator's scale signals that "Discord bot" is the wrong mental model. This is an organizational coordination system with production integrations.

5. **"They wrote BLS threshold signature integration for a BFT consensus protocol in Go, as a university research project"** — protocol-level cryptography work at university is genuinely unusual.

---

## Should Hidden Work Become Standalone Repos?

| Work | Public Repo? | Reason |
|------|-------------|--------|
| Ralph loop engine (template + runner) | **Consider it** | Extractable from the monorepo, genuinely useful to others, demonstrates meta-engineering thinking |
| Cheerful (private org) | No | Proprietary client work |
| Decision Orchestrator (private org) | No | Proprietary client work |
| PH real estate loop outputs | No | Too domain-specific for profile narrative |
| OOM postmortem gist | Already quasi-public | Pin it, link from README |

**The ralph loop engine is the only hidden work that warrants a standalone public repo decision**. The `_template/` directory, `loop.sh`, and `ralph-loops.yml` workflow could be extracted into a public repo (`derwells/ralph` or `derwells/ralph-loops`) that demonstrates the system design. This would be the only public artifact of the meta-engineering work.

---

## The Missing Container: Profile README

The single biggest narrative gap is structural, not content-related. There is no `derwells/derwells` repo. Without a profile README, there is no place to:
- Name the invisible work
- Explain the career arc
- Link to gists, org repos, or external work
- Signal what kind of engineer this person is to a stranger

Every other gap (invisible AI systems, unlinked BHS-GQ work, unlinked gists) would be partially closed by a well-written profile README. The README is not one of several actions — it's the prerequisite for all other narrative changes to land.

---

## Spec Implications

1. **Profile README is the #1 priority** — create the `derwells/derwells` repo and write a README that names the invisible work explicitly. Not "some work I can't show you" — named systems, named tech, real numbers. The spec must provide the complete final content.

2. **The meta-hook is the opener** — "I built an iterative analysis system that runs on GitHub Actions CI. This profile was assembled by it." Short, specific, true, memorable.

3. **Named-system descriptions for private work** — Cheerful and Decision Orchestrator need 1–2 sentence descriptions in the README with tech stack highlights and scale numbers. The custom MCP angle for Decision Orchestrator is the most distinctive element.

4. **OOM postmortem gist must be featured** — pin it as a gist OR link it prominently from the README. It's the only public artifact proving production systems experience.

5. **BHS-GQ org reference** — the README should include a brief mention of the blockchain consensus research with a link to `github.com/BHS-GQ`. It's public, documented, and demonstrates distributed systems depth that corroborates the current AI infrastructure work.

6. **blocked-floyd-warshall-gpu README** — writing this README is a concrete unblocking action. It turns a 7-point repo into a 10-point repo and gives the profile a third SHOWCASE-tier pin. The spec must include the README content.

7. **Consider a ralph-loops public repo** — if the forward ralph has bandwidth, extracting the loop engine as a standalone public repo is the one piece of hidden work that could become a genuine portfolio artifact. It's the "show don't tell" version of describing the meta-engineering work.

8. **Topics batch** — all KEEP/SHOWCASE repos currently have zero topics. A single API batch adds instant discoverability. This must be in the execution script.

9. **The "why the contribution graph looks sparse" note** — the profile README should address the sparse graph directly and factually: "Most of my work lives in private org repos." This prevents the wrong inference (inactive) and signals the right one (professional, production-focused).
