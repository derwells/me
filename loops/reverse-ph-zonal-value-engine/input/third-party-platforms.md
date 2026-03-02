# Third-Party Platform Raw Data Cache

**Fetched:** 2026-03-02
**Purpose:** Cached source data for Wave 4 deep dives. This file contains raw observations from site visits; the processed analysis is in `analysis/third-party-platform-survey.md`.

---

## ZonalValueFinderPH (zonalvaluefinderph.com)

### Homepage
- "2025 BIR Zonal Values in 3-easy-clicks"
- Three search modes: City/Municipality, Barangay, Street/Subdivision/Condominium
- Select2 dropdowns with AJAX population
- Backend endpoints: POST /get_dropdown_data, POST /chat
- Google Analytics: G-5C23VSP54R
- Google AdSense + gizokraijaw.net ad scripts
- Data labeled "updated as of March 1, 2025"
- No operator info in footer

### All Cities Page
- ~1,600+ cities/municipalities listed
- Organized alphabetically by province
- Table: Municipalities/Cities | Province | Action button
- Responsive design, hover-activated buttons

### Revenue Regions Page
- 19 Revenue Regions
- ~111 Revenue District Offices
- Hierarchical: Region > RDO > Cities/Municipalities
- RDO numbers 1-115 (not all sequential)

### Search Data Page (Street Search)
- Text input: minimum 3 characters
- Results in table with "Show Zonal Values" popup
- "Narrow down your query" warning at >10 results
- "Make A New Search" reset button

### Makati Results Page (Confirmed Data Columns)
- Barangay: San Lorenzo, Bangkal, Bel-Air, etc.
- Street: EAST DRIVE, ABELARDO, AMORSOLO, MAKATI AVENUE, etc.
- Vicinity: AYALA CENTER, SAN LORENZO VILLAGE, DON BOSCO TO EDSA, Bel-Air - 1 Side
- Class: CR, RR, CC, RC, PS, X
- Price per SQM: 35,000 to 750,000 PHP
- Example: San Lorenzo - Ayala Center, EAST DRIVE, CR, 750,000

### Classification Codes Page
- Code/Classification legend table
- RR, CR, RC, CC, CL, A1-A50
- Agricultural: 50 subcategories (A1=Riceland Irrigated through A50=Other Agricultural Lands)
- Missing from their list: GL, GP, I, PS, X, APD (but PS and X appear in actual results)

### Disclaimer (verbatim)
"The information provided on this website is intended for general informational purposes only. It is not intended to be used for making purchase decisions or as a reference for final computations. The zonal values presented on this website might not be accurate and should not be relied upon for any financial or legal decisions. For accurate and up-to-date zonal values, it is strongly recommended that you consult the official website of the Bureau of Internal Revenue (BIR) of the Philippines."

---

## LandValuePH (landvalueph.com)

### Homepage
- "Philippines #1 online property valuation tool"
- "Check land value using official BIR zonal data"
- "200+ cities" coverage
- "From P399" pricing
- "Trusted by 8,500+ Filipino property owners across 17+ regions"
- Founded 2024
- Google Analytics: GA-F2923PHJMS
- Contentsquare monitoring
- No display advertising

### Zonal Value Directory
- City links: Makati, Quezon City, Manila, Taguig, Pasig, Paranaque, Cavite, Laguna, Cebu, Iloilo City, Bacolod, Baguio, NCR
- Tools linked: Land value lookup, selling cost computation, estate tax calculator, CGT calculator
- "official BIR data" emphasized
- No unified search bar — navigate by clicking city links

### Land Value Calculator (Paid)
- Vacant Lots: PHP 299
- House & Lot: PHP 799
- Inputs: Location/region, barangay, lot size, shape, road access, frontage, zoning, flood risk, utilities, title status, neighborhood development
- Processing: "Live BIR zonal data integration with multi-factor adjustment algorithms"
- 8-23 market adjustment factors depending on property type
- Output: 6-7 page PDF report
- Includes: BIR ZV lookup, market-adjusted valuation, CGT/transfer tax, depreciation (H&L), comparables
- Instant generation after payment

### Key Claims
- "Zonal values typically updated only every 3-5 years"
- "Often fall 30-50% below actual market prices"
- Metro Manila prime areas: PHP 200,000-500,000/sqm commercial
- Provincial cities: PHP 5,000-25,000/sqm
- Agricultural rural: PHP 50-500/sqm

---

## REN.PH (ren.ph)

### Homepage
- "Philippine Sovereign Real Estate Ledger"
- "Raising the Standard in Philippine Real Estate"
- "Free verification platform for Philippine real estate"
- "Public infrastructure" positioning
- No signup, no ads, no paywall
- Powered by Godmode PH
- Founder: Aaron Zara, PRC License #0025157

### Zonal Value Tool
- ZonalSearch component
- Search by city or barangay
- Regional browsing categories
- Database stats (explicit):
  - 73 provinces
  - 1,913 cities/municipalities
  - 46,444 barangays
  - 336,792 zone records
- Categories: residential, commercial, industrial
- RDO code tracking per record
- Last updated: 2024

### Technology
- Next.js (React, SSR + streaming)
- Supabase backend
- Geist design system
- Google Analytics GA-4
- "Agentic AI Orchestration" for broker verification

### Other Services
- Broker license verification: 25,264+ verified PRC profiles
- License-to-Sell (LTS): 8,240+ DHSUD records
- Transfer tax calculator
- Legal templates (contracts, deeds, SPAs)
- Due diligence checklists
- HOA rights guides, foreclosure guides
- Academy: RA 9646 Essentials
- PRC exam results tracking

### Data Provenance
- PRC, DHSUD, BIR (three government agencies)
- "97.7% direct government provenance" (for broker verification)

---

## Housal (housal.com)

### Zonal Value Tool
- Text search with autocomplete
- Example searches: Makati, BGC, Quezon City, Cebu, Forbes Park, San Juan
- Classification filters: RC, RR, CC, CR, PS
- Historical filter toggle (current vs historical)
- Sort by year
- 1,961,265+ records (also "2M+ official records")
- 30,000+ searchable locations
- 17 regions, 81 provinces

### Browse Interface
- Hierarchy: Region > Province > City > Barangay
- Pages dynamically loaded (showed "0 Regions" and "0 Total Records" in static fetch)
- City pages also showed 0 records for Makati in static fetch

### Company
- Located in BGC, Taguig City, Metro Manila
- Revenue: Property listing subscriptions ("Post Unlimited Properties"), Founder's Circle membership
- Also a full property marketplace (Buy, Sell, Rent, Projects)

### Technology
- Next.js (confirmed: /_next/static/chunks/)
- Light/dark theme with localStorage
- Heavy client-side rendering

### Disclaimer
"Market prices are typically 20-50% higher than BIR zonal values, especially in premium locations. Always verify with the BIR for official transactions."

---

## RealValueMaps (realvaluemaps.com)

### Homepage Claims
- "2025 BIR Zonal Values"
- "Instant Access to 2.7M+ Properties"
- 42,011 barangays
- 121 RDOs (vs 124 actual — 3 missing)
- Google Analytics: G-R03W6GPKEL

### Technology
- JavaScript-heavy application
- Minimal static HTML rendered
- Framework not determinable

### No Other Data Available
- No operator info found
- No reviews or social media presence
- No pricing or monetization visible
- Site did not render meaningfully in static fetch

---

## ZonalValue.com (zonalvalue.com) — Brief

- Organizes by district subdomains (e.g., ncr1stdistrict.zonalvalue.com)
- Major cities coverage
- Free lookup
- No record count disclosed
- No further analysis performed — smaller player
