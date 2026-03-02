# Frontier — TSVJ Backoffice Web App Spec

## Statistics
- Total aspects discovered: 26
- Analyzed: 12
- Pending: 14
- Convergence: 46.2%

## Pending Aspects (ordered by dependency)

### Wave 1: Source Extraction
- [x] data-model-extract — Extract all entities, fields, relationships, and constraints from process catalog into unified data model
- [x] ui-requirements-extract — Extract all views, forms, dashboards, tables, exports from process catalog; group by role (admin/accountant)
- [x] cross-cutting-extract — Extract VAT matrix, EWT rules, tenant type bifurcation, numbering, lease lifecycle as they affect web app design

### Wave 2: Architecture Decisions
Depends on Wave 1 data.
- [x] project-structure — Turborepo monorepo layout: packages, apps, shared code organization
- [x] database-schema — Drizzle schema design: table organization, naming conventions, migration strategy, Supabase integration
- [x] auth-and-roles — Supabase Auth setup, admin vs accountant role enforcement, row-level security
- [x] api-layer — tRPC router organization, middleware, error handling patterns
- [x] ui-framework — Next.js app router structure, component library choice (shadcn/ui vs alternatives), layout patterns
- [x] state-and-data-fetching — tRPC + React Query patterns, optimistic updates, cache invalidation
- [x] shared-computations — Where billing/tax/penalty computation logic lives (shared package), decimal handling, rounding rules
- [x] document-generation — PDF generation for invoices, receipts, contracts, rent roll exports (CSV/XLSX)
- [x] compliance-alerts — Notification system for deadline alerts (in-app, email), scheduled jobs
- [ ] deployment — Vercel/Railway/Supabase deployment topology, environment config, CI/CD

### Wave 3: Feature Specs
Depends on Wave 2 decisions.
- [ ] spec-F0 — Foundation: Lease & Tenant Master (data model, CRUD views, admin forms)
- [ ] spec-P1 — Rent Escalation Calculation (NHSB lookup, computation engine, escalation history view)
- [ ] spec-P2 — Water Billing (meter readings entry, per-tier computation, billing run)
- [ ] spec-P3 — Electric Billing (meter readings entry, blended rate computation, billing run)
- [ ] spec-P4 — Late Payment Penalties (penalty computation, grace period, arrears alerts)
- [ ] spec-P5 — Monthly Billing Generation (billing run, invoice generation, statement view)
- [ ] spec-P6 — Tenant Payment Tracking (payment entry, allocation, balance dashboard)
- [ ] spec-P7 — Security Deposit Lifecycle (collection, holding, deduction, refund workflow)
- [ ] spec-P8 — Lease Contract Generation (template system, variable substitution, DST, PDF)
- [ ] spec-P9 — Lease Renewal & Extension (expiry workflow, reconduction detection, renewal)
- [ ] spec-P10 — Lease Status Visibility (portfolio dashboard, state machine, alerts)
- [ ] spec-P11 — Rent Roll Preparation (26-column report, export, accountant view)
- [ ] spec-P12 — Tax Data Compilation (6 sub-processes, quarterly/annual summaries)
- [ ] spec-P13 — Official Receipt / Invoice Data (dual-document, ATP tracking, numbering)
- [ ] spec-P14 — Expense Tracking (disbursement entry, EWT computation, categorization)

### Wave 4: Synthesis
Depends on all Wave 3 specs.
- [ ] architecture-compilation — Combine Wave 2 decisions into output/architecture.md with cross-references to feature specs
- [ ] self-review — Verify completeness, consistency, forward-loop readiness

