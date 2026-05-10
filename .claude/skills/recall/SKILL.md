---
name: recall
description: Search across saved session logs, SESSION_REPORT, research journal, and project STATUS files for past decisions, discussions, or context. Returns a structured answer with file paths cited every time. Use when asking "when did I decide X" or "what did I conclude about Y".
---

# /recall

**Usage:** `/recall <query>`

Examples:
```
/recall when did I decide to use BLUPs over bivariate slopes
/recall what did the council critique flag about the empirical walkthrough
/recall did I cite Vlandas-Halikiopoulou anywhere
/recall what was the Phase 2 plan for the asymmetric-welfare paper
```

MVP architecture: text search + LLM summarisation over the project's session corpus. Not a vector index. Performance is fine for the first 1–2 years of accumulated logs; upgrade to vector search only when context-window viability breaks.

---

## Phase 1 — Build corpus

Read these paths in order, capping the total at ~50 files:

1. `quality_reports/session_logs/*.md` (date-ordered, newest first)
2. `SESSION_REPORT.md` at project root
3. `quality_reports/research_journal.md`
4. `projects/*/STATUS.md` (all active project STATUSes)

**Skip files under `quality_reports/session_logs/_private/`** — these are excluded by convention from the recall corpus.

If the corpus has >50 entries, prefer the **30 most recent session logs** + the four canonical files above. Skip older logs unless the query explicitly mentions a date range.

Read each file fully; do not pre-summarise. Fidelity matters at this stage.

## Phase 2 — Pre-filter by topic (optional)

The `/done` controlled vocabulary (see `.claude/skills/done/SKILL.md`) lists known topics. If the user's query contains words that match a controlled-vocab topic — e.g., "BLUPs" → `multilevel-models`, "council" → `council-skills`, "asymmetric mechanism" → `theory` — pre-filter the corpus to session logs tagged with that topic.

Topic-keyword associations:
- `multilevel-models` ← BLUPs, random slopes, mixed model, cross-level interaction, ICC
- `identification` ← parallel trends, IV, RDD, DiD, instrument
- `council-skills` ← council, persona, critique panel, ideation panel
- `voice` ← voice-ben, humanize, em-dash, GPT zero, detector
- `paper-draft` ← abstract, intro, §V, manuscript, draft
- `infrastructure` ← skill, agent, settings, hooks, MEMORY.md
- `theory` ← asymmetric, dignity, decommodification, mechanism, CWED
- `lit-review` ← citation, INDEX, lit note, scoop
- `data-cleaning` ← ESS, ISSP, CWED merge, ISCO crosswalk
- `defence-prep` ← seminar, walkthrough, Q&A, methods defense
- `talk-prep` ← slides, build_slides, Quarto, beamer, speaker

Pre-filtering is a perf optimisation, not a correctness gate. If pre-filtering returns zero matches, fall back to the full corpus rather than reporting "not found."

## Phase 3 — Search and summarise

Within the filtered corpus, find the **3-5 most relevant entries** to the query. Relevance = direct mention of the query terms, related concept, or session topic that overlaps. For each:

1. Extract the specific decision, discussion, or claim that addresses the query.
2. Note the file path and date (parse from filename or date heading).
3. Quote the relevant 1-3 sentences verbatim where possible — fidelity beats paraphrase.

Use `Grep` for the keyword pass when the corpus is large; use `Read` when you've narrowed to a handful of files.

## Phase 4 — Return a structured answer

Always print this shape, even if the answer is "not found":

```
## Direct answer

<One paragraph. If the corpus contains a clear answer, state it with the date and source. If the corpus does not contain a clear answer, say so explicitly: "The corpus does not directly answer this. The closest related discussion is [X]." Never fabricate.>

## Top 3 relevant sessions

1. **YYYY-MM-DD — <session topic>** — `quality_reports/session_logs/YYYY-MM-DD_<slug>.md`
   <one-line summary of what the session covered relative to the query>

2. ...

3. ...

## Confidence

<One sentence: Was this answered from explicit corpus content, inferred from related but non-identical content, or absent from the corpus? Use one of: HIGH (explicit), MEDIUM (inferred), LOW (absent or speculative).>

## Suggested next read

The single most relevant file path. Preferably full path so the user can click.

## Files consulted (audit trail)

- N session logs scanned
- SESSION_REPORT.md, research_journal.md, projects/*/STATUS.md
- Pre-filter topic: <topic if applied, else "none">
```

---

## Implementation rules

- **Cite paths every time.** Every claim in the direct answer must be traceable to a specific file. No floating claims.
- **Be conservative on direct answers.** If the corpus is silent, say so. The skill is an archive search, not a memory simulation. Better to return "not in corpus" than to invent.
- **No subagent dispatch for the MVP.** Read + Grep in the main session is faster and more transparent than spawning a general-purpose agent.
- **Print the audit trail.** The user must be able to verify what the skill consulted. The "Files consulted" section is mandatory.
- **Honour `_private/`.** Never read or surface anything under `quality_reports/session_logs/_private/`. The convention exists so Ben can put sensitive notes there without cross-session leakage.
- **Don't auto-edit anything.** This is read-only. No writes, ever.
- **Don't speculate.** If a file mentions "the council critique flagged X" and the query asks about Y, don't infer Y from X. Stick to what's explicit.

---

## Performance notes

- **Read budget:** total corpus reads should not exceed ~50 files. If `quality_reports/session_logs/` grows beyond 50 entries, prefer the 30 most-recent + canonical files.
- **Date-range filtering** is a future upgrade. For now, the recency-bias of "most recent first" is sufficient.
- **Grep speed:** use `Grep` first for the keyword pass when the corpus has >10 files; only `Read` the files Grep flags. This is 5-10× faster than Read-everything-and-skim.

---

## What this skill is *not*

- **Not a memory simulation.** The skill returns what the corpus says, not what Claude infers about Ben's mental model.
- **Not a vector search.** No embeddings, no similarity scoring, no clustering. Lexical match + Claude's reading.
- **Not auto-triggered.** Manual invocation only. Auto-triggering would create false starts and noise.
- **Not a substitute for `/resume`.** `/resume` reads STATUS + recent commits + plans for context-restoration; `/recall` is for targeted past-decision lookup. Use both.
- **Not a replacement for `git log` / `git blame`.** Those are authoritative for "what changed in code." `/recall` is for "what was decided about a topic across sessions" — a different dimension.
