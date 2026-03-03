# TSVJ Backoffice Web App — Architecture Specification

*Compiled from Wave 2 architecture decisions. Each section references the detailed analysis file in `analysis/` for the full rationale, code samples, and trade-off evaluation.*

---

## 1. Overview

A backoffice web application for a Philippine TSVJ (condominium corporation) property management operation. Automates 14 business processes — from tenant/lease management through billing, payments, tax compliance, and document generation — serving ~50 rental units across commercial and residential regimes.

**Users:** Two roles — Admin (property manager, full CRUD) and Accountant (read-only views + exports).

**Scale:** ~2 concurrent users, ~100 tenants, ~50 active leases, <500 documents/month.

---

## 2. Stack Decisions

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| **Framework** | Next.js (App Router) | ^16.1 | Server Components + Turbopack default, native Vercel hosting |
| **API** | tRPC | ^11.10 | End-to-end type safety, server-side caller for RSC prefetch |
| **Database** | PostgreSQL (Supabase) | 15 | Managed Postgres with Auth, pg_cron, Edge Functions |
| **ORM** | Drizzle ORM | ^0.45 | Type-safe queries, migration tooling, PostgreSQL-native features |
| **Validation** | Zod | ^3.24 | Shared input validation between tRPC + react-hook-form |
| **Auth** | Supabase Auth | @supabase/ssr | Email/password, cookie-based sessions, JWT role claims |
| **UI Components** | shadcn/ui (Radix unified) | latest | Composable primitives, Tailwind styling, zero runtime |
| **Styling** | Tailwind CSS | ^4 | CSS-based theme config, utility-first |
| **Data Fetching** | React Query (@trpc/tanstack-react-query) | ^5 | Cache, invalidation, RSC hydration |
| **State (URL)** | nuqs | latest | URL query params for filters, bookmarkable/shareable |
| **State (Forms)** | react-hook-form + @hookform/resolvers | latest | Zod resolver, uncontrolled inputs |
| **Tables** | TanStack Table | ^8 | Headless, sorting, filtering, cursor pagination |
| **Decimal Math** | decimal.js | ^10 | 7 rounding modes needed (ROUND_DOWN for NHSB, HALF_UP for VAT, etc.) |
| **Serialization** | superjson | ^2 | Date/Decimal transport over tRPC |
| **PDF** | @react-pdf/renderer | ^4 | Server-side PDF, no Chromium dependency |
| **Spreadsheets** | SheetJS (xlsx) | 0.20.3 (CDN) | Client-side XLSX/CSV, dynamic import |
| **Email** | Resend | — | Transactional email via Supabase Edge Function |
| **Monorepo** | Turborepo | ^2.8 | Build orchestration, caching |
| **Package Manager** | pnpm | ^9 | Workspace protocol, fast |
| **Testing** | Vitest | ^3 | Fast, ESM-native, works with Turborepo |
| **Hosting** | Vercel | Free/Pro | Native Next.js host, serverless, preview deploys |

*Full rationale: `analysis/project-structure.md`*

---

## 3. Project Structure

