# Ops Handover Phase 2: Session Memory + Voice Artefacts

> **For the Claude session or collaborator picking this up.** Read end to end before touching anything. Phase 1 (council skills + agent pruning) lives in `docs/ops_handover_council.md` and is a *prerequisite reference* for some context here, but the work is otherwise separable. If Phase 1 has not been executed, do that first or read its conventions before starting Phase 2.

---

## TL;DR

Three skills, in dependency order:

1. **Extend `/done`** so session-end captures auto-update `STATUS.md`, append to the research journal, and tag the session for later retrieval. (~30–45 min)
2. **Build `/recall`** as a semantic-style search across saved session logs and project STATUS files. MVP version uses LLM dispatch over the log corpus, not a real vector index. (~60–90 min)
3. **Refactor `voice-ben` into a structured artefact** with explicit ban lists, required transitions, sentence rules, and anti-pattern examples. Then build `/voice-audit` that runs the artefact as a deterministic check on prose. (~60–90 min)

**Time budget:** 2.5–3.5 hours total. The phases are independent enough that you can stop after any of them and hand back to Ben without leaving a half-finished system.

**Scope discipline:** four explicit out-of-scope items below. Most importantly: do *not* build a real vector-database `/recall` in this handover. The MVP is sufficient and ships in a fraction of the time.

---

## Why these three together

They share a theme: long-horizon infrastructure for a multi-year PhD. Each pays its rent slowly — none of them produce a dramatic win on day one, but together they compound across the next four to six years of Ben's research life.

- `/done` makes session memory durable so the next session inherits context cleanly
- `/recall` makes that memory queryable so insights from session 47 are still available in session 412
- Voice artefacts make Ben's authorial voice stable across collaborators, AI model upgrades, and the natural drift that happens when you write under deadline pressure

If Ben does only one of the three, do `/done` — it's the foundation the others depend on (recall searches the logs `/done` produces; voice-audit will reference the same session logs to confirm voice consistency).

---

## Project context (compact)

Repository: `C:\Users\PKF715\Documents\claude_repos\Research_Master`. Ben Smart, MSc Economics → starting PhD political economy. He runs Claude Code with ~17 active skills and (post-Phase-1) ~11 active agents.

Existing infrastructure relevant to this handover:

```
.claude/
  skills/
    done/SKILL.md          ← existing, will be EXTENDED not replaced
    voice-ben/SKILL.md     ← existing, will be REFACTORED
  rules/
    logging.md             ← documents session_log + research_journal conventions
    workflow.md            ← references session log triggers
quality_reports/
  session_logs/            ← daily session captures (per logging.md)
  research_journal.md      ← append-only agent activity log
  plans/                   ← saved plans
SESSION_REPORT.md          ← consolidated operations log
projects/
  seminar_paper/STATUS.md  ← active-project state (manually maintained)
  msc_thesis/STATUS.md     ← thesis state
manuscripts/               ← paper drafts (writer signs here)
docs/empirical_walkthrough_v1.md  ← test artefact for voice-audit
```

Ben's stated motivation for this phase (verbatim, distilled):

- "Almost too many things to keep track of across sessions"
- "Want voice/vocabulary stuff to be deterministic, not vibes"
- "Don't write grants — focus is paper writing and thesis design"

---

## Phase 1 — Extend `/done` (≈30–45 min)

**Goal:** ensure every session-end produces durable artefacts that downstream skills (and Ben himself) can rely on.

### Procedure

1. **Inspect the existing skill.** Read `.claude/skills/done/SKILL.md` first. Note: do *not* replace it; extend it. The existing skill is the foundation; we add capture comprehensiveness on top.
2. **Read `.claude/rules/logging.md`** — it defines the three-tier logging pattern (session_log → SESSION_REPORT.md → research_journal.md). The extended `/done` should respect all three.

### What the extended `/done` should do

When invoked, the skill should:

1. **Identify the active project**, by checking which `projects/<name>/STATUS.md` was most recently modified, or by asking the user if ambiguous.
2. **Generate a session summary** with these required sections:
   - **What was done** — bulleted list of concrete actions (files created, decisions made, scripts run)
   - **Decisions and rationale** — for each non-trivial choice, what was decided and why (1–2 sentences)
   - **Blockers / open questions** — anything unresolved, with the specific question framed
   - **Next session pointer** — what the next session should pick up first
   - **Topics** — comma-separated tags from a controlled vocabulary (econometrics, identification, multilevel-models, voice, infrastructure, paper-draft, thesis-design, lit-review, defence-prep, etc.)
3. **Append the summary** to:
   - `quality_reports/session_logs/YYYY-MM-DD_<short-description>.md` (new file per session)
   - `SESSION_REPORT.md` (the consolidated log; append, never overwrite)
   - `quality_reports/research_journal.md` (one-line summary if any agents were dispatched)
