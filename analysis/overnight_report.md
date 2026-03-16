# Overnight Report — Sorting Mechanism Analysis

**Date:** 2026-03-16
**Script:** `analysis/run_sorting_mechanism.py` + `analysis/fix_plots_ab.py`

---

## 1. What Ran Successfully

| Section | Status | Detail |
|---------|--------|--------|
| 1. Load ESS Data | SUCCESS | 188,764 obs from waves 6–9, 34 countries |
| 2. Merge RTI | SUCCESS | 87.8% match rate, N=165,667 with RTI scores |
| 3. Construct DVs | SUCCESS | Anti-immig index (alpha=0.864), redistribution, deservingness (wave 8) |
| 4. Clean Controls | SUCCESS | Age, gender, education, income, urban, L-R scale |
| 5. Welfare Indicators | SUCCESS | CPDS merged, 40.7% match (22 countries with ALMP data) |
| 5b. Regime Classification | SUCCESS | Nordic/Continental/Liberal/Southern/Eastern + Other |
| 6a. Plot A (RTI vs anti-immig) | SUCCESS | Fixed after initial grid layout bug; all 5 regimes plotted |
| 6b. Plot B (RTI vs redistribution) | SUCCESS | Fixed after initial grid layout bug; all 5 regimes plotted |
| 6c. Plot C (welfare vs slopes) | SUCCESS | Country-level ALMP vs RTI-attitude slopes |
| 7. Summary Statistics | SUCCESS | By regime, saved as CSV |
| 8. Diagnostic Models | SUCCESS | Mixed models for H1 and H2 converged |
| 9. Exploration | SUCCESS | Education moderator, within-regime variation, deservingness correlations |
| 10. Save Outputs | SUCCESS | Master CSV (188,764 x 37), codebook |

---

## 2. What Failed and Why

### Plot A & B — initial run (FIXED)

**Error:** `IndexError: list index out of range` — the subplot grid was 2x2 (4 slots) but 5 regimes had data (including Eastern). Fixed by switching to 2x3 grid in `fix_plots_ab.py`. Both plots now saved correctly.

### Notebook not re-run

The original notebook (`sorting_mechanism_exploration.ipynb`) had a SyntaxError in cell 12 (backslash inside f-string) that blocked all subsequent cells. Rather than fixing cells one-by-one, a standalone script was written that implements the full pipeline correctly. The notebook's logic is sound; the bugs are syntactic.

---

## 3. Key Findings from Plots

### Plot A: RTI vs Anti-Immigration (THE CRITICAL PLOT)

**The sorting pattern IS visible — but not in the direction expected by H1.**

Raw bivariate slopes (RTI → anti-immigration attitudes) by regime:

| Regime | Slope | p-value | N |
|--------|-------|---------|---|
| Nordic | 0.479 | <0.001 | 25,905 |
| Continental | 0.505 | <0.001 | 40,823 |
| **Liberal** | **0.560** | **<0.001** | **15,794** |
| Southern | 0.463 | <0.001 | 17,328 |
| Eastern | 0.295 | <0.001 | 50,924 |

**Interpretation:** Higher RTI → more anti-immigration attitudes EVERYWHERE. The slope is steepest in Liberal regimes (0.560) and weakest in Eastern Europe (0.295). The difference between Nordic (0.479) and Liberal (0.560) is in the predicted direction — vulnerability converts more strongly to exclusionary attitudes in liberal welfare states. However, Continental is very close to Liberal, and Nordic is not clearly lower than either. The gradient is subtle, not dramatic.

**Honest assessment:** The basic finding (RTI predicts anti-immigration) is robust and strong. But the cross-regime variation in slopes is modest. The Liberal regime does show the steepest slope, consistent with H1, but the Nordic-Continental-Liberal differences are not large in raw bivariate terms.

### Plot B: RTI vs Redistribution Support

| Regime | Slope | p-value | N |
|--------|-------|---------|---|
| Nordic | 0.099 | <0.001 | 25,794 |
| Continental | 0.139 | <0.001 | 40,805 |
| Liberal | 0.138 | <0.001 | 15,658 |
| Southern | 0.069 | <0.001 | 17,432 |
| Eastern | 0.128 | <0.001 | 52,772 |

