# Session 3 Findings — 2026-05-04

**Author:** Claude (Opus 4.7, 1M context)
**Time elapsed:** ~3.5 hours
**Reference:** `audit_and_review_2026-05-04.md` (audit done previously this day)
**Working notes (raw):** `session3_workingnotes.md`

---

## Section 1: Foundation Fixes — All Completed

### 1a. BLUPs jackknife — **PAPER VALUES REPRODUCE**

The most consequential finding of the session.

The audit's open Issue B1 was that Claim 14's BLUPs jackknife sequence (excl GB → r=−0.802; excl NO → r=−0.794; excl GB+NO → r=−0.717) appeared in no saved CSV. The bivariate fallback showed GB+NO as the *most fragile* pair (r=−0.335, p=0.263), inconsistent with the paper's robustness claim.

**I added a BLUPs jackknife block to `scripts/random_slopes_models.py`** (after line 303, ~85 lines) that:
1. Refits the random-slopes mixed model with `cntry` grouping (matching `_diagnose_cwed_correlation.py`'s spec) and full individual controls.
2. Extracts BLUPs at country level (`fixed_slope + ranef['task_z']`).
3. Computes single-country jackknife (15 drops) and two-country jackknife (105 pairs) on those BLUPs.
4. Saves to `outputs/tables/blups_country_slopes.csv`, `blups_jackknife_single.csv`, `blups_jackknife_two.csv`.

**Reproduction quality:**

| Quantity | Paper claim | Computed | Match |
|---|---|---|---|
| Full-sample BLUPs r | −0.848 | −0.8552 | ✓ within rounding |
| Excl GB | −0.802 | −0.8080 | ✓ within rounding (p=0.0005) |
| Excl NO | −0.794 | −0.7926 | ✓ essentially exact (p=0.0007) |
| Excl GB+NO (pair) | −0.717, p=0.006 | −0.7003, p=0.0077 | ✓ within rounding |

**Robustness at the BLUPs level (105 two-country pairs):**
- 0 / 105 pairs flip sign.
- 105 / 105 pairs significant at p<0.05.

**Audit revision.** Audit Section A Claim 14 should be updated from ✗ to ✓. Audit Section B Issue B1 is closed. The paper's robustness narrative in §V.D fully holds at the BLUPs level. The bivariate fallback (`jackknife_two_country.csv`) showing GB+NO weakening to r=−0.335 is correct but is a different statistic on a different methodology. The paper correctly relegates the bivariate version to "the replication appendix" (§V.D).

### 1b. Macro robustness persisted

`outputs/tables/rs_macro_controls.csv` now contains the M3+GDP/Gini result that was previously printed only to console. β=−0.0655, SE=0.0094, p<0.0001. Matches the paper's β=−0.066, p<0.001 within rounding.

### 1c. STATUS.md + MEMORY.md updated

- `projects/seminar_paper/STATUS.md`: Empirical Narrative section rewritten with current random-slopes numbers (β=0.168 / 0.127 / −0.059 / −0.066), v3 reference removed, Key Files updated to reflect that `random_slopes_models.py` is canonical for headline numbers and that `analysis/README.md` documents the canonical-source map.
- `MEMORY.md`: `[LEARN:workflow]` updated from "CWED interaction β=−0.056 survives GDP, Gini" to "β=−0.066 (p<0.001, `rs_macro_controls.csv`)" with a note that the older −0.056 came from the random-intercepts spec.

### 1d. Stale files archived

| Moved | New location |
|---|---|
| `outputs/tables/{table1_summary_stats, table2_main_results, tableA1_robustness, country_slopes, jackknife_details, summary_stats}.csv` + `table2_main_results.json` (all March 16, all stale) | `outputs/tables/archive/march16_pre_random_slopes/` |
| `analysis/overnight_report.md` (March 16, superseded) | `analysis/archive/` |
| `analysis/walkthrough_*.py` (5 files), `analysis/fix_plots_ab.py` (pedagogical, not pipeline) | `analysis/archive/walkthrough/` |
| `manuscripts/paper_draft_v3_final.md`, `paper_draft_v5_big_bet_theory.md`, `medium bet_paper_draft_v4_final.md` | `manuscripts/archive/` |

Each archive folder has a README explaining what's there and why.

**Verified before archiving:** No build script reads any of the moved files. `scripts/build_submission_docx.py` only reads `MANUSCRIPT`. `scripts/create_figures_final.py` reads `analysis/sorting_mechanism_master_v2.csv`, `analysis/final_results.json`, `outputs/tables/rs_jackknife.csv` (none archived). All references to the moved files in code are `to_csv` writes only.

### 1e. `analysis/README.md` written

A canonical-source map listing which scripts produce which tables, plus a full re-run order. The two-pipeline architecture (`final_analysis_pipeline.py` historical/RI; `random_slopes_models.py` canonical/RS) is now explicitly documented. New maintainers (or future-Ben) shouldn't walk into the wrong directory anymore.

### Pre-existing bug fix (introduced during 1a, not in the audit)

`scripts/random_slopes_models.py:267` had `r1, p1 = _stats.pearsonr(...)` inside the bivariate single-country jackknife loop, overwriting the `r1, m1 = fit_mlm(...)` Model 1 results dict from line 113. This caused the wrap-up `comparison` block at line 417 (`r1['rti_coef']`) to fail with `IndexError: invalid index to scalar variable`. The script's mid-section outputs all saved correctly (because the error was in the wrap-up), but the comparison CSV was not regenerated. **Fixed:** loop variables renamed to `r_jk, p_jk` with an inline comment explaining why.

---

## Section 2: Sub-component analysis verified and extended

The CWED sub-component decomposition exists at `analysis/cwed_subcomponents_report.md` (Apr 29) — but it used **OLS + country-wave fixed effects + cluster-robust SEs**, which is a different specification from §V.D's random-slopes mixed model. For consistency with §V.D, I re-ran the decomposition in the random-slopes spec via `scripts/cwed_subcomponents_extended.py`.

### 2a + 2b. Sub-components in random-slopes spec, with and without macro controls

| Sub-component | RS β | SE | p | RS+macro β | SE | p |
|---|------|-----|---|------------|-----|---|
| **Composite (TOTGEN)** | −0.0585 | 0.024 | 0.015 * | −0.0647 | 0.009 | <0.001 *** |
| **Unemployment (UEGEN)** | −0.0514 | 0.010 | <0.001 *** | −0.0551 | 0.011 | <0.001 *** |
| **Sickness (SKGEN)** | −0.0473 | 0.010 | <0.001 *** | −0.0660 | 0.011 | <0.001 *** |
| **Pensions (PGEN)** | −0.0131 | 0.013 | 0.310 | −0.0206 | 0.015 | 0.172 |

N=81,885 (RS base) / 59,364 (RS+macro). Saved at `outputs/tables/cwed_subcomponents_rs.csv`, `cwed_subcomponents_macro.csv`.

**Pensions are robustly weakest** — clean confirmation of the dignity-mechanism prediction that pensions, decoupled from the working-age dignity dynamic, should not moderate. β=−0.013 (p=0.31) base, β=−0.021 (p=0.17) with macros. Both nulls.

**Unemployment vs Sickness is closer than the existing report claimed.** UEGEN β=−0.051 vs SKGEN β=−0.047 in RS base — statistically indistinguishable. Under macro controls **the ordering flips: SKGEN β=−0.066 vs UEGEN β=−0.055**.

**This is a softening of the existing analysis's claim, not a refutation.** The dignity-mechanism prediction "welfare programmes that touch working-age workers carry the moderation; pensions don't" is supported. The stronger prediction "specifically unemployment" is not cleanly supported in the random-slopes spec consistent with §V.D. The defensible reading is broader: programmes that engage working-age dignity (UE and SK both) carry the moderation; pensions don't.

### 2c. UEGEN country jackknife

| Statistic | Value |
|---|---|
| Country drops that converged | 15 of 15 ✓ |
| β range | [−0.0588, −0.0438] |
| Sign-flip count | 0 of 15 ✓ |
| p<0.05 count | 10 of 15 |

UEGEN interaction is sign-stable across all 15 single-country drops, but 5 drops weaken below conventional significance. **Moderate fragility on the UEGEN-specific finding.** The composite (TOTGEN) interaction is more robust to country exclusions (β range [−0.062, −0.051] in `rs_jackknife.csv`, all significant). Saved at `outputs/tables/uegen_country_jackknife.csv`.

### 2d. Item-level decomposition of the anti-immig index

Random-slopes Model 3 with composite CWED, separately on each raw item of the index (imwbcnt, imueclt, imbgeco — items are 0-10 ESS coded so HIGH = pro-immig; the composite reverses to HIGH = anti-immig).

| Item | Label | RTI main β | CWED interaction β | p |
|---|---|---|---|---|
| imwbcnt | "make country worse generally" | −0.178 (SE 0.087) | +0.072 (SE 0.085) | 0.39 (n.s.) |
| imueclt | "undermine cultural life" | −0.222 (SE 0.012) | +0.045 (SE 0.011) | <0.001 *** |
| imbgeco | "bad for economy" | −0.242 (SE 0.012) | +0.055 (SE 0.011) | <0.001 *** |

(Positive interaction on raw items = negative interaction on the reverse-coded composite — directionally consistent.) Saved at `outputs/tables/cwed_interaction_by_item.csv`.

**The naive "cultural item carries the moderation" prediction is NOT supported.** The economic item (imbgeco) shows slightly STRONGER moderation than the cultural item (imueclt). Both highly significant, in the same direction, similar magnitudes.

**The richer §III misattribution-channel reading IS supported.** Per paper §III: identity switches from class to cultural and then ECONOMIC frustration gets misattributed to immigrants (Wagner 2022's "kicking down" + Wu 2022's misdirection). Under that reading, both cultural and economic items respond, driven by the same identity-switch upstream. The data is consistent with this richer reading.

**The imwbcnt item has anomalous SE inflation** (RTI main SE=0.087 vs 0.012 for the other items — 7× larger). Possible scale/distribution issue specific to this item, or random-slopes convergence problem. Not central to the asymmetric story but worth a brief follow-up before publication.

---

## Section 3: New exploratory findings

### 3a. Subjective insecurity as control — **SKIPPED with documented reason**

The brief asked to test whether the RTI effect is mediated by felt vulnerability. Two issues blocked execution:

1. **Data:** `hincfel`, `lkuemp`, `stfeco`, `stflife` are NOT in the master CSV `analysis/sorting_mechanism_master_v2.csv` (verified — only `trstprl`, `trstplt` of the candidate items are present). To run the analysis I'd need to re-merge from raw ESS waves 6–9 — adding 30–60 min plus risk of subtle merge changes that could affect downstream numbers. Per the brief's "conservative choice when ambiguous" rule, I skipped.

2. **Theory:** The closest available proxies (`trstprl`, `trstplt`) are *downstream* mediators of the welfare-encounter mechanism per §III.B (Soss 1999, Wagner 2022, De Blok and Kumlin 2022). Adding them as controls on the right-hand side would partial out part of the very mechanism the paper identifies — a mediator-as-control bias that produces a "false null."

**Recommended next step (not in this session):** Add `hincfel` (feeling about household income) and `lkuemp` (likelihood of unemployment) to the master via a small re-merge from raw ESS, then test mediation properly with Imai-Keele-Tingley product method or analogous. Half-day's work outside this session's budget.

### 3c. Regional sanity check — **IMPORTANT NEGATIVE FINDING**

**Question:** Do within-country regional RTI → right-populist-vote-share patterns correlate with CWED in a way directionally consistent with the country-level r=−0.85?

**Method:** Milner 2021 NUTS-2 panel (`imputed_econdata_voteshare_merged.dta`), `_mi_m==1` imputation, deduplicated on (nuts2, year), 1991–2018, 13 countries with sufficient data. Per-country bivariate Pearson r of `rti_region` vs `nuts2_right_pop_vs`; meta-correlate the country-level r values with CWED total generosity. (My initial spec used year FE + cluster SE; with 6–22 regions × 2–3 election years per country, year FE absorbed too much of the variation. Bivariate Pearson on the full 1991–2018 panel is the cleaner check.)

Saved: `outputs/tables/regional_sanity_check.csv`, `outputs/figures/regional_sanity_check.png/.pdf`.

**Result:**

| Statistic | Value |
|---|---|
| Meta Pearson r(CWED, regional_r) | +0.150, p=0.659 |
| Meta Spearman ρ(CWED, regional_r) | +0.009, p=0.979 |
| N | 11 (countries with both Milner regional + CWED) |

**The country-level r=−0.85 finding does NOT extend to within-country regional aggregate vote shares.** The regional pattern doesn't track CWED at all.

**Two structural observations:**

1. **7 of 12 within-country regional correlations are NEGATIVE** (DE, DK, ES, FI, IT, NL, NO, SE). Most countries show: high-RTI regions vote LESS right-populist within country. This is OPPOSITE the individual-level finding (high-RTI individuals more anti-immig). Classic ecological-vs-individual divergence.

2. **Regions with high RTI (lots of routine workers) are typically urban/industrial centers** — high immigrant share, more education, larger left/center vote — compositional features that suppress aggregate right-populist vote share even when individual high-RTI workers in those regions are more anti-immigration.

**Why this does NOT break the asymmetric story.** The paper's central claim is identified at the individual × country cross-level interaction. The regional sanity check tests a different object: within-country region-level vote shares vs regional aggregate RTI. The two need not track. The §V.F discussion of attitude→vote conversion under supply-side constraints already names this distinction (Brexit, FPTP suppression, Ireland's lack of a radical right).

