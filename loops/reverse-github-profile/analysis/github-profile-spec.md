# GitHub Profile Spec — derwells

**Generated**: 2026-02-26
**Source**: All 10 analysis files from the `github-profile-reverse` ralph loop
**Purpose**: Complete, actionable specification for transforming the GitHub profile from scattered student-era repos into a curated presence that tells the story of an AI infrastructure engineer.

---

## 1. Profile README

Complete markdown content for the `derwells/derwells` repo. Ready to commit as-is.

```markdown
**I build the reliability layer for AI agents in production.** Custom MCP servers, durable workflows, observability pipelines. Shipping across two orgs.

---

### What I'm building

**At [PyMC Labs](https://www.pymc-labs.com/)** — A Discord-based organizational OS. Custom MCP tool registry built at the protocol level (not FastMCP): scope-based credential gating, dynamic tool assembly, crash-resilient session persistence across three storage layers. 36K LOC Python. Claude Agent SDK + Supabase + Langfuse + Fly.io.

**At Nuts & Bolts AI** — Influencer marketing platform with AI-personalized email campaigns. Temporal.io for durable campaign workflows, Claude Agent SDK for per-creator email drafting. 13K LOC, FastAPI + Next.js.

**On my own** — An iterative analysis engine that runs autonomously on GitHub Actions CI. Wave-based frontiers, convergence detection, failure handling. This profile was assembled by one.

### Selected work

- **[crowNNs](https://github.com/derwells/crowNNs)** — Tree crown detection in airborne RGB. Replaced RetinaNet with FCOS inside DeepForest, benchmarked on NVIDIA T4.
- **[multithreaded-fileserver](https://github.com/derwells/multithreaded-fileserver)** — Concurrent file server in C with hand-over-hand locking and per-filepath thread groups.
- **[blocked-floyd-warshall-gpu](https://github.com/derwells/blocked-floyd-warshall-gpu)** — All-pairs shortest path on GPU (CUDA). Blocked decomposition with shared memory, benchmarked to 10K×10K.
- **[OOM postmortem](https://gist.github.com/derwells/aeeb264030016517b23871ce85e38ff8)** — Production crash analysis: Claude SDK subprocess trees hitting Fly.io memory limits.
- **[PyMC contribution](https://github.com/pymc-devs/pymc-examples/pull/844)** — ZeroSumNormal example notebook for the PyMC probabilistic programming library.

### Background

Before AI infrastructure: [BFT consensus protocols with BLS threshold signatures in Go](https://github.com/BHS-GQ/quorum-hotstuff), GPU parallel algorithms in CUDA, concurrent systems in C. The systems depth is why the AI infra work holds up.

Most of my work lives in private org repos. Public repos here are the foundations.
```

### README Design Rationale

- **Hook**: One bold sentence that states the identity. "Reliability layer for AI agents" is specific, differentiating, and provable. No greeting — the name is already on the profile.
- **What I'm building**: Two production systems named with org, tech stack, and LOC. Not "some private work I can't show" — concrete descriptions with real numbers. The ralph loops mention ends with the meta-hook ("This profile was assembled by one").
- **Selected work**: 5 items mixing pinned repos (3), a gist (1), and an open PR (1). The OOM postmortem proves production systems experience. The PyMC PR is the only public professional trace.
- **Background**: Brief — one sentence linking to BHS-GQ. "Systems depth is why the AI infra work holds up" connects the past to the present. Final line addresses the sparse contribution graph.
- **What's NOT here**: No badges, no stats widgets, no visitor counter, no emoji section headers, no "how to reach me" block. Clean, text-forward, engineer-to-engineer.

---

## 2. Pin List

6 repos pinned in this order (left to right on the profile):

