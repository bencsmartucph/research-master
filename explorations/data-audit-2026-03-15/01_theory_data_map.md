# 01 — Theory–Data Map
> Phase 3: Data Audit | Date: 2026-03-15
> Maps all 15 theory modules to datasets and variables, with ground-truth status from live sample inspection.
> Status codes: MAPPED = variable confirmed in actual data file | PARTIAL = some required variables present, others missing or require construction | NO PATH = key variable absent from repository

---

## Summary Table

| Module | Theory | Primary Dataset(s) | Required Variables | Status |
|--------|--------|-------------------|-------------------|--------|
| 01 | Embedded Liberalism | CPDS, Milner regional | `almp_pmp`, `social1-8`, `nuts2_right_pop_vs`, `shock_china_imports` | MAPPED |
| 02 | Automation & RTI | isco08_3d-task3.csv, Im ESS, Baccini individual | `isco08`, `task` (NOT `rtask`/`nrtask`), `rti` | PARTIAL |
| 03 | Globalisation/Trade/Spatial | Milner regional merged | `shock_china_imports`, `nuts2_right_pop_vs`, `regional_gdp`, `nuts2` | MAPPED |
| 04 | Precarity & Skill Specificity | Aspiration/apprehension, ESS | `short_isco3d`, `class5`, `rr`, `dfincac` | PARTIAL |
| 05 | Policy Feedback | Baccini analysis-ready, CPDS | `austerity_dummy`, `populism_score`, `almp_pmp` | MAPPED |
| 06 | ALMPs | CPDS, ELFS, Gingrich RP_Context | `almp_pmp`, `RTIshare`, ALMP type (NOT available) | PARTIAL |
| 07 | Welfare Design/Trust | ESS (all waves) | `trstprl`, `trstplt`, `trstep`, `stfgov`, `stfdem` | MAPPED |
| 08 | Status & Recognition | Cicollini (EU-SILC required) | `posit_income_change` | NO PATH |
| 09 | Ontological Security | ESS | `stflife`, `happy`, `atchctr`, `atcherp`, `sclact` | MAPPED |
| 10 | Moral Economy | ESS, Steiner ZA7700, ISSP | `imwbcnt`, `imueclt`, `gincdif`, welfare attitudes | MAPPED |
| 11 | Social Investment | CPDS, ESS | `educexp_gov`, `almp_pmp`, `eisced` | PARTIAL |
| 12 | Populism/Mobilization | Baccini individual, GPS, crosswalk | `populism_score`, party vote crosswalk | PARTIAL |
| 13 | Dual Pathway Synthesis | Baccini + Milner + CPDS | All above; `posit_income_change` absent | PARTIAL |
| 14 | Mechanisms Catalog | Cross-cutting | See individual modules | N/A |
| 15 | Cognitive Frames | ESS, Aspiration/apprehension | `imueclt`, `imwbcnt`, `trstep`, `lrscale` | MAPPED |

---

## Detailed Module-by-Module Mapping

### Module 01: Embedded Liberalism & Economic Vulnerability

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Trade openness / Chinese import exposure | `shock_china_imports`, `shock_lowwage_imports`, `shock_wlrd_ind` | milner_merged_regional (nuts2 level) | MAPPED |
| Welfare state generosity | `social1`–`social8` (social transfer categories) | CPDS_Aug_2020.dta | MAPPED (need codebook for label mapping) |
| ALMP spending | `almp_pmp` | CPDS_Aug_2020.dta | MAPPED |
| Regional GDP per capita | `regional_gdp`, `reg_gva_total` | milner_merged_regional | MAPPED |
| Far-right/populist vote share | `nuts2_right_pop_vs`, `nuts2_left_pop_vs` | milner_merged_regional | MAPPED |
| Austerity fiscal consolidation | `austerity_dummy`, `total_impact_t`, `spend_impact_t` | Baccini individual, Alesinadata_annual | MAPPED |

**Notes:** CPDS `social1`–`social8` variable labels require pyreadstat meta inspection to identify which sub-category corresponds to which spending type. Milner regional file is the analysis-ready merge of NUTS2 regional data + trade exposure + electoral outcomes.

---