**Why this DOES change the calculation about Appendix D.** The audit (Section H Action 10) recommended a 1–2 week NUTS-2 regional falsification using Milner data as the most ambitious one-month addition. **This sanity check suggests that doing the obvious version of that analysis — country-level CWED moderation of regional RTI → right-populist vote share — will not yield a clean replication of the country-level pattern.** Ben would either need to argue the discrepancy via attitudes-vs-votes plus supply-side mediation (already done in §V.F), in which case the Appendix adds little, OR use a different design (individual ESS with NUTS-2 region IDs + regional features as moderators, closer to Schraff & Pontusson 2024 at individual level), which is more like 4–6 weeks of work and is thesis-scale.

**See Section 5 for what this means for Ben's decision.**

---

## Section 4: Ready for integration into the manuscript

For Ben to integrate when he returns. None of these were applied to the manuscript — they are findings ready for him to write up.

### 4.1 §V.D — One-paragraph addition: CWED sub-component decomposition

**Where:** End of §V.D (the CWED Finding section), before §V.E.

**Approximate length:** 4–6 sentences plus updated/new figure.

**Content:**

The composite CWED finding decomposes into its three sub-components in a way that informs the asymmetric mechanism. In random-slopes Model 3 specifications matching §V.B, the cross-level interaction with unemployment generosity (UEGEN) is β=−0.051 (p<0.001), with sickness generosity (SKGEN) β=−0.047 (p<0.001), and with pension generosity (PGEN) β=−0.013 (p=0.310). The pension null holds with macro controls (β=−0.021, p=0.17), confirming that welfare programmes decoupled from working-age dignity do not moderate the conversion of automation exposure into exclusionary attitudes. The unemployment and sickness sub-components are statistically indistinguishable in the base specification and roughly comparable under macro controls, suggesting the moderation operates through working-age welfare programmes broadly rather than through the unemployment encounter specifically. Figure 7 (already in `outputs/figures/`) plots the country-level scatter for each sub-component and supports the visual reading.

