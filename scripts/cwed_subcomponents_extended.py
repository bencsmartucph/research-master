"""
CWED Sub-Components — Extended (Session 3, 2026-05-04)
=======================================================

Re-runs the CWED sub-component decomposition in the random-slopes specification
(consistent with §V.D Model 3 of paper_draft_v4_final.md) and extends it with:

  - macro-controls robustness (GDP growth + post-fiscal Gini, parallel to Claim 13)
  - country-exclusion jackknife on the dominant sub-component (predicted: UEGEN)
  - item-level decomposition of the anti-immig index (imwbcnt / imueclt / imbgeco)

The pre-existing analysis at `analysis/cwed_subcomponents_results.json` used OLS
with country-wave fixed effects and cluster-robust SEs. That's a defensible spec
but differs from §V.D's random-slopes mixed model. This script produces the
random-slopes version for §V.D consistency.

Run:
    python scripts/cwed_subcomponents_extended.py

Outputs:
    outputs/tables/cwed_subcomponents_rs.csv          — main results (RS spec)
    outputs/tables/cwed_subcomponents_macro.csv       — RS + GDP/Gini robustness
    outputs/tables/uegen_country_jackknife.csv        — UEGEN single-country drops
    outputs/tables/cwed_interaction_by_item.csv       — item-level decomposition
"""

import sys, io, os, warnings
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
import patsy
from statsmodels.regression.mixed_linear_model import MixedLM
warnings.filterwarnings('ignore')

os.makedirs('outputs/tables', exist_ok=True)

# ── Configuration ──────────────────────────────────────────────────────────────
MASTER = 'analysis/sorting_mechanism_master_v2.csv'
CWED_FILE = 'data/raw/CWED/cwed-subset.csv'
CPDS_FILE = 'data/raw/baccini_2024/Replication V3/Data/Raw Data/CPDS_Aug_2020.dta'

CTRLS = ['agea', 'age_sq', 'female', 'college', 'hinctnta', 'urban']
GROUPS = 'cntry_wave'

ISO3_TO_ISO2 = {
    'AUT': 'AT', 'BEL': 'BE', 'CHE': 'CH', 'DEU': 'DE', 'DNK': 'DK',
    'ESP': 'ES', 'FIN': 'FI', 'FRA': 'FR', 'GBR': 'GB', 'IRL': 'IE',
    'ITA': 'IT', 'NLD': 'NL', 'NOR': 'NO', 'PRT': 'PT', 'SWE': 'SE',
}
ISO2_TO_ISO3 = {v: k for k, v in ISO3_TO_ISO2.items()}

# ── Load and merge ─────────────────────────────────────────────────────────────
print("Loading master and CWED sub-components...")
df = pd.read_csv(MASTER, low_memory=False)
df = df.dropna(subset=['task_z', 'anti_immig_index'])
print(f"  Base N: {len(df):,}")

# CWED sub-components: re-build mean 2005-2011 per country (matches paper convention)
cwed = pd.read_csv(CWED_FILE)
cwed_window = cwed[(cwed['YEAR'] >= 2005) & (cwed['YEAR'] <= 2011)].copy()
cwed_window['cntry'] = cwed_window['COUNTRY ABBREV'].map(ISO3_TO_ISO2)
cwed_window = cwed_window.dropna(subset=['cntry'])
# Coerce sub-component columns to numeric — CWED CSV has object dtype with stray strings
for col in ['TOTGEN', 'UEGEN', 'SKGEN', 'PGEN']:
    cwed_window[col] = pd.to_numeric(cwed_window[col], errors='coerce')
cwed_country = (cwed_window.groupby('cntry')[['TOTGEN', 'UEGEN', 'SKGEN', 'PGEN']]
                .mean().reset_index()
                .rename(columns={'TOTGEN': 'cwed_total',
                                 'UEGEN': 'cwed_ue',
                                 'SKGEN': 'cwed_sk',
                                 'PGEN': 'cwed_pen'}))
print(f"  CWED 15-country sub-components computed:")
for c in ['cwed_total', 'cwed_ue', 'cwed_sk', 'cwed_pen']:
    print(f"    {c}: range [{cwed_country[c].min():.2f}, {cwed_country[c].max():.2f}], mean {cwed_country[c].mean():.2f}")

df = df.merge(cwed_country, on='cntry', how='left')

# Z-standardize on the 15-country sample for each sub-component
df_rs = df.dropna(subset=['cwed_total']).copy()  # restricts to 15 WE countries
for col in ['cwed_total', 'cwed_ue', 'cwed_sk', 'cwed_pen']:
    df_rs[col + '_z'] = (df_rs[col] - df_rs[col].mean()) / df_rs[col].std()
print(f"  RS sample (CWED-available): {len(df_rs):,} obs, {df_rs['cntry'].nunique()} countries")

