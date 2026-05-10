"""
Teaching interactive: "Same mean, different slopes — why averages lie"

The pedagogical anchor for understanding multilevel moderation. Demonstrates
that two countries can have identical mean attitudes while having completely
different conversion rates of RTI into anti-immigration sentiment.

Slider controls the gap between country means. As you drag the means together,
the bar chart shows the gap shrinking. But the regression lines on the scatter
stay where they are — the slopes don't change. Pedagogical punchline: "if you
only compare means, this country contrast looks like nothing. The moderation
lives in the slopes."

Output: outputs/figures/walkthrough/teaching_same_mean.html
"""
import os
import numpy as np
import plotly.graph_objects as go

OUT = "outputs/figures/walkthrough"
os.makedirs(OUT, exist_ok=True)
np.random.seed(42)

# ── Generate synthetic data ──────────────────────────────────────────────────
# Two countries, fixed slopes (large gap), varying mean offset
N_PER = 200
RTI_RANGE = (-2.5, 2.5)
rti = np.linspace(RTI_RANGE[0], RTI_RANGE[1], N_PER)

# Country A (Liberal-like): steep slope
slope_a = 0.55
# Country B (Nordic-like): flat slope
slope_b = 0.18

# Common baseline anchor (where the lines pass at RTI = 0)
baseline = 5.0

# Mean-offset levels we'll let the user toggle. Negative means B is below A.
offset_levels = np.arange(-3.0, 3.01, 0.25)


