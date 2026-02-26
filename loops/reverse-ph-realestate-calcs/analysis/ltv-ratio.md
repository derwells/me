# LTV Ratio — Verification & Cross-Check Report

**Aspect:** ltv-ratio (Wave 2)
**Date:** 2026-02-26
**Type:** Independent verification of extracted LTV computation rules
**Sources consulted:** 15+ independent sources across 5 categories (see Section 6)
**Methodology:** Cross-checked each claim from primary extraction against 3-5 secondary sources

---

## 1. Claim-by-Claim Verification

### Claim 1: Collateral Value = min(Appraised Value, Selling Price) — universally applied?

**Verdict: CONFIRMED**

This principle is confirmed across all source categories:

- **Pag-IBIG (HDMF):** The Respicio.ph practitioner guide explicitly states Pag-IBIG uses the "lower of two values: Total Contract Price (TCP) and Pag-IBIG Appraisal." The loanable amount is then calculated as a percentage of this lower figure. (Source: respicio.ph/commentaries/pag-ibig-housing-loan-equity-basis-philippines)
- **Pag-IBIG official:** The Pag-IBIG Fund website states the loan amount is based on the *lowest* among: actual need (selling price), capacity to pay, and loan-to-appraisal value. (Source: pagibigfund.gov.ph/availmentofnewloan.html)
- **Commercial banks:** The BSP input file states "Always base loanable amount on the lower of appraised value or selling price." The RichestPH practitioner guide confirms "If the bank's appraiser values the condo at less than what you've agreed to pay, you have a few options." (Source: richestph.com)
- **SSS Housing Loan:** Similar principle: loanable amount based on appraised value of collateral (70%-90%), borrower capacity, and actual need — lowest governs. (Source: SSS housing loan guidelines via search results)
- **General principle:** Standard mortgage practice globally and in PH — lender bases LTV on lower of appraised value or contract price to protect collateral interest.

**Edge case — When appraised value > selling price:** The collateral value defaults to the selling price. The borrower does NOT get credit for the higher appraisal. This protects the lender against inflated purchase prices but also prevents over-leverage on underpriced deals. Multiple sources confirm this consistently.

**Edge case — When selling price > appraised value:** The collateral value defaults to the appraised value. The borrower must cover the gap between selling price and loanable amount as additional equity/down payment. This is the more common scenario and is well-documented.

---

### Claim 2: Pag-IBIG Retail LTV Tiers (100/90/80) under "Circular 443"

**Verdict: CONFLICT — Major circular number error; LTV tiers partially confirmed but require correction**

**Critical finding:** Circular No. 443 is NOT a housing circular. According to the Scribd-hosted list of Pag-IBIG circulars, Circular 443 falls under the *Provident* division and is titled "Amended Guidelines on the Treatment and Release of the Pag-IBIG Fund Residual Total Accumulated Value (RTAV)." It contains no LTV provisions whatsoever.

The actual governing circulars for LTV are:
- **Circular No. 396** (modified EUF guidelines) — foundational
- **Circular No. 402** (LTV and capacity-to-pay determination) — amended LTV provisions of Circular 396
- **Circular No. 473** (current Regular Housing Loan Program, 2021) — reconfirmed equity floors
- **Circular No. 474** (Affordable Housing Program, 2021)

**The LTV tiers extracted need correction.** The primary extraction listed this "Circular 443 era" table:

| Collateral Value | Extracted LTV | Status |
|---|---|---|
| Up to P400,000 | 100% | CONFLICT |
| P400,001-P1,250,000 | 90% | CONFLICT |
| P1,250,001-P6,000,000 | 80% | CONFLICT |

The **actual current framework** (Circular 402 / Circular 473) uses a different structure entirely, based on housing category rather than peso-amount tiers:

| Loan Category | LTV Ratio | Source |
|---|---|---|
| Up to Socialized Housing Loan Ceiling | 100% (developer-assisted) | Circular 402, 403 |
| Up to Economic Housing Limit (~P2.5M) | 95% | Circular 402, Respicio.ph |
| Over Economic Housing Limit up to P6M | 90% | Circular 402, omnicalculator.com |
| Residential Lot only (no house) | 70% | Respicio.ph, multiple practitioner sources |

