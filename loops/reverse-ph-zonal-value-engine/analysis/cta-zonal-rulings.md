# CTA & Supreme Court Zonal Value Rulings — Analysis

**Wave:** 1 — Source Acquisition
**Date:** 2026-03-02
**Aspect:** cta-zonal-rulings
**Sources:** 9 court cases (4 CTA, 5 Supreme Court), 4 BIR administrative issuances, legal commentaries

---

## Summary

Philippine jurisprudence on zonal value disputes clusters around **five principal dispute categories**, each with direct implications for the zonal value lookup engine's resolution logic. The landmark case is *CIR v. Aquafresh Seafoods* (G.R. No. 170389, 2010), which definitively established that **published zonal classifications cannot be unilaterally overridden by the BIR** — a principle that simplifies the engine's classification resolution: the published schedule is authoritative, period.

---

## Five Categories of Zonal Value Disputes

### Category 1: Classification Disputes (Actual Use vs. Published Classification)

**Governing case:** CIR v. Aquafresh Seafoods (G.R. No. 170389 / CTA E.B. No. 77)

**The dispute pattern:**
- BIR investigator conducts ocular inspection → observes commercial activity on land classified as residential
- BIR reclassifies the property unilaterally → assesses higher CGT/DST based on commercial zonal value
- Taxpayer protests, citing the published schedule's residential classification

**Established rules:**
1. **Published classification is binding.** If a zone is classified in the published schedule (via DOF Department Order), that classification governs regardless of actual use.
2. **"Predominant use" rule has a narrow scope.** It applies ONLY to areas "where the properties are NOT YET classified and their respective zonal valuation are NOT YET determined." This is a gap-filling rule, not an override.
3. **Reclassification requires the full statutory pipeline.** Section 6(E) NIRC mandates consultation with public and private appraisers. The BIR cannot skip this through enforcement actions.
4. **Fraud allegations require clear and convincing evidence.** The BIR's claim that the taxpayer colluded with the City Assessor was rejected for lack of proof.

**Specific values:**
- Residential (RR): PHP 650/sqm
- Commercial (CR) claimed by BIR: PHP 2,000/sqm
- Delta: 3.08x — demonstrating how classification disputes create massive tax exposure

**Engine implication:** The engine should resolve classification based on the published schedule, NOT based on any "actual use" input. If a user queries a property on a street classified as RR in the schedule, the engine returns the RR value — no second-guessing. This dramatically simplifies the matching logic.

---

### Category 2: Missing/Absent Zonal Value (No Published Value for Location or Classification)

**Governing cases:**
- Spouses Emiliano v. CIR (CTA E.B. No. 1103, 2015)
- CIR v. Heirs of Gamboa (CTA Case No. 9720, 2020)
- CTA Case No. 9234 (General Purpose Interior classification gap)

**The dispute pattern:**
- Property is in a barangay or has a classification code with no published zonal value
- BIR substitutes its own valuation (bank appraisal, SID investigation, comparable sales) without following Section 6(E)/(F) procedures
- Taxpayer challenges the unilateral valuation

**Established rules:**
1. **No published ZV → BIR cannot substitute arbitrarily.** BIR must follow Section 6(F) appraisal procedures, which require independent valuation methodology.
2. **Due process is essential.** The STCRPV → TCRPV → ECRPV → DOF Secretary pipeline cannot be bypassed, even when the absence of a ZV creates an administrative inconvenience.
3. **Bank appraisals are not a valid substitute.** The BIR cannot simply adopt a bank's appraised value (Heirs of Gamboa).
4. **Classification gaps create real disputes.** CTA Case No. 9234 shows that even specific sub-classifications (e.g., "General Purpose Interior") may be present in one Department Order but absent in another, requiring a fallback mechanism.

**Engine implication:** The engine MUST implement a clear fallback hierarchy when no exact match exists:
1. Exact match (street + classification) → return value
2. Barangay general rate (same classification) → return value with confidence flag
3. No match at all → return NULL with explicit "no published zonal value" indicator

