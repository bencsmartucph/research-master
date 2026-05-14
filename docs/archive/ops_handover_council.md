# Ops Handover: Council Skills + Agent Pruning

> **For the Claude session or collaborator picking this up.** Read this document end to end before touching anything. The work is bounded; the codebase has more to it than this brief covers, and most of it is out of scope. The user (Ben) has explicitly deferred everything not listed in the *Phases* section.

---

## TL;DR

Build two new slash-command skills (`/council-critique` and `/council-ideate`) that orchestrate Ben's existing subagents in parallel and produce a synthesised report. Then prune the agents directory by archiving everything that doesn't serve the council pattern or core research workflow. Test both skills on a real artefact before declaring done.

**Time budget:** 90–120 minutes total. Don't exceed without checking back with Ben.

**Scope discipline:** Three things are explicitly *out of scope* for this handover (Continuous Improvement Pipeline, voice-ben refactor, modifications to existing infrastructure beyond the agents directory). See *Out of Scope* below.

---

## Who Ben is, and what Research_Master is

Ben Smart — MSc Economics (University of Copenhagen, completing 2026), starting a PhD in political economy / comparative politics. Research focus: how economic disruption (automation, trade, austerity) shapes populist political behaviour, and what welfare design can do about it. He just finished a methods seminar on his asymmetric-welfare paper and is about to enter thesis design phase.

Research_Master is his working repository at `C:\Users\PKF715\Documents\claude_repos\Research_Master`. Top-level structure relevant to this handover:

```
.claude/
  agents/         ← 25+ agent definitions, mostly unused (this handover's focus)
  skills/         ← 17 active skills (do not touch except as specified)
  rules/          ← path-scoped rules (read but don't modify)
docs/
  empirical_walkthrough_v1.md            ← his paper-defence document
  learning_econometrics/                 ← in-progress foundations resource
manuscripts/
  paper_draft_v4_final.md                ← his current paper
CLAUDE.md
MEMORY.md
```

Ben's stated needs that this handover addresses:

- A council of named expert critics for paper review, identification-strategy review, and methodology rigour
- Ideation support — pressure-testing ideas before they harden into commitments
- Protection against myopia (over-focus on one framing or method)
- Reducing the cognitive overhead of an agents directory he doesn't trust because he's never used most of it

Ben's stated *non*-needs (do not build for these):