**Alternative view from Respicio.ph** (may reflect older or simplified interpretation):

| Loan Amount | Max LTV | Min Equity |
|---|---|---|
| Up to P500K | 95% | 5% |
| P500K-P2M | 90% | 10% |
| P2M-P6M | 80% | 20% |
| Residential lots only | 70% | 30% |

**Assessment:** The "100/90/80" tiers in the primary extraction appear to be a simplified practitioner interpretation that merges different circular provisions. The peso thresholds (P400K, P1.25M, P6M) do not correspond to any single circular's table. The actual current system is category-based (socialized / economic / open market) with LTV caps of 100/95/90, not 100/90/80.

---

### Claim 3: Pag-IBIG Buyback Guaranty LTV Tiers (100/100/95/90)

**Verdict: CONFIRMED with corrections — these are from an OLDER circular, not current**

The buyback guaranty LTV table is confirmed by an authoritative source (LegalDex.com, extracting HDMF Circular No. 247-09):

| Loan Amount | With Buyback Guaranty | Without Buyback (Retail) |
|---|---|---|
| Up to P400,000 | 100% | 100% |
| P400,001-P750,000 | 100% | 90% |
| P750,001-P1,250,000 | 95% | 85% |
| P1,250,001-P3,000,000 | 90% | 80% |

**The primary extraction's "retail" table had:** 100/90/90/80 (for the same brackets). The verified table shows the retail column is actually 100/90/**85**/80 — the P750K-P1.25M bracket is 85%, not 90%.

**Important context:** This table is from the **older EUF circular era** (Circular 247-09 and successors, when the maximum loan was P3M). The current Circular 402/473 framework (P6M maximum) uses the category-based system described in Claim 2 above. The buyback-guaranty-vs-retail distinction appears to have been **largely superseded** by the current simplified category-based approach, though the buyback guaranty mechanism itself still exists for developer-assisted loans.

---

### Claim 4: PH Has No Hard Regulatory LTV Cap (Unlike SG/HK/KR)

**Verdict: PARTIALLY CONFIRMED — Nuanced**

The situation is more complex than a simple "no cap":

**What exists:**
1. **General Banking Act (RA 8791), Section 37:** Statutory cap of 75% of appraised value of real estate + 60% of appraised value of insured improvements. This IS a hard legal lending limit, directly in the statute. HOWEVER, Section 42 empowers the Monetary Board to increase or decrease these ratios.
2. **BSP Circular 855 (2014):** 60% collateral valuation cap for classification/provisioning purposes. This is explicitly NOT a lending cap. The BSP FAQ confirms: "The collateral cap will not preclude FIs from granting loans with loan-to-collateral value ratios in excess of 60%."
3. **BSP Circular 688 (2010):** Introduced macroprudential LTV ceilings — 60% for non-residential, 80% for residential. The exact binding nature is unclear; banks routinely lend above 80% for residential.

**How PH differs from SG/HK/KR:**
- **Singapore:** Hard, tiered, frequently-adjusted LTV limits (75% first property, 45% second, 35% third+) enforced by MAS. Plus TDSR cap at 55%.
- **Hong Kong:** Hard, tiered LTV limits (70% for properties <HK$30M, 60% for >HK$35M; 60% for non-self-use) enforced by HKMA.
- **Korea:** Hard LTV limits varying by region (40-70%) actively adjusted as countercyclical tool.
- **Philippines:** The Section 37 cap of 75%+60% exists as a statutory limit, but banks and Pag-IBIG routinely offer 80-95% LTV. This is likely enabled by the Monetary Board's power under Section 42 to "increase the maximum ratios" in special cases, or through the interpretation that government housing programs (Pag-IBIG) are not covered by the same banking regulations.

**IMF FSAP 2022 assessment:** The IMF noted that the BSP has LTV as a tool but uses it from a microprudential (not macroprudential/countercyclical) perspective. The IMF recommended the BSP "consider the modernization of its policy toolkit" and adopt "time-varying tools such as LTV and DTI." This implies the existing LTV framework is not actively managed as a binding macroprudential tool in the way SG/HK/KR operate theirs.

