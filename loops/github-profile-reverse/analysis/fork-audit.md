# Fork Audit — derwells

**Analyzed**: 2026-02-24
**Sources**: GitHub API (commits, branches, compare, PR metadata), `analysis/repo-inventory.md`, `analysis/signal-vs-noise.md`

---

## Summary

Three public forks. One has a live, meaningful OSS contribution (pymc-examples). One is a pure clone (moodle). One has original work but it's 6 years old and trivially scoped (shalltear). Signal-vs-noise verdicts are **confirmed**: archive moodle and shalltear, keep pymc-examples — but the keep rationale hinges on surfacing the PR context in the description, not the fork metadata.

---

## Fork 1: pymc-examples

**Fork of**: pymc-devs/pymc-examples

### Branch Analysis

| Branch | Status |
|--------|--------|
| `main` | 0 commits ahead, 2 commits behind upstream — no original work on main |
| `zerosumnormal-notebook` | **7 upstream + 1 original commit** — the PR vehicle |

### The PR (what this fork actually is)

```
PR #844: "Add ZeroSumNormal example notebook"
State: open
Created: 2026-02-13 | Updated: 2026-02-16
Additions: +1,872 lines | Deletions: 0 | Files: 1
```

The fork exists entirely to host the `zerosumnormal-notebook` branch for this open contribution. The PR is a comprehensive Jupyter notebook demonstrating PyMC's `ZeroSumNormal` distribution for categorical regression — covering identifiability problems, the ZSN solution, and practical modeling patterns.

**Commit attribution note**: The branch's original commit is authored as `[Claude]`. This is significant — it means the notebook was written with Claude Code assistance and committed as a Claude-authored commit, then submitted by derwells as a PR. The work is real (1,872 lines of original notebook content) and the OSS contribution is genuine, but the authorship metadata shows AI-assisted generation rather than hand-coded prose.

### Meaningful Contributions?

**Yes** — the PR is original, substantive, and an active contribution to a major Bayesian ML library. But the fork itself shows nothing on the main branch. A stranger browsing the fork sees an empty clone unless they know to look at the branches.

### Verdict: **KEEP**

The fork is the PR vehicle and the PR is real work. Keep it, but description must surface the contribution context explicitly.

**Updated description**: `"Working fork — ZeroSumNormal example notebook contributed to pymc-devs/pymc-examples (PR #844)"`

---

## Fork 2: moodle

**Fork of**: moodle/moodle (the world's open source learning platform)

### Branch Analysis

| Branch | Status |
|--------|--------|
| `MOODLE_13_STABLE` | Upstream stable branch |
| `MOODLE_14_STABLE` | Upstream stable branch |
| `MOODLE_15_STABLE` | Upstream stable branch |

No personal branches. No commits by derwells on any branch.

### Meaningful Contributions?

**None.** The fork has only upstream legacy stable branches — these were present in the upstream repo at fork time, not created by derwells. Zero commits, zero PRs, zero issues referenced.

This was almost certainly cloned as a reference while doing university coursework involving Moodle (LMS used by many universities for course delivery). No evidence of development intent.

### Verdict: **ARCHIVE** (confirmed)

No original work anywhere in the fork. Pure reference clone. Archive immediately.

---

## Fork 3: shalltear

**Fork of**: lickorice/shalltear ("A general-purpose Discord bot")

### Branch Analysis

| Branch | Status |
|--------|--------|
| `master` | Upstream base — shared upstream commits |
| `dev` | Commits by Carlos Panganiban (upstream contributor or co-developer) |
| `price_graph` | **7 commits by `dwells` (derwells)** — original work |

### What's on price_graph

```
7 commits ahead of master | 0 behind
All committed 2020-05-11

Commits by dwells:
  - Rebase price_graph to master
  - Clean plant.py
  - Update requirements.txt to include matplotlib
  - Add images folder
  - Limit log entries in graph to 48
  - Fix plantstats() message and plant stats graph x-axis text
  - Add plant stats graph
```

The work: added matplotlib-based plant stats graphing to the base Discord bot. This is a small feature extension (7 commits in a single day, all 2020-05-11).

### Context

This looks like a collaborative school or friend-group project. Carlos Panganiban appears to be the upstream author or co-developer (commits on `dev` branch include adding `PriceLog` objects, pricing infrastructure). Derwells added the graph visualization layer on top. The project is a price/plant tracking Discord bot — possibly for a game or a shared household interest.

### Meaningful Contributions?

**Technically yes, but irrelevant.** derwells made original commits (7) that added real functionality. However:
- 6 years old (May 2020)
- Trivial scope: one day of work, one feature (matplotlib graph)
- Abandoned since fork date — no activity since 2020-05-11
- Doesn't demonstrate anything the profile needs to show
- The current Discord bot work (Decision Orchestrator at PyMC Labs) is architecturally orders of magnitude beyond this

### Verdict: **ARCHIVE** (confirmed)

Original work exists but is too old, too small, and tells the wrong story. A 2020 matplotlib graph added to a Discord bot does not belong in a profile that needs to convey "production AI infrastructure builder."

**One exception worth noting**: If the profile narrative ever mentions Discord bot evolution (from 2020 shalltear → 2026 Decision Orchestrator), shalltear could be referenced as a historical origin. But this is an edge case that would be handled in profile prose, not by keeping the fork visible.

---

## Final Verdicts Table

| Fork | Commits by derwells | Meaningful Work | Verdict | Reason |
|------|---------------------|-----------------|---------|--------|
| pymc-examples | 1 (on feature branch, AI-authored) | YES — active OSS PR, +1,872 lines | **KEEP** | Live contribution to major Bayesian ML library |
| moodle | 0 | NO | **ARCHIVE** | Pure reference clone, no contributions anywhere |
| shalltear | 7 (on price_graph branch) | MARGINAL | **ARCHIVE** | 6-year-old trivial feature, abandoned, wrong story |

---

## Patterns

1. **Fork ≠ contribution signal on main branch**: All three forks show 0 ahead commits on their default branch. Without branch awareness, the pymc-examples contribution is completely invisible. This confirms that the fork's description is the only way to surface what it's for.

2. **The AI authorship in pymc-examples**: The ZeroSumNormal notebook commit is attributed to `[Claude]`. This is the only repo in the public profile where AI-assisted authorship is explicitly tracked in git. The PR is still a real contribution (submitted and maintained by derwells), but this is context worth knowing for how to frame it — it's Claude-assisted OSS contribution, not hand-coded from scratch.

3. **shalltear is a real fork with original work but wrong era**: The pattern of "small bot feature → production AI infrastructure" is actually a compelling evolution story, but telling that story requires the private monorepo work to be visible somewhere. Without that, keeping shalltear just adds noise.

---

## Spec Implications

1. **moodle**: Archive immediately. No caveats.

2. **shalltear**: Archive. Optionally mention it in the profile README if narrating the "Discord bot origins" angle — but don't pin it.

3. **pymc-examples**: Keep. Update description to surface the PR explicitly. Don't pin this — it's a fork, not an original repo, and a stranger won't understand the contribution without clicking into it. Let the profile README mention it as "active PyMC contributor" instead, with the PR link.

4. **No new SHOWCASE candidates**: The fork audit doesn't surface any hidden SHOWCASE repos. The verdicts from signal-vs-noise stand unchanged.
