# Frontend & API Design — Zonal Value Lookup Engine

**Wave 5 | Aspect: frontend-api-design**
**Date:** 2026-03-04
**Depends on:** Wave 2 (all format analyses), Wave 3 (all resolution logic), Wave 4 (competitive-gap-synthesis), Wave 5 (rust-engine-design, wasm-vs-hybrid-tradeoff, data-pipeline-architecture)

---

## Summary

This analysis designs the TypeScript/React frontend and API contracts for the Zonal Value Lookup Engine. The frontend is a **progressive web app** (PWA) that loads the WASM engine and data bundles client-side, performs all lookups locally (property details never leave the browser), and surfaces results with confidence scoring, legal metadata, and RPVARA regime awareness. A **public REST API** serves downstream integrators (tax calculators, property platforms, law firm tools) with the same resolution logic via a thin server-side wrapper around the Rust engine.

The design addresses every competitive gap identified in Wave 4: address-based resolution (not table browsing), legal metadata (DO#, effectivity date), confidence scoring, privacy-preserving client-side computation, RPVARA regime display, and API-first architecture for programmatic access.

---

## 1. Frontend Architecture

### 1.1 Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Framework | React 19 + TypeScript | Dominant PH developer ecosystem (Wave 4: Housal uses Next.js, REN.PH uses Next.js); component model fits cascading input UX |
| Build | Vite 6 | Fast dev, tree-shaking, WASM-compatible import; RealValueMaps also uses Vite (Wave 4) |
| Styling | Tailwind CSS 4 | Utility-first, small bundle, matches industry practice |
| State | Zustand | Lightweight — no Redux overhead for essentially 3 state slices (engine, query, result) |
| WASM bridge | wasm-bindgen + Web Worker | Engine runs in dedicated Worker for privacy isolation (Wave 5 wasm-vs-hybrid-tradeoff §2.4) |
| PWA | Workbox 7 | Service Worker for offline capability — unique among all 7 competitors (Wave 4) |
| Hosting | Static CDN (Cloudflare Pages) | ~$20/mo, no server for frontend (Wave 5 wasm-vs-hybrid-tradeoff §2.6) |

**Design decision trace:** React over Svelte/Vue because (1) PH developer hiring pool is largest for React, (2) both leading competitors use Next.js/React (Wave 4), (3) React 19's concurrent features handle the async WASM Worker communication naturally.

### 1.2 Application Structure

```
src/
├── main.tsx                      # Entry, Service Worker registration
├── App.tsx                       # Root layout, loading states
├── worker/
│   ├── engine.worker.ts          # Web Worker: WASM init + lookup bridge
│   └── messages.ts               # Typed postMessage protocol
├── hooks/
│   ├── useEngine.ts              # Engine lifecycle (init, load chunks, status)
│   ├── useLookup.ts              # Debounced lookup with result state
│   ├── useLocationCascade.ts     # City → Barangay cascading dropdown state
│   └── useAvailableCodes.ts      # Classification codes for current location
├── components/
│   ├── lookup/
│   │   ├── LookupForm.tsx        # Primary input form
│   │   ├── LocationSelector.tsx  # City/Barangay cascading dropdowns
│   │   ├── AddressInput.tsx      # Street + vicinity free-text with suggestions
│   │   ├── ClassificationPicker.tsx # Available codes for location
│   │   ├── PropertyTypeSelector.tsx # Land / Condo / Parking
│   │   └── TransactionDatePicker.tsx # For DO effectivity + regime detection
│   ├── result/
│   │   ├── ResultCard.tsx        # Primary result display
│   │   ├── ConfidenceBadge.tsx   # Color-coded confidence tier
│   │   ├── MatchExplanation.tsx  # How the match was made (transparency)
│   │   ├── FallbackIndicator.tsx # Which fallback level, why
│   │   ├── LegalMetadata.tsx     # DO#, effectivity, RDO, regime
│   │   ├── WarningsList.tsx      # Stale schedule, regime mismatch, etc.
│   │   └── AlternativeValues.tsx # Other classifications at same location
│   ├── status/
│   │   ├── EngineStatus.tsx      # Loading progress, data freshness
│   │   ├── DataCoverage.tsx      # Which Revenue Regions loaded
│   │   └── RegimeBanner.tsx      # RPVARA transition awareness
│   └── shared/
│       ├── SearchableDropdown.tsx # Typeahead for city/barangay
│       └── LoadingSpinner.tsx
├── stores/
│   ├── engineStore.ts            # WASM state: loaded chunks, version
│   ├── queryStore.ts             # Current query input
│   └── resultStore.ts            # Last lookup result
├── types/
│   ├── query.ts                  # LookupQuery TypeScript interface
│   ├── result.ts                 # LookupResult TypeScript interface
│   └── engine.ts                 # Engine status types
├── lib/
│   ├── workerBridge.ts           # Type-safe Worker message passing
│   └── formatting.ts             # PHP currency, classification labels
└── sw.ts                         # Service Worker (Workbox precache)
```

### 1.3 Web Worker Communication Protocol

The WASM engine runs in a dedicated Web Worker. The main thread never touches WASM memory — this is the privacy boundary (Wave 5 wasm-vs-hybrid-tradeoff §2.4).

```typescript
// worker/messages.ts

// Main → Worker
type WorkerRequest =
  | { type: 'init'; chunks: ArrayBuffer[] }
  | { type: 'loadChunk'; regionId: number; data: ArrayBuffer }
  | { type: 'lookup'; id: string; query: LookupQuery }
  | { type: 'availableCodes'; rdo: number; municipality: number; barangay: number }
  | { type: 'municipalities'; rdo: number }
  | { type: 'barangays'; rdo: number; municipality: number }
  | { type: 'dataVersion' }

// Worker → Main
type WorkerResponse =
  | { type: 'initComplete'; version: string; recordCount: number }
  | { type: 'chunkLoaded'; regionId: number; recordCount: number }
  | { type: 'lookupResult'; id: string; result: LookupResult }
  | { type: 'availableCodesResult'; codes: ClassCodeInfo[] }
  | { type: 'municipalitiesResult'; items: LocationItem[] }
  | { type: 'barangaysResult'; items: LocationItem[] }
  | { type: 'dataVersionResult'; version: DataVersion }
  | { type: 'error'; id?: string; message: string }
```

**Design decision trace:** JSON-serialized `postMessage` rather than `SharedArrayBuffer` because (1) query/result payloads are small (<10 KB), (2) SAB requires COOP/COEP headers which complicate CDN deployment, (3) serialization cost is negligible vs. the <10ms engine lookup time.

### 1.4 Engine Lifecycle

```typescript
// hooks/useEngine.ts

interface EngineState {
  status: 'uninitialized' | 'loading-core' | 'loading-ncr' | 'ncr-ready'
         | 'loading-full' | 'ready' | 'error';
  loadedRegions: Set<number>;    // Revenue Region IDs loaded
  recordCount: number;
  dataVersion: string;           // Content-hash of manifest
  lastUpdated: string;           // ISO date of latest DO in dataset
}

// Loading sequence (from Wave 5 wasm-vs-hybrid-tradeoff §3.1):
// Phase 1: engine.wasm + jurisdiction.bin + meta.bin    (~585 KB brotli)
// Phase 2: ncr-data.bin                                 (~385 KB brotli)
// Phase 3: remaining 19 Revenue Region chunks           (~3.7 MB total, background)
```

**Progressive readiness:** The UI is functional as soon as NCR data loads (~500ms on 4G). A subtle banner shows "Loading provincial data..." during Phase 3. If the user searches for a provincial location before its chunk is loaded, the UI shows "Loading [Revenue Region name]..." and fetches that specific chunk on demand.

---

## 2. Search UX Design

### 2.1 Input Model

The search form maps to the engine's `LookupQuery` (Wave 5 rust-engine-design §4.1):

```typescript
// types/query.ts

interface LookupQuery {
  // Required — cascading dropdowns
  cityMunicipality: string;      // Searchable dropdown, PSGC-backed
  barangay: string;              // Searchable dropdown, filtered by city

  // Optional — free-text with autocomplete
  street?: string;               // "Ayala Avenue", "Shaw Blvd"
  vicinity?: string;             // "near EDSA", "along National Highway"

  // Required for classification — dynamic per-location
  classification?: ClassCode;    // Populated from availableCodes()

  // Property type — radio buttons
  propertyType: 'land' | 'condo' | 'parking';

  // Condo-specific (shown only when propertyType = 'condo')
  condoBuilding?: string;        // Building name
  titleType?: 'CCT' | 'TCT';    // Condominium vs Transfer Certificate

  // BGC-specific (shown only for Taguig + Fort Bonifacio)
  floorAreaRatio?: number;       // FAR 1-18

  // Optional — for DO effectivity + regime detection
  transactionDate?: string;      // ISO date, defaults to today

  // Provincial-specific (shown for provincial barangays)
  roadProximity?: RoadTier;      // National Highway → Interior → Watershed
}
```

### 2.2 Input Flow (Step by Step)

The input form uses **progressive disclosure** — fields appear as they become relevant, reducing cognitive load for simple lookups while exposing full power for complex ones.

```
Step 1: WHERE (always shown)
┌─────────────────────────────────────────────────────┐
│  City / Municipality    [Makati City          ▼]    │
│  Barangay               [Bel-Air              ▼]    │
│  Street (optional)      [Ayala Avenue            ]  │
│  Vicinity (optional)    [near Paseo de Roxas      ] │
└─────────────────────────────────────────────────────┘

Step 2: WHAT (always shown)
┌─────────────────────────────────────────────────────┐
│  Property Type     ◉ Land  ○ Condo  ○ Parking       │
│  Classification    [Commercial Regular (CR)    ▼]   │
│                    ↑ Only shows codes available at   │
│                      this barangay (e.g., 5 for     │
│                      Binondo vs 43 for Davao)       │
└─────────────────────────────────────────────────────┘

Step 3: WHEN (collapsed by default, expandable)
┌─────────────────────────────────────────────────────┐
│  ▸ Transaction Date (defaults to today)              │
│    [2026-03-04]                                      │
│    ↑ Determines which DO revision applies +          │
│      RPVARA regime detection                         │
└─────────────────────────────────────────────────────┘

Conditional fields (appear based on context):
┌─────────────────────────────────────────────────────┐
│  IF propertyType = 'condo':                          │
│    Building Name    [One Rockwell               ]    │
│    Title Type       ◉ CCT  ○ TCT                     │
│                                                       │
│  IF barangay = 'Fort Bonifacio' (BGC):               │
│    Floor Area Ratio [▼ FAR 1-18]                     │
│                                                       │
│  IF provincial location detected:                    │
│    Road Proximity   [▼ National Highway / Interior]  │
└─────────────────────────────────────────────────────┘
```

**Design decision trace:**
- **City → Barangay cascading dropdowns** rather than a single address text field because: (1) BIR organizes data by barangay — the matching pipeline needs barangay as input (Wave 3 address-matching-algorithms §2); (2) all 7 competitors use this pattern — validated UX for Filipino users (Wave 4); (3) structured input eliminates a class of ambiguity (which "San Isidro"?).
- **Classification as dropdown, not free-text**, because: (1) only codes available at the selected barangay are valid (RDO 30 Binondo has 5 codes, RDO 113A Davao has 43 — Wave 2 classification-code-usage); (2) user may not know BIR classification codes — dropdown shows human-readable labels.
- **Transaction date** defaulting to today but user-adjustable, because: (1) CTA rulings require the specific revision effective at transaction date (Wave 1 cta-zonal-rulings; Wave 4 competitive-gap-synthesis §2.3); (2) no competitor supports this — unique differentiator.
- **Progressive disclosure** for condo/BGC/provincial fields because: (1) 60%+ of lookups are simple land queries — don't clutter with condo fields; (2) BGC FAR is relevant to only 544 records in RDO 44 (Wave 2 address-vicinity-patterns); (3) road proximity only matters for provincial (59.3% of records but <20% of users per Wave 4 Housal traffic patterns).

### 2.3 Autocomplete & Suggestions

```typescript
// Location selectors: backed by WASM engine data

// City search: type-ahead over ~1,913 municipalities
// Source: Wave 3 rdo-jurisdiction-mapping — PSGC-backed, ~42K barangays
// Uses municipalities_for_rdo() WASM export for RDO-aware filtering
citySearch(query: string): LocationItem[] {
  // Filter from jurisdiction data loaded in Phase 1
  // Return top 10 matches, sorted by: exact prefix > fuzzy > population rank
}

// Barangay search: filtered by selected city
barangaySearch(cityId: number, query: string): LocationItem[] {
  // Uses barangays_for_municipality() WASM export
  // Special handling for Manila's ~897 numbered barangays (Wave 2)
}

// Street suggestions: NOT from engine data (would reveal data structure)
// Instead: no server-side suggestions — user types freely
// The engine does the matching client-side after submission
```

**Privacy note:** Street autocomplete could reveal data structure to network observers. Since all computation is client-side and the engine handles fuzzy matching, we don't need server-side street suggestions. The user types freely; the engine matches.

### 2.4 Classification Display

Classification codes are displayed with human-readable labels and contextual grouping:

```typescript
// lib/formatting.ts

const CLASSIFICATION_LABELS: Record<string, { label: string; group: string }> = {
  'RR':  { label: 'Residential Regular', group: 'Residential' },
  'CR':  { label: 'Commercial Regular', group: 'Commercial' },
  'RC':  { label: 'Residential Condominium', group: 'Condominium' },
  'CC':  { label: 'Commercial Condominium', group: 'Condominium' },
  'PS':  { label: 'Parking Slot', group: 'Condominium' },
  'I':   { label: 'Industrial', group: 'Industrial' },
  'X':   { label: 'Institutional / Exempt', group: 'Institutional' },
  'GL':  { label: 'Government Lot', group: 'Government' },
  'GP':  { label: 'Government Property (≥5,000 sqm)', group: 'Government' },
  'CL':  { label: 'Communal Lot', group: 'Government' },
  'APD': { label: 'Ancestral Property Domain', group: 'Government' },
  'DA':  { label: 'Drying Area', group: 'Agricultural' },
  'A':   { label: 'Agricultural (General)', group: 'Agricultural' },
  // A1-A50 grouped under Agricultural with specific labels
  'A1':  { label: 'Riceland – Irrigated', group: 'Agricultural' },
  'A2':  { label: 'Riceland – Rain-fed', group: 'Agricultural' },
  // ... (50 agricultural sub-codes per RMO 31-2019 Annex B, Wave 1)
};

// Dropdown groups codes by category, only shows codes available at location
// Source: Wave 2 classification-code-usage — NCR shows ~7 codes, provincial shows ~59
```

---

## 3. Result Display

### 3.1 Result Card Structure

The result card is the primary output. It must communicate: the value, how confident we are, why we're confident (or not), and the legal authority.

```
┌─────────────────────────────────────────────────────────────┐
│  ZONAL VALUE                                                │
│                                                              │
│  ₱35,000 /sqm                 [HIGH CONFIDENCE] ████████░░  │
│                                                  92%         │
│                                                              │
│  Classification: Commercial Regular (CR)                     │
│  Location: Bel-Air, Makati City (RDO 47 — North Makati)     │
│  Matched: AYALA AVENUE — PASEO DE ROXAS TO MAKATI AVENUE    │
│                                                              │
│  ┌─ Legal Authority ─────────────────────────────────────┐  │
│  │  DO 022-2021 (7th Revision)                           │  │
│  │  Effective: January 1, 2022                           │  │
│  │  Regime: Pre-transition (BIR Zonal Value)             │  │
│  │  Tax base: max(Selling Price, Zonal Value, FMV)       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ⚠ Schedule is 4 years old (last revised 2022).             │
│    BIR may issue a new revision. Check bir.gov.ph           │
│                                                              │
│  ▸ How was this matched? (expandable)                        │
│  ▸ Other classifications at this location (3 available)      │
│  ▸ View revision history                                     │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Confidence Display

Confidence is the engine's most important differentiating output — no competitor has it (Wave 4 competitive-gap-synthesis §2.2).

```typescript
// components/result/ConfidenceBadge.tsx

interface ConfidenceDisplay {
  tier: 'HIGH' | 'MEDIUM' | 'LOW' | 'VERY_LOW' | 'NO_MATCH';
  score: number;         // 0.0–1.0
  color: string;         // Semantic color
  message: string;       // Human-readable explanation
}

// Source: Wave 3 address-matching-algorithms — 5-tier model
// Wave 5 rust-engine-design §2.5
const CONFIDENCE_TIERS: Record<string, ConfidenceDisplay> = {
  HIGH: {
    tier: 'HIGH',
    color: '#16a34a',     // Green
    message: 'Exact or near-exact match found. This value is highly reliable.',
  },
  MEDIUM: {
    tier: 'MEDIUM',
    color: '#ca8a04',     // Amber
    message: 'Good match with minor ambiguity. Verify the matched address.',
  },
  LOW: {
    tier: 'LOW',
    color: '#ea580c',     // Orange
    message: 'Approximate match. The engine used fallback rules. Verify carefully.',
  },
  VERY_LOW: {
    tier: 'VERY_LOW',
    color: '#dc2626',     // Red
    message: 'Weak match. This value may not apply to your property. Consider a BIR written inquiry.',
  },
  NO_MATCH: {
    tier: 'NO_MATCH',
    color: '#6b7280',     // Gray
    message: 'No published zonal value found for this location and classification.',
  },
};
```

### 3.3 Match Explanation (Transparency)

The expandable "How was this matched?" section shows the engine's reasoning — critical for professional users (tax practitioners, lawyers) who need to justify the value used.

```
▾ How was this matched?

  Address mode: NCR Cross-Street Boundaries
  Street match: Exact (normalized "AYALA AVENUE" = "AYALA AVENUE")
  Vicinity match: Boundary segment "PASEO DE ROXAS TO MAKATI AVENUE"
  Classification: Single code at location (auto-resolved)
  Fallback level: Level 0 — Exact match

  Confidence breakdown:
    Address match quality:    1.00  (exact)
    Classification certainty: 1.00  (single code)
    Fallback penalty:         1.00  (no fallback needed)
    Data freshness:           0.95  (4 years since revision)
    Regime penalty:           1.00  (pre-transition)
    ─────────────────────────
    Composite:                0.95 → capped at 1.00 → 0.95

  Source: Wave 3 address-matching-algorithms (8-phase pipeline),
          Wave 3 fallback-hierarchy-implementation (7-level decision tree)
```

**Design decision trace:** Exposing the full confidence breakdown is a deliberate differentiation choice. Per Wave 4 competitive-gap-synthesis §6.1, every competitor treats lookup as a black box. Tax practitioners need to understand *why* a value was returned to defend it in a BIR assessment or CTA proceeding. The breakdown directly maps to the Rust engine's `ConfidenceBreakdown` struct (Wave 5 rust-engine-design §2.5).

### 3.4 Fallback Scenarios

Different fallback levels produce different result card layouts:

**Level 0 (Exact Match):** Standard green result card. No warnings.

**Level 1-2 (Same Street / Fuzzy):** Amber banner: "Matched to a nearby vicinity segment on the same street" or "Matched via alias: VITO CRUZ → PABLO OCAMPO SR."

**Level 3 (Catch-All):** Amber banner: "No specific entry for this street. Using the barangay's general zonal value for 'ALL OTHER STREETS/LOTS'."

**Level 4 (Adjacent Barangay):** Orange banner: "No entry in [Barangay]. Using value from adjacent [Other Barangay]. This is an approximation per DOF Department Order Rule 2."

**Level 5 (Institutional → CR):** Orange banner: "No institutional (X) zonal value published. Using nearest commercial regular (CR) value per DOF DO footnote."

**Level 6 (No Match):** Gray result card with no value. Explicit message: "No published zonal value exists for this location and classification. Per CTA rulings (Emiliano EB 1103, Gamboa 9720), the BIR cannot substitute an arbitrary value. You may need to request a BIR written inquiry (RMO 31-2019 procedure)."

**Design decision trace:** The explicit Level 6 NULL return is a legal compliance feature, not a UX failure. Per Wave 1 cta-zonal-rulings and Wave 3 fallback-hierarchy-implementation, the engine must never fabricate a value. Telling the user "no value exists" is the legally correct answer. The message references the BIR written inquiry procedure (RMO 31-2019) as the next step.

### 3.5 Warnings Display

Warnings surface data quality issues and legal caveats. Sourced from `Warning` enum (Wave 5 rust-engine-design §2.5):

| Warning | Display | Priority |
|---------|---------|----------|
| `StaleSchedule` | "⚠ Schedule is [N] years old (last revised [year])." | Medium — shown for >3 years |
| `RegimeSourceMismatch` | "⚠ This LGU has transitioned to BLGF SMV, but SMV data is not yet available. Using BIR zonal value as fallback." | High — shown in Regime B/C |
| `MultipleClassifications` | "ℹ [N] classification codes available at this location. Showing [selected]. [View all →]" | Low — informational |
| `AgriculturalAreaThreshold` | "ℹ Agricultural classification (GP) typically requires ≥5,000 sqm lot area." | Low |
| `IntraBarangaySplit` | "ℹ This barangay spans two RDOs. Your street was matched to RDO [N]." | Medium |
| `NoCoverageBarmmLgu` | "⚠ This municipality has no published BIR RDO assignment (BARMM, 2024). No zonal value data available." | High |
| `NonStandardCode` | "ℹ Classification '[WC]' is a non-standard regional code. Mapped to [CR] for lookup." | Low |

### 3.6 Alternative Values Section

When multiple classifications are available at the same location (30% of lookups per Wave 3 classification-resolution-logic):

```
▾ Other classifications at this location (5 available)

  Classification           Zonal Value    Status
  ─────────────────────────────────────────────────
  Residential Regular (RR) ₱25,000/sqm
  Commercial Regular (CR)  ₱35,000/sqm    ← Selected
  Industrial (I)           ₱20,000/sqm
  Institutional (X)        —              (uses CR fallback)
  Government Lot (GL)      ₱15,000/sqm
```

---

## 4. RPVARA Transition UX

### 4.1 Regime Awareness

The frontend detects the applicable RPVARA regime per the engine's three-regime model (Wave 3 rpvara-dual-source-resolution) and displays it prominently:

**Regime A (Pre-transition — vast majority as of March 2026):**
```
Legal Authority
  DO 022-2021 (7th Revision)
  Effective: January 1, 2022
  Regime: Pre-transition (BIR Zonal Value)
  Tax base formula: max(Selling Price, Zonal Value, FMV)
```

**Regime B (Transition Year 1 — hypothetical until SMVs are approved):**
```
Legal Authority
  BLGF SMV Schedule — [Municipality], [Year]
  Effective: [Date]
  Regime: RPVARA Transition Year 1 (6% RPT cap applies)
  Tax base formula: max(Selling Price, Schedule of Market Values)

  ⚠ RPVARA Transition Notice
  This municipality has transitioned from BIR Zonal Values to
  BLGF Schedule of Market Values under RA 12001. The 6% RPT
  increase cap (Section 29(c)) applies for the first year.

  BIR Zonal Value (pre-transition): ₱35,000/sqm
  BLGF SMV (current):               ₱42,000/sqm
```

**Regime C (Post-transition steady state):**
```
Legal Authority
  BLGF SMV Schedule — [Municipality], [Year]
  Regime: Post-transition (BLGF SMV, steady state)
  Tax base formula: max(Selling Price, Schedule of Market Values)
```

### 4.2 Dual-Source Display

When both BIR ZV and BLGF SMV data exist for a location (transition period), the result card shows both values with clear labeling:

```
┌─ Dual-Source Values (RPVARA Transition) ──────────────┐
│                                                         │
│  BLGF SMV:  ₱42,000/sqm  ← applies for this regime    │
│  BIR ZV:    ₱35,000/sqm  (pre-transition reference)    │
│                                                         │
│  The applicable value depends on the transaction type:  │
│  • Capital Gains Tax: uses BLGF SMV (post-transition)   │
│  • Real Property Tax: 6% cap applies (transition yr 1)  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Public REST API

### 5.1 Architecture

The API is a thin HTTP wrapper around the same `zv-engine` Rust crate used by the WASM frontend. It runs as a Rust server (axum) with the engine loaded in-process — no database, no ORM, just the binary data bundle in memory.

```
API Architecture:
  CDN (Cloudflare) → axum server → zv-engine (in-process)
                                      ↓
                                  Binary data bundle
                                  (~17 MB in memory)
```

**Design decision trace:** API exists because (1) Wave 4 competitive-gap-synthesis identified "no API anywhere" as the single largest structural gap; (2) downstream tax computation engines, property platforms, and legal compliance tools need programmatic access; (3) API-first infrastructure has a 6-12 month first-mover window.

### 5.2 Base URL & Versioning

```
Base URL: https://api.zonalvalue.ph/v1
Versioning: URL path (/v1, /v2) for breaking changes
Content-Type: application/json
Authentication: API key via X-Api-Key header
Rate limits: Free tier 100 req/day, Pro 10,000 req/day, Enterprise unlimited
```

### 5.3 Endpoints

#### 5.3.1 Lookup (Primary)

```
POST /v1/lookup

Request:
{
  "city_municipality": "Makati City",
  "barangay": "Bel-Air",
  "street": "Ayala Avenue",
  "vicinity": "Paseo de Roxas to Makati Avenue",
  "classification": "CR",
  "property_type": "land",
  "transaction_date": "2026-03-04"
}

Response (200):
{
  "zonal_value": {
    "amount_per_sqm": 35000.00,
    "currency": "PHP",
    "amount_centavos": 3500000
  },
  "confidence": {
    "score": 0.95,
    "tier": "HIGH",
    "breakdown": {
      "address_match": 1.00,
      "classification": 1.00,
      "fallback_penalty": 1.00,
      "data_freshness": 0.95,
      "regime_penalty": 1.00
    }
  },
  "match": {
    "mode": "ncr_cross_street",
    "street_method": "exact_normalized",
    "matched_street": "AYALA AVENUE",
    "matched_vicinity": "PASEO DE ROXAS - MAKATI AVENUE",
    "fallback_level": 0,
    "fallback_name": "exact_match"
  },
  "classification": {
    "code": "CR",
    "label": "Commercial Regular",
    "path": "single_code",
    "alternatives": ["RR", "I", "X", "GL"]
  },
  "legal": {
    "department_order": "DO 022-2021",
    "revision": "7th Revision",
    "effectivity_date": "2022-01-01",
    "rdo": {
      "id": 47,
      "name": "North Makati",
      "revenue_region": "RR7A"
    },
    "regime": "pre_transition",
    "tax_base_formula": "three_way_max",
    "formula_description": "max(Selling Price, Zonal Value, FMV)"
  },
  "warnings": [
    {
      "code": "stale_schedule",
      "message": "Schedule is 4 years old (last revised 2022).",
      "severity": "medium"
    }
  ],
  "data_version": "2026-03-01T00:00:00Z",
  "engine_version": "1.0.0"
}
```

**Response when no value found (Level 6 fallback):**

```
Response (200):
{
  "zonal_value": null,
  "confidence": {
    "score": 0.0,
    "tier": "NO_MATCH"
  },
  "match": {
    "fallback_level": 6,
    "fallback_name": "no_match"
  },
  "legal": {
    "note": "No published zonal value exists for this location and classification. Per CTA rulings (Emiliano EB 1103, Gamboa 9720), the BIR cannot substitute an arbitrary value.",
    "next_step": "Request a BIR written inquiry per RMO 31-2019 procedure."
  },
  "warnings": []
}
```

**Design decision trace:**
- Returns `null` for `zonal_value` rather than omitting the field, because downstream consumers need an explicit signal vs. an error. Per Wave 3 fallback-hierarchy-implementation: "engine returns None at Level 6 per CTA rulings."
- `amount_centavos` integer field alongside `amount_per_sqm` float, because Wave 5 rust-engine-design §8 Decision #14: "Integer arithmetic (centavos) — avoids floating-point rounding in tax computation."
- `regime` and `tax_base_formula` included in every response because downstream tax calculators need this to select the correct formula (Wave 3 rpvara-dual-source-resolution: three-way max vs. two-way max).

#### 5.3.2 Available Classifications

```
GET /v1/classifications?city=Makati+City&barangay=Bel-Air

Response (200):
{
  "city_municipality": "Makati City",
  "barangay": "Bel-Air",
  "rdo": { "id": 47, "name": "North Makati" },
  "available_codes": [
    { "code": "RR", "label": "Residential Regular" },
    { "code": "CR", "label": "Commercial Regular" },
    { "code": "RC", "label": "Residential Condominium" },
    { "code": "CC", "label": "Commercial Condominium" },
    { "code": "PS", "label": "Parking Slot" },
    { "code": "I", "label": "Industrial" },
    { "code": "X", "label": "Institutional / Exempt" }
  ]
}
```

**Design decision trace:** This endpoint exists because Wave 2 classification-code-usage found stark NCR/provincial divergence: NCR is a 7-code system, provincial is 59-code. The frontend classification picker must be filtered to available codes — the API supports this for downstream integrators too.

#### 5.3.3 Location Hierarchy

```
GET /v1/locations/municipalities?region=NCR

Response (200):
{
  "municipalities": [
    { "id": 137600, "name": "Makati City", "rdo_ids": [47, 48, 49, 50] },
    { "id": 137500, "name": "Taguig City", "rdo_ids": [44] },
    ...
  ]
}

GET /v1/locations/barangays?municipality_id=137600

Response (200):
{
  "municipality": { "id": 137600, "name": "Makati City" },
  "barangays": [
    { "id": 13760001, "name": "Bel-Air", "rdo_id": 47 },
    { "id": 13760002, "name": "Cembo", "rdo_id": 44, "note": "EMBO transfer per RAO 1-2024" },
    ...
  ]
}
```

**Design decision trace:** PSGC-based IDs per Wave 4 realvaluemaps-approach design validation ("PSGC codes as canonical location keys") and Wave 5 rust-engine-design Decision #10.

#### 5.3.4 Data Version & Freshness

```
GET /v1/data/version

Response (200):
{
  "version": "2026-03-01",
  "bundle_hash": "a3f8c2...",
  "total_records": 690412,
  "rdo_coverage": 122,
  "rdo_total": 124,
  "missing_rdos": [
    { "id": 115, "reason": "PDF-only workbook, not machine-readable" },
    { "id": 119, "reason": "File not published on bir.gov.ph" }
  ],
  "latest_department_order": {
    "number": "DO 045-2025",
    "rdo": 47,
    "effectivity": "2025-07-01"
  },
  "stale_schedule_count": 47,
  "stale_schedule_pct": 38.2,
  "regime_summary": {
    "pre_transition": 1713,
    "in_preparation": 2,
    "approved_smv": 0
  }
}
```

#### 5.3.5 Bulk Lookup (Pro/Enterprise)

```
POST /v1/lookup/bulk

Request:
{
  "queries": [
    { "city_municipality": "Makati City", "barangay": "Bel-Air", "classification": "CR" },
    { "city_municipality": "Taguig City", "barangay": "Fort Bonifacio", "classification": "CC", "floor_area_ratio": 12 },
    { "city_municipality": "Pangasinan", "barangay": "Poblacion", "classification": "A1", "road_proximity": "national_highway" }
  ]
}

Response (200):
{
  "results": [
    { /* same as single lookup result */ },
    { /* ... */ },
    { /* ... */ }
  ],
  "batch_id": "b7a3f1...",
  "processing_time_ms": 12
}
```

Max 100 queries per batch (free), 1,000 (Pro), 10,000 (Enterprise).

#### 5.3.6 Historical Lookup (Pro/Enterprise)

```
POST /v1/lookup/historical

Request:
{
  "city_municipality": "Makati City",
  "barangay": "Bel-Air",
  "street": "Ayala Avenue",
  "classification": "CR",
  "transaction_date": "2019-06-15"
}

Response: Same as /v1/lookup but resolves against the DO revision
effective at the specified transaction_date. Uses the server-side
historical dataset (~2.97M records) not available in the WASM bundle.
```

**Design decision trace:** Historical data is ~18 MB brotli (Wave 2 data-size-estimation), too large for WASM bundle. Wave 5 wasm-vs-hybrid-tradeoff §3.1 Phase 3 designates historical as server-side only. This endpoint fulfills that design.

### 5.4 Error Responses

```typescript
// Standard error format

interface ApiError {
  error: {
    code: string;          // Machine-readable
    message: string;       // Human-readable
    details?: object;      // Additional context
  };
}

// Error codes:
// 400 — invalid_query: Missing required fields, invalid classification code, etc.
// 401 — unauthorized: Missing or invalid API key
// 404 — location_not_found: City/barangay not in jurisdiction map
// 429 — rate_limit_exceeded: Include Retry-After header
// 500 — engine_error: Internal engine failure (should never happen)
// 503 — data_loading: Engine still loading data on startup
```

### 5.5 API Pricing Model

Source: Wave 4 competitive-gap-synthesis §4.1 — RealValueMaps' freemium pricing (Free/₱2,999/₱9,999) validates commercial model. Adjusted based on actual market context.

| Tier | Price | Requests/day | Features |
|------|-------|-------------|----------|
| Free | ₱0 | 100 | Single lookup, current revision only |
| Pro | $49/mo | 10,000 | Bulk lookup, historical, webhooks for data updates |
| Enterprise | Custom | Unlimited | SLA, dedicated support, on-premise deployment option |

**Design decision trace:** Free tier at 100 req/day because (1) individual tax practitioners typically do 5-20 lookups/day, (2) enough for evaluation, (3) prevents scraping. Pro at $49/mo targets accounting firms and property platforms. Enterprise for banks, Big-4, government agencies.

---

## 6. State Management

### 6.1 Store Design

```typescript
// stores/engineStore.ts (Zustand)

interface EngineStore {
  // Engine lifecycle
  status: EngineStatus;
  worker: Worker | null;
  loadedRegions: Set<number>;
  recordCount: number;
  dataVersion: string;

  // Actions
  initEngine: () => Promise<void>;
  loadRegion: (regionId: number) => Promise<void>;
}

// stores/queryStore.ts (Zustand)

interface QueryStore {
  // Current query state
  cityMunicipality: string;
  barangay: string;
  street: string;
  vicinity: string;
  classification: ClassCode | null;
  propertyType: 'land' | 'condo' | 'parking';
  transactionDate: string;

  // Condo-specific
  condoBuilding: string;
  titleType: 'CCT' | 'TCT' | null;

  // BGC-specific
  floorAreaRatio: number | null;

  // Provincial-specific
  roadProximity: RoadTier | null;

  // Actions
  setField: <K extends keyof QueryStore>(key: K, value: QueryStore[K]) => void;
  resetQuery: () => void;
}

// stores/resultStore.ts (Zustand)

interface ResultStore {
  // Last lookup result
  result: LookupResult | null;
  isLoading: boolean;
  error: string | null;

  // History (local, in-memory only — never sent to server)
  recentLookups: LookupResult[];  // Last 10, for quick re-query

  // Actions
  setResult: (result: LookupResult) => void;
  clearResult: () => void;
}
```

**Privacy note:** `recentLookups` is kept in Zustand (in-memory only), never persisted to localStorage or IndexedDB. When the tab closes, history is gone. This is intentional — we don't store property lookup history on the user's device where it could be inspected by shared-device users.

---

## 7. Performance Targets

| Metric | Target | Basis |
|--------|--------|-------|
| Time to first interactive (NCR) | < 1s on 4G | Phase 1+2: 585 KB brotli at 30 Mbps (Wave 5 wasm-vs-hybrid-tradeoff) |
| Time to full dataset ready | < 5s on 4G | Phase 3: 4.8 MB total brotli background load |
| Lookup latency (user-perceived) | < 100ms | <10ms engine + <50ms Worker postMessage + <40ms React render |
| Repeat visit cold start | < 100ms | Service Worker cache, V8 code caching, zero network |
| API response latency (P50) | < 50ms | In-process engine, no database, no I/O |
| API response latency (P99) | < 200ms | Worst case: full fallback cascade + fuzzy matching |
| Lighthouse Performance score | > 90 | Static assets, minimal JS, WASM in Worker (no main thread blocking) |

---

## 8. Offline & PWA

### 8.1 Service Worker Strategy

```typescript
// sw.ts (Workbox)

import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst } from 'workbox-strategies';

// Precache: app shell (HTML, CSS, JS, engine.wasm)
precacheAndRoute(self.__WB_MANIFEST);

// Data chunks: CacheFirst with content-hash versioning
// Source: Wave 5 data-pipeline-architecture §Stage 6 — content-hash filenames
// for immutable CDN caching
registerRoute(
  ({ url }) => url.pathname.match(/^\/data\/zv-.*\.bin$/),
  new CacheFirst({
    cacheName: 'zv-data-chunks',
    plugins: [
      // No expiration — content-hash versioning handles invalidation
      // Old chunks cleaned up when manifest.json updates
    ],
  })
);

// Manifest: NetworkFirst (short TTL, detects data updates)
registerRoute(
  ({ url }) => url.pathname === '/data/manifest.json',
  new NetworkFirst({
    cacheName: 'zv-manifest',
    networkTimeoutSeconds: 3,
  })
);
```

### 8.2 Update Flow

```
1. User opens app (repeat visit)
2. Service Worker serves cached app shell + data chunks → instant
3. Service Worker fetches manifest.json in background
4. If manifest hash differs → new data available
5. Download changed chunks only (content-hash versioning)
6. Show unobtrusive "Update available — refresh to use latest data" banner
7. On refresh: swap to new chunks, engine re-initializes with fresh data
```

**Design decision trace:** The update flow mirrors Wave 5 data-pipeline-architecture §Stage 6 (Publish): atomic CDN deployment with `manifest.json` (short TTL) pointing to immutable chunk files (infinite TTL). Service Worker + content-hash versioning means the user downloads only the changed Revenue Region chunk when BIR updates a single RDO — typically ~230 KB, not the full 4.8 MB.

---

## 9. Accessibility & Localization

### 9.1 Accessibility

- All form inputs have associated `<label>` elements
- Confidence tiers use color + text + icon (not color alone) — colorblind safe
- Keyboard navigation: Tab through form fields, Enter to submit, Esc to clear
- Screen reader: ARIA live regions for result updates, descriptive aria-labels for confidence badges
- Result card: semantic HTML (`<dl>` for key-value pairs, `<details>` for expandable sections)

### 9.2 Localization (v2)

Initial launch: English only. v2 adds Filipino (Tagalog) and Cebuano.

**Design decision trace:** RealValueMaps' react-i18next integration (Wave 4 realvaluemaps-approach) validates multilingual UX as a pattern worth adopting. Filipino and Cebuano cover >80% of Philippine population. Classification labels and legal metadata remain in English (BIR official language).

---

## 10. TypeScript Type Definitions

Complete TypeScript types mirroring the Rust engine's public API surface:

```typescript
// types/result.ts — mirrors Wave 5 rust-engine-design §2.5

interface LookupResult {
  zonalValue: ZonalValue | null;
  confidence: ConfidenceScore;
  match: MatchDetail;
  classification: ClassificationResult;
  legal: LegalMetadata;
  warnings: Warning[];
}

interface ZonalValue {
  amountPerSqm: number;         // PHP, 2 decimal places
  amountCentavos: number;       // Integer, for exact computation
  currency: 'PHP';
}

interface ConfidenceScore {
  score: number;                 // 0.0–1.0
  tier: 'HIGH' | 'MEDIUM' | 'LOW' | 'VERY_LOW' | 'NO_MATCH';
  breakdown: {
    addressMatch: number;
    classification: number;
    fallbackPenalty: number;
    dataFreshness: number;
    regimePenalty: number;
  };
}

interface MatchDetail {
  mode: 'ncr_cross_street' | 'road_proximity' | 'bgc_far_tier' | 'condo_building';
  streetMethod: 'exact_normalized' | 'alias_resolution' | 'substring_containment'
    | 'token_set_jaccard' | 'fuzzy_jaro_winkler' | 'catch_all' | 'no_match';
  matchedStreet: string | null;
  matchedVicinity: string | null;
  fallbackLevel: number;        // 0–6
  fallbackName: string;
  pipelinePhaseReached: number; // 1–8
}

interface ClassificationResult {
  code: string;                  // "CR", "RR", "A1", etc.
  label: string;                 // "Commercial Regular"
  path: 'single_code' | 'user_selected' | 'condo_ground_floor_cc'
    | 'condo_business_cc' | 'parking_slot_formula'
    | 'institutional_fallback' | 'government_property';
  alternatives: string[];        // Other available codes at this location
}

interface LegalMetadata {
  departmentOrder: string | null;     // "DO 022-2021"
  revision: string | null;            // "7th Revision"
  effectivityDate: string | null;     // ISO date
  rdo: { id: number; name: string; revenueRegion: string } | null;
  regime: 'pre_transition' | 'transition_year_1' | 'post_transition';
  taxBaseFormula: 'three_way_max' | 'two_way_max';
  formulaDescription: string;
}

type Warning = {
  code: 'stale_schedule';
  departmentOrder: string;
  yearsOld: number;
  severity: 'medium';
} | {
  code: 'regime_source_mismatch';
  expectedRegime: string;
  actualSource: string;
  severity: 'high';
} | {
  code: 'multiple_classifications';
  availableCodes: string[];
  severity: 'low';
} | {
  code: 'agricultural_area_threshold';
  severity: 'low';
} | {
  code: 'intra_barangay_split';
  barangay: string;
  rdoA: number;
  rdoB: number;
  severity: 'medium';
} | {
  code: 'no_coverage_barmm';
  municipality: string;
  severity: 'high';
} | {
  code: 'non_standard_code';
  original: string;
  mappedTo: string;
  severity: 'low';
};
```

---

## 11. Design Decision Traceability

| # | Decision | Source | Finding |
|---|----------|--------|---------|
| 1 | City → Barangay cascading dropdowns (not free-text address) | Wave 3 address-matching-algorithms §2 | Engine pipeline requires barangay as structured input; all 7 competitors use this pattern (Wave 4) |
| 2 | Classification dropdown filtered per-location | Wave 2 classification-code-usage | NCR: 7 codes, provincial: 59 codes, RDO 30: 5, RDO 113A: 43 |
| 3 | Transaction date picker (defaults to today) | Wave 1 cta-zonal-rulings | CTA rulings require DO revision effective at transaction date; no competitor supports this (Wave 4 §2.3) |
| 4 | Progressive disclosure (condo/BGC/provincial fields) | Wave 2 address-vicinity-patterns | BGC FAR: 544 records in RDO 44 only; road proximity: provincial only; condo: 9,712 records |
| 5 | 5-tier confidence badge with color + text + icon | Wave 3 address-matching-algorithms | 5-tier model (HIGH ≥0.85, MEDIUM 0.65-0.84, LOW 0.50-0.64, VERY LOW <0.50, NO MATCH 0.0) |
| 6 | Explicit Level 6 NULL result (not error) | Wave 1 cta-zonal-rulings, Wave 3 fallback-hierarchy | CTA Emiliano/Gamboa: BIR cannot substitute arbitrary values; engine returns None |
| 7 | Full confidence breakdown in expandable section | Wave 4 competitive-gap-synthesis §6.1 | Every competitor is a black box; tax practitioners need to justify values used |
| 8 | Web Worker isolation (no SharedArrayBuffer) | Wave 5 wasm-vs-hybrid-tradeoff §2.4 | Privacy: extension content scripts cannot access Worker memory; SAB requires COOP/COEP headers |
| 9 | No street autocomplete from server | Privacy model | Server-side suggestions would reveal data structure; client-side fuzzy matching handles this |
| 10 | recentLookups in-memory only (no persistence) | Privacy model | Property lookup history should not survive tab close on shared devices |
| 11 | API POST /v1/lookup (not GET) | Privacy model | Lookup parameters in URL would appear in server access logs, CDN logs, browser history |
| 12 | PSGC-based location IDs | Wave 4 realvaluemaps-approach, Wave 5 rust-engine-design Decision #10 | Unambiguous canonical location identifier validated by RealValueMaps' design |
| 13 | Content-hash versioned data chunks + Service Worker | Wave 5 data-pipeline-architecture §Stage 6 | Atomic CDN deployment; only changed chunks re-downloaded on BIR updates |
| 14 | Free tier at 100 req/day | Wave 4 competitive-gap-synthesis §4.1 | Individual practitioners: 5-20 lookups/day; prevents scraping; RealValueMaps' freemium validates model |
| 15 | API integer centavos alongside float amount | Wave 5 rust-engine-design Decision #14 | Integer arithmetic avoids floating-point rounding in downstream tax computation |
| 16 | Historical lookup as separate API-only endpoint | Wave 2 data-size-estimation | Historical: ~18 MB brotli, too large for WASM; Wave 5 wasm-vs-hybrid-tradeoff Phase 3 |
| 17 | English-first, Filipino/Cebuano in v2 | Wave 4 realvaluemaps-approach | react-i18next EN/TL/CEB validated as pattern; BIR official language is English |
| 18 | Regime + tax base formula in every API response | Wave 3 rpvara-dual-source-resolution | Downstream tax calculators need regime to select three-way vs two-way max formula |

---

## 12. Open Questions for Implementation

1. **Location search ranking:** Should city/barangay search results be ranked by population, alphabetical, or frequency of tax transactions? Population data available via PSA/PSGC; transaction frequency would require analytics.

2. **Map integration (v2):** Wave 4 validated viewport-based boundary loading and reverse geocoding as input methods (RealValueMaps pattern). Should map be a primary input method or a supplementary visualization? Map adds Leaflet (~40 KB) + barangay GeoJSON (~2-5 MB) to bundle. Likely v2 feature.

3. **Shareable result URLs:** Should results be shareable via URL? If query parameters are in the URL, they appear in browser history and server logs (privacy concern). Could use client-side fragment (#) to keep parameters local. Useful for tax practitioners sharing with colleagues.

4. **Webhook notifications for data updates:** Pro/Enterprise API feature — notify integrators when BIR publishes new DOs. Implementation: compare manifests on pipeline rebuild, emit webhook to registered URLs. Design deferred to API v2.

5. **Embed mode:** Should the engine support iframe embedding for property platforms? Would need postMessage API for cross-origin communication. Potential distribution channel but complicates privacy model.
