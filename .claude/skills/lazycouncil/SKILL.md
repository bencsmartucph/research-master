---
name: lazycouncil
description: Quality-bar-calibrated council review that finds only what blocks excellence AT THE STATED BAR, not perfection. Three personas, mandatory severity classification, feasibility-gated proposals (no raw "you should run X"), ship-oriented two-list synthesis. Use when /council-critique would catastrophize — i.e. when the target is a seminar paper, workshop draft, or any artefact that needs to be excellent-and-soon rather than journal-perfect. Manual invocation: /lazycouncil path/to/artefact.md [--bar workshop|seminar|journal]
disable-model-invocation: false
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task", "Bash"]
---

# /lazycouncil

**Usage:** `/lazycouncil path/to/artefact.md [--bar workshop|seminar|journal]`

Default bar: **seminar**. Three personas review in parallel, every issue is severity-classified against the bar, proposed extensions are feasibility-probed before they reach the user, and synthesis is two short lists only. Saves a report to `quality_reports/lazycouncil/` and a separate deferred-items file.

This is the calibrated counterpart to `/council-critique`. Council-critique finds every problem because its job is to find problems; that is correct for journal pre-submission and wrong for a seminar paper three weeks out. Lazycouncil exists because **critics catastrophize, and the antidote is a critic bound to a quality bar with feasibility-gated proposals.** It guides toward the path of least resistance to excellence, not perfection.

## The three mechanisms (why this is not just "council-critique lite")

1. **Quality-bar calibration.** Every issue every persona raises must be classified `BLOCKS-BAR`, `BLOCKS-HIGHER-BAR-ONLY`, or `COSMETIC`. Only `BLOCKS-BAR` reaches the user. `BLOCKS-HIGHER-BAR-ONLY` is logged to a deferred file and **deliberately not surfaced**. This is the structural anti-catastrophizing valve, not a tonal instruction.
2. **Feasibility-gated proposals.** A persona may propose creative extensions, but proposals do NOT go to the user raw. Each triggers an autonomous feasibility probe (~30 min: data/infra existence + a cheap signal check). Only PASS / UNCERTAIN-with-note extensions appear in synthesis, tagged with the probe result and an effort estimate.
3. **Ship-oriented synthesis.** Output is exactly two lists: ship blockers and feasibility-tested optional upgrades. Nothing else. If there are no ship blockers, the synthesis says so plainly: "Submittable at the <bar> bar. No blockers."

## The bars

| Bar | The question each persona answers | What gets classified BLOCKS-BAR |
|---|---|---|
| `workshop` | "Is the core idea defensible and interesting enough to present?" | Only: the central claim is wrong, incoherent, or uninteresting. Rough edges, missing robustness, thin lit review are NOT blockers. |
| `seminar` (default) | "Would this earn a strong grade and survive a friendly-but-sharp discussant?" | Numbers wrong/inconsistent; a limitation dishonestly hidden; the contribution illegible; a claim the data cannot support stated without hedge. Journal-grade identification armour is NOT a blocker. |
| `journal` | "Would this survive R&R at a good field journal?" | Collapses toward /council-critique severity. If you pick this bar, consider using /council-critique instead — lazycouncil's value is at workshop/seminar. |

The bar is the single most important input. State it explicitly in every persona prompt. When samples disagree on whether something blocks, the bar breaks the tie.

## Phase 1 — Resolve target and bar

1. Take the artefact path (positional arg). Parse `--bar` if present; default `seminar`.
2. Verify the file exists. If not, abort: `File not found: <path>`.
3. `<stem>` = basename without extension, lowercased, non-alnum → `_`.
4. State the resolved bar back to the user in one line before dispatching: *"Reviewing `<path>` at the **<bar>** bar — blockers only, journal-grade concerns filed not surfaced."*

## Phase 2 — Summarise if large

