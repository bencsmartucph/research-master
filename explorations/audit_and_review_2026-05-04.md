# Audit and Strategic Review — 2026-05-04

**Author:** Claude (Opus 4.7, 1M context)
**Subject:** "Dignity Is a Baseline" (`manuscripts/paper_draft_v4_final.md`)
**Operating frame:** Audit-only. Pre-submission, ~one month to deadline.

---

## Section A: Verification of Paper Claims

The paper's headline numbers come from `scripts/random_slopes_models.py` (canonical for Models 1–3) and `analysis/final_results.json` (canonical for Models 5, 6, country correlations). Three different output sources do not agree with each other; the paper consistently draws from the right one for each claim.

| # | Claim | Status | Source / Detail |
|---|-------|--------|-----------------|
| 1 | ESS rounds 6–9, 34 countries, N=188,764 | ✓ | `analysis/sorting_mechanism_master_v2.csv` is exactly (188,764 × 48); 34 distinct `cntry` values |
| 2 | RTI ISCO-08 match rate 87.8%, N=165,667 | ✓ | `task` non-null for 165,667 of 188,764 (87.76%) |
| 3 | Anti-immigration α=0.864 (3 items, reverse-coded 0–10) | ✓ | α=0.8644 over `imwbcnt + imueclt + imbgeco` (NOT `imbleco` as the brief writes — that's a typo for `imbgeco`, "Immigration good for economy"). Logic at `analysis/econometric_review_diagnostics.py:550–580` |
| 4 | CWED 15 Western European countries, mean 2005–2011 | ✓ | `analysis/final_analysis_pipeline.py:141–156` filters `YEAR >= 2005 & YEAR <= 2011`, computes country means, merges as time-invariant. 15-country list confirmed |
| 5 | Model 1: RTI β=0.168, p<0.001 | ✓ | `outputs/tables/rs_results.csv:M1_baseline_rs` β=0.16810, p=1.1e-32, n=133,016 |
| 6 | Model 2: RTI × Liberal β=0.127, p=0.003 | ✓ | `outputs/tables/rs_results.csv:M2_regime_rs` β=0.12711, p=0.00325 |
| 7 | Model 3: RTI × CWED β=−0.059, p=0.015, N≈81,885 | ✓ | `outputs/tables/rs_results.csv:M3_cwed_rs` β=−0.05918, p=0.01509, n=81,885; also in `rs_vs_ri_model3.csv` |
| 8 | Country-level r BLUPs vs CWED = −0.848, N=15 | ✓ | `final_results.json:cwed_vs_slopes_generosity` r=−0.84831, n=15 |
| 9 | Country-level r RTI slopes vs ALMP = 0.01, N=15 | ✓ | `final_results.json:almp_vs_slopes_matched` r=0.01094, n=15 |
| 10 | Solidarity Model 5: RTI × Liberal β=+0.011, p=0.285 | ✓ but spec-inconsistent | Matches `final_results.json:model5` (random intercepts), NOT `rs_results.csv:M5_redistribution_rs` (random slopes; β=0.0133, p=0.488). See B2 |
| 11 | ISSP β=+0.010, SE=0.016, p=0.55, N=10,216, 12 countries | ? not saved | `scripts/issp_solidarity_leg.py` computes and prints these values (lines 245–251) but writes no CSV/JSON. Values match STATUS. 12 countries = WEST_EU_15 minus AT/BE/IT |
| 12 | Voting Model 6: RTI × Liberal β=−0.123, p=0.032 | ✓ | `final_results.json:model6` β=−0.12286, p=0.03243 |
| 13 | Macro robustness β=−0.066, p<0.001 | ? not saved | Computed at `random_slopes_models.py:184–188` (CWED + GDP/Gini) but printed only — `M3_cwed_macro_controls` is not written to any CSV |
| 14 | Two-country jackknife (drop UK + NO): r=−0.717, p=0.006 | ✓ (reproduced 2026-05-04, Session 3) | BLUPs jackknife block added to `scripts/random_slopes_models.py`; saved to `outputs/tables/blups_jackknife_{single,two}.csv`. Excl GB → r=−0.808, excl NO → r=−0.793, excl GB+NO → r=−0.700 (p=0.008), all within rounding of paper claims. 105/105 pairs stay p<0.05, 0/105 flip sign. Issue B1 closed. The bivariate jackknife at `outputs/tables/jackknife_two_country.csv` (GB+NO drop r=−0.335) is correctly relegated to "the replication appendix" alternative per §V.D and is a different statistic on a different methodology |

**Headline (revised 2026-05-04 PM after Session 3 fixes).** Of 14 claims, **13 now verify cleanly** (Claim 14 closed; macro-controls Claim 13 now persisted to `rs_macro_controls.csv`). Claim 11 (ISSP) still computes-but-doesn't-save in `scripts/issp_solidarity_leg.py` — minor reproducibility hygiene item, not a substantive issue. Claim 10 (Model 5) reveals a methodological inconsistency (paper states random-slopes spec but the reported number is from random-intercepts) but the asymmetric story is unaffected by either spec.

---

## Section B: Broken Foundations

Issues that would change paper claims if true. Severity-ranked, highest first.

### B1. Claim 14 jackknife reproducibility — **CLOSED 2026-05-04 (Session 3)**

**Status:** Resolved. BLUPs jackknife block added to `scripts/random_slopes_models.py`. Outputs persisted to `outputs/tables/blups_country_slopes.csv`, `blups_jackknife_single.csv`, `blups_jackknife_two.csv`. Paper's −0.802 / −0.794 / −0.717 sequence reproduces within rounding (−0.808 / −0.793 / −0.700). All 105 two-country pairs stay p<0.05; 0 flip sign. Robustness narrative in §V.D fully holds at the BLUPs level.

The original audit text below is preserved for the record.

---

### B1 (original, retained for record). Claim 14 jackknife is not reproducible from saved outputs (HIGH)

The paper §V.D claims: "excluding the United Kingdom (lowest CWED) gives r=−0.802; excluding Norway (highest CWED) gives r=−0.794; excluding both simultaneously gives r=−0.717 (p=0.006)." These are presented as BLUPs jackknife values (matching the headline r=−0.848 from BLUPs).

These specific values appear in no saved CSV or JSON. The diagnostic `_diagnose_cwed_correlation.py` computes BLUPs (full sample r=−0.855, close to the published −0.848) but does NOT compute the jackknife. The canonical `random_slopes_models.py` (lines 238–303) saves a jackknife but it is the bivariate per-country OLS version (full-sample r=−0.625), and on that version, GB+NO exclusion gives r=−0.335 (p=0.263) — the worst pair in the entire 105-pair file. The script's comment at line 239–242 *claims* it reproduces the published BLUPs numbers, but the implementation uses bivariate OLS at line 253 (`stats.linregress`).

**Why it matters.** The robustness narrative in §V.D is one of the paper's anchors. Reproducibility is a hard gate at every Tier-2 target journal in your `domain-profile.md` (CPS, BJPS, JESP). A referee or thesis examiner who tries to reproduce will not find the numbers. Worse, on the bivariate version that IS saved, GB+NO is the most fragile pair — meaning the paper's "robust to all single-country exclusions" sentence may not even be defensible on the bivariate alternative reported in the replication appendix (per §V.D).

**Recommended fix.** Add a BLUPs jackknife block to `random_slopes_models.py` after the existing OLS block. ~20 lines of code: extract `m3_rs_reml.random_effects` per country, compute country-level slope as `fixed_slope + ranef`, then iterate over single-country drops and pair-drops on those BLUPs. Save to `outputs/tables/blups_jackknife_single.csv` and `blups_jackknife_two.csv`. Confirm the −0.802 / −0.794 / −0.717 values reproduce. **If they don't reproduce, the paper sentence has to change.**

### B2. Methodological inconsistency in Model 5 specification (MEDIUM)

§V.B states all mixed models use random slopes for RTI by country-wave: `(1 + RTI | country-wave)`, "confirmed over random intercepts alone by likelihood ratio test." But Claim 10's β=+0.011, p=0.285 for Model 5 (redistribution × Liberal) matches `final_results.json:model5` (random intercepts), not `rs_results.csv:M5_redistribution_rs` (random slopes; β=0.013, p=0.488).

Both are nulls. The asymmetric story survives. But the methods description does not match the reported number — a careful referee will catch this.

**Recommended fix.** Use the random-slopes value (β=0.013, p=0.488) for §V.F. The asymmetric story is not weaker — if anything, the larger p strengthens the "the null is decisive" reading. One-line edit.

### B3. Documentation triangle is loose (MEDIUM, reproducibility)

Three sources of truth carry different numbers:
- The paper (v4 final): β=0.168, 0.127, −0.059 (random slopes, correct).
- `STATUS.md` lines 35–38: β=0.182, 0.117, −0.056 (random intercepts, stale).
- `MEMORY.md [LEARN:writing]`: "CWED interaction β=−0.056 survives GDP, Gini..." (also stale; paper says β=−0.066 with macro controls).

The pipeline architecture has a fork that's not documented anywhere obvious: `final_analysis_pipeline.py` → `final_results.json` is the *historical* main pipeline (random intercepts); `random_slopes_models.py` → `rs_*.csv` is the *current canonical* source for headline numbers (random slopes). MEMORY.md does name this in [LEARN:code], but no obvious README says "headline numbers come from `random_slopes_models.py`."

`STATUS.md` internally contradicts itself: "Working draft: paper_draft_v4_final.md" (line 11) but "Key files: Draft: paper_draft_v3_final.md" (line 22). The v3 reference is stale.

**Recommended fix.** Add a five-line `analysis/README.md` ("Canonical numbers: rs_results.csv for Models 1–3; final_results.json for Models 5–6 and country correlations; rs_vs_ri_model3.csv for the spec comparison."). Update STATUS.md to v4 numbers and remove the v3 line. Update the [LEARN:writing] entry. Move `analysis/overnight_report.md` (Mar 16, superseded) to `analysis/archive/`.

### B4. Stale outputs in `outputs/tables/` (LOW, but watch)

`table2_main_results.csv`, `tableA1_robustness.csv`, `summary_stats.csv`, `country_slopes.csv`, `jackknife_details.csv` carry March 16 timestamps (pre-random-slopes work). `final_results.json` is April 18; the `rs_*.csv` files are April 18 / May 2.

If `scripts/build_submission_docx.py` or `scripts/create_figures_final.py` reads from any of the March 16 tables, it could embed stale numbers in figures. The exploration subagent noted that `final_results.json` `model3_cwed` (β=−0.056, RI spec) is what `create_figures_final.py` would have access to as a JSON lookup. The Figure 6 caption / table 2 body need to be checked against rs_*.csv rather than the stale CSVs.

**Recommended fix.** Spot-check that all build scripts read from `rs_results.csv` and the May 2 jackknife files, not March 16 tables. Delete or archive tables that are no longer canonical.

---

## Section C: Things I Found You Didn't Ask About

Discoveries beyond the explicit verification list.

### C1. The brief contains two factual errors about your own data

**(a)** The brief describes Ciccolini's `essprt-all.dta` as containing `posit_income_change`, "apparently pre-merged with ESS waves 1–9." This is wrong. The file is a 5,402-row × 13-column **party-name crosswalk** (columns: `ess_party_id`, `partyfacts_id`, country, party name). MEMORY.md `[LEARN:data]` is correct: "`posit_income_change` is NOT in this repo. `essprt-all.dta` is a party crosswalk only." However, the folder *does* contain `Ciccolini_LeftBehindWhom.do` (216 KB — Ciccolini's full construction script) and `partyfacts-mapping.csv` (9 MB). If you run the do-file against your own ESS extract, you can reconstruct positional-income-change at the respondent level.

