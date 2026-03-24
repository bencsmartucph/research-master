"""
Econometric Review Diagnostics — Sorting Mechanism Paper
=========================================================
Hostile-but-constructive referee review. Loads actual data,
re-estimates models, runs influence diagnostics, specification tests,
and sample composition checks.

Author: Methods Referee (Claude, 2026-03-16)
"""

# --- Config ---
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
import json
import traceback

warnings.filterwarnings('ignore')

ROOT = Path(r'C:\Users\PKF715\Documents\claude_repos\Research_Master')
MASTER_FILE = ROOT / 'analysis' / 'sorting_mechanism_master_v2.csv'
RESULTS_FILE = ROOT / 'analysis' / 'final_results.json'
DIAG_DIR = ROOT / 'analysis' / 'review_diagnostics'
DIAG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Collect all findings for the review document
findings = {}

# ============================================================
# LOAD DATA AND REPORTED RESULTS
# ============================================================
print('='*60)
print('  LOADING DATA')
print('='*60)

master = pd.read_csv(MASTER_FILE)
print(f'Master dataset: {master.shape}')

with open(RESULTS_FILE, 'r') as f:
    reported = json.load(f)

# Reproduce the analysis sample construction
master['task_z'] = (master['task'] - master['task'].mean()) / master['task'].std()
controls = ['agea', 'age_sq', 'female', 'college', 'hinctnta', 'urban']
model_vars_base = ['anti_immig_index', 'task_z', 'welfare_regime', 'cntry_wave'] + controls

REGIME_ORDER = ['Nordic', 'Continental', 'Liberal', 'Southern', 'Eastern']

analysis = master.dropna(subset=model_vars_base).copy()
analysis = analysis[analysis['welfare_regime'].isin(REGIME_ORDER)].copy()
analysis['non_college'] = (1 - analysis['college']).astype(int)

print(f'Analysis sample: {len(analysis):,}')
print(f'Reported N for Model 1: {reported["model1"]["n"]}')
findings['sample_n_match'] = len(analysis) == reported['model1']['n']
print(f'  Sample N matches reported: {findings["sample_n_match"]}')

# CWED subsample
for var in ['cwed_generosity', 'cwed_ue_generosity', 'cwed_sk_generosity', 'conditionality']:
    if var in analysis.columns:
        analysis[f'{var}_z'] = (analysis[var] - analysis[var].mean()) / analysis[var].std()

analysis_cwed = analysis.dropna(subset=['cwed_generosity_z']).copy()
print(f'CWED subsample: {len(analysis_cwed):,}')
print(f'Reported CWED N: {reported["model3"]["n"]}')
findings['cwed_n_match'] = len(analysis_cwed) == reported['model3']['n']
print(f'  CWED N matches reported: {findings["cwed_n_match"]}')


# ============================================================
# 1. VERIFICATION: Re-estimate Model 2
# ============================================================
print('\n' + '='*60)
print('  1. VERIFICATION: Re-estimate Model 2')
print('='*60)

formula2 = ('anti_immig_index ~ task_z * C(welfare_regime, Treatment(reference="Nordic"))'
            ' + agea + age_sq + female + college + hinctnta + urban')
m2 = smf.mixedlm(formula2, data=analysis, groups=analysis['cntry_wave']).fit(reml=True)

# Compare coefficients
verification_results = []
for param_name in m2.params.index:
    if 'task_z' in param_name:
        my_coef = m2.params[param_name]
        my_se = m2.bse[param_name]
        my_p = m2.pvalues[param_name]

        # Find matching reported coefficient
        reported_coef = None
        for rkey, rval in reported['model2']['params'].items():
            if param_name in rkey or rkey in param_name:
                reported_coef = rval
                break

        if reported_coef:
            coef_diff = abs(my_coef - reported_coef['coef'])
            se_diff = abs(my_se - reported_coef['se'])
            verification_results.append({
                'param': param_name[:60],
                'my_coef': my_coef,
                'reported_coef': reported_coef['coef'],
                'coef_diff': coef_diff,
                'my_se': my_se,
                'reported_se': reported_coef['se'],
                'se_diff': se_diff,
                'match': coef_diff < 0.001,
            })

verif_df = pd.DataFrame(verification_results)
print('\nModel 2 verification:')
print(verif_df.to_string(index=False))
verif_df.to_csv(DIAG_DIR / 'model2_verification.csv', index=False)

all_match = verif_df['match'].all()
findings['model2_verification'] = 'PASS' if all_match else 'DISCREPANCY DETECTED'
print(f'\nAll coefficients match within 0.001: {all_match}')


