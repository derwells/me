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

---

## 13. Addendum: City-Level Department Order Organization (March 4, 2026)

**Method:** Web search engine snippet analysis of Google-indexed Housal pages. The city-level pages (`/find-zonal-value/city/{slug}`) render a DO-grouped intermediate layer that is NOT exposed by the three API endpoints discovered in the JS chunk analysis. This layer is visible in Google's cached snippet data even though the pages themselves client-render to "0 records" when fetched statically.

### 13.1 DO-Level Grouping Discovered

Housal organizes records at the city level by Department Order, showing:

**Per-DO metadata fields:**
- DO number (e.g., "DO 005-24", "DO 054-2023", "DO 26-89")
- Year (extracted from DO number or separately stored)
- Status: "Current" vs "Historical"
- Record count per DO
- Average zonal value per DO
- Min/max range per DO

**This is a significant finding** — the earlier API analysis concluded "no DO#, no effectivity date, no revision history per record." However, the city browse pages DO show DO-level organization as an intermediate grouping layer. This suggests either:
1. A separate API endpoint exists for DO-level aggregation (not yet discovered), OR
2. The DO metadata is injected server-side during page generation but not exposed in the records API, OR
3. The DO grouping is computed from some field in the database not returned in the records API response (e.g., a `department_order` column exists but is not included in the records endpoint response schema).

**The record-level API still returns no DO# per record** — but the city-level browse UI groups records by DO and shows DO-level statistics.

### 13.2 DO Data Samples from Search Engine Snippets

**City of Taguig:**
- DO 005-24 (Current, 2024) — Avg ₱168,558, 4,243 records, Range ₱1,132–₱2,160,000
- (Historical DOs not captured in snippet)

**City of Cebu (9 DOs total: 3 current, 6 historical):**

| DO | Status | Year | Avg (₱/sqm) | Records | Range |
|----|--------|------|-------------|---------|-------|
| DO 054-2023 | Current | 2023 | 69,734 | 1,091 | 168–249,000 |
| DO 86-2023 | Current | 2023 | 41,727 | 2,093 | 580–130,000 |
| DO 16-2020 | Current | 2020 | 21,880 | 1,338 | 400–105,000 |
| DO 064-18 | Historical | 2018 | 50,626 | 769 | 123–190,000 |
| DO 36-07 | Historical | 2007 | 11,912 | 550 | 2,875–60,000 |
| DO 46-07 | Historical | 2007 | 11,434 | 117 | 3,800–39,000 |
| DO 18-97 | Historical | 1997 | 6,534 | 94 | 2,350–18,500 |
| DO 20-93 | Historical | 1993 | 3,666 | 296 | 500–22,500 |
| DO 26-89 | Historical | 1989 | 1,314 | 780 | (range not captured) |

**Key observations:**
- Cebu City's total across all DOs: 7,128 records — less than the 10,600 returned by the API, suggesting some records may not be assigned to a DO
- Multiple DOs can be "Current" simultaneously (DO 054-2023 + DO 86-2023 + DO 16-2020 for Cebu) — these likely correspond to different RDOs within the same city (Cebu has RDO 81 North and RDO 82 South)
- Historical data goes back to 1989 (DO 26-89), confirming deep historical coverage
- DO numbering format is inconsistent: "DO 054-2023" vs "DO 064-18" vs "DO 36-07" vs "DO 18-97" — reflects actual BIR naming conventions

**Payao, Zamboanga Sibugay (2 Historical DOs):**
- DO 58-2019 (2019) — Avg ₱156, 466 records, Range ₱100–₱250
- DO 28-97 (1997) — Avg ₱109, 35 records, Range ₱0–₱200

**Cagayan de Oro: 1 Current + 7 Historical DOs** (details not captured)

**City of Mandaluyong:** DO 40-03 referenced in URL parameter (`?do=DO+40-03`)

### 13.3 Filter and Sort Parameters

The city-level pages support URL query parameters:

