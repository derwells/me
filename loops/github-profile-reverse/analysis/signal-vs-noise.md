# Signal vs. Noise — derwells

**Analyzed**: 2026-02-23
**Sources**: `analysis/repo-inventory.md`, `analysis/repo-readme-scan.md`, `analysis/repo-clustering.md`

---

## Summary

Of the 11 public repos, 1 is clear SHOWCASE, 7 are KEEP (with varying action requirements), and 3 are ARCHIVE. The real finding: the highest-leverage single action in the entire portfolio is writing a README for `blocked-floyd-warshall-gpu` — it scores KEEP at 7/12 today but would flip to SHOWCASE at 10/12 after a README. Three repos (moodle, shalltear, wordhack) are pure noise and should be archived immediately.

---

## Scoring System

Each repo scored on four dimensions:

| Dimension | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|
| **Originality** | Pure clone, no contribution | Fork with minor context OR trivial original | Original work with moderate effort | Original, research-grade, non-trivial |
| **Activity** | 4+ years old | 2-4 years old | 1-2 years old | Active within 1 year |
| **Story value** | Tells no story | Weak/thin narrative | Good story, one angle | Compelling, multi-dimensional |
| **README quality** | None | Stub/template/wrong | Functional, covers basics | Excellent — results, context, framing |

**Verdict thresholds**: 8+ = SHOWCASE | 4-7 = KEEP | 0-3 = ARCHIVE

---

## Full Scoring Table

| Repo | Originality | Activity | Story Value | README | Total | Verdict |
|------|-------------|----------|-------------|--------|-------|---------|
| crowNNs | 3 | 1 | 3 | 3 | **10** | **SHOWCASE** |
| blocked-floyd-warshall-gpu | 3 | 1 | 3 | 0 | **7** | **KEEP** → *SHOWCASE after README* |
| LPRNet | 2 | 1 | 2 | 2 | **7** | **KEEP** |
| multithreaded-fileserver | 2 | 1 | 2 | 2 | **7** | **KEEP** |
| pymc-examples (fork) | 1 | 2 | 2 | 1 | **6** | **KEEP** |
| halleys-comet | 2 | 0 | 1 | 2 | **5** | **KEEP** |
| lotka-volterra | 1 | 0 | 1 | 2 | **4** | **KEEP** |
| derwells.github.io | 1 | 2 | 1 | 0 | **4** | **KEEP** |
| wordhack | 1 | 0 | 0 | 0 | **1** | **ARCHIVE** |
| moodle (fork) | 0 | 0 | 0 | 1 | **1** | **ARCHIVE** |
| shalltear (fork) | 0 | 0 | 0 | 1 | **1** | **ARCHIVE** |

---

## Per-Repo Verdicts with Rationale

### SHOWCASE

#### crowNNs — Score: 10/12
**Verdict**: SHOWCASE — Pin, update description, add topics

- **Originality (3)**: Original research — replaced RetinaNet with FCOS in the DeepForest pipeline for tree crown detection in aerial imagery. Not a tutorial implementation; a real experimental comparison.
- **Activity (1)**: Last active July 2023 — stale but the work quality transcends recency.
- **Story value (3)**: The results table is the killer detail. Precision 0.64 vs SOTA 0.66 — competitive results on a real task, benchmarked against two baselines (DeepForest, lidR). This is the only public repo that shows "ML practitioner who runs real experiments," not just "person who followed a PyTorch tutorial."
- **README quality (3)**: Best README in the portfolio. Clear problem statement, results table, training setup (GCP T4), structured Getting Started / Training / Evaluation sections.

**Actions**: Pin this repo. Update description to: "Tree crown detection in aerial RGB imagery — FCOS replacing RetinaNet, benchmarked vs DeepForest and lidR." Add topics: `computer-vision`, `object-detection`, `pytorch`, `remote-sensing`, `aerial-imagery`.

---

### KEEP (descending score)

#### blocked-floyd-warshall-gpu — Score: 7/12 (potential: 10/12)
**Verdict**: KEEP today → SHOWCASE after README is written. **This is the highest-leverage action in the portfolio.**

