# Lease Renewal & Extension Processing — Process Analysis & Feature Spec

*Analyzed: 2026-02-26 | Wave 2 | Depends on: lease-contract-requirements, rent-control-rules, corporate-rental-tax, crispina-models, crispina-services, security-deposit-rules*

---

## 1. Process Description

**What:** Manage the full lifecycle of lease continuity events — formal renewal (new contract replacing expired one), extension (addendum prolonging existing contract), and tacit reconduction (implied month-to-month continuation after 15-day holdover with acquiescence). Includes deposit adjustment, escalation application, DST filing, and board resolution requirements for each scenario.

**When:**
- **Proactive:** 60-90 days before lease expiry — initiate renewal/extension negotiation
- **At expiry:** Execute renewal contract or extension addendum, or send notice of non-renewal
- **Post-expiry (unintentional):** Detect tacit reconduction if tenant continues past 15 days without notice

**Who does it:** Property manager initiates, negotiates terms, prepares documents. Board resolution (if needed) from corporate governance. Notary for execution. BIR Form 2000 for DST filing.

**Frequency:** With 20-100 units, approximately 20-50 renewal events per year (most leases are 1-2 years). Cluster around common lease start months.

---

## 2. Current Method

**Fully manual / ad hoc.** No systematic tracking of upcoming expirations.

Current workflow:
1. Property manager checks lease files periodically (or tenant asks about renewal)
2. Negotiate new terms informally
3. Either draft a new contract (from Word template) or verbal agreement to continue
4. Sometimes no action taken → lease drifts into tacit reconduction without awareness
5. DST on renewal frequently missed or filed late
6. Deposit top-up not consistently collected when rent increases
7. No record of which leases are in month-to-month holdover status

**Pain points:**
- Unintentional tacit reconduction creates ejectment complications for controlled units
- Missed DST filings → penalty exposure (25% surcharge + 12% interest)
- No visibility into upcoming expirations across the portfolio
- Deposit adjustment on renewal is inconsistent
- No board resolution linkage for renewed leases
- Holdover tenants not systematically identified or managed

---

## 3. Regulatory Rules with Legal Citations

### Rule 1: Three Lease Continuity Scenarios

PH law recognizes three distinct ways a lease can continue beyond its original term:

| Scenario | Legal Basis | New Document? | DST? | Effect |
|----------|------------|---------------|------|--------|
| **Renewal** (new contract) | Art. 1306 (freedom of contract) | Yes — full new contract | Yes — full DST for new term | Fresh contract; all terms negotiable |
| **Extension** (addendum) | Art. 1306 | Yes — addendum/amendment | Yes — DST on extension period only | Same contract prolonged; amended terms |
| **Tacit reconduction** | Civil Code Art. 1670 | No | No (no document to stamp) | Implied month-to-month; original terms except period and guaranty |

**Verification:** CONFIRMED — NIRC Sec. 194 taxes the *document*, not the underlying lease. No document = no DST. Respicio.ph, accountaholicsph.com, BIR FOI response all confirm DST attaches "on each lease, agreement, memorandum, or contract." Tacit reconduction arises by operation of law, not by document execution.

### Rule 2: Tacit Reconduction (Art. 1670)

**Three elements required** (SC: *Samelo v. Manotok Services*, G.R. No. 170509; *Buce v. Sps. Galeon*, G.R. No. 222785, Mar. 2, 2020):

1. Original lease term has expired
2. Lessor has NOT given notice to vacate
3. Lessee continued enjoying the property for **15 days** with lessor's acquiescence

**Effect:**
- Implied new lease created — NOT for original term
- Period: month-to-month for urban property with monthly rent (Art. 1687)
- **Original terms revived** — except the period and guaranty/surety obligations (Art. 1672)
- Month-to-month lease is "with a definite period" — terminable at end of each month upon demand to vacate

**Art. 1672 — Guaranty/surety extinguished:** If the original lease had a third-party guarantor, the guaranty does NOT survive tacit reconduction. The surety is released from liability for the implied renewed lease.

**Verification:** CONFIRMED — lawphil.net (Arts. 1670, 1672, 1687), *Paterno v. Court of Appeals* (G.R. No. 115763), *Buce v. Galeon* (G.R. No. 222785). All three elements consistently applied across SC jurisprudence.

### Rule 3: Notice Requirements to Prevent Tacit Reconduction

**What constitutes valid objection (prevents implied renewal):**

| Action | Effect | Citation |
|--------|--------|----------|
| Written notice of non-renewal | Prevents reconduction | Art. 1670; *Buce v. Galeon* |
| Notice to vacate (before or after expiry) | Prevents reconduction | *Samelo v. Manotok* (G.R. 170509) |
| Filing ejectment case | Evidence of objection | *Buce v. Galeon* (G.R. 222785) |
| Verbal objection alone | **Insufficient** — written notice best practice | Art. 1670 (interpreted strictly) |
| Continued acceptance of rent after notice | **Ambiguous** — may negate notice | Jurisprudential risk area |

