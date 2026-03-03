# Deployment — Vercel + Supabase Topology, CI/CD, Environment Config

*Wave 2 Architecture Decision | Depends on: project-structure, database-schema, auth-and-roles, api-layer, compliance-alerts, document-generation*

---

## Decision Summary

**Hosting:** Vercel for the Next.js app (serverless functions + edge network). **Database & Auth:** Supabase (managed Postgres, Auth, Edge Functions, pg_cron). **Email:** Resend (transactional email API). **CI/CD:** GitHub Actions for lint/test/typecheck on PRs, Vercel auto-deploys on merge to `main`. Three environments: local dev (Supabase CLI), preview (Vercel preview + Supabase staging project), production (Vercel + Supabase production project). Drizzle migrations applied via CI before deployment.

---

## 1. Hosting Platform Selection

### 1.1 Options Evaluated

| Platform | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Vercel** | Native Next.js host, zero-config Turborepo support, automatic preview deploys, generous free tier, global edge network, serverless functions | 50MB function size limit (no Chromium), 10s default timeout (extendable to 60s on Pro), vendor lock-in for edge features | **Selected** |
| Railway | Docker-based, no function size limits, persistent servers, pg_cron support, good for long-running processes | Manual Next.js config, no automatic preview deploys, less Next.js-optimized | Rejected |
| Fly.io | Docker-based, global edge, persistent VMs | More operational overhead, manual scaling, no built-in preview deploys | Rejected |
| Self-hosted (VPS) | Full control, cheapest at scale | Operational burden for a 2-user app, no auto-scaling, manual TLS | Rejected |

### 1.2 Why Vercel

1. **Native Next.js integration.** Vercel is the company behind Next.js. Build optimization, ISR, RSC streaming, Turbopack — all work without configuration. For a forward loop building the app feature-by-feature, zero-config deployment removes an entire failure category.

2. **Turborepo integration.** Vercel detects the Turborepo root and only rebuilds affected packages on each push. Build caching across deployments reduces CI time from minutes to seconds for incremental changes.

3. **Preview deployments.** Every PR gets a unique URL (`<branch>.vercel.app`). Combined with the Supabase staging project, this enables end-to-end review of each feature before merge.

4. **Serverless function model fits the workload.** This is a 2-user backoffice app. Request volume is negligible — serverless cold starts are acceptable. No need for persistent servers.

5. **No Chromium dependency.** The PDF generation decision (`@react-pdf/renderer`, not Puppeteer) was partially motivated by Vercel's 50MB uncompressed function size limit. This constraint is already satisfied.

### 1.3 Vercel Plan

**Free tier is sufficient for MVP.** Limits:

| Resource | Free Tier | This App's Usage |
|----------|-----------|-----------------|
| Bandwidth | 100 GB/month | <1 GB (2 users) |
| Serverless invocations | 100K/month | <5K (2 users, ~100 requests/day) |
| Function size | 50MB uncompressed | ~30MB (Next.js + @react-pdf/renderer) |
| Function duration | 10s (default) | Sufficient for all routes (PDF render <1s, batch ZIP <5s) |
| Build minutes | 6000/month | ~200 (Turbo-cached incremental builds) |
| Preview deployments | Unlimited | Yes |
| Team members | 1 | 1 (deploy account) |

If the free tier's 10s function timeout is hit during batch PDF ZIP generation (100 invoices), upgrade to Pro ($20/month) for 60s timeout. But for ~50 tenants, batch ZIP completes in <5s.

---

## 2. Supabase Configuration

### 2.1 Supabase Project Structure

Two Supabase projects (not one) — staging and production:

| Project | Purpose | Database | Auth | Edge Functions |
|---------|---------|----------|------|----------------|
| `tsvj-staging` | Preview + dev shared DB | Supabase free tier | Enabled | Deployed |
| `tsvj-production` | Production | Supabase Pro ($25/month) | Enabled | Deployed |

**Why Supabase Pro for production:** The free tier has a 500MB database limit and pauses after 1 week of inactivity. For a backoffice app that receives daily pg_cron jobs, the inactivity pause would break the compliance alert system. Pro provides 8GB database, no pause, daily backups, and 7-day PITR (Point-in-Time Recovery).

