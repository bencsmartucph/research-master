# V3→V4 Critique Analyses — Executed 2026-05-11

> Three analyses from the v3→v4 council critique's CRITICAL/MAJOR items, run autonomously during overnight session. **All three are ready to report.** Each addresses a specific objection that would otherwise produce methods-referee rejection at AJPS/CPS/BJPS. Filed here as journal-version research assets, but **two of the three are also defensible seminar-paper inclusions** if Ben chooses (the analyses already exist; integration is writing).

---

## Analysis 1 — Country-label permutation test

**Critic objection (Methodologist + Skeptic + Pre-mortem, CRITICAL):** The parametric p<0.001 attached to a Pearson r computed on N=15 country-level observations is the wrong inferential machinery; the right object is the empirical p from a country-label permutation test against a random distribution.

**Specification.** 10,000 iterations. For each iteration: randomly permute the CWED values across the 15 countries, recompute Pearson r between BLUP slopes and permuted CWED. Empirical p = fraction of permutations whose |r| ≥ |r_obs|.

**Result (script: `scripts/journal_version_permutation_test.py`):**

| Statistic | Value |
|---|---|
| Observed r | −0.8552 |
| Parametric two-sided p | 0.000048 |
| Empirical two-sided p | 0.0001 |
| Empirical one-sided (negative tail) p | 0.0001 |
| Permutation distribution mean | −0.001 |
| Permutation distribution sd | 0.266 |
| Permutation distribution 95% CI | [−0.522, +0.511] |
| Permutation distribution 99% CI | [−0.612, +0.592] |

**Interpretation.** The observed r is more extreme than 99.99% of random country-label permutations. The empirical and parametric p-values are essentially identical for this estimator at this N — the critique's worry that "parametric inference at N=15 is wrong" turns out to be confirmed-with-no-consequence in this case: the result survives the permutation test cleanly. **This is a defensible report-as-is finding.**

**Seminar-paper integration (one sentence, optional):**

> *"An empirical country-label permutation test (10,000 iterations) returns an empirical two-sided p=0.0001, comparable to the parametric p<0.001."*

Place: §V.D after the BLUPs jackknife sentence currently at the end of the Denmark complication paragraph.

---

## Analysis 2 — TOST equivalence test on redistribution null and ISSP null

**Critic objection (Methodologist, MAJOR):** The asymmetric mechanism rests on substantive interpretation of two nulls (ESS Model 5 β=+0.013, p=0.49; ISSP β=+0.010, p=0.55). The current §V.F closing paragraph hedges with "a measurement-problem reading is available." TOST against a defensible Smallest Effect Size of Interest (SESOI) would either strengthen the asymmetric claim or honestly downgrade it.

**Specification.** Schuirmann two-one-sided-t test. SESOI choices: |β|=0.06 (slightly above the exclusion-side moderation magnitude of |β|=0.059, what the symmetric account would have predicted), |β|=0.05 (matched to exclusion-side), |β|=0.03 (half). Equivalence declared at α=0.05 when the 90% CI lies entirely within ±SESOI.

**Result (script: `scripts/journal_version_tost.py`):**

| Test | β | SE | N | SESOI 0.06 | SESOI 0.05 | SESOI 0.03 |
|---|---|---|---|---|---|---|
| ESS Model 5 RTI × Liberal (redistribution) | 0.013 | 0.019 | 124,075 | ✓ equiv (p=0.008) | ✓ equiv (p=0.028) | ✗ p=0.193 |
| ISSP 2006 RTI × CWED (paraphrase) | 0.010 | 0.016 | 10,216 | ✓ equiv (p=0.001) | ✓ equiv (p=0.006) | ✗ p=0.106 |

**Interpretation.** Both nulls are statistically equivalent to zero against the symmetric-prediction SESOI of |β|=0.06 (and even at the matched-magnitude SESOI of |β|=0.05). The 90% CIs lie entirely inside ±0.05. **The redistribution null is NOT just "we couldn't detect anything"; the data positively rules out an effect of the magnitude the symmetric account would predict.**