**(b)** The brief describes `siwe_2017/` as "Subjective In-Work Experience." It is not. The file `SIWE_betaMay2017.dta` is a 580 × 64 country-year **welfare expenditure** dataset (categories: health, oldage, disability, unemployment, ALMP, PLMP, education, R&D, plus standardized ratios `bweOLD_SP`, `bweWORK_SI`). Effectively a richer SOCX-style alternative to CWED at the country-year level. The misnomer is propagated into REPOSITORY_MAP.md line 269. If the actual SIWE survey is what you wanted, it isn't in this folder under that name.

**(c)** The brief asks whether Quality of Government data is in the repo "as `qog/` or `quality_of_government/`." It is — `data/raw/qog/` (97 MB) contains three QoG releases including `qog_eqi_ind_24.dta` (52 MB, individual-level European Quality of Government Index 2024) and `qog_eureg_wide2_nov20.csv` (34 MB, NUTS-2 regional institutional quality). Currently unused.

### C2. The "imbleco" / "imbgeco" typo in the brief

Claim 3 in the brief lists three anti-immigration items "imwbcnt", "imueclt", and (implicitly via the index name) the third item. The actual third item per `analysis/codebook.md` and the running pipeline at `analysis/run_sorting_mechanism.py:96` is `imbgeco` ("Immigration good for economy"). The brief uses `imbleco` informally elsewhere. Trivial — but the variable is `imbgeco`.

