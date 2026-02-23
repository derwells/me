# Profile Snapshot — derwells

**Analyzed**: 2026-02-23
**Source**: GitHub API (live), GraphQL (unavailable — unauthenticated), public events API

---

## Summary

Derick Wells's GitHub profile is a blank slate with no bio, no profile README, no pinned repos, and no topic tags anywhere. A stranger visiting gets zero orientation: just a name, a location (Philippines), and 11 scattered repos spanning ML, numerical computing, systems programming, and old forks. The profile is functionally invisible.

---

## Raw Profile Fields

| Field | Value | Status |
|-------|-------|--------|
| Name | Derick Wells | ✓ Set |
| Location | Philippines | ✓ Set |
| Bio | *empty* | ✗ Missing |
| Company | *empty* | ✗ Missing |
| Blog/website | *empty* | ✗ Missing |
| Twitter | *empty* | ✗ Missing |
| Email (public) | *empty* | ✗ Missing |
| Hireable | *not set* | ✗ Missing |

**Score: 2/8 fields populated.** The minimum possible presence.

---

## Structural Elements

### Profile README
- `derwells/derwells` repo does **NOT exist**
- No profile README whatsoever
- A visitor sees only the default GitHub profile layout

### Pinned Repos
- **None pinned** (confirmed via events API; GraphQL unavailable)
- GitHub defaults to showing recently updated repos
- Currently the "top" repos shown would be: pymc-examples (Feb 2026), derwells.github.io (Aug 2025), LPRNet, crowNNs...
- The ordering conveys no intentional narrative

### Topic Tags
- **Zero topics on any repo** (confirmed from repo-inventory)
- No discoverability via GitHub's topic search
- A stranger has no tag-based orientation

---

## Activity Level

**Public activity is sparse.** The only public events in the last year:
- 2026-02-13: Forked `pymc-devs/pymc-examples`, created a branch, opened a PR

That's it — 3 public events, all from one day, all related to one fork. This low public event count reflects that real work happens in private repos (`me` monorepo, `qabot`, org repos).

**Account stats**:
- Account age: ~7 years (since Jan 2019)
- Followers: 10 | Following: 10
- Public repos: 11
- Public gists: 4 (content unknown — possible signal worth checking)

---

## First Impression: What A Stranger Sees

Visiting `github.com/derwells` today:

1. **No bio** — First thing a visitor notices is: nothing. No hook, no context.
2. **No pinned repos** — The feed shows whatever GitHub's default sort is (recently updated). Currently this surfaces pymc-examples (a fork), which is actively misleading.
3. **Repo list** — Scrolling down: a mix of old ML projects (crowNNs, LPRNet), physics simulations (halleys-comet, lotka-volterra), systems code (multithreaded-fileserver), an unexplained CUDA repo with no description, and some dead forks.
4. **No narrative** — A stranger cannot tell: Is this a student? A researcher? A software engineer? What do they care about? What are they working on now?

**The gut reaction**: "This looks like an inactive account. Maybe a student who hasn't updated in years." This is the WRONG impression — the person is actively building sophisticated AI agent systems, but all that work is invisible.

---

## What's Absent (and What It Costs)

| Missing Element | Cost |
|-----------------|------|
| Profile README | No hook, no story, no differentiation |
| Bio | No one-line context for who this person is |
| Pinned repos | Profile shows stale forks by default |
| Topic tags | Zero discoverability via GitHub search |
| Website/blog | No path to deeper context |
| Description on blocked-floyd-warshall-gpu | Impressive GPU work is completely dark |

---

## Spec Implications

1. **Profile README is highest priority** — Create `derwells/derwells` repo with a README. This is the single biggest ROI change.
2. **Bio line** — Short, punchy, factual. Should hint at AI systems + current work.
3. **Pin 6 repos deliberately** — Remove the misleading default (fork at top) and tell a curated story.
4. **Do NOT link Twitter** — Field is empty; no cross-linking needed unless social presence exists.
5. **Website** — If `derwells.github.io` is live and reasonable, link it from the profile. Quick win.
6. **Public activity signal is low** — The profile won't show a green contribution graph full of squares. The README and pins need to compensate by being strong enough to communicate active work.
