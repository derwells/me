# Repo Inventory — derwells

**Analyzed**: 2026-02-23
**Source**: Live GitHub API (as of today) + pre-seeded input/github-repos.md

---

## Key Observation: Most Repos Are Private

The pre-seeded `input/github-repos.md` shows ~50 repos historically. The live API returns **11 public repos**. The vast majority of older work (university coursework, blockchain experiments, PHP projects, etc.) has been made private or deleted. This is actually a good sign — deliberate pruning has already begun. But the current 11-repo public face is still not curated or story-driven.

The private `me` monorepo and `qabot` repo contain the most impressive current work (Claude Agent SDK, MCP servers, Supabase, Langfuse, ralph loops) — completely invisible from the public profile.

---

## All Current Public Repos

| Repo | Type | Language | Stars | Forks | Has Desc | Has Topics | Last Activity | Archived |
|------|------|----------|-------|-------|----------|-----------|---------------|----------|
| pymc-examples | fork | - | 0 | 0 | yes | no | 2026-02-13 | no |
| derwells.github.io | original | JavaScript | 0 | 0 | yes | no | 2025-08-02 | no |
| LPRNet | original | Jupyter Notebook | 0 | 0 | yes | no | 2024-06-30 | no |
| crowNNs | original | Python | 1 | 0 | yes | no | 2023-07-27 | no |
| multithreaded-fileserver | original | C | 0 | 0 | yes | no | 2023-07-07 | no |
| blocked-floyd-warshall-gpu | original | Cuda | 0 | 0 | **no** | no | 2023-07-07 | no |
| halleys-comet | original | Python | 1 | 0 | yes | no | 2023-01-05 | no |
| lotka-volterra | original | Python | 0 | 0 | yes | no | 2022-09-06 | no |
| moodle | fork | - | 0 | 0 | yes | no | 2022-07-28 | no |
| shalltear | fork | - | 0 | 0 | yes | no | 2020-05-11 | no |
| wordhack | original | Python | 0 | 0 | yes | no | 2020-03-15 | **no README** |

**Totals**: 11 public repos | 8 original, 3 forks | 2 total stars | 0 topics on any repo

---

## Original Repos — Detailed Assessment

### derwells.github.io
- **Language**: JavaScript (Jekyll theme)
- **Description**: "Github Pages template for academic personal websites, forked from mmistakes/minimal-mistakes"
- **README**: Template README from the academic pages theme — completely generic, not personalized
- **Reality**: Personal website repo. Last touched Aug 2025. Exists but the description makes it sound like a template, not a real site.
- **Notable**: This is the most recently updated original repo (2025).

### LPRNet
- **Language**: Jupyter Notebook
- **Description**: "Keras implementation of LPRNet: https://arxiv.org/abs/1806.10447"
- **README**: Good and concise. States it's trained on CCPD-Base dataset, self-learning mini-project, mentions GPU used (GTX 1660 Super).
- **Reality**: License plate recognition neural network implementation. CV/ML work from a paper.

### crowNNs
- **Language**: Python
- **Description**: "Tree Crown Detection in Airborne RGB imagery"
- **README**: Good. Has a results table comparing CrowNNs vs DeepForest (SOTA) vs lidR. Used GCP T4 GPU.
- **Reality**: Computer vision research — replacing RetinaNet with FCOS for tree crown detection. Benchmarked against state-of-the-art. This is the most impressive public repo.

### multithreaded-fileserver
- **Language**: C
- **Description**: "Multithreaded mock file server"
- **README**: Decent. Shows build commands, explains 3 operations (write/read/empty).
- **Reality**: Systems programming project — concurrent fileserver in C with a linked list.

### blocked-floyd-warshall-gpu
- **Language**: Cuda
- **Description**: **NONE** — completely empty
- **README**: **NONE**
- **Reality**: GPU implementation of the blocked Floyd-Warshall algorithm. High-performance computing. Completely undiscoverable without opening the code.

### halleys-comet
- **Language**: Python
- **Description**: "Halley's comet plotter using fourth-order Runge-Kutta."
- **README**: Decent. Explains the math, has install/run instructions. Links to Google Drive for docs.
- **Reality**: Numerical simulation — Runge-Kutta ODE solver for orbital mechanics.

### lotka-volterra
- **Language**: Python
- **Description**: "Lotka-Volterra predator-prey dynamics solved using root-finding methods."
- **README**: Decent. Links to Google Drive for documentation.
- **Reality**: Alternative numerical approach (Regula-Falsi root finding) for predator-prey dynamics.

### wordhack
- **Language**: Python
- **Description**: "Word-factory game made for the completion of CS11"
- **README**: **NONE**
- **Reality**: Word game built for a CS course. The "CS11" context makes it sound like a freshman assignment.

---

## Fork Repos — Assessment

### pymc-examples
- **Description**: "Examples of PyMC models, including a library of Jupyter notebooks."
- **Reality**: Fork of the official PyMC examples repo. Updated Feb 2026 — suggests active work with PyMC (matches monorepo project card for `pymc--decision-orchestrator`).
- **Added value**: Unknown from metadata alone. Need fork-audit to assess commits.

### moodle
- **Description**: "Moodle - the world's open source learning platform"
- **Reality**: The official Moodle description. Clearly just a clone with no personal contribution.
- **Action**: Archive.

### shalltear
- **Description**: "A general-purpose Discord bot."
- **Reality**: Discord bot fork from 2020. No activity since fork date. Likely a starter template.
- **Action**: Archive (or possibly KEEP if used as base for current bot work).

---

## What's Missing / Invisible

1. **No profile README** — `derwells/derwells` repo does not exist
2. **No bio** — Empty
3. **No topics on any repo** — Zero discoverability
4. **Private monorepo** — All current AI/agent work (Claude SDK, MCP servers, ralph loops) is invisible
5. **Private qabot repo** — Recent Python/AI work not visible
6. **No pinned repos** — No curation signal
7. **blocked-floyd-warshall-gpu** — Impressive GPU work with literally no description or README

---

## Profile-Level Stats

- **Account age**: Since January 2019 (~7 years)
- **Location**: Philippines
- **Followers**: 10
- **Following**: 10
- **Hireable**: not set
- **Blog**: empty
- **Bio**: empty
- **Company**: empty

---

## Summary

The profile currently shows 11 public repos spanning ML/CV (crowNNs, LPRNet), numerical computing (halleys-comet, lotka-volterra), systems/HPC (multithreaded-fileserver, blocked-floyd-warshall-gpu), a personal site, and three low-value forks. None have topic tags. The most impressive current work (AI agent systems, MCP servers, ralph loop engine) is entirely private. The profile tells no story — it reads as a scattered collection of old university projects with two outlier ML repos.
