# Working with the Harness — Reference Guide

> Written 2026-05-01 after a session of stress-testing the harness. Captures the trust tiers, the agent inventory, the skill inventory, the hooks setup, and the anti-patterns surfaced during the session. Update when new agents/skills/hooks are added or when failure modes are discovered.

---

## Part 1 — The Trust Tier Framework

The harness has worker-critic pairs across many domains. They are not all equally trustworthy. The single most important question to ask before delegating any task is: **how complete is the rubric the critic uses?**

A rubric is a model of quality. The more checkable rules it contains, the more confidently the critic can substitute for human review. If most quality-relevant features are language-dependent, voice-dependent, or argument-dependent, the rubric is necessarily incomplete and the critic cannot close the loop alone.

### Tier 1 — Full autonomy (rubric is complete)

| Pair | Domain | Why the rubric is complete |
|------|--------|----------------------------|
| `coder` + `coder-critic` | Cleaning scripts, regression tables, plotting | Code either runs or doesn't. Numbers either match or don't. Standard errors either cluster correctly or don't. |
| `data-engineer` + `coder-critic` | Data pipelines, cleaning logic | Same as above. Reproducibility checks are mechanical. |
| `verifier` (submission mode) | Replication packages | AEA-style checklist with 6 categories, all rule-checkable. |
| `replication-auditor` | End-to-end replication | Same logic. |

**Rule:** Run the loop autonomously; require critic score ≥ 80 before merging. If <80, read both the artefact and the critique before deciding.

### Tier 2 — Supervised autonomy (rubric is mostly complete)

| Pair | Domain | What's mechanical | What needs you |
|------|--------|-------------------|----------------|
| `librarian` + `librarian-critic` | Lit notes, synthesis, INDEX updates | Citation accuracy, factual claims about papers, scope calibration | Strategic positioning, novelty claims, gap framing |
| `strategist` + `strategist-critic` | DiD assumptions, IV exclusion, RDD bandwidth | Econometric standards (parallel trends, first-stage F, manipulation tests) | Whether the strategy *fits* the substantive question |

**Rule:** Run the loop, but read the critique before applying any change that touches strategic positioning or interpretation. The librarian-critic's 78/100 today caught Wagner's sample-power caveat and three missing corpus papers — both surfaced via mechanical checks; both required your judgment to act on.

### Tier 3 — Critic as advisor only (rubric is voice/argument-dependent)

| Pair | Domain | Failure mode if used autonomously |
|------|--------|------------------------------------|
| `writer` + `writer-critic` | Generic academic prose | Strips voice features (anti-hedging rules misread "Indeed, X reconciles Y" type Ben-voice as hedging) |
| `writer` + `writer-critic-ben` | Ben prose specifically | Better calibration but should still gate at human adjudication for any HUMAN ADJUDICATE flag |
| `storyteller` + `storyteller-critic` | Beamer talks | Visual judgment; audience calibration |

**Rule:** Critic produces report; you read it; you decide what to apply. Never let the writer agent close this loop without reading what it changed. The voice-blindness demo on 2026-05-01 showed a single autonomous round erasing five distinct voice features from §III.D.

### Tier 4 — Manual (your hands on the keyboard)

| Domain | Why |
|--------|-----|
| Theoretical sections (§III, §IV in the seminar paper structure) | The argument's spine. AI co-writing is most insidious here because surface polish hides drift from your actual position. |
| Introduction's contribution paragraph | What's new is your judgment, not extractable from the data. |
| Conclusion / discussion | Where the paper says what it means. Most consequential per word. |
| MEMORY.md, STATUS.md updates | These are your operating system. Don't outsource them. |
| Voice samples themselves | The calibration corpus. Touching this with AI is recursive contamination. |

**Rule:** Type cold. Use Claude for grammar polish only. The "temp music" effect is real — AI prose under your name shapes future writing.

---

## Part 2 — Decision Rules

When you have a task, run through these in order:

### 1. Where in the trust tier does this sit?

