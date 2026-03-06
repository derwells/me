# Dependencies Audit

Full audit of package versions, EOL status, and known vulnerabilities across both repositories.

## Lektor Site (pymc-labs-website-source)

### Python Runtime & Package Manager

| Component | Version | Status | Notes |
|-----------|---------|--------|-------|
| Python | 3.9 (pixi.toml) / 3.8 (CI workflows) | **EOL** | Python 3.9 EOL Oct 2025. Python 3.8 EOL Oct 2024. CI uses 3.8, pixi uses 3.9 — mismatch. Both unsupported. |
| Pixi | v6 lockfile format | Current | Modern conda-based package manager, but CI workflows still reference deleted `requirements.txt` |

### Python Dependencies (from pixi.toml + pixi.lock)

| Package | Pinned Version | Resolved Version | Status | Notes |
|---------|---------------|-----------------|--------|-------|
| lektor | >=3.3.9 | 3.3.12 | Current | Latest available via conda-forge |
| flask | 2.3.1 | 2.3.1 | **EOL** | Flask 2.x is superseded; 3.1.x is current. Flask 2.3 has no active security support |
| requests | 2.29.0 | 2.29.0 | Outdated | Current is 2.32.x. 2.29 lacks urllib3 2.x support |
| jinja2 | 3.1.2 | 3.1.2 | Outdated | Current is 3.1.5+. Has CVE-2024-34064 (sandbox escape) — fixed in 3.1.4 |
| werkzeug | 2.3.0 | 2.3.0 | **EOL** | Current is 3.1.x. 2.3 has CVE-2024-34069 (debugger RCE) — though not exploitable in static site build |
| mistune | 0.8.4 | 0.8.4 | **EOL/Critical** | Current is 3.1.x. Has CVE-2022-34749 (ReDoS), CVE-2024-34069. 0.x branch abandoned since 2022 |
| pygments | * (unpinned) | 2.19.2 | Current | Unpinned but resolves to latest |
| urllib3 | (transitive) | 1.26.19 | **EOL** | 1.x branch is legacy. Current is 2.3.x. Has known CVEs in older 1.26.x versions |

### Lektor Plugins (from .lektorproject)

| Plugin | Version | Status | Notes |
|--------|---------|--------|-------|
| lektor-markdown-header-anchors | 0.3 | Unmaintained | Last PyPI release 2017. Works but no updates |
| lektor-markdown-highlighter | 0.3 | Unmaintained | Last PyPI release 2016. Uses Pygments (OK) |
| lektor-tags | 0.2 | **Unused** | Installed but never configured (no tag model/template). Dead dependency |
| collapsible-markdown-code-snippets | 0.0.1 (local) | Custom | In-repo plugin at `packages/`. No external dependency |

### CDN Dependencies (from templates/layout.html)

| Library | Version | CDN Source | Status | Notes |
|---------|---------|-----------|--------|-------|
| Bootstrap CSS | 4.5.2 | stackpath.bootstrapcdn.com | **EOL** | Bootstrap 4 EOL Jan 2023. No security patches. Current is 5.3.x |
| Bootstrap JS | 4.5.2 | stackpath.bootstrapcdn.com | **EOL** | Same as above |
| jQuery | 3.5.1 (slim) | code.jquery.com | Outdated | Current is 3.7.x. 3.5.1 has no critical CVEs but lacks fixes from later versions |
| Popper.js | 1.16.1 | cdn.jsdelivr.net | **EOL** | Replaced by @popperjs/core 2.x. 1.x unmaintained |
| Font Awesome | 6.7.2 (CSS) + Kit 8cc267a9ab (JS) | cdnjs.cloudflare.com + kit.fontawesome.com | Current | Dual-loaded (CSS and Kit JS) — redundant |
| Highlight.js | 10.7.2 (CSS only) | cdnjs.cloudflare.com | Outdated | CSS loaded but JS is commented out — unused. Current is 11.11.x |
| MathJax | 2.7.5 | cdnjs.cloudflare.com | **EOL** | MathJax 2.x EOL since 2020. Current is 4.0.x. Has known rendering bugs |
| Google Analytics (gtag) | GA4 G-F3RDLH8R8X | googletagmanager.com | Current | |

