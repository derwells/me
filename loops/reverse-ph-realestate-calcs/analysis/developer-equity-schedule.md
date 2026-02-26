# Developer Equity/Downpayment Schedule — Computation Extraction

**Aspect:** developer-equity-schedule (Wave 2)
**Date:** 2026-02-26
**Primary source:** `input/developer-payment-terms.md` (Ayala Land group, SMDC, DMCI Homes, Megaworld)
**Verification:** Cross-checked against 25+ independent sources (see verification report)
**Deterministic:** Yes (given contractual parameters) — 8 core computations, all fully deterministic once contract terms are set

---

## 1. Inputs

| Input | Type | Source |
|-------|------|--------|
| `total_contract_price` | currency (PHP) | Contract to Sell (CTS) |
| `list_price` | currency (PHP) | Developer price list (SMDC model) |
| `other_charges_pct` | float (0.065–0.085) | Developer schedule (SMDC: 6.5%–8.5%) |
| `vat_applicable` | boolean | True if selling_price > ₱3,600,000 AND seller is VAT-registered |
| `dp_percentage` | float (0.05–1.0) | Contract terms |
| `reservation_fee` | currency (PHP) | Developer schedule (₱15K–₱500K) |
| `installment_months` | integer (8–72) | Contract terms |
| `spot_cash_discount_rate` | float (0.05–0.32) | Developer discount schedule |
| `dp_based_discount_rate` | float (0.0–0.12) | Lookup table by dp_percentage (DMCI/Alveo model) |
| `pdc_bonus_rate` | float (0.0–0.02) | DMCI: 2% if PDCs submitted within 30 days |
| `penalty_rate_per_month` | float (0.02–0.03) | Developer terms (Ayala: 2%, SMDC/DMCI/Megaworld: 3%) |
| `unpaid_amount` | currency (PHP) | Buyer payment records |
| `months_late` | integer | Payment records |
| `days_late` | integer | Payment records (DMCI escalating model) |
| `unit_floor_area_sqm` | float | Unit specification |
| `assoc_dues_rate_per_sqm` | currency (PHP) | Developer schedule (₱50–₱250/sqm/month) |
| `advance_months` | integer (2–3) | Developer turnover requirements |
| `annual_lump_sum_pct` | float (0.015–0.025) | Megaworld-specific |
| `lump_sum_years` | integer | Megaworld DP period |
| `lease_total_paid` | currency (PHP) | DMCI HomeReady lease contract |

---

## 2. Core Computations

### 2.1 TCP Composition (SMDC Model)

**Formula:**
```
IF selling_price > ₱3,600,000 AND seller_is_vat_registered:
    TCP = list_price + (list_price × other_charges_pct) + (list_price × 0.12)
ELSE:
    TCP = list_price + (list_price × other_charges_pct)
```

**Worked example (Sands Residences):**
```
list_price = ₱6,125,000
other_charges = 8.5% → ₱520,625
VAT = 12% → ₱735,000
TCP = ₱6,125,000 + ₱520,625 + ₱735,000 = ₱7,380,625
```

**Other charges breakdown (SMDC 6.5% example):**
- Registration: 1.28%
- DST: 1.50%
- Transfer tax: 0.75%
- Legal: 0.15%
- Utilities: 1.55%
- Misc: 0.27%
- RPT advance: 1.00%

**Note:** Most developers (Ayala, DMCI, Megaworld) quote TCP inclusive of charges. SMDC uniquely separates list_price from other_charges in their computation sheets. For non-SMDC developers, TCP is the stated contract price directly.

**VAT threshold:** ₱3,600,000 effective January 1, 2024 (BIR RR 1-2024). Previous threshold ₱3,199,200 is outdated. Subject to CPI adjustment every 3 years (next: ~2027). Adjacent units by same buyer from any seller within 12 months are aggregated per RR 13-2012. Parking lots always subject to 12% VAT regardless of price.

**Verification:** CONFIRMED. Formula structure verified from SMDC Calculator (c.smdc.homes), Sands Residences computation sheets, and Gold Residences pricing. VAT threshold CORRECTED from ₱3,199,200 to ₱3,600,000 per BIR RR 1-2024.

---

### 2.2 Monthly Equity Installment

**Formula:**
```
monthly_equity = (TCP × dp_percentage - reservation_fee) / installment_months
```

**Worked example:**
```
TCP = ₱3,500,000
dp_percentage = 20%
reservation_fee = ₱20,000
installment_months = 24
monthly_equity = (₱3,500,000 × 0.20 - ₱20,000) / 24
             = (₱700,000 - ₱20,000) / 24
             = ₱680,000 / 24
             = ₱28,333.33/month
```

