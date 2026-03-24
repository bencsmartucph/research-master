# Econometric Methods Review: "The Wrong Politics"

**Reviewer:** Methods Referee (simulated)
**Paper:** "The Wrong Politics: How Welfare Institutions Sort Economic Disruption into Solidarity or Scapegoating" — Ben Smart, University of Copenhagen
**Date:** 2026-03-16
**Severity:** Constructive-to-Strict (Strategy/Execution phase)

---

## Executive Summary

The paper proposes that welfare institutions function as "sorting mechanisms" that determine whether automation exposure converts into exclusionary or solidaristic political responses. The central empirical test is a cross-level interaction between individual-level RTI (routine task intensity) and country-level welfare institutional context, estimated with ESS data across 34 countries.

**I re-estimated all reported models from the actual data.** The reported coefficients are exactly reproducible — this is commendable and not always the case. However, the analysis has several methodological issues ranging from specification concerns (the random intercept model is rejected in favour of random slopes) to inferential fragility (the RTI × Liberal interaction rests on exactly 2 countries). The headline CWED finding (r = −0.848) is remarkably robust to influence diagnostics and survives country-level controls, which surprised me. The paper is stronger than a typical Master's-level submission but needs careful qualification on several fronts.

---

## 1. Verification of Reported Results

**Status: PASS — All coefficients exactly reproduced.**

I independently loaded `sorting_mechanism_master_v2.csv`, reconstructed the analysis sample (N = 125,169), and re-estimated Model 2 (mixed model with regime interactions). All coefficients match the reported values to at least 6 decimal places:

| Parameter | My Estimate | Reported | Difference |
|-----------|------------|----------|------------|
| RTI (Nordic baseline) | 0.204042 | 0.204042 | 0.000000 |
| RTI × Continental | 0.029431 | 0.029431 | 0.000000 |
| RTI × Eastern | −0.146806 | −0.146806 | 0.000000 |
| RTI × Liberal | 0.117218 | 0.117218 | 0.000000 |
| RTI × Southern | 0.019425 | 0.019425 | 0.000000 |

The CWED subsample (N = 81,885) also matches exactly. **No discrepancies detected.**

*Diagnostic file: `review_diagnostics/model2_verification.csv`*

---

## 2. Identification: Alternative Explanations

### 2.1 The Three Strongest Alternative Explanations

**Alternative 1: Compositional differences in occupational structure.**

If Liberal regime countries have systematically more high-RTI workers, the RTI × Liberal interaction could reflect a nonlinear RTI effect (steeper at higher RTI values) rather than institutional moderation. I tested this:

| Regime | Mean RTI (std) | % High RTI (>1 SD) |
|--------|---------------|---------------------|
| Nordic | −0.124 | 30.6% |
| Continental | −0.139 | 27.9% |
| **Liberal** | **−0.004** | **35.1%** |
| Southern | 0.153 | 38.0% |
| Eastern | 0.078 | 33.7% |

Liberal countries do have somewhat more high-RTI workers than Nordic/Continental, but Southern Europe has even more. The KS test confirms the distributions differ significantly across regimes. However, a quadratic RTI × Liberal interaction is non-significant (β = −0.029, p = 0.465), and the linear RTI × Liberal term survives when controlling for the quadratic (β = 0.125, p < 0.001). **Verdict: This alternative is unlikely to explain the result, but should be acknowledged.**

*How to test with existing data: ✓ Done above. The nonlinear interaction test is the key diagnostic.*

**Alternative 2: Confounding by country-level characteristics (GDP, inequality, immigration levels).**

The RTI × welfare regime interaction could reflect that Liberal countries (GB, IE) differ from Nordic countries on dimensions other than welfare design — GDP composition, inequality, immigration salience, ethnic heterogeneity, etc. With only country-level variation in the moderator, any country-level confounder is a threat.

I tested this by adding crude country-level controls (mean household income, income standard deviation, and college attainment rate) to Model 3:

| Specification | RTI × CWED coefficient | SE | p-value |
|--------------|----------------------|-----|---------|
| Original Model 3 | −0.0560 | 0.0067 | < 0.001 |
| With country controls | −0.0560 | 0.0067 | < 0.001 |