### GitHub Actions Dependencies (CI workflows)

| Action | Version Used | Current Version | Status |
|--------|-------------|----------------|--------|
| actions/checkout | v2 | v4 | **Outdated** | 2 major versions behind. v2 uses Node 12 (EOL) |
| actions/setup-python | v2 | v5 | **Outdated** | 3 major versions behind. v2 uses Node 12 (EOL) |
| actions/cache | v4 | v4 | Current | |
| peaceiris/actions-gh-pages | v3 | v4 | **Outdated** | v3 uses Node 16 (EOL) |
| nwtgck/actions-netlify | v1.1 | v3 | **Outdated** | 2 major versions behind |
| gr2m/merge-schedule-action | v1 | v2 | **Outdated** | |

### CI Pipeline Issues
- **Broken build**: All 3 workflows reference `requirements.txt` which was deleted when migrating to Pixi. No workflow has been updated to use `pixi install && pixi run build`.
- **Python version mismatch**: Workflows use 3.8 (EOL Oct 2024), pixi.toml targets 3.9 (EOL Oct 2025). Neither is supported.
- **set-output deprecated**: `::set-output` syntax in pip cache step was deprecated in GitHub Actions Oct 2022, removed in 2024.
- **PAT auth**: Uses `secrets.GHPAGES_TOKEN` (Personal Access Token) rather than GitHub App or `GITHUB_TOKEN` with permissions.

---

## Next.js Site (pymc-rebranded-website)

### Runtime Requirements

| Component | Version | Status | Notes |
|-----------|---------|--------|-------|
| Node.js | >=20.9.0 (per Next.js) | Current | Node 20 LTS supported until Apr 2026. Node 22 LTS now available |
| npm | (lockfileVersion 3) | Current | |

### Direct Dependencies (30 packages)

| Package | Specified | Resolved | Status | Notes |
|---------|----------|---------|--------|-------|
| next | ^16.0.7 | 16.0.10 | Current | **3 high vulns** (DoS via Image Optimizer, HTTP deserialization, PPR endpoint) — all require self-hosting with specific configs |
| react | ^19.2.1 | 19.2.3 | Current | |
| react-dom | ^19.2.1 | 19.2.3 | Current | |
| axios | ^1.7.9 | 1.13.2 | **Vulnerable** | **High**: Prototype pollution via `__proto__` key in mergeConfig. Update to >=1.8.2 |
| jspdf | ^3.0.3 | 3.0.4 | **Critical** | **8 CVEs**: Local file inclusion, PDF injection, DoS, XMP injection, race condition. Heavily vulnerable package |
| swiper | ^11.2.6 | 11.2.10 | **Critical** | Prototype pollution vulnerability |
| react-syntax-highlighter | ^15.6.1 | 15.6.6 | **Moderate** | Via refractor → prismjs (DOM clobbering). Prismjs 1.30.0 |
| react-vertical-timeline-component | ^3.5.3 | 3.5.3 | **High** | Pulls in deprecated @babel/preset-es2015 with vulnerable json5 0.5.1 (prototype pollution). Package unmaintained since 2021 |
| framer-motion | ^11.16.3 | 11.18.2 | Current | Heavy bundle (~30 components import it). No known vulns |
| katex | ^0.16.27 | 0.16.27 | Current | Replaced MathJax 2 — good upgrade |
| sharp | ^0.34.3 | 0.34.5 | Current | Image processing for Next.js |
| sweetalert2 | ^11.17.2 | 11.26.10 | Current | Alert/modal library |
| chart.js (peer) | — | 4.5.1 | Current | Via react-chartjs-2. For benchmark feature |
| chartjs-plugin-datalabels | ^2.2.0 | 2.2.0 | Current | |
| clsx | ^2.1.1 | 2.1.1 | Current | Utility |
| html-to-image | ^1.11.13 | 1.11.13 | Current | For certificate PDF generation |
| lucide-react | ^0.534.0 | 0.534.0 | Current | Icon lib 1/3 |
| next-sitemap | ^4.2.3 | 4.2.3 | Current | |
| react-chartjs-2 | ^5.3.0 | 5.3.1 | Current | |
| react-fast-marquee | ^1.6.5 | 1.6.5 | Current | |
| react-hook-form | ^7.54.2 | 7.68.0 | Current | |
| react-icons | ^5.4.0 | 5.5.0 | Current | Icon lib 2/3 |
| react-markdown | ^10.0.1 | 10.1.0 | Current | |
| react-responsive | ^10.0.0 | 10.0.1 | Current | |
| react-typed | ^2.0.12 | 2.0.12 | Current | Typing animation |
| rehype-highlight | ^7.0.2 | 7.0.2 | Current | |
| rehype-katex | ^7.0.1 | 7.0.1 | Current | |
| rehype-raw | ^7.0.0 | 7.0.0 | Current | |
| remark-gfm | ^4.0.1 | 4.0.1 | Current | |
| remark-math | ^6.0.0 | 6.0.0 | Current | |
| tailwind-merge | ^2.6.0 | 2.6.0 | Current | |
| unist-util-visit | ^5.0.0 | 5.0.0 | Current | |

