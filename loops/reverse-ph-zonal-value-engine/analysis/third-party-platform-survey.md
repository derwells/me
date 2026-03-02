# Third-Party Platform Survey — Zonal Value Lookup Platforms

**Wave:** 1 — Source Acquisition
**Date:** 2026-03-02
**Platforms surveyed:** ZonalValueFinderPH, LandValuePH, REN.PH, Housal, RealValueMaps, ZonalValue.com
**Method:** Web search, site fetching, interface analysis, technology fingerprinting

---

## Summary

Six third-party platforms were surveyed. All source their data from the same upstream: BIR Excel workbooks published on bir.gov.ph. None offer a public API. They range from ad-supported free lookup tools (ZonalValueFinderPH) to freemium property appraisal platforms (LandValuePH) to public-infrastructure verification ledgers (REN.PH). The two largest by record count are RealValueMaps (2.7M+) and Housal (1.96M+), but their records include historical revisions, not just current values. No platform solves the core engineering problem: programmatic address-to-zonal-value resolution with classification awareness and fallback logic.

---

## Platform 1: ZonalValueFinderPH

**URL:** https://zonalvaluefinderph.com
**Tagline:** "2025 BIR Zonal Values in 3-easy-clicks"
**Operator:** Anonymous (no company or individual identified; no About page; contact form only)

### Search UX

Three search modes, all using Select2 dropdowns with AJAX-populated options:

1. **By City/Municipality** — Select city from dropdown, view all barangays + streets in that city
2. **By Barangay** — Select barangay, view streets within it
3. **By Street/Subdivision/Condominium** — Text input search (minimum 3 characters), searches across entire Philippines

Backend endpoints:
- `POST /get_dropdown_data` — populates cascading dropdowns
- `POST /chat` — handles user questions (chat widget)

Results appear in a table after 3-5 seconds processing delay, with a "Show Zonal Values" button per row that opens a popup table.

### Data Model

Results table columns (confirmed from Makati results page):

| Column | Description |
|--------|-------------|
| **Barangay** | Administrative district within the city |
| **Street** | Street name or subdivision/condo name |
| **Vicinity** | Boundary descriptor (e.g., "DON BOSCO TO EDSA") |
| **Class** | BIR classification code (RR, CR, RC, CC, PS, X, etc.) |
| **Price per SQM** | Zonal value in PHP per square meter |

This maps directly to the BIR Annex C standard format (4 columns: Street, Vicinity, Classification, ZV/SQM) plus a Barangay grouping column. No Department Order number, no effectivity date, no revision history.

### Coverage

- **~1,600+ cities/municipalities** listed on the all-cities page (organized alphabetically by province)
- **19 Revenue Regions, ~111 RDOs** listed on the revenue regions page
- Claims nationwide coverage
- No record count disclosed; site claims "30,000+ records" in prior analysis but this may be understated

### Data Source & Freshness

- Data labeled as "updated as of March 1, 2025" on homepage
- Sourced from BIR Excel workbooks (manual ingestion, not API)
- **No effectivity dates or DO numbers** displayed per record — user cannot determine which revision they are seeing
- **No indication of monitoring for BIR updates** — unclear how frequently re-ingested

### Accuracy Disclaimer

Explicit and prominent: *"The zonal values presented on this website might not be accurate and should not be relied upon for any financial or legal decisions. For accurate and up-to-date zonal values, it is strongly recommended that you consult the official website of the Bureau of Internal Revenue (BIR)."*

### Technology

- **Frontend:** jQuery + Select2 (cascading AJAX dropdowns), vanilla CSS
- **Backend:** Unknown server-side (POST endpoints suggest Python/Flask or PHP)
- **Analytics:** Google Analytics (G-5C23VSP54R)
- **Ads:** Google AdSense + gizokraijaw.net ad network script
- No framework fingerprint (not React/Next.js/Vue)

### Monetization

- **Google AdSense display ads** — primary revenue
- **Third-party ad network** (gizokraijaw.net) — additional ad revenue
- No premium tier, no paid features
- Pure ad-supported free lookup

### Classification Codes Referenced

