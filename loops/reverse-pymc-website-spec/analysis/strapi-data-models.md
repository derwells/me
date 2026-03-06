# Strapi Data Models — Reverse-Engineered from Frontend

## Key Finding

The Strapi backend source code is **not included** in the `pymc-rebranded-website` repository. Strapi runs as a separate deployment on Heroku (`pymc-backend-afc5c26e8ab7.herokuapp.com`). All data models below are **reverse-engineered** from the Next.js frontend's API calls, component field access patterns, and response shapes.

## Architecture

- **Backend URL**: Configured via `NEXT_PUBLIC_STRAPI_URL` env var
- **Hardcoded in sitemap**: `https://pymc-backend-afc5c26e8ab7.herokuapp.com`
- **Auth**: Token-based (`x-access-token` header from localStorage), but most endpoints called with `secured: false`
- **API Style**: Strapi v4 REST API (standard `?populate=*`, `?filters[...]`, `?pagination[...]` query params)
- **Media**: Cloudinary (2 accounts, per previous analysis)

## Content Types (Collections)

### 1. `article` (API: `/api/articles`)

The primary blog content type. Queried with pagination, filtering, sorting, and population.

| Field | Type | Evidence | Required |
|-------|------|----------|----------|
| `id` | Integer | Strapi default | Yes |
| `title` | String | `post?.title` — used in blog cards, detail, metadata | Yes |
| `slug` | String | `filters[slug][$eq]=${slug}` — URL routing key | Yes |
| `description` | String | `post?.description` — used in featured blog, JSON-LD | No |
| `detail` | RichText/Markdown | `post?.detail` — rendered via ReactMarkdown | Yes |
| `cover` | Media (relation) | `post?.cover?.url` — Cloudinary image | No |
| `video` | String (URL) | `post.video` — YouTube embed or direct video URL | No |
| `featured` | Boolean | `post?.featured` — determines featured blog display | No |
| `blog_created_date` | Date | `post?.blog_created_date` — custom date field (preferred over createdAt) | No |
| `meta_title` | String | `post?.meta_title` — SEO override title | No |
| `meta_description` | String | `post?.meta_description` — SEO override description | No |
| `categories` | Relation (many-to-many) | `populate[categories]=true`, `post.categories[0].name` | No |
| `authors` | Relation (one-to-many or many-to-many) | `post.authors?.map(a => a.name)` — array with `id`, `name` | No |
| `createdAt` | DateTime | Strapi default, fallback for blog_created_date | Auto |
| `updatedAt` | DateTime | Used in sitemap `lastmod` | Auto |
| `publishedAt` | DateTime | Used in category filtering (`blog.publishedAt`) | Auto |
| `status` | Enum (draft/published) | `&status=draft` query param for draft preview | Auto |

**API Endpoints Used**:
- `GET /api/articles?populate[categories]=true&populate[cover]=true&pagination[page]=X&pagination[pageSize]=Y&sort=createdAt:desc` — paginated list
- `GET /api/articles?filters[slug][$eq]=SLUG&populate=*` — single blog by slug
- `GET /api/articles?filters[slug][$eq]=SLUG&populate=*&status=draft` — draft preview
- `GET /api/articles?pagination[pageSize]=1000&sort=createdAt:desc` — all blogs (sitemap, home featured)
- `GET /api/articles?filters[categories][name][$eq]=X&...` — category filter
- `GET /api/articles?filters[title][$containsi]=X&...` — title search

### 2. `category` (API: `/api/categories`)

Blog categories with relation back to articles.

| Field | Type | Evidence |
|-------|------|----------|
| `id` | Integer | Strapi default |
| `name` | String | `cat.name` — displayed as filter chips and blog tags |
| `slug` | String (likely) | URL-generated from name: `name.toLowerCase().replace(/\s+/g, "-")` |
| `blogs` | Relation (many-to-many to articles) | `populate[blogs][fields][0]=id&populate[blogs][fields][1]=publishedAt` |
| `updatedAt` | DateTime | Used in sitemap |

**API Endpoints Used**:
- `GET /api/categories?populate[blogs][fields][0]=id&populate[blogs][fields][1]=publishedAt` — categories with blog counts
- `GET /api/categories` — plain list (sitemap)

### 3. `author` (inferred from article relation)

Referenced through article's `authors` relation. Minimal fields visible.

| Field | Type | Evidence |
|-------|------|----------|
| `id` | Integer | `a.id` in author map |
| `name` | String | `a.name` — displayed as byline |

**Note**: Authors appear as a separate content type (not just a text field), evidenced by `post.authors?.map(a => <span key={a.id}>{a.name}</span>)`. However, no direct `/api/authors` endpoint is called from the frontend.

### 4. `team` (API: `/api/teams`)

Team member profiles. This is the CMS-managed version (in addition to the hardcoded `libs/team.js` array of 29 members).

