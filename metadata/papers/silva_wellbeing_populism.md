# Well-being Foundations of Populism in Europe

**Authors:** Silva, Bruno Castanho (+ co-authors?)  
**Year:** ~2022–2024  
**Journal:** European Journal of Political Research / Comparative Political Studies  
**Folder:** `data/raw/silva_wellbeing/`  
**Theory modules:** [09](../theory/09_*.md), [11](../theory/11_*.md), [12](../theory/12_*.md)

---

## Research Question

Does low subjective well-being (independent of economic hardship) predict populist party support? Can well-being improvements reduce populist appeal?

## Core Argument

Populist attitudes are grounded in subjective well-being deprivation rather than solely objective economic hardship. Life dissatisfaction and anxiety predict populist voting even after controlling for material circumstances.

## Identification Strategy

ESS cross-national analysis. Well-being measures (life satisfaction, happiness) as independent variable predicting populist party support.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (ESS, multiple countries) |
| Outcome variable | Populist party vote / populist attitudes scale |
| Sample | European countries covered by ESS |

## Key Datasets

| Dataset | Role |
|---------|------|
| `graphsdata.dta` | Silva's analysis-ready dataset — pre-aggregated for graphing |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Subjective well-being (stflife, happy, or composite)` |  |
| **outcome** | `Populist party support or populist attitude scale` |  |
| **controls** | `Objective economic situation, education, age, country FE` |  |

## ⚠️ Data Quirks

The graphsdata.dta appears to be pre-aggregated/processed data for producing graphs. For individual-level analysis you would need to go back to the ESS waves.

## Notes

Useful for module 09 (ontological security) testing — shows the psychological channel is empirically distinct from material hardship.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*