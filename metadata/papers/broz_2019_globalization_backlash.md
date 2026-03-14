# The Economic Geography of the Globalization Backlash

**Authors:** Broz, J. Lawrence; Frieden, Jeffry; Weymouth, Stephen  
**Year:** 2019  
**Journal:** International Organization  
**Folder:** `data/raw/broz_2019/`  
**Theory modules:** [01](../theory/01_*.md), [03](../theory/03_*.md), [12](../theory/12_*.md)

---

## Research Question

Does globalization backlash (voting for anti-trade politicians) concentrate geographically in regions most exposed to import competition and most dependent on manufacturing?

## Core Argument

Globalization backlash is geographically concentrated in regions with high manufacturing employment exposure to low-wage import competition. The 2016 Trump vote and Brexit are both driven by this geography, not just individual-level economics.

## Identification Strategy

Regional analysis. Input-output (IO) tables measure industry-level import exposure, allocated to regions by employment shares. DID-style cross-regional comparison.

## Study Details

| Property | Value |
|----------|-------|
| Unit of analysis | Region (county/constituency/NUTS) |
| Outcome variable | Trump vote 2016 / Brexit vote / anti-trade party support |
| Sample | US (Trump) and UK (Brexit) primarily; some comparative data |

## Key Datasets

| Dataset | Role |
|---------|------|
| `BFW_IO.dta` | Input-output import exposure by industry and region |
| `BFW_manufacturing_shares.dta` | Manufacturing employment share by region |

## Variable Map

| Role | Variable(s) | Notes |
|------|------------|-------|
| **treatment** | `Import penetration (IO-based regional measure)` |  |
| **outcome** | `Anti-trade/populist vote share by region` |  |
| **controls** | `Regional income, education, demographic composition` |  |

## ⚠️ Data Quirks

Primarily a US/UK paper — limited direct applicability to continental Europe without additional trade data. The BFW IO table methodology is influential but specific.

## Notes

The IO-based regional exposure measure is more sophisticated than simple trade-to-GDP ratios. Complements the Milner OECD trade files which use a simpler approach.

---
*Context file auto-generated 2026-03-13. Update as analysis progresses.*