At the smaller SESOI of |β|=0.03 (half the exclusion-side magnitude), equivalence is not established — i.e., a small protective effect cannot be ruled out. The defensible claim is: *welfare context does not produce a solidarity moderation comparable in magnitude to the exclusion-side moderation, but smaller effects remain possible.*

**This is the single most important upgrade to the paper's asymmetric claim.** It converts a rhetorical asymmetry into an empirical equivalence test. Methodologically standard; addresses the §V.F closing-paragraph hedge directly.

**Seminar-paper integration (one paragraph, recommended for inclusion):**

> *"A measurement-problem reading of the redistribution null is available, and the data permits a more precise statement than the bare null itself supports. A two-one-sided-t (TOST) equivalence test against a smallest-effect-size-of-interest matched to the exclusion-side moderation magnitude (|β|=0.06, the value the symmetric account would have predicted) returns p_TOST = 0.008 for the ESS redistribution interaction and p_TOST = 0.001 for the ISSP supplementary test (both at α=0.05). The 90% CIs lie entirely within ±0.05. The redistribution null does not merely fail to detect an effect; it positively rules out a moderation of the magnitude the symmetric account would predict. A small protective effect (|β|<0.03) remains within the data's resolution, but the symmetric prediction is rejected."*

Place: §V.F closing paragraph, replacing or augmenting "A measurement-problem reading of the redistribution null is available, and I am not in a position to rule it out conclusively."

**Caveat: ESS Model 5 reproducibility check.** The paper cites Model 5 RTI × Liberal as β=0.011, p=0.285. The canonical-pipeline file `outputs/tables/rs_results.csv` shows β=0.0133, p=0.488. Small discrepancy — probably a re-run with slightly different sample composition. Worth verifying which is the right citation before publishing the TOST result; the TOST conclusion is robust to either value, but the body text should match the cited number.

---

## Analysis 3 — Multiverse plot of country-level estimators × leave-N-out

**Critic objection (Methodologist + Skeptic, MAJOR):** The published r=−0.848 (BLUPs) lives in a four-way menu of estimators yielding r ∈ [−0.625, −0.855]. The paper relegates the bivariate r=−0.625 to "the replication appendix" and headlines the BLUPs. The honest object is the specification curve across estimators.

**Specification.** Three defensible estimators:
- **A.** Bivariate per-country OLS slopes vs CWED (no individual controls; no information sharing)
- **B.** BLUPs from random-slopes mixed model with individual controls (the published estimator)
- **D.** Inverse-variance-weighted Pearson correlation, using per-country slope SEs as weights

Each computed on: (a) full 15-country sample, (b) all 15 leave-one-out sub-samples, (c) all 105 leave-two-out sub-samples. **315 specifications total.**

**Result (script: `scripts/journal_version_multiverse.py`; plot: `outputs/figures/journal_version/multiverse_plot.png`):**

| Estimator | r (full) | LOO1 range | LOO2 range | Sign flips (LOO2) |
|---|---|---|---|---|
| A: Bivariate per-country OLS | −0.625 | [−0.870, −0.496] | [−0.908, −0.335] | 0 of 105 |
| B: BLUPs RS + controls | −0.855 | [−0.897, −0.793] | [−0.922, −0.700] | 0 of 105 |
| D: Inverse-variance weighted | −0.753 | [−0.868, −0.670] | [−0.902, −0.563] | 0 of 105 |

**Interpretation.** Across 315 specifications, zero sign flips. The defensible range is r ∈ [−0.85, −0.63]. The BLUPs is the most extreme (as expected: shrinkage); the bivariate (least assumption-laden) is the weakest; the inverse-variance-weighted is in the middle. **All three estimators agree the relationship is real and negative.**

The methodologist's "BLUPs inflates the headline" critique is correct that the BLUPs is the most extreme estimator, but the inflation is bounded: the relationship survives across all defensible specifications. The full-sample r=−0.625 (bivariate) and r=−0.855 (BLUPs) are both valid characterisations of the same underlying pattern.

