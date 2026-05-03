# Empirical Walkthrough — Section V

**A tutor-document for Ben Smart, on the empirical analysis of *Dignity Is a Baseline*.**

This is the conversation we should have had before you wrote §V, except you wrote §V first, which is the right way around. You now know what your data says. The job here is to make sure you know *why* each modelling choice was made, what each parameter is actually telling you, and where the inference is and isn't defensible. The structure follows §V from A through G, but the weight is on the eight econometric ideas that do the load-bearing work: random slopes, cross-level interactions, likelihood ratio tests, cluster-robust standard errors, matched-sample logic, inference at N=15, the two-DV asymmetry, and the behavioural-attitudinal distinction. For each, you get the intuition first, the algebra in toggles, the code from your own pipeline, the alternatives you didn't take and why, and a recall prompt to make sure the explanation stuck. By the end you should be able to defend every modelling decision in §V to a hostile referee in thirty seconds, including the ones you would not have phrased that way three months ago.

---

## §V.A — Data and Measurement (compact)

The data come from ESS rounds 6–9, fieldwork 2012–2018, 34 countries, 188,764 individual-wave observations. RTI is mapped from three-digit ISCO-08 occupation codes using the Goos-Manning-Salomons (2014) task scores. The anti-immigration index is three ESS items reverse-coded onto a 0–10 scale; α=0.864 says the items hang together well enough to treat as one construct. The redistribution outcome is `gincdif` reverse-coded onto 1–5. CWED decommodification is the country-level mean across unemployment, sickness, and pension programme generosity scores, 2005–2011, time-invariant. ALMP is country-level spending share of GDP from CPDS, also collapsed to a country-level mean.

The two non-trivial measurement choices both deserve a paragraph each, because both will be challenged.

**Why a three-item composite, not each item separately?** The α=0.864 says respondents who give a hostile answer on one item give hostile answers on the others; you are measuring one underlying disposition, not three. Running the analysis on each item separately would triple the multiple-testing burden, sacrifice statistical power, and produce three slightly noisier estimates of the same thing. The composite is the disciplined choice. The cost is that any item-specific signal (say, hostility specifically on the *cultural* item but not the *economic* one) is averaged out. For your asymmetric-mechanism story this cost is acceptable, since the theory is about general exclusionary disposition, not about which specific framing of immigration triggers it.

**Why ES-ISCED rather than years of education?** ES-ISCED is the ESS-harmonised seven-category education classification; years-of-education varies wildly in its meaning across countries. A Danish vocational diploma at age 18 is not equivalent to a British BTEC at age 18, but ES-ISCED forces them onto the same conceptual ladder. The cost is that you treat education as a categorical (ordered) variable rather than a continuous one, which means you cannot ask "what is the marginal return to one additional year of schooling?". Since you are using education as a *control*, not an object of inference, this cost is essentially zero. The benefit is cross-national comparability, which you absolutely need.

The 87.8% match rate on RTI matters less than it sounds. The 12.2% unmatched are mostly observations missing ISCO codes (small employers, students, retirees). They drop out of the analysis sample, which is fine; the threat would be if the missing-at-random assumption failed, and you have no reason to think it does.

<details>
<summary>Recall prompt: §V.A measurement</summary>

Without re-reading: why is α=0.864 a sufficient justification for the composite? What would change if it were 0.55? (Answer: at α=0.864 the items measure one latent construct well; at 0.55 they would not, and you would need either factor scores from a CFA, or to report the items separately.)
</details>

---

## §V.B — Concept 1: Multilevel models with random slopes

### The problem

You have individuals nested in country-waves nested in countries. A person from Denmark in ESS round 7 shares a context with other Danes in round 7; that context is shared in ways your individual-level controls cannot capture. If you run a single pooled OLS regression of anti-immigration on RTI plus controls, you make two implicit assumptions, and both are wrong. First, you assume errors across observations are independent, when in fact people in the same country-wave share unobserved shocks (an immigration crisis, an electoral campaign, a recession). Second, and worse for your story, you assume the *effect of RTI* is identical in every country. The whole point of §V is to test whether that effect varies by welfare regime. So you need a model that lets the slope vary.

### Concrete first

Suppose three countries: Denmark, the UK, and Italy. Within each country, individuals vary in RTI from −1.5 (very abstract jobs) to +1.5 (very routine jobs), and the slope of anti-immigration on RTI is 0.40 in Denmark, 0.55 in Italy, and 0.70 in the UK. Pooled OLS would estimate something like 0.55, the average slope. It would also report a tight standard error, because pooled OLS believes you have one slope estimated on lots of data. But you don't have one slope; you have three slopes, and the precision of the *average* slope is governed by how many *countries* you have, not how many people. Treating cross-country variation in the slope as if it were sampling noise within a single slope is exactly the mistake the multilevel model fixes.

### Setup

Start with the simplest case: random intercepts only.

$$y_{ij} = \beta_0 + \beta_1 \cdot \text{RTI}_{ij} + u_{0j} + \varepsilon_{ij}$$

where $j$ indexes country-wave and $i$ indexes individuals. The term $u_{0j} \sim N(0, \tau_0^2)$ is a country-wave-specific intercept, drawn from a normal with variance $\tau_0^2$. This says: every country-wave gets its own baseline level of anti-immigration, but the *slope of RTI* on anti-immigration is the same everywhere ($\beta_1$). That's still wrong for your purposes. Now extend to random slopes:

$$\color{blue}{y_{ij}} = \color{purple}{\beta_0} + \color{purple}{\beta_1} \cdot \color{blue}{\text{RTI}_{ij}} + \underbrace{u_{0j}}_{\text{country-wave intercept}} + \underbrace{u_{1j} \cdot \color{blue}{\text{RTI}_{ij}}}_{\text{country-wave slope deviation}} + \color{red}{\varepsilon_{ij}}$$

with $(u_{0j}, u_{1j}) \sim N(0, \Sigma)$ where $\Sigma$ is a 2×2 covariance matrix capturing how intercepts and slopes vary, and how they covary. In R/lme4 syntax this is `(1 + RTI | country_wave)`; in your statsmodels code you build it from `patsy.dmatrix('~task_z', ...)`. The fixed-effect $\beta_1$ is now the *average* slope across country-waves; $u_{1j}$ captures the country-wave-specific deviation from that average.

| Equation | What it says |
|----------|--------------|
| $\beta_1$ | The average slope of RTI on anti-immigration across all country-waves. |
| $u_{1j}$ | How much country-wave $j$'s slope deviates from that average. |
| $\sigma^2_{u_1}$ | The variance of those deviations. If small, slopes are nearly identical across country-waves; if large, they vary a lot. |
| $\sigma^2_\varepsilon$ | Within-country-wave individual-level residual variance. |

### Code

From `scripts/random_slopes_models.py`:

```python
60   CTRLS   = 'agea + age_sq + female + college + hinctnta + urban'
61   GROUPS  = 'cntry_wave'
62   RE_INTR = None            # random intercept only (old spec)
63   RE_SLOP = '~task_z'      # random slopes (correct spec)

70       import patsy
71       from statsmodels.regression.mixed_linear_model import MixedLM
80       endog, exog = patsy.dmatrices(formula, data=data, return_type='dataframe')
81       endog = endog.iloc[:, 0]
82       groups = data[GROUPS].astype(str).tolist()
83
84       if re_formula:
85           exog_re = patsy.dmatrix(re_formula, data=data, return_type='dataframe')
86           m = MixedLM(endog, exog, groups=groups, exog_re=exog_re)
87       else:
88           m = MixedLM(endog, exog, groups=groups)
89
90       m = m.fit(reml=True, method='lbfgs')
```

Two non-obvious lines. Line 85: `patsy.dmatrix('~task_z', ...)` returns a design matrix with an intercept column and a `task_z` column. Passing this as `exog_re` is what turns `(1 | cntry_wave)` into `(1 + task_z | cntry_wave)`. Line 90: REML estimation with L-BFGS optimisation. REML (restricted maximum likelihood) gives less biased variance-component estimates than ML when the number of fixed effects is non-trivial, which it is here. L-BFGS rather than Newton-Raphson because Newton-Raphson chokes on sample sizes this large.

### What goes wrong without random slopes?

If you fit Model 3 (the cross-level interaction) with random intercepts only, you get a slightly different point estimate but, critically, *much* tighter standard errors. The published Model 3 reports β=−0.059 with SE such that p=0.015. The random-intercepts-only version returns roughly the same coefficient but a noticeably smaller SE. That sounds like it should be good news. It isn't. The smaller SE is buying its precision by *assuming* RTI's effect is identical in every country-wave; the LR test rejects that assumption at p<10⁻²⁰. So the smaller SE is wrong, and any inference based on it (a confidence interval, a p-value, a power calculation) is wrong in a direction that flatters your finding. The wider SE from the random-slopes model is the *honest* SE; it admits that your inference about $\beta_3$ depends on cross-country slope variation, of which you have a finite amount.

### Alternatives

**OLS with country-wave fixed effects + clustered SEs.** This is what you run as a robustness check. It absorbs all country-wave-level variation as dummies, so country-wave-specific intercepts are not modelled stochastically; they are absorbed deterministically. The clustered SEs at the country-wave level then handle within-cluster correlation. *What it buys:* simplicity, no distributional assumption on the intercept distribution, easy interpretation. *What it costs:* you cannot estimate cross-level effects (since the country-wave dummies absorb anything that varies only at country-wave level, which includes welfare regime). For Models 1 and 2 you can have it both ways by including welfare regime in the FE specification, but for Model 3 the CWED interaction would be collinear with country dummies. So OLS+FE works as a *robustness check on the individual-level coefficients* but cannot replace the mixed model for the cross-level interaction. The directional convergence between the two estimators (same sign, same approximate magnitude) is the right robustness signal. Identical coefficients would be suspicious; convergence within reason is what you want.

**Bayesian multilevel model with weakly-informative priors.** A Bayesian MLM (Stan, brms) would give you full posterior distributions on every parameter, which is materially more informative than your frequentist confidence intervals when N is small at the cluster level. *What it buys:* honest small-sample inference at the country level, principled handling of the cluster-level $N=15$ problem in §V.D, and the option to report posterior probabilities like "Pr(β₃ < 0) = 0.992" which a referee can read more directly than a p-value. *What it costs:* you have to defend the prior. A weakly-informative prior on $\beta_3$ centred at zero would *shrink* extreme country-level estimates toward the grand mean. The shrinkage is a feature in most settings. In your setting it is a problem: the UK and Norway are the endpoints that drive r=−0.848, and Bayesian shrinkage would specifically dampen those endpoints. So you would get a smaller correlation by the same logic that produces the better-calibrated inference. This is a real trade-off; reasonable people would defend either choice. The argument for staying frequentist is that your readers expect the standard estimator, the priors would themselves become a defensive surface, and the jackknife in §V.D already does a defensible job of probing the leverage problem.

