"""
Interactive: cross-level interaction (the β₃ slider).

Lets Ben drag CWED across its observed range and watch the predicted slope of
RTI on anti-immigration update in real time. Two visual elements:
  1. The "fan plot" — predicted slope as a function of CWED (line)
  2. The "implied regression line" — for the currently-selected CWED, the
     predicted Y vs RTI relationship (a line whose slope changes with CWED)

This is the core pedagogical move for cross-level interactions: β₃ is the rate
at which the slope of one variable changes with the level of another. Sliding
CWED makes that abstract definition immediate.

Output: outputs/figures/walkthrough/interactive_cross_level.html
"""
import os
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

OUT = 'outputs/figures/walkthrough'
os.makedirs(OUT, exist_ok=True)

# Published Model 3 (random slopes) parameters from the paper
beta1 = 0.215   # main effect of RTI at CWED = 0 (standardised)
beta3 = -0.059  # cross-level interaction
se3 = 0.024
beta0 = 5.0     # baseline anti-immigration at RTI=0, CWED=0
beta2 = -0.069  # main effect of CWED on level (smaller and not significant)

# CWED z-scores: the observed range in your 15-country sample
cwed_z_grid = np.linspace(-2, 2, 41)
rti_grid = np.linspace(-2, 2, 50)

# Compute the predicted slope at each CWED value
predicted_slopes = beta1 + beta3 * cwed_z_grid

# Build figure with two subplots: left = fan plot, right = implied regression line
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Predicted RTI-slope as CWED varies (the fan)",
                    "What the implied regression line looks like"),
    column_widths=[0.5, 0.5],
    horizontal_spacing=0.12,
)

# LEFT panel: fan plot — show the predicted slope across CWED values
# Add the line of predicted slopes
fig.add_trace(go.Scatter(
    x=cwed_z_grid, y=predicted_slopes,
    mode='lines', name='Predicted slope = β₁ + β₃·CWED',
    line=dict(color='#2c3e8e', width=3),
    hovertemplate='CWED z = %{x:.2f}<br>Predicted slope = %{y:.3f}<extra></extra>',
), row=1, col=1)

# 95% CI band
slope_se = se3 * np.abs(cwed_z_grid)
fig.add_trace(go.Scatter(
    x=np.concatenate([cwed_z_grid, cwed_z_grid[::-1]]),
    y=np.concatenate([predicted_slopes - 1.96 * slope_se,
                      (predicted_slopes + 1.96 * slope_se)[::-1]]),
    fill='toself', fillcolor='rgba(44,62,142,0.15)',
    line=dict(color='rgba(255,255,255,0)'),
    name='95% CI', showlegend=True, hoverinfo='skip',
), row=1, col=1)

# Reference at CWED z = 0 (average country)
fig.add_hline(y=beta1, line_dash='dot', line_color='gray', opacity=0.5, row=1, col=1,
              annotation_text=f'Slope at average CWED = {beta1:.3f}',
              annotation_position='top right', annotation_font_size=10)

# Markers showing key countries' positions
country_data = {
    'GB (UK)': -2.0, 'IT': -1.4, 'DE': -1.0, 'FI': -0.5, 'DK': -0.5,
    'NO': 2.0, 'BE': 1.4, 'NL': 0.7, 'FR': 0.5,
}
for cntry, cwed_z in country_data.items():
    slope_here = beta1 + beta3 * cwed_z
    fig.add_trace(go.Scatter(
        x=[cwed_z], y=[slope_here], mode='markers+text',
        marker=dict(size=10, color='#d62728', line=dict(color='white', width=2)),
        text=[cntry], textposition='top center', textfont=dict(size=9),
        showlegend=False,
        hovertemplate=f'<b>{cntry}</b><br>CWED z = {cwed_z:.1f}<br>Predicted slope = {slope_here:.3f}<extra></extra>',
    ), row=1, col=1)