If Tier 1 → dispatch the worker-critic pair, walk away, check at end.
If Tier 2 → dispatch the pair, schedule review time after.
If Tier 3 → dispatch the worker, supervise the critic loop, adjudicate.
If Tier 4 → don't dispatch. Open the file and write.

### 2. Is this a one-off task or a recurring pattern?

One-off → dispatch directly.
Recurring → consider whether it should be a slash command (skill) or an agent invocation. Skills are better when the prompt is reusable; agents are better when the work is investigative.

### 3. Is the artefact under your name?

If yes → assume Tier 3 minimum. Even empirics-heavy papers have voice in the abstract, intro, and discussion.
If no (replication notes, internal memos, code documentation) → Tier 1 or 2 depending on domain.

### 4. Is this overnight or attended work?

Overnight → require critic score ≥ 80 AND a verifier check on the run completion. The coder-critic's "wrong-machine silent exit" finding is exactly the failure that disappears in a wake-up summary.
Attended → standard worker-critic loop is fine.

---

## Part 3 — The Five Tips, Expanded

### Tip 1: Use `writer-critic-ben` whenever polishing prose, but never let it close the loop on theoretical sections

The agent loads `voice-ben/SKILL.md` and `Voice and Writing Style.txt` before scoring. It has a Preserve-on-sight list (epistemic positioning like "on my reading", aphoristic three-beat closers, "Not X but Y" constructions, distinctive transitions) and adds a Voice Loss deduction category for drift toward generic register.

**Standard workflow:**
1. You draft (or write a section by hand)
2. Dispatch `writer-critic-ben` to score
3. Read the report
4. Apply only the auto-fix subset (those marked AUTO-FIX) yourself
5. Adjudicate the rest (those marked HUMAN ADJUDICATE)

**Never** dispatch `writer` to revise based on `writer-critic-ben`'s output without you in the middle. The agent will dutifully apply HUMAN ADJUDICATE findings as if they were auto-fixes.

**Specifically reserve for human judgment:**
- Any flag on aphoristic structures (closers, paragraph capstones)
- "I argue / on my reading / I should note / I take this literally" findings
- Any suggestion to merge short declarative sentences into longer compound ones (rhythmic loss is invisible to the rubric)
- Citation density flags in theory-heavy sections (you quote more than most academic writers)

**Use `writer-critic` (the generic one) for:**
- Talk slides
- Replication notes
- Internal documentation
- Email drafts where voice doesn't matter

### Tip 2: Run the empirics + lit loops autonomously with a hard 80-threshold

Both pairs you can trust to detect what they detect. What they cannot detect is what their rubric doesn't cover.

**Hard rule:** No artefact merges if critic score < 80, regardless of how good it looks to you. The 78 on the librarian today was *very close* to passing despite catching a near-fatal positioning error. The threshold matters because critics can be wrong — but the asymmetric severity protects you. A false-positive deduction costs you ten minutes of reading; a false-negative pass costs you a referee response.

**For empirics specifically:** the coder-critic also gives an "overnight-safety verdict" if you ask for one. Treat that as separate from the score. A 95 with "UNSAFE FOR OVERNIGHT" beats an 85 with "SAFE-WITH-CAVEATS" for autonomous runs.

**For literature specifically:** the librarian-critic checks coverage, citation accuracy, theoretical framing, and gap identification. It does NOT check whether the synthesis advances *your specific* argument. That's your read.

### Tip 3: Overnight runs as orchestrated jobs, not as long single agents

A safe overnight pattern looks like:

```
1. You write a brief (the BRIEF.md — define question, scope, success criteria)
2. Orchestrator dispatches workers in parallel where independent
3. Critics dispatched after each worker completes
4. Verifier agent runs at end:
   - Confirms all critic scores ≥ 80
   - Confirms all expected output files exist
   - Confirms no agents exited with sys.exit(0) on a fatal branch
   - Writes wake-up summary to a single file
5. You read the wake-up summary first, then the artefacts that scored highest
```

**Critical:** the verifier must explicitly check for *unfinished work*, not just *completed work*. The coder-critic on 2026-05-01 noted that a wrong-machine run silently exits 0 and produces no figure — a wake-up summary that reports only on what *did* run will miss this entirely.

