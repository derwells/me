# Spec Review — LinkedIn Profile Spec

**Reviewed**: 2026-02-24
**Source**: `analysis/linkedin-profile-spec.md` + all Wave 1–2 analysis files
**Verdict**: **CONVERGED — spec passes. One minor factual flag, no blockers.**

---

## Review Criteria

The spec must pass all six criteria before convergence is declared.

---

## Criterion 1: Does the headline make you want to click the profile?

**Headline under review:**
```
AI Infrastructure Engineer | Claude Agent SDK · Temporal.io · MCP | Nuts & Bolts AI · PyMC Labs
```

**Verdict: PASS**

- "AI Infrastructure Engineer" immediately differentiates from "AI Developer" or "AI/ML Engineer." The word "infrastructure" signals a layer below — deliberate.
- Temporal.io and MCP are niche enough that a technical reader stops: *someone who lists those has actually used them at depth.* No bootcamp teaches these.
- Two named orgs as credibility anchors. Both are findable, real, differentiated (influencer marketing + scientific computing org = the platform thesis in four words).
- 97 chars leaves room for expansion if needed. Nothing truncated on any viewport.
- Swap test: no other developer on LinkedIn has this specific combination. The headline fails the swap test in the right direction.

**Alternate headline** (Option B from identity-synthesis) is held in reserve for when/if content publishing begins. Current choice is optimal for discoverability-first phase.

---

## Criterion 2: Does the about section hook in the first 2 lines?

**Hook under review:**
```
Most AI apps sit on top of LLMs. I build the layer that makes them reliable.
```

**Verdict: PASS**

- 76 characters. Fits on one mobile line. Well inside the ~200 char mobile truncation boundary.
- Contrast hook — creates immediate cognitive distinction. The reader now has a conceptual frame: *this person is not an app developer, they're building something beneath.*
- "Reliable" is the operative word — immediately implies Temporal.io, session persistence, audit trails, crash recovery. The About section then delivers on that implication.
- Second sentence before fold: "I've proven it twice: the same AI agent infrastructure stack, deployed at two production companies in completely different domains."
- What the reader sees before "See More": the hook (distinction claim) + social proof (two production companies). Both must-click signals land before the fold. ✓

**Mobile truncation check:**
> "Most AI apps sit on top of LLMs. I build the layer that makes them reliable.\n\nI've proven it twice: the same AI agent infrastructure stack, deployed at two production companies in..."

Strong enough to earn the click. The "proven it twice" line converts curiosity into interest.

---

## Criterion 3: Do the experience entries show range AND depth?

**Entries under review:** Nuts and Bolts AI, PyMC Labs, Education (+ optional Independent ML Research)

**Verdict: PASS — with one factual verify flag**

**Depth signal (PyMC Labs):**
- "Built custom MCP tool registry at protocol level — not FastMCP, not a wrapper." — This is the deepest signal in the profile. Immediately separates from someone who *used* MCP from someone who *implemented* it.
- "Implemented three-layer session persistence (Claude context windows + Langfuse traces + Supabase records)" — architectural specificity rare in the AI space.
- FCIS applied to a 36,400 LOC Discord bot — architectural discipline where none is expected. The contrast makes it striking.

**Breadth signal (Nuts and Bolts AI):**
- Six bullets covering backend (FastAPI), orchestration (Temporal.io), AI personalization (Claude Agent SDK), email orchestration (Gmail API + OAuth), internal tooling (Slack + MCP + RAG), and frontend (Next.js + React 19 + Zustand + Radix).
- 5,570 commits is a concrete scale signal — not a number that fits a weekend project.

**Education entry:**
- Six bullets — each maps to a named, specific artifact: crowNNs (benchmarked against SOTA), LPRNet (paper reproduction), Floyd-Warshall in CUDA (HPC), Runge-Kutta (numerical methods), concurrent fileserver (C systems), Brainfuck-to-MIPS (compiler theory). This reads as rigorous coursework, not checkbox academics.

**Factual flag — Next.js version:**
The Nuts and Bolts AI description says "Next.js 16+, React 19" in the stack line. Next.js 16 does not exist as of 2026-02-24 (current production version is Next.js 15). This should read either "Next.js 15, React 19" or simply "Next.js, React 19." Derick should verify and correct before pasting.

> **Action required**: Verify actual Next.js version used on Cheerful and update the experience entry stack line before pasting.

This is a minor fix Derick can do inline while copying — it does not block the overall spec.

---

## Criterion 4: Is there personality, or is it generic LinkedIn slop?

**Verdict: PASS — strong personality signal throughout**

Specific personality signals that pass the swap test:

| Generic slop | This profile instead |
|---|---|
| "Experienced AI engineer" | "I build the layer that makes them reliable" |
| "Proficient in Python and ML" | "CUDA GPU kernels, Runge-Kutta orbital simulations, Brainfuck-to-MIPS compiler in Rust" |
| "Built scalable AI systems" | "Protocol-level MCP registry — not FastMCP, not a wrapper. The actual protocol." |
| "Strong fundamentals" | "That didn't happen by accident." |
| "Worked on AI pipelines" | "Pipelines that survive crashes and retry intelligently" |

The profile has convictions: it distinguishes between "FastMCP" and "the actual protocol." It explains *why* things are built a certain way, not just *what* was built. This is the Simon Willison voice the identity-synthesis targeted — named things, verifiable specifics, confident without grandiose.

The "not hustle-porn" criterion from identity-synthesis holds: the About section doesn't mention passion, grind, or love of code. It mentions what was built and why it's architecturally interesting.

---

## Criterion 5: Is anything missing?

**Verdict: Nothing blocking. Two optional enhancements noted.**

**What's covered:**
- ✓ Headline (ready to paste)
- ✓ About / Summary (1,520 chars, hook confirmed, social proof confirmed)
- ✓ Experience entries (Nuts & Bolts AI, PyMC Labs, Education, optional ML Research)
- ✓ Featured section (minimum viable + enhanced path)
- ✓ Skills (30 skills, Tier 1–3, pin guidance)
- ✓ Profile photo and banner recommendations
- ✓ Custom URL recommendation
- ✓ Contact / location
- ✓ Execution checklist (14 items, top-to-bottom)
- ✓ [FILL IN] items clearly labeled

**Optional enhancement 1 — About section length:**
The About section is 1,520 of 2,600 allowed characters (~58% utilized). There's room to expand if desired — for example, adding a sentence about the ralph loop engine or the PyMC Labs origin story (numerical methods background → probabilistic computing org = earned connection, not cold outreach). This is not required — the current draft is complete — but worth noting if Derick wants more texture.

**Optional enhancement 2 — ralph loop engine / meta-system:**
The Phase 6 meta-system work (ralph loop: iterative analysis pipeline with wave-based frontier, convergence detection, CI integration) doesn't appear in the LinkedIn spec. This is a judgment call: surfacing it would reinforce the "one layer deeper" through-line, but it's hard to frame concisely for LinkedIn without sounding obscure. Omitting it is the right choice for the current spec. If Derick writes a LinkedIn post, *that* would be the right venue for the meta-system story.

**Nothing is missing that would block use of the spec.**

---

## Criterion 6: Would a stranger understand the breadth + depth in 30 seconds?

**Verdict: PASS**

The Signal Summary at the bottom of the spec captures exactly this. Testing it:

**In 30 seconds, a stranger reading this profile understands:**

1. *The claim*: Builds the infrastructure layer that makes AI agents reliable — not just "builds AI apps"
2. *The proof*: Two production systems at two named companies; 50,000+ LOC; protocol-level MCP registry; Temporal.io durable workflows
3. *The differentiator*: Same deliberate platform (Claude Agent SDK + custom MCP + Supabase + Langfuse) proven across two completely different domains — this didn't happen by accident
4. *The depth*: The foundation (CUDA, numerical methods, ML research, compiler theory) explains why the production work has architectural discipline that most AI engineers skip
5. *The person*: Based in Philippines; works remotely; has opinions about abstraction levels; explains their work without hustle-porn

All five signals land within the headline + first paragraph of About. The experience entries then prove the claims with specifics.

---

## Final Verdict

**PASS — spec is ready to use.**

The spec contains one factual verify item (Next.js version) that Derick must check before pasting the Nuts and Bolts AI experience description. Everything else is final and copy-paste ready.

**Why this profile works:**

The central insight from all analysis: *derwells has done the unusual thing twice.* Two production systems, same platform, different domains. That's the story. The spec makes it visible in the headline, the hook, the About section, and both experience entries. Every section reinforces the same frame. Nothing contradicts it.

The profile will fail the swap test — no other developer on LinkedIn has this specific combination of Temporal.io, protocol-level MCP, Claude Agent SDK, and PyMC Labs in their background. That's the goal.

---

## Items Derick Must Handle Before Publishing

| Item | Action |
|------|--------|
| Next.js version | Verify actual version used on Cheerful; update stack line in Nuts and Bolts AI entry |
| Employment dates | Fill in start/end dates for both roles |
| Employment type | Full-time or Contract for both roles |
| University name | Search LinkedIn for the exact school page |
| Education dates | Confirm exact start/end years |
| Profile photo | Upload if not current |
| Custom URL | Check availability of `derwells` before committing |

These are information only Derick has — no further loop analysis can resolve them.
