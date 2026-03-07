# Spec Self-Review

## Methodology

Systematic review of `output/pymc-website-spec.md` against all 18 analysis files in `analysis/`. Checked for:
1. **Completeness** — Every analysis aspect represented in the spec
2. **Accuracy** — Numbers, counts, and facts match source analysis
3. **Internal consistency** — Cross-references within the spec are coherent
4. **Coverage gaps** — Anything important in analysis files but missing from spec

## Completeness Check

All 18 analysis aspects are represented in the unified spec:

| # | Analysis File | Spec Section(s) | Status |
|---|--------------|-----------------|--------|
| 1 | clone-source-repo | S2.1, S3 | Covered |
| 2 | clone-rebranded-repo | S2.2, S4 | Covered |
| 3 | cache-redesign-plan | S12 | Covered |
| 4 | lektor-site-structure | S3.1-S3.3 | Covered |
| 5 | lektor-content-schema | S3.2 | Covered |
| 6 | lektor-build-deploy | S3.5 | Covered |
| 7 | nextjs-app-structure | S4.1-S4.2 | Covered |
| 8 | nextjs-components | S4.3 | Covered |
| 9 | strapi-data-models | S5.2 | Covered |
| 10 | strapi-api-endpoints | S5.3 | Covered |
| 11 | integrations | S6 | Covered |
| 12 | dependencies-audit | S9 | Covered |
| 13 | blog-posts-catalog | S7.1 | Covered |
| 14 | team-members-catalog | S7.2 | Covered |
| 15 | clients-catalog | S7.3 | Covered |
| 16 | courses-catalog | S7.4 | Covered |
| 17 | static-pages-catalog | S7.5 | Covered |
| 18 | media-assets-audit | S8 | Covered |

## Accuracy Check

### Numbers Verified

| Claim | Spec Value | Source Analysis | Match |
|-------|-----------|----------------|:-----:|
| Blog posts (Lektor) | 52 | blog-posts-catalog: 52 | Yes |
| Team members (Lektor) | 26 | team-members-catalog: 26 | Yes |
| Team members (Next.js hardcoded) | 29 | team-members-catalog: 29 | Yes |
| Clients (unique) | 22 | clients-catalog: 22 | Yes |
| Courses/workshops | 5 | courses-catalog: 5 | Yes |
| Local media files | 526 | media-assets-audit: 526 | Yes |
| Media size | 165 MB | media-assets-audit: 165.02 MB | Yes |
| Third-party services | 17 | integrations: 17 | Yes |
| npm audit vulns | 39 (2 critical, 31 high, 6 moderate) | dependencies-audit: 39 | Yes |
| Page routes (Lektor) | 17 | lektor-site-structure: 17 | Yes |
| Page routes (Next.js) | 22 + 1 API + 5 draft | nextjs-app-structure: 22 + 1 + 5 | Yes |
| Components (Next.js) | 80 | nextjs-components: 80 | Yes |
| Issues registry | 50 (6C, 11H, 15M, 18L) | Count: 6+11+15+18=50 | Yes |
| Lektor models | 10 | lektor-site-structure: 10 | Yes |
| Strapi content types | 11 | strapi-data-models: 11 | Yes |
| Overlap team members | 8 | team-members-catalog: 8 | Yes |
| YouTube embeds | 158 | media-assets-audit: 158 | Yes |
| Cloudinary URLs | 45 | media-assets-audit: 45 | Yes |
| Potential savings | ~80 MB | media-assets-audit: ~80 MB | Yes |

### Discrepancy Found

| Location | Issue | Resolution |
|----------|-------|------------|
| S5.3 "Custom Routes (6)" | Table lists 7 endpoints but header says 6. The source analysis (`strapi-api-endpoints.md`) also says "6 custom route handlers" but enumerates 7 in its summary list. The 7 are: certificates/verify, certificates/download, certificates/email, contact-form/submit, registration-form/submit, coupons/validate-title, benchmark/submit. | **Fix: Update to 7 custom routes, 16 total.** The original analysis miscounted — benchmark/submit was likely added to the list after the count was written. |

## Internal Consistency Check

- Executive Summary "Key Numbers" table matches detailed sections: Yes
- Issues Registry severity counts match listed items: Yes (6+11+15+18=50)
- Cross-site comparison table aligns with detailed findings: Yes
- Redesign considerations reference actual findings: Yes
- Route counts in S3.4 (17) and S4.2 (22+1+5) match overview: Yes

## Coverage Assessment

### Well-Covered Areas
- Architecture of both sites (tech stack, routing, build/deploy)
- Data models and content schemas (including reverse-engineered Strapi)
- API endpoints with auth status, source files, and payloads
- Component structure with counts, organization, and issues
- Content inventory with complete catalogs
- Media assets with optimization opportunities
- Dependency audit with specific CVEs and EOL dates
- Cross-site comparison showing migration status
- Comprehensive issues registry with severity levels

### Minor Gaps (acceptable for as-is spec)
1. **Strapi DB content counts unknown** — Blog posts in Strapi DB can't be counted without API access. Spec correctly notes this as "Unknown (Strapi DB)". Not fixable from repo analysis alone.
2. **Exact Cloudinary usage split** — Two accounts identified (dx3t8udaw, dhgr6mghh) but the business reason for the split is undocumented. Noted in S8.3.
3. **Heroku plan/limits** — No information about the Heroku tier, dyno type, or database size for the Strapi backend. Would require Heroku dashboard access.

These gaps are inherent limitations of repo-only analysis and are appropriately flagged in the spec rather than silently omitted.

## Verdict

The unified spec is **complete and accurate** with one minor counting error (6 vs 7 custom routes) that has been corrected. All 18 analysis aspects are represented. Numbers are consistent between analysis files and the spec. The issues registry is comprehensive. The spec serves its intended purpose as a factual baseline for the architecture redesign.

**Recommendation:** Converge the loop. The spec is ready for use.
