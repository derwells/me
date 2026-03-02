# API Layer — tRPC Router Organization, Middleware, Error Handling

*Wave 2 Architecture Decision | Depends on: data-model-extract, ui-requirements-extract, cross-cutting-extract, project-structure, database-schema, auth-and-roles*

---

## Decision Summary

tRPC v11 with 21 sub-routers merged into one `appRouter`. Procedures follow a `domain.verb` naming convention (e.g., `tenant.list`, `billingRun.finalize`). Three middleware layers: auth (from auth-and-roles), audit logging (auto-logs all mutations), and database injection. Zod schemas for all inputs and outputs with superjson transformer for Date/Decimal serialization. Cursor-based pagination for all list endpoints. Server-side caller for RSC prefetching via React Query hydration. Database transactions wrap all multi-step mutations. Error handling uses tRPC error codes with structured error metadata.

---

## 1. Router Architecture

### 1.1 Root Router

```ts
// apps/web/src/trpc/router.ts
import { router } from "./init";
import { tenantRouter } from "@/routers/tenant";
import { leaseRouter } from "@/routers/lease";
import { propertyRouter } from "@/routers/property";
import { chargeTypeRouter } from "@/routers/charge-type";
import { escalationRouter } from "@/routers/escalation";
import { waterRouter } from "@/routers/water";
import { electricRouter } from "@/routers/electric";
import { penaltyRouter } from "@/routers/penalty";
import { billingRunRouter } from "@/routers/billing-run";
import { paymentRouter } from "@/routers/payment";
import { depositRouter } from "@/routers/deposit";
import { contractRouter } from "@/routers/contract";
import { renewalRouter } from "@/routers/renewal";
import { portfolioRouter } from "@/routers/portfolio";
import { rentRollRouter } from "@/routers/rent-roll";
import { taxRouter } from "@/routers/tax";
import { documentRouter } from "@/routers/document";
import { expenseRouter } from "@/routers/expense";
import { settingsRouter } from "@/routers/settings";
import { complianceRouter } from "@/routers/compliance";
import { alertRouter } from "@/routers/alert";

export const appRouter = router({
  tenant: tenantRouter,
  lease: leaseRouter,
  property: propertyRouter,
  chargeType: chargeTypeRouter,
  escalation: escalationRouter,
  water: waterRouter,
  electric: electricRouter,
  penalty: penaltyRouter,
  billingRun: billingRunRouter,
  payment: paymentRouter,
  deposit: depositRouter,
  contract: contractRouter,
  renewal: renewalRouter,
  portfolio: portfolioRouter,
  rentRoll: rentRollRouter,
  tax: taxRouter,
  document: documentRouter,
  expense: expenseRouter,
  settings: settingsRouter,
  compliance: complianceRouter,
  alert: alertRouter,
});

export type AppRouter = typeof appRouter;
```

**21 sub-routers** (not 19 as initially estimated — `chargeType` and `alert` were separated out from `settings` for cleaner organization).

### 1.2 Procedure Naming Convention

Every procedure follows `router.verb` pattern. Standard verbs:

| Verb | Method | Purpose | Auth Level |
|------|--------|---------|:----------:|
| `list` | `query` | Paginated list with filters | `protectedProcedure` |
| `getById` | `query` | Single entity by ID | `protectedProcedure` |
| `create` | `mutation` | Create new entity | `adminProcedure` |
| `update` | `mutation` | Update existing entity | `adminProcedure` |
| `delete` | `mutation` | Delete or deactivate entity | `adminProcedure` |
| `export` | `query` | Generate CSV/XLSX data | `protectedProcedure` |

Domain-specific verbs (not every router has all of these):

| Verb | Router(s) | Purpose |
|------|-----------|---------|
| `run` | `escalation`, `water`, `electric`, `penalty` | Execute a computation batch |
| `finalize` | `billingRun`, `water`, `electric` | Lock a draft billing run (immutable after) |
| `allocate` | `payment` | Apply payment to charges (Art. 1252-1254) |
| `generate` | `contract`, `rentRoll`, `document` | Generate a document/report |
| `dismiss` | `alert` | Dismiss an alert (both roles) |
| `getSummary` | `tax`, `portfolio`, `deposit` | Aggregated summary view |
| `getBalance` | `tenant`, `payment` | TenantBalance materialized view query |

### 1.3 Full Procedure Inventory

This maps every tRPC procedure to its router, method type, auth level, and primary database entities:

**Foundation (F0):**

