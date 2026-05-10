# `analysis/` — Pipeline Architecture and Canonical Sources

**Last updated:** 2026-05-04 (audit Action 7)

This directory contains the analysis pipeline. There are TWO co-existing pipelines, and this README clarifies which is canonical for which numbers.

---

## Canonical-source map for paper numbers

| Paper claim / quantity | Canonical source | File |
|------------------------|------------------|------|
| Models 1, 2, 3 (random-slopes spec) — coefficients, SEs, p-values | `scripts/random_slopes_models.py` → `outputs/tables/rs_results.csv` | rows `M1_baseline_rs`, `M2_regime_rs`, `M3_cwed_rs` |
| Model 3 macro-controls robustness (Claim 13: β=−0.066) | `scripts/random_slopes_models.py` → `outputs/tables/rs_macro_controls.csv` | row `M3_cwed_macro_controls` |
| Random-slopes vs random-intercepts comparison (Claim 7) | `scripts/random_slopes_models.py` → `outputs/tables/rs_vs_ri_model3.csv` | both specs, REML |
| Country-level RTI slope ↔ CWED correlation (Claim 8: r=−0.848) | `scripts/random_slopes_models.py` BLUPs block → `outputs/tables/blups_country_slopes.csv` | per-country BLUPs |
| BLUPs jackknife (Claim 14) | `scripts/random_slopes_models.py` → `outputs/tables/blups_jackknife_single.csv`, `blups_jackknife_two.csv` | single and pair drops |
| Bivariate per-country OLS slopes ("replication appendix" alternative) | `scripts/random_slopes_models.py` → `outputs/tables/per_country_slopes.csv`, `jackknife_single_country.csv`, `jackknife_two_country.csv` | weaker than BLUPs (full-sample r=−0.625 vs −0.848) |
| Models 5, 6 (random-intercepts spec; redistribution and radical-right vote) | `analysis/final_analysis_pipeline.py` → `analysis/final_results.json` | `model5`, `model6` keys |
| Country-level r vs ALMP (Claim 9: r=0.01, matched 15) | `analysis/final_analysis_pipeline.py` → `analysis/final_results.json` | `almp_vs_slopes_matched` |
| ISSP supplementary test (Claim 11) | `scripts/issp_solidarity_leg.py` (prints to stdout; not persisted) | n/a |

---

## The two pipelines

### `scripts/random_slopes_models.py` (CANONICAL for headline numbers)

**Random-slopes mixed model spec.** Random slopes for RTI by country-wave for Models 1–3 (and for Model 5 redistribution if you re-run). The paper's §V.B states "I estimate mixed models with country-wave random slopes for RTI (`1 + RTI | country-wave`)" — this is the script that does that.

**Outputs in `outputs/tables/`:**
- `rs_results.csv` — Models 1–5 (random slopes)
- `rs_macro_controls.csv` — Model 3 + GDP/Gini macro controls
- `rs_vs_ri_model3.csv` — RI vs RS direct comparison on the same complete-case sample
- `rs_jackknife.csv` — Model 3 interaction-coefficient leave-one-country-out
- `per_country_slopes.csv` — bivariate per-country OLS slopes (15 countries)
- `jackknife_single_country.csv`, `jackknife_two_country.csv` — bivariate jackknife
- `blups_country_slopes.csv` — BLUPs at country level (paper's r=−0.848 source)
- `blups_jackknife_single.csv`, `blups_jackknife_two.csv` — BLUPs jackknife (Claim 14)

### `analysis/final_analysis_pipeline.py` (HISTORICAL — random intercepts)

**Random-intercepts spec, March–April 2026.** Generates `analysis/final_results.json` plus the figures via `outputs/tables/`. Still run for Models 5, 6, the country correlations, and the ALMP/CWED matched-sample comparison.

**Outputs:**
- `analysis/final_results.json` — Models 1–7 (RI), country correlations, ALMP comparison
- (March 16 outputs in `outputs/tables/archive/march16_pre_random_slopes/` — superseded)

The headline coefficients in `final_results.json:model1/model2/model3` are random-INTERCEPTS values (β=0.182, 0.117, −0.056). These are NOT what the paper reports. The paper reports the random-slopes values (β=0.168, 0.127, −0.059) from `rs_results.csv`.

### `analysis/_diagnose_cwed_correlation.py` (DIAGNOSTIC)

Tests four methodologies for computing the country-level RTI slope:
1. Bivariate per-country OLS → r=−0.625
2. OLS with controls → r=−0.786
3. BLUPs from random-slopes mixed model with controls → r=−0.855 (matches paper's −0.848 within rounding)
4. Country-wave OLS averaged within country → r=−0.702

Used once during April 2026 to settle the methodology question. The BLUPs computation is now also performed in `random_slopes_models.py` (BLUPs block) so this diagnostic is no longer needed for the headline number, but is preserved as the original methodology audit.

---

## Order of operations (full re-run)

If you need to regenerate everything from scratch:

```bash
# 1. Build the master analysis dataset (sorting_mechanism_master_v2.csv)
python analysis/run_sorting_mechanism.py

# 2. Run the historical pipeline (Models 1-7 RI, country correlations, figures inputs)
python analysis/final_analysis_pipeline.py

# 3. Run the canonical random-slopes pipeline (paper headline numbers)
python scripts/random_slopes_models.py

# 4. Optional: regenerate the figures
python scripts/create_figures_final.py

# 5. Optional: pedagogical walkthrough figures (in archive)
python analysis/archive/walkthrough/walkthrough_figures.py
```

---

## Subdirectories

- `review_diagnostics/` — model validation, sensitivity, missingness, Cook's distance, VIF, etc. Generated by `analysis/review_diagnostics_part2.py` and `analysis/econometric_review_diagnostics.py`.
- `archive/` — superseded scripts and reports. See `archive/README.md` if present.
- `archive/walkthrough/` — pedagogical scripts used to produce `outputs/figures/walkthrough/`.

---

## Documentation files

- `codebook.md` — variable definitions and transformations
- `econometric_review.md` — methods choices and assumptions
- `cwed_subcomponents_report.md` — CWED decomposition into UEGEN / SKGEN / PGEN
- `final_analysis_report.md` — historical pipeline overview (some references to archived files; treat as historical record)
