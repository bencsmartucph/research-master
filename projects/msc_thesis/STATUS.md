# MSc Thesis — STATUS

> **NEXT:** Ship the seminar paper first (Monday May 11 polish pass; see `projects/seminar_paper/STATUS.md`). Thesis topic locks in late summer; scoop scan due Aug 1 (Todoist 6gcPG6wFFF93Mx6X). Per `CLAUDE.md` Project Context, the thesis is the Y1 paper of the five-year arc — NOT a PhD chapter.

## Stage

**Not yet started.** Autumn 2026 → spring 2027. Seminar paper finalises first. Topic flexibility noted, but the Danish-register design is the front-runner given existing CEBI employment grants register access without fresh Forskerservice authorisation.

## Timeline (corrected 2026-05-10)

- **Now → late May 2026:** finish seminar paper
- **June – July 2026:** rest period, scoop scan for thesis topic (Todoist due Aug 1)
- **August 2026 → June 2027:** MSc thesis (autumn semester writing + spring semester defense)
- **Autumn 2026 – January 2027:** PhD applications (parallel; see Applications Studio in Notion + Todoist)
- **Fall 2027:** PhD start (target Copenhagen / EU first; London / Berkeley / NYC / Sydney secondary)

**Implication:** register access for the thesis is via current CEBI employment. Fresh Forskerservice authorisation belongs in 2027 PhD-stage planning, NOT now. The two Todoist tasks predicated on "PhD now" (May-31 CEBI email, Sep-30 Forskerservice deadline) were deleted 2026-05-10.

## Theoretical anchor (post-big-bet)

The seminar paper commits to an asymmetric mechanism: welfare design's political effects are damage-cumulative and not symmetrically reversible. The thesis tests two distinct predictions this generates:

**Prediction 1 (positive):** Conditionality-introducing welfare reforms in countries with previously dignity-preserving regimes should produce *new* damage signatures — elevated RTI→exclusion slopes, attitudinal path-dependence at the individual level. **Detectable.**

**Prediction 2 (null):** Decommodification-expanding reforms in countries with previously stigmatising regimes should produce *weaker or null* mirror-image protective signatures. Active solidarity uplift should not be detectable in the same data.

The asymmetric theory is testable in a way the symmetric theory is not. The thesis design should be evaluated against its ability to deliver evidence on both predictions, not just on whether welfare reform shifts attitudes generically.

## Council ideation roadmap (2026-05-08)

See `quality_reports/council_ideations/2026-05-08_extend_asymmetric_welfare_danish_registry.md` for the full three-persona generative council output. The synthesis maps a **five-year arc** where the thesis is Y1:

- **Y1 (MSc thesis — this design):** within-Denmark mass-layoff DiD around the 2010 dagpengereform; Statistics Denmark register linkage to political outcomes (Folketing electoral register); RTI-heterogeneous response. Aim: reduced-form within-individual analogue of the seminar paper's cross-national moderation. Targets AJPS, AEJ:Applied.
- **Y2 (PhD year 1):** mechanism-replication paper extending Y1's setup. Tests Prediction 1 directly via path-dependence.
- **Y3 (PhD year 2):** mechanism-interrogation paper distinguishing stigma vs contribution-history vs economic-exposure as competing mediators. Combines survey-experimental module (Stantcheva-style elicitation, van Oorschot deservingness battery) with register linkage on lifetime tax history (SKAT) and benefit-form history (DREAM).
- **Y4 (PhD year 3):** generational-transmission paper. Multi-generational register linkage (BEF parent-child identifiers back to 1968) tied to parent's DREAM transfer history during child's formative years (ages 6-18). Categorically impossible in ESS; uniquely possible in Danish registers.
- **Y5 (PhD year 4 / book):** cross-national synthesis with mechanism evidence. Return to comparative frame armed with within-Denmark mechanism papers; test generalisation to Sweden, Norway, Finland via Nordic register-research network.

**Why this arc matters for the seminar paper:** the Y2 within-individual design directly defuses three CRITICAL items from the council critique of the empirical walkthrough (institutional-bundle confounding, selection into RTI, N=15 ceiling). The thesis is the load-bearing causal-identification move the seminar paper's §V.G gestures toward.

## Candidate thesis designs (refined under asymmetric framing)

