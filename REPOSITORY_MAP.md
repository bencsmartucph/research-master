# Research_Master Repository Structure — Detailed Edition

**Last updated:** May 4, 2026 | **Status:** Active research project  
**Data volume:** 2.6 GB unique data (104 datasets, 37K-line data dictionary)  
**Analysis coverage:** 20 study folders, 97 lit notes, 15 theory modules

---

## Quick Navigation by Task

| I need to... | Go to | What you'll find |
|--|--|--|
| **Find a variable** | `metadata/data_dictionary.md` (37K lines) | Full column schema + 5-row sample for each of 104 datasets |
| **Link theory to data** | `metadata/theory_data_bridge.md` | Which theory module uses which dataset & variables |
| **Check occupational exposure** | `data/raw/shared_isco_task_scores/` | ISCO-08 3-digit → task intensity mapping |
| **Load ESS data** | `scripts/load_ess.py` or `.R` | Auto-handles encoding, merges all available ESS waves |
| **Run the main analysis** | `analysis/final_analysis_pipeline.py` | Full pipeline: load → merge → models → tables → JSON |
| **See results tables** | `outputs/tables/*.csv` | Summary stats, main results, robustness, jackknife diagnostics |
| **View publication figures** | `outputs/figures/*.pdf` | 20+ publication-ready plots (both PDF + PNG) |
| **Check data diagnostics** | `analysis/review_diagnostics/` | Missing data, influence, functional form, VIF checks |
| **Find a specific paper** | `docs/literature/` (97 notes) | Standardized YYYY_author_slug.md format, cross-linked |
| **Read about a theory concept** | `docs/theory/` (15 modules) | 8-16K word modules + searchable JSON index |

---

## Root Level

```
Research_Master/
│
├── CLAUDE.md                    Session primer & global instructions (6.8 KB)
├── MEMORY.md                    Persistent learnings ([LEARN] tagged, 10.4 KB)
├── README.md                    Human-readable project overview (7.7 KB)
├── REPOSITORY_MAP.md            This file — detailed directory structure
│
└── Yiwen.pdf                    External archived document
```

---

## 📊 `data/` — Raw Datasets & Processed Samples

### Structure Overview
```
data/
├── raw/                         19 study folders, ~2.6 GB unique data
│   ├── [Study folders detailed below]
│
├── samples/                     Diagnostic and analytical samples
│   ├── [top-100 diagnostic samples]
│   ├── stratified/              [Weighted stratified samples by country-wave]
│   └── README.md                Sample documentation
```

---

### `data/raw/` — All 20 Study Folders (Detailed)

#### ESS (European Social Survey) — Cross-National Individual-Level Data
Individual political attitudes, demographics, employment across 15+ waves (2002–present). **Unit:** Individual. **Sample:** 30K–50K per wave.

```
ESS_csv/                         CSV versions of ESS waves 1–9 (all languages)
├── ESS1e06_7/  ESS2e03_6/  ESS3e03_7/  ... ESS9e03_2/
│   └── ESS{N}e{version}_{release}.csv    (~30–70 MB each)
└── [Contains: demographics, politics, attitudes, employment, trust]
```

**Key variables in ESS data:**
- `age`, `gndr`, `eduyrs` — demographics
- `isco08` — 4-digit occupation code (must truncate to 3-digit for task merge)
- `rlgdgr` — religiosity
- `trstprl`, `trstgen`, `stfgov` — institutional trust
- `imwbcnt`, `imuecnt`, `imbleco` — immigration attitudes (anti-immigration index)
- `gincdif` — support for redistribution (reverse-coded to `redist_support`)
- `vote` / vote choice variables — party voted for

**Analysis-ready merged ESS files:**
```
gugushvili_2025/                ESS subset with task scores pre-merged
├── ESS1e06_7/
├── ESS2e03_6 (1)/
├── ESS3e03_7/
├── ESS4e04_6/
├── ESS5e03_5/
└── [Contains: individual data + occupation task intensity]
```

#### Occupation Task Scores — ISCO-08 Occupational Characteristics
Maps 3-digit ISCO-08 occupation codes to routine task intensity (RTI), skills, and automation risk.

```
shared_isco_task_scores/        Task intensity by occupation
├── isco08_3d-task3.csv         ⭐ Core mapping: 3-digit ISCO → task intensity
│                                   Cols: isco08_3d, task, rtask, nrtask
│
├── D1.1_Survey on Automation Risk_v2.0*.dta
│                                Survey on automation exposure (reference data)
└── MANIFEST.TXT                 Data provenance
```

**Critical note:** Variable is `task` (NOT `rtask` or `nrtask`). To merge:
```python
df['isco08_3d'] = df['isco08'].astype(int) // 10  # Truncate 4-digit → 3-digit
df = df.merge(tasks, on='isco08_3d', how='left')
```

#### Welfare State Data — Policy Context & Country-Level Moderators
Comparative welfare spending, generosity indices, and institutional features.

```
CWED/                           Comparative Welfare Entitlements Dataset
├── [CWED raw files — generosity indices by country-year]
└── [Used as country-level moderator: cwed_generosity (mean 2005–2011)]

baccini_2024/Replication V3/Data/
├── Raw Data/
│   ├── Baciini - ESSdata.dta   (598 MB) ⭐ ESS + austerity + CPDS merged
│   ├── CPDS_Aug_2020.dta       Country-year panel: welfare, tax, ALMP spending
│   └── Austerity measures by country-year
│
└── [15 countries, ESS waves 6–9, district-level variation in austerity]
```

**Key variables in Baccini data:**
- `cwed_generosity` — Welfare state generosity index (institutional moderator)
- `austerity_cuts` — District-level austerity magnitude
- All original ESS variables (demographics, attitudes, vote choice)

#### Trade & Economic Geography — Regional Economic Exposure
Regional-level trade exposure, GDP, unemployment, and far-right vote share for spatial analysis.

