# Aspiration versus Apprehension: [Automation Anxiety and Political Preferences]

**Authors:** Unknown (check folder for .do or .py scripts)  
**Year:** ~2022–2024  
**Journal:** Unknown  
**Folder:** `data/raw/aspiration_apprehension/`  
**Theory modules:** [02](../theory/02_*.md), [04](../theory/04_*.md), [08](../theory/08_*.md), [15](../theory/15_*.md)

---

## Research Question

Does anticipatory apprehension about automation (vs. aspiration) predict distinct political outcomes? Can we measure the anticipation-experience gap?

## Core Argument

Apprehension about future automation risk (anticipated hardship) drives different political responses than aspiration. The study directly tests the anticipated vs. experienced hardship distinction.

## Identification Strategy

Survey-based, likely cross-sectional. Constructs an aspiration/apprehension index from survey items.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (survey) |
| Outcome variable | Political attitudes / party preference |
| Sample | Unknown — check the CSV for country variable |

## Key Datasets

| Dataset | Role |
|---------|------|
| `aspiration_apprehension_data.csv` | Main analysis dataset with constructed index |
| `isco08_3d-task3.csv` | RTI task scores — also in this folder |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Apprehension vs. aspiration index (constructed from survey items)` |  |
| **occupation_link** | `isco08 code → merge with isco08_3d-task3 for RTI` |  |
| **outcome** | `Party preference / political attitudes` |  |

## ⚠️ Data Quirks

This is a smaller study. Check the CSV headers in data_dictionary.md to understand the survey instrument design.

## Notes

The isco08_3d-task3.csv copy in this folder is the same file as in the main repo — use either.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*