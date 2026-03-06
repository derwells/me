# Clone Source Repo — Data Acquisition

## Summary

Successfully cloned `pymc-labs/pymc-labs-website-source` (shallow, `--depth 1`) to `input/pymc-labs-website-source/`.

- **Default branch:** `master`
- **Total files (including .git):** 551
- **Total files (excluding .git):** 522
- **File tree saved to:** `raw/source-file-tree.txt`

## Repository Structure

| Directory | File Count | Description |
|-----------|-----------|-------------|
| `content/blog-posts/` | 329 | Blog post `.lr` files and associated media |
| `content/team/` | 53 | Team member profiles |
| `assets/static/` | 46 | Static assets (CSS, JS, images, favicons, workshop assets) |
| `content/clients/` | 18 | Client entries (logos, descriptions) |
| `templates/` | ~16 | Jinja2 HTML templates (layout, pages, macros, blocks) |
| `content/workshops/` | 4 | Workshop/course content |
| `content/products/` | 3 | Product pages |
| `resources/` | 3 | Hugo-style generated resources |
| `.github/workflows/` | 3 | CI/CD: `main.yml`, `deploy-previews.yml`, `merge-schedule.yml` |
| `models/` | ~6 | Lektor model definitions (`.ini` files) |
| `flowblocks/` | ~4 | Lektor flowblock definitions |
| `databags/` | ~2 | Lektor databag JSON files |
| `packages/` | 2 | Custom Lektor plugin: `collapsible-markdown-code-snippets` |
| `configs/` | 1+ | Configuration files |
| `docs/` | 1+ | Documentation |

## Top-Level Config Files

- `pymc-labs.lektorproject` — Lektor project configuration
- `pixi.toml` / `pixi.lock` — Pixi (conda-based) dependency management
- `AGENTS.md` — AI agent instructions (Cursor/Codex)
- `.devcontainer/` — Dev container setup (Dockerfile + devcontainer.json)

## Key Observations

1. **Content-heavy repo:** 329 blog post entries dominate the file count, plus 53 team members and 18 clients.
2. **Lektor CMS:** Standard Lektor project structure with models, templates, flowblocks, databags, and content directories.
3. **Pixi for dependencies:** Uses Pixi (conda-based) rather than pip/requirements.txt — modern Python dependency management.
4. **Three CI workflows:** Main deploy, preview deploys, and a merge schedule workflow.
5. **Custom plugin:** `collapsible-markdown-code-snippets` package in `packages/` — custom Lektor plugin for code display.
6. **Workshop assets:** Dedicated static assets for "Applied Bayesian Modeling" workshop with instructor images and CSS.
7. **Client logos:** 18 client logo PNGs in `assets/static/images/client_logos/` (Roche, HelloFresh, Gates Foundation, Columbia University, etc.).