### Module 02: Automation & Technological Change

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Routine Task Intensity (RTI) — occupation-level | `task` (composite, isco08_3d-task3.csv) | isco08_3d-task3.csv | PARTIAL — variable is named `task`, NOT `rtask`/`nrtask` as documented |
| RTI — individual-level (pre-computed) | `rti` | Baccini individualdata.dta | MAPPED |
| RTI — regional share | `RTIshare`, `RTIshare_1999` | ELFS_regional_routine_shares.dta | MAPPED |
| ISCO-08 occupation code (merge key) | `isco08` | Im ESS CSV, Baccini ESSdata | MAPPED |
| ISCO-88 occupation code (in Gugushvili waves) | `iscoco` | ESS waves 1–5 (Gugushvili) | MAPPED — but ISCO-88 ≠ ISCO-08; requires `correspondence.dta` crosswalk |
| ISCO-88 → ISCO-08 crosswalk | `isco88`, `isco08` | correspondence.dta (Kurer) | MAPPED |
| Radical right vote | country-specific `prtvt*` | Im ESS CSV | MAPPED (complex structure) |
| State ALMP response to automation | contextual ALMP per routine worker | RP_Context_Data.dta | MAPPED |

**CRITICAL DOCUMENTATION ERROR:** The theory_data_bridge.md states RTI variables are named `rtask` and `nrtask`. The actual task file (`isco08_3d-task3.csv`) contains only two columns: `isco08_3d` and `task`. There is ONE composite task score, not separate routine/non-routine scores. Any code using `rtask`/`nrtask` will fail silently (missing variable).

**CRITICAL PATH NOTE:** ESS waves 1–5 (Gugushvili) use ISCO-88 (`iscoco`), NOT ISCO-08. The direct merge path documented in CLAUDE.md (`df['isco08'] // 10`) does not apply to these files. Correct merge requires two steps: (1) `correspondence.dta` ISCO-88 → ISCO-08 crosswalk, then (2) 3-digit truncation. Alternatively, use the Im ESS CSV or Baccini ESSdata which contain `isco08` directly.

---

### Module 03: Globalisation, Trade & Spatial Dimensions

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Chinese import exposure | `shock_china_imports`, `shock_china_ind`, `china_imp_D05T08` | milner_merged_regional | MAPPED |
| Low-wage country imports | `shock_lowwage_imports`, `shock_lowwage_ind` | milner_merged_regional | MAPPED |
| Regional manufacturing employment | `emp_industry`, `mfgempshare` (ELFS) | milner_merged_regional, ELFS | MAPPED |
| Regional GDP / decline | `regional_gdp`, `reg_gva_total` | milner_merged_regional | MAPPED |
| Right-wing populist vote share (NUTS2) | `nuts2_right_pop_vs`, `nuts2_right_pop_vs_diff` | milner_merged_regional | MAPPED |
| NUTS2 region identifier | `nuts2`, `nutsid` | milner_merged_regional | MAPPED |
| Robot adoption shock | `robots_shock_nmwi` | milner_merged_regional | MAPPED |

**Notes:** The milner_merged_regional file is the most complete analysis-ready dataset for trade + regional + electoral analysis. `nuts2_right_pop_vs` is right-wing populist vote share; also has `nuts2_left_pop_vs`, `nuts2_main_left_vs`, `nuts2_main_right_vs` for decomposition.

---

### Module 04: Precarity, Skill Specificity & Occupational Risk

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Occupational risk (subjective apprehension) | `short_isco3d`, `class5`, `class8`, `rr` (radical right) | aspiration_apprehension_data.csv | PARTIAL — 31 variables, no standard ESS identifiers |
| Financial precarity (objective) | `hinctnta` (income decile) | ESS waves 4–5 | MAPPED |
| Financial precarity (subjective) | `dfincac` (difficulty affording basic needs) | ESS — needs wave check | PARTIAL |
| Skill specificity (proxy via task type) | `task` → routine = specific skills | isco08_3d-task3.csv | PARTIAL |
| ISCO crosswalk for class scheme | `isco88`, `isco08` → EGP/Oesch scheme | correspondence.dta | MAPPED |
| Job insecurity (Sweden only) | SIWE_betaMay2017.dta variables | siwe_2017 | PARTIAL — single-country only |

**Notes:** The aspiration_apprehension_data.csv has 31 columns covering a custom multi-country survey but lacks documentation in the data_dictionary.md for exact country and year coverage. Variable names use coded labels (X5_3, X8_8_7 etc.). Cannot determine N per country without loading the full file.

---

