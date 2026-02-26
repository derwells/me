# Repo README Scan — derwells

**Analysis Date**: 2026-02-25
**Source**: Raw GitHub content (public repos only, curl fallback due to no gh CLI auth in CI)

---

## Summary

8 original public repos scanned. Only 2 have READMEs worth keeping with minor edits (`crowNNs`, `multithreaded-fileserver`). 1 has no README at all (`blocked-floyd-warshall-gpu`). 2 have template/boilerplate READMEs that actively harm the profile (`derwells.github.io`). The rest are minimal but serviceable. The most technically impressive public repo — CUDA GPU parallel algorithms — has zero documentation.

---

## README Assessment Per Repo

### 1. `crowNNs` — Grade: B+

**What it does**: Tree Crown Detection in Airborne RGB imagery. Replaced RetinaNet with FCOS inside the DeepForest library. Benchmarked against SOTA.

**README quality**: The best README in the public profile. Has:
- Concrete benchmark results table (Precision/Recall vs. DeepForest SOTA vs. lidR 2016)
- Training infrastructure noted (NVIDIA T4 on GCP)
- Getting Started, Training, Evaluation sections
- Clear, concise

**What's missing**: No images, no example predictions, no visual of what "tree crown detection" looks like.

**Assessment**: Usable as-is. Could be elevated with one example image.

**Description**: "Tree Crown Detection in Airborne RGB imagery" — decent, keep with minor improvement.

---

### 2. `multithreaded-fileserver` — Grade: B

**What it does**: Concurrent file server in C implementing hand-over-hand locking. Worker threads grouped by target filepath — threads in the same group run in order, threads in different groups run concurrently.

**README quality**: Solid. Has:
- Build instructions (gcc with pthread)
- Command documentation (write/read/empty)
- Clear explanation of the synchronization design (hand-over-hand locking strategy)
- Testing instructions with autotest.sh

**What's missing**: No diagram of the concurrency model, no performance numbers.

**Assessment**: Good for a systems project. Communicates the interesting design choice clearly.

**Description**: "Multithreaded mock file server" — fine, but undersells it. Should mention hand-over-hand locking or concurrent file operations.

---

### 3. `LPRNet` — Grade: C+

