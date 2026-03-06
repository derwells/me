# Strapi API Endpoints

## Overview

The Next.js frontend communicates with a Strapi v4 backend hosted on Heroku (`pymc-backend-afc5c26e8ab7.herokuapp.com`). The base URL is configured via `NEXT_PUBLIC_STRAPI_URL` environment variable and consumed through a thin axios wrapper (`libs/http-client.js`).

## API Client Architecture

### HTTP Client (`libs/http-client.js`)
- Thin axios wrapper: `GetApiData(endpoint, method, payload, secured)`
- Prepends `API_BASE_URL` (from `config/index.jsx` = `process.env.NEXT_PUBLIC_STRAPI_URL`)
- Auth via `x-access-token` header from localStorage `user.token` (see `libs/auth.utils.js`)
- **Nearly all calls pass `secured=false`** — auth header is never attached in practice

### Dual Fetch Patterns
The codebase uses two conflicting patterns to call Strapi:
1. **Via `GetApiData` wrapper** — `app/api/blog/index.js`, `app/api/contact/index.js`, `app/api/certificate/index.js`, `app/api/promotion-bars/index.js`, `components/blog/BlogContent.jsx`
2. **Direct `fetch()`/`axios` with inline URLs** — `app/team/page.jsx`, `app/team-detail/[id]/page.jsx`, `app/verify/[id]/page.js`, all course components, `components/contact/ContactFormModal.jsx`, `components/contact/ContactFormForPage.jsx`, `components/benchmark/AddModalContent.jsx`

This inconsistency means some server-side calls use native `fetch()` with ISR revalidation (team pages), while client-side calls use axios without caching.

## Endpoint Catalog

### 1. Articles (Blog)

| Endpoint | Method | Auth | Source File | Notes |
|----------|--------|------|-------------|-------|
| `/api/articles?populate[categories]=true&populate[cover]=true&pagination[page]={p}&pagination[pageSize]={n}&sort=createdAt:desc` | GET | No | `app/api/blog/index.js:4` | Paginated blog listing with optional filter query |
| `/api/articles?pagination[pageSize]=1000&sort=createdAt:desc` | GET | No | `app/api/blog/index.js:16` | All blogs (up to 1000) — used by FeaturedBlogs and sitemap |
| `/api/articles?filters[slug][$eq]={slug}&populate=*` | GET | No | `app/api/blog/index.js:25` | Single blog by slug with all relations |
| `/api/articles?filters[slug][$eq]={slug}&populate=*&status=draft` | GET | No | `app/api/blog/index.js:33` | Draft blog preview — **unauthenticated access to unpublished content** |
| `/api/articles?filters[featured][$eq]=true&...` | GET | No | `components/home/FeaturedBlogs/index.jsx:20` | Featured articles filter (up to 100) |

**Query Parameters Used:**
- `populate[categories]=true`, `populate[cover]=true`, `populate=*`
- `pagination[page]`, `pagination[pageSize]`
- `sort=createdAt:desc`
- `filters[slug][$eq]`, `filters[featured][$eq]=true`
- `status=draft` (Strapi v4 draft/publish)
- Arbitrary filter queries passed from blog search/filter UI

### 2. Categories

| Endpoint | Method | Auth | Source File | Notes |
|----------|--------|------|-------------|-------|
| `/api/categories?populate[blogs][fields][0]=id&populate[blogs][fields][1]=publishedAt` | GET | No | `components/blog/BlogContent.jsx:62` | Categories with blog counts (for filter sidebar) |
| `/api/categories` | GET | No | `next-sitemap.config.js:22` | All categories for sitemap generation |

### 3. Teams

| Endpoint | Method | Auth | Source File | Notes |
|----------|--------|------|-------------|-------|
| `/api/teams?populate=*&filters[isVisible][$eq]=true&sort=orderNumber:asc,name:asc&pagination[page]=1&pagination[pageSize]=40` | GET | No | `app/team/page.jsx:18` | Team listing, server-side with `revalidate: 60` (ISR) |
| `/api/teams?filters[slug][$eq]={id}&populate=*` | GET | No | `app/team-detail/[id]/page.jsx:9` | Single team member by slug, server-side with `revalidate: 60` |

**Notes:**
- Uses native `fetch()` (not GetApiData) for Next.js ISR compatibility
- Team data is **also** hardcoded in `libs/team.js` (29 members) as a fallback/overlay — dual data source issue

### 4. Certificates

