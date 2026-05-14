# Memo for Council Review — v3→v4 Comparison Verdict + Current Plan

**Date:** 2026-05-08
**Purpose:** Anchor artefact for `/council-critique`. The council should evaluate (a) the v3 → v4 verdict below, (b) the implemented refinement plan, and (c) where the v4 paper is most exposed.
**Paper under discussion:** `manuscripts/paper_draft_v4_final.md` (post-refinement, includes new §III.D recursive loop, §I twofold claim, §III.A forward-reference, §III.F numbered predictions P1–P5, §V.D BLUPs jackknife sentence)
**Background context:** `explorations/session3_findings_2026-05-04.md`; `manuscripts/Archive/paper_draft_v3_final.md` (sorting-mechanism framing, pre-asymmetric reframe).

---

## 1. What I claimed about v3 → v4

After diffing v3 (sorting-mechanism framing, 6,090 words, pre-voice-pass, last meaningful work Apr 18) against v4 (asymmetric framing, ~7,800 words, post-three-voice-passes, last work May 1), my verdict was:

**v4 is more sophisticated than v3, not less.** The user's worry that voice passes stripped sophistication does not survive comparison of the actual documents.

The v3 → v4 transition conflates two distinct changes:
1. **The Apr 25 asymmetric reframe** — a substantive theoretical commitment shift from symmetric sorting (welfare moderates both directions) to asymmetric mechanism (welfare can damage but cannot symmetrically protect).
2. **Three voice passes** (Apr 26–27): em-dash purge (81 → 0), aggressive trim (7186 → 5501 words; though v4 grew back to ~7,800), and quote-mosaic intro restructuring.

### Sophistication gains in v4 that did not exist in v3

- **§III.B "Why Welfare, and Not Something Else"** — entirely new argument; pre-empts the "many institutions shape identity" objection by eliminating courts, markets, religion as alternatives.
- **§III.D / §III.E split (post-refinement)** — recursive loop and identity-investment irreversibility now separated.
- **§III.E "Why the Mirror Image Does Not Exist"** — three structural reasons for asymmetry (loss aversion, status positionality, identity-investment irreversibility). Not in v3.
- **§III.F "What the Asymmetric Theory Predicts"** — explicit Popperian falsifiability section, now with five numbered predictions (P1–P5).
- **§V.D BLUPs methodological disclosure** — explicit contrast of bivariate per-country OLS (r=−0.625) vs random-slopes BLUP estimate (r=−0.848). Plus the new 105-pair two-country jackknife.
- **§II Burgoon & Schakel engagement** — resolves apparent contradiction between supply-side (party platforms) and demand-side (individual attitudes).

### Where v3 was tighter (pre-refinement v4)

- Recursive loop was its own §IV; analytical force lost when absorbed into §III.D paragraph 3. **Restored in current §III.D.**
- Implementation/visibility two-channel framing was clearer.
- Limitations paragraph was more thorough.

### Voice pass effect, isolated

Additive, not subtractive. Em-dashes removed (now relaxed back to <8 per 1000 words for selective use). Ben tics layered in. Aphoristic closings added ("permission, not propulsion"; "Three asymmetries, none with a mirror image"). Sentence length increased; sophistication preserved at the sentence level.

### Bottom-line verdict

v4 is bolder, sharper, more falsifiable, more committed. The risk in v4 is overcommitment — a referee could argue the asymmetric reframe is post-hoc rationalization of a null finding, with §III.E's three-pillar defence (loss aversion, positionality, irreversibility) recruited specifically to absorb a measurement issue on the redistribution side.

---

## 2. The implemented refinement plan (today)

Triggered by user concerns about voice-pass sophistication loss + Amalie's seminar feedback ("no more analysis, hone argument or sign-post hypothesis") + Ben's desire to ship quickly.

| # | Edit | Section | Status |
|---|---|---|---|
| 1 | Recursive loop split into standalone §III.D | §III.C–F | Applied |
| 2 | Cross-references updated | §IV, §V.F | Applied |
| 3 | Voice-ben skill relaxed (em-dash target 0 → <8/1000) | `.claude/skills/voice-ben/SKILL.md` | Applied |
| 4 | BLUPs jackknife sentence | §V.D last paragraph | Applied |
| 5 | Central hypothesis sign-post | §I | Applied |
| 6 | Forward-reference to §V.D / §V.F | §III.A | Applied |
| 7 | Predictions numbered (P1–P5) | §III.F | Applied |

## 3. Outstanding decisions (not yet executed)

- **Drop Appendix D entirely.** Session3 regional sanity check shows NUTS-2 falsification would null (Pearson r=+0.15, p=0.66; 7 of 12 within-country correlations *negative*, indicating ecological-vs-individual divergence). Saves 1–2 weeks. Open: write a deferral sentence in §V.G, or silent?
- **Close audit Claim 14** (admin in `audit_and_review_2026-05-04.md`).
- **Sub-components paragraph for §V.D** (session3 §4.1, ~150 words). Pension null clean, UE ≈ SK indistinguishable. Conservative framing. Borderline given "no more analysis" instruction.

---

## 4. What the council should evaluate

1. **Is the v3 → v4 verdict defensible?** Did I miss a way in which v4 *did* lose sophistication?
2. **Is the current plan adequate to ship?** Or is there a load-bearing problem the plan doesn't address?
3. **Where is the v4 paper most exposed?** What's the strongest attack a referee at a top journal (target tier: AJPS, CPS, EJPR) would make?
4. **What's the *new* claim that earns this paper its space?** Stripping the lit review back to nothing, is there a single sharp claim that survives?

The user wants to ship the paper quickly to focus on other studies. Council recommendations should be calibrated to that constraint: top 3–5 issues only, with effort estimates. No 20-item laundry lists.
