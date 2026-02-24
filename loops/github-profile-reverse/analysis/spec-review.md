# Spec Review — derwells GitHub Profile Spec

**Reviewed**: 2026-02-24
**Source**: `analysis/github-profile-spec.md`
**Verdict**: **PASS — converge**

---

## Review Questions

### 1. Does the README have personality or is it generic?

**PASS.**

The README has several distinct personality beats:

- "campaigns don't fail silently at 2am" — shows the pragmatic engineering mindset, not feature list prose
- "Same stack. Two domains. A platform thesis, not a coincidence." — three sentences that compress a year of architectural thinking
- "Not just an employee. Not just a user. Both." — punchy. Earns the section.
- "The actual commit cadence is not quiet." — confident without being defensive

The opening line ("I build the infrastructure layer that AI products run on") answers "who is this" in one clause. No preamble, no context-setting. The README is text-forward, no widgets, and specific enough that it couldn't describe anyone else.

The identity-synthesis tone calibration ("confident and specific, not modest, not boastful") is executed correctly. Technologies are named precisely: "Temporal.io durable workflows," "scope-based credential gating," "Claude Agent SDK" — not "advanced AI tooling."

**One note**: The "On the horizon" section mentions `ralph`, the Claude Code skills framework, and the MCP registry as future public projects. This is good forward motion signaling. The risk is that if these never ship public, the section looks aspirational rather than active. Not a blocker — the section uses "working on extracting" (not "coming soon"), which is honest and hedged.

---

### 2. Are the pins telling the right story?

**PASS with one note.**

Pin order: crowNNs → blocked-floyd-warshall-gpu → LPRNet → multithreaded-fileserver → halleys-comet → pymc-examples

The README frames the pins explicitly: "The repos below show where the technical depth comes from — GPU kernels, ML experiments, numerical computing. All from 2022–2024, before the work went private." This framing is necessary and correct. Without it, the pin set tells an "academic ML researcher" story. With it, the pins serve as evidence of technical foundation for the AI infrastructure identity.

The conditional logic around pymc-examples is correctly handled: "If the description update isn't done first, don't pin this repo. Pin `lotka-volterra` as the 6th slot instead." This is exactly the right defensive condition.