**Example prompt for the verifier:**
> "Check the run at `demos/overnight-pattern/`. For each expected output (BRIEF.md lists them), confirm the file exists and is non-empty. For each agent dispatched, confirm a critic ran on its output. List anything missing or any critic score < 80. Fail the run if any are missing."

**Don't run anything in Tier 3 or Tier 4 overnight.** Prose work is not safe for unattended autonomy.

### Tip 4: Fix the harness frictions when you encounter them

The two from the 2026-05-01 audit:

**Friction A: MCP server injecting "MUST cite with numbered references" into tool outputs.**
- Source: a cloud-level MCP server (Consensus or similar — visible in tool ID `e3e0d460-af3d-4896-83c2-1a2752e28303` from the system prompt). Not configured in local `.claude/`.
- Action: review your Claude Code on the web settings → MCP servers. If you don't actively use Consensus/PubMed search, remove it. Agents in this session correctly ignored the injection but a less-disciplined model wouldn't.
- Workaround if you can't remove: agents in your stack already handle this correctly (both demos). No code change needed if you're aware of the friction.

**Friction B: Cloud "do not write report files" rule conflicts with agent definitions saying "Save the Report."**
- Source: a cloud-level instruction (not in local config; not in CLAUDE.md). Possibly part of the web environment defaults.
- Local fix applied 2026-05-01: updated `writer-critic.md` and `writer-critic-ben.md` to instruct the agent to return reports inline if writing is blocked, and to include the intended save path so the parent agent can persist.
- Pending: do the same for `coder-critic.md`, `librarian-critic.md`, `strategist-critic.md`, `explorer-critic.md`, `storyteller-critic.md` if you want consistent behaviour.

**General pattern:** when an agent reports a conflict between its definition and a runtime rule, update the agent definition to acknowledge the conflict and degrade gracefully. Don't try to defeat the runtime rule; document the friction and adapt.

### Tip 5: Solo-writing days, scheduled

The "temp music" framing protects against fingerprint erosion. Implementation:

**Frequency:** at least every other week during the sprint. Ideally weekly.

**Constraint:** pick a section. Type it cold. No co-writing, no `voice-ben`, no `humanize-academic`. You can use Claude for grammar polish *after* you've completed the draft, but not during.

**Diagnostic:** compare what you produced solo to what you'd produce with the harness. The gap is your voice's actual baseline. If the gap is small, the harness is calibrated correctly. If it's growing, fingerprints are eroding faster than you're noticing.

**Bonus:** keep one channel that the AI never touches at all. A reading journal, a weekly memo to yourself, a daily 15-minute notes practice. When the harness drifts (and it will), this channel is your independent reference for what your actual thinking sounds like.

---

## Part 4 — Skills Reference

A skill is a slash-command-shaped reusable prompt. They live in `.claude/skills/[name]/SKILL.md`. Invoke via `/[name]` or by referencing the skill in a prompt.

### Project skills (live in this repo)

| Skill | Purpose | When to use |
|-------|---------|-------------|
| `voice-ben` | Write in Ben's authentic register | Before any prose that will appear under your name. Loads pre-AI samples + voice rules. |
| `humanize-academic` | Reduce AI-detection signal | After voice-ben if detector resistance matters. Honest about its limits. |
| `notes-prose-gap` | Catch hedging-vs-confidence mismatch | When prose under-claims what working notes have already concluded. Specific Ben pattern. |
| `quote-mosaic` | Theory section restructure | When a section needs 3-5 direct quotes with author commentary. AI-detector resistant by construction. |
| `read-paper` | Ingest new paper | PDF/docx/md → structured note + INDEX.md update |
| `resume` | Pick up project context | Replaces HANDOVER.md. Reads STATUS + git log + latest plan. |
| `critique` | Worker-critic in a box | Spawns subagent to review any output. Use when you want one-shot adversarial review. |

### User-level skills (live in `~/.claude/skills/`)

