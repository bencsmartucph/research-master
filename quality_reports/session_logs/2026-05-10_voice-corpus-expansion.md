# Session — 2026-05-10: Voice corpus expansion + pre-commit hook scope filter

**Topics:** voice, infrastructure

## What was done

- **Pre-AI corpus extraction** across 7 essays (22,167 words) in `manuscripts/Writing Samples/Pre-AI/`. Frequency-counted seed vocabulary; dispatched `general-purpose` subagent for deep pattern extraction.
- **voice-ben YAML refactor** (`.claude/skills/voice-ben/SKILL.md`):
  - Removed AI-extrapolated vocabulary that scored 0 in corpus (`valorises` in pure form, `instigates`, `inveigle`, `obsequious`, `avaricious`, `concomitant`, `incipient`, `pertinacity`, `progenitor`, `configurations`, `elucidates`, `presupposes`, `promulgates`).
  - Added corpus-verified high-frequency transitions: `Essentially,` (14x), `Corroborating this idea,` (5x), `Supporting this theory,` (6x), `This is exemplified by` (5x), the `Through this perspective` family (9 across variants), `Whilst X, Y` (7x, preferred 7:1 over `while`), `This perspective directs our attention to` (3x).
  - Added top-frequency verbs the seed list missed: `frame / framing` (22), `reinforces` (12), `facilitates` (11), `exemplifies` (9), `legitimises` (7), `harnesses` (5), `augments` (5), `problematises` (4), `characterises` (5).
  - Added new `negative_space` section listing words that sound like Ben's register but appear 0 times in 22k words (hegemony, ethos, milieu, valence, imaginary, assemblage, ensemble, conjuncture, edifice, etc.) so future audits reject them proactively.
  - British -ise spelling preference codified.
  - Calibration history extended to 2026-05-10.
- **Created `manuscripts/Writing Samples/voice_lexicon.md`** — standalone writing-aid lexicon. Top-30 quick reference, transitions organised by purpose (open / pivot / cite / close / enumerate), distinctive verbs by function, citation-attribution verbs ranked by frequency, six argumentation moves with quoted examples from the corpus, negative-space anti-list, spelling preferences, quarterly maintenance protocol.
- **Two commits + push to `origin/master`**:
  - `309f7e2` infra: post-deployment session log + SESSION_REPORT update (prior session's loose ends)
  - `25927d0` voice: corpus-verified lexicon + voice-ben YAML expansion
- **Pre-commit hook scope filter** (`~/.claude/hooks/check-em-dashes.py`, user-level):
  - Added `SKIP_PATH_PARTS`, `SKIP_FILENAMES`, `SKIP_PATH_GLOBS` lists mirroring voice-ben's `scope_excludes`.
  - 15-case test against representative paths: all OK. Signed prose still audited; infrastructure / tutor docs / session logs correctly excluded.

## Decisions and rationale

- **Decision:** Built standalone `voice_lexicon.md` alongside the YAML refactor rather than only updating the spec.
  **Why:** Ben asked for a list he can use as a writing aid (he used to keep one before). The YAML is canonical for `/voice-audit`; the lexicon is for him to scan while drafting.
- **Decision:** Added a `negative_space` section to the YAML and the lexicon — words that *sound* like Ben's register but score 0 in 22k words.
  **Why:** Most vocabulary calibration tells you what to use; the failure mode for AI-detection is reaching for theory-vocabulary that *sounds* like the writer but isn't. The anti-list catches that drift before it ships.
- **Decision:** Pre-commit hook filter implemented at user level (not project `.git/hooks/`).
  **Why:** Path conventions like `quality_reports/`, `.claude/`, `MEMORY.md`, `STATUS.md` are Ben's portable conventions across all repos per his global preferences. Centralising the exclusion list in `~/.claude/hooks/` avoids maintenance per-repo.
- **Decision:** Did NOT auto-commit the /done outputs.
  **Why:** Per CLAUDE.md global rule. User decides when to commit session logs.

## Blockers / open questions

- Should the calibration sources `Pre-AI/*` themselves be excluded from voice-audit? They're signed prose so excluding them is wrong; but a hypothetical edit to a 2017 essay would currently trigger the audit. Defaulting to "audit them" — they're the calibration ground-truth and should pass cleanly. Surface this only if a real edit triggers a warning.
- The lexicon's "frame / framing" verb has 22 occurrences but the verb-vs-noun split wasn't separated by the extraction subagent. May want to verify how many are verbal "frame this as X" vs nominal "the frame".

## Next session pointer

If picking up the voice work: re-run `/voice-audit manuscripts/paper_draft_v4_final.md` after fixing the 4 em-dash apposition stackings flagged in `quality_reports/voice_audits/2026-05-08_paper_draft_v4_final.md`. Expected score post-fix: 88-92. If detector resistance still matters, anchor-paragraph retype (open + close paragraphs typed from memory).
