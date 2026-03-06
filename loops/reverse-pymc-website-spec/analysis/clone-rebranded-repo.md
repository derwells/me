# Clone Rebranded Repo — Analysis

## Summary

Cloned `pymc-labs/pymc-rebranded-website` (shallow) to `input/pymc-rebranded-website/`. File tree saved to `raw/rebranded-file-tree.txt`.

## Repo Metadata

| Field | Value |
|-------|-------|
| Default branch | `main` |
| Language | JavaScript |
| Created | 2025-03-24 |
| Last pushed | 2026-03-06 |
| Repo size | 60.6 MB |
| Active branches | 30 (including `dev`, `develop`, `staging`, `new-dev`) |
| Total files | 379 |

## Tech Stack (first-pass)

- **Framework**: Next.js 16 (App Router, Turbopack dev mode)
- **React**: 19.2.1
- **Styling**: Tailwind CSS 3.4.1
- **HTTP**: Axios (to Strapi backend via `NEXT_PUBLIC_STRAPI_URL`)
- **UI/Animation**: framer-motion, lucide-react, react-icons, swiper, react-fast-marquee
- **Content rendering**: react-markdown, rehype-katex, rehype-highlight, rehype-raw, remark-gfm, remark-math
- **Charts**: react-chartjs-2, chartjs-plugin-datalabels
- **Forms**: react-hook-form, sweetalert2
- **PDF/Image**: jspdf, html-to-image (certificate generation)
- **SEO**: next-sitemap
- **Image optimization**: sharp

## Directory Structure

```
pymc-rebranded-website/
├── app/                    # Next.js App Router (22 page routes)
│   ├── api/                # Client-side API wrappers (blog, certificate, contact, promotion-bars)
│   ├── about/
│   ├── benchmark/LLMPriceIsRight/  # LLM benchmark tool (3 sub-pages)
│   ├── blog-posts/         # Blog listing + [id] detail + filters/[category]
│   ├── cancel/             # Payment cancellation
│   ├── congratulations/    # Payment success
│   ├── contact/
│   ├── courses/            # 4 individual course pages + listing
│   │   ├── ai-assisted-data-science/
│   │   ├── applied-bayesian-modeling/
│   │   ├── applied-bayesian-regression-modeling/
│   │   └── bayesian-marketing-analytics/
│   ├── draft-post/[id]/    # Draft blog preview
│   ├── privacy-policy/
│   ├── team/               # Team listing
│   ├── team-detail/[id]/   # Individual team member
│   ├── terms-and-conditions/
│   └── verify/[id]/        # Certificate verification
├── components/             # 80 component files across 15 directories
│   ├── Payments/           # Stripe integration
│   ├── about/
│   ├── benchmark/          # LLM benchmark components
│   ├── blog/
│   ├── contact/
│   ├── courses/
│   ├── home/
│   ├── industries/         # (draft feature)
│   ├── layout/             # Header, Footer, navigation
│   ├── privacy-policy/
│   ├── services/           # (draft feature)
│   ├── shared/             # Reusable components
│   ├── team/
│   └── ui/                 # Base UI components
├── config/                 # API base URL config
├── draft/                  # 5 draft pages (industries, services, solutions)
├── libs/                   # Auth, GTM, HTTP client, SEO, team utils
├── public/                 # 174 static assets (151 images), 32 MB total
│   ├── clients/            # Client logos
│   ├── courses/            # Course images
│   ├── home/
│   ├── industries/
│   ├── marimo/             # Embedded marimo notebooks
│   ├── services/
│   ├── solutions/
│   ├── svg/                # Icon SVGs
│   ├── team/               # Team headshots
│   └── users/
├── utils/                  # Navigation items, footer, dates, LLM benchmark data
├── package.json
├── next.config.mjs
├── tailwind.config.mjs
└── postcss.config.mjs
```

## Route Map (22 pages)

| Route | Type | Notes |
|-------|------|-------|
| `/` | Static | Home page |
| `/about` | Static | About page |
| `/blog-posts` | Dynamic | Blog listing (fetches from Strapi) |
| `/blog-posts/[id]` | Dynamic | Single blog post |
| `/blog-posts/filters/[category]` | Dynamic | Blog filtered by category |
| `/draft-post/[id]` | Dynamic | Draft blog preview |
| `/team` | Dynamic | Team listing |
| `/team-detail/[id]` | Dynamic | Team member profile |
| `/courses` | Static/Dynamic | Course listing |
| `/courses/ai-assisted-data-science` | Static | Course detail |
| `/courses/applied-bayesian-modeling` | Static | Course detail |
| `/courses/applied-bayesian-regression-modeling` | Static | Course detail |
| `/courses/bayesian-marketing-analytics` | Static | Course detail |
| `/contact` | Static | Contact form |
| `/benchmark/LLMPriceIsRight` | Static | LLM benchmark tool |
| `/benchmark/LLMPriceIsRight/leaderboard` | Static | Benchmark leaderboard |
| `/benchmark/LLMPriceIsRight/add-model` | Static | Add model to benchmark |
| `/cancel` | Static | Payment cancellation |
| `/congratulations` | Static | Payment success |
| `/verify/[id]` | Dynamic | Certificate verification |
| `/privacy-policy` | Static | Privacy policy |
| `/terms-and-conditions` | Static | Terms and conditions |

## Redirects (from next.config.mjs)

| Source | Destination | Type |
|--------|-------------|------|
| `/what-we-do` | `/` | Permanent |
| `/team/:id` | `/team-detail/:id` | Permanent |
| `/impressum` | `/about` | Permanent |
| `/products` | `/#products` | Permanent |
| `/clients` | `/#clients` | Permanent |
| HTTP requests | HTTPS redirect | Permanent |
| `pymc-labs.com` | `www.pymc-labs.com` | Permanent |

## Backend Integration

- **Strapi CMS** backend (URL via `NEXT_PUBLIC_STRAPI_URL` env var)
- API wrapper pattern in `app/api/` — client-side functions calling Strapi REST endpoints
- Strapi endpoints observed:
  - `GET /api/articles` — blog posts (with pagination, filtering, sorting)
  - `GET /api/articles?filters[slug][$eq]=...&populate=*` — single post
  - `PUT /api/certificates/:id/download` — certificate download tracking
  - `POST /api/contact-users` — contact form submission
  - `GET /api/promotion-bars` — promotional banners
- Auth via `libs/auth.utils.js`, HTTP client via `libs/http-client.js` (axios)
- Images served from Cloudinary (`res.cloudinary.com` in image config)

## Draft/In-Progress Features

5 draft pages in `draft/` directory (not routed):
- Industries listing + detail
- Services listing + detail
- Solutions listing

Components exist for these in `components/industries/` and `components/services/`.

## Notable Observations

1. **Unresolved merge conflict in README.md** — the file has raw conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
2. **Wildcard image domains** — `next.config.mjs` allows images from any `https://*` and `http://*` host (security concern)
3. **No Strapi source in this repo** — the Strapi backend is deployed separately; no `src/api/` Strapi code here
4. **LLM Benchmark tool** — custom interactive tool at `/benchmark/LLMPriceIsRight` (unique feature not in source site)
5. **Certificate system** — PDF generation (jspdf + html-to-image) with verification endpoint
6. **4 courses hardcoded** — individual course pages are static files, not CMS-driven
7. **30 branches** — active development with many feature branches, some stale
8. **Marimo notebooks** — embedded in `/public/marimo/` (blog widget)
