# Database Schema Design — Drizzle ORM + Supabase Postgres

*Wave 2 Architecture Decision | Depends on: data-model-extract, cross-cutting-extract, project-structure*

---

## Decision Summary

65 entities → **44 Drizzle tables** + **1 materialized view** + **20 pgEnum definitions**, organized across 8 schema files in `packages/db/src/schema/`. Uses `serial` (auto-increment integer) primary keys, `snake_case` table/column naming, PostgreSQL `numeric` for all monetary values, and `timestamp with time zone` for all timestamps. Migrations managed by `drizzle-kit` with a push-based workflow for development and migration-file-based workflow for production. TenantBalance is a PostgreSQL materialized view refreshed on payment/charge events.

---

## 1. Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | `snake_case`, singular noun | `lease`, `water_meter`, `billing_run` |
| Columns | `snake_case` | `date_start`, `lease_regime`, `vat_rate` |
| Enums | `snake_case` with descriptive name | `lease_status`, `unit_type`, `payment_method` |
| Enum values | `SCREAMING_SNAKE_CASE` | `CONTROLLED_RESIDENTIAL`, `MONTH_TO_MONTH` |
| Foreign keys | `<referenced_table>_id` | `tenant_id`, `lease_id`, `water_meter_id` |
| Indexes | `idx_<table>_<columns>` | `idx_charge_lease_id`, `idx_lease_status` |
| Unique constraints | `unq_<table>_<columns>` | `unq_nhsb_cap_rate_year` |
| Check constraints | `chk_<table>_<description>` | `chk_lease_due_day_range` |

**Rationale:** PostgreSQL convention is `snake_case`. Drizzle maps these to camelCase in TypeScript automatically via its column definition API. Singular table names to match Drizzle's convention (the table represents the entity, not the collection).

---

## 2. Primary Key Strategy

**Decision: `serial` (auto-increment integer) for all tables.**

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| UUID v4 | No coordination needed, safe for distributed systems | 16 bytes, poor index locality, slower joins on large tables, hard to debug manually | Rejected |
| UUID v7 | Time-sorted, better index locality than v4 | Still 16 bytes, library dependency, newer standard | Rejected |
| `serial` (int4) | 4 bytes, sequential, excellent index locality, human-readable for debugging | Theoretical exhaustion at ~2.1B rows | **Selected for most tables** |
| `bigserial` (int8) | Same as serial but 8 bytes, no practical exhaustion | Slightly larger than serial | **Selected for high-volume tables** |

**Which tables use `bigserial`:**
- `charge` — central entity, cross-referenced by billing, payments, documents, reports
- `payment_allocation` — one payment can generate many allocations
- `issued_document_line` — many line items per document
- `depreciation_schedule_entry` — monthly entries per asset over years

All other tables use `serial`. At the scale of this system (~100 units, ~100 tenants), even `serial` will never be exhausted, but `bigserial` for high-volume tables is a zero-cost safety margin.

**Drizzle pattern:**
```ts
import { serial, bigserial } from "drizzle-orm/pg-core";

// Standard table
export const tenant = pgTable("tenant", {
  id: serial("id").primaryKey(),
  // ...
});

// High-volume table
export const charge = pgTable("charge", {
  id: bigserial("id", { mode: "number" }).primaryKey(),
  // ...
});
```

---

## 3. Column Type Mapping

### 3.1 Monetary Values

| Drizzle Type | PostgreSQL Type | Usage | JavaScript Representation |
|-------------|----------------|-------|--------------------------|
| `numeric("col", { precision: 10, scale: 2 })` | `numeric(10,2)` | Standard monetary (up to PHP 99,999,999.99) | `string` → parse with `decimal.js` |
| `numeric("col", { precision: 12, scale: 2 })` | `numeric(12,2)` | Aggregate/summary amounts | `string` |
| `numeric("col", { precision: 4, scale: 2 })` | `numeric(4,2)` | Percentage rates (0.12 = 12%) | `string` |
| `numeric("col", { precision: 5, scale: 4 })` | `numeric(5,4)` | Precision rates (0.0230 = 2.3%) | `string` |
| `numeric("col", { precision: 8, scale: 4 })` | `numeric(8,4)` | Per-kWh electric rates | `string` |

**Key rule:** Drizzle returns `numeric` columns as strings. The tRPC router layer (or the computations package) converts strings to `Decimal` objects for arithmetic, then converts back to string for storage. Never use JavaScript `number` for monetary arithmetic.

### 3.2 Temporal Values

