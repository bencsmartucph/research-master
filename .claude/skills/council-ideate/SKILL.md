---
name: council-ideate
description: Run a four-persona generative council that produces creative angles on a research idea or artefact, then synthesises them into a five-year research programme suggestion. Use when the user wants ideation help, idea pressure-testing, or protection from myopia on a research direction.
---

# /council-ideate

**Usage:** `/council-ideate path/to/doc.md` *or* `/council-ideate "research direction in quotes"`

Three generative personas in parallel, one synthesis pass, single round. Saves a full report to `quality_reports/council_ideations/` and prints a compact summary. Reference design: [docs/council_design.md](../../../docs/council_design.md).

**Critical difference from `/council-critique`:** the three parallel personas are *generative*, not critical. They are unleashed to produce concrete angles, not caveats. The critical filter happens *only* in the synthesis layer. If the personas come back hedged, the prompt is broken — re-issue with more emphasis on "specific concrete suggestions."

---

## Phase 1 — Resolve input

The argument is either:

- **A file path** (ends in `.md`, `.tex`, `.txt`, or contains `/` or `\`) — treat as document.
- **A literal topic string** (anything else, especially when quoted) — treat as research direction.

Slug for output naming: if path, use the filename stem; if string, take the first 6-8 words and snake_case them.

## Phase 2 — Frame the topic

**If a document:** dispatch one `general-purpose` Task call to summarise:
> "Read `<path>`. Produce a 200-word summary covering the central idea, the methodological approach, the data, the headline finding, and one or two visible limitations. Plain prose."

The returned summary becomes `<framing>`.

**If a topic string:** in the main session, expand it into a 2-3 sentence framing that names the empirical context, the proposed mechanism, and what would count as evidence. Example input: `"extend the asymmetric-welfare framework to non-Western European contexts"`. Example expansion: *"Ben's asymmetric-welfare paper documents that welfare generosity dampens populist response to economic disruption, but only in Western European democracies. The proposal is to extend this framework to non-Western contexts — Eastern Europe, East Asia, Latin America — where welfare institutions, populist parties, and disruption channels differ substantially. Evidence would require comparable cross-national data on economic disruption, vote choice, and welfare regime."*

`<framing>` becomes the seed text for all three personas.

## Phase 3 — Dispatch three generative personas in parallel

Send **one message containing three `Task` tool calls** (parallelism is essential for usable response time). All three use `subagent_type: general-purpose`.

| Slot | Persona | Framing line (prepend to prompt) |
|---|---|---|
| 1 | The Obvious Extension | "What's the boring, predictable next move from this work that any supervisor would suggest? Be specific." |
| 2 | The Adjacent Outsider | "What's the contrarian move from a discipline next door — sociology, behavioural economics, social psychology — that the author would otherwise miss?" |
| 3 | The Constraint Inverter | "What's the version of this idea that's only possible if the usual constraint (cross-sectional data, small N, single dataset) is dropped?" |

**Each prompt body:**

```
You are operating as <PERSONA NAME> on a research-ideation council.

Persona framing: <FRAMING LINE>

The seed: <framing from Phase 2>

Your job is to GENERATE concrete angles, not to caveat. Be specific.
A "concrete angle" names: a research question, a setting / data source,
and one paragraph on why this is worth doing. Avoid abstraction.

Produce a structured report with EXACTLY these four headings:

## Three concrete angles
(Numbered 1-3. Each angle: question + setting + one-paragraph rationale.)

## What you'd need to do this
(Per angle: data, method, partnerships, time horizon. Bullet form.)

## Closest existing literature
(Per angle: 1-3 specific papers or research programmes the angle is in conversation with. Authors and approximate dates are enough — don't fabricate citations.)

## Why someone smart would dismiss this
(One paragraph. The strongest objection a senior critic would raise — feasibility, novelty, identification, scoop risk.)

Stay generative. The synthesiser will filter; you propose.
```

**Failure handling:** if any returns an error, note in synthesis and continue. Do not block.

## Phase 4 — Synthesise (in main session)

After all three Task calls return, the main session produces the synthesis directly. **No fourth Task dispatch** — synthesis is "The Synthesis" persona, executed by the main session reading the three outputs.

Produce four sections:

**`## The convergent thread`** — what angle or theme is visible across all three personas? Even when they're proposing very different ideas, there is usually a deeper question they all converge on. Name it.

**`## The boldest single move`** — of all the angles proposed, which has the highest information value if it works? Bold ≠ reckless. Bold = high payoff conditional on feasibility.

**`## A five-year research programme combining these`** — a short narrative (3-5 paragraphs) describing how a PhD or early-career researcher could build a coherent agenda from these threads. Year-by-year is fine; thematic phases are also fine. Concrete: name papers, datasets, conferences.

**`## Three things to check before committing`** — falsifiers, scoop risks, data feasibility. The critical filter that the personas didn't apply. Default to **Mode 2** of Ben's criticism scale (3 priority items, not a 15-item risk register).

## Phase 5 — Save full report

Path: `quality_reports/council_ideations/YYYY-MM-DD_<slug>.md`. Create the directory if missing.

File structure:

```markdown
# Council Ideation — <topic or path>

**Date:** YYYY-MM-DD
**Input:** <path or "<topic string>">
**Framing:** <2-3 sentence framing from Phase 2>
**Personas:** Obvious Extension, Adjacent Outsider, Constraint Inverter (synthesis by main session)

---

## Synthesis

<four sections from Phase 4>

---

## Raw persona reports

<details>
<summary>Obvious Extension</summary>
<full raw report>
</details>

<details>
<summary>Adjacent Outsider</summary>
...
</details>

<details>
<summary>Constraint Inverter</summary>
...
</details>
```

Always save, even if synthesis is partial because of failures.

## Phase 6 — Print compact summary

Print to the user (in chat, NOT in the saved file):

```
Council ideation: <slug>

Boldest move: <one line — the standout angle>

Five-year programme thread: <one or two sentences>

Three checks before committing:
1. <check one>
2. <check two>
3. <check three>

Full report: quality_reports/council_ideations/YYYY-MM-DD_<slug>.md
```

Never silently exit.

---

## Implementation rules

- **Parallel dispatch is non-negotiable.** One message, three Task calls.
- **No fourth Task call for synthesis.** Main session does it.
- **No voice-ben pass.** Council reports are internal.
- **Personas are generative, not critical.** If the returned reports look like risk registers, the persona prompts have been weakened — re-emphasise concrete angles.
- **No fabricated citations.** "Closest existing literature" should name authors / approximate dates only; never invent paper titles or DOIs.
- **Mode 2 in the "three checks" section.** Top three concerns, ranked. Hold the rest unless asked.
