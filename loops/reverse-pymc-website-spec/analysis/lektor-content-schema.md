# Lektor Content Schema — pymc-labs-website-source

## Overview

Lektor uses `.lr` (Lektor Record) files as its content format. Each content item lives in a directory under `content/`, with a `contents.lr` file containing field values and optional attachment files (images, PDFs) alongside it. Fields are separated by `---` delimiters. The format is:

```
field_name: value
---
another_field: value
---
multiline_field:

Multi-line content here...
```

Flow fields (used in `generic_page`) use a nested block syntax:

```
content:

#### block_type ####
field: value
----
another_field: value
#### block_type ####
...
```

Note: block field separators use `----` (4 dashes) vs. top-level `---` (3 dashes).

## Content Type Hierarchy

Lektor uses a parent-child model system. Parent models define collection containers; child models define the items within.

```
index (singleton)
├── blog_posts (collection parent)
│   └── blog_post (child, 52 items)
├── team (collection parent)
│   └── teammate (child, 26 items)
├── clients (collection parent)
│   └── client (child, 17 items + 1 hidden)
├── contact (collection parent, no children)
├── newsletter (collection parent, no children)
├── generic_page (5 pages: what-we-do, products, workshops, privacy-policy, impressum, terms-and-conditions)
├── sitemap (uses _template override, no model)
└── workshops/applied-bayesian-modeling (uses built-in `page` model + _template override)
```

## Detailed Field Schemas

### `index` — Homepage (`content/contents.lr`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Company name ("PyMC Labs") |
| `tagline` | string | yes | Tagline ("The Bayesian Consultancy") |
| `mission` | markdown | yes | One-line mission statement |
| `pitch_deck` | html | no | Google Slides embed HTML (defined in model but not used in current content) |
| `description` | markdown | no | Explicitly unused per model comment |

**Actual content**: Only `title`, `tagline`, and `mission` are populated. `pitch_deck` and `description` are absent from the .lr file.

### `blog_post` — Blog Posts (`content/blog-posts/<slug>/contents.lr`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Post title |
| `project_name` | string | no | Subtitle/project name (rarely used) |
| `authors` | checkboxes | yes | Author names (see Author Problem below) |
| `external_authors` | strings | no | One per line; only 1 post uses this field |
| `date` | date | yes | Publication date (YYYY-MM-DD) |
| `summary` | string | no | One-sentence summary for blog listing |
| `blog_post` | markdown | yes | Main body content |
| `youtube_video` | string | no | YouTube embed URL |
| `visible` | boolean | yes | Show on blog listing (all 52 are `yes`) |
| _(attachments)_ | files | — | Images referenced in markdown body |

