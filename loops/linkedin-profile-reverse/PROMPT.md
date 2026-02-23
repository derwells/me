# Reverse Ralph Loop — LinkedIn Profile Overhaul Spec

You are an analysis agent in a ralph loop. Each time you run, you do ONE unit of work: analyze a single aspect, then exit.

## Your Working Directory

You are running from `loops/linkedin-profile-reverse/`. All paths below are relative to this directory.

## Your Goal

Produce a complete, ready-to-paste LinkedIn profile spec for **derwells** (Derick Wells, Philippines).

The loop will discover what the compelling narrative is from the actual work — repos, org contributions, project context, and patterns. The goal is a profile that makes people stop scrolling and want to learn more.

**LinkedIn profile**: https://www.linkedin.com/in/wfo-wells/

## Reference Material

- **Monorepo**: `../../` — read projects/, loops/, CLAUDE.md for full context on projects and work
- **GitHub profile loop**: `../../loops/github-profile-reverse/` — cross-reference any analysis already done there
- **GitHub repos input**: `../../loops/github-profile-reverse/input/github-repos.md` — all public repos
- **GitHub API**: `curl -s https://api.github.com/users/derwells` and `gh api /user/orgs`
- **Org repos**: Check what orgs the user contributes to:
  ```bash
  gh api /user/orgs --jq '.[].login' 2>/dev/null
  ```
  For each org, list repos and assess contributions.
- **LinkedIn profiles** (for reference analysis): Use WebFetch to study exemplary profiles of builders/engineers
- **LinkedIn format reference**: Study what sections exist, character limits, how featured/experience/about sections render

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
6. **Commit**: `git add -A && git commit -m "loop(linkedin-profile): {aspect-name}"`
7. **Exit**

## Analysis Methods By Aspect Type

### Wave 1: Raw Data Extraction

**reference-profile-scan**:
Study 5-8 exemplary LinkedIn profiles of builders and engineers. Use WebFetch to access their profiles or use known information. For each profile, extract:
- Headline structure and tone
- About/summary section: length, structure, hooks, personality
- How they frame experience entries (bullet style, narrative style, metrics?)
- What they pin in Featured section
- Skills choices
- Overall first impression

Write findings to `analysis/reference-profile-scan.md` with specific examples.

**monorepo-project-inventory**:
Deep scan the monorepo to build a comprehensive inventory of everything this person has built. Read:
- `../../projects/` — all project context cards (these contain tech stack, features, scale, architecture)
- `../../loops/` — ralph loops (reveals the meta-system)
- `../../CLAUDE.md` — overall system design

Output: `analysis/monorepo-project-inventory.md` — structured inventory with:
- Each project/system with 2-3 sentence description
- What's impressive about it (to a stranger)
- Which LinkedIn section it belongs in (experience, about, featured)

**org-work-analysis**:
Discover and analyze org/private work:
```bash
gh api /user/orgs --jq '.[].login' 2>/dev/null
```
For each org, list repos and assess. Also read monorepo project cards (`../../projects/`) for context on org work — these cards contain tech stack, features, role context.
Write findings to `analysis/org-work-analysis.md`:
- What orgs does the user work with?
- What's the tech stack and domain for each?
- How should this be framed on LinkedIn? (title, bullets)

