# MEMORY.md — Persistent Research Discoveries

> This file captures corrections, discoveries, and hard-won knowledge from working sessions.
> Tag format: `[LEARN:category]` — categories: data, theory, code, notation, citation, method, pitfall
> 
> **How to use:** When you correct Claude mid-session, add a [LEARN] tag here.
> Run `/tools learn` (or ask Claude to formalise it into a skill) when a correction is multi-step.
> Claude should read this file at the start of every session that involves data or code.

---

## Data

- [LEARN:data] ESS vote variables are country-specific: `prtvtXXX` where XXX = 2-letter ISO code (e.g., `prtvtgb`, `prtvtde`). The `ess_populist_crosswalk.csv` in `data/raw/langenkamp_belonging/` harmonises these across waves.

- [LEARN:data] ISSP ZA-files use numeric codes for everything — country, occupation, political attitudes. ALWAYS load `meta.variable_value_labels` via pyreadstat before any recoding. Do not assume label meanings from column names.

- [LEARN:data] ESS ISCO-08 codes are 4-digit. The task score file (`isco08_3d-task3.csv`) uses 3-digit. Truncate with `df['isco08'] // 10` BEFORE merging. Failing to do this produces ~0% match rate silently.

- [LEARN:data] **CORRECTION (2026-03-15 audit):** The task score file (`isco08_3d-task3.csv`) has column `task`, NOT `rtask` or `nrtask`. Every reference to `rtask`/`nrtask` in CLAUDE.md, HANDOVER.md, theory_data_bridge.md, and domain-profile.md is wrong. Use `task` when merging.

- [LEARN:data] **CORRECTION (2026-03-15 audit):** ESS Gugushvili waves 1–5 use ISCO-88 (`iscoco`), NOT `isco08`. The two-step merge path for RTI is: `iscoco` → `data/raw/kurer_2020_declining_middle/correspondence.dta` (ISCO-88 → ISCO-08 crosswalk, 446 rows) → truncate 4→3 digit → `task` score. `correspondence.dta` is many-to-many — deduplicate before merging to avoid row inflation (~190% inflation observed in audit).

- [LEARN:data] `ess_populist_crosswalk.csv` in `data/raw/langenkamp_2022/` is semicolon-delimited. Always load with `pd.read_csv(..., sep=';')`. Standard `read_csv` will silently return a single-column dataframe.

- [LEARN:data] The two Euroscepticism files are the same study in different formats: `Euroscepticism as a syndrome of stagnation.csv` (135MB) and `...-Data for replication-1.dta` (90MB). Always use the `.dta` for analysis.

- [LEARN:data] Baccini raw vs. analysis-ready: `Raw Data/` contains components; `Data/individualdata.dta` and `Data/districtdata.dta` are the merged, analysis-ready files. Always use the latter. In Research_Master these are at `data/raw/baccini_2024/Data/`.

- [LEARN:data] **CORRECTION (2026-03-15 audit):** `posit_income_change` is NOT in `essprt-all.dta` and is NOT in this repository. Cicollini constructs it from EU-SILC microdata in a separate Stata do file. `essprt-all.dta` is a party crosswalk (5,402 rows × 13 cols: cntry, essround, prtvt variable codes → partyfacts IDs). Using `essprt-all.dta` for status analysis will silently return no usable data. Module 08 (Status/Recognition) REQUIRES NEW DATA for the positional income pathway.

- [LEARN:data] `world-c.dta` and `world-d.dta` in Cicollini are geographic map files, not analysis datasets. Do not load them expecting survey data.

- [LEARN:data] ESS is NOT panel data — it is repeated cross-sections. Exception: some waves have a rotating panel component, but this is rarely used in the replication files here.

---

## Code

- [LEARN:code] Always use `pyreadstat` (not `pandas.read_stata`) for `.dta` files — pyreadstat preserves value labels and variable labels that are critical for ISSP files.

- [LEARN:code] For ESS CSV files, multi-encoding fallback is required: try `utf-8` → `latin-1` → `cp1252`. The Im ESS CSV requires `latin-1`.

- [LEARN:code] Sequential inline Python is the house style for analysis scripts: no function definitions, section headers (`# --- Config ---`, `# --- Load ---`, `# --- Transform ---`, `# --- Validate ---`, `# --- Save ---`), inline `assert` for validation.

---

## Theory

- [LEARN:theory] The "dual pathway" in Module 13 is NOT just material + cultural. It is: material hardship pathway (Module 01-04) AND status/recognition pathway (Modules 08-10), mediated by cognitive frames (Module 15) and conditioned by institutional context (Modules 05-07, 11). The trilemma (efficiency / equity / fiscal) is a key constraint.

- [LEARN:theory] "Welfare chauvinism" (Module 12) is a supply-side response to demand-side status anxiety — distinguish carefully between voters' preferences for exclusionary welfare and parties' strategic framing of those preferences.

---

## Citation

- [LEARN:citation] The routine task intensity (RTI) measure used in this repo follows Goos, Manning & Salomons (2014), implemented via the `isco08_3d-task3.csv` file. Cite the original Autor, Levy & Murnane (2003) framework plus the European adaptation.

- [LEARN:citation] For populism measurement using the Global Party Survey, cite Norris (2020) — not Norris & Inglehart (2019), which is the cultural backlash book.

---

## Method

- [LEARN:method] When using country × wave FE in ESS regressions, you cannot also include country-level time-invariant variables (e.g., welfare regime type) directly — they are absorbed. Use interactions (welfare_regime × treatment) or cross-country variance in robustness checks.

---

- [LEARN:data] `atchctr` and `atcherp` (national/European attachment, Module 09) are absent from Gugushvili ESS waves 1–5. They are present in Baccini ESSdata (waves 6+). Ontological security analysis using these variables is limited to more recent waves.

- [LEARN:data] `hinctnta` (household income decile) is absent from ESS waves 1–3. Present in waves 4–5 (Gugushvili) and Baccini (waves 6+). For multi-wave income controls, use `hinctnt` (waves 1–3) and document the variable switch.

---

*Add new discoveries below with [LEARN:category] prefix. Date optional but helpful.*