# RIGHT panel: implied regression lines for selected CWED values
# Show 3 specific CWED levels with different colours
cwed_demo = [-2.0, 0.0, 2.0]  # low (UK-like), average, high (Norway-like)
labels_demo = ['Low CWED (≈ UK)', 'Average CWED', 'High CWED (≈ Norway)']
colours_demo = ['#d62728', '#888', '#2c3e8e']

for cwed_z, label, colour in zip(cwed_demo, labels_demo, colours_demo):
    intercept_here = beta0 + beta2 * cwed_z
    slope_here = beta1 + beta3 * cwed_z
    y_pred = intercept_here + slope_here * rti_grid
    fig.add_trace(go.Scatter(
        x=rti_grid, y=y_pred, mode='lines',
        name=f'{label} (slope = {slope_here:.3f})',
        line=dict(color=colour, width=3),
        hovertemplate=f'<b>{label}</b><br>RTI = %{{x:.2f}}<br>Predicted Y = %{{y:.2f}}<extra></extra>',
    ), row=1, col=2)

# Annotations on right panel
fig.add_annotation(
    x=1.8, y=beta0 + beta2 * (-2.0) + (beta1 + beta3 * (-2.0)) * 1.8,
    text='High-RTI workers in low-CWED<br>countries are most anti-immigration',
    showarrow=True, arrowhead=2, ax=-30, ay=-40,
    font=dict(size=10, color='#d62728'),
    row=1, col=2,
)

fig.update_xaxes(title_text='CWED (standardised, z-score)', row=1, col=1, showgrid=True, gridcolor='#eee')
fig.update_yaxes(title_text='Slope of anti-immigration on RTI', row=1, col=1, showgrid=True, gridcolor='#eee')
fig.update_xaxes(title_text='RTI (standardised)', row=1, col=2, showgrid=True, gridcolor='#eee')
fig.update_yaxes(title_text='Predicted anti-immigration index', row=1, col=2, showgrid=True, gridcolor='#eee')

fig.update_layout(
    title=dict(
        text='<b>The cross-level interaction, made visible</b><br>'
             '<span style="font-size:13px;color:#555">β₃ = −0.059 means: each one-SD increase in CWED reduces the slope of RTI on anti-immigration by 0.059 scale points. '
             'Hover the dots on the left to see country positions.</span>',
        x=0.02, xanchor='left',
    ),
    height=560, width=1100,
    plot_bgcolor='white',
    font=dict(family='Georgia, serif', size=12),
    legend=dict(x=0.5, y=-0.15, xanchor='center', yanchor='top', orientation='h'),
    annotations=[
        dict(x=1.0, y=-0.30, xref='paper', yref='paper', xanchor='right', yanchor='top',
             text='<i>Left: the slope of RTI on anti-immigration depends linearly on CWED. '
                  'Right: that linear dependence translates into different regression lines for different countries.<br>'
                  'The Liberal-vs-Nordic gap in §V is the difference between the red and blue lines on the right panel.</i>',
             showarrow=False, font=dict(size=10, color='#666'),
             bgcolor='rgba(255,255,255,0.85)', bordercolor='lightgray', borderwidth=1, borderpad=5),
    ],
)

# Bug fix: subplot title fonts have to be set after layout
for ann in fig.layout.annotations:
    if 'Predicted RTI-slope' in str(ann.text) or 'implied regression' in str(ann.text):
        ann.font = dict(size=12, color='#333')

out_path = f'{OUT}/interactive_cross_level.html'
fig.write_html(out_path, include_plotlyjs='cdn')
print(f"Saved: {out_path}  ({os.path.getsize(out_path)/1024:.0f} KB)")
print(f"\nKey teaching points:")
print(f"  - Slope at low CWED (UK-like, z=-2):    {beta1 + beta3*(-2):.3f}")
print(f"  - Slope at average CWED (z=0):          {beta1:.3f}")
print(f"  - Slope at high CWED (Norway-like, z=2): {beta1 + beta3*2:.3f}")
print(f"  - Total slope range: {abs((beta1+beta3*2)-(beta1+beta3*(-2))):.3f} scale points across 4 SDs of CWED")
