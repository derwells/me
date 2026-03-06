# Frontier — PyMC Labs Website Spec

## Statistics
- Total aspects discovered: 19
- Analyzed: 11
- Pending: 8
- Convergence: 58%

## Pending Aspects (ordered by dependency)

### Wave 1: Data Acquisition
- [x] clone-source-repo — Clone pymc-labs-website-source, save file tree to raw/
- [x] clone-rebranded-repo — Clone pymc-rebranded-website, save file tree to raw/
- [x] cache-redesign-plan — Fetch architecture redesign plan to input/ for cross-reference

### Wave 2: Architecture Analysis
Depends on Wave 1 data.
- [x] lektor-site-structure — Lektor models, templates, databags, flowblocks, plugins
- [x] lektor-content-schema — .lr file structure, fields, content types, relationships
- [x] lektor-build-deploy — Build pipeline, GitHub Actions, hosting config (GitHub Pages + Netlify)
- [x] nextjs-app-structure — App/pages router, route map, layouts, middleware
- [x] nextjs-components — Component tree, shared components, UI library usage
- [x] strapi-data-models — Content types, relations, custom controllers, lifecycle hooks
- [x] strapi-api-endpoints — REST/GraphQL endpoints, auth, custom routes
- [x] integrations — Stripe, Mailchimp, analytics, third-party services across both repos
- [ ] dependencies-audit — Package versions, EOL/vulnerability status across both repos

### Wave 3: Content Audit
Depends on Wave 2 analysis.
- [ ] blog-posts-catalog — All blog posts: titles, dates, authors, categories, media
- [ ] team-members-catalog — All team members: names, roles, bios, headshots, social links
- [ ] clients-catalog — Client logos, testimonials, case studies
- [ ] courses-catalog — All courses: titles, descriptions, curricula, instructors, pricing, status
- [ ] static-pages-catalog — Every standalone page (About, Contact, Privacy, etc.)
- [ ] media-assets-audit — Images, PDFs, videos: sizes, formats, optimization status

### Wave 4: Synthesis
Depends on all Wave 2 and Wave 3 analysis.
- [ ] unified-spec-draft — Synthesize all analysis into unified spec document
- [ ] spec-self-review — Review for completeness and accuracy

## Recently Analyzed
- [x] clone-source-repo (Wave 1) — 522 files, 329 blog posts, Lektor CMS, Pixi deps
- [x] clone-rebranded-repo (Wave 1) — 379 files, Next.js 16 + Strapi CMS, 22 routes, 80 components, 174 public assets
- [x] cache-redesign-plan (Wave 1) — No formal plan document found in repos/issues. Documented known intent (Framer + Next.js + Hugo split) from loop context.
- [x] lektor-site-structure (Wave 2) — 10 models, 22 templates, 4 flowblocks, 2 databags, 4 plugins (1 custom). Bootstrap 4 + jQuery. Mailchimp, GA4, Wise.com integrations. 17 routes. Multiple EOL deps (Python 3.9, Mistune 0.8, MathJax 2).
- [x] lektor-content-schema (Wave 2) — .lr file format with `---` delimiters, flow blocks with `####` syntax. 52 blog posts (2021-2025), 26 teammates (7 hidden), 18 clients (1 hidden, 0 testimonials). Author checkboxes bypassed (26 unique free-text values vs 13 hardcoded). Ghost `_model: testimonials` reference. Dead `testimonial` flowblock. Undeclared fields silently ignored. No pagination, no tags, no relational integrity.
- [x] lektor-build-deploy (Wave 2) — Broken CI: requirements.txt removed (migrated to Pixi) but workflows never updated. 3 GH Actions workflows (deploy, preview, merge-schedule). Deploys to pymc-labs.github.io via force-orphan push. Netlify for PR previews. CNAME www.pymc-labs.com but HTTPS not enforced. Canonical URL mismatch. PAT auth, outdated Actions (v2), Python 3.8 in CI vs 3.9 in pixi.
- [x] nextjs-app-structure (Wave 2) — Next.js 16 App Router (no src/), 22 page routes + 1 API route handler. "use client" root layout (anti-pattern). Strapi backend on Heroku, Cloudinary media. Dual team data (Strapi + hardcoded JS array with 29 members). 4 course pages fully hardcoded. 5 draft routes (industries/services/solutions) outside app/. No middleware, no error boundaries. 3 icon libraries. Wrong domain (pymc-labs.io) in contact/team JSON-LD. Wildcard image domains (security risk). 12 architectural issues documented.
- [x] nextjs-components (Wave 2) — 80 component files across 12 subdirs. Feature-first flat structure, low reuse. 3-4 duplicate contact form implementations. Duplicate Pagination components. 3 icon libs loaded simultaneously (FA CDN + lucide-react + react-icons). Pervasive framer-motion dependency (~30 components). Hardcoded testimonials (6), team bios (29 with JSX), FAQ placeholder from payment template. Typos in component names (Vedio, Dunamic, Inovation). dangerouslySetInnerHTML, console.logs in prod, Mailchimp JSONP injection. No design system, no TypeScript, no error boundaries.
- [x] strapi-data-models (Wave 2) — 11 content types reverse-engineered from frontend (no Strapi source in repo). Core: article (18 fields, categories/authors relations), team (16 fields, bio as JSON array, partner/isVisible booleans, specializations), certificate (PascalCase fields, verify/download custom routes), category, author. Forms: contact-user (legacy), contact-form (newer with inquiry categories), registration-form (payment link generation). Also: coupon (promo validation), promotion-bar, benchmark (model submission). 7 custom route handlers beyond CRUD. 3 duplicate contact systems. Dual team data (Strapi + hardcoded). Most endpoints unauthenticated.
- [x] strapi-api-endpoints (Wave 2) — 15 unique Strapi endpoints (9 standard CRUD + 6 custom routes). Zero authentication on all calls. Dual fetch patterns (GetApiData wrapper vs direct fetch/axios). Draft blogs accessible without auth. Unauthenticated PUT on certificates. 3 duplicate contact form systems. Mailchimp JSONP in 2 components (deprecated, credentials exposed). Hardcoded Heroku URL in sitemap config. Wildcard image domains (SSRF risk). 12 issues documented.
- [x] integrations (Wave 2) — 17 unique third-party services cataloged (8 Lektor, 14 Next.js, 5 shared). Payment: Wise.com (both sites, dynamic in Next.js) + Stripe (incomplete). Email: Mailchimp (both, JSONP regression in Next.js). Analytics: GA4 (Lektor direct) → GTM + HubSpot + Bing (Next.js). Backend: Strapi on Heroku + Cloudinary (2 accounts). Hosting: GitHub Pages + Netlify previews (Lektor), Heroku (Strapi). 3 icon libraries, 3 duplicate contact systems. 12 security concerns documented (zero auth, SSRF, JSONP injection, exposed credentials, plaintext API keys).