- **Originality (3)**: Real CUDA kernel implementation. Blocked Floyd-Warshall is a research-grade optimization — requires understanding memory hierarchy, warp alignment (BLOCKWIDTH=32), and cache-oblivious tiling. Not a beginner CUDA project.
- **Activity (1)**: Last active July 2023 — same wave as crowNNs.
- **Story value (3)**: With framing, the story is excellent: "wrote CUDA kernels for all-pairs shortest paths, benchmarked GPU vs CPU at 10,000 nodes, 10 trials per size for statistical accuracy." Without framing (current state): zero story, invisible to any visitor.
- **README quality (0)**: No README, no description. Currently the 4 `.cu` files are all a visitor sees. Zero discoverability.

**Critical note**: This repo scores KEEP at 7 because README is 0. After writing a README with benchmark results (GPU vs CPU timing table, build instructions, algorithm explanation), the score becomes 10 — SHOWCASE. The forward ralph must write this README before doing anything else.

**Actions**: Write README (highest priority). Add description: "GPU-accelerated Blocked Floyd-Warshall for all-pairs shortest paths — CUDA kernels benchmarked 100–10,000 nodes." Add topics: `cuda`, `gpu`, `algorithms`, `high-performance-computing`, `parallel-computing`.

---

#### LPRNet — Score: 7/12
**Verdict**: KEEP — good supporting evidence of GPU ML experience

- **Originality (2)**: Keras implementation of a specific arxiv paper (1806.10447). Not a copy-paste tutorial — they trained it on a specific dataset (CCPD-Base) on their own hardware (GTX 1660 Super). More applied than pure research.
- **Activity (1)**: Last active June 2024 — the most recently updated ML repo.
- **Story value (2)**: Reinforces the ML/GPU cluster alongside crowNNs. Paper citation + dataset + hardware specs give it academic credibility. But it's a supporting actor, not the lead — crowNNs tells the better story.
- **README quality (2)**: Clear and honest. Missing: accuracy/performance numbers.

**Actions**: Keep as-is or add accuracy metrics (optional). Update description: "Keras implementation of LPRNet (arxiv:1806.10447) for license plate recognition, trained on CCPD-Base." Add topics: `computer-vision`, `keras`, `license-plate-recognition`, `deep-learning`.

---

#### multithreaded-fileserver — Score: 7/12
**Verdict**: KEEP — demonstrates systems depth, rare in a mostly-ML profile

- **Originality (2)**: Original C implementation, non-trivial synchronization. Hand-over-hand (lock coupling) locking is not a standard intro-systems-course technique — it requires thinking about ordered lock acquisition on a linked list.
- **Activity (1)**: Last active July 2023.
- **Story value (2)**: In a profile dominated by Python/ML, a C concurrent systems project adds breadth. Shows this person can reason about locks, threads, and shared state — which maps to the production systems work happening in the private monorepo.
- **README quality (2)**: Technical and complete. Build commands, operation explanations, testing section.

**Actions**: Keep as-is. Update description: "Concurrent fileserver in C — hand-over-hand locking, reader/writer thread groups, autotest suite." Add topics: `c`, `concurrency`, `systems-programming`, `multithreading`.

---

#### pymc-examples — Score: 6/12
**Verdict**: KEEP — surface the OSS contribution, not just the fork

- **Originality (1)**: Fork of the official PyMC examples repo. However, the fork is active (Feb 2026) and contains open PR #844 (+1,872 lines, ZeroSumNormal notebook) — real original work, just not merged yet.
- **Activity (2)**: Most recently touched repo in the portfolio (Feb 2026). Active signal.
- **Story value (2)**: The fork alone is meaningless. But the fork + active OSS PR to a major Bayesian ML library + employment at PyMC Labs = coherent narrative about deep ecosystem integration. The story value is contextual — it's only compelling when framed properly.
- **README quality (1)**: Upstream PyMC README — fine, but not personalized.

