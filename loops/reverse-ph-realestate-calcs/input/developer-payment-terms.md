# Developer Payment Terms — Source Acquisition

Fetched 2026-02-26. Covers Ayala Land group (Avida, Alveo, ALP, Amaia), SMDC, DMCI Homes, Megaworld.

---

## 1. Common Payment Structures Across All Developers

### 1.1 Payment Options (Universal Pattern)

Every major PH developer offers these standard payment tiers:

| Option | Structure | Typical Discount |
|--------|-----------|-----------------|
| **Spot Cash** | 100% TCP within 30 days of reservation | 5%–32% off TCP |
| **Deferred Cash** | 100% TCP spread over 24–48 months at 0% interest | 1%–10% off TCP |
| **Installment (Equity + Financing)** | DP spread monthly (0% interest) + balance via bank/in-house | 0%–4% |
| **In-House Financing** | DP + balance amortized at developer's rate (14%–18% p.a.) | None |

### 1.2 Universal Computation Formulas

**Spot cash:**
```
net_price = TCP × (1 - spot_cash_discount_rate)
amount_due = net_price - reservation_fee
```

**Monthly equity/DP installment:**
```
monthly_dp = (TCP × dp_percentage - reservation_fee) / installment_months
```

**Balance at turnover:**
```
turnover_balance = TCP × (1 - dp_percentage) - applicable_discounts
```

**Total Contract Price components (SMDC model, others similar):**
```
TCP = list_price + other_charges (6.5%–8.5%) + VAT (12% if > ₱3,199,200)
```

### 1.3 Contract Structure (Universal)

Two-document flow:
1. **Reservation Agreement** → **Contract to Sell (CTS)** — developer retains title, buyer has equitable interest
2. **Deed of Absolute Sale (DOAS)** — after full payment, unconditional ownership transfer

Maceda Law (RA 6552) applies to all CTS for residential installment sales.

---

## 2. Developer-Specific Discount Schedules

### Ayala Land Group

| Brand | Spot Cash Discount | Deferred Discount | Notes |
|-------|-------------------|-------------------|-------|
| **Avida** (condos) | 9% | 0% (24 months) | 7% for land/H&L |
| **Alveo** | 5% | 1%–2% (varies by DP%) | Higher DP → higher discount |
| **ALP** | 15%–17% | N/A | Highest in Ayala group |
| **Amaia** | 5%–10% | 0% (24 months) | 10% non-RFO, 5% RFO |

Alveo tiered deferred discount structure:
- 50% DP / 50% deferred → 2% discount
- 30% DP / 70% deferred → 1% discount
- 20% DP / 80% deferred → 0% discount
- 10% DP / 90% deferred → 0% discount

### SMDC

| Option | Discount | Notes |
|--------|----------|-------|
| 100% Spot Cash | Up to 32% | Varies by project; promotional |
| 5% Spot + 15% Spread | ~20% | Gold Residences example |
| 15% Spread only | ~20% | Same discount as 5%+15% in some projects |
| 10% Spot DP + 90% deferred (30 mos) | 3% | MPlace data |
| 20% Spot DP + 80% deferred (30 mos) | 4% | MPlace data |

Additional SMDC stackable discounts: Employee 8%, Bulk 1%, Loyalty 1%, promos variable.

### DMCI Homes

Scaled discount by DP percentage (Sorrel/Zinnia data):

| DP % | Discount | + PDC Discount |
|------|----------|---------------|
| 100% (spot) | 10% | +2% |
| 50% | 8% | +2% |
| 40% | 7% | +2% |
| 30% | 6% | +2% |
| 20% | 2% | +2% |

PDC discount (2%) conditional on submitting documents + PDCs within 30 days. Missing this deadline → automatic in-house financing conversion.

### Megaworld

| Option | Discount |
|--------|----------|
| 100% Spot Cash | ~20% |
| 50% Spot | ~15% |
| Deferred (24–48 months) | ~10% |

Megaworld equity structure uses **annual lump-sum payments** (1.5%–2.5% of TCP) in addition to monthly installments — unique among major developers.

---

## 3. Downpayment / Equity Parameters

### DP Percentages by Developer

