# Catalog Self-Review — Completeness, Actionability, and Scoring Correctness

**Wave:** 4 (Scoring & Synthesis)
**Aspect:** catalog-review
**Date:** 2026-02-27
**Method:** Systematic cross-check of `output/opportunity-catalog.md` against all Wave 2–3 analysis files, existing-tools-survey coverage matrix, practitioner-workflow lifecycle analysis, complexity-scoring dimensions, and the now-available `loops/reverse-ph-tax-computations/output/opportunity-catalog.md`.

---

## 1. Completeness Check

### 1.1 All 16 Wave 2 Computations Present?

**PASS.** All 16 computations from Wave 2 are present in the catalog with full entries:

| # | Computation | Entry Present | Inputs/Outputs | Legal Basis | Current State | Complexity | Competitive Gap | Score | Tax Cross-Ref |
|---|------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | assessment-level-lookup | Y | Y | Y | Y | Y | Y | Y | Y |
| 2 | socialized-housing-compliance | Y | Y | Y | Y | Y | Y | Y | Y |
| 3 | condo-association-dues | Y | Y | Y | Y | Y | Y | Y | Y |
| 4 | bp220-lot-compliance | Y | Y | Y | Y | Y | Y | Y | Y |
| 5 | improvement-depreciation | Y | Y | Y | Y | Y | Y | Y | Y |
| 6 | developer-equity-schedule | Y | Y | Y | Y | Y | Y | Y | Y |
| 7 | rent-increase-computation | Y | Y | Y | Y | Y | Y | Y | Y |
| 8 | notarial-fees | Y | Y | Y | Y | Y | Y | Y | Y |
| 9 | pagibig-amortization | Y | Y | Y | Y | Y | Y | Y | Y |
| 10 | broker-commission | Y | Y | Y | Y | Y | Y | Y | Y |
| 11 | ltv-ratio | Y | Y | Y | Y | Y | Y | Y | Y |
| 12 | bank-mortgage-amortization | Y | Y | Y | Y | Y | Y | Y | Y |
| 13 | maceda-refund | Y | Y | Y | Y | Y | Y | Y | Y |
| 14 | pagibig-loan-eligibility | Y | Y | Y | Y | Y | Y | Y | Y |
| 15 | rod-registration-fees | Y | Y | Y | Y | Y | Y | Y | Y |
| 16 | condo-common-area-pct | Y | Y | Y | Y | Y | Y | Y | Y |

### 1.2 Missing Computations — Scope Boundary Review

Checked the PROMPT.md scope definition against delivered computations:

**Primary — Financing & Amortization (5 items):** All covered (pagibig-loan-eligibility, pagibig-amortization, bank-mortgage-amortization, developer-equity-schedule, ltv-ratio).

**Primary — Regulatory Compliance (5 items):** All covered (maceda-refund, socialized-housing-compliance, rent-increase-computation, bp220-lot-compliance, condo-common-area-pct).

**Primary — Valuation & Assessment (3 items):** All covered (assessment-level-lookup, improvement-depreciation). FMV estimation formulas were in scope but not extracted as a separate computation — covered implicitly via the BUCC pipeline in improvement-depreciation and the "higher value rule" in assessment-level-lookup. The income approach capitalization rate (mentioned in scope as "fair market value estimation formulas") is **non-deterministic** (requires judgment on cap rate selection) and was correctly excluded.

**Secondary — Fees & Dues (4 items):** All covered (rod-registration-fees, notarial-fees, broker-commission, condo-association-dues).

**Emergent discoveries during analysis:** condo-association-dues was discovered during Wave 1 analysis of condo-act-common-areas. Correctly added to Wave 2 frontier and fully analyzed.

**Potential gap:** Comparable sales analysis (per-sqm pricing by location) was mentioned in scope under "fair market value estimation formulas." This is fundamentally non-deterministic (requires market data and judgment) and correctly excluded. No action needed.

**Verdict: COMPLETE.** All scoped deterministic computations are present. Non-deterministic items correctly excluded.

---

## 2. Scoring Correctness

### 2.1 Automation Gap (A) Cross-Check

Verified each A score against the existing-tools-survey coverage matrix:

