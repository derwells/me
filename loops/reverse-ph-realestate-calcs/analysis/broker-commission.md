# Real Estate Broker Commission Computation — Wave 2 Extraction

**Aspect:** broker-commission (Wave 2)
**Date:** 2026-02-27
**Primary source:** `input/prc-broker-regulations.md`
**Verification:** Independent subagent cross-checked 15 claims against 22+ secondary sources (law firms, BIR resources, tax consultancies, developer sites, MLS platforms)

---

## Critical Correction from Wave 1

**The Wave 1 source cites pre-TRAIN EWT rates (RR 10-2013: 10%/15% at ₱720K threshold) as current.** These were superseded by **RR No. 11-2018** (implementing TRAIN Law, RA 10963), effective January 1, 2018. The correct current rates for individual licensed brokers are **5%/10% at ₱3M threshold**, not 10%/15% at ₱720K.

**Severity: HIGH** — directly affects net commission computation. An individual broker earning ₱2M/year would have EWT overstated by 100% (₱200K vs. correct ₱100K).

---

## Regulatory Framework Summary

### Key Structural Finding: No Statutory Rate Schedule

RA 9646 (RESA) defines broker/salesperson roles and licensing requirements but does **NOT** prescribe commission rates. Rates are contractual, governed by Civil Code Art. 1306 (freedom of contract). Neither the PRBRES nor PRC has issued any resolution recommending rates as of February 2026.

**Implication for automation:** Commission *rates* are inputs (contractual), not computed values. The automation opportunity lies in: (a) rate benchmarking by property type, (b) multi-tier split computation, (c) tax withholding calculation, (d) BIR form generation.

### Regulatory Stack

| Layer | Authority | What It Governs |
|---|---|---|
| RA 9646 (RESA) | Statute | Licensing, practice scope, salesperson restrictions |
| RESA IRR | PRBRES | Implementing rules for licensing/supervision |
| Civil Code Art. 1306 | General law | Contractual basis for commission agreements |
| RR 11-2018 (TRAIN) | BIR | Current EWT rates for professional fees |
| NIRC as amended by TRAIN | BIR | VAT threshold (₱3M), percentage tax (3%), 8% flat option |

---

## Extracted Computations

### Computation 1: Sale Commission (Gross)

**Deterministic: YES** (given contractual rate)

**Inputs:**
- `selling_price` (₱): contract price or TCP
- `commission_rate` (decimal): contractually agreed rate

**Formula:**
```
gross_commission = selling_price × commission_rate
```

**Rate Benchmarks (industry standard, NOT regulated):**

| Property Type | Typical Rate | Source Quality |
|---|---|---|
| Condominium (vertical) | 3%–5% | Confirmed, 6+ sources |
| Subdivision (horizontal) | 3%–5% | Confirmed, 6+ sources |
| Economic/socialized housing (horizontal) | 6%–7% | Confirmed, 3 sources |
| Pre-owned / secondary market | 2.5%–5% | Confirmed, 4 sources |
| Foreclosed / bank-owned (ROPA) | 3%–5% | Confirmed, 3 sources |

**Developer-specific rates:**

| Developer | Rate | Verification |
|---|---|---|
| SMDC | 4.75% + incentives | UNVERIFIED — widely cited in practitioner circles but not publicly confirmed |
| Ayala Land group | 3%–5% | General range only; requires formal accreditation |
| DMCI Homes | 3%–5% | General range only; accreditation required |
| Megaworld | 3%–5% | General range only |
| Vista Land (Camella, Crown Asia) | 3%–5%, up to 6–7% for horizontal | General range |

**Example:**
- ₱5,000,000 TCP at 5%: gross_commission = ₱250,000

**Verification:** CONFIRMED — 3–5% range unanimous across all 22+ sources; 5% as "standard" confirmed.

### Computation 2: Residential Lease Commission

**Deterministic: YES**

**Inputs:**
- `monthly_rent` (₱): agreed monthly rental
- `lease_years` (integer): lease term in years

**Formula:**
```
lease_commission = monthly_rent × lease_years
```