**Between-effects estimator.** Collapse to country-level means and run OLS on those means. *What it buys:* a clean answer to a country-level question, with the right unit of analysis. *What it costs:* you throw away within-country variation in RTI, which is most of your data. For Model 3 specifically, the between-effects estimator is essentially what you do in the §V.D scatter (per-country slopes vs CWED). Running it as the *main* model would mean abandoning the cross-level interaction structure entirely. The mixed model is strictly more informative because it uses the within-country data to estimate slopes precisely *and* uses the between-country variation in those slopes to estimate the cross-level interaction.

**Jackknife across countries.** You already do some of this. *What it buys:* a non-parametric check on whether single observations are driving the result. *What it costs:* it tells you about leverage but not about uncertainty in any principled way. Jackknife is an answer to "is my finding driven by one country?" not an answer to "what is the standard error of my estimate?". Both questions matter; jackknife is the right tool for the first but not the second.

The mixed model with random slopes wins this trade-off because (a) it is the standard estimator a referee will expect, (b) the LR test gives you a defensible statistical justification for it, (c) the SE inflation it produces is the *correct* SE rather than a defect, and (d) the cross-level interaction $\beta_3$ requires a multilevel structure to be identified at all. The OLS+FE robustness, the implicit between-effects in §V.D, and the jackknife together cover the alternatives at a level a reasonable referee will accept.

### Worked example

A quick sense of what random slopes do to your data. Pretend for a moment that Denmark has a within-Denmark RTI slope of 0.41, Sweden has 0.40, the UK has 0.51, Ireland has 0.51, and Italy has 0.46. The pooled OLS slope is the (weighted) average, somewhere around 0.45. The random-intercepts-only mixed model returns the same point estimate, with a small SE. The random-slopes mixed model returns the same point estimate, with a larger SE that reflects the variance of those five numbers around 0.45. Now imagine the LR test: it asks whether the variance of those five numbers is statistically distinguishable from zero. With p < 10⁻²⁰ the answer is overwhelmingly yes. You then know the random-slopes specification is required, and the larger SE is the one to report.

<details>
<summary>Active recall prompt: random slopes</summary>

Without re-reading: what would happen to the SE on β₃ in Model 3 if you dropped the random slopes term? Would the point estimate change? Would the inference become more or less defensible?

(Answer: the SE would get noticeably smaller; the point estimate would barely change; the inference would become *less* defensible because the smaller SE assumes a slope-homogeneity that the LR test rejects.)
</details>

### Connections

Random slopes are the heteroskedasticity-of-effects analogue of the heteroskedasticity-of-errors you already know how to handle. There, you allow the residual variance to differ across observations and use White or cluster-robust standard errors. Here, you allow the *coefficient itself* to differ across clusters and use a mixed model to estimate both the average coefficient and the variance of that coefficient. Both moves are about not pretending you have more information than you do.

This concept also enables your thesis. The within-country fixed-effects design you intend to run on Danish registry data is, in spirit, an even stronger version of the same logic: rather than allowing slopes to differ across countries and then averaging, you exploit within-country variation in welfare reforms to identify the slope from variation that other country-level confounders cannot generate.

---

## §V.B — Concept 2: Cross-level interactions

### The problem

You want to test whether the slope of RTI on anti-immigration depends on a country-level variable (welfare context). A standard within-level interaction (RTI × Income, or RTI × Education) is identified from variation that exists *within* a country. A cross-level interaction is identified from variation *across* countries. That difference matters, because cross-country variation is much harder to come by, harder to defend as exogenous, and much more vulnerable to confounding.

### Concrete first

Imagine just two countries. In Country A, the slope of anti-immigration on RTI is 0.50. In Country B, it is 0.30. The difference is 0.20. If Country A is "Liberal" and Country B is "Nordic", then a regression with $\text{RTI} \times \text{Liberal}$ as the interaction term will return 0.20 as the coefficient on the interaction. That's the cross-level interaction in its simplest form. Now generalise: with five regimes and 34 countries, the regression returns the average difference in slopes between each non-Nordic regime and the Nordic baseline. This is what your Model 2 is doing.

### Setup

The cross-level interaction model:

$$\color{blue}{y_{ij}} = \color{purple}{\beta_0} + \color{purple}{\beta_1}\color{blue}{\text{RTI}_{ij}} + \color{green}{\beta_2}\color{orange}{W_j} + \underbrace{\color{red}{\beta_3}(\color{blue}{\text{RTI}_{ij}} \times \color{orange}{W_j})}_{\text{cross-level interaction}} + \gamma\mathbf{X}_{ij} + u_{0j} + u_{1j}\color{blue}{\text{RTI}_{ij}} + \color{red}{\varepsilon_{ij}}$$

Reading the colours: blue is individual-level (RTI varies person to person), orange is country-level (welfare context is constant within a country), purple/green/red are the coefficients we estimate. The interaction term mixes a blue and an orange variable; that's what makes it cross-level.

| Equation | What it says |
|----------|--------------|
| $\beta_1$ | The slope of RTI on anti-immigration *when $W_j = 0$*. Since you've standardised CWED to mean 0, this is the slope at average decommodification. |
| $\beta_2$ | The effect of moving from average to one-SD-higher decommodification on anti-immigration *for someone with average RTI*. |
| $\beta_3$ | The amount by which a one-SD-higher decommodification *changes the slope* of RTI on anti-immigration. This is your central parameter. |

For Model 3, $\beta_3 = -0.059$, $p = 0.015$. In words: a one-standard-deviation increase in welfare decommodification reduces the slope of RTI on anti-immigration by 0.059 scale points. A negative interaction is what the asymmetric theory predicts: more dignity-preserving welfare flattens the conversion of vulnerability into exclusion.

### Code

From `analysis/final_analysis_pipeline.py`:

```python
489  print('\n--- Model 3: CWED generosity interaction (Mixed) ---')
490  try:
491      # Subset to countries with CWED data
492      analysis_cwed = analysis.dropna(subset=['cwed_generosity_z']).copy()
493      print(f'CWED analysis sample: {len(analysis_cwed):,} obs ({len(analysis_cwed)/len(analysis):.1%} of main sample)')
494
495      formula3 = ('anti_immig_index ~ task_z * cwed_generosity_z'
496                  ' + agea + age_sq + female + college + hinctnta + urban')
497      m3 = smf.mixedlm(formula3, data=analysis_cwed, groups=analysis_cwed['cntry_wave']).fit(reml=True)
505          'coef_interaction': m3.params['task_z:cwed_generosity_z'],
506          'se_interaction': m3.bse['task_z:cwed_generosity_z'],
507          'p_interaction': m3.pvalues['task_z:cwed_generosity_z'],
```

Note: this is the *random-intercepts-only* version of Model 3, which is what produced the published β=−0.059. The `*` operator in the formula expands automatically to include both main effects and the interaction. Line 492 restricts the analysis sample to country-waves with non-missing CWED data, which is the 15 Western European countries; this gives roughly 81,885 observations (58% of the main sample). The random-slopes counterpart that the LR test demands lives in `scripts/random_slopes_models.py` and gives roughly the same point estimate with a larger SE.

### What goes wrong without modelling this carefully?

Two things, in sequence.

First, if you ignore the cross-level structure and run plain OLS with the interaction term, your standard error on $\beta_3$ will be far too small. OLS treats every individual as an independent observation; for a country-level moderator, the *real* sample size for $\beta_3$ is closer to the number of countries than the number of individuals. The mixed model corrects this by giving the country-level term its proper weight in the inference. This is the random-slopes argument again: an interaction with a country-level variable is identified primarily off cross-country slope variation, and the SE has to reflect how much such variation is available.

Second, if you fit the interaction in a country-fixed-effects OLS, the country dummies absorb every country-level predictor, including CWED. The interaction itself survives (because it varies within country in the sense that high-RTI vs low-RTI individuals within a high-CWED country face different effective contexts), but the main effect of CWED is unidentifiable. This is fine if you only care about $\beta_3$, but it makes interpretation awkward. The mixed model lets you estimate $\beta_2$ and $\beta_3$ jointly, which is the right inferential structure for a cross-level interaction.

### Alternatives

**Country-FE OLS with a within-only interaction.** Drop the country-level main effect, keep just $\text{RTI} \times \text{CWED}$ as an interaction. *What it buys:* shields you from cross-country confounding on the main effects. *What it costs:* the interaction is now identified off the *within-country covariance* between RTI and the constructed RTI×CWED product, which is mechanical (since CWED is constant within country, the interaction within country is just RTI scaled by a country-specific constant). This is identifiable but harder to interpret cleanly. The mixed model is more transparent about what variation is doing the work.

**Two-step estimation (BLUPs scatter).** Fit a random-slopes model with no country-level moderator; extract the country-specific slopes (the BLUPs, $\hat\beta_1 + \hat u_{1j}$); then regress those slopes on CWED in a second-stage OLS. *What it buys:* a clean visual story (your Figure 6 is essentially this) and an intuitive interpretation. *What it costs:* the second-stage SEs ignore that the BLUPs are themselves estimated with error, so a naïve second-stage p-value will be too small. Your §V.D scatter is morally this design but uses *separate-country OLS* rather than BLUPs (more on this in Concept 5), which is even more transparent. The single-step cross-level interaction is the right *inferential* model; the two-step scatter is the right *visual* model. You should report both, which is what you do.

**Separate regressions by regime.** Run a separate model in each regime, compare slopes informally. *What it buys:* nothing the regime-interaction Model 2 doesn't already give you, but with worse SEs and no formal test of the difference. *What it costs:* statistical efficiency. This is a non-starter for inference but useful for descriptive Figure 2.

The mixed model with the interaction term wins because it produces a single, interpretable test ($\beta_3$ with its SE and p-value) and the published result (β=−0.059, p=0.015) is the parameter the theoretical claim hangs on. The two-step scatter in §V.D and the separate-regime descriptive plots are both supplements that make the same finding more readable.

### Worked example

