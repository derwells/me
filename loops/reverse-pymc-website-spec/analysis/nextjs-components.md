# Next.js Components Analysis

## Component Inventory

**Total component files: 80** (across `components/`, `app/`, `libs/`, `utils/`)

### Directory Structure

```
components/           # 80 files in 12 subdirectories
  layout/             # 2 — Navbar, Footer (app chrome)
  shared/             # 11 — Reusable cross-page components
  ui/                 # 3 — Primitive UI components
  home/               # 13 — Homepage sections
  blog/               # 11 — Blog listing/detail components
  contact/            # 4 — Contact form variants
  team/               # 2 — Team card/detail
  courses/            # 1 — CoursesContent
  about/              # 3 — About page sections
  benchmark/          # 11 — LLM Price Is Right tool
  industries/         # 5 — Draft industry pages
  services/           # 6 — Draft service pages
  Payments/           # 2 — Stripe payment result pages
  privacy-policy/     # 1 — Privacy policy content

app/                  # Route-colocated components
  courses/components/ # 7 — Shared course landing components
  courses/ai-assisted-data-science/  # 12 inline components (Ai* prefix)
  courses/applied-bayesian-modeling/components/  # 8 — Registration, certificate, promo
  team-detail/[id]/   # 2 — EmptyState, Skeleton
  blog-posts/[id]/    # 1 — PostDetailsClient

libs/                 # 5 — Utility modules (not components)
utils/                # 7 — Helper functions and data
config/               # 1 — API base URL export
```

## Architecture Overview

### Layout System

The app uses a **"use client" root layout** anti-pattern (`app/layout.js:1`). The entire app is client-rendered:

1. **`app/layout.js`** — Root layout, "use client". Loads fonts (Roboto, Inter), GTM, HubSpot, Bing validation, FA 6.7.2 via CDN, Swiper CSS. Generates page titles via pathname switch-case. Embeds Organization JSON-LD.
2. **`app/ClientProvider.jsx`** — Wraps all pages with Navbar + ContactPopup modal + Footer. Manages contact modal state at app level.
3. **`components/layout/Navbar.jsx`** — Fixed top nav, scroll-aware styling, mobile slide-in drawer (framer-motion). Reads nav items from `utils/NavItems.js`. Supports dropdown menus. GTM tracking on contact click.
4. **`components/layout/Footer.jsx`** — Newsletter subscription via Mailchimp JSONP (hardcoded list ID `cdca7f3ebb`), social links (Bluesky, X, Meetup, YouTube, LinkedIn), footer nav from `utils/FooterItems.js`. Uses SweetAlert2 for feedback.
5. **`components/shared/Layout.jsx`** — Simple `max-w-7xl mx-auto` container wrapper. Used by most section components.

### Shared Components (11 files)

| Component | Purpose | Data Source | Notes |
|-----------|---------|-------------|-------|
| `Layout` | Max-width container | Props | Trivial wrapper |
| `Hero` | Blue overlay hero with Swiper slides | Props | Used on About page |
| `DynamicHero` | Background-image hero | Props | CSS class-based bg switching |
| `DynamicHero2` | Animated circles hero | Props | Floating framer-motion circles |
| `ContactUs` | Full contact form section | Strapi `/api/contact-users` | react-hook-form + SweetAlert2 |
| `FAQ` | Carousel FAQ | **Hardcoded** | Payment gateway placeholder text (!!) |
| `Pagination` | Page number buttons | Props | Duplicated — also exists in `blog/Pagination.jsx` |
| `Partners` | Partner bios layout | Props (from team data) | Alternating image/text layout |
| `Slider` | Blog post Swiper carousel | Props (blog data) | Uses ThreeDCard |
| `ContentVedio` | Content + video/image split | Props | Typo in name ("Vedio") |
| `DunamicCard` | Animated card with icon | Props | Typo in name ("Dunamic") |
| `SolutionsSection` | Image + content grid | Props | Uses `dangerouslySetInnerHTML` for paragraph |

