# Media Assets Audit

## Summary

Total media across both sites: **526 local files (165 MB)** plus **45 Cloudinary-hosted images** and **158+ YouTube video embeds**. The Lektor site carries the bulk of the weight (134 MB across 352 files) with zero image optimization. The Next.js site is lighter (31 MB across 174 local files) but has triple-format client logos and duplicate team photos. Neither site uses modern image optimization pipelines.

---

## 1. Lektor Site — Local Media

### 1.1 Content Directory (blog posts, team, clients, products)

| Format | Files | Size (MB) | Notes |
|--------|------:|----------:|-------|
| PNG | 246 | 100.88 | Dominant format, no WebP conversion |
| JPG/JPEG | 30 | 14.02 | Team headshots + some blog covers |
| GIF | 4 | 10.46 | Animated data visualizations |
| SVG | 23 | 1.45 | Chart outputs (matplotlib) |
| WebP | 2 | 0.58 | Only 2 files use modern format |
| **Total** | **306** | **127.76** | |

**Oversized files:**
- 30 files > 1 MB (combined ~57 MB)
- 85 files > 500 KB (combined ~100 MB)
- 129 PNGs > 200 KB — candidates for WebP conversion
- 8 JPGs > 500 KB — mostly team headshots

**Top 10 largest files:**

| File | Size | Type |
|------|------|------|
| `blog-posts/modelling-changes-marketing-effectiveness-over-time/new-a.gif` | 5.9 MB | Animated GIF |
| `blog-posts/2023-19-11-marketing-effectiveness/cover.png` | 4.9 MB | Blog cover |
| `team/ricardo-vieira/headshot.jpg` | 3.2 MB | Team headshot |
| `blog-posts/causalpy-*/cover.png` | 3.2 MB | Blog cover |
| `blog-posts/bayesian_computation_in_finance/cover.png` | 2.8 MB | Blog cover |
| `blog-posts/likelihood-approximations-*/weibull.gif` | 2.8 MB | Animated GIF |
| `blog-posts/innovation-lab/cover.png` | 2.8 MB | Blog cover |
| `blog-posts/pymc-marketing-*/cover.png` | 2.4 MB | Blog cover |
| `blog-posts/synthetic-consumers-open-ended/cover.png` | 2.2 MB | Blog cover |
| `team/benjamin-vincent/headshot.jpg` | 2.0 MB | Team headshot |

**Heaviest blog posts by total image weight:**

| Blog Post | Images | Total Size (MB) |
|-----------|-------:|-----------------:|
| cohort-revenue-retention | 19 | 10.7 |
| modelling-changes-marketing-effectiveness-over-time | 6 | 7.9 |
| markov-process | 20 | 7.1 |
| likelihood-approximations-through-neural-networks | 13 | 5.7 |
| 2023-19-11-marketing-effectiveness | 1 | 4.9 |
| bayesian_computation_in_finance | 11 | 4.8 |
| probabilistic-forecasting | 10 | 4.1 |
| innovation-lab | 9 | 3.8 |
| causal-inference-in-pymc | 7 | 3.6 |
| causalpy-* | 3 | 3.5 |

**Team headshots (26 files, 12.0 MB):**
- Largest: `ricardo-vieira/headshot.jpg` (3.2 MB) — raw camera resolution
- Smallest: `alona-krokhmal/headshot.jpg` (8 KB) — excessively compressed
- Wildly inconsistent sizes: 8 KB to 3.2 MB range (400x variation)
- All served at whatever original resolution — no thumbnailing

**Placeholder/broken files (5 files, 10 bytes total):**
- `blog-posts/innovation-lab/old_cover_2.png` (2 bytes)
- `blog-posts/innovation-lab/old_cover_3.png` (2 bytes)
- `blog-posts/innovation-lab/old_cover_5.png` (2 bytes)
- `blog-posts/innovation-lab/old_cover_6.png` (2 bytes)
- `blog-posts/synthetic-consumers/old_cover_2.png` (2 bytes)

These are empty/corrupt files (2 bytes = not valid images). Likely leftover from cover image replacements.

### 1.2 Assets Directory (static files)