| Slot | Repo | Owner | Node ID | Justification |
|------|------|-------|---------|---------------|
| 1 | `crowNNs` | derwells | `R_kgDOHStcpg` | Best ML/CV project. Real benchmark table, GPU training on GCP. SHOWCASE (9/12). |
| 2 | `multithreaded-fileserver` | derwells | `R_kgDOGu8w5g` | Systems programming in C. Hand-over-hand locking is a distinctive design. SHOWCASE (8/12). |
| 3 | `blocked-floyd-warshall-gpu` | derwells | `R_kgDOIsB-Rw` | Only public CUDA repo. GPU parallel algorithms are rare on profiles. SHOWCASE (10/12 after README). |
| 4 | `LPRNet` | derwells | `R_kgDOG1jB1w` | ML breadth. License plate recognition shows applied CV work. KEEP (5/12). |
| 5 | `quorum-hotstuff` | BHS-GQ | `R_kgDOIpvHsg` | BFT consensus in Go with BLS threshold signatures. Distributed systems credibility. Currently pinned — keep it. |
| 6 | `halleys-comet` | derwells | `MDEwOlJlcG9zaXRvcnkzNDgzNzE0MTI=` | Numerical methods. Weakest slot but name is memorable, has 1 star. |

**Unpinned** (removing from current pins):
- `emnet` (BHS-GQ, node ID `R_kgDOJZE5ZQ`) — Caliper benchmarking network, less impressive than quorum-hotstuff. One BHS-GQ pin is enough.

**Why this order**: Slots 1-3 are the three SHOWCASE repos spanning ML → systems → GPU. Slot 4 adds ML breadth. Slot 5 adds distributed systems depth (Go, BFT, crypto). Slot 6 fills the final slot with something memorable. The arc reads: "ML researcher + systems programmer + GPU engineer + distributed systems" — the complete foundation for the AI infrastructure identity.

---

## 3. Archive List

4 repos to archive (hidden from profile, not deleted):

| Repo | Node ID | Reason |
|------|---------|--------|
| `derwells.github.io` | `R_kgDOHtDqIA` | Stale personal site says "graduating student." Template README confuses visitors. Actively harmful to the narrative. |
| `wordhack` | `MDEwOlJlcG9zaXRvcnkyMjUwOTI4NDQ=` | 6-year-old CS11 coursework word game. Zero connection to current identity. |
| `moodle` | `R_kgDOHvFfYg` | Empty PHP fork of Moodle LMS. Zero original commits. Pure noise. |
| `shalltear` | `MDEwOlJlcG9zaXRvcnkyNjI5NzU2MDM=` | Empty Discord bot fork. 5.5 years abandoned. Zero commits. |

**Result**: Profile goes from 11 public repos to 7. Signal-to-noise ratio improves dramatically.

---

## 4. Description Updates

New `description` strings for every repo that remains visible:

| Repo | Current Description | New Description |
|------|-------------------|-----------------|
| `crowNNs` | "Tree Crown Detection in Airborne RGB imagery" | `Tree crown detection in airborne RGB — FCOS vs. RetinaNet, benchmarked on GPU` |
| `multithreaded-fileserver` | "Multithreaded mock file server" | `Concurrent file server in C with hand-over-hand locking and per-filepath thread groups` |
| `blocked-floyd-warshall-gpu` | *(none)* | `Blocked Floyd-Warshall APSP on GPU (CUDA) — benchmarked from 100 to 10K-vertex graphs` |
| `LPRNet` | "Keras implementation of LPRNet: https://arxiv.org/abs/1806.10447" | `Keras implementation of LPRNet for license plate recognition, trained on CCPD-Base` |
| `halleys-comet` | "Halley's comet plotter using fourth-order Runge-Kutta." | `Halley's comet orbit simulation using 4th-order Runge-Kutta` |
| `lotka-volterra` | "Lotka-Volterra predator-prey dynamics solved using root-finding methods." | `Lotka-Volterra predator-prey model solved via Regula-Falsi root-finding` |
| `pymc-examples` | *(upstream, unchanged)* | *(no change — fork inherits upstream description)* |

**Rationale**: Remove URLs from descriptions (LPRNet), surface the interesting design choice (multithreaded-fileserver), add descriptions where missing (blocked-floyd-warshall-gpu). Keep descriptions punchy — one line, no periods at end.

---

## 5. Topic Tags

New `topics` arrays for every kept repo. Currently ALL repos have zero topics.

