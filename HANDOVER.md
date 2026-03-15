# HANDOVER.md — Agent Briefing Document

> **Read this before touching anything.** This is the complete state-of-play for Ben Smart's dissertation research infrastructure as of 2026-03-14.
> You are a new Claude agent continuing work on this repository. Everything you need is here and in the files referenced below.

---

## Who You Are Helping

**Ben Smart** — PhD researcher, political economy / comparative politics. Dissertation: how economic disruption (automation, trade, austerity) shapes populist political behaviour in Europe, and what welfare state institutions can do about it. Early ideation stage — building theoretical and empirical infrastructure before committing to a specific chapter.

**Primary code stack:** Python (pyreadstat, pandas, statsmodels) and R (haven, tidyverse, fixest). NOT Stata, but most data is `.dta`.

**Tone:** Ben is technically capable and working fast. Be direct, skip preamble, propose concrete next steps. He values precision over hedging.

---

## Repository: Research_Master

**Location:** `Economics of the Welfare State/Research_Master/` on Ben's computer.
*(In this session: `/sessions/loving-sweet-sagan/mnt/Research_Master/`)*

This is a clean, AI-optimised research hub built from scratch in March 2026 by migrating and restructuring Ben's older `Data/` repository. The original `Data/` folder still exists — do not touch it.

### Full Structure

```
Research_Master/
│
├── CLAUDE.md                    ← PRIMARY SESSION PRIMER — read every session
├── HANDOVER.md                  ← THIS FILE
├── README.md                    ← Human overview
├── MEMORY.md                    ← Persistent LEARN tags — read before coding
│
├── .claude/
│   ├── rules/
│   │   └── domain-profile.md   ← Field calibration: journals, methods, data, referees
│   └── skills/                 ← [TO BUILD] Dissertation-specific skill files
│
├── docs/
│   ├── theory/                 ← 15 theory module .md files + theory_index.json
│   │   ├── 01_embedded_liberalism.md ... 15_cognitive_frames.md
│   │   └── theory_index.json   ← Machine-readable index + 97 literature notes
│   └── literature/             ← 97 paper notes (UUID-stripped, clean slugs)
│
├── metadata/
│   ├── data_dictionary.md      ← Schema + 5-row samples for ALL 104 datasets
│   ├── theory_data_bridge.md   ← ⭐ Theory modules → datasets → variables
│   └── papers/                 ← 16 per-paper context files
│
├── data/
│   ├── raw/                    ← 19 folders, 164 files, 2.6GB [git-ignored]
│   │   ├── MANIFEST.json       ← Index of all raw data folders
│   │   ├── gingrich_2019/      ← Automation & voting (ISSP ZA-files)
│   │   ├── kurer_2020/         ← Declining middle (SHP/BHPS/SOEP panels)
│   │   ├── baccini_2024/       ← Austerity & populism (ESS + district data)
│   │   ├── im_2021/           ← Radical right reservoir (pooled ESS)
│   │   ├── cicollini_2025/     ← Positional income change + party scores
│   │   ├── milner_2021/         ← Trade, regional data
│   │   ├── shared_isco_task_scores/ ← RTI task scores (the key merge file)
│   │   └── ... (13 more folders)
│   └── samples/
│       ├── top100/             ← 3 files (baccini, im, euroscepticism)
│       └── stratified/         ← 14 files stratified by cntry/essround/nuts2
│
├── scripts/
│   ├── load_ess.py             ← Python utility library (load, merge, RTI, EGP)
│   ├── load_ess.R              ← R mirror
│   └── make_stratified_samples.py
│
├── explorations/               ← [SANDBOX] Experimental work goes here first
│   └── (empty — create [project-slug]/ subdirs per experiment)
│
└── analysis/                   ← Production analysis (graduate from explorations/)
    outputs/figures/
    outputs/tables/
```

---

## The Three Knowledge Systems

Always use these together before writing code or designing analysis:

| System              | File                              | Use when                                                             |
| ------------------- | --------------------------------- | -------------------------------------------------------------------- |
| **Theory Bridge**   | `metadata/theory_data_bridge.md`  | Translating a mechanism into a testable variable                     |
| **Data Dictionary** | `metadata/data_dictionary.md`     | Looking up exact column names, value ranges, missingness             |
| **Domain Profile**  | `.claude/rules/domain-profile.md` | Calibrating analysis design, identification strategy, target journal |