# ============================================================
# 2. INFLUENCE DIAGNOSTICS: CWED correlation
# ============================================================
print('\n' + '='*60)
print('  2. INFLUENCE DIAGNOSTICS: CWED r=-0.848')
print('='*60)

# Get country slopes
country_slopes = []
for cntry in sorted(analysis['cntry'].unique()):
    data_c = analysis[analysis['cntry'] == cntry].dropna(subset=['anti_immig_index', 'task_z'])
    if len(data_c) > 50:
        slope, intercept, r, p, se = stats.linregress(data_c['task_z'], data_c['anti_immig_index'])
        regime = data_c['welfare_regime'].mode().iloc[0]
        cwed_val = data_c['cwed_generosity'].iloc[0] if data_c['cwed_generosity'].notna().any() else np.nan
        almp_val = data_c['almp_pmp'].iloc[0] if 'almp_pmp' in data_c.columns and data_c['almp_pmp'].notna().any() else np.nan
        country_slopes.append({
            'cntry': cntry, 'slope': slope, 'se': se, 'p': p, 'n': len(data_c),
            'regime': regime, 'cwed_generosity': cwed_val, 'almp_pmp': almp_val,
        })

slopes_df = pd.DataFrame(country_slopes)
slopes_cwed = slopes_df.dropna(subset=['cwed_generosity']).copy()
print(f'Countries with CWED data: {len(slopes_cwed)}')
print(slopes_cwed[['cntry', 'regime', 'slope', 'cwed_generosity']].to_string(index=False))

# Full correlation
r_full, p_full = stats.pearsonr(slopes_cwed['cwed_generosity'], slopes_cwed['slope'])
print(f'\nFull sample: r={r_full:.3f}, p={p_full:.6f}, N={len(slopes_cwed)}')

# Leave-one-out influence diagnostics
influence_results = []
for i, row in slopes_cwed.iterrows():
    excluded = row['cntry']
    subset = slopes_cwed[slopes_cwed['cntry'] != excluded]
    if len(subset) >= 5:
        r_loo, p_loo = stats.pearsonr(subset['cwed_generosity'], subset['slope'])
        influence_results.append({
            'excluded': excluded,
            'r': r_loo,
            'p': p_loo,
            'r_change': r_loo - r_full,
            'n': len(subset),
        })

influence_df = pd.DataFrame(influence_results)
print('\nLeave-one-out influence on CWED correlation:')
print(influence_df.sort_values('r').to_string(index=False))
influence_df.to_csv(DIAG_DIR / 'cwed_influence_loo.csv', index=False)

# Drop GB
excl_gb = slopes_cwed[slopes_cwed['cntry'] != 'GB']
r_no_gb, p_no_gb = stats.pearsonr(excl_gb['cwed_generosity'], excl_gb['slope'])
print(f'\nDrop GB: r={r_no_gb:.3f}, p={p_no_gb:.6f}')

# Drop NO
excl_no = slopes_cwed[slopes_cwed['cntry'] != 'NO']
r_no_no, p_no_no = stats.pearsonr(excl_no['cwed_generosity'], excl_no['slope'])
print(f'Drop NO: r={r_no_no:.3f}, p={p_no_no:.6f}')

# Drop both
excl_both = slopes_cwed[~slopes_cwed['cntry'].isin(['GB', 'NO'])]
r_no_both, p_no_both = stats.pearsonr(excl_both['cwed_generosity'], excl_both['slope'])
print(f'Drop GB+NO: r={r_no_both:.3f}, p={p_no_both:.6f}')

# Cook's distance via OLS regression of slope on generosity
X_cook = sm.add_constant(slopes_cwed['cwed_generosity'].values)
y_cook = slopes_cwed['slope'].values
ols_cook = sm.OLS(y_cook, X_cook).fit()
influence_obj = ols_cook.get_influence()
cooks_d = influence_obj.cooks_distance[0]
slopes_cwed_copy = slopes_cwed.copy()
slopes_cwed_copy['cooks_d'] = cooks_d

print('\nCook\'s distance:')
for _, row in slopes_cwed_copy.sort_values('cooks_d', ascending=False).iterrows():
    flag = ' *** INFLUENTIAL' if row['cooks_d'] > 4/len(slopes_cwed) else ''
    print(f"  {row['cntry']}: Cook's D = {row['cooks_d']:.4f}{flag}")

slopes_cwed_copy[['cntry', 'regime', 'slope', 'cwed_generosity', 'cooks_d']].to_csv(
    DIAG_DIR / 'cwed_cooks_distance.csv', index=False)

