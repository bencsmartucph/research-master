---
name: council-critique
description: Run a five-persona adversarial council review on a paper, memo, or draft, dispatching to specialised research-critic agents in parallel and producing a synthesised report. Use when the user asks for council review, structured critique, or pre-submission review of a research artefact.
---

# /council-critique

**Usage:** `/council-critique path/to/artefact.md`

Five named expert personas reviewing in parallel, separate synthesis pass, single round. Saves a full report to `quality_reports/council_critiques/` and prints a compact action list. Reference design: [docs/council_design.md](../../../docs/council_design.md).

This is a *specialisation* of the user-level `/council` command. Where `/council --type paper` resolves a generic panel, this skill hard-wires Ben's research-critic agents to fixed personas. Use this for paper, memo, identification-strategy, and chapter review. Use the user-level `/council` for skill design, plan reviews, decisions.

---

## Phase 1 — Resolve target

1. Take the artefact path from the user invocation (positional argument).
2. If invocation has no path, ask once: *"Path to the artefact you want the council to review?"*
3. Verify the file exists. If not, abort with `File not found: <path>`.
4. Slug the basename for output naming: `<stem>` = filename without extension, lowercased, non-alnum → `_`.

## Phase 2 — Summarise if large

Check file size. If >500 lines or extension is `.pdf` / `.docx`:

- Dispatch **one** `general-purpose` Task call with prompt:
  > "Read `<path>`. Produce a 200-word summary covering: (a) central claim, (b) identification strategy or methodological approach, (c) data, (d) headline result, (e) any visible limitations the author flags. Plain prose, no headings."
- Wait for return. The returned summary is `<artefact_summary>`.

If ≤500 lines and a text format, skip summarisation. Read the file directly into main context as `<artefact_text>`. Prefer skipping summarisation when feasible — fidelity matters.

## Phase 3 — Dispatch five council personas in parallel

Send **one message containing five `Task` tool calls** (true parallelism — sequential dispatch makes this skill too slow to use). Each call has `subagent_type` set to the agent name and a prompt structured as below.

| Slot | `subagent_type` | Persona | Framing line (prepend to prompt) |
|---|---|---|---|
| 1 | `econometrician` | The Skeptic | "Assume the central result is wrong. What's the most plausible reason?" |
| 2 | `methods-referee` | The Methodologist | "What specification or robustness check would a methods referee at the target journal demand?" |
| 3 | `strategist-critic` | The Pre-mortem | "The paper got rejected. In two sentences, what does the rejection letter say about the identification strategy?" |
| 4 | `domain-referee` | The External-Validity Hawk | "Where does this not generalise? Whose context is missing from the sample / theory / framing?" |
| 5 | `editor` | The Contribution Auditor | "Strip the literature review back to nothing. What's the *new* claim that earns this paper its space?" |

**Each prompt body:**

```
You are operating as <PERSONA NAME> on a council review.

Persona framing: <FRAMING LINE>

The artefact to review: <ARTEFACT PATH>

<If summarised: "Brief summary for context (read the file yourself for details):
<artefact_summary>">

<If not summarised: paste artefact_text inside ---BEGIN/---END fences>

Produce a structured report with EXACTLY these four headings:

## Top issues
(3-5 bullets, ranked. Each bullet: one-sentence problem + severity CRITICAL/MAJOR/MINOR.)

## Specific suggestions
(2-4 bullets. Concrete and actionable, not vague. State what to change.)

## What you don't know
(1-3 bullets. Things you would need to see to give a stronger verdict — pre-trend plots, robustness tables, sample construction details.)

## Confidence
(One paragraph: how sure are you of your top issues? What would change your mind?)

Do NOT praise. Start with problems. Stay in your persona's framing — leave the synthesis to the orchestrator.
```

**Failure handling:** if any of the five returns an error or empty output, note the failure in the synthesis ("`<persona>` failed; not included") and continue. Do not block on individual failures.

## Phase 4 — Synthesise (in main session, no extra dispatch)

After all five Task calls return, the main session produces the synthesis. **Do NOT dispatch a sixth Task call** — `editor` already ran as the Contribution Auditor.

Read all five raw outputs as input data and produce four sections:

**`## Convergent critiques`** — issues flagged by ≥2 personas. Group them; cite which personas raised each. These are high-confidence problems.

**`## Divergent critiques`** — issues flagged by exactly one persona. Note which. These are judgement-call territory; user decides if they bite.

**`## Missing dimensions`** — what *should* have been flagged but wasn't. This is your own contribution as synthesiser, not a re-shuffle. Examples: a control variable nobody questioned, a literature thread none of the personas know.

**`## Top three actions`** — ranked, concrete, with effort estimate per action. Default to **Mode 2** on Ben's criticism scale (the 3-5 most impactful issues only — not a 20-item laundry list).

## Phase 5 — Save full report

Path: `quality_reports/council_critiques/YYYY-MM-DD_<stem>.md`. Create the directory if missing.

File structure:

```markdown
# Council Critique — <artefact path>

**Date:** YYYY-MM-DD
**Artefact:** <path>
**Personas:** Skeptic (econometrician), Methodologist (methods-referee), Pre-mortem (strategist-critic), External-Validity Hawk (domain-referee), Contribution Auditor (editor)

---

## Synthesis

<the four sections from Phase 4>

---

## Raw persona reports

<details>
<summary>Skeptic (econometrician)</summary>

<full raw report>

</details>

<details>
<summary>Methodologist (methods-referee)</summary>
...
</details>

<and so on for the other three>
```

Always save the file, even if synthesis is partial because of failures. Note failures explicitly in the synthesis.

## Phase 6 — Print compact summary

Print to the user (in chat, NOT in the saved file):

```
Council critique: <stem>

Top three actions:
1. <action one — one line>
2. <action two — one line>
3. <action three — one line>

Convergent issues: <count>. Divergent: <count>. Missing dimensions flagged: <count>.

Full report: quality_reports/council_critiques/YYYY-MM-DD_<stem>.md
```

Never silently exit. Always print something even if synthesis failed.

---

## Implementation rules

- **Parallel dispatch is non-negotiable.** One message, five Task calls. Sequential dispatch breaks the use case.
- **No sixth Task call for synthesis.** The main session synthesises directly.
- **No voice-ben pass.** Council reports are internal artefacts, not prose Ben publishes under his name.
- **No iterative debate.** Single round only — round-2 multi-agent literature documents drift toward conformity.
- **Hard cap five personas.** Beyond five, synthesis becomes harder and returns diminish.
- **Mode 2 by default in synthesis.** Top 3-5 actions ranked. Hold further notes if asked.
