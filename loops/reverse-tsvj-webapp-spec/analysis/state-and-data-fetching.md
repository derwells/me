# State & Data Fetching — tRPC + React Query Patterns, Optimistic Updates, Cache Invalidation

*Wave 2 Architecture Decision | Depends on: api-layer, ui-framework, project-structure, auth-and-roles*

---

## Decision Summary

React Query (via `@trpc/tanstack-react-query`) is the sole client-side data layer — no Redux, Zustand, or Context for server state. Server Components prefetch data via tRPC server caller; client components consume it via React Query hydration with zero redundant fetches. 30-second stale time, no automatic refetch on window focus (backoffice with 2 users). Optimistic updates only for dismissing alerts and toggling charge type active/inactive — all other mutations use invalidation-based refetch. Form state managed by react-hook-form (not React Query). URL state managed by nuqs. The only global client state is the sidebar open/close toggle (React useState in layout).

---

## 1. State Categories

This app has four categories of state. Each uses a different management approach:

| Category | Examples | Managed By | Rationale |
|----------|----------|------------|-----------|
| **Server state** | Tenant list, lease details, balances | React Query (via tRPC) | Cached, invalidated on mutations, prefetched in RSC |
| **Form state** | Input values, validation errors, dirty tracking | react-hook-form | Uncontrolled inputs, Zod resolver, no global store |
| **URL state** | Filter values, search queries, sort direction | nuqs | Bookmarkable, shareable, survives refresh |
| **UI state** | Sidebar open/close, active tab, wizard step | React useState | Component-local, no persistence needed |

**What this app does NOT have:**
- No global client state store (no Redux, Zustand, Jotai). Server state lives in React Query's cache. Form state lives in react-hook-form. URL state lives in the URL. UI state is component-local. There is nothing left that needs a global store.
- No WebSocket/realtime subscriptions. Two users sharing a backoffice don't need live updates. The 30s stale time + mutation invalidation is sufficient.
- No offline support. This is a desktop backoffice app — always connected.

---

## 2. React Query Configuration

### 2.1 QueryClient Setup

```ts
// apps/web/src/trpc/query-client.tsx
import { QueryClient, defaultShouldDehydrateQuery } from "@tanstack/react-query";

export function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,              // 30s — data doesn't change often for 2 users
        gcTime: 5 * 60_000,             // 5 min garbage collection (keep cache warm for back-nav)
        refetchOnWindowFocus: false,     // No aggressive refetching for backoffice
        refetchOnReconnect: true,        // Do refetch after network recovery
        retry: 1,                        // One retry on network failure, then show error
        retryDelay: 1000,               // 1s delay before retry
      },
      mutations: {
        retry: false,                    // Never auto-retry mutations
      },
      dehydrate: {
        shouldDehydrateQuery: (query) =>
          defaultShouldDehydrateQuery(query) ||
          query.state.status === "pending",  // Dehydrate pending queries for RSC prefetch
      },
    },
  });
}
```

**Why these defaults:**
- **`staleTime: 30_000`:** With ~2 concurrent users, data rarely changes between the time you fetch and the time you view it. 30s prevents unnecessary refetches during navigation (e.g., tenant list → tenant detail → back to list = no refetch if within 30s).
- **`gcTime: 5 * 60_000`:** Keeps cached data for 5 minutes after unmount. This means navigating between pages doesn't trigger fresh fetches for recently-viewed data.
- **`refetchOnWindowFocus: false`:** A property manager switching between tabs doesn't need instant data sync. Manual refresh or mutation invalidation handles staleness.
- **`retry: 1`:** One retry covers transient network blips. More retries would delay error display without benefit.

### 2.2 Singleton QueryClient Pattern

The QueryClient must be a stable singleton on the client (not recreated on each render) but a fresh instance per request on the server (no cross-request cache bleed).

```tsx
// apps/web/src/trpc/client.tsx
"use client";

import { useState } from "react";
import { QueryClientProvider } from "@tanstack/react-query";
import { createTRPCClient, httpBatchLink } from "@trpc/client";
import { createTRPCContext } from "@trpc/tanstack-react-query";
import superjson from "superjson";
import { makeQueryClient } from "./query-client";
import type { AppRouter } from "./router";

export const { TRPCProvider, useTRPC } = createTRPCContext<AppRouter>();

let browserQueryClient: QueryClient | undefined;

function getQueryClient() {
  if (typeof window === "undefined") {
    // Server: always new (no cross-request leaks)
    return makeQueryClient();
  }
  // Browser: singleton
  if (!browserQueryClient) browserQueryClient = makeQueryClient();
  return browserQueryClient;
}

export function Providers({ children }: { children: React.ReactNode }) {
  const queryClient = getQueryClient();

  const [trpcClient] = useState(() =>
    createTRPCClient<AppRouter>({
      links: [
        httpBatchLink({
          url: "/api/trpc",
          transformer: superjson,
          maxURLLength: 2083,
        }),
      ],
    }),
  );

  return (
    <QueryClientProvider client={queryClient}>
      <TRPCProvider trpcClient={trpcClient} queryClient={queryClient}>
        {children}
      </TRPCProvider>
    </QueryClientProvider>
  );
}
```

