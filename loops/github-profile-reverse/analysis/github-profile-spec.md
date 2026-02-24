# GitHub Profile Spec — derwells

**Generated**: 2026-02-24
**Sources**: All analysis files in `analysis/`
**Status**: Ready for forward ralph execution

---

## 0. Executive Summary

This spec transforms a blank-slate GitHub profile ("inactive student account") into a profile that accurately represents Derick Wells as a protocol-level AI infrastructure builder working at two companies. The invisible professional work — 49,500+ LOC across two production AI systems — cannot be shown via repos (all private), so the profile README carries the entire story. Everything else (archiving noise, descriptions, topics, pins) is table stakes that clears the way for the README to land.

**Execution order**:
1. Pre-work A: Write `blocked-floyd-warshall-gpu` README (Section 3) — required before pin step
2. Pre-work B: Fix `derwells.github.io` README (Section 8) — required before pin step
3. Run the execution script (Section 10) — archives, descriptions, topics, bio
4. Create `derwells/derwells` repo and push profile README (Section 2)
5. Pin repos via GraphQL (Section 10 — included in script)

---

## 1. Profile Bio

**New bio** (118 chars — under the 160-char GitHub limit):

```
AI agent infrastructure @ PyMC Labs & Nuts and Bolts AI | custom MCP, durable workflows, Bayesian ML | GPU when it counts
```

**Why this bio works**:
- Names both employers explicitly (legible in ML community and AI products space)
- Names actual technologies (not "leveraging AI")
- "GPU when it counts" closes with personality — implies judgment, not resume-padding
- Pipe separators create visual rhythm on a single line
- Zero buzzwords

---

## 2. Profile README

**Target**: `derwells/derwells` repo → `README.md`

Complete markdown content, ready to commit. No changes needed — copy verbatim.

---

```markdown
# derwells

I build the infrastructure layer that AI products run on — custom MCP registries, durable workflow orchestration, agent frameworks. Currently at [PyMC Labs](https://www.pymc-labs.com) and [Nuts and Bolts AI](https://nutsandbolts.ai).

---

## What I build

Two production systems, one architectural thesis: Claude Agent SDK + custom MCP servers + Supabase + Langfuse, applied independently to two different domains.

**Cheerful** @ Nuts and Bolts AI — AI-powered influencer marketing automation. Temporal.io durable workflows (campaigns don't fail silently at 2am), multi-agent pipelines, three apps. Production.

**Decision Orchestrator** @ PyMC Labs — organizational coordination system for a distributed research team. Discord-native. Built a custom MCP tool registry from scratch: `@tool` decorator, context injection, scope-based credential gating (tools only access credentials for their authorized server/channel context). 36,400 lines. Production.

Same stack. Two domains. A platform thesis, not a coincidence.

---

## Public work

The repos below show where the technical depth comes from — GPU kernels, ML experiments, numerical computing. All from 2022–2024, before the work went private.

- **[crowNNs](https://github.com/derwells/crowNNs)** — Tree crown detection in aerial imagery. Replaced RetinaNet with FCOS in the DeepForest pipeline, benchmarked vs SOTA. Precision 0.64 vs DeepForest 0.66.
- **[blocked-floyd-warshall-gpu](https://github.com/derwells/blocked-floyd-warshall-gpu)** — CUDA implementation of Blocked Floyd-Warshall. GPU vs CPU timing at 100–10,000 nodes, 10 trials per size. Warp-aligned (BLOCKWIDTH=32).
- **[LPRNet](https://github.com/derwells/LPRNet)** — Keras implementation of LPRNet ([arxiv:1806.10447](https://arxiv.org/abs/1806.10447)) for license plate recognition, trained on CCPD-Base.
- **[multithreaded-fileserver](https://github.com/derwells/multithreaded-fileserver)** — Concurrent fileserver in C. Hand-over-hand locking on linked lists.

---

## PyMC ecosystem

At PyMC Labs building AI infrastructure for the team. Also contributing to [pymc-devs/pymc-examples](https://github.com/pymc-devs/pymc-examples): ZeroSumNormal notebook covering identifiability, sum-to-zero constraints, and categorical regression ([PR #844](https://github.com/pymc-devs/pymc-examples/pull/844)).

Not just an employee. Not just a user. Both.

---

## Why the graph looks quiet

All current work is private — building AI infrastructure for clients. The actual commit cadence is not quiet.

---

## On the horizon

Working on extracting some tools from the private monorepo as standalone public projects:

- `ralph` — frontier-based iterative analysis engine for CI (30-min cron, convergence detection, autonomous commits)
- Claude Code skills framework — 14 skills for disciplined AI agent behavior
- Custom MCP registry with scope-based credential gating
```