| Parameter | Values | Description |
|-----------|--------|-------------|
| `filter` | `all`, `current`, `historical` | Filters DOs by status |
| `sort` | `year`, `value`, `records` | Sorts DO listing |
| `do` | e.g., `DO+40-03` | Selects specific DO |

This confirms the "current vs historical" filter is applied at the DO level, not at the individual record level. The system categorizes DOs as either current (active) or historical (superseded).

### 13.4 Search Engine Snippet Data — Per-Record Fields

Google search snippets for specific street pages (`/find-zonal-value/{street}`) reveal per-record display format:

**Makati (67 zonal value entries, BIR RDO 47):**
- Makati Avenue: CR 2022, ₱500,000, DO 35-2021
- P. De Roxas - Ayala Ave (Salcedo Subd): CR 2022, ₱500,000
- Jupiter - Neptune (Bel Air 2 Side): CR 2022, ₱500,000
- Gil Puyat - Jupiter: CR 2022, ₱500,000
- Ayala Avenue: CR 2021, ₱940,000, DO 37-2021
- Ayala Avenue: CR 2016, ₱550,000, DO 62-2016
- Makati Avenue: CR 2017, ₱500,000, DO 22-2017

**Quezon City (500 entries, BIR RDO 38):**
- EDSA: CR, ₱350,000
- DO references: DO 033-2024 and DO 007-2024 observed
- Major streets: Quezon Ave., G. Araneta Ave., Katipunan Ave., Commonwealth Ave., Aurora Blvd., Timog Ave., Tomas Morato Ave.

**Taguig (5th-11th Ave, 18 entries, BIR RDO 44):**
- CR values under DO 005-24: ₱900,000, ₱750,000, ₱600,000

**Per-record display format from snippets:**
```
[Classification Code] [Year] ₱[Value] · [Classification Description] · [DO Reference]
```
Example: "CR 2022 ₱500,000 · Commercial Regular · DO 35-2021"

**This reveals that DO# IS stored per record and displayed in the frontend, even though the `/api/zonal-values/records` endpoint does not return it.** The per-record DO# must be either:
1. Fetched from a different (undiscovered) API endpoint, or
2. Injected during server-side rendering from a field not exposed in the client API

### 13.5 Revised Record Schema Assessment

Based on the addendum findings, the actual Housal database likely has MORE fields than the 12 discovered via API probing:

| Field | In API Response | In Frontend Display | Assessment |
|-------|----------------|--------------------|----|
| id | Yes | N/A | Confirmed |
| streetName | Yes | Yes | Confirmed |
| buildingName | Yes (mostly null) | Partially | Confirmed |
| vicinity | Yes (mostly null) | Not visible | Confirmed |
| classification | Yes | Yes | Confirmed |
| classificationDesc | Yes | Yes | Confirmed |
| zonalValue | Yes | Yes | Confirmed |
| propertyType | Yes | Not visible | Confirmed |
| barangay | Yes (often empty) | Contextual | Confirmed |
| city | Yes | Yes | Confirmed |
| province | Yes (often empty) | Contextual | Confirmed |
| region | Yes (often empty) | Contextual | Confirmed |
| **departmentOrder** | **NO** | **YES** (e.g., "DO 35-2021") | **New: stored but not in records API** |
| **year** | **NO** | **YES** (e.g., "2022") | **New: stored but not in records API** |
| **doStatus** | **NO** | **YES** ("Current"/"Historical") | **New: stored but not in records API** |
| **rdo** | **NO** | **YES** (e.g., "RDO 47") | **New: shown on street pages** |

This raises the total estimated fields per record from 12 to at least 15-16. The records API is serving a reduced projection — likely for performance (excluding string fields like DO reference reduces payload size for pagination).

### 13.6 Additional Coverage Data from Search Engine Snippets

**BIR Info Page (/bir) additional statistics:**
- "122 BIR RDO Offices" (vs actual 124 — 2 missing)
- 6 classification codes listed: RR, RC, CR, CC, IR, AR