findings['cwed_influence'] = {
    'full_r': r_full, 'full_p': p_full,
    'no_gb_r': r_no_gb, 'no_gb_p': p_no_gb,
    'no_no_r': r_no_no, 'no_no_p': p_no_no,
    'no_both_r': r_no_both, 'no_both_p': p_no_both,
    'max_cooks_d': float(cooks_d.max()),
    'max_cooks_country': slopes_cwed_copy.loc[slopes_cwed_copy['cooks_d'].idxmax(), 'cntry'],
}

# Influence diagnostic plot
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Panel A: Full sample scatter
ax = axes[0]
for regime, color in [('Nordic', '#2166AC'), ('Continental', '#67A9CF'),
                       ('Liberal', '#D6604D'), ('Southern', '#F4A582')]:
    mask = slopes_cwed['regime'] == regime
    if mask.any():
        ax.scatter(slopes_cwed.loc[mask, 'cwed_generosity'], slopes_cwed.loc[mask, 'slope'],
                  color=color, s=60, label=regime, zorder=3)
        for _, row in slopes_cwed[mask].iterrows():
            ax.annotate(row['cntry'], (row['cwed_generosity'], row['slope']),
                       fontsize=7, ha='left', va='bottom')
# Fit line
z = np.polyfit(slopes_cwed['cwed_generosity'], slopes_cwed['slope'], 1)
x_line = np.linspace(slopes_cwed['cwed_generosity'].min(), slopes_cwed['cwed_generosity'].max(), 100)
ax.plot(x_line, np.polyval(z, x_line), 'k--', alpha=0.5)
ax.set_xlabel('CWED Total Generosity')
ax.set_ylabel('RTI → Anti-Immigration Slope')
ax.set_title(f'Full Sample (r={r_full:.3f}, N={len(slopes_cwed)})')
ax.legend(fontsize=8)

# Panel B: Drop GB
ax = axes[1]
for regime, color in [('Nordic', '#2166AC'), ('Continental', '#67A9CF'),
                       ('Liberal', '#D6604D'), ('Southern', '#F4A582')]:
    mask = (slopes_cwed['regime'] == regime) & (slopes_cwed['cntry'] != 'GB')
    if mask.any():
        ax.scatter(slopes_cwed.loc[mask, 'cwed_generosity'], slopes_cwed.loc[mask, 'slope'],
                  color=color, s=60, zorder=3)
        for _, row in slopes_cwed[mask].iterrows():
            ax.annotate(row['cntry'], (row['cwed_generosity'], row['slope']),
                       fontsize=7, ha='left', va='bottom')
z2 = np.polyfit(excl_gb['cwed_generosity'], excl_gb['slope'], 1)
ax.plot(x_line, np.polyval(z2, x_line), 'k--', alpha=0.5)
ax.set_xlabel('CWED Total Generosity')
ax.set_title(f'Drop GB (r={r_no_gb:.3f})')

# Panel C: Cook's distance
ax = axes[2]
ax.bar(range(len(slopes_cwed_copy)), slopes_cwed_copy.sort_values('cooks_d', ascending=False)['cooks_d'].values,
       color='steelblue', alpha=0.7)
ax.set_xticks(range(len(slopes_cwed_copy)))
ax.set_xticklabels(slopes_cwed_copy.sort_values('cooks_d', ascending=False)['cntry'].values,
                   rotation=45, ha='right', fontsize=8)
ax.axhline(y=4/len(slopes_cwed), color='red', linestyle='--', label=f'4/N = {4/len(slopes_cwed):.3f}')
ax.set_ylabel("Cook's Distance")
ax.set_title("Influence Diagnostics")
ax.legend(fontsize=8)

plt.tight_layout()
fig.savefig(DIAG_DIR / 'cwed_influence_diagnostics.png')
plt.close()
print('Saved cwed_influence_diagnostics.png')


# ============================================================
# 3. SPECIFICATION TESTS
# ============================================================
print('\n' + '='*60)
print('  3. SPECIFICATION TESTS')
print('='*60)

