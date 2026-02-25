# Repo Inventory — derwells

**Analysis Date**: 2026-02-25
**Source**: Public GitHub API + `input/github-repos.md` (authenticated snapshot)

---

## Summary

derwells has 11 public repos and ~39 private repos (visible from authenticated snapshot in `input/github-repos.md`). The public profile shows almost nothing of the actual work — no topics on any repo, no profile README, no pinned repos, no org memberships visible. The real work (two substantial AI systems built professionally) is completely invisible. Most public repos are old coursework or hobby projects.

---

## Public Repos (11 total, visible to world)

| Repo | Type | Language | Stars | Last Updated | Has README | Has Description | Has Topics | Archived |
|------|------|----------|-------|-------------|------------|-----------------|------------|----------|
| pymc-examples | fork | Python | 0 | 2026-02-13 | yes | yes | no | no |
| derwells.github.io | original | JavaScript | 0 | 2025-08-02 | yes | yes | no | no |
| LPRNet | original | Jupyter Notebook | 0 | 2024-06-30 | yes | yes | no | no |
| crowNNs | original | Python | 1 | 2023-07-27 | yes | yes | no | no |
| multithreaded-fileserver | original | C | 0 | 2023-07-07 | yes | yes | no | no |
| blocked-floyd-warshall-gpu | original | CUDA | 0 | 2023-07-07 | **no** | **no** | no | no |
| halleys-comet | original | Python | 1 | 2023-01-05 | yes | yes | no | no |
| lotka-volterra | original | Python | 0 | 2022-09-06 | yes | yes | no | no |
| moodle | fork | PHP | 0 | 2022-07-28 | yes | yes | no | no |
| shalltear | fork | Python | 0 | 2020-05-11 | yes | yes | no | no |
| wordhack | original | Python | 0 | 2020-03-15 | yes | yes | no | no |

**Public repo stats:**
- Total: 11
- Original: 8, Forks: 3
- With topics: 0 / 11 (zero!)
- With description: 10 / 11
- With README: 10 / 11 (blocked-floyd-warshall-gpu has neither)
- Stars: 2 total (crowNNs=1, halleys-comet=1)
- Profile README (derwells/derwells): **does not exist**
- Pinned repos: **none visible** (unauthenticated query shows none)

---

## Private Repos (~39, from authenticated snapshot)

These were captured in `input/github-repos.md` from an authenticated session. Not visible to the public.

### Recent / Significant Private Repos

| Repo | Language | Created | Updated | Description | Notes |
|------|----------|---------|---------|-------------|-------|
| me | TypeScript | 2026-02-23 | 2026-02-23 | (none) | The monorepo — ralph loop system, project cards |
| qabot | Python | 2024-11-25 | 2024-11-26 | (none) | Unknown — likely LLM-related Q&A bot |
| azc4 | C++ | 2023-06-20 | 2023-07-03 | (none) | Unknown |
| distributed-ml-notes | — | 2023-02-01 | 2023-02-01 | "Monolithic notes repo" | Notes on distributed ML |
| monolith-notes | — | 2022-09-30 | 2023-04-04 | "Repository of all my Obsidian notes" | Personal notes |

### Blockchain / Distributed Systems Private Repos (2022)

| Repo | Language | Created | Description |
|------|----------|---------|-------------|
| eth1-quorum-port | Go | 2022-11-25 | (none) — Quorum/Ethereum work |
| eth1-geth-hs | Go | 2022-11-27 | (none) |
| eth1-quorum-old | Go | 2022-11-23 | (none) |
| eth1-setup-generator | Python | 2022-11-12 | (none) |
| eth1-testbench | Shell | 2022-11-06 | (none) |
| besu-test | Shell | 2022-10-24 | (none) |
| besu-ibft-test | Shell | 2022-10-20 | "Initial test for Besu using IBFT 2.0" |
| hs-dev-quickstart | Solidity | 2022-12-18 | (none) |
| hs-network-shell | Shell | 2022-12-18 | (none) |
| kompakt | Python | 2022-12-09 | (none) |

### CS Coursework Private Repos

