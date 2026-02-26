# Developer Payment Terms — Source Acquisition

## Summary

Survey of published payment computation terms from four major Philippine developers (Ayala Land group, SMDC, DMCI Homes, Megaworld) to identify common equity schedule patterns, discount formulas, penalty structures, and turnover balance rules relevant to the Wave 2 `developer-equity-schedule` computation extraction.

---

## 1. Spot Cash Discount

Spot cash = full payment of TCP (Total Contract Price) within a defined window (typically 30–60 days from reservation).

### Ayala Land Group

| Brand | Product Type | Discount | Window |
|-------|-------------|----------|--------|
| Avida | Towers (condos) | **9%** off TCP | 30 days |
| Avida | Land & Houses | **7%** off TCP | 30 days |
| Alveo | Lots (Montala) | **5%** off TCP | 60 days |
| Ayala Land Premier | Lots/Condos | **15–17%** off list price | 30 days (varies) |
| Amaia | Non-RFO | **10%** off TCP | 30 days |
| Amaia | RFO | **5%** off TCP | 30 days |
| Amaia | Spot cash (7 days) | **10%** off TCP | 7 days |

Note: Ayala Land Premier discounts vary significantly by project. A 17% discount was observed for Enara at NUVALI lots; Arbor Lanes condos advertised up to 15%. These are the highest published discounts among mainstream developers.

### SMDC

- Up to **32% spot cash discount** on select units (promotional, project-specific)
- Typical non-promo range: **10–16%** depending on project and unit type
- Additional stackable discounts: 8% employee, 1% bulk, 1% buyer loyalty, various promo discounts

### DMCI Homes

- **10–16% discount** for 100% cash term (project-dependent)
- Additional **2% PDC discount** if complete documents + post-dated checks submitted within 30 days

### Megaworld

- Spot cash discounts are project-specific; not published as standard percentages
- General industry pattern: large discount for outright payment within 30 days

### Common Pattern

```
net_price = TCP × (1 - spot_cash_discount_rate)
```

Discount rates range from 5% to 32% depending on developer, brand tier, project phase, and promotional period. The discount is conditional on timely payment within the specified window.

---

## 2. Deferred Cash Payment

Deferred cash = full TCP paid in installments over an extended period without bank financing.

### Ayala Land Group

| Brand | Structure | Term | Discount | Interest |
|-------|-----------|------|----------|----------|
| Avida | 100% balance net of RF | 24 months | Unspecified | 0% |
| Avida | 20% spot DP + balance | 18–23 months | Unspecified | 0% |
| Alveo (Montala) | 50% DP + 50% deferred | 24 months | 2% | 0% |
| Alveo (Montala) | 30% DP + 70% deferred | 24 months | 1% | 0% |
| Alveo (Montala) | 20% DP + 80% deferred | 24 months | None | 0% |
| Alveo (Montala) | 10% DP + 90% deferred | 24 months | None | 0% |
| Amaia | Full TCP deferred | 24 months | None | 0% |

### SMDC

- Not explicitly labeled "deferred cash" but effectively: 20% spread over 30 months at 0% interest + 80% lump sum at turnover

### Megaworld

- Deferred cash covers entire TCP over up to 3 years
- No discount (unlike spot cash), but also no interest

### Common Pattern

Deferred cash discount decreases as the DP percentage decreases and/or the deferred term lengthens. The formula:

```
deferred_discount_rate = f(dp_percentage, term_months)
# Higher DP + shorter term → higher discount
# Typical range: 0% to 5%
```

Deferred cash is always 0% interest — the "cost" to the buyer is the absence of a larger spot cash discount.

---

## 3. Downpayment / Equity Schedule

The downpayment (DP) or "equity" is the portion of TCP the buyer pays before turnover, typically financed interest-free by the developer.

### Ayala Land Group

