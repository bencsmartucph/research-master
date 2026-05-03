# Econometrics from the Counterfactual Up

A progressive walkthrough that builds applied econometric fluency from the ground up,
using Ben's welfare-state paper (`manuscripts/paper_draft_v4_final.md`) as the running
example. Designed to be read one chapter per session, with exercises actually attempted.

The goal is not to "cover" topics. It is to build the habit of seeing a method, naming
its alternatives, articulating the trade-off, and being able to defend the choice in
plain English under adversarial pressure. The bar at the end is: Ben can sit across from
a methods referee and walk them through every choice in §V without flinching.

## How to use this

1. Read each chapter in order. Do not skip exercises; they are where the learning lives.
2. Reveal the answer toggles only after attempting.
3. The end-of-chapter check is a five-question recall. If you get fewer than four right,
   re-read the chapter before moving on.
4. Tell Claude what to sharpen before the next chapter.

## Companion resource

`docs/empirical_walkthrough_v1.md` is the consolidated defence document for the existing
paper — useful as a one-stop reference when prepping for a methods exam. This resource
is the build-up; that one is the consolidation. Both should be readable side by side.

## Structure

### Part I — The Counterfactual Question
1. Two classrooms: what causal inference actually is
2. The selection problem: why "comparing groups" usually lies to you
3. Conditional independence: what it would take for a comparison to be honest
4. From experiments to observational data: the bridge

### Part II — Regression as a Tool for Counterfactuals
5. What OLS is doing (the projection picture, not just the formula)
6. Controls, partial-out, and the FWL theorem (regression-as-matching)
7. Standard errors: what they actually measure, and why naive ones lie
8. Clustering: the moment regression's IID assumption breaks

### Part III — The Multilevel Move
9. When observations clump: country-waves, classrooms, hospitals
10. Random intercepts: letting baselines vary
11. Random slopes: letting effects vary
12. BLUPs and shrinkage: the gift and the price
13. Likelihood ratio tests: deciding whether the complexity earns its keep

### Part IV — Cross-Level Reasoning
14. The cross-level interaction: what β₃ asks
15. Identification with N=15 countries: where the leverage lives
16. The matched-sample move: trading power for argument
17. Jackknife and bootstrap: probing leverage at small N

### Part V — From Coefficients to Claims
18. Reading nulls as evidence (when you have a theory that predicts them)
19. The two-DV asymmetry: how independent failures triangulate
20. Attitudes vs behaviours: why they need different inferential frames
21. The killer-line catalogue: defending every §V choice in 30 seconds

### Part VI — The Within-Country Step (where you're going)
22. Difference-in-differences: the school-vs-school question with time
23. Event study: tracking the dynamic
24. Triple-difference: when the treatment varies along a third dimension
25. What your thesis design will and won't be able to claim

## Conventions

- **What's actually going on** boxes — moments where the math is doing something elegant; pause and look
- **Try this** prompts — short exercises woven through; don't read past them
- **Defend the choice** rehearsals — adversarial questions you should be able to answer in 30 seconds
- **Recall** at the end of each chapter — five questions, hidden answers in toggles
- **Connections** — pointers backwards (what this builds on) and forwards (what it enables)

## Status

| Chapter | Status |
|---------|--------|
| 01 — The counterfactual question | DRAFTED |
| 02 — The selection problem | pending |
| 03 — Conditional independence | pending |
| ... | pending |
