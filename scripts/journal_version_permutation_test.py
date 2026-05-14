"""Country-label permutation test for the §V.D headline correlation r=−0.848.

Per v3→v4 council critique (Methodologist + Skeptic + Pre-mortem CRITICAL):
the parametric p<0.001 attached to a Pearson r computed on N=15 country-level
observations is the wrong inferential machinery; the right object is the
empirical p from a country-label permutation test against a random distribution.

Output: outputs/tables/journal_version/permutation_test_blups_cwed.csv
        outputs/tables/journal_version/permutation_test_summary.json

Run cost: ~10 seconds for 10,000 iterations on N=15.
"""
import os, json, numpy as np, pandas as pd
from pathlib import Path
from scipy import stats

REPO = Path(r"C:/Users/PKF715/Documents/claude_repos/Research_Master")
SRC = REPO / "outputs/tables/blups_country_slopes.csv"
OUT_DIR = REPO / "outputs/tables/journal_version"
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(SRC)
assert {"cntry", "blup_slope", "cwed"} <= set(df.columns), df.columns
n = len(df)
print(f"N = {n} countries")

# Observed correlation
r_obs, p_param = stats.pearsonr(df["blup_slope"], df["cwed"])
print(f"Observed r = {r_obs:.4f}, parametric p = {p_param:.6f}")

# Permutation: shuffle CWED labels across countries, recompute r each time
rng = np.random.default_rng(seed=2026)
N_ITER = 10_000
slope = df["blup_slope"].values
cwed = df["cwed"].values
perm_rs = np.empty(N_ITER)
for i in range(N_ITER):
    permuted_cwed = rng.permutation(cwed)
    perm_rs[i], _ = stats.pearsonr(slope, permuted_cwed)

# Empirical p-values
# Two-sided: fraction of permutations whose |r| >= |r_obs|
p_two = float(np.mean(np.abs(perm_rs) >= abs(r_obs)))
# One-sided (negative tail, since theory predicts r < 0): fraction with r <= r_obs
p_one = float(np.mean(perm_rs <= r_obs))

# Distribution stats
quantiles = {f"q{q}": float(np.quantile(perm_rs, q / 100)) for q in [1, 2.5, 5, 50, 95, 97.5, 99]}

summary = {
    "n_countries": n,
    "n_iterations": N_ITER,
    "r_observed": float(r_obs),
    "p_parametric_two_sided": float(p_param),
    "p_empirical_two_sided": p_two,
    "p_empirical_one_sided_negative": p_one,
    "permutation_distribution_mean": float(perm_rs.mean()),
    "permutation_distribution_std": float(perm_rs.std()),
    **{f"permutation_distribution_{k}": v for k, v in quantiles.items()},
    "interpretation": (
        "Observed r=" + f"{r_obs:.4f}" + " is more extreme than "
        f"{(1 - p_two) * 100:.2f}% of permutations under the null of no association. "
        "Empirical two-sided p = " + f"{p_two:.4f}" + ". "
        "Parametric p =" + f" {p_param:.6f}" + " is " + (
            "comparable" if abs(p_param - p_two) < 0.005 else "different"
        ) + " to the empirical p."
    ),
}

# Save
with (OUT_DIR / "permutation_test_summary.json").open("w") as f:
    json.dump(summary, f, indent=2)

pd.DataFrame({"perm_r": perm_rs}).to_csv(OUT_DIR / "permutation_test_distribution.csv", index=False)
print(json.dumps(summary, indent=2))
