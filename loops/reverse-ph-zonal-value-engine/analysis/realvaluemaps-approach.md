# RealValueMaps Approach — Reverse Engineering

**Wave:** 4 — Competitive & Third-Party Analysis
**Date:** 2026-03-04
**Method:** Multi-angle investigation — WHOIS/domain analysis, JS bundle decompilation, sitemap/robots.txt analysis, API endpoint probing, JSON-LD extraction, Google index analysis, web search for operator identity and third-party citations
**Prior work:** `third-party-platform-survey.md` (Wave 1) documented RealValueMaps as a JS-heavy SPA with 2.7M+ records but minimal observable data. This analysis penetrates the SPA layer.

---

## Summary

RealValueMaps (realvaluemaps.com) is a **less than 11-month-old** (domain registered April 13, 2025), **anonymous**, **Singapore-registered** (JSON-LD claim), React/Vite SPA that claims 2.7M+ BIR zonal value records. Deep analysis of its JavaScript bundles, API endpoints, and structured data reveals a **commercially ambitious but operationally incomplete platform**: the API backend (`api.realvaluemaps.com`) is currently serving an Open WebUI AI chat instance instead of zonal value data, the classification taxonomy in its JS config uses LGU SMV tier codes (R1-R3, C1-C3, I1-I3) instead of BIR Annex B codes (RR, CR, RC, CC), key statistics are hardcoded in the frontend with fabricated social proof (10,247 reviews, 99.8% accuracy — zero external reviews exist), and the codebase contains template placeholder URLs (`github.com/yourusername/realvaluemaps-frontend`). Despite this, the technical architecture demonstrates several genuinely interesting design choices — PSGC-based location identification, Leaflet map with dynamic GeoJSON barangay boundaries, viewport-based data loading, and reverse geocoding — that represent the most sophisticated mapping approach in the Philippine zonal value space.

**Assessment: Operationally non-functional as of March 2026. Architecture is template-scaffolded with ambitious feature design but unverified data. API backend has been replaced/overwritten. Not a competitive threat, but the map-based UX concept and PSGC integration are worth noting as design validation for our engine.**

---

## 1. Domain & Identity

### Domain Registration (WHOIS)

| Field | Value |
|-------|-------|
| **Registrar** | NameCheap, Inc. (IANA ID: 1068) |
| **Created** | April 13, 2025 |
| **Expires** | April 13, 2026 |
| **Nameservers** | aiden.ns.cloudflare.com, anita.ns.cloudflare.com |
| **IP Address** | 104.21.88.5 (Cloudflare range) |
| **Privacy** | Withheld for Privacy ehf (Iceland-based privacy service) |
| **Domain Status** | clientTransferProhibited |

The domain is **less than 11 months old**. The registrant identity is fully redacted behind NameCheap's privacy service.

### Dual Domain Problem

- **Primary operational domain:** `realvaluemaps.com` (serves the SPA, TLS works)
- **Claimed canonical domain:** `realvaluemaps.ph` (referenced in robots.txt and sitemap.xml)
- **Status of .ph:** TLS connection failures on every fetch attempt; zero Google indexed pages
- **Interpretation:** Either a failed domain migration (.ph → .com) or the .ph was the original plan but was never operationalized. The sitemap/robots.txt config files reference `.ph` but the actual HTML `<link rel="canonical">` correctly uses `.com`.

### Operator Identity

**Unknown.** Every investigation vector returned empty:

| Vector | Result |
|--------|--------|
| Website About page | SPA shell, no renderable content |
| WHOIS | Privacy-shielded |
| LinkedIn company page | Not found |
| Facebook / Twitter / Instagram | Not found |
| Crunchbase / PitchBook / GetLatka | Not found |
| Philippine SEC/DTI registration | Not found |
| News articles / press coverage | Zero |
| Reddit / Facebook groups / forums | Zero mentions |
| Blog posts by or about | Zero |
| Third-party citations | Zero |

### JSON-LD Organization Claim

The frontend generates client-side JSON-LD with this organization block:

```json
{
  "@type": "Organization",
  "name": "RealValueMaps",
  "address": {
    "streetAddress": "Digital Office",
    "addressLocality": "Singapore",
    "addressRegion": "Singapore",
    "postalCode": "018989",
    "addressCountry": "SG"
  },
  "contactPoint": {
    "telephone": "+63-2-8888-4444",
    "contactType": "Customer Service",
    "areaServed": "PH",
    "availableLanguage": ["English", "Filipino", "Cebuano"]
  },
  "sameAs": [
    "https://facebook.com/realvaluemaps",
    "https://twitter.com/realvaluemaps",
    "https://linkedin.com/company/realvaluemaps"
  ],
  "foundingDate": "2024"
}
```

