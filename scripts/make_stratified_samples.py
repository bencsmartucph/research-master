"""
Stratified Sample Generator
============================
Creates stratified 200-row samples for large ACTUALLY GOOD datasets (>10MB).

Unlike the top-100 samples (which cluster on early rows = single countries),
these samples are stratified by `cntry` and/or `essround` to give cross-national
coverage — essential for developing cross-national analysis code.

Usage:
    python scripts/make_stratified_samples.py

Outputs to: data/samples/stratified/
"""

import os
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import pyreadstat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AG = os.path.join(ROOT, "ACTUALLY GOOD")
SAMPLES_DIR = os.path.join(ROOT, "samples", "stratified")
os.makedirs(SAMPLES_DIR, exist_ok=True)

SAMPLE_N = 200  # total rows per sample
ROWS_PER_STRATUM = 5  # rows per country (or country-wave combination)

def stratified_sample(df, strat_cols, n_per_stratum=ROWS_PER_STRATUM, total=SAMPLE_N):
    """Draw n_per_stratum rows per stratum, cap at total rows."""
    available = [c for c in strat_cols if c in df.columns]
    if not available:
        return df.head(total)
    group_col = available[0]  # use first available stratum column
    sampled = (
        df.groupby(group_col, group_keys=False)
        .apply(lambda g: g.sample(min(len(g), n_per_stratum), random_state=42))
    )
    return sampled.head(total)

def try_read_dta(path, row_limit=5000):
    for enc in ["utf-8", "latin-1", "cp1252", None]:
        try:
            kwargs = {"row_limit": row_limit}
            if enc:
                kwargs["encoding"] = enc
            df, meta = pyreadstat.read_dta(path, **kwargs)
            return df, meta
        except Exception:
            continue
    return None, None

def try_read_csv(path, nrows=5000):
    for enc in ["utf-8", "latin-1", "cp1252"]:
        try:
            return pd.read_csv(path, nrows=nrows, low_memory=False, encoding=enc), None
        except Exception:
            continue
    return None, None

# ── Target files (>10MB in ACTUALLY GOOD, not yet sampled or worth stratifying) ──

targets = [
    # ESS files (Gugushvili) — need stratified sample by cntry
    {
        "path": "1 - Gugushvii - 2025 - Downward Class Mobility and Far-Right Party Support in Western Europeow/ESS1e06_7 (1)/ESS1e06_7.dta",
        "slug": "ESS1e06_7", "strat": ["cntry"], "note": "ESS wave 1 (Gugushvili)",
    },
    {
        "path": "1 - Gugushvii - 2025 - Downward Class Mobility and Far-Right Party Support in Western Europeow/ESS2e03_6 (1)/ESS2e03_6.dta",
        "slug": "ESS2e03_6", "strat": ["cntry"], "note": "ESS wave 2 (Gugushvili)",
    },
    {
        "path": "1 - Gugushvii - 2025 - Downward Class Mobility and Far-Right Party Support in Western Europeow/ESS3e03_7 (1)/ESS3e03_7.dta",
        "slug": "ESS3e03_7", "strat": ["cntry"], "note": "ESS wave 3 (Gugushvili)",
    },
    {
        "path": "1 - Gugushvii - 2025 - Downward Class Mobility and Far-Right Party Support in Western Europeow/ESS4e04_6/ESS4e04_6.dta",
        "slug": "ESS4e04_6", "strat": ["cntry"], "note": "ESS wave 4 (Gugushvili)",
    },
    {
        "path": "1 - Gugushvii - 2025 - Downward Class Mobility and Far-Right Party Support in Western Europeow/ESS5e03_5/ESS5e03_5.dta",
        "slug": "ESS5e03_5", "strat": ["cntry"], "note": "ESS wave 5 (Gugushvili)",
    },
    # Cicollini — stratify by cntry + essround
    {
        "path": "3 - cicollini/essprt-all.dta",
        "slug": "cicollini_essprt_all", "strat": ["cntry", "essround"], "note": "Cicollini: ESS with positional income change",
    },
    # Milner merged — stratify by country
    {
        "path": "1 - Milner - Voting for Populism -  Globalization, Technological Change, and the Extreme Right/data/data/imputed/imputed_econdata_voteshare_merged.dta",
        "slug": "milner_merged_regional", "strat": ["country", "cntry", "nuts2", "nuts"], "note": "Milner: analysis-ready regional merged data",
    },
    # Gingrich ISSP ZA-files (sample the largest ones; rest are manageable)
    {
        "path": "0 - Gingrich Did State Responses to Automation Matter for Voters/ZA6770_v2-1-0.dta/ZA6770_v2-1-0.dta",
        "slug": "ZA6770_ISSP2016", "strat": ["V3", "COUNTRY"], "note": "Gingrich: ISSP 2016 Role of Government V",
    },
    {
        "path": "0 - Gingrich Did State Responses to Automation Matter for Voters/ZA5400_v4-0-0.dta/ZA5400_v4-0-0.dta",
        "slug": "ZA5400_ISSP2010", "strat": ["V3", "COUNTRY"], "note": "Gingrich: ISSP 2010 Environment III",
    },
    {
        "path": "0 - Gingrich Did State Responses to Automation Matter for Voters/ZA4950_v2-3-0.dta/ZA4950_v2-3-0.dta",
        "slug": "ZA4950_ISSP2009", "strat": ["V3", "COUNTRY"], "note": "Gingrich: ISSP 2009 Social Inequality IV",
    },
    # Baccini district and individual analysis-ready files
    {
        "path": "1 - Baccini 2024 - Austerity, Economic Vulnerability, and Populism/Replication V3/Data/individualdata.dta",
        "slug": "baccini_individualdata", "strat": ["cntry", "country"], "note": "Baccini: analysis-ready individual data",
    },
    {
        "path": "1 - Baccini 2024 - Austerity, Economic Vulnerability, and Populism/Replication V3/Data/Raw Data/Analysis_Dataset_District_Level.dta",
        "slug": "baccini_district_level", "strat": ["cntry", "country", "nuts2"], "note": "Baccini: district-level analysis data",
    },
    # Steiner ZA7700
    {
        "path": "2 - Steiner- Left Behind and United by Populism/data_raw/ZA7700_v2-0-0-mv.dta",
        "slug": "ZA7700_steiner", "strat": ["V3", "COUNTRY", "country"], "note": "Steiner: ISSP 2019 Social Inequality",
    },
    # Euroscepticism .dta
    {
        "path": "2 - Euroscepticism as a syndrome of stagnation/Euroscepticism as a syndrome of stagnation - Data for replication-1.dta",
        "slug": "euroscepticism_dta", "strat": ["cntry", "country", "V3"], "note": "Euroscepticism replication .dta",
    },
]

