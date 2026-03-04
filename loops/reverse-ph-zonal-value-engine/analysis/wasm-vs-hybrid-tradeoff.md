# WASM vs. Hybrid Architecture Tradeoff — Decision Analysis

**Wave:** 5 — App Architecture Design
**Date:** 2026-03-04
**Aspect:** `wasm-vs-hybrid-tradeoff`
**Depends on:** Wave 2 (data-size-estimation), Wave 3 (all resolution logic), Wave 4 (competitive-gap-synthesis), Wave 5 (rust-engine-design)

---

## Summary

**Decision: Full client-side WASM is the primary architecture, with tiered loading as the data delivery strategy and a lightweight API fallback for historical/RPVARA-overflow scenarios.**

The ~4.6 MB brotli bundle (engine + current-revision data) is well within the range of production WASM deployments (DuckDB WASM: ~3.2 MB compressed; Photoshop Web: 80+ MB multi-module). Philippine median mobile download (30-35 Mbps) delivers this in ~1.3 seconds. The data cost is negligible (₱0.05, or 0.007% of NCR daily minimum wage). Budget Android devices (4-6 GB RAM, Helio G-series) can handle the ~15-20 MB decompressed runtime memory easily. iOS Safari's 256 MB WASM memory ceiling is not a constraint.

The architecture uses **three tiers**: (1) engine WASM + NCR data (~585 KB brotli) for instant first render, (2) full current dataset (~4.4 MB brotli) streamed in background, (3) historical data + RPVARA overflow via optional API. A Web Worker isolates the WASM engine for privacy — no browser extension content script can access query data.

---

## 1. Architecture Options Evaluated

### Option A: Full Client-Side WASM (All Data Embedded)
Ship the entire ~690K current-revision dataset in the WASM bundle. All computation happens in-browser. No server API for lookups.

### Option B: Hybrid (WASM Logic + API Data)
Ship only the matching engine in WASM (~200 KB). Data fetched per-query or per-RDO from a server API. Computation still in WASM, but data comes from the network.

### Option C: Tiered Client-Side (Recommended)
Ship engine + regional data chunks progressively. NCR first (highest demand), then Revenue Region chunks in background. Full dataset eventually resident in-browser. Historical data and RPVARA overflow served via optional API.

### Option D: Server-Side Only
Traditional API. All computation on server. Simplest architecture but sacrifices privacy, offline capability, and creates ongoing infrastructure cost.

---

## 2. Evaluation Framework

### 2.1 Bundle Size Feasibility

| Component | Raw | Brotli | Source |
|-----------|-----|--------|--------|
| WASM engine (Rust matching logic) | ~500 KB | ~200 KB | Wave 5 rust-engine-design |
| Full current data (690K records) | ~14.7 MB | ~4.4 MB | Wave 2 data-size-estimation |
| NCR-only data (24 RDOs, 40K records) | ~1.1 MB | ~385 KB | Wave 2 data-size-estimation |
| Jurisdiction map (~42K entries) | ~800 KB | ~400 KB | Wave 3 rdo-jurisdiction-mapping |
| **Full bundle (Option A)** | **~16 MB** | **~5.0 MB** | Combined |
| **NCR-first bundle (Option C tier 1)** | **~2.4 MB** | **~585 KB** | Engine + NCR + jurisdiction |

**Comparison to production WASM deployments:**

| Application | Compressed Transfer | Widely Deployed? |
|-------------|-------------------|-----------------|
| SQLite WASM | ~600 KB–1.2 MB | Yes (massive adoption) |
| DuckDB WASM | ~3.2 MB | Yes (Observable, MotherDuck) |
| **Our engine (full)** | **~5.0 MB** | — |
| Figma | ~3-5 MB (estimated) | Yes (millions of users) |
| Photoshop Web | 80+ MB (multi-module) | Yes (Adobe production) |
| AutoCAD Web | 15+ MB (lazy-loaded chunks) | Yes (Autodesk production) |

**Verdict: 5.0 MB brotli is well within production norms.** DuckDB WASM at 3.2 MB is widely deployed without complaints. Our bundle is 56% larger but includes a complete dataset — DuckDB ships no data.

### 2.2 Network Performance (Philippine Context)

| Metric | Value | Source |
|--------|-------|--------|
| Median mobile download (4G LTE) | 30-35 Mbps | Ookla/Opensignal 2025 |
| P25 mobile download (congested/rural) | ~10 Mbps | Estimated from DICT/Opensignal |
| Worst-case mobile (weak rural signal) | ~3-5 Mbps | BARMM/Eastern Visayas data |
| Median fixed broadband | ~94-105 Mbps | Ookla 2025 |
| 5G (when available) | 130-280 Mbps | Opensignal Q1 2025 |