| Repo | Topics |
|------|--------|
| `crowNNs` | `computer-vision`, `object-detection`, `deep-learning`, `pytorch`, `remote-sensing` |
| `multithreaded-fileserver` | `c`, `concurrency`, `systems-programming`, `multithreading`, `file-server` |
| `blocked-floyd-warshall-gpu` | `cuda`, `gpu`, `parallel-computing`, `algorithms`, `high-performance-computing` |
| `LPRNet` | `deep-learning`, `ocr`, `license-plate-recognition`, `keras`, `computer-vision` |
| `halleys-comet` | `numerical-methods`, `simulation`, `runge-kutta`, `astronomy`, `python` |
| `lotka-volterra` | `numerical-methods`, `simulation`, `predator-prey`, `python`, `scientific-computing` |
| `pymc-examples` | `pymc`, `bayesian-statistics`, `probabilistic-programming`, `jupyter` |

**Total**: 7 repos × ~5 topics = 35 topic assignments. From zero to meaningful discoverability.

---

## 6. Bio Update

| Field | Current | New |
|-------|---------|-----|
| Bio | "Engineer, sometimes Product. Really into LLMs right now!" | `AI infrastructure engineer. I build the reliability layer for AI agents in production.` |
| Company | *(empty)* | *(leave empty — naming both orgs is awkward)* |
| Blog | *(empty)* | *(leave empty — derwells.github.io is stale; update this field when a non-stale site exists)* |
| Location | Philippines | *(keep)* |

**Bio length**: 87 characters (GitHub limit: 160). Leaves room if needed.

**Why this bio**: Replaces vague hobbyist framing ("Really into LLMs right now!") with a concrete identity statement. "Reliability layer" is distinctive — most engineers in the LLM space are building applications, not infrastructure. "In production" signals real deployed systems, not side projects.

---

## 7. blocked-floyd-warshall-gpu README

This repo currently has NO README and NO description. Writing this README is the single highest-leverage action — it transforms a 7/12 KEEP repo into a 10/12 SHOWCASE repo.

Complete README content for `derwells/blocked-floyd-warshall-gpu/README.md`:

```markdown
# Blocked Floyd-Warshall on GPU

GPU-accelerated all-pairs shortest path (APSP) using blocked Floyd-Warshall with CUDA shared memory.

## What this is

Three implementations of the Floyd-Warshall algorithm for computing shortest paths between all vertex pairs, benchmarked against each other:

1. **CPU baseline** — Standard O(n³) triple-nested loop
2. **Naive GPU** — Direct CUDA port using global memory
3. **Blocked GPU** — Three-phase blocked decomposition using shared memory for cache efficiency

The blocked approach tiles the adjacency matrix into 32×32 blocks (warp-aligned) and processes them in three phases per iteration:

- **Phase 1**: Self-dependent diagonal block (1 thread block)
- **Phase 2**: Blocks in the same row/column as the pivot (n thread blocks)
- **Phase 3**: All remaining blocks (n×n grid, fully parallel)

Each phase loads tiles into `__shared__` memory, avoiding repeated global memory accesses.

## Benchmark

Tests run 10 iterations per matrix size on random integer adjacency matrices:

| Matrix Size | CPU | Naive GPU | Blocked GPU |
|-------------|:---:|:---------:|:-----------:|
| 100×100     | ✓   | ✓         | ✓           |
| 250×250     | ✓   | ✓         | ✓           |
| 500×500     | ✓   | ✓         | ✓           |
| 750×750     | ✓   | ✓         | ✓           |
| 1000×1000   | ✓   | ✓         | ✓           |
| 2500×2500   | —   | ✓         | ✓           |
| 5000×5000   | —   | ✓         | ✓           |
| 7500×7500   | —   | ✓         | ✓           |
| 10000×10000 | —   | ✓         | ✓           |

CPU tests cap at n=1000 (O(n³) becomes impractical beyond that). GPU implementations scale to 10K vertices.

Timing results are written to `record.csv` with columns: `id, size, kernel, exec_time`.

## Build & Run

Requires NVIDIA GPU and CUDA toolkit.

```bash
nvcc main.cu data.cu -o fw
./fw
```

## Configuration

- **Block width**: 32 (one CUDA warp). Compile-time constant `BLOCKWIDTH` in `main.cu`.
- **Test iterations**: 10 per size. Constant `NUMTESTS`.
- **Correctness checks**: Disabled by default. Set `DO_CHECKS` to `true` to verify GPU output against CPU baseline.
```