```
tsvj-backoffice/
├── turbo.json
├── package.json
├── pnpm-workspace.yaml
├── .env.example
│
├── apps/
│   └── web/                          # Next.js 16 (frontend + tRPC API)
│       ├── src/
│       │   ├── app/
│       │   │   ├── (app)/            # Authenticated routes (sidebar layout)
│       │   │   │   ├── dashboard/
│       │   │   │   ├── tenants/
│       │   │   │   ├── leases/
│       │   │   │   ├── billing/
│       │   │   │   ├── payments/
│       │   │   │   ├── documents/
│       │   │   │   ├── reports/
│       │   │   │   ├── renewals/
│       │   │   │   ├── expenses/
│       │   │   │   ├── alerts/
│       │   │   │   └── settings/
│       │   │   ├── (auth)/           # Login page
│       │   │   ├── api/
│       │   │   │   ├── trpc/[trpc]/  # tRPC HTTP handler
│       │   │   │   ├── pdf/          # PDF generation routes
│       │   │   │   └── health/       # Health check
│       │   │   ├── layout.tsx        # Root layout (Providers)
│       │   │   └── middleware.ts     # Auth redirect
│       │   ├── components/
│       │   │   ├── layout/           # App shell (sidebar, header, alert-bell)
│       │   │   ├── tenants/          # Tenant-specific components
│       │   │   ├── leases/           # Lease-specific components
│       │   │   ├── billing/          # Billing components
│       │   │   ├── payments/         # Payment components
│       │   │   ├── documents/        # Document/invoice components
│       │   │   ├── reports/          # Report components
│       │   │   ├── renewals/         # Renewal components
│       │   │   ├── expenses/         # Expense components
│       │   │   ├── dashboard/        # Dashboard widgets
│       │   │   ├── settings/         # Settings components
│       │   │   ├── shared/           # DataTable, EmptyState, ConfirmDialog, etc.
│       │   │   └── pdf/              # PDF template components (@react-pdf)
│       │   ├── routers/              # tRPC routers (one file per domain)
│       │   ├── trpc/                 # tRPC client, server, context, middleware
│       │   └── lib/                  # Helpers (supabase client, formatting)
│       └── public/
│           └── fonts/                # Inter TTF files for PDF rendering
│
├── packages/
│   ├── db/                           # @tsvj/db — Drizzle schema + migrations
│   │   ├── src/
│   │   │   ├── schema/               # 8 schema files (see §4)
│   │   │   ├── relations.ts          # Centralized Drizzle relations
│   │   │   ├── seed/                 # Seed data scripts
│   │   │   └── index.ts              # Re-exports: schema, db client, types
│   │   └── drizzle/                  # Migration files
│   │       └── custom/               # PL/pgSQL, materialized views, pg_cron
│   │
│   ├── computations/                 # @tsvj/computations — Pure business logic
│   │   └── src/
│   │       ├── decimal.ts            # Peso type, 7 rounding helpers
│   │       ├── escalation.ts         # NHSB + contractual rent escalation
│   │       ├── water.ts              # Tiered water billing
│   │       ├── electric.ts           # Blended electric billing
│   │       ├── penalty.ts            # Late payment + safe harbour caps
│   │       ├── billing.ts            # VAT determination, charge builder
│   │       ├── payment.ts            # Art. 1252-1254 allocation
│   │       ├── deposit.ts            # Security deposit validation
│   │       ├── contract.ts           # DST computation
│   │       ├── tax.ts                # EWT, VAT summary, apportionment
│   │       └── lease.ts              # State machine helpers
│   │
│   ├── ui/                           # @tsvj/ui — shadcn/ui components
│   │   └── src/
│   │       └── components/           # Radix primitives (Button, Dialog, etc.)
│   │
│   └── tsconfig/                     # @tsvj/tsconfig — Shared TS configs
│
├── supabase/
│   ├── config.toml                   # Supabase CLI config
│   └── functions/
│       └── send-alert-emails/        # Edge Function for email digest
│
├── tooling/
│   └── eslint/                       # Shared ESLint config
│
└── .github/
    └── workflows/
        ├── ci.yml                    # PR checks (lint, test, typecheck, schema)
        ├── migrate.yml               # Production DB migrations on merge
        └── edge-functions.yml        # Supabase Edge Function deploy
```

### 3.1 Turborepo Pipeline

```json
{
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": [".next/**", "dist/**"] },
    "lint": { "dependsOn": ["^build"] },
    "typecheck": { "dependsOn": ["^build"] },
    "test": { "dependsOn": ["^build"] },
    "dev": { "persistent": true, "cache": false }
  }
}
```

### 3.2 Root Scripts

```json
{
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "lint": "turbo lint",
    "typecheck": "turbo typecheck",
    "test": "turbo test",
    "db:push": "pnpm --filter @tsvj/db drizzle-kit push",
    "db:generate": "pnpm --filter @tsvj/db drizzle-kit generate",
    "db:migrate": "pnpm --filter @tsvj/db drizzle-kit migrate",
    "db:seed": "pnpm --filter @tsvj/db tsx src/seed/index.ts"
  }
}
```

*Full rationale: `analysis/project-structure.md`*

---

## 4. Database Schema

### 4.1 Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | `snake_case`, singular | `lease`, `billing_run` |
| Columns | `snake_case` | `date_start`, `vat_rate` |
| Enums | `snake_case` descriptive name | `lease_status`, `payment_method` |
| Enum values | `SCREAMING_SNAKE_CASE` | `CONTROLLED_RESIDENTIAL` |
| Primary keys | `serial` (most tables), `bigserial` (high-volume: charge, payment_allocation, issued_document_line, depreciation_schedule_entry) |
| Monetary values | PostgreSQL `numeric(precision, scale)` → JavaScript `string` → `decimal.js` for arithmetic |
| Timestamps | `timestamp with time zone` (`timestamptz`), defaultNow() |
| Foreign keys | `<referenced_table>_id`, always indexed |

### 4.2 Schema Files

8 schema files in `packages/db/src/schema/`:

| File | Tables | Purpose |
|------|--------|---------|
| `foundation.ts` | tenant, property, rentable, room | Core entities |
| `lease.ts` | lease, lease_event, recurring_charge, recurring_charge_period, nhsb_cap_rate, escalation_event, security_deposit, non_renewal_notice, renewal_record | Lease lifecycle |
| `billing.ts` | charge_type, billing_run, charge, credit_memo, penalty_ledger, demand_record | Billing + penalties |
| `payments.ts` | payment, payment_allocation, payment_event, form_2307_record | Payment tracking |
| `utilities.ts` | water_meter, water_meter_tenant, water_meter_reading, maynilad_bill, maynilad_rate_schedule, water_billing_run, water_charge, electric_meter, electric_meter_tenant, electric_meter_reading, meralco_bill, electric_billing_run, electric_charge | Water + electric |
| `documents.ts` | document_sequence, authority_to_print, issued_document, issued_document_line, lease_template, lease_clause | Document infra |
| `expenses.ts` | supplier_payee, expense_category, disbursement_voucher, input_vat_record, ewt_withheld_record | Expense tracking |
| `system.ts` | app_settings, audit_log, alert | System-wide |
| `reporting.ts` | rent_roll_report, lis_report, compliance_obligation, compliance_deadline, fixed_asset_register, depreciation_schedule_entry | Reporting |

