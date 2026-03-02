# UI Framework — Next.js App Router, Component Library, Layout Patterns

*Wave 2 Architecture Decision | Depends on: data-model-extract, ui-requirements-extract, cross-cutting-extract, project-structure, auth-and-roles, api-layer*

---

## Decision Summary

Next.js 16 App Router with Tailwind CSS v4 and shadcn/ui (unified Radix package). Server Components as the default rendering model — Client Components only for interactive elements (forms, tables with sorting/filtering, modals). react-hook-form + Zod resolver for all forms. TanStack Table for all data tables (~35 tables across the app). Sheet-based detail panels for quick view, full pages for CRUD. Consistent page layout: breadcrumb → page header → content. All monetary inputs use a `CurrencyInput` composed component. All regime-dependent forms conditionally render fields based on `lease_regime`.

---

## 1. Component Library Decision

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| **shadcn/ui (Radix unified)** | Copy-paste ownership, full customization, Radix accessibility, active ecosystem, Tailwind-native | Must compose complex components yourself | **Selected** |
| Mantine | Rich component set, built-in form support | Opinionated styling, CSS-in-JS overhead, harder to customize deeply | Rejected |
| Ant Design | Comprehensive backoffice components | Heavy bundle, difficult Tailwind integration, opinionated design system | Rejected |
| Headless UI + custom | Lightweight, full control | Much more build work for ~35 tables + ~19 forms, no community components | Rejected |

**Rationale:** shadcn/ui provides the right balance for a backoffice app: production-ready primitives (Dialog, Select, Tabs, Table, Form) that can be customized to match the domain (currency inputs, regime badges, TIN formatting). The February 2026 Radix unified package migration means one `radix-ui` dependency instead of ~20 individual packages. TanStack Table integration is well-documented in shadcn's data-table recipe.

### 1.1 shadcn/ui Components Used

**Base primitives** (from `packages/ui/src/components/ui/`):

| Component | Usage Count (est.) | Primary Use Case |
|-----------|:-----------------:|------------------|
| `Button` | ~100+ | Actions, navigation, form submission |
| `Input` | ~60+ | Text fields, search bars |
| `Select` | ~30+ | Dropdowns (tenant type, status, regime, payment method) |
| `Dialog` | ~15 | Confirmation modals, escalation preview, penalty preview |
| `Table` | ~35 | Data tables (via TanStack Table wrapper) |
| `Tabs` | ~8 | Tenant detail, lease detail, tax dashboard |
| `Card` | ~25 | Dashboard KPI cards, summary cards |
| `Badge` | ~20 | Status badges (lease, billing run, deposit, payment) |
| `Form` | ~19 | All forms (react-hook-form integration) |
| `DatePicker` | ~15 | Date inputs (billing period, lease term, payment date) |
| `Sidebar` | 1 | App shell sidebar (shadcn sidebar component) |
| `Command` | 1 | Quick navigation (Cmd+K palette) |
| `Toast` | global | Success/error notifications |
| `Alert` | ~5 | Inline warnings (VAT conflict, ATP exhaustion, arrears) |
| `Checkbox` | ~10 | Payment allocation checkboxes, billing scope selection |
| `RadioGroup` | ~5 | Tenant type, lease regime, billing scope |
| `Textarea` | ~5 | Notes, descriptions, clause editing |
| `Separator` | ~20 | Section dividers in forms and detail views |
| `Skeleton` | ~10 | Loading states for data tables and detail views |
| `DropdownMenu` | ~10 | Row actions (edit, delete, view), user menu |
| `Sheet` | ~5 | Mobile sidebar, quick-view panels |
| `Progress` | ~3 | ATP utilization bar, monthly close progress |
| `Tooltip` | ~15 | Truncated text, icon explanations |
| `Popover` | ~3 | Alert bell dropdown, date picker popover |
| `ScrollArea` | ~5 | Long lists inside dialogs/sheets |

### 1.2 Composed Components

Domain-specific components built on shadcn primitives. Located in `packages/ui/src/components/composed/`:

| Component | Built On | Purpose |
|-----------|----------|---------|
| `CurrencyInput` | `Input` | PHP currency input with decimal.js formatting; accepts/displays `₱12,345.67`; stores raw numeric string |
| `TINInput` | `Input` | TIN format mask (`###-###-###-###`); validates on blur |
| `PesoDisplay` | `<span>` | Read-only currency display with thousands separator and ₱ prefix |
| `RegimeBadge` | `Badge` | Color-coded lease regime badge (blue=controlled, green=commercial, gray=non-controlled) |
| `StatusBadge` | `Badge` | Generic status badge with color map (per entity type) |
| `RoleGate` | — | Conditional render by role (from auth-and-roles decision) |
| `ExportButton` | `Button` + `DropdownMenu` | CSV/XLSX export trigger with format selection |
| `DataTable` | `Table` + TanStack Table | Full-featured data table (sorting, filtering, pagination, row actions) |
| `EmptyState` | `Card` | "No data" placeholder with icon and action button |
| `ConfirmDialog` | `Dialog` | Confirmation modal with destructive action warning |
| `PageHeader` | — | Page title + breadcrumbs + action buttons pattern |
| `FormSection` | — | Collapsible form section with divider and heading |
| `AlertBanner` | `Alert` | Persistent top-of-page banner for system-wide warnings (VAT config, ATP exhaustion) |

