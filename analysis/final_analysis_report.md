# Final Analysis Report — Sorting Mechanism Paper

**Date:** 2026-03-16
**Script:** `analysis/final_analysis_pipeline.py`
**Master dataset:** `analysis/sorting_mechanism_master_v2.csv` (188,764 x 48)

---

## 1. Sample Description

| | N |
|---|---|
| **Total observations** | 188,764 |
| **Analysis sample** (complete cases, 5 main regimes) | 125,169 |
| **CWED subsample** (countries with welfare data) | 81,885 |
| **Waves** | 6, 7, 8, 9 (fieldwork 2012-2018) |
| **Countries** | 34 (32 in analysis after excluding Other) |

### Observations by Regime

| Regime | Full Sample | Analysis Sample |
|--------|------------|-----------------|
| Nordic | 27,920 | 24,100 |
| Continental | 45,863 | 35,984 |
| Liberal | 18,704 | 12,576 |
| Southern | 21,409 | 12,722 |
| Eastern | 62,327 | 39,787 |
| Other (IL, RU) | 12,541 | *excluded* |

### CWED Coverage

24 of 34 ESS countries have CWED generosity data (58.0% of observations). Missing countries: AL, CY, HR, IL, IS, ME, RS, RU, UA, XK — predominantly non-OECD or small states. Eastern European coverage is limited (only BG, CZ, EE, HU, LT, LV, PL, SI, SK have partial data, but TOTGEN is NaN for most).

**CWED generosity by regime (mean 2005-2011):**

| Regime | CWED Total Generosity |
|--------|----------------------|
| Nordic | 36.9 |
| Continental | 36.5 |
| Southern | 32.8 |
| Liberal | 31.9 |
| Eastern | NaN (insufficient data) |

---

## 2. Key Result: RTI x Liberal Interaction

### Model 2: Regime Interaction (Mixed Model)

The core finding from the overnight session is **confirmed and strengthened**:

| Interaction | Coefficient | SE | p-value |
|-------------|-------------|-----|---------|
| RTI main (Nordic reference) | 0.204 | 0.013 | <0.001 |
| RTI x Continental | 0.029 | 0.016 | 0.073 |
| RTI x Eastern | -0.147 | 0.016 | <0.001 |
| **RTI x Liberal** | **0.117** | **0.021** | **<0.001** |
| RTI x Southern | 0.019 | 0.022 | 0.376 |

**Interpretation:** A 1-SD increase in RTI is associated with 0.204 additional points on the anti-immigration index in Nordic countries. In Liberal regimes, this effect is 0.117 points *larger* (total: 0.321). The Liberal interaction is highly significant (z=5.51).

**Controls:** age, age-squared, gender, college, household income decile, urban/rural. Random intercepts by country-wave.

### Model 3: CWED Generosity Interaction (THE NEW KEY MODEL)

| Variable | Coefficient | SE | p-value |
|----------|-------------|-----|---------|
| RTI (std) | 0.216 | 0.008 | <0.001 |
| CWED generosity (std) | -0.069 | 0.064 | 0.281 |
| **RTI x CWED generosity** | **-0.056** | **0.007** | **<0.001** |

**Interpretation:** The interaction is **negative and highly significant** (z=-8.38). In countries with more generous welfare systems, the RTI-to-anti-immigration link is *weaker*. A 1-SD increase in CWED generosity reduces the RTI marginal effect by 0.056 points. This is exactly what the theory predicts.

**Substantive magnitude:** The RTI effect ranges from approximately 0.27 (1 SD below mean generosity) to 0.16 (1 SD above). The most generous welfare states (Norway, Belgium) buffer roughly 40% of the vulnerability-to-exclusion link compared to the least generous (UK).

### Model 3b: UE-Specific Generosity

RTI x UE generosity: **-0.052 (p<0.001)**. The unemployment insurance component alone drives a similar buffering effect.

### Model 3c: Conditionality

RTI x Conditionality: **-0.018 (p=0.010)**. Surprising direction — conditionality is *negatively* associated with the RTI slope, not positively as expected. However, the conditionality measure (UEWAIT + UEQUAL) may capture different things than theoretical conditionality (punitive activation vs. qualifying periods).

---

## 3. ALMP Puzzle Resolution

