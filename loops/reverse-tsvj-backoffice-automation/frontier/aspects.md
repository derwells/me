# Frontier — Back-Office Automation Survey

## Statistics
- Total aspects discovered: 28
- Analyzed: 12
- Pending: 16
- Convergence: 43%

## Pending Aspects (ordered by dependency)

### Wave 1: Source Acquisition (9 aspects)

- [x] crispina-models — Extract all SQLAlchemy models from tsvjph/crispina: lease, tenant, charge, payment, transaction, charge_type, property, room, rentable. Document fields, relationships, and constraints.
  → `input/crispina-models.md`
- [x] crispina-services — Extract math.py (compound interest), date.py (date splitting), and any other service logic. Document formulas and helper functions.
  → `input/crispina-services.md`
- [x] crispina-water-calculator — Extract the standalone water/ billing calculator. Document its inputs, outputs, rate tables, and billing logic.
  → `input/crispina-water-calculator.md`
- [x] rent-control-rules — Fetch RA 9653, latest NHSB resolution (2024-01), and Civil Code lease articles. Extract: allowable increase caps by rent bracket, deposit limits, advance rent limits, grace period rules.
  → `input/rent-control-rules.md`
- [x] corporate-rental-tax — Fetch BIR rules for SEC-registered rental corporations: RCIT/MCIT, VAT threshold (3M), percentage tax (3%), EWT (5%), DST on leases. Document forms, deadlines, and computation formulas.
  → `input/corporate-rental-tax.md`
- [x] utility-billing-regulations — Fetch Meralco rate schedules and Maynilad sub-metering rules for Las Piñas. Document: rate tiers, allowable markups, billing statement requirements.
  → `input/utility-billing-regulations.md`
- [x] security-deposit-rules — Fetch PH deposit laws: residential controlled (2 months max) vs commercial (no cap). Document: deduction rules, return timeline (30 days), interest obligations, tax treatment.
  → `input/security-deposit-rules.md`
- [x] lease-contract-requirements — Fetch Civil Code lease provisions + corporate requirements: board resolution, secretary's certificate, notarization for >1 year, mandatory clauses, DST on execution.
  → `input/lease-contract-requirements.md`
- [x] accounting-agency-handoff — Research what data a PH external accountant needs monthly/quarterly/annually from a rental corporation: rent roll, 2307 certificates, expense vouchers, bank statements, OR stubs.
  → `input/accounting-agency-handoff.md`

### Wave 2: Process Analysis & Feature Specs (14 aspects)
Depends on Wave 1 data.

**Day-to-day operations (highest priority):**
- [x] tenant-payment-tracking — How to track who has paid, who hasn't, running balances per tenant. Partial payment allocation. Dashboard visibility into payment status across all units.
- [x] monthly-billing-generation — How to generate monthly bills for all tenants: rent + utilities + other charges. Statement format, delivery, due dates.
- [x] rent-escalation-calculation — Annual rent increase computation: NHSB caps for controlled units, contractual % or CPI-linked for commercial. When and how escalation triggers.
- [ ] late-payment-penalties — Penalty computation: residential (capped at 1 month/year) vs commercial (contractual, subject to Art. 1229). Compounding rules, grace periods.
- [ ] water-billing — Meter reading → per-unit consumption → bill. Rate application, common area apportionment, statement generation. Compare Crispina water calculator vs regulatory requirements.
- [ ] electric-billing — Electric bill splitting across units. Sub-metering, Meralco rate application, common area allocation methods (by floor area vs equal split vs actual).
- [ ] security-deposit-lifecycle — Collection at lease start, tracking during lease, deductions at end (itemized), refund with interest (controlled) or per contract (commercial). Tax reclassification on application.

**Contracts & lease management:**
- [ ] lease-contract-generation — Generating new lease contracts: template system, variable substitution, mandatory PH clauses, board resolution reference, notarization tracking. PDF output.
- [ ] lease-renewal-extension — Renewal vs extension vs tacit reconduccion (15 days post-expiry). New DST obligation, deposit top-up, escalation on renewal, holdover penalty rates.
- [ ] lease-status-visibility — Dashboard showing all active leases: tenant, unit, term dates, monthly rate, escalation schedule, upcoming renewals, expiring leases alert.

**Accounting agency handoff:**
- [ ] rent-roll-preparation — Monthly rent roll spreadsheet: tenant, unit, gross rent, VAT, EWT withheld, net collected, OR number, date. Format the accountant expects.
- [ ] tax-data-compilation — Preparing data for BIR quarterly/annual filings: 2307 tracking, gross receipts summary for VAT/percentage tax, EWT summary, DST register.
- [ ] official-receipt-data — Data needed to generate BIR-registered official receipts: sequential numbering, tenant TIN, amount breakdown, VAT component.
- [ ] expense-tracking — Recording disbursements (repairs, maintenance, utilities, permits) with receipts for deduction claims. What the accountant needs for books of accounts.

### Wave 3: Handoff & Integration Analysis (3 aspects)
Depends on Wave 2 data.

- [ ] data-flow-mapping — Map the full pipeline: daily operations → monthly close → accountant handoff → BIR/SEC filings. Identify which Wave 2 processes feed which.
- [ ] process-dependencies — Identify which processes generate data consumed by other processes (e.g., payment tracking feeds rent roll, rent roll feeds tax data).
- [ ] compliance-calendar — Annual calendar of all filing deadlines: BIR monthly/quarterly/annual, SEC GIS/AFS, LGU business permits, RPT, fire safety. Alert triggers.

### Wave 4: Synthesis & Catalog (2 aspects)
Depends on all Wave 3 analysis.

- [ ] catalog-draft — Compile all analyses into output/process-catalog.md. Group by category, include cross-cutting concerns, map dependencies, leave pain/frequency columns blank for owner scoring.
- [ ] catalog-review — Self-review the catalog for completeness: all processes covered, specs are actionable, regulatory citations are accurate, no gaps in the pipeline from operations to filings.

## Recently Analyzed

| # | Aspect | Wave | Output | Date |
|---|---|---|---|---|
| 1 | rent-control-rules | 1 | input/rent-control-rules.md | 2026-02-25 |
| 2 | corporate-rental-tax | 1 | input/corporate-rental-tax.md | 2026-02-25 |
| 3 | utility-billing-regulations | 1 | input/utility-billing-regulations.md | 2026-02-25 |
| 9 | crispina-water-calculator | 1 | input/crispina-water-calculator.md | 2026-02-26 |
| 10 | tenant-payment-tracking | 2 | analysis/tenant-payment-tracking.md | 2026-02-26 |
| 11 | monthly-billing-generation | 2 | analysis/monthly-billing-generation.md | 2026-02-26 |
| 12 | rent-escalation-calculation | 2 | analysis/rent-escalation-calculation.md | 2026-02-26 |