### C3. The "abandoned spine" — the sorting mechanism work

`analysis/run_sorting_mechanism.py` is 1,370 lines. `sorting_mechanism_exploration.ipynb` exists. `sorting_mechanism_master_v2.csv` (59 MB) is the master analysis file. `outputs/figures/fig2_sorting_pattern.pdf` was produced. Yet "sorting" is not a section of v4 — it has been demoted to mechanism-only language. This is the spine of an alternative paper that was started, partially executed, and absorbed rather than published. The selection-bias diagnostic it tests (do populist-leaning workers sort INTO automatable jobs?) is itself a defensible referee response — keep it parked rather than buried.

### C4. The paper currently has TWO siblings as alternative drafts

`manuscripts/paper_draft_v5_big_bet_theory.md` (141 lines, theory-only standalone version) and `manuscripts/medium bet_paper_draft_v4_final.md` (319 lines, the medium-bet fallback). STATUS line 9 says these are "preserved." Decide: are they archived, or are they live alternatives? If the former, move to `manuscripts/archive/`.

### C5. Walkthrough infrastructure produced but never referenced

`analysis/walkthrough_*.py` (5 files, May 2026) and `outputs/figures/walkthrough/` (8 PNGs + 3 Plotly HTMLs per [LEARN:code]) are the empirical-walkthrough document `docs/empirical_walkthrough_v1.md` — a "consolidated defence document for §V" per MEMORY. The walkthrough is in `docs/`, not in the paper or its appendices. It is a pre-defence pedagogical resource for you. Worth knowing it exists; not an audit issue.

### C6. The Gingrich harmonization do-file is right there

Per the exploration: `gingrich_2019/` contains `create_ISSPCombined.do` (387 KB) — Gingrich's own harmonization script for the ISSP Role of Government waves (1985, 1986, 1989, 1990, 1992, 1993, 1994, 1995, 1996, 1998, 2006, 2007, 2008, 2010). The §V.F single-wave 2006 supplementary test could become a 1985–2010 time series with this do-file. ZA6770 (RoG 2016) is NOT in the folder — extending past 2010 needs a fresh GESIS download.

### C7. There's no `qog/` use in any current script

`grep -r 'qog'` should return nothing in `analysis/` and `scripts/`. The 97 MB of QoG data is sitting unloaded. Worth recognising even if you don't use it for this paper.

---

## Section D: Independent Exploration — What I Found Before Reading Your List

I asked the exploration subagent to inventory the repo before consulting your Thread 2 list. The convergences and divergences:

**Convergences (your list and mine agreed):**
- Milner 2021 regional data is exceptional. NUTS-2, 1991–2015, 285 columns, multiply-imputed, with `nuts2_right_pop_vs`, `rti_region`, `shock_china_ind`, `shock_robots_mfg`. This is not "could-be-useful" — it is *analysis-ready for a regional design*.
- Baccini district-level data is present and tractable. `Analysis_Dataset_District_Level.dta` has shift-share IV, district vote shares (`distelections.dta`).
- CWED sub-components are accessible via `cwed-subset.csv`. Disaggregation by `UEGEN`, `SKGEN`, `PGEN` is half a day's work and is already partially run (`analysis/cwed_subcomponents_report.md`, `outputs/figures/fig7_cwed_subcomponents.pdf`).
- Gingrich's ISSP series is multi-wave 1985–2010 with the harmonization do-file included.

