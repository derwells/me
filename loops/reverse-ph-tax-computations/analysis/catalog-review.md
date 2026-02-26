# Catalog Self-Review — Completeness, Actionability, and Scoring Correctness

**Wave:** 4 (Scoring & Synthesis)
**Date:** 2026-02-26
**Aspect:** catalog-review
**Verdict:** PASS — catalog is complete, actionable, and correctly scored. Minor housekeeping corrections applied.

---

## 1. Completeness Review

### All 12 Computations Present

| # | Computation | Catalog Entry | Analysis File | Verification Status |
|---|---|---|---|---|
| 1 | Zonal Value Lookup | Present | zonal-value-lookup.md | Confirmed (10+ sources) |
| 2 | RPT Computation | Present | rpt-computation.md | Confirmed with corrections |
| 3 | Installment VAT Schedule | Present | installment-vat-schedule.md | Confirmed (12+ sources) |
| 4 | VAT on Real Property | Present | vat-real-property.md | Confirmed with corrections |
| 5 | CWT Rate and Timing | Present | cwt-rate-and-timing.md | Confirmed (10+ sources) |
| 6 | Transfer Tax | Present | transfer-tax.md | Confirmed with corrections |
| 7 | CGT Computation | Present | cgt-computation.md | Confirmed (5+ sources) |
| 8 | Highest-of-Three Base | Present | highest-of-three-base.md | Confirmed (6+ sources) |
| 9 | DST on Mortgage | Present | dst-on-mortgage.md | Confirmed (5+ sources) |
| 10 | EWT Rate Classification | Present | ewt-rate-classification.md | Confirmed (8+ sources) |
| 11 | Form 2307 Issuance | Present | form-2307-issuance.md | Confirmed (15 sources) |
| 12 | DST on Conveyance | Present | dst-on-sale.md | Confirmed (6+ sources) |

All 12 present. No gaps.

### PROMPT.md Scope Coverage

| Scope Item | Status | Where Covered |
|---|---|---|
| CGT, DST, VAT, CWT, Transfer Tax | Covered | Entries #1–12 |
| Highest-of-three base | Covered | Entry #8 |
| Zonal value lookup | Covered | Entry #1 |
| EWT rate classification | Covered | Entry #10 |
| VAT reconciliation (2550M vs 2550Q vs ITR) | Correctly excluded | Not a deterministic computation — filing workflow. 2550M abolished (mandatory quarterly since Jan 2023). Noted in bir-form-structures.md and practitioner-workflow.md |
| Form 2307 issuance logic | Covered | Entry #11 |
| Alphalist generation (1604-C/E/F) | Correctly excluded | Data formatting task (compile 2307s into DAT file), not a tax computation. Covered within Form 2307 entry's reconciliation chain description |
| RPT computation + SEF | Covered | Entry #2 (SEF = AV × 1%, included in formula) |

### Supporting Infrastructure

- **Analysis files:** 21 files in `analysis/` (all Wave 1–4 aspects covered)
- **Input files:** 3 files in `input/` (nirc-tax-titles, bir-revenue-regulations, bir-form-2307-reference)
- **Note:** 3 Wave 1 files (practitioner-guides, bir-form-structures, zonal-value-samples) stored in `analysis/` rather than `input/` per PROMPT.md convention. Content is intact; minor organizational inconsistency, not worth relocating.

### Computations Considered But Correctly Excluded

1. **Capital/ordinary asset classification** — Non-deterministic (requires judgment per RR 7-2003). Correctly treated as user input across all dependent computations.
2. **VAT reconciliation** — Filing workflow, not computation. No deterministic formula to extract.
3. **Alphalist/DAT generation** — Data formatting per BIR Module v7.4 spec. Infrastructure task, not tax computation.
4. **Percentage tax (3%)** — Simple flat rate for non-VAT-registered sellers. Already encoded in all existing tools. Zero opportunity.

---

## 2. Actionability Review

### Required Fields Per Entry

| Field | Present in All 12? | Quality |
|---|---|---|
| What it computes (inputs → outputs) | YES | Specific input types, formulas with variables, worked examples where relevant |
| Legal basis | YES | Specific NIRC sections, RR numbers, RMC numbers. Dates included for amendments |
| Current state | YES | Clear categorization: fully manual / partially automated / well-covered |
| Complexity estimate | YES | 3-dimension scoring (BR/LT/ED) with raw counts and justification |
| Competitive gap | YES | Named tools (JuanTax, Taxumo, QNE, eONETT, Housal, REN.PH, etc.) with specific feature coverage |
| Moat score | YES | Justified per entry; consistent scale across catalog |

### Strategic Guidance Completeness

| Element | Present | Assessment |
|---|---|---|
| 4-tier ranking | YES | Clear thresholds (80–125 / 50–79 / 25–49 / 1–24) |
| Strategic build clusters | YES | 4 clusters (A–D) with dependency chain and aggregate scores |
| Deep-dive loop recommendations | YES | P0–P3 priority with scope estimates |
| Infrastructure dependencies | YES | Zonal value → 5 computations; LGU database → 2 computations |
| Time-sensitivity | YES | RPVARA first-mover window (through mid-2026) flagged |
| Non-deterministic boundaries | YES | 4 gates explicitly identified and scoped as user inputs |

