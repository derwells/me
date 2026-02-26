# Security Deposit Lifecycle — Process Analysis & Feature Spec

*Analyzed: 2026-02-26 | Wave 2 | Depends on: security-deposit-rules, crispina-models, crispina-services, corporate-rental-tax, lease-contract-requirements*

---

## 1. Process Description

**What:** Track security deposits through their full lifecycle — collection at lease start, holding during lease, deductions at lease end, and refund/forfeiture with interest and tax reclassification.

**When:**
- **Collection:** At lease execution (one-time per lease)
- **Holding:** Continuous during lease term (interest accrual for controlled residential)
- **Deduction assessment:** At lease end, after premises inspection
- **Refund/forfeiture:** Within 1 month of turnover (controlled) or ~30 days (commercial)
- **Tax reclassification:** At the moment of application or forfeiture (ad hoc)

**Who does it:**
- **Property manager:** Collects deposit, records in ledger, orders inspection, computes deductions, initiates refund
- **Bank:** Holds deposit during lease (required for controlled residential)
- **Accountant:** Journals the liability at receipt, reclassifies to income on application/forfeiture, reports on VAT/ITR

---

## 2. Current Method

**Fully manual / spreadsheet.** No Crispina support exists.

Typical current workflow:
1. Collect deposit at lease signing → record in Excel with tenant name, amount, date
2. Deposit into bank account (sometimes co-mingled with operating funds)
3. At lease end → inspect premises → handwritten deduction list
4. Compute refund (deposit minus deductions) → sometimes forget to add interest
5. Issue check or bank transfer → no formal accounting reclassification
6. Accountant finds out about forfeiture at year-end when reconciling

**Pain points:** No per-tenant ledger, interest not tracked, tax reclassification missed, deduction documentation informal, return deadline not monitored, no distinction between controlled and commercial rules.

---

## 3. Regulatory Rules with Legal Citations

### 3a. Two-Regime System

| Rule | Residential Controlled | Commercial |
|------|----------------------|------------|
| **Governing law** | RA 9653 Sec. 7 | Civil Code Arts. 1306, 1456, 1642-1688 |
| **Coverage** | Units in NCR + highly urbanized cities with rent ≤ PHP 10,000/mo | All other leases |
| **Max deposit** | 2 months' rent | No cap (Art. 1306 freedom to contract) |
| **Max advance rent** | 1 month | No cap |
| **Bank-holding** | Mandatory — deposit must be in bank under lessor's name during entire lease (Sec. 7) | Not mandated; trust money doctrine (Art. 1456) discourages co-mingling |
| **Interest** | ALL bank interest must be returned to lessee at lease end (Sec. 7) | Contractual only; no statutory obligation |
| **Return deadline** | 1 month from BOTH lease expiry AND actual turnover (Sec. 7) | Reasonable time; 30-day benchmark (Civil Code Art. 1170, jurisprudence) |
| **Delay penalty** | 6% p.a. legal interest from demand (Nacar v. Gallery Frames, G.R. 189871, 2013; BSP Circular 799-2013) | Same — 6% p.a. from demand |
| **Penalty for violation** | PHP 25,000–50,000 fine (RA 9653 Sec. 12); imprisonment for repeat offense; DHSUD blacklisting | Civil liability + potential estafa (RPC Art. 315) |

### 3b. Permissible Deductions

**Legal basis:** Civil Code Arts. 1657(1), 1658 (lessee repair obligations); RA 9653 Sec. 7 ("commensurate to the pecuniary damage")

**Allowed:**
- Unpaid rent
- Unpaid utility bills
- Unpaid association dues (if contractual)
- Damage beyond normal wear and tear (*deterioro extraordinario*)
- Contractually-agreed repairs chargeable to tenant

**Not allowed:**
- Routine repainting
- Minor nail holes
- Normal appliance wear
- Any damage from ordinary use

**Documentation requirement:** Itemized statement with official receipts or repair quotations required. Burden of proof rests on the landlord. Generic claims are disallowed (Civil Code Arts. 1170, 1173, Art. 19 — abuse of right).

