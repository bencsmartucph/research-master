# Populism and Layers of Social Belonging

**Authors:** Langenkamp, Anke (+ Bienstman?)  
**Year:** 2022  
**Journal:** European Journal of Political Research  
**Folder:** `data/raw/langenkamp_2022/`  
**Theory modules:** [09](../theory/09_*.md), [10](../theory/10_*.md), [12](../theory/12_*.md)

---

## Research Question

Does social belonging (local, national, European) mediate the relationship between economic vulnerability and populist voting? Are populist voters primarily those who feel their community has declined?

## Core Argument

Layers of social belonging shape populist attitudes. Local community decline → weakened local belonging → populist mobilization. National belonging that is threatened (not absent) drives populist support.

## Identification Strategy

ESS analysis with ESS-party crosswalk to identify populist vote.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (ESS) |
| Outcome variable | Populist party vote (coded via ess_populist_crosswalk.csv) |
| Sample | European countries in ESS |

## Key Datasets

| Dataset | Role |
|---------|------|
| `ess_populist_crosswalk.csv` | KEY FILE: maps ESS party vote codes → populist classification across waves |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **key_contribution** | `The ess_populist_crosswalk.csv is the most reusable file from this study` |  |
| **treatment** | `Social belonging (atchctr, atcherp, local belonging proxy)` |  |
| **outcome** | `Populist party vote` |  |

## ⚠️ Data Quirks

The ess_populist_crosswalk.csv is the main intellectual contribution of this folder from a data infrastructure standpoint — it is cited and reused across multiple other papers.

## Notes

The crosswalk file is gold for any ESS-based populism analysis.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*