**Design A — Welfare contact as treatment (recommended, hardest):**
Compare political attitudes before/after individual welfare contact events. Register linkage of IDA + DREAM + Folketing electoral register. Mass layoffs identified via firm-level FIDA shocks. Best test of Prediction 1 at the individual level via path-dependence. Dal Bó-Finan-Folke-Persson-Rickne (2023, QJE) Sweden Democrats template demonstrates the method works for political outcomes.

**Design B — Municipal variation:**
Exploit cross-municipality variation in activation policy implementation (sanction rates, counselling intensity). Tests Prediction 1 cleanly; harder to test Prediction 2.

**Design C — Reform quasi-experiment:**
Event studies around Danish activation reforms (2003 contact requirements; 2006 benefit duration tightening; **2010 dagpengereform** — halved UI duration from 4→2 years, tightened eligibility from 52→26 weeks of work; 2013 Disability Pension Reform). DiD or event study. Most tractable. All four reforms are *conditionality-introducing* — they test Prediction 1 directly. There is no decommodification-expanding reform of comparable magnitude in the same period; this absence is itself consistent with the asymmetric theory and worth noting in the framing.

**Recommended starting design:** C with the 2010 dagpengereform as the central shock, RTI-coded treatment heterogeneity from ISCO-08 codes via the same `isco08_3d-task3.csv` task scores used in the seminar paper, and Folketing electoral register as the political outcome. Closest to the Dal Bó et al. (2023) and Dustmann-Vasiljeva-Damm (2019) templates.

## Pre-commitment checks (from council ideation §"Three things to check before committing")

1. **Scoop scan due 2026-08-01** (Todoist 6gcPG6wFFF93Mx6X): targeted lit scan in IZA / NBER / SSRN / Google Scholar for any 2024-2026 paper combining ISCO-task-coded RTI exposure with Danish register political outcomes. Adjacent flagged: Dustmann-Vasiljeva-Damm 2019, Dal Bó et al. 2023, Mitrut-Wolff Danish welfare-transmission, Andersen-Svarer-Kreiner UI-reform tradition. If a close-enough paper already exists, reframe the angle.
2. **Does Denmark have enough decommodification variation, or does the within-country project test a *related-but-different* claim?** Denmark sits at high-decommodification end. Within-Denmark variation is mostly *conditionality* (means-tested vs contributory) and *temporal retrenchment* (2010 reform). Decide whether this is a feature (sharper test of conditionality vs generosity) or a bug (a different claim than the cross-national paper). Surface in the thesis framing rather than letting a referee surface it. **Tentative read:** feature, not bug — the asymmetric theory makes the conditionality channel central to damage signatures.
3. **Co-supervisor candidate already in orbit:** Andersen-Svarer-Kreiner UI-reform group at Aarhus / Copenhagen. Tier-3 supervisors in the Notion Supervisor Watchlist (see Applications Studio).

## Candidate theoretical sharpenings (from 2026-05-10 second-Claude ideation session)

A separate Claude session ran a three-prompt ideation against the seminar paper's outputs. Three patterns surfaced that have thesis implications. None should be committed to the seminar paper without explicit decision; all three deserve serious consideration as thesis-stage refinements.

### Two-channel theory (the strongest candidate)

**Encounter channel** vs **environment channel**: welfare design has two distinct effects on political behaviour. The encounter channel is the §III.B/C mechanism — what happens to a specific person at a specific institutional encounter. The environment channel is what the institutional vocabulary does to *everyone* who lives inside it, encounter-experienced or not. The country-level CWED finding (r=−0.85) is likely picking up the environment channel because welfare design varies cross-nationally but is roughly uniform within country; the within-country regional null is consistent with this because there is little within-country variance in welfare *design* (only in implementation/discourse). The sub-component non-specificity (UE ≈ SK) also follows from environment-channel dominance.

**Why this matters for the thesis:** the Y1 within-individual Danish-register design is positioned to *separate* encounter from environment for the first time. Testable prediction: if encounter is the dominant channel, RTI × CWED moderation should be substantially stronger for welfare-receipt-yes than welfare-receipt-no individuals. If similar — environment dominates. This is the highest-information test the thesis can run; it adjudicates between two distinct stories of welfare's political effect that the seminar paper currently conflates.

**Strategic implication:** this reframing strengthens the seminar paper's argument rather than weakening it — environment-channel dominance would mean welfare design's largest political effect is on the people who *don't* encounter it directly, who carry institutional vocabulary into politics regardless of personal exposure. That's a stronger architectural-reading claim, not a weaker one.

