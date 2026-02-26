# Lease Contract Generation — Process Analysis & Feature Spec

## Process Description

**What:** Generate a new lease contract document for a tenant, incorporating all mandatory PH clauses, corporate authorization references, deposit/advance terms, escalation schedule, and utility arrangements. Produce a signed-ready PDF (or print-ready document) with all variable fields substituted from the system's lease data.

**When:** At the start of every new tenancy. Also triggered for lease renewals (covered separately in `lease-renewal-extension.md`). The document must be executed before the tenant occupies the unit, and DST must be filed within 5 days after the close of the month in which the contract is signed.

**Who does it:** Property manager drafts the contract from a template, fills in tenant/unit details, gets board resolution (if not covered by a standing resolution), arranges notarization, computes and files DST.

**Frequency:** ~5-20 new leases per year for a 20-100 unit portfolio (turnover-dependent). Each lease is a one-time event per tenancy but involves multiple sequential steps.

---

## Current Method

**Fully manual / Word template.** The business currently:
1. Maintains a Word document template for lease contracts
2. Manually fills in tenant name, unit, term dates, rent amount, deposit, etc.
3. Prints 3+ copies for signing
4. Arranges notarization appointment
5. Manually computes DST and files BIR Form 2000
6. No systematic tracking of which leases have been notarized, registered with RD, or had DST filed

**Pain points:** Inconsistent clause inclusion, risk of RA 9653 violations in residential contracts (oversize deposits, illegal escalation rates), missed DST filings, no board resolution linkage, no tracking of contract execution milestones.

---

## Regulatory Rules with Legal Citations

### 1. Writing Requirement
**Civil Code Art. 1403(2)(e):** Leases of real property for longer than one year must be in writing (Statute of Frauds). Without a written contract, the lease is unenforceable in court. Best practice: put ALL leases in writing regardless of term.

**Verification:** CONFIRMED — lawphil.net (RA 386 full text), Respicio.ph commentary, SC jurisprudence (Paredes v. Espino, G.R. No. L-23351). Effect is "unenforceable" (not void).

### 2. Notarization
Not required for validity between parties, but needed for:
- **Registry of Deeds registration** (to bind third parties)
- **Court admissibility** as public document (without additional proof of authenticity)
- **Practical enforceability** (banks, government agencies expect notarized leases)

2004 Rules on Notarial Practice (A.M. No. 02-8-13-SC): All signatories must appear in person, present valid government-issued IDs, sign in notary's presence. At least 3 original copies (lessor, lessee, notary). DST stamps must be affixed and cancelled before notary signs.

**Verification:** CONFIRMED with nuance — DST is payable on the document regardless of notarization status (notarization is not a prerequisite for DST filing). The "3 originals" is established practice from notarial record-keeping obligations.

### 3. Corporate Lessor Authorization
**RA 11232 (Revised Corporation Code), Section 39:** Board of Directors must authorize lease execution via Board Resolution.

Resolution must specify: property, lessee, term, rental rate, authorized signatory. Secretary's Certificate (notarized) must certify the resolution is in force and accompany the lease.

**Officers with implied authority** (President/CEO/GM) may sign without specific resolution per jurisprudence, but explicit board authorization is best practice for real property leases.

**Critical nuance:** If the lease covers "all or substantially all" corporate assets, 2/3 stockholder approval is also required (RA 11232 Sec. 39).

**Verification:** CONFIRMED — RA 11232 text, SC jurisprudence on implied corporate authority. Nuance about 2/3 stockholder vote for substantially all assets verified.

### 4. DST on Lease Contracts
**NIRC Section 194 (as amended by TRAIN Law, RA 10963, effective January 1, 2018):**

| Portion of Annual Rent | DST |
|---|---|
| First PHP 2,000 (or fractional part) | **PHP 6.00** |
| Every PHP 1,000 (or fractional part) in excess of PHP 2,000 | **PHP 2.00** additional |

Applied **per year** of the lease term.

**Formula:**
```
Annual DST = PHP 6.00 + CEILING((Annual Rent − PHP 2,000) / PHP 1,000) × PHP 2.00
Total DST = Annual DST × Number of Years of Lease Term
```

**Example — Monthly rent PHP 15,000 (Annual = PHP 180,000), 2-year lease:**
- Annual DST = PHP 6.00 + CEILING((180,000 − 2,000) / 1,000) × PHP 2.00
- = PHP 6.00 + 178 × PHP 2.00 = **PHP 362.00**
- Total DST = PHP 362.00 × 2 = **PHP 724.00**

