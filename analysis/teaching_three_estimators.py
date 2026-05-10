"""
Teaching interactive: "Three estimators on the same data — what each one buys you"

The pedagogical anchor for understanding partial pooling. Shows what happens
when you analyse the same 12-country dataset with three different estimators:

  1. Pure pooling  — OLS with no country distinction (one global slope)
  2. No pooling    — separate OLS per country (one slope per country, equal weight)
  3. Partial pool. — multilevel model that shrinks small-N countries toward mean

A scenario selector lets the user switch between low-noise (large samples,
clear pattern), realistic, and high-noise (small samples, noisy data) settings.
At each setting, the three panels show what the estimators do.

Pedagogical punchline: when noise is high or samples are small, no-pooling
estimates flicker wildly and become unreliable. Partial pooling stays
defensible by borrowing strength across countries.

Output: outputs/figures/walkthrough/teaching_three_estimators.html
"""
import os
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

OUT = "outputs/figures/walkthrough"
os.makedirs(OUT, exist_ok=True)


# ── Synthetic dataset generator ──────────────────────────────────────────────

def generate_scenario(true_slopes, sample_sizes, noise_sd, seed=42):
    """Generate per-country data and compute the three estimators."""
    rng = np.random.default_rng(seed)
    countries = []
    all_x, all_y = [], []
    for k, (slope, n) in enumerate(zip(true_slopes, sample_sizes)):
        x = rng.uniform(-2.5, 2.5, n)
        intercept = 5.0
        y = intercept + slope * x + rng.normal(0, noise_sd, n)
        countries.append({
            "id": chr(65 + k),  # A, B, C...
            "n": n,
            "true_slope": slope,
            "x": x, "y": y,
        })
        all_x.append(x); all_y.append(y)

    # ── Pure pooling: one OLS through all data ──
    X = np.concatenate(all_x); Y = np.concatenate(all_y)
    pooled_slope, pooled_intercept = np.polyfit(X, Y, 1)

    # ── No pooling: separate OLS per country ──
    for c in countries:
        s, i = np.polyfit(c["x"], c["y"], 1)
        c["nopool_slope"] = s
        c["nopool_intercept"] = i

    # ── Partial pooling: shrink each country's slope toward grand mean ──
    # Simplified shrinkage: factor ~ within-country precision /
    # (within-country precision + between-country precision).
    # Approximated as n / (n + lambda) where lambda controls global shrinkage.
    # Larger lambda -> more shrinkage. Tuned so small-N countries shrink heavily.
    grand_mean_slope = np.mean([c["nopool_slope"] for c in countries])
    lam = (noise_sd ** 2) * 8  # heuristic; bigger noise => more shrinkage
    for c in countries:
        weight = c["n"] / (c["n"] + lam)
        c["partial_slope"] = weight * c["nopool_slope"] + (1 - weight) * grand_mean_slope
        c["partial_intercept"] = c["nopool_intercept"]  # for plotting; intercept shrinkage less critical
        c["shrinkage_weight"] = weight  # 1.0 = trust your data; 0.0 = use grand mean

    return countries, pooled_slope, pooled_intercept, grand_mean_slope


# Three scenarios — same true slopes, different noise/sample-size profiles
TRUE_SLOPES = [0.55, 0.50, 0.45, 0.40, 0.40, 0.35, 0.30, 0.30, 0.25, 0.20, 0.20, 0.15]

scenarios = {
    "Low noise, large samples (clean pattern)": dict(
        sample_sizes=[1500] * 12, noise_sd=0.5, seed=42,
    ),
    "Realistic conditions": dict(
        sample_sizes=[800, 1200, 600, 1500, 400, 900, 1100, 350, 700, 250, 800, 200],
        noise_sd=1.5, seed=42,
    ),
    "High noise, small samples (noisy)": dict(
        sample_sizes=[150, 80, 200, 100, 60, 180, 80, 120, 50, 90, 70, 50],
        noise_sd=2.5, seed=42,
    ),
}