**Download times for full bundle (5.0 MB brotli):**

| Connection | Speed | Download Time | Acceptable? |
|------------|-------|---------------|-------------|
| Fixed broadband | 100 Mbps | **0.4 seconds** | Excellent |
| 5G | 130 Mbps | **0.3 seconds** | Excellent |
| 4G median | 30 Mbps | **1.3 seconds** | Good |
| 4G congested | 10 Mbps | **4.0 seconds** | Marginal |
| Rural weak signal | 3 Mbps | **13.3 seconds** | Poor |

**Download times for NCR-first tier (585 KB brotli):**

| Connection | Speed | Download Time | Acceptable? |
|------------|-------|---------------|-------------|
| 4G median | 30 Mbps | **0.16 seconds** | Excellent |
| 4G congested | 10 Mbps | **0.47 seconds** | Good |
| Rural weak signal | 3 Mbps | **1.6 seconds** | Good |

**Data cost impact:**
- 5 MB at Philippine prepaid rates (₱10/GB): **₱0.05** — functionally zero
- As fraction of NCR minimum wage (₱695/day): **0.007%** — negligible
- As fraction of 1 GB daily prepaid pack: **0.5%** — negligible

**Key insight: the network concern is NOT data cost — it is latency for rural/congested users.** The tiered loading strategy (Option C) mitigates this by delivering a functional NCR lookup in <0.5 seconds on any connection, while streaming the full dataset in background.

### 2.3 Device Capability (Philippine Market)

**Dominant device tiers:**

| Tier | Price Range | RAM | Chipset | Market Share |
|------|-------------|-----|---------|-------------|
| Budget | <₱5,000 | 4-6 GB | Unisoc T, Helio G85 | ~30% |
| Mid-range | ₱5K-10K | 6-8 GB | Helio G99, Dimensity 6300 | ~40% |
| Upper-mid | ₱10K-15K | 8-12 GB | Dimensity 7025, Snapdragon 6 | ~20% |
| Flagship/iPhone | >₱15K | 8-16 GB | A-series, Snapdragon 8 | ~10% |

**WASM runtime memory requirements:**

| Component | Memory | Notes |
|-----------|--------|-------|
| Decompressed data | ~15-20 MB | 690K × 20B records + string table + indexes |
| WASM engine runtime | ~1-2 MB | Code + stack + working memory |
| Alias dictionary | ~500 KB | 211+ aliases + Wikipedia renames |
| Street index | ~2-3 MB | Per-barangay tokenized entries |
| **Total runtime** | **~20-25 MB** | Well within budget |

**Assessment against device tiers:**

| Device Tier | Available RAM (after OS) | 25 MB WASM? | Verdict |
|-------------|--------------------------|-------------|---------|
| Budget (4 GB) | ~1.5-2 GB free | 1.25% of free RAM | No issue |
| Mid-range (6 GB) | ~2.5-3 GB free | 0.8% of free RAM | No issue |
| iPhone (4-8 GB) | ~1.5-4 GB free | <2% of free RAM | No issue |

**iOS Safari memory ceiling:** 256 MB for WASM linear memory. Our 25 MB runtime is **10% of this limit** — no concern.

**WASM compilation time (estimated):**

| Platform | Compilation Rate | Time for ~500 KB engine | Notes |
|----------|-----------------|------------------------|-------|
| Desktop Chrome | 30-60 MB/s | ~10-15 ms | Negligible |
| Mobile Chrome | ~8 MB/s | ~60 ms | Negligible |
| Mobile Safari | ~8 MB/s | ~60 ms | Negligible |

The engine WASM is only ~500 KB — compilation is trivially fast. The data is NOT compiled (loaded as an ArrayBuffer and parsed by the engine), so data size does not affect WASM compilation time.

**V8 code caching:** Chrome automatically caches compiled WASM for modules >128 KB. On repeat visits, compilation time is effectively **zero** — cached native code is deserialized directly.

### 2.4 Privacy Model

| Dimension | Full Client-Side (A/C) | Hybrid (B) | Server-Side (D) |
|-----------|----------------------|------------|-----------------|
| Address query visible to server? | **No** | Yes (per-RDO fetch reveals city) | Yes (full query) |
| Classification intent visible? | **No** | No (resolved client-side) | Yes |
| Query frequency trackable? | **No** | Yes (API logs) | Yes |
| Offline capability | **Full** (after cache) | Partial (engine only) | None |
| Data at rest on client | Encrypted in browser cache | None (volatile) | None |