### 2.3 Server-Side Integration

Server Components use a separate server-side query client + tRPC caller. The dehydrated state is passed to the client via `HydrateClient`:

```tsx
// apps/web/src/trpc/server.tsx
import { createHydrationHelpers } from "@trpc/tanstack-react-query";
import { createCallerFactory } from "@trpc/server";
import { cache } from "react";
import { appRouter } from "./router";
import { createTRPCContext } from "./context";
import { makeQueryClient } from "./query-client";

const createCaller = createCallerFactory(appRouter);

// Per-request caching (React cache deduplicates within a single RSC render)
const getQueryClient = cache(makeQueryClient);
const getCaller = cache(async () => {
  const ctx = await createTRPCContext();
  return createCaller(ctx);
});

export const { trpc: serverTrpc, HydrateClient } = createHydrationHelpers<AppRouter>(
  getCaller,
  getQueryClient,
);
```

**Usage in a Server Component:**

```tsx
// apps/web/src/app/(app)/tenants/page.tsx
import { serverTrpc, HydrateClient } from "@/trpc/server";
import { TenantListClient } from "@/components/tenants/tenant-list-client";

export default async function TenantsPage() {
  // Prefetch — data is serialized into HTML, client picks it up
  void serverTrpc.tenant.list.prefetch({ limit: 25 });
  void serverTrpc.alert.list.prefetch();  // Prefetch alerts for header badge

  return (
    <HydrateClient>
      <TenantListClient />
    </HydrateClient>
  );
}
```

**Key behavior:**
- `serverTrpc.tenant.list.prefetch()` executes the tRPC query server-side and serializes the result into the HTML via `HydrateClient`.
- The client-side `useTRPC().tenant.list.useQuery({ limit: 25 })` in `TenantListClient` finds the data already in the cache — no loading spinner, no duplicate fetch.
- The `void` prefix signals that we intentionally don't `await` the prefetch — they run in parallel and resolve before the component renders.

---

## 3. Query Patterns

### 3.1 List Queries (Cursor-Based Pagination)

All list views use cursor-based pagination. The pattern:

```tsx
// apps/web/src/components/tenants/tenant-list-client.tsx
"use client";

import { useTRPC } from "@/trpc/client";
import { useQueryStates, parseAsString } from "nuqs";
import { useSuspenseQuery } from "@tanstack/react-query";

export function TenantListClient() {
  const trpc = useTRPC();

  // URL-persisted filters
  const [filters] = useQueryStates({
    search: parseAsString,
    type: parseAsString,
  });

  // Initial page (prefetched server-side)
  const { data } = useSuspenseQuery(
    trpc.tenant.list.queryOptions({
      limit: 25,
      search: filters.search ?? undefined,
      isCorporate: filters.type === "corporate" ? true
                 : filters.type === "individual" ? false
                 : undefined,
    }),
  );

  return (
    <DataTable
      columns={tenantColumns}
      data={data.items}
      totalCount={data.totalCount}
      hasMore={!!data.nextCursor}
      // ...
    />
  );
}
```

**Why `useSuspenseQuery`:** When data is prefetched server-side, `useSuspenseQuery` guarantees the data is available synchronously on the client (no loading state needed). If the prefetch is missing (e.g., client-side navigation), Suspense renders the nearest `<Suspense>` fallback. This eliminates the need for manual loading state management on every page.

### 3.2 Suspense Boundary Pattern

Each page layout includes a Suspense boundary:

```tsx
// apps/web/src/app/(app)/tenants/page.tsx
import { Suspense } from "react";
import { DataTableSkeleton } from "@/components/shared/data-table-skeleton";

export default async function TenantsPage() {
  void serverTrpc.tenant.list.prefetch({ limit: 25 });

  return (
    <HydrateClient>
      <PageHeader title="Tenants" />
      <Suspense fallback={<DataTableSkeleton columns={5} rows={10} />}>
        <TenantListClient />
      </Suspense>
    </HydrateClient>
  );
}
```

The `DataTableSkeleton` renders shimmer rows matching the expected table layout. This is shown only on client-side navigation when the data isn't prefetched — server-rendered pages show data immediately.

### 3.3 "Load More" Pagination

List views use a "Load More" button (not traditional page numbers). When clicked, the next page is fetched and appended:

```tsx
"use client";

export function TenantListClient() {
  const trpc = useTRPC();
  const [allItems, setAllItems] = useState<TenantListItem[]>([]);
  const [cursor, setCursor] = useState<number | undefined>(undefined);

  const { data } = useSuspenseQuery(
    trpc.tenant.list.queryOptions({
      limit: 25,
      cursor,
      // ... filters
    }),
  );

  // Append new items when cursor changes
  useEffect(() => {
    if (data) {
      setAllItems(prev =>
        cursor ? [...prev, ...data.items] : data.items
      );
    }
  }, [data, cursor]);

  return (
    <>
      <DataTable columns={tenantColumns} data={allItems} />
      {data.nextCursor && (
        <Button
          variant="outline"
          onClick={() => setCursor(data.nextCursor!)}
        >
          Load More ({data.totalCount - allItems.length} remaining)
        </Button>
      )}
    </>
  );
}
```

**Why "Load More" over infinite scroll or page numbers:**
- **Simplicity:** No intersection observer complexity, no "jump to page 5" with cursor-based pagination.
- **Backoffice context:** Users typically search/filter to find what they need. Scrolling through 100+ records is rare. "Load More" handles the edge case.
- **Cursor-based compatible:** Page numbers require offset-based queries. "Load More" naturally maps to cursor-based.

### 3.4 Detail Queries

Detail pages fetch a single entity by ID:

```tsx
// Server Component page
export default async function TenantDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const tenantId = Number(id);

  void serverTrpc.tenant.getById.prefetch({ id: tenantId });

  return (
    <HydrateClient>
      <Suspense fallback={<DetailSkeleton />}>
        <TenantDetail tenantId={tenantId} />
      </Suspense>
    </HydrateClient>
  );
}

// Client Component
function TenantDetail({ tenantId }: { tenantId: number }) {
  const trpc = useTRPC();
  const { data: tenant } = useSuspenseQuery(
    trpc.tenant.getById.queryOptions({ id: tenantId }),
  );

  return (
    <Tabs defaultValue="overview">
      <TabsContent value="overview">
        <TenantOverview tenant={tenant} />
      </TabsContent>
      <TabsContent value="leases">
        {/* Lazy-loaded: only fetches when tab is clicked */}
        <Suspense fallback={<DataTableSkeleton />}>
          <TenantLeases tenantId={tenantId} />
        </Suspense>
      </TabsContent>
    </Tabs>
  );
}
```

### 3.5 Lazy Tab Loading

Tabs within detail views are lazy-loaded — data is fetched only when the tab is activated. This avoids fetching lease history, billing records, and payment data when the user only wants to see the tenant overview.

**Implementation:** Each tab content is wrapped in its own `<Suspense>` boundary. The tab component uses `useSuspenseQuery` internally, so data fetches when the tab mounts (on first click).

```tsx
function TenantLeases({ tenantId }: { tenantId: number }) {
  const trpc = useTRPC();
  // This query only runs when this component mounts (when tab is clicked)
  const { data } = useSuspenseQuery(
    trpc.lease.list.queryOptions({ tenantId, limit: 25 }),
  );

  return <DataTable columns={leaseColumns} data={data.items} />;
}
```

---

## 4. Mutation Patterns

### 4.1 Standard Mutation with Invalidation

The default pattern for all mutations: execute the mutation, then invalidate affected queries to trigger refetch.

```tsx
function TenantForm({ tenantId }: { tenantId?: number }) {
  const trpc = useTRPC();
  const queryClient = useQueryClient();
  const router = useRouter();

  const createMutation = useMutation(
    trpc.tenant.create.mutationOptions({
      onSuccess(data) {
        // Invalidate list cache — next visit to /tenants refetches
        queryClient.invalidateQueries({ queryKey: trpc.tenant.list.queryKey() });
        toast.success("Tenant created");
        router.push(`/tenants/${data.id}`);
      },
      onError(error) {
        if (error.data?.code === "CONFLICT") {
          form.setError("tin", { message: "A tenant with this TIN already exists" });
        } else {
          toast.error(error.message);
        }
      },
    }),
  );

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit((values) => createMutation.mutate(values))}>
        {/* ... fields ... */}
        <Button type="submit" disabled={createMutation.isPending}>
          {createMutation.isPending ? "Saving..." : "Save"}
        </Button>
      </form>
    </Form>
  );
}
```

**Why invalidation over optimistic updates (for most mutations):**
1. **Correctness:** The server may transform data (compute balances, assign document numbers, apply VAT). The client can't predict the server's response.
2. **Simplicity:** Optimistic updates require rollback logic for every mutation. For a 2-user backoffice where latency isn't critical, the extra ~200ms for a refetch is acceptable.
3. **Mutation then navigate:** Most mutations navigate to a detail page after success (`router.push`). The detail page fetches fresh data anyway.