| Endpoint | Method | Auth | Source File | Notes |
|----------|--------|------|-------------|-------|
| `/api/certificates/verify/{id}` | GET | No | `app/verify/[id]/page.js:10`, `CertificateVerificationClient.jsx:67` | Verify certificate by VerifyId — returns PascalCase fields (AttendeeName, WorkshopTitle, CompletionDate, VerifyId, CertificateImage) |
| `/api/certificates/{id}/download` | PUT | No | `app/api/certificate/index.js:4` | Mark certificate as downloaded — **unauthenticated PUT** |
| `/api/certificates/email/{email}` | GET | No | `VerifyCertificateModal.jsx:26` | Lookup certificate by email — returns VerifyId or "Nothing found" |

**Custom Routes (non-standard Strapi):**
- `GET /api/certificates/verify/:id` — custom controller
- `PUT /api/certificates/:id/download` — custom controller (state mutation without auth)
- `GET /api/certificates/email/:email` — custom controller

### 5. Contact Forms (3 systems)

#### System A: Legacy Contact Users
| Endpoint | Method | Auth | Source File | Notes |
|----------|--------|------|-------------|-------|
| `/api/contact-users` | POST | No | `app/api/contact/index.js:4` | Standard Strapi collection create. Used by `components/shared/ContactUs.jsx`. Includes server-side rate limiting ("already contacted us recently"). Payload: `{ data: { firstName, lastName, email, message } }` |

#### System B: Contact Form (newer)
| Endpoint | Method | Auth | Source File | Notes |
|----------|--------|------|-------------|-------|
| `/api/contact-form/submit` | POST | No | `components/contact/ContactFormModal.jsx:86`, `ContactFormForPage.jsx:100` | Custom route handler. Payload: `{ data: { firstName, lastName, email, phoneNumber, message, inquiryCategory, discoverySource? } }`. Returns `{ success: true }`. |

**ContactFormModal vs ContactFormForPage:**
- Modal version: 6 fields (no discoverySource)
- Page version: 7 fields (adds discoverySource dropdown)
- Both POST to same endpoint — duplicate implementations with slightly different field sets

**Inquiry Categories (hardcoded in both):**
1. Expert Access Program
2. Workshop
3. Consulting And Custom Bayesian Models
4. MMM Insights Agent
5. General Inquiry

**Discovery Sources (page version only):**
1. Social media (LinkedIn, X, Bluesky)
2. Google search
3. Colleague or referral
4. GitHub / Open-source libraries
5. Newsletter or event
6. Other

#### System C: Legacy ContactUs shared component
Uses System A endpoint (`/api/contact-users`) with react-hook-form and SweetAlert2. Fields: firstName, lastName, email, message. Has rate-limit error handling.

### 6. Registration Forms

| Endpoint | Method | Auth | Source File | Notes |
|----------|--------|------|-------------|-------|
| `/api/registration-form/submit` | POST | No | `RegistrationForm.jsx:122`, `WaitingListForm.jsx:98` | Custom route. Returns `{ success: true, url: "..." }` where url is a payment link. |

**Registration Payload:**
```json
{
  "data": {
    "name": "...",
    "email": "...",
    "role": "...",
    "organization": "...",
    "message": "...",
    "termsAccepted": true,
    "heardFrom": "...",
    "workshopType": "/applied-bayesian-modeling",
    "clientId": "GA4-client-id",
    "isWaitingList": false  // true for WaitingListForm
  }
}
```

**Response:**
- `{ success: true, url: "https://wise.com/pay/r/..." }` — dynamic Wise.com payment link
- Server generates payment URL based on registration (replaces previously hardcoded Wise links)

**heardFrom Options:** PyMC Labs Website, PyMC Labs newsletter, LinkedIn, Twitter/BlueSky, Referral from colleague/friend

### 7. Coupons

| Endpoint | Method | Auth | Source File | Notes |
|----------|--------|------|-------------|-------|
| `/api/coupons/validate-title` | POST | No | `PromoCodeModal.jsx:27` | Custom route. Payload: `{ title: "PROMO_CODE" }`. Returns `{ match: true, discount: 20, wiseLink: "..." }` or `{ match: false }`. Discount applied as percentage off $1699 base price. |

### 8. Benchmark

| Endpoint | Method | Auth | Source File | Notes |
|----------|--------|------|-------------|-------|
| `/api/benchmark/submit` | POST | No | `components/benchmark/AddModalContent.jsx:35` | Custom route. Payload: `{ data: { modelName, apiUrl, apiKey, description } }`. Accepts LLM model submissions for "Price Is Right" benchmark. **API keys submitted in plaintext over the wire.** |

