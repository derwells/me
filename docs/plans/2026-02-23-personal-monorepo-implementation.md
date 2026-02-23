# Personal Monorepo Bootstrap — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Bootstrap a personal monorepo at `/home/derick/dev/me/` with ralph loop templates and project context cards.

**Architecture:** Flat directory structure — `projects/` for context cards, `loops/` for ralph loop system. Everything else is emergent. Loop template is reverse-only (frontier-driven analysis → spec).

**Tech Stack:** Markdown, YAML, Bash

**Reference repo:** Cloned at `/tmp/clsandoval-monorepo` — studied and selectively adapted. Key source files for project content: `loops/linkedin-profile-reverse/analysis/cheerful-analysis.md`, `loops/linkedin-profile-reverse/analysis/decision-orchestrator-analysis.md`, `loops/github-profile-reverse/input/private-work-context.md`.

---

### Task 1: Create .gitignore

**Files:**
- Create: `.gitignore`

**Step 1: Write .gitignore**

```
# OS
.DS_Store
Thumbs.db

# Editors
*.swp
*.swo
*~
.idea/
.vscode/

# Loop artifacts
/loops/*/raw/
/loops/*/input/**/*.mp4
/loops/*/input/**/*.wav
/loops/*/input/**/*.mp3

# Cloned repos inside loops (private code)
/loops/*/input/decision-orchestrator/
/loops/*/input/cheerful/

# Python (loops may generate scripts)
__pycache__/
*.pyc
.venv/

# Temp
/tmp/
```

**Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: add .gitignore"
```

---

### Task 2: Create loop template — PROMPT.md.example

**Files:**
- Create: `loops/_template/PROMPT.md.example`

**Step 1: Write the reverse loop prompt template**

This is adapted from clsandoval's template and real PROMPT.md files (especially estate-tax-reverse). Uses `{{placeholder}}` markers for fill-in-the-blank usage.

```markdown
# {{Idea Name}} — Reverse Ralph Loop

You are an analysis agent in a ralph loop. Each time you run, you do ONE unit of work, then exit.

## Your Working Directory

You are running from `loops/{{idea-name}}/`. All paths below are relative to this directory.

## Your Goal

{{Describe what this loop should explore/analyze/produce. Be specific about the final output — a spec, a report, a dataset, etc.}}

## Reference Material

{{List input sources. These might be URLs to fetch in Wave 1, local files in input/, or external APIs to query.}}

### Cached Sources (after Wave 1)
{{List the files that Wave 1 will produce in input/ — later waves read from these instead of re-fetching.}}

## What To Do This Iteration

1. **Read the frontier**: Open `frontier/aspects.md`
2. **Find the first unchecked `- [ ]` aspect** in dependency order (Wave 1 before Wave 2 before Wave 3...)
   - If a later-wave aspect depends on data that doesn't exist yet, skip to an earlier-wave aspect
   - If ALL aspects are checked `- [x]`: write convergence summary to `status/converged.txt` and exit
3. **Analyze that ONE aspect** using the appropriate method (see below)
4. **Write findings** to `analysis/{{aspect-name}}.md`
5. **Update the frontier**:
   - Mark the aspect as `- [x]` in `frontier/aspects.md`
   - Update Statistics (increment Analyzed, decrement Pending, update Convergence %)
   - If you discovered new aspects worth analyzing, add them to the appropriate Wave
   - Add a row to `frontier/analysis-log.md`
6. **Commit**: `git add -A && git commit -m "loop({{idea-name}}): {{aspect-name}}"`
7. **Exit**

## Analysis Methods By Wave

### Wave 1: {{Data Acquisition / Initial Exploration}}
{{Describe what tools and methods to use for initial data gathering. Examples: fetch URLs, clone repos, parse files, run extraction scripts.}}

### Wave 2: {{Pattern Analysis / Deep Dive}}
Depends on Wave 1 data.
{{Describe how to analyze patterns from Wave 1 data. Examples: LLM reasoning over raw data, statistical analysis, cross-referencing sources.}}

### Wave 3: {{Synthesis / Output}}
Depends on all Wave 2 analysis.
{{Describe how to synthesize findings into the final output. Typically: draft the spec/report, then self-review it.}}

## Rules

- Do ONE aspect per run, then exit. Do not analyze multiple aspects.
- Always check if required source files exist before starting a later-wave aspect.
- Write findings in markdown with specific numbers, examples, and citations.
- When you discover a new aspect worth analyzing, add it to the frontier in the appropriate wave.
- Keep analysis files focused. One aspect = one file.
- {{Add any domain-specific rules here.}}
```

**Step 2: Commit**

```bash
git add loops/_template/PROMPT.md.example
git commit -m "feat: add reverse loop prompt template"
```

---

### Task 3: Create loop template — frontier/aspects.md.example

**Files:**
- Create: `loops/_template/frontier/aspects.md.example`

**Step 1: Write the frontier template**

```markdown
# Frontier — {{Idea Name}}