### 4.2 Cross-Router Invalidation

Some mutations affect data across multiple routers. The complete invalidation map:

```tsx
// Centralized invalidation map — imported by mutation hooks

// payment.create → affects tenant balance, charge statuses, portfolio stats
const paymentCreateInvalidations = (queryClient: QueryClient, trpc: TRPCUtils) => {
  queryClient.invalidateQueries({ queryKey: trpc.payment.list.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.tenant.getBalance.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.tenant.getById.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.portfolio.getSummary.queryKey() });
};

// billingRun.finalize → creates charges, invoices, updates balances
const billingRunFinalizeInvalidations = (queryClient: QueryClient, trpc: TRPCUtils) => {
  queryClient.invalidateQueries({ queryKey: trpc.billingRun.list.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.billingRun.getById.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.tenant.getBalance.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.document.listInvoices.queryKey() });
};

// lease.activate → changes portfolio counts
const leaseActivateInvalidations = (queryClient: QueryClient, trpc: TRPCUtils) => {
  queryClient.invalidateQueries({ queryKey: trpc.lease.list.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.lease.getById.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.portfolio.getSummary.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.portfolio.list.queryKey() });
};

// escalation.run → changes lease rent amount
const escalationRunInvalidations = (queryClient: QueryClient, trpc: TRPCUtils) => {
  queryClient.invalidateQueries({ queryKey: trpc.escalation.list.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.lease.getById.queryKey() });
};

// deposit.apply → creates charges, affects balance
const depositApplyInvalidations = (queryClient: QueryClient, trpc: TRPCUtils) => {
  queryClient.invalidateQueries({ queryKey: trpc.deposit.getById.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.deposit.list.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.tenant.getBalance.queryKey() });
};

// water.finalize / electric.finalize → creates charges
const utilityFinalizeInvalidations = (queryClient: QueryClient, trpc: TRPCUtils) => {
  queryClient.invalidateQueries({ queryKey: trpc.billingRun.list.queryKey() });
  queryClient.invalidateQueries({ queryKey: trpc.tenant.getBalance.queryKey() });
};
```

**Implementation approach:** Each mutation hook includes its invalidations inline. A shared `invalidation-map.ts` file exports helper functions to keep them consistent. Feature specs reference which invalidation helper to use.

### 4.3 Optimistic Updates (Limited Use)

Optimistic updates are used for only two interactions where instant feedback matters and the server response is predictable:

#### Alert Dismissal

```tsx
function AlertList() {
  const trpc = useTRPC();
  const queryClient = useQueryClient();

  const dismissMutation = useMutation(
    trpc.alert.dismiss.mutationOptions({
      onMutate: async ({ id }) => {
        // Cancel outgoing refetches
        await queryClient.cancelQueries({ queryKey: trpc.alert.list.queryKey() });

        // Snapshot previous value
        const previous = queryClient.getQueryData(trpc.alert.list.queryKey());

        // Optimistically remove the alert
        queryClient.setQueryData(
          trpc.alert.list.queryKey(),
          (old: Alert[] | undefined) =>
            old?.filter(a => a.id !== id) ?? [],
        );

        return { previous };
      },
      onError: (_err, _vars, context) => {
        // Rollback on error
        if (context?.previous) {
          queryClient.setQueryData(trpc.alert.list.queryKey(), context.previous);
        }
      },
      onSettled: () => {
        queryClient.invalidateQueries({ queryKey: trpc.alert.list.queryKey() });
      },
    }),
  );

  // ...
}
```

**Why optimistic for alert dismiss:** The user clicks an "X" to dismiss a notification. They expect it to disappear instantly. The server response is always success (dismiss is idempotent). Rollback is trivial (re-show the alert).

#### Charge Type Toggle (is_active)

```tsx
// Toggling a charge type active/inactive — predictable, instant feedback expected
const toggleMutation = useMutation(
  trpc.chargeType.update.mutationOptions({
    onMutate: async ({ id, isActive }) => {
      await queryClient.cancelQueries({ queryKey: trpc.chargeType.list.queryKey() });
      const previous = queryClient.getQueryData(trpc.chargeType.list.queryKey());

      queryClient.setQueryData(
        trpc.chargeType.list.queryKey(),
        (old: ChargeType[] | undefined) =>
          old?.map(ct => ct.id === id ? { ...ct, isActive } : ct) ?? [],
      );

      return { previous };
    },
    onError: (_err, _vars, context) => {
      if (context?.previous) {
        queryClient.setQueryData(trpc.chargeType.list.queryKey(), context.previous);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: trpc.chargeType.list.queryKey() });
    },
  }),
);
```

**Everything else uses invalidation-based refetch.** Mutations like creating a billing run, recording a payment, or generating a contract involve server-side computations that the client cannot predict. Optimistic updates would show incorrect data.