**Actions**: Update description to surface the contribution context: "Working fork for contributing to pymc-devs/pymc-examples — ZeroSumNormal notebook (PR #844)." Add topics: `pymc`, `bayesian`, `probabilistic-programming`, `statistics`.

---

#### halleys-comet — Score: 5/12
**Verdict**: KEEP (lower priority) — supporting evidence of numerical computing depth

- **Originality (2)**: Original numerical simulation with parameterized ODE system.
- **Activity (0)**: Jan 2023 — 3+ years old.
- **Story value (1)**: Interesting subject matter (orbital mechanics) but thin narrative. The README links to an external Google Drive doc (fragile dependency).
- **README quality (2)**: Functional — explains the math, has run instructions, parameterized.

**Actions**: Keep. Minor optional polish: embed a sample orbit plot image. Update description: "Halley's comet orbital simulation using 4th-order Runge-Kutta ODE solver." Add topics: `numerical-methods`, `simulation`, `ode`, `scientific-computing`, `python`.

---

#### lotka-volterra — Score: 4/12
**Verdict**: KEEP (lowest priority original) — barely earns its place via the methodology angle

- **Originality (1)**: Original simulation, but the Regula-Falsi choice is the only differentiating detail.
- **Activity (0)**: Sep 2022 — 3+ years old.
- **Story value (1)**: The methodological curiosity (why Regula-Falsi instead of Runge-Kutta?) is the only interesting angle. Currently buried. If foregrounded in the description, slightly more compelling.
- **README quality (2)**: Functional but links to external Google Drive docs.

**Actions**: Keep but deprioritize. Update description to lead with the methodology: "Predator-prey dynamics via Regula-Falsi root-finding (alternative to Runge-Kutta)." Add topics: `numerical-methods`, `scientific-computing`, `differential-equations`, `python`.

---

#### derwells.github.io — Score: 4/12
**Verdict**: KEEP — utility repo, expected to exist, but must fix the actively misleading README

- **Originality (1)**: Personal site built on a template (academicpages / Minimal Mistakes). The customization is personal, but the base is off-the-shelf.
- **Activity (2)**: Last updated Aug 2025 — the most recently active repo overall.
- **Story value (1)**: Personal site repos are expected and neutral. They don't add story; they just shouldn't subtract story. Currently they subtract (the template README makes it look like an unconfigured clone).
- **README quality (0)**: ACTIVELY MISLEADING. It's the academicpages theme's README — instructions for other people to fork the template. A visitor reads: "This person forked a template and never set it up."

**Actions**: Replace README entirely (2 lines is enough: "Personal website at [derwells.github.io](https://derwells.github.io). Built with Jekyll + Minimal Mistakes."). Update description: "Source for derwells.github.io — personal site built on Jekyll + Minimal Mistakes." Add topics: `jekyll`, `github-pages`, `personal-website`.

---

### ARCHIVE

#### wordhack — Score: 1/12
**Verdict**: ARCHIVE — CS1 assignment with no story value

- **Originality (1)**: Original code, but it's a word-factory game built for CS11 (a freshman-level course).
- **Activity (0)**: March 2020 — 6 years old.
- **Story value (0)**: "CS11 word game" tells the story of "this person was a first-year student." That's not the story we're trying to tell.
- **README quality (0)**: RST stub with only install/run instructions. Doesn't even describe what the game is.

**Reason to archive**: Occupies visible space without communicating anything positive. The CS11 label actively anchors the profile to freshman-level work.

---

#### moodle — Score: 1/12
**Verdict**: ARCHIVE — pure upstream clone, zero personal contribution

- **Originality (0)**: Exact clone of the Moodle LMS. No commits beyond the fork.
- **Activity (0)**: July 2022 — 3.5 years old, no activity since fork.
- **Story value (0)**: Tells no story. Why is Moodle forked? Unknown. No PR, no issue, no commit. Probably cloned for reference while doing university coursework.
- **README quality (1)**: Upstream Moodle README — not the user's work.

**Reason to archive**: Pure noise. A visitor sees a fork of a massive LMS with zero personal contribution and wonders why it's there.

---

