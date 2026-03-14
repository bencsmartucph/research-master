# 🧪 Mini-Samples

> **Auto-generated** test samples — 100 rows each, drawn from the top 3 largest datasets.
> Use these to develop and debug code logic without loading gigabyte-scale files.
> ⚠️ Do NOT use for statistical inference — these are not random samples.

---

## Files in this folder

### `baccini_ESSdata`

**Source paper:** Baccini 2024 – Austerity, Economic Vulnerability, and Populism  
**Source file:** `Baciini - ESSdata.dta`  
**Description:** Baccini (2024) – individual-level ESS survey data used in austerity & populism study. **Largest dataset (599 MB, ~650k rows)**. Contains socioeconomic, political preference, and demographic variables for European respondents.

| Property | Value |
|----------|-------|
| Rows | 100 |
| Columns | 211 |
| Files | `baccini_ESSdata_sample100.csv`, `baccini_ESSdata_sample100.dta` |

**First 8 columns:** `cntry`, `cname`, `cedition`, `cproddat`, `cseqno`, `name`, `essround`, `edition`, ... (+203 more)

---

### `im_radical_right_ESS`

**Source paper:** Im – A Reservoir of Votes for the Radical Right  
**Source file:** `Im - A Reservoir of Votes for the Radical Right - ESS.csv`  
**Description:** Im et al. – pooled ESS dataset used to study radical right voting reservoirs. **Second largest (402 MB)**. Contains individual political attitudes, occupation codes, and radical right vote variables.

| Property | Value |
|----------|-------|
| Rows | 100 |
| Columns | 1379 |
| Files | `im_radical_right_ESS_sample100.csv` |

**First 8 columns:** `country`, `isco08dig2`, `sh_highrisk`, `obs`, `country_m`, `country_p`, `isco08_2`, `cntry`, ... (+1371 more)

---

### `euroscepticism_stagnation`

**Source paper:** Euroscepticism as a Syndrome of Stagnation  
**Source file:** `Euroscepticism as a syndrome of stagnation.csv`  
**Description:** Euroscepticism replication dataset (CSV version). **Third largest (135 MB)**. Country-level and individual panel data linking economic stagnation indicators to EU scepticism.

| Property | Value |
|----------|-------|
| Rows | 100 |
| Columns | 38 |
| Files | `euroscepticism_stagnation_sample100.csv` |

**First 8 columns:** `id`, `year`, `wave`, `country_new`, `nuts2_region`, `trust_eu`, `eu_pos`, `ec_exp`, ... (+30 more)

---

## How to use these samples

```python
import pandas as pd

# Load a sample to develop your analysis code
df = pd.read_csv('samples/baccini_ESSdata_sample100.csv')

# Once code is validated, switch to the full dataset:
# df = pd.read_csv('ACTUALLY GOOD/1 - Baccini .../Baciini - ESSdata.dta')
```

```stata
* In Stata, use the .dta samples directly:
use "samples/baccini_ESSdata_sample100.dta", clear
```