**Who pays:** Primarily the lessor (NIRC Sec. 173). Contract may stipulate lessee bears DST (common in commercial).

**Filing:** BIR Form 2000, within 5 days after close of month when contract was executed.

**Verification:** CONFIRMED — rates corrected from pre-TRAIN (PHP 3/PHP 1) to TRAIN-amended (PHP 6/PHP 2). Filing deadline and per-year computation confirmed. Note: `input/lease-contract-requirements.md` contains the pre-TRAIN rates and needs correction.

### 5. Mandatory and Essential Contract Clauses

| Clause | Legal Basis | Notes |
|---|---|---|
| Party identification | Civil Code Art. 1643 | Full legal names, TIN, addresses; corporate: SEC reg no., authorized signatory |
| Property description | Civil Code Art. 1643 | Address, floor area, unit number, TCT/CCT number |
| Term / duration | Civil Code Art. 1643 | Fixed start and end dates |
| Rental rate | Civil Code Art. 1643 | Monthly amount in PHP, due date, payment mode |
| Security deposit | RA 9653 Sec. 7 (residential) | Controlled: max 2 months; commercial: as negotiated |
| Advance rent | RA 9653 Sec. 7 (residential) | Controlled: max 1 month |
| Permitted use | Civil Code | Residential, commercial, or mixed |
| **Subletting restriction** | **Express clause required** | **Civil Code Art. 1650 default: subletting IS PERMITTED** unless expressly prohibited. RA 9653 Sec. 8 overlays additional restriction for controlled units (written consent required). Corporate lessor should always include express prohibition clause. |
| Rent escalation schedule | Contractual; NHSB cap for controlled | Amount/%, trigger date, notice period |
| Repair/maintenance allocation | Civil Code Art. 1654 | Structural = lessor; minor = lessee |
| Utilities arrangement | Contractual | Sub-metering rights, allocation method |
| Termination grounds | Civil Code Art. 1673 + RA 9653 Sec. 9 | Different grounds for controlled vs commercial |
| Force majeure | Civil Code Art. 1659 | Suspension of rent if uninhabitable |
| Governing law and venue | Contractual | Philippine law; Las Piñas RTC/MTC |
| Board resolution reference | RA 11232 | Resolution number, date, authorized signatory |

**Verification:** CONFIRMED — Art. 1650 subletting default corrected (default is PERMITTED, not prohibited). Express prohibition clause is mandatory for the lessor's protection.

### 6. Registration with Registry of Deeds
**Civil Code Art. 1648 (primary) / Art. 709 (general principle):** Leases exceeding one year should be registered with the RD to bind third parties (e.g., subsequent purchasers). Unregistered lease binds only lessor and lessee.

**Fee:** ~PHP 1,000 + IT fee for annotation on the owner's title.

**Verification:** CONFIRMED — Art. 1648 is the correct primary citation for lease registration (Art. 709 is the general registry principle).

### 7. Rent-Controlled Unit Protections
The contract template for controlled residential units must enforce RA 9653 constraints:
- Deposit ≤ 2 months' rent; advance ≤ 1 month
- Escalation ≤ NHSB cap (2.3% for 2025, 1% for 2026)
- No eviction for lease expiry alone (Art. 1673(1) suspended per RA 9653 Sec. 12)
- Subletting requires written lessor consent (RA 9653 Sec. 8)

### 8. DST Exemptions
**No exemption** for residential vs. commercial or low-rent leases. DST applies to ALL written lease agreements. NIRC Section 199 exemptions cover primarily financial market instruments. Diplomatic exemptions arise from Vienna Convention; agrarian from RA 6657/RA 11953 — neither from Sec. 199.

**Verification:** CONFIRMED with characterization correction on Section 199 scope.

---

## Formula / Decision Tree

### Contract Type Selection