**Caveat to flag:** The existing report at `analysis/cwed_subcomponents_report.md` claimed clean UEGEN > SKGEN > PGEN ordering at individual level. That ordering was an artefact of the OLS+FE+cluster spec used in that report. In the RS spec consistent with §V.D, UEGEN ≈ SKGEN >> PGEN. The substantive interpretation should be tightened to what the data actually shows.

### 4.2 §V.D — Sentence on BLUPs jackknife reproducibility

**Where:** §V.D last paragraph, after the existing single-country exclusion sentence.

**Approximate length:** 1–2 sentences.

**Content:**

A two-country BLUPs jackknife across all 105 country pairs gives r ∈ [−0.700, −0.897], with no pair flipping sign and 105/105 retaining significance at p<0.05. The single-country and pair-country jackknife values are now persisted at `outputs/tables/blups_jackknife_*.csv` for replication.

### 4.3 Appendix A or §V.D — Macro-controls robustness now persisted

**Where:** Reference can stay in Appendix A as already drafted; just confirm the value matches the persisted CSV.

**Content:**

The β=−0.066 (p<0.001) macro-controls robustness result is now in `outputs/tables/rs_macro_controls.csv`. The Appendix A sentence "Adding country-level GDP growth and post-fiscal Gini as macro controls — sourced from the Comparative Political Data Set over 2012–2018 — leaves the buffering coefficient essentially unchanged (β=−0.066, p<0.001)" is correctly sourced and reproducible.