**Problems with this claim:**
1. "Digital Office" at Singapore postal code 018989 — this is the Marina Bay area; "Digital Office" is not a real street address
2. Phone number +63-2-8888-4444 — PH country code, looks like a generic/placeholder number
3. All three `sameAs` social profiles (Facebook, Twitter, LinkedIn) — **none exist**
4. Claims founding in 2024, but domain registered April 2025

This JSON-LD appears to be **aspirational/template content**, not verified business information.

---

## 2. Technology Stack

### Confirmed Stack (from JS bundle analysis)

| Layer | Technology | Evidence |
|-------|-----------|----------|
| **Frontend Framework** | React | `react-vendor-fb33f09a.js` chunk (138 KB) |
| **Build Tool** | Vite | Asset hashing pattern (`index-d9f2f610.js`), modulepreload links |
| **Router** | React Router v6.x | `@remix-run/router v1.23.0` (router-vendor chunk) |
| **Map Library** | Leaflet 1.9.4 | `map-vendor-20236363.js` chunk, unpkg CDN CSS |
| **Map Tiles** | CARTO Voyager | `{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png` |
| **Charts** | Chart.js | `chart-vendor-e7180a51.js` chunk |
| **CSS** | Tailwind CSS | `tw-` prefixed classes, standard breakpoints |
| **Icons** | Lucide | Detected in bundle |
| **i18n** | react-i18next | Supports English, Filipino/Tagalog, Cebuano |
| **Analytics** | Google Analytics 4 | `G-R03W6GPKEL` (conditional: disabled in dev) |
| **CDN/Proxy** | Cloudflare | CF-Ray headers, Cloudflare IP range |
| **Backend API** | `api.realvaluemaps.com` | Preconnect header, but currently broken |

### Wappalyzer Additional Detections

Wappalyzer detected additional third-party integrations in the site scripts:

| Service | Purpose | Significance |
|---------|---------|--------------|
| **Amazon Cognito** | User auth | User Pool + Identity Pool in ap-southeast-2 (Sydney) |
| **Stripe** | Payments | Live public key detected (not test mode) |
| **Pipedrive** | CRM | Sales pipeline management |
| **HubSpot** | CRM | Marketing/customer management |
| **AWS S3** | Asset hosting | `s3.amazonaws.com` references |

**Note:** Wappalyzer also flagged Nuxt.js (Vue.js), but the direct bundle analysis definitively shows React + Vite (not Vue/Nuxt). The Wappalyzer Vue detection is likely a false positive from Vite build patterns.

### Bundle Sizes

| Asset | Size | Notes |
|-------|------|-------|
| Main JS | 622 KB | Application logic, routes, components |
| React vendor | 138 KB | React runtime |
| Router vendor | — | React Router v6 |
| Chart vendor | — | Chart.js |
| Map vendor | — | Leaflet 1.9.4 |
| CSS | 68 KB | Tailwind compiled |
| **Total initial** | **~1 MB** | Before any data loading |

### Key Infrastructure Choice: Sydney (ap-southeast-2)

Amazon Cognito is configured in **ap-southeast-2 (Sydney, Australia)** — not ap-southeast-1 (Singapore) which would be the standard choice for a Philippines-serving platform. This adds ~50ms latency for PH users compared to Singapore. Possible explanations:
- Developer/operator is based in Australia
- Accidental region selection during setup
- Following a template that defaulted to Sydney

---

## 3. API Architecture (Currently Non-Functional)

### API Domain Status

`api.realvaluemaps.com` is **currently serving an Open WebUI instance** (self-hosted LLM chat interface) instead of the expected REST API:

- Nginx 1.29.3 server header
- `meta name="robots" content="noindex,nofollow"`
- Splash screen, theme system, manifest.json — all Open WebUI artifacts
- Only `/health` returns proper JSON: `{"status": true}`
- All other API endpoints return Open WebUI HTML shell

**Interpretation:** The API backend has been either:
1. Replaced/overwritten by deploying Open WebUI to the same subdomain
2. Taken down and the domain repurposed for AI experimentation
3. Never fully operationalized — the frontend was built against a planned API that was never production-deployed

