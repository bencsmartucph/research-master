---
name: done
description: Project-level session capture. Writes a structured session log to quality_reports/session_logs/, appends to SESSION_REPORT.md and research_journal.md, and updates the active project STATUS.md. Tags with controlled-vocabulary topics so /recall stays queryable. Use at session-end to make context durable for the next session.
---

# /done

**Usage:** `/done` *(no arguments — the skill identifies the active project automatically)*

Project-level session capture. Coexists with the user-level `/done` command at `~/.claude/commands/done.md`; this project skill takes precedence in the Research_Master context and writes to project-specific paths instead of global ones. The two are complementary, not duplicative — the user-level command handles cross-machine routing, working-notes, global handoff; this project skill handles project artefacts (STATUS, SESSION_REPORT, research_journal, controlled-vocab session log).

If you also want global capture, invoke the user-level `/done` separately or via the natural-language trigger after this skill completes.

---

## Controlled vocabulary — TOPICS

Session-log entries MUST tag topics from this fixed list. New topics require an explicit user nod before being added (the skill prompts; never silently invents).

```
econometrics            — model specifications, estimators, inference
identification          — causal design, IV, RDD, DiD, parallel trends
multilevel-models       — random slopes/intercepts, BLUPs, cross-level interactions
data-cleaning           — ESS / ISSP / CWED / register data wrangling
data-discovery          — locating new data sources or coverage
theory                  — asymmetric mechanism, dignity, decommodification
lit-review              — paper ingestion, INDEX updates, positioning
paper-draft             — writing, abstract revisions, section restructuring
voice                   — voice-ben work, humanize-academic, detector resistance
infrastructure          — skills, agents, rules, settings, project-meta
council-skills          — council-critique, council-ideate, persona work
thesis-design           — thesis chapter planning, registry data, PhD scope
defence-prep            — seminar prep, methods walkthrough, Q&A rehearsal
talk-prep               — slides, speaker scripts, conference materials
robustness              — sensitivity analyses, jackknife, spec curves
ideation                — brainstorming, research-direction work
admin                   — supervisor email, deadlines, application logistics
```

When a session topic doesn't fit any of the above, the skill prompts:

> *"Topic not in controlled vocabulary. Closest matches: [X], [Y]. Add new topic '[proposed]' to the list, or use one of these? (Add | Use [X] | Use [Y])"*

If the user adds, edit this skill's vocabulary list in the same `/done` invocation. Only add once — don't grow the list per-session.

---

## Procedure

### Step 1 — Identify the active project

Determine which project this session worked on:

1. **Most recent STATUS.md modification.** Check `projects/*/STATUS.md` mtimes — newest is the default candidate.
2. **Conversation evidence.** If the session touched files under `projects/<name>/`, `manuscripts/`, or `talks/`, that's the project. Cross-check against the STATUS mtime; mismatch → ask the user.
3. **Ambiguous.** If multiple projects were touched or none clearly dominate, ask:
   > *"Active project for this session? (seminar_paper | msc_thesis | none)"*

If `none`, the skill skips the STATUS.md update step but still writes session log + SESSION_REPORT + research_journal.

### Step 2 — Generate the session summary

Extract from the conversation. Required sections:

- **What was done** — bulleted list of concrete actions (files created/modified/deleted, scripts run, decisions made, agents dispatched). Cite paths where applicable.
- **Decisions and rationale** — for each non-trivial choice, what was decided and why (1-2 sentences each). Don't include trivial implementation choices.
- **Blockers / open questions** — anything unresolved. Frame each as a specific question the next session can act on, not a vague concern.
- **Next session pointer** — one or two sentences naming the single most important thing to do first next time.
- **Topics** — comma-separated tags from the controlled vocabulary above. 1-4 topics typical; 6+ is a sign the session was unfocused and worth flagging.

### Step 3 — Append to four files

**a) `quality_reports/session_logs/YYYY-MM-DD_<short-description>.md`** (new file per session)

Format:

```markdown
# Session — YYYY-MM-DD: <short description>

**Topics:** topic1, topic2, topic3

## What was done
- ...

## Decisions and rationale
- **Decision:** ...
  **Why:** ...

## Blockers / open questions
- ...

## Next session pointer
...
```

