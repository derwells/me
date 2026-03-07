# Clients Catalog — PyMC Labs Websites

## Overview

Client data exists in three distinct forms across the two sites:

1. **Lektor content records** — 17 visible + 1 hidden client directories under `content/clients/`, with logos decoupled in `assets/static/images/client_logos/`
2. **Next.js client logo carousel** — 18 numbered `.webp` files in `public/clients/` with no metadata (names only in `TrustedBy.jsx` alt-text)
3. **Next.js hardcoded testimonials** — 6 client testimonials in `components/home/Testimonials.jsx`, plus placeholder testimonials on course pages

No client data lives in Strapi. There is no case study content on either site.

## Lektor Client Records (17 visible + 1 hidden)

**Model**: `models/client.ini` — 5 fields: `client_name`, `testimonial`, `logo_filename`, `date`, `homepage_url`
**Parent**: `models/clients.ini` — routes children to `client` model
**Parent content anomaly**: `content/clients/contents.lr` declares `_model: testimonials` (nonexistent model)

| # | Slug | Client Name | Logo File | Homepage URL | Date | Testimonial | Visible |
|---|------|-------------|-----------|-------------|------|-------------|---------|
| 1 | akili | Akili | akili.png (52 KB) | https://www.akiliinteractive.com | — | — | yes |
| 2 | alva_labs | Alva Labs | alva_labs.png (19 KB) | https://www.alvalabs.io/ | — | — | yes |
| 3 | appgrowth | Appgrowth | appgrowth.png (21 KB) | — | 2020-10-28 | (empty) | yes |
| 4 | appodeal | Appodeal | appodeal.png (19 KB) | https://appodeal.com | — | — | yes |
| 5 | civiqs | civiqs | civiqs.png (18 KB) | https://civiqs.com | — | — | yes |
| 6 | columbia | Columbia University | columbia_university.png (49 KB) | https://www.columbia.edu/ | — | — | yes |
| 7 | everysk | Everysk | everysk.png (46 KB) | https://www.everysk.com | 2020-10-15 | (empty) | yes |
| 8 | examplar-tech | Examplar Tech | exemplar_tech.png (5 KB) | http://www.exemplartech.com | — | — | yes |
| 9 | gain-theory | Gain Theory | gain_theory.png (12 KB) | https://www.gaintheory.com | — | — | **hidden** |
| 10 | gates | Gates | gates.png (115 KB) | https://www.gatesfoundation.org | — | — | yes |
| 11 | hello-fresh | Hello Fresh | hello_fresh.png (64 KB) | https://www.hellofresh.com | — | — | yes |
| 12 | indigo-ag | Indigo Ag | indigo.png (11 KB) | https://www.indigoag.com | — | — | yes |
| 13 | quoniam | Quoniam | quoniam.png (7 KB) | https://www.quoniam.com/en/home/ | — | (empty) | yes |
| 14 | redhawk | Redhawk | redhawk.png (18 KB) | http://www.redhawkresearch.com/ | 2021-01-17 | (empty) | yes |
| 15 | roche | Roche | roche.png (46 KB) | https://www.roche.com | — | — | yes |
| 16 | sweeplift | Sweeplift | sweeplift.png (28 KB) | https://www.sweeplift.com | — | — | yes |
| 17 | visualvest | VisualVest | visualvest.png (66 KB) | https://www.visualvest.de/ | — | — | yes |

**Total Lektor logos**: 18 PNG files (597 KB) — includes `colgate-palmolive.png` which has no content record (logo-only, used in workshop template)

### Lektor Client Data Anomalies

1. **Zero actual testimonials**: 4 clients have the `testimonial` field present but all are empty strings. The model supports testimonials; none exist.
2. **Undeclared `client` field**: `appgrowth/contents.lr` and `everysk/contents.lr` contain a `client:` field not in `client.ini` — legacy remnant from an earlier schema. Lektor silently ignores it.
3. **Name casing inconsistency**: "civiqs" is lowercase while all others are capitalized.
4. **Slug/filename mismatches**: `examplar-tech` (slug) vs `exemplar_tech.png` (logo) — typo in slug ("Examplar" vs "Exemplar").
5. **Mixed URL schemes**: 2 clients use `http://` (Exemplar Tech, Redhawk), rest use `https://`.
6. **Logo decoupling**: Logos live in `assets/static/images/client_logos/`, not as content attachments. The `logo_filename` field is a plain string — no validation that the file exists.
7. **Orphan logo**: `colgate-palmolive.png` (13 KB) exists in the logos directory but has no corresponding content record. It's referenced only in the hardcoded workshop template (`templates/applied-bayesian-modeling.html:284`).
8. **Only 3 clients have dates**: Appgrowth (2020-10-28), Everysk (2020-10-15), Redhawk (2021-01-17). Purpose unclear — possibly engagement start date.

