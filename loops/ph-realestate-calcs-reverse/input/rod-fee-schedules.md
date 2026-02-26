# Registry of Deeds Fee Schedules — Source Extraction

**Aspect:** rod-fee-schedules (Wave 1)
**Date:** 2026-02-26
**Sources:**
- PD 1529 (Property Registration Decree, 1978), Sec. 117 — authorizes LRA to set fee schedules
- LRA Circular No. 61 (November 4, 1993) — original fee schedule, Supreme Court E-Library
- LRA Circular No. 11-2002 — revised fees for chattel mortgages and real estate instruments (PD 1529), per EO 197 (Jan 13, 2000) and DOF-DBM Joint Circular 2000-2 (Apr 4, 2000)
- LRA Circular No. 13-2016 — updated schedule (most recently cited in practitioner sources as the operative version)
- LRA Circular No. 20-2021 — later amendment (full text in binary PDF; key changes not extractable)
- LRA ERCF online tool: https://lra.gov.ph/ercf/
- 2004 Rules on Notarial Practice (A.M. No. 02-8-13-SC) + A.M. No. 19-08-15-SC (effective Jan 1, 2020)
- SC Circular No. 73-2014 — notarial fee schedule reference

---

## Part A: LRA Registration Fees (for Title Transfer / TCT Issuance)

### Legal Basis
PD 1529, Section 117: "The fees for registration of deeds of sale, mortgage, lease, and other instruments shall be in accordance with the schedule of fees prescribed by the Commissioner of Land Registration."

Fees are paid to the **Register of Deeds (RD)** where the property is located.

### Value Basis
Fees are computed on the **highest of:**
1. Gross selling price (GSP) stated in the deed
2. BIR zonal value
3. LGU Assessor's Fair Market Value (FMV)

### Fee Structure (LRA Circular No. 11-2002 / 13-2016)

**For property values ≤ ₱1,700,000:** Fixed tiered table (17 tiers). Key reference points from practitioner sources:

| Property Value | Registration Fee |
|---|---|
| Up to ₱500 | ₱21 |
| ₱500 – ₱1,000 | ₱48 |
| ₱1,000 – ₱5,000 | ₱78 |
| ₱5,000 – ₱10,000 | ₱108 |
| ₱10,000 – ₱20,000 | ₱157.50 |
| ₱20,000 – ₱50,000 | ₱225 |
| ₱50,000 – ₱100,000 | ₱345 |
| ₱100,000 – ₱200,000 | ₱636 |
| ₱200,000 – ₱500,000 | ₱1,106 |
| ₱500,000 – ₱1,000,000 | ₱2,286 |
| ₱1,000,000 – ₱1,700,000 | ₱5,546 (at ₱1M) |
| At ₱1,700,000 | ₱8,796 (cap of fixed table) |

*Note: Intermediate bracket amounts from the 17-tier table are not fully reproduced in accessible practitioner sources. The ₱1M = ₱5,546 and ₱1.7M = ₱8,796 values are confirmed by multiple practitioner sources.*

**For property values > ₱1,700,000:**
```
Registration Fee = ₱8,796 + (CEIL((Value − ₱1,700,000) / ₱20,000) × ₱90)
```
Where CEIL = ceiling function (round up to next ₱20,000 increment).

**Sample computations:**
- ₱2,000,000: ₱8,796 + (CEIL(300,000/20,000) × ₱90) = ₱8,796 + (15 × ₱90) = ₱8,796 + ₱1,350 = **₱10,146**
- ₱5,000,000: ₱8,796 + (CEIL(3,300,000/20,000) × ₱90) = ₱8,796 + (165 × ₱90) = ₱8,796 + ₱14,850 = **₱23,646**
- ₱10,000,000: ₱8,796 + (CEIL(8,300,000/20,000) × ₱90) = ₱8,796 + (415 × ₱90) = ₱8,796 + ₱37,350 = **₱46,146**

**Effective rate observation:** For large transactions, the effective rate approaches ~0.46% at ₱10M — not simply 0.25% as some sources claim. The 0.25% figure is a rough approximation for mid-range values.

### Additional Charges at Registry of Deeds

| Charge | Amount |
|---|---|
| Entry fee (per instrument) | ₱50 |
| Primary Entry Number annotation | ₱50 per instrument |
| Owner's Duplicate TCT issuance | ₱330 per title |
| Certified True Copy (CTC) | ₱150 (first page) + ₱20/additional page; some sources: ₱273 first 3 pages + ₱20/additional |
| Legal Research Fee | 1% of the registration fee (remitted to UP Law Center) |
| Data processing / IT fee | ₱20–₱100 (varies by Registry; some charge ₱50) |
| Assurance Fund Contribution | 0.25% of property value (one-time, separate from registration fee) |

### Exemptions
- Government transactions (national/local government properties)
- Agrarian Reform Beneficiaries (RA 6657 / CARP)
- Indigents with court-issued pauper's permits
- Low-cost housing annotations (RA 7279 — UDHA): waived or halved fees