| Drizzle Type | PostgreSQL Type | Usage |
|-------------|----------------|-------|
| `date("col")` | `date` | Business dates (lease start/end, billing period, etc.) |
| `timestamp("col", { withTimezone: true })` | `timestamptz` | Audit timestamps (`created_at`, `updated_at`, `finalized_at`) |

**Pattern for audit timestamps:**
```ts
import { timestamp } from "drizzle-orm/pg-core";

const timestamps = {
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow().$onUpdate(() => new Date()),
};
```

Every table that tracks creation/modification includes `...timestamps` via spread. Tables with only creation tracking (audit logs, events) use only `createdAt`.

### 3.3 Text and Boolean

| Drizzle Type | PostgreSQL Type | Usage |
|-------------|----------------|-------|
| `text("col")` | `text` | Variable-length strings (names, addresses, descriptions) |
| `varchar("col", { length: N })` | `varchar(N)` | Fixed-format strings (TIN: 15 chars, ATP number: 30 chars) |
| `boolean("col")` | `boolean` | Flags (`is_corporate`, `is_vat_registered`, `is_active`) |
| `integer("col")` | `integer` | Counts, floor numbers, day-of-month |

### 3.4 JSONB Columns

| Table | Column | JSONB Structure | Purpose |
|-------|--------|----------------|---------|
| `lease` | `escalation_params` | `{ rate?: number, steps?: Array, base_cpi?: number, ... }` | Per-escalation-type config |
| `maynilad_bill` | `bill_components` | `{ basic, env_charge, sewerage, fcda, msc, vat }` | Maynilad bill breakdown |
| `maynilad_rate_schedule` | `tiers` | `[{ min_cu_m, max_cu_m, rate_per_cu_m }]` | Per-tier rate table |
| `meralco_bill` | `bill_components` | `{ generation, transmission, system_loss, ... }` | Meralco bill breakdown |
| `water_charge` | `tier_breakdown` | `[{ tier, cu_m, rate, amount }]` | Per-tier computation audit |
| `lease_event` | `details` | varies by event type | Additional context per event |
| `payment_event` | `details` | varies by event type | Allocation/reversal details |
| `compliance_obligation` | `deadline_rule` | `{ day, relative_to, offset_months? }` | Deadline computation rule |
| `rent_roll_report` | `report_data` | 26-column row array | Snapshot data for export |
| `lis_report` | `report_data` | 9-column row array | Semi-annual LIS data |

**Zod schemas for each JSONB column** are defined in `@tsvj/db` alongside the Drizzle schema and exported for use in tRPC input validation:

```ts
// packages/db/src/schema/billing.ts
import { z } from "zod";

export const escalationParamsSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("NHSB_CAP") }),
  z.object({ type: z.literal("FIXED_PCT"), rate: z.string() }),
  z.object({
    type: z.literal("STEPPED"),
    steps: z.array(z.object({ year: z.number(), rate: z.string() })),
  }),
  z.object({
    type: z.literal("CPI_LINKED"),
    baseCpi: z.string(),
    baseDate: z.string(),
  }),
  z.object({ type: z.literal("NONE") }),
]);
```

---

## 4. Schema File Organization

Maps to the project structure decision. 8 schema files + 1 enums file + 1 relations file:

```
packages/db/src/schema/
├── index.ts          # Re-exports all tables, enums, relations, Zod schemas
├── enums.ts          # All 20 pgEnum definitions
├── foundation.ts     # 7 tables: property, room, rentable, tenant, lease, lease_rentable, charge_type
├── billing.ts        # 14 tables: recurring_charge, recurring_charge_period, nhsb_cap_rate,
│                     #   escalation_event, water_meter, water_meter_tenant, water_meter_reading,
│                     #   maynilad_bill, maynilad_rate_schedule, water_billing_run, water_charge,
│                     #   electric_meter, electric_meter_tenant, electric_meter_reading
├── charges.ts        # 7 tables: meralco_bill, electric_billing_run, electric_charge,
│                     #   penalty_ledger, demand_record, billing_run, charge, credit_memo
├── collection.ts     # 9 tables: payment, payment_allocation, payment_event, security_deposit,
│                     #   deposit_interest_accrual, deposit_deduction, deposit_application,
│                     #   deposit_refund, form_2307_record
├── contracts.ts      # 7 tables: lease_template, lease_clause, board_resolution,
│                     #   lease_execution_milestone, dst_computation, lease_event, non_renewal_notice
├── documents.ts      # 4 tables: document_sequence, authority_to_print, issued_document,
│                     #   issued_document_line
├── expenses.ts       # 5 tables: supplier_payee, expense_category, disbursement_voucher,
│                     #   input_vat_register, ewt_withheld_register
├── reporting.ts      # 8 tables: fixed_asset_register, depreciation_schedule_entry, rent_roll_report,
│                     #   lis_report, output_vat_summary, income_tax_quarterly_data, sawt_record,
│                     #   ewt_withheld_summary, dst_register, compliance_obligation, compliance_deadline
├── system.ts         # 3 tables: app_settings, alert, audit_log
└── relations.ts      # All Drizzle relations() definitions (centralized)
```