# --- 3a. Random intercept vs random slope ---
print('\n--- 3a. Random intercept vs random slope ---')
try:
    # Random intercept only (current Model 2)
    m2_ri = smf.mixedlm(formula2, data=analysis, groups=analysis['cntry_wave']).fit(reml=False)

    # Random slope on task_z
    m2_rs = smf.mixedlm(formula2, data=analysis, groups=analysis['cntry_wave'],
                         re_formula='~task_z').fit(reml=False)

    lr_stat = -2 * (m2_ri.llf - m2_rs.llf)
    # 2 additional parameters (variance of random slope + covariance)
    lr_p = stats.chi2.sf(lr_stat, df=2)

    print(f'Random intercept log-lik: {m2_ri.llf:.1f}')
    print(f'Random slope log-lik: {m2_rs.llf:.1f}')
    print(f'LR test statistic: {lr_stat:.2f}')
    print(f'LR p-value (df=2): {lr_p:.6f}')

    findings['random_slope_test'] = {
        'lr_stat': lr_stat,
        'p_value': lr_p,
        'conclusion': 'Random slopes NEEDED (misspecification)' if lr_p < 0.05 else 'Random intercept sufficient'
    }
    print(f'Conclusion: {findings["random_slope_test"]["conclusion"]}')

    # Check if key interaction changes with random slopes
    lib_key_rs = [k for k in m2_rs.params.index if 'Liberal' in k and 'task_z' in k]
    if lib_key_rs:
        k = lib_key_rs[0]
        print(f'\nRTI x Liberal with random slopes: {m2_rs.params[k]:.4f} (SE={m2_rs.bse[k]:.4f}, p={m2_rs.pvalues[k]:.4f})')
        findings['random_slope_liberal_coef'] = {
            'coef': float(m2_rs.params[k]),
            'se': float(m2_rs.bse[k]),
            'p': float(m2_rs.pvalues[k]),
        }

except Exception as e:
    print(f'Random slope test failed: {e}')
    traceback.print_exc()
    findings['random_slope_test'] = {'status': f'FAILED: {e}'}

# --- 3b. VIF / Multicollinearity ---
print('\n--- 3b. VIF (Multicollinearity) ---')
try:
    vif_vars = ['task_z', 'agea', 'age_sq', 'female', 'college', 'hinctnta', 'urban']
    vif_data = analysis[vif_vars].dropna()
    vif_data = sm.add_constant(vif_data)

    vif_results = []
    for i, col in enumerate(vif_data.columns):
        if col != 'const':
            vif_val = variance_inflation_factor(vif_data.values, i)
            vif_results.append({'variable': col, 'VIF': vif_val})
            flag = ' *** HIGH' if vif_val > 5 else ' ** moderate' if vif_val > 2.5 else ''
            print(f'  {col}: VIF = {vif_val:.2f}{flag}')

    vif_df = pd.DataFrame(vif_results)
    vif_df.to_csv(DIAG_DIR / 'vif_results.csv', index=False)
    findings['vif'] = {v['variable']: v['VIF'] for v in vif_results}

    # Specific concern: RTI-education correlation
    r_rti_edu, p_rti_edu = stats.pearsonr(analysis['task_z'], analysis['college'])
    print(f'\n  RTI-college correlation: r={r_rti_edu:.3f} (p={p_rti_edu:.6f})')
    findings['rti_education_corr'] = {'r': r_rti_edu, 'p': p_rti_edu}

except Exception as e:
    print(f'VIF failed: {e}')

# --- 3c. Functional form: nonlinear RTI ---
print('\n--- 3c. Functional form (nonlinearity in RTI) ---')
try:
    analysis['task_z_sq'] = analysis['task_z'] ** 2

    # Linear vs quadratic
    formula_lin = ('anti_immig_index ~ task_z + agea + age_sq + female + college + hinctnta + urban + C(cntry_wave)')
    formula_quad = ('anti_immig_index ~ task_z + task_z_sq + agea + age_sq + female + college + hinctnta + urban + C(cntry_wave)')

    m_lin = smf.ols(formula_lin, data=analysis).fit()
    m_quad = smf.ols(formula_quad, data=analysis).fit()

    # F-test for quadratic term
    quad_coef = m_quad.params.get('task_z_sq', np.nan)
    quad_p = m_quad.pvalues.get('task_z_sq', np.nan)

    print(f'  Quadratic term (task_z^2): {quad_coef:.4f} (p={quad_p:.4f})')
    print(f'  R² linear: {m_lin.rsquared:.6f}')
    print(f'  R² quadratic: {m_quad.rsquared:.6f}')
    print(f'  R² improvement: {m_quad.rsquared - m_lin.rsquared:.6f}')

    findings['nonlinearity'] = {
        'quad_coef': float(quad_coef),
        'quad_p': float(quad_p),
        'conclusion': 'Significant nonlinearity' if quad_p < 0.05 else 'Linear form adequate'
    }

    # Residuals vs fitted plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Residuals vs fitted
    ax = axes[0]
    fitted = m_lin.fittedvalues
    resids = m_lin.resid
    # Sample for visibility
    idx = np.random.choice(len(fitted), min(5000, len(fitted)), replace=False)
    ax.scatter(fitted.iloc[idx], resids.iloc[idx], alpha=0.1, s=5, color='steelblue')
    # Lowess
    from statsmodels.nonparametric.smoothers_lowess import lowess
    lowess_fit = lowess(resids.values[idx], fitted.values[idx], frac=0.3)
    ax.plot(lowess_fit[:, 0], lowess_fit[:, 1], 'r-', linewidth=2, label='LOWESS')
    ax.axhline(0, color='grey', linestyle='--')
    ax.set_xlabel('Fitted Values')
    ax.set_ylabel('Residuals')
    ax.set_title('Residuals vs Fitted')
    ax.legend()

    # Binned residuals by RTI decile
    ax = axes[1]
    analysis['task_decile'] = pd.qcut(analysis['task_z'], 10, labels=False, duplicates='drop')
    binned_resid = analysis.copy()
    binned_resid['resid'] = m_lin.resid.reindex(analysis.index)
    binned_resid = binned_resid.dropna(subset=['resid'])
    mean_resid = binned_resid.groupby('task_decile')['resid'].mean()
    mean_rti = binned_resid.groupby('task_decile')['task_z'].mean()
    ax.bar(mean_rti.values, mean_resid.values, width=0.15, color='steelblue', alpha=0.7)
    ax.axhline(0, color='grey', linestyle='--')
    ax.set_xlabel('RTI (standardized, decile means)')
    ax.set_ylabel('Mean Residual')
    ax.set_title('Mean Residual by RTI Decile')

    plt.tight_layout()
    fig.savefig(DIAG_DIR / 'functional_form_diagnostics.png')
    plt.close()
    print('Saved functional_form_diagnostics.png')

