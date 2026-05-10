---
name: voice-audit
description: Deterministic check on prose against the voice-ben YAML spec. Scans for banned vocabulary, banned punctuation patterns, missing required transitions, and structural violations. Produces a structured audit report with hard violations, soft signals, suggested rewrites, and a voice-confidence score. Manual invocation only — does NOT auto-trigger and does NOT auto-rewrite.
---

# /voice-audit

**Usage:** `/voice-audit path/to/prose.md`

Reads the voice-ben spec from `.claude/skills/voice-ben/SKILL.md` (frontmatter only) and runs it as a mechanical check on the prose at the given path. Output is a structured report — never an edit.

This is a CHECK, not a REWRITE. Ben decides what to change.

---

## Phase 1 — Load the spec

Read `.claude/skills/voice-ben/SKILL.md`, parse the YAML frontmatter, and extract:

- `banned_vocabulary` (list)
- `banned_vocabulary_exceptions` (list — these override matches in `banned_vocabulary`)
- `banned_phrases` (list)
- `banned_structures` (list of regex-shaped patterns)
- `banned_punctuation` (object — em-dash rule, density target)
- `required_transitions` (categorised lists)
- `distinctive_vocabulary` (categorised lists; not enforced as required, but absence is a soft signal)
- `sentence_rules` (object)
- `structural_rules` (object)
- `diagnostic_targets` (object)

If the body of voice-ben.md is updated but the frontmatter isn't, this audit reads only the frontmatter — the user must keep the YAML canonical.

## Phase 2 — Verify scope

Check the target path against `scope_applies_to` and `scope_excludes` in the spec. If the path matches `scope_excludes` (e.g., `quality_reports/**`, `docs/learning_econometrics/**`, `MEMORY.md`), abort with:

> *"`<path>` is in voice-ben's `scope_excludes`. Voice-audit does not run on internal/tutor/infrastructure documents. If you want to audit anyway, override with `/voice-audit <path> --force`."*

The `--force` override exists for the rare case Ben wants to audit something out of scope (e.g., checking whether a tutor doc accidentally has Ben-voice patterns). It is opt-in only.

## Phase 3 — Hard violations: banned items

For each item, use `Grep -n -i` on the prose file. Apply exceptions.

**Banned vocabulary:**
For each item in `banned_vocabulary`, scan the file. Report every line + line number, except where the item is in `banned_vocabulary_exceptions` (e.g., `foster` always passes; `robust` passes when adjacent to "across specifications" / "to" / "estimator" / methodological context).

The `robust` exception logic: if the line contains "robust" AND any of `["specifications", "estimator", "to ", "across"]`, mark as METHODOLOGICAL (not a violation). Otherwise mark as violation.

**Banned phrases:**
For each multi-word phrase in `banned_phrases`, grep with literal-string matching (Ripgrep -F or quoted regex). Report line + line number per match.

**Banned structures:**
These are pattern-shaped, not literal. Build regexes:

- `"It's not just X — it's Y"` → `\bnot just .+? — it'?s\b` (and the no-em-dash variant: `\bnot just .+?,?\s+it'?s\b`)
- `"Not only X, but Y"` → `\bNot only .+?, but\b`
- `"This isn't about X. It's about Y"` → `\bThis isn'?t about .+?\.\s+It'?s about\b`
- `"What X is, is Y"` → `\bWhat .+? is,? is\b`
- `"X is fundamentally Y"` → `\bis fundamentally\b`
- `"What makes X X is Y"` → `\bWhat makes .+? .+? is\b`

Report line + line number per match. Use multiline grep where the pattern can span lines (the "This isn't... It's..." form often does).

## Phase 4 — Punctuation density

Compute against the document:

**Em-dashes (`—` U+2014, also `--`):**
- Count occurrences via `Grep -c '—|--'` on the file.
- Compute words ≈ `wc -w` minus tokens that are clearly not prose words (URLs, citations, table cells). For an MVP estimate, use raw word count.
- Compute em-dashes per 1000 words. Compare to `diagnostic_targets.em_dashes_per_1000_words` (target: <8).
- If above target, flag as a HARD violation. List the lines.

**Em-dash apposition stacking** (the `— X — pattern`):
- Search for two em-dashes in the same sentence: `—[^.!?\n—]{1,80}—`.
- Each match is a HARD violation per `sentence_rules.no_em_dash_apposition_stacking`.

**Semicolons:**
- Count and compute per-1000. Compare to `5-12` target.
- Below 5: SOFT signal (not enough Ben-voice rhythm). Above 12: usually fine; flag if extreme.

**Mid-sentence colons:**
- Count `: ` mid-sentence. Compare to `<8 per 1000`. Above target: SOFT signal.

## Phase 5 — Soft signals: required transitions

Count occurrences across all categories in `required_transitions` (high_frequency, citation_framings, argument_pivots, signature_phrasing, enumeration). Compute per-1000-words density. Compare to `diagnostic_targets.ben_transitions_per_1000_words: ">=5"`.

If density < 5 per 1000 words: SOFT signal "Low Ben-transition density — prose may not sound like Ben." List which categories were absent entirely.