---

## 5. Query Key Management

### 5.1 tRPC Query Keys

tRPC v11 auto-generates query keys based on the procedure path and input. The format:

```
[["tenant", "list"], { input: { limit: 25, search: "juan" } }]
```

This means:
- `trpc.tenant.list.queryKey()` matches ALL tenant.list queries (any input)
- `trpc.tenant.list.queryKey({ limit: 25 })` matches only that specific input
- `trpc.tenant.queryKey()` matches ALL tenant queries (list, getById, getBalance)

### 5.2 Invalidation Granularity

Use broad invalidation by default. Narrow only when performance requires it:

```tsx
// GOOD: Invalidate all tenant queries (simple, correct)
queryClient.invalidateQueries({ queryKey: trpc.tenant.queryKey() });

// GOOD: Invalidate all tenant lists (filter/search variations)
queryClient.invalidateQueries({ queryKey: trpc.tenant.list.queryKey() });

// Rarely needed: Invalidate one specific tenant detail
queryClient.invalidateQueries({
  queryKey: trpc.tenant.getById.queryKey({ id: specificTenantId }),
});
```

**Why broad invalidation:** With ~2 users and ~100 entities, the cost of a few extra refetches is negligible. Narrow invalidation is error-prone (forget to invalidate a specific filter combination = stale data). Broad invalidation is always correct.

---

## 6. Data Flow Architecture

### 6.1 End-to-End Data Flow

```
User Action (click, submit)
  │
  ▼
Client Component
  ├── Query: useSuspenseQuery(trpc.entity.list.queryOptions({...}))
  │     │
  │     ▼
  │   React Query Cache
  │     │ (cache miss or stale)
  │     ▼
  │   httpBatchLink → POST /api/trpc/entity.list
  │     │
  │     ▼
  │   tRPC Handler → middleware(auth, audit) → procedure handler
  │     │
  │     ▼
  │   Drizzle ORM → PostgreSQL → result
  │     │
  │     ▼
  │   superjson serialize → HTTP response → React Query cache → render
  │
  └── Mutation: useMutation(trpc.entity.create.mutationOptions({...}))
        │
        ▼
      POST /api/trpc/entity.create (single, not batched)
        │
        ▼
      tRPC Handler → validate input (Zod) → middleware(admin, audit)
        │
        ▼
      ctx.db.transaction() → insert/update/delete → commit
        │
        ▼
      superjson serialize → HTTP response
        │
        ▼
      onSuccess callback → invalidateQueries → refetch affected queries → re-render
```

### 6.2 Server-Side Prefetch Flow

```
Browser Request → Next.js Server
  │
  ▼
Server Component (page.tsx)
  ├── createSupabaseServerClient() → auth check
  ├── getCaller() → tRPC server caller
  ├── serverTrpc.entity.list.prefetch({...}) → runs query server-side
  │     │
  │     ▼
  │   Drizzle ORM → PostgreSQL → result → dehydrate into QueryClient
  │
  ▼
HydrateClient → serializes dehydrated state into <script> tag
  │
  ▼
Browser receives HTML with embedded data
  │
  ▼
Client Component hydrates → useSuspenseQuery finds data in cache → renders immediately
```

### 6.3 Monetary Value Flow

Monetary values follow a strict string-based pipeline to avoid floating-point errors:

```
PostgreSQL (numeric)
  → Drizzle ORM (string — numeric columns return string in JS)
    → tRPC procedure (string — pass through, no conversion)
      → superjson serialize (string — no transformation needed)
        → Client (string → display via PesoDisplay)
        → Client (string → Decimal for arithmetic via decimal.js)
```

The client never stores monetary values as JavaScript `number`. All arithmetic uses `decimal.js`:

```tsx
import Decimal from "decimal.js";

// Client-side balance computation (for display purposes)
const totalCharges = charges.reduce(
  (sum, c) => sum.plus(new Decimal(c.amount)),
  new Decimal(0),
);

// Display
<PesoDisplay amount={totalCharges.toFixed(2)} />
```

---

## 7. Form Data Flow

### 7.1 Form ↔ tRPC Integration

Forms use react-hook-form with Zod resolver. The form schema matches the tRPC input schema (or is a subset of it):

```
Zod Schema (single source of truth)
  │
  ├── react-hook-form resolver (client-side validation on submit)
  │     │
  │     ▼
  │   form.handleSubmit() → only fires if Zod validation passes
  │     │
  │     ▼
  │   mutation.mutate(values) → POST to tRPC
  │
  └── tRPC .input() validation (server-side re-validation)
        │
        ▼
      Procedure handler (business rules beyond Zod: uniqueness, state checks)
```

### 7.2 Form State is NOT in React Query