### UI Primitives (3 files)

| Component | Purpose | Notes |
|-----------|---------|-------|
| `Button` | Polymorphic button/link | Supports `as="button"` or `as="link"` |
| `Card3D` | 3D tilt card on mouse hover | Context-based (MouseEnterContext). Exports CardContainer, CardBody, CardItem |
| `CardHover` | Hover effect grid with animated background | Uses framer-motion layoutId animation |

### Page-Specific Component Breakdown

#### Home (13 files)
- `HomeContent` — Orchestrator: Hero > HeroSlider > WhatWeDo > AboutUs > Innovation > FeaturedBlogs
- `Hero` — Video background hero with "Bayesian AI Consultancy" heading, mobile-aware animations
- `HeroSlider` — Logo carousel (client logos)
- `Logos` — Custom requestAnimationFrame-based scrolling logo strip (18 client logos hardcoded as paths)
- `Testimonials` — Swiper carousel, **6 testimonials hardcoded** (Colgate-Palmolive, SALK, Akili, Indigo, Ovative, Haleon)
- `Stats` — Commented out in HomeContent
- `FeaturedBlogs/index.jsx` — Featured blog posts from Strapi API
- `FeaturedBlogs/ThreeDCard.jsx` — 3D hover blog card
- `FeaturedBlogs/3DOld.jsx` — Legacy version (unused)
- `ContactPopup` — Modal contact form
- `AboutUs`, `Inovation`, `WhatWeDo` — Marketing content sections

#### Blog (11 files)
- `BlogContent` — Main blog listing orchestrator. Fetches from Strapi `/api/articles`. Client-side pagination (48 per page), category filtering via `/api/categories`, debounced search. Contains `console.log` in production code.
- `BlogCard` — 3-column grid card with Cloudinary image loader
- `FeaturedBlog` — Featured post hero card
- `Filter` — Category filter bar (first 4 shown, rest in dropdown)
- `Pagination` — Blog-specific pagination (different from shared/Pagination!)
- `Newsletter` — Mailchimp subscription (same JSONP as Footer)
- `TableOfContents` — Auto-generated TOC for blog posts
- `PostSkeleton`, `BlogCardsSkeleton`, `FeaturedSkeleton` — Loading states
- `EmptyState`, `NoPostFound` — Empty states
- `data.js` — Blog-related static data

#### Contact (4 files — 3 different contact form implementations!)
1. `ContactFormForPage` — Full-page form with inquiry category + discovery source dropdowns. Posts to Strapi `/api/contact-form/submit`. Uses axios directly.
2. `ContactFormModal` — Modal version of contact form
3. `ContactUsForm` — Another form variant
4. `Form` — Generic form component
- Plus `shared/ContactUs` — yet another contact form (4th implementation)

#### Team (2 files + hardcoded data)
- `TeamCard` — Grid of non-partner team members. Uses FA icons via CDN class names (`fab fa-github`).
- `TeamDetails` — Individual team member detail view
- **Dual data source**: Strapi API for partner data vs `libs/team.js` hardcoded array (29 members with JSX bios)

#### Courses (complex, mixed architecture)
- `app/courses/components/` — 7 shared course components (Hero, FAQ, Feature, Instructors, Testimonials, CourseTypes, TrustedBy)
- `app/courses/ai-assisted-data-science/` — 12 inline components all with `Ai` prefix (AiHero, AiCurriculum, AiFaq, AiPricing, etc.)
- `app/courses/applied-bayesian-modeling/components/` — 8 components including RegistrationForm, CertificateCanvas, CertificateVerificationClient, PromoCodeModal, WaitingListForm, DownloadButton
- All 4 course detail pages are **fully hardcoded** — no CMS, no shared data model