**Why centralized relations:** Drizzle's `relations()` API requires all referenced tables to be importable from a single scope. If relations are defined alongside tables, circular imports are inevitable (e.g., `lease` references `charge`, `charge` references `lease`). A single `relations.ts` file that imports all tables avoids this.

**Note on table count:** The data model extract listed 65 entities. Several are consolidated:
- `TenantBalance` → materialized view (not a Drizzle table)
- `TenantStatement` from the extract → not a separate table; generated on-the-fly from charges/payments
- Some entities from the extract map to the same logical table with additional columns
- Final count: **44 tables** + **1 materialized view** + **20 enums**

---

## 5. Enum Definitions

All enums are defined in `packages/db/src/schema/enums.ts` using Drizzle's `pgEnum`:

```ts
import { pgEnum } from "drizzle-orm/pg-core";

// Foundation
export const unitTypeEnum = pgEnum("unit_type", ["RESIDENTIAL", "COMMERCIAL"]);
export const leaseStatusEnum = pgEnum("lease_status", [
  "DRAFT", "ACTIVE", "EXPIRED", "MONTH_TO_MONTH", "HOLDOVER", "TERMINATED", "RENEWED",
]);
export const leaseRegimeEnum = pgEnum("lease_regime", [
  "CONTROLLED_RESIDENTIAL", "NON_CONTROLLED_RESIDENTIAL", "COMMERCIAL",
]);
export const escalationTypeEnum = pgEnum("escalation_type", [
  "NHSB_CAP", "FIXED_PCT", "STEPPED", "CPI_LINKED", "NONE",
]);

// Billing
export const meterTypeEnum = pgEnum("meter_type", ["SUB_METER", "COMMON_AREA", "MASTER"]);
export const billingRunStatusEnum = pgEnum("billing_run_status", ["DRAFT", "FINALIZED"]);
export const billingRunTypeEnum = pgEnum("billing_run_type", ["BATCH", "INDIVIDUAL"]);
export const chargeStatusEnum = pgEnum("charge_status", [
  "DRAFT", "FINALIZED", "PAID", "PARTIALLY_PAID", "CREDITED",
]);
export const vatTreatmentEnum = pgEnum("vat_treatment", ["VATABLE", "EXEMPT", "PENDING"]);

// Collection
export const paymentMethodEnum = pgEnum("payment_method", [
  "CASH", "CHECK", "BANK_TRANSFER", "GCASH", "OTHER",
]);
export const allocationRuleEnum = pgEnum("allocation_rule", [
  "TENANT_DESIGNATED", "ART_1253_PENALTY_FIRST", "ART_1254_MOST_ONEROUS", "FIFO",
]);
export const depositStatusEnum = pgEnum("deposit_status", [
  "HELD", "PARTIALLY_APPLIED", "FULLY_APPLIED", "REFUNDED",
]);
export const paymentEventTypeEnum = pgEnum("payment_event_type", [
  "CREATED", "ALLOCATED", "REVERSED", "BOUNCED",
]);

// Contracts
export const leaseEventTypeEnum = pgEnum("lease_event_type", [
  "CREATED", "ACTIVATED", "EXPIRED", "RENEWED", "RECONDUCTION_STARTED",
  "TERMINATED", "NOTICE_SENT", "ANNIVERSARY",
]);
export const leaseExecMilestoneEnum = pgEnum("lease_exec_milestone", [
  "DRAFT", "SIGNED", "NOTARIZED", "REGISTERED", "DST_FILED",
]);
export const demandMethodEnum = pgEnum("demand_method", ["LETTER", "EMAIL", "PERSONAL"]);

// Documents
export const documentTypeEnum = pgEnum("document_type", ["INVOICE", "RECEIPT", "CREDIT_MEMO"]);

// Expenses
export const payeeTypeEnum = pgEnum("payee_type", ["INDIVIDUAL", "CORPORATE"]);
export const fixedAssetStatusEnum = pgEnum("fixed_asset_status", [
  "ACTIVE", "DISPOSED", "FULLY_DEPRECIATED",
]);

// Reporting / Compliance
export const complianceFrequencyEnum = pgEnum("compliance_frequency", [
  "MONTHLY", "QUARTERLY", "SEMI_ANNUAL", "ANNUAL", "EVENT_DRIVEN",
]);
export const regulatorEnum = pgEnum("regulator", ["BIR", "SEC", "LGU", "OTHER"]);
export const complianceStatusEnum = pgEnum("compliance_status", [
  "UPCOMING", "IN_PROGRESS", "FILED", "OVERDUE",
]);
export const alertLevelEnum = pgEnum("alert_level", ["INFO", "WARNING", "URGENT", "OVERDUE"]);
export const dstEventTypeEnum = pgEnum("dst_event_type", ["NEW_LEASE", "RENEWAL", "EXTENSION"]);
export const refundMethodEnum = pgEnum("refund_method", ["CASH", "CHECK", "BANK_TRANSFER"]);
```

