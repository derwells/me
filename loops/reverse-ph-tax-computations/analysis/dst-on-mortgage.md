# DST on Mortgage — Computation Extraction
## Aspect: dst-on-mortgage | Wave 2
## Analyzed: 2026-02-25

---

## Overview

Documentary Stamp Tax on mortgage instruments is imposed under **NIRC Section 195**, as amended by the TRAIN Law (RA 10963, effective January 1, 2018) and implemented by **RR 4-2018**.

This is a **stepped-schedule tax**, not a simple percentage — the rate is expressed as a flat base amount plus a fixed increment per ₱5,000 band.

---

## Inputs

| Input | Type | Description |
|---|---|---|
| `amount_secured` | Number (₱) | Principal amount of loan/credit secured by the mortgage |
| `instrument_date` | Date | Date document was made/notarized (determines pre- vs post-TRAIN rate) |
| `is_open_end` | Boolean | Whether the mortgage is for a revolving/fluctuating account with no fixed limit |
| `amount_actually_loaned` | Number (₱) | For open-end mortgages: amount actually loaned at time of execution |

---

## Formula

### Post-TRAIN (instruments dated on or after January 1, 2018)

```
IF amount_secured <= 5,000:
    DST = 40.00

ELSE:
    bands_above_first = ceil((amount_secured - 5,000) / 5,000)
    DST = 40.00 + (bands_above_first × 20.00)
```

**Effective rate approximation:** ~0.40% of amount secured for large amounts (decreases toward this asymptote as amount grows)

### Pre-TRAIN (instruments dated before January 1, 2018)

```
IF amount_secured <= 5,000:
    DST = 20.00

ELSE:
    bands_above_first = ceil((amount_secured - 5,000) / 5,000)
    DST = 20.00 + (bands_above_first × 10.00)
```

**Effective rate (pre-TRAIN):** ~0.20% asymptote

### Rate Table (Post-TRAIN)

| Amount Secured | Pre-TRAIN DST | Post-TRAIN DST |
|---|---|---|
| ≤ ₱5,000 | ₱20.00 | **₱40.00** |
| Each additional ₱5,000 (or fraction) above ₱5,000 | + ₱10.00 | **+ ₱20.00** |

---

## Worked Example

**Scenario:** Real estate mortgage (REM) for ₱5,000,000, notarized February 2026 (post-TRAIN)

| Step | Computation | Amount |
|---|---|---|
| Base tax on first ₱5,000 | Flat | ₱40.00 |
| Excess above ₱5,000 | ₱5,000,000 − ₱5,000 = ₱4,995,000 | — |
| Bands in excess | ₱4,995,000 ÷ ₱5,000 = 999 (exact, no fraction) | 999 bands |
| DST on excess | 999 × ₱20 | ₱19,980.00 |
| **Total DST** | ₱40 + ₱19,980 | **₱20,020.00** |
| Effective rate | ₱20,020 / ₱5,000,000 | 0.4004% |

---

## Instruments Covered (Triggers)

Section 195 applies to:
- Real estate mortgages (REM) — land, buildings, improvements
- Chattel mortgages — personal property
- Pledges of any property (real or personal)
- Deeds of trust where property is conveyed as security
- Deeds of trust to be sold/converted into money, if intended only as security

**Not covered by Section 195:**
- Standalone promissory notes / loan agreements (those are taxed under Section 179 at ₱1.50 per ₱200 post-TRAIN = 0.75%)
- OLSA exception: see Edge Cases

---

## Edge Cases

### Open-End Mortgages / Revolving Credit / Fluctuating Accounts

When a mortgage secures a revolving credit line or future advances with no fixed ceiling:
- DST is computed only on the **amount actually loaned or given at the time of execution**
- Each **subsequent advance** triggers additional DST on the new advance amount using the same rate schedule
- Each drawdown is treated as a separate taxable event

Example: ₱10M revolving credit line, initial draw ₱3M at execution, subsequent draws of ₱2M and ₱5M:
- DST at execution: on ₱3M → ₱11,980
- DST at ₱2M draw: ₱7,980
- DST at ₱5M draw: ₱19,980
- Total: ₱39,940 vs. a fixed ₱10M mortgage would be: ₱39,980 (negligible difference due to step function)

### Fixed-Ceiling Mortgages with Future Advances

If the total credit granted is **specified in the mortgage** document (even if not all drawn at once):
- DST is paid upfront on the **full specified ceiling amount**
- No additional DST on subsequent drawdowns up to that ceiling

### OLSA (Omnibus Loan and Security Agreement)

Under RR 9-94, when a single instrument combines both:
- A loan agreement / promissory note, AND
- The mortgage/pledge securing it

Then DST is assessed as a single instrument — the applicable rate is for the **loan instrument** (Section 179), not the mortgage rate (Section 195). This avoids "double" DST and is commonly used in bank financing.

### Assignment / Transfer of Mortgage

When a mortgage is assigned to another creditor:
- The assignment document is a separate taxable instrument
- DST on the assignment is at the same rate as the original instrument per Section 198
- The original DST does not "carry over" to the new holder

### Extensions and Restructuring