4. **Update the active `STATUS.md`** by appending a `## YYYY-MM-DD session` block with the summary's first three sections (skip Topics there).
5. **Print to user** a 5-line confirmation: which files were updated, location of the session log, and the top 1-2 next-session pointers.

### Critical implementation notes

- **Topics must be from a controlled vocabulary.** Add a list at the top of the skill body. New topics require Ben's nod (the skill should ask before introducing one). This is what makes `/recall` queryable — uncontrolled tags become noise within months.
- **The `STATUS.md` append should not bloat indefinitely.** If a STATUS.md exceeds 600 lines, the skill prompts the user to roll over older entries to an `_archive/` subfolder. Keep STATUS.md scannable.
- **Don't auto-trigger writer/voice-ben on session summary text.** The session log is internal infrastructure, not external prose. Voice-audit should not flag session logs.

### Acceptance criteria for Phase 1

- [ ] `.claude/skills/done/SKILL.md` reflects the extended behaviour
- [ ] A test invocation of `/done` produces all four file updates (session log, SESSION_REPORT, research journal, STATUS) in the expected locations
- [ ] The controlled-vocabulary topic list is visible in the skill body
- [ ] No existing skill behaviour is broken (regression: ensure Ben's old `/done` triggers still work)

---

## Phase 2 — Build `/recall` MVP (≈60–90 min)

**Goal:** a queryable archive of past sessions that surfaces the right session log when Ben can't remember when he made a decision or what he concluded about a topic.

### Architecture decision: MVP, not full vector search

A real semantic-search system requires embeddings, a vector store (Chroma, Qdrant, sqlite-vec, etc.), an indexing pipeline, and refresh logic. That is a 2-day engineering project, not a 90-minute one, and is **out of scope here**.

The MVP works differently. It treats the corpus of session logs and STATUS files as a moderately-sized text body (say, <500 KB until late in the PhD) and dispatches a query to the main LLM session with the relevant excerpts in context. No embeddings, no vector index, no refresh logic. Performance is fine for the first 1–2 years; if Ben's corpus eventually exceeds what fits in a context window, *then* upgrade to a real vector store.

### What `/recall` should do

When invoked with a query (e.g., `/recall when did I decide to use BLUPs over bivariate slopes`):

1. **Build the corpus** by reading:
   - `quality_reports/session_logs/*.md` (date-ordered)
   - `SESSION_REPORT.md`
   - `quality_reports/research_journal.md`
   - All `projects/*/STATUS.md` files
2. **Pre-filter** by topic if the query mentions a controlled-vocabulary topic. (Reduces context load.)
3. **Run a search-and-summarise pass** over the filtered corpus:
   - Find the 3–5 most relevant session entries
   - For each, extract the decision/discussion that relates to the query
   - Cite the file path and date
4. **Return a structured response:**
   - **Direct answer** if the corpus contains one
   - **Top 3 relevant sessions** with file paths and 1-line summaries
   - **Confidence note** — was this answered in the corpus or inferred?
   - **Suggested next read** — the single most relevant file path

### Implementation notes

- **Use `Read` and `Grep` directly.** No subagent dispatch for the MVP — Ben dislikes agent overhead and the search is fast enough without it.
- **Cap corpus reads at ~50 files.** If `quality_reports/session_logs/` grows beyond 50 entries before the MVP is replaced, add date-range filtering to the skill.
- **Print every file path the skill consulted** at the end, so Ben can audit the search.
- **Be conservative on direct answers.** If the corpus doesn't clearly answer the query, say so explicitly. The skill is an archive search, not a memory simulation.

### Acceptance criteria for Phase 2

- [ ] `.claude/skills/recall/SKILL.md` exists with correct frontmatter
- [ ] Test query: `/recall when did I decide to use BLUPs methodology` returns a useful answer pointing at the relevant session log (ensure at least one session log already mentions this — create a test entry if needed)
- [ ] The skill response cites file paths every time, never floats a claim without a source
- [ ] The skill explicitly handles "not found in corpus" without fabricating

---

## Phase 3 — Voice file as structured artefact + `/voice-audit` (≈60–90 min)

**Goal:** transform `voice-ben` from a vibes-calibrated style guide into a deterministic, structured artefact, and add `/voice-audit` to enforce it on prose Ben will publish.

### Inspect first

Read `.claude/skills/voice-ben/SKILL.md` end to end. Also read:

- `~/.claude/CLAUDE.md` — Ben's global writing preferences, including the em-dash prohibition
- `manuscripts/Writing Samples/` if it exists — the pre-AI writing samples used for voice calibration
- `docs/empirical_walkthrough_v1.md` — *not* in voice-ben's scope (it's TO Ben not FROM Ben), but useful as a counter-example for what voice-ben should ignore

