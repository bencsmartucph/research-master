# 03 — Feasibility Verdicts
> Phase 3: Data Audit | Date: 2026-03-15
> Direct verdicts on whether each theory module can be tested with existing data.
> These verdicts are intended to inform Phase 4 (paper design). Do not commit to a
> research design that requires a NO PATH variable without a data acquisition plan.

---

## Verdict Key

| Symbol | Meaning |
|--------|---------|
| **FEASIBLE** | Variables present, merges work, adequate sample. Ready to use. |
| **FEASIBLE WITH CAVEATS** | Core analysis feasible, but specific limitations apply. Document and proceed. |
| **REQUIRES NEW DATA** | Key variable missing; cannot proceed without data acquisition. |
| **UNCLEAR** | Cannot fully assess from samples alone; Ben's input needed. |

---

## Module-by-Module Verdicts

---

### Module 01: Embedded Liberalism & Economic Vulnerability

**Verdict: FEASIBLE WITH CAVEATS**

**What works:**
- Milner analysis-ready merged file (`milner_merged_regional_strat200.csv`) contains all key trade exposure variables: `shock_china_imports`, `shock_lowwage_imports`, `shock_wlrd_ind`, `robots_shock_nmwi`.
- Right-wing populist vote outcome at NUTS2 level: `nuts2_right_pop_vs` and `nuts2_right_pop_vs_diff`.
- Regional GDP: `regional_gdp`, `reg_gva_total`.
- CPDS: 1722 country-years, 36 countries, 1960–2018. `almp_pmp` and `social1`–`social8` confirmed present.

**Caveats:**
1. CPDS `social1`–`social8` column labels are not self-documenting — CPDS codebook needed to identify which subcategory measures "welfare compensation to trade losers" vs. total social expenditure. Do not assume label meaning from position.
2. The Milner regional file unit is NUTS2-year. Individual-level welfare compensation (did affected workers actually receive benefits?) is NOT available in this infrastructure — only aggregate national spending.
3. CPDS covers only to 2018. Post-2018 austerity and welfare trends are not captured.

---

### Module 02: Automation & Technological Change

**Verdict: FEASIBLE WITH CAVEATS**

**What works:**
- `isco08_3d-task3.csv` confirmed present at `data/raw/shared_isco_task_scores/` and `data/raw/aspiration_apprehension/`. Single composite `task` score (1–3 scale) for 125 3-digit ISCO-08 codes.
- `correspondence.dta` (Kurer 2020) confirmed: 446 rows, maps `isco88` → `isco08`. Two-step RTI merge from Gugushvili ESS waves tested: ~190% step-1 match (correspondence is many-to-many — some ISCO-88 codes map to multiple ISCO-08 codes; this inflates rows), ~187% end-to-end. Row inflation must be resolved (e.g., take first match or use mode) before using this merge in analysis.
- Baccini `individualdata.dta` has pre-computed `rti` — this is the cleanest route for automation analysis and avoids the ISCO-88/08 conversion entirely.
- Im ESS CSV has `isco08` directly (4-digit) — covers more waves.
- ELFS `RTIshare` gives regional-level automation exposure by NUTS2 (238 regions).

**Caveats:**
1. **DOCUMENTATION ERROR IN CLAUDE.md AND theory_data_bridge.md**: The task score variable is named `task`, NOT `rtask`/`nrtask`. All existing code references using `rtask` or `nrtask` will silently fail. Update documentation and code.
2. **ISCO mismatch in Gugushvili ESS waves 1–5**: These files use `iscoco` (ISCO-88 4-digit), not `isco08`. The direct merge path documented in CLAUDE.md (`df['isco08'] // 10`) does NOT apply. The correct path requires the `correspondence.dta` crosswalk first, but the many-to-many mapping creates row inflation. Baccini `rti` or Im ESS `isco08` avoid this complication.
3. The `task` score is a composite (1=non-routine manual, 2=routine, 3=non-routine cognitive — infer from range; codebook not in repository). The monotonic directionality should be confirmed before use.
4. The anticipation/apprehension pathway (Module 04 overlap) is measured differently from the objective RTI pathway. Do not conflate.

---

### Module 03: Globalisation, Trade & Spatial Dimensions

**Verdict: FEASIBLE**

