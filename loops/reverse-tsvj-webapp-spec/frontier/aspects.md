# Frontier — TSVJ Backoffice Web App Spec

## Statistics
- Total aspects discovered: 26
- Analyzed: 2
- Pending: 24
- Convergence: 7.7%

## Pending Aspects (ordered by dependency)

### Wave 1: Source Extraction
- [x] data-model-extract — Extract all entities, fields, relationships, and constraints from process catalog into unified data model
- [x] ui-requirements-extract — Extract all views, forms, dashboards, tables, exports from process catalog; group by role (admin/accountant)
- [ ] cross-cutting-extract — Extract VAT matrix, EWT rules, tenant type bifurcation, numbering, lease lifecycle as they affect web app design

### Wave 2: Architecture Decisions
Depends on Wave 1 data.
- [ ] project-structure — Turborepo monorepo layout: packages, apps, shared code organization
- [ ] database-schema — Drizzle schema design: table organization, naming conventions, migration strategy, Supabase integration
- [ ] auth-and-roles — Supabase Auth setup, admin vs accountant role enforcement, row-level security
- [ ] api-layer — tRPC router organization, middleware, error handling patterns
- [ ] ui-framework — Next.js app router structure, component library choice (shadcn/ui vs alternatives), layout patterns
- [ ] state-and-data-fetching — tRPC + React Query patterns, optimistic updates, cache invalidation
- [ ] shared-computations — Where billing/tax/penalty computation logic lives (shared package), decimal handling, rounding rules
- [ ] document-generation — PDF generation for invoices, receipts, contracts, rent roll exports (CSV/XLSX)
- [ ] compliance-alerts — Notification system for deadline alerts (in-app, email), scheduled jobs
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
