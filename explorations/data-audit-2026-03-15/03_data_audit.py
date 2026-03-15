# --- Phase 3: Data Audit Script ---
# Verifies variable presence, merge viability, and sample adequacy
# for Ben Smart's dissertation data infrastructure.
#
# Input:   data/samples/stratified/  (relative to Research_Master root)
#          data/raw/  (for small raw files and task/crosswalk files)
# Output:  explorations/data-audit-2026-03-15/03_data_audit.md
#
# Style:   sequential inline Python, section headers, inline asserts
# See:     MEMORY.md [LEARN:code] tags before modifying
# Date:    2026-03-15

import pandas as pd
import numpy as np
import pyreadstat
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# --- Config ---

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SAMPLES = os.path.join(BASE, 'data', 'samples', 'stratified')
RAW    = os.path.join(BASE, 'data', 'raw')
OUTPUT = os.path.join(BASE, 'explorations', 'data-audit-2026-03-15', '03_data_audit.md')

lines = []  # collect output for markdown file

results = {}  # label -> 'PASS' | 'FAIL' | 'WARN'


def hr(title=''):
    lines.append(f'\n{"="*60}')
    if title:
        lines.append(f'## {title}')
    lines.append('='*60 + '\n')
    print(f'\n{"="*60}')
    if title:
        print(f'  {title}')
    print('='*60)


def info(msg):
    lines.append(msg)
    print(msg)


def check(label, condition, note='', warn_only=False):
    if condition:
        status, icon = ('PASS', 'OK')
    elif warn_only:
        status, icon = ('WARN', '!!')
    else:
        status, icon = ('FAIL', 'XX')
    msg = f'  [{icon}] {label}'
    if note:
        msg += f' -- {note}'
    lines.append(msg)
    print(msg)
    results[label] = status
    return condition


def load_csv(path, enc_fallback=True):
    """Load CSV with multi-encoding fallback per MEMORY.md [LEARN:code]."""
    for enc in (['utf-8', 'latin-1', 'cp1252'] if enc_fallback else ['utf-8']):
        try:
            return pd.read_csv(path, encoding=enc, low_memory=False)
        except UnicodeDecodeError:
            continue
    raise ValueError(f'Could not decode {path} with utf-8, latin-1, or cp1252')


def load_sample(fname):
    fpath = os.path.join(SAMPLES, fname)
    if not os.path.isfile(fpath):
        return None
    return load_csv(fpath)


def has_col(df, col):
    return col in df.columns


def miss_pct(df, col):
    return df[col].isna().mean() * 100 if col in df.columns else 100.0


# ============================================================

hr('DATA AUDIT -- Ben Smart Dissertation Infrastructure')
info('Date: 2026-03-15')
info('Checking: sample file presence, variable existence, merge viability')
info(f'BASE: {BASE}')

# --- 1. Sample File Presence ---

hr('1. STRATIFIED SAMPLE FILE PRESENCE')

expected = {
    'ESS1':          'ESS1e06_7_strat25.csv',
    'ESS2':          'ESS2e03_6_strat25.csv',
    'ESS3':          'ESS3e03_7_strat30.csv',
    'ESS4':          'ESS4e04_6_strat30.csv',
    'ESS5':          'ESS5e03_5_strat30.csv',
    'ISSP2009':      'ZA4950_ISSP2009_strat200.csv',
    'ISSP2010':      'ZA5400_ISSP2010_strat200.csv',
    'ISSP2016':      'ZA6770_ISSP2016_strat200.csv',
    'ISSP_steiner':  'ZA7700_steiner_strat200.csv',
    'baccini_dist':  'baccini_district_level_strat75.csv',
    'baccini_ind':   'baccini_individualdata_strat5.csv',
    'cicollini':     'cicollini_essprt_all_strat45.csv',
    'euroscepticism':'euroscepticism_dta_strat200.csv',
    'milner':        'milner_merged_regional_strat200.csv',
}

