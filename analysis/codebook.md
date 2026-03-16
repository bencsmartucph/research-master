# Codebook: sorting_mechanism_master.csv
Generated: 2026-03-16
Observations: 188,764
Variables: 37

| Variable | Type | N Valid | % Missing | Mean | SD | Min | Max | Description |
|----------|------|--------|-----------|------|-----|-----|-----|-------------|
| essround | int64 | 188,764 | 0.0% | 7.47 | 1.16 | 6.00 | 9.00 | ESS wave number |
| cntry | object | 188,764 | 0.0% | NA | NA | NA | NA | Country (ISO-2) |
| cntry_wave | object | 188,764 | 0.0% | NA | NA | NA | NA | Country x wave identifier |
| welfare_regime | object | 188,764 | 0.0% | NA | NA | NA | NA | Welfare regime classification |
| idno | int64 | 188,764 | 0.0% | 8990478.66 | 58445607.32 | 1.00 | 551603139.00 | Respondent ID |
| isco08_raw | int64 | 188,764 | 0.0% | 11642.48 | 20307.01 | 0.00 | 99999.00 | Raw ISCO-08 code (4-digit) |
| isco08_3d | Int64 | 188,764 | 0.0% | 1163.97 | 2030.58 | 0.00 | 9999.00 | Truncated ISCO-08 (3-digit) |
| task | float64 | 165,667 | 12.2% | 1.93 | 0.85 | 1.00 | 3.00 | Routine task intensity score |
| imwbcnt | float64 | 180,448 | 4.4% | 4.98 | 2.39 | 0.00 | 10.00 | Immigrants make country worse(0)-better(10) |
| imueclt | float64 | 181,279 | 4.0% | 5.48 | 2.61 | 0.00 | 10.00 | Immigration undermines(0)-enriches(10) culture |
| imbgeco | float64 | 180,833 | 4.2% | 5.00 | 2.52 | 0.00 | 10.00 | Immigration bad(0)-good(10) for economy |
| anti_immig_index | float64 | 183,035 | 3.0% | 4.85 | 2.23 | 0.00 | 10.00 | Anti-immigration index (reversed, 0-10, higher=more anti) |
| gincdif | float64 | 185,351 | 1.8% | 2.08 | 1.01 | 1.00 | 5.00 | Gov should reduce income differences (1-5) |
| redist_support | float64 | 185,351 | 1.8% | 3.92 | 1.01 | 1.00 | 5.00 | Redistribution support (reversed, 1-5, higher=more support) |
| trstprl | float64 | 184,475 | 2.3% | 4.36 | 2.65 | 0.00 | 10.00 | Trust in parliament (0-10) |
| trstplt | float64 | 185,532 | 1.7% | 3.51 | 2.45 | 0.00 | 10.00 | Trust in politicians (0-10) |
| agea | float64 | 188,152 | 0.3% | 49.43 | 18.67 | 15.00 | 104.00 | Age in years |
| age_sq | float64 | 188,152 | 0.3% | 2792.35 | 1890.46 | 225.00 | 10816.00 | Age squared |
| female | float64 | 188,716 | 0.0% | 0.53 | 0.50 | 0.00 | 1.00 | Female (1=yes) |
| eisced | float64 | 187,643 | 0.6% | 3.94 | 1.84 | 1.00 | 7.00 | Education (ISCED, 1-7) |
| eduyrs | float64 | 186,808 | 1.0% | 12.84 | 3.99 | 0.00 | 40.00 | Years of education |
| hinctnta | float64 | 152,180 | 19.4% | 5.19 | 2.78 | 1.00 | 10.00 | Household income decile (1-10) |
| urban | float64 | 188,439 | 0.2% | 0.33 | 0.47 | 0.00 | 1.00 | Urban residence (1=big city/suburbs) |
| lrscale | float64 | 163,164 | 13.6% | 5.13 | 2.27 | 0.00 | 10.00 | Left-right self-placement (0-10) |
| college | float64 | 187,643 | 0.6% | 0.23 | 0.42 | 0.00 | 1.00 | College educated (ISCED>=6) |
| fieldwork_year | int64 | 188,764 | 0.0% | 2014.94 | 2.33 | 2012.00 | 2018.00 | ESS fieldwork year |
| almp_pmp | float64 | 76,905 | 59.3% | 0.69 | 0.39 | 0.08 | 2.03 | ALMP spending (% GDP, CPDS) |
| unemp_pmp | float64 | 88,361 | 53.2% | 1.09 | 0.87 | 0.20 | 3.24 | Unemployment benefits (% GDP, CPDS) |
| socexp_t_pmp | float64 | 167,525 | 11.3% | 43.43 | 12.70 | 14.50 | 64.09 | Total social expenditure (% GDP, CPDS) |
| active_passive_ratio | float64 | 71,743 | 62.0% | 0.40 | 0.16 | 0.06 | 0.77 | ALMP/(ALMP+unemployment) ratio |
| training_share | float64 | 72,355 | 61.7% | 0.28 | 0.18 | 0.00 | 0.63 | Training share of ALMP |
| incentive_share | float64 | 71,603 | 62.1% | 0.16 | 0.11 | 0.03 | 0.50 | Incentive share of ALMP |
| sbstrec | float64 | 42,224 | 77.6% | 3.03 | 1.05 | 1.00 | 5.00 | Social benefits make people lazy (1-5, wave 8) |
| sbprvpv | float64 | 43,047 | 77.2% | 2.58 | 1.00 | 1.00 | 5.00 | Social benefits prevent poverty (1-5, wave 8) |
| sbbsntx | float64 | 41,063 | 78.2% | 3.06 | 1.05 | 1.00 | 5.00 | Social benefits cost businesses too much (1-5, wave 8) |
| uentrjb | float64 | 43,313 | 77.1% | 2.98 | 1.09 | 1.00 | 5.00 | Unemployed should take any job (1-5, wave 8) |
| narrow_deserving | float64 | 43,990 | 76.7% | 3.01 | 0.87 | 1.00 | 5.00 | Narrow deservingness index (sbstrec+uentrjb, higher=more restrictive) |