**What it does**: Keras implementation of [LPRNet](https://arxiv.org/abs/1806.10447) (License Plate Recognition Network). Trained on CCPD-Base dataset on an NVIDIA GTX 1660 Super.

**README quality**: Minimal but honest:
- What it is (Keras, LPRNet, CCPD-Base)
- Self-aware disclaimer: "Mini-project for self-learning. Not suited for production use."
- References arxiv paper
- Points to training notebook

**What's missing**: Zero results (no accuracy numbers, no example outputs). Calling it a "mini-project" undersells whatever was actually built.

**Assessment**: Passable but misses an opportunity to show outcomes. A single example plate recognition output would make this significantly better.

**Description**: "Keras implementation of LPRNet: https://arxiv.org/abs/1806.10447" — the URL in the description is ugly. Should just be a clean sentence.

---

### 4. `blocked-floyd-warshall-gpu` — Grade: F (NO README)

**What it does**: CUDA implementation of blocked Floyd-Warshall all-pairs shortest path on GPU. Benchmarks against CPU baseline. Tests matrix sizes from 100 to 10,000. Block width: 32 (warp-aligned). Runs 10 test iterations per size. Has both CPU and GPU implementations for comparison.

**README quality**: **DOES NOT EXIST**. No description field either (the only repo with no description).

**What's missing**: Everything. The actual work is interesting (GPU parallel algorithms, systematic benchmarking across matrix sizes up to 10K×10K) but there's zero documentation.

**Assessment**: This is the biggest gap in the public profile. It's the only CUDA/GPU repo visible, it demonstrates real HPC/parallel computing skills, and it's completely invisible. A 30-line README with one benchmark table would transform this repo.

**Spec action**: Write README urgently. Content should include:
- What Floyd-Warshall does, why GPU parallelization matters
- The blocked approach explanation (why blocking? cache efficiency)
- Benchmark results table (CPU vs GPU at matrix sizes 100–10K)
- Build instructions

---

### 5. `halleys-comet` — Grade: C

**What it does**: Halley's comet orbit simulation using 4th-order Runge-Kutta. Three differential equations for each 3D axis. Plots estimated trajectory from 1986 onwards.

**README quality**: Serviceable:
- Explains the physics problem briefly
- Documentation link (Google Drive PDF)
- Installation instructions (numpy, matplotlib)
- Usage with default parameters listed

**What's missing**: The README doesn't show what the output looks like. No plots embedded. Documentation is on Google Drive (not in-repo).

**Assessment**: Adequate for a coursework-level project. The physics framing ("comet acceleration described using three differential equations") is more interesting than the README makes it sound.

**Description**: "Halley's comet plotter using fourth-order Runge-Kutta." — accurate, acceptable.

---

### 6. `lotka-volterra` — Grade: C

**What it does**: Lotka-Volterra predator-prey dynamics solved via Regula-Falsi root finding instead of the typical Runge-Kutta numerical integration. The alternative approach is the interesting angle here.

**README quality**: Same template as halleys-comet (probably written at the same time):
- Documentation link (Google Drive PDF)
- Installation/usage instructions

**What's missing**: The interesting technical angle (why root-finding instead of ODE integration?) is not explained in the README at all.

**Assessment**: The README undersells the work. The method substitution (root-finding for ODE dynamics) is worth one sentence of explanation.

**Description**: "Lotka-Volterra predator-prey dynamics solved using root-finding" — acceptable.

---

### 7. `derwells.github.io` — Grade: D (Template Boilerplate)

**What it does**: Personal academic website hosted on GitHub Pages. Customized from the academicpages theme.

**README quality**: The README is the **verbatim academicpages template README**. It starts with the history of the theme ("forked from Minimal Mistakes Jekyll Theme, released under MIT License by Michael Rose") and instructions for *other people* to fork and use the template. It does not describe derwells's actual site at all.

**What's missing**: Custom description of the actual site. Current description on GitHub says "Github Pages template for academic personal websites, forked from the Minimal Mistakes Jekyll Theme" — which makes it look like he's hosting someone else's template, not his own site.

**Assessment**: Actively harmful. The README confuses visitors. The site is stale anyway (says "graduating student" according to profile-snapshot analysis). This repo should be archived or updated once the site is updated.

---

### 8. `wordhack` — Grade: D+

**What it does**: Terminal word-factory game (Boggle-style) with trie data structure for word validation. Built for CS11 coursework. Has Sphinx documentation, ASCII art, custom fonts. Reasonably well-structured Python codebase.

**README quality**: Has `README.rst` (not `.md`). Content: just installation (`pip install -r requirements.txt`) and run instructions (`python3 main.py`). That's it.

**What's missing**: What is the game? How do you play? What does it look like? The repo has a `resources/images/` folder with screenshots (`game_gui.png`, `letter_box_4x4.png`, `leaderboard.png`) but they're not referenced in the README.

**Assessment**: Old coursework (2020). Has screenshots in the repo but doesn't show them. Low priority to fix — repo is too old to be a showcase piece.

---

## Summary Table

| Repo | Grade | README Exists | Meaningful Content | Shows Results | Spec Action |
|------|-------|--------------|-------------------|---------------|-------------|
| `crowNNs` | B+ | yes | yes | yes (benchmark table) | Keep, minor improvement |
| `multithreaded-fileserver` | B | yes | yes | no | Keep, update description |
| `LPRNet` | C+ | yes | partial | no | Add results, clean description |
| `blocked-floyd-warshall-gpu` | **F** | **NO** | N/A | N/A | **Write README now** |
| `halleys-comet` | C | yes | partial | no | Acceptable as-is |
| `lotka-volterra` | C | yes | partial | no | Acceptable as-is |
| `derwells.github.io` | D | yes (template) | no | N/A | Archive or rewrite |
| `wordhack` | D+ | yes (RST) | minimal | no | Low priority; old |

---

## Key Findings

### 1. The Best README Is Also the Best Repo
`crowNNs` has the most complete README and is also the most interesting public project (ML benchmarking, custom architecture). This is not coincidence — it was worth documenting.

### 2. The Most Technically Impressive Repo Has Zero Documentation
`blocked-floyd-warshall-gpu` demonstrates GPU computing, parallel algorithms (blocked Floyd-Warshall), and systematic benchmarking. It's the only repo that would interest an HPC or systems engineer. It has no README and no description. This is a critical gap.

### 3. Two READMEs Actively Mislead Visitors
- `derwells.github.io` — README says "fork me" template instructions, not "this is my site"
- `wordhack` — README.rst says nothing about what the game is

### 4. Numeric Results Are Rare
Only `crowNNs` includes actual numbers (precision/recall). `LPRNet` should have results. `blocked-floyd-warshall-gpu` should have CPU vs GPU benchmark numbers. Numbers make technical READMEs credible.

### 5. Forked Repos Not Scanned
The 3 forked repos (`pymc-examples`, `moodle`, `shalltear`) were not assessed here — their READMEs are owned by upstream. They add no README value to the profile.

---

## Spec Implications

1. **URGENT: Write README for `blocked-floyd-warshall-gpu`** — This is the highest-priority README action. Include benchmark results, explanation of blocked approach, build instructions.

2. **Update `LPRNet` README** — Add accuracy metrics or example outputs. Remove "not suited for production use" self-deprecation (just state it's a learning project).

3. **Rewrite `derwells.github.io` README** — Or archive the repo. The current README actively confuses visitors into thinking they're looking at a template.

4. **Clean up `multithreaded-fileserver` description** — "Multithreaded mock file server" undersells the interesting design. Should mention concurrent access and locking strategy.

5. **`crowNNs` is pin-ready** — The README already supports pinning. Could add an example tree detection image to make it visually compelling.

6. **`wordhack` — low priority** — Old CS11 coursework. If kept, screenshots are in the repo, just not referenced. Not worth significant effort.

7. **No repos need description removed** — but several need descriptions added or improved.