| Computation | Tools Survey Coverage | A Score | Expected (rubric) | Match? |
|------------|----------------------|:-------:|:------------------:|:------:|
| assessment-level-lookup | POOR (simplified RPT tools) | 4 | 4 (POOR → 4) | Y |
| socialized-housing-compliance | ZERO | 5 | 5 | Y |
| condo-association-dues | ZERO | 5 | 5 | Y |
| bp220-lot-compliance | ZERO | 5 | 5 | Y |
| improvement-depreciation | ZERO | 5 | 5 | Y |
| developer-equity-schedule | POOR (ForeclosurePH partial CTS) | 4 | 4 | Y |
| rent-increase-computation | ZERO | 5 | 5 | Y |
| notarial-fees | ZERO | 5 | 5 | Y |
| pagibig-amortization | PARTIAL (basic covered, MRI/FGI missing) | 3 | 3 | Y |
| broker-commission | PARTIAL (iRealtee SaaS-locked) | 3 | 3 | Y |
| ltv-ratio | POOR (generic LTV only) | 4 | 4 | Y |
| bank-mortgage-amortization | GOOD (11+ tools, basic) | 2 | 2 | Y |
| maceda-refund | ZERO | 5 | 5 | Y |
| pagibig-loan-eligibility | GOOD (official tool) | 2 | 2 | Y |
| rod-registration-fees | GOOD (LRA ERCF official) | 2 | 2 | Y |
| condo-common-area-pct | ZERO | 5 | 5 | Y |

**RESULT: 16/16 consistent.** All A scores match the tools survey evidence per the rubric.

### 2.2 Market Frequency (F) Cross-Check

Verified against practitioner-workflow lifecycle analysis and transaction volume estimates:

| Computation | Lifecycle Stage(s) | Volume Basis | F Score | Reasonable? |
|------------|-------------------|-------------|:-------:|:-----------:|
| assessment-level-lookup | Annual RPT, every property | All properties nationwide | 5 | Y |
| socialized-housing-compliance | Stage 1 (project filing) | Every socialized project | 4 | Y — per-project not per-unit |
| condo-association-dues | Stage 6 (monthly) | Every condo unit monthly | 4 | Y |
| bp220-lot-compliance | Stage 1 (project filing) | Per socialized project | 3 | Y — per-project, hundreds/yr |
| improvement-depreciation | Assessment pipeline | Every improved property | 3 | Y — assessor workflow |
| developer-equity-schedule | Stage 1 (every buyer) | Every buyer interaction | 5 | Y — highest frequency |
| rent-increase-computation | Annual, all rentals | Every rental unit/year | 4 | Y — rental segment only |
| notarial-fees | Every transaction | Universal | 5 | Y |
| pagibig-amortization | Stage 4 (loan processing) | Every Pag-IBIG loan | 5 | Y |
| broker-commission | Stage 1 (pre-sale) | Every brokered deal | 5 | Y |
| ltv-ratio | Stage 4 (loan processing) | Every financed purchase | 4 | Y |
| bank-mortgage-amortization | Stages 1, 4, 6 | Every bank-financed purchase | 5 | Y |
| maceda-refund | Stage 3 (defaults) | Defaults only, subset | 3 | Y |
| pagibig-loan-eligibility | Stage 1, 4 | Every Pag-IBIG applicant | 5 | Y |
| rod-registration-fees | Stage 5 (closing) | Every property transfer | 5 | Y |
| condo-common-area-pct | One-time per project | Per condo project at inception | 2 | Y |

**RESULT: 16/16 reasonable.** No F scores appear miscalibrated relative to volume evidence.

### 2.3 Moat Defensibility (M) Cross-Check

Verified against complexity-scoring dimensions and data acquisition barriers:

| Computation | Complexity Score | Key Moat Drivers | M Score | Reasonable? |
|------------|:---------------:|-----------------|:-------:|:-----------:|
| assessment-level-lookup | 17 (highest) | 1,488+ LGU database, RA 12001 | 5 | Y |
| socialized-housing-compliance | 11 | JMC ceiling + zonal + 6 modes | 4 | Y |
| condo-association-dues | 15 | Per-corp data + multi-regulation | 4 | Y |
| bp220-lot-compliance | 14 | 15 decision points + JMC layering | 5 | Y |
| improvement-depreciation | 14 | LGU BUCC + depreciation tables | 5 | Y |
| developer-equity-schedule | 14 | Per-developer data, accessible | 3 | Y |
| rent-increase-computation | 11 | NHSB history compilation | 3 | Y |
| notarial-fees | 12 | Trivial deterministic portions | 2 | Y |
| pagibig-amortization | 10 | MRI/FGI data gap (2014-2018) | 3 | Y |
| broker-commission | 15 | Multi-tier + EWT tracking | 3 | Y |
| ltv-ratio | 10 | Well-documented, stable | 2 | Y |
| bank-mortgage-amortization | 14 | Multi-bank rate database | 3 | Y |
| maceda-refund | 6 (lowest) | Simple formula, SC edge cases | 2 | Y |
| pagibig-loan-eligibility | 12 | Official tool exists | 2 | Y |
| rod-registration-fees | 12 | National table, straightforward | 2 | Y |
| condo-common-area-pct | 10 | Master-deed dependent | 2 | Y |