**Total: 44 Drizzle tables + 1 materialized view (tenant_balance) + 24 pgEnums.**

### 4.3 Relations

All Drizzle relations are defined in a centralized `packages/db/src/relations.ts` file (not co-located with schema) to prevent circular imports between schema files.

### 4.4 Materialized View: tenant_balance

PostgreSQL materialized view computing per-tenant balance from charges and payment allocations. Refreshed within transactions on payment/charge mutations via `REFRESH MATERIALIZED VIEW CONCURRENTLY tenant_balance`. Not managed by Drizzle — defined in `packages/db/drizzle/custom/001_tenant_balance_view.sql`.

### 4.5 Custom SQL Objects

Objects not managed by Drizzle, applied via custom migration scripts:

| Object | File | Purpose |
|--------|------|---------|
| `tenant_balance` materialized view | `custom/001_tenant_balance_view.sql` | Per-tenant balance aggregation |
| `process_daily_alerts()` PL/pgSQL function | `custom/002_process_daily_alerts.sql` | Daily lease lifecycle + compliance + arrears checks |
| pg_cron schedule | `custom/003_cron_setup.sql` | Two jobs: 00:05 PHT alert generation, 00:06 PHT email trigger |
| Partial indexes | `custom/004_partial_indexes.sql` | Performance indexes not expressible in Drizzle |

### 4.6 Migration Strategy

- **Development:** `drizzle-kit push` (schema-first, no migration files)
- **Production:** `drizzle-kit generate` → `drizzle-kit migrate` (file-based, versioned)
- **Direct connection** for migrations (no PgBouncer)
- **Pooled connection** for app runtime (PgBouncer, `?pgbouncer=true`)

*Full rationale: `analysis/database-schema.md`*

---

## 5. Authentication & Authorization

### 5.1 Auth Provider

Supabase Auth with email/password. No magic links, no OAuth, no self-registration. Admin creates the accountant account via Supabase Admin API.

### 5.2 Role Model

Role stored in `app_metadata.role` (server-writable JWT claim, not user-editable):

| Role | Create | Read | Update | Delete | Exports |
|------|:------:|:----:|:------:|:------:|:-------:|
| **Admin** | All | All | All | All | All |
| **Accountant** | None | All (except settings internals) | alert.dismiss only | None | All |

### 5.3 4-Layer Defense

```
Layer 1: Next.js middleware    → redirects unauthenticated to /login
Layer 2: Server Component      → redirects wrong role (accountant → admin page)
Layer 3: tRPC middleware        → UNAUTHORIZED (no session) / FORBIDDEN (wrong role)
Layer 4: Client RoleGate        → hides admin-only UI elements
```

### 5.4 tRPC Middleware

```
protectedProcedure  = any authenticated user (queries + alert.dismiss)
adminProcedure      = admin role only (all mutations except alert.dismiss)
```

### 5.5 Session Management

Cookie-based via `@supabase/ssr`. No localStorage tokens. Session timebox: 24h (configurable). Inactivity timeout: 8h (configurable).

**No Row-Level Security.** Role enforcement is handled by tRPC middleware, not Postgres RLS. With 2 users and a single-tenant app, RLS adds complexity without benefit.

*Full rationale: `analysis/auth-and-roles.md`*

---

## 6. API Layer (tRPC)

### 6.1 Router Organization

21 sub-routers, ~90 procedures total:

| Router | Procedures | Domain |
|--------|:----------:|--------|
| `tenant` | 5 | Tenant CRUD + balance |
| `lease` | 6 | Lease CRUD + lifecycle |
| `property` | 4 | Property/rentable CRUD |
| `chargeType` | 4 | Charge type config |
| `escalation` | 9 | Rent escalation + NHSB |
| `water` | 17 | Water billing pipeline |
| `electric` | 16 | Electric billing pipeline |
| `penalty` | 10 | Late payment penalties |
| `billingRun` | 11 | Monthly billing + invoicing |
| `payment` | 11 | Payment recording + allocation |
| `deposit` | 7 | Security deposit lifecycle |
| `renewal` | 12 | Lease renewal + reconduction |
| `portfolio` | 4 | Lease status dashboard |
| `rentRoll` | 13 | Rent roll + LIS + SAWT |
| `tax` | 8 | Tax data compilation |
| `document` | 8 | Invoice/receipt/credit memo registers |
| `atp` | 7 | Authority to Print management |
| `contract` | 6 | Lease contract generation |
| `expense` | 17 | Expense/voucher management |
| `alert` | 4 | Alert list/dismiss |
| `compliance` | 4 | Compliance calendar |
| `settings` | 5 | App settings + admin tools |

### 6.2 Naming Convention

`domain.verb` — e.g., `tenant.list`, `billingRun.finalize`, `payment.create`.

### 6.3 Key Patterns

