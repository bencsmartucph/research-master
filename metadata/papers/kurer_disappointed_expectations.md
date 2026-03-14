# Disappointed Expectations: Downward Mobility and Electoral Change

**Authors:** Kurer, Thomas (with van Staalduinen?)  
**Year:** 2022  
**Journal:** American Political Science Review (likely)  
**Folder:** `data/raw/kurer_2022_disappointed_expectations/`  
**Theory modules:** [04](../theory/04_*.md), [08](../theory/08_*.md), [13](../theory/13_*.md)

---

## Research Question

Does failing to meet intergenerational status expectations (status discordance) drive radical voting independently of actual income level?

## Core Argument

Political dissatisfaction is driven by the gap between expected and actual status trajectories. Voters who fall short of intergenerational expectations (measured relative to their father's occupational status) are more likely to abstain or vote for radical parties.

## Identification Strategy

Cross-national ESS analysis. Status discordance constructed as: own occupation class rank minus father's occupation class rank. Tests against absolute income and income change.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (ESS cross-sections) |
| Outcome variable | Radical party support; mainstream party vote; abstention |
| Sample | Multiple European countries (ESS) |

## Key Datasets

| Dataset | Role |
|---------|------|
| `correspondence.dta` | ISCO → EGP class scheme for both respondent and father |
| `ESS waves` | Father's occupation + own occupation + party vote |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Status discordance (own EGP rank − father EGP rank)` |  |
| **outcome** | `Radical right/left vote, abstention, mainstream party support` |  |
| **controls** | `Income, age, education, gender, country FE` |  |
| **gender_heterogeneity** | `Effect much weaker for women (emancipatory experience moderates it)` |  |

## ⚠️ Data Quirks

Father's occupation requires careful handling of 'not applicable' and missing codes in ESS. EGP class scheme construction requires the correspondence.dta crosswalk.

## Notes

Empirically pins down the 'status discordance' mechanism from module 08. The 1-2pp effect on radical voting is comparable in magnitude to income effects.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*