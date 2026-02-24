# Narrative Gaps — derwells

**Analyzed**: 2026-02-24
**Sources**: `analysis/monorepo-deep-scan.md`, `analysis/repo-clustering.md`, `analysis/org-contributions.md`, `analysis/signal-vs-noise.md`, `analysis/fork-audit.md`

---

## Summary

The gap between "what this person has built" and "what their GitHub shows" is as large as it gets. The public profile reads as a dormant student account — no bio, no pins, no recent activity, a handful of academic repos. The private reality: 49,500+ lines of production AI infrastructure across two companies, a custom MCP registry built at protocol level, an autonomous analysis engine running in CI, and a 14-skill framework for AI agent behavior. Not a single line of this is visible from the public profile. The profile doesn't understate the work — it doesn't represent it at all.

---

## Gap 1: The Entire Professional Identity Is Invisible

**What exists**: Two production AI systems deployed at two companies.

| System | Scale | Key tech | Visibility |
|--------|-------|----------|------------|
| Cheerful (Nuts and Bolts AI) | 13,100 LOC, 5,570 commits, 3 apps, 5-person team | Temporal.io, Claude Agent SDK, MCP, FastAPI, Next.js | **None** — no org trace, no public repo, no mention anywhere |
| Decision Orchestrator (PyMC Labs) | 36,400 LOC, custom MCP registry, 24 dependencies | Discord.py, Claude Agent SDK, custom MCP protocol, SQLAlchemy 2.0, Fly.io | **Trace**: 1 PR to pymc-devs/pymc-examples (unrelated to DO) |

**What GitHub shows**: Nothing. A stranger cannot tell that this person has shipped two production systems, works at two companies, or has any professional engineering experience whatsoever.

**The holy shit moment**: Cheerful has **5,570 commits** in a private repo — more commits than most public open-source projects that people showcase as career-defining work. It's a *multi-year production platform* that's completely invisible.

**Why it matters**: The public profile's biggest liability isn't the noise repos (moodle, shalltear, wordhack). It's the absence of the actual story. Archiving the noise helps. But the profile needs a README that says "here's what I actually do" because the repo list will never say it.

---

## Gap 2: The Platform Thesis Is Undetectable

**What exists**: Two separate production systems built with identical infrastructure choices — Claude Agent SDK + custom MCP servers + Supabase + Langfuse + Composio. Applied independently to marketing automation and organizational coordination.

**What this signals**: A deliberate architectural thesis — not someone who used Claude once, but someone who has a point of view on how to build AI systems, validated it twice in production across different domains.

**What GitHub shows**: Nothing. The two systems are private. The shared architecture is invisible. The intentionality is undiscoverable.

**Why it matters**: "Used AI to build a thing" is generic. "Applied the same Claude SDK + custom MCP + Langfuse architecture across two different business domains because I think that's the right foundation layer for AI products" is a position. The profile README is the only place this position can be stated.

---

## Gap 3: The MCP Registry — The Technical Differentiator

**What exists**: A protocol-level MCP tool registry in Decision Orchestrator, hand-built (not FastMCP, not a wrapper). Includes a `@tool` decorator, context injection, and scope-based credential gating — tools only access credentials scoped to their server/channel context.

**What this signals**: Understanding MCP at the protocol spec level, not just as a user of available tools. Most AI developers consume MCP tools; this person built the registry layer. That's infrastructure work, not application work.

**What GitHub shows**: Zero. The registry is private.

**Why it matters for the profile**: "Built AI apps" and "built MCP infrastructure" are categorically different claims. The former describes 80% of AI developers right now. The latter describes a much smaller cohort who understand the protocol deeply enough to build their own tooling on top of it. This distinction should be explicit in the profile README.

**Could become a standalone public repo**: The custom MCP registry is conceptually extractable as a standalone project. A clean, documented public version of the scope-based credential gating system would be genuinely novel and worth showcasing. This is speculative but worth flagging as a future option — the spec should note this.

---

## Gap 4: The GPU/HPC Story Is Half-Told

**What exists**: Three public repos demonstrating GPU competency (crowNNs, LPRNet, blocked-floyd-warshall-gpu) plus a pattern of GPU/CUDA stars (ThunderKittens, GPU-Puzzles, tinygrad, llama.cpp) confirming the interest is persistent.

**What's visible**: crowNNs (good README, strong signal), LPRNet (decent README).

**What's invisible**: blocked-floyd-warshall-gpu — CUDA kernel implementation of Blocked Floyd-Warshall, benchmarked at 10,000 nodes, 10 runs per size — has zero README. The GPU/HPC capability exists publicly but the most "pure" HPC piece is completely undiscoverable.

