# Seminar Paper — STATUS

> **NEXT:** Run main models in R using lme4 random slopes as final specification.

## Paper

**Title:** "The Wrong Politics: How Welfare Institutions Sort Economic Disruption into Solidarity or Scapegoating"

**Stage:** Analysis complete. Draft at v3. Submission blocked on R lme4 replication.

**Key files:**
- Draft: `manuscripts/paper_draft_v3_final.md`
- Pipeline: `analysis/final_analysis_pipeline.py`
- Dataset: `analysis/sorting_mechanism_master_v2.csv` (188,764 × 48)
- Results: `analysis/final_results.json`
- Review: `analysis/econometric_review.md`

## Empirical Narrative (present in this order)

1. RTI predicts anti-immigration everywhere (Model 1, β=0.182, N=125,169)
2. Stronger in Liberal regimes (Model 2, RTI × Liberal β=0.117, p=0.002 with random slopes)
3. NOT about spending — ALMP shows wrong direction (r=+0.41) — the ALMP puzzle
4. IS about decommodification — CWED r=-0.848 across 15 countries (Model 3, β=-0.056, p<0.001)
5. Concentrated among non-college workers (54% slope reduction, but p=0.179 — suggestive)
6. Produces attitudes, not necessarily votes (Model 6, supply-side constraint UK/IE)
7. Robust: jackknife range [0.073, 0.161], never crosses zero

**Figure 6** (CWED vs. country slopes) is the single most important figure.

## Decisions Already Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Main DV | Anti-immigration index (3 items, α=0.864) | High reliability |
| Welfare measure | CWED generosity (primary), regime (secondary) | Theoretically superior |
| Reference category | Nordic | Most dignity-preserving |
| Model ordering | Model 3 leads, Model 2 supports | CWED stronger + more precise |
| Education | Report descriptively, note non-significant 3-way | Honest |
| RR vote | Include, explain supply-side | Adds depth |
| Random slopes | Required: `(1 + task_z | cntry_wave)` | LR test p<10⁻²⁰ |

## Outstanding Tasks

1. ⬜ R lme4 replication with random slopes (submission blocker)
2. ⬜ Add GDP/Gini/immigration controls to Model 3 in final draft
3. ⬜ Figure polishing session
4. ⬜ Low-effort extensions (CWED sub-components, wave stability, gender)
5. ⬜ Final proofread + reference audit (Wagner, Stutzmann, Pelc)
6. ⬜ Income missingness sensitivity check

---
*Updated April 2026.*