If >500 lines or `.pdf`/`.docx`: dispatch one `general-purpose` Task to produce a 200-word summary (central claim, method, data, headline result, flagged limitations). Otherwise read the file directly as `<artefact_text>` — prefer this; fidelity matters at the seminar bar too.

## Phase 3 — Dispatch three personas in parallel

**One message, three `Task` calls.** Parallel dispatch is non-negotiable.

| Slot | `subagent_type` | Persona | Framing line |
|---|---|---|---|
| 1 | `editor` | The Pragmatist | "What is already good enough at the <bar> bar? What is the shortest path to done? Resist the urge to improve what does not block." |
| 2 | `methods-referee` | The Rigor Auditor | "What would genuinely embarrass the author at the <bar> bar — not at a higher one? A concern that only bites at journal stage is NOT an embarrassment here." |
| 3 | `strategist-critic` | The Curious Extender | "Overnight compute is ~free. What ONE extension would most increase this artefact's interest? Propose it as a testable idea, not a demand — it will be feasibility-probed before it reaches the author." |

**Each prompt body:**

```
You are operating as <PERSONA NAME> on a lazycouncil review.

QUALITY BAR: <bar>. The question you are answering: "<bar question from the table>".
A concern that only bites at a HIGHER bar is explicitly out of scope for your
BLOCKS-BAR list — classify it BLOCKS-HIGHER-BAR-ONLY and move on. Do not
catastrophize. Your job is to protect excellence at THIS bar, not to find every
flaw that exists at any bar.

Artefact: <path>
<artefact_text or summary>

Produce a structured report with EXACTLY these headings:

## Issues (every issue MUST carry a severity tag)
For each issue, one line, prefixed with exactly one of:
[BLOCKS-BAR]            — the artefact fails the <bar> bar until this is fixed
[BLOCKS-HIGHER-BAR-ONLY] — real, but only matters at a higher bar than <bar>
[COSMETIC]              — trivial; mention only if a one-touch fix
Rank BLOCKS-BAR first. Be specific and concrete.

## Shortest fix path
(Only for the BLOCKS-BAR items. The minimum change that clears each. If there
are no BLOCKS-BAR items, write: "No blockers at the <bar> bar.")

## Proposed extension (Curious Extender ONLY; others write "n/a")
(ONE extension. State: the idea, the data/variables it would need, the cheap
signal check that would tell us in ~30 min whether it is worth doing, and what
a positive result would add. It will be feasibility-probed; do not oversell.)

## Confidence
(One paragraph. How sure are you of the BLOCKS-BAR calls specifically?)

Do NOT praise. Do NOT pad. Stay in your persona. The synthesiser handles the rest.
```

## Phase 4 — Feasibility gate (the novel mechanism)

Collect the Curious Extender's single proposed extension (and any extension the other two personas raised as a BLOCKS-BAR fix that requires new analysis).

For **each** such proposal, dispatch one `general-purpose` Task — the **feasibility probe** — with a ~30-minute budget:

```
Feasibility probe. Budget: ~30 minutes. Do NOT do the full analysis.

Proposed extension: <verbatim proposal>

Two questions only:
1. EXISTENCE: do the data, variables, and infrastructure to do this exist in
   this repo? Name the files/columns. If anything required is missing, that is
   a FAIL — say so and stop.
2. CHEAP SIGNAL: if existence passes, run the single cheapest check that
   indicates whether there is likely signal (a descriptive, a correlation, a
   2x2, a quick subgroup mean). Not the full model. Report the raw number.

Return EXACTLY:
VERDICT: PASS / FAIL / UNCERTAIN
EVIDENCE: [files/columns checked; the cheap-signal number with its method]
EFFORT-IF-PURSUED: [rough hours for the real version]
ONE-LINE: [what a positive full result would let the author claim]
```

Rules:
- A proposal with VERDICT FAIL is dropped silently from synthesis (logged to the deferred file with its probe evidence).
- PASS and UNCERTAIN proposals enter synthesis, tagged with the probe's EVIDENCE, EFFORT, and ONE-LINE.
- If a persona proposed no extension, skip the probe for that slot. Never fabricate a proposal to fill the slot.
- Probes run in parallel with each other where there is more than one.