- **Input validation:** Zod schemas inline per procedure + shared pagination/filter schemas
- **Serialization:** superjson transformer (Date → ISO string, monetary values stay as `string`)
- **Pagination:** Cursor-based for all list endpoints (no offset)
- **Transactions:** `ctx.db.transaction()` for all multi-table mutations
- **Audit logging:** Fire-and-forget middleware on admin mutations → `audit_log` table
- **Error codes:** UNAUTHORIZED, FORBIDDEN, BAD_REQUEST, NOT_FOUND, CONFLICT, PRECONDITION_FAILED
- **Batch link:** `httpBatchLink` batches concurrent queries; mutations are never batched

### 6.4 Server-Side Prefetching

Server Components use `serverTrpc.entity.prefetch()` to run queries server-side. Data is dehydrated via `HydrateClient` and hydrated into React Query on the client — zero loading spinners for initial page load.

### 6.5 Export Pattern

Spreadsheet exports use tRPC queries returning structured JSON. The client dynamically imports SheetJS and generates XLSX/CSV locally. No server-side file generation for exports.

*Full rationale: `analysis/api-layer.md`*

---

## 7. UI Framework

### 7.1 Component Library

shadcn/ui (Radix unified package) for all primitives. No component library runtime — components are copied into the codebase and customizable.

### 7.2 Composed Domain Components

13 domain-specific composed components built on shadcn primitives:

| Component | Purpose |
|-----------|---------|
| `CurrencyInput` | Masked numeric input with ₱ prefix, 2-decimal enforcement |
| `TINInput` | Masked input enforcing NNN-NNN-NNN-NNN format |
| `PesoDisplay` | Formats string amount as ₱XX,XXX.XX |
| `RegimeBadge` | Color-coded badge for lease regime |
| `StatusBadge` | Variant-mapped badge for entity statuses |
| `RoleGate` | Conditionally renders children based on user role |
| `ExportButton` | Split button: primary XLSX, dropdown CSV |
| `DataTable` | TanStack Table wrapper with sorting, filtering, Load More |
| `EmptyState` | Illustration + message for empty lists |
| `ConfirmDialog` | Destructive action confirmation with typed consequences |
| `PageHeader` | Title + breadcrumbs + action buttons |
| `FormSection` | Grouped form fields with label |
| `AlertBanner` | Persistent top banner for OVERDUE alerts and system warnings |

### 7.3 Page Pattern

Every page follows this Server Component → Client Component pattern:

```
Server Component (page.tsx)
  → auth check (Supabase session)
  → role check (redirect if forbidden)
  → serverTrpc.entity.prefetch()
  → <HydrateClient>
      → <Suspense fallback={<Skeleton />}>
          → <ClientComponent />  (useSuspenseQuery)
      → </Suspense>
  → </HydrateClient>
```

### 7.4 Forms

react-hook-form + Zod resolver for all 19 forms. Form schemas shared with tRPC input schemas (or a subset). Regime-adaptive lease form uses `superRefine` for controlled/commercial rule enforcement.

### 7.5 Data Tables

TanStack Table v8 for ~35 data tables. Cursor-based pagination with "Load More" button. URL-persisted filters via nuqs.

### 7.6 Toasts

sonner for toast notifications. Success toasts on mutations, error toasts for server errors.

### 7.7 No Dark Mode

Not in MVP. Tailwind v4 CSS-based theme config makes it straightforward to add later.

*Full rationale: `analysis/ui-framework.md`*

---

## 8. State & Data Fetching

### 8.1 State Categories

| Category | Managed By | Examples |
|----------|------------|----------|
| Server state | React Query (via tRPC) | Tenant list, lease details, balances |
| Form state | react-hook-form | Input values, validation errors |
| URL state | nuqs | Filter values, search, sort |
| UI state | React useState | Sidebar toggle, active tab |

**No global state store.** No Redux, Zustand, or Context for server state. React Query is the single source of truth for all server data.

### 8.2 React Query Configuration

```
staleTime:              30 seconds (30s)
gcTime:                 5 minutes
refetchOnWindowFocus:   false
retry:                  1 (queries), 0 (mutations)
```

Alert count query uses shorter staleTime (10s) for header badge freshness.

### 8.3 Mutation Pattern

Standard: mutation → `onSuccess` callback → `invalidateQueries` for affected queries → React Query refetches.

**Optimistic updates** used only for:
1. Alert dismissal (instant X-button feedback)
2. Charge type active/inactive toggle

Everything else uses invalidation-based refetch for correctness.

### 8.4 Cross-Router Invalidation Map

Key mutation → invalidation relationships:

| Mutation | Invalidates |
|----------|------------|
| `payment.create` | payment.list, tenant.getBalance, tenant.getById, portfolio.getSummary |
| `billingRun.finalize` | billingRun.list, billingRun.getById, tenant.getBalance, document.listInvoices |
| `lease.activate` | lease.list, lease.getById, portfolio.getSummary, portfolio.list |
| `escalation.run` | escalation.list, lease.getById |
| `deposit.apply` | deposit.getById, deposit.list, tenant.getBalance |
| `alert.dismiss` | alert.list, alert.count |

### 8.5 Monetary Values

Strings end-to-end: PostgreSQL `numeric` → Drizzle `string` → tRPC `string` → client `string` → display via `PesoDisplay` or arithmetic via `decimal.js`.