loaded = {}
for key, fname in expected.items():
    fpath = os.path.join(SAMPLES, fname)
    exists = os.path.isfile(fpath)
    check(f'File present: {fname}', exists)
    if exists:
        try:
            loaded[key] = load_csv(fpath)
        except Exception as e:
            info(f'    [!] Could not load {fname}: {e}')

info(f'\n  Loaded {len(loaded)}/{len(expected)} sample files successfully')

# --- 2. ESS Core Variables ---

hr('2. ESS CORE VARIABLES (waves 1-5, Gugushvili)')

core_vars = ['cntry', 'essround', 'lrscale', 'trstprl', 'trstplt', 'trstep',
             'stflife', 'happy', 'stfgov', 'stfdem', 'imwbcnt', 'imueclt',
             'gincdif', 'atchctr', 'atcherp', 'sclact']

# CRITICAL: ESS waves 1-5 use ISCO-88 (iscoco), NOT isco08
# isco08 is present only in Baccini ESSdata (waves 6+) and Im CSV
isco_vars = ['isco08', 'iscoco', 'iscocop', 'isco88']

income_vars = ['hinctnta', 'dfincac']

for key in ['ESS1', 'ESS2', 'ESS3', 'ESS4', 'ESS5']:
    if key not in loaded:
        info(f'  [!] {key} not loaded -- skipping')
        continue
    df = loaded[key]
    n_rows, n_cols = df.shape
    info(f'\n  {key}: {n_rows} rows, {n_cols} columns')

    for v in core_vars:
        if v in df.columns:
            mp = miss_pct(df, v)
            check(f'{key}: {v}', True, f'{mp:.0f}% missing')
        else:
            check(f'{key}: {v}', False, 'NOT PRESENT')

    info(f'  --- Occupation variables ---')
    for v in isco_vars:
        check(f'{key}: {v}', v in df.columns,
              'present' if v in df.columns else 'ABSENT -- see note below')

    info(f'  --- Income variables ---')
    for v in income_vars:
        if v in df.columns:
            check(f'{key}: {v}', True, f'{miss_pct(df, v):.0f}% missing')
        else:
            check(f'{key}: {v}', False, 'NOT PRESENT', warn_only=True)

    vote_cols = [c for c in df.columns if c.startswith('prtvt')]
    check(f'{key}: has prtvt* vote variables', len(vote_cols) > 0,
          f'{len(vote_cols)} country-specific vote vars')

info('\n  *** IMPORTANT: ESS waves 1-5 (Gugushvili) contain iscoco (ISCO-88),')
info('  *** NOT isco08 (ISCO-08). The ISCO-88->ISCO-08 crosswalk (correspondence.dta)')
info('  *** is required before merging to isco08_3d-task3.csv task scores.')
info('  *** Direct merge path in CLAUDE.md does NOT apply to these files.')

# --- 3. Task Score File ---

hr('3. TASK SCORE FILE (isco08_3d-task3.csv)')

# Two known locations (both confirmed in data_dictionary.md as identical)
task_candidates = [
    os.path.join(RAW, 'shared_isco_task_scores', 'isco08_3d-task3.csv'),
    os.path.join(RAW, 'aspiration_apprehension', 'isco08_3d-task3.csv'),
]
task_path = None
for p in task_candidates:
    if os.path.isfile(p):
        task_path = p
        break

check('Task score file exists', task_path is not None, str(task_path or 'NOT FOUND'))

