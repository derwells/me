# Static Pages Catalog

Complete inventory of every standalone page across both PyMC Labs websites, excluding content already cataloged in blog-posts-catalog, team-members-catalog, clients-catalog, and courses-catalog.

## Summary

| Metric | Lektor | Next.js | Combined |
|--------|--------|---------|----------|
| Standalone pages | 10 | 14 deployed + 5 draft | 29 |
| CMS-managed content | 6 (flow blocks) | 0 | 6 |
| Hardcoded content | 4 (templates/forms) | 14 | 18 |
| Legal pages | 3 | 2 | 5 (3 overlap) |
| Redirected Lektor pages | — | 4 (what-we-do, impressum, products, clients) | — |

---

## Lektor Site — Standalone Pages

### 1. Homepage `/`

| Property | Value |
|----------|-------|
| **Content file** | `content/contents.lr` (8 lines) |
| **Model** | `index` (singleton) |
| **Template** | `templates/index.html` |
| **Fields** | `title: "PyMC Labs"`, `tagline: "The Bayesian Consultancy"`, `mission: "Bring Bayesian methods into wide practice."` |
| **Unused fields** | `pitch_deck` (HTML, empty in model), `description` (markdown, empty in model) |
| **Template content** | Hero image, value prop, YouTube embed, mission statement |
| **Data sources** | `databags/contact.json` → Thomas Wiecki / info@pymc-labs.com |
| **Integrations** | GA4 (G-F3RDLH8R8X), MathJax 2.7.5, Font Awesome 6.7.2 Kit 8cc267a9ab |

### 2. What We Do `/what-we-do/`

| Property | Value |
|----------|-------|
| **Content file** | `content/what-we-do/contents.lr` (178 lines) |
| **Model** | `generic_page` |
| **Template** | `templates/generic_page.html` |
| **Title** | "What we do" |
| **Flow blocks** | 8 `text` blocks + 1 `html` block (9 total) |
| **Sections** | Who we are, How Bayesian statistics can help (5 subsections), How we work with you (7-step process), Who we're here for, Curious to learn more? |
| **HTML block** | Google Slides iframe embed (pitch deck presentation) |
| **External links** | PyMC docs, PeerJ article, rt.live, twiecki.io blog, Calendly (no longer referenced) |
| **Note** | Redirected to `/` in Next.js (`next.config.mjs` line 29) |

### 3. Products `/products/`

| Property | Value |
|----------|-------|
| **Content file** | `content/products/contents.lr` (45 lines) |
| **Model** | `generic_page` |
| **Template** | `templates/generic_page.html` |
| **Title** | "Products" |
| **Flow blocks** | 3 `text` blocks |
| **Products listed** | CausalPy (causal inference), PyMC-Marketing (MMM + CLV) |
| **Images** | `casualpy-logo.jpg` (note typo: "casualpy" not "causalpy"), `pycmarketing-logo.jpg` (embedded in markdown) |
| **External links** | CausalPy ReadTheDocs, PyMC-Marketing docs, Calendly 30-min session (Niall Oulton) |
| **Note** | Redirected to `/#products` in Next.js (`next.config.mjs` line 69) |

### 4. Workshops (Listing) `/workshops/`

| Property | Value |
|----------|-------|
| **Content file** | `content/workshops/contents.lr` (81 lines) |
| **Model** | `generic_page` |
| **Template** | `templates/generic_page.html` |
| **Title** | "Corporate workshops" |
| **Flow blocks** | 5 `text` blocks |
| **Sections** | Overview, The workshops (format details), Student testimonials (4 anonymous blockquotes), Curious to learn more? |
| **Format details** | 2x 3-hour sessions/week over 3 weeks, Google Meet, Jupyter Notebooks via GitHub |
| **Levels** | Beginner, intermediate, advanced |
| **Images** | `workshop_banner.png` (commented out in HTML), `workshop_logos.png` |
| **Contact** | info@pymc-labs.com (no form, no Wise link on this page) |

### 5. Privacy Policy `/privacy-policy/`