**The gap within the visible**: crowNNs and LPRNet use GPUs to *train models*. blocked-floyd-warshall-gpu *writes CUDA kernels* — a different, lower-level skill (writing GPU kernels vs using GPU-accelerated frameworks). Without a README on blocked-FW, this distinction is invisible and the full stack of GPU competency doesn't register.

**Delta**: GPU story is 60% told. A README for blocked-floyd-warshall-gpu completes it. This is the lowest-effort, highest-leverage action for the forward ralph — one file, one repo, major signal unlock.

---

## Gap 5: The Bayesian Modeling Depth Is Invisible

**What exists**:
- Employed at PyMC Labs (the company that maintains PyMC, a major probabilistic programming library)
- Active OSS contributor: PR #844 to pymc-devs/pymc-examples (+1,872 lines, ZeroSumNormal notebook covering identifiability, sum-to-zero constraints, categorical regression, factorial designs)
- Genuine starred repos in the PyMC ecosystem (PyMC, Arviz, pymc-bart)

**What GitHub shows**: A fork of pymc-examples with no description and a blank main branch. The PR isn't visible unless a visitor specifically checks the fork's branches.

**The unusual combination**: GPU/CUDA competency + Bayesian probabilistic modeling + AI agent infrastructure is a rare combo. Most GPU people don't have probabilistic modeling depth. Most Bayesian modelers don't write CUDA kernels. This combination is a real differentiator that's completely invisible because it requires connecting three dots that the profile never surfaces.

**What should be explicit**: The profile README should name PyMC Labs and call out both the employment (building AI infrastructure for them) AND the OSS contribution to the library they maintain. These reinforce each other — it's not just "I work there," it's "I work there AND contribute to the open-source project they're known for."

---

## Gap 6: The "Active Developer" Illusion

**What GitHub shows**: The most recently touched public repo is pymc-examples (Feb 2026 — today). The second most recent is derwells.github.io (Aug 2025). Every ML repo is from 2023 or earlier. Contribution graph is sparse. The profile looks like someone who was active in university and has since gone quiet.

**What's actually happening**: The person is actively building production systems full-time. The private commit cadence (5,570 commits in Cheerful alone) implies months-to-years of continuous development. The ralph loops are running in CI on a 30-minute cron right now.

**This is an unfixable structural gap** with one exception: the profile README can state it explicitly. Something like "All current work is private — building AI infrastructure for clients" reframes "quiet GitHub" as "active contractor/developer with confidential work" rather than "person who stopped coding."

**Note for the spec**: The forward ralph cannot make private repos public — that's not within scope. But the README must proactively address the activity gap or visitors will infer inactivity incorrectly.

---

## Gap 7: The Ralph Loop Engine — Invisible Meta-System

**What exists**: A self-designed iterative analysis pattern running in GitHub Actions on a 30-minute cron. Frontier-based convergence detection, autonomous bot commits, GitHub issue creation on convergence, matrix strategy for multiple concurrent loops, 1800s timeout per iteration.

**What this signals**: This person doesn't just build apps — they build systems for building things. The ralph loop engine is a meta-cognitive tool made into code. Running an LLM-driven analysis pipeline as a CI job with convergence mechanics is not a common approach; it reflects a specific way of thinking about structured reasoning, automation, and feedback loops.

**What GitHub shows**: The public `.github/workflows/` is visible if someone specifically looks at the me monorepo — but the me monorepo is private. The ralph loop engine is entirely invisible.

**Could become a standalone public repo**: The loop engine (loop.sh, PROMPT.md pattern, _registry.yaml, CI workflow) is a standalone tool that could be published as an open-source project. It would be genuinely useful to others doing LLM-driven iterative analysis. This is worth flagging as a future public project option.

---

## Gap 8: The Claude Code Skills Framework

**What exists**: 14 custom skills built for Claude Code — a prompt engineering framework for disciplined AI agent behavior. ~2,975 lines across SKILL.md files plus supporting docs. Includes meta-skills (a skill for writing new skills, a skill for discovering other skills). Currently used in every Claude Code session in this monorepo.

**What this signals**: Prompt engineering at framework level. Not one-off prompts — a coherent system with taxonomy, patterns, and meta-recursive structure. This is a non-trivial intellectual product.

**What GitHub shows**: Zero. Everything is in the private me monorepo.

**Could become a standalone public repo**: The skills framework is the most immediately publishable of the hidden assets. Extraction would require sanitizing any company-specific references, but the skill structure (each skill is a self-contained SKILL.md with examples, anti-patterns, and verification criteria) is inherently shareable. A public `claude-code-skills` repo would attract meaningful attention from the AI developer community.