### Discovered API Endpoints (from JS Bundle)

Despite the API being non-functional, the frontend code reveals the complete planned API surface:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check (only working endpoint) |
| `/api/search?q={query}&limit={n}` | GET | Location search |
| `/api/suggestions?q={query}` | GET | Search autocomplete |
| `/api/stats/summary` | GET | Dashboard statistics |
| `/api/stats/comprehensive` | GET | Detailed statistics |
| `/api/rdo/list` | GET | List of Revenue District Offices |
| `/api/rdo-coverage` | GET | RDO coverage statistics |
| `/api/effectivity-dates` | GET | Zonal value effectivity dates |
| `/api/psgc/search?q={query}&limit={n}` | GET | PSGC code search |
| `/api/locations/coordinates?barangay={name}` | GET | Barangay lat/lng |
| `/api/locations/coordinates?municipality={name}` | GET | Municipality lat/lng |
| `/api/locations-with-coordinates?q={query}&limit={n}` | GET | Location search with coordinates |
| `/api/location/{municipality}/{barangay}?classification={code}` | GET | Zonal values for a location |
| `/api/viewport-data?north={}&south={}&east={}&west={}&zoom={}` | GET | Map boundary polygons |
| `/api/reverse-geocode?lat={}&lng={}` | GET | Lat/lng → barangay |
| `/api/barangay/{psgc_code}/detail` | GET | Barangay detail page |
| `/api/municipalities?province={name}` | GET | Municipality listing |
| `/api/v1/zonal-values` | GET | Data export/download |

**18 endpoints** — this is a comprehensive API design that covers search, map, statistics, location hierarchy, and data export. If functional, it would be the most complete API in the Philippine zonal value space. But it appears to be **vaporware** as of March 2026.

### PSGC Integration (Noteworthy Design Choice)

The API uses **Philippine Standard Geographic Code (PSGC)** as a location identifier:
- `/api/psgc/search` for PSGC code lookup
- `/barangay/:psgc_code` route for direct PSGC-based navigation
- PSGC appears in reverse geocoding responses

PSGC is the authoritative Philippine government geographic coding system. Using it as the primary location key (rather than free-text city/barangay names) is architecturally sound — it eliminates name ambiguity and enables direct linkage to PSA census data and other government datasets. **This is a design decision our engine should adopt.**

---

## 4. Map-Based Approach (Key Differentiator)

### Map Architecture

RealValueMaps is the **only platform with a map-based interface** among all surveyed competitors:

| Component | Implementation |
|-----------|---------------|
| **Map library** | Leaflet 1.9.4 |
| **Base tiles** | CARTO Voyager (OpenStreetMap data) |
| **Boundary data** | Dynamic GeoJSON barangay polygons |
| **Loading strategy** | Viewport-based (`/api/viewport-data?north=&south=&east=&west=&zoom=`) |
| **Caching** | Client-side, max 20 entries |
| **Interaction** | Click polygon → load barangay zonal values |
| **Reverse geocode** | Custom `/api/reverse-geocode?lat=&lng=` endpoint |

### Viewport-Based Data Loading

The map loads barangay boundary polygons dynamically based on the visible viewport:
```
/api/viewport-data?north={lat}&south={lat}&east={lng}&west={lng}&zoom={level}
```

This is the standard approach for data-dense mapping — only load geometries visible on screen. At low zoom levels, show municipality/city boundaries; at higher zoom, show individual barangay polygons. This prevents loading all 42,011 barangay boundaries simultaneously.

### GeoJSON Boundary Source

The planned boundary data likely comes from one of two Philippine GeoJSON sources:
1. **faeldon/philippines-json-maps** (GitHub) — region/province/municipality/barangay GeoJSON/TopoJSON, the standard open-source Philippine mapping dataset
2. **PSA PSGC boundary files** — official government boundaries, though less commonly in web-ready formats

### Assessment of Map Approach

**Strengths:**
- Visual, intuitive — click a location on the map to see zonal values
- Eliminates address matching entirely for map users — point-and-click bypasses text input
- Barangay boundaries provide immediate spatial context
- Reverse geocoding enables "what zonal value applies to this GPS point?" queries