---

## 2. Next.js App Router Structure

### 2.1 Rendering Model

**Default: Server Components.** Every page file (`page.tsx`) is a Server Component that:
1. Checks auth (via `createSupabaseServerClient()`)
2. Checks role (redirect if unauthorized for this page)
3. Prefetches tRPC data via server caller
4. Renders the page shell (breadcrumb, header, layout)
5. Passes interactive portions to Client Components

**Client Components** are used only when the component needs:
- Event handlers (onClick, onChange, onSubmit)
- React hooks (useState, useEffect, useQuery)
- Browser APIs
- tRPC mutations

```
Server Component (page.tsx)
  ├── PageHeader (server — static title + breadcrumbs)
  ├── RoleGate wrapper (client — conditional render)
  └── TenantListClient (client — interactive table with sorting, filtering, pagination)
        ├── DataTable (client — TanStack Table)
        ├── FilterBar (client — search + select filters)
        └── ExportButton (client — triggers download)
```

### 2.2 Route Group Layout

```
src/app/
├── layout.tsx              # Root: <html>, font loading, TRPCProvider, QueryClientProvider
├── page.tsx                # Redirect to /dashboard
├── globals.css             # Tailwind v4 import + CSS variables
│
├── (auth)/                 # Unauthenticated route group
│   ├── layout.tsx          # Centered card layout, no sidebar
│   └── login/
│       └── page.tsx        # Login form (Client Component)
│
├── (app)/                  # Authenticated route group
│   ├── layout.tsx          # Sidebar + Header + AlertBanner + main content area
│   ├── dashboard/
│   │   └── page.tsx        # Dashboard (Server Component + client widgets)
│   ├── tenants/...         # F0
│   ├── leases/...          # F0
│   ├── properties/...      # F0
│   ├── billing/...         # P1-P5
│   ├── payments/...        # P6
│   ├── deposits/...        # P7
│   ├── contracts/...       # P8
│   ├── portfolio/...       # P10
│   ├── reports/...         # P11, P12
│   ├── expenses/...        # P14
│   └── settings/...        # System
│
└── api/
    └── trpc/
        └── [trpc]/route.ts # tRPC HTTP handler
```

### 2.3 `(app)/layout.tsx` — Authenticated Shell

The authenticated layout provides the persistent app shell:

```
┌────────────────────────────────────────────────────────┐
│  AlertBanner (conditionally rendered)                  │
│  "Electric VAT treatment not configured — go to..."    │
├──────────┬─────────────────────────────────────────────┤
│          │  Header                                     │
│          │  ┌─────────────────────────────────────────┐│
│ Sidebar  │  │ Breadcrumbs │         [🔔 3] [Admin ▾] ││
│          │  └─────────────────────────────────────────┘│
│ (collap- │                                             │
│  sible)  │  {children}                                 │
│          │                                             │
│          │                                             │
│          │                                             │
└──────────┴─────────────────────────────────────────────┘
```

**Implementation:**

```tsx
// apps/web/src/app/(app)/layout.tsx
import { createSupabaseServerClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import { SidebarProvider } from "@tsvj/ui";
import { AppSidebar } from "@/components/layout/sidebar";
import { AppHeader } from "@/components/layout/header";
import { AlertBannerServer } from "@/components/layout/alert-banner";

export default async function AppLayout({ children }: { children: React.ReactNode }) {
  const supabase = await createSupabaseServerClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) redirect("/login");

  const role = user.app_metadata?.role as "admin" | "accountant";

  return (
    <SidebarProvider>
      <AppSidebar role={role} />
      <main className="flex-1 flex flex-col min-h-screen">
        <AlertBannerServer />
        <AppHeader />
        <div className="flex-1 p-6">
          {children}
        </div>
      </main>
    </SidebarProvider>
  );
}
```

### 2.4 Sidebar Component

Uses shadcn's `Sidebar` component. Navigation items are role-filtered (from auth-and-roles §5.3):

