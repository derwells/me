# Org Contributions — derwells

**Analyzed**: 2026-02-25
**Sources**: GitHub Search API (public PRs), GitHub public events API, monorepo project cards (`../../projects/`), LinkedIn loop `analysis/org-work-analysis.md`

---

## Summary

derwells has contributed to 5 distinct GitHub orgs across their career. Two are current production work (private, established via project cards). Three are from the university period (2022): a blockchain consensus research project, a CS coursework org, and a minor UP-adjacent student org. The only public trace of current professional work is a single open PR to `pymc-devs/pymc-examples`. Everything else from the professional orgs is in private repos — invisible to the public profile.

---

## Discovery Method

- `gh api /user/orgs` — not usable (no GH_TOKEN in CI environment)
- `/users/derwells/orgs` (public) — returns empty array (org memberships are private, standard)
- **GitHub Search API**: `author:derwells type:pr` — 13 total PRs across all public repos, revealing 4 orgs
- **Public events API**: 3 events total, all Feb 13, 2026 (PyMC PR)
- **Project cards**: Authoritative source for professional org work (private orgs)

---

## Org 1: BHS-GQ — Blockchain Consensus Research (2022–2023)

**Full name**: Basic HotStuff in GoQuorum
**GitHub**: `github.com/BHS-GQ`
**Type**: Academic/research org (university-adjacent)
**Visibility**: Public
**Created**: 2022-11-30

### What it is