The `<short-description>` slug: 3-6 words from the dominant session topic, lowercased, hyphen-separated. Examples: `council-skills-deployment`, `voice-yaml-refactor`, `blups-disclosure-fix`. If a file already exists with the same slug today, append `_2`, `_3`.

**b) `SESSION_REPORT.md`** at project root (consolidated operations log; create if missing)

Append a dated entry per the template in `.claude/rules/logging.md`:

```markdown
## YYYY-MM-DD HH:MM — <Session topic>

**Project:** <name or "General">
**Topics:** topic1, topic2

**Operations:**
- ...

**Decisions:**
- ... — ...

**Results:**
- ...

**Status:**
- Done: ...
- Pending: ...
```

If the file doesn't exist, create with header `# Session Report — Research_Master`. Append-only; never overwrite.

**c) `quality_reports/research_journal.md`** — *only if at least one agent was dispatched this session* (per the rules in `.claude/rules/logging.md`)

One line per agent dispatch:

```markdown
### YYYY-MM-DD HH:MM — <agent-name>
**Phase:** <Discovery/Strategy/Execution/Peer Review/Presentation>
**Target:** <file or topic>
**Score:** <NN/100 or PASS/FAIL or N/A>
**Verdict:** <one-line summary>
**Report:** <path or "in session">
```

If no agents were dispatched, skip this file entirely.

If the file doesn't exist, create with header `# Research Journal — Research_Master` and add the entry.

**d) Active project's `STATUS.md`** (if active project identified)

Append a `## YYYY-MM-DD session` block at the END of the file (NOT the top — STATUS.md is forward-looking; session blocks accumulate at the bottom for chronological audit):

```markdown
## YYYY-MM-DD session

**What was done**
- ...

**Decisions**
- ...

**Open questions**
- ...
```

Skip the Topics field here (STATUS.md is for project state, not for /recall indexing).

### Step 4 — Bloat check on STATUS.md

After updating, count lines in STATUS.md. If >600 lines, prompt:

> *"STATUS.md is now N lines. Roll over older session blocks to projects/<name>/_archive/STATUS_YYYY-MM.md? (yes / not yet)"*

If yes, move all `## YYYY-MM-DD session` blocks older than 30 days into the archive file. Keep the head of STATUS.md (Paper, Empirical Narrative, etc.) untouched.

### Step 5 — Print confirmation (≤5 lines)

```
SESSION CAPTURED — <topic summary>
Topics: <comma-separated>
Files updated: <count> [session log, SESSION_REPORT, (research journal,) (STATUS)]
Session log: quality_reports/session_logs/YYYY-MM-DD_<slug>.md
Next: <one-line next-session pointer>
```

---

## Implementation rules

- **Don't auto-trigger writer / voice-ben / humanize-academic on session-summary text.** Session logs are infrastructure, not prose Ben publishes. The voice skills must skip them.
- **Use atomic writes for SESSION_REPORT.md and research_journal.md.** Both are append-only; concurrent invocations across machines could corrupt them. If write fails, surface the error in the confirmation; don't silently skip.
- **Cite paths every time.** Every "Files updated" reference uses the exact path so `/recall` can find it later.
- **Resist topic bloat.** The vocabulary must stay small for `/recall` to work. If the user proposes a new topic, ask whether an existing one covers it; only add when genuinely novel.
- **No clever inference about project identity.** If ambiguous, ask. Wrong project tagging poisons the corpus.
- **Don't index `_private` session logs.** Any session log under `quality_reports/session_logs/_private/` is excluded from this skill's writes (the skill writes only to the main directory). `/recall` honours the same convention.

---

## What this skill is *not*

- **Not the user-level `/done`.** That command writes to `~/Documents/session-log.md`, `~/.claude/handoff.md`, and routes via CWD-precedence. This project skill writes to project paths. Either or both can be invoked.
- **Not a working-notes archiver.** If the session produced substantial draft content not yet saved to a real file, save it explicitly first; this skill only logs metadata.
- **Not a quality gate.** It captures what happened; it does not score or block.
