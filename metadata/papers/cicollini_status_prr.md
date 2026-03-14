# Economic Status Loss and Populist Radical Right Voting

**Authors:** Cicollini, Silvia (or Ciccolini)  
**Year:** 2024–2025  
**Journal:** Comparative Political Studies / APSR  
**Folder:** `data/raw/cicollini_2025/`  
**Theory modules:** [08](../theory/08_*.md), [13](../theory/13_*.md), [15](../theory/15_*.md)

---

## Research Question

Does positional income change (change in income rank, not absolute income) explain support for populist radical right parties, controlling for absolute income changes?

## Core Argument

Economic status loss (falling in the income distribution) predicts PRR voting independently of absolute income deterioration. Status as zero-sum means relative decline generates resentment even when absolute living standards are stable.

## Identification Strategy

ESS panel or repeated cross-section. Constructs positional income change as income rank change within country-wave. Includes absolute income + income change as controls.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (ESS, multiple waves) |
| Outcome variable | Populist radical right party vote; cultural conservatism; anti-redistribution |
| Sample | Western Europe, ESS (multiple waves) |

## Key Datasets

| Dataset | Role |
|---------|------|
| `essprt-all.dta` | ESS with CONSTRUCTED positional income change variable — key dataset |
| `election_year_data.dta` | Country-election year data for merge |
| `partyfacts-core.csv` | Party crosswalk |
| `partyfacts-mapping.csv` | Party mapping across sources |
| `ess_populist_crosswalk.csv` | ESS party codes → populist classification |
| `view_party.csv` | Party view data |
| `public_data_link_export_2021-09-28.csv` | Partyfacts export |
| `world-c.dta / world-d.dta` | Stata ado world files |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Positional income change (pre-constructed in essprt-all.dta)` |  |
| **outcome** | `PRR vote; anti-immigration; anti-EU; anti-redistribution` |  |
| **controls** | `Absolute income, income change, education, age, country FE` |  |

## ⚠️ Data Quirks

essprt-all.dta already has the key positional income variable constructed — don't reconstruct from scratch. world-c.dta and world-d.dta are Stata map files, not analysis datasets.

## Notes

The 14pp effect of positional income on PRR probability is one of the strongest status-based findings. The anti-redistribution finding (status losers oppose redistribution) is counterintuitive and important.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*