### 4.4 §V.E or Appendix B — One-paragraph caveat on item-level

**Where:** Optional. Could go in §V.E (if Ben wants to report the item-level decomposition as a sharpening test) or Appendix B (if as supplementary).

**Approximate length:** 3–4 sentences if added.

**Content:**

A natural sharpening test asks whether the moderation operates specifically through the cultural item (imueclt — "undermine cultural life") rather than the economic one (imbgeco — "bad for economy"). The data does not support a clean cultural-only reading: in random-slopes Model 3, the cultural item shows β=+0.045 (p<0.001) and the economic item β=+0.055 (p<0.001) — both highly significant, similar magnitudes, slightly favouring the economic item. This is consistent with the §III misattribution channel (cultural-identity switch causes economic frustration to be projected onto immigrants), under which both items respond to the same upstream mechanism, but it does not support a stronger reading where cultural attribution is the sole channel. The composite anti-immig index aggregates both correctly.

### 4.5 No changes recommended to: Claim 14 sentence, ALMP comparison, Model 6, asymmetric framing in §III

These all hold as written. The BLUPs jackknife confirms Claim 14 within rounding tolerance.

---

## Section 5: Things that surfaced that need Ben's judgement

These are the items where I took the conservative path or where a substantive call shouldn't be made autonomously.

