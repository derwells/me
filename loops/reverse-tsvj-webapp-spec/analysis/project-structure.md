# Project Structure — Turborepo Monorepo Layout

*Wave 2 Architecture Decision | Depends on: data-model-extract, ui-requirements-extract, cross-cutting-extract*

---

## Decision Summary

Turborepo monorepo with **4 packages** and **1 app**. The Next.js app handles both frontend and API (tRPC lives inside the app via App Router route handlers). Shared packages isolate the database layer, business computation logic, and UI components. No separate backend app — tRPC procedures run as Next.js API routes.

---

## Pinned Dependencies

| Package | Version | Rationale |
|---------|---------|-----------|
| turbo | ^2.8 | Latest stable Turborepo with composable config |
| next | ^16.1 | Latest stable Next.js with App Router + Turbopack default |
| @trpc/server | ^11.10 | Latest tRPC v11 with SSE subscriptions, server prefetching |
| @trpc/client | ^11.10 | Matching client |
| @trpc/tanstack-react-query | ^11.10 | React Query integration for tRPC v11 |
| @tanstack/react-query | ^5 | Required by tRPC v11 |
| drizzle-orm | ^0.45 | Latest stable Drizzle (v1 beta available but not stable enough) |
| drizzle-kit | ^0.30 | Migration tooling |
| zod | ^3.24 | Validation (tRPC + forms) |
| @supabase/supabase-js | ^2 | Supabase client (auth, storage, realtime) |
| radix-ui | latest | Unified Radix package (Feb 2026 shadcn migration) |
| tailwindcss | ^4 | Styling |
| decimal.js | ^10 | Arbitrary-precision decimal arithmetic (built-in TS types, needed for context-specific rounding modes like ROUND_DOWN for NHSB escalation) |
| superjson | ^2 | Date/Decimal serialization over tRPC |
| typescript | ^5.7 | Required by tRPC v11 |
| pnpm | ^9 | Package manager (Turborepo default) |

**Why decimal.js over big.js:** The cross-cutting extract identifies 7 context-specific rounding rules (ROUND_DOWN for NHSB escalation, HALF_UP for water billing, etc.). `decimal.js` provides `toDecimalPlaces(dp, roundingMode)` with all IEEE 754 rounding modes built in. `big.js` supports only 4 rounding modes via `Big.RM`. The 15KB bundle size difference is negligible for a backoffice app.

---

## Monorepo Root Structure

```
tsvj-backoffice/
├── turbo.json                    # Turborepo pipeline config
├── package.json                  # Root workspace config (pnpm)
├── pnpm-workspace.yaml           # Workspace definition
├── pnpm-lock.yaml
├── tsconfig.json                 # Base TypeScript config
├── .env.example                  # Environment variable template
├── .gitignore
│
├── apps/
│   └── web/                      # Next.js 16 application (frontend + API)
│
├── packages/
│   ├── db/                       # Drizzle schema, migrations, Supabase client
│   ├── computations/             # Pure business logic (billing, tax, penalties)
│   ├── ui/                       # Shared UI components (shadcn/ui)
│   └── tsconfig/                 # Shared TypeScript configs
│
├── tooling/
│   └── eslint/                   # Shared ESLint config
│
└── .github/
    └── workflows/                # CI/CD
```

---

## Package Details

### `apps/web` — Next.js Application

The single application in the monorepo. Contains the tRPC API route handler, all pages, and server/client components.