**Weaknesses:**
- Doesn't solve the core BIR matching problem — BIR zonal values are assigned by street/vicinity, not by barangay polygon
- Within a single barangay, multiple streets have different zonal values (often 5-50x range)
- Map click → barangay → shows all values for that barangay ≠ address-level lookup
- Barangay boundary accuracy varies (PSA boundaries don't always match BIR's barangay assignments)
- Mobile UX: map interaction on small screens is significantly harder than text input

**Our engine's position:** A map interface is a **nice-to-have complement** to text-based address matching, not a replacement. The core resolution pipeline (address → barangay → street → vicinity → classification → zonal value) remains text-based. A map can serve as an input method (click → reverse geocode → feed into text pipeline) and as a visualization layer (show results on a map with barangay context).

---

## 5. Data Model & Classification Errors

### Claimed Data Model (from JS Bundle)

The JSON-LD Dataset block claims:
- **2.7M+ records** across 42,011 barangays and 121 RDOs
- **Temporal coverage:** 1989-2025
- **License:** CC-BY-4.0 (claiming BIR public data under Creative Commons)
- **Format:** `application/json` via `/api/v1/zonal-values`
- **Variables:** Zonal Value per sqm (PHP/m2), Property Classification

### Classification Taxonomy Problem

The classification codes hardcoded in the frontend JavaScript are **fundamentally wrong for BIR zonal value data**:

| RealValueMaps Taxonomy | BIR Annex B Standard | Issue |
|----------------------|---------------------|-------|
| R1 (Low Density Residential) | RR (Residential Regular) | R1/R2/R3 are LGU SMV tier codes |
| R2 (Medium Density) | — | Not a BIR classification |
| R3 (High Density) | — | Not a BIR classification |
| C1 (Neighborhood Commercial) | CR (Commercial Regular) | C1/C2/C3 are LGU SMV tier codes |
| C2 (Major Commercial) | — | Not a BIR classification |
| C3 (Central Business) | — | Not a BIR classification |
| CBD (Central Business District) | — | Not a BIR classification |
| I1 (Light Industrial) | I (Industrial) | BIR uses single "I" code |
| I2 (Medium Industrial) | — | Not a BIR classification |
| I3 (Heavy Industrial) | — | Not a BIR classification |
| A1 (Agricultural) | A (Agricultural) / A1-A50 | BIR A1 = "Riceland Irrigated", not generic |
| A2 (Agricultural Residential) | — | Not a BIR classification |
| AG (General Agricultural) | — | Not a BIR classification |
| AX (Mixed Agricultural) | — | Not a BIR classification |
| GP (General Purpose) | GP (Govt Purpose) ≥5,000 sqm | Different meaning in BIR context |

**This is a critical data model error.** BIR uses 63 functional classification codes (RR, CR, RC, CC, PS, X, I, GL, GP, CL, APD, DA, A, plus A1-A50 agricultural subcodes). RealValueMaps uses what appears to be an **LGU SMV/zoning taxonomy** (R1-R3 density tiers, C1-C3 commercial tiers, I1-I3 industrial tiers). These are the kind of codes used in BLGF Schedule of Market Values, not BIR Zonal Value schedules.

**Possible explanations:**
1. The developer confused BIR zonal value classifications with LGU zoning classifications
2. The data model was designed from a template/specification document, not from actual BIR workbook data
3. The records were never actually parsed from BIR workbooks — the 2.7M figure may be fabricated

### Hardcoded Fallback Statistics

When the API fails (which is currently always), the frontend displays hardcoded statistics:

| Classification | Record Count | Avg Value (PHP/sqm) |
|---------------|-------------|---------------------|
| Agricultural | 449,234 | 124 |
| Residential | 352,482 | 2,972 |
| Commercial | 132,421 | 7,549 |
| Residential Condo | 89,234 | 15,234 |
| Industrial | 26,189 | 3,713 |
| General Purpose | 34,567 | 2,156 |
| Mixed Use | 12,345 | 4,523 |
| Special | 3,898 | 8,967 |
| **Total** | **~1,100,370** | — |

**Problem:** These sum to ~1.1M, not 2.7M. The "2.7M" headline figure is the claimed total, but the category breakdown accounts for only 41% of it. The missing 1.6M records are unaccounted for.

### Fabricated Social Proof

The JS config contains hardcoded metrics:
- **Data Accuracy: 99.8%** — no methodology, no audit, no basis
- **User Rating: 4.8** — zero external reviews exist on any platform
- **Total Reviews: 10,247** — completely fabricated (zero external reviews found)

