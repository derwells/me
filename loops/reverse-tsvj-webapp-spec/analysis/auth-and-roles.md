# Auth & Roles — Supabase Auth + tRPC Middleware

*Wave 2 Architecture Decision | Depends on: data-model-extract, ui-requirements-extract, cross-cutting-extract, project-structure, database-schema*

---

## Decision Summary

Supabase Auth with email/password login (no magic links, no OAuth — two known users). User role stored as a custom claim in Supabase Auth metadata (`app_metadata.role`). Role enforcement via tRPC middleware — not RLS. Two middleware guards: `authed` (any logged-in user) and `adminOnly` (rejects accountant). Client-side role propagation via Supabase session + React context (`useRole` hook) + `<RoleGate>` component. No self-registration — admin creates the accountant account via the settings page.

---

## 1. Why Supabase Auth (Not Custom)

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Supabase Auth | Built-in session management, JWT tokens, `auth.users` table, works with Supabase client, free tier covers this | Limited customization; ties auth to Supabase platform | **Selected** |
| NextAuth.js / Auth.js | Flexible providers, middleware-based | Extra dependency, separate session store, doesn't leverage Supabase's auth infra | Rejected |
| Custom JWT | Full control | Significant implementation effort for a 2-user app; reimplements what Supabase provides | Rejected |

**Rationale:** This is a 2-user backoffice app. Supabase Auth's email/password provider is sufficient. The JWT contains the role claim, which the tRPC context extracts on every request. No external OAuth needed — these are internal users with known credentials.

---

## 2. User Role Model

### 2.1 Role Definition

Two roles, no hierarchy (accountant is not a "subset" of admin — they have different views, not fewer views):

| Role | Key | Description |
|------|-----|-------------|
| Admin | `admin` | Property manager. Full CRUD on all entities. Runs billing, records payments, manages leases. |
| Accountant | `accountant` | Read-only access to most entities. Can view, filter, export reports. Cannot create, edit, or delete. |

### 2.2 Role Storage

The role is stored in Supabase Auth's `app_metadata` — a JSONB field on `auth.users` that is **server-writable only** (cannot be changed by the user via the client SDK):

```ts
// When admin creates the accountant user (server-side, via Supabase Admin API):
await supabaseAdmin.auth.admin.updateUserById(userId, {
  app_metadata: { role: "accountant" },
});

// When admin creates their own account (seeded or first setup):
await supabaseAdmin.auth.admin.updateUserById(adminUserId, {
  app_metadata: { role: "admin" },
});
```

**Why `app_metadata` not a custom `user` table:**
1. `app_metadata` is embedded in the JWT — the tRPC context reads it without a DB query on every request.
2. Only 2 users — a separate user profile table adds complexity for zero benefit.
3. `app_metadata` is tamper-proof from the client side (unlike `user_metadata`).

### 2.3 TypeScript Types

```ts
// packages/db/src/schema/system.ts (or a shared types file)
export const APP_ROLES = ["admin", "accountant"] as const;
export type AppRole = (typeof APP_ROLES)[number];

// Zod schema for role validation
import { z } from "zod";
export const appRoleSchema = z.enum(APP_ROLES);
```

---

## 3. Auth Flow

### 3.1 Login

```
User → /login page → email + password → Supabase Auth signInWithPassword()
  → Supabase returns session (access_token JWT + refresh_token)
  → Client stores session in cookie (Supabase SSR helper)
  → Redirect to /dashboard
```

**Implementation: Supabase SSR package (`@supabase/ssr`)**

The `@supabase/ssr` package handles cookie-based session management for Next.js App Router. It provides:
- `createServerClient()` — for Server Components, Route Handlers, and Server Actions
- `createBrowserClient()` — for Client Components

### 3.2 Session Cookie Strategy

```ts
// apps/web/src/lib/supabase/server.ts
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export async function createSupabaseServerClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            cookieStore.set(name, value, options);
          });
        },
      },
    },
  );
}
```

```ts
// apps/web/src/lib/supabase/client.ts
import { createBrowserClient } from "@supabase/ssr";

export function createSupabaseBrowserClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}
```

### 3.3 Middleware (Next.js Route Protection)

Next.js middleware runs on every request and refreshes the Supabase session (prevents stale JWTs):

