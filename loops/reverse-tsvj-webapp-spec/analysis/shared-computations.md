# Shared Computations Package — `@tsvj/computations`

*Wave 2 Architecture Decision | Depends on: data-model-extract, cross-cutting-extract, project-structure, database-schema*

---

## Decision Summary

Pure TypeScript package (`@tsvj/computations`) with **zero internal dependencies** — only `decimal.js ^10` for arbitrary-precision arithmetic. All billing, tax, penalty, deposit, and lease computation logic lives here as pure functions: data in → result out, no database access, no I/O. This enables deterministic unit testing of ~95 regulatory rules independently of the API/UI layers.

**Key design choices:**
- `Peso` wrapper type around `Decimal` for all monetary arithmetic
- 7 context-specific rounding helpers (not a generic "round" function)
- All functions accept plain objects (not Drizzle row types) — decoupled from ORM
- All monetary inputs/outputs are `string` (matching Drizzle's `numeric` → `string` mapping); converted to `Peso` internally
- Each module exports a primary computation function + supporting helpers
- Every function is synchronous (no async, no side effects)

---

## 1. Decimal Foundation (`src/decimal.ts`)

### 1.1 The `Peso` Type

`Peso` is a thin wrapper around `decimal.js`'s `Decimal` that enforces the invariant: **all monetary values are stored with exactly 2 decimal places at rest, but intermediate computations may use higher precision.**

```ts
import Decimal from "decimal.js";

// Configure decimal.js globally for this package
Decimal.set({
  precision: 20,       // More than enough for PHP monetary values
  rounding: Decimal.ROUND_HALF_UP,  // Default rounding mode (overridden per context)
});

/** Monetary value in Philippine Pesos. Wraps decimal.js Decimal. */
export type Peso = Decimal;

/**
 * Create a Peso from string, number, or Decimal.
 * Strings are the canonical input format (from Drizzle numeric columns).
 */
export function peso(value: string | number | Decimal): Peso {
  return new Decimal(value);
}

/** Convert Peso back to string for storage/serialization (2 decimal places). */
export function pesoToString(value: Peso): string {
  return value.toFixed(2);
}

/** Rate type — percentages stored as decimals (0.12 = 12%). */
export type Rate = Decimal;

export function rate(value: string | number | Decimal): Rate {
  return new Decimal(value);
}
```

### 1.2 Context-Specific Rounding Functions

Seven distinct rounding contexts from the cross-cutting extract. Each is a named function — callers never choose rounding modes manually.

```ts
/**
 * NHSB rent escalation: ROUND_DOWN (truncate toward zero).
 * Precedent: Crispina math.py uses floor rounding for escalation.
 * Example: PHP 10,230.456 → PHP 10,230.45
 */
export function roundNHSB(value: Peso): Peso {
  return value.toDecimalPlaces(2, Decimal.ROUND_DOWN);
}

/**
 * Water per-tier billing: Standard HALF_UP rounding to 2 decimals.
 * Example: PHP 523.455 → PHP 523.46
 */
export function roundWater(value: Peso): Peso {
  return value.toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
}

/**
 * Electric blended rate: HALF_UP to 4 decimals (for per-kWh rate),
 * then final charge rounded to 2 decimals.
 */
export function roundElectricRate(value: Decimal): Decimal {
  return value.toDecimalPlaces(4, Decimal.ROUND_HALF_UP);
}

export function roundElectricCharge(value: Peso): Peso {
  return value.toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
}

/**
 * VAT computation: HALF_UP to 2 decimals.
 * vat_amount = ROUND(base_amount × vat_rate, 2)
 */
export function roundVAT(value: Peso): Peso {
  return value.toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
}

/**
 * EWT computation: HALF_UP to 2 decimals.
 * ewt_amount = ROUND(gross_amount × ewt_rate, 2)
 */
export function roundEWT(value: Peso): Peso {
  return value.toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
}

/**
 * Penalty computation: HALF_UP to 2 decimals, then cap check applied separately.
 */
export function roundPenalty(value: Peso): Peso {
  return value.toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
}

/**
 * Generic monetary rounding (for cases not covered above — e.g., deposit refund).
 * HALF_UP to 2 decimals.
 */
export function roundMoney(value: Peso): Peso {
  return value.toDecimalPlaces(2, Decimal.ROUND_HALF_UP);
}
```

### 1.3 Comparison Helpers

```ts
/** Check if a monetary amount is zero. */
export function isZero(value: Peso): boolean {
  return value.isZero();
}

/** Check if value > 0. */
export function isPositive(value: Peso): boolean {
  return value.greaterThan(0);
}

/** Minimum of two Peso values. */
export function minPeso(a: Peso, b: Peso): Peso {
  return Decimal.min(a, b);
}

/** Maximum of two Peso values. */
export function maxPeso(a: Peso, b: Peso): Peso {
  return Decimal.max(a, b);
}
```

---

## 2. Computation Modules

Each module follows the same pattern:
1. **Input type:** A plain object describing the data needed (not a Drizzle row)
2. **Output type:** A plain object describing the computed result
3. **Primary function:** A single entry-point function that does the computation
4. **Supporting functions:** Smaller helpers used by the primary function (also exported for testing)

All monetary fields in input/output types use `string` (matching Drizzle → tRPC → client serialization). Internal arithmetic uses `Peso`.

---

### 2.1 Escalation (`src/escalation/`)

#### `nhsb.ts` — NHSB Cap Rate Escalation

```ts
export interface NHSBEscalationInput {
  currentRent: string;       // Current monthly rent (Peso string)
  nhsbCapRate: string;       // NHSB cap rate for the year (e.g., "0.023" for 2.3%)
  leaseAnniversaryDate: string; // ISO date string
  effectiveDate: string;     // When new rent takes effect (ISO date)
}

export interface EscalationResult {
  previousRent: string;
  newRent: string;           // After applying escalation and ROUND_DOWN
  escalationRate: string;    // Rate used (e.g., "0.023")
  escalationAmount: string;  // newRent - previousRent
  effectiveDate: string;
  thresholdCrossed: boolean; // true if newRent > PHP 10,000 (exits rent control)
}

export function computeNHSBEscalation(input: NHSBEscalationInput): EscalationResult;
```

**Rules applied:**
- `newRent = ROUND_DOWN(currentRent × (1 + nhsbCapRate), 2)`
- Compounding: applies to *current* rent (not original rent)
- Threshold crossing: `newRent > 10000` → `thresholdCrossed = true`
- Max once per 12 months (enforced by caller — this function is stateless)

#### `contractual.ts` — Contractual Escalation

```ts
export type EscalationType = "FIXED_PERCENT" | "STEPPED" | "CPI_LINKED" | "NONE";

export interface ContractualEscalationInput {
  currentRent: string;
  escalationType: EscalationType;
  escalationParams: ContractualEscalationParams;
  yearIndex: number;         // Which year of the lease (1-indexed)
}

export type ContractualEscalationParams =
  | { type: "FIXED_PERCENT"; rate: string }            // e.g., "0.05" for 5%
  | { type: "STEPPED"; schedule: SteppedRate[] }       // year → rate
  | { type: "CPI_LINKED"; baseRate: string; cpiAdjustment: string }
  | { type: "NONE" };

export interface SteppedRate {
  fromYear: number;
  toYear: number;
  rate: string;
}

export function computeContractualEscalation(input: ContractualEscalationInput): EscalationResult;
```

**Rules applied:**
- FIXED_PERCENT: `newRent = roundMoney(currentRent × (1 + rate))`
- STEPPED: look up rate for `yearIndex` in schedule, then apply like FIXED_PERCENT
- CPI_LINKED: `newRent = roundMoney(currentRent × (1 + baseRate + cpiAdjustment))`
- NONE: `newRent = currentRent` (identity)
- No ROUND_DOWN here — that's NHSB-specific. Commercial uses standard rounding.

#### `threshold.ts` — Rent Control Threshold

```ts
export interface ThresholdCheckInput {
  newMonthlyRent: string;
  unitType: "RESIDENTIAL" | "COMMERCIAL";
  currentRegime: "CONTROLLED_RESIDENTIAL" | "NON_CONTROLLED_RESIDENTIAL" | "COMMERCIAL";
}

export interface ThresholdCheckResult {
  crossedThreshold: boolean;
  newRegime: "CONTROLLED_RESIDENTIAL" | "NON_CONTROLLED_RESIDENTIAL" | "COMMERCIAL";
  reason: string | null;     // e.g., "Rent PHP 10,230 exceeds PHP 10,000 threshold"
}

/** PHP 10,000/month threshold for rent control exit (RA 9653). */
export const RENT_CONTROL_THRESHOLD = "10000";

export function checkThresholdCrossing(input: ThresholdCheckInput): ThresholdCheckResult;
```

---

### 2.2 Water Billing (`src/water/`)

#### `tiered-billing.ts` — Maynilad Per-Tier Computation

```ts
export interface WaterTier {
  minCuM: number;            // Inclusive lower bound (cu.m.)
  maxCuM: number | null;     // Inclusive upper bound (null = unlimited)
  ratePerCuM: string;        // Peso per cu.m. for this tier
}

export interface WaterBillingInput {
  consumption: number;        // Tenant's metered consumption in cu.m.
  tiers: WaterTier[];         // Maynilad rate schedule (ordered by tier)
  environmentalChargePct: string;  // e.g., "0.25" (25% of Basic Charge, 2025+)
  sewerageChargePct: string;  // e.g., "0.20" (20% of Basic Charge) or "0" for residential
  fcdaPerCuM: string;        // Foreign Currency Differential Adjustment (quarterly)
  mscAmount: string;         // Maintenance Service Charge (flat)
  isResidential: boolean;    // Controls sewerage (residential = no sewerage)
}

export interface WaterBillingResult {
  tierBreakdown: TierBreakdownLine[];  // Per-tier consumption and charge
  basicCharge: string;        // Sum of tier charges
  environmentalCharge: string;
  sewerageCharge: string;     // "0.00" for residential
  fcdaCharge: string;
  mscCharge: string;
  totalBeforeVAT: string;
  vatRate: string;            // Always "0.00" for water pass-through
  vatAmount: string;          // Always "0.00"
  totalCharge: string;        // = totalBeforeVAT (since no VAT on water)
}

export interface TierBreakdownLine {
  tierNumber: number;
  consumptionInTier: number;  // cu.m. consumed in this tier
  ratePerCuM: string;
  tierCharge: string;
}

export function computeWaterBilling(input: WaterBillingInput): WaterBillingResult;
```

**Rules applied:**
- Each tenant's consumption starts at lowest tier (per-tier, NOT blended)
- `basicCharge = SUM(consumptionInTier × ratePerCuM)` across tiers, each tier rounded via `roundWater`
- `environmentalCharge = roundWater(basicCharge × environmentalChargePct)`
- `sewerageCharge = isResidential ? 0 : roundWater(basicCharge × sewerageChargePct)`
- `fcdaCharge = roundWater(consumption × fcdaPerCuM)`
- `totalBeforeVAT = basicCharge + environmentalCharge + sewerageCharge + fcdaCharge + mscCharge`
- VAT = 0 always (water pass-through is NOT VATable per BIR RR 16-2005)

#### `allocation.ts` — Common Area / Shared Meter Allocation

```ts
export interface AllocationInput {
  totalMasterBill: string;   // Maynilad master meter total
  tenantCharges: { tenantId: number; charge: string }[];
  commonAreaConsumption: number;  // cu.m. not assigned to any tenant meter
  allocationMethod: "FLOOR_AREA" | "EQUAL_SPLIT";
  tenantFloorAreas?: { tenantId: number; floorAreaSqm: string }[];
  activeTenantCount: number;
}

export interface AllocationResult {
  commonAreaCharge: string;  // Total common area cost
  perTenantAllocation: { tenantId: number; commonAreaShare: string }[];
  reconciliationDelta: string;  // totalMasterBill - SUM(tenantCharges) - commonAreaCharge (should be ~0)
}

export function allocateCommonArea(input: AllocationInput): AllocationResult;
```

**Rules applied:**
- FLOOR_AREA: `share_i = commonAreaCharge × (floorArea_i / totalFloorArea)`
- EQUAL_SPLIT: `share_i = commonAreaCharge / activeTenantCount`
- Reconciliation check: `|delta| ≤ 1.00` (rounding variance acceptable)

---

### 2.3 Electric Billing (`src/electric/`)

#### `blended-rate.ts` — Meralco Blended Rate

```ts
export interface ElectricBillingInput {
  meralcoTotalBill: string;  // Total Meralco bill amount
  meralcoTotalKwh: number;   // Total kWh on master meter
  tenantConsumption: number;  // This tenant's sub-meter kWh
  adminFeePerKwh: string;    // Optional admin fee (e.g., "1.00"), "0" if none
  vatRate: string;            // From AppSettings.electric_vat_treatment: "0.12", "0", or "PENDING"
}

export interface ElectricBillingResult {
  blendedRatePerKwh: string;  // roundElectricRate(meralcoTotalBill / meralcoTotalKwh)
  baseCharge: string;          // roundElectricCharge(tenantConsumption × blendedRatePerKwh)
  adminFee: string;            // roundElectricCharge(tenantConsumption × adminFeePerKwh)
  subtotal: string;            // baseCharge + adminFee
  vatRate: string;
  vatAmount: string;           // roundVAT(subtotal × vatRate), or "0.00" if exempt/pending
  totalCharge: string;         // subtotal + vatAmount
}

export function computeElectricBilling(input: ElectricBillingInput): ElectricBillingResult;
```

**Rules applied:**
- `blendedRate = roundElectricRate(meralcoTotalBill / meralcoTotalKwh)` — 4 decimal places
- `baseCharge = roundElectricCharge(consumption × blendedRate)` — 2 decimal places
- Admin fee: separate line item, not embedded in per-kWh rate
- VAT: depends on `AppSettings.electric_vat_treatment` — if "PENDING", treated as 0 but flagged

#### `allocation.ts` — Common Area Electric Allocation

Same pattern as water allocation — shared meter common area allocated by floor area or equal split.

```ts
export function allocateElectricCommonArea(input: AllocationInput): AllocationResult;
```

Reuses the same `AllocationInput` / `AllocationResult` types from `src/water/allocation.ts`. These types are moved to a shared `src/types.ts` file.

---

### 2.4 Penalty (`src/penalty/`)

#### `simple-interest.ts` — Late Payment Penalty Computation

```ts
export interface PenaltyInput {
  unpaidAmount: string;       // Outstanding base amount (pre-VAT)
  penaltyRateMonthly: string; // e.g., "0.01" (1%/month) for controlled, "0.03" for commercial
  daysOverdue: number;        // Days past grace period
  gracePeriodDays: number;    // 5 for controlled (RA 9653), per contract for commercial
  dueDate: string;            // ISO date — charge due date
  paymentDate: string;        // ISO date — date of computation
}

export interface PenaltyResult {
  rawPenalty: string;         // Before cap application
  cappedPenalty: string;      // After cap (if controlled)
  capApplied: boolean;        // true if cap reduced the amount
  daysOverdue: number;
  effectiveDaysCharged: number; // days after grace period
}

export function computePenalty(input: PenaltyInput): PenaltyResult;
```

**Rules applied:**
- `effectiveDays = max(0, daysOverdue - gracePeriodDays)`
- `rawPenalty = roundPenalty(unpaidAmount × penaltyRateMonthly × (effectiveDays / 30))`
- Simple interest only — no compounding (Art. 2212: compound interest only from judicial demand)
- Cap applied separately (see below)

#### `caps.ts` — Controlled Lease Safe Harbour Caps

```ts
export interface PenaltyCapInput {
  rawPenalty: string;          // From computePenalty
  monthlyRent: string;         // Current monthly rent
  totalPenaltiesThisYear: string; // Sum of all penalties assessed in the current year
  leaseRegime: "CONTROLLED_RESIDENTIAL" | "NON_CONTROLLED_RESIDENTIAL" | "COMMERCIAL";
}

export interface PenaltyCapResult {
  finalPenalty: string;        // After both caps applied
  monthlyCapApplied: boolean;  // Exceeded 1%/month
  annualCapApplied: boolean;   // Exceeded 1 month's rent / year
}

/**
 * Controlled residential safe harbour:
 * - Per-month cap: ≤ 1% of monthly rent
 * - Annual cap: total penalties in year ≤ 1 month's rent
 */
export function applyPenaltyCaps(input: PenaltyCapInput): PenaltyCapResult;
```

**Rules applied (controlled residential only):**
- Monthly cap: `min(rawPenalty, roundPenalty(monthlyRent × 0.01))`
- Annual cap: `min(afterMonthlyCap, monthlyRent - totalPenaltiesThisYear)`
- If `leaseRegime !== "CONTROLLED_RESIDENTIAL"`, return rawPenalty unchanged (no caps)

---

### 2.5 Billing (`src/billing/`)

#### `vat.ts` — VAT Determination Logic

```ts
export type ChargeTypeCode =
  | "RENT" | "WATER" | "ELECTRIC" | "PENALTY"
  | "DEPOSIT_APPLICATION" | "ADMIN_FEE" | "OTHER";

export interface VATDeterminationInput {
  chargeType: ChargeTypeCode;
  unitType: "RESIDENTIAL" | "COMMERCIAL";
  currentMonthlyRent: string;
  lessorIsVATRegistered: boolean;
  electricVATSetting: "VATABLE" | "EXEMPT" | "PENDING";
}

export interface VATDeterminationResult {
  vatRate: string;            // "0.12" or "0.00"
  isVATExempt: boolean;       // true for residential ≤ PHP 15K
  reason: string;             // Human-readable (e.g., "Residential ≤ PHP 15K — NIRC 109(1)(Q)")
  requiresReview: boolean;    // true if PENDING electric VAT
}

/** PHP 15,000/month VAT exemption threshold for residential (NIRC Sec. 109(1)(Q)). */
export const VAT_EXEMPT_THRESHOLD = "15000";

/** PHP 3,000,000 aggregate annual receipts VAT registration threshold. */
export const VAT_REGISTRATION_THRESHOLD = "3000000";

export function determineVATRate(input: VATDeterminationInput): VATDeterminationResult;
```

**Rules applied (decision tree from cross-cutting extract §1.1):**
1. WATER → always 0% (not VATable, BIR RR 16-2005)
2. ELECTRIC → from `electricVATSetting` (configurable, CONFLICTING rule)
3. RESIDENTIAL + rent ≤ PHP 15K → 0% (permanent exemption)
4. Lessor below PHP 3M threshold → 0%
5. All other → 12%

#### `charge-builder.ts` — Build Charge Record

```ts
export interface ChargeBuilderInput {
  baseAmount: string;         // Pre-VAT amount
  vatRate: string;            // From determineVATRate
  chargeType: ChargeTypeCode;
  leaseId: number;
  billingPeriodStart: string; // ISO date
  billingPeriodEnd: string;   // ISO date
  dueDate: string;            // ISO date
}

export interface BuiltCharge {
  baseAmount: string;
  vatRate: string;
  vatAmount: string;          // roundVAT(baseAmount × vatRate)
  totalAmount: string;        // baseAmount + vatAmount
  isVATExempt: boolean;
}

export function buildCharge(input: ChargeBuilderInput): BuiltCharge;
```

---

### 2.6 Payment Allocation (`src/payment/`)

#### `art-1252.ts` — Civil Code Art. 1252-1254 Allocation

```ts
export interface OutstandingCharge {
  chargeId: number;
  chargeType: ChargeTypeCode;
  baseAmount: string;
  vatAmount: string;
  totalAmount: string;
  unpaidAmount: string;       // Remaining unpaid on this charge
  dueDate: string;            // For FIFO ordering
  isInterestOrPenalty: boolean; // Art. 1253: interest/penalties before principal
}

export interface PaymentAllocationInput {
  paymentAmount: string;      // Total payment received
  ewtWithheld: string;        // EWT deducted by corporate tenant (reduces cash, not invoice total)
  outstandingCharges: OutstandingCharge[]; // All unpaid charges for this tenant
  tenantDesignation: number[] | null;  // Charge IDs the tenant wants to pay (Art. 1252), null = auto
  isCorporateTenant: boolean;
}

export interface AllocationLine {
  chargeId: number;
  allocatedAmount: string;    // Amount applied to this charge
  chargeFullyPaid: boolean;
}

export interface PaymentAllocationResult {
  allocations: AllocationLine[];
  totalAllocated: string;     // Sum of all allocations
  remainingCredit: string;    // paymentAmount - totalAllocated (overpayment if > 0)
  ewtAllocated: string;       // EWT portion applied
}

export function allocatePayment(input: PaymentAllocationInput): PaymentAllocationResult;
```

**Rules applied:**
1. **Art. 1252 (debtor designates):** If `tenantDesignation` is not null, allocate to those charges in order
2. **Art. 1253 (mandatory):** Interest and penalties satisfied before principal — always enforced regardless of designation
3. **Art. 1254 (most onerous → FIFO):** If no designation, sort charges by: (a) interest/penalty first, (b) then most onerous (highest interest-bearing or oldest overdue), (c) then FIFO by due date
4. **EWT reconciliation:** For corporate tenants, `cashReceived + ewtWithheld = invoiceTotal`. The EWT portion is treated as partial satisfaction of the invoice.

---

### 2.7 Deposit (`src/deposit/`)

#### `validation.ts` — Deposit Cap Validation

```ts
export interface DepositValidationInput {
  depositMonths: number;       // Requested deposit in months of rent
  advanceMonths: number;       // Requested advance rent in months
  monthlyRent: string;
  leaseRegime: "CONTROLLED_RESIDENTIAL" | "NON_CONTROLLED_RESIDENTIAL" | "COMMERCIAL";
}

export interface DepositValidationResult {
  isValid: boolean;
  maxDepositMonths: number;    // 2 for controlled, unlimited for commercial
  maxAdvanceMonths: number;    // 1 for controlled, unlimited for commercial
  violation: string | null;    // e.g., "Controlled residential: max 2 months deposit + 1 month advance (RA 9653 Sec. 7)"
  depositAmount: string;       // depositMonths × monthlyRent
  advanceAmount: string;       // advanceMonths × monthlyRent
}

export function validateDeposit(input: DepositValidationInput): DepositValidationResult;
```

**Rules applied:**
- Controlled residential: max 2 months deposit + 1 month advance (RA 9653 Sec. 7)
- Commercial: no cap (freedom of contract)
- Validation returns violation message but does not throw — the caller decides how to handle

#### `refund.ts` — Deposit Refund Computation

```ts
export interface DepositRefundInput {
  depositAmount: string;
  accruedInterest: string;     // Bank interest (controlled: ALL returned to lessee)
  deductions: { description: string; amount: string }[];
  leaseRegime: "CONTROLLED_RESIDENTIAL" | "NON_CONTROLLED_RESIDENTIAL" | "COMMERCIAL";
}

export interface DepositRefundResult {
  totalDeductions: string;
  interestReturned: string;    // = accruedInterest for controlled; per contract for commercial
  refundAmount: string;        // deposit - deductions + interestReturned
  isForfeiture: boolean;       // deductions >= deposit + interest
  taxReclassificationAmount: string; // Amount that becomes gross receipts (applied/forfeited portion)
  vatOnReclassification: string;     // 12% of taxReclassificationAmount (if VATable)
  ewtOnReclassification: string;     // 5% of taxReclassificationAmount (if corporate tenant)
}

export function computeDepositRefund(input: DepositRefundInput): DepositRefundResult;
```

**Rules applied:**
- Controlled: ALL interest returned to lessee, even if deductions apply
- `refundAmount = depositAmount - totalDeductions + interestReturned`
- If `totalDeductions >= depositAmount + interestReturned` → forfeiture (but "automatic forfeiture" clauses are void)
- Tax reclassification: applied/forfeited portion becomes gross receipts → VAT + EWT apply (BIR Ruling 118-12)

---

### 2.8 Contract (`src/contract/`)

#### `dst.ts` — Documentary Stamp Tax

```ts
export interface DSTInput {
  monthlyRent: string;
  leaseTermYears: number;     // Integer years (partial years rounded up)
  leaseTermMonths?: number;   // Additional months beyond full years
}

export interface DSTResult {
  annualRent: string;          // monthlyRent × 12
  totalRent: string;           // annualRent × leaseTermYears
  dstAmount: string;           // Per NIRC Sec. 194 formula
  formula: string;             // Human-readable formula breakdown
}

/**
 * NIRC Sec. 194 (TRAIN Law):
 * DST = PHP 6 on first PHP 2,000 + CEIL((totalRent - 2000) / 1000) × PHP 2
 */
export function computeDST(input: DSTInput): DSTResult;
```

**Rules applied:**
- `totalRent = monthlyRent × 12 × leaseTermYears` (+ pro-rata for additional months)
- `dstAmount = 6 + CEIL((totalRent - 2000) / 1000) × 2` (when totalRent > 2000)
- `dstAmount = 6` (when totalRent ≤ 2000)
- No rounding needed — formula produces integer Peso amounts

---

### 2.9 Tax Computations (`src/tax/`)

#### `ewt-rent.ts` — EWT on Rent (5%)

```ts
export interface EWTRentInput {
  chargeBaseAmount: string;    // Pre-VAT charge amount
  chargeType: ChargeTypeCode;
  isCorporateTenant: boolean;
}

export interface EWTRentResult {
  ewtApplicable: boolean;     // true only for corporate tenants
  ewtRate: string;             // "0.05" for rent/penalty/deposit, "0.02" for utilities
  ewtAmount: string;           // roundEWT(chargeBaseAmount × ewtRate)
  atcCode: string;             // "WC157" for rent, "WC160" for utilities
}

export function computeEWTOnRent(input: EWTRentInput): EWTRentResult;
```

**Rules applied:**
- Only corporate tenants withhold EWT (RR 02-98)
- Base rent / penalty / deposit application: 5% (ATC: WC157)
- Utility pass-throughs: 2% (ATC: WC160, reimbursement rate)
- Withholding on base amount (excluding VAT)

#### `ewt-supplier.ts` — EWT on Supplier Payments (2-15%)

```ts
export interface EWTSupplierInput {
  grossAmount: string;         // Expense gross amount
  payeeType: "INDIVIDUAL" | "CORPORATE";
  isVATRegistered: boolean;
  isLargeTaxpayer: boolean;
  ewtRateIndividual: string;   // From ExpenseCategory
  ewtRateCorporate: string;    // From ExpenseCategory
}

export interface EWTSupplierResult {
  ewtRate: string;             // Selected rate based on payee type
  ewtAmount: string;           // roundEWT(grossAmount × ewtRate)
  inputVATCreditable: boolean; // true if supplier is VAT-registered
  inputVATAmount: string;      // 12% of grossAmount if creditable, else "0.00"
  netPayment: string;          // grossAmount - ewtAmount + vatAmount (VAT is NOT withheld)
  atcCode: string;             // From expense category
}

export function computeEWTOnSupplier(input: EWTSupplierInput): EWTSupplierResult;
```

**Rules applied:**
- Rate determined by `payeeType`: individual → `ewtRateIndividual`, corporate → `ewtRateCorporate`
- EWT withheld from gross payment
- VAT is NOT withheld (passed through to supplier)
- Input VAT creditable only from VAT-registered suppliers

#### `vat-summary.ts` — Quarterly VAT Summary (2550Q Data)

```ts
export interface VATSummaryInput {
  charges: { baseAmount: string; vatRate: string; vatAmount: string; isVATExempt: boolean }[];
  inputVATEntries: { vatAmount: string; isCreditable: boolean }[];
  uncollectedReceivables: { baseAmount: string; vatAmount: string; ageInQuarters: number }[];
  apportionmentPct: string;   // VATable revenue ÷ total revenue (for mixed-operation)
}

export interface VATSummaryResult {
  vatableSales: string;
  exemptSales: string;
  zeroRatedSales: string;     // (not applicable in this context, always "0.00")
  outputVAT: string;
  inputVAT: string;            // Total creditable input VAT (after apportionment)
  uncollectedVATDeduction: string;  // RR 3-2024 adjustment (one-quarter claim window)
  netVATPayable: string;       // outputVAT - inputVAT - uncollectedVATDeduction
}

export function computeVATSummary(input: VATSummaryInput): VATSummaryResult;
```

**Rules applied:**
- VATable sales = sum of base amounts where `vatRate > 0`
- Exempt sales = sum of base amounts where `isVATExempt = true`
- Input VAT apportionment: `creditableInput = inputVAT × apportionmentPct` (for mixed-operation)
- Uncollected receivables: `deduction = SUM(vatAmount)` where `ageInQuarters <= 1` (one-quarter claim window, RR 3-2024)

#### `apportionment.ts` — Mixed-Operation Input VAT Apportionment

```ts
export interface ApportionmentInput {
  vatableSales: string;
  exemptSales: string;
  totalInputVAT: string;
}

export interface ApportionmentResult {
  apportionmentPct: string;   // vatableSales / (vatableSales + exemptSales)
  creditableInputVAT: string; // totalInputVAT × apportionmentPct
  nonCreditableInputVAT: string; // totalInputVAT - creditableInputVAT
}

export function computeApportionment(input: ApportionmentInput): ApportionmentResult;
```

---

### 2.10 Lease Lifecycle (`src/lease/`)

#### `state-machine.ts` — Valid State Transitions

```ts
export type LeaseStatus = "DRAFT" | "ACTIVE" | "EXPIRED" | "MONTH_TO_MONTH" | "HOLDOVER" | "TERMINATED" | "RENEWED";

export interface TransitionInput {
  currentStatus: LeaseStatus;
  targetStatus: LeaseStatus;
  leaseRegime: "CONTROLLED_RESIDENTIAL" | "NON_CONTROLLED_RESIDENTIAL" | "COMMERCIAL";
}

export interface TransitionResult {
  isValid: boolean;
  reason: string | null;       // Why invalid, if applicable
  eventType: string | null;    // LeaseEventType to record (e.g., "EXPIRED", "RECONDUCTION_STARTED")
  sideEffects: string[];       // Human-readable list of cascading effects
}

export function validateTransition(input: TransitionInput): TransitionResult;
```

**Valid transitions (from cross-cutting extract §5.1):**
- DRAFT → ACTIVE
- ACTIVE → EXPIRED (auto, daily job)
- ACTIVE → HOLDOVER (commercial only)
- EXPIRED → MONTH_TO_MONTH (auto, 15-day countdown)
- EXPIRED → TERMINATED (admin action)
- EXPIRED → RENEWED (admin action)
- MONTH_TO_MONTH → TERMINATED
- MONTH_TO_MONTH → RENEWED
- HOLDOVER → TERMINATED

#### `alerts.ts` — Expiry Countdown Alert Generation

```ts
export interface LeaseAlertInput {
  dateEnd: string;             // ISO date — lease expiry
  today: string;               // ISO date — current date
  status: LeaseStatus;
  leaseRegime: "CONTROLLED_RESIDENTIAL" | "NON_CONTROLLED_RESIDENTIAL" | "COMMERCIAL";
}

export type AlertLevel = "INFO" | "WARNING" | "URGENT" | "CRITICAL" | "OVERDUE";

export interface LeaseAlertResult {
  alerts: GeneratedAlert[];
}

export interface GeneratedAlert {
  level: AlertLevel;
  daysUntilExpiry: number;
  message: string;
  actionRequired: boolean;
}

/** Alert windows: 90 (info), 60 (warning), 30 (urgent), 15 (critical) days. */
export function generateLeaseAlerts(input: LeaseAlertInput): LeaseAlertResult;
```

---

## 3. Shared Types (`src/types.ts`)

Types reused across multiple modules:

```ts
/** Allocation method for common area charges (water/electric). */
export type AllocationMethod = "FLOOR_AREA" | "EQUAL_SPLIT";

/** Common input for common area allocation (used by both water and electric). */
export interface AllocationInput {
  totalMasterBill: string;
  tenantCharges: { tenantId: number; charge: string }[];
  commonAreaConsumption: number;
  allocationMethod: AllocationMethod;
  tenantFloorAreas?: { tenantId: number; floorAreaSqm: string }[];
  activeTenantCount: number;
}

export interface AllocationResult {
  commonAreaCharge: string;
  perTenantAllocation: { tenantId: number; commonAreaShare: string }[];
  reconciliationDelta: string;
}

/** Charge type codes used across billing, payment, and tax modules. */
export type ChargeTypeCode =
  | "RENT" | "WATER" | "ELECTRIC" | "PENALTY"
  | "DEPOSIT_APPLICATION" | "ADMIN_FEE" | "OTHER";

/** Lease regime — affects computation rules across every module. */
export type LeaseRegime = "CONTROLLED_RESIDENTIAL" | "NON_CONTROLLED_RESIDENTIAL" | "COMMERCIAL";

/** Unit type — determines regime classification. */
export type UnitType = "RESIDENTIAL" | "COMMERCIAL";
```

---

## 4. Integration Pattern: How tRPC Routers Call Computations

The `@tsvj/computations` package is pure — no DB access. tRPC routers bridge the gap:

```
1. tRPC procedure receives validated Zod input
2. Router queries DB via @tsvj/db for required data
3. Router maps Drizzle rows → computation input objects (plain objects with string amounts)
4. Router calls @tsvj/computations function
5. Router maps computation result → Drizzle insert/update
6. Router returns result to client
```

**Example: Rent escalation in the escalation router**

```ts
// apps/web/src/routers/escalation.ts (pseudocode)
import { computeNHSBEscalation, checkThresholdCrossing } from "@tsvj/computations";

export const escalationRouter = router({
  runEscalation: adminProcedure
    .input(z.object({ leaseId: z.number(), nhsbRateId: z.number() }))
    .mutation(async ({ ctx, input }) => {
      // 1. Query DB
      const lease = await ctx.db.query.lease.findFirst({ where: eq(lease.id, input.leaseId) });
      const currentPeriod = await ctx.db.query.recurringChargePeriod.findFirst({ ... });
      const nhsbRate = await ctx.db.query.nhsbCapRate.findFirst({ where: eq(nhsbCapRate.id, input.nhsbRateId) });

      // 2. Call computation
      const result = computeNHSBEscalation({
        currentRent: currentPeriod.amount,          // string from DB
        nhsbCapRate: nhsbRate.capRate,               // string from DB
        leaseAnniversaryDate: lease.dateStart,       // string
        effectiveDate: computeNextAnniversary(lease),
      });

      // 3. Check threshold
      const threshold = checkThresholdCrossing({
        newMonthlyRent: result.newRent,
        unitType: lease.unitType,
        currentRegime: lease.leaseRegime,
      });

      // 4. Write results to DB
      await ctx.db.transaction(async (tx) => {
        await tx.insert(recurringChargePeriod).values({
          recurringChargeId: currentPeriod.recurringChargeId,
          amount: result.newRent,
          effectiveDate: result.effectiveDate,
        });
        await tx.insert(escalationEvent).values({
          leaseId: input.leaseId,
          previousRent: result.previousRent,
          newRent: result.newRent,
          escalationRate: result.escalationRate,
          thresholdCrossed: threshold.crossedThreshold,
        });
        if (threshold.crossedThreshold) {
          await tx.update(lease).set({ leaseRegime: threshold.newRegime }).where(eq(lease.id, input.leaseId));
        }
      });

      return result;
    }),
});
```

**Key boundary:** The computation function never knows about the database. It receives strings, does math, returns strings. The router handles all persistence.

---

## 5. Testing Strategy

### 5.1 Test Organization

```
packages/computations/tests/
├── decimal.test.ts                  # Rounding functions, Peso type
├── escalation/
│   ├── nhsb.test.ts                 # NHSB escalation with known rates
│   ├── contractual.test.ts          # Fixed %, stepped, CPI-linked
│   └── threshold.test.ts            # PHP 10K threshold crossing
├── water/
│   ├── tiered-billing.test.ts       # Per-tier computation with real Maynilad rates
│   └── allocation.test.ts           # Floor area vs. equal split
├── electric/
│   ├── blended-rate.test.ts         # Blended rate with various bill structures
│   └── allocation.test.ts           # Common area allocation
├── penalty/
│   ├── simple-interest.test.ts      # Grace period, daily accrual
│   └── caps.test.ts                 # Monthly and annual caps for controlled
├── billing/
│   ├── vat.test.ts                  # All 8 VAT scenarios from cross-cutting extract
│   └── charge-builder.test.ts       # Charge creation with VAT
├── payment/
│   └── art-1252.test.ts             # Art. 1252 designation, Art. 1253 priority, Art. 1254 FIFO
├── deposit/
│   ├── validation.test.ts           # 2+1 rule, commercial no-cap
│   └── refund.test.ts               # Deduction, interest, tax reclassification
├── contract/
│   └── dst.test.ts                  # DST formula edge cases
├── tax/
│   ├── ewt-rent.test.ts             # 5% EWT on rent, 2% on utilities
│   ├── ewt-supplier.test.ts         # Rate matrix by payee type
│   ├── vat-summary.test.ts          # 2550Q data with apportionment
│   └── apportionment.test.ts        # Mixed-operation input VAT
└── lease/
    ├── state-machine.test.ts        # Valid/invalid transitions
    └── alerts.test.ts               # Alert generation at 90/60/30/15 days
```

### 5.2 Test Patterns

All tests use Vitest. Test structure for each module:

```ts
// tests/escalation/nhsb.test.ts
import { describe, it, expect } from "vitest";
import { computeNHSBEscalation } from "../../src/escalation/nhsb";

describe("NHSB Escalation", () => {
  it("applies 2.3% cap with ROUND_DOWN", () => {
    const result = computeNHSBEscalation({
      currentRent: "10000.00",
      nhsbCapRate: "0.023",
      leaseAnniversaryDate: "2025-03-01",
      effectiveDate: "2026-03-01",
    });
    // 10000 × 1.023 = 10230.00 (ROUND_DOWN to 2 decimals = 10230.00)
    expect(result.newRent).toBe("10230.00");
    expect(result.thresholdCrossed).toBe(true); // > PHP 10,000
  });

  it("ROUND_DOWN truncates, does not round up", () => {
    const result = computeNHSBEscalation({
      currentRent: "8500.00",
      nhsbCapRate: "0.023",
      leaseAnniversaryDate: "2025-03-01",
      effectiveDate: "2026-03-01",
    });
    // 8500 × 1.023 = 8695.50 → ROUND_DOWN = 8695.50 (no truncation needed, exact)
    expect(result.newRent).toBe("8695.50");
    expect(result.thresholdCrossed).toBe(false);
  });

  it("detects threshold crossing at exactly PHP 10,001", () => {
    const result = computeNHSBEscalation({
      currentRent: "9785.00",
      nhsbCapRate: "0.023",
      leaseAnniversaryDate: "2025-03-01",
      effectiveDate: "2026-03-01",
    });
    // 9785 × 1.023 = 10010.055 → ROUND_DOWN = 10010.05
    expect(result.newRent).toBe("10010.05");
    expect(result.thresholdCrossed).toBe(true);
  });

  it("compounding: applies rate to current rent, not original", () => {
    // Year 1: 8000 × 1.023 = 8184
    const year1 = computeNHSBEscalation({
      currentRent: "8000.00",
      nhsbCapRate: "0.023",
      leaseAnniversaryDate: "2024-03-01",
      effectiveDate: "2025-03-01",
    });
    expect(year1.newRent).toBe("8184.00");

    // Year 2: 8184 × 1.01 = 8265.84 (different NHSB rate)
    const year2 = computeNHSBEscalation({
      currentRent: year1.newRent,
      nhsbCapRate: "0.01",
      leaseAnniversaryDate: "2024-03-01",
      effectiveDate: "2026-03-01",
    });
    expect(year2.newRent).toBe("8265.84");
  });
});
```

### 5.3 Test Data Expectations

Key test vectors derived from regulatory rules:

| Module | Test Case | Input | Expected Output |
|--------|-----------|-------|-----------------|
| NHSB escalation | 2.3% cap, PHP 10K rent | rent=10000, rate=0.023 | newRent=10230.00, crossed=true |
| NHSB escalation | 1% cap, PHP 8K rent | rent=8000, rate=0.01 | newRent=8080.00, crossed=false |
| Water tiered | 15 cu.m. consumption | 0-10@11.90, 11-20@18.10 | basic=11.90×10 + 18.10×5 = 209.50 |
| Electric blended | 1000 kWh, PHP 12,000 bill | totalBill=12000, totalKwh=1000 | blendedRate=12.0000 |
| Penalty controlled | PHP 10K rent, 35 days overdue, 5-day grace | unpaid=10000, rate=0.01 | rawPenalty=100.00, cap=100.00 |
| VAT residential | Rent PHP 12,000 | unitType=RESIDENTIAL, rent=12000 | vatRate=0.00, exempt=true |
| VAT commercial | Rent PHP 25,000 | unitType=COMMERCIAL, rent=25000 | vatRate=0.12, exempt=false |
| DST | PHP 15K/month, 2 years | monthlyRent=15000, years=2 | DST = 6 + CEIL((360000-2000)/1000)×2 = PHP 722 |
| Art. 1252 | PHP 50K payment, 3 charges | payment=50000, charges=[...] | penalties first, then oldest |
| Deposit 2+1 | Controlled, 3 months deposit | depositMonths=3, regime=CONTROLLED | isValid=false |
| EWT rent | Corporate, PHP 20K rent | base=20000, corporate=true | ewt=1000.00 (5%) |

### 5.4 Forward Loop Verification Commands

Each feature spec references specific test files:

```bash
# Run all computation tests
pnpm --filter @tsvj/computations test

# Run specific module tests
pnpm --filter @tsvj/computations test -- tests/escalation/
pnpm --filter @tsvj/computations test -- tests/water/
pnpm --filter @tsvj/computations test -- tests/penalty/
pnpm --filter @tsvj/computations test -- tests/billing/vat.test.ts

# TypeScript compilation check
pnpm --filter @tsvj/computations tsc --noEmit
```

---

## 6. Package Configuration

### `packages/computations/package.json`

```json
{
  "name": "@tsvj/computations",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "exports": {
    ".": "./src/index.ts"
  },
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "decimal.js": "^10"
  },
  "devDependencies": {
    "@tsvj/tsconfig": "workspace:*",
    "typescript": "^5.7",
    "vitest": "^3.0"
  }
}
```

### `packages/computations/tsconfig.json`

```json
{
  "extends": "@tsvj/tsconfig/library.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src/**/*.ts"],
  "exclude": ["tests", "dist"]
}
```

### `packages/computations/vitest.config.ts`

```ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    include: ["tests/**/*.test.ts"],
  },
});
```

---

## 7. Decimal Handling End-to-End Flow

```
PostgreSQL numeric(10,2)
    │
    ▼ Drizzle returns string
  "10230.05"
    │
    ▼ tRPC superjson (strings pass through)
  "10230.05"
    │
    ▼ @tsvj/computations: peso("10230.05") → Decimal object
  Decimal { ... }
    │
    ▼ Arithmetic with context-specific rounding
  Decimal { ... }
    │
    ▼ pesoToString(result) → "10455.42"
  "10455.42"
    │
    ▼ tRPC returns string to client
  "10455.42"
    │
    ▼ Client: peso("10455.42") for display math (optional)
    ▼ PesoDisplay component: formatCurrency("10455.42") → "₱10,455.42"
```

**Never at any point does a monetary value pass through JavaScript's `number` type.** The entire pipeline is string → Decimal → string → string.

---

## 8. Boundary: What Does NOT Live in `@tsvj/computations`

| Concern | Where It Lives | Why |
|---------|---------------|-----|
| Database queries | tRPC routers (`apps/web/src/routers/`) | Computations are pure — no DB access |
| Document numbering (atomic increment) | tRPC router + raw SQL (SELECT FOR UPDATE) | Requires database transaction, not a computation |
| Lease state transitions (auto) | pg_cron PL/pgSQL function | Runs in DB for reliability, not in app layer |
| PDF generation | tRPC router (future) | I/O-bound, not computation |
| CSV/XLSX export | Client-side via SheetJS | UI concern, data already computed server-side |
| Alert persistence | tRPC router → alert table | Side effect, not computation |
| Cache invalidation | tRPC router → React Query | UI/API concern |
| Audit logging | tRPC middleware | Cross-cutting concern handled at middleware layer |

The `@tsvj/computations` package is responsible for ONE thing: **deterministic business arithmetic**. Given inputs, produce outputs. Everything else is someone else's job.

---

*Decision made: 2026-03-02 | 10 computation modules, 7 rounding contexts, ~20 primary functions, all pure and synchronous | Forward loop implements alongside feature-specific tRPC routers*
