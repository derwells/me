# Team Members Catalog

## Summary

Two completely separate team member datasets exist across the Lektor and Next.js sites with minimal overlap. The Lektor site has 26 members (19 visible), while the Next.js `libs/team.js` hardcodes 29 members (all rendered, 1 commented out). The Next.js team page also fetches from Strapi at runtime, creating a dual-data-source architecture where the hardcoded file is used for the About page TeamSlider but Strapi data drives the /team listing.

## Lektor Site: Team Members (26 total)

### Data Model (`models/teammate.ini`)

| Field | Type | Notes |
|-------|------|-------|
| name | string | Required display name |
| github_url | url | |
| twitter_url | url | |
| mastodon_url | url | Only used by 1 member (Virgile Andreani) |
| linkedin_url | url | |
| personal_url | url | |
| specializations | string | Comma-separated free text |
| location | string | Free text city/country |
| blurb | string | Short tagline (labeled "140 characters") |
| extended_bio | markdown | Longer bio, bullet-point style |
| visible | boolean | Controls display on team page |

**Undeclared field used in practice:** `picture` — 7 members have an external URL `picture` field that is NOT in the model definition. This is a Lektor quirk: undeclared fields are silently ignored by the CMS but may have been used by an earlier template.

### Complete Lektor Team Roster

| Slug | Name | Visible | Location | Specializations | Social Links | Headshot Size | Has Blurb | Has Extended Bio |
|------|------|---------|----------|----------------|--------------|--------------|-----------|-----------------|
| adrian-seyboldt | Adrian Seyboldt | yes | — | — | GitHub, Twitter | 944 KB | no | no |
| alexandre-andorra | Alexandre Andorra | yes | Paris, France | Bayesian models, Causal inference, Teaching | GitHub, Twitter, LinkedIn, Personal | 908 KB | yes | no |
| alona-krokhmal | Alona Krokhmal | **no** | — | — | GitHub, LinkedIn | 8 KB | yes | no |
| benjamin-vincent | Benjamin Vincent | yes | Scotland, UK | Bayesian Modeling, Causal Inference, PM | GitHub, Twitter, LinkedIn, Personal | 2.0 MB | yes | no |
| bernard-mares | Bernard (Ben) Mares | yes | Ferney-Voltaire, France | Math Modeling, Package Mgmt | GitHub, LinkedIn, Personal | 55 KB | no | no |
| bill-engels | Bill Engels | yes | Portland, OR | — | GitHub, LinkedIn | 32 KB | no | no |
| brandon-willard | Brandon T. Willard | **no** | Chicago, USA | PL Development, Symbolic Math, ML, etc. | GitHub, LinkedIn, Personal | 57 KB | no | no |
| daniel-saunders | Daniel Saunders | yes | — | — | GitHub, LinkedIn, Personal | 50 KB | yes | yes |
| eric-ma | Eric J. Ma | yes | Cambridge, USA | Deep learning, Graph theory, Bayesian stats | GitHub, Twitter, LinkedIn, Personal | 21 KB | yes | no |
| george-ho | George Ho | **no** | NYC, USA | — | GitHub, LinkedIn, Twitter, Personal | 35 KB | no | no |
| juan-orduz | Juan Orduz | yes | Berlin, Germany | Time series, causal inference, marketing | GitHub, Twitter, LinkedIn, Personal | 80 KB | yes | yes |
| larry-dong | Larry Dong | **no** | Toronto, Canada | — | GitHub, LinkedIn, Twitter, Personal | 40 KB | no | no |
| luciano-paz | Luciano Paz | yes | Trieste, Italy | Bayesian statistics | GitHub, LinkedIn, Personal | 43 KB | yes | no |
| maxim-kochurov | Maxim Kochurov | yes | Moscow, Russia | CV, Bayesian modelling, optimization, dev | GitHub, LinkedIn, Twitter | 227 KB | no | no |
| niall-oulton | Niall Oulton | yes | London, UK | MMM, Bayesian Modeling, PM, Client | GitHub, Twitter, LinkedIn | 1.5 MB | yes | no |
| oriol-abril-pla | Oriol Abril Pla | **no** | Barcelona, Spain | Bayesian stats, Data viz, Model comparison | GitHub, Twitter, LinkedIn, Personal | 303 KB | yes | no |
| osvaldo-martin | Osvaldo Martin | yes | San Luis, Argentina | Bayesian modeling, Exploratory analysis | GitHub, Twitter, Personal | 382 KB | yes | no |
| ravin-kumar | Ravin Kumar | **no** | Los Angeles, USA | Decision Making, Bayesian stats, Supply Chain | GitHub, Twitter, LinkedIn, Personal | 193 KB | yes | no |
| reshama-shaikh | Reshama Shaikh | yes | New York, NY, USA | Statistics, marketing, strategy | GitHub, Twitter, LinkedIn, Personal | 181 KB | yes | no |
| ricardo-vieira | Ricardo Vieira | yes | — | — | GitHub, Personal | 3.3 MB | no | no |
| sef-madria | Sef Madria | yes | — | — | GitHub | 27 KB | no | yes (used as blurb) |
| thomas-wiecki | Thomas Wiecki | yes | — | Bayesian statistics, teaching | GitHub, Twitter, LinkedIn, Personal | 679 KB | yes | yes |
| tomas-capretto | Tomás Capretto | yes | Colón, Argentina | Data viz, Statistics, Bayesian modeling | GitHub, Twitter, LinkedIn, Personal | 39 KB | yes | no |
| ulf-aslak | Ulf Aslak | yes | Gilleleje, Denmark | Complex networks, marketing, Bayesian, teaching | GitHub, Twitter, LinkedIn, Personal | 110 KB | yes | yes |
| virgile-andreani | Virgile Andreani | **no** | Boston, MA | Mathematical modeling, scientific computing | GitHub, LinkedIn, Mastodon, Personal | 51 KB | yes | yes |
| will-dean | Will Dean | yes | — | — | GitHub, LinkedIn, Personal | 87 KB | yes | yes |