---

## 8. Execution Script

Bash script using `gh` CLI that executes all changes. Run section by section or all at once.

```bash
#!/usr/bin/env bash
# ============================================================
# GitHub Profile Overhaul — derwells
# Generated by: ralph loop (github-profile-reverse)
# Date: 2026-02-26
#
# Usage:
#   chmod +x execute-profile-overhaul.sh
#   ./execute-profile-overhaul.sh
#
# Prerequisites:
#   - gh CLI authenticated (gh auth status)
#   - git configured for push access
# ============================================================

set -euo pipefail

echo "========================================="
echo "GitHub Profile Overhaul — derwells"
echo "========================================="

# ----------------------------------------------------------
# Step 1: Update bio
# ----------------------------------------------------------
echo ""
echo "=== Step 1: Update bio ==="
gh api /user -X PATCH \
  -f bio="AI infrastructure engineer. I build the reliability layer for AI agents in production."
echo "  ✓ Bio updated"

# ----------------------------------------------------------
# Step 2: Archive noise repos
# ----------------------------------------------------------
echo ""
echo "=== Step 2: Archive noise repos ==="
for repo in derwells.github.io wordhack moodle shalltear; do
  echo "  Archiving $repo..."
  gh api "/repos/derwells/$repo" -X PATCH -f archived=true
done
echo "  ✓ 4 repos archived"

# ----------------------------------------------------------
# Step 3: Update repo descriptions
# ----------------------------------------------------------
echo ""
echo "=== Step 3: Update repo descriptions ==="

gh api /repos/derwells/crowNNs -X PATCH \
  -f description="Tree crown detection in airborne RGB — FCOS vs. RetinaNet, benchmarked on GPU"

gh api /repos/derwells/multithreaded-fileserver -X PATCH \
  -f description="Concurrent file server in C with hand-over-hand locking and per-filepath thread groups"

gh api /repos/derwells/blocked-floyd-warshall-gpu -X PATCH \
  -f description="Blocked Floyd-Warshall APSP on GPU (CUDA) — benchmarked from 100 to 10K-vertex graphs"

gh api /repos/derwells/LPRNet -X PATCH \
  -f description="Keras implementation of LPRNet for license plate recognition, trained on CCPD-Base"

gh api /repos/derwells/halleys-comet -X PATCH \
  -f description="Halley's comet orbit simulation using 4th-order Runge-Kutta"

gh api /repos/derwells/lotka-volterra -X PATCH \
  -f description="Lotka-Volterra predator-prey model solved via Regula-Falsi root-finding"

echo "  ✓ 6 descriptions updated"

# ----------------------------------------------------------
# Step 4: Update repo topics
# ----------------------------------------------------------
echo ""
echo "=== Step 4: Update repo topics ==="

echo '{"names":["computer-vision","object-detection","deep-learning","pytorch","remote-sensing"]}' | \
  gh api /repos/derwells/crowNNs/topics -X PUT --input -

echo '{"names":["c","concurrency","systems-programming","multithreading","file-server"]}' | \
  gh api /repos/derwells/multithreaded-fileserver/topics -X PUT --input -

echo '{"names":["cuda","gpu","parallel-computing","algorithms","high-performance-computing"]}' | \
  gh api /repos/derwells/blocked-floyd-warshall-gpu/topics -X PUT --input -

echo '{"names":["deep-learning","ocr","license-plate-recognition","keras","computer-vision"]}' | \
  gh api /repos/derwells/LPRNet/topics -X PUT --input -

echo '{"names":["numerical-methods","simulation","runge-kutta","astronomy","python"]}' | \
  gh api /repos/derwells/halleys-comet/topics -X PUT --input -

echo '{"names":["numerical-methods","simulation","predator-prey","python","scientific-computing"]}' | \
  gh api /repos/derwells/lotka-volterra/topics -X PUT --input -

echo '{"names":["pymc","bayesian-statistics","probabilistic-programming","jupyter"]}' | \
  gh api /repos/derwells/pymc-examples/topics -X PUT --input -

echo "  ✓ 7 repos tagged (35 topics total)"

# ----------------------------------------------------------
# Step 5: Add README to blocked-floyd-warshall-gpu
# ----------------------------------------------------------
echo ""
echo "=== Step 5: Add README to blocked-floyd-warshall-gpu ==="

BFW_README_CONTENT=$(base64 -w 0 <<'BFWEOF'
# Blocked Floyd-Warshall on GPU

GPU-accelerated all-pairs shortest path (APSP) using blocked Floyd-Warshall with CUDA shared memory.

## What this is

Three implementations of the Floyd-Warshall algorithm for computing shortest paths between all vertex pairs, benchmarked against each other:

1. **CPU baseline** — Standard O(n³) triple-nested loop
2. **Naive GPU** — Direct CUDA port using global memory
3. **Blocked GPU** — Three-phase blocked decomposition using shared memory for cache efficiency

The blocked approach tiles the adjacency matrix into 32×32 blocks (warp-aligned) and processes them in three phases per iteration:

- **Phase 1**: Self-dependent diagonal block (1 thread block)
- **Phase 2**: Blocks in the same row/column as the pivot (n thread blocks)
- **Phase 3**: All remaining blocks (n×n grid, fully parallel)

Each phase loads tiles into `__shared__` memory, avoiding repeated global memory accesses.

## Benchmark

Tests run 10 iterations per matrix size on random integer adjacency matrices:

| Matrix Size | CPU | Naive GPU | Blocked GPU |
|-------------|:---:|:---------:|:-----------:|
| 100×100     | ✓   | ✓         | ✓           |
| 250×250     | ✓   | ✓         | ✓           |
| 500×500     | ✓   | ✓         | ✓           |
| 750×750     | ✓   | ✓         | ✓           |
| 1000×1000   | ✓   | ✓         | ✓           |
| 2500×2500   | —   | ✓         | ✓           |
| 5000×5000   | —   | ✓         | ✓           |
| 7500×7500   | —   | ✓         | ✓           |
| 10000×10000 | —   | ✓         | ✓           |

CPU tests cap at n=1000 (O(n³) becomes impractical beyond that). GPU implementations scale to 10K vertices.

Timing results are written to `record.csv` with columns: `id, size, kernel, exec_time`.

## Build & Run

Requires NVIDIA GPU and CUDA toolkit.

```bash
nvcc main.cu data.cu -o fw
./fw
```

## Configuration

- **Block width**: 32 (one CUDA warp). Compile-time constant `BLOCKWIDTH` in `main.cu`.
- **Test iterations**: 10 per size. Constant `NUMTESTS`.
- **Correctness checks**: Disabled by default. Set `DO_CHECKS` to `true` to verify GPU output against CPU baseline.
BFWEOF
)

gh api /repos/derwells/blocked-floyd-warshall-gpu/contents/README.md -X PUT \
  -f message="Add README with benchmark description" \
  -f content="$BFW_README_CONTENT"

echo "  ✓ README pushed to blocked-floyd-warshall-gpu"

# ----------------------------------------------------------
# Step 6: Create profile README repo and push
# ----------------------------------------------------------
echo ""
echo "=== Step 6: Create profile README (derwells/derwells) ==="

# Create the repo (will fail gracefully if it already exists)
gh api /user/repos -X POST \
  -f name=derwells \
  -f description="Profile README" \
  -f public=true \
  -f auto_init=true \
  2>/dev/null || echo "  (repo may already exist, continuing...)"

# Wait for GitHub to initialize the repo
sleep 2

# Get the SHA of the auto-generated README (needed for update)
CURRENT_SHA=$(gh api /repos/derwells/derwells/contents/README.md --jq '.sha' 2>/dev/null || echo "")

PROFILE_README_CONTENT=$(base64 -w 0 <<'PROFILEEOF'
**I build the reliability layer for AI agents in production.** Custom MCP servers, durable workflows, observability pipelines. Shipping across two orgs.

---

### What I'm building

**At [PyMC Labs](https://www.pymc-labs.com/)** — A Discord-based organizational OS. Custom MCP tool registry built at the protocol level (not FastMCP): scope-based credential gating, dynamic tool assembly, crash-resilient session persistence across three storage layers. 36K LOC Python. Claude Agent SDK + Supabase + Langfuse + Fly.io.

**At Nuts & Bolts AI** — Influencer marketing platform with AI-personalized email campaigns. Temporal.io for durable campaign workflows, Claude Agent SDK for per-creator email drafting. 13K LOC, FastAPI + Next.js.

**On my own** — An iterative analysis engine that runs autonomously on GitHub Actions CI. Wave-based frontiers, convergence detection, failure handling. This profile was assembled by one.

### Selected work

- **[crowNNs](https://github.com/derwells/crowNNs)** — Tree crown detection in airborne RGB. Replaced RetinaNet with FCOS inside DeepForest, benchmarked on NVIDIA T4.
- **[multithreaded-fileserver](https://github.com/derwells/multithreaded-fileserver)** — Concurrent file server in C with hand-over-hand locking and per-filepath thread groups.
- **[blocked-floyd-warshall-gpu](https://github.com/derwells/blocked-floyd-warshall-gpu)** — All-pairs shortest path on GPU (CUDA). Blocked decomposition with shared memory, benchmarked to 10K×10K.
- **[OOM postmortem](https://gist.github.com/derwells/aeeb264030016517b23871ce85e38ff8)** — Production crash analysis: Claude SDK subprocess trees hitting Fly.io memory limits.
- **[PyMC contribution](https://github.com/pymc-devs/pymc-examples/pull/844)** — ZeroSumNormal example notebook for the PyMC probabilistic programming library.

### Background

Before AI infrastructure: [BFT consensus protocols with BLS threshold signatures in Go](https://github.com/BHS-GQ/quorum-hotstuff), GPU parallel algorithms in CUDA, concurrent systems in C. The systems depth is why the AI infra work holds up.

Most of my work lives in private org repos. Public repos here are the foundations.
PROFILEEOF
)

if [ -n "$CURRENT_SHA" ]; then
  # Update existing README
  gh api /repos/derwells/derwells/contents/README.md -X PUT \
    -f message="Add profile README" \
    -f content="$PROFILE_README_CONTENT" \
    -f sha="$CURRENT_SHA"
else
  # Create new README (repo was just created without auto_init, or README doesn't exist)
  gh api /repos/derwells/derwells/contents/README.md -X PUT \
    -f message="Add profile README" \
    -f content="$PROFILE_README_CONTENT"
fi

echo "  ✓ Profile README pushed to derwells/derwells"

# ----------------------------------------------------------
# Step 7: Pin repos
# ----------------------------------------------------------
echo ""
echo "=== Step 7: Pin repos ==="
echo ""
echo "  Attempting GraphQL pin mutations..."
echo "  (If these fail, pin manually at https://github.com/derwells)"
echo ""

# Unpin current items first
echo "  Unpinning current items..."
for NODE_ID in "R_kgDOG1jB1w" "R_kgDOGu8w5g" "R_kgDOIpvHsg" "R_kgDOJZE5ZQ"; do
  gh api graphql -f query="
    mutation {
      unpinItem(input: {itemId: \"$NODE_ID\"}) {
        clientMutationId
      }
    }
  " 2>/dev/null && echo "    Unpinned $NODE_ID" || echo "    Could not unpin $NODE_ID (may not be pinned)"
done

# Pin in desired order (order of addition = display order)
echo "  Pinning new items..."
PIN_ORDER=(
  "R_kgDOHStcpg"                              # 1. crowNNs
  "R_kgDOGu8w5g"                              # 2. multithreaded-fileserver
  "R_kgDOIsB-Rw"                              # 3. blocked-floyd-warshall-gpu
  "R_kgDOG1jB1w"                              # 4. LPRNet
  "R_kgDOIpvHsg"                              # 5. quorum-hotstuff (BHS-GQ)
  "MDEwOlJlcG9zaXRvcnkzNDgzNzE0MTI="         # 6. halleys-comet
)
PIN_NAMES=(
  "crowNNs"
  "multithreaded-fileserver"
  "blocked-floyd-warshall-gpu"
  "LPRNet"
  "quorum-hotstuff"
  "halleys-comet"
)

for i in "${!PIN_ORDER[@]}"; do
  gh api graphql -f query="
    mutation {
      pinItem(input: {itemId: \"${PIN_ORDER[$i]}\"}) {
        pinnedItem {
          ... on Repository { name }
        }
      }
    }
  " 2>/dev/null && echo "    Pinned ${PIN_NAMES[$i]}" || echo "    Could not pin ${PIN_NAMES[$i]} — pin manually"
done

# ----------------------------------------------------------
# Done
# ----------------------------------------------------------
echo ""
echo "========================================="
echo "Profile overhaul complete."
echo ""
echo "Manual verification:"
echo "  1. Visit https://github.com/derwells"
echo "  2. Check: Bio shows new text"
echo "  3. Check: Profile README renders correctly"
echo "  4. Check: 6 repos pinned in correct order"
echo "  5. Check: 4 repos archived (invisible from profile)"
echo "  6. Check: Descriptions updated on all repos"
echo "  7. Check: Topics visible on all repos"
echo "  8. Check: blocked-floyd-warshall-gpu has README"
echo ""
echo "If pinning failed via API, pin these 6 repos manually"
echo "at https://github.com/derwells (click 'Customize your pins'):"
echo "  1. crowNNs"
echo "  2. multithreaded-fileserver"
echo "  3. blocked-floyd-warshall-gpu"
echo "  4. LPRNet"
echo "  5. quorum-hotstuff (BHS-GQ org)"
echo "  6. halleys-comet"
echo "========================================="
```

