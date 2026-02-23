# Repo README Scan — derwells

**Analyzed**: 2026-02-23
**Source**: Live README fetches from GitHub (main + master branches)

---

## Summary

6 of 8 original repos have usable READMEs. The best (crowNNs, multithreaded-fileserver) are clear and substantive. The worst (derwells.github.io) is actively misleading — it's the theme's template README, not a personal site README. Two repos have no README at all: `blocked-floyd-warshall-gpu` (high-priority gap, impressive GPU work) and `wordhack` (only has a `.rst` install stub).

---

## Per-Repo Assessment

### 1. derwells.github.io
- **README exists**: Yes (master branch)
- **Quality**: **Terrible — wrong README**
- **Content**: Literally the academicpages theme's README. Instructions for *other people* to fork the template. Talks about "forked from mmistakes/minimal-mistakes" and has a changelog for the theme.
- **Problem**: This makes the repo look like a copy of a template, not a personal website. A visitor sees: "This person copied an academic website template and never set it up."
- **Reality**: This is the user's actual personal site, last updated Aug 2025. The repo description also says "Github Pages template for academic personal websites, forked from mmistakes/minimal-mistakes" — which is the template's description, not a personal one.
- **Action needed**: Replace README entirely. Strip template content. Write: "Personal website at [derwells.github.io](https://derwells.github.io). Built with Jekyll + Minimal Mistakes."
- **Priority**: MEDIUM (repo may be archived or redirected to the actual site)

---

### 2. LPRNet
- **README exists**: Yes (master branch)
- **Quality**: **Good — concise and honest**
- **Content**:
  - Links to the paper (arxiv 1806.10447)
  - States dataset (CCPD-Base)
  - Notes training hardware (GTX 1660 Super)
  - Honest "mini-project for self-learning, not suited for production"
  - Points to training notebook
- **What's missing**: No results / accuracy numbers. No visual output example.
- **Action needed**: Minor — optionally add accuracy metrics or a sample output image.
- **Priority**: LOW

---

### 3. crowNNs
- **README exists**: Yes (master branch)
- **Quality**: **Best README in the portfolio**
- **Content**:
  - Clear problem statement ("replacing RetinaNet with FCOS in DeepForest")
  - Benchmarked against SOTA: results table with precision/recall vs DeepForest vs lidR (2016)
  - Training setup (NVIDIA T4, GCP)
  - Getting Started, Training, Evaluation sections
- **Notable**: The results table is the killer detail — it shows this person ran a proper ML experiment, not just a tutorial. Precision 0.64 vs SOTA 0.66 means they got competitive results.
- **What's missing**: Nothing critical. Could add a sample image of tree crown detection.
- **Action needed**: None required. Minor optional improvement: sample visualization.
- **Priority**: LOW (already strong)

---

### 4. multithreaded-fileserver
- **README exists**: Yes (master branch)
- **Quality**: **Good — technical and complete**
- **Content**:
  - Build commands (gcc with pthread)
  - Explains 3 operations (write/read/empty)
  - Explains synchronization: hand-over-hand locking, worker thread groups
  - Testing section with autotest.sh
  - Usage example
- **What's missing**: Nothing significant. Context note (university systems project) would help frame it.
- **Action needed**: Minor — optionally add a one-line context note.
- **Priority**: LOW

---

### 5. blocked-floyd-warshall-gpu
- **README exists**: **NO — CRITICAL GAP**
- **Files in repo**: `.gitignore`, `data.cu`, `data.h`, `main.cu` (11,700 bytes)
- **What the code actually does** (from reading main.cu):
  - GPU-accelerated Blocked Floyd-Warshall for all-pairs shortest paths
  - Benchmarks against matrix sizes: 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10,000 nodes
  - Compares GPU vs CPU implementations
  - BLOCKWIDTH = 32 (CUDA warp-aligned)
  - 10 test runs per size for timing accuracy
  - Has both `floyd_warshall_cpu` and GPU kernel implementations
- **Why this matters**: This is real GPU/HPC work. All-pairs shortest paths is a classic algorithms problem; the blocked GPU variant is a research-grade optimization. Testing at 10,000 nodes shows serious scale testing.
- **Current state**: Completely undiscoverable. No description, no README. Someone visiting this repo sees 4 files and zero context.
- **Action needed**: Write README from scratch. Must include: what the algorithm does, why the blocked variant is faster, benchmark results table (GPU vs CPU by matrix size), build/run instructions.
- **Priority**: HIGH — this is the highest-leverage README gap in the portfolio