Site's BIR_Land_Classifications page lists a legend table with codes and definitions. Agricultural subcodes A1-A50 documented. Matches RMO 31-2019 Annex B, though missing some codes (GL, GP, APD not listed on their classification page).

### Strengths

- Simplest UX of all platforms surveyed — genuinely 3 clicks
- Good coverage breadth (nationwide)
- Free, no signup required
- Mobile-responsive table design

### Weaknesses

- No effectivity date or DO# per record — legally material omission
- No fallback logic — if street not found, user gets nothing
- No classification filtering in search — must scan visually
- No historical values or revision tracking
- Anonymous operator — trust deficit
- Ad-heavy (multiple ad networks)
- Data freshness unverifiable

---

## Platform 2: LandValuePH

**URL:** https://www.landvalueph.com
**Tagline:** "Philippines #1 online property valuation tool"
**Operator:** Anonymous entity (founded 2024; no company registration or individual disclosed)
**Trust signal:** Claims "8,500+ Filipino property owners across 17+ regions"

### Search UX

Navigation-based rather than search-based: users click through city/municipality links to reach location-specific pages. No unified search bar on the main zonal value directory.

**City page structure:** e.g., `/zonal-value/quezon-city` — dynamically loads zonal data per barangay with residential and commercial rate comparisons. Data loads asynchronously ("Loading zonal data...").

**Land value calculator** (paid feature) at `/how-much-is-my-land-worth`:
- Input: Location, lot size, shape, road access, frontage, zoning classification, flood risk, utility availability, title status, neighborhood development level
- Processing: "Live BIR zonal data integration with multi-factor adjustment algorithms" applying 8-23 market adjustment factors
- Output: 6-7 page PDF report with BIR zonal value, market-adjusted valuation, CGT/transfer tax breakdowns, depreciation schedules, comparables

### Data Model

City pages show zonal values organized by barangay with these apparent fields:
- **Barangay/Location**
- **Residential zonal value (PHP/sqm)**
- **Commercial zonal value (PHP/sqm)**

This is a simplified view compared to the raw BIR data — individual street/vicinity records appear to be aggregated or summarized at barangay level for the free tier.

### Coverage

- **200+ cities** claimed
- Metro Manila, Cavite, Bulacan, Laguna, Cebu, Iloilo specifically named
- 17+ regions
- No total record count disclosed

### Data Source & Freshness

- Explicitly states use of "official BIR data"
- Blog content references "2025 Guide"
- Key insight from site content: "Zonal values are typically updated only every 3-5 years and often fall 30-50% below actual market prices" — LandValuePH's value proposition is bridging this gap with market adjustment algorithms

### Accuracy Disclaimer

Not as prominent as ZonalValueFinderPH. Site emphasizes its data comes from "official BIR data" but does not have a visible per-page disclaimer about accuracy limitations.

### Technology

- **Frontend:** Modern CSS3 with custom properties, semantic HTML, performance-optimized
- **Analytics:** Google Analytics (GA-F2923PHJMS) + Contentsquare monitoring
- **Loading:** Deferred script loading for performance optimization
- Dynamic data loading (JavaScript-rendered tables)
- Framework not definitively identified but appears lightweight/custom

### Monetization

**Freemium model:**
- **Free:** BIR zonal value lookup, estate tax calculator, CGT calculator
- **Paid:** Property appraisal reports
  - Vacant lot: PHP 299 (~$5-6 USD)
  - House & lot: PHP 799 (~$14-15 USD)
- No display advertising visible — revenue from paid reports

### Strengths

- Value-added layer on top of raw BIR data (market adjustment algorithms)
- Clean, ad-free interface
- Tax calculators integrated alongside zonal data
- Actionable output (PDF reports for property transactions)

### Weaknesses

- Navigation-based browsing is less efficient than search
- Free tier appears to show aggregated/simplified data (barangay-level, not street-level)
- Dynamic loading means pages may not render for crawlers/scrapers
- No API
- No effectivity date tracking
- Record count undisclosed — unclear how complete the coverage is
- Paid reports are a black box — no transparency on methodology beyond "8-23 adjustment factors"