---

## 3. Pre-work: blocked-floyd-warshall-gpu README

**Priority**: HIGH — write this before finalizing pins. Flips this repo from KEEP (7/12) to SHOWCASE (10/12) and justifies it in the pin set.

**File to create**: `README.md` in the `derwells/blocked-floyd-warshall-gpu` repo.

**Note on benchmark numbers**: The code benchmarks at sizes 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10,000 nodes with 10 trials per size. The actual timing output requires running the CUDA binary on a GPU. Two options:
- (a) Run `./bfw` on a CUDA-capable machine and fill in the table
- (b) Publish with placeholder values and a note to run the benchmark yourself

If running the benchmark isn't feasible, option (b) is acceptable — the structural description of what was benchmarked (sizes, trials, GPU vs CPU) already tells the story even without specific millisecond values.

**Complete README content** (replace `[...]` fields with actual values if running the benchmark):

---

```markdown
# Blocked Floyd-Warshall (GPU)

GPU-accelerated all-pairs shortest paths (APSP) using the Blocked Floyd-Warshall algorithm, implemented in CUDA C.

## What this is

Floyd-Warshall computes shortest paths between every pair of vertices in a weighted graph in O(n³) time. The **blocked (tiled) variant** divides the distance matrix into blocks and processes them in three phases — enabling data reuse within shared memory and reducing global memory bandwidth pressure.

This implementation runs the blocked variant on GPU via CUDA. Block width is set to 32 (matching GPU warp size for aligned memory access). Benchmarked against a CPU reference implementation across graph sizes from 100 to 10,000 nodes.

## Benchmark results

10 trials per matrix size. Timing is mean wall-clock time in milliseconds.

| Nodes | CPU (ms) | GPU (ms) | Speedup |
|-------|----------|----------|---------|
| 100   | —        | —        | —       |
| 250   | —        | —        | —       |
| 500   | —        | —        | —       |
| 750   | —        | —        | —       |
| 1,000  | —       | —        | —       |
| 2,500  | —       | —        | —       |
| 5,000  | —       | —        | —       |
| 7,500  | —       | —        | —       |
| 10,000 | —       | —        | —       |

*(Run `./bfw` to reproduce — outputs timing per size to stdout)*

## Build & run

```bash
nvcc -O2 -o bfw main.cu data.cu
./bfw
```

Requires CUDA toolkit and an NVIDIA GPU.

## Files

- `main.cu` — driver, CPU reference implementation, benchmarking loop
- `data.cu` / `data.h` — graph generation (random dense weighted graphs)
```

---

**Forward ralph note**: Fill in the benchmark table by running the compiled binary on any CUDA-capable machine. The `—` placeholders communicate the intent even without numbers, but actual speedup numbers would make this significantly more compelling as a pin.

---

## 4. Pin List

Pin exactly these 6 repos, in this order. GitHub displays pins in order — earlier = more prominent.