#### Benchmark / LLM Price Is Right (11 files)
- Self-contained mini-app for LLM benchmarking
- `LLMPriceContent`, `TopModel`, `Methodology`, `DataMethodology`, `Evaluation`, `Caveats`, `BusinessApplication`, `ExampleProduct`, `Showcase`, `CallToAction`, `KeyFinding`
- Uses Chart.js (`react-chartjs-2`) + `chartjs-plugin-datalabels`
- Leaderboard data in `utils/leaderboard.json`

#### Payments (2 files)
- `CancelContent` — Stripe payment cancellation page
- `Congratulationscontent` — Stripe payment success page (note: inconsistent casing)

## Key Dependency Libraries

| Library | Version | Used For | Components Using |
|---------|---------|----------|-----------------|
| `framer-motion` | ^11.16.3 | Animations, page transitions | ~30+ components (pervasive) |
| `swiper` | ^11.2.6 | Carousels/sliders | Hero, Testimonials, Slider, Blog featured, HeroSlider |
| `react-hook-form` | ^7.54.2 | Form state | shared/ContactUs only |
| `sweetalert2` | ^11.17.2 | Alert dialogs | Footer, shared/ContactUs |
| `react-markdown` | ^10.0.1 | Blog content rendering | Blog detail, Navbar (promotion bar) |
| `react-chartjs-2` | ^5.3.0 | Charts | Benchmark components only |
| `lucide-react` | ^0.534.0 | Icons | ~5 components (Search, Loader2, CheckCircle2, X) |
| `react-icons` | ^5.4.0 | Icons | ~15 components (FA, Gr, Im, Bs icon sets) |
| Font Awesome 6.7.2 | CDN | Icons | Navbar (CDN link), TeamCard (class-based) |
| `axios` | ^1.7.9 | HTTP client | All API calls via `libs/http-client.js` |
| `react-syntax-highlighter` | ^15.6.1 | Code blocks | Blog detail |
| `rehype-katex` + `remark-math` | ^7/^6 | Math rendering | Blog detail |
| `katex` | ^0.16.27 | LaTeX rendering | Blog detail |
| `html-to-image` + `jspdf` | ^1.11/^3.0 | Certificate PDF generation | Course certificate components |
| `react-fast-marquee` | ^1.6.5 | Marquee animation | Unknown (not seen in components read) |
| `react-responsive` | ^10.0.0 | Media queries | Unknown |
| `react-typed` | ^2.0.12 | Typing animation | Unknown |
| `react-vertical-timeline-component` | ^3.5.3 | Timeline UI | Unknown (likely courses) |
| `tailwind-merge` + `clsx` | ^2.6/^2.1 | Class merging | `utils/utils.js` `cn()` helper |

## Utility Layer

### API Client (`libs/http-client.js`)
- Thin axios wrapper: `GetApiData(endpoint, method, payload, secured)`
- Base URL from `NEXT_PUBLIC_STRAPI_URL` env var
- Auth via `x-access-token` header from localStorage (SSR-unsafe, guarded with `typeof window`)

### API Service Modules (`app/api/*/index.js`)
- `blog` — `getBlogs()`, `getAllBlogs()`, `getSingleBlog()`, `getSingleDraftBlog()`
- `contact` — `SendContactForm()`
- `certificate` — `updateCertificateDownloadStatus()`
- `promotion-bars` — `getPromotionBar()` (commented out in Navbar)

### GTM Tracking (`libs/gtm.js`)
- Generic `trackEvent()` + specialized: `trackCTA()`, `trackContactUs()`, `trackEnrollNow()`, `trackMakePayment()`
- All use `window.dataLayer.push()` with 300ms callback delay

### SEO Helper (`libs/seo.js`)
- `createMetadata()` — Generates Next.js metadata object with OpenGraph + Twitter cards
- Hardcoded domain: `https://www.pymc-labs.com`
- Default OG image from Cloudinary

### Navigation Data
- `utils/NavItems.js` — 5 nav items: Home, About (/team), Blog, Courses, Resources (dropdown with LLM benchmark)
- `utils/FooterItems.js` — 3 items: Home, About, Blog (Industries/Services/Privacy commented out)