**Net assessment:** The claim that PH has "NO hard regulatory LTV cap" is an **oversimplification**. A statutory cap exists (Section 37: 75%+60%), but it is effectively non-binding in practice because:
- The Monetary Board has power to increase it
- Pag-IBIG (a government fund, not a bank) operates under its own circulars
- BSP Circular 855's 60% is explicitly a provisioning measure, not a lending cap
- Banks routinely lend at 80-90% without regulatory sanction

---

### Claim 5: General Banking Act Sec. 37 States 75% + 60%

**Verdict: CONFIRMED**

Direct quote from RA 8791 Section 37: "loans and other credit accommodations against real estate shall not exceed seventy-five percent (75%) of the appraised value of the respective real estate security, plus sixty percent (60%) of the appraised value of the insured improvements."

Confirmed across multiple sources:
- BSP official PDF: bsp.gov.ph/Regulations/Banking%20Laws/gba.pdf
- Supreme Court E-Library: elibrary.judiciary.gov.ph/thebookshelf/showdocs/2/5339
- LawPhil: lawphil.net/statutes/repacts/ra2000/ra_8791_2000.html
- Baker McKenzie Asia Pacific Guide to Lending and Taking Security (Philippines chapter)

**Additional context confirmed:** The predecessor statute (RA 337, old General Banking Act) had a lower limit of 70% for real estate and 50% for chattels. RA 8791 increased these to 75% and 60% respectively.

The Monetary Board retains power under Section 42 to adjust these ratios up or down.

---

### Claim 6: Expanded 4PH Program (Circular 473) — Different LTV Rules?

**Verdict: PARTIALLY CONFIRMED — different interest rates, not fundamentally different LTV**

**What Circular 473 governs:**
- End-User Home Financing (EUF) under the Expanded 4PH (Pambansang Pabahay para sa Pilipino) program
- OFWs may qualify for socialized housing regardless of income
- Subsidized interest rate: 3% for first 5 years, extendable to 10 years for eligible borrowers

**LTV under 4PH:**
- Socialized housing units financed under 4PH follow the same LTV framework as the AHP (Circular 474): up to 100% LTV for loans within the socialized housing loan ceiling
- The key benefit of 4PH is the interest rate subsidy (3% vs. standard 5.75%+), not a different LTV structure
- Updated price ceilings: horizontal units up to P844,440-P950,000; vertical (condo) units up to P1.8M-P2.0M (NCR/HUC with zonal value add-on)

**No independent LTV table for 4PH was found** in any source. The program appears to inherit the AHP LTV framework for socialized units.

---

### Claim 7: Do Any Banks Advertise LTV Above 90%? (UnionBank 99%?)

**Verdict: CONFIRMED — but with important caveats**

**UnionBank:** Multiple independent sources confirm UnionBank advertises financing "up to 99% of the property's value." However, there is inconsistency:
- n90.asia states UnionBank offers "up to 99% of the property's value"
- Other sources (MoneyMax, CashMart) reference "up to 90% of the property's appraised value"
- UnionBank's own loan calculator references a minimum down payment of "10% to 99%"

**Interpretation:** The "99%" likely refers to the *down payment flexibility range* (borrower can choose 10% to 99% down payment), meaning the bank finances anywhere from 1% to 90%. The actual maximum LTV appears to be 90% in standard practice. The "99% financing" claim may apply to specific developer-partnered products with enhanced terms.

**Other banks for comparison:**
| Bank | Max LTV (House & Lot) | Max LTV (Condo) | Max LTV (Vacant Lot) |
|---|---|---|---|
| BPI | 90% | 60% | 60% |
| BDO | 80% | 70% | 70% |
| Metrobank | 80% (90% accredited developer) | 80% | Varies |
| UnionBank | 90% (up to 99% claimed) | Varies | Varies |
| Maybank | 90% | 90% | 60% |
| AllBank | 90% | Varies | Varies |
| RCBC | 80% | Varies | Varies |
| PNB | 80-90% | Varies | Varies |

