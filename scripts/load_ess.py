"""
ESS Loader Utility
==================
Reusable functions for loading, labelling, and merging European Social Survey data.

Usage:
    from scripts.load_ess import load_ess_wave, load_pooled_ess, attach_rti_scores

All paths are relative to the Data/ root directory.
"""

import os
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np

try:
    import pyreadstat
    HAS_PYREADSTAT = True
except ImportError:
    HAS_PYREADSTAT = False
    print("Warning: pyreadstat not installed. Install with: pip install pyreadstat")


# ── Path configuration ────────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ESS_WAVE_PATHS = {
    1: "data/raw/gugushvili_2025/ESS1e06_7 (1)/ESS1e06_7.dta",
    2: "data/raw/gugushvili_2025/ESS2e03_6 (1)/ESS2e03_6.dta",
    3: "data/raw/gugushvili_2025/ESS3e03_7 (1)/ESS3e03_7.dta",
    4: "data/raw/gugushvili_2025/ESS4e04_6/ESS4e04_6.dta",
    5: "data/raw/gugushvili_2025/ESS5e03_5/ESS5e03_5.dta",
    # For waves 6+, use Baccini ESSdata or Im reservoir file
    "baccini_pool": "data/raw/baccini_2024/Replication V3/Data/Raw Data/Baciini - ESSdata.dta",
    "im_pool":      "data/raw/im_2021/Im - A Reservoir of Votes for the Radical Right - ESS.csv",
    "cicollini":    "data/raw/cicollini_2025/essprt-all.dta",
}

TASK_FILE = "data/raw/aspiration_apprehension/isco08_3d-task3.csv"
CROSSWALK_FILE = "data/raw/langenkamp_2022/ess_populist_crosswalk.csv"
CORRESPONDENCE_FILE = "data/raw/kurer_2020_declining_middle/cps-19-0286replication/CPS-19-0286(Replication)/correspondence.dta"


# ── Core loading functions ────────────────────────────────────────────────────

def load_ess_wave(wave, cols=None, countries=None, sample_only=False):
    """
    Load a single ESS wave.

    Parameters
    ----------
    wave : int (1–5) or str ("baccini_pool", "im_pool", "cicollini")
    cols : list of str, optional — select specific columns
    countries : list of str, optional — e.g. ["DE", "FR", "GB"]
    sample_only : bool — load from data/samples/stratified/ instead of full file

    Returns
    -------
    pd.DataFrame
    """
    if sample_only:
        sample_map = {
            1: "data/samples/stratified/ESS1e06_7_strat25.csv",
            2: "data/samples/stratified/ESS2e03_6_strat25.csv",
            3: "data/samples/stratified/ESS3e03_7_strat30.csv",
            4: "data/samples/stratified/ESS4e04_6_strat30.csv",
            5: "data/samples/stratified/ESS5e03_5_strat30.csv",
        }
        path = os.path.join(ROOT, sample_map.get(wave, ""))
        if not os.path.exists(path):
            raise FileNotFoundError(f"No stratified sample for wave {wave}. Run make_stratified_samples.py first.")
        df = pd.read_csv(path, low_memory=False)
    else:
        rel_path = ESS_WAVE_PATHS.get(wave)
        if rel_path is None:
            raise ValueError(f"Unknown wave: {wave}. Options: {list(ESS_WAVE_PATHS.keys())}")
        path = os.path.join(ROOT, rel_path)
        ext = os.path.splitext(path)[1].lower()
        if ext == ".dta":
            assert HAS_PYREADSTAT, "pyreadstat required for .dta files"
            df, meta = pyreadstat.read_dta(path)
        else:
            df = pd.read_csv(path, low_memory=False, encoding="latin-1")

    if isinstance(wave, int):
        df["essround"] = wave

    if countries:
        df = df[df["cntry"].isin(countries)]

    if cols:
        present = [c for c in cols if c in df.columns]
        missing = [c for c in cols if c not in df.columns]
        if missing:
            print(f"  ⚠️ Columns not found in wave {wave}: {missing}")
        df = df[present]

    return df


def load_pooled_ess(waves=None, cols=None, countries=None, sample_only=False):
    """
    Load and pool multiple ESS waves (1–5 from Gugushvili files).

    Parameters
    ----------
    waves : list of int, default [1, 2, 3, 4, 5]
    cols : list of str — select these columns (intersected per wave)
    countries : list of str — filter to these ISO-2 country codes
    sample_only : bool — use stratified samples for development

    Returns
    -------
    pd.DataFrame with added 'essround' column
    """
    if waves is None:
        waves = [1, 2, 3, 4, 5]

    frames = []
    for w in waves:
        try:
            df_w = load_ess_wave(w, cols=cols, countries=countries, sample_only=sample_only)
            frames.append(df_w)
            print(f"  Loaded wave {w}: {len(df_w):,} rows")
        except Exception as e:
            print(f"  ⚠️ Wave {w} failed: {e}")

    if not frames:
        raise RuntimeError("No waves loaded successfully.")

    return pd.concat(frames, ignore_index=True, sort=False)


# ── Occupation task score merger ──────────────────────────────────────────────

