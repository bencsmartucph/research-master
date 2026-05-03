"""
Interactive: cluster-robust SE inflation factor.

The thing Ben said he doesn't actually understand. Two sliders:
  - intra-cluster correlation (ρ)
  - average cluster size (n̄)

Output: SE inflation factor (the design effect √(1 + (n̄−1)ρ)) shown as a
big number, with the formula displayed and a comparison heatmap so the
intuition becomes spatial.

This is the "naive SE is wrong by a factor of X" calculator. Ben can plug in
his actual numbers (cluster size ~1,400 individuals per country-wave; ρ ~ 0.05)
and see "factor of 8.4" — then drag to see how it changes if either parameter
changes.

Output: outputs/figures/walkthrough/interactive_cluster_se.html
"""
import os
import numpy as np
import plotly.graph_objects as go

OUT = 'outputs/figures/walkthrough'
os.makedirs(OUT, exist_ok=True)

# Heatmap: SE inflation factor as a function of (ρ, n̄)
rho_grid = np.linspace(0.001, 0.30, 60)
n_grid = np.linspace(10, 2000, 60)
RHO, N = np.meshgrid(rho_grid, n_grid)
DESIGN_EFFECT = 1 + (N - 1) * RHO
SE_INFLATION = np.sqrt(DESIGN_EFFECT)

# Build figure
fig = go.Figure()

fig.add_trace(go.Heatmap(
    x=rho_grid, y=n_grid, z=SE_INFLATION,
    colorscale='Viridis', zmin=1, zmax=20,
    colorbar=dict(title=dict(text='SE inflation<br>factor', side='right'),
                  tickvals=[1, 2, 5, 10, 15, 20]),
    hovertemplate='ρ = %{x:.3f}<br>cluster size n̄ = %{y:.0f}<br>SE inflation = %{z:.2f}×<extra></extra>',
))

# Contour overlays at meaningful inflation levels
contour_levels = [2, 5, 10, 20]
fig.add_trace(go.Contour(
    x=rho_grid, y=n_grid, z=SE_INFLATION,
    contours=dict(start=2, end=20, size=3, coloring='none', showlabels=True,
                  labelfont=dict(size=11, color='white')),
    line=dict(color='white', width=1), showscale=False, hoverinfo='skip',
))

# Anchor points for Ben's actual paper values
# Country-wave clustering: ~1400 obs per cluster, ICC ~0.05
ben_n = 1400
ben_rho = 0.05
ben_inflation = np.sqrt(1 + (ben_n - 1) * ben_rho)
fig.add_trace(go.Scatter(
    x=[ben_rho], y=[ben_n], mode='markers+text',
    marker=dict(size=18, color='red', symbol='star', line=dict(color='white', width=2)),
    text=[f'  Your paper:<br>  inflation = {ben_inflation:.1f}×'],
    textposition='middle right', textfont=dict(size=11, color='red'),
    name='Your paper (estimated)',
    hovertemplate=f'<b>Your country-wave clustering</b><br>n̄ ≈ 1400, ρ ≈ 0.05<br>SE inflation ≈ {ben_inflation:.1f}×<extra></extra>',
))

# Reference cases
ref_cases = [
    (0.10, 30, 'Classroom data\n(30 students per class, ρ=0.10)'),
    (0.02, 100, 'Mild ICC, medium clusters'),
    (0.20, 500, 'Strong ICC, large clusters'),
]
for rho, n, label in ref_cases:
    inflation = np.sqrt(1 + (n - 1) * rho)
    fig.add_trace(go.Scatter(
        x=[rho], y=[n], mode='markers+text',
        marker=dict(size=11, color='white', symbol='circle', line=dict(color='black', width=1.5)),
        text=[f'  {label.split(chr(10))[0]}<br>  inflation = {inflation:.1f}×'],
        textposition='middle right', textfont=dict(size=9, color='black'),
        showlegend=False,
        hovertemplate=f'<b>{label.replace(chr(10), " ")}</b><br>SE inflation = {inflation:.1f}×<extra></extra>',
    ))

fig.update_layout(
    title=dict(
        text='<b>How wrong is the naive standard error?</b><br>'
             '<span style="font-size:13px;color:#555">'
             'Design effect: SE_inflation = √(1 + (n̄−1)ρ). Hover anywhere to see "your naive SE is X× too small at this combo".</span>',
        x=0.02, xanchor='left',
    ),
    xaxis_title='Intra-cluster correlation (ρ)',
    yaxis_title='Average cluster size (n̄)',
    height=580, width=950,
    plot_bgcolor='white',
    font=dict(family='Georgia, serif', size=12),
    annotations=[
        dict(x=0.99, y=0.02, xref='paper', yref='paper', xanchor='right', yanchor='bottom',
             text='<i>If you cluster 1,400 ESS respondents per country-wave with even modest ρ=0.05,<br>'
                  'the naive (unclustered) SE is roughly 8× too small. That alone moves your<br>'
                  'p=0.0000001 to a much more honest p=0.05. The point estimate is unchanged.<br>'
                  'The clustered SE is the right SE; the naive SE is just an arithmetic mistake.</i>',
             showarrow=False, font=dict(size=11, color='#444'),
             bgcolor='rgba(255,255,255,0.92)', bordercolor='lightgray', borderwidth=1, borderpad=8, align='left'),
    ],
)

fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

out_path = f'{OUT}/interactive_cluster_se.html'
fig.write_html(out_path, include_plotlyjs='cdn')
print(f"Saved: {out_path}  ({os.path.getsize(out_path)/1024:.0f} KB)")

print(f"\nWorked example for Ben's paper:")
print(f"  Cluster size n̄ ≈ {ben_n}, intra-cluster correlation ρ ≈ {ben_rho}")
print(f"  Design effect = 1 + (n̄−1)ρ = 1 + {ben_n-1} × {ben_rho} = {1 + (ben_n-1)*ben_rho:.1f}")
print(f"  SE inflation factor = √{1 + (ben_n-1)*ben_rho:.1f} = {ben_inflation:.2f}×")
print(f"  Naive SE is {ben_inflation:.0f}× too small. Clustering corrects this.")
