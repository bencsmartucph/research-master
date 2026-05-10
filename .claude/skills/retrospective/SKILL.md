---
name: retrospective
description: Run a four-persona post-deployment retrospective audit. Each persona reads the handover spec(s), session logs, and deployed artefacts, then assesses spec-vs-output alignment, cross-artefact coherence, future-user usability, and missed-opportunities. Produces a synthesised report. Use after a multi-artefact deployment (handover execution, repo refactor, infrastructure rollout) to catch hallucinations and gaps before they harden.
---

# /retrospective

**Usage:** `/retrospective --handover <path> [--handover <path> ...] [--since YYYY-MM-DD] [--name <slug>]`

Examples:
```
/retrospective --handover docs/repo_building/ops_handover_council.md --since 2026-05-08 --name council-deployment
/retrospective --handover docs/repo_building/ops_handover_phase_2.md --since 2026-05-08 --name phase-2-deployment
/retrospective --handover docs/repo_building/ops_handover_council.md --handover docs/repo_building/ops_handover_phase_2.md --since 2026-05-08 --name council-and-phase-2
/retrospective --handover docs/strategic_memo_2026-04-25.md --since 2026-04-25 --name asymmetric-paper-pivot
```

Four-persona retrospective audit, parallel dispatch, separate synthesis. Saves a full report to `quality_reports/retrospectives/` and prints a compact action list. Reference design: same architectural pattern as `/council-critique` but with **handover-spec + session-logs + deployed-files** as inputs (not a single artefact) and personas calibrated for spec-vs-output alignment (not methodology critique).

This skill exists to fill the gap that `/critique` (single-file) and `/council-critique` (single-artefact, methodology-focused) don't cover: post-deployment retrospective auditing across multiple files.

---

## Phase 1 — Resolve inputs

1. **Handover document(s).** Required. Read every `--handover <path>` argument; concatenate as the *spec*. If no handover provided, ask:
   > *"Which handover document(s) is this retrospective auditing? Provide one or more `--handover <path>`."*
2. **Since date.** Optional. Default: the mtime of the oldest handover document (i.e., everything since the spec was written).
3. **Name slug.** Optional. Default: derived from the handover filename(s). Used for the output file path: `quality_reports/retrospectives/YYYY-MM-DD_<slug>.md`.
4. **Build the artefact corpus.** Read these in this order, capping at ~40 files:
   - All handover documents (the *spec*)
   - All `quality_reports/session_logs/*.md` with mtime >= `--since` (the *execution narrative*)
   - `SESSION_REPORT.md` entries since `--since` (filter by date heading)
   - `quality_reports/research_journal.md` entries since `--since`
   - All files modified in `git log --since=<date> --name-only --pretty=format:` (the *deployed artefacts* — restrict to files explicitly named in the handover acceptance criteria, and any new skill / agent / config files)
   - All `projects/*/STATUS.md` files (for context on what was active)
5. **Git state context.** Run `git log --since=<date> --oneline` and capture the commit list — the personas need to see what was committed vs. what's still pending.

Skip files under `quality_reports/session_logs/_private/` per the privacy convention.

## Phase 2 — Build the seed summary

Dispatch **one** `general-purpose` Task call with prompt:

> *"Read the handover document(s) at <paths>. Then read the session logs in `quality_reports/session_logs/` with mtime >= <date>. Produce a 300-word 'spec vs. delivery' summary covering: (a) what the handover(s) set out to build (acceptance criteria), (b) what session logs say was actually delivered, (c) what session logs say was deferred or descoped, (d) what's currently uncommitted vs. pushed (per the git state). Plain prose, no headings."*

Wait for return. The returned summary is `<deployment_summary>` — every persona sees this so they audit the same understood facts.

## Phase 3 — Dispatch four retrospective personas in parallel

Send **one message containing four `Task` tool calls** (true parallelism — sequential dispatch is too slow). All four use `subagent_type: general-purpose`.

| Slot | Persona | Framing prompt |
|---|---|---|
| 1 | **Spec-vs-Output Auditor** | "Walk every acceptance criterion in the handover document line by line. For each `- [ ]` item: was it actually delivered? Did execution silently widen or narrow scope? Quote the spec and the deployed file together when they disagree." |
| 2 | **Cross-artefact Coherence Critic** | "Do the deployed pieces fit together as a system? Look for: contracts between skills (e.g., does /done's controlled vocabulary match /recall's topic-keyword pre-filter?); shared frontmatter between voice-ben and voice-audit; hook scope filters that should mirror skill scope_excludes; agent dispatch references between skills; any place where two pieces *should* talk but don't." |
| 3 | **Future-User Usability Critic** | "Will the user-of-six-months-from-now (with degraded session memory of why this was built) successfully invoke each piece, recover from failure, and discover the right tool for the job? Look for: invocation discoverability, error message clarity, natural-language trigger fidelity, cognitive overhead, multi-step workflow friction." |
| 4 | **Missed-opportunities Reviewer** | "What's nearby and obvious that the deployment did NOT do? Adjacent skills the handover hinted at but skipped. Patches that would take 5 minutes and pay rent for years. Patterns that would compound. Cross-cutting fixes whose absence is currently invisible. Be specific — name files, name patterns, name what to add." |

**Each prompt body:**