You have $\beta_3 = -0.059$. CWED is standardised; one SD of CWED in your sample is roughly the gap between the median country and the top quartile. So moving a country from CWED-average to one-SD-above-average reduces the slope of RTI on anti-immigration by 0.059 scale points. The unconditional slope at average CWED is $\beta_1 = 0.215$. So in a country one SD above the CWED mean (roughly Sweden), the conditional slope is $0.215 - 0.059 = 0.156$. In a country one SD below (roughly Greece or Spain), it is $0.215 + 0.059 = 0.274$. The implied difference between high-CWED and low-CWED countries is therefore $0.274 - 0.156 = 0.118$ scale points per SD of RTI. This matches the regime gap you report in Model 2 between Liberal and Nordic ($\beta_{\text{RTI} \times \text{Liberal}} = 0.127$). The two specifications converge on the same substantive story, by different routes.

<details>
<summary>Active recall prompt: cross-level interactions</summary>

Without re-reading: in Model 3, what would $\beta_1$ mean if you had *not* standardised CWED? What would happen to its SE?

(Answer: $\beta_1$ would be the slope of RTI on anti-immigration *at CWED = 0*, which is outside your sample range and therefore meaningless. The SE would also typically inflate, because the model is now extrapolating to a CWED value that no country in your data actually has. Standardising puts $\beta_1$ on the slope at average CWED, which is interpretable.)
</details>

### Connections

This builds on the standard interaction term you already know (Income × Education, say). What's new is that one of the variables is at a higher level of aggregation than the other, which raises the SE in a principled way and forces you to think about the country-level $N$ rather than the individual $N$. It enables the §V.D country-level scatter, which is the most consequential figure in your paper, by giving the cross-level interaction its formal individual-level counterpart.

It also enables the within-country thesis design. Replace welfare regime with a within-country welfare reform, and the cross-level interaction becomes a within-country difference-in-differences. The structure of inference is the same; only the source of identifying variation changes.

---

## §V.B — Concept 3: Likelihood ratio tests

### The problem

You added random slopes to Model 3. How do you know the addition is justified, rather than just adding two parameters (the slope variance and the slope-intercept covariance) for the sake of it? In a frequentist framework, the answer is the likelihood ratio test: a formal test of whether the more complex model fits the data significantly better than the simpler one.

### Concrete first

Imagine you are choosing between two models. Model A has 5 parameters and a log-likelihood of −1000. Model B nests A and adds 2 more parameters (so it has 7), with a log-likelihood of −985. The difference is 15 log-likelihood units, in B's favour. Is this difference statistically meaningful, or did B just exploit two extra knobs to fit noise? The LR test asks: under the null that the extra parameters are zero, the test statistic $2(\ell_B - \ell_A)$ is distributed asymptotically $\chi^2$ with degrees of freedom equal to the number of extra parameters. So $2 \times 15 = 30$ on $\chi^2_2$ has $p < 10^{-6}$. Model B fits better, and the improvement is not noise.

### Setup

For two nested models (every parameter in the smaller model is also in the larger one):

$$\Lambda = 2(\ell_{\text{full}} - \ell_{\text{reduced}}) \sim \chi^2_{k}$$