---

## Part B: Annotation Fees (by Transaction Type)

Annotation = recording of encumbrances, claims, or modifications against an existing title.

### Real Estate Mortgage (REM)
| Mortgage Amount | Base Fee Formula |
|---|---|
| Up to ₱100,000 | ₱500 + 0.5% of amount |
| ₱100,001 – ₱500,000 | ₱1,000 + 0.3% of excess over ₱100,000 |
| Over ₱500,000 | ₱2,000 + 0.2% of excess over ₱500,000 |

Plus: ₱200 annotation fee per title.
Release/Cancellation of Mortgage: **half** the original registration fee.

**Sample:** ₱3,000,000 mortgage: ₱2,000 + (0.2% × ₱2,500,000) = ₱2,000 + ₱5,000 = ₱7,000 base + ₱200 annotation = **₱7,200**

### Adverse Claim (Sec. 70, PD 1529)
- Filing fee: ₱500
- Annotation fee: ₱100 per title
- (Lapses after 30 days unless extended by court order)

### Lis Pendens (Sec. 76, PD 1529)
- Entry fee: ₱300
- Annotation fee: ₱200 per title
- Cancellation fee (upon resolution): ₱200

### Lease / Sublease
- If rental value is ascertainable: 0.1% of total rental value (minimum ₱500)
- Annotation fee: ₱150 per title
- Agricultural leases: exempt or ₱100

### Easement / Right-of-Way
- Fixed fee: ₱400 (or 0.2% of value if compensation involved, minimum ₱300)
- Annotation: ₱100 per title

### Other Annotations
| Type | Fee |
|---|---|
| Attachment (levy) | ₱500 + ₱100 per title |
| Consolidation of ownership | ₱300 + ₱100 per title |
| Amendment / Correction | ₱1,000 |

---

## Part C: Notarial Fees (for Real Estate Documents)

### Legal Basis
- 2004 Rules on Notarial Practice (A.M. No. 02-8-13-SC), effective August 1, 2004
- Amended by A.M. No. 19-08-15-SC (effective January 1, 2020)
- SC Circular No. 73-2014 provides a notarial fee schedule

### Key Characteristics
**No single national fee schedule exists.** IBP chapters in provinces/cities set Minimum Fee Schedules. The Rules prohibit "excessive or unconscionable" fees but do not mandate specific amounts.

### Typical Rates for Real Estate Documents

For Deeds of Absolute Sale (DOAS) and real estate instruments:
- **Common practice:** 1–2% of transaction value (selling price or FMV, whichever is higher)
- **Typical range in peso terms:** ₱1,000 – ₱10,000 for most residential transactions
- **For larger transactions:** progressive structure under A.M. No. 19-08-15-SC; illustrative example from sources: ₱1.5M property → ₱1,000; ₱12M property → ₱5,000 (first ₱10M) + ₱1,000 (additional ₱2M) = ₱6,000

### Strict Cap on Notarial Act
Per the 2004 Rules: ₱200 per original instrument for the pure notarial act (stamping, signing, recording). Professional fees for drafting the DOAS are separate (typically ₱1,000–₱5,000 additional).

### Per-Page Fees
- IBP schedules: ₱20–₱50 per page for complex multi-page instruments
- Certified copies: ₱150 per document + ₱50 per additional page (some sources)
- Notarial register copies: ₱36 per page (historical schedule)

### Practical Note
In high-value transactions, notaries typically negotiate a total fee covering drafting + notarization. The 1% of transaction value is a reasonable estimator for automation purposes.

---

## Key Observations for Wave 2

**rod-registration-fees computation (Wave 2)** should implement:
1. Two-tier fee engine: lookup table for ≤₱1,700,000; formula for >₱1,700,000
2. Value base = MAX(GSP, BIR zonal, LGU FMV)
3. Additional charge computation: entry fee + owner's duplicate + legal research fee
4. Exemption check (government, agrarian, indigent, low-cost housing)

**rod-annotation-fees computation (Wave 2)** — may want to separate annotation types:
- Mortgage annotation has the most complex formula (tiered + percentage)
- Other annotations are mostly flat fees

**notarial-fees computation (Wave 2)** — effectively non-deterministic unless modeling IBP chapter minimums:
- The 1–2% heuristic is practical but not statutory
- Only the ₱200/instrument cap and the A.M. No. 19-08-15-SC progressive structure are legally grounded

**Priority computations for the catalog:**
1. Registration fee (high frequency, semi-complex two-tier formula) — HIGH priority
2. Mortgage annotation fee (moderate frequency, tiered-percentage formula) — MEDIUM priority
3. Notarial fee (high frequency, but largely non-deterministic) — LOW deterministic value

**Update risk:** LRA updates fee schedules roughly every 3–5 years. Circular 11-2002 → 13-2016 → 20-2021 suggests periodic updates. Any automation must track these changes.
