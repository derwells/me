# Prior Analysis Import — Annotation and Gap Mapping

**Wave:** 1 — Source Acquisition
**Date:** 2026-03-02
**Aspect:** `prior-analysis-import`
**Source:** `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md` (414 lines, dated 2026-02-26)

---

## Summary

The prior analysis from the PH Tax Computations reverse loop established the foundational 5-step resolution pipeline, 10 complexity drivers, fallback hierarchy, RPVARA transition overview, and third-party platform survey. This import annotates every section of that analysis against the 6 Wave 1 analyses completed in this loop, identifying what has been **confirmed**, **deepened**, **corrected**, or **flagged for deeper investigation** in Waves 2-6.

**Overall assessment:** The prior analysis is structurally sound — no material errors were found. However, Wave 1 has revealed significantly more complexity than anticipated in three areas: (1) workbook format heterogeneity (4+ column patterns, not just "varies slightly"), (2) provincial data structure (multi-municipality hierarchy, road-proximity vicinity model, sitio-level addressing), and (3) the footnote convention reversal between regions. The prior analysis correctly identified the 10 complexity drivers, but underestimated their severity in several cases.

---

## Section-by-Section Annotation

### 1. Resolution Algorithm — Step 1: RDO Jurisdiction Mapping

**Prior claim:** 124 RDOs, static lookup table, automation complexity LOW.

**Status:** CONFIRMED with nuances.

| Finding | Prior Analysis | Wave 1 Status |
|---------|---------------|---------------|
| 124 RDOs nationwide | ✓ Confirmed | Confirmed (RealValueMaps claims 121 — 3 possibly missing) |
| Jurisdiction by property location | ✓ Confirmed | Confirmed by RMC 115-2020 analysis |
| Static table, rarely changes | ✗ Partially incorrect | **RDO boundaries DO shift.** NCR analysis found RR8 split into RR8A/RR8B; South Makati barangays transferred to Taguig per RAO 1-2024. Historical jurisdiction changes affect which RDO workbook to search for older transactions. |
| City-to-RDO is ~124 entries | ✗ Understated | A city may have multiple RDOs (Makati has 4: RDO 47/48/49/50; QC has 4: RDO 28/38/39/40). The mapping is city/district → RDO, not just city → RDO. More like ~200+ entries. |

**Deepened by:** `bir-workbook-ncr-samples.md` (historical RDO reorganization), `bir-workbook-provincial-samples.md` (multi-municipality workbooks)
**Needs further investigation:** Wave 3 `rdo-jurisdiction-mapping` — must formalize the complete city/district/barangay → RDO table with historical changes

---

### 2. Resolution Algorithm — Step 2: Schedule Retrieval & Effectivity Date

**Prior claim:** Each RDO has effectivity dates via DOF DOs; effective 15 days after publication; automation complexity MEDIUM.

**Status:** CONFIRMED and DEEPENED.

| Finding | Prior Analysis | Wave 1 Status |
|---------|---------------|---------------|
| Effectivity from DOF DO | ✓ Confirmed | All 31 workbooks carry DO numbers with effectivity dates |
| 7+ revisions per RDO | ✓ Confirmed | NCR: 6-10 revisions (28-37 years). Provincial: 5-17 revisions (28-35 years). RDO 56 holds record at 17 revisions. |
| 38% outdated | ✓ Confirmed | Confirmed by RPVARA analysis (DOF 2024 data) |
| ZIP files on bir.gov.ph | ✗ Partially superseded | BIR CMS API (`bir-cdn.bir.gov.ph`) provides structured JSON with CDN download URLs. This is more reliable than navigating the website. |

**New findings from Wave 1:**
- **5+ date format variations** in effectivity dates: Excel serial dates, Python datetime objects, text strings in multiple formats (M/D/YYYY, Month D YYYY, abbreviated). Parser must handle all.
- **Multiple DOs per sheet** — RDO 44 (Taguig) contains barangays from two different DOs with different effectivity dates in a single sheet. Effectivity tracking must be per-barangay, not per-sheet.
- **Mixed revision numbers within one DO** — Provincial workbooks (RDO-4) have different municipalities at different revision numbers within the same DO. Revision tracking must be per-municipality.