**City record counts from /bir page (marketing numbers, NOT API-verified):**

| City | Claimed Records | API-verified Records | Inflation Factor |
|------|----------------|---------------------|-----------------|
| Quezon City | 120K+ | 43,826 | 2.74x |
| Manila | 85K+ | (not probed) | — |
| Cebu City | 65K+ | 10,600 | 6.13x |
| Davao City | 55K+ | (not probed) | — |
| Makati | 45K+ | 16,843 | 2.67x |
| Pasig | 42K+ | (not probed) | — |
| Taguig (BGC) | 38K+ | 12,126 | 3.13x |
| Mandaluyong | 25K+ | (not probed) | — |

The inflation factor ranges from 2.67x to 6.13x. The /bir page numbers may count DO-grouped aggregations differently, or may include records from a wider query scope than the API returns.

**Regional coverage claimed:**
- NCR/Metro Manila: 17 Cities
- Central Luzon: 7 Provinces
- CALABARZON: 5 Provinces
- Central Visayas: 4 Provinces
- Western Visayas: 6 Provinces
- Davao Region: 5 Provinces (62,155+ records)
- Northern Mindanao: 5 Provinces
- Ilocos Region: 4 Provinces
- Plus 9 additional regions

**Province-level examples:**
- Pampanga: 19,265+ records across 19 cities/municipalities
- Laguna: 33,331+ records across 25 cities/municipalities
- CALABARZON total: 125,714+ records across 5 provinces

### 13.7 Dual URL Scheme — Additional Patterns

The SEO URL scheme has a deeper nesting than initially documented:

```
/zonal-values/{region}/{province}/{city}/{barangay}/{street}
```

Example discovered:
```
/zonal-values/mimaropa-region/palawan/el-nido/sibaltan/along-barangay-road
```

This 5-level hierarchy (region > province > city > barangay > street) is the deepest URL nesting observed. It suggests Housal generates SEO pages at the individual street level within barangays. The page for the above URL showed "0 Records" when fetched (dynamic rendering), but the URL structure confirms the intended data model granularity.

**Additional URL patterns confirmed:**
- `/find-zonal-value/province/{province-slug}` — province-level with city/municipality listing
- `/find-zonal-value/barangay/{barangay-slug}` — direct barangay access
- `/find-zonal-value?q={query}` — search query parameter

### 13.8 Historical Data Depth

Oldest DO references discovered across all cities:
- DO 26-89 (1989) — Cebu City
- DO 20-93 (1993) — Cebu City
- DO 28-97 (1997) — Payao, Zamboanga Sibugay
- DO 18-97 (1997) — Cebu City
- DO 56-90 (1990) — referenced for Cagayan de Oro (not confirmed in snippets)

This confirms Housal's historical coverage extends back to at least 1989, representing 35+ years of zonal value revision history. The 9 DOs for Cebu City alone span 1989-2023, providing a rich longitudinal dataset.

### 13.9 Effectivity Date Status

**No effectivity date observed anywhere in Housal's frontend or search snippets.** The `ZonalValueCard` component (from JS chunk analysis) has an `effective_from` field in its schema, but:
- It is not populated in API responses
- It does not appear in Google search snippets
- The DO year serves as a rough proxy but is NOT the same as the formal effectivity date

The BIR source workbooks contain effectivity dates in the NOTICE sheet. Housal appears to have extracted the DO year but NOT the specific effectivity date. This is a legally material gap — the effectivity date determines which zonal value schedule applies to a transaction on a specific date.

### 13.10 PS (Parking Slot) Classification Details

From legal analysis (Respicio & Co.), PS is BIR shorthand for "Parking Slot (Condominium)" or "Condominium Parking Space." Key distinction: **PS is valued per slot, not per square meter** — although in practice, BIR workbooks often list PS with a per-sqm figure that represents the slot value divided by an assumed area. PS can have its own Condominium Certificate of Title (CCT), making it separately conveyable. This aligns with our engine's PS pricing rule analysis (60-70% of RC/CC parent).