| Property | Value |
|----------|-------|
| **Content file** | `content/privacy-policy/contents.lr` (108 lines) |
| **Model** | `generic_page` |
| **Template** | `templates/generic_page.html` |
| **Title** | "Privacy Policy" |
| **Flow blocks** | 9 `text` blocks |
| **Sections** | What personal data we collect, How we use it, Legal basis, Direct marketing, Sharing, International transfers, Retention, Your rights |
| **Legal entity** | PyMC Labs (no explicit company name — less specific than T&C) |
| **GDPR compliance** | Yes — right to access, erasure, restrict, object, portability, withdraw consent |
| **Missing** | No cookie policy details, no contact info at bottom (truncated), no DPO designation |

### 6. Impressum `/impressum/`

| Property | Value |
|----------|-------|
| **Content file** | `content/impressum/contents.lr` (35 lines) |
| **Model** | `generic_page` |
| **Template** | `templates/generic_page.html` |
| **Title** | "Impressum" |
| **Flow blocks** | 1 `text` block |
| **Language** | German (EU legal requirement for German-language markets) |
| **Legal entity** | PyMC OÜ (osaühing — Estonian private limited company) |
| **Address** | Parda 8, 10151 Tallinn, Estonia |
| **VAT ID** | EE102757468 |
| **Contact** | info@pymc-labs.com |
| **Disclaimers** | Liability for content, external links, copyright (section headers only, no full text) |
| **Note** | Redirected to `/about` in Next.js (`next.config.mjs` line 64) — legal content lost |

### 7. Terms and Conditions `/terms-and-conditions/`

| Property | Value |
|----------|-------|
| **Content file** | `content/terms-and-conditions/contents.lr` (135 lines) |
| **Model** | `generic_page` |
| **Template** | `templates/generic_page.html` |
| **Title** | "PyMC Labs Workshop Terms" |
| **Flow blocks** | 12 `text` blocks |
| **Sections** | Introduction, Registration & Payment, Workshop, Intellectual Property, Usage of Materials, Publishing online, Personal Data, Cancellation & Refunds, Liability, Governing Law, Miscellaneous |
| **Legal entity** | PyMC Labs ("the Company") |
| **Jurisdiction** | Estonia |
| **Refund policy** | Full refund if cancelled 7+ days before start; 14-day consumer right of withdrawal |
| **Delivery** | Google Meet (live online), recordings available |
| **Terminology** | Uses "Workshop" throughout (not "Course") |

### 8. Contact `/contact/`

| Property | Value |
|----------|-------|
| **Content file** | `content/contact/contents.lr` (empty — 0 bytes after `_model` line stripped) |
| **Model** | `contact` (collection parent, no custom fields) |
| **Template** | `templates/contact.html` |
| **Form** | Mailchimp embedded iframe |
| **Mailchimp details** | List ID `ffcf543278f48b79571b62010`, Form ID `cdca7f3ebb`, hosted at `us10.list-manage.com` |
| **Note** | Zero content in .lr file — everything is in the template |

### 9. Newsletter `/newsletter/`

| Property | Value |
|----------|-------|
| **Content file** | `content/newsletter/contents.lr` (1 line: `_model: testimonials`) |
| **Model declared** | `testimonials` (does not exist — ghost reference) |
| **Template** | `templates/newsletter.html` |
| **Form** | Mailchimp HTML form (native, not iframe) |
| **Mailchimp details** | Same list `ffcf543278f48b79571b62010` as contact form |
| **Anomaly** | `_model: testimonials` — model doesn't exist, Lektor falls back gracefully |

### 10. Sitemap `/sitemap/`

| Property | Value |
|----------|-------|
| **Content file** | `content/sitemap/contents.lr` (1 line: `_template: sitemap.html`) |
| **Model** | `page` (built-in) with template override |
| **Template** | `templates/sitemap.html` |
| **Content** | Dynamic — recursively lists all pages at build time |
| **Purpose** | Human-readable site map (separate from XML sitemap in `content/robots.txt`) |

### Lektor Navigation Structure

**Header nav** (from `databags/nav.json`):

| Item | Route | Icon |
|------|-------|------|
| What we do | `/what-we-do` | fa-info-circle |
| Products | `/products` | fa-shopping-cart |
| Team | `/team` | fa-user-friends |
| Clients | `/clients` | fa-microphone |
| Workshops | `/workshops` | fa-chalkboard-teacher |
| Blog | `/blog-posts` | fa-book-open |