### What the refactored voice artefact should contain

Restructure into `voice-ben.md` (or similar) with a YAML frontmatter spec and a markdown body. The frontmatter is the deterministic part; the body is human-readable rationale.

**Required frontmatter sections:**

```yaml
---
banned_vocabulary:
  - delve
  - leverage         # except in technical sense (regression leverage)
  - underscore
  - comprehensive
  - multifaceted
  - holistic
  - robust           # except in methodological sense (inference-resistant)
  # ... extend from existing voice-ben + Ben's CLAUDE.md
banned_punctuation:
  - em-dash          # never (use semicolons or periods)
  - oxford-comma     # if Ben prefers; check voice samples first
required_transitions:
  - Indeed
  - Furthermore
  - Through this perspective
  - Effectively
  - undergirding
  - as purported by
  - Drawing on
  - Firstly / Secondly / Thirdly
sentence_rules:
  - max_parentheticals_per_sentence: 1
  - prefer_semicolon_over_em_dash: true
  - claim_before_example: true
  - no_throat_clearing_openers: true   # no "It is interesting to note that..."
structural_rules:
  - first_sentence_states_the_claim: true
  - no_buried_thesis_in_paragraph: true
voice_calibration_sources:
  - manuscripts/Writing Samples/Global_Media_2017.docx
  - manuscripts/Writing Samples/Politicians_and_Twitter_2017.docx
  - manuscripts/Writing Samples/Newspaper_Representations_2018.docx
detection_resistance:
  - target: GPT-Zero
  - acceptable_human_score: 60+
  - notes: "AI-edited AI prose ceiling is ~60% human; for higher, Ben must retype anchor paragraphs."
---
```

**Required body sections:**

1. **Voice calibration overview** (1 paragraph) — what voice-ben is and is not
2. **Pre-AI sample summary** (1 paragraph) — what the writing samples reveal about Ben's voice
3. **Anti-pattern catalogue** (3–5 examples) — concrete bad-prose example with concrete rewrite, one per top failure mode
4. **Skill-scope clarification** — voice-ben applies to prose Ben SIGNS (papers, essays, abstracts, blog posts, statements of purpose). It does NOT apply to internal docs, plans, code comments, tutor-style documents (see `~/.claude/projects/.../memory/feedback_voice_skills_scope.md` for the existing scope decision).

### Build `/voice-audit` skill

Once the voice artefact is structured, the audit skill is mechanical:

**File:** `.claude/skills/voice-audit/SKILL.md`

**What it does, given a path to prose:**