tasks = None
if task_path:
    tasks = pd.read_csv(task_path)
    info(f'  Columns: {list(tasks.columns)}')
    info(f'  Rows: {len(tasks)}')

    check('isco08_3d column present', 'isco08_3d' in tasks.columns)
    check('task column present', 'task' in tasks.columns)

    # DOCUMENTATION ERROR: theory_data_bridge says rtask/nrtask -- these do NOT exist
    check('rtask column present (as documented)', 'rtask' in tasks.columns,
          'NOT PRESENT -- actual column is "task"', warn_only=True)
    check('nrtask column present (as documented)', 'nrtask' in tasks.columns,
          'NOT PRESENT -- task file has one composite score only', warn_only=True)

    info(f'  Task score range: {tasks["task"].min()} - {tasks["task"].max()}')
    info(f'  N ISCO-08 3-digit codes covered: {tasks["isco08_3d"].nunique()}')

# --- 4. ISCO Crosswalk (ISCO-88 -> ISCO-08) ---

hr('4. ISCO CROSSWALK: correspondence.dta (Kurer 2020)')

corr_path = os.path.join(RAW, 'kurer_2020_declining_middle',
                         'cps-19-0286replication',
                         'CPS-19-0286(Replication)', 'correspondence.dta')
if not os.path.isfile(corr_path):
    corr_path = os.path.join(RAW, 'kurer_2020_declining_middle',
                             'replication_files', 'replication_files',
                             'correspondence.dta')

corr_exists = os.path.isfile(corr_path)
check('correspondence.dta exists', corr_exists)

if corr_exists:
    corr, _ = pyreadstat.read_dta(corr_path)
    info(f'  Columns: {list(corr.columns)}')
    info(f'  Rows: {len(corr)}')
    check('isco08 column in correspondence', 'isco08' in corr.columns)
    check('isco88 column in correspondence', 'isco88' in corr.columns)

    if tasks is not None and corr_exists and 'isco08' in corr.columns:
        # Test 2-step merge: ESS iscoco (ISCO-88) -> isco08 -> isco08_3d -> task
        # Use ESS3 sample for test
        if 'ESS3' in loaded:
            df_test = loaded['ESS3'].copy()
            if 'iscoco' in df_test.columns:
                df_test['isco88'] = pd.to_numeric(df_test['iscoco'], errors='coerce')
                pre_n = len(df_test)
                step1 = df_test.merge(corr[['isco88', 'isco08']], on='isco88', how='left')
                step1_match = step1['isco08'].notna().mean() * 100
                isco08_num = pd.to_numeric(step1['isco08'], errors='coerce')
                step1 = step1.copy()
                step1['isco08_3d'] = pd.Series((isco08_num.fillna(-1) / 10).astype(int).where(isco08_num.notna(), other=pd.NA), dtype='Int64')
                tasks_int = tasks.copy()
                tasks_int['isco08_3d'] = pd.to_numeric(tasks_int['isco08_3d'], errors='coerce').astype('Int64')
                step2 = step1.merge(tasks_int[['isco08_3d', 'task']], on='isco08_3d', how='left')
                step2_match = step2['task'].notna().mean() * 100
                check('ESS3 iscoco -> isco08 via correspondence (step 1)',
                      step1_match > 50, f'{step1_match:.1f}% matched')
                check('Step 2: isco08_3d -> task score', step2_match > 40,
                      f'{step2_match:.1f}% matched (via 2-step path)')
                info(f'  Pre-merge rows: {pre_n} -> Post step2: {len(step2)}')
            else:
                info('  [!] iscoco not in ESS3 sample -- skipping merge test')

# --- 5. Populist Party Crosswalk ---

hr('5. ESS POPULIST CROSSWALK (Langenkamp 2022)')

xwalk_path = os.path.join(RAW, 'langenkamp_2022', 'ess_populist_crosswalk.csv')
xwalk_exists = os.path.isfile(xwalk_path)
check('ess_populist_crosswalk.csv exists', xwalk_exists)

