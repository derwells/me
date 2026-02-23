# Repo Clustering — derwells

**Analyzed**: 2026-02-23
**Sources**: `analysis/repo-inventory.md`, `analysis/repo-readme-scan.md`, `analysis/monorepo-deep-scan.md`, `analysis/org-contributions.md`

---

## Summary

The 11 public repos cluster into 6 natural groups — but the most important cluster (AI Agent Infrastructure) is entirely private and invisible. The public profile tells a story of "CS student who did interesting GPU, ML, and algorithms projects." The private reality is "builder of production AI systems with a coherent architectural thesis across two companies." The clustering exercise makes this gap impossible to ignore: the visible clusters are all historical artifacts; the invisible cluster is the actual professional identity.

---

## Visible Clusters (Public Repos)

### Cluster A: Machine Learning / Computer Vision
**Repos**: crowNNs, LPRNet
**Signal strength**: STRONG (2 repos, both original, both benchmarked, both use GPU hardware)

| Repo | Description | Key signal |
|------|-------------|------------|
| crowNNs | Tree crown detection, FCOS replacing RetinaNet | Results table vs SOTA (DeepForest, lidR); precision 0.64 vs SOTA 0.66 |
| LPRNet | License plate recognition, Keras implementation of arxiv paper | Paper-linked, GPU-trained (GTX 1660 Super), dataset cited |

**What this tells a stranger**: This person implements ML papers, runs proper experiments, and benchmarks against state-of-the-art. Not tutorials — original experiments.

**Narrative value**: HIGH. crowNNs in particular is the strongest public repo — it shows ML rigor, not just code literacy.

**Cluster coherence**: Strong. Both are vision tasks, both use GPU hardware, both cite external references (papers / SOTA methods). They belong together.

---

### Cluster B: GPU Acceleration / High-Performance Computing
**Repos**: blocked-floyd-warshall-gpu (core), with crowNNs + LPRNet as supporting evidence
**Signal strength**: MODERATE-STRONG for the capability; WEAK for discoverability (blocked-FW has no README)

| Repo | Description | Key signal |
|------|-------------|------------|
| blocked-floyd-warshall-gpu | CUDA implementation of Blocked Floyd-Warshall | Benchmarks at 100–10,000 nodes, GPU vs CPU timing, 10 runs per size |

**Note**: This cluster overlaps with Cluster A — crowNNs and LPRNet both used GPU hardware, showing the GPU capability is consistent and not isolated. The blocked-FW repo is the most pure HPC piece: it's about GPU acceleration itself, not just using a GPU to train a model.

**What this tells a stranger**: Currently nothing (no README, no description). With a README: "This person writes CUDA kernels, not just PyTorch calls — they understand the hardware layer."

**Narrative value**: HIGH latent, ZERO current. The gap between potential and actual discoverability here is the largest in the portfolio.

**Cluster coherence**: This is more of a cross-cutting capability than a standalone cluster. GPU acceleration shows up in 3 repos. If given proper framing (README for blocked-FW), this becomes a credible HPC signal.

---

### Cluster C: Scientific / Numerical Computing
**Repos**: halleys-comet, lotka-volterra
**Signal strength**: MODERATE (2 repos, both original, same period ~2022, clear academic origin)

| Repo | Description | Key signal |
|------|-------------|------------|
| halleys-comet | Runge-Kutta 4th-order ODE solver for orbital mechanics | Math-forward README, parameterized simulation |
| lotka-volterra | Predator-prey dynamics via Regula-Falsi root finding | Methodological framing: "normally Runge-Kutta, this uses Regula-Falsi" |

**What this tells a stranger**: This person is comfortable with numerical methods, differential equations, and scientific simulation. The lotka-volterra choice of Regula-Falsi (non-standard) signals intellectual curiosity about methodology.