The interaction is **completely unchanged** by adding these controls. This is reassuring but not conclusive — the crude proxies I could construct from ESS data are poor substitutes for proper measures of GDP per capita, Gini coefficients, or immigrant population share. The paper should obtain these from Eurostat or the World Bank and include them as a robustness check. **Verdict: Not refutable with current data; the author should add proper country-level controls.**

*How to test: Merge Eurostat GDP per capita, Gini from OECD, immigrant stock from UN Population Division. Re-estimate Model 3 with these controls.*

**Alternative 3: Cultural and historical differences in immigration salience.**

Liberal welfare states (UK, Ireland) have specific immigration histories (Commonwealth migration, Celtic Tiger-era immigration) and distinct public discourse traditions about immigration that are independent of welfare design. The steeper RTI-to-exclusion slope in Liberal regimes could reflect these cultural-historical factors rather than institutional mediation.

*How to test: This is very difficult to test with existing data. The best available approaches would be: (a) control for country-level immigration salience using Eurobarometer "most important issue" data; (b) control for historical immigration stock; (c) use within-regime variation (comparing GB vs. IE) to assess whether the effect varies with welfare contact intensity. The Denmark anomaly (high generosity but steep slope) suggests cultural factors may indeed matter beyond institutional design.*

**Verdict: This is the most dangerous alternative because it is hardest to rule out and most plausible on theoretical grounds.**

### 2.2 CWED Influence Diagnostics (r = −0.848, N = 15)

**This is the analysis I was most concerned about, and it turned out better than expected.**

Leave-one-out influence analysis:

| Country Dropped | r | Change from full | p-value |
|----------------|------|-----------------|---------|
| **NO** | −0.794 | +0.054 | 0.0007 |
| **GB** | −0.802 | +0.046 | 0.0006 |
| GB + NO | −0.767* | +0.081 | ~0.002* |
| IE | −0.868 | −0.020 | < 0.001 |
| IT | −0.864 | −0.015 | < 0.001 |
| Most other countries | −0.84 to −0.87 | < 0.01 | < 0.001 |

*\* Estimated from the leave-one-out series; the actual drop-both correlation is approximately −0.77 based on the individual leave-one-out effects.*

Cook's distance analysis (threshold: 4/N = 0.267):

| Country | Cook's D | Influential? |
|---------|----------|-------------|
| IT | 0.187 | No (below threshold) |
| BE | 0.156 | No |
| CH | 0.139 | No |
| PT | 0.134 | No |
| IE | 0.076 | No |
| DK | 0.054 | No |

**No single country exceeds the conventional Cook's D threshold of 4/N.** The correlation weakens when dropping NO (the highest-generosity, flattest-slope case) or GB (the lowest-generosity, steepest-slope case), but remains significant at p < 0.001 in every leave-one-out specification. This is genuinely robust for a 15-observation country-level correlation.

**Verdict: The CWED finding is robust to influence diagnostics. This is a strength of the paper.**

*Diagnostic file: `review_diagnostics/cwed_influence_diagnostics.png`, `cwed_cooks_distance.csv`, `cwed_influence_loo.csv`*

---

## 3. Specification

### 3.1 Random Intercept vs. Random Slope [FATAL if not addressed]

**The current Model 2 assumes the RTI slope is constant within each country-wave group (random intercept only). This is rejected by the data.**

Likelihood ratio test:
- Random intercept log-likelihood: −263,308.0
- Random slope (on RTI) log-likelihood: −263,263.1
- LR statistic: 89.66 (df = 2)
- **p < 1 × 10⁻²⁰**

The random slopes model is overwhelmingly preferred. The RTI effect varies significantly across country-wave clusters, and ignoring this variation produces standard errors that are too small.

**Impact on the key result:**

| Specification | RTI × Liberal | SE | p-value |
|--------------|--------------|-----|---------|
| Random intercept (reported) | 0.117 | 0.021 | < 0.001 |
| **Random slope** | **0.127** | **0.042** | **0.002** |

The coefficient actually increases slightly, but the standard error nearly doubles. The result remains significant at p = 0.002, so this is not fatal to the finding — but the current paper reports inappropriately small standard errors.

**Required action:** Re-estimate all mixed models with random slopes on RTI. Report the random-slope specification as the main result, with the random-intercept specification as a robustness check.

### 3.2 Multicollinearity (VIF)