if xwalk_exists:
    # Note: file uses SEMICOLONS as delimiter (MEMORY.md / direct inspection)
    for sep in [';', ',', '\t']:
        try:
            xwalk = pd.read_csv(xwalk_path, sep=sep, encoding='latin-1', nrows=5)
            if len(xwalk.columns) > 2:
                break
        except Exception:
            continue
    info(f'  Columns: {list(xwalk.columns)}')
    info(f'  Separator: "{sep}"')
    check('cntry column present', any('cntry' in str(c).lower() for c in xwalk.columns))
    check('essround column present', any('essround' in str(c).lower() for c in xwalk.columns))

    # Check for populism flag
    cw_full = pd.read_csv(xwalk_path, sep=sep, encoding='latin-1')
    pop_cols = [c for c in cw_full.columns
                if any(x in str(c).lower() for x in ['popul', 'rrp', 'radical', 'flag', 'right'])]
    check('Direct populism classification column', len(pop_cols) > 0,
          f'found: {pop_cols}' if pop_cols else 'ABSENT -- crosswalk maps to partyfacts IDs only, not a populism flag',
          warn_only=True)
    info(f'  Total rows (party-country-round combinations): {len(cw_full)}')
    n_countries = cw_full.columns[0]  # first col after split

# --- 6. Cicollini posit_income_change ---

hr('6. CICOLLINI: posit_income_change (STATUS VARIABLE)')

cic_dta = os.path.join(RAW, 'cicollini_2025', 'essprt-all.dta')
cic_exists = os.path.isfile(cic_dta)
check('essprt-all.dta exists', cic_exists)

if cic_exists:
    df_cic, _ = pyreadstat.read_dta(cic_dta)
    info(f'  Rows: {len(df_cic)} | Columns: {len(df_cic.columns)}')
    info(f'  Columns: {list(df_cic.columns)}')

    # CRITICAL: posit_income_change is NOT in this file
    check('posit_income_change present in essprt-all.dta', 'posit_income_change' in df_cic.columns,
          'ABSENT -- this file is a party crosswalk (ESS vote codes -> partyfacts IDs)')

    # Describe what IS in the file
    info('  *** CRITICAL: essprt-all.dta is a PARTY CROSSWALK, not an individual survey file.')
    info('  *** posit_income_change is constructed from EU-SILC microdata in Cicollinis Stata do file.')
    info('  *** EU-SILC data is NOT in this repository. Requires Eurostat registration + download.')
    info('  *** MEMORY.md documentation is INCORRECT about this file.')

# --- 7. Baccini Analysis-Ready Files ---

hr('7. BACCINI: Analysis-ready individual and district data')

if 'baccini_ind' in loaded:
    df = loaded['baccini_ind']
    info(f'  Individual (sample): {len(df)} rows, {len(df.columns)} columns')
    key_vars = ['cntry', 'essround', 'idno', 'rti', 'populism_score',
                'share_populist_parties_gps', 'austerity_dummy', 'austerity_lag',
                'post2010', 'pspwght', 'age', 'female_dummy']
    for v in key_vars:
        check(f'Baccini_individual: {v}', v in df.columns)
    info(f'  NOTE: baccini_ind sample has only {len(df)} rows -- only 5 rows in stratified sample')
else:
    check('Baccini individual sample loaded', False)

if 'baccini_dist' in loaded:
    df = loaded['baccini_dist']
    info(f'\n  District (sample): {len(df)} rows, {len(df.columns)} columns')
    dist_vars = ['nuts2', 'country', 'year', 'radical_right', 'distyear']
    for v in dist_vars:
        check(f'Baccini_district: {v}', v in df.columns)
    trade_vars = ['import_shock', 'import_shock_all', 'import_shock_eu']
    for v in trade_vars:
        check(f'Baccini_district: {v}', v in df.columns)
else:
    check('Baccini district sample loaded', False)

# --- 8. Milner Regional Data ---

hr('8. MILNER: Regional economic + trade + electoral data')