## Issues and Anti-Patterns

### Architecture Issues
1. **"use client" root layout** — Entire app is client-rendered, defeating Next.js SSR/SSG benefits
2. **No TypeScript** — All files are `.js`/`.jsx`, no type safety
3. **No error boundaries** — No error.js or not-found.js files
4. **Dual data sources for team** — Strapi API + hardcoded `libs/team.js` (29 members with JSX in data)
5. **Hardcoded course pages** — 4 courses fully hardcoded, no CMS integration

### Component Issues
6. **3-4 different contact form implementations** — `shared/ContactUs`, `contact/ContactFormForPage`, `contact/ContactFormModal`, `contact/Form` + home/ContactPopup
7. **Duplicate Pagination** — `shared/Pagination.jsx` and `blog/Pagination.jsx` are separate implementations
8. **3 icon libraries loaded simultaneously** — Font Awesome CDN (entire CSS), `lucide-react`, `react-icons` (multiple icon packs: fa, fa6, gr, im, bs)
9. **Typos in component names** — `ContentVedio`, `DunamicCard`, `VedioSection` (appears twice), `Inovation`, `Congratulationscontent`
10. **Placeholder content in shared FAQ** — Hardcoded "Instapay" and "ACME payment gateway" questions in `shared/FAQ.jsx` — clearly copied from a template

### Security/Quality Issues
11. **`dangerouslySetInnerHTML`** in SolutionsSection and layout JSON-LD — potential XSS if data is user-supplied
12. **`console.log` in production** — BlogContent, Footer (`subscribeUser`), utils (`ImageUrlValid`)
13. **External placeholder image** — Falls back to `developers.elementor.com` placeholder when images are missing
14. **Mailchimp JSONP** — Injects `<script>` tags into DOM for newsletter subscription (Footer + blog Newsletter) — fragile, no CSP-compatible
15. **No input sanitization** — Contact forms post raw user input to Strapi

### Missing Components
16. **No loading states** — Only blog has skeleton loaders
17. **No shared modal system** — ContactPopup is ad-hoc
18. **No toast/notification system** — Uses SweetAlert2 in some places, inline status text in others
19. **No image optimization strategy** — Mix of Cloudinary loader, direct URLs, and Next.js Image with wildcard domains

## Component Reuse Matrix

| Shared Component | Home | Blog | Team | About | Courses | Benchmark | Contact | Industries | Services |
|-----------------|------|------|------|-------|---------|-----------|---------|------------|----------|
| Layout | x | x | x | x | | | x | x | x |
| DynamicHero | | | | | | | | x | x |
| DynamicHero2 | | | x | | x | | | | |
| Hero (shared) | | | | x | | | | | |
| ContactUs | | | | | | | x | | |
| FAQ | | | | | | | | | x |
| Partners | | | x | | | | | | |
| Slider | | x | | | | | | | |
| SolutionsSection | | | | | | | | x | |
| DunamicCard | | | | | | | | x | x |
| ContentVedio | | | | x | | | | x | |
| Pagination (shared) | | | x | | | | | | |
| Button (ui) | | | | | x | | | | |

## Summary

The Next.js component architecture is a **flat, feature-first structure** with significant code duplication and inconsistency. Key concerns for the redesign:

- **80 component files** but low reuse — most are page-specific one-offs
- **Heavy client-side rendering** throughout (framer-motion dependency makes SSR difficult)
- **4 contact form variants** that should be 1
- **3 icon libraries** that should be 1
- **No component library or design system** — ad-hoc styling with CSS variables (`--color1`, `--color2`) and Tailwind
- **Hardcoded content throughout** — testimonials, team bios (JSX!), course details, FAQ placeholder text
- **Draft pages** (industries, services, solutions) in `draft/` directory — 5 pages not deployed but components exist in `components/industries/` and `components/services/`
