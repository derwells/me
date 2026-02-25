# DHSUD Housing Price Ceilings — Source Notes

**Fetched:** 2026-02-25
**Primary sources:** DHSUD official announcements, PNA, GMA News, CREBA, Manila Times

---

## Legal Framework

### Governing Authority
- **Republic Act 11201** (DHSUD Act) mandates DHSUD (formerly with NEDA, now with DEPDev) to jointly determine price ceilings for socialized, low-cost/economic, and middle-income housing.
- Ceilings may be reviewed and revised at any time, but **not more than once every two years**.
- Compliance with price ceilings is required for issuance of License to Sell (LTS) by DHSUD.

### Related Laws
- **RA 7279** (Urban Development and Housing Act, UDHA) — defines socialized housing, mandates Balanced Housing Development requirement (Section 18)
- **RA 10884** — amended RA 7279; refined Balanced Housing Development rules
- **BP 220** — sets minimum design standards for economic and socialized housing (separate aspect)

---

## Current Price Ceilings by JMC

### JMC 2025-001 (Socialized Housing) — Signed December 1, 2025; IRR effective December 23, 2025
**Validity:** 3 years from effectivity

#### Horizontal/Subdivision (House-and-Lot)
| Floor Area | Maximum Selling Price |
|---|---|
| 24–26 sqm | ₱844,440 |
| 27 sqm and above | ₱950,000 |

- Minimum floor area raised from 22 sqm → **24 sqm**
- Price is **inclusive of all costs** (land acquisition, development, construction)

#### Vertical/Condominium
| Building Height | Floor Area | Maximum Selling Price |
|---|---|---|
| 3–5 floors | 24–26 sqm | ₱1,280,000 |
| 3–5 floors | 27 sqm+ | ₱1,500,000 |
| 6 floors and above | 24–26 sqm | ₱1,600,000 |
| 6 floors and above | 27 sqm+ | ₱1,800,000 |

#### NCR/Highly Urbanized City Add-On (Zonal Value Adjustment)
For condominiums in NCR and other HUCs, the selling price ceiling may be increased by:
| Zonal Value of Land (per sqm) | Allowable Add-On |
|---|---|
| ₱20,000–₱24,999 | ₱50,000 |
| ₱25,000–₱29,999 | ₱100,000 |
| ₱30,000–₱39,999 | ₱150,000 |
| ₱40,000 and above | ₱200,000 |

---

### JMC 2023-003 (Socialized Housing) — Signed October 2023 [SUPERSEDED by JMC 2025-001]
For reference only:
- Horizontal: ₱850,000 for units ≥28 sqm (with loft ≥50% base, or 32 sqm total)
- Condo (4-storey): ₱933,320 (22 sqm) / ₱1,060,591 (25 sqm) / ₱1,145,438 (27 sqm)
- Condo (5–9 floors): ₱1,000,000 (22 sqm) / ₱1,136,364 (25 sqm) / ₱1,227,273 (27 sqm)
- Condo (10+ floors): ₱1,320,000 (22 sqm) / ₱1,500,000 (25 sqm) / ₱1,620,000 (27 sqm)
- Max with land development cost: ₱1,800,000

---

### JMC 2024-001 (Low-Cost & Medium-Cost Housing) — Issued 2024
**Guarantee ceilings** (for government-backed housing programs):
| Level | Classification | Price Range |
|---|---|---|
| Level 1-A | Socialized | ≤₱300,000 |
| Level 1-B | Socialized (upper) | >₱300,000 to ₱500,000 |
| Level 2 | Economic | >₱500,000 to ₱1,250,000 |
| Level 3 | Low-Cost | >₱1,250,000 to ₱3,000,000 |
| Medium Cost | Medium-Cost | >₱3,000,000 to ₱4,000,000 |
| Open Market | Open Market | >₱4,000,000 |

**Guarantee ceilings (updated 2024):**
- Low-cost housing guarantee ceiling: **₱4,900,000**
- Medium-cost housing guarantee ceiling: **₱6,600,000**

Note: The "guarantee ceiling" is the max loan amount eligible for government guaranty (via HGC), distinct from the selling price ceiling for socialized housing.

---

## Balanced Housing Development Requirement (RA 7279, Sec. 18 as amended by RA 10884)

Developers of proposed subdivision and condominium projects must develop socialized housing equivalent to:
- **Subdivision projects:** At least **15%** of total subdivision area OR project cost (developer's option)
  - Original RA 7279 stated 20%; RA 10884 amendments and HLURB IRR set 15% for subdivision
- **Condominium projects:** At least **5%** of condominium area OR project cost
- **BOI-registered projects:** 20% of total registered project area/cost (horizontal) or 20% of total floor area (vertical)

### Compliance Modes
1. Develop socialized housing in same city/municipality (preferred)
2. Development of a new settlement
3. Slum upgrading/renewal (Zonal Improvement Program/Slum Improvement and Resettlement)
4. Joint-venture with LGU or Key Shelter Agencies
5. Participation in Community Mortgage Program (CMP)
6. Incentivized Compliance (IC): Contribute funds ≥20% of required compliance percentage to BALAI Program

### Compliance Computation (BOI-registered ITH purposes)
- Based on **actual units sold** during ITH availment period
- Non-recoverable participation costs: credit value = 25% of total project cost of socialized project

---

## Key Computation Triggers

1. **Maximum selling price compliance check:** Is unit price ≤ ceiling for its floor area tier and building height?
2. **Zonal value add-on:** In NCR/HUC, look up zonal value per sqm → apply add-on from table above
3. **Balanced housing requirement:** 15% (subdivision) or 5% (condo) of area OR cost → developer chooses basis
4. **Category determination:** Classify unit into Level 1-A through Open Market by selling price

---

## Key Sections for Wave 2 Analysis

- `socialized-housing-compliance` — use floor area tiers + building height tiers + zonal value add-on
- `bp220-lot-compliance` — separate aspect (BP 220 minimum area standards)
- Guarantee vs. selling price distinction: JMC 2024-001 sets guarantee ceilings (HGC backing); JMC 2025-001 sets maximum selling price (LTS compliance)

---

## Sources
- DHSUD news release on JMC 2025-001: https://dhsud.gov.ph/news/dhsud-depdev-update-price-ceiling-for-socialized-housing/
- PNA: https://www.pna.gov.ph/articles/1264339
- GMA News (JMC 2025-001): https://www.gmanetwork.com/news/topstories/nation/968277/dhsud-depdev-update-price-ceilings-for-socialized-housing/story/
- Inquirer (low-cost ceilings): https://newsinfo.inquirer.net/1849997/govt-raises-price-ceilings-for-low-cost-housing-projects
- CREBA (balanced housing): https://creba.ph/balanced-housing-new-compliance-mode/
- Context.ph: https://context.ph/2025/12/01/govt-hikes-socialized-housing-price-ceilings/
- Verizon PH (classification guide): https://www.verizonph.com/differentiate-socialized-economic-low-cost-medium-cost-and-open-market-housing-and-its-prices-in-the-philippines