**Footer nav** (from `databags/nav.json`):

| Item | URL | Icon |
|------|-----|------|
| Twitter | https://twitter.com/pymc_labs | fa-brands fa-twitter |
| GitHub | https://github.com/pymc-labs | fa-brands fa-github |
| LinkedIn | https://www.linkedin.com/company/pymc-labs/ | fa-brands fa-linkedin |
| YouTube | https://www.youtube.com/c/PyMCLabs | fa-brands fa-youtube |
| Meetup | https://www.meetup.com/pymc-labs-online-meetup/ | fa-brands fa-meetup |
| Newsletter | `/newsletter` | fa-solid fa-bell |
| Privacy Policy | `/privacy-policy` | fa-solid fa-lock |
| Impressum | `/impressum` | fa-solid fa-info-circle |

---

## Next.js Site — Standalone Pages

### 1. Homepage `/`

| Property | Value |
|----------|-------|
| **File** | `app/page.js` (18 lines) |
| **Component** | `HomeContent` (client-side) |
| **Metadata** | `createMetadata()` — "PyMC Labs \| Bayesian AI Consultancy for Advanced Modeling, AI Systems & Data Strategy" |
| **Data source** | Strapi (featured blogs), hardcoded testimonials (6), hardcoded client logos |
| **Key sections** | Hero video, logo carousel (TrustedBy), testimonials (Swiper), featured blogs, contact CTA |

### 2. About `/about`