**Narrative value**: MEDIUM. These are clearly academic projects but they show mathematical depth. The methodological curiosity (why use Regula-Falsi instead of Runge-Kutta?) is the most interesting signal here — it implies someone who asks "is there a better way?" rather than defaulting to the standard approach.

**Cluster coherence**: Strong. Both are Python numerical simulations with ODE-adjacent methods, both from ~2022, both link to external documentation. Clearly from the same course or period.

---

### Cluster D: Systems Programming
**Repos**: multithreaded-fileserver
**Signal strength**: WEAK (single repo, no supporting evidence)

| Repo | Description | Key signal |
|------|-------------|------------|
| multithreaded-fileserver | Concurrent fileserver in C with hand-over-hand locking | pthread, linked-list with concurrent access, autotest suite |

**What this tells a stranger**: This person can write C and understands concurrent programming. Hand-over-hand (lock coupling) is a non-trivial synchronization strategy.

**Narrative value**: MEDIUM. One repo makes a weak cluster, but the skills demonstrated (C, concurrency, correctness testing) are valuable. Without a companion systems repo, this reads as "had a systems programming course" rather than "systems programmer."

**Cluster coherence**: Thin. Only one repo. May be better presented as a standalone artifact than a cluster.

---

### Cluster E: Personal Web Presence
**Repos**: derwells.github.io
**Signal strength**: N/A (utility repo, not a skill signal)

| Repo | Description | Key signal |
|------|-------------|------------|
| derwells.github.io | Personal website (Jekyll + Minimal Mistakes) | Last updated Aug 2025; currently has wrong README |

**What this tells a stranger**: Currently: "This person copied a Jekyll template and didn't modify the README." Actually: personal website, actively maintained.

**Narrative value**: Neutral to negative in current state. After fixing (correct README, correct description): becomes neutral — it's expected to exist.

**Cluster coherence**: N/A — standalone utility.

---

### Cluster F: Noise / Low-Value Forks
**Repos**: moodle, shalltear, wordhack
**Signal strength**: NEGATIVE (noise that dilutes the profile)

| Repo | Description | Key signal |
|------|-------------|------------|
| moodle | Official Moodle fork | Zero personal contribution — just a clone |
| shalltear | Generic Discord bot fork (2020) | No activity post-fork |
| wordhack | CS11 word game | CS1 assignment, RST-only README that explains nothing |

**What this tells a stranger**: "This person has old forks they never cleaned up." These repos drag down the profile's signal-to-noise ratio.

**Narrative value**: NEGATIVE. They occupy visible space without communicating anything positive.

---

## Hidden Cluster (Private / Invisible Work)

### Cluster G: AI Agent Infrastructure (THE DOMINANT CLUSTER)
**Repos**: Cheerful (private), Decision Orchestrator (private), Ralph loop engine (private), Claude Code skills system (private), qabot (private)
**Signal strength**: ENORMOUS — but completely invisible from public profile

| Asset | Description | Key signal |
|-------|-------------|------------|
| Cheerful | Full-stack influencer marketing automation, 3 apps | Temporal.io, Claude Agent SDK, MCP, 5,570 commits, 5-person team |
| Decision Orchestrator | Discord-based organizational OS, PyMC Labs | Custom MCP registry (protocol-level), FCIS arch, 36,400 LOC |
| Ralph loop engine | CI-driven iterative analysis, frontier-based convergence | Runs every 30 min in CI, autonomous, convergence detection |
| Claude Code skills | 14-skill AI agent programming framework | ~2,975 lines, meta-recursive (skill for writing skills) |

**What this tells someone who can see it**: "This person builds AI infrastructure that other people build things on. Not apps — platforms. Same architectural thesis applied across two domains. They think about AI systems at the protocol level."

**Narrative value**: THE WHOLE STORY. This cluster is the actual professional identity. Every other cluster is academic history.

**Note**: This cannot be linked from the profile directly (private repos), but the profile README must describe it. The story can be told without code links.

---