| Format | Files | Size (MB) | Notes |
|--------|------:|----------:|-------|
| JPG/JPEG | 13 | 3.10 | Workshop images, home page |
| PNG | 26 | 1.92 | Client logos, favicon, product logos |
| afdesign | 1 | 0.93 | Affinity Designer source file (should not be deployed) |
| CSS | 3 | 0.02 | Workshop + custom styles |
| JS | 2 | 0.01 | Toggle code + workshop script |
| ICO | 1 | 0.01 | Favicon |
| **Total** | **46** | **5.99** | |

**Notable:**
- `static/images/blog_post/cover.afdesign` (975 KB) — design source file deployed to production
- `static/images/pymc_labs_home.jpeg` (1.0 MB) — homepage hero image, unoptimized
- `static/workshops/applied-bayesian-modeling/` — 11 files (2.7 MB): workshop photos, instructor headshots, certificate template, CSS, JS
- 17 client logos in `static/images/client_logos/` (597 KB total, all PNG)

### 1.3 Video Content

No local video files. All video content uses **YouTube embeds**:
- **158 unique YouTube URLs** across blog posts
- Most reference a single video (`5QgiixYjmTM`) with 40+ timestamp-anchored links (webinar chapter navigation)
- 14 blog posts (27%) contain embedded videos
- No Vimeo or self-hosted video

---

## 2. Next.js Site — Local Media (public/)

### 2.1 Overall Breakdown

| Format | Files | Size (MB) | Notes |
|--------|------:|----------:|-------|
| JPG/JPEG | 36 | 13.79 | Team photos, workshop images |
| PNG | 65 | 9.39 | UI elements, course assets, logos |
| SVG | 29 | 1.27 | Icons, logos, client logos |
| WebP | 21 | 0.86 | Client logos (duplicate format) |
| MP4 | 1 | 5.85 | Hero background video |
| JSX | 18 | 0.08 | SVG icon components (misplaced in public/) |
| HTML | 1 | 0.02 | Unknown |
| XML | 2 | 0.02 | Sitemaps |
| TXT | 1 | 0.00 | robots.txt |
| **Total** | **174** | **31.27** | |

### 2.2 By Directory

| Directory | Files | Size (MB) | Contents |
|-----------|------:|----------:|----------|
| users/ | 22 | 12.75 | Team member photos (identical to Lektor headshots) |
| HeroBgs/ | 5 | 7.19 | Hero.mp4 (5.85 MB) + background PNGs |
| courses/ | 28 | 3.65 | Workshop banners, instructor photos, certificate template, AI course assets |
| clients/ | 49 | 1.81 | 18 clients × 2-3 formats each (PNG + SVG/WebP) |
| industries/ | 6 | 1.77 | Card images (draft feature) |
| home/ | 8 | 1.35 | Stats, hero, about video thumbnail |
| team/ | 1 | 0.92 | Single duplicate (adrian-seyboldt.jpg) |
| services/ | 5 | 0.44 | Service page images (draft feature) |
| solutions/ | 3 | 0.15 | Solution page images (draft feature) |
| svg/ | 25 | 0.15 | **18 JSX files + 7 SVG brand logos** |
| about/ | 1 | 0.05 | About page image |
| marimo/ | 1 | 0.02 | Marimo notebook file |
| (root) | 20 | 1.07 | Logos, certificates, sitemaps, favicons |

### 2.3 Team Photos — Duplicate Analysis

**19 identical files** exist in both `public/users/` (Next.js) and `content/team/*/headshot.*` (Lektor):

| Member | Lektor Size | Next.js Size | Identical? |
|--------|-------------|-------------|------------|
| adrian-seyboldt | 966 KB | 966 KB | Yes |
| alexandre-andorra | 929 KB | 929 KB | Yes |
| benjamin-vincent | 2,049 KB | 2,049 KB | Yes |
| ricardo-vieira | 3,375 KB | 3,375 KB | Yes |
| niall-oulton | 1,513 KB | 1,513 KB (jpg) + 738 KB (png) | **2 copies in Next.js** |
| thomas-wiecki | 694 KB | 694 KB | Yes |
| osvaldo-martin | 390 KB | 390 KB | Yes |
| *(14 more)* | *varies* | *identical* | Yes |

