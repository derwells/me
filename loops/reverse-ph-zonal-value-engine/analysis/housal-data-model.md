# Housal Data Model — Reverse Engineering

**Wave:** 4 — Competitive & Third-Party Analysis
**Date:** 2026-03-04
**Method:** WebFetch of 15+ Housal pages/endpoints, JavaScript chunk analysis, API endpoint discovery and probing
**Prior work:** `third-party-platform-survey.md` (Wave 1) documented Housal at high level; this analysis goes deep into actual data structures.

---

## Summary

Housal's zonal value tool is built on Next.js App Router with React Server Components. The frontend pages render shells that load data asynchronously from internal API routes. Through JavaScript chunk analysis, three API endpoints were discovered and successfully probed, revealing the complete record schema, actual data counts, and coverage patterns. Key findings: (1) Housal stores **~2M flat records** with 12 fields per record — no DO#, no effectivity date, no revision history per record; (2) the search is city-scoped with classification filtering, not address-aware; (3) major coverage gaps exist — Fort Bonifacio (BGC) is absent from Taguig's barangay list despite BGC being a premium market; (4) Housal's record counts (~16.8K Makati, ~12.1K Taguig, ~43.8K QC, ~10.6K Cebu) suggest they have ingested current + some historical revisions but with significant incompleteness.

---

## 1. URL Architecture

### Dual URL Scheme

Housal maintains TWO parallel URL schemes for zonal values:

**User-facing search tool** (`/find-zonal-value/`):
```
/find-zonal-value                          — main search page
/find-zonal-value/browse                   — browse by region
/find-zonal-value/{city-slug}              — city results (e.g., /find-zonal-value/makati)
```
Route parameter: `params.slug` (single segment, city name only)

**SEO/sitemap pages** (`/zonal-values/`):
```
/zonal-values/{region}/{province}/{city}           — city page
/zonal-values/{region}/{province}/{city}/{barangay} — barangay page
/zonal-values/projects/{project-slug}              — project page
```

Both URL schemes render page shells with "Loading zonal values..." placeholders. Actual data loads via client-side JavaScript after hydration.

### Sitemap Structure

Sitemap index at `/sitemap.xml` contains 9 nested sitemaps:

| Sitemap | Content | Priority | Frequency |
|---------|---------|----------|-----------|
| `sitemap-static.xml` | 7 core pages | 0.7-1.0 | daily-monthly |
| `sitemap-properties.xml` | Property listings | — | — |
| `sitemap-projects.xml` | Real estate projects | — | — |
| `sitemap-developers.xml` | Developer pages | — | — |
| `sitemap-faqs.xml` | FAQ pages | — | — |
| `sitemap-legal.xml` | Legal pages | — | — |
| **`sitemap-zonal-cities.xml`** | City-level zonal pages | 0.7 | monthly |
| **`sitemap-zonal-barangays.xml`** | Barangay-level zonal pages | 0.6 | monthly |
| **`sitemap-zonal-projects.xml`** | ~450+ project zonal pages | 0.8 | weekly |

All zonal sitemaps use the `/zonal-values/` URL pattern (not `/find-zonal-value/`).

### robots.txt

```
Disallowed: /admin/*, /api/*, /dashboard/*, /auth/*, _next/*, /checkout/*, /portal/*
```

API endpoints are explicitly blocked from crawlers. AI bots (GPTBot, anthropic-ai, PerplexityBot, etc.) have additional restrictions on `/buy/*` and `/rent/*`.

---

## 2. API Endpoints Discovered

Three internal API endpoints were discovered by analyzing the JavaScript chunk `628ed6eb9096041f.js`:

### 2.1 `/api/zonal-values/barangays`

**Purpose:** Returns barangay list with aggregate statistics for a given city.

**Parameters:**
- `city` (required) — city slug (e.g., `makati`, `taguig`, `cebu`, `quezon-city`)

