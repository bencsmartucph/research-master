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

- [LEARN:data] The two Euroscepticism files are the same study in different formats: `Euroscepticism as a syndrome of stagnation.csv` (135MB) and `...-Data for replication-1.dta` (90MB). Always use the `.dta` for analysis.

- [LEARN:data] Baccini raw vs. analysis-ready: `Raw Data/` contains components; `Data/individualdata.dta` and `Data/districtdata.dta` are the merged, analysis-ready files. Always use the latter. In Research_Master these are at `data/raw/baccini_2024/Data/`.

- [LEARN:data] `posit_income_change` in Cicollini's `essprt-all.dta` is pre-constructed. Do NOT reconstruct it from ESS income variables — the construction methodology is in the paper and replicating it is error-prone.

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

*Add new discoveries below with [LEARN:category] prefix. Date optional but helpful.*
