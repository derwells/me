# Frontier — PyMC Labs Website Spec

## Statistics
- Total aspects discovered: 20
- Analyzed: 20
- Pending: 0
- Convergence: 100% (CONVERGED)

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
- [x] dependencies-audit — Package versions, EOL/vulnerability status across both repos

### Wave 3: Content Audit
Depends on Wave 2 analysis.
- [x] blog-posts-catalog — All blog posts: titles, dates, authors, categories, media
- [x] team-members-catalog — All team members: names, roles, bios, headshots, social links
- [x] clients-catalog — Client logos, testimonials, case studies
- [x] courses-catalog — All courses: titles, descriptions, curricula, instructors, pricing, status
- [x] static-pages-catalog — Every standalone page (About, Contact, Privacy, etc.)
- [x] media-assets-audit — Images, PDFs, videos: sizes, formats, optimization status

### Wave 4: Synthesis
Depends on all Wave 2 and Wave 3 analysis.
- [x] unified-spec-draft — Synthesize all analysis into unified spec document
- [x] spec-self-review — Review for completeness and accuracy

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
- [x] dependencies-audit (Wave 2) — 39 npm audit vulns in Next.js (2 critical: jspdf 8 CVEs, swiper prototype pollution; 31 high from react-vertical-timeline-component → @babel/preset-es2015 chain). Lektor: Python 3.8/3.9 EOL, Flask/Werkzeug 2.3 EOL, mistune 0.8 EOL (multiple CVEs), Jinja2 3.1.2 CVE. CDN: Bootstrap 4 EOL, MathJax 2 EOL, Popper.js 1.x EOL. All 6 GH Actions outdated (v2). Lektor CI broken. Next.js has zero CI. Neither repo has tests. Wave 2 complete.
- [x] blog-posts-catalog (Wave 3) — 52 Lektor posts (2021-02 to 2025-06), all visible. 14 video posts (27%), 30 with summaries (58%). 276 images (115 MB, mostly PNG). 22 unique authors, Thomas Wiecki leads with 12. No categories in Lektor. Next.js serves from Strapi (categories, search, pagination, featured flag, draft preview). Unused 2,822-line placeholder data.js. 5 slug conventions mixed. Date typo in one slug. JSON-LD path mismatch (/blog/ vs /blog-posts/).
- [x] team-members-catalog (Wave 3) — 26 Lektor members (19 visible, 7 hidden), 29 Next.js hardcoded members + Strapi dual source. Only 8 overlap between sites. 5 partners in Next.js (new tier). Dual data source: libs/team.js for About TeamSlider, Strapi for /team page. 2 Cloudinary accounts. Inconsistent bio formats (Markdown vs JSX vs JSON arrays). 14 issues: wrong LinkedIn URL, missing https://, wrong domain in JSON-LD, no content sync.
- [x] clients-catalog (Wave 3) — 22 unique clients across both sites. 17 Lektor content records (16 visible + 1 hidden) with 0 actual testimonials. 18 Next.js logos (opaque c1-c21 naming). 6 real testimonials hardcoded in Next.js homepage. 11 placeholder/fake testimonials on course pages (including "Akari" template text). Bain & Company new in Next.js. 3 testimonial companies (Haleon, Ovative, SALK) not in any logo set. No case studies exist. 16 issues: wrong profile images, alt-text typos, orphan Colgate logo, dead flowblock.
- [x] courses-catalog (Wave 3) — 5 offerings: 1 Lektor generic workshop page + 1 hidden ABM template + 4 Next.js course pages (ABM, Regression, Marketing Analytics, AI-Assisted DS). All 100% hardcoded (zero CMS). 12 unique instructors. Prices: $1,499-$2,249. Registration via Strapi → Wise.com payment URLs. AI course has completely different architecture (12 custom components) + 100% placeholder testimonials ("Akari" template). Swapped instructor anchor links, stale countdown timer, misspelled names. 19 issues documented.
- [x] static-pages-catalog (Wave 3) — 10 Lektor standalone pages + 15 Next.js deployed pages + 5 draft routes. 6 CMS-managed (Lektor flow blocks), 18 hardcoded. 4 Lektor pages redirected in Next.js (what-we-do→/, impressum→/about, products→/#products, clients→/#clients). Impressum legal content lost in redirect. Privacy policy divergence (Next.js shorter, missing sections). T&C terminology mismatch (Workshop vs Course). Contact page wrong domain (pymc-labs.io). No 404, no error boundaries, no loading states. Pre-generated static sitemap. 16 issues documented.
- [x] media-assets-audit (Wave 3) — 526 local files (165 MB) + 45 Cloudinary URLs + 158 YouTube embeds. Lektor: 306 content images (128 MB, 80% unoptimized PNG), 46 static assets (6 MB incl. deployed .afdesign source file). Next.js: 174 public files (31 MB incl. 5.85 MB hero video), 18 JSX misplaced in public/svg/. 19 identical team photos duplicated across repos. Triple-format client logos (49 files for 18 clients). 2 Cloudinary accounts with no documented split. ~80 MB savings possible from WebP + resize. Wave 3 complete. 18 issues documented.
- [x] unified-spec-draft (Wave 4) — Synthesized all 18 analysis files into unified spec at output/pymc-website-spec.md. 12 sections covering architecture, data models, API endpoints, components, content inventory (52 blog posts, 47 unique team members, 22 clients, 5 courses), media assets (526 files, 165 MB), dependency audit (44+ vulns), and 50 documented issues. Cross-referenced against redesign plan. Identified 6 critical, 11 high, 15 medium, 18 low issues.
- [x] spec-self-review (Wave 4) — All 20 aspects verified against spec. One counting error corrected (6→7 custom Strapi routes, 15→16 total endpoints). All numbers match source analysis. Three minor gaps noted as inherent repo-only limitations. Loop CONVERGED.