| Skill | Purpose |
|-------|---------|
| `init` | Initialize a new CLAUDE.md |
| `review` | Review a pull request |
| `security-review` | Security review of pending changes |
| `simplify` | Code review for reuse, quality, efficiency |
| `loop` | Recurring task on interval (e.g., poll status) |
| `claude-api` | Build Claude API apps |
| `keybindings-help` | Customize keyboard shortcuts |
| `update-config` | Configure Claude Code via settings.json |
| `fewer-permission-prompts` | Add allowlist for common bash/MCP tools |
| `session-start-hook` | Set up startup hook for Claude Code on the web |

### Plugin/feature skills (auto-loaded)

These come bundled and don't need explicit invocation. Documented for awareness:
- `notes-prose-gap` (also project-level — the diagnostic)
- `voice-ben` (project-level — voice production)

---

## Part 5 — Agents Reference

Agents are dispatched via the `Agent` tool with a specific `subagent_type`. Each runs in its own context window and returns a single message. Worker-critic pairs are the core pattern.

### Worker agents

| Agent | Domain | Output | Critic |
|-------|--------|--------|--------|
| `librarian` | Literature ingestion | Annotated notes, synthesis, INDEX updates | `librarian-critic` |
| `explorer` | Data discovery | Ranked data source list with feasibility grades | `explorer-critic` (alias: `surveyor`) |
| `data-engineer` | Data cleaning, wrangling, viz | Cleaning scripts, figures, documentation | `coder-critic` |
| `coder` | Analysis scripts | R/Stata/Python scripts producing tables/figures | `coder-critic` |
| `strategist` | Identification design | Strategy memo (estimand, estimator, assumptions, robustness) | `strategist-critic` (alias: `econometrician`) |
| `writer` | Paper sections | Draft text with humanizer pass | `writer-critic` or `writer-critic-ben` |
| `storyteller` | Beamer talks | Slide decks (4 formats: JM, seminar, short, lightning) | `storyteller-critic` (alias: `discussant`) |

### Critic agents