**One note**: The spec puts halleys-comet (#5) before pymc-examples (#6). From a narrative standpoint, pymc-examples carries more of the profile story (OSS contribution, PyMC Labs embedding). The ordering is by signal strength (score-based), which is defensible. If the profile owner has to choose between keeping 5 or 6 pins, pymc-examples should stay over halleys-comet — the spec doesn't explicitly say this but the analysis files imply it. Not a spec failure; a callout for awareness.

---

### 3. Are we archiving enough noise?

**PASS.**

Archive list: moodle (pure upstream clone, 0 original commits), shalltear (generic Discord bot fork from 2020, no post-fork activity), wordhack (CS11 freshman assignment, RST stub README).

All three are 1/12 on the signal scoring rubric. These are not borderline calls.

The two lowest-scoring *kept* repos — derwells.github.io (4/12) and lotka-volterra (4/12) — are both correctly retained. Archiving a personal site repo looks strange; it's expected to exist and neutral after the README fix. lotka-volterra is original work and carries the Regula-Falsi methodological angle that the identity-synthesis flagged as a personality signal worth preserving.

Post-cleanup: 8 visible repos with clean descriptions and topics. Significantly better signal-to-noise than 11 repos with no descriptions, no topics, and 3 pure noise forks.

---

### 4. Are descriptions punchy or boring?

**PASS — all 8 descriptions are specific and non-generic.**

| Repo | Verdict |
|------|---------|
| crowNNs | "FCOS replacing RetinaNet, benchmarked vs DeepForest and lidR" — technique + evaluation context. ✓ |
| blocked-floyd-warshall-gpu | "CUDA kernels benchmarked 100–10,000 nodes" — concrete scale signals rigor. ✓ |
| LPRNet | "arxiv:1806.10447" citation + "CCPD-Base" dataset — both signal applied ML credibility. ✓ |
| multithreaded-fileserver | "hand-over-hand locking, reader/writer thread groups, autotest suite" — specific technique, not "a concurrent server." ✓ |
| pymc-examples | "Working fork — ZeroSumNormal example notebook contributed to pymc-devs/pymc-examples (PR #844)" — explains the fork immediately. ✓ |
| halleys-comet | "4th-order Runge-Kutta ODE solver" — names the method, which is the whole point of the repo. ✓ |
| lotka-volterra | "via Regula-Falsi root-finding (alternative to Runge-Kutta)" — methodological angle foregrounded. ✓ |
| derwells.github.io | "Source for derwells.github.io — personal site built on Jekyll + Minimal Mistakes" — appropriate brevity for a utility repo. ✓ |

None of the descriptions are "A project that demonstrates X skills." All name specific techniques, scales, or algorithms.

---

### 5. Is anything missing?

**Mostly PASS — one execution ordering issue to flag.**

**Coverage check**:
- ✓ Profile bio (118 chars, under 160 limit)
- ✓ Profile README (complete markdown, ready to commit)
- ✓ Pin list (6 repos, ordered, justified)
- ✓ Archive list (3 repos, each with specific reason)
- ✓ Description updates (all 8 kept repos)
- ✓ Topic tags (all 8 kept repos, 3-5 tags each)
- ✓ Pre-work A: blocked-floyd-warshall-gpu README (complete content provided)
- ✓ Pre-work B: derwells.github.io README fix (2-line replacement provided)
- ✓ Future public repos (flagged as optional candidates, not required)
- ✓ Execution script (`gh` CLI, `set -euo pipefail`, all steps covered)

**Execution ordering ambiguity** (minor — forward ralph will resolve, but worth noting):

Section 0 lists this execution order:
1. Pre-work A (blocked-floyd-warshall-gpu README)
2. Pre-work B (derwells.github.io README)
3. Run execution script (archives, descriptions, topics, bio)
4. Create `derwells/derwells` repo and push profile README
5. Pin repos (included in script)

The ordering says "push profile README" (step 4) happens AFTER running the script (step 3), but the script's pre-flight check asks "Have you pushed the profile README?" before running. Also, Step 5 of the script creates the `derwells/derwells` repo if it doesn't exist — but you can't push the README to a repo that doesn't exist yet, so the profile README push can only happen after the script creates the repo.

Recommended execution ordering (not a blocker, just clearer):
1. Pre-work A: Write blocked-floyd-warshall-gpu README (clone repo, push)
2. Pre-work B: Fix derwells.github.io README (clone repo, push)
3. Run execution script — Step 5 will create `derwells/derwells` repo
4. Push profile README content to the newly created `derwells/derwells` repo
5. (Pinning happens as part of the script's Step 6)

The forward ralph reading this carefully will figure it out. The pre-flight confirmation prompt is a reasonable safety net. Not a spec failure.

**What's intentionally not included** (correct omissions):
- No automation for profile README git push — this is correct; it requires manual git operations (clone, write file, commit, push), which can't be done purely with `gh api`
- No automation for creating the blocked-floyd-warshall-gpu README (requires cloning the repo and committing a file) — correctly delegated to pre-work section
- No CI/CD setup — out of scope

---

### 6. Would a stranger understand the breadth + depth in 30 seconds?

**PASS.**

Walking through the 30-second path:

**Seconds 0–5**: Bio line — "AI agent infrastructure @ PyMC Labs & Nuts and Bolts AI | custom MCP, durable workflows, Bayesian ML | GPU when it counts"
→ Immediately: two named employers, three specific technologies, one personality beat. Story established.

**Seconds 5–15**: Profile README opens — "I build the infrastructure layer that AI products run on — custom MCP registries, durable workflow orchestration, agent frameworks."
→ Confirmed: infrastructure builder, specific what.

**Seconds 15–25**: "What I build" section — two named systems (Cheerful, Decision Orchestrator), one-line each with specifics. "Same stack. Two domains. A platform thesis, not a coincidence."
→ Understood: this person has a repeatable position, not a one-off project.

**Seconds 25–30**: Pin row — crowNNs, blocked-floyd-warshall-gpu, LPRNet, multithreaded-fileserver
→ Technical foundation visible: ML experiments, CUDA kernels, C systems work.

**Verdict**: Yes. A stranger lands on this profile and within 30 seconds knows: (a) what this person does right now, (b) who they do it for, (c) what technical depth the ML/GPU repos represent, and (d) why the contribution graph looks sparse. The profile has no unanswered questions that aren't intentionally left open.

---

## Spec Completeness Matrix

| Section | Status | Notes |
|---------|--------|-------|
| Bio | ✓ Complete | 118 chars, specific, named employers |
| Profile README | ✓ Complete | Ready to commit verbatim |
| Pin list | ✓ Complete | 6 repos, justified, conditional for pymc-examples |
| Archive list | ✓ Complete | 3 repos with specific reasons |
| Description updates | ✓ Complete | All 8 kept repos, punchy and specific |
| Topic tags | ✓ Complete | All 8 kept repos, 3-5 tags each |
| Pre-work A (blocked-FW README) | ✓ Complete | Full README content provided |
| Pre-work B (site README fix) | ✓ Complete | 2-line replacement provided |
| Future repos (optional) | ✓ Complete | 3 candidates flagged with rationale |
| Execution script | ✓ Complete | All steps, idempotent where possible |
| Execution order | ⚠️ Minor ambiguity | Profile README push ordering unclear; forward ralph will resolve |

---

## Verdict

**PASS — converge.**

The spec produces a profile that tells the correct story (protocol-level AI infrastructure builder, working at two companies, with GPU/ML technical depth as foundation) in a way that's immediately legible to a technical stranger. The README has personality. The descriptions are specific. The archive list is decisive. The execution script covers all mechanical changes.

The execution ordering ambiguity is minor and self-resolving — the pre-flight check and step structure make the intent clear even if the sequence in Section 0 is slightly imprecise.

No additional fix-it aspects needed. Writing `status/converged.txt`.