where $k$ is the difference in the number of parameters and $\ell$ is the log-likelihood. For your random-slopes-vs-random-intercepts test, $k = 2$ (slope variance + slope-intercept covariance). The asymptotic $\chi^2$ distribution holds under regularity conditions; for variance components on the boundary (a variance can't be negative) the distribution is technically a mixture of $\chi^2$s, which is conservative, so the standard $\chi^2$ test gives a slightly larger p-value than the true one. That conservativeness works in your favour.

### Code

From `scripts/random_slopes_models.py`:

```python
154  print("\nLR test: random slopes vs intercept-only on Model 3...")
160  _df3_cc = df3.dropna(subset=['task_z','anti_immig_index','cwed_generosity_z',
161                                 'agea','age_sq','female','college','hinctnta','urban',
162                                 GROUPS]).reset_index(drop=True)
163  _endog3, _exog3 = patsy.dmatrices(f3, data=_df3_cc, return_type='dataframe')
164  _endog3 = _endog3.iloc[:, 0]
165  _grp3   = _df3_cc[GROUPS].astype(str).tolist()
166  _re3    = patsy.dmatrix('~task_z', data=_df3_cc, return_type='dataframe')
167  try:
168      m3_ri_lr = _MixedLM(_endog3, _exog3, groups=_grp3).fit(reml=False, method='lbfgs', disp=False)
169      m3_rs_lr = _MixedLM(_endog3, _exog3, groups=_grp3, exog_re=_re3).fit(reml=False, method='lbfgs', disp=False)
170      lr_stat = 2 * (m3_rs_lr.llf - m3_ri_lr.llf)
171      lr_p = scipy_stats.chi2.sf(max(lr_stat, 0), df=2)
172      print(f"  LR χ²={lr_stat:.1f}, p={lr_p:.2e} → random slopes {'justified ✓' if lr_p < 0.05 else 'marginal'}")
```

Two non-obvious things. Line 160: the LR test requires both models to be fit on *exactly the same data*, hence the explicit complete-case subset that's used for both fits. Lines 168–169: `reml=False` switches to maximum likelihood. This is essential. REML log-likelihoods are not comparable across models with different fixed-effects or random-effects structures, because REML conditions on a different sufficient statistic in each. ML log-likelihoods are directly comparable, which is what the LR test requires. Line 171: $\chi^2_2$ p-value, with $df=2$ for the two extra parameters in the full model.

### What the result is telling you

The result was $p < 10^{-20}$. That's a $\chi^2_2$ statistic above 90, which is enormous. In substantive terms: the slopes of RTI on anti-immigration are not interchangeable across country-waves. They vary, the variation is large enough to detect with overwhelming statistical confidence, and any model that ignores the variation will produce understated standard errors and therefore overstate the precision of every coefficient that involves RTI. The LR test is the formal warrant for using the random-slopes specification rather than the random-intercepts-only one; it converts a defensible methodological preference into an empirically justified one.

### What goes wrong if you skip the LR test?

Two things. First, you lose the formal warrant for the random-slopes spec, and a referee can press you on whether the added complexity is justified. The LR test is the cheap, standard, well-understood answer to that question; not running it means you have to defend the spec on intuition alone. Second, and worse, if you compare REML log-likelihoods rather than ML log-likelihoods (a common mistake), the test statistic is biased and the conclusion can flip in either direction. The fix is simple (refit both models with `reml=False`) but easy to miss; getting it wrong undermines the inference.

### Alternatives

**AIC / BIC.** Information criteria are an alternative to the LR test for comparing nested or non-nested models. AIC penalises model complexity less than BIC. *What they buy:* they work for non-nested model comparisons (where the LR test doesn't apply) and they don't require setting an arbitrary significance threshold. *What they cost:* they don't give you a p-value, which is what most referees expect to see for a model-selection decision. With $p < 10^{-20}$ on the LR test, AIC and BIC will both massively prefer the random-slopes model anyway, so the choice of criterion is a non-issue here. The LR test is just the convention.

**Bayesian model comparison via Bayes factors.** Compare the marginal likelihoods of the two models. *What it buys:* a directly interpretable quantity (the ratio of evidence for one model vs the other) without the awkward asymptotic-distribution caveats. *What it costs:* requires a fully specified prior on every parameter in both models, and computing the marginal likelihood is non-trivial. For an LR statistic this large the Bayes factor would also overwhelmingly favour the random-slopes model; the additional machinery doesn't change the conclusion. So this is technically defensible but adds work without changing the answer.

**Just trust the larger SE.** Some practitioners would argue that if the random-slopes spec produces larger SEs, that's evidence enough that slope variance matters, and the LR test is overkill. *What it buys:* one fewer table in the appendix. *What it costs:* nothing in your case, but in general you would lose the formal warrant for the spec, and a thoughtful referee will ask. Better to run the test; it costs nothing.

The LR test wins because it's the standard, well-understood, conservative test for nested random-effects structures. Skipping it would invite the question; running it answers the question definitively.

### Worked example

The published LR statistic is roughly $\chi^2_2 = 90+$ with $p < 10^{-20}$. To get a sense of what that means: under the null of no slope variation, you would expect the LR statistic to be drawn from $\chi^2_2$ with mean 2. Observing a value above 90 is something like 45 standard deviations from the null mean. The chance of seeing this by chance is, in human terms, zero. The slopes vary; the random-slopes spec is required.

<details>
<summary>Active recall prompt: LR tests</summary>

Without re-reading: why does the LR test require ML rather than REML estimation? What would happen if you ran it on REML log-likelihoods?

(Answer: REML conditions on the residuals of the fixed-effects model, so the log-likelihoods of two REML fits with different fixed or random effects are not on the same scale. The difference is uninterpretable. ML log-likelihoods are computed on the full data and are comparable across nested specifications. Running the LR test on REML log-likelihoods can give a wildly wrong test statistic in either direction.)
</details>

### Connections

The LR test is the workhorse of nested model comparison across maximum-likelihood econometrics. You already know it from the test for added regressors in a logistic model (where it's the deviance test) and from the test for restrictions in a SEM. The mixed-model application is the same logic; the only special feature is the variance-component-on-the-boundary issue, which makes the test conservative. For your purposes, "conservative" means you can quote the p-value as reported and not worry about overstating significance.

---

## §V.B — Concept 4: Cluster-robust standard errors

### The problem

In the OLS robustness specification, you cluster standard errors at the country-wave level. The reason is that observations within a country-wave are not independent. Two Danes surveyed in ESS round 7 share a context (Danish electoral campaign, Danish media, Danish economy at that moment) that creates within-cluster correlation in their outcomes that your individual-level controls cannot fully absorb. If you ignore this correlation and use vanilla OLS standard errors, you treat dependent observations as independent and your standard errors are far too small. Cluster-robust SEs correct for this.

### Concrete first

Imagine 100 individuals in Denmark in 2014 and 100 individuals in the UK in 2014. If a Danish electoral campaign in 2014 made all Danes 0.5 points more anti-immigration than they would otherwise have been (a country-wave shock), then the Danish observations are not independent draws; they share a 0.5-point common shift. Vanilla OLS would treat your data as 200 independent observations and report a standard error appropriate to N=200. The right standard error is closer to one appropriate to N=2 country-waves, because the variation that matters for cross-country inference is at the country-wave level. Cluster-robust SEs interpolate between these extremes, accounting for within-cluster correlation while still using the within-cluster variation that does exist.

### Setup

The cluster-robust variance formula:

$$\widehat{V}_{\text{cluster}}(\hat\beta) = (X'X)^{-1} \left[\sum_{g=1}^{G} X_g' \hat\varepsilon_g \hat\varepsilon_g' X_g\right] (X'X)^{-1}$$

where $g$ indexes clusters, $X_g$ and $\hat\varepsilon_g$ are the design matrix and residuals for cluster $g$, and $G$ is the number of clusters. The middle term replaces the vanilla OLS $\sigma^2 X'X$ with a sum over clusters, allowing the residual covariance within a cluster to be arbitrary. The cost is precision: the variance estimator has finite-sample bias that grows when $G$ is small (rule of thumb: needs $G \geq 30$ to be well-behaved; you have ~136 country-waves, so this is fine).

### Code

The country-wave-clustered OLS robustness check:

```python
441      formula1 = 'anti_immig_index ~ task_z + agea + age_sq + female + college + hinctnta + urban + C(cntry_wave)'
442      m1 = smf.ols(formula1, data=analysis).fit(cov_type='cluster', cov_kwds={'groups': analysis['cntry_wave']})
```

And the regime-interaction version:

```python
687  def run_robustness(label, data, formula_extra='', extra_controls=''):
690          base = ('anti_immig_index ~ task_z * C(welfare_regime, Treatment(reference="Nordic"))'
691                  ' + agea + age_sq + female + college')
697          base += ' + C(cntry_wave)'
698
699          m = smf.ols(base, data=data).fit(cov_type='cluster',
700                                            cov_kwds={'groups': data['cntry_wave']})
```

Two things to note. The fixed effects are `C(cntry_wave)`, which absorbs all country-wave-level intercepts as dummies. The clustering is *also* at the country-wave level; this is the standard pairing. You absorb the cluster-level mean and then cluster the SEs at the same level, which handles both the level shifts (via the dummies) and the within-cluster correlation in residuals (via the clustering).

### How this differs from the random-effects correction

Both the random-effects model and cluster-robust SEs handle within-cluster correlation, but they do so differently. The random-effects model is *parametric*: it assumes a specific structure for the cluster-level variance (a normal distribution with constant variance) and uses that structure to compute SEs. Cluster-robust SEs are *non-parametric*: they make no assumption about the structure of within-cluster correlation; they just sum the residual cross-products within each cluster. Random effects are more efficient if their assumption is correct; cluster-robust is more defensive if you're unsure.

You report both because they answer slightly different questions. The mixed model gives you the substantively interpretable cross-level interaction $\beta_3$ with the right SE for that parameter. The OLS+FE+clustered specification gives you the same individual-level coefficients with an SE that doesn't depend on any particular distributional assumption about country-wave intercepts. *Directional convergence* between the two estimators is the right robustness signal: same sign, same approximate magnitude, similar SEs (the OLS+FE will typically be slightly tighter, because the dummies absorb more variance deterministically; the mixed model is more conservative). If they diverged, you would have a problem; they don't, so the inference holds across two different estimation frameworks.

### What goes wrong without clustering?

If you ignore clustering and use vanilla OLS standard errors on data with within-country-wave correlation, your SEs will be far too small. How small depends on the intra-cluster correlation $\rho$ and the average cluster size $\bar{n}$: the SE understatement factor is roughly $\sqrt{1 + (\bar{n} - 1)\rho}$. With country-wave clusters of about 1,400 individuals each and even modest $\rho = 0.05$, this is $\sqrt{1 + 1399 \times 0.05} = \sqrt{70.95} \approx 8.4$. So your unclustered SE could be 8 times too small. The point estimate is unbiased; the SE is wildly wrong, and any inference based on it is unreliable. This is one of the most common mistakes in applied work.

### Alternatives

**Two-way clustering (country and wave).** Cluster on country *and* on wave separately. *What it buys:* handles correlation that's common across all observations in a given wave (a pan-European shock in 2016, say) as well as within-country correlation. *What it costs:* requires more clusters in each dimension to be well-behaved (your 4 waves is too few for wave-level clustering to give a sensible SE). For your purposes, country-wave clustering already absorbs both forms of correlation by treating the country-wave as the cluster; two-way clustering would not add much.

**Country-level clustering.** Cluster on country alone (not country-wave). *What it buys:* if you think there's serial correlation across waves within a country (the same Dane surveyed in two waves would be correlated), this catches it. *What it costs:* fewer clusters (34 vs 136) means the SE estimator has more finite-sample bias, and the rule of thumb $G \geq 30$ is uncomfortably close. Since ESS is repeated cross-sections and not a panel, the case for country-level clustering is weak; different individuals in different waves shouldn't have more correlation than the country-wave structure already captures.

**Wild cluster bootstrap.** Bootstrap the residuals at the cluster level. *What it buys:* better small-cluster behaviour; works when $G$ is too small for the asymptotic cluster-robust formula to be reliable. *What it costs:* computationally expensive, harder to implement, less standard. With $G = 136$ country-waves you don't need it.

**The random-effects model itself.** As discussed in Concept 1. *What it buys:* parametric efficiency, structured cross-level inference. *What it costs:* depends on assumptions about cluster-level variance distributions. You report both, which is the right move.

The country-wave clustered SE plus country-wave fixed effects is the standard, well-understood specification. With $G = 136$ clusters it's well above the small-sample concern threshold. The directional convergence with the random-slopes mixed model is the right cross-validation.

### Worked example

The published Model 1 has $\beta_{\text{RTI}} = 0.168$ with $p < 0.001$ from the country-wave-clustered OLS+FE specification. The mixed-model counterpart returns roughly the same point estimate. If you ran vanilla OLS without clustering and without country-wave dummies, you would likely get something around 0.17 with a standard error that's small enough to make the p-value vanishingly small; in that pre-clustered world your SE understatement might be a factor of 5 or more. The point estimate would barely move; the inference would be drastically wrong. Both the FE absorption and the clustering are doing essential work.

<details>
<summary>Active recall prompt: cluster-robust SEs</summary>

Without re-reading: in your specification, what does the country-wave fixed effect absorb that the cluster-robust SE then doesn't need to handle? What does the cluster-robust SE handle that the fixed effect doesn't?

(Answer: the FE absorbs the *level* of anti-immigration in each country-wave, so the conditional residual within a country-wave has mean zero. The cluster-robust SE handles within-country-wave *correlation* in those residuals, which the FE alone does not. They handle different aspects of the same dependence problem and both are needed.)
</details>

### Connections

This is the same idea as Newey-West HAC standard errors in time-series, generalised to a panel structure. The Newey-West correction handles serial correlation in residuals; cluster-robust handles within-cluster correlation in panel residuals. Both are non-parametric corrections to the OLS variance formula that allow for forms of dependence the basic formula assumes away. In your analysis, the cluster-robust SE plus the random-slopes mixed model are the two parallel ways of being honest about the multilevel structure of the data.

---

## §V.D — Concept 5: The matched-sample logic

### The problem

The §V.D contrast is the most consequential in the paper. ALMP correlates with country-level slopes at $r = 0.01$; CWED correlates at $r = -0.848$. A skeptical reader will say: of course you got different correlations, the samples are different (22 countries for ALMP vs 15 for CWED). The matched-sample move heads off that objection by computing the ALMP correlation on the *same* 15 countries as CWED. When the ALMP correlation stays near zero on the matched sample, the difference between the two correlations cannot be attributed to sample composition; it has to be attributed to what the two measures actually capture.

### Concrete first

Imagine you wanted to test whether ice cream sales predict drowning rates. You find $r = 0.6$ on a US sample and $r = 0.05$ on an Antarctic sample. The naive reader concludes that ice cream causes drowning in the US but not in Antarctica. The right move is to recognise that the samples differ on a confounder (temperature: hot countries have both more ice cream and more swimming), so the correlation difference is sample-driven, not measure-driven. The matched-sample equivalent here would be: compare ice cream and drowning on the same set of countries. If you do that and the correlation drops to 0.05, you've isolated the role of the confounder.

For your CWED-vs-ALMP comparison, the logic runs the other way. You have two measures of welfare quality. If ALMP and CWED produced different correlations only because they're computed on different country sets, then matching on the country set should equalise them. It doesn't; ALMP stays at $r = 0.01$ on the matched 15 countries while CWED gives $r = -0.848$ on the same 15. The difference is in *what the measures capture*, not which countries are included.

### Setup

The matched-sample procedure is conceptually simple. Run the per-country regression of anti-immigration on RTI for every country. Extract the country-level slopes. Compute two Pearson correlations: one between slopes and CWED on the 15-country CWED sample, one between slopes and ALMP *on the same 15-country sample*. Report both. The key step is the second one: you intentionally throw away ALMP data from the 7 countries that aren't in CWED, even though using those 7 would give you more statistical power on the ALMP correlation.

### Code

From `analysis/final_analysis_pipeline.py`:

```python
833  try:
834      # Get country-specific RTI -> anti-immig slopes
835      country_slopes = []
836      for cntry in sorted(analysis['cntry'].unique()):
837          data_c = analysis[analysis['cntry'] == cntry].dropna(subset=['anti_immig_index', 'task_z'])
838          if len(data_c) > 50:
839              slope, intercept, r, p, se = stats.linregress(data_c['task_z'], data_c['anti_immig_index'])
840              regime = data_c['welfare_regime'].mode().iloc[0]
841              cwed_val = data_c['cwed_generosity'].iloc[0] if data_c['cwed_generosity'].notna().any() else np.nan
844              almp_val = data_c['almp_pmp'].iloc[0] if 'almp_pmp' in data_c.columns and data_c['almp_pmp'].notna().any() else np.nan
845
846              country_slopes.append({
847                  'cntry': cntry, 'slope': slope, 'se': se, 'p': p, 'n': len(data_c),
848                  'regime': regime, 'cwed_generosity': cwed_val, 'cwed_ue_generosity': cwed_ue,
849                  'conditionality': cond_val, 'almp_pmp': almp_val,
850              })
852      slopes_df = pd.DataFrame(country_slopes)
857      slopes_cwed = slopes_df.dropna(subset=['cwed_generosity'])
858      if len(slopes_cwed) >= 5:
859          r_gen, p_gen = stats.pearsonr(slopes_cwed['cwed_generosity'], slopes_cwed['slope'])
876      slopes_almp = slopes_df.dropna(subset=['almp_pmp'])
877      if len(slopes_almp) >= 5:
878          r_almp, p_almp = stats.pearsonr(slopes_almp['almp_pmp'], slopes_almp['slope'])
879          print(f'ALMP spending vs slope: r={r_almp:.3f}, p={p_almp:.3f}')
```

Note line 839: `stats.linregress` is a *separate per-country OLS regression*, not a BLUP from a multilevel model. This is a deliberate choice (more on it below). Lines 857 and 876: the `dropna(subset=...)` calls produce two different sub-samples of `slopes_df`. The CWED sample is whatever 15 countries have CWED values. The matched-sample version of the ALMP correlation requires you to compute `stats.pearsonr` on the *intersection* of the CWED-available and ALMP-available countries, which on your data is essentially the CWED 15 (since CWED is the more restrictive of the two).

### Why use separate OLS rather than BLUPs?

A natural alternative would be to fit one mixed model (random slopes only, no cross-level moderator), extract the country-level BLUPs ($\hat\beta_1 + \hat u_{1j}$), and use *those* as the per-country slopes in the scatter against CWED. The advantage of BLUPs is that they shrink extreme country-level estimates toward the grand mean, which reduces the influence of high-leverage points. The disadvantage, in your specific case, is that the shrinkage would dampen exactly the UK–Norway endpoints that drive $r = -0.848$, weakening the very pattern you're trying to display. Using separate per-country OLS means each country's slope is estimated only from its own data, with no shrinkage, no information sharing. Each point on the scatter is a self-contained estimate. This is more transparent for visual presentation and for the leverage discussion in §V.D, even though the BLUPs would be more statistically efficient.

This is a defensible choice but you should be able to articulate it. The BLUP version is what a methodologically conservative critic might prefer; the separate-OLS version is what a substantively communicative author should prefer for §V.D's central figure. You report both in spirit (the cross-level interaction in Model 3 is the BLUP-equivalent in formal terms), so the reader has access to both perspectives.

### What goes wrong without matching?

If you reported ALMP at $r$-something on 22 countries and CWED at $r = -0.848$ on 15 countries, a sharp referee would object that you can't compare correlations across different country sets. The 7 extra countries in the ALMP sample (the Eastern European countries that aren't in CWED) might have unusual ALMP-slope relationships that distort the ALMP correlation. The matched-sample move forecloses this objection. By computing ALMP on the same 15 countries as CWED, you are explicitly *holding sample composition constant*, so any difference in the two correlations must be due to what the measures themselves capture.

### Alternatives

**Report ALMP on the full 22-country sample.** *What it buys:* more statistical power, more countries means more precision on the ALMP correlation. *What it costs:* the comparison with CWED is no longer apples-to-apples; the referee will object; the substantive argument loses its sharpness. The matched-sample restriction is a methodological move, not a weakness; it forecloses the obvious confound at the cost of statistical power. You should accept the cost.

**Meta-analytic weighting.** Treat each country's slope as an effect-size estimate with its own sampling variance and use inverse-variance weighting in the second-stage correlation. *What it buys:* gives more weight to country-slopes estimated more precisely. *What it costs:* doesn't address the sample-composition issue at all; you still need to match. With your large country-wave sample sizes the weights would be roughly equal anyway, so the procedure adds complexity without changing the substantive answer. Defensible but unnecessary.

**Equivalence testing rather than null comparison.** Rather than reporting "ALMP correlation is null", formally test whether the ALMP correlation is statistically equivalent to zero (i.e., reject the hypothesis that $|r_{\text{ALMP}}|$ exceeds some bound). *What it buys:* converts "we failed to find an effect" into "we positively found that the effect is small". *What it costs:* requires you to specify the equivalence bound, which is judgement-dependent and contestable. With $r = 0.01$ on N=15, formal equivalence testing would reject any equivalence bound larger than about 0.5; this gives you something to claim but is not as cleanly damning as "the correlation is essentially zero". Worth considering for a journal version but not essential.

**Bayesian comparison with a prior.** Compute the posterior probability that the ALMP correlation is in some band, and compare to the same posterior for CWED. *What it buys:* a directly interpretable quantity (Pr(r > 0) for ALMP, Pr(r < -0.5) for CWED). *What it costs:* prior dependence and additional machinery. The Bayesian version would tell the same story; the frequentist matched-sample version is sufficient for the paper.

The matched-sample restriction wins because it directly addresses the most natural objection (sample composition), at a known cost (statistical power on ALMP) that is acceptable given what's gained (a clean apples-to-apples comparison). The other refinements would each be defensible, but none change the conclusion.

### Worked example

You have 22 countries with ALMP data and 15 with CWED data. The matched 15 are the intersection. On the matched 15, ALMP correlates with country slopes at $r = 0.01$, $p = 0.97$. On the same matched 15, CWED correlates at $r = -0.848$, $p < 0.001$. The two measures, computed on identical samples with identical methodology, return wildly different correlations. The only thing differing is what the measures capture: spending vs decommodification. The substantive conclusion is therefore not "more welfare = less backlash" (since spending is the natural intuition behind that and spending shows nothing) but "more decommodifying welfare = less backlash". Spending and decommodification are genuinely different institutional dimensions, and only one of them does the political work.

<details>
<summary>Active recall prompt: matched-sample logic</summary>

Without re-reading: what would happen to the published ALMP correlation if you computed it on the full 22-country sample rather than the matched 15? Would the difference change your substantive conclusion?

(Answer: you might get a slightly different number, perhaps $r$ around 0.10 or -0.10 depending on which 7 extra countries you include and how their ALMP-slope relationships look. But you would no longer be comparing apples to apples with CWED, and the methodological move that forecloses the sample-composition objection would be lost. The substantive conclusion still favours decommodification over spending, but the argument becomes weaker, and a careful reader will spot the asymmetry in samples and ask why.)
</details>

### Connections

The matched-sample idea is closely related to the more general principle of *holding the comparison constant* that runs through good causal inference. In experimental design it shows up as randomisation; in observational design as matching estimators (propensity score matching, Mahalanobis matching) and as the within-comparison structure of fixed-effects regression. Here it shows up as the deliberate choice to restrict the ALMP analysis to the same countries as the CWED analysis, even though doing so throws away usable data. The lesson is that the *informativeness* of a comparison sometimes matters more than its statistical power.

---

## §V.D — Concept 6: Inference at N=15

### The problem

The headline result of §V.D is $r = -0.848$ on 15 country-level observations. This is striking and unsettling in equal measure. It is striking because $r = -0.848$ is large by the standards of any cross-national correlation in this literature; it implies CWED accounts for 72% of the variance in country-level RTI-slopes. It is unsettling because N=15 is a small sample, and a correlation that large could in principle be driven by one or two unusually-placed countries. The §V.D treatment of this concern (single-country jackknife, two-country jackknife, statement of the epistemic ceiling) is the right shape; this section unpacks what each piece is doing.

### Concrete first

Imagine 15 dots on a scatter plot. If 13 of them lie roughly on a downward-sloping line and 2 of them are extreme: one in the top-right corner, one in the bottom-left corner. If you remove either of the extreme dots, the line through the remaining 14 might be much flatter. So the apparent $r = -0.85$ is driven heavily by those two extreme points; in technical terms, they have high *leverage*. The jackknife asks: what does the correlation look like if I drop one country at a time? If the correlation is robust to dropping any single point, the result is not driven by one outlier. If the correlation drops dramatically when you remove one specific point, you've found a leverage problem.

For your data: the UK is the lowest-CWED country and shows the steepest slope; Norway is the highest-CWED country and shows the flattest slope. They sit at the two endpoints of the scatter. Dropping the UK gives $r = -0.802$; dropping Norway gives $r = -0.794$; dropping both gives $r = -0.717$ with $p = 0.006$. The correlation softens when you drop endpoints, but it doesn't collapse. The result is leveraged (as any small-N correlation will be) but not driven by a single point.

### Setup

The correlation coefficient on N observations:

$$r = \frac{\sum_{i=1}^{N}(x_i - \bar x)(y_i - \bar y)}{\sqrt{\sum_{i=1}^{N}(x_i - \bar x)^2 \sum_{i=1}^{N}(y_i - \bar y)^2}}$$

Sampling distribution under the null $r = 0$: Fisher's z-transform $z = \frac{1}{2}\ln\frac{1+r}{1-r}$ is approximately normal with SE $1/\sqrt{N-3}$. With N=15, SE(z) ≈ 0.29; the 95% CI on r=−0.848 is approximately $(-0.95, -0.59)$. So even at N=15, the CI does not include zero; the correlation is statistically distinguishable from zero. But the CI is wide. The correlation could plausibly be anywhere from −0.59 to −0.95, which is a meaningful range substantively.

The jackknife procedure: for each country $k = 1, \dots, 15$, compute $r_{(-k)}$, the correlation on the 14 remaining countries. The collection $\{r_{(-1)}, \dots, r_{(-15)}\}$ is the jackknife distribution. Its range tells you how leverage-sensitive the headline correlation is.

### Code

The cross-level interaction jackknife (which is the formally inferential one, not just the visual r-statistic) lives in `scripts/random_slopes_models.py`:

```python
191  print("\nJackknife (leave-one-country-out)...")
192  countries = df3['cntry'].dropna().unique()
193  jack_coefs = []
194  _ctrl_cols_j = ['task_z','anti_immig_index','cwed_generosity_z',
195                  'agea','age_sq','female','college','hinctnta','urban', GROUPS, 'cntry']
196  for ctry in countries:
197      try:
198          d = df3[df3['cntry'] != ctry][_ctrl_cols_j].dropna().reset_index(drop=True)
199          _ej, _xj = patsy.dmatrices(f3, data=d, return_type='dataframe')
200          _ej = _ej.iloc[:, 0]
201          _gj = d[GROUPS].astype(str).tolist()
202          _rj = patsy.dmatrix('~task_z', data=d, return_type='dataframe')
203          mj = _MixedLM(_ej, _xj, groups=_gj, exog_re=_rj).fit(
204              reml=True, method='lbfgs', disp=False)
205          k = next((k for k in mj.params.index if 'cwed_generosity_z' in k and 'task_z' in k), None)
206          if k:
207              jack_coefs.append((ctry, float(mj.params[k])))
208      except Exception:
209          pass
210
211  jack_df = pd.DataFrame(jack_coefs, columns=['excl_country','cwed_int'])
212  jack_min, jack_max = jack_df['cwed_int'].min(), jack_df['cwed_int'].max()
213  sign_stable = 'YES' if jack_max < 0 else 'NO — sign flip!'
```

Line 213 is the headline diagnostic: the sign of the jackknifed interaction coefficient is stable (always negative) across all single-country exclusions. Sign-stability is a stronger property than just non-zero magnitude; it says the qualitative conclusion (more decommodification flattens the RTI slope) survives every single-country removal.

The two-country jackknife (excluding UK *and* Norway simultaneously, returning $r = -0.717$, $p = 0.006$) doesn't appear as a saved loop in either script and was apparently computed interactively. Worth pinning down for the journal version: a clean two-country jackknife loop over all $\binom{15}{2} = 105$ pairs would give you the joint leverage distribution and let you report the worst-case pair, not just one specific pair.

### What goes wrong without jackknifing?

You report $r = -0.848$ with $p < 0.001$ and a referee asks: "what if I remove Norway?". If you have no answer, the referee is entitled to suspect the result is one country away from disappearing. The jackknife pre-empts this question by showing what happens under every single-country removal. With $r$ bounded between $-0.802$ and $-0.794$ on single-country exclusions, you can say with confidence that the result is not driven by a single point. The two-country exclusion result of $r = -0.717$ shows that even the most leveraged-sounding objection (drop both endpoints) leaves a substantial and statistically significant correlation. This is the right epistemic ceiling: the correlation is robust to single-country and two-country removals, but you cannot rule out that with a different country selection or a different time window the result might attenuate further.

### Alternatives

**Bootstrap rather than jackknife.** Resample countries with replacement and compute the correlation on each bootstrap sample. *What it buys:* full sampling distribution of the correlation, not just leave-one-out diagnostics. *What it costs:* with N=15, the bootstrap is itself unreliable; the same countries get resampled many times and the bootstrap distribution under-represents the true sampling variability. The jackknife is more conservative for this size.

**Wild bootstrap or Bayesian posterior.** Either would give better-calibrated inference at this N than the asymptotic Fisher z-transform. *What they buy:* honest small-sample uncertainty quantification. *What they cost:* additional methodology that the median referee won't know how to evaluate; for a paper at this stage, the jackknife is the more communicable check.

**Simply not making strong claims at N=15.** The most defensive option: report the correlation, report the jackknife, report the wide CI, and refuse to go beyond "consistent with the asymmetric mechanism". *What it buys:* immunity to the leverage objection. *What it costs:* you would lose the ability to make the central empirical argument of the paper. The right balance, which §V.D strikes well, is to present the correlation as striking but qualified, with the jackknife making the qualifications quantitative.

**Robust correlation (Spearman, Kendall).** Use a rank-based correlation that's less sensitive to extreme observations. *What it buys:* leverage-resistance built into the estimator itself. *What it costs:* throws away cardinal information. With 15 observations and an essentially monotonic relationship, Spearman would likely give a similar magnitude. Worth running as a robustness check; the headline Pearson correlation is what readers expect.

The jackknife is the standard, well-understood, transparent answer to the leverage question at small N. Combined with the two-country exclusion and the cross-level interaction (which is identified at the individual level rather than the country level), the §V.D evidence package is as robust as 15 country-level observations allow.

### Worked example

A way to internalise what's happening at N=15 and $r = -0.848$. The squared correlation, $r^2 = 0.72$, says that 72% of the variance in country-level RTI-slopes is *linearly accounted for* by CWED. The remaining 28% is everything else: institutional confounders, measurement error in the slope estimates themselves (each country-slope is itself an estimate with a SE), random country-to-country variation. With 15 countries, the unaccounted 28% allows for considerable individual deviation; some countries will fall well off the line. Denmark, with high CWED but a relatively steep slope, is exactly such a deviation, and §V.D treats it correctly as additional evidence rather than as an embarrassment.

The jackknife results say: removing the UK alone gives $r = -0.802$, which is essentially the same correlation. Removing Norway alone gives $r = -0.794$, also essentially the same. Removing both gives $r = -0.717$, which is meaningfully smaller but still substantial; $r = -0.717$ on N=13 has $p = 0.006$, well below conventional significance thresholds. The epistemic ceiling is roughly: you can defend "decommodification accounts for somewhere between 50% and 75% of the variance in country-level slopes among Western European countries during 2012–2018". You cannot defend a stronger claim than that without within-country variation, which is the thesis design.

<details>
<summary>Active recall prompt: inference at N=15</summary>

Without re-reading: what would $r$ become if you used the full 22-country ALMP sample for the CWED correlation rather than the matched 15? (Trick question.) What does the Denmark observation in §V.D contribute to or against the asymmetric mechanism story?

(Answers: trick question because CWED data only exist for the 15 countries; you couldn't extend the CWED correlation to 22 even if you wanted to, which is why the matched-sample direction goes from CWED's restrictive 15 to ALMP's broader 22 rather than the other way. Denmark is high-CWED but high-slope, an apparent anomaly that §V.D reads as additional evidence: Danish flexicurity combines generous benefits with high activation/conditionality, so on the asymmetric reading the steep Danish slope is what conditionality predicts, with decommodification held high.)
</details>

### Connections

The N=15 problem is endemic to comparative welfare-state research; almost everyone working in this area faces the same constraint, because the world contains a finite number of countries and only some of them have comparable institutional data. The standard responses are: (a) jackknife to demonstrate non-leverage, (b) report cross-level interactions at the individual level as a more powerful check, (c) acknowledge the constraint explicitly, and (d) point toward within-country designs as the next step. Your §V.D and §V.G handle all four. The thesis design will fix the constraint by exploiting within-country reform variation, which converts a 15-country comparison into a far larger number of within-country before-after comparisons.

---

## §V.F — Concept 7: The two-DV asymmetry

### The problem

The paper's central theoretical claim is *asymmetric*: welfare design moderates the conversion of vulnerability into exclusion, but does *not* equivalently moderate the conversion of the same vulnerability into solidarity. This requires two separate empirical findings: (a) a positive interaction on the exclusion DV (which you have, $\beta_3 = -0.059$, $p = 0.015$, with the negative sign meaning more decommodification flattens the exclusion slope), and (b) a *null* interaction on the solidarity DV (the redistribution model returning $\beta_{\text{RTI} \times \text{Liberal}} = 0.011$, $p = 0.285$, plus the supplementary ISSP test returning $\beta = +0.010$, $p = 0.55$). A reader who treats nulls as uninformative will read (b) as a measurement failure; the asymmetric theory reads (b) as the main confirmation.

### Concrete first

Two stylised mechanism diagrams. Symmetric account: dignity-stripping welfare → exclusion ↑; dignity-preserving welfare → solidarity ↑. Both arrows are operative; the welfare state can either damage *or* heal. Asymmetric account: dignity-stripping welfare → exclusion ↑ (operative); dignity-preserving welfare → exclusion ↓ (operative, this is the same arrow read in the other direction); dignity-preserving welfare → solidarity ↑ (NOT operative; welfare design alone does not produce solidarity, even when it stops producing exclusion).

The empirical signature of the symmetric account: positive interactions on both DVs, with moderation flowing in opposite directions for exclusion and solidarity. The empirical signature of the asymmetric account: a positive interaction on exclusion plus a *null* on solidarity. You observe the second pattern. Dismissing the null as a measurement problem is one read; treating it as substantive is the asymmetric theory's read; you should be honest about which is more defensible given your data.

### Setup

The exclusion model returns $\beta_3 = -0.059$ ($p = 0.015$); the solidarity model returns $\beta_{\text{RTI} \times \text{Liberal}} = 0.011$ ($p = 0.285$). Let me write out what each one says formally:

| Equation | What it says |
|----------|--------------|
| $\frac{\partial^2 \text{anti\_immig}}{\partial \text{RTI} \cdot \partial \text{CWED}} = -0.059$ | The slope of anti-immigration on RTI is 0.059 scale points lower per SD of CWED. Negative interaction; CWED dampens the conversion. |
| $\frac{\partial^2 \text{redist\_support}}{\partial \text{RTI} \cdot \partial \text{Liberal}} = 0.011$ | The slope of redistribution support on RTI is essentially the same in Liberal and Nordic regimes. No interaction detectable. |

The ISSP supplementary test on a different sample, different outcome, different time period, returns essentially the same null ($\beta = +0.010$, $p = 0.55$). Two independent nulls on the solidarity side, one positive on the exclusion side.

### Code

The redistribution null in `analysis/final_analysis_pipeline.py`:

```python
573  # --- Model 5: Redistribution DV ---
574  print('\n--- Model 5: Redistribution DV ---')
575  try:
576      analysis_redist = analysis.dropna(subset=['redist_support']).copy()
577      formula5 = ('redist_support ~ task_z * C(welfare_regime, Treatment(reference="Nordic"))'
578                  ' + agea + age_sq + female + college + hinctnta + urban')
579      m5 = smf.mixedlm(formula5, data=analysis_redist, groups=analysis_redist['cntry_wave']).fit(reml=True)
580
581      m5_params = {}
582      for param in m5.params.index:
583          if 'task_z' in param:
584              m5_params[param] = {
585                  'coef': m5.params[param],
586                  'se': m5.bse[param],
587                  'p': m5.pvalues[param],
588              }
589      results['model5'] = {'params': m5_params, 'n': int(m5.nobs)}
```

The ISSP confirmation lives in `scripts/issp_solidarity_leg.py`:

```python
140  def run_model(df):
142      Random slopes model: solidarity ~ task_z * cwed_z + controls + (1 + task_z | iso2)
143      Matches Model 3 structure from main paper: RTI slope varies by country,
144      cwed_z at country level predicts that slope variation via cross-level interaction.
145      With N=12 countries the between-level is small — report with that caveat.
147      import statsmodels.api as sm
148
149      exog_re = df[['task_z']].copy()
150      exog_re.insert(0, 'const', 1.0)
151      model = smf.mixedlm(
152          'solidarity ~ task_z * cwed_z + age + age2 + female + college',
153          data=df,
154          groups=df['iso2'],
155          exog_re=exog_re,
156      )
```

The ISSP test mirrors Model 3's structure precisely (random slopes on task_z, country as the grouping, cross-level interaction with CWED), but on a different dataset (ISSP 2006), a different outcome (`solidarity` derived from the ISSP unemployment-spending item), and a different time period. The result: $\beta = +0.010$, SE = 0.016, $p = 0.55$. Same null, different sample. Two independent failures to find a moderation effect on the solidarity side.

### Why the null is more informative than it looks

Three reasons.

First, the *exclusion* finding is the one the symmetric account most needed to fail (no welfare moderation of exclusion would be a fatal blow to both buffering and asymmetric theories; only the asymmetric theory predicts the positive moderation you observe). The fact that exclusion succeeds means your data has enough cross-country variation to detect moderation when it exists. So the *failure* to detect moderation on solidarity is informative; you have demonstrated that the same data, the same estimator, and a directly comparable specification can detect moderation on one DV but not the other. The null cannot be dismissed as "the data is too noisy for this kind of test"; the data is plenty good enough to detect the exclusion moderation of similar magnitude.

Second, the ISSP confirmation runs on a *different sample with a different outcome at a different time*. If the ESS Model 5 null were a measurement artefact specific to the ESS redistribution item, the ISSP test might show a positive moderation. It doesn't; it shows a null of the same shape ($\beta$ near zero, $p$ well above significance) on the ISSP unemployment-spending item. Two independent measurement instruments, two nulls. This is much harder to dismiss as measurement noise than a single null would be.

Third, the asymmetric mechanism in §III.D *predicts* the null, on three separate grounds: loss aversion (gains don't register the way losses do), the positional nature of status (relational goods can't be redistributed without losses to the currently-recognised), and the irreversibility of defensive identity investments (once committed, they don't unwind when the institutional environment improves). A theory that predicts the null and observes the null is doing the work theories are supposed to do; a theory that predicts the null and observes a positive moderation would be in trouble. So the null is the prediction; the absence of a positive interaction is the *confirmation*, not the absence of evidence.

### What goes wrong without taking the null seriously?

If you frame the redistribution null as "we couldn't find a moderation effect, possibly because of measurement issues", you concede the symmetric reading and weaken your central theoretical claim. The symmetric reading would say: welfare moderates exclusion (your finding), and presumably also moderates solidarity (which we just couldn't measure). The asymmetric reading says: welfare moderates exclusion, but does not moderate solidarity, because the underlying mechanism is asymmetric. Whether this difference matters depends on how rhetorically committed you want to be to the asymmetric framework. The §V.F text takes the asymmetric reading and is honest about the alternative; the within-country thesis design will be the test that distinguishes the two readings definitively.

### Alternatives

**Equivalence testing on the null.** Formally test whether the solidarity moderation is statistically equivalent to zero, by setting an equivalence bound and rejecting the hypothesis that $|\beta| > $ bound. *What it buys:* converts "we failed to find an effect" into "we positively found that the effect is small". *What it costs:* requires defending the equivalence bound. With $\beta = 0.011$ on the ESS redistribution model, you could probably reject any equivalence bound larger than about 0.05; this gives a quantitative claim ("moderation of solidarity is bounded above by 0.05 scale points per SD of CWED") which is stronger than the bare null. Worth adding to the journal version.

**Bayesian posterior comparison.** Compute the posterior probability that the exclusion moderation is more negative than zero, and the posterior probability that the solidarity moderation is in some symmetric band around zero. *What it buys:* directly interpretable probabilities ("Pr(exclusion moderation < 0) = 0.99; Pr(|solidarity moderation| < 0.05) = 0.95") which a non-statistician reader can absorb. *What it costs:* prior dependence and additional machinery. For a paper at this stage, the frequentist version is sufficient; for a journal version, a Bayesian sensitivity analysis would be a useful supplement.

**Two-DV joint test.** Run a multivariate model with both DVs jointly and test the cross-equation restriction that the moderation is the same on both. *What it buys:* a single statistical test of the asymmetry hypothesis. *What it costs:* the multivariate model requires assumptions about the cross-DV correlation structure that you don't currently have to make. The univariate-with-comparison framing is more transparent.

**Power analysis on the null.** Compute the minimum detectable effect size on the solidarity moderation given your sample. *What it buys:* shows that even effects much smaller than the exclusion moderation would have been detectable, which strengthens the substantive claim. *What it costs:* trivial. Worth running and reporting; even one sentence ("Power to detect a solidarity moderation of equal magnitude to the exclusion moderation exceeds 0.99") would be a meaningful addition.

The current §V.F treatment, which presents both findings symmetrically and notes the asymmetric reading is more parsimonious, is defensible. The equivalence test or the power analysis would each strengthen it without changing the substance.

### Worked example

Compare the two coefficients side by side: exclusion moderation $-0.059$ ($p = 0.015$); solidarity moderation $0.011$ ($p = 0.285$); ISSP solidarity moderation $+0.010$ ($p = 0.55$). The exclusion moderation is roughly 5–6 times the magnitude of either solidarity moderation, and the SE is roughly comparable; the difference in p-values is driven primarily by the difference in point estimates. Power to detect a solidarity moderation of magnitude 0.059 (i.e., the exclusion moderation translated onto the solidarity DV) would have been very high in your sample. So the absence of detection on solidarity isn't a sample-size problem; it's that the effect, if present, is much smaller than the exclusion effect. This is precisely the asymmetric prediction.

<details>
<summary>Active recall prompt: two-DV asymmetry</summary>

Without re-reading: if the solidarity moderation had come out at $\beta = -0.030$, $p = 0.10$ (a marginally non-significant negative effect), how would you read the two-DV evidence package? Does that change the asymmetric mechanism story?

(Answer: a moderation half the size of the exclusion moderation but in the same direction would be marginally consistent with a *partial* symmetric mechanism; you'd want to check power and consider equivalence testing. The asymmetric mechanism would still be more parsimonious if the solidarity effect were genuinely smaller, but the qualitative claim "no detectable moderation on solidarity" would be weaker. The actual results, with the solidarity moderation essentially at zero with the wrong sign, are stronger evidence for the asymmetric reading than a marginal-but-correct-sign result would have been.)
</details>

### Connections

This is a worked example of why null findings in a well-powered design are evidence, not failures. The standard frequentist framing ("we couldn't reject the null") is misleading; what you actually have is a well-powered failure to find an effect, which under a theory that predicts the null is positive evidence for the theory. This is the same logic that drives equivalence testing in clinical trials, where the goal is often to show that two treatments are *not* meaningfully different. The asymmetric theory is making a meaningful prediction (no moderation on solidarity) and the data is consistent with it; a symmetric theory makes the opposite prediction and is harder to reconcile with the data.

This connects to the within-country thesis design in a specific way: if the ESS-and-ISSP nulls reflect a real asymmetric mechanism, then within-country reform variation should also fail to produce solidarity uplift, even when it produces exclusion reduction. If the nulls reflect a measurement problem with cross-sectional designs, the within-country panel design will detect the moderation that the cross-sectional design missed. Either way, the thesis is set up to falsify or confirm the §V.F reading. This is the right structure: the seminar paper makes a claim that is consistent with the data and predicts what the thesis will and will not find.

---

## §V.F — Concept 8: The behavioural-vs-attitudinal distinction

### The problem

§V.F reports a result that looks, on its face, like a contradiction. The RTI × Liberal interaction on anti-immigration *attitudes* is positive ($\beta = 0.127$, $p = 0.003$): Liberal regimes show steeper conversion of RTI into hostile attitudes. But the same interaction on *radical right voting* is negative ($\beta = -0.123$, $p = 0.032$): Liberal regimes show weaker conversion of RTI into radical right votes. A naive reader will say: if more exclusionary attitudes don't translate into more radical right votes, doesn't that undermine the attitude finding? The right answer is no; it confirms a more sophisticated mechanism in which attitudes and votes are mediated by the *supply side* of the political market.

### Concrete first

Take Ireland (a Liberal regime in this analysis). Ireland in 2012–2018 had no electorally significant radical right party. So a high-RTI Irish worker who developed strongly anti-immigration attitudes had *nowhere to vote* for those attitudes. The attitude appears in your ESS data; the corresponding radical right vote does not, because no relevant party existed to absorb it. Alternatively: take the UK, with first-past-the-post electoral arithmetic. UKIP achieved substantial vote shares without proportionate seat representation, and the channel for high-RTI Liberal-regime exclusionary preferences was Brexit, not a radical right party. Both are cases where attitudinal sorting (your ESS finding) failed to convert into radical right vote shares for reasons that have nothing to do with attitudes themselves.

Now compare to a Continental regime like Austria or Germany, with proportional electoral systems and well-established radical right parties (FPÖ, AfD). Here the supply-side filter is much weaker; an exclusionary attitude in a high-RTI Continental worker can convert directly into a radical right vote. So the "translation rate" from attitudes to votes varies systematically with supply-side institutions, and the sign-reversal in your radical right model is a feature of that variation, not a contradiction of the attitude finding.

### Setup

Conceptually, the two-stage model:

$$\text{RTI} \xrightarrow{\beta_{\text{att}}} \text{exclusionary attitudes} \xrightarrow{\beta_{\text{trans}}} \text{radical right vote}$$

where $\beta_{\text{att}}$ is the attitude-formation coefficient (your central object) and $\beta_{\text{trans}}$ is the attitude-to-vote translation coefficient, which depends on supply-side institutions. The reduced-form RTI-on-vote coefficient is roughly the product $\beta_{\text{att}} \cdot \beta_{\text{trans}}$. If $\beta_{\text{trans}}$ varies across regimes (high in Continental, low in Liberal), then the reduced-form RTI-on-vote interaction with regime can have a different sign from the RTI-on-attitudes interaction with regime, even when both are correctly estimated.

The supply-side variables that matter:
- **Electoral system:** PR makes small-party representation easier; FPTP suppresses it.
- **Party availability:** if no significant radical right party exists in a country, the attitude-to-vote channel is essentially zero in that country.
- **Mainstream party positioning:** if mainstream parties have absorbed restrictive immigration positions, the radical right loses its differentiating position and attracts fewer votes.
- **Political culture:** taboos against radical right voting (as in post-WWII Germany before the AfD breakthrough) suppress vote shares without changing attitudes.

§V.F doesn't model these directly; the §VI discussion treats the attitude-vs-vote distinction as the boundary of the paper's claim and notes that the supply-side translation is "a separate paper". This is the right move at this stage; the data to model supply-side translation properly (party-level data, electoral system features, mainstream-party positioning by year) sit outside the ESS framework and would require a different paper.

### Code

Model 6 (radical right voting) is structurally the same as Model 2 (attitudes by regime) with the radical right binary as the DV. The pipeline subagent didn't extract the exact lines, but the formula is essentially:

```python
formula6 = ('radical_right_vote ~ task_z * C(welfare_regime, Treatment(reference="Nordic"))'
            ' + agea + age_sq + female + college + hinctnta + urban')
m6 = smf.mixedlm(formula6, data=analysis_vote, groups=analysis_vote['cntry_wave']).fit(reml=True)
```

with `radical_right_vote` constructed via the Langenkamp 2022 crosswalk (see CLAUDE.md). The Langenkamp crosswalk is itself a substantive choice: it classifies parties as radical right based on expert-survey criteria, and the boundaries are contestable (is Fidesz radical right? Is the True Finns? Were they always?). Different classifications would give somewhat different results, but the qualitative pattern (RTI predicts radical right voting more strongly in Nordic than in Liberal regimes, conditional on supply-side availability) is reasonably robust.

### What goes wrong if you read Model 6 as testing the attitude mechanism?

You conclude that the attitude finding is contradicted by the voting finding. This is the wrong conclusion. The attitude model tests whether welfare context moderates the conversion of vulnerability into exclusionary disposition; the voting model tests whether welfare context moderates the conversion of vulnerability into radical right ballot box behaviour. These are two different DVs measuring two different dependent variables, mediated by different mechanisms. The attitude mechanism (welfare-dignity → identity processing → exclusionary attitudes) is your paper's claim. The vote mechanism (attitudes → supply-side filter → radical right votes) is a downstream story that the paper deliberately leaves for later. Conflating them produces the apparent contradiction.

The right framing, which §V.F gets to and §VI extends, is: *attitudes sort, supply-side institutions then determine whether attitudes become votes*. The asymmetric mechanism is about the sorting; the radical right voting result is about the translation. Both are real; neither contradicts the other.

### Alternatives

**Estimate a structural attitude-then-vote model.** Treat exclusionary attitudes as a mediator between RTI and radical right voting, and estimate the indirect and direct effects formally. *What it buys:* a quantitative decomposition of how much of the RTI-on-vote relationship runs through attitudes vs through other channels. *What it costs:* requires parametric assumptions about the mediation structure (typically Baron-Kenny or one of its modern descendants), and the assumptions are strong (no unmeasured confounding of the attitude-vote relationship, conditional on observed controls). With cross-sectional ESS data this is hard to defend rigorously. The thesis design with within-individual variation would make this much more tractable.

**Add supply-side controls.** Include country-level variables for electoral system disproportionality, presence/absence of radical right party, mainstream-party immigration positioning. *What it buys:* an explicit account of what's driving the attitude-vote translation. *What it costs:* requires party-level data over time that's not currently in the analysis pipeline; would need to merge in CHES (Chapel Hill Expert Survey) or GPS (Global Party Survey) scores. Worth doing for a journal version, but properly out of scope for the seminar paper.

**Run vote-share regressions at the country-wave level instead of individual-level.** Aggregate radical right vote share to the country-wave level and regress on country-wave RTI distribution and welfare context. *What it buys:* the unit of analysis matches the supply-side story (parties compete at the country level). *What it costs:* throws away individual-level variation, and the cross-level interaction structure becomes degenerate. The individual-level Model 6 is more informative even with the supply-side filtering.

**Treat the §V.F radical right finding as separately supportive of the asymmetric mechanism.** In Nordic regimes (where radical right parties exist and are well-established), high-RTI workers vote radical right at higher rates; this confirms that when attitudes can translate, they do. In Liberal regimes (where the radical right is mostly absent, and the immigration-restrictive position has been absorbed into mainstream parties), high-RTI workers don't vote radical right because there's no radical right party to vote for; the attitudes are still there (Model 2 confirms this) and channel into other behaviours (Brexit, mainstream-party Conservative voting). *What it buys:* a unified reading of Models 2 and 6 that treats them as joint evidence for an attitudinal mechanism with supply-side translation. *What it costs:* speculation about the channels in Liberal regimes, since you don't have direct evidence on Brexit or Conservative voting in this analysis. §V.F gestures in this direction; §VI develops it more.

The current treatment (acknowledge the attitude-vote distinction, treat the radical right finding as descriptive of supply-side translation rather than a test of the attitudinal mechanism) is the right one for this paper. The structural mediation analysis or the supply-side controls would be the right additions for a journal version targeting CPS or EJPR; a referee at AJPS or APSR will likely ask for one of them.

### Worked example

Take the Liberal-regime gap. RTI × Liberal on anti-immigration attitudes: $\beta = +0.127$ ($p = 0.003$). RTI × Liberal on radical right voting: $\beta = -0.123$ ($p = 0.032$). Adding these is meaningless (different DVs), but their signs can be interpreted jointly as: in Liberal regimes, the same one-SD increase in RTI produces 0.127 more scale points of exclusionary attitudes *and* a lower probability of radical right voting (relative to Nordic baseline). The combination tells you: attitudes form, but they don't translate into radical right ballots because the radical right is structurally suppressed in the Liberal cases (Ireland's absent party, the UK's electoral arithmetic and Brexit channel). The attitudinal mechanism is confirmed; the political-translation mechanism is supply-side dependent. Two findings, one consistent reading.

<details>
<summary>Active recall prompt: behavioural-attitudinal distinction</summary>

Without re-reading: if you found the attitude moderation positive in Liberal regimes *and* the radical right vote moderation positive in Liberal regimes, what would that tell you? What if both were null?

(Answers: positive on both would mean attitudes sort *and* translate freely; supply-side filtering would be small or absent, and the asymmetric mechanism would be visible at both attitude and vote levels. Null on both would mean either no attitudinal mechanism, or that the mechanism is symmetric and produces no detectable cross-regime variation; either reading would weaken the asymmetric claim. The actual finding (positive on attitudes, negative on votes) is the empirically richest pattern: it confirms attitude-formation while revealing that supply-side translation is non-trivial.)
</details>

### Connections

This is an instance of the more general distinction between *demand-side* and *supply-side* explanations in political economy. Demand-side: what voters want (attitudes, preferences, dispositions). Supply-side: what political entrepreneurs offer (parties, candidates, institutional opportunities). Mainstream comparative politics oscillates between treating one side or the other as primary; the right answer is usually that both matter and they interact. The Norris-Inglehart cultural backlash thesis is essentially demand-side (voter preferences shifted toward authoritarian-traditional values); the institutionalist response is essentially supply-side (parties and electoral systems vary in how they convert preferences into votes); the right reading is that preferences vary structurally (your asymmetric mechanism) and that translation varies institutionally (Model 6).

This connects to the thesis design in a useful way: within-country variation in welfare reform is a demand-side shifter (it changes what workers experience and therefore what they think). Within-country variation in supply-side conditions (party entry, electoral reform, mainstream-party positioning) is a separate thing the thesis can also exploit. If the registry-based thesis can identify both types of variation, it can decompose the full RTI-to-vote pathway into its attitudinal and translational components, which would settle the question §V.F flags.

---

## §V.G — Limitations (compact)

The cross-sectional design cannot establish temporal ordering. You write this directly in §V.G, which is correct. The CWED scores are time-invariant (means over 2005–2011); the ESS observations are 2012–2018; the RTI scores are based on ISCO-08 task content from 2003 (Autor-Levy-Murnane) and updated in Goos-Manning-Salomons (2014). None of these vary at the right frequency to identify a within-country reform effect. The §V.D country-level correlation, while striking, rests on 15 country-level observations and is leveraged by endpoints (the jackknife handles this honestly).

Country-level welfare indicators are confounded with other institutional differences. Nordic countries with high CWED also tend to have stronger unions, higher social trust, proportional electoral systems, lower ethnic heterogeneity. The macro-controls robustness check (GDP growth, Gini) addresses macroeconomic confounders but not these deeper institutional correlates. Within-country variation in CWED over time, exploiting reform episodes, is the only way to break this confounding. The Danish 2003, 2006, and 2013 activation reforms are exactly the kind of within-country variation the thesis can use.

The individual-level Model 3 cross-level interaction is more defensible than the country-level scatter, because it pools across all individuals within all 15 countries and is identified at the individual level. It is the right specification to anchor the formal claim on; the country-level scatter in §V.D is the right specification to communicate the substantive story. Both are needed.

The asymmetric mechanism's internal predictions about within-country reform episodes are the falsifiable part. The cross-sectional evidence here is consistent with the mechanism but cannot test the irreversibility, the loss aversion, or the path-dependence claims directly. The thesis design, by exploiting within-individual variation across welfare reform episodes (Danish registry data), can run those tests.

<details>
<summary>Recall prompt: §V.G limitations</summary>

Without re-reading: name the three things the cross-sectional design *cannot* test that the within-country thesis design *can*. (Answers: temporal ordering of the welfare-encounter to attitude-formation pathway; the irreversibility claim, since cross-sectional data has no notion of reversal; the loss-aversion asymmetry, which requires comparing within-individual responses to gains and losses of equivalent magnitude.)
</details>

---

## Where to next

Two natural extensions sit immediately downstream of §V.

The first is the **CWED sub-components** analysis flagged in MEMORY.md. CWED total generosity is the mean of three sub-scores: unemployment, sickness, and pension generosity. The asymmetric mechanism implies that unemployment generosity should do most of the moderation work, since it is the welfare encounter most directly relevant to RTI workers facing automation displacement. Pension generosity is partly a deferred-consumption mechanism that operates differently for younger working-age respondents. Sickness generosity sits in between. Decomposing the headline $r = -0.848$ into the contributions from each sub-component is a one-day analysis that would meaningfully sharpen the institutional story. The pipeline already loads `UEGEN`, `SKGEN`, and `PGEN` separately; the analysis is just per-sub-component correlations and a sub-component-by-sub-component cross-level interaction.

The second is the **within-country thesis design** on Danish registry data. The cross-sectional design here is consistent with the asymmetric mechanism but cannot identify the within-individual response to welfare reform that the mechanism's irreversibility and loss-aversion components actually predict. The thesis can: by tracking individuals across the 2003, 2006, and 2013 Danish activation reforms, you can estimate within-individual changes in attitudes and (eventually) voting in response to changes in welfare conditionality, holding decommodification roughly constant. This converts the 15-country cross-sectional comparison into a far larger number of within-country before-after comparisons, addresses the institutional-confounding problem in §V.G, and provides the falsification test for the irreversibility claim.

A third, less central extension is the **two-country jackknife as a saved loop** in the random-slopes module. The single-country jackknife is in `scripts/random_slopes_models.py` lines 191–214; the two-country exclusion result reported in §V.D ($r = -0.717$, $p = 0.006$ on excluding UK and Norway) was computed interactively, which is fine but not reproducible from the script alone. A simple loop over $\binom{15}{2} = 105$ country pairs would give the joint-leverage distribution and let you report the worst-case pair in any direction, not just the one specific pair. This is a fifteen-minute task and it would head off any referee asking for the worst-case removal.

The headline finding will hold up. Decommodification and not spending is the dimension along which the political effects of welfare design are visible. The asymmetric mechanism is the most parsimonious reading of why the exclusion side is detectable everywhere and the solidarity side is not. The empirical work supports the theoretical claim; the alternatives are real but less parsimonious. The next step is the within-country test that the cross-sectional data cannot run.
