# Identity Synthesis — derwells

**Analyzed**: 2026-02-24
**Sources**: `analysis/repo-clustering.md`, `analysis/signal-vs-noise.md`, `analysis/fork-audit.md`, `analysis/narrative-gaps.md`, `analysis/monorepo-deep-scan.md`, `analysis/org-contributions.md`, `analysis/profile-snapshot.md`, `analysis/repo-readme-scan.md`

---

## Summary

The data converges on a single, crisp identity: a **protocol-level AI infrastructure builder** with unusual technical breadth (GPU kernels → probabilistic modeling → AI agent orchestration) and a demonstrable platform thesis proven across two production deployments. The profile currently shows "CS student who did interesting projects." The profile needs to show "engineer who builds the layer that AI products run on." Everything follows from getting this one reframe right.

---

## Primary Archetype

**"Protocol-Level AI Infrastructure Builder"**

This is the label that best fits the data, for three specific reasons:

1. **Protocol-level, not application-level**: Most AI developers consume MCP tools. This person built the registry — a custom MCP tool registry with `@tool` decorator, context injection, and scope-based credential gating in Decision Orchestrator. That's infrastructure design at the spec layer, not app glue code.

2. **Infrastructure, not apps**: The work produces platforms that other builders run on: Cheerful is the infrastructure that the Nuts and Bolts AI team builds campaigns on; Decision Orchestrator is the infrastructure that PyMC Labs uses to coordinate as an organization. Neither is an end-user product — both are platforms.

3. **Proven twice, same thesis**: Same architectural choices (Claude Agent SDK + MCP + Supabase + Langfuse) deployed independently at two companies in different domains (marketing automation, organizational coordination). Two data points = a position, not a coincidence.

**Alternative labels considered and rejected**:
- "AI Engineer" — generic, used by everyone
- "Full-Stack Developer" — undersells the protocol/infrastructure depth
- "ML Engineer" — incomplete; the public ML repos are historical; the current work is agent infrastructure
- "Researcher" — misleading; this is production systems work, not research

---

## One-Line Bio Draft

**Primary (118 chars)**:
```
AI agent infrastructure @ PyMC Labs & Nuts and Bolts AI | custom MCP, durable workflows, Bayesian ML | GPU when it counts
```

**Alternative (107 chars, slightly punchier)**:
```
Building AI agent infrastructure at PyMC Labs + Nuts and Bolts AI. MCP registries, Temporal.io, probabilistic ML.
```

**Constraints satisfied**:
- Under 160 chars (GitHub bio limit)
- Names actual employers (not "a startup")
- Names actual technologies (not "leveraging AI")
- Implies the GPU capability without overclaiming
- No buzzwords: no "passionate," no "innovative," no "building the future of"

**Recommendation**: Use the primary. The pipe separators create visual rhythm. "GPU when it counts" closes with personality — implies judgment about when GPU-level work is actually warranted, not resume-padding.

---

## Narrative Bullets

These are the 5 sentences that define the profile. Use in the README, paraphrase in prose.

1. **The infrastructure thesis**: Builds AI agent systems at the protocol layer — custom MCP tool registries with scope-based credential gating, not FastMCP wrappers. The registry is the differentiator, not the application on top.

2. **The platform pattern**: Two production systems, same architecture (Claude Agent SDK + custom MCP + Supabase + Langfuse + Composio), two different domains. Cheerful (influencer marketing automation at Nuts and Bolts AI) and Decision Orchestrator (organizational OS at PyMC Labs) share the same infrastructure DNA. This is a thesis, not a coincidence.

3. **The GPU thread**: Writes CUDA kernels (blocked Floyd-Warshall benchmarked at 100–10,000 nodes, 10 trials per size) and trains CV models that benchmark near SOTA (crowNNs: precision 0.64 vs DeepForest 0.66 on tree crown detection). GPU competency spans the stack from kernel-level to framework-level.