### 2.2 Supabase Services Used

| Service | Purpose | Configured By |
|---------|---------|---------------|
| **Postgres** | Primary database (Drizzle ORM) | Connection string via `DATABASE_URL` |
| **Auth** | Email/password authentication, JWT | Supabase client libraries |
| **Edge Functions** | Alert email digest (Resend integration) | `supabase/functions/send-alert-emails/` |
| **pg_cron** | Daily alert generation + lease lifecycle | SQL migration (enabled on Pro) |
| **pg_net** | HTTP calls from pg_cron to Edge Functions | SQL migration (enabled on Pro) |
| **Realtime** | Not used | Disabled |
| **Storage** | Not used (PDFs generated on-demand) | Disabled |

### 2.3 pg_cron Availability

pg_cron is available on all Supabase paid plans. On the free tier, pg_cron is NOT available — the daily alert job and lease lifecycle transitions will not run.

**Implication for staging:** The staging project (free tier) will not have pg_cron. To test the daily job during development:
- Use `settings.runLifecycleCheck` tRPC mutation (manually triggers `process_daily_alerts()`)
- Or upgrade staging to Pro if automated testing of cron jobs is needed

**Implication for production:** Production MUST be on a paid Supabase plan (Pro $25/month) for pg_cron and pg_net.

### 2.4 Connection Pooling

Supabase provides built-in PgBouncer (connection pooler). Configuration:

```
# Direct connection (for migrations, seed scripts — NOT for the app)
DIRECT_DATABASE_URL=postgresql://postgres:[password]@db.[ref].supabase.co:5432/postgres

# Pooled connection (for the Next.js app — used in all tRPC requests)
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?pgbouncer=true
```

**Why pooled for the app:** Vercel serverless functions spin up/down independently. Without pooling, each function invocation opens a new Postgres connection. PgBouncer pools connections, preventing connection exhaustion. The `?pgbouncer=true` flag disables prepared statements (required for PgBouncer in transaction mode).

**Why direct for migrations:** `drizzle-kit push` and `drizzle-kit migrate` require direct connections (prepared statements, schema introspection).

---

## 3. Environment Configuration

### 3.1 Environment Variables

```bash
# .env.example (committed to repo — no secrets)

# === Supabase ===
NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# Server-only
SUPABASE_SERVICE_ROLE_KEY=eyJ...
DATABASE_URL=postgresql://postgres.<ref>:<password>@aws-0-<region>.pooler.supabase.com:6543/postgres?pgbouncer=true
DIRECT_DATABASE_URL=postgresql://postgres:<password>@db.<ref>.supabase.co:5432/postgres

# === Resend (email) ===
RESEND_API_KEY=re_...

# === App ===
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 3.2 Variable Sources by Environment

| Variable | Local Dev | Vercel Preview | Vercel Production |
|----------|-----------|---------------|-------------------|
| `NEXT_PUBLIC_SUPABASE_URL` | `.env.local` (local Supabase CLI) | Vercel env var (staging project) | Vercel env var (production project) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `.env.local` | Vercel env var | Vercel env var |
| `SUPABASE_SERVICE_ROLE_KEY` | `.env.local` | Vercel env var | Vercel env var |
| `DATABASE_URL` | `.env.local` (local DB, pooled) | Vercel env var (staging, pooled) | Vercel env var (production, pooled) |
| `DIRECT_DATABASE_URL` | `.env.local` (local DB, direct) | GitHub Actions secret (staging) | GitHub Actions secret (production) |
| `RESEND_API_KEY` | `.env.local` (test key) | Vercel env var | Vercel env var |
| `NEXT_PUBLIC_APP_URL` | `http://localhost:3000` | Vercel auto-set (`VERCEL_URL`) | `https://tsvj.app` (custom domain) |

### 3.3 Vercel Environment Variable Scopes

Vercel supports scoping env vars to environments (Production, Preview, Development):

