# 🌉 Theory–Data Bridge

> **Purpose:** Maps each of the 15 theory modules to the specific datasets and variables in this repository that operationalize their core constructs.
> **How to use:** When you know which theory module you're working with, come here first. This tells you which datasets to load and which variables measure the key concepts.
> **See also:** `data_dictionary.md` for full column schemas · `theory/` folder for full module prose.

---

## Navigation

| Module | Theory | Primary Datasets | Unit of Analysis |
|--------|--------|-----------------|-----------------|
| [01](#01-embedded-liberalism--economic-vulnerability) | Embedded Liberalism & Economic Vulnerability | Milner OECD trade, CPDS | Country-year |
| [02](#02-automation--technological-change) | Automation & Technological Change | isco08_3d-task3, Gingrich ZA-files, Baccini ESSdata | Individual (+ occupation) |
| [03](#03-globalization-trade--spatial-dimensions) | Globalization, Trade & Spatial | Milner trade, BFW, ARDECO, CLEA | Region-year / country-year |
| [04](#04-precarity-skill-specificity--occupational-risk) | Precarity & Skill Specificity | isco08_3d-task3, correspondence, ESS | Individual / occupation |
| [05](#05-policy-feedback--welfare-institutions) | Policy Feedback & Welfare Institutions | CPDS, Baccini austerity, Alesinadata | Country-year |
| [06](#06-active-labour-market-policies-almps) | ALMPs | CPDS, ELFS | Country-year / region-year |
| [07](#07-welfare-design-trust--legitimacy) | Welfare Design, Trust & Legitimacy | ESS (trstprl, stfgov), ZA welfare modules | Individual |
| [08](#08-status-recognition--relative-position) | Status, Recognition & Relative Position | Cicollini essprt-all, Gugushvili ESS, correspondence | Individual |
| [09](#09-ontological-security--psychology) | Ontological Security & Psychology | ESS (wellbeing vars), Silva graphsdata, Steiner ZA7700 | Individual |
| [10](#10-moral-economy-deservingness--welfare-chauvinism) | Moral Economy & Deserving­ness | ESS (immigration/welfare vars), ISSP ZA-files, Steiner ZA7700 | Individual |
| [11](#11-social-investment-paradigm) | Social Investment | CPDS, ESS (education/skills vars) | Country-year / individual |
| [12](#12-populism--right-wing-mobilization) | Populism & Right-Wing Mobilization | CLEA, party_classifications, Global Party Survey, MPDataset | Party-election / individual |
| [13](#13-dual-pathway-synthesis--the-trilemma) | Dual Pathway Synthesis | Baccini analysis-ready .dta files, Milner merged data | Individual + district |
| [14](#14-mechanisms-catalog) | Mechanisms Catalog | Cross-cutting — see individual modules | — |
| [15](#15-cognitive-frames-belief-systems--political-realignment) | Cognitive Frames & Belief Systems | Cicollini, Aspiration/Apprehension, ESS attitude vars | Individual |

---

## 01: Embedded Liberalism & Economic Vulnerability

**Core construct:** The bargain between trade openness and welfare compensation, and its breakdown. Key variables are trade openness (imports/exports as % GDP), welfare spending generosity, and indicators of whether compensation reached the actual losers.

**Theory file:** `theory/01_embedded_liberalism_economic_vulnerability.md`
**See also in theory:** modules 03 (trade → place), 04 (skills → risk), 05 (welfare feedback), 11 (social investment alternative)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `oecd_chinese_trade.dta` | `data/raw/milner_2021/data/oecd_trade/` | Chinese import penetration by sector/country | Core "China shock" exposure variable |
| `oecd_lowwage_trade.dta` | same folder | Low-wage import exposure | Broader trade competition measure |
| `oecd_world_trade.dta` | same folder | Overall trade openness | |
| `CPDS_Aug_2020.dta` | `data/raw/baccini_2024/Raw Data/` | Welfare spending, social transfers, ALMP % GDP | Comparative Political Dataset — country-year panel |
| `FRED_deflator_2020 (2015 base).csv` | `data/raw/milner_2021/oecd_trade/` | Price deflators for trade data | Needed to convert trade values to real terms |
| `regional_gdp_by_year.dta` | `data/raw/milner_2021/ardeco/` | Regional GDP per capita (NUTS2) | ARDECO data — region-year |
| `imputed_econdata_voteshare_merged.dta` | `data/raw/milner_2021/imputed/` | Merged regional econdata + vote shares | **Analysis-ready merged file** |

### Construct → Variable Mapping

| Theoretical construct | Variable name(s) | Dataset |
|----------------------|-----------------|---------|
| Trade openness | country-level trade/GDP ratios | CPDS, OECD trade files |
| Chinese import exposure | regional Chinese import penetration | oecd_chinese_trade.dta |
| Welfare compensation generosity | social transfer spending % GDP | CPDS |
| Regional inequality | GDP per capita NUTS2, growth rates | regional_gdp_by_year.dta |
| Populist/far-right response | FarRight vote share, ER_voteshare | imputed_econdata_voteshare_merged.dta |

---

## 02: Automation & Technological Change

**Core construct:** Routine Task Intensity (RTI) as the measure of automation vulnerability — not skill level. The key causal chain is: high-RTI occupation → anticipated status decline (not actual job loss) → support for radical right. The *isco08_3d-task3.csv* file is the **central linking dataset** that enables this analysis across virtually all other datasets.

**Theory file:** `theory/02_automation_technological_change.md`
**See also in theory:** modules 04 (skill specificity adds another dimension), 08 (status decline mechanism), 12 (how automation-exposed workers reach populism)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `isco08_3d-task3.csv` | `data/raw/aspiration_apprehension/` | `isco08_3d`, `rtask`, `nrtask`, task intensity scores | **THE key linking file** — merge to any dataset with ISCO-08 codes |
| `SIWE_betaMay2017.dta` | `data/raw/siwe_2017/` | Swedish work environment, task assessments, job security | Individual-level task self-reports (Sweden only) |
| `RP_Context_Data.dta` | `data/raw/gingrich_2019/` | Regional automation policy context, ALMP spending, routine employment shares | Region-level automation exposure |
| `ELFS_regional_routine_shares.dta` | `data/raw/baccini_2024/Raw Data/` | Regional share of routine employment (NUTS2) | From EU Labour Force Survey |
| ZA-files (ISSP waves) | `data/raw/gingrich_2019/` | Vote choice + occupation codes → merge with RTI | See list below |
| `Baciini - ESSdata.dta` | `data/raw/baccini_2024/Raw Data/` | Individual ESS with `isco08`, political attitudes | Largest ESS file (599MB) — use sample first |
| `Im - A Reservoir...ESS.csv` | `data/raw/im_2021/` | Pooled ESS with radical right vote + occupation | Analysis-ready for automation-voting analysis |

**ISSP ZA-file series (Gingrich):**
| File | ZA code | Year | ISSP module |
|------|---------|------|-------------|
| `ZA2880.dta` | ZA2880 | 1997 | Work Orientations II |
| `ZA2900.dta` | ZA2900 | 1997 | Social Inequality II |
| `ZA3090.dta` | ZA3090 | 1999 | Social Inequality III |
| `ZA3190.dta` | ZA3190 | 1999 | Work Orientations II |
| `ZA3430.dta` | ZA3430 | 2001 | Social Networks II |
| `ZA3440.dta` | ZA3440 | 2002 | Family and Changing Gender Roles |
| `ZA3680.dta` | ZA3680 | 2003 | National Identity II |
| `ZA3880.dta` | ZA3880 | 2005 | Work Orientations III |
| `ZA3910.dta` | ZA3910 | 2004 | Citizenship II |
| `ZA3950.dta` | ZA3950 | 2005 | Social Inequality III |
| `ZA4350.dta` | ZA4350 | 2006 | Role of Government IV |
| `ZA4700.dta` | ZA4700 | 2007 | Social Networks III |
| `ZA4850.dta` | ZA4850 | 2008 | Religion III |
| `ZA4950.dta` | ZA4950 | 2009 | Social Inequality IV |
| `ZA5400.dta` | ZA5400 | 2010 | Environment III |
| `ZA5500.dta` | ZA5500 | 2011 | Health & Healthcare |
| `ZA5800.dta` | ZA5800 | 2012 | Family and Changing Gender Roles |
| `ZA5950.dta` | ZA5950 | 2013 | National Identity III |
| `ZA6670.dta` | ZA6670 | 2015 | Work Orientations IV |
| `ZA6770.dta` | ZA6770 | 2016 | Role of Government V |

### Construct → Variable Mapping

| Theoretical construct | Variable name(s) | Dataset |
|----------------------|-----------------|---------|
| Routine Task Intensity (RTI) | `rtask`, `rti` | isco08_3d-task3.csv |
| Non-routine task intensity | `nrtask` | isco08_3d-task3.csv |
| Occupation code (merge key) | `isco08` (4-digit) → `isco08_3d` (3-digit) | ESS / ISSP ZA-files |
| Radical right vote | party vote variable → classify via party_classifications | ESS, ISSP |
| Regional routine employment share | `routine_share` (approx.) | ELFS_regional_routine_shares.dta |
| State ALMP response to automation | spending per routine-job at risk | RP_Context_Data.dta |

### Critical merge note
ESS provides 4-digit ISCO-08 (`isco08`). The task file uses 3-digit (`isco08_3d`). Truncate:
```python
df['isco08_3d'] = (df['isco08'] / 10).astype(int)
tasks = pd.read_csv('data/raw/aspiration_apprehension/isco08_3d-task3.csv')
df = df.merge(tasks, on='isco08_3d', how='left')
```

---

## 03: Globalization, Trade & Spatial Dimensions

**Core construct:** Trade shocks create geographically concentrated, persistent regional decline. The China shock operates at the regional level: constituencies with more manufacturing exposure voted more for anti-system parties. Housing markets mediate this through local economic optimism. Key unit of analysis is the **region** (NUTS2/3 or constituency).

**Theory file:** `theory/03_globalization_trade_spatial.md`
**See also in theory:** modules 01 (welfare compensation), 04 (occupational risk in affected regions), 12 (political consequences)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `BFW_IO.dta` | `data/raw/broz_2019/
| `BFW_manufacturing_shares.dta` | same | Manufacturing employment share by region | |
| `oecd_chinese_trade.dta` | `data/raw/milner_2021/oecd_trade/` | Chinese import penetration | |
| `oecd_lowwage_trade.dta` | same | Low-wage country trade | |
| `oecd_world_trade.dta` | same | Overall trade openness | |
| `CLEA_voteshare_turnout.dta` | `data/raw/milner_2021/parties_votes/` | Constituency-level vote shares by party | CLEA electoral archive — join on region code |
| `regional_gdp_by_year.dta` | `data/raw/milner_2021/ardeco/` | Regional GDP per capita, NUTS2 | ARDECO |
| `regional_data_impute.dta` | `data/raw/milner_2021/imputed/` | Regional economic data (imputed) | |
| `imputed_econdata_voteshare_merged.dta` | same | **Analysis-ready:** regional econdata + vote shares | Use this for regional-level analysis |
| `parlgov_election_05202020.csv` | `data/raw/milner_2021/parties_votes/` | National election results | ParlGov |

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| Chinese import exposure | import penetration index | BFW_IO.dta, oecd_chinese_trade.dta |
| Manufacturing decline | manufacturing employment share, change | BFW_manufacturing_shares.dta |
| Regional economic decline | GDP per capita, growth rate (NUTS2) | regional_gdp_by_year.dta |
| Far-right vote share | vote share by party (need party classification) | CLEA_voteshare_turnout.dta |
| Party populism classification | party family / far-right flag | party_classifications.dta |

---

## 04: Precarity, Skill Specificity & Occupational Risk

**Core construct:** Skill specificity determines whether unemployment risk can be absorbed (transferable skills → low risk; specific skills → high risk). Precarity is multidimensional: work conditions + tenure security + financial stability. Age-differentiated effects: younger workers need job opportunities, older workers need early retirement options.

**Theory file:** `theory/04_precarity_skill_specificity.md`
**See also in theory:** modules 02 (automation as source of precarity), 03 (regional context), 08 (status loss pathway)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `isco08_3d-task3.csv` | `data/raw/aspiration_apprehension/` | Task scores including skill measures | Proxy for skill specificity via task type |
| `correspondence.dta` | `data/raw/kurer_2020_declining_middle/
| `SIWE_betaMay2017.dta` | `data/raw/siwe_2017/
| `aspiration_apprehension_data.csv` | `data/raw/aspiration_apprehension/` | Aspiration vs. apprehension index, occupation, voting | Directly tests anticipated vs. experienced hardship |
| `Baciini - ESSdata.dta` | `data/raw/baccini_2024/Raw Data/` | ESS with occupation + subjective economic security | Individual-level |
| `ELFS_regional_routine_shares.dta` | `data/raw/baccini_2024/Raw Data/` | Regional routine employment share | Region-level precarity exposure |

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| Skill specificity (proxy) | routine vs. abstract task mix | isco08_3d-task3.csv |
| ISCO occupation crosswalk | `isco88`, `isco08`, class codes | correspondence.dta |
| Financial precarity | subjective financial hardship | ESS (`hinctnta`, `dfincac`) |
| Job insecurity | perceived job security | SIWE, ESS |
| Anticipated hardship | apprehension index | aspiration_apprehension_data.csv |
| Work tenure insecurity | contract type, tenure | SIWE |

---

## 05: Policy Feedback & Welfare Institutions

**Core construct:** Welfare policies generate self-reinforcing (upward spirals of solidarity) or self-undermining (austerity → backlash) feedback. Austerity cuts create "interpretive effects" that teach norms about who is deserving. Baccini (2024) tests this directly: austerity → economic vulnerability → populist voting.

**Theory file:** `theory/05_policy_feedback_welfare_institutions.md`
**See also in theory:** modules 06 (ALMPs as feedback mechanism), 07 (design details), 11 (social investment alternative), 12 (populist backlash outcome)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `CPDS_Aug_2020.dta` | `data/raw/baccini_2024/Raw Data/` | Social transfers, welfare spending, ALMP, unemployment insurance | **Core macro welfare state panel** — country-year |
| `Alesinadata_annual.dta` | same | Fiscal consolidation episodes (Alesina-Ardagna method) | Annual austerity data |
| `Austeritydata_byelperiod.csv` | same | Austerity by electoral period | |
| `Analysis_Dataset_District_Level.dta` | `data/raw/baccini_2024/Data/Raw Data/` | District-level austerity exposure + electoral outcomes | |
| `districtdata.dta` | `data/raw/baccini_2024/Data/` | **Analysis-ready** district-level dataset | Use this for Baccini replication |
| `individualdata.dta` | same | **Analysis-ready** individual-level dataset | Use this for Baccini replication |
| `macrodata_ind.dta` | `data/raw/baccini_2024/Raw Data/` | Country-level macro indicators | |
| `graphsdata.dta` | `data/raw/silva_wellbeing/

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| Welfare state generosity | social transfer spending % GDP | CPDS |
| Austerity (fiscal consolidation) | fiscal balance change, spending cuts | Alesinadata_annual.dta |
| Austerity exposure | district-level cuts | Analysis_Dataset_District_Level.dta |
| ALMP spending | almp % GDP | CPDS |
| Unemployment insurance | UI replacement rate | CPDS |
| Populist vote response | party vote share in district | districtdata.dta |

---

## 06: Active Labour Market Policies (ALMPs)

**Core construct:** ALMP type and implementation quality determine outcomes. Enabling (human capital) ALMPs → wellbeing gains. Punitive/workfare ALMPs → stigma. The CPDS measures ALMP spending as % GDP but doesn't distinguish types — the distinction requires additional qualitative classification.

**Theory file:** `theory/06_almps_active_labour_market_policy.md`
**See also in theory:** modules 05 (feedback), 07 (implementation dignity), 11 (social investment frame)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `CPDS_Aug_2020.dta` | `data/raw/baccini_2024/Raw Data/` | ALMP spending % GDP, passive spending, employment rates | Country-year |
| `ELFS_regional_routine_shares.dta` | same | Regional labour market structure | Region-year |
| `RP_Context_Data.dta` | `data/raw/gingrich_2019/` | State-level ALMP responses to automation exposure | Key for Gingrich's policy context argument |

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| ALMP spending | ALMP % GDP | CPDS |
| Passive labour market spending | PLMP % GDP | CPDS |
| Active/passive ratio | calculated: ALMP/PLMP | CPDS |
| Regional labour market structure | routine employment shares | ELFS |
| Policy context (automation-specific) | ALMP per routine worker | RP_Context_Data.dta |

---

## 07: Welfare Design, Trust & Legitimacy

**Core construct:** How welfare is designed and delivered signals social worth. Procedural fairness matters most for already-dissatisfied citizens. Visibility of welfare can prime populist reactions (visibility-priming effect). CARIN criteria (Control, Attitude, Reciprocity, Identity, Need) drive deservingness judgments.

**Theory file:** `theory/07_welfare_design_trust_legitimacy.md`
**See also in theory:** modules 05 (feedback loop), 10 (moral economy elaboration), 11 (social investment approach)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `Baciini - ESSdata.dta` | `data/raw/baccini_2024/Raw Data/` | ESS trust variables + welfare attitudes | Large (599MB) — use sample |
| ESS CSVs (waves 1–9) | `data/raw/gugushvili_2025/` or `Public Data/ESS_csv/` | Trust variables, welfare support, satisfaction | |
| `ZA7700_v2-0-0-mv.dta` | `data/raw/steiner_left_behind/data_raw/` | ISSP social inequality module incl. welfare attitudes | Steiner's dataset |
| ISSP ZA-files | `data/raw/gingrich_2019/` | Welfare attitude modules | |

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| Trust in parliament | `trstprl` | ESS |
| Trust in politicians | `trstplt` | ESS |
| Trust in EU | `trstep` | ESS |
| Satisfaction with government | `stfgov` | ESS |
| Satisfaction with democracy | `stfdem` | ESS |
| Welfare attitudes (deservingness) | welfare attitude battery | ESS, ISSP ZA-files |
| Welfare chauvinism | immigration attitudes + welfare | ESS `imwbcnt`, `imueclt` |

---

## 08: Status, Recognition & Relative Position

**Core construct:** Economic status is zero-sum and relational. Status loss (relative decline) drives radical right support *independently* of material hardship. Cicollini (2025) operationalizes this with **positional income change** — the shift in an individual's income *rank* over time, controlling for absolute income level.

**Theory file:** `theory/08_status_recognition_theory.md`
**See also in theory:** modules 02 (automation as status threat), 09 (psychological elaboration), 12 (political outlet for status anxiety), 13 (synthesis)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `essprt-all.dta` | `data/raw/cicollini_2025/` | ESS with **positional income change** computed | **Key for status analysis** — Cicollini's constructed variable |
| `election_year_data.dta` | same | Country-election year data for merging | |
| ESS waves (Gugushvili) | `data/raw/gugushvili_2025/` | Intergenerational class position (ESS1–5) | Class mobility → status discordance |
| `correspondence.dta` | `data/raw/kurer_2020_declining_middle/
| `aspiration_apprehension_data.csv` | `data/raw/aspiration_apprehension/` | Aspiration vs. apprehension; occupational expectations | Tests anticipated vs. realised status change |

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| Positional income change | `posit_income_change` (constructed) | essprt-all.dta |
| Absolute income change | income level + change | ESS `hinctnta` |
| Intergenerational class mobility | father occupation vs. own occupation | Gugushvili ESS waves + correspondence.dta |
| Status discordance | expected vs. actual class position | aspiration_apprehension_data.csv |
| PRR voting | radical right party vote | ESS vote variables → party_classifications |
| Subjective class position | `subjclass` (where available) | ESS |

---

## 09: Ontological Security & Psychology

**Core construct:** Rapid economic and social change threatens stable identity. Existential anxiety — independent of political attitudes — creates vulnerability to populist fantasy narratives. Life dissatisfaction is a stronger predictor of populist attitudes than economic concerns alone. Loneliness creates desire for community → populist mobilization.

**Theory file:** `theory/09_ontological_security_psychology.md`
**See also in theory:** modules 08 (status anxiety), 12 (fantasy mobilization), 15 (cognitive frames)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `graphsdata.dta` | `data/raw/silva_wellbeing/
| `ZA7700_v2-0-0-mv.dta` | `data/raw/steiner_left_behind/data_raw/` | ISSP social inequality + wellbeing | Steiner left-behind analysis |
| `R_Plots_Data.csv` | `data/raw/steiner_left_behind/data_processed/` | Processed data for Steiner plots | |
| `Baciini - ESSdata.dta` | `data/raw/baccini_2024/Raw Data/` | ESS wellbeing variables + populist vote | Large — use sample |
| ESS waves | Various | `stflife`, `happy`, `atchctr`, `atcherp`, `sclact` | |

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| Life satisfaction | `stflife` | ESS |
| Happiness | `happy` | ESS |
| Attachment to country | `atchctr` | ESS |
| Attachment to Europe | `atcherp` | ESS |
| Social activity (loneliness proxy) | `sclact`, `sclmeet` | ESS |
| Subjective well-being index | composite | Silva graphsdata.dta |
| Anxiety / worry | `wrclmch` (worry about climate, proxy) | ESS |

---

## 10: Moral Economy, Deservingness & Welfare Chauvinism

**Core construct:** Producerism creates a moral divide between "productive workers" and "parasitic strata" above and below. CARIN criteria shape who is seen as deserving welfare. Status-anxious voters engage in "defensive othering" and "kicking down" — distancing themselves from even lower-status groups to protect their own social position.

**Theory file:** `theory/10_moral_economy_deservingness.md`
**See also in theory:** modules 07 (welfare design responds to these attitudes), 08 (status anxiety origin), 12 (populist exploitation)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `ZA7700_v2-0-0-mv.dta` | `data/raw/steiner_left_behind/data_raw/` | ISSP social inequality — welfare attitudes, fairness | Steiner dataset |
| `Euroscepticism...replication-1.dta` | `data/raw/euroscepticism_stagnation/
| ESS waves | Various | Immigration attitudes + welfare support battery | |
| ISSP ZA-files | `data/raw/gingrich_2019/` | Social inequality modules (ZA3090, ZA4950) | |

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| Welfare chauvinism | welfare for immigrants attitudes | ESS |
| Immigration attitudes (cultural) | `imueclt` (cultural enrichment) | ESS |
| Immigration attitudes (economic) | `imwbcnt` (good/bad for country) | ESS |
| Redistribution preferences | social inequality attitude battery | ISSP (ZA3090, ZA4950, ZA7700) |
| Deserving vs. undeserving | CARIN-related items | ZA7700 |
| Far-right voting | party vote → party family | ESS + party_classifications |

---

## 11: Social Investment Paradigm

**Core construct:** The alternative to passive compensation: capabilities-enhancing investment (education, childcare, active training) that addresses *both* material needs and status concerns. Predistribution preference: less-educated prefer job quality/wages; more-educated prefer redistribution. Social investment creates upward spirals of inclusive solidarity.

**Theory file:** `theory/11_social_investment_paradigm.md`
**See also in theory:** modules 05 (policy feedback), 06 (ALMP types), 07 (dignity in implementation)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `CPDS_Aug_2020.dta` | `data/raw/baccini_2024/Raw Data/` | Education spending, childcare, ALMP as % GDP | Country-year |
| ESS waves | Various | Skills preferences, education level, training participation | Individual |

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| Social investment spending | education + childcare + ALMP % GDP | CPDS |
| Skills investment preference | survey items on training/education | ESS |
| Education level | `eduyrs`, `eisced` | ESS |
| Predistribution vs. redistribution | job quality vs. income transfer preference | ESS attitude battery |

---

## 12: Populism & Right-Wing Mobilization

**Core construct:** Populist parties mobilize status-anxious and existentially insecure voters through nostalgic restoration fantasies and scapegoating. Key empirical task: measuring party-level populism and linking it to individual vote choice. Misattribution: automation anxiety → blamed on immigration/trade.

**Theory file:** `theory/12_populism_welfare_chauvinism.md`
**See also in theory:** modules 08 (status anxiety origin), 09 (psychological mechanism), 10 (moral economy), 15 (cognitive mediation)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `party_classifications.dta` | `data/raw/milner_2021/parties_votes/` | Party family (populist/far-right flag) | Join key: country + party name |
| `CLEA_voteshare_turnout.dta` | same | Constituency/national vote shares | |
| `parlgov_election_05202020.csv` | same | Election results + cabinet formation | ParlGov |
| `Global_Party_Survey_by_Party_Stata...dta` | `data/raw/baccini_2024/Raw Data/` | Expert survey of party positions incl. populism scale | |
| `MPDataset_MPDS2019b.dta` | same | Manifesto data — party ideology scores | |
| `partyfacts-core.csv` + `partyfacts-mapping.csv` | `data/raw/cicollini_2025/` | **Party ID crosswalk** across datasets | Essential for harmonising party IDs |
| `ess_populist_crosswalk.csv` | `data/raw/langenkamp_2022/` | ESS party vote codes → populist classification | Merge with ESS on cntry + essround |
| `view_party.csv` | `data/raw/cicollini_2025/` | Party view data | |
| `public_data_link_export_2021-09-28.csv` | same | Party facts public data export | |
| `Clean Data, February 2021.dta` | `data/raw/armaly_us/

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| Party populism score | populism scale (expert survey) | Global_Party_Survey |
| Far-right party family | party_family = far_right/populist | party_classifications.dta |
| Vote for populist party | ESS vote → crosswalk → populist flag | ESS + ess_populist_crosswalk.csv |
| Party manifesto position | RILE, welfare state position | MPDataset_MPDS2019b.dta |
| Party ID harmonisation | Partyfacts ID | partyfacts-core/mapping.csv |

---

## 13: Dual Pathway Synthesis & The Trilemma

**Core construct:** Economic vulnerability operates through *four* interconnected pathways — material (hardship → redistribution demand), status (relative decline → status remedies), temporal (anticipated vs. experienced), and institutional (welfare design → solidarity norms). No traditional policy can satisfy all three dimensions of the trilemma simultaneously; social investment is the proposed resolution.

**Theory file:** `theory/13_dual_pathway_synthesis.md`
**See also in theory:** all other modules — this is the synthesis

**Empirical implication:** To test the four-pathway model, you need a dataset that links individual-level economic vulnerability indicators (material + status + anticipated) with political outcomes, controlling for institutional context (welfare state type). The **Baccini analysis-ready files** are the best starting point.

### Primary Datasets (synthesis requires merging)

| Dataset | Path | Role in synthesis | Unit |
|---------|------|------------------|------|
| `individualdata.dta` | `data/raw/baccini_2024/Data/` | **Analysis-ready individual level** — material pathway | Individual |
| `districtdata.dta` | same | **Analysis-ready district level** — institutional pathway | District |
| `essprt-all.dta` | `data/raw/cicollini_2025/` | Status pathway — positional income change | Individual |
| `imputed_econdata_voteshare_merged.dta` | `data/raw/milner_2021/imputed/` | Regional economic pathway + vote outcomes | Region |
| `CPDS_Aug_2020.dta` | `data/raw/baccini_2024/Raw Data/` | Institutional context (welfare state type) | Country-year |

---

## 14: Mechanisms Catalog

This is a cross-cutting reference module. For each mechanism, the relevant datasets are documented in the corresponding thematic module above. See `theory/14_mechanisms_catalog.md` for the full list.

**Quick cross-reference:**
- Economic grievance activation → modules 01, 02, 03, 04 above
- Policy feedback (self-reinforcing / undermining) → module 05
- Status as zero-sum → module 08
- Identity switching → module 15
- Ontological insecurity → module 09
- ALMP type effects → module 06

---

## 15: Cognitive Frames, Belief Systems & Political Realignment

**Core construct:** Political responses to economic vulnerability are *cognitively mediated*. Automation anxiety gets misattributed to immigration (cognitive availability + political entrepreneurship). Identity switching (class → cultural identity) reduces redistribution demand. Meritocratic beliefs insulate high earners from inequality awareness through spatial segregation. Universalism vs. particularism is an emerging moral dimension that reorganizes the partisan landscape.

**Theory file:** `theory/15_cognitive_frames_belief_systems.md`
**See also in theory:** modules 02 (automation source), 04 (precarity source), 08 (status), 10 (moral economy), 12 (populist exploitation), 13 (synthesis)

### Primary Datasets

| Dataset | Path | Key variables | Notes |
|---------|------|---------------|-------|
| `essprt-all.dta` | `data/raw/cicollini_2025/` | ESS with positional income + ideology + immigration | Cicollini's key dataset |
| `aspiration_apprehension_data.csv` | `data/raw/aspiration_apprehension/` | Apprehension index, occupation, political attitudes | Tests misattribution |
| `Baciini - ESSdata.dta` | `data/raw/baccini_2024/Raw Data/` | ESS with economic + cultural attitudes | Large — use sample |
| `Euroscepticism...replication-1.dta` | `data/raw/euroscepticism_stagnation/
| `Clean Data, February 2021.dta` | `data/raw/armaly_us/

### Construct → Variable Mapping

| Theoretical construct | Variable | Dataset |
|----------------------|----------|---------|
| Immigration attitudes (cultural blame) | `imueclt`, `imwbcnt` | ESS |
| Trade attitude (unfair competition) | trade fairness items | ISSP ZA-files |
| Meritocratic beliefs | social mobility attitudes | ESS, ISSP |
| Universalism-particularism | moral orientation scale | ESS (constructed from items) |
| Identity (class vs. cultural) | class identity + cultural conservatism | ESS |
| EU attitudes (Euroscepticism) | `trstep`, EU attitude battery | ESS, Euroscepticism.dta |
| Populism attitudes (supply-side) | populism index | essprt-all.dta, Armaly |

---

## Cross-Dataset Merge Reference

The most common merge patterns across all modules:

| From | To | Join key(s) | Notes |
|------|----|------------|-------|
| ESS individual | isco08_3d-task3 (RTI) | `isco08_3d` (3-digit) | Truncate 4-digit ESS code |
| ESS individual | ess_populist_crosswalk | `cntry` + `essround` + party code | Party vote varies by country |
| ESS individual | party_classifications | `cntry` + party name | Needs party name harmonisation |
| ESS individual | partyfacts-mapping | Partyfacts ID | Via partyfacts crosswalk |
| ESS individual | essprt-all (Cicollini) | ESS individual ID or cntry+essround+idno | |
| ESS individual | correspondence (ISCO crosswalk) | `isco88` or `isco08` | For class scheme construction |
| Region-level | CLEA vote shares | NUTS2/country + election year | |
| Region-level | regional_gdp_by_year | NUTS2 + year | ARDECO |
| Country-year | CPDS | `cntry` + `year` | |
| Country-year | parlgov_election | country + election year | |

---

*Bridge auto-generated from theory modules + data dictionary on 2026-03-13. Update when new datasets added or theory modules revised.*
