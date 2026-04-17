# Skill Audit — 2026-04-17

**Auditor:** Opus 4.7 (architect) using `/critique` on itself and siblings.
**Target:** `.claude/skills/{critique,read-paper,resume}/SKILL.md`

## Critic's findings (fresh-context subagent)
Produced via Agent tool, general-purpose subagent. Critic had stale repo state — correctly flagged real prompt/spec issues, falsely claimed `projects/` missing and `HANDOVER.md` still present.

## Patches applied

### /critique
- Subagent invocation now specifies Agent tool + `subagent_type: general-purpose` (was ambiguous "subagent not named agent").
- Added `---BEGIN WORK--- / ---END WORK---` fences to isolate content from caller framing.
- Dropped "summarize first if >500 lines" — critics need the exact text; added guidance to pass file path and let the critic Read.
- Filled in flag-variant prompt text (`--theory`, `--methods`, `--writing`, default) that was previously referenced but unspecified.
- Synthesis step now requires a one-sentence reason per rejected critique point (discipline against sunk-cost bias).

### /read-paper
- Replaced Unix-only `/tmp/converted.md` + single-quoted shell with bash `$(mktemp -d)` pattern that works on Git Bash for Windows.
- Added tool-availability probe + fallback chain for PDF (pymupdf → pdftotext → fail with install hint) and DOCX (pandoc or fail).
- Added scanned-PDF guard: if converted output <200 words, abort rather than write an empty note.
- Realigned on "subagent (general-purpose)" — no named agents (was inconsistent with /critique).
- Added concrete slug rule with collision suffixing.
- Removed auto-`git add`/`git commit` — user commits manually. Rationale: network-drive lock issues + risk of sweeping unrelated dirty files.
- INDEX append now dedupes via grep check.

### /resume
- Added Step 0: argument validation with a helpful "available projects:" listing.
- Dropped `--all` from `git log` (pulled unrelated branches).
- Empty-plans-directory guarded with `[ -z "$LATEST" ]` fallback.
- Plan-read window expanded from 30 to 40 lines (the NEXT line lives below status/approach in the template).

## Rejected critic points
- "projects/ directory doesn't exist" — REJECTED. Verified existence via Explore pre-critique. Critic had stale snapshot.
- "HANDOVER.md still tracked/modified" — REJECTED. Confirmed missing at repo root. Likely critic was seeing old git status from an older session.

## Verdict
Skills now fit for solo-research use. `/critique` earns its keep — applying it to itself surfaced 6 real specification gaps that a same-context review would have missed. The fresh-context adversarial pattern is validated.

## Next tasks in plan
- T2 (Gemini): build `docs/literature/INDEX.md`
- T3 (Gemini): build `metadata/literature_map.md`
- T4 (Sonnet fresh): archive 10 of 16 agents; delete `.claude/rules/archive/`
- T5 (after seminar submission): bootstrap `Thesis_Master/` sibling repo