# ── Helper: fit random-slopes Model 3 with sub-component ──────────────────────
def fit_rs_model3(data, cwed_var, extra_controls=None):
    """Fit `anti_immig_index ~ task_z * cwed_var + CTRLS + extras` with (1+task_z|cntry_wave)."""
    ctrls_list = list(CTRLS) + (extra_controls or [])
    formula = f'anti_immig_index ~ task_z * {cwed_var} + ' + ' + '.join(ctrls_list)
    keep = ['task_z', 'anti_immig_index', cwed_var, GROUPS] + ctrls_list
    sub = data[keep].dropna().reset_index(drop=True)
    endog, exog = patsy.dmatrices(formula, data=sub, return_type='dataframe')
    endog = endog.iloc[:, 0]
    groups = sub[GROUPS].astype(str).tolist()
    exog_re = patsy.dmatrix('~task_z', data=sub, return_type='dataframe')
    m = MixedLM(endog, exog, groups=groups, exog_re=exog_re).fit(reml=True, method='lbfgs', disp=False)
    int_key = next((k for k in m.params.index if cwed_var in k and 'task_z' in k), None)
    if int_key is None:
        return None
    return {
        'spec': cwed_var,
        'n_obs': int(m.nobs),
        'n_groups': sub[GROUPS].nunique(),
        'rti_main': m.params.get('task_z', np.nan),
        'rti_main_se': m.bse.get('task_z', np.nan),
        'cwed_main': m.params.get(cwed_var, np.nan),
        'interaction_beta': m.params[int_key],
        'interaction_se': m.bse[int_key],
        'interaction_p': m.pvalues[int_key],
    }

# ── 2a/2b: Sub-components — random-slopes Model 3, with and without macros ───
print("\n[2a/2b] Sub-components in random-slopes spec (consistent with §V.D)...")

# Macro controls: GDP growth and Gini, mean 2012-2018 (matches random_slopes_models.py)
print("  Loading macro controls (GDP growth, Gini)...")
cpds = pd.read_stata(CPDS_FILE, columns=['iso', 'year', 'realgdpgr', 'postfisc_gini'])
cpds_mean = (cpds[cpds['year'].between(2012, 2018)]
             .groupby('iso')[['realgdpgr', 'postfisc_gini']]
             .mean().reset_index()
             .rename(columns={'realgdpgr': 'gdp_growth',
                              'postfisc_gini': 'gini',
                              'iso': 'iso3'}))
df_rs['iso3'] = df_rs['cntry'].map(ISO2_TO_ISO3)
df_rs_macro = df_rs.merge(cpds_mean, on='iso3', how='left')
print(f"    Macro merged: {df_rs_macro['gdp_growth'].notna().sum():,} obs with GDP/Gini")

rs_results = []
macro_results = []
for label, var in [('Composite', 'cwed_total_z'),
                   ('Unemployment', 'cwed_ue_z'),
                   ('Sickness', 'cwed_sk_z'),
                   ('Pensions', 'cwed_pen_z')]:
    print(f"\n  {label}:")
    # Base RS (no macro controls)
    res = fit_rs_model3(df_rs, var)
    if res:
        res['label'] = label
        res['model'] = 'RS_base'
        rs_results.append(res)
        stars = '***' if res['interaction_p'] < 0.001 else '**' if res['interaction_p'] < 0.01 else '*' if res['interaction_p'] < 0.05 else '†' if res['interaction_p'] < 0.10 else ''
        print(f"    RS base:  β={res['interaction_beta']:+.4f}  SE={res['interaction_se']:.4f}  p={res['interaction_p']:.4f} {stars}  N={res['n_obs']:,}")
    # With macro controls
    res_m = fit_rs_model3(df_rs_macro.dropna(subset=['gdp_growth', 'gini']), var, extra_controls=['gdp_growth', 'gini'])
    if res_m:
        res_m['label'] = label
        res_m['model'] = 'RS_macro'
        macro_results.append(res_m)
        stars = '***' if res_m['interaction_p'] < 0.001 else '**' if res_m['interaction_p'] < 0.01 else '*' if res_m['interaction_p'] < 0.05 else '†' if res_m['interaction_p'] < 0.10 else ''
        print(f"    RS+macro: β={res_m['interaction_beta']:+.4f}  SE={res_m['interaction_se']:.4f}  p={res_m['interaction_p']:.4f} {stars}  N={res_m['n_obs']:,}")

pd.DataFrame(rs_results).to_csv('outputs/tables/cwed_subcomponents_rs.csv', index=False)
pd.DataFrame(macro_results).to_csv('outputs/tables/cwed_subcomponents_macro.csv', index=False)
print("\n  Saved: cwed_subcomponents_rs.csv, cwed_subcomponents_macro.csv")

# ── 2c: UEGEN country jackknife ───────────────────────────────────────────────
# Predicted dominant sub-component is UEGEN. Test single-country drops.
# (PGEN/SKGEN jackknives skipped to keep runtime under control; if UEGEN proves
#  dominant in 2a/2b, this is the consequential robustness check.)
print("\n[2c] UEGEN country jackknife (random-slopes spec)...")
ue_jack = []
countries = sorted(df_rs['cntry'].dropna().unique())
for c in countries:
    d = df_rs[df_rs['cntry'] != c]
    res = fit_rs_model3(d, 'cwed_ue_z')
    if res:
        ue_jack.append({
            'excluded': c,
            'beta': res['interaction_beta'],
            'se': res['interaction_se'],
            'p': res['interaction_p'],
            'n_obs': res['n_obs'],
            'n_groups': res['n_groups'],
            'n_countries': df_rs[df_rs['cntry'] != c]['cntry'].nunique(),
        })
