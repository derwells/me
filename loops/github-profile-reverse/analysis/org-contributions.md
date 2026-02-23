# Org Contributions — derwells

**Analyzed**: 2026-02-23
**Sources**: GitHub API (orgs, events, PRs), monorepo project cards, starred repos

---

## Summary

No public org memberships visible. All professional org work (Nuts and Bolts AI, PyMC Labs) is in private repos. The only public trace of org activity is one open PR to `pymc-devs/pymc-examples` — a 1,872-line Jupyter notebook contribution to a 369-star repo. This single public contribution actually signals the depth of the PyMC Labs employment: derwells isn't just using PyMC, they're deployed at the company that builds it and contributing back to the open-source project.

---

## Data

### Public Org Memberships

```
GET /users/derwells/orgs → []
```

No public org memberships. All org work is in private orgs or hidden membership.

### Org Activity via Public Events

Only 3 public events on record (sparse event history):

| Event | Repo | Date |
|-------|------|------|
| PullRequestEvent | pymc-devs/pymc-examples | 2026-02-13 |
| CreateEvent | derwells/pymc-examples | 2026-02-13 |
| ForkEvent | pymc-devs/pymc-examples | 2026-02-13 |

One org appears: `pymc-devs`.

### pymc-devs/pymc-examples — Open PR #844

**Title**: "Add ZeroSumNormal example notebook"
**State**: Open (as of 2026-02-23)
**URL**: https://github.com/pymc-devs/pymc-examples/pull/844

**PR stats**:
- 1 file changed: `examples/generalized_linear_models/GLM-ZeroSumNormal.ipynb`
- +1,872 lines, 0 deletions
- Status: Added (new notebook)

**PR description excerpt**:
> This PR adds a comprehensive example notebook demonstrating PyMC's `ZeroSumNormal` distribution, which is ideal for categorical regression with sum-to-zero constraints. [...] This continues the work started in #210 by @drbenvincent and @aseyboldt. The original PR from 2021 used PyMC3 with a custom ZeroSumNormal implementation.

**Coverage in notebook**:
- Identifiability problems in categorical modeling
- Design matrix analysis (linear dependence in one-hot encoding)
- Contrast coding schemes: reference coding vs sum-to-zero coding
- ZeroSumNormal mathematics (covariance structure and properties)
- Worked example: comparing treatment group means with posterior analysis
- Advanced usage: multi-dimensional sum-to-zero constraints for factorial designs

**Repo context** (`pymc-devs/pymc-examples`):
- Stars: 369, Forks: 310
- Part of the PyMC project ecosystem — official examples library

### Professional Org Work (Private, via Monorepo Project Cards)

#### PyMC Labs (pymc-labs org — private)
- **Role**: Building Decision Orchestrator, the internal organizational OS
- **Tech**: 36,400 LOC, custom MCP tool registry, Discord-based workflow orchestration
- **Context**: PyMC Labs is the professional services arm of the PyMC project (the widely-used probabilistic programming library). Trust level: production infrastructure used by people who build statistical frameworks.
- **Org's GitHub**: `pymc-devs` has 39 public repos, 581 followers
- **Connection**: The PR to pymc-devs/pymc-examples + professional work at PyMC Labs = deep integration into this ecosystem

#### Nuts and Bolts AI (private org, no public GitHub trace)
- **Role**: Building Cheerful, full-stack influencer marketing AI platform
- **Tech**: 13,100 LOC, 5,570 commits, 3 apps (FastAPI backend, Next.js webapp, Claude Agent SDK context engine)
- **No GitHub org found**: No public `nutsandbolts-ai` or similar org visible. All work private.

### Starred Repos (Technical Signal)

Starred repos reveal genuine interests beyond the resume:

| Category | Repos |
|----------|-------|
| GPU/CUDA | ThunderKittens (tile primitives), GPU-Puzzles (learn CUDA), tinygrad |
| LLMs/AI | llama.cpp, micrograd, humanlayer, learning-ai |
| Game AI | PascalPons/connect4 solver, LightZero (reinforcement learning) |
| Python tooling | marimo (reactive notebooks), supabase-pydantic, pyaccelsx |
| Data infra | Apache Druid, pgdog (PostgreSQL pooler) |
| Modern C++ | Modern-CPP-Programming course |
| Blockchain | go-ethereum, Consensys/quorum (older interest) |
| Discord bots | rico-bot (Discord bot — aligns with Decision Orchestrator domain) |
| Backends | pocketbase, pockethost |

Strong signal: GPU/CUDA interests (ThunderKittens, GPU-Puzzles, tinygrad) align with `blocked-floyd-warshall-gpu` public repo (GPU-accelerated graph algorithms). This isn't just a class project — it reflects persistent interest in low-level compute.

---

## Patterns

1. **Invisible professional work**: All paid engineering work is private. The public profile shows none of it except one PR.
2. **PyMC ecosystem integration**: The PR is substantive (1,872 lines of pedagogical Bayesian content). Not a typo fix. Someone who works at PyMC Labs and also contributes mathematical/statistical content to the open-source examples library.
3. **Two separate employer orgs, both fully private**: Nuts and Bolts AI (no public GitHub trace at all), PyMC Labs (one public trace via PR).
4. **Starred repos confirm repo themes**: GPU/CUDA stars align with `blocked-floyd-warshall-gpu`. Discord bot star aligns with Decision Orchestrator. These aren't random follows.
5. **Statistical modeling depth**: Contributing a ZeroSumNormal notebook requires real Bayesian/probabilistic programming knowledge — not just using PyMC but understanding sum-to-zero constraints in categorical regression.

---

## Spec Implications

1. **Bio should name "PyMC Labs"** — It's a recognizable org in the ML/stats world (PyMC has significant mindshare). "Building AI infrastructure at PyMC Labs" is more credible than vague language.

2. **The pymc-examples PR is a link-able public artifact** — One of the very few public works. Could be referenced in the profile README under "recent work" or similar.

3. **ZeroSumNormal notebook signals Bayesian chops** — This is domain-specific statistical knowledge. Alongside the GPU work, it signals a technically unusual combo: low-level compute AND probabilistic modeling AND AI agent systems.

4. **No public org repos to pin** — Cannot pin org repos (all private). Profile pins must come entirely from personal repos. Confirms the README is the only place to describe org work.

5. **The Nuts and Bolts AI work is completely undiscoverable** — No event, no PR, no org. It only surfaces in the private monorepo. The profile README must carry this story explicitly.

6. **Starred GPU repos + blocked-floyd-warshall-gpu** — The GPU interest is real and persistent, not a class artifact. The profile README could mention "GPU kernel design" or similar as a genuine interest area, not just a historical note.