```
apps/web/
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── drizzle.config.ts             # Points to @tsvj/db schema
├── public/
│   └── ...
│
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── layout.tsx            # Root layout (providers, sidebar)
│   │   ├── page.tsx              # Dashboard redirect
│   │   ├── globals.css
│   │   │
│   │   ├── (auth)/               # Auth route group (no sidebar)
│   │   │   ├── login/page.tsx
│   │   │   └── layout.tsx
│   │   │
│   │   ├── (app)/                # Authenticated route group (with sidebar)
│   │   │   ├── layout.tsx        # Sidebar + header + alert banner
│   │   │   ├── dashboard/page.tsx
│   │   │   │
│   │   │   ├── tenants/
│   │   │   │   ├── page.tsx          # Tenant list (table)
│   │   │   │   ├── new/page.tsx      # Create tenant form
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx      # Tenant detail (tabs)
│   │   │   │       └── edit/page.tsx # Edit tenant form
│   │   │   │
│   │   │   ├── leases/
│   │   │   │   ├── page.tsx          # Lease list / portfolio view
│   │   │   │   ├── new/page.tsx
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx      # Lease detail (tabs: charges, payments, events)
│   │   │   │       └── edit/page.tsx
│   │   │   │
│   │   │   ├── properties/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx
│   │   │   │       └── rooms/...
│   │   │   │
│   │   │   ├── billing/
│   │   │   │   ├── escalation/page.tsx       # P1: NHSB rates, escalation runs
│   │   │   │   ├── water/page.tsx            # P2: Meter readings, billing runs
│   │   │   │   ├── electric/page.tsx         # P3: Meter readings, billing runs
│   │   │   │   ├── penalties/page.tsx        # P4: Penalty computation
│   │   │   │   ├── runs/
│   │   │   │   │   ├── page.tsx              # P5: Billing run list
│   │   │   │   │   ├── new/page.tsx          # P5: Billing run wizard
│   │   │   │   │   └── [id]/page.tsx         # P5: Billing run detail + invoice list
│   │   │   │   └── charges/page.tsx          # Cross-reference: all charges
│   │   │   │
│   │   │   ├── payments/
│   │   │   │   ├── page.tsx                  # P6: Payment list
│   │   │   │   ├── new/page.tsx              # P6: Record payment (Art. 1252-1254 allocation)
│   │   │   │   └── [id]/page.tsx             # P6: Payment detail
│   │   │   │
│   │   │   ├── deposits/
│   │   │   │   ├── page.tsx                  # P7: Deposit list
│   │   │   │   └── [id]/page.tsx             # P7: Deposit lifecycle view
│   │   │   │
│   │   │   ├── contracts/
│   │   │   │   ├── page.tsx                  # P8: Contract list
│   │   │   │   ├── generate/page.tsx         # P8: Contract generation wizard
│   │   │   │   └── templates/page.tsx        # P8: Template management
│   │   │   │
│   │   │   ├── portfolio/
│   │   │   │   └── page.tsx                  # P10: Lease status visibility dashboard
│   │   │   │
│   │   │   ├── reports/
│   │   │   │   ├── rent-roll/page.tsx        # P11: 26-column rent roll
│   │   │   │   ├── tax/page.tsx              # P12: Tax data compilation
│   │   │   │   └── documents/page.tsx        # P13: Invoice/receipt registers
│   │   │   │
│   │   │   ├── expenses/
│   │   │   │   ├── page.tsx                  # P14: Expense list
│   │   │   │   ├── new/page.tsx              # P14: Disbursement voucher entry
│   │   │   │   └── suppliers/page.tsx        # P14: Supplier/payee management
│   │   │   │
│   │   │   └── settings/
│   │   │       ├── page.tsx                  # App settings (electric VAT, ATP management)
│   │   │       ├── users/page.tsx            # User management
│   │   │       └── compliance/page.tsx       # Compliance calendar
│   │   │
│   │   └── api/
│   │       └── trpc/
│   │           └── [trpc]/route.ts   # tRPC HTTP handler (catch-all)
│   │
│   ├── trpc/                     # tRPC setup (client, server, router aggregation)
│   │   ├── init.ts               # initTRPC with context, middleware
│   │   ├── router.ts             # Root appRouter (merges all sub-routers)
│   │   ├── context.ts            # Request context (Supabase session, user role)
│   │   ├── middleware.ts         # Auth middleware, role guards
│   │   ├── server.ts             # Server-side caller (RSC prefetch)
│   │   ├── client.tsx            # Client-side tRPC + React Query provider
│   │   └── query-client.tsx      # TanStack Query client config
│   │
│   ├── routers/                  # tRPC sub-routers (one per domain)
│   │   ├── tenant.ts             # F0: Tenant CRUD
│   │   ├── lease.ts              # F0: Lease CRUD + lifecycle events
│   │   ├── property.ts           # F0: Property + Room + Rentable CRUD
│   │   ├── charge-type.ts        # F0: ChargeType seed + management
│   │   ├── escalation.ts         # P1: NHSB rates, escalation runs
│   │   ├── water.ts              # P2: Meter readings, billing
│   │   ├── electric.ts           # P3: Meter readings, billing
│   │   ├── penalty.ts            # P4: Penalty computation
│   │   ├── billing-run.ts        # P5: Billing run, invoice generation
│   │   ├── payment.ts            # P6: Payment entry, allocation
│   │   ├── deposit.ts            # P7: Security deposit lifecycle
│   │   ├── contract.ts           # P8: Contract generation
│   │   ├── renewal.ts            # P9: Lease renewal/extension
│   │   ├── portfolio.ts          # P10: Lease status dashboard
│   │   ├── rent-roll.ts          # P11: Rent roll generation
│   │   ├── tax.ts                # P12: Tax data compilation
│   │   ├── document.ts           # P13: Invoice/receipt registers
│   │   ├── expense.ts            # P14: Expense tracking
│   │   ├── settings.ts           # App settings, ATP management
│   │   ├── compliance.ts         # Compliance obligations + alerts
│   │   └── alert.ts              # Unified alert system
│   │
│   ├── components/               # React components
│   │   ├── layout/
│   │   │   ├── sidebar.tsx
│   │   │   ├── header.tsx
│   │   │   ├── alert-banner.tsx
│   │   │   └── breadcrumbs.tsx
│   │   ├── tenants/              # Per-feature component groups
│   │   ├── leases/
│   │   ├── billing/
│   │   ├── payments/
│   │   ├── deposits/
│   │   ├── contracts/
│   │   ├── reports/
│   │   ├── expenses/
│   │   └── shared/               # Shared components (data tables, form fields, etc.)
│   │
│   ├── hooks/                    # Custom React hooks
│   │   ├── use-role.ts           # Current user role
│   │   └── use-alerts.ts         # Alert subscription
│   │
│   └── lib/                      # App-level utilities
│       ├── constants.ts
│       └── format.ts             # Currency, date, number formatting
│
├── supabase/                     # Supabase local dev config
│   ├── config.toml
│   └── seed.sql                  # Dev seed data
│
└── e2e/                          # Playwright E2E tests (future)
    └── ...
```