Under Section 199(d), certain **renewals or extensions of existing debt** do not attract additional DST on the same principal if the original tax was paid. However:
- New principal advances (even as part of a restructure) are subject to fresh DST on the additional amount
- A full replacement loan (new promissory note + new mortgage) is a new taxable event

---

## Legal Citations

| Authority | Text | Relevant Provision |
|---|---|---|
| NIRC Section 195 (as amended by RA 10963) | "On every mortgage or pledge of lands, estate, or property, real or personal, heritable or movable, whatsoever, where the same shall be made as a security for the payment of any definite and certain sum of money lent at the time or previously due and owing or forborne to be paid, being payable... on each ₱5,000 (or fractional part thereof) of the amount secured..." | Base rate schedule |
| RA 10963 (TRAIN Law), Section 58 | Amended Section 195: increased base from ₱20 to ₱40; increased incremental from ₱10 to ₱20 | Rate doubling |
| RR 4-2018, Section 19 | "On Mortgages, Pledges and Deeds of Trust... increased from P20.00 to P40.00" (base); "increased from P10.00 to P20.00" (incremental) | Implementing regulation |
| NIRC Section 200 | DST return filed within 5 days after close of month in which document was made/signed | Filing deadline |
| NIRC Section 198 | Assignments and renewals of mortgage subject to same rate as original instrument | Transfer DST |
| RR 9-94 | OLSA single-instrument treatment | OLSA exception |

---

## Filing Requirements

| Element | Detail |
|---|---|
| Form | BIR Form 2000-OT (Documentary Stamp Tax Declaration/Return — One-Time Transactions) |
| Monthly filers (banks, financial institutions) | BIR Form 2000 (DST Monthly Return) |
| Deadline | **5 days after close of the month** in which document was executed (e.g., mortgage notarized March 15 → deadline April 5) |
| Hard outer deadline | In no case later than date of registration with Register of Deeds (for real property mortgages) |
| Filing venue | AAB within territorial jurisdiction of RDO where mortgagor is registered or where property is located |
| If no AAB | Revenue Collection Officer or City/Municipal Treasurer within same RDO |
| eONETT | Available for real property transactions via BIR eONETT online system |
| Liable party | Contractually assignable; by convention typically the borrower/mortgagor |
| Late penalty | 25% surcharge + 12% per annum interest on unpaid tax |

---

## Source Conflict — Resolved

During extraction, a discrepancy was found between two internal source documents:

| Source | Base (≤₱5,000) | Incremental (per ₱5,000) |
|---|---|---|
| nirc-tax-titles.md (Wave 1 cache) | ₱40 ✓ | ₱20 ✗ (shows ₱20 which is correct, but formula shows ×₱20 — actually this IS correct) |
| bir-revenue-regulations.md (Wave 1 cache) | ₱40 ✓ | ₱40 ✗ (INCORRECT — this is the bir-revenue-regulations error) |

**Resolution:** Verification subagent confirmed via 5+ independent sources (NTRC Tax Research Journal, Supreme Court E-Library RA 10963 full text, RR 4-2018 full text, Tax and Accounting Center, practitioner commentaries) that:

- Pre-TRAIN: base ₱20, incremental ₱10
- Post-TRAIN (TRAIN doubled both): base ₱40, incremental ₱20

The `bir-revenue-regulations.md` cached file incorrectly stated the post-TRAIN incremental as ₱40. This was an error in Wave 1 extraction. The correct incremental is **₱20**.

**Correct post-TRAIN formula:**
```
DST = ₱40 + ceil((amount - ₱5,000) / ₱5,000) × ₱20  [for amounts > ₱5,000]
DST = ₱40  [for amounts ≤ ₱5,000]
```

---

## Determinism Assessment

**Deterministic: YES** (with conditions)

| Condition | Deterministic? | Notes |
|---|---|---|
| Fixed-amount mortgage | ✅ Yes | Pure formula: base + (bands × ₱20) |
| Open-end/revolving mortgage | ✅ Yes (per-drawdown) | DST per drawdown = same formula on drawdown amount |
| OLSA single-instrument | ✅ Yes (once instrument type determined) | Use Section 179 formula instead |
| Pre- vs post-TRAIN rate selection | ✅ Yes (based on instrument date) | Binary date cutoff: January 1, 2018 |

The pre/post-TRAIN rate selection is fully deterministic based on instrument date. The OLSA determination (does this instrument combine a note and mortgage?) involves document review but the rate selection once determined is algorithmic.

---

## Automation Notes

**Complexity:** Low-medium
- Formula: stepped arithmetic (not percentage) — requires ceil() function
- Two rate schedules: pre- and post-TRAIN (date-gated)
- Edge cases: open-end (per-drawdown tracking), OLSA exception, assignments
- No lookup tables needed — all rates are statutory constants
- No zonal value dependency (unlike CGT, DST on conveyance, CWT)

**Implementation inputs required:**
1. Amount secured (numeric)
2. Instrument date (for pre/post-TRAIN selection)
3. Instrument type flag (regular mortgage vs. OLSA vs. open-end)
4. For open-end: amount actually loaned at execution date

**Key automation value:** Practitioners regularly miscalculate the stepped schedule (treating it as a percentage). A calculator showing the stepped bands with ₱5,000 units is genuinely useful for loan documentation.
