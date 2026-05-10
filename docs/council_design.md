# Council Design — `/council-critique` and `/council-ideate`

> The council pattern: dispatch named expert personas in parallel, synthesise their outputs separately, never majority-vote on narrative output. Two project-level specialisations of the generic user-level `/council` command, calibrated to Ben's research-domain agents.

---

## Purpose

Council exists to protect against two failure modes of solo research: (1) myopic critique, where a single reviewer's framing dominates and surfaces only the issues that framing privileges; and (2) under-pressured ideation, where a promising idea hardens into commitment before the author has stress-tested it from non-obvious angles. Council buys structured adversarial diversity in a single turn, with parallel dispatch keeping the wall-clock cost roughly equal to one critique. Use when the artefact or idea is consequential enough to warrant 5 minutes of multi-perspective scrutiny — pre-submission paper review, identification-strategy memos, thesis-chapter direction, or before committing a research extension to the workplan.

---

## Two Variants

**`/council-critique`** evaluates work in progress. Five named personas operate in parallel, each dispatched to one of Ben's specialised research agents. A synthesis pass identifies convergent issues (high-confidence problems flagged by multiple personas), divergent issues (judgement-call territory), missing dimensions (what nobody flagged), and produces a ranked top-three actions. Suited to: paper drafts, identification memos, draft chapters, slide decks, robustness sections.

**`/council-ideate`** generates and pressure-tests ideas. Four generative personas (three parallel + one synthesis) produce specific concrete angles rather than caveats — the critical filtering happens in the synthesis layer, not in the personas themselves. Suited to: research extensions, thesis direction, chapter-question framing, methodological pivots.

---

## Persona-to-Agent Mapping — `/council-critique`

| Persona | Agent dispatched | Framing prompt prepended |
|---|---|---|
| The Skeptic | `econometrician` | "Assume the central result is wrong. What's the most plausible reason?" |
| The Methodologist | `methods-referee` | "What specification or robustness check would a methods referee at the target journal demand?" |
| The Pre-mortem | `strategist-critic` | "The paper got rejected. In two sentences, what does the rejection letter say about the identification strategy?" |
| The External-Validity Hawk | `domain-referee` | "Where does this not generalise? Whose context is missing from the sample / theory / framing?" |
| The Contribution Auditor | `editor` | "Strip the literature review back to nothing. What's the *new* claim that earns this paper its space?" |

Each persona prompt prepends the framing to: (a) the artefact summary, (b) the artefact path for the agent to Read, (c) the explicit output shape `## Top issues / ## Specific suggestions / ## What you don't know / ## Confidence`.

---

## Persona-to-Agent Mapping — `/council-ideate`

| Persona | Agent dispatched | Framing prompt prepended |
|---|---|---|
| The Obvious Extension | `general-purpose` | "What's the boring, predictable next move from this work that any supervisor would suggest? Be specific." |
| The Adjacent Outsider | `general-purpose` | "What's the contrarian move from a discipline next door — sociology, behavioural economics, social psychology — that the author would otherwise miss?" |
| The Constraint Inverter | `general-purpose` | "What's the version of this idea that's only possible if the usual constraint (cross-sectional data, small N, single dataset) is dropped?" |
| The Synthesis | (main session, after the three return) | "Given these three angles, what's the research programme over five years that they jointly suggest?" |

Each persona produces: `## Three concrete angles / ## What you'd need to do this / ## Closest existing literature / ## Why someone smart would dismiss this`.

---

## Synthesis Protocol

The skill body runs synthesis directly in the main session — no sixth subagent dispatch. For `/council-critique`, the synthesis produces:

- **Convergent critiques** — issues flagged by ≥2 personas, high confidence
- **Divergent critiques** — flagged by exactly 1 persona, judgement-call
- **Missing dimensions** — what should have been flagged but wasn't (the synthesiser's own contribution; not just a re-shuffle of inputs)
- **Top three actions** — ranked, with effort estimate per action

For `/council-ideate`, the synthesis produces:

- **The convergent thread** — angle visible across all three personas
- **The boldest single move** — the angle with highest information value if it works
- **A five-year research programme** combining the three
- **Three things to check before committing** — falsifiers, scoop risks, data feasibility

Synthesis defaults to **Mode 2** on Ben's criticism scale (priority — the 3-5 most impactful issues). Ranked, not exhaustive. Hold further notes if asked.

---

## Invocation Examples

```
/council-critique manuscripts/paper_draft_v4_final.md
/council-critique projects/seminar_paper/identification_memo.md
/council-ideate "extend the asymmetric-welfare framework to non-Western European contexts"
/council-ideate docs/learning_econometrics/01_counterfactual_question.md
```

Reports save to `quality_reports/council_critiques/YYYY-MM-DD_<artefact-stem>.md` and `quality_reports/council_ideations/YYYY-MM-DD_<topic-slug>.md` respectively. The compact summary printed to the user is actionable in under 60 seconds; the full report is for archive and re-read.

---

## What Council Is *Not*

- **Not a substitute for human supervisor review.** Five LLM critics surface known categories of problem, not novel ones. An advisor still sees what nobody has trained the agents to see.
- **Not used for code review.** The existing `coder-critic` (currently archived; reactivate if data work resumes) is the right tool. Council adds nothing there.
- **Not a brainstorm-with-self tool.** It's structured adversarial review. If the task is "help me think about X," that's `/grill-me` territory, not council.
- **Not a replacement for the user-level `/council` command.** That command at `~/.claude/commands/council.md` remains the generic parallel-critic pattern (with `--type plan/paper/decision/grant/chef-skill`). The two project skills here are *specialisations* — they hard-wire the persona-to-agent mapping for Ben's research workflow rather than resolving panel from flags. Use the user-level `/council` for non-research tasks (skill design, plan reviews, decisions); use the project skills for paper/idea work.