### The puzzle

The overnight run found: ALMP spending vs RTI->anti-immigration slopes: r=0.41, p=0.057. Countries with MORE ALMP spending showed STEEPER vulnerability-to-exclusion slopes. This contradicted the theory.

### The resolution

CWED generosity vs RTI->anti-immigration slopes: **r=-0.848, p<0.001** (N=15 countries with both measures).

**The ALMP puzzle is resolved.** The explanation is straightforward:

1. **ALMP spending measures effort, not generosity.** Countries can spend a lot on ALMPs while having punitive, conditional systems (e.g., UK's workfare). CWED's decommodification index captures whether workers can sustain a reasonable living standard *without* working — the relevant theoretical dimension.

2. **The composition of spending matters.** ALMP spending includes training, job subsidies, and direct job creation. Not all ALMP spending is "enabling" in the theoretical sense.

3. **The CWED relationship is very strong.** r=-0.848 means 72% of cross-country variation in RTI slopes is explained by welfare generosity. This is one of the strongest cross-level relationships in the data.

4. **UE-specific generosity also works:** r=-0.687, p=0.005. The unemployment benefit component alone accounts for 47% of the variance — theoretically coherent since unemployment insurance is the most directly relevant institution for automation-exposed workers.

### Country-Level Evidence

| Country | Regime | RTI Slope | CWED Generosity |
|---------|--------|-----------|-----------------|
| NO | Nordic | 0.314 | 43.0 |
| BE | Continental | 0.382 | 41.6 |
| NL | Continental | 0.358 | 38.3 |
| FR | Continental | 0.413 | 38.0 |
| SE | Nordic | 0.433 | 37.0 |
| CH | Continental | 0.350 | 37.0 |
| IE | Liberal | 0.497 | 35.2 |
| ES | Southern | 0.443 | 35.3 |
| FI | Nordic | 0.444 | 33.9 |
| DK | Nordic | 0.502 | 34.2 |
| AT | Continental | 0.426 | 34.3 |
| PT | Southern | 0.538 | 32.7 |
| DE | Continental | 0.475 | 32.1 |
| IT | Southern | 0.480 | 29.9 |
| GB | Liberal | 0.560 | 28.0 |

Notable: Norway (highest generosity) has one of the flattest slopes. GB (lowest generosity among established Western democracies) has the steepest.

**Anomaly:** Denmark has high generosity (34.2) but a steep slope (0.502). This may reflect the specific Danish flexicurity model, which combines generous benefits with high labour market flexibility — creating different dynamics than pure decommodification.

---

## 4. All Model Results

### Table 2: Main Results

| | Model 1 | Model 2 | Model 3 | Model 4 |
|---|---------|---------|---------|---------|
| **DV** | Anti-immig | Anti-immig | Anti-immig | Anti-immig |
| **Specification** | Baseline | Regime int. | CWED int. | Education triple |
| RTI (std) | 0.182*** | 0.204*** | 0.216*** | 0.136*** |
| RTI x Liberal | — | 0.117*** | — | -0.031 (n.s.) |
| RTI x CWED generosity | — | — | -0.056*** | — |
| RTI x non-college | — | — | — | 0.074* |
| RTI x Liberal x non-college | — | — | — | 0.084 (p=0.18) |
| College | -0.735*** | -0.735*** | -0.883*** | — |
| Non-college | — | — | — | 0.810*** |
| N | 125,169 | 125,169 | 81,885 | 125,169 |
| R-sq / converged | 0.182 | conv. | conv. | conv. |

### Table 3: Secondary Results

| | Model 5 | Model 6 | Model 7 |
|---|---------|---------|---------|
| **DV** | Redistribution | RR vote (logit) | Mediation |
| RTI (Nordic) | 0.044*** | 0.220*** | — |
| RTI x Liberal | 0.011 (n.s.) | -0.123* | — |
| RTI -> deservingness | — | — | -0.030*** |
| Deservingness -> anti-immig | — | — | -0.453*** |
| RTI direct (controlling deserv.) | — | — | 0.166*** |
| N | 124,075 | 110,471 | 28,860 |

---

## 5. Education Moderation

### Model 4: Triple Interaction

The triple interaction RTI x Liberal x non-college is positive (0.084) but does not reach significance (p=0.179). However, the simpler descriptive pattern is clear:

| Education | Nordic | Continental | Liberal | Southern |
|-----------|--------|-------------|---------|----------|
| Non-college slope | higher | higher | highest | higher |
| College slope | lower | lower | much lower | lower |

The RTI x non-college interaction IS significant (0.074, p=0.048): non-college workers show steeper RTI->anti-immigration slopes in ALL regimes. The regime-specific differences among non-college workers are more modest.

**Interpretation for the paper:** Education moderates the sorting mechanism. College education provides a cognitive buffer that partially breaks the vulnerability-to-exclusion link. This is consistent with the "identity switching" mechanism in Module 15: college-educated workers can construct professional identities that transcend occupational vulnerability.

---

## 6. Deservingness Mediation (Model 7, Wave 8 Only)

The Baron-Kenny sequence:

1. **RTI -> narrow deservingness:** -0.030 (p<0.001). Higher RTI is associated with slightly *less* restrictive deservingness views (unexpected direction).

2. **Deservingness -> anti-immigration (controlling for RTI):** -0.453 (p<0.001). More restrictive deservingness views are associated with *less* anti-immigration sentiment (unexpected direction — the negative sign reflects the scaling of the deservingness measure).

3. **RTI direct effect (controlling for deservingness):** 0.166 (p<0.001). The RTI effect barely changes when controlling for deservingness (from ~0.20 to 0.17), suggesting deservingness is NOT a major mediator.

**Honest assessment:** The mediation story is weak. Deservingness doesn't appear to be the primary channel through which RTI translates to anti-immigration attitudes. The mechanism is more likely direct status threat or identity switching rather than welfare entitlement logic.

---

## 7. Radical Right Vote (Model 6)

### Construction

Radical right parties were manually classified from the Langenkamp crosswalk (conservative list — only universally recognized radical right parties included). 229 party-round combinations across 20 countries.

**Overall vote rate:** 3.9% (of those who reported a vote). This is plausible for ESS waves 2012-2018.

### Sanity Check — Top 5 Countries by RR Vote Share

| Country | RR Share | Party |
|---------|----------|-------|
| AT | 11.5% | FPO |
| SI | 11.2% | SDS/SNS |
| CH | 9.2% | SVP |
| DK | 9.1% | DF |
| FI | 9.0% | PS |

These are plausible and consistent with known election results.

### Model 6 Results

RTI predicts radical right voting in Nordic countries (b=0.220, p<0.001). But the RTI x Liberal interaction is **negative** (-0.123, p=0.032) — the opposite direction from the attitudinal result! In Liberal regimes, RTI is *less* associated with radical right voting.

**Interpretation:** This apparent contradiction likely reflects the supply side. Liberal welfare states (UK, IE) simply don't have strong radical right parties during 2012-2018. UKIP's peak was brief (2014-2015) and BNP was marginal. The demand for exclusionary attitudes exists (Model 2), but the party system doesn't translate it into radical right votes in the same way.

---

## 8. Robustness Summary

The RTI x Liberal coefficient from Model 2 (OLS with country-wave FE) survives all specifications:

| Specification | RTI x Liberal | SE | p-value | N |
|---------------|--------------|-----|---------|---|
| **Main** | **0.117** | **0.035** | **0.001** | **125,169** |
| Excl. Eastern | 0.128 | 0.036 | <0.001 | 85,382 |
| No income control | 0.132 | — | <0.001 | 125,169 |
| With L-R scale | 0.116 | 0.033 | <0.001 | 113,897 |
| Jackknife mean | 0.117 | — | — | — |
| Jackknife range | [0.073, 0.161] | — | — | — |

**The coefficient is remarkably stable.** The jackknife range never crosses zero; the minimum (0.073, excl. GB) is still positive and significant.

**Interesting jackknife patterns:**
- Excluding GB *weakens* the coefficient (0.073) — GB is a key driver of the Liberal regime's steeper slope.
- Excluding IE *strengthens* the coefficient (0.161) — IE's intermediate position (high generosity + Liberal classification) makes the Liberal contrast larger when removed.
- Excluding NO weakens it somewhat (0.088) — Norway's flat slope contributes to the Nordic reference baseline.

---

## 9. Honest Assessment: What the Data Shows and Doesn't

### What the data clearly shows:

1. **RTI predicts anti-immigration attitudes** (b=0.18-0.22, p<0.001). This is robust across every specification.

2. **The RTI->exclusion link is steeper in Liberal welfare regimes** than Nordic (b=0.117, p<0.001). This survives all robustness checks.

3. **Welfare generosity buffers the link** (CWED interaction: -0.056, p<0.001). The country-level correlation is very strong (r=-0.85). This is the strongest finding in the paper.

4. **Non-college workers show steeper slopes** in all regimes. Education moderates vulnerability.

### What the data suggests but doesn't prove:

5. **The mechanism is not deservingness.** Mediation analysis shows weak and sometimes counter-directional effects. The mechanism is more likely direct status threat or identity switching.

6. **The radical right vote pattern is more complex** than the attitudinal pattern. Supply-side factors (party availability) complicate the behavioural DV.

### Caveats and limitations:

7. **CWED data ends in 2011.** We use 2005-2011 averages as time-invariant country characteristics. This is defensible (welfare generosity is slow-moving) but not ideal. The implicit assumption is that the cross-country ranking of generosity didn't change substantially between 2011 and 2018.

8. **Eastern European countries lack CWED generosity data.** The CWED analysis is effectively limited to Western Europe + a few Central European countries. Eastern European results come from the regime-based analysis only.

9. **Cross-sectional identification.** We cannot rule out that people sort into automatable occupations for reasons correlated with their political attitudes (referee concern #5). The standardized RTI coefficient partially addresses this, but a panel design would be stronger.

10. **The Denmark anomaly.** Denmark has high welfare generosity but a steep RTI slope. This doesn't break the overall pattern but does complicate the simple Nordic-as-buffer narrative. The Danish case may require separate treatment.

11. **The conditionality measure doesn't work as expected.** UEWAIT and UEQUAL capture qualifying periods, not the punitive/enabling distinction that the theory emphasizes. Better conditionality data (e.g., Knotz index) would strengthen this dimension.

---

## 10. Files Produced

### Updated Data
```
analysis/sorting_mechanism_master_v2.csv    — 188,764 x 48 (adds CWED + radical right)
analysis/final_results.json                 — all model results as JSON
```

### Figures
```
outputs/figures/fig2_sorting_pattern.pdf/png        — RTI vs anti-immig by regime (THE KEY FIGURE)
outputs/figures/fig3_marginal_effects.pdf/png        — marginal effects by regime
outputs/figures/fig4_education_moderator.pdf/png     — education moderation
outputs/figures/fig5_robustness.pdf/png              — coefficient stability
outputs/figures/fig6_cwed_vs_slopes.pdf/png          — CWED generosity vs country slopes
```

### Tables
```
outputs/tables/table1_summary_stats.csv
outputs/tables/table2_main_results.csv + .json
outputs/tables/tableA1_robustness.csv
outputs/tables/country_slopes.csv
outputs/tables/jackknife_details.csv
```

---

## 11. Recommended Paper Structure

Based on these results, the empirical section should be organized as:

1. **H1 (strong support):** Welfare regimes sort economic disruption. RTI->exclusion link is stronger in Liberal than Nordic regimes. Both regime-based (Model 2) and continuous (Model 3) specifications confirm this.

2. **The CWED story (the main contribution):** Move beyond Esping-Andersen typologies. Show that welfare *generosity* (a continuous, measurable concept) predicts the strength of the sorting mechanism. Figure 6 is powerful — r=-0.85 is a striking cross-level relationship.

3. **H2 (weak, move to appendix):** The redistribution pathway is much weaker. RTI x Liberal is not significant for redistribution attitudes. The sorting mechanism operates primarily through the exclusion channel, not the solidarity channel.

4. **Education moderation (supporting evidence):** Non-college workers drive the pattern. Present descriptively rather than relying on the insignificant triple interaction.

5. **Behavioural DV (appendix):** Report the radical right vote results but note the supply-side complication. The demand for exclusion exists (Model 2); its translation to votes depends on party system characteristics beyond the scope of this paper.

6. **Robustness (appendix):** The coefficient stability plot (Figure 5) and jackknife analysis demonstrate that the core finding is not driven by any single country.