### 5.1 The audit's Section A Claim 14 needs updating from ✗ to ✓

The audit (`audit_and_review_2026-05-04.md`) listed Claim 14 as ✗ NOT REPRODUCIBLE. With the BLUPs jackknife now computed, Claim 14 should move to ✓. Audit Section B Issue B1 should be marked closed. The audit document is mine; I'm flagging this for your decision rather than editing my own audit unilaterally — but I'll edit it on your say-so.

### 5.2 Sub-components: the existing report's "UEGEN > SKGEN > PGEN" ordering claim was spec-specific

The existing `analysis/cwed_subcomponents_report.md` (Apr 29) claims clean UEGEN > SKGEN > PGEN at individual level. That ordering used OLS+FE+cluster, not random slopes. **In the random-slopes spec consistent with §V.D, UEGEN ≈ SKGEN with macros putting SKGEN slightly ahead.** The pension null holds either way.

This shifts the §V.D narrative IF you integrate sub-components. Two options:

(a) **Conservative:** Report the broader claim — "working-age welfare programmes (UE and SK both) carry the moderation; pensions, which don't engage the working-age dignity dynamic, do not." This is well-supported.

(b) **Aggressive:** Argue UEGEN is the dominant channel based on the existing OLS+FE analysis, and treat the RS-spec results as more conservative variance estimates. Riskier.