| Variable | Production | Preview | Development |
|----------|:----------:|:-------:|:-----------:|
| `NEXT_PUBLIC_SUPABASE_URL` | prod project | staging project | — (use .env.local) |
| `SUPABASE_SERVICE_ROLE_KEY` | prod key | staging key | — |
| `DATABASE_URL` | prod pooled URL | staging pooled URL | — |
| `RESEND_API_KEY` | production key | test key | — |

This ensures preview deployments use the staging Supabase project, never production.

---

## 4. Local Development Setup

### 4.1 Supabase CLI Local Development

Supabase CLI runs a full Supabase stack locally (Postgres, Auth, Edge Functions, Studio):

```bash
# One-time setup
supabase init                    # Already done (supabase/ directory exists)
supabase start                   # Starts local Postgres, Auth, Studio

# Local connection details (output by supabase start)
# API URL:   http://127.0.0.1:54321
# DB URL:    postgresql://postgres:postgres@127.0.0.1:54322/postgres
# Anon Key:  eyJ... (local)
# Service Key: eyJ... (local)
```

### 4.2 Local .env.local

```bash
# apps/web/.env.local (git-ignored, created from .env.example)
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<local anon key from supabase start>
SUPABASE_SERVICE_ROLE_KEY=<local service key from supabase start>
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres
DIRECT_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres
RESEND_API_KEY=re_test_...
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 4.3 Development Workflow

```bash
# Terminal 1: Start Supabase (local Postgres + Auth)
supabase start

# Terminal 2: Push schema to local DB + seed
pnpm db:push && pnpm db:seed

# Terminal 3: Start Next.js dev server (Turbopack)
pnpm dev
```

The dev server runs at `http://localhost:3000`. Supabase Studio (local database admin) at `http://127.0.0.1:54323`.

### 4.4 Supabase CLI Config

```toml
# supabase/config.toml (key sections)

[auth]
enabled = true
site_url = "http://localhost:3000"

[auth.email]
enable_signup = false
enable_confirmations = false   # Skip email confirmation in dev

[auth.sessions]
timebox = "24h"
inactivity_timeout = "8h"

[db]
major_version = 15

[db.seed]
enabled = true
sql_paths = ["./seed.sql"]
```

---

## 5. CI/CD Pipeline

### 5.1 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Developer pushes branch / opens PR                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           ▼                       ▼
┌─────────────────────┐  ┌──────────────────────┐
│  GitHub Actions      │  │  Vercel               │
│  (CI: lint, test,    │  │  (CD: build + deploy) │
│   typecheck,         │  │                       │
│   schema check)      │  │  Preview deploy on PR │
│                      │  │  Production deploy on │
│  Runs on: PR open,   │  │  merge to main        │
│  push to PR branch   │  │                       │
└──────────┬──────────┘  └──────────────────────┘
           │
           ▼ (on merge to main)
┌─────────────────────┐
│  GitHub Actions      │
│  (CD: run migrations │
│   against production │
│   DB before Vercel   │
│   deploy completes)  │
└─────────────────────┘
```

### 5.2 CI Workflow: Pull Request Checks

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      - name: Typecheck
        run: pnpm typecheck

      - name: Lint
        run: pnpm lint

      - name: Test (computations)
        run: pnpm --filter @tsvj/computations test

      - name: Test (db)
        run: pnpm --filter @tsvj/db test
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

      - name: Test (web)
        run: pnpm --filter web test
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.STAGING_SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.STAGING_SUPABASE_ANON_KEY }}
          SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.STAGING_SUPABASE_SERVICE_ROLE_KEY }}

      - name: Schema consistency check
        run: pnpm --filter @tsvj/db drizzle-kit check
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

      - name: Build
        run: pnpm build
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.STAGING_SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.STAGING_SUPABASE_ANON_KEY }}
```

### 5.3 CD Workflow: Database Migrations

Database migrations must run BEFORE the new application code deploys. Otherwise, the app may reference schema changes that don't exist yet.

```yaml
# .github/workflows/migrate.yml
name: Migrate

on:
  push:
    branches: [main]
    paths:
      - 'packages/db/**'

jobs:
  migrate-production:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      - name: Run migrations
        run: pnpm --filter @tsvj/db drizzle-kit migrate
        env:
          DATABASE_URL: ${{ secrets.PRODUCTION_DIRECT_DATABASE_URL }}

      - name: Seed (if needed)
        run: pnpm db:seed
        env:
          DATABASE_URL: ${{ secrets.PRODUCTION_DATABASE_URL }}
```

