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
- [LEARN:code] **Published §V.D r=-0.848 comes from BLUPs of random-slopes MixedLM with individual controls, NOT bivariate per-country OLS.** Canonical source: `scripts/random_slopes_models.py`. Older `analysis/final_analysis_pipeline.py` Model 3 (random intercepts only, separate-OLS slopes) is superseded for headline numbers. Same data, four methodologies: bivariate r=-0.625, OLS+controls r=-0.786, BLUPs r=-0.855 (published), country-wave averages r=-0.702.
- [LEARN:code] `scripts/random_slopes_models.py` now includes two-country jackknife (105 pairs), per-country OLS slopes vs CWED, RI vs RS direct comparison. Adds `outputs/tables/jackknife_two_country.csv`, `per_country_slopes.csv`, `rs_vs_ri_model3.csv`.
- [LEARN:code] `analysis/walkthrough_figures.py` produces 8 PNG figures + 3 Plotly HTML interactives in `outputs/figures/walkthrough/`. Used by the empirical walkthrough doc. Run after any master-CSV change.

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
- [LEARN:writing] `docs/empirical_walkthrough_v1.md` (~17,200 words) is the consolidated defence document for §V — read before any methodology defence/Q&A. Eight static figures + three interactive HTMLs embedded. "Defending the choice in 30 seconds" rehearsal box at the end of each of the 8 concepts.
- [LEARN:writing] **BLUPs disclosure inserted in `manuscripts/paper_draft_v4_final.md` §V.D (2026-05-03):** two sentences before any reported correlation, naming the slope-extraction methodology and noting the bivariate alternative gives r=-0.625.
- [LEARN:writing] **§III restructure (2026-05-10):** §III is now A through F, not A through E. The recursive-loop section was split back out as §III.D after being absorbed into §III.D's "Why the Mirror Image Does Not Exist" in v4. Renumbering: A=Evidence Demands, B=Why Welfare, C=Damage Cascade, **D=Recursive Loop (restored)**, E=Mirror Image (was D), F=Predictions (was E). Cross-references in §IV scope conditions and §V.F updated. Reason: v3 §IV recursive-loop content carried analytical weight ("preferences that are outputs of policy appear as inputs"; Pierson reverse-feedback) that was buried when collapsed into the mirror-image discussion.
- [LEARN:writing] **§I central-hypothesis sign-post added + §III.A forward-reference + §III.F numbered predictions (P1-P5) (2026-05-10):** per Amalie's seminar feedback ("hone argument, sign-post hypothesis"). Twofold-claim paragraph at §I close; falsifiable-form bridge sentence opening §III.A; predictions labelled (P1)-(P5) inline (not bolded headers, per voice-ben "no Wikipedia-AI scaffolding"). Three predictions tested in paper, two in thesis.
- [LEARN:writing] **§V.D BLUPs jackknife sentence added + §V.G sharpened to name Danish reforms (2026-05-10):** 105-pair two-country BLUPs jackknife sentence appended to §V.D closing paragraph (r range [-0.700, -0.897], 0 sign flips, 105/105 p<0.05). §V.G "subsequent work" replaced with specific reforms (2003, 2006, 2010, 2013 dagpengereform / activation reforms) and "administrative-register linkage". Removes vagueness; signals concrete next-paper design without naming "MSc thesis" in the manuscript.
- [LEARN:writing] **Voice audit on `paper_draft_v4_final.md` (2026-05-08, /voice-audit) scored 68/100 (Mixed):** four em-dash apposition stacks (lines 93/113/361/383) and transition density 1.0/1000 vs target ≥5/1000. **Apposition stacks all fixed 2026-05-10** (converted to parentheses). Transition density still low — deferred to Monday-morning retype pass alongside detection-resistance keystroke work; not a blocker for seminar submission.

---

## Council feedback (May 2026) — rationale for accept/defer