**Privacy is the foundational competitive differentiator.** Every existing platform (Housal, RealValueMaps, ZonalValueFinderPH, REN.PH, LandValuePH) is server-side — the server sees every property lookup. For users computing tax obligations (CGT at 6%, estate tax at 6%, donor's tax at 6%), revealing the property and classification to a server is a privacy leak with potential financial consequences.

**Web Worker isolation for privacy hardening:**

Running the WASM engine in a dedicated Web Worker provides an additional privacy layer:

1. **Extension content scripts cannot access Worker globals** — WASM memory is isolated from the page context
2. **Main thread communicates only via `postMessage`** — serialized query/result, no shared memory
3. **No third-party script on the page can read WASM linear memory** — even if analytics or ad scripts are added later

```
Architecture:
  Main Thread (React UI)
    ↕ postMessage (query parameters / lookup result)
  Web Worker (isolated context)
    ↕ WASM FFI (typed values, no exported memory)
  WASM Engine (zv-engine, linear memory private)
```

**Spectre/Meltdown:** Not a relevant threat for this use case. Side-channel attacks require a co-located attacker process. We control the page — no third-party code runs in the Worker.

### 2.5 Offline Capability

| Scenario | Full Client-Side (A/C) | Hybrid (B) | Server-Side (D) |
|----------|----------------------|------------|-----------------|
| First visit (no cache) | Requires download | Requires download | Requires network |
| Repeat visit (cached) | **Works offline** | Engine only (no data) | Fails |
| Airplane mode | **Full functionality** | No lookups | Fails |
| Intermittent connection | **Unaffected** | Degraded (fetch failures) | Degraded |

**Offline matters for Philippine tax practitioners.** BIR Revenue District Offices are not always in areas with reliable connectivity. Tax accountants who serve provincial clients may need to look up zonal values during client meetings or at BIR offices without Wi-Fi. The PWA/offline pattern is a genuine differentiator.

### 2.6 Infrastructure Cost

| Architecture | Hosting | Database | API Infra | CDN | Monthly Cost (est.) |
|-------------|---------|----------|-----------|-----|-------------------|
| Full client (A/C) | Static files | None | None | ~$20 | **~$20** |
| Hybrid (B) | Static + API | PostgreSQL | Node/Rust API | ~$20 | ~$100-200 |
| Server-side (D) | API server | PostgreSQL | Node/Rust API | ~$20 | ~$100-300 |

Full client-side eliminates ongoing infrastructure cost. The entire deployment is static files on a CDN (Cloudflare Pages, Vercel, Netlify). No database, no API server, no scaling concerns. Data updates are bundle rebuilds pushed to CDN.

### 2.7 Data Freshness & Updates

| Architecture | Update Mechanism | Latency | User Action |
|-------------|-----------------|---------|-------------|
| Full client (A/C) | Rebuild data bundle, push to CDN | Service Worker detects update on next visit | Automatic (SW updates cache) |
| Hybrid (B) | Update database, API serves fresh data | Immediate | None |
| Server-side (D) | Update database | Immediate | None |

BIR publishes zonal value revisions infrequently (quarterly to annually per RDO). The typical update cycle:
1. BIR publishes a new DOF Department Order with revised schedule
2. The workbook for the affected RDO is updated on bir.gov.ph
3. Our ingestion pipeline re-parses the workbook
4. A new data bundle is built and deployed to CDN
5. Service Worker detects the new version on next user visit
6. User sees "Update available" prompt or auto-updates in background

**This latency (hours to days) is acceptable** given that BIR updates are pre-announced and practitioners expect a lead time before new values are effective.

---

## 3. The Recommended Architecture: Option C (Tiered Client-Side)

### 3.1 Loading Strategy

```
Phase 1: Instant Render (< 200ms after page load)
├── Fetch engine.wasm (~200 KB brotli)
│   └── WebAssembly.instantiateStreaming() — compile while downloading
├── Fetch jurisdiction.bin (~400 KB brotli)
│   └── RDO → municipality → barangay tree for location dropdowns
└── Show UI immediately: city/barangay selectors functional

Phase 2: NCR Data (< 500ms on 4G)
├── Fetch ncr-data.bin (~385 KB brotli)
│   └── 24 NCR RDOs, 40K records
├── Pass ArrayBuffer to Web Worker → WASM engine parses
└── NCR lookups now functional (covers ~80% of tax transactions)

Phase 3: Full Dataset (< 3s on 4G, background)
├── Fetch remaining 19 Revenue Region chunks (~230 KB each, ~3.7 MB total)
│   └── Prioritize user's detected region, then geographically outward
├── Each chunk parsed into WASM memory as it arrives
└── Full 690K-record dataset resident in-browser

Phase 4: Caching (Service Worker)
├── All assets cached in Cache Storage API
├── engine.wasm + data chunks: Cache-Control: max-age=31536000, immutable
├── Versioned by content hash: engine.[hash].wasm, ncr-data.[hash].bin
└── Subsequent visits: zero network fetches, instant startup
```

### 3.2 Revenue Region Chunking Strategy

Data is partitioned into 19 Revenue Region chunks plus NCR (which is pre-loaded):

| Chunk | Revenue Region | RDOs | Est. Records | Est. Brotli |
|-------|---------------|------|-------------|-------------|
| 0 | NCR (pre-loaded) | 24 | 40,000 | 385 KB |
| 1 | RR1 (Pangasinan, La Union, etc.) | 8 | ~52,000 | ~340 KB |
| 2 | RR2 (Cagayan Valley) | 5 | ~32,500 | ~210 KB |
| 3 | RR3 (Central Luzon) | 8 | ~52,000 | ~340 KB |
| 4 | RR4A (CALABARZON) | 8 | ~52,000 | ~340 KB |
| 5 | RR4B (MIMAROPA) | 4 | ~26,000 | ~170 KB |
| 6 | RR5 (Bicol) | 5 | ~32,500 | ~210 KB |
| 7 | RR6 (Western Visayas) | 6 | ~39,000 | ~255 KB |
| 8 | RR7A (Cebu) | 4 | ~26,000 | ~170 KB |
| 9 | RR7B (Eastern Visayas) | 4 | ~26,000 | ~170 KB |
| 10 | RR8A (Northern Mindanao) | 4 | ~26,000 | ~170 KB |
| 11 | RR8B (Northeastern Mindanao) | 4 | ~26,000 | ~170 KB |
| 12 | RR9 (Zamboanga) | 4 | ~26,000 | ~170 KB |
| 13 | RR10 (Northern Luzon) | 5 | ~32,500 | ~210 KB |
| 14 | RR11 (Davao) | 4 | ~26,000 | ~170 KB |
| 15 | RR12 (SOCCSKSARGEN) | 4 | ~26,000 | ~170 KB |
| 16 | RR13 (Caraga) | 4 | ~26,000 | ~170 KB |
| 17 | RR19 (BARMM) | 4 | ~26,000 | ~170 KB |
| 18 | Metadata (string table, aliases) | — | — | ~500 KB |
| **Total** | | **124** | **~690,000** | **~4.8 MB** |

**Loading priority algorithm:**
1. Always load chunk 0 (NCR) first — 80%+ of tax transactions
2. Detect user's location (IP geolocation or explicit selection) → load that Revenue Region next
3. Load adjacent Revenue Regions
4. Load remaining chunks in background (low-priority fetch)

### 3.3 Data Separation: Engine vs. Data

The WASM engine and data are **separate artifacts**, not a single monolithic binary:

```
Artifacts:
├── zv-engine.[hash].wasm      (~200 KB brotli)   ← Rust matching engine
├── zv-meta.[hash].bin         (~500 KB brotli)    ← String table, aliases, jurisdiction
├── zv-ncr.[hash].bin          (~385 KB brotli)    ← NCR data chunk
├── zv-rr01.[hash].bin         (~340 KB brotli)    ← Revenue Region 1 chunk
├── zv-rr02.[hash].bin         (~210 KB brotli)    ← Revenue Region 2 chunk
│   ... (17 more regional chunks)
└── zv-historical.[hash].bin   (~18 MB brotli)     ← Server-side only (optional API)
```

**Why separate:**
1. **Independent versioning** — When BIR updates one RDO's zonal values, only that Revenue Region chunk changes. The engine WASM and all other chunks remain cached.
2. **Selective loading** — Budget users can use NCR-only mode (585 KB total download) without loading provincial data.
3. **Cache efficiency** — V8 code caches the compiled WASM independently from data. Engine updates (rare) don't invalidate data cache.
4. **RPVARA transition** — When BLGF SMV data becomes available, it's a new chunk type (`zv-smv-[lgu].[hash].bin`) without changing the engine or existing BIR data chunks.

### 3.4 RPVARA Transition: Data Size Impact

During the RPVARA transition period (2026-2028+), the dataset may grow:

| Scenario | Additional Records | Additional Brotli | Total Client-Side |
|----------|-------------------|-------------------|------------------|
| No LGUs transitioned (current) | 0 | 0 | 4.8 MB |
| 10% LGUs transitioned | ~69K | ~480 KB | 5.3 MB |
| 50% LGUs transitioned | ~345K | ~2.4 MB | 7.2 MB |
| 100% dual-source (worst case) | ~690K | ~4.4 MB | 9.2 MB |
| Post-transition (BIR data retired) | 0 | 0 | ~4.8 MB |

**Tiered loading handles this gracefully:**
- At 50% transition: 7.2 MB total, but NCR-first still loads in <500ms. Full dataset in ~5s on 4G.
- At 100% dual-source (theoretical worst case): 9.2 MB exceeds the 5 MB mobile target but fits within the 10 MB desktop comfort zone. This scenario is unlikely to occur simultaneously — RPVARA compliance is rolling by LGU.
- **Post-transition:** Dataset returns to ~690K records as BIR zonal values are phased out. Bundle size returns to ~4.8 MB.

**Architectural note:** BLGF SMV data is delivered as separate chunks (`zv-smv-[lgu].bin`), loaded only when a user queries a jurisdiction that has transitioned. This avoids pre-loading RPVARA data for LGUs still on BIR ZV (the vast majority through 2027).

### 3.5 Historical Data: API-Only

Historical zonal values (~2.97M records, ~18 MB brotli) are **not included in the client-side bundle**. They are served via an optional read-only API:

```
GET /api/v1/historical?rdo=47&barangay=Bel-Air&do=DO-35-21
→ Returns historical records for that location under that Department Order

GET /api/v1/history?rdo=47&barangay=Bel-Air
→ Returns all historical ZV records for that location across all DOs
```

**Rationale:**
- Historical lookups are rare (<5% of queries) — most users need the current zonal value for an active transaction
- 18 MB brotli is too large for mobile WASM budget
- Historical data is less privacy-sensitive (past values are public record from published DOs)
- The API handles a "What was the zonal value on [date]?" query by resolving the effective DO for that date — this query pattern benefits from server-side indexing

**The API is optional.** The core product (current zonal value lookup) works entirely client-side. The historical API is an enhancement for tax practitioners who need date-specific values for back-filing, estate tax computation, or CTA dispute preparation.

---

## 4. Browser Compatibility & WASM Support

### 4.1 Philippine Browser Market Share

| Browser | Mobile Share | Desktop Share | WASM Support |
|---------|-------------|---------------|-------------|
| Chrome | **90.1%** | **82.2%** | Full (streaming compile, code cache) |
| Safari | 7.9% | 2.9% | Full (iOS 15+, lazy compilation) |
| Samsung Internet | 0.7% | — | Full (Chromium-based) |
| Edge | — | 10.0% | Full (Chromium-based) |
| Firefox | — | 1.6% | Full (streaming compile, Ion) |
| Brave | 0.4% | 0.8% | Full (Chromium-based) |

**WASM support is effectively universal** in the Philippines. Chrome + Chromium-based browsers = **91.2% of mobile** and **93.0% of desktop**. The remaining ~8% is Safari (full WASM support since iOS 15, released September 2021).

No user will encounter a browser that doesn't support WASM.

### 4.2 Platform-Specific Considerations

**Chrome (90%+ of PH users):**
- Streaming compilation via `instantiateStreaming()` — compiles while downloading
- Automatic code caching for modules >128 KB — second visit loads cached native code
- Liftoff (baseline) → TurboFan (optimizing) tiered compilation
- **No size limits for async compilation** (deprecated 8 MB sync limit never applied)

**Safari (8% of PH users — iPhone owners):**
- Lazy compilation strategy — functions compiled on first call
- 256 MB maximum WASM linear memory (our 25 MB runtime is 10% of this)
- `SharedArrayBuffer` requires COOP+COEP headers (needed only if using WASM threads)
- **Known issue:** Memory not released on page reload in some iOS versions — mitigated by our modest memory footprint

**Samsung Internet / Edge / Brave:**
- All Chromium-based — identical WASM behavior to Chrome

---

## 5. Service Worker & Caching Architecture

### 5.1 Cache Strategy

```javascript
// service-worker.js — cache-first for versioned assets
const CACHE_NAME = 'zv-engine-v1';
const VERSIONED_ASSETS = [
  '/zv-engine.abc123.wasm',
  '/zv-meta.def456.bin',
  '/zv-ncr.ghi789.bin',
  // ... Revenue Region chunks
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(VERSIONED_ASSETS))
  );
});

self.addEventListener('fetch', (event) => {
  if (isVersionedAsset(event.request.url)) {
    // Cache-first: versioned assets are immutable
    event.respondWith(
      caches.match(event.request).then(cached => cached || fetch(event.request))
    );
  }
});
```

### 5.2 Update Flow

```
1. New BIR Department Order published for RDO 47 (Makati)
2. Ingestion pipeline re-parses RDO 47 workbook
3. New NCR data chunk built: zv-ncr.[new-hash].bin
4. index.html updated to reference new chunk hash
5. Service Worker detects index.html change on next visit
6. SW fetches only the changed chunk (~385 KB for NCR)
7. Old chunk evicted from cache
8. User sees fresh data — no full re-download
```

**Typical update size:** When a single RDO updates, only its Revenue Region chunk changes. Average chunk: ~230 KB brotli. Users download ~230 KB, not the full 4.8 MB.

### 5.3 Offline-First PWA

The application can register as a PWA (Progressive Web App) for full offline capability:

```json
// manifest.json
{
  "name": "PH Zonal Value Lookup",
  "short_name": "ZV Lookup",
  "start_url": "/",
  "display": "standalone",
  "description": "Privacy-first Philippine zonal value lookup engine"
}
```

After first visit with all chunks cached, the application works entirely offline — no network required for any lookup. This is unique among all surveyed platforms (Wave 4 competitive-gap-synthesis: zero platforms offer offline capability).

---

## 6. Performance Projections

### 6.1 First Visit (Cold Start)

| Phase | Transfer | Time (4G 30Mbps) | Time (rural 5Mbps) | Cumulative |
|-------|----------|------------------|--------------------|----|
| HTML + JS shell | ~50 KB | 13 ms | 80 ms | 80 ms |
| Engine WASM (stream compile) | ~200 KB | 53 ms | 320 ms | 400 ms |
| Jurisdiction metadata | ~400 KB | 107 ms | 640 ms | — |
| NCR data chunk | ~385 KB | 103 ms | 616 ms | — |
| **UI functional (NCR)** | — | **~280 ms** | **~1.7 s** | — |
| Remaining data (background) | ~3.7 MB | 987 ms | 5.9 s | — |
| **Full dataset ready** | — | **~1.3 s** | **~7.6 s** | — |

*Note: Engine WASM compilation overlaps with data download (streaming compilation). Jurisdiction + NCR data download is parallel.*

### 6.2 Repeat Visit (Warm Start)

| Phase | Transfer | Time | Notes |
|-------|----------|------|-------|
| HTML + JS shell | From SW cache | ~10 ms | No network |
| Engine WASM | From code cache | ~5 ms | V8 deserializes cached native code |
| Data | From Cache API | ~20 ms | Parsed into WASM memory |
| **UI functional** | — | **~35 ms** | Effectively instant |

### 6.3 Lookup Performance

From Wave 5 rust-engine-design performance targets:

| Operation | Target | Method |
|-----------|--------|--------|
| Exact match (street + vicinity) | <1 ms | LocationIndex O(1) scoping |
| Fuzzy match (5-tier cascade) | <10 ms | Per-barangay ~160 records |
| Full fallback (7-level tree) | <50 ms | Adjacent barangay scan |
| Bundle parse (cold) | <500 ms | Custom binary format |

---

## 7. Comparison Matrix: Final Decision

| Criterion | A: Full Client | B: Hybrid | **C: Tiered (Recommended)** | D: Server-Only |
|-----------|---------------|-----------|---------------------------|----------------|
| **Privacy** | Complete | Partial (city visible) | **Complete** | None |
| **Offline** | Full | Engine only | **Full** | None |
| **First-render latency** | ~1.3s (4G) | ~300ms | **~280ms (4G)** | ~300ms |
| **Full data ready** | ~1.3s | Per-query (~200ms each) | **~1.3s (background)** | Per-query |
| **Mobile budget users** | ~5 MB initial | ~200 KB initial | **~585 KB initial** | ~50 KB initial |
| **Rural users** | ~7.6s cold | ~2s + per-query | **~1.7s functional, 7.6s full** | Per-query |
| **Infrastructure cost** | ~$20/mo (CDN) | ~$100-200/mo | **~$20/mo (CDN) + $50 optional API** | ~$100-300/mo |
| **Update latency** | Hours (SW cycle) | Immediate | **Hours (SW cycle)** | Immediate |
| **RPVARA scalability** | Breaks at ~9 MB | Unlimited | **Graceful (chunked loading)** | Unlimited |
| **Historical data** | Not included | Via API | **Via optional API** | Included |
| **Competitive moat** | Strong (privacy) | Weak (API = commodity) | **Strong (privacy + speed)** | None |

### Why Option C Wins

1. **Best of both worlds:** 585 KB first render (as fast as hybrid) with full client-side privacy (as private as Option A)
2. **Graceful degradation:** Rural users get NCR lookups in 1.7 seconds; full dataset streams in background
3. **RPVARA-ready:** Dual-source data loaded as separate chunks — no architecture change when BLGF SMV data arrives
4. **Minimal infrastructure:** Static files on CDN + optional historical API
5. **Update efficiency:** Only changed Revenue Region chunks re-downloaded (~230 KB avg)
6. **Competitive moat:** No existing platform offers client-side computation, offline capability, or sub-1-second NCR lookups

---

## 8. Implementation Specifications

### 8.1 Web Worker Interface

```typescript
// worker.ts — WASM engine host
interface LookupQuery {
  municipality: string;
  barangay: string;
  street?: string;
  vicinity?: string;
  classification?: string;
  property_type: 'land' | 'condo' | 'parking';
  transaction_date?: string; // ISO 8601
  title_type?: 'CCT' | 'TCT';
  area_sqm?: number;
}

interface LookupResult {
  zonal_value_per_sqm: number | null;
  classification: string;
  department_order: string;
  effectivity_date: string;
  rdo: string;
  confidence: {
    overall: number;
    tier: 'HIGH' | 'MEDIUM' | 'LOW' | 'VERY_LOW' | 'NO_MATCH';
    breakdown: {
      address_match: number;
      classification: number;
      fallback_penalty: number;
      data_freshness: number;
      regime_penalty: number;
    };
  };
  fallback_level: number;
  fallback_description: string;
  regime: 'PRE_TRANSITION' | 'TRANSITION_YEAR_1' | 'POST_TRANSITION';
  warnings: string[];
  alternatives: Array<{
    classification: string;
    zonal_value_per_sqm: number;
  }>;
}

// Worker message protocol
type WorkerMessage =
  | { type: 'init'; chunks: ArrayBuffer[] }
  | { type: 'add_chunk'; region: string; data: ArrayBuffer }
  | { type: 'lookup'; id: number; query: LookupQuery }
  | { type: 'available_codes'; id: number; rdo: string; barangay: string };

type WorkerResponse =
  | { type: 'ready'; record_count: number; regions_loaded: string[] }
  | { type: 'chunk_loaded'; region: string; records_added: number }
  | { type: 'result'; id: number; result: LookupResult }
  | { type: 'codes'; id: number; codes: string[] }
  | { type: 'error'; id: number; message: string };
```

### 8.2 WASM Export Surface

From Wave 5 rust-engine-design, 5 exported functions:

```rust
#[wasm_bindgen]
pub fn init(data: &[u8]) -> Result<(), JsValue>;

#[wasm_bindgen]
pub fn add_chunk(region_data: &[u8]) -> Result<u32, JsValue>;

#[wasm_bindgen]
pub fn lookup(query_json: &str) -> String; // JSON LookupResult

#[wasm_bindgen]
pub fn available_codes(rdo: u8, barangay: u16) -> String; // JSON string[]

#[wasm_bindgen]
pub fn municipalities_for_rdo(rdo: u8) -> String; // JSON string[]
```

### 8.3 Data Bundle Build Pipeline

```
BIR workbooks (124 .xls files, ~182 MB)
    ↓ Rust parser (calamine crate)
Normalized records (690K rows, 4-column schema)
    ↓ String interning + binary serialization
Per-Revenue-Region binary chunks (19 + NCR)
    ↓ Brotli compression
CDN-ready artifacts (~4.8 MB total)
    ↓ Content-hash naming
Deployed to CDN with immutable cache headers
```

### 8.4 Lazy Loading Trigger Points

```typescript
// Progressive loading in React component
const ZonalValueLookup = () => {
  const [engine, setEngine] = useState<ZvEngine | null>(null);
  const [loadedRegions, setLoadedRegions] = useState<Set<string>>(new Set());

  useEffect(() => {
    // Phase 1: Load engine + metadata + NCR
    const worker = new Worker('/zv-worker.js');
    initializeEngine(worker).then(setEngine);
  }, []);

  useEffect(() => {
    if (!engine) return;
    // Phase 2: Load user's region based on selection
    // Triggered when user selects a non-NCR city
  }, [engine, selectedCity]);

  // Phase 3: Background loading of all regions
  useEffect(() => {
    if (!engine) return;
    loadRemainingRegions(engine, loadedRegions);
  }, [engine]);
};
```

---

## 9. Risk Assessment

### 9.1 Risks Mitigated by Tiered Loading

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| 5 MB too large for rural PH mobile | Medium | Medium | NCR-first at 585 KB; full data in background |
| iOS Safari memory OOM | Very Low | High | 25 MB runtime << 256 MB ceiling |
| RPVARA doubles dataset | Medium (2027) | Medium | Separate SMV chunks; only load for transitioned LGUs |
| BIR updates workbook format | Low | Medium | Engine and data separate; parser fix doesn't invalidate data cache |
| Browser doesn't support WASM | Negligible | High | 99%+ PH browsers support WASM (Chrome 90%, Safari 8%) |

### 9.2 Residual Risks (Accepted)

| Risk | Probability | Impact | Acceptance Rationale |
|------|------------|--------|---------------------|
| Data bundle stale for hours after BIR update | High | Low | BIR updates are pre-announced; practitioners expect lead time |
| Service Worker cache not cleared by user | Low | Low | Content-hash versioning ensures fresh data on SW update cycle |
| Very old devices (pre-WASM browsers) | Negligible | Low | <1% of PH users; no remediation planned |

---

## 10. Design Decisions Traced to Wave Findings

| # | Decision | Rationale | Source |
|---|----------|-----------|--------|
| 1 | Full client-side primary architecture | 4.6 MB brotli fits mobile budget; privacy is competitive moat | Wave 2 data-size-estimation, Wave 4 competitive-gap-synthesis |
| 2 | Separate engine WASM from data chunks | Independent versioning; only changed RR chunks re-downloaded | Wave 2 sheet-organization (DO-per-RDO update pattern) |
| 3 | NCR-first loading (585 KB) | ~80% of tax transactions are NCR; 24 RDOs = 40K records = 385 KB | Wave 2 data-size-estimation §6.2 |
| 4 | Revenue Region chunking (19 chunks) | Natural administrative boundary; avg ~230 KB per chunk | Wave 3 rdo-jurisdiction-mapping (RR→RDO mapping) |
| 5 | Web Worker isolation | Privacy: extensions can't access WASM memory in Worker context | Wave 4 competitive-gap-synthesis (privacy gap #1) |
| 6 | Historical data API-only | 18 MB brotli exceeds mobile WASM budget; <5% of queries | Wave 2 data-size-estimation §4.2 |
| 7 | Service Worker + Cache API (not IndexedDB) | V8 auto-caches compiled WASM from network fetch; SW is the standard pattern | Browser WASM code caching requires network fetch path |
| 8 | Content-hash versioning on all artifacts | Per-chunk invalidation on BIR updates; immutable cache headers | Wave 2 sheet-organization (per-RDO update frequency) |
| 9 | RPVARA SMV as separate chunk type | Dual-source loaded only for transitioned LGUs; no pre-loading waste | Wave 3 rpvara-dual-source-resolution §7 |
| 10 | PWA manifest for offline installation | Tax practitioners need offline lookups at BIR offices, client meetings | Wave 4 competitive-gap-synthesis (zero platforms offer offline) |
| 11 | Custom binary format (not JSON/Protobuf) | 7x smaller than JSON, 3.4x smaller than Protobuf; Rust reads directly | Wave 2 data-size-estimation §4.1 |
| 12 | Brotli compression (not gzip) | 30% compression ratio vs 38% gzip on binary data; universal browser support | Wave 2 data-size-estimation §4.1 |

---

## Sources

- Wave 2 `data-size-estimation.md` — record counts, binary format sizing, compression ratios
- Wave 3 `rpvara-dual-source-resolution.md` — dual-source data volume projections
- Wave 4 `competitive-gap-synthesis.md` — privacy gap analysis, platform capabilities
- Wave 5 `rust-engine-design.md` — WASM export surface, binary bundle format, performance targets
- Ookla Speedtest Global Index (2025) — Philippine mobile median 35.56 Mbps
- Opensignal Philippines April 2025 — per-carrier download speed experience
- StatCounter (February 2026) — Philippine browser market share (Chrome 90.1% mobile)
- V8 Blog: Code Caching for WebAssembly Developers — automatic caching >128 KB modules
- V8 Blog: WASM Compilation Pipeline — streaming compilation, Liftoff→TurboFan tiering
- Mozilla Hacks: Firefox Streaming and Tiering Compiler — 30-60 MB/s desktop compile rate
- Godot issue #70621 — iOS Safari 256 MB WASM memory ceiling
- Emscripten issue #19374 — Safari memory leak on reload
- DuckDB WASM — ~3.2 MB compressed transfer size benchmark
- Philippine Standard Geographic Codes (PSGC) — PSA barangay/municipality canonical IDs
- DICT Internet Speed Report March 2025 — Philippines last in ASEAN for mobile broadband
- Globe Go50/Go+99 prepaid plans — ₱10/GB effective data cost
- NCR minimum wage (2025) — ₱695/day (DOLE Wage Order)
