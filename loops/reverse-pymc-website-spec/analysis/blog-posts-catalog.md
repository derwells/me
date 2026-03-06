# Blog Posts Catalog

## Summary

- **Lektor site**: 52 blog posts (2021-02 to 2025-06), all visible, stored as `.lr` content files with inline markdown and attached images
- **Next.js site**: Blog content served entirely from Strapi CMS (`/api/articles`), no static blog content in repo. One 2,822-line placeholder `data.js` file exists but is unused (0 imports). Draft preview route at `/draft-post/[id]/`
- **Total blog images (Lektor)**: 276 files, 115 MB total (244 PNG, 24 SVG, 4 GIF, 2 WebP, 1 JPG, 1 JPEG)
- **Content not migratable from repo**: Next.js blog content lives in Strapi DB on Heroku -- must be exported via API, not from filesystem

## Lektor Blog Architecture

### Content Model (`models/blog_post.ini`)

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | Main title |
| `project_name` | string | Subtitle / short title (used on some video posts) |
| `authors` | checkboxes | 13 hardcoded choices, but free-text in practice |
| `external_authors` | strings | Multi-line external authors (rarely used) |
| `date` | date | Publication date |
| `summary` | string | One-sentence summary for listing page |
| `blog_post` | markdown | Main content body |
| `youtube_video` | string | YouTube embed URL (optional) |
| `visible` | boolean | Display toggle |
| `attachments` | enabled | File attachments (images) |

### Data Integrity Issues

1. **Author field mismatch**: Model defines 13 checkbox choices but content files use free-text with 26 unique author strings (including multi-author like "Benjamin Vincent, Maxim Kochurov"). No normalization.
2. **Summary field inconsistency**: 30 of 52 posts (58%) have the `summary` field. All 22 missing summaries are from 2022-07 onward -- appears the convention was abandoned mid-2022, then stopped entirely after 2023-06.
3. **No categories/tags**: Lektor blog has zero categorization. The `lektor-tags` plugin is installed but unused. All posts are in a flat list.
4. **No pagination**: Blog listing renders all 52 posts on a single page.

## Next.js Blog Architecture

### Strapi Article Content Type (reverse-engineered from API calls)

| Field | Type | Source |
|-------|------|--------|
| `title` | string | API |
| `slug` | string | URL identifier |
| `description` | string | Short description |
| `detail` | markdown (rich text) | Full blog body |
| `blog_created_date` | date | Custom field (falls back to `createdAt`) |
| `cover` | media (Cloudinary) | Cover image |
| `video` | string | YouTube embed URL |
| `featured` | boolean | Featured post flag |
| `meta_title` | string | SEO override |
| `meta_description` | string | SEO override |
| `categories` | relation (many-to-many) | Category objects with `name` |
| `authors` | relation (many-to-many) | Author objects with `name` |

### Features Added in Next.js