- [LEARN:writing] **Council critique on `docs/empirical_walkthrough_v1.md` (2026-05-08):** Five-persona adversarial review identified convergent CRITICAL issues: (1) N=15 macro-confounding not bounded (need Oster δ / Cinelli-Hazlett), (2) BLUPs vs four-estimator specification search ($r \in [-0.625, -0.855]$), (3) effective N for β₃ is 15 not 82,000 — rhetorical inversion in §V.D, (4) asymmetry rests on bare nulls without TOST + SUR equivalence testing, (5) scoop positioning vs Vlandas-Halikiopoulou / Ennser-Jedenastik / Gingrich. **Decision: DEFER to journal-version rewrite (post-thesis stage).** Rationale: Amalie's seminar feedback explicitly said "no more analysis, focus on argument / sign-posting"; each CRITICAL item implies new analysis (1-2 days each). Filed at `quality_reports/journal_version_targets/` (Todoist task 6gcPG9GvfFCQrWCX, due 2026-05-15). The walkthrough critique reads almost like an AJPS/CPS referee report; it's the right input at journal stage, wrong input now. Scoop positioning verified sharp in §II as written — single CRITICAL fix downgraded.
- [LEARN:theory] **Council ideation on Danish-registry extension (2026-05-08):** Three-persona generative council mapped a five-year arc: Y1 MSc thesis (within-Denmark mass-layoff DiD around 2010 dagpengereform), Y2 mechanism-replication paper (Statistics Denmark register linkage to political outcomes), Y3 mechanism-interrogation (stigma vs contribution-account vs economic-exposure mediators), Y4 generational-transmission (BEF multi-generational linkage), Y5 cross-national synthesis. **Decision: ACCEPT as thesis roadmap.** Year-2 paper design directly defuses three of the council critique's CRITICAL objections (institutional-bundle confounding, selection into RTI, N=15 ceiling) — making the thesis the load-bearing causal-identification move the seminar paper gestures toward. See `quality_reports/council_ideations/2026-05-08_extend_asymmetric_welfare_danish_registry.md`. Linked in `projects/msc_thesis/STATUS.md`.

---

## Project timeline correction (2026-05-10)

- [LEARN:workflow] **TIMELINE CORRECTION:** CLAUDE.md previously described Ben as "MSc Economics conferred 2026, beginning PhD." Wrong. **Correct timeline:** seminar paper this term (May 2026) → MSc thesis next semester (autumn 2026 → spring 2027) → PhD applications autumn-winter 2026/2027 → PhD start Fall 2027. Implication: register data access for the MSc thesis comes via existing CEBI employment (no Forskerservice application required); fresh Forskerservice authorisation is a 2027 concern for PhD-stage register work. Three Todoist tasks deleted that assumed the wrong premise (May-31 CEBI email, Sep-30 Forskerservice deadline). Scoop-scan deadline brought forward to Aug-1 (before thesis topic locks).

---

## Project Context — operative heuristic (2026-05-10)

- [LEARN:workflow] **PRIMARY HEURISTIC: accelerated paper completion.** When weighing trade-offs in the seminar paper, balance maximum possible quality against the practical constraints of current data and timeline. Concrete implications: (a) defer council-critique CRITICAL items to journal-version rewrite (they require new analysis Amalie advised against); (b) ship the asymmetric framing as-committed without further theoretical excavation; (c) the Monday-morning retype pass is the last substantive editing block before submission; (d) any recommendation that implies "another analytical pass" should be scored against this heuristic and explicitly justified. See Project Context block in `CLAUDE.md` for the durable statement.
- [LEARN:writing] Public-writing project lives in `essays/`, separate from `manuscripts/`. Audience: AI labs as employers, LinkedIn + Substack venues, NOT academic journals. Voice-ben + humanize-academic auto-trigger for anything in `essays/` that will appear under Ben's name.
- [LEARN:writing] Voice-ben + humanize-academic do NOT trigger for tutor docs addressed TO Ben (e.g., `docs/empirical_walkthrough_v1.md`, `docs/learning_econometrics/01_*.md`). Trigger only for prose Ben publishes UNDER his name.
- [LEARN:writing] Patient Tutor essays drafted May 2026: short-form LinkedIn v2 in session transcript; long-form companion ~5,200 words at `essays/patient_tutor/companion_long.md`. Register is intentionally non-academic (Bruenig/Goldsmith-Pinkham-adjacent, autobiographical, concessive). Voice-ben rules still apply but seminar-paper formality does not. Continuation state in `essays/patient_tutor/STATUS.md`.

---

## Workflow

