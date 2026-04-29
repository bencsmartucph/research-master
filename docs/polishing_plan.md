# Polishing Plan & Research Extensions
## From Seminar Paper to Thesis

---

## Part I: Polishing the Seminar Paper (Next 2 Weeks)

### 1.1 Things to Fix Before Sending to Amalie

**Figures.** The current figures are functional but not publication-quality. Specific improvements:
- Figure 2 (sorting pattern): add confidence bands to the regression lines, use consistent y-axis range across panels, add a note explaining RTI is standardised
- Figure 6 (CWED vs. slopes): this is the paper's most striking visual — consider adding the ALMP version as a companion panel (6a: ALMP, 6b: CWED) to make the contrast visible in a single figure
- All figures: ensure consistent colour scheme, serif fonts, remove chart junk

**The Denmark paragraph.** Write the flexicurity discussion. DK's high generosity + steep slope is the most interesting outlier and needs 3–4 sentences in the empirical section explaining why it doesn't undermine the argument.

**R replication.** The Python statsmodels mixed models are diagnostic. Run the final specifications in R using lme4/lmerTest for the submitted version. The R code blocks are already written in the notebook — just execute them. This matters because lme4 uses REML estimation and handles random effects more flexibly.

**Reference list audit.** Several references in the current draft need verification: check that Wagner (2022, 2023), Stutzmann (2025), and Pelc (2025) have correct years and titles. Some may be working papers with updated publication details.

**Proofread for voice consistency.** The theory sections are in your voice. Some of the empirical prose still reads more like the Claude voice than yours — especially the limitations section and parts of the discussion. Read aloud and rewrite anything that sounds too careful or hedged.

### 1.2 Low-Effort Model Extensions (Can Do This Week)

These require no new data — just additional specifications on the existing dataset.

| Extension | What it tests | Effort | Priority |
|-----------|---------------|--------|----------|
| CWED sub-components | Run Model 3 separately with unemployment generosity, sickness generosity, pension generosity instead of composite. Which dimension drives the result? | 30 min | High — tells you which specific decommodification channel matters |
| Wave-by-wave stability | Run Model 2 separately for each ESS round. Is the RTI × Liberal interaction stable across 2012/2014/2016/2018 or does it strengthen over time? | 30 min | Medium — referee will ask |
| Gender interaction | RTI × Liberal × female. Is the sorting mechanism stronger for men? The theory (status anxiety, masculine work identity) predicts it should be. | 30 min | Medium — theoretically motivated |
| Subjective insecurity as alternative IV | Replace RTI with `emplno` (perceived unemployment risk). If the interaction holds with subjective vulnerability, the mechanism isn't specific to automation. | 20 min | Medium — broadens the claim |
| Individual CWED model with controls for GDP/immigration | Add GDP per capita and immigrant stock (% foreign-born) as country-level controls alongside CWED. If the CWED interaction survives, it's not just picking up wealth or immigration exposure. | 30 min | High — most obvious confounder |
| Decompose anti-immigration index | Run Model 2 separately for each component: imwbcnt (general), imueclt (cultural), imbgeco (economic). Does the sorting mechanism operate more through cultural or economic immigration concerns? | 20 min | Medium — theoretically interesting |

### 1.3 Data You Could Add Quickly

| Data source | What it adds | Access | Effort |
|-------------|-------------|--------|--------|
| Chapel Hill Expert Survey | Party-level positions on economic and cultural dimensions — allows classifying radical right parties more precisely | chesdata.eu, free | 1–2 hours to merge |
| OECD Social Expenditure (SOCX) | Disaggregated social spending by function — separates education spending from unemployment spending from healthcare | stats.oecd.org, free | 1–2 hours to download and merge |
| Eurostat immigration data | Country-level immigrant stock and flow data — controls for immigration salience | ec.europa.eu/eurostat, free | 1 hour |
| ESS Round 10 (2020/21) | Post-COVID observations — tests whether the sorting mechanism held during an unprecedented economic shock | europeansocialsurvey.org | 2–3 hours to download, clean, merge |
| ESS Round 4 (2008) welfare attitudes module | Additional wave with deservingness items — would double the H3 mediation sample | Already in repo (waves 1–5 CSVs) but needs ISCO crosswalk | 3–4 hours if using the crosswalk carefully |

---

## Part II: Extensions for the Thesis (Next Semester)

### 2.1 The Causal Identification Project (Highest Priority)

**The problem:** The seminar paper establishes a cross-national association between welfare decommodification and the vulnerability-to-exclusion slope. But this association is confounded by everything else that differs across countries. The thesis needs within-country, ideally within-person, causal evidence.

**The Danish registry design:**

Denmark's administrative registers link individual employment histories, welfare contact records, and municipal-level service data. Combined with survey data on political attitudes (either the Danish National Election Study or ESS Denmark), this enables designs that the cross-national analysis cannot:

*Design A: Welfare contact as treatment.* Compare political attitudes before and after individual welfare contact events (job loss → activation programme entry). If the sorting mechanism operates through welfare experience, attitudes should shift more toward exclusion after contact with punitive activation and less (or toward solidarity) after contact with enabling programmes. This requires linking register-based welfare contact records to survey-based attitude measures — feasible if CEBI can provide the data linkage.

*Design B: Municipal variation in implementation quality.* Danish municipalities vary in how they implement national activation policies — some emphasise sanctions, others emphasise counselling and support. If the sorting mechanism operates through implementation quality, municipalities with more punitive implementation should show stronger vulnerability-to-exclusion slopes. This is a natural experiment if you can measure municipal implementation variation.

