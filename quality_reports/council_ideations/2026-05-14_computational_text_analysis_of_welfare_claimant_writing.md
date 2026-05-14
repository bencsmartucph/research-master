# Council Ideation — Computational Text Analysis of Welfare Claimant Writing

**Date:** 2026-05-14
**Input:** `"computational text analysis of welfare claimant writing as a method for studying institutional damage to self-concept — extending the asymmetric-welfare dignity-mechanism research programme beyond cross-national survey work"` (inferred from preceding chat context — Ben's recommended bet from the Prompt 3 follow-up on resist-the-survey-paradigm).
**Framing:** The asymmetric-welfare paper documents that welfare design moderates the conversion of economic disruption into anti-immigration attitudes, but the theory it rests on — that stigmatising welfare encounter damages self-concept and triggers identity switching — is articulated in qualitative work (Wagner 2022, Patrick 2016, Soss 1999) and cannot be tested with attitudinal survey items that ask people to summarise their inner lives on Likert scales. The proposal is to apply computational text analysis to claimant-produced writing — tribunal appeal letters, online forum posts on r/UniversalCredit and Mumsnet, oral history transcripts — measuring linguistic markers of agentive selfhood (modality, voice, hedging, framing) before and after welfare encounter events. Evidence would require building a longitudinal corpus where the same individual is observed across multiple time-points and identifiable institutional encounters.
**Personas:** Obvious Extension, Adjacent Outsider, Constraint Inverter (synthesis by main session)

---

## Synthesis

### The convergent thread

All three personas circle the same data attractor: **r/UniversalCredit + Mumsnet benefits forums** as the corpus, **within-person event-anchored change** as the unit of variation, and **language produced for the writer's own purposes** as the evidence. The Obvious Extension treats it as a DiD panel exploiting UC rollout. The Adjacent Outsider applies Pennebaker-Al-Mosaiwi clinical psycholinguistic depression markers to it. The Constraint Inverter treats it as a network and asks whether claimant identity disorganisation has a contagion structure. They disagree about which method to bring; they agree about which site.

But the deeper convergence is methodological-philosophical. **All three personas share the bet that institutional damage to self-concept is measurable at scale in writing that wasn't produced for measurement.** What Wagner observed in thirty ethnographic interviews can — in principle — be measured in tens of thousands of forum posts, *if* the linguistic markers are valid proxies for the underlying construct *and if* the event-anchoring can be made reliable. Both IF clauses are the load-bearing assumptions of the whole programme. The personas differ on which default to break (text-as-given for the Constraint Inverter, individual-as-unit for the network move, single-language for the parallel corpus). They agree that the ESS-Likert paradigm has run out of analytical room for the question the dignity thread is actually asking.

### The boldest single move

**The Counterfactual Claimant Experiment** (Constraint Inverter Angle 1). Recruit ~2,000 current or recent UC, ESA, and PIP claimants on Prolific UK; randomly assign rights-based, means-tested, or no-framing prompts for the agency that processed their last benefits interaction; have each participant write the same biographical incident under three different frames; measure within-person shifts in linguistic agency markers (modality, voice, first-person agency, internal-state vs. external-cause verb ratios).

Why it's the highest-information-value move:

- **It makes a directional commitment the observational angles can't.** If framing shifts language within 400 words, the dignity-damage mechanism is *acute*. If it doesn't, the mechanism is *cumulative* across many encounters, and the entire research programme has to reorganise around long-run dose-response measurement. Either result reshapes the next paper.
- **Within-person experimental identification is the cleanest the data permit.** Participant fixed effects absorb stable individual style; random framing assignment is exogenous by construction.
- **It's a single 12-month paper.** Doable in PhD years 2–3. Publishable in *Journal of Politics* or *British Journal of Political Science* experimental section — venues your home discipline reads.
- **The null is informative.** Most experiments fear the null; this design's null updates the theory in a specific way (mechanism is cumulative, not acute) without sinking the dissertation.
- **It dissolves the construct-validity critique** the Adjacent Outsider raised. The manipulation IS the test. The linguistic markers don't need to be pre-validated against clinical proxies to deliver the headline result; they only need to *respond* to the framing.

The runner-up is Conversation Analysis of recorded DWP encounters (Adjacent Outsider Angle 1) — methodologically bolder still, going to the actual moment of damage in turn-by-turn detail. But N≈40 and a 2–3 year fieldwork commitment make the cost-information ratio worse for an early-career programme. The experiment beats the CA on time-to-first-paper; the CA beats the experiment on depth-of-mechanism.

### A five-year research programme combining these

**Year 1 (final MSc + PhD start).** Methods foundation. A Loughborough or York corpus-linguistics summer school. Two papers read deeply: Wagner 2022 and Al-Mosaiwi & Johnstone 2018. **A 200-participant Phase 0 validation pilot** — Prolific UK volunteers writing spontaneously, paired with the Sense of Agency Scale and PHQ-9 — to calibrate a Python NLP pipeline against clinical proxies. The pipeline (modality detection, first-person singular rate, absolutist-word density, voice extraction) becomes the spine of every later paper. If the markers don't correlate with the construct at this stage, redesign before going further. ~£3,000, 2 months.

**Year 2 (PhD chapter 2).** The Counterfactual Claimant Experiment. N≈2,000 on Prolific UK, pre-registered on OSF, ESRC PhD enrichment funding (~£25,000). Submission target: *Journal of Politics* (experimental section) or *BJPS*. This is the cleanest-ID paper. If the manipulation moves markers within-person, the mechanism is acute and you have a defensible measurement instrument. If it doesn't, you've learned the mechanism is dose-cumulative and the rest of the programme adjusts accordingly.

**Year 3 (PhD chapter 3).** The r/UniversalCredit + Mumsnet longitudinal corpus. Using the now-validated markers, scrape and panel-structure the full r/UniversalCredit + r/DWPhelp + r/BenefitsAdviceUK + Mumsnet benefits forum (2018–2027). Event-anchor via regex extraction of self-disclosure ("got sanctioned", "MR refused", "tribunal date") with human-coded validation on a stratified subsample. Difference-in-differences with user and time fixed effects, exploiting UC rollout cohort variation. Submission target: *Sociological Science*, *AJS*, or a computational social science venue — where the methods read clean and the construct travels. This is the high-N within-person paper.

**Year 4 (PhD chapter 4).** Branch by what Year 2 established. If the mechanism is **acute** (experiment delivered), pursue the **tribunal-FOI design** (Obvious Extension Angle 3): UK First-tier Tribunal appeal documents acquired via FOI to HMCTS, linked to subsequent r/DWPhelp posting activity. Causal identification via tribunal-panel fixed effects. Submission target: *J. Public Economics* or *J. Social Policy*. If the mechanism is **cumulative**, pursue the **four-regime parallel corpus** (Constraint Inverter Angle 3): UK + Sweden + Germany + Italy tribunal/appeal letters and elicited narratives, LLM-translated with documented audit. Tests Esping-Andersen predictions on text. Submission target: *CPS* or *APSR*. The branch point is informative.

**Year 5 (dissertation + first postdoc applications).** The integrative chapter. Triangulate experiment (acute, manipulable, clean ID, narrow ecological footprint), corpus (cumulative, observational, large N, rich event structure), and institutional-variation paper (cross-regime or tribunal-FOI). The triangulation argument *is* the dissertation's contribution: dignity damage is a measurable inner-life process that operates at multiple temporal scales and across institutional contexts, and the same linguistic markers can be deployed at each scale. Job market paper: the experiment. Second paper: the corpus. Third paper: the institutional-variation chapter. Conference pathway across APSA, MPSA, EPSA (substantive/methods) plus IC2S2 and Text-as-Data (computational social science). A semester visiting Pennebaker's lab at UT Austin or Bail's Polarization Lab at Duke in Year 4 sets up the postdoc network.

### Three things to check before committing

1. **Construct validity — Phase 0 pilot is non-negotiable.** All three personas hand-waved past whether agency markers (modality, first-person singular, absolutist words) actually track the construct (self-concept damage) for *this* population. The Pennebaker / Al-Mosaiwi validation was done on clinical depression samples; mapping it to welfare claimants is plausible but not established. Run the 200-participant pilot with clinical proxies (Sense of Agency Scale, PHQ-9) before committing 3+ years to the programme. If the markers don't correlate, the entire architecture is built on sand and the personas have been hand-waving.

2. **Scoop risk on r/UniversalCredit is real and named by two of three personas.** A Computational Sociology PhD (Bail's lab at Duke, De Choudhury's at Georgia Tech, Saha's network) could publish a defensible version of the longitudinal Reddit-welfare paper within 18 months of starting on it. Decide now whether to lead-author this *or* yield it. If yielding, commit to the harder-to-replicate angles (tribunal FOI, Conversation Analysis recordings, the four-regime parallel corpus) for primary novelty. A reasonable hedge: pre-register the Reddit corpus design publicly in Year 2 alongside the experiment, which establishes scientific priority without requiring the corpus paper to be done yet.

3. **The "political-economy-doesn't-read-it" problem.** All three personas raised some version. AJPS/CPS referees may treat computational text work on welfare claimants as "humanistic gesture, wrong evidence base." Plan publication strategy from the design stage, not the end: experiment → *JoP / BJPS* (clean experimental ID is what those venues want), Reddit corpus → *Sociological Science / PNAS-Nexus* (computational sociology venues that read this work as central), tribunal letters or cross-regime → *CPS / JESP* (welfare-state venues where the institutional variation is the contribution). Build co-author networks across home and adjacent fields so the referee pool is favourably composed for each paper. The dissertation can be all three; individual papers should be venue-targeted from the first sentence of the abstract.

---

## Raw persona reports

<details>
<summary>Obvious Extension</summary>

## Three concrete angles

**1. Welfare regime moderation of automation-anti-immigration link, with mechanism evidence from ESS open-ended responses**

Question: Does the strength of the routine-task-intensity → anti-immigration relationship vary systematically across welfare regimes, and can open-ended ESS responses about "the most important issue facing this country" be used to validate that the mechanism is identity-defensive rather than material-competitive?

Setting: ESS waves 6-9 (already loaded in Research_Master), with a methodological extension using the open-ended response fields that exist in some ESS waves. Supplement with the EVS 2017 wave which has more extensive open-ended modules. Cross-national, 15-20 European countries, individual-level.

Rationale: This is the obvious senior-advisor move. It takes the existing paper's central finding — welfare design moderates conversion of disruption into exclusion — and bolts on a mechanism test that the supervisor has been asking for since draft v3. The Likert-scale measurement critique that motivated the bigger qualitative-text proposal can be partially addressed within the existing dataset by treating open-ended responses as a low-stakes proxy. You get a job-market paper that extends the seminar paper, validates the published methodology, and demonstrates text-analysis capability without requiring a new corpus from scratch. The dissertation chapter writes itself: Chapter 1 is the published asymmetric paper, Chapter 2 is the cross-regime extension with mechanism evidence, Chapter 3 is the more ambitious claimant-corpus work.

**2. r/UniversalCredit longitudinal user-level corpus, with policy-shock identification**

Question: Do welfare claimants' linguistic markers of agentive selfhood (first-person agency, modality, voice) shift in measurable ways around documented institutional encounter events (sanctions, assessments, appeal outcomes), and do these shifts predict subsequent expression of anti-outgroup sentiment in the same user's posting history?

Setting: r/UniversalCredit, r/DWPhelp, and r/BenefitsAdviceUK on Reddit (~50,000-100,000 unique users posting 2016-2026, scraped via Pushshift or the academic Reddit API). User-level panel with self-reported encounter events that can be timestamp-anchored. Optionally extend to Mumsnet's "money matters" forum which has overlapping demographics.

Rationale: This is the most fundable version of the claimant-text idea because the data is free, already digitised, and has a built-in panel structure where the same pseudonymous user is observable across hundreds of posts spanning years. The 2017-2018 Universal Credit rollout, the 2022 cost-of-living payments, and various sanction-regime changes provide policy shocks for difference-in-differences identification at the user level (with users in different rollout cohorts as the comparison). You can pre-register the linguistic markers from Wagner (2022) and Patrick (2016) as hypotheses and test them with off-the-shelf NLP tools (spaCy for dependency parsing, transformer embeddings for stance). This is a paper Ben can write in 18-24 months with current Python skills plus one corpus-linguistics short course.

**3. Tribunal appeal letters from PIP/UC decisions, FOI-acquired, with linguistic measurement of dignity recovery**

Question: Among claimants who win their PIP or Universal Credit tribunal appeal, does the language of their appeal submission (high agency, formal voice, claims-making register) correlate with the linguistic register of their subsequent online expression — and conversely, do claimants who lose appeals show measurable shifts toward depersonalised or fatalistic register in subsequent online traces?

Setting: UK First-tier Tribunal (Social Security and Child Support) appeal documents acquired via FOI request to HMCTS, redacted by tribunal staff, linked at the postcode-district level to subsequent r/DWPhelp posting activity through self-declaration in claimant posts ("won my MR" / "lost my tribunal"). N likely 500-2,000 linkable cases, but each case has a rich pre/post linguistic profile.

Rationale: This is the version that gets you a Russell Group / continental-Europe PhD offer because it combines administrative data acquisition (signals research-infrastructure competence), causal identification (the tribunal outcome is plausibly as-good-as-random conditional on case characteristics), and computational text analysis (signals methodological depth). It also lets you write the dignity-recovery paper that the qualitative welfare literature has been pointing toward for fifteen years but cannot test because qualitative methods cannot establish counterfactuals. The headline finding — "winning a tribunal appeal partially restores agentive language, losing accelerates its decline" — would be a *Comparative Political Studies* or *Journal of Social Policy* paper with crossover potential to *JPubE*.

## What you'd need to do this

**Angle 1 (welfare-regime moderation + ESS open-ended):**
- Data: Already have. Add EVS 2017 wave (free download). Extract ESS open-ended fields from raw .dta files; you have not previously used these.
- Method: Existing pipeline plus topic modelling (BERTopic or seeded LDA) on open-ended responses; sentiment/stance extraction with a pre-trained multilingual model (XLM-RoBERTa).
- Partnerships: None essential. A computational linguistics co-author at KU or LSE would smooth review but not blocking.
- Time horizon: 6-9 months to a working paper; 12-15 months to journal submission. Compatible with finishing the MSc thesis in parallel.

**Angle 2 (Reddit longitudinal corpus):**
- Data: Reddit Pushshift archive (~$0 if academic access, ~$200-500 if API tier). ~500 GB of raw text to process. Local GPU or Copenhagen HPC access for embedding generation.
- Method: User-level panel construction (deduplicate accounts, infer encounter events from regex-extracted self-reports); linguistic feature extraction; difference-in-differences with user and time fixed effects. Pre-registration of linguistic hypotheses derived from Wagner (2022).
- Partnerships: A corpus linguist co-author is genuinely helpful — Maite Taboada (SFU) or Paul Baker (Lancaster) run programmes that do exactly this kind of work. A welfare-rights organisation (CPAG, Z2K) for ground-truthing encounter-event language.
- Time horizon: 18-24 months. Three months on infrastructure, six on corpus construction, six on analysis, three on writing. Fits within Year 1-2 of PhD.

**Angle 3 (Tribunal FOI + linkage):**
- Data: FOI request to HMCTS for redacted appeal documents — non-trivial, expect 6-12 months and possibly a refusal that requires ICO escalation. Backup: scraped UK case-law database (BAILII) for the subset of cases with written decisions. r/DWPhelp scrape as in Angle 2.
- Method: OCR (Tesseract or AWS Textract for handwritten appeals); same linguistic-feature pipeline as Angle 2; record linkage via self-declaration plus postcode district where available. Causal identification via tribunal-panel fixed effects (some panels are systematically more claimant-favourable, exploit this for IV).
- Partnerships: Essential. UK welfare-rights NGO for FOI navigation and ethics framing. UK socio-legal scholar (Robert Thomas at Manchester, Joe Tomlinson at York) for institutional knowledge of tribunal process. Probably needs a UK-based co-PI to make the FOI work.
- Time horizon: 30-36 months. This is a dissertation, not a chapter — it needs to be the structural centre of a PhD.

## Closest existing literature

**Angle 1:**
- Brady & Finnigan (2014) on cross-national welfare attitudes — the published ESS-pooled regression template.
- Häusermann, Kurer & Schwander (2015) on welfare-state preferences by occupational class — the closest methodological cousin.
- Naumann, Buss & Bähr (2016) and Margalit (2013) on automation/economic-shock attitudes — the literature the seminar paper is already in conversation with.

**Angle 2:**
- Wagner (2022) on claimant linguistic agency under Universal Credit — the qualitative anchor.
- Baker & McEnery (2015) and Baker (2014) on corpus-assisted discourse analysis of UK welfare press coverage — the methodological template.
- Saha, Schoenebeck & De Choudhury (2017) on Reddit-based longitudinal mental-health linguistic markers — the closest methodological precedent for the panel design.

**Angle 3:**
- Adler (2003, 2018) on UK tribunal justice and administrative-law dignity — the institutional literature.
- Patrick (2016, 2017) "For Whose Benefit?" — the qualitative dignity-recovery framing.
- Soss (1999, 2000) "Lessons of Welfare" — the foundational claim that welfare institutions teach political subjectivity, which Angle 3 operationalises at scale.

## Why someone smart would dismiss this

The senior critic objection across all three angles is the same: NLP measurement of "agentive selfhood" or "dignity register" is a contested research programme even within computational sociolinguistics, and the validity of these constructs has not been established in a way that would survive a methods referee at AJPS or CPS. You are proposing to measure a latent construct (self-concept damage) via surface linguistic features (modality, voice, first-person agency), then make causal claims about that latent construct from those surface features, and the chain of inference has at least three weak links — construct validity of the linguistic markers, reliability of pseudonymous-account longitudinal linkage, and the assumption that linguistic shifts on Reddit reflect underlying psychological shifts rather than platform-specific register adaptation. A senior critic would say: do Angle 1, publish it, then decide whether Angles 2 and 3 are worth a PhD's worth of methodological risk. The compromise version — Angle 1 as MSc thesis and Year 1 publication, Angle 2 as the methodologically ambitious centrepiece with Angle 3 as the dignity-recovery showstopper — is the safe path. Pursuing 2 and 3 without 1 as a foundation is high-variance, and the variance is on the downside.

</details>

<details>
<summary>Adjacent Outsider</summary>

## Three concrete angles

**1. Conversation Analysis of Welfare Encounters: Sequence Structure as Identity Damage**

*Question:* How does the turn-taking architecture of Jobcentre/DWP work-capability interviews systematically produce "dispreferred self-presentations" — and does repeated participation in this sequence structure correlate with downstream linguistic markers of diminished agency in unscripted speech?

*Setting:* Audio recordings of UK DWP work-capability assessments (obtainable via SAR requests by claimants who consent, or via charities like Z2K and Disability Rights UK that already hold a small corpus), paired with the same individuals' speech in non-institutional settings (interviews with the researcher, voice diary entries via a phone app).

*Rationale:* Political economy treats the welfare encounter as a transaction over benefits. Conversation analysis (Sacks, Schegloff, Heritage) treats it as a *micro-political* event with measurable structural features — adjacency pairs, repair sequences, who initiates topic shifts, who has rights to ask questions. The DWP assessment is structurally an institutional interrogation: the claimant is in second-pair-part position for hundreds of consecutive turns, must produce "dispreferred" admissions of incapacity to qualify for support, and has no rights to topic-initiation. Heritage and Stivers have shown in medical-encounter CA that this kind of sequence position produces measurable downstream effects on patient self-presentation. If welfare encounters damage selfhood, *the damage is happening in the turn-by-turn structure of these interactions*, not in some downstream attitudinal residue. Recording the encounter itself bypasses the entire problem of asking people to summarise their inner lives on Likert scales.

**2. Linguistic Inquiry & Word Count (LIWC) + Psycholinguistic Depression Markers on Longitudinal Claimant Writing**

*Question:* Do claimants' first-person singular pronoun rates, absolutist-thinking markers ("always," "never," "completely"), and cognitive-processing word frequencies shift across the trajectory of a Universal Credit claim — and do these shifts predict subsequent political-attitude changes measurable in the same individuals' forum posts?

*Setting:* r/UniversalCredit and r/DWPhelp Reddit corpora (publicly scrapeable, ~150K posts, many users with multi-year posting histories), plus Mumsnet Money/Welfare boards. Build a pipeline that identifies users with documented "trigger events" (sanction, MR refused, PIP review) through self-disclosure in posts, then computes within-person time series of psycholinguistic features.

*Rationale:* The psycholinguistics of depression literature (Pennebaker, Rude, Al-Mosaiwi) has established that *first-person singular pronoun frequency* and *absolutist thinking* are robust markers of depressive and anxious cognition that *predict* clinical depression onset rather than just correlating with it. Al-Mosaiwi & Johnstone (2018) found absolutist words have higher prevalence in anxiety/depression/suicidal-ideation forums than control forums by a factor of ~1.5-1.8 — a much larger effect than most attitudinal-survey effects in political behaviour. Crucially: these markers are extractable from text people produce *for their own purposes*, not in response to a survey. This is the methodological move that lets you observe identity damage without asking people to summarise it. The political-economy contribution is showing that the same linguistic features that predict clinical depression are *moderated by welfare regime generosity* — i.e., that institutional design produces measurable psycholinguistic damage.

**3. Narrative Identity Coding (McAdams Life-Story Protocol) on Welfare-Reform Oral Histories**

*Question:* When claimants tell the story of their relationship to work and welfare, do they construct "redemption sequences" (bad → good, agency restored) versus "contamination sequences" (good → bad, agency lost) at different rates depending on welfare-regime type — and does the *narrative arc* predict subsequent voting behaviour better than the attitudinal content?

*Setting:* British Library oral history collections on poverty and welfare (the "Living with Hard Times" and "Millennium Memory Bank" archives), supplemented with new fieldwork interviews using McAdams' Life Story Interview protocol with matched samples of UK and Danish/Swedish long-term claimants.

*Rationale:* Developmental and personality psychology — specifically Dan McAdams' three decades of work on narrative identity at Northwestern — has built a coding scheme for how people construct life stories, with redemption sequences, contamination sequences, agency themes, and communion themes as the core dimensions. McAdams and colleagues have shown these narrative features predict mental health, political ideology, and generativity *better than* trait-level personality measures. The political-economy literature on welfare and selfhood has zero engagement with this tradition. The contribution would be: *welfare regime type predicts the distribution of redemption vs. contamination sequences in claimants' life narratives*, with stigmatising means-tested regimes producing higher rates of contamination sequences and universalist regimes producing higher rates of redemption sequences. This connects the inner-life inquiry (how do people construct themselves as agents?) to the institutional inquiry (what does the welfare state do?) at the level of the *story*, which is where identity lives in the developmental-psychology tradition.

## What you'd need to do this

**Angle 1 (Conversation Analysis):**
- Data: ~30-50 audio recordings of DWP assessments + matched non-institutional speech samples. Realistic acquisition route: partnership with Z2K (advocacy charity, already collects SAR-released assessment recordings) or with Public Law Project.
- Method: CA training. The standard route is the Loughborough or York CA summer schools (1-2 weeks intensive). Transcription using Jefferson conventions is labour-intensive — budget ~10 hours of transcription per hour of audio.
- Partnerships: A CA-trained co-supervisor or collaborator (Elizabeth Stokoe at Loughborough or Paul Drew/Merran Toerien at York are the obvious UK names; Toerien has worked specifically on welfare-assessment interviews).
- Time horizon: 2-3 years for a defensible corpus. Single-encounter qualitative study possible in 12 months.

**Angle 2 (Psycholinguistic Markers on Reddit/Mumsnet):**
- Data: Reddit API scrape of r/UniversalCredit (free, ~150K posts), Mumsnet welfare boards (scraping permitted under their ToS for academic work; check). Pushshift.io archive if Reddit API restrictions tighten.
- Method: LIWC-22 (commercial license ~$90/year academic) or open-source alternative (Empath, or building dictionaries from scratch). Pennebaker's research group at UT Austin maintains the LIWC validation literature; their handbook is the methodological starting point.
- Partnerships: A psycholinguist as second supervisor. Mohammed Al-Mosaiwi (Reading) works on exactly this; Pennebaker's lab at UT Austin or James Pennebaker himself would be the gold-standard external advisor.
- Time horizon: 12-18 months for corpus + analysis. The data are already there; the work is computational.
- IRB/ethics: Reddit posts are public but "contextual integrity" (Nissenbaum) is a live ethical question — the discipline is still working out the norms. Mumsnet specifically has had recent controversies over researcher use of posts. Get explicit IRB approval and consider whether to seek user consent for direct quotation.

**Angle 3 (Narrative Identity Coding):**
- Data: ~40-60 life-story interviews (the McAdams protocol takes 2-3 hours per interview), matched UK and Nordic samples. Plus secondary analysis of British Library oral histories (already transcribed, freely accessible).
- Method: McAdams' Life Story Interview protocol (publicly available from his Foley Center website) + the coding manuals for redemption, contamination, agency, and communion themes. Coding requires two trained coders for inter-rater reliability; budget 4-6 hours per transcript for double-coding.
- Partnerships: A narrative psychologist. Jonathan Adler (Olin) is McAdams' most active senior collaborator and runs the Personality and Psychotherapy Lab. Dan McAdams himself is still active at Northwestern.
- Time horizon: 3 years if collecting new interviews; 18 months for secondary-analysis-only design using British Library archives.

## Closest existing literature

**Angle 1:**
- Drew & Heritage (1992), *Talk at Work* — foundational CA-of-institutions text. Sets up the framework for analysing asymmetric institutional encounters.
- Toerien, Sainsbury, Drew & Irvine (2013-2015 series) on UK work-capability assessments — already done conversation-analytic work on this exact setting. Toerien is the closest thing to a direct predecessor; her work would be the platform to extend.
- Stivers, Mondada & Steensig (2011), *The Morality of Knowledge in Conversation* — pushes CA into the territory of how rights and obligations to know things get distributed in talk. Directly relevant to "what does it do to claimants to be in a knowledge-deficit position for 90 minutes?"

**Angle 2:**
- Pennebaker, Mehl & Niederhoffer (2003), "Psychological aspects of natural language use" — the canonical statement of the LIWC research programme.
- Al-Mosaiwi & Johnstone (2018), "In an absolute state: Elevated use of absolutist words" — direct precedent for the depression-markers move. Published in *Clinical Psychological Science*.
- Eichstaedt et al. (2018) on predicting depression from Facebook language — *PNAS* paper that showed clinical-grade prediction from social media text alone. Demonstrates the method works at scale.

**Angle 3:**
- McAdams (1985 onwards), the entire narrative identity research programme. *The Stories We Live By* (1993) is the popular statement; *The Redemptive Self* (2006) is the most directly relevant to political-economy questions because it explicitly links narrative form to civic engagement.
- Adler, Lodi-Smith, Philippe & Houle (2016) meta-analysis in *Personality and Social Psychology Review* — establishes that narrative identity features predict well-being independently of trait personality.
- Hammack (2008), "Narrative and the Cultural Psychology of Identity" — bridges McAdams' developmental tradition to political-identity questions, which is the bridge Ben specifically needs.

## Why someone smart would dismiss this

The strongest objection is *measurement-as-theory-laundering*: a senior critic from political economy would say that linguistic markers (pronoun rates, redemption sequences, repair structures) are tools developed to study clinical depression and personality, not political behaviour, and importing them as proxies for "identity damage" risks dressing up a clinical-psychology finding as a political-economy finding without doing the conceptual work to show that the construct *measured* is the construct *theorised*. Worse: it lets the political-economy researcher avoid the hard question (what does it mean to say welfare damages selfhood, *politically*?) by substituting a tractable measurement question (do pronoun rates shift?). The methods are also slow and expensive — three years of CA training and transcription, or a narrative-identity coding project with double-coded inter-rater reliability, produces n=40 cases that no top-five political-economy journal will accept as evidence about institutional effects. The scoop risk is real on Angle 2 specifically: the digital-trace + welfare-encounter combination is sitting there in plain sight; someone in computational sociology will get to it within 18 months of Ben starting. The dismissal a comparative-politics referee at AJPS or CPS would write: "interesting humanistic gesture, wrong evidence base, doesn't update the welfare-state-and-populism literature in a way the field can use."

</details>

<details>
<summary>Constraint Inverter</summary>

## Three concrete angles

**1. The Counterfactual Claimant: LLM-Elicited Self-Concept Under Manipulated Welfare Encounter Conditions**

*Question:* Does the same individual produce systematically different markers of agentive selfhood when narrating a welfare encounter framed as rights-based versus means-tested, holding the underlying biographical content constant?

*Setting:* A controlled writing experiment running through Prolific UK with 1,500-2,000 current or recent Universal Credit, ESA, and PIP claimants. Each participant writes three 400-word narratives about a recent benefits interaction under randomly assigned framings of the agency that processed it (rights-bearer addressing a public service vs. supplicant addressing a discretionary gatekeeper vs. control with no framing). A subset of 400 also completes a second wave four weeks later under a different framing — within-person experimental variation. The fixed biographical core is held constant via a structured prompt (the same incident must be re-narrated under each frame).

*Rationale:* This drops the text-as-given constraint completely. The dignity-damage hypothesis predicts the framing itself should alter linguistic agency markers in real time — modal verb distribution, ratio of internal-state verbs to external-cause verbs, the prevalence of "they made me" versus "I decided to" constructions. If Wagner's claim is right, even a paragraph of frame-priming should produce measurable register shifts in the next 400 words a real claimant writes about a real encounter. This is testable in a way the qualitative literature has never managed because no one has manipulated the framing while collecting the writing. It also gives him a within-person identification strategy that observational tribunal corpora cannot: participant fixed effects absorb stable individual differences in writing style, and the random framing assignment is exogenous by construction. Three potential publication venues — *Journal of Politics* (experimental section), *British Journal of Political Science*, *American Journal of Political Science* — all of which weight clean experimental identification heavily.

---

**2. The Mumsnet-r/UniversalCredit Linguistic Contagion Map: Network-Level Self-Concept as a Diffusing Property**

*Question:* When a high-profile claimant whose posting history shows a recent identity rupture (a shift in linguistic agency markers tied to a documented welfare encounter) posts in a forum, do reply chains in the next 72 hours show measurable convergence toward that linguistic register among repliers — controlling for thread topic, repliers' own pre-thread baselines, and seasonal/political shocks?

*Setting:* The full r/UniversalCredit corpus (2018-present, ~150,000 posts) plus the Mumsnet "Money Matters / Benefits" sub-forum (publicly archived, ~30 years of continuous posting), linked at the user level via persistent usernames. Each user has a 2-5 year prior posting history that establishes a personal linguistic baseline. The unit of analysis is the *dyad-hour*: a poster X is exposed at time t to poster Y's recent post; does X's writing in the next 72 hours shift toward Y's register more than would be predicted by X's own trajectory and the forum's contemporaneous drift? A claimant-encounter event is identified by external markers — mentions of specific case-management interactions, tribunal dates, sanction notices — and validated by a human-coded subsample.

*Rationale:* This drops the individual-as-unit constraint. The political economy literature on welfare politics treats individual attitudes as primary; the qualitative literature treats individual self-concept as primary; nobody asks whether stigmatising welfare encounter has a *contagion structure* — whether one claimant's identity disorganisation propagates linguistically through the community in ways that compound the institutional damage. If it does, the policy implication is enormous: the dignity cost of one bad encounter is not bounded by the individual who experienced it. This is the kind of finding that gets a paper out of comparative welfare studies and into general-interest political science, because it reframes welfare design as a public-goods problem rather than a transaction. Networks are exactly the unit where computational text wins over Likert scales — surveys can never see this.

---

**3. The Four-Regime Parallel Corpus: Same Life Event, Four Welfare Architectures, Translated Synthetic Twins**

*Question:* Holding the underlying life event constant (job loss followed by first contact with the welfare state), does the linguistic register of claimant narratives differ systematically across Nordic, Continental, Liberal, and Southern welfare regimes in ways that map onto the institutional features the political economy literature attributes to those regimes?

*Setting:* A four-country parallel corpus combining (a) tribunal appeal letters and welfare-rights organisation archives in Sweden, Germany, the UK, and Italy, scraped from publicly accessible legal databases and FOI'd from welfare-rights NGOs; (b) for each country, 200 semi-structured first-encounter narratives elicited through partnership with two welfare-rights organisations per country; (c) LLM-translated parallel versions of each narrative into a common pivot language for cross-regime linguistic comparison, with human translators auditing a stratified subsample. The unit is the *narrative-encounter-regime* triplet. The empirical strategy is a regime × encounter-type interaction on standardised linguistic agency indices, with the LLM translation step explicitly validated against human translation for the markers being measured (a methods contribution in itself).

*Rationale:* This drops the single-language / single-country constraint that has made computational welfare-self-concept work impossible at scale. The Esping-Andersen typology and its descendants make sharp predictions about how welfare encounter should differ across regimes — Nordic universalism should produce rights-talk register, Liberal means-testing should produce supplicant register, Southern familialism should produce shame-deflection register. Nobody has tested these predictions on text because nobody has built the parallel corpus. The LLM-translation step is what makes it newly possible: cross-language linguistic markers are computable to a usable approximation as of 2024-25, and the validation literature is mature enough that referees won't reject on translation grounds if the audit is documented. This is an *APSR* / *Comparative Political Studies* paper if it works — direct empirical test of the central institutional claim in the welfare-state-politics canon.

---

## What you'd need to do this

**Angle 1 (Counterfactual Claimant Experiment):**
- *Data:* Prolific UK panel access, screening to current/recent UC, ESA, PIP claimants; pre-registration on OSF; IRB approval at UCPH or via PhD-host institution.
- *Method:* Within-person fixed-effects regression on linguistic markers; pre-registered analysis plan; multiple-comparisons correction across markers; manipulation checks for framing comprehension.
- *Partnerships:* A welfare-rights advisor at Citizens Advice or Z2K for ethical framing of prompts; one computational-linguistics co-author to validate the agency-marker construct.
- *Time horizon:* 8 months data collection, 4 months analysis. Realistic as a PhD chapter 2 (year 2-3 of the programme).
- *Cost:* £18,000-25,000 in Prolific incentives; one round of funding application (ESRC PhD enrichment, Leverhulme).

**Angle 2 (Linguistic Contagion Network):**
- *Data:* r/UniversalCredit + Mumsnet scrapes (legal under research-use exceptions but requires a careful ToS and ethics path); username persistence verification; human-coded subsample (~2,000 posts) for event-marker validation.
- *Method:* Dyad-level diffusion models with poster and time fixed effects; placebo tests on non-welfare subreddits matched on demographics; sensitivity to spillover assumptions à la Aronow & Samii.
- *Partnerships:* One quant-soc collaborator with social-network econometrics chops (LSE Methodology, Oxford Internet Institute); ethics consultation given that posters are identifiable across platforms even if anonymous on each.
- *Time horizon:* 12-15 months. The data collection is the slow part; the analysis is fast. Realistic as a thesis core chapter (chapter 3).
- *Cost:* Low — mostly compute. Storage and a server for the corpus.

**Angle 3 (Four-Regime Parallel Corpus):**
- *Data:* Tribunal/legal databases in four countries (Bundessozialgericht for Germany, First-tier Tribunal for the UK, equivalents in Sweden and Italy); welfare-rights NGO partnerships in each country (these need to be lined up early — they are the binding constraint); 800 elicited narratives across the four countries.
- *Method:* Pre-registered cross-regime hypothesis tests; LLM translation pipeline with documented validation against human translators on the specific linguistic markers; bootstrap confidence intervals clustered at narrative level.
- *Partnerships:* One political-economy senior co-author with welfare-state credentials (someone in the Iversen / Häusermann / Gingrich orbit); four NGO data-access agreements; one comparative linguist or NLP-methods co-author.
- *Time horizon:* 24-30 months from first contact. This is the entire dissertation if it works. The NGO partnership lead-time alone is 6 months.
- *Cost:* £40,000-60,000 incl. translation audit, fieldwork travel, LLM API. A serious funding application — Open Society, Joseph Rowntree, possibly an ERC Starting Grant adjacent path for a postdoc.

---

## Closest existing literature

**Angle 1:**
- Pennebaker et al., expressive-writing paradigm (1990s-2010s) — established that prompted writing produces measurable linguistic markers tied to psychological state; provides the methodological precedent for treating elicited text as causally informative.
- Mutz & Reeves on experimental priming in political communication (mid-2000s onward) — the closest political-science analogue to manipulating frame-then-measure-response.
- Boyd, Ashokkumar, et al. on LIWC-style linguistic markers for psychological state (2010s-2020s) — provides validated measurement instruments for the agency-marker construct.

**Angle 2:**
- Bail, Argyle, and the Polarization Lab at Duke (late 2010s-present) — closest existing programme on networked linguistic and attitudinal contagion in online political communities.
- Centola's experimental network diffusion work (2010s) — provides the identification template for distinguishing contagion from homophily.
- Wagner (2022) and Patrick (2016) on welfare-encounter qualitative narratives — the substantive theoretical anchor; this work would be the quantitative network extension of their individual-level claims.

**Angle 3:**
- Esping-Andersen (1990), Ferrera (1996), and the welfare-regime typology canon — the predictions being tested.
- Brady, Beckfield, Jäntti, et al. on cross-national welfare-attitudes work (2000s-2010s) — closest existing comparative-welfare empirical programme, but on attitudes not text.
- Roberts, Stewart, et al. on structural topic models cross-language (2010s-present) — the methodological precedent for cross-language computational text analysis at this scale.

---

## Why someone smart would dismiss this

The senior critic's strongest objection is identification across all three angles, but it bites hardest on Angle 2: the linguistic-contagion design cannot cleanly separate genuine contagion (X is influenced by Y's register) from homophily (X and Y both belong to a sub-community whose register is shifting for an unmeasured external reason — a sanctions wave, a policy announcement, a viral news story about a claimant death). The standard fix — exogenous shocks to who X is exposed to — is unavailable on forums where exposure is endogenous to X's interests. Centola-style experimental networks fix this; observational ones don't. A referee at AJPS would write "the contagion estimate is upward-biased by unmeasured community-level shocks correlated with both exposure and outcome" and that would be that. Angle 3 has an analogous problem at the regime level (regimes differ on dozens of things besides welfare design, so any cross-regime linguistic difference is over-identified). Angle 1 escapes the identification critique but invites a different one — that elicited writing under a research prompt is not the same construct as spontaneous writing during a real encounter, and the experimental finding may not externally validate to the institutional setting it is supposed to illuminate. The honest answer is that the strongest version of this research programme triangulates all three: the experiment for clean identification, the corpus for ecological validity, the cross-regime for institutional variance — and that no single paper carries the full claim. That is a dissertation-scale answer, not a paper-scale one, and it is the right answer.

</details>
