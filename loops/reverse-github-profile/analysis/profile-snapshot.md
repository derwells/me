# Profile Snapshot — derwells

**Analysis Date**: 2026-02-25
**Sources**: GitHub REST API (`/users/derwells`), public events, gist API, derwells.github.io

---

## Summary

The GitHub profile of Derick Wells is a study in invisibility. The public face — a 7-word bio, 11 repos with zero topics, no pinned repos, no profile README — tells none of the real story. What's hidden: two production AI systems, 4 technically sophisticated public gists from the last 60 days, and a live personal website that isn't even linked. A stranger visiting this profile sees a junior ML student, not a professional AI systems engineer.

---

## Current Profile State

### Core Fields

| Field | Value | Assessment |
|-------|-------|------------|
| Name | Derick Wells | Fine |
| Bio | "Engineer, sometimes Product. Really into LLMs right now!" | Honest but weak — undersells depth |
| Company | (none) | Missing |
| Location | Philippines | Fine |
| Blog / Website | (empty) | **Broken** — derwells.github.io exists but isn't linked |
| Twitter/X | (none) | Fine |
| Public repos | 11 | Low signal |
| Public gists | 4 | Actually impressive but invisible |
| Followers | 10 | Small network |
| Following | 10 | Small network |
| Account created | January 2019 | ~7 years old |
| Profile README | **DOES NOT EXIST** | Critical gap |
| Pinned repos | **NONE** | Critical gap |

### Current Bio Analysis

> "Engineer, sometimes Product. Really into LLMs right now!"

What it communicates to a stranger:
- Someone who's unsure whether they're an engineer or PM
- A hobbyist interested in LLMs (not a builder)
- No tech stack, no domain, no proof

What it should communicate:
- Builds production LLM systems (not just "interested")
- Backend + AI infrastructure, not CRUD apps
- Something concrete (what kind of AI systems?)

---

## Pinned Repos

**Current pins: NONE**

Nothing is pinned. This is the most visible section of a GitHub profile and it's completely empty. A visitor gets the default repo listing sorted by... something. No curation, no story.

---

## Profile README

**Does not exist.** The `derwells/derwells` repo was confirmed non-existent via API (`404 Not Found`). No special profile README section appears on the profile.

This is the highest-leverage missing piece. A profile README is the first thing a visitor sees — a full-width block above repos with whatever markdown you want.

---

## Contribution Activity

### Recent Public Events (last 90 days)

| Date | Event | Repo |
|------|-------|------|
| 2026-02-13 | PR opened | pymc-devs/pymc-examples |
| 2026-02-13 | Branch created | derwells/pymc-examples (fork) |
| 2026-02-13 | Forked | pymc-devs/pymc-examples → derwells/pymc-examples |

Only 3 public events in the visible window. All from a single day (Feb 13) contributing a PR to PyMC's examples repo. Everything else — all the real work — is in private repos.

### Contribution Graph (inferred)
Contribution graph visible on the profile almost certainly shows a sparse public record. The actual work (Cheerful, Daimon, monorepo) generates zero public commits. A recruiter or colleague checking the contribution graph would conclude minimal activity.

---

## Personal Website: derwells.github.io

**Status: LIVE but catastrophically stale and not linked.**

The site is live (`HTTP 200`) and renders at `https://derwells.github.io`. The repo was last updated 2025-08-02.

**What the site says today:**
> "Hi, I'm Derick Wells."
> "I'm a graduating computer science student at the University of the Philippines Diliman."

This is 100% inaccurate. Derick has clearly graduated. The site references an internship at Thinking Machines Data Science and helping upgrade the university LMS — work from 2021-2022. The copyright footer says © 2023.

The `author__bio` field in the page HTML is **empty** (`<p class="author__bio"></p>`), meaning the sidebar shows no bio text.