# Pre-compute each scenario
scenario_data = {}
for name, cfg in scenarios.items():
    scenario_data[name] = generate_scenario(
        TRUE_SLOPES, cfg["sample_sizes"], cfg["noise_sd"], cfg["seed"]
    )


# ── Build figure ─────────────────────────────────────────────────────────────

# Three columns: pure pooling, no pooling, partial pooling
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=(
        "<b>1. Pure pooling (OLS)</b><br><span style='font-size:11px;color:#888'>One slope for everyone</span>",
        "<b>2. No pooling (separate OLS per country)</b><br><span style='font-size:11px;color:#888'>Each country gets its own slope, equally weighted</span>",
        "<b>3. Partial pooling (multilevel)</b><br><span style='font-size:11px;color:#888'>Slopes borrow strength from neighbours</span>",
    ),
    horizontal_spacing=0.06,
)

xline = np.linspace(-2.5, 2.5, 100)

# Country palette
import colorsys
def country_colour(i, n):
    h = 0.6 - (i / (n - 1)) * 0.55  # blue → red gradient by true slope rank
    r, g, b = colorsys.hsv_to_rgb(h, 0.7, 0.85)
    return f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"

# Initial scenario
init_scenario = "Realistic conditions"


def add_traces_for_scenario(fig, scenario_name):
    countries, pooled_slope, pooled_int, gm_slope = scenario_data[scenario_name]

    # Panel 1: pure pooling — one big line over scattered data
    all_x = np.concatenate([c["x"] for c in countries])
    all_y = np.concatenate([c["y"] for c in countries])
    fig.add_trace(go.Scatter(
        x=all_x, y=all_y, mode="markers",
        marker=dict(size=3, color="lightgray", opacity=0.4),
        showlegend=False, name="all data",
        hoverinfo="skip",
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=xline, y=pooled_int + pooled_slope * xline,
        mode="lines", line=dict(color="black", width=4),
        name=f"Pooled OLS (slope={pooled_slope:.3f})",
        showlegend=True, hovertemplate="Pooled slope: %{y:.3f}<extra></extra>",
    ), row=1, col=1)

    # Panel 2 & 3: per-country lines (no pooling and partial pooling)
    for i, c in enumerate(sorted(countries, key=lambda x: x["true_slope"])):
        col = country_colour(i, len(countries))
        # No pooling
        fig.add_trace(go.Scatter(
            x=xline, y=c["nopool_intercept"] + c["nopool_slope"] * xline,
            mode="lines", line=dict(color=col, width=2.5),
            name=f"{c['id']} (n={c['n']}, slope={c['nopool_slope']:.2f})",
            legendgroup=c["id"], showlegend=False,
            hovertemplate=(f"<b>Country {c['id']}</b><br>n = {c['n']}<br>"
                            f"true slope: {c['true_slope']:.2f}<br>"
                            f"estimated slope: {c['nopool_slope']:.3f}<extra></extra>"),
        ), row=1, col=2)
        # Partial pooling
        fig.add_trace(go.Scatter(
            x=xline, y=c["partial_intercept"] + c["partial_slope"] * xline,
            mode="lines", line=dict(color=col, width=2.5),
            name=f"{c['id']} partial",
            legendgroup=c["id"], showlegend=False,
            hovertemplate=(f"<b>Country {c['id']}</b><br>n = {c['n']}<br>"
                            f"true slope: {c['true_slope']:.2f}<br>"
                            f"partial-pooled slope: {c['partial_slope']:.3f}<br>"
                            f"shrinkage weight: {c['shrinkage_weight']:.2f} "
                            f"(1.0 = trust data, 0.0 = trust mean)<extra></extra>"),
        ), row=1, col=3)

    # Add the grand mean reference line on the partial-pooling panel
    fig.add_trace(go.Scatter(
        x=xline, y=5.0 + gm_slope * xline, mode="lines",
        line=dict(color="black", width=4, dash="dash"),
        name=f"Grand mean (slope={gm_slope:.3f})",
        showlegend=True,
        hovertemplate=f"Grand mean slope: {gm_slope:.3f}<extra></extra>",
    ), row=1, col=3)