**RESULT: 16/16 reasonable.** Moat scores appropriately correlate with complexity and data barriers. Note: high complexity does not always mean high moat (broker-commission has complexity 15 but M:3 because data is accessible) — this is correctly handled.

### 2.4 Composite Score Arithmetic

Verified all 16 multiplications:

| Computation | A | F | M | Claimed | Calculated | Match? |
|------------|:-:|:-:|:-:|:-------:|:----------:|:------:|
| assessment-level-lookup | 4 | 5 | 5 | 100 | 100 | Y |
| socialized-housing-compliance | 5 | 4 | 4 | 80 | 80 | Y |
| condo-association-dues | 5 | 4 | 4 | 80 | 80 | Y |
| bp220-lot-compliance | 5 | 3 | 5 | 75 | 75 | Y |
| improvement-depreciation | 5 | 3 | 5 | 75 | 75 | Y |
| developer-equity-schedule | 4 | 5 | 3 | 60 | 60 | Y |
| rent-increase-computation | 5 | 4 | 3 | 60 | 60 | Y |
| notarial-fees | 5 | 5 | 2 | 50 | 50 | Y |
| pagibig-amortization | 3 | 5 | 3 | 45 | 45 | Y |
| broker-commission | 3 | 5 | 3 | 45 | 45 | Y |
| ltv-ratio | 4 | 4 | 2 | 32 | 32 | Y |
| bank-mortgage-amortization | 2 | 5 | 3 | 30 | 30 | Y |
| maceda-refund | 5 | 3 | 2 | 30 | 30 | Y |
| pagibig-loan-eligibility | 2 | 5 | 2 | 20 | 20 | Y |
| rod-registration-fees | 2 | 5 | 2 | 20 | 20 | Y |
| condo-common-area-pct | 5 | 2 | 2 | 20 | 20 | Y |

**RESULT: 16/16 arithmetic confirmed.** No calculation errors.

---

## 3. Actionability Assessment

### 3.1 Can Each Entry Support a Deep-Dive Decision?

For each catalog entry, verified: (a) inputs/outputs are typed and enumerated, (b) legal basis has specific section/circular numbers, (c) competitive gap identifies what to build that doesn't exist, (d) moat analysis explains defensibility rationale.

**PASS for all 16.** Every entry provides sufficient detail to decide whether to launch a dedicated deep-dive loop. The recommended deep-dive loops table (6 entries) directly maps from the scored catalog.

### 3.2 Strategic Recommendations Clarity

- **Three build strategies** (quick wins / high-frequency engines / infrastructure plays): Clear, actionable, with specific computation assignments.
- **Shared data layer table**: 6 layers with composite point totals and cross-loop references. All arithmetic verified correct.
- **Deep-dive loop recommendations**: 6 prioritized loops with computation bundles and rationale. Priorities logically follow from scores.
- **Ecosystem gap visualization**: ASCII bar chart provides quick visual summary.

**One weakness:** The "Three Build Strategies" table doesn't include explicit time-to-value estimates (just "Weeks" / "1-2 months" / "3-6 months"). These are rough heuristics, not evidence-based. This is acceptable for a survey-level catalog but should be flagged as estimates.

### 3.3 Missing Actionability Elements

**MINOR GAPS:**
1. No explicit "next steps" or decision framework for choosing between strategies. The reader must synthesize from the strategic analysis section.
2. No market size estimates (TAM/SAM). Transaction volumes are described qualitatively (e.g., "millions of rental units") but not quantified. This is appropriate for a computation survey but limits business case construction.
3. No technology stack recommendations. The catalog is technology-agnostic by design, which is correct for a survey-level output.

---

## 4. Tax Loop Cross-Reference Reconciliation

**UPDATE: The `loops/reverse-ph-tax-computations/output/opportunity-catalog.md` now exists** (dated 2026-02-26, self-reviewed). The catalog's statement that "ph-tax-computations-reverse catalog not yet produced" is now **stale**.

### 4.1 Cross-Reference Validation

