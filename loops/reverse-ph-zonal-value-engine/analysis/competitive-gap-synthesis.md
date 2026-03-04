# Competitive Gap Synthesis — State of the Art & Opportunity Map

**Wave:** 4 — Competitive & Third-Party Analysis
**Date:** 2026-03-04
**Method:** Synthesis of Wave 1 survey (7 platforms) + Wave 4 deep dives (Housal, RealValueMaps) + Wave 2-3 technical findings
**Dependencies:** `third-party-platform-survey.md`, `housal-data-model.md`, `realvaluemaps-approach.md`, all Wave 2-3 analyses

---

## Summary

Seven platforms were analyzed at increasing depth across Waves 1 and 4. The Philippine zonal value lookup market is structurally immature: every platform is a closed web application with no API, no address matching beyond dropdown selection, no legal metadata tracking, and zero RPVARA readiness. The two largest players (Housal at ~2M records, RealValueMaps at 2.7M claimed) have fundamental data quality issues — Housal's vicinity column is ~95% null and its barangay field ~60-70% empty; RealValueMaps uses the wrong classification taxonomy entirely and has a non-functional API backend. The market opportunity is not incremental improvement — it is a category-defining first: an API-first engine with client-side computation, street-level address matching, legal metadata tracking, and dual-source RPVARA architecture. No existing platform addresses even one of these capabilities fully.

---

## 1. Market Landscape Overview

### Platform Tiers

**Tier 1 — Data Scale Players (non-functional for real use):**
- **Housal** (1.96M records, ~$1.8M marketplace revenue, ~20 staff) — real data but critically incomplete; zonal tool is a free SEO acquisition feature for their property marketplace
- **RealValueMaps** (2.7M claimed, $0 revenue, anonymous) — operationally vacant; wrong taxonomy, non-functional API, fabricated metrics

**Tier 2 — Functional Lookup Tools:**
- **ZonalValueFinderPH** (~30K+ records, ad-supported, anonymous) — simplest UX, genuinely useful for basic lookups, but no metadata or intelligence
- **REN.PH** (336K records, free public infrastructure, named operator) — cleanest architecture (Next.js + Supabase), most transparent data model, but secondary feature for a broader platform

**Tier 3 — Value-Added / Niche:**
- **LandValuePH** (undisclosed records, freemium PHP 299-799 reports) — market adjustment algorithms as differentiator, but opaque methodology
- **ZonalValue.com** (undisclosed, district-based subdomains) — minimal presence
- **FileDocsPhil** (resells BIR Excel for ₱560) — validates market pain; existence proves BIR's UX is so poor people pay to avoid it

### The Absence of an API-First Player

Every platform is a closed web application. None offers:
- A documented public API
- Programmatic access for downstream tax computation engines
- Webhook/notification for data updates
- Bulk export in structured formats

