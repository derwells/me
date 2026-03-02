# Analysis Log — TSVJ Backoffice Web App Spec

| # | Aspect | Wave | Output File | Summary |
|---|--------|------|-------------|---------|
| 1 | data-model-extract | 1 | `input/data-model-extract.md` | 65 entities (51 new, 7 enhanced existing), 20 enums, ~300 fields. Organized into 6 categories: Foundation (7), Billing (16), Collection (10), Contracts (7), Handoff/Reporting (18), Cross-cutting (2). Includes state machines, JSONB schemas, decimal handling rules, and full relationship map. |
| 2 | ui-requirements-extract | 1 | `input/ui-requirements-extract.md` | ~47 views, ~19 forms, ~35 tables, ~21 exports, ~6 dashboards across 14 processes + foundation + settings. Full role-based access matrix (Admin=full CRUD, Accountant=read+export). ASCII mockups for: app shell, dashboard, tenant CRUD, lease CRUD, escalation, water/electric billing, penalties, billing run wizard, payment recording with Art. 1252-1254 allocation, deposit lifecycle, contract generation wizard, portfolio dashboard, rent roll (26 columns), tax data compilation, 2307 tracking, document registers, ATP management, expense entry. 16 export types identified. |