```
milner_2021/                    Trade exposure + regional economic data
├── data/data/
│   ├── oecd_trade/
│   │   ├── oecd_chinese_trade.dta        China import penetration by sector
│   │   ├── oecd_lowwage_trade.dta        Low-wage country imports
│   │   ├── oecd_world_trade.dta          Overall trade openness
│   │   └── FRED_deflator_2020.csv        Price deflators (real terms conversion)
│   │
│   ├── ardeco/
│   │   └── regional_gdp_by_year.dta      Regional GDP per capita (NUTS2)
│   │
│   ├── wdi/
│   │   ├── var_labels_complete.xlsx      World Bank indicators + labels
│   │   └── wdi_labels.do                 Stata codebook
│   │
│   ├── parties_votes/
│   │   ├── CLEA_voteshare_turnout.dta    Far-right vote share by region-year
│   │   └── party_classifications.dta     Party ideology classification
│   │
│   └── imputed/
│       └── imputed_econdata_voteshare_merged.dta  ⭐ **Analysis-ready merged**
│           (57 MB) Combines trade, regional GDP, vote shares, demographics
│
└── [NUTS2 regions, 15 countries, 2002–2020]
```

#### Panel Survey Data — Status Decline & Personality Change
Individual-level panel data tracking employment transitions, occupational change, and political attitudes over time.

```
kurer_2020_declining_middle/    Status decline in panel data (SOEP, BHPS, SHP)
├── replication_files/replication_files/
│   ├── 0_1_create_SHP.do       Build SHP panel (Swiss Household Panel)
│   ├── 0_2_create_BHPS.do      Build BHPS panel (British Household Panel)
│   ├── 0_3_create_SOEP.do      Build SOEP panel (German Socio-Economic Panel)
│   ├── 1_pooled_panels.R       Combine panels + create variables
│   ├── 3_SHP-analysis.R        Swiss analysis
│   ├── 4_BHPS-analysis.R       British analysis
│   ├── 5_SOEP-analysis.R       German analysis
│   ├── 7_FE-analysis_Stata.do  Fixed-effects models (all panels)
│   └── Readme.pdf              Data & codebook
│
└── [Kurer's replication package: status anxiety mechanisms]
```

#### Positional Income & Status Decline — ESS + Individual Wealth Rank
Combines ESS with estimated positional income (income rank within country-age cohort).

```
cicollini_2025/                 "Left Behind Whom?" — Positional income analysis
├── essprt-all.dta              ⭐ (2.0 MB) ESS waves 1–9 + positional income
│                                  Cols: all ESS variables + posit_income_change
│
├── election_year_data.dta      Election timing for causal inference
├── Ciccolini_LeftBehindWhom.do Stata code (replication)
├── partyfacts-core.csv         Party nomenclature mapping (8.7 MB)
├── partyfacts-mapping.csv      Full party-year mapping (1.5 MB)
└── Readme.docx                 Data documentation
```

**Critical data:** `essprt-all.dta` is pre-built; don't reconstruct `posit_income_change`.

#### Automation Perceptions & Risk — ISSP/ZA Survey Series
Individual attitudes toward automation, robots, job security, and economic anxiety across multiple waves.

```
gingrich_2019/                  ISSP Work Orientation Module (2005, 2010, 2015, 2016)
├── ZA4950_v2-3-0.dta           ISSP 2009 Work Orientation (39.9 MB)
├── ZA5400_v4-0-0.dta           ISSP 2010 Work Orientation (42.4 MB)
├── ZA5500_v3-0-0.dta           ISSP 2010 Work Orientation alt (34.5 MB)
├── ZA5800_v3-0-0.dta           ISSP 2010 Role of Government (38.4 MB)
├── ZA5950_v2-0-0.dta           ISSP 2012 Work Orientation (34.1 MB)
├── ZA6670_v2-0-0.dta           ISSP 2015 Role of Government (38.2 MB)
├── ZA6770_v2-1-0.dta           ISSP 2016 Work Orientation (43.4 MB)
└── [All in Stata format; ~20K obs per wave]
```

**Key variables:** Automation risk perceptions, job security concerns, income support preferences, government role attitudes.

#### Euroscepticism & Economic Stagnation — Cross-National Survey
ESS-based data examining the link between economic stagnation and EU skepticism across regions.

```
euroscepticism_stagnation/      Regional stagnation + EU attitudes
├── Euroscepticism as a syndrome of stagnation.csv     (135 MB)
├── Euroscepticism as a syndrome of stagnation - Data for replication-1.dta  (90 MB)
└── [Region-year: unemployment, growth, EU support]
```

#### Radical Right Vote Choice & Party Identification — ESS + Classification
Individual vote choice for radical right parties, coded using expert survey data.

```
im_2021/                        "A Reservoir of Votes for the Radical Right"
├── Im - A Reservoir of Votes for the Radical Right - ESS.csv  (401.6 MB)
│   └── Contains: ESS + radical right vote classification (Chapel Hill Expert Survey)
│
langenkamp_2022/                ESS-Populist Party Crosswalk
├── ess_populist_crosswalk.csv  ESS party vote → populist classification
│   └── **CRITICAL:** Semicolon-delimited (`,` NOT `;` as delimiter fails)
│
└── [Gingrich + Im + Langenkamp together form party classification consensus]
```

#### Populism, Attitudes & Radicalism — Additional Attitude Surveys
Specialized surveys on populist attitudes, authoritarianism, and anti-system views.

```
aspiration_apprehension/        "Aspirations and Apprehension" survey data
├── [Individual attitudes toward future, security, mobility]
│
how_not_authoritarian_populism/ ESS subset with populism coding
├── ess_variable_coding.xlsx    Populism construct coding
├── prep_ess1_7.Rmd             ESS waves 1–7 preparation
├── prep_ess9.Rmd               ESS wave 9 preparation
├── replication_figures_tables.Rmd
└── [Used for populism outcome validation]

status_decline_working_class/   "The Death of the Working Class"
├── [Regional-level working-class decline indicators]
│
steiner_left_behind/            "Left Behind in the Brexit Debate"
├── ZA7700_*.dta                ISSP data for UK working-class analysis
└── [Survey on government role + economic attitudes]
```

#### Institutional & Welfare Legitimacy — Wellbeing & Trust
Survey data on trust in institutions, government satisfaction, and subjective wellbeing as mechanisms.

```
silva_wellbeing/                "Welfare and Wellbeing in Europe"
├── graphsdata.dta              Life satisfaction, wellbeing by country-year
├── silva - populism_v3_V3.do   Stata analysis code
└── [Individual wellbeing + institutional satisfaction link]

siwe_2017/                      "Subjective In-Work Experience" survey
├── SIWE_betaMay2017.dta        Employment quality + subjective experience
└── SIWE Codebook.pdf
```