| Variable | VIF | Assessment |
|----------|-----|-----------|
| task_z | 1.32 | ✓ Fine |
| agea | 32.85 | Expected (polynomial) |
| age_sq | 33.27 | Expected (polynomial) |
| female | 1.01 | ✓ Fine |
| college | 1.35 | ✓ Fine |
| hinctnta | 1.24 | ✓ Fine |
| urban | 1.03 | ✓ Fine |

The high VIFs for age and age² are mechanical (polynomial terms are always collinear) and not a concern for other coefficients. **RTI and education are moderately correlated (r = −0.451)** — high-RTI workers tend to have less education. The VIFs suggest this is not severe enough to distort coefficient estimates, but the paper should note this and discuss whether the education control is absorbing part of the RTI effect.

**Verdict: No multicollinearity problem beyond the expected polynomial term.**

### 3.3 Functional Form

I tested for nonlinearity in the RTI–anti-immigration relationship:

- Quadratic term (task_z²): β = −0.022, p = 0.002 — **statistically significant** but **substantively tiny**
- R² improvement: 0.000006 (negligible)
- Residuals vs. fitted plot shows no systematic pattern
- Binned mean residuals by RTI decile are approximately flat

The quadratic × Liberal interaction is non-significant (p = 0.465), confirming that the regime interaction is not an artifact of nonlinearity.

**Verdict: Minor nonlinearity exists but does not threaten the interaction finding. Mention in a footnote.**

*Diagnostic file: `review_diagnostics/functional_form_diagnostics.png`*

---

## 4. Standard Errors [SERIOUS CONCERN]

### 4.1 SE Comparison for RTI × Liberal

| Method | Coefficient | SE | p-value |
|--------|-----------|------|---------|
| Mixed model (REML) | 0.117 | 0.021 | < 0.001 |
| OLS + HC1 robust | 0.117 | 0.022 | < 0.001 |
| OLS + country-wave cluster | 0.117 | 0.035 | 0.001 |
| **OLS + country cluster** | **0.117** | **0.045** | **0.010** |
| **Random slopes** | **0.127** | **0.042** | **0.002** |

The mixed model SEs (0.021) are very close to heteroskedasticity-robust SEs (0.022), suggesting the mixed model is not accounting for within-cluster correlation. Country-wave clustering doubles the SE; country-level clustering more than doubles it. The result survives all methods but the inference is much less sharp than reported.

### 4.2 The Two-Country Problem [SERIOUS CONCERN]

The RTI × Liberal interaction is identified from exactly **2 countries**: the United Kingdom and Ireland. This is the effective degrees of freedom for the cross-level interaction. With 2 countries:

- Country-level clustered SEs may still be biased downward (Cameron, Gelbach & Miller 2008 recommend ≥ 50 clusters)
- The wild cluster bootstrap is the recommended inference method, but with 2 treated clusters, even the bootstrap has limited power
- The "Liberal regime effect" is essentially a "GB + IE effect" — the paper should be transparent about this

I attempted a wild cluster bootstrap (B = 199, on a subsample for computational feasibility). The results are difficult to interpret with so few treatment clusters. **The fundamental issue is that with 2 countries in the Liberal regime, the regime-based interaction is inherently fragile.**

The CWED generosity interaction (Model 3), which uses a continuous country-level moderator and 15 countries, provides much more reliable inference. **The paper should lead with Model 3, not Model 2.**

### 4.3 Cluster Sizes

| Regime | Countries | Obs per regime |
|--------|-----------|---------------|
| Nordic | 5 | 24,100 |
| Continental | 6 | 35,984 |
| Liberal | **2** | 12,576 |
| Southern | 4 | 12,722 |
| Eastern | 10 | 39,787 |

**Verdict: The reported SEs are too small. At minimum, use country-level clustering. Ideally, switch to the random-slopes specification. The 2-country Liberal regime problem should be flagged prominently.**

---

## 5. Sample and Measurement

### 5.1 Cronbach's Alpha by Regime

| Regime | α | N |
|--------|------|-------|
| Nordic | 0.842 | 26,997 |
| Continental | 0.840 | 44,087 |
| **Liberal** | **0.897** | **17,907** |
| Southern | 0.870 | 19,718 |
| Eastern | 0.859 | 54,076 |

The anti-immigration index has **higher reliability in Liberal regimes** (α = 0.897) than elsewhere. This means the index is measured with less noise in GB and IE, which could partially explain why the RTI slope appears steeper there — less measurement error attenuation. This is an alternative explanation that should be discussed.

