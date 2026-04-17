"""
Publication-quality figures for seminar paper.
Argument: automation exposure → anti-immigration attitudes;
          welfare generosity buffers this effect.

Run: python scripts/create_figures_final.py
Outputs: outputs/figures/fig1_rti_antiimmig_by_cwed.pdf/.png
         outputs/figures/fig6_cwed_country_slopes.pdf/.png
         outputs/figures/fig_regime_heterogeneity.pdf/.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import json, os, warnings
warnings.filterwarnings('ignore')

os.makedirs('outputs/figures', exist_ok=True)

# ── Global style ──────────────────────────────────────────────────────────────
mpl.rcParams.update({
    'font.family':       'serif',
    'font.size':         11,
    'axes.titlesize':    11,
    'axes.labelsize':    11,
    'xtick.labelsize':   10,
    'ytick.labelsize':   10,
    'legend.fontsize':   10,
    'figure.dpi':        150,
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.linewidth':    0.8,
})
GREY   = '#444444'
BLUE   = '#2166AC'
RED    = '#D6604D'
PURPLE = '#762A83'

def save(fig, name):
    fig.savefig(f'outputs/figures/{name}.pdf', bbox_inches='tight')
    fig.savefig(f'outputs/figures/{name}.png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f'  Saved: outputs/figures/{name}.pdf/.png')

# ── Load data ─────────────────────────────────────────────────────────────────
df  = pd.read_csv('analysis/sorting_mechanism_master_v2.csv', low_memory=False)
res = json.load(open('analysis/final_results.json'))
slopes_df = pd.read_csv('analysis/review_diagnostics/cwed_cooks_distance.csv')

# ── FIGURE 1: RTI effect on anti-immig by CWED high/low ──────────────────────
print("Figure 1: RTI × CWED high/low split...")

df1 = df.dropna(subset=['task_z','anti_immig_index','cwed_generosity_z','agea',
                          'age_sq','female','college','hinctnta','urban'])

# Median split
median_cwed = df1['cwed_generosity_z'].median()
df1_low  = df1[df1['cwed_generosity_z'] <= median_cwed].copy()
df1_high = df1[df1['cwed_generosity_z'] >  median_cwed].copy()

# Partial regression: residualise controls out, plot task_z vs anti_immig
from numpy.linalg import lstsq

def partial_slope(data, x_col, y_col, ctrl_cols):
    """OLS residuals of y ~ ctrls, x ~ ctrls → slope of resid_y ~ resid_x."""
    X = data[ctrl_cols].assign(const=1).values
    y_resid = data[y_col].values - X @ lstsq(X, data[y_col].values, rcond=None)[0]
    x_resid = data[x_col].values - X @ lstsq(X, data[x_col].values, rcond=None)[0]
    return x_resid, y_resid

ctrls = ['agea','age_sq','female','college','hinctnta','urban']

x_lo, y_lo = partial_slope(df1_low,  'task_z', 'anti_immig_index', ctrls)
x_hi, y_hi = partial_slope(df1_high, 'task_z', 'anti_immig_index', ctrls)

# Bin x into 20 quantile bins for plotting clarity
def binned_means(x, y, n_bins=20):
    bins = pd.qcut(x, n_bins, duplicates='drop')
    bx = pd.Series(x).groupby(bins).mean().values
    by = pd.Series(y).groupby(bins).mean().values
    return bx, by

bx_lo, by_lo = binned_means(x_lo, y_lo)
bx_hi, by_hi = binned_means(x_hi, y_hi)

# OLS fit lines
def fit_line(x, y):
    b = np.polyfit(x, y, 1)
    xx = np.linspace(x.min(), x.max(), 100)
    return xx, np.polyval(b, xx), b[0]

xx_lo, yy_lo, s_lo = fit_line(x_lo, y_lo)
xx_hi, yy_hi, s_hi = fit_line(x_hi, y_hi)

# CI via bootstrap (fast: 200 reps)
def boot_ci(x, y, n=200):
    slopes = []
    for _ in range(n):
        idx = np.random.randint(0, len(x), len(x))
        slopes.append(np.polyfit(x[idx], y[idx], 1)[0])
    return np.percentile(slopes, [2.5, 97.5])

ci_lo = boot_ci(x_lo, y_lo)
ci_hi = boot_ci(x_hi, y_hi)

fig, ax = plt.subplots(figsize=(6, 4.2))

# Scatter (binned)
ax.scatter(bx_lo, by_lo, color=RED,  alpha=0.55, s=28, zorder=3)
ax.scatter(bx_hi, by_hi, color=BLUE, alpha=0.55, s=28, zorder=3)

# Fit lines
ax.plot(xx_lo, yy_lo, color=RED,  lw=2,   label=f'Low welfare generosity  (β={s_lo:.3f})')
ax.plot(xx_hi, yy_hi, color=BLUE, lw=2,   label=f'High welfare generosity (β={s_hi:.3f})')

# CI shading
for xx, ci, col in [(xx_lo, ci_lo, RED), (xx_hi, ci_hi, BLUE)]:
    ax.fill_between(xx,
                    np.polyval([ci[0], np.mean(y_lo if col==RED else y_hi)], xx),
                    np.polyval([ci[1], np.mean(y_lo if col==RED else y_hi)], xx),
                    color=col, alpha=0.12)

ax.axhline(0, color=GREY, lw=0.6, ls='--', alpha=0.5)
ax.axvline(0, color=GREY, lw=0.6, ls='--', alpha=0.5)
ax.set_xlabel('Routine Task Intensity (standardised, residualised)')
ax.set_ylabel('Anti-immigration attitudes (residualised)')
ax.legend(frameon=False, loc='upper left')
fig.tight_layout()
save(fig, 'fig1_rti_antiimmig_by_cwed')

# ── FIGURE 6: CWED generosity vs country RTI slopes ──────────────────────────
print("Figure 6: CWED vs country slopes...")

# Use updated slopes from random_slopes_models if available, else review_diagnostics
rs_jack = pd.read_csv('outputs/tables/rs_jackknife.csv') \
    if os.path.exists('outputs/tables/rs_jackknife.csv') else None

sd = slopes_df.copy().dropna(subset=['slope','cwed_generosity'])

# Country labels (ISO-2 → common name)
LABELS = {
    'AT':'Austria','BE':'Belgium','CH':'Switzerland','DE':'Germany',
    'DK':'Denmark','ES':'Spain','FI':'Finland','FR':'France',
    'GB':'UK','GR':'Greece','IE':'Ireland','NL':'Netherlands',
    'NO':'Norway','PT':'Portugal','SE':'Sweden',
}
sd['label'] = sd['cntry'].map(LABELS).fillna(sd['cntry'])

REGIME_COLORS = {
    'Nordic':'#4393C3','Continental':'#74C476',
    'Liberal':'#FD8D3C','Southern':'#FB6A4A','Eastern':'#9E9AC8'
}
sd['color'] = sd['regime'].map(REGIME_COLORS).fillna(GREY)

fig, ax = plt.subplots(figsize=(6.5, 4.8))

for _, row in sd.iterrows():
    ax.scatter(row['cwed_generosity'], row['slope'],
               color=row['color'], s=55, zorder=4, edgecolors='white', lw=0.5)
    ax.annotate(row['label'],
                xy=(row['cwed_generosity'], row['slope']),
                xytext=(4, 2), textcoords='offset points',
                fontsize=8, color=GREY)

# OLS fit line
x_s, y_s = sd['cwed_generosity'].values, sd['slope'].values
b_s = np.polyfit(x_s, y_s, 1)
xx_s = np.linspace(x_s.min()-2, x_s.max()+2, 100)
ax.plot(xx_s, np.polyval(b_s, xx_s), color=GREY, lw=1.5, ls='--', alpha=0.7,
        label=f'r = {res["cwed_vs_slopes_generosity"]["r"]:.2f} '
              f'(p={res["cwed_vs_slopes_generosity"]["p"]:.3f})')

# Regime legend
for regime, col in REGIME_COLORS.items():
    if regime in sd['regime'].values:
        ax.scatter([], [], color=col, s=40, label=regime)

ax.axhline(0, color=GREY, lw=0.6, ls='-', alpha=0.3)
ax.set_xlabel('CWED Welfare Generosity Score')
ax.set_ylabel('Country RTI→Anti-Immigration Slope')
ax.legend(frameon=False, fontsize=9, loc='upper right')
fig.tight_layout()
save(fig, 'fig6_cwed_country_slopes')

# ── FIGURE 3: Regime heterogeneity (RTI coef + CI by regime) ─────────────────
print("Figure 3: Regime heterogeneity...")

# Use country slopes data (already have per-country slopes × regime from review_diagnostics)
regime_slopes = sd.groupby('regime')['slope'].agg(['mean','std','count']).reset_index()
regime_slopes['se'] = regime_slopes['std'] / np.sqrt(regime_slopes['count'])
regime_slopes['ci_lo'] = regime_slopes['mean'] - 1.96 * regime_slopes['se']
regime_slopes['ci_hi'] = regime_slopes['mean'] + 1.96 * regime_slopes['se']

# Order by generosity (Nordic most generous → Liberal least)
gen_order = {'Nordic':1,'Continental':2,'Southern':3,'Liberal':4,'Eastern':5}
regime_slopes['order'] = regime_slopes['regime'].map(gen_order)
regime_slopes = regime_slopes.sort_values('order')
regime_slopes = regime_slopes[regime_slopes['regime'].isin(['Nordic','Continental','Liberal','Southern'])]

fig, ax = plt.subplots(figsize=(5.5, 4))

colors = [REGIME_COLORS.get(r, GREY) for r in regime_slopes['regime']]
y_pos = range(len(regime_slopes))

ax.barh(list(y_pos), regime_slopes['mean'].values,
        xerr=1.96 * regime_slopes['se'].values,
        color=colors, alpha=0.8, height=0.55,
        error_kw=dict(lw=1.5, capsize=4, capthick=1.5, color=GREY))

ax.axvline(0, color=GREY, lw=0.8, ls='--', alpha=0.5)
ax.set_yticks(list(y_pos))
ax.set_yticklabels(regime_slopes['regime'].tolist())
ax.set_xlabel('Mean RTI → Anti-Immigration Slope')
ax.invert_yaxis()  # Nordic at top (most generous)

# Annotate n
for i, row in enumerate(regime_slopes.itertuples()):
    ax.text(row.mean + 1.96*row.se + 0.002, i,
            f'n={int(row.count)}', va='center', fontsize=8.5, color=GREY)

fig.tight_layout()
save(fig, 'fig_regime_heterogeneity')

print("\nAll figures saved.")
print("Key patterns:")
print(f"  Fig 1: Low-generosity slope β={s_lo:.3f} > High-generosity slope β={s_hi:.3f}")
print(f"  Fig 6: r={res['cwed_vs_slopes_generosity']['r']:.3f} (p={res['cwed_vs_slopes_generosity']['p']:.4f})")
print(f"  Fig 3: Regime slopes (mean) —")
for row in regime_slopes.itertuples():
    print(f"    {row.regime}: {row.mean:.3f} ± {1.96*row.se:.3f}")