```
IF unit.is_rent_controlled AND monthly_rent <= PHP 10,000:
    template = RESIDENTIAL_CONTROLLED
    max_deposit = 2 × monthly_rent
    max_advance = 1 × monthly_rent
    escalation_cap = NHSB_rate_for_year  # 2.3% 2025, 1% 2026
    subletting_clause = "requires written consent" (RA 9653 Sec. 8)
    ejectment_grounds = RA_9653_GROUNDS  # stricter
ELSE:
    template = COMMERCIAL (or RESIDENTIAL_UNCONTROLLED)
    max_deposit = None  # no cap
    max_advance = None  # no cap
    escalation_cap = None  # contractual
    subletting_clause = "prohibited" (express clause; Art. 1650 default is PERMITTED)
    ejectment_grounds = CIVIL_CODE_GROUNDS  # Art. 1673
```

### DST Computation (TRAIN Law rates)

```python
def compute_lease_dst(monthly_rent: Decimal, years: int) -> Decimal:
    annual_rent = monthly_rent * 12
    if annual_rent <= 2000:
        annual_dst = Decimal("6.00")
    else:
        excess = annual_rent - Decimal("2000")
        units = math.ceil(excess / Decimal("1000"))
        annual_dst = Decimal("6.00") + units * Decimal("2.00")
    return annual_dst * years
```

### Contract Generation Workflow

```
1. SELECT template based on unit type (controlled / commercial)
2. VALIDATE inputs:
   - Deposit amount ≤ cap (if controlled)
   - Advance amount ≤ cap (if controlled)
   - Escalation rate ≤ NHSB cap (if controlled)
   - Board resolution exists and is in force
3. SUBSTITUTE variables into template:
   - Lessor: corporate name, SEC reg no., TIN, address, authorized signatory
   - Lessee: name, TIN (if corporate), address
   - Property: address, unit, floor area, TCT/CCT
   - Term: start date, end date, years
   - Rent: monthly amount, due date (5th for controlled per RA 9653 Sec. 7)
   - Escalation: rate, trigger date, formula
   - Deposit: amount, bank holding obligation (if controlled)
   - Advance: amount
   - Utilities: arrangement description
4. COMPUTE DST → store amount + filing deadline
5. GENERATE PDF (or print-ready document)
6. TRACK execution milestones:
   - [ ] Contract drafted
   - [ ] Board resolution in force (if needed)
   - [ ] Signed by both parties
   - [ ] Notarized
   - [ ] DST stamps affixed and cancelled
   - [ ] DST filed (BIR Form 2000) by deadline
   - [ ] Registered with RD (if term > 1 year)
   - [ ] Deposit collected and banked (if controlled)
   - [ ] Advance rent collected
```

---

## Edge Cases and Special Rules

1. **Controlled unit with rent near PHP 10,000 threshold:** If escalation would push monthly rent above PHP 10,000, the unit exits rent control for the next lease year. System must detect threshold crossing and switch contract type/constraints.

2. **Corporate lessee:** Request their Board Resolution + Secretary's Certificate authorizing the lease. Both parties need corporate authorization if both are corporations.

3. **Multi-unit lease:** One lease covering multiple rentables (e.g., tenant leases Unit 101A + 101B). Contract must list all units; DST computed on aggregate annual rent.

4. **Lease term fractional years:** DST computation uses number of years. A 1.5-year lease = 2 years for DST (fractional part rounds up per NIRC "or fractional part thereof" language).

5. **Escalated rent across lease years:** DST is computed per year using that year's rent. If monthly rent is PHP 10,000 Year 1 and PHP 12,000 Year 2:
   - Year 1 DST on PHP 120,000 annual rent
   - Year 2 DST on PHP 144,000 annual rent
   - Total DST = sum of both years

6. **Advance rent in DST base:** Advance rent is included in the DST computation base. Security deposits are NOT included (refundable, not consideration for use).

7. **Standing board resolution:** The board may pass a standing resolution authorizing the President to execute leases up to a certain value/duration without per-lease approval. System should track: resolution scope, authorized officer, still-in-force status.

8. **Vacancy decontrol:** New tenant in a previously controlled unit → lessor sets rent freely (RA 9653 Sec. 4). The unit may re-enter controlled status if new rent ≤ PHP 10,000.

9. **Tacit reconduction risk:** System must generate alerts when lease is within 30-60 days of expiry. If tenant continues past 15 days post-expiry without signed renewal → implied month-to-month lease created (Art. 1670). This is NOT a contract generation event per se, but the system should flag it.

10. **Zero-term or same-day lease:** Crispina's `split_by_year` requires `date_start < date_end` (strict inequality). Minimum term = 1 day. Practical minimum for rental contracts = 1 month.

---