The engine should NEVER fabricate or interpolate a value. The absence of a published value is itself legally meaningful — it triggers a different administrative pathway (RDO written inquiry / Section 6(F) appraisal).

---

### Category 3: Procedural Defects in Zonal Value Establishment

**Governing cases:**
- CIR v. Aquafresh Seafoods (consultation requirement)
- Spouses Emiliano v. CIR (due process)
- CIR v. Spouses Gow (assessment procedure)

**The dispute pattern:**
- BIR publishes or applies zonal values without following the required procedural steps
- Taxpayer challenges the assessment on procedural grounds

**Established rules:**
1. **Section 6(E) consultation is mandatory**, not advisory. The committee must include both public and private sector appraisers.
2. **Publication requirements are strict.** RR 6-01 mandates: 2 newspapers × 2 consecutive weeks + posting at RDO, City/Municipal Hall, barangay halls.
3. **Effectivity starts 15 days after last publication** unless a later date is specified.
4. **Published values carry "presumptive validity"** (CIR v. Spouses Salvador, 2016) — once properly published, they're binding until revised through the same procedure.

**Engine implication:** The engine should track the Department Order number and effectivity date for each schedule revision. When processing a transaction, the engine must match the transaction date to the correct revision — applying a future revision to a past transaction is procedurally defective and judicially challengeable.

---

### Category 4: Stale/Outdated Zonal Values

**Context (not a single case, but a systemic issue):**
- BIR mandate: revise zonal values every 3 years (EO 45, RMO 31-2019)
- Reality: 38% of schedules outdated per DOF 2024 data; ~40% of RDO SMVs and ~60% of LGU SMVs not revised (BLGF 2021 report)
- RPVARA (RA 12001, 2024) specifically addresses this as a systemic failure

**Established rules:**
1. **Existing schedule remains in force until formally revised** — even if decades old. The 1995 Revised Zonal Values in the Aquafresh case were applied to a 1999 transaction without challenge to their validity.
2. **A taxpayer may contest the zonal value "as applied" but not the schedule itself.** The schedule's validity is presumed until revised; the taxpayer's remedy is to challenge whether the correct schedule was applied to their property.
3. **BIR cannot unilaterally "update" values without going through the full revision pipeline.** Even if the schedule is clearly outdated, the BIR must follow Section 6(E) procedures.

**Engine implication:** The engine will inevitably serve stale data for many RDOs. This is legally correct — the stale value IS the applicable value until revision. The engine should display the effectivity date and Department Order number prominently so users understand the vintage of the data. Consider a "last revised" indicator with a staleness warning for schedules older than 3 years.

---

### Category 5: Zonal Value vs. Other Valuations (Expropriation / Just Compensation)

**Governing cases (Supreme Court):**
- Republic v. Spouses Legaspi (G.R. No. 221995)
- Republic v. Estrella Decena (G.R. No. 212786)
- Republic v. Spouses Goloyuco (G.R. No. 222551)
- Secretary of DPWH v. Spouses Tecson (G.R. No. 179334, 2015)
- Republic v. Castillo (G.R. No. 220451, Feb 2024)

**The dispute pattern:**
- Government expropriates property and offers compensation based on BIR zonal value
- Landowner argues zonal value drastically understates fair market value

**Established rules:**
1. **ZV is "merely one of the indices" of FMV** — not the sole basis for just compensation
2. **ZV is the basis for provisional compensation** (under RA 10752/RA 8974), but final just compensation requires a full valuation
3. **Private appraisals can prevail** if supported by comparable sales data (Republic v. Castillo, 2024)
4. **The gap can be enormous.** In DPWH v. Spouses Mirandilla: ZV = PHP 2,300/sqm, court award = PHP 15,000/sqm (6.5x)

**Engine implication:** While expropriation is technically out of scope for a tax computation engine, this category is important context for the engine's UI. The engine should clearly label its output as "BIR Zonal Value (for tax computation purposes)" and explicitly NOT represent it as "fair market value" or "property value." A disclaimer is warranted.