**Key finding:** No bank was confirmed to routinely offer above 90% LTV as a standard product. Claims of 95-99% appear to be marketing/edge cases for specific developer tie-ups.

---

### Claim 8: Separate LTV Framework for Condominiums vs. House-and-Lot?

**Verdict: CONFIRMED — condos typically get lower LTV**

Multiple sources confirm banks apply different (lower) LTV ratios for condominiums vs. house-and-lot:

- **BDO:** 80% for house-and-lot vs. 70% for condominiums
- **BPI:** 90% for house-and-lot vs. 60% for condominiums
- **Maybank:** 90% for both house-and-lot and condominiums (exception)
- **General market:** "Banks in the Philippines generally offer lower LTV ratios for condominiums compared to house and lot properties" (multiple sources)

**Reasons cited for lower condo LTV:**
1. **Depreciation risk** — building structure ages; unlike house-and-lot where land appreciates
2. **Complex collateral assessment** — shared common areas, condominium corporation dynamics
3. **Market volatility** — condo values more volatile, especially in oversupplied markets
4. **Pre-selling risk** — pre-selling condos receive even lower LTV due to completion risk

**Vacant lots** receive the lowest LTV across all sources:
- BPI: 60%
- Maybank: 60%
- Pag-IBIG: 70%
- General practice: 60-70%

**Pag-IBIG distinction:** The Pag-IBIG LTV framework does NOT appear to differentiate by property type (condo vs. house-and-lot) within its category-based system. The LTV is driven by loan amount category (socialized/economic/open market), not property type. However, for residential lots only, a separate 70% LTV applies.

---

## 2. Additional Findings Not in Primary Extraction

### 2a. Affordable Housing Program (AHP) — 0% Equity

Under Circular 474 (2021), loans up to P580,000 under the AHP qualify for 100% LTV (0% equity). This is a distinct program from the regular EUF and was not captured in the primary extraction's LTV tables.

### 2b. Green Housing Loans — Potential Future LTV Changes

Future Pag-IBIG pilot (expected 2024-2025) may adopt a higher LTV ceiling of up to 97% for certified eco-friendly homes (EDGE/Berde certified). Not yet confirmed as active policy.

### 2c. 70% LTV Threshold for Buyback Exemption

Under the older EUF framework, a loan secured by First REM (instead of Contract to Sell) could be exempted from the buyback guaranty requirement if the loan-to-collateral ratio does not exceed 70%. This is a distinct threshold from the standard LTV tiers.

### 2d. BSP Rediscounting Cap

MORB Appendix 36 caps BSP rediscounting availments against a mortgaged property at 80% of collateral value. This affects banks' cost-of-funds for housing loans but is not a consumer-facing LTV limit.

### 2e. Insurance Value Computation

FGI/FAPI insurance uses a separate "min" calculation: insured value = lower of (appraised value of housing component) or (loan amount). This is distinct from the LTV collateral value computation.

---

## 3. Corrections to Primary Extraction

### Correction 1: Wrong Circular Number
The primary extraction attributes the retail LTV tiers to "Circular 443." This is incorrect. Circular 443 is a provident (savings) circular, not housing. The correct governing circulars are:
- **Circular 402** (LTV determination rules)
- **Circular 473** (current regular housing loan program)
- **Older framework:** Circular 247-09 / Circular 396 (buyback-vs-retail tables)

### Correction 2: Retail LTV Table Is From Older Era
The "retail (no buyback guaranty)" table with tiers at P400K/P750K/P1.25M/P3M is from the older EUF era (Circular 247-09). The current framework under Circular 402/473 uses category-based LTV (socialized 100% / economic 95% / over-economic 90%).

### Correction 3: Retail P750K-P1.25M Bracket
The primary extraction shows 90% for retail at P750K-P1.25M. The verified figure from LegalDex/Circular 247-09 is 85%.

