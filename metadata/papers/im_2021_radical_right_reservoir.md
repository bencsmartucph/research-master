# A Reservoir of Votes for the Radical Right: How Automation and Labour Market Vulnerability Predict Radical Right Voting

**Authors:** Im, Zhen Jie; Mayer, Nonna; Palier, Bruno; Palme, Joakim (or Im & Komp-Leukkunen)  
**Year:** 2019/2021  
**Journal:** West European Politics / EJPR  
**Folder:** `data/raw/im_2021/`  
**Theory modules:** [02](../theory/02_*.md), [04](../theory/04_*.md), [12](../theory/12_*.md)

---

## Research Question

Does automation risk create a 'reservoir' of potential radical right voters among workers who are 'just about managing' — employed in threatened occupations but not yet unemployed?

## Core Argument

Automation risk predicts radical right voting only for those who are financially 'just about managing' — not the very poor (who turn to the left) nor the comfortable (who don't feel threatened). This non-linear relationship identifies the specific vulnerability window.

## Identification Strategy

Pooled cross-sectional ESS analysis. RTI score merged by occupation code. Interaction between automation risk and financial situation category.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (pooled ESS, multiple waves and countries) |
| Outcome variable | Vote for radical right party |
| Sample | Western Europe, multiple ESS waves |

## Key Datasets

| Dataset | Role |
|---------|------|
| `Im - A Reservoir...ESS.csv` | Pooled ESS, 402MB — USE SAMPLE for development |
| `isco08_3d-task3.csv` | RTI scores by occupation |
| `ess_populist_crosswalk.csv` | ESS party codes → populist classification |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Automation risk / RTI score (from isco08_3d-task3, merged by isco08_3d)` |  |
| **moderator** | `Financial situation category (ESS `hinctnta` or `subjinc` equivalent)` |  |
| **outcome** | `Radical right party vote (coded via ess_populist_crosswalk)` |  |
| **controls** | `Education, age, gender, country FE, wave FE` |  |

## ⚠️ Data Quirks

The 402MB CSV may have encoding issues — use latin-1 if utf-8 fails. Column names may differ from standard ESS naming — check the data_dictionary.md schema.

## Notes

The 'just about managing' finding is a key heterogeneity result for module 02 and 04 theory. The non-linear effect means OLS will underestimate it.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*