**Deepened by:** `bir-workbook-ncr-samples.md`, `bir-workbook-provincial-samples.md`
**Needs further investigation:** Wave 2 `sheet-organization` — document the full sheet structure taxonomy

---

### 3. Resolution Algorithm — Step 3: Property Address Matching

**Prior claim:** 4-column Annex C format; matching hierarchy (exact → subdivision → barangay general); automation complexity HIGH.

**Status:** CONFIRMED but SIGNIFICANTLY UNDERESTIMATED in complexity.

| Finding | Prior Analysis | Wave 1 Status |
|---------|---------------|---------------|
| Standard 4-column format | ✓ Confirmed as baseline | 4 columns is the invariant, but **4 distinct column layout patterns** exist (standard 4-col, 5-col split vicinity, 5-col offset gap, 10-col comparison). Plus provincial workbooks embed revision number in ZV column header. |
| Merged cells in barangay groupings | ✗ Understated | Merge counts range from 28 to 3,929 per sheet. RDO-81 (Cebu) has 1.07 merges per row — virtually every data row. Merge severity was far worse than suggested. |
| Vicinity descriptor ambiguity | ✗ Understated — only NCR model described | **Two fundamentally different vicinity models** discovered: NCR cross-street mode ("EDSA to Gil Puyat") vs Provincial road-proximity mode ("ALONG NATIONAL HIGHWAY" / "50 METERS INWARD" / "INTERIOR LOT"). These require separate matching algorithms. |
| Image-based PDFs for some RDOs | ✓ Confirmed | RDO-57 Biñan has a PDF version (1.80 MB) alongside Excel |
| Name variations | ✗ Understated | Also need to handle "SITIO" sub-barangay addressing (unique to provincial), "continuation" barangay blocks, 6+ barangay header variants (NCR) + 6+ provincial variants, numbered barangays (Davao), district hierarchy (Davao). |
| "ALL OTHER STREETS" catch-all | ✓ Confirmed | Universal across both NCR and provincial workbooks. Also confirmed: "ALL OTHER CONDOMINIUMS" catch-all entries. |