### 9. Promotion Bars

| Endpoint | Method | Auth | Source File | Notes |
|----------|--------|------|-------------|-------|
| `/api/promotion-bars` | GET | No | `app/api/promotion-bars/index.js:4` | Standard Strapi collection list. Used by Navbar to show site-wide promotional banner. |

## Next.js API Route (Internal)

| Endpoint | Method | Notes |
|----------|--------|-------|
| `/blog-posts/{id}/md` | GET | `app/blog-posts/[id]/md/route.js` — Converts blog post to markdown. Server-side only, calls Strapi internally via `getSingleBlog()`. Returns `text/markdown`. |

## External Third-Party Endpoints

### Mailchimp Newsletter (JSONP)
- **URL:** `https://twiecki.us10.list-manage.com/subscribe/post-json?u=ffcf543278f48b79571b62010&id=cdca7f3ebb&f_id=003f33e2f0`
- **Used in:** `components/layout/Footer.jsx:63`, `components/blog/Newsletter.jsx:23`
- **Method:** JSONP via dynamic script injection (not `fetch()`)
- **Params:** `EMAIL`, `subscribe=Subscribe`, dynamic callback name
- **Issues:** Duplicate implementation (Footer + Newsletter), JSONP is deprecated/insecure, list credentials hardcoded in client-side JS

### Sitemap (Hardcoded Heroku URL)
- `next-sitemap.config.js:10` and `:22` use hardcoded `https://pymc-backend-afc5c26e8ab7.herokuapp.com/api/...` instead of `NEXT_PUBLIC_STRAPI_URL`
- Fetches all articles and categories at build time for sitemap generation

## Environment Variables

| Variable | Purpose | Notes |
|----------|---------|-------|
| `NEXT_PUBLIC_STRAPI_URL` | Strapi backend base URL | Points to Heroku deployment |
| `NEXT_PUBLIC_GTM_ID` | Google Tag Manager ID | GTM tracking |
| `NEXT_PUBLIC_SITE_URL` | Canonical site URL | Used in layout for canonical URLs |
| `NEXT_PUBLIC_BASE_URL` | Base URL for certificate verification links | Used in LinkedIn share URLs |

## Summary Statistics

- **Total unique Strapi endpoints:** 15 (9 standard CRUD + 6 custom route handlers)
- **Custom routes:** `/registration-form/submit`, `/contact-form/submit`, `/certificates/verify/:id`, `/certificates/:id/download`, `/certificates/email/:email`, `/coupons/validate-title`, `/benchmark/submit`
- **Authenticated endpoints:** 0 (all calls pass `secured=false` or use direct fetch without auth)
- **Total external integrations:** 2 (Mailchimp JSONP, Wise.com payment links)

## Issues and Concerns

1. **Zero authentication on all endpoints** — Draft blog access, certificate state mutation (PUT), benchmark submissions with API keys, and all form submissions are unauthenticated
2. **Draft blog access without auth** — `getSingleDraftBlog()` exposes unpublished content to anyone with the slug
3. **Unauthenticated PUT on certificates** — `PUT /api/certificates/{id}/download` mutates state without any auth check
4. **API keys in plaintext** — Benchmark model submissions include API keys without transport-level protection beyond HTTPS
5. **Hardcoded Heroku URL in sitemap** — `next-sitemap.config.js` bypasses the env var, creating a deployment coupling
6. **Dual fetch patterns** — Mix of GetApiData wrapper and direct fetch/axios makes it hard to add global error handling, caching, or auth
7. **3 duplicate contact systems** — contact-users (legacy), contact-form/submit (modal), contact-form/submit (page) — different field sets, different UX patterns, same purpose
8. **Duplicate Mailchimp JSONP** — Same subscription logic copy-pasted in Footer and Newsletter components
9. **No API error boundaries** — Most components catch errors with `console.error` + SweetAlert, no centralized error handling
10. **JSONP for newsletter** — Deprecated pattern, script injection vector, Mailchimp list credentials exposed in client JS
11. **No rate limiting visible on most endpoints** — Only contact-users has server-side rate limiting (legacy system); newer contact-form/submit does not
12. **Wildcard image domains** — `next.config.mjs` allows `hostname: '*'` for both HTTP and HTTPS, enabling SSRF via image optimization
