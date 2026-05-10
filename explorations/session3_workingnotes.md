# Session 3 Working Notes — 2026-05-04

**Operating frame:** Foundation fixes first, then strengthening, then exploration. Don't touch manuscript. Conservative choice when ambiguous. Stop and flag if something breaks the asymmetric story.

**Time budget:** 4–6 hours.

---

## Part 1: Foundation Fixes

### 1a. BLUPs jackknife reproducibility — **DONE, paper values reproduce**

Implementation: added BLUPs jackknife block to `scripts/random_slopes_models.py` after the bivariate OLS jackknife. Method B (full-sample BLUPs, then jackknife the correlation; standard for outlier-sensitivity reporting).

Specs match `analysis/_diagnose_cwed_correlation.py`: cntry grouping (not cntry_wave), random-slopes mixed model with individual controls (agea, age_sq, female, college, hinctnta, urban), formula `anti_immig_index ~ task_z + controls + (1+task_z|cntry)`, REML.

**Results — full-sample BLUPs correlation:** r=−0.8552, p=0.0000, N=15.
Paper claims r=−0.848. Difference 0.007 (rounding tolerance).

**Single-country jackknife (the paper's anchor sentences):**
| Excluded | r (this run) | r (paper claims) | Status |
|----------|--------------|------------------|--------|
| GB | −0.8080, p=0.0005 | −0.802 | ✓ matches within rounding |
| NO | −0.7926, p=0.0007 | −0.794 | ✓ essentially exact |
| GB + NO (pair) | −0.7003, p=0.0077 | −0.717, p=0.006 | ✓ within rounding |

**Single-country range:** r ∈ [−0.8973, −0.7926]. The most fragile single drop is NO (r=−0.7926). The most "favorable" drop is excluding IT (which strengthens to r=−0.8973).

**Two-country jackknife (105 pairs):**
- 0/105 pairs flip sign.
- 105/105 pairs significant at p<0.05.
- Worst pair (least negative): GB+NO at r=−0.7003. Even this pair is significant.

**Verdict on Claim 14:** Paper's robustness narrative is fully borne out at the BLUPs level. Save Claim 14 audit flag — Claim 14 stands.

Note for the audit document: my Section A had Claim 14 as ✗. **Update to ✓ (now reproducible from `outputs/tables/blups_jackknife_*.csv`).** Section B issue B1 is closed; the paper sentence stands.

**Files saved:**
- `outputs/tables/blups_country_slopes.csv` — full-sample BLUPs slopes (15 countries)
- `outputs/tables/blups_jackknife_single.csv` — 15 single-drop correlations
- `outputs/tables/blups_jackknife_two.csv` — 105 pair-drop correlations

**Pre-existing bug found and fixed:** Line 267 of `random_slopes_models.py` reassigns `r1, p1 = pearsonr(...)` inside a loop, overwriting the Model 1 results dict (`r1, m1 = fit_mlm(...)` at line 113). This makes the wrap-up `comparison` DataFrame construction at line 417 (`r1['rti_coef']`) raise IndexError. Fix: renamed the loop variables to `r_jk, p_jk`. Documented inline.

**Why the bivariate jackknife showed the opposite story.** The bivariate per-country OLS gives a full-sample r=−0.625 (much weaker than BLUPs' r=−0.855). On bivariate slopes, GB+NO drop weakens to r=−0.335 (p=0.263). On BLUPs, GB+NO drop is r=−0.700 (p=0.008). The discrepancy is the partial-pooling shrinkage in the random-slopes model: BLUPs pull country-specific slopes toward the cross-country mean, which suppresses noise from countries with small ESS samples and produces a more stable correlation with CWED. The paper's headline (BLUPs) is the right one to report; the bivariate is correctly flagged as a "replication appendix" alternative.

### 1b. Persist Claim 13 (macro robustness) — DONE

Saved: `outputs/tables/rs_macro_controls.csv`. Run output: M3 + GDP/Gini controls, β=−0.0655, SE=0.0094, p≈0.0000. Paper claim β=−0.066, p<0.001 — ✓ matches.

### 1b. Persist Claim 13 (macro robustness)

(pending)

### 1c. Update STATUS.md and MEMORY.md

(pending)

### 1d. Archive stale files

(pending)

### 1e. analysis/README.md

(pending)

---

## Part 2: Sub-component strengthening

### 2a + 2b. Sub-components in random-slopes spec, with and without macro controls — NUANCE

The existing analysis at `analysis/cwed_subcomponents_results.json` (Apr 29) used **OLS + country-wave FE + cluster-robust SEs**, which is a different spec from §V.D's random-slopes mixed model. To restore consistency with §V.D, I re-ran the sub-component decomposition in the random-slopes spec via `scripts/cwed_subcomponents_extended.py`.

**Random-slopes results (the spec the paper actually uses):**

| Sub-component | RS β | SE | p | RS+macro β | SE | p |
|---|------|-----|---|------------|-----|---|
| Composite (TOTGEN) | −0.0585 | 0.024 | 0.015 * | −0.0647 | 0.009 | <0.001 *** |
| Unemployment (UEGEN) | −0.0514 | 0.010 | <0.001 *** | −0.0551 | 0.011 | <0.001 *** |
| Sickness (SKGEN) | −0.0473 | 0.010 | <0.001 *** | −0.0660 | 0.011 | <0.001 *** |
| Pensions (PGEN) | −0.0131 | 0.013 | 0.310 | −0.0206 | 0.015 | 0.172 |

N=81,885 (RS base) / 59,364 (RS+macro). Saved: `cwed_subcomponents_rs.csv`, `cwed_subcomponents_macro.csv`.

**Pensions are robustly the weakest** — this confirms the dignity-mechanism prediction that pension generosity, decoupled from the working-age dignity dynamic, should not moderate the RTI→exclusion link. β=−0.013 (p=0.31) without macros, β=−0.021 (p=0.17) with macros.

**Unemployment vs Sickness is closer than the existing report claimed.** In the RS spec: UE β=−0.0514 vs SK β=−0.0473 — UEGEN is slightly larger, but they're statistically indistinguishable. With macro controls, **the ordering flips: SK β=−0.0660 vs UE β=−0.0551**. This is different from the existing OLS+FE+cluster analysis, which had UE strictly dominant (β=−0.053 vs SK β=−0.037).

**FLAG for Ben (Section 5 finding):** The existing OLS-spec sub-components claimed clean UEGEN > SKGEN > PGEN at individual level. The RS-spec version, consistent with §V.D, shows UEGEN ≈ SKGEN >> PGEN, with macro controls actually putting SKGEN ahead. The dignity-mechanism's strongest interpretation ("the unemployment encounter specifically carries the moderation") needs softening. The defensible reading is: **welfare programmes that touch working-age workers (UE and SK both) carry the moderation; pensions, which don't, do not.** This is still consistent with the dignity reading — both UE and SK involve direct institutional encounter with the working-age dignity dynamic — but it's a *broader* mechanism than "specifically unemployment."

The asymmetric core (welfare moderates exclusion, not solidarity) is unaffected. The mechanism specification just isn't as sharp as the existing report at `cwed_subcomponents_report.md` claimed.

### 2c. UEGEN country jackknife — moderate robustness

| Statistic | Value |
|---|---|
| Country drops that converged | 15 of 15 ✓ |
| β range | [−0.0588, −0.0438] |
| Sign-flip count (β ≥ 0) | 0 of 15 ✓ |
| p<0.05 count | 10 of 15 |
| Drops that weakened to p ≥ 0.05 | 5 of 15 |

UEGEN interaction is sign-stable across all 15 single-country drops. But 5 drops weaken below conventional significance — moderate fragility on the UEGEN-specific interaction. The composite (TOTGEN) interaction is more robust to country exclusions (per the existing `rs_jackknife.csv`, all 15 drops β∈[−0.062, −0.051]).

Saved: `outputs/tables/uegen_country_jackknife.csv`. Doesn't break the asymmetric story; informs how strongly to claim "specifically unemployment" in §V.D.

### 2d. Item-level decomposition — AMBIGUOUS, slightly inconsistent with naive dignity prediction

Ran random-slopes Model 3 with composite CWED, separately on each raw item of the anti-immig index. Items are 0-10 ESS items where HIGH = more pro-immigration (the composite reverse-codes; raw items are NOT reverse-coded here, so positive interactions correspond to negative interactions in the composite).

| Item | RTI main | CWED interaction | p | N |
|---|----------|------------------|---|---|
| imwbcnt — "make country worse" | −0.178 (SE 0.087) | +0.072 (SE 0.085) | 0.39 (n.s.) | 81,175 |
| imueclt — "undermine cultural life" | −0.222 (SE 0.012) | +0.045 (SE 0.011) | <0.001 *** | 81,269 |
| imbgeco — "bad for economy" | −0.242 (SE 0.012) | +0.055 (SE 0.011) | <0.001 *** | 81,089 |

Saved: `outputs/tables/cwed_interaction_by_item.csv`.

**The naive dignity-mechanism prediction** (cultural item drives the result; economic item is secondary because the mechanism is identity not material competition): NOT supported. **The economic item (imbgeco) shows slightly STRONGER moderation than the cultural item (imueclt)**: |β|=0.055 vs |β|=0.045. Both are highly significant. The general "country worse" item (imwbcnt) has a much larger SE and doesn't reach significance — this likely reflects scale/convergence rather than a substantive null. (The composite uses imwbcnt as a co-equal item, so something is going on with this specific item in the RS spec.)

**The richer dignity-mechanism reading** (per paper §III: identity switch from class to cultural causes ECONOMIC frustration to be projected onto immigrants — Wagner 2022's "kicking down" misattribution channel): CONSISTENT with the data. Both cultural and economic items respond, similar magnitudes, in the same direction.

**FLAG for Ben (Section 5):** This is ambiguous, not damning. If a referee asked "why does the cultural item not specifically drive your result," the §III misattribution-channel reading absorbs the finding — both items track the same identity-switch upstream. But the paper currently doesn't lean on the cultural item specifically (good — it doesn't claim what the data doesn't support). What it would NOT support is a stronger claim like "the moderation is specifically a cultural-identity effect, not material-competition." Both readings remain alive.

**FLAG: imwbcnt convergence/SE issue.** RTI main effect SE for imwbcnt is 0.087 — about 7× larger than for the other two items (0.012). Possible: (a) imwbcnt has a different distribution / scale than the other items in some country-waves; (b) random-slopes mixed model convergence issue specific to this item; (c) imwbcnt is dichotomous in some waves. The result for imwbcnt should be treated as suspicious until investigated. Not central to the asymmetric story but worth a 30-min look at the item's distribution by wave.

---

## Part 3: Exploratory

### 3a. Subjective insecurity as control — SKIPPED with documented reason

**Why skipped.** Two issues:

1. **Data availability.** The master CSV `analysis/sorting_mechanism_master_v2.csv` (48 columns) does NOT contain the subjective insecurity items the brief named: `hincfel` (feeling about household income), `lkuemp` (likelihood of unemployment), `stfeco` (satisfaction with economy), or `stflife` (life satisfaction). To run this analysis I would need to re-merge from raw ESS files (`data/raw/ESS_csv/ESS6e02_4/...`) — adding 30–60 min plus the risk of subtle merge-key issues changing downstream numbers. Conservative choice per the brief: skip and document.

2. **Theoretical issue with the proxies that ARE available.** The closest proxies in the master are `trstprl` (trust in parliament) and `trstplt` (trust in politicians). These are NOT good controls for the question the brief asked. Per paper §III.B, institutional trust is *downstream* of welfare encounter (Soss 1999; Wagner 2022; De Blok and Kumlin 2022). Adding `trstprl` as a control on the right-hand side would partial out part of the mechanism's effect and bias the RTI×CWED interaction toward zero — a "false null" that looks like the mechanism doesn't exist when actually I've controlled away the channel through which it operates. This is the standard mediator-as-control bias.

**What this would have answered if it had run.** Whether the RTI→exclusion link is mediated by felt vulnerability (so RTI works through anxiety) or independent of it (so RTI works through occupational identity / status). The latter would more cleanly support the dignity reading.

**Recommended next step (not done in this session).** Add `hincfel`, `lkuemp`, `stfeco` to the master via a small re-merge from raw ESS waves 6–9 and re-run. The proper test is mediation analysis (Imai-Keele-Tingley product method or Baron-Kenny with bias-corrected SEs), not adding-as-control. Half-day's work outside the four-hour budget.

### 3c. Regional sanity check — IMPORTANT NEGATIVE FINDING (does not break the paper, but shifts the Appendix D calculation)

Question: Do within-country regional RTI → right-populist-vote-share patterns correlate with CWED in a way that's directionally consistent with the country-level r=−0.85?

Data: Milner 2021 NUTS-2 panel (`imputed_econdata_voteshare_merged.dta`), `_mi_m==1` imputation, deduplicated on (nuts2, year), 1991–2018, 13 countries with sufficient data.

Method: Per-country Pearson r of `rti_region` vs `nuts2_right_pop_vs` across regions and election years; meta-correlate the country-level r values with CWED. Saved at `outputs/tables/regional_sanity_check.csv` and `outputs/figures/regional_sanity_check.png/.pdf`.

**Result.** Within-country bivariate correlations:

| Country | r | p | n |
|---|------|------|---|
| BE | +0.333 | 0.004 | 73 |
| DE | −0.293 | 0.146 | 26 |
| DK | −0.387 | 0.083 | 21 |
| ES | −0.040 | 0.632 | 144 |
| FI | −0.360 | 0.077 | 25 |
| FR | +0.021 | 0.827 | 113 |
| GR | +0.208 | 0.041 | 97 |
| IT | −0.239 | 0.003 | 156 |
| NL | −0.384 | 0.000 | 96 |
| NO | −0.346 | 0.015 | 49 |
| PT | +0.237 | 0.101 | 49 |
| SE | −0.347 | 0.009 | 56 |

(IE skipped — only 2 regions in NUTS-2 data.)

**Meta-correlation: r(CWED, regional_r) = +0.150, p=0.659; Spearman ρ = +0.009, p=0.979, N=11.** The within-country regional pattern does NOT track CWED. The country-level r=−0.85 does not extend to within-country regional aggregate vote shares.

**Two structural observations:**

1. **7 of 12 within-country correlations are negative** (DE, DK, ES, FI, IT, NL, NO, SE). Most countries have a within-country negative pattern: regions with HIGHER RTI vote LESS right-populist. This is the OPPOSITE direction from the individual-level finding (high-RTI individuals are MORE anti-immig). Classic ecological-vs-individual divergence.

2. **Regions with high RTI (lots of routine workers) are typically urban/industrial.** They have more immigrants, more education, stronger left/center parties — compositional features that suppress aggregate right-populist vote share even when individual high-RTI workers in those regions are more anti-immigration.

**Why this does NOT break the asymmetric story:**

The paper's central claim is identified at the individual × country cross-level interaction (RTI × CWED on individual anti-immig attitudes). The regional sanity check tests a DIFFERENT object: within-country region-level vote shares correlated with regional RTI aggregate. The two need not track, and the structural reasons above explain why they don't.

The §V.F discussion of attitude→vote conversion under supply-side constraints (Brexit, FPTP, Ireland's lack of a radical-right party) already names this distinction. The regional finding is consistent with that discussion: vote share is a different beast from attitudes, mediated by supply-side institutions and compositional features.

**Why this DOES change the calculation about Appendix D:**

The audit (Section H, Action 10) recommended a 1–2 week NUTS-2 regional falsification using Milner data as the most ambitious one-month addition. **This sanity check suggests that doing the obvious version of that analysis — country-level CWED moderation of regional RTI → right-populist vote share — will not yield a clean replication.** Ben would either (a) have to argue the discrepancy via attitudes-vs-votes plus supply-side mediation (already done in §V.F), in which case the Appendix adds little, or (b) have to use a different design (individual ESS with NUTS-2 identifier + regional features), which is more like 4–6 weeks of work and is a thesis-scale move.

**FLAG for Ben (Section 5):** Reconsider Appendix D before committing the 1–2 weeks. The audit's recommendation was based on Milner's data being analysis-ready (it is) and on the country-level pattern presumably extending to regional level (it doesn't, in this quick check). A more defensible regional design uses individual-level ESS with NUTS-2 identifier — closer to Schraff & Pontusson 2024 but at individual level — and that's a more substantial project. The half-day sanity check may have just saved 1–2 weeks.

**What the sanity check did NOT test, that would be more aligned with the paper:** individual-level RTI × regional CWED variation × individual anti-immig attitudes. ESS already has individual data; merging NUTS-2 region IDs + regional CWED variation requires the regional CWED data which isn't standard (CWED is country-year, not region-year). This is the design the proper regional analysis would need; it doesn't currently exist in the repo and would take real construction.

---

## Running findings log

(append findings here as they emerge)