## Statistics
- Total aspects discovered: {{N}}
- Analyzed: 0
- Pending: {{N}}
- Convergence: 0%

## Pending Aspects (ordered by dependency)

### Wave 1: {{Data Acquisition / Initial Exploration}}
- [ ] {{aspect-1}} — {{Description of what to explore or fetch}}
- [ ] {{aspect-2}} — {{Description of what to explore or fetch}}

### Wave 2: {{Pattern Analysis / Deep Dive}}
Depends on Wave 1 data.
- [ ] {{aspect-3}} — {{Description of pattern to analyze}}
- [ ] {{aspect-4}} — {{Description of pattern to analyze}}

### Wave 3: {{Synthesis / Output}}
Depends on all Wave 2 analysis.
- [ ] {{output-draft}} — {{Synthesize all findings into final output}}
- [ ] {{output-review}} — {{Self-review for completeness and actionability}}

## Recently Analyzed
(Empty — loop hasn't started yet)
```

**Step 2: Commit**

```bash
git add loops/_template/frontier/aspects.md.example
git commit -m "feat: add frontier aspects template"
```

---

### Task 4: Create loop template — loop.sh

**Files:**
- Create: `loops/_template/loop.sh` (executable)

**Step 1: Write loop.sh**

Copy directly from clsandoval's template — it works as-is. Standard bash runner: pipes PROMPT.md into `claude --print --dangerously-skip-permissions`, 1800s timeout, 3-failure stop, 5s sleep between iterations. Checks for convergence (`status/converged.txt`) and pause (`status/paused.txt`) signals.

```bash
#!/bin/bash
# Ralph Loop — Standard Runner
# Runs Claude Code repeatedly until convergence.
#
# Usage: cd loops/<idea-name> && ./loop.sh [max_iterations]

set -uo pipefail

# Allow nested Claude Code sessions
unset CLAUDECODE 2>/dev/null || true

WORK_DIR="$(cd "$(dirname "$0")" && pwd)"
LOOP_NAME="$(basename "$WORK_DIR")"
PROMPT_FILE="$WORK_DIR/PROMPT.md"
CONVERGED_FILE="$WORK_DIR/status/converged.txt"
PAUSED_FILE="$WORK_DIR/status/paused.txt"
MAX_ITERATIONS=${1:-40}
SLEEP_BETWEEN=5

cd "$WORK_DIR"

if [ ! -f "$PROMPT_FILE" ]; then
    echo "ERROR: PROMPT.md not found at $PROMPT_FILE"
    exit 1
fi

if [ -f "$PAUSED_FILE" ]; then
    echo "Loop '$LOOP_NAME' is paused. Remove status/paused.txt to resume."
    exit 0
fi

if [ -f "$CONVERGED_FILE" ]; then
    echo "Loop '$LOOP_NAME' already converged."
    exit 0
fi

mkdir -p status

iteration=0
failures=0

echo "=== Ralph Loop Starting: $LOOP_NAME ==="
echo "Working directory: $WORK_DIR"
echo "Max iterations: $MAX_ITERATIONS"
echo ""

while [ ! -f "$CONVERGED_FILE" ] && [ "$iteration" -lt "$MAX_ITERATIONS" ]; do
    iteration=$((iteration + 1))
    echo "--- Iteration $iteration / $MAX_ITERATIONS ---"
    echo "$(date '+%Y-%m-%d %H:%M:%S')"

    iter_log="/tmp/ralph-${LOOP_NAME}-iter-${iteration}.log"
    if timeout 1800 bash -c 'unset CLAUDECODE; cat "$1" | stdbuf -oL claude --print --dangerously-skip-permissions' _ "$PROMPT_FILE" 2>&1 | stdbuf -oL tee "$iter_log"; then
        echo ""
        echo "Iteration $iteration completed successfully."
        failures=0
    else
        iter_exit=$?
        if [ "$iter_exit" -eq 124 ]; then
            echo "WARNING: Iteration $iteration timed out after 1800s"
        else
            echo "WARNING: Iteration $iteration exited with code $iter_exit"
        fi
        failures=$((failures + 1))
        if [ "$failures" -ge 3 ]; then
            echo "ERROR: 3 consecutive failures. Stopping loop."
            break
        fi
    fi

    echo "Sleeping ${SLEEP_BETWEEN}s..."
    sleep "$SLEEP_BETWEEN"
done

echo ""
echo "=== Loop Summary: $LOOP_NAME ==="
echo "Iterations run: $iteration"
echo "Failures: $failures"

if [ -f "$CONVERGED_FILE" ]; then
    echo "Status: CONVERGED"
    cat "$CONVERGED_FILE"
elif [ "$iteration" -ge "$MAX_ITERATIONS" ]; then
    echo "Status: STOPPED (max iterations reached)"
    echo "Check frontier/ for remaining work."
else
    echo "Status: STOPPED (failures)"
    echo "Check /tmp/ralph-${LOOP_NAME}-iter-*.log for details."
fi
```

**Step 2: Make executable and commit**

```bash
chmod +x loops/_template/loop.sh
git add loops/_template/loop.sh
git commit -m "feat: add loop.sh bash runner"
```

---

### Task 5: Create loop registry

**Files:**
- Create: `loops/_registry.yaml`

**Step 1: Write empty registry**

```yaml
# Ralph Loop Registry
# Track active, paused, and converged loops.
#
# Fields:
#   description: What the loop does
#   type: reverse | forward
#   status: active | paused | converged
#   created: YYYY-MM-DD
#   converged_at: YYYY-MM-DD (when applicable)

loops: {}
```

**Step 2: Commit**

```bash
git add loops/_registry.yaml
git commit -m "feat: add empty loop registry"
```

---

### Task 6: Create project context card — Cheerful

**Files:**
- Create: `projects/nutsandbolts--cheerful.md`

**Step 1: Write Cheerful context card**

Content pulled from clsandoval's `loops/linkedin-profile-reverse/analysis/cheerful-analysis.md` and `loops/github-profile-reverse/input/private-work-context.md`. Same project, same team — Derick is a contributor alongside clsandoval.

The card should cover:
- What Cheerful is (email automation platform for influencer marketing at Nuts and Bolts AI)
- Tech stack (detailed):
  - Backend: Python, FastAPI, Temporal.io, Claude SDK + Agent SDK, Gmail API, Composio, Supabase, Langfuse
  - Frontend: Next.js 16+, React 19, TanStack Query, Zustand, Tailwind + Radix/shadcn
  - Context Engine: Slack Bolt, Claude Agent SDK, Onyx RAG, MCP servers
- Key features: campaign management, creator search/enrichment, AI email drafting, Gmail OAuth, Temporal workflows, Slack Context Engine, multi-step campaign wizard
- Scale: ~2,170 source files, ~13,100 LOC, ~5,570 total commits, 3 apps, team of 5
- Connection to Decision Orchestrator: same architectural DNA (Claude SDK, MCP, Supabase, Langfuse, Composio)
- Empty Notes section

**Step 2: Commit**

```bash
git add projects/nutsandbolts--cheerful.md
git commit -m "feat: add Cheerful project context card"
```

---

### Task 7: Create project context card — Decision Orchestrator

**Files:**
- Create: `projects/pymc--decision-orchestrator.md`

**Step 1: Write Decision Orchestrator context card**

Content pulled from clsandoval's `loops/linkedin-profile-reverse/analysis/decision-orchestrator-analysis.md` and `loops/github-profile-reverse/input/private-work-context.md`. Same project, same team.

The card should cover:
- What it is (Discord-based organizational OS at PyMC Labs)
- Tech stack (detailed):
  - Core: Python 3.12+, discord.py, Claude Agent SDK, Composio
  - MCP: Custom MCP tool registry with @tool decorator, context injection, credential gating (NOT FastMCP)
  - Database: Supabase (PostgreSQL), SQLAlchemy 2.0
  - Infra: FastAPI (webhooks), Langfuse, Fly.io
  - Architecture: FCIS (Functional Core, Imperative Shell)
- Key features: workflow-based orchestration, intelligent message routing, custom MCP tool registry, thread session persistence, multi-platform integrations (Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io), Discord archive sync, shared client library
- Scale: ~285 Python files, ~36,400 LOC, 24 direct dependencies, 5+ database tables
- Connection to Cheerful: same architectural DNA
- PyMC Labs context: what the org does, how Decision Orchestrator fits
- Empty Notes section

**Step 2: Commit**

```bash
git add projects/pymc--decision-orchestrator.md
git commit -m "feat: add Decision Orchestrator project context card"
```

---

### Task 8: Create CLAUDE.md

**Files:**
- Create: `CLAUDE.md`

**Step 1: Write CLAUDE.md**

Root context file. Must cover:
- Repo purpose: personal monorepo, primarily a ralph loop system with project context
- Structure: `projects/` (context cards, `company--project.md` naming), `loops/` (template + registry)
- How ralph loops work: reverse loops, frontier-driven, one-unit-per-iteration, wave dependencies, convergence via frontier exhaustion + self-review
- How to run: Claude Code web (user is outer loop, "run one iteration") vs CLI (`./loop.sh`)
- How to start a new loop: cp template, fill PROMPT.md, seed frontier, add to registry
- Project context: point to `projects/` for Cheerful and Decision Orchestrator details
- `[[wikilinks]]` convention: lightweight cross-reference, greppable
- Keep it concise — this is a reference, not a manual

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "feat: add root CLAUDE.md context file"
```

---

## Execution Order

Tasks 1-5 have no dependencies on each other (all independent files). Tasks 6-7 are independent. Task 8 (CLAUDE.md) references the structure from all prior tasks so should go last.

Recommended: run tasks 1-5 in parallel, then 6-7 in parallel, then task 8.