**What works:**
- Milner `imputed_econdata_voteshare_merged.dta` (analysis-ready, 285 columns) is the primary dataset. Contains Chinese import shock (`shock_china_imports`, `shock_china_ind`), low-wage import shock, world trade shock, manufacturing employment share, regional GDP, NUTS2 identifiers, and populist vote outcomes (`nuts2_right_pop_vs`, `nuts2_left_pop_vs`).
- Robot adoption shock (`robots_shock_nmwi`) also present.
- BFW IO data (`BFW_IO.dta`, `BFW_manufacturing_shares.dta`) available in broz_2019 as alternative Chinese import exposure source.
- CLEA electoral archive (party-level vote shares) + party classifications both present.

**No blocking gaps identified.** This is the best-supported module in the infrastructure.

---

### Module 04: Precarity, Skill Specificity & Occupational Risk

**Verdict: FEASIBLE WITH CAVEATS**

**What works:**
- `aspiration_apprehension_data.csv` (31 columns) has `short_isco3d` (3-digit occupation), `class5/class8` (class categories), `rr` (radical right vote flag). This is the primary test of anticipated vs. experienced hardship.
- ESS waves 4–5 have `hinctnta` (household income decile) for material precarity.
- `correspondence.dta` enables EGP/Oesch class scheme construction from ISCO codes.

**Caveats:**
1. `aspiration_apprehension_data.csv` has 31 variables with non-standard names (X5_3, X8_8_7 etc.) suggesting a custom survey design, not ESS. Country coverage and sample size unknown — need to load full file and inspect metadata. If coverage is limited to a few countries, cross-national analysis is not feasible.
2. `hinctnta` absent from ESS waves 1–3, present in waves 4–5 only (30% missing in wave 5). Income effects analysis is limited to later waves.
3. `dfincac` (subjective financial difficulty) is NOT present in the Gugushvili waves. It exists in the Baccini ESSdata (large file). Subjective precarity measurement requires the 598MB Baccini ESS file.
4. SIWE (Sweden only) provides detailed job security measures but cannot support cross-national analysis.

---

### Module 05: Policy Feedback & Welfare Institutions

**Verdict: FEASIBLE**

**What works:**
- Baccini `individualdata.dta` is analysis-ready: `cntry`, `essround`, `idno`, `rti`, `populism_score`, `share_populist_parties_gps`, `austerity_dummy`, `austerity_lag`, `austerity_lead`, `post2010`, demographics.
- Baccini `districtdata.dta` has `radical_right`, `nuts2`, trade shock variables, district-year structure.
- Alesinadata: 629 country-years of fiscal consolidation episodes (`total_impact_t`, `spend_impact_t`, `tax_impact_t`).
- CPDS: generosity, social spending, ALMP.

**Note:** Baccini analysis-ready files are the strongest test of the policy feedback pathway. The replication design is confirmed feasible — the main paper's identification strategy (DiD, austerity × ESS individual outcomes) can be re-run with existing files.

---

### Module 06: Active Labour Market Policies (ALMPs)

**Verdict: FEASIBLE WITH CAVEATS**

**What works:**
- CPDS has `almp_pmp` (ALMP % GDP), `unemp_pmp` (passive spending). Country-year panel, 36 countries, 1960–2018.
- ELFS has `RTIshare` and `RTIshare_1999` by NUTS2 region (238 regions). This enables Gingrich-style "ALMP response per routine worker" calculation.
- Gingrich `RP_Context_Data.dta` available for state-level automation policy context.

**Caveats:**
1. **ALMP type (enabling vs. punitive) is NOT measurable from available data.** This is the central construct of Module 06's theoretical argument. CPDS spending is undifferentiated. Measuring this would require LABREF (EU Labour Market Reform Database), MISSOC (Mutual Information System on Social Protection), or OECD Employment Outlook conditionality indicators — none in repository.
2. Country × wave FE absorbs time-invariant ALMP variation — within-country changes in ALMP spending are modest and may be insufficient for identification.

**What Module 06 can test with available data:** Whether ALMP spending level (not type) moderates the automation–populism relationship. This is a weaker test than the full theoretical argument.

---

### Module 07: Welfare Design, Trust & Legitimacy

**Verdict: FEASIBLE**

