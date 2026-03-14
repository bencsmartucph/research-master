# Euroscepticism as a Syndrome of Stagnation

**Authors:** Unknown (check for authorship in file or README)  
**Year:** ~2022–2024  
**Journal:** European Union Politics / JEPP  
**Folder:** `data/raw/euroscepticism_stagnation/`  
**Theory modules:** [01](../theory/01_*.md), [03](../theory/03_*.md), [09](../theory/09_*.md), [15](../theory/15_*.md)

---

## Research Question

Is Euroscepticism driven by stagnation — economic, social, and political — rather than a coherent ideology? Can stagnation indicators predict EU attitudes better than standard economic grievance measures?

## Core Argument

Euroscepticism is a 'syndrome of stagnation': it is driven by a combination of economic stagnation, blocked social mobility, and dissatisfaction with democracy — rather than purely economic or cultural factors. It is the co-occurrence of multiple forms of stagnation that produces it.

## Identification Strategy

Multi-country panel or pooled cross-section. Stagnation indicators constructed from economic, social, and political data.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (survey) possibly with country-year context variables |
| Outcome variable | Euroscepticism / anti-EU attitudes |
| Sample | Multiple EU member states |

## Key Datasets

| Dataset | Role |
|---------|------|
| `Euroscepticism...replication-1.dta` | Main analysis .dta file, 90MB — use this |
| `Euroscepticism...csv` | Same dataset as .csv (135MB) — .dta version preferred |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Stagnation indicators (economic + social + political)` |  |
| **outcome** | `EU attitude measures (trust in EU, anti-EU vote, exit support)` |  |
| **controls** | `Country FE, wave/year FE, standard sociodemographics` |  |

## ⚠️ Data Quirks

The CSV (135MB) and the DTA (90MB) appear to contain the same data — use the .dta for R/Python analysis. The CSV has encoding issues — use latin-1 if utf-8 fails.

## Notes

Useful for connecting the standard economic vulnerability → radical right story to a distinct EU-specific outcome variable.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*