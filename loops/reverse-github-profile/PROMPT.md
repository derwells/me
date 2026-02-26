# Reverse Ralph Loop — GitHub Profile Audit & Spec

You are an analysis agent in a ralph loop. Each time you run, you do ONE unit of work: analyze a single aspect of a GitHub profile, then exit.

## Your Working Directory

You are running from `loops/github-profile-reverse/`. All paths below are relative to this directory.

## Your Goal

Analyze the GitHub profile of `derwells` to extract a complete "profile spec" — a concrete, actionable document that a forward ralph can execute to transform the profile from a scattered collection of repos into a curated presence that tells a compelling story.

The loop will discover and synthesize what that story is — based on the actual work, repos, and patterns found.

## Reference Material

- **Repo inventory**: `input/github-repos.md` (all public repos with metadata)
- **Monorepo codebase**: `../../` (the actual monorepo — read projects/, loops/, CLAUDE.md for context)

### GitHub API Access (IMPORTANT: Use `gh` CLI for ALL GitHub API calls)

The `gh` CLI is authenticated with full repo/org scopes. **Always use `gh api` instead of `curl`** for GitHub API calls — this gives authenticated access, higher rate limits, and visibility into private repos and org memberships.

- **User's public repos**: `gh api /users/derwells/repos --paginate -q '.[] | {name, description, language, stargazers_count, forks_count, fork, created_at, updated_at, topics, archived}'`
- **ALL repos (including private)**: `gh api /user/repos --paginate -f type=all -q '.[] | select(.owner.login == "derwells") | {name, description, language, private, stargazers_count, fork, created_at, updated_at}'`
- **User profile**: `gh api /users/derwells`
- **Individual repo**: `gh api /repos/derwells/{repo}`
- **Repo commits by user**: `gh api /repos/{owner}/{repo}/commits --jq '.[].commit.message' -f author=derwells -f per_page=10`
- **README fetching**: `gh api /repos/derwells/{repo}/readme --jq '.content' | base64 -d` (or fall back to `curl -s https://raw.githubusercontent.com/derwells/{repo}/main/README.md`)
- **Pinned repos (GraphQL)**: `gh api graphql -f query='{ user(login: "derwells") { pinnedItems(first: 6) { nodes { ... on Repository { name description url stargazerCount } } } } }'`
- **Org memberships (authenticated — sees private orgs)**: `gh api /user/orgs --jq '.[].login'`
- **Org repos**: `gh api /orgs/{org}/repos --paginate --jq '.[].full_name'`
- **User's PRs in a repo**: `gh api /repos/{owner}/{repo}/pulls --jq '.[] | select(.user.login == "derwells") | {title, state, html_url}'`

## What To Do This Iteration

1. **Read the frontier**: Open `frontier/aspects.md`
2. **Find the first unchecked `- [ ]` aspect** in dependency order (Wave 1 before Wave 2 before Wave 3)
   - If Wave 2 aspects depend on Wave 1 data that doesn't exist yet, skip to another Wave 1 aspect
   - If ALL aspects are checked `- [x]`: write "CONVERGED" to `status/converged.txt` and exit
3. **Analyze that ONE aspect** using the appropriate method (see below)
4. **Write findings** to `analysis/{aspect-name}.md`
5. **Update the frontier**:
   - Mark the aspect as `- [x]` in `frontier/aspects.md`
   - Update the Statistics section (increment Analyzed, decrement Pending, update Convergence %)
   - If you discovered new aspects worth analyzing, add them to the "Discovered Aspects" section, then move them to the appropriate Wave in "Pending Aspects"
   - Add a row to `frontier/analysis-log.md`
6. **Commit**: `git add -A && git commit -m "loop(github-profile): {aspect-name}"`
7. **Exit**

## Analysis Methods By Aspect Type

### Wave 1: Raw Data Extraction

**repo-inventory**:
Read `input/github-repos.md` for the pre-seeded snapshot. Enrich with live authenticated GitHub API data:
```bash
gh api /users/derwells/repos --paginate > raw/repos-public.json
gh api /user/repos --paginate -f type=all > raw/repos-all.json
```
For each repo, extract: name, description, language, stars, forks, is_fork, private, created_at, updated_at, topics.
Write a structured inventory to `analysis/repo-inventory.md` with a table of ALL repos (public AND private personal repos) including:
- Original vs fork
- Public vs private
- Has README (yes/no)
- Has description (yes/no)
- Last activity (date)
- Primary language
- Stars