**Note:** 24 enums total (4 more than the data model extract's 20 count — `billing_run_type`, `vat_treatment`, `refund_method`, and `regulator` were implicit in the extract but needed as explicit enums).

---

## 6. Index Strategy

### 6.1 Primary Indexes (automatic on PK)

Every table gets an automatic B-tree index on `id` via the primary key constraint.

### 6.2 Foreign Key Indexes

**Rule: Every foreign key column gets a B-tree index.** PostgreSQL does not auto-index foreign keys (unlike some other databases). Without these, `JOIN` and cascading delete performance degrades.

```ts
// Example from foundation.ts
export const lease = pgTable("lease", {
  id: serial("id").primaryKey(),
  tenantId: integer("tenant_id").notNull().references(() => tenant.id),
  // ...
}, (table) => [
  index("idx_lease_tenant_id").on(table.tenantId),
  index("idx_lease_status").on(table.status),
  index("idx_lease_date_end").on(table.dateEnd),
]);
```

### 6.3 Query-Critical Indexes

These indexes support the most common query patterns. Listed by schema file:

**foundation.ts:**
| Index | Columns | Purpose |
|-------|---------|---------|
| `idx_lease_tenant_id` | `lease.tenant_id` | All tenant-scoped queries |
| `idx_lease_status` | `lease.status` | Portfolio dashboard, daily job filters |
| `idx_lease_date_end` | `lease.date_end` | Expiry detection (daily job) |
| `idx_lease_regime` | `lease.lease_regime` | Regime-filtered queries |
| `idx_rentable_property_id` | `rentable.property_id` | Property-scoped unit lists |
| `idx_rentable_unit_type` | `rentable.unit_type` | Regime-based filtering |
| `idx_tenant_tin` | `tenant.tin` | Unique partial index (WHERE tin IS NOT NULL) |

**charges.ts:**
| Index | Columns | Purpose |
|-------|---------|---------|
| `idx_charge_lease_id` | `charge.lease_id` | Lease detail view (charges tab) |
| `idx_charge_tenant_id` | `charge.tenant_id` | Tenant balance computation |
| `idx_charge_billing_period` | `charge.billing_period` | Monthly billing queries |
| `idx_charge_status` | `charge.status` | Unpaid charge queries |
| `idx_charge_billing_run_id` | `charge.billing_run_id` | Billing run detail |

**collection.ts:**
| Index | Columns | Purpose |
|-------|---------|---------|
| `idx_payment_tenant_id` | `payment.tenant_id` | Tenant payment history |
| `idx_payment_date_issued` | `payment.date_issued` | Date-range payment queries |
| `idx_payment_allocation_payment_id` | `payment_allocation.payment_id` | Payment detail |
| `idx_payment_allocation_charge_id` | `payment_allocation.charge_id` | Charge payment status |
| `idx_form_2307_tenant_quarter` | `form_2307_record.(tenant_id, quarter)` | Quarterly 2307 lookup |

**documents.ts:**
| Index | Columns | Purpose |
|-------|---------|---------|
| `idx_issued_document_number` | `issued_document.document_number` | Unique lookup by doc# |
| `idx_issued_document_tenant_id` | `issued_document.tenant_id` | Per-tenant document list |
| `idx_document_sequence_type_property` | `document_sequence.(document_type, property_id)` | Atomic number assignment |

**contracts.ts:**
| Index | Columns | Purpose |
|-------|---------|---------|
| `idx_lease_event_lease_id` | `lease_event.lease_id` | Lease event history |
| `idx_lease_event_type` | `lease_event.event_type` | Event-type filtering |
| `idx_lease_event_date` | `lease_event.event_date` | Timeline queries |

### 6.4 Composite Indexes

| Index | Columns | Purpose |
|-------|---------|---------|
| `idx_charge_tenant_period` | `charge.(tenant_id, billing_period)` | Tenant monthly billing view |
| `idx_charge_lease_status` | `charge.(lease_id, status)` | Unpaid charges per lease |
| `idx_escalation_event_lease_date` | `escalation_event.(lease_id, event_date)` | Escalation history |
| `idx_water_meter_reading_meter_date` | `water_meter_reading.(water_meter_id, reading_date)` | Consumption calculation (current − previous) |
| `idx_electric_meter_reading_meter_date` | `electric_meter_reading.(electric_meter_id, reading_date)` | Consumption calculation |

### 6.5 Partial Indexes

```sql
-- Only index non-null TINs (many tenants may have NULL TIN initially)
CREATE UNIQUE INDEX idx_tenant_tin_unique ON tenant (tin) WHERE tin IS NOT NULL;

-- Only index unpaid charges (most queries filter for outstanding items)
CREATE INDEX idx_charge_unpaid ON charge (tenant_id, due_date) WHERE status IN ('FINALIZED', 'PARTIALLY_PAID');

-- Active leases (daily job + portfolio dashboard filter)
CREATE INDEX idx_lease_active ON lease (date_end) WHERE status = 'ACTIVE';

-- Expired leases awaiting reconduction check
CREATE INDEX idx_lease_expired ON lease (date_end) WHERE status = 'EXPIRED';
```

In Drizzle, partial indexes are defined via raw SQL in the table's extra config or via migration SQL files.

---

## 7. Constraints

### 7.1 Check Constraints

| Table | Constraint | Expression | Purpose |
|-------|-----------|-----------|---------|
| `lease` | `chk_lease_due_day_range` | `custom_due_day >= 1 AND custom_due_day <= 31` | Valid day-of-month |
| `lease` | `chk_lease_dates` | `date_end > date_start` | End after start |
| `lease` | `chk_deposit_controlled` | `lease_regime != 'CONTROLLED_RESIDENTIAL' OR deposit_months <= 2` | RA 9653 max 2 months deposit |
| `charge` | `chk_charge_amounts` | `base_amount >= 0 AND vat_amount >= 0 AND total_amount >= 0` | No negative charges |
| `charge` | `chk_charge_vat_rate` | `vat_rate IN (0.00, 0.12)` | Only valid PH VAT rates |
| `payment` | `chk_payment_positive` | `amount > 0` | Payments must be positive |
| `security_deposit` | `chk_deposit_positive` | `amount > 0` | Deposits must be positive |
| `water_meter_tenant` | `chk_share_pct` | `share_pct > 0 AND share_pct <= 100` | Valid percentage |
| `electric_meter_tenant` | `chk_share_pct` | `share_pct > 0 AND share_pct <= 100` | Valid percentage |

### 7.2 Unique Constraints

| Table | Columns | Purpose |
|-------|---------|---------|
| `nhsb_cap_rate` | `year` | One rate per year |
| `lease_rentable` | `(lease_id, rentable_id)` | No duplicate lease-unit assignments |
| `lease_execution_milestone` | `(lease_id, milestone)` | One milestone per type per lease |
| `document_sequence` | `(document_type, property_id)` | One sequence per doc type per establishment |
| `authority_to_print` | `atp_number` | ATP numbers are globally unique |
| `issued_document` | `document_number` | Document numbers are globally unique |
| `charge_type` | `code` | Charge type codes unique |
| `compliance_obligation` | `code` | Obligation codes unique |
| `expense_category` | `code` | ATC codes unique |
| `water_meter` | `meter_identifier` | Meter IDs unique |
| `electric_meter` | `meter_identifier` | Meter IDs unique |

### 7.3 Foreign Key Cascade Rules

| Pattern | ON DELETE | ON UPDATE | Applied To |
|---------|-----------|-----------|-----------|
| Core entity → child | `CASCADE` | `CASCADE` | `lease_event.lease_id`, `payment_allocation.payment_id`, `water_charge.water_billing_run_id` |
| Reference/lookup → dependent | `RESTRICT` | `CASCADE` | `charge.charge_type_id`, `lease.tenant_id`, `rentable.property_id` |
| Soft-delete entities | `SET NULL` | — | `charge.billing_run_id` (charges can exist without a billing run) |

**Design rule:** `RESTRICT` is the default. `CASCADE` only where the child entity has no meaning without the parent (e.g., `water_charge` has no meaning without its `water_billing_run`). Never cascade delete from `tenant` or `lease` — those are protected.

---

## 8. TenantBalance Materialized View

The `TenantBalance` from the data model extract is implemented as a **PostgreSQL materialized view** — not a Drizzle table. Drizzle does not natively support materialized views, so this is created via a SQL migration.

### 8.1 View Definition

```sql
CREATE MATERIALIZED VIEW tenant_balance AS
SELECT
  t.id AS tenant_id,
  COALESCE(SUM(c.total_amount) FILTER (WHERE c.status IN ('FINALIZED', 'PAID', 'PARTIALLY_PAID')), 0) AS total_billed,
  COALESCE(SUM(pa.amount), 0) AS total_paid,
  COALESCE(SUM(p.ewt_withheld), 0) AS total_ewt,
  COALESCE(SUM(c.total_amount) FILTER (WHERE c.status IN ('FINALIZED', 'PAID', 'PARTIALLY_PAID')), 0)
    - COALESCE(SUM(pa.amount), 0)
    - COALESCE(SUM(p.ewt_withheld), 0) AS balance,
  MIN(c.due_date) FILTER (WHERE c.status IN ('FINALIZED', 'PARTIALLY_PAID')) AS oldest_unpaid_date,
  COUNT(DISTINCT c.billing_period) FILTER (WHERE c.status IN ('FINALIZED', 'PARTIALLY_PAID')) AS months_in_arrears,
  MAX(p.date_issued) AS last_payment_date,
  NOW() AS last_refreshed
FROM tenant t
LEFT JOIN charge c ON c.tenant_id = t.id
LEFT JOIN payment_allocation pa ON pa.charge_id = c.id
LEFT JOIN payment p ON p.tenant_id = t.id
GROUP BY t.id
WITH DATA;

CREATE UNIQUE INDEX idx_tenant_balance_tenant_id ON tenant_balance (tenant_id);
```

### 8.2 Refresh Strategy

The view is refreshed **concurrently** (non-blocking) at these points:
1. After every payment recording (`payment.create` tRPC mutation)
2. After every billing run finalization (`billingRun.finalize` mutation)
3. After every charge status change (credit memo, reversal)

```ts
// In tRPC router, after payment/charge mutation:
await db.execute(sql`REFRESH MATERIALIZED VIEW CONCURRENTLY tenant_balance`);
```

`CONCURRENTLY` requires the unique index (`idx_tenant_balance_tenant_id`) and allows reads during refresh. For ~100 tenants this refresh takes <100ms.

### 8.3 Drizzle Type Export

Since Drizzle doesn't manage the view, we define a type manually:

```ts
// packages/db/src/schema/views.ts
export type TenantBalance = {
  tenantId: number;
  totalBilled: string;  // numeric → string
  totalPaid: string;
  totalEwt: string;
  balance: string;
  oldestUnpaidDate: string | null;
  monthsInArrears: number;
  lastPaymentDate: string | null;
  lastRefreshed: Date;
};
```

The tRPC router queries this view via raw SQL (`db.execute(sql`SELECT * FROM tenant_balance WHERE tenant_id = ${id}`)`) and maps the result to the typed interface.

---

## 9. Document Sequence Atomicity

The `document_sequence` table handles BIR-mandated gapless sequential numbering. The critical requirement is **atomic increment with overflow check**.

### 9.1 Implementation Pattern

```ts
// In tRPC router (e.g., billingRun.finalize or payment.create)
async function getNextDocumentNumber(
  tx: Transaction,
  documentType: "INVOICE" | "RECEIPT" | "CREDIT_MEMO",
  propertyId: number,
): Promise<{ number: number; formatted: string }> {
  const [seq] = await tx.execute(sql`
    UPDATE document_sequence
    SET current_number = current_number + 1
    WHERE document_type = ${documentType}
      AND property_id = ${propertyId}
      AND current_number < series_end
    RETURNING current_number, prefix, series_end
  `);

  if (!seq) {
    throw new TRPCError({
      code: "PRECONDITION_FAILED",
      message: `ATP exhausted for ${documentType}. Register a new ATP before issuing documents.`,
    });
  }

  const formatted = `${seq.prefix}${String(seq.current_number).padStart(7, "0")}`;
  return { number: seq.current_number, formatted };
}
```

**Key details:**
- `SELECT ... FOR UPDATE` is implicit in `UPDATE ... RETURNING` (row-level lock)
- The `WHERE current_number < series_end` prevents overflow — if the ATP is exhausted, the UPDATE affects 0 rows and `seq` is null
- This runs inside the same transaction as the charge/payment creation, ensuring atomicity
- The tRPC middleware wraps the entire operation in a `db.transaction()`

### 9.2 ATP Utilization Alerts

The `authority_to_print` table tracks utilization percentage. This is a **generated column** in Drizzle:

```ts
// Note: Drizzle doesn't support GENERATED columns natively.
// Implemented as a view column or computed in the query layer.
// The tRPC settings router computes utilization:
//   (current_number - series_start) / (series_end - series_start + 1) * 100
```

The alert system (tRPC `alert` router) checks utilization on each document issuance and creates alerts at 80%, 90%, and 100%.

---

## 10. AppSettings Table

A single-row configuration table for system-wide settings:

```ts
export const appSettings = pgTable("app_settings", {
  id: serial("id").primaryKey(),
  electricVatTreatment: vatTreatmentEnum("electric_vat_treatment").notNull().default("PENDING"),
  defaultWaterAllocationMethod: text("default_water_allocation_method").notNull().default("FLOOR_AREA"),
  defaultElectricAllocationMethod: text("default_electric_allocation_method").notNull().default("FLOOR_AREA"),
  companyName: text("company_name").notNull().default(""),
  companyTin: varchar("company_tin", { length: 15 }),
  companyAddress: text("company_address"),
  ...timestamps,
});
```

Enforced as single-row via a check constraint (`CHECK (id = 1)`) or application-level guard. Seed data creates the initial row on first migration.

---

## 11. Audit Log Table

Lightweight audit trail for admin actions (not for event sourcing — that's what `lease_event`, `payment_event`, etc. handle per-domain):

```ts
export const auditLog = pgTable("audit_log", {
  id: bigserial("id", { mode: "number" }).primaryKey(),
  userId: text("user_id").notNull(),         // Supabase auth.users.id
  action: text("action").notNull(),          // e.g., "lease.create", "payment.record"
  entityType: text("entity_type").notNull(), // e.g., "lease", "charge"
  entityId: integer("entity_id"),            // PK of affected entity
  details: jsonb("details"),                 // Before/after snapshot
  ipAddress: text("ip_address"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index("idx_audit_log_user_id").on(table.userId),
  index("idx_audit_log_entity").on(table.entityType, table.entityId),
  index("idx_audit_log_created_at").on(table.createdAt),
]);
```

---

## 12. Alert Table

Unified alert/notification system for lease lifecycle alerts, compliance deadline alerts, and ATP utilization alerts:

```ts
export const alert = pgTable("alert", {
  id: serial("id").primaryKey(),
  level: alertLevelEnum("level").notNull(),
  category: text("category").notNull(),       // "LEASE_EXPIRY", "COMPLIANCE", "ATP_EXHAUSTION", etc.
  title: text("title").notNull(),
  message: text("message").notNull(),
  entityType: text("entity_type"),            // "lease", "compliance_deadline", "authority_to_print"
  entityId: integer("entity_id"),
  isDismissed: boolean("is_dismissed").notNull().default(false),
  dismissedBy: text("dismissed_by"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index("idx_alert_active").on(table.createdAt).where(sql`is_dismissed = false`),
  index("idx_alert_category").on(table.category),
]);
```

---

## 13. Migration Strategy

### 13.1 Development Workflow

```bash
# Schema change → push directly to dev Supabase instance
pnpm --filter @tsvj/db drizzle-kit push

# Generate migration files for review
pnpm --filter @tsvj/db drizzle-kit generate
```

`drizzle-kit push` applies schema changes directly (no migration files) — fast for local dev.

### 13.2 Production Workflow

```bash
# Generate migration SQL from schema diff
pnpm --filter @tsvj/db drizzle-kit generate

# Review generated SQL in packages/db/drizzle/
# Apply to production
pnpm --filter @tsvj/db drizzle-kit migrate
```

All migration files are committed to git. CI runs `drizzle-kit check` to verify schema consistency.

### 13.3 Seed Data

Seed data is managed in `packages/db/src/seed/`:

| File | Contents | When |
|------|----------|------|
| `charge-types.ts` | 9 ChargeType records (RENT, WATER, ELECTRIC, etc.) | Always — required for system to function |
| `compliance.ts` | ~43 ComplianceObligation records | Always — BIR/SEC/LGU deadlines |
| `expense-categories.ts` | 14+ ExpenseCategory records (ATC codes) | Always — EWT rate lookup |
| `app-settings.ts` | 1 AppSettings row (defaults) | Always — single-row config |
| `dev-data.ts` | Sample tenants, leases, properties, charges | Dev only — `NODE_ENV=development` |

Seed script: `pnpm --filter @tsvj/db db:seed`

### 13.4 drizzle.config.ts

```ts
// packages/db/drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/schema/index.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  verbose: true,
  strict: true,
});
```

The same config is referenced by `apps/web/drizzle.config.ts` (which points to the package).

---

## 14. Supabase Integration

### 14.1 Database Client

```ts
// packages/db/src/client.ts
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "./schema";

export function createDbClient(connectionString: string) {
  const client = postgres(connectionString, {
    max: 10,                    // Connection pool size
    idle_timeout: 20,           // Close idle connections after 20s
    connect_timeout: 10,        // Timeout for new connections
  });
  return drizzle(client, { schema });
}

export type DbClient = ReturnType<typeof createDbClient>;
```

**Driver choice: `postgres` (postgres.js) over `@supabase/supabase-js` for database access.** Supabase's JS client uses their REST API (PostgREST), which doesn't support Drizzle ORM. We use the Supabase connection string with `postgres.js` driver for direct Postgres access. Supabase JS client is used only for auth and storage.

### 14.2 Connection String

```
# Direct connection (for Drizzle/postgres.js)
DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres

# Pooled connection (for serverless environments — Next.js API routes)
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?pgbouncer=true
```

In production, use the **pooled connection** via Supabase's built-in PgBouncer. The `?pgbouncer=true` flag disables prepared statements (required for PgBouncer in transaction mode).

### 14.3 Row-Level Security (RLS)

**Decision: RLS is NOT used for role-based access control.** Instead, role enforcement is handled in the tRPC middleware layer.

**Rationale:**
1. Only 2 roles (Admin, Accountant) — simple enough for middleware
2. Drizzle ORM does not natively support RLS policies (would need raw SQL migrations)
3. The tRPC `adminOnly` middleware is simpler to test and reason about
4. RLS would conflict with the direct `postgres.js` connection (which uses `postgres` role, not per-user roles)
5. For 2 users, the complexity of RLS policies across 44 tables is not justified

**What RLS IS used for:** Supabase Auth's built-in RLS on `auth.users` table (managed by Supabase, not by us).

---

## 15. Soft Delete vs. Hard Delete

**Decision: No soft delete pattern. Entities are either immutable audit records or have explicit status fields.**

| Entity Type | Deletion Strategy |
|-------------|-------------------|
| Audit/event logs (`lease_event`, `payment_event`, `audit_log`) | Never deleted. Immutable. |
| BIR-regulated documents (`charge`, `issued_document`, `credit_memo`) | Never deleted. Status-based lifecycle (DRAFT → FINALIZED → PAID). Cancelled charges are status `CREDITED` with a linked CreditMemo. |
| Configuration (`charge_type`, `lease_template`, `lease_clause`) | `is_active` boolean flag. Deactivated, not deleted. Referenced by historical data. |
| Meters (`water_meter`, `electric_meter`) | `is_active` boolean flag. |
| Master data (`tenant`, `lease`, `property`, `rentable`) | Never deleted. Protected by FK constraints. Tenants with no active leases remain for historical reporting. |
| Draft entities (`billing_run` in DRAFT, `water_billing_run` in DRAFT) | Can be hard-deleted before finalization. After finalization, immutable. |

---

## 16. Schema Validation Rules at DB Level

The Drizzle schema encodes all constraints that can be enforced at the database level. The tRPC layer adds application-level validation via Zod. The split:

| Concern | DB Level (Drizzle) | App Level (Zod/tRPC) |
|---------|-------------------|----------------------|
| Required fields | `.notNull()` | `.min(1)` for strings |
| Type constraints | Column types, enums | Zod schemas |
| Referential integrity | Foreign keys | Checked before insert |
| Business invariants | CHECK constraints | Computation validation |
| Cross-table rules | — | tRPC mutation logic |
| Regime-dependent rules | CHECK where static | tRPC conditional logic |

---

## 17. Forward Loop Schema Verification

The forward loop verifies schema correctness using:

```bash
# Schema consistency check (types match migration state)
pnpm --filter @tsvj/db drizzle-kit check

# TypeScript compilation of schema files
pnpm --filter @tsvj/db tsc --noEmit

# Database integration tests (push to test DB, verify constraints)
pnpm --filter @tsvj/db test
```

Each feature spec (F0, P1, etc.) includes specific schema additions and their verification commands.

---

*Decision made: 2026-03-02 | 44 tables, 1 materialized view, 24 enums, serial PKs, numeric-only monetary, centralized relations, push-based dev migrations, no RLS (middleware-based auth), no soft deletes*
