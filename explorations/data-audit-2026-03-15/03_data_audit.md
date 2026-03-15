# 03 -- Data Audit Output
> Phase 3: Live variable verification | Date: 2026-03-15

```

============================================================
## DATA AUDIT -- Ben Smart Dissertation Infrastructure
============================================================

Date: 2026-03-15
Checking: sample file presence, variable existence, merge viability
BASE: C:\Users\PKF715\Documents\claude_repos\Research_Master

============================================================
## 1. STRATIFIED SAMPLE FILE PRESENCE
============================================================

  [OK] File present: ESS1e06_7_strat25.csv
  [OK] File present: ESS2e03_6_strat25.csv
  [OK] File present: ESS3e03_7_strat30.csv
  [OK] File present: ESS4e04_6_strat30.csv
  [OK] File present: ESS5e03_5_strat30.csv
  [OK] File present: ZA4950_ISSP2009_strat200.csv
  [OK] File present: ZA5400_ISSP2010_strat200.csv
  [OK] File present: ZA6770_ISSP2016_strat200.csv
  [OK] File present: ZA7700_steiner_strat200.csv
  [OK] File present: baccini_district_level_strat75.csv
  [OK] File present: baccini_individualdata_strat5.csv
  [OK] File present: cicollini_essprt_all_strat45.csv
  [OK] File present: euroscepticism_dta_strat200.csv
  [OK] File present: milner_merged_regional_strat200.csv

  Loaded 14/14 sample files successfully

============================================================
## 2. ESS CORE VARIABLES (waves 1-5, Gugushvili)
============================================================


  ESS1: 25 rows, 567 columns
  [OK] ESS1: cntry -- 0% missing
  [OK] ESS1: essround -- 0% missing
  [OK] ESS1: lrscale -- 8% missing
  [OK] ESS1: trstprl -- 0% missing
  [OK] ESS1: trstplt -- 0% missing
  [OK] ESS1: trstep -- 16% missing
  [OK] ESS1: stflife -- 0% missing
  [OK] ESS1: happy -- 0% missing
  [OK] ESS1: stfgov -- 4% missing
  [OK] ESS1: stfdem -- 0% missing
  [OK] ESS1: imwbcnt -- 8% missing
  [OK] ESS1: imueclt -- 8% missing
  [OK] ESS1: gincdif -- 0% missing
  [XX] ESS1: atchctr -- NOT PRESENT
  [XX] ESS1: atcherp -- NOT PRESENT
  [OK] ESS1: sclact -- 4% missing
  --- Occupation variables ---
  [XX] ESS1: isco08 -- ABSENT -- see note below
  [OK] ESS1: iscoco -- present
  [OK] ESS1: iscocop -- present
  [XX] ESS1: isco88 -- ABSENT -- see note below
  --- Income variables ---
  [!!] ESS1: hinctnta -- NOT PRESENT
  [!!] ESS1: dfincac -- NOT PRESENT
  [OK] ESS1: has prtvt* vote variables -- 21 country-specific vote vars

  ESS2: 25 rows, 604 columns
  [OK] ESS2: cntry -- 0% missing
  [OK] ESS2: essround -- 0% missing
  [OK] ESS2: lrscale -- 16% missing
  [OK] ESS2: trstprl -- 4% missing
  [OK] ESS2: trstplt -- 4% missing
  [OK] ESS2: trstep -- 12% missing
  [OK] ESS2: stflife -- 0% missing
  [OK] ESS2: happy -- 0% missing
  [OK] ESS2: stfgov -- 0% missing
  [OK] ESS2: stfdem -- 0% missing
  [OK] ESS2: imwbcnt -- 4% missing
  [OK] ESS2: imueclt -- 4% missing
  [OK] ESS2: gincdif -- 4% missing
  [XX] ESS2: atchctr -- NOT PRESENT
  [XX] ESS2: atcherp -- NOT PRESENT
  [OK] ESS2: sclact -- 0% missing
  --- Occupation variables ---
  [XX] ESS2: isco08 -- ABSENT -- see note below
  [OK] ESS2: iscoco -- present
  [OK] ESS2: iscocop -- present
  [XX] ESS2: isco88 -- ABSENT -- see note below
  --- Income variables ---
  [!!] ESS2: hinctnta -- NOT PRESENT
  [!!] ESS2: dfincac -- NOT PRESENT
  [OK] ESS2: has prtvt* vote variables -- 25 country-specific vote vars

  ESS3: 30 rows, 519 columns
  [OK] ESS3: cntry -- 0% missing
  [OK] ESS3: essround -- 0% missing
  [OK] ESS3: lrscale -- 13% missing
  [OK] ESS3: trstprl -- 3% missing
  [OK] ESS3: trstplt -- 3% missing
  [OK] ESS3: trstep -- 7% missing
  [OK] ESS3: stflife -- 0% missing
  [OK] ESS3: happy -- 0% missing
  [OK] ESS3: stfgov -- 3% missing
  [OK] ESS3: stfdem -- 3% missing
  [OK] ESS3: imwbcnt -- 3% missing
  [OK] ESS3: imueclt -- 3% missing
  [OK] ESS3: gincdif -- 3% missing
  [XX] ESS3: atchctr -- NOT PRESENT
  [XX] ESS3: atcherp -- NOT PRESENT
  [OK] ESS3: sclact -- 0% missing
  --- Occupation variables ---
  [XX] ESS3: isco08 -- ABSENT -- see note below
  [OK] ESS3: iscoco -- present
  [OK] ESS3: iscocop -- present
  [XX] ESS3: isco88 -- ABSENT -- see note below
  --- Income variables ---
  [!!] ESS3: hinctnta -- NOT PRESENT
  [!!] ESS3: dfincac -- NOT PRESENT
  [OK] ESS3: has prtvt* vote variables -- 24 country-specific vote vars

  ESS4: 30 rows, 674 columns
  [OK] ESS4: cntry -- 0% missing
  [OK] ESS4: essround -- 0% missing
  [OK] ESS4: lrscale -- 13% missing
  [OK] ESS4: trstprl -- 3% missing
  [OK] ESS4: trstplt -- 0% missing
  [OK] ESS4: trstep -- 17% missing
  [OK] ESS4: stflife -- 0% missing
  [OK] ESS4: happy -- 0% missing
  [OK] ESS4: stfgov -- 3% missing
  [OK] ESS4: stfdem -- 10% missing
  [OK] ESS4: imwbcnt -- 3% missing
  [OK] ESS4: imueclt -- 7% missing
  [OK] ESS4: gincdif -- 0% missing
  [XX] ESS4: atchctr -- NOT PRESENT
  [XX] ESS4: atcherp -- NOT PRESENT
  [OK] ESS4: sclact -- 7% missing
  --- Occupation variables ---
  [XX] ESS4: isco08 -- ABSENT -- see note below
  [OK] ESS4: iscoco -- present
  [OK] ESS4: iscocop -- present
  [XX] ESS4: isco88 -- ABSENT -- see note below
  --- Income variables ---
  [OK] ESS4: hinctnta -- 47% missing
  [OK] ESS4: dfincac -- 0% missing
  [OK] ESS4: has prtvt* vote variables -- 29 country-specific vote vars

  ESS5: 30 rows, 675 columns
  [OK] ESS5: cntry -- 0% missing
  [OK] ESS5: essround -- 0% missing
  [OK] ESS5: lrscale -- 10% missing
  [OK] ESS5: trstprl -- 7% missing
  [OK] ESS5: trstplt -- 0% missing
  [OK] ESS5: trstep -- 0% missing
  [OK] ESS5: stflife -- 0% missing
  [OK] ESS5: happy -- 3% missing
  [OK] ESS5: stfgov -- 0% missing
  [OK] ESS5: stfdem -- 0% missing
  [OK] ESS5: imwbcnt -- 10% missing
  [OK] ESS5: imueclt -- 3% missing
  [OK] ESS5: gincdif -- 3% missing
  [XX] ESS5: atchctr -- NOT PRESENT
  [XX] ESS5: atcherp -- NOT PRESENT
  [OK] ESS5: sclact -- 0% missing
  --- Occupation variables ---
  [XX] ESS5: isco08 -- ABSENT -- see note below
  [OK] ESS5: iscoco -- present
  [OK] ESS5: iscocop -- present
  [XX] ESS5: isco88 -- ABSENT -- see note below
  --- Income variables ---
  [OK] ESS5: hinctnta -- 30% missing
  [!!] ESS5: dfincac -- NOT PRESENT
  [OK] ESS5: has prtvt* vote variables -- 25 country-specific vote vars

  *** IMPORTANT: ESS waves 1-5 (Gugushvili) contain iscoco (ISCO-88),
  *** NOT isco08 (ISCO-08). The ISCO-88->ISCO-08 crosswalk (correspondence.dta)
  *** is required before merging to isco08_3d-task3.csv task scores.
  *** Direct merge path in CLAUDE.md does NOT apply to these files.

============================================================
## 3. TASK SCORE FILE (isco08_3d-task3.csv)
============================================================

  [OK] Task score file exists -- C:\Users\PKF715\Documents\claude_repos\Research_Master\data\raw\shared_isco_task_scores\isco08_3d-task3.csv
  Columns: ['isco08_3d', 'task']
  Rows: 125
  [OK] isco08_3d column present
  [OK] task column present
  [!!] rtask column present (as documented) -- NOT PRESENT -- actual column is "task"
  [!!] nrtask column present (as documented) -- NOT PRESENT -- task file has one composite score only
  Task score range: 1 - 3
  N ISCO-08 3-digit codes covered: 125

============================================================
## 4. ISCO CROSSWALK: correspondence.dta (Kurer 2020)
============================================================

  [OK] correspondence.dta exists
  Columns: ['isco08', 'isco88']
  Rows: 446
  [OK] isco08 column in correspondence
  [OK] isco88 column in correspondence
  [OK] ESS3 iscoco -> isco08 via correspondence (step 1) -- 89.1% matched
  [OK] Step 2: isco08_3d -> task score -- 87.5% matched (via 2-step path)
  Pre-merge rows: 30 -> Post step2: 64

============================================================
## 5. ESS POPULIST CROSSWALK (Langenkamp 2022)
============================================================

  [OK] ess_populist_crosswalk.csv exists
  Columns: ['cntry', 'essround', 'variable', 'ess_id', 'party', 'partyfacts_id', 'partyfacts_name']
  Separator: ";"
  [OK] cntry column present
  [OK] essround column present
  [!!] Direct populism classification column -- ABSENT -- crosswalk maps to partyfacts IDs only, not a populism flag
  Total rows (party-country-round combinations): 3469

============================================================
## 6. CICOLLINI: posit_income_change (STATUS VARIABLE)
============================================================

  [OK] essprt-all.dta exists
  Rows: 5402 | Columns: 13
  Columns: ['ess_cntry', 'essround', 'ess_variable', 'ess_party', 'ess_party_id', 'ess_id', 'first_ess_id', 'partyfacts_id', 'country', 'name_short', 'name', 'name_english', 'technical']
  [XX] posit_income_change present in essprt-all.dta -- ABSENT -- this file is a party crosswalk (ESS vote codes -> partyfacts IDs)
  *** CRITICAL: essprt-all.dta is a PARTY CROSSWALK, not an individual survey file.
  *** posit_income_change is constructed from EU-SILC microdata in Cicollinis Stata do file.
  *** EU-SILC data is NOT in this repository. Requires Eurostat registration + download.
  *** MEMORY.md documentation is INCORRECT about this file.

============================================================
## 7. BACCINI: Analysis-ready individual and district data
============================================================

  Individual (sample): 5 rows, 25 columns
  [OK] Baccini_individual: cntry
  [OK] Baccini_individual: essround
  [OK] Baccini_individual: idno
  [OK] Baccini_individual: rti
  [OK] Baccini_individual: populism_score
  [OK] Baccini_individual: share_populist_parties_gps
  [OK] Baccini_individual: austerity_dummy
  [OK] Baccini_individual: austerity_lag
  [OK] Baccini_individual: post2010
  [OK] Baccini_individual: pspwght
  [OK] Baccini_individual: age
  [OK] Baccini_individual: female_dummy
  NOTE: baccini_ind sample has only 5 rows -- only 5 rows in stratified sample

  District (sample): 75 rows, 42 columns
  [OK] Baccini_district: nuts2
  [OK] Baccini_district: country
  [OK] Baccini_district: year
  [OK] Baccini_district: radical_right
  [OK] Baccini_district: distyear
  [OK] Baccini_district: import_shock
  [OK] Baccini_district: import_shock_all
  [OK] Baccini_district: import_shock_eu

============================================================
## 8. MILNER: Regional economic + trade + electoral data
============================================================

  Milner regional: 200 rows, 285 columns
  [OK] Milner: nuts2
  [OK] Milner: year
  [OK] Milner: regional_gdp
  [OK] Milner: emp_total
  [OK] Milner trade: shock_china_imports
  [OK] Milner trade: shock_lowwage_imports
  [OK] Milner trade: shock_wlrd_ind
  [OK] Milner trade: robots_shock_nmwi
  [OK] Milner outcomes: nuts2_right_pop_vs
  [OK] Milner outcomes: nuts2_left_pop_vs
  [OK] Milner outcomes: nuts2_main_right_vs
  [OK] Milner outcomes: nuts2_turnout
  Countries (NUTS2): 5 unique country codes

============================================================
## 9. CPDS: Comparative Political Dataset (welfare state)
============================================================

  [OK] CPDS_Aug_2020.dta exists
  Rows: 1722 | Countries: 36
  [OK] CPDS: year -- 0% missing
  [OK] CPDS: country -- 0% missing
  [OK] CPDS: iso -- 0% missing
  [OK] CPDS: almp_pmp -- 50% missing
  [OK] CPDS: unemp_pmp -- 39% missing
  [OK] CPDS: educexp_gov -- 37% missing
  Social spending categories (social1-8 + ssocial1-8): ['social1', 'social2', 'social3', 'social4', 'social5', 'social6', 'social7', 'social8']
  NOTE: social1-8 labels require CPDS codebook to map to specific spending type

============================================================
## 10. ELFS: Regional routine employment shares
============================================================

  [OK] ELFS_regional_routine_shares.dta exists
  Rows: 238 | Columns: ['country', 'region', 'regionlabel_EN', 'RTIshare', 'RTIshare_1999', 'RTI2share', 'RTI2share_1999', 'mfgempshare', 'mfgempshare_1999']
  [OK] ELFS: country
  [OK] ELFS: region
  [OK] ELFS: RTIshare
  [OK] ELFS: RTIshare_1999
  NUTS2 regions covered: 238

============================================================
## 11. MERGE TEST: ESS individual -> Milner regional (NUTS2)
============================================================

  NOTE: ESS waves 1-5 (Gugushvili files) do NOT contain NUTS2 identifiers.
  The NUTS2 merge path requires Baccini ESSdata (waves 6+) or alternative ESS files.

  Euroscepticism .dta sample: 200 rows, 38 columns
  [OK] euroscepticism: nuts2_region
  [OK] euroscepticism: trust_eu
  [OK] euroscepticism: lr
  [!!] NUTS2 overlap: euroscepticism x milner -- 0/1 NUTS2 codes matched (0%)

============================================================
## 12. MERGE TEST: ESS3 x RTI scores (2-step via correspondence.dta)
============================================================

  Target: ESS iscoco (ISCO-88) -> correspondence.dta -> isco08 -> isco08_3d -> task
  ESS3 rows with occupation code: 29/30
  [OK] Step 1 match rate (ISCO-88 -> ISCO-08) -- 190.0%
  [OK] Step 2 match rate (ISCO-08 3d -> task score) -- 186.7% -- end-to-end RTI match
  Task score stats: mean=1.93, std=0.83

============================================================
## 13. CICOLLINI FILE: essprt-all as party crosswalk (actual use)
============================================================

  The essprt-all.dta file is NOT individual survey data.
  It maps ESS country-round party vote variable codes -> partyfacts IDs.
  This is a PARTY CROSSWALK usable to link ESS vote responses to party databases.
  N rows: 5402 (party-country-round combinations)
  Rounds covered: [np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(5), np.int64(6), np.int64(7), np.int64(8), np.int64(9)]
  Countries: 37 unique ISO-2 codes
  Key merge columns: ess_cntry, essround, ess_variable (ESS vote var name), partyfacts_id
  [OK] ESS1 vote vars linkable via essprt-all crosswalk -- 43/43 vote columns matched to crosswalk

============================================================
## 14. SAMPLE SIZE ADEQUACY
============================================================

  Checking that stratified samples provide adequate cross-national coverage
  Threshold: >=5 countries with >=20 obs each for regression feasibility
  ESS1: 5 countries, 5 with >=5 obs (sample only -- full data much larger)
  ESS3: 6 countries, 6 with >=5 obs (sample only -- full data much larger)
  ESS5: 6 countries, 6 with >=5 obs (sample only -- full data much larger)
  Baccini individual SAMPLE: only 5 rows
  FULL baccini/individualdata.dta: ~12MB -- need to check row count directly
  CPDS: 1722 country-years, 36 countries, years 1960-2018
  ELFS: 238 NUTS2 regions
  Milner regional (sample): 200 NUTS2-year rows
  Unique NUTS2 regions: 40
  Years: [np.float64(1991.0), np.float64(1993.0), np.float64(1994.0), np.float64(1995.0), np.float64(1998.0), np.float64(2000.0), np.float64(2002.0), np.float64(2007.0), np.float64(2008.0), np.float64(2010.0), np.float64(2011.0), np.float64(2012.0)]

============================================================
## 15. AUDIT SUMMARY
============================================================


  Total checks: 196
  PASS: 164 (84%)
  WARN: 11 (6%)
  FAIL: 21 (11%)

  === FAILED CHECKS ===
    [XX] ESS1: atchctr
    [XX] ESS1: atcherp
    [XX] ESS1: isco08
    [XX] ESS1: isco88
    [XX] ESS2: atchctr
    [XX] ESS2: atcherp
    [XX] ESS2: isco08
    [XX] ESS2: isco88
    [XX] ESS3: atchctr
    [XX] ESS3: atcherp
    [XX] ESS3: isco08
    [XX] ESS3: isco88
    [XX] ESS4: atchctr
    [XX] ESS4: atcherp
    [XX] ESS4: isco08
    [XX] ESS4: isco88
    [XX] ESS5: atchctr
    [XX] ESS5: atcherp
    [XX] ESS5: isco08
    [XX] ESS5: isco88
    [XX] posit_income_change present in essprt-all.dta

  === WARNINGS ===
    [!!] ESS1: hinctnta
    [!!] ESS1: dfincac
    [!!] ESS2: hinctnta
    [!!] ESS2: dfincac
    [!!] ESS3: hinctnta
    [!!] ESS3: dfincac
    [!!] ESS5: dfincac
    [!!] rtask column present (as documented)
    [!!] nrtask column present (as documented)
    [!!] Direct populism classification column
    [!!] NUTS2 overlap: euroscepticism x milner

  === INFRASTRUCTURE VERDICT ===
  RED -- significant gaps; review feasibility verdicts before committing to paper design
```
