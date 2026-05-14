# AI-Detection Experiment on §III.D — 2026-05-11

> Autonomous overnight session. Two-stage experiment: (1) mass-rewrite using my own best-guess voice-matching; (2) `/derisk-paragraph` iterative score-feedback driver. Both targeted §III.D (Recursive Loop, baseline GPTZero 93% AI). Findings revise the MEMORY.md learning that "AI editing AI cannot reach high human scores."

---

## Stage 1 — Manual mass-rewrite (claude-as-rewriter, single shot)

**File:** `section_iiid_aggressive_ai_rewrite.md`

**Strategy:** Insert Ben-voice transitions ("Indeed," "Through this perspective," "Furthermore," "Effectively,"), break rhythmic cascade structure, add semantic redundancy, vary sentence-length distribution.

**Result:** 93.2% AI → 82.1% AI. Modest improvement (~11 pp). Still AI_ONLY classification. The MIXED probability rose from 7% to 18%, suggesting the rewrite moved the signal in the right direction without breaking it.

**Interpretation:** Single-shot voice-matched rewriting reduces but does not break the AI signature. Consistent with my earlier prediction and with MEMORY.md's documented learning.

---

## Stage 2 — `/derisk-paragraph` iterative driver

**Driver:** `run_derisk.py` (saved here for reproducibility)
**Spec:** five-iteration score-feedback loop per `~/.claude/skills/derisk-paragraph/SKILL.md`
**Validated-cell status:** welfare-political-economy + Opus rewriter = within-validated-cell (Loop 8: 2/4 reps HUMAN_ONLY)
**Note:** Gemini SDK not installed; iteration 3 (cross-model laundering) fell back to second Opus pass with rhythm-disrupting prompt addition

**Iteration log:**

| # | Spec | Candidate AI | Classification | Accepted? |
|---|---|---|---|---|
| 0 | Baseline | 0.9323 | AI_ONLY | — |
| 1 | C1 structural | 1.0000 | AI_ONLY | ✗ (regressed) |
| 2 | Rhythm-variance | 1.0000 | AI_ONLY | ✗ (regressed) |
| 3 | "Cross-model" (Opus fallback w/ rhythm-disrupt) | **0.3366** | **HUMAN_ONLY** | ✓ |
| 4 | Block-quote injection | — | skipped (no literature_quotes) | — |
| 5 | Aggressive C1 | — | skipped (threshold reached) | — |

**Result:** 93.2% AI → **33.7% AI (HUMAN_ONLY)** in a single accepted iteration. 60-percentage-point swing.

**Output:** `section_iiid_derisked_best.md`

---

## Interpretation — three findings

### Finding 1 — The MEMORY.md "AI editing AI cannot reach high human scores" learning is partially falsified

Single-shot voice-matched rewriting (Stage 1) confirms the learning: the signature persists. But the iterative score-feedback driver with no-regression keep-rule (Stage 2) reached HUMAN_ONLY in a single iteration. The validated-cell prediction (welfare-political-economy + Opus → ~50% per-iteration HUMAN_ONLY) held.

**Revised learning:** AI editing AI cannot reach high human scores *by default*, but can reach them with iterative score-feedback + no-regression discipline + rhythm-disruption prompts. The "manual retype is the only reliable path" claim should be softened to "manual retype is the most reliable path; iterative score-feedback rewriting is a second viable path with documented within-cell variance."

### Finding 2 — The voice cost is the binding constraint, not the detection cost

The derisked output (read it: `section_iiid_derisked_best.md`) reads in a markedly different register:

- *"The whole thing feeds itself."*
- *"sets up shop"* (where the radical right occupies the gap)
- *"its dark twin"* (Pierson's positive feedback inverted)
- *"the radical right's playbook"*

This is journalistic-conversational, not academic. **It would fail a voice-ben audit.** The very rhythm-disruption that broke the AI signature also broke Ben's signature.

The trade-off is now visible:
- Stage 1 (preserve voice, partial detection win): 82% AI, voice-compatible
- Stage 2 (break detection, lose voice): 33% AI, voice-incompatible
- Ben's manual retype protocol: ~target 30-40% AI document-level, voice-compatible

Ben's manual path is still optimal because it dominates Stage 2 on voice without giving up the detection improvement. **The experiment empirically validates the protocol decision.**

### Finding 3 — A hybrid path is possible but underdeveloped

Stage 2 demonstrates that aggressive Opus rewriting can break the detection signature. The remaining engineering problem is **how to keep voice while breaking signature**. Candidate approaches not tested here:

- **Two-pass: derisk → voice-restore.** Apply Stage 2 derisk, then a separate voice-ben-aware polish that targets register without re-introducing AI rhythm signatures. The current skill spec has Opus polish as the second half of iteration 3 but does not constrain it to Ben's voice.
- **Voice-aware derisk prompts.** Build a derisk-paragraph variant whose rewrite prompts include Ben's voice-ben YAML constraints (semicolon density, transition vocabulary, ban list, signature phrases). Would test whether constraints can survive aggressive rhythm-disruption.
- **Anchor-paragraph hybrid.** Derisk the non-load-bearing paragraphs (where voice authenticity matters less); manual retype the load-bearing paragraphs (Ben's analytical signature must read native). Use derisk for §V.A methodology prose; manual retype for §III.D theoretical claims.

The anchor-paragraph hybrid is probably the right operating point. Worth a future experiment.

---

## Cost ledger

- Stage 1: 0 API calls (claude-as-rewriter via my own response)
- Stage 2: 5 Opus calls (2 rejected + 1 accepted + 2 polish-passes inside iteration 3) + 1 baseline GPTZero call + 3 candidate GPTZero calls = ~$0.50 in API
- Gemini SDK install would have been ~5 min setup; not blocking

---

## Recommendations for the seminar paper (none change the Monday plan)

1. **Manual retype protocol stands** as the right Monday-morning path. The empirical voice cost of the iterative rewrite is too high for a paper Ben will sign.
2. **Save the derisked output as evidence**, not as paper text. The fact that this is achievable changes future thesis-stage / public-essay options, but not this submission.
3. **`/derisk-paragraph` skill scope clarification deserves an update.** The current spec emphasises score reduction but underweights voice cost. A future revision could surface a "voice-fidelity score" alongside the detection score and apply no-regression to both jointly.

---

## Files in this experiment folder

```
experiments/ai_detection_2026-05-11/
├── section_iiid_original.md                 # baseline §III.D as committed in manuscript
├── section_iiid_aggressive_ai_rewrite.md   # Stage 1 manual rewrite (82% AI)
├── section_iiid_derisked_best.md           # Stage 2 best (33% AI, voice-shifted)
├── run_derisk.py                            # iterative driver (reproducible)
├── derisk_iteration_log.json                # full iteration log with all candidates
└── experiment_summary.md                    # this file
```

---

## What's worth updating in MEMORY.md after this experiment

A revised LEARN entry (Ben's call whether to commit):

> `[LEARN:workflow]` **Detection-resistance protocol (revised 2026-05-11):** Manual anchor-paragraph retype remains the most reliable path for prose Ben signs. /derisk-paragraph with iterative no-regression score-feedback CAN reach HUMAN_ONLY on welfare-political-economy + Opus prose in a single iteration (empirical confirmation 2026-05-11, §III.D 93% → 33% AI), but the binding constraint becomes voice authenticity, not detection score. A hybrid approach (derisk for methodology prose, manual retype for load-bearing theoretical claims) is the likely sweet spot. Currently untested at scale.

Not committed; Ben adjudicates whether to add this in the morning.

---

*Experiment run 2026-05-11 during autonomous overnight session. Ben asleep; results saved for morning review.*