**profile-snapshot**:
Capture the current state of the GitHub profile. Use:
```bash
gh api /users/derwells > raw/profile.json
gh api graphql -f query='{ user(login: "derwells") { pinnedItems(first: 6) { nodes { ... on Repository { name description url stargazerCount } } } } }' > raw/pinned.json
```
Document in `analysis/profile-snapshot.md`:
- Bio / company / location / blog (or lack thereof)
- Current pinned repos (query via GraphQL above — **do not guess**)
- Contribution activity level
- Profile README existence (check if `derwells/derwells` repo exists)
- Overall first impression: what story does this profile tell a stranger?

**monorepo-deep-scan**:
Read the actual monorepo to understand what impressive work is hidden inside. Scan:
- `../../projects/` — What project context cards exist? Read them for tech stack, features, scale
- `../../loops/` — What ralph loops exist? Read the registry, read PROMPT.md files
- `../../CLAUDE.md` — What does the system design look like?
- `../../.github/workflows/` — What CI/CD automation exists?

Write findings to `analysis/monorepo-deep-scan.md` focusing on:
- What would impress a technical person if they could see inside
- What capabilities are completely invisible from the GitHub profile
- Specific numbers (repo count, project complexity, etc.)

**repo-readme-scan**:
For each ORIGINAL (non-fork) repo, fetch and evaluate its README:
```bash
for repo in $(gh api /users/derwells/repos --paginate --jq '.[] | select(.fork == false) | .name'); do
  echo "=== $repo ===" >> raw/readmes.txt
  gh api "/repos/derwells/$repo/readme" --jq '.content' 2>/dev/null | base64 -d >> raw/readmes.txt 2>&1 || echo "(no README)" >> raw/readmes.txt
  echo -e "\n\n" >> raw/readmes.txt
done
```
Write assessment to `analysis/repo-readme-scan.md`:
- Which repos have good READMEs vs none vs template junk
- Which repos need READMEs written
- Which repos have misleading/stale descriptions

**org-contributions**:
Scan ALL GitHub orgs (authenticated endpoint reveals private memberships):
```bash
gh api /user/orgs --jq '.[].login'
```
For each org found, list repos and check for meaningful contributions:
```bash
for org in $(gh api /user/orgs --jq '.[].login'); do
  echo "=== $org ===" >> raw/org-repos.txt
  gh api "/orgs/$org/repos" --paginate --jq '.[].full_name' >> raw/org-repos.txt 2>&1
  echo "" >> raw/org-repos.txt
done
```
Also check the monorepo project cards (`../../projects/`) for context on org work.

**Priority guidance**: Focus analysis on recent work and repos related to **distributed systems and backend engineering**. Older/irrelevant orgs can be briefly noted and moved on.