**Why tRPC inside the Next.js app (not a separate `packages/trpc`):** For a two-user backoffice app, a separate tRPC package adds indirection without benefit. The routers import directly from `@tsvj/db` and `@tsvj/computations`. If the API ever needs to serve a mobile app, the routers can be extracted to a package later — but YAGNI for now.

---

### `packages/db` — Database Layer

Contains all Drizzle schema definitions, migrations, and the Supabase client factory. This is the single source of truth for the data model.

```
packages/db/
├── package.json                  # name: "@tsvj/db"
├── tsconfig.json
├── drizzle.config.ts
│
├── src/
│   ├── index.ts                  # Re-exports: schema, client, types
│   ├── client.ts                 # Drizzle + Supabase Postgres client factory
│   │
│   ├── schema/                   # Drizzle table definitions
│   │   ├── index.ts              # Re-exports all schemas
│   │   ├── enums.ts              # All pgEnum definitions (20 enums from data model extract)
│   │   │
│   │   ├── foundation.ts         # Property, Room, Rentable, Tenant, Lease, LeaseRentable, ChargeType
│   │   ├── billing.ts            # RecurringCharge, RecurringChargePeriod, NHSBCapRate, EscalationEvent,
│   │   │                         # WaterMeter, WaterMeterReading, MayniladBill, WaterBillingRun, WaterCharge,
│   │   │                         # ElectricMeter, ElectricMeterReading, MeralcoBill, ElectricBillingRun, ElectricCharge
│   │   ├── charges.ts            # Charge (unified), PenaltyCharge, BillingRun, BillingRunItem
│   │   ├── collection.ts         # Payment, PaymentAllocation, SecurityDeposit, DepositDeduction,
│   │   │                         # TenantStatement, Form2307Record, SAWTRecord
│   │   ├── contracts.ts          # LeaseTemplate, LeaseTemplateClause, GeneratedContract, ContractVariable,
│   │   │                         # LeaseEvent, LeaseRenewal
│   │   ├── documents.ts          # AuthorityToPrint, DocumentSequence, IssuedDocument, IssuedDocumentLine,
│   │   │                         # DocumentRegister, CreditMemo
│   │   ├── expenses.ts           # SupplierPayee, ExpenseCategory, DisbursementVoucher, DisbursementVoucherLine,
│   │   │                         # EWTWithheldRegister
│   │   ├── reporting.ts          # RentRollSnapshot, RentRollLine, OutputVATSummary, InputVATRegister,
│   │   │                         # TaxFilingRecord, ComplianceObligation
│   │   ├── system.ts             # AppSettings, Alert, AuditLog, User (Supabase auth.users reference)
│   │   └── relations.ts          # All Drizzle relations() definitions (centralized)
│   │
│   ├── migrations/               # Drizzle-kit generated migrations
│   │   └── ...
│   │
│   └── seed/                     # Seed data for development
│       ├── index.ts
│       ├── charge-types.ts       # ChargeType seed (RENT, WATER, ELECTRIC, PENALTY, etc.)
│       ├── compliance.ts         # ComplianceObligation seed (~43 deadlines)
│       └── dev-data.ts           # Sample tenants, leases, properties for dev
│
└── drizzle/                      # Drizzle-kit output dir (generated)
    └── ...
```