#### Additional Studies — Heterogeneous Research Materials
Specialized datasets for robustness and alternative specifications.

```
armaly_us/                      US-specific populism study
broz_2019/                      Trade politics + polarization
gugushvili_2025/                ⭐ ESS + task scores (see above)
```

---

### `data/samples/` — Diagnostic and Analytical Samples

**Purpose:** For testing pipelines, generating walkthroughs, and stratified analysis.

```
data/samples/
│
├── [Top-100 samples for diagnostics]
│   ├── baccini_ESSdata_sample100.csv        Top 100 obs from Baccini (38 cols)
│   ├── baccini_ESSdata_sample100.dta        Same, Stata format
│   ├── euroscepticism_stagnation_sample100.csv
│   ├── im_radical_right_ESS_sample100.csv
│   │
│   └── README.md                             Sample documentation
│
└── stratified/                              Stratified samples (weighted by country-wave)
    ├── ESS1e06_7_strat25.csv                ESS wave 1: 25 obs per country (strat)
    ├── ESS2e03_6_strat25.csv                ESS wave 2: 25 obs
    ├── ESS3e03_7_strat30.csv                ESS wave 3: 30 obs (larger sample)
    ├── ESS4e04_6_strat30.csv                ESS wave 4: 30 obs
    ├── ESS5e03_5_strat30.csv                ESS wave 5: 30 obs
    ├── ZA4950_ISSP2009_strat200.csv         ISSP 2009: 200 obs (larger ISSP)
    ├── ZA5400_ISSP2010_strat200.csv         ISSP 2010: 200 obs
    ├── ZA6770_ISSP2016_strat200.csv         ISSP 2016: 200 obs
    ├── ZA7700_steiner_strat200.csv          Steiner "Left Behind" data
    ├── baccini_district_level_strat75.csv   Austerity: 75 districts
    ├── baccini_individualdata_strat5.csv    ESS individual: 5 obs per country
    ├── cicollini_essprt_all_strat45.csv     Positional income: 45 obs per country
    ├── euroscepticism_dta_strat200.csv      Euroscepticism: 200 obs
    ├── milner_merged_regional_strat200.csv  Trade: 200 regions
    │
    └── README.md                             Stratified sample documentation
```

**How samples are created:**
```python
# From scripts/make_stratified_samples.py
df_strat = df.groupby('country_wave', group_keys=False).apply(
    lambda x: x.sample(n=min(strat_size, len(x)), random_state=42)
)
```

---

## 📋 `metadata/` — Data Schemas, Mappings & Documentation

### Structure Overview
```
metadata/
├── data_dictionary.md           Full schema for all 104 datasets (37K lines)
├── theory_data_bridge.md        Theory module → dataset → variable mapping
├── literature_map.md            Theory → Top 5 papers per module
└── papers/                      [Subdirectory for per-study notes]
```

---

### `metadata/data_dictionary.md` — Comprehensive Data Reference (37,199 lines)

**Auto-generated:** 2026-03-13 from `map_data.py`  
**Coverage:** 104 unique datasets (duplicates deduplicated) across 19 study folders

#### How to Use the Data Dictionary

**Find a variable by name:**
```bash
grep -n "imwbcnt\|gincdif\|isco08" metadata/data_dictionary.md
```

**Sections in the file:**
1. **Repository Overview** (top of file) — Total files, size, duplicate statistics
2. **File Index** (by size) — All 104 datasets ranked by file size
3. **Duplicate Files Detected** — 24 redundant copies identified
4. **Dataset Schemas & Samples** — For each dataset:
   - Column names and types
   - Stata variable labels (if applicable)
   - 5-row data sample
   - Min/max/missing statistics

#### Key Datasets in the Dictionary

| Dataset | Size | Rows/Cols | Key Variables | Line Range (approx) |
|---------|------|-----------|---------------|-----|
| `Baccini - ESSdata.dta` | 598 MB | ESS individual-level | demographics, occupation, attitudes, austerity | 1,000–2,500 |
| `Im - Radical Right ESS.csv` | 401 MB | ESS individual-level | vote choice, party identification, radical right flag | 2,500–3,500 |
| `Euroscepticism.csv` | 135 MB | Region-year | EU attitudes, economic stagnation | 3,500–4,500 |
| `Milner merged.dta` | 57 MB | Region-year | trade, GDP, vote share | 4,500–5,500 |
| `cicollini essprt-all.dta` | 2.0 MB | Individual-year | positional income, ESS attitude vars | 5,500–6,500 |
| `ISSP ZA4950.dta` | 39.9 MB | Individual-year | automation perceptions, job security | 6,500–7,500 |
| ISSP ZA series (5 more files) | 30–43 MB each | Individual-year | work orientation, government role | 7,500–12,000 |

