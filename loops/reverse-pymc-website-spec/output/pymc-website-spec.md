# PyMC Labs Website — Unified As-Is Specification

> **Generated:** 2026-03-07
> **Source analysis:** 18 aspects across 4 waves (Data Acquisition, Architecture Analysis, Content Audit, Media Assets Audit)
> **Repositories analyzed:**
> - `pymc-labs/pymc-labs-website-source` — Production Lektor static site
> - `pymc-labs/pymc-rebranded-website` — In-progress Next.js + Strapi rewrite

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Overview](#2-architecture-overview)
3. [Lektor Site (Production)](#3-lektor-site-production)
4. [Next.js Site (Rebranded)](#4-nextjs-site-rebranded)
5. [Strapi CMS Backend](#5-strapi-cms-backend)
6. [Third-Party Integrations](#6-third-party-integrations)
7. [Content Inventory](#7-content-inventory)
8. [Media Assets](#8-media-assets)
9. [Dependency & Security Audit](#9-dependency--security-audit)
10. [Cross-Site Comparison](#10-cross-site-comparison)
11. [Issues Registry](#11-issues-registry)
12. [Redesign Considerations](#12-redesign-considerations)

---

## 1. Executive Summary

PyMC Labs operates two website codebases in parallel:

1. **Lektor site** (`pymc-labs-website-source`) — The current production site at `www.pymc-labs.com`, a Python-based static site generator using Jinja2 templates, Bootstrap 4, and `.lr` content files. Deployed to GitHub Pages via force-orphan push. **CI is broken** (references deleted `requirements.txt`), serving stale content from the last successful deploy.

2. **Next.js site** (`pymc-rebranded-website`) — An in-progress rewrite using Next.js 16, React 19, Tailwind CSS, and a Strapi v4 CMS backend on Heroku. Not yet in production. Has **zero CI/CD**, **zero tests**, and **39 npm audit vulnerabilities** (2 critical).

### Key Numbers

| Metric | Lektor | Next.js | Combined |
|--------|--------|---------|----------|
| Content items | 97 (52 blog, 26 team, 18 client, 1 course) | 29 hardcoded team + Strapi DB | ~126+ |
| Page routes | 17 | 22 + 1 API + 5 draft | 45 |
| Components/templates | 22 templates + 4 macros + 4 flowblocks | 80 component files | ~110 |
| Local media files | 352 (134 MB) | 174 (31 MB) | 526 (165 MB) |
| Third-party services | 8 | 14 | 17 unique |
| Known vulnerabilities | 5+ Python CVEs + EOL CDN libs | 39 npm audit (2 critical, 31 high) | 44+ |
| Test coverage | 0% | 0% | 0% |
| CI/CD status | Broken | Absent | Non-functional |

### Critical Findings

1. **Broken production CI** — Lektor deploy workflow references deleted `requirements.txt`. Site serves stale content.
2. **Zero authentication** — All 16 Strapi endpoints are unauthenticated. Draft blogs, certificate state mutation, and API key submissions are publicly accessible.
3. **Dual data sources** — Team members exist in both hardcoded JS (29 members) and Strapi CMS with only 8 overlapping. Content will inevitably drift.
4. **100% hardcoded courses** — All 4 Next.js course pages are hardcoded JSX. No CMS integration for the primary revenue-generating content.
5. **Critical vulnerabilities** — jspdf (8 CVEs), swiper (prototype pollution), axios (prototype pollution), mistune 0.8 (multiple CVEs).
6. **No Strapi source code** — The CMS backend is deployed separately on Heroku with no source in the repo. Data models are reverse-engineered from frontend API calls.

---

## 2. Architecture Overview

### 2.1 Lektor Site Architecture

```
Browser → GitHub Pages (pymc-labs.github.io)
           ↓ CNAME: www.pymc-labs.com
           Static HTML/CSS/JS

Build:    Lektor (Python) → HTML → force-orphan push to gh-pages
Content:  .lr files in content/ directory (file-based CMS)
Media:    Local files in assets/static/ and content/ attachments
CI:       GitHub Actions (BROKEN — references deleted requirements.txt)
Preview:  Netlify PR previews (also broken)
```

### 2.2 Next.js Site Architecture

```
Browser → Next.js App (not yet deployed to production)
           ↓
           App Router (22 routes)
           ↓
           Strapi v4 REST API (Heroku)
           ↓
           Cloudinary (2 accounts) for media

Framework: Next.js 16 + React 19 (App Router, no TypeScript)
Backend:   Strapi on Heroku (pymc-backend-afc5c26e8ab7.herokuapp.com)
Media:     Cloudinary (dx3t8udaw, dhgr6mghh) + local public/ files
CI:        None
```

### 2.3 Domain & DNS

| Property | Value |
|----------|-------|
| Production domain | `www.pymc-labs.com` |
| DNS target | GitHub Pages (`pymc-labs.github.io`) |
| HTTPS enforced | **No** (`https_enforced: false`) |
| Canonical URL in Lektor | `https://pymc-labs.github.io/` (mismatch) |
| Wrong domain references | `pymc-labs.io` in Next.js contact + team JSON-LD |

---

## 3. Lektor Site (Production)

### 3.1 Tech Stack

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.9 (pixi) / 3.8 (CI) | **Both EOL** |
| Lektor | 3.3.12 | Current |
| Flask | 2.3.1 | **EOL** |
| Jinja2 | 3.1.2 | CVE-2024-34064 |
| Werkzeug | 2.3.0 | **EOL** |
| Mistune | 0.8.4 | **EOL/Critical** (multiple CVEs) |
| Bootstrap | 4.5.2 (CDN) | **EOL** (Jan 2023) |
| jQuery | 3.5.1 (CDN) | Outdated |
| MathJax | 2.7.5 (CDN) | **EOL** (since 2020) |
| Font Awesome | 6.7.2 (CDN) | Current |

### 3.2 Data Models (10 models)

| Model | Type | Items | Key Fields |
|-------|------|-------|------------|
| `index` | Singleton | 1 | title, tagline, mission |
| `blog_posts` / `blog_post` | Collection | 52 | title, authors (checkboxes), date, summary, blog_post (markdown), youtube_video, visible |
| `team` / `teammate` | Collection | 26 | name, social URLs (5), specializations, location, blurb, extended_bio, visible |
| `clients` / `client` | Collection | 18 | client_name, testimonial (all empty), logo_filename, date, homepage_url |
| `generic_page` | Page | 6 | title, content (flow: text, image, html blocks) |
| `contact` | Parent | 1 | (empty — form in template) |
| `newsletter` | Parent | 1 | (ghost `_model: testimonials` reference) |

**Content format:** `.lr` files with `---` field delimiters. Flow blocks use `####` syntax with `----` sub-delimiters.

**Schema issues:**
- Blog post `authors` field uses hardcoded checkboxes (13 names) but content has 26 unique free-text values
- `testimonial` flowblock exists but is not whitelisted in any flow field (dead code)
- `picture` field on 10 teammates is undeclared in model (silently ignored)
- Ghost `_model: testimonials` references on `clients/` and `newsletter/` parents

### 3.3 Templates & Rendering

- **22 templates:** 13 page templates, 4 macros, 4 block templates, 1 sitemap
- **4 flowblocks:** text, image, html, testimonial (testimonial is unusable)
- **2 databags:** `nav.json` (6 header + 8 footer items), `contact.json` (Thomas Wiecki, info@pymc-labs.com)
- **4 plugins:** 3 community (header-anchors, highlighter, tags) + 1 custom (collapsible-code)
- **Workshop page** (`applied-bayesian-modeling.html`) is fully hardcoded HTML — not CMS-driven

### 3.4 Route Map (17 routes)

| Route | Template | Content Source |
|-------|----------|---------------|
| `/` | `index.html` | CMS (index model) |
| `/what-we-do/` | `generic_page.html` | CMS (flow blocks) |
| `/products/` | `generic_page.html` | CMS (flow blocks) |
| `/team/` | `team.html` | CMS (collection listing) |
| `/team/<slug>/` | `teammate.html` | CMS (individual record) |
| `/clients/` | `clients.html` | CMS (collection listing) |
| `/clients/<slug>/` | `client.html` | CMS (individual record) |
| `/workshops/` | `generic_page.html` | CMS (flow blocks) |
| `/workshops/applied-bayesian-modeling/` | `applied-bayesian-modeling.html` | **Hardcoded template** |
| `/blog-posts/` | `blog_posts.html` | CMS (collection listing, no pagination) |
| `/blog-posts/<slug>/` | `blog_post.html` | CMS (individual record) |
| `/contact/` | `contact.html` | Mailchimp iframe |
| `/newsletter/` | `newsletter.html` | Mailchimp HTML form |
| `/privacy-policy/` | `generic_page.html` | CMS (flow blocks) |
| `/impressum/` | `generic_page.html` | CMS (flow blocks) |
| `/terms-and-conditions/` | `generic_page.html` | CMS (flow blocks) |
| `/sitemap/` | `sitemap.html` | Dynamic (recursive listing) |

### 3.5 Build & Deploy

- **Build:** `lektor build` via Pixi (conda-forge)
- **Deploy:** `peaceiris/actions-gh-pages@v3` force-orphan push to `pymc-labs/pymc-labs.github.io`
- **Preview:** Netlify PR previews via `nwtgck/actions-netlify@v1.1`
- **Auth:** PAT-based (`GHPAGES_TOKEN`)
- **Status:** **BROKEN** — `requirements.txt` deleted during Pixi migration, CI never updated
- **All 6 GitHub Actions on v2** (current: v4/v5), running on Node 12 EOL runners

---

## 4. Next.js Site (Rebranded)

### 4.1 Tech Stack

| Component | Version | Status |
|-----------|---------|--------|
| Next.js | 16.0.10 | Current (3 high vulns in self-hosted configs) |
| React | 19.2.3 | Current |
| Tailwind CSS | 3.4.19 | Outdated (4.0 available) |
| framer-motion | 11.18.2 | Current (pervasive — ~30 components) |
| axios | 1.13.2 | **Vulnerable** (prototype pollution) |
| jspdf | 3.0.4 | **Critical** (8 CVEs) |
| swiper | 11.2.10 | **Critical** (prototype pollution) |
| Node.js | >=20.9.0 | Current |

**No TypeScript. No tests. No CI/CD.**

### 4.2 Route Map (22 pages + 1 API + 5 draft)

#### Static Pages

| Route | Data Source | Rendering |
|-------|------------|-----------|
| `/` | Strapi (client-side) + hardcoded | Client |
| `/about` | Static/hardcoded | Client |
| `/contact` | Form → Strapi | Client |
| `/courses` | Strapi (client-side) | Client |
| `/blog-posts` | Strapi (client-side, paginated) | Client |
| `/privacy-policy` | Hardcoded JSX | Client |
| `/terms-and-conditions` | Hardcoded JSX (447 lines) | Client |
| `/cancel` | Static (noindex) | Client |
| `/congratulations` | Static (noindex) | Client |
| `/benchmark/LLMPriceIsRight` | Local JSON | Client |
| `/benchmark/.../leaderboard` | Local JSON + Chart.js | Client |
| `/benchmark/.../add-model` | Form → Strapi | Client |

#### Dynamic Pages

| Route | Data Source | Rendering |
|-------|------------|-----------|
| `/blog-posts/[id]` | Strapi | Server |
| `/blog-posts/filters/[category]` | Strapi | Client |
| `/draft-post/[id]` | Strapi (draft, **no auth**) | Server |
| `/team` | Strapi (ISR/60s) | Server |
| `/team-detail/[id]` | Strapi (ISR/60s) | Server |
| `/verify/[id]` | Strapi | Server |

#### Hardcoded Course Pages

| Route | Price | Instructors | Status |
|-------|-------|-------------|--------|
| `/courses/applied-bayesian-modeling` | $1,499/$1,699 | Downey, Leos Barajas, Fonnesbeck | Waiting list |
| `/courses/applied-bayesian-regression-modeling` | $1,499/$1,699 | Orduz, Vincent, Forde | Waiting list |
| `/courses/bayesian-marketing-analytics` | $2,249/$2,499 | McWilliams, Trujillo, Vincent, Allen | Waiting list |
| `/courses/ai-assisted-data-science` | $2,000 | Bowne-Anderson, Wiecki, Fiaschi | Waiting list |

#### Redirects (from `next.config.mjs`)

| Source | Destination | Type |
|--------|-------------|------|
| `/what-we-do` | `/` | Permanent |
| `/impressum` | `/about` (legal content lost) | Permanent |
| `/products` | `/#products` | Permanent |
| `/clients` | `/#clients` | Permanent |
| `/team/:id` | `/team-detail/:id` | Permanent |
| HTTP | HTTPS | Permanent |
| Non-www | www | Permanent |

### 4.3 Component Architecture

**80 component files** across 12 subdirectories. Feature-first flat structure with low reuse.

| Directory | Files | Purpose |
|-----------|-------|---------|
| `layout/` | 2 | Navbar, Footer |
| `shared/` | 11 | Layout, Hero variants, ContactUs, FAQ, Pagination, Partners, Slider |
| `ui/` | 3 | Button, Card3D, CardHover |
| `home/` | 13 | Homepage sections (Hero, Testimonials, Logos, FeaturedBlogs) |
| `blog/` | 11 | Blog listing/detail (BlogContent, BlogCard, Filter, Pagination, Newsletter) |
| `contact/` | 4 | 3 different contact form implementations |
| `team/` | 2 | TeamCard, TeamDetails |
| `courses/` | 1 | CoursesContent |
| `about/` | 3 | About page sections |
| `benchmark/` | 11 | LLM Price Is Right (self-contained mini-app) |
| `industries/` | 5 | Draft (unused) |
| `services/` | 6 | Draft (unused) |
| `Payments/` | 2 | Stripe cancel/success pages |
| `privacy-policy/` | 1 | PrivacyPolicyContent |

**Key architectural issues:**
1. `"use client"` on root layout — entire app is client-rendered
2. 3-4 duplicate contact form implementations
3. 3 icon libraries loaded simultaneously (FA CDN + lucide-react + react-icons)
4. framer-motion dependency in ~30 components
5. No error boundaries, no `not-found.jsx`, no `loading.jsx`
6. Typos in component names: `ContentVedio`, `DunamicCard`, `Inovation`, `Congratulationscontent`
7. `dangerouslySetInnerHTML` usage, `console.log` in production code
8. Placeholder FAQ content from payment gateway template ("Instapay", "ACME")

### 4.4 Data Fetching

**Dual fetch patterns:**
1. `GetApiData()` — Axios wrapper in `libs/http-client.js` (client-side calls)
2. Direct `fetch()` — Native fetch with ISR revalidation (server-side team pages)

**Auth:** Token-based (`x-access-token`) mechanism exists in `libs/auth.utils.js` but all API calls pass `secured=false`.

**Environment variables:**

| Variable | Purpose |
|----------|---------|
| `NEXT_PUBLIC_STRAPI_URL` | Strapi backend URL (exposed to client) |
| `NEXT_PUBLIC_SITE_URL` | Canonical site URL |
| `NEXT_PUBLIC_GTM_ID` | Google Tag Manager ID |
| `NEXT_PUBLIC_BASE_URL` | Certificate verification base URL |

No `.env.example` file exists.

---

## 5. Strapi CMS Backend

### 5.1 Deployment

| Property | Value |
|----------|-------|
| Hosting | Heroku (`pymc-backend-afc5c26e8ab7.herokuapp.com`) |
| API style | Strapi v4 REST |
| Media | Cloudinary (2 accounts) |
| Source code | **Not in repository** — deployed separately |
| Auth | Token-based, but **all endpoints called unauthenticated** |

### 5.2 Content Types (11 reverse-engineered)

#### Core Collections

| Content Type | Fields | Relations | Notes |
|-------------|--------|-----------|-------|
| `article` | 18 (title, slug, description, detail, cover, video, featured, blog_created_date, meta_title, meta_description, status) | categories (M2M), authors (M2M), cover (media) | Primary blog content |
| `team` | 16 (name, slug, desc, bio, partner, isVisible, orderNumber, location, social links) | specializations (relation), profile_image (media) | Bio stored as JSON string array |
| `certificate` | 7 (AttendeeName, Email, WorkshopTitle, CompletionDate, VerifyId, CertificateImage) | — | PascalCase fields (non-standard) |
| `category` | 3 (name, slug, blogs relation) | blogs (M2M to articles) | Blog categories |
| `author` | 2 (id, name) | articles (M2M) | Minimal — name only |

#### Form Collections

| Content Type | Fields | Notes |
|-------------|--------|-------|
| `contact-user` | 4 (firstName, lastName, email, message) | Legacy, has rate limiting |
| `contact-form` | 7 (firstName, lastName, email, phoneNumber, message, inquiryCategory, discoverySource) | Newer, custom `/submit` route |
| `registration-form` | 9 (name, email, role, organization, message, termsAccepted, heardFrom, workshopType, clientId) | Returns Wise payment URL |

#### Utility Collections

| Content Type | Fields | Notes |
|-------------|--------|-------|
| `coupon` | 4 (title, discount, wiseLink, match) | Promo code validation |
| `promotion-bar` | Unknown | Site-wide banner |
| `benchmark` | 4 (modelName, apiUrl, apiKey, description) | LLM model submissions (**API keys in plaintext**) |

### 5.3 API Endpoints (16 unique)

#### Standard CRUD (9)

| Endpoint | Method | Used For |
|----------|--------|----------|
| `GET /api/articles` | GET | Blog listing (paginated, filtered, sorted) |
| `GET /api/articles?filters[slug][$eq]=X&populate=*` | GET | Single blog by slug |
| `GET /api/articles?status=draft` | GET | Draft preview (**no auth**) |
| `GET /api/categories` | GET | Blog category listing |
| `GET /api/teams?populate=*&filters[isVisible][$eq]=true` | GET | Team listing (ISR/60s) |
| `GET /api/teams?filters[slug][$eq]=X&populate=*` | GET | Single team member (ISR/60s) |
| `POST /api/contact-users` | POST | Legacy contact form (rate limited) |
| `GET /api/promotion-bars` | GET | Promotional banner |
| `GET /api/articles?filters[featured][$eq]=true` | GET | Featured blog posts |

#### Custom Routes (7)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `GET /api/certificates/verify/:id` | GET | Public certificate verification |
| `GET /api/certificates/email/:email` | GET | Certificate lookup by email |
| `PUT /api/certificates/:id/download` | PUT | Track download (**unauthenticated state mutation**) |
| `POST /api/contact-form/submit` | POST | Contact form with inquiry categories |
| `POST /api/registration-form/submit` | POST | Course registration, returns payment URL |
| `POST /api/coupons/validate-title` | POST | Promo code validation |
| `POST /api/benchmark/submit` | POST | LLM model submission (**plaintext API keys**) |

---

## 6. Third-Party Integrations

### 6.1 Complete Integration Inventory (17 services)

| # | Service | Category | Lektor | Next.js | Status |
|---|---------|----------|:------:|:-------:|--------|
| 1 | Wise.com | Payment | Hardcoded link | Dynamic server-generated | Active |
| 2 | Stripe | Payment | - | Partial (result pages only) | Incomplete |
| 3 | Mailchimp | Email | HTML form + iframe | JSONP (deprecated) | Active |
| 4 | Google Analytics 4 | Analytics | Direct (`G-F3RDLH8R8X`) | Via GTM | Active |
| 5 | Google Tag Manager | Analytics | - | Yes | Active |
| 6 | HubSpot | CRM | - | Yes (`50315116`) | Active |
| 7 | Bing Webmaster | SEO | - | Meta tag | Active |
| 8 | Strapi CMS | Backend | - | Heroku | Active |
| 9 | Cloudinary | Image CDN | - | 2 accounts | Active |
| 10 | Heroku | Hosting | - | Strapi backend | Active |
| 11 | GitHub Pages | Hosting | Production | - | Active |
| 12 | Netlify | Hosting | PR previews | - | Active |
| 13 | YouTube | Video | Embeds (158 URLs) | 3 embeds | Active |
| 14 | Font Awesome | Icons | CDN | CDN + npm (2 more icon libs) | Active |
| 15 | MathJax | Math | 2.7.5 (CDN) | - | **EOL** |
| 16 | KaTeX | Math | - | npm | Active |
| 17 | Marimo | Notebooks | - | public/ dir | Unclear |

### 6.2 Migration Summary (Lektor to Next.js)

| Category | Lektor | Next.js | Assessment |
|----------|--------|---------|------------|
| Payment | Hardcoded Wise link | Dynamic Wise via Strapi | Improved |
| Newsletter | HTML form | JSONP injection | **Regressed** (security) |
| Contact | Mailchimp iframe | 3 duplicate Strapi forms | Mixed |
| Analytics | GA4 only | GTM + GA4 + HubSpot + Bing | Expanded |
| CMS | File-based (self-contained) | Strapi on Heroku | More capable, adds dependency |
| Icons | 1 library | 3 libraries | **Regressed** (bloated) |
| Math | MathJax 2 (EOL) | KaTeX | Improved |
| CSS | Bootstrap 4 (EOL) | Tailwind 3.4 | Improved |
| Social | Mastodon | Bluesky | Platform shift |

---

## 7. Content Inventory

### 7.1 Blog Posts

**Lektor:** 52 posts (2021-02 to 2025-06), all visible, stored as `.lr` files with attached images.
**Next.js/Strapi:** Blog content in Strapi DB (not in repo). Must be exported via API.

| Metric | Lektor | Next.js/Strapi |
|--------|--------|----------------|
| Post count | 52 | Unknown (Strapi DB) |
| Date range | 2021-02 to 2025-06 | Unknown |
| Video posts | 14 (27%) | Supported |
| With summaries | 30 (58%) | `description` field |
| Categories | None (tags plugin unused) | Yes (M2M relation) |
| Pagination | None (all on one page) | Yes (server-side) |
| Search | None | Client-side title search |
| Draft preview | None | `/draft-post/[id]` (no auth) |
| Images | 276 files, 115 MB (80% PNG) | Cloudinary |

**Top authors (Lektor):** Thomas Wiecki (12), Benjamin Vincent (8), Juan Orduz (4), Ricardo Vieira (2), plus 18 others with 1-2 posts each. 22 unique individuals.

**Topic areas:** Marketing Mix Models (8), PyMC Core/Technical (7), Case Studies (6), Causal Inference (4), CLV (4), Time Series (3), A/B Testing (2), Synthetic Consumers/AI (3), Cross-posts (4).

### 7.2 Team Members

Two completely divergent rosters with minimal overlap.

| Metric | Lektor | Next.js (hardcoded) | Strapi |
|--------|--------|---------------------|--------|
| Total members | 26 | 29 (+ 1 commented out) | Unknown |
| Visible | 19 | All | `isVisible` filter |
| Hidden | 7 | 1 (commented out) | Unknown |
| Partners | N/A (no distinction) | 5 | `partner` boolean |
| Overlap | — | 8 members on both sites | — |
| Bio format | Markdown | JSX (partners) / strings | JSON array |
| Image storage | Local `headshot.jpg` | Cloudinary URLs | Cloudinary via Strapi |
| Specializations | Comma-separated string | String array | Relation (separate type) |

**Partners (Next.js):** Thomas Wiecki (Founder), Christian Luhmann (COO), Luca Fiaschi (Partner GenAI), Niall Oulton (VP Marketing Analytics), Joe Wilkinson (VP Marketing Analytics).

**Only on Lektor (18):** Adrian Seyboldt, Alexandre Andorra, Benjamin Vincent, Bill Engels, Eric Ma, Luciano Paz, Maxim Kochurov, Osvaldo Martin, Reshama Shaikh, Ricardo Vieira, Tomas Capretto, Ulf Aslak, Will Dean, plus 5 hidden.

**Only on Next.js (21):** Christian Luhmann, Joe Wilkinson, Luca Fiaschi, Allen Downey, Benjamin Maier, Camilo Saldarriaga, Christopher Fonnesbeck, Colt Allen, Eliot Carlson, Erik Ringen, Evan Wimpey, Francesco Muia, Halah Joseph, Jake Piekarski, Kemble Fletcher, Kusti Skyten, Maxim Laletin, Mengxing Baldour-Wang, Nina Rismal, Olivera Stojanovic, Pablo de Roque, Purna Mansingh, Sandra Meneses, Teemu Sailynoja, Titi Alailima.

### 7.3 Clients

22 unique clients across both sites. No case studies exist.

| Source | Count | Testimonials |
|--------|-------|-------------|
| Lektor content records | 17 visible + 1 hidden | 0 (all empty) |
| Next.js logos | 18 (opaque c1-c21 naming) | N/A |
| Next.js homepage testimonials | — | 6 real (wrong profile images) |
| Next.js course testimonials | — | 6 placeholder ("Anjali Patel" x4) |
| Next.js AI course testimonials | — | 5 template text ("Akari" product) |

**New in Next.js only:** Bain & Company.
**Testimonial-only companies:** Haleon, Ovative Group, SALK (no logos anywhere).
**Hidden/removed:** Gain Theory.

### 7.4 Courses

5 course/workshop offerings. All content is 100% hardcoded — zero CMS integration.

| Course | Site | Price | Instructors | Status |
|--------|------|-------|-------------|--------|
| Workshops (generic) | Lektor | N/A | N/A | Generic pitch page |
| Applied Bayesian Modeling | Both | $1,499/$1,699 | Downey, Leos Barajas, Fonnesbeck | Waiting list |
| Applied Bayesian Regression | Next.js | $1,499/$1,699 | Orduz, Vincent, Forde | Waiting list |
| Bayesian Marketing Analytics | Next.js | $2,249/$2,499 | McWilliams, Trujillo, Vincent, Allen | Waiting list |
| AI-Assisted Data Science | Next.js | $2,000 | Bowne-Anderson, Wiecki, Fiaschi | Waiting list |

**Registration flow (Next.js):** Form → POST `/api/registration-form/submit` → Strapi returns Wise.com payment URL → redirect.

**12 unique instructors** across all courses. AI course has completely different architecture (12 custom components, dark theme) vs shared `AppliedBayesianModeling` component for the 3 cohort courses.

### 7.5 Static Pages

| Page | Lektor | Next.js | Notes |
|------|:------:|:-------:|-------|
| Homepage | CMS | Hardcoded + Strapi | Completely different designs |
| About | - | Hardcoded | New page |
| What We Do | CMS (flow blocks) | Redirected to `/` | Content lost |
| Products | CMS (flow blocks) | Redirected to `/#products` | Content lost |
| Impressum | CMS (German legal) | Redirected to `/about` | **Legal content lost** |
| Privacy Policy | CMS (9 sections) | Hardcoded (7 sections) | Next.js version shorter |
| Terms & Conditions | CMS ("Workshop") | Hardcoded ("Course") | Terminology mismatch |
| Contact | Mailchimp iframe | Strapi form | Different systems |
| Newsletter | Mailchimp form | In Footer component | No dedicated page |
| Sitemap | Dynamic HTML | Static XML in public/ | Different formats |
| Certificate Verify | - | Server (Strapi) | New feature |
| LLM Benchmark | - | Client (3 sub-routes) | New feature |
| Cancel/Congratulations | - | Static (noindex) | Payment result pages |

---

## 8. Media Assets

### 8.1 Grand Totals

| Source | Files | Size |
|--------|------:|------|
| Lektor content media | 306 | 127.76 MB |
| Lektor assets/static | 46 | 5.99 MB |
| Next.js public/ | 174 | 31.27 MB |
| Next.js Cloudinary | 45 URLs | ~2-5 MB (est.) |
| YouTube embeds | 158 URLs | External |
| **Combined local** | **526** | **165.02 MB** |

### 8.2 Optimization Opportunities

| Issue | Files | Current Size | Potential Savings |
|-------|------:|-------------|-------------------|
| Unoptimized PNGs (Lektor) | 129 (>200 KB each) | 100.9 MB | ~60-70 MB with WebP |
| Animated GIFs | 4 | 10.5 MB | ~8 MB with WebM/MP4 |
| Oversized team headshots | 30+ | ~12 MB | ~11 MB (17-107x oversized) |
| Triple-format client logos (Next.js) | 49 | 1.8 MB | ~1.2 MB |
| Duplicate team photos across repos | 19 | ~11 MB | 100% (dedup) |
| **Conservative total savings** | | | **~80 MB (48%)** |

### 8.3 Media Issues

- 5 corrupt placeholder files (2 bytes each) in Lektor blog posts
- `.afdesign` source file (975 KB) deployed to production
- 18 JSX component files misplaced in `public/svg/`
- 2 Cloudinary accounts with no documented split
- Thomas Wiecki and Ulf Aslak photos exist in 3 locations
- Hero.mp4 (5.85 MB) served locally without CDN
- No responsive image pipeline on either site

---

## 9. Dependency & Security Audit

### 9.1 Critical Vulnerabilities

| Package | Repo | Severity | CVEs/Issues |
|---------|------|----------|-------------|
| jspdf 3.0.4 | Next.js | **Critical** | 8 CVEs: local file inclusion, PDF injection, DoS, XMP injection |
| swiper 11.2.10 | Next.js | **Critical** | Prototype pollution |
| mistune 0.8.4 | Lektor | **Critical** | CVE-2022-34749 (ReDoS), multiple CVEs, abandoned branch |
| axios 1.13.2 | Next.js | **High** | Prototype pollution via `__proto__` in mergeConfig |
| react-vertical-timeline-component | Next.js | **High** | 31 transitive vulns via deprecated @babel/preset-es2015 → json5 0.5.1 |
| Jinja2 3.1.2 | Lektor | **High** | CVE-2024-34064 (sandbox escape) |
| Flask 2.3 / Werkzeug 2.3 | Lektor | **High** | EOL, CVE-2024-34069 (debugger RCE) |

### 9.2 EOL Components

| Component | Version | EOL Date | Replacement |
|-----------|---------|----------|-------------|
| Python 3.8 (CI) | 3.8 | Oct 2024 | Python 3.12+ |
| Python 3.9 (pixi) | 3.9 | Oct 2025 | Python 3.12+ |
| Bootstrap 4 | 4.5.2 | Jan 2023 | Bootstrap 5.3 or Tailwind |
| MathJax 2 | 2.7.5 | 2020 | MathJax 4 or KaTeX |
| Popper.js 1 | 1.16.1 | — | @popperjs/core 2.x |
| Flask 2.3 | 2.3.1 | — | Flask 3.1 |
| Werkzeug 2.3 | 2.3.0 | — | Werkzeug 3.1 |

### 9.3 npm Audit Summary (Next.js)

| Severity | Count |
|----------|------:|
| Critical | 2 |
| High | 31 |
| Moderate | 6 |
| **Total** | **39** |

31 of 39 high vulns come from a single package: `react-vertical-timeline-component` → deprecated `@babel/preset-es2015` → `json5 0.5.1`.

### 9.4 Security Concerns (Integration-Specific)

| # | Severity | Issue |
|---|----------|-------|
| 1 | Critical | Zero authentication on all 16 Strapi endpoints |
| 2 | Critical | API keys submitted in plaintext (benchmark) |
| 3 | High | Wildcard `*` image domains enable SSRF |
| 4 | High | Unauthenticated PUT on certificates |
| 5 | High | Draft blog content accessible without auth |
| 6 | Medium | Mailchimp credentials in client JS (both sites) |
| 7 | Medium | JSONP newsletter subscription (deprecated, script injection) |
| 8 | Medium | HTTPS not enforced on GitHub Pages |
| 9 | Medium | HubSpot script loaded outside `<head>` |
| 10 | Low | Hardcoded Heroku URL in sitemap config |
| 11 | Low | Wrong domain (`pymc-labs.io`) in JSON-LD |
| 12 | Low | PAT-based deploy auth |

---

## 10. Cross-Site Comparison

### 10.1 Technology Migration

| Concern | Lektor | Next.js | Status |
|---------|--------|---------|--------|
| Language | Python 3.9 (EOL) | Node.js 20+ | Upgraded |
| Framework | Lektor 3.3 | Next.js 16 | Upgraded |
| CSS | Bootstrap 4 (EOL) | Tailwind 3.4 | Upgraded |
| JS | jQuery 3.5 | React 19 | Upgraded |
| Math | MathJax 2 (EOL) | KaTeX 0.16 | Upgraded |
| Markdown | mistune 0.8 (EOL) | react-markdown 10 | Upgraded |
| Analytics | GA4 only | GTM + GA4 + HubSpot | Expanded |
| Icons | Font Awesome (1 lib) | FA + lucide + react-icons (3 libs) | **Regressed** |
| Newsletter | HTML form | JSONP injection | **Regressed** |
| Content mgmt | File-based (git) | Strapi on Heroku | More capable, external dependency |
| Type safety | N/A (Python) | No TypeScript | Gap |
| Tests | None | None | Unchanged |
| CI/CD | Broken | Absent | Unchanged |

### 10.2 Content Migration Status

| Content Type | Lektor → Next.js | Notes |
|-------------|:----------------:|-------|
| Blog posts | Partially migrated | Lektor has .lr files; Next.js reads from Strapi DB (separate) |
| Team members | Divergent | Only 8 overlap out of 47 unique members |
| Clients | Mostly migrated | 16 of 17 Lektor clients have Next.js logos |
| Courses | Expanded | 1 Lektor workshop → 4 Next.js courses (all hardcoded) |
| Privacy Policy | Shortened | 9 sections → 7 sections (Direct Marketing clause dropped) |
| Terms & Conditions | Reworded | "Workshop" → "Course" |
| Impressum | **Lost** | Redirected to `/about` with no legal content |
| What We Do | **Lost** | Redirected to `/` |
| Products | **Lost** | Redirected to `/#products` anchor |

---

## 11. Issues Registry

### 11.1 Critical (Immediate Action Required)

| # | Issue | Location |
|---|-------|----------|
| 1 | Lektor CI broken — `requirements.txt` deleted, workflows never updated | `.github/workflows/main.yml`, `deploy-previews.yml` |
| 2 | Zero authentication on all Strapi endpoints | All Next.js API calls |
| 3 | jspdf 3.0.4 — 8 CVEs (file inclusion, PDF injection, DoS) | `package.json` |
| 4 | API keys submitted in plaintext to benchmark endpoint | `POST /api/benchmark/submit` |
| 5 | swiper 11.2.10 — prototype pollution | `package.json` |
| 6 | mistune 0.8.4 — multiple CVEs, abandoned | `pixi.toml` |

### 11.2 High

| # | Issue | Location |
|---|-------|----------|
| 7 | 39 npm audit vulnerabilities (31 from react-vertical-timeline-component) | `package-lock.json` |
| 8 | Wildcard `*` image domains enable SSRF | `next.config.mjs` |
| 9 | Unauthenticated draft blog access | `/draft-post/[id]` |
| 10 | Unauthenticated PUT on certificates | `PUT /api/certificates/:id/download` |
| 11 | Python 3.8/3.9 both EOL | CI workflows + `pixi.toml` |
| 12 | Flask/Werkzeug/Jinja2 CVEs | `pixi.toml` |
| 13 | HTTPS not enforced on production site | GitHub Pages settings |
| 14 | AI course testimonials 100% placeholder ("Akari" template) | `AiTestimonials.jsx` |
| 15 | All course content hardcoded — no CMS | All course `page.js` files |
| 16 | 129 unoptimized PNGs (100.9 MB) | Lektor `content/` |
| 17 | No Strapi source code in any repository | External Heroku deployment |

### 11.3 Medium

| # | Issue | Location |
|---|-------|----------|
| 18 | Impressum legal content lost in redirect | `next.config.mjs` |
| 19 | Privacy Policy divergence (missing sections) | Next.js privacy policy |
| 20 | 3 duplicate contact form implementations | `components/contact/`, `components/shared/ContactUs` |
| 21 | Dual team data sources (hardcoded JS + Strapi) | `libs/team.js` + Strapi API |
| 22 | Wrong domain (`pymc-labs.io`) in JSON-LD | Contact + team-detail pages |
| 23 | Mailchimp JSONP injection (deprecated) | Footer, blog Newsletter |
| 24 | `"use client"` root layout anti-pattern | `app/layout.js` |
| 25 | Canonical URL mismatch (`pymc-labs.github.io`) | `.lektorproject` |
| 26 | Countdown timer hardcoded to stale date | `AppliedBayesianModeling.jsx` |
| 27 | Instructor anchor links swapped (Downey/Leos Barajas) | ABM course `page.js` |
| 28 | `console.log` in production (multiple files) | BlogContent, Footer, RegistrationForm, verify page |
| 29 | 3 icon libraries loaded simultaneously | Layout + npm deps |
| 30 | Hardcoded Heroku URL in sitemap config | `next-sitemap.config.js` |
| 31 | Terms terminology mismatch ("Workshop" vs "Course") | Legal pages |
| 32 | 2 Cloudinary accounts with no documented split | Next.js codebase |

### 11.4 Low

| # | Issue | Location |
|---|-------|----------|
| 33 | Blog post author model/content mismatch | `models/blog_post.ini` |
| 34 | Dead `testimonial` flowblock | `flowblocks/testimonial.ini` |
| 35 | Ghost `_model: testimonials` references | `clients/contents.lr`, `newsletter/contents.lr` |
| 36 | Unused `lektor-tags` plugin | `.lektorproject` |
| 37 | Alt-text typos ("Melindia", "Resarch") | `TrustedBy.jsx` |
| 38 | Slug typo ("examplar-tech" vs "exemplar") | Lektor `content/clients/` |
| 39 | Wrong LinkedIn URL for Luca Fiaschi (GitHub URL) | `libs/team.js` |
| 40 | Typos in component names (Vedio, Dunamic, Inovation) | Various components |
| 41 | `.afdesign` source file deployed to production | Lektor static assets |
| 42 | 18 JSX files misplaced in `public/svg/` | Next.js `public/` |
| 43 | 5 corrupt 2-byte placeholder images | Lektor blog posts |
| 44 | No `not-found.jsx` or error boundaries | Next.js app directory |
| 45 | Pre-generated static sitemap (won't update) | Next.js `public/sitemap.xml` |
| 46 | Placeholder FAQ from payment template ("Instapay") | `shared/FAQ.jsx` |
| 47 | Homepage testimonials use wrong profile images | `Testimonials.jsx` |
| 48 | Course testimonials use placeholder names | `Testimonials.jsx` |
| 49 | Opaque client logo filenames (c1-c21) | Next.js `public/clients/` |
| 50 | No `.env.example` file | Next.js repo |

---

## 12. Redesign Considerations

The planned architecture redesign splits into: **Framer** (marketing) + **focused Next.js app** (enrollment) + **Hugo** (blog). Based on this analysis, key considerations include:

### 12.1 Content That Must Be Migrated

| Content | Source | Migration Method | Complexity |
|---------|--------|-----------------|------------|
| 52 blog posts + 276 images | Lektor `.lr` files | Parse `---` format → Hugo frontmatter + markdown | Medium |
| Strapi blog content | Strapi API | Export via `/api/articles?pagination[pageSize]=1000` before Heroku shutdown | Medium |
| 26 Lektor team members | Lektor `.lr` files | Parse to structured data | Low |
| 29 Next.js team members | `libs/team.js` | Extract from JSX array | Low |
| Strapi team data | Strapi API | Export via `/api/teams` | Low |
| 22 client records + logos | Both repos | Consolidate, deduplicate | Low |
| 6 real testimonials | `Testimonials.jsx` (hardcoded) | Extract from JSX | Low |
| 4 course definitions | Hardcoded JSX | Extract structured data from page files | Medium |
| Legal pages | Both repos | Merge (Lektor has more complete versions) | Low |
| Media assets (165 MB) | Both repos + Cloudinary | Optimize (WebP), consolidate, set up CDN | High |

### 12.2 Systems That Must Be Preserved

1. **Course registration → Wise.com payment** — Server-side URL generation via Strapi
2. **Certificate verification** — Public verify/download/email lookup
3. **Coupon validation** — Promo code → discounted Wise link
4. **Blog categories + search + pagination** — Currently Strapi-backed
5. **Newsletter subscription** — Mailchimp (needs proper implementation, not JSONP)
6. **Analytics** — GTM + GA4 + HubSpot tracking events

### 12.3 Content Gaps to Address

1. **No case studies** — Neither site has them despite having 22 clients
2. **Impressum lost** — German legal requirement not met in Next.js
3. **Privacy policy incomplete** — Missing direct marketing and registration data sections
4. **Zero actual course testimonials** — All are placeholder
5. **No author profiles** — Blog authors aren't linked to team members
6. **No content sync** — Team rosters completely divergent between sites

### 12.4 Technical Debt to Resolve

1. **No Strapi source code** — Backend is a black box; content type schemas must be documented/exported before any migration
2. **No tests anywhere** — Zero test infrastructure across both repos
3. **No CI/CD** — Must be established for any new architecture
4. **Authentication** — Must be added to any enrollment/admin endpoints
5. **Image optimization pipeline** — ~80 MB savings possible, no responsive images
6. **Single data source** — Eliminate dual team data (hardcoded + CMS)

---

*This spec was generated by a ralph reverse loop analyzing 18 aspects across `pymc-labs/pymc-labs-website-source` and `pymc-labs/pymc-rebranded-website`. Each aspect's detailed analysis is available in the `analysis/` directory.*
