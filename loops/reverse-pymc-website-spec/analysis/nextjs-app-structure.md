# Next.js App Structure — pymc-rebranded-website

## Framework & Runtime

| Property | Value |
|----------|-------|
| Framework | Next.js 16.0.7 (App Router) |
| React | 19.2.1 |
| Language | JavaScript (.js/.jsx, no TypeScript) |
| Dev server | Turbopack (`next dev --turbopack`) |
| CSS | Tailwind CSS 3.4.1 + global CSS vars |
| Fonts | Google Fonts: Roboto (primary), Inter (secondary) via `next/font` |
| Path aliases | `@/*` maps to project root (`jsconfig.json`) |
| No `src/` directory | App, components, libs, utils all at project root |

## Project Root Layout

```
pymc-rebranded-website/
├── app/                  # Next.js App Router (routes + API)
├── components/           # React component library (~80 files)
├── config/               # Single file: API_BASE_URL from env
├── draft/                # Unused route drafts (industries, services, solutions)
├── libs/                 # HTTP client, auth, SEO helper, team data, GTM
├── public/               # Static assets (~174 files, ~32 MB)
├── utils/                # Nav/footer config, LLM benchmark data, helpers
├── next.config.mjs       # Images, redirects
├── next-sitemap.config.js # Dynamic sitemap generation
├── tailwind.config.mjs   # Minimal customization (marquee animation)
├── package.json          # 32 deps, 5 devDeps
└── jsconfig.json         # Path alias @/*
```

## Route Map (22 page routes + 1 API route handler)

### Static Pages (no dynamic segments)

| Route | File | Rendering | Data Source |
|-------|------|-----------|-------------|
| `/` | `app/page.js` | Client (via HomeContent) | Strapi (client-side) |
| `/about` | `app/about/page.jsx` | Client (via AboutContent) | None (static) |
| `/team` | `app/team/page.jsx` | **Server** (async) | Strapi REST (`/api/teams?populate=*`) with ISR (revalidate: 60s) |
| `/contact` | `app/contact/page.js` | Client (via ContactFormPage) | None |
| `/courses` | `app/courses/page.jsx` | Client (via CoursesContent) | Strapi (client-side) |
| `/blog-posts` | `app/blog-posts/page.jsx` | Client (via BlogContent) | Strapi (client-side via API wrapper) |
| `/privacy-policy` | `app/privacy-policy/page.jsx` | Client | None (static content) |
| `/terms-and-conditions` | `app/terms-and-conditions/page.jsx` | Client | None (static content) |
| `/cancel` | `app/cancel/page.js` | Client | None (noindex) |
| `/congratulations` | `app/congratulations/page.js` | Client | None (noindex) |
| `/benchmark/LLMPriceIsRight` | `app/benchmark/LLMPriceIsRight/page.jsx` | Client | Local JSON (`utils/leaderboard.json`) |
| `/benchmark/LLMPriceIsRight/leaderboard` | `.../leaderboard/page.jsx` | Client | Local JSON |
| `/benchmark/LLMPriceIsRight/add-model` | `.../add-model/page.jsx` | Client | None (form) |

### Dynamic Pages

| Route | File | Rendering | Data Source |
|-------|------|-----------|-------------|
| `/blog-posts/[id]` | `app/blog-posts/[id]/page.jsx` | **Server** (`"use server"`) | Strapi REST (`/api/articles?filters[slug][$eq]=...&populate=*`) |
| `/blog-posts/filters/[category]` | `.../filters/[category]/page.jsx` | Client (BlogContent) | Strapi (client-side filtering) |
| `/draft-post/[id]` | `app/draft-post/[id]/page.jsx` | Server | Strapi (draft articles: `status=draft`) |
| `/team-detail/[id]` | `app/team-detail/[id]/page.jsx` | **Server** (async) | Strapi REST (`/api/teams?filters[slug][$eq]=...`) with ISR (revalidate: 60s) |
| `/verify/[id]` | `app/verify/[id]/page.js` | **Server** (async) | Strapi REST (`/api/certificates/verify/:id`) |

### Course Detail Pages (hardcoded per course)