**Rules:**
- 0% interest on DP installments — universal among all major developers (industry practice, not legal mandate)
- Reservation fee always deducted before spreading
- RF deducted from DP for most developers; SMDC credits it to DP which then reduces TCP balance (functionally equivalent)

**Edge cases:**
- **Split DP structure** (Ayala Land Premier, Alveo): DP split into "spot DP" (10-30% paid upfront) + "spread DP" (remainder over months). Formula applies to spread portion: `monthly_equity = (TCP × dp_pct - RF - spot_dp_amount) / spread_months`
- **Megaworld annual lump sums** (see §2.8): Monthly equity plus annual lump-sum payments required
- **DMCI HomeReady** (see §2.9): Different path where lease payments substitute for DP

**Verification:** CONFIRMED across CebuHouseFinder, FilipinoHomes.com, DMCI Payment Terms, Respicio.ph.

---

### 2.3 Spot Cash Net Price

**Formula:**
```
net_price = TCP × (1 - spot_cash_discount_rate)
amount_due = net_price - reservation_fee
```

**Worked example (DMCI, 100% spot):**
```
TCP = ₱5,000,000
discount = 10% + 2% PDC = 12%
net_price = ₱5,000,000 × (1 - 0.12) = ₱4,400,000
amount_due = ₱4,400,000 - ₱20,000 = ₱4,380,000
```

**Discount ranges by developer:**

| Developer | Spot Cash Discount |
|-----------|-------------------|
| Avida (condos) | 9% |
| Avida (land/H&L) | 7% |
| Alveo | 5% |
| ALP | 15%–17% |
| Amaia | 5%–10% |
| SMDC | 10%–32% (project-dependent) |
| DMCI | 10%–16% (+2% PDC bonus) |
| Megaworld | ~20% |

**Note:** Specific discount rates are project-specific and promotional — the formula is deterministic but the discount_rate parameter is non-deterministic (changes by project, period, promo). Automation value is in the computation engine, not in predicting rates.

**Verification:** CONFIRMED from Crown Asia, DMCI Projects, Residencia Manila.

---

### 2.4 Scaled Discount by DP Percentage (Lookup Table)

**DMCI model (standard tiers per memo PD-19-09-026):**

| DP % | Base Discount | PDC Bonus | Total |
|------|--------------|-----------|-------|
| 100% (spot) | 10% | +2% | 12% |
| 50% | 8% | +2% | 10% |
| 40% | 7% | +2% | 9% |
| 30% | 6% | +2% | 8% |
| 20% | 2% | +2% | 4% |

**PDC bonus condition:** Submit required documents + post-dated checks within 30 days of reservation. Missing deadline → automatic in-house financing conversion.

**DMCI computation:**
```
total_discount = lookup_discount(dp_percentage) + (pdc_bonus IF pdc_submitted_on_time)
net_tcp = TCP × (1 - total_discount)
```

**Alveo model (deferred cash discount):**

| DP % | Deferred Discount |
|------|-------------------|
| 50% | 2% |
| 30% | 1% |
| 20% | 0% |
| 10% | 0% |

**Automation note:** Each developer maintains their own lookup table. Tables change periodically (project-specific memos). The computation logic (lookup → apply discount → compute schedule) is deterministic; the table contents are configuration data.

**Verification:** CONFIRMED from DMCI agent sites (Sorrel/Zinnia data), Alveo buying guide.

---

### 2.5 Turnover Balance

**Simple formula:**
```
turnover_balance = TCP × (1 - dp_percentage)
```

**With discount (order of operations matters):**

Three developer-specific variants exist:

**Variant A — Discount on TCP first, then split (DMCI model):**
```
discounted_tcp = TCP × (1 - discount_rate)
turnover_balance = discounted_tcp × (1 - dp_percentage)
```

**Variant B — Discount on deferred portion only (Alveo model):**
```
dp_amount = TCP × dp_percentage
deferred_amount = TCP × (1 - dp_percentage)
turnover_balance = deferred_amount × (1 - deferred_discount_rate)
```

**Variant C — Discount reduces DP, balance unchanged (SMDC promo model):**
```
turnover_balance = TCP × (1 - dp_percentage)
# discount applied to reduce monthly equity, not balance
```

**Worked example (Variant A, DMCI 30% DP + 6% discount):**
```
TCP = ₱5,000,000
discounted_tcp = ₱5,000,000 × 0.94 = ₱4,700,000
turnover_balance = ₱4,700,000 × 0.70 = ₱3,290,000
```