**Content stats**:
- 52 blog post directories
- Date range: 2021-02-18 to 2025-06-02
- 14 posts include YouTube video embeds
- 0 posts are hidden (`visible: no`)
- 1 post explicitly uses `external_authors` (empty value)
- 1 post explicitly declares `_model: blog_post` (others rely on parent model's `[children]` config)
- Attachment counts range from 1 file (just `contents.lr` + cover) to 21 files (complex posts with many inline images)

**The Author Problem**: The `blog_post.ini` model defines `authors` as a `checkboxes` field with 13 hardcoded choices:

```
Adrian Seyboldt, Alex Andorra, Alexander Fengler, Tiann Van Der Merwe,
Benjamin Vincent, Bill Engels, Eric J. Ma, Luciano Paz, Maxim Kochurov,
Oriol Abril Pla, Ricardo Vieira, Thomas Wiecki, Tomás Capretto
```

However, **26 distinct author values** appear across blog posts, including:
- Authors not in the checkboxes: Juan Orduz (4 posts), Allen Downey (2), Chris Fonnesbeck (2), Niall Oulton (2), Austin Rochford, Camilo Saldarriaga, Luca Fiaschi, Martin Ingram, Nina Rismal, William Dean
- Multi-author strings as single values: "Ricardo Vieira, Adrian Seyboldt", "Nina Rismal and Luca Fiaschi", "Juan Orduz and Colt Allen"
- Name inconsistencies: "Alex Andorra" (checkbox) vs. "Alexandre Andorra and Rémi Louf" (content), "Tiann Van Der Merwe" (checkbox) vs. "Tiaan Van Der Merwe" (content)

This means the checkboxes constraint is not enforced at content level — authors are effectively free-text strings. The checkbox UI in Lektor admin is bypassed (content likely edited directly in files).

### `teammate` — Team Members (`content/team/<slug>/contents.lr`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Full name |
| `github_url` | url | no | GitHub profile |
| `twitter_url` | url | no | Twitter/X profile |
| `mastodon_url` | url | no | Mastodon profile |
| `linkedin_url` | url | no | LinkedIn profile |
| `personal_url` | url | no | Personal website |
| `specializations` | string | no | Comma-separated skills |
| `location` | string | no | Geographic location |
| `blurb` | string | no | Short bio (140 char guideline) |
| `extended_bio` | markdown | no | Detailed biography |
| `visible` | boolean | yes | Show on team page |
| `picture`* | string | no | External URL to headshot image |

*`picture` is NOT defined in `teammate.ini` but appears in 10 of 26 content files. Lektor silently ignores undefined fields. This is a legacy field — all team member directories also contain a `headshot.jpg` attachment file, which the template actually uses. The `picture` field points to external GitHub-hosted URLs from the old Hugo site and is effectively dead data.

**Content stats**:
- 26 team member directories
- 19 visible (`visible: yes`), 7 hidden (`visible: no`)
- Hidden members: Alona Krokhmal, Brandon Willard, George Ho, Larry Dong, Oriol Abril Pla, Ravin Kumar, Virgile Andreani
- Every directory contains `headshot.jpg` alongside `contents.lr`
- Social links vary: some have 1, some have all 5

### `client` — Clients (`content/clients/<slug>/contents.lr`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `client_name` | string | yes | Company name |
| `testimonial` | markdown | no | Client quote |
| `logo_filename` | string | yes | Filename referencing `assets/static/images/client_logos/` |
| `date` | date | no | Engagement date |
| `homepage_url` | url | no | Client website |

**Content stats**:
- 18 client directories total
- 1 hidden (`_hidden: yes`): Gain Theory
- 17 visible clients
- 4 clients have the `testimonial` field present but all are empty strings
- 0 clients have actual testimonial text
- Logo is a string filename (e.g., `akili.png`), not an image attachment — decoupled from content directory

**Data anomalies**:
- `appgrowth/contents.lr` contains an undeclared `client:` field (not in `client.ini`) alongside `client_name:` — likely a remnant from an earlier schema
- `clients/contents.lr` (the parent) declares `_model: testimonials` — a model that does not exist. Lektor falls back to its built-in default model, and the `[children]` config in `clients.ini` still routes children to the `client` model correctly.

### `generic_page` — Static Pages

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Page title |
| `content` | flow | yes | Flow field accepting `text`, `image`, `html` blocks |

**Pages using this model** (6 total):
| Page | Flow Blocks Used | Approximate Content |
|------|-----------------|---------------------|
| `/what-we-do/` | 8x text, 1x html | Company pitch, methodology, Google Slides embed |
| `/products/` | 3x text | CausalPy and PyMC-Marketing descriptions + images as markdown |
| `/workshops/` | 5x text | Workshop overview, testimonials as blockquotes, CTA |
| `/privacy-policy/` | 9x text | GDPR-compliant privacy policy |
| `/impressum/` | 1x text | German legal notice (PyMC OU, Estonia) |
| `/terms-and-conditions/` | 12x text | Workshop terms and conditions |

The `testimonial` flowblock (defined in `flowblocks/testimonial.ini`) is NOT listed in the `generic_page` model's `flow_blocks` whitelist (`text, image, html`), making it unusable in generic pages despite being defined.

### `contact` and `newsletter` — Minimal Parents

Both are collection parent models with no custom fields and no child content. Their `contents.lr` files:
- `contact/contents.lr`: empty (0 bytes)
- `newsletter/contents.lr`: `_model: testimonials` (references nonexistent model)

These exist purely as URL routes. The actual form functionality is in their templates (`contact.html` uses a Mailchimp iframe, `newsletter.html` uses a Mailchimp HTML form).

### `sitemap` — Template Override

`content/sitemap/contents.lr` contains only `_template: sitemap.html`. No model is specified — it uses Lektor's built-in page model. The template recursively lists all site pages.

### `workshops/applied-bayesian-modeling` — Hardcoded Workshop

```
_model: page
_hidden: true
_template: applied-bayesian-modeling.html
title: Applied Bayesian Modeling Workshop
body: (empty)
```

Uses Lektor's built-in `page` model, is hidden from navigation/listings, and delegates all rendering to a hardcoded template. All workshop content (schedule, pricing, instructors, FAQ) lives in `templates/applied-bayesian-modeling.html`, not in content files.

## Flow Block Schemas

### `text` (`flowblocks/text.ini`)

| Field | Type | Description |
|-------|------|-------------|
| `section_header` | string | Optional heading text |
| `section_level` | integer | Heading level (1-6) |
| `markdown` | markdown | Body content |

Most commonly used block. Often used with empty `section_header` and `section_level` when the heading is in the markdown itself.

### `image` (`flowblocks/image.ini`)

| Field | Type | Description |
|-------|------|-------------|
| `url` | url | Image URL |

Minimal — just a URL. A `class` field is commented out in the .ini source. Rarely used because images are typically embedded inline via markdown `![](filename)` syntax instead.

### `html` (`flowblocks/html.ini`)

| Field | Type | Description |
|-------|------|-------------|
| `html` | html | Raw HTML content |

Used for embeds (Google Slides iframe on what-we-do page).

### `testimonial` (`flowblocks/testimonial.ini`)

| Field | Type | Description |
|-------|------|-------------|
| `client` | text | Client name |
| `testmonial` | markdown | Testimonial text (note: **typo** — missing 'i') |

**Defined but unusable**: Not included in `generic_page.content`'s `flow_blocks` whitelist. No other model uses flow fields. This block is dead code.

## Lektor System Fields

Several Lektor system fields appear in content files:

| Field | Usage Count | Purpose |
|-------|-------------|---------|
| `_model` | 12 files | Explicit model declaration (normally inferred from parent) |
| `_template` | 2 files | Template override (sitemap, workshop) |
| `_hidden` | 2 files | Hide from queries/listings (Gain Theory client, workshop subpage) |

Most content relies on implicit model assignment via the parent's `[children]` configuration rather than explicit `_model` declarations.

## Schema Issues and Anomalies Summary

1. **No relational integrity**: Blog post authors are free-text strings, not linked to `teammate` records. Author names are inconsistent between blog posts and team member names.
2. **Ghost model reference**: `clients/contents.lr` and `newsletter/contents.lr` reference `_model: testimonials` which doesn't exist. Works due to Lektor's fallback behavior.
3. **Undefined fields in content**: `teammate` has `picture` field in 10 content files but not in model; `client` has `client` field in `appgrowth` but not in model. Lektor silently ignores these.
4. **Dead flowblock**: `testimonial` block exists but can't be used — not whitelisted in any flow field.
5. **Unused model fields**: `index.description`, `index.pitch_deck` have no content; `blog_post.external_authors` used once with empty value.
6. **No pagination**: `team.ini` has pagination commented out. Blog listing has no pagination either — all 52 posts render on one page.
7. **No tagging/categorization**: Despite `lektor-tags` plugin being installed, no tag fields exist in any model.
8. **Logo decoupling**: Client logos are plain string filenames referencing a separate static directory, not content attachments. Adding a client requires coordinating between content file and static assets.
9. **Hardcoded workshop**: The only course/workshop has all content in a template file, making it impossible to manage via Lektor's CMS admin.
10. **Empty testimonials**: The `testimonial` field exists on all clients but none have actual content — all are empty strings.