**What works:**
All key ESS trust and satisfaction variables confirmed present across waves 1–5:
- `trstprl` (parliament), `trstplt` (politicians), `trstep` (EU) — all waves
- `stfgov` (government satisfaction), `stfdem` (democracy satisfaction) — all waves
- `gincdif` (redistribution preference) — all waves

Steiner ZA7700 and ISSP ZA-files (Gingrich) provide welfare attitude batteries. Note: ISSP files use numeric codes; always load `meta.variable_value_labels` before using.

No blocking gaps.

---

### Module 08: Status, Recognition & Relative Position

**Verdict: REQUIRES NEW DATA** (for core construct) / **FEASIBLE WITH CAVEATS** (for proxies)

**The core problem:** `posit_income_change` — the central operationalisation of the status pathway — does NOT exist in this repository. `essprt-all.dta` (the file named in MEMORY.md as its source) is a party crosswalk (5,402 rows × 13 columns mapping ESS vote variable codes to partyfacts IDs). Cicollini's Stata do file constructs `posit_income_change` from EU-SILC microdata (European Union Statistics on Income and Living Conditions) which is not downloaded or stored here.

**To use `posit_income_change`:**
1. Register at Eurostat/EU-SILC data portal.
2. Download EU-SILC rotational panel data for relevant countries and years.
3. Run Cicollini's `Ciccolini_LeftBehindWhom.do` Stata script (requires Stata 18, `iscogen`, `wbopendata`, and ~15 additional packages).
4. This is a multi-week data acquisition project.

**What CAN be tested with available data (proxies only):**
- Relative income position: `hinctnta` decile (available waves 4–5; subjective position only, not trajectory).
- Class trajectory: `iscoco` (respondent) + `iscocop` (partner) as proxy for intergenerational context, via `correspondence.dta` for class scheme.
- Apprehension index: `aspiration_apprehension_data.csv` `class5/class8` — but this is a different construct (forward-looking fear, not actual rank trajectory).
- `essprt-all.dta` IS useful as a party crosswalk to assign populism scores to ESS vote responses.

**IMPORTANT UPDATE TO MEMORY.md REQUIRED:** Current entry stating `posit_income_change` is pre-constructed in `essprt-all.dta` is incorrect. The file is a party crosswalk. This must be corrected to prevent future misuse.

---

### Module 09: Ontological Security & Psychology

**Verdict: FEASIBLE WITH CAVEATS**

**What works:**
- `stflife`, `happy`, `stfgov`, `stfdem` confirmed present all waves.
- `sclact` (social activity) present all waves (proxy for social isolation).

**Caveats:**
1. `atchctr` (attachment to country) and `atcherp` (attachment to Europe) are ABSENT from Gugushvili ESS waves 1–5. These variables were not included in the Gugushvili compilation. They are available in Baccini ESSdata (waves 6+). Analysis of ontological attachment restricted to later waves unless Baccini file is used.
2. `graphsdata.dta` (Silva wellbeing) is 4.7KB — almost certainly a summary statistics file for graphs, not individual-level data. Cannot drive individual-level analysis.
3. Direct loneliness measures are absent. `sclact`/`sclmeet` are proxies only.

---

### Module 10: Moral Economy, Deservingness & Welfare Chauvinism

**Verdict: FEASIBLE**

**What works:**
- `imwbcnt` (immigration effect on economy), `imueclt` (immigration cultural enrichment), `gincdif` confirmed in all ESS waves.
- `imsmetn`, `impcntr` (immigration restriction items) present in waves.
- Steiner ZA7700: 200-row sample from 442-column ISSP social inequality module. Full file is 7.1MB (.dta). Has CARIN-adjacent welfare attitude battery.
- ISSP ZA-files (Gingrich): Multiple waves of social inequality module (ZA3090, ZA4950, ZA6770). Note ISSP numeric coding — always load meta first.

No blocking gaps for basic welfare chauvinism + immigration attitudes analysis.

---

### Module 11: Social Investment Paradigm

**Verdict: FEASIBLE WITH CAVEATS**

