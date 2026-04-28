# 🧠 CLAUDE.md — Session Primer

> **Read this file at the start of every session. ~100 lines. Everything else is on-demand.**

---

## Researcher

**Ben Smart** (`bencsmart@gmail.com`) — MSc Economics (University of Copenhagen, conferred 2026), beginning PhD in political economy / comparative politics.

**Focus:** How economic disruption (automation, trade, austerity) shapes political preferences — specifically populist and radical right support — and what welfare state design can do about it.

**Code stack:** Python (.py) and R (.R / .Rmd). Data files are mostly .dta — load with `pyreadstat` (Python) or `haven` (R).

---

## Pointers (load on demand)

| What | Where |
|------|-------|
| Paper status + decisions | `projects/seminar_paper/STATUS.md` |
| Thesis designs | `projects/msc_thesis/STATUS.md` |
| Theory module quick-ref | `docs/theory/README.md` |
| Literature index (greppable) | `docs/literature/INDEX.md` |
| Theory → data mapping | `metadata/theory_data_bridge.md` |
| Literature → theory mapping | `metadata/literature_map.md` |
| Data dictionary | `metadata/data_dictionary.md` |
| Persistent corrections | `MEMORY.md` |
| **Working relationship & calibration** | **`docs/working_with_ben.md`** |
| **Intellectual portrait** | **`docs/A Mind in Formation with part 6.md`** |
| Strategic memo (active sprint) | `docs/strategic_memo_2026-04-25.md` |

**Convention:** Never read .pdf, .docx, or files >500 lines in main context. Use the explorer agent or convert with pandoc first.

---

## Voice & Collaboration Rules (standing context)

**Before drafting anything that will appear under Ben's name:** invoke the `voice-ben` skill. Pre-AI samples in `manuscripts/Writing Samples/` are the calibration. Em-dashes are the #1 AI tell and not in his voice; use semicolons. Distinctive transitions: `Indeed`, `Furthermore`, `Through this perspective`, `Effectively`, `undergirding`, `as purported by`, `Drawing on`, `Firstly/Secondly/Thirdly`.

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
├── manuscripts/               ← Paper drafts (v3_final is current)
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

| Concept | Variable | Dataset | Notes |
|---------|----------|---------|-------|
| Country (ISO-2) | `cntry` | All ESS | |
| ESS round | `essround` | All ESS | |
| ISCO-08 occupation | `isco08` | ESS waves 6–9 | 4-digit; truncate to 3-digit before task merge |
| Routine task intensity | `task` | isco08_3d-task3.csv | **NOT** `rtask`/`nrtask` |
| RTI standardised | `task_z` | Constructed | Mean 0, SD 1 |
| Anti-immigration index | `anti_immig_index` | Constructed | 3-item composite, α=0.864 |
| Redistribution support | `redist_support` | Constructed | `gincdif` reverse-coded, 1–5 |
| CWED generosity | `cwed_generosity` | CWED | Mean 2005–2011, 15 countries |
| Welfare regime | `welfare_regime` | Constructed | Nordic/Continental/Liberal/Southern/Eastern |
| Radical right vote | `radical_right_vote` | Constructed | Langenkamp crosswalk |
| Household income | `hinctnta` | ESS | 21-30% missing in Liberal/Southern |

---

*Last updated: April 2026. Target: ≤100 lines. Update when research direction changes or new data added.*