```tsx
// apps/web/src/components/layout/sidebar.tsx
"use client";

import {
  Sidebar, SidebarContent, SidebarGroup, SidebarGroupLabel,
  SidebarMenu, SidebarMenuItem, SidebarMenuButton, SidebarMenuSub,
  SidebarMenuSubItem, SidebarMenuSubButton,
} from "@tsvj/ui";
import type { AppRole } from "@tsvj/db";

interface NavItem {
  label: string;
  href?: string;
  icon: React.ComponentType;
  roles: AppRole[];
  children?: Array<{ label: string; href: string }>;
}

const NAV_ITEMS: NavItem[] = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard, roles: ["admin", "accountant"] },
  { label: "Tenants", href: "/tenants", icon: Users, roles: ["admin", "accountant"] },
  { label: "Leases", href: "/leases", icon: FileText, roles: ["admin", "accountant"] },
  { label: "Properties", href: "/properties", icon: Building, roles: ["admin", "accountant"] },
  {
    label: "Billing", icon: Receipt, roles: ["admin"],
    children: [
      { label: "Escalation", href: "/billing/escalation" },
      { label: "Water", href: "/billing/water" },
      { label: "Electric", href: "/billing/electric" },
      { label: "Penalties", href: "/billing/penalties" },
      { label: "Billing Runs", href: "/billing/runs" },
    ],
  },
  { label: "Payments", href: "/payments", icon: Banknote, roles: ["admin", "accountant"] },
  { label: "Deposits", href: "/deposits", icon: Shield, roles: ["admin", "accountant"] },
  { label: "Contracts", href: "/contracts", icon: ScrollText, roles: ["admin"] },
  { label: "Portfolio", href: "/portfolio", icon: PieChart, roles: ["admin", "accountant"] },
  {
    label: "Reports", icon: BarChart3, roles: ["admin", "accountant"],
    children: [
      { label: "Rent Roll", href: "/reports/rent-roll" },
      { label: "Tax Data", href: "/reports/tax" },
      { label: "Documents", href: "/reports/documents" },
    ],
  },
  { label: "Expenses", href: "/expenses", icon: CreditCard, roles: ["admin", "accountant"] },
  { label: "Settings", href: "/settings", icon: Settings, roles: ["admin"] },
];

export function AppSidebar({ role }: { role: AppRole }) {
  const filtered = NAV_ITEMS.filter(item => item.roles.includes(role));
  // ... render SidebarMenu with filtered items
}
```

**Icon library:** `lucide-react` (already included with shadcn/ui). Consistent 20×20 icons in sidebar, 16×16 in buttons.

### 2.5 Page Layout Pattern

Every page follows a consistent structure:

```tsx
// Standard page pattern
export default async function TenantsPage() {
  // 1. Auth check
  const supabase = await createSupabaseServerClient();
  const { data: { user } } = await supabase.auth.getUser();

  // 2. Prefetch data
  const caller = await createServerCaller();
  void caller.tenant.list({ limit: 25 });

  // 3. Render
  return (
    <HydrateClient>
      <PageHeader
        title="Tenants"
        breadcrumbs={[{ label: "Tenants" }]}
        actions={
          <RoleGate allowed={["admin"]}>
            <Button asChild>
              <Link href="/tenants/new">Add Tenant</Link>
            </Button>
          </RoleGate>
        }
      />
      <TenantListClient />
    </HydrateClient>
  );
}
```

The `PageHeader` component provides:

```
┌──────────────────────────────────────────────────────────┐
│ Dashboard > Tenants                     [+ Add Tenant]   │
│ ─────────────────────────────────────────────────────────│
│ Manage tenant records and view balances                  │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Form Handling

### 3.1 Form Library Decision

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| **react-hook-form + @hookform/resolvers/zod** | Minimal re-renders, Zod integration (shared schemas with tRPC), shadcn Form component built for it | Learning curve for Controller pattern | **Selected** |
| Formik | Familiar API | More re-renders, Yup-biased, less active | Rejected |
| Conform (server actions) | Progressive enhancement | Server actions add complexity for this use case; tRPC mutations are the transport layer | Rejected |

**Rationale:** react-hook-form is the standard for shadcn/ui forms. The `@hookform/resolvers/zod` package lets the same Zod schemas used in tRPC input validation be reused for client-side form validation — single source of truth for validation rules.

### 3.2 Form Architecture

```
Zod Schema (shared)
    ├── tRPC input validation (server)
    └── react-hook-form resolver (client)

Form Component
    ├── useForm({ resolver: zodResolver(schema), defaultValues })
    ├── FormField → FormItem → FormLabel + FormControl + FormMessage
    └── onSubmit → trpc.entity.create.useMutation()
```

### 3.3 Standard Form Pattern

```tsx
// apps/web/src/components/tenants/tenant-form.tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { trpc } from "@/trpc/client";
import {
  Form, FormField, FormItem, FormLabel, FormControl, FormMessage,
  Input, Button, RadioGroup, RadioGroupItem, Checkbox,
} from "@tsvj/ui";
import { TINInput } from "@tsvj/ui";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

const tenantFormSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  tin: z.string().regex(/^\d{3}-\d{3}-\d{3}(-\d{3})?$/).optional().or(z.literal("")),
  isCorporate: z.boolean(),
  isVatRegistered: z.boolean(),
  contactEmail: z.string().email().optional().or(z.literal("")),
  contactPhone: z.string().optional(),
  address: z.string().optional(),
});

type TenantFormValues = z.infer<typeof tenantFormSchema>;

