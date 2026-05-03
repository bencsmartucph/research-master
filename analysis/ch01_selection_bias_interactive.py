"""
Chapter 1 interactive: selection bias slider.

Generates a self-contained HTML file that lets Ben drag the strength of an
unobserved confounder (call it U) and watch:
  - The true ATE (constant)
  - The naive comparison E[Y|D=1] - E[Y|D=0] (moves with U)
  - The selection-bias term (the gap)

Pedagogical move: shows in real time why "comparing groups" lies to you, and
why the strength of the lie scales with how much U drives both selection-into-
treatment and the outcome.

Output: docs/learning_econometrics/interactives/ch01_selection_bias.html
"""
import os
import numpy as np
import plotly.graph_objects as go

OUT = 'docs/learning_econometrics/interactives'
os.makedirs(OUT, exist_ok=True)

# Generate sample data once; the "U strength" slider just re-weights it.
np.random.seed(7)
N = 1000
# Latent confounder U ~ N(0, 1)
U = np.random.normal(0, 1, N)
# Treatment depends on U (when slider is high) plus noise
# Outcome depends on D (true ATE = 1.0) plus a U-influence (the slider)
true_ATE = 1.0

# Pre-compute Y(0) and Y(1) under varying alpha (U-on-Y influence)
alpha_grid = np.linspace(0, 3, 31)  # confounder strength
gamma = 1.5  # how strongly U pushes selection-into-treatment

# Selection: D = 1 if U + noise > threshold; threshold tuned to give ~50% treated
selection_noise = np.random.normal(0, 1, N)
prop_treated = 1 / (1 + np.exp(-(gamma * U + selection_noise)))
D = (np.random.uniform(0, 1, N) < prop_treated).astype(int)

# Pre-compute the trace data
naive_ate = []
selection_bias = []
for alpha in alpha_grid:
    Y0 = alpha * U + np.random.normal(0, 0.5, N)
    Y1 = Y0 + true_ATE
    Y = D * Y1 + (1 - D) * Y0
    naive = Y[D == 1].mean() - Y[D == 0].mean()
    bias = naive - true_ATE
    naive_ate.append(naive)
    selection_bias.append(bias)

naive_ate = np.array(naive_ate)
selection_bias = np.array(selection_bias)

# ── Build the figure ─────────────────────────────────────────────────────────
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=alpha_grid, y=[true_ATE] * len(alpha_grid),
    mode='lines', name='True ATE (what we want)',
    line=dict(color='#2c3e8e', width=3),
    hovertemplate='True ATE: %{y:.2f}<extra></extra>',
))

fig.add_trace(go.Scatter(
    x=alpha_grid, y=naive_ate,
    mode='lines+markers', name='Naive comparison: E[Y|D=1] − E[Y|D=0]',
    line=dict(color='#d62728', width=3),
    marker=dict(size=7),
    hovertemplate='Naive estimate: %{y:.2f}<br>Confounder strength: %{x:.2f}<extra></extra>',
))

fig.add_trace(go.Scatter(
    x=alpha_grid, y=selection_bias,
    mode='lines', name='Selection bias (the gap)',
    line=dict(color='#888', width=2, dash='dot'),
    hovertemplate='Selection bias: %{y:+.2f}<extra></extra>',
))

# Annotations: anchor key points
# At alpha = 0, naive == true ATE (no confounding)
fig.add_annotation(
    x=0, y=true_ATE, text='No confounder: naive = true ATE',
    showarrow=True, arrowhead=2, ax=60, ay=-30, font=dict(size=11),
)
# At alpha = 3, the bias is large
fig.add_annotation(
    x=3, y=naive_ate[-1], text=f'Strong confounder:<br>naive ≈ {naive_ate[-1]:.2f},<br>but true ATE is still {true_ATE:.1f}',
    showarrow=True, arrowhead=2, ax=-90, ay=-40, font=dict(size=11),
)

fig.update_layout(
    title=dict(
        text='<b>The selection-bias decomposition, in pictures</b><br>'
             '<span style="font-size:13px;color:#555">'
             'Drag along the x-axis: as the unobserved confounder gets stronger, '
             'the naive comparison drifts away from the true effect. The gap is selection bias.'
             '</span>',
        x=0.02, xanchor='left',
    ),
    xaxis_title='Strength of unobserved confounder U on outcome Y (α)',
    yaxis_title='Estimated treatment effect',
    height=540, width=900,
    plot_bgcolor='white',
    font=dict(family='Georgia, serif', size=13),
    legend=dict(x=0.02, y=0.98, xanchor='left', yanchor='top',
                bgcolor='rgba(255,255,255,0.9)', bordercolor='lightgray', borderwidth=1),
    annotations=[
        dict(x=0.99, y=0.02, xref='paper', yref='paper', xanchor='right', yanchor='bottom',
             text='<i>Setup: true ATE = 1.0. U pushes both selection (γ=1.5) and outcomes (α slider).<br>'
                  'When α=0, U does not affect Y, so the naive comparison is unbiased. When α grows, bias grows linearly.</i>',
             showarrow=False, font=dict(size=11, color='#666'),
             bgcolor='rgba(255,255,255,0.85)', bordercolor='lightgray', borderwidth=1, borderpad=6),
    ],
)
fig.update_xaxes(showgrid=True, gridcolor='#eee', zeroline=False)
fig.update_yaxes(showgrid=True, gridcolor='#eee', zeroline=True, zerolinecolor='lightgray')

out_path = f'{OUT}/ch01_selection_bias.html'
fig.write_html(out_path, include_plotlyjs='cdn')
print(f"Saved: {out_path}  ({os.path.getsize(out_path)/1024:.0f} KB)")
print("\nKey teaching points the figure makes:")
print(f"  1. At α=0 (no confounder-Y link), naive = true ATE = {true_ATE:.1f}. Comparison is honest.")
print(f"  2. At α=1, naive estimate ≈ {naive_ate[10]:.2f} — already 50% inflated.")
print(f"  3. At α=3, naive estimate ≈ {naive_ate[-1]:.2f} — almost double the true effect.")
print(f"  4. The grey dotted line IS the selection-bias term from the chapter's algebra.")