### "Care without connection" (candidate sharpening of asymmetric mechanism)

The seminar paper's §III.E currently explains the solidarity null via three pillars (loss aversion, status positionality, irreversibility) plus a gesture at "solidarity requires political work." The second-Claude session identified a sharper version inside Ben's own curatorial corpus: the hooks passage "cathexis is not love; care is a dimension of love but caregiving alone is not loving" maps directly onto the welfare-solidarity asymmetry. Decommodification delivers care (material support) without delivering connection (the relational thickness — shared workplaces, ritual repetition, deliberative practice — that builds solidarity-as-thick-relation).

**Thesis-relevance:** Y3 mechanism-interrogation paper could test relational thickness as a moderator. Survey-experimental: vary the *form* of welfare receipt (transactional cash transfer vs participatory programme with peer interaction) and measure solidarity outcomes. Register-linked: identify Danish programmes that vary on the transactional-vs-relational dimension and test attitudinal path-dependence.

**Sharper version of the §III.D framing:** the right gloss on "solidarity requires political work that welfare design alone cannot do" is *solidarity is relational rather than transactional; decommodification (a property of transfers) can clear the ground for relational solidarity but cannot construct it.* This is a one-sentence move; surfaced for Ben's decision tomorrow as a candidate sharpening.

### Pattern A — Cultural ≈ economic items respond similarly (sample-level refinement)

Session3 item-level analysis: imueclt (cultural) β=+0.045, imbgeco (economic) β=+0.055; both p<0.001. The cultural-only specificity claim is not supported. The data is consistent with welfare moderating BOTH cultural AND economic anti-immigration channels in parallel.

**Theoretical implication:** the §III.C misattribution stage is currently presented as cultural-rerouting of economic frustration. A cleaner version: economic and status anxieties operate in parallel, both shaped by welfare design, both producing exclusion under stigmatising regimes. This widens what the moderation operates on without disturbing the asymmetric core.

**Thesis-relevance:** Y2-Y3 papers can test parallel channels directly with item-level Danish survey data linked to register.

### Pattern C — Sickness/unemployment sub-typology heterogeneity

Sub-component analysis flips between specs: UE > SK under base spec, SK > UE under macro controls. Probably reflects which Bismarckian / Liberal / Nordic countries drop from the macro-controls sample. The deeper claim: welfare states aren't unitary within country — sickness, unemployment, and pensions carry different cultural registers (Bismarckian sickness = status-preserving; Liberal sickness = means-tested last resort).

**Refined dignity claim:** "the dignity register of the most-encountered welfare programme matters" rather than "decommodification matters." Cross-national variation in moderation could track unemployment-CWED variation in Liberal-vs-Nordic comparison but sickness-CWED variation in Bismarckian-vs-Nordic comparison. Testable but underpowered at N=15; thesis-stage register data dissolves the constraint.

### Reasoning provenance (from second-Claude session)

The second Claude flagged its own reasoning as **[grounded]** (from session 1-3 computed numbers), **[adjacent]** (extending from saved-passages + manuscript), or **[speculative]** (pattern-matching training data). Two-channel theory and Pattern A are well-grounded in actual computed numbers; care-vs-connection is adjacent (extends Ben's hooks corpus); Pattern C is partly speculative on cause. Full transcript preserved in `quality_reports/council_ideations/2026-05-10_second_claude_three_prompts.md` (file does not yet exist; create from transcript when integrating these candidates).

---

## Link to seminar paper

The seminar paper establishes the cross-national association (CWED × RTI → exclusion) and theorises why no symmetric mirror-image association on the solidarity side exists. Its §V.G (sharpened 2026-05-10) names the Danish activation reforms 2003 / 2006 / 2010 / 2013 and "administrative-register linkage" as the design follow-up. The thesis provides the causal identification using within-country variation.

Under the asymmetric framing, the strongest test is on Prediction 1 (damage signatures) using within-individual welfare encounter data, not just within-country aggregate variation.

---

*Updated 2026-05-10 — high-fidelity sync to reflect council ideation roadmap, timeline correction (thesis is Y1 of five-year arc, not PhD chapter), and scoop-scan + supervisor-watchlist linkage. Previous 2026-04-25 entry superseded.*