Housal has 3 internal API endpoints (discovered via JS chunk analysis) but they are undocumented, use reduced projections (DO#, year, doStatus omitted from response), and are not intended for external consumption. RealValueMaps designed 18 API endpoints but zero are functional — the API subdomain serves an Open WebUI AI chat instance.

**This is the single largest structural gap.** BIR zonal values are a foundational input to every Philippine real estate tax computation (CGT, DST, CWT, estate tax, donor's tax, RPT). Yet there is no programmatic way to look up a zonal value. Every downstream system (tax calculators, legal compliance tools, property platforms) must either manually look up values or build their own ingestion pipeline. An API-first engine with correct data, legal metadata, and RPVARA support would be category-defining infrastructure.

---

## 2. Capability Gap Matrix

### 2.1 Data Completeness

| Capability | ZVFPH | LandValue | REN.PH | Housal | RealValue | **Our Engine** |
|-----------|-------|-----------|--------|--------|-----------|---------------|
| All 63 BIR classification codes | Partial | Unknown | 3 groups | 9 codes | **Wrong taxonomy** | All 63 + normalization |
| Agricultural subcodes (A1-A50) | Listed | Unknown | No | No | No | Full 50 subcodes |
| Non-standard code mapping | No | No | No | No | No | 6 codes mapped (WC→CR, etc.) |
| Footnote preservation | No | No | No | Noise in data | N/A | Stripped + metadata preserved |
| Condo-specific records | Yes | Unknown | Unknown | Yes | Unknown | 6 NCR + 2 provincial patterns |
| Parking slot records | Unclear | Unknown | Unknown | Yes (PS code) | No | 4 PS models + RDO-specific formulas |
| Historical revisions | No | No | No | Yes (DO-grouped) | Claimed | Full per-revision tracking |

**Key finding from Wave 4 deep dives:**
- Housal stores DO# and doStatus in its database but does NOT return them via the records API — a deliberate reduced projection for performance. This means even the most complete platform hides legally material metadata from users.
- RealValueMaps uses LGU SMV tier codes (R1/R2/R3, C1/C2/C3) instead of BIR Annex B codes — a **fundamental taxonomy error** that makes their data structurally incompatible with actual BIR workbooks. This strongly suggests the 2.7M record count is either fabricated or parsed from a non-BIR source.

### 2.2 Resolution Intelligence

| Capability | ZVFPH | LandValue | REN.PH | Housal | RealValue | **Our Engine** |
|-----------|-------|-----------|--------|--------|-----------|---------------|
| Street-level address matching | No | No | No | No | No | 8-phase pipeline, 5-tier cascade |
| Vicinity/cross-street parsing | No | No | No | No | No | Dual-mode (NCR cross-street + provincial road-proximity) |
| Fuzzy matching | No | No | No | No | No | Jaro-Winkler at 0.90 threshold |
| Alias resolution | No | No | No | No | No | 211+ BIR annotations + Wikipedia renames |
| Barangay catch-all fallback | No | No | No | No | No | "ALL OTHER STREETS" (185 entries) |
| Adjacent barangay fallback | No | No | No | No | No | Level 4: DOF DO Rule 2 |
| Institutional → Commercial | No | No | No | No | No | Level 5: X → nearest CR |
| Confidence scoring | No | No | No | No | No | 0.0-1.0 scale, 5 UI tiers |
| NULL return (CTA mandate) | N/A | N/A | N/A | N/A | N/A | Level 6: explicit NULL per Emiliano/Gamboa |

**Every platform's resolution logic is identical:** user selects city → barangay → browses a table of all records. No platform narrows results by street address, handles ambiguous input, or implements any fallback when a street isn't found. The user is the matching engine.

This is where our 8-phase pipeline (normalize → detect mode → resolve barangay → match street → parse vicinity → resolve classification → apply fallback → score confidence) creates the widest competitive moat. It transforms a manual table-scanning exercise into a sub-10ms programmatic lookup.

### 2.3 Legal Metadata

| Capability | ZVFPH | LandValue | REN.PH | Housal | RealValue | **Our Engine** |
|-----------|-------|-----------|--------|--------|-----------|---------------|
| Department Order # per record | No | No | No | In DB, not in API | Planned, not built | Per-record, per-revision |
| Effectivity date per record | No | No | No | No | Planned, not built | Per-revision (3 format parsers) |
| RDO jurisdiction per record | No | No | Yes | In DB, not in API | Planned | Per-record with temporal versioning |
| Transaction-date-aware lookup | No | No | No | No | No | "What ZV applied on [date]?" |
| Revision history per location | No | No | No | Historical filter | Claimed | Full DO chain per street |
| Schedule vintage warnings | No | No | No | No | No | Stale schedule flagging (38% outdated) |

**This is the most legally consequential gap.** Under CTA rulings (Emiliano EB 1103, Gamboa 9720), the specific revision effective at the transaction date determines the applicable zonal value. A property sold on March 15, 2024 in a municipality where DO 45-21 was replaced by DO 12-24 effective April 1, 2024 must use the old DO. No platform supports this query. They show "current" values with no way to determine which revision the user is seeing.

### 2.4 Privacy & Computation Model

| Capability | ZVFPH | LandValue | REN.PH | Housal | RealValue | **Our Engine** |
|-----------|-------|-----------|--------|--------|-----------|---------------|
| Client-side computation | No | No | No | No | No (planned) | WASM engine, data local |
| Server-side dependency | Full | Full | Full | Full | Full | Optional (lazy loading) |
| Property details transmitted | Yes | Yes | Yes | Yes | Yes | Never leave browser |
| Offline capability | No | No | No | No | No | Full (after initial load) |

**Every platform transmits the user's property lookup to its servers.** For tax-sensitive transactions (estate planning, capital gains, corporate restructuring), this creates a privacy concern — the platform knows what property the user is researching and when. Our WASM-first architecture (4.6 MB brotli bundle = engine + full current dataset) eliminates this entirely. Property details never leave the browser.

### 2.5 RPVARA Transition Readiness

| Capability | ZVFPH | LandValue | REN.PH | Housal | RealValue | **Our Engine** |
|-----------|-------|-----------|--------|--------|-----------|---------------|
| Awareness of RA 12001 | No | No | No | No | No | Three-regime model formalized |
| BLGF SMV data source | No | No | No | No | No | Pluggable SourceParser trait |
| BIR ZV ↔ SMV taxonomy mapping | No | No | No | No | No | LandUseCategory common denominator |
| Per-LGU regime detection | No | No | No | No | No | LguRegimeRegistry (~1,715 entries) |
| Dual-source lookup | No | No | No | No | No | Regime-agnostic matching + regime-aware tax base |
| Graceful degradation | N/A | N/A | N/A | N/A | N/A | 7-scenario cascade |

**Zero platforms mention RPVARA, RA 12001, or the BIR-to-BLGF transition.** This is the most significant medium-term opportunity. By July 2026, some LGUs will begin transitioning from BIR zonal values to BLGF Schedule of Market Values. The transition will be staggered (historical compliance ~37% predicts most LGUs will miss deadlines), creating a multi-year period where different jurisdictions use different data sources with incompatible classification taxonomies. Our three-regime model (pre-transition BIR ZV, transition-year SMV with 6% RPT cap, post-transition steady-state) is architecturally unique in this market.

---

## 3. Data Quality Assessment

### 3.1 Record Count Reality

| Platform | Claimed Records | Verified Records | Verification Method | Reality Assessment |
|----------|----------------|-----------------|--------------------|--------------------|
| RealValueMaps | 2,700,000+ | **0** | API probing (non-functional) | **Unverifiable — API serves AI chat, not data** |
| Housal | 1,961,265+ | ~123K (4 cities probed) | API endpoint probing | **Inflated 2.67-6.13x** vs actual API counts |
| REN.PH | 336,792 | Not probed | Self-reported, transparent | **Plausible** — aligns with current-only estimate |
| ZonalValueFinderPH | ~30,000+ (estimated) | Not probed | Page analysis | **Unknown** |
| LandValuePH | Undisclosed | Not probed | N/A | **Unknown** |

**Our estimate from direct BIR workbook parsing:** ~690K current-revision records (range 550K-850K), ~2.97M including all historical revisions (4.3x multiplier). REN.PH's 336K is approximately half our estimate, suggesting either barangay-level aggregation or incomplete RDO coverage. Housal's ~2M aligns with historical inclusion but has severe quality issues (95% null vicinities).

### 3.2 Critical Quality Gaps by Platform

**Housal (most complete but most flawed):**
- Vicinity column ~95% null — the core BIR field for address resolution is missing from almost all records
- Barangay ~60-70% empty — basic geographic hierarchy incomplete
- Only 9 of 63 classification codes observed — 86% of Annex B taxonomy absent
- Asterisk footnote markers left as noise in streetName field (not stripped)
- Fort Bonifacio (BGC) entirely absent from Taguig barangay hierarchy — the highest-value zone in the Philippines is orphaned
- Taguig aggregation shows 100x discrepancy (stats: 158-1,270/sqm vs actual records: 6,000-900,000/sqm)
- Record count inflation: BIR homepage claims 45K+ Makati (API returns 16,843), 120K+ QC (API returns 43,826)

**RealValueMaps (ambitious but vacant):**
- Wrong classification taxonomy (LGU SMV tier codes, not BIR Annex B) — structurally incompatible
- API backend replaced by Open WebUI AI chat instance — zero functional endpoints
- Fabricated social proof (10,247 reviews, 99.8% accuracy — zero external reviews exist)
- Template placeholder in code (`github.com/yourusername/realvaluemaps-frontend`)
- Hardcoded statistics sum to 1.1M (41% of claimed 2.7M) — 1.6M records unaccounted for
- Domain less than 11 months old with zero external traction

**ZonalValueFinderPH (functional but thin):**
- No effectivity date or DO# — legally material omission
- No classification filtering in search
- Anonymous operator
- Ad-heavy experience

**REN.PH (cleanest but secondary):**
- "Last updated: 2024" — not current with 2025 revisions
- Zonal values are secondary feature to broker verification platform
- 336K records may be barangay-level aggregation, not full street-level
- No effectivity date or DO# visible per record

---

## 4. What the Market Gets Right (Validated Patterns)

Despite the structural immaturity, several design patterns across platforms have been validated and should be adopted:

### 4.1 Adopted Design Patterns

| Pattern | Source | How Our Engine Uses It |
|---------|--------|----------------------|
| **PSGC codes as canonical location keys** | RealValueMaps | Barangay indexing + RDO jurisdiction mapping uses PSGC for unambiguous location identification |
| **Viewport-based boundary loading** | RealValueMaps | Optional map UI layer loads GeoJSON by viewport for 42K+ barangay polygons |
| **Reverse geocoding as input method** | RealValueMaps | Coordinate → barangay → text pipeline as alternative to address input |
| **Effectivity date tracking** | RealValueMaps (planned) | Per-revision DO# and effectivity date — we implement what they designed but couldn't build |
| **Historical revision grouping by DO** | Housal | City-level DO grouping with per-DO metadata (record count, status, year range) |
| **RDO jurisdiction tracking** | REN.PH | Per-record RDO with temporal versioning for boundary changes (RAO 1-2024, etc.) |
| **Classification filtering** | Housal | Per-query classification selection with RDO-aware available codes index |
| **Multilingual UX** | RealValueMaps | English + Filipino + Cebuano as future UX consideration |
| **Free tier with API monetization** | RealValueMaps (pricing) | Validates commercial model: free lookups, paid API access for downstream integrations |
| **Current/historical toggle** | Housal | User-selectable temporal scope (default: current revision, optional: historical chain) |

### 4.2 Rejected Patterns

| Pattern | Source | Why We Reject It |
|---------|--------|-----------------|
| **Barangay-level aggregation** | LandValuePH | Loses street-level granularity — within a single barangay, ZVs can range 5-50x |
| **Map-only interface** | RealValueMaps | Map doesn't solve BIR's text-based matching problem; complement, not replacement |
| **Server-side-only computation** | All platforms | Privacy concern; our WASM engine keeps property details local |
| **Ad-supported free model** | ZonalValueFinderPH | Degrades trust for tax-sensitive professional use |
| **Hiding DO#/effectivity from API** | Housal | Legally material metadata must be accessible — reduced projection is a design mistake |
| **LGU SMV taxonomy for BIR data** | RealValueMaps | Structurally incompatible — tier codes (R1/R2/R3) ≠ functional use codes (RR/CR/RC/CC) |

---

## 5. Competitive Moat Analysis

### 5.1 Moat Depth by Capability

| Capability | Difficulty to Replicate | Time to Build | Our Advantage Duration |
|-----------|------------------------|---------------|----------------------|
| **8-phase address matching pipeline** | Very High | 6-12 months | 2-3 years (requires Wave 2-3 level data analysis) |
| **7-level fallback decision tree** | High | 3-6 months | 2+ years (legal research + CTA case analysis) |
| **63-code classification resolution** | Medium | 2-4 months | 1-2 years (requires workbook parsing + code mapping) |
| **RPVARA three-regime model** | Very High | 6-12 months | 3-5 years (first-mover + regulatory uncertainty) |
| **WASM client-side engine** | Medium | 2-3 months | 1 year (architectural choice, not deep domain knowledge) |
| **Per-revision DO# + effectivity tracking** | Medium | 1-2 months | 1 year (data pipeline, not algorithm) |
| **124-RDO workbook parser** | High | 4-8 months | 2+ years (6 column patterns, 6 merge categories, footnote handling) |

**Deepest moats:** Address matching and RPVARA dual-source — both require months of domain-specific analysis that cannot be shortcut. The Wave 2-3 data (28,109 vicinity patterns, 52,327 merge cells, 76,577 classified rows, 9 CTA rulings) represents an irreplaceable knowledge base.

### 5.2 First-Mover Windows

**RPVARA Window (12-18 months):** Zero competitors are building for the BIR-to-BLGF transition. The first engine with dual-source lookup and per-LGU regime detection will capture professional users (tax practitioners, law firms, Big-4 advisory) who need transition-period guidance. Window opens when first BLGF SMVs are approved (likely H2 2026) and closes when competitors catch up (~2028).

**API-First Window (6-12 months):** The absence of any public zonal value API means every downstream system that needs ZV data today must build its own pipeline. An API with correct data, legal metadata, and sub-second response times would attract integration partners immediately. Window is shorter because API wrapping is technically simpler than deep matching logic.

**Privacy Window (ongoing):** Client-side WASM computation is a permanent architectural advantage, not a temporary window. Competitors would need to rebuild from scratch to match this — their server-side architectures cannot be incrementally migrated to client-side.

---

## 6. Strategic Positioning

### 6.1 What Everyone Gets Wrong

1. **Treating zonal value lookup as a table browsing problem.** Every platform displays a paginated table of records and asks the user to find their property. The actual problem is address-to-value resolution — a matching algorithm, not a table filter.

2. **Ignoring the legal dimension.** Zonal values are legal instruments with specific effective dates, revision chains, and jurisdictional scope. Displaying a value without its DO#, effectivity date, and RDO jurisdiction is like displaying a statute without its section number — technically present but professionally useless.

3. **Building for today's regulatory regime only.** RPVARA (RA 12001) fundamentally restructures property valuation in the Philippines. Every platform assumes BIR zonal values are the permanent single source. Our engine's dual-source architecture anticipates the 3-5 year transition.

4. **Assuming address matching is simple.** BIR workbooks contain 28,109 vicinity records across 31 sampled workbooks, with 13,080 unique values spanning two fundamentally different addressing models (NCR cross-street boundaries vs. provincial road-proximity tiers), 211 street name aliases, 331 three-segment separator ambiguities, and special cases like BGC's FAR-based pricing, Pasig's semicolon-qualified barangays, and Manila's zone-based numbered barangays. No competitor has even attempted to parse this complexity.

5. **Neglecting data quality.** Housal — the most complete platform — has ~95% null vicinities and ~60-70% empty barangays. RealValueMaps uses the wrong classification taxonomy entirely. The bar for "correct data" is extraordinarily low. Direct BIR workbook parsing with footnote handling, merge cell resolution, and cross-revision normalization is a genuine differentiator.

### 6.2 Where the Opportunity Lies

**For an API-first engine, the opportunity is threefold:**

1. **Professional infrastructure** — Tax practitioners, law firms, Big-4 advisory, notaries, and BIR-accredited tax agents need programmatic, legally defensible zonal value lookups with metadata. No platform serves them. A correct API with DO#, effectivity dates, confidence scoring, and RPVARA awareness becomes essential professional infrastructure.

2. **Platform integration** — Every property platform (Lamudi, PropertyGuru, Carousell Property, 99.co, local developers' sites) and every tax compliance tool needs zonal values as an input. Today they either hardcode values, link to BIR's Excel files, or build fragile custom pipelines. An API replaces all of this.

3. **Privacy-sensitive use cases** — Estate planning, corporate restructuring, and government transaction due diligence involve sensitive property lookups. Client-side WASM computation is the only architecture that guarantees property details never leave the user's device. This is not a feature — it's a trust architecture.

### 6.3 Positioning Statement

> The Zonal Value Lookup Engine is the first programmatic, address-aware, legally complete, RPVARA-ready zonal value resolution system for the Philippines. It replaces table browsing with sub-10ms address matching, adds legal metadata (DO#, effectivity dates, confidence scoring) that no competitor tracks, prepares for the BIR-to-BLGF transition that no competitor acknowledges, and keeps property details private through client-side WASM computation that no competitor offers.

---

## 7. Threat Assessment Summary

| Platform | Threat Level | Rationale | Timeline to Compete |
|----------|-------------|-----------|-------------------|
| **Housal** | LOW | Real company with real data, but zonal tool is maintenance-mode SEO feature; CEO possibly disengaged; no RPVARA awareness; 12 competitive gaps; could awaken if market heats up | 12-18 months if prioritized |
| **RealValueMaps** | NONE | Operationally vacant, wrong taxonomy, non-functional API, fabricated metrics, anonymous operator, <1 year old | N/A |
| **REN.PH** | LOW-MEDIUM | Clean architecture, named operator (Aaron Zara), transparent data model, free public positioning; but zonal values are secondary to broker verification platform; limited to 336K records | 6-12 months if prioritized |
| **ZonalValueFinderPH** | NEGLIGIBLE | jQuery/ad-supported, anonymous, no technical sophistication, no funding signals | Not competitive |
| **LandValuePH** | LOW | Interesting value-add model (market adjustment), but opaque methodology, anonymous, small scale | Not competitive on core ZV |
| **ZonalValue.com** | NEGLIGIBLE | Minimal presence, district-based subdomains, no scale | Not competitive |
| **FileDocsPhil** | NEGLIGIBLE | Reselling BIR Excel files for ₱560 — validates pain, not a competitor | Not competitive |
| **BIR RPIS** | UNKNOWN | Government's own Real Property Information System (under procurement, target July 2026); if it launches with a functional API, it changes the landscape; but PH government IT projects have a poor track record | 2-4 years (if ever) |

**Net assessment:** No current platform is within 12 months of matching our planned capabilities. The deepest moats (address matching, fallback logic, RPVARA) require domain knowledge that took Waves 1-3 to develop. The most credible future threat is BIR's own RPIS system, but government IT procurement timelines and the RPVARA transition to BLGF make its scope and timeline uncertain.

---

## 8. Implications for Wave 5 Architecture

This synthesis directly informs Wave 5 architecture decisions:

1. **API-first design is confirmed as the highest-leverage architecture.** Every competitor is a closed web app. The API is the product; the frontend is a reference implementation.

2. **WASM bundle at 4.6 MB brotli is viable and unique.** No competitor offers client-side computation. The full current dataset (~690K records) fits in a mobile-friendly WASM bundle (data-size-estimation analysis).

3. **Address matching pipeline is the core differentiator.** Design the Rust engine around the 8-phase pipeline — this is what transforms "browse a table" into "resolve my address."

4. **Legal metadata is non-negotiable.** Every record must carry DO#, effectivity date, RDO jurisdiction, and confidence score. Housal deliberately hides DO# from their API response — we expose it as a first-class field.

5. **RPVARA dual-source must be architecturally native, not bolted on.** The SourceParser trait, LguRegimeRegistry, and regime-agnostic matching layer from rpvara-dual-source-resolution must be core engine types, not optional modules.

6. **Parser robustness for 124 RDOs is infrastructure.** 6 column patterns, 6 merge categories, 5,418+ footnote-annotated cells, 3 effectivity date formats, 25 sheet naming anomalies — the data pipeline must handle all of these. This is not a one-time ingestion; it's an ongoing pipeline as BIR publishes updates.

7. **Monetization validates as freemium API.** RealValueMaps priced API access at PHP 2,999/mo (Professional) and PHP 9,999/mo (Enterprise). Even with their non-functional platform, this pricing anchors market expectations. Our engine targets professional users (tax practitioners, law firms, property platforms) willing to pay for correct, metadata-rich, programmatic access.

---

## Appendix A: Full Platform Comparison Table

| Dimension | ZVFPH | LandValue | REN.PH | Housal | RealValue | ZonalValue | FileDocs | **Our Engine** |
|-----------|-------|-----------|--------|--------|-----------|------------|----------|---------------|
| **Records** | ~30K+ | Unknown | 336K | ~2M | 2.7M (unverified) | Unknown | N/A | ~690K current + ~2.97M historical |
| **API** | No | No | No | Internal only | Designed, non-functional | No | No | **Public, documented** |
| **Address matching** | No | No | No | No | No | No | N/A | **8-phase pipeline** |
| **Fallback logic** | No | No | No | No | No | No | N/A | **7-level decision tree** |
| **Classification codes** | Partial | Unknown | 3 groups | 9 codes | Wrong taxonomy | Unknown | N/A | **All 63 + 6 non-standard** |
| **DO# tracking** | No | No | No | In DB only | Planned | No | N/A | **Per-record** |
| **Effectivity date** | No | No | No | No | Planned | No | N/A | **Per-revision** |
| **Confidence score** | No | No | No | No | No | No | N/A | **0.0-1.0 scale** |
| **RPVARA ready** | No | No | No | No | No | No | N/A | **3-regime model** |
| **Client-side compute** | No | No | No | No | No | No | N/A | **WASM (4.6 MB brotli)** |
| **Privacy** | Server | Server | Server | Server | Server | Server | N/A | **Property details never leave browser** |
| **Map interface** | No | No | No | No | Yes (broken) | No | N/A | **Optional complement** |
| **Historical data** | No | No | No | Yes | Claimed | Unknown | N/A | **Full revision chain** |
| **Condo handling** | Basic | Unknown | Unknown | Basic | None | Unknown | N/A | **6 patterns + PS rules** |
| **Monetization** | Ads | PHP 299-799 | Free | Marketplace | PHP 0-9,999/mo | Unknown | ₱560/file | **Freemium API** |
| **Framework** | jQuery | Custom | Next.js | Next.js | React+Vite | Unknown | Unknown | **Rust + WASM + TypeScript** |
| **Operator** | Anon | Anon | Godmode PH | Housal Inc. | Anon | Anon | Unknown | — |
| **Threat level** | None | Low | Low-Med | Low | None | None | None | — |

---

## Sources

All source data comes from prior loop analyses:
- `analysis/third-party-platform-survey.md` — Wave 1 survey of 7 platforms
- `analysis/housal-data-model.md` — Wave 4 deep dive (API probing, JS chunk analysis, coverage verification)
- `analysis/realvaluemaps-approach.md` — Wave 4 deep dive (WHOIS, bundle decompilation, API probing, JSON-LD extraction)
- `analysis/data-size-estimation.md` — Wave 2 data sizing (confirms 690K current records, 4.6 MB WASM bundle)
- `analysis/address-matching-algorithms.md` — Wave 3 pipeline design (8-phase, dual-mode)
- `analysis/fallback-hierarchy-implementation.md` — Wave 3 fallback design (7-level tree)
- `analysis/classification-resolution-logic.md` — Wave 3 classification design (7 paths, 63 codes)
- `analysis/rpvara-dual-source-resolution.md` — Wave 3 RPVARA design (3 regimes, 7 degradation scenarios)