**Note:** The turnover balance is the amount to be financed via bank loan, Pag-IBIG, or in-house financing. It determines the loanable amount application.

**Verification:** CONFIRMED with nuance — variant structure identified during verification. General formula correct; discount application order varies by developer.

---

### 2.6 Late Payment Penalty

#### 2.6a Simple Penalty (Ayala, SMDC, Megaworld)

**Formula:**
```
penalty = unpaid_amount × penalty_rate_per_month × months_late
```

**Rates:**
- Ayala/Avida: 2%/month (24% p.a.)
- SMDC: 3%/month (36% p.a.)
- Megaworld: 3%/month (36% p.a.)

**SMDC special rule:** Penalty activates only when cumulative payment deficit exceeds 25% of monthly amortization. Below that threshold, no penalty applies.

**"Fraction thereof" rule:** Both SMDC and Ayala contracts state "per month or fraction thereof" — even 1 day late = full month penalty.

#### 2.6b Escalating Penalty (DMCI)

**Formula:**
```
penalty_rate = 3% × CEILING(days_late / 30)
penalty = unpaid_amount × penalty_rate
```

**Progression:**

| Days Late | Rate | Cumulative |
|-----------|------|------------|
| 1–30 | 3% | 3% |
| 31–60 | 6% | 6% |
| 61–90 | 9% | 9% |
| 91–120 | 12% | 12% |
| ... | ... | ... |
| 331–360 | 36% | 36% |
| 361–365+ | 39%? | **Cap uncertain** |

**⚠ Conflict:** The formula yields 39% at 365 days (CEILING(365/30) = 13 × 3%), but source material states 36% cap. The exact cap point (36% at month 12 vs. 39% at month 13) requires verification from actual CTS document. Flagged for manual review.

#### Legal Constraints on Penalties

