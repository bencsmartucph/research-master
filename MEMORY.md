# MEMORY.md — Persistent Research Discoveries

> **5 categories only:** `data`, `code`, `theory`, `writing`, `workflow`.
> **How to use:** Read at session start. Add corrections with `[LEARN:category]` prefix.
> **Hard cap:** 150 lines. Quarterly prune — delete superseded, merge duplicates.

---

## Data

- [LEARN:data] ESS vote variables are country-specific: `prtvtXXX` where XXX = 2-letter ISO code. Harmonised via `data/raw/langenkamp_2022/ess_populist_crosswalk.csv`.
- [LEARN:data] ISSP ZA-files use numeric codes — always load `meta.variable_value_labels` via pyreadstat before recoding.
- [LEARN:data] ESS ISCO-08 codes are 4-digit. Task score file uses 3-digit. Truncate: `df['isco08'] // 10`.
- [LEARN:data] **CORRECTION:** Task score column is `task`, NOT `rtask`/`nrtask`. Every prior reference was wrong.
- [LEARN:data] ESS waves 1–5 use ISCO-88 (`iscoco`), not `isco08`. Need crosswalk via `kurer_2020_declining_middle/correspondence.dta` (many-to-many — deduplicate first).
- [LEARN:data] `ess_populist_crosswalk.csv` is semicolon-delimited. Use `sep=';'`.
- [LEARN:data] Euroscepticism `.dta` and `.csv` are the same data — use the `.dta`.
- [LEARN:data] Baccini: always use `Data/individualdata.dta` and `Data/districtdata.dta`.
- [LEARN:data] `posit_income_change` is NOT in this repo. `essprt-all.dta` is a party crosswalk only.
- [LEARN:data] ESS is repeated cross-sections, NOT panel data.
- [LEARN:data] `atchctr`/`atcherp` absent from ESS waves 1–5; present in waves 6+.
- [LEARN:data] `hinctnta` absent from ESS waves 1–3. 21-30% missing in Liberal/Southern regimes.
- [LEARN:data] CWED: 15 Western European countries only. N drops to ~81,885 for Model 3. Mean 2005-2011, time-invariant.
- [LEARN:data] Verify file paths before analysis: `Path(f).exists()`.
- [LEARN:data] Always use explicit encoding: `encoding='utf-8'` or `'utf-8-sig'`.
- [LEARN:data] Print dtypes on load — check merge key types before joining.
- [LEARN:data] Test merges on small samples first (100 rows, check NaN rates).

---

## Code

- [LEARN:code] Always use `pyreadstat` (not `pandas.read_stata`) for `.dta` files.
- [LEARN:code] ESS CSV multi-encoding fallback: try `utf-8` → `latin-1` → `cp1252`.
- [LEARN:code] House style: sequential inline Python, no function defs, section headers (`# --- Config ---`, etc.), inline `assert`.
- [LEARN:code] Final pipeline: `analysis/final_analysis_pipeline.py`. Master dataset: `analysis/sorting_mechanism_master_v2.csv` (188,764 × 48).
- [LEARN:code] R final spec: `lme4::lmer` with `anti_immig_index ~ task_z * welfare_regime + controls + (1 + task_z | cntry_wave)`.
- [LEARN:code] Random slopes REQUIRED. LR test p<10⁻²⁰. SE doubles but survives at p=0.002. Python statsmodels = diagnostic only.

---

## Theory

- [LEARN:theory] "Dual pathway" = material hardship (01-04) AND status/recognition (08-10), mediated by cognitive frames (15), conditioned by institutions (05-07, 11).
- [LEARN:theory] Welfare chauvinism (12) = supply-side response to demand-side status anxiety.
- [LEARN:theory] Core claim: decommodification, not spending, is operative. ALMP/CWED contrast is the paper's central empirical argument.
- [LEARN:theory] ALMP puzzle: spending aggregates enabling + punitive programmes. CWED captures whether workers can sustain themselves without employment — the theoretically correct dimension.
- [LEARN:theory] **Asymmetric mechanism (committed April 2026):** welfare design's political effects are asymmetric — damage is detectable, equivalent protection is not. Three asymmetries: loss aversion (Kahneman-Tversky), positional status (Gidron-Hall 2017), irreversibility of defensive othering (Pierson 1994 photographic-negative reading). "Dignity is a baseline good. Its absence damages; its presence clears the ground for solidarity without producing it."
- [LEARN:theory] Solidarity construction is *not* purely a function of welfare design — requires political work (coalitional framing, electoral institutions, narrative entrepreneurs) that welfare design alone cannot supply. Welfare's role is permissive not productive on the solidarity side.