### 13.11 Competitor Benchmark Update

| Platform | Records | Barangays | RDOs | Historical | DO Tracking | Effectivity Date |
|----------|---------|-----------|------|------------|-------------|-----------------|
| **Housal** | ~2M | 30,000+ locations | 122 (claimed) | Yes (DO-grouped) | Yes (display only) | No |
| **RealValueMaps** | 2.7M+ | 42,011 | 121 | Likely | Unknown | Unknown |
| **REN.PH** | 336K | 46,444 | N/A | No | No | No |
| **ZonalValueFinderPH** | ~30K+ | N/A | 111 | No | No | No |
| **Our Engine** | ~690K current + 2.97M hist. | ~42K | 124 | Yes (versioned) | Yes (per-record) | Yes (per-record) |

Housal's DO-level grouping is more sophisticated than initially assessed — they DO track Department Orders, but the tracking is at the grouping/display level, not at the individual record level in their API. Our engine's per-record DO tracking with effectivity dates remains a significant differentiator.

---

## 14. Business Context & Strategic Assessment

### 14.1 Company Profile

**Legal entity:** Housal Inc., BGC, Taguig City, Metro Manila
**Founders:** Raneza Mathur and Yash Mathur (co-founders per Crunchbase/Tracxn); **Yogesh Mathur** (Founder/CEO, public face — "Hands-On CTO Driving Product and Technology")
**Founded:** 2015 (incorporation per Tracxn) / 2016 (per GetLatka); launched April 26, 2018 at Shangri-La at the Fort
**Team:** ~16-20 employees (PitchBook: 16, GetLatka: 20)
**Operations:** Philippines (Makati, Taguig), Indonesia (Jakarta), United States (San Francisco) per Kalibrr

**Revenue (self-reported via GetLatka, unverified):**

| Year | Revenue |
|------|---------|
| 2016 | $0 |
| 2021 | $1.2M |
| 2023 | $1.1M (decline) |
| 2024 | $1.8M |

**Funding:** Conflicting information — GetLatka claims $1M raised; Tracxn lists "not raised any funding yet." Brook Capital (Malta) lists Housal in portfolio with a "coming soon" detail page that has been static for years. Assessment: likely a small seed/angel investment, not a formal round.

**Developer clients:** Vista Land, Century Properties, Alveo Land (per Tracxn); Ayala Land, SMDC, Megaworld (per homepage 2026). These are standard listing partnerships, not exclusive data arrangements.

### 14.2 Zonal Value Tool as Traffic Acquisition

The zonal value tool is a **free SEO traffic acquisition feature**, not a core revenue product:
- Free, no signup required
- Sits at high-intent SEO URLs (`/find-zonal-value`, `/bir`, `/zonal-values`)
- Uses **programmatic SEO** — thousands of auto-generated city/barangay/street pages
- Pages rank for "zonal value [city name]" queries — core search pattern for property transactions
- Cross-promotes property marketplace with CTAs to browse listings and subscribe

**Revenue comes from:** property listing subscriptions ("Post Unlimited Properties"), Founder's Circle membership, CRM/marketing tools for brokers and developers.

**Broader free tool suite (all traffic acquisition):** mortgage calculator, closing costs estimator, ROI calculator, affordability calculator, disaster risk checker, document templates.

### 14.3 Data Ingestion Process

**No public documentation exists.** No engineering blog, no technical content, no data methodology transparency. Blog content (last published September 2022) is generic real estate advice only.

**Inferred process:** Manual/semi-automated ingestion of BIR Excel workbooks from bir.gov.ph. No official BIR data partnership — same upstream as all competitors.

**Job listing signals:** Previous Kalibrr postings included "Data I/O Manager" (suggests dedicated data pipeline role), "Backend Developer Smartflows" (workflow automation), "Data Science" and "Data Analyst" roles — indicating some investment in data infrastructure, though likely not at the level of a purpose-built parsing pipeline for BIR's heterogeneous workbook formats.

