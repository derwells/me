# LinkedIn Format Research

## Character Limits (2025)

### Profile Sections

| Section | Limit | Notes |
|---|---|---|
| Professional Headline | 220 chars (desktop) / 240 chars (mobile) | Most important SEO field |
| About Section | 2,600 chars | ~200–300 chars visible before "See More" |
| Experience Title | 100 chars | |
| Experience Description | 2,000 chars | ~300 chars visible before "See More" |
| Custom LinkedIn URL | 29 chars | |
| Skills (per skill) | 80 chars | |
| Publication Title | 250 chars | |
| Publication Description | 2,000 chars | |
| Connection Request Note | 300 chars | |
| Website Anchor Text | 30 chars | |

---

## Critical Truncation Points

### About Section
- **Desktop**: First ~200–300 characters visible before "See More" button
- **Mobile**: First ~200 characters (less than desktop)
- **Implication**: The hook — the first 1–2 sentences — must do the work. The reader won't see anything else unless they tap "See More"
- **57%+ of LinkedIn traffic is mobile** → optimize for mobile first

### Experience Description
- Similarly truncated on mobile — first 3–4 lines act as a hook
- Use line breaks and bullet points to make the visible area punchy

### Headline
- Fully visible everywhere (no truncation) — this is prime real estate

---

## SEO / Search Visibility

### How LinkedIn Search Works
LinkedIn's algorithm functions like a lightweight search engine:
1. Crawls profiles for keyword matches to search query
2. Prioritizes **exact keyword matches** in: Headline (highest weight), About section, Experience titles/descriptions
3. Boosts profiles with: recent activity (posts, profile updates), high click-through rates in search results, complete profiles

### Keyword Strategy
- **Headline**: 3–4 primary keywords max. The headline gets the highest algorithmic weight.
- **About**: 8–12 keywords naturally integrated (2,600 chars gives room)
- **Each Experience entry**: 3–5 relevant keywords
- **Skills section**: 30–40 skills, prioritized by relevance
- LinkedIn also indexes for Google — profiles rank in Google results, increasing discoverability

### What Gets Penalized
- Unnatural keyword stuffing (algorithm detects and may penalize)
- Vague buzzwords ("innovative," "motivated") — too common, no signal value
- Concrete job titles + technical skills perform far better

---

## Featured Section

### What It Is
- Sits between About and Activity sections (high visibility, above the fold on some viewport sizes)
- User-curated — you choose what to pin
- Not indexed by LinkedIn search (so this is about human impression, not SEO)

### What You Can Pin
1. **Links** — external URLs (portfolio, GitHub, projects, blog posts)
2. **Media** — uploaded images, PDFs, presentations, videos
3. **LinkedIn Posts** — posts you've already published on LinkedIn
4. **LinkedIn Articles** — longform articles published on LinkedIn

### Key Rules
- Must have already posted on LinkedIn to feature a post
- Can feature as many items as you want (reorderable)
- Visibility follows your profile's privacy settings
- Not discoverable via search — purely a human engagement tool

### Best Practices for a Builder/Engineer Profile
- Link to GitHub profile or notable repos
- Link to personal site or portfolio
- Pin a post if you've ever written about a project publicly
- Upload a PDF "project overview" as a media item
- Keep to 3–5 items max — more dilutes attention

---

## Experience Section Structure

### What the Form Gives You
- **Title** (100 chars) — the job title / role label
- **Company** — must match a LinkedIn company page (or create one) OR free-text
- **Location**
- **Start / End date** (or "currently working here")
- **Employment type** (Full-time, Part-time, Contract, Freelance, etc.)
- **Description** (2,000 chars) — supports bullet points via Unicode bullets (•)

### Formatting Tips
- LinkedIn doesn't render markdown — no bold, no headers in descriptions
- Can use Unicode characters for visual structure: bullet points (•), em dashes (—), arrows (→)
- Bullet points via "•" character (copy-paste — not auto-formatted)
- Line breaks are preserved
- First 3–4 lines of each entry visible without clicking "See More"

### Side Projects / Freelance Framing
- Use "Employment type: Freelance" or "Contract" for project-based work
- If no formal company, you can enter a descriptive name (e.g., "Independent")
- Multiple roles at same company: LinkedIn allows stacking them under one company entry

---

## Skills Section

### Format
- Each skill: up to 80 chars
- Can add up to 50 skills
- Skills can be endorsed by connections
- Top 3 pinned skills show prominently on profile

### SEO Value
- Skills section is indexed — technical skills here boost search visibility
- Order matters: pin your most strategic skills first

---

## Profile Completeness Signal

LinkedIn's algorithm boosts complete profiles. "All-Star" status requires:
- Profile photo
- Headline
- About section
- Current position with description
- Education
- 5+ skills
- 50+ connections

---

## Mobile vs Desktop Rendering

| Element | Desktop | Mobile |
|---|---|---|
| Headline | Full 220 chars shown | Truncated (varies by device) |
| About | ~300 chars before "See More" | ~200 chars before "See More" |
| Experience description | ~300 chars before "See More" | Less |
| Featured section | Shows as horizontal scroll of cards | Stacks vertically |
| Profile photo | Circle, prominent | Circle, smaller |

**Key implication**: Front-load the most compelling information everywhere. Do not bury the lede.

---

## Vanity URL

- Format: `linkedin.com/in/[custom-url]`
- Max 29 characters
- Case-insensitive
- Current URL for derwells: `linkedin.com/in/wfo-wells/`
- Recommendation: Assess whether `derwells` or similar is available and cleaner

---

## What the Spec Must Account For

1. **Hook = first 200 chars of About section** — must work as a standalone sentence
2. **Headline = SEO string** — pack role keywords, not personality (personality goes in About)
3. **Experience descriptions** — bullet points with Unicode "•", front-load metrics/outcomes
4. **Featured section** — GitHub, personal site, any public project demo
5. **Skills** — technical-first, 30+ for maximum search coverage
6. **Everything must read well with zero formatting** — no markdown rendering in LinkedIn

---

*Sources: simplygreatresumes.com, testfeed.ai, outx.ai, metricool.com, linkedin.com/help, salesrobot.co, buffer.com/resources/linkedin-seo*