- **Category filtering**: Dynamic categories fetched from `/api/categories`, displayed as filter chips (top 4) + dropdown for rest
- **Category URL routes**: `/blog-posts/filters/[category]` for category-specific pages
- **Full-text search**: Client-side title search with 500ms debounce
- **Featured post**: `featured` boolean flag, featured post rendered with distinct layout
- **Pagination**: Server-side via Strapi pagination (12 per page, or 48 when checking for featured)
- **Related posts**: Fetches 6 posts from same first category
- **Table of Contents**: Auto-generated from headings in markdown
- **Collapsible code blocks**: Custom rehype plugin for `#!collapse` directive
- **Math rendering**: KaTeX (replacing Lektor's MathJax 2)
- **Draft preview**: `/draft-post/[id]` fetches `status=draft` articles (no auth required)
- **Markdown export**: `/blog-posts/[id]/md` API route returns post as markdown

### Placeholder Data File (unused)

`components/blog/data.js` (2,822 lines) contains hardcoded blog post array with lorem ipsum / gibberish descriptions, Unsplash placeholder images, and duplicate IDs. Zero components import this file. Likely a design prototype artifact.

## Complete Blog Post Catalog (Lektor)

### Posts by Year

| Year | Count | Posts with Video | Posts with Summary |
|------|-------|------------------|--------------------|
| 2021 | 7 | 0 | 7 |
| 2022 | 19 | 8 | 16 |
| 2023 | 13 | 5 | 7 |
| 2024 | 6 | 0 | 0 |
| 2025 | 7 | 2 | 0 |
| **Total** | **52** | **14** (27%) | **30** (58%) |

### Content Types

| Type | Count | Description |
|------|-------|-------------|
| Long-form technical article | 33 | Original markdown posts (50-3000+ lines) |
| Video + discussion notes | 14 | YouTube embed + panel discussion timestamps/notes |
| Cross-post / stub | 4 | Short intro linking to external content (< 30 lines) |
| Thought leadership | 1 | `labs-principles` — non-technical opinion piece |

### Author Frequency

| Author | Posts | Notes |
|--------|-------|-------|
| Thomas Wiecki | 12 | Co-founder, most video panel hosts |
| Benjamin Vincent | 8 | Also 2 co-authored |
| Juan Orduz | 4 | Also 1 co-authored |
| Ricardo Vieira | 2 | Also 3 co-authored |
| Niall Oulton | 2 | Marketing focus |
| Chris Fonnesbeck | 2 | Sports analytics |
| Allen Downey | 2 | Synthetic consumers series |
| Ricardo Vieira + Tomas Capretto | 2 | Co-authored |
| Others (1 post each) | 12 | William Dean, Tiaan Van Der Merwe, Alexander Fengler, Adrian Seyboldt, Ravin Kumar, Nina Rismal, Martin Ingram, Luciano Paz, Luca Fiaschi, Eric J. Ma, Camilo Saldarriaga, Bill Engels, Austin Rochford |

**Total unique author strings**: 26 (including multi-author variants)
**Unique individual authors**: ~22

### Full Post List

| # | Date | Slug | Title | Authors | Video | Images | Lines |
|---|------|------|-------|---------|-------|--------|-------|
| 1 | 2021-02-18 | saving-the-world | Introducing PyMC Labs | Thomas Wiecki | No | 2 | 133 |
| 2 | 2021-02-25 | everysk | Bayesian model to infer private equity returns from capital in and outflows | Ravin Kumar | No | 1 | 77 |
| 3 | 2021-05-26 | markov-process | Estimating a Candidate's Popularity over Time with Markov Processes | Alexandre Andorra and Remi Louf | No | 20 | 3053 |
| 4 | 2021-09-17 | bayesian-media-mix-modeling-for-marketing-optimization | Bayesian Media Mix Modeling for Marketing Optimization | Benjamin Vincent | No | 6 | 95 |
| 5 | 2021-09-21 | reducing-customer-acquisition-costs-how-we-helped-optimizing-hellofreshs-marketing-budget | Improving the Speed and Accuracy of Bayesian Media Mix Models | Benjamin Vincent | No | 3 | 67 |
| 6 | 2021-10-22 | bayes-is-slow-speeding-up-hellofreshs-bayesian-ab-tests-by-60x | Bayes is slow? Speeding up HelloFresh's Bayesian AB tests by 60x | Benjamin Vincent | No | 5 | 79 |
| 7 | 2021-12-22 | pymc-stan-benchmark | MCMC for big datasets: faster sampling with JAX and the GPU | Martin Ingram | No | 7 | 224 |
| 8 | 2022-01-03 | the-quickest-migration-guide-ever-from-pymc3-to-pymc-v40 | The Quickest Migration Guide Ever from PyMC3 to PyMC v4.0 | Eric J. Ma | No | 1 | 169 |
| 9 | 2022-01-10 | labs-principles | My Journey Building PyMC Labs: Five Principles from Open Source | Thomas Wiecki | No | 1 | 129 |
| 10 | 2022-01-15 | 01-xpost-tw-stochastic-volatility | Stochastic Volatility Model with PyMC | Thomas Wiecki | No | 1 | 20 |
| 11 | 2022-05-15 | 04-xpost-be-time-series-volcano | Building Time-Series Models With Known Data Structure | Bill Engels | No | 1 | 25 |
| 12 | 2022-05-16 | pymc-in-browser | Running PyMC in the Browser with PyScript | Thomas Wiecki | No | 1 | 114 |
| 13 | 2022-06-15 | 02-xpost-tw-MCMC-sampling | MCMC sampling for dummies | Thomas Wiecki | No | 1 | 26 |
| 14 | 2022-06-24 | bayesian-vector-autoregression | Bayesian Vector Autoregression in PyMC | Ricardo Vieira | No | 11 | 654 |
| 15 | 2022-07-10 | 2022-07-10-ricardo-video | PyMC, Aesara and AePPL: The New Kids on The Block | Ricardo Vieira | Yes | 1 | 362 |
| 16 | 2022-07-13 | causal-inference-in-pymc | What if? Causal inference through counterfactual reasoning in PyMC | Benjamin Vincent | No | 7 | 160 |
| 17 | 2022-07-15 | 03-xpost-ar-nba-irt | NBA Foul Analysis with Item Response Theory using PyMC | Austin Rochford | No | 1 | 27 |
| 18 | 2022-07-19 | modelling-changes-marketing-effectiveness-over-time | Bayesian Media Mix Models: Modelling changes in marketing effectiveness over time | Benjamin Vincent | No | 6 | 85 |
| 19 | 2022-08-11 | 2022-08-11-indigo | Bayesian Modeling in Biotech: Using PyMC to Analyze Agricultural Data | Thomas Wiecki | Yes | 1 | 72 |
| 20 | 2022-08-12 | bayesian-inference-at-scale-running-ab-tests-with-millions-of-observations | Bayesian inference at scale: Running A/B tests with millions of observations | Benjamin Vincent, Maxim Kochurov | No | 7 | 187 |
| 21 | 2022-08-17 | spatial-gaussian-process-01 | Modeling spatial data with Gaussian processes in PyMC | Luciano Paz | No | 11 | 548 |
| 22 | 2022-10-26 | 2022-10-26-AlvaLabs | Bayesian Item Response Modeling in PyMC | Thomas Wiecki | Yes | 1 | 77 |
| 23 | 2022-10-31 | Thomas_PyData_London | Solving Real-World Business Problems with Bayesian Modeling | Thomas Wiecki | Yes | 1 | 105 |
| 24 | 2022-11-11 | 2022-11-11-HelloFresh | Bayesian Marketing Mix Models: State of the Art and their Future | Thomas Wiecki | Yes | 1 | 72 |
| 25 | 2022-11-17 | causalpy-a-new-package-for-bayesian-causal-inference-for-quasi-experiments | CausalPy - causal inference for quasi-experiments | Benjamin Vincent | No | 3 | 64 |
| 26 | 2022-12-08 | 2022-12-08-Salk | Hierarchical Bayesian Modeling of Survey Data with Post-stratification | Thomas Wiecki | Yes | 1 | 66 |
| 27 | 2023-01-03 | jax-functions-in-pymc-3-quick-examples | How to use JAX ODEs and Neural Networks in PyMC | Ricardo Vieira, Adrian Seyboldt | No | 5 | 729 |
| 28 | 2023-01-12 | 2023-01-12-Akili | Likelihood Approximations for Cognitive Modeling with PyMC | Thomas Wiecki | Yes | 1 | 102 |
| 29 | 2023-03-31 | likelihood-approximations-through-neural-networks | Likelihood Approximations with Neural Networks in PyMC | Ricardo Vieira, Alexander Fengler | No | 13 | 1546 |
| 30 | 2023-04-06 | pymc-marketing-a-bayesian-approach-to-marketing-data-science | PyMC-Marketing: A Bayesian Approach to Marketing Data Science | Benjamin Vincent | Yes | 3 | 92 |
| 31 | 2023-04-20 | simulating-data-with-pymc | Simulating data with PyMC | Ricardo Vieira, Tomas Capretto | No | 10 | 558 |
| 32 | 2023-06-12 | out-of-model-predictions-with-pymc | Out of model predictions with PyMC | Ricardo Vieira, Tomas Capretto | No | 15 | 2216 |
| 33 | 2023-06-20 | 2023-06-20-juan-marketing-analytics | Bayesian Methods in Modern Marketing Analytics | Thomas Wiecki | Yes | 1 | 118 |
| 34 | 2023-07-31 | 2023-07-18-niall-In-house-marketing | Building an in-house marketing analytics solution | Niall Oulton | Yes | 1 | 93 |
| 35 | 2023-08-01 | causal-analysis-with-pymc-answering-what-if-with-the-new-do-operator | Causal analysis with PyMC: Answering "What If?" with the new do operator | Benjamin Vincent, Thomas Wiecki | No | 11 | 411 |
| 36 | 2023-09-25 | from-uncertainty-to-insight-how-bayesian-data-science-can-transform-your-business | From Uncertainty to Insight: How Bayesian Data Science Can Transform Your Business | Tiaan Van Der Merwe | No | 4 | 125 |
| 37 | 2023-09-26 | 2023-09-15-Hierarchical-models-Chris-Fonnesbeck | Developing Hierarchical Models for Sports Analytics | Chris Fonnesbeck | Yes | 1 | 125 |
| 38 | 2023-10-27 | 2023-10-27-Latent-calendar-Will | Latent Calendar: Modeling Weekly Behavior with Latent Components | William Dean | Yes | 1 | 96 |
| 39 | 2023-11-19 | 2023-19-11-marketing-effectiveness | Mastering Marketing Effectiveness: A Comprehensive Guide for Digital Marketers | Niall Oulton | No | 1 | 74 |
| 40 | 2024-05-14 | cohort-revenue-retention | Cohort Revenue & Retention Analysis | Juan Orduz | No | 19 | 348 |
| 41 | 2024-05-28 | pareto-nbd | Customer Lifetime Value in the non-contractual continuous case | Juan Orduz and Colt Allen | No | 10 | 162 |
| 42 | 2024-07-26 | hierarchical_clv | Hierarchical Customer Lifetime Value Models | Juan Orduz | No | 7 | 201 |
| 43 | 2024-08-01 | bayesian-marcel | Bayesian Baseball Monkeys | Chris Fonnesbeck | No | 9 | 849 |
| 44 | 2024-08-12 | mmm_roas_lift | Unobserved Confounders, ROAS and Lift Tests in Media Mix Models | Juan Orduz | No | 9 | 647 |
| 45 | 2024-09-19 | causal-sales-analytics-are-my-sales-incremental-or-cannibalistic | Causal sales analytics: Are my sales incremental or cannibalistic? | Benjamin Vincent | No | 8 | 124 |
| 46 | 2025-02-24 | the-ai-mmm-agent | The AI MMM Agent: An AI-Powered Shortcut to Bayesian Marketing Mix Insights | Luca Fiaschi | Yes | 4 | 93 |
| 47 | 2025-03-25 | how-realistic-are-synthetic-consumers | How Realistic Are Synthetic Consumers? | Allen Downey | No | 5 | 79 |
| 48 | 2025-03-26 | synthetic-consumers | Synthetic Consumers: The Promise, The Reality, and The Future | Nina Rismal and Luca Fiaschi | No | 3 | 46 |
| 49 | 2025-04-28 | probabilistic-forecasting | Probabilistic Time Series Analysis: Opportunities and Applications | Juan Orduz | No | 10 | 326 |
| 50 | 2025-05-13 | synthetic-consumers-open-ended-responses | Can Synthetic Consumers Answer Open-Ended Questions? | Allen Downey | No | 3 | 224 |
| 51 | 2025-05-29 | bayesian_computation_in_finance | Application of Bayesian Computation in Finance | Camilo Saldarriaga | No | 11 | 180 |
| 52 | 2025-06-02 | innovation-lab | AI Innovation Lab: An agentic platform for transforming product development | Nina Rismal | Yes | 9 | 124 |

## Topic Analysis (inferred from titles)

| Topic Area | Post Count | Examples |
|------------|------------|----------|
| Marketing Mix Models / MMM | 8 | bayesian-media-mix-modeling, mmm_roas_lift, the-ai-mmm-agent |
| Customer Lifetime Value / CLV | 4 | pareto-nbd, hierarchical_clv, cohort-revenue-retention |
| Causal Inference | 4 | causal-inference-in-pymc, causalpy, causal-sales-analytics |
| PyMC Core / Technical | 7 | pymc-stan-benchmark, jax-functions, simulating-data-with-pymc |
| A/B Testing | 2 | bayes-is-slow, bayesian-inference-at-scale |
| Time Series / Forecasting | 3 | bayesian-vector-autoregression, probabilistic-forecasting |
| Gaussian Processes | 2 | spatial-gaussian-process-01, time-series-volcano |
| Case Studies (client panels) | 6 | Indigo, AlvaLabs, HelloFresh, Salk, Akili |
| Synthetic Consumers / AI | 3 | synthetic-consumers, how-realistic, open-ended-responses |
| Finance | 2 | everysk, bayesian_computation_in_finance |
| Cross-posts / Stubs | 4 | 01-xpost-tw, 02-xpost-tw, 03-xpost-ar, 04-xpost-be |
| Other (misc) | 7 | labs-principles, pymc-in-browser, markov-process, etc. |

## Image Optimization Findings

### Largest Images (> 2 MB)

| File | Size | Post |
|------|------|------|
| modelling-changes-marketing-effectiveness-over-time/new-a.gif | 5.9 MB | Marketing effectiveness |
| 2023-19-11-marketing-effectiveness/cover.png | 4.9 MB | Marketing effectiveness guide |
| causalpy/cover.png | 3.3 MB | CausalPy |
| likelihood-approximations/weibull.gif | 2.9 MB | Likelihood approximations |
| bayesian_computation_in_finance/cover.png | 2.9 MB | Finance |
| innovation-lab/cover.png | 2.8 MB | Innovation Lab |
| pymc-marketing/cover.png | 2.5 MB | PyMC Marketing |
| synthetic-consumers-open-ended-responses/cover.png | 2.2 MB | Synthetic consumers |
| how-realistic-are-synthetic-consumers/cover.png | 2.0 MB | Synthetic consumers |

**Total > 1 MB images**: ~20 files
**Optimization opportunity**: Converting PNGs to WebP and GIFs to video could reduce 115 MB to ~20-30 MB.

## Slug Inconsistencies

Multiple naming conventions in use:
- **Date-prefixed**: `2022-07-10-ricardo-video`, `2023-19-11-marketing-effectiveness`
- **Cross-post prefixed**: `01-xpost-tw-stochastic-volatility`
- **Title-based kebab**: `bayesian-media-mix-modeling-for-marketing-optimization`
- **Underscore mixed**: `bayesian_computation_in_finance`, `hierarchical_clv`, `mmm_roas_lift`
- **CamelCase**: `Thomas_PyData_London`
- **Date in slug is wrong**: `2023-19-11-marketing-effectiveness` (19th month doesn't exist; actual date: 2023-11-19)
- **Slug/date mismatch**: `2023-07-18-niall-In-house-marketing` has `date: 2023-07-31`

## Migration Considerations

1. **Lektor to Hugo/other SSG**: Blog content is self-contained in `.lr` files with attached images. Migration requires parsing `.lr` format (simple `---` delimited key-value) into frontmatter + markdown body.
2. **Next.js/Strapi content**: Must export from Strapi API before Heroku shutdown. The `/api/articles?pagination[pageSize]=1000` endpoint can dump all content. Blog body is markdown in `detail` field.
3. **Image hosting**: Lektor images are local files (115 MB). Next.js images are on Cloudinary. Both need consolidation.
4. **URL redirects needed**: Lektor uses `/blog-posts/<slug>/`, Next.js uses `/blog-posts/<slug>`. Same path structure, so redirects mainly needed for any slug changes.
5. **Categories**: Only exist in Strapi. Lektor posts would need categorization during migration.
6. **Authors**: Neither system has a proper author entity with profiles. Lektor uses free-text, Strapi has a basic author model (name only).
7. **Video posts**: 14 posts (27%) include YouTube embeds. These need special handling in any blog platform.

## Issues Found

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| 1 | Medium | 22 posts missing summary field (all post-2022-07) | Lektor content |
| 2 | Low | Author field model (checkboxes) doesn't match content (free-text) | `models/blog_post.ini` vs content |
| 3 | Low | 4 cross-post stubs with minimal content (20-27 lines) | 01-04 xpost slugs |
| 4 | Medium | Date typo in slug: `2023-19-11` (month 19) | 2023-19-11-marketing-effectiveness |
| 5 | Low | Mixed slug conventions (kebab, underscore, CamelCase, date-prefix) | Multiple posts |
| 6 | Low | No categories/tags in Lektor (lektor-tags plugin installed but unused) | Lektor site |
| 7 | Info | Unused 2,822-line placeholder data.js in Next.js repo | `components/blog/data.js` |
| 8 | Medium | Draft blog posts accessible without auth in Next.js | `/draft-post/[id]` route |
| 9 | Low | console.log in production blog listing component | `BlogContent.jsx:142` |
| 10 | Low | JSON-LD uses `/blog/` path but actual route is `/blog-posts/` | `app/blog-posts/[id]/page.jsx:44` |