### Correction 4: BSP "No Hard LTV Cap" Oversimplification
Section 37 of RA 8791 IS a statutory lending limit (75% + 60%). The claim should be refined to: "PH does not actively use LTV as a countercyclical macroprudential tool in the manner of SG/HK/KR, and the statutory Section 37 limit is effectively non-binding in practice for housing due to Monetary Board override authority and Pag-IBIG's separate regulatory framework."

### Correction 5: BSP Circular 688 Characterization
The primary extraction states Circular 688 thresholds "appear to be monitoring thresholds, not hard lending caps." The evidence is ambiguous — the circular text was not fully accessible (scanned PDF). What IS confirmed is that BSP Circular 855 (2014) subsequently established the 60% collateral valuation cap as a classification/provisioning measure, explicitly not a lending cap. Circular 688's provisions may have been effectively superseded by Circular 855's framework.

---

## 4. Verified LTV Computation Model

### Core Formula (Confirmed)
```
Collateral_Value = min(Appraised_Value, Selling_Price)
Max_Loanable_Amount = LTV_Cap% * Collateral_Value
Actual_Loan = min(Max_Loanable_Amount, Capacity_to_Pay_Cap, Loan_Entitlement, Actual_Need)
```

### Pag-IBIG LTV Schedule (Current — Circular 402/473)
```
IF housing_program == "AHP" AND loan_amount <= Socialized_Housing_Ceiling:
    LTV = 100%
ELIF housing_program == "AHP" AND loan_amount <= 750,000:
    LTV = 95%
ELIF collateral_value <= Economic_Housing_Limit:   # ~P2,499,999.99
    LTV = 95%
ELIF collateral_value <= 6,000,000:
    LTV = 90%
ELIF property_type == "lot_only":
    LTV = 70%
```

### Pag-IBIG LTV Schedule (Older — Circular 247-09, for reference)
```
# With Buyback Guaranty
IF loan_amount <= 400,000:       LTV = 100%
ELIF loan_amount <= 750,000:     LTV = 100%
ELIF loan_amount <= 1,250,000:   LTV = 95%
ELIF loan_amount <= 3,000,000:   LTV = 90%

# Without Buyback Guaranty (Retail)
IF loan_amount <= 400,000:       LTV = 100%
ELIF loan_amount <= 750,000:     LTV = 90%
ELIF loan_amount <= 1,250,000:   LTV = 85%
ELIF loan_amount <= 3,000,000:   LTV = 80%
```

### Commercial Bank LTV (Market Practice, not hard regulation)
```
IF property_type == "house_and_lot" AND developer_tier == "top" AND purpose == "primary_residence":
    LTV = 80%-90%   # Bank-specific, BPI/Maybank/AllBank at 90%
ELIF property_type == "house_and_lot":
    LTV = 70%-80%   # BDO at 80%, RCBC at 80%
ELIF property_type == "condo" AND purpose == "own_occupancy":
    LTV = 60%-80%   # BPI at 60%, BDO at 70%, Metrobank at 80%
ELIF property_type == "vacant_lot":
    LTV = 60%-70%   # BPI at 60%, Maybank at 60%, Pag-IBIG at 70%
ELIF purpose == "investment" OR purpose == "secondary_home":
    LTV = 60%
```

---

## 5. Confidence Assessment

| Claim | Verdict | Confidence | Sources |
|---|---|---|---|
| Collateral = min(appraised, selling) | CONFIRMED | HIGH (5/5 source categories) | Pag-IBIG, BSP, banks, practitioners, SSS |
| Pag-IBIG retail LTV 100/90/80 under "Circular 443" | REJECTED — wrong circular #; outdated tiers | HIGH | Scribd circulars list, Circular 402, e-Library |
| Pag-IBIG buyback LTV 100/100/95/90 | CONFIRMED — but from older circular | HIGH | LegalDex (Circular 247-09), Respicio.ph |
| PH has no hard regulatory LTV cap | PARTIALLY CONFIRMED — nuanced | MEDIUM | RA 8791 Sec 37, BSP FAQ C855, IMF FSAP 2022 |
| GBA Sec 37: 75% + 60% | CONFIRMED | HIGH | BSP official text, LawPhil, Supreme Court E-Library |
| Expanded 4PH different LTV | NOT CONFIRMED — uses AHP/regular framework | MEDIUM | PNA, DHSUD, search results |
| Banks above 90% LTV (UnionBank 99%) | PARTIALLY CONFIRMED — marketing claim, actual likely 90% | MEDIUM | n90.asia, MoneyMax, UnionBank site |
| Separate condo vs house-and-lot LTV | CONFIRMED | HIGH | BDO, BPI, Maybank, practitioner guides |

