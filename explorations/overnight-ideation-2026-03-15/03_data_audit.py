# --- Overnight Ideation Data Audit ---
# Phase 3: Verify key variables exist, merges work, sample sizes adequate
# Input:  data/samples/stratified/  (relative to Research_Master root)
# Output: prints structured audit report (captured to 03_data_audit.md)
# Style:  sequential inline Python, section headers, inline asserts
# Date:   2026-03-15

import pandas as pd
import numpy as np
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# --- Config ---
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Research_Master/
SAMPLES = os.path.join(BASE, "data", "samples", "stratified")

results = {}  # collect pass/fail for summary

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check(label, condition, note=""):
    status = "PASS" if condition else "FAIL"
    icon = "✓" if condition else "✗"
    msg = f"  [{icon}] {label}"
    if note:
        msg += f" — {note}"
    print(msg)
    results[label] = status
    return condition

def cols(df, *names):
    """Return list of which columns are present."""
    return [c for c in names if c in df.columns]

# --- 1. File Presence ---
section("1. STRATIFIED SAMPLE FILE PRESENCE")

expected_files = {
    "ESS1":     "ESS1e06_7_strat25.csv",
    "ESS2":     "ESS2e03_6_strat25.csv",
    "ESS3":     "ESS3e03_7_strat30.csv",
    "ESS4":     "ESS4e04_6_strat30.csv",
    "ESS5":     "ESS5e03_5_strat30.csv",
    "ISSP2009": "ZA4950_ISSP2009_strat200.csv",
    "ISSP2010": "ZA5400_ISSP2010_strat200.csv",
    "ISSP2016": "ZA6770_ISSP2016_strat200.csv",
    "ISSP_steiner": "ZA7700_steiner_strat200.csv",
    "baccini_district": "baccini_district_level_strat75.csv",
    "baccini_individual": "baccini_individualdata_strat5.csv",
    "cicollini": "cicollini_essprt_all_strat45.csv",
    "euroscepticism": "euroscepticism_dta_strat200.csv",
    "milner_regional": "milner_merged_regional_strat200.csv",
}

loaded = {}
for key, fname in expected_files.items():
    fpath = os.path.join(SAMPLES, fname)
    exists = os.path.isfile(fpath)
    check(f"File present: {fname}", exists)
    if exists:
        try:
            for enc in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(fpath, encoding=enc, low_memory=False)
                    loaded[key] = df
                    break
                except UnicodeDecodeError:
                    continue
        except Exception as e:
            print(f"    [!] Could not load {fname}: {e}")

print(f"\n  Loaded {len(loaded)}/{len(expected_files)} sample files successfully")

# --- 2. ESS Core Variables ---
section("2. ESS CORE VARIABLES (checking waves 1–5)")

ess_keys = ['ESS1', 'ESS2', 'ESS3', 'ESS4', 'ESS5']
core_vars = ['cntry', 'essround', 'isco08', 'lrscale', 'trstprl',
             'stflife', 'hinctnta', 'imwbcnt', 'imueclt']
outcome_vars = ['vote']  # vote choice vars are country-specific prtvt* — checked separately

for key in ess_keys:
    if key not in loaded:
        print(f"  [!] {key} not loaded — skipping")
        continue
    df = loaded[key]
    present = cols(df, *core_vars)
    n = len(df)
    print(f"\n  {key}: {n} rows, {len(df.columns)} columns")
    for v in core_vars:
        in_df = v in df.columns
        if in_df:
            miss_pct = df[v].isna().mean() * 100
            check(f"  {key}: {v}", in_df, f"{miss_pct:.1f}% missing")
        else:
            check(f"  {key}: {v}", False, "NOT PRESENT")

    # Check for any prtvt vote variables
    vote_cols = [c for c in df.columns if c.startswith('prtvt')]
    check(f"  {key}: has prtvt* vote variables", len(vote_cols) > 0,
          f"{len(vote_cols)} vote variables: {vote_cols[:5]}")

# --- 3. ISCO-08 Task Score Merge ---
section("3. ISCO-08 TASK SCORE MERGE")

task_path = os.path.join(BASE, "data", "raw", "shared_isco_task_scores", "isco08_3d-task3.csv")
if not os.path.isfile(task_path):
    # Try aspiration_apprehension location (confirmed duplicate in data_dictionary)
    task_path = os.path.join(BASE, "data", "raw", "aspiration_apprehension", "isco08_3d-task3.csv")

task_exists = os.path.isfile(task_path)
check("Task score file present", task_exists, task_path)