*Full rationale: `analysis/state-and-data-fetching.md`*

---

## 9. Shared Computations Package

### 9.1 Design Principles

`@tsvj/computations` is a pure TypeScript package with **zero internal dependencies** (only `decimal.js ^10`):

- All functions are pure and synchronous (no I/O, no database)
- Inputs/outputs are plain objects with `string` monetary values
- Each module exports a primary computation function + supporting helpers
- tRPC routers bridge database ↔ computation (fetch data, call computation, persist results)

### 9.2 Peso Type & Rounding

`Peso` wraps `decimal.js`'s `Decimal`. 7 context-specific rounding helpers:

| Helper | Rounding Mode | Usage |
|--------|:------------:|-------|
| `roundNHSB(value)` | ROUND_DOWN | NHSB escalation cap (always favor tenant) |
| `roundWater(value)` | HALF_UP, 2dp | Water bill per tier |
| `roundElectricRate(value)` | HALF_UP, 4dp | Blended kWh rate |
| `roundElectric(value)` | HALF_UP, 2dp | Electric bill total |
| `roundVAT(value)` | HALF_UP, 2dp | VAT computation |
| `roundEWT(value)` | HALF_UP, 2dp | EWT computation |
| `roundPenalty(value)` | HALF_UP, 2dp | Penalty interest |

### 9.3 Computation Modules

| Module | Primary Function | Key Logic |
|--------|-----------------|-----------|
| `escalation.ts` | `computeEscalation()` | NHSB compounding (ROUND_DOWN), contractual (fixed/stepped/CPI), threshold crossing detection |
| `water.ts` | `computeWaterBilling()` | Per-tier MWSS IRR 2008-02, sewerage commercial-only, common area allocation |
| `electric.ts` | `computeElectricBilling()` | Blended rate (NOT per-tier), EPIRA no-markup, common area allocation |
| `penalty.ts` | `computePenalty()` | Simple interest, controlled safe harbour caps (1%/month, 1×rent/year) |
| `billing.ts` | `determineVAT()` | 8-scenario VAT tree (water=0%, electric configurable, residential≤₱15K exempt, commercial=12%) |
| `payment.ts` | `allocatePayment()` | Art. 1252-1254 (debtor designation → penalties before principal → most onerous/FIFO) |
| `deposit.ts` | `validateDeposit()` | RA 9653 caps (controlled: 2+1 months), refund computation |
| `contract.ts` | `computeDST()` | RA 9243 DST on leases (0.5% of excess over ₱1M for controlled, 0.75% for commercial) |
| `tax.ts` | `computeEWTOnRent()`, `computeEWTOnSupplier()` | EWT rate determination, VAT summary aggregation, input VAT apportionment |
| `lease.ts` | `determineReconduction()` | Art. 1670 tacit reconduction, Art. 1672 guarantor release |

### 9.4 Testing Strategy

Each module has a dedicated test file with test vectors derived from regulatory rules. Tests run via `pnpm --filter @tsvj/computations test`. No database or network access — pure function tests.

*Full rationale: `analysis/shared-computations.md`*

---

## 10. Document Generation

### 10.1 PDF Generation

`@react-pdf/renderer ^4` for server-side PDF rendering. No Chromium dependency. PDFs served via dedicated Next.js API routes:

| Route | Document Type | Auth | Trigger |
|-------|--------------|:----:|---------|
| `/api/pdf/invoice/[id]` | VAT Sales Invoice (16 mandatory fields per RR 7-2024) | Both | Billing run finalized |
| `/api/pdf/receipt/[id]` | Official Receipt | Both | Payment recorded |
| `/api/pdf/contract/[id]` | Lease Contract (clause assembly) | Admin | Contract generation wizard |
| `/api/pdf/statement/[id]` | Billing Statement | Both | Billing run finalized |
| `/api/pdf/form2307/[id]` | Supplier Form 2307 | Admin | Expense voucher finalized |
| `/api/pdf/batch` | ZIP of multiple PDFs (POST) | Both | Batch download button |

**Storage:** PDFs generated on-demand (not stored). All data needed to reproduce a finalized document is frozen in `issued_document` + `issued_document_line` at issuance time.

**Batch download:** `archiver ^7` for ZIP creation, capped at 100 documents per batch.

**Font:** Inter (TTF) for ₱ and ñ support, registered server-side.

### 10.2 Spreadsheet Exports

Client-side SheetJS (`xlsx 0.20.3` from CDN) via dynamic import. 13 export types:

| Export | Format | Source |
|--------|--------|--------|
| Rent Roll | XLSX, CSV | P11 |
| LIS Report | XLSX | P11 |
| SAWT | XLSX | P11 |
| 2550Q Data | XLSX | P12 |
| 1702Q Data | XLSX | P12 |
| EWT Summary | XLSX | P12 |
| DST Register | XLSX | P12 |
| SLSP | XLSX | P12 |
| Expense Register | XLSX, CSV | P14 |
| Input VAT Register | XLSX | P14 |
| Fixed Asset Schedule | XLSX | P14 |
| Depreciation Schedule | XLSX | P14 |
| Tenant Balance Report | CSV | P6 |