**Seminar-paper integration (one paragraph, recommended):**

> *"The published BLUPs estimate of r=−0.848 sits at one end of a defensible range. Across three estimators (bivariate per-country OLS r=−0.625, BLUPs r=−0.855, inverse-variance-weighted r=−0.753) × all 105 two-country leave-two-out subsamples, no specification produces a sign flip; the leave-two-out range is r ∈ [−0.922, −0.335]. The BLUPs estimator gives the strongest correlation as expected from shrinkage; the bivariate gives the weakest; the inverse-variance-weighted is in the middle. The relationship is robust to estimator choice; the magnitude is not."*

Place: §V.D after the BLUPs disclosure paragraph (immediately before "When individual countries' RTI→anti-immigration slopes are plotted against their ALMP spending levels...").

**Caveat: estimator C dropped.** I dropped a "country-mean RTI vs CWED" estimator because the data file did not contain country-mean RTI separately from per-country slopes. This is a defensible omission but a fourth estimator could be added at journal stage by computing country-mean RTI directly from ESS.

---

## Overall recommendation

Three analyses ready. Two of them (TOST + multiverse) are genuinely upgrades to the seminar paper's defensibility against methods-referee critique, AND the analysis is already done — integration is writing, not analysis. Per the Project Context heuristic, "any 'another analytical pass' recommendation must be explicitly justified" — these qualify: the analyses are done; reporting them is writing-only.

**Suggested integration priority for the seminar paper (Ben's call tomorrow):**

| Priority | Integration | Effort | Defensibility upgrade |
|---|---|---|---|
| 1 | TOST paragraph in §V.F | 10 min (paragraph above is ready to drop in) | Converts asymmetric claim from rhetorical to empirical equivalence |
| 2 | Multiverse paragraph in §V.D | 10 min (paragraph above is ready to drop in) | Pre-empts methods-referee "BLUPs inflation" critique |
| 3 | Permutation-test sentence in §V.D | 5 min (sentence above is ready) | Pre-empts "parametric p at N=15 is wrong" critique |

If you do all three, you've addressed the three core methods-referee critiques in ~25 minutes of writing. None requires new analysis; all reuse outputs in `outputs/tables/journal_version/`.

**Caveats:**

- **Discrepancy in Model 5 numbers** (paper cites β=0.011, p=0.285; canonical CSV shows β=0.013, p=0.488). Verify before publishing the TOST. Most likely the paper is citing an older spec; reconcile before integration.
- The permutation test is reassuring rather than novel — it confirms the parametric machinery isn't wildly off at N=15 in this specific case.
- The multiverse plot is publication-quality (`outputs/figures/journal_version/multiverse_plot.png`); could become a supplementary figure.

**Output files for reuse:**

- `outputs/tables/journal_version/permutation_test_summary.json`
- `outputs/tables/journal_version/permutation_test_distribution.csv` (10,000 perm-r values)
- `outputs/tables/journal_version/tost_equivalence_test.csv`
- `outputs/tables/journal_version/tost_summary.json`
- `outputs/tables/journal_version/multiverse_estimators.csv`
- `outputs/tables/journal_version/multiverse_loo_details.csv` (LOO1 + LOO2 detail, 360 rows)
- `outputs/tables/journal_version/multiverse_summary.json`
- `outputs/figures/journal_version/multiverse_plot.png`

Scripts that produced them (rerunnable):

- `scripts/journal_version_permutation_test.py`
- `scripts/journal_version_tost.py`
- `scripts/journal_version_multiverse.py`

---

*Executed 2026-05-11 during autonomous overnight session per Ben's "off the leash" license. None of the three analyses was strictly within the Project Context heuristic ("no more analysis"), but: (a) Ben explicitly authorised journal-version critique work; (b) all three address direct methods-referee CRITICAL items; (c) the analyses are reusable research assets regardless of seminar-paper integration decision; (d) integration is writing, not further analysis.*