**Other problems:**
- Not linked from GitHub profile (the `blog` field is empty)
- LinkedIn is linked (positive: `linkedin.com/in/derick-w-8a26b61a1`)
- GitHub is linked back to profile
- No mention of current work, AI systems, LLMs, anything post-2023
- Academic template ("academicpages") — appropriate for CS students, less so for professionals

**Decision needed**: Update the existing site OR just ensure the GitHub profile stands alone. The site needs heavy rework to be an asset vs a liability.

---

## Public Gists (4 total — the hidden gems)

The 4 public gists are the most impressive public artifacts on this profile. All from the last 60 days (Jan-Feb 2026), all deeply technical, all showing real professional work:

| Gist | Date | Content | Signal |
|------|------|---------|--------|
| **Daimon crash postmortem — Feb 16, 2026** | 2026-02-16 | OOM analysis for Discord bot (Claude Code subprocess, Fly.io memory limits, SIGKILL behavior, concurrency) | ⭐⭐⭐ Production systems debugging |
| **Save Instance Back as Template - Design Document** | 2026-01-24 | Product/engineering design doc for a feature | ⭐⭐ Engineering product thinking |
| **Commissions App - Container Registry Webhook Explanation** | 2026-01-23 | Technical explanation of webhook architecture | ⭐⭐ Backend/DevOps work |
| **Discord Search API for Bots - Current State** | 2026-01-22 | Deep dive on Discord API, limitations, workarounds | ⭐⭐ API research for production bot |

The crash postmortem is exceptional. It shows: production system operation, memory profiling, OOM analysis on Fly.io, Claude Agent SDK internals (spawning subprocess trees), Langfuse integration (counting tool observations per session), and a fix proposal. This alone would impress a senior engineer.

**Problem**: Gists are invisible from the profile unless linked. No visitor would find them.

---

## First Impression: Stranger's Perspective

**Scenario**: A technical recruiter or potential collaborator lands on `github.com/derwells` cold.

What they see in the first 5 seconds:
- Small avatar
- "Derick Wells"
- Bio: "Engineer, sometimes Product. Really into LLMs right now!"
- Philippines
- No company, no website, no socials
- 11 repos (no topics visible in overview)
- No pinned section

What they conclude:
- Junior or mid-level engineer somewhere in Asia
- Interested in LLMs (a lot of people say this in 2026)
- Works on side projects (that ML stuff from 2022-2023)
- No obvious professional signal
- 10 followers = not a recognized voice

What they MISS:
- Two production AI systems in active use by real companies
- Deep expertise in Claude Agent SDK, Temporal.io, MCP protocol
- Systems-level thinking (OOM postmortems, subprocess tree analysis)
- 7 years of coding across 50+ repos
- Live gists with technical depth most engineers never publish

**Verdict**: The profile is a lie of omission. Technically accurate, deeply misleading.

---

## Spec Implications

1. **Profile README is #1 priority** — Create `derwells/derwells` repo. The README must do the work the rest of the profile fails to do.

2. **Fix the blog link** — `https://derwells.github.io` must be in the profile's website field. Even stale, it's better than nothing. Preferably fix the site simultaneously.

3. **Bio rewrite** — "Engineer, sometimes Product. Really into LLMs right now!" → something concrete that signals what you build, not what you're "into."

4. **Pin 6 repos** — Curate. Nothing is currently pinned. Pick the 6 that tell the story (existing analysis in `analysis/repo-inventory.md` has candidates).

5. **Topics on all kept repos** — Zero topics means zero discoverability. This is a 5-minute fix per repo.

6. **Surface the gists** — Link to the crash postmortem from the profile README or add as a featured item. It's impressive work that's publicly accessible but hidden.

7. **Website: update or deprioritize** — The derwells.github.io site saying "graduating CS student" is worse than no site. Either update it to reflect 2026 reality, or add a note in the README that it's outdated.

8. **Contribution graph** — Can't fix directly (it reflects actual commits), but the profile README can explain that real work is in private org repos.
