# Voting for Populism: Globalization, Technological Change, and the Extreme Right

**Authors:** Milner, Helen V. (with Rudra? or solo)  
**Year:** 2021  
**Journal:** Journal of Politics / IO / Comparative Political Studies  
**Folder:** `data/raw/milner_2021/`  
**Theory modules:** [01](../theory/01_*.md), [02](../theory/02_*.md), [03](../theory/03_*.md), [12](../theory/12_*.md)

---

## Research Question

Do globalization (trade exposure) and technological change (RTI) independently and jointly predict extreme right voting at both regional and individual levels?

## Core Argument

Both trade exposure and automation risk predict extreme right voting. The effects are largely independent (not mediated by each other), suggesting they operate through different mechanisms. Regional concentration amplifies individual-level effects.

## Identification Strategy

Multi-level analysis combining OECD trade data (regional exposure) with individual ESS data and RTI occupation scores. Both regional OLS and individual-level models.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Both regional (NUTS2) and individual (ESS) |
| Outcome variable | Far-right/extreme right vote share (regional) and individual vote choice |
| Sample | Western Europe, NUTS2 regions, ESS waves |

## Key Datasets

| Dataset | Role |
|---------|------|
| `milner - ess.csv` | Milner's processed ESS file, 78MB — in Good Data |
| `oecd_chinese_trade.dta` | Chinese import penetration by region |
| `oecd_lowwage_trade.dta` | Low-wage trade exposure |
| `oecd_world_trade.dta` | Overall trade openness |
| `regional_gdp_by_year.dta` | ARDECO regional GDP (NUTS2) |
| `regional_data_impute.dta` | Imputed regional economic data |
| `imputed_econdata_voteshare_merged.dta` | ANALYSIS-READY merged regional file |
| `CLEA_voteshare_turnout.dta` | Constituency vote shares |
| `party_classifications.dta` | Party family classifications |
| `parlgov_election_05202020.csv` | Election data |
| `FRED_deflator_2020 (2015 base).csv` | Price deflator |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment_1** | `Chinese import penetration (regional, from oecd_chinese_trade)` |  |
| **treatment_2** | `RTI share of regional employment (from ELFS / isco08_3d-task3 + ESS)` |  |
| **outcome** | `Far-right vote share (regional) or individual radical right vote` |  |
| **controls** | `Regional GDP, unemployment, education, manufacturing share` |  |

## ⚠️ Data Quirks

The milner - ess.csv in Good Data/ is a working copy. The canonical analysis-ready file is imputed_econdata_voteshare_merged.dta in ACTUALLY GOOD/. The FRED deflator is needed to put trade flows in real terms.

## Notes

This replication pack is the most complete for multi-level trade + automation analysis. The imputed_econdata_voteshare_merged.dta file is extremely useful — it has already merged regional economic data with vote shares.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*