| Developer | Standard DP% | Promo DP% | Max Spread (months) |
|-----------|-------------|-----------|---------------------|
| Avida (condos) | 20% | 10%–20% | 8–36 |
| Avida (land/H&L) | 20% | — | 12 |
| Alveo | 10%–50% | — | 18–24 |
| ALP | 10%–50% | — | 25–30 |
| SMDC | 15%–20% | 0% spot + 15%–20% spread | 24–48 |
| DMCI (mid-rise) | 20% | 12% | 36–52 |
| DMCI (high-rise) | 30% | 5% spot + 5% spread | 12 |
| Megaworld | 30%–40% | 0% spot + spread | 36–72 |

All developers: DP installments at **0% interest**.

### SMDC Zero-Downpayment Model

"No Spot DP" means reservation fee only upfront; full DP% spread over 24–48 months.
```
reservation_fee (₱15K–₱50K) → monthly DP (0%, 24–48 mos) → balance via financing
```

---

## 4. Reservation Fees

| Developer | Range | Deductible? | Refundable? | Validity |
|-----------|-------|-------------|-------------|----------|
| Avida | ₱20K–₱80K | Yes (from DP) | No | 30 days |
| Alveo | ~₱50K | Yes | No | 30 days |
| ALP | ₱200K–₱500K | Yes | No | 30 days |
| SMDC | ₱15K–₱50K | Yes (from TCP) | No | 30 days |
| DMCI | ₱20K (unit), ₱10K (parking) | Yes (from DP) | No | 7–30 days |
| Megaworld | ₱25K–₱100K | Yes | No | 30 days |

**Universal rule:** Non-refundable, deductible from DP/TCP, 30-day validity window.

---

## 5. Late Payment Penalties

| Developer | Rate | Structure | Notes |
|-----------|------|-----------|-------|
| Ayala/Avida | 2%/month | Simple interest on unpaid amount | Judicial limit: 24% p.a. |
| SMDC | 3%/month | Simple; kicks in when deficit >25% of monthly amortization | 5 business days notice |
| DMCI | 3%/30-day block | Escalating: 3%, 6%, 9%…up to 36% at 365 days | Most punitive structure |
| Megaworld | 3%/month | Simple interest on delayed amount | Standard |

**Computation (simple):**
```
penalty = unpaid_amount × penalty_rate_per_month × months_late
```

**DMCI escalating computation:**
```
penalty = unpaid_amount × (3% × ceiling(days_late / 30))
```

**Legal ceiling:** Courts routinely reduce penalties >24% p.a. (2%/month) as unconscionable. BSP Circular 957 treats >3%/month as prima facie unconscionable. Default legal interest (no contractual rate): 6% p.a. per BSP Circular 799.

**Grace periods:** No penalties during Maceda Law statutory grace periods.

---

## 6. Bank Financing Terms

### Standard Parameters

| Parameter | Typical Range |
|-----------|--------------|
| LTV (balance financed) | 70%–90% of TCP |
| Interest rate | 5.25%–12% (fixed period + repricing) |
| Fixed period | 1–5 years |
| Loan tenor | 10–25 years |
| Income requirement | Monthly amortization ≤ 35% of gross income |
| Employment | 2+ years current employer |

### Developer-Specific Notes

- **Ayala Land:** BPI Family Bank (sister company) offers up to 90% LTV for ALP/Alveo
- **SMDC:** BDO (SM group) as primary partner; 15+ accredited banks
- **DMCI:** 15+ accredited banks; reminder sent 1 year before financing due date
- **Megaworld:** BDO, BPI, Union Bank, HSBC; Pag-IBIG NOT available for Megaworld units

### In-House Financing (Post-DP Balance)

| Parameter | Typical |
|-----------|---------|
| Interest rate | 14%–18% p.a. fixed |
| Maximum term | 5–10 years |
| DP required | 10%–50% |
| Credit check | Minimal/none |
| Advantage | No bank approval needed |

**Avida in-house:** 18% fixed, 10-year term.
**DMCI in-house:** Rate set by internal memo; terms 1–10 years; minimum 50 PDCs.

---

## 7. Turnover / Closing Costs

### Standard Charges at Turnover

| Charge | Rate |
|--------|------|
| Documentary Stamp Tax (DST) | 1.5% of higher(NSP, FMV) |
| Transfer Tax | 0.5%–0.75% (varies by LGU) |
| Registration Fee | ~0.25% |
| Notarial/Processing Fee | ₱5K–₱15K |
| Real Property Tax (1 year advance) | ~1% of assessed value |
| Utility setup (Meralco, water) | ₱8K–₱25K |
| Association dues (2–3 months advance) | ₱50–₱250/sqm/month |
| **Total closing costs** | **4%–10% of TCP** |