Write findings to `analysis/org-contributions.md`:
- What orgs does the user contribute to?
- What projects/repos in those orgs? (For large orgs, focus on repos with derwells's contributions)
- What's the role/contribution?
- What tech stack and domain?
- Which org work is most relevant to the profile narrative (prioritize distributed systems + backend)?

### Wave 2: Pattern Analysis

For all Wave 2 aspects, read the relevant Wave 1 analysis files, reason about patterns, and write detailed findings to `analysis/{aspect-name}.md`.

Each analysis file MUST include:
- **Summary**: 2-3 sentence overview
- **Data**: Specific repos, numbers, examples
- **Patterns**: What's consistent/repeatable
- **Spec Implications**: Concrete actions for the forward ralph

**repo-clustering**:
Read `analysis/repo-inventory.md`. Cluster repos into thematic groups. Discover the clusters from the actual data — don't force categories. For each cluster: how many repos, how strong is the signal, what story does it tell?

**signal-vs-noise**:
Read `analysis/repo-inventory.md` and `analysis/repo-readme-scan.md`. For EVERY repo, assign a verdict:

| Verdict | Criteria | Action |
|---------|----------|--------|
| **SHOWCASE** | Original, impressive, tells a story | Pin, write/improve README, add topics |
| **KEEP** | Original or meaningful fork, worth having visible | Update description, add topics |
| **ARCHIVE** | Fork with no contributions, stale, duplicate, noise | Archive (make invisible) |

Score each repo on: Originality (0-3), Activity (0-3), Story value (0-3), README quality (0-3).
Total score determines verdict: 8+ = SHOWCASE, 4-7 = KEEP, 0-3 = ARCHIVE.

**fork-audit**:
Read `analysis/repo-inventory.md`. For each forked repo, determine:
- Did the user make meaningful commits beyond the fork?
- Is it an active contribution to upstream?
- Does it demonstrate a skill or interest worth showcasing?
- Or is it just a clone with no added value?

Use the GitHub API to check:
```bash
gh api "/repos/derwells/{repo}/commits" -f author=derwells -f per_page=5
```

Verdict for each fork: KEEP (meaningful work), ARCHIVE (just a clone), SHOWCASE (substantial modification).

**narrative-gaps**:
Read `analysis/monorepo-deep-scan.md`, `analysis/repo-clustering.md`, and `analysis/org-contributions.md`. Identify:
- What skills/projects are completely invisible from the profile?
- What would make someone say "holy shit" if they could see it?
- What's the delta between "what this person has built" and "what their GitHub shows"?
- Should any hidden work become standalone repos or be referenced in the profile README?

**identity-synthesis**:
Read ALL Wave 2 analysis files. Synthesize into a cohesive identity:
- One-line bio draft (max 160 chars)
- 3-5 bullet narrative ("This person builds X, ships Y, automates Z")
- Primary archetype: what's the memorable label? Discover this from the data.
- What to emphasize vs downplay — **prioritize LLMs, recent professional work, and maybe distributed systems, and backend engineering**
- Tone calibration

### Wave 3: Synthesis

**profile-spec**:
Read EVERY file in `analysis/`. Synthesize into a complete, actionable specification at `analysis/github-profile-spec.md`. The spec must include:

1. **Profile README** — Complete markdown content for the `derwells/derwells` repo README.md. Not a template. The actual final content, ready to commit. Must include:
   - A hook (who is this person, in one punchy line)
   - What I build / what I'm into (2-4 lines, not a resume)
   - Featured projects with one-line descriptions (3-5 projects)
   - Current obsessions / rabbit holes (if relevant)
   - NO badges, NO GitHub stats widgets, NO "visitor count" cringe. Clean, text-forward, personality.

2. **Pin List** — Exactly 6 repos to pin, ordered. With justification for each.

3. **Archive List** — Every repo to archive, with one-line reason each.

4. **Description Updates** — New `description` string for every repo that's being kept. Must be punchy, not generic.

5. **Topic Tags** — New `topics` array for every repo being kept.

6. **Bio Update** — One-line bio for the GitHub profile.

7. **Execution Script** — A bash script using `gh` CLI that executes ALL changes:
   - Archive repos
   - Update descriptions
   - Update topics
   - Create `derwells/derwells` repo if it doesn't exist
   - Push the profile README
   - Note: pinning repos requires GraphQL API

**spec-review**:
Read the generated spec and ask: "Would a stranger looking at this profile immediately understand what this person does and be impressed?" Check for:
- Does the README have personality or is it generic?
- Are the pins telling the right story?
- Are we archiving enough noise?
- Are descriptions punchy or boring?
- Is anything missing?
- Would a stranger understand the breadth + depth in 30 seconds?

If the spec passes: write `status/converged.txt` with convergence summary.
If the spec fails: add specific fix-it aspects to the frontier and do NOT write converged.txt.

## Rules

- Do ONE aspect per run, then exit. Do not analyze multiple aspects.
- Always check if required data exists before starting a Wave 2 aspect. If `analysis/repo-inventory.md` doesn't exist yet, you cannot do `repo-clustering`.
- Write findings in markdown. Include specific repos, numbers, and examples.
- When you discover a new aspect worth analyzing (something you didn't expect), add it to the frontier.
- Keep analysis files focused. One aspect = one file. Cross-reference other analysis files by filename.
- The final spec must be concrete enough that a fresh Claude Code session (or a forward ralph) can execute every change with zero ambiguity.
- When evaluating repos, read the actual code/README when possible, don't just go by metadata.