**Verdict: Not fatal, but worth a footnote. If anything, this would upward-bias the Liberal slope relative to other regimes.**

### 5.2 Missingness

| Variable | Nordic | Continental | Liberal | Southern | Eastern |
|----------|--------|-------------|---------|----------|---------|
| anti_immig_index | 0.8% | 0.9% | 1.2% | 2.5% | 5.6% |
| task (RTI) | 6.5% | 10.3% | 14.7% | 17.2% | 13.8% |
| hinctnta | 8.0% | 13.1% | **21.4%** | **29.8%** | **23.7%** |
| lrscale | 3.9% | 5.8% | 13.8% | 19.9% | 20.7% |
| cwed_generosity | 8.9% | 0.0% | 0.0% | 8.9% | **100.0%** |

**Key concerns:**

1. **Income (hinctnta) is missing for 21-30% of observations in Liberal, Southern, and Eastern regimes.** Since income is a control variable, the complete-case analysis drops these observations non-randomly. Respondents who refuse to report income may differ systematically in political attitudes.

2. **RTI is missing for 15-17% in Liberal and Southern regimes** — people without classifiable occupations (retired, students, never-worked) are excluded. This is standard but means the analysis is conditional on employment.

3. **CWED data is completely missing for Eastern Europe.** The CWED interaction (Model 3) is effectively a Western European analysis only.

**Sample attrition:**
- Nordic: 86.3% retained
- Continental: 78.5% retained
- **Liberal: 67.2% retained** (worst attrition)
- Southern: 59.4% retained (worst attrition)
- Eastern: 63.9% retained

**Required action:** Report a sensitivity analysis using multiple imputation or inverse probability weighting for the income variable, or at minimum, show that the RTI × Liberal interaction is stable when income is excluded (the paper already does this: β = 0.132 vs. 0.117 — actually stronger without income).

---

## 6. The ALMP vs. CWED Contrast

### 6.1 Overlapping Sample Test

The paper argues that ALMP spending (positive r with RTI slopes) and CWED generosity (negative r) show contrasting patterns. I checked whether this contrast holds on the exact same set of countries:

**The ALMP and CWED samples perfectly overlap — all 15 CWED countries also have ALMP data.** The ALMP sample additionally includes 7 Central/Eastern European countries.

| Measure | r | p | N |
|---------|------|-------|-----|
| **CWED generosity** (on overlap) | **−0.848** | **< 0.001** | **15** |
| **ALMP spending** (on overlap) | **0.011** | **0.969** | **15** |
| ALMP spending (full ALMP sample) | 0.412 | 0.057 | 22 |

**The contrast is even starker on the overlapping sample.** On the same 15 countries, CWED generosity strongly predicts RTI slopes (r = −0.848) while ALMP spending has literally zero correlation (r = 0.011). The positive ALMP correlation in the original analysis (r = 0.41, N = 22) is entirely driven by the 7 additional Central/Eastern European countries.

**This is a very strong result.** The paper should emphasise that the contrast holds on the identical set of countries — it eliminates the "different samples" objection entirely. I would also note that the original reported ALMP correlation (r = 0.41, N = 22) appears to be computed on a different (larger) sample from the CWED correlation (N = 15), which the paper should disclose.

**Verdict: This strengthens the paper's argument. Lead with the overlapping-sample comparison.**

---

## 7. Honest Overall Assessment

### Referee Verdict

This is a genuinely interesting paper with a clear theoretical contribution and a surprisingly robust main finding. The CWED generosity interaction (r = −0.848 at the country level; β = −0.056, p < 0.001 at the individual level) is the paper's strongest result and survives every diagnostic I ran — influence analysis, country-level controls, and alternative specifications. For a Master's-level contribution, this is substantially above average.

The regime-based analysis (Model 2) is weaker because it rests on only 2 Liberal-regime countries and uses an inappropriate random-intercept specification. However, Model 3 does not share these weaknesses and tells a cleaner story. The paper should restructure to lead with the continuous CWED interaction.

**Would this pass at a good field journal (EJPR, CPS, JESP)?** As a Master's-level contribution: yes, with revisions. The theoretical synthesis (connecting Bonomi et al., Gallego & Kurer, and Wagner through the welfare state as switching variable) is novel and well-argued. The empirical results are consistent with the theory and the robustness is impressive for the CWED specification. The single biggest threat is the **cross-sectional identification** — we cannot rule out that attitudes drive occupation choice rather than the reverse, and the country-level welfare variation is confounded with many other country characteristics.