---

## Platform 3: REN.PH

**URL:** https://ren.ph
**Zonal tool URL:** https://ren.ph/tools/zonal-value
**Tagline:** "Philippine Sovereign Real Estate Ledger" / "Raising the Standard in Philippine Real Estate"
**Operator:** **Godmode PH** (AI consultancy and PropTech developer)
**Founder:** **Aaron Zara** — PRC License #0025157, licensed real estate broker and software architect, CEO and "Fractional CTO"
**Focus:** Broad real estate verification platform; zonal values are one tool among many

### Search UX

**ZonalSearch component** with:
- Text search bar: search by city or barangay
- Regional browsing: clickable regional categories leading to province > city > barangay hierarchy
- No signup required, no paywall

### Data Model

The most transparent data model of all platforms surveyed. Site explicitly discloses database statistics:

| Metric | Count |
|--------|-------|
| **Provinces** | 73 |
| **Cities/Municipalities** | 1,913 |
| **Barangays** | 46,444 |
| **Zone records** | 336,792 |

Per-record fields:
- Location hierarchy (province > city > barangay)
- Zonal value per sqm
- Property classification: residential, commercial, industrial
- RDO code (jurisdiction tracking)

**Key distinction:** REN.PH explicitly tracks **RDO jurisdiction** per record, which is essential for legal accuracy. Most other platforms omit this.

### Coverage

- **73 provinces, 1,913 cities, 46,444 barangays** — this is comprehensive national coverage
- **336,792 zone records** — significantly fewer than Housal (1.96M) or RealValueMaps (2.7M), suggesting REN.PH stores only current revisions, not historical data
- Data sources verified from: **PRC, DHSUD, and BIR** (three Philippine government agencies)
- Last updated: 2024

### Data Source & Freshness

- Data sourced directly from BIR workbooks
- Cross-verified with PRC (Professional Regulation Commission) and DHSUD (Department of Human Settlements and Urban Development) data
- "97.7% direct government provenance" claimed for broker verification (unclear if this applies to zonal data)
- No automatic update monitoring disclosed

### Accuracy Disclaimer

Minimal — the platform's positioning as "public infrastructure" implies a higher standard of accuracy, but no explicit disclaimer was observed on the zonal value tool page.

### Technology

The most sophisticated tech stack of all platforms surveyed:

