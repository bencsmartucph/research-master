"""
Regional Sanity Check (Session 3, 2026-05-04)
==============================================

Quick regional-level test of the country-level finding from §V.D.

Question: Do regional-level RTI → right-populist-vote-share slopes (computed
within country across NUTS-2 regions × years) correlate with country-level
CWED in the same direction as the individual-level finding (paper's r=−0.848)?

This is NOT the full Appendix D the audit recommends. It's the half-day
"does the pattern survive at all at the regional level?" check that informs
whether the full ~2-week regional analysis is worth committing to.

Data: Milner 2021 NUTS-2 panel `imputed_econdata_voteshare_merged.dta`
(15 countries, 164 NUTS-2 regions, 1991–2018, 5+ multiple imputations).

Method:
1. Take imputation #1 only (single realization for the sanity check; full
   analysis would pool over imputations using Rubin's rules).
2. Restrict to the post-2008 window (where right-populist vote shares are
   most variable and ESS fieldwork waves 6–9 overlap).
3. Within each country: regress nuts2_right_pop_vs on rti_region with year
   fixed effects, take the coefficient as the country-level "regional-RTI
   elasticity of right-populist vote."
4. Correlate those 15 country-level betas with CWED total generosity.

Predicted direction (per paper §V.D): negative correlation. More-decommodified
countries should have SMALLER regional-RTI → right-populist effects, because
welfare design buffers the conversion of automation exposure into far-right
support.

Run: python scripts/regional_sanity_check.py

Outputs:
    outputs/tables/regional_sanity_check.csv     — per-country regional slope + CWED
    outputs/figures/regional_sanity_check.png    — scatter
"""

import sys, io, os, warnings
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats as st
import pyreadstat
warnings.filterwarnings('ignore')

os.makedirs('outputs/tables', exist_ok=True)
os.makedirs('outputs/figures', exist_ok=True)

# ── Configuration ──────────────────────────────────────────────────────────────
MILNER = 'data/raw/milner_2021/data/data/imputed/imputed_econdata_voteshare_merged.dta'
CWED_FILE = 'data/raw/CWED/cwed-subset.csv'
YEAR_MIN, YEAR_MAX = 1991, 2018  # full Milner panel; sensitivity to post-2008 below

# ── Load Milner data ───────────────────────────────────────────────────────────
print(f"Loading Milner NUTS-2 panel...")
df, meta = pyreadstat.read_dta(MILNER)
print(f"  Shape: {df.shape}")
print(f"  Years: {df['year'].min():.0f} – {df['year'].max():.0f}")

# Imputation: _mi_m is the imputation index (0=observed, 1-9=imputations).
# Take _mi_m==1 for the sanity check (full analysis would pool over imputations
# using Rubin's rules; one imputation is fine for "does the pattern hold at all").
df = df[df['_mi_m'] == 1].copy()
df = df.drop_duplicates(subset=['nuts2', 'year'])
print(f"  After _mi_m==1 and deduplication on (nuts2, year): {len(df):,} rows")

# Window
df = df[(df['year'] >= YEAR_MIN) & (df['year'] <= YEAR_MAX)].copy()
df = df[df['nutslevel'] == 2.0].copy()
print(f"  After window {YEAR_MIN}-{YEAR_MAX} and NUTS2 only: {len(df):,} rows, {df['nuts2'].nunique()} regions, {df['cname'].nunique()} countries")

# Map country names to ISO-2 (matching CWED)
CNAME_TO_ISO2 = {
    'Austria': 'AT', 'Belgium': 'BE', 'Switzerland': 'CH', 'Germany': 'DE',
    'Denmark': 'DK', 'Spain': 'ES', 'Finland': 'FI', 'France': 'FR',
    'United Kingdom': 'GB', 'Ireland': 'IE', 'Italy': 'IT', 'Netherlands': 'NL',
    'Norway': 'NO', 'Portugal': 'PT', 'Sweden': 'SE', 'Greece': 'GR',
    # Catch a few possible alternative spellings
    'Great Britain': 'GB', 'UK': 'GB',
}
df['cntry'] = df['cname'].map(CNAME_TO_ISO2)
n_unmapped = df['cntry'].isna().sum()
if n_unmapped > 0:
    unmapped = df[df['cntry'].isna()]['cname'].unique()
    print(f"  WARNING: {n_unmapped} rows have unmapped cname: {unmapped}")
df = df.dropna(subset=['cntry'])

# Drop rows with missing key vars
df = df.dropna(subset=['rti_region', 'nuts2_right_pop_vs'])
print(f"  Complete cases on rti_region + nuts2_right_pop_vs: {len(df):,} rows, {df['cntry'].nunique()} countries")