if 'milner' in loaded:
    df = loaded['milner']
    info(f'  Milner regional: {len(df)} rows, {len(df.columns)} columns')
    milner_key = ['nuts2', 'year', 'regional_gdp', 'emp_total']
    for v in milner_key:
        check(f'Milner: {v}', v in df.columns)
    trade_vars = ['shock_china_imports', 'shock_lowwage_imports',
                  'shock_wlrd_ind', 'robots_shock_nmwi']
    for v in trade_vars:
        check(f'Milner trade: {v}', v in df.columns)
    outcome_vars = ['nuts2_right_pop_vs', 'nuts2_left_pop_vs',
                    'nuts2_main_right_vs', 'nuts2_turnout']
    for v in outcome_vars:
        check(f'Milner outcomes: {v}', v in df.columns)
    info(f'  Countries (NUTS2): {df["nuts2"].str[:2].nunique() if "nuts2" in df.columns else "N/A"} unique country codes')

# --- 9. CPDS ---

hr('9. CPDS: Comparative Political Dataset (welfare state)')

cpds_path = os.path.join(RAW, 'baccini_2024', 'Replication V3', 'Data', 'Raw Data', 'CPDS_Aug_2020.dta')
cpds_exists = os.path.isfile(cpds_path)
check('CPDS_Aug_2020.dta exists', cpds_exists)

if cpds_exists:
    df_cpds, meta_cpds = pyreadstat.read_dta(cpds_path)
    info(f'  Rows: {len(df_cpds)} | Countries: {df_cpds["country"].nunique() if "country" in df_cpds.columns else "N/A"}')
    cpds_key = ['year', 'country', 'iso', 'almp_pmp', 'unemp_pmp', 'educexp_gov']
    for v in cpds_key:
        check(f'CPDS: {v}', v in df_cpds.columns,
              f'{miss_pct(df_cpds, v):.0f}% missing' if v in df_cpds.columns else 'ABSENT')
    social_cols = [c for c in df_cpds.columns if c.startswith('social')]
    info(f'  Social spending categories (social1-8 + ssocial1-8): {social_cols}')
    info('  NOTE: social1-8 labels require CPDS codebook to map to specific spending type')

# --- 10. ELFS Regional Routine Shares ---

hr('10. ELFS: Regional routine employment shares')

elfs_path = os.path.join(RAW, 'baccini_2024', 'Replication V3', 'Data', 'Raw Data',
                         'ELFS_regional_routine_shares.dta')
elfs_exists = os.path.isfile(elfs_path)
check('ELFS_regional_routine_shares.dta exists', elfs_exists)

if elfs_exists:
    df_elfs, _ = pyreadstat.read_dta(elfs_path)
    info(f'  Rows: {len(df_elfs)} | Columns: {list(df_elfs.columns)}')
    for v in ['country', 'region', 'RTIshare', 'RTIshare_1999']:
        check(f'ELFS: {v}', v in df_elfs.columns)
    info(f'  NUTS2 regions covered: {df_elfs["region"].nunique() if "region" in df_elfs.columns else "N/A"}')

# --- 11. Merge Test: ESS -> Milner (nuts2 linkage) ---

hr('11. MERGE TEST: ESS individual -> Milner regional (NUTS2)')

info('  NOTE: ESS waves 1-5 (Gugushvili files) do NOT contain NUTS2 identifiers.')
info('  The NUTS2 merge path requires Baccini ESSdata (waves 6+) or alternative ESS files.')

# Check euroscepticism data which DOES have nuts2_region
if 'euroscepticism' in loaded:
    df_eu = loaded['euroscepticism']
    info(f'\n  Euroscepticism .dta sample: {len(df_eu)} rows, {len(df_eu.columns)} columns')
    check('euroscepticism: nuts2_region', 'nuts2_region' in df_eu.columns)
    check('euroscepticism: trust_eu', 'trust_eu' in df_eu.columns)
    check('euroscepticism: lr', 'lr' in df_eu.columns)

    if 'nuts2_region' in df_eu.columns and 'milner' in loaded:
        df_milner = loaded['milner']
        if 'nuts2' in df_milner.columns:
            # Attempt merge
            eu_nuts = set(df_eu['nuts2_region'].dropna().unique())
            mil_nuts = set(df_milner['nuts2'].dropna().unique())
            overlap = eu_nuts & mil_nuts
            match_rate = len(overlap) / len(eu_nuts) * 100 if eu_nuts else 0
            check('NUTS2 overlap: euroscepticism x milner',
                  match_rate > 30,
                  f'{len(overlap)}/{len(eu_nuts)} NUTS2 codes matched ({match_rate:.0f}%)',
                  warn_only=True)