# Build all three scenarios as toggle-button states
# We track trace indices per scenario for visibility toggling
trace_indices = {}
for name in scenarios:
    start = len(fig.data)
    add_traces_for_scenario(fig, name)
    end = len(fig.data)
    trace_indices[name] = list(range(start, end))

# Set initial visibility: only the realistic scenario visible
initial_visible = trace_indices[init_scenario]
for i in range(len(fig.data)):
    fig.data[i].visible = (i in initial_visible)

# Update menu — radio buttons for scenario selection
buttons = []
for name in scenarios:
    visible = [i in trace_indices[name] for i in range(len(fig.data))]
    buttons.append(dict(
        label=name, method="update",
        args=[{"visible": visible}],
    ))

fig.update_layout(
    title=dict(
        text="<b>Three estimators on the same data — what each one buys you</b><br>"
             "<span style='font-size:13px;color:#555'>"
             "Switch between scenarios. Compare what the three estimators do as data quality varies.</span>",
        x=0.02, xanchor="left",
    ),
    height=600, width=1300, plot_bgcolor="white",
    font=dict(family="Georgia, serif", size=12),
    margin=dict(t=130, b=140, l=50, r=20),
    legend=dict(x=1.0, y=0.5, xanchor="right", yanchor="middle",
                bgcolor="rgba(255,255,255,0.85)", bordercolor="lightgray", borderwidth=1,
                font=dict(size=10)),
    updatemenus=[dict(
        type="buttons", direction="right",
        x=0.5, y=1.16, xanchor="center",
        buttons=buttons,
        bgcolor="white", bordercolor="lightgray",
    )],
    annotations=[
        dict(x=0.02, y=-0.20, xref="paper", yref="paper",
             xanchor="left", yanchor="top",
             text=(
                 "<b>What to watch for.</b> Switch from <i>low noise, large samples</i> "
                 "to <i>high noise, small samples</i> and look at the middle panel. "
                 "The no-pooling slopes go from a clean ordered fan to a chaotic mess — "
                 "small-N countries get wildly off their true values because each country's slope "
                 "is estimated from too few observations to be reliable. "
                 "Now look at the right panel: under partial pooling, those same small-N countries "
                 "stay close to the grand mean (dashed line), because the multilevel model "
                 "<i>knows</i> their estimates are unreliable and pulls them toward the average. "
                 "Large-N countries keep their distinctive slopes; small-N ones shrink. "
                 "<b>That is partial pooling. That is what BLUPs are doing in §V.D.</b>"
             ),
             showarrow=False, font=dict(size=11, color="#444"), align="left",
             bordercolor="#888", borderwidth=1, borderpad=8,
             bgcolor="rgba(255,250,230,0.92)"),
    ],
)

fig.update_xaxes(title_text="RTI", range=[-2.7, 2.7], showgrid=True, gridcolor="#eee")
fig.update_yaxes(title_text="Anti-immigration", range=[2, 8], showgrid=True, gridcolor="#eee")

out_path = f"{OUT}/teaching_three_estimators.html"
fig.write_html(out_path, include_plotlyjs="cdn")
print(f"Saved: {out_path}  ({os.path.getsize(out_path)/1024:.0f} KB)")

# Diagnostic
print("\nDiagnostic numbers per scenario:")
for name, (countries, p_slope, _, gm) in scenario_data.items():
    nopool = np.array([c["nopool_slope"] for c in countries])
    partial = np.array([c["partial_slope"] for c in countries])
    truth = np.array([c["true_slope"] for c in countries])
    print(f"\n{name}")
    print(f"  Pure pooling slope: {p_slope:.3f}")
    print(f"  No pooling — RMSE vs truth: {np.sqrt(np.mean((nopool - truth)**2)):.3f}")
    print(f"  Partial pooling — RMSE vs truth: {np.sqrt(np.mean((partial - truth)**2)):.3f}")