- **Art. 1229, Civil Code:** Courts may reduce unconscionable penalties
- **Supreme Court jurisprudence:** Rates >2%/month (24% p.a.) routinely reduced; 3%/month (36% p.a.) prima facie unconscionable (*Megalopolis Properties v. D'Nhew Lending*)
- **BSP Circular 799:** Fallback legal interest rate = 6% p.a. when contractual rate is voided
- **Maceda Law:** No penalties during statutory grace periods (Section 3: 1 month per year of installments paid, once per 5 years)

**Correction:** The "3%/month unconscionable" standard comes from Supreme Court jurisprudence, NOT BSP Circular 957 (which concerns bank examination powers). Previous source material incorrectly attributed this to BSP Circular 957.

**Verification:** CONFIRMED (simple penalty rates and formula). DMCI escalating structure confirmed from Buyer's Guide with cap uncertainty noted.

---

### 2.7 Reservation Fee Computation

**Not a computed value per se, but a lookup + deduction:**

```
# Lookup
reservation_fee = developer_rf_schedule(developer, brand, unit_type)

# Deduction (applied to DP)
effective_dp = TCP × dp_percentage - reservation_fee
```

**Fee Schedule:**

| Developer | Brand | Range |
|-----------|-------|-------|
| Ayala Land | Avida | ₱20K–₱80K |
| Ayala Land | Alveo | ~₱50K |
| Ayala Land | ALP | ₱200K–₱500K |
| SM Prime | SMDC | ₱15K–₱50K |
| DMCI Homes | — | ₱20K (unit) + ₱10K (parking) |
| Megaworld | — | ₱25K–₱100K |

**Universal rules:**
- Non-refundable (exception: developer lacks License to Sell per DHSUD Board Resolution 848-09 — then RF must be immediately refundable)
- Deductible from DP
- 30-day validity window for document submission and first payment
- Secures the unit; CTS signed after RF and documents processed

**Verification:** CONFIRMED with nuance on DHSUD refundability exception.

---

### 2.8 Megaworld Annual Lump-Sum Payment

**Formula (unique to Megaworld):**
```
annual_lump_sum = TCP × annual_lump_sum_pct
total_lump_sums = annual_lump_sum × lump_sum_years
```

**Rates:** 1.5%–2.5% of TCP per year, in addition to monthly equity installments.

**Worked example:**
```
TCP = ₱8,000,000
annual_lump_sum_pct = 2%
lump_sum_years = 3
annual_payment = ₱8,000,000 × 0.02 = ₱160,000
total = ₱160,000 × 3 = ₱480,000
```

**Modified equity formula for Megaworld:**
```
total_dp = TCP × dp_percentage
lump_sum_total = TCP × annual_lump_sum_pct × lump_sum_years
monthly_portion = total_dp - reservation_fee - lump_sum_total
monthly_equity = monthly_portion / installment_months
```

**Verification:** Confirmed from Megaworld BGC and Iloilo project documentation. Unique among major developers — no other developer uses this structure.

---

### 2.9 DMCI HomeReady (Rent-to-Own) DP Credit

**Formula:**
```
dp_credit = total_lease_payments × 0.60
remaining_dp = (TCP × dp_percentage) - dp_credit
balance_for_financing = TCP - (TCP × dp_percentage)
```

**Parameters:**
- Lease term: 24–36 months
- 60% of total lease payments credited toward DP
- After lease: remaining DP (typically 10%) + 90% balance via bank financing
- Price locked at lease start ("Price Protect")
- 36-month term: 10% rent increase in year 3
- Opt-out with no penalties (lease contract, not CTS — Maceda Law does not apply)

**Verification:** Confirmed from DMCI HomeReady page. Niche product but fully deterministic computation.

---

## 3. Closing Cost Estimation

**Aggregate formula:**
```
closing_costs = DST + transfer_tax + registration_fee + notarial_fee + rpt_advance + utility_setup + assoc_dues_advance

WHERE:
  DST = MAX(selling_price, zonal_value, fmv) × 0.015
  transfer_tax = MAX(selling_price, zonal_value, fmv) × lgu_rate  # 0.50%–0.75%
  registration_fee = rod_fee_schedule(MAX(selling_price, zonal_value, fmv))  # see rod-registration-fees
  notarial_fee = 1%–2% of property value (heuristic; varies by IBP chapter)
  rpt_advance = assessed_value × rpt_rate × 1  # 1 year advance
  utility_setup = ₱8,000–₱25,000 (lump sum)
  assoc_dues_advance = unit_floor_area_sqm × assoc_dues_rate_per_sqm × advance_months
```

**Typical total:** 4%–10% of TCP

**Note:** DST, transfer tax, and RPT are tax computations covered in `loops/ph-tax-computations-reverse/`. Cross-reference that catalog for detailed extraction. The closing cost estimator aggregates tax + non-tax components.

**Verification:** Ranges confirmed from multiple practitioner guides (Respicio.ph, Federal Land, RealLiving.com.ph). Individual component computations are extracted in dedicated aspects (rod-registration-fees, notarial-fees, broker-commission, etc.).

---

## 4. Decision Tree: Developer Payment Option Selection

```
BUYER SELECTS PAYMENT OPTION:

1. SPOT CASH (100% within 30 days)
   ├── net_price = TCP × (1 - spot_discount)
   ├── amount_due = net_price - reservation_fee
   └── DONE (one-time payment)

2. DEFERRED CASH (100% spread, 0% interest)
   ├── net_price = TCP × (1 - deferred_discount)
   ├── monthly = (net_price - reservation_fee) / deferred_months
   └── DONE (24–48 monthly payments)

3. INSTALLMENT (DP + Bank/Pag-IBIG Financing)
   ├── total_dp = TCP × dp_percentage
   ├── IF developer has scaled_discount_table:
   │   ├── discount = lookup(dp_percentage)
   │   └── total_dp = TCP × (1 - discount) × dp_percentage  [DMCI model]
   │       OR total_dp = TCP × dp_percentage  [discount applied to deferred only, Alveo model]
   ├── monthly_equity = (total_dp - reservation_fee) / equity_months
   ├── turnover_balance = TCP - total_dp  [varies by discount application model]
   └── turnover_balance → bank mortgage or Pag-IBIG loan application

4. IN-HOUSE FINANCING (DP + Developer loan)
   ├── Same DP computation as #3
   ├── balance = TCP - total_dp
   ├── amortization = standard declining balance (14%–18% p.a., 5–10 years)
   └── monthly = balance × [r(1+r)^n] / [(1+r)^n - 1]

5. DMCI HOMEREADY (Rent-to-Own)
   ├── lease period (24–36 months)
   ├── dp_credit = total_lease × 0.60
   ├── remaining_dp = (TCP × dp_pct) - dp_credit
   └── balance → bank financing
```

---

## 5. Edge Cases and Special Rules

### 5.1 Maceda Law Interaction
All CTS installment sales are subject to RA 6552. Key implications for equity schedules:
- Down payments and reservation fees count as "installments" for the 2-year threshold
- After 2+ years of payments: buyer entitled to grace period (1 month/year paid, once per 5 years)
- Cash surrender value = 50% of total payments + 5%/year after year 5 (max 90%)
- Developer cannot cancel CTS without paying CSV and providing notarized notice
- **Cross-reference:** `analysis/maceda-refund.md` (pending Wave 2)

### 5.2 Price Escalation
- No standardized deterministic formula across developers
- PD 957 text does NOT contain a 10% cap (may exist in DHSUD implementing rules — unverified)
- Judicial rule: Unilateral escalation without clear formula is void (*Orbe v. Filinvest*, G.R. No. 208185)
- Major developers absorb cost increases for preselling (TCP fixed at reservation)
- **Classification:** Non-deterministic — excluded from scoring

### 5.3 VAT Aggregation
- Adjacent units purchased by same buyer from any seller within 12 months are aggregated per BIR RR 13-2012
- Threshold: ₱3,600,000 (updated per BIR RR 1-2024)
- Condo parking lots always subject to 12% VAT (not classified as residential dwellings)

### 5.4 SMDC Deficit Tolerance
- SMDC penalty triggers only when cumulative deficit > 25% of monthly amortization
- Below that threshold: no penalty accrues — creates a small tolerance buffer

---

## 6. Verification Status Summary

| Computation | Status | Sources |
|-------------|--------|---------|
| TCP composition (SMDC) | ✅ CONFIRMED (VAT threshold CORRECTED to ₱3.6M) | SMDC Calculator, Sands/Gold computation sheets |
| Monthly equity installment | ✅ CONFIRMED | CebuHouseFinder, FilipinoHomes, DMCI, Respicio |
| Spot cash net price | ✅ CONFIRMED | Crown Asia, DMCI Projects, Residencia Manila |
| Scaled discount (DMCI) | ✅ CONFIRMED | DMCI agent sites, memo PD-19-09-026 |
| Turnover balance | ✅ CONFIRMED (3 variants documented) | Federal Land, RealLiving, DMCI |
| Late penalty (simple) | ✅ CONFIRMED | SMDC Terms, Respicio, Filipino Law Group |
| Late penalty (DMCI escalating) | ⚠️ CONFIRMED with cap uncertainty | DMCI Buyer's Guide (exact cap needs CTS verification) |
| Reservation fee treatment | ✅ CONFIRMED | RichestPH, Respicio, SMDC Terms, DMCI Guide |
| Megaworld lump sums | ✅ CONFIRMED | Megaworld BGC/Iloilo project docs |
| DMCI HomeReady | ✅ CONFIRMED | DMCI HomeReady official page |
| Closing cost estimation | ✅ CONFIRMED (ranges) | Respicio, Federal Land, RealLiving |

**Key corrections applied:**
1. VAT threshold updated from ₱3,199,200 → ₱3,600,000 (BIR RR 1-2024)
2. BSP Circular 957 attribution corrected → Supreme Court jurisprudence
3. PD 957 "10% escalation cap" flagged as not found in statute text
4. Adjacent unit aggregation scope corrected to include purchases from different sellers

---

## 7. Deterministic Assessment

**Deterministic: YES** — All 8+ core computations are fully deterministic given contractual parameters.

**Non-deterministic parameters (configuration data, not computation logic):**
- Discount rates (project-specific, promotional)
- In-house financing interest rates (internal developer memos)
- Other charges percentage (varies by developer/project)
- Association dues rates (set by property management)
- Price escalation clauses (contractual, non-standard)

**Automation value:** High. The computation engine is deterministic and universal across developers. Competitive advantage lies in:
1. Supporting all 3 discount application variants (DMCI, Alveo, SMDC models)
2. Handling the full decision tree (5 payment options with sub-computations)
3. Incorporating Maceda Law calculations into equity tracking
4. Aggregating closing costs from tax + non-tax components
5. Supporting developer-specific edge cases (Megaworld lump sums, DMCI HomeReady, SMDC deficit tolerance)

---

## Legal Citations

| Law/Regulation | Relevance |
|----------------|-----------|
| PD 957 (Subdivision & Condo Buyer's Protective Decree) | CTS requirements, developer obligations |
| RA 6552 (Maceda Law) | Installment buyer protection, refund/grace computation |
| BIR RR 1-2024 | VAT exemption threshold ₱3,600,000 |
| BIR RR 13-2012 | Adjacent unit VAT aggregation rules |
| BSP Circular 799 | Legal interest rate 6% p.a. (fallback) |
| Art. 1229, Civil Code | Court power to reduce unconscionable penalties |
| Art. 1305, Civil Code | Freedom of contract (rates are contractual) |
| DHSUD Board Res. 848-09 | No fee collection before License to Sell |
| *Orbe v. Filinvest* (G.R. 208185) | Unilateral escalation without formula is void |
| *Megalopolis Properties v. D'Nhew Lending* | 3%/month (36% p.a.) penalty is unconscionable |