react-hook-form manages its own state internally (uncontrolled inputs). Form values are never stored in React Query's cache. This avoids:
- Form input causing React Query cache updates (and trigger refetches)
- Stale cache overwriting user's in-progress edits
- Complex synchronization between form state and server state

The form receives `defaultValues` from a prefetched query, but after that, form state is independent:

```tsx
function EditTenantPage({ tenantId }: { tenantId: number }) {
  const trpc = useTRPC();
  const { data: tenant } = useSuspenseQuery(
    trpc.tenant.getById.queryOptions({ id: tenantId }),
  );

  // defaultValues set once from server data — form is independent after this
  return <TenantForm defaultValues={tenant} tenantId={tenantId} />;
}
```

### 7.3 Mutation Loading States

During mutation, the submit button shows a loading state and inputs are disabled:

```tsx
<Button type="submit" disabled={mutation.isPending}>
  {mutation.isPending ? "Saving..." : "Save"}
</Button>
```

The form stays on-screen during the mutation. On success, it navigates away. On error, it stays and shows the error (toast or field-level).

---

## 8. URL State for Filters

### 8.1 nuqs Integration

All filter/search state is stored in URL query parameters via `nuqs`. This provides:
- **Bookmarkable filters:** `/tenants?search=juan&type=corporate`
- **Back button support:** Browser back restores previous filter state
- **Shareable links:** Admin can share a filtered view with the accountant
- **Server Component compatibility:** URL params are available in Server Components for prefetching

```tsx
// apps/web/src/components/tenants/tenant-filter-bar.tsx
"use client";

import { useQueryStates, parseAsString, parseAsBoolean } from "nuqs";

export function TenantFilterBar() {
  const [filters, setFilters] = useQueryStates({
    search: parseAsString.withDefault(""),
    type: parseAsString,            // "corporate" | "individual" | null (all)
    hasBalance: parseAsBoolean,     // true | false | null (all)
  });

  return (
    <div className="flex items-center gap-3 mb-4">
      <Input
        placeholder="Search by name or TIN..."
        value={filters.search}
        onChange={(e) => setFilters({ search: e.target.value || null })}
        className="max-w-sm"
      />
      <Select
        value={filters.type ?? "all"}
        onValueChange={(v) => setFilters({ type: v === "all" ? null : v })}
      >
        {/* ... options ... */}
      </Select>
    </div>
  );
}
```

### 8.2 Filter → Query Binding

URL filter state drives the tRPC query input:

```tsx
function TenantListClient() {
  const trpc = useTRPC();
  const [filters] = useQueryStates({
    search: parseAsString,
    type: parseAsString,
  });

  const { data } = useSuspenseQuery(
    trpc.tenant.list.queryOptions({
      limit: 25,
      search: filters.search ?? undefined,
      isCorporate: filters.type === "corporate" ? true
                 : filters.type === "individual" ? false
                 : undefined,
    }),
  );

  // When filters change, React Query sees a new queryKey (different input)
  // → fetches fresh data → renders updated list
}
```

**React Query deduplication:** If the user types "jua" then "juan", React Query keeps the "jua" query in cache and fires a new query for "juan". If they delete back to "jua", it hits the cache (within staleTime). No debounce is needed for the query itself — but nuqs provides a `throttleMs` option to reduce URL updates:

```tsx
const [search, setSearch] = useQueryState("search", parseAsString.withOptions({
  throttleMs: 300,  // Debounce URL updates to 300ms
}));
```

---

## 9. Dashboard Data Fetching

The dashboard page prefetches multiple independent queries in parallel:

```tsx
// apps/web/src/app/(app)/dashboard/page.tsx
export default async function DashboardPage() {
  // All prefetches run in parallel (they're independent)
  void serverTrpc.portfolio.getSummary.prefetch();
  void serverTrpc.alert.list.prefetch();
  void serverTrpc.compliance.getCalendar.prefetch({ daysAhead: 30 });
  void serverTrpc.tenant.getBalance.prefetch();  // Aggregate balances

  return (
    <HydrateClient>
      <PageHeader title="Dashboard" />
      <Suspense fallback={<DashboardSkeleton />}>
        <DashboardContent />
      </Suspense>
    </HydrateClient>
  );
}
```

On the client, each dashboard widget fetches its own data independently:

```tsx
function KPICards() {
  const trpc = useTRPC();
  const { data: summary } = useSuspenseQuery(
    trpc.portfolio.getSummary.queryOptions(),
  );

  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
      <KPICard title="Active Leases" value={summary.activeLeases} />
      <KPICard title="Expiring (90d)" value={summary.expiringSoon} variant="warning" />
      <KPICard title="Month-to-Month" value={summary.monthToMonth} />
      <KPICard title="Vacant Units" value={summary.vacantUnits} />
    </div>
  );
}
```