| Brand | DP % | Monthly Installment | Term | Interest |
|-------|------|---------------------|------|----------|
| Avida (condos) | 20% of TCP | DP spread over 8–36 months | 8–36 mo | 0% |
| Avida (lots/H&L) | 20% of TCP | DP spread over 12 months | 12 mo | 0% |
| Alveo | 10–50% of TCP | Various (project-specific) | 18–24 mo | 0% |
| ALP (Park Central) | 10% spot + 30% spread | 25 monthly payments | 25 mo | 0% |
| ALP (Enara NUVALI) | 20% spot + 30% spread | 30 monthly payments | 30 mo | 0% |
| ALP (Orchard Vistas) | 10% spot + 20% spread | 24 monthly payments | 24 mo | 0% |

### SMDC

| Scheme | DP Structure | Term | Interest |
|--------|-------------|------|----------|
| 20 Spot – 80 | 20% spot DP (1 month) | Immediate | 0% |
| 10-10-80 | 10% spot + 10% spread | 30 months | 0% |
| 20 Spread – 80 | 20% spread | 30 months | 0% |
| EOP (RFO) | 5% spot (Filipino) / 10% (foreign) | Immediate | 0% on remaining 22 mo |

### DMCI Homes

| Scheme | DP % | Term | Interest |
|--------|------|------|----------|
| Pre-selling | 20–30% | Spread over construction period | 0% |
| RFO | 10% spot | Immediate (or 3–12 months promo) | 0% |
| RFO promo | 5% spot + 5% stretched | 3–12 months | 0% |

### Megaworld

- 30–35% of TCP paid over construction period (pre-selling)
- No spot DP required on many projects ("No Spot Downpayment" promos)
- Monthly amortization starts 1 month after reservation

### Common DP Computation

```
monthly_equity = (TCP × dp_percentage - reservation_fee) / term_months
```