*Design C: Reform-based quasi-experiment.* Denmark has introduced several activation reforms over the past two decades (2003 "More People to Work," 2006 Welfare Agreement, 2013 reform of cash benefits). If the sorting mechanism operates as theorised, reforms that increased conditionality should have shifted the vulnerability-to-exclusion slope upward, while reforms that increased enabling support should have flattened it. A difference-in-differences or event study design around these reforms could provide causal evidence.

**Talk to Amalie about data access.** She works at CEBI and knows the Danish register landscape. The thesis design depends entirely on what data linkages are feasible. Bring the specific question — "can we link individual welfare contact records to political attitude measures?" — to your next meeting.

### 2.2 The Place-Based Extension

The seminar paper operates at the individual level. The thesis could add a community-level analysis testing whether the sorting mechanism operates through local welfare infrastructure degradation as well as individual welfare contact.

**Design:** Using Danish municipal data, test whether municipalities that have experienced welfare service cuts (fewer caseworkers per capita, Jobcentre closures, longer waiting times) show stronger vulnerability-to-exclusion slopes than municipalities with maintained service quality. This requires municipal-level data on welfare service provision linked to individual-level ESS or DNES data.

**Connection to the literature:** This directly tests the "welfare cascade" hypothesis — that welfare institutional quality operates at the community level, not just the individual level. It would connect the individual-level sorting mechanism to Bolet's (2021) community-degradation findings and Broz et al.'s argument about the politics of place.

### 2.3 The Australia Comparison

A structured Denmark-Australia comparison would provide the strongest possible counterfactual for the sorting mechanism. Two wealthy democracies at opposite ends of the welfare regime spectrum, both experiencing automation and globalisation, but with very different institutional contexts mediating the political response.

**Data:** The Australian data landscape is more limited than the Danish one. The Household, Income, and Labour Dynamics in Australia (HILDA) survey has employment history and some political attitude measures. The Australian Election Study has detailed political variables. Neither has the register-level welfare contact data that Danish data provides.

**Feasibility:** This is probably a standalone paper rather than a thesis chapter. The cross-national comparison would rely on survey data from both countries, with the Danish register analysis providing the causally identified evidence and the Australian comparison providing external validity.

### 2.4 The Deservingness Deep Dive

The seminar paper's H3 (mediation through deservingness) produced weak and partially unexpected results — RTI was associated with slightly *less* restrictive deservingness views, not more. This may reflect measurement issues (the ESS deservingness items are limited) or genuine theoretical complexity (automation-exposed workers may have more empathy for others facing economic difficulty).

**Extension:** Use the dedicated ESS welfare attitudes module (Rounds 4 and 8) with the full battery of deservingness items, combined with the CWED welfare indicators, to test whether welfare institutional context moderates how economic vulnerability shapes deservingness perceptions. The specific prediction: conditional welfare should narrow deservingness boundaries among the economically vulnerable, while universal welfare should maintain broader boundaries.

**Data:** Already partially in the repo. Round 8 has the welfare attitudes module and ISCO-08. Round 4 has the module but requires the ISCO-88 crosswalk.

### 2.5 The Supply Side

The seminar paper focuses entirely on the demand side: how welfare institutions shape citizens' preferences. But the supply side matters. Radical right parties actively construct narratives channelling economic anxiety into cultural politics. The interaction between institutional demand-side effects and party supply-side framing is undertheorised.

**Extension:** Merge Chapel Hill Expert Survey party positions with the ESS data to test whether the sorting mechanism is stronger in countries where radical right parties are more electorally successful (supply available) or where mainstream parties have adopted exclusionary positions (supply mainstreamed). This would partially address the radical right vote puzzle from Model 6 (Liberal regimes produce exclusionary attitudes but lack radical right party supply).

### 2.6 The Longitudinal Dimension

The seminar paper uses repeated cross-sections (ESS waves 6–9). A longitudinal extension would track whether the sorting mechanism has strengthened over time as welfare conditionality has increased across European countries.

**Design:** Use all available ESS rounds (1–10) with the welfare regime interaction, testing whether the RTI × Liberal (or RTI × CWED) coefficient has grown over the 2002–2021 period. This requires solving the ISCO-88/ISCO-08 crosswalk problem for early rounds — worth the effort if it produces a time trend showing the sorting mechanism intensifying alongside welfare retrenchment.

---

## Part III: The Meeting with Amalie

### What to bring:
1. The paper draft (v3)
2. Figure 6 (CWED vs. slopes) — printed, in colour. This is the figure that makes the argument visually.
3. A one-page summary of the thesis designs (2.1 above) to discuss data access

### What to ask:
1. Does the CWED finding convince her, or does she see confounders I'm missing?
2. Which thesis design (A, B, or C) does she think is most feasible with CEBI data access?
3. Does she see the connection to her Ballard-Rosa et al. paper the way I do — and does she think the upstream institutional mechanism is a viable extension of their framework?
4. Would she be interested in supervising a thesis that builds on this paper's framework with Danish registry data?

### What NOT to do:
- Don't apologise for last year. You've already addressed it. Show up with the work.
- Don't present everything you've read. Present the argument, the finding, and the plan.
- Don't ask permission to pursue the project. Ask for feedback on a project you're already pursuing.

---

## Timeline

| When | What |
|------|------|
| This week | Run the low-effort model extensions (1.2). Fix figures. Proofread. |
| Next week | R replication of main models. Add GDP/immigration controls to Model 3. |
| Week 3 | Submit seminar paper. |
| Week 3–4 | Meet Amalie with draft + thesis proposal. |
| Weeks 5–8 | Explore Danish data access. Begin thesis proposal. |
| Next semester | Thesis: causal identification using Danish registry data. |

---

*Do not use the buffer time for more reading. The reading is done.*