**Actionability verdict:** The catalog is directly usable for prioritizing deep-dive loops. No additional analysis needed to decide whether to build P0 (Zonal Value) or P1 (RPT) next.

---

## 3. Scoring Correctness Review

### Per-Entry Score Validation

| Entry | AG | MF | MD | Score | Review |
|---|---|---|---|---|---|
| Zonal Value Lookup | 5 | 5 | 5 | 125 | CORRECT — absolute gap, universal prerequisite, massive data moat |
| RPT Computation | 5 | 5 | 5 | 125 | CORRECT — absolute gap, annual obligation, 1,700-LGU database |
| Installment VAT | 5 | 3 | 5 | 75 | CORRECT — absolute gap, developer subset, deepest operational complexity |
| VAT on Real Property | 4 | 4 | 4 | 64 | CORRECT — filing covered but decision logic isn't, most external dependencies |
| CWT Rate and Timing | 5 | 4 | 3 | 60 | CORRECT — absolute gap, compact rate table but meaningful branching |
| Transfer Tax | 4 | 5 | 3 | 60 | CORRECT — no per-LGU tool, every sale, shared LGU database moat |
| CGT Computation | 3 | 5 | 3 | 45 | CORRECT — basic exists, gap in advanced features, law is public |
| Highest-of-Three Base | 4 | 5 | 2 | 40 | CORRECT — integration layer, max(a,b,c), moat in data not formula |
| DST on Mortgage | 5 | 4 | 2 | 40 | CORRECT — zero coverage, every mortgage, straightforward once read |
| EWT Classification | 2 | 5 | 2 | 20 | CORRECT — QNE/JuanTax/Taxumo cover this, no differentiation |
| Form 2307 | 2 | 5 | 2 | 20 | CORRECT — multiple tools generate 2307, workflow not computation gap |
| DST on Conveyance | 2 | 5 | 1 | 10 | CORRECT — base × 1.5%, trivially replicable, zero moat |

### Cross-Entry Consistency Checks

1. **AG consistency:** Absolute gaps (score 5) all verified — no existing tool handles CWT tiering, installment VAT schedules, full-LGU RPT, mortgage DST, or API-accessible zonal lookup. Partially covered (score 2-3) correctly identifies tools that exist. ✓
2. **MF consistency:** MF=5 applied to 9/12 computations reflecting universal or near-universal applicability. MF=3 for installment VAT (developer subset only) and MF=4 for VAT/CWT (ordinary asset subset) and DST on mortgage (financed transactions) correctly differentiate frequency. ✓
3. **MD consistency:** MD=5 reserved for data moats (zonal value workbooks, LGU database, multi-period tracking). MD=1 only for trivially replicable formula (DST on sale). Intermediate scores (2-4) reflect increasing regulatory depth and data requirements. ✓
4. **No score conflicts between catalog and opportunity-scoring analysis file.** All 12 entries match exactly. ✓

### Potential Scoring Challenges (Reviewed, No Changes Made)

1. **Installment VAT MF=3:** Could argue MF=4 since developer sales are a large market segment and each developer generates thousands of schedules. However, the computation applies to a *subset* of RE transactions (developers/installment sellers only), unlike CGT/DST which apply to every transaction. MF=3 is defensible.

2. **Transfer Tax MD=3:** Could argue MD=2 since the formula is simple (base × rate). However, the LGU rate database requirement elevates moat beyond the formula. The strategic note that "marginal moat drops to ~1 once RPT engine exists" correctly captures the dependency without adjusting the raw score.

3. **Multiplicative scoring model:** AG × MF × MD means a low score on any dimension severely depresses the composite. DST on Conveyance (AG=2, MF=5, MD=1 = 10) illustrates this — high frequency doesn't compensate for trivial moat. This is the intended behavior: computations need strength on all three dimensions to rank highly.

---

## 4. Issues Found and Corrections Applied

| # | Issue | Severity | Correction |
|---|---|---|---|
| 1 | Frontier statistics wrong: showed Total 24, Analyzed 22, Pending 2. Actual: Total 23, Analyzed 22, Pending 1 | Minor | Corrected in frontier/aspects.md |
| 2 | Analysis log missing transfer-tax entry (Wave 2, 2026-02-26) | Minor | Added as entry #15 in frontier/analysis-log.md |
| 3 | Catalog status line says "Draft (pending self-review)" | Expected | Updated to "Final" in output/opportunity-catalog.md |
| 4 | 3 Wave 1 files in analysis/ instead of input/ | Cosmetic | Noted; not relocated (content intact, references work) |

---

## 5. Final Assessment

The opportunity catalog is **complete, actionable, and correctly scored**. It covers all 12 deterministic computations in scope, with verified formulas (Wave 2 cross-checks against 2+ independent sources each), competitive gap analysis (12 tools surveyed), practitioner workflow context, and a multiplicative scoring model that correctly prioritizes data-moat opportunities over formula-complexity ones.

The catalog directly answers the loop's goal: "which computations deserve their own dedicated deep-dive loop?" Answer: P0 Zonal Value Lookup, P1 RPT Computation, P2 ONETT Transaction Tax Engine, P3 Installment VAT Schedule.

**Recommendation:** Loop converged. Proceed to convergence.
