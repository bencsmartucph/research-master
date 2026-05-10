"""Fix Plots A and B — the grid layout bug with 5 regimes."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

ROOT = Path(r'C:\Users\PKF715\Documents\claude_repos\Research_Master')
FIG_DIR = ROOT / 'outputs' / 'figures'

sns.set_theme(style='whitegrid', font_scale=1.1)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['figure.dpi'] = 150

# Load the master dataset we just saved
ess = pd.read_csv(ROOT / 'analysis' / 'sorting_mechanism_master.csv')
print(f'Loaded master dataset: {len(ess):,} rows')

regime_colors = {'Nordic': '#2196F3', 'Continental': '#FF9800',
                 'Liberal': '#F44336', 'Southern': '#4CAF50',
                 'Eastern': '#9C27B0'}

plot_regimes = ['Nordic', 'Continental', 'Liberal', 'Southern', 'Eastern']

# ============================================================
# PLOT A: RTI vs anti-immigration by regime
# ============================================================
plot_df = ess[
    ess['welfare_regime'].isin(plot_regimes) &
    ess['task'].notna() &
    ess['anti_immig_index'].notna()
].copy()

regimes_with_data = [r for r in plot_regimes
                     if (plot_df['welfare_regime'] == r).sum() >= 100]
n_regimes = len(regimes_with_data)
print(f'Plot A: {len(plot_df):,} obs, {n_regimes} regimes with data')

# Use 2x3 grid for 5 regimes
nrows, ncols = 2, 3
fig, axes = plt.subplots(nrows, ncols, figsize=(18, 10), sharey=True)
axes_list = axes.flatten().tolist()

for idx, regime in enumerate(regimes_with_data):
    ax = axes_list[idx]
    rdf = plot_df[plot_df['welfare_regime'] == regime].copy()

    n_bins = min(20, max(5, len(rdf) // 100))
    rdf['rti_bin'] = pd.qcut(rdf['task'], q=n_bins, duplicates='drop')
    binned = rdf.groupby('rti_bin', observed=True).agg(
        rti_mean=('task', 'mean'),
        dv_mean=('anti_immig_index', 'mean'),
        dv_se=('anti_immig_index', lambda x: x.std() / np.sqrt(len(x))),
    ).reset_index()

    color = regime_colors.get(regime, 'gray')
    ax.errorbar(binned['rti_mean'], binned['dv_mean'],
                yerr=1.96 * binned['dv_se'], fmt='o', markersize=5,
                capsize=2, alpha=0.8, color=color)

    valid = rdf[['task', 'anti_immig_index']].dropna()
    slope, intercept, r_val, p_val, se = stats.linregress(
        valid['task'], valid['anti_immig_index'])
    x_range = np.linspace(rdf['task'].min(), rdf['task'].max(), 100)
    ax.plot(x_range, intercept + slope * x_range, '--', color=color, alpha=0.7,
            label=f'slope={slope:.3f} (p={p_val:.3f})')

    ax.set_xlabel('RTI Score (automation exposure)')
    ax.set_ylabel('Anti-immigration index (0-10)')
    ax.set_title(f'{regime} (N={len(rdf):,})')
    ax.legend(fontsize=9)

    print(f'  {regime}: slope={slope:.4f}, p={p_val:.4f}, N={len(valid):,}')

# Hide unused subplots
for idx in range(n_regimes, nrows * ncols):
    axes_list[idx].set_visible(False)

plt.tight_layout()
plt.savefig(FIG_DIR / 'fig2_rti_vs_antiimmig_by_regime.pdf', bbox_inches='tight')
plt.savefig(FIG_DIR / 'fig2_rti_vs_antiimmig_by_regime.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved Plot A: fig2_rti_vs_antiimmig_by_regime.pdf + .png')

# ============================================================
# PLOT B: RTI vs redistribution by regime
# ============================================================
plot_df2 = ess[
    ess['welfare_regime'].isin(plot_regimes) &
    ess['task'].notna() &
    ess['redist_support'].notna()
].copy()

regimes_with_data_b = [r for r in plot_regimes
                       if (plot_df2['welfare_regime'] == r).sum() >= 100]
n_reg_b = len(regimes_with_data_b)
print(f'\nPlot B: {len(plot_df2):,} obs, {n_reg_b} regimes with data')

fig, axes = plt.subplots(nrows, ncols, figsize=(18, 10), sharey=True)
axes_list = axes.flatten().tolist()

for idx, regime in enumerate(regimes_with_data_b):
    ax = axes_list[idx]
    rdf = plot_df2[plot_df2['welfare_regime'] == regime].copy()

    n_bins = min(20, max(5, len(rdf) // 100))
    rdf['rti_bin'] = pd.qcut(rdf['task'], q=n_bins, duplicates='drop')
    binned = rdf.groupby('rti_bin', observed=True).agg(
        rti_mean=('task', 'mean'),
        dv_mean=('redist_support', 'mean'),
        dv_se=('redist_support', lambda x: x.std() / np.sqrt(len(x))),
    ).reset_index()

    color = regime_colors.get(regime, 'gray')
    ax.errorbar(binned['rti_mean'], binned['dv_mean'],
                yerr=1.96 * binned['dv_se'], fmt='o', markersize=5,
                capsize=2, alpha=0.8, color=color)

    valid = rdf[['task', 'redist_support']].dropna()
    slope, intercept, r_val, p_val, se = stats.linregress(
        valid['task'], valid['redist_support'])
    x_range = np.linspace(rdf['task'].min(), rdf['task'].max(), 100)
    ax.plot(x_range, intercept + slope * x_range, '--', color=color, alpha=0.7,
            label=f'slope={slope:.3f} (p={p_val:.3f})')

    ax.set_xlabel('RTI Score (automation exposure)')
    ax.set_ylabel('Redistribution support (1-5)')
    ax.set_title(f'{regime} (N={len(rdf):,})')
    ax.legend(fontsize=9)

    print(f'  {regime}: slope={slope:.4f}, p={p_val:.4f}, N={len(valid):,}')

for idx in range(n_reg_b, nrows * ncols):
    axes_list[idx].set_visible(False)

plt.tight_layout()
plt.savefig(FIG_DIR / 'fig4_rti_vs_redistribution_by_regime.pdf', bbox_inches='tight')
plt.savefig(FIG_DIR / 'fig4_rti_vs_redistribution_by_regime.png', bbox_inches='tight', dpi=150)
plt.close()
print('Saved Plot B: fig4_rti_vs_redistribution_by_regime.pdf + .png')

print('\nDone! Both critical plots saved.')