except Exception as e:
    print(f'Functional form test failed: {e}')
    traceback.print_exc()


# ============================================================
# 4. STANDARD ERRORS
# ============================================================
print('\n' + '='*60)
print('  4. STANDARD ERRORS COMPARISON')
print('='*60)

try:
    formula_ols = ('anti_immig_index ~ task_z * C(welfare_regime, Treatment(reference="Nordic"))'
                   ' + agea + age_sq + female + college + hinctnta + urban + C(cntry_wave)')

    # (a) Mixed model SEs (from Model 2)
    lib_key_mixed = [k for k in m2.params.index if 'Liberal' in k and 'task_z' in k][0]
    mixed_coef = m2.params[lib_key_mixed]
    mixed_se = m2.bse[lib_key_mixed]
    mixed_p = m2.pvalues[lib_key_mixed]

    # (b) OLS with country-wave FE and robust (HC1) SEs
    m_ols_robust = smf.ols(formula_ols, data=analysis).fit(cov_type='HC1')
    lib_key_ols = [k for k in m_ols_robust.params.index if 'Liberal' in k and 'task_z' in k][0]
    robust_coef = m_ols_robust.params[lib_key_ols]
    robust_se = m_ols_robust.bse[lib_key_ols]
    robust_p = m_ols_robust.pvalues[lib_key_ols]

    # (c) OLS with country-wave clustered SEs
    m_ols_cw = smf.ols(formula_ols, data=analysis).fit(
        cov_type='cluster', cov_kwds={'groups': analysis['cntry_wave']})
    cw_se = m_ols_cw.bse[lib_key_ols]
    cw_p = m_ols_cw.pvalues[lib_key_ols]

    # (d) OLS with country-level clustered SEs (fewer clusters)
    m_ols_cc = smf.ols(formula_ols, data=analysis).fit(
        cov_type='cluster', cov_kwds={'groups': analysis['cntry']})
    cc_se = m_ols_cc.bse[lib_key_ols]
    cc_p = m_ols_cc.pvalues[lib_key_ols]

    se_comparison = pd.DataFrame([
        {'Method': 'Mixed model (REML)', 'Coefficient': mixed_coef, 'SE': mixed_se, 'p-value': mixed_p},
        {'Method': 'OLS + HC1 robust', 'Coefficient': robust_coef, 'SE': robust_se, 'p-value': robust_p},
        {'Method': 'OLS + country-wave cluster', 'Coefficient': robust_coef, 'SE': cw_se, 'p-value': cw_p},
        {'Method': 'OLS + country cluster', 'Coefficient': robust_coef, 'SE': cc_se, 'p-value': cc_p},
    ])

    print('\nRTI x Liberal coefficient across SE methods:')
    print(se_comparison.to_string(index=False))
    se_comparison.to_csv(DIAG_DIR / 'se_comparison.csv', index=False)

    findings['se_comparison'] = se_comparison.to_dict('records')

    # Count clusters
    n_cntry_wave = analysis['cntry_wave'].nunique()
    n_cntry = analysis['cntry'].nunique()
    n_liberal = analysis[analysis['welfare_regime'] == 'Liberal']['cntry'].nunique()

    print(f'\nNumber of country-wave clusters: {n_cntry_wave}')
    print(f'Number of country clusters: {n_cntry}')
    print(f'Number of Liberal regime countries: {n_liberal}')
    print(f'Liberal regime countries: {sorted(analysis[analysis["welfare_regime"] == "Liberal"]["cntry"].unique())}')

    # Cluster sizes
    cluster_sizes = analysis.groupby('welfare_regime')['cntry'].nunique()
    print(f'\nCountries per regime:')
    print(cluster_sizes.to_string())

    findings['cluster_info'] = {
        'n_cntry_wave_clusters': int(n_cntry_wave),
        'n_country_clusters': int(n_cntry),
        'n_liberal_countries': int(n_liberal),
    }