---

## 6. Sources Consulted

### Category 1: Pag-IBIG Official / Legal
1. Pag-IBIG Circular No. 402 — via Supreme Court E-Library (elibrary.judiciary.gov.ph)
2. Pag-IBIG Circular No. 403 — via Supreme Court E-Library
3. Pag-IBIG Circular No. 247-09 — via LegalDex (legaldex.com)
4. Pag-IBIG Fund official website (pagibigfund.gov.ph/availmentofnewloan.html)
5. Pag-IBIG Circulars list — via Scribd (scribd.com/document/942639624)

### Category 2: BSP Regulations
6. RA 8791 (General Banking Law) Section 37 — via BSP official PDF (bsp.gov.ph)
7. BSP Circular 855 FAQ — via BSP website (bsp.gov.ph/Regulations/FAQ/FAQ_C855.pdf)
8. BSP MORB Section 303 — via morb.bsp.gov.ph
9. BSP Circular 688 — via BSP website (bsp.gov.ph/Regulations/Issuances/2010/c688.pdf)
10. Inquirer Business coverage of Circular 855 (business.inquirer.net/180612)

### Category 3: Bank Product Pages
11. UnionBank Home Loan (unionbankph.com)
12. BDO Home Loan (bdo.com.ph)
13. Metrobank Home Loan (metrobank.com.ph)
14. BPI Home Loan (bpi.com.ph)

### Category 4: Practitioner / Comparison Guides
15. Respicio.ph — Pag-IBIG housing loan equity basis (respicio.ph/commentaries)
16. n90.asia — Best Bank Offering Housing Loans (n90.asia/post)
17. MoneyMax — Best Housing Loans (moneymax.ph/loans/articles)
18. OmniCalculator — Pag-IBIG Housing Loan Calculator (omnicalculator.com)
19. RichestPH — Philippine Condo LTV guide (richestph.com)
20. FilipiKnow — Loan-to-value ratio (filipiknow.net)

### Category 5: International / Regulatory Analysis
21. IMF FSAP 2022 — Philippines Macroprudential Policy Technical Note (IMF Country Report 22/156)
22. ADB — LTV Policy as Macroprudential Tool in Asia (adb.org/publications)
23. BIS Papers No. 94 — Macroprudential Frameworks (bis.org/publ/bppdf/bispap94t.pdf)
24. Baker McKenzie — Philippines Lending and Taking Security Guide (resourcehub.bakermckenzie.com)

---

## 7. Summary for Computation Implementation

For a PH real estate computation tool, the LTV module should implement:

1. **Collateral value computation:** `min(appraised_value, selling_price)` — universally applicable
2. **Pag-IBIG current LTV lookup:** Category-based (socialized/economic/open market) with caps of 100/95/90
3. **Pag-IBIG legacy LTV lookup:** Buyback-vs-retail tables for backward compatibility with older accounts
4. **Commercial bank LTV:** Configurable by bank, property type, and purpose — no single regulatory table
5. **Lot-only exception:** 60-70% across all lenders
6. **Output:** Max loanable amount, required equity, actual LTV ratio

The key computation insight is that LTV is NOT a single formula but a **tiered lookup** that varies by:
- Lender type (Pag-IBIG vs. bank)
- Housing program (standard EUF vs. AHP vs. 4PH)
- Property type (house-and-lot vs. condo vs. lot)
- Developer relationship (buyback guaranty vs. retail)
- Loan purpose (primary residence vs. investment)
- Bank-specific policy (BPI vs. BDO vs. Metrobank each have different tables)