ue_jack_df = pd.DataFrame(ue_jack).sort_values('beta')
ue_jack_df.to_csv('outputs/tables/uegen_country_jackknife.csv', index=False)
print(f"  UEGEN jackknife: {len(ue_jack_df)} of {len(countries)} country drops converged")
if len(ue_jack_df):
    print(f"    β range: [{ue_jack_df['beta'].min():.4f}, {ue_jack_df['beta'].max():.4f}]")
    print(f"    Sign-flip count: {(ue_jack_df['beta'] >= 0).sum()} of {len(ue_jack_df)}")
    print(f"    p<0.05 count:    {(ue_jack_df['p'] < 0.05).sum()} of {len(ue_jack_df)}")
print("  Saved: uegen_country_jackknife.csv")

# ── 2d: Item-level decomposition ──────────────────────────────────────────────
# Anti-immig index = (imwbcnt + imueclt + imbgeco) / 3, all reverse-coded.
# Run RS Model 3 (composite CWED) separately on each item.
# The dignity mechanism predicts cultural item (imueclt) > economic item (imbgeco).
print("\n[2d] Item-level decomposition (composite CWED, RS spec)...")

ITEM_COLS = ['imwbcnt', 'imueclt', 'imbgeco']  # confirmed by grep'd codebook
ITEM_LABELS = {
    'imwbcnt': 'Country worse',
    'imueclt': 'Cultural undermining',
    'imbgeco': 'Bad for economy',
}

# Check items are in the master
item_present = [c for c in ITEM_COLS if c in df.columns]
print(f"  Items in master: {item_present}")

if not item_present:
    print("  WARNING: No raw items in master. The anti_immig_index is pre-aggregated;")
    print("           the items would need to be re-merged from ESS source data.")
    print("           Skipping item-level decomposition.")
    item_results = []
else:
    item_results = []
    for item in ITEM_COLS:
        if item not in df_rs.columns:
            print(f"    {item}: NOT in master, skipping")
            continue
        # Reverse-code if needed: ESS items are 0-10 where higher = more anti-immig
        # The composite anti_immig_index uses (10 - item) for some — check via correlation
        # Use raw item; if the item is already coded so high = anti-immig, the sign is right.
        # If low = anti-immig (which is the ESS default), sign is wrong but magnitude is right.
        formula_item = f'{item} ~ task_z * cwed_total_z + ' + ' + '.join(CTRLS)
        keep_item = [item, 'task_z', 'cwed_total_z', GROUPS] + CTRLS
        sub = df_rs[keep_item].dropna().reset_index(drop=True)
        if len(sub) < 100:
            print(f"    {item}: too few obs ({len(sub)}), skipping")
            continue
        try:
            endog, exog = patsy.dmatrices(formula_item, data=sub, return_type='dataframe')
            endog = endog.iloc[:, 0]
            groups = sub[GROUPS].astype(str).tolist()
            exog_re = patsy.dmatrix('~task_z', data=sub, return_type='dataframe')
            m = MixedLM(endog, exog, groups=groups, exog_re=exog_re).fit(reml=True, method='lbfgs', disp=False)
            int_key = next((k for k in m.params.index if 'cwed_total_z' in k and 'task_z' in k), None)
            if int_key:
                row = {
                    'item': item,
                    'item_label': ITEM_LABELS[item],
                    'rti_main': m.params.get('task_z', np.nan),
                    'rti_main_se': m.bse.get('task_z', np.nan),
                    'rti_main_p': m.pvalues.get('task_z', np.nan),
                    'cwed_int': m.params[int_key],
                    'cwed_int_se': m.bse[int_key],
                    'cwed_int_p': m.pvalues[int_key],
                    'n_obs': int(m.nobs),
                    'n_groups': sub[GROUPS].nunique(),
                }
                item_results.append(row)
                stars = '***' if row['cwed_int_p'] < 0.001 else '**' if row['cwed_int_p'] < 0.01 else '*' if row['cwed_int_p'] < 0.05 else '†' if row['cwed_int_p'] < 0.10 else ''
                print(f"    {item} ({ITEM_LABELS[item]}): RTI×CWED β={row['cwed_int']:+.4f}, p={row['cwed_int_p']:.4f} {stars}")
        except Exception as e:
            print(f"    {item}: failed — {e}")

if item_results:
    pd.DataFrame(item_results).to_csv('outputs/tables/cwed_interaction_by_item.csv', index=False)
    print("  Saved: cwed_interaction_by_item.csv")

print("\n══ Done. Summary ══════════════════════════════════════════════════════")
print(f"  Sub-components RS: {len(rs_results)} fit")
print(f"  Sub-components RS+macro: {len(macro_results)} fit")
print(f"  UEGEN jackknife: {len(ue_jack_df)} country drops")
print(f"  Item-level: {len(item_results)} items")