def attach_rti_scores(df, isco_col="isco08"):
    """
    Merge Routine Task Intensity (RTI) scores onto a dataframe.

    Loads isco08_3d-task3.csv and merges by 3-digit ISCO-08 code.
    Adds columns: rtask, nrtask (and any other task score columns present).

    Parameters
    ----------
    df : pd.DataFrame with an ISCO-08 column
    isco_col : str — name of the ISCO-08 column (default 'isco08')

    Returns
    -------
    pd.DataFrame with task score columns added
    """
    task_path = os.path.join(ROOT, TASK_FILE)
    if not os.path.exists(task_path):
        raise FileNotFoundError(f"Task file not found: {task_path}")

    tasks = pd.read_csv(task_path, low_memory=False)
    print(f"  Task file columns: {list(tasks.columns)}")

    # Find the ISCO-3d column in task file
    isco_key = None
    for candidate in ["isco08_3d", "isco3d", "isco08", "isco"]:
        if candidate in tasks.columns:
            isco_key = candidate
            break
    if isco_key is None:
        raise ValueError(f"Could not find ISCO column in task file. Columns: {list(tasks.columns)}")

    # Create 3-digit ISCO in df
    if isco_col in df.columns:
        df = df.copy()
        df["isco08_3d"] = (pd.to_numeric(df[isco_col], errors="coerce") / 10).astype("Int64")
        tasks[isco_key] = pd.to_numeric(tasks[isco_key], errors="coerce").astype("Int64")
        df = df.merge(tasks.rename(columns={isco_key: "isco08_3d"}), on="isco08_3d", how="left")
        n_matched = df["isco08_3d"].notna().sum()
        print(f"  RTI merge: {n_matched:,}/{len(df):,} rows matched")
    else:
        print(f"  ⚠️ Column '{isco_col}' not found in dataframe. Available: {list(df.columns[:10])}")

    return df


# ── Populist party crosswalk ──────────────────────────────────────────────────

def attach_populist_flag(df, cntry_col="cntry", round_col="essround"):
    """
    Attach a populist party flag using the Langenkamp crosswalk.

    The crosswalk maps ESS country-specific party vote codes to a populist
    party classification. Requires cntry and essround in the dataframe.

    Parameters
    ----------
    df : pd.DataFrame with ESS data
    cntry_col : str
    round_col : str

    Returns
    -------
    pd.DataFrame with 'populist_vote' column added
    """
    xwalk_path = os.path.join(ROOT, CROSSWALK_FILE)
    if not os.path.exists(xwalk_path):
        print(f"  ⚠️ Crosswalk file not found: {xwalk_path}")
        return df

    xwalk = pd.read_csv(xwalk_path, low_memory=False)
    print(f"  Crosswalk loaded: {len(xwalk):,} rows, columns: {list(xwalk.columns[:8])}")

    # The crosswalk structure varies — inspect it to build the correct merge
    # This is a placeholder merge — adjust column names after inspecting:
    # df = df.merge(xwalk[['cntry', 'essround', 'party_code', 'populist']], on=['cntry', 'essround', ...])
    print("  ⚠️ Crosswalk merge logic requires customisation. Inspect crosswalk columns first.")
    print(f"     Crosswalk columns: {list(xwalk.columns)}")

    return df


# ── ISCO → EGP class scheme ───────────────────────────────────────────────────

def attach_egp_class(df, isco_col="isco08", father_isco_col=None):
    """
    Attach Erikson-Goldthorpe-Portocarero (EGP) class scheme.
    Uses Kurer's correspondence.dta crosswalk file.

    Parameters
    ----------
    df : pd.DataFrame
    isco_col : str — respondent's ISCO code column
    father_isco_col : str — father's ISCO code column (optional)

    Returns
    -------
    pd.DataFrame with 'egp_class' (and optionally 'egp_class_father') added
    """
    corr_path = os.path.join(ROOT, CORRESPONDENCE_FILE)
    if not os.path.exists(corr_path):
        alt = "data/raw/kurer_2020_declining_middle/replication_files/replication_files/correspondence.dta"
        corr_path = os.path.join(ROOT, alt)

    if not os.path.exists(corr_path):
        print(f"  ⚠️ Correspondence file not found. EGP class not attached.")
        return df

    assert HAS_PYREADSTAT
    corr, _ = pyreadstat.read_dta(corr_path)
    print(f"  Correspondence file columns: {list(corr.columns)}")
    print("  ⚠️ EGP merge requires inspecting correspondence.dta structure. Placeholder only.")
    # Build merge after inspecting: corr likely has isco88/isco08 → egp mapping

    return df


# ── Quick inspection helper ───────────────────────────────────────────────────

def quick_info(df, name="df"):
    """Print quick descriptive info about a dataframe."""
    print(f"\n── {name} ─────────────────────────────")
    print(f"  Shape:    {df.shape[0]:,} rows × {df.shape[1]} cols")
    if "cntry" in df.columns:
        print(f"  Countries ({df['cntry'].nunique()}): {sorted(df['cntry'].dropna().unique())}")
    if "essround" in df.columns:
        print(f"  ESS rounds: {sorted(df['essround'].dropna().unique())}")
    missing = (df.isna().mean() * 100).round(1)
    high_miss = missing[missing > 30]
    if len(high_miss):
        print(f"  High missingness (>30%): {len(high_miss)} columns")
    print(f"  Columns: {list(df.columns[:10])}{'...' if df.shape[1] > 10 else ''}")


# ── Example / demo ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("ESS Loader — Demo (sample mode)")
    print("=" * 50)

    # Demo: load stratified sample of waves 1 and 2
    df = load_pooled_ess(waves=[1, 2], sample_only=True)
    quick_info(df, "Pooled ESS (waves 1-2, sample)")

    # Demo: attach RTI scores
    if "isco08" in df.columns:
        df = attach_rti_scores(df)
        if "rtask" in df.columns:
            print(f"\n  RTI stats: mean={df['rtask'].mean():.3f}, sd={df['rtask'].std():.3f}")

    print("\nReady. Import this module in your analysis scripts:")
    print("  from scripts.load_ess import load_pooled_ess, attach_rti_scores, quick_info")
