# Personal Monorepo

Personal knowledge base and ralph loop system. Project context for things I'm working on, and a loop engine for frontier-driven iterative analysis.

## Structure

```
├── CLAUDE.md              # This file
├── projects/              # Context cards for things I'm working on
│   ├── nutsandbolts--cheerful.md
│   └── pymc--decision-orchestrator.md
└── loops/                 # Ralph loop system
    ├── _template/         # Copy this to start a new loop
    └── _registry.yaml     # Loop status tracker
```

Other directories (`docs/plans/`, `data/`, `research/`) are created when needed — not pre-scaffolded.

## Projects

Lightweight context cards in `projects/`. Naming: `company--project.md`. Read these for tech stack, features, scale, and architectural context when working on related loops or tasks.

Current projects:
- [[nutsandbolts--cheerful]] — email automation platform for influencer marketing (Nuts and Bolts AI)
- [[pymc--decision-orchestrator]] — Discord-based organizational OS (PyMC Labs)

Both share architectural DNA: Claude Agent SDK, custom MCP servers, Supabase, Langfuse, Composio.

## Ralph Loops

### What They Are

A ralph loop is a frontier-driven iterative analysis pattern. Each iteration does ONE unit of work, then exits. State lives on the filesystem. The loop converges when all aspects are analyzed and the output passes self-review.

### Reverse Loops (analysis → spec)

The only loop type currently templated. Takes something (a video, a codebase, a legal document) and produces a structured output (a spec, a report, a dataset).

### How They Work

1. **Frontier** (`frontier/aspects.md`) — wave-based checklist of aspects to analyze. Waves have dependencies (Wave 2 depends on Wave 1 data).
2. **One iteration = one aspect** — read frontier, pick first unchecked item, analyze it, write findings to `analysis/`, update frontier, commit, exit.
3. **Emergent discovery** — analyzing one aspect may reveal new ones. Add them to the frontier.
4. **Convergence** — all aspects checked + output passes self-review → write `status/converged.txt`.

### Running a Loop

**Claude Code web (primary):** Open session, point at the loop's `PROMPT.md`, say "run one iteration." You are the outer loop.

**Claude Code CLI:** `cd loops/<name> && ./loop.sh [max_iterations]` — bash runner handles iteration, timeouts (1800s), failure detection (3 consecutive = stop), and convergence checks.

### Starting a New Loop

```bash
cp -r loops/_template loops/<name>
cd loops/<name>
mv PROMPT.md.example PROMPT.md        # Fill in {{placeholders}}
mv frontier/aspects.md.example frontier/aspects.md  # Seed your waves
```

Add entry to `loops/_registry.yaml`. Run it.

### Loop Directory Structure (per loop)

```
loops/<name>/
├── PROMPT.md              # Loop instructions (Claude reads this each iteration)
├── loop.sh                # Bash runner (or symlink to _template/loop.sh)
├── frontier/
│   ├── aspects.md         # Wave-based checklist (the frontier)
│   └── analysis-log.md    # Iteration history
├── analysis/              # One .md per analyzed aspect
├── input/                 # Reference material, cached sources
├── raw/                   # Tool outputs (JSON, CSV, etc.)
└── status/
    ├── converged.txt      # Written when loop converges
    └── paused.txt         # Create to pause the loop
```

## GitHub Access

The `gh` CLI is available and authenticated. Use it for GitHub API access in loops and tasks:
- `gh api` for raw API queries (supports `--jq` for filtering)
- `gh repo`, `gh issue`, `gh pr`, `gh release` for structured queries
- In headless/CI environments, set `GH_TOKEN` env var — `loop.sh` passes it through automatically

## Conventions

- `[[wikilinks]]` are a lightweight cross-reference convention. Not rendered — just greppable.
- Commit messages for loop iterations: `loop(<name>): <aspect-name>`
- Project file naming: `company--project.md` (double-dash separator)
