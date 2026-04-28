---
name: notes-prose-gap
description: Diagnostic skill that catches a specific writing pattern of Ben's — where his working notes commit to stronger conclusions than his prose. Use when reviewing any drafted prose alongside MEMORY.md, STATUS files, or working notes. Triggered observation from 2026-04-25 session: MEMORY.md said "Accept as genuine asymmetry" while the paper rhetorically softened the asymmetry into a symmetric sorting frame.
disable-model-invocation: false
allowed-tools: ["Read", "Grep", "Edit"]
---

# Notes-Prose Gap Diagnostic

> A pattern this user has, that I should catch on his behalf because he doesn't always catch it himself.

## The pattern

Ben's working notes (MEMORY.md, STATUS files, marginal annotations, decisions logs) commit to claims that his published prose softens. The conclusions in the notes are firmer than the conclusions in the paper. The gap is invisible to him — it's a feature of how careful academic writers protect themselves at draft stage — but it weakens the work because the prose ends up making narrower claims than the analysis supports.

This was observed concretely on 2026-04-25. The MEMORY.md entry read:

> `[LEARN:writing] Redistribution (H2): RTI × Liberal = 0.011, p=0.285. Accept as genuine asymmetry.`

The paper at that point was framing the same finding as a "limitation" of single-item measurement, hedging on whether the asymmetry was real. The note had committed; the prose hadn't. The big-bet reframe in the session was, in part, an act of permission to write what the notes had already concluded.

## When this skill applies

Use whenever:
- A paper or section is being revised and there are accessible notes (MEMORY.md, STATUS, marginal annotations, decision logs)
- The user is considering whether to "soften" a claim in revision
- Drafted prose is being reviewed for theoretical commitment

This skill is not about adding new claims. It's about catching where the prose is hedging on claims the notes have already accepted.

## The diagnostic

### Step 1: Identify the load-bearing claims in the prose

For the section under review, list every empirical or theoretical claim that the argument depends on. For each, note the verb of commitment:
- Strong: "X causes Y", "X is the mechanism", "X explains the variance"
- Medium: "X is associated with Y", "X is part of what shapes Y", "X helps explain Y"
- Weak: "X may be related to Y", "X could plausibly..."
- Hedged-evasive: "Whether X relates to Y is an open question"

### Step 2: Search the notes for the same claims

Grep MEMORY.md, the relevant STATUS file, and any visible decision logs for the variable names, finding magnitudes, or theoretical concepts at play.

```bash
grep -i "asymmetr\|null\|finding\|reject\|accept" MEMORY.md
grep -i "decision\|conclude\|established\|confirmed" projects/*/STATUS.md
```

### Step 3: Compare commitment levels

For each load-bearing claim, ask:
- What level of commitment is in the prose?
- What level of commitment is in the notes?
- Are they the same?

A gap means the prose is hedging where the notes have committed.

### Step 4: Surface the gap to the user

Don't fix it silently. Surface it explicitly:

> "MEMORY.md says 'Accept as genuine asymmetry' — present prose hedges this as 'open question pending measurement work'. Two options: (a) commit prose to the position the notes hold, (b) update notes to match prose. Which is it?"

The user is the one who decides which direction to resolve the gap. The diagnostic just makes it visible.

## Why this matters

Three reasons:

1. **The work is weaker for the gap.** When the paper makes narrower claims than the analysis supports, the contribution looks smaller than it is. Reviewers reward strong-but-defensible claims.

2. **It's a sign that the writer's instinct knows the answer.** Hedging in drafts when the notes have committed is a self-protective instinct, not a calibration error. Catching the hedge gives the writer a chance to write what they actually believe.

3. **The pattern compounds.** A career of softening conclusions in prose produces a body of work that consistently undersells its findings. This is fixable in revision but only if the gap is named.

## When NOT to push for resolution

- The notes are themselves wrong or premature. (Notes can record provisional conclusions that don't survive scrutiny.)
- The hedging in prose is doing legitimate work — e.g., a methodological caveat that genuinely matters.
- The user has explicitly decided to hedge for strategic reasons (referee management, supervisor preference). Respect their judgment.

The diagnostic is for surfacing, not for forcing. The user retains authority over how to resolve.

## Anti-patterns

### Anti-pattern: Making the change without surfacing the gap
Don't silently strengthen the prose to match the notes. The user needs to see the gap to learn from it. Editing without naming defeats the diagnostic purpose.

### Anti-pattern: Strengthening the prose without checking the notes
Don't push the user toward stronger claims based on your own reading of the data. The diagnostic is "compare prose to user's own notes," not "Claude pushes for confidence."

### Anti-pattern: Treating every hedge as a gap
Some hedging is appropriate. The pattern of concern is specifically: confident note + hedged prose on the *same claim*. A hedge that exists in both notes and prose isn't the gap; it's calibration.

## Calibration data from this session

| Source | Claim about asymmetry |
|--------|----------------------|
| MEMORY.md `[LEARN:writing]` (April 2026) | "RTI × Liberal = 0.011, p=0.285. Accept as genuine asymmetry." |
| Strategic memo §"Decision committed" (later 2026-04-25) | "Big bet — adopted." Title locked at asymmetric framing. |
| Paper draft §VII (before big-bet reframe) | "The asymmetry between exclusion and solidarity findings deserves reflection. ... This may indicate genuine theoretical asymmetry: preventing the damage cascade may be more achievable..." |

The "may indicate" hedge in the prose is the gap. The notes had already accepted; the prose was still considering. Catching this and making the gap visible was the diagnostic move that triggered the big-bet reframe.

## Self-check before delivery

1. Did I read at least MEMORY.md and the relevant STATUS file?
2. Did I name specific gaps, not generic concerns?
3. Did I let the user decide direction, or did I prescribe?
4. Did I distinguish "hedge that should be removed" from "hedge that is methodological caveat"?