**Key nuance:** The notice need NOT be given before the lease expires. A notice given within the 15-day window still prevents reconduction (*Buce v. Galeon*). However, best practice is to give notice 60-90 days before expiry.

**For controlled units (RA 9653 Sec. 9(c)):** If the non-renewal is for owner-use repossession, the lessor must give **3-month written advance notice** AND cannot re-lease for 1 year after repossession.

**Verification:** CONFIRMED — *Buce v. Galeon* (2020) is the leading case. Alburolaw.com, legalresource.ph, respicio.ph all consistent on the three-element test.

### Rule 4: Art. 1673(1) Suspension for Controlled Units (RA 9653 Sec. 12)

For rent-controlled residential units (NCR, monthly rent ≤ PHP 10,000):
- **Period expiry alone is NOT grounds for ejectment** — Art. 1673(1) is suspended
- This applies to BOTH original and tacitly renewed leases
- Lessor cannot eject simply because the lease term ended
- Valid ejectment grounds: non-payment (3 months arrears), unauthorized subletting, owner-use (with 3-month notice), condemnation order

**Practical implication:** Even if the lessor gives a non-renewal notice for a controlled unit, they can only eject for specific RA 9653 grounds. Simply not wanting to renew is insufficient unless it's for owner's use.

**Verification:** CONFIRMED — RA 9653 Sec. 12 text on lawphil.net; respicio.ph commentary; thecorpusjuris.com.

### Rule 5: DST on Renewals and Extensions (NIRC Sec. 194, TRAIN Law)

**Rate (post-TRAIN, RA 10963, effective Jan 1, 2018; RR 4-2018):**

| Portion of Annual Rent | DST |
|------------------------|-----|
| First PHP 2,000 (or fractional part) | **PHP 6.00** |
| Every PHP 1,000 (or fractional part) in excess | **PHP 2.00** additional |

Applied **per year** of the renewed/extended term.

**DST treatment by scenario:**

| Scenario | DST Base | Filing |
|----------|----------|--------|
| Renewal (new contract, 2-year term) | Full annual rent × 2 years | BIR Form 2000, 5 days after month-end of execution |
| Extension addendum (extending by 1 year) | Annual rent × 1 year (extension period only) | Same filing rule |
| Tacit reconduction | **No DST** — no document executed | N/A |
| Month-to-month holdover (written agreement) | Annual rent × fraction (if written for defined period) | If reduced to writing, DST applies |

**NIRC Sec. 198 reinforcement:** "Assignments and renewals of certain instruments" — DST on renewals at the same rate as the original. DST paid on original contract CANNOT be credited to renewal.

**Verification:** CONFIRMED — RR 4-2018 (SC E-Library: elibrary.judiciary.gov.ph), respicio.ph DST on lease commentary, BIR FOI response on Section 194. Rates confirmed as PHP 6/PHP 2 (doubled from pre-TRAIN PHP 3/PHP 1).

### Rule 6: NHSB Escalation Cap on Renewal

**NHSB 2024-01:** Cap applies to "same tenant continuing/renewing":
- 2025: **2.3%** for units ≤ PHP 10,000/month in the prior year
- 2026: **1%** for units ≤ PHP 10,000/month in the prior year

**Application to renewal:**
- The cap applies to each year of the renewed term (not just the first year)
- Each year's increase compounds on the prior year's rent
- The NHSB resolution in effect for the calendar year of the anniversary determines that year's cap

**Vacancy decontrol (RA 9653 Sec. 4):** If the tenant vacates and a NEW tenant takes the unit, the lessor may set rent freely. The unit may re-enter controlled status if the new rent ≤ PHP 10,000.

**Threshold crossing:** If escalation pushes rent above PHP 10,000, the unit exits rent control for the next lease cycle. System must detect this.

**Verification:** CONFIRMED — NHSB 2024-01 text (dhsud.gov.ph), PNA article, RA 9653 Sec. 4.

### Rule 7: Security Deposit Adjustment on Renewal

**Controlled residential (RA 9653 Sec. 7):**
- Maximum deposit: **2 months of the NEW rent** upon renewal
- All accrued bank interest must be **returned to the lessee at lease expiration** (Sec. 7)
- RA 9653 does NOT explicitly address what happens to the deposit at renewal (as opposed to expiration)
- **Common practice (two approaches):**
  1. **Settle and re-collect:** Return old deposit + accrued interest at old lease end; collect new deposit at new rent level → clean accounting
  2. **Top-up:** Retain existing deposit, credit accrued interest to tenant, collect only the difference between old deposit and new cap → simpler for tenant

