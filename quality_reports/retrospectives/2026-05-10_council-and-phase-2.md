# Retrospective — Council Phase 1 + Phase 2 (memory + voice) Deployment

**Date:** 2026-05-10
**Handovers audited:**
- `docs/repo_building/ops_handover_council.md` (Phase 1: council-critique, council-ideate, agent pruning)
- `docs/repo_building/ops_handover_phase_2.md` (Phase 2: extend /done, build /recall, refactor voice-ben, build /voice-audit)

**Since:** 2026-05-08
**Commits in scope:** `daca47c..4b60d62` (7 commits — council deployment, session memory + voice tooling, post-deployment tracker, talk polish, repo housekeeping, analysis extensions, /done outputs, voice corpus expansion)
**Personas:** Spec-vs-Output Auditor · Cross-artefact Coherence Critic · Future-User Usability Critic · Missed-opportunities Reviewer

---

## Synthesis

### Convergent findings — flagged by ≥2 personas

**1. CRITICAL — Vocabulary contract `/done` ↔ `/recall` is broken at 6 of 17 topics.**
Flagged by **Coherence Critic** (CRITICAL) and **Missed-opportunities Reviewer** (related: hard-coded keyword table will drift).

`/done` writes session logs tagged with one of 17 controlled-vocabulary topics. `/recall`'s Phase 2 pre-filter (`recall/SKILL.md` lines 41-52) only lists keyword-associations for 11 of them. **Missing entirely:** `econometrics`, `data-discovery`, `thesis-design`, `robustness`, `ideation`, `admin`. Sessions tagged with these fall through to full-corpus fallback — recall still works, but the optimisation is structurally blind to a third of your tag space. As more sessions accumulate, this becomes a slowdown.

**2. MAJOR — Single-test validation only; discriminator test on `/voice-audit` was never run.**
Flagged by **Spec Auditor** (MINOR re: discriminator gotcha) and **Missed-opportunities Reviewer** (MINOR re: no regression fixtures across all skills).

The Phase 2 handover line 301 explicitly required testing `/voice-audit` on BOTH `manuscripts/paper_draft_v4_final.md` (real Ben prose) AND `docs/empirical_walkthrough_v1.md` (NOT Ben prose) to verify the audit discriminates. Only the first ran. The discrimination test was a **gotcha note**, not a hard acceptance bullet, but the calibration warning was ignored. Compounds with the broader pattern: each new skill was tested exactly once and no regression fixture was saved.

**3. MAJOR — Cross-skill compositions skipped wholesale.**
Flagged by **Missed-opportunities Reviewer** (MAJOR) and **Future-User Usability Critic** (multi-step workflow friction).

Three concrete missing compositions:
- `/done` does not detect when the session touched `manuscripts/**` and offer to run `/voice-audit` on the modified draft before logging.
- `/recall`'s corpus (`recall/SKILL.md` lines 23-33) lists session logs + STATUS but **omits `quality_reports/council_critiques/` and `quality_reports/voice_audits/`** — the durable decision artefacts that recall should index. Past flagged issues are structurally invisible to recall.
- `/voice-audit` has no integration with `/done`'s STATUS update — voice scores never enter the project record, so trend-tracking over time is manual.