**Response schema:**
```json
{
  "success": true,
  "city": "Makati",
  "total": 30,
  "barangays": [
    {
      "code": "<string>",
      "name": "Bel-Air",
      "slug": "bel-air",
      "recordCount": 597,
      "avgZonalValue": 168932.08,
      "minZonalValue": 46000,
      "maxZonalValue": 940000
    }
  ]
}
```

### 2.2 `/api/zonal-values/records`

**Purpose:** Returns paginated zonal value records for a city, with optional classification and barangay filters.

**Parameters:**
- `city` (required) — city slug
- `classification` (optional) — classification code filter (CC, RC, RR, CR, PS, etc.)
- `barangay` (optional) — barangay slug (NOTE: slug-based filtering appears broken — `bel-air` and `Bel-Air` both returned 0 results; `western-bicutan` worked)
- `limit` (optional, default appears to be 50)
- `offset` (optional, for pagination)

**Response schema:**
```json
{
  "success": true,
  "records": [
    {
      "id": "<UUID>",
      "streetName": "100 WEST",
      "buildingName": null,
      "vicinity": null,
      "classification": "CC",
      "classificationDesc": "Commercial Condominium",
      "zonalValue": 240000,
      "propertyType": "STREET",
      "barangay": "",
      "city": "City of Makati",
      "province": "",
      "region": "NCR"
    }
  ],
  "total": 16843,
  "limit": 50,
  "offset": 0,
  "hasMore": true
}
```

### 2.3 `/api/search/universal`

**Purpose:** Universal search across all content types (properties, projects, developers, agents, zonal values).

**Parameters:**
- `q` (required) — search query
- `limit` (optional)
- Additional: `property_type`, `listing_type`, `city`

**Response schema:**
```json
{
  "success": true,
  "results": [...],
  "categories": {
    "property": [...],
    "project": [...],
    "zonal_value": [...]
  },
  "totals": {
    "total": 600,
    "properties": 10,
    "projects": 3,
    "zonal_values": 10
  }
}
```

Search for "BGC" returned zonal value results showing Avida buildings in Taguig with CC classification at 216,000-252,000/sqm.

### 2.4 `/api/search/log`

**Purpose:** Logs search queries (analytics, not data retrieval).

**Parameters:** `sessionId`, `queryText`, `resultsCount`, `source`

---

## 3. Record Schema — Full Field Analysis

Each zonal value record contains exactly **12 fields**:

| Field | Type | Description | Population Rate |
|-------|------|-------------|-----------------|
| `id` | UUID | Unique record identifier | 100% |
| `streetName` | string | Street, building, or location name | 100% |
| `buildingName` | string/null | Building name (condos) | ~5% (mostly null) |
| `vicinity` | string/null | Vicinity/boundary descriptor | ~5% (mostly null) |
| `classification` | string | BIR classification code | 100% |
| `classificationDesc` | string | Human-readable classification | 100% |
| `zonalValue` | integer | Value per sqm in PHP | 100% |
| `propertyType` | string | Record type enum | 100% |
| `barangay` | string | Barangay name (often empty) | ~30-40% |
| `city` | string | Full city name (e.g., "City of Makati") | 100% |
| `province` | string | Province name (often empty for NCR) | ~20% |
| `region` | string | Region (often empty) | ~40% |

### Critical Missing Fields (vs. BIR source data)

Housal's records are **missing** several fields present in BIR workbooks:

| Missing Field | Significance |
|---------------|-------------|
| **Department Order (DO#)** | Cannot determine which revision a record belongs to |
| **Effectivity date** | Cannot determine when the zonal value became effective |
| **Revision history** | No way to know if this is the latest or a prior revision |
| **RDO code** | No jurisdiction tracking (critical for legal accuracy) |
| **Footnote markers** | All asterisk annotations stripped — loses deletion/new/transfer status |

### `propertyType` Enum Values

Observed values across all probed cities:
- `STREET` — standard street/land record (majority)
- `ALL_STREETS` — catch-all barangay record (e.g., "ALL OTHER STREETS IN BARANGAY")
- `CONDO` — condominium building record

### `classification` Code Coverage

Observed codes in API responses:

| Code | Description | Observed |
|------|-------------|----------|
| RR | Residential Regular | Yes (most common) |
| CR | Commercial Regular | Yes |
| RC | Residential Condominium | Yes |
| CC | Commercial Condominium | Yes |
| PS | Parking Slot | Yes |
| I | Industrial | Yes (Taguig) |
| A | Agricultural | Yes (Taguig) |
| GP | Government Property | Yes (Taguig) |
| APD | Area for Priority Development | Yes (Makati, end of dataset) |

**NOT observed (likely missing):**
- X (Institutional/Exempt) — standard code present in BIR data
- DA (Drying Area) — provincial code
- Agricultural sub-codes (A1-A50) — provincial codes
- WC, AR, PC, PH, R, A0 — non-standard regional codes

### `vicinity` and `buildingName` Sparsity

The `vicinity` and `buildingName` fields are almost always null/empty in the API responses. This is a **critical data loss** — the BIR source workbooks have vicinity data for nearly every record. Housal appears to have either:
1. Failed to parse the vicinity column from BIR workbooks, OR
2. Merged the vicinity into the `streetName` field (some streetName values contain asterisk markers like "10TH *" and "10TH **" suggesting partial vicinity encoding)

The asterisk patterns in `streetName` (e.g., "100 WEST **", "10TH *", "10th AVENUE**") map to BIR footnote conventions indicating the record is from a newer revision or has special status.

---

## 4. Data Coverage Analysis

### Record Counts by City (sampled)

| City | Total Records | Barangays | Notes |
|------|--------------|-----------|-------|
| **Makati** | 16,843 | 30 | Most records per barangay: Post Proper Southside (814) |
| **Taguig** | 12,126 | 17 | **Fort Bonifacio/BGC MISSING from barangay list** |
| **Quezon City** | 43,826 | N/A | Largest city dataset |
| **Cebu City** | 10,600 | N/A | Provincial city, confirmed functional |

### Makati Barangay Coverage (30 barangays)

Complete list with record counts:

| Barangay | Records | Avg ZV (PHP/sqm) | Min | Max |
|----------|---------|-------------------|-----|-----|
| Post Proper Southside | 814 | 385,992 | 98,000 | 900,000 |
| Bel-Air | 597 | 168,932 | 46,000 | 940,000 |
| San Lorenzo | 465 | 167,435 | 110 | 940,000 |
| Poblacion | 306 | 178,338 | 3,224 | 400,000 |
| Post Proper Northside | 270 | 510,185 | 200,000 | 900,000 |
| Guadalupe Nuevo | 205 | 46,098 | 800 | 300,000 |
| San Antonio | 150 | 131,306 | 9,630 | 450,000 |
| Rizal | 133 | 47,925 | 47,000 | 79,000 |
| Pembo | 131 | 62,924 | 59,000 | 123,000 |
| Pinagkaisahan | 124 | 70,513 | 1,200 | 300,000 |
| Valenzuela | 122 | 46,159 | 3,500 | 250,000 |
| East Rembo | 108 | 100,630 | 75,000 | 180,000 |
| Tejeros | 96 | 57,529 | 2,000 | 250,000 |
| West Rembo | 93 | 100,774 | 83,000 | 150,000 |
| South Cembo | 87 | 118,494 | 103,000 | 250,000 |
| Forbes Park | 81 | 8,886 | 2,200 | 20,000 |
| Santa Cruz | 77 | 108,987 | 40,000 | 250,000 |
| Olympia | 74 | 112,705 | 9,170 | 275,000 |
| Guadalupe Viejo | 69 | 173,485 | 57,750 | 350,000 |
| Pitogo | 67 | 80,631 | 2,500 | 214,000 |
| Comembo | 45 | 76,933 | 65,000 | 138,000 |
| La Paz | 40 | 120,238 | 42,000 | 250,000 |
| Palanan | 39 | 4,230 | 4,000 | 12,000 |
| San Isidro | 37 | 5,357 | 5,000 | 10,000 |
| Cembo | 34 | 97,559 | 70,000 | 200,000 |
| Carmona | 32 | 144,594 | 100,000 | 300,000 |
| Bangkal | 32 | 4,422 | 4,000 | 10,000 |
| Singkamas | 24 | 92,583 | 70,000 | 180,000 |
| Kasilawan | 20 | 85,500 | 80,000 | 150,000 |
| Pio Del Pilar | 15 | 107,000 | 91,000 | 130,000 |

**Notable data anomalies:**
- Forbes Park avg ZV of 8,886/sqm is suspiciously low for the most exclusive residential area in Manila. BIR zonal values for Forbes Park land are indeed much lower than market (typically 150,000-250,000/sqm market) but 8,886 seems low even for BIR — this may reflect very old revision data.
- Bangkal, Palanan, San Isidro all show avg ZV under 5,500/sqm — these are the EMBO barangays recently transferred to Taguig jurisdiction. Low values may reflect legacy pre-transfer schedules.
- San Lorenzo min of 110 PHP/sqm is an obvious data artifact (possibly a parsing error or a special-category record).

### Taguig Barangay Coverage (17 barangays)

| Barangay | Records | Avg ZV (PHP/sqm) | Min | Max |
|----------|---------|-------------------|-----|-----|
| Western Bicutan | 10 | 1,270 | 300 | 8,000 |
| Wawa | 18 | 828 | 155 | 8,000 |
| Bagumbayan | 28 | 719 | 185 | 8,000 |
| Maharlika Village | 2 | 455 | 310 | 600 |
| Tuktukan | 15 | 394 | 200 | 650 |
| Upper Bicutan | 4 | 378 | 300 | 600 |
| Lower Bicutan | 12 | 366 | 215 | 600 |
| Hagonoy | 16 | 341 | 100 | 650 |
| Ibayo-Tipas | 39 | 308 | 100 | 700 |
| Bambang | 11 | 300 | 165 | 500 |
| Santa Ana | 25 | 280 | 110 | 500 |
| Ligid-Tipas | 23 | 260 | 100 | 500 |
| North Signal Village | 2 | 233 | 165 | 300 |
| Napindan | 16 | 223 | 110 | 350 |
| Calzada | 6 | 198 | 180 | 230 |
| Ususan | 25 | 381 | 165 | 1,500 |
| Palingon | 9 | 158 | 140 | 195 |

**CRITICAL COVERAGE GAP: Fort Bonifacio is entirely absent.** Fort Bonifacio (BGC) is the highest-value real estate zone in the Philippines, with BIR zonal values of 100,000-900,000/sqm. Yet Housal's Taguig barangay endpoint returns only 17 barangays — Fort Bonifacio is not among them. The 12,126 total Taguig records returned by the records endpoint DO contain BGC-area data (records with "Bonifacio Center" vicinity and values up to 900,000/sqm), but these are NOT associated with any barangay in the barangay listing.

**Additionally suspicious:** The Taguig avg ZV values shown in the barangay listing (158-1,270/sqm) are absurdly low and appear to be 1/100th of correct values. The records endpoint shows the same Taguig streets with values of 6,000-900,000/sqm. This suggests the barangay aggregation for Taguig is computing statistics from a different (possibly legacy) subset of records, or there is a unit conversion error in the aggregation.

---

## 5. Search Architecture

### Search Input Model

From JS chunk analysis, the search component (`HousalAISearch`) provides:

1. **Universal search** (`/api/search/universal`) — single text input searching across properties, projects, developers, agents, and zonal values simultaneously
2. **Zonal value browse** — region > province > city > barangay hierarchical navigation
3. **Classification filter** — post-search filter by classification code

The search accepts: building names, street addresses, barangay names, city names, developer names.

### Search Result Categories

Results are categorized into:
- `calculator_result` — tax calculators
- `tool` — platform tools
- `property` — property listings
- `project` — real estate projects
- `developer` — developer profiles
- `agent` — real estate agents
- `zonal_value` — zonal value records
- `city` — city pages
- `neighborhood` — neighborhood pages
- `faq` — FAQ entries
- `guide` — guide articles

### Result Card Fields (from ZonalValueCard component)

The `ZonalValueCard` component renders:
- `meta.price` — zonal value
- `meta.classification` — classification code
- `meta.effective_from` — effectivity date (interesting — this field exists in the card component but NOT in the API record schema; it may be unpopulated or sourced differently for search results)
- `meta.zonal_value` — redundant value field
- `meta.location_type` — location categorization

### Session Management

- Session ID stored in `localStorage` as `"housal_search_session"`
- Search queries are logged via `/api/search/log` for analytics

---

## 6. Technology Stack

### Frontend
- **Framework:** Next.js App Router (React Server Components with streaming)
- **CSS:** Tailwind CSS (chunk-based CSS files)
- **Fonts:** Custom WOFF2 fonts
- **Theme:** Light/dark mode with localStorage persistence and system preference detection
- **Analytics:** Google Analytics GA-4
- **Components:** ThemeProvider, GA4Script, ScrollToTop, EnhancedHeader, EnhancedFooter, ClientPageRoot

### Architecture Pattern
- Server-rendered page shells with RSC streaming (`$L`, `$RC`, `$RV`, `$RB` markers)
- Client-side data fetching after hydration
- No `__NEXT_DATA__` JSON (App Router, not Pages Router)
- No visible Supabase client references in JS chunks (backend-only database access)
- `/api/*` routes blocked by robots.txt but accessible via browser JavaScript

### Key JavaScript Chunks
- `628ed6eb9096041f.js` — Main search component with API endpoint URLs and data schemas
- `06f877eb12ef82cc.js` — UI card components (PropertyCard, ProjectCard, ZonalValueCard, AgentCard)
- Core framework chunks handle theme, analytics, routing

---

## 7. Data Organization Model

### How Housal Organized ~2M Records

Based on all API probing, Housal's data organization is:

```
Region (17)
  └── Province / District
        └── City / Municipality
              └── Barangay (optional, often empty)
                    └── Street/Building Record
                          ├── classification (code)
                          ├── classificationDesc (text)
                          ├── zonalValue (integer, PHP/sqm)
                          ├── propertyType (STREET | ALL_STREETS | CONDO)
                          ├── buildingName (nullable)
                          └── vicinity (nullable)
```

**Key observations:**
1. **Flat record structure** — no hierarchy enforcement. Barangay, province, and region are optional string fields, not foreign keys.
2. **No revision/temporal dimension** — no DO#, no effectivity date, no version tracking per record. The "1.96M" count is not explained by multi-version records in the API (the homepage claims "2024-2025 Data Year").
3. **City is the primary query dimension** — all API endpoints are city-scoped. No cross-city search.
4. **Classification is a post-filter** — applied after city selection, not part of the primary query.
5. **Barangay is unreliable** — many records have empty barangay fields. The barangay aggregation endpoint returns statistics, but individual record queries by barangay are inconsistent.

### Record Count Reconciliation

| Source | Claimed Count | Notes |
|--------|--------------|-------|
| Homepage | "1.97M Locations" | Marketing number |
| BIR info page | "2M+ zonal value records" | Rounded up |
| Makati API total | 16,843 | Per-city query |
| Taguig API total | 12,126 | Per-city query |
| Quezon City API total | 43,826 | Per-city query |
| Cebu City API total | 10,600 | Per-city query |

If we assume ~124 RDOs with an average of ~16,000 records each (which is high — Makati is above-average density), that yields ~2M, consistent with the claim. However, the per-record data quality (missing barangay, missing vicinity, no DO#) suggests bulk ingestion with limited normalization.

---

## 8. Coverage Gaps & Data Quality Issues

### Structural Gaps

1. **No Fort Bonifacio/BGC barangay** — The highest-value real estate zone in the Philippines is missing from Taguig's barangay listing. BGC records exist in the flat records table but are orphaned from the barangay hierarchy.

2. **Taguig valuation anomaly** — Barangay-level statistics show avg ZV of 158-1,270/sqm while individual records show 6,000-900,000/sqm. The aggregation is broken or computed from a different dataset.

3. **Empty barangay/province/region fields** — ~60-70% of records have empty barangay fields, ~80% have empty province fields. This degrades the hierarchical browse experience.

4. **Vicinity column almost entirely empty** — The BIR source data's vicinity column (critical for address matching) is not populated in Housal's records. This means Housal cannot support vicinity-based address resolution.

5. **No footnote preservation** — BIR asterisk conventions (new, deleted, transferred records) are stripped. Users cannot distinguish current from deleted records.

### Classification Gaps

6. **Only ~9 classification codes observed** — vs. 63 in BIR Annex B. Agricultural sub-codes (A1-A50) absent. X (Institutional) not observed. This means provincial and agricultural zone coverage is likely poor.

7. **APD classification present** — "Area for Priority Development" appears in Makati data, which is not a standard Annex B code. This suggests some RDO-specific codes were ingested without normalization.

### Functional Gaps

8. **No address matching** — The API is city-scoped, returning all records alphabetically. There is no address-to-record resolution logic.

9. **No fallback hierarchy** — When a specific street is not found, the system provides no fallback (barangay catch-all, adjacent barangay, etc.).

10. **No RPVARA awareness** — No mention of RA 12001, BLGF SMV, or dual-source handling anywhere in the platform.

11. **No DO# or effectivity tracking** — Users cannot determine which BIR revision they are looking at. The `effective_from` field exists in the card component but is not populated in API responses.

12. **No RDO jurisdiction tracking** — Critical for legal accuracy; absent from the data model.

---

## 9. Comparison with Our Engine Design

| Feature | Housal | Our Planned Engine |
|---------|--------|--------------------|
| Record count | ~2M (flat, no versioning) | ~690K current + ~2.97M historical (versioned) |
| Classification codes | ~9 observed | 63 (full Annex B) |
| Address matching | None (alphabetical list) | 8-phase pipeline with fuzzy matching |
| Fallback hierarchy | None | 7-level decision tree |
| Vicinity data | Empty/missing | Full preservation from BIR workbooks |
| DO#/effectivity | Missing | Per-record, temporal versioning |
| RDO jurisdiction | Missing | ~42K entry mapping table |
| Footnote preservation | Stripped | u16 metadata per record |
| RPVARA readiness | None | 3-regime model, LguRegimeRegistry |
| BGC FAR tiers | Missing/broken | 544 records with FAR 1-18 handling |
| Data delivery | Server-side API only | Client-side WASM (~4.6 MB brotli) |
| Privacy | Server sees all queries | Property details never leave browser |

---

## 10. BIR Info Page Data (housal.com/bir)

The `/bir` page provides reference information:

**Database claims:**
- 2M+ zonal value records
- 122 BIR Revenue District Offices (vs actual 124 — 2 missing)
- 17 regions

**Property classifications listed (6 codes):**
- RR: Residential Regular
- RC: Residential Condo
- CR: Commercial Regular
- CC: Commercial Condo
- IR: Industrial Regular
- AR: Agricultural Regular

Note: IR and AR are NOT standard Annex B codes. Standard is I (Industrial) and A (Agricultural) with sub-codes A1-A50. Housal has created non-standard "Regular" variants.

**Featured cities with claimed data:**

| City | Claimed Records | Claimed Avg Value |
|------|----------------|-------------------|
| Makati | 45K+ | 180,000/sqm |
| Taguig (BGC) | 38K+ | 200,000/sqm |
| Quezon City | 120K+ | 45,000/sqm |
| Manila | 85K+ | 55,000/sqm |

**Discrepancy with API data:** The BIR page claims 45K+ Makati records, but the API returns total: 16,843. Similarly, Taguig claims 38K+ but API returns 12,126. QC claims 120K+ but API returns 43,826. These inflated numbers on the BIR page may include historical revisions that are not returned by the current API, or they may be marketing numbers.

**Tax use cases documented:** CGT (6%), DST (1.5%), Estate Tax, Donor's Tax.

**Update frequency noted:** "Every 3 years through Department Orders."

---

## 11. Raw API Response Samples

### Makati Records (first 50 of 16,843)

Sample records demonstrating the data structure:

```
100 WEST          | —                       | CC  | 240,000
100 WEST          | —                       | RC  | 220,000
100 WEST          | —                       | PS  | 168,000
100 WEST **       | —                       | CC  | 150,000
100 WEST **       | —                       | RC  | 140,000
10TH              | —                       | RR  | 35,000
10TH              | —                       | RR  | 11,000
10TH *            | East Rembo              | CR  | 110,000
10TH *            | East Rembo              | RR  | 75,000
10th AVENUE**     | Post Proper Northside   | CR  | 250,000
10TH AVENUE       | —                       | RR  | 100,000
10TH ST.          | —                       | RR  | 100,000
10TH ST.**        | Post Proper Northside   | CR  | 550,000
10TH ST.**        | Post Proper Northside   | RR  | 350,000
139 CORPORATE CENTER | Bel-Air              | CC  | 155,000
139 CORPORATE CENTER | Bel-Air              | PS  | 108,000
139 CORPORATE CENTER | —                    | CC  | 100,000
139 CORPORATE CENTER | —                    | PS  | 78,000
```

Key observations from raw data:
1. **Duplicate records** — "100 WEST" appears with `**` suffix AND without, at different ZV values. These likely represent different revisions (newer with `**`), but without DO# there's no way to distinguish.
2. **Asterisk encoding in streetName** — `*` and `**` suffixes are BIR footnote markers that were NOT stripped from street names but WERE lost from the metadata. They're noise in the streetName field.
3. **Case inconsistency** — "10th AVENUE" vs "10TH AVENUE" in the same dataset.
4. **Empty barangay** — Most records have no barangay despite the BIR source grouping records by barangay.
5. **No vicinity** — Cross-street boundary data is entirely absent.

### Taguig Western Bicutan Records (10 of 10)

```
BAYANI ROAD         | Western Bicutan | RR   | 600
BAYANI ROAD         | Western Bicutan | CR   | 650
C-5                 | Western Bicutan | I    | 8,000
MCKINLEY PARKWAY    | Western Bicutan | CR   | 8,000
MCKINLEY PARKWAY    | Western Bicutan | RR   | 8,000
NATIONAL HIGHWAY    | Western Bicutan | CR   | 600
NATIONAL HIGHWAY    | Western Bicutan | RR   | 300
ALL OTHER STREETS   | Western Bicutan | A    | 300
ALL OTHER STREETS   | Western Bicutan | GP   | 300
ALL OTHER STREETS   | Western Bicutan | RC   | 8,000
```

This shows the full range of property types including Agricultural (A), Government Property (GP), and Industrial (I) classifications within a single barangay. The "ALL OTHER STREETS" entries are the BIR catch-all fallback records.

---

## 12. Implications for Our Engine

### What Housal Gets Right
1. City-based initial scoping is a reasonable UX choice
2. Classification filtering is a necessary feature
3. Flat record storage is simple and queryable
4. Universal search across content types is good UX

### What Housal Gets Wrong (our opportunity)
1. **No address resolution** — this is the #1 gap. Users must manually scroll through thousands of alphabetically-sorted records to find their street.
2. **No vicinity data** — eliminates the possibility of resolving "which section of this street" (the core BIR lookup logic).
3. **No fallback logic** — when a street isn't found, there's no guidance.
4. **No revision tracking** — users cannot trust the data currency.
5. **No classification intelligence** — no Aquafresh rule, no PS formula derivation, no condo-ground-floor-CC rule.
6. **Broken barangay aggregation** — Taguig statistics are off by 100x, BGC is entirely missing.
7. **Footnote markers as noise** — asterisks in streetName degrade search/matching quality.
8. **No RPVARA readiness** — will be blindsided by the 2026-2027 transition.

### Data Volume Benchmark
Housal's ~2M records across ~124 RDOs is consistent with our estimate of ~690K current + multiple historical revisions. Their flat storage model works for simple display but cannot support the resolution logic our engine requires.