---

## The Delta Quantified

| Dimension | What GitHub shows | What actually exists | Gap |
|-----------|-------------------|----------------------|-----|
| Production LOC | ~8,500 (public repos) | ~49,500+ (private) | **6x hidden** |
| Production commits | ~few dozen (public) | ~5,570+ (Cheerful alone) | **100x+ hidden** |
| Current work status | Appears inactive | Full-time production development | **Completely misrepresented** |
| Tech stack breadth | Python/ML, C, JavaScript | + Temporal.io, Claude Agent SDK, MCP protocol, Langfuse, Supabase, Discord.py, Fly.io | **Depth hidden** |
| Architectural sophistication | Academic projects | Protocol-level MCP registry, FCIS, durable workflows | **Category difference** |
| Professional context | No org affiliations visible | Building infrastructure for 2 companies | **Entirely invisible** |

---

## What Should Become Public (Actionable Recommendations)

These are not required for the profile spec but represent future leverage opportunities worth flagging:

1. **Ralph Loop Engine**: Extract as `ralph` — a public repo for frontier-driven iterative analysis in CI. Genuinely novel, would attract attention from AI developers. Requires sanitizing company-specific content from the workflows.

2. **Claude Code Skills Framework**: Extract as `claude-code-skills` or similar. The most immediately publishable hidden asset. A clean public version (14 skills as SKILL.md files + usage docs) would be immediately useful to the AI developer community.

3. **MCP Registry**: Scope-based credential gating for MCP tool registries. Could be a standalone library or part of a larger "building with Claude Agent SDK" post. More technical, smaller audience, but high credibility signal.

**Note**: These are future options, not spec requirements. The forward ralph should focus on the existing profile — these are items to flag for the profile owner.

---

## What the Profile README Must Carry

The profile README is the only vehicle for the invisible work. It must explicitly state:

1. **The current job**: Building AI infrastructure at PyMC Labs + Nuts and Bolts AI. Don't make visitors guess.
2. **What "AI infrastructure" means specifically**: MCP registries, durable workflow orchestration, agent frameworks. Not "I use ChatGPT."
3. **The platform thesis**: Same architecture across two domains — this is the differentiating signal.
4. **The GPU thread**: Real CUDA work, genuine ongoing interest, connects academic and professional work.
5. **The PyMC contribution**: Employment at PyMC Labs + OSS PR to pymc-devs/pymc-examples. Both must be named.
6. **Why GitHub looks quiet**: Proactively address the "inactive developer" perception with one sentence.

---

## Patterns

1. **The profile's biggest problem isn't noise — it's silence.** Archiving moodle/shalltear/wordhack helps, but the absence of the real story is the dominant issue. Noise removal is table stakes; the README is the actual fix.

2. **Two gaps require only prose to close; one gap requires writing code.** The AI Infrastructure gap and the "active developer" gap both close with README content. The GPU/HPC gap closes with a blocked-floyd-warshall-gpu README (one file, one repo). These three actions cover the majority of the delta.

3. **The hidden assets have unusual density.** Most developers have a gap between "what I've done" and "what's on GitHub." This gap is unusually wide — not because the person is being strategic about hiding things, but because the work environment (two private contractor/employee codebases) structurally prevents public attribution.

4. **The combination of skills (GPU + Bayesian + AI Agent Infrastructure) is unusual enough to be the hook.** Individual dimensions (GPU work, Bayesian modeling, AI apps) are common. All three in one person, with production evidence, is not. The profile narrative should lean into this combination rather than presenting them as separate isolated interests.

---

## Spec Implications

1. **Profile README is mandatory, not optional.** The repo list alone cannot tell the story. The README is not a nice-to-have — it's the entire point of the profile changes.

2. **Address the activity gap proactively.** One sentence: "Currently: all work is private — building AI infrastructure for clients." Without this, the profile reads as inactive.

3. **Name the employers.** "PyMC Labs" and "Nuts and Bolts AI" are real names that a visitor can look up. Vague language ("a company" / "clients") loses credibility. Use the actual names.

4. **The platform thesis is the one-liner hook.** A version of: "I build AI agent infrastructure with the same stack — Claude Agent SDK + custom MCP + Langfuse — across whatever domain needs it." This is specific, differentiated, and true.

5. **Flag the extractable projects.** The spec should include a "future public repos" section noting ralph engine and Claude Code skills as candidates. The forward ralph should mention these to the profile owner as options, not requirements.

6. **blocked-floyd-warshall-gpu README is prerequisite work.** Write it before finalizing the pin list, because it determines whether this repo joins crowNNs as a SHOWCASE anchor or stays in the KEEP pool.