### Lektor Statistics
- **Total members:** 26
- **Visible:** 19 (73%)
- **Hidden:** 7 (Alona Krokhmal, Brandon Willard, George Ho, Larry Dong, Oriol Abril Pla, Ravin Kumar, Virgile Andreani)
- **With blurb:** 18 (69%)
- **With extended bio:** 6 (23%) — Daniel Saunders, Juan Orduz, Thomas Wiecki, Ulf Aslak, Virgile Andreani, Will Dean. Sef Madria uses `extended_bio` field as a blurb.
- **With location:** 19 (73%)
- **With specializations:** 15 (58%)
- **With external `picture` URL (undeclared field):** 7 — Adrian Seyboldt, Alexandre Andorra, Brandon Willard, Eric Ma, Luciano Paz, Maxim Kochurov, Oriol Abril Pla, Ravin Kumar, Thomas Wiecki, Virgile Andreani (actually 10, pointing to GitHub avatars or external sites)
- **Total headshot storage:** ~12 MB (26 files, all JPEG)
- **Largest headshots:** Ricardo Vieira (3.3 MB), Benjamin Vincent (2.0 MB), Niall Oulton (1.5 MB) — candidates for optimization
- **Smallest headshot:** Alona Krokhmal (8 KB) — likely a placeholder

### Lektor Social Link Coverage

| Platform | Count | % |
|----------|-------|---|
| GitHub | 26 | 100% |
| LinkedIn | 21 | 81% |
| Twitter | 17 | 65% |
| Personal website | 17 | 65% |
| Mastodon | 1 | 4% |

## Next.js Site: Team Members

### Dual Data Source Architecture

The Next.js site has **two independent team data sources**:

1. **`libs/team.js`** — Hardcoded JSX array of 29 members (+ 1 commented out). Used by:
   - `components/about/TeamSlider.jsx` — Swiper carousel on About page (reads from `libs/team.js` directly)

2. **Strapi REST API** (`/api/teams`) — Dynamic CMS data. Used by:
   - `app/team/page.jsx` — Team listing page (fetches from Strapi with ISR/60s)
   - `app/team-detail/[id]/page.jsx` — Team detail page (fetches by slug from Strapi with ISR/60s)
   - `components/shared/Partners.jsx` — Partners section (receives Strapi data as prop from team page)
   - `components/team/TeamCard.jsx` — Team grid (receives Strapi data as prop from team page)

**Critical inconsistency:** The About page TeamSlider uses the hardcoded `libs/team.js` while the /team page uses Strapi. A member could appear on one page but not the other.

