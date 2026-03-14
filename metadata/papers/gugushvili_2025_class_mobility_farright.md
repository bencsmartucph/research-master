# Downward Class Mobility and Far-Right Party Support in Western Europe

**Authors:** Gugushvili, Alexi  
**Year:** 2025  
**Journal:** Comparative Political Studies (likely)  
**Folder:** `data/raw/gugushvili_2025/`  
**Theory modules:** [04](../theory/04_*.md), [08](../theory/08_*.md), [13](../theory/13_*.md)

---

## Research Question

Does intergenerational downward class mobility (falling relative to one's parents) increase support for far-right parties in Western Europe?

## Core Argument

Intergenerational class downgrading — measured as an objective fall in class position relative to origin — significantly predicts far-right voting. This is distinct from both absolute poverty and current class position.

## Identification Strategy

Pooled ESS analysis (waves 1–5). Class position measured via EGP class scheme from ISCO codes. Compares own class to father's class. Country and wave fixed effects.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (ESS waves 1–5) |
| Outcome variable | Far-right party vote (coded from ESS party vote variable) |
| Sample | Western Europe, ESS rounds 1–5 (approx. 2002–2011) |

## Key Datasets

| Dataset | Role |
|---------|------|
| `ESS1e06_7.dta` | ESS wave 1 |
| `ESS2e03_6.dta` | ESS wave 2 |
| `ESS3e03_7.dta` | ESS wave 3 |
| `ESS4e04_6.dta` | ESS wave 4 |
| `ESS5e03_5.dta` | ESS wave 5 |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Class mobility: own EGP class − father's EGP class (requires correspondence.dta crosswalk)` |  |
| **outcome** | `Far-right party vote` |  |
| **controls** | `Current income, education, age, employment status, country FE, wave FE` |  |

## ⚠️ Data Quirks

ESS .dta files are large (28–51MB each). Father's occupation variable naming varies across waves. EGP class construction requires correspondence.dta from the Kurer folder.

## Notes

Complements Kurer (2020) at the cross-national level. Uses the same EGP class scheme but applies it to an ESS pooled cross-section rather than a panel.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*