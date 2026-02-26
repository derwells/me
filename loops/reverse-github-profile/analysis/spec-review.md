# Spec Review — derwells GitHub Profile

**Reviewed**: 2026-02-26
**Source**: `analysis/github-profile-spec.md` + all 10 prior analysis files
**Method**: Line-by-line review against quality criteria, plus live API verification of all URLs, node IDs, and current profile state

---

## Review Question: "Would a stranger looking at this profile immediately understand what this person does and be impressed?"

**Answer: Yes.** The spec passes. Here's the breakdown.

---

## 1. Does the README Have Personality?

**PASS — strong personality, not generic.**

The README avoids every common pitfall:
- No "Hi, I'm X" greeting (the name is already on the profile)
- No badges, stats widgets, or visitor counters
- No "passionate about" or "I love building" language
- No emoji section headers
- No "how to reach me" block

What it does instead:
- Opens with a bold identity statement: **"I build the reliability layer for AI agents in production."** This is specific ("reliability layer"), differentiating ("for AI agents"), and verifiable ("in production").
- Names two production systems with org names, tech stacks, and LOC. Not "some private work" — concrete: "36K LOC Python. Claude Agent SDK + Supabase + Langfuse + Fly.io."
- The meta-hook ("This profile was assembled by one") is subtle and memorable. Engineers who get it will be intrigued. Those who don't will just read it as "has a CI system."
- Links to the OOM postmortem gist — proves production debugging experience in a way no repo listing can.
- Final line ("Most of my work lives in private org repos. Public repos here are the foundations.") is honest, direct, and addresses the sparse contribution graph without over-explaining.

**Tone**: Engineer-to-engineer. Matches the OOM postmortem voice identified in identity-synthesis. No posturing.

---

## 2. Are the Pins Telling the Right Story?

**PASS — the arc is coherent and the selection is defensible.**

| Slot | Repo | Signal | Assessment |
|------|------|--------|------------|
| 1 | crowNNs | ML/CV with real benchmarks | Best ML project. Pin-ready. |
| 2 | multithreaded-fileserver | Systems programming in C | Hand-over-hand locking is distinctive. Pin-ready. |
| 3 | blocked-floyd-warshall-gpu | GPU/CUDA parallel algorithms | Depends on README being written (spec includes it). Strong after. |
| 4 | LPRNet | ML breadth | Weakish but acceptable filler. |
| 5 | quorum-hotstuff (BHS-GQ) | Distributed systems / BFT consensus in Go | Strong — adds distributed systems depth. Good deviation from identity-synthesis recommendation. |
| 6 | halleys-comet | Numerical methods | Weakest slot. Memorable name, 1 star. Acceptable. |

The pin arc reads: ML research → systems → GPU → ML breadth → distributed consensus → numerical methods. A stranger sees: "this person has depth across the stack, not just one area."

**Note**: The spec improved on the identity-synthesis pin recommendation by swapping lotka-volterra (slot 6) for quorum-hotstuff (slot 5). This is a better choice — BFT consensus in Go with BLS threshold signatures is a far stronger signal than numerical methods coursework. The identity-synthesis said "downplay blockchain" but quorum-hotstuff is protocol-level distributed systems research, not application-layer blockchain. The spec made the right call.

**Weakness acknowledged**: All pinned repos are from 2022-2023. Zero pins from the current era (2024-2026) because the current work is private. The README compensates for this by describing the current work explicitly.

---

## 3. Are We Archiving Enough Noise?

**PASS — the right 4 repos are being archived.**

| Repo | Score | Reason | Assessment |
|------|-------|--------|------------|
| derwells.github.io | 3/12 | Stale "graduating student" site. Actively harmful. | Correct to archive. |
| wordhack | 3/12 | 6-year-old CS coursework. Zero relevance. | Correct to archive. |
| moodle | 0/12 | Empty PHP fork. Pure noise. | Correct to archive. |
| shalltear | 0/12 | Empty fork. 5.5 years stale. | Correct to archive. |

**Result**: 11 → 7 visible repos. All 7 remaining repos have a reason to exist.