Checked all 8 bridge points claimed in the catalog against the tax loop catalog:

| This Loop | Tax Loop Entry | Claimed Connection | Verified? |
|-----------|---------------|-------------------|:---------:|
| assessment-level-lookup (100) | RPT Computation (125) | Determines RPT tax base | **CONFIRMED** — tax loop's RPT entry explicitly requires assessment levels from LGC §218. Deeply interlinked: assessment-level-lookup IS a sub-computation of RPT. Both loops identify LGU database as dominant moat. |
| rod-registration-fees (20) | Highest-of-Three Base (40), CGT (45), Transfer Tax (60) | "Higher value rule" determines tax bases | **CONFIRMED** — tax loop identifies `max(GSP, ZV, AFMV)` as shared tax base computation. |
| broker-commission (45) | CWT Rate and Timing (60) | EWT on commission | **CONFIRMED** — tax loop's CWT entry covers EWT rates (1.5/3/5/6%) per RR 11-2018. Our broker-commission analysis has the correct post-TRAIN individual broker rates (5%/10% at ₱3M). Different rate tiers apply to brokers (individual) vs. property sellers (habitually engaged) — NOT a conflict, different taxpayer categories. |
| condo-association-dues (80) | N/A (dues exempt) | SC GR 215801 — IT/VAT/WT exempt | **CONFIRMED** — tax loop does not have a separate entry for condo dues taxation because SC settled this as exempt. |
| socialized-housing-compliance (80) | VAT on Real Property (64) | VAT exemption under NIRC §109(P) | **CONFIRMED** — tax loop's VAT entry lists socialized housing exemption as a decision gate. |
| developer-equity-schedule (60) | VAT on Real Property (64) | VAT on TCP above ₱3.6M | **CONFIRMED** — tax loop confirms ₱3.6M threshold per RR 1-2024. |
| notarial-fees (50) | VAT on Real Property (64) | VAT on notarial services >₱3M | **CONFIRMED** — indirect: if notary exceeds ₱3M annual gross. |
| rent-increase-computation (60) | CWT Rate and Timing (60) | CWT 5% on rent | **CONFIRMED** — tax loop covers CWT rates including rental income withholding. |

**RESULT: 8/8 bridge points verified.** All cross-references are accurate.

### 4.2 Key Shared Data Assets — Cross-Loop View