**Pattern:** tRPC query returns structured JSON → client formats via SheetJS → triggers browser download. Export queries use `enabled: false` (fetched only on button click, not on page load).

*Full rationale: `analysis/document-generation.md`*

---

## 11. Compliance & Alert System

### 11.1 Alert Categories

| Category | Source | Levels Used |
|----------|--------|-------------|
| `LEASE_EXPIRY` | Daily pg_cron job | INFO (90d), WARNING (60d), URGENT (30d), OVERDUE (15d) |
| `COMPLIANCE` | Daily pg_cron job | INFO (30d), WARNING (15d), URGENT (5d), OVERDUE (past) |
| `ATP_EXHAUSTION` | Synchronous on document issuance | INFO (80%), WARNING (90%), OVERDUE (100% = blocks issuance) |
| `ARREARS` | Synchronous on payment + daily job | WARNING (2 months), URGENT (3+ months = ejectment ground) |
| `FORM_2307_MISSING` | Daily pg_cron job | WARNING (10d post-quarter), URGENT (20d post-quarter) |

### 11.2 Alert Generation

- **Daily job:** `process_daily_alerts()` PL/pgSQL function via pg_cron (00:05 PHT). Handles lease lifecycle transitions, compliance deadline checks, arrears refresh, Form 2307 tracking.
- **Synchronous triggers:** ATP exhaustion checked during document number assignment; arrears checked during payment recording.
- **Deduplication:** Time-windowed `WHERE NOT EXISTS` per (category, entity, level).

### 11.3 Email Notifications

Resend API via Supabase Edge Function. URGENT/OVERDUE alerts only. Daily digest (not per-alert). Triggered by a second pg_cron job (00:06 PHT) that calls the Edge Function via `pg_net.http_post()`. ~5-10 emails/month estimated.

### 11.4 Compliance Calendar

~43 seeded compliance obligations (BIR, SEC, LGU). `compliance_deadline` table tracks per-period instances with status flow: UPCOMING → IN_PROGRESS → FILED (or OVERDUE if missed). Admin manages via `/settings/compliance` calendar view.

### 11.5 In-App Alert UI

- **Header bell icon:** Badge count of WARNING+ alerts, dropdown list, click to navigate
- **Alert banner:** Persistent top banner for OVERDUE items and system warnings
- **Dashboard widgets:** Upcoming deadlines, arrears alerts
- **Alerts page:** Full filterable list at `/alerts`

*Full rationale: `analysis/compliance-alerts.md`*

---

## 12. Deployment & Infrastructure

### 12.1 Topology

```
┌─────────────┐     ┌──────────────────────────┐
│   Vercel     │     │   Supabase (Pro $25/mo)   │
│   Next.js    │────▶│   PostgreSQL 15           │
│   Serverless │     │   Auth (email/password)   │
│   (Free/Pro) │     │   pg_cron + pg_net        │
└─────────────┘     │   Edge Functions          │
                     └──────────────────────────┘
                              │
                     ┌────────▼────────┐
                     │   Resend (Free)  │
                     │   Email API      │
                     └─────────────────┘
```

### 12.2 Environments

| Environment | Hosting | Database | Purpose |
|-------------|---------|----------|---------|
| Local dev | `next dev` + Supabase CLI | Local Postgres | Development |
| Preview | Vercel preview deploy | Supabase staging (free) | PR review |
| Production | Vercel production | Supabase Pro ($25/mo) | Live |

### 12.3 CI/CD Pipeline

1. **PR opened:** GitHub Actions runs lint, typecheck, test, schema check against staging DB
2. **PR merged to main:** Vercel auto-deploys; GitHub Actions runs Drizzle migrations against production DB (before deploy completes)
3. **Edge Function changes:** Separate workflow deploys via `supabase functions deploy`

### 12.4 Connection Pooling

- **App runtime:** Pooled connection via Supabase PgBouncer (`?pgbouncer=true`)
- **Migrations:** Direct connection (prepared statements, schema introspection)

### 12.5 Cost

| Service | Monthly | Notes |
|---------|:-------:|-------|
| Vercel | $0-20 | Free sufficient; Pro only if batch PDF timeout hit |
| Supabase Pro | $25 | Required for pg_cron, no-pause, backups |
| Resend | $0 | 3K/month free (need <50) |
| Domain | ~$2 | .app or .ph |
| **Total** | **$27-47** | |

### 12.6 Security Hardening

- HTTP security headers (X-Frame-Options: DENY, X-Content-Type-Options: nosniff, etc.) in `next.config.ts`
- Server-only secrets never prefixed with `NEXT_PUBLIC_`
- Health check endpoint at `/api/health`
- Network restrictions on Supabase Postgres (Vercel IPs + developer IP)
- No CSP in MVP (added post-stabilization)

*Full rationale: `analysis/deployment.md`*

---

## 13. Feature Specs

### 13.1 Spec Inventory

15 feature specs in `output/feature-specs/`:

| Spec | Feature | New Tables | tRPC Procedures | Dependencies |
|------|---------|:----------:|:---------------:|-------------|
| F0 | Foundation (Tenant, Lease, Property, Settings) | 7+3+2+1 = 13 | ~20 | None |
| P1 | Rent Escalation | 4 | 9 | F0 |
| P2 | Water Billing | 7 | 17 | F0 |
| P3 | Electric Billing | 6 | 16 | F0 |
| P4 | Late Payment Penalties | 2 | 10 | F0 |
| P5 | Monthly Billing Generation | 3+2 = 5 | 11 | F0, P1, P2, P3, P4 |
| P6 | Tenant Payment Tracking | 4+1 view | 11 | F0, P5 |
| P7 | Security Deposit Lifecycle | — (in F0) | 7 | F0 |
| P8 | Lease Contract Generation | — (in F0) | 6 | F0, P7 |
| P9 | Lease Renewal & Extension | 2 | 12 | F0, P1, P7, P8 |
| P10 | Lease Status Visibility | — | 4 | F0 |
| P11 | Rent Roll Preparation | 2 | 13 | F0, P5, P6 |
| P12 | Tax Data Compilation | — (in system) | 8 | F0, P5, P6, P11, P14 |
| P13 | Official Receipt / Invoice Data | — (in F0) | 15 | F0, P5, P6 |
| P14 | Expense Tracking | 5+2 = 7 | 17 | F0 |

### 13.2 Forward Loop Implementation Order

Follows the MVP pipeline from the process catalog:

```
Phase 1 (Core Billing Pipeline):  F0 → P1 → P5 → P6 → P11
Phase 2 (Utility Billing):        P2 + P3 + P4
Phase 3 (Lease Lifecycle):         P8 + P9 + P10
Phase 4 (Compliance + Expenses):   P7 + P12 + P13 + P14
```

Within each phase, features can be implemented in the listed order. Each feature spec is self-contained: a forward loop agent (or developer) can implement it from the spec alone + this architecture doc + the process catalog.

### 13.3 Feature Spec Structure

Every feature spec includes:

1. **Summary** — What the feature does
2. **Data model** — Drizzle schema (new tables, columns, enums)
3. **API surface** — tRPC procedures with Zod input/output schemas
4. **UI views** — ASCII mockups, role access, user interactions
5. **Business logic** — Computation rules, edge cases, regulatory references
6. **Validation rules** — Zod schemas for all inputs
7. **Dependencies** — Which features must exist first

**Backpressure sections (required in every spec):**

8. **Verification Commands** — Exact shell commands for the forward loop to confirm success (`pnpm build`, `pnpm test`, `pnpm lint`, `drizzle-kit check`, smoke tests)
9. **Acceptance Criteria** — Binary pass/fail checkboxes with specific verification method
10. **Done Signal** — `<task-complete>{spec-id}</task-complete>` output only after all criteria pass

---

## 14. Cross-Cutting Concerns

### 14.1 VAT Treatment Matrix

8 scenarios for VAT determination (implemented in `@tsvj/computations/billing.ts`):

| Charge Type | Tenant Type | Monthly Rent | VAT Rate | Rule |
|-------------|------------|:------------:|:--------:|------|
| Rent | Any | ≤₱15,000 | 0% (Exempt) | RA 9337 Sec. 109(P) |
| Rent | Any | >₱15,000 | 12% | Standard VAT |
| Water | Any | Any | 0% (Exempt) | BIR RR 16-2005 |
| Electric | Any | Any | Configurable | `AppSettings.electric_vat_treatment` (must be set before first billing) |
| Penalty | — | — | Follows parent rent charge | Same regime as the rent charge |
| Admin Fee | Any | Any | 12% | Always VATable |
| Common Area | — | — | Follows charge type | Same as water/electric |
| Deposit | — | — | N/A | Not a charge, no VAT |

### 14.2 EWT Rules

| Context | Rate | ATC Code | Applies To |
|---------|:----:|----------|------------|
| Rent (corporate tenant) | 5% | WC157 | All corporate tenants |
| Rent (individual tenant) | 0% | — | No withholding |
| Supplier (professional) | 10/15% | WI010/WI011 | Per expense_category |
| Supplier (contractor) | 2% | WC010/WC011 | Per expense_category |
| Supplier (government) | 0% | — | Government payees exempt |
| Utilities (direct) | 0% | — | MERALCO/Maynilad direct |

EWT computed by `@tsvj/computations/tax.ts`. Applied at payment time (P6) for rent, at voucher creation (P14) for expenses.

### 14.3 Tenant Type Bifurcation

10 processes behave differently based on tenant type (corporate vs individual) or lease regime (controlled residential vs commercial):

| Process | Bifurcation |
|---------|------------|
| P1 Escalation | Controlled: NHSB ROUND_DOWN cap. Commercial: contractual rate |
| P4 Penalties | Controlled: 1%/month + 1×rent/year safe harbour. Commercial: contractual rate uncapped |
| P5 VAT | ≤₱15K exempt residential vs 12% commercial |
| P6 EWT | Corporate: 5% withholding. Individual: none |
| P6 Form 2307 | Corporate: quarterly tracking. Individual: N/A |
| P7 Deposit | Controlled: capped at 2+1 months (RA 9653). Commercial: contractual |
| P8 Contract | Different clause templates per regime |
| P9 Renewal | Controlled: NHSB cap on renewal rent. Commercial: market rate |
| P9 Reconduction | Controlled: Art. 1687 monthly periods. Commercial: Art. 1670 same terms |
| P10 Status | Controlled: ejectment restricted (RA 9653 Sec. 10). Commercial: standard Civil Code |