---

## Summary of All Changes

### Before → After

| Aspect | Before | After |
|--------|--------|-------|
| Bio | "Engineer, sometimes Product. Really into LLMs right now!" | "AI infrastructure engineer. I build the reliability layer for AI agents in production." |
| Profile README | Does not exist | Full README describing production AI work, selected projects, background |
| Pinned repos | LPRNet, multithreaded-fileserver, quorum-hotstuff, emnet | crowNNs, multithreaded-fileserver, blocked-floyd-warshall-gpu, LPRNet, quorum-hotstuff, halleys-comet |
| Visible repos | 11 (4 noise) | 7 (all signal) |
| Topics | 0 across all repos | 35 across 7 repos |
| Descriptions | 3 missing/bad | All repos have punchy, accurate descriptions |
| blocked-floyd-warshall-gpu | No README, no description | Full README with benchmark table + description |
| First impression | "Junior ML hobbyist" | "AI infrastructure engineer who ships production systems" |

### What a stranger sees in 30 seconds (after)

1. **Bio**: "AI infrastructure engineer. I build the reliability layer for AI agents in production." — immediate identity signal
2. **Profile README**: Bold opener + two production systems with org names, tech stacks, and LOC + selected work with links + systems background
3. **Pins**: ML/CV → systems → GPU → ML breadth → distributed consensus → numerical methods. Coherent arc from foundations to AI infra.
4. **Repos**: 7 clean repos with topics and descriptions. No noise forks, no stale sites, no empty READMEs.
5. **OOM postmortem gist**: Linked from README — proves production systems experience with real debugging

### What remains invisible (acceptable)

- The private org repos (Cheerful, Decision Orchestrator) — described in README, can't be linked
- The monorepo and ralph loop engine — described in README, repo is private
- The detailed gists beyond the OOM postmortem — discoverable if someone clicks through
- The contribution graph — still sparse for public contributions; README addresses this

### Forward-ralph considerations (optional, not in this spec)

1. **Extract ralph loop engine as public repo** — would be the strongest "show don't tell" artifact. Demonstrates meta-engineering without relying on description alone.
2. **Update derwells.github.io** — currently archived. If a non-stale personal site is built later, un-archive and link from the blog profile field.
3. **Add example images to crowNNs README** — the repo has benchmark numbers but no visual of tree crown detection output. One image would elevate the README from B+ to A.
4. **Add accuracy metrics to LPRNet README** — currently no results shown. Even one accuracy number improves the story.
