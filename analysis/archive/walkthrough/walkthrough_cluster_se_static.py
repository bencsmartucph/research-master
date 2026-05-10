"""
Static PNG version of the cluster-SE inflation heatmap.

Mirrors the Plotly interactive (analysis/walkthrough_cluster_se_interactive.py)
but as a self-contained matplotlib figure that embeds in slide decks (HTML + PPTX).

Output: outputs/figures/walkthrough/fig8_cluster_se_static.png
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

OUT = "outputs/figures/walkthrough"
os.makedirs(OUT, exist_ok=True)

mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "figure.dpi": 130,
    "savefig.dpi": 160,
    "savefig.bbox": "tight",
})

rho_grid = np.linspace(0.001, 0.30, 60)
n_grid = np.linspace(10, 2000, 60)
RHO, N = np.meshgrid(rho_grid, n_grid)
SE_INFLATION = np.sqrt(1 + (N - 1) * RHO)

fig, ax = plt.subplots(figsize=(9.5, 5.5))
img = ax.pcolormesh(RHO, N, SE_INFLATION, cmap="viridis", shading="auto", vmin=1, vmax=20)
cbar = plt.colorbar(img, ax=ax, ticks=[1, 2, 5, 10, 15, 20], pad=0.02)
cbar.set_label("SE inflation factor", fontsize=10)

# Contours at meaningful levels
contours = ax.contour(RHO, N, SE_INFLATION, levels=[2, 3, 5, 8, 10, 15],
                       colors="white", linewidths=0.9)
ax.clabel(contours, inline=True, fontsize=9, fmt="%dx")

# Anchor: Ben's paper
ben_n, ben_rho = 1400, 0.05
ben_inflation = np.sqrt(1 + (ben_n - 1) * ben_rho)
ax.scatter([ben_rho], [ben_n], s=350, c="red", marker="*",
           edgecolor="white", linewidth=2.0, zorder=10)
ax.annotate(
    f"Your paper\n($\\bar{{n}}$=1400, $\\rho$≈0.05)\n→ inflation = {ben_inflation:.1f}×",
    xy=(ben_rho, ben_n),
    xytext=(0.10, 1700),
    fontsize=11, color="red", fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
)

# Reference cases
refs = [
    (0.10, 30, "Classroom data"),
    (0.02, 100, "Mild ICC, medium clusters"),
    (0.20, 500, "Strong ICC, large clusters"),
]
for rho, n, label in refs:
    inflation = np.sqrt(1 + (n - 1) * rho)
    ax.scatter([rho], [n], s=80, c="white", marker="o",
               edgecolor="black", linewidth=1.2, zorder=9)
    ax.annotate(f"  {label}\n  ({inflation:.1f}×)", xy=(rho, n),
                xytext=(rho + 0.005, n + 30),
                fontsize=8.5, color="black")

ax.set_xlabel(r"Intra-cluster correlation ($\rho$)", fontsize=11)
ax.set_ylabel(r"Average cluster size ($\bar{n}$)", fontsize=11)
ax.set_title(
    f"Design effect = $1+(\\bar{{n}}-1)\\rho$    →    SE inflation = $\\sqrt{{\\,1+(\\bar{{n}}-1)\\rho\\,}}$\n"
    f"For your country-wave clustering: design effect = {1+(ben_n-1)*ben_rho:.0f}, "
    f"naive SE is {ben_inflation:.1f}× too small",
    fontsize=11, loc="left", pad=12,
)

plt.tight_layout()
out_path = f"{OUT}/fig8_cluster_se_static.png"
plt.savefig(out_path)
plt.close()
print(f"Saved: {out_path}")
print(f"\nKey number for the slide: design effect = {1+(ben_n-1)*ben_rho:.0f}, "
      f"SE inflation = {ben_inflation:.2f}x")
