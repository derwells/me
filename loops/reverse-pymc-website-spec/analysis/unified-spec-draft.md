# Unified Spec Draft — Wave 4 Synthesis

## Summary

Synthesized all 18 analysis files (3 Wave 1 data acquisition + 9 Wave 2 architecture analysis + 6 Wave 3 content audit) into a single unified as-is specification document at `output/pymc-website-spec.md`.

## Output

**File:** `output/pymc-website-spec.md`
**Length:** ~850 lines
**Sections:** 12

## Spec Structure

| # | Section | Content |
|---|---------|---------|
| 1 | Executive Summary | Key numbers, critical findings, overall assessment |
| 2 | Architecture Overview | Both site architectures, DNS/domain setup |
| 3 | Lektor Site (Production) | Tech stack, 10 data models, 22 templates, 17 routes, build/deploy |
| 4 | Next.js Site (Rebranded) | Tech stack, 22 routes + API + drafts, 80 components, data fetching |
| 5 | Strapi CMS Backend | 11 content types, 15 endpoints (9 CRUD + 6 custom), auth status |
| 6 | Third-Party Integrations | 17 services cataloged, migration assessment |
| 7 | Content Inventory | 52 blog posts, 47 team members, 22 clients, 5 courses, static pages |
| 8 | Media Assets | 526 files (165 MB), optimization opportunities (~80 MB savings) |
| 9 | Dependency & Security Audit | 44+ vulnerabilities, 7 EOL components |
| 10 | Cross-Site Comparison | Technology migration status, content migration gaps |
| 11 | Issues Registry | 50 issues: 6 critical, 11 high, 15 medium, 18 low |
| 12 | Redesign Considerations | Migration plan, systems to preserve, gaps, technical debt |

## Synthesis Decisions

1. **Issue prioritization:** Classified all issues from individual analyses into Critical/High/Medium/Low severity. Critical = security vulnerabilities with active CVEs or broken production systems. High = significant security gaps, missing functionality, or data integrity risks. Medium = code quality, duplication, maintainability. Low = typos, dead code, minor inconsistencies.

2. **Content consolidation:** Combined per-aspect content counts into unified inventory. Deduplicated team members across sites (47 unique from 26 Lektor + 29 Next.js with 8 overlap). Combined client list (22 unique from 17 Lektor + 18 Next.js logos + 3 testimonial-only).

3. **Cross-referencing redesign plan:** Mapped findings against the planned Framer + Next.js + Hugo split. Identified specific content migration paths, systems that must be preserved (registration, certificates, coupons), and content gaps to address (no case studies, lost Impressum, incomplete privacy policy).

4. **Architecture documentation:** Included both high-level diagrams and detailed route/model/endpoint tables. Kept sufficient detail for implementation planning while remaining readable as a reference document.

## Key Findings Surfaced in Synthesis

- **47 unique team members** across both sites with only 8 overlap — the rosters are almost entirely divergent
- **50 documented issues** across all severity levels
- **~80 MB** of media savings possible through optimization alone
- **Zero test coverage** on both repos
- **No CI/CD** functional on either repo
- **No Strapi source code** accessible — backend is a black box
- **All revenue-generating content** (courses) is 100% hardcoded with no CMS

## Completeness Check

All 18 analysis aspects are represented in the unified spec:

| Aspect | Spec Section(s) |
|--------|----------------|
| clone-source-repo | Section 2, 3 |
| clone-rebranded-repo | Section 2, 4 |
| cache-redesign-plan | Section 12 |
| lektor-site-structure | Section 3.1-3.4 |
| lektor-content-schema | Section 3.2 |
| lektor-build-deploy | Section 3.5 |
| nextjs-app-structure | Section 4.1-4.4 |
| nextjs-components | Section 4.3 |
| strapi-data-models | Section 5.2 |
| strapi-api-endpoints | Section 5.3 |
| integrations | Section 6 |
| dependencies-audit | Section 9 |
| blog-posts-catalog | Section 7.1 |
| team-members-catalog | Section 7.2 |
| clients-catalog | Section 7.3 |
| courses-catalog | Section 7.4 |
| static-pages-catalog | Section 7.5 |
| media-assets-audit | Section 8 |