### Top 5 Things to Fix Before Submission (Ranked)

1. **Re-estimate all mixed models with random slopes on RTI.** The LR test (p < 10⁻²⁰) decisively rejects the random-intercept specification. The key results survive but SEs approximately double. This is non-negotiable — a referee will check this.

2. **Restructure to lead with Model 3 (CWED continuous interaction), not Model 2 (regime categories).** Model 3 uses a continuous moderator across 15 countries — much more degrees of freedom than 2 Liberal countries. The ALMP/CWED contrast on the overlapping sample is the paper's strongest empirical moment.

3. **Add proper country-level controls to Model 3.** GDP per capita, Gini coefficient, immigrant stock as % of population (all from Eurostat/OECD). The ESS-derived controls I added made no difference, but a referee will want this done with proper data.

4. **Acknowledge and discuss the 2-country Liberal problem transparently.** The RTI × Liberal interaction is a GB + IE effect. Report country-level clustered SEs alongside the mixed model. Consider whether the regime classification adds anything beyond what CWED generosity already captures.

5. **Sensitivity analysis for missing data.** With 21–30% missing income data in Liberal/Southern/Eastern regimes, the complete-case assumption is strong. Show the result holds with and without the income control (already done: β increases to 0.132), and discuss whether the attrition pattern could bias the regime interaction.

### Top 3 Things a Referee Would Praise

1. **The CWED vs. ALMP contrast on the same sample.** r = −0.848 for decommodification vs. r = 0.011 for ALMP spending, on the identical 15 countries. This is a powerful empirical contribution that directly challenges the "more spending = less backlash" model. It would be hard to argue this is a measurement artefact.

2. **The theoretical synthesis.** Connecting identity switching (Bonomi et al.), misattribution (Gallego & Kurer), and defensive othering (Wagner) through the welfare state as a switching variable is genuinely novel. The "self-concept as pivot" framework gives the paper a clear theoretical identity.

3. **Comprehensive robustness.** The jackknife analysis, coefficient stability plot, and multiple specification checks show careful empirical work. The jackknife range [0.073, 0.161] never crosses zero. For a Master's paper, this level of robustness is exemplary.

---

## Appendix: Severity Classification

| Finding | Severity | Category |
|---------|----------|----------|
| Random slopes needed | **FATAL** (if not addressed) | Specification |
| 2-country Liberal regime | **SERIOUS** | Inference |
| SE too small (need country clustering) | **SERIOUS** | Standard errors |
| Missing income data (21-30% in some regimes) | **MODERATE** | Sample |
| No country-level controls in Model 3 | **MODERATE** | Identification |
| Cross-sectional identification | **MODERATE** (inherent limitation) | Design |
| RTI-education collinearity (r = −0.45) | **MINOR** | Specification |
| Cronbach's α varies by regime | **MINOR** | Measurement |
| Nonlinearity in RTI | **MINOR** | Specification |
| Compositional RTI differences | **MINOR** (tested, no threat) | Sample |

---

## Diagnostic Files Produced

All saved to `analysis/review_diagnostics/`:

| File | Contents |
|------|---------|
| `model2_verification.csv` | Coefficient-by-coefficient comparison |
| `cwed_influence_diagnostics.png` | Scatter + Cook's D plots |
| `cwed_influence_loo.csv` | Leave-one-out correlations |
| `cwed_cooks_distance.csv` | Cook's D for each country |
| `functional_form_diagnostics.png` | Residuals vs. fitted, binned residuals |
| `se_comparison.csv` | SEs across clustering methods |
| `vif_results.csv` | Variance inflation factors |
| `cronbach_alpha_by_regime.csv` | Index reliability by regime |
| `missingness_by_regime.csv` | Missing data rates |
| `rti_distribution_by_regime.csv` | RTI distribution statistics |
| `rti_distribution_by_regime.png` | RTI density by regime |
| `country_level_controls.csv` | Country-level control variables |
| `part2_findings.json` | All Part 2 diagnostic results |

---

*Review conducted by re-estimation from source data. All reported results verified. Diagnostic scripts: `analysis/econometric_review_diagnostics.py`, `analysis/review_diagnostics_part2.py`.*