## What Crispina Built

### Exists
- **Lease model:** `pk`, `tenant_pk`, `date_start`, `date_end` — basic lease record
- **LeaseGenerate schema:** `tenant_pk`, `rentable_pks` (list), `recurring_charge_generators` (list) — API input for creating a lease with pre-computed escalation
- **LeaseRentable M2M:** Supports one lease covering multiple rentables
- **RecurringCharge + RecurringChargePeriod:** Pre-computed escalation stored as date-bounded rate periods (excellent audit trail)
- **RecurringChargeGenerate:** Accepts `yearly_increase_percent` for automated escalation at creation
- **Compound interest formula:** `base × (1 + rate)^years` with ROUND_DOWN (tenant-favorable)
- **Lease-anniversary splitting:** `split_by_year()` correctly uses lease anniversary dates, not calendar years

### NOT Built (Gaps)
| Feature | Status | Impact |
|---|---|---|
| Contract document template system | NOT BUILT | No template engine, no variable substitution, no PDF generation |
| Board resolution tracking | NOT BUILT | No model for resolutions, authorized signatories, or in-force status |
| DST computation | NOT BUILT | No DST formula, no Form 2000 tracking, no filing deadline alerts |
| Lease status field | NOT BUILT | Cannot distinguish active/expired/terminated/month-to-month |
| Rent control flag | NOT BUILT | No way to enforce RA 9653 constraints per unit/lease |
| Notarization tracking | NOT BUILT | No milestone tracking for contract execution steps |
| RD registration tracking | NOT BUILT | No tracking of which leases >1 year are registered |
| Contract execution milestones | NOT BUILT | No workflow state machine for drafting → signing → notarizing → filing |
| Tenant TIN | NOT BUILT | Needed for contract header (corporate lessee identification) |
| Corporate flag on tenant | NOT BUILT | Needed to determine if lessee board resolution is required |
| Unit floor area | NOT BUILT | Needed in contract property description |
| Lease event log | NOT BUILT (TODO in code) | No audit trail for contract-level events |

### Dependencies (No Crispina code, not in any library)
- PDF generation library (e.g., WeasyPrint, ReportLab, or Jinja2 → HTML → PDF)
- Template engine for variable substitution (Jinja2)
- Digital signature integration (optional, not yet mandated for mid-size lessors)

---

## Lightweight Feature Spec

### Data Model Additions

```
LeaseContract (new)
├── pk: UUID
├── lease_pk: FK → Lease
├── contract_type: ENUM (RESIDENTIAL_CONTROLLED, RESIDENTIAL_UNCONTROLLED, COMMERCIAL)
├── template_version: String  # which template revision was used
├── generated_at: DateTime
├── signed_at: DateTime (nullable)
├── notarized_at: DateTime (nullable)
├── notary_name: String (nullable)
├── notary_doc_no: String (nullable)  # Notarial register reference
├── rd_registered_at: DateTime (nullable)  # Registry of Deeds
├── rd_entry_number: String (nullable)
├── document_url: String (nullable)  # path to generated PDF
└── status: ENUM (DRAFT, SIGNED, NOTARIZED, REGISTERED, VOID)

BoardResolution (new)
├── pk: UUID
├── resolution_number: String
├── resolution_date: Date
├── scope_description: Text  # "All leases up to PHP 50K/month for TSVJ Center"
├── authorized_officer: String  # "John Doe, President"
├── authorized_position: String
├── max_monthly_rent: CurrencyDecimal (nullable)  # scope limit
├── max_lease_years: Integer (nullable)  # scope limit
├── is_standing: Boolean  # true = covers multiple leases
├── secretary_certificate_date: Date (nullable)
├── is_in_force: Boolean (default True)
└── superseded_by_pk: FK → BoardResolution (nullable)

DSTRecord (new)
├── pk: UUID
├── lease_contract_pk: FK → LeaseContract
├── annual_rent_year_1: CurrencyDecimal
├── annual_dst_per_year: JSONB  # [{year: 1, annual_rent: X, dst: Y}, ...]
├── total_dst: CurrencyDecimal
├── lease_years: Integer
├── filing_deadline: Date  # 5 days after month-end of execution
├── filed_at: Date (nullable)
├── form_2000_reference: String (nullable)
├── paid_by: ENUM (LESSOR, LESSEE, SPLIT)
└── payment_reference: String (nullable)

# Enhancements to existing models:

Lease (enhanced)
├── + status: ENUM (DRAFT, ACTIVE, EXPIRED, TERMINATED, MONTH_TO_MONTH)
├── + is_rent_controlled: Boolean
├── + board_resolution_pk: FK → BoardResolution (nullable)

Tenant (enhanced)
├── + tin: String (nullable)  # BIR Tax Identification Number
├── + is_corporate: Boolean (default False)
├── + sec_registration_no: String (nullable)

Rentable (enhanced)
├── + floor_area_sqm: Decimal (nullable)
├── + tct_cct_number: String (nullable)  # Transfer/Condominium Certificate of Title
├── + unit_type: ENUM (RESIDENTIAL_CONTROLLED, RESIDENTIAL_UNCONTROLLED, COMMERCIAL)

ContractTemplate (new)
├── pk: UUID
├── name: String  # "Residential Controlled Lease v2.1"
├── contract_type: ENUM (RESIDENTIAL_CONTROLLED, RESIDENTIAL_UNCONTROLLED, COMMERCIAL)
├── template_body: Text  # Jinja2 template with {{ variables }}
├── version: String
├── is_active: Boolean
├── created_at: DateTime
└── approved_by: String (nullable)
```