### Lektor Client Rendering

- **`/clients/` page** (`templates/clients.html`): Renders all visible children as Bootstrap card columns using `macros/client.html`. Cards show logo (clickable if `homepage_url` set), and conditionally show client name + testimonial + date if testimonial exists. Since no testimonials exist, all cards are logo-only.
- **Workshop page** (`templates/applied-bayesian-modeling.html:283-297`): Hardcodes 15 client logos directly in template HTML (bypasses content system entirely). Includes Colgate-Palmolive (no content record) and Alva Labs (no `homepage_url` in content).
- **Individual client pages** (`templates/client.html`): Each client has its own URL (`/clients/<slug>/`) rendered via `macros/client.html` — same card format as listing.

## Next.js Client Logos (18 logos)

Client logos in the Next.js repo are numbered files (`c1.webp` through `c16.webp`, plus `c20.webp` and `c21.webp`) with no metadata in the filesystem. Names are only available from the `TrustedBy.jsx` component's alt-text.

**Source**: `public/clients/` — 51 files total (PNG + SVG + WebP variants), 1.8 MB

| File | Alt Text (from TrustedBy.jsx) | Also in Lektor? |
|------|-------------------------------|-----------------|
| c1.webp (34 KB) | Akili | Yes |
| c2.webp (12 KB) | Alva | Yes (Alva Labs) |
| c21.webp (28 KB) | Bain & Company | **No — new client** |
| c20.webp (37 KB) | Colgate Palmolive | **Logo-only in Lektor (no content record)** |
| c3.webp (11 KB) | App Growth | Yes (Appgrowth) |
| c4.webp (30 KB) | App Odeal | Yes (Appodeal) |
| c5.webp (11 KB) | CIVIQS | Yes |
| c6.webp (31 KB) | Columbia University | Yes |
| c7.webp (29 KB) | Everysk | Yes |
| c8.webp (4 KB) | Exemplar | Yes (Examplar Tech) |
| c9.webp (25 KB) | Bill & Melindia Gates | Yes (Gates) — typo: "Melindia" should be "Melinda" |
| c10.webp (19 KB) | Hello Fresh | Yes |
| c11.webp (8 KB) | Indigo | Yes (Indigo Ag) |
| c12.webp (18 KB) | Quoniam | Yes |
| c13.webp (10 KB) | RedHawk Resarch LLC | Yes (Redhawk) — typo: "Resarch" should be "Research" |
| c14.webp (27 KB) | Roche | Yes |
| c15.webp (24 KB) | SweepLift | Yes |
| c16.webp (13 KB) | VisualVest | Yes |

### Next.js Logo Usage

Logos appear in two components with different implementations:

1. **`components/home/Logos.jsx`** — Used on homepage (`Inovation.jsx` section "Some of our clients") and About page (`AboutContent.jsx`). Custom `requestAnimationFrame` auto-scroll at 30px/sec, speed-up button (400px/sec). No alt-text — just `"Logo ${i}"`. 18 logos, duplicated array for seamless loop.

2. **`app/courses/components/TrustedBy.jsx`** — Used on courses pages as "Trusted by Professionals in Top Companies". Swiper carousel with autoplay. Same 18 logos but with named alt-text. Uses `<img>` tag (not `next/image`).

### Next.js vs Lektor Logo Comparison

| Aspect | Lektor | Next.js |
|--------|--------|---------|
| Count | 18 PNG files (17 with content records + 1 orphan) | 18 unique logos (51 files across PNG/SVG/WebP) |
| Format | PNG only | WebP (used in code) + PNG + SVG backups |
| Total size | 597 KB | 1.8 MB (all variants) |
| New clients | — | Bain & Company, Colgate-Palmolive (promoted from logo-only) |
| Missing clients | Gain Theory (hidden) | Gain Theory (removed entirely) |
| Metadata | Content records with name, URL, date | Alt-text strings only (in TrustedBy.jsx) |
| Naming | Descriptive (`hello_fresh.png`) | Numbered (`c10.webp`) — opaque |

