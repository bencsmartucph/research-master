# Four Claude Code Prompts — Next Phase
# Each prompt is for a FRESH session. Attach the listed files with each.

---
---

# PROMPT 1: ECONOMETRIC REVIEW
# Fresh session. Attach: MEMORY.md, CLAUDE.md, final_analysis_report.md, final_results.json, paper_draft_v3_final.md

---

## Context

You are an econometric methods referee reviewing a seminar paper by a Master's student at the University of Copenhagen. The paper argues that welfare institutions "sort" economic disruption into solidarity or scapegoating, and tests this with ESS cross-national data. The student's supervisor is Amalie Jensen (co-author of Ballard-Rosa, Jensen & Scheve 2022 in ISQ).

The analysis pipeline is at `C:\Users\PKF715\Documents\claude_repos\Research_Master\analysis\final_analysis_pipeline.py`
The master dataset is at `analysis/sorting_mechanism_master_v2.csv`
The results are in `analysis/final_results.json`

## Your task

Act as a hostile but constructive econometric referee. Your job is to find every methodological weakness before a real referee does. Produce a detailed review document saved to `analysis/econometric_review.md`.

## Specific things to investigate

### 1. Identification
- The paper claims welfare institutions moderate the RTI→exclusion link. What are the three strongest alternative explanations for the RTI × welfare regime interaction? For each: how would you test for it, and can it be tested with the existing data?
- The CWED generosity correlation (r=-0.848, N=15) is eye-catching. Run influence diagnostics: what happens if you drop GB? Drop NO? Drop both? Cook's distance for each country. If removing one or two countries kills the result, flag it.
- The country-level correlation conflates welfare generosity with GDP, immigration levels, inequality, ethnic heterogeneity, and a dozen other things. Can you add country-level controls (GDP per capita, Gini, immigrant stock as % population) and see if the CWED interaction in Model 3 survives?

### 2. Specification
- Load the actual data and re-estimate Model 2 yourself. Verify the coefficients match final_results.json. If they don't, document the discrepancy.
- Check whether the random intercept specification is appropriate. Run a likelihood ratio test comparing random intercept vs. random slope (allowing the RTI slope to vary by country). If random slopes are needed, the current Model 2 is misspecified.
- Test for multicollinearity between RTI and the control variables (especially education — high RTI workers tend to have lower education). Compute VIFs. If VIF > 5, flag it.
- Check the functional form of RTI. Is the relationship with anti-immigration linear, or is there a nonlinear pattern (quadratic, threshold)? Plot residuals vs. fitted values.

### 3. Standard errors
- Are the standard errors appropriate? With country-wave clusters of very different sizes (Nordic ~6K per wave, Eastern ~13K), check whether clustered SEs at the country level change the inference. Compare: (a) mixed model SEs, (b) OLS with country-wave FE and robust SEs, (c) OLS with country-clustered SEs.
- With only 2 Liberal regime countries (GB, IE), how reliable is the RTI × Liberal interaction? The effective degrees of freedom for this interaction are very low. Flag this as a limitation and compute the wild cluster bootstrap p-value if feasible.

### 4. Sample and measurement
- Check for compositional effects: is the RTI distribution the same across regimes, or do Liberal regime countries have systematically different occupational structures? If Liberal countries have more high-RTI workers, the interaction could reflect a nonlinear RTI effect rather than institutional moderation.
- Check whether the anti-immigration index behaves the same across countries. Run Cronbach's alpha separately by regime. If the index has different reliability in different contexts, the cross-regime comparison is complicated.
- What percentage of the sample is missing on each control variable? If missingness is non-random (e.g., more missing income data in Eastern Europe), the complete-case analysis may be biased. Suggest a sensitivity analysis.

### 5. The ALMP vs. CWED contrast
- The paper makes much of the contrast between ALMP (positive r) and CWED (negative r). But these are measured on different samples (22 vs. 15 countries). Run both correlations on the OVERLAPPING sample of countries. Does the contrast hold on the same set of countries?

### 6. Honest overall assessment
At the end, provide:
- A 1-paragraph "referee verdict": would this pass at a good field journal (EJPR, CPS, JEPS) as a Master's-level contribution? What's the single biggest threat to the main finding?
- A ranked list of the 5 most important things to fix before submission
- A ranked list of 3 things a referee would praise

## Rules
- Load and verify the actual data — don't trust the reported numbers
- Be specific: when you flag a problem, show the diagnostic output
- Distinguish between fatal problems (the result may be wrong) and presentation issues (the result is fine but needs better framing)
- Save all diagnostic outputs, plots, and tables to `analysis/review_diagnostics/`
- Be harsh but fair. The student wants to know the truth.