### Logic / Formulas

**DST Computation (TRAIN Law, RA 10963):**
```python
def compute_dst(lease) -> DSTRecord:
    records = []
    for year_idx, period in enumerate(lease.recurring_charge_periods):
        annual_rent = period.amount * 12
        if annual_rent <= Decimal("2000"):
            annual_dst = Decimal("6.00")
        else:
            excess = annual_rent - Decimal("2000")
            units = math.ceil(excess / Decimal("1000"))
            annual_dst = Decimal("6.00") + units * Decimal("2.00")
        records.append({"year": year_idx + 1, "annual_rent": annual_rent, "dst": annual_dst})
    total_dst = sum(r["dst"] for r in records)
    filing_deadline = last_day_of_month(lease.signed_at) + timedelta(days=5)
    return DSTRecord(annual_dst_per_year=records, total_dst=total_dst, ...)
```

**Validation Rules (at contract generation):**
```python
def validate_lease_contract(lease, contract_type):
    errors = []
    if contract_type == RESIDENTIAL_CONTROLLED:
        if deposit_amount > 2 * monthly_rent:
            errors.append("Deposit exceeds RA 9653 limit (2 months)")
        if advance_amount > 1 * monthly_rent:
            errors.append("Advance exceeds RA 9653 limit (1 month)")
        if escalation_rate > nhsb_cap_for_year(start_year):
            errors.append(f"Escalation {escalation_rate}% exceeds NHSB cap {nhsb_cap}%")
    if lease.term_years > 1 and not lease.board_resolution:
        errors.append("Board resolution required for lease >1 year")
    if not tenant.tin and tenant.is_corporate:
        errors.append("Corporate tenant TIN required")
    return errors
```

**Board Resolution Scope Check:**
```python
def check_board_resolution_covers(resolution, lease):
    if not resolution.is_in_force:
        return False
    if resolution.max_monthly_rent and lease.monthly_rent > resolution.max_monthly_rent:
        return False
    if resolution.max_lease_years and lease.term_years > resolution.max_lease_years:
        return False
    return True
```

### Template System

Template engine: Jinja2 with the following variable context:
```python
template_context = {
    # Lessor (corporation)
    "lessor_name": "TSVJ Corporation",
    "lessor_sec_no": "CS202X-XXXXX",
    "lessor_tin": "XXX-XXX-XXX-000",
    "lessor_address": "Crispina Ave, Pamplona 3, Las Piñas City",
    "authorized_signatory": "Juan Dela Cruz",
    "authorized_position": "President",
    "board_resolution_no": "BR-2025-003",
    "board_resolution_date": "2025-01-15",

    # Lessee
    "lessee_name": tenant.full_name or tenant.billing_name,
    "lessee_tin": tenant.tin,  # if corporate
    "lessee_address": "...",

    # Property
    "property_name": "TSVJ Center",
    "property_address": "Crispina Ave, Pamplona 3, Las Piñas City",
    "unit_designation": "Unit 101",
    "floor_area_sqm": "25.00",
    "tct_cct_no": "TCT No. T-XXXXX",

    # Terms
    "lease_start": "2025-03-01",
    "lease_end": "2027-02-28",
    "lease_years": 2,
    "monthly_rent": "15,000.00",
    "due_day": 5,  # 5th of month for controlled; contractual for commercial
    "escalation_rate": "2.3%",
    "escalation_type": "NHSB cap",  # or "fixed", "stepped", "CPI-linked"

    # Financial
    "security_deposit": "30,000.00",  # 2 months
    "advance_rent": "15,000.00",     # 1 month
    "vat_rate": "12%",  # or "EXEMPT" for controlled ≤ PHP 15K
    "dst_amount": "724.00",

    # Clauses (conditional)
    "is_rent_controlled": True,
    "subletting_clause": "PROHIBITED without prior written consent of the LESSOR",
    "ejectment_grounds": [...],
}
```