| Field | Type | Evidence |
|-------|------|----------|
| `id` | Integer | Strapi default |
| `name` | String | `member.name` |
| `slug` | String | `filters[slug][$eq]=${id}` — URL routing |
| `desc` | String | `member.desc` / `details?.desc` — role/title |
| `bio` | JSON (string array) | `Array.isArray(member.bio)`, `details?.bio?.map(item => ...)` |
| `profile_image` | Media (relation) | `member.profile_image?.url` — Cloudinary image |
| `linkedin` | String (URL) | `details?.linkedin` |
| `twitter` | String (URL) | `details?.twitter` |
| `github` | String (URL) | `details?.github` |
| `website` | String (URL) | `details?.website` / `member.website` |
| `medium` | String (URL) | `member.medium` — in JSON-LD sameAs (team-detail page) |
| `partner` | Boolean | `item?.partner === true/false` — separates "Our Partners" from "Our Team" |
| `isVisible` | Boolean | `filters[isVisible][$eq]=true` — visibility toggle |
| `orderNumber` | Integer | `sort=orderNumber:asc,name:asc` — display ordering |
| `specializations` | Relation or JSON | `details?.specializations?.map(s => s.name)` — array of objects with `name` |
| `location` | String | `details?.location` |

**API Endpoints Used**:
- `GET /api/teams?populate=*&filters[isVisible][$eq]=true&sort=orderNumber:asc,name:asc&pagination[page]=1&pagination[pageSize]=40` — team list
- `GET /api/teams?filters[slug][$eq]=SLUG&populate=*` — single team member

**ISR**: Both endpoints use `next: { revalidate: 60 }` (60-second incremental static regeneration).

### 5. `certificate` (API: `/api/certificates`)

Course completion certificates with verification and download tracking.

| Field | Type | Evidence |
|-------|------|----------|
| `id` | Integer | Strapi default |
| `AttendeeName` | String | `certificateData.AttendeeName` — PascalCase field naming |
| `Email` | String | `certificateData.Email` (commented out in UI but present in data) |
| `WorkshopTitle` | String | `certificateData.WorkshopTitle` |
| `CompletionDate` | Date | `certificateData.CompletionDate` |
| `VerifyId` | String | `certificateData.VerifyId` — public verification ID |
| `CertificateImage` | Media (relation) | `certificateData.CertificateImage?.url` — in OG metadata |

**API Endpoints Used (Custom Controllers)**:
- `GET /api/certificates/verify/:id` — verify certificate by VerifyId (public)
- `GET /api/certificates/email/:email` — look up certificate by email, returns `{ VerifyId }` or `{ message: "Nothing found" }`
- `PUT /api/certificates/:id/download` — track download event

**Note**: PascalCase field naming (`AttendeeName`, `WorkshopTitle`) is unusual for Strapi — suggests custom controller that transforms the response or a non-standard content type definition.

### 6. `contact-user` (API: `/api/contact-users`)

Legacy contact form submissions (used by the shared `ContactUs` component).

| Field | Type | Evidence |
|-------|------|----------|
| `firstName` | String | react-hook-form `register("firstName")` |
| `lastName` | String | react-hook-form `register("lastName")` |
| `email` | String | react-hook-form `register("email")` |
| `message` | Text | react-hook-form `register("message")` |

**API Endpoints Used**:
- `POST /api/contact-users` — standard Strapi collection create

**Note**: Has rate limiting — error message: "You have already contacted us recently. Please wait before submitting again." This suggests a custom lifecycle hook or middleware on the Strapi side.

### 7. `contact-form` (Custom Route: `/api/contact-form/submit`)

Newer contact form submissions (used by `ContactFormModal` and `ContactFormForPage`).

| Field | Type | Evidence |
|-------|------|----------|
| `firstName` | String | `formData.firstName` |
| `lastName` | String | `formData.lastName` |
| `email` | String | `formData.email` |
| `phoneNumber` | String | `formData.phoneNumber` (optional) |
| `message` | Text | `formData.message` |
| `inquiryCategory` | Enum/String | Options: "Expert Access Program", "Workshop", "Consulting And Custom Bayesian Models", "MMM Insights Agent", "General Inquiry" |
| `discoverySource` | Enum/String | Options: "Social media", "Google search", "Colleague or referral", "GitHub", "Newsletter or event", "Other" (only in page version) |

**API Endpoints Used**:
- `POST /api/contact-form/submit` — custom route (not standard Strapi CRUD), returns `{ success: true }`

**Note**: Two separate contact form implementations exist — `ContactFormModal` omits `discoverySource`, `ContactFormForPage` includes it. Both POST to the same endpoint.

### 8. `registration-form` (Custom Route: `/api/registration-form/submit`)

Course registration and waiting list. Custom controller that processes payment.

| Field | Type | Evidence |
|-------|------|----------|
| `name` | String | Participant name |
| `email` | String | Participant email |
| `role` | String | Optional |
| `organization` | String | Optional |
| `message` | Text | Optional (commented out in registration, visible in waiting list) |
| `termsAccepted` | Boolean | Required checkbox |
| `heardFrom` | Enum/String | Options: "PyMC Labs Website", "PyMC Labs newsletter", "LinkedIn", "Twitter/BlueSky", "Referral from colleague/friend" |
| `workshopType` | String | Auto-derived from URL pathname (e.g., "/applied-bayesian-modeling") |
| `clientId` | String | GA4 client ID (registration only) |
| `isWaitingList` | Boolean | `true` for waiting list, absent for registration |