## Recently Analyzed
- data-model-extract (Wave 1) — 65 entities, 20 enums, ~300 fields extracted from process catalog
- ui-requirements-extract (Wave 1) — ~47 views, ~19 forms, ~35 tables, ~21 exports, ~6 dashboards. Full role-based access matrix (Admin vs Accountant). ASCII mockups for all key screens.
- cross-cutting-extract (Wave 1) — 5 cross-cutting concerns (VAT matrix with 8 scenarios, EWT rules for rent + suppliers, tenant type bifurcation across 10 processes, sequential numbering with ATP management, lease lifecycle state machine with 8 event types). Plus decimal handling rules and compliance calendar summary. 3 conflicting rules flagged for accountant configuration.
- project-structure (Wave 2) — Turborepo monorepo: 1 app (apps/web: Next.js 16 + tRPC v11), 4 packages (@tsvj/db, @tsvj/computations, @tsvj/ui, @tsvj/tsconfig). tRPC routers inside Next.js app (not separate package). Schema files organized by entity category (6 files). Computations package = zero internal deps, pure functions, decimal.js for rounding. 15-step forward loop implementation order. Vitest for all test layers.
- database-schema (Wave 2) — 44 Drizzle tables + 1 materialized view (TenantBalance) + 24 pgEnums across 8 schema files. Serial PKs (bigserial for high-volume tables). PostgreSQL numeric-only for all monetary values (never float). snake_case naming. Centralized relations.ts to avoid circular imports. Atomic document sequence increment with ATP overflow check. No RLS (middleware-based role enforcement). No soft deletes (status-based lifecycle + immutable audit logs). Push-based dev migrations, file-based production. JSONB columns with paired Zod schemas. FK indexes on all foreign keys + query-critical composite/partial indexes.
- auth-and-roles (Wave 2) — Supabase Auth email/password (no magic links, no OAuth). Role stored in `app_metadata.role` (server-writable JWT claim). tRPC middleware: `authed` (any logged-in user) + `adminOnly` (rejects accountant). 4-layer defense: Next.js middleware (auth redirect) → page-level Server Component (role redirect) → tRPC middleware (UNAUTHORIZED/FORBIDDEN) → client-side RoleGate (UX). No RLS. No self-registration (admin creates accountant via Supabase Admin API). @supabase/ssr for cookie-based sessions. Complete role-procedure mapping: all queries = protectedProcedure, all mutations = adminProcedure (except alert.dismiss). Settings router admin-only for reads too.
- api-layer (Wave 2) — 21 sub-routers, ~90 procedures (full inventory). domain.verb naming (e.g., tenant.list, billingRun.finalize). superjson transformer for Date serialization, monetary values stay as strings. Cursor-based pagination for all list endpoints. Zod input schemas inline per router + shared pagination/filter schemas. Transaction-wrapped multi-table mutations. Fire-and-forget audit logging middleware on all admin mutations. RSC prefetching via tRPC server caller + React Query hydration. Client-side CSV/XLSX export via SheetJS (dynamic import). pg_cron daily lifecycle job for lease state transitions + compliance deadline alerts. httpBatchLink for request batching. Cross-router cache invalidation map. 6 tRPC error codes used with structured business rule error metadata.
- ui-framework (Wave 2) — Next.js 16 App Router with Server Components default. shadcn/ui (Radix unified) for all primitives + 13 composed domain components (CurrencyInput, TINInput, PesoDisplay, RegimeBadge, StatusBadge, RoleGate, ExportButton, DataTable, EmptyState, ConfirmDialog, PageHeader, FormSection, AlertBanner). react-hook-form + Zod resolver for all 19 forms (shared schemas with tRPC). TanStack Table v8 for ~35 data tables with sorting, filtering, cursor-based pagination. Regime-adaptive lease form with superRefine for controlled/commercial rule enforcement. nuqs for URL filter state. sonner for toasts. date-fns for date formatting. Consistent page pattern: Server Component page → auth check → prefetch → HydrateClient → Client Component. No dark mode in MVP. Tailwind v4 with CSS-based theme config. ~42KB additional client bundle (excluding dynamic-imported SheetJS).
- state-and-data-fetching (Wave 2) — React Query (via @trpc/tanstack-react-query) as sole data layer. useSuspenseQuery + RSC prefetch via serverTrpc for zero-loading-spinner page loads. 30s staleTime, no refetchOnWindowFocus. Invalidation-based cache updates for all mutations except alert dismiss + charge type toggle (optimistic). Cross-router invalidation map for payment/billing/lease mutations. nuqs for URL filter state, react-hook-form for form state, local useState for UI state. No global state store. httpBatchLink batches concurrent queries. "Load More" pagination pattern. Suspense boundaries on all data pages. Monetary values stay as strings end-to-end.
- shared-computations (Wave 2) — Pure TypeScript `@tsvj/computations` package with zero internal deps (only decimal.js). Peso wrapper type + 7 context-specific rounding functions (ROUND_DOWN for NHSB, HALF_UP for water/electric/VAT/EWT/penalty, 4-decimal for electric rate). 10 computation modules: escalation (NHSB + contractual + threshold), water (tiered-billing + allocation), electric (blended-rate + allocation), penalty (simple-interest + caps), billing (VAT determination + charge builder), payment (Art. 1252-1254 allocation), deposit (validation + refund), contract (DST), tax (EWT rent + EWT supplier + VAT summary + apportionment), lease (state machine + alerts). ~20 primary functions, all pure/synchronous, string inputs/outputs. tRPC routers bridge DB↔computation. Complete test strategy with test vectors per module.
- document-generation (Wave 2) — @react-pdf/renderer ^4 for server-side PDF via dedicated Next.js API routes (/api/pdf/[type]/[id]). 5 PDF types: VAT Sales Invoice (16 mandatory RR 7-2024 fields), Official Receipt, Lease Contract (clause assembly + variable substitution), Billing Statement, Supplier Form 2307. On-demand generation (not stored). Batch download via archiver ^7 (ZIP). SheetJS 0.20.3 (CDN install) for 13 XLSX/CSV exports via dynamic import. Inter font for ₱/ñ. pdf-parse for test assertions. PDF infra in F0, invoice/receipt templates in P5/P6, contract in P8, Form 2307 in P14.
- compliance-alerts (Wave 2) — 5 alert categories (LEASE_EXPIRY, COMPLIANCE, ATP_EXHAUSTION, ARREARS, FORM_2307_MISSING) fed by daily pg_cron PL/pgSQL function + synchronous tRPC triggers. Resend email via Supabase Edge Function for URGENT/OVERDUE (daily digest, ~5-10/month). ComplianceDeadline table tracks ~43 seeded obligations with JSONB deadline_rule computation. Deduplication via time-windowed NOT EXISTS checks. Alert UI: header bell dropdown + /alerts page + dashboard widgets + persistent AlertBanner for OVERDUE. Compliance calendar at /settings/compliance with admin mark-as-filed workflow. alert.dismiss is only mutation both roles can access. Implementation spans F0 (infra) → P5/P6 (ATP + arrears) → P10 (lease lifecycle) → P12 (compliance deadlines + calendar).