**New complexity not in prior analysis:**
1. **Provincial multi-municipality structure** — A single workbook covers up to 16 municipalities with independent header blocks, creating Province → City → Barangay → Street hierarchy (4 levels vs NCR's 3).
2. **Sitio sub-barangay granularity** — Cebu/Laguna/Davao workbooks use SITIO entries below barangay level. Not present in NCR.
3. **Road proximity hierarchy** — Provincial ZVs are tiered by road class: National > Provincial > Municipal > Barangay > 50m inward > Interior > Watershed. This is a different matching dimension than NCR street-specific matching.
4. **Phantom columns** — Workbooks report up to 16,384 columns but use only 4. Parser must detect actual data occupancy.
5. **Multi-row entries** — Street names carry forward across continuation rows (empty col 0 = same street, different classification). Universal pattern.

**Deepened by:** `bir-workbook-ncr-samples.md`, `bir-workbook-provincial-samples.md`
**Needs further investigation:**
- Wave 2 `workbook-column-layouts` — document all column patterns with detection heuristics
- Wave 2 `merged-cell-patterns` — taxonomy of merge patterns
- Wave 2 `address-vicinity-patterns` — pattern catalog for both NCR and provincial modes
- Wave 3 `address-matching-algorithms` — design dual-mode matching strategy

---

### 4. Resolution Algorithm — Step 4: Classification Code Resolution

**Prior claim:** 13 primary + 50 agricultural = 63 codes; predominant use rule; automation complexity PARTIALLY DETERMINISTIC.

**Status:** CONFIRMED and DEEPENED.

| Finding | Prior Analysis | Wave 1 Status |
|---------|---------------|---------------|
| 63 total classification codes | ✓ Confirmed | Annex B analysis confirmed 13 primary + 50 agricultural sub-codes |
| DA (Drying Area) as 13th code | Not mentioned initially | **Confirmed as present in provincial, absent from NCR.** Added to the code list. |
| Agricultural minimum 1,000 sqm | ✓ Confirmed | Not contradicted by any source |
| GP minimum 5,000 sqm | ✓ Confirmed | Confirmed in Annex B analysis |
| Predominant use rule (DOF Reg 1-92) | ✓ Confirmed | CTA rulings analysis confirms narrow scope: "only for areas where properties are NOT YET classified" — published classification prevails (Aquafresh principle) |

**New findings from Wave 1:**
1. **Legacy code meaning changes** — Pre-2019 workbooks used non-standard A-codes. Example: A1 = "Unirrigated Riceland" in 1990 Pangasinan vs A1 = "Riceland Irrigated" in the 2019 standard. The parser must read per-sheet classification legends for historical data.
2. **"A*" placeholder code** — RDO-83 uses `A*` as an unresolved agricultural sub-code placeholder. Must handle as valid but empty.
3. **Agricultural dominance in provincial data** — 20-46% of provincial rows use A1-A50 codes (vs. ~0% in NCR). This was noted but not quantified in the prior analysis.
4. **Aquafresh ruling simplifies engine design** — Published classification is authoritative. Engine does NOT need to determine "actual use." When multiple classifications exist for one street, present all options; user selects. This reduces the non-deterministic gate.

**Deepened by:** `rmo-31-2019-annexes.md`, `cta-zonal-rulings.md`, `bir-workbook-provincial-samples.md`
**Needs further investigation:**
- Wave 2 `classification-code-usage` — map code frequency distribution per RDO
- Wave 3 `classification-resolution-logic` — formalize pseudocode

---

### 5. Resolution Algorithm — Step 5: Value Extraction & Total Computation

**Prior claim:** Trivial arithmetic; condos are per-unit; automation complexity LOW.

**Status:** CONFIRMED with corrections.

| Finding | Prior Analysis | Wave 1 Status |
|---------|---------------|---------------|
| Land: ZV/sqm × area | ✓ Confirmed | No contradictions |
| Condo: per-unit (no multiplication) | ✓ Confirmed | Condo tables organized by building name, tower, floor range. RC/CC/PS entries. |
| PS ~60% of unit value | ✗ Partially corrected | RDO 44 notes state PS = 70% of condo unit ZV. Observed Makati data shows ~60%. Varies by RDO — not a fixed ratio. |

**New findings from Wave 1:**
1. **Non-integer ZVs exist** — Cebu (RDO-81) assigns fractional values (e.g., PHP 28,387.50/sqm). Not a floating-point artifact. Parser must preserve decimals, not blindly round.
2. **Floating-point artifacts also exist** — NCR workbooks have `118999.99999999999` instead of `119000`. These ARE artifacts and should be rounded. Need conditional rounding logic.
3. **BGC FAR-based pricing** — Taguig (RDO-44) uses Floor Area Ratio tiers (FAR 1–18) instead of standard street-vicinity matching. Values range PHP 205,000–2,160,000/sqm. Requires special-cased handling.
4. **"Under construction" condos** — RDO-51 has a dedicated section for condos with assigned ZVs not yet completed.
5. **Ground floor CC rule** — Provincial notes: "Ground floor of residential condominium shall be classified as Commercial (CC)." This is a resolution rule embedded in workbook notes.
6. **RC → CC upgrade rule** — "Any unit in RC project found to be used in business: classified CC with 20% added." Embedded in workbook notes.

**Deepened by:** `bir-workbook-ncr-samples.md`, `bir-workbook-provincial-samples.md`
**Needs further investigation:** Wave 2 `condo-table-structures` — document all condo-specific formats and rules

---

### 6. Fallback Rules (6-Level Hierarchy)

**Prior claim:** 6-level fallback: exact match → barangay general → special use (nearest CR) → LGU FMV markup → written inquiry → zonal classification ruling.

**Status:** CONFIRMED with refinement.

| Finding | Prior Analysis | Wave 1 Status |
|---------|---------------|---------------|
| 6-level hierarchy | ✓ Confirmed | Multiple sources verify. CTA rulings establish legal authority for each level. |
| Levels 1-2 (exact/barangay general) | ✓ Confirmed | "ALL OTHER STREETS" entries confirmed universal. 3 fallback rules embedded in workbooks match levels 1-3. |
| Level 3 (special use → nearest CR) | ✓ Confirmed | Respicio & Co., CTA rulings |
| Level 4 (LGU FMV markup) | ✗ Corrected | Prior analysis said "LGU FMV + 20%". Actual rule is **LGU FMV + 100% (residential/general) or + 150% (commercial/industrial/fishpond)** per RAMO 2-91. Prior analysis elsewhere correctly states these figures but the summary row used "+20%" — an error. |
| Level 5-6 (written inquiry, classification ruling) | ✓ Confirmed | Administrative practices confirmed |

**Critical finding from CTA rulings (new):**
- **Fallback must return NULL, not interpolation.** CTA cases (Emiliano, Gamboa) establish that the BIR cannot substitute arbitrary valuations when no published ZV exists. The engine must surface "no published zonal value" explicitly — this is legally meaningful and triggers a different administrative pathway.
- **Three simpler rules embedded in workbooks** — Adjacent barangay of similar conditions (Rule 1), similarly situated property in adjacent barangay (Rule 2), nearest street of similar conditions in same barangay (Rule 3). These are the workbook-codified subset of the 6-level hierarchy.

**Deepened by:** `cta-zonal-rulings.md`, `rmo-31-2019-annexes.md`
**Needs further investigation:** Wave 3 `fallback-hierarchy-implementation` — implement with worked examples from actual data

---

### 7. RPVARA Transition (RA 12001)

**Prior claim:** BIR → BLGF authority transfer; three-way max → two-way max; 2-year transition; 6% RPT cap; dual-source needed.

**Status:** CONFIRMED and SUBSTANTIALLY DEEPENED.

The prior analysis covered this in ~30 lines. The Wave 1 `rpvara-transition-mechanics.md` analysis expanded it to 320 lines with:

| New Depth Added | Details |
|-----------------|---------|
| **Section 29(b) full text** | Interim rule: max(SP, ZV, existing_SMV) — three-way max continues during transition |
| **Section 31 saving clause** | BIR ZVs don't expire automatically; continue until replaced per-jurisdiction |
| **Three regimes per property** | Pre-transition, transition year 1 (6% cap), post-transition — engine must detect per-jurisdiction |
| **Realistic timeline assessment** | 37-42% LGU compliance rate historically; July 2026 deadline unlikely for most LGUs; dual-source extends to 2028+ |
| **SMV format unknown** | Column layout, classification codes, and publication format for BLGF SMVs not yet specified |
| **RPIS system** | Centralized database mandated but not yet operational; potential future API source |
| **Tax-type impact matrix** | Detailed CGT, DST, donor's tax, estate tax, VAT, RPT impact mapped across all 3 regimes |
| **7 key uncertainties** | SMV format, PVS classification codes, BIR operational guidance, RPIS specs, LGU compliance pace, pending BIR revisions, condo valuation under new system |

**Prior analysis was correct but shallow.** The RPVARA transition is more complex than initially characterized, especially the dual-source detection problem (per-jurisdiction, not nationwide).

**Deepened by:** `rpvara-transition-mechanics.md`
**Needs further investigation:** Wave 3 `rpvara-dual-source-resolution` — design the detection/switching mechanism

---

### 8. RMC 115-2020 — Certification Procedure

**Prior claim:** Certification no longer required for ONETT; BIR treats published schedules as authoritative.

**Status:** CONFIRMED. No corrections needed.

Wave 1 analysis confirmed all provisions. The key implication stands: the same data the BIR uses is publicly downloadable, supporting automated resolution.

---

### 9. Third-Party Data Sources

**Prior claim:** 6 platforms surveyed; no public API; Housal 1.96M, ZonalValueFinderPH ~30K.

**Status:** CONFIRMED and DEEPENED.

The prior analysis covered 6 platforms in a summary table (~15 lines). Wave 1 `third-party-platform-survey.md` expanded to 578 lines covering 7 platforms:

| Improvement | Details |
|-------------|---------|
| **+1 platform** | FileDocsPhil added (sells BIR Excel files for ₱560) |
| **REN.PH deep dive** | Next.js + Supabase; 336K records; named operator (Aaron Zara, PRC #0025157); RDO tracking per record; current-revision-only → useful WASM bundling benchmark |
| **Housal business intel** | $1.8M revenue, 20 team, $1M funding (Brook Capital), DO# per record |
| **RealValueMaps** | 2.7M records, 42K barangays, 121/124 RDOs, anonymous operator |
| **8 competitive gaps** | No API, no address matching with fallback, no effectivity dates, primitive classification filtering, unverifiable freshness, all server-side (privacy gap), zero RPVARA readiness, REN.PH 336K current-only benchmark |
| **Record count reconciliation** | REN.PH 336K ≈ current-only; Housal 1.96M ≈ including historical; our estimate ~690K current across 124 RDOs |
| **Technology comparison** | Stack analysis for each platform |

**Deepened by:** `third-party-platform-survey.md`
**Needs further investigation:**
- Wave 4 `housal-data-model` — reverse-engineer their 1.96M record structure
- Wave 4 `realvaluemaps-approach` — validate 2.7M claim, check for GIS integration
- Wave 4 `competitive-gap-synthesis` — define the opportunity

---

### 10. Edge Cases

**Prior claim:** Condos (per-unit), multiple classifications per street, "along [Street]" vs interior, stale schedules, installment timing.

**Status:** CONFIRMED with many additions.

| Edge Case | Prior Status | Wave 1 Additions |
|-----------|-------------|------------------|
| Condo per-unit | ✓ Confirmed | + BGC FAR-based pricing, "under construction" section, ground floor CC rule, RC→CC 20% upgrade rule |
| Multiple classifications per street | ✓ Confirmed | Universal pattern; multi-row entries with empty col 0 = continuation |
| "Along [Street]" vs interior | ✓ Confirmed (NCR) | Provincial equivalent: road proximity hierarchy (7 tiers from national highway to watershed) |
| Stale schedules | ✓ Confirmed | CTA confirms existing values remain in force until revised |
| Installment timing (OT-028-2024) | ✓ Confirmed | No contradicting sources |

**New edge cases discovered in Wave 1:**
1. **Footnote convention reversal** — `*` means "newly identified" in Pangasinan/Laguna but "deleted/removed" in NCR/Cebu. Per-region configuration required.
2. **Non-integer ZVs** — Cebu has legitimate fractional values (PHP 28,387.50); NCR has floating-point artifacts to round. Conditional rounding.
3. **Zero-value entries** — Indicate pending TCRPV assignment (RDO 47: AYALA AVENUE* with ZV=0). Not actual zeros.
4. **Jurisdiction annotations** — Streets with ZV=0 and footnote "not within the barangay's jurisdiction" (RDO 41).
5. **"(NEW)" vicinity marker** — Functions as both footnote and vicinity modifier (RDO-57).
6. **"A*" unresolved code** — Agricultural placeholder never assigned a specific sub-code (RDO-83).
7. **Barangay continuation blocks** — Provincial workbooks re-insert header blocks mid-barangay across page breaks.
8. **Numbered barangays** — Davao uses "BARANGAY NO. 1" through "NO. 80+" instead of names.

**Deepened by:** All Wave 1 analyses
**Needs further investigation:**
- Wave 2 `footnote-convention-mapping` — map per-region conventions
- Wave 2 `condo-table-structures` — document all condo edge cases
- Wave 2 `address-vicinity-patterns` — catalog all pattern types

---

### 11. Complexity Drivers (10 total)

The prior analysis identified 10 complexity drivers. Wave 1 has re-assessed each:

| # | Driver | Prior Severity | Wave 1 Revised Severity | Notes |
|---|--------|---------------|------------------------|-------|
| 1 | 124 heterogeneous workbooks | HIGH | **EXTREME** | 4+ column patterns, 6+ barangay header variants, 5+ date formats, up to 3,929 merged ranges per sheet. Far worse than "slightly different." |
| 2 | Address matching ambiguity | HIGH | **EXTREME** | Two fundamentally different matching models (NCR cross-street vs provincial road-proximity). Plus sitio addressing, numbered barangays, continuation blocks. |
| 3 | No API (data acquisition) | MEDIUM | MEDIUM (reduced) | BIR CMS API provides structured JSON with CDN URLs. Not a public lookup API, but significantly improves acquisition over manual ZIP downloading. |
| 4 | Image-based PDFs (some RDOs) | MEDIUM | LOW-MEDIUM | Only 2 confirmed PDF files across 31 sampled workbooks. Most data is in parseable Excel format. |
| 5 | Update monitoring (124 RDOs) | MEDIUM | MEDIUM | Confirmed: no central notification. BIR CMS API could be polled for changes. |
| 6 | RPVARA dual-source transition | MEDIUM | **HIGH** | Per-jurisdiction regime detection needed. 7 key format/classification unknowns. Dual-source period extends to 2028+. |
| 7 | Classification judgment | MEDIUM | LOW-MEDIUM (reduced) | Aquafresh ruling simplifies: published classification is authoritative. Non-deterministic gate is narrower than estimated — only when user must choose among listed classifications. |
| 8 | Condo vs. land bifurcation | MEDIUM | **HIGH** | BGC FAR-based pricing, "under construction" condos, ground floor CC rule, RC→CC 20% upgrade rule, PS ratio variation. More edge cases than expected. |
| 9 | Fallback rule chain | MEDIUM | MEDIUM | 6-level hierarchy confirmed. CTA adds: MUST return NULL not interpolation when no value exists. Legally grounded. |
| 10 | Stale data management | MEDIUM | MEDIUM | Confirmed 38% outdated. Schedule vintage is legally material per CTA rulings. |

**New complexity drivers discovered (not in prior analysis):**

| # | Driver | Severity | Description |
|---|--------|----------|-------------|
| 11 | **Footnote convention reversal** | MEDIUM | `*` marker meaning varies by region. Per-workbook or per-Revenue-Region configuration needed. |
| 12 | **Provincial multi-municipality workbooks** | HIGH | Single workbook covers up to 16 municipalities with Province → City → Barangay → Street hierarchy. Parser must track municipality context transitions. |
| 13 | **Legacy classification code mapping** | MEDIUM | Pre-2019 A-codes had different meanings. Historical revision parsing requires per-sheet legend reading. |
| 14 | **ZV value type heterogeneity** | LOW-MEDIUM | Non-integer legitimate values (Cebu) vs floating-point artifacts (NCR). PHP 25 to PHP 2,160,000 range (200,000x). |

---

### 12. Data Dependencies

Prior analysis table mapped 5 dependencies with automation feasibility. Wave 1 revisions:

| Dependency | Prior Feasibility | Revised Feasibility | Revision Rationale |
|-----------|------------------|--------------------|--------------------|
| RDO jurisdiction table | HIGH | HIGH (but larger than expected) | ~200+ entries, not ~124. District-level granularity needed. Historical changes exist. |
| Zonal value schedule (Excel) | MEDIUM | MEDIUM-HIGH (improved) | BIR CMS API helps acquisition. But format heterogeneity is worse than expected. |
| Address normalization | LOW-MEDIUM | LOW | Two matching models needed (NCR + provincial). Sitio addressing. Numbered barangays. |
| Classification code | MEDIUM | MEDIUM-HIGH (simplified) | Aquafresh ruling makes published classification authoritative. Non-deterministic gate narrower. |
| Effectivity date tracking | MEDIUM | MEDIUM | Per-barangay tracking needed (not per-sheet). BIR CMS API could help. |

---

### 13. Verification Summary

The prior analysis's verification table (15 claims checked against 10+ sources) holds up entirely. No material conflicts. The one correction (ECRPV committee level) was already documented. Wave 1 has independently confirmed all key claims through actual workbook inspection and legal source analysis.

---

## Gap Map: What This Loop Must Deepen

### Gaps in the Prior Analysis That Wave 1 Has Not Yet Addressed

| Gap | Priority | Target Wave/Aspect |
|-----|----------|-------------------|
| Complete RDO jurisdiction mapping table | HIGH | Wave 3: `rdo-jurisdiction-mapping` |
| Address matching algorithm design (dual-mode) | CRITICAL | Wave 3: `address-matching-algorithms` |
| Fallback hierarchy worked examples with real data | HIGH | Wave 3: `fallback-hierarchy-implementation` |
| RPVARA dual-source detection mechanism | HIGH | Wave 3: `rpvara-dual-source-resolution` |
| Housal/RealValueMaps data model reverse-engineering | MEDIUM | Wave 4: `housal-data-model`, `realvaluemaps-approach` |
| Competitive gap synthesis for API-first approach | MEDIUM | Wave 4: `competitive-gap-synthesis` |

### New Aspects Discovered by Wave 1 That Were Not in the Prior Analysis

| New Aspect | Added To | Wave | Priority |
|-----------|---------|------|----------|
| Footnote convention mapping | `footnote-convention-mapping` | 2 | HIGH |
| BGC FAR-based pricing | Covered in `condo-table-structures` | 2 | MEDIUM |
| Provincial road-proximity matching | Covered in `address-vicinity-patterns` | 2 | HIGH |
| Sitio sub-barangay addressing | Covered in `address-matching-algorithms` | 3 | MEDIUM |
| Legacy classification code evolution | Covered in `classification-code-usage` | 2 | MEDIUM |
| Under-construction condo handling | Covered in `condo-table-structures` | 2 | LOW |

### Data Size Estimates for Architecture (Wave 5 Input)

| Metric | Prior Estimate | Wave 1 Estimate | Source |
|--------|---------------|-----------------|--------|
| Total current-revision rows | Not estimated | ~690,000 | `bir-workbook-provincial-samples.md` extrapolation |
| NCR rows (current) | Not estimated | ~35,000-40,000 | `bir-workbook-ncr-samples.md` (24 RDOs) |
| Provincial rows (current) | Not estimated | ~650,000 | Extrapolated from 7 RDOs × ~100 provincial RDOs |
| ZV range | Not estimated | PHP 25 – 2,160,000/sqm | Full workbook analysis |
| Housal records (incl. historical) | 1,961,265 | ✓ Confirmed | Platform survey |
| REN.PH records (current only) | Not available | 336,792 | Platform survey — benchmark for WASM |

---

## Conclusions

1. **The prior analysis is a solid foundation.** No structural changes needed to the 5-step resolution pipeline. The complexity drivers are correct, with 4 additional drivers identified.

2. **Severity was underestimated.** Format heterogeneity (driver #1) and address matching (driver #2) are EXTREME, not just HIGH. The provincial data model adds a hierarchy level, a completely different vicinity model, and sub-barangay addressing.

3. **Legal analysis was strengthened.** CTA rulings (Aquafresh, Emiliano, Gamboa) provide concrete resolution rules that simplify some aspects (classification is from published schedule) while constraining others (fallback must return NULL, not interpolation).

4. **RPVARA is more complex than characterized.** Per-jurisdiction regime detection, 7 format unknowns, dual-source period extending to 2028+ — the prior analysis's brief section is now a 320-line deep dive.

5. **Data size is tractable for WASM.** ~690K current-revision rows is far smaller than the 1.96M/2.7M third-party counts (which include historical). REN.PH's 336K current-only count suggests that with good normalization, the dataset may fit in a WASM bundle.

6. **The competitive gap is wider than stated.** Eight specific gaps identified across all 7 platforms. No API, no address matching, no effectivity tracking, no fallback logic, no privacy model, no RPVARA readiness. The engineering moat is real.

---

## Sources

- Prior analysis: `../reverse-ph-tax-computations/analysis/zonal-value-lookup.md` (414 lines)
- Wave 1 analyses (this loop): `bir-workbook-ncr-samples.md`, `bir-workbook-provincial-samples.md`, `rmo-31-2019-annexes.md`, `rpvara-transition-mechanics.md`, `cta-zonal-rulings.md`, `third-party-platform-survey.md`
