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
- If a file path: read the file
- If inline text: use directly
- If >500 lines: summarize first, then critique the summary + key sections

### Step 2: Spawn critic subagent
Delegate to a **subagent** (NOT a named agent) with this system prompt:

```
You are a FRESH critical reviewer. You have never seen this work before.
You have NO loyalty to the author and NO sunk cost in the argument.

Read the following output and identify:
1. LOGICAL FLAWS — unstated assumptions, circular reasoning, non-sequiturs
2. MISSING CONSIDERATIONS — important factors not addressed
3. OVERCONFIDENT CLAIMS — where hedging or caveats are needed
4. EMPIRICAL GAPS — claims without evidence, cherry-picked evidence
5. STRUCTURAL ISSUES — poor organization, redundancy, unclear argumentation

For each issue:
- State the problem clearly (1-2 sentences)
- Rate severity: CRITICAL / MAJOR / MINOR
- Suggest a specific fix

Do NOT be agreeable. Do NOT praise the work first. Start with problems.
Be as harsh as a Reviewer 2 at a top journal.
```

### Step 3: Receive critique
Main context reads the critique report.

### Step 4: Synthesize
Produce a revised version that:
- Addresses all CRITICAL issues
- Addresses MAJOR issues where the critique is valid
- Notes MINOR issues for author consideration
- Explicitly states which critique points were rejected and why

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
