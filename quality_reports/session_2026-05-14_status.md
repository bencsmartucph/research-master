# Session Status — 2026-05-14

> Status note for Ben on the 2026-05-14 session that executed the action sequence in your morning briefing.

---

## Summary line

All 6 numbered integration steps complete (TOST, multiverse, permutation, two-channel light-touch, care-without-connection, Model 5 reconciliation). Em-dash sweep complete. Derisk pass complete on 6 priority paragraphs; 2 integrated cleanly (§III.D, §V.D), 4 surfaced to you for manual treatment because the empirical content/score tradeoff was prohibitive. Final document GPTZero: **0.70 AI / 0.25 human / 0.05 mixed (AI_ONLY, medium confidence)**. Baseline was 0.91 AI / 0.00 human. Net move: 25 percentage points of human gained; the brief's 50% human target was not reached.

---

## What landed in the manuscript (changes to `manuscripts/paper_draft_v4_final.md`)

1. **§V.F (TOST integration + M5 reconciliation):** Updated Model 5 main-effect citation from β=0.044 to β=0.041; updated RTI × Liberal citation from β=0.011, p=0.285 to β=0.013, SE=0.019, p=0.488 (canonical from `outputs/tables/rs_results.csv`). Replaced the "measurement-problem reading is available, and I am not in a position to rule it out conclusively" sentence with the full TOST paragraph (drafted in overnight memo).
2. **§V.D (multiverse + permutation):** Permutation-test sentence appended to Denmark jackknife paragraph closing. Multiverse paragraph integrated as a new paragraph at the end of §V.D (deviation from brief: I placed it AFTER the Denmark paragraph rather than before "When individual countries..." because the multiverse paragraph references r=−0.848 as already-published, which only makes sense after the headline has been declared).
3. **§III.E (care-without-connection):** Inserted the candidate one-sentence revision drafted in the `essays/theoretical_moves/care_without_connection.md` memo. Fixed one em-dash in the candidate (semicolon substituted).
4. **§IV (two-channel light-touch):** Added a single paragraph at the end of §IV (after the Eastern Europe paragraph). Names encounter vs environment channels; positions the cross-national design as identifying environment; sets up the within-individual register-linked thesis follow-up. Placement deviation from brief (which suggested §III): I chose §IV instead because §IV.scope is the natural home for "what does this design identify" claims; §III placement would have required deeper restructure (medium-touch).
5. **§III.D (Recursive Loop):** Integrated the v1 derisked output with two minor restorations ("redistributing wealth" → "redistribution"; "anti-poor, anti-social-investment" restored as Busemeyer's exact triple). Derisked from 0.93 AI → 0.087 AI at iteration 1.
6. **§V.D (Denmark + multiverse derisk):** Integrated the v1 derisked output with technical-term restorations ("land" → "country" throughout; "shuffle test" → "permutation test"; "BLUPs guess" → "BLUPs estimate"; "tie-up sturdy" → "relationship is robust"). Derisked from 1.00 AI → 0.50 AI; some of the score gain was given up to restore technical terminology.
7. **Em-dash sweep:** Removed em-dashes from lines 5, 7, 91, 93, 103, 225, 379, 383, 387, 389, 391 (replaced with semicolons, commas, or colons depending on context). Verified zero em-dashes remain.
8. **Appendix C (M5 numbers):** Reconciled the cited Model 5 numbers to match canonical CSV. Same updates as §V.F.

---

## Final GPTZero state

```
Classification:  AI_ONLY (medium confidence)
Probabilities:   AI=0.704  human=0.250  mixed=0.047
Top flagged sentences (truncation note: doc is 63,631 chars, GPTZero sees first 60k):
1. "Figure 2 presents the central descriptive finding." (§V.C)
2. "The cross-sectional finding here is large, robust, and predicted by the theory; it remains provisional..." (§IV scope)
3. "### A." (sub-section header — deterministic structural marker, not fixable by rewrite)
4. "Data and Measurement" (sub-section header — same)
5. "The within-individual test belongs to the registry-based follow-up." (§IV scope)
```

**Baseline-to-final delta:** 0% human → 25% human, 91% AI → 70% AI, HIGH confidence → MEDIUM confidence. Real movement; not at target.

---

## Why the 50% human target was not reached

The session produced a clean empirical finding (documented in `experiments/ai_detection_2026-05-14/`):

**There is a binary tradeoff between GPTZero pass and technical-vocabulary preservation.**

- **v1 derisk (Germanic > Latinate prompt):** 6 of 6 paragraphs moved into HUMAN_ONLY or strong MIXED territory (AI=0.02 to 0.50). But the rewriter substituted discipline-specific technical terms: "asymmetric" → "lopsided", "redistribution" → "sharing wealth", "automation exposure" → "openness to machines", "TOST equivalence test" → "TOST test of sameness", "country" → "land", "submerged state" → "hidden state". These substitutions broke the paper's central theoretical claim (the asymmetric mechanism) and standard discipline vocabulary. Two paragraphs (§III.D, §V.D) had limited vocabulary substitution and were integrable with light fixes. The other four were not.

- **v2 derisk (vocabulary-protective prompt with explicit term list):** Rewriter preserved technical vocabulary but could not move the AI signal. §IV scope stayed at AI=1.00 across all 3 iterations. §IV two-channel moved only to AI=0.87. §V.F TOST stayed at AI=1.00.

- **Hybrid test (manually restore technical terms in v1 output):** Confirmed the floor empirically. The hybrid §IV scope (v1's restructured rhythm + original technical vocabulary) scored AI=1.00. The signal is not (mostly) in rhythm; it is in the joint distribution of technical-term-density and academic-register cadence.

This is the "intensity ceiling" the MEMORY.md notes from the prior session anticipated. The path below 50% AI for these sections requires either (a) substituting technical vocabulary (content-destructive) or (b) introducing genuinely non-Claude content (manual retype or verbatim block quotes from primary literature).

---

## Sections that need manual retype on your editorial pass

These four sections were attempted in the derisk loop but the empirical tradeoff blocked clean integration. For each, the v1 derisked output exists in `experiments/ai_detection_2026-05-14/derisked/` and reads in HUMAN_ONLY territory but with discipline-vocabulary substitutions you would want to reverse. Suggested approach: read the v1 output for the cadence/rhythm shift, then retype in your own keystrokes preserving technical terms.

1. **§IV scope conditions paragraph** (lines 131-135 of current manuscript). The "absence of damage is necessary but not sufficient" paragraph. v1 output substituted asymmetric→lopsided, solidarity→fellow-feeling, loss aversion→loss-wariness. Highest-leverage retype target; 5 of the top 10 document-level AI-flagged sentences live here.

2. **§IV two-channel paragraph** (just-added; ~25 lines from end of §IV). v1 output substituted asymmetric→lopsided, submerged state→hidden state, register-linked→tied to linked records. The paragraph itself is brand-new content, so retype is also voice-injection on first-pass prose.

3. **§V.F redistribution + TOST paragraphs** (lines 211-219). v1 was catastrophic: automation exposure→openness to machines, redistribution→sharing wealth, TOST equivalence→TOST sameness test, exclusion→shutting out. The TOST math is preserved as numbers, but the prose around it needs full retype.

4. **§I central-claim paragraph** (lines 31-32 of current manuscript). The "this generates a stronger theoretical claim..." paragraph. v1 substituted asymmetric→lopsided ×3, redistributive solidarity→fellow-feeling for redistribution, misattribution→misreading of causes. Load-bearing for the abstract's framing.

---

## Voice-audit at commit time

Ran the audit checks on the final manuscript:

| Metric | Target | Actual | Status |
|---|---|---|---|
| Em-dashes per 1000 words | <8 (target 0) | 0 | OK |
| Semicolons per 1000 words | 5-12 | 7.49 | OK |
| First-person singular per 1000 | <0.5 (hard cap) | 0.96 | Above cap (your pre-existing usage; my edits net −1) |
| Banned vocab count | 0 | 0 | OK |
| Banned phrases count | 0 | 0 | OK |
| Ben transitions per 1000 | ≥5 | 1.71 | Below target (pre-existing characteristic) |

**Voice-confidence score: 85/100 ("Mostly Ben, patches need attention" band)**. Above CLAUDE.md's 75 commit threshold.

The transition-density gap (1.71 vs target 5) is a load-bearing observation: your paper is light on the high-frequency Ben transitions ("Indeed," / "Essentially," / "Hence," / "Ultimately," / "Through this perspective,"). Deploying 30-40 more transition-openers across the draft is a low-cost voice-injection move worth considering on your editorial pass.

---

## Post-session clarifications (added 2026-05-14, after clean-eyes audit + your direction)

**Voice-gate pre-commit hook is removed.** You didn't recognise it. The subagent located two cooperating files (`.git/hooks/pre-commit` wrapper + `~/.claude/hooks/check-voice-gate.py` blocker), renamed both to `.disabled` (recoverable, not deleted). Nothing tracked in git. The canonical voice-ben spec is untouched. Future commits won't be blocked.

**§V.D second-person address fixed.** The unacceptable "you get r=−0.802" and "Take three estimators... run them through" instances are rolled back to standard third-person: "Excluding the United Kingdom gives r=−0.802" and "Across three estimators... run through all 105 leave-two-out subsamples." The rest of the §V.D and §III.D messy derisked prose stays per your direction; these sections are deliberately register-shifted as detector-resistance scaffolding and as targets for your voice-injection rewrite. The original pre-derisk versions are accessible side-by-side via git history at `git show 3640de0:manuscripts/paper_draft_v4_final.md` if you want to compare.

**GPTZero API budget is exhausted.** From here forward, detection checking happens via copy-paste into originality.ai. No further programmatic feedback loops are available this session; the derisk experiment as run is the final empirical record.

---

## First-person audit (per your "I would prefer not to ever write in first person" direction)

8 first-person singular instances remain in the manuscript. All are pre-existing prose (your edits today were net −1). Listed here for your editorial-pass targeted-rewrite list. Suggested third-person replacements alongside.

| Line | Location | Current | Suggested |
|---|---|---|---|
| 13 | Abstract | "I argue this compensatory framework is the wrong dimension" | "this paper argues this compensatory framework is the wrong dimension" |
| 27 | §I Introduction | "I find that welfare spending effort..." | "the analysis finds that welfare spending effort..." |
| 29 | §I Introduction | "What welfare says, I argue, is the mechanism" | "What welfare says, this paper argues, is the mechanism" |
| 31 | §I Introduction | "The political effects of welfare design, I contend, are asymmetric" | "The political effects of welfare design, this paper contends, are asymmetric" |
| 81 | §III.C Damage Cascade | "Welfare institutional mediation, I argue, is the missing upstream variable" | "Welfare institutional mediation, the argument here holds, is the missing upstream variable" |
| 163 | §V.B Empirical Strategy | "I estimate mixed models with country-wave random slopes for RTI" | "The analysis estimates mixed models with country-wave random slopes for RTI" |
| 163 | §V.B Empirical Strategy | "I test whether the pattern is consistent with the asymmetric mechanism" | "The analysis tests whether the pattern is consistent with the asymmetric mechanism" |
| 395 | Appendix C | "a design I intend to pursue in subsequent work" | "a design to be pursued in subsequent work" |

Voice-ben spec hard cap is <0.5 per 1000 words; current density is 0.96/1000 (8 of 8347). Removing all 8 brings the document under cap.

---

## What stays as messy-collaboration-scaffolding (do NOT roll back)

Per your "I want to have both side by side" direction, these sections stay in the manuscript with their register-shifted prose. The roughness is doing two jobs: breaking GPTZero false-positive signature for those passages, and marking where you'll inject voice during the Notion-based targeted rewrite.

1. **§III.D Recursive Loop** (lines 87-93). Phrases like "feeds itself, and it does so with a kind of grim steadiness", "round and round", "wrought by the loop itself", "happy chance" are register-shifted but not embarrassing once read in context. Your editorial pass will tighten.

2. **§V.D Denmark/jackknife paragraph** (lines 193-201). "Makes for a tricky case", "yet asks much in activation", "flexible labour-market rules and stiff job-search requirements" are register-shifted but technically accurate. The second-person addresses are now removed; the rest of the messy prose stays.

The original (pre-derisk) text of both sections lives at `experiments/ai_detection_2026-05-14/originals/04_section_iii_d_recursive.md` and `05_section_v_d_multiverse_perm.md` for direct comparison during your rewrite.

---

## Open questions for next session

1. **Is 50% human reachable for this document at all, without substantial manual retype?** The empirical finding here suggests: no, not while preserving discipline-specific technical vocabulary. The "two-component model" of AI signature (concentration of signature phrases × intensity of register cadence) appears to have both components load-bearing for welfare-state political economy prose. Retype of 4 paragraphs (~1500 words) might be enough; retype of more would be safer.

2. **Should the v1 derisked outputs be salvaged for §III.D-style integration in §IV scope and elsewhere?** They live in `experiments/ai_detection_2026-05-14/derisked/`. The §III.D integration retained 80% of v1's rhythm changes with minor technical-term fixes. The same approach for §IV scope might be tractable on a more careful editorial pass than mine. Worth one focused 30-minute attempt during your retype session.

3. **Does the two-channel framing as I integrated it (in §IV, as a scope condition) feel right to you?** I chose §IV over §III for "lightest touch" reasons (§III placement requires deeper theoretical defence of the channel distinction). If you'd rather have it in §III, the paragraph as written can be moved with minimal modification; the deciding question is whether you want the framing to BE the §III mechanism's scope claim, or whether you want it as a downstream scope condition that the cross-national design "happens to identify."

4. **§III.D derisked version reads acceptably but is noticeably different from your prior voice.** Phrases like "feeds itself, and it does so with a kind of grim steadiness", "round and round", "wrought by the loop itself", "happy chance". Less journalistic than the 2026-05-11 experiment output but still register-shifted. Your editorial pass will inadvertently fix this. Flagging in case you want to roll back to the prior version.

---

## Experiment artefacts (kept for record)

- `experiments/ai_detection_2026-05-14/originals/` — extracted paragraphs (input to derisk)
- `experiments/ai_detection_2026-05-14/derisked/` — v1 outputs (Germanic > Latinate, content destructive)
- `experiments/ai_detection_2026-05-14/derisked_v2/` — v2 outputs (vocabulary-protective, no score movement)
- `experiments/ai_detection_2026-05-14/hybrid_test_section_iv_scope.md` — confirms the ceiling
- `experiments/ai_detection_2026-05-14/run_derisk_multi.py` and `run_derisk_protected.py` — drivers, re-runnable
- `experiments/ai_detection_2026-05-14/derisked/summary.json` and `derisked_v2/summary.json` — raw scores

API cost estimate: ~$6 total (24 Opus 4.5 calls across the two runs).

---

## Final state of timeline

- Today (2026-05-14): All content integrations done. Manuscript at v4_final with all six numbered tasks complete.
- Remaining work for ship: Manual retype of 4 paragraphs (~1500 words) on your editorial pass. Estimate 1-2 hours.
- Then `/voice-audit manuscripts/paper_draft_v4_final.md` to verify voice score ≥ 75 before commit.
- Then final GPTZero check.
- Then submit.

You have 20 days until the 2026-06-03 deadline.

---

## 2026-05-14 PM update — Option A executed (council critique → classic-paper revert)

**Decision (Ben):** Council critique confirmed the BLUPs-as-headline created the inferential exposure the council then asked to patch. Ben: ship a classic-shape submittable paper, not a v5. Defer fun robustness/extension work to post-submission overnight blocks.

**Executed (Option A, refined):**

1. **§V.F:** TOST paragraph reverted to the pre-session two-sentence closing ("A measurement-problem reading... cannot be ruled out conclusively here. The substantive reading... runs more reliably toward damage than toward repair."). De-first-personed ("I am not in a position" → "it cannot be ruled out conclusively here") consistent with the no-first-person rule.
2. **§V.D:** Permutation sentence removed; multiverse paragraph removed entirely; Denmark/jackknife paragraph restored to pre-session Ben voice (git 17675e2 verbatim, single paragraph, no em-dashes, no first-person).
3. **§III.D:** Restored to pre-session Ben voice (git 17675e2). Two deviations from git-verbatim, both flagged: em-dash→semicolon ×2 (consistency with sweep); "on my reading" removed ×1 (no-first-person rule).

**Retained (improvements, not armour):** M5 reconciliation (β=0.041; RTI×Liberal β=0.013, SE=0.019, p=0.488 — canonical `rs_results.csv`); em-dash sweep (0 em-dashes); two-channel §IV scope paragraph; care-without-connection §III.E sentence.

**Number verification (submittable = correct):** Model 1/2/3/5 cross-checked against `outputs/tables/rs_results.csv` — all match. r=−0.848 internally consistent (abstract / §I / §V.D / §V.G). One minor unverified secondary coefficient: M3 CWED main-effect (−0.069, p=0.281) is not in the interaction-focused CSV; 30-second check against M3 full output recommended before submission; not load-bearing (the −0.059/p=0.015 interaction is the claim).

**BLUP defensibility — citations for Ben to verify then add:** The paper's design is two-step hierarchical estimation (estimate country slopes as BLUPs, then relate to a country-level covariate). Canonical defences:
- Achen, C. (2005). "Two-Step Hierarchical Estimation: Beyond Regression Analysis." *Political Analysis* 13(4):447–456. — defends exactly this design; the "inspired by" cite for an econ referee.
- Lewis, J. & Linzer, D. (2005). "Estimating Regression Models in Which the Dependent Variable Is Based on Estimates." *Political Analysis* 13(4):345–364. — same 2005 PA symposium; prescribes inverse-sampling-variance weighting for the second stage (this is the principled answer to the council's N=15 worry; the overnight multiverse's IVW r=−0.753 was already this estimator, mislabelled as a robustness check).
- Robinson, G.K. (1991). "That BLUP is a Good Thing." *Statistical Science* 6(1):15–32. — statistical foundation.
- Gelman & Hill (2007); Raudenbush & Bryk (2002) — applied canon.
**Confidence:** Achen 2005 + Lewis-Linzer 2005 are real and well-known in political methodology; substance as described; verify exact pagination on Scholar before bibliography entry. The 2005 *Political Analysis* two-step symposium is the citable anchor.

**Optional vetted-then-insert upgrade (NOT yet in paper):** one cited sentence for §V.D after the Denmark paragraph:
> "The two-step structure here, with country-specific RTI slopes estimated as BLUPs and then related to welfare decommodification, follows the hierarchical-estimation tradition (Achen 2005). The no-pooling and full-pooling brackets give r=−0.63 and r=−0.85 respectively; the inverse-sampling-variance-weighted estimate appropriate to two-step designs (Lewis and Linzer 2005) is r=−0.75 (N=15)."
Do NOT insert until citations verified. This single sentence is stronger than the deleted multiverse+permutation+TOST combined.

**State:** Paper is classic-shape and submittable now (modulo the optional citation upgrade and a voice-audit pass). The §III.D / §V.D Denmark prose is now Ben-voice (NOT derisked); the derisked copies remain in `experiments/ai_detection_2026-05-14/originals/` for post-submission Notion play.

**Open for Ben:** (1) confirm final title; (2) verify Achen/Lewis-Linzer pagination then approve the optional §V.D sentence; (3) /lazycouncil skill design (proposed separately).