| Procedure | Type | Auth | Description |
|-----------|:----:|:----:|-------------|
| `tenant.list` | query | protected | Paginated tenant list with search, filter by type |
| `tenant.getById` | query | protected | Tenant detail + related leases |
| `tenant.getBalance` | query | protected | TenantBalance materialized view for one tenant |
| `tenant.create` | mutation | admin | Create tenant with TIN validation |
| `tenant.update` | mutation | admin | Update tenant fields |
| `lease.list` | query | protected | Paginated lease list with status/regime filters |
| `lease.getById` | query | protected | Lease detail + charges, payments, events |
| `lease.create` | mutation | admin | Create lease, set regime, create LeaseEvent(CREATED) |
| `lease.update` | mutation | admin | Update lease fields |
| `lease.activate` | mutation | admin | DRAFT→ACTIVE transition, LeaseEvent(ACTIVATED) |
| `lease.terminate` | mutation | admin | →TERMINATED transition, trigger P7 deposit workflow |
| `property.list` | query | protected | Property list |
| `property.getById` | query | protected | Property with rooms and rentables |
| `property.create` | mutation | admin | Create property |
| `property.update` | mutation | admin | Update property |
| `property.createRoom` | mutation | admin | Add room to property |
| `property.createRentable` | mutation | admin | Add rentable to room |
| `chargeType.list` | query | protected | All charge types |
| `chargeType.create` | mutation | admin | Create custom charge type |
| `chargeType.update` | mutation | admin | Update charge type (toggle is_active) |

**Billing (P1-P5):**

| Procedure | Type | Auth | Description |
|-----------|:----:|:----:|-------------|
| `escalation.list` | query | protected | Escalation events by lease |
| `escalation.getNHSBRates` | query | protected | NHSB cap rate table |
| `escalation.run` | mutation | admin | Compute escalation for a lease, create EscalationEvent |
| `escalation.upsertNHSBRate` | mutation | admin | Add/update NHSB cap rate for a year |
| `water.listMeters` | query | protected | Water meters with tenant assignments |
| `water.listReadings` | query | protected | Readings for a meter |
| `water.createReading` | mutation | admin | Record meter reading |
| `water.createMayniladBill` | mutation | admin | Enter Maynilad bill |
| `water.run` | mutation | admin | Compute water charges for a billing period |
| `water.finalize` | mutation | admin | Lock water billing run |
| `electric.listMeters` | query | protected | Electric meters with tenant assignments |
| `electric.listReadings` | query | protected | Readings for a meter |
| `electric.createReading` | mutation | admin | Record meter reading |
| `electric.createMeralcoBill` | mutation | admin | Enter Meralco bill |
| `electric.run` | mutation | admin | Compute electric charges for a billing period |
| `electric.finalize` | mutation | admin | Lock electric billing run |
| `penalty.list` | query | protected | Penalty charges by tenant |
| `penalty.compute` | mutation | admin | Compute penalties for overdue charges |
| `billingRun.list` | query | protected | Billing runs by period |
| `billingRun.getById` | query | protected | Billing run detail with generated charges |
| `billingRun.create` | mutation | admin | Create draft billing run (select tenants, period) |
| `billingRun.finalize` | mutation | admin | Lock billing run, generate invoices, assign doc numbers |
| `billingRun.export` | query | protected | Export billing run data |

**Collection (P6-P7):**

| Procedure | Type | Auth | Description |
|-----------|:----:|:----:|-------------|
| `payment.list` | query | protected | Payment list with date/tenant filters |
| `payment.getById` | query | protected | Payment detail with allocations |
| `payment.create` | mutation | admin | Record payment, compute Art. 1252-1254 allocation |
| `payment.reverse` | mutation | admin | Reverse a payment (creates reversal event) |
| `deposit.list` | query | protected | Security deposits by tenant/status |
| `deposit.getById` | query | protected | Deposit lifecycle detail |
| `deposit.collect` | mutation | admin | Record deposit collection |
| `deposit.apply` | mutation | admin | Apply deposit to charges (deduction) |
| `deposit.refund` | mutation | admin | Initiate deposit refund |
| `deposit.getSummary` | query | protected | Aggregate deposit statistics |

**Contracts (P8-P10):**

| Procedure | Type | Auth | Description |
|-----------|:----:|:----:|-------------|
| `contract.list` | query | protected | Generated contracts |
| `contract.generate` | mutation | admin | Generate contract from template + lease data |
| `contract.listTemplates` | query | protected | Lease templates |
| `contract.createTemplate` | mutation | admin | Create/update lease template |
| `contract.computeDST` | query | protected | DST calculation preview |
| `renewal.list` | query | protected | Leases approaching expiry or in renewal |
| `renewal.renew` | mutation | admin | Create renewal lease, link to parent |
| `renewal.sendNotice` | mutation | admin | Record non-renewal notice |
| `portfolio.getSummary` | query | protected | Portfolio dashboard (counts by status, regime) |
| `portfolio.getExpiryTimeline` | query | protected | Leases by expiry date (timeline view) |
| `portfolio.list` | query | protected | Full lease portfolio list with filters |