| Repo | Language | Created | Description |
|------|----------|---------|-------------|
| cs155exam | Yacc | 2023-06-18 | (none) |
| cs155_ps2 | Lex | 2023-04-18 | "CS 155 Probset 2" |
| cs155-bf-to-mips | Rust | 2023-03-22 | (none) |
| cs171-ejer-2 | CUDA | 2022-11-11 | (none) |
| cs171-ejer1 | CUDA | 2022-10-03 | (none) |
| cs145-project | Python | 2022-05-24 | (none) |
| cs138-2122 | Python | 2021-10-27 | (none) |
| cs140-2122 | C | 2021-11-05 | (none) |
| custom-udp | Python | 2022-05-17 | (none) |
| hsq-docker-benchmark | Shell | 2023-04-12 | (none) |
| fileserver-cs140-2122 | C | 2021-11-30 | "Naive concurrent file server implementation." |
| mipsscp-cs21-2021 | Python | 2021-06-19 | (none) |
| mipsinc-cs21-2021 | C | 2021-05-24 | (none) |
| mipsinmips-cs21-2021 | Assembly | 2021-05-24 | (none) |
| cpsolns | Python | 2021-10-09 | "My programming problems solutions" |
| short | — | 2023-06-08 | (none) |
| short-paper | — | 2023-06-08 | (none) |

### Old Web / Hobby Private Repos

| Repo | Language | Created | Description |
|------|----------|---------|-------------|
| stocksbot | Python | 2022-02-25 | "Made for the completion of CS 192" |
| tsvjhub | PHP | 2020-07-15 | (none) |
| tsvj-website | Vue | 2021-03-21 | (none) |
| tsvj_dorm | PHP | 2020-05-25 | (none) |
| tweety-sample | PHP | 2020-12-11 | (none) |
| property_hub | PHP | 2020-08-09 | (none) |
| uvle-docs | — | 2022-02-08 | (none) |
| dagster_starter | HCL | 2021-07-01 | (none) |

---

## Key Observations

### 1. Massive Visibility Gap
The public profile (11 repos) tells none of the real story. The user's most impressive work — two production AI systems built professionally for PyMC Labs and Nuts & Bolts AI — has zero GitHub presence. Both projects (see `../../projects/`) are in private org repos not owned by `derwells`.

### 2. Professional Work (Completely Hidden)
From monorepo project cards:
- **Cheerful (Nuts & Bolts AI)**: FastAPI + Temporal.io + Claude Agent SDK + custom MCP + Gmail OAuth + Next.js + Supabase + Langfuse. ~13,100 LOC, ~5,570 commits, 3 apps. Full-stack email automation platform for influencer marketing.
- **Decision Orchestrator (PyMC Labs)**: Discord bot as organizational OS. Custom hand-built MCP protocol (NOT FastMCP), Claude Agent SDK, Supabase, Langfuse, Fly.io. ~36,400 LOC, 285 Python files.

### 3. Public Repo Signal Is Weak
Best public repos:
- `crowNNs` — tree crown detection CV project (1 star), has description
- `multithreaded-fileserver` — shows systems/concurrent programming ability
- `blocked-floyd-warshall-gpu` — CUDA/GPU work but has NO description or README
- `LPRNet` — license plate recognition, shows ML/computer vision work
- `halleys-comet` — numerical methods demo (1 star)

### 4. Zero Discoverability
- **No topics** on any repo (0/11)
- **No profile README**
- **No pinned repos**
- **No blog/website linked**
- Bio: "Engineer, sometimes Product. Really into LLMs right now!" — honest but undersells the technical depth

### 5. Language Distribution (Public)
- Python: 4 repos (crowNNs, halleys-comet, lotka-volterra, wordhack)
- Jupyter Notebook: 1 (LPRNet)
- C: 1 (multithreaded-fileserver)
- CUDA: 1 (blocked-floyd-warshall-gpu)
- JavaScript: 1 (derwells.github.io)
- Forks: 3 (pymc-examples/Python, moodle/PHP, shalltear/Python)

### 6. Activity Timeline
- 2020: Old web projects (PHP), Discord bot
- 2021-2022: University coursework (OS, compilers, networking, numerical methods)
- 2022: Blockchain/Ethereum experiments (private), GPU computing
- 2023: ML/CV projects going public; compiler coursework
- 2024: LPRNet update, qabot (private)
- 2025-2026: Professional AI systems work (all private/org), monorepo system

---

## Spec Implications

1. **Create profile README** — derwells/derwells repo doesn't exist. Must be created.
2. **Add topics to all kept repos** — currently zero. Simple wins.
3. **Pin strategically** — nothing is pinned. Pick 6 that tell the actual story.
4. **Archive noise** — the 3 forks (moodle, shalltear) and old PHP stuff (if public) should be archived.
5. **Surface the AI/LLM work** — the bio hint ("Really into LLMs") is the only signal. The profile needs to deliver on this promise.
6. **blocked-floyd-warshall-gpu** needs at minimum a description and README before it's pin-worthy.
7. **Private repos**: Most coursework/blockchain can stay private. No need to make anything public that isn't ready.
8. **Consider a `projects` or `featured` pinned gist** — since the real work (Cheerful, Decision Orchestrator) can't be linked directly, the profile README can describe them with context.
