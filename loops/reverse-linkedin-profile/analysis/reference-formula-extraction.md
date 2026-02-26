# Reference Formula Extraction

**Analyzed**: 2026-02-23
**Sources**: `analysis/reference-profile-scan.md`, `analysis/linkedin-format-research.md`, `analysis/monorepo-project-inventory.md`, `analysis/org-work-analysis.md`, `analysis/github-profile-cross-ref.md`

---

## The Core Formula

Great LinkedIn profiles share one structural secret: **they describe what you made, not what you do.**

swyx doesn't say "Developer Relations professional." He says "Editor of Latent.Space. Fostering the Rise of the AI Engineer."
Simon Willison doesn't say "open source developer." He says "Creator of Datasette. Co-creator of Django."
Addy Osmani doesn't say "senior engineer at Google." He says "Engineering Leader, Google Chrome. Best-selling Author."

The formula: **Named things + Intellectual ownership > Job category + Role level**

This is the lens through which to evaluate every line on derwells' profile.

---

## Formula 1: Concept Ownership vs. Job Title Ownership

**The pattern**: The most compelling profiles anchor identity to something the person *made or coined* — not to a job category they *belong to*.

| Forgettable | Compelling |
|-------------|------------|
| "Senior Software Engineer" | "Creator of Datasette" |
| "AI/ML Developer" | "Fostering the Rise of the AI Engineer" |
| "Full-Stack Developer" | "Built what makes AI agents reliable in production" |

**Applied to derwells**: The specific things he owns are:
1. A **protocol-level MCP registry** — not a user of MCP tools, builder of MCP infrastructure
2. A **platform thesis** — same architecture stack applied deliberately across two different production deployments
3. **Temporal.io for AI workflows** — durable, crash-resistant campaign execution in production

None of these are job categories. They are specific things he built. The profile must lead with these, not with "AI Engineer."

---

## Formula 2: How to Handle Breadth vs. Depth (The Polymath Paradox)

**The problem**: derwells has genuine breadth — CUDA, CV/ML research, numerical computing, C systems programming, full-stack web (React 19), compiler theory, AI agent infrastructure. This can read as "scattered student" or "rare generalist" depending entirely on how it's framed.

**What reference profiles do**: They lead with depth on ONE primary identity, then let breadth unfurl as the *explanation* for why they're unusually good at that one thing.

Addy Osmani writes about JavaScript design patterns AND Stoic philosophy — this reads as "deep thinker with range" not "confused engineer" because engineering is his primary anchor and philosophy is explicitly a side of him. The books are named things, not genre labels.

Simon Willison's breadth (Django co-creator → Lanyrd founder → Eventbrite director → solo open source → AI blogging) reads coherently because every step is a named thing with verifiable context, not a category claim.

**The formula for breadth**:
```
[Deep anchor: the specific thing you're known for]
[Origin: where the breadth came from, as a story]
[Breadth as "also built this, also know this" — never as the lead]
```

**Applied to derwells**:
- Deep anchor: AI agent infrastructure (Temporal.io, MCP registry, Claude Agent SDK) at two production orgs
- Origin: scientific computing (CUDA, Runge-Kutta, CV research, HPC) → production AI systems — this arc *explains* the infrastructure rigor
- Breadth signals: CUDA kernels, React 19 frontends, Langfuse observability — mentioned as proof of range, never as the headline

The CUDA background explains *why* someone's infrastructure thinking is lower-level than average. The React 19 frontend work explains *why* the API design is consumer-aware. The breadth strengthens the depth claim when framed as backstory.

---

## Formula 3: Hook Architecture (The First 200 Characters)

**The constraint**: ~200 characters visible before "See More" on mobile (57%+ of LinkedIn traffic). This is the only thing most people read. The hook must earn the click — or the profile has failed.

**Hook taxonomy from reference profiles**:

| Type | Example | Mechanism |
|------|---------|-----------|
| Contrast hook | "Most AI apps are wrappers. I build the layer underneath." | Creates immediate distinction |
| Claim hook | "I caught fire coding." | Emotion + specificity = memorability |
| Origin hook | "It started with CUDA kernels." | Curiosity about the arc |
| Number hook | "Two orgs. One platform. 50,000+ lines of production AI code." | Scale as proof |
| Concept hook | "Isn't it crazy what zeros and ones can do?" | Philosophical, opens a conversation |

**What doesn't work as a hook**:
- "I am an experienced software engineer with X years of..."
- "Passionate about building impactful solutions..."
- "Results-driven professional with a track record of..."

These fail because they could be true of millions of people. A good hook is *specific enough to be false* about everyone else.

**Best hooks for derwells** (ranked by differentiation):

**Option A — Contrast hook** (recommended):
> "Most AI apps sit on top of LLMs. I build the layer that makes them reliable."