## Phase 5 — Synthesise (main session, no extra dispatch)

Produce exactly two lists. Nothing else in the user-facing synthesis.

**`## Ship blockers (<bar> bar)`** — issues tagged `BLOCKS-BAR` by ≥1 persona, deduplicated, each with the shortest fix path and an effort estimate. If empty: write exactly *"No ship blockers. This is submittable at the <bar> bar."* and stop the list there. Do not soften an empty list with "but you could still…".

**`## Feasibility-tested optional upgrades`** — only probe-PASS / probe-UNCERTAIN extensions, ranked by (interest × ease) using the probe's EFFORT and ONE-LINE. Each entry: the idea, the probe's cheap-signal number, effort, what it would add. The user picks zero or more. Make explicit that zero is a valid and often correct choice.

Everything classified `BLOCKS-HIGHER-BAR-ONLY` by any persona goes to the **deferred file**, NOT the synthesis. One line per item: the issue + which persona + "deferred: bites at higher bar."

## Phase 6 — Save

- Report: `quality_reports/lazycouncil/YYYY-MM-DD_<stem>.md` — the two synthesis lists + raw persona reports in `<details>` blocks + probe results.
- Deferred: `quality_reports/lazycouncil/YYYY-MM-DD_<stem>_deferred.md` — the BLOCKS-HIGHER-BAR-ONLY items, so they are recoverable when the bar later rises (e.g. journal-version rewrite) without polluting the seminar-stage decision.

Create directories if missing. Always save both files even on partial failure.

## Phase 7 — Print compact summary

```
Lazycouncil: <stem> @ <bar> bar

Ship blockers: <n>
<if 0: "Submittable. No blockers at the <bar> bar.">
<if >0: numbered one-liners with effort>

Feasibility-tested upgrades available: <n> (you may take zero)
<numbered one-liners with effort + the cheap-signal number>

Deferred to higher bar: <n> items (filed, not shown) — quality_reports/lazycouncil/..._deferred.md
Full report: quality_reports/lazycouncil/YYYY-MM-DD_<stem>.md
```

## Implementation rules

- **Parallel dispatch non-negotiable** (Phase 3: one message, three Task calls; Phase 4 probes parallel where >1).
- **Hard cap three personas.** Laziness is the feature. Five is for journal stage — use /council-critique.
- **No sixth/fourth synthesis dispatch.** Main session synthesises directly.
- **The bar is mandatory in every persona prompt.** A lazycouncil run with no stated bar is a bug.
- **Never surface BLOCKS-HIGHER-BAR-ONLY items in the synthesis.** They go to the deferred file. Surfacing them defeats the skill's entire purpose.
- **Never present a feasibility-FAIL extension as an option.** The gate is the point.
- **An empty ship-blocker list is a valid, common, good outcome.** Say "submittable" plainly. Do not manufacture concern.
- **Mode 2 by default** on Ben's criticism scale, but the bar already does most of the volume control.
- **No voice-ben pass.** Lazycouncil reports are internal artefacts.

## What this skill is NOT

- **Not /council-critique.** That finds everything at journal severity. This finds only what blocks the stated bar and feasibility-gates its proposals.
- **Not /critique.** That is worker-critic on a single output with full context. This is a calibrated panel.
- **Not /clean-eyes-review.** That audits direction drift with no conversation history. This audits an artefact against a quality bar.
- **Not a rubber stamp.** The Rigor Auditor still has teeth — it is bound to the bar, not muzzled. At the seminar bar a genuinely wrong number is still BLOCKS-BAR.

## Related

- `council-critique` — the full five-persona journal-severity counterpart; use at journal stage.
- `council-ideate` — generative angles, not critique.
- `clean-eyes-review` — direction-drift audit, no history.
- `empirical-probe` — the standalone version of the Phase 4 feasibility mechanism.