| Property | Value |
|----------|-------|
| **File** | `app/about/page.jsx` (20 lines) |
| **Component** | `AboutContent` (client-side) |
| **Metadata** | `createMetadata()` — "PyMC Labs \| Inventors of PyMC & Experts in Bayesian AI Modeling" |
| **Data source** | Static/hardcoded |
| **Key sections** | Hero, About section, WhatWeDo, Innovation, Partners slider (from `libs/team.js`) |
| **Note** | New page — no equivalent in Lektor (closest: What We Do, but that's redirected to `/`) |

### 3. Team (Listing) `/team`

| Property | Value |
|----------|-------|
| **File** | `app/team/page.jsx` (65 lines) |
| **Component** | Server component (async) |
| **Metadata** | `createMetadata()` — "About PyMC Labs \| Creators of PyMC & Experts in Bayesian AI..." |
| **Data source** | Strapi REST API (`/api/teams?populate=*&filters[isVisible][$eq]=true`) |
| **Revalidation** | ISR, 60 seconds |
| **Key sections** | Hero with 3 rotating slides, Partners section, Team card grid, Client logos |
| **Components** | Hero, Partners, Logos, TeamCard |

### 4. Contact `/contact`

| Property | Value |
|----------|-------|
| **File** | `app/contact/page.js` (53 lines) |
| **Component** | `ContactFormPage` (client-side) |
| **Metadata** | `generateMetadata()` — "Contact PyMC Labs" (wrong domain: `pymc-labs.io` in OG URL) |
| **Data source** | Form submits to Strapi `/api/contact-form/submit` |
| **Key sections** | Hero with descriptive text, contact form (inquiry categories, discovery source) |
| **Email shown** | info@pymc-labs.com (in hero JSX) |
| **Bug** | OpenGraph URL uses `pymc-labs.io` instead of `pymc-labs.com` (line 34) |

### 5. Blog (Listing) `/blog-posts`

| Property | Value |
|----------|-------|
| **File** | `app/blog-posts/page.jsx` (17 lines) |
| **Component** | `BlogContent` (client-side) |
| **Metadata** | `createMetadata()` — "PyMC Labs Blog \| Tutorials, Case Studies & Applied Bayesian Analytics" |
| **Data source** | Strapi API with client-side pagination (48/page), category filter, search |

### 6. Blog Category Filter `/blog-posts/filters/[category]`

| Property | Value |
|----------|-------|
| **File** | `app/blog-posts/filters/[category]/page.jsx` |
| **Component** | `BlogContent` with category pre-filter |
| **Data source** | Strapi (client-side filtering) |

### 7. Draft Blog Preview `/draft-post/[id]`

| Property | Value |
|----------|-------|
| **File** | `app/draft-post/[id]/page.jsx` |
| **Rendering** | Server-side |
| **Data source** | Strapi (filters for `status=draft`) |
| **Note** | Preview-only route, not indexed. No authentication required (security concern). |

### 8. Privacy Policy `/privacy-policy`

| Property | Value |
|----------|-------|
| **File** | `app/privacy-policy/page.jsx` (15 lines) → `components/privacy-policy/PrivacyPolicyContent.jsx` (208 lines) |
| **Component** | `PrivacyPolicyContent` (client-side, framer-motion) |
| **Metadata** | `createMetadata()` — "Privacy Policy \| PyMC Labs" |
| **Sections** | Data collection, How we use it, Legal basis, Sharing, International transfers, Retention, Your rights |
| **Missing vs Lektor** | No "Direct marketing" section, no workshop/course registration data mention |
| **Bug** | Stray `f` character at line 30 of PrivacyPolicyContent.jsx (JSX attribute position — may cause hydration warning) |

### 9. Terms and Conditions `/terms-and-conditions`

| Property | Value |
|----------|-------|
| **File** | `app/terms-and-conditions/page.jsx` (447 lines — all hardcoded JSX) |
| **Component** | Inline (no separate component file) |
| **Rendering** | `"use client"` with framer-motion animations |
| **Sections** | Introduction, Registration & Payment, Course, IP, Usage of Materials, Publishing online, Personal Data, Cancellation & Refunds, Liability, Governing Law, Miscellaneous |
| **Terminology** | Uses "Course" throughout (Lektor uses "Workshop") |
| **Components** | DynamicHero, Layout, motion.h3 for each section |
| **Content** | Substantively identical legal text to Lektor, just reformatted as JSX with animation delays |

### 10. Certificate Verification `/verify/[id]`

| Property | Value |
|----------|-------|
| **File** | `app/verify/[id]/page.js` (79 lines) |
| **Rendering** | Server component (async) |
| **Data source** | Strapi API (`/api/certificates/verify/${id}`) |
| **Metadata** | Dynamic — "Certificate for {AttendeeName} - {WorkshopTitle}" with OpenGraph images |
| **Component** | `CertificateVerificationClient` |
| **Features** | Structured data (certificate: recipient, workshop, completion_date, issuer, verified) |
| **Bug** | `console.log('Certificate Data:', certificateData)` in production (line 77) |

### 11. Congratulations (Payment Success) `/congratulations`

| Property | Value |
|----------|-------|
| **File** | `app/congratulations/page.js` (16 lines) |
| **Component** | `CongratulationsContent` |
| **Metadata** | `robots: { index: false, follow: false }` (noindex) |
| **Purpose** | Stripe/payment success callback page |

### 12. Cancel (Payment Cancellation) `/cancel`

| Property | Value |
|----------|-------|
| **File** | `app/cancel/page.js` (16 lines) |
| **Component** | `CancelContent` |
| **Metadata** | `robots: { index: false, follow: false }` (noindex) |
| **Purpose** | Stripe/payment cancellation callback page |

### 13. LLM Price Is Right Benchmark `/benchmark/LLMPriceIsRight`

| Property | Value |
|----------|-------|
| **File** | `app/benchmark/LLMPriceIsRight/page.jsx` (28 lines) |
| **Component** | `LLMPriceContent` (self-contained mini-app) |
| **Metadata** | `createMetadata()` — "LLM Price Estimation Benchmark \| Test Real-World Pricing, Strategy & Business Insights" |
| **OG Image** | Cloudinary-hosted thumbnail (`dhgr6mghh` account) |
| **Data source** | Local JSON (`utils/leaderboard.json`, `utils/llmBenchmarkData.js`) |
| **Sub-routes** | `/leaderboard`, `/add-model` |

### 14. Benchmark Leaderboard `/benchmark/LLMPriceIsRight/leaderboard`

| Property | Value |
|----------|-------|
| **File** | `app/benchmark/LLMPriceIsRight/leaderboard/page.jsx` (307 lines) |
| **Rendering** | `"use client"` |
| **Data source** | `utils/llmBenchmarkData.js` (static), `utils/UpdateDates` |
| **Features** | Chart.js bar chart + scatter plot, 3 metrics (Elo, MAPE, Overbid Rate), provider color coding |
| **Libraries** | Chart.js, react-chartjs-2, chartjs-plugin-datalabels, lucide-react (ArrowLeft icon) |
| **Note** | No metadata export — relies on parent layout `generateTitle()` fallback |

### 15. Benchmark Add Model `/benchmark/LLMPriceIsRight/add-model`

| Property | Value |
|----------|-------|
| **File** | `app/benchmark/LLMPriceIsRight/add-model/page.jsx` (21 lines) |
| **Component** | `AddModalContent` |
| **Metadata** | `createMetadata()` — "Submit Your LLM for Price Benchmark Testing" |
| **Purpose** | Form for submitting new LLM models to benchmark |

### Draft Routes (in `draft/` directory, NOT deployed)

5 pages parked outside `app/` — not accessible via routing:

| Route (intended) | File | Purpose |
|-------------------|------|---------|
| `/industries` | `draft/industries/page.jsx` | Industries listing |
| `/industries-detail/[id]` | `draft/industries-detail/page.jsx` | Industry detail |
| `/services` | `draft/services/page.jsx` | Services listing |
| `/service-detail/[id]` | `draft/service-detail/page.jsx` | Service detail |
| `/solutions` | `draft/solutions/page.jsx` | Solutions page |

Components exist in `components/industries/` and `components/services/` but are unreachable.

### Next.js Global Layout & Infrastructure

**Root Layout** (`app/layout.js`, 105 lines):
- `"use client"` directive (anti-pattern — disables server metadata generation)
- Fonts: Roboto + Inter (Google Fonts, 4 weights each)
- `generateTitle()` — fallback title generator based on pathname (8 hardcoded paths + slug-based fallback)
- Organization JSON-LD on every page (Schema.org)
- GTM via `NEXT_PUBLIC_GTM_ID`
- HubSpot tracking script (`50315116`)
- Bing Webmaster verification (`BA24037511ADB1040EEF597B103472EF`)
- Font Awesome 6.7.2 via CDN
- Swiper CSS imports at root level
- `ClientProvider` wraps all children

**Redirects** (`next.config.mjs`):

| Source | Destination | Type |
|--------|-------------|------|
| `/what-we-do` | `/` | Permanent |
| `/impressum` | `/about` | Permanent |
| `/products` | `/#products` | Permanent |
| `/clients` | `/#clients` | Permanent |
| `/team/:id` | `/team-detail/:id` | Permanent |
| HTTP → HTTPS | `https://www.pymc-labs.com/...` | Permanent |
| Non-www → www | `https://www.pymc-labs.com/...` | Permanent |

**Sitemap**: Pre-generated XML files in `public/` (`sitemap.xml`, `sitemap-0.xml`) — not dynamically generated from Next.js sitemap API.

**Missing infrastructure**: No `robots.txt` route handler, no `not-found.jsx`, no error boundary pages, no `loading.jsx` files.

---

## Cross-Site Page Comparison

### Pages Present in Both Sites

| Page | Lektor Route | Next.js Route | Content Sync |
|------|-------------|---------------|--------------|
| Homepage | `/` | `/` | Different — Lektor is minimal hero+mission; Next.js has video hero, testimonials, featured blogs |
| Team listing | `/team/` | `/team` | Different data sources (Lektor .lr vs Strapi API) |
| Contact | `/contact/` | `/contact` | Different — Mailchimp iframe vs Strapi form submission |
| Blog listing | `/blog-posts/` | `/blog-posts` | Different — Lektor static vs Strapi-backed with search/filter |
| Privacy Policy | `/privacy-policy/` | `/privacy-policy` | Similar text but Next.js version is shorter (missing Direct Marketing, workshop data sections) |
| Terms & Conditions | `/terms-and-conditions/` | `/terms-and-conditions` | Same legal text, different terminology ("Workshop" vs "Course") |
| Workshops/Courses | `/workshops/` | `/courses` | Different — Lektor is generic pitch; Next.js has 4 detailed course pages |

### Pages Only in Lektor

| Page | Route | Fate in Next.js |
|------|-------|-----------------|
| What We Do | `/what-we-do/` | Redirected to `/` |
| Products | `/products/` | Redirected to `/#products` (anchor on homepage) |
| Impressum | `/impressum/` | Redirected to `/about` — **legal content lost** |
| Newsletter | `/newsletter/` | No equivalent route — newsletter in Footer component instead |
| Sitemap | `/sitemap/` | Pre-generated XML only — no human-readable sitemap |
| Clients listing | `/clients/` | Redirected to `/#clients` (anchor on homepage) |

### Pages Only in Next.js

| Page | Route | Purpose |
|------|-------|---------|
| About | `/about` | Company overview (no Lektor equivalent) |
| Certificate verification | `/verify/[id]` | Course completion certificates |
| Congratulations | `/congratulations` | Payment success (noindex) |
| Cancel | `/cancel` | Payment cancellation (noindex) |
| LLM Benchmark | `/benchmark/LLMPriceIsRight` | Interactive benchmark tool (3 sub-routes) |
| Benchmark Leaderboard | `/benchmark/LLMPriceIsRight/leaderboard` | Chart.js visualizations |
| Benchmark Add Model | `/benchmark/LLMPriceIsRight/add-model` | Model submission form |
| Draft Blog Preview | `/draft-post/[id]` | Unauthenticated draft preview |
| Blog Category Filter | `/blog-posts/filters/[category]` | Category-based listing |

---

## Issues Found

1. **Impressum legal content lost in redirect** — Next.js redirects `/impressum` → `/about`, which contains no legal entity info, VAT ID, or address. German law requires Impressum for commercial websites targeting German users. PyMC OÜ being Estonian-registered doesn't exempt them.

2. **Privacy Policy divergence** — Lektor version has 9 sections including Direct Marketing and workshop/course registration data handling. Next.js version has only 7 sections, missing these critical clauses. Neither mentions cookie consent banners or specific third-party data processors (Strapi, Cloudinary, HubSpot, GTM).

3. **Terms terminology mismatch** — Lektor says "Workshop", Next.js says "Course". Both refer to the same offerings. Should be consistent for legal clarity.

4. **Contact page wrong domain** — Next.js contact page has `pymc-labs.io` in OpenGraph metadata (line 34 of `app/contact/page.js`).

5. **No `not-found.jsx`** — Next.js site has no custom 404 page. Users hitting bad URLs get default Next.js error page.

6. **No error boundaries** — No `error.jsx` files anywhere in the Next.js app directory.

7. **No `loading.jsx`** — No loading states for server-rendered pages (team listing, blog detail, certificate verification).

8. **Root layout as client component** — `"use client"` on `app/layout.js` is an anti-pattern that disables automatic server-side metadata for child routes. Each page must export its own metadata since the layout can't use `generateMetadata()`.

9. **Stray character in PrivacyPolicyContent** — Line 30 of `components/privacy-policy/PrivacyPolicyContent.jsx` has a stray `f` after `animate={{ opacity: 1 }}` that may cause JSX parsing issues or hydration warnings.

10. **Pre-generated sitemap** — `public/sitemap.xml` and `public/sitemap-0.xml` are static files, not dynamically generated. New pages/blog posts won't appear in the sitemap unless manually regenerated.

11. **Leaderboard page missing metadata** — `/benchmark/LLMPriceIsRight/leaderboard` has no metadata export; it relies on root layout's `generateTitle()` which produces a generic title.

12. **console.log in production** — Certificate verification page (`app/verify/[id]/page.js` line 77) logs certificate data to console.

13. **Unauthenticated draft preview** — `/draft-post/[id]` fetches draft articles from Strapi with no authentication, allowing anyone to read unpublished content.

14. **Products page typo** — Lektor `content/products/` references `casualpy-logo.jpg` (missing the "u" in "causal").

15. **Newsletter ghost model** — Lektor `content/newsletter/contents.lr` declares `_model: testimonials` which doesn't exist.

16. **Twitter social link outdated** — Lektor footer nav links to `twitter.com/pymc_labs` (now X.com). Next.js links to `x.com` in some places but not consistently.