```ts
// apps/web/src/middleware.ts
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            request.cookies.set(name, value);
            supabaseResponse.cookies.set(name, value, options);
          });
        },
      },
    },
  );

  const { data: { user } } = await supabase.auth.getUser();

  // Redirect unauthenticated users to login
  if (!user && !request.nextUrl.pathname.startsWith("/login")) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    return NextResponse.redirect(url);
  }

  // Redirect authenticated users away from login
  if (user && request.nextUrl.pathname.startsWith("/login")) {
    const url = request.nextUrl.clone();
    url.pathname = "/dashboard";
    return NextResponse.redirect(url);
  }

  return supabaseResponse;
}

export const config = {
  matcher: [
    // Match all routes except static files and API routes handled by tRPC
    "/((?!_next/static|_next/image|favicon.ico|api/trpc).*)",
  ],
};
```

**Note:** This middleware only handles route-level auth (redirects). The actual role-based access control is in the tRPC middleware layer. The Next.js middleware does NOT check roles — it only checks "logged in or not."

---

## 4. tRPC Context & Middleware

### 4.1 Request Context

Every tRPC request extracts the user and role from the Supabase session:

```ts
// apps/web/src/trpc/context.ts
import { createSupabaseServerClient } from "@/lib/supabase/server";
import type { AppRole } from "@tsvj/db";

export async function createTRPCContext() {
  const supabase = await createSupabaseServerClient();
  const { data: { user } } = await supabase.auth.getUser();

  return {
    supabase,
    user,
    role: (user?.app_metadata?.role as AppRole) ?? null,
  };
}

export type TRPCContext = Awaited<ReturnType<typeof createTRPCContext>>;
```

### 4.2 Auth Middleware

Two middleware levels — `authed` (any role) and `adminOnly`:

```ts
// apps/web/src/trpc/middleware.ts
import { TRPCError } from "@trpc/server";
import { initTRPC } from "@trpc/server";
import type { TRPCContext } from "./context";

const t = initTRPC.context<TRPCContext>().create();

// Base: requires authenticated user with a valid role
export const authed = t.middleware(({ ctx, next }) => {
  if (!ctx.user || !ctx.role) {
    throw new TRPCError({ code: "UNAUTHORIZED" });
  }
  return next({
    ctx: {
      ...ctx,
      user: ctx.user,      // Non-null after this point
      role: ctx.role,       // Non-null after this point
    },
  });
});

// Admin-only: rejects accountant role
export const adminOnly = t.middleware(({ ctx, next }) => {
  if (!ctx.user || !ctx.role) {
    throw new TRPCError({ code: "UNAUTHORIZED" });
  }
  if (ctx.role !== "admin") {
    throw new TRPCError({
      code: "FORBIDDEN",
      message: "Admin access required",
    });
  }
  return next({
    ctx: {
      ...ctx,
      user: ctx.user,
      role: ctx.role as "admin",
    },
  });
});

// Procedure builders
export const publicProcedure = t.procedure;
export const protectedProcedure = t.procedure.use(authed);
export const adminProcedure = t.procedure.use(adminOnly);
```

### 4.3 Middleware Usage in Routers

Every tRPC router procedure uses one of the three procedure builders:

```ts
// apps/web/src/routers/tenant.ts
import { adminProcedure, protectedProcedure } from "@/trpc/middleware";
import { z } from "zod";

export const tenantRouter = router({
  // Both roles can list/view
  list: protectedProcedure
    .query(async ({ ctx }) => { /* ... */ }),

  getById: protectedProcedure
    .input(z.object({ id: z.number() }))
    .query(async ({ ctx, input }) => { /* ... */ }),

  // Only admin can create/update/delete
  create: adminProcedure
    .input(tenantCreateSchema)
    .mutation(async ({ ctx, input }) => { /* ... */ }),

  update: adminProcedure
    .input(tenantUpdateSchema)
    .mutation(async ({ ctx, input }) => { /* ... */ }),
});
```

### 4.4 Complete Role-Procedure Mapping

This table maps every tRPC sub-router's procedures to the required role:

| Router | Queries (list/get/export) | Mutations (create/update/delete/run) |
|--------|:------------------------:|:-----------------------------------:|
| `tenant` | `protectedProcedure` | `adminProcedure` |
| `lease` | `protectedProcedure` | `adminProcedure` |
| `property` | `protectedProcedure` | `adminProcedure` |
| `charge-type` | `protectedProcedure` | `adminProcedure` |
| `escalation` | `protectedProcedure` | `adminProcedure` |
| `water` | `protectedProcedure` | `adminProcedure` |
| `electric` | `protectedProcedure` | `adminProcedure` |
| `penalty` | `protectedProcedure` | `adminProcedure` |
| `billing-run` | `protectedProcedure` | `adminProcedure` |
| `payment` | `protectedProcedure` | `adminProcedure` |
| `deposit` | `protectedProcedure` | `adminProcedure` |
| `contract` | `protectedProcedure` | `adminProcedure` |
| `renewal` | `protectedProcedure` | `adminProcedure` |
| `portfolio` | `protectedProcedure` | `adminProcedure` |
| `rent-roll` | `protectedProcedure` | `adminProcedure` (generate/finalize) |
| `tax` | `protectedProcedure` | `adminProcedure` |
| `document` | `protectedProcedure` | `adminProcedure` |
| `expense` | `protectedProcedure` | `adminProcedure` |
| `settings` | `adminProcedure` (all) | `adminProcedure` |
| `compliance` | `protectedProcedure` | `adminProcedure` |
| `alert` | `protectedProcedure` | `protectedProcedure` (dismiss own alerts) |

**Pattern:** All queries use `protectedProcedure` (both roles can read). All mutations use `adminProcedure` (only admin can write). Exception: `settings` is admin-only for reads too (accountant has no reason to see app config). `alert.dismiss` uses `protectedProcedure` because both roles can dismiss their own alerts.

---

## 5. Client-Side Role Enforcement

Server-side middleware is the authoritative guard. Client-side enforcement is for UX only (hiding buttons, disabling forms).

### 5.1 Role Context

```ts
// apps/web/src/hooks/use-role.ts
"use client";

import { createSupabaseBrowserClient } from "@/lib/supabase/client";
import { useEffect, useState } from "react";
import type { AppRole } from "@tsvj/db";

export function useRole(): AppRole | null {
  const [role, setRole] = useState<AppRole | null>(null);

  useEffect(() => {
    const supabase = createSupabaseBrowserClient();
    supabase.auth.getUser().then(({ data: { user } }) => {
      setRole((user?.app_metadata?.role as AppRole) ?? null);
    });
  }, []);

  return role;
}

export function useIsAdmin(): boolean {
  return useRole() === "admin";
}
```

### 5.2 RoleGate Component

Conditionally renders children based on role. Used for hiding create/edit buttons and form sections from accountant:

```tsx
// packages/ui/src/components/composed/role-gate.tsx
"use client";

import { useRole } from "@/hooks/use-role";
import type { AppRole } from "@tsvj/db";

interface RoleGateProps {
  allowed: AppRole[];
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function RoleGate({ allowed, children, fallback = null }: RoleGateProps) {
  const role = useRole();
  if (!role || !allowed.includes(role)) return fallback;
  return children;
}
```

**Usage:**
```tsx
// In a tenant list page
<RoleGate allowed={["admin"]}>
  <Button asChild>
    <Link href="/tenants/new">Add Tenant</Link>
  </Button>
</RoleGate>
```

### 5.3 Sidebar Navigation Filtering

The sidebar hides sections the current role cannot access:

```ts
// apps/web/src/components/layout/sidebar.tsx
const NAV_ITEMS = [
  { label: "Dashboard", href: "/dashboard", roles: ["admin", "accountant"] },
  { label: "Tenants", href: "/tenants", roles: ["admin", "accountant"] },
  { label: "Leases", href: "/leases", roles: ["admin", "accountant"] },
  { label: "Properties", href: "/properties", roles: ["admin", "accountant"] },
  {
    label: "Billing",
    roles: ["admin"],
    children: [
      { label: "Escalation", href: "/billing/escalation" },
      { label: "Water", href: "/billing/water" },
      { label: "Electric", href: "/billing/electric" },
      { label: "Penalties", href: "/billing/penalties" },
      { label: "Billing Runs", href: "/billing/runs" },
    ],
  },
  { label: "Payments", href: "/payments", roles: ["admin", "accountant"] },
  { label: "Deposits", href: "/deposits", roles: ["admin", "accountant"] },
  { label: "Contracts", href: "/contracts", roles: ["admin"] },
  {
    label: "Reports",
    roles: ["admin", "accountant"],
    children: [
      { label: "Rent Roll", href: "/reports/rent-roll" },
      { label: "Tax Data", href: "/reports/tax" },
      { label: "Documents", href: "/reports/documents" },
    ],
  },
  { label: "Expenses", href: "/expenses", roles: ["admin", "accountant"] },
  { label: "Settings", href: "/settings", roles: ["admin"] },
];
```