## Testimonials (Next.js Only)

Lektor has zero actual testimonials despite having a `testimonial` field on the client model and a dead `testimonial` flowblock. All testimonial content is in the Next.js repo, hardcoded in JSX.

### Homepage Testimonials (`components/home/Testimonials.jsx`)

6 client testimonials in a Swiper carousel ("What Our Clients Say"):

| # | Contact Name | Company | Title | Testimonial Length |
|---|-------------|---------|-------|--------------------|
| 1 | Iraklis Pappas | Colgate-Palmolive | Global Head of AI | 280 chars |
| 2 | Tarmo Juristo | SALK | CEO | 384 chars |
| 3 | Titi Alailima, MSE | Akili | VP of Applied Data | 303 chars |
| 4 | Manu Martinet, Phd | Indigo | Lead Data Scientist | 411 chars |
| 5 | Tim McWilliams | Ovative Group | Sr. Manager Data Science | 252 chars |
| 6 | Nathan Kafi | Haleon | Principal Data Scientist | 296 chars |

**Issues**:
- **Wrong profile images**: All 6 testimonials use PyMC team member headshots as placeholder images (e.g., `/users/benjamin-vincent.jpg` for 3 different people). Comment in code says "Replace with actual path."
- **New companies in testimonials**: SALK, Ovative Group, and Haleon are not in either site's client logo set.
- **Missing punctuation/spacing**: Several testimonials have sentences run together without spaces after periods (e.g., "our modeling and so my prior was that...So we got").

### Course Testimonials — Applied Bayesian Modeling (`app/courses/components/Testimonials.jsx`)

6 student testimonials in a Swiper carousel ("What Our Students are Saying"):

| # | Text (excerpt) | Name | Role |
|---|----------------|------|------|
| 1 | "The quality of instruction here was on a completely different level..." | Anjali Patel | Team Leader |
| 2 | "I had several mediocre attempts at using pymc before the course..." | Anjali Patel | Team Leader |
| 3 | "I recommend this course to anyone who wants to create Bayesian models..." | Anjali Patel | Team Leader |
| 4 | "I think the overall organization is great -- the lectures, course materials..." | Anjali Patel | Team Leader |
| 5 | "I have a much better appreciation of hierarchical modeling..." | Robert Fox | Web Designer |
| 6 | "Before the course I was only loosely familiar with Bayesian analysis..." | Liam Turner | Product Manager |

**Issues**:
- **Placeholder names/roles**: 4 of 6 testimonials use "Anjali Patel / Team Leader" — clearly placeholder attributions for real student quotes. "Robert Fox / Web Designer" and "Liam Turner / Product Manager" are likely also placeholders.
- **Placeholder images**: All use Unsplash stock photos. Name/avatar rendering is commented out in the JSX (lines 114-125).
- **2 testimonials commented out**: "Sophia Adams" and "Ava Martinez" entries are commented out in source.

### Course Testimonials — AI-Assisted Data Science (`app/courses/ai-assisted-data-science/AiTestimonials.jsx`)

5 testimonials with a different design (bento grid layout):

| # | Type | Name | Company/Logo | Content |
|---|------|------|-------------|---------|
| 1 | video | Ryan Kenter | AltForms | Thumbnail only (no actual video) |
| 2 | text | Gustavo Workman | Product. | "Akari helped us cut project delays by 40%..." |
| 3 | text | Martin Westervelt | Sitemark | Same "Akari" text |
| 4 | text | Livia Levin | luminous | Same "Akari" text |
| 5 | video | Sarah Mendez | AltForms | Thumbnail only |

**Issues**:
- **100% placeholder content**: All text testimonials reference "Akari" — a completely unrelated product. These are from a UI template.
- **Fake names and companies**: None of the names or companies (AltForms, Product., Sitemark, luminous) are real clients.
- **Non-functional video**: Video testimonials show a thumbnail but have no play functionality or video source.

## Case Studies

Neither site has case study content. No dedicated case study pages, templates, or content types exist in either repo.

## Cross-Site Client Inventory Summary

Combining both repos, the complete client universe is:

