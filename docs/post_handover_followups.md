# Post-Handover Follow-ups

> Tracker for actions surfaced by the council and voice-audit deployments. This file is the working list — update as items are completed, defer with reasons, or escalate.
>
> **Last updated:** 2026-05-08
> **Related files:** `docs/ops_handover_council.md`, `docs/ops_handover_phase_2.md`, `quality_reports/council_critiques/2026-05-08_empirical_walkthrough_v1.md`, `quality_reports/council_ideations/2026-05-08_extend_asymmetric_welfare_danish_registry.md`, `quality_reports/voice_audits/2026-05-08_paper_draft_v4_final.md`

---

## Priority 1 — do within the next 7 days

### 1.1 Audit step — read all three council/audit reports end to end

This is the validation step before relying on the new skills. Skim each report and ask: *did this surface real issues, or hallucinate plausible-sounding ones?* If real → skills are validated and you can lean on them. If mixed → adjust the persona prompts before next use.

- [ ] Read `quality_reports/council_critiques/2026-05-08_empirical_walkthrough_v1.md`
- [ ] Read `quality_reports/council_ideations/2026-05-08_extend_asymmetric_welfare_danish_registry.md`
- [ ] Read `quality_reports/voice_audits/2026-05-08_paper_draft_v4_final.md`

**Time:** ~45 minutes total.
**Outcome:** decision on whether the skills are calibrated correctly. If they are, the rest of this tracker is actionable; if they aren't, the calibration step comes first.

### 1.2 Fix the four em-dash apposition stackings in `paper_draft_v4_final.md`

Voice-audit flagged this exact pattern (the 2026-05-08 voice-ben update warned about it). It's quick, concrete, and the paper text reads more like your voice afterwards. Lowest-risk action on the list.

- [ ] Open `manuscripts/paper_draft_v4_final.md`
- [ ] Find each em-dash apposition stacking (the audit report names them with line numbers)
- [ ] Replace with semicolon, colon, or sentence break per voice-ben spec
- [ ] Re-run `/voice-audit` to confirm the score moves up
- [ ] If the score moves into the 75+ range, voice-audit is calibrated correctly; if not, investigate

**Time:** ~30 minutes.
**Outcome:** paper draft cleaner; voice-audit calibration confirmed.

### 1.3 Decide on the timing of TOST + SUR (council Action 2)

This is the biggest substantive upgrade the council surfaced. Two paths:

**Path A — Implement now, before any seminar revision deadline.** Pros: the seminar paper goes from "consistent with asymmetric mechanism" to "formally rejects symmetric buffering at p<X." Cons: 1–2 day analysis project, you just gave the talk and need recovery time.

**Path B — Queue for the journal-version revision after seminar feedback.** Pros: lets seminar feedback inform what to test exactly. Cons: it's exactly the kind of thing a methods referee will demand later, so you're paying twice (one round of feedback + one revision-to-add-it).

- [ ] Decide path (recommend Path B unless seminar feedback demands faster turnaround)
- [ ] If Path A: schedule the 1–2 day work block. If Path B: log this as a thesis-cycle todo and proceed.

**Time decision (not implementation):** ~10 minutes after reading the council critique.

---

## Priority 2 — queue for the next paper revision cycle

### 2.1 Specification curve over the BLUPs/OLS estimator menu (council Action 1)

You already have the four estimates (BLUPs −0.855, OLS-with-controls −0.786, bivariate −0.625, country-wave averaged −0.702). Adding a few more reasonable specifications and plotting the curve converts the methodology disclosure issue into a robustness *strength*.

- [ ] When in revision mode: produce `outputs/figures/walkthrough/spec_curve_cwed_correlation.png`
- [ ] Update the §V.D paper text to point at the curve as the headline robustness signal
- [ ] Replace the existing one-disclosure-sentence with "the result is robust across the methodology menu, with X% of the spec curve mass below r = −0.7"

**Time:** ~3–4 hours of analysis work plus 30 min of writing.
**When:** during the next paper revision pass.

### 2.2 Literature positioning vs Vlandas-Halikiopoulou (2022), Ennser-Jedenastik (2019), Gingrich (2019) (council Action 3)

The Contribution Auditor flagged scoop risk on the moderation claim. A single careful paragraph in the introduction situating your moderation finding against theirs is sufficient.

- [ ] During next intro revision: read or re-skim those three papers if you haven't recently
- [ ] Draft the differentiating paragraph
- [ ] Voice-audit the result before finalising

**Time:** ~1–2 hours.
**When:** during the next intro revision pass.

