# PRC & RESA Broker Commission Regulations — Source Extraction

**Aspect:** prc-broker-regulations (Wave 1)
**Date:** 2026-02-26
**Sources:**
- RA 9646 (Real Estate Service Act of the Philippines, 2009) — primary statute
- RESA IRR (PRBRES implementing rules, published ~2010) — implementing regulations
- Revenue Regulations No. 10-2013 — withholding tax rates for real estate service practitioners
- Revenue Regulations No. 30-2003 — affidavit requirement for 10% EWT rate
- Civil Code of the Philippines (RA 386), Art. 1305 — contractual basis for commission agreements
- Practitioner sources: Respicio & Co., iRealtee, HousingInteractive, Verizon PH, PhilPropertyExpert, Lamudi, ForeclosurePhilippines

---

## Part A: Legal Framework — RA 9646 (RESA)

### Key Definitions

**Real Estate Broker** (Sec. 3(g)(4)):
> "A duly registered and licensed natural person who, for a professional fee, commission or other valuable consideration, acts as an agent of a party in a real estate transaction to offer, advertise, solicit, list, promote, mediate, negotiate or effect the meeting of the minds on the sale, purchase, exchange, mortgage, lease, or joint venture, or other similar transactions on real estate or any interest therein."

**Real Estate Salesperson** (Sec. 3(g)(5)):
> "A duly accredited natural person who performs service for, and in behalf of a real estate broker who is registered and licensed by the Professional Regulatory Board of Real Estate Service for or in expectation of a share in the commission, professional fee, compensation or other valuable consideration."

### Salesperson Compensation Restriction (Sec. 31)
> "No salesperson shall be entitled to receive or demand a fee, commission or compensation of any kind from any person, other than the duly licensed real estate broker who has direct control and supervision over him, for any service rendered or work done by such salesperson in any real estate transaction."

**Key implication for computation:** Salesperson compensation is always a derivative of the broker's commission — the salesperson cannot independently charge the client. All commission computation flows through the broker.

### Licensing Requirements
- Brokers: Must pass PRC licensure examination
- Salespersons: Accredited (no exam), must complete 2 years college + Board-required training
- Salesperson must be under direct supervision of a licensed broker
- Salesperson cannot be signatory to agreements unless supervising broker also signs

### Penalties for Unlicensed Practice (Sec. 39)
- Licensed practitioner violation: Fine ≥ ₱100,000 or imprisonment ≥ 2 years, or both
- Unlicensed practitioner violation: Doubled — fine ≥ ₱200,000 or imprisonment ≥ 4 years, or both

---

## Part B: Commission Rates — No Statutory Schedule

### Critical Finding: RESA Does NOT Prescribe Commission Rates

Neither RA 9646 nor its IRR mandate any specific commission rate schedule. Commission rates are contractual, governed by the Civil Code (Art. 1305 — meeting of minds). The PRBRES has not issued any resolution establishing mandatory or recommended commission rates as of 2026.

This is a fundamental structural difference from some other jurisdictions — Philippine broker commissions are entirely market-driven.

### Industry-Standard Rates (Practice, Not Law)

#### Sale Transactions

| Property Type | Commission Rate | Notes |
|---|---|---|
| General sales (industry standard) | 3%–5% of selling price | 5% most commonly cited as "standard" |
| Horizontal projects (economic housing) | 6%–7% | Higher due to competitive, high-demand nature |
| Vertical projects (condominiums) | 3%–5% | Standard developer commission range |
| Pre-owned / secondary market | ~5% | Broker may bear additional marketing expenses |

**Formula (sale):**
```
gross_commission = selling_price × commission_rate
```

#### Lease Transactions — Residential

**Industry standard:** 1 month's rent per year of lease term.

**Formula:**
```
lease_commission = monthly_rent × lease_years
```

Example: ₱30,000/month rent, 2-year lease → commission = ₱30,000 × 2 = ₱60,000

Broker entitled to commission again on renewal.

#### Lease Transactions — Commercial

**Industry standard:** 3%–6% of total lease value (cumulative rent over entire term).

**Formula:**
```
total_lease_value = monthly_rent × lease_months
commercial_lease_commission = total_lease_value × commission_rate
```

Example: ₱100,000/month, 5-year lease → total value = ₱6,000,000 → at 5% = ₱300,000

---

## Part C: Commission Split Structures

### Broker–Salesperson Split
No mandatory split ratio. Common arrangements:
- **50/50** — equal split between broker and salesperson (most commonly cited)
- **60/40** — broker 60%, salesperson 40%
- **80/20** — firm retains 80%, agent 20% (common for new agents)
- **100% to agent** — agent pays desk/platform fee instead (less common in PH)

### Listing Broker–Selling Broker Split (Co-brokerage / MLS)
- **50/50** between listing broker and selling broker is standard in MLS arrangements
- Not mandatory; governed by MLS or co-brokerage agreement

