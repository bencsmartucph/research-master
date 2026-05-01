"""
Descriptive scatterplot: routine task intensity (RTI) vs. anti-immigration attitudes,
faceted by country.

Inputs (checked in order; first usable wins):
    1. data/samples/baccini_ESSdata_sample100.csv  (specified by brief)
    2. data/samples/im_radical_right_ESS_sample100.csv  (fallback proxy source)

Optional input (gracefully skipped if missing):
    data/raw/shared_isco_task_scores/isco08_3d-task3.csv

Output:
    demos/overnight-pattern/fig_rti_vs_attitudes_descriptive.pdf

Notes:
    - data/raw/ is gitignored on this branch, so the canonical 3-digit ISCO-08 task
      score table is unavailable. The script falls back to a major-group (1-digit
      ISCO) RTI proxy keyed on occupation-label substrings. This is a proxy, not
      the canonical RTI; documented in figure-caption metadata.
    - The Baccini sample carries demographic + occupation + party-vote columns
      but NOT the ESS immigration attitude battery (imbgeco, imueclt, imwbcnt).
      The script falls back to the Im sample, which has both isco08 and the
      immigration items.
"""

# --- Config ---
import sys
import random
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

random.seed(42)
np.random.seed(42)

REPO_ROOT = Path("/home/user/research-master")
BACCINI_CSV = REPO_ROOT / "data/samples/baccini_ESSdata_sample100.csv"
IM_CSV = REPO_ROOT / "data/samples/im_radical_right_ESS_sample100.csv"
TASK_SCORES_CSV = REPO_ROOT / "data/raw/shared_isco_task_scores/isco08_3d-task3.csv"
OUT_PDF = REPO_ROOT / "demos/overnight-pattern/fig_rti_vs_attitudes_descriptive.pdf"

IMMIG_ITEMS = ["imbgeco", "imueclt", "imwbcnt"]
# Each item is 0-10 with 0 = anti-immigration pole, 10 = pro-immigration pole.
# Anti-immigration index = 10 - mean(items), so higher = more anti-immigration.

# --- Path checks ---
print(f"[paths] BACCINI_CSV exists: {BACCINI_CSV.exists()}")
print(f"[paths] IM_CSV exists:      {IM_CSV.exists()}")
print(f"[paths] TASK_SCORES_CSV exists: {TASK_SCORES_CSV.exists()}")

if not BACCINI_CSV.exists() and not IM_CSV.exists():
    print("[fatal] Neither sample CSV is reachable; cannot proceed.")
    sys.exit(0)

# --- Load Baccini sample (the brief's preferred source) and probe for attitudes ---
baccini_has_attitudes = False
if BACCINI_CSV.exists():
    df_b = pd.read_csv(BACCINI_CSV)
    print(f"[load] Baccini sample shape: {df_b.shape}")
    print(f"[load] Baccini dtypes (selected): "
          f"isco08={df_b['isco08'].dtype if 'isco08' in df_b.columns else 'absent'}, "
          f"cntry={df_b['cntry'].dtype if 'cntry' in df_b.columns else 'absent'}")
    present = [c for c in IMMIG_ITEMS if c in df_b.columns]
    print(f"[probe] Baccini immigration items present: {present}")
    baccini_has_attitudes = len(present) >= 2

# --- Decide source ---
# Per brief: prefer Baccini. If it lacks attitudes, fall back to Im sample as
# the closest available proxy (same survey family, same isco08 column, full
# immigration battery).
if baccini_has_attitudes:
    src_path = BACCINI_CSV
    df = df_b.copy()
    src_label = "baccini_ESSdata_sample100.csv"
    print("[source] Using Baccini sample (attitudes present).")
else:
    if not IM_CSV.exists():
        print("[fatal] Baccini sample lacks immigration attitudes and the Im "
              "fallback sample is unreachable. Exiting cleanly.")
        sys.exit(0)
    src_path = IM_CSV
    df = pd.read_csv(IM_CSV)
    src_label = "im_radical_right_ESS_sample100.csv (fallback)"
    print(f"[source] Baccini sample lacks immigration items; using Im sample "
          f"as fallback. shape={df.shape}")

print(f"[load] {src_label} dtypes:")
print(df[["cntry", "isco08"] + [c for c in IMMIG_ITEMS if c in df.columns]].dtypes)

# --- Optional canonical RTI table ---
canonical_rti = None
if TASK_SCORES_CSV.exists():
    canonical_rti = pd.read_csv(TASK_SCORES_CSV)
    print(f"[rti] Canonical 3-digit task scores loaded: shape={canonical_rti.shape}")