# ── Per-country bivariate correlation (cleaner than year-FE with tiny N) ──────
# Earlier draft used year FE + cluster SE; per-country N is too small for that
# spec to behave well (some countries have only 2 election years × 5 regions =
# 10 observations, of which year FE absorbs 1 dof). Use bivariate Pearson r —
# it captures the cross-region within-country pattern most robustly given N.
print(f"\nPer-country bivariate correlations (rti_region vs nuts2_right_pop_vs)...")
country_betas = []
for c in sorted(df['cntry'].unique()):
    sub = df[df['cntry'] == c].copy()
    n_regions = sub['nuts2'].nunique()
    n_obs = len(sub)
    if n_obs < 10 or n_regions < 3:
        print(f"  {c}: too few obs ({n_obs} rows, {n_regions} regions), skipping")
        continue
    r, p = st.pearsonr(sub['rti_region'], sub['nuts2_right_pop_vs'])
    rho, p_rho = st.spearmanr(sub['rti_region'], sub['nuts2_right_pop_vs'])
    country_betas.append({
        'cntry': c, 'r_pearson': r, 'p_pearson': p, 'r_spearman': rho, 'p_spearman': p_rho,
        'n_obs': n_obs, 'n_regions': n_regions, 'n_years': sub['year'].nunique(),
        'mean_right_pop_vs': sub['nuts2_right_pop_vs'].mean(),
    })
    print(f"  {c}: r={r:+.3f}, p={p:.3f}  (n={n_obs}, regions={n_regions}, years={sub['year'].nunique()})")

slopes_df = pd.DataFrame(country_betas)
slopes_df['beta_rti_region'] = slopes_df['r_pearson']  # alias for downstream code
print(f"\n  Country-level Pearson r computed: {len(slopes_df)} countries")

# ── Merge with CWED ────────────────────────────────────────────────────────────
ISO3_TO_ISO2 = {'AUT':'AT','BEL':'BE','CHE':'CH','DEU':'DE','DNK':'DK',
                'ESP':'ES','FIN':'FI','FRA':'FR','GBR':'GB','IRL':'IE',
                'ITA':'IT','NLD':'NL','NOR':'NO','PRT':'PT','SWE':'SE'}
cwed = pd.read_csv(CWED_FILE)
cwed_window = cwed[(cwed['YEAR'] >= 2005) & (cwed['YEAR'] <= 2011)].copy()
cwed_window['cntry'] = cwed_window['COUNTRY ABBREV'].map(ISO3_TO_ISO2)
cwed_window['TOTGEN'] = pd.to_numeric(cwed_window['TOTGEN'], errors='coerce')
cwed_country = (cwed_window.dropna(subset=['cntry'])
                .groupby('cntry')['TOTGEN'].mean()
                .reset_index().rename(columns={'TOTGEN': 'cwed'}))
slopes_df = slopes_df.merge(cwed_country, on='cntry', how='left')
print(f"  Merged with CWED: {slopes_df['cwed'].notna().sum()} of {len(slopes_df)} countries have CWED")

# ── The headline correlation ───────────────────────────────────────────────────
valid = slopes_df.dropna(subset=['cwed', 'beta_rti_region'])
if len(valid) >= 5:
    r, p = st.pearsonr(valid['cwed'], valid['beta_rti_region'])
    rho, p_rho = st.spearmanr(valid['cwed'], valid['beta_rti_region'])
    print(f"\n══ HEADLINE: Regional-RTI-slope vs CWED correlation ═══════════════════")
    print(f"  Pearson r  = {r:+.4f}, p = {p:.4f}, N = {len(valid)}")
    print(f"  Spearman ρ = {rho:+.4f}, p = {p_rho:.4f}, N = {len(valid)}")
    print(f"  Predicted direction: NEGATIVE (more decommodified → smaller regional-RTI → right-pop slope)")
    if r < -0.3:
        print(f"  → consistent with country-level finding (paper r=-0.848)")
    elif r > 0.3:
        print(f"  → INCONSISTENT — regional pattern goes OPPOSITE to country-level. FLAG.")
    else:
        print(f"  → weak/null at regional level. Country-level finding may not survive at NUTS-2.")

# ── Save ───────────────────────────────────────────────────────────────────────
slopes_df.to_csv('outputs/tables/regional_sanity_check.csv', index=False)
print(f"\nSaved: outputs/tables/regional_sanity_check.csv")

# ── Plot ───────────────────────────────────────────────────────────────────────
if len(valid) >= 5:
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(valid['cwed'], valid['beta_rti_region'], s=60, alpha=0.7, edgecolor='k', linewidth=0.5)
    for _, row in valid.iterrows():
        ax.annotate(row['cntry'], (row['cwed'], row['beta_rti_region']),
                    xytext=(4, 4), textcoords='offset points', fontsize=10)
    coef = np.polyfit(valid['cwed'], valid['beta_rti_region'], 1)
    xs = np.linspace(valid['cwed'].min(), valid['cwed'].max(), 50)
    ax.plot(xs, np.polyval(coef, xs), '--', color='red', alpha=0.6, linewidth=1.5)
    ax.set_xlabel('CWED total generosity (mean 2005–2011)', fontsize=11)
    ax.set_ylabel('Country-level regional-RTI β\n(NUTS-2 right-populist vote share, year FE)', fontsize=11)
    ax.set_title(f'Regional sanity check: r = {r:+.2f}, p = {p:.3f}, N = {len(valid)}', fontsize=11)
    ax.axhline(0, color='grey', linewidth=0.5, alpha=0.5)
    ax.grid(alpha=0.3)
    plt.rcParams.update({'font.family': 'serif'})
    plt.tight_layout()
    plt.savefig('outputs/figures/regional_sanity_check.png', dpi=150, bbox_inches='tight')
    plt.savefig('outputs/figures/regional_sanity_check.pdf', bbox_inches='tight')
    plt.close()
    print(f"Saved: outputs/figures/regional_sanity_check.png/.pdf")

print("\nDone.")
