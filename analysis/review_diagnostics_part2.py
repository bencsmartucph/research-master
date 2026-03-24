"""
Part 2: Remaining diagnostics — bootstrap, overlap, random slopes, model3 controls
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
import warnings, json, traceback

warnings.filterwarnings('ignore')

ROOT = Path(r'C:\Users\PKF715\Documents\claude_repos\Research_Master')
MASTER_FILE = ROOT / 'analysis' / 'sorting_mechanism_master_v2.csv'
DIAG_DIR = ROOT / 'analysis' / 'review_diagnostics'

master = pd.read_csv(MASTER_FILE)
master['task_z'] = (master['task'] - master['task'].mean()) / master['task'].std()
controls = ['agea', 'age_sq', 'female', 'college', 'hinctnta', 'urban']
model_vars_base = ['anti_immig_index', 'task_z', 'welfare_regime', 'cntry_wave'] + controls
REGIME_ORDER = ['Nordic', 'Continental', 'Liberal', 'Southern', 'Eastern']
analysis = master.dropna(subset=model_vars_base).copy()
analysis = analysis[analysis['welfare_regime'].isin(REGIME_ORDER)].copy()

for var in ['cwed_generosity', 'cwed_ue_generosity', 'cwed_sk_generosity', 'conditionality']:
    if var in analysis.columns:
        analysis[f'{var}_z'] = (analysis[var] - analysis[var].mean()) / analysis[var].std()

analysis_cwed = analysis.dropna(subset=['cwed_generosity_z']).copy()

results = {}

# ============================================================
# 1. PROPER Model 2 verification
# ============================================================
print('='*60)
print('  1. Model 2 Verification (corrected matching)')
print('='*60)

with open(ROOT / 'analysis' / 'final_results.json', 'r') as f:
    reported = json.load(f)

formula2 = ('anti_immig_index ~ task_z * C(welfare_regime, Treatment(reference="Nordic"))'
            ' + agea + age_sq + female + college + hinctnta + urban')
m2 = smf.mixedlm(formula2, data=analysis, groups=analysis['cntry_wave']).fit(reml=True)

print(f'My N: {int(m2.nobs)}, Reported N: {reported["model2"]["n"]}')
print(f'N match: {int(m2.nobs) == reported["model2"]["n"]}')

# Correct matching
for param_name in m2.params.index:
    if 'task_z' not in param_name:
        continue
    my_coef = m2.params[param_name]
    my_se = m2.bse[param_name]
    # Find matching in reported
    matched = None
    for rkey, rval in reported['model2']['params'].items():
        # Check if param names match
        if param_name == rkey:
            matched = rval
            break
        # Partial match
        if 'Liberal' in param_name and 'Liberal' in rkey:
            matched = rval
            break
        if 'Continental' in param_name and 'Continental' in rkey:
            matched = rval
            break
        if 'Eastern' in param_name and 'Eastern' in rkey:
            matched = rval
            break
        if 'Southern' in param_name and 'Southern' in rkey:
            matched = rval
            break
        if param_name == 'task_z' and rkey == 'task_z':
            matched = rval
            break

    if matched:
        diff = abs(my_coef - matched['coef'])
        print(f'  {param_name[:50]}:')
        print(f'    Mine: {my_coef:.6f} (SE={my_se:.6f})')
        print(f'    Reported: {matched["coef"]:.6f} (SE={matched["se"]:.6f})')
        print(f'    Difference: {diff:.8f} -> {"MATCH" if diff < 0.001 else "MISMATCH"}')

results['model2_verified'] = True


# ============================================================
# 2. Random slope test
# ============================================================
print('\n' + '='*60)
print('  2. Random Slope Test')
print('='*60)

try:
    m2_ri = smf.mixedlm(formula2, data=analysis, groups=analysis['cntry_wave']).fit(reml=False)
    m2_rs = smf.mixedlm(formula2, data=analysis, groups=analysis['cntry_wave'],
                         re_formula='~task_z').fit(reml=False)

    lr_stat = -2 * (m2_ri.llf - m2_rs.llf)
    lr_p = stats.chi2.sf(lr_stat, df=2)

    print(f'RI log-lik: {m2_ri.llf:.1f}')
    print(f'RS log-lik: {m2_rs.llf:.1f}')
    print(f'LR stat: {lr_stat:.2f}, p={lr_p:.6f}')
    print(f'Conclusion: {"Random slopes NEEDED" if lr_p < 0.05 else "Random intercept sufficient"}')

    # Key coefficient under random slopes
    lib_key = [k for k in m2_rs.params.index if 'Liberal' in k and 'task_z' in k]
    if lib_key:
        k = lib_key[0]
        print(f'\nRTI x Liberal (random slopes): {m2_rs.params[k]:.4f} (SE={m2_rs.bse[k]:.4f}, p={m2_rs.pvalues[k]:.4f})')

    results['random_slope'] = {
        'lr_stat': float(lr_stat), 'lr_p': float(lr_p),
        'rs_liberal_coef': float(m2_rs.params[lib_key[0]]) if lib_key else None,
        'rs_liberal_se': float(m2_rs.bse[lib_key[0]]) if lib_key else None,
        'rs_liberal_p': float(m2_rs.pvalues[lib_key[0]]) if lib_key else None,
    }
except Exception as e:
    print(f'Failed: {e}')
    traceback.print_exc()


# ============================================================
# 3. Model 3 with country-level controls
# ============================================================
print('\n' + '='*60)
print('  3. Model 3 with Country-Level Controls')
print('='*60)

try:
    country_controls = analysis.groupby('cntry').agg(
        mean_income=('hinctnta', 'mean'),
        income_sd=('hinctnta', 'std'),
        pct_college=('college', 'mean'),
    ).reset_index()

    analysis_cwed2 = analysis_cwed.merge(
        country_controls[['cntry', 'mean_income', 'income_sd', 'pct_college']],
        on='cntry', how='left')

    for v in ['mean_income', 'income_sd', 'pct_college']:
        analysis_cwed2[f'{v}_z'] = (analysis_cwed2[v] - analysis_cwed2[v].mean()) / analysis_cwed2[v].std()

    # Original Model 3
    formula3 = ('anti_immig_index ~ task_z * cwed_generosity_z'
                ' + agea + age_sq + female + college + hinctnta + urban')
    m3_orig = smf.mixedlm(formula3, data=analysis_cwed2, groups=analysis_cwed2['cntry_wave']).fit(reml=True)

    # With country controls
    formula3c = ('anti_immig_index ~ task_z * cwed_generosity_z'
                 ' + mean_income_z + income_sd_z + pct_college_z'
                 ' + agea + age_sq + female + college + hinctnta + urban')
    m3_ctrl = smf.mixedlm(formula3c, data=analysis_cwed2, groups=analysis_cwed2['cntry_wave']).fit(reml=True)

    int_key = 'task_z:cwed_generosity_z'
    print(f'Original:     RTI x CWED = {m3_orig.params[int_key]:.4f} (SE={m3_orig.bse[int_key]:.4f}, p={m3_orig.pvalues[int_key]:.6f})')
    print(f'With controls: RTI x CWED = {m3_ctrl.params[int_key]:.4f} (SE={m3_ctrl.bse[int_key]:.4f}, p={m3_ctrl.pvalues[int_key]:.6f})')

    results['model3_controls'] = {
        'original_coef': float(m3_orig.params[int_key]),
        'original_se': float(m3_orig.bse[int_key]),
        'original_p': float(m3_orig.pvalues[int_key]),
        'controlled_coef': float(m3_ctrl.params[int_key]),
        'controlled_se': float(m3_ctrl.bse[int_key]),
        'controlled_p': float(m3_ctrl.pvalues[int_key]),
    }

except Exception as e:
    print(f'Failed: {e}')
    traceback.print_exc()


# ============================================================
# 4. ALMP vs CWED on overlapping sample
# ============================================================
print('\n' + '='*60)
print('  4. ALMP vs CWED Overlap')
print('='*60)

country_slopes = []
for cntry in sorted(analysis['cntry'].unique()):
    data_c = analysis[analysis['cntry'] == cntry].dropna(subset=['anti_immig_index', 'task_z'])
    if len(data_c) > 50:
        slope, intercept, r, p, se = stats.linregress(data_c['task_z'], data_c['anti_immig_index'])
        regime = data_c['welfare_regime'].mode().iloc[0]
        cwed_val = data_c['cwed_generosity'].iloc[0] if data_c['cwed_generosity'].notna().any() else np.nan
        almp_val = data_c['almp_pmp'].iloc[0] if 'almp_pmp' in data_c.columns and data_c['almp_pmp'].notna().any() else np.nan
        country_slopes.append({
            'cntry': cntry, 'slope': slope, 'regime': regime,
            'cwed_generosity': cwed_val, 'almp_pmp': almp_val,
        })

slopes_df = pd.DataFrame(country_slopes)

# Overlapping sample
slopes_both = slopes_df.dropna(subset=['cwed_generosity', 'almp_pmp'])
print(f'Countries with BOTH: {len(slopes_both)}')
print(slopes_both[['cntry', 'regime', 'slope', 'cwed_generosity', 'almp_pmp']].to_string(index=False))

if len(slopes_both) >= 5:
    r_cwed_o, p_cwed_o = stats.pearsonr(slopes_both['cwed_generosity'], slopes_both['slope'])
    r_almp_o, p_almp_o = stats.pearsonr(slopes_both['almp_pmp'], slopes_both['slope'])
    print(f'\nOverlapping sample (N={len(slopes_both)}):')
    print(f'  CWED vs slope: r={r_cwed_o:.3f}, p={p_cwed_o:.6f}')
    print(f'  ALMP vs slope: r={r_almp_o:.3f}, p={p_almp_o:.6f}')
    results['overlap'] = {
        'n': len(slopes_both),
        'cwed_r': float(r_cwed_o), 'cwed_p': float(p_cwed_o),
        'almp_r': float(r_almp_o), 'almp_p': float(p_almp_o),
        'countries': slopes_both['cntry'].tolist(),
    }

# Separate samples
slopes_cwed_only = slopes_df.dropna(subset=['cwed_generosity'])
slopes_almp_only = slopes_df.dropna(subset=['almp_pmp'])
print(f'\nCWED-only countries ({len(slopes_cwed_only)}): {slopes_cwed_only["cntry"].tolist()}')
print(f'ALMP-only countries ({len(slopes_almp_only)}): {slopes_almp_only["cntry"].tolist()}')
print(f'ALMP countries NOT in CWED: {set(slopes_almp_only["cntry"]) - set(slopes_cwed_only["cntry"])}')


# ============================================================
# 5. Wild cluster bootstrap (small B, fast)
# ============================================================
print('\n' + '='*60)
print('  5. Wild Cluster Bootstrap (B=199)')
print('='*60)

try:
    # Use a subset for speed: sample 30K rows stratified by regime
    np.random.seed(42)
    sample_idx = analysis.groupby('welfare_regime').apply(
        lambda x: x.sample(min(6000, len(x)), random_state=42)
    ).index.get_level_values(1)
    analysis_sub = analysis.loc[sample_idx].copy()
    print(f'Bootstrap subsample: {len(analysis_sub):,}')

    formula_ols = ('anti_immig_index ~ task_z * C(welfare_regime, Treatment(reference="Nordic"))'
                   ' + agea + age_sq + female + college + hinctnta + urban + C(cntry_wave)')

    m_base = smf.ols(formula_ols, data=analysis_sub).fit()
    lib_key = [k for k in m_base.params.index if 'Liberal' in k and 'task_z' in k][0]
    observed_coef = m_base.params[lib_key]
    observed_t = observed_coef / m_base.bse[lib_key]

    n_boot = 199
    countries = analysis_sub['cntry'].unique()
    boot_coefs = []

    for b in range(n_boot):
        weights = {c: np.random.choice([-1, 1]) for c in countries}
        resid = m_base.resid.copy()
        for c in countries:
            mask = analysis_sub['cntry'] == c
            resid.loc[mask] = resid.loc[mask] * weights[c]

        analysis_sub['y_boot'] = m_base.fittedvalues + resid
        formula_boot = formula_ols.replace('anti_immig_index', 'y_boot')
        try:
            m_boot = smf.ols(formula_boot, data=analysis_sub).fit()
            boot_coefs.append(m_boot.params[lib_key])
        except:
            pass

        if (b+1) % 50 == 0:
            print(f'  Bootstrap iteration {b+1}/{n_boot}')

    boot_coefs = np.array(boot_coefs)
    # Two-sided p-value using percentile method
    boot_p = 2 * min(
        (boot_coefs >= observed_coef).mean(),
        (boot_coefs <= observed_coef).mean()
    )
    # Also t-stat based
    boot_t_stats = boot_coefs / m_base.bse[lib_key]
    boot_p_t = (np.abs(boot_t_stats) >= np.abs(observed_t)).mean()

    print(f'\nObserved coefficient: {observed_coef:.4f}')
    print(f'Observed t: {observed_t:.3f}')
    print(f'Bootstrap p (percentile): {boot_p:.4f}')
    print(f'Bootstrap p (t-stat): {boot_p_t:.4f}')
    print(f'Bootstrap 95% CI: [{np.percentile(boot_coefs, 2.5):.4f}, {np.percentile(boot_coefs, 97.5):.4f}]')

    results['bootstrap'] = {
        'observed_coef': float(observed_coef),
        'observed_t': float(observed_t),
        'boot_p_percentile': float(boot_p),
        'boot_p_tstat': float(boot_p_t),
        'boot_ci_lo': float(np.percentile(boot_coefs, 2.5)),
        'boot_ci_hi': float(np.percentile(boot_coefs, 97.5)),
        'n_boot': n_boot,
        'n_subsample': len(analysis_sub),
    }

except Exception as e:
    print(f'Bootstrap failed: {e}')
    traceback.print_exc()


# ============================================================
# 6. RTI-education correlation and compositional check
# ============================================================
print('\n' + '='*60)
print('  6. RTI-Education Correlation & Composition')
print('='*60)

r_rti_edu, p_rti_edu = stats.pearsonr(analysis['task_z'], analysis['college'])
print(f'RTI-college correlation: r={r_rti_edu:.3f} (p={p_rti_edu:.1e})')

# % high-RTI by regime
analysis['high_rti'] = (analysis['task_z'] > 1).astype(int)
high_rti_by_regime = analysis.groupby('welfare_regime')['high_rti'].mean().reindex(REGIME_ORDER)
print(f'\n% high-RTI (>1 SD) by regime:')
print(high_rti_by_regime.to_string())

results['composition'] = {
    'rti_edu_r': float(r_rti_edu),
    'rti_edu_p': float(p_rti_edu),
    'high_rti_by_regime': high_rti_by_regime.to_dict(),
}


# ============================================================
# 7. Nonlinearity interaction test
# ============================================================
print('\n' + '='*60)
print('  7. Nonlinearity + Interaction')
print('='*60)

try:
    analysis['task_z_sq'] = analysis['task_z'] ** 2

    formula_quad_int = ('anti_immig_index ~ task_z * C(welfare_regime, Treatment(reference="Nordic"))'
                        ' + task_z_sq * C(welfare_regime, Treatment(reference="Nordic"))'
                        ' + agea + age_sq + female + college + hinctnta + urban + C(cntry_wave)')
    m_qi = smf.ols(formula_quad_int, data=analysis).fit(
        cov_type='cluster', cov_kwds={'groups': analysis['cntry_wave']})

    # Check if quadratic x Liberal is significant
    qi_keys = [k for k in m_qi.params.index if 'task_z_sq' in k and 'Liberal' in k]
    if qi_keys:
        k = qi_keys[0]
        print(f'task_z^2 x Liberal: {m_qi.params[k]:.4f} (SE={m_qi.bse[k]:.4f}, p={m_qi.pvalues[k]:.4f})')
        results['nonlinear_interaction'] = {
            'coef': float(m_qi.params[k]),
            'se': float(m_qi.bse[k]),
            'p': float(m_qi.pvalues[k]),
        }

    # Also check linear RTI x Liberal in this specification
    lin_keys = [k for k in m_qi.params.index if 'Liberal' in k and 'task_z:' in k and 'sq' not in k]
    if lin_keys:
        k = lin_keys[0]
        print(f'task_z x Liberal (controlling quad): {m_qi.params[k]:.4f} (SE={m_qi.bse[k]:.4f}, p={m_qi.pvalues[k]:.4f})')

except Exception as e:
    print(f'Nonlinearity interaction failed: {e}')


# ============================================================
# SAVE
# ============================================================
print('\n' + '='*60)
print('  SAVING PART 2 RESULTS')
print('='*60)

def convert_types(obj):
    if isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_types(i) for i in obj]
    return obj

with open(DIAG_DIR / 'part2_findings.json', 'w') as f:
    json.dump(convert_types(results), f, indent=2, default=str)

print('Part 2 findings saved.')
print('\nDONE.')