### 14.4 Current Status & RPVARA Readiness

- **No blog posts since September 2022**
- **No press coverage since 2018 launch**
- **Zero RPVARA (RA 12001) mentions anywhere on the platform** — will be blindsided by the 2026-2027 transition from BIR zonal values to BLGF SMVs
- **CEO's LinkedIn** (Yogesh Mathur) now lists position as "Confidential - AI Startup" rather than Housal CEO — possible reduced involvement or pivot
- **Tracxn ranking:** #1 Real Estate IT company in Philippines (out of 15 startups)

### 14.5 Strategic Assessment for Our Engine

**Housal's strengths relative to other competitors:**
1. Largest named dataset (1.96M records with historical depth back to 1989)
2. DO-level organization (more sophisticated than most competitors)
3. Named company with physical presence and developer clients
4. Modern tech stack (Next.js App Router)
5. Traffic: zonal value tool likely generates significant organic search traffic

**Housal's structural weaknesses (our opportunity):**
1. Zonal values are a traffic tool, not a product — limited investment incentive
2. No API (despite clear demand)
3. No address matching or fallback logic
4. Vicinity data missing — cannot resolve "which section of this street"
5. Record count inflation (2.67x-6.13x marketing vs API reality)
6. BGC entirely missing from Taguig barangay hierarchy
7. Classification coverage limited to ~9 of 63 Annex B codes
8. No RPVARA readiness — existential risk from BIR→BLGF transition
9. No data provenance or accuracy guarantees
10. No privacy model — all queries server-side

**Competitive window:** Housal appears to be in maintenance mode for the zonal value tool (no updates since 2022, CEO possibly disengaged). The RPVARA transition creates a 12-18 month window where first-mover advantage on dual-source architecture is significant. An API-first engine with client-side computation, address matching, and RPVARA readiness would occupy a completely different value tier.

---

## Sources

- [Housal zonal value search](https://www.housal.com/find-zonal-value)
- [Housal browse regions](https://www.housal.com/find-zonal-value/browse)
- [Housal BIR page](https://www.housal.com/bir)
- [Housal API: /api/zonal-values/barangays?city=makati](https://www.housal.com/api/zonal-values/barangays?city=makati)
- [Housal API: /api/zonal-values/records?city=makati&limit=50](https://www.housal.com/api/zonal-values/records?city=makati&limit=50)
- [Housal API: /api/search/universal?q=BGC&limit=10](https://www.housal.com/api/search/universal?q=BGC&limit=10)
- [Housal sitemap.xml](https://www.housal.com/sitemap.xml)
- [Housal robots.txt](https://www.housal.com/robots.txt)
- [Housal JS chunk 628ed6eb9096041f.js — API endpoint discovery](https://www.housal.com/_next/static/chunks/628ed6eb9096041f.js)
- [GetLatka — Housal revenue profile](https://getlatka.com/companies/housalcom)
- [Brook Capital — Housal portfolio](https://www.brookcapital.co.uk/portfolio/housal)
- [PRNewswire — Housal launch (April 2018)](https://www.prnewswire.com/news-releases/the-launch-of-housal-inc-an-online-real-estate-platform-coincides-with-world-intellectual-property-day-introducing-the-revolutionary-real-estate-tool-at-shangri-la-fort-300635085.html)
- [Tracxn — Housal company profile](https://tracxn.com/d/companies/housal/)
- [Crunchbase — Housal](https://www.crunchbase.com/organization/housal)
- [Kalibrr — Housal job listings](https://www.kalibrr.id/c/housal-inc/jobs)
- [Housal city page — Cebu City (Google snippet)](https://www.housal.com/find-zonal-value/city/city-of-cebu)
- [Housal city page — Taguig (Google snippet)](https://www.housal.com/find-zonal-value/city/city-of-taguig)
- [Respicio & Co. — PS classification analysis](https://www.lawyer-philippines.com/articles/meaning-of-ps-classification-in-zonal-valuation-philippines)
