# Signal vs. Noise — derwells

**Analyzed**: 2026-02-25
**Sources**: `analysis/repo-inventory.md`, `analysis/repo-readme-scan.md`, `analysis/repo-clustering.md`

---

## Summary

11 public repos scored across four axes (Originality, Activity, Story Value, README Quality). Result: **2 SHOWCASE**, **5 KEEP**, **4 ARCHIVE**. The noise is concentrated in 3 forks and 1 stale personal site. The real urgency is that `blocked-floyd-warshall-gpu` is a conditional SHOWCASE — it will score SHOWCASE the moment a README is written, but currently sits at KEEP due to zero documentation.

---

## Scoring Rubric

| Axis | 0 | 1 | 2 | 3 |
|------|---|---|---|---|
| **Originality** | Fork, no additions | Fork with contribution OR original but trivial | Original, meaningful work | Original, non-trivial, distinctive |
| **Activity** | Dead (3+ years) | Stale (1–3 years) | Recent (6–12 months) | Active (< 6 months) |
| **Story Value** | No connection to narrative | Weak signal | Supports narrative | Core to identity |
| **README Quality** | Missing or template | Minimal/stub | Solid | Excellent (results, visuals, clear) |

**Verdict thresholds**: SHOWCASE ≥ 8 | KEEP 4–7 | ARCHIVE ≤ 3

---

## Full Scorecard

### SHOWCASE

---

#### `crowNNs` — Score: **9/12**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 3 | Original research: replaced RetinaNet backbone with FCOS inside DeepForest, benchmarked against SOTA on real airborne imagery |
| Activity | 1 | Last updated 2023-07-27 (2.5 years ago) |
| Story Value | 3 | Best ML project in the public profile; real benchmark table, GPU training on GCP; directly supports the ML/AI narrative |
| README Quality | 2 | B+ grade: has precision/recall table, infrastructure notes, structured sections — the only public README with numeric results |
| **Total** | **9** | **SHOWCASE** |

**Verdict**: SHOWCASE. Pin immediately. Add one example output image to elevate README from B+ to A.

**Description update**: `"Tree crown detection in airborne RGB imagery — FCOS vs. RetinaNet, benchmarked on GPU"` (was: "Tree Crown Detection in Airborne RGB imagery")

**Topics**: `computer-vision`, `object-detection`, `deep-learning`, `pytorch`, `remote-sensing`

---

#### `multithreaded-fileserver` — Score: **8/12**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 3 | Original C implementation; non-trivial concurrent design (hand-over-hand locking, per-filepath thread groups) |
| Activity | 1 | Last updated 2023-07-07 (2.5 years ago) |
| Story Value | 2 | Strong systems fundamentals signal; validates the "built real things in C" layer of the tech stack |
| README Quality | 2 | B grade: build instructions, command docs, clear explanation of locking strategy, test instructions |
| **Total** | **8** | **SHOWCASE** |

**Verdict**: SHOWCASE. Pin. Update description to surface the interesting design choice.

**Description update**: `"Concurrent file server in C with hand-over-hand locking — per-filepath thread groups for parallel read/write"` (was: "Multithreaded mock file server")

**Topics**: `c`, `concurrency`, `systems-programming`, `multithreading`, `file-server`

---

### KEEP (with actions)

---

#### `blocked-floyd-warshall-gpu` — Score: **7/12** → **Conditional SHOWCASE**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 3 | Original CUDA implementation; blocked decomposition for cache efficiency on GPU; systematic benchmark across matrix sizes 100–10K |
| Activity | 1 | Last updated 2023-07-07 (2.5 years ago) |
| Story Value | 3 | ONLY public CUDA repo; GPU parallel algorithms is distinctive (few people have public CUDA repos); directly validates HPC depth |
| README Quality | 0 | **Does not exist** — no README, no description. Critical gap. |
| **Total** | **7 → 10** | **KEEP now / SHOWCASE after README** |

**Verdict**: KEEP. Would score 10/12 (SHOWCASE) with a README written. Writing the README is the single highest-leverage action in the entire profile. After README, pin immediately.

**Action required**: Write README with: blocked Floyd-Warshall explanation, why GPU/blocked decomposition, benchmark table (CPU vs GPU at matrix sizes 100, 500, 1000, 5000, 10000), build/run instructions.

**Description to add**: `"Blocked Floyd-Warshall all-pairs shortest path on GPU (CUDA) — benchmarked vs. CPU across 100–10K matrix sizes"`

**Topics**: `cuda`, `gpu`, `parallel-computing`, `algorithms`, `high-performance-computing`, `floyd-warshall`

