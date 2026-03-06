# Analysis Log — PyMC Labs Website Spec

| # | Aspect | Wave | Date | Notes |
|---|--------|------|------|-------|
| 1 | clone-source-repo | 1 | 2026-03-06 | Cloned pymc-labs-website-source (522 files). 329 blog posts, 53 team members, 18 clients. Lektor CMS + Pixi deps. File tree saved to raw/source-file-tree.txt. |
| 2 | clone-rebranded-repo | 1 | 2026-03-06 | Cloned pymc-rebranded-website (379 files). Next.js 16 + Strapi CMS backend. 22 page routes, 80 components, 174 public assets (32 MB). 4 courses, LLM benchmark tool, certificate system. No Strapi source in repo (deployed separately). File tree saved to raw/rebranded-file-tree.txt. |
| 3 | cache-redesign-plan | 1 | 2026-03-06 | No formal plan document found in either repo, issues, or PRs. Documented known redesign intent (Framer marketing + focused Next.js enrollment + Hugo blog) from loop context. Saved to input/redesign-plan.md. Wave 1 complete. |
| 4 | lektor-site-structure | 2 | 2026-03-06 | 10 models (blog_post, teammate, client, generic_page, index + collection parents). 22 templates (13 pages, 4 macros, 4 block templates, 1 sitemap). 4 flowblocks (text, image, html, testimonial). 2 databags (nav, contact). 4 plugins (3 community + 1 custom collapsible-code). Bootstrap 4.5.2 + jQuery 3.5.1 + FA 6.7.2 + MathJax 2.7.5. GA4, Mailchimp (newsletter + contact), Wise.com (workshop payments). 17 routes. Hardcoded author checkboxes, unused lektor-tags plugin, workshop page fully hardcoded in template. |