**Interpretation:** Higher RTI → slightly MORE redistribution support in all regimes. The slopes are much flatter than for anti-immigration (0.07–0.14 vs 0.30–0.56). The cross-regime variation does NOT clearly match H2 predictions — Nordic doesn't have the steepest slope. The redistribution channel appears weaker than the exclusion channel.

### Plot C: Country-Level Welfare vs RTI Slopes

- **ALMP spending vs RTI→anti-immigration slope: r=0.41, p=0.007** — Countries with MORE ALMP spending actually show STEEPER RTI→anti-immigration slopes. This is the OPPOSITE of what the theory predicts (more ALMP should buffer the vulnerability-to-exclusion link).
- **Active/passive ratio vs slope: r=-0.15, p=0.370** — Not significant.

**Honest assessment:** The positive ALMP correlation is puzzling and potentially problematic for the theory. It could reflect: (a) reverse causality (countries with more anti-immigration sentiment invest more in ALMP), (b) omitted variables (Nordic countries have both high ALMP and high RTI-attitude slopes), or (c) the ALMP measure doesn't capture conditionality/punitiveness (high ALMP spending could be punitive or enabling).

### Model Results (Mixed Models with Controls)

**Model 1b: Anti-immigration ~ RTI × welfare regime** (Nordic = reference)

| Interaction | Coefficient | p-value | Interpretation |
|-------------|-------------|---------|----------------|
| RTI main (Nordic) | 0.142 | <0.001 | Strong positive: higher RTI → more anti-immigration in Nordic |
| RTI × Continental | 0.002 | 0.889 | No difference from Nordic |
| **RTI × Liberal** | **0.103** | **<0.001** | **Significantly steeper slope than Nordic — supports H1** |
| RTI × Southern | -0.044 | 0.042 | Slightly flatter slope than Nordic |

**This is the key result.** After controlling for education, age, gender, income, and urban/rural, the RTI→anti-immigration link IS significantly stronger in Liberal regimes compared to Nordic. The effect size is meaningful: a 1-SD increase in RTI is associated with 0.103 additional scale points of anti-immigration sentiment in Liberal vs Nordic regimes.

**Model 2b: Redistribution ~ RTI × welfare regime**

| Interaction | Coefficient | p-value |
|-------------|-------------|---------|
| RTI main (Nordic) | 0.048 | <0.001 |
| RTI × Continental | 0.014 | 0.086 |
| RTI × Liberal | 0.006 | 0.556 |
| RTI × Southern | -0.065 | <0.001 |

The redistribution model shows a weaker and less theoretically coherent pattern. The RTI → redistribution link doesn't vary significantly between Nordic and Liberal regimes.

### Education as Moderator

| Education | Nordic | Continental | Liberal | Southern |
|-----------|--------|-------------|---------|----------|
| Non-college | 0.275 | 0.304 | 0.302 | 0.224 |
| College | 0.203 | 0.207 | 0.102 | 0.166 |

**Finding:** The RTI→anti-immigration slope is steeper for non-college workers in ALL regimes. The education buffering effect is strongest in Liberal regimes (non-college: 0.302 vs college: 0.102 — a 66% reduction). This supports the theoretical prediction that education moderates the identity-switching mechanism.

### Deservingness (Wave 8)

- RTI → narrow deservingness: r = -0.080 (higher RTI → slightly LESS restrictive deservingness)
- Narrow deservingness → anti-immigration: r = -0.189

The deservingness correlations are weak and in an unexpected direction. Higher RTI is associated with slightly MORE generous deservingness views, not less. This complicates the H3 mediation story.

---

## 4. Data Quality Issues

- **RTI match rate (87.8%)** is excellent — much better than the 70–80% expected
- **CPDS match rate (40.7%)** is limited because many ESS countries (especially Eastern European) are not in CPDS. This affects the continuous welfare indicator analysis but not the regime-based approach.
- **Household income (hinctnta)** has 19.4% missing — highest missingness among controls. Consider sensitivity analysis with and without this control.
- **Left-right scale** has 13.6% missing — consider whether to include as control vs. mediator.
- **Deservingness items** only available in wave 8 (44,387 obs) — limits H3 analysis to one wave.
- **Israel and Russia** classified as "Other" — 12,541 observations. Could be excluded or kept depending on theoretical scope.
- **18 countries** have data in all 4 waves; remaining 16 appear in only some waves.

