# Demo Brief — Worker-Critic Loop on Synthetic Prose

**Date:** 2026-05-01
**Purpose:** First end-to-end demonstration of the writer + writer-critic pattern on the
`claude/ai-trends-analysis-xzncF` branch. Throwaway content; pattern is the point.

---

## Hypothetical Paper

**Title:** "Automation Anxiety and Trade Union Membership in Western Europe"

**Research question:** Does perceived automation risk increase or decrease union
membership among routine-task-intensive workers?

**Theoretical tension:**
- Insider-outsider theory (Rueda 2005) predicts decrease — automation-exposed workers
  are labour-market outsiders, and outsiders are systematically under-represented in
  unions designed for stable insiders.
- Threat-response theory (Olson 1965, applied to economic insecurity by Mosimann &
  Pontusson 2017) predicts increase — perceived threat motivates collective action,
  particularly when institutional channels for collective response exist.

**Data:**
- European Social Survey rounds 7–9 (2014–2018)
- N = 85,000 individuals
- 18 Western European countries
- ISCO-08 occupation codes merged at 3-digit to RTI task scores (Goos, Manning &
  Salomons 2014)

**Method:** Multilevel logistic regression of union membership on RTI exposure,
with country fixed effects, individual controls (age, gender, education, income
decile, employment status), and a cross-level interaction with country-level
sectoral bargaining coverage (Visser ICTWSS).

**Headline finding:** Automation exposure increases union membership probability
by 4.2 percentage points (β = 0.042, SE = 0.011, p < 0.001), but only in
countries with strong sectoral bargaining (top tercile of ICTWSS coverage).
In countries with weak sectoral bargaining (bottom tercile), the effect is
indistinguishable from zero (β = 0.003, SE = 0.014, p = 0.83).

**Robustness:**
- Falsification using occupational tenure (placebo: no effect)
- Alternative RTI measures (Autor-Dorn 2013; Acemoglu-Restrepo 2020)
- Restricted sample excluding public-sector workers (effect persists, β = 0.038)
- Heterogeneity by education (concentrated among non-college workers)

**Contribution:** Reframes the automation-and-politics debate by showing that
worker responses to economic disruption are not uniform; the institutional
infrastructure for collective response moderates whether anxiety produces
solidarity or atomisation.

---

## Demo Task

Worker (`writer` agent): Draft a 300-word abstract using the ingredients above.
Follow the standard economics abstract structure (motivation, data, method,
finding, contribution) and the project's voice conventions per
`manuscripts/Writing Samples/Voice and Writing Style.txt` (no em-dashes;
semicolons preferred; transitions like "Indeed", "Through this perspective",
"undergirding").

Critic (`writer-critic` agent): Score the abstract against the 6 check categories
(structure, claims-evidence, identification fidelity, writing quality, grammar,
compilation). Produce a deduction-itemised report.

Then iterate: worker revises based on critique, critic re-scores. Stop after
round 2 or when score >= 90, whichever first.

---

## What we are demonstrating

1. **Separation of powers** — the critic cannot soften findings on its own work
   because it did not produce the work.
2. **Iteration mechanics** — score deltas, revision focus, convergence.
3. **Rubric enforcement** — the critic evaluates against a fixed rubric, not on
   vibes.

This demo does not produce anything for the seminar paper. It is purely to
verify the harness behaves as designed before we trust it on real prose.