### Inputs and Outputs

**Inputs:**
- Tenant record (from system)
- Rentable/unit record (from system)
- Lease terms: start date, end date, monthly rent, escalation parameters
- Deposit and advance amounts
- Board resolution reference
- Contract type selection (or auto-detected from unit type + rent amount)

**Outputs:**
- `LeaseContract` record with status tracking
- `DSTRecord` with computed amount and filing deadline
- Generated PDF document (contract text with all variables substituted)
- Execution milestone checklist (draft → signed → notarized → DST filed → RD registered)
- Validation warnings (RA 9653 violations, missing board resolution, etc.)

---

## Automability Score: 4/5

**Justification:**
- Template selection and variable substitution: **fully deterministic** (5/5)
- DST computation: **purely formulaic** (5/5)
- RA 9653 constraint validation: **deterministic rules** (5/5)
- Board resolution scope check: **deterministic** (5/5)
- Contract clause selection (controlled vs commercial): **deterministic** (5/5)

**What requires human judgment (prevents 5/5):**
- Custom clause negotiation for commercial leases (non-standard terms)
- Board resolution drafting and approval (corporate governance)
- Notarization scheduling and in-person signing
- Decision on whether to register with RD (cost-benefit for short leases)
- Vacancy decontrol pricing (setting new rent for a vacant unit)
- Exception handling for unusual lease structures (e.g., rent-free fit-out periods)

---

## Verification Status

| Rule | Status | Sources |
|---|---|---|
| Writing requirement (Art. 1403) | CONFIRMED | lawphil.net, Respicio.ph, SC: Paredes v. Espino |
| Notarization requirements | CONFIRMED (nuance: DST ≠ notarization prerequisite) | 2004 Rules on Notarial Practice, lawphil.net |
| Board Resolution (RA 11232) | CONFIRMED (nuance: 2/3 vote if "substantially all" assets) | RA 11232 Sec. 39, SC jurisprudence |
| DST rates (TRAIN Law) | **CORRECTED** — PHP 6/PHP 2 (not PHP 3/PHP 1) | NIRC Sec. 194 as amended by RA 10963 |
| Mandatory clauses (Art. 1643) | CONFIRMED | Civil Code Art. 1643, RA 9653 Sec. 7 |
| Subletting default (Art. 1650) | **CORRECTED** — default is PERMITTED; express prohibition needed | Civil Code Art. 1650, RA 9653 Sec. 8 |
| RD registration (Art. 1648) | CONFIRMED (citation corrected: Art. 1648, not Art. 709) | Civil Code Art. 1648/709 |
| DST exemptions (Sec. 199) | CONFIRMED (characterization corrected) | NIRC Sec. 199 |

**8/8 rules verified. 3 corrections applied (DST rates, subletting default, article citation). No unresolved conflicts.**

---

## Upstream Corrections Needed

The following corrections should be applied to `input/lease-contract-requirements.md`:

1. **Section 6 (DST on Lease Contracts):** DST rate table shows pre-TRAIN rates (PHP 3/PHP 1). Should be **PHP 6/PHP 2** per TRAIN Law (RA 10963, effective Jan 1, 2018). Example computation should double accordingly.

2. **Section 4 (Mandatory Clauses):** Art. 1650 subletting note states "Default: not allowed without lessor consent." Should state: **"Default: PERMITTED unless expressly prohibited (Art. 1650). RA 9653 Sec. 8 overlays written consent requirement for controlled units."**

3. **Section 3 (Registry of Deeds):** Primary citation should be **Art. 1648** (specific to lease registration), not Art. 709 alone.
