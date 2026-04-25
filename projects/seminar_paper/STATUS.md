# Seminar Paper — STATUS

> **NEXT:** Editorial pass on big-bet draft. Title locked, asymmetric framing committed. Six-week sprint per `docs/strategic_memo_2026-04-25.md` Path A.

## Paper

**Title:** "Dignity Is a Baseline: Welfare Institutions and the Asymmetric Politics of Economic Disruption"

**Stage:** Big-bet asymmetric reframe committed and implemented (v4 final). Medium-bet fallback preserved as `medium bet_paper_draft_v4_final.md`. Standalone big-bet theory draft retained as `paper_draft_v5_big_bet_theory.md` for reference.

**Working draft:** `manuscripts/paper_draft_v4_final.md` — body ~6,800 words, six sections (I Intro, II Limits of Buffering, III Asymmetric Mechanism A–E, IV Scope Conditions, V Empirical Analysis A–G, VI Discussion). Build script reads this file unchanged.

**Key change from medium bet:**
- Asymmetric mechanism is now the central theoretical claim, not a concession in §VI.F
- §III restructured into A (What Evidence Demands) / B (Why Welfare) / C (Damage Cascade) / D (Why Mirror Image Doesn't Exist) / E (Predictions)
- Old §IV (Recursive Loop) absorbed into §III.D
- Old §V (Counterfactual) reframed as §IV (Scope Conditions and Limits)
- §VI.F promoted: Appendix C ISSP null promoted into body as confirmation
- Title changed; abstract rewritten; §I introduction rewritten

**Key files:**
- Draft: `manuscripts/paper_draft_v3_final.md`
- Pipeline: `analysis/final_analysis_pipeline.py`
- Dataset: `analysis/sorting_mechanism_master_v2.csv` (188,764 × 48)
- Results: `analysis/final_results.json`
- ISSP solidarity script: `scripts/issp_solidarity_leg.py`
- Review diagnostics: `analysis/review_diagnostics/part2_findings.json`

---

## Empirical Narrative (present in this order)

1. RTI predicts anti-immigration everywhere (Model 1, β=0.182, N=125,169)
2. Stronger in Liberal regimes (Model 2, RTI × Liberal β=0.117, p<0.001 with random slopes)
3. NOT about spending — ALMP shows near-zero on matched 15-country sample (r=+0.011, p=0.97, N=15)
4. IS about decommodification — CWED r=−0.848 across 15 countries (Model 3, β=−0.056, p<0.001)
5. Concentrated among non-college workers (54% slope reduction, but p=0.179 — suggestive only)
6. Attitude→vote conversion constrained by supply side (Model 6: Liberal β=−0.123 — FPTP + UKIP channel explains)
7. Robust: jackknife range [0.073, 0.161], never crosses zero; stable across UK/NO/DK exclusions

**Figure 6** (CWED vs. country slopes) is the single most important figure.

---

## Decisions Made This Session (April 2026)

| Issue | Resolution |
|-------|-----------|
| ALMP sample mismatch | Fixed: matched-sample r=+0.011 (N=15) — strengthens, not weakens, the argument |
| Causal overclaiming §VII, abstract, §I | Cleaned throughout — "associated with", "consistent with", "co-varies with" |
| Outlier sensitivity on N=15 | Added battery: DK, UK, NO, DK+NO exclusions all give r < −0.717, p < 0.007 |
| Model 6 factual error | Fixed: UKIP vote share acknowledged (15–27%); FPTP seat suppression + Brexit channel |
| §VI.I confounding paragraph | Expanded: names social trust, unions, PR systems, ethnic homogeneity as confounders |
| ISSP solidarity leg | RAN: β=+0.010, p=0.55 — NULL. Treat as second null with temporal caveat |

---

## ISSP Solidarity Result

**Dataset:** ISSP 2006 Role of Government IV (ZA4700), N=10,216, 12/15 WE countries (AT, BE, IT absent)
**Model:** `solidarity ~ task_z * cwed_z + controls + (1 + task_z | country)`
**RTI × CWED interaction:** β=+0.010, SE=0.016, **p=0.55 — NULL**
**OLS cross-check:** β=−0.012, p=0.77 (opposite sign)
**Main RTI effect:** β=−0.109 (routine workers wanted *less* spending in 2006 — pre-automation salience)

**Interpretation:** 2006 predates the automation discourse (Frey & Osborne 2013); "sorting into solidarity" may require that automation risk be cognitively salient as a class threat. Not a refutation of the theoretical mechanism — but cannot be claimed as confirmation either.

**Decision:** Acknowledge in §VI.I as second null alongside Model 5 (gincdif). Do NOT add as main result.

**Sentence to add to §VI.I:**
> "A supplementary test using ISSP 2006 Role of Government data similarly finds no interaction between automation exposure and welfare generosity on redistribution support (β=+0.010, SE=0.016, p=0.55, N=10,216), consistent with the Model 5 null and consistent with automation risk not yet registering as a salient class threat in the pre-Frey-and-Osborne period."

---

## Outstanding Tasks (big-bet path)

### Editorial pass on big-bet draft (priority)
1. ⬜ **Voice consistency pass** — new §III.D, §IV, §V.F, §VI sections need a unified voice review against `manuscripts/Writing Samples/Voice and Writing Style.txt`
2. ⬜ **Forward/backward cross-references** — verify all section refs (§II, §III.B, §V.D, §V.F, §VI, Appendix C) point correctly after renumbering
3. ⬜ **Trim pass** — body is ~6,800 words; target 5,000–6,000 if possible. §III is the major addition; §V/§VI may have residual medium-bet phrasing
4. ⬜ **Full reference audit** — verify the new Tier 1 citations (Kurer & Palier 2019, Burgoon & Schakel 2022, Van Hootegem 2025, Bornschier-Haffert-Häusermann 2024, Im 2023, Halikiopoulou & Vlandas 2016, Ennser-Jedenastik 2019, Iversen & Soskice 2001, Kurer & van Staalduinen 2022, Kuziemko 2023, Goos-Manning-Salomons 2014, Jeffrey 2020, Kahneman & Tversky 1979) — confirm working paper status, year, page numbers
5. ⬜ **Grep forbidden verbs**: `shape|produce|determine|cause|convert|activate|mediate|trigger|channel` — each hit needs checking against the new asymmetric framing
6. ⬜ **Check Figure 6 JSON freshness** — `create_figures_final.py` reads from `final_results.json`; confirm matched ALMP entry renders correctly
7. ⬜ **Update Figure 6 caption** for asymmetric framing language

### Empirical extensions (per strategic memo)
1. ⬜ **CWED sub-components** (unemployment / sickness / pensions separately) — central under big bet, not nice-to-have. Theoretical prediction: unemployment-CWED carries the bulk of the cross-national signal because unemployment is where vulnerable workers actually encounter conditional welfare. ~1 hr.
2. ⬜ **`gvctax` two-item composite** as supplementary solidarity outcome — second nullifies measurement-artefact reading of the asymmetry. ~20 min.
3. ⬜ **Within-country FE on AT/DE/NL/GB CWED time-variation** — bridges to thesis design; draft as Appendix D.

### Nice-to-have (do if time, skip if tight)
- ⬜ CWED sub-components (unemployment/sickness/pensions separately) — 1 hr
- ⬜ `gvctax` two-item composite as supplementary solidarity outcome — 20 min

### Skip entirely
- ~~R lme4 replication~~ — Python MixedLM workaround is verified correct; R replication is robustness only, not a blocker
- ~~Wave stability robustness~~ — ESS rounds 6–9 span too short; country-wave FE absorbs most variation
- ~~Gender interaction~~ — orthogonal to core argument

---

## PhD / Thesis Forward Plan

The paper documents cross-sectional associations. The causal claim requires **within-country variation in welfare generosity over time** — CWED changes following benefit reforms as the shock.

**Key design gap to fill in thesis:**
- Instrument: benefit reform timing (CWED change years) as exogenous shock to decommodification
- Outcome: RTI–attitude slope should shift following generosity changes
- Data: CWED waves 1971–2011 show meaningful within-country variation for AT, DE, NL, GB
- This is mentioned in the updated §VII conclusion as the required next step

**For a new Opus session on thesis design:**
- Start with: "I have a paper showing welfare decommodification (CWED) cross-sectionally moderates RTI→anti-immigration. I want to design a causally identified test. What are my options given data constraints?"
- Relevant files to read in that session: this STATUS.md, `analysis/final_results.json`, `docs/theory/README.md`
- Key datasets already on disk: CWED (`data/raw/CWED/cwed-subset.csv`), ESS waves 1–9, CPDS

---

*Updated April 2026 — end of pre-submission polish session.*