```
You are operating as <PERSONA NAME> on a post-deployment retrospective.

Persona framing: <FRAMING PROMPT>

Inputs to read:
- Handover spec(s): <paths> (the *intent*)
- Session logs since <date>: <paths in quality_reports/session_logs/> (the *execution narrative*)
- SESSION_REPORT.md entries since <date> (the *consolidated log*)
- Deployed files: <paths from git log --since> (the *output*)
- Git commit list since <date>: <list>

Brief summary for context (read the actual files for details):
<deployment_summary from Phase 2>

Produce a structured report with EXACTLY these four headings:

## Findings (ranked)
(3-5 bullets, ranked. Each bullet: one-sentence finding + severity CRITICAL / MAJOR / MINOR. Quote source lines where relevant. Stay in your persona's framing.)

## Specific recommendations
(2-4 bullets. Concrete and actionable: which file to edit, which line to change, which test to run.)

## What you don't know
(1-3 bullets. Things you would need to see to give a stronger verdict. Be specific about the file or section.)

## Confidence
(One paragraph: how sure are your findings? What would change your mind? What's the strongest evidence for and against your top finding?)

Do NOT praise. Start with problems. Stay in your persona — leave synthesis to the orchestrator.
Do NOT speculate beyond what's in the source files. The retrospective is an audit, not a brainstorm.
```

**Failure handling:** if any of the four returns an error, note in synthesis and continue. Do not block.

## Phase 4 — Synthesise (main session, no extra dispatch)

After all four Task calls return, the main session produces the synthesis directly. **Do NOT dispatch a fifth Task call.**

Read the four raw reports as input data and produce these sections (note: ranked, Mode 2 calibration — top 3-5 most impactful, not exhaustive):

**`## Convergent findings`** — issues flagged by ≥2 personas. Group them; cite which personas raised each. These are high-confidence problems.

**`## Divergent findings`** — flagged by exactly one persona. Note which. Judgement-call territory; user decides if they bite.

**`## Promised but not delivered`** — items where the handover's acceptance criteria say one thing and the deployed files don't fully match. Quote both. This is the highest-stakes category — silently-narrowed scope is the worst-case audit failure.

**`## Delivered but not specified (scope creep)`** — items the deployment included that the handover did not call for. Could be helpful additions or scope drift; user decides.

**`## Top three high-leverage follow-ups`** — ranked, concrete, with effort estimate per action. These are the items worth adding to `docs/post_handover_followups.md` (or wherever the user tracks active work).

## Phase 5 — Save full report

Path: `quality_reports/retrospectives/YYYY-MM-DD_<slug>.md`. Create the directory if missing.

File structure:

```markdown
# Retrospective — <name>

**Date:** YYYY-MM-DD
**Handover(s) audited:** <paths>
**Since:** <date>
**Commits in scope:** <list>
**Personas:** Spec-vs-Output Auditor, Cross-artefact Coherence Critic, Future-User Usability Critic, Missed-opportunities Reviewer

---

## Synthesis

<the five sections from Phase 4>

---

## Raw persona reports

<details>
<summary>Spec-vs-Output Auditor</summary>

<full raw report>

</details>

<details>
<summary>Cross-artefact Coherence Critic</summary>
...
</details>

<details>
<summary>Future-User Usability Critic</summary>
...
</details>

<details>
<summary>Missed-opportunities Reviewer</summary>
...
</details>
```

Always save the file, even if synthesis is partial because of failures. Note failures explicitly in the synthesis.

## Phase 6 — Print compact summary

Print to the user (in chat, NOT in the saved file):

```
Retrospective: <slug>

Convergent findings: <count> | Divergent: <count> | Promised-not-delivered: <count> | Scope creep: <count>

Top three follow-ups:
1. <action one — one line>
2. <action two — one line>
3. <action three — one line>

Full report: quality_reports/retrospectives/YYYY-MM-DD_<slug>.md

Suggested next move: append items 1-3 to docs/post_handover_followups.md.
```

Never silently exit. Always print something even if synthesis failed.

---

## Implementation rules

- **Parallel dispatch is non-negotiable.** One message, four Task calls. Sequential dispatch makes this skill too slow.
- **No fifth Task call for synthesis.** The main session synthesises directly.
- **No voice-ben pass.** Retrospective reports are internal infrastructure, not signed prose.
- **No iterative debate.** Single round only.
- **No fabricated quotes.** Personas must cite actual lines from the source files. If a persona's report contains a quote, the quote must be verifiable.
- **Honour `_private/`.** Skip session logs under `quality_reports/session_logs/_private/`.
- **Mode 2 in synthesis.** Top 3-5 actions ranked. Hold further notes if asked.
- **Cite paths every time.** Every finding in the synthesis must trace to a specific file. No floating claims.

---

## What this skill is *not*

- **Not `/critique`.** That single-file pass is for prose hallucination-checking. Retrospective audits the deployment as a system.
- **Not `/council-critique`.** That single-artefact pass uses methodology-calibrated personas. Retrospective uses alignment-calibrated personas with both spec and output as inputs.
- **Not `/voice-audit`.** That deterministic check verifies prose against the voice spec. Retrospective audits skills, agents, and infrastructure files.
- **Not auto-triggered.** Manual invocation only — typically once per major handover or deployment.
- **Not a substitute for the user-level `/council --chef-skill`.** That's per-skill design review. Retrospective is cross-cutting.