**Forfeiture limits:** "Automatic forfeiture" clauses for any breach are void (Art. 1306/1409). RA 9653 Sec. 7 requires only partial forfeiture "commensurate to the pecuniary damage" — total forfeiture requires total damage proof.

### 3c. Tax Treatment

**At receipt — NOT taxable (liability):**
- BIR Ruling DA-334-2004: Refundable deposits are not income at receipt
- RMC 11-2024 (Jan 22, 2024): Confirms deposit = liability for lessor, asset for lessee
- Advance rent is different: taxable at receipt regardless of when period covered begins (substance over form — BIR looks at refundability)

**At application/forfeiture — BECOMES taxable income:**
- BIR Ruling 118-12: Taxable upon application/forfeiture
- BIR Ruling DA-489-03, 033-00: Forfeited deposits = gross receipts
- RR 16-2005: Subject to 12% VAT if lessor is VAT-registered (gross receipts > PHP 3M)
- RR 2-98 (as amended by RR 11-2018, 14-2021): Subject to 5% EWT as rental income
- Residential ≤ PHP 15,000/mo: VAT-exempt per NIRC 109(1)(Q), but still subject to income tax
- RCIT: Applied/forfeited amounts flow to gross receipts for 20-25% RCIT (CREATE Law, RA 11534)

**Accounting entries:**
```
At receipt:
  DR  Cash / Bank                    xxx
      CR  Security Deposit Liability     xxx

At application to unpaid rent:
  DR  Security Deposit Liability     xxx
      CR  Rental Income                  xxx
  (Output VAT liability recognized; EWT receivable if corporate tenant withheld)

At refund:
  DR  Security Deposit Liability     xxx
      CR  Cash / Bank                    xxx

Interest return (controlled residential):
  DR  Interest Expense               xxx
      CR  Cash / Bank                    xxx
```