### 9.1 Dashboard Refresh

Dashboard data has the same 30s stale time as everything else. Since the dashboard is the landing page, data is always reasonably fresh (fetched on page load). For manual refresh, a "Refresh" button in the page header invalidates all dashboard queries:

```tsx
function DashboardRefreshButton() {
  const queryClient = useQueryClient();
  const trpc = useTRPC();

  return (
    <Button
      variant="outline"
      size="sm"
      onClick={() => {
        queryClient.invalidateQueries({ queryKey: trpc.portfolio.queryKey() });
        queryClient.invalidateQueries({ queryKey: trpc.alert.queryKey() });
        queryClient.invalidateQueries({ queryKey: trpc.compliance.queryKey() });
      }}
    >
      Refresh
    </Button>
  );
}
```

---

## 10. Batch Link Behavior

### 10.1 Request Batching

`httpBatchLink` batches concurrent tRPC queries into a single HTTP request. This is automatic — no configuration needed per query.

**Typical batch scenarios:**
- **Page load:** A detail page may fire `tenant.getById` + `alert.list` simultaneously → 1 HTTP request
- **Dashboard load:** 4 independent queries → 1 HTTP request
- **Tab switch + alert check:** 2 queries → 1 HTTP request

**Mutations are NOT batched.** Each mutation is a separate HTTP request because:
1. Mutations have side effects — batching complicates error handling (partial success)
2. Mutations are infrequent (1-2/minute) — no batching benefit

### 10.2 Batch Size Limits

```ts
httpBatchLink({
  url: "/api/trpc",
  transformer: superjson,
  maxURLLength: 2083,  // Switch from GET to POST if URL exceeds this
})
```

For GET batch requests, tRPC encodes queries in the URL. If the combined URL exceeds 2083 characters (IE limit), it automatically switches to a POST request. This is transparent to the client code.

---

## 11. Error Handling in Data Fetching

### 11.1 Query Errors

| Error Type | Handling | User Experience |
|------------|----------|-----------------|
| Network error | React Query retries once (1s delay) | Brief loading state → error boundary if retry fails |
| UNAUTHORIZED | tRPC error → redirect to /login | Automatic redirect (Next.js middleware catches first) |
| FORBIDDEN | tRPC error → error boundary | "Access denied" message |
| NOT_FOUND | tRPC error → Next.js not-found() | 404 page |
| Server error | No retry for 5xx in queries (retry: 1 covers transient) | Error boundary with "Something went wrong" + retry button |

### 11.2 Mutation Errors

| Error Type | Handling | User Experience |
|------------|----------|-----------------|
| Zod validation | `error.data.zodError` → set form field errors | Inline field-level error messages |
| BAD_REQUEST (business rule) | `error.message` → toast | "Deposit exceeds max for controlled lease" toast |
| CONFLICT (unique violation) | Specific field error | "A tenant with this TIN already exists" on the TIN field |
| PRECONDITION_FAILED | Toast with explanation | "Billing run already finalized — cannot modify" |
| FORBIDDEN | Toast | "Admin access required" |
| Network/5xx | Toast | "Something went wrong — please try again" |

### 11.3 Error Boundary Configuration

Each route segment has an `error.tsx` that catches unhandled errors:

```tsx
// apps/web/src/app/(app)/tenants/error.tsx
"use client";

export default function TenantError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <h2 className="text-lg font-semibold">Something went wrong</h2>
      <p className="text-muted-foreground mt-2">{error.message}</p>
      <Button onClick={reset} className="mt-4">Try again</Button>
    </div>
  );
}
```

---

## 12. Special Data Fetching Patterns

### 12.1 TenantBalance Materialized View

The `tenant_balance` materialized view is queried like any other table. It's refreshed server-side on payment/charge events (inside the transaction). The client queries it via `tenant.getBalance`:

```tsx
// Dashboard: aggregate balance for all tenants
const { data } = useSuspenseQuery(
  trpc.tenant.getBalance.queryOptions(),
);

// Tenant detail: single tenant balance
const { data } = useSuspenseQuery(
  trpc.tenant.getBalance.queryOptions({ tenantId: 123 }),
);
```

**No special client-side caching for the materialized view.** It's treated like any other query — 30s stale time, invalidated on payment/charge mutations.

### 12.2 Export Data Fetching

Export operations fetch data only on explicit user action (button click), not on page load:

```tsx
function ExportButton({ reportId }: { reportId: number }) {
  const trpc = useTRPC();

  // Query is disabled by default — only runs when refetch() is called
  const exportQuery = useQuery({
    ...trpc.rentRoll.export.queryOptions({ reportId }),
    enabled: false,
  });

  async function handleExport() {
    const result = await exportQuery.refetch();
    if (result.data) {
      const XLSX = await import("xlsx");
      const ws = XLSX.utils.json_to_sheet(result.data.rows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
      XLSX.writeFile(wb, result.data.filename);
    }
  }

  return (
    <Button onClick={handleExport} disabled={exportQuery.isFetching}>
      {exportQuery.isFetching ? "Exporting..." : "Export XLSX"}
    </Button>
  );
}
```

