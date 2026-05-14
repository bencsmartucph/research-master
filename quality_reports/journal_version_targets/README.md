# Journal-Version Targets

> Filing folder for council-critique and methodology-referee findings that are valid but **deferred** past the seminar-paper stage. Per `CLAUDE.md` Project Context: the seminar paper ships under the accelerated-completion heuristic; rigorous-but-time-expensive items live here until the journal-version rewrite.

When you return to this paper for journal submission (anticipated post-MSc-thesis, ~late 2027), open this folder first.

## Filed items

### `2026-05-08_empirical_walkthrough.md` (pending file; pointer in `quality_reports/council_critiques/2026-05-08_empirical_walkthrough_v1.md`)

**Convergent CRITICAL items from five-persona council critique:**

1. **N=15 macro-confounding bounded** — Oster (2019) δ or Cinelli-Hazlett (2020) robustness value at country level. Estimated effort: 1 day.
2. **BLUPs specification curve** — multiverse plot reporting r range $[-0.625, -0.855]$ across the four defensible estimators × controls × aggregation choices; demote single-point r=−0.848 from headline. Estimated effort: 1 day.
3. **Effective-N reframing** — rewrite the §V.D "Model 3 is more powerful than the country scatter" line; β₃ is identified by 15 country-CWED pairs, not 82,000 individuals. Estimated effort: 1 hour (writing) + 0 analysis.
4. **TOST + SUR for the asymmetry** — formal equivalence test on the solidarity moderation with declared bound (|β| < 0.05), plus joint cross-equation Wald test of $H_0: \beta_{3,\text{excl}} = \beta_{3,\text{sol}}$. Promotes asymmetry from rhetorical to empirical contribution. Estimated effort: 1 day.
5. **Wild cluster bootstrap at G=15** — Cameron-Gelbach-Miller / Roodman `boottest` for the cross-level interaction. Estimated effort: 0.5 day.
6. **Scope condition prose** — Eastern Europe absent by data construction, refugee crisis 2015-16 unmodelled, CWED 2005-11 mean applied to 2012-18 outcomes. Estimated effort: 1 day prose work.
7. **Within-ISCO-3d between-country contrast** — addresses occupational-sorting confound (the textbook RTI-paper critique). Estimated effort: 2-3 days.

**Total estimated effort: ~8-10 days analytical + writing. Sequence as a single sprint when journal-version is the active project.**

### Reference: full critique with persona breakdowns

See `quality_reports/council_critiques/2026-05-08_empirical_walkthrough_v1.md` for the raw five-persona reports and synthesis.

### Reference: thesis-level extensions that defuse items 1-3

See `quality_reports/council_ideations/2026-05-08_extend_asymmetric_welfare_danish_registry.md`. The Y2 within-individual register design directly addresses institutional-bundle confounding, selection into RTI, and the N=15 ceiling — making the thesis the load-bearing causal-identification move.

---

*Created 2026-05-10 in support of the high-fidelity sync. Folder previously did not exist; Todoist task `6gcPG9GvfFCQrWCX` (due Friday May 15) is the filing reminder.*