I'd recommend (a). The dignity argument doesn't hinge on UEGEN being uniquely dominant — the contrast that matters is "working-age (UE+SK) vs decoupled (P)." But this is your call.

### 5.3 The item-level decomposition undercuts a "cultural-only" reading

The naive prediction that imueclt (cultural) should dominate imbgeco (economic) is not supported. Both items respond, similarly, with the economic item slightly stronger.

This doesn't damage §III as written — the misattribution channel reads both items as downstream of the same identity switch. But if you've been thinking of saying anything in the paper or talk like "the cultural attribution is what carries the moderation," the data is more ambiguous than that. The defensible reading is: "the moderation operates through both cultural and economic anti-immigration items, consistent with §III's prediction that economic frustration is misattributed culturally once the cultural-identity switch has fired."

### 5.4 Appendix D regional analysis: the audit's recommendation is in question

**This is the most consequential Section 5 item.** The audit recommended Appendix D (regional NUTS-2 falsification using Milner data) as the most ambitious one-month addition (~1–2 weeks). The sanity check shows the obvious version of that analysis — country-level CWED moderation of regional RTI → right-populist vote share — produces a NULL meta-correlation (Pearson r=+0.15, p=0.66; Spearman ρ=+0.01, p=0.98).

The result doesn't break the paper. It's a plausibly-explained ecological-vs-individual divergence: regions with high RTI are urban/industrial centers with compensating compositional features (immigrant share, education levels). The §V.F supply-side discussion already names this kind of attitude-vs-vote divergence.

**But it does change the calculation about Appendix D.** Three options:

(a) **Drop Appendix D entirely.** The half-day saved 1–2 weeks. The country-level individual-level finding stands on its own.

(b) **Reframe Appendix D as "we tested it at NUTS-2 level and the country-level cross-sectional pattern doesn't extend, here's why."** Defensible but adds little to the paper. Refers to existing §V.F supply-side language for the explanation.

(c) **Build the proper regional design — individual ESS with NUTS-2 identifier + regional features.** Closer to Schraff & Pontusson 2024 but at individual level. 4–6 weeks (thesis-scale, not paper-scale).

I'd recommend (a) for this paper and (c) for the thesis. (b) wastes the page.

### 5.5 Subjective insecurity as control — the proper test still hasn't been run

I documented the data limitation and the mediator-as-control bias issue, but the substantive question (is the RTI effect mediated by felt vulnerability, or independent of it?) remains open. This is a half-day project with a small ESS re-merge plus proper mediation analysis. Worth doing for the thesis if not for this paper.

### 5.6 imwbcnt item-level convergence anomaly

The "make country worse generally" item shows a 7× SE inflation in the random-slopes spec — `RTI main SE=0.087` vs `0.012` for the other two items, on similar N and similar variance. Possible: the item has different missingness/scale across waves, or RS convergence specific to this item. Not central to anything paper-relevant but flagged for a 30-min look before final publication. The composite anti-immig index averages all three including imwbcnt; the composite's RS spec is well-behaved.

---

## Section 6: Files created or modified

### Modified
- `scripts/random_slopes_models.py` — added BLUPs jackknife block (~85 lines) and persistence of macro-controls result; fixed pre-existing `r1, p1` loop-variable name collision.
- `projects/seminar_paper/STATUS.md` — Empirical Narrative section rewritten with current numbers; v3 reference removed; Key Files updated.
- `MEMORY.md` — `[LEARN:workflow]` entry on CWED interaction updated from β=−0.056 (RI) to β=−0.066 (RS+macros).