### Cluster H: Probabilistic Modeling / PyMC Ecosystem (Semi-visible)
**Assets**: pymc-examples fork (public), OSS PR #844 (+1,872 lines), employment at PyMC Labs, Decision Orchestrator deployed for PyMC Labs
**Signal strength**: MODERATE (multiple independent signals pointing to same area)

| Asset | Description | Key signal |
|-------|-------------|------------|
| pymc-examples fork | Public fork, last updated Feb 2026 | Active engagement with PyMC ecosystem |
| PR #844 | ZeroSumNormal notebook to pymc-devs/pymc-examples | +1,872 lines, open OSS contribution to major Bayesian ML library |
| PyMC Labs employment | Building organizational OS for PyMC Labs | Deep ecosystem integration — employed by the people who maintain PyMC |
| Starred repos | PyMC, Arviz, pymc-bart, etc. | Genuine interest, not performative |

**What this tells a stranger**: This person is embedded in the PyMC ecosystem — not a user, but an OSS contributor AND employed by the team that maintains the library.

**Narrative value**: HIGH, and currently nearly invisible. The pymc-examples fork exists publicly but gives no context. The OSS contribution is the most concrete public evidence of Bayesian modeling depth.

---

## Cluster Map Summary

| Cluster | Repos | Visibility | Narrative Value | Action |
|---------|-------|-----------|----------------|--------|
| A: ML/CV | crowNNs, LPRNet | Public | HIGH | Pin crowNNs, keep both |
| B: GPU/HPC | blocked-floyd-warshall-gpu | Public (but hidden) | HIGH latent | Write README — unlock this |
| C: Scientific Computing | halleys-comet, lotka-volterra | Public | MEDIUM | Keep, minor polish |
| D: Systems | multithreaded-fileserver | Public | MEDIUM | Keep |
| E: Web Presence | derwells.github.io | Public | NEUTRAL | Fix README/description |
| F: Noise | moodle, shalltear, wordhack | Public | NEGATIVE | Archive all three |
| G: AI Agent Infrastructure | Cheerful, DO, Ralph, Skills | **PRIVATE** | THE STORY | Describe in README |
| H: Probabilistic Modeling | pymc-examples, PR #844 | **Mostly private** | HIGH | Surface in bio + README |

---

## The Two-Layer Narrative Problem

The profile currently tells a one-layer story: "person who did academic CS projects." The real story is two-layered:

**Layer 1 (visible, historical)**: Strong student who implemented ML papers with GPU hardware, wrote CUDA kernels, did numerical computing, and built concurrent systems in C.

**Layer 2 (invisible, current)**: Builder of production AI infrastructure at protocol level — custom MCP registries, durable workflow orchestration, iterative analysis engines running in CI, AI agent frameworks deployed at PyMC Labs and Nuts and Bolts AI.

The profile README must bridge these layers: acknowledge the visible academic work as context, then pivot hard to the invisible professional work as the actual identity.

---

## Spec Implications

1. **Archive cluster F completely** (moodle, shalltear, wordhack) — they're noise that dilutes the cluster signal.

2. **Unlock cluster B** — Writing a README for blocked-floyd-warshall-gpu with benchmark numbers would make the GPU/HPC story visible and coherent. Currently this is the highest-leverage single file write in the portfolio.

3. **Pin cluster A** (crowNNs, LPRNet) — the visible ML cluster should dominate the pin slots because it has the strongest public evidence of real work.

4. **Surface cluster H in the bio** — "PyMC contributor" or "building for PyMC Labs" is immediately legible to the Bayesian ML community and establishes credibility.

5. **Profile README must carry cluster G** — The AI agent infrastructure story cannot be inferred from the repo list. It must be written out in prose. This is the most important single piece of content to create.

6. **The platform thesis** (same Claude SDK + MCP + Supabase + Langfuse architecture deployed across two different domains) is the sharpest version of the cluster G story. Lead with this.