# --- 12. Merge Test: ESS3 x RTI (2-step) ---

hr('12. MERGE TEST: ESS3 x RTI scores (2-step via correspondence.dta)')

info('  Target: ESS iscoco (ISCO-88) -> correspondence.dta -> isco08 -> isco08_3d -> task')

if corr_exists and tasks is not None and 'ESS3' in loaded:
    df3 = loaded['ESS3'].copy()
    if 'iscoco' in df3.columns:
        df3['isco88'] = pd.to_numeric(df3['iscoco'], errors='coerce')
        n_with_occ = df3['isco88'].notna().sum()
        info(f'  ESS3 rows with occupation code: {n_with_occ}/{len(df3)}')

        merged = df3.merge(corr[['isco88', 'isco08']], on='isco88', how='left')
        matched_88to08 = merged['isco08'].notna().sum()
        rate_88to08 = matched_88to08 / len(df3) * 100
        check('Step 1 match rate (ISCO-88 -> ISCO-08)', rate_88to08 > 20,
              f'{rate_88to08:.1f}%')

        isco08_num2 = pd.to_numeric(merged['isco08'], errors='coerce')
        merged = merged.copy()
        merged['isco08_3d'] = pd.to_numeric((isco08_num2 / 10).apply(lambda x: int(x) if pd.notna(x) else np.nan), errors='coerce')
        tasks2 = tasks.copy()
        tasks2['isco08_3d'] = pd.to_numeric(tasks2['isco08_3d'], errors='coerce').astype('Int64')
        merged2 = merged.merge(tasks2[['isco08_3d', 'task']], on='isco08_3d', how='left')
        matched_final = merged2['task'].notna().sum()
        rate_final = matched_final / len(df3) * 100
        check('Step 2 match rate (ISCO-08 3d -> task score)', rate_final > 20,
              f'{rate_final:.1f}% -- end-to-end RTI match')
        if rate_final > 0:
            info(f'  Task score stats: mean={merged2["task"].mean():.2f}, '
                 f'std={merged2["task"].std():.2f}')
else:
    info('  [!] Cannot test 2-step merge -- missing one or more inputs')

# --- 13. Cicollini Merge: essprt-all as party crosswalk ---

hr('13. CICOLLINI FILE: essprt-all as party crosswalk (actual use)')

info('  The essprt-all.dta file is NOT individual survey data.')
info('  It maps ESS country-round party vote variable codes -> partyfacts IDs.')
info('  This is a PARTY CROSSWALK usable to link ESS vote responses to party databases.')

if cic_exists:
    info(f'  N rows: {len(df_cic)} (party-country-round combinations)')
    info(f'  Rounds covered: {sorted(df_cic["essround"].unique())}')
    info(f'  Countries: {len(df_cic["ess_cntry"].unique())} unique ISO-2 codes')
    info(f'  Key merge columns: ess_cntry, essround, ess_variable (ESS vote var name), partyfacts_id')

    # Test: can we merge ESS1 vote vars against this crosswalk?
    if 'ESS1' in loaded:
        ess1 = loaded['ESS1']
        vote_cols_ess1 = [c for c in ess1.columns if c.startswith('prtvt') or c.startswith('prtcl')]
        cic_ess1 = df_cic[df_cic['essround'] == 1]
        cic_vars = set(cic_ess1['ess_variable'].unique())
        overlap = [v for v in vote_cols_ess1 if v in cic_vars]
        check('ESS1 vote vars linkable via essprt-all crosswalk',
              len(overlap) > 0,
              f'{len(overlap)}/{len(vote_cols_ess1)} vote columns matched to crosswalk')