If density 0 across all categories: this is a stronger signal — flag as HARD with note "No required transitions used; very unlikely this is Ben's voice."

## Phase 6 — Structural checks (best-effort)

Where mechanical detection is possible:

- **Bold-term-explanation lists** (`**Term:**` followed by explanation): grep for `^\*\*[A-Z][^\*]{2,30}:\*\*\s+\w`. Each match is HARD ("#1 AI tell" per the spec).
- **Throat-clearing openers** (sentence starts with hedge): grep for `^(It is interesting to note that|It should be mentioned that|It is worth pointing out that)\b`. HARD.
- **Definitional template** (`What X is, is Y`): caught in Phase 3 banned_structures.
- **Question restatement** (rhetorical "What is X?" sentence followed by "X is..."): heuristic, hard to do mechanically. SOFT-signal-only: count `^(What|How|Why) [^.!?]{3,80}\?\s*\n[A-Z]` — list as candidates for review.
- **Grand opening world-state** (first sentence contains "In today's", "In a world where", "In an era of"): HARD.

## Phase 7 — Voice-confidence score

Compute coarse score 0–100:

```
start at 100
for each HARD violation:        deduct 5 points
for each em-dash above target:  deduct 1 point per excess em-dash
for each SOFT signal:           deduct 2 points
for transition density < 3:     deduct 10 points (large penalty)
floor at 0
```

Banding:
- **90-100:** Highly consistent with Ben's voice. Ship.
- **70-89:** Mostly Ben, with patches that need attention.
- **50-69:** Mixed — substantial editing or anchor-paragraph retyping recommended.
- **0-49:** Almost certainly not Ben's voice — restructure rather than edit.

## Phase 8 — Output report

Print to chat (and optionally save to `quality_reports/voice_audits/YYYY-MM-DD_<artefact-stem>.md` if the prose is a paper draft):

```
## Voice Audit — <path>

**Voice-confidence score:** NN / 100  (band: <Highly consistent / Mostly Ben / Mixed / Not Ben>)

### Hard violations (banned items, structural patterns)

[For each violation, include: rule name, line number, the offending text, suggested rewrite where possible.]

- **Banned vocabulary: `delve`** at line 42:
  > "we delve into the welfare regime variation"
  Suggested rewrite: drop "delve into"; replace with "examine" or restructure.

- **Em-dash apposition stacking** at line 117:
  > "Welfare design — the institutional architecture of decommodification — shapes..."
  Suggested rewrite: use commas or parentheses for the apposition.

- **Bold-term-explanation list** at line 203:
  > **Stigma:** the felt experience of receipt
  Suggested rewrite: convert to inline prose ("Firstly, stigma — the felt experience of receipt — does X").

### Soft signals (density, frequency)

- Em-dashes: 14 occurrences in ~2,300 words = 6.1 per 1000 (under target)
- Semicolons: 22 in ~2,300 words = 9.6 per 1000 (within range — good)
- Required Ben transitions: 4 in ~2,300 words = 1.7 per 1000 (BELOW target of >=5; this is a soft signal)
- Categories absent: signature_phrasing (no `undergirding`, `as purported by`)

### Diagnostic targets

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Em-dashes per 1000 words | <8 | 6.1 | OK |
| Semicolons per 1000 words | 5-12 | 9.6 | OK |
| Banned words | 0 | 1 | VIOLATION |
| Bold-term lists | 0 | 1 | VIOLATION |
| Ben transitions per 1000 words | >=5 | 1.7 | LOW |

### Suggested next step

[One sentence — usually one of: "Apply the rewrites above"; "Restructure rather than edit if score < 50"; "Run anchor-paragraph retype protocol if detector resistance matters and score is 50-70".]
```

---

## Implementation rules

- **Voice-audit is a CHECK, not a REWRITE.** Hard rule. Never auto-edit.
- **The frontmatter is canonical.** When Ben updates a banned word, he updates the YAML in `voice-ben/SKILL.md`; the audit reads from there. Body is rationale, not enforcement.
- **Don't trigger automatically.** Manual invocation only — never on tutor docs, internal memos, code, or session logs.
- **Honour `scope_excludes`.** If the path matches an exclusion pattern, refuse cleanly with the `--force` opt-in.
- **No fabricated rewrites.** If the audit can't suggest a meaningful rewrite, say "no automatic rewrite available — restructure manually."
- **Cite line numbers every time.** Every violation has a line number; every soft signal has a count + density.

---

## What this skill is *not*

- **Not a rewriter.** Hard rule. Voice-audit is a checker.
- **Not auto-triggered.** Manual only. The user invokes `/voice-audit <path>` when they want a check.
- **Not a substitute for `voice-ben`.** That skill informs *writing*; this skill *checks* finished prose.
- **Not a substitute for `humanize-academic`.** That skill targets detector-resistance specifically (anchor retype protocol, perplexity-breaking moves). Voice-audit checks adherence to Ben's voice rules; humanize-academic is the next layer when detector resistance specifically matters.
- **Not a moralist.** It reports patterns; the user decides whether each is a problem in context.