### Dev Dependencies (5 packages)

| Package | Specified | Resolved | Status | Notes |
|---------|----------|---------|--------|-------|
| tailwindcss | ^3.4.1 | 3.4.19 | Outdated | Tailwind 4.0 released Jan 2025. 3.x still maintained but will eventually EOL |
| eslint | ^9 | 9.39.2 | Current | |
| eslint-config-next | ^16.0.7 | 16.0.10 | Current | |
| @eslint/eslintrc | ^3 | 3.3.3 | Current | |
| postcss | ^8 | 8.5.6 | Current | |

### npm Audit Summary

| Severity | Count | Notes |
|----------|-------|-------|
| Critical | 2 | jspdf (8 advisories), swiper (prototype pollution) |
| High | 31 | Mostly transitive via react-vertical-timeline-component → @babel/preset-es2015 → json5 0.5.1. Also: axios, next (3), minimatch |
| Moderate | 6 | ajv (ReDoS), dompurify (XSS), lodash (prototype pollution), prismjs (DOM clobbering) |
| Low | 0 | |
| **Total** | **39** | |

### Transitive Vulnerability Chain Detail

1. **react-vertical-timeline-component** → @babel/preset-es2015 (deprecated, Babel 6 era) → 25 @babel/plugin-transform-* packages → @babel/core → json5 0.5.1 (prototype pollution CVE-2022-46175). This single unmaintained package accounts for **31 of 39 vulnerabilities**.

2. **jspdf 3.0.4** — 8 distinct CVEs ranging from local file inclusion to DoS. Used only for certificate PDF generation. Should be replaced or updated when patches available.

3. **swiper 11.2.10** — Prototype pollution. Used for carousel/slider components. No patched version available yet.

4. **minimatch 3.1.2** — ReDoS vulnerabilities. Transitive via next-sitemap → fast-glob. A newer minimatch 9.0.5 is also present (via typescript-estree, which is safe).

### Notable Absent Dependencies

| Missing | Impact |
|---------|--------|
| TypeScript | Entire codebase is plain JavaScript — no type safety |
| Testing framework | No Jest, Vitest, Playwright, or Cypress. Zero test infrastructure |
| Linting for a11y | No eslint-plugin-jsx-a11y |
| .env.example | No documentation of required environment variables |
| Prettier / code formatter | No formatting configuration |

