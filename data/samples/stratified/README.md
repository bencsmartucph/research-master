# Stratified Samples

> Stratified by `cntry` / `essround` / `country` to give cross-national coverage.
> Each file has ~5 rows per country (or country-wave), up to 200 rows total.
> Use these for developing and debugging multi-country analysis code.

| File | Description | Rows | Cols |
|------|-------------|------|------|
| `ESS1e06_7_strat25.csv` | ESS wave 1 (Gugushvili) | 25 | 567 |
| `ESS2e03_6_strat25.csv` | ESS wave 2 (Gugushvili) | 25 | 604 |
| `ESS3e03_7_strat30.csv` | ESS wave 3 (Gugushvili) | 30 | 519 |
| `ESS4e04_6_strat30.csv` | ESS wave 4 (Gugushvili) | 30 | 674 |
| `ESS5e03_5_strat30.csv` | ESS wave 5 (Gugushvili) | 30 | 675 |
| `cicollini_essprt_all_strat45.csv` | Cicollini: ESS with positional income change | 45 | 13 |
| `milner_merged_regional_strat200.csv` | Milner: analysis-ready regional merged data | 200 | 285 |
| `ZA6770_ISSP2016_strat200.csv` | Gingrich: ISSP 2016 Role of Government V | 200 | 442 |
| `ZA5400_ISSP2010_strat200.csv` | Gingrich: ISSP 2010 Environment III | 200 | 357 |
| `ZA4950_ISSP2009_strat200.csv` | Gingrich: ISSP 2009 Social Inequality IV | 200 | 364 |
| `baccini_individualdata_strat5.csv` | Baccini: analysis-ready individual data | 5 | 25 |
| `baccini_district_level_strat75.csv` | Baccini: district-level analysis data | 75 | 42 |
| `ZA7700_steiner_strat200.csv` | Steiner: ISSP 2019 Social Inequality | 200 | 442 |
| `euroscepticism_dta_strat200.csv` | Euroscepticism replication .dta | 200 | 38 |

## How to use

```python
import pandas as pd
df = pd.read_csv('samples/stratified/ESS1e06_7_strat200.csv')
# Develop your cross-national analysis code here
# Then switch to the full file:
# import pyreadstat
# df, meta = pyreadstat.read_dta('ACTUALLY GOOD/1 - Gugushvii.../ESS1e06_7.dta')
```

## Regenerate

```bash
python scripts/make_stratified_samples.py
```