---

#### `pymc-examples` (fork) — Score: **6/12**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 1 | Fork; added a ZeroSumNormal notebook to submit an open PR (only public trace of current PyMC Labs work) |
| Activity | 3 | Last updated 2026-02-13 — the most recently active public repo |
| Story Value | 2 | Only public evidence of current professional engagement; the PR in flight connects to the PyMC Labs client work |
| README quality | 0 | Upstream README only; no personal contribution to documentation |
| **Total** | **6** | **KEEP** |

**Verdict**: KEEP visible (don't archive). It's the only public bridge to current professional work. Pin consideration: yes, if no better Cluster 1 artifact is available. Once the PR merges, the story is: "contributed to the PyMC examples repo." Note: forks can't be pinned by default (GitHub limitation), but can be made visible via profile README link.

**Description note**: Upstream description is fine. Don't add personal description.

---

#### `LPRNet` — Score: **5/12**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 2 | Original Keras implementation of a published architecture (LPRNet) on a real dataset |
| Activity | 1 | Last updated 2024-06-30 (1.5 years ago) |
| Story Value | 1 | ML learning project; "not suited for production" self-deprecation buries the story; low differentiation |
| README Quality | 1 | Minimal but honest; references arxiv paper; missing any results |
| **Total** | **5** | **KEEP** |

**Verdict**: KEEP. Not a pin candidate. Update description and remove the ugly URL from the description field. Adding even one result metric (e.g., "achieved X% character accuracy on CCPD-Base") would improve this significantly.

**Description update**: `"Keras implementation of LPRNet for license plate recognition, trained on CCPD-Base"` (was: "Keras implementation of LPRNet: https://arxiv.org/abs/1806.10447")

**Topics**: `deep-learning`, `ocr`, `license-plate-recognition`, `keras`, `computer-vision`

---

#### `halleys-comet` — Score: **4/12**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 2 | Original numerical methods project (4th-order Runge-Kutta orbit simulation) |
| Activity | 0 | Last updated 2023-01-05 (3+ years ago) |
| Story Value | 1 | Interesting physics problem but indistinguishable from standard coursework; no connection to primary narrative |
| README Quality | 1 | Serviceable stub; missing visuals or output |
| **Total** | **4** | **KEEP (barely)** |

**Verdict**: KEEP. Do not pin. Low priority. Description is acceptable as-is.

**Topics to add**: `numerical-methods`, `simulation`, `runge-kutta`, `astronomy`, `python`

---

#### `lotka-volterra` — Score: **4/12**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 2 | Original implementation; the root-finding approach (Regula-Falsi instead of ODE integration) is genuinely interesting but unexplained |
| Activity | 0 | Last updated 2022-09-06 (3+ years ago) |
| Story Value | 1 | Interesting method but buried; no connection to primary narrative |
| README Quality | 1 | Same template as halleys-comet; doesn't explain the interesting angle |
| **Total** | **4** | **KEEP (barely)** |

**Verdict**: KEEP. Do not pin. Low priority. Description could be improved to mention the root-finding approach.

**Description update**: `"Lotka-Volterra predator-prey model using Regula-Falsi root-finding instead of ODE integration"` (was: "Lotka-Volterra predator-prey dynamics solved using root-finding")

**Topics to add**: `numerical-methods`, `simulation`, `predator-prey`, `python`, `scientific-computing`

---

### ARCHIVE

---

#### `derwells.github.io` — Score: **3/12**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 2 | Original personal site, but built from the academicpages template |
| Activity | 1 | Last updated 2025-08-02, but content says "graduating student" — stale and misleading |
| Story Value | 0 | Actively harmful: presents the user as a student, not an engineer. README is verbatim template boilerplate that confuses visitors. |
| README Quality | 0 | Verbatim academicpages template README — describes how to fork the template for others. Not about the actual site at all. |
| **Total** | **3** | **ARCHIVE** |

**Verdict**: ARCHIVE. The site is stale ("graduating student"), the README actively misleads visitors into thinking this is a template repo, and it adds zero signal to the engineering narrative. If a personal site is ever rebuilt/updated, un-archive at that time.

---

#### `wordhack` — Score: **3/12**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 2 | Original terminal word game (Boggle-style) with trie data structure; has Sphinx docs and screenshots |
| Activity | 0 | Last updated 2020-03-15 — 6 years ago |
| Story Value | 0 | 2020 intro CS coursework. No connection to current narrative. The trie data structure is basic CS; no differentiation. |
| README Quality | 1 | RST with install/run only; screenshots in repo but not referenced |
| **Total** | **3** | **ARCHIVE** |

**Verdict**: ARCHIVE. 6-year-old coursework adds noise to a profile trying to signal production AI engineering. The trie and word game angle has zero connection to the target narrative.

---

#### `moodle` (fork) — Score: **0/12**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 0 | Fork of the Moodle LMS (PHP). No personal commits beyond the fork. |
| Activity | 0 | Last updated 2022-07-28 (3.5 years ago) |
| Story Value | 0 | PHP LMS fork with zero contributions. No story. |
| README Quality | 0 | Upstream Moodle README only |
| **Total** | **0** | **ARCHIVE** |

**Verdict**: ARCHIVE immediately. Empty fork of a PHP LMS. Makes the profile look like a student who cloned course materials.

---

#### `shalltear` (fork) — Score: **0/12**

| Axis | Score | Reasoning |
|------|-------|-----------|
| Originality | 0 | Fork of unknown Python project. No personal commits. |
| Activity | 0 | Last updated 2020-05-11 — 5.5 years ago |
| Story Value | 0 | Unknown purpose, zero contributions, ancient |
| README Quality | 0 | Upstream README only |
| **Total** | **0** | **ARCHIVE** |

**Verdict**: ARCHIVE immediately. 5-year-old empty fork. Provides zero signal and reduces average repo quality.

---

## Summary Table

| Repo | Origin. | Activity | Story | README | **Total** | **Verdict** |
|------|---------|----------|-------|--------|-----------|-------------|
| `crowNNs` | 3 | 1 | 3 | 2 | **9** | **SHOWCASE** |
| `multithreaded-fileserver` | 3 | 1 | 2 | 2 | **8** | **SHOWCASE** |
| `blocked-floyd-warshall-gpu` | 3 | 1 | 3 | 0 | **7** | **KEEP → SHOWCASE*** |
| `pymc-examples` (fork) | 1 | 3 | 2 | 0 | **6** | **KEEP** |
| `LPRNet` | 2 | 1 | 1 | 1 | **5** | **KEEP** |
| `halleys-comet` | 2 | 0 | 1 | 1 | **4** | **KEEP** |
| `lotka-volterra` | 2 | 0 | 1 | 1 | **4** | **KEEP** |
| `derwells.github.io` | 2 | 1 | 0 | 0 | **3** | **ARCHIVE** |
| `wordhack` | 2 | 0 | 0 | 1 | **3** | **ARCHIVE** |
| `moodle` (fork) | 0 | 0 | 0 | 0 | **0** | **ARCHIVE** |
| `shalltear` (fork) | 0 | 0 | 0 | 0 | **0** | **ARCHIVE** |

*`blocked-floyd-warshall-gpu` rises to 10/12 (SHOWCASE) once README is written.

---

## Priority Action List

### Immediate (before anything else)
1. **Archive** `moodle`, `shalltear`, `derwells.github.io`, `wordhack` — pure noise removal
2. **Write README** for `blocked-floyd-warshall-gpu` — unlocks a SHOWCASE repo and makes the GPU/HPC cluster visible
3. **Pin** `crowNNs` and `multithreaded-fileserver` — both SHOWCASE-ready now

### High Priority
4. **Update description** for `multithreaded-fileserver` — current description undersells the design
5. **Update description** for `LPRNet` — remove URL from description, clean wording
6. **Add topics** to all KEEP and SHOWCASE repos — currently zero topics on everything

### Medium Priority
7. **Update description** for `lotka-volterra` — surface the root-finding angle
8. **Consider README addition** for `LPRNet` — one result metric would meaningfully improve it

### Low Priority
9. `halleys-comet` — acceptable as-is, just add topics
10. `pymc-examples` fork — keep visible; no description changes needed

---

## Spec Implications

1. **4 repos to archive** = the profile goes from 11 public repos to 7. Quality immediately improves.
2. **2 SHOWCASE repos ready now** (`crowNNs`, `multithreaded-fileserver`). 1 more pending README (`blocked-floyd-warshall-gpu`). That's a 3-pin foundation.
3. **Pin slots**: With 3 owned SHOWCASE repos and `pymc-examples` as the only current-work artifact, 3 slots remain for gists or profile README context (since the real AI systems work is all private org repos).
4. **Zero topics anywhere** is a single batch fix. All KEEP/SHOWCASE repos should get 5-6 relevant topics.
5. **The narrative gap** is stark: the 2 SHOWCASE repos (crowNNs, multithreaded-fileserver) are from 2023. The production AI work (2024–2026) has no public repo equivalent. The profile README is the only venue to describe this invisible work.