Why: Immediately distinguishes. Creates a conceptual frame (infrastructure, not apps) that a stranger can hold in mind. "Reliable" is the key word — points to Temporal.io, session persistence, audit trails. Under 200 characters.

**Option B — Platform thesis hook**:
> "I've deployed the same AI agent infrastructure stack at two production companies. That wasn't accidental."

Why: The repetition signals intentionality. "Two companies" is a social proof anchor. "Not accidental" creates curiosity. The reader wants to know what the stack is.

**Option C — Arc hook**:
> "It started with CUDA kernels and Runge-Kutta solvers. Now I build what makes AI agents reliable in production."

Why: The origin story creates narrative. CUDA + Runge-Kutta signals genuine systems depth (not a bootcamp story). The contrast shows the arc.

**Option D — Specific claim hook**:
> "Built a custom MCP tool registry at protocol level. Deployed durable AI workflows with Temporal.io. In production, at two orgs."

Why: Densely specific. Every phrase is a differentiator. Reads confidently. May feel like a list — could be restructured.

**Recommendation**: Option A or B for the opening line, then use Option C's arc structure as the second sentence. Together they create: immediate distinction + curiosity about origin.

---

## Formula 4: Experience Entry Construction

**What reference profiles do with experience bullets**:

The winning structure from all reference profiles and research:
```
[2-3 sentence narrative: what the role was, what you owned, scope]

• [Action verb] + [specific what] + [result/scale with number]
• [Action verb] + [specific what] + [result/scale with number]
• [Action verb] + [specific what] + [result/scale with number]
• [Named technologies] worked with: [3-5 specific tools]
```

**The STAR formula for bullets**: Action verb → Scope/Context → Result with number

Strong bullet examples from reference scan:
- "Built and deployed a microservices architecture on AWS that scaled to 50,000 users without downtime."
- "Automated CI/CD pipelines with GitHub Actions, cutting release cycles from 2 weeks to 3 days."
- "Launched AI-powered reporting feature used by 60% of customers within 3 months, driving $2M in upsell revenue."

**Applied to derwells' specific bullets**:

For Nuts and Bolts AI (Cheerful):
- "Built durable AI campaign workflows with Temporal.io — pipelines that survive crashes and retry intelligently across 5,570 commits of production code."
- "Engineered AI-personalized creator outreach at scale using Claude Agent SDK — unique emails per creator, not mail-merge."
- "Implemented multi-account Gmail orchestration handling email threading, tracking, and sending across multiple OAuth accounts simultaneously."
- "Built internal Slack AI assistant from scratch: Claude Agent SDK + custom MCP server + Onyx RAG — the team's operational infrastructure."

For PyMC Labs (Decision Orchestrator):
- "Built custom MCP tool registry at protocol level (not FastMCP) — @tool decorator, runtime context injection, scope-based credential gating per channel."
- "Designed dynamic tool assembly system: each incoming request gets a custom-assembled tool set based on workflow context."
- "Implemented three-layer session persistence (Claude context + Langfuse traces + Supabase records) — agents survive crashes with full audit trails."
- "Applied FCIS (Functional Core, Imperative Shell) architecture to a 36,400 LOC Python codebase — deliberate discipline, not coincidence."
- "Integrated 7 platforms: Toggl, Google Workspace, Xero, Bluedot, Onyx RAG, GitHub, Fly.io."

---

## Formula 5: The Impressive vs. Forgettable Test

**The test**: After reading the profile, can I swap this person's name with any other developer and have it still be true?

Forgettable profiles pass the swap test — they're accurate but interchangeable.
Impressive profiles fail it — they describe something specific to exactly this person.

**The swap test applied to derwells**:

Fails (forgettable):
- "Experienced AI engineer with strong fundamentals and production experience."
- "Full-stack developer with expertise in Python, JavaScript, and AI frameworks."
- "Built scalable AI systems for multiple clients."

Passes (impressive — cannot swap):
- "Built a protocol-level MCP tool registry with scope-based credential gating — not a wrapper, the actual protocol implementation."
- "Deployed the same Claude Agent SDK + MCP + Supabase + Langfuse stack across two orgs in different domains — deliberately."
- "Used Temporal.io for durable AI workflows in production influencer marketing campaigns."

**The uniqueness signals in derwells' story** (things that fail the swap test):
1. Protocol-level MCP registry (not a consumer of MCP — the builder)
2. Platform thesis proven across two different domains simultaneously
3. Temporal.io for AI workflow durability (unusual choice for SaaS, signals reliability thinking)
4. Academic arc: CUDA + Runge-Kutta + CV research → AI agent infrastructure (the through-line explains the rigor)
5. FCIS architecture applied to a Discord bot — architectural discipline in a domain (Discord bots) that usually lacks any

---

## Formula 6: Headline Construction for Builders

**The three headline archetypes** from reference scan:

**Type 1: Role + Identity**
`[Primary Role/Company] | [What you built or coined] | [Community/stack signal]`
Example: "Creator of Datasette | Co-creator of Django | Open source developer"

**Type 2: Mission-forward**
`[Movement/concept you're advancing] | [Where you do it] | [Who trusts you]`
Example: "Fostering the Rise of the AI Engineer | Editor of Latent.Space"

**Type 3: Stack + Impact (SEO-optimized)**
`[Role] | [Top 3 technologies] | [Result or niche]`
Example: "Backend Engineer | Python, AWS | Scaling APIs for fast-growing startups"

**For LinkedIn search visibility**: Type 3 has the best keyword density. Types 1 and 2 have better human impression. The right choice depends on whether the goal is discoverability (recruiters searching) or impression (people who click the profile link).

**For derwells**: Given that the current profile is nearly empty and both current roles are invisible, discoverability is less critical than impression. The goal is: if someone sees the profile, they should immediately understand what's impressive.

**Recommended headline formula** (hybrid):
`[Specific what] | [Stack keywords for SEO] | [Social proof anchor: named orgs]`

Draft examples:
- `AI Infrastructure Engineer | Claude Agent SDK · Temporal.io · MCP | Nuts & Bolts AI, PyMC Labs`
- `Building AI Agent Infrastructure | Python · Temporal.io · Claude Agent SDK · MCP | Influencer Automation & Org OS`
- `AI Agent Infra @ Nuts & Bolts AI · PyMC Labs | Temporal.io · MCP (protocol) · Claude SDK · Langfuse`

The named orgs anchor credibility. The stack terms (Temporal.io, MCP, Claude Agent SDK, Langfuse) are differentiated enough to signal "serious" to a technical reader and searchable for recruiters.

---

## Formula 7: Featured Section as "Proof of Work"

**The formula**: Featured = the 3-5 things you'd show someone in the first 5 minutes of a pitch meeting.

For builders, the hierarchy:
1. **Live product or demo** (if accessible) — highest trust, shows it's real
2. **GitHub profile** — especially if pinned repos show relevant work
3. **Personal site or portfolio** — signals professionalism
4. **A post or article you wrote** about something technical — shows thinking, not just doing
5. **Notable open source project** with a compelling README

**Applied to derwells**:
- GitHub link (github.com/derwells) — surfaces the public repos; crowNNs is the best signal there
- Personal site link (if one exists or is created)
- A LinkedIn post about building MCP infrastructure or Temporal.io workflows (would need to write this)
- crowNNs repo directly — benchmarked against SOTA, strongest public technical signal

If there are no existing posts: a Featured link to the GitHub profile + a Featured link to the crowNNs repo readme is a minimum viable Featured section.

---

## Formula 8: Skills Ordering for SEO

**The insight**: LinkedIn weights the first 3-5 skills most heavily for search ranking. Skills are not just labels — they're search index entries.

**Ordering principle**: Lead with the most differentiated + currently strategic skills. Generic skills go later.

**Draft ordering for derwells** (most to least differentiated):
1. Claude Agent SDK
2. Model Context Protocol (MCP)
3. Temporal.io
4. Langfuse
5. AI Agent Architecture
6. Python
7. FastAPI
8. Next.js
9. React
10. Supabase
11. PostgreSQL
12. TypeScript
13. Composio
14. CUDA
15. Computer Vision
16. Machine Learning
17. Distributed Systems
18. Discord.py
19. SQLAlchemy
20. Git / GitHub

The top 5 are the most differentiated — no one searching "Temporal.io" and "MCP" is going to find thousands of results. They're also the real story. Python and React go below because they're table stakes.

---

## Summary: The Formula Applied to derwells

| Formula Element | derwells Version |
|-----------------|-----------------|
| Concept ownership | Protocol-level MCP registry; platform thesis (same stack, two orgs) |
| Depth anchor | AI agent infrastructure (not "AI developer" broadly) |
| Breadth as backstory | CUDA → CV research → AI agent infra — arc explains the rigor |
| Hook | "Most AI apps sit on top of LLMs. I build the layer that makes them reliable." |
| About structure | Hook → Platform thesis (two orgs, same stack) → Origin arc → Specific differentiators → CTA |
| Named things | Temporal.io, Claude Agent SDK, MCP registry, Langfuse, crowNNs, Cheerful, Decision Orchestrator |
| Numbers | 5,570 commits, 36,400 LOC, two production orgs, 7 integrations |
| Headline | Role + Stack keywords + Named orgs |
| Featured | GitHub link, crowNNs repo, a post about MCP/Temporal if written |
| Swap test | Must fail — no other developer can claim the same specific combination |

The single most important insight from this extraction: **derwells' story is not "AI developer" — it's "the person who builds infrastructure that AI agents run on, proven across two different production domains."** That's the frame every section must reinforce.