| Route | File | Notes |
|-------|------|-------|
| `/courses/applied-bayesian-modeling` | `app/courses/applied-bayesian-modeling/page.js` | Inline content: curriculum, FAQ, pricing ($1,499), instructors, JSON-LD |
| `/courses/applied-bayesian-regression-modeling` | `.../page.js` | Similar hardcoded structure |
| `/courses/bayesian-marketing-analytics` | `.../page.js` | Similar hardcoded structure |
| `/courses/ai-assisted-data-science` | `.../page.js` | Similar hardcoded structure |

### API Route Handler

| Route | File | Method | Purpose |
|-------|------|--------|---------|
| `/blog-posts/[id]/md` | `app/blog-posts/[id]/md/route.js` | GET | Returns blog post as plain markdown (`text/markdown`) |

### Draft Routes (in `draft/` directory, NOT in `app/`)

Unused/in-progress pages not accessible via routing:
- `draft/industries/` — Industries listing page
- `draft/industries-detail/` — Industry detail page
- `draft/services/` — Services listing page
- `draft/service-detail/` — Service detail page
- `draft/solutions/` — Solutions page

## Layout & Provider Architecture

### Root Layout (`app/layout.js`)

**Critical issue: `"use client"` on root layout.** This makes the entire layout a client component, which means:
- `metadata` export at the page level still works (App Router handles it), but the layout itself cannot use server-only features
- `usePathname()` is used for dynamic `<title>` generation (redundant — pages already export `metadata`)
- Title generation uses a client-side `generateTitle()` function with hardcoded pathname-to-title mapping

**Embedded scripts in layout:**
- Google Tag Manager (GTM) via `NEXT_PUBLIC_GTM_ID` env var
- HubSpot tracking script (`js.hs-scripts.com/50315116.js`) — loaded outside `<head>`, directly in root
- Bing Webmaster verification meta tag
- Organization JSON-LD schema (dynamically generated per page, **incorrectly** uses page title as org name)
- Font Awesome 6.7.2 via CDN link (despite `lucide-react` and `react-icons` also in deps)

### ClientProvider (`app/ClientProvider.jsx`)

Wraps all pages with:
- `<Navbar>` — top navigation with contact modal trigger
- `<ContactPopup>` — modal contact form (state managed here)
- `<Footer>` — site footer with contact modal trigger
- Main content wrapped in `<main className='pt-20'>` (fixed navbar offset)

## next.config.mjs

### Image Configuration
- **Domains**: `res.cloudinary.com` (explicit) + wildcard `*` for both HTTP and HTTPS
- **Security concern**: Wildcard `*` remote patterns allow any image domain
- Sharp installed for server-side image optimization

### Redirects (7 rules)
| Source | Destination | Type |
|--------|-------------|------|
| `/what-we-do` | `/` | Permanent |
| HTTP requests | `https://www.pymc-labs.com/...` | Permanent |
| `pymc-labs.com` (no www) | `https://www.pymc-labs.com/...` | Permanent |
| `/team/:id` | `/team-detail/:id` | Permanent |
| `/impressum` | `/about` | Permanent |
| `/products` | `/#products` | Permanent |
| `/clients` | `/#clients` | Permanent |

**Note**: The `/team/:id` -> `/team-detail/:id` redirect indicates the team detail route was moved but the URL structure wasn't cleaned up (an extra redirect hop for every team member link).

## Data Fetching Architecture

### Strapi Backend
- **URL**: `NEXT_PUBLIC_STRAPI_URL` env var (exposed to client)
- **Known Heroku deployment**: `pymc-backend-afc5c26e8ab7.herokuapp.com` (hardcoded in sitemap config)
- **Media storage**: Cloudinary (`res.cloudinary.com`, accounts: `dx3t8udaw` and `dhgr6mghh`)
- **Auth**: Token-based (`x-access-token` header from localStorage)
- **HTTP client**: Axios wrapper in `libs/http-client.js`

### API Wrapper Functions (`app/api/`)
These are NOT Next.js API route handlers — they're client-side data fetching functions mislocated in the `app/api/` directory:

| File | Functions | Strapi Endpoints |
|------|-----------|------------------|
| `app/api/blog/index.js` | `getBlogs()`, `getAllBlogs()`, `getSingleBlog()`, `getSingleDraftBlog()` | `/api/articles` |
| `app/api/certificate/index.js` | `updateCertificateDownloadStatus()` | `/api/certificates/:id/download` (PUT) |
| `app/api/contact/index.js` | `SendContactForm()` | `/api/contact-users` (POST) |
| `app/api/promotion-bars/index.js` | `getPromotionBar()` | `/api/promotion-bars` (GET) |