#### shalltear — Score: 1/12
**Verdict**: ARCHIVE — generic Discord bot fork with no post-fork activity

- **Originality (0)**: Fork of a generic Discord bot. No personal commits visible.
- **Activity (0)**: May 2020 — 6 years old, no activity since fork.
- **Story value (0)**: "Forked a Discord bot in 2020 and never touched it" tells no story. Even if this was used as a template for personal bots, there's no evidence of that.
- **README quality (1)**: Upstream bot README.

**Note**: shalltear is referenced in the clustering analysis as potentially related to the current Discord-based Decision Orchestrator at PyMC Labs. This connection is speculative and not evidenced. The fork's 2020 vintage and the DO's current-year sophistication make any connection irrelevant. Archive.

---

## Verdict Summary

| Verdict | Count | Repos |
|---------|-------|-------|
| **SHOWCASE** | 1 | crowNNs |
| **SHOWCASE** (after README) | 1 | blocked-floyd-warshall-gpu |
| **KEEP** | 6 | LPRNet, multithreaded-fileserver, pymc-examples, halleys-comet, lotka-volterra, derwells.github.io |
| **ARCHIVE** | 3 | wordhack, moodle, shalltear |

Post-cleanup public profile: **8 repos** (1-2 SHOWCASE, 6 KEEP, 0 ARCHIVE). Significantly cleaner signal-to-noise ratio.

---

## Action Priority Order

For the forward ralph, execute in this order:

1. **Write README for blocked-floyd-warshall-gpu** (flips from KEEP to SHOWCASE — highest ROI)
2. **Archive moodle, shalltear, wordhack** (removes 3 noise repos)
3. **Fix derwells.github.io README** (stops actively lying to visitors)
4. **Update descriptions for all KEEP repos** (above, per-repo)
5. **Add topics to all repos** (above, per-repo) — zero effort, high discoverability
6. **Pin crowNNs + blocked-floyd-warshall-gpu** (after README is written) + 4 more to determine

---

## Patterns

1. **The three-score-zero repos all have one thing in common**: no original contribution beyond forking or trivial assignments. Originality is the dominant differentiator — even old repos with thin READMEs (halleys-comet, lotka-volterra) clear the KEEP bar because they represent original problem-solving.

2. **README quality is the most fixable dimension**: Two repos would jump verdict categories with README work alone (blocked-floyd-warshall-gpu: KEEP→SHOWCASE; derwells.github.io: neutral→actually-neutral instead of negative). This is the clearest ROI in the portfolio.

3. **Activity scores are uniformly low**: No public repo has been touched in the last year (except pymc-examples fork, touched Feb 2026). This makes sense — all current work is in private repos. The forward ralph cannot fix this without either making private work public or committing to public projects. This is a structural gap the profile README must address in prose.

4. **The pinnable SHOWCASE set is thin**: Only 1-2 repos clear the SHOWCASE bar on their own merits. The 6 pin slots available must be filled with the best KEEP repos. Clustering analysis suggests: crowNNs, blocked-floyd-warshall-gpu (after README), LPRNet, multithreaded-fileserver, pymc-examples, halleys-comet as the pin set — but `fork-audit` and `narrative-gaps` may change this.

---

## Spec Implications

1. **Archive immediately**: moodle, shalltear, wordhack. No information lost. Profile signal-to-noise improves immediately.

2. **Write blocked-floyd-warshall-gpu README before finalizing pin list**: The pin decision depends on whether this repo qualifies as SHOWCASE. Without a README it can't be pinned with confidence; after a README it's the second-strongest technical story after crowNNs.

3. **Update all descriptions and topics for KEEP repos**: None have topics; most have stale or weak descriptions. This is mechanical work the forward ralph can execute with `gh repo edit`.

4. **derwells.github.io**: Fix README or consider not pinning this at all. A personal site repo occupies a pin slot better used for a technical project.

5. **The profile needs 6 pins; current SHOWCASE set is 2 (after README)**: The remaining 4 pins must come from the KEEP pool. Recommended: LPRNet, multithreaded-fileserver, pymc-examples, halleys-comet — in that order.