**Timing:** The migration workflow triggers on push to `main` when `packages/db/` changes. Vercel's build takes 1-3 minutes; the migration runs in <30 seconds. Migrations complete before the new deployment goes live.

**Rollback strategy:** Drizzle-kit generates both up and down migration SQL. If a migration fails, the workflow fails and Vercel's deployment is blocked (GitHub status check). Manual rollback: run the down migration against production.

### 5.4 Vercel Configuration

```json
// vercel.json (root)
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "buildCommand": "pnpm build",
  "installCommand": "pnpm install",
  "framework": "nextjs",
  "outputDirectory": "apps/web/.next"
}
```

Vercel auto-detects the Turborepo setup and only rebuilds affected packages. The `buildCommand` runs the Turborepo `build` task, which builds all dependencies in order.

### 5.5 Branch Strategy

Simple trunk-based development for a solo developer + forward loop:

```
main (production)
  └── feature/<feature-id>  (e.g., feature/F0, feature/P1)
        └── PR → main
```

Each forward loop iteration creates a feature branch, implements the spec, opens a PR, and merges to `main` after CI passes. The feature branch is deleted after merge.

---

## 6. Database Migration Workflow

### 6.1 Development (Schema-First)

```bash
# 1. Edit Drizzle schema files in packages/db/src/schema/
# 2. Push changes to local DB (no migration files)
pnpm db:push

# 3. If schema looks good, generate migration files
pnpm --filter @tsvj/db drizzle-kit generate

# 4. Review generated SQL in packages/db/drizzle/
# 5. Commit migration files + schema changes
```

### 6.2 Production (Migration-File-Based)

```bash
# CI runs on merge to main:
pnpm --filter @tsvj/db drizzle-kit migrate
# This applies all pending migration files from packages/db/drizzle/
```

### 6.3 Custom SQL Migrations

Some database objects are not managed by Drizzle (materialized views, pg_cron jobs, PL/pgSQL functions). These are managed via custom SQL migration files:

```
packages/db/drizzle/
├── 0000_init.sql                     # Drizzle-generated (tables, enums, indexes)
├── 0001_add_water_billing.sql        # Drizzle-generated
├── ...
├── custom/
│   ├── 001_tenant_balance_view.sql   # Materialized view
│   ├── 002_process_daily_alerts.sql  # PL/pgSQL function
│   ├── 003_cron_setup.sql            # pg_cron schedule
│   └── 004_partial_indexes.sql       # Partial indexes (raw SQL)
```

Custom migrations are applied in order after Drizzle migrations. The CI workflow runs both:

```bash
pnpm --filter @tsvj/db drizzle-kit migrate
pnpm --filter @tsvj/db run migrate:custom  # Applies custom/*.sql in order
```

The `migrate:custom` script uses `postgres.js` to execute each SQL file sequentially with idempotent checks (`CREATE OR REPLACE FUNCTION`, `CREATE INDEX IF NOT EXISTS`, etc.).

---

## 7. Supabase Edge Function Deployment

### 7.1 Edge Function: `send-alert-emails`

Deployed via Supabase CLI:

```bash
supabase functions deploy send-alert-emails --project-ref <ref>
```

### 7.2 Edge Function Environment Variables

Set via Supabase Dashboard or CLI:

```bash
supabase secrets set RESEND_API_KEY=re_... --project-ref <ref>
```

The Edge Function also needs the Supabase service role key to query the `alert` table. This is automatically available in Edge Functions via `Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")`.

### 7.3 Edge Function CI/CD

Edge Functions are deployed separately from the Next.js app. A dedicated GitHub Actions workflow handles this:

```yaml
# .github/workflows/edge-functions.yml
name: Deploy Edge Functions

on:
  push:
    branches: [main]
    paths:
      - 'supabase/functions/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: supabase/setup-cli@v1
        with:
          version: latest

      - run: supabase functions deploy send-alert-emails --project-ref ${{ secrets.SUPABASE_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
```

