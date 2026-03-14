# Did State Responses to Automation Matter for Voters?

**Authors:** Gingrich, Jane  
**Year:** 2019  
**Journal:** Comparative Political Studies (likely)  
**Folder:** `data/raw/gingrich_2019/`  
**Theory modules:** [02](../theory/02_*.md), [04](../theory/04_*.md), [05](../theory/05_*.md), [06](../theory/06_*.md)

---

## Research Question

Do state-level policy responses to automation exposure (ALMPs, retraining programmes) moderate the relationship between automation risk and radical right voting?

## Core Argument

Automation risk (measured via RTI at the occupation level) drives support for the populist right, but the effect is conditional on what states did to help routine workers. Active labour market policies can partially offset the political backlash from automation exposure.

## Identification Strategy

Cross-national comparison using ISSP survey data merged with occupational RTI scores and country-level ALMP spending data. Interaction design: automation exposure × ALMP generosity.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (ISSP survey respondents) nested in countries |
| Outcome variable | Vote for populist right party (binary or vote share) |
| Sample | Multiple Western European countries, 2000s–2016, multiple ISSP waves |

## Key Datasets

| Dataset | Role |
|---------|------|
| `isco08_3d-task3.csv` | RTI task scores merged by ISCO code |
| `ZA-series ISSP files (ZA2880–ZA6770)` | Survey data: vote choice + occupation |
| `RP_Context_Data.dta` | Regional/national policy context, ALMP spending |
| `CPDS_Aug_2020.dta` | Country-level welfare state indicators |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Routine Task Intensity (RTI) from isco08_3d-task3.csv → merge via isco code` |  |
| **moderator** | `ALMP spending % GDP (CPDS) or state policy response (RP_Context_Data)` |  |
| **outcome** | `Vote for populist right (coded from ISSP party vote variable)` |  |
| **controls** | `Income, education, age, employment status, country FE` |  |

## ⚠️ Data Quirks

ISSP ZA-files use numeric value labels for everything — always load meta.variable_value_labels. Occupation codes may be ISCO-88 in older waves; use correspondence.dta to crosswalk to ISCO-08.

## Notes

This paper is foundational for the automation → populism literature. The RP_Context_Data.dta file is unique — it contains Gingrich's constructed policy context variable.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*