The sidebar component filters `NAV_ITEMS` by `role` before rendering. The accountant never sees Billing, Contracts, or Settings nav items.

### 5.4 Page-Level Route Protection

Even if the accountant navigates directly to `/billing/water`, the page-level Server Component checks the role:

```tsx
// apps/web/src/app/(app)/billing/water/page.tsx
import { createSupabaseServerClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";

export default async function WaterBillingPage() {
  const supabase = await createSupabaseServerClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (user?.app_metadata?.role !== "admin") {
    redirect("/dashboard");
  }

  // ... render page
}
```

This is defense-in-depth. The tRPC middleware is the primary guard; the page redirect prevents the accountant from seeing a page full of "unauthorized" errors.

---

## 6. User Management

### 6.1 Admin Creates Accountant

No self-registration. The admin creates the accountant account via the Settings > Users page:

```
Admin navigates to /settings/users
  → Fills in email + temporary password
  → Selects role: "accountant"
  → Submits
  → tRPC settings.createUser mutation:
      1. Calls supabaseAdmin.auth.admin.createUser({ email, password, app_metadata: { role } })
      2. Returns success
  → Accountant receives email or admin shares credentials manually
```

**Supabase Admin Client (server-side only):**

```ts
// apps/web/src/lib/supabase/admin.ts
import { createClient } from "@supabase/supabase-js";

// Uses SUPABASE_SERVICE_ROLE_KEY — NEVER exposed to client
export const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
);
```

This client is only used in the `settings` tRPC router (which is `adminProcedure`-protected).

### 6.2 Initial Setup (Seed)

On first deployment, the admin account is created via Supabase Dashboard or a seed script:

```bash
# Via Supabase CLI (local dev)
supabase auth admin create-user \
  --email admin@tsvj.ph \
  --password <temp-password> \
  --data '{"role": "admin"}'
```

Or via the seed SQL:

```sql
-- supabase/seed.sql
-- Note: This uses Supabase's auth.users table directly (dev only)
INSERT INTO auth.users (
  instance_id, id, aud, role, email,
  encrypted_password, email_confirmed_at,
  raw_app_meta_data, raw_user_meta_data,
  created_at, updated_at
) VALUES (
  '00000000-0000-0000-0000-000000000000',
  gen_random_uuid(), 'authenticated', 'authenticated',
  'admin@tsvj.ph',
  crypt('admin123', gen_salt('bf')),
  now(),
  '{"provider": "email", "providers": ["email"], "role": "admin"}'::jsonb,
  '{}'::jsonb,
  now(), now()
);
```

### 6.3 User List View

The settings page shows both users with ability to:
- Change accountant's password (reset)
- Deactivate accountant (via `supabaseAdmin.auth.admin.updateUserById(id, { ban_duration: "876000h" })`)
- No role change UI needed — roles are fixed at creation

---

## 7. Audit Trail Integration

Every admin mutation is logged to the `audit_log` table (defined in database-schema analysis §11):

```ts
// In tRPC middleware, after adminProcedure mutations:
async function logAuditEvent(ctx: AdminContext, action: string, entityType: string, entityId: number, details?: unknown) {
  await ctx.db.insert(auditLog).values({
    userId: ctx.user.id,
    action,
    entityType,
    entityId,
    details: details ? JSON.stringify(details) : null,
  });
}
```

The `userId` in audit logs references `auth.users.id` (UUID string from Supabase Auth). No foreign key constraint to `auth.users` — the audit log is intentionally decoupled from the auth system to ensure logs persist even if a user is deleted.

---

## 8. Password Policy & Session Config

### 8.1 Supabase Auth Config

Configured via Supabase Dashboard or `supabase/config.toml`:

```toml
# supabase/config.toml (relevant sections)
[auth]
enabled = true
site_url = "http://localhost:3000"
additional_redirect_urls = ["http://localhost:3000"]

[auth.email]
enable_signup = false          # No self-registration
double_confirm_changes = true
enable_confirmations = false   # Dev: skip email confirmation

[auth.sessions]
timebox = "24h"                # Session duration
inactivity_timeout = "8h"     # Idle timeout
```

**`enable_signup = false`** is critical — prevents anyone from creating an account via the Supabase client. Only the admin can create users via the service role key.

### 8.2 Password Constraints

Supabase Auth enforces a minimum 6-character password by default. For a 2-user backoffice, this is acceptable. If stronger policy is needed, validate in the `settings.createUser` mutation before calling the Supabase Admin API.