- **Framework:** Next.js (React, server-side rendering with streaming)
- **Backend:** Supabase (PostgreSQL)
- **Design system:** Geist (Vercel's design system)
- **Analytics:** Google Analytics GA-4
- **AI:** "Agentic AI Orchestration" referenced for broker verification
- **No advertising scripts**

### Monetization

**None visible.** The platform is positioned as free public infrastructure:
- No premium tier
- No paywalls
- No advertisements
- No signup required
- Business model unclear — possibly funded by Godmode PH consulting revenue, or positioned as a lead generation/trust-building tool for the consultancy

### Beyond Zonal Values

REN.PH is a much broader platform than a zonal value tool:
- **Broker license verification:** 25,264+ verified PRC profiles
- **License-to-Sell verification:** 8,240+ DHSUD records
- **Transfer tax calculator**
- **Legal templates:** Contracts, deeds, SPAs
- **Due diligence checklists**
- **Academy courses:** RA 9646 Essentials, real estate fundamentals
- **Broker/project directory** with location-based browsing
- **PRC exam results** tracking

### Strengths

- Most transparent data model (explicit record counts and source provenance)
- RDO jurisdiction tracking per record
- Modern tech stack (Next.js + Supabase) — cleanest architecture
- No ads, no paywall — highest trust positioning
- Broader platform context adds credibility (broker verification, legal tools)
- Named, licensed operator (Aaron Zara, PRC #0025157)

### Weaknesses

- 336K records is far fewer than Housal/RealValueMaps — may not include all street-level records (possibly barangay-level aggregation or current-revision-only)
- "Last updated: 2024" — not current with 2025 revisions
- No effectivity date or DO# per record visible
- Zonal values are a secondary feature, not the primary focus — may get less development attention
- No API despite sophisticated tech stack

---

## Platform 4: Housal

**URL:** https://www.housal.com/find-zonal-value
**Browse URL:** https://www.housal.com/find-zonal-value/browse
**Tagline:** "Find BIR Zonal Values Philippines 2025 | Official Property Valuations"
**Operator:** Housal (registered in BGC, Taguig City, Metro Manila)
**Focus:** Full property marketplace (buy/sell/rent) with zonal value tool as one feature

### Search UX

- **Text search** with autocomplete: accepts city, barangay, street, subdivision, building names
- **Browse hierarchy:** Region > Province > City > Barangay
- **Classification filters:** RC (Residential Condo), RR (Residential Regular), CC (Commercial Condo), CR (Commercial Regular), PS (Parking Slot)
- **Historical filter:** toggle between "current" and "historical" values
- **Sort options:** by year

### Data Model

| Metric | Count |
|--------|-------|
| **Total records** | 1,961,265+ (also cited as "2M+ official records") |
| **Locations** | 30,000+ |
| **Regions** | 17 |
| **Provinces** | 81 |

The ~2M record count includes **historical revisions** — confirmed by the "historical" filter toggle and per-city URLs like `?filter=historical&sort=year`. This means the same street/classification may have multiple records across different revision years.

Per-record fields (inferred):
- Region > Province > City > Barangay > Street/Building/Village
- Classification code (RC, RR, CC, CR, PS)
- Zonal value per sqm (PHP)
- Year/revision (for historical tracking)

### Coverage

- Claims nationwide across all 17 regions, 81 provinces
- 30,000+ searchable locations
- Historical data included (multiple revisions per location)

### Data Source & Freshness

- Labeled as "2024-2025 BIR valuations"
- BIR workbooks as upstream source
- Historical tracking suggests systematic ingestion across revision years

### Technology

- **Framework:** Next.js (React) — `/\_next/static/chunks/` references confirmed
- Light/dark theme with localStorage persistence
- Dynamic/client-side data loading (browse pages showed 0 records in static fetch, indicating server-rendered data)

### Monetization

- **Property marketplace:** Primary revenue from property listing subscriptions ("Post Unlimited Properties")
- **Founder's Circle membership** — premium membership program
- Zonal value tool appears to be a **free traffic acquisition tool** for the marketplace
- No ads on the zonal value pages

### Disclaimer

*"Market prices are typically 20-50% higher than BIR zonal values, especially in premium locations. Always verify with the BIR for official transactions."*

### Strengths

- Largest record count among named platforms (1.96M+)
- Historical revision tracking — unique among surveyed platforms
- Classification-specific filtering
- Modern tech stack (Next.js)
- Named company with physical address (BGC)

### Weaknesses

- Browse pages returned 0 records in static fetch — heavy client-side rendering may indicate fragile data loading
- No API
- Zonal values are a secondary feature to the property marketplace
- No DO# or effectivity date per record visible
- No fallback logic for missing streets

---

## Platform 5: RealValueMaps

**URL:** https://realvaluemaps.com
**Tagline:** "2025 BIR Zonal Values - Instant Access to 2.7M+ Properties"
**Operator:** Unknown (no company, individual, or About page found)
**Focus:** Pure zonal value lookup

### Data Model

| Metric | Count |
|--------|-------|
| **Total records** | 2,700,000+ |
| **Barangays** | 42,011 |
| **RDOs** | 121 |

The 2.7M record count is the largest claimed by any platform. Like Housal, this almost certainly includes historical revisions (121 RDOs x ~42K barangays x ~multiple streets x multiple revisions).

**Notable:** Claims 121 RDOs vs. the actual 124 RDOs — suggesting 3 RDOs may be missing from coverage.

### Search UX

Could not be fully analyzed — the site rendered primarily as a JavaScript application with minimal static HTML. Google Analytics tracking (G-R03W6GPKEL) was the only visible technical element from static fetch.

### Technology

- Heavy JavaScript application (minimal static HTML)
- Google Analytics GA-4
- Framework not determinable from static fetch

### Monetization

Unknown — no advertising, no pricing, no premium tier visible from available data.

### Strengths

- Largest record count claimed (2.7M+)
- Explicit RDO count (121) and barangay count (42,011) suggest genuine data coverage

### Weaknesses

- Anonymous operator — lowest trust among all platforms
- Site rendered poorly in static fetch — may indicate technical fragility
- No visible disclaimer
- No API
- Minimal web presence — no reviews, no social media mentions found
- 121 vs 124 RDOs suggests incomplete coverage

---

## Platform 6: ZonalValue.com (brief)

**URL:** https://zonalvalue.com
**Focus:** BIR zonal value lookup (major cities)
**Operator:** Unknown

Appeared in multiple search results but was not deeply analyzed as it is a smaller player with less coverage. Organized by district (e.g., `ncr1stdistrict.zonalvalue.com`), suggesting a geographic subdomain structure. No record count disclosed. Free lookup, no known API.

---

## Comparative Analysis

### Coverage Matrix

| Platform | Record Count | Cities | Barangays | RDOs | Historical | Classification Filter |
|----------|-------------|--------|-----------|------|------------|----------------------|
| **RealValueMaps** | 2,700,000+ | N/A | 42,011 | 121 | Likely | Unknown |
| **Housal** | 1,961,265+ | 30,000+ locations | N/A | N/A | Yes | Yes (5 codes) |
| **REN.PH** | 336,792 | 1,913 | 46,444 | N/A | No (current only) | Yes (R/C/I) |
| **ZonalValueFinderPH** | ~30,000+ (est.) | 1,600+ | N/A | 111 | No | No |
| **LandValuePH** | Undisclosed | 200+ | N/A | N/A | No | No |
| **ZonalValue.com** | Undisclosed | Major cities | N/A | N/A | Unknown | Unknown |

### Record Count Reconciliation

The variation in record counts is explained by what constitutes a "record":

- **REN.PH (336K):** Likely current-revision, street-level records only. This is closest to the actual BIR data volume (~690K estimated rows across all 124 RDOs from our workbook analysis, but many rows are duplicated across revision sheets).
- **Housal (1.96M):** Includes historical revisions. Multiple records per street across revision years.
- **RealValueMaps (2.7M):** Likely includes historical revisions plus possibly finer-grained sub-street entries.
- **Our estimate from actual workbook analysis:** ~690K total rows across all 124 RDOs for current revisions (from Wave 1 bir-workbook-provincial-samples analysis).

### Data Freshness

| Platform | Claimed freshness | Verifiable? | Effectivity date tracked? |
|----------|-------------------|-------------|---------------------------|
| ZonalValueFinderPH | "March 1, 2025" | No | No |
| LandValuePH | "2025 Guide" (blog) | No | No |
| REN.PH | "Last updated: 2024" | Partially (explicit disclosure) | No |
| Housal | "2024-2025 BIR valuations" | Partially | No (but historical toggle exists) |
| RealValueMaps | "2025 BIR Zonal Values" | No | Unknown |

**Critical gap across all platforms:** None track the legally material **Department Order number** or **effectivity date** per zonal value record. Under CTA rulings (see `analysis/cta-zonal-rulings.md`), the specific revision that was effective at the transaction date determines the applicable zonal value. Without DO#/effectivity tracking, these tools cannot reliably support actual tax computation.

### Technology Comparison

| Platform | Framework | Backend | Data Loading | API |
|----------|-----------|---------|-------------|-----|
| ZonalValueFinderPH | jQuery/Select2 | Unknown (Flask/PHP?) | AJAX POST | No |
| LandValuePH | Custom/lightweight | Unknown | JS dynamic | No |
| REN.PH | **Next.js** | **Supabase (PostgreSQL)** | SSR + streaming | No |
| Housal | **Next.js** | Unknown | CSR dynamic | No |
| RealValueMaps | Unknown JS app | Unknown | JS dynamic | No |

### Monetization Comparison

| Platform | Model | Revenue Source |
|----------|-------|----------------|
| ZonalValueFinderPH | Ad-supported | Google AdSense + third-party ads |
| LandValuePH | **Freemium** | Paid appraisal reports (PHP 299-799) |
| REN.PH | **Free public infrastructure** | None visible (parent consultancy?) |
| Housal | **Marketplace cross-sell** | Property listing subscriptions |
| RealValueMaps | Unknown | None visible |

---

## Key Findings for Engine Design

### 1. No API exists anywhere
Every platform is a closed web application. No public endpoints for programmatic zonal value lookup. This confirms the API-first approach as a genuine market gap.

### 2. Nobody solves address matching properly
All platforms require exact or near-exact location selection (dropdown or text match). None implement fuzzy address matching, vicinity segment resolution, or cross-street interpretation. None handle the fallback hierarchy (street not found -> barangay general -> LGU FMV markup).

### 3. Nobody tracks legal metadata
No platform displays Department Order numbers, effectivity dates, or revision history per record in a way that supports actual tax computation. Housal's historical filter is the closest, but it lacks DO# linking.

### 4. Classification filtering is primitive
Only Housal and REN.PH offer classification-based filtering. None handle edge cases documented in our CTA rulings analysis: mixed-use resolution, predominant use rule, reclassification timing.

### 5. Data is stale across the board
No platform monitors BIR for workbook updates in real-time. "Last updated" dates are homepage-level, not per-record. Given that BIR updates are ad hoc by RDO (not on a schedule), staleness is a structural risk for all platforms.

### 6. Privacy model is uniformly server-side
All platforms transmit the user's property search query to their servers. No platform offers client-side computation. This means every lookup creates a record of what property the user is researching — a meaningful privacy concern for tax-sensitive transactions.

### 7. REN.PH has the cleanest architecture to learn from
Supabase + Next.js with explicit government data provenance tracking. Their 336K record count for current-revision data is a useful benchmark for our WASM bundling analysis.

---

## Implications for Wave 4 (Deep Dives)

This survey identifies what needs deeper investigation in Wave 4:

1. **Housal data model** (Wave 4: housal-data-model) — Their 1.96M record structure with historical tracking needs reverse-engineering. How do they organize revisions? What are the actual per-record fields when data loads?
2. **RealValueMaps approach** (Wave 4: realvaluemaps-approach) — Their 2.7M claim and 121-RDO coverage needs validation. Is there GIS integration? How do they handle the 3 missing RDOs?
3. **Competitive gap synthesis** (Wave 4: competitive-gap-synthesis) — Combine these findings with the detailed data format analysis from Wave 2 to define the exact opportunity for an API-first engine with client-side computation.

---

## Sources

- [ZonalValueFinderPH homepage](https://zonalvaluefinderph.com/)
- [ZonalValueFinderPH all cities](https://zonalvaluefinderph.com/zonal-values-all-cities)
- [ZonalValueFinderPH revenue regions](https://zonalvaluefinderph.com/bir-revenue-regions)
- [ZonalValueFinderPH classification codes](https://zonalvaluefinderph.com/BIR_Land_Classifications)
- [ZonalValueFinderPH search tool](https://zonalvaluefinderph.com/search-data)
- [ZonalValueFinderPH Makati results](https://zonalvaluefinderph.com/zonal-values/?city=MAKATI&province=METRO%20MANILA)
- [LandValuePH homepage](https://www.landvalueph.com/)
- [LandValuePH zonal value directory](https://www.landvalueph.com/zonal-value)
- [LandValuePH land value calculator](https://www.landvalueph.com/how-much-is-my-land-worth)
- [LandValuePH Quezon City](https://www.landvalueph.com/zonal-value/quezon-city)
- [REN.PH homepage](https://ren.ph)
- [REN.PH zonal value tool](https://ren.ph/tools/zonal-value)
- [Housal zonal value search](https://www.housal.com/find-zonal-value)
- [Housal browse regions](https://www.housal.com/find-zonal-value/browse)
- [Housal BIR page](https://www.housal.com/bir)
- [RealValueMaps homepage](https://realvaluemaps.com/)
- [BIR official zonal values](https://www.bir.gov.ph/zonal-values)