---

## 8. Domain & DNS

### 8.1 Custom Domain

Production URL: `https://tsvj.app` (or `https://app.tsvj.ph` — depending on domain availability).

Configured in Vercel:
1. Add custom domain in Vercel Dashboard
2. Set DNS records (CNAME or A record) pointing to Vercel
3. Vercel auto-provisions TLS certificate via Let's Encrypt

### 8.2 Supabase Custom Domain (Optional)

Supabase custom domains (`auth.tsvj.app` instead of `<ref>.supabase.co`) are available on Pro plan. Not required for MVP — the default Supabase URL works. Consider for production polish if cookies need to be same-origin.

---

## 9. Monitoring & Error Tracking

### 9.1 Decision: Vercel Built-in + Supabase Dashboard (No External APM for MVP)

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Vercel Analytics + Logs | Built-in, zero config, function logs, web vitals | Limited retention (free: 1h, Pro: 3 days) | **Selected for MVP** |
| Sentry | Rich error tracking, source maps, performance | Additional dependency, $26/month | Deferred to post-MVP |
| Supabase Dashboard | Database metrics, auth logs, Edge Function logs | Limited to Supabase services | **Selected for MVP** |
| Axiom / BetterStack | Log aggregation, alerts | External service, cost | Deferred |

### 9.2 What's Monitored

| Concern | Tool | What to Watch |
|---------|------|---------------|
| Serverless function errors | Vercel Logs | 500 errors, timeouts, unhandled exceptions |
| Build failures | GitHub Actions | CI failures, migration errors |
| Database health | Supabase Dashboard | Connection count, query latency, disk usage |
| Auth events | Supabase Dashboard (Auth logs) | Failed logins, token refresh failures |
| Edge Function errors | Supabase Dashboard (Functions logs) | Email send failures |
| pg_cron job failures | Supabase Dashboard (Postgres logs) | `process_daily_alerts()` errors |
| Application errors | Audit log table | Failed mutations, business rule violations |

### 9.3 Health Check Endpoint

A simple health check for uptime monitoring:

```ts
// apps/web/src/app/api/health/route.ts
import { createDbClient } from "@tsvj/db";

export async function GET() {
  try {
    const db = createDbClient(process.env.DATABASE_URL!);
    await db.execute(sql`SELECT 1`);
    return Response.json({ status: "ok", timestamp: new Date().toISOString() });
  } catch {
    return Response.json({ status: "error" }, { status: 503 });
  }
}
```

Can be monitored by a free uptime service (UptimeRobot, Better Uptime free tier) to alert if the app goes down.

---

## 10. Security Hardening

### 10.1 Environment Variable Security

- `SUPABASE_SERVICE_ROLE_KEY` and `DATABASE_URL` are **server-only** — never prefixed with `NEXT_PUBLIC_`
- All secrets stored in Vercel's encrypted environment variables (AES-256)
- GitHub Actions secrets for CI/CD — never logged, never echoed
- `.env.local` is in `.gitignore` — never committed

### 10.2 HTTP Security Headers

Configured in `next.config.ts`:

```ts
// apps/web/next.config.ts
const securityHeaders = [
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
];

const nextConfig = {
  async headers() {
    return [{ source: "/(.*)", headers: securityHeaders }];
  },
};
```

**CSP (Content Security Policy):** Deferred to post-MVP. A strict CSP requires careful allowlisting of Supabase URLs, inline scripts from Next.js hydration, etc. Adding it mid-development creates friction for the forward loop. Add after all features are stable.

### 10.3 Rate Limiting

Not required for MVP (2 users, private backoffice). If exposed to the internet without IP restriction, consider Vercel's Edge Middleware rate limiting or `@upstash/ratelimit`.

### 10.4 Network Access

Supabase Postgres is accessible via the internet by default (with password auth). For production hardening:
- Enable Supabase's network restrictions (allow only Vercel's IP ranges + developer IP)
- Available on Pro plan via Supabase Dashboard → Settings → Network

---

## 11. Cost Estimate

### 11.1 Monthly Costs