### No CI/CD Workflows
The rebranded repo has **zero GitHub Actions workflows**. No automated builds, tests, linting, or deployments. Deployment method unknown (likely manual or Vercel/Heroku).

---

## Cross-Repo Comparison

### Technology Migration Status

| Concern | Lektor (Source) | Next.js (Rebranded) | Migration Status |
|---------|----------------|---------------------|------------------|
| Language | Python 3.9 (EOL) | Node.js 20+ | Upgraded |
| Framework | Lektor 3.3.12 | Next.js 16.0.10 | Upgraded |
| CSS | Bootstrap 4 (EOL) | Tailwind 3.4 | Upgraded |
| JS Framework | jQuery 3.5.1 | React 19.2 | Upgraded |
| Math rendering | MathJax 2 (EOL) | KaTeX 0.16 | Upgraded |
| Markdown | mistune 0.8 (EOL) | react-markdown 10 + remark/rehype | Upgraded |
| Analytics | GA4 direct | GTM + GA4 + HubSpot | Expanded |
| Icons | Font Awesome 6.7 | FA CDN + lucide-react + react-icons | Regressed (3 libs) |
| Email | Mailchimp HTML form | Mailchimp JSONP | **Regressed** (security) |

### Shared Vulnerability Concerns

1. **No authentication anywhere**: Lektor is static (OK). Next.js/Strapi has zero auth on all API endpoints (not OK).
2. **Outdated transitive deps**: Both repos carry outdated transitive dependencies, but the Next.js repo is actively accumulating vulnerability debt.
3. **No CI in either repo**: Lektor CI is broken (references deleted requirements.txt). Next.js has no CI at all.

---

## Risk Summary

### Critical (Immediate Action Required)
1. **jspdf 3.0.4** — 8 CVEs including local file inclusion and arbitrary JS execution. Used in certificate generation.
2. **swiper 11.2.10** — Prototype pollution. Used in multiple carousel components.
3. **Lektor CI completely broken** — Cannot deploy source site via GitHub Actions.

### High (Action Required)
4. **39 npm audit vulnerabilities** — 31 from react-vertical-timeline-component alone (replace package).
5. **axios prototype pollution** — Direct dependency, update to >=1.8.2.
6. **Python 3.8/3.9 EOL** — No security patches for either version.
7. **Flask 2.3 / Werkzeug 2.3 EOL** — Known CVEs in both.
8. **mistune 0.8.4** — Multiple CVEs, abandoned branch.
9. **Jinja2 3.1.2** — CVE-2024-34064 (sandbox escape).

### Moderate
10. **Bootstrap 4 EOL** — No security patches since Jan 2023.
11. **MathJax 2 EOL** — Abandoned since 2020.
12. **Popper.js 1.x EOL** — Replaced by @popperjs/core.
13. **GitHub Actions on v2** — Running on Node 12 (EOL) runners.
14. **prismjs DOM clobbering** — Via react-syntax-highlighter.
15. **Tailwind 3.x** — Still maintained but 4.0 available.

### Low
16. **Highlight.js 10.7 CSS loaded but unused** — Dead dependency in Lektor.
17. **lektor-tags plugin installed but unused** — Dead dependency.
18. **lodash 4.17.21** — Prototype pollution in `_.unset`/`_.omit` (rarely exploitable in practice).

---

## Dependency Counts

| Metric | Lektor Site | Next.js Site |
|--------|------------|-------------|
| Direct runtime deps | 7 (Python) + 7 (CDN) | 30 (npm) |
| Direct dev deps | 0 | 5 (npm) |
| Lektor plugins | 4 (3 community + 1 custom) | N/A |
| Total resolved packages | ~35 (conda) | 804 (npm) |
| Known vulnerabilities | 5+ (Python CVEs) + EOL CDN libs | 39 (npm audit) |
| EOL/deprecated components | 8 | 3 |
| Missing test infrastructure | Yes | Yes |
| CI/CD status | Broken | Absent |
