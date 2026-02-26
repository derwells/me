# Repo Clustering — derwells

**Analyzed**: 2026-02-25
**Sources**: `analysis/repo-inventory.md`, `analysis/org-contributions.md`, `analysis/monorepo-deep-scan.md`, `analysis/repo-readme-scan.md`

---

## Summary

11 public repos and ~39 private repos cluster into 8 thematic groups. The dominant story — production AI systems engineering (two orgs, 49,500 combined LOC) — is entirely invisible from the public profile. The visible public work (ML/CV projects, GPU algorithms, a concurrent C fileserver) is a weak shadow of the actual technical depth. There is a coherent career trajectory from systems programming → distributed consensus → ML/CV → production AI orchestration that the current profile completely fails to communicate.

---

## Cluster 1: AI / LLM Systems Engineering (Current, Production)

**Signal strength**: CRITICAL — the most important cluster, zero public visibility

| Repo | Owner | Public? | Language | LOC | Notes |
|------|-------|---------|----------|-----|-------|
| Decision Orchestrator | PyMC Labs (private org) | No | Python | ~36,400 | Discord-based organizational OS; custom MCP protocol |
| Cheerful | Nuts & Bolts AI (private org) | No | Python + JS | ~13,100 | Email automation platform; Temporal.io + Claude Agent SDK |
| `me` (monorepo) | derwells (private) | No | TypeScript | — | Ralph loop engine; GitHub Actions CI; frontier-driven analysis system |
| `qabot` | derwells (private) | No | Python | — | LLM Q&A bot (2024) |
| `pymc-examples` | fork (public) | Yes | Python | — | Only public trace of current professional work |

**What this cluster says**: This person builds production AI systems for real organizations — not demos, not toy repos. Two deployed systems, two different orgs, same architectural stack (Claude Agent SDK + MCP + Supabase + Langfuse). The monorepo itself is meta-engineering: a structured convergence system running autonomously on GitHub Actions.

**Story strength**: Strongest cluster in the profile. Completely invisible to a profile visitor.

**Why it's invisible**:
- Both production systems are in private org repos the user doesn't own
- The monorepo is private
- The only public trace is a single open PR to `pymc-devs/pymc-examples` and its fork

---

## Cluster 2: Machine Learning / Computer Vision (2022–2024)

**Signal strength**: MEDIUM — the best visible public cluster

| Repo | Public? | Language | Stars | Last Updated | Notes |
|------|---------|----------|-------|--------------|-------|
| `crowNNs` | Yes | Python | 1 | 2023-07-27 | Tree crown detection; FCOS vs RetinaNet; benchmarked on T4 GCP |
| `LPRNet` | Yes | Jupyter | 0 | 2024-06-30 | License plate recognition; Keras; CCPD-Base dataset |

**What this cluster says**: Knows ML deeply enough to replace a backbone architecture (RetinaNet → FCOS), run GPU training on GCP, and produce benchmark tables. Demonstrates hands-on CV work, not just tutorials.

**Spec implication**: `crowNNs` is pin-ready. `LPRNet` needs result numbers added.

---

## Cluster 3: High-Performance Computing / GPU Algorithms

**Signal strength**: HIGH potential, but currently invisible due to missing README

| Repo | Public? | Language | Stars | Last Updated | Notes |
|------|---------|----------|-------|--------------|-------|
| `blocked-floyd-warshall-gpu` | Yes | CUDA | 0 | 2023-07-07 | Blocked APSP on GPU; benchmarked 100–10K matrices; NO README |
| `cs171-ejer-2` | No | CUDA | — | 2022-11-11 | CUDA coursework (private) |
| `cs171-ejer1` | No | CUDA | — | 2022-10-03 | CUDA coursework (private) |

**What this cluster says**: Has actual GPU programming experience (CUDA, not just PyTorch wrappers). The blocked Floyd-Warshall implementation is non-trivial — blocked decomposition for cache efficiency on GPU, systematic benchmarking across matrix sizes. This is HPC work.

**Spec implication**: `blocked-floyd-warshall-gpu` needs a README urgently. It's the only public CUDA repo — without documentation it's invisible. With a README + benchmark table, it becomes one of the most distinctive repos on the profile (very few people have public CUDA repos).

---

## Cluster 4: Systems Programming / Concurrent Systems

**Signal strength**: MEDIUM — validates low-level fundamentals