if task_exists:
    tasks = pd.read_csv(task_path)
    print(f"  Task file: {len(tasks)} rows, columns: {list(tasks.columns)}")
    check("isco08_3d column present in task file", 'isco08_3d' in tasks.columns)

    # Test merge with ESS3 (has isco08 confirmed in CLAUDE.md)
    if 'ESS3' in loaded:
        df = loaded['ESS3'].copy()
        if 'isco08' in df.columns:
            # CRITICAL: truncate 4-digit to 3-digit per MEMORY.md
            df['isco08_3d'] = pd.to_numeric(df['isco08'], errors='coerce').astype('Int64') // 10
            pre_n = len(df)
            merged = df.merge(tasks, on='isco08_3d', how='left')
            post_n = len(merged)
            check("ESS3 × task scores merge preserves row count", pre_n == post_n,
                  f"{pre_n} → {post_n} rows")
            task_cols = [c for c in tasks.columns if c != 'isco08_3d']
            if task_cols:
                match_rate = merged[task_cols[0]].notna().mean() * 100
                check(f"Task score match rate ({task_cols[0]})", match_rate > 50,
                      f"{match_rate:.1f}% matched")
                print(f"  Task score columns available: {task_cols}")
        else:
            print("  [!] isco08 not present in ESS3 sample — cannot test merge")

# --- 4. Cicollini Positional Income ---
section("4. CICOLLINI: posit_income_change")

if 'cicollini' in loaded:
    df = loaded['cicollini']
    print(f"  Cicollini sample: {len(df)} rows, {len(df.columns)} columns")
    print(f"  Columns: {list(df.columns)}")
    check("posit_income_change present", 'posit_income_change' in df.columns,
          "CRITICAL — do not reconstruct")
    if 'posit_income_change' in df.columns:
        miss = df['posit_income_change'].isna().mean() * 100
        desc = df['posit_income_change'].describe()
        check("posit_income_change has variation", df['posit_income_change'].nunique() > 2,
              f"mean={desc['mean']:.3f}, std={desc['std']:.3f}, {miss:.1f}% missing")

    # Check for ESS linkage variables
    ess_link = cols(df, 'cntry', 'essround', 'idno')
    check("ESS linkage variables present", len(ess_link) >= 2,
          f"found: {ess_link}")

    # Check for party vote variables (for populist vote outcome)
    vote_cols = [c for c in df.columns if 'vote' in c.lower() or c.startswith('prtvt')]
    print(f"  Vote-related columns: {vote_cols[:10]}")

# --- 5. Baccini Individual-Level Data ---
section("5. BACCINI: individual and district level")

if 'baccini_individual' in loaded:
    df = loaded['baccini_individual']
    print(f"  Baccini individual: {len(df)} rows, {len(df.columns)} columns")
    key_baccini_ind = ['cntry', 'essround', 'lrscale', 'trstprl']
    for v in key_baccini_ind:
        in_df = v in df.columns
        check(f"Baccini_individual: {v}", in_df)
    # Check for austerity variable
    austerity_cols = [c for c in df.columns if 'auster' in c.lower()]
    check("Baccini austerity measure present", len(austerity_cols) > 0,
          f"found: {austerity_cols}")
    populism_cols = [c for c in df.columns if 'popul' in c.lower() or 'gps' in c.lower()]
    check("Baccini populism/GPS measure present", len(populism_cols) > 0,
          f"found: {populism_cols[:5]}")

if 'baccini_district' in loaded:
    df = loaded['baccini_district']
    print(f"\n  Baccini district: {len(df)} rows, {len(df.columns)} columns")
    district_key = ['nuts2', 'nuts3']
    for v in district_key:
        in_df = v in df.columns
        check(f"Baccini_district: {v}", in_df)
    farright_cols = [c for c in df.columns if 'right' in c.lower() or 'farright' in c.lower() or 'er_vote' in c.lower()]
    check("Far-right vote share present", len(farright_cols) > 0,
          f"found: {farright_cols[:5]}")

# --- 6. Milner Regional Data ---
section("6. MILNER: regional trade + economic data")

if 'milner_regional' in loaded:
    df = loaded['milner_regional']
    print(f"  Milner regional: {len(df)} rows, {len(df.columns)} columns")
    milner_key = ['nuts2', 'cntry']
    for v in milner_key:
        in_df = v in df.columns
        check(f"Milner: {v}", in_df)
    trade_cols = [c for c in df.columns if 'trade' in c.lower() or 'china' in c.lower() or 'import' in c.lower()]
    check("Trade exposure variable present", len(trade_cols) > 0,
          f"found: {trade_cols[:5]}")