**Considered but rejected**: Should lotka-volterra (4/12, barely KEEP) also be archived? No — keeping it has low cost (doesn't actively harm the narrative) and shows numerical methods breadth. Archive would reduce to 6 visible repos which exactly matches pin count, creating the impression that the user only has pinned repos. 7 is the right number.

---

## 4. Are Descriptions Punchy or Boring?

**PASS — SHOWCASE descriptions are punchy, KEEP descriptions are functional.**

| Repo | New Description | Grade |
|------|-----------------|-------|
| crowNNs | "Tree crown detection in airborne RGB — FCOS vs. RetinaNet, benchmarked on GPU" | A — surfaces the comparison and GPU angle |
| multithreaded-fileserver | "Concurrent file server in C with hand-over-hand locking and per-filepath thread groups" | A — names both distinctive design choices |
| blocked-floyd-warshall-gpu | "Blocked Floyd-Warshall APSP on GPU (CUDA) — benchmarked from 100 to 10K-vertex graphs" | A — mentions CUDA and scale range |
| LPRNet | "Keras implementation of LPRNet for license plate recognition, trained on CCPD-Base" | B — functional, removes URL from description |
| halleys-comet | "Halley's comet orbit simulation using 4th-order Runge-Kutta" | B — clean and accurate |
| lotka-volterra | "Lotka-Volterra predator-prey model solved via Regula-Falsi root-finding" | B — surfaces the interesting method choice |

All descriptions are one-liners without trailing periods. Good convention.

---

## 5. Is Anything Missing?

**One minor gap. Not blocking.**

### Verified (PASS)
- Bio: 87 chars, well within 160 limit. Strong identity statement.
- Profile README: All 5 links verified live (crowNNs, multithreaded-fileserver, blocked-floyd-warshall-gpu, OOM gist `aeeb264030016517b23871ce85e38ff8`, PyMC PR #844). All resolve correctly.
- Execution script: Covers all 7 steps (bio, archive, descriptions, topics, README push, profile repo creation, pinning). Has fallback instructions for GraphQL pin failures.
- Node IDs: Verified current 4 pins (LPRNet, multithreaded-fileserver, quorum-hotstuff, emnet) match the unpin node IDs in the script.
- `derwells/derwells` repo confirmed non-existent (404). Script correctly handles creation.
- `blocked-floyd-warshall-gpu` README confirmed non-existent (404). Script correctly handles creation.
- Topics: 35 topics across 7 repos. All relevant and specific.

### New discovery since profile-snapshot
- A 5th gist exists: "Open-Source Readiness: Soft Launch Design for Decision Orchestrator" (Feb 18, 2026). This wasn't captured in the original profile-snapshot (which found 4 gists). The spec's analysis-log notes "10 gists found" — the earlier profile-snapshot was incomplete. **Not blocking** — the OOM postmortem gist is still the right one to feature. The open-source readiness gist is interesting context but not profile-spec material.

### Blog/website field decision
The spec explicitly decides to leave the blog field empty (don't link stale derwells.github.io). **Correct call.** Linking to a site that says "graduating student" is worse than having no link.

### Execution script technical notes
- `base64 -w 0` is Linux-specific (macOS omits `-w`). Fine for the target environment (CI/headless Linux).
- `sleep 2` after repo creation could be tight if GitHub is slow. Low risk — if it fails, rerunning the script will work (the SHA check handles existing READMEs).
- `set -euo pipefail` with `2>/dev/null || echo "..."` fallbacks on pin mutations is correct error handling.

---

## 6. 30-Second Stranger Test

Simulating a cold visit to `github.com/derwells` after the spec is executed:

**Second 0-2 (Bio)**: "AI infrastructure engineer. I build the reliability layer for AI agents in production." → Immediate signal: this person builds production AI infrastructure. Not a hobbyist.

**Second 2-15 (Profile README)**: Bold hook → two named production systems (PyMC Labs: 36K LOC, custom MCP; Nuts & Bolts AI: 13K LOC, Temporal.io) → ralph loops meta-hook → 5 selected works with links → systems background with BHS-GQ link → "most of my work is in private repos."

**Second 15-25 (Pins)**: 6 repos spanning ML/CV → systems → GPU → distributed consensus. Coherent arc. All with descriptions and topics.

**Second 25-30 (Repo list)**: 7 clean repos. No noise forks, no stale sites, no empty READMEs.

**Would they understand?** Yes. The README carries the narrative.
**Would they be impressed?** Yes. The combination of production scale (49K LOC), custom MCP at protocol level, Temporal.io for AI workflows, OOM postmortems, and systems foundations in C/CUDA/Go is a strong, coherent story.
**Would they remember this profile?** Yes. "Reliability layer for AI agents" is distinctive. The meta-hook is memorable. The OOM postmortem link is unusual.

---

## Verdict

**PASS. The spec is ready for execution.**

The profile README is the anchor — it transforms an invisible engineer into a legible one. The pins reinforce the story. The archive removes noise. The descriptions and topics add discoverability.

### Minor suggestions for the forward ralph (non-blocking)
1. **Slot 6 upgrade**: If a public `ralph-loops` repo is ever created, replace halleys-comet (weakest pin) with it.
2. **crowNNs README image**: Adding one example output image of tree crown detection would elevate the README from B+ to A.
3. **LPRNet accuracy metric**: Even one accuracy number in the README would improve the story.
4. **lotka-volterra**: Could be archived in a future pass if more impressive repos are created. Low priority.

### Convergence
All 12 aspects analyzed. Spec passes review. Writing `status/converged.txt`.