**API Endpoints Used**:
- `POST /api/registration-form/submit` — returns `{ success: true, url: "..." }` where `url` is a payment link (Wise.com or Stripe)

**Note**: This is a custom controller — not standard Strapi CRUD. The response includes a dynamic payment URL, suggesting server-side payment link generation.

### 9. `coupon` (Custom Route: `/api/coupons/validate-title`)

Promo code validation for course discounts.

| Field | Type | Evidence |
|-------|------|----------|
| `title` | String | Coupon code string (sent as `{ title: promoCode }`) |
| `discount` | Number | Percentage discount (used as `data.discount / 100 * 1699`) |
| `wiseLink` | String (URL) | Discounted payment link |
| `match` | Boolean | Whether the coupon is valid (response field) |

**API Endpoints Used**:
- `POST /api/coupons/validate-title` — validates coupon, returns `{ match: true/false, discount, wiseLink }`

### 10. `promotion-bar` (API: `/api/promotion-bars`)

Site-wide promotional banner managed via CMS.

| Field | Type | Evidence |
|-------|------|----------|
| Unknown | Unknown | Consumed by `Navbar.jsx` — no field access visible beyond the API call |

**API Endpoints Used**:
- `GET /api/promotion-bars` — fetched in Navbar component

### 11. `benchmark` (Custom Route: `/api/benchmark/submit`)

LLM Price Is Right benchmark model submissions.

| Field | Type | Evidence |
|-------|------|----------|
| `modelName` | String | Required — e.g., "GPT-4 Custom" |
| `apiUrl` | String (URL) | Required — OpenAI-compatible endpoint |
| `apiKey` | String | Required — encrypted on server |
| `description` | Text | Optional |

**API Endpoints Used**:
- `POST /api/benchmark/submit` — custom route for model submission

**Note**: The leaderboard data itself is served from a static `leaderboard.json` file in the frontend (`utils/leaderboard.json`), not from Strapi. The submission endpoint is for new model intake only.

## Custom Routes Summary

The Strapi backend has at least **5 custom route handlers** beyond standard CRUD:

| Custom Route | Method | Purpose |
|--------------|--------|---------|
| `/api/certificates/verify/:id` | GET | Public certificate verification |
| `/api/certificates/email/:email` | GET | Certificate lookup by email |
| `/api/certificates/:id/download` | PUT | Track certificate download |
| `/api/contact-form/submit` | POST | Contact form with email notification |
| `/api/registration-form/submit` | POST | Course registration + payment link generation |
| `/api/coupons/validate-title` | POST | Promo code validation |
| `/api/benchmark/submit` | POST | LLM benchmark model submission |

## Data Model Diagram (Relations)

```
article ----* categories (many-to-many)
article ----* authors (many-to-many or one-to-many)
article ----> cover (media)

team ----> profile_image (media)
team ----* specializations (component or relation)

certificate (standalone, no visible relations)

coupon (standalone)
promotion-bar (standalone)
```

## Issues and Observations

1. **Duplicate contact systems**: Three separate contact mechanisms coexist:
   - `POST /api/contact-users` (legacy, with rate limiting)
   - `POST /api/contact-form/submit` (newer, with inquiry categories)
   - Mailchimp JSONP (newsletter subscription in Footer/blog)

2. **Inconsistent field naming**: Certificates use PascalCase (`AttendeeName`, `WorkshopTitle`) while all other content types use camelCase — suggests different developers or a custom controller that doesn't follow conventions.

3. **Dual team data**: CMS-managed teams via Strapi coexist with 29 hardcoded members in `libs/team.js`. The hardcoded version includes JSX in bios. No synchronization mechanism.

4. **No Strapi source in repo**: The backend is a black box from the frontend's perspective. Content type schemas, lifecycle hooks, middleware, custom controllers, and plugins are all unknown. This is a significant risk for the redesign.

5. **Hardcoded Heroku URL**: `next-sitemap.config.js` has the Strapi Heroku URL hardcoded instead of using `NEXT_PUBLIC_STRAPI_URL`, creating a deployment coupling.

6. **Missing auth on most endpoints**: Nearly all API calls pass `secured: false`, meaning the Strapi endpoints are publicly accessible. Certificate download tracking (`PUT`) is also unauthenticated.

7. **Payment link generation**: The registration form submission returns a dynamic payment URL, suggesting the Strapi backend integrates with Wise.com (or possibly Stripe) for payment link generation. Previously this was hardcoded Wise.com links (commented-out code still visible).

8. **Benchmark leaderboard is static**: Despite having a submission endpoint, the actual leaderboard data comes from a committed JSON file, not from Strapi. This creates a manual update bottleneck.

9. **No content versioning**: Draft blog preview exists (`?status=draft`) but there's no evidence of content versioning, scheduled publishing, or editorial workflow beyond draft/published states.

10. **Specializations model unclear**: Team specializations appear as `{ name: "..." }` objects but it's unclear if this is a Strapi component, a separate collection, or a JSON field.