Where:
- `TCP` = Total Contract Price (inclusive of VAT)
- `dp_percentage` = 10%–30% (varies by developer, project, scheme)
- `reservation_fee` is deducted (it's credited toward the DP)
- `term_months` = 8–60 months (pre-selling: aligned with construction timeline)
- Interest = 0% during DP period (universal across all major developers)

---

## 4. Bank Financing Portion

The balance after DP is paid via bank loan or developer in-house financing.

### Ayala Land Group

- Standard: **80% of TCP** financed through bank
- BPI Family Bank (Ayala sister company): up to **90% LTV** for ALP/Alveo properties
- Accredited banks: BPI, Chinabank, BDO, Metrobank, PSBank
- Estimated monthly amortization rates (from Avida Riala sample):
  - 5 years: ~₱81,867/mo on ₱4.23M balance
  - 10 years: ~₱47,013/mo
  - 15 years: ~₱35,734/mo
  - 20 years: ~₱30,338/mo

### SMDC

- Standard: **80% of TCP** through bank financing
- Bank application processed upon turnover

### DMCI Homes

- Standard: **70–80% of TCP** through bank financing
- 12 accredited banks
- In-house financing available: max 10 years term (higher interest than bank)
- Developer-assisted: Letter of Guarantee processing ~30 days

### Megaworld

- **65–70% of TCP** financed at turnover (after 30–35% DP)
- No in-house financing; buyer must arrange bank loan

### In-House Financing (Developer)

| Developer | Available | Max Term | Interest Rate |
|-----------|-----------|----------|---------------|
| Avida | Yes | 10 years | 18% fixed |
| SMDC | Yes | 10 years (SERP promo: 0%) | Higher than bank (rate unpublished) |
| DMCI | Yes | 10 years minus utilized months | Unpublished (higher than bank) |
| Megaworld | No | — | — |

---

## 5. Reservation Fee

| Developer | Amount | Deductible from DP? | Refundable? |
|-----------|--------|---------------------|-------------|
| Avida | ₱20,000–₱80,000 (project-dependent) | Yes | No |
| Alveo | ~₱50,000 (standard); ₱100,000+ for premium | Yes | No |
| ALP | ₱200,000–₱500,000 | Yes | No |
| SMDC | ₱25,000 (standard) | Yes | No |
| DMCI | ₱20,000 (unit) + ₱10,000 (parking) | Yes | No |
| Megaworld | Project-specific | Yes (implied) | No |

### Common Pattern

```
first_month_equity = monthly_equity_amount  # RF already deducted from DP total
net_dp = (TCP × dp_percentage) - reservation_fee
monthly_equity = net_dp / installment_months
```

Reservation fee is universally:
- Non-refundable
- Deductible from the downpayment
- Must be followed by documentary requirements within 7–30 days
- Unit held for 30 days; if DP/documents not submitted, reservation cancelled and RF forfeited

---

## 6. Penalties for Late Payment

### Ayala Land Group (Avida — from computation sheets)

- **2% of unpaid amount per month** (or fraction thereof) of delay
- Discounts are conditional on timely compliance — any default voids discount entitlement
- Default triggers seller's remedial options (demand, cancellation per Maceda Law)

### SMDC

- **3% penalty per month** if deficit exceeds 25% of monthly amortization (cumulative)
- Underpayment applied to last installment due (or balloon payment)
- Company demands payment within 5 working days before penalty kicks in

### DMCI Homes

Progressive penalty structure:

| Days Past Due | Cumulative Penalty |
|---------------|-------------------|
| 1–30 | 3% |
| 31–60 | 6% |
| 61–90 | 9% |
| 91–120 | 12% |
| ... | +3% per 30-day block |
| 331–365 | 36% |
| 365+ | 36% + continued accrual |

This is effectively **3% per month simple interest**, capping at 36% per year, with continued accrual beyond.

### Industry Pattern

```
penalty = unpaid_amount × penalty_rate × months_overdue
# penalty_rate typically 2%–3% per month (simple, not compounding)
# Some developers (DMCI) use progressive tiers
# All subject to Maceda Law protections (grace periods, refund rights)
```

Judicial limit: Courts routinely reduce penalties exceeding 24% per annum (2% per month) as unconscionable. Developer contracts typically stay at or below this threshold.

---

## 7. Turnover / Balance Payment

The "balance" or "lump sum" is the portion of TCP not covered by the DP, due at or before turnover.

### Common Structures

| Structure | DP | Balance | When Due |
|-----------|-----|---------|----------|
| 10-20-70 | 10% spot + 20% spread | 70% lump sum | At turnover |
| 20-80 | 20% (spot or spread) | 80% lump sum | At turnover |
| 30-70 | 30% (spot or spread) | 70% lump sum | At turnover |
| 10-10-80 (SMDC) | 10% spot + 10% spread | 80% lump sum | At turnover |

### Rules

1. Balance must be paid via bank financing (Letter of Guarantee) or cash at turnover
2. Developer issues notice ~6–12 months before projected turnover for bank loan processing
3. Buyer must issue **guarantee check** covering lump sum amount (Avida/SMDC)
4. Upon bank's release of Letter of Guarantee, developer returns guarantee check
5. If buyer cannot secure bank financing by turnover: account may be restructured or cancelled
6. Some projects allow periodic lump sum payments during construction (e.g., 2.5% at 12th, 24th, 36th month)

### Computation

```
balance = TCP × (1 - dp_percentage)
# If spot cash discount applies: balance = TCP × (1 - discount_rate) × (1 - dp_percentage)
# Balance paid via: bank loan, Pag-IBIG, or cash
```

---

## 8. Price Escalation Clauses

### Regulatory Framework

- **PD 957** (and DHSUD implementing rules): maximum **10% per annum** escalation for regulated projects (subdivisions, condominiums under DHSUD jurisdiction)
- Escalation must be **expressly stated** in the Contract to Sell
- Must comply with **mutuality of contracts** (Art. 1308, Civil Code) — cannot be unilateral

### Developer Practice

- Major developers (Ayala Land, SMDC, DMCI, Megaworld) do **not publish standard escalation formulas** on their websites
- Price escalation is typically handled through:
  1. **Phase-based repricing** — each new phase/tranche of a development is priced higher than the previous
  2. **List price updates** — developer periodically updates the official price list; buyers who have signed CTS are locked in
  3. **Construction cost escalation** — some contracts allow adjustment tied to construction cost index (not publicly documented)
- Pre-selling buyers are generally **locked into the TCP at reservation** — escalation risk transfers to the developer
- Escalation clauses, where present, are typically **CPI-linked** or **fixed percentage** (5–10% annually), but these are more common in commercial leases than residential sales

### Key Finding

Price escalation clauses in residential Contracts to Sell are **not standardized or publicly documented** by major developers. The primary price escalation mechanism is **phase-based repricing** rather than contractual escalation on existing sales. This makes it a non-deterministic element for automation purposes.

---

## Cross-Developer Comparison Matrix

| Feature | Ayala Land (Avida) | SMDC | DMCI | Megaworld |
|---------|-------------------|------|------|-----------|
| Spot cash discount | 7–17% | 10–32% | 10–16% | Project-specific |
| Deferred cash term | 24 months, 0% | 30 months, 0% | Construction period, 0% | Up to 3 years, 0% |
| DP range | 10–30% | 5–20% | 10–30% | 30–35% |
| DP installment term | 8–36 months | 22–30 months | Construction period | Construction period |
| DP interest | 0% | 0% | 0% | 0% |
| Bank financing % | 80% (90% w/ BPI) | 80% | 70–80% | 65–70% |
| In-house financing | Yes (18% fixed, 10yr) | Yes | Yes (10yr max) | No |
| Reservation fee | ₱20K–₱500K | ₱25K | ₱20K (unit) | Project-specific |
| RF deductible from DP | Yes | Yes | Yes | Yes |
| Late penalty rate | 2%/month | 3%/month | 3%/month (progressive) | Project-specific |
| PDC discount | N/A | N/A | 2% | N/A |

---

## Computation Patterns Identified for Wave 2

The following deterministic computations emerge from this data:

1. **Spot cash net price**: `net = TCP × (1 - discount_rate)` — inputs: TCP, discount_rate (varies by developer/project/promo)
2. **Monthly equity/DP installment**: `monthly = (TCP × dp_pct - reservation_fee) / months` — inputs: TCP, dp_pct, RF, months
3. **Late payment penalty**: `penalty = unpaid × rate × months_overdue` (simple) or progressive tiers (DMCI-style)
4. **Total cost comparison across payment schemes**: given TCP, compare total outlay for spot cash vs deferred vs bank financing (requires amortization computation from `bank-mortgage-amortization` aspect)
5. **Guarantee check amount**: `guarantee = TCP × balance_pct` — for bank financing applications
6. **In-house financing amortization**: standard amortization formula at developer's fixed rate (e.g., Avida 18%)

### Non-Deterministic Elements (excluded from scoring)

- Spot cash discount rate: varies by project, promo period, negotiation — no universal formula
- Price escalation: not standardized across developers
- In-house financing interest rate: often undisclosed (except Avida 18%)

---

## Sources

### Ayala Land Group
- [Avida Home Financing](https://avidaland.com/home-financing.php) — spot cash 9%/7%, deferred terms, in-house 18%
- [Avida Buyers' Guide](https://www.avidaland.com/buyers-guide) — reservation process, payment channels
- [Alveo Buying Guide](https://www.alveoland.com.ph/buying-guide/) — reservation fee, 30-day payment deadline
- [Alveo Premium Property FAQs](https://alveopremiumproperty.com/faqs/) — payment schemes, RF non-refundable
- [Montala Alviera (Alveo)](https://www.ayalalandalviera.com/montala-alviera.html) — deferred payment discount tiers (1–5%)
- [Avida Towers Cloverleaf Sample Computation](https://cloverleafavida.wordpress.com/sample-computations/) — 10-10-80 scheme worked example
- [Avida Towers Centera Computation (PDF)](https://assets.onepropertee.com/forum-attachments/files/at+centera+4-214+20%25in+36mos_.YWXcuX75fdnrxM8LE.pdf) — 2% penalty clause
- [Avida Towers Prime Taft Computation (PDF)](https://www.preselling.com.ph/wp-content/uploads/2020/01/Avida-Towers-Prime-Taft-Sample-Computation.pdf)
- [Avida Towers Riala (Cebu)](https://www.cebu-realestateshop.com/condo-for-sale/avida) — sample computation with amortization estimates
- [Ayala Land Premier PreSelling (Preselling.com.ph)](https://www.preselling.com.ph/agent/ayala-land-premier/) — 15–17% spot cash discount, ALP reservation fees
- [Ayala Land Premier by Rowie Morito](https://www.myproperty.ph/ayala-land-premier-agn-2/) — lot payment terms, 15% cash discount
- [Amaia Scapes Pampanga Pricelist](https://www.amaiascapespampanga.com/amaia-scapes-pampanga-pricelist) — 7%/10% spot cash
- [Amaia Land Home Financing](https://www.amaialand.com/home-financing/) — 10% non-RFO / 5% RFO discount

### SMDC
- [SMDC Payment Guidelines](https://smdc.com/payment-guidelines/) — payment schemes overview
- [SMDC Condo Promos 2026](https://manilacondosbysmdc.com/promos/) — up to 32% spot cash discount
- [SMDC SERP Program](https://manilacondosbysmdc.com/unlock-your-dream-home-with-smdcs-special-employee-rfo-payterm-program-serp/) — 0% interest 10yr, 8% employee discount
- [SMDC Early Occupancy Program](https://manilacondosbysmdc.com/early-occupancy-program/) — 5% DP, 0% interest 22 months
- [SMDC April 2023 Promo Terms (Studocu)](https://www.studocu.com/ph/document/ama-university/intermediate-accounting-1/smdc-pdev-slsc-iom-0744-announcement-of-april-2023-special-payment-terms-promo-discounts-and-rf/67118711) — stackable discount rules, 3% penalty clause

### DMCI Homes
- [DMCI Buyers Guide](https://www.dmcihomes.com/guides/buyers-guide) — penalty schedule (3%/30-day tiers), restructuring fee ₱10K
- [DMCI Price List Comparisons](https://dmciprojects.net/dmci-price/) — 10–16% cash discount, 2% PDC discount
- [DMCI Payment Terms Blog](https://dmcihomesworld.wordpress.com/payment-terms/) — DP terms, RFO promos
- [DMCI Payment Options](https://www.dmcipropertyfinder.com/payment-options.html) — in-house financing details

### Megaworld
- [Megaworld BGC Property FAQs](https://www.bgcpropertyinvestments.com/faqs) — no in-house financing, 30–35% DP
- [Megaworld Luxury FAQ](https://www.megaworldluxury.com/faq/) — reservation fee non-refundable
- [Uptown Arts Megaworld](https://www.megaworldcbd.com/uptown-arts) — no spot DP promo

### Legal / Industry
- [Filipino Law Group — Missed Payments](https://filipinolawgroup.com/missed-payments-real-estate-financing/) — Maceda Law protections
- [Respicio & Co. — Penalties for Nonpayment](https://www.lawyer-philippines.com/articles/penalties-for-nonpayment-of-installment-on-land-purchase-philippines) — judicial limits on penalties
- [DHSUD Maceda Law FAQ](https://dhsud.gov.ph/maceda-law-ra-6552-legal-faqs/) — grace period, refund computation
- [Phoenix Realty — Financing Terms](https://www.phoenixrealty.com.ph/blogs/real-estate-financing-terms) — spot cash vs deferred vs installment definitions