| # | Client | Lektor Record | Lektor Logo | Next.js Logo | Next.js Testimonial | Notes |
|---|--------|:---:|:---:|:---:|:---:|-------|
| 1 | Akili | Yes | Yes | Yes | Yes (Titi Alailima) | |
| 2 | Alva Labs | Yes | Yes | Yes | — | |
| 3 | Appgrowth | Yes | Yes | Yes | — | Undeclared `client` field |
| 4 | Appodeal | Yes | Yes | Yes | — | |
| 5 | Bain & Company | — | — | Yes | — | **Next.js only** |
| 6 | civiqs | Yes | Yes | Yes | — | Lowercase in Lektor |
| 7 | Colgate-Palmolive | — | Yes (orphan) | Yes | Yes (Iraklis Pappas) | No Lektor content record |
| 8 | Columbia University | Yes | Yes | Yes | — | |
| 9 | Everysk | Yes | Yes | Yes | — | Undeclared `client` field |
| 10 | Exemplar Tech | Yes | Yes | Yes | — | Slug typo: "Examplar" |
| 11 | Gain Theory | **Hidden** | Yes | — | — | Hidden in Lektor, absent from Next.js |
| 12 | Gates Foundation | Yes | Yes | Yes | — | Alt typo: "Melindia" |
| 13 | Haleon | — | — | — | Yes (Nathan Kafi) | **Testimonial only** |
| 14 | Hello Fresh | Yes | Yes | Yes | — | |
| 15 | Indigo Ag | Yes | Yes | Yes | Yes (Manu Martinet) | |
| 16 | Ovative Group | — | — | — | Yes (Tim McWilliams) | **Testimonial only** |
| 17 | Quoniam | Yes | Yes | Yes | — | |
| 18 | Redhawk | Yes | Yes | Yes | — | Alt typo: "Resarch" |
| 19 | Roche | Yes | Yes | Yes | — | |
| 20 | SALK | — | — | — | Yes (Tarmo Juristo) | **Testimonial only** |
| 21 | Sweeplift | Yes | Yes | Yes | — | |
| 22 | VisualVest | Yes | Yes | Yes | — | |

**Totals**: 22 unique clients across both sites
- 17 with Lektor content records (16 visible + 1 hidden)
- 18 with Next.js logos
- 6 with real testimonials (all Next.js only)
- 3 companies appear only in testimonials (Haleon, Ovative Group, SALK)
- 1 company appears only in Next.js logos (Bain & Company)

## Issues Summary

| # | Issue | Severity | Location |
|---|-------|----------|----------|
| 1 | Zero testimonials in Lektor despite model support | Data gap | `content/clients/*/contents.lr` |
| 2 | Ghost `_model: testimonials` on parent | Bug | `content/clients/contents.lr` |
| 3 | Orphan Colgate-Palmolive logo (no content record) | Data inconsistency | `assets/static/images/client_logos/colgate-palmolive.png` |
| 4 | Opaque numbered filenames (c1-c21) in Next.js | Maintainability | `public/clients/` |
| 5 | Alt-text typos: "Melindia" Gates, "Resarch" LLC | Quality | `app/courses/components/TrustedBy.jsx` |
| 6 | Slug typo: "examplar-tech" vs "exemplar" | Quality | `content/clients/examplar-tech/` |
| 7 | Wrong profile images on all 6 homepage testimonials | UX/Quality | `components/home/Testimonials.jsx` |
| 8 | 100% placeholder course testimonials (AI-Assisted DS) | Content gap | `app/courses/ai-assisted-data-science/AiTestimonials.jsx` |
| 9 | Placeholder names on Applied Bayesian testimonials | Content gap | `app/courses/components/Testimonials.jsx` |
| 10 | No alt-text on homepage Logos carousel | Accessibility | `components/home/Logos.jsx` |
| 11 | Duplicate logo assets (PNG + SVG + WebP for same logo) | Storage waste | `public/clients/` (1.8 MB) |
| 12 | 3 testimonial companies not in logo set | Data inconsistency | Haleon, Ovative Group, SALK |
| 13 | No case studies exist on either site | Content gap | Both repos |
| 14 | Client logos hardcoded in workshop template (bypasses CMS) | Architecture | `templates/applied-bayesian-modeling.html:283-297` |
| 15 | Dead `testimonial` flowblock in Lektor | Dead code | `flowblocks/testimonial.ini` |
| 16 | Mixed HTTP/HTTPS client URLs | Security | Exemplar Tech, Redhawk |