**Key finding:** `niall-oulton` has two different files in Next.js (`niall-oulton.jpg` at 1,513 KB + `niall_oulton.png` at 738 KB) — duplicate with different underscore convention.

Additional photos only in Next.js `public/users/`: `christian_luhmann.png`, `joe_wilkinson.png`, `luca_fiaschi.jpg` (3 files using underscores instead of hyphens — inconsistent naming).

Also: `public/team/adrian-seyboldt.jpg` (966 KB) is an **exact duplicate** of `public/users/adrian-seyboldt.jpg`.

### 2.4 Client Logos — Triple Format Redundancy

18 unique client IDs (c1-c21, with gaps at c17-c19). Each client has **2-3 format variants**:

| Clients | Formats per client | Total files |
|---------|-------------------|-------------|
| 13 clients (c1-c13) | 3 formats (PNG + SVG + WebP) | 39 |
| 5 clients (c14-c21) | 2 formats (PNG + WebP) | 10 |
| **Total** | | **49 files, 1.81 MB** |

All use opaque naming (`c1.png`, `c4.svg`) — client names only appear in component alt-text. No programmatic format selection; likely manual copy of export variants.

### 2.5 JSX Files in public/svg/ (Architectural Issue)

18 JSX component files stored in `public/svg/` instead of in the components directory:
- `A1.jsx`, `A2.jsx`, `A3.jsx` — About section SVGs
- `F1.jsx`-`F6.jsx` — Feature/function SVGs
- `S1.jsx`-`S4.jsx` — Service SVGs
- `UB1.jsx`-`UB4.jsx` — "Use/Benefit" SVGs
- `Pinned.jsx` — Pinned icon

These are React components (not static assets) misplaced in the public directory. They won't be bundled by Next.js from here — likely unused or imported via a non-standard path.

### 2.6 Video Content

- **1 local video:** `HeroBgs/Hero.mp4` (5.85 MB) — hero section background
- **3 YouTube embeds** in code (2 unique videos + 1 rickroll placeholder `dQw4w9WgXcQ`)
- Video embed in `ContentVedio.jsx` component (note: typo in component name)

---

## 3. Cloudinary-Hosted Media (Next.js)

### 3.1 Account Breakdown

| Account | Unique URLs | Purpose |
|---------|-------------|---------|
| `dx3t8udaw` | 42 | Strapi-connected: team photos, course instructor headshots, course banners |
| `dhgr6mghh` | 3 | Second account: benchmark thumbnail, 2 team headshots (thomas-wiecki, ulf-aslak) |
| **Total** | **45** | |

### 3.2 Content Breakdown (dx3t8udaw)

- **~30 team member photos** — uploaded to Strapi, served via Cloudinary
- **6 course instructor headshots** — hardcoded URLs in `Instructors.jsx`
- **2 course banner images** — Open Graph / hero images
- **2 supplementary** — course detail images
- Formats: mostly `.webp` (modern), some `.jpg` and `.png`

### 3.3 Content Breakdown (dhgr6mghh)

- `LLM_Price_BenchMark_Thumbnail_xf2oqe.png` — benchmark page hero
- `thomas-wiecki_qaebca.webp` — duplicate team photo
- `ulf-aslak_mkqu24.webp` — duplicate team photo

**Issue:** Thomas Wiecki and Ulf Aslak have photos in **three locations**: Lektor headshots, Next.js `public/users/`, and Cloudinary `dhgr6mghh`. No single source of truth.

---

## 4. Image Optimization Analysis

### 4.1 Format Modernization Opportunities

| Repo | Current | Candidates | Estimated Savings |
|------|---------|------------|-------------------|
| Lektor | 246 PNGs (100.9 MB) | 129 PNGs > 200 KB | ~60-70 MB with WebP/AVIF conversion |
| Lektor | 4 GIFs (10.5 MB) | All 4 animated GIFs | ~8 MB with WebM/MP4 conversion |
| Lektor | 29 JPGs > 200 KB | 8 > 500 KB (headshots) | ~5 MB with resizing to display size |
| Next.js | 65 PNGs (9.4 MB) | 14 PNGs > 200 KB | ~3-5 MB with WebP conversion |

**Conservative total savings: ~80 MB (48% reduction)** from format conversion alone.

### 4.2 Missing Optimization Features

