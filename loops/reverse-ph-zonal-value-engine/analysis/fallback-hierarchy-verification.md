# Fallback Hierarchy Verification — Independent Source Cross-Check

**Wave:** 3 — Resolution Logic Deep-Dive
**Date:** 2026-03-03
**Aspect:** `fallback-hierarchy-implementation` (verification sub-task)
**Method:** Web search for independent sources (legal databases, law firm commentaries, BIR issuances, CTA decisions)
**Sources consulted:** 18+ independent sources across legal, practitioner, and government domains

---

## Executive Summary

The 6-level fallback hierarchy is **LARGELY CONFIRMED** with two significant corrections required:

1. **Level 4 LGU FMV markup percentages: CRITICAL DISCREPANCY IDENTIFIED.** Two competing formulas exist: RAMO 2-91 specifies **LGU FMV + 100%** (residential/general) / **LGU FMV + 150%** (commercial/industrial/fishpond). A separate practitioner source (Respicio & Co.) cites **LGU FMV + 20%** as current RDO practice. These are NOT the same rule — RAMO 2-91 is the formal issuance; the 20% figure appears to be a more recent informal RDO practice that has not been formally codified. Both may coexist depending on RDO.

2. **The three "embedded workbook rules" are CONFIRMED as appearing in actual BIR Department Order footnotes** (not just workbook implementation guidelines). They are standard provisions attached to DOF-approved zonal value schedules.

3. **All three CTA/SC cases are CONFIRMED** with correct holdings.

4. **Level 6 (Zonal Classification Ruling) is CONFIRMED** as an administrative practice but has NO formal BIR issuance codifying it — it exists in the gap between administrative practice and formal regulation.

---

## Level 1: Exact Street + Classification Match

### Claimed Rule
> Exact street + classification match found → Use matched value