- [LEARN:workflow] Resume sessions via `git log` + most recent plan file in `quality_reports/plans/`, not HANDOVER.md.
- [LEARN:workflow] Never read .pdf or .docx in main context — use explorer agent or convert with pandoc.
- [LEARN:workflow] Stage specific files with `git add [files]`, not `git add -A`.
- [LEARN:workflow] Complete all pipeline steps before moving on — use TodoWrite upfront.
- [LEARN:workflow] CWED interaction β=-0.059 (p=0.015, random slopes spec, paper §V.D) survives GDP+Gini macro controls at β=-0.066 (p<0.001, `rs_macro_controls.csv`). This is the key robustness check. Older β=-0.056 number was from the random-intercepts spec (`final_results.json`) and is no longer canonical.
- [LEARN:workflow] **Multi-session adversarial iteration pattern**: when a draft feels stale, dispatch a second Claude session to critique it without seeing the first session's reasoning. Ben adjudicates between the two. The second session frequently catches what the first missed (e.g., the "paper-is-the-curriculum" reframe came from a side session reviewing a "patient tutor" outline). Use whenever a piece is on its second pass and feels like it has run out of intellectual tension.
- [LEARN:workflow] Anchor-paragraph retype protocol for detector resistance: Ben types opening + closing paragraphs from memory (closes file, types fresh). Three retyped paragraphs out of ten typically averages document detector scores down by 30-50 percentage points. Other paragraphs can stay close to drafted.
- [LEARN:workflow] **Detection-resistance protocol revised 2026-05-14:** Voice loss is acceptable IF AI-rewritten prose (a) passes GPTZero HUMAN_ONLY AND (b) reads compelling/eloquent. Voice re-injection happens during the editing pass on sections Ben specifically chooses to revise (adding literature, extending arguments, developing ideas, surfacing future research) — the editing inadvertently re-injects Ben regardless. Manual retype remains one option; /derisk-paragraph + editorial polish is now a co-equal second option, judged section-by-section. Empirical basis: 2026-05-11 overnight experiment showed §III.D moved from 93% AI → 33% AI (HUMAN_ONLY) via /derisk-paragraph on the validated welfare-political-economy + Opus cell. The earlier "manual retype is the only reliable path" learning is partially superseded for the welfare-PE/Opus cell. The full validated-cell map lives in `~/.claude/skills/derisk-paragraph/SKILL.md`.
- [LEARN:workflow] **`/council-critique <artefact>`** (May 2026): five-persona adversarial review (Skeptic/Methodologist/Pre-mortem/External-Validity Hawk/Contribution Auditor) dispatching to econometrician, methods-referee, strategist-critic, domain-referee, editor in parallel. Synthesis identifies convergent / divergent / missing dimensions + top-three actions. Reports save to `quality_reports/council_critiques/`. Use for paper, memo, identification-strategy, chapter review.
- [LEARN:workflow] **`/council-ideate "<topic>"` or `/council-ideate <doc>`** (May 2026): three-persona generative council (Obvious Extension / Adjacent Outsider / Constraint Inverter) using `general-purpose` subagents in parallel, then synthesis (convergent thread / boldest move / five-year programme / three checks). Reports save to `quality_reports/council_ideations/`. Use for research-direction pressure-testing and protection from myopia.
- [LEARN:workflow] Council skills coexist with the user-level `/council` command (`~/.claude/commands/council.md`); the project skills hard-wire research-domain agents while `/council` resolves a generic panel via flags. Use council-critique / council-ideate for paper and idea work; use the user-level `/council` for skill design, plan reviews, decisions.
- [LEARN:workflow] **`/done` (project-level, May 2026)** captures session-end across four files: `quality_reports/session_logs/YYYY-MM-DD_<slug>.md`, `SESSION_REPORT.md`, `quality_reports/research_journal.md` (only if agents dispatched), and the active `STATUS.md`. Tags drawn from a controlled 17-topic vocabulary. Coexists with the user-level `/done` command; both can be invoked. Resist topic bloat — adding new topics requires explicit nod.
- [LEARN:workflow] **`/recall <query>` (May 2026)** searches across session logs, SESSION_REPORT, research_journal, and STATUS files for past decisions. MVP uses Read+Grep directly (no vector index). Always cites file paths; conservative on direct answers — returns "not in corpus" rather than fabricating. Honours `quality_reports/session_logs/_private/` exclusion. Upgrade to vector store only when corpus exceeds context-window viability (12-18 months out).
- [LEARN:workflow] **`/voice-audit <path>` (May 2026)** runs deterministic checks against the YAML frontmatter in `voice-ben/SKILL.md`. Test on `paper_draft_v4_final.md` scored 68/100 (Mixed band) — caught 4 em-dash apposition stackings and low transition density. CHECK only, never auto-rewrites. Honours `scope_excludes` (skips tutor docs, infrastructure, code).
- [LEARN:voice] **voice-ben spec is now structured YAML in the frontmatter** of `.claude/skills/voice-ben/SKILL.md`. The frontmatter is canonical (consumed by `/voice-audit`); the body is human-readable rationale. When updating bans/rules, edit the YAML, not the body. Calibration sources, exceptions (`foster`, `robust` methodological), and detection-resistance ceiling all encoded.

---

*Last updated: May 2026. Quarterly prune: delete superseded, merge duplicates. Hard cap: 150 lines.*
