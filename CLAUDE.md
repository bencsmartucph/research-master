# 🧠 CLAUDE.md — Session Primer

> **Read this file at the start of every session before touching any data or writing any code.**

---

## Researcher

**Ben Smart** (`bencsmart@gmail.com`) — PhD, political economy / comparative politics.

**Dissertation focus:** How economic disruption (automation, trade, austerity, occupational decline) shapes political preferences — specifically populist and radical right support — and what welfare state design can do about it.

**Stage:** Early ideation. Building theoretical framework and data infrastructure before committing to an empirical chapter.

**Code stack:** Python (.py) and R (.R / .Rmd). Data files are mostly .dta — load with `pyreadstat` (Python) or `haven` (R).

---

## Repository Map

```
Research_Master/               ← ROOT
│
├── CLAUDE.md                  ← YOU ARE HERE — read first
├── README.md                  ← Human overview
├── .gitignore                 ← data/raw/ excluded from git
│
├── docs/
│   ├── theory/                ← 15 theory module .md files + theory_index.json
│   └── literature/            ← 97 paper notes (cleaned slugs)
│
├── metadata/
│   ├── data_dictionary.md     ← Schema + samples for all 104 unique datasets
│   ├── theory_data_bridge.md  ← ⭐ Theory modules → datasets → variables
│   └── papers/                ← Per-paper context (research design + variables)
│       └── INDEX.md
│
├── data/
│   ├── raw/                   ← Replication data (19 study folders, clean slugs)
│   │   ├── gingrich_2019/
│   │   ├── kurer_2020_declining_middle/
│   │   ├── kurer_2022_disappointed_expectations/
│   │   ├── baccini_2024/
│   │   ├── im_2021/
│   │   ├── milner_2021/
│   │   ├── gugushvili_2025/
│   │   ├── aspiration_apprehension/
│   │   ├── euroscepticism_stagnation/
│   │   ├── silva_wellbeing/
│   │   ├── steiner_left_behind/
│   │   ├── langenkamp_2022/
│   │   ├── cicollini_2025/
│   │   ├── broz_2019/
│   │   ├── armaly_us/
│   │   ├── siwe_2017/
│   │   ├── how_not_authoritarian_populism/
│   │   ├── status_decline_working_class/
│   │   ├── shared_isco_task_scores/
│   │   └── MANIFEST.json      ← File counts + sizes per folder
│   └── samples/
│       ├── top100/            ← 100-row samples (top-N, 3 largest datasets)
│       └── stratified/        ← 200-row stratified samples (by cntry/wave)
│
├── scripts/
│   ├── load_ess.py            ← Load ESS waves + attach RTI scores (Python)
│   ├── load_ess.R             ← Same for R
│   └── make_stratified_samples.py
│
├── analysis/                  ← Your R/Python analysis scripts go here
└── outputs/
    ├── figures/               ← Plots and visualisations
    └── tables/                ← Regression tables, summary stats
```

---

## The Three Knowledge Systems

Use these together. Start with the bridge.

| System | Location | Purpose |
|--------|----------|---------|
| **Theory KB** | `docs/theory/` (15 .md files) | Full prose: mechanisms, key authors, empirical evidence, quotes |
| **Theory Index** | `docs/theory/theory_index.json` | Machine-readable: module metadata + **97 literature notes linked** |
| **Literature** | `docs/literature/` (97 .md files) | Paper notes: detailed summaries, methods, key findings |
| **Data Dictionary** | `metadata/data_dictionary.md` | Column names, types, missingness, 5-row samples for all datasets |
| **Theory–Data Bridge** | `metadata/theory_data_bridge.md` | Maps each theory module → datasets → variable names |
| **Paper Contexts** | `metadata/papers/` | Per-study: research question, ID strategy, analysis-ready files |

**Standard session workflow:**
1. Read this file
2. Identify relevant theory module(s) from the Quick Reference below
3. Open `metadata/theory_data_bridge.md` → find datasets + variables for that module
4. Check exact column names in `metadata/data_dictionary.md`
5. Load from `data/samples/` for development; switch to `data/raw/` when ready
6. Use `scripts/load_ess.py` or `scripts/load_ess.R` for common operations

---

## Theory Module Quick Reference

**I. Vulnerability Foundations**
- `01` Embedded Liberalism — trade + welfare compensation failing
- `02` Automation — RTI/routineness → anticipated status decline → radical right
- `03` Globalisation & Trade — China shock, regional decline, place-based politics
- `04` Precarity & Skill Specificity — skill transferability, multidimensional precarity