results = []
for t in targets:
    full_path = os.path.join(AG, t["path"])
    if not os.path.exists(full_path):
        print(f"  ⚠️  Not found: {t['path'][:60]}")
        continue

    size_mb = os.path.getsize(full_path) / 1e6
    slug = t["slug"]
    note = t["note"]
    ext = os.path.splitext(full_path)[1].lower()

    print(f"\n📂 [{size_mb:.0f}MB] {slug}")
    print(f"   {note}")

    try:
        if ext == ".dta":
            df, meta = try_read_dta(full_path, row_limit=10000)
        else:
            df, _ = try_read_csv(full_path, nrows=10000)

        if df is None:
            print(f"   ❌ Could not read")
            continue

        sample = stratified_sample(df, t["strat"])
        n_rows, n_cols = sample.shape

        # Save CSV
        out_csv = os.path.join(SAMPLES_DIR, f"{slug}_strat{n_rows}.csv")
        sample.to_csv(out_csv, index=False, encoding="utf-8", errors="replace")

        # Report strata coverage
        for col in t["strat"]:
            if col in sample.columns:
                n_strata = sample[col].nunique()
                print(f"   ✅ {n_rows} rows × {n_cols} cols | {n_strata} unique '{col}' values")
                break
        else:
            print(f"   ✅ {n_rows} rows × {n_cols} cols (no strat col found, top-N used)")

        results.append({
            "slug": slug, "note": note, "rows": n_rows, "cols": n_cols,
            "file": os.path.basename(out_csv),
        })

    except Exception as e:
        print(f"   ❌ Error: {e}")

# ── README ──
readme_lines = [
    "# Stratified Samples",
    "",
    "> Stratified by `cntry` / `essround` / `country` to give cross-national coverage.",
    "> Each file has ~5 rows per country (or country-wave), up to 200 rows total.",
    "> Use these for developing and debugging multi-country analysis code.",
    "",
    "| File | Description | Rows | Cols |",
    "|------|-------------|------|------|",
]
for r in results:
    readme_lines.append(f"| `{r['file']}` | {r['note']} | {r['rows']} | {r['cols']} |")

readme_lines += [
    "",
    "## How to use",
    "",
    "```python",
    "import pandas as pd",
    "df = pd.read_csv('data/samples/stratified/ESS1e06_7_strat200.csv')",
    "# Develop your cross-national analysis code here",
    "# Then switch to the full file:",
    "# import pyreadstat",
    "# df, meta = pyreadstat.read_dta('data/raw/gugushvili_2025/ESS1e06_7.dta')",
    "```",
    "",
    "## Regenerate",
    "",
    "```bash",
    "python scripts/make_stratified_samples.py",
    "```",
]

with open(os.path.join(SAMPLES_DIR, "README.md"), "w") as f:
    f.write("\n".join(readme_lines))

print(f"\n✅ Done. {len(results)} stratified samples created in {SAMPLES_DIR}")