**SMDC "other charges" (bundled into TCP):** 6.5%–8.5% covering registration, DST, transfer tax, legal fees, utility, misc, RPT.

**DMCI misc expenses:** 3.6%–13.5% of TCP (wide range depending on inclusions).

### VAT Rule
- 12% VAT on residential units > ₱3,199,200 (seller is VAT-registered)
- Adjacent units by same buyer from same seller within 12 months are aggregated

---

## 8. Price Escalation

- **PD 957 cap:** Escalation limited to 10% per annum for regulated projects (must be in CTS)
- **Practice:** Major developers set fixed TCP at reservation for preselling; absorb cost increases
- **Judicial rule:** Unilateral escalation without clear formula is void; ambiguous clauses construed against developer (Orbe v. Filinvest, G.R. No. 208185)
- **Maceda Law Section 7:** Contract stipulations contrary to buyer protections are null and void
- **Conclusion:** Price escalation is NOT a standard deterministic computation — mostly contractual and non-standard

---

## 9. DMCI-Specific: Rent-to-Own (HomeReady)

- Lease term: 24–36 months
- 60% of total lease payments credited toward DP
- After lease: 10% DP remaining + 90% balance via financing
- Price locked at lease start ("Price Protect")
- Can opt out with no penalties (lease contract, not CTS)
- 36-month term: 10% rent increase in year 3

---

## 10. Key Deterministic Computations Identified

From this source acquisition, the following computations are clearly deterministic and parameterized:

1. **Monthly equity installment** — `(TCP × dp% - reservation_fee) / months`
2. **Spot cash net price** — `TCP × (1 - discount%)`
3. **Scaled discount by DP%** — lookup table (DMCI model, Alveo model)
4. **Late payment penalty** — simple (rate × months) or escalating (DMCI)
5. **Turnover balance** — `TCP × (1 - dp%) - discounts`
6. **Closing cost estimation** — sum of DST + transfer tax + registration + notarial + utilities + advance dues
7. **TCP with VAT and charges** — `list_price × (1 + other_charges%) × (1 + VAT% if applicable)`
8. **Association dues advance** — `unit_sqm × rate_per_sqm × advance_months`
9. **DMCI HomeReady DP credit** — `total_lease_paid × 60%`
10. **Annual lump-sum (Megaworld)** — `TCP × lump_sum% × number_of_years`

**Non-deterministic / excluded:**
- Price escalation clauses (contractual, non-standard)
- In-house financing interest rates (internal memos, not published)
- Project-specific promo discounts (change frequently)

---

## Sources

### Ayala Land Group
- Avida Land home financing: avidaland.com/home-financing.php
- Avida Towers Cloverleaf sample computations: cloverleafavida.wordpress.com
- Alveo buying guide: alveoland.com.ph/buying-guide/
- Montala Alviera (Alveo) payment terms: ayalalandalviera.com
- Amaia Land home financing: amaialand.com/home-financing/

### SMDC
- SMDC Terms and Services: smdc.com/terms-and-services/
- SMDC Payment Guidelines: smdc.com/payment-guidelines/
- Gold Residences computation: goldresidences.net/prices-and-computation/
- Mint Residences computation: mint-residences.com/price-and-computation/
- Sands Residences units/prices: sands-residences.com/units/
- MPlace payment terms: smmplace.weebly.com
- SMDC Move In Now (Philstar 2025/04/03): philstar.com/business/2025/04/03/2433003

### DMCI Homes
- DMCI Buyer's Guide: dmcihomes.com/guides/buyers-guide
- DMCI Price List 2025: dmciprojects.net/dmci-price/
- DMCI Payment Terms: dmcihomesworld.wordpress.com/payment-terms/
- DMCI HomeReady: dmcihomes.com/homeready

### Megaworld
- Megaworld Living reservation: megaworldliving.com/how-to-reserve-a-unit-in-megaworld
- Megaworld BGC Uptown Modern: megaworldbgccondo.com
- Megaworld Iloilo FAQ: iloilocondominiums.com/faq/
- Megaworld Horizon financing guide: megaworldhorizon.com

### Legal / Industry
- Respicio.ph — late payment penalties, CTS vs DOAS, hidden charges
- Filipino Law Group — missed payments
- BSP Circular 799 (legal interest 6% p.a.)
- BSP Circular 957 (anti-predatory lending)
- PD 957 (subdivision/condo buyer protection)
- Orbe v. Filinvest (G.R. No. 208185) — escalation clause jurisprudence
