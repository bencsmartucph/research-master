# Voice Audit — `manuscripts/paper_draft_v4_final.md`

**Date:** 2026-05-08
**Voice-confidence score:** 68 / 100  (band: **Mixed** — substantial editing recommended)
**Word count:** 8,081

---

## Hard violations

### Em-dash apposition stacking (4 instances)

Per `voice-ben` rule `no_em_dash_apposition_stacking`. Each match deducts 5 points.

- **Line 113:** *"...solidarity requires supply-side construction — political entrepreneurship, coalitional framing, electoral system affordances — that welfare quality alone cannot provide."*
  Suggested rewrite: replace with parentheses or commas. *"...solidarity requires supply-side construction (political entrepreneurship, coalitional framing, electoral system affordances) that welfare quality alone cannot provide."*

- **Line 361:** *"...adding country-level GDP growth and post-fiscal Gini as macro controls — sourced from the Comparative Political Data Set over 2012–2018 — leaves the buffering coefficient essentially unchanged..."*
  Suggested rewrite: *"...adding country-level GDP growth and post-fiscal Gini as macro controls (sourced from the Comparative Political Data Set over 2012-2018) leaves the buffering coefficient essentially unchanged..."*

- **Line 383:** *"The redistribution asymmetry — clear exclusion effects, no detectable solidarity effects — is consistent across..."*
  Suggested rewrite: *"The redistribution asymmetry — clear exclusion effects against no detectable solidarity effects — is consistent across..."* (single em-dash, contrastive use). Or with a colon: *"The redistribution asymmetry is consistent across both ESS Model 5 and ISSP Model 5: clear exclusion effects, no detectable solidarity effects."*

- **Line 93:** Pattern detected; long line omitted from this report. Manual review recommended.

### Banned vocabulary

**0 hits.** Voice-ben pass already scrubbed `delve / underscore / bolster / harness / leverage / unpack / pivotal / groundbreaking / cutting-edge / transformative / game-changing / innovative / comprehensive / seamless / intricate / vibrant / multifaceted / holistic / testament` from the draft. Pass.

### Banned phrases

**0 hits.** Pass.

### Banned structures

**0 hits.** No "What X is, is Y", "Not just X — but Y", or related templates detected. Pass.

### Bold-term-explanation lists

**0 hits.** No `**Term:**` followed by explanation patterns detected. Pass.

---

## Soft signals

### Em-dash density

13 occurrences in 8,081 words = **1.6 per 1000** (target <8). **Comfortably under target.** The remaining em-dashes are likely doing legitimate cadence work (negation pivots, citation pauses) rather than default punctuation.

### Semicolon density

31 occurrences = **3.8 per 1000** (target 5-12). **Below target.** Ben's pre-AI register uses semicolons heavily for clause separation; under-3.8 suggests opportunities to restore some semicolons that the voice pass may have over-corrected to periods. Soft signal, -2 points.

### Required transition density

8 hits across `Indeed | Furthermore | Similarly | Through this perspective | Conceptually | Consequently | Effectively | Ultimately | undergirding | as purported by | Drawing on | Firstly / Secondly / Thirdly` in 8,081 words = **1.0 per 1000** (target ≥5). **WELL below target.** -10 points.

This is the dominant soft signal. The paper is light on Ben's signature transition vocabulary. Consider:
- Inserting `Indeed,` at 2-3 paragraph openers in §III and §V
- Using `undergirding much of...` once in the literature section
- Replacing one `In contrast,` with a `yet` mid-sentence pivot

Note: the audit's transition regex covers the high-frequency category most strictly; "yet" mid-sentence (frequent in Ben's pre-AI samples) is not counted in this pass. A future audit refinement could add `yet` mid-sentence as a softer signal.

### Categories absent entirely

- `signature_phrasing` (no `undergirding`, `as purported by` detected) — these are the highest-perplexity-breaking transitions and should appear at least once in any theory section.

---

## Diagnostic targets

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Em-dashes per 1000 words | <8 | 1.6 | OK |
| Semicolons per 1000 words | 5-12 | 3.8 | LOW (soft signal) |
| Banned words | 0 | 0 | OK |
| Bold-term lists | 0 | 0 | OK |
| Em-dash apposition stacking | 0 | 4 | VIOLATION |
| Ben transitions per 1000 words | ≥5 | 1.0 | LOW (soft signal) |
| `What X is, is Y` constructions | 0 | 0 | OK |
| Throat-clearing openers | 0 | 0 | OK |

---

## Score calculation

```
Start:                                         100
- 4 × em-dash apposition stacking (HARD):      -20
- semicolon density below range (SOFT):         -2
- transition density well below target (SOFT): -10
                                              ----
Voice-confidence score:                         68 / 100   (band: Mixed)
```

---

## Suggested next step

Apply the four em-dash apposition rewrites above (15 minutes; mechanical). Then add 4-6 Ben-signature transitions to lift density above 5/1000 — specifically one `undergirding much of...` somewhere in §III. After both, expected score: 88-92. The paper does not need restructuring; it needs targeted polish.

If GPT-Zero detector resistance is still a concern after this pass, anchor-paragraph retype protocol (open + close paragraphs typed from memory) is the next move per `voice-ben` `detection_resistance` notes.

---

*Generated by `/voice-audit` against the spec at `.claude/skills/voice-ben/SKILL.md` (frontmatter version dated 2026-05-08).*