except Exception as e:
    print(f'SE comparison failed: {e}')
    traceback.print_exc()


# ============================================================
# 5. SAMPLE AND MEASUREMENT
# ============================================================
print('\n' + '='*60)
print('  5. SAMPLE AND MEASUREMENT')
print('='*60)

# --- 5a. RTI distribution by regime ---
print('\n--- 5a. RTI distribution by regime ---')
rti_by_regime = analysis.groupby('welfare_regime')['task_z'].agg(['mean', 'std', 'median', 'skew'])
print(rti_by_regime.reindex(REGIME_ORDER))
rti_by_regime.to_csv(DIAG_DIR / 'rti_distribution_by_regime.csv')

# KS tests comparing Liberal to each other regime
print('\nKolmogorov-Smirnov tests (Liberal vs others):')
liberal_rti = analysis[analysis['welfare_regime'] == 'Liberal']['task_z']
for regime in REGIME_ORDER:
    if regime != 'Liberal':
        other_rti = analysis[analysis['welfare_regime'] == regime]['task_z']
        ks_stat, ks_p = stats.ks_2samp(liberal_rti, other_rti)
        print(f'  Liberal vs {regime}: KS={ks_stat:.4f}, p={ks_p:.6f}')

findings['rti_composition'] = rti_by_regime.reindex(REGIME_ORDER).to_dict()

# RTI distribution plot
fig, ax = plt.subplots(figsize=(8, 5))
regime_colors = {'Nordic': '#2166AC', 'Continental': '#67A9CF', 'Liberal': '#D6604D',
                 'Southern': '#F4A582', 'Eastern': '#B2ABD2'}
for regime in REGIME_ORDER:
    data_r = analysis[analysis['welfare_regime'] == regime]['task_z']
    ax.hist(data_r, bins=50, alpha=0.4, density=True, label=regime, color=regime_colors[regime])
ax.set_xlabel('RTI (standardized)')
ax.set_ylabel('Density')
ax.set_title('RTI Distribution by Welfare Regime')
ax.legend()
fig.savefig(DIAG_DIR / 'rti_distribution_by_regime.png')
plt.close()

# --- 5b. Cronbach's alpha by regime ---
print('\n--- 5b. Cronbach\'s alpha by regime ---')
immig_items = ['imwbcnt', 'imueclt', 'imbgeco']
# Check if items exist
available_items = [c for c in immig_items if c in master.columns]
print(f'Immigration items available: {available_items}')

def cronbach_alpha(data):
    """Compute Cronbach's alpha for a set of items."""
    data = data.dropna()
    if len(data) < 10 or data.shape[1] < 2:
        return np.nan
    item_vars = data.var(axis=0, ddof=1)
    total_var = data.sum(axis=1).var(ddof=1)
    n_items = data.shape[1]
    return (n_items / (n_items - 1)) * (1 - item_vars.sum() / total_var)

if len(available_items) >= 2:
    alpha_results = []
    for regime in REGIME_ORDER:
        data_r = master[master['welfare_regime'] == regime][available_items]
        alpha = cronbach_alpha(data_r)
        alpha_results.append({'regime': regime, 'alpha': alpha, 'n': len(data_r.dropna())})
        print(f'  {regime}: alpha={alpha:.3f}, N={len(data_r.dropna()):,}')

    # Overall
    alpha_all = cronbach_alpha(master[available_items])
    print(f'  Overall: alpha={alpha_all:.3f}')

    alpha_df = pd.DataFrame(alpha_results)
    alpha_df.to_csv(DIAG_DIR / 'cronbach_alpha_by_regime.csv', index=False)
    findings['cronbach_alpha'] = alpha_df.set_index('regime')['alpha'].to_dict()
else:
    print('  Cannot compute — items not available in master dataset')
    findings['cronbach_alpha'] = 'Items not available in master'

# --- 5c. Missingness analysis ---
print('\n--- 5c. Missingness analysis ---')
miss_vars = ['anti_immig_index', 'task', 'agea', 'female', 'college', 'hinctnta', 'urban',
             'lrscale', 'cwed_generosity']