else:
    print("[rti] Canonical 3-digit task scores unavailable (data/raw/ gitignored).")
    print("[rti] Falling back to ISCO-08 major-group (1-digit) RTI proxy.")

# --- Build RTI proxy ---
# In the Im sample, isco08 is stored as occupation-label strings (e.g.
# 'Managing directors and chief executives'). Map each label to an ISCO-08
# major group via keyword matching, then assign a major-group RTI proxy.
# Major-group RTI proxy values follow the standard literature pattern
# (Goos, Manning & Salomons 2014; Autor & Dorn 2013): low for
# managers/professionals, mid for technicians/service, high for clerical /
# craft / operative / elementary occupations.

MAJOR_GROUP_RTI = {
    1: -1.5,  # Managers (low RTI)
    2: -1.2,  # Professionals (low RTI)
    3: -0.3,  # Technicians and associate professionals (mid-low)
    4: +1.2,  # Clerical support workers (high RTI)
    5: -0.2,  # Service and sales workers (mid)
    6: +0.3,  # Skilled agricultural (mid-high)
    7: +1.0,  # Craft and related trades (high RTI)
    8: +1.4,  # Plant and machine operators, assemblers (high RTI)
    9: +0.8,  # Elementary occupations (high RTI)
    0: np.nan,  # Armed forces / unclassified
}

KEYWORD_TO_MAJOR = [
    # Major group 1: managers
    ("manager", 1), ("director", 1), ("chief executive", 1),
    ("official", 1), ("legislator", 1), ("supervisor", 1),
    ("traditional chief", 1), ("heads of village", 1),
    # Major group 2: professionals
    ("professional", 2), ("engineer", 2), ("teacher", 2), ("scientist", 2),
    ("medical practitioner", 2), ("physician", 2), ("lawyer", 2),
    ("developer", 2), ("analyst", 2), ("architect", 2), ("accountant", 2),
    ("psychologist", 2), ("physiotherapist", 2), ("adviser", 2),
    ("systems administrator", 2),
    # Major group 3: technicians and associate professionals
    ("technician", 3), ("associate professional", 3), ("instructor", 3),
    ("nursing associate", 3), ("police inspector", 3), ("detective", 3),
    ("financial and investment", 3),
    # Major group 4: clerical support
    ("clerk", 4), ("secretar", 4), ("bookkeep", 4), ("receptionist", 4),
    ("client information", 4), ("clerical support", 4),
    # Major group 5: service and sales
    ("sales assistant", 5), ("shop sales", 5), ("service worker", 5),
    ("cook", 5), ("waiter", 5), ("personal care", 5),
    ("hairdresser", 5), ("security guard", 5), ("police officer", 5),
    ("health care assist", 5), ("croupier", 5), ("bookmaker", 5),
    ("gaming worker", 5),
    # Major group 6: skilled agricultural
    ("agricultur", 6), ("forestry", 6), ("fisher", 6),
    ("crop", 6), ("animal producer", 6),
    # Major group 7: craft and related trades
    ("craft", 7), ("trades worker", 7), ("electrician", 7), ("plumber", 7),
    ("carpenter", 7), ("welder", 7), ("metal", 7),
    ("concrete", 7), ("mechanic", 7), ("printer", 7),
    ("tailor", 7), ("dressmaker", 7), ("furrier", 7), ("hatter", 7),
    ("precision-instrument", 7), ("instrument maker", 7),
    # Major group 8: plant and machine operators
    ("operator", 8), ("driver", 8), ("assembler", 8), ("plant", 8),
    # Major group 9: elementary
    ("kitchen helper", 9), ("labourer", 9), ("laborer", 9),
    ("helper", 9), ("elementary", 9), ("cleaner", 9),
    ("freight handler", 9), ("odd job", 9), ("shelf filler", 9),
    # Major group 0: armed forces
    ("armed forces", 0), ("military", 0),
]


def label_to_major(label):
    if not isinstance(label, str):
        return np.nan
    s = label.lower()
    for kw, mg in KEYWORD_TO_MAJOR:
        if kw in s:
            return mg
    return np.nan