### 12.3 Wizard Multi-Step Data

Wizards (billing run, contract generation, payment recording) accumulate data across steps. This data is stored in component-local `useState` — not in React Query or URL state.

```tsx
function BillingRunWizard() {
  const [wizardData, setWizardData] = useState<WizardData>({
    step: 1,
    period: null,
    selectedTenants: [],
    previewCharges: [],
  });

  // Step 2 fetches a preview of charges (server computation)
  // This IS a React Query query — it's server data
  // But the step/selection state is local
}
```

**Separation:** Server data (previewed charges, computed allocations) is fetched via tRPC queries. User selections (which tenants, which period, which allocation rule) are local state. When the wizard completes, the final mutation sends both.

---

## 13. Performance Characteristics

### 13.1 Query Volume Estimates

| Page | Queries on Load | Batch Requests |
|------|:--------------:|:--------------:|
| Dashboard | 4-5 | 1 |
| Tenant list | 1-2 | 1 |
| Tenant detail | 2 (overview + first tab) | 1 |
| Billing run wizard | 1-3 per step | 1 per step |
| Rent roll | 1 (report) + 1 (export, on click) | 1 |
| Settings | 2-3 | 1 |

Total: ~5-15 queries per page navigation, batched into 1-2 HTTP requests.

### 13.2 Cache Hit Rate

For a 2-user backoffice with 30s stale time:
- **Back navigation:** ~90% cache hit (user returns within 30s)
- **Tab switching:** ~80% cache hit (first tab data still fresh)
- **After mutation:** 0% cache hit (invalidated, refetched)
- **Dashboard return:** ~70% cache hit (data changes infrequently)

### 13.3 Network Payload Sizes

| Query | Typical Response Size |
|-------|:--------------------:|
| Tenant list (25 items) | ~5KB |
| Lease detail | ~3KB |
| Billing run detail (50 charges) | ~15KB |
| Rent roll (100 rows × 26 cols) | ~50KB |
| Dashboard aggregates | ~2KB |
| Export data | ~50-200KB |

All well within reasonable limits. No need for response compression beyond standard gzip/brotli at the HTTP level.

---

## 14. Forward Loop Implications

### 14.1 F0 Must Set Up

1. `apps/web/src/trpc/query-client.tsx` — QueryClient factory with defaults
2. `apps/web/src/trpc/client.tsx` — TRPCProvider with httpBatchLink and superjson
3. `apps/web/src/trpc/server.tsx` — Server caller + HydrateClient for RSC prefetch
4. Root layout wrapping children in `<Providers>`
5. `useSuspenseQuery` pattern in first list page (tenants)
6. `useMutation` with invalidation pattern in first form (tenant create/update)
7. `<Suspense>` boundaries on all data-dependent pages
8. `DataTableSkeleton` component for loading states

### 14.2 Each Feature Must

- Use `useSuspenseQuery` (not `useQuery`) for data displayed on page load
- Use `useQuery` with `enabled: false` only for on-demand fetches (exports, previews)
- Prefetch primary data in the Server Component page via `serverTrpc.X.prefetch()`
- Include cross-router invalidations in mutation `onSuccess` callbacks
- Wrap lazy-loaded tab content in `<Suspense>` boundaries
- Never convert monetary values to `number` — keep as `string`, use `Decimal` for arithmetic
- Use `nuqs` for all filter/search state (not `useState`)

### 14.3 Anti-Patterns to Avoid

- **Do NOT use `useQuery` for page-level data.** Use `useSuspenseQuery` + Suspense boundary. `useQuery` requires manual loading state handling; `useSuspenseQuery` leverages Suspense for a consistent pattern.
- **Do NOT create global state stores.** If you're tempted to use Context or Zustand for server data, use React Query instead. If it's URL state, use nuqs. If it's UI state, use local useState.
- **Do NOT manually set query data after mutations** (except for the two optimistic update cases). Always invalidate and let React Query refetch.
- **Do NOT use `refetchInterval`.** No polling. The daily pg_cron job handles background updates. Users see updates after mutation invalidation or page navigation.

---

*Decision made: 2026-03-02 | React Query via tRPC as sole data layer, useSuspenseQuery + RSC prefetch for zero-loading-spinner page loads, invalidation-based cache updates (optimistic only for alert dismiss + charge type toggle), nuqs for URL filter state, react-hook-form for form state, no global state store, 30s staleTime, httpBatchLink*