| Critic | What it checks | Score gate |
|--------|----------------|------------|
| `librarian-critic` | Coverage, citation accuracy, framing, gaps | ≥ 80 |
| `explorer-critic` / `surveyor` | Measurement validity, sample selection, identification fit | ≥ 80 |
| `coder-critic` / `debugger` / `r-reviewer` | 12 categories: code quality, reproducibility, strategic alignment | ≥ 80 |
| `strategist-critic` / `econometrician` | 4 phases: claim, design validity, inference, polish | ≥ 80 |
| `writer-critic` | 6 categories: structure, claims, identification, writing, grammar, compilation | ≥ 80 |
| `writer-critic-ben` | Same 6 + voice-aware modifications + Voice Loss category | ≥ 80 |
| `storyteller-critic` | Narrative flow, visual quality, content fidelity | ≥ 80 |
| `proofreader` | Manuscript polish (alias for writer-critic in some contexts) | ≥ 80 |
| `slide-auditor` | Visual layout for RevealJS/Beamer | Advisory |
| `tikz-reviewer` | TikZ diagrams (devil's advocate) | Iterative |

### Special-purpose agents

| Agent | Use |
|-------|-----|
| `orchestrator` | Phase transitions, dependency graph management, multi-pair dispatch |
| `verifier` | Compilation, execution, file integrity checks (standard mode); AEA replication audit (submission mode) |
| `editor` | Lit reviewer (Phase 1), paper critic (Phase 3), journal editor (Phase 4) |
| `referee` | Simulated blind peer review, 5 dimensions weighted |
| `domain-referee` / `methods-referee` | Specialized referees, dispatched independently |
| `replication-auditor` | End-to-end replication validation |
| `Explore` | Fast read-only search for code (less depth than `general-purpose`) |
| `Plan` | Software architect agent for implementation strategy |
| `general-purpose` | Catch-all for unscoped multi-step tasks |

### Domain-specialized review agents

| Agent | Use |
|-------|-----|
| `pedagogy-reviewer` | Holistic pedagogical review for slides |
| `domain-reviewer` | Substantive domain review for lectures |
| `quarto-critic` / `quarto-fixer` | RevealJS comparison vs Beamer benchmark |
| `beamer-translator` | Beamer LaTeX → Quarto RevealJS |

---

## Part 6 — Hooks Reference

Hooks are shell commands executed in response to Claude Code events. Configured in `.claude/settings.json` or `~/.claude/settings.json`.

### Active hooks observed in this session

**Stop hook:** `~/.claude/stop-hook-git-check.sh`
- Triggers when a session is about to end with untracked files
- Forces a commit-and-push before stopping
- Cannot be bypassed; the session enforces git hygiene
- **Implication:** any work you do creates a paper trail. Sandbox demos are best done in a `demos/` directory clearly marked as throwaway, with descriptive commit messages, so the trail stays organised.

### Hook patterns worth knowing

| Event | Common use |
|-------|------------|
| `PreToolUse` | Validate before risky operations (e.g., block `rm -rf` on production paths) |
| `PostToolUse` | Log tool usage; auto-format code; run tests after writes |
| `UserPromptSubmit` | Inject context (e.g., always-on git status) |
| `Stop` | Enforce commit hygiene (this session's setup); save session report |
| `SessionStart` | Pre-load project context; warm caches |

### Hooks for the overnight pattern

If you set up overnight runs, consider adding:

1. **PreCompact hook:** dump active todos, current plan, and MEMORY.md additions to disk before context compression. Survives the squeeze.
2. **Stop hook (already have):** the git-check ensures nothing is lost when a session times out.
3. **PostToolUse on Agent dispatches:** log each subagent invocation to `quality_reports/research_journal.md` automatically (currently this is manual per `logging.md`).

To add a hook, see `.claude/skills/update-config/` or run `/update-config`.

---

## Part 7 — Anti-Patterns

Documented from the 2026-05-01 session and earlier.

### Don't run an autonomous loop on Tier 3 or Tier 4 work
The voice-blindness demo showed five distinct fingerprints erased in a single round. Cumulative loss across many rounds is invisible from inside the loop.

### Don't trust a critic score in isolation
The librarian-critic's 78/100 was technically a REVISE recommendation but the issues it caught (Wagner sample-power, three missing corpus papers) were strategically much more serious than the score suggested. Always read the report, not just the number.

### Don't dispatch a worker without scheduling its critic
Per `agents.md`: every worker has a paired critic. The orchestrator's separation-of-powers rule exists for a reason. A creator scoring its own work has incentive to find only fixable issues.

### Don't conflate skills and agents
- Skills run inline in your main session (your context, your tools).
- Agents run in a fresh subagent context (their own window, their own tools).
- Use skills for reusable prompts; use agents for work that should be isolated from the main thread.

### Don't read large files in main context
Per `heavy-reads.md`:
- No PDFs / docx in main context — convert with pandoc or use `/read-paper`
- No files > 500 lines without a specific reason
- `metadata/data_dictionary.md` (2.8 MB) — grep, don't read
- `analysis/final_analysis_pipeline.py` (1,320 lines) — delegate summary to subagent
- Any `.dta` file — write a script with pyreadstat

### Don't commit demo-data to the seminar paper branch
Sandbox work (like the 2026-05-01 demos) belongs on a separate branch (`claude/ai-trends-analysis-xzncF`), not on the working seminar paper branch. Demos are reference material; they shouldn't pollute the paper's commit history.

### Don't outsource MEMORY.md or STATUS.md updates
These are your operating system. The persistent corrections in MEMORY.md are how Claude learns about your project across sessions. The next-step pointers in STATUS.md are how you resume after compression. Type these yourself — they're not large, and the cost of getting them wrong is high.

### Don't let critics close their own loops
Per the agents.md three-strikes rule: max 3 rounds per worker-critic pair before escalation. If a pair fails to converge in 3 rounds, escalate to user. Never iterate indefinitely; the convergence failure is itself information.

---

## Part 8 — Maintenance Checklist (Quarterly)

Every 3 months, walk through:

### Voice calibration
- [ ] Read three paragraphs of recent prose. Does it still sound like you?
- [ ] Run a paragraph through `voice-ben` and `writer-critic-ben`. Are the deductions reasonable?
- [ ] If voice-ben is over-correcting OR under-correcting, update the SKILL.md from current samples.

### Memory pruning
- [ ] MEMORY.md hard cap is 150 lines. Currently at ~80. When it grows past 130, prune superseded `[LEARN]` entries.
- [ ] Move stale entries to an archive file rather than deleting (provenance matters).

### Agent calibration
- [ ] Run a small task on each tier you actively use. Compare critic scores to your own assessment.
- [ ] If a critic is consistently too lenient or too strict, update its agent definition.

### Skill audit
- [ ] Skills accumulate. Some become unused. Archive what you haven't invoked in 3 months.
- [ ] If you've developed manual workflows that should be skills, formalise them.

### Hook review
- [ ] Are hooks still triggering for the right events?
- [ ] Have any new repetitive corrections emerged that should become hooks?

### Trust tier review
- [ ] Has any agent or skill graduated from one tier to another? (Better calibration → higher trust.)
- [ ] Has any artefact failed in a way that suggests the tier was too generous?

---

## Part 9 — Quick Reference Card

When in doubt:

| Question | Answer |
|----------|--------|
| Should I dispatch a worker-critic pair? | Yes for empirics, lit, replication, identification design. No for theoretical sections, intros, conclusions, voice samples. |
| Should I trust the critic's score alone? | Only for Tier 1 (empirics, replication). Otherwise read the report. |
| Should I run this overnight? | Tier 1 yes; Tier 2 yes with verifier; Tier 3 and Tier 4 no. |
| Should I let the writer agent revise after the critic? | If critic is `writer-critic-ben` and all findings are AUTO-FIX: yes. If any HUMAN ADJUDICATE: no. |
| Should I commit a demo? | Yes, on a separate branch. Never on the working paper branch. |
| Should I read the file in main context? | No if it's >500 lines or PDF/docx. Delegate or convert. |
| Should I update MEMORY.md / STATUS.md? | Yes, by hand, after every significant session. |
| Should I make it a skill? | If you've done it 3+ times the same way, yes. |
| Should I make it a hook? | If a correction is recurring across sessions, yes. |

---

## Appendix — File Map

```
.claude/
├── agents/
│   ├── orchestrator.md
│   ├── librarian.md / librarian-critic.md
│   ├── explorer.md / explorer-critic.md
│   ├── data-engineer.md
│   ├── coder.md / coder-critic.md
│   ├── strategist.md / strategist-critic.md
│   ├── writer.md / writer-critic.md / writer-critic-ben.md
│   ├── storyteller.md / storyteller-critic.md
│   └── verifier.md, referee.md, ...
├── skills/
│   ├── voice-ben/SKILL.md
│   ├── humanize-academic/SKILL.md
│   ├── notes-prose-gap/SKILL.md
│   ├── quote-mosaic/SKILL.md
│   ├── critique/SKILL.md
│   ├── read-paper/SKILL.md
│   └── resume/SKILL.md
├── rules/
│   ├── workflow.md, agents.md, quality.md
│   ├── domain-profile.md, journal-profiles.md
│   ├── revision.md, logging.md
│   ├── working-paper-format.md, figures.md, tables.md
│   ├── heavy-reads.md, meta-governance.md
└── settings.json (hooks live here)

CLAUDE.md          ← session primer, ~100 lines
MEMORY.md          ← persistent [LEARN] corrections, ~150 line cap
README.md          ← human overview

docs/
├── working_with_harness.md       ← THIS FILE
├── theory/                        ← 15 modules
├── literature/INDEX.md            ← 97 papers
├── A Mind in Formation...md       ← intellectual portrait
└── working_with_ben.md            ← collaboration theory

quality_reports/
├── plans/                         ← saved plans, dated
├── session_logs/                  ← per-session detail
├── merges/                        ← quality reports at merge time
└── research_journal.md            ← agent-level history (append-only)
```

---

*Last updated: 2026-05-01. Update when new agents/skills/hooks added or when failure modes are discovered.*