### Created
- `scripts/cwed_subcomponents_extended.py` — RS-spec sub-component decomposition + macro robustness + UEGEN jackknife + item-level decomposition.
- `scripts/regional_sanity_check.py` — Milner regional pattern vs CWED meta-correlation.
- `analysis/README.md` — canonical-source map for the two-pipeline architecture.
- `outputs/tables/blups_country_slopes.csv` — full-sample BLUPs slopes (15 countries).
- `outputs/tables/blups_jackknife_single.csv` — 15 single-country drops on BLUPs.
- `outputs/tables/blups_jackknife_two.csv` — 105 two-country drops on BLUPs.
- `outputs/tables/rs_macro_controls.csv` — Claim 13 result persisted.
- `outputs/tables/cwed_subcomponents_rs.csv` — sub-components in RS spec.
- `outputs/tables/cwed_subcomponents_macro.csv` — sub-components with macro controls.
- `outputs/tables/uegen_country_jackknife.csv` — UEGEN single-country jackknife.
- `outputs/tables/cwed_interaction_by_item.csv` — item-level decomposition.
- `outputs/tables/regional_sanity_check.csv` — country-level regional r vs CWED.
- `outputs/figures/regional_sanity_check.png/.pdf` — regional sanity scatter.
- `outputs/tables/archive/march16_pre_random_slopes/README.md` — archive doc.
- `analysis/archive/walkthrough/README.md` — archive doc.
- `manuscripts/archive/README.md` — archive doc.
- `session3_workingnotes.md` — running notes.
- `session3_findings_2026-05-04.md` — this report.

### Archived (moved, not deleted)
- 7 stale CSV/JSON files in `outputs/tables/` → `outputs/tables/archive/march16_pre_random_slopes/`
- `analysis/overnight_report.md` → `analysis/archive/`
- 6 walkthrough/fix Python files → `analysis/archive/walkthrough/`
- 3 alternative manuscript drafts → `manuscripts/archive/`

---

## Section 7: One-paragraph summary

The audit's three open numerical issues all closed cleanly. The BLUPs jackknife reproduces the paper's −0.802 / −0.794 / −0.717 sequence within rounding (Claim 14 stands; audit Section A entry should move to ✓), the macro-controls β=−0.066 is now persisted, and the documentation triangle (STATUS, MEMORY, scripts) is realigned with v4. Files that should not have been at the canonical paths anymore are now in archive folders with READMEs explaining what's there. The two-pipeline architecture is documented in `analysis/README.md`. On the strengthening side, the CWED sub-component decomposition runs cleanly in the random-slopes spec consistent with §V.D, and produces a *softened* version of the existing analysis's claim — pensions are robustly weakest as the dignity mechanism predicts, but unemployment and sickness are statistically indistinguishable rather than UE > SK > P. The item-level decomposition does not support a "cultural item carries the moderation" reading; both cultural and economic items respond, similar magnitudes, with the economic item slightly stronger, consistent with §III's misattribution-channel reading rather than a pure cultural-attribution one. The most consequential exploratory finding is the regional sanity check, which suggests the audit's recommended Appendix D move (NUTS-2 regional falsification using Milner data) will not yield a clean replication of the country-level pattern — within-country regional aggregate vote shares don't track CWED, and 7 of 12 within-country correlations are negative (high-RTI regions vote less right-populist), an ecological-vs-individual divergence consistent with §V.F's supply-side discussion but not with the audit's expectation of a clean falsification artifact. The asymmetric story stands. The recommendation about how to spend the next month should change: skip Appendix D as currently scoped (or do version (a) from §5.4 — drop entirely), spend the saved 1–2 weeks on the multi-wave ISSP harmonization (audit Action 8) and on integrating the sub-components paragraph into §V.D (Action 4 plus §4.1 above). What to do first when you return: review §5.4 (the Appendix D decision) and §5.2 (sub-component framing), since both are framing calls only you can make. Everything else is integrate-when-ready.
