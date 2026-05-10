"""
Interactive Plotly artifact for the empirical walkthrough.

Builds a single self-contained HTML file that lets Ben toggle between bivariate
per-country OLS slopes and BLUPs from the random-slopes MixedLM, and watch the
CWED correlation move from r=-0.625 to r=-0.855 in front of him. This is the
core pedagogical moment about shrinkage and what BLUPs are doing.

Also includes a per-country hover with the gap between the two estimates.

Run: python analysis/walkthrough_interactive.py
Output: outputs/figures/walkthrough/interactive_blups_vs_bivariate.html
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import patsy
from statsmodels.regression.mixed_linear_model import MixedLM
from scipy import stats as st
import plotly.graph_objects as go

OUT = 'outputs/figures/walkthrough'
os.makedirs(OUT, exist_ok=True)

# ── Load data and fit slopes (both methodologies) ────────────────────────────
print("Loading data...")
df = pd.read_csv('analysis/sorting_mechanism_master_v2.csv', low_memory=False)
df = df.dropna(subset=['task_z', 'anti_immig_index'])
df_c = df.dropna(subset=['cwed_generosity']).copy()
ctrl_cols = ['agea', 'age_sq', 'female', 'college', 'hinctnta', 'urban']

# Bivariate per-country
biv_rows = []
for ctry in sorted(df_c['cntry'].unique()):
    dc = df_c[df_c['cntry'] == ctry][['task_z', 'anti_immig_index', 'cwed_generosity']].dropna()
    if len(dc) < 50:
        continue
    s, _, _, _, se = st.linregress(dc['task_z'], dc['anti_immig_index'])
    biv_rows.append({'cntry': ctry, 'slope_biv': s, 'cwed': dc['cwed_generosity'].iloc[0], 'n': len(dc)})
biv_df = pd.DataFrame(biv_rows)

# BLUPs from MixedLM with controls
print("Fitting random-slopes MixedLM with controls (for BLUPs)...")
formula = 'anti_immig_index ~ task_z + ' + ' + '.join(ctrl_cols)
df_fit = df_c[['task_z', 'anti_immig_index', 'cntry'] + ctrl_cols].dropna()
endog, exog = patsy.dmatrices(formula, data=df_fit, return_type='dataframe')
endog = endog.iloc[:, 0]
groups = df_fit['cntry'].astype(str).tolist()
exog_re = patsy.dmatrix('~task_z', data=df_fit, return_type='dataframe')
m_rs = MixedLM(endog, exog, groups=groups, exog_re=exog_re).fit(reml=True, method='lbfgs')
fixed_slope = m_rs.params['task_z']
re = m_rs.random_effects
blup_rows = [
    {'cntry': c, 'slope_blup': fixed_slope + (vals['task_z'] if 'task_z' in vals else 0.0)}
    for c, vals in re.items()
]
blup_df = pd.DataFrame(blup_rows)

slopes = biv_df.merge(blup_df, on='cntry', how='inner').sort_values('cwed').reset_index(drop=True)
slopes['shrinkage'] = slopes['slope_biv'] - slopes['slope_blup']
print(slopes.to_string(index=False))

# Headline correlations
r_biv, p_biv = st.pearsonr(slopes['cwed'], slopes['slope_biv'])
r_blup, p_blup = st.pearsonr(slopes['cwed'], slopes['slope_blup'])
print(f"\nBivariate: r={r_biv:.3f}, p={p_biv:.4f}")
print(f"BLUPs:     r={r_blup:.3f}, p={p_blup:.4f}")

# ── Build interactive figure ─────────────────────────────────────────────────
fig = go.Figure()

xs_line = np.linspace(slopes['cwed'].min() - 1, slopes['cwed'].max() + 1, 100)

# ── Bivariate trace ──
fit_b = st.linregress(slopes['cwed'], slopes['slope_biv'])
hover_biv = [
    f"<b>{r['cntry']}</b><br>CWED: {r['cwed']:.2f}<br>"
    f"Bivariate slope: {r['slope_biv']:.3f}<br>BLUP slope: {r['slope_blup']:.3f}<br>"
    f"Shrinkage: {r['shrinkage']:+.3f}<br>N obs: {r['n']:,}"
    for _, r in slopes.iterrows()
]
fig.add_trace(go.Scatter(
    x=slopes['cwed'], y=slopes['slope_biv'],
    mode='markers+text', name='Bivariate slopes',
    text=slopes['cntry'], textposition='top right', textfont=dict(size=10),
    marker=dict(size=12, color='#888', line=dict(color='white', width=1)),
    hovertemplate='%{customdata}<extra></extra>', customdata=hover_biv,
    visible=True,
))
fig.add_trace(go.Scatter(
    x=xs_line, y=fit_b.intercept + fit_b.slope * xs_line,
    mode='lines', name=f'OLS fit (r = {r_biv:.3f}, p = {p_biv:.4f})',
    line=dict(color='#888', width=2.5, dash='solid'),
    hoverinfo='skip',
    visible=True,
))

# ── BLUPs trace ──
fit_p = st.linregress(slopes['cwed'], slopes['slope_blup'])
fig.add_trace(go.Scatter(
    x=slopes['cwed'], y=slopes['slope_blup'],
    mode='markers+text', name='BLUP slopes',
    text=slopes['cntry'], textposition='top right', textfont=dict(size=10),
    marker=dict(size=12, color='#2c3e8e', line=dict(color='white', width=1)),
    hovertemplate='%{customdata}<extra></extra>', customdata=hover_biv,
    visible=False,
))
fig.add_trace(go.Scatter(
    x=xs_line, y=fit_p.intercept + fit_p.slope * xs_line,
    mode='lines', name=f'OLS fit (r = {r_blup:.3f}, p = {p_blup:.4f})',
    line=dict(color='#2c3e8e', width=2.5, dash='solid'),
    hoverinfo='skip',
    visible=False,
))

# ── BOTH trace (overlay) ──
fig.add_trace(go.Scatter(
    x=slopes['cwed'], y=slopes['slope_biv'],
    mode='markers', name='Bivariate', marker=dict(size=11, color='#888', symbol='circle-open'),
    hovertemplate='%{customdata}<extra></extra>', customdata=hover_biv,
    visible=False,
))
fig.add_trace(go.Scatter(
    x=slopes['cwed'], y=slopes['slope_blup'],
    mode='markers+text', name='BLUPs',
    text=slopes['cntry'], textposition='top right', textfont=dict(size=10),
    marker=dict(size=12, color='#2c3e8e'),
    hovertemplate='%{customdata}<extra></extra>', customdata=hover_biv,
    visible=False,
))
# Connecting lines showing shrinkage per country
for _, row in slopes.iterrows():
    fig.add_trace(go.Scatter(
        x=[row['cwed'], row['cwed']],
        y=[row['slope_biv'], row['slope_blup']],
        mode='lines', line=dict(color='gray', width=1, dash='dot'),
        hoverinfo='skip', showlegend=False, visible=False,
    ))
# Both fit lines
fig.add_trace(go.Scatter(
    x=xs_line, y=fit_b.intercept + fit_b.slope * xs_line,
    mode='lines', name=f'Bivariate fit (r = {r_biv:.3f})',
    line=dict(color='#888', width=2),
    hoverinfo='skip', visible=False,
))
fig.add_trace(go.Scatter(
    x=xs_line, y=fit_p.intercept + fit_p.slope * xs_line,
    mode='lines', name=f'BLUPs fit (r = {r_blup:.3f})',
    line=dict(color='#2c3e8e', width=2.5),
    hoverinfo='skip', visible=False,
))

# Visibility patterns
n_traces = len(fig.data)
n_country_lines = len(slopes)
# Indices: [biv_pts, biv_line, blup_pts, blup_line, both_biv_pts, both_blup_pts, *country_lines, both_biv_line, both_blup_line]
biv_visible = [True, True, False, False, False, False] + [False] * n_country_lines + [False, False]
blup_visible = [False, False, True, True, False, False] + [False] * n_country_lines + [False, False]
both_visible = [False, False, False, False, True, True] + [True] * n_country_lines + [True, True]

fig.update_layout(
    title=dict(
        text='<b>BLUPs vs bivariate per-country slopes — same data, different methodology, different correlation</b><br>'
             '<span style="font-size:13px;color:#555">Toggle to feel what shrinkage does to the §V.D headline finding.</span>',
        x=0.02, xanchor='left',
    ),
    xaxis_title='CWED total generosity (country level)',
    yaxis_title='Per-country slope of anti-immigration on RTI',
    height=620, width=900,
    plot_bgcolor='white',
    font=dict(family='Georgia, serif', size=13),
    legend=dict(x=0.02, y=0.02, xanchor='left', yanchor='bottom',
                bgcolor='rgba(255,255,255,0.85)', bordercolor='lightgray', borderwidth=1),
    updatemenus=[dict(
        type='buttons', direction='right', x=0.5, y=1.13, xanchor='center',
        buttons=[
            dict(label='Bivariate (no controls, no shrinkage)',
                 method='update', args=[{'visible': biv_visible}]),
            dict(label='BLUPs (controls + shrinkage) ← published',
                 method='update', args=[{'visible': blup_visible}]),
            dict(label='Both, side by side',
                 method='update', args=[{'visible': both_visible}]),
        ],
    )],
    annotations=[
        dict(x=0.99, y=0.97, xref='paper', yref='paper', xanchor='right', yanchor='top',
             text='<i>Hover any point to see both slope estimates and the shrinkage gap for that country.</i>',
             showarrow=False, font=dict(size=11, color='#666'), bgcolor='rgba(255,255,255,0.85)',
             bordercolor='lightgray', borderwidth=1, borderpad=4),
    ],
)

fig.update_xaxes(showgrid=True, gridcolor='#eee', zeroline=False)
fig.update_yaxes(showgrid=True, gridcolor='#eee', zeroline=False)

out_path = f'{OUT}/interactive_blups_vs_bivariate.html'
fig.write_html(out_path, include_plotlyjs='cdn')
print(f"\nSaved: {out_path}  ({os.path.getsize(out_path)/1024:.0f} KB)")