| Service | Tier | Monthly Cost | Notes |
|---------|------|:------------:|-------|
| Vercel | Free (or Pro $20) | $0-20 | Free sufficient for 2 users; Pro only if 60s timeout needed for batch ZIP |
| Supabase | Pro | $25 | Required for pg_cron, no-pause, backups, PITR |
| Resend | Free tier | $0 | 3K emails/month (need <50/month) |
| Domain | Annual | ~$2/month | .app or .ph domain |
| **Total** | | **$27-47/month** | |

### 11.2 Scaling Path (If Needed)

This cost structure handles up to ~100 users without changes. Beyond that:
- Vercel Pro handles significant traffic before needing Enterprise
- Supabase Pro handles 8GB database (this app will use <500MB for years)
- Resend free tier handles 3K emails/month

The app would need significant growth beyond a single TSVJ corporation before cost optimization is relevant.

---

## 12. Deployment Checklist for Forward Loop

The forward loop implements F0 (Foundation) first, which includes the full deployment pipeline. This checklist defines what F0 must set up:

### 12.1 One-Time Setup (Before F0)

These are manual steps performed once by the developer (not the forward loop):

1. **Create Supabase projects** — staging + production via Supabase Dashboard
2. **Create Vercel project** — link to GitHub repo, configure environment variables
3. **Register domain** — point DNS to Vercel
4. **Create GitHub secrets** — all `DATABASE_URL`, `SUPABASE_*` variables for CI
5. **Enable pg_cron** — in Supabase Dashboard → Extensions (production project)
6. **Enable pg_net** — in Supabase Dashboard → Extensions (production project)
7. **Create Resend account** — get API key, verify sender domain

### 12.2 F0 Implementation (Forward Loop)

1. Initialize Turborepo monorepo structure
2. Set up `packages/db` with Drizzle schema, generate initial migration
3. Set up `packages/computations` with `decimal.ts` and `Peso` type
4. Set up `packages/ui` with shadcn/ui base components
5. Set up `apps/web` with Next.js, tRPC, Supabase Auth
6. Create `.github/workflows/ci.yml`
7. Create `.github/workflows/migrate.yml`
8. Create `.github/workflows/edge-functions.yml`
9. Create `vercel.json`
10. Create `supabase/config.toml`
11. Create health check endpoint (`/api/health`)
12. Create `next.config.ts` with security headers
13. Verify: `pnpm build` succeeds
14. Verify: `pnpm test` passes
15. Verify: `pnpm lint` passes
16. Verify: deploy to Vercel preview works

---

## 13. Forward Loop Verification

Every feature spec includes deployment-related verification:

```bash
# Build succeeds (Next.js + all packages)
pnpm build

# Lint passes
pnpm lint

# TypeScript compiles
pnpm typecheck

# Schema consistency (Drizzle schema matches migrations)
pnpm --filter @tsvj/db drizzle-kit check
```

These are already included in the CI workflow and run on every PR. The forward loop should run these locally before committing to catch issues early.

---

## 14. Decisions Not Made (Deferred)

| Decision | Reason | When to Decide |
|----------|--------|----------------|
| Content Security Policy | Requires feature-complete app to enumerate all script/style sources | Post-MVP, before public launch |
| Sentry / APM integration | 2 users don't need rich error tracking yet | When errors become hard to diagnose from Vercel logs |
| CDN for static assets | Vercel Edge Network handles this by default | Only if serving from a different CDN |
| Database read replicas | Single Supabase instance handles this load | If read latency becomes an issue |
| Automated E2E tests in CI | Playwright E2E deferred to post-MVP per project-structure decision | After core features stabilize |
| Blue-green deployment | Vercel handles atomic deploys; no manual blue-green needed | Never (Vercel manages this) |
| Supabase Branching | Supabase's per-branch database feature (preview) | If parallel feature development creates migration conflicts |

---

*Decision made: 2026-03-02 | Vercel (free/Pro) for Next.js hosting, Supabase Pro ($25/mo) for Postgres + Auth + pg_cron + Edge Functions, Resend for email, GitHub Actions CI/CD, trunk-based development, ~$27-47/month total cost*