### 14.4 Sequential Numbering

Gapless sequential numbering for BIR-regulated documents:

| Document Type | Format | Source | ATP-Controlled |
|---------------|--------|--------|:--------------:|
| VAT Sales Invoice | INV-YYYY-NNNN | `document_sequence` | Yes |
| Official Receipt | OR-YYYY-NNNN | `document_sequence` | Yes |
| Credit Memo | CM-YYYY-NNNN | `document_sequence` | Yes |
| Disbursement Voucher | DV-YYYYMM-NNNN | `document_sequence` | No |

Atomic increment via `UPDATE ... RETURNING` within transactions. ATP exhaustion at 100% blocks document issuance.

### 14.5 Lease Lifecycle State Machine

```
DRAFT → ACTIVE → EXPIRED → MONTH_TO_MONTH → TERMINATED
                          → RENEWED
               → TERMINATED (early termination)
```

8 event types tracked in `lease_event`: ACTIVATED, EXPIRED, RECONDUCTION_STARTED, ANNIVERSARY, RENEWED, TERMINATED, NOTICE_SENT, STATUS_CHANGED.

State transitions triggered by:
- Manual admin actions (DRAFT→ACTIVE, TERMINATED)
- Daily pg_cron job (ACTIVE→EXPIRED after date_end, EXPIRED→MONTH_TO_MONTH after 15-day Art. 1670 window)
- Renewal process (ACTIVE→RENEWED when successor lease created)

---

## 15. Key Decisions Summary

| Decision | Choice | Alternative Rejected | Why |
|----------|--------|---------------------|-----|
| PDF library | @react-pdf/renderer | Puppeteer | No Chromium = Vercel-compatible, simpler deployment |
| Spreadsheet export | Client-side SheetJS | Server-side generation | Small datasets (<200 rows), zero server load |
| State management | React Query only | Redux/Zustand | Server state in cache, URL state in nuqs, form state in RHF — nothing left for global store |
| Decimal handling | decimal.js | big.js | 7 rounding modes needed; big.js supports only 4 |
| Primary keys | serial/bigserial | UUID | 2-user single-tenant app; integer PKs = smaller, faster, human-readable |
| Auth | Supabase Auth email/password | Magic links, OAuth | Private backoffice for 2 known users |
| Role enforcement | tRPC middleware | Postgres RLS | 2 users, single-tenant — middleware is simpler and sufficient |
| PDF storage | On-demand generation | Stored files | <500 PDFs/month, render time ~200-500ms, data frozen at issuance |
| Email | Resend via Edge Function | SendGrid, direct SMTP | Simple API, free tier sufficient, Supabase-native integration |
| Hosting | Vercel + Supabase | Railway, self-hosted | Zero-config Next.js hosting + managed Postgres with built-in auth/cron |
| Pagination | Cursor-based + Load More | Offset + page numbers | Cursor-based is natural for sequential data; Load More simpler than infinite scroll |
| Monitoring | Vercel Logs + Supabase Dashboard | Sentry, Axiom | Sufficient for 2 users; add APM post-MVP if needed |

---

## Appendix A: Environment Variables

```bash
# .env.example

# === Supabase ===
NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# Server-only
SUPABASE_SERVICE_ROLE_KEY=eyJ...
DATABASE_URL=postgresql://postgres.<ref>:<password>@aws-0-<region>.pooler.supabase.com:6543/postgres?pgbouncer=true
DIRECT_DATABASE_URL=postgresql://postgres:<password>@db.<ref>.supabase.co:5432/postgres

# === Resend ===
RESEND_API_KEY=re_...

# === App ===
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## Appendix B: Forward Loop Quick Reference

### Starting a Feature

1. Read the feature spec: `output/feature-specs/<spec-id>.md`
2. Read this architecture doc for patterns and conventions
3. Read the process catalog (`input/process-catalog.md`) for regulatory rules referenced in the spec
4. Create branch: `feature/<spec-id>`
5. Implement following the spec's sections in order

### Verifying Work

After implementing each feature, run:

```bash
pnpm build                                    # TypeScript compiles
pnpm test                                     # All tests pass
pnpm lint                                     # No lint errors
pnpm --filter @tsvj/db drizzle-kit check      # Schema consistent
```

Then check the spec's Acceptance Criteria section and verify each criterion.

### Done Signal

Output `<task-complete>{spec-id}</task-complete>` only after ALL verification commands pass and ALL acceptance criteria are checked.

### Implementation Order

```
F0 → P1 → P5 → P6 → P11 → P2 → P3 → P4 → P8 → P9 → P10 → P7 → P12 → P13 → P14
```

---

*Compiled from 10 Wave 2 analysis files. See `analysis/` directory for full rationale, code samples, and trade-off evaluations per architectural concern.*