**Reporting (P11-P14):**

| Procedure | Type | Auth | Description |
|-----------|:----:|:----:|-------------|
| `rentRoll.generate` | mutation | admin | Generate 26-column rent roll for a period |
| `rentRoll.getById` | query | protected | Rent roll snapshot |
| `rentRoll.export` | query | protected | Export rent roll (CSV/XLSX) |
| `tax.getVATSummary` | query | protected | Quarterly VAT summary (2550Q data) |
| `tax.getEWTSummary` | query | protected | Quarterly EWT summary (1601-EQ data) |
| `tax.getIncomeSummary` | query | protected | Quarterly income tax data |
| `tax.getSAWT` | query | protected | SAWT data from collected 2307s |
| `tax.export` | query | protected | Export tax data compilation |
| `document.listInvoices` | query | protected | Invoice register |
| `document.listReceipts` | query | protected | Receipt register |
| `document.getById` | query | protected | Single document detail |
| `document.export` | query | protected | Export document register |
| `expense.list` | query | protected | Disbursement vouchers |
| `expense.getById` | query | protected | Voucher detail |
| `expense.create` | mutation | admin | Create disbursement voucher with EWT computation |
| `expense.update` | mutation | admin | Update draft voucher |
| `expense.listSuppliers` | query | protected | Supplier/payee list |
| `expense.createSupplier` | mutation | admin | Create supplier |
| `expense.updateSupplier` | mutation | admin | Update supplier |
| `expense.export` | query | protected | Export expense register |

**System:**

| Procedure | Type | Auth | Description |
|-----------|:----:|:----:|-------------|
| `settings.get` | query | admin | Get AppSettings |
| `settings.update` | mutation | admin | Update AppSettings |
| `settings.listUsers` | query | admin | List auth users |
| `settings.createUser` | mutation | admin | Create accountant via Supabase Admin API |
| `settings.resetPassword` | mutation | admin | Reset user password |
| `settings.listATP` | query | admin | Authority to Print records |
| `settings.createATP` | mutation | admin | Register new ATP |
| `compliance.list` | query | protected | Compliance obligations with upcoming deadlines |
| `compliance.getCalendar` | query | protected | Calendar view of deadlines |
| `compliance.updateStatus` | mutation | admin | Mark obligation as filed |
| `alert.list` | query | protected | Active (undismissed) alerts |
| `alert.dismiss` | mutation | protected | Dismiss an alert (both roles) |

---

## 2. tRPC Initialization

### 2.1 `initTRPC` Setup

```ts
// apps/web/src/trpc/init.ts
import { initTRPC } from "@trpc/server";
import superjson from "superjson";
import type { TRPCContext } from "./context";

const t = initTRPC.context<TRPCContext>().create({
  transformer: superjson,
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    };
  },
});

export const router = t.router;
export const publicProcedure = t.procedure;
export const middleware = t.middleware;
export const mergeRouters = t.mergeRouters;
```

