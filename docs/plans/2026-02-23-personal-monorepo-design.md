# Personal Monorepo — Design Doc

**Created:** 2026-02-23
**Status:** Approved
**Reference:** https://github.com/clsandoval/monorepo (studied, selectively adapted)

---

## What This Is

A personal monorepo rooted at `/home/derick/dev/me/`. Two purposes:

1. **Ralph loops** — the core feature. Frontier-driven analysis loops that converge on specs.
2. **Project context** — lightweight index of things I'm working on, so Claude can orient itself.

## What We're NOT Building

Studied clsandoval's monorepo and deliberately skipping:

- Entity system (8 types, YAML frontmatter, Dataview schemas)
- Dashboards (Dataview queries)
- Automations (OpenClaw Telegram bot, webhook infra)
- CI/CD loop runner (`.github/workflows/ralph-loops.yml`)
- Meetings, trips, people, places, businesses folders
- Heavy Obsidian integration

These can be added later if needed. Starting minimal.

## Structure

```
/home/derick/dev/me/
├── CLAUDE.md
├── .gitignore
├── projects/
│   ├── nutsandbolts--cheerful.md
│   └── pymc--decision-orchestrator.md
└── loops/
    ├── _template/
    │   ├── PROMPT.md.example
    │   ├── frontier/
    │   │   └── aspects.md.example
    │   └── loop.sh
    └── _registry.yaml
```

Other directories (`docs/plans/`, `data/`, `research/`, `inbox/`) get created organically when something needs them. No empty placeholder folders.

### Naming Convention

Project files use `company--project.md` format (double-dash separator):
- `nutsandbolts--cheerful.md`
- `pymc--decision-orchestrator.md`

## Ralph Loops (Reverse Only for Now)

### How They Work

A ralph loop is a frontier-driven iterative analysis pattern:

1. **Frontier** (`frontier/aspects.md`) — a checklist of aspects to analyze, organized in dependency waves
2. **One iteration = one aspect** — each run reads the frontier, picks the first unchecked item, analyzes it, writes findings, updates the frontier, commits, exits
3. **Convergence** — when all aspects are checked and the output passes self-review, the loop writes `status/converged.txt`
4. **State is on the filesystem** — if the loop crashes, it restarts, reads what's done, picks up where it left off

### Running Loops

**Claude Code web (primary):** Open a session, point it at the loop's PROMPT.md, say "run one iteration." User is the outer loop.

**Claude Code CLI:** `cd loops/<name> && ./loop.sh` — bash script pipes PROMPT.md into Claude repeatedly until convergence.

### Template

`loops/_template/` contains:

- **`PROMPT.md.example`** — reverse loop template with `{{placeholder}}` markers. Copy, rename to `PROMPT.md`, fill in blanks.
- **`frontier/aspects.md.example`** — wave-based checklist template. Copy, rename, seed with initial aspects.
- **`loop.sh`** — bash runner from clsandoval's repo (works as-is). 1800s timeout per iteration, 3-failure stop, sleep between iterations.

### Starting a New Loop

1. `cp -r loops/_template loops/<name>`
2. Rename `PROMPT.md.example` → `PROMPT.md`, fill in the `{{placeholders}}`
3. Rename `frontier/aspects.md.example` → `frontier/aspects.md`, seed waves
4. Add entry to `loops/_registry.yaml`
5. Run it

### Registry

`loops/_registry.yaml` — tracks all loops with status, type, description, dates. Starts empty.

## Project Context Cards

`projects/` holds lightweight context cards. Each file covers:

- What the project is
- Tech stack
- Key features built
- Scale (LOC, commits, team size)
- Architectural connections to other projects
- Notes section for personal context

Content for Cheerful and Decision Orchestrator is pulled from clsandoval's analysis files (same projects, same teams).

## CLAUDE.md

Root context file that covers:

- Repo purpose and structure
- How ralph loops work (reverse, frontier-driven, one-unit-per-iteration, convergence)
- How to run loops (web vs CLI)
- Pointer to project context in `projects/`
- `[[wikilinks]]` as lightweight cross-reference convention
- Professional context summary

Concise but complete enough for Claude to orient in any session.

## Cross-References

`[[wikilinks]]` are a lightweight convention. Not rendered by Obsidian — just a greppable cross-reference pattern that Claude can follow.