**Interest treatment on renewal:**
- RA 9653 Sec. 7 says interest is returned "at the expiration of the lease contract"
- A renewal is technically a new contract → old lease "expires" → interest should be settled
- Conservative interpretation: return interest at renewal, reset interest accrual for the new term
- Practical: many lessors retain deposit and simply top up, not returning interest until final lease end. This is legally questionable for controlled units.

**Commercial:** Deposit adjustment is purely contractual. No statutory cap, no interest obligation unless contractually stipulated. Common to adjust deposit to match new rent level (especially for significant increases).

**Verification:** CONFIRMED with qualification — RA 9653 Sec. 7 text (lawphil.net), Salenga Law Firm commentary, lamudi.com.ph, respicio.ph. The gap on renewal-specific deposit treatment is a genuine ambiguity in the statute. No BIR ruling or SC decision directly addresses deposit handling at renewal vs. final expiration. Flagged as **UNVERIFIED** for the top-up practice specifically.

### Rule 8: Holdover Penalty Rates

**Art. 1671:** If tenant stays past expiry **over the lessor's objection**, tenant is treated as a **possessor in bad faith** — liable for:
- Reasonable compensation (in lieu of rent) for the holdover period
- All fruits/income derived or which could have been derived from the property
- Actual damages, moral damages (if bad faith proven), exemplary damages (if wanton refusal)
- Attorney's fees and litigation costs

**Contractual holdover clauses:**
- Lease contracts commonly stipulate holdover rates of **150-200% of last monthly rent**
- These are enforceable but subject to Art. 1229 reduction if "iniquitous or unconscionable"
- Government/PEZA leases: 150-200% is standard and generally upheld

**For controlled units:** Art. 1673(1) suspension means the lessor generally cannot enforce holdover penalties simply because the lease expired. However, if the lessor gives proper notice of non-renewal for a valid RA 9653 ground (e.g., owner-use), holdover after the notice period may trigger Art. 1671 consequences.

**Verification:** CONFIRMED — respicio.ph (holdover penalties commentary), alburolaw.com, Art. 1671/1229 text on chanrobles.com. Holdover rate range (150-200%) confirmed as market practice; enforceability subject to Art. 1229.

### Rule 9: Board Resolution for Renewal

**RA 11232 (Revised Corporation Code):**

| Scenario | Board Resolution Required? | Citation |
|----------|---------------------------|----------|
| New renewal contract | Yes — board authorization via majority vote | RA 11232 Sec. 39 |
| Extension addendum | Recommended — especially if terms change | RA 11232 Sec. 22, 39 |
| Tacit reconduction | No — arises by operation of law, not corporate action | Art. 1670 |
| Renewal in ordinary course of business | Board only (no stockholder vote) | RA 11232 Sec. 39, ordinary course exception |
| Lease of all/substantially all assets | 2/3 stockholder vote required | RA 11232 Sec. 39 |

**Standing resolution:** A board may issue a standing/continuing resolution authorizing officers to execute lease renewals under predefined terms (e.g., "all renewals of existing leases at the same or NHSB-capped rate, for terms ≤ 2 years"). This is valid as long as:
- The resolution has not been amended or rescinded
- The renewal falls within the scope specified
- The Secretary's Certificate certifies the resolution remains in force