**Schema file organization rationale:** Files map to the 6 entity categories from the data model extract (Foundation=7, Billing=16, Collection=10, Contracts=7, Documents=6+, Expenses=5, Reporting=6+, System=4). Each file stays under ~15 tables, keeping files navigable. Relations are centralized in one file to avoid circular import issues (Drizzle's `relations()` requires all tables to be importable from a single scope).

**Package exports:**
```ts
// packages/db/src/index.ts
export * from "./schema";
export { createDbClient } from "./client";
export type { DbClient } from "./client";
```

---

### `packages/computations` — Business Logic

Pure TypeScript functions for all billing, tax, and penalty computations. No database access, no I/O — takes data in, returns results. This makes the logic independently testable and reusable.

```
packages/computations/
├── package.json                  # name: "@tsvj/computations"
├── tsconfig.json
├── vitest.config.ts              # Unit tests for all computation logic
│
├── src/
│   ├── index.ts                  # Re-exports all computation modules
│   │
│   ├── decimal.ts                # decimal.js wrapper: Peso type, rounding helpers per context
│   │                             # exports: peso(), roundNHSB(), roundStandard(), roundRate()
│   │
│   ├── escalation/               # P1: Rent escalation
│   │   ├── nhsb.ts               # NHSB cap rate lookup + compounding calculation
│   │   ├── contractual.ts        # Fixed %, stepped, CPI-linked escalation
│   │   └── threshold.ts          # PHP 10K threshold crossing detection
│   │
│   ├── water/                    # P2: Water billing
│   │   ├── tiered-billing.ts     # Maynilad per-tier computation
│   │   └── allocation.ts         # Shared meter allocation
│   │
│   ├── electric/                 # P3: Electric billing
│   │   ├── blended-rate.ts       # Meralco blended rate computation
│   │   └── allocation.ts         # Shared meter allocation
│   │
│   ├── penalty/                  # P4: Late payment penalties
│   │   ├── simple-interest.ts    # Monthly simple interest computation
│   │   └── caps.ts               # Controlled-lease safe harbour caps
│   │
│   ├── billing/                  # P5: Billing generation
│   │   ├── charge-builder.ts     # Build Charge from RecurringChargePeriod + utilities + penalties
│   │   └── vat.ts                # VAT determination logic (8 scenarios from cross-cutting extract)
│   │
│   ├── payment/                  # P6: Payment allocation
│   │   └── art-1252.ts           # Art. 1252-1254 allocation algorithm (most onerous first)
│   │
│   ├── deposit/                  # P7: Security deposit
│   │   ├── validation.ts         # 2+1 rule enforcement for controlled leases
│   │   └── refund.ts             # Deduction computation, interest return
│   │
│   ├── contract/                 # P8: Contract generation
│   │   └── dst.ts                # Documentary Stamp Tax computation (TRAIN Law formula)
│   │
│   ├── tax/                      # P12: Tax computations
│   │   ├── ewt-rent.ts           # 5% EWT on rent (corporate tenants)
│   │   ├── ewt-supplier.ts       # 2-15% EWT on supplier payments (rate matrix lookup)
│   │   ├── vat-summary.ts        # Quarterly VAT summary (2550Q data)
│   │   └── apportionment.ts      # Mixed-operation input VAT apportionment
│   │
│   └── lease/                    # P9/P10: Lease lifecycle
│       ├── state-machine.ts      # Valid transitions, reconduction detection
│       └── alerts.ts             # Expiry countdown alert generation
│
└── tests/                        # Unit tests (one per module)
    ├── escalation/
    │   ├── nhsb.test.ts
    │   └── threshold.test.ts
    ├── water/
    │   └── tiered-billing.test.ts
    ├── electric/
    │   └── blended-rate.test.ts
    ├── penalty/
    │   └── simple-interest.test.ts
    ├── billing/
    │   └── vat.test.ts
    ├── payment/
    │   └── art-1252.test.ts
    ├── deposit/
    │   └── validation.test.ts
    ├── contract/
    │   └── dst.test.ts
    ├── tax/
    │   ├── ewt-rent.test.ts
    │   ├── ewt-supplier.test.ts
    │   └── vat-summary.test.ts
    └── lease/
        └── state-machine.test.ts
```

**Why a separate `computations` package:**
1. **Testability:** ~95 regulatory rules (from process catalog) each need deterministic unit tests. Pure functions with no DB dependency = fast, reliable tests.
2. **Forward loop constraint:** Each feature spec's verification commands include `pnpm run test -- packages/computations/tests/<module>`. Isolating computation logic means the forward loop can verify correctness independently of UI/API.
3. **Reusability:** If a mobile app or CLI tool needs the same logic, it imports `@tsvj/computations` directly.

**Package exports:**
```ts
// packages/computations/src/index.ts
export * from "./decimal";
export * from "./escalation";
export * from "./water";
export * from "./electric";
export * from "./penalty";
export * from "./billing";
export * from "./payment";
export * from "./deposit";
export * from "./contract";
export * from "./tax";
export * from "./lease";
```

---

### `packages/ui` — Shared UI Components

shadcn/ui-based component library. Components are copied in via `npx shadcn add` and customized as needed.

```
packages/ui/
├── package.json                  # name: "@tsvj/ui"
├── tsconfig.json
├── tailwind.config.ts
│
├── src/
│   ├── index.ts                  # Re-exports all components
│   │
│   ├── components/
│   │   ├── ui/                   # shadcn/ui base components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── select.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── table.tsx
│   │   │   ├── tabs.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── card.tsx
│   │   │   ├── form.tsx          # react-hook-form + zod integration
│   │   │   ├── data-table.tsx    # TanStack Table wrapper (35+ tables in the app)
│   │   │   ├── date-picker.tsx
│   │   │   ├── toast.tsx
│   │   │   ├── alert.tsx
│   │   │   ├── command.tsx       # Command palette (for quick nav)
│   │   │   ├── sidebar.tsx       # shadcn sidebar component
│   │   │   └── ...               # Other shadcn primitives as needed
│   │   │
│   │   └── composed/             # App-specific composed components
│   │       ├── currency-input.tsx    # PHP currency input with decimal.js formatting
│   │       ├── tin-input.tsx         # TIN format validation (###-###-###-###)
│   │       ├── peso-display.tsx      # Currency display with proper formatting
│   │       ├── regime-badge.tsx      # Lease regime badge (CONTROLLED/NON_CONTROLLED/COMMERCIAL)
│   │       ├── status-badge.tsx      # Generic status badge (lease, deposit, billing run states)
│   │       ├── role-gate.tsx         # Renders children only if user has required role
│   │       └── export-button.tsx     # CSV/XLSX export trigger
│   │
│   └── lib/
│       └── utils.ts              # cn() helper, etc.
```

**Why `packages/ui` instead of components in `apps/web`:** The shadcn pattern already expects a `components/ui/` directory. Putting it in a shared package lets future apps (e.g., a tenant-facing portal) reuse the same design system. For a single-app project this is marginally useful — but it's the standard Turborepo pattern and costs nothing to set up.

---

### `packages/tsconfig` — Shared TypeScript Configs

```
packages/tsconfig/
├── package.json                  # name: "@tsvj/tsconfig"
├── base.json                     # Shared base config (strict, ESM, path aliases)
├── nextjs.json                   # Extends base, adds Next.js-specific settings
├── library.json                  # Extends base, for packages/db and packages/computations
└── vitest.json                   # Test-specific overrides
```

### `tooling/eslint` — Shared ESLint Config

```
tooling/eslint/
├── package.json                  # name: "@tsvj/eslint-config"
├── base.js                       # Base rules (strict TypeScript, no-unused-vars, etc.)
├── nextjs.js                     # Next.js-specific rules
└── library.js                    # Library-specific rules
```

---

## turbo.json Pipeline Configuration

```jsonc
{
  "$schema": "https://turborepo.dev/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "dependsOn": ["^build"],
      "persistent": true,
      "cache": false
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"]
    },
    "db:generate": {
      "cache": false
    },
    "db:migrate": {
      "cache": false
    },
    "db:push": {
      "cache": false
    },
    "db:seed": {
      "cache": false
    },
    "typecheck": {
      "dependsOn": ["^build"]
    }
  }
}
```

---

## Dependency Graph

```
apps/web
  ├── @tsvj/db             (schema types, client)
  ├── @tsvj/computations   (billing, tax, penalty logic)
  └── @tsvj/ui             (shared components)

packages/computations
  └── decimal.js           (no internal dependencies)

packages/db
  ├── drizzle-orm
  ├── @supabase/supabase-js
  └── zod                  (for schema validation types)

packages/ui
  ├── radix-ui
  ├── tailwindcss
  ├── @tanstack/react-table
  └── react-hook-form + @hookform/resolvers
```

**Key constraint:** `@tsvj/computations` has ZERO internal package dependencies. It depends only on `decimal.js`. This keeps computation logic portable and fast to test.

**`@tsvj/db`** does NOT depend on `@tsvj/computations`. Computed values (VAT, penalties, escalation results) are calculated in the tRPC router layer by calling `@tsvj/computations` functions, then stored via `@tsvj/db`. This avoids coupling the schema to business logic.

---

## Forward Loop Implementation Order

The forward loop implements features in this order (from process catalog MVP pipeline). Each maps to a folder in `apps/web/src/routers/` and corresponding pages:

| Order | Feature | Creates/Modifies | Primary Package Work |
|:-----:|---------|-------------------|---------------------|
| 1 | F0 (Foundation) | `foundation.ts` schema, tenant/lease/property routers + pages | `@tsvj/db` schema, seed data |
| 2 | P1 (Escalation) | `billing.ts` schema additions, escalation router + pages | `@tsvj/computations/escalation` |
| 3 | P5 (Monthly Billing) | `charges.ts` schema, billing-run router + wizard | `@tsvj/computations/billing` |
| 4 | P6 (Payment Tracking) | `collection.ts` schema, payment router + pages | `@tsvj/computations/payment` |
| 5 | P11 (Rent Roll) | `reporting.ts` schema, rent-roll router + page | — (aggregation queries) |
| 6 | P2 (Water) | `billing.ts` additions, water router + pages | `@tsvj/computations/water` |
| 7 | P3 (Electric) | `billing.ts` additions, electric router + pages | `@tsvj/computations/electric` |
| 8 | P4 (Penalties) | `charges.ts` additions, penalty router + pages | `@tsvj/computations/penalty` |
| 9 | P8 (Contracts) | `contracts.ts` schema, contract router + wizard | `@tsvj/computations/contract` |
| 10 | P9 (Renewal) | `contracts.ts` additions, renewal router + pages | `@tsvj/computations/lease` |
| 11 | P10 (Portfolio) | — (reads existing data), portfolio router + dashboard | `@tsvj/computations/lease` |
| 12 | P7 (Deposits) | `collection.ts` additions, deposit router + pages | `@tsvj/computations/deposit` |
| 13 | P12 (Tax Data) | `reporting.ts` additions, tax router + pages | `@tsvj/computations/tax` |
| 14 | P13 (Documents) | `documents.ts` schema, document router + pages | — (numbering logic in router) |
| 15 | P14 (Expenses) | `expenses.ts` schema, expense router + pages | `@tsvj/computations/tax` |

---

## Testing Strategy

| Layer | Tool | Location | Run Command |
|-------|------|----------|-------------|
| Computation unit tests | Vitest | `packages/computations/tests/` | `pnpm --filter @tsvj/computations test` |
| Database schema tests | Vitest + Drizzle push to test DB | `packages/db/tests/` | `pnpm --filter @tsvj/db test` |
| tRPC router integration tests | Vitest + tRPC caller | `apps/web/tests/routers/` | `pnpm --filter web test` |
| Component tests | Vitest + Testing Library (future) | `apps/web/tests/components/` | `pnpm --filter web test` |
| E2E tests | Playwright (future, post-MVP) | `e2e/` | `pnpm run e2e` |

**Forward loop verification:** Each feature spec includes `pnpm run test -- <pattern>` targeting the specific test files for that feature. The forward loop runs these after implementing each feature.

---

## Script Conventions

Root `package.json` scripts:
```json
{
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "lint": "turbo lint",
    "test": "turbo test",
    "typecheck": "turbo typecheck",
    "db:generate": "turbo db:generate",
    "db:migrate": "turbo db:migrate",
    "db:push": "turbo db:push",
    "db:seed": "turbo db:seed",
    "db:studio": "pnpm --filter @tsvj/db drizzle-kit studio",
    "format": "prettier --write \"**/*.{ts,tsx,md}\""
  }
}
```

Each package also has its own scripts in `package.json` that Turborepo orchestrates.

---

*Decision made: 2026-03-02 | Concrete, actionable structure ready for forward loop scaffolding in F0*