---

## 5. Sample Description

- **Full master dataset:** 188,764 rows × 37 variables
- **H1 analysis sample (complete cases on RTI + anti-immig + all controls):** 133,016
- **Waves:** 6, 7, 8, 9 (fieldwork years 2012, 2014, 2016, 2018)
- **34 countries:** AL, AT, BE, BG, CH, CY, CZ, DE, DK, EE, ES, FI, FR, GB, HR, HU, IE, IL, IS, IT, LT, LV, ME, NL, NO, PL, PT, RS, RU, SE, SI, SK, UA, XK

### Observations by Regime

| Regime | N |
|--------|---|
| Continental | 45,863 |
| Eastern | 62,327 |
| Liberal | 18,704 |
| Nordic | 27,920 |
| Southern | 21,409 |
| Other (IL, RU) | 12,541 |

---

## 6. Decisions Still Needed

1. **The ALMP puzzle:** Countries with more ALMP spending show STEEPER vulnerability→exclusion slopes (r=0.41, p=0.007). This contradicts the theory. Before proceeding, decide: (a) is the ALMP measure capturing what we think? (b) should we use a different welfare indicator (conditionality ratio, universalism index from CWED)? (c) is this a composition effect (Nordic countries are outliers)?

2. **Eastern European countries:** They comprise the largest regime group (62,327 obs) and show the flattest RTI→anti-immigration slope. Include in main analysis or restrict to Western Europe? The theory is developed primarily for Western welfare states.

3. **Redistribution DV weakness:** The RTI×regime interaction for redistribution is much weaker than for anti-immigration. Is H2 worth pursuing, or should the paper focus on H1 (the exclusion story)?

4. **Radical right vote:** Not yet constructed. Needed for a complete analysis but attitude-based DVs are sufficient for the current exploration.

5. **Wave selection:** Currently using waves 6–9 only (ISCO-08). Adding waves 4–5 would require the ISCO-88→ISCO-08 crosswalk (available in repo, but many-to-many — see MEMORY.md). Worth the complexity for ~100K additional observations?

---

## 7. Recommended Next Steps

1. **Read Plot A carefully.** The Liberal regime DOES show the steepest slope, which supports H1. The mixed model confirms this is significant after controls. This is a viable empirical strategy.

2. **Address the ALMP puzzle** before using continuous welfare indicators. Consider downloading CWED universalism data or Knotz conditionality index as alternative measures.

3. **Run R multilevel models** with `lme4` — the Python mixed models here are diagnostics. The final specification should use REML estimation with proper random slopes consideration.

4. **Focus the paper on H1** (vulnerability → exclusion, moderated by welfare context). The evidence for H2 (solidarity pathway) is weaker. Consider reframing H2 as exploratory.

5. **Construct radical right vote** using Langenkamp crosswalk — this adds a behavioral DV alongside attitudinal ones.

6. **Consider country-specific slopes plot** — the within-regime variation plot shows substantial heterogeneity within regimes. Individual country labels with slopes would be informative.

---

## Files Produced

```
analysis/
  sorting_mechanism_master.csv    — merged analysis dataset (188,764 x 37)
  codebook.md                     — variable descriptions
  overnight_report.md             — this file
  run_sorting_mechanism.py        — standalone pipeline script
  fix_plots_ab.py                 — fix script for plots A and B

outputs/figures/
  fig2_rti_vs_antiimmig_by_regime.pdf + .png  ← THE CRITICAL PLOT
  fig4_rti_vs_redistribution_by_regime.pdf + .png
  welfare_vs_rti_slopes.pdf + .png
  rti_distribution.pdf + .png
  rti_by_education_regime.pdf + .png
  within_regime_country_variation.pdf + .png

outputs/tables/
  summary_stats.csv
```
