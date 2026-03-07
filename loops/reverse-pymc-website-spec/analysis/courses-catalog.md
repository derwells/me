# Courses Catalog

## Summary

5 course/workshop offerings across both sites: 1 generic corporate workshop page (Lektor) + 1 detailed hardcoded workshop page (Lektor) + 4 course detail pages (Next.js) + 1 course listing page (Next.js). All course content is 100% hardcoded in JSX/HTML — zero CMS integration. The Next.js site has evolved the "workshops" branding to "courses" with significant expansion (3 new courses added beyond the original Applied Bayesian Modeling).

## Lektor Site — Workshops

### Workshop Listing Page (`/workshops/`)

- **Route**: `/workshops/`
- **Model**: `generic_page` (uses flow blocks)
- **Content file**: `content/workshops/contents.lr`
- **Content**: Marketing copy describing corporate workshops, 4 anonymous student testimonials (blockquotes), 3 workshop levels mentioned (beginner/intermediate/advanced)
- **No individual course data** — just a generic pitch page with email CTA (`info@pymc-labs.com`)
- **References**: Wise.com payment links, PyMC docs link
- **Images**: `workshop_banner.png` (commented out), `workshop_logos.png`

### Applied Bayesian Modeling Workshop Page (`/workshops/applied-bayesian-modeling/`)

- **Route**: `/workshops/applied-bayesian-modeling/`
- **Model**: `page` (but uses custom template)
- **Template**: `templates/applied-bayesian-modeling.html` (fully hardcoded HTML, not CMS-driven)
- **Content file**: `content/workshops/applied-bayesian-modeling/contents.lr` — just sets `_hidden: true`, `_template: applied-bayesian-modeling.html`
- **Hidden**: `_hidden: true` (not linked from main navigation, direct access only)
- **Payment**: Direct Wise.com link (`https://wise.com/pay/r/elkuVRPWrYJR3rI`) — hardcoded, no server-generated URLs
- **Price**: $1,499 (early bird) / $1,699 (original) — hardcoded
- **Countdown timer**: JavaScript timer targeting `2025-08-05T15:00:00Z` (in workshop.js)
- **Course schedule**: 8 sessions, June 2-25, 11am-1pm ET
- **Instructors**: Chris Fonnesbeck, Allen Downey, Vianey Leos Barajas (hardcoded with bios and social links)
- **Testimonials**: 6 testimonials in carousel (screenshot images, not text)
- **Certificate**: Certificate of completion image, LinkedIn sharing
- **Client logos**: 15 logos from `/static/images/client_logos/` (different set than homepage)
- **FAQ**: 6 questions hardcoded
- **Terms**: Checkbox requirement before enrollment (JS-enforced)
- **Assets**: 2.7 MB in `assets/static/workshops/applied-bayesian-modeling/` (CSS, JS, instructor photos, workshop screenshots, certificate template, preview image)

## Next.js Site — Courses

### Course Listing Page (`/courses`)

- **Route**: `/courses`
- **Component**: `components/courses/CoursesContent.jsx` (client component)
- **Sections**: Hero, Features, CourseTypes (4 cards), Instructors carousel, TrustedBy, Testimonials carousel, FAQ
- **Course cards** (from `app/courses/components/CourseTypes.jsx`):

| # | Course | Action | Link |
|---|--------|--------|------|
| 1 | Applied Bayesian Modeling | Join the Waiting List | `/courses/applied-bayesian-modeling` |
| 2 | Bayesian Marketing Analytics | Join the Waiting List | `/courses/bayesian-marketing-analytics` |
| 3 | Applied Bayesian Regression Modeling | Join the Waiting List | `/courses/applied-bayesian-regression-modeling` |
| 4 | Custom Workshops | Request Info | `/contact` |

- **Instructors carousel** (from `app/courses/components/Instructors.jsx`): 6 instructors hardcoded — Allen Downey, Chris Fonnesbeck, Vianey Leos Barajas, Juan Orduz, Tim McWilliams, Nathaniel Ford (name misspelled — should be "Forde")
- **Testimonials** (from `app/courses/components/Testimonials.jsx`): 6 testimonials, 4 attributed to "Anjali Patel" / "Team Leader" (placeholder), 1 "Robert Fox" / "Web Designer", 1 "Liam Turner" / "Product Manager" — all using Unsplash stock photos (commented out in render). Names/avatars section is commented out, only quote text displays.

### Course Detail Pages — Shared Architecture

All 3 cohort courses reuse the `AppliedBayesianModeling` component (`app/courses/applied-bayesian-modeling/AppliedBayesianModeling.jsx`) as a shared layout. This 844-line monolith (self-described as "TODO: this is a quick migration from the old website") accepts `content` and `faqList` props.