---

### 6. halleys-comet
- **README exists**: Yes (master branch)
- **Quality**: **Functional but thin**
- **Content**:
  - Explains the problem (comet trajectory using 3D Runge-Kutta ODE)
  - Links to Google Drive for documentation (not ideal — external dependency)
  - Install and run instructions
  - Default simulation parameters
- **What's missing**: An actual plot output would make this compelling. "Plots go to /plots directory" with no example is a missed opportunity.
- **Action needed**: Low priority. Optional: add a sample plot image.
- **Priority**: LOW

---

### 7. lotka-volterra
- **README exists**: Yes (master branch)
- **Quality**: **Functional but thin**
- **Content**:
  - Explains the methodological choice (Regula-Falsi vs standard Runge-Kutta)
  - Links to Google Drive docs (same external dependency issue)
  - Install + run instructions
  - Initial values
- **Notable**: The methodological framing ("normally done with Runge-Kutta; this uses Regula-Falsi root finding") is actually interesting — it signals intellectual curiosity. But it's buried.
- **Action needed**: Consider making the methodological choice more prominent in the description.
- **Priority**: LOW

---

### 8. wordhack
- **README exists**: Yes — but `.rst` format, minimal
- **Quality**: **Inadequate**
- **Content**: Install requirements, run command on Windows, run command on Linux. Nothing else.
- **What's missing**: What is the game? What does "Word-factory" mean? What does it look like? Why was CS11?
- **Reality**: This is a freshman Python game (word factory from CS11). The existing README.rst doesn't even describe the game — it's just install instructions.
- **Action needed**: Archive candidate. If kept, needs a complete README rewrite. But given it's a CS1 assignment, archiving is likely correct.
- **Priority**: LOW (because this repo will likely be archived)

---

## README Quality Matrix

| Repo | Has README | Quality | Priority Action |
|------|-----------|---------|----------------|
| crowNNs | Yes | **Excellent** | None required |
| multithreaded-fileserver | Yes | **Good** | Optional minor polish |
| LPRNet | Yes | **Good** | Optional: add accuracy numbers |
| halleys-comet | Yes | **Fair** | Optional: add sample plot |
| lotka-volterra | Yes | **Fair** | Optional: emphasize method choice |
| wordhack | Yes (.rst) | **Poor** | Archive likely; rewrite if kept |
| derwells.github.io | Yes | **Misleading** | REPLACE — strip template, write personal site README |
| blocked-floyd-warshall-gpu | **NO** | **Missing** | WRITE README — high-leverage gap |

---

## Repos Needing READMEs Written

### blocked-floyd-warshall-gpu — Suggested README structure:
```
# Blocked Floyd-Warshall (GPU)

GPU-accelerated implementation of the Blocked Floyd-Warshall algorithm for all-pairs shortest paths.

## What Is Blocked Floyd-Warshall?
...explain the algorithm and why blocking improves GPU parallelism...

## Benchmark Results
| Matrix Size | CPU (ms) | GPU (ms) | Speedup |
|-------------|----------|----------|---------|
| ...         | ...      | ...      | ...     |

## Build & Run
...
```
Note: The benchmark numbers are in the code (runs 10 tests per size) — they exist but aren't surfaced.

---

## Spec Implications

1. **blocked-floyd-warshall-gpu** needs a README before `signal-vs-noise` can correctly score it. Currently scores 0 on README quality despite being a strong technical piece. Writing the README would flip its score from ARCHIVE-range to KEEP/SHOWCASE-range.

2. **derwells.github.io** has an actively harmful README — it makes a personal site look like an unconfigured theme fork. Priority fix: replace it.

3. **crowNNs** is the strongest README asset. The results table is the only public evidence that this person does real ML experiments with benchmarking rigor. Protect and feature it.

4. **wordhack** has a README.rst (GitHub renders RST) but it communicates nothing substantive. Combined with the repo being a CS1 assignment, archive is the right call.

5. For the forward ralph, README improvements are the highest-leverage per-repo action — more impactful than just adding topic tags or updating descriptions.