**Edge cases:**
- Partial-year lease: prorate (e.g., 1.5 years = 1.5 × monthly_rent)
- Renewal: broker customarily entitled to commission again on renewal (industry practice, not statutory)
- Referral scenario: if another agent referred the tenant, referral fee (commonly 20% of agent's share) is deducted from the salesperson's portion

**Example:**
- ₱30,000/month, 2-year lease: commission = ₱60,000

**Verification:** CONFIRMED — consistent across 5 independent sources.

### Computation 3: Commercial Lease Commission

**Deterministic: YES** (given contractual rate)

**Inputs:**
- `monthly_rent` (₱): agreed monthly rental
- `lease_months` (integer): total lease term in months
- `commission_rate` (decimal): contractually agreed rate (typically 3%–6%)

**Formula:**
```
total_lease_value = monthly_rent × lease_months
commercial_lease_commission = total_lease_value × commission_rate
```

**Example:**
- ₱100,000/month, 5-year lease at 5%: ₱100K × 60 × 0.05 = ₱300,000

**Verification:** CONFIRMED — Respicio & Co. independently produced identical computation example.

### Computation 4: Broker–Salesperson Split

**Deterministic: YES** (given contractual split ratio)

**Inputs:**
- `gross_commission` (₱): from Computation 1, 2, or 3
- `split_type` (enum): determines ratio
- `referral_fee_pct` (decimal, optional): if referral agent involved

**Common Split Ratios:**

| Arrangement | Broker Share | Agent Share | Context |
|---|---|---|---|
| 50/50 | 50% | 50% | Most common starting point for new salespersons |
| 60/40 | 40% | 60% | Experienced salesperson negotiation |
| 80/20 (firm-heavy) | 80% | 20% | New agents at large firms |
| 80/20 (agent-heavy) | 20% | 80% | Top producers |
| 100/0 | 0% | 100% | Agent pays desk/platform fee instead |

**Formula:**
```
broker_share = gross_commission × broker_pct
agent_share = gross_commission × agent_pct

# If referral involved:
referral_fee = agent_share × referral_fee_pct
agent_net = agent_share - referral_fee
```

**Key constraint (RESA Sec. 31):** Salesperson can ONLY receive compensation from their supervising broker. The client pays the broker; the broker pays the salesperson. This is statutory, not just convention.

**Verification:** CONFIRMED — all split ratios confirmed. Note: 80/20 direction is ambiguous across sources (both interpretations exist in practice).

### Computation 5: Multi-Tier Brokerage Distribution

**Deterministic: YES** (given hierarchy configuration)

**Inputs:**
- `gross_commission` (₱)
- `retention_pct` (decimal): brokerage firm retention
- `tier_splits[]` (array of {role, pct}): distribution tiers after retention

**Formula:**
```
firm_retention = gross_commission × retention_pct
distributable = gross_commission - firm_retention

for each tier in tier_splits:
    tier_amount = distributable × tier.pct
```

**iRealtee Model (one documented example):**
```
firm_retention = gross_commission × 0.20
distributable = gross_commission × 0.80
selling_agent = distributable × 0.60
unit_manager = distributable × 0.15
division_manager = distributable × 0.10
other_overrides = distributable × 0.15  # reserve/other tiers
```

**Example (₱5M TCP at 5% = ₱250K gross):**
- Firm retention: ₱50,000
- Selling agent: ₱120,000
- Unit manager override: ₱30,000
- Division manager override: ₱20,000
- Other overrides/reserve: ₱30,000

**Verification:** CONFIRMED as iRealtee-specific model (Manila Times 2026 coverage). Not a universal standard — each brokerage defines its own tier structure.

### Computation 6: Co-Brokerage (MLS) Split

**Deterministic: YES**

**Inputs:**
- `gross_commission` (₱): total commission on the transaction
- `mls_split_ratio` (decimal): typically 50/50

**Formula:**
```
listing_broker_share = gross_commission × 0.50
selling_broker_share = gross_commission × 0.50
```

Each broker then distributes their share per their own internal split (Computation 4 or 5).

**Example (₱5M sale at 5% = ₱250K):**
- Listing broker: ₱125,000
- Selling broker: ₱125,000
- Equivalent to 2.5% each of selling price

**Verification:** CONFIRMED — CEREBMLS (PHMLS) rules explicitly establish 50/50 split.

### Computation 7: Expanded Withholding Tax (EWT) on Commission

**Deterministic: YES**

**Inputs:**
- `gross_commission` (₱): gross professional fee (exclusive of VAT if VAT-registered)
- `payee_type` (enum): individual | corporate
- `annual_gross_income` (₱): payee's declared annual gross
- `has_sworn_declaration` (bool): whether payee submitted Sworn Declaration per RR 11-2018

**Formula (CURRENT — post-TRAIN, RR 11-2018):**
```
if payee_type == "individual":
    if has_sworn_declaration and annual_gross_income <= 3_000_000:
        ewt_rate = 0.05  # 5%
    else:
        ewt_rate = 0.10  # 10% (default / gross > ₱3M)
elif payee_type == "corporate":
    if annual_gross_income <= 720_000:
        ewt_rate = 0.10  # 10%
    else:
        ewt_rate = 0.15  # 15%

ewt = gross_commission × ewt_rate
```

**CRITICAL: EWT base for VAT-registered brokers:**
```
# If broker is VAT-registered, EWT is computed on fee EXCLUSIVE of VAT
ewt_base = gross_commission  # NOT gross_commission × 1.12
ewt = ewt_base × ewt_rate
```

**Sworn Declaration requirement (RR 11-2018, Annexes B-1 to B-3):**
- Must be submitted to all withholding agents by **January 15** each year
- Or prior to first payment of the year
- Without it: higher rate applies automatically (10% for individuals, 15% for corporates)

**Examples (individual licensed broker, ₱2M annual gross, has declaration):**
- ₱100,000 commission: EWT = ₱100K × 5% = ₱5,000
- **Primary source would have computed:** ₱100K × 10% = ₱10,000 (WRONG — uses pre-TRAIN rates)

**Legal basis:** RR No. 11-2018 (implementing RA 10963 / TRAIN Law), superseding RR 10-2013.

**Verification:** CORRECTED — 6 authoritative sources confirm TRAIN Law rates (Tax and Accounting Center, PWC Philippines, Forvis Mazars, Triple-i Consulting, iRealtee, Filepino).

### Computation 8: VAT on Commission

**Deterministic: YES**

**Inputs:**
- `gross_commission` (₱): professional fee amount
- `broker_annual_gross` (₱): broker's annual gross receipts/sales
- `vat_inclusive` (bool): whether quoted fee is VAT-inclusive

**Formula:**
```
if broker_annual_gross > 3_000_000:
    # VAT-registered broker
    if vat_inclusive:
        vat = gross_commission / 1.12 × 0.12
        net_of_vat = gross_commission / 1.12
    else:
        vat = gross_commission × 0.12
        total_payable = gross_commission + vat
else:
    # Non-VAT broker: percentage tax (3%) or 8% flat option
    vat = 0
    # Broker pays 3% percentage tax on gross OR 8% flat income tax
```

**Tax options for non-VAT brokers (annual gross ≤ ₱3M):**

| Option | Rate | Basis | What It Replaces |
|---|---|---|---|
| Graduated income tax + 3% percentage tax | Varies + 3% | Graduated brackets + gross receipts | Standard |
| 8% flat income tax | 8% | Gross receipts in excess of ₱250K | Graduated income tax AND percentage tax |

**Verification:** CONFIRMED — ₱3M threshold verified as current (TRAIN Law, unchanged as of Feb 2026).

### Computation 9: Net Commission After Tax

**Deterministic: YES**

**Inputs:**
- `gross_commission` (₱)
- `ewt` (₱): from Computation 7
- `vat` (₱): from Computation 8 (if VAT-exclusive billing)

**Formula:**
```
# Broker perspective (what broker actually receives):
net_receivable = gross_commission - ewt

# If VAT-registered and billing VAT-exclusive:
# Client pays: gross_commission + vat
# Broker receives: gross_commission + vat - ewt
# Broker remits: vat (less input VAT credits)
# Broker's net: gross_commission - ewt (same)
```

**Full Example (₱5M sale, individual broker, ₱2M annual gross, has declaration):**
```
selling_price     = ₱5,000,000
commission_rate   = 5%
gross_commission  = ₱250,000
ewt (5%)          = ₱12,500
net_receivable    = ₱237,500

# BIR Form 2307 issued by payor: ₱12,500 creditable tax
```

**Full Example (₱5M sale, VAT-registered broker, >₱3M annual gross, no declaration):**
```
selling_price     = ₱5,000,000
commission_rate   = 5%
gross_commission  = ₱250,000
vat (12%)         = ₱30,000
total_billed      = ₱280,000
ewt (10%, on ₱250K) = ₱25,000
net_receivable    = ₱280,000 - ₱25,000 = ₱255,000
# Broker remits ₱30,000 VAT (less input credits)
# Effective net after VAT remittance: ₱225,000
```

### Computation 10: Finder's Fee (Distinct from Commission)

**Deterministic: CONDITIONAL** (if fee structure agreed)

**Inputs:**
- `transaction_value` (₱): selling price
- `finder_fee_rate` (decimal): typically 1%–2% (lower than brokerage commission)

**Formula:**
```
finder_fee = transaction_value × finder_fee_rate
```

**Legal distinction from broker commission:**

| Aspect | Broker Commission | Finder's Fee |
|---|---|---|
| Licensing | PRC license required (RESA) | No license required |
| Scope | Full brokerage: negotiate, mediate, close | Introduction/referral ONLY |
| Typical rate | 3%–5% | 1%–2% |
| Legal basis | Contract of agency | Quantum meruit (Art. 2142, Civil Code) |
| Risk | Regulated practice | Must NOT cross into brokerage activities |
| Penalty if unlicensed | ₱200K fine and/or 4 years imprisonment | N/A if limited to referral |

**Verification:** CONFIRMED — functional scope test confirmed (if finder negotiates → unlicensed brokerage).

### Computation 11: Rent-to-Own Commission

**Deterministic: YES** (once transaction structure is determined)

**Inputs:**
- `total_contract_price` (₱): TCP of the rent-to-own unit
- `commission_rate` (decimal): standard sale rate (3%–5%)
- `transaction_structure` (enum): "sale" | "lease_with_option"

**Formula:**
```
if transaction_structure == "sale":
    # Most common for developer rent-to-own programs
    commission = total_contract_price × commission_rate
elif transaction_structure == "lease_with_option":
    # Rare: separate lease and purchase commissions
    lease_commission = monthly_rent × lease_years
    # Purchase commission triggered only if option exercised
    purchase_commission = purchase_price × commission_rate
```

**Verification:** CONFIRMED as market practice (developer programs treated as sales). No authoritative guidance found for lease-with-option split.

---

## BIR Forms for Commission Tax Compliance

| Form | Purpose | Filed By |
|---|---|---|
| **2307** | Certificate of Creditable Tax Withheld at Source | Issued by payor (developer/owner) to broker |
| **1601-EQ** | Quarterly Remittance of EWT | Withholding agent |
| **2550M** | Monthly VAT Declaration | VAT-registered brokers |
| **2550Q** | Quarterly VAT Return | VAT-registered brokers |
| **2551Q** | Quarterly Percentage Tax Return | Non-VAT brokers (3% option) |
| **1701** | Annual Income Tax Return (self-employed) | Broker |
| **1701Q** | Quarterly Income Tax Return | Broker |

**Most critical for brokers:** BIR Form 2307 — without it, broker cannot claim tax credits for EWT withheld at source.

---

## Edge Cases and Special Rules

### 1. Procuring Cause Doctrine
Philippine jurisprudence applies the "efficient procuring cause" doctrine (Civil Code Art. 1875) to determine commission entitlement. The broker whose efforts directly led to the sale is entitled to commission. This is a **legal determination** (not a computation) but affects **whether** commission is payable.

Key SC decisions:
- *Inland Realty Corp. v. CA* (G.R. No. 112051, 1996) — ready, willing, able buyer test
- *Prudential Bank v. CA* (G.R. No. 103957, 1993) — original broker prevails
- *Ticong v. Malim* (G.R. No. 220785) — foundation of negotiation, not just introduction

### 2. Prescription Periods for Commission Claims
- Written contract: 10 years (Art. 1144, Civil Code)
- Oral contract: 6 years (Art. 1145, Civil Code)

### 3. Commission Payment Timing
- **Developer sales (spot cash):** Released upon document completion
- **Developer sales (installment/financing):** Triggered by DP completion, loan takeout, or turnover (varies by developer)
- **Pre-owned/secondary:** Upon deal closing (payment + DOAS signing)
- **Lease:** Upfront at signing, or staggered (50/25/25 — move-in/mid-lease/end)

### 4. Property Management Fees (Separate from Commission)
Not a brokerage commission but a related recurring fee computation:
- Residential: ~10% of monthly rent collected
- Commercial: 3%–10% of rental income
- Fixed-fee model: ₱5,000–₱15,000/month per property

### 5. Foreclosed Property (ROPA) Commission
- Banks: 3%–5% (BPI confirmed at 5% via Buena Mano program)
- Pag-IBIG: historically 5% but removed accredited broker list as of September 2019; directs buyers to deal directly with the Fund now

---

## Verification Summary

| Claim | Verdict | Notes |
|---|---|---|
| RESA does not prescribe rates | CONFIRMED | Art. 1306 (not 1305) is more precise citation |
| Sale commission 3–5%, 5% standard | CONFIRMED | Unanimous, 6+ sources |
| Horizontal/economic: 6–7% | CONFIRMED | 3 sources |
| Residential lease: 1 month/year | CONFIRMED | 5 sources |
| Commercial lease: 3–6% total value | CONFIRMED | Identical worked example in Respicio |
| Splits: 50/50, 60/40, 80/20 | CONFIRMED | 80/20 direction ambiguous (both exist) |
| SMDC 4.75% | UNVERIFIED | Plausible but not publicly confirmed |
| EWT: 10%/15% at ₱720K (RR 10-2013) | **CORRECTED** | Superseded: 5%/10% at ₱3M for individuals (RR 11-2018) |
| Affidavit for 10% rate (RR 30-2003) | **CORRECTED** | Now "Sworn Declaration" under RR 11-2018 for 5% rate |
| VAT: 12% if gross > ₱3M | CONFIRMED | TRAIN Law threshold, unchanged |
| Salesperson only from broker (Sec. 31) | CONFIRMED | Exact statutory language verified |
| Multi-tier: 20%/60/15/10 (iRealtee) | CONFIRMED | One model, not universal |
| MLS co-broke split: 50/50 | CONFIRMED | CEREBMLS rules explicit |
| Procuring cause doctrine | CONFIRMED | Multiple SC decisions |
| Renewal commission | CONFIRMED | Industry practice, not statutory |

**Overall: 12 CONFIRMED, 2 CORRECTED, 1 UNVERIFIED**

---

## Determinism Assessment

| Computation | Deterministic? | Key Dependency |
|---|---|---|
| Sale commission (gross) | YES | Rate is contractual input |
| Residential lease commission | YES | Standard formula |
| Commercial lease commission | YES | Rate is contractual input |
| Broker–salesperson split | YES | Split ratio is contractual input |
| Multi-tier distribution | YES | Tier config is contractual input |
| Co-brokerage (MLS) split | YES | 50/50 standard per CEREBMLS |
| EWT computation | YES | RR 11-2018 rates (post-TRAIN) |
| VAT computation | YES | ₱3M threshold per TRAIN Law |
| Net commission after tax | YES | Derived from above |
| Finder's fee | CONDITIONAL | Rate negotiated; scope test is legal judgment |
| Rent-to-own commission | YES | Once structure determined (sale vs. lease) |
| Property management fee | YES | Given agreed rate; rate itself negotiated |

**Overall: 11 computations are fully deterministic given contractual inputs. Commission rates themselves are non-deterministic (contractual), but the computation mechanics are entirely deterministic.**

---

## Automation Opportunity Assessment (for Wave 4)

1. **Multi-tier commission split calculator** — HIGH value. Complex arithmetic that brokerages do manually or in spreadsheets. Configurable tier structures, referral deductions, co-brokerage splits.

2. **Net commission calculator with tax** — HIGH value. Most practitioners don't correctly compute post-TRAIN EWT rates. Critical: many online resources still cite pre-2018 rates. First-mover advantage in getting this right.

3. **BIR Form 2307 generator** — HIGH value. Every commission payment requires this certificate. Auto-generating from commission computation saves significant compliance effort.

4. **Commission rate benchmarking engine** — MEDIUM value. Database of industry rates by property type, developer, and location. High data acquisition cost but unique competitive moat.

5. **Closing cost aggregator** — HIGH value (as component). Commission is one of 5–7 closing cost items. Cross-references: ROD registration fees (analysis/rod-registration-fees.md), notarial fees (analysis/notarial-fees.md), and tax computations (ph-tax-computations-reverse loop).

---

## Legal Citations

| Citation | Description |
|---|---|
| RA 9646 (RESA) | Real Estate Service Act (2009); licensing, practice scope |
| RA 9646 Sec. 31 | Salesperson compensation restriction |
| Civil Code Art. 1306 | Freedom of contract (commission rate basis) |
| Civil Code Art. 1875 | Agency relationship (procuring cause basis) |
| Civil Code Art. 2142 | Quantum meruit (finder's fee basis) |
| RR No. 11-2018 | Current EWT rates for professionals (post-TRAIN) |
| RA 10963 (TRAIN Law) | VAT threshold ₱3M, 8% flat tax option |
| RR No. 10-2013 | SUPERSEDED EWT rates (pre-TRAIN); still applies to corporates |
| RR No. 30-2003 | Original affidavit requirement (concept preserved in RR 11-2018) |
| PRBRES Res. No. 11 (2021) | Supervision guidelines for salespersons |
| CEREBMLS Rules | 50/50 co-brokerage split |

**Cross-references:**
- Tax withholding computations → `loops/ph-tax-computations-reverse/` (EWT/VAT are tax topics but included here because they directly affect net commission)
- ROD registration fees → `analysis/rod-registration-fees.md`
- Notarial fees → `analysis/notarial-fees.md`
- Developer payment terms → `analysis/developer-equity-schedule.md` (commission timing tied to DP/turnover milestones)