---

## 9. Environment Variables

```bash
# .env.local (apps/web)

# Public — embedded in client bundle
NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...  # anon key (safe to expose)

# Private — server-side only
SUPABASE_SERVICE_ROLE_KEY=eyJ...       # admin key (NEVER expose to client)
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres?pgbouncer=true
```

The `SUPABASE_SERVICE_ROLE_KEY` is used only in:
1. `apps/web/src/lib/supabase/admin.ts` — user management
2. Never imported in client components

---

## 10. Security Considerations

### 10.1 Defense in Depth

Four layers of access control, each independent:

| Layer | What It Checks | Failure Mode |
|-------|---------------|-------------|
| 1. Next.js middleware | Is the user authenticated? | Redirect to `/login` |
| 2. Page-level Server Component | Does the user's role allow this page? | Redirect to `/dashboard` |
| 3. tRPC middleware (`protectedProcedure` / `adminProcedure`) | Is the user authenticated + correct role for this operation? | `UNAUTHORIZED` / `FORBIDDEN` error |
| 4. Client-side `<RoleGate>` + sidebar filtering | Should this UI element be visible? | Hidden (UX only, not a security boundary) |

Layers 1-3 are security boundaries. Layer 4 is UX polish.

### 10.2 No RLS — Justified

The database-schema analysis (§14.3) already decided: no RLS. The rationale applies here too:
- 2 users, 2 roles, simple permission model
- Drizzle ORM doesn't natively manage RLS
- `postgres.js` connects as the `postgres` role (not per-user)
- tRPC middleware is simpler to test and audit

### 10.3 Token Security

- Supabase JWTs are stored in `httpOnly` cookies (via `@supabase/ssr`), not `localStorage`
- `app_metadata.role` is server-side only — the user cannot modify their own role via the client SDK
- The `SUPABASE_SERVICE_ROLE_KEY` bypasses RLS and can create users — never exposed to the client bundle

### 10.4 CSRF Protection

Next.js App Router with Server Actions has built-in CSRF protection (same-origin checks). tRPC over HTTP also benefits from this when called from the Next.js app. No additional CSRF tokens needed.

---

## 11. File Locations Summary

| File | Purpose |
|------|---------|
| `apps/web/src/lib/supabase/server.ts` | Supabase server client factory (cookie-based) |
| `apps/web/src/lib/supabase/client.ts` | Supabase browser client factory |
| `apps/web/src/lib/supabase/admin.ts` | Supabase admin client (service role key) |
| `apps/web/src/middleware.ts` | Next.js middleware (auth redirect) |
| `apps/web/src/trpc/context.ts` | tRPC context (extracts user + role) |
| `apps/web/src/trpc/middleware.ts` | `authed`, `adminOnly` middleware + procedure builders |
| `apps/web/src/hooks/use-role.ts` | Client-side role hook |
| `packages/ui/src/components/composed/role-gate.tsx` | Conditional rendering by role |
| `apps/web/src/components/layout/sidebar.tsx` | Role-filtered navigation |
| `apps/web/src/app/(auth)/login/page.tsx` | Login page |
| `apps/web/src/app/(app)/settings/users/page.tsx` | User management (admin only) |

---

## 12. Forward Loop Implications

### 12.1 F0 (Foundation) Must Include

The F0 feature spec must set up:
1. Supabase SSR client files (`server.ts`, `client.ts`, `admin.ts`)
2. Next.js middleware for auth redirects
3. tRPC context and middleware (`context.ts`, `middleware.ts`)
4. Login page with Supabase `signInWithPassword`
5. Logout action
6. `useRole` hook
7. `<RoleGate>` component
8. Sidebar with role filtering
9. Settings > Users page for admin to create accountant

### 12.2 Every Feature Must

- Use `protectedProcedure` for queries and `adminProcedure` for mutations (unless explicitly exempt per the mapping in §4.4)
- Use `<RoleGate>` to hide create/edit/delete buttons from accountant
- Include admin-only page-level redirect for pages like billing, contracts, settings

### 12.3 Verification

Every feature spec's acceptance criteria must include:
- `- [ ] Accountant role blocked — <mutation> with accountant session returns FORBIDDEN`
- This verifiable criterion prevents forward loop drift on auth enforcement

---

*Decision made: 2026-03-02 | Supabase Auth email/password, app_metadata role claim, tRPC middleware enforcement (authed + adminOnly), no RLS, 4-layer defense-in-depth, admin-only user management*