---

## Implications for Engine Design (Cross-Cutting)

### 1. Classification Resolution Is Simpler Than Expected
The Aquafresh ruling means the engine does NOT need to determine "actual use" — it only needs to look up the published classification. If the published schedule says "RR" for a street/vicinity, that's the answer. The engine should not accept user-overridden classifications that contradict the published schedule.

However, the user still needs to select a classification when a vicinity has MULTIPLE classifications listed (e.g., a street with both RR and CR entries for different properties). This is a UX design challenge, not a legal one.

### 2. Fallback Must Be Explicit, Not Interpolated
When no value is found, the engine must return a clear "no published zonal value" result — not an interpolated or estimated value. This is a legal requirement, not just a UX choice. The BIR itself must follow Section 6(F) procedures in this situation.

The fallback chain:
1. Exact match (street + vicinity + classification)
2. Barangay-level general rate (same classification)
3. "No published zonal value" — advise user to submit written inquiry to RDO

### 3. Schedule Vintage Is Legally Material
The engine must track and display the Department Order number and effectivity date. Transactions are assessed against the schedule in effect at the transaction date, not the latest schedule. This means the engine may need to serve multiple revisions for a single RDO.

### 4. Condominium Valuation Has Unique Complexity
No specific CTA ruling was found directly addressing per-unit vs. per-sqm condominium disputes, but the BIR's classification system treats condominiums distinctly:
- Ground floor → classified as commercial (per BIR convention)
- Parking slots (PS) → valued per slot, not per sqm
- Per-building valuation matrices exist for named projects
- Floor-range and tower-specific values exist in NCR workbooks

### 5. RPVARA Transition Creates a Temporal Fork
Post-RPVARA (RA 12001, effective 2024), the CIR's authority to determine zonal values will be replaced by DOF-approved SMVs. During the 2-year transition, existing zonal values remain in force. The engine must be designed to handle this transition — eventually consuming SMV data from BLGF/DOF alongside legacy BIR zonal values.

---

## Case Inventory for Engine Validation

These cases provide real-world test scenarios for validating the engine's resolution logic:

| Case | Test Scenario | Expected Engine Behavior |
|------|--------------|-------------------------|
| Aquafresh | Property in Barrio Banica, Roxas City, classified RR in schedule but used commercially | Return RR value (PHP 650/sqm), NOT CR value |
| Spouses Emiliano | Property with no published zonal value | Return "no published ZV" result |
| Heirs of Gamboa | Property where BIR used bank appraisal | Return "no published ZV" — bank appraisal is not a valid substitute |
| CTA 9234 | "General Purpose Interior" classification absent from DO 50-2000 | Return fallback value or "classification not in current DO" |
| DPWH v. Mirandilla | Expropriation context | Return BIR ZV with disclaimer: "for tax computation only, not indicative of fair market value" |

---

## Gaps and Areas for Deeper Investigation (Wave 3+)

1. **Agricultural reclassification timing:** When agricultural land is reclassified by the LGU but the BIR schedule hasn't been updated, which value applies? Likely the existing published schedule (per Aquafresh principle), but no specific CTA case directly addresses this common scenario.

2. **Condo-specific disputes:** No CTA case found on per-unit vs. per-sqm condo valuation disputes. This may indicate it hasn't been litigated (possibly because BIR workbooks explicitly specify the unit, making disputes less common) or that cases aren't publicly available.

3. **Multi-classification streets:** What happens when a single street has multiple classification entries (e.g., RR for one side, CR for the other)? The engine needs a strategy for presenting all options to the user. No CTA ruling found on this specific scenario.

4. **Revision retroactivity:** Can a new zonal schedule be applied retroactively to pending transactions? The 15-day effectivity rule from RR 6-01 suggests not, but this hasn't been directly litigated in the CTA cases found.

5. **RPVARA transition disputes:** RA 12001 is new (2024) — no CTA cases yet on disputes arising from the BIR→BLGF transition. This is a future dispute category the engine should monitor.
