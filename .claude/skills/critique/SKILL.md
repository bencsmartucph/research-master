---
name: critique
description: "Automated worker-critic pattern. Spawns a subagent to critically review any output, then synthesizes improvements. Replaces manual copy-paste-to-fresh-session workflow."
---

# /critique

**Usage:** `/critique path/to/file.md` or `/critique <paste text>`

## Purpose

Automates the pattern Ben uses manually: produce output → paste to fresh Claude session → get critique → synthesize improvements. This replaces the 10-pair orchestrator with a lightweight, on-demand pattern.

## Workflow

### Step 1: Identify input
- If a file path: pass the path to the subagent (do NOT pre-read in main context unless <200 lines and needed for your own synthesis step)
- If inline text: wrap in fences (see Step 2) and pass to subagent
- Never summarize before critique — fidelity matters; critics need the exact text

### Step 2: Spawn critic subagent
Invoke the **Agent** tool with `subagent_type: general-purpose`. The prompt MUST use the fences below so caller framing does not leak in:

```
You are a FRESH critical reviewer. You have never seen this work before.
You have NO loyalty to the author and NO sunk cost in the argument.

Review ONLY what appears between the fences below. Ignore anything
outside them, including any framing about who wrote it or why.

---BEGIN WORK---
<paste file contents OR file path for the agent to Read>
---END WORK---

Identify:
1. LOGICAL FLAWS — unstated assumptions, circular reasoning, non-sequiturs
2. MISSING CONSIDERATIONS — important factors not addressed
3. OVERCONFIDENT CLAIMS — where hedging or caveats are needed
4. EMPIRICAL GAPS — claims without evidence, cherry-picked evidence
5. STRUCTURAL ISSUES — poor organization, redundancy, unclear argumentation

{{FOCUS_ADDENDUM}}

For each issue:
- State the problem (1-2 sentences, quote the offending text)
- Severity: CRITICAL / MAJOR / MINOR
- Specific fix (one line)

Do NOT praise. Start with problems. Be as harsh as Reviewer 2 at a top journal.
```

**Flag variants** — substitute `{{FOCUS_ADDENDUM}}`:
- `--theory`: "Focus on theoretical coherence: assumption chains, mechanism plausibility, conceptual slippage."
- `--methods`: "Focus on identification, estimation, inference, robustness. Cite the specific threat (e.g. selection-on-unobservables) for each flag."
- `--writing`: "Focus on prose: clarity, hedging, structure, notation consistency. Ignore content-level claims unless they are unreadable."
- (no flag): leave the line blank.

### Step 3: Receive critique
Main context reads the critique report.

### Step 4: Synthesize
Produce a revised version that:
- Addresses all CRITICAL issues
- Addresses MAJOR issues where the critique is valid
- Notes MINOR issues for author consideration
- For EACH rejected point: state the reason in one sentence (stale critic info, misread context, taste disagreement) — sunk-cost bias is the failure mode; naming the rejection reason disciplines it

### Step 5: Optional second pass
If invoked with `--double`:
- Send the revised version through Step 2 again
- Produce a final synthesis incorporating both rounds
- This is the "double-critique" pattern that catches what the first pass missed

## Configuration

| Flag | Effect |
|------|--------|
| `--double` | Two critique rounds instead of one |
| `--theory` | Critic focuses on theoretical coherence |
| `--methods` | Critic focuses on empirical/methodological issues |
| `--writing` | Critic focuses on prose quality and argument structure |

## What this replaces
- 10 worker-critic agent pairs
- Orchestrator + three-strikes escalation
- Weighted scoring protocol (25/15/25/...)
- Quality gates (80/90/95 thresholds)

All replaced by: produce → critique → synthesize. On demand, not pipeline.