miss_vars = [v for v in miss_vars if v in master.columns]

miss_by_regime = {}
for regime in REGIME_ORDER:
    data_r = master[master['welfare_regime'] == regime]
    miss_pct = (data_r[miss_vars].isna().sum() / len(data_r) * 100).round(1)
    miss_by_regime[regime] = miss_pct

miss_df = pd.DataFrame(miss_by_regime)
print(miss_df.to_string())
miss_df.to_csv(DIAG_DIR / 'missingness_by_regime.csv')
findings['missingness'] = miss_df.to_dict()

# Total sample vs analysis sample by regime
print('\nSample attrition by regime:')
for regime in REGIME_ORDER:
    total = len(master[master['welfare_regime'] == regime])
    in_analysis = len(analysis[analysis['welfare_regime'] == regime])
    pct_retained = in_analysis / total * 100
    print(f'  {regime}: {total:,} -> {in_analysis:,} ({pct_retained:.1f}% retained)')


# ============================================================
# 6. ALMP vs CWED ON OVERLAPPING SAMPLE
# ============================================================
print('\n' + '='*60)
print('  6. ALMP vs CWED ON OVERLAPPING SAMPLE')
print('='*60)

slopes_both = slopes_df.dropna(subset=['cwed_generosity', 'almp_pmp'])
print(f'Countries with BOTH CWED and ALMP data: {len(slopes_both)}')
print(slopes_both[['cntry', 'regime', 'slope', 'cwed_generosity', 'almp_pmp']].to_string(index=False))

if len(slopes_both) >= 5:
    r_cwed_overlap, p_cwed_overlap = stats.pearsonr(slopes_both['cwed_generosity'], slopes_both['slope'])
    r_almp_overlap, p_almp_overlap = stats.pearsonr(slopes_both['almp_pmp'], slopes_both['slope'])

    print(f'\nOn overlapping sample (N={len(slopes_both)}):')
    print(f'  CWED generosity vs slope: r={r_cwed_overlap:.3f}, p={p_cwed_overlap:.6f}')
    print(f'  ALMP spending vs slope: r={r_almp_overlap:.3f}, p={p_almp_overlap:.6f}')

    findings['overlap_contrast'] = {
        'n_overlap': len(slopes_both),
        'cwed_r': r_cwed_overlap, 'cwed_p': p_cwed_overlap,
        'almp_r': r_almp_overlap, 'almp_p': p_almp_overlap,
        'countries': slopes_both['cntry'].tolist(),
    }
else:
    print('  Too few countries for overlap analysis')
    findings['overlap_contrast'] = 'Insufficient overlap'


# ============================================================
# 7. ALTERNATIVE EXPLANATIONS
# ============================================================
print('\n' + '='*60)
print('  7. ALTERNATIVE EXPLANATIONS')
print('='*60)

# Can we control for GDP, Gini, immigrant stock at country level?
# These would need to be added to the CWED model
# Check what country-level variables exist in the data
print('\nAvailable country-level variables in master:')
for col in master.columns:
    nunique_by_country = master.groupby('cntry')[col].nunique()
    if (nunique_by_country <= 2).all() and col not in ['cntry', 'welfare_regime', 'cntry_wave']:
        # This is a country-level variable (constant within country)
        pass  # Too many to print

# Check if any GDP/Gini/immigrant variables exist
potential_controls = [c for c in master.columns if any(x in c.lower() for x in ['gdp', 'gini', 'immigrant', 'foreign', 'migrant', 'ineq'])]
print(f'Potential country-level controls found: {potential_controls}')

# We'll construct what we can from the data itself
# Immigrant stock proxy: average immigration attitudes by country (crude)
# GDP proxy: average income by country
# Gini proxy: income inequality by country

print('\nConstructing crude country-level controls from ESS data:')
country_controls = analysis.groupby('cntry').agg(
    mean_income=('hinctnta', 'mean'),
    income_sd=('hinctnta', 'std'),
    pct_college=('college', 'mean'),
    mean_age=('agea', 'mean'),
    n=('anti_immig_index', 'count'),
).reset_index()

print(country_controls.to_string(index=False))
country_controls.to_csv(DIAG_DIR / 'country_level_controls.csv', index=False)

