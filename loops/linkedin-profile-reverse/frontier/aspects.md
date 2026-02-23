# Analysis Frontier — LinkedIn Profile

## Statistics
- Total aspects discovered: 13
- Analyzed: 6
- Pending: 7
- Convergence: 46%

## Pending Aspects (ordered by dependency)

### Wave 1: Raw Data Extraction
- [x] reference-profile-scan — Study 5-8 exemplary LinkedIn profiles of builders/engineers; extract headline structure, about hooks, experience framing, featured section patterns
- [x] monorepo-project-inventory — Deep scan monorepo projects/, loops/, CLAUDE.md to inventory everything impressive this person has built
- [x] org-work-analysis — Discover and analyze org/private work via GitHub orgs and monorepo project cards
- [x] github-profile-cross-ref — Pull any existing analysis from the github-profile-reverse loop (repo clustering, identity synthesis, narrative gaps)
- [x] linkedin-format-research — Research LinkedIn's actual format constraints: character limits, section rendering, mobile truncation, SEO/search behavior
- [x] current-profile-snapshot — Capture current LinkedIn profile state via WebFetch; identify what's missing or outdated

### Wave 2: Pattern Analysis (depends on Wave 1)
- [ ] reference-formula-extraction — Extract the formula: what makes reference profiles compelling? How do polymaths avoid looking scattered?
- [ ] career-narrative-arc — Map chronological arc from actual data; find the through-line connecting everything
- [ ] experience-entry-design — Design each LinkedIn experience entry: title, company, date range, bullet points, what to emphasize
- [ ] identity-synthesis — Synthesize headline drafts, about section draft, featured recommendations, skills list, tone calibration

### Wave 3: Synthesis (depends on all Wave 2)
- [ ] linkedin-profile-spec — Complete actionable spec: headline, about, all experience entries, featured, skills, execution checklist
- [ ] spec-review — Review spec against quality bar; check for personality, range, signal clarity, completeness

### Wave 4: Spec Fixes (populated during spec-review if needed)
(Empty — spec-review hasn't run yet)

## Recently Analyzed
- [x] reference-profile-scan — Profiles of swyx, Simon Willison, Pieter Levels, Addy Osmani + generic developer examples. Key insight: top builders own concepts, not job titles. Named products > generic responsibilities. Hook in first 2 lines is critical.
- [x] monorepo-project-inventory — Two production AI systems (Cheerful/Nuts+Bolts, Decision Orchestrator/PyMC Labs) + ralph loop engine. Platform thesis: same architectural DNA (Claude SDK, MCP, Supabase, Langfuse) across two domains. All impressive work is private/invisible. Key story: builds the infrastructure layer, not just apps.
- [x] org-work-analysis — Two orgs: Nuts and Bolts AI (Cheerful, influencer marketing automation) and PyMC Labs (Decision Orchestrator, organizational AI OS). Both use identical architectural DNA (Claude Agent SDK, custom MCP, Supabase, Langfuse, Composio). Neither role appears on current LinkedIn. Platform thesis confirmed: same stack, different domains = deliberate. Highest-ROI LinkedIn update is adding both as experience entries.
- [x] github-profile-cross-ref — GitHub loop has 3/12 aspects done (repo-inventory, profile-snapshot, monorepo-deep-scan). Key extractions: (1) Enormous public/private gap — public GitHub reads "inactive student," real work is 50k+ LOC of production AI infra. (2) Five thematic clusters identified: CV/ML research, numerical computing, HPC/systems, production AI (private), meta-systems (private). (3) Platform thesis confirmed independently: same stack (Claude SDK + MCP + Supabase + Langfuse) across two domains. (4) MCP registry built at protocol level = the key differentiator. (5) Academic arc (CUDA/Runge-Kutta/CV) → production AI infra is a coherent story. LinkedIn must tell the story GitHub cannot.
- [x] linkedin-format-research — Headline: 220 chars, highest SEO weight. About: 2600 chars, first ~200 visible before "See More" (mobile). Experience description: 2000 chars. Featured: links/media/posts, not indexed by search. No markdown in LinkedIn — use Unicode bullets (•). Key: front-load everything, hook = first 200 chars of About.
- [x] current-profile-snapshot — LinkedIn blocked WebFetch (999). Reconstructed from cross-refs: both current roles (Nuts+Bolts AI, PyMC Labs) are absent from profile. URL is opaque `wfo-wells`. No headline, no about, no skills visible. Critical gap: 50k+ LOC of production AI work completely invisible. Vanity URL, headline, about, and two experience entries all need to be written from scratch.

## Discovered Aspects
(Empty — no new aspects discovered yet)
