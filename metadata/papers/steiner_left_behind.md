# Left Behind and United by Populism? Class, Populism and Political Representation in Europe

**Authors:** Steiner, Nils D. (likely)  
**Year:** ~2020–2022  
**Journal:** Politische Vierteljahresschrift / West European Politics  
**Folder:** `data/raw/steiner_left_behind/`  
**Theory modules:** [03](../theory/03_*.md), [09](../theory/09_*.md), [10](../theory/10_*.md), [12](../theory/12_*.md)

---

## Research Question

Are 'left-behind' communities (economically declining regions and social groups) more united by populism than divided by economic interests? Is shared grievance a stronger predictor of populism than class position?

## Core Argument

Populism serves as a common political home for diverse 'left-behind' groups whose traditional class-based political homes have collapsed. Shared feelings of being left behind transcend class divisions.

## Identification Strategy

ISSP analysis (ZA7700 — social inequality module) with geographic/community context variables.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (ISSP survey) |
| Outcome variable | Populist party support or populist attitudes |
| Sample | Multiple countries (ISSP 2019 Social Inequality module) |

## Key Datasets

| Dataset | Role |
|---------|------|
| `ZA7700_v2-0-0-mv.dta` | ISSP 2019 Social Inequality — main analysis file |
| `ZA7700 - steiner.csv` | CSV version (32MB) — same data |
| `R_Plots_Data.csv` | Processed data for R plots |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Left-behind index (economic + geographic + subjective)` |  |
| **outcome** | `Populist party support, anti-establishment attitudes` |  |
| **controls** | `Class, income, education, country FE` |  |

## ⚠️ Data Quirks

ZA7700 is the 2019 ISSP Social Inequality module — one of the most recent and richest ISSP waves for this literature. Value labels are numeric — load meta.

## Notes

Connects module 03 (place-based decline) and module 10 (moral economy) through the shared 'left behind' framing.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*