---

## Writing

- [LEARN:writing] RTI measure: cite Goos, Manning & Salomons (2014) via `isco08_3d-task3.csv`, plus Autor, Levy & Murnane (2003).
- [LEARN:writing] Populism measurement: cite Norris (2020), not Norris & Inglehart (2019).
- [LEARN:writing] Working papers to verify: Wagner (2022/2023), Stutzmann (2025), Pelc (2025) — check for published versions.
- [LEARN:writing] Model ordering: lead with Model 3 (CWED continuous), then Model 2 (regime categorical).
- [LEARN:writing] Education moderation: report descriptively, note non-significant 3-way (p=0.179).
- [LEARN:writing] Redistribution (H2): RTI × Liberal = 0.011, p=0.285. Accept as genuine asymmetry — and (April 2026) foreground it as the paper's central theoretical claim, not a concession.
- [LEARN:writing] RR vote (Model 6): RTI × Liberal = -0.123, p=0.032 (negative). Supply-side explanation. Frame as confirmation of attitudes-vs-votes distinction, not as puzzle.
- [LEARN:writing] Title (April 2026): "Dignity Is a Baseline: Welfare Institutions and the Asymmetric Politics of Economic Disruption." Locked.
- [LEARN:writing] Tier 1 added citations: Kurer & Palier 2019 (dignity appeal), Burgoon & Schakel 2022 (engagement, not contradiction — platform vs voter level), Van Hootegem 2025 (two faces of activation), Häusermann-Kurer-Zollinger 2023 (universalism-particularism), Im 2023 (status decline panel), Kurer & van Staalduinen 2022 (status discordance asymmetry), Kahneman & Tversky 1979 (loss aversion), Goos-Manning-Salomons 2014 (RTI), Iversen & Soskice 2001 (asset theory), Bornschier-Haffert-Häusermann 2024 (cleavage), Halikiopoulou & Vlandas 2016 (predecessor of V&H 2022), Ennser-Jedenastik 2019 (cushion or catalyst), Jeffrey 2020 (rhetoric), Kuziemko 2023 (predistribution preference).
- [LEARN:writing] Country × wave FE absorbs time-invariant country vars. Use interactions or cross-country variance checks.
- [LEARN:writing] CWED sample (N=81,885) differs from Model 2 sample (N=125,169). Always report Ns separately.
- [LEARN:writing] Ben's pre-AI voice (Global Media essay 2017): heavy semicolons, near-zero em-dashes. Transition vocabulary "Indeed/Ultimately/Through this perspective/Consequently/Thus/Similarly/yet". Match this register when ghostwriting; em-dashes are the #1 AI-detection tell — purge to <30 per 7000 words.
- [LEARN:writing] Will Francis humanizing rules are a starting heuristic. Where WF banned words conflict with Ben's voice (e.g., "foster" appears in Global Media essay), voice wins.
- [LEARN:code] `scripts/build_submission_docx.py` now inserts figures via `FIGURE_MAP` dict. Currently maps Figure 2/3/6; add new entries when paper references additional figures. Falls back to grey placeholder if image not found.

---

## Workflow

- [LEARN:workflow] Resume sessions via `git log` + most recent plan file in `quality_reports/plans/`, not HANDOVER.md.
- [LEARN:workflow] Never read .pdf or .docx in main context — use explorer agent or convert with pandoc.
- [LEARN:workflow] Stage specific files with `git add [files]`, not `git add -A`.
- [LEARN:workflow] Complete all pipeline steps before moving on — use TodoWrite upfront.
- [LEARN:workflow] CWED interaction β=-0.056 survives GDP, Gini, immigrant stock controls. This is the key robustness check.

---

*Last updated: April 2026. Quarterly prune: delete superseded, merge duplicates. Hard cap: 150 lines.*