A research project implementing the [Basic HotStuff](https://arxiv.org/pdf/1803.05069.pdf) BFT consensus protocol inside GoQuorum 22.7.4 (the enterprise Ethereum fork). Uses [kyber/v3](https://github.com/dedis/kyber) threshold BLS signatures. Built an emulated network (`emnet`) using Hyperledger Caliper for performance benchmarking.

### Repos

| Repo | Language | Stars | Description |
|------|----------|-------|-------------|
| `quorum-hotstuff` | Go | 1 | GoQuorum with Basic HotStuff consensus implementation |
| `bls-key-generator` | Go | 0 | BLS key generation for threshold signatures |
| `emnet` | Python | 1 | Emulated network for benchmarking |
| `caliper-benchmarks` | — | 0 | Hyperledger Caliper benchmark files |
| `caliper` | — | 0 | Hyperledger Caliper fork |

### derwells's Contributions (5 merged PRs)

| PR | Repo | Title | Status |
|----|------|-------|--------|
| #1 | `quorum-hotstuff` | Use threshold signatures (BLS) | Merged |
| #2 | `quorum-hotstuff` | Overhaul Basic HotStuff implementation | Merged |
| #1 | `emnet` | Use separated Caliper instance | Merged |
| #3 | `emnet` | Cleanup repository: experiment data and docu | Merged |
| #1 | `bls-key-generator` | Overhaul/flow go | Merged |

The two PRs to `quorum-hotstuff` are the highest-signal contributions:
- **BLS threshold signatures**: Integrating cryptographic threshold signing into the consensus protocol
- **Overhaul HotStuff implementation**: Described as an overhaul — substantial rewrite, not a patch

### Context

Timeline matches perfectly with private `eth1-quorum-*` repos (Nov–Dec 2022) and the private Solidity/Shell blockchain repos (`hs-dev-quickstart`, `hs-network-shell`). This was clearly a sustained blockchain/consensus research effort during university, possibly a thesis or senior research project. The "BHS-GQ" naming ("Basic HotStuff in GoQuorum") and the professionalism of the org (README quality, Docker support, Hyperledger integration) suggests an academic group project that went beyond typical coursework.

### Tech Demonstrated

- **Go**: Non-trivial Go contributions to a Geth-derived codebase
- **BFT consensus protocols**: Basic HotStuff is the protocol underlying several production blockchains (notably Meta's Diem/Libra lineage)
- **BLS threshold cryptography**: Protocol-level signing; not typical application-layer work
- **Hyperledger Caliper**: Blockchain performance benchmarking

### Profile Relevance

**Medium** — impressive academically but 2022–2023 vintage. Shows distributed systems depth and low-level systems thinking (consensus protocols, cryptography). Not the primary narrative (that's the AI agent work) but corroborates the "distributed systems backend" signal. Worth a brief mention if the profile leans into a distributed systems angle.

---

## Org 2: pymc-devs — Open Source Statistical Computing (2026)

**GitHub**: `github.com/pymc-devs`
**Type**: Open source project (major probabilistic programming library)
**Visibility**: Public
**Context**: The professional home of PyMC Labs (derwells's current employer)

### derwells's Contributions (1 open PR)

| PR | Title | Status | Date |
|----|-------|--------|------|
| pymc-devs/pymc-examples #844 | Add ZeroSumNormal example notebook | Open | 2026-02-13 |

**What it is**: Adding a Jupyter notebook example demonstrating `ZeroSumNormal` distribution to the official PyMC examples repository — the canonical reference notebooks for the widely-used PyMC Bayesian modeling library.

### Context

This PR is the only publicly visible evidence of current professional work. It corroborates the PyMC Labs relationship: derwells contributes to the open-source project that PyMC Labs is the commercial/services arm of. Contributing a documented, working notebook example is a genuine open-source contribution — not a trivial change.

### Profile Relevance

**High** — this is the only public professional contribution. The `pymc-examples` fork on the profile + this PR signals:
1. Active engagement with a real open-source project (not toy code)
2. Statistical computing knowledge (ZeroSumNormal is a specific distribution used in Bayesian hierarchical models)
3. Association with the PyMC ecosystem, which has meaningful name recognition in the data science/ML world

The fork (`derwells/pymc-examples`) should stay public and perhaps get a topic tag (`bayesian`, `pymc`, `probabilistic-programming`).

---

## Org 3: stocksbot — CS Coursework (2022)

**GitHub**: `github.com/stocksbot`
**Type**: University coursework org (CS 192)
**Visibility**: Public (1 repo)

### derwells's Contributions (4 merged PRs)

| PR | Title | Status |
|----|-------|--------|
| #1 | Make EconomyAccount unique per guild | Merged |
| #3 | Add Stocks DB Object and price fetch | Merged |
| #8 | Add cog for listing stock info/prices | Merged |
| #12 | Update embeds | Merged |

**What it is**: A Discord stocks bot built for CS 192 (software engineering course) completion. The public `derwells/stocksbot` repo is the personal fork of this org project.

### Profile Relevance

**Low** — coursework, 2022, trivial compared to current work. Not useful for profile narrative. The `derwells/stocksbot` public repo can be archived.

---

## Org 4: tusvi — Student Community (2022)

**GitHub**: `github.com/tusvi`
**Type**: UP Diliman engineering/student org (GDSC = Google Developer Student Clubs)

### derwells's Contributions (1 PR)

| PR | Title | Status |
|----|-------|--------|
| tusvi/gdsc-upd_engg_ds_interview #1 | Update README.md formatting | Closed |

**Profile Relevance**: **None** — minor README formatting PR to a student org repo.

---

## Org 5: Nuts and Bolts AI — Production Work (Current, Private)

**Type**: Private startup org
**Visibility**: Private (zero public repos)
**Confirmed via**: Project card `../../projects/nutsandbolts--cheerful.md`

### What derwells built

Full-stack AI engineer on Cheerful — an influencer marketing automation platform:
- **Backend**: Python/FastAPI + Temporal.io durable workflows
- **AI layer**: Claude Agent SDK for individualized email personalization
- **Frontend**: Next.js 16+ / React 19 campaign management UI
- **Context Engine**: Slack bot with MCP tool orchestration + Onyx RAG
- **Scale**: ~13,100 LOC, ~5,570 commits, 3 apps, 5-person team

**Profile Relevance**: **Critical** — the most substantial current professional work, zero GitHub visibility. Cannot be linked to from a public profile, but must be described in the profile README.

---

## Org 6: PyMC Labs — Production Work (Current, Private)

**Type**: Professional services arm of the PyMC project
**Visibility**: Private (Decision Orchestrator repo not public)
**Confirmed via**: Project card `../../projects/pymc--decision-orchestrator.md`
**Public trace**: `derwells/pymc-examples` fork + open PR to `pymc-devs/pymc-examples`

### What derwells built

Discord-based organizational OS (Decision Orchestrator):
- **Custom MCP tool registry**: Protocol-level implementation, NOT FastMCP. `@tool` decorator, context injection, scope-based credential gating
- **Dynamic tool assembly**: Each request gets a custom tool set based on workflow + context
- **Three-layer session persistence**: Claude context + Langfuse + Supabase simultaneously, crash-resilient
- **7 platform integrations**: Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io
- **Scale**: ~36,400 LOC, 285 Python files, deployed on Fly.io

**Profile Relevance**: **Critical** — technically the strongest story on the profile. The custom MCP registry is a genuine architectural differentiator in the current AI tooling landscape. Zero GitHub visibility.

---

## Cross-Org Synthesis

### Contributions by Era

| Era | Orgs | Character | Profile signal |
|-----|------|-----------|----------------|
| 2022–2023 | BHS-GQ, stocksbot, tusvi | University research + coursework | Distributed systems depth (BHS-GQ), otherwise noise |
| 2026 | pymc-devs, Nuts & Bolts AI (private), PyMC Labs (private) | Professional production work | Critical — but mostly invisible |

### Public vs. Invisible Work

| Org | Public? | Quality | Visibility |
|-----|---------|---------|------------|
| BHS-GQ/quorum-hotstuff | Yes | Strong (BFT consensus, BLS crypto in Go) | Near-zero (no topics, not linked from profile) |
| pymc-devs/pymc-examples | Yes | Solid (real open-source contribution) | Near-zero (PR not featured) |
| Nuts and Bolts AI | No | Excellent (production AI system) | Zero |
| PyMC Labs | No | Excellent (production AI infrastructure) | Zero (except fork/PR) |

---

## Spec Implications

1. **Profile README must describe the private org work explicitly** — both Cheerful and Decision Orchestrator need named descriptions. Not "some work I can't show" — concrete systems with named tech and real numbers.

2. **pymc-examples fork should get proper topics** — `bayesian`, `pymc`, `probabilistic-programming`, `jupyter`. It's the only public org contribution from current work.

3. **BHS-GQ work is linkable but needs positioning** — The `BHS-GQ/quorum-hotstuff` repo shows genuine distributed systems research from university. If the profile narrative includes distributed systems, this is worth a cross-reference in the README. Could add something like "including a BFT consensus implementation in GoQuorum during university research."

4. **No new repos needed** — The org work doesn't warrant creating new public repos. The better move is describing it well in the profile README.

5. **The PyMC connection is a genuine narrative asset** — "contributes to PyMC open-source" + "builds internal infrastructure for PyMC Labs" is a coherent story. The ZeroSumNormal PR is a concrete example to name.

6. **Contribution graph gap is explainable** — The sparse public contribution graph should be acknowledged in the profile README: "Most of my work is in private org repos." The gists and pymc PR are the only public evidence.
