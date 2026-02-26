# Fork Audit — derwells

**Analyzed**: 2026-02-26
**Sources**: `analysis/repo-inventory.md`, GitHub API (compare endpoints, branch listing, PR search), `analysis/org-contributions.md`

---

## Summary

derwells has 3 public forks. Two (`moodle`, `shalltear`) are empty clones with zero original commits — pure noise. One (`pymc-examples`) is the working branch for an active open-source contribution to pymc-devs, the org derwells currently works with professionally. The fork-audit confirms and refines the `signal-vs-noise` verdicts: archive both dead forks, keep `pymc-examples` for its PR signal value.

---

## Data

### Fork 1: `pymc-examples` — KEEP

| Property | Value |
|----------|-------|
| Upstream | `pymc-devs/pymc-examples` |
| Forked | 2026-02-13 (very recent) |
| Ahead of upstream | 0 commits (on `main`) |
| Behind upstream | 2 commits (on `main`) |
| Custom branches | 9 branches, including `zerosumnormal-notebook` |
| Active PR upstream | **Yes** — PR #844 open in `pymc-devs/pymc-examples` |
| PR title | "Add ZeroSumNormal example notebook" |

**What the work is**: The `zerosumnormal-notebook` branch contains 1 commit adding a comprehensive Jupyter notebook demonstrating the `ZeroSumNormal` distribution introduced in PyMC v5. The notebook covers:
- Mathematical foundations of sum-to-zero constraints and their role in identifiability
- Design matrix linear dependence with categorical predictors
- Contrast coding schemes (reference vs sum-to-zero)
- Practical group-means example
- Advanced multi-axis zero-sum usage

The commit message credits "Claude" as author but co-authored by `noreply@anthropic.com` — indicating this was a Claude-assisted contribution. The PR is open as of Feb 2026.

**Verdict**: **KEEP**. This fork exists to support an active upstream contribution to a major open-source Python probabilistic programming library. The contribution itself is substantive (not a typo fix), and `pymc-devs` is also the org where derwells works professionally (PyMC Labs). The fork being 0 commits ahead on `main` is expected — all work is on the `zerosumnormal-notebook` branch.

**Profile signal**: The PR provides the only public, verifiable link between derwells and their professional work at PyMC Labs. It should be referenced in the profile README.

---

### Fork 2: `moodle` — ARCHIVE

| Property | Value |
|----------|-------|
| Upstream | `moodle/moodle` |
| Forked | 2022-07-28 |
| Ahead of upstream | 0 (compare returned 404 — branches likely diverged names) |
| Commits by derwells | **0** — all commits are by upstream contributors (Jun Pataleta, Paul Holden, etc.) |
| Age | 3.5 years, last pushed 2022-07-29 |

**What the work is**: There is no work. All commits visible in the fork are from upstream Moodle core contributors. The fork was created on July 28, 2022 and nothing was ever done with it. Likely a read-only reference clone during a university course that used Moodle.

**Verdict**: **ARCHIVE**. Pure clone, zero original contribution, 3.5 years stale. Clutters the profile with an irrelevant PHP LMS codebase.

---

### Fork 3: `shalltear` — ARCHIVE

| Property | Value |
|----------|-------|
| Upstream | `lickorice/shalltear` |
| Forked | 2020-05-11 |
| Ahead of upstream | 0 commits |
| Behind upstream | 18 commits |
| Commits by derwells | **0** — fork created and immediately abandoned |
| Age | 5.5 years |

**What the work is**: There is no work. Fork was created on 2020-05-11 at 07:51 and pushed at 08:37 — a 46-minute window — then never touched again. The upstream is a "general-purpose Discord bot" (lickorice/shalltear). No PRs filed upstream, no branches, 18 commits behind.

**Verdict**: **ARCHIVE**. Instant-clone never modified, 5.5 years abandoned. The only Python Discord bot work that matters is `decision-orchestrator` (professional, private). This fork actively misleads anyone who stumbles on the profile.

---

## Patterns

1. **Forks follow life stages**: The two dead forks correspond to exactly two periods — 2020 student Discord bot era (`shalltear`) and 2022 university coursework era (`moodle`). Neither has any original work.

2. **The active fork is new and purposeful**: `pymc-examples` was forked specifically to file a PR — the standard GitHub flow for open-source contribution. It's the only fork that functions as intended.

3. **Confirmation of signal-vs-noise verdicts**: All three fork verdicts here match the `signal-vs-noise` analysis exactly: `pymc-examples` (KEEP, 6/12), `moodle` (ARCHIVE), `shalltear` (ARCHIVE).

---

## Spec Implications

1. **Archive `moodle` and `shalltear`** immediately. No exceptions. These add zero signal and actively undermine the profile's story.

2. **Keep `pymc-examples`** but update its description. The repo's current description is inherited from upstream: "Examples of PyMC models, including a library of Jupyter notebooks." A fork-specific description isn't possible via the standard repo description field in a fork, but topics can be set: add `pymc`, `bayesian-statistics`, `contributing`, `open-source`.

3. **Reference the PyMC PR in the profile README**: "Contributing to [pymc-devs/pymc-examples](https://github.com/pymc-devs/pymc-examples)" with a link to the notebook PR is the only public proof of professional-adjacent open-source work.

4. **The `zerosumnormal-notebook` PR is pin-adjacent**: If the PR gets merged before the profile overhaul, the fork itself becomes SHOWCASE-eligible (PR merged into a major OSS project). Monitor PR #844 status.