**Shared features across all cohort course pages:**
- `isCourseLive` flag controls enrollment vs waiting list mode
- Registration form → POST to Strapi `/api/registration-form/submit` → returns Wise payment URL
- Waiting list form → same Strapi endpoint with `isWaitingList: true`
- Promo code modal → validates via Strapi `/api/coupons/validate-title` → returns discount + custom Wise link
- Certificate verification modal → Strapi certificate lookup/download
- Countdown timer hardcoded to `2025-08-05T15:00:00Z` (stale date, shared across all courses)
- GTM tracking on enrollment clicks (`trackEnrollNow`, `trackMakePayment`)
- GA4 client ID extracted from cookies and sent with registration
- JSON-LD structured data (`@type: Course`) with `CourseInstance`
- framer-motion animations
- `console.log` statements left in production code

### Course 1: Applied Bayesian Modeling

| Field | Value |
|-------|-------|
| **Route** | `/courses/applied-bayesian-modeling` |
| **Level** | Beginner - Intermediate |
| **Duration** | 4 weeks, 8 sessions |
| **Schedule** | Mon/Wed, 11am-1pm ET |
| **Dates (JSON-LD)** | Jan 12 - Feb 4, 2026 |
| **Price** | $1,499 (early bird) / $1,699 (original) |
| **isCourseLive** | `false` (waiting list mode) |
| **Instructors** | Allen Downey, Vianey Leos Barajas, Chris Fonnesbeck |
| **Topics** | Intro to Bayesian modeling, Priors/Likelihood, Building Models, Bayesian Regression, Hierarchical Models, MCMC, Causal Inference, Time Series |
| **Prerequisites** | Python, NumPy, Jupyter Notebooks |
| **Testimonials** | 6 hardcoded (anonymous, with workshop screenshot images) |
| **OG Image** | Cloudinary (`dx3t8udaw`) |
| **Certificate** | Yes (template image at `/courses/applied-bayesian-modeling/certificate-template.png`) |
| **Assets** | 2.7 MB (instructor photos, workshop screenshots, certificate template, banner) |

**Bug**: Allen Downey's instructor `href` points to `#vianey-leos-barajas` instead of `#allen-downey`. Vianey's `href` points to `#allen-downey` instead of `#vianey-leos-barajas`. The anchor links are swapped.

### Course 2: Applied Bayesian Regression Modeling

