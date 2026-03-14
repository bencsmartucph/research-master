"""
setup_data_raw.py
=================
ONE-TIME SETUP SCRIPT — run this once to populate data/raw/ with clean slug folders.

This copies all replication data from the original 'ACTUALLY GOOD/' folder into
Research_Master/data/raw/ with clean, readable folder names (slugs).

HOW TO RUN
----------
1. Open a terminal (PowerShell or Command Prompt)
2. Navigate to the Research_Master folder:
       cd "C:\\path\\to\\Economics of the Welfare State\\Data\\Research_Master"
   OR if you've moved Research_Master to Desktop:
       cd "C:\\Users\\PKF715\\Desktop\\Research_Master"
3. Run:
       python setup_data_raw.py

WHAT IT DOES
------------
- Reads from:  ../ACTUALLY GOOD/   (sibling of Research_Master inside Data/)
  OR set SOURCE_DIR below to wherever ACTUALLY GOOD/ lives on your machine
- Copies to:   data/raw/           (inside Research_Master)
- Renames folders using SLUG_MAP (messy → clean names)
- Skips __MACOSX and ._ junk files
- Skips any folder already in data/raw/ (safe to re-run)
- Prints a summary at the end

TIME: Expect ~5–15 minutes for 2.5GB depending on disk speed.

NOTE: Originals in ACTUALLY GOOD/ are NOT touched.
"""

import os
import shutil

# ── Config ────────────────────────────────────────────────────────────────────

# Where to find the original ACTUALLY GOOD/ folder.
# By default this assumes Research_Master is inside Data/ (i.e. Data/Research_Master/).
# If you've moved Research_Master elsewhere, update this to the absolute path.
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR   = os.path.join(SCRIPT_DIR, "..", "ACTUALLY GOOD")
DEST_DIR     = os.path.join(SCRIPT_DIR, "data", "raw")

# Mapping from messy folder names → clean slugs
SLUG_MAP = {
    "0 - Gingrich Did State Responses to Automation Matter for Voters":
        "gingrich_2019",
    "0 - Kurer - The Declining Middle Occupational Change, Social Status, and the Populist Right":
        "kurer_2020_declining_middle",
    "0 - Kurer - Disappointed Expectations":
        "kurer_2022_disappointed_expectations",
    "0 - SIWE_beta_May2017":
        "siwe_2017",
    "1 - Aspiration versus Apprehension":
        "aspiration_apprehension",
    "1 - Baccini 2024 - Austerity, Economic Vulnerability, and Populism":
        "baccini_2024",
    "1 - Gugushvii - 2025 - Downward Class Mobility and Far-Right Party Support in Western Europeow":
        "gugushvili_2025",
    "1 - Im -  A Reservoir of Votes for the Radical Right":
        "im_2021",
    "1 - Milner - Voting for Populism -  Globalization, Technological Change, and the Extreme Right":
        "milner_2021",
    "2 - Euroscepticism as a syndrome of stagnation":
        "euroscepticism_stagnation",
    "2 - Silva -  Well-being foundations of populism in Europe":
        "silva_wellbeing",
    "2 - Steiner- Left Behind and United by Populism":
        "steiner_left_behind",
    "3 - 2022 - Langenkamp  Populism and Layers of Social Belonging":
        "langenkamp_2022",
    "3 - How (not) to explain the rise of authoritarian populism":
        "how_not_authoritarian_populism",
    "3 - cicollini":
        "cicollini_2025",
    "3 - conflicting A decline in the social status of the working class":
        "status_decline_working_class",
    "4- Broz The Economic Geography of the Globalization Backlash":
        "broz_2019",
    "Automation data for occupations in Europe doi-10.34894-fvtr7s":
        "shared_isco_task_scores",
    "armaly- The Disparate Correlates of Populist Support in the United States":
        "armaly_us",
}

# ── Validate ──────────────────────────────────────────────────────────────────

SOURCE_DIR = os.path.normpath(SOURCE_DIR)
DEST_DIR   = os.path.normpath(DEST_DIR)

if not os.path.isdir(SOURCE_DIR):
    print(f"\n❌ ERROR: Cannot find source folder:\n   {SOURCE_DIR}")
    print("\nFix: Open setup_data_raw.py and set SOURCE_DIR to the absolute path of your ACTUALLY GOOD/ folder.")
    exit(1)

os.makedirs(DEST_DIR, exist_ok=True)

# ── Copy ──────────────────────────────────────────────────────────────────────

print(f"\nSource:      {SOURCE_DIR}")
print(f"Destination: {DEST_DIR}\n")

copied   = []
skipped  = []
unmapped = []

for folder_name in os.listdir(SOURCE_DIR):
    src = os.path.join(SOURCE_DIR, folder_name)
    if not os.path.isdir(src):
        continue

    slug = SLUG_MAP.get(folder_name)
    if slug is None:
        unmapped.append(folder_name)
        print(f"  ⚠️  No slug for: {folder_name}")
        continue

    dest = os.path.join(DEST_DIR, slug)
    if os.path.exists(dest):
        skipped.append(slug)
        print(f"  ⏭️  Skipping (already exists): {slug}")
        continue

    print(f"  📂 Copying: {folder_name}\n       → {slug}")
    shutil.copytree(
        src,
        dest,
        ignore=shutil.ignore_patterns("__MACOSX", "._*", ".DS_Store")
    )
    copied.append(slug)

# ── Summary ───────────────────────────────────────────────────────────────────

print(f"\n{'='*60}")
print(f"✅ Copied:   {len(copied)} folders")
print(f"⏭️  Skipped:  {len(skipped)} (already existed)")
if unmapped:
    print(f"⚠️  Unmapped: {len(unmapped)} (no slug defined — see list above)")
print(f"\ndata/raw/ is now at: {DEST_DIR}")

# Write/update MANIFEST.json
import json
from datetime import datetime

manifest = {}
for slug in os.listdir(DEST_DIR):
    slug_path = os.path.join(DEST_DIR, slug)
    if not os.path.isdir(slug_path):
        continue
    files = []
    total_bytes = 0
    for root, dirs, fnames in os.walk(slug_path):
        dirs[:] = [d for d in dirs if d not in ("__MACOSX",)]
        for f in fnames:
            if f.startswith("._") or f == ".DS_Store":
                continue
            fp = os.path.join(root, f)
            sz = os.path.getsize(fp)
            files.append(os.path.relpath(fp, slug_path))
            total_bytes += sz
    manifest[slug] = {
        "file_count": len(files),
        "total_mb": round(total_bytes / 1_000_000, 1),
        "files": sorted(files)
    }

manifest_path = os.path.join(DEST_DIR, "MANIFEST.json")
with open(manifest_path, "w") as f:
    json.dump({
        "generated": datetime.now().isoformat()[:10],
        "total_folders": len(manifest),
        "folders": manifest
    }, f, indent=2)

print(f"\nMANIFEST.json updated: {manifest_path}")
print("="*60)
print("\nDone! Research_Master/data/raw/ is fully populated.")
print("You can now move Research_Master anywhere on your computer.")
