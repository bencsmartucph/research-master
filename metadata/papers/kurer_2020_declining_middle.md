# The Declining Middle: Occupational Change, Social Status, and the Populist Right

**Authors:** Kurer, Thomas  
**Year:** 2020  
**Journal:** Comparative Political Studies  
**Folder:** `data/raw/kurer_2020_declining_middle/`  
**Theory modules:** [02](../theory/02_*.md), [04](../theory/04_*.md), [08](../theory/08_*.md), [13](../theory/13_*.md)

---

## Research Question

Does automation-driven status decline (not actual unemployment) drive radical right voting? Can we distinguish the 'anticipated hardship' pathway from the 'experienced hardship' pathway?

## Core Argument

Routine workers who are threatened by automation but still employed — facing anticipated status decline — are the most strongly drawn to radical right parties. Actual displacement (job loss) pushes workers toward pro-welfare parties, not the radical right. Relative positional decline, not material hardship, is the core mechanism.

## Identification Strategy

Panel data design using SOEP (Germany), BHPS (UK), SHP (Switzerland). Individual fixed effects. Tracks employment trajectories over time, distinguishing those who lost jobs (experienced hardship) from those still in threatened occupations (anticipated hardship).

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Individual (panel, three countries) |
| Outcome variable | Vote for populist right party (panel, first differences) |
| Sample | Germany (SOEP), UK (BHPS), Switzerland (SHP) — three-country panel |

## Key Datasets

| Dataset | Role |
|---------|------|
| `correspondence.dta` | ISCO-88 ↔ ISCO-08 crosswalk + EGP class scheme |
| `isco08_3d-task3.csv` | RTI scores for occupation-level automation risk |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `RTI score for individual's occupation (from isco08_3d-task3)` |  |
| **key_distinction** | `employed in high-RTI job (anticipated) vs. unemployed from high-RTI job (experienced)` |  |
| **outcome** | `Radical right party vote` |  |
| **controls** | `Income change, employment status, class trajectory, country` |  |

## ⚠️ Data Quirks

Panel dataset (SOEP/BHPS/SHP) is NOT in this repository — the data folder contains only the correspondence.dta crosswalk file and replication code. Access to SOEP/BHPS/SHP requires separate licensing.

## Notes

The 'anticipated vs. experienced hardship' distinction is one of the most-cited findings in this literature. The correspondence.dta file is essential — it enables ISCO-88 → ISCO-08 conversion and EGP class scheme construction for any dataset with occupation codes.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*