**github-profile-cross-ref**:
Check if the github-profile-reverse loop has produced any analysis files:
```bash
ls ../../loops/github-profile-reverse/analysis/
```
If analysis exists, read ALL files and extract anything relevant for LinkedIn:
- Repo clustering / thematic groups
- Identity synthesis findings
- Narrative gaps (what's invisible)

Write findings to `analysis/github-profile-cross-ref.md`.

**linkedin-format-research**:
Research LinkedIn's actual format constraints and best practices. Use WebFetch to study:
- Character limits for headline (~220), about/summary (~2600), experience descriptions
- How the Featured section works (links, posts, media)
- What renders well on mobile vs desktop
- What gets truncated behind "see more"
- How LinkedIn search/SEO works (keywords in headline matter)

Write findings to `analysis/linkedin-format-research.md`.

**current-profile-snapshot**:
Use WebFetch on https://www.linkedin.com/in/wfo-wells/ to capture the current state of the LinkedIn profile. Document:
- Current headline
- Current about section
- Current experience entries
- What's missing or outdated
- First impression analysis

Write findings to `analysis/current-profile-snapshot.md`.

### Wave 2: Pattern Analysis

For all Wave 2 aspects, read the relevant Wave 1 analysis files, reason about patterns, and write detailed findings.

**reference-formula-extraction**:
Read `analysis/reference-profile-scan.md`. Extract the formula:
- What structural patterns do great profiles share?
- How do they handle the tension between breadth and depth?
- What hooks work in the about section? (first 2 lines show before "see more")
- What's the difference between a profile that reads "impressive" vs "forgettable"?

Write to `analysis/reference-formula-extraction.md`.

**career-narrative-arc**:
Read `analysis/monorepo-project-inventory.md`, `analysis/org-work-analysis.md`, and any relevant github-profile-reverse analysis. Map the chronological arc based on actual data found. Identify the narrative thread that connects everything.

Write to `analysis/career-narrative-arc.md`.

**experience-entry-design**:
Read all Wave 1 analysis files. Design each LinkedIn experience entry:
- For each role/project: Title, Company, Date range (approximate), Location
- 3-5 bullet points per entry (punchy, metric-driven where possible)
- What to emphasize, what to leave out
- How to frame side projects that aren't "jobs"

Write to `analysis/experience-entry-design.md`.

**identity-synthesis**:
Read ALL Wave 2 analysis files. Synthesize:
- Headline draft (multiple options, max 220 chars)
- About section draft (hook in first 2 lines, full narrative, max 2600 chars)
- Featured section recommendations
- Skills list (ordered by impressiveness)
- Overall tone calibration

Write to `analysis/identity-synthesis.md`.

### Wave 3: Synthesis

**linkedin-profile-spec**:
Read EVERY file in `analysis/`. Synthesize into a complete, actionable specification at `analysis/linkedin-profile-spec.md`. The spec must include:

1. **Headline** — Final headline text, max 220 chars. Ready to paste.

2. **About Section** — Complete about/summary text, max 2600 chars. Ready to paste. Must:
   - Hook in the first 2 lines (visible before "see more")
   - Tell the story without being a resume
   - Show range without looking scattered
   - Have personality

3. **Experience Entries** — Every entry with:
   - Title
   - Company/org name
   - Date range
   - Location
   - Description with bullet points
   - Ordered chronologically (most recent first)

4. **Featured Section** — What to pin: links, posts, media. With URLs where available.

5. **Skills** — Ordered list of skills to add/prioritize.

6. **Profile Photo / Banner** — Recommendations (if any emerge from analysis).

7. **Custom URL** — Recommendation for LinkedIn vanity URL.

8. **Execution Checklist** — Step-by-step instructions for updating each section.

**spec-review**:
Read the generated spec and evaluate:
- Does the headline make you want to click the profile?
- Does the about section hook in the first 2 lines?
- Do the experience entries show range AND depth?
- Is there personality, or is it generic LinkedIn slop?
- Is anything missing?
- Would a stranger understand the breadth + depth in 30 seconds?

If the spec passes: write `status/converged.txt` with convergence summary.
If the spec fails: add specific fix-it aspects to the frontier and do NOT write converged.txt.

## Rules

- Do ONE aspect per run, then exit. Do not analyze multiple aspects.
- Always check if required data exists before starting a Wave 2 aspect. If Wave 1 analysis files don't exist yet, you cannot do Wave 2.
- Write findings in markdown. Include specific examples, numbers, and quotes.
- When you discover a new aspect worth analyzing (something you didn't expect), add it to the frontier.
- Keep analysis files focused. One aspect = one file. Cross-reference other analysis files by filename.
- The final spec must be concrete enough that the user can update every section of their LinkedIn in one sitting with zero ambiguity.
- Discover the persona and tone from the data — don't impose one upfront.