### Module 05: Policy Feedback & Welfare Institutions

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Austerity (binary) | `austerity_dummy` | Baccini individualdata.dta | MAPPED |
| Austerity (lagged/lead) | `austerity_lag`, `austerity_lead` | Baccini individualdata.dta | MAPPED |
| Austerity (fiscal episodes) | `total_impact_t`, `spend_impact_t`, `tax_impact_t` | Alesinadata_annual.dta | MAPPED |
| Individual populist vote | `populism_score`, `share_populist_parties_gps` | Baccini individualdata.dta | MAPPED |
| Welfare state generosity | `social1`–`social8` | CPDS_Aug_2020.dta | MAPPED |
| District-level far-right vote | `radical_right`, `nuts2` | Baccini districtdata.dta | MAPPED |

---

### Module 06: Active Labour Market Policies (ALMPs)

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| ALMP spending % GDP | `almp_pmp` | CPDS_Aug_2020.dta | MAPPED |
| Passive spending % GDP | `unemp_pmp` | CPDS_Aug_2020.dta | MAPPED |
| Regional routine employment share | `RTIshare`, `RTI2share` | ELFS_regional_routine_shares.dta | MAPPED |
| State ALMP response (automation context) | automation-context ALMP variable | RP_Context_Data.dta | MAPPED |
| ALMP type (enabling vs. punitive) | NOT AVAILABLE | — | NO PATH |

**Critical caveat:** CPDS `almp_pmp` is total ALMP spending as % GDP. It cannot distinguish enabling (human capital investment) ALMPs from punitive/workfare ALMPs. This distinction is central to Module 06's theoretical argument. Operationalising the enabling/punitive distinction requires country expert surveys or qualitative classification not in the repository.

---

### Module 07: Welfare Design, Trust & Legitimacy

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Trust in parliament | `trstprl` | ESS all waves | MAPPED |
| Trust in politicians | `trstplt` | ESS all waves | MAPPED |
| Trust in EU | `trstep` | ESS all waves | MAPPED |
| Satisfaction with government | `stfgov` | ESS all waves | MAPPED |
| Satisfaction with democracy | `stfdem` | ESS all waves | MAPPED |
| Welfare deservingness attitudes | ISSP attitude battery | ZA7700 (Steiner), ZA3090, ZA4950 | MAPPED (numeric codes — load meta first) |

---

### Module 08: Status, Recognition & Relative Position

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Positional income change (rank trajectory) | `posit_income_change` | **NOT IN REPOSITORY** | NO PATH |
| Absolute income (proxy only) | `hinctnta` | ESS waves 4–5 | MAPPED (but wrong construct) |
| Intergenerational class mobility | father ISCO + respondent ISCO | ESS `iscoco` + `iscocop` (ISCO-88) | PARTIAL — needs class coding via correspondence.dta |
| Status discordance (apprehension index) | `class5`, `class8`, apprehension items | aspiration_apprehension_data.csv | PARTIAL — custom survey, limited coverage |
| Subjective class position | `subjclass` (ESS, where available) | ESS — wave-specific | PARTIAL |

**CRITICAL FINDING:** `posit_income_change` is constructed by Cicollini using EU-SILC microdata (income survey panel tracking individual income rank over time). The `essprt-all.dta` file in `cicollini_2025/` is a **party-ESS vote variable crosswalk** (5,402 rows × 13 columns), NOT the individual-level analysis dataset. The individual-level dataset with `posit_income_change` was built in Cicollini's Stata do file from EU-SILC data that is not stored in this repository. This variable cannot be used without downloading EU-SILC microdata, which requires EUROSTAT registration and is country-year specific.

---

### Module 09: Ontological Security & Psychology

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Life satisfaction | `stflife` | ESS all waves | MAPPED |
| Happiness | `happy` | ESS all waves | MAPPED |
| Attachment to country | `atchctr` | ESS (need wave check) | MAPPED |
| Attachment to Europe | `atcherp` | ESS (need wave check) | MAPPED |
| Social activity / loneliness proxy | `sclact`, `sclmeet` | ESS | MAPPED |
| Wellbeing index (pre-constructed) | composite index | graphsdata.dta (Silva) — 4.7KB only | PARTIAL — tiny file, likely analysis-summary |

---

### Module 10: Moral Economy, Deservingness & Welfare Chauvinism

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Immigration attitudes (cultural) | `imueclt` | ESS all waves | MAPPED |
| Immigration attitudes (economic) | `imwbcnt` | ESS all waves | MAPPED |
| Redistribution preference | `gincdif` (government should reduce differences) | ESS all waves | MAPPED |
| Welfare chauvinism items | ISSP social inequality battery | ZA7700 (Steiner), ZA3090, ZA4950 | MAPPED (numeric codes — load meta) |
| Euroscepticism | `trust_eu`, `eu_pos` | euroscepticism_stagnation .dta | MAPPED |