**II. Institutions & Mechanisms**
- `05` Policy Feedback — self-reinforcing / self-undermining welfare loops
- `06` ALMPs — enabling vs. punitive active labour market policies
- `07` Welfare Design & Legitimacy — procedural fairness, CARIN deservingness

**III. Psychological & Social**
- `08` Status & Recognition — zero-sum status, recognition > redistribution
- `09` Ontological Security — existential anxiety, fantasy narratives
- `10` Moral Economy — CARIN framework, producerism, welfare chauvinism

**IV. Solutions & Synthesis**
- `11` Social Investment — capabilities, predistribution, dignity
- `12` Populism & Mobilization — status remedies, in/out-group construction
- `13` Dual Pathway Synthesis — the trilemma
- `14` Mechanisms Catalog — comprehensive cross-cutting list

**V. Cognitive & Political Frames**
- `15` Cognitive Frames — misattribution, identity switching, meritocracy

---

## Key Data Relationships

### ESS → occupation task scores (automation exposure)
```python
import pyreadstat, pandas as pd
df, _ = pyreadstat.read_dta('data/raw/gugushvili_2025/ESS1e06_7 (1)/ESS1e06_7.dta')
tasks = pd.read_csv('data/raw/shared_isco_task_scores/isco08_3d-task3.csv')
df['isco08_3d'] = df['isco08'].astype(int) // 10
df = df.merge(tasks, on='isco08_3d', how='left')
```

### ESS → populist party classification
```python
crosswalk = pd.read_csv('data/raw/langenkamp_2022/ess_populist_crosswalk.csv')
# merge on: cntry + essround + country-specific party vote code
```

### ESS individual → positional income (status)
```python
df, _ = pyreadstat.read_dta('data/raw/cicollini_2025/essprt-all.dta')
# posit_income_change is pre-constructed — do not recompute from scratch
```

### ESS individual → regional economic data
```python
regional, _ = pyreadstat.read_dta('data/raw/milner_2021/data/imputed/imputed_econdata_voteshare_merged.dta')
# join key: nuts2 + year (or country + election year)
```

---

## Variable Quick Reference

| Concept | Variable | Dataset |
|---------|----------|---------|
| Country (ISO-2) | `cntry` | All ESS |
| ESS round | `essround` | All ESS |
| ISCO-08 occupation | `isco08` | ESS |
| Routine task intensity | `rtask`, `nrtask` | shared_isco_task_scores/isco08_3d-task3.csv |
| Left-right self-placement | `lrscale` | ESS |
| Vote (country-specific) | `prtvt[XX]` | ESS |
| Trust in parliament | `trstprl` | ESS |
| Household income | `hinctnta` | ESS |
| Immigration attitude | `imwbcnt`, `imueclt` | ESS |
| Life satisfaction | `stflife` | ESS |
| Positional income change | `posit_income_change` | cicollini_2025/essprt-all.dta |
| Austerity measure | `austerity_*` | baccini_2024/Raw Data/ |
| Far-right vote share | `FarRight`, `ER_voteshare` | milner_2021/, CLEA |
| Party populism score | `populism`, `gps_*` | baccini_2024/Raw Data/Global_Party_Survey |
| NUTS region | `nuts2`, `nuts3` | milner_2021/data/ardeco/, baccini_2024/ |

---

## Common Pitfalls

1. **ISSP ZA-files have numeric codes** — always load `meta.variable_value_labels` before recoding
2. **ESS vote variables are country-specific** — `prtvtXX` where XX = ISO-2 code. Use `ess_populist_crosswalk.csv` to harmonise
3. **ESS ISCO codes need truncation** — 4-digit in ESS, 3-digit in task file: `df['isco08'] // 10`
4. **Euroscepticism .dta and .csv are the same data** — use the .dta
5. **Baccini analysis-ready files** — use `baccini_2024/Data/individualdata.dta` and `districtdata.dta`, not the raw components
6. **`posit_income_change` is pre-constructed** in Cicollini's `essprt-all.dta` — don't rebuild from ESS income variables

---

## Refresh Commands

```bash
# Regenerate data dictionary (run from Research_Master/)
python scripts/make_stratified_samples.py

# Re-run literature scan (if new notes added)
# python ../migrate_literature.py  (or adapt the script)
```

---

*Update this file when research direction changes, new data is added, or variable quirks are discovered.*