**What works:**
- CPDS has `educexp_gov` (public education spending) and `almp_pmp` (ALMP spending) — two key social investment components. Country-year, 1960–2018.
- ESS has `eduyrs` (years of education) and `eisced` (ISCED level) — need to confirm presence in Gugushvili waves (likely present but not confirmed in this audit's core variable list).
- Childcare spending: present within CPDS `social` subcategories but not individually labelled. CPDS codebook needed.

**Caveats:**
1. **Social investment spending is undifferentiated in CPDS.** `almp_pmp` includes passive elements. `educexp_gov` is total education spending, not earmarked for early childhood. Cross-national variation in social investment quality (not just quantity) requires additional sources (OECD Family Database, Eurostat).
2. CPDS covers to 2018. Social investment trends post-2018 are not available.
3. Module 11 is primarily a moderator/context variable — the question is whether high social investment regimes show weaker automation→populism links. This is testable with CPDS + ESS + milner if interaction terms are used.

---

### Module 12: Populism & Right-Wing Mobilization

**Verdict: FEASIBLE WITH CAVEATS**

**What works:**
- Baccini `individualdata.dta`: `populism_score` and `share_populist_parties_gps` directly available — these are pre-constructed from the Global Party Survey. Most direct route for individual-level populist vote analysis.
- Milner `imputed_econdata_voteshare_merged.dta`: `nuts2_right_pop_vs` for NUTS2-level right-wing populist vote share.
- `essprt-all.dta`: Party crosswalk (5,402 rows) mapping ESS vote variables to partyfacts IDs. ESS1 vote vars: 43/43 matched. Can link to GPS/Manifesto/CHES via partyfacts ID.
- `Global_Party_Survey_by_Party.dta` available in baccini_2024 for party-level populism scores.

**Caveats:**
1. **Langenkamp crosswalk is NOT a populism flag.** `ess_populist_crosswalk.csv` is semicolon-delimited and maps ESS vote codes to partyfacts IDs. It does NOT contain a `populism_flag` or binary RRP indicator. Creating a binary populist vote variable requires joining the crosswalk with GPS scores or CHES scores, both of which ARE in the repository.
2. The party crosswalk chain is: ESS `prtvtXX` → langenkamp `variable` column → `partyfacts_id` → GPS/Manifesto/CHES scores. This chain has been partially tested (all 43 ESS1 vote vars matched to crosswalk).
3. CLEA electoral archive (constituency/national vote shares) is available but requires party family classification for RRP identification.

---

### Module 13: Dual Pathway Synthesis & The Trilemma

**Verdict: FEASIBLE WITH CAVEATS**

**What can be tested (3-pathway version):**
1. **Material hardship pathway**: Baccini `individualdata.dta` — `austerity_dummy`, demographics, `populism_score`. FEASIBLE.
2. **Automation/RTI pathway**: Baccini `rti` (pre-computed) + `populism_score`. FEASIBLE.
3. **Institutional context (moderation)**: CPDS `almp_pmp` merged on `cntry` + `year`. FEASIBLE.

**What cannot be tested with existing data:**
4. **Status/positional decline pathway**: `posit_income_change` NOT AVAILABLE (see Module 08). BLOCKED.

**Additional caveats:**
- The 3-pathway synthesis (material + automation + institutional context) is feasible using Baccini analysis-ready files merged with CPDS. This is the most tractable starting point.
- Temporal pathway (anticipated hardship): `aspiration_apprehension_data.csv` provides a partial test if country coverage is adequate. But this cannot be merged directly with Baccini individual data without common individual-level identifiers.
- Mediation analysis (status anxiety as mediator of automation → populism) requires a mediating variable. With available data, `lrscale`, `imwbcnt`, or trust variables serve as proxies for attitudes that may mediate the pathway, but these are not validated mediator measures.
- **The full four-pathway synthesis requires EU-SILC data acquisition.** Estimated data acquisition time: 2–4 weeks.

---

### Module 14: Mechanisms Catalog

**Verdict: N/A** (cross-cutting reference module — see constituent modules above)

---

### Module 15: Cognitive Frames, Belief Systems & Political Realignment

**Verdict: FEASIBLE WITH CAVEATS**

**What works:**
- Immigration attitudes (`imueclt`, `imwbcnt`, `imsmetn`, `impcntr`) confirmed in all ESS waves.
- EU attitudes (`trstep`, `euftf`) confirmed in all waves.
- Left-right self-placement (`lrscale`) confirmed in all waves.
- `euroscepticism_stagnation.dta` has `eu_pos`, `trust_eu`, `lr`, `nuts2_region`, economic variables.
- `aspiration_apprehension_data.csv` enables misattribution test (automation risk → immigration blame).

**Caveats:**
1. `atchctr`/`atcherp` absent from Gugushvili waves 1–5 (confirmed FAIL). Available in Baccini ESSdata waves 6+.
2. **Meritocratic beliefs**: No standard cross-national scale available in the repository. Constructing a meritocracy scale from ESS items requires identifying which items tap meritocratic attribution (e.g., `wrclmch` is worry about climate change, not meritocracy — the theory_data_bridge.md note on this variable is misleading).
3. Universalism-particularism scale: Must be constructed from available ESS items. No pre-built scale.
4. Armaly data is US-only — cannot contribute to European analysis.

---

## Cross-Cutting Merge Feasibility Summary

| Merge | Keys | Status | Match rate | Notes |
|-------|------|--------|-----------|-------|
| ESS (Gugushvili) → RTI scores | `iscoco` → `correspondence.dta` → `isco08_3d` → `task` | FEASIBLE WITH CAVEATS | ~187% (row inflation due to many-to-many in correspondence) | Deduplicate before using |
| ESS (Im/Baccini) → RTI scores | `isco08` → `isco08_3d` → `task` | FEASIBLE | ~80–90% expected | Direct 1-step merge |
| ESS individual → Milner regional | `nuts2` (individual) → `nuts2` (regional) | BLOCKED for Gugushvili waves | Gugushvili ESS lacks NUTS2 | Use Baccini ESSdata instead |
| ESS individual → Cicollini status | EU-SILC individual ID | BLOCKED | 0% — data not in repo | Requires EU-SILC download |
| ESS vote var → populism score | `prtvtXX` → essprt-all → partyfacts_id → GPS | FEASIBLE | 43/43 ESS1 vote vars linked | Two-step; GPS merge not yet tested |
| Country-year → CPDS | `cntry` + `year` | FEASIBLE | ~100% (within covered years) | CPDS covers to 2018 |
| NUTS2 → ELFS routine shares | `nuts2` | FEASIBLE | 238 regions available | Single cross-section (2 time points) |
| NUTS2 → Milner regional | `nuts2` + `year` | FEASIBLE | Tested in milner merged file | Analysis-ready file already merged |
| ESS → ISSP (Gingrich ZA files) | No common individual ID | N/A | N/A | These are separate surveys, not mergeable |

---

## Priority Assessment for Phase 4 (Paper Design)

**Highest feasibility (start here):**
1. **Module 05 — Policy Feedback via Baccini**: Analysis-ready files with austerity + populism + individual controls. Cleanest identification.
2. **Module 03 — Trade/Spatial via Milner**: Regional analysis-ready file with trade shocks + electoral outcomes. NUTS2-year panel.
3. **Module 07 — Welfare Design/Trust**: ESS trust + satisfaction batteries, cross-national, all waves.
4. **Module 10 — Moral Economy**: ESS immigration attitudes + redistribution, all waves.

**Feasible but requires setup work:**
5. **Module 02 — Automation**: Baccini `rti` is the cleanest entry point (skip ISCO conversion entirely). Two-step merge from Gugushvili waves is viable but needs deduplication.
6. **Module 12 — Populism measurement**: Party crosswalk chain needs testing through to GPS scores.
7. **Module 06 — ALMPs as context**: CPDS spending available; type distinction is not.

**Blocked pending data acquisition:**
8. **Module 08 — Status/positional decline**: Requires EU-SILC microdata + Cicollini do file. Multi-week project.
9. **Module 13 (full, 4-pathway)**: Depends on Module 08 fix.

**Specific documentation errors to fix before writing analysis code:**
1. `rtask`/`nrtask` → rename to `task` everywhere in documentation and scripts.
2. MEMORY.md entry on `posit_income_change` being pre-constructed in `essprt-all.dta` is wrong — correct this entry.
3. CLAUDE.md `Key Data Relationships` example uses `isco08` on Gugushvili ESS — add note that `iscoco` (ISCO-88) is the actual column name.
4. Theory_data_bridge.md isco08_3d-task3.csv location shows `data/raw/aspiration_apprehension/` as primary — `data/raw/shared_isco_task_scores/` also confirmed present (both are valid).

---

*Generated: 2026-03-15 | Based on live inspection of 14 stratified sample files + 6 raw data files*
*For methodology: see 03_data_audit.py and 03_data_audit.md*