---

## 6. Business Model

### Pricing Tiers (from JS Bundle)

| Plan | Price | Searches | API Calls | Features |
|------|-------|----------|-----------|----------|
| **Free** | PHP 0/month | 1,000/month | — | Basic info, limited historical |
| **Professional** | PHP 2,999/month (~$52/mo) | Unlimited | 10,000/month | Full historical, exports, priority support |
| **Enterprise** | PHP 9,999/month (~$173/mo) | Unlimited | Unlimited | Custom integrations, white-label, advanced analytics |

### Paywall Mechanism

The frontend uses `localStorage.searchCount` to track searches. After **5 free searches**, a paywall modal appears. Analytics tracks `paywall_encountered`, `upgrade_prompted`, `pricing_viewed`, `trial_started` events.

### Payment Infrastructure

- **Stripe:** Live public key detected (not test mode) — payment processing is wired up
- **Checkout path:** `/checkout/` blocked in robots.txt — checkout flow exists

### CRM Infrastructure

- **Pipedrive + HubSpot** — dual CRM suggests active sales pipeline management or a migration in progress
- This level of CRM tooling indicates serious commercial intent

### Assessment

Despite the ambitious monetization infrastructure (Stripe, dual CRM, 3-tier pricing), the platform cannot currently deliver its core value proposition because the API backend is non-functional. The pricing tiers reference API access (10,000 calls/month for Pro) for an API that doesn't serve data.

---

## 7. SEO & Discoverability

### Google Indexing

| Query | Results |
|-------|---------|
| `site:realvaluemaps.com` | **1 page** (homepage only) |
| `site:realvaluemaps.ph` | **0 pages** |

This is catastrophically poor for a site with 171 URLs in its sitemap. The SPA architecture with no server-side rendering means Google's crawler sees only the 4,915-byte HTML shell (no content). All content is rendered client-side via JavaScript.

### SEO Content Investment

Despite the indexing failure, the sitemap reveals significant content planning:
- **97 location pages** (Metro Manila, Cebu, Davao neighborhoods)
- **27 RDO pages**
- **10 educational guides** (zonal value explanation, CGT, estate tax, property transfer, etc.)
- **Multilingual:** English + Filipino + Cebuano support via react-i18next

None of this content is visible to search engines because of the SPA architecture.

### SEO Bot Blocking

robots.txt blocks SemrushBot, AhrefsBot, and MJ12bot — standard competitive intelligence tools. This suggests awareness of SEO competition but contradicts the stated goal of "We welcome all crawlers to index our comprehensive property data" in the robots.txt comment.

---

## 8. Sitemap Analysis (URL Taxonomy)

### 171 URLs, 5 Categories

**Core App (14 pages):**
- `/`, `/search`, `/map`, `/pricing`, `/calculator`, `/tax-calculator`, `/stats`
- `/about`, `/login`, `/register`, `/dashboard`, `/glossary`, `/privacy`, `/terms`

**Location Pages (97 pages):**
Three-level hierarchy: `/location/{region}/{city}/{neighborhood}`
- Metro Manila: Makati (10 neighborhoods), BGC-Taguig (5), Pasig (5), QC (10)
- Cebu: Cebu City (10), Mandaue (5), Lapu-Lapu (5)
- Davao: Davao City (10)

**RDO Pages (27 pages):**
Pattern: `/rdo/{city}` — 18 Metro Manila, 4 Cebu, 2 Davao, 3 other major cities

**Educational Guides (10 pages):**
- how-to-find-zonal-value, zonal-value-vs-market-value, capital-gains-tax-guide
- estate-tax-computation, property-transfer-guide, bir-requirements-2025
- real-estate-investment-guide, property-valuation-methods, tax-exemptions-guide
- first-time-buyer-guide

**Geographic Coverage Gap:** Sitemap location pages only cover **3 metro areas** (Metro Manila, Cebu, Davao) despite claiming 42,011 barangays and 121 RDOs nationwide. The vast majority of the claimed geographic coverage has no dedicated landing pages.

---

## 9. Comparison with Housal

