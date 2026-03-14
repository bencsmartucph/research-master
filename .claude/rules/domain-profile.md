# Domain Profile: Political Economy / Comparative Politics
# Calibrates all agents to Ben Smart's dissertation research

---

## Researcher
- **Name:** Ben Smart (bencsmart@gmail.com)
- **Degree:** PhD — Political Economy / Comparative Politics
- **Institution:** UCL (Economics of the Welfare State group)
- **Dissertation focus:** How economic disruption (automation, trade, austerity, occupational decline) shapes populist political behaviour in Europe, and what welfare state design can do about it
- **Stage:** Early ideation — building theoretical framework and empirical infrastructure before committing to a chapter

---

## Field & Adjacent Subfields
- Comparative political economy
- Welfare state politics
- Electoral behaviour / political sociology
- Labour economics (as it intersects with politics)
- Economic geography (place-based politics)

---

## Target Journals (ranked by tier)
| Tier | Journal | Notes |
|------|---------|-------|
| 1 | American Political Science Review (APSR) | Methods rigour + theoretical contribution |
| 1 | American Journal of Political Science (AJPS) | Causal identification prioritised |
| 1 | Comparative Political Studies (CPS) | Cross-national comparative work |
| 2 | European Journal of Political Research (EJPR) | European focus welcome |
| 2 | British Journal of Political Science (BJPS) | Methods + substance balance |
| 2 | Political Science Research & Methods (PSRM) | Methods-forward papers |
| 2 | West European Politics (WEP) | European cases, welfare state |
| 3 | Journal of European Social Policy (JESP) | Policy-oriented findings |
| 3 | Socio-Economic Review (SER) | CPE, labour market, welfare |

---

## Common Identification Strategies (in this literature)
- **Difference-in-differences:** Policy shocks (austerity cutbacks, benefit reforms); regional exposure (Baccini 2024 design)
- **Shift-share / Bartik IV:** Trade exposure (China shock à la Autor/Dorn/Hanson); automation exposure by regional occupational mix
- **Panel fixed effects:** Individual panel data (SOEP, BHPS, SHP); ESS repeated cross-sections with country × wave FE
- **Regression discontinuity:** Electoral thresholds; programme eligibility cutoffs
- **Mediation / causal mechanisms:** Baron-Kenny or structural equation models for status anxiety pathways
- **Cross-national comparative:** Most-similar / most-different systems logic; welfare regime typologies

---

## Seminal References (referee will expect these)
- Iversen & Soskice (2001) — varieties of capitalism, insider/outsider
- Oesch (2006, 2013) — class schema, occupational structure
- Mudde (2004, 2007) — populism as thin ideology, demand-side
- Autor, Dorn & Hanson (2013, 2016) — China shock, routine task hypothesis
- Gingrich & Häusermann (2015) — welfare state politics, distributive coalitions
- Kurer (2020) — declining middle, anticipatory status decline
- Baccini, Pinto & Weymouth (2024) — austerity and populism
- Im, Mayer, Palier & Rovny (2019) — radical right vote reservoir
- Oesch & Rennwald (2018) — electoral realignment, new cleavage
- Kriesi et al. (2008, 2012) — globalisation cleavage
- Norris & Inglehart (2019) — cultural backlash thesis

---

## Common Data Sources (this research programme)
| Dataset | Key use | Location |
|---------|---------|----------|
| European Social Survey (ESS) waves 1–9 | Individual-level political attitudes, vote choice | `data/raw/baccini_2024/`, `data/raw/im_2021/` |
| ISSP ZA-file series | Automation perceptions, occupational context | `data/raw/gingrich_2019/` |
| ISCO-08 task scores | Routine Task Intensity (RTI), automation exposure | `data/raw/shared_isco_task_scores/` |
| Cicollini ESS positional income | Positional income change measure | `data/raw/cicollini_2025/` |
| Milner regional trade data | Trade exposure, regional economic geography | `data/raw/milner_2021/` |
| Baccini austerity data | District-level austerity cuts + ESS merge | `data/raw/baccini_2024/` |
| CPDS (Comparative Political Data Set) | ALMP spending, welfare regime vars | `data/raw/baccini_2024/Raw Data/` |
| NUTS2/3 regional panels | Regional GDP, unemployment, far-right vote share | `data/raw/milner_2021/` |

---

## Field Conventions
- **Unit of analysis:** Usually individual-level (ESS) with country × wave FE; sometimes district/regional
- **Standard controls:** Age, gender, education (ISCED), household income (decile), employment status, union membership, country FE, wave FE
- **Clustering:** Standard errors clustered at country-wave level (or region for regional analyses)
- **Outcome variable:** Usually a binary or ordinal populist/radical-right vote indicator, or attitude scales (immigration, EU, redistribution)
- **Occupational coding:** Always document whether ISCO-88 or ISCO-08; truncation from 4-digit to 3-digit when merging task scores
- **Party coding:** Use Global Party Survey (GPS) scores or Chapel Hill Expert Survey (CHES) — always cite the version year
- **Welfare regimes:** Esping-Andersen (1990) three-worlds as baseline; Ferrera (1996) for Southern Europe

---

## Referee Concerns (the questions they always ask)
1. **Causality:** "Is this causal or correlational? What is the identification strategy?"
2. **Ecological fallacy:** "Are you inferring individual attitudes from regional economic data?"
3. **Reverse causality:** "Could populist voting drive economic outcomes rather than the other way?"
4. **Measurement validity:** "How are you measuring 'populism'? Is this a demand- or supply-side story?"
5. **Selection into occupation:** "Do people sort into routine/automatable jobs for reasons correlated with political preferences?"
6. **Cross-national equivalence:** "Are your measures comparable across ESS country-waves?"
7. **The cultural vs. economic debate:** "Norris & Inglehart argue this is cultural backlash — how do you respond?"
8. **Heterogeneity:** "Does the effect vary by welfare regime type? That's where the institutional argument lives."

---

## Notation Conventions
- Treatment indicators: D_i or D_{it}
- Outcome: Y_{it}
- Country fixed effects: α_c
- Wave fixed effects: λ_t
- Standard: β for main coefficient of interest, always report 95% CI alongside p-values
- Table format: Coefficient + SE in parentheses, stars at 0.10 / 0.05 / 0.01

---

## Anti-Patterns to Avoid
- Do NOT use `Good Data/` folder — always use `data/raw/` in Research_Master
- Do NOT reconstruct `posit_income_change` — it is pre-built in Cicollini's `essprt-all.dta`
- Do NOT treat ESS as panel data — it is repeated cross-sections (exception: rotating panel component in some waves)
- Do NOT merge on 4-digit ISCO-08 to task scores — truncate to 3-digit first (`isco08 // 10`)
- Do NOT use ISSP value codes without decoding `meta.variable_value_labels`