---

### Module 11: Social Investment Paradigm

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Social investment spending | `educexp_gov`, `almp_pmp` | CPDS_Aug_2020.dta | MAPPED |
| Education level | `eisced`, `eduyrs` | ESS — need wave check | PARTIAL |
| Childcare spending | NOT explicitly labelled in CPDS | CPDS `social` subcategories | PARTIAL |
| Predistribution preferences | no direct survey variable | — | NO PATH |

---

### Module 12: Populism & Right-Wing Mobilization

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Individual populist party vote | `populism_score`, `share_populist_parties_gps` | Baccini individualdata.dta | MAPPED |
| Party populism score (expert survey) | GPS data (large DTA) | Global_Party_Survey_by_Party.dta | MAPPED |
| ESS party vote → populist flag | `ess_populist_crosswalk.csv` | langenkamp_2022 | PARTIAL — crosswalk maps to partyfacts IDs, NOT direct populism flag |
| Regional right-wing populist vote | `nuts2_right_pop_vs` | milner_merged_regional | MAPPED |
| Party manifesto position | RILE, welfare position | MPDataset_MPDS2019b.dta | MAPPED |

**Notes:** The Langenkamp crosswalk is semicolon-delimited (not comma-delimited) and maps ESS party vote variable codes to partyfacts IDs. It does NOT contain a direct `populism_flag` or `rrp_flag` column. To get a binary populist vote indicator requires a subsequent merge with the Global Party Survey or a populism classification dataset. The Baccini `populism_score` is already constructed and is the most direct route for individual-level populism vote analysis.

---

### Module 13: Dual Pathway Synthesis & The Trilemma

| Pathway | Variables needed | Available? |
|---------|-----------------|------------|
| Material hardship | `austerity_dummy`, `hinctnta`, `rti` | YES — Baccini individual |
| Status/positional decline | `posit_income_change` | NO — EU-SILC required |
| Anticipated hardship | apprehension index | PARTIAL — aspiration_apprehension_data.csv |
| Institutional context (welfare design) | `almp_pmp`, welfare regime type | YES — CPDS |
| Political outcome | `populism_score`, `nuts2_right_pop_vs` | YES — multiple files |

**Status: PARTIAL** — Three of four pathways testable. The status pathway (Module 08) is blocked by missing EU-SILC data. The three-pathway model (material + automation + austerity) with institutional moderation is fully feasible with available data.

---

### Module 14: Mechanisms Catalog

Cross-cutting reference module — no standalone dataset. See constituent modules above.

---

### Module 15: Cognitive Frames, Belief Systems & Political Realignment

| Theoretical construct | Variable name(s) | Dataset | Status |
|----------------------|-----------------|---------|--------|
| Immigration blame (misattribution) | `imueclt`, `imwbcnt` | ESS all waves | MAPPED |
| EU attitudes / Euroscepticism | `trstep`, `eu_pos`, `trust_eu` | ESS, euroscepticism.dta | MAPPED |
| Left-right self-placement | `lrscale` | ESS all waves | MAPPED |
| Meritocratic beliefs | no standard ESS variable | — | NO PATH |
| Universalism-particularism scale | constructed from items | ESS — requires construction | PARTIAL |
| Populism attitudes index | populism attitude items | Armaly US data, essprt-all | PARTIAL (Armaly is US-only) |
| Apprehension index (misattribution test) | `short_isco3d`, apprehension score | aspiration_apprehension_data.csv | PARTIAL |

---

## Path-Not-Found Summary

| Module | Missing variable / construct | Why it's missing | What would unlock it |
|--------|------------------------------|-----------------|---------------------|
| 02 | `rtask`, `nrtask` as named | Task file only has `task` (one composite score) | Rename references or use `task` |
| 08 | `posit_income_change` | Requires EU-SILC microdata (Eurostat registration) | Download EU-SILC via essurvey/Eurostat; run Cicollini do file |
| 06 | ALMP type classification | No cross-national ALMP type dataset in repo | Add LABREF/MISSOC conditionality data |
| 11 | Childcare spending (labelled) | CPDS `social` subcategories unlabelled | Read CPDS codebook to map social1–8 |
| 15 | Meritocratic beliefs scale | No standard cross-national measure | Construct from available ESS items |

---

*Generated: 2026-03-15 | Source: Live inspection of stratified samples + raw data files + data_dictionary.md*