### Developer Commission Distribution (Brokerage Firm Hierarchy)
Example from iRealtee (₱5M TCP at 5% = ₱250,000 gross):

| Tier | Percentage | Amount |
|---|---|---|
| Brokerage retention | 20% | ₱50,000 |
| Selling agent | 60% | ₱120,000* |
| Unit manager override | 15% | ₱30,000* |
| Division manager override | 10% | ₱20,000* |

*Percentages of remaining ₱200,000 after brokerage retention.

Note: Tier percentages must sum correctly. The ₱250,000 → 20% retention (₱50,000) → remaining ₱200,000 split 60/15/10 among agent tiers = ₱120,000 + ₱30,000 + ₱20,000 = ₱170,000, leaving ₱30,000 unallocated (likely other overrides or reserves). Actual structures vary by brokerage.

### Developer-Specific Commission Rates

| Developer | Published Rate | Notes |
|---|---|---|
| SMDC | 4.75% + incentives | Publicly stated; claims "highest in industry" |
| DMCI Homes | 3%–5% (est.) | Not publicly disclosed; requires accreditation training |
| Ayala Land / Alveo / Avida | 3%–5% (est.) | Not publicly disclosed; formal D&B pre-qualification |
| Megaworld | 3%–5% (est.) | Not publicly disclosed |

---

## Part D: Tax Treatment of Commissions

### Expanded Withholding Tax (EWT) — RR 10-2013

| Practitioner Status | Annual Gross Income | EWT Rate |
|---|---|---|
| PRC-licensed RESP | > ₱720,000 | 15% |
| PRC-licensed RESP | ≤ ₱720,000 | 10% |
| Unlicensed practitioner | Any | 10% (flat) |

**Requirement for 10% rate (RR 30-2003):** Licensed practitioner must provide payor an **Affidavit — Declaration of Current Year's Gross Income**. Without affidavit → 15% applies.

**Formula:**
```
ewt = gross_commission × ewt_rate
net_commission = gross_commission - ewt
```

### VAT on Commissions
- **12% VAT** applies if broker's annual gross sales exceed **₱3,000,000** threshold
- Below threshold: exempt from VAT

**Formula (if VAT-registered):**
```
vat = gross_commission × 0.12
total_payable_by_payor = gross_commission + vat  # or VAT-inclusive pricing
```

---

## Part E: Procuring Cause Doctrine

Philippine jurisprudence applies the "procuring cause" doctrine for commission entitlement. The broker who is the "efficient procuring cause" — whose efforts directly led to the consummation of the sale or lease — is entitled to commission.

This is **not a computation** but a legal determination relevant to disputes. It affects *whether* commission is payable, not *how much*.

---

## Part F: Commission Payment Timing

### Developer Sales
- **Spot cash:** Commission released upon document completion
- **Installment/financing:** Commission release depends on developer's commission scheme — may be triggered by buyer's down payment completion, loan takeout, or turnover

### Pre-Owned / Secondary Market
- Commission released upon deal closing (payment receipt + DOAS signing)

### Lease
- **Upfront:** Full commission upon lease signing
- **Staggered:** 50% at move-in, 25% at mid-lease, 25% at lease end (per PhilPropertyExpert policy example)
- Terms governed by individual brokerage agreements

---

## Part G: Computation-Relevant Provisions for Wave 2

The following computations can be extracted for the broker-commission aspect:

1. **Sale commission computation** — inputs: selling_price, commission_rate → output: gross_commission. Simple percentage. Deterministic given inputs.

2. **Residential lease commission** — inputs: monthly_rent, lease_years → output: commission (1 month/year). Deterministic.

3. **Commercial lease commission** — inputs: monthly_rent, lease_months, commission_rate → output: commission (% of total lease value). Deterministic.

4. **Commission split computation** — inputs: gross_commission, split_ratio (varies by arrangement type) → outputs: broker_share, agent_share. Deterministic given contractual split.

5. **Multi-tier distribution** — inputs: gross_commission, brokerage_retention_%, agent_%, manager_override_%, ... → outputs: per-tier amounts. Deterministic given hierarchy config.

6. **EWT computation** — inputs: gross_commission, practitioner_licensed (bool), annual_gross_income, has_affidavit (bool) → output: ewt_amount. Deterministic per RR 10-2013.

7. **VAT computation** — inputs: gross_commission, broker_annual_gross_sales → output: vat_amount (12% if above ₱3M, else 0). Deterministic.

8. **Net commission after tax** — inputs: gross_commission, ewt, vat → output: net_receivable. Deterministic.

**Key observation:** While individual commission *rates* are contractual (not regulated), the *computation mechanics* once rates are agreed are fully deterministic. The automation opportunity lies in: (a) providing rate benchmarks by property type, (b) computing multi-tier splits, (c) automatically calculating tax withholdings, and (d) generating BIR Form 2307 certificates.