| Field | Value |
|-------|-------|
| **Route** | `/courses/applied-bayesian-regression-modeling` |
| **Level** | Beginner |
| **Duration** | 4 weeks, 8 sessions |
| **Schedule** | Mon/Wed, 3-5pm EST |
| **Dates (JSON-LD)** | Mar 3 - Mar 26, 2026 |
| **Price** | $1,499 (early bird) / $1,699 (original) |
| **isCourseLive** | `false` (waiting list mode) |
| **Instructors** | Juan Orduz, Ben Vincent, Nathaniel Forde |
| **Topics** | Intro to Regression, Intro to Bambi, Model Interpretation, Hierarchical Models, Gaussian Processes/Splines, MRP, Causal Inference, Survival Analysis |
| **Prerequisites** | Python, basic regression, intro Bayesian stats |
| **Tools** | Bambi, PyMC, ArviZ |
| **Testimonials** | None (reuses parent component's hardcoded testimonials, but carousel section is commented out) |
| **OG Image** | Cloudinary (`dx3t8udaw`) |
| **Twitter image** | Empty string `""` |
| **Certificate** | Shares ABM certificate section |

**Bug**: `startDate` is `null` but `endDate` is "March 26" — inconsistent, hero will show "join the waiting list" but course outline shows specific dates.

### Course 3: Bayesian Marketing Analytics

| Field | Value |
|-------|-------|
| **Route** | `/courses/bayesian-marketing-analytics` |
| **Level** | Beginner |
| **Duration** | 4 weeks, 9 sessions (8 + 1 optional pre-install) |
| **Schedule** | Mon/Wed, 3-5pm EST |
| **Dates (JSON-LD)** | Feb 2 - Feb 26, 2026 (but schedule shows Jan 29 pre-session) |
| **Price** | $2,249 (early bird) / $2,499 (original) — **highest priced** |
| **isCourseLive** | `false` (waiting list mode) |
| **Instructors** | Timothy McWilliams (lead, all sessions), Carlos Trujillo, Ben Vincent, Colt Allen (guest sessions) |
| **Topics** | Marketing Analytics, MMM Fundamentals, Hierarchical/Advanced MMMs, Optimization/Scenario Planning, Calibrating with Quasi-experiments, CLV Modeling, Bass Diffusion, Customer Choice Modeling |
| **Prerequisites** | Python, regression, probability, marketing domain knowledge |
| **Tools** | PyMC-Marketing, CausalPy |
| **Testimonials** | None (carousel section commented out) |
| **OG Image** | Cloudinary (`dx3t8udaw`) |
| **Certificate** | Shares ABM certificate section |
| **Price comment** | `// you can adjust price if needed` — developer note left in code |

### Course 4: Applied AI-Assisted Data Science

| Field | Value |
|-------|-------|
| **Route** | `/courses/ai-assisted-data-science` |
| **Level** | Beginner - Intermediate |
| **Duration** | Tailored (no fixed schedule) |
| **Schedule** | No fixed dates |
| **Price** | $2,000 (shown in AiPricing component) |
| **isCourseLive** | `false` (waiting list mode) |
| **Instructors** | Hugo Bowne-Anderson ("The Educator"), Thomas Wiecki ("The Scientist"), Luca Fiaschi ("The Strategist") — no photos, just initials |
| **Curriculum** | 4 sessions: Setup & Planning, Descriptive & Diagnostic, Predictive & Prescriptive, Final Capstone |
| **Prerequisites** | Not specified (generic "teams" focus) |
| **Certificate** | Not mentioned (no certificate section in AI page client) |
| **OG Image** | Cloudinary (`dx3t8udaw`) — reuses ABM course image |

**Completely different page architecture**: Uses `AiPageClient` instead of `AppliedBayesianModeling`. Has 12 custom section components (`AiAssistedHero`, `AiFeatures`, `AiAboutCourse`, `AiInstructors`, `AiWhoFor`, `AiWhyBuilt`, `AiWhyTake`, `AiCurriculum`, `AiPricing`, `AiTestimonials`, `AiCommunity`, `AiFaq`). Dark theme design vs blue theme for cohort courses.

**Testimonials are 100% placeholder**:
- 3 text testimonials all say "Akari helped us cut project delays by 40%..." — this is template text from a different product
- Names: "Gustavo Workman", "Martin Westervelt", "Livia Levin" — all fake
- All 3 have role "Head of Operations, AltForms" — template placeholder
- Companies: "Product.", "Sitemark", "luminous" — template brands
- 2 video testimonials with no actual videos (just thumbnail images)
- 1 pricing testimonial: "Jordon Huge", "AI Automation Engineer" — also appears to be placeholder

## Cross-Site Comparison

| Aspect | Lektor | Next.js |
|--------|--------|---------|
| **Branding** | "Workshops" | "Courses" |
| **Number of offerings** | 1 (ABM only) + generic page | 4 (ABM + Regression + Marketing + AI) |
| **Content source** | Hardcoded HTML template | Hardcoded JSX props |
| **Payment** | Direct Wise.com link | Server-generated Wise URL via Strapi |
| **Promo codes** | None | Strapi coupon validation |
| **Registration** | None (direct payment link) | Full registration form → Strapi |
| **Waiting list** | None | Strapi-backed waiting list form |
| **Certificates** | Static image only | Dynamic: verify by ID, download by email, PDF generation |
| **Tracking** | None | GTM + GA4 client ID on registration |
| **Terms** | JS checkbox before payment link | Checkbox in registration form |
| **Schedule dates** | June 2-25 (2025) | Jan-Mar 2026 cohorts |
| **ABM instructors** | Same 3 | Same 3 |
| **ABM price** | Same ($1,499/$1,699) | Same ($1,499/$1,699) |

## Instructor Roster Across All Courses

| Instructor | ABM (Lektor) | ABM (Next.js) | Regression | Marketing | AI |
|------------|:---:|:---:|:---:|:---:|:---:|
| Allen Downey | Yes | Yes | - | - | - |
| Chris Fonnesbeck | Yes | Yes | - | - | - |
| Vianey Leos Barajas | Yes | Yes | - | - | - |
| Juan Orduz | - | - | Yes | - | - |
| Ben Vincent | - | - | Yes | Yes | - |
| Nathaniel Forde | - | - | Yes | - | - |
| Timothy McWilliams | - | - | - | Yes (lead) | - |
| Carlos Trujillo | - | - | - | Yes | - |
| Colt Allen | - | - | - | Yes | - |
| Hugo Bowne-Anderson | - | - | - | - | Yes |
| Thomas Wiecki | - | - | - | - | Yes |
| Luca Fiaschi | - | - | - | - | Yes |

**Total unique instructors**: 12

## Registration & Payment Flow

```
User clicks "Enroll Now" / "Join Waiting List"
    |
    v
isCourseLive === true?
    |--- Yes --> RegistrationForm modal
    |               |
    |               v
    |           POST /api/registration-form/submit
    |           { name, email, role, organization, heardFrom, workshopType, clientId }
    |               |
    |               v
    |           Strapi returns { success: true, url: "https://wise.com/pay/r/..." }
    |               |
    |               v
    |           window.open(url) --> Wise.com payment page
    |
    |--- No --> WaitingListForm modal
                    |
                    v
                POST /api/registration-form/submit
                { name, email, role, organization, heardFrom, workshopType, isWaitingList: true }
                    |
                    v
                Success popup

PromoCodeModal (currently disabled/commented out in most places):
    POST /api/coupons/validate-title { title: promoCode }
    Returns { match: true, discount: N, wiseLink: "..." }
    Adjusts price display + stores discount Wise link
```

## Static Assets

| Location | Files | Size |
|----------|-------|------|
| Lektor: `assets/static/workshops/applied-bayesian-modeling/` | 16 files (CSS, JS, images) | 2.7 MB |
| Lektor: `content/workshops/` | 2 images (banner, logos) | ~100 KB |
| Next.js: `public/courses/applied-bayesian-modeling/` | 13 files (instructor photos, workshop screenshots, certificate, banner) | 2.7 MB |
| Next.js: `public/courses/ai-assisted-data-science/` | 15 files (hero, cards, pain points, testimonial, community map) | 1.1 MB |
| Cloudinary (Next.js courses) | Instructor photos, OG images | External CDN |

**Total local course assets**: ~6.6 MB

## Issues Found

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| 1 | **High** | AI course testimonials are 100% placeholder from a template ("Akari" product text, fake names/companies) | `app/courses/ai-assisted-data-science/AiTestimonials.jsx` |
| 2 | **High** | All course content is hardcoded — no CMS. Adding/editing courses requires code changes and redeployment | All course `page.js` files |
| 3 | **Medium** | Countdown timer hardcoded to `2025-08-05` — stale date, shows 0:0:0:0 for all courses | `AppliedBayesianModeling.jsx:69` |
| 4 | **Medium** | Allen Downey's instructor anchor href points to `#vianey-leos-barajas` and vice versa (swapped) | `app/courses/applied-bayesian-modeling/page.js:247,259` |
| 5 | **Medium** | Instructor name misspelled: "Nathaniel Ford" should be "Nathaniel Forde" | `app/courses/components/Instructors.jsx:39` |
| 6 | **Medium** | Course listing testimonials use placeholder names ("Anjali Patel" x4) with Unsplash stock photos | `app/courses/components/Testimonials.jsx` |
| 7 | **Medium** | `console.log("Show discount link", ...)` and `console.log("clen", ...)` in production registration form | `RegistrationForm.jsx:24,120` |
| 8 | **Medium** | AI course pricing page testimonial from "Jordon Huge, AI Automation Engineer" appears to be placeholder | `AiPricing.jsx:125-139` |
| 9 | **Low** | AI course reuses ABM OG image (`Starting_January_12_1`) — wrong branding | `app/courses/ai-assisted-data-science/page.js:16` |
| 10 | **Low** | Regression course has empty Twitter image string `""` | `app/courses/applied-bayesian-regression-modeling/page.js:28` |
| 11 | **Low** | Marketing course price has developer comment `// you can adjust price if needed` | `app/courses/bayesian-marketing-analytics/page.js:40` |
| 12 | **Low** | Regression course `startDate` is null but `endDate` is "March 26" — inconsistent display | `app/courses/applied-bayesian-regression-modeling/page.js:35-37` |
| 13 | **Low** | ABM monolith component is 844 lines with TODO comment acknowledging it needs refactoring | `AppliedBayesianModeling.jsx:1-2` |
| 14 | **Low** | Lektor ABM page is `_hidden: true` — likely superseded by Next.js version but still accessible | `content/workshops/applied-bayesian-modeling/contents.lr:4` |
| 15 | **Low** | Testimonials and Industries sections commented out in `AppliedBayesianModeling.jsx` but code still present | `AppliedBayesianModeling.jsx:387-535` |
| 16 | **Low** | JSON-LD script id is `blog-posting-jsonld` despite being a Course schema | `app/courses/applied-bayesian-modeling/page.js:317` |
| 17 | **Low** | `totalHistoricalEnrollment: 0` in all course JSON-LD — either not tracked or not updated | All course `page.js` files |
| 18 | **Info** | AI course has completely different page architecture (12 custom components vs shared AppliedBayesianModeling) | `app/courses/ai-assisted-data-science/` |
| 19 | **Info** | Duplicate instructor photo assets — Lektor and Next.js both have identical ABM instructor images locally | Both repos |
