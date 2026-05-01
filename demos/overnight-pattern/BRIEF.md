# Demo Brief — Multi-Agent Overnight Pattern

**Date:** 2026-05-01
**Branch:** `claude/ai-trends-analysis-xzncF`
**Purpose:** Demonstrate trustworthy multi-agent workflow for "overnight" research tasks — the use case where Ben hands Claude a question before bed and wakes to a draft, with critics catching errors before they accumulate.

---

## The Research Question (synthetic but realistic)

**Q:** The asymmetric mechanism predicts that conditionality-introducing welfare reforms produce damage signatures (elevated RTI → exclusion slopes) but that decommodification expansions do not produce mirror-image protective signatures of equivalent strength. What does the existing literature say about this asymmetry, and is the descriptive empirical pattern consistent with it?

This is a question Ben would actually ask. The seminar paper takes the asymmetric position; the thesis design tests it causally. The literature and empirical legs of the answer should be tractable in ~30 minutes of agent work.

---

## Two Tracks (run in parallel)

### Track 1 — Literature Synthesis

**Worker:** `librarian`
**Critic:** `librarian-critic`

**Task:** Synthesise 3 papers from `docs/literature/` that bear on the asymmetric mechanism. Produce a 400–600 word note covering:
- What each paper claims about welfare design's political effects
- Whether each paper is more consistent with a symmetric or asymmetric reading
- Where the literature has gaps the seminar paper addresses

Save synthesis to `demos/overnight-pattern/lit_synthesis_v1.md`.

**Expected critic findings:** missing key papers, weak theoretical framing, citation accuracy issues, gaps the synthesis fails to identify.

### Track 2 — Empirical Descriptive

**Worker:** `coder`
**Critic:** `coder-critic`

**Task:** Write a Python script that loads `data/samples/baccini_ESSdata_sample100.csv` and produces a descriptive scatterplot of routine task intensity (`isco08` truncated to 3-digit, mapped to a synthetic RTI proxy if needed) versus an anti-immigration attitude variable, faceted by country.

Constraints (per project rules):
- No embedded title in the figure (per `.claude/rules/figures.md`)
- Serif font family
- Show all years on the x-axis if temporal
- Save as PDF to `demos/overnight-pattern/fig_rti_vs_attitudes_descriptive.pdf`
- Save script to `demos/overnight-pattern/script_rti_descriptive.py`

**Expected critic findings:** missing theme compliance, hardcoded paths, missing assertions, missing reproducibility scaffolding (set.seed equivalent), placeholder content where real ESS columns should be.

---

## Demo Goals

1. **Show parallel multi-agent dispatch** — both tracks run simultaneously
2. **Show critic catching real issues** — issues that would degrade autonomous overnight runs if uncaught
3. **Show the trust tier in practice** — these are the contexts where the rubrics ARE complete (no voice dependence)
4. **Identify any harness frictions** — same conflicts the writer-critic pair surfaced (report-writing instruction conflict, etc.) may appear here too

After both tracks complete, parent agent (in main session) writes a synthesis memo capturing what worked, what the critics caught, and what overnight mode would need to look like to be safe.

---

## Out of scope

- Full identification strategy (strategist agent) — separate demo
- Editorial polish of any prose produced — covered by writer-critic-ben demo
- Causal claims — this is descriptive only

---

*Note: The literature notes in `docs/literature/` are pre-existing summaries; the librarian synthesises across them rather than reading PDFs in this demo.*