- Email/inbox triage
- Meeting capture
- Calendar integration
- Grant proposals
- Tax workflows
- Boxing (irrelevant; he just mentioned this as a thing he doesn't care about)

---

## Phase 1 — Agent pruning (≈20 min)

**Goal:** reduce `.claude/agents/` from 25+ entries to roughly 8–10 actively useful ones, by archiving the rest into `.claude/agents/_archive/`. Do not delete; archive is recoverable.

**Procedure:**

1. Create directory `.claude/agents/_archive/` if it doesn't exist.
2. For each agent listed in the *Archive set* below, move it (do not copy + delete; use `git mv` if you want git history preserved, otherwise plain `mv`).
3. Leave everything in the *Keep set* in place.
4. After moving, verify the count: `ls .claude/agents/*.md | wc -l` should return roughly 8–10 (depends on edge cases below).

**Keep set** — these map directly to council-critique, council-ideate, or core research workflow:

| Agent | Role |
|---|---|
| `econometrician.md` | Causal-inference critic (council member: Skeptic) |
| `methods-referee.md` | Methods rigour critic (council member: Methodologist) |
| `domain-referee.md` | Substantive critic (council member: External-validity hawk) |
| `strategist-critic.md` | Identification critic (council member: Pre-mortem) |
| `editor.md` | Synthesis (council synthesiser) |
| `writer.md` | Paper drafting (worker, not council) |
| `writer-critic.md` | Paper polish (paired with writer) |
| `librarian.md` | Literature ingestion (worker) |
| `librarian-critic.md` | Literature quality (paired with librarian) |
| `general-purpose.md` | Utility (used by skills for ad-hoc tasks) |
| `explorer.md` | Data and idea discovery (used in council-ideate) |

**Archive set** — move these to `.claude/agents/_archive/`:

```
beamer-translator.md          # specialised: Beamer→Quarto, niche
code-simplifier.md            # marginal; writer-critic covers most
coder.md                      # rare-use; reactivate if data work resumes
coder-critic.md               # paired with coder; archive together
data-engineer.md              # overlaps with coder
debugger.md                   # overlaps with coder-critic
discussant.md                 # duplicates storyteller-critic
domain-reviewer.md            # duplicates domain-referee
explorer-critic.md            # archive (explorer kept; critic rarely used)
methodology Reviewer.md       # template-only, never instantiated
orchestrator.md               # meta-infra; out of scope here
pedagogy-reviewer.md          # not Ben's workflow
proofreader.md                # overlaps with writer-critic
quarto-critic.md              # only matters during deck-building
quarto-fixer.md               # only matters during deck-building
r-reviewer.md                 # overlaps with coder-critic
referee.md                    # generic; methods-referee + domain-referee replace it
replication-auditor.md        # only matters at submission
slide-auditor.md              # only matters during deck-building
statusline-setup.md           # utility, archive
storyteller.md                # only matters during talk prep
storyteller-critic.md         # only matters during talk prep
strategist.md                 # rare-use worker; strategist-critic kept
surveyor.md                   # duplicates explorer-critic
tikz-reviewer.md              # irrelevant for non-deck work
verifier.md                   # matters at submission only
Writing Reviewer.md           # template-only, never instantiated
```

**Edge cases requiring judgement:**

- If an agent is referenced in `CLAUDE.md`, `.claude/rules/`, or any active skill, *do not archive without first updating the reference*. Search before archiving: `grep -r "\bAGENT_NAME\b" .claude/ docs/ CLAUDE.md MEMORY.md`.
- If `git mv` reports the file is gitignored or otherwise tracked oddly, fall back to plain `mv` and check that the move is detected by `git status`.

**Output:** a clean `.claude/agents/` directory with 11 files (or close to it), and a `.claude/agents/_archive/` directory containing the rest.

---

## Phase 2 — Council design document (≈20 min)

**Goal:** produce `docs/council_design.md` that documents the council pattern Ben wants, the persona-to-agent mappings, and the invocation conventions. The two skills in Phases 3 and 4 reference this document.

**File:** `docs/council_design.md`

**Required sections:**

1. **Purpose** — one paragraph: what the council pattern is for, when to use it.
2. **Two variants:**
   - `/council-critique` — for *evaluating* work in progress (papers, identification memos, draft chapters, slide decks). Five named personas operating in parallel, then a synthesis.
   - `/council-ideate` — for *generating* and pressure-testing ideas. Four personas with different generative remits.
3. **Persona-to-agent mapping for council-critique:**

   | Persona | Agent it dispatches to | Framing prompt for the agent |
   |---|---|---|
   | The Skeptic | `econometrician` | "Assume the central result is wrong. What's the most plausible reason?" |
   | The Methodologist | `methods-referee` | "What specification or robustness check would a methods referee at the target journal demand?" |
   | The Pre-mortem | `strategist-critic` | "The paper got rejected. In two sentences, what does the rejection letter say about the identification strategy?" |
   | The External-Validity Hawk | `domain-referee` | "Where does this not generalise? Whose context is missing from the sample / theory / framing?" |
   | The Contribution Auditor | `editor` | "Strip the literature review back to nothing. What's the *new* claim that earns this paper its space?" |

4. **Persona-to-agent mapping for council-ideate:**

   | Persona | Agent or invocation | Framing prompt |
   |---|---|---|
   | The Obvious Extension | `general-purpose` (subagent) | "What's the boring, predictable next move from this work that any supervisor would suggest? Be specific." |
   | The Adjacent Outsider | `general-purpose` (subagent) | "What's the contrarian move from a discipline next door — sociology, behavioural economics, social psychology — that the author would otherwise miss?" |
   | The Constraint Inverter | `general-purpose` (subagent) | "What's the version of this idea that's only possible if the usual constraint (cross-sectional data, small N, single dataset) is dropped?" |
   | The Synthesis | runs after the three above | "Given these three angles, what's the research programme over five years that they jointly suggest?" |

5. **Synthesis protocol** — how the editor agent (or main session) consumes parallel critiques and produces:
   - **Convergent critiques** (every persona flagged the same issue → high-confidence problem)
   - **Divergent critiques** (only one persona flagged → judgement call territory)
   - **Missing dimensions** (what nobody flagged that should have been flagged)
   - **Top three actions** (ranked recommendations the user can choose to adopt)

6. **Invocation examples:**
   ```
   /council-critique manuscripts/paper_draft_v4_final.md
   /council-critique projects/seminar_paper/identification_memo.md
   /council-ideate "extend the asymmetric-welfare framework to non-Western European contexts"
   /council-ideate docs/learning_econometrics/01_counterfactual_question.md
   ```

7. **What council is *not*:** explicit non-uses to prevent scope creep. *Not* a substitute for human supervisor review. *Not* used for code review (Ben's existing coder-critic handles that). *Not* a brainstorm-with-self tool — it's structured adversarial review.

The document should be 600–1,000 words. Don't pad. Use the table format above.

---

## Phase 3 — Build `/council-critique` skill (≈30 min)

**File:** `.claude/skills/council-critique/SKILL.md`

**Frontmatter:**
```yaml
---
name: council-critique
description: Run a five-persona adversarial council review on a paper, memo, or draft, dispatching to specialised research-critic agents in parallel and producing a synthesised report. Use when the user asks for council review, structured critique, or pre-submission review of a research artefact.
---
```

**Skill body should:**

1. Read the artefact path from the user invocation.
2. If the artefact is large (>500 lines or PDF/docx), summarise it briefly first so each persona's prompt isn't bloated. Use the `general-purpose` agent for the summary.
3. Dispatch five subagent calls in parallel (single message with multiple Agent tool calls — this is critical for speed):
   - `econometrician` with the Skeptic framing
   - `methods-referee` with the Methodologist framing
   - `strategist-critic` with the Pre-mortem framing
   - `domain-referee` with the External-Validity Hawk framing
   - `editor` with the Contribution Auditor framing
4. Each persona prompt should include: (a) the artefact summary, (b) the persona-specific framing from `docs/council_design.md`, (c) the explicit instruction to return a structured report with `## Top issues`, `## Specific suggestions`, `## What you don't know`, `## Confidence` sections.
5. After all five agents return, run a synthesis pass that produces the four-section output (convergent, divergent, missing, top-three-actions) defined in the design doc.
6. Save the full council report to `quality_reports/council_critiques/YYYY-MM-DD_<artefact-stem>.md`.
7. Print a compact summary to the user: top three actions + a pointer to the saved full report.

**Important implementation notes:**

- Use the `Task` tool for subagent dispatch (not `Bash` or `WebFetch`).
- Dispatch all five subagents in *one* message with multiple tool calls — running them sequentially would multiply the response time by five.
- The synthesis pass can be done in the main session (no need to spawn another subagent).
- If any subagent fails, continue with the others and note the failure in the synthesis. Don't block on individual failures.

**Exit conditions:**

- The skill always saves a full report file, even if synthesis is partial.
- The skill always prints something to the user — never silently exits.

---

## Phase 4 — Build `/council-ideate` skill (≈30 min)

**File:** `.claude/skills/council-ideate/SKILL.md`

**Frontmatter:**
```yaml
---
name: council-ideate
description: Run a four-persona generative council that produces creative angles on a research idea or artefact, then synthesises them into a five-year research programme suggestion. Use when the user wants ideation help, idea pressure-testing, or protection from myopia on a research direction.
---
```

**Skill body should:**

1. Read the input — either a path to a doc or a literal topic string.
2. If a doc, summarise it; if a topic string, expand it slightly into a 2–3 sentence framing.
3. Dispatch three subagent calls in parallel:
   - `general-purpose` with the Obvious Extension framing
   - `general-purpose` with the Adjacent Outsider framing
   - `general-purpose` with the Constraint Inverter framing
4. Each persona returns a structured report: `## Three concrete angles`, `## What you'd need to do this`, `## Closest existing literature`, `## Why someone smart would dismiss this`.
5. After the three return, run a synthesis pass producing: `## The convergent thread`, `## The boldest single move`, `## A five-year research programme combining these`, `## Three things to check before committing`.
6. Save full report to `quality_reports/council_ideations/YYYY-MM-DD_<topic-slug>.md`.
7. Print compact summary.

**Critical difference from council-critique:**

- The personas in council-ideate are *generative* not *critical*. The framing prompts should produce specific, concrete suggestions — not lists of caveats. Each persona should aim to produce three actionable ideas, not three reasons to be cautious.
- The synthesis layer is what introduces critical filtering. The personas themselves are unleashed.

---

## Phase 5 — Test on a real artefact (≈20 min)

**Goal:** verify both skills work end-to-end before declaring done.

**Tests:**

1. `/council-critique docs/empirical_walkthrough_v1.md` — should produce a synthesised report covering the methodology hierarchy, BLUPs choice, asymmetric-confirmation framing, and limitations. Verify the report saves to `quality_reports/council_critiques/`.
2. `/council-ideate "extend the asymmetric-welfare mechanism to within-country variation using Danish registry data"` — should produce three creative angles plus a five-year programme synthesis. Verify the report saves to `quality_reports/council_ideations/`.

**Success criteria for each test:**

- Skill runs to completion without error.
- All subagents return content (not just empty `<result>` tags).
- The synthesis is non-trivial — i.e., it does more than concatenate the persona reports; it identifies convergent issues, divergent issues, and missing dimensions for council-critique, or a programmatic synthesis for council-ideate.
- The saved report file is human-readable.
- The compact summary printed to the user is actionable in under 60 seconds of reading.

If either test fails, debug and re-run. Do not declare done with a failing test.

---

## Acceptance criteria for the whole handover

The handover is complete when *all* of the following are true:

- [ ] `.claude/agents/_archive/` exists and contains the agents from the *Archive set*
- [ ] `.claude/agents/` contains roughly 11 active agents (the *Keep set*)
- [ ] No active skill or rule references an archived agent (search-and-fix any reference)
- [ ] `docs/council_design.md` exists and documents both council variants per spec
- [ ] `.claude/skills/council-critique/SKILL.md` exists with correct frontmatter and dispatch logic
- [ ] `.claude/skills/council-ideate/SKILL.md` exists with correct frontmatter and dispatch logic
- [ ] A test run of `/council-critique docs/empirical_walkthrough_v1.md` produces a saved report
- [ ] A test run of `/council-ideate "<test prompt>"` produces a saved report
- [ ] A short note appended to `MEMORY.md` documenting the new skills and their use cases (≤5 lines)

---

## Out of scope (do *not* do these)

These have been explicitly deferred by Ben. Do not start them as part of this handover.

1. **Continuous Improvement Pipeline.** Multi-stage pipeline that filters daily tips through escalating critic review. Deferred 1–2 weeks until council habits form.
2. **Voice-ben refactor.** Restructuring the existing `voice-ben` skill into a YAML with explicit vocabulary bans, sentence rules, and required transitions. Deferred to a separate session.
3. **Modifying CLAUDE.md or MEMORY.md beyond the single 5-line note in acceptance criteria.** Both files contain calibrated user instructions; adding to them is fine, restructuring is out of scope.
4. **Modifying any existing skill in `.claude/skills/`.** Note the existing `/council` skill — Ben previously had a generic "Parallel Critics + Separate Synthesis" skill at this path. *Inspect it first.* If it's roughly equivalent to what `/council-critique` will be, *deprecate it cleanly* (move to `.claude/skills/_archive/`) and proceed. If it has unique features the new skills should preserve, fold them into the new design before archiving. Either way, do not silently overwrite.
5. **Modifying `.claude/rules/`.** Path-scoped rules are out of scope.
6. **Building any new subagents.** The four council-critique personas map to existing agents; the council-ideate personas use `general-purpose`. No new agent files needed.
7. **Touching the talk artefacts in `talks/2026-05-04_seminar/`.** That work was completed in a prior session; leave it alone.
8. **Anything related to the empirical walkthrough or learning_econometrics resource.** Both are useful as test artefacts for council-critique but are not subjects of modification here.

---

## Files to read first (in this order)

1. `CLAUDE.md` — Ben's project-level rules (≤100 lines)
2. `.claude/rules/agents.md` — agent dispatch conventions
3. `.claude/rules/quality.md` — scoring and severity calibration (referenced by council synthesis)
4. The five Keep-set agent files used by council-critique: `econometrician.md`, `methods-referee.md`, `strategist-critic.md`, `domain-referee.md`, `editor.md`
5. The existing `.claude/skills/council/SKILL.md` if present — for the deprecation decision in *Out of Scope* point 4
6. `~/.claude/CLAUDE.md` — Ben's global instructions (especially the "Calibrating criticism" mode-1-to-4 framework, which the council should respect)

Do not read the entire `docs/` tree, the manuscripts, or the analysis pipelines. They are out of scope for this handover.

---

## Notes and gotchas

- **Parallel dispatch is critical.** Both skills depend on parallel subagent calls for performance. If you run agents sequentially, the skill becomes too slow to use and Ben will abandon it. Use one tool-use message with five (or three) `Task` invocations.
- **The `editor` agent serves dual roles** in council-critique: it's both the Contribution Auditor persona AND, conceptually, the synthesis voice. The skill body handles synthesis directly in the main session — don't dispatch a sixth call to `editor` for synthesis on top of its persona role.
- **Ben's voice-ben skill exists** but is *not* in scope here. Don't auto-trigger it for the council reports — those are internal artefacts, not prose he'll publish under his name.
- **Quality reports go to** `quality_reports/council_critiques/` and `quality_reports/council_ideations/`. These directories may not exist; create them if needed.
- **Ben's calibration preference:** when synthesising, default to *Mode 2* on the criticism scale defined in his global `CLAUDE.md` ("priority — the 3–5 most impactful issues"). Don't produce 20-issue laundry lists.
- **Time-boxing:** if you exceed 120 minutes total, stop and check back with Ben rather than pushing through. Likely cause of overrun is over-engineering the synthesis pass; simpler is better.

---

## Final handoff message to Ben

When the handover is complete, post to Ben (do not modify any user-facing file with this message; just print it):

```
Council infrastructure deployed. Summary:

- Agent directory: pruned from N to 11 active; archive at .claude/agents/_archive/
- Council design: docs/council_design.md
- New skills: /council-critique, /council-ideate
- Test runs: passed (reports at quality_reports/council_critiques/ and quality_reports/council_ideations/)

Try first:
  /council-critique docs/empirical_walkthrough_v1.md

Out of scope, deferred per your brief: continuous improvement pipeline, voice-ben refactor.
```

That's the handover. Stay bounded. Ask Ben before expanding scope.