1. Loads the voice-ben spec (frontmatter only — body is human reference, not machine input)
2. For each banned vocabulary item, scans the prose with `Grep -n -i` and lists every occurrence
3. For each banned punctuation rule, scans similarly
4. Counts required-transition usage and flags if zero (low-likelihood-this-is-Ben score)
5. Tests sentence-level rules where possible (e.g., max parentheticals per sentence — count `\([^)]*\)` per sentence)
6. Outputs a structured report:
   - **Hard violations** (banned vocabulary or punctuation found)
   - **Soft signals** (no required transitions used; suspicious sentence patterns)
   - **Suggested rewrites** for each hard violation (the skill can use the body's anti-pattern catalogue as templates)
   - **Voice-confidence score** — coarse 0–100 where 100 is "consistent with Ben's voice across all checks", 0 is "almost certainly not Ben"

### Critical implementation notes

- **Voice-audit is a CHECK, not a REWRITE.** It produces flags and suggestions; Ben decides what to change. The skill must never auto-edit prose.
- **The frontmatter is canonical.** When Ben updates a banned word, he updates the YAML, not prose-narrating "I should also avoid X" in the body. Body is rationale; YAML is enforcement.
- **Don't trigger voice-audit automatically.** It runs on demand, on artefacts Ben names. Never on tutor docs, internal memos, or code.
- **Preserve the existing voice-ben skill's writing-samples calibration.** The samples are the source of truth for the rules; don't lose the connection.

### Acceptance criteria for Phase 3

- [ ] `voice-ben` skill body restructured around the YAML frontmatter spec above
- [ ] All bans and rules in the YAML are derived from existing CLAUDE.md guidance + the writing samples (no fabricated rules)
- [ ] `.claude/skills/voice-audit/SKILL.md` exists and runs against a test artefact
- [ ] Test run on `manuscripts/paper_draft_v4_final.md` produces a structured report with hard-violation count, soft-signal count, and confidence score
- [ ] No auto-rewrite behaviour exists in voice-audit

---

## Acceptance criteria — whole handover

- [ ] Phase 1: extended `/done` produces all four expected artefacts on a test run
- [ ] Phase 2: `/recall` MVP returns useful results citing real file paths
- [ ] Phase 3: voice artefact restructured + `/voice-audit` works on a test artefact
- [ ] No agent files modified (this handover is skill-only)
- [ ] No existing skill broken (regression check)
- [ ] Short note appended to `MEMORY.md` (≤8 lines) documenting the three new/refactored skills
- [ ] Final handoff message printed (template at end of this doc)

---

## Out of scope (do *not* do these)

1. **Real vector-database `/recall`.** Ship the MVP. A vector-search upgrade is a separate handover when the corpus exceeds what fits in context (likely 12–18 months out).
2. **Auto-triggering voice-audit.** Manual-invocation only. Auto-triggering would create noise on every internal doc and tutor file. Ben dislikes pattern bloat.
3. **Continuous Improvement Pipeline.** Still deferred per Ben's earlier brief; not part of this handover. Schedule for a Phase 3 handover once council and these skills have been in use for 2–3 weeks.
4. **Adding new agents.** This handover is purely skill-side. The agent directory was settled in `ops_handover_council.md`.
5. **Modifying CLAUDE.md or rules/.** Adding ≤8 lines to MEMORY.md per acceptance criteria is the only allowed user-instruction modification.
6. **Touching `talks/`, `manuscripts/`, `analysis/`, or `docs/learning_econometrics/`.** These are subjects of test runs only; no modifications.
7. **Migrating Ben's existing session logs to a new format.** Backwards compatibility matters more than format perfection. New `/done` writes the new format; old logs stay as they are.

---

## Files to read first (in this order)

1. `docs/ops_handover_council.md` — for conventions and shared context (skim only)
2. `~/.claude/CLAUDE.md` — Ben's global preferences (full read)
3. `CLAUDE.md` — project-level instructions (full read)
4. `.claude/rules/logging.md` — existing logging conventions (full read)
5. `.claude/skills/done/SKILL.md` — existing `/done` skill (full read; extending not replacing)
6. `.claude/skills/voice-ben/SKILL.md` — existing voice skill (full read; refactoring)
7. `manuscripts/Writing Samples/` directory contents (skim — these are the voice-calibration source)

Do **not** read `manuscripts/paper_draft_v4_final.md` end-to-end. It's a test artefact for voice-audit; the audit doesn't need to comprehend the substance, only check the prose.

---

## Notes and gotchas

- **The dependency order matters.** `/done` must produce useful logs before `/recall` is testable. If you build `/recall` first, the test corpus will be too sparse to evaluate the skill, and you'll incorrectly conclude it works fine when it actually fails on real data later. Build in order: `/done` → `/recall` → voice work.
- **Topics list discipline.** A controlled vocabulary fails if it grows uncontrolled. The `/done` skill should *resist* new topics — when the user proposes one, ask whether an existing topic covers it. Only add genuinely new topics. Without this, `/recall` becomes useless within 6 months.
- **Voice-audit produces flags, not edits.** Hard rule. The moment voice-audit auto-rewrites, it becomes a different skill (a stylistic enforcer rather than a checker), and Ben loses control. Resist any temptation to add an auto-fix mode.
- **Test artefact suggestions.** For `/done`, run on the most recent real session you can reconstruct. For `/recall`, query something Ben definitely decided in a recent session (e.g., "BLUPs methodology", "council skill design"). For voice-audit, run on `manuscripts/paper_draft_v4_final.md` (real Ben prose) AND on `docs/empirical_walkthrough_v1.md` (NOT Ben prose — should produce a meaningfully different audit result; if it produces the same result, the audit isn't discriminating).
- **Backwards compatibility on voice-ben.** Ben's existing voice-ben skill references writing samples by path. If you move or rename anything in `manuscripts/Writing Samples/`, update the references. Better: don't move anything.
- **Don't index session logs that contain personal information by default.** If any session log includes things like personal email exchanges, financial details, or third-party private info, the `/recall` skill should respect a `_private` subfolder convention: any session log under `quality_reports/session_logs/_private/` is excluded from `/recall` by default. Note this in the skill body.

---

## Final handoff message to Ben

When the handover is complete, print this to Ben (do not modify any user-facing file):

```
Phase 2 deployed.

- /done extended: now updates STATUS.md, SESSION_REPORT.md, research_journal.md, and writes a controlled-vocabulary tagged session log.
- /recall MVP shipped: search across session logs by query. Cites file paths every time.
- voice-ben refactored into structured YAML spec; /voice-audit added for deterministic enforcement.

Try first:
  /done                                          # at the end of the next session
  /recall when did I decide on BLUPs            # after a few sessions accumulate
  /voice-audit manuscripts/paper_draft_v4_final.md

Out of scope, deferred per your brief: continuous improvement pipeline, real vector-DB recall.
Phase 3 handover (improvement pipeline) is on standby once these are in regular use.
```

That's the handover. Three skills, dependency-ordered, time-budgeted, scope-disciplined.