**Verification:** CONFIRMED — RA 11232 text (lawphil.net), taxacctgcenter.ph (Title IV commentary), Baker McKenzie Philippines leases guide, pdfcoffee.com (sample Secretary's Certificate for lease renewal).

### Rule 10: Renewal vs. Extension — Legal Distinction

**PH law does NOT have a bright-line statutory distinction** between "renewal" and "extension." However, in practice and jurisprudence:

| Characteristic | Renewal | Extension |
|---------------|---------|-----------|
| Nature | New contract replacing expired one | Prolongation of existing contract |
| Effect on original | Original terminates; new contract begins | Original continues with amended term |
| DST treatment | Full DST on new term's annual rent | DST on extension period only |
| Deposit | Old deposit settled; new deposit at new rate | Deposit continues; top-up if rate changes |
| Escalation | Fresh negotiation; new escalation schedule | Continues original escalation schedule |
| Board resolution | New resolution (or standing resolution) | May rely on original authorization |
| Document | Full new contract | Addendum/amendment |

**DST implication confirmed:** The BIR applies DST "on each" document. A renewal creates a new contract → full DST. An extension addendum → DST on the extension period only. NIRC Sec. 198 applies the same rate to renewals as the original.

**Verification:** CONFIRMED — The distinction is established through practice and BIR treatment, not through explicit statute. respicio.ph, accountaholicsph.com, BIR FOI responses consistent.

---

## 4. Formula / Decision Tree

### Lease Expiry Decision Tree

```
LEASE APPROACHING EXPIRY (60-90 days before end date):
│
├─ Does lessor want to continue with same tenant?
│  │
│  ├─ YES → RENEWAL or EXTENSION
│  │  │
│  │  ├─ Same terms, longer period? → EXTENSION (addendum)
│  │  │   ├─ DST on extension period only
│  │  │   ├─ Deposit: top-up to new rate if escalated
│  │  │   └─ Board resolution: recommended
│  │  │
│  │  └─ Different terms (rent, escalation, etc.)? → RENEWAL (new contract)
│  │      ├─ Full DST on new term
│  │      ├─ IF controlled unit:
│  │      │   ├─ New rent ≤ old_rent × (1 + NHSB_cap)
│  │      │   ├─ Deposit ≤ 2 × new_monthly_rent
│  │      │   └─ Advance ≤ 1 × new_monthly_rent
│  │      ├─ IF commercial:
│  │      │   ├─ Rent freely negotiated
│  │      │   └─ Deposit freely negotiated
│  │      ├─ Settle old deposit (return + interest if controlled)
│  │      ├─ Collect new deposit
│  │      └─ New board resolution (or standing resolution in scope)
│  │
│  └─ NO → NON-RENEWAL
│     │
│     ├─ IF controlled unit:
│     │   ├─ Can only eject for RA 9653 grounds
│     │   ├─ Owner-use: 3-month advance written notice (Sec. 9(c))
│     │   └─ 1-year no-re-lease restriction after repossession
│     │
│     └─ IF commercial:
│         ├─ Send written notice of non-renewal BEFORE expiry
│         ├─ Must be received before 15-day window starts
│         └─ If tenant stays past notice → Art. 1671 (bad faith possessor)
│
├─ NO ACTION TAKEN (missed expiry):
│  │
│  ├─ Tenant continues 15+ days with acquiescence?
│  │   → TACIT RECONDUCTION (Art. 1670)
│  │   ├─ Month-to-month lease created
│  │   ├─ Original terms survive (except period + guaranty)
│  │   ├─ No DST (no new document)
│  │   ├─ Terminable at end of any month with demand to vacate
│  │   └─ IF controlled: Art. 1673(1) still suspended — need RA 9653 grounds
│  │
│  └─ Lessor objects within 15 days?
│      → No implied renewal; tenant must vacate or face Art. 1671
```

### DST Computation on Renewal (TRAIN Law)

```python
def compute_renewal_dst(monthly_rent: Decimal, years: int) -> Decimal:
    """Same formula as new lease DST — TRAIN rates (PHP 6/PHP 2)."""
    annual_rent = monthly_rent * 12
    if annual_rent <= Decimal("2000"):
        annual_dst = Decimal("6.00")
    else:
        excess = annual_rent - Decimal("2000")
        units = math.ceil(excess / Decimal("1000"))
        annual_dst = Decimal("6.00") + units * Decimal("2.00")
    return annual_dst * years
```

### Deposit Adjustment on Renewal (Controlled)

```python
def compute_deposit_adjustment(
    old_monthly_rent: Decimal,
    new_monthly_rent: Decimal,
    existing_deposit: Decimal,
    accrued_interest: Decimal,
    is_controlled: bool,
) -> dict:
    if is_controlled:
        new_max_deposit = new_monthly_rent * 2
        # Conservative: settle old, collect new
        return {
            "refund_old": existing_deposit + accrued_interest,
            "collect_new": new_max_deposit,
            "net_from_tenant": new_max_deposit - existing_deposit - accrued_interest,
            "interest_settled": accrued_interest,
        }
    else:
        # Commercial: contractual — typically adjust to new rent level
        new_deposit = new_monthly_rent * deposit_months  # per contract
        return {
            "top_up_amount": max(Decimal("0"), new_deposit - existing_deposit),
            "interest_settled": Decimal("0"),  # no statutory obligation
        }
```

### Renewal Validation (Controlled Unit)

```python
def validate_renewal(lease, new_terms, is_controlled):
    errors = []
    if is_controlled:
        max_increase = get_nhsb_cap(new_terms.start_year)
        max_new_rent = lease.current_rent * (1 + max_increase)
        if new_terms.monthly_rent > max_new_rent:
            errors.append(
                f"Rent PHP {new_terms.monthly_rent} exceeds NHSB cap "
                f"({max_increase*100}% → max PHP {max_new_rent})"
            )
        if new_terms.deposit > new_terms.monthly_rent * 2:
            errors.append("Deposit exceeds RA 9653 limit (2 months)")
        if new_terms.advance > new_terms.monthly_rent:
            errors.append("Advance exceeds RA 9653 limit (1 month)")
        # Check threshold crossing
        if new_terms.monthly_rent > Decimal("10000"):
            errors.append(
                "WARNING: New rent exceeds PHP 10,000 — unit will exit rent control"
            )
    return errors
```

---

## 5. Edge Cases and Special Rules

1. **Tacit reconduction + controlled unit:** Even after tacit reconduction creates a month-to-month lease, Art. 1673(1) remains suspended. The lessor cannot eject simply because the month ended. They need an RA 9653 ground. This makes tacit reconduction particularly sticky for controlled units.

2. **Guaranty/surety loss on reconduction (Art. 1672):** If the original lease had a guarantor (common for commercial tenants), the guaranty is extinguished upon tacit reconduction. The lessor loses this security without realizing it. System must alert: "WARNING: Guarantor obligation will not survive if lease enters tacit reconduction."

3. **Threshold crossing on renewal:** Controlled unit at PHP 9,900/month with 2.3% NHSB increase → PHP 10,127.70 → exits rent control. The system must detect this at renewal time and switch contract type to COMMERCIAL/RESIDENTIAL_UNCONTROLLED. This unlocks: no deposit cap, no escalation cap, Art. 1673(1) ejectment restored.

4. **Serial tacit reconduction:** A lease that has been on month-to-month for years. Each month is technically a new "lease period." If the lessor eventually wants to formalize, they should execute a new written contract (triggering DST) rather than continue in the ambiguous month-to-month state.

5. **Written holdover agreement:** If the lessor and tenant sign a written month-to-month holdover agreement (rather than relying on tacit reconduction), this IS a document → DST applies. Many property managers unknowingly create DST obligations by formalizing holdover arrangements.

6. **Deposit top-up timing:** RA 9653 doesn't specify WHEN the top-up must be collected at renewal. Best practice: collect before or at lease commencement. Do not allow tenant to occupy under renewed terms without deposit at new level.

7. **NHSB resolution gap:** If no new NHSB resolution is issued for 2027+, the last published cap (1% for 2026) remains in effect until superseded. The system should alert when no NHSB rate is available for the upcoming calendar year.

8. **Renewal of multi-unit lease:** If one lease covers multiple rentables (e.g., Units 101A + 101B), the renewal must address all units. DST computed on aggregate annual rent. If one unit is controlled and another is not, separate renewal treatment may be needed.

9. **Corporate lessee renewal:** If the lessee is also a corporation, request their updated Board Resolution + Secretary's Certificate authorizing the renewed lease. Both parties need corporate authorization.

10. **Retroactive renewal:** If parties negotiate renewal terms after the lease has already expired (but before 15-day reconduction), the new contract should be dated from the actual expiry date to avoid a gap. DST is computed on the signing date.

---

## 6. What Crispina Built

### Exists
- **Lease model:** `pk`, `tenant_pk`, `date_start`, `date_end` — basic lease record
- **RecurringCharge + RecurringChargePeriod:** Pre-computed escalation stored as periods
- **LeaseGenerate schema:** Creates a new lease with escalation — could be used for renewals by creating a fresh Lease record
- **Lease-anniversary splitting:** `split_by_year()` correctly handles anniversary-based periods
- **Compound interest formula:** `base × (1 + rate)^years` with ROUND_DOWN

### NOT Built (Gaps)

| Feature | Status | Impact |
|---------|--------|--------|
| Lease status field | NOT BUILT | Cannot distinguish ACTIVE / EXPIRED / MONTH_TO_MONTH / TERMINATED |
| Lease event log | NOT BUILT (TODO in code) | No audit trail for renewals, extensions, reconduction |
| Renewal/extension linkage | NOT BUILT | No way to link a renewed lease to its predecessor |
| Tacit reconduction detection | NOT BUILT | No expiry monitoring, no 15-day countdown, no alert |
| Holdover tracking | NOT BUILT | No holdover status, no penalty rate, no notice tracking |
| Notice tracking | NOT BUILT | No record of non-renewal notices sent/received |
| Deposit adjustment on renewal | NOT BUILT | No deposit model exists at all |
| DST computation on renewal | NOT BUILT | No DST model exists at all |
| Board resolution linkage | NOT BUILT | No resolution-to-lease mapping |
| Expiry alerting | NOT BUILT | No proactive alerts for upcoming expirations |
| Rent control flag | NOT BUILT | Cannot apply different rules for controlled vs commercial |
| Guarantor tracking | NOT BUILT | No guarantor model → cannot alert about Art. 1672 risk |

### Design Observation
Crispina's Lease model has a docstring: "State table of a lease. Shouldn't be updated directly." This implies the **correct approach for renewal is to create a NEW Lease record** (not modify the existing one), which aligns with PH compliance: a renewal is a new contract triggering new DST. The predecessor-successor linkage is the missing piece.

---

## 7. Lightweight Feature Spec

### Data Model Additions

```
# New models

LeaseEvent (new — audit log for all lease lifecycle events)
├── pk: UUID
├── lease_pk: FK → Lease
├── event_type: ENUM (
│       CREATED, ACTIVATED, RENEWED, EXTENDED,
│       TACIT_RECONDUCTION, NOTICE_SENT, NOTICE_RECEIVED,
│       HOLDOVER_STARTED, TERMINATED, EXPIRED, VOIDED
│   )
├── event_date: Date
├── description: Text
├── related_lease_pk: FK → Lease (nullable)  # for RENEWED: points to new lease
├── related_document_pk: FK → LeaseContract (nullable)
├── created_by: String  # user/system
└── metadata: JSONB  # flexible event-specific data

RenewalRecord (new — links predecessor to successor lease)
├── pk: UUID
├── predecessor_lease_pk: FK → Lease (unique)  # old lease
├── successor_lease_pk: FK → Lease (unique)    # new lease
├── renewal_type: ENUM (RENEWAL, EXTENSION, TACIT_RECONDUCTION)
├── effective_date: Date
├── old_monthly_rent: CurrencyDecimal
├── new_monthly_rent: CurrencyDecimal
├── escalation_applied: PercentageDecimal (nullable)
├── deposit_adjustment: CurrencyDecimal (nullable)  # net change
├── interest_settled: CurrencyDecimal (nullable)
├── dst_record_pk: FK → DSTRecord (nullable)  # null for tacit reconduction
├── board_resolution_pk: FK → BoardResolution (nullable)
└── notes: Text (nullable)

NonRenewalNotice (new — tracks notices to prevent reconduction)
├── pk: UUID
├── lease_pk: FK → Lease
├── notice_type: ENUM (NON_RENEWAL, VACATE, OWNER_USE_REPOSSESSION)
├── sent_date: Date
├── received_date: Date (nullable)
├── notice_method: ENUM (PERSONAL, REGISTERED_MAIL, EMAIL, BARANGAY)
├── ra9653_ground: ENUM (nullable)  # for controlled units
├── response_received: Boolean (default False)
├── response_date: Date (nullable)
├── document_url: String (nullable)
└── re_lease_restriction_until: Date (nullable)  # 1 year for owner-use

HoldoverRecord (new — tracks post-expiry holdover status)
├── pk: UUID
├── lease_pk: FK → Lease
├── expiry_date: Date  # original lease end
├── holdover_start: Date  # expiry_date + 1
├── reconduction_date: Date (nullable)  # expiry + 15 days (if no notice)
├── notice_sent_date: Date (nullable)  # if notice sent within 15 days
├── holdover_rate_multiplier: Decimal (nullable)  # e.g., 2.0 for 200%
├── status: ENUM (WITHIN_15_DAYS, RECONDUCCION_ACTIVE, NOTICE_SERVED, VACATED)
└── resolved_date: Date (nullable)

# Enhancements to existing models

Lease (enhanced)
├── + status: ENUM (DRAFT, ACTIVE, EXPIRED, MONTH_TO_MONTH,
│                   HOLDOVER, TERMINATED, RENEWED, VOIDED)
├── + predecessor_lease_pk: FK → Lease (nullable)  # quick link to prior lease
├── + is_rent_controlled: Boolean
├── + has_guarantor: Boolean (default False)
├── + guarantor_name: String (nullable)
├── + guarantor_contact: String (nullable)
├── + holdover_rate_multiplier: Decimal (nullable)  # contractual holdover rate

Rentable (enhanced, if not already from lease-contract-generation)
├── + unit_type: ENUM (RESIDENTIAL_CONTROLLED, RESIDENTIAL_UNCONTROLLED, COMMERCIAL)
```

### Logic / Workflows

**1. Expiry Alert System (daily job):**
```python
def check_upcoming_expirations():
    today = date.today()
    alerts = []

    # 90-day warning
    expiring_90 = Lease.query.filter(
        Lease.status == 'ACTIVE',
        Lease.date_end == today + timedelta(days=90)
    )
    for lease in expiring_90:
        alerts.append(Alert(
            severity='INFO',
            message=f"Lease for {lease.tenant.full_name} expires in 90 days",
            action='INITIATE_RENEWAL_DISCUSSION'
        ))

    # 30-day warning
    expiring_30 = Lease.query.filter(
        Lease.status == 'ACTIVE',
        Lease.date_end == today + timedelta(days=30)
    )
    for lease in expiring_30:
        if not lease.has_pending_renewal:
            alerts.append(Alert(
                severity='WARNING',
                message=f"Lease expiring in 30 days — no renewal initiated",
                action='URGENT_RENEWAL_OR_NOTICE'
            ))
            if lease.has_guarantor:
                alerts.append(Alert(
                    severity='WARNING',
                    message=f"Guarantor obligation at risk if tacit reconduction occurs (Art. 1672)"
                ))

    # 15-day reconduction countdown
    expired_recently = Lease.query.filter(
        Lease.status == 'EXPIRED',
        Lease.date_end >= today - timedelta(days=15),
        Lease.date_end < today
    )
    for lease in expired_recently:
        days_since_expiry = (today - lease.date_end).days
        if not NonRenewalNotice.exists(lease_pk=lease.pk):
            alerts.append(Alert(
                severity='CRITICAL',
                message=f"Day {days_since_expiry}/15 post-expiry — "
                        f"tacit reconduction in {15 - days_since_expiry} days if no action",
                action='SEND_NON_RENEWAL_NOTICE_OR_EXECUTE_RENEWAL'
            ))

    # Auto-transition to MONTH_TO_MONTH
    reconduccion_candidates = Lease.query.filter(
        Lease.status == 'EXPIRED',
        Lease.date_end <= today - timedelta(days=15)
    )
    for lease in reconduccion_candidates:
        if not NonRenewalNotice.exists(lease_pk=lease.pk):
            lease.status = 'MONTH_TO_MONTH'
            LeaseEvent.create(
                lease_pk=lease.pk,
                event_type='TACIT_RECONDUCTION',
                event_date=lease.date_end + timedelta(days=15),
                description='Implied renewal per Art. 1670 — tenant continued 15+ days, no notice given'
            )

    return alerts
```

**2. Renewal Execution Flow:**
```python
def execute_renewal(old_lease, new_terms, renewal_type):
    # 1. Validate
    errors = validate_renewal(old_lease, new_terms, old_lease.is_rent_controlled)
    if errors:
        return errors

    # 2. Create new lease (immutable record pattern)
    new_lease = Lease.create(
        tenant_pk=old_lease.tenant_pk,
        date_start=new_terms.start_date,
        date_end=new_terms.end_date,
        status='DRAFT',
        is_rent_controlled=determine_rent_control(new_terms.monthly_rent),
        predecessor_lease_pk=old_lease.pk,
    )

    # 3. Generate recurring charges with escalation
    for charge_gen in new_terms.recurring_charge_generators:
        generate_recurring_charge(charge_gen, new_lease.pk)

    # 4. Compute DST (if not tacit reconduction)
    dst_record = None
    if renewal_type != 'TACIT_RECONDUCTION':
        dst_record = compute_renewal_dst(
            new_terms.monthly_rent,
            new_terms.years
        )

    # 5. Handle deposit adjustment
    deposit_adjustment = compute_deposit_adjustment(
        old_monthly_rent=old_lease.current_rent,
        new_monthly_rent=new_terms.monthly_rent,
        existing_deposit=old_lease.security_deposit_amount,
        accrued_interest=old_lease.deposit_accrued_interest,
        is_controlled=old_lease.is_rent_controlled,
    )

    # 6. Create renewal record
    RenewalRecord.create(
        predecessor_lease_pk=old_lease.pk,
        successor_lease_pk=new_lease.pk,
        renewal_type=renewal_type,
        effective_date=new_terms.start_date,
        old_monthly_rent=old_lease.current_rent,
        new_monthly_rent=new_terms.monthly_rent,
        deposit_adjustment=deposit_adjustment['net_from_tenant'],
        interest_settled=deposit_adjustment.get('interest_settled', 0),
        dst_record_pk=dst_record.pk if dst_record else None,
    )

    # 7. Update old lease status
    old_lease.status = 'RENEWED'
    LeaseEvent.create(
        lease_pk=old_lease.pk,
        event_type='RENEWED',
        related_lease_pk=new_lease.pk,
    )

    return new_lease
```

### Inputs and Outputs

**Inputs:**
- Existing lease record (predecessor)
- Renewal type selection (renewal / extension / system-detected tacit reconduction)
- New terms: start date, end date, monthly rent, escalation parameters
- Deposit amount (or top-up instruction)
- Board resolution reference (or standing resolution validation)

**Outputs:**
- New Lease record (successor, linked to predecessor)
- RenewalRecord (audit trail of the transition)
- DSTRecord with amount and filing deadline (if applicable)
- Deposit adjustment computation (refund/collect/top-up)
- LeaseContract document (if renewal or extension — same template system as new leases)
- Updated predecessor lease status (RENEWED / TERMINATED)
- Alerts for compliance milestones (DST filing, notarization, deposit collection)

---

## 8. Automability Score: 4/5

**Justification:**

| Component | Automability | Notes |
|-----------|-------------|-------|
| Expiry alerting (60/30/15-day) | 5/5 | Purely date-based, deterministic |
| Tacit reconduction detection | 5/5 | Date math + notice tracking |
| DST computation on renewal | 5/5 | Purely formulaic |
| NHSB cap validation (controlled) | 5/5 | Lookup table + arithmetic |
| Deposit adjustment computation | 5/5 | Formula + regime rules |
| Renewal record creation + linkage | 5/5 | Deterministic data operations |
| Contract generation for renewal | 4/5 | Same as new lease (template + substitution) |
| Holdover management | 3/5 | Detection automatic; response requires human judgment |
| Non-renewal decision | 2/5 | Business decision requiring human judgment |
| Term negotiation (commercial) | 1/5 | Fully human — rent, term, conditions |
| Board resolution approval | 1/5 | Corporate governance process |
| Notice drafting for RA 9653 grounds | 2/5 | Template-assisted but grounds selection is human |

**Overall: 4/5** — The mechanics of renewal processing (computation, tracking, alerting, document generation) are highly automatable. The decision to renew or not, terms negotiation, and corporate governance steps require human judgment.

---

## 9. Verification Status

| # | Rule | Status | Sources |
|---|------|--------|---------|
| 1 | Three continuity scenarios (renewal/extension/reconduction) | **CONFIRMED** | NIRC Sec. 194, Art. 1670, Art. 1306; respicio.ph, BIR FOI |
| 2 | Tacit reconduction elements (Art. 1670) | **CONFIRMED** | *Samelo v. Manotok* (G.R. 170509), *Buce v. Galeon* (G.R. 222785), lawphil.net |
| 3 | Art. 1672 — guaranty extinguished on reconduction | **CONFIRMED** | Art. 1672 text (lawphil.net, chanrobles.com) |
| 4 | Notice requirements to prevent reconduction | **CONFIRMED** | *Buce v. Galeon* (G.R. 222785, 2020), alburolaw.com, legalresource.ph |
| 5 | Art. 1673(1) suspension for controlled units | **CONFIRMED** | RA 9653 Sec. 12, lawphil.net, thecorpusjuris.com |
| 6 | DST on renewals (TRAIN rates: PHP 6/PHP 2) | **CONFIRMED** | RR 4-2018 (SC E-Library), NIRC Sec. 194/198, respicio.ph |
| 7 | No DST on tacit reconduction | **CONFIRMED (reasoning)** | NIRC Sec. 194 taxes documents; no document = no DST. No contrary BIR ruling found. |
| 8 | NHSB cap on renewal | **CONFIRMED** | NHSB 2024-01 (dhsud.gov.ph), PNA, RA 9653 Sec. 4 |
| 9 | Deposit adjustment on renewal (controlled) | **CONFIRMED with gap** | RA 9653 Sec. 7 (lawphil.net), respicio.ph, lamudi.com.ph. Gap: no explicit statutory guidance on deposit treatment at renewal vs. final expiration. |
| 10 | Holdover penalties (Art. 1671) | **CONFIRMED** | Art. 1671 text, respicio.ph holdover commentary, alburolaw.com |
| 11 | Contractual holdover rates (150-200%) | **CONFIRMED** | respicio.ph, government lease practice, Art. 1229 reduction principle |
| 12 | Board resolution for renewal | **CONFIRMED** | RA 11232 Secs. 22, 35, 39; Baker McKenzie PH; taxacctgcenter.ph |
| 13 | Standing resolution validity | **CONFIRMED** | RA 11232 Sec. 39 ordinary course exception; sample Secretary's Certificates |
| 14 | Renewal vs. extension distinction | **CONFIRMED (practice-based)** | No bright-line statute; established through BIR DST treatment and market practice |

**14/14 rules verified. 1 gap documented (deposit at renewal). No unresolved source conflicts.**

---

## 10. Source Conflicts Documented

1. **Deposit handling at renewal:** RA 9653 Sec. 7 says interest is returned "at the expiration of the lease contract." Whether a renewal constitutes "expiration" (triggering interest settlement) or merely "continuation" is ambiguous. Conservative approach: treat renewal as expiration of old lease → settle interest → collect new deposit. This is the safer interpretation for a system design.

2. **DST rate discrepancy in input files:** `input/lease-contract-requirements.md` contains pre-TRAIN rates (PHP 3/PHP 1). The correct TRAIN-amended rates are PHP 6/PHP 2 per RR 4-2018. This was already flagged in the `lease-contract-generation.md` analysis.

3. **Rent Control Act rate brackets:** Some secondary sources cite the old tiered bracket system (2%/7%/11%) which was replaced by uniform percentages from 2024 onward. System should use only the NHSB resolution rates, not historical brackets.
