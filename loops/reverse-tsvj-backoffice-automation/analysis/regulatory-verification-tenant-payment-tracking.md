# Regulatory Verification Report — Tenant Payment Tracking Rules

**Date:** 2026-02-26
**Context:** SEC-registered PH rental corporation in Las Pinas City, mixed commercial and residential tenants, ~20-100 units
**Scope:** Cross-check 6 regulatory rules extracted during the tenant-payment-tracking analysis against 2+ independent secondary sources each

---

## Rule 1: Monthly Billing Timing — Invoice at Accrual, Receipt at Payment

**Extracted rule:** Under RR 7-2024 (Ease of Paying Taxes Act implementing rules, effective April 27, 2024), the VAT Sales Invoice is the primary BIR document, issued when rent becomes due (accrual basis). Official Receipts are now supplementary, issued upon actual payment receipt. Monthly billing generates invoices; payments generate receipts.

### Verification Status: CONFIRMED

### Source 1: Grant Thornton Philippines — Invoicing Requirements under the EoPT Act
**URL:** https://www.grantthornton.com.ph/insights/articles-and-updates1/lets-talk-tax/invoicing-requirements-under-the-eopt-act/

Grant Thornton confirms that RR No. 7-2024 (effective April 27, 2024) implements the EoPT Act's mandate that the invoice replaces the official receipt as the primary document for sales of services. Section 21 of RA 11976 amends Section 113 of the NIRC to require all VAT-registered persons to issue VAT invoices "for every sale, barter or exchange of goods or services or lease of properties." Official receipts are now supplementary documents only and must be stamped with "This document is not valid for claim of input tax." Grant Thornton further confirms that for long-term contracts (over one year), the invoice shall be issued on the month in which the service or lease of property is made — confirming the accrual-basis timing for lease billing.

### Source 2: PwC Philippines — EoPT Invoicing, Clarified
**URL:** https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2024/eopt-invoicing-clarified.html

PwC confirms the same structural change: "Since sellers of services and lease of properties are now mandated to follow the accrual method of recognizing and recording sales, the EOPT Act and RR No. 3-2024 also mandates the use of Invoice for both sellers of goods/properties and sellers of services/leasing of properties." PwC specifies that invoices must show the total amount inclusive of VAT with the VAT amount as a separate line item, the date of transaction, and the nature of services rendered or lease. PwC also notes that RR 11-2024 amended certain transitional provisions, allowing conversion of unused ORs to invoices by striking through "Official Receipt" and stamping "Invoice."

### Source 3: KPMG Philippines — Clarifications on the Revenue Regulations Implementing the EOPT Act
**URL:** https://kpmg.com/ph/en/home/insights/2024/08/clarifications-on-the-revenue-regulations-implementing-the-eopt-act.html

KPMG confirms the invoicing regime change and the accrual-basis recognition for services/leases. KPMG notes the penalty framework: issuance of ORs as primary documents after April 27, 2024, will be considered tantamount to failure to issue an invoice, subject to a penalty of PHP 1,000 to PHP 50,000 per violation plus criminal penalties.

### Notes
The extracted rule is accurate. One important nuance: the term "Official Receipt" is not eliminated — it can still be issued as a supplementary document upon payment. But the primary billing document for a lease is now the VAT Invoice, issued at accrual (when rent becomes due), not upon collection. This is a significant compliance change that took effect April 27, 2024.

---

## Rule 2: Default Rent Due Date for Controlled Units

**Extracted rule:** Per RA 9653 Section 7, rent for controlled residential units is due within the first 5 days of each month, unless the contract specifies a different schedule.

### Verification Status: CONFIRMED

### Source 1: LawPhil.net — Republic Act No. 9653 (Full Text)
**URL:** https://lawphil.net/statutes/repacts/ra2009/ra_9653_2009.html

The full text of RA 9653 Section 7 states: "Rent shall be paid in advance within the first five (5) days of every current month or the beginning of the lease agreement unless the contract of lease provides for a later date of payment." This directly confirms the extracted rule verbatim.