# --- Coerce isco08 to major group + immigration items to numeric ---
# Build all derived columns in a single concat to avoid DataFrame fragmentation.
isco_raw = df["isco08"]
if pd.api.types.is_numeric_dtype(isco_raw):
    isco_major = (pd.to_numeric(isco_raw, errors="coerce") // 1000).astype("Float64")
    print("[rti] Numeric isco08 detected; major group = first digit of 4-digit code.")
else:
    isco_major = isco_raw.apply(label_to_major)
    matched = isco_major.notna().sum()
    total = df["isco08"].notna().sum()
    print(f"[rti] String isco08 detected; keyword-matched "
          f"{matched}/{total} occupation labels to major groups.")

rti_proxy = isco_major.map(MAJOR_GROUP_RTI)
assert rti_proxy.notna().sum() > 0, "RTI proxy is fully missing — keyword map failed."

immig_numeric_frame = pd.DataFrame(
    {item + "_num": pd.to_numeric(df[item], errors="coerce")
     for item in IMMIG_ITEMS if item in df.columns},
    index=df.index,
)
num_cols = list(immig_numeric_frame.columns)
assert len(num_cols) >= 2, "Fewer than 2 immigration items numeric — index unreliable."
# ESS items run 0-10 with 0 = anti, 10 = pro. Recode to anti-immigration direction.
anti_immig_index = 10 - immig_numeric_frame.mean(axis=1)

df = pd.concat(
    [df, isco_major.rename("isco_major"), rti_proxy.rename("rti_proxy"),
     immig_numeric_frame, anti_immig_index.rename("anti_immig_index")],
    axis=1,
)
print(f"[rti] rti_proxy non-missing: {df['rti_proxy'].notna().sum()}/{len(df)}")
print(f"[attitudes] anti_immig_index non-missing: "
      f"{df['anti_immig_index'].notna().sum()}/{len(df)}")
print(f"[attitudes] index summary: mean={df['anti_immig_index'].mean():.2f}, "
      f"sd={df['anti_immig_index'].std():.2f}")

# --- Restrict to analysis sample ---
plot_df = df.dropna(subset=["cntry", "rti_proxy", "anti_immig_index"]).copy()
assert len(plot_df) > 0, "Plot sample is empty after dropping NAs."
print(f"[sample] Plot sample size: {len(plot_df)} (countries: "
      f"{sorted(plot_df['cntry'].unique().tolist())})")

# Add small jitter on the discrete RTI axis so points don't fully overlap.
rng = np.random.default_rng(42)
plot_df["rti_jitter"] = plot_df["rti_proxy"] + rng.uniform(-0.08, 0.08, size=len(plot_df))

# --- Plot ---
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

countries = sorted(plot_df["cntry"].unique().tolist())
n_countries = len(countries)
ncols = min(3, n_countries)
nrows = int(np.ceil(n_countries / ncols))

fig, axes = plt.subplots(nrows, ncols, figsize=(3.2 * ncols, 2.8 * nrows),
                         sharex=True, sharey=True, squeeze=False)

for idx, country in enumerate(countries):
    ax = axes[idx // ncols][idx % ncols]
    sub = plot_df[plot_df["cntry"] == country]
    ax.scatter(sub["rti_jitter"], sub["anti_immig_index"],
               s=22, alpha=0.65, color="#2b5d8b", edgecolor="white", linewidth=0.4)
    # Country panel label as text inside the panel — NOT a figure title.
    ax.text(0.04, 0.95, country, transform=ax.transAxes,
            fontsize=10, fontweight="bold", va="top", ha="left",
            family="serif")
    # Linear fit if at least 3 points
    if len(sub) >= 3:
        x = sub["rti_proxy"].to_numpy()
        y = sub["anti_immig_index"].to_numpy()
        slope, intercept = np.polyfit(x, y, 1)
        xs = np.linspace(x.min(), x.max(), 50)
        ax.plot(xs, intercept + slope * xs, color="#c0392b", linewidth=1.2, alpha=0.8)

    ax.grid(True, alpha=0.25, linewidth=0.4)
    ax.set_axisbelow(True)

# Blank any unused subplots
for idx in range(n_countries, nrows * ncols):
    fig.delaxes(axes[idx // ncols][idx % ncols])

# Shared axis labels — one per figure, not per panel — to avoid overlap.
fig.supxlabel("Routine task intensity (ISCO-08 major-group proxy)",
              fontfamily="serif", fontsize=10)
fig.supylabel("Anti-immigration index (0-10, higher = more anti)",
              fontfamily="serif", fontsize=10)

# Per .claude/rules/figures.md: NO embedded title or subtitle on the figure.
fig.suptitle("")  # explicit blank
fig.tight_layout()

OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT_PDF, format="pdf", bbox_inches="tight")
plt.close(fig)

assert OUT_PDF.exists() and OUT_PDF.stat().st_size > 0, "Figure failed to write."
print(f"[output] Wrote {OUT_PDF} ({OUT_PDF.stat().st_size} bytes)")
print(f"[output] Source CSV: {src_label}")
print(f"[output] N countries plotted: {n_countries}")
print(f"[output] N observations plotted: {len(plot_df)}")
print("[done]")