| Dimension | RealValueMaps | Housal |
|-----------|--------------|--------|
| **Age** | ~11 months (Apr 2025) | ~8 years (2016/2018) |
| **Operator** | Unknown (Singapore claim) | Housal Inc., BGC (named CEO, ~20 staff) |
| **Records claimed** | 2.7M+ | 1.96M+ |
| **Records verified** | 0 (API non-functional) | ~123K probed across 4 cities |
| **Framework** | React + Vite | Next.js (React) |
| **Map interface** | Yes (Leaflet) | No |
| **API** | 18 endpoints designed, 0 functional | 3 internal endpoints, functional |
| **Classification codes** | Wrong taxonomy (R1/R2/R3) | BIR codes (RR, CR, RC, CC, PS) |
| **Pricing** | PHP 0/2,999/9,999/mo | Free (marketplace cross-sell) |
| **SEO indexed pages** | 1 | Many |
| **Social proof** | Zero (fabricated 10,247 reviews) | Limited but real company |
| **Data source** | Claimed BIR, unverified | BIR workbooks, verified |
| **DO#/effectivity** | Unknown | DO# in database but not in API |
| **RPVARA readiness** | Unknown (likely none) | Zero |
| **Revenue** | Unknown (probably $0) | ~$1.8M (marketplace) |

**Key differences:**
1. RealValueMaps is architecturally more ambitious (map interface, PSGC, reverse geocoding, 18 API endpoints, multilingual) but operationally vacant
2. Housal is less ambitious technically but actually functional with real data
3. RealValueMaps uses wrong classification codes — a fundamental data model error that Housal doesn't make
4. RealValueMaps' dual CRM + Stripe + 3-tier pricing suggests commercial ambition that far exceeds its current capabilities

---

## 10. What RealValueMaps Gets Right (Design Validation)

Despite the operational failures, several architectural choices are genuinely good and validate design decisions for our engine:

### 10.1 PSGC-Based Location Identification
Using Philippine Standard Geographic Codes as the canonical location key eliminates name ambiguity. Our engine should incorporate PSGC codes in the RDO jurisdiction mapping and barangay indexing.

### 10.2 Viewport-Based Map Data Loading
Loading GeoJSON boundaries by map viewport (`north/south/east/west + zoom`) is the correct approach for 42K+ barangay polygons. Our engine's optional map layer should use this pattern.

### 10.3 Reverse Geocoding
`/api/reverse-geocode?lat=&lng=` → barangay + municipality + province is a valuable input method. Users with GPS coordinates can bypass text-based address matching entirely. Our WASM engine should support coordinate-to-barangay lookup using PSGC boundary data.

### 10.4 Effectivity Date Tracking
The planned `/api/effectivity-dates` endpoint suggests awareness that legal effectivity dates are material — a feature no current competitor fully implements. Our engine tracks DO# and effectivity per revision.

### 10.5 Multilingual Support
English + Filipino + Cebuano (the three most-spoken languages in the Philippines) is appropriate for a nationwide tool. Our engine should note this as a future UX consideration.

---

## 11. What RealValueMaps Gets Wrong (Gaps)

### 11.1 Classification Taxonomy (Critical)
Using LGU SMV tier codes (R1-R3, C1-C3, I1-I3) instead of BIR Annex B codes (RR, CR, RC, CC, A1-A50) means the data model is structurally incompatible with actual BIR workbook data. This cannot be fixed with a mapping table — the taxonomies measure different things (density tiers vs. functional use codes).

### 11.2 No Address Matching
No evidence of address matching logic in the frontend or API design. The API uses barangay-level location keys (`/api/location/{municipality}/{barangay}`), not street/vicinity resolution. This means a user in Barangay Bel-Air would see ALL zonal values for that barangay (potentially 50+ entries ranging from ₱35,000 to ₱250,000/sqm) without street-level narrowing.

### 11.3 No Fallback Logic
No fallback hierarchy visible. If a location isn't in the database, the user gets nothing.

### 11.4 No Classification Resolution
No evidence of handling multi-classification properties, condo-specific rules, parking slot formulas, or institutional fallback logic.

### 11.5 SPA Without SSR (SEO Failure)
A pure client-side SPA for a content-heavy site is an architectural mistake. The 171 planned pages are invisible to search engines. This is a solved problem (Next.js SSR, Nuxt SSG, Astro, etc.) that they chose not to implement.

### 11.6 Fabricated Metrics
Hardcoding "99.8% accuracy" and "10,247 reviews" when zero external reviews exist is a trust-destroying choice if discovered by users or competitors.

### 11.7 API Backend Abandoned
The most critical gap: the entire backend API has been replaced by an Open WebUI instance. The frontend is an empty shell.

---

## 12. Competitive Gap Summary