| Data Asset | This Loop's Composite Points | Tax Loop's Composite Points | Combined |
|-----------|:---------------------------:|:--------------------------:|:--------:|
| BIR zonal values | 200 (assessment + socialized + ROD) | 125+ (ZV lookup is #1 at 125, feeds CGT/DST/CWT/VAT/transfer tax) | **325+** |
| LGU assessment database | 175 (assessment + depreciation) | 125 (RPT is co-#1 at 125) + 60 (transfer tax shares LGU rate DB) | **360+** |
| EWT/VAT thresholds | 175 (broker + condo dues + notarial) | 64+ (VAT) + 60 (CWT) | **299+** |

**BIR zonal values and LGU assessment database are confirmed as the highest-leverage cross-loop shared data assets**, supporting >300 composite points each across both catalogs.

### 4.3 Overlap Between assessment-level-lookup and RPT Computation

This loop's #1 entry (assessment-level-lookup, score 100) and the tax loop's co-#1 entry (RPT Computation, score 125) are deeply interlinked. Assessment level is a sub-computation within the RPT pipeline:

```
FMV → Assessment Level Lookup → Assessed Value → RPT Rate Application → Tax Due
 ↑ this loop covers ↑                              ↑ tax loop covers ↑
```

This is not a conflict — the boundary is clean. Assessment level determination (classification, §218 bracket lookup, AV calculation) is a non-tax valuation computation. RPT rate application, SEF, idle land levy, and penalty computation are tax computations. Both need the same LGU data layer.

**Recommendation:** A deep-dive loop for "PH Property Assessment Engine" should explicitly coordinate with the tax loop's RPT scope to avoid duplication.

---

## 5. Issues Found and Corrections Required

### 5.1 STALE CLAIM — Tax Loop Catalog Status

**Location:** Catalog introduction (line 6) and cross-reference section (line 431)

**Issue:** The catalog states "catalog not yet produced" for the tax loop, but `loops/reverse-ph-tax-computations/output/opportunity-catalog.md` now exists (dated 2026-02-26).

**Action:** Update the catalog to reference the now-available tax loop catalog and note key reconciliation findings.

**Severity:** LOW — factual staleness, not a scoring or analysis error. The cross-reference table itself was accurate even before the tax catalog was produced (it used legal/regulatory connections, not catalog-specific data).

### 5.2 MINOR — Tools Survey Count Discrepancy

**Location:** Catalog summary says "34 tools surveyed" but the updated existing-tools-survey analysis header says "50+ tools identified across 7 categories."

**Explanation:** The tools survey was expanded after the initial count. The original 34 count (from the analysis-log entry) refers to the initial survey scope. The expanded survey found 50+ tools but only 34 had substantive coverage worth detailed analysis.

**Action:** No change needed — the catalog's claims about coverage levels are based on the full expanded survey. The "34" figure in some places could be updated to "50+" for consistency but does not affect any scoring.

**Severity:** COSMETIC.

### 5.3 MINOR — Time-to-Value Estimates

**Location:** Strategic Analysis → Three Build Strategies table

**Issue:** "Weeks" / "1-2 months" / "3-6 months" estimates are heuristic, not evidence-based. No methodology for these estimates is documented.

**Action:** No change needed for the catalog, but flag that these are rough heuristics for the deep-dive loop consumers.

**Severity:** LOW — appropriate for survey-level output.

### 5.4 OBSERVATION — Notarial Fees Scoring Nuance

**Location:** Entry #8 (notarial-fees), score A:5 × F:5 × M:2 = 50

**Observation:** The A:5 score (zero tools) is technically correct but the entry's own text acknowledges that only 2 of 5 sub-computations are fully deterministic. The effective automation opportunity is narrower than the headline A:5 suggests. The opportunity-scoring analysis file has a clear caveat ("this score requires context") — this caveat should ideally be more prominent in the catalog entry itself.

**Action:** The catalog entry already includes the qualifying text. No scoring change needed — the rubric measures tool coverage, not determinism. The M:2 score already penalizes for low moat, and the entry explicitly notes it's "best positioned as a closing cost aggregation component, not standalone."

**Severity:** NONE — correctly handled.

---

## 6. Overall Assessment

### Verdict: CATALOG IS COMPLETE, ACTIONABLE, AND CORRECTLY SCORED

| Dimension | Status | Notes |
|-----------|--------|-------|
| Completeness | **PASS** | All 16 scoped computations present. Non-deterministic items correctly excluded. Emergent discovery (condo-association-dues) captured. |
| Scoring correctness | **PASS** | 16/16 A scores match tools survey. 16/16 F scores match workflow analysis. 16/16 M scores match complexity/data barriers. 16/16 arithmetic verified. |
| Internal consistency | **PASS** | Tier assignments match composite scores. Rankings are monotonic. Cross-references between sections are consistent. |
| Actionability | **PASS** | Each entry has typed inputs/outputs, specific legal citations, competitive gap analysis, and scored recommendation. Deep-dive loop table provides clear prioritization. |
| Tax loop cross-reference | **PASS with update needed** | All 8 bridge points verified against now-available tax loop catalog. Shared data assets confirmed. One stale claim needs updating. |
| Strategic analysis | **PASS** | Three strategies, six data layers, six deep-dive recommendations all logically follow from scoring. Moat-gap matrix insight ("no defended-but-covered quadrant") is novel and actionable. |

### Key Strengths
1. **Verification depth:** Every Wave 2 computation was cross-checked against 8–25+ independent sources. 19 critical corrections documented. This is unusually thorough for a survey.
2. **Lifecycle mapping:** The practitioner-workflow expansion (130+ sources, 6-stage lifecycle) provides exceptional context for frequency and pain point scoring.
3. **Multiplicative scoring:** Correctly penalizes single-dimension weakness. The Maceda refund (A:5, F:3, M:2 = 30) vs. assessment-level-lookup (A:4, F:5, M:5 = 100) ranking captures the intuition that deep moats matter more for long-term value.
4. **Cross-loop coordination:** BIR zonal values and LGU assessment database identified as 325+ and 360+ combined composite point shared assets across both loops.

### Key Limitation
The catalog is a **survey**, not a specification. Each entry provides enough to decide "should we deep-dive?" but not enough to build. The recommended deep-dive loops are the next step for any computation selected for implementation.

---

## 7. Corrections Applied to Catalog

The following correction was applied to `output/opportunity-catalog.md`:

1. **Updated tax loop cross-reference** to reflect that the tax loop catalog now exists, with key reconciliation findings (ZV lookup at 125, RPT at 125, shared data asset confirmation, assessment-level/RPT boundary clarification).
