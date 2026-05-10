# HANDOVER — 2026-05-04

*Read this first. ~3 minutes. Then open the four essay drafts in `essays/patient_tutor/` and the index file alongside them.*

## Where things stand

Two parallel projects shipped major work in the last 48 hours.

**Research project (Research_Master proper).** The empirical walkthrough document for §V is finished and lives at `docs/empirical_walkthrough_v1.md` (~17,200 words, 8 static figures embedded, 3 interactive Plotly HTMLs linked, "Defending the choice in 30 seconds" rehearsals at the end of every concept). The substantive find of the week is the BLUPs methodology correction in §V.D — the published r = −0.848 comes from BLUPs of a random-slopes mixed model with controls, not the bivariate per-country OLS the older code path implements. A two-sentence disclosure has been inserted into `manuscripts/paper_draft_v4_final.md` §V.D (2026-05-03). The supporting code lives in an updated `scripts/random_slopes_models.py` (now includes two-country jackknife, RI vs RS comparison, per-country slopes vs CWED). All figures and interactives produced by `analysis/walkthrough_figures.py` and three companion scripts.

**Public-writing project (new `essays/` directory).** Four complete drafts of the LinkedIn-first essay, each in a different form and register. They live in `essays/patient_tutor/` alongside `VERSIONS_INDEX.md` which compares them. The four versions are:

- `v_false_dichotomy.md` — argument-driven, contested-thesis essay (~1,450 words)
- `v_building_is_learning.md` — optimistic pedagogy essay (~1,400 words)
- `v_discovery_story.md` — pure narrative, no overt thesis (~1,600 words)
- `v_curious_confession.md` — short lyrical confession (~750 words)

The previous draft (`draft.md`) is the paper-is-the-curriculum version from the side session and is now superseded by the four newer versions. Keep it as a fifth comparison point if useful.

The Compile Error long-form essay has not been drafted; the research base for it sits at `docs/learning_econometrics/compile_error_research_base.md` and the source material at `docs/learning_econometrics/the_paper_is_the_curriculum.md`. Both are ready to mine when you start that piece — target window is across summer per the strategy discussion.

## What you need to do tomorrow

1. **Read the four drafts in order.** Don't read the index first. Open each draft cold and read the opening paragraph; keep notes on which one made you want to keep reading.
2. **Read `VERSIONS_INDEX.md`** after the cold-read pass. It compares them on form, audience, and what each one risks.
3. **Choose one** (or specify a hybrid if you want me to combine elements across versions).
4. **Apply the retype protocol**: read the chosen draft once, close the file, type the opening paragraph and the closing paragraph from memory. Don't re-open while typing. Roughness helps.
5. **Publish or hand back to me for the final polish pass.**

If you want me to draft the next version (combining elements from across the four), open a fresh session with the new specification — the current session is heavy with this work and a clean session will be sharper.

## What's been committed and what hasn't

I have prepared two staged commits but not pushed yet — see "Git state" below. Talks/, Yiwen.pdf, the .docx of the paper, and the unrelated changes in `manuscripts/Writing Samples/` are deliberately left unstaged because they're separate concerns and you should review them before deciding.

## Strategic direction (for fresh-eyes context)

The writing project has three pieces in queue, prioritised:

| Piece | Status | Window | Audience |
|---|---|---|---|
| Patient Tutor (LinkedIn) | Four drafts ready; choose tomorrow | This week | LinkedIn, Anthropic-as-employer audience |
| Compile Error (Substack long-form) | Research base assembled | Across summer | Substack subscribers, AI-and-knowledge-work corner of the internet |
| Workflow piece | Dropped | — | Absorbed into Compile Error if needed; will date by summer |

The Compile Error essay's three load-bearing claims (friction collapse, asymmetry equalisation, skill bifurcation) are independent and could each be their own piece. Decide closer to the time whether to publish as one essay or three.

The undergraduate redesign (project + oral assessment, AI explicitly allowed in production) sits as a possible future op-ed for *Inside Higher Ed* or similar. Not in the immediate queue.

## Persistent learnings now in MEMORY.md

Six new entries added today, covering: the BLUPs methodology fact, the new diagnostics in `random_slopes_models.py`, the figures pipeline, the empirical walkthrough document, the BLUPs paper disclosure, the essays/ directory conventions, the voice-ben skill triggering rules, the multi-session adversarial iteration pattern, and the anchor-paragraph retype protocol. Read MEMORY.md if you haven't lately.

## Git state

The following groups of changes are ready to stage as two clean commits:

**Commit 1: Empirical walkthrough infrastructure**
- `docs/empirical_walkthrough_v1.md`
- `analysis/walkthrough_figures.py`, `analysis/walkthrough_interactive.py`, `analysis/walkthrough_cluster_se_interactive.py`, `analysis/walkthrough_cross_level_interactive.py`, `analysis/_diagnose_cwed_correlation.py`, `analysis/ch01_selection_bias_interactive.py`
- `scripts/random_slopes_models.py` (modified — adds RI vs RS, per-country slopes, two-country jackknife)
- `manuscripts/paper_draft_v4_final.md` (modified — BLUPs disclosure in §V.D)
- `outputs/figures/walkthrough/` (new directory, all 11 outputs)
- `outputs/tables/jackknife_*.csv`, `outputs/tables/per_country_slopes.csv`, `outputs/tables/rs_vs_ri_model3.csv`

**Commit 2: Public-writing project + learning resource**
- `essays/` (entire new directory)
- `docs/learning_econometrics/` (entire new directory)
- `MEMORY.md` (modified — new entries from this session)
- `HANDOVER.md` (this file)

I have NOT staged or committed these — see "What you should review before committing" below.

## What you should review before committing

- The talks/ updates (separate seminar prep — review separately)
- `manuscripts/Writing Samples/Voice and Writing Style.txt` (modified — what changed?)
- `manuscripts/Writing Samples/abstract examples.txt` (deleted — intentional?)
- `setup_data_raw.py` (deleted — intentional?)
- `docs/four_prompts.md` (deleted, then re-added at `docs/archive/four_prompts.md` — confirm the move)
- `Yiwen.pdf` and `Yiwen_annotated.pdf` (unrelated downloads — gitignore or stage?)
- `.claude/agents/orchestrator.md` and `.claude/skills/voice-ben/SKILL.md` (modified — what changed?)

If the answers to these are quick (yes commit / no don't), you can do it inline tomorrow morning. If any of them needs longer thought, they sit unstaged and don't block the two clean commits above.

## One thing I would do tomorrow even if I had time for nothing else

Read `essays/patient_tutor/v_curious_confession.md` and `essays/patient_tutor/v_false_dichotomy.md` back-to-back. They are the two extremes of what this piece could be — the lyrical short version and the contested long version. The choice between them is the most important strategic decision in the writing project, and the choice will probably be obvious within five minutes of reading both.

If neither feels right, the answer is probably `v_building_is_learning.md` (the safe LinkedIn-friendly version). If the discovery story version feels right, you're committing to publishing on Substack rather than LinkedIn. Each of those decisions cascades into the rest of the queue.

---

*Status: writing project at decision point; research project has shipped the consolidated defence document and the BLUPs paper disclosure; both are in clean state pending the two prepared commits. Sleep well; the work is in better shape than it was 48 hours ago.*
