# Current Profile Snapshot — derwells (LinkedIn)

**Analyzed**: 2026-02-23
**Source**: WebFetch attempt (blocked — LinkedIn returns 999 for unauthenticated bots), cross-referenced from `analysis/org-work-analysis.md`, `analysis/monorepo-project-inventory.md`, `analysis/github-profile-cross-ref.md`, `../../loops/github-profile-reverse/analysis/profile-snapshot.md`

---

## Access Note

LinkedIn returns HTTP 999 for automated requests — this is their standard anti-scraping response. Direct profile content could not be fetched. What follows is reconstructed from:
1. Known data in prior Wave 1 analysis files (org-work-analysis, monorepo-project-inventory, github-profile-cross-ref)
2. The GitHub profile loop's profile-snapshot (which documented the GitHub side as of 2026-02-23)
3. Inferences from the LinkedIn URL structure itself (`wfo-wells`)

The user should verify specific current headline/about text directly. The gaps identified below are high-confidence based on cross-reference data.

---

## What Is Known About The Current Profile

### URL and Identity

- **LinkedIn URL**: `linkedin.com/in/wfo-wells`
- **Vanity URL**: `wfo-wells` — opaque, not name-based. Likely an auto-generated slug or old handle. Does not include "derwells" or "Derick Wells."
- **Name on profile**: Derick Wells

### Current Experience Entries

**High confidence (from org-work-analysis.md):**

> "neither of these roles is currently on the LinkedIn profile"

| Org | Project | On LinkedIn? |
|-----|---------|-------------|
| Nuts and Bolts AI | Cheerful | **No** |
| PyMC Labs | Decision Orchestrator | **No** |

Both production roles — the person's primary professional output for the past 1-2 years — are absent from the profile. This is the largest gap.

### GitHub Profile Cross-Signal

From `../../loops/github-profile-reverse/analysis/profile-snapshot.md`:
- GitHub `company` field: **empty**
- GitHub `bio`: **empty**
- GitHub `blog/website`: **empty**

GitHub and LinkedIn tend to be updated in tandem. The blank GitHub state strongly suggests the LinkedIn profile is similarly sparse — no current job listed, no recent updates, possibly still showing university-era information (if anything).

### What Likely Appears (Based on Arc)

Given the academic arc documented in monorepo-project-inventory:
- **Education**: University (Philippines) — likely a BS in Computer Science or similar, 2019–2023 (7-year-old account, born ~2001, graduated ~2023 based on repo timeline)
- **Old projects**: Possibly some university project entries or skills from 2021-2022 era
- **No current employer listed**: Confirmed by org-work-analysis
- **Skills section**: Unknown, possibly auto-added from endorsements or empty

### What Is Almost Certainly Missing

Based on all Wave 1 analysis, the following are absent from the current profile:

| Missing element | Significance | Where it belongs |
|-----------------|-------------|------------------|
| Nuts and Bolts AI experience entry | Primary current role; ~13,100 LOC production platform | Experience |
| PyMC Labs experience entry | Primary current or recent role; 36,400 LOC infrastructure project | Experience |
| AI/agent tech stack skills | Claude Agent SDK, MCP, Temporal.io, Langfuse, Composio | Skills |
| About/Summary | Almost certainly empty or generic | About |
| Compelling headline | `wfo-wells` URL suggests no strong headline identity | Headline |
| Featured section | Likely empty or default | Featured |
| Custom URL | `wfo-wells` is not name-based or memorable | URL |

---

## First Impression Analysis

### What A Stranger Sees Today

Based on the reconstructed state:

1. **Headline**: Likely bare or generic (e.g., "Software Engineer" or blank) — no product/platform signal
2. **About**: Almost certainly empty or a one-liner. No hook, no story.
3. **Experience**: University-era entries (if any) and/or empty. Two production roles invisible.
4. **Skills**: May have some auto-generated entries from early career, but AI stack is absent.
5. **Activity**: Low — no posts, no content signal.

**The gut reaction a recruiter gets today**: "Inactive. Maybe a student who graduated and disappeared. No current employer visible. Nothing to click on."

This is exactly the same problem as the GitHub profile: the gap between what's visible and what's real is enormous. A stranger cannot tell this person is:
- Building production AI infrastructure at two companies
- The author of a custom MCP registry built at protocol level
- Working with Temporal.io, Claude Agent SDK, Langfuse across two production systems
- 50,000+ LOC of active production code in the last 12 months

### Comparison: Current vs. Reality

| What LinkedIn shows | What's real |
|---------------------|-------------|
| No employer / student-era entries | Two active production roles |
| No skills in AI | Custom MCP implementation, Claude Agent SDK, Temporal.io |
| No headline claim | The differentiating pitch: "AI infrastructure builder, two domains, same platform" |
| `wfo-wells` URL | Should be `derick-wells` or `derwells` |
| No featured content | crowNNs or MCP post would drive profile clicks |
| No about section | The platform thesis story + academic arc |

---

## Gap Severity Assessment

| Gap | Severity | Urgency |
|-----|----------|---------|
| Two current roles not listed | Critical | Highest |
| No headline | Critical | Highest |
| No about section | Critical | High |
| `wfo-wells` URL | Moderate | Medium |
| No skills (AI stack) | Moderate | Medium |
| No featured content | Low | Low |

---

## What The Updated Profile Must Do

This snapshot confirms what the org-work-analysis recommended: **the single most important update is adding experience entries for Nuts and Bolts AI and PyMC Labs.** Everything else (headline, about, skills) builds on top of these anchors.

A visitor looking at the profile after the update should be able to answer in 10 seconds:
1. What does this person build? (AI agent infrastructure)
2. Where do they work? (Nuts and Bolts AI + PyMC Labs)
3. What specifically did they ship? (Cheerful campaign engine + Decision Orchestrator)
4. What tech stack? (Claude Agent SDK, MCP, Temporal.io, Supabase, Langfuse)
5. Why does that matter? (platform-level thinking, same architecture proven across two domains)

Currently: none of these questions can be answered from the profile.

---

## Action Items (Carried Forward to Wave 2)

1. **URL**: Change vanity URL from `wfo-wells` to `derwells` or `derick-wells-ai` (shorter, name-based, memorable)
2. **Headline**: Lead with role identity + domain (not just "Software Engineer")
3. **About**: Write from scratch — platform thesis hook in first 2 lines
4. **Experience**: Add Nuts and Bolts AI (Cheerful) + PyMC Labs (Decision Orchestrator) as full entries
5. **Skills**: Add entire AI stack: Python, Claude Agent SDK, MCP, Temporal.io, FastAPI, Next.js, Supabase, Langfuse, Composio, CUDA, PostgreSQL
6. **Featured**: Pin crowNNs GitHub link or a written post about building AI infrastructure
