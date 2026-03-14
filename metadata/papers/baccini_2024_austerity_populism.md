# Austerity, Economic Vulnerability, and Populism

**Authors:** Baccini, Leonardo  
**Year:** 2024  
**Journal:** Comparative Political Studies / APSR (forthcoming or published)  
**Folder:** `data/raw/baccini_2024/`  
**Theory modules:** [01](../theory/01_*.md), [05](../theory/05_*.md), [13](../theory/13_*.md)

---

## Research Question

Does austerity (fiscal consolidation) increase support for populist parties, and does this effect operate through increasing economic vulnerability at the district and individual level?

## Core Argument

Austerity → economic vulnerability → populist voting. The effect operates at both the district level (regional economic decline) and the individual level (personal economic insecurity). Welfare state design moderates the effect.

## Identification Strategy

Difference-in-differences using variation in austerity exposure across UK districts (constituencies). Uses the Alesina-Ardagna austerity classification. Combines individual-level ESS data with district-level fiscal data.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (ESS) nested in districts (UK constituencies) |
| Outcome variable | Vote for populist party (primarily UK; UKIP, BNP) |
| Sample | UK constituencies, ESS waves covering 2000s–2016 |

## Key Datasets

| Dataset | Role |
|---------|------|
| `Baciini - ESSdata.dta` | Individual ESS data, 599MB — USE SAMPLE for development |
| `individualdata.dta` | Analysis-ready individual level (use this first) |
| `districtdata.dta` | Analysis-ready district level (use this first) |
| `Analysis_Dataset_District_Level.dta` | Raw district data |
| `Analysis_Dataset_Individual_Level.dta` | Raw individual data |
| `Alesinadata_annual.dta` | Fiscal consolidation episodes (annual) |
| `Austeritydata_byelperiod.csv` | Austerity by electoral period |
| `CPDS_Aug_2020.dta` | Country-level macro + welfare state |
| `ELFS_regional_routine_shares.dta` | Regional routine employment shares |
| `Global_Party_Survey.dta` | Party populism scores |
| `MPDataset_MPDS2019b.dta` | Manifesto party ideology |
| `parlgov_cabinets.csv / parlgov_ind.csv` | Cabinet data |
| `distelections.dta` | District-level election results |
| `macrodata_ind.dta` | Country macro indicators |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Austerity cuts (fiscal consolidation measure from Alesinadata / Austeritydata)` |  |
| **mediator** | `Economic vulnerability (district unemployment, individual economic insecurity)` |  |
| **outcome** | `Populist party vote share (district) or individual vote (ESS)` |  |
| **moderator** | `Welfare state type, regional routine employment share` |  |
| **controls** | `Income, education, employment status, region FE, year FE` |  |

## ⚠️ Data Quirks

The 'Baciini - ESSdata.dta' (note typo in filename) is 599MB — always use the sample or the analysis-ready individualdata.dta for development. The analysis-ready files (individualdata.dta, districtdata.dta) are in Data/ not Raw Data/.

## Notes

Most comprehensive dataset in the repo. Contains all the building blocks for a full causal chain test: austerity exposure → district economic decline → individual insecurity → populist vote.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*