### 2.3 Address low transition-density flag from voice-audit

Voice-audit signalled that the paper has a low density of your distinctive transitions (*Indeed, Furthermore, Through this perspective, Effectively, Drawing on*). Adding 3–5 of these in the right places would lift the voice-audit score and make the prose feel more like yours.

- [ ] Identify 3–5 paragraph transitions in `paper_draft_v4_final.md` that currently use generic connectives (*also, additionally, however*)
- [ ] Replace with your distinctive transitions where the meaning fits
- [ ] Re-run voice-audit; expect the score to move 5–10 points

**Time:** ~1 hour.
**When:** during the next paper revision pass; bundle with 2.2.

---

## Priority 3 — bedding-in actions over the next 2–3 weeks

These build the habits that make the new infrastructure pay its rent over the PhD horizon.

### 3.1 Run `/done` at the end of the next 5–10 real sessions

Without a populated session-log corpus, `/recall` returns nothing and the controlled-vocabulary topic list never gets validated. Five to ten clean session captures is the threshold where `/recall` starts being useful for finding past decisions.

- [ ] After your next 5+ real working sessions, invoke `/done` at the end and commit the resulting session log
- [ ] After ~5 logs accumulate, run `/recall` against a known past decision to see if it surfaces correctly
- [ ] If topics in the controlled vocabulary feel wrong, edit the skill body to refine them

**Time:** ~2 minutes per session × 5–10 sessions.

### 3.2 Run `/council-critique` on one more artefact within 2 weeks

Single-test-run validation isn't enough to know the skill is reliable. Pick a different kind of artefact for the second run.

- [ ] Suggested target 1: `docs/learning_econometrics/01_counterfactual_question.md` (different domain, different format)
- [ ] Or: a draft identification memo for the thesis design when you start one

**Time:** ~10 minutes to invoke + ~20 minutes to read the report.

### 3.3 Run `/voice-audit` on the next paper-tier prose you produce

The audit improves with calibration data. Running it on three or four pieces of prose lets you see whether the score-to-quality mapping is well-calibrated for your voice specifically.

- [ ] Next time you write a paper section, abstract, or grant text: run `/voice-audit` before finalising
- [ ] Track scores in a small log (`quality_reports/voice_audit_log.md`) so you can see drift over time

---

## Priority 4 — longer horizon

### 4.1 Phase 3 handover: continuous improvement pipeline

On standby per `ops_handover_phase_2.md`. Trigger conditions: Phase 1 (council) and Phase 2 (memory + voice) have been used regularly for at least 2–3 weeks, and you have a clear sense of the patterns where new ideas/tips/skills enter your awareness but don't get systematically captured.

- [ ] Wait until council and `/done` are habitual (probably late May or June 2026)
- [ ] Then write the handover and execute it

**Time:** TBD; rough estimate 3–4 hours of execution.

### 4.2 Quarterly MEMORY.md `[LEARN]` review

The two MEMORY.md updates from this handover round added 8 [LEARN] entries (3 from Phase 1 council, 5 from Phase 2). These compound, but they also drift — entries that were true 6 months ago may not be true today. Quarterly review catches drift.

- [ ] Set a calendar reminder for ~2026-08-08 (3 months out)
- [ ] At that review: read each [LEARN] entry, mark as still-true / partially-true / superseded / delete

**Time:** ~30 min per quarter.

### 4.3 `/recall` upgrade to vector-search backend

Deferred 12–18 months per `ops_handover_phase_2.md`. Trigger condition: the session-log corpus exceeds ~50 files and `/recall` MVP starts truncating or missing relevant entries.

- [ ] Defer until trigger condition met (probably mid-2027)

---

## Cross-cutting notes

- **Don't act on Priority 2 items until you're already in a paper revision cycle.** Doing them speculatively wastes effort if seminar feedback redirects the paper. The seminar response window is the natural trigger.
- **The voice-audit score is a thermometer, not a target.** Don't optimise for the number; optimise for the violations it identifies.
- **Council reports are reference material, not implementation lists.** Save them, re-read them when revising the relevant artefact, but don't try to implement everything they suggest. The council is an idea generator; you're the filter.

---

## Revisit cadence

This file should be touched whenever:
- A Priority 1 item is completed (mark it, add resulting follow-ups)
- A council or voice-audit run surfaces new actions worth tracking
- Phase 3 handover is triggered (which closes most of Priority 4)

Quarterly: full review. Delete completed items, escalate anything that's been in Priority 2 for more than 6 months without progress.