| Repo | Public? | Language | Stars | Last Updated | Notes |
|------|---------|----------|-------|--------------|-------|
| `multithreaded-fileserver` | Yes | C | 0 | 2023-07-07 | Concurrent file server; hand-over-hand locking; worker thread groups |
| `fileserver-cs140-2122` | No | C | — | 2021-11-30 | Earlier file server coursework (private) |
| `custom-udp` | No | Python | — | 2022-05-17 | Custom UDP implementation (private) |
| `azc4` | No | C++ | — | 2023-07-03 | Unknown (private C++ project) |

**What this cluster says**: Built concurrent systems from scratch in C — real threading, hand-over-hand locking (not just mutexes around everything). The fileserver is the refined public version of earlier coursework. UDP implementation shows networking fundamentals.

**Spec implication**: `multithreaded-fileserver` is worth keeping public and pinning. It directly validates the systems layer of the tech stack.

---

## Cluster 5: Blockchain / Distributed Consensus (2022–2023)

**Signal strength**: MEDIUM — strong research signal from a specific period

| Repo | Owner | Public? | Language | Notes |
|------|-------|---------|----------|-------|
| `quorum-hotstuff` | BHS-GQ (org) | Yes | Go | Basic HotStuff BFT inside GoQuorum; 2 major PRs by derwells |
| `emnet` | BHS-GQ (org) | Yes | Python | Emulated network for Caliper benchmarking; 2 PRs |
| `bls-key-generator` | BHS-GQ (org) | Yes | Go | BLS threshold signature keygen; 1 PR |
| `eth1-quorum-port` | derwells (private) | No | Go | Personal Ethereum/Quorum research |
| `eth1-geth-hs` | derwells (private) | No | Go | Personal research |
| `eth1-quorum-old` | derwells (private) | No | Go | Personal research |
| `eth1-setup-generator` | derwells (private) | No | Python | Setup tooling |
| `eth1-testbench` | derwells (private) | No | Shell | Network testbench |
| `besu-ibft-test` | derwells (private) | No | Shell | Hyperledger Besu IBFT 2.0 test |
| `hs-dev-quickstart` | derwells (private) | No | Solidity | HotStuff dev quickstart |
| `kompakt` | derwells (private) | No | Python | Unknown blockchain tooling |

**What this cluster says**: In 2022–2023, did serious distributed consensus research — not application-layer blockchain work, but protocol-level BFT implementation with threshold BLS signatures. This is the kind of work done in academic labs or by engineers building L1 blockchain clients. The org (BHS-GQ) has public repos with real documentation.

**Spec implication**: This cluster is linkable from the profile (org repos are public) but 2–3 years old. If the profile narrative includes distributed systems as context for the AI work, mention it briefly. Not a primary narrative point — more like a "systems depth" credibility signal.

---

## Cluster 6: Scientific Computing / Numerical Methods (2022)

**Signal strength**: WEAK — coursework-tier, low differentiation

| Repo | Public? | Language | Stars | Last Updated | Notes |
|------|---------|----------|-------|--------------|-------|
| `halleys-comet` | Yes | Python | 1 | 2023-01-05 | Runge-Kutta orbit simulation |
| `lotka-volterra` | Yes | Python | 0 | 2022-09-06 | Predator-prey via Regula-Falsi root-finding |
| `cs145-project` | No | Python | — | 2022-05-24 | Unknown scientific computing coursework |

**What this cluster says**: Did numerical methods coursework. Knows Runge-Kutta and root-finding methods. These are interesting physics problems but the repos are indistinguishable from generic coursework.

**Spec implication**: Low value. Keep but don't emphasize. No pinning. They don't add to the primary narrative (AI engineering). Update descriptions minimally.

---

## Cluster 7: Compilers / Systems Software (2023)

**Signal strength**: NICHE — technically interesting but private and dated

| Repo | Public? | Language | Notes |
|------|---------|----------|-------|
| `cs155-bf-to-mips` | No | Rust | Brainfuck → MIPS compiler (CS 155 coursework) |
| `cs155_ps2` | No | Lex | Lexer (coursework) |
| `cs155exam` | No | Yacc | Parser (exam) |

**What this cluster says**: Built a compiler (Brainfuck → MIPS in Rust) and knows lexer/parser theory. Demonstrates systems software depth.

**Spec implication**: All private, stay private. Interesting detail for interviews, not for a public profile narrative.

---

## Cluster 8: Legacy Web / Coursework Noise (2020–2022)

**Signal strength**: ZERO — pure noise for the target narrative