def country_data(slope, intercept, n=N_PER, noise=0.5, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.uniform(*RTI_RANGE, n)
    y = intercept + slope * x + rng.normal(0, noise, n)
    return x, y


# ── Build the figure with frames ─────────────────────────────────────────────
fig = go.Figure()

# We'll present three panels: scatter (left), country means bar chart (right top),
# slope-only view (right bottom). Use a 2x2 subplot via make_subplots.
from plotly.subplots import make_subplots
fig = make_subplots(
    rows=2, cols=2,
    column_widths=[0.62, 0.38],
    row_heights=[0.55, 0.45],
    specs=[
        [{"rowspan": 2}, {"type": "bar"}],
        [None, {"type": "scatter"}],
    ],
    subplot_titles=(
        "RTI vs anti-immigration — the actual data",
        "Country means (this is what naive comparison shows)",
        "Slopes only (this is what moderation looks like)",
    ),
    horizontal_spacing=0.10,
    vertical_spacing=0.18,
)

# Pre-generate one fixed dataset for each country (we'll just shift Y for the offset)
xa, ya_base = country_data(slope_a, baseline, seed=1)
xb, yb_base = country_data(slope_b, baseline, seed=2)


def make_frame(offset):
    ya = ya_base + offset / 2.0
    yb = yb_base - offset / 2.0
    return ya, yb


# Initial frame at offset = 0
ya0, yb0 = make_frame(0.0)

# Left panel: scatter of two countries + their regression lines
fig.add_trace(go.Scatter(
    x=xa, y=ya0, mode="markers", name="Country A (Liberal-like)",
    marker=dict(color="#d62728", size=6, opacity=0.55),
    legendgroup="A", showlegend=True,
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=xb, y=yb0, mode="markers", name="Country B (Nordic-like)",
    marker=dict(color="#2c3e8e", size=6, opacity=0.55),
    legendgroup="B", showlegend=True,
), row=1, col=1)

# Regression lines (one per country)
xline = np.array(RTI_RANGE)
fig.add_trace(go.Scatter(
    x=xline, y=baseline + slope_a * xline,  # offset added in updates
    mode="lines", name=f"A slope = {slope_a:.2f}",
    line=dict(color="#d62728", width=4),
    legendgroup="A", showlegend=False,
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=xline, y=baseline + slope_b * xline,
    mode="lines", name=f"B slope = {slope_b:.2f}",
    line=dict(color="#2c3e8e", width=4),
    legendgroup="B", showlegend=False,
), row=1, col=1)

# Right top: country means bar chart
fig.add_trace(go.Bar(
    x=["Country A", "Country B"],
    y=[ya0.mean(), yb0.mean()],
    marker_color=["#d62728", "#2c3e8e"],
    text=[f"{ya0.mean():.2f}", f"{yb0.mean():.2f}"],
    textposition="outside",
    showlegend=False,
), row=1, col=2)

# Right bottom: slope-only view (origin-centred regression lines)
fig.add_trace(go.Scatter(
    x=xline, y=slope_a * xline, mode="lines",
    line=dict(color="#d62728", width=4),
    name="A slope", showlegend=False,
), row=2, col=2)
fig.add_trace(go.Scatter(
    x=xline, y=slope_b * xline, mode="lines",
    line=dict(color="#2c3e8e", width=4),
    name="B slope", showlegend=False,
), row=2, col=2)

# Add a horizontal baseline at 0 in the slope panel
fig.add_hline(y=0, line_dash="dot", line_color="gray", line_width=1, row=2, col=2)

# Build slider frames
frames = []
for offset in offset_levels:
    ya, yb = make_frame(offset)
    int_a = baseline + offset / 2.0
    int_b = baseline - offset / 2.0
    frames.append(go.Frame(
        name=f"{offset:+.2f}",
        data=[
            go.Scatter(x=xa, y=ya, mode="markers",
                       marker=dict(color="#d62728", size=6, opacity=0.55)),
            go.Scatter(x=xb, y=yb, mode="markers",
                       marker=dict(color="#2c3e8e", size=6, opacity=0.55)),
            go.Scatter(x=xline, y=int_a + slope_a * xline, mode="lines",
                       line=dict(color="#d62728", width=4)),
            go.Scatter(x=xline, y=int_b + slope_b * xline, mode="lines",
                       line=dict(color="#2c3e8e", width=4)),
            go.Bar(x=["Country A", "Country B"], y=[ya.mean(), yb.mean()],
                   marker_color=["#d62728", "#2c3e8e"],
                   text=[f"{ya.mean():.2f}", f"{yb.mean():.2f}"],
                   textposition="outside"),
            go.Scatter(x=xline, y=slope_a * xline, mode="lines",
                       line=dict(color="#d62728", width=4)),
            go.Scatter(x=xline, y=slope_b * xline, mode="lines",
                       line=dict(color="#2c3e8e", width=4)),
        ],
    ))

fig.frames = frames

# Slider controls
sliders = [dict(
    active=int(np.argmin(np.abs(offset_levels - 0.0))),
    currentvalue=dict(
        prefix="Country mean gap (A − B): ", visible=True, xanchor="left",
        font=dict(size=14, color="#333"),
    ),
    pad=dict(t=50, b=10),
    steps=[
        dict(
            method="animate",
            label=f"{offset:+.2f}",
            args=[
                [f"{offset:+.2f}"],
                dict(mode="immediate", frame=dict(duration=0, redraw=True),
                     transition=dict(duration=0)),
            ],
        )
        for offset in offset_levels
    ],
)]

# Axis labels
fig.update_xaxes(title_text="RTI (z-score)", range=RTI_RANGE, row=1, col=1)
fig.update_yaxes(title_text="Anti-immigration index (0–10)", range=[1, 9], row=1, col=1)
fig.update_yaxes(title_text="Mean attitude", range=[1, 9], row=1, col=2)
fig.update_xaxes(title_text="RTI", range=RTI_RANGE, row=2, col=2)
fig.update_yaxes(title_text="Slope effect", range=[-2, 2], row=2, col=2)

fig.update_layout(
    title=dict(
        text="<b>Same mean, different slopes — why averages lie</b><br>"
             "<span style='font-size:13px;color:#555'>"
             "Drag the slider to set the gap between Country A's and B's mean attitudes. "
             "Watch the bar chart respond. Watch the scatter and slopes <i>not</i> respond.</span>",
        x=0.02, xanchor="left",
    ),
    height=620, width=1100, plot_bgcolor="white",
    font=dict(family="Georgia, serif", size=12),
    sliders=sliders,
    margin=dict(t=120, b=80, l=60, r=20),
    annotations=[
        dict(x=0.02, y=-0.16, xref="paper", yref="paper",
             xanchor="left", yanchor="top",
             text="<b>What this shows.</b> When the slider is at zero, the two countries have <i>identical means</i> "
                  "(bar chart confirms it). A naive comparison says \"welfare doesn't matter — these countries are the same\". "
                  "But the scatter on the left shows two completely different slopes. "
                  "The Liberal-like country converts each unit of RTI into 0.55 scale points of anti-immigration; "
                  "the Nordic-like country only converts 0.18. <b>The moderation is in the slope, not the mean.</b> "
                  "That is why your paper does not compare regime means — it compares regime slopes.",
             showarrow=False, font=dict(size=11, color="#444"), align="left",
             bordercolor="#888", borderwidth=1, borderpad=8,
             bgcolor="rgba(255,250,230,0.9)"),
    ],
)

# Re-style subplot title fonts
for ann in fig.layout.annotations:
    text = getattr(ann, "text", "") or ""
    if any(text.startswith(prefix) for prefix in ("RTI vs", "Country means", "Slopes only")):
        ann.font = dict(size=12, color="#0b3d91")

fig.update_xaxes(showgrid=True, gridcolor="#eee")
fig.update_yaxes(showgrid=True, gridcolor="#eee")

out_path = f"{OUT}/teaching_same_mean.html"
fig.write_html(out_path, include_plotlyjs="cdn")
print(f"Saved: {out_path}  ({os.path.getsize(out_path)/1024:.0f} KB)")
print("\nKey teaching points:")
print(f"  - Country A (Liberal-like) slope: {slope_a}")
print(f"  - Country B (Nordic-like) slope:  {slope_b}")
print(f"  - When mean gap = 0, naive comparison sees nothing.")
print(f"  - The slope gap (0.55 - 0.18 = 0.37) is what your paper actually measures.")
