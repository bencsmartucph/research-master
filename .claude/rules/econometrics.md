# Econometrics: Statsmodels, Multilevel Models, OxMetrics — Recurring Pitfalls

> Antidotes to specific failure modes Claude has caused under deadline pressure on Ben's analyses. Not a general best-practices document — only patterns that have already cost time once. Add new entries here when a recurring mistake is identified.

---

## 1. statsmodels time-series: VAR uses `k_ar`, NOT `k_ar_diff`

```python
from statsmodels.tsa.api import VAR
model = VAR(df).fit(maxlags=4, ic='aic')         # OK — VAR class
print(model.k_ar)                                 # number of lags estimated
```

`k_ar_diff` is the lag count for the **VECM** class (`statsmodels.tsa.vector_ar.vecm.VECM`), not VAR. They are different attributes on different model classes.

**Antidote:** Before writing analysis code, state in one line which class you are using and which lag-attribute it exposes. Verify against `dir(model)` if uncertain.

```python
# VAR class:    model.k_ar           (number of lags in level VAR)
# VECM class:   model.k_ar_diff      (number of lags in differenced VECM)
# ARMA class:   model.k_ar           (AR component order)
```

If a generated analysis hits `AttributeError` on `k_ar` or `k_ar_diff`, it is almost certainly the wrong attribute for the wrong class — fix the class identification first, do not paper-over with `getattr(model, ..., default)`.

---

## 2. Multilevel models with country-level predictors

A random-intercept-only specification is **degenerate** when the predictor of interest is measured at the country level (e.g., CWED generosity, welfare regime type). With no within-country variance in the predictor, the random intercept absorbs everything the country-level predictor would otherwise estimate, and the predictor's coefficient is identified only from cross-country variation that the model is also trying to absorb.

**Symptoms:** the country-level predictor's coefficient is near-zero with a giant SE, or the model fails to converge, or the within-country variance component collapses.

**Right specifications:**

| Goal | Spec |
|------|------|
| Estimate the cross-country effect of a country-level predictor | **Country fixed effects + cluster-robust SE** at country-wave level (drop random intercepts) — but then the country-level predictor cannot be identified separately from FE. |
| Estimate cross-level interaction (country-level × individual-level) | **Random slope** on the individual-level predictor + cross-level interaction term. |
| Cross-classified hierarchy (individuals nested in country-waves) | Random intercepts at country-wave level + the country-level predictor enters at level 2; verify variance components are non-zero. |

**Antidote:** Before fitting any multilevel model with a country-level moderator (e.g., `cwed_generosity`, `welfare_regime`), state explicitly:
1. What variance the country-level predictor identifies off (within or between).
2. What random terms are in the model.
3. Whether (1) and (2) are compatible.

If they aren't, rewrite the spec before running. See `metadata/theory_data_bridge.md` for which variables are at which level.

---

## 3. Outcome coding direction — verify BEFORE interpretation

Several ESS / ISSP variables have non-obvious coding directions. Misinterpreting the sign of a coefficient is one of the easiest deadline errors to make.

| Variable | Apparent meaning | Actual coding | Pre-AI fix |
|---|---|---|---|
| `gincdif` (ESS) | Government should reduce income differences | **Reverse-coded:** 1 = "agree strongly" → high redistribution support | Reverse-code into `redist_support` (1-5, higher = more support) before fitting. CLAUDE.md notes this. |
| `imueclt` / `imwbcnt` (ESS) | Immigration impact | Higher = MORE positive view; ensure index direction matches the others before averaging | Reverse-code if combining with anti-immigration items. |
| `lrscale` (ESS) | Left-right self-placement | 0 = left, 10 = right (standard) | None — but always state direction in output. |
| `trstplt` etc. (ESS trust series) | 0 = no trust, 10 = complete trust | Higher = more trust | None — but state direction. |
| ISSP value codes generally | Various | Always decode using `meta.variable_value_labels` before use | Per `domain-profile.md`. |

**Antidote — three-line spec before every regression:**

```
# Model class:           [OLS / logit / VAR / lme4 / etc.]
# Outcome direction:     [higher = more X]   ← state explicitly
# Expected sign of β:    [positive / negative, given the theory]
```

If the estimated sign is opposite of the expected sign, **recheck the outcome coding before rewriting the theory.** This is the single most common deadline-pressure mistake — re-coding a hypothesis to match a sign error.

---

## 4. OxMetrics syntax (when translating to/from Python)

OxMetrics uses different notation than statsmodels:

| Operation | OxMetrics | statsmodels |
|---|---|---|
| First difference | `Diff(var)` or `D(var)` | `var.diff()` |
| Lag-1 | `var(-1)` | `var.shift(1)` |
| Sum lag 1-4 | `var(-1, -4)` (range syntax) | `var.shift(1) + var.shift(2) + var.shift(3) + var.shift(4)` |
| ADF test | `Augm(var)` | `from statsmodels.tsa.stattools import adfuller; adfuller(var.dropna())` |
| Johansen | `Johansen` command in batch | `from statsmodels.tsa.vector_ar.vecm import coint_johansen` |

**Antidote:** When translating an OxMetrics specification to Python or vice versa, paste the exact OxMetrics syntax in a comment above the Python translation. Verifying syntax is faster than debugging a regression that ran but tested the wrong hypothesis.

---

## 5. Cluster-robust SE convention (for this research programme)

Per `domain-profile.md`: cluster at the **country-wave level** for ESS analyses, or at the **region level** for regional analyses. This is a field convention; deviating from it is a referee flag at top journals.

```python
# ESS individual-level analysis
from linearmodels.panel import PanelOLS
result = model.fit(cov_type='clustered', cluster_entity=df['cntry_wave'])
```

Do not cluster on country alone in ESS work — country-wave is the standard since ESS is repeated cross-sections, not panel.

---

## When to update this file

Add an entry when:
- A delegated analysis script hits a runtime error from wrong syntax (e.g., `k_ar` vs `k_ar_diff`).
- An interpretation is reversed because outcome coding was unchecked.
- A multilevel model fails to converge from a degenerate specification.
- Any pattern shows up in two separate sessions.

Don't add generic econometrics advice. This file is a list of antidotes to mistakes that have already happened, not a textbook.