**EWT timing edge case:** When a corporate tenant has already vacated at the moment of deposit application/forfeiture, the lessee cannot issue Form 2307 (they're no longer paying). The withholding obligation effectively shifts to the lessor's self-assessment — document the application event and include in ITR.

### 3d. Edge Cases

1. **Vacancy decontrol:** When a unit re-leases above PHP 10,000/mo threshold, the 1+2 cap and bank-holding mandate no longer apply. Track per-lease, not per-unit.

2. **Tacit reconduction (Art. 1670):** When a fixed-term lease rolls into month-to-month, the original deposit obligation carries forward. The lessor has no basis to demand a "top-up" unless a new written agreement is executed. If the original controlled rate was below PHP 10,000, the deposit rules under RA 9653 continue.

3. **Deposit top-up on renewal:** On lease renewal with escalated rent, the lessor may request additional deposit to maintain the 2-month ratio. This requires a new agreement and triggers new deposit-handling obligations. For commercial leases, top-up terms are purely contractual.

4. **Partial application:** Tenant has PHP 20,000 deposit, owes PHP 8,000 unpaid rent. Only PHP 8,000 reclassifies as income. Remaining PHP 12,000 remains a liability and must be refunded.

5. **Deposit application order (Art. 1252-1254):** When tenant has multiple debts (rent + utilities + penalties), deposit application follows Civil Code allocation rules: debtor designates → interest before principal → most onerous first. In practice for deposits, the landlord typically allocates per the itemized deduction statement and the tenant can contest.

6. **Advance rent vs. deposit substance test:** A "deposit" earmarked as the last month's rent is advance rent in substance. BIR looks at refundability: if no obligation to refund → advance rent → taxable at receipt.

7. **PFRS 16 (lessee side):** For corporate tenants, refundable deposits require present-value measurement as financial assets. The lessor system doesn't control this, but should provide clear documentation to support tenant accounting.

---

## 4. What Crispina Built

**Nothing.** Security deposit tracking is entirely absent from the Crispina codebase.

**Confirmed gaps (from `input/crispina-models.md`):**
- No `SecurityDeposit` or `DepositLedger` model
- No `DepositDeduction` model
- No `DepositRefund` model
- No deposit-related `ChargeType` seeded
- No `bank_account_reference` field anywhere
- No interest accrual tracking
- No lease-end inspection model
- Tenant model lacks `is_rent_controlled` flag needed for regime determination
- Lease model lacks status field to trigger end-of-lease deposit workflow

**Adjacent Crispina features relevant to deposits:**
- `Charge` model stores `base_amount` + `vat_rate_used` — could be adapted for deposit application charges
- `Payment` → `PaymentAllocation` pattern could track refund disbursements
- `ChargeType` is extensible — deposit collection/application/refund could be new charge types
- `CurrencyDecimal(10,2)` precision is adequate for deposit amounts

---

## 5. Lightweight Feature Spec

### 5a. Data Model

```
SecurityDeposit
  pk: UUID
  lease_pk: FK → Lease
  tenant_pk: FK → Tenant
  deposit_type: ENUM(SECURITY_DEPOSIT, ADVANCE_RENT)
  amount_collected: CurrencyDecimal
  date_collected: Date
  bank_account_reference: String(255), nullable  -- required for controlled residential
  lease_regime: ENUM(CONTROLLED_RESIDENTIAL, COMMERCIAL, NON_CONTROLLED_RESIDENTIAL)
  status: ENUM(HELD, PARTIALLY_APPLIED, FULLY_APPLIED, REFUNDED)
  created_at, last_updated_at

DepositInterestAccrual
  pk: UUID
  security_deposit_pk: FK → SecurityDeposit
  accrual_period_start: Date  -- e.g., start of month
  accrual_period_end: Date
  interest_rate_applied: PercentageDecimal  -- actual bank rate
  interest_amount: CurrencyDecimal
  source: ENUM(BANK_PASSBOOK, COMPUTED)
  created_at

DepositDeduction
  pk: UUID
  security_deposit_pk: FK → SecurityDeposit
  deduction_type: ENUM(UNPAID_RENT, UNPAID_UTILITIES, PROPERTY_DAMAGE, OTHER)
  description: String(500)  -- itemized description
  amount: CurrencyDecimal
  receipt_reference: String(255), nullable  -- OR# or quotation ref
  supporting_document_path: String(500), nullable
  date_assessed: Date
  assessed_by: String(255)  -- inspector name
  created_at

DepositApplication
  pk: UUID
  security_deposit_pk: FK → SecurityDeposit
  amount_applied: CurrencyDecimal
  application_type: ENUM(RENT_ARREARS, UTILITY_ARREARS, DAMAGE_DEDUCTION, FORFEITURE)
  date_applied: Date
  charge_pk: FK → Charge, nullable  -- links to the Charge created for tax purposes
  vat_amount: CurrencyDecimal  -- 12% VAT on applied amount (if VAT-registered)
  ewt_amount: CurrencyDecimal  -- 5% EWT (if corporate tenant)
  notes: Text, nullable
  created_at

DepositRefund
  pk: UUID
  security_deposit_pk: FK → SecurityDeposit
  amount_refunded: CurrencyDecimal  -- deposit balance after deductions
  interest_refunded: CurrencyDecimal  -- accrued bank interest (controlled)
  total_refund: CurrencyDecimal  -- amount_refunded + interest_refunded
  refund_method: ENUM(CHECK, BANK_TRANSFER, CASH)
  refund_reference: String(255)  -- check# or transfer ref
  date_refunded: Date
  date_turnover: Date  -- when tenant surrendered premises
  deadline_date: Date  -- computed: turnover + 30 days
  is_overdue: Boolean (computed hybrid)
  created_at
```

**Enhancements to existing models:**

```
Lease (add fields):
  + lease_regime: ENUM(CONTROLLED_RESIDENTIAL, COMMERCIAL, NON_CONTROLLED_RESIDENTIAL)
  + status: ENUM(ACTIVE, EXPIRED, TERMINATED, MONTH_TO_MONTH)
  + date_turnover: Date, nullable  -- actual premises return date

Tenant (add fields):
  + tin: String(20), nullable  -- BIR TIN
  + is_corporate: Boolean, default False
  + is_vat_registered: Boolean, default False

Rentable (add fields):
  + unit_type: ENUM(RESIDENTIAL, COMMERCIAL)
```

### 5b. Formulas and Logic

**Deposit cap validation (at collection):**
```python
if lease.lease_regime == CONTROLLED_RESIDENTIAL:
    assert deposit.amount_collected <= 2 * lease.monthly_rent
    assert advance_rent_amount <= 1 * lease.monthly_rent
    # Require bank_account_reference
    assert deposit.bank_account_reference is not None
```

**Interest accrual (controlled residential only):**
```python
# Manual entry per period (from bank passbook)
# OR computed at a default rate if bank rate unavailable
# All interest belongs to tenant — no lessor share
total_interest = sum(accrual.interest_amount for accrual in deposit.interest_accruals)
```

**Refund computation:**
```python
total_deductions = sum(d.amount for d in deposit.deductions)
assert total_deductions <= deposit.amount_collected  # Cannot deduct more than deposit

refund_amount = deposit.amount_collected - total_deductions
interest_amount = total_interest_accrued  # controlled residential only
total_refund = refund_amount + interest_amount

# Deadline check
deadline = deposit_refund.date_turnover + timedelta(days=30)
is_overdue = date.today() > deadline
```

**Tax reclassification on application:**
```python
def apply_deposit(deposit, amount, application_type):
    # Create Charge record for the applied amount (reclassify to income)
    charge = Charge(
        base_amount=amount,
        vat_rate_used=Decimal("0.1200") if lessor_is_vat_registered else Decimal("0.0000"),
        charge_type_pk=DEPOSIT_APPLICATION_CHARGE_TYPE,
        date_issued=date.today(),
        tenant_pk=deposit.tenant_pk,
    )

    # VAT component
    if lessor_is_vat_registered and monthly_rent > 15000:
        vat = round_currency(amount * Decimal("0.12"))
    else:
        vat = Decimal("0.00")

    # EWT (only if corporate tenant and not already vacated)
    if tenant.is_corporate:
        ewt = round_currency(amount * Decimal("0.05"))
    else:
        ewt = Decimal("0.00")

    application = DepositApplication(
        security_deposit_pk=deposit.pk,
        amount_applied=amount,
        application_type=application_type,
        date_applied=date.today(),
        charge_pk=charge.pk,
        vat_amount=vat,
        ewt_amount=ewt,
    )

    # Update deposit status
    total_applied = sum(a.amount_applied for a in deposit.applications) + amount
    if total_applied >= deposit.amount_collected:
        deposit.status = FULLY_APPLIED
    else:
        deposit.status = PARTIALLY_APPLIED
```

**Overdue penalty (delayed refund):**
```python
# Legal interest: 6% p.a. from date of formal demand (Nacar v. Gallery Frames)
# Only applies AFTER formal demand letter sent and deadline passed
if demand_date and date.today() > demand_date:
    days_overdue = (date.today() - demand_date).days
    legal_interest = round_currency(
        refund_amount * Decimal("0.06") * days_overdue / 365
    )
```

### 5c. Business Rules / Decision Tree

```
LEASE STARTS:
  ├─ Is unit controlled residential (rent ≤ PHP 10K/mo in NCR)?
  │   ├─ YES → Max deposit = 2 months rent
  │   │        Max advance = 1 month rent
  │   │        Bank account REQUIRED
  │   │        Interest tracking REQUIRED
  │   └─ NO  → No cap; bank-hold recommended but not mandated
  │            Interest per contract only
  │
  DURING LEASE:
  │  ├─ Controlled → Record interest accruals periodically (from passbook)
  │  └─ Commercial → No action unless contractual interest clause
  │
  LEASE ENDS:
  ├─ Premises inspection → generate deduction list
  │   ├─ Each deduction must be:
  │   │   ├─ Beyond normal wear and tear
  │   │   ├─ Supported by receipts or quotations
  │   │   └─ Within the deposit amount (cannot deduct more than held)
  │   │
  │   ├─ Deductions > 0?
  │   │   ├─ YES → Create DepositApplication(s) for each deduction type
  │   │   │        Reclassify applied amount as income
  │   │   │        Trigger VAT output (if VAT-registered, rent > PHP 15K)
  │   │   │        Trigger EWT tracking (if corporate tenant)
  │   │   └─ NO  → Full refund
  │   │
  │   └─ Compute refund = deposit - total deductions + interest (controlled)
  │
  REFUND:
  ├─ Issue within 30 days of turnover
  ├─ Refund = deposit balance + all accrued interest (controlled)
  ├─ If overdue → 6% p.a. legal interest from demand date
  └─ Record refund method, reference, date

  TAX EVENTS:
  ├─ Application: DR Deposit Liability / CR Rental Income
  │   ├─ Include in gross receipts for VAT (2550Q)
  │   ├─ Include in gross receipts for income tax (1702Q)
  │   └─ Track EWT via 2307 (if corporate tenant still active)
  └─ Refund: DR Deposit Liability / CR Cash (no income event)
```

### 5d. Inputs and Outputs

**Inputs:**
- Lease details (tenant, unit, regime, monthly rent, start/end dates)
- Deposit amount collected
- Bank account reference (controlled residential)
- Periodic interest accrual records (from bank passbook)
- Premises inspection report (at lease end)
- Deduction items with supporting documents
- Demand letter date (if refund delayed)

**Outputs:**
- Per-tenant deposit ledger showing current balance and status
- Interest accrual log (controlled residential)
- Itemized deduction statement (for tenant and accountant)
- Tax reclassification journal entries (for accountant handoff)
- VAT and EWT amounts on applied deposits (for BIR returns)
- Refund check/transfer instruction
- Overdue refund alert with legal interest computation
- Dashboard: deposits approaching lease-end (30/60/90 day alerts)
- Subsidiary ledger — Security Deposits (liability schedule for AFS)

### 5e. Reporting for Accountant Handoff

The deposit system must produce:
1. **Monthly:** Security deposit liability schedule (per-tenant breakdown, movements)
2. **Quarterly:** Applied/forfeited deposits summary for inclusion in 2550Q (VAT) and 1702Q (income tax)
3. **Annually:** Full deposit register with opening balance, collections, applications, refunds, closing balance — for AFS notes disclosure under PFRS 15
4. **Ad hoc:** Per-event reclassification journal entries when deposits are applied or forfeited

---

## 6. Automability Score: 3/5

**Justification:**

Deterministic (automatable) elements:
- Deposit cap validation (2-month rule for controlled, no cap for commercial) → purely formulaic
- Interest accrual computation once rate is entered → formulaic
- Refund deadline calculation → date arithmetic
- Tax reclassification journal entries → deterministic once application amount is known
- VAT and EWT computation on applied amounts → formulaic
- Overdue interest at 6% p.a. → formulaic
- Dashboard alerts for approaching lease-ends → date comparison

Human judgment required:
- **Premises inspection:** Distinguishing "normal wear and tear" from deductible damage is inherently subjective and frequently disputed. No formula can automate this — it requires physical inspection and judgment.
- **Deduction amount:** Even when damage is acknowledged, the cost of repair is estimated (quotation-based), not computed.
- **Regime classification at lease start:** Determining whether a unit qualifies as "controlled residential" requires human assessment of rent level, location, and unit type.
- **Interest rate entry:** Bank passbook interest must be manually extracted and entered.
- **Demand letter issuance:** Decision to send a formal demand for overdue refund is a legal/business judgment.
- **Deposit application allocation:** When tenant owes multiple debts, deciding which to apply deposit against involves judgment (though Art. 1252-1254 provides a default hierarchy).

The lifecycle score is lower than billing (5/5) or payment tracking (4/5) because the critical lease-end phase — inspection, deduction assessment, and dispute resolution — is fundamentally a human judgment process. The system automates the bookkeeping, computation, and compliance tracking around those decisions, but cannot replace the decisions themselves.

---

## 7. Verification Status

All regulatory rules cross-checked against 2+ independent sources via verification subagent.

| Rule | Status | Sources |
|------|--------|---------|
| Deposit caps (2+1 controlled, no cap commercial) | **CONFIRMED** | LawPhil RA 9653, Respicio, ChanRobles, Salenga Law |
| Bank-holding mandate (controlled) | **CONFIRMED** | LawPhil RA 9653, AVISO Law, Salenga Law |
| Return timeline (1 month / 30-day benchmark) | **CONFIRMED** | Respicio (2 articles), BSP Circular 799, Nacar v. Gallery Frames |
| Deduction rules (itemized, burden on landlord) | **CONFIRMED** | Respicio (2 articles), RichestPH, ChanRobles; NOTE: "Radiowealth Finance v. Palacol" citation in Wave 1 input is **hallucinated** — no such PH SC case exists. Principle is valid from Civil Code Arts. 1170, 1173, 19 and RA 9653 Sec. 7 |
| Tax: not taxable at receipt | **CONFIRMED** | BIR Ruling DA-334-2004, RMC 11-2024, BDB Law, KPMG PH |
| Tax: taxable at application/forfeiture | **CONFIRMED** | BIR Ruling 118-12, DA-489-03, RR 16-2005, PwC PH, Forvis Mazars |
| Interest: all bank interest to lessee (controlled) | **CONFIRMED** | LawPhil RA 9653, Respicio, BSP E-Library |
| PFRS/accounting treatment | **CONFIRMED** | Grant Thornton PH, Respicio, BDB Law |
| Estafa exposure on misappropriation | **CONFIRMED** | NDV Law, Respicio, Legaspi v. People (SC) |
| Deposit application order (Art. 1252-1254) | **CONFIRMED** | Respicio, ChanRobles, JurisDoctor |

### Corrections to Wave 1 Input

1. **`input/security-deposit-rules.md` line 67:** "Radiowealth Finance v. Palacol" citation does not exist. The principle (itemized deductions required, burden on landlord) derives from Civil Code Arts. 1170, 1173, Art. 19 and RA 9653 Sec. 7.
2. **`input/security-deposit-rules.md` lines 30-32:** RA 9653 Sec. 12 provides fines of PHP 25,000–50,000, not "up to PHP 100,000."
3. **`input/security-deposit-rules.md` line 10:** Coverage is NCR + highly urbanized cities, not just "Metro Manila."
4. **BIR Rulings DA-593-04 and 025-02:** Specific ruling numbers unverifiable via primary sources, though the legal principles they represent are confirmed through other authoritative rulings (DA-489-03, 033-00, RR 16-2005).

---

## 8. Process Dependencies

**Feeds into:**
- **Rent roll preparation** → deposit movements reported monthly to accountant
- **Tax data compilation** → applied/forfeited amounts in gross receipts for VAT and income tax
- **Expense tracking** → interest returned to controlled tenants is a deductible expense
- **Official receipt data** → application of deposit to rent requires OR/invoice issuance
- **Lease contract generation** → deposit amount/terms embedded in contract
- **Lease renewal/extension** → deposit top-up or carry-forward decision

**Depends on:**
- **Tenant payment tracking** → determine unpaid rent balances for deduction
- **Water/electric billing** → determine unpaid utility balances for deduction
- **Late payment penalties** → penalties may be deducted from deposit
- **Lease status visibility** → lease-end triggers deposit refund workflow

---

*Source files: input/security-deposit-rules.md, input/crispina-models.md, input/crispina-services.md, input/corporate-rental-tax.md, input/lease-contract-requirements.md. Verification via cross-reference against 20+ independent sources.*