export function TenantForm({ defaultValues, tenantId }: {
  defaultValues?: Partial<TenantFormValues>;
  tenantId?: number;
}) {
  const router = useRouter();
  const isEdit = !!tenantId;

  const form = useForm<TenantFormValues>({
    resolver: zodResolver(tenantFormSchema),
    defaultValues: {
      name: "",
      isCorporate: false,
      isVatRegistered: false,
      ...defaultValues,
    },
  });

  const createMutation = trpc.tenant.create.useMutation({
    onSuccess(data) {
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
  });

  const updateMutation = trpc.tenant.update.useMutation({
    onSuccess() {
      toast.success("Tenant updated");
      router.push(`/tenants/${tenantId}`);
    },
  });

  function onSubmit(values: TenantFormValues) {
    if (isEdit) {
      updateMutation.mutate({ id: tenantId!, ...values });
    } else {
      createMutation.mutate(values);
    }
  }

  const isCorporate = form.watch("isCorporate");

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6 max-w-2xl">
        {/* FormField components */}
        {/* Conditional corporate fields shown when isCorporate=true */}
      </form>
    </Form>
  );
}
```

### 3.4 Regime-Adaptive Forms

The lease creation form is the most complex form in the app. It adapts required fields and validation based on `lease_regime`:

```
User selects Rentable
  → unit_type auto-determined (RESIDENTIAL or COMMERCIAL)
  → lease_regime auto-suggested (CONTROLLED_RESIDENTIAL if residential + rent ≤ ₱10K)

User confirms/overrides regime
  → Form adapts:
     CONTROLLED_RESIDENTIAL:
       - Escalation: locked to "NHSB Cap" (no other options)
       - Penalty rate: default 1%, max 1% (validated)
       - Grace period: default 5 days, min 5 (validated)
       - Deposit: max 2 months' rent (validated by Zod refine)
       - Advance: max 1 month (validated)
       - Due day: default 5th

     COMMERCIAL:
       - Escalation: all options available (Fixed %, Stepped, CPI, None)
       - Penalty rate: configurable (warn at >3%)
       - Grace period: configurable
       - Deposit: no cap
       - Advance: no cap
       - Due day: configurable
```

**Implementation approach:** A single `LeaseForm` component with conditional rendering driven by `form.watch("leaseRegime")`. Zod validation uses `.superRefine()` to enforce regime-specific constraints:

```ts
const leaseFormSchema = z.object({
  leaseRegime: z.enum(["CONTROLLED_RESIDENTIAL", "NON_CONTROLLED_RESIDENTIAL", "COMMERCIAL"]),
  depositMonths: z.number().min(0),
  advanceMonths: z.number().min(0),
  penaltyRateMonthly: z.number().min(0).max(100),
  gracePeriodDays: z.number().min(0),
  escalationType: z.enum(["NHSB_CAP", "FIXED_PERCENT", "STEPPED", "CPI_LINKED", "NONE"]),
  // ... other fields
}).superRefine((data, ctx) => {
  if (data.leaseRegime === "CONTROLLED_RESIDENTIAL") {
    if (data.depositMonths > 2) {
      ctx.addIssue({ code: "custom", path: ["depositMonths"], message: "Controlled residential: max 2 months deposit (RA 9653)" });
    }
    if (data.advanceMonths > 1) {
      ctx.addIssue({ code: "custom", path: ["advanceMonths"], message: "Controlled residential: max 1 month advance (RA 9653)" });
    }
    if (data.penaltyRateMonthly > 1) {
      ctx.addIssue({ code: "custom", path: ["penaltyRateMonthly"], message: "Controlled residential: max 1%/month (RA 9653 Sec. 7)" });
    }
    if (data.gracePeriodDays < 5) {
      ctx.addIssue({ code: "custom", path: ["gracePeriodDays"], message: "Controlled residential: min 5-day grace period (RA 9653 Sec. 7)" });
    }
    if (data.escalationType !== "NHSB_CAP") {
      ctx.addIssue({ code: "custom", path: ["escalationType"], message: "Controlled residential: only NHSB cap rate escalation allowed" });
    }
  }
});
```

### 3.5 Form Sections

Complex forms (lease, disbursement voucher, billing run) use collapsible `FormSection` components to organize related fields:

```
┌─────────────────────────────────────────┐
│ ▼ Basic Information                     │
│   Tenant: [Select...]                   │
│   Unit(s): [Select...]                  │
│   Regime:  (●) Controlled  (○) Comm.    │
│                                         │
│ ▼ Term & Rent                           │
│   Start: [____]  End: [____]            │
│   Monthly Rate: [₱_____]               │
│   Due Day: [5]                          │
│                                         │
│ ▶ Escalation  (collapsed)              │
│ ▶ Penalties   (collapsed)              │
│ ▶ Deposit & Advance (collapsed)        │
│                                         │
│        [Cancel]  [Save as Draft]        │
└─────────────────────────────────────────┘
```

### 3.6 Toast Notifications

**Library:** `sonner` (recommended by shadcn/ui, zero-config toast).

| Event | Toast Type | Example |
|-------|:----------:|---------|
| Entity created | Success | "Tenant created" |
| Entity updated | Success | "Lease updated" |
| Billing run finalized | Success | "Billing run finalized — 47 invoices generated" |
| Validation error | Error | "Invalid TIN format" |
| Permission denied | Error | "Admin access required" |
| ATP exhaustion warning | Warning | "Invoice ATP at 90% — register new ATP" |
| Network error | Error | "Connection failed — please retry" |

---

## 4. Data Table Pattern

### 4.1 TanStack Table Setup

The `DataTable` composed component wraps TanStack Table v8 with shadcn's `Table` primitive. It supports:

- Column sorting (click header)
- Column visibility toggle (dropdown)
- Search/filter bar
- Cursor-based pagination (Load More or Prev/Next)
- Row actions (dropdown menu per row)
- Row selection (checkbox column, for batch operations)
- Responsive stacking (narrow screens show card layout)

### 4.2 DataTable Component API

```tsx
<DataTable
  columns={tenantColumns}
  data={data?.items ?? []}
  isLoading={isLoading}
  // Pagination
  hasMore={!!data?.nextCursor}
  onLoadMore={() => fetchNextPage()}
  totalCount={data?.totalCount}
  // Filtering
  filterBar={<TenantFilterBar />}
  // Row actions
  onRowClick={(row) => router.push(`/tenants/${row.id}`)}
  // Empty state
  emptyState={
    <EmptyState
      icon={Users}
      title="No tenants"
      description="Create your first tenant to get started."
      action={<Button asChild><Link href="/tenants/new">Add Tenant</Link></Button>}
    />
  }