**4. MAJOR — `/voice-audit` documents a `--force` escape hatch but doesn't implement it.**
Flagged by **Future-User Usability Critic** (MAJOR) and implied by **Coherence Critic** (the abort points to a path that doesn't work).

`voice-audit/SKILL.md` Phase 2 abort message tells the user to invoke `/voice-audit <path> --force` to override `scope_excludes`. The skill body has no flag-handler — when future-Ben tries `--force`, the skill will treat it as a second positional argument (file-not-found) or ignore it silently. The recovery path documented in the abort message is broken.

**5. MAJOR — Voice-ben YAML `scope_excludes` and the pre-commit hook diverge in both directions.**
Flagged by **Coherence Critic** (MAJOR) — solo but high-confidence and structurally important.

The hook (`~/.claude/hooks/check-em-dashes.py`) excludes paths NOT listed in voice-ben's YAML: `working-notes/`, `docs/repo_building/`, `HANDOFF.md`, `HANDOVER.md`, `CLAUDE.md`, the `voice_*` filename glob. Conversely, voice-ben names `docs/empirical_walkthrough_v1.md` as a single file but the hook generalises to `empirical_walkthrough_*`. The hook is the *more correct* / *more complete* list; the YAML drifts. `/voice-audit` reads only the YAML, so a manual `/voice-audit docs/repo_building/foo.md` will NOT abort with the scope-excludes refusal even though the hook (and intent) treats it as out-of-scope.

**Bonus convergent issue (also coherence):** the hook's em-dash threshold is `<5/1k` while voice-ben's `diagnostic_targets.em_dashes_per_1000_words` is `<8/1k`. The hook's own warning text says "voice-ben target: <5/1k" — internally contradicting the very spec it claims to mirror.

### Divergent findings — flagged by exactly one persona

- **MAJOR — No skill-ecology README in `.claude/skills/`** (Missed-opportunities only). 22 skills now exist; future-Ben has no map of when to reach for which. The `/critique` vs `/council-critique` vs `/review` vs `/retrospective` boundary is genuinely confusing without one.
- **MAJOR — Controlled vocabulary in `/done` was guessed, not corpus-derived** (Missed-opportunities only). The 17 topics were authored by inspection. The repo has months of session logs that could have been scanned to extract empirical topic distribution. 5 minutes of effort with 4-6 years of payoff.
- **MAJOR — No commit-time gate for council-critique before submission** (Missed-opportunities only). Voice-audit has a recent gate in CLAUDE.md but council-critique does not. A 10-line patch in `.claude/settings.json` checking that a `quality_reports/council_critiques/` entry exists for `manuscripts/<paper>.md` newer than the paper's mtime would close it.
- **MAJOR — `general-purpose` agent file is not in `.claude/agents/`** (Spec Auditor only). Phase 1 acceptance criterion line 273 said "roughly 11 active agents (the *Keep set*)" and the keep set listed `general-purpose.md`. The deployed directory has 10. The harness likely resolves `general-purpose` from a built-in registry — so this is functionally fine, but the spec drift is undocumented.
- **MAJOR — `/done` description leads with architecture not natural-language triggers** (Future-User only). Description starts "Project-level session capture" — six-months-future-Ben says "wrap up", "log this session", "session done" — none appear in the description.
- **MAJOR — Three overlapping critique tools with no top-level disambiguation** (Future-User only). `/critique`, `/council-critique`, user-level `/council`, and `/retrospective` all match queries like "review this draft". I gave you a verbal decision tree in this conversation, but it lives nowhere persistent.
- **MINOR — Archive directory is `archive/` not `_archive/` as specified** (Spec Auditor only). Convention drift; the underscore matters because `_archive/` is the common "skip in autoload" convention. Mitigated by the directory predating this handover.
- **MINOR — MEMORY.md additions exceed the line cap in spirit** (Spec Auditor only). Phase 1 said ≤5 lines, Phase 2 said ≤8; combined we wrote ~12 lines across 7 entries.
- **MINOR — Lexicon ↔ voice-ben YAML have unsynced top-frequency anchors** (Coherence Critic only). `voice_lexicon.md`'s top-30 includes high-frequency terms (`neoliberal`, `deliberative`, `populist`, `discursive`, `institutional`, `norm(s)`) that don't appear in voice-ben's `distinctive_vocabulary`. Either intentional (lexicon as writer-aid superset) or accidental drift.
- **MINOR — `/done`'s "ask before adding new topic" flow has friction risk** (Future-User only). 17 tags is borderline; the new-topic prompt fires at the worst moment (end-of-session).

### Promised but not delivered

- **Voice-audit discriminator test on `docs/empirical_walkthrough_v1.md`** — Phase 2 gotcha (line 301), not formally bullet-pointed; missed. Surfaces as the convergent finding 2 above.
- **The `/council` user-level command's coexistence decision was not logged.** Phase 1 Out-of-Scope point 4 required either deprecation or fold-and-archive. The existing `/council` was left in place — defensible (different scope, different path) but the explicit decision was never recorded in `quality_reports/research_journal.md`.
- **Voice-ben `scope_excludes` is incomplete relative to the hook's real exclusion list.** Convergent finding 5 above.

### Delivered but not specified (scope creep — generally helpful)

- **`voice_lexicon.md`** as a standalone writing-aid was not in either handover spec. Genuinely useful addition, but worth flagging as scope expansion.
- **Pre-commit hook scope filter** in `~/.claude/hooks/check-em-dashes.py` was not a handover deliverable. Good fix; emerged from usage friction.
- **The full-corpus voice extraction (the second pass with subagent-read of all 7 essays)** went well beyond Phase 2's voice-ben "refactor into YAML" bullet — added a comprehensive linguistic catalogue. Helpful but unbudgeted.
- **`/retrospective` skill** (this very skill) was built outside both handovers' scope. Will compound positively across future deployments.

### Top three high-leverage follow-ups

Ranked by leverage / effort. All three are 5-10 minute patches that fix multiple convergent findings.

**1. Sync `/recall`'s topic-keyword pre-filter with `/done`'s controlled vocabulary.** Single-file edit to `.claude/skills/recall/SKILL.md` lines 41-52. Add the 6 missing topics with keyword associations:

```
- `econometrics` ← regression, estimator, fixed effects, clustering, inference, panel
- `data-discovery` ← new dataset, source, register, coverage
- `thesis-design` ← thesis, chapter, PhD scope, registry
- `robustness` ← jackknife, sensitivity, spec curve, leave-one-out
- `ideation` ← brainstorm, council-ideate, direction
- `admin` ← supervisor, deadline, application, email
```

Also: change /recall's table to read /done's vocabulary block at runtime rather than hard-coding, so future drift is impossible. **Effort: ~5 minutes. Fixes: convergent finding 1, divergent finding "hard-coded drift".**

**2. Add `/recall`'s corpus to include council critiques and voice audits.** Two-line edit to `recall/SKILL.md` Phase 1. Add `quality_reports/council_critiques/*.md` and `quality_reports/voice_audits/*.md` to the corpus list. **Effort: ~5 minutes. Fixes: convergent finding 3 (recall structurally indexes flagged issues).**

**3. Reconcile voice-ben YAML `scope_excludes` with the pre-commit hook's exclusion list, AND fix the em-dash threshold contradiction.** Two-file edit:
- Add to `voice-ben/SKILL.md` frontmatter `scope_excludes`: `working-notes/**`, `docs/repo_building/**`, `HANDOFF.md`, `HANDOVER.md`, `CLAUDE.md`, `manuscripts/Writing Samples/voice_*.md`. Generalise `docs/empirical_walkthrough_v1.md` → `docs/empirical_walkthrough_*`.
- Pick one em-dash threshold. Either set `THRESHOLD_PER_1K = 8` in `~/.claude/hooks/check-em-dashes.py` line 18 (matching YAML) and fix the warning-message text on line 71, OR tighten YAML to `<5` (matching hook). The hook's own message currently contradicts its own constant — that's the unambiguous fix.

**Effort: ~10 minutes. Fixes: convergent finding 5 + bonus em-dash threshold contradiction.**

---

## Raw persona reports

<details>
<summary>Spec-vs-Output Auditor</summary>

## Findings (ranked)

- **MAJOR — `general-purpose` agent is missing from `.claude/agents/` entirely, and the keep count is 10 not 11.** `ops_handover_council.md` line 79 lists `general-purpose.md | Utility (used by skills for ad-hoc tasks)` in the Keep set, and line 119 says *"a clean `.claude/agents/` directory with 11 files"*. Acceptance criterion line 273: *"`.claude/agents/` contains roughly 11 active agents (the *Keep set*)"*. The deployed directory contains only 10 files; `general-purpose.md` is in neither active nor archive. This matters because both `/council-critique` and `/council-ideate` dispatch `subagent_type: general-purpose`. If Claude Code's harness resolves `general-purpose` from a built-in registry this is fine in practice, but the spec called for a file-backed agent — silent execution drift.
- **MINOR — archive directory is `archive/` not `_archive/` as specified.** Phase 1 step 1: *"Create directory `.claude/agents/_archive/` if it doesn't exist."* Acceptance criterion line 272 says *"`.claude/agents/_archive/` exists"*. Deployed path: `.claude/agents/archive/`. The `_` prefix matters because `_archive` is a common convention for "skip in autoload".
- **MINOR — Phase 1's legacy `/council` coexistence decision was not logged.** Out-of-Scope point 4 instructed "Inspect first. If roughly equivalent, deprecate cleanly. Either way, do not silently overwrite." The legacy `/council` at `~/.claude/commands/council.md` was left untouched. Coexistence is defensible since it's user-level not project-level, but the handover asked for an explicit decision, and the session logs should record that decision.
- **MINOR — voice-audit discriminator test was not run.** Phase 2 line 301 (Notes and gotchas) explicitly required testing on `docs/empirical_walkthrough_v1.md` to verify discrimination. Only the paper draft test ran. Formal acceptance criterion (line 253) is met — but the calibration warning was ignored.
- **MINOR — MEMORY.md note exceeds the cumulative line cap.** Phase 1 line 280 said ≤5 lines; Phase 2 line 265 said ≤8 lines. Combined writes ~12 lines across 7 entries.

## Specific recommendations

- Restore `general-purpose` agent file or document its absence (one-line note in `docs/council_design.md` and the two council SKILLs acknowledging that `general-purpose` resolves to Claude Code's built-in agent and is intentionally not file-backed).
- `git mv .claude/agents/archive .claude/agents/_archive` and grep for any `agents/archive/` references before committing.
- Run `/voice-audit docs/empirical_walkthrough_v1.md --force` (after the `--force` flag is actually implemented per finding 4 elsewhere) and save to `quality_reports/voice_audits/2026-05-10_empirical_walkthrough_v1.md`.
- Add a one-line entry to `quality_reports/research_journal.md` for 2026-05-08 stating that the user-level `/council` was inspected and intentionally retained.

## What you don't know

- Did not deeply read the three session logs; the execution narrative may explicitly justify the `archive/` rename and `general-purpose` omission.
- Did not test whether `general-purpose` as a `subagent_type` actually resolves at runtime in this Claude Code build.
- Did not verify the test-artefact reports' substantive quality.

## Confidence

High on the spec-vs-deployed-file diffs (findings 1, 2, 4, 5). Medium on finding 3 (the legacy `/council` coexistence) because the handover language was ambiguous. What would change my mind: evidence in session logs that `general-purpose` was deliberately not file-backed; evidence the user explicitly approved `archive/`; a runtime test of `/council-ideate` succeeding.

</details>

<details>
<summary>Cross-artefact Coherence Critic</summary>

## Findings (ranked)

- **CRITICAL — Vocabulary contract /done ↔ /recall is incomplete.** /done's controlled vocabulary lists 17 topics; /recall's Topic-keyword associations only covers 11. Missing: `econometrics`, `data-discovery`, `thesis-design`, `robustness`, `ideation`, `admin`. Sessions tagged with these topics fall through to full-corpus fallback.
- **MAJOR — Scope contract voice-ben YAML ↔ pre-commit hook diverge in both directions.** The hook excludes paths NOT in YAML's scope_excludes (`working-notes/`, `docs/repo_building/`, `HANDOFF.md`, `HANDOVER.md`, `CLAUDE.md`, `voice_*` glob). Conversely, YAML names `docs/empirical_walkthrough_v1.md` as a single file but the hook generalises to `empirical_walkthrough_*`. The hook is more complete; YAML drifts. /voice-audit reads only YAML, so manual audit on `docs/repo_building/foo.md` won't abort.
- **MAJOR — Threshold contract: hook em-dash threshold ≠ YAML diagnostic_target.** Hook `THRESHOLD_PER_1K = 5`. YAML target `<8 per 1000 words`. Hook message says "voice-ben target: <5/1k" — internally contradicting itself.
- **MINOR — Lexicon ↔ voice-ben YAML have unsynced top-frequency anchors.** `voice_lexicon.md` top-30 includes `neoliberal` (27), `deliberative` (26), `populist` (13), `discursive` (13), `institutional` (15), `norm(s)` (10) — none appear in voice-ben's `distinctive_vocabulary`. Lexicon also adds negative-space items (`monolithic`, `totalising`, `dialectic`) that YAML lacks.
- **MINOR — Recall topic key for `paper-draft` is partial.** Keyword list doesn't include "paper" itself; queries like "what did the paper conclude" miss the pre-filter.

All other contracts pass: council-critique's five `subagent_type` references all exist as `.md` files; voice-audit's referenced YAML field names all exist in voice-ben; output paths exist; co-existence with user-level commands is documented.

## Specific recommendations

- Add 6 missing topic associations to `recall/SKILL.md` lines 41-52.
- Reconcile voice-ben `scope_excludes` (lines 420-429) with the hook's exclusion list. Bring YAML into line with hook.
- Pick one em-dash threshold. Either set hook to 8 (matching YAML) and fix line 71's warning text, OR tighten YAML to <5.
- Decide whether voice_lexicon.md and voice-ben YAML should be in lockstep or whether lexicon is intentionally a superset.

## What you don't know

- Whether the lexicon-vs-YAML divergence is intentional or accidental drift.
- Whether the user-level `/done` and `/council` commands actually defer to project skills via CWD precedence in current Claude Code behaviour.
- Whether `THRESHOLD_PER_1K = 5` in the hook is a deliberate tighter pre-publish gate.

## Confidence

High on the recall-vocabulary mismatch and the hook-threshold inconsistency. Medium-high on the scope-excludes divergence: divergence is real but intent (whether by design) requires user judgement. Agent-dispatch and output-path contracts confirmed: all five council agents and all six output directories exist exactly as referenced.

</details>

<details>
<summary>Future-User Usability Critic</summary>

## Findings (ranked)

- **MAJOR — `/done` description omits its most-likely natural-language triggers.** Description leads with "Project-level session capture" and lists destinations. Six-months-future-Ben says "wrap up", "log this session", "session done", "capture what we did" — none appear. Compounded: there are TWO `done` skills registered (project + user-level command), nothing in the description signals which fires when.
- **MAJOR — Three overlapping critique tools with no decision-tree disambiguation.** `/critique`, `/council-critique`, user-level `/council`, and `/retrospective` all match queries like "review this draft". `council-critique/SKILL.md` has a one-line disambiguation against user-level `/council` but nothing distinguishes it from simpler `/critique`. Cold-invocation six months out: user picks `/critique` for a paper that warrants the panel, or vice versa.
- **MAJOR — `/voice-audit` `--force` flag is documented but the harness will not pass it.** `voice-audit/SKILL.md` lines 37-39 instruct the user to invoke `/voice-audit <path> --force`. Slash-command argument parsing here is just positional path; no flag handler. When future-Ben tries `--force`, the skill will treat it as a second path (file-not-found) or ignore silently.
- **MINOR — `/done`'s 17-topic vocabulary is borderline; the "ask before adding" flow has friction risk.** 17 tags is at the upper end of reliable choice without consulting the list. The bigger issue: every session whose topic is genuinely novel triggers an interactive prompt mid-`/done`. For an end-of-session ritual, the prompt is one too many.
- **MINOR — `/recall`'s topic-keyword pre-filter is hard-coded and will drift.** When `/done` adds a topic, `/recall` won't know about it until manually edited.

## Specific recommendations

- Edit `done/SKILL.md` line 3 description to lead with trigger phrases. Suggested: "Capture an end-of-session summary: writes a session log, updates SESSION_REPORT and the active project STATUS, tags topics for later /recall. Use at session-end, when wrapping up, when the user says 'log this' or 'we're done for today'."
- Add a top-of-file "When to use which" block to `council-critique/SKILL.md` mapping: small/quick → /critique; full pre-submission → /council-critique; non-research → user-level /council; post-deployment audit → /retrospective.
- Fix the `--force` path in `voice-audit/SKILL.md`. Either implement argument-splitting OR drop the documentation.
- Make `/recall`'s topic-keyword table read-from-source: read controlled vocabulary from `done/SKILL.md` at runtime.

## What you don't know

- Whether the harness fuzzy-auto-triggers on description fields, or only literal slash-command invocation.
- Whether `/critique` is genuinely overlapping or solves a different task.
- How often `/done` has been invoked and how often the new-topic prompt has actually fired.

## Confidence

Medium-high on findings (1)–(3): description-vs-trigger fidelity, multi-tool disambiguation, and the broken `--force` are visible directly in artefact text. Lower on (4)–(5): both depend on usage patterns I haven't measured.

</details>

<details>
<summary>Missed-opportunities Reviewer</summary>

## Findings (ranked)

1. **MAJOR — No "skill ecology" README in `.claude/skills/`.** 22 skills exist; no map of when to reach for which. The boundary between `/critique` vs `/council-critique` vs `/review` vs `/retrospective` is genuinely confusing without one.
2. **MAJOR — Controlled vocabulary in `/done` was guessed, not corpus-derived.** The 17 topics were authored by inspection. The repo has months of session logs that could have been scanned to extract empirical topic distribution. 5 minutes of effort with 4-6 years of payoff.
3. **MAJOR — No cross-skill compositions where they'd help.** Three concrete misses: (a) `/done` doesn't detect when session touched `manuscripts/**` and offer to run `/voice-audit`; (b) `/recall` doesn't include `quality_reports/council_critiques/` or `quality_reports/voice_audits/` in its corpus; (c) `/voice-audit` has no integration with `/done`'s STATUS update.
4. **MAJOR — Gating gap: no commit-time hook for council-critique before submission.** Voice-audit gate exists in CLAUDE.md but council-critique doesn't. A 10-line patch in `.claude/settings.json` would close it.
5. **MINOR — Single-test validation only, no regression fixture.** Each skill tested exactly once. The post_handover_followups doc names this gap (G.1) but did not fill it.

## Specific recommendations

- Add `.claude/skills/README.md` — one-page table: skill → when-to-use → when-NOT-to-use → paired skill.
- Patch `recall/SKILL.md` Phase 1 corpus (lines 23-33) to include `quality_reports/council_critiques/*.md` and `quality_reports/voice_audits/*.md`.
- Derive the controlled vocabulary empirically. Run once: scan tag-like words across session logs and SESSION_REPORT, count frequencies, replace the guessed list. Document derivation date.
- Add "When NOT to use" subsection to `voice-audit/SKILL.md` and `council-critique/SKILL.md`.
- Add a regression fixture per skill at `.claude/skills/<name>/test_fixture.md`.
- Add the council-critique submission gate.

## What you don't know

- Whether `.claude/settings.json` already has gating hooks I haven't read.
- Whether existing user-level `/done` and project `/done` actually compose cleanly or produce duplicated entries.
- Whether test fixtures already exist somewhere I didn't grep.

## Confidence

High on findings 1, 2, and 3 — direct reads of skill bodies and handover specs. Medium-high on finding 4 because I'm inferring the absence of a council-critique gate from CLAUDE.md contents. Medium on finding 5 because the followups doc already names the gap (G.1). Recommendations are conservative 5-15 minute patches.

</details>