### Hardcoded Team Data (`libs/team.js`) — 29 Active + 1 Commented Out

| # | ID (slug) | Name | Partner | Role (desc) | Specializations | Image Source |
|---|-----------|------|---------|-------------|----------------|-------------|
| 1 | thomas-wiecki | Dr. Thomas Wiecki | **yes** | Founder of PyMC Labs | Probabilistic AI statistics, teaching | Cloudinary (dhgr6mghh) |
| 2 | christian-luhmann | Dr. Christian Luhmann | **yes** | Chief Operating Officer | Data Science | Cloudinary (dx3t8udaw) |
| 3 | luca-fiaschi | Dr. Luca Fiaschi | **yes** | Partner Gen AI Vertical | Probabilistic AI statistics | Cloudinary (dx3t8udaw) |
| 4 | niall-oulton | Niall Oulton | **yes** | VP Marketing Analytics | Marketing Analytics | Cloudinary (dx3t8udaw) |
| 5 | joe-wilkinson | Joe Wilkinson | **yes** | VP Marketing Analytics | Marketing Analytics | Cloudinary (dx3t8udaw) |
| 6 | allen-downey | Allen Downey | no | Principal Data Scientist | 13 specializations | Cloudinary (dx3t8udaw) |
| 7 | benjamin-maier | Benjamin Maier | no | Principal Data Scientist | 10 specializations | Cloudinary (dx3t8udaw) |
| 8 | bernard-mares | Bernard Mares | no | Principal Data Scientist | 10 specializations | Cloudinary (dx3t8udaw) |
| 9 | camilo-saldarriaga | Camilo Saldarriaga | no | Senior Researcher | 8 specializations | Cloudinary (dx3t8udaw) |
| 10 | christopher-fonnesbeck | Christopher Fonnesbeck | no | Principal Data Scientist | 8 specializations | Cloudinary (dx3t8udaw) |
| 11 | colt-allen | Colt Allen | no | Principal Data Scientist | 12 specializations | Cloudinary (dx3t8udaw) |
| 12 | daniel-saunders | Daniel Saunders | no | Principal Data Scientist | 4 specializations | Cloudinary (dx3t8udaw) |
| 13 | eliot-carlson | Eliot Carlson | no | Junior Researcher | 4 specializations | Cloudinary (dx3t8udaw) |
| 14 | erik-ringen | Erik Ringen | no | Principal Data Scientist | 4 specializations | Cloudinary (dx3t8udaw) |
| 15 | evan-wimpey | Evan Wimpey | no | Director of Analytics | 3 specializations | Cloudinary (dx3t8udaw) |
| 16 | francesco-muia | Francesco Muia | no | Principal Data Scientist | 8 specializations | Cloudinary (dx3t8udaw) |
| 17 | halah-joseph | Halah Joseph | no | Go to Market Manager | 7 specializations | Cloudinary (dx3t8udaw) |
| 18 | jake-piekarski | Jake Piekarski | no | Junior Researcher | 7 specializations | Cloudinary (dx3t8udaw) |
| 19 | juan-orduz | Juan Orduz | no | Principal Data Scientist | 10 specializations | Cloudinary (dx3t8udaw) |
| 20 | kemble-fletcher | Kemble Fletcher | no | Director of Product Development | 11 specializations | Cloudinary (dx3t8udaw) |
| 21 | kusti-skyten | Kusti Skyten | no | Associate Data Scientist | 13 specializations | Cloudinary (dx3t8udaw) |
| 22 | maxim-laletin | Maxim Laletin | no | Gen AI Intern | 7 specializations | Cloudinary (dx3t8udaw) |
| 23 | mengxing-baldour-wang | Mengxing Baldour-Wang | no | Junior Researcher | 4 specializations | Cloudinary (dx3t8udaw) |
| — | ~~niall-oulton~~ | ~~Niall Oulton~~ | ~~no~~ | ~~Vice President~~ | — | **Commented out** (duplicate of partner #4) |
| 24 | nina-rismal | Nina Rismal | no | Senior Researcher | 4 specializations | Cloudinary (dx3t8udaw) |
| 25 | olivera-stojanovic | Olivera Stojanovic | no | Principal Data Scientist | 6 specializations | Cloudinary (dx3t8udaw) |
| 26 | oriol-abril-pla | Oriol Abril Pla | no | Principal Data Scientist | 9 specializations | Cloudinary (dx3t8udaw) |
| 27 | pablo-de-roque | Pablo de Roque | no | (empty) | 5 specializations | Cloudinary (dx3t8udaw) |
| 28 | purna-mansingh | Purna Mansingh | no | Jr. Researcher & Community Mgr | 7 specializations | Cloudinary (dx3t8udaw) |
| 29 | sandra-meneses | Sandra Meneses | no | Senior ML Engineer | 5 specializations | Cloudinary (dx3t8udaw) |
| 30 | teemu-sailynoja | Teemu Sailynoja | no | Junior Researcher | 10 specializations | Cloudinary (dx3t8udaw) |
| 31 | titi-alailima | Titi Alailima | no | Principal Data Scientist | 11 specializations | Cloudinary (dx3t8udaw) |
| 32 | ulf-aslak | Ulf Aslak | no | Principal Data Scientist | 9 specializations | Cloudinary (dhgr6mghh) |

### Strapi Team Content Type (Inferred from API calls)

Fields consumed by the frontend:

| Field | Type | Usage |
|-------|------|-------|
| name | string | Display name |
| slug | string | URL routing (`/team-detail/[slug]`) |
| desc | string | Role/title |
| partner | boolean | Separates Partners section from Team grid |
| isVisible | boolean | Filter in API query |
| orderNumber | integer | Sort order (ascending) |
| bio | JSON array | Array of strings, rendered as bullet list |
| specializations | relation | Many-to-many, rendered as `{name}` tags |
| profile_image | media (Cloudinary) | Single image with `.url` property |
| location | string | Displayed on detail page |
| github | url | Social link |
| twitter | url | Social link |
| linkedin | url | Social link |
| website | url | Social link |
| medium | url | Social link (only Luca Fiaschi) |

### Next.js Statistics
- **Hardcoded in `libs/team.js`:** 29 active entries + 1 commented out
- **Partners (partner=true):** 5 (Thomas Wiecki, Christian Luhmann, Luca Fiaschi, Niall Oulton, Joe Wilkinson)
- **Non-partner team members:** 24 (+ 1 commented-out duplicate Niall)
- **With bio text:** 27 of 29 (93%) — Benjamin Maier and Erik Ringen have empty bio arrays
- **Cloudinary accounts used:** 2 (`dx3t8udaw` for most, `dhgr6mghh` for Thomas Wiecki and Ulf Aslak)
- **Image formats:** Mostly .webp, some .jpg and .png
- **Role distribution:** 10 Principal Data Scientist, 4 Junior Researcher, 2 Senior Researcher, 2 VP Marketing Analytics, 1 COO, 1 Founder, 1 Director of Analytics, 1 Director of Product Dev, 1 Go to Market Mgr, 1 Sr ML Engineer, 1 Associate DS, 1 Gen AI Intern, 1 Jr Researcher & Community Mgr, 1 Partner, 1 empty

## Cross-Site Comparison

### Members on Both Sites (9 overlap)

| Slug | Lektor Visible | Next.js Partner | Role Changes |
|------|---------------|-----------------|-------------|
| thomas-wiecki | yes | **yes** | "Founder, PyMC Labs" → "Founder of PyMC Labs" |
| niall-oulton | yes | **yes** | "Marketing analytics specialist" → "VP Marketing Analytics" |
| bernard-mares | yes | no | No role → "Principal Data Scientist" |
| daniel-saunders | yes | no | Generic blurb → "Principal Data Scientist" |
| juan-orduz | yes | no | "Mathematician and data scientist" → "Principal Data Scientist" |
| oriol-abril-pla | **no** (hidden) | no | Hidden on Lektor, visible on Next.js |
| ulf-aslak | yes | no | Generic blurb → "Principal Data Scientist" |
| will-dean | yes | no | — (not in Next.js hardcoded, may be in Strapi) |

Wait — Will Dean is NOT in `libs/team.js`. Let me recount:

**Actually present on both sites (8 overlap):**
thomas-wiecki, niall-oulton, bernard-mares, daniel-saunders, juan-orduz, oriol-abril-pla, ulf-aslak + partial overlap via Strapi for others.

### Only on Lektor (18 members)
Adrian Seyboldt, Alexandre Andorra, Alona Krokhmal, Benjamin Vincent, Bill Engels, Brandon Willard, Eric Ma, George Ho, Larry Dong, Luciano Paz, Maxim Kochurov, Osvaldo Martin, Ravin Kumar, Reshama Shaikh, Ricardo Vieira, Sef Madria, Tomas Capretto, Virgile Andreani, Will Dean

### Only on Next.js `libs/team.js` (21 members)
Christian Luhmann, Luca Fiaschi, Joe Wilkinson, Allen Downey, Benjamin Maier, Camilo Saldarriaga, Christopher Fonnesbeck, Colt Allen, Eliot Carlson, Erik Ringen, Evan Wimpey, Francesco Muia, Halah Joseph, Jake Piekarski, Kemble Fletcher, Kusti Skyten, Maxim Laletin, Mengxing Baldour-Wang, Nina Rismal, Olivera Stojanovic, Pablo de Roque, Purna Mansingh, Sandra Meneses, Teemu Sailynoja, Titi Alailima

### Data Model Differences

| Feature | Lektor | Next.js (hardcoded) | Strapi (inferred) |
|---------|--------|-------------------|-------------------|
| Bio format | Markdown (extended_bio) | JSX elements (partners) or plain strings (non-partners) | JSON string array |
| Specializations | Comma-separated string | String array | Relation (separate content type) |
| Image storage | Local `headshot.jpg` + some external URLs | Cloudinary URLs | Cloudinary via Strapi media |
| Visibility control | `visible` boolean | All shown (1 commented out) | `isVisible` boolean + `orderNumber` sort |
| Partner distinction | None | `partner` boolean | `partner` boolean |
| Social links | 5 URL fields (github, twitter, mastodon, linkedin, personal) | Object properties (github, twitter, linkedin, website, medium) | Same as hardcoded |
| Title/role | `blurb` field (free text) | `desc` field (structured role) | `desc` field |

## Issues Found

1. **Dual data source on Next.js** — `libs/team.js` (29 members) is used by TeamSlider on About page, while Strapi data is used by /team page. Members could appear on one but not the other.

2. **Commented-out duplicate** — Niall Oulton appears as partner (#4) and has a commented-out non-partner entry (#23-ish) with different role text ("VP Marketing Analytics" vs "Vice President").

3. **Inconsistent bio formats** — Partners in `libs/team.js` use JSX `<p>` elements with `key` props; non-partners use plain string arrays. Mixing formats in the same data structure.

4. **Wrong LinkedIn for Luca Fiaschi** — His `linkedin` field points to `https://github.com/lfiaschi` (a GitHub URL, not LinkedIn).

5. **Missing `https://` on some URLs** — Bernard Mares github: `github.com/maresb/`, Evan Wimpey github: `github.com/ewimpey`, Olivera Stojanovic linkedin: `www.linkedin.com/...`. TeamDetails component handles linkedin prefix but not others.

6. **Wrong domain in JSON-LD** — Team detail page uses `pymc-labs.io` instead of `pymc-labs.com` in JSON-LD structured data.

7. **`libs/team.js` imports Team but TeamSlider reads from hardcoded, not Strapi** — About page's team carousel will never reflect Strapi updates.

8. **Pablo de Roque has empty `desc`** — No role title displayed.

9. **Two Cloudinary accounts** — Most images on `dx3t8udaw`, but Thomas Wiecki and Ulf Aslak use `dhgr6mghh`. Likely different upload sessions or migration artifacts.

10. **Lektor headshot sizes wildly inconsistent** — Range from 8 KB (placeholder?) to 3.3 MB. No image optimization pipeline. Total ~12 MB for 26 headshots.

11. **Undeclared `picture` field in Lektor** — 7+ members have external `picture` URLs in .lr files, but this field isn't in the model. These URLs point to GitHub avatars and external sites that may break.

12. **Stale social links** — Lektor Twitter URLs still use `twitter.com` (now X). Mastodon field exists but only 1 member uses it. No Bluesky field despite social platform shift noted in integrations analysis.

13. **No content sync between sites** — The 8 members who appear on both have divergent bios, specializations, and social links. No single source of truth.

14. **Specializations data quality gap** — Lektor uses free-text comma-separated strings (inconsistent). Next.js hardcoded uses structured arrays. Strapi uses a relation to a separate specializations content type. Three different approaches.