/>
```

### 4.3 Column Definition Pattern

```tsx
// apps/web/src/components/tenants/columns.tsx
"use client";

import { ColumnDef } from "@tanstack/react-table";
import { PesoDisplay, RegimeBadge, StatusBadge } from "@tsvj/ui";

export const tenantColumns: ColumnDef<TenantListItem>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => (
      <Link href={`/tenants/${row.original.id}`} className="font-medium hover:underline">
        {row.original.name}
      </Link>
    ),
  },
  {
    accessorKey: "tin",
    header: "TIN",
    cell: ({ row }) => row.original.tin ?? "—",
  },
  {
    accessorKey: "isCorporate",
    header: "Type",
    cell: ({ row }) => row.original.isCorporate ? "Corporate" : "Individual",
  },
  {
    accessorKey: "balance",
    header: "Balance",
    cell: ({ row }) => <PesoDisplay amount={row.original.balance} />,
  },
  {
    id: "actions",
    cell: ({ row }) => <TenantRowActions tenant={row.original} />,
  },
];
```

### 4.4 Filter Bar Pattern

Each data table has a corresponding filter bar component:

```tsx
// Filter bar renders above the table
function TenantFilterBar() {
  const [search, setSearch] = useQueryState("search");     // URL query params via nuqs
  const [type, setType] = useQueryState("type");
  const [hasBalance, setHasBalance] = useQueryState("hasBalance");

  return (
    <div className="flex items-center gap-3">
      <Input
        placeholder="Search by name or TIN..."
        value={search ?? ""}
        onChange={(e) => setSearch(e.target.value || null)}
        className="max-w-sm"
      />
      <Select value={type ?? "all"} onValueChange={(v) => setType(v === "all" ? null : v)}>
        <SelectTrigger className="w-[140px]"><SelectValue placeholder="All types" /></SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All types</SelectItem>
          <SelectItem value="individual">Individual</SelectItem>
          <SelectItem value="corporate">Corporate</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}
```

### 4.5 URL State Management

**Library:** `nuqs` — type-safe URL query state for Next.js App Router. Filter/search values persist in the URL, so the page is bookmarkable and shareable.

```ts
import { useQueryState, parseAsString, parseAsBoolean } from "nuqs";

// In filter components:
const [search, setSearch] = useQueryState("q", parseAsString);
const [status, setStatus] = useQueryState("status", parseAsString);
```

**Why `nuqs` over `useSearchParams`:** `nuqs` provides type-safe parsing, shallow routing (no full page reload), and debounce support for search inputs. `useSearchParams` requires manual serialization/deserialization.

---

## 5. Detail View Pattern

### 5.1 Tabbed Detail Layout

Entity detail views (tenant, lease, deposit) use a tabbed layout:

```
┌──────────────────────────────────────────────────────────┐
│  ← Tenants / Juan Cruz                    [Edit] [···]   │
├──────────────────────────────────────────────────────────┤
│  [Overview] [Leases] [Billing] [Payments] [Documents]    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Tab content here                                        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Implementation:** shadcn `Tabs` component. Each tab panel loads its data independently via tRPC queries (lazy loading — data fetched only when tab is activated).

```tsx
// apps/web/src/components/tenants/tenant-detail.tsx
"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@tsvj/ui";

export function TenantDetail({ tenantId }: { tenantId: number }) {
  const { data: tenant } = trpc.tenant.getById.useQuery({ id: tenantId });

  return (
    <Tabs defaultValue="overview" className="space-y-4">
      <TabsList>
        <TabsTrigger value="overview">Overview</TabsTrigger>
        <TabsTrigger value="leases">Leases</TabsTrigger>
        <TabsTrigger value="billing">Billing</TabsTrigger>
        <TabsTrigger value="payments">Payments</TabsTrigger>
        <TabsTrigger value="documents">Documents</TabsTrigger>
      </TabsList>
      <TabsContent value="overview">
        <TenantOverviewTab tenant={tenant} />
      </TabsContent>
      <TabsContent value="leases">
        <TenantLeasesTab tenantId={tenantId} />
      </TabsContent>
      {/* ... */}
    </Tabs>
  );
}
```

### 5.2 Tab Routing

Tabs do NOT use URL-based routing (no `/tenants/123/leases` route). Tabs are client-side state within the detail page. This keeps the route structure flat and avoids unnecessary route segments.

**Exception:** The dashboard tabs (if any) use URL-based routing because they represent distinct data views.

---

## 6. Multi-Step Wizards

Three features use multi-step wizard flows:

1. **Billing Run** (P5): Select period → Review charges → Confirm/Finalize
2. **Contract Generation** (P8): Select lease → Choose template → Review clauses → Preview → Generate
3. **Record Payment** (P6): Select tenant → Enter amount → Review allocation → Confirm

### 6.1 Wizard Pattern

Wizards are single-page Client Components with step state:

```tsx
"use client";

export function BillingRunWizard() {
  const [step, setStep] = useState(1);
  const [data, setData] = useState<WizardData>({});

  return (
    <div>
      <WizardStepIndicator currentStep={step} totalSteps={3} labels={["Select Period", "Review", "Confirm"]} />

      {step === 1 && (
        <SelectPeriodStep
          onNext={(periodData) => { setData({ ...data, ...periodData }); setStep(2); }}
        />
      )}
      {step === 2 && (
        <ReviewChargesStep
          data={data}
          onBack={() => setStep(1)}
          onNext={(reviewData) => { setData({ ...data, ...reviewData }); setStep(3); }}
        />
      )}
      {step === 3 && (
        <ConfirmStep data={data} onBack={() => setStep(2)} />
      )}
    </div>
  );
}
```

### 6.2 WizardStepIndicator Component

```
Step 1           Step 2           Step 3
  ●─────────────────○─────────────────○
Select Period    Review Charges    Confirm
```

Uses `cn()` for active/inactive/completed styling. Located in `packages/ui/src/components/composed/wizard-step-indicator.tsx`.

---

## 7. Dashboard Layout

### 7.1 Grid System

The dashboard uses CSS Grid for responsive card layout:

```
Desktop (≥1024px):
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ KPI Card│ │ KPI Card│ │ KPI Card│ │ KPI Card│
└─────────┘ └─────────┘ └─────────┘ └─────────┘
┌───────────────────────┐ ┌──────────────────────┐
│ Revenue Summary       │ │ Collection Rate      │
└───────────────────────┘ └──────────────────────┘
┌────────────────────────────────────────────────┐
│ Upcoming Deadlines                             │
└────────────────────────────────────────────────┘
┌───────────────────────┐ ┌──────────────────────┐
│ Arrears Alerts        │ │ Monthly Close        │
└───────────────────────┘ └──────────────────────┘

Tablet (768-1023px): 2-column grid
Mobile (<768px): single column stack
```

```tsx
<div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
  <KPICard title="Active Leases" value={47} icon={FileText} />
  <KPICard title="Expiring (90d)" value={3} icon={Clock} variant="warning" />
  <KPICard title="Month-to-Month" value={5} icon={Repeat} />
  <KPICard title="Vacant Units" value={8} icon={Building} />
</div>
<div className="grid gap-4 grid-cols-1 lg:grid-cols-2 mt-4">
  <RevenueSummaryCard />
  <CollectionRateCard />
</div>
```

### 7.2 KPI Card Component

```tsx
// packages/ui/src/components/composed/kpi-card.tsx
interface KPICardProps {
  title: string;
  value: number | string;
  icon: React.ComponentType;
  description?: string;        // e.g., "3 more than last month"
  variant?: "default" | "warning" | "danger";
  href?: string;               // Click to navigate
}
```

---

## 8. Responsive Design

### 8.1 Breakpoint Strategy

This is a backoffice app primarily used on desktop. Tablet support is secondary. Mobile is out of scope for MVP but the layout should not break.

| Breakpoint | Usage |
|:----------:|-------|
| `<768px` (mobile) | Sidebar collapses to hamburger menu; single-column layout; tables stack to cards |
| `768–1023px` (tablet) | Sidebar persistent but narrow; 2-column grids; tables scroll horizontally |
| `≥1024px` (desktop) | Full sidebar; 4-column KPI grid; tables at full width |

### 8.2 Table Responsiveness

For screens below 768px, the `DataTable` component switches from table layout to a card-based layout where each row becomes a card:

```
Desktop:
│ Name      │ TIN        │ Type       │ Balance    │
│───────────│────────────│────────────│────────────│
│ Juan Cruz │ 123-456-78 │ Individual │ ₱15,200    │

Mobile:
┌────────────────────────────────────┐
│ Juan Cruz                    ₱15,200│
│ TIN: 123-456-78 · Individual       │
└────────────────────────────────────┘
```

This is handled in the `DataTable` component with a `mobileColumns` prop that selects which columns to show and how to format them.

---

## 9. Loading & Error States

### 9.1 Loading

- **Page-level:** Server Components render immediately with prefetched data (no loading spinner for initial page load)
- **Tab-level:** `Skeleton` components match the expected layout while tab data loads
- **Table-level:** `DataTable` shows skeleton rows (shimmer effect) during loading
- **Form submission:** Button shows spinner + "Saving..." text; form inputs disabled during mutation

### 9.2 Error States

- **tRPC query errors:** Inline error message with retry button (via React Query's error state)
- **tRPC mutation errors:** Toast notification (via `onError` callback) + form field errors for Zod validation
- **Page-level errors:** Next.js `error.tsx` boundary with "Something went wrong" message and retry button
- **Not Found:** Next.js `not-found.tsx` with "Entity not found" message

### 9.3 Empty States

Every list page has a contextual empty state:

```tsx
<EmptyState
  icon={Users}
  title="No tenants yet"
  description="Create your first tenant to get started with lease management."
  action={
    <RoleGate allowed={["admin"]}>
      <Button asChild><Link href="/tenants/new">Add Tenant</Link></Button>
    </RoleGate>
  }
/>
```

---

## 10. CSS & Styling

### 10.1 Tailwind CSS v4

Tailwind v4 is used for all styling. Configuration via CSS (not `tailwind.config.ts` — Tailwind v4 uses CSS-based config):

```css
/* apps/web/src/app/globals.css */
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.205 0.042 265.755);
  --color-primary-foreground: oklch(0.985 0.002 247.858);
  --color-destructive: oklch(0.577 0.245 27.325);
  /* ... shadcn theme variables */

  /* Custom app colors */
  --color-regime-controlled: oklch(0.623 0.214 259.815);    /* blue */
  --color-regime-commercial: oklch(0.723 0.191 149.579);    /* green */
  --color-regime-non-controlled: oklch(0.556 0.018 285.938);/* gray */

  --color-status-active: oklch(0.723 0.191 149.579);
  --color-status-expiring: oklch(0.795 0.184 86.047);
  --color-status-month-to-month: oklch(0.623 0.214 259.815);
  --color-status-holdover: oklch(0.577 0.245 27.325);
  --color-status-terminated: oklch(0.439 0.018 285.938);
  --color-status-draft: oklch(0.556 0.018 285.938);

  --color-alert-info: oklch(0.623 0.214 259.815);
  --color-alert-warning: oklch(0.795 0.184 86.047);
  --color-alert-urgent: oklch(0.745 0.177 55.388);
  --color-alert-overdue: oklch(0.577 0.245 27.325);
}
```

### 10.2 Dark Mode

**Not in MVP scope.** The app uses a light theme only. The shadcn theme variables support dark mode if needed later (toggle CSS variables), but no dark mode toggle will be implemented in the forward loop.

### 10.3 Typography

- **Font:** System font stack (`font-sans` in Tailwind — no custom font loading)
- **Headings:** `text-2xl font-semibold` for page titles, `text-lg font-medium` for section headers
- **Body:** `text-sm` default (14px — standard for backoffice data-dense UI)
- **Monospace:** `font-mono text-sm` for TIN, invoice numbers, amounts in tables

---

## 11. Additional UI Libraries

| Library | Purpose | Bundle Impact |
|---------|---------|:------------:|
| `lucide-react` | Icons (sidebar, buttons, empty states) | Tree-shaken, ~1KB per icon |
| `sonner` | Toast notifications | ~5KB |
| `nuqs` | URL query state management for filters | ~3KB |
| `@tanstack/react-table` | Data table engine | ~15KB (already required by shadcn data-table) |
| `react-hook-form` | Form state management | ~9KB |
| `@hookform/resolvers` | Zod resolver for react-hook-form | ~2KB |
| `cmdk` | Command palette (Cmd+K) | ~5KB (bundled with shadcn Command) |
| `date-fns` | Date formatting and manipulation | Tree-shaken, ~2KB per function |
| `xlsx` (SheetJS) | CSV/XLSX export | ~300KB, dynamic import only on export pages |

**Total additional client bundle:** ~42KB (excluding SheetJS which is dynamic-imported). Acceptable for a backoffice app.

**Date library choice: `date-fns` over `dayjs` or `luxon`.** date-fns is tree-shakeable (import only `format`, `parseISO`, `differenceInDays`, etc.), functional (no mutable Date wrappers), and works well with superjson's Date serialization. The app needs ~10 date functions; tree-shaking keeps the bundle impact to ~2-3KB.

---

## 12. Component Organization

### 12.1 File Structure Convention

```
apps/web/src/components/
├── layout/                  # Shell components (sidebar, header, breadcrumbs)
│   ├── sidebar.tsx
│   ├── header.tsx
│   ├── alert-banner.tsx
│   └── breadcrumbs.tsx
│
├── shared/                  # Reusable components not in @tsvj/ui
│   ├── page-header.tsx
│   ├── filter-bar.tsx
│   └── wizard-step-indicator.tsx
│
├── tenants/                 # Feature-specific components
│   ├── tenant-form.tsx
│   ├── tenant-detail.tsx
│   ├── tenant-list-client.tsx
│   ├── tenant-filter-bar.tsx
│   └── columns.tsx          # TanStack Table column definitions
│
├── leases/
│   ├── lease-form.tsx
│   ├── lease-detail.tsx
│   ├── lease-list-client.tsx
│   └── columns.tsx
│
├── billing/
│   ├── escalation/
│   │   ├── escalation-dashboard.tsx
│   │   ├── apply-escalation-dialog.tsx
│   │   └── nhsb-rate-form.tsx
│   ├── water/
│   │   ├── meter-reading-entry.tsx
│   │   ├── water-billing-result.tsx
│   │   └── columns.tsx
│   ├── electric/
│   │   └── ...
│   ├── penalties/
│   │   └── ...
│   └── runs/
│       ├── billing-run-wizard.tsx
│       └── billing-run-detail.tsx
│
├── payments/
│   ├── payment-form.tsx     # Includes allocation UI
│   ├── payment-list-client.tsx
│   ├── balance-dashboard.tsx
│   └── columns.tsx
│
├── deposits/
│   ├── deposit-detail.tsx
│   ├── deduction-form.tsx
│   └── columns.tsx
│
├── contracts/
│   ├── contract-wizard.tsx
│   ├── template-list.tsx
│   ├── milestone-tracker.tsx
│   └── columns.tsx
│
├── reports/
│   ├── rent-roll.tsx        # 26-column table + export
│   ├── tax-dashboard.tsx
│   ├── document-registers.tsx
│   └── columns.tsx
│
├── expenses/
│   ├── disbursement-form.tsx
│   ├── supplier-form.tsx
│   └── columns.tsx
│
├── dashboard/
│   ├── kpi-cards.tsx
│   ├── revenue-summary.tsx
│   ├── collection-rate.tsx
│   ├── upcoming-deadlines.tsx
│   ├── arrears-alerts.tsx
│   └── monthly-close.tsx
│
└── settings/
    ├── user-management.tsx
    ├── app-settings-form.tsx
    ├── atp-management.tsx
    └── compliance-calendar.tsx
```

### 12.2 Naming Conventions

| Pattern | Example | Purpose |
|---------|---------|---------|
| `*-form.tsx` | `tenant-form.tsx` | Create/edit forms |
| `*-detail.tsx` | `tenant-detail.tsx` | Tabbed detail view |
| `*-list-client.tsx` | `tenant-list-client.tsx` | Client-side list with DataTable |
| `*-filter-bar.tsx` | `tenant-filter-bar.tsx` | Filter controls above table |
| `columns.tsx` | `tenants/columns.tsx` | TanStack Table column definitions |
| `*-dialog.tsx` | `apply-escalation-dialog.tsx` | Modal dialog components |
| `*-wizard.tsx` | `billing-run-wizard.tsx` | Multi-step wizard components |
| `*-dashboard.tsx` | `balance-dashboard.tsx` | Dashboard/summary views |

---

## 13. Forward Loop Implications

### 13.1 F0 Must Set Up

1. **shadcn/ui initialization:** `npx shadcn@latest init` in `packages/ui/`, add base components (Button, Input, Select, Dialog, Table, Tabs, Card, Badge, Form, Toast, Sidebar, etc.)
2. **TanStack Table:** `DataTable` composed component with sorting, filtering, pagination
3. **react-hook-form:** Form pattern with Zod resolver
4. **Layout shell:** Sidebar, Header, AlertBanner, PageHeader, Breadcrumbs
5. **Composed components:** CurrencyInput, TINInput, PesoDisplay, RegimeBadge, StatusBadge, RoleGate, ExportButton, EmptyState, ConfirmDialog
6. **Tailwind v4 theme:** CSS variables for regime colors, status colors, alert colors
7. **Toast provider:** sonner setup in root layout
8. **nuqs:** URL state management for filter bars

### 13.2 Each Feature Must

- Use `PageHeader` for page title + breadcrumbs + action buttons
- Use `DataTable` for list views (not raw `<table>` elements)
- Use `react-hook-form` + Zod for all forms
- Use `RoleGate` to hide admin-only actions from accountant
- Use `PesoDisplay` for all monetary values (never raw number formatting)
- Use `StatusBadge` with the correct color map for the entity type
- Use `toast` (sonner) for mutation success/error feedback
- Follow the component naming conventions

### 13.3 Verification Pattern

Each feature spec should include UI-specific acceptance criteria:
- `- [ ] Form validation — submit with empty required field shows inline error message`
- `- [ ] Regime adaptation — selecting CONTROLLED_RESIDENTIAL locks escalation to NHSB_CAP`
- `- [ ] Role gate — accountant sees no [+ Create] button on the list page`
- `- [ ] Table pagination — scrolling past 25 items loads next page via cursor`
- `- [ ] Toast — successful mutation shows success toast`

---

*Decision made: 2026-03-02 | Next.js 16 App Router, shadcn/ui (Radix unified), react-hook-form + Zod, TanStack Table, sonner toasts, nuqs URL state, date-fns, Server Components by default, regime-adaptive forms, consistent page/table/form patterns*