**Mandatory pre-coding sequence:**

1. Read `CLAUDE.md` (you're doing this now via HANDOVER.md)
2. Read `MEMORY.md` — absorb all `[LEARN]` tags before writing any code
3. Check `theory_data_bridge.md` for the relevant theory module
4. Look up exact variable names in `data_dictionary.md`
5. Load from `data/samples/stratified/` to develop; switch to `data/raw/` when ready

---

## Workflow System (Clo-Author + DAAF Hybrid)

This repository implements a research workflow modelled on two open-source frameworks:

- **Clo-Author** (hsantanna.org/clo-author) — command-based research pipeline with worker-critic pairs
- **DAAF** (github.com/DAAF-Contribution-Community/daaf) — agent behavioural protocols, adversarial verification

### Command Reference

| Command                          | What runs                                                     | Output                                      |
| -------------------------------- | ------------------------------------------------------------- | ------------------------------------------- |
| `/discover --theory [mechanism]` | Read relevant module from `docs/theory/` + check bridge       | Mechanism summary + testable hypotheses     |
| `/discover --lit [topic]`        | lit-review-assistant skill + Consensus/Scholar Gateway search | Annotated bibliography, frontier map        |
| `/discover --data [construct]`   | source-researcher pattern on target dataset                   | Variable map, caveats, suppression patterns |
| `/strategize`                    | Strategist + strategist-critic (worker-critic pair)           | Strategy memo, pseudo-code, robustness plan |
| `/strategize --pap`              | Strategist in PAP mode                                        | Pre-analysis plan (AEA/OSF format)          |
| `/analyze [dataset]`             | data-planner → research-executor → code-reviewer              | Scripts + output + QA report                |
| `/analyze --dual r,python`       | Same analysis in R + Python, convergence check                | Two implementations + divergence flag       |
| `/review --peer [journal]`       | domain-referee + methods-referee (blind, parallel)            | Editorial decision + point-by-point         |
| `/review --methods`              | strategist-critic only                                        | Identification critique                     |
| `/review --code`                 | code-reviewer only                                            | Script QA                                   |
| `/tools learn`                   | Formalise a multi-step discovery into a skill                 | New `.claude/skills/[name]/SKILL.md`        |

*Note: These commands are workflow conventions. Invoke them by describing the intent to Claude — e.g., "Run a /strategize --pap for the following research question..."*

### Worker-Critic Pattern

Every substantive output should be reviewed adversarially before Ben sees it. Standard pair:

**For empirical strategy:**

- Worker: "You are the Strategist. Given this research question and the theory bridge, propose an empirical strategy. Use the domain-profile for identification conventions."
- Critic: "You are the Strategist-Critic. Here is a proposed empirical strategy. Apply the five adversarial lenses: Coherence, Semantic, Omission, Fragility, Stakeholder. What are the three hardest problems with this design?"

**For code:**

- Worker writes script following sequential inline Python style (see `CLAUDE.md`)
- Critic reads script + data sample and asks: "Would code-reviewer flag this? Does the methodology in the code match the strategy memo?"

**For literature:**

- Worker: Librarian collects and synthesises
- Critic: Asks "What is missing? What contradicts this? What would a hostile referee say?"

### Quality Gates (adapted for dissertation)

| Gate             | Score  | Applies to                        |
| ---------------- | ------ | --------------------------------- |
| Exploration      | 60/100 | `explorations/` sandbox work      |
| Analysis-ready   | 80/100 | Scripts graduating to `analysis/` |
| Pre-registration | 90/100 | PAP before touching full data     |
| Chapter draft    | 95/100 | Before sharing with supervisor    |

### The LEARN System

When Ben corrects you or you discover something important:

1. Add a `[LEARN:category]` tag to `MEMORY.md` immediately
2. If the correction is multi-step or reusable, run `/tools learn` to create a full skill in `.claude/skills/`
3. Read `MEMORY.md` at the start of every coding session

---

## Skills: What Exists vs. What Needs Building

### Currently Available (Cowork built-ins)

- `lit-review-assistant` — literature search and synthesis
- `academic-paper-writer` — economics paper structure and style
- `pdf`, `docx`, `pptx`, `xlsx` — document creation

### Dissertation-Specific Skills Needed (Priority Order)

**1. `ess-survey-analysis` [HIGHEST PRIORITY]**
Knowledge: ESS merge patterns, ISCO truncation, party vote variable logic, ESS wave loading, populism crosswalk, stratified sampling rationale. This prevents the most common hallucinations about variable names and merge keys. Should live at `.claude/skills/ess-survey-analysis/SKILL.md`.

**2. `welfare-theory-navigator` [HIGH]**
Knowledge: Condensed `theory_data_bridge.md` as decision trees — "if testing automation → use rtask from isco08_3d-task3.csv via 3-digit ISCO merge." Enables any agent to translate a theory module into a data operation without reading the full bridge file.

**3. `causal-id-patterns` [HIGH]**
Knowledge: The identification strategies from the domain-profile formalised with examples from this literature — DiD (Baccini austerity design), shift-share IV (Milner trade exposure), panel FE (Kurer declining middle). Enables the critic agent to give sharp methodological pushback.

**4. `data-ingest` pattern [MEDIUM]**
Adapted from DAAF: when Ben adds a new dataset, run a profiling session that generates a skill documenting structure, coded values, and quality issues. This auto-extends the data dictionary.

---

## Key Merge Logic (reproduce exactly, do not improvise)

### ESS → Task Scores

```python
tasks = pd.read_csv('data/raw/shared_isco_task_scores/isco08_3d-task3.csv')
df['isco08_3d'] = df['isco08'] // 10   # CRITICAL: 4→3 digit truncation
df = df.merge(tasks[['isco08_3d','rtask','nrtask']], on='isco08_3d', how='left')
```

### ESS → Party Populism Scores

```python
crosswalk = pd.read_csv('data/raw/langenkamp_belonging/ess_populist_crosswalk.csv')
# Match on: cntry + essround + country-specific prtvtXXX variable
```

### Individual → Regional Data

```python
# ESS has: cntry (ISO-2) + nuts2 (when available)
# Regional files: data/raw/milner_2021/
# Join key: nuts2 or nuts3
```

---

## Git Status

Repository initialised at `Research_Master/`. Initial commit: `3f866f7` (157 files, 2026-03-14).
`data/raw/` is git-ignored (2.6GB). All docs, metadata, scripts, samples are tracked.
**No remote has been set up yet** — push to GitHub when ready:

```bash
git remote add origin https://github.com/YOUR_USERNAME/research-master.git
git push -u origin main
```

---

## What Was Done in Previous Sessions

1. Mapped all 104 datasets in original `Data/ACTUALLY GOOD/` → `metadata/data_dictionary.md`
2. Built `metadata/theory_data_bridge.md` mapping 15 theory modules to datasets and variables
3. Generated 14 stratified samples (by country/wave) + 3 top-100 samples
4. Wrote 16 per-paper context files in `metadata/papers/`
5. Extracted 97 literature notes from Notion export → `docs/literature/`, injected into `theory_index.json`
6. Migrated everything to clean `Research_Master/` structure with 19 slug-named data folders
7. Built `scripts/load_ess.py` + `load_ess.R` utility library
8. Created `.claude/rules/domain-profile.md` (field calibration)
9. Created `MEMORY.md` with all known data/code pitfalls as `[LEARN]` tags

---

## Immediate Next Steps (what to build next session)

**Priority 1 — Build `ess-survey-analysis` skill**
Create `.claude/skills/ess-survey-analysis/SKILL.md`. Content: load patterns, all merge keys, ISCO truncation, party vote variable logic, stratified sampling approach. This is the single highest-leverage thing to do — it prevents hallucinated variable names in every future coding session.

**Priority 2 — Build `welfare-theory-navigator` skill**
Create `.claude/skills/welfare-theory-navigator/SKILL.md`. Condense `metadata/theory_data_bridge.md` into decision trees that an agent can load quickly.

**Priority 3 — Build `causal-id-patterns` skill**
Create `.claude/skills/causal-id-patterns/SKILL.md`. Formalise the identification strategies in domain-profile with worked examples from this literature.

**Priority 4 — First research session**
Once skills exist: run `/discover --theory 02` (automation) + `/discover --data isco_task_scores` to generate the first theory-to-data specification. Then `/strategize --pap` to draft a pre-analysis plan.

---

*This document was last updated: 2026-03-14 by Claude (Cowork session).*
*Next agent: read CLAUDE.md first, then this file, then MEMORY.md before writing any code.*