| Gap | RealValueMaps | Housal | Our Engine |
|-----|--------------|--------|------------|
| Correct BIR classification codes | Wrong taxonomy | Partial (9 of 63) | All 63 + normalization |
| Street-level address matching | None | None | 8-phase pipeline |
| Fallback logic | None | None | 7-level decision tree |
| Classification resolution | None | None | 7 resolution paths |
| DO#/effectivity date | Planned, not implemented | In DB, not in API | Per-record, per-revision |
| Condo handling | None | Basic | 6 layout patterns + PS rules |
| RPVARA dual-source | None | None | 3-regime model |
| Map interface | Yes (Leaflet, non-functional) | None | Optional complement |
| PSGC integration | Yes (planned, non-functional) | None | Adopt for barangay keys |
| API access | 18 endpoints planned, 0 functional | 3 internal, undocumented | Designed in Wave 5 |
| Client-side privacy | SPA but server-dependent | Server-side | WASM engine, data stays local |
| Historical data | Claimed 1989-2025 | 1989-2024 | Full historical via workbook parsing |
| Data verified | No | Partially | Direct BIR workbook parsing |

---

## 13. Strategic Assessment

### Threat Level: NONE

RealValueMaps is not a competitive threat because:
1. **API is non-functional** — the backend has been replaced by an AI chat tool
2. **Wrong data model** — classification taxonomy is fundamentally incompatible with BIR data
3. **Zero social proof** — no external reviews, citations, or user community
4. **Less than 1 year old** with no visible traction
5. **Anonymous operator** with fabricated metrics

### Lessons to Absorb

Despite being non-functional, RealValueMaps' architecture provides useful design validation:
1. **PSGC codes** → adopt as canonical barangay identifier in our engine
2. **Map + reverse geocoding** → plan as optional input method (coordinate → barangay → text pipeline)
3. **Viewport-based boundary loading** → correct pattern for map UI layer
4. **Effectivity date API** → validates our per-revision DO# tracking
5. **Multilingual UX** → note for forward loop (English + Filipino + Cebuano)
6. **Freemium with API tiers** → validates commercial model (PHP 2,999/mo for API access)

### Template/AI-Generated Platform Hypothesis

Multiple signals suggest this may be a template-scaffolded or AI-generated platform:
- `github.com/yourusername/realvaluemaps-frontend` placeholder in code
- Fabricated statistics (reviews, accuracy ratings)
- JSON-LD with fake social profiles and "Digital Office" address
- Wrong classification taxonomy (copy-pasted from LGU/zoning context, not BIR)
- Ambitious architecture with zero operational data
- API domain repurposed for Open WebUI (developer experimentation over production)
- The entire site could have been generated by Claude/GPT with domain-specific prompts but without access to actual BIR workbook data

---

## Appendix A: Raw Data Points

### robots.txt (Full)
```
# RealValueMaps Robots.txt
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /dashboard/
Disallow: /checkout/
Crawl-delay: 1

Allow: /location/
Allow: /rdo/
Allow: /guide/
Allow: /search
Allow: /map
Allow: /pricing

Sitemap: https://realvaluemaps.ph/sitemap.xml

User-agent: Googlebot
Crawl-delay: 0

User-agent: Googlebot-Image
Allow: /images/
Allow: /og-images/

User-agent: SemrushBot
Disallow: /
User-agent: AhrefsBot
Disallow: /
User-agent: MJ12bot
Disallow: /
```

### Meta Tags (Main Page)
- `lang="en-PH"`
- `description`: "Access 2.7M+ BIR zonal value records across 42,011 barangays and 121 RDOs. Find Philippine zonal values instantly. More comprehensive than competitors."
- `keywords`: "Philippine zonal values, BIR zonal values, property values Philippines, real estate valuation, Bureau of Internal Revenue, property search, zonal value finder"
- `author`: "RealValueMaps Team"
- `og:locale`: `en_PH`
- `theme-color`: `#1e40af` (blue)
- Language alternates: `en`, `tl` (Tagalog), `ceb` (Cebuano)
- PWA: `mobile-web-app-capable: yes`, `apple-mobile-web-app-capable: yes`

### HTML Shell Size
- 92 lines, 4,915 bytes
- Content: `<div id="root"></div>` (all rendering is client-side)

### Google Analytics
- `G-R03W6GPKEL`
- Conditional loading: disabled on localhost/development environments
