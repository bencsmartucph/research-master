# The Disparate Correlates of Populist Support in the United States

**Authors:** Armaly, Miles T. (+ co-authors)  
**Year:** 2020–2021  
**Journal:** Political Behavior / Political Research Quarterly  
**Folder:** `data/raw/armaly_us/`  
**Theory modules:** [12](../theory/12_*.md), [15](../theory/15_*.md), [10](../theory/10_*.md)

---

## Research Question

Are the correlates of populist support in the United States heterogeneous across population subgroups? Do economic and cultural grievances drive populism differently for different groups?

## Core Argument

Populist support in the US has disparate correlates: economic anxiety, cultural threat, and political alienation operate differently across demographic groups. No single factor explains populism; the combination varies by group.

## Identification Strategy

US national survey (February 2020). Latent class analysis to identify distinct types of populist supporters.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (US survey) |
| Outcome variable | Populism attitude scale (multi-item) |
| Sample | US national sample, February 2020 |

## Key Datasets

| Dataset | Role |
|---------|------|
| `Data, February 2020.csv` | Raw survey data |
| `Clean Data, February 2021.dta` | Cleaned analysis dataset |
| `mean by item.csv` | Item-level descriptives |
| `lca means.csv / lca means 10 classes.csv` | LCA results |
| `populism means.csv / mean short populism.csv` | Populism scale scores |
| `Correlations.csv` | Correlation matrix |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **outcome** | `Populism scale (multi-item Likert battery)` |  |
| **predictors** | `Economic anxiety, cultural threat, political alienation, partisanship` |  |
| **methodology** | `Latent class analysis (see lca means files)` |  |

## ⚠️ Data Quirks

US-focused — limited direct comparability to European studies. The LCA approach is methodologically distinct from regression-based European studies.

## Notes

Useful as a comparative reference point for the US case. The misattribution mechanism (module 15) is particularly relevant here.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*