| Feature | Lektor | Next.js |
|---------|--------|---------|
| WebP/AVIF serving | No (2 WebP files total) | Partial (21 WebP in clients/, Cloudinary uses WebP) |
| Responsive images (`srcset`) | No | No (uses `next/image` in some places but not consistently) |
| Lazy loading | No | Partial (Next.js Image component) |
| Image CDN | No (served from GitHub Pages) | Partial (Cloudinary for Strapi content, local for rest) |
| Thumbnail generation | No | No |
| Build-time optimization | No | No build pipeline for images |
| Alt text | Inconsistent | Inconsistent (client logos have it, many images lack it) |

### 4.3 Specific Headshot Optimization

Team headshots are the worst offenders for oversized images relative to display size:

| Display Size | Typical File Size | Optimal File Size | Waste Factor |
|-------------|------------------|-------------------|-------------|
| ~200×200px avatar | 500 KB - 3.2 MB | 10-30 KB (WebP) | 17x - 107x |

---

## 5. Issues Catalog

| # | Issue | Severity | Location |
|---|-------|----------|----------|
| 1 | **129 unoptimized PNGs** (100.9 MB) served without WebP/AVIF conversion | High | Lektor content/ |
| 2 | **Team headshots 17-107x oversized** for display dimensions | High | Both repos |
| 3 | **19 identical team photos duplicated** across repos (~11 MB waste) | Medium | Lektor content/team/ + Next.js public/users/ |
| 4 | **Niall Oulton has 3 photo files** in Next.js (jpg + png + Lektor copy) | Low | Next.js public/users/ |
| 5 | **adrian-seyboldt.jpg duplicated** in both public/users/ and public/team/ | Low | Next.js public/ |
| 6 | **Triple-format client logos** (49 files for 18 clients) with no programmatic selection | Medium | Next.js public/clients/ |
| 7 | **5 corrupt placeholder files** (2 bytes each, not valid images) | Low | Lektor content/blog-posts/ |
| 8 | **Affinity Designer source file** (cover.afdesign, 975 KB) deployed to production | Low | Lektor assets/static/images/blog_post/ |
| 9 | **18 JSX components in public/svg/** — React files misplaced in static assets dir | Medium | Next.js public/svg/ |
| 10 | **2 Cloudinary accounts** with no documented ownership or purpose split | Medium | Next.js codebase |
| 11 | **Thomas Wiecki & Ulf Aslak photos in 3 locations** — no single source of truth | Medium | Both repos + Cloudinary |
| 12 | **Hero.mp4 (5.85 MB)** served locally without CDN or compression | Medium | Next.js public/HeroBgs/ |
| 13 | **No responsive image pipeline** — all images served at original resolution | High | Both repos |
| 14 | **4 animated GIFs (10.5 MB)** could be ~80% smaller as WebM/MP4 | Medium | Lektor content/ |
| 15 | **Draft feature assets (industries, services, solutions)** consuming 2.4 MB for unused pages | Low | Next.js public/ |
| 16 | **Rickroll placeholder** (`dQw4w9WgXcQ`) in YouTube embed code | Low | Next.js components |
| 17 | **Inconsistent team photo naming** — hyphens vs underscores (e.g., `niall-oulton.jpg` vs `niall_oulton.png`) | Low | Next.js public/users/ |
| 18 | **No image alt-text standards** — missing or inconsistent across both sites | Medium | Both repos |

---

## 6. Grand Totals

| Source | Files | Size | Notes |
|--------|------:|------|-------|
| Lektor content media | 306 | 127.76 MB | Blog images, team headshots, client logos |
| Lektor assets/static | 46 | 5.99 MB | Workshop images, logos, favicons, CSS/JS |
| Next.js public/ | 174 | 31.27 MB | Team photos, client logos, hero video, course assets |
| Next.js Cloudinary | 45 URLs | ~est. 2-5 MB | Team photos, instructor headshots, course banners |
| YouTube embeds | 158 URLs | External | Blog video content (Lektor), 3 embeds (Next.js) |
| **Combined local** | **526** | **165.02 MB** | |
| **After dedup** | ~490 | ~153 MB | Removing cross-repo duplicates |
| **After optimization** | ~490 | **~70-80 MB** | WebP conversion + resize + GIF→video |