| Repo | Public? | Language | Notes |
|------|---------|----------|-------|
| `derwells.github.io` | Yes | JavaScript | Stale academic site, template README |
| `wordhack` | Yes | Python | 2020 word game, CS11 coursework |
| `moodle` | Yes (fork) | PHP | Moodle fork, no contributions |
| `shalltear` | Yes (fork) | Python | Unknown fork, 2020 |
| `stocksbot` | No | Python | CS 192 coursework Discord bot |
| `tsvjhub`, `tsvj-website`, `tsvj_dorm`, `tweety-sample`, `property_hub` | No | PHP/Vue | Old web projects |
| `dagster_starter` | No | HCL | Starter template |
| `uvle-docs` | No | — | Unknown docs |
| `monolith-notes`, `distributed-ml-notes` | No | — | Personal notes |

**Spec implication**: Everything here should be archived (hidden from profile). The three public forks (`moodle`, `shalltear`) and the stale site (`derwells.github.io`) are the most urgent. `wordhack` is old but original — could stay private if not archived.

---

## Cluster Summary Table

| Cluster | # Public Repos | # Private Repos | # Org Repos | Signal | Primary Action |
|---------|---------------|-----------------|-------------|--------|----------------|
| AI/LLM Systems | 1 (fork) | 2 | 2 (private) | **CRITICAL** | Describe in README; can't pin org repos |
| ML / CV | 2 | 0 | 0 | **MEDIUM** | Pin `crowNNs`; improve `LPRNet` |
| HPC / GPU | 1 | 2 (private) | 0 | **HIGH** | Write README for `blocked-floyd-warshall-gpu`; pin it |
| Systems Programming | 1 | 3 (private) | 0 | **MEDIUM** | Pin `multithreaded-fileserver` |
| Blockchain / Consensus | 0 | 7 (private) | 3 (public org) | **MEDIUM** | Reference from README; don't pin |
| Scientific Computing | 2 | 1 (private) | 0 | **WEAK** | Keep, don't pin |
| Compilers | 0 | 3 (private) | 0 | **NICHE** | Keep private, don't surface |
| Legacy / Noise | 4 + 3 forks | 8+ | 0 | **ZERO** | Archive all |

---

## The Career Arc Story

The clusters, read chronologically, tell a coherent story that the public profile completely fails to convey:

```
2020–2021: Web development (PHP, Vue, Discord bots) → CS fundamentals (MIPS assembly, C)
2022: Systems depth — concurrent programming (C), GPU/CUDA, networking (UDP), compilers
2022–2023: Distributed systems research — BFT consensus (BHS-GQ), Ethereum/Quorum (Go)
2023: ML/CV projects — tree crown detection (CV), license plate recognition, GPU optimization
2024: Professional AI engineering begins — LLM tooling, private org work
2025–2026: Production AI systems — two orgs, custom MCP, Temporal.io, 49,500 LOC
```

The arc is: systems engineer → ML practitioner → AI infrastructure builder.

**This is the profile's best story and it is completely invisible.**

---

## Spec Implications

1. **Primary narrative must be Cluster 1** — The AI/LLM systems engineering cluster is the only story worth telling prominently. All profile energy should focus on surfacing this invisible work.

2. **Supporting clusters (2, 3, 4) validate the systems depth** — ML/CV + HPC/GPU + concurrent systems form a coherent "foundations stack" that explains WHY the AI engineering is credible. Pin reps from each cluster to show this depth.

3. **Blockchain cluster (5) is linkable but secondary** — mention in README as "distributed systems research" context. Don't make it a primary signal (it's 2022-2023 vintage).

4. **Archive the noise cluster (8) aggressively** — 4 public repos + 3 forks should be archived. They dilute the signal-to-noise ratio significantly.

5. **The "six pins" should span the arc**:
   - Something from Cluster 1 (ideally `pymc-examples` with the open PR, or a gist about production AI work)
   - `crowNNs` (Cluster 2 — best README, ML benchmark)
   - `blocked-floyd-warshall-gpu` (Cluster 3 — after README is written)
   - `multithreaded-fileserver` (Cluster 4 — systems fundamentals)
   - Profile README gist or another Cluster 1 artifact
   - Wild card: a gist (OOM postmortem) or the BHS-GQ org link

6. **The scientific computing cluster (6) needs no action** — `halleys-comet` and `lotka-volterra` are passable. Don't pin, don't archive. Just update descriptions.