---
---

# PROMPT 2: PUBLICATION FIGURES + CREATIVE VISUALISATIONS
# Fresh session. Attach: MEMORY.md, final_analysis_report.md, paper_draft_v3_final.md

---

## Context

You are a data visualisation specialist creating publication-ready figures and exploring creative alternatives for a political economy seminar paper. The paper argues that welfare institutions sort economic disruption into exclusionary vs. solidaristic politics. The key finding is that CWED welfare generosity explains 72% of cross-country variation in how automation exposure converts into anti-immigration attitudes (r=-0.848).

Repo: `C:\Users\PKF715\Documents\claude_repos\Research_Master`
Data: `analysis/sorting_mechanism_master_v2.csv`
Results: `analysis/final_results.json`
Existing figures: `outputs/figures/`

## Task A: Polish Existing Figures

Remake all 5 figures (fig2–fig6) at publication quality. Requirements:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

REGIME_COLORS = {
    'Nordic': '#2166AC',
    'Continental': '#67A9CF',
    'Liberal': '#D6604D',
    'Southern': '#F4A582',
    'Eastern': '#B2ABD2',
}
```

Specific improvements for each figure:
- **Figure 2 (sorting pattern):** Add 95% CI shading around regression lines. Consistent y-axis across panels. More bins (15–20). Panel titles without "(N=...)": put N in a subtle annotation inside each panel.
- **Figure 3 (marginal effects):** Add individual country points behind the regime bars (jittered). This shows within-regime variation while maintaining the regime summary.
- **Figure 4 (education):** Consider a slope-comparison format: paired bars (non-college, college) for each regime, with connecting lines showing the reduction. Or a Cleveland dot plot.
- **Figure 5 (robustness):** Add the jackknife range as a shaded band behind the individual specification points. Label each specification clearly.
- **Figure 6 (CWED vs. slopes):** This is the paper's hero figure. Polish heavily: add the ALMP version as a companion panel (side by side: left = ALMP, right = CWED) so the contrast is visible at a glance. Different marker sizes by sample size. Clean country labels that don't overlap.

Save polished versions to `outputs/figures/polished/` as both PDF and PNG at 300 DPI.

## Task B: Creative / Alternative Visualisations

Explore alternatives that might communicate the findings more powerfully. These are experimental — not all will work. Save anything interesting to `outputs/figures/experimental/`.

Ideas to try:

1. **The "sorting funnel" diagram.** A conceptual figure showing the causal chain: Economic Disruption → [Welfare Institutional Context] → Solidarity OR Scapegoating. Not a data figure — a theoretical diagram using SVG/matplotlib. Think of it as Figure 1 in the paper.

2. **Slope map of Europe.** A choropleth map where each country is coloured by its RTI→anti-immigration slope. If you can get a European shapefile (geopandas + naturalearth_lowres), this would show the geographic pattern strikingly: dark red for GB, lighter for Continental, blue for Nordic.

3. **The ALMP-to-CWED transformation.** An animated or side-by-side figure showing the same countries in the same positions but with the x-axis changing from ALMP spending to CWED generosity — and the fit line rotating from positive to negative. This is the paper's "aha" moment visualised.

4. **Individual country trajectory lines.** For the 4–5 most theoretically important countries (GB, DK, DE, SE, NO), show RTI vs. anti-immigration as individual regression lines on the same axes, colour-coded by regime. This would make the UK's steep slope visually immediate compared to Norway's flat one.

5. **Marginal effects with CWED as continuous moderator.** A Johnson-Neyman plot: x-axis = CWED generosity, y-axis = marginal effect of RTI on anti-immigration, with a shaded region where the effect is significant. This shows at what level of welfare generosity the sorting mechanism "turns on."

6. **The recursive loop diagram.** A circular/feedback diagram showing: Conditional Welfare → Damaged Self-Concept → Identity Switching → Misattribution → Othering → Support for Further Conditionality → back to start. Could be done as a circular flow chart.

## Rules
- Prioritise Tasks A over B — polished versions of existing figures are more important than experimental ones
- For the hero figure (Figure 6), try at least 3 different layouts and save all of them
- All text on figures should be legible at A4 print size
- No gridlines on scatter plots. Minimal gridlines on bar charts.
- Country labels should never overlap — use adjustText or manual positioning
- Save everything to the appropriate subfolder

---
---

# PROMPT 3: LOW-EFFORT MODEL EXTENSIONS
# Fresh session. Attach: MEMORY.md, CLAUDE.md, final_analysis_report.md, final_results.json

---

## Context

You are extending the empirical analysis for a seminar paper on welfare institutions and the political consequences of automation. The main finding is established: RTI × Liberal interaction = 0.117 (p<0.001) and RTI × CWED generosity interaction = -0.056 (p<0.001). Now we need to run additional specifications that a referee would request.

Repo: `C:\Users\PKF715\Documents\claude_repos\Research_Master`
Data: `analysis/sorting_mechanism_master_v2.csv`
Pipeline: `analysis/final_analysis_pipeline.py`

## Extensions to run

For each extension: run the model, save the results to `analysis/extensions/`, and write a 2–3 sentence interpretation. At the end, produce `analysis/extensions/extensions_summary.md` with all results.

### Extension 1: CWED Sub-Components
Run Model 3 (RTI × welfare indicator) separately with:
- Unemployment insurance generosity only
- Sickness insurance generosity only
- Pension generosity only
Which specific dimension of decommodification drives the result? This tells us whether the mechanism is about labour market decommodification specifically or about the welfare state's general character.

### Extension 2: Wave-by-Wave Stability
Run Model 2 (RTI × regime) separately for each ESS round (6, 7, 8, 9). Report the RTI × Liberal coefficient for each wave. Is the sorting mechanism stable, strengthening, or weakening over 2012–2018? Produce a simple line plot showing the coefficient over time with CIs.

### Extension 3: Gender Interaction
Run: `anti_immig ~ RTI × regime × female + controls + (1|cntry_wave)`
Is the sorting mechanism stronger for men? The theory predicts it should be (masculine work identity, status anxiety channelled through gender). Report RTI × Liberal separately for men and women.

### Extension 4: Subjective Insecurity as Alternative IV
Replace RTI with `emplno` (perceived unemployment risk). Run Model 2 with this alternative vulnerability measure. If the regime interaction holds with subjective insecurity, the mechanism isn't specific to automation — it's about economic vulnerability more broadly. This broadens the paper's claim.

### Extension 5: Country-Level Confounders
Add to Model 3 (RTI × CWED) as country-level controls:
- GDP per capita (you'll need to construct this — check if it's in the CPDS data already merged, or use a simple classification: high/medium/low GDP)
- If immigrant stock data is available in any merged dataset, include it
- If Gini coefficient is available, include it
Run Model 3 with these controls added. Does the RTI × CWED interaction survive? This is the most important robustness check because the biggest confounder concern is that CWED correlates with wealth/development.

### Extension 6: Decompose Anti-Immigration
Run Model 2 separately with each component of the anti-immigration index as DV:
- `imwbcnt_rev` (immigrants make country worse/better — general)
- `imueclt_rev` (undermine/enrich cultural life — cultural dimension)
- `imbgeco_rev` (bad/good for economy — economic dimension)
Does the sorting mechanism operate more through cultural or economic anti-immigration sentiment? This is theoretically important: the identity-switching theory predicts cultural concerns should dominate.

### Extension 7: Nonlinear RTI Effects
Add RTI² to Model 1 (baseline). Is the relationship between RTI and anti-immigration attitudes nonlinear? If there's a threshold effect (the relationship steepens at high RTI), this matters for interpretation — it means the sorting mechanism is concentrated among the most automation-exposed workers.

## Output format

For each extension, produce:
1. A results table (coefficients, SEs, p-values, N)
2. A 2–3 sentence interpretation
3. Any relevant diagnostic plot

Compile into `analysis/extensions/extensions_summary.md` with clear section headers.

## Rules
- Use the same model specification as the main analysis (same controls, same random effects structure) unless the extension specifically requires a change
- Validate that your baseline replication matches the reported results before running extensions
- If any extension fails to converge, note it and try an OLS with clustered SEs as fallback
- Don't interpret non-significant results as "no effect" — note power considerations
- Be honest about what each extension shows, even if it complicates the story

---
---

# PROMPT 4: NEW DATA EXPLORATION (For Next Week)
# Fresh session. Attach: MEMORY.md, CLAUDE.md, paper_draft_v3_final.md, polishing_plan.md

---

## Context

You are exploring new datasets that could strengthen a seminar paper on welfare institutions and the political consequences of automation. The paper's main finding is that CWED welfare generosity moderates how automation exposure converts into anti-immigration attitudes (RTI × CWED = -0.056, p<0.001). We want to add country-level controls that address the most obvious confounders, and explore whether additional data sources could sharpen the analysis.

Repo: `C:\Users\PKF715\Documents\claude_repos\Research_Master`
Existing data: `analysis/sorting_mechanism_master_v2.csv`

## Task 1: Download and Profile New Datasets

The following are all freely available. Download each, profile it (columns, coverage, sample), and assess its value for the paper. Save everything to `data/raw/new_downloads/`.

### 1a. Chapel Hill Expert Survey (CHES)
- URL: https://www.chesdata.eu/ches-europe
- Download the trend file (1999–2019)
- We need: party-level radical right classification, party positions on immigration, economic left-right
- Profile: which ESS countries × waves have CHES party data? How many parties per country?
- Assess: can we construct a better radical right vote variable than the Langenkamp crosswalk?

### 1b. OECD Social Expenditure (SOCX)
- URL: https://stats.oecd.org → Social Protection → Social Expenditure
- Download: total social expenditure and sub-categories (old age, survivors, incapacity, health, family, ALMP, unemployment, housing, other) as % GDP
- Profile: country × year coverage, overlap with ESS sample
- Assess: does disaggregated spending tell a different story than CWED generosity? Specifically, does the composition of spending (% on active vs. passive, % on education vs. transfers) predict RTI→exclusion slopes?

### 1c. Eurostat Migration Data
- URL: https://ec.europa.eu/eurostat/data/database → Population → International migration
- Download: immigrant stock as % of population, by country and year
- Profile: coverage overlap with ESS
- Assess: is immigration level a confounder? Countries with more immigrants may have both more anti-immigration sentiment AND different welfare states. Adding immigrant stock as a control in Model 3 addresses this.

### 1d. World Inequality Database (WID) or Eurostat Gini
- URL: https://wid.world or Eurostat income distribution
- Download: Gini coefficient by country and year
- Assess: inequality as a confounder. More unequal countries may have both steeper RTI→exclusion slopes and less generous welfare. Controlling for Gini in Model 3 tests whether the CWED finding is really about welfare or about inequality.

### 1e. ESS Round 10 (2020/21)
- URL: https://www.europeansocialsurvey.org
- Check: is it downloadable as CSV? What countries are included?
- Assess: would adding post-COVID data strengthen or complicate the analysis? The pandemic produced a massive economic shock with extensive government intervention — it could be a natural test of the sorting mechanism under extreme conditions, or it could confound everything because COVID-era welfare was historically unusual.

**For each dataset:** if download is straightforward, download it. If it requires registration or complex navigation, document the URL and exact steps needed so Ben can do it manually. Don't spend more than 15 minutes trying to download any single dataset.

## Task 2: Merge and Test Confounders

Once you have country × year data on immigrant stock and Gini:

1. Merge onto the existing master dataset by country × year
2. Rerun Model 3 (RTI × CWED generosity + controls + new country-level controls)
3. Report: does the RTI × CWED interaction survive after controlling for immigrant stock, GDP, and inequality?
4. Also: run the country-level correlation (CWED vs. RTI slopes) controlling for these variables using partial correlations

This is the single most important robustness check for the paper. If CWED generosity is just proxying for "rich, equal, low-immigration Nordic countries," the theoretical interpretation is undermined.

## Task 3: Explore CHES for Radical Right Classification

If CHES data is downloaded:
1. Identify radical right parties using the `family` variable (typically coded as family=70 or similar) OR using the `galtan` score > 7 + `lrecon` < 5 (economically centrist/left but culturally authoritarian)
2. Merge onto ESS party vote data via party name × country × year
3. Construct improved `radical_right_vote` binary variable
4. Rerun Model 6 (radical right vote ~ RTI × regime) with the improved classification
5. Report: does the better classification change the Model 6 results? Specifically, does it resolve the UK/Ireland supply-side problem?

## Task 4: Assessment Report

Produce `analysis/new_data_assessment.md` containing:

1. **Data inventory:** What was downloaded, what wasn't, what needs manual download
2. **Confounder test results:** Does Model 3 survive the new controls?
3. **Partial correlation:** CWED vs. slopes controlling for GDP, immigration, inequality
4. **CHES assessment:** Is the radical right classification better? Does it change results?
5. **ESS Round 10 assessment:** Worth adding or not?
6. **Recommendations:** Which new data sources should be incorporated into the final paper, and which are better saved for the thesis?

## Rules
- Profile before merging — always check country codes match before attempting joins
- If a download fails or requires registration, document and move on
- The confounder test (Task 2) is the highest priority — if you only finish one task, finish that one
- Don't modify the existing master dataset — create a new version if adding variables
- Be honest: if the new controls weaken the CWED finding, say so clearly

---
---

# END OF PROMPTS