**Why superjson:** tRPC serializes data as JSON over HTTP. JavaScript `Date` objects, `Decimal` instances, and `BigInt` are not JSON-serializable. superjson handles this transparently:
- `Date` ↔ ISO string (automatic round-trip)
- `Decimal` must be serialized as string before passing to tRPC (superjson doesn't handle decimal.js natively — the router converts `Decimal` → `string` and the client parses `string` → `Decimal` when needed)

### 2.2 Request Context

```ts
// apps/web/src/trpc/context.ts
import { createSupabaseServerClient } from "@/lib/supabase/server";
import { createDbClient } from "@tsvj/db";
import type { AppRole } from "@tsvj/db";

const db = createDbClient(process.env.DATABASE_URL!);

export async function createTRPCContext() {
  const supabase = await createSupabaseServerClient();
  const { data: { user } } = await supabase.auth.getUser();

  return {
    db,
    supabase,
    user,
    role: (user?.app_metadata?.role as AppRole) ?? null,
  };
}

export type TRPCContext = Awaited<ReturnType<typeof createTRPCContext>>;
```

**Key detail:** The database client (`db`) is a module-level singleton — created once and reused across requests. The postgres.js connection pool handles concurrency. The Supabase client is per-request because it reads cookies from the request context.

---

## 3. Middleware Stack

### 3.1 Middleware Layers (in execution order)

```
Request → tRPC handler
  → 1. Auth middleware (authed / adminOnly)  [from auth-and-roles decision]
  → 2. Audit logging middleware (mutations only)
  → 3. Procedure handler (business logic)
  → Response
```

### 3.2 Auth Middleware

Already defined in the auth-and-roles decision. Three procedure builders:

```ts
export const publicProcedure = t.procedure;          // No auth (login only)
export const protectedProcedure = t.procedure.use(authed);    // Any role
export const adminProcedure = t.procedure.use(adminOnly);     // Admin only
```

### 3.3 Audit Logging Middleware

Auto-logs all mutations to the `audit_log` table. Applied at the router level, not globally — only mutations need logging.

```ts
// apps/web/src/trpc/middleware.ts (addition)
export const withAuditLog = middleware(async ({ ctx, next, path, type }) => {
  const result = await next();

  // Only log mutations, only if user is authenticated
  if (type === "mutation" && ctx.user) {
    // Fire-and-forget — don't block the response
    ctx.db.insert(auditLog).values({
      userId: ctx.user.id,
      action: path,            // e.g., "tenant.create"
      entityType: path.split(".")[0],  // e.g., "tenant"
      entityId: null,          // Overridden by individual procedures if needed
      createdAt: new Date(),
    }).catch(() => {});        // Swallow audit log failures (non-critical)
  }

  return result;
});
```

**Design choice: fire-and-forget.** Audit logging must not fail a business operation. If the audit insert fails (connection issue, etc.), the mutation still succeeds. For a 2-user backoffice this is acceptable. The domain-specific event tables (`lease_event`, `payment_event`) serve as the authoritative audit trail for regulated operations — the `audit_log` table is supplementary.

**Enrichment:** Individual mutation handlers can enrich the audit log with `entityId` and `details` by writing directly to the audit log after the main operation, using the same transaction.

### 3.4 Admin Procedure with Audit Log

The standard admin procedure is composed as:

```ts
export const adminProcedure = t.procedure.use(adminOnly).use(withAuditLog);
```

This means every admin mutation is automatically logged. Protected procedures (queries) are not logged — read access doesn't need audit tracking for this use case.

---

## 4. Input/Output Patterns

### 4.1 Zod Input Schemas

Every procedure input is validated via Zod. Schema organization:

```
apps/web/src/routers/
├── tenant.ts            # Router + inline Zod schemas
├── lease.ts
├── ...
```

Zod schemas are defined inline in each router file (not in a separate schemas directory). For schemas shared between multiple routers (e.g., pagination), a shared file exists:

```ts
// apps/web/src/trpc/schemas.ts
import { z } from "zod";

// Shared pagination input
export const paginationInput = z.object({
  cursor: z.number().optional(),       // ID of last item (cursor-based)
  limit: z.number().min(1).max(100).default(25),
});

// Shared date range filter
export const dateRangeInput = z.object({
  from: z.date().optional(),
  to: z.date().optional(),
});

// Shared sort input
export const sortInput = z.object({
  field: z.string(),
  direction: z.enum(["asc", "desc"]).default("desc"),
});
```

**Example: Tenant router inputs:**

```ts
// apps/web/src/routers/tenant.ts
const tenantListInput = z.object({
  ...paginationInput.shape,
  search: z.string().optional(),        // Name or TIN search
  isCorporate: z.boolean().optional(),  // Filter by type
  hasActiveLease: z.boolean().optional(),
});

const tenantCreateInput = z.object({
  name: z.string().min(1).max(255),
  tin: z.string().regex(/^\d{3}-\d{3}-\d{3}-\d{3}$/).optional(),
  isCorporate: z.boolean(),
  isVatRegistered: z.boolean(),
  contactEmail: z.string().email().optional(),
  contactPhone: z.string().optional(),
  address: z.string().optional(),
});

const tenantUpdateInput = z.object({
  id: z.number(),
  ...tenantCreateInput.partial().shape,  // All fields optional for update
});
```

### 4.2 Output Structure

Query outputs follow a consistent structure:

**List queries:**
```ts
type ListOutput<T> = {
  items: T[];
  nextCursor: number | null;  // null = no more pages
  totalCount: number;         // Total matching items (for UI "showing X of Y")
};
```

**Get queries:**
```ts
// Direct entity return with related data
type TenantDetail = {
  id: number;
  name: string;
  tin: string | null;
  isCorporate: boolean;
  isVatRegistered: boolean;
  // ... fields
  leases: Array<{ id: number; status: string; dateStart: string; dateEnd: string }>;
  balance: TenantBalance | null;
};
```

**Mutation outputs:**
```ts
// Return the created/updated entity
type MutationOutput<T> = T;  // Just the entity — no wrapper
```

### 4.3 Cursor-Based Pagination

All list endpoints use cursor-based pagination (not offset-based). The cursor is the `id` of the last item on the current page.

```ts
// Generic list implementation pattern
async function listWithCursor<T>(
  db: DbClient,
  table: PgTable,
  input: { cursor?: number; limit: number; /* filters */ },
) {
  const items = await db
    .select()
    .from(table)
    .where(
      input.cursor
        ? gt(table.id, input.cursor)
        : undefined,
    )
    .orderBy(asc(table.id))
    .limit(input.limit + 1);  // Fetch one extra to detect next page

  const hasMore = items.length > input.limit;
  if (hasMore) items.pop();

  return {
    items,
    nextCursor: hasMore ? items[items.length - 1].id : null,
    totalCount: await db.select({ count: count() }).from(table),
  };
}
```

**Why cursor-based over offset-based:**
1. Stable pagination — inserting/deleting rows doesn't shift pages
2. Better performance on large tables (no `OFFSET N` scan)
3. Natural fit for "load more" patterns
4. The `id` cursor is always available (serial PK, monotonically increasing)

**Exception:** Some admin views (e.g., NHSB cap rate table, charge type list, supplier list) are small enough that the full list is returned without pagination. These use `limit: 500` or no pagination input.

### 4.4 Filtering and Search

List endpoints accept filter parameters specific to each entity:

```ts
// Example: lease.list
const leaseListInput = z.object({
  ...paginationInput.shape,
  status: z.enum(["DRAFT", "ACTIVE", "EXPIRED", "MONTH_TO_MONTH", "HOLDOVER", "TERMINATED", "RENEWED"]).optional(),
  leaseRegime: z.enum(["CONTROLLED_RESIDENTIAL", "NON_CONTROLLED_RESIDENTIAL", "COMMERCIAL"]).optional(),
  tenantId: z.number().optional(),
  propertyId: z.number().optional(),
  expiringWithinDays: z.number().optional(),  // For portfolio dashboard filter
});
```

Text search (tenant name, TIN) uses PostgreSQL `ILIKE` for simplicity — full-text search is overkill for ~100 tenants.

```ts
// In query
.where(
  input.search
    ? or(
        ilike(tenant.name, `%${input.search}%`),
        ilike(tenant.tin, `%${input.search}%`),
      )
    : undefined,
)
```

### 4.5 Monetary Value Serialization

All monetary values are stored as PostgreSQL `numeric` and returned from Drizzle as strings. The tRPC layer passes them through as strings. The client-side is responsible for display formatting and any arithmetic (using `decimal.js`).

```
DB (numeric) → Drizzle (string) → tRPC (string via superjson) → Client (string → Decimal for math, format for display)
```

This avoids floating-point precision issues at every layer. The `@tsvj/ui` `PesoDisplay` component handles formatting: `₱12,345.67`.

---

## 5. Transaction Patterns

### 5.1 When to Use Transactions

**Always use a database transaction when a mutation:**
1. Writes to multiple tables
2. Reads data that informs what it writes (read-then-write)
3. Must be atomic (all-or-nothing)

**In practice, most mutations use transactions.** The exceptions are simple single-table inserts (e.g., `escalation.upsertNHSBRate`).

### 5.2 Transaction Pattern

```ts
// apps/web/src/routers/payment.ts — example of transactional mutation
export const paymentRouter = router({
  create: adminProcedure
    .input(paymentCreateInput)
    .mutation(async ({ ctx, input }) => {
      return await ctx.db.transaction(async (tx) => {
        // 1. Insert payment
        const [newPayment] = await tx.insert(payment).values({
          tenantId: input.tenantId,
          amount: input.amount,
          paymentMethod: input.paymentMethod,
          referenceNumber: input.referenceNumber,
          dateIssued: input.dateIssued,
        }).returning();

        // 2. Compute allocation (Art. 1252-1254)
        const unpaidCharges = await tx
          .select()
          .from(charge)
          .where(and(
            eq(charge.tenantId, input.tenantId),
            inArray(charge.status, ["FINALIZED", "PARTIALLY_PAID"]),
          ))
          .orderBy(asc(charge.dueDate));

        const allocations = allocatePayment(
          input.amount,
          unpaidCharges,
          input.allocationRule,
        );

        // 3. Insert allocations
        await tx.insert(paymentAllocation).values(
          allocations.map(a => ({
            paymentId: newPayment.id,
            chargeId: a.chargeId,
            amount: a.amount,
          })),
        );

        // 4. Update charge statuses
        for (const a of allocations) {
          const remaining = /* compute remaining balance */;
          await tx.update(charge)
            .set({ status: remaining === "0.00" ? "PAID" : "PARTIALLY_PAID" })
            .where(eq(charge.id, a.chargeId));
        }

        // 5. Generate receipt (assign document number atomically)
        if (input.generateReceipt) {
          const docNum = await getNextDocumentNumber(tx, "RECEIPT", input.propertyId);
          await tx.insert(issuedDocument).values({
            documentType: "RECEIPT",
            documentNumber: docNum.formatted,
            tenantId: input.tenantId,
            paymentId: newPayment.id,
            // ...
          });
        }

        // 6. Refresh materialized view
        await tx.execute(sql`REFRESH MATERIALIZED VIEW CONCURRENTLY tenant_balance`);

        // 7. Log payment event
        await tx.insert(paymentEvent).values({
          paymentId: newPayment.id,
          eventType: "CREATED",
          details: { allocations },
        });

        return newPayment;
      });
    }),
});
```

### 5.3 Transaction Isolation Level

Default PostgreSQL isolation level (`READ COMMITTED`) is used. For the atomic document sequence increment (§9 of database-schema), the `UPDATE ... RETURNING` pattern with row-level lock is sufficient — no need for `SERIALIZABLE` isolation.

### 5.4 Long-Running Mutations

Some operations process many entities (e.g., `billingRun.create` generates charges for all tenants in a billing period). These use a single transaction but may take several seconds.

**Pattern:** The mutation returns immediately with a `billingRun` entity in `DRAFT` status. The charges are created within the same transaction. If the transaction fails, the entire billing run is rolled back. There is no background job queue — the transaction completes synchronously.

**Rationale:** With ~100 tenants and ~5 charge types each, a billing run creates ~500 charges. This takes <2 seconds in PostgreSQL. A job queue adds complexity without benefit at this scale.

---

## 6. Error Handling

### 6.1 tRPC Error Codes Used

| Error Code | When Used |
|------------|-----------|
| `UNAUTHORIZED` | No session / invalid JWT |
| `FORBIDDEN` | Accountant attempting admin-only operation |
| `NOT_FOUND` | Entity not found by ID |
| `BAD_REQUEST` | Input validation passes Zod but fails business rule (e.g., deposit exceeds 2-month cap for controlled lease) |
| `PRECONDITION_FAILED` | Operation cannot proceed (e.g., ATP exhausted, billing run already finalized) |
| `CONFLICT` | Unique constraint violation (e.g., duplicate TIN, duplicate meter reading for same date) |
| `INTERNAL_SERVER_ERROR` | Unexpected error (DB connection failure, etc.) |

### 6.2 Business Rule Errors

Business rule violations (not caught by Zod) throw `TRPCError` with structured metadata:

```ts
throw new TRPCError({
  code: "BAD_REQUEST",
  message: "Deposit exceeds maximum for controlled residential lease (max 2 months)",
  cause: {
    rule: "RA_9653_DEPOSIT_CAP",
    field: "depositMonths",
    max: 2,
    actual: input.depositMonths,
  },
});
```

### 6.3 Zod Validation Errors

tRPC automatically catches Zod validation errors from `.input()` and returns them as `BAD_REQUEST` with the flattened Zod error in `shape.data.zodError` (configured in `init.ts` errorFormatter). The client accesses field-level errors:

```ts
// Client-side error handling
const { error } = trpc.tenant.create.useMutation();
if (error?.data?.zodError?.fieldErrors) {
  // { name: ["Required"], tin: ["Invalid format"] }
}
```

### 6.4 Client-Side Error Handling

tRPC + React Query surfaces errors via the standard `error` property on query/mutation results:

```tsx
const createTenant = trpc.tenant.create.useMutation({
  onError(error) {
    if (error.data?.code === "CONFLICT") {
      toast.error("A tenant with this TIN already exists");
    } else if (error.data?.zodError) {
      // Form field errors — handled by react-hook-form integration
    } else {
      toast.error(error.message);
    }
  },
  onSuccess(data) {
    toast.success("Tenant created");
    router.push(`/tenants/${data.id}`);
  },
});
```

### 6.5 Global Error Boundary

A React error boundary wraps the app to catch unhandled errors. tRPC query errors are caught by React Query's built-in error handling — no global error boundary needed for API errors.

---

## 7. Server-Side Rendering Integration

### 7.1 RSC Prefetching with tRPC

Server Components can prefetch tRPC queries so the page renders with data already loaded (no loading spinner). This uses tRPC v11's server-side caller:

```ts
// apps/web/src/trpc/server.ts
import { createTRPCContext } from "./context";
import { appRouter } from "./router";
import { createCallerFactory } from "@trpc/server";

const createCaller = createCallerFactory(appRouter);

export async function createServerCaller() {
  const ctx = await createTRPCContext();
  return createCaller(ctx);
}
```

**Usage in a Server Component page:**

```tsx
// apps/web/src/app/(app)/tenants/page.tsx
import { createServerCaller } from "@/trpc/server";
import { HydrateClient, trpc } from "@/trpc/client";

export default async function TenantsPage() {
  const caller = await createServerCaller();
  // Prefetch the data server-side
  void caller.tenant.list({ limit: 25 });

  return (
    <HydrateClient>
      <TenantListClient />
    </HydrateClient>
  );
}
```

The prefetched data is serialized into the page HTML. The client component picks it up via React Query hydration — no duplicate fetch.

### 7.2 tRPC HTTP Handler

```ts
// apps/web/src/app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "@/trpc/router";
import { createTRPCContext } from "@/trpc/context";

const handler = (request: Request) =>
  fetchRequestHandler({
    endpoint: "/api/trpc",
    req: request,
    router: appRouter,
    createContext: createTRPCContext,
  });

export { handler as GET, handler as POST };
```

### 7.3 Client-Side tRPC Provider

```tsx
// apps/web/src/trpc/client.tsx
"use client";

import { createTRPCClient, httpBatchLink } from "@trpc/client";
import { createTRPCReact } from "@trpc/tanstack-react-query";
import superjson from "superjson";
import type { AppRouter } from "./router";

export const trpc = createTRPCReact<AppRouter>();

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,          // 30s stale time (data refreshes aren't urgent for backoffice)
        refetchOnWindowFocus: false, // Backoffice — no need for aggressive refetching
      },
    },
  }));

  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: "/api/trpc",
          transformer: superjson,
        }),
      ],
    }),
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  );
}
```

**`staleTime: 30_000` (30 seconds):** For a 2-user backoffice, data doesn't change frequently. A 30-second stale time reduces unnecessary refetches. Mutations explicitly invalidate relevant query keys (see §8).

---

## 8. Cache Invalidation

### 8.1 Pattern: Invalidate After Mutation

Every mutation that modifies data explicitly invalidates the affected query keys:

```ts
// Client-side: using tRPC's React Query utils
const utils = trpc.useUtils();

const createTenant = trpc.tenant.create.useMutation({
  onSuccess() {
    utils.tenant.list.invalidate();      // Refetch tenant list
    utils.tenant.getById.invalidate();   // Refetch all tenant details
  },
});
```

### 8.2 Cross-Router Invalidation Map

Some mutations affect data across multiple routers:

| Mutation | Invalidates |
|----------|-------------|
| `payment.create` | `payment.list`, `tenant.getBalance`, `charge.list` (status changes), `portfolio.getSummary` |
| `billingRun.finalize` | `billingRun.list`, `billingRun.getById`, `charge.list`, `tenant.getBalance`, `document.listInvoices` |
| `lease.activate` | `lease.list`, `lease.getById`, `portfolio.getSummary`, `portfolio.list` |
| `escalation.run` | `escalation.list`, `lease.getById` (rent amount changes) |
| `deposit.apply` | `deposit.getById`, `tenant.getBalance`, `charge.list` |
| `water.finalize` / `electric.finalize` | Water/electric lists + `billingRun.list`, `charge.list` |

The client-side mutation hooks include all necessary invalidations. This is documented in each feature spec's implementation details.

---

## 9. Export Endpoints

### 9.1 CSV/XLSX Export Pattern

Export endpoints are tRPC queries that return structured data. The client-side converts to CSV/XLSX using a browser library:

```ts
// Server: export query returns raw data
rentRoll.export: protectedProcedure
  .input(z.object({ reportId: z.number() }))
  .query(async ({ ctx, input }) => {
    const report = await ctx.db.query.rentRollReport.findFirst({
      where: eq(rentRollReport.id, input.reportId),
    });
    return {
      columns: RENT_ROLL_COLUMNS,  // 26 column definitions
      rows: report.reportData,     // Array of row data
      filename: `rent-roll-${report.period}.xlsx`,
    };
  }),
```

```tsx
// Client: convert to file and trigger download
import { utils, writeFile } from "xlsx";  // SheetJS

function ExportButton({ reportId }: { reportId: number }) {
  const { data, refetch } = trpc.rentRoll.export.useQuery(
    { reportId },
    { enabled: false },  // Only fetch on click
  );

  async function handleExport() {
    const result = await refetch();
    if (result.data) {
      const ws = utils.json_to_sheet(result.data.rows);
      const wb = utils.book_new();
      utils.book_append_sheet(wb, ws, "Rent Roll");
      writeFile(wb, result.data.filename);
    }
  }

  return <Button onClick={handleExport}>Export XLSX</Button>;
}
```

**Why client-side file generation over server-side:**
1. Avoids file storage/cleanup on the server
2. The data is already fetched via tRPC — just format it client-side
3. SheetJS (`xlsx`) runs in the browser and supports both CSV and XLSX
4. For ~100 rows × 26 columns, client-side generation is instantaneous

### 9.2 Export Library

**SheetJS (`xlsx`)** — selected for XLSX generation. Adds ~300KB to the client bundle, but it's only loaded on export pages (dynamic import).

```ts
// Dynamic import to avoid bundling on non-export pages
const handleExport = async () => {
  const XLSX = await import("xlsx");
  // ... generate file
};
```

---

## 10. Daily Scheduled Job

### 10.1 Lease Lifecycle Cron

A daily scheduled job runs the lease lifecycle state machine (from cross-cutting-extract §5.4). Implementation options:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Supabase Edge Function + pg_cron | Runs in Supabase, no external infra | Edge functions have 150s timeout, pg_cron setup required | **Selected** |
| Vercel Cron + API route | Integrates with Vercel deployment | Requires Vercel Pro plan for <1h intervals; external trigger | Alternative |
| GitHub Actions cron | Free, already in use | 5-minute minimum interval (fine for daily); external to app | Fallback |

**Selected: Supabase pg_cron triggering a database function.**

The job runs at 00:05 UTC+8 (Manila time) daily:

```sql
-- Runs inside Supabase, no HTTP call needed
SELECT cron.schedule(
  'lease-lifecycle-check',
  '5 0 * * *',  -- Daily at 00:05 Manila (adjust for UTC offset)
  $$SELECT process_lease_lifecycle()$$
);
```

The `process_lease_lifecycle()` function is a PostgreSQL function that:
1. Moves ACTIVE leases past `date_end` → EXPIRED
2. Moves EXPIRED leases past 15 days → MONTH_TO_MONTH (tacit reconduction)
3. Creates `lease_event` records for each transition
4. Creates `alert` records for leases approaching expiry (90/60/30/15 days)
5. Creates ANNIVERSARY events where applicable

**Why a PL/pgSQL function instead of a tRPC endpoint:** The lifecycle check is a pure data operation (read leases, compare dates, update statuses, insert events). Running it inside the database avoids the HTTP round-trip and application layer overhead. It also runs even if the Next.js app is down.

### 10.2 Compliance Deadline Alerts

Same pattern — a daily pg_cron job checks `compliance_deadline` for upcoming deadlines and creates `alert` records at 30/15/5 days before.

### 10.3 Manual Trigger

Both jobs can also be triggered manually via admin-only tRPC mutations (for testing and catch-up):

```ts
settings.runLifecycleCheck: adminProcedure
  .mutation(async ({ ctx }) => {
    await ctx.db.execute(sql`SELECT process_lease_lifecycle()`);
    return { success: true };
  }),
```

---

## 11. API Route Handler Configuration

### 11.1 Batch Link Configuration

tRPC's `httpBatchLink` batches multiple concurrent queries into a single HTTP request. Configuration:

```ts
httpBatchLink({
  url: "/api/trpc",
  transformer: superjson,
  maxURLLength: 2083,  // Batch via POST when URL exceeds IE limit
})
```

For this backoffice app, page loads typically trigger 2-4 concurrent queries (list data + balance + alerts). Batching reduces these to a single HTTP request.

### 11.2 Request/Response Size

No custom size limits needed. The largest response is the rent roll export (~100 rows × 26 columns ≈ 50KB JSON). Well within default limits.

---

## 12. Forward Loop Implications

### 12.1 F0 Must Set Up

1. `apps/web/src/trpc/init.ts` — tRPC initialization with superjson, error formatter
2. `apps/web/src/trpc/context.ts` — Request context with db + supabase + user
3. `apps/web/src/trpc/middleware.ts` — Auth middleware + audit logging
4. `apps/web/src/trpc/router.ts` — Root router (initially with just F0 sub-routers)
5. `apps/web/src/trpc/schemas.ts` — Shared pagination/filter schemas
6. `apps/web/src/trpc/server.ts` — Server-side caller for RSC
7. `apps/web/src/trpc/client.tsx` — Client provider with React Query
8. `apps/web/src/app/api/trpc/[trpc]/route.ts` — HTTP handler
9. Four initial sub-routers: `tenant`, `lease`, `property`, `chargeType`

### 12.2 Each Feature Must

- Define all Zod input schemas inline in the router file
- Use cursor-based pagination for list endpoints
- Wrap multi-table mutations in `ctx.db.transaction()`
- Include cross-router cache invalidation in the client mutation hooks
- Return monetary values as strings (never convert to JavaScript `number`)
- Use `protectedProcedure` for queries and `adminProcedure` for mutations (per role-procedure mapping)

### 12.3 Verification Per Feature

Each feature spec must verify:
- `pnpm run build` — TypeScript compiles (catches input/output type mismatches)
- `pnpm run test -- apps/web/tests/routers/<router>.test.ts` — Router integration tests pass
- `pnpm run lint` — No lint errors

---

*Decision made: 2026-03-02 | 21 sub-routers, ~90 procedures, cursor-based pagination, superjson serialization, transaction-wrapped mutations, fire-and-forget audit logging, RSC prefetching via server caller, client-side export generation, pg_cron daily lifecycle job*