# --- 7. ESS Populist Crosswalk ---
section("7. ESS POPULIST CROSSWALK (Langenkamp)")

crosswalk_path = os.path.join(BASE, "data", "raw", "langenkamp_2022", "ess_populist_crosswalk.csv")
cw_exists = os.path.isfile(crosswalk_path)
check("Populist crosswalk file present", cw_exists)

if cw_exists:
    cw = pd.read_csv(crosswalk_path)
    print(f"  Crosswalk: {len(cw)} rows, columns: {list(cw.columns)}")
    check("cntry in crosswalk", 'cntry' in cw.columns)
    check("essround in crosswalk", 'essround' in cw.columns)
    n_countries = cw['cntry'].nunique() if 'cntry' in cw.columns else 0
    n_rounds = cw['essround'].nunique() if 'essround' in cw.columns else 0
    print(f"  Countries: {n_countries}, ESS rounds: {n_rounds}")
    populism_cols = [c for c in cw.columns if 'popul' in c.lower() or 'rrp' in c.lower() or 'far' in c.lower()]
    check("Populism classification columns present", len(populism_cols) > 0,
          f"found: {populism_cols}")

# --- 8. Aspiration/Apprehension Data ---
section("8. ASPIRATION/APPREHENSION DATA")

asp_path = os.path.join(BASE, "data", "raw", "aspiration_apprehension", "aspiration_apprehension_data.csv")
asp_exists = os.path.isfile(asp_path)
check("Aspiration/apprehension data present", asp_exists)

if asp_exists:
    asp = pd.read_csv(asp_path, low_memory=False)
    print(f"  Aspiration data: {len(asp)} rows, {len(asp.columns)} columns")
    # Look for the key aspiration/apprehension measures
    asp_cols = [c for c in asp.columns if any(x in c.lower() for x in
                ['aspir', 'appreh', 'expect', 'prosp', 'futur'])]
    print(f"  Aspiration/apprehension proxies: {asp_cols[:10]}")
    check("Has prospective/expectation variables", len(asp_cols) > 0,
          f"{len(asp_cols)} found")

# --- 9. Key Merge Test: ESS3 + Cicollini ---
section("9. MERGE TEST: ESS3 × Cicollini (positional income)")

if 'ESS3' in loaded and 'cicollini' in loaded:
    ess = loaded['ESS3'].copy()
    cic = loaded['cicollini'].copy()

    # Find common key columns
    ess_cols_lower = {c.lower(): c for c in ess.columns}
    cic_cols_lower = {c.lower(): c for c in cic.columns}

    common_lower = set(ess_cols_lower.keys()) & set(cic_cols_lower.keys())
    print(f"  Common columns (case-insensitive): {sorted(common_lower)[:20]}")

    # Try merge on idno + cntry + essround if available
    potential_keys = []
    for k in ['idno', 'cntry', 'essround']:
        if k in ess.columns and k in cic.columns:
            potential_keys.append(k)

    check("Merge key variables exist in both", len(potential_keys) >= 1,
          f"usable keys: {potential_keys}")

    if potential_keys:
        try:
            test_merge = ess.merge(cic[potential_keys + (['posit_income_change']
                                   if 'posit_income_change' in cic.columns else [])],
                                   on=potential_keys, how='left')
            match_rate = 0
            if 'posit_income_change' in test_merge.columns:
                match_rate = test_merge['posit_income_change'].notna().mean() * 100
                check("ESS3 × Cicollini merge yields posit_income_change",
                      match_rate > 0, f"{match_rate:.1f}% matched")
        except Exception as e:
            print(f"  [!] Merge test failed: {e}")

# --- 10. Summary ---
section("10. AUDIT SUMMARY")

n_pass = sum(1 for v in results.values() if v == "PASS")
n_fail = sum(1 for v in results.values() if v == "FAIL")
n_total = len(results)

print(f"\n  Total checks: {n_total}")
print(f"  PASS: {n_pass} ({n_pass/n_total*100:.0f}%)")
print(f"  FAIL: {n_fail} ({n_fail/n_total*100:.0f}%)")

if n_fail > 0:
    print(f"\n  FAILED CHECKS:")
    for label, status in results.items():
        if status == "FAIL":
            print(f"    ✗ {label}")

print(f"\n  Infrastructure verdict: ", end="")
if n_fail == 0:
    print("GREEN — all critical variables present, core merges viable")
elif n_fail <= 3:
    print("AMBER — minor gaps, core programme feasible")
else:
    print("RED — significant gaps, review before committing to paper design")