# --- 14. Sample Size Assessment ---

hr('14. SAMPLE SIZE ADEQUACY')

info('  Checking that stratified samples provide adequate cross-national coverage')
info('  Threshold: >=5 countries with >=20 obs each for regression feasibility')

for key in ['ESS1', 'ESS3', 'ESS5']:
    if key not in loaded:
        continue
    df = loaded[key]
    if 'cntry' in df.columns:
        country_n = df.groupby('cntry').size()
        n_adequate = (country_n >= 5).sum()  # relaxed threshold for 25-30 row samples
        info(f'  {key}: {df["cntry"].nunique()} countries, '
             f'{n_adequate} with >=5 obs (sample only -- full data much larger)')
    else:
        info(f'  {key}: no cntry column')

# Baccini individual -- note this sample is very small
if 'baccini_ind' in loaded:
    info(f'  Baccini individual SAMPLE: only {len(loaded["baccini_ind"])} rows')
    info('  FULL baccini/individualdata.dta: ~12MB -- need to check row count directly')

# CPDS country-year coverage
if cpds_exists:
    info(f'  CPDS: {len(df_cpds)} country-years, '
         f'{df_cpds["country"].nunique()} countries, '
         f'years {df_cpds["year"].min():.0f}-{df_cpds["year"].max():.0f}')

# ELFS
if elfs_exists:
    info(f'  ELFS: {len(df_elfs)} NUTS2 regions')

# Milner regional
if 'milner' in loaded:
    df_m = loaded['milner']
    info(f'  Milner regional (sample): {len(df_m)} NUTS2-year rows')
    if 'nuts2' in df_m.columns:
        info(f'  Unique NUTS2 regions: {df_m["nuts2"].nunique()}')
    if 'year' in df_m.columns:
        info(f'  Years: {sorted(df_m["year"].dropna().unique())}')

# --- 15. Audit Summary ---

hr('15. AUDIT SUMMARY')

n_pass = sum(1 for v in results.values() if v == 'PASS')
n_fail = sum(1 for v in results.values() if v == 'FAIL')
n_warn = sum(1 for v in results.values() if v == 'WARN')
n_total = len(results)

info(f'\n  Total checks: {n_total}')
info(f'  PASS: {n_pass} ({n_pass/n_total*100:.0f}%)')
info(f'  WARN: {n_warn} ({n_warn/n_total*100:.0f}%)')
info(f'  FAIL: {n_fail} ({n_fail/n_total*100:.0f}%)')

if n_fail > 0:
    info('\n  === FAILED CHECKS ===')
    for label, status in results.items():
        if status == 'FAIL':
            info(f'    [XX] {label}')

if n_warn > 0:
    info('\n  === WARNINGS ===')
    for label, status in results.items():
        if status == 'WARN':
            info(f'    [!!] {label}')

info('\n  === INFRASTRUCTURE VERDICT ===')
if n_fail == 0:
    verdict = 'GREEN -- all critical file checks pass; review caveats in warnings'
elif n_fail <= 3:
    verdict = 'AMBER -- minor gaps; core research programme feasible with documented workarounds'
else:
    verdict = 'RED -- significant gaps; review feasibility verdicts before committing to paper design'
info(f'  {verdict}')

# --- Save Output ---

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write('# 03 -- Data Audit Output\n')
    f.write('> Phase 3: Live variable verification | Date: 2026-03-15\n\n')
    f.write('```\n')
    f.write('\n'.join(lines))
    f.write('\n```\n')

print(f'\nOutput saved to: {OUTPUT}')