### Server-Side Data Fetching
- **Team pages**: Direct `fetch()` with ISR (`next: { revalidate: 60 }`)
- **Blog detail**: Via Axios wrapper (runs on server due to `"use server"` directive)
- **Certificate verification**: Direct Axios call on server

### Client-Side Data Fetching
- Blog listing, courses listing, home page content: All fetched client-side via Axios wrapper

## Sitemap Configuration (`next-sitemap.config.js`)

- Site URL: `https://www.pymc-labs.com`
- Robots.txt generation: **disabled**
- Dynamic paths fetched from Strapi at build time (blog posts + categories)
- Excluded routes: `/cancel`, `/congratulations`, `/about`
- **Hardcoded Strapi URL** in sitemap config (not using env var)

## SEO Architecture

### Metadata Strategy
- `libs/seo.js` — `createMetadata()` helper generating title, description, canonical, OpenGraph, Twitter cards
- Default OG image: Cloudinary-hosted favicon
- Most pages use `createMetadata()`, but course detail pages and contact page define metadata inline
- Blog detail pages generate dynamic metadata on the server with `generateMetadata()`
- JSON-LD structured data on: organization (layout), blog posts, team members, courses

### Canonical URL Issues
- Layout generates canonical from `NEXT_PUBLIC_SITE_URL` env var
- `libs/seo.js` hardcodes `https://www.pymc-labs.com`
- Contact page OG URL uses `pymc-labs.io` (wrong domain)
- Team detail JSON-LD uses `pymc-labs.io` (wrong domain)
- Blog detail canonical uses relative URL (`/blog-posts/${id}`) without domain

## Team Data Architecture (Dual Source)

Team data comes from TWO sources:
1. **Strapi CMS** — used by `/team` (listing) and `/team-detail/[id]` (detail) pages via REST API
2. **Hardcoded JS array** — `libs/team.js` exports a `Team` array with 29 members (5 partners + 24 team members)

The `libs/team.js` file contains JSX in bio fields (React elements, not strings), making it non-portable. One member (Niall Oulton) is commented out (appears as partner instead). The hardcoded array is imported in `team-detail/[id]/page.jsx` but the page actually fetches from Strapi — the import appears unused.

**Key inconsistency**: 29 members hardcoded vs. whatever Strapi has. The hardcoded data includes Cloudinary image URLs, suggesting it was migrated from or alongside Strapi.

## Environment Variables

| Variable | Purpose | Exposure |
|----------|---------|----------|
| `NEXT_PUBLIC_STRAPI_URL` | Strapi API base URL | Client + Server |
| `NEXT_PUBLIC_SITE_URL` | Canonical site URL | Client + Server |
| `NEXT_PUBLIC_GTM_ID` | Google Tag Manager ID | Client + Server |

No `.env.example` file exists in the repo.

## Key Architectural Issues

1. **`"use client"` root layout** — Prevents server rendering benefits at the layout level; generates titles client-side instead of using metadata API properly
2. **API wrappers in `app/api/`** — Confusing: these are NOT Next.js API routes, just client-side fetch functions. Actual route handler exists only at `blog-posts/[id]/md/route.js`
3. **Dual team data sources** — Strapi CMS and hardcoded `libs/team.js` will inevitably drift
4. **Wildcard image domains** — `*` hostname pattern in `next.config.mjs` is a security risk (SSRF vector)
5. **Hardcoded Strapi URL** in `next-sitemap.config.js` (doesn't use env var)
6. **Wrong domain references** — `pymc-labs.io` used in contact page and team detail JSON-LD (should be `pymc-labs.com`)
7. **HubSpot script outside `<head>`** — Placed directly on `<body>`'s sibling level
8. **No error boundaries** — No `error.js` or `not-found.js` files anywhere
9. **No middleware** — No auth protection, no locale handling, no edge logic
10. **3 icon libraries** — Font Awesome (CDN), lucide-react (npm), react-icons (npm) all included
11. **Draft routes outside app directory** — `draft/` contains 5 unused page templates for industries, services, solutions
12. **Course pages fully hardcoded** — Curriculum, pricing, FAQ, instructors all inline in page files instead of CMS-driven
