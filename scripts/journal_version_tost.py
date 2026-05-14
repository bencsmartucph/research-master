"""TOST equivalence test on the redistribution null and the ISSP null.

Per v3→v4 council critique (Methodologist MAJOR): the asymmetric mechanism's
substantive interpretation of nulls requires distinguishing "data could not detect
the effect" from "data rules out the effect at a defensible SESOI." Two-one-sided-t
tests against a Smallest Effect Size of Interest (SESOI) of |β|=0.06 — the
magnitude the symmetric account would have predicted (the exclusion-side moderation
gives β=-0.059, so the symmetric prediction for solidarity is +0.059).

Output: outputs/tables/journal_version/tost_equivalence_test.csv
        outputs/tables/journal_version/tost_summary.json
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(r"C:/Users/PKF715/Documents/claude_repos/Research_Master")
OUT_DIR = REPO / "outputs/tables/journal_version"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Canonical values (read from rs_results.csv where available; else from paper)
def tost(beta, se, n_obs, sesoi, label):
    """Schuirmann two-one-sided-t test.

    H0_lower: beta <= -sesoi (true effect is at least as negative as -SESOI)
    H0_upper: beta >= +sesoi (true effect is at least as positive as +SESOI)
    Both rejected ⇒ effect is statistically equivalent to zero against SESOI.
    Uses a normal approximation (n>>30 in all cases here).
    """
    # Lower bound: t = (beta - (-sesoi)) / se = (beta + sesoi) / se; we want one-sided p that t > critical
    t_lower = (beta + sesoi) / se
    p_lower = 1 - stats.norm.cdf(t_lower)  # P(Z > t_lower) under H0_lower
    # Upper bound: t = (beta - (+sesoi)) / se = (beta - sesoi) / se; we want one-sided p that t < critical
    t_upper = (beta - sesoi) / se
    p_upper = stats.norm.cdf(t_upper)  # P(Z < t_upper) under H0_upper
    p_tost = max(p_lower, p_upper)
    # 90% CI for equivalence inference (TOST uses 90% CI, equivalent to alpha=0.05 each side)
    ci_low = beta - 1.645 * se
    ci_high = beta + 1.645 * se
    equiv_at_05 = (ci_low > -sesoi) and (ci_high < sesoi)
    return {
        "label": label,
        "beta": beta,
        "se": se,
        "n_obs": n_obs,
        "sesoi": sesoi,
        "ci90_low": ci_low,
        "ci90_high": ci_high,
        "p_lower": float(p_lower),
        "p_upper": float(p_upper),
        "p_tost": float(p_tost),
        "equivalent_at_alpha_0.05": bool(equiv_at_05),
        "interpretation": (
            f"At alpha=0.05 (TOST 90% CI): 90% CI [{ci_low:.4f}, {ci_high:.4f}] "
            + ("lies within" if equiv_at_05 else "does NOT lie entirely within")
            + f" the equivalence bound (±{sesoi}). "
            + ("Effect is statistically equivalent to zero against SESOI |β|=" + str(sesoi)
               if equiv_at_05 else
               "Cannot reject the possibility of an effect as large as ±" + str(sesoi))
        ),
    }


# Canonical values
# Pull Model 5 redistribution from rs_results.csv
rs = pd.read_csv(REPO / "outputs/tables/rs_results.csv")
m5 = rs[rs["model"] == "M5_redistribution_rs"].iloc[0]
m5_beta = float(m5["int_task_z:welfare_regime[T.Liberal]"])
m5_se = float(m5["int_task_z:welfare_regime[T.Liberal]_se"])
m5_n = int(m5["n_obs"])

# ISSP 2006 values (from paper Appendix C / scripts/issp_solidarity_leg.py)
issp_beta = 0.010
issp_se = 0.016
issp_n = 10216

# Exclusion-side moderation (M3 CWED) for reference — what the symmetric account predicts magnitude-wise
m3 = rs[rs["model"] == "M3_cwed_rs"].iloc[0]
m3_beta = float(m3["int_task_z:cwed_generosity_z"])

# SESOI choices: 0.06 (slightly above the exclusion-side magnitude), 0.05 (closer), 0.03 (half)
SESOIS = [0.06, 0.05, 0.03]

results = []
for label, beta, se, n in [
    ("ESS Model 5 redistribution × Liberal (RS)", m5_beta, m5_se, m5_n),
    ("ISSP 2006 RTI × CWED (paraphrase)", issp_beta, issp_se, issp_n),
]:
    for sesoi in SESOIS:
        results.append(tost(beta, se, n, sesoi, f"{label} | SESOI={sesoi}"))

df = pd.DataFrame(results)
df.to_csv(OUT_DIR / "tost_equivalence_test.csv", index=False)

# Top-line summary
summary = {
    "reference_exclusion_moderation": {
        "model": "M3 CWED random-slopes",
        "beta": m3_beta,
        "note": "The symmetric account predicts solidarity-side moderation of comparable magnitude. SESOI choices test against |β| of 0.06 (slightly above exclusion-side), 0.05 (matched), and 0.03 (half).",
    },
    "ess_model5_liberal": {
        "beta": m5_beta,
        "se": m5_se,
        "n": m5_n,
        "tost_results_by_sesoi": {
            r["sesoi"]: {
                "equivalent_at_alpha_0.05": r["equivalent_at_alpha_0.05"],
                "p_tost": r["p_tost"],
                "ci90": [r["ci90_low"], r["ci90_high"]],
            }
            for r in results[:3]
        },
    },
    "issp_2006_rti_cwed": {
        "beta": issp_beta,
        "se": issp_se,
        "n": issp_n,
        "tost_results_by_sesoi": {
            r["sesoi"]: {
                "equivalent_at_alpha_0.05": r["equivalent_at_alpha_0.05"],
                "p_tost": r["p_tost"],
                "ci90": [r["ci90_low"], r["ci90_high"]],
            }
            for r in results[3:]
        },
    },
    "headline_interpretation": (
        f"ESS Model 5 (β={m5_beta:.4f}, SE={m5_se:.4f}, N={m5_n:,}): "
        + ("TOST rejects the symmetric prediction at SESOI=0.06" if results[0]["equivalent_at_alpha_0.05"]
           else "TOST does NOT reject the symmetric prediction at SESOI=0.06")
        + ". ISSP (β=0.010, SE=0.016, N=10,216): "
        + ("TOST rejects at SESOI=0.06" if results[3]["equivalent_at_alpha_0.05"]
           else "TOST does NOT reject at SESOI=0.06")
        + ". "
    ),
}

with (OUT_DIR / "tost_summary.json").open("w") as f:
    json.dump(summary, f, indent=2, default=str)

print(json.dumps(summary, indent=2, default=str))