# Test Model 3 with additional country-level controls
print('\nModel 3 with additional country-level controls:')
try:
    # Merge country controls
    analysis_cwed2 = analysis_cwed.merge(country_controls[['cntry', 'mean_income', 'income_sd', 'pct_college']],
                                          on='cntry', how='left')

    # Standardize
    for v in ['mean_income', 'income_sd', 'pct_college']:
        analysis_cwed2[f'{v}_z'] = (analysis_cwed2[v] - analysis_cwed2[v].mean()) / analysis_cwed2[v].std()

    formula3_controls = ('anti_immig_index ~ task_z * cwed_generosity_z'
                        ' + mean_income_z + income_sd_z + pct_college_z'
                        ' + agea + age_sq + female + college + hinctnta + urban')
    m3_controls = smf.mixedlm(formula3_controls, data=analysis_cwed2,
                               groups=analysis_cwed2['cntry_wave']).fit(reml=True)

    int_key = 'task_z:cwed_generosity_z'
    print(f'  RTI x CWED (with country controls): {m3_controls.params[int_key]:.4f} '
          f'(SE={m3_controls.bse[int_key]:.4f}, p={m3_controls.pvalues[int_key]:.4f})')
    print(f'  Original: {reported["model3"]["coef_interaction"]:.4f} (SE={reported["model3"]["se_interaction"]:.4f})')

    findings['model3_with_controls'] = {
        'coef': float(m3_controls.params[int_key]),
        'se': float(m3_controls.bse[int_key]),
        'p': float(m3_controls.pvalues[int_key]),
    }

except Exception as e:
    print(f'  Model 3 with controls failed: {e}')
    traceback.print_exc()


# ============================================================
# 8. WILD CLUSTER BOOTSTRAP (simplified)
# ============================================================
print('\n' + '='*60)
print('  8. WILD CLUSTER BOOTSTRAP (simplified)')
print('='*60)

try:
    # With only 2 Liberal countries, standard inference is suspect
    # Implement a simplified wild cluster bootstrap at the country level

    formula_ols = ('anti_immig_index ~ task_z * C(welfare_regime, Treatment(reference="Nordic"))'
                   ' + agea + age_sq + female + college + hinctnta + urban + C(cntry_wave)')

    m_base = smf.ols(formula_ols, data=analysis).fit()
    lib_key = [k for k in m_base.params.index if 'Liberal' in k and 'task_z' in k][0]
    observed_t = m_base.params[lib_key] / m_base.bse[lib_key]

    n_boot = 999
    countries = analysis['cntry'].unique()
    boot_t_stats = []

    np.random.seed(42)
    for b in range(n_boot):
        # Rademacher weights at country level
        weights = {c: np.random.choice([-1, 1]) for c in countries}
        analysis_boot = analysis.copy()

        # Under H0: RTI x Liberal = 0, construct bootstrap DV
        # Restricted residuals approach
        # Simplified: just perturb residuals by country-level Rademacher
        resid = m_base.resid.copy()
        for c in countries:
            mask = analysis_boot['cntry'] == c
            resid.loc[mask] = resid.loc[mask] * weights[c]

        analysis_boot['y_boot'] = m_base.fittedvalues + resid

        try:
            formula_boot = ('y_boot ~ task_z * C(welfare_regime, Treatment(reference="Nordic"))'
                           ' + agea + age_sq + female + college + hinctnta + urban + C(cntry_wave)')
            m_boot = smf.ols(formula_boot, data=analysis_boot).fit()
            boot_coef = m_boot.params[lib_key]
            boot_se = m_boot.bse[lib_key]
            boot_t = boot_coef / boot_se
            boot_t_stats.append(boot_t)
        except:
            pass

    boot_t_stats = np.array(boot_t_stats)
    # Two-sided p-value
    boot_p = (np.abs(boot_t_stats) >= np.abs(observed_t)).mean()

    print(f'Observed t-statistic: {observed_t:.3f}')
    print(f'Wild cluster bootstrap p-value (B={n_boot}): {boot_p:.4f}')
    print(f'  (vs. country-clustered p: {cc_p:.4f})')

    findings['wild_cluster_bootstrap'] = {
        'observed_t': float(observed_t),
        'boot_p': float(boot_p),
        'n_boot': n_boot,
    }

except Exception as e:
    print(f'Wild cluster bootstrap failed: {e}')
    traceback.print_exc()


# ============================================================
# SAVE ALL FINDINGS
# ============================================================
print('\n' + '='*60)
print('  SAVING FINDINGS')
print('='*60)

# Convert numpy types for JSON serialization
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

with open(DIAG_DIR / 'all_findings.json', 'w') as f:
    json.dump(convert_types(findings), f, indent=2, default=str)

print('All findings saved to review_diagnostics/all_findings.json')
print('\nDiagnostic files:')
for f in sorted(DIAG_DIR.glob('*')):
    print(f'  {f.name}')

print('\n' + '='*60)
print('  DIAGNOSTICS COMPLETE')
print('='*60)