**To find construct-variable mappings:** Use `theory_data_bridge.md` instead (it's indexed by theory concept).

---

### `metadata/theory_data_bridge.md` — Theory to Data Operationalization

**Purpose:** Jump from a theory module to the exact datasets and variables that measure its concepts.

**Structure:**
- **Navigation table** — 15 theory modules with their primary datasets
- **Per-module section** — Construct → Variable mapping
  - Which datasets operationalize each concept
  - Step-by-step variable construction
  - Sample merge code (Python/R)

#### Example: Module 01 (Embedded Liberalism)

```markdown
## 01: Embedded Liberalism & Economic Vulnerability

### Constructs & Variables
| Construct | Variable | Dataset | Notes |
|-----------|----------|---------|-------|
| Trade openness | chinese_import_share | oecd_chinese_trade.dta | China shock |
| Welfare generosity | cwed_generosity | CPDS_Aug_2020.dta | Mean 2005–2011 |
| Austerity magnitude | austerity_cuts | Baccini district-level | District-level variation |
```

#### All 15 Modules Cross-Referenced

1. **Embedded Liberalism** → Trade data (Milner) + welfare (CPDS)
2. **Automation** → Task scores (shared_isco) + ESS employment
3. **Globalization** → Regional trade + ARDECO GDP
4. **Precarity** → Task intensity + occupational heterogeneity
5. **Policy Feedback** → CPDS spending data + austerity shocks
6. **ALMPs** → CPDS ALMP spending + ELFS (labor force)
7. **Welfare Design** → ESS trust variables + institutional design
8. **Status** → Cicollini positional income + Gugushvili ESS
9. **Ontological Security** → Silva wellbeing + Steiner attitudes
10. **Moral Economy** → ESS immigration variables + ISSP deserving­ness
11. **Social Investment** → CPDS education spending + skills measures
12. **Populism** → Party classifications (CLEA, GPS, CHES) + vote choice
13. **Dual Pathway** → Baccini merged (individual + district) + Milner regional
14. **Mechanisms** → Cross-cutting (see individual modules)
15. **Cognitive Frames** → Cicollini attitudes + Aspiration/Apprehension survey

---

### `metadata/literature_map.md` — Theory to Literature Mapping

**Purpose:** For each theory module, which papers in your literature review are most important.

**Format:** Theory module → Top 5 papers (with DOI, brief summary, relevance note)

**Example entries:**
```markdown
## Module 01: Embedded Liberalism

1. Ruggie (1982, 1995) — Embedded liberalism as historical compromise
2. Baccini & Weymouth (2021) — Trade exposure + populism in ESS
3. Rodrik (2011) — Globalization trilemma: democracy, sovereignty, integration
4. Gingrich & Häusermann (2015) — Welfare politics in dual labor markets
5. Iversen & Soskice (2001) — Varieties of capitalism → welfare demand
```

**Use case:** When writing the literature review for a module, open the map, then grep your `docs/literature/` folder for the papers listed.

---

### `metadata/papers/` — Subdirectory for Per-Study Metadata

**Current status:** Directory exists but is empty (reserved for future expansion).

**Planned use:** One folder per major study (e.g., `baccini_2024/`, `milner_2021/`) containing:
- `README.md` — Study overview, key papers, data provenance
- `codebook.md` — Per-study variable documentation (more detailed than data_dictionary)
- `sample_code.R` or `.py` — Example merge/analysis code for the study
- `notes.md` — Implementation notes (data cleaning quirks, unit-of-analysis issues, etc.)

---

## 🔬 `analysis/` — Empirical Pipeline & Diagnostics

### Structure Overview
```
analysis/
├── final_analysis_pipeline.py          ⭐ Main pipeline: load → merge → models → output
├── final_analysis_report.md            Pipeline documentation
├── final_results.json                  Serialized regression results
│
├── [Model-specific scripts]
│   ├── random_slopes_models.py         Multilevel mixed-effects models
│   ├── run_sorting_mechanism.py        Occupational selection into automation exposure
│   └── sorting_mechanism_master_v2.csv Sorting mechanism results
│
├── [Diagnostic and exploratory scripts]
│   ├── _diagnose_cwed_correlation.py   Welfare generosity correlation checks
│   ├── ch01_selection_bias_interactive.py
│   ├── walkthrough_*.py                Step-by-step tutorial scripts (4 files)
│   ├── sorting_mechanism_exploration.ipynb
│   └── fix_plots_ab.py
│
├── [Documentation]
│   ├── codebook.md                     Variable definitions + transformations
│   ├── cwed_subcomponents_report.md    Welfare generosity decomposition
│   ├── econometric_review.md           Methods & assumptions justification
│   ├── overnight_report.md             Ad-hoc analysis summary
│   └── final_analysis_report.md        Full pipeline documentation
│
└── review_diagnostics/                 Model validation & sensitivity checks
    ├── cronbach_alpha_by_regime.csv    Internal consistency of scales
    ├── country_level_controls.csv      Control variables by country
    ├── cwed_*.csv                      CWED generosity diagnostics
    ├── cwed_influence_loo.csv          Leave-one-out influence (CWED)
    ├── cwed_cooks_distance.csv         Cook's distance (CWED outliers)
    ├── functional_form_diagnostics.png Linearity check plot
    ├── cwed_influence_diagnostics.png  Influence diagnostics plot
    ├── missingness_by_regime.csv       Missing data patterns by regime type
    ├── model2_verification.csv         Model 2 spec verification
    ├── part2_findings.json             Phase 2 results (JSON)
    ├── rti_distribution_*.csv/.png     RTI distribution by regime
    ├── se_comparison.csv               Standard error robustness (cluster vs panel)
    └── vif_results.csv                 Multicollinearity (VIF) checks
```

---

### `final_analysis_pipeline.py` — The Core Analysis Script

**Purpose:** Single authoritative source for all empirical results. Runs end-to-end: load → clean → merge → model → export.

**Main steps:**
1. **Load** — All 3 datasets (Baccini ESSdata, CWED country-level, ISCO task scores)
2. **Merge** — ESS individual × ISCO occupations × CWED country-year
3. **Construct** — Anti-immigration index (3 items), RTI standardized, welfare regime dummies
4. **Model** — Main specifications + robustness variants
5. **Export** — To `outputs/tables/` (CSV + JSON) and `outputs/figures/` (matplotlib)

**Output files it generates:**
- `outputs/tables/table1_summary_stats.csv` — Descriptive statistics
- `outputs/tables/table2_main_results.csv` — Main model estimates
- `outputs/tables/tableA1_robustness.csv` — Robustness variants
- `outputs/figures/fig1_*.pdf` — All publication figures
- `final_results.json` — Serialized model objects for downstream use

---

### Model-Specific Scripts

#### `random_slopes_models.py` — Multilevel Mixed-Effects
**Purpose:** Random slopes (by country, by regime) to test heterogeneity of automation effects.

**Outputs:**
- `outputs/tables/rs_results.csv` — Random slopes model estimates
- `outputs/tables/rs_jackknife.csv` — Jackknife uncertainty for random slopes
- `outputs/tables/rs_vs_ri_model3.csv` — Random slopes vs random intercept comparison
- `outputs/figures/fig6_cwed_country_slopes.pdf` — Country-specific slopes visualization

**Key model:**
```python
# Main specification
anti_immig ~ 1 + task_z * cwed_generosity + X + (1 + task_z | cntry)
# Plus regime interactions
... + (1 | welfare_regime)
```

#### `run_sorting_mechanism.py` — Occupational Selection
**Purpose:** Do individuals with populist attitudes sort into/out of automatable occupations?

**Tests:** Selection bias into treatment (RTI exposure).

**Outputs:**
- `sorting_mechanism_master_v2.csv` — Selection probabilities
- `outputs/figures/fig2_sorting_pattern.pdf` — Visual of sorting

#### Walkthrough & Tutorial Scripts
**Purpose:** Interactive, step-by-step pedagogical code for understanding the analysis.

- `walkthrough_interactive.py` — Full pipeline (condensed)
- `walkthrough_cluster_se_interactive.py` — Clustering logic explained
- `walkthrough_cross_level_interactive.py` — Cross-level interactions (RTI × CWED)
- `walkthrough_figures.py` — Figure generation with annotations

---

### Diagnostic Files (`review_diagnostics/`)

| File | What It Tests | Interpretation |
|------|---------------|-----------------|
| `vif_results.csv` | Multicollinearity (VIF < 5 is OK) | Check for collinearity between RTI, CWED |
| `cronbach_alpha_by_regime.csv` | Internal consistency of anti-immigration scale (α ≥ 0.7 is good) | Scale reliability by welfare regime |
| `model2_verification.csv` | Model 2 coefficient replication | Validate main findings stability |
| `rti_distribution_by_regime.png` | RTI kernel density by regime type | Visual: automation exposure heterogeneity |
| `functional_form_diagnostics.png` | Linearity + residual patterns | Check for nonlinearity, heteroskedasticity |
| `cwed_influence_loo.csv` | Leave-one-out influence on main effect | Countries driving welfare moderator |
| `cwed_cooks_distance.csv` | Cook's distance for outliers | Identifies influential welfare regimes |
| `missingness_by_regime.csv` | % missing by welfare regime | Unequal data quality by country group |
| `se_comparison.csv` | Cluster vs panel SEs | Sensitivity of inference to clustering |
| `country_level_controls.csv` | Country-level control variables | GDP, unemployment, trade openness |

**How to use diagnostics:**
- **If VIF > 5:** Check correlation structure between RTI and CWED
- **If α < 0.7 in some regimes:** Consider regime-specific anti-immigration scaling
- **If CooksD is large for 1 country:** Rerun excluding that country (jackknife available)
- **If functional form plot shows curvature:** Consider spline or polynomial RTI term

---

### Documentation Files

| File | Purpose |
|------|---------|
| `codebook.md` | Variable definitions + transformation formulas |
| `econometric_review.md` | Methods choices + robustness discussion |
| `final_analysis_report.md` | Full pipeline explanation (what each section does) |
| `cwed_subcomponents_report.md` | Welfare generosity decomposed into: universalism, generosity level, duration |
| `overnight_report.md` | Ad-hoc overnight analysis (used to resolve specific issues) |

---

## 📊 `outputs/` — Publication-Ready Figures, Tables & Exports

### Structure Overview
```
outputs/
├── figures/                     20+ publication-ready PDF + PNG pairs
│   ├── [Main figures fig1–fig7]
│   ├── [Additional diagnostic figures]
│   └── walkthrough/             Didactic step-by-step visualizations
│
├── tables/                      Results tables (CSV + JSON)
│   ├── [Main results tables]
│   ├── [Robustness tables]
│   ├── [Jackknife diagnostics]
│   └── [Per-country heterogeneity]
│
└── anki/                        Learning exports
    └── learning_econometrics.tsv   Spaced repetition flashcards
```

---

### `outputs/figures/` — Detailed Figure Guide

**Convention:** All figures exported as both PDF (publication) and PNG (screen/web).

#### Main Results Figures

| Figure | File | What It Shows | Used In | Code |
|--------|------|---------------|---------|------|
| **Fig 1** | `fig1_rti_antiimmig_by_cwed.pdf` | Scatter: RTI (x) vs Anti-immigration (y), colored by CWED generosity | Paper intro / motivation | `final_analysis_pipeline.py` |
| **Fig 2a** | `fig2_rti_vs_antiimmig_by_regime.pdf` | Regime-specific slopes: Does automation effect differ by welfare type? | Results section | Main pipeline |
| **Fig 2b** | `fig2_sorting_pattern.pdf` | Selection: Do populists avoid automatable jobs? Propensity score balance | Appendix / mechanisms | `run_sorting_mechanism.py` |
| **Fig 3** | `fig3_marginal_effects.pdf` | Marginal effect of RTI on anti-immigration across range of CWED (95% CI bands) | Main specification (moderator test) | Main pipeline |
| **Fig 4a** | `fig4_education_moderator.pdf` | Education heterogeneity: Does education dampen automation effect? | Robustness / heterogeneity | Main pipeline |
| **Fig 4b** | `fig4_rti_vs_redistribution_by_regime.pdf` | Alternate outcome: RTI on redistribution support (vs anti-immigration) | Appendix / mechanism validity | Main pipeline |
| **Fig 5** | `fig5_robustness.pdf` | Coef plot: Main effect across 6 model specs (specification robustness) | Appendix | Main pipeline |
| **Fig 6a** | `fig6_cwed_country_slopes.pdf` | Random slopes: Country-specific RTI effects (conditional on welfare regime) | Appendix / heterogeneity | `random_slopes_models.py` |
| **Fig 6b** | `fig6_cwed_vs_slopes.pdf` | Meta-regression: Country RTI slope (y) vs CWED generosity (x) | Main story: welfare moderates effect | Main pipeline |
| **Fig 7** | `fig7_cwed_subcomponents.pdf` | CWED decomposed: Which welfare components matter most? (universalism vs benefit level) | Appendix / mechanism | `scripts/cwed_subcomponents_analysis.py` |

#### Supporting Diagnostic Figures

| Figure | File | What It Shows | Purpose |
|--------|------|---------------|---------|
| — | `dv_correlation_matrix.pdf` | Correlation between anti-immigration, redistribution, EU skepticism | Check outcome construct validity |
| — | `rti_distribution.pdf` | Kernel density of RTI by country | Visual: automation exposure heterogeneity |
| — | `rti_by_education_regime.pdf` | RTI distribution: education × welfare regime (3×3 matrix) | Stratification check |
| — | `welfare_vs_rti_slopes.pdf` | Scatter: Country-level CWED (x) vs country RTI slope (y) | Context for Fig 6b |
| — | `within_regime_country_variation.pdf` | Boxplot: RTI by country, faceted by welfare regime | Shows within-regime variation |
| — | `fig_regime_heterogeneity.pdf` | Interaction effect: RTI × Regime, with 95% CIs | Regime comparison snapshot |

#### Walkthrough Figures

| Folder | Purpose |
|--------|---------|
| `walkthrough/` | Step-by-step visual tutorials for methods (clustering, cross-level interactions, etc.) |

---

### `outputs/tables/` — Results Tables (CSV Format)

**All tables exported as `.csv` (readable in Excel, Python, R) + summary as `.json` (structured metadata).**

#### Main Results Tables

| Table | File | Contents | Rows/Cols |
|-------|------|----------|-----------|
| **Table 1** | `table1_summary_stats.csv` | Descriptive statistics: N, mean, SD, min, max by welfare regime | 25 variables × 5 regimes |
| **Table 2** | `table2_main_results.csv` | Main model estimates: coef, SE, t-stat, p-val for all specifications | 8 specs × 6 predictors |
| **Table 2 (JSON)** | `table2_main_results.json` | Same as CSV, but structured JSON (model objects, metadata) | Serialized Python models |
| **Table A1** | `tableA1_robustness.csv` | Robustness checks: alternative specs, subsamples, exclusions | 6 specs × 6 predictors |

#### Heterogeneity & Mechanism Tables

| Table | File | Contents | Rows/Cols |
|-------|------|----------|-----------|
| — | `per_country_slopes.csv` | Country-specific RTI slopes (random slopes estimates) | 15 countries × 4 columns |
| — | `country_slopes.csv` | Country slopes with 95% CIs | 15 countries × 3 columns |
| — | `rs_results.csv` | Random slopes model summary (variance components, correlations) | Model diagnostics |
| — | `rs_vs_ri_model3.csv` | Random slopes vs random intercept comparison (both specs side-by-side) | Model comparison |

#### Diagnostic & Jackknife Tables

| Table | File | Contents | Purpose |
|-------|------|----------|---------|
| — | `jackknife_details.csv` | Leave-one-out coef when each country excluded | Influence diagnostics |
| — | `jackknife_single_country.csv` | Single-country jackknife errors | Confidence in country effect |
| — | `jackknife_two_country.csv` | Pairwise country jackknife | Robustness to regional clusters |
| — | `summary_stats.csv` | Summary statistics by group | Descriptive baseline |

#### Sorting Mechanism Tables

| Table | File | Contents |
|-------|------|----------|
| — | `sorting_mechanism_master.csv` | Full sorting mechanism results (old version) |
| — | `sorting_mechanism_master_v2.csv` | Updated sorting analysis (selection bias test) |

---

### `outputs/anki/` — Learning Exports

**Purpose:** Spaced repetition study decks for econometric concepts.

| File | Contents | Use Case |
|------|----------|----------|
| `learning_econometrics.tsv` | Flashcard deck: CWED concepts, RTI measurement, identification assumptions, test statistics | Self-study / review |

**Format:** Tab-separated values (TSV):
```
Question | Answer
What is CWED generosity? | Comparative Welfare Entitlements Dataset index: average benefit duration + replacement rates (2005–2011)
How do you merge task scores to ESS? | Truncate ISCO to 3-digit: isco08 // 10, then merge on isco08_3d
What's the exclusion restriction for RTI IV? | Occupational routine task intensity (determined by tech adoption, not country policies)
```

---

## 📚 `docs/` — Theory, Literature & Essays

### `docs/theory/` — 15 Core Theory Modules

**Location:** `docs/theory/`  
**Count:** 15 modules × 8–16 KB each = 115+ KB total  
**Format:** Markdown (greppable, version-controlled)  
**Index:** `docs/theory/theory_index.json` (full-text searchable)

#### All 15 Modules (with core construct)

| # | Module | Construct | Lines |
|---|--------|-----------|-------|
| 01 | Embedded Liberalism & Economic Vulnerability | Trade-welfare bargain → populism when compensation fails | ~300 |
| 02 | Automation & Technological Change | Routine task shifts → occupational decline → anxiety | ~320 |
| 03 | Globalization, Trade & Spatial Dimensions | Regional trade exposure → unequal economic shocks | ~280 |
| 04 | Precarity & Skill Specificity | Occupation-specific skills → worker vulnerability in transitions | ~220 |
| 05 | Policy Feedback & Welfare Institutions | Welfare design → expectations → resentment when cut | ~360 |
| 06 | Active Labour Market Policies (ALMPs) | Training + job search support → skill updating or déclassement | ~310 |
| 07 | Welfare Design, Trust & Legitimacy | Institutional design → citizen engagement and support | ~300 |
| 08 | Status, Recognition & Relative Position | Income rank within cohort → status anxiety → populism | ~340 |
| 09 | Ontological Security & Psychology | Security in life trajectory → response to disruption | ~360 |
| 10 | Moral Economy & Deservingness | Who "deserves" welfare? Conditional support + chauvinism | ~400 |
| 11 | Social Investment Paradigm | Human capital investment (education, training) as welfare alternative | ~350 |
| 12 | Populism & Right-Wing Mobilization | Thin ideology + supply-side party strategies + demand grievances | ~380 |
| 13 | Dual Pathway Synthesis: The Trilemma | Economic disruption → either status anxiety pathway OR redistributive resentment pathway | ~440 |
| 14 | Mechanisms Catalog | Systematic inventory of causal pathways and mediators | ~450 |
| 15 | Cognitive Frames & Belief Systems | How people interpret disruption (via frames: responsibility, deservingness, blame) | ~480 |

**To find a concept:** 
```bash
grep -r "status decline\|automation exposure\|welfare resentment" docs/theory/
```

**To see the searchable index:**
```bash
cat docs/theory/theory_index.json | jq '.[] | select(.module == "13")' # Show module 13 terms
```

---

### `docs/literature/` — 97 Annotated Literature Notes

**Location:** `docs/literature/`  
**Format:** `YYYY_author_shortitle.md` (standardized slugs for grepping)  
**Total:** ~200 KB of distilled lit knowledge

#### File Naming Convention
```
YYYY_author_shortslug.md
│     │      │
│     │      └─ Shortened title (kebab-case)
│     └───────── Author last name
└──────────────── Publication year
```

#### Example File Names
```
2021_baccini_trade_as_villain.md
2020_kurer_declining_middle.md
2019_oesch_rennwald_realignment.md
2024_garritzmann_häusermann_pinggera.md
```

#### Literature Note Structure
Each note contains:
- **Citation:** Full APA format
- **Core claim:** 1–2 sentence thesis
- **Methods:** Design, sample, identification
- **Key findings:** Effect sizes, heterogeneity
- **Theory relevance:** Which of the 15 modules this supports
- **Data sources:** Datasets used (if applicable)
- **Quotes:** 3–5 key passages (for voice + citation)
- **Tags:** `#automation`, `#trade`, `#welfare-design`, etc.

#### How to Navigate Literature
**By theory module:**
```bash
# Find papers relevant to automation (Module 02)
grep -l "automation\|task\|occupational change" docs/literature/*.md | head -10
```

**By theme:**
```bash
# Find papers on welfare resentment
grep -l "resentment\|deservingness\|chauvinism" docs/literature/*.md
```

**Complete index:** See `metadata/literature_map.md` for curated "Top 5 papers per theory module"

---

### `docs/archive/` — Superseded Documents

| File | Status | Reason |
|------|--------|--------|
| `four_prompts.md` | Archived | Old session prompts (replaced by live session structure) |

---

### `docs/learning_econometrics/` — Pedagogical Materials

**Purpose:** Self-study resources on econometric methods used in the project.

```
docs/learning_econometrics/
├── figures/                 Visual aids for econometric concepts
├── interactives/            Interactive code snippets / walkthroughs
└── [Concept markdown files]
```

---

## 🎯 `essays/` — Intellectual Context & Handover

### Structure
```
essays/
│
├── HANDOVER.md              ⭐ Current state: decisions, findings, next steps
│                             (Moved from root HANDOVER.md)
│
├── patient_tutor/           Long-form intellectual essays
│   ├── A Mind in Formation with part 6.md    Intellectual portrait (7K+)
│   ├── working_with_ben.md                   Collaboration guide for Claude
│   ├── Ben's Learning Workflow.txt           Epistemic methodology
│   ├── v_building_is_learning.md             Thesis philosophy section
│   ├── v_discovery_story.md                  Research narrative arc
│   ├── v_curious_confession.md               Personal reflection on method
│   ├── v_false_dichotomy.md                  Theoretical argument
│   └── VERSIONS_INDEX.md                     Version control for essays
│
└── compile_error/           Pedagogical pieces (work-in-progress)
```

---

## 🗣️ `talks/` — Presentations & Conference Materials

### Structure
```
talks/
│
└── 2026-05-04_seminar/      May 4, 2026 seminar presentation ("Dignity Is a Baseline")
    │
    ├── Dignity_Is_a_Baseline_2026-05-04_v2.pptx   PowerPoint export (final)
    ├── slides.qmd                                  Quarto markdown source
    ├── slides.html                                 Rendered HTML (for browser)
    ├── speaker_script.md                           Full presenter notes
    ├── build_slides.py                             Quarto build automation
    ├── custom.scss                                 Reveal.js theme CSS
    └── test_compile.css.map                        Build artifact
```

**How to regenerate slides:**
```bash
cd talks/2026-05-04_seminar/
python build_slides.py
# OR
quarto render slides.qmd --to revealjs
```

---

## 📋 `quality_reports/` — Session Logs & Plans

### Structure
```
quality_reports/
│
├── plans/                   Approved implementation plans (saved to disk for context survival)
│   ├── 2026-04-30_seminar-slides.md             Seminar presentation plan
│   ├── gemini-task-literature-index.md          Literature indexing task
│   ├── gemini-task-prune-infrastructure.md      Codebase cleanup
│   └── gemini-task-theory-literature-map.md     Theory-literature mapping
│
└── session_logs/            Per-session documentation (incremental notes)
    ├── 2026-03-15_handover.md                   Handover session log
    └── 2026-04-17_skill_audit.md                Skill infrastructure audit
```

---

## 🔍 `explorations/` — One-Off Analyses & Prototypes

```
explorations/
│
├── data-audit-2026-03-15/           Diagnostic data quality checks
│   └── [Distribution analysis, missing data patterns]
│
└── overnight-ideation-2026-03-15/   Exploratory theory sketching
    └── [Brainstorm ideas, not for publication]
```

---

## 🎨 `.claude/` — Agent Infrastructure

### `.claude/agents/` — Agent Configurations (5 files)

| File | Agent Type | Purpose |
|------|-----------|---------|
| `orchestrator.md` | Master orchestrator | Dependency graph, multi-agent dispatch, workflow automation |
| `coder.md` | Data scientist agent | Analysis script generation, pipeline debugging |
| `explorer.md` | Data explorer agent | Dataset discovery, schema documentation |
| `librarian.md` | Lit review agent | Paper ingestion, literature notes, cross-linking |
| `writer-critic.md` | Manuscript reviewer | Prose quality, argument structure, hedging detection |

### `.claude/rules/` — Governance Rules (5 files)

| File | Scope | Key Content |
|------|-------|-----------|
| `domain-profile.md` | Field calibration | Target journals, ref concerns, notation conventions |
| `journal-profiles.md` | Journal-specific | Review standards for AER, QJE, AJPS, etc. |
| `workflow.md` | Task execution | Plan-first protocol, orchestrator loop, dependency graph |
| `quality.md` | Quality gates | Scoring rubric (0–100), thresholds (80/90/95) |
| `logging.md` | Record-keeping | Session logs, research journal, memory updates |

### `.claude/skills/` — 17 Callable Skills

| Skill | Purpose | Invocation |
|-------|---------|-----------|
| `discover` | Literature + data discovery | `/discover "welfare institutions"` |
| `strategize` | Identification strategy design | `/strategize [research question]` |
| `analyze` | Run analysis pipeline | `/analyze [script name]` |
| `write` | Draft paper sections | `/write "Introduction"` |
| `review` | Peer review simulation | `/review --peer AJPS` |
| `revise` | R&R revision routing | `/revise [feedback.md]` |
| `talk` | Conference presentation | `/talk [paper.md]` |
| `submit` | Final gate check | `/submit [paper.pdf]` |
| `tools` | Utility scripts | `/tools [compile / validate / commit]` |
| [+ 8 more specialized skills] | Research operations | [Various] |

---

## 🗺️ Summary Navigation Map

### By Research Phase

| Phase | Key Files | Agent | Typical Questions |
|-------|-----------|-------|-------------------|
| **Discovery** | `docs/theory/`, `docs/literature/` | Librarian | Which papers support this theory? |
| **Strategy** | `metadata/theory_data_bridge.md`, `analysis/codebook.md` | Strategist | How do I operationalize this construct? |
| **Execution** | `analysis/final_analysis_pipeline.py`, `data/raw/` | Coder | Which dataset do I need? How do I merge? |
| **Results** | `outputs/figures/`, `outputs/tables/`, `analysis/review_diagnostics/` | Analyst | Are my results robust? What do the diagnostics say? |
| **Writing** | `manuscripts/`, `talks/` | Writer | How do I frame these results for my audience? |

### By Question Type

| Question | Answer Location |
|----------|-----------------|
| "What's in dataset X?" | `metadata/data_dictionary.md` — search for dataset name |
| "Which variables measure [construct]?" | `metadata/theory_data_bridge.md` — search for construct name |
| "How do I load ESS data?" | `scripts/load_ess.py` or `.R` — load functions with examples |
| "What are the main findings?" | `outputs/tables/table2_main_results.csv` — coefficients |
| "Is the effect robust?" | `outputs/tables/tableA1_robustness.csv` — alternative specs |
| "How does it vary by country?" | `outputs/figures/fig6_cwed_country_slopes.pdf` — random slopes |
| "What's the mechanism?" | `docs/theory/14_mechanisms_catalog.md` — full inventory |

---

## 📊 Repository Statistics (May 4, 2026)

| Metric | Count |
|--------|-------|
| **Data** ||
| Study folders | 20 |
| Unique datasets | 104 |
| Total data volume | 2.6 GB (unique) |
| Data dictionary lines | 37,199 |
| **Theory & Literature** ||
| Theory modules | 15 |
| Literature notes | 97 |
| Total theory prose | 115+ KB |
| **Analysis** ||
| Python scripts | 12 |
| R/Stata scripts | 3 |
| Diagnostic files | 15+ |
| **Outputs** ||
| Publication figures | 20+ (PDF + PNG pairs) |
| Results tables | 12+ (CSV + JSON) |
| Manuscript drafts | 2 active versions |
| **Infrastructure** ||
| Agent configs | 5 |
| Skill scripts | 17 |
| Governance rules | 5 |
| **Documentation** ||
| Session logs | 2+ |
| Implementation plans | 3 |
| Status files | 2 |

---

## 🔗 Key Relationships & Data Flows

### Data → Analysis → Results Flow
```
data/raw/[20 studies]
  ↓ [load_ess.py, scripts/*.py]
data/samples/  [analysis-ready subsets]
  ↓ [final_analysis_pipeline.py]
analysis/  [models, diagnostics]
  ↓ [export to JSON/CSV]
outputs/  [tables/ figures/]
  ↓
manuscripts/  [embed in paper]
  ↓
talks/  [adapt for presentation]
```

### Theory → Data → Paper Flow
```
docs/theory/ [15 modules]
  ↓
metadata/theory_data_bridge.md [map concepts to variables]
  ↓
metadata/data_dictionary.md [find exact columns]
  ↓
data/raw/ + analysis/ [load, construct, test]
  ↓
docs/literature/ [synthesize with 97 notes]
  ↓
manuscripts/ [write findings + theory synthesis]
```

### Quality Gate Dependencies
```
data/samples/  [diagnostics] →→ PASS?
  ↓
analysis/final_analysis_pipeline.py  →→ PASS?
  ↓
analysis/review_diagnostics/  [validation] →→ PASS?
  ↓
outputs/  [figures, tables ready]
  ↓
manuscripts/  [can draft]
  ↓
talks/  [final presentation]
```

---

## 🔧 Troubleshooting & Common Tasks

### "I need variable X. Where is it?"

1. **Try data dictionary first:**
   ```bash
   grep -n "varname" metadata/data_dictionary.md
   ```
   If found → tells you which dataset (section header) + column + sample values

2. **If not found → construct it:**
   Look up the construct in `metadata/theory_data_bridge.md`
   - Find formula for variable construction
   - Check `analysis/codebook.md` for transformation code

3. **If still missing → check scripts:**
   ```bash
   grep -r "varname\|my_construct" scripts/ analysis/
   ```

### "How do I load dataset Y and merge it?"

**For ESS data:**
```bash
python scripts/load_ess.py --waves 6 7 8 9
# Handles encoding, missing values, version management
```

**For study-specific data:**
1. Find study folder in `data/raw/`
2. Look for `README.md` or `codebook` in that folder
3. Check `analysis/final_analysis_pipeline.py` for merge example
4. See `metadata/theory_data_bridge.md` for merge logic

### "I need to understand the main analysis. Where do I start?"

1. Read: `analysis/final_analysis_report.md` (overview)
2. Read: `analysis/codebook.md` (variable transformations)
3. Skim: `analysis/final_analysis_pipeline.py` (actual code)
4. Check: `analysis/review_diagnostics/` (validation)
5. Review: `outputs/tables/table2_main_results.csv` (results)

### "Figure X in the paper isn't matching my latest analysis run. Where's the mismatch?"

1. **Check figure generation code:**
   ```bash
   grep -n "fig1\|fig_rti_antiimmig" scripts/*.py analysis/*.py
   ```

2. **Check if data inputs changed:**
   ```bash
   git diff HEAD~5 data/raw/  # Did any raw data get re-downloaded?
   ```

3. **Re-run pipeline:**
   ```bash
   python analysis/final_analysis_pipeline.py --overwrite-outputs
   ```

4. **Verify new figure matches paper:** Compare `outputs/figures/fig1_*.pdf` timestamp against manuscript edit date

### "I want to check if result is robust to [specification change]. How?"

1. **See robustness already done:**
   `outputs/tables/tableA1_robustness.csv` — alternative specs already computed

2. **Check what was varied:**
   `analysis/final_analysis_report.md` → "Robustness" section lists all specs tested

3. **Add new robustness check:**
   Edit `analysis/final_analysis_pipeline.py` → add new `spec_` and rerun

4. **Jackknife diagnostics:**
   `analysis/review_diagnostics/jackknife_*.csv` — see what happens if one country/region is excluded

---

## Last Reviewed & Next Update

**Last reviewed:** May 4, 2026  
**Next update trigger:** After journal submission, major data refresh, or thesis chapter completion  
**Maintained by:** Ben Smart  
**Repository:** `Research_Master/REPOSITORY_MAP.md`