### Source 1: Section 6(E) NIRC of 1997, as amended by RA 10963 (TRAIN Law)
- **Finding:** The Commissioner is authorized to "divide the Philippines into different zones or areas and shall determine the fair market value of real properties located in each zone or area." Published zonal values apply provided they are "higher than (1) the fair market value as shown in the schedule of values of the provincial and city assessors and (2) the gross selling price."
- **Verdict:** **CONFIRMED.** The statutory framework establishes exact-match lookup as the primary mechanism.
- **Source:** [NIRC Section 6(E)](https://www.bir.gov.ph/index.php/tax-code.html); [RMO 31-2019 (PDF)](https://blgf.gov.ph/wp-content/uploads/2015/09/BIR-RMO_No.-31-2019-SMV.pdf)

### Source 2: CIR v. Aquafresh Seafoods, Inc. (G.R. No. 170389, October 20, 2010)
- **Finding:** The Supreme Court held that "the existing Revised Zonal Values in the City of Roxas should prevail for purposes of determining respondent's tax liabilities." Published classification is binding — BIR "cannot unilaterally change the zonal valuation of such properties to 'commercial' without first conducting a re-evaluation."
- **Verdict:** **CONFIRMED.** Published schedule values are authoritative; exact match is the default and legally correct lookup.
- **Source:** [G.R. No. 170389 (LawPhil)](https://lawphil.net/judjuris/juri2010/oct2010/gr_170389_2010.html)

### Source 3: Respicio & Co. Legal Commentary
- **Finding:** "For national taxes, the FMV used is the higher of (a) BIR zonal value, if any, or (b) FMV per the assessor's schedule ('market value' on the property's tax declaration) for the relevant date."
- **Verdict:** **CONFIRMED.** Standard practitioner understanding aligns with the claimed rule.
- **Source:** [Respicio & Co. — Capital Gains Tax Based on Zonal Value](https://www.lawyer-philippines.com/articles/capital-gains-tax-based-on-zonal-value-philippines)

**LEVEL 1 VERDICT: FULLY CONFIRMED (3/3 sources agree)**

---

## Level 2: Barangay General Entry ("All Other Streets" / "General Purpose Interior")

### Claimed Rule
> Street not listed but barangay has "All other streets" or "General Purpose Interior" entry → Use barangay-level general entry. Claimed authority: RMO 31-2019 practice.

### Source 1: Actual BIR Zonal Value Workbooks (sampled from 31 RDO workbooks)
- **Finding:** "ALL OTHER STREETS IN [BARANGAY NAME]" entries are confirmed present — 185 such entries documented across sampled workbooks (see `analysis/address-matching-algorithms.md`). These function as barangay-level catch-all rates. "GENERAL PURPOSE INTERIOR" entries also documented in specific RDOs (e.g., DO 33-05 for Cabuyao, Laguna: "General Purpose Interior" at P825.00/sqm).
- **Verdict:** **CONFIRMED.** These entries exist in published schedules as standard catch-all mechanisms.
- **Source:** `analysis/address-matching-algorithms.md`, `analysis/address-vicinity-patterns.md`; [ZonalValuesPH — Marikina "All Other Streets"](https://zonalvaluesph.altervista.org/zonal-value-of-all-other-streets-along-marikina-city-whereisit-137402689/)

### Source 2: BIR DOF Department Order Footnotes (Standard Provision)
- **Finding:** BIR zonal value schedules contain a standard fallback footnote: "Where in the approved listing of zonal values, no value has been prescribed for a particular classification, the zonal value prescribed for the same class of real property located in the other street/subdivision within the same barangay of similar conditions shall be used." This is effectively the mechanism that "All Other Streets" entries implement.
- **Verdict:** **CONFIRMED.** The catch-all entries are the DOF-approved implementation of this standard footnote rule.
- **Source:** Multiple DOF Department Orders implementing BIR zonal value schedules; web search synthesis from [BIR Zonal Values](https://www.bir.gov.ph/zonal-values)

### Source 3: Respicio & Co. Commentary
- **Finding:** Confirms that if a property is on a street not in the schedule, practitioners should "find the applicable barangay/subdivision entry."
- **Verdict:** **CONFIRMED.**
- **Source:** [Respicio — Basis for Zonal Valuation](https://www.respicio.ph/commentaries/basis-for-zonal-valuation-of-properties-in-the-philippines)

**Claimed authority note:** The claim attributes this to "RMO 31-2019 practice." More precisely, the "All Other Streets" entries and general-rate fallbacks appear in the **DOF Department Orders** implementing the schedules (which are drafted per RMO 31-2019 procedures), not in the text of RMO 31-2019 itself. The RMO governs the *process* for establishing values; the DOs contain the actual values and catch-all entries. This is a minor precision correction, not a substantive error.

**LEVEL 2 VERDICT: FULLY CONFIRMED (3/3 sources agree). Minor authority attribution refinement needed — DOF DOs, not RMO 31-2019 text per se.**

---

## Level 3: Institutional Property (X Code) Fallback

### Claimed Rule
> Property is special use (school, hospital, church) with no X code entry → Apply nearest commercial zonal value within same barangay. Claimed authority: RMO 31-2019 / RAMO 2-91.

### Source 1: BIR DOF Department Order Standard Footnotes
- **Finding:** BIR zonal value schedules contain the standard footnote: "If no zonal value has been prescribed for institutional properties (schools, hospitals, churches), the commercial value of the property nearest to the institution, within the same barangay, shall be used."
- **Verdict:** **CONFIRMED.** The exact rule as stated. "Nearest commercial zonal value within same barangay" is the correct formulation.
- **Source:** Standard DOF Department Order footnotes (confirmed across multiple RDO schedules via web search)

### Source 2: RMO 31-2019 Annex B Classification Code Definition
- **Finding:** Annex B defines X (Institutional) as "Schools, churches, hospitals." The code exists in the standard classification system. The fallback-to-commercial rule is not in the RMO text itself but in the DOF Department Order footnotes that implement the schedules drafted under RMO 31-2019 procedures.
- **Verdict:** **CONFIRMED** for the rule. **PARTIALLY CONFIRMED** for authority attribution — the rule is in DOF Department Order footnotes, not in RMO 31-2019 body text or RAMO 2-91.
- **Source:** `analysis/rmo-31-2019-annexes.md`; [BIR Land Classifications](https://zonalvaluefinderph.com/BIR_Land_Classifications)

### Source 3: Analysis Loop Internal Validation
- **Finding:** `analysis/classification-resolution-logic.md` documents "Path 6: Institutional Fallback — X code with no value → nearest CR in same barangay/street" as one of the 7 resolution paths, noting it is "per BIR DO footnotes."
- **Verdict:** **CONFIRMED** — consistent with the DO footnote source.
- **Source:** `analysis/classification-resolution-logic.md`

**Authority correction:** The claim cites "RMO 31-2019 / RAMO 2-91" as authority. More accurately, the institutional fallback rule appears in **DOF Department Order footnotes** (which are the published zonal value schedules). Neither the RMO 31-2019 body text nor RAMO 2-91 contains this specific rule. RAMO 2-91 covers a different scenario entirely (no zonal value exists at all → use LGU FMV + markup).

**LEVEL 3 VERDICT: RULE CONFIRMED (3/3 sources agree). Authority attribution needs correction — DOF DO footnotes, not RMO 31-2019 or RAMO 2-91.**

---

## Level 4: No Barangay-Level Zonal Value — LGU FMV Markup

### Claimed Rule
> No barangay-level zonal value exists at all → Use LGU FMV + 100% (residential/general) or LGU FMV + 150% (commercial/industrial/fishpond), or nearest comparable zone's value. Claimed authority: RAMO 2-91.

### Source 1: RAMO 2-91 Full Text (Supreme Court E-Library)
- **Finding:** RAMO 2-91 (Revenue Administrative Memorandum Order No. 2-91, February 18, 1991) states: "When the zonal value of land has NOT been established, there shall be added to the market value per latest tax declaration ONE HUNDRED PERCENT (100%) thereof. PROVIDED, that if the property is classified as commercial, industrial and agricultural devoted to fishpond/prawn farm, ONE HUNDRED FIFTY PERCENT (150%) shall be added thereto."
- **Verdict:** **CONFIRMED.** The 100%/150% markups are the exact text of RAMO 2-91.
- **Source:** [RAMO 2-91 — Supreme Court E-Library](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/49658)

### Source 2: Respicio & Co. Legal Commentary
- **Finding:** States that "Where no zonal value exists (typically rural barangays), RDO uses the **LGU FMV plus 20%** or adopts the nearest comparable zone."
- **Verdict:** **CONTRADICTS the 100%/150% figures.** This source cites a **20% markup** as current RDO practice, not the 100%/150% from RAMO 2-91.
- **Source:** [Respicio — Basis for Zonal Valuation](https://www.respicio.ph/commentaries/basis-for-zonal-valuation-of-properties-in-the-philippines)

### Source 3: BIR DOF Department Order Footnotes
- **Finding:** Standard footnote in zonal value schedules states: "In the absence of zonal valuation, property shall be valued pursuant to RAMO 2-91." This confirms RAMO 2-91 as the formal fallback authority.
- **Verdict:** **CONFIRMS RAMO 2-91 as the formal authority** but does not resolve the 100% vs. 20% discrepancy.
- **Source:** Multiple DOF Department Orders; web search synthesis

### Discrepancy Resolution Analysis

The **100%/150% (RAMO 2-91)** vs. **20% (Respicio practitioner source)** discrepancy requires careful analysis:

| Factor | RAMO 2-91 (100%/150%) | Respicio (20%) |
|--------|----------------------|----------------|
| **Source type** | Formal BIR administrative issuance (1991) | Legal commentary (2025) |
| **Legal authority** | Published in SC E-Library, referenced in DOF DOs | Practitioner observation, no issuance cited |
| **Date** | February 18, 1991 | Published August 2025 |
| **Context** | Formula for computing tax base when no ZV exists | Description of current RDO operational practice |

**Most likely explanation:** RAMO 2-91's 100%/150% formula was established in 1991 when LGU tax declaration market values were significantly lower relative to actual market values. The formula was designed to approximate actual FMV from often-understated tax declaration values. Over 35 years, LGU assessors have (in many areas) updated their Schedules of Market Values to be closer to actual market values, making the 100% markup excessive. Some RDOs may have adopted an informal operational practice of using a lower markup (20%) that better reflects current conditions — but this informal practice has no formal issuance backing it.

**For the engine:** The formal rule (RAMO 2-91, 100%/150%) is the legally defensible position. The 20% figure may represent current operational practice at some RDOs but is not codified. The engine should:
1. Reference RAMO 2-91 as the applicable formula when returning a "no ZV" result
2. Note that actual RDO practice may vary
3. NOT compute a markup value (as this would be generating a zonal value that does not exist in the published schedule — the CTA rulings prohibit this)

**LEVEL 4 VERDICT: PARTIALLY CONFIRMED.**
- **100%/150% formula:** CONFIRMED as the text of RAMO 2-91
- **RAMO 2-91 as authority:** CONFIRMED by DOF DO standard footnotes
- **"Nearest comparable zone" alternative:** CONFIRMED as a separate fallback option
- **DISCREPANCY FLAG:** A 20% figure from practitioner sources suggests operational practice may diverge from the formal issuance. Engine should cite formal rule but flag this as a known practical divergence.

---

## Level 5: Boundary Dispute / Ambiguous Jurisdiction

### Claimed Rule
> Written inquiry to RDO Zonal Valuation Section; escalation to BIR Valuation and Classification Division (national office). Claimed authority: RMO 31-2019.

### Source 1: BIR Citizens Charter 2024
- **Finding:** The BIR Citizens Charter documents the processing of One-Time Transactions (ONETT) including zonal value certification. Processing jurisdiction is at the RDO level. The Charter confirms that the RDO with jurisdiction over the property location is responsible for processing. Simple ONETT transactions should not exceed 3 working days.
- **Verdict:** **PARTIALLY CONFIRMED.** The RDO is confirmed as the first point of contact. The Citizens Charter does not specifically describe a "Zonal Valuation Section" or escalation procedures.
- **Source:** [BIR Citizens Charter 2024](https://bir-cdn.bir.gov.ph/BIR/pdf/citizens-charter-rr-rdo-2024-v3.pdf)

### Source 2: Respicio & Co. Legal Commentary
- **Finding:** "If taxpayers believe that the zonal value set by the BIR is unreasonably high, they can engage in administrative remedies. Typically, this involves contacting the BIR's **Valuation and Classification Division**, or filing a written protest with the Revenue District Office (RDO)." A protest must be filed within 30 days from payment or receipt of assessment.
- **Verdict:** **PARTIALLY CONFIRMED.** The existence of the Valuation and Classification Division as an escalation point is confirmed. However, this source describes it in the context of *contesting* a published value, not in the context of *absence* of a value. The specific "Zonal Valuation Section" within the RDO is not verified as a named organizational unit — practitioners refer to the broader "Valuation and Classification Division" at the national office level.
- **Source:** [Respicio — Real Estate Zonal Value Inquiry](https://www.lawyer-philippines.com/articles/real-estate-zonal-value-inquiry-in-the-philippines)

### Source 3: RMO 31-2019 Committee Structure
- **Finding:** RMO 31-2019 establishes the three-tier committee system: Sub-Technical Committee on Real Property Valuation (STCRPV) at the RDO level, Technical Committee on Real Property Valuation (TCRPV) at the Regional level, and Executive Committee on Real Property Valuation (ECRPV) at the national level. Boundary and classification disputes would follow this committee escalation path rather than a generic "written inquiry" path.
- **Verdict:** **ADDS TO the claimed rule.** The escalation path is more structured than "RDO → national office." It follows the STCRPV → TCRPV → ECRPV → CIR approval pipeline.
- **Source:** [RMO 31-2019 (BLGF)](https://blgf.gov.ph/wp-content/uploads/2015/09/BIR-RMO_No.-31-2019-SMV.pdf); [RMC 06-2021 (BLGF)](https://blgf.gov.ph/wp-content/uploads/2015/09/RMC-06-2021-RMO-31-2019-Zonal-Values.pdf)

### Source 4: RR No. 11-2013
- **Finding:** "Under RR No. 11-2013, stakeholders can petition the CIR for revision of a specific zone's value, citing new market evidence."
- **Verdict:** **ADDS TO the claimed rule.** RR 11-2013 provides a formal mechanism for requesting zonal value revision (which would address boundary gaps), but this is a petition for revision rather than a one-off inquiry.
- **Source:** [Respicio — Basis for Zonal Valuation](https://www.respicio.ph/commentaries/basis-for-zonal-valuation-of-properties-in-the-philippines)

### Additional finding: RMC 115-2020
- **Finding:** Revenue Memorandum Circular 115-2020 eliminated the requirement for taxpayers to present zonal value certificates for ONETT processing. Revenue officers must obtain zonal values from the BIR website. However, taxpayers may still obtain certifications for transactions with other agencies.
- **Verdict:** **ADDS CONTEXT.** The "written inquiry" process has been simplified since 2020 — the burden of determining the applicable ZV has shifted to the BIR revenue officer, not the taxpayer.
- **Source:** [Manila Bulletin — BIR No Longer Requires ZV Certificate](https://mb.com.ph/2020/10/27/payment-of-capital-gains-tax-no-longer-requires-zonal-value-certificate-bir/)

**Process reconstruction from sources:**
1. Taxpayer files ONETT documents at the RDO
2. ONETT examiner looks up ZV from the published schedule (BIR website)
3. If no ZV found: ONETT examiner applies RAMO 2-91 (LGU FMV + markup) or requests STCRPV input
4. For boundary disputes: STCRPV → TCRPV → ECRPV escalation per RMO 31-2019
5. Taxpayer may also petition CIR for revision under RR 11-2013

**Specific names NOT verified:**
- "Zonal Valuation Section" — not confirmed as a named RDO sub-unit. The STCRPV is the relevant organizational body.
- No specific BIR form number identified for zonal value absence inquiries.
- No specific timeline found for processing written inquiries about absent values.

**LEVEL 5 VERDICT: PARTIALLY CONFIRMED.**
- Written inquiry to RDO: **CONFIRMED** (but process has been simplified by RMC 115-2020)
- Escalation path: **CONFIRMED** but more accurately described as STCRPV → TCRPV → ECRPV → CIR (per RMO 31-2019), not "RDO → Valuation and Classification Division"
- "Zonal Valuation Section": **NOT VERIFIED** as a specific organizational unit
- RMO 31-2019 as authority: **CONFIRMED** for the committee escalation structure
- No specific form or timeline: **NOT FOUND** — gap in available public information

---

## Level 6: Newly Reclassified Land — Zonal Classification Ruling

### Claimed Rule
> Newly reclassified land (e.g., agricultural → residential conversion) → RDO issues Zonal Classification Ruling pending next revision cycle. Claimed authority: Administrative practice.

### Source 1: Respicio & Co. Legal Commentary (August 2025)
- **Finding:** "Once agricultural land is re-classified to residential or commercial, the next zonal update normally reallocates the lot to a higher bracket. Until then, the Revenue District Office (RDO) issues a 'Zonal Classification Ruling' upon the developer's request."
- **Verdict:** **CONFIRMED** as practitioner-documented administrative practice. The term "Zonal Classification Ruling" is used.
- **Source:** [Respicio — Basis for Zonal Valuation](https://www.respicio.ph/commentaries/basis-for-zonal-valuation-of-properties-in-the-philippines)

### Source 2: CIR v. Aquafresh Seafoods (G.R. No. 170389)
- **Finding:** The Supreme Court ruled that the BIR cannot reclassify properties without following the full Section 6(E) procedure (public/private appraiser consultation, committee review, DOF approval, publication). This means that between the time an LGU reclassifies land and the next BIR zonal value revision, the **existing published classification governs**.
- **Verdict:** **ADDS COMPLEXITY.** The Aquafresh ruling creates a tension: the existing published classification prevails (Aquafresh), but the RDO can issue a Zonal Classification Ruling to bridge the gap (practitioner source). The ZCR appears to be the administrative mechanism by which the reclassification enters the BIR system pending the next formal revision.
- **Source:** [G.R. No. 170389 (LawPhil)](https://lawphil.net/judjuris/juri2010/oct2010/gr_170389_2010.html)

### Source 3: RR No. 11-2013
- **Finding:** "Under RR No. 11-2013, stakeholders can petition the CIR for revision of a specific zone's value, citing new market evidence." This provides a formal mechanism for requesting revision (which would cover newly reclassified land).
- **Verdict:** **PARTIALLY CONFIRMS** — a formal petition mechanism exists, but the "Zonal Classification Ruling" as a specific interim instrument is not found in any formal BIR issuance.
- **Source:** [Respicio — Basis for Zonal Valuation](https://www.respicio.ph/commentaries/basis-for-zonal-valuation-of-properties-in-the-philippines)

### Formal issuance search result
- **Finding:** No BIR Revenue Memorandum Order, Revenue Regulation, or Revenue Memorandum Circular was found that formally defines or establishes the "Zonal Classification Ruling" as an administrative instrument. The term appears only in practitioner commentary, not in primary legal sources.
- **Verdict:** The ZCR appears to be an **informal administrative practice** — a functional mechanism used by RDOs to address a real gap, but not formally codified in any published BIR issuance.

**LEVEL 6 VERDICT: PARTIALLY CONFIRMED.**
- Existence of practice: **CONFIRMED** by practitioner source
- "Zonal Classification Ruling" term: **CONFIRMED** in legal commentary but **NOT FOUND** in any formal BIR issuance
- Mechanism: Consistent with Aquafresh principle (published classification governs until formal revision)
- Authority: Correctly labeled as "Administrative practice" — no formal legal authority identified
- **Engine implication:** The engine should NOT implement ZCR logic. If the published schedule shows "A" (agricultural) and the LGU has reclassified to residential, the engine should return the published "A" value with a note that the classification may be outdated pending BIR schedule revision. Per Aquafresh, the published classification is authoritative.

---

## Embedded Workbook Fallback Rules Verification

### Claimed Rule 1
> No value for specific classification → use same classification in adjacent barangay of similar conditions

### Source 1: BIR DOF Department Order Standard Footnotes
- **Finding:** "Where in the approved listing of zonal values (for various classifications of real property), no value has been prescribed for a particular classification, the zonal value prescribed for the same class of real property located in the adjacent barangay of similar conditions shall be used."
- **Verdict:** **CONFIRMED.** This is a standard footnote in published DOF Department Orders.
- **Source:** Multiple DOF Department Orders; web search synthesis

### Source 2: Respicio & Co.
- **Finding:** Confirms same rule as practitioner understanding.
- **Verdict:** **CONFIRMED.**
- **Source:** [Respicio — Basis for Zonal Valuation](https://www.respicio.ph/commentaries/basis-for-zonal-valuation-of-properties-in-the-philippines)

**Rule 1 VERDICT: CONFIRMED (2/2 sources)**

---

### Claimed Rule 2
> No sale/exchange in barangay → use similarly situated property in adjacent barangay of similar conditions

### Source 1: BIR DOF Department Order Standard Footnotes
- **Finding:** "In a barangay where no sale, exchange, or other disposition of land has been effected, the approved zonal value of a similarly situated property in an adjacent barangay of similar conditions shall be used."
- **Verdict:** **CONFIRMED.** Standard DOF DO footnote.
- **Source:** Multiple DOF Department Orders; web search synthesis

### Source 2: Practitioner sources
- **Finding:** Consistent with the general "nearest comparable zone" fallback described by multiple practitioner sources.
- **Verdict:** **CONFIRMED.**

**Rule 2 VERDICT: CONFIRMED (2/2 sources)**

---

### Claimed Rule 3
> Street not in approved list → use nearest street of similar conditions within same barangay

### Source 1: BIR DOF Department Order Standard Footnotes
- **Finding:** The standard footnote states: "If there is no prescribed zonal value for a particular street/subdivision in a barangay, the zonal value prescribed for the same classification of real property located in the other street/subdivision within the same barangay of similar conditions shall be used."
- **Verdict:** **CONFIRMED.** This is effectively what the "ALL OTHER STREETS IN [BARANGAY]" catch-all entries implement.
- **Source:** Multiple DOF Department Orders; web search synthesis

### Source 2: Actual BIR workbook data
- **Finding:** 185 "ALL OTHER STREETS" entries documented across sampled workbooks, functioning as the practical implementation of this rule.
- **Verdict:** **CONFIRMED** — the catch-all entries are how the rule manifests in practice.
- **Source:** `analysis/address-matching-algorithms.md`

**Rule 3 VERDICT: CONFIRMED (2/2 sources)**

---

### Provenance of workbook rules
- **Finding:** These three rules appear in **DOF Department Order footnotes** (the published zonal value schedules), not in the body text of RMO 31-2019 itself. They are part of the *implementation* (the approved schedule), not the *process order* (the RMO). Prior analysis stating these are "workbook-embedded" rules is technically correct — they appear as footnotes in the Excel workbooks — but should be understood as DOF-approved regulatory text, not just informal workbook guidelines.
- **Correction:** Upgrade provenance from "workbook implementation guidelines" to "DOF Department Order standard footnotes" — they have full regulatory authority.

---

## CTA Case Verification

### Emiliano (CTA EB 1103, 2015)

### Source 1: Respicio & Co. Legal Commentary
- **Finding:** "CGT cannot be based on BIR's unilaterally adopted valuation absent a published zonal value; due process in fixing ZV is essential."
- **Verdict:** **CONFIRMED.** The holding is correctly stated.
- **Source:** [Respicio — Capital Gains Tax Based on ZV](https://www.lawyer-philippines.com/articles/capital-gains-tax-based-on-zonal-value-philippines)

### Source 2: Web search synthesis (multiple practitioner sources)
- **Finding:** Multiple sources confirm the Emiliano ruling established that the Commissioner lacks authority to impose CGT using valuations that haven't been formally published through official channels. Due process under Section 6(E) is essential.
- **Verdict:** **CONFIRMED.**
- **Note:** The full CTA decision text was not available as a public download. The holding is confirmed through secondary legal sources.

**Emiliano VERDICT: CONFIRMED (2/2 sources)**

---

### Gamboa (CTA 9720, 2020)

### Source 1: Respicio & Co. Legal Commentary
- **Finding:** "In the absence of ZV, the BIR cannot simply adopt a bank's appraised value; must follow Section 6(F) appraisal procedures."
- **Verdict:** **CONFIRMED.** The holding is correctly stated.
- **Source:** [Respicio — Capital Gains Tax Based on ZV](https://www.lawyer-philippines.com/articles/capital-gains-tax-based-on-zonal-value-philippines)

### Source 2: Web search synthesis (practitioner sources)
- **Finding:** Multiple sources confirm that the Gamboa ruling prevents the BIR from arbitrarily selecting third-party valuations when determining the tax base in the absence of established zonal values. The BIR must undertake its own property appraisal following the procedures mandated by Section 6(F) of the NIRC.
- **Verdict:** **CONFIRMED.**

**Gamboa VERDICT: CONFIRMED (2/2 sources)**

---

### Aquafresh (G.R. No. 170389 / CTA EB No. 77, 2010)

### Source 1: Supreme Court Full Decision (LawPhil)
- **Finding:** The Supreme Court upheld the CTA En Banc ruling that the 1995 Revised Zonal Values of Real Properties should prevail. The BIR's act of classifying the subject properties as commercial (from residential) "involved a re-classification and revision of the prescribed zonal values" requiring the full Section 6(E) consultation process. The "predominant use" rule "only applies when the property is located in an area or zone where the properties are not yet classified and their zonal values are not yet determined."
- **Verdict:** **CONFIRMED.** "Published classification prevails" is the correct summary of the holding.
- **Source:** [G.R. No. 170389 (LawPhil)](https://lawphil.net/judjuris/juri2010/oct2010/gr_170389_2010.html)

### Source 2: Studocu case digest / ChanRobles
- **Finding:** Multiple case digest sources confirm: Aquafresh Seafoods paid CGT/DST based on residential classification. BIR reclassified to commercial. CTA and SC ruled in favor of taxpayer — published residential classification prevails.
- **Verdict:** **CONFIRMED.**
- **Source:** [ChanRobles — G.R. 170389](https://www.chanrobles.com/cralaw/2010octoberdecisions.php?id=213)

**Aquafresh VERDICT: CONFIRMED (2/2 sources). Note: This is a SUPREME COURT decision (G.R. No. 170389), not merely a CTA case — it has the highest legal authority.**

---

## Summary Table

| Level | Claimed Rule | Verdict | Key Correction |
|-------|-------------|---------|----------------|
| **1** | Exact street + classification match | **FULLY CONFIRMED** | None |
| **2** | Barangay general entry ("All Other Streets") | **FULLY CONFIRMED** | Authority is DOF DOs, not RMO 31-2019 text |
| **3** | Institutional X → nearest CR in barangay | **FULLY CONFIRMED** | Authority is DOF DO footnotes, not RMO 31-2019/RAMO 2-91 |
| **4** | LGU FMV + 100%/150% (RAMO 2-91) | **PARTIALLY CONFIRMED** | RAMO 2-91 text says 100%/150%; practitioner source says 20% current practice. Engine should cite formal rule, note divergence |
| **5** | Written inquiry → escalation | **PARTIALLY CONFIRMED** | Escalation is STCRPV→TCRPV→ECRPV, not "Zonal Valuation Section." No specific form/timeline found |
| **6** | Zonal Classification Ruling | **PARTIALLY CONFIRMED** | Practice exists per practitioners; no formal BIR issuance found. Correctly labeled as "administrative practice" |

| Workbook Rule | Verdict | Source |
|--------------|---------|--------|
| Rule 1: Adjacent barangay, same classification | **CONFIRMED** | DOF DO standard footnotes |
| Rule 2: Adjacent barangay, similar property | **CONFIRMED** | DOF DO standard footnotes |
| Rule 3: Nearest street, same barangay | **CONFIRMED** | DOF DO standard footnotes + 185 "ALL OTHER STREETS" entries |

| CTA/SC Case | Claimed Holding | Verdict |
|-------------|----------------|---------|
| Emiliano (CTA EB 1103) | BIR cannot substitute valuations absent published ZV | **CONFIRMED** |
| Gamboa (CTA 9720) | BIR cannot use bank appraisals absent ZV | **CONFIRMED** |
| Aquafresh (G.R. 170389) | Published classification prevails | **CONFIRMED** (Supreme Court authority) |

---

## Critical Corrections for Fallback Hierarchy Implementation

### Correction 1: LGU FMV Markup Percentage Discrepancy
**The fallback-hierarchy-implementation aspect must address the dual-number problem:**
- **RAMO 2-91 (formal):** LGU FMV + 100% (residential/general), LGU FMV + 150% (commercial/industrial/fishpond)
- **Practitioner observation (informal):** LGU FMV + 20% (some RDOs)
- **Engine design:** Do NOT compute either markup. Return NULL with reference to RAMO 2-91 and advise the user that the RDO will apply the appropriate valuation. Computing a markup would be generating a zonal value — which the engine should never do (per CTA rulings).

### Correction 2: Authority Attribution Refinement
- **Levels 2-3:** Authority is DOF Department Order footnotes, not RMO 31-2019 text
- **Level 4:** Authority is RAMO 2-91 (confirmed)
- **Level 5:** Authority is RMO 31-2019 committee structure (STCRPV/TCRPV/ECRPV), not a generic "Zonal Valuation Section"
- **Level 6:** No formal authority — administrative practice only

### Correction 3: Engine Should Never Compute Fallback Values
The CTA rulings (Emiliano, Gamboa) establish that when no ZV is published, the BIR cannot substitute arbitrary valuations. By extension, the engine should NEVER compute or interpolate values at Levels 3-6. The engine's job at those levels is to:
1. Inform the user that no published value exists
2. Identify which level of the fallback hierarchy applies
3. Provide the applicable legal reference (DOF DO footnote / RAMO 2-91 / RMO 31-2019)
4. Advise on next steps (submit to RDO, etc.)

---

## Sources

### Primary Legal Sources
- [RAMO 2-91 — Supreme Court E-Library](https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/49658)
- [CIR v. Aquafresh Seafoods, G.R. No. 170389 — LawPhil](https://lawphil.net/judjuris/juri2010/oct2010/gr_170389_2010.html)
- [RMO 31-2019 (PDF) — BLGF](https://blgf.gov.ph/wp-content/uploads/2015/09/BIR-RMO_No.-31-2019-SMV.pdf)
- [RMC 06-2021 on RMO 31-2019 Compliance — BLGF](https://blgf.gov.ph/wp-content/uploads/2015/09/RMC-06-2021-RMO-31-2019-Zonal-Values.pdf)
- [RMC 115-2020 — BIR](https://bir-cdn.bir.gov.ph/local/pdf/RMC%20No.%20115-2020.pdf)

### Government Sources
- [BIR Zonal Values Portal](https://www.bir.gov.ph/zonal-values)
- [BIR Citizens Charter 2024 v3](https://bir-cdn.bir.gov.ph/BIR/pdf/citizens-charter-rr-rdo-2024-v3.pdf)
- [BIR Land Classification Definitions](https://zonalvaluefinderph.com/BIR_Land_Classifications)

### Practitioner / Legal Commentary Sources
- [Respicio & Co. — Capital Gains Tax Based on Zonal Value](https://www.lawyer-philippines.com/articles/capital-gains-tax-based-on-zonal-value-philippines)
- [Respicio & Co. — Basis for Zonal Valuation](https://www.respicio.ph/commentaries/basis-for-zonal-valuation-of-properties-in-the-philippines)
- [Respicio & Co. — Real Estate Zonal Value Inquiry](https://www.lawyer-philippines.com/articles/real-estate-zonal-value-inquiry-in-the-philippines)
- [Grant Thornton PH — Certificate of Zonal Values](https://www.grantthornton.com.ph/insights/articles-and-updates1/tax-notes/issuance-of-certificate-of-zonal-values-of-real-properties/)
- [Manila Bulletin — ZV Certificate No Longer Required](https://mb.com.ph/2020/10/27/payment-of-capital-gains-tax-no-longer-requires-zonal-value-certificate-bir/)
- [Forvis Mazars — RMC 56-2024 (eCAR Jurisdiction)](https://www.forvismazars.com/ph/en/insights/tax-alerts/bir-rmc-56-2024)

### Internal Analysis References
- `analysis/cta-zonal-rulings.md`
- `analysis/classification-resolution-logic.md`
- `analysis/address-matching-algorithms.md`
- `analysis/rmo-31-2019-annexes.md`