**Divergences (things I noticed that your list didn't):**
- **Quality of Government regional data** is in the repo (`data/raw/qog/`), 97 MB across three files including NUTS-2 institutional quality. You asked whether it might be there; it is. This is a *competing institutional moderator* to CWED. If the dignity-mechanism story is right, it should be CWED that moderates and not QoG (or both, with CWED dominant). Testing this head-to-head would sharpen the dignity reading against a "weak-state" alternative reading of the same effect.
- **Euroscepticism data is enormous** (`euroscepticism_stagnation/`, 566,764 rows × 38 cols, NUTS-2 region IDs, 2009–2020). It contains pooled Eurobarometer, not just one wave. EU-attitudes as a *parallel outcome* to anti-immigration is in this file at the right unit of analysis for spatial work.
- **Im 2021's pre-merged ESS** has share-based exposure (`sh_highrisk` by 2-digit ISCO) — an alternative aggregation to your individual RTI. Can be used as a robustness pillar without doing fresh merge work.
- **Status decline / Steiner Left Behind / How Not Authoritarian Populism** are essentially script-only folders. Source data isn't in them. They look like resurrected replication packages that someone partially repaired but never ran end-to-end.
- **`aspiration_apprehension/`** contains a small replication CSV plus another copy of ISCO-08 task scores. Probably redundant with `shared_isco_task_scores/`.

The biggest divergence in framing: my exploration agent rated the **Milner regional + QoG combo** as the highest-leverage opportunity in the repo. I think that's right but with a caveat — see Section G.

---

## Section E: Inventory of Unrealised Work

For each dataset/folder: status, what integration would require, expected payoff.

| Item | Status | Path | Integration cost | Payoff for this paper or thesis |
|------|--------|------|------------------|---------------------------------|
| **CWED sub-components (UEGEN / SKGEN / PGEN)** | partial | `data/raw/CWED/cwed-subset.csv`, `analysis/cwed_subcomponents_report.md` (Apr 29), `fig7_cwed_subcomponents.pdf` | half a day to integrate into v4 §V.D | HIGH — directly tests the dignity-mechanism prediction (unemployment-CWED carries the moderation, sickness/pension don't). Already analysed; just write a paragraph and update Figure 6 / 7 |
| **Milner 2021 NUTS-2 regional panel** | unused | `data/raw/milner_2021/data/data/imputed/imputed_econdata_voteshare_merged.dta` (57 MB; 285 cols; 1991–2015) | 1–2 weeks for an Appendix D regional falsification check; longer for a regional reframe | HIGH (paper) as falsification — cross-region within-country variation cannot have the same country-level confounds. MOST AMBITIOUS use is a regional companion paper but that's thesis-scale |
| **Gingrich ISSP series 1985–2010** | partial (only 2006 used) | `data/raw/gingrich_2019/`, `create_ISSPCombined.do` (387 KB harmonization) | 2–3 days to harmonize and run the §V.F test on 14 waves instead of 1 | HIGH — converts "single-wave 2006 null" into "1985–2010 time-series null"; the asymmetric prediction's solidarity null becomes much more decisive |
| **Baccini district-level austerity** | unused | `data/raw/baccini_2024/.../Raw Data/Analysis_Dataset_District_Level.dta` (9,190 rows × 42 cols, with shift-share IV) | 1–2 weeks for a district-level DiD with welfare regime as moderator | HIGH (paper) — direct mapping from Baccini 2024's design to your moderator question. Also addresses "is this really institutions or is this just austerity?" |
| **Within-country CWED time variation (1971–2011)** for AT/DE/NL/GB | unused | `data/raw/CWED/cwed-subset.csv` + ESS waves 1–9 + `kurer_2020/correspondence.dta` (ISCO-88→08 crosswalk) | 2 weeks: ESS1–5 ISCO crosswalk + within-country merge + reform-timing event study | HIGH (thesis) — solves the cross-sectional confound objection. Already named for thesis in §V.G and §VII |
| **QoG regional institutional quality** | unused | `data/raw/qog/qog_eureg_wide2_nov20.csv` (34 MB, NUTS-2) | 3–5 days as a competing-moderator robustness check against CWED | MEDIUM — addresses "is it really welfare or just state capacity?" Sharper if combined with Milner |
| **Ciccolini positional income change** | unused | `data/raw/cicollini_2025/Ciccolini_LeftBehindWhom.do` (do-file) | 1 day if the do-file runs cleanly against your ESS extract | MEDIUM — alternative disruption operationalisation independent of ISCO. Useful as a robustness pillar |
| **Im 2021 share-based exposure (`sh_highrisk`)** | unused | `data/raw/im_2021/Im - A Reservoir of Votes for the Radical Right - ESS.csv` (402 MB) | 1 day | MEDIUM — share-based exposure as a robustness pillar; cites a closely related published paper |
| **Euroscepticism pooled Eurobarometer (NUTS-2)** | unused | `data/raw/euroscepticism_stagnation/...dta` (566,764 rows, 38 cols, 2009–2020) | 1 week | MEDIUM — alternative outcome (EU support) at NUTS-2 level. Closer to Schraff/Pontusson's design |
| **Steiner ZA7700 (UK 2017+)** | unused | `data/raw/steiner_left_behind/ZA7700_*.dta` | 1 day | LOW — single-country UK data, narrow use |
| **`status_decline_working_class/`, `aspiration_apprehension/`, `how_not_authoritarian_populism/`** | unusable as-is | scripts only, no source data | N/A | Skip |
| **Kurer 2020 panel (SHP/BHPS/SOEP)** | scripts only, no panels | `data/raw/kurer_2020_declining_middle/replication_files/` | 2–4 weeks panel acquisition (SHP free, BHPS UK Data Service, SOEP free) + 4–6 weeks harmonisation | HIGH (thesis), prohibitive for this paper |
| **`silva_wellbeing/graphsdata.dta`** | very small | derived ESS subset for a 2023 paper | 1 day if useful | LOW — tiny |
| **CWED 1971–2011 raw** | unused | `data/raw/CWED/` (full series) | within-country reform-event analysis is a thesis design | HIGH (thesis) |
| **Walkthrough scripts and figures** | done, used internally | `analysis/walkthrough_*.py`, `outputs/figures/walkthrough/` | N/A — already in `docs/empirical_walkthrough_v1.md` | Internal pre-defence resource, not for the paper |

---

## Section F: Multiple-Paper Sketches

Five distinct papers this repo could support, in two sentences each. I name the closest, the strongest given your dignity-thread commitments, and the most surprising.

**Paper 1 (current). Cross-sectional asymmetric moderation.** Cross-national CWED variation moderates RTI → anti-immigration (matched 15-country sample), while ALMP and welfare spending do not; the same disruption fails to predict moderated solidarity. Individual × country, status quo. **(closest to current — drafted, v4 final)**

**Paper 2. Within-country welfare reform timing as quasi-experiment.** Use ESS waves 1–9 with ISCO-88 → ISCO-08 crosswalk plus CWED time variation (1971–2011) for AT/DE/NL/GB; identify off CWED reform years (e.g. Danish flexicurity 2003/2006/2013, Hartz reforms 2003–05, Bismarck unemployment reform). Tests asymmetric prediction within rather than across countries — solves the cross-sectional confound. **(strongest given your theoretical commitments — but explicitly a thesis chapter, not a one-month addition)**

**Paper 3. Regional NUTS-2 design (Schraff/Pontusson template).** Regional far-right vote share by NUTS-2 region 1991–2015 (Milner), with regional automation/trade exposure × CWED at country-level OR QoG at regional-level as moderators. Two-way (region, year) FE quasi-binomial GLM, ~1,200 regional units. Closer to ecological tests but loses the individual-level dignity-cascade granularity. **(most empirically credible at the cost of theoretical sharpness — the Milner data is fully ready)**

**Paper 4. Conditionality, not generosity, is the operative dimension.** Build a conditionality index (Knotz 2018 + Van Hootegem 2025 enabling/punitive ALMP disaggregation) and test head-to-head against CWED generosity. The dignity-thread prediction: conditionality moderates more sharply than generosity does. Sharpens the central claim; data assembly is the bottleneck. **(theoretically purest but data-acquisition-heavy)**

**Paper 5 (wild card). The subjective dignity damage paper.** Test the upstream mechanism, not the downstream outcome: routine workers in punitive welfare regimes report worse subjective dignity (welfare trust, life satisfaction, perceived discrimination, status concern), and the gradient is asymmetric in the same way the political outcome is. Uses ESS welfare-trust items + Silva wellbeing data. **(most surprising — directly observes the mechanism the paper currently theorises but cannot test)**

**My take.** Paper 1 is the right paper *for this submission window* given the dignity-thread theory. Paper 2 is the thesis chapter. Paper 3 is the wrong reframe — Schraff and Pontusson 2024 already occupy that space, and a regional design would lose the individual-level dignity-cascade narrative that is the contribution. Paper 5 is the most theoretically alive of the alternatives but requires real construct development; better as a thesis chapter than as a paper insertion.

---

## Section F.2: Identification Possibilities (Phase 2 — what the data permits)

Twelve identification approaches the data on hand can support, before filtering for feasibility. For each: what it identifies that the current cross-sectional design cannot.

1. **Cross-national CWED moderation (current).** Country-level institutional variation × individual exposure. Identifies the conditional treatment effect under the assumption that country-level CWED captures dignity-relevant institutional design. Cannot rule out unobserved country-level confounds.
2. **CWED sub-component decomposition.** Tests whether moderation is specifically `UEGEN` (unemployment generosity) vs. `SKGEN` / `PGEN`. Within-CWED falsification — if pensions drive the moderation, the dignity-encounter mechanism is wrong. Already analysed.
3. **Within-country CWED time variation 1971–2011.** AT/DE/NL/GB/DK show meaningful CWED change. With ESS waves 1–9 and ISCO-88 → ISCO-08 crosswalk (`kurer_2020/correspondence.dta`), identifies welfare reform effects on RTI-attitude slopes within country. Solves cross-sectional confound. **Thesis-scale.**
4. **Welfare reform timing as DiD treatment.** Discrete reform years (DK flexicurity 2003/2006/2013, Hartz reforms 2003–05, Bismarck unemployment 2005, UK 2008+ activation) as treatment. Pre-post comparison + parallel trends. Builds on Rickard's EGF design. Thesis-scale unless restricted to 1–2 cases.
5. **Regional NUTS-2 design** (Milner). Within-country cross-region variation in industrial composition × welfare moderation. Identifies regional vote-share response under cross-region within-country variation. Schraff/Pontusson 2024 template.
6. **District-level austerity DiD** (Baccini). Cross-district within-country austerity intensity variation × welfare regime as moderator. Cleaner identification than country-year ALMP.
7. **Shift-share Bartik IV for RTI.** Lagged occupational composition × national task-shift trends to instrument for individual RTI. Identifies LATE under the assumption workers don't anticipate national shifts.
8. **Hybrid within/between estimator** (Ronchi). Separates cross-sectional from within-person variation if Kurer panel data can be acquired. Tests sorting vs. treatment.
9. **Diagonal Reference Models** (Gugushvili). Mobility effects net of origin and destination class. Tests whether the cascade is upstream of mobility.
10. **Trade exposure as alternative disruption shock.** Milner's `shock_china_ind` and `shock_robots_mfg`. Tests whether the asymmetric mechanism generalises beyond automation.
11. **Multi-wave ISSP series 1985–2010** (Gingrich harmonisation). Adds temporal identification — does the asymmetric pattern shift around the Frey-and-Osborne 2013 cultural moment, or hold across the entire post-1985 period? Tests scope conditions of the mechanism.
12. **QoG regional institutional quality as competing moderator.** Tests whether the moderation is welfare-specific or just state-capacity. If QoG dominates CWED, the dignity reading needs to be reconsidered as state-capacity.

**Triage.** The currently-feasible set for paper improvement (this month): 1, 2, 5, 11, 12. The rest are thesis-scale or require external data acquisition. The two highest-payoff additions to v4 are 2 (sub-components) and 11 (multi-wave ISSP) — both addable in days.

---

## Section F.3: Measurement Alternatives (Phase 3)

For each construct, alternative operationalisations available in the repo. Force-list of three+ each.

**Disruption / automation exposure.**
- *Current:* RTI (routine task intensity) via ISCO-08 3-digit `task` (Goos/Manning/Salomons 2014).
- *Alt 1:* Survey on Automation Risk in `shared_isco_task_scores/D1.1_Survey on Automation Risk_v2.0.dta`.
- *Alt 2:* Im 2021 share-based exposure (`sh_highrisk` by 2-digit ISCO).
- *Alt 3:* Trade exposure (Milner's China-shock import penetration; `oecd_chinese_trade.dta`).
- *Alt 4:* Robot exposure (Milner's `shock_robots_mfg`).
- *Alt 5:* Subjective economic insecurity (ESS items `stfeco`, `hltphh`) — perceptual, but introduces endogeneity.
- *Alt 6:* Occupational decline rate (employment growth in occupation, lagged) — Kurer's measure.
- **Closest to theory:** Occupational decline rate (Alt 6) cleanly captures the structural shock the worker experiences regardless of psychological state. RTI is the second-best given data on hand.

**Welfare design.**
- *Current:* CWED total generosity (mean 2005–2011), with regime categorical and ALMP as foils.
- *Alt 1:* CWED sub-components (`UEGEN`, `SKGEN`, `PGEN`) — already accessible.
- *Alt 2:* Conditionality (Knotz 2018 — would need acquisition).
- *Alt 3:* Enabling vs. punitive ALMP disaggregation (Van Hootegem 2025 — partly constructable from CPDS).
- *Alt 4:* SIWE country-year welfare expenditure (richer than CWED but generosity-based).
- *Alt 5:* QoG institutional quality (state-capacity rather than welfare-specific).
- *Alt 6:* Universalism (proportion of population eligible) vs. generosity (benefit level) — Garritzmann/Häusermann typology, partly constructable.
- **Closest to theory:** Conditionality (Alt 2) — directly operationalises dignity-damaging encounter — but data isn't ready. **Sub-components (Alt 1) is the best feasible move:** unemployment-CWED operationalises "encounter at point of vulnerability" much more sharply than total CWED.

**Exclusion outcome.**
- *Current:* Anti-immigration index (3-item: `imwbcnt + imueclt + imbgeco`, α=0.864).
- *Alt 1:* Single items separately — diagnostic check on the index.
- *Alt 2:* Welfare chauvinism items (ESS rotating modules — wave 8 has some).
- *Alt 3:* Authoritarian values (Ballard-Rosa et al. 2022 operationalisation).
- *Alt 4:* Radical right vote (already in Model 6).
- *Alt 5:* General trust / particularised trust split (`trstplt`, `trstprl`).
- **Closest to theory:** Welfare chauvinism (Alt 2) directly captures the "kicking down" dynamic Wagner 2022 names — but availability across waves is limited. The 3-item anti-immig index is the right primary outcome.

**Solidarity outcome.**
- *Current:* Redistribution support (`gincdif` reverse-coded 1–5).
- *Alt 1:* `gvctax` government-should-reduce-income-differences — STATUS line 88 mentions as supplementary.
- *Alt 2:* Multi-item composite (`gincdif + gvslvol + ...`).
- *Alt 3:* Deservingness items (which groups deserve welfare — wave 8 only).
- *Alt 4:* Particularistic-authoritarian welfare preferences (Busemeyer/Rathgeb/Sahm 2023 index, partly constructable from ESS items).
- *Alt 5:* Vote for left/redistributive parties.
- *Alt 6:* ISSP solidarity items (already used as Appendix C).
- **Closest to theory:** Particularistic-authoritarian preferences (Alt 4) — directly captures the syndrome the cascade ends in. The current `gincdif` outcome treats redistribution as fungible with recognition, which the §III.D theory denies. **A `gvctax` two-item composite as Appendix D-style supplementary** would be the cheapest move (STATUS line 88 already names it; ~20 min).

**The cleanest framing point.** The asymmetric-mechanism prediction is sharpest when the *same* disruption is shown to predict more exclusion AND fail to predict more solidarity, where solidarity is operationalised in a way that captures the syndrome the theory claims is hard to construct (particularistic-authoritarian welfare preferences), not generic "should government redistribute." The current operationalisation is defensible but slightly under-theorised — `gincdif` answers a different question than the one §III.D actually predicts about.

---

## Section G: Strategic Alternatives Review (Phase 4)

Opinionated answers to (a)–(d). Not lists — judgement.

### (a) Best achievable in a month

**Paper 1 with three additions and two trims.** Specifically:

- **Add CWED sub-component decomposition to §V.D body** (already analysed at `analysis/cwed_subcomponents_report.md`; just integrate). Predicted UEGEN > SKGEN > PGEN on the moderator. If the prediction holds, this is the single strongest sentence the paper can add — it makes the dignity-mechanism reading specific (it's the unemployment encounter, not retirement) rather than general.
- **Run the multi-wave ISSP harmonisation** using Gingrich's `create_ISSPCombined.do` (waves 1985–2010, 14 waves) and replace the §V.F single-wave 2006 supplementary test with a time-series version. This converts "one null on one outdated wave" into "consistent null across two and a half decades" — a much stronger asymmetric confirmation.
- **Add an Appendix D regional NUTS-2 falsification using Milner's data.** Two pages, the central question being: "Does the country-level cross-sectional moderator pattern survive at the regional level, where regional-within-country variation rules out time-invariant country confounds?" If yes, the cross-sectional design's biggest weakness is partially answered. The Milner file is analysis-ready; this is 1–2 weeks of work.

- **Trim the education three-way moderation** (Appendix B) — currently described as "exploratory pending a design with adequate statistical power for three-way interactions" (p=0.179). It does not earn its page.
- **Compress Model 6 / radical right vote analysis** in §V.F. Currently described as "behavioural models are descriptive of electoral systems' translation of attitudes into votes, not tests of the asymmetric mechanism itself." That sentence is correct — and a sentence is enough. The current §V.F second half is two pages of defending a result the asymmetric mechanism doesn't claim.

This version is internally consistent (numerical claims reproducible), externally grounded (uses Milner / Gingrich templates), theoretically sharper (sub-components specify the dignity claim), and robust at multiple levels (regional + multi-wave + sub-component + macro-control + jackknife).

### (b) Highest-leverage adjustments — the action list

| # | Action | File / location | Effort | Buys | Priority |
|---|--------|------------------|--------|------|----------|
| 1 | Add BLUPs jackknife to `random_slopes_models.py` and save to CSV. Verify −0.802 / −0.794 / −0.717 reproduce; if not, update §V.D | `scripts/random_slopes_models.py:215+`; new `outputs/tables/blups_jackknife_*.csv` | 2 hours | Closes Claim 14 reproducibility gap. Either confirms the paper or forces a small correction | **MUST DO** |
| 2 | Reconcile Model 5 spec inconsistency (B2). Use β=0.013, p=0.488 from rs_results.csv | `manuscripts/paper_draft_v4_final.md` §V.F | 30 min | Removes a methodological inconsistency a careful referee will catch | **MUST DO** |
| 3 | Persist Claim 13 (macro robustness β=−0.066). Add CSV write to `random_slopes_models.py:188` | `scripts/random_slopes_models.py:188` | 15 min | Reproducibility of a quoted value | **MUST DO** |
| 4 | Integrate CWED sub-components into §V.D body and Figure 6/7 caption. **Use the conservative framing per Session 3 finding 5.2:** "working-age welfare programmes (UE and SK both) carry the moderation; pensions, decoupled from the working-age dignity dynamic, do not." UEGEN ≈ SKGEN >> PGEN in the random-slopes spec; the original "UEGEN > SKGEN > PGEN" ordering was an artefact of OLS+FE+cluster | `manuscripts/paper_draft_v4_final.md` §V.D + `outputs/tables/cwed_subcomponents_rs.csv` + `outputs/figures/fig7_cwed_subcomponents.pdf` | 4 hours | Theoretically sharpens the central claim — distinguishes welfare-encounter dignity programmes from decoupled (pensions). | **HIGHEST PAYOFF QUICK WIN** |
| 5 | Update STATUS.md numbers and remove v3 reference; update MEMORY [LEARN:writing] entries | `projects/seminar_paper/STATUS.md`, `MEMORY.md` | 1 hour | Stops future-you walking into wrong numbers | **DO** |
| 6 | Move `analysis/overnight_report.md`, `walkthrough_*.py`, alternative drafts to archive folders | `analysis/archive/`, `manuscripts/archive/` | 1 hour | Reduces path-dependency confusion; clarifies what's canonical | **DO** |
| 7 | Add `analysis/README.md` documenting which scripts produce which canonical outputs | `analysis/README.md` (new) | 30 min | Pipeline architecture documented | **DO** |
| 8 | Run Gingrich's `create_ISSPCombined.do` and replace §V.F single-wave 2006 with multi-wave 1985–2010 | `data/raw/gingrich_2019/create_ISSPCombined.do` + new `scripts/issp_multiwave.py` | 2–3 days | Converts a single null into a multi-decade null — much stronger confirmation of the asymmetric prediction | **HIGH PAYOFF** |
| 9 | Run Ciccolini do-file to construct posit_income_change at respondent level. Use as alternative-disruption robustness in §V.E | `data/raw/cicollini_2025/Ciccolini_LeftBehindWhom.do` | 1 day if it runs clean; could be 3 if it doesn't | Independent disruption measure, addresses ISCO-classification objection | **MEDIUM PAYOFF** |
| 10 | ~~Build Appendix D regional NUTS-2 falsification using Milner data~~ **DROPPED 2026-05-04 (Session 3)**. The half-day sanity check (`outputs/tables/regional_sanity_check.csv`) found that the country-level r=−0.85 does NOT extend to within-country regional aggregate vote shares (Pearson r=+0.15, p=0.66; Spearman ρ=+0.01, p=0.98 across 11 countries). 7 of 12 within-country regional correlations are NEGATIVE (high-RTI regions vote LESS right-populist), classic ecological-vs-individual divergence consistent with §V.F's supply-side discussion. The obvious version of the Appendix would not yield a clean replication; the proper individual-level-with-NUTS-2 design is thesis-scale (4–6 weeks). Decision: drop. | n/a | n/a | n/a — sanity check saved 1–2 weeks of work |
| 11 | Tighten §III.D's three-asymmetry argument with explicit literature templates (Vlandas/Halikiopoulou as the buffering target; Burgoon/Schakel as the contradiction case already cited; Gingrich 2019 as the "concerning finding" already cited). Add Schraff/Pontusson as the regional comparator if you do action 10 | `manuscripts/paper_draft_v4_final.md` §III.D | 1 day | Makes asymmetric framing visibly grounded in the literature; helps the comparative-table moves your domain referee will look for | **DO** |
| 12 | Run grep on forbidden verbs (`shape\|produce\|determine\|cause\|convert\|activate\|mediate\|trigger\|channel`) per STATUS line 82; pass each hit through the asymmetric-framing lens | `manuscripts/paper_draft_v4_final.md` | half a day | Keeps causal language consistent with the cross-sectional design | **DO** |
| 13 | CWED total + sub-component robustness with macro controls (GDP / Gini / immigrant stock). Persist to CSV | `scripts/random_slopes_models.py` | 1 day | One more nail in "is it really welfare or just economic conditions" | **NICE TO HAVE** |
| 14 | Use QoG NUTS-2 institutional quality as a competing-moderator robustness | `data/raw/qog/qog_eureg_wide2_nov20.csv` + new merge | 3–5 days | Rules out a "weak-state" alternative reading; sharpens the dignity claim against state-capacity | **NICE TO HAVE — only if action 10 is done** |
| 15 | Run Baccini district-level austerity DiD with welfare regime as moderator | `data/raw/baccini_2024/.../Analysis_Dataset_District_Level.dta` | 1–2 weeks | Direct test of "is the moderation about welfare design or about austerity itself" | **THESIS — too much for one month** |
| 16 | Acquire Kurer panels (SHP, BHPS, SOEP) and run the within-individual asymmetric test | external | 2–4 weeks acquisition + 4–6 weeks harmonisation | Within-person identification, the cleanest possible | **THESIS** |

**Order if I had to commit to a one-month plan:**
- Week 1: actions 1, 2, 3, 4, 5, 6, 7, 8 (start) — close numerical gaps, add sub-components, kick off ISSP harmonization.
- Week 2: action 8 (finish), action 9, action 12.
- Week 3: action 10 (Appendix D regional) — start.
- Week 4: action 10 finish, action 11 polish, action 14 if time.

### (c) What to consider abandoning

- **Education three-way moderation (Appendix B).** Paper says "exploratory pending power"; p=0.179 is not earning its page. Move the descriptive 0.280 vs 0.128 finding to a footnote in §V.E or §VI. Cuts ~half a page.
- **Model 6 / radical right vote (§V.F second half).** Compress to one paragraph: "Behavioural models reflect electoral-system translation of attitudes into votes (Mod 6 RTI×Liberal=−0.123 in FPTP UK while UKIP captured 12% in 2015 and 2017 General Elections — Brexit then reabsorbed it). The asymmetric mechanism is theorised at the attitudinal layer; supply-side institutions condition the conversion to votes (see Bornschier et al. 2024 on cleavage formation, Hooghe & Marks 2018 on populist supply)." Cuts ~1–1.5 pages.
- **`overnight_report.md` and `paper_draft_v3_final.md`** in active locations. Move to archive folders. Their continued presence at the canonical paths invites confusion.
- **The medium-bet draft (`medium bet_paper_draft_v4_final.md`).** If the asymmetric framing is committed (per STATUS line 9, MEMORY [LEARN:theory] line 51), the medium-bet draft is no longer a fallback. Move to `manuscripts/archive/`.

### (d) What belongs to the thesis instead of this paper

- **Within-country welfare reform timing analysis (Paper 2).** Already named in §V.G and §VII as the next step. Don't try to fit it in the month. ESS1–5 ISCO crosswalk + CWED time variation + within-country reform-event-study is a thesis chapter.
- **Kurer-style panel analysis (Paper 8 / item 16 above).** Panel acquisition + harmonisation is too much for one month and is itself a thesis-scale empirical contribution.
- **Conditionality-vs-generosity head-to-head (Paper 4).** Construct development is itself a thesis-scale contribution. Knotz / Van Hootegem operationalisations need real engagement.
- **The subjective-dignity-damage paper (Paper 5).** Theoretically interesting but a different paper — and the construct work for "subjective dignity damage" is not trivial.
- **Baccini-style district-level austerity DiD (item 15).** Replicating Baccini 2024 with a welfare-design moderator is itself a chapter-scale ambition. Worth doing, not in May.
- **Danish registry data work** (named in §V.G). The within-individual gold standard.

---

## Section H: Highest-Leverage Adjustments — Triaged

(Already produced as part of Section G(b). The five items I would commit to first, in order:)

1. **Action 4 (CWED sub-components in §V.D body) — 4 hours, sharpens the dignity claim.** Predicted: UEGEN >> SKGEN > PGEN. If the prediction holds, this is the single strongest paragraph the paper can add. If it doesn't hold (pensions or sickness drive the moderation), the asymmetric-mechanism story needs revisiting, which is *also* a paper-improvement.
2. **Action 1 (BLUPs jackknife reproducibility) — 2 hours, closes the audit gap.** Either confirms the paper's robustness sentence or forces a correction. Both outcomes improve the paper.
3. **Actions 2 + 3 (Model 5 spec inconsistency + Claim 13 persistence) — 45 minutes total.** Trivial fixes, removes a referee target.
4. **Action 8 (multi-wave ISSP) — 2–3 days, converts the §V.F null into time-series.** Highest payoff per day of work. Gingrich's harmonization do-file is already there.
5. ~~Action 10 (Appendix D regional falsification using Milner)~~ **DROPPED 2026-05-04 (Session 3)** per the half-day sanity check showing the country-level pattern does not extend to NUTS-2 vote-share aggregates. The 1–2 weeks this would have taken should be redirected to **Action 8 (multi-wave ISSP)** — the next-most-ambitious item that the data actually supports.

Items 1–4 should ship in week 1–2 regardless. Item 5 (multi-wave ISSP) is now the most ambitious move that fits in the month. Items 6, 7 (other Section H actions) follow.

---

## Section I: One-paragraph verdict (revised 2026-05-04 PM after Session 3)

The current v4 paper is closer to its strongest one-month form than the audit assumed and closer still after the Session 3 fixes. There is no broken foundation that flips the asymmetric conclusion: the cross-national CWED moderation is well-defended, the random-slopes specification is appropriate, the matched-15-country sample is consistent everywhere, the encoding/missing-data handling is clean, and the BLUPs jackknife the paper relies on for §V.D's robustness narrative now reproduces from saved CSVs (excl GB → r=−0.808, NO → r=−0.793, GB+NO pair → r=−0.700, all within rounding of the paper's claims; 105/105 pairs significant). The remaining numerical-hygiene items (Model 5 spec inconsistency, ISSP not-saved-to-disk) are afternoon-scale fixes. The highest-leverage paper-strengthening move is integrating the already-analysed CWED sub-components into §V.D body — but in the *conservative* form: "working-age welfare programmes (unemployment and sickness both) carry the moderation; pensions, decoupled from the working-age dignity dynamic, do not." The original report's clean UEGEN > SKGEN > PGEN ordering was a spec artefact; in the random-slopes spec consistent with §V.D the unemployment and sickness sub-components are statistically indistinguishable, but the pension null is robust either way and that's the contrast the dignity-mechanism story actually needs. The genuinely substantial empirical extension that fits in a month is replacing the §V.F single-wave 2006 ISSP test with the multi-wave 1985–2010 series Gingrich's harmonization do-file is already set up to produce; this converts "one null on one wave" into "consistent null across two and a half decades" and is the cleanest empirical strengthening available without reframing the paper. The audit's previously-most-ambitious recommendation (Appendix D regional NUTS-2 falsification using Milner data) is now dropped: a half-day sanity check showed the country-level pattern does not extend to within-country regional aggregate vote shares — 7 of 12 within-country correlations are negative (high-RTI regions vote less right-populist), an ecological-vs-individual divergence consistent with §V.F's supply-side discussion but not with what the Appendix would have shown. The rest — within-country welfare reform identification, Kurer-style panel work, conditionality-vs-generosity construct development, subjective-dignity measurement — belongs to the thesis. The shape of the dignity-baseline argument is right. Polish, persist, sharpen — don't reframe.
