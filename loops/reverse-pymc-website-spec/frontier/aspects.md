# Frontier — PyMC Labs Website Spec

## Statistics
- Total aspects discovered: 19
- Analyzed: 0
- Pending: 19
- Convergence: 0%

## Pending Aspects (ordered by dependency)

### Wave 1: Data Acquisition
- [ ] clone-source-repo — Clone pymc-labs-website-source, save file tree to raw/
- [ ] clone-rebranded-repo — Clone pymc-rebranded-website, save file tree to raw/
- [ ] cache-redesign-plan — Fetch architecture redesign plan to input/ for cross-reference

### Wave 2: Architecture Analysis
Depends on Wave 1 data.
- [ ] lektor-site-structure — Lektor models, templates, databags, flowblocks, plugins
- [ ] lektor-content-schema — .lr file structure, fields, content types, relationships
- [ ] lektor-build-deploy — Build pipeline, GitHub Actions, hosting config (GitHub Pages + Netlify)
- [ ] nextjs-app-structure — App/pages router, route map, layouts, middleware
- [ ] nextjs-components — Component tree, shared components, UI library usage
- [ ] strapi-data-models — Content types, relations, custom controllers, lifecycle hooks
- [ ] strapi-api-endpoints — REST/GraphQL endpoints, auth, custom routes
- [ ] integrations — Stripe, Mailchimp, analytics, third-party services across both repos
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
(Empty — loop hasn't started yet)
