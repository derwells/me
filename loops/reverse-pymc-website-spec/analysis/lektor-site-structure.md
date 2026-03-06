# Lektor Site Structure — pymc-labs-website-source

## Overview

The production PyMC Labs website is a **Lektor** static site (Python-based CMS) using Jinja2 templates, Bootstrap 4, and deployed to GitHub Pages. The project file is `pymc-labs.lektorproject`.

- **URL**: https://pymc-labs.github.io/ (canonical)
- **Locale**: en_US
- **Deploy targets**: GitHub Pages via `ghpages://` protocol (SSH and HTTPS variants)
- **Package manager**: Pixi (conda-forge + pypi channels)
- **Python version**: 3.9

## Models (10 total)

All defined in `models/*.ini`:

| Model | File | Type | Notable Fields |
|-------|------|------|----------------|
| `index` | `index.ini` | Singleton | title (string), tagline (string), mission (markdown), pitch_deck (html), description (markdown, unused) |
| `blog_posts` | `blog_posts.ini` | Collection parent | Children: `blog_post` |
| `blog_post` | `blog_post.ini` | Child item | title, project_name, authors (checkboxes, 13 hardcoded names), external_authors (strings), date, summary, blog_post (markdown), visible (boolean), youtube_video (string) |
| `team` | `team.ini` | Collection parent | Children: `teammate` |
| `teammate` | `teammate.ini` | Child item | name, github_url, twitter_url, mastodon_url, linkedin_url, personal_url, specializations, location, blurb (140 chars), extended_bio (markdown), visible (boolean) |
| `clients` | `clients.ini` | Collection parent | Children: `client` |
| `client` | `client.ini` | Child item | client_name, testimonial (markdown), logo_filename (string, references `assets/static/images/client_logos/`), date, homepage_url |
| `contact` | `contact.ini` | Collection parent | Children: self-referencing |
| `newsletter` | `newsletter.ini` | Collection parent | Children: self-referencing |
| `generic_page` | `generic_page.ini` | Page | title, content (flow field: text, image, html blocks) |

### Key Observations
- The `blog_post.authors` field uses hardcoded `checkboxes` choices (13 authors) rather than a relational lookup to the `teammate` model. Comment in source: "I'm not sure how to dynamically load choices from another model yet."
- The `client.logo_filename` is a plain string referencing files in a static directory — not an attachment or image field.
- `contact` and `newsletter` models are minimal collection parents with no custom fields.

## Templates (22 files)

Located in `templates/`:

### Page Templates (13)
| Template | Model | Purpose |
|----------|-------|---------|
| `layout.html` | — | Base layout: navbar, footer, Bootstrap 4, Font Awesome 6, MathJax, Google Analytics, Pygments CSS, header anchor links |
| `index.html` | `index` | Homepage: hero image, value proposition, YouTube embed, mission, contact info from databag |
| `blog_posts.html` | `blog_posts` | Blog listing: sorted by date descending, visible filter |
| `blog_post.html` | `blog_post` | Single post: title, summary, authors, date, YouTube embed or cover image, markdown body, CTA footer |
| `team.html` | `team` | Team listing: sorted by name, visible filter |
| `teammate.html` | `teammate` | Individual profile: headshot, bio, specializations, location, social links |
| `clients.html` | `clients` | Client grid: Bootstrap card-columns layout |
| `client.html` | `client` | Individual client page |
| `contact.html` | `contact` | Mailchimp contact form (embedded iframe from `us10.list-manage.com`) |
| `newsletter.html` | `newsletter` | Mailchimp newsletter subscription form (embedded HTML form) |
| `generic_page.html` | `generic_page` | Generic flow-based page: iterates over text/html/image blocks |
| `sitemap.html` | — | Recursive sitemap listing all pages |
| `html.html` | — | Empty template (extends layout, empty body block) |
| `applied-bayesian-modeling.html` | — | Standalone workshop landing page: hardcoded course schedule, pricing ($1,499/$1,699), instructor bios, FAQ, testimonial carousel, Wise.com payment link |