| # | Repo | Verdict | Justification |
|---|------|---------|---------------|
| 1 | **crowNNs** | SHOWCASE | Strongest public repo. Results table vs SOTA is the clearest evidence of real ML rigor. Leads the ML/CV story. |
| 2 | **blocked-floyd-warshall-gpu** | SHOWCASE (after README) | Most technically differentiating public artifact. CUDA kernels at scale — proves the GPU depth is at the kernel level, not just framework calls. *Pin after README is written.* |
| 3 | **LPRNet** | KEEP | Reinforces GPU + ML cluster alongside crowNNs. arxiv paper link + training hardware specs signal applied ML credibility. |
| 4 | **multithreaded-fileserver** | KEEP | Only systems/C repo in the portfolio. Demonstrates that the ML work isn't isolated — there's computer science depth underneath. Hand-over-hand locking is non-trivial. |
| 5 | **halleys-comet** | KEEP | Adds scientific computing dimension. Supports the "numerical methods" thread that connects to PyMC work. |
| 6 | **pymc-examples** | KEEP | Surfaces the OSS contribution context. After description update ("Working fork — ZeroSumNormal notebook contributed to pymc-devs/pymc-examples (PR #844)"), this communicates PyMC ecosystem integration for any visitor who clicks. |

**Note on pymc-examples**: Normally, pinning forks is not recommended (visitors don't understand them without context). The description update makes this work — it clearly explains what the fork is for. If the description update isn't done first, don't pin this repo. Pin `lotka-volterra` as the 6th slot instead.

**Do not pin**: `derwells.github.io` — a utility repo occupies a pin slot better used for a technical artifact. `lotka-volterra` — weaker than the six listed above. `pymc-examples` (only if description update has not been applied).

---

## 5. Archive List

Archive all three immediately. This reduces visible repo count from 11 to 8, significantly improving signal-to-noise.

| Repo | Reason |
|------|--------|
| **moodle** | Pure reference clone of the Moodle LMS. Zero commits by derwells on any branch. Tells no story. Almost certainly cloned for university coursework reference. |
| **shalltear** | Fork of a generic Discord bot (2020). 7 original commits (one day, matplotlib plant stats graph) on a dead feature branch — too old, too small, abandoned. The current Discord-bot work (Decision Orchestrator) is categorically more sophisticated; keeping shalltear adds noise rather than history. |
| **wordhack** | CS11 (freshman-level) word-factory game. RST stub README that doesn't even describe the game. 6 years old. Anchors the profile to freshman-level work. |

**How to archive**: `gh repo archive derwells/{repo} --yes` — this makes the repo read-only and greyed out in the profile. It does NOT delete the repo. Can be unarchived via web UI.

---

## 6. Description Updates

New `description` string for every repo being kept. All descriptions are punchy, specific, and not generic.

| Repo | Current description | New description |
|------|---------------------|-----------------|
| crowNNs | *(none)* | `Tree crown detection in aerial RGB imagery — FCOS replacing RetinaNet, benchmarked vs DeepForest and lidR` |
| blocked-floyd-warshall-gpu | *(none)* | `GPU-accelerated Blocked Floyd-Warshall for all-pairs shortest paths — CUDA kernels benchmarked 100–10,000 nodes` |
| LPRNet | *(none)* | `Keras implementation of LPRNet (arxiv:1806.10447) for license plate recognition, trained on CCPD-Base` |
| multithreaded-fileserver | *(none)* | `Concurrent fileserver in C — hand-over-hand locking, reader/writer thread groups, autotest suite` |
| pymc-examples | `pymc-devs/pymc-examples` (upstream description) | `Working fork — ZeroSumNormal example notebook contributed to pymc-devs/pymc-examples (PR #844)` |
| halleys-comet | *(none)* | `Halley's comet orbital simulation using 4th-order Runge-Kutta ODE solver` |
| lotka-volterra | *(none)* | `Predator-prey dynamics via Regula-Falsi root-finding (alternative to Runge-Kutta)` |
| derwells.github.io | `Github Pages template for academic personal websites, forked from mmistakes/minimal-mistakes` | `Source for derwells.github.io — personal site built on Jekyll + Minimal Mistakes` |

---

## 7. Topic Tags

New `topics` array for every repo being kept. Currently zero repos have any topics — adding these significantly improves discoverability.

| Repo | Topics |
|------|--------|
| crowNNs | `computer-vision`, `object-detection`, `pytorch`, `remote-sensing`, `aerial-imagery` |
| blocked-floyd-warshall-gpu | `cuda`, `gpu`, `algorithms`, `high-performance-computing`, `parallel-computing` |
| LPRNet | `computer-vision`, `keras`, `license-plate-recognition`, `deep-learning` |
| multithreaded-fileserver | `c`, `concurrency`, `systems-programming`, `multithreading` |
| pymc-examples | `pymc`, `bayesian`, `probabilistic-programming`, `statistics` |
| halleys-comet | `numerical-methods`, `simulation`, `ode`, `scientific-computing`, `python` |
| lotka-volterra | `numerical-methods`, `scientific-computing`, `differential-equations`, `python` |
| derwells.github.io | `jekyll`, `github-pages`, `personal-website` |

---

## 8. derwells.github.io README Fix

The current README is the academicpages theme's own README — instructions for other people to fork the template. It makes the repo look like an unconfigured clone. Replace it entirely.

**File**: `README.md` in the `derwells/derwells.github.io` repo

**Complete new content** (2 lines — that's all this needs):

```markdown
Personal website at [derwells.github.io](https://derwells.github.io). Built with Jekyll + Minimal Mistakes.
```

**How**: Clone the repo, replace README.md, commit, push.

---

## 9. Future Public Repos (Optional — Not Required for This Spec)

These are items to flag for the profile owner. The forward ralph should not attempt to create these repos — they require extracting and sanitizing private monorepo content. Flagging them as options.

| Project | What it is | Why it's worth open-sourcing |
|---------|-----------|------------------------------|
| **ralph loop engine** | Frontier-based iterative analysis engine running in GitHub Actions CI (30-min cron, convergence detection, autonomous commits, GitHub issue creation on convergence) | Genuinely novel tool for LLM-driven structured analysis. Small, conceptually clean, would attract AI developer attention. Requires sanitizing company-specific workflow content. |
| **Claude Code skills framework** | 14 custom skills for disciplined Claude Code agent behavior (~2,975 lines of SKILL.md files). Meta-recursive (includes a skill for writing new skills). | Most immediately publishable hidden asset. Clean extraction path — each skill is a self-contained SKILL.md. Would be immediately useful to anyone using Claude Code seriously. |
| **Custom MCP registry** | Scope-based credential gating for MCP tool registries — `@tool` decorator, context injection, per-server/channel credential scoping | High credibility signal in the AI infrastructure community. Smaller audience than the above, but establishes the protocol-level work as concrete and extractable. |

---

## 10. Execution Script

Complete bash script using `gh` CLI. Run from any directory after `gh auth login`.

**Prerequisites**: `gh` CLI authenticated with `repo` scope. `git` installed.

```bash
#!/usr/bin/env bash
# GitHub profile update script for derwells
# Run: bash execute-profile-spec.sh
# Prerequisites: gh auth login (with repo scope), git

set -euo pipefail

echo ""
echo "=== PRE-FLIGHT CHECKS ==="
echo "Ensure you have completed pre-work before running:"
echo "  1. Written README.md for derwells/blocked-floyd-warshall-gpu (Section 3)"
echo "  2. Fixed README.md for derwells/derwells.github.io (Section 8)"
echo "  3. Created and pushed derwells/derwells profile README (Section 2)"
echo ""
read -p "Pre-work complete? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Complete pre-work first. See Sections 2, 3, and 8 of this spec."
  exit 1
fi

echo ""
echo "=== STEP 1: ARCHIVE NOISE REPOS ==="
# Warning: gh repo archive cannot be undone via CLI; use GitHub web UI to unarchive
gh repo archive derwells/moodle --yes
echo "Archived: moodle"
gh repo archive derwells/shalltear --yes
echo "Archived: shalltear"
gh repo archive derwells/wordhack --yes
echo "Archived: wordhack"

echo ""
echo "=== STEP 2: UPDATE DESCRIPTIONS ==="
gh repo edit derwells/crowNNs \
  --description "Tree crown detection in aerial RGB imagery — FCOS replacing RetinaNet, benchmarked vs DeepForest and lidR"
echo "Updated: crowNNs"

gh repo edit derwells/blocked-floyd-warshall-gpu \
  --description "GPU-accelerated Blocked Floyd-Warshall for all-pairs shortest paths — CUDA kernels benchmarked 100–10,000 nodes"
echo "Updated: blocked-floyd-warshall-gpu"

gh repo edit derwells/LPRNet \
  --description "Keras implementation of LPRNet (arxiv:1806.10447) for license plate recognition, trained on CCPD-Base"
echo "Updated: LPRNet"

gh repo edit derwells/multithreaded-fileserver \
  --description "Concurrent fileserver in C — hand-over-hand locking, reader/writer thread groups, autotest suite"
echo "Updated: multithreaded-fileserver"

gh repo edit derwells/pymc-examples \
  --description "Working fork — ZeroSumNormal example notebook contributed to pymc-devs/pymc-examples (PR #844)"
echo "Updated: pymc-examples"

gh repo edit derwells/halleys-comet \
  --description "Halley's comet orbital simulation using 4th-order Runge-Kutta ODE solver"
echo "Updated: halleys-comet"

gh repo edit derwells/lotka-volterra \
  --description "Predator-prey dynamics via Regula-Falsi root-finding (alternative to Runge-Kutta)"
echo "Updated: lotka-volterra"

gh repo edit derwells/derwells.github.io \
  --description "Source for derwells.github.io — personal site built on Jekyll + Minimal Mistakes"
echo "Updated: derwells.github.io"

echo ""
echo "=== STEP 3: ADD TOPIC TAGS ==="
# Note: --add-topic adds topics without removing existing ones (idempotent)
gh repo edit derwells/crowNNs \
  --add-topic computer-vision \
  --add-topic object-detection \
  --add-topic pytorch \
  --add-topic remote-sensing \
  --add-topic aerial-imagery
echo "Topics set: crowNNs"

gh repo edit derwells/blocked-floyd-warshall-gpu \
  --add-topic cuda \
  --add-topic gpu \
  --add-topic algorithms \
  --add-topic high-performance-computing \
  --add-topic parallel-computing
echo "Topics set: blocked-floyd-warshall-gpu"

gh repo edit derwells/LPRNet \
  --add-topic computer-vision \
  --add-topic keras \
  --add-topic license-plate-recognition \
  --add-topic deep-learning
echo "Topics set: LPRNet"

gh repo edit derwells/multithreaded-fileserver \
  --add-topic c \
  --add-topic concurrency \
  --add-topic systems-programming \
  --add-topic multithreading
echo "Topics set: multithreaded-fileserver"

gh repo edit derwells/pymc-examples \
  --add-topic pymc \
  --add-topic bayesian \
  --add-topic probabilistic-programming \
  --add-topic statistics
echo "Topics set: pymc-examples"

gh repo edit derwells/halleys-comet \
  --add-topic numerical-methods \
  --add-topic simulation \
  --add-topic ode \
  --add-topic scientific-computing \
  --add-topic python
echo "Topics set: halleys-comet"

gh repo edit derwells/lotka-volterra \
  --add-topic numerical-methods \
  --add-topic scientific-computing \
  --add-topic differential-equations \
  --add-topic python
echo "Topics set: lotka-volterra"

gh repo edit derwells/derwells.github.io \
  --add-topic jekyll \
  --add-topic github-pages \
  --add-topic personal-website
echo "Topics set: derwells.github.io"

echo ""
echo "=== STEP 4: UPDATE PROFILE BIO ==="
gh api -X PATCH /user \
  -f bio="AI agent infrastructure @ PyMC Labs & Nuts and Bolts AI | custom MCP, durable workflows, Bayesian ML | GPU when it counts"
echo "Bio updated."

echo ""
echo "=== STEP 5: CREATE PROFILE README REPO (if not exists) ==="
if ! gh repo view derwells/derwells --json name &>/dev/null 2>&1; then
  gh repo create derwells/derwells --public --description "GitHub profile README"
  echo "Created: derwells/derwells"
else
  echo "derwells/derwells already exists — skipping creation."
fi

echo ""
echo "=== STEP 6: PIN REPOS VIA GRAPHQL ==="
echo "Fetching node IDs..."

USER_ID=$(gh api graphql -f query='{ viewer { id } }' --jq '.data.viewer.id')

CROWNS_ID=$(gh api graphql \
  -f query='{ repository(owner: "derwells", name: "crowNNs") { id } }' \
  --jq '.data.repository.id')

BFW_ID=$(gh api graphql \
  -f query='{ repository(owner: "derwells", name: "blocked-floyd-warshall-gpu") { id } }' \
  --jq '.data.repository.id')

LPRNET_ID=$(gh api graphql \
  -f query='{ repository(owner: "derwells", name: "LPRNet") { id } }' \
  --jq '.data.repository.id')

FILESERVER_ID=$(gh api graphql \
  -f query='{ repository(owner: "derwells", name: "multithreaded-fileserver") { id } }' \
  --jq '.data.repository.id')

HALLEYS_ID=$(gh api graphql \
  -f query='{ repository(owner: "derwells", name: "halleys-comet") { id } }' \
  --jq '.data.repository.id')

PYMC_ID=$(gh api graphql \
  -f query='{ repository(owner: "derwells", name: "pymc-examples") { id } }' \
  --jq '.data.repository.id')

echo "Setting pinned repositories..."
gh api graphql -f query="
mutation {
  updatePinnedRepositories(input: {
    ownerId: \"$USER_ID\",
    repositoryIds: [
      \"$CROWNS_ID\",
      \"$BFW_ID\",
      \"$LPRNET_ID\",
      \"$FILESERVER_ID\",
      \"$HALLEYS_ID\",
      \"$PYMC_ID\"
    ]
  }) {
    owner {
      pinnedRepositories {
        nodes { name }
      }
    }
  }
}" --jq '.data.updatePinnedRepositories.owner.pinnedRepositories.nodes[].name'

echo ""
echo "=== DONE ==="
echo ""
echo "Verify at: https://github.com/derwells"
echo ""
echo "Manual check: visit the profile and confirm:"
echo "  - Bio shows: AI agent infrastructure @ PyMC Labs & Nuts and Bolts AI..."
echo "  - 6 pinned repos visible in correct order"
echo "  - moodle, shalltear, wordhack archived (greyed out if viewed via /repositories)"
echo "  - Profile README displays correctly"
```

---

## Appendix: Before/After Summary

| Element | Before | After |
|---------|--------|-------|
| Bio | *(empty)* | "AI agent infrastructure @ PyMC Labs & Nuts and Bolts AI \| custom MCP, durable workflows, Bayesian ML \| GPU when it counts" |
| Profile README | Does not exist | Full narrative: platform thesis, public work, PyMC ecosystem, why quiet, on the horizon |
| Pinned repos | None | 6: crowNNs, blocked-floyd-warshall-gpu, LPRNet, multithreaded-fileserver, halleys-comet, pymc-examples |
| Archived repos | None | 3: moodle, shalltear, wordhack |
| Repos with descriptions | 0/11 | 8/8 (kept repos) |
| Repos with topics | 0/11 | 8/8 (kept repos) |
| Visitor first impression | "Inactive student account" | "AI infrastructure builder working at two companies; deep ML and GPU background" |
| Key story told | Nothing | Two production systems, one architectural thesis; Python GPU→Bayesian ML→AI agent infra breadth; active despite quiet graph |