4. **The PyMC embedding**: Employed at PyMC Labs (professional services arm of the PyMC project) AND contributing OSS notebooks to the pymc-devs/pymc-examples library. Not a user, not an employee — both simultaneously. ZeroSumNormal notebook PR (#844, +1,872 lines) is the public artifact.

5. **Meta-systems thinking**: Builds systems for building: a frontier-based iterative analysis engine (ralph loops) running in GitHub Actions CI on a 30-minute cron, and a 14-skill Claude Code framework for disciplined AI agent behavior. The thing being built includes the tools used to build it.

---

## What to Emphasize

**Lead with these, in order**:

1. **Protocol-level MCP work** — This is the most differentiating fact. Most people in "AI engineering" either (a) don't know what MCP is, or (b) know it and use existing servers. Building the registry layer requires reading the spec. Name it directly.

2. **The platform thesis (two companies, same architecture)** — This is the identity crystallization. It converts "I built two things" into "I have a point of view on how to build AI systems." The word "thesis" is exactly right here.

3. **The triple combo (GPU + Bayesian + AI agent infra)** — Each domain alone is common. All three in one person, with production evidence in two of them and competitive benchmarks in the third, is rare. The profile should make this combination visible as a coherent whole, not three isolated interests.

4. **PyMC Labs / PyMC ecosystem integration** — The combination of "employed there" + "OSS contributor to their library" is a strong signal. In the Bayesian ML community, this is immediately legible as deep ecosystem integration. Name both PyMC Labs and the pymc-devs/pymc-examples PR.

5. **Proactive acknowledgment of private work** — "All current work is private — building AI infrastructure for clients" is not an excuse. It's context that reframes the sparse contribution graph from "inactive" to "active under NDA/contractor confidentiality." One sentence does this.

---

## What to Downplay (but not hide)

**Provide as context, not lead story**:

- **Academic ML projects** (crowNNs, LPRNet, halleys-comet, lotka-volterra) — Technically impressive and worth pinning, but they are supporting evidence of technical depth, not the primary story. They prove that the AI infrastructure work is grounded in real ML/numerical knowledge. Present them as "where the technical depth comes from," not "what this person does."

- **Systems programming background** (multithreaded-fileserver) — Good signal of computer science foundations. Don't lead with it; let it appear in the repo list as a natural complement to the GPU work.

- **Personal site** (derwells.github.io) — Expected to exist, neutral. Fix it so it doesn't actively mislead (currently shows the academicpages theme README), then forget about it.

**Do not mention**:

- CS11 word game (wordhack) — archive it
- Moodle fork — archive it
- shalltear bot — archive it (the Discord-bot evolution story is interesting but requires private work to be visible to land; without that context, keeping shalltear just adds noise)

---

## Tone Calibration

**The voice for this profile**: Confident and specific. Not modest, not boastful. Technical enough to be credible; human enough to have a personality.

**Do**:
- Name technologies precisely: "Claude Agent SDK," "Temporal.io durable workflows," "scope-based credential gating" — not "advanced AI tooling"
- Name employers: "PyMC Labs," "Nuts and Bolts AI" — not "a startup" or "my employer"
- Cite numbers: "10,000 nodes," "36,400 LOC," "+1,872 lines" — specificity signals rigor
- Acknowledge constraints honestly: "all current work is private" — not "unfortunately due to NDA..."
- Show methodology curiosity: the Regula-Falsi choice, the SOTA benchmarking — these details show intellectual character

**Don't**:
- "Passionate about..." — delete on sight
- "Leveraging AI to..." — generic
- "Innovative solutions" / "cutting-edge" — meaningless
- Apologize for sparse public activity — address it, don't apologize for it
- Oversell the academic projects as current work — they're historical depth, not current focus
- Mention "Claude" or "ChatGPT" in generic "I use AI" framing — the work is specific enough not to need this

**Personality signals to preserve**:
- The Regula-Falsi choice in lotka-volterra (someone who asks "is there a better method?")
- The SOTA benchmarking in crowNNs (someone who measures, not assumes)
- "10 trials per size for statistical accuracy" in blocked-floyd-warshall-gpu (someone who controls for variance)
- Building tools for their own tools (ralph loop engine) — recursive systems thinker
- These signals already exist in the public repos; the README should reflect the same mindset in prose

---

## Cohesive Identity Statement (for spec writing)

For the forward ralph writing the profile spec, this is the anchor:

> **Derick Wells builds AI agent infrastructure at the protocol layer.** He's shipped two production systems — Cheerful (Nuts and Bolts AI) and Decision Orchestrator (PyMC Labs) — using the same architectural thesis: Claude Agent SDK + custom MCP servers + Supabase + Langfuse. The Decision Orchestrator has a hand-built MCP tool registry with scope-based credential gating. The public repos show where the technical depth comes from: CUDA kernels benchmarked to 10k nodes, CV models near SOTA on tree crown detection, numerical computing in C and Python. He works at PyMC Labs and contributes to their open-source library. All current production work is private. The profile needs to say this, because the repo list never will.

---

## Bio vs README Divide

**Bio** (one line, 160 chars max): States the current identity and context. Employers, tech, one personality beat. See "One-Line Bio Draft" above.

**README** (multi-section): Carries the full story. Covers:
- Hook (who is this person, immediately)
- What I build (the platform thesis)
- Where I build it (named employers + OSS)
- The visible public work (3-5 repos with one-line descriptions)
- The invisible current work (named in prose, no code links needed)
- The GPU thread (interests that explain the public repos)
- Why the graph looks quiet (one sentence)

The bio is the invitation. The README is the room.

---

## Spec Implications

1. **The README is the whole game.** Everything else (pins, descriptions, topics, archiving noise) is table stakes. The README is the only place the actual story lives.

2. **Lead the README with the infrastructure thesis, not the academic projects.** Don't open with "Here are my ML projects from 2023" — open with who this person is right now and work backward to what's in the repo list.

3. **The one-line bio must name employers.** "PyMC Labs" is a legible name in the ML/stats community. "Nuts and Bolts AI" is legible in the AI products space. Vague language wastes the specificity.

4. **The pin set should anchor the technical story.** crowNNs (ML rigor, SOTA benchmarking), blocked-floyd-warshall-gpu (CUDA kernels, after README is written), LPRNet (GPU ML, arxiv-linked), multithreaded-fileserver (systems depth), pymc-examples (PyMC ecosystem). Five strong pins. The 6th slot is flexible — either halleys-comet (numerical computing) or leave it as 5 (the profile doesn't need to fill all 6).

5. **The archetype must anchor the README's opening line.** Not a full summary — just one punchy sentence that answers "what is this person?" before a visitor has to scroll. Something like: "I build the plumbing that AI products run on — custom MCP registries, durable workflow orchestration, agent frameworks. Currently at PyMC Labs and Nuts and Bolts AI."

6. **Future extractable projects** should be mentioned briefly in the README as "in progress" or "working on open-sourcing" — this signals active forward motion rather than a static repo archive. Candidates: ralph loop engine, Claude Code skills framework.