### Macros (4)
| Macro | File | Functions |
|-------|------|-----------|
| `macros/blog_post.html` | Blog helpers | `render_blog_post_card()`, `render_cover_image()`, `render_blog_post_page()`, `render_date()`, `render_authors()`, `render_blog_post_og_image()` |
| `macros/teammate.html` | Team helpers | `render_teammate_card()`, `render_teammate_page()` |
| `macros/client.html` | Client helpers | `render_client()` |
| `macros/slideshow.html` | Carousel | `render_slideshow()` (Bootstrap carousel for image attachments) |

### Block Templates (4)
For flowblock rendering in `generic_page`:
| Block | Template |
|-------|----------|
| `blocks/text.html` | — |
| `blocks/image.html` | — |
| `blocks/html.html` | — |
| `blocks/testimonial.html` | — |

## Flowblocks (4)

Defined in `flowblocks/*.ini`, used by `generic_page.content` flow field:

| Block | Fields |
|-------|--------|
| `text` | section_header (string), section_level (integer), markdown (markdown) |
| `image` | url (url) — class field commented out |
| `html` | html (html) |
| `testimonial` | client (text), testmonial [sic] (markdown) — note typo in field name |

## Databags (2)

JSON data stores in `databags/`:

| Databag | File | Contents |
|---------|------|----------|
| `contact` | `contact.json` | `{ name: "Thomas Wiecki", email: "info@pymc-labs.com" }` |
| `nav` | `nav.json` | Header nav (6 items: What we do, Products, Team, Clients, Workshops, Blog) + Footer nav (8 items: Twitter, GitHub, LinkedIn, YouTube, Meetup, Newsletter, Privacy Policy, Impressum) |

## Plugins & Packages

### Registered Lektor Plugins (from `.lektorproject`)
| Plugin | Version | Purpose |
|--------|---------|---------|
| `lektor-markdown-header-anchors` | 0.3 | Auto-generates anchor IDs on headings |
| `lektor-markdown-highlighter` | 0.3 | Syntax highlighting via Pygments (configured: `tango` style in `configs/markdown-highlighter.ini`) |
| `lektor-tags` | 0.2 | Tag support (though tags are not visible in models or templates) |

### Custom Plugin (in `packages/`)
- **`collapsible-markdown-code-snippets`** (v0.0.1) — Custom Lektor plugin that adds `#!collapse` and `#!hide` directives to code blocks. `#!collapse` wraps code in a Bootstrap collapse toggle; `#!hide` suppresses rendering entirely. Inserted as first renderer mixin (runs before highlighter).

## Content Directory Structure

Top-level `content/` contains 14 entries:

| Path | Model Used | Count |
|------|-----------|-------|
| `content/contents.lr` | `index` | 1 (homepage) |
| `content/blog-posts/` | `blog_posts` → `blog_post` | 53 subdirectories |
| `content/team/` | `team` → `teammate` | 27 subdirectories |
| `content/clients/` | `clients` → `client` | 18 subdirectories |
| `content/contact/` | `contact` | 1 |
| `content/newsletter/` | `newsletter` | 1 |
| `content/what-we-do/` | `generic_page` | 1 |
| `content/products/` | `generic_page` | 1 |
| `content/workshops/` | `generic_page` | 1 |
| `content/privacy-policy/` | `generic_page` | 1 |
| `content/impressum/` | `generic_page` | 1 |
| `content/terms-and-conditions/` | `generic_page` | 1 |
| `content/sitemap/` | sitemap | 1 |
| `content/robots.txt` | — | Static file |

**Note**: Wave 1 counted 329 blog posts, but only 53 directories exist in `content/blog-posts/`. The discrepancy likely came from counting all files (including attachments within blog post directories) vs. just the blog post directories themselves.

## Static Assets

Located in `assets/static/`:

| Directory | Contents |
|-----------|----------|
| `css/` | `custom_style.css`, `table_style.css` |
| `scripts/` | `toggle_code.js` |
| `images/` | `pymc-labs-logo.png`, `pymc-labs-icon.png`, `pymc_labs_home.jpeg`, `blog_post/` (default cover), `client_logos/` |
| `workshops/` | `applied-bayesian-modeling/` (CSS, JS, images for workshop landing page) |
| Root | `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png` |

## Frontend Stack

| Component | Version/Source |
|-----------|---------------|
| Bootstrap | 4.5.2 (CDN) |
| jQuery | 3.5.1 slim (CDN) |
| Popper.js | 1.16.1 (CDN) |
| Font Awesome | 6.7.2 (CDN + kit 8cc267a9ab) |
| MathJax | 2.7.5 (CDN, TeX inline `$...$`) |
| Highlight.js | 10.7.2 (CSS CDN, but commented out JS — Pygments used instead) |
| Google Fonts | Inter (workshop page only) |

## External Services (from templates)

| Service | Integration Point |
|---------|-------------------|
| **Google Analytics** | GA4 tag `G-F3RDLH8R8X` in `layout.html` |
| **Mailchimp** | Newsletter form (list `ffcf543278f48b79571b62010`, form ID `cdca7f3ebb`); Contact form (iframe embed) |
| **YouTube** | Embedded videos on homepage and blog posts |
| **Wise.com** | Payment link for workshop enrollment (`wise.com/pay/r/elkuVRPWrYJR3rI`) |

## Route Map (from nav.json + content structure)

| Route | Template/Content |
|-------|-----------------|
| `/` | `index.html` (homepage) |
| `/what-we-do/` | `generic_page.html` |
| `/products/` | `generic_page.html` |
| `/team/` | `team.html` |
| `/team/<slug>/` | `teammate.html` |
| `/clients/` | `clients.html` |
| `/clients/<slug>/` | `client.html` |
| `/workshops/` | `generic_page.html` |
| `/workshops/applied-bayesian-modeling/` | `applied-bayesian-modeling.html` (hardcoded template) |
| `/blog-posts/` | `blog_posts.html` |
| `/blog-posts/<slug>/` | `blog_post.html` |
| `/contact/` | `contact.html` |
| `/newsletter/` | `newsletter.html` |
| `/privacy-policy/` | `generic_page.html` |
| `/impressum/` | `generic_page.html` |
| `/terms-and-conditions/` | `generic_page.html` |
| `/sitemap/` | `sitemap.html` |

## Dependencies (from pixi.toml)

| Package | Pinned Version |
|---------|---------------|
| Python | 3.9.* |
| Lektor | >=3.3.9 |
| Flask | 2.3.1.* |
| Requests | 2.29.0.* |
| Jinja2 | 3.1.2.* |
| Werkzeug | 2.3.0.* |
| Pygments | * (unpinned) |
| Mistune | 0.8.4.* |

## Notable Issues / Surprises

1. **Hardcoded author checkboxes** — Blog post authors are a static list in `blog_post.ini`, not linked to the `teammate` model. Adding a new author requires editing the model file.
2. **Typo in flowblock** — `testimonial.ini` has field `testmonial` (missing 'i').
3. **Unused `lektor-tags` plugin** — Registered in `.lektorproject` but no tag fields in models or tag-related templates exist.
4. **Workshop page is fully hardcoded** — `applied-bayesian-modeling.html` has all content (schedule, pricing, instructors, FAQ) directly in the template, not in content files.
5. **Duplicate Font Awesome loading** — Both CDN CSS and FA Kit JS loaded in `layout.html`.
6. **MathJax v2** — Using end-of-life MathJax 2.7.5 (MathJax 3 is current).
7. **Bootstrap 4** — End of life; Bootstrap 5 is current.
8. **Python 3.9** — Reaches end of life October 2025, already past EOL as of analysis date.
9. **Mistune 0.8.4** — Extremely old markdown parser; current is 3.x. Known security issues in 0.x line.
10. **Contact form uses iframe** — Not a native form; depends on Mailchimp hosted page availability.