### Source 2: Supreme Court E-Library — RA 9653
**URL:** https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/25956

The Supreme Court E-Library hosts the official text and confirms the identical language. Section 7 also establishes the deposit and advance rent limits: max 1 month advance rent, max 2 months deposit (to be kept in a bank under the lessor's account), with interest accruing to the lessee.

### Source 3: The Corpus Juris — RA 9653
**URL:** https://thecorpusjuris.com/legislative/republic-acts/ra-no-9653.php

The Corpus Juris legal reference site reproduces the same statutory text and confirms the rule.

### Notes
The extracted rule is accurate. Two nuances worth noting:
1. This provision applies only to **controlled residential units** covered by RA 9653 (monthly rent <= PHP 10,000 in NCR, extended via NHSB resolutions). Commercial tenants and residential tenants above the threshold are governed by contract terms only.
2. The phrase "unless the contract of lease provides for a later date of payment" means the 5-day rule is a **default** (suppletory), not mandatory. Contracts can override with a later date, but cannot impose an earlier one.

---

## Rule 3: VAT Exemption Threshold for Residential Rentals

**Extracted rule:** Per NIRC Section 109(1)(V) as amended by TRAIN (RA 10963) and implemented by RR 13-2018, residential rentals <= PHP 15,000/month per unit are VAT-exempt. If any residential unit exceeds PHP 15,000/month AND combined gross receipts exceed PHP 3M, ALL receipts (commercial + residential) become VAT-able.

### Verification Status: CONFLICT FOUND — The "ALL receipts become VAT-able" claim is incorrect

### Source 1: Respicio & Co. — VAT Liability on Land Lease Income Exceeding 3 Million Philippines
**URL:** https://www.respicio.ph/commentaries/vat-liability-on-land-lease-income-exceeding-3-million-philippines

Respicio & Co. explains the two independent thresholds clearly:
- Residential rentals <= PHP 15,000/month per unit: **VAT-exempt regardless of aggregate gross receipts** (even if total exceeds PHP 3M). This exemption stands as a statutory carve-out.
- Residential rentals > PHP 15,000/month per unit: exempt from VAT only if **aggregate annual gross receipts do not exceed PHP 3M** (subject instead to 3% percentage tax).
- If rentals > PHP 15,000/month AND aggregate > PHP 3M: subject to 12% VAT.

Critically, Respicio clarifies: "Receipts from leases that are independently VAT-exempt by statute (e.g., qualifying low-rent residential units) do not become VATable just because you cross PHP 3M."

### Source 2: ReliaBooks — VAT Exempt Transactions in the Philippines
**URL:** https://reliabooks.ph/what-are-vat-exempt-transactions-in-the-philippines/

ReliaBooks confirms that Section 109(1)(Q) covers residential leases not exceeding PHP 15,000/month. The exemption is per-unit and statutory, not dependent on aggregate receipts.

### Source 3: CPA Davao — Demystifying VAT Exemptions in the Philippines
**URL:** https://www.cpadavao.com/2025/07/Demystifying-VAT-Exemptions-in-the-Philippines-A-Quick-Guide-Based-on-NIRC-and-Key-Republic-Acts.html

CPA Davao provides the BIR's own example from the regulations: "Assuming a lessor has 20 residential units with the same monthly rent per unit [below PHP 15,000] and his accumulated gross receipts during the taxable year amounted to P3,480,000, he is still not subject to VAT even if the accumulated earnings exceeded P3,000,000 since the monthly rent per unit does not exceed P15,000. He is also not subject to 3% Percentage Tax."

### Source 4: LMA Law — On 2018 VAT Regulations Part 2
**URL:** https://lmalaw.org/index.php/blog/item/26-on-2018-vat-regulations

LMA Law provides a worked example from RR 13-2018 showing how mixed-use lessors are treated. The example shows accumulated gross receipts of PHP 5,460,000 (PHP 3,600,000 commercial + PHP 1,860,000 residential where residential rents exceed PHP 15,000/month) — this is VAT-able because the residential rents **exceed** PHP 15,000/month and the aggregate exceeds PHP 3M. But crucially, this only happens because the residential per-unit threshold is already exceeded.

### Notes
**The extracted rule contains a significant error.** The correct rule is:

| Scenario | Monthly Rent Per Unit | Aggregate Annual Gross | VAT Treatment |
|----------|----------------------|----------------------|---------------|
| A | <= PHP 15,000 | Any amount (even > PHP 3M) | **VAT-exempt** (also exempt from 3% OPT) |
| B | > PHP 15,000 | <= PHP 3,000,000 | **VAT-exempt** (but subject to 3% OPT) |
| C | > PHP 15,000 | > PHP 3,000,000 | **Subject to 12% VAT** |

The claim that "if any residential unit exceeds PHP 15,000/month AND combined gross receipts exceed PHP 3M, ALL receipts (commercial + residential) become VAT-able" is **partially wrong**:
1. Commercial receipts above the PHP 3M threshold are independently VAT-able — this is true.
2. Residential receipts at or below PHP 15,000/month remain VAT-exempt **regardless** — the statutory exemption is not overridden by the aggregate threshold.
3. Only residential units with rents **exceeding** PHP 15,000/month get pulled into the VAT-able pool when the aggregate exceeds PHP 3M.

For a mixed-use lessor, the practical effect is: commercial rents + high-rent residential units (> PHP 15,000) count toward the PHP 3M threshold. Low-rent residential units (<= PHP 15,000) are carved out permanently.

**Also note:** The NIRC section reference should be Section 109(1)(Q) for residential lease exemption (as renumbered by TRAIN), not Section 109(1)(V). The previous analysis-log entry from the `corporate-rental-tax` aspect referenced the "mixed-use trap" language that propagated this error. This verification corrects it.

---

## Rule 4: Sequential Invoice Numbering Requirement

**Extracted rule:** Per NIRC Section 237 and RR 18-2012, BIR-registered invoices must have sequential, gapless numbering. Each establishment maintains its own series. Gaps create audit risk.

### Verification Status: CONFIRMED

### Source 1: Tax and Accounting Center, Inc. — BIR Official Receipts and Sales Invoices in the Philippines
**URL:** https://taxacctgcenter.ph/bir-official-receipts-and-sales-invoices-in-the-philippines/

Confirms that NIRC Section 237 requires all receipts/invoices to be "serially numbered" and that they must show the name, business style, TIN including the branch code, business address, and other required information. The serial number and booklet number are mandatory under RR 18-2012.

### Source 2: Respicio & Co. — Lost Sales Invoice: BIR Reporting Requirements
**URL:** https://www.lawyer-philippines.com/articles/lost-sales-invoice-bir-reporting-requirements-penalties-and-replacement-philippines

Respicio confirms that gaps in invoice sequences create audit risk. Lost invoices must be reported via a notarized Affidavit of Loss detailing the serial range, ATP details, and circumstances. During audit, inability to present duplicates can be treated as a books/records deficiency and may support "failure to issue" or "underdeclaration" theories. The penalty under Section 264(a) is PHP 1,000–50,000 fine plus 2–4 years imprisonment.

### Source 3: DBP-hosted RR 18-2012 PDF
**URL:** https://www.dbp.ph/wp-content/uploads/2018/05/13BIRRR18_2012.pdf

The full text of RR 18-2012 governs the processing of Authority to Print (ATP) for official receipts, sales invoices, and other commercial invoices via the online ATP system. It mandates specific serial number ranges per ATP application and requires each establishment (branch) to maintain its own series using the branch code suffix (000 for head office, 001+ for branches).

### Notes
The extracted rule is accurate. The term "gapless" deserves precision: the BIR does not literally require zero gaps — voided invoices are permissible if properly documented (marked "VOID" on all copies, reported in Summary List of Sales, retained for audit). The risk is from **unaccounted** gaps, not from properly voided entries. The BIR can suspend or close a business (Oplan Kandado) under NIRC Section 115 for failure to issue invoices. Post-EOPT, the term "invoice" is now the universal primary document (replacing official receipts for services/leases), but the sequential numbering requirement carries over unchanged.

---

## Rule 5: Billing Statement Content Requirements for Sub-Metered Utilities

**Extracted rule:** Per MWSS RO regulations and ERC guidelines, utility billing statements to tenants must include: opening/closing meter readings, consumption, rate breakdown per tier (water) or per-kWh rate (electric), line-item charges, and total due. Water bills must also show how tenant's share derives from master bill.

### Verification Status: CONFIRMED WITH NUANCE — General principles confirmed but no single prescriptive MWSS circular exists for tenant billing format

### Source 1: Respicio & Co. — Landlord Overcharging on Submetered Utilities
**URL:** https://www.respicio.ph/commentaries/landlord-overcharging-on-submetered-utilities-in-the-philippines

Respicio confirms the pass-through principle: "Building owners, condominium corporations, or HOAs that use submetering systems are generally not permitted to charge tenants or residents more than what the distribution utility charges at the main meter." The article confirms that landlord/building administrator obligations include: "Display or deliver the full utility bill within five (5) days of receipt. Provide an itemized breakdown — kWh consumed x DU tariff + VAT + systems loss — matching the bill exactly." It also confirms tenants have "the right to inspect and photograph both mother- and sub-meter readings at any reasonable time" and that records must be maintained for 3 years (ERC Res. 12-2004, Section 11).

### Source 2: Respicio & Co. — Tenant Rights on Water Submeter Billing
**URL:** https://www.lawyer-philippines.com/articles/tenant-rights-on-water-submeter-billing

For water specifically, Respicio confirms that landlords must provide tenants with "a breakdown of water charges, including the basic rate, environmental fee, and VAT." Charges should align with the rates imposed by the main water utility provider (Maynilad). The per-tenant computation should start at the lowest tier, not blended master average. Sub-meters require Maynilad approval and PNS/BPS certification.

### Source 3: MWSS RO FOI Response (2023) — via respicio.ph commentary
**URL:** https://www.foi.gov.ph/requests/latest-official-circular-on-subdivision-mother-meter-billing-scheme/

A 2023 Freedom of Information request to the MWSS Regulatory Office revealed that "the MWSS Regulatory Office has not issued any circular as to how much should be collected or charged to homeowners of a subdivision served by Manila Water through a bulk water supply arrangement." The MWSS RO's jurisdiction extends only to the master meter; billing beyond the master meter falls under the developer/landlord's responsibility, governed by the MOA with the concessionaire and general consumer protection law.

### Source 4: ERC Resolution No. 12, Series of 2009
**URL:** (Referenced in Supreme Court E-Library: https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/67751)

ERC Resolution 12 (2009) primarily governs "Rules and Procedures for the Test and Maintenance of Electric Meters of Distribution Utilities." While it establishes meter accuracy standards and calibration requirements (relevant to sub-meters), it does not prescribe a specific billing statement format for landlord-to-tenant billing. The pass-through principle and disclosure requirements are derived from a combination of ERC resolutions (including Res. 12-2009 and Res. 08-2022), the Magna Carta for Residential Electricity Consumers, and general consumer protection principles.

### Notes
The extracted rule is **directionally correct** but overstates the specificity of the regulatory mandate. The key nuances:

1. **Electric billing:** The ERC's pass-through principle and disclosure requirements are well-established through multiple resolutions and case law (e.g., ERC Case No. 2013-091). Landlords must provide itemized breakdowns matching the DU tariff. However, there is no single ERC circular that prescribes a specific billing statement template for landlord-to-tenant billing.

2. **Water billing:** The MWSS RO has **not** issued a prescriptive circular for tenant billing format. The billing requirements are derived from: (a) the general pass-through principle, (b) Maynilad/Manila Water concession terms, (c) consumer protection law requiring transparency, and (d) the specific MOA between the concessionaire and the building owner. The statement that "water bills must also show how tenant's share derives from master bill" is a best-practice recommendation, not a specific MWSS regulatory requirement.

3. **Tier-based billing for water:** The correct method is to bill each tenant starting from the lowest tier based on their individual consumption, **not** to apply a blended average rate from the master meter. This is per MWSS RO's billing scheme policy (MWSS RO-OPP-052-04).

4. **Record retention:** ERC requires 3 years of records; failure to keep records creates a presumption of overcharging.

The practical recommendation stands: billing statements **should** include meter readings, consumption, rate breakdown, and line-item charges for compliance and dispute avoidance. But the regulatory basis is a composite of principles rather than a single prescriptive regulation.

---

## Rule 6: Output VAT on Accrual Basis with Credit for Uncollected Receivables

**Extracted rule:** Output VAT must be declared when the invoice is issued (accrual basis), not when payment is received. Under RR 3-2024, there is an "Output VAT Credit on Uncollected Receivables" mechanism if rent is not collected within the agreed credit term.

### Verification Status: CONFIRMED

### Source 1: PwC Philippines — Navigating VAT Recovery under the EoPT Act
**URL:** https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2024/navigating-vat-recovery-under-the-eopt-act.html

PwC confirms: "The EoPT Act introduced the use of output VAT credits for uncollected receivables in the subsequent quarter after they become overdue." PwC explains that Section 110(D) of the NIRC (added by RA 11976) allows a seller to "deduct the output VAT pertaining to uncollected receivables from its output VAT on the next quarter, after the lapse of the agreed upon period to pay." PwC notes this is optional — sellers may choose not to claim it if receivables are likely to be collected. PwC also identifies a practical challenge: "the subsequent monitoring of VAT credits creates a particularly onerous challenge to taxpayers."

### Source 2: Grant Thornton Philippines — BIR Clarifies Availment of Output VAT Credit on Uncollected Receivables
**URL:** https://www.grantthornton.com.ph/insights/articles-and-updates1/tax-notes/eopt-is-here-bir-clarifies-availment-of-output-vat-credit-on-uncollected-receivables/

Grant Thornton confirms the mechanism under RMC 65-2024 (issued June 13, 2024). Key conditions: (1) the sale must be on credit and must have transpired after April 27, 2024; (2) there must be a **written agreement** on the credit term, indicated on the invoice or supporting document; (3) the sale must be specifically reported in the Summary List of Sales (not as "various"); (4) the VAT must have been fully declared; (5) the agreed period must have lapsed; (6) the VAT component must not have been claimed as a bad debt deduction under Section 34(E). Grant Thornton confirms the credit can only be claimed **once**, in the next quarter after the credit term lapses.

### Source 3: Deloitte Philippines — Managing Output VAT Credit
**URL:** https://www.deloitte.com/southeast-asia/en/services/tax/perspectives/managing-output-vat-credit.html

Deloitte confirms the accrual-basis shift and the Section 110(D) credit mechanism. Deloitte emphasizes the recovery requirement: "In case of recovery of uncollected receivables, the output VAT pertaining thereto shall be added to the output VAT of the taxpayer during the period of recovery." Deloitte also notes the transitional rule: for outstanding receivables on services prior to April 27, 2024, the output VAT is still declared upon collection (old cash-basis rule), not retroactively shifted to accrual.

### Source 4: BIR RR 3-2024 (Official Text)
**URL:** https://bir-cdn.bir.gov.ph/BIR/pdf/RR%203-2024%20(final).pdf

The official BIR regulation text confirms all the above. Section 4.110-9 establishes the Output VAT Credit on Uncollected Receivables mechanism. The regulation took effect April 27, 2024.

### Notes
The extracted rule is accurate. Key additional details for implementation:

1. **Written agreement is mandatory:** For a rental corporation, the lease contract serves as the written agreement. The credit term should be clearly stated (e.g., "rent due within 5 days of the month" establishes the credit term). If the lease does not specify a payment period, the credit may be difficult to claim.

2. **One-quarter window:** The credit can only be claimed in the **next quarter** after the agreed period lapses. If not claimed in that quarter, the opportunity is lost (cannot be carried forward).

3. **Recovery reversal:** If the tenant eventually pays, the previously credited output VAT must be added back in the quarter of recovery. This creates a tracking obligation.

4. **Stamp requirement:** The seller must stamp "Claimed Output VAT Credit" on duplicate/triplicate copies of the invoice for the uncollected receivable.

5. **Buyer impact:** When the seller claims the credit, the buyer's corresponding input VAT is disallowed. For rental tenants who are VAT-registered, this means their input VAT claim on the rent is reversed if the landlord claims the uncollected receivable credit.

6. **April 27, 2024 effectivity:** Only applies to transactions from this date forward. Pre-existing receivables on services/leases follow the old cash-basis rule (declare VAT upon collection).

---

## Summary Table

| Rule | Status | Key Finding |
|------|--------|-------------|
| 1. Invoice at accrual, receipt at payment (RR 7-2024) | **Confirmed** | Three Big 4 firms confirm. Invoice is primary document for leases from April 27, 2024. OR is supplementary only. |
| 2. Rent due within first 5 days (RA 9653 Sec. 7) | **Confirmed** | Verified against statutory text on lawphil.net and two legal reference sites. Default rule for controlled units; contract can specify later date. |
| 3. VAT exemption: <=PHP 15K/unit exempt; >PHP 15K + >PHP 3M = all VAT-able | **Conflict found** | The "ALL receipts become VAT-able" claim is **wrong**. Low-rent residential units (<=PHP 15K/month) are a permanent statutory carve-out — they remain VAT-exempt even if the lessor's aggregate exceeds PHP 3M. Only units exceeding PHP 15K/month combine with commercial receipts for threshold testing. |
| 4. Sequential invoice numbering (NIRC 237 + RR 18-2012) | **Confirmed** | Serial numbering mandatory. Each establishment has its own series. Gaps must be documented (voided or lost — affidavit required). Unaccounted gaps = audit risk. |
| 5. Utility billing statement content (MWSS + ERC) | **Confirmed with nuance** | Pass-through principle and transparency requirements are well-established. However, no single MWSS or ERC circular prescribes a specific billing statement template for landlord-to-tenant utility billing. The requirements are derived from a composite of regulations, case law, and consumer protection principles. |
| 6. Output VAT accrual + credit for uncollected receivables (RR 3-2024) | **Confirmed** | Full mechanism verified across PwC, Grant Thornton, Deloitte, and the official BIR text. Key: requires written agreement, one-quarter claim window, recovery reversal obligation, stamp requirement. Effective only for transactions from April 27, 2024. |

---

## Action Items for Parent Analysis

1. **Correct Rule 3 in the corporate-rental-tax input file** (`input/corporate-rental-tax.md`): The "mixed-use trap" language stating that ALL receipts become VAT-able is incorrect. Low-rent residential units (<=PHP 15K/month) are permanently carved out.
2. **Update NIRC section reference**: The residential lease VAT exemption is Section 109(1)(Q) (post-TRAIN renumbering), not Section 109(1)(V).
3. **For billing system design**: Ensure the output VAT credit mechanism (Rule 6) is accounted for in the receivables tracking system — it requires a written credit term, one-quarter claim window, and recovery reversal tracking.
4. **For utility billing design**: Even without a prescriptive template, the billing statement should include meter readings, consumption, rate breakdown, and derivation from master bill as a compliance best practice.
