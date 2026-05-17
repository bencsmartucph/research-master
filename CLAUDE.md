# 🧠 CLAUDE.md — Session Primer

> **Read this file at the start of every session. ~100 lines. Everything else is on-demand.**

---

## Environment

- OS: Windows. Prefer PowerShell tool for shell commands; fall back to Bash only when needed.
- Git is not always on PATH for plugin/marketplace installs. If `git not found` appears, suggest setting PATH or using full path to git.exe rather than retrying.
- `.claude/` writes require interactive approval — never dispatch parallel sub-agents for edits inside `.claude/`. Edit those from the main session.

---

## Ask before persistent writes (bypass-permissions guard)

Ben often runs in **bypass-permissions mode**, so the harness will not prompt before writes. This means *Claude* has to be the gate. Before writing or editing any of the following, **explicitly ask first** — even for what looks like a small change:

- `CLAUDE.md` (any), `MEMORY.md`, `~/.claude/CLAUDE.md`
- Anything inside `.claude/skills/`, `.claude/agents/`, `.claude/rules/`, `.claude/settings*.json`
- `projects/*/STATUS.md` *content edits* (the `/done` skill's appended session blocks are exempt)
- Adding a new entry to controlled vocabularies (e.g., `/done` topics list)

For ordinary working files (scripts, manuscripts, figures, session logs, plans), proceed without asking. The rule targets *persistent context that auto-loads forever* — those edits compound, so they need a human nod every time.

Phrasing: *"I want to add X to MEMORY.md / CLAUDE.md / the done skill — confirm?"* One line, then wait.

---

## Voice gate before publication

Before committing prose Ben will sign (papers, abstracts, blog posts, applications), run `/voice-audit <path>`. Score must be ≥ 75 (Mixed → Recognisable band) before commit. Fix flagged violations, re-run, repeat.

---

## Verification before building

When verifying methodology or statistics (e.g., which model spec produced a published coefficient), always reproduce/verify against ground-truth source data before building outputs on the number. Flag discrepancies explicitly rather than proceeding. Do not trust secondary-source claims about formatting, parameters, or results when the primary source is accessible.

---

## Project Context — primary heuristic for this sprint (added 2026-05-10)

**Primary heuristic: accelerated completion of the seminar paper.** Every recommendation, edit, and follow-up should balance *maximum possible quality* against the *practical constraints of current data and timeline*. Concrete operational implications:

- **Defer, do not ignore, the council critique on the empirical walkthrough.** Its CRITICAL items (Oster δ bounding of N=15 confounding, BLUPs specification curve, effective-N reframing, TOST + SUR equivalence testing, AJPS-grade scoop positioning) are valid for journal-version rewrite or if time permits. They likely are out of scope for the seminar paper per Amalie's "no more analysis, hone argument" instruction. Filed at `quality_reports/journal_version_targets/`.
- **Ship the asymmetric framing as committed.** The v3/v4 hedge into symmetric "sorting" language was diagnosed as self-protection (see Part 6 of `docs/A Mind in Formation with part 6.md`). The asymmetric reframe is final; further theoretical excavation does not improve the paper at seminar stage.
- **Monday-morning retype pass is the last substantive editing block before submission.** §III.D, §I sign-post, §III.A forward-reference, §III.E para 3, §V.D BLUPs sentence — retype from evidence base in own keystrokes for detector-resistance. Don't expand scope past that.
- **Any "another analytical pass" recommendation must be explicitly justified against this heuristic.** Default disposition: defer to journal stage or MSc thesis (autumn 2026 → spring 2027) follow-up.
- **Single source of truth:** when this block conflicts with older notes elsewhere, this block wins. Older docs flagged stale will be pruned at next consolidation pass.

---

## Researcher

**Ben Smart** (`bencsmart@gmail.com`) — MSc Economics at the University of Copenhagen (in progress; thesis autumn 2026 → spring 2027). Preparing PhD applications for **Fall 2027 start** (deadlines Nov 2026 – Jan 2027). Employed at CEBI; Danish-register data access for the MSc thesis comes via this employment. Fresh Forskerservice authorisation belongs in 2027 PhD-stage planning, not now.

**Focus:** How economic disruption (automation, trade, austerity) shapes political preferences — specifically populist and radical right support — and what welfare state design can do about it.

**Code stack:** Python (.py) and R (.R / .Rmd). Data files are mostly .dta — load with `pyreadstat` (Python) or `haven` (R).

---

## Pointers (load on demand)

| What                                                 | Where                                                                           |
| ---------------------------------------------------- | ------------------------------------------------------------------------------- |
| Paper status + decisions                             | `projects/seminar_paper/STATUS.md`                                              |
| Thesis designs                                       | `projects/msc_thesis/STATUS.md`                                                 |
| Theory module quick-ref                              | `docs/theory/README.md`                                                         |
| Literature index (greppable)                         | `docs/literature/INDEX.md`                                                      |
| Theory → data mapping                                | `metadata/theory_data_bridge.md`                                                |
| Literature → theory mapping                          | `metadata/literature_map.md`                                                    |
| Data dictionary                                      | `metadata/data_dictionary.md`                                                   |
| Persistent corrections                               | `MEMORY.md`                                                                     |
| **Working relationship & calibration**               | **`docs/working_with_ben.md`**                                                  |
| **Intellectual portrait**                            | **`docs/A Mind in Formation with part 6.md`**                                   |
| Strategic memo (current, 2026-05-10)                 | `docs/strategic_memo_2026-05-10.md`                                             |
| Strategic memo (six-week sprint, prior)              | `docs/strategic_memo_2026-04-25.md`                                             |
| **Council critiques + ideations + voice audits**     | **`quality_reports/council_critiques/`, `council_ideations/`, `voice_audits/`** |
| **Journal-version deferral folder**                  | **`quality_reports/journal_version_targets/`**                                  |
| **Build commands (docx, slides, figures, analysis)** | **`scripts/README.md`**                                                         |

**Convention:** Never read `.pdf` or files >2000 lines in main context. `.docx` is fine after `pandoc` conversion to `.md` (if under 2000 lines). Files 500–2000 lines may be read directly when calibration / analytical fidelity matters. Subagents doing analytical work must return raw counts + method, not just summary stats. See `.claude/rules/heavy-reads.md` for the full contract.

---

## Voice & Collaboration Rules (standing context)

**Before drafting anything that will appear under Ben's name:** invoke the `voice-ben` skill. Pre-AI samples in `manuscripts/Writing Samples/Pre-AI/` are the calibration; the full corpus-verified lexicon lives in `manuscripts/Writing Samples/voice_lexicon.md` and the canonical machine-readable spec is the YAML frontmatter of `.claude/skills/voice-ben/SKILL.md`. Em-dashes are banned (target 0); use semicolons or the ` - ` (space-hyphen-space) clause-break pattern. For distinctive transitions, verbs, adjectives, and argumentation moves, refer to `voice_lexicon.md` rather than memorising a list — it's corpus-verified and updates when new signed prose enters the calibration corpus. (Earlier inline lists here contained `Drawing on` and `as purported by`, which score zero in the corpus and were AI-extrapolated entries; removed 2026-05-10.)

**Before recommending hedged prose:** invoke `notes-prose-gap`. He has a pattern of hedging in prose claims that his working notes have already accepted. Catch the gap; don't perpetuate it.

**For detector-resistance work:** invoke `humanize-academic`. Honest about limits — AI editing AI cannot reach high human-detection scores; the reliable fix is for him to type key paragraphs himself. Recommend that explicitly when surface editing is exhausted.

**For theory-heavy intros:** invoke `quote-mosaic`. The structure (3-5 direct quotes with author commentary) aligns with his curatorial method and breaks LLM perplexity signature. This worked on the asymmetric welfare paper (100% AI → 60% human in one restructure).

**Recommendation default:** when offered safe-vs-authentic choices, recommend authentic. When offered shorter-vs-deeper, recommend deeper. He picks the bigger move reliably and benefits from being offered it. See `docs/working_with_ben.md` for the full collaboration theory.

---

## Repository Map

```
Research_Master/
├── CLAUDE.md                  ← YOU ARE HERE
├── MEMORY.md                  ← Persistent [LEARN] corrections
├── README.md                  ← Human overview
│
├── projects/
│   ├── seminar_paper/STATUS.md ← Current paper state
│   └── msc_thesis/STATUS.md    ← Thesis designs
│
├── .claude/
│   ├── agents/                ← explorer, librarian, coder, writer-critic
│   ├── skills/                ← /analyze, /review, /write, /read-paper, /resume, /critique
│   └── rules/                 ← domain-profile, journal-profiles, figures, tables, working-paper-format, heavy-reads
│
├── docs/
│   ├── theory/                ← 15 theory modules + README.md + theory_index.json
│   └── literature/            ← 97 paper notes + INDEX.md
│
├── metadata/
│   ├── data_dictionary.md     ← Column schemas (~2.8 MB, load sections on demand)
│   ├── theory_data_bridge.md  ← Theory → datasets → variables
│   └── literature_map.md      ← Theory → top papers
│
├── data/
│   ├── raw/                   ← 19 study folders (~2.6 GB, git-ignored)
│   └── samples/               ← top100/ and stratified/
│
├── scripts/                   ← load_ess.py, load_ess.R, make_stratified_samples.py
├── manuscripts/               ← Paper drafts (v4_final is current; v3/v5/medium-bet archived May 2026)
├── analysis/                  ← Pipeline, master dataset, results, review
├── outputs/                   ← figures/ and tables/
└── quality_reports/           ← plans/ and session_logs/
```

---

## Key Data Relationships

### ESS → occupation task scores (automation exposure)

```python
import pyreadstat, pandas as pd
df, _ = pyreadstat.read_dta('data/raw/gugushvili_2025/ESS1e06_7 (1)/ESS1e06_7.dta')
tasks = pd.read_csv('data/raw/shared_isco_task_scores/isco08_3d-task3.csv')
df['isco08_3d'] = df['isco08'].astype(int) // 10
df = df.merge(tasks, on='isco08_3d', how='left')
# CRITICAL: column is 'task', NOT 'rtask' or 'nrtask' — see MEMORY.md
```

### ESS → populist party classification

```python
crosswalk = pd.read_csv('data/raw/langenkamp_2022/ess_populist_crosswalk.csv', sep=';')
# CRITICAL: semicolon-delimited — see MEMORY.md
```

### ESS → CWED welfare generosity (paper's key moderator)

```python
# CWED merged at country level as time-invariant (mean 2005-2011)
# 15 Western European countries (58% of obs). Variable: cwed_generosity
# Constructed in analysis/final_analysis_pipeline.py
```

---

## Variable Quick Reference

| Concept                | Variable             | Dataset             | Notes                                          |
| ---------------------- | -------------------- | ------------------- | ---------------------------------------------- |
| Country (ISO-2)        | `cntry`              | All ESS             |                                                |
| ESS round              | `essround`           | All ESS             |                                                |
| ISCO-08 occupation     | `isco08`             | ESS waves 6–9       | 4-digit; truncate to 3-digit before task merge |
| Routine task intensity | `task`               | isco08_3d-task3.csv | **NOT** `rtask`/`nrtask`                       |
| RTI standardised       | `task_z`             | Constructed         | Mean 0, SD 1                                   |
| Anti-immigration index | `anti_immig_index`   | Constructed         | 3-item composite, α=0.864                      |
| Redistribution support | `redist_support`     | Constructed         | `gincdif` reverse-coded, 1–5                   |
| CWED generosity        | `cwed_generosity`    | CWED                | Mean 2005–2011, 15 countries                   |
| Welfare regime         | `welfare_regime`     | Constructed         | Nordic/Continental/Liberal/Southern/Eastern    |
| Radical right vote     | `radical_right_vote` | Constructed         | Langenkamp crosswalk                           |
| Household income       | `hinctnta`           | ESS                 | 21-30% missing in Liberal/Southern             |

---

*Last updated: 2026-05-10. Target: ≤120 lines (with Project Context block; was ≤100). Update when research direction changes or new data added.*
