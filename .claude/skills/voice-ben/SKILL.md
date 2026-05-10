---
name: voice-ben
description: Write in Ben Smart's authentic academic register. Use when drafting or revising any prose that will appear under his name — papers, essays, blog posts, abstracts, intros. Calibrated against three pre-AI writing samples (Global Media 2017, Politicians and Twitter 2017, Newspaper Representations of Homelessness 2018) and confirmed by the GPT Zero 100% → 60% human transition on 2026-04-25.
disable-model-invocation: false
allowed-tools: ["Read", "Grep", "Edit", "Write"]

# Deterministic voice spec — consumed by /voice-audit and used as authoritative reference for voice-ben
banned_vocabulary:
  - delve
  - dive into
  - navigate              # only figurative use; literal navigation is fine
  - underscore
  - bolster
  - harness
  - leverage              # only general use; "regression leverage" is a technical exception
  - unpack
  - shed light on
  - pave the way
  - pivotal
  - groundbreaking
  - cutting-edge
  - transformative
  - game-changing
  - innovative
  - comprehensive
  - seamless
  - intricate
  - vibrant
  - multifaceted
  - holistic
  - testament
  - landscape             # only figurative; "policy landscape" banned, "the landscape east of London" fine
  - realm

banned_vocabulary_exceptions:
  # Voice-calibrated keeps. These appear in pre-AI samples or methodological contexts.
  - foster                # appears in Global Media 2017; Ben uses it
  - robust                # methodological sense only ("robust across specifications")
  - nuanced               # banned as empty praise; allowed when it carries genuine technical meaning

banned_phrases:
  - "In today's [fast-paced/rapidly evolving/digital] world"
  - "It's important to note that"
  - "It's worth noting that"
  - "One of the most"
  - "When it comes to"
  - "At its core"
  - "At the end of the day"
  - "This is where X comes in"
  - "Let's break it down"
  - "Plays a crucial role in"
  - "It cannot be overstated"
  - "underscoring the importance of"
  - "highlighting the need for"
  - "reflecting a broader trend toward"
  - "marking a significant shift in"

banned_structures:
  - "It's not just X — it's Y"
  - "Not only X, but Y"
  - "This isn't about X. It's about Y."
  - "No X. No Y. Just Z."
  - "What X is, is Y"
  - "X is fundamentally Y"
  - "What makes X X is Y"

banned_punctuation:
  em_dash:
    rule: "selective_use"
    target: "fewer than 8 per 1000 words"
    rationale: "Em-dashes appear in Ben's pre-AI samples but only sparingly. Default to semicolons; reserve em-dashes for inline negation, mid-sentence list framing, and citation pauses where a semicolon would feel anaemic. Avoid em-dash apposition stacking back-to-back."
  oxford_comma:
    rule: "no_constraint"
    rationale: "Voice samples are inconsistent; do not enforce either way."
  hyphen_clause_break:
    rule: "positive_signature"
    target: "expected 1-3 per 1000 words in modern (post-2019) prose; rare in pre-2019 samples"
    rationale: "Ben adopted ` - ` (space-hyphen-space) as a clause-break around 2019 and uses it deliberately. In Origins it appears at ~2.4/1000 words. Do NOT normalise to `—`; do NOT flag as a violation. When writing in Ben's voice, use this hyphen pattern in place of em-dashes for inline appositions and clause breaks. Confirmed pattern; not an artifact."

required_transitions:
  # Corpus-verified against 22,167 words of pre-AI Ben prose (May 2026 calibration).
  # Counts shown in parentheses. Deploy at least 5 per 1000 words in argumentative prose.
  high_frequency:
    - "Indeed,"                                  # 28 occurrences — the dominant transition
    - "Essentially,"                             # 14 — second-most-common; often paragraph-closer
    - "However,"                                 # 13
    - "Hence,"                                   # 11
    - "Effectively,"                             # 11
    - "Consequently,"                            # 12
    - "Ultimately,"                              # 10
    - "Furthermore,"                             # 8
    - "Thus,"                                    # 7
    - "Similarly,"                               # 6
    - "Conceptually,"                            # 5
    - "In contrast,"                             # 4
    - "Accordingly,"                             # 4
    - "Arguably,"                                # 3
    - "Correspondingly,"                         # 3
    - "Contrastingly,"                           # 3 — Ben uses this in place of "By contrast" / "Conversely"
    - "In this sense,"                           # 3
    - "Importantly,"                             # 2
    - "Moreover,"                                # 2
    - "Primarily,"                               # 2
  citation_framings:
    # Confirmed in corpus — full read, not just grep
    - "Supporting this theory,"                  # 6 — formulaic citation lead-in
    - "Corroborating this idea,"                 # 5 — variant: "Corroborating the existence of..."
    - "This view is consistent with"             # 2
    - "Building on [framework / Author's work],"  # 2
    - "[Author] (YEAR p.NN) argues that..."      # ~30+ — dominant citation form
    - "[Author] (YEAR p.NN) suggests that..."    # 26+
    - "[Author] (YEAR p.NN) contends that..."    # 14+
    - "[Author] (YEAR p.NN) outlines how/that..." # 12+
    - "[Author] (YEAR p.NN) claims that..."      # 10+
    - "[Author] (YEAR p.NN) notes that..."       # several
    - "[Author] (YEAR p.NN) posits that..."      # 2 (Origins)
    - "For [Author], [claim]."                   # 14+ — SIGNATURE topical-attribution pivot
    - "According to [Author/Source],"            # 4+
    - "As [Author] argues/suggests/contends/notes/outlines,"  # 8+ — "As Mendes contends"; "As Pearson et al. suggest"
    - "As outlined by [Author],"                 # 2
    - "Following [Author]'s [proposition/work],"  # 1 (Origins) — gerund-opener variant
    - "Expanding on [Author]'s work,"            # 1 (Origins)
    - "Utilizing [Author]'s concept of [X],"     # 1 (Origins)
    - "Through the perspectives of [Author],"    # 1
    - "Such perspectives undergird [Author]'s contention"  # 1 — distinctive variant
    - "As trumpeted by [school/authors],"        # 1 — distinctive
    - "Whilst [Author] (YEAR) suggests X, Y"     # concessive citation lead-in
    - "(Author1 YEAR pNN; Author2 YEAR pNN; Author3 YEAR pNN)"  # signature: stacked parenthetical citations, often three deep
  argument_pivots:
    - "yet"                                      # mid-sentence pivot, comma + yet + clause; preferred over em-dash
    - "Yet" (sentence-initial)                   # 2 — "Yet by exploring..."; "Yet while there is significant power..."
    - "Whilst X, Y"                              # 7 — Ben uses "whilst" 7:1 over "while"
    - "Although X, Y"                            # 5+ — concessive
    - "Despite X, Y"                             # 2 (Origins) — concessive opener
    - "Rather than [X], [Y]"                     # 2+
    - "Instead, [main claim]"                    # 3+
    - "Through this perspective,"                # 4
    - "Through such perspectives,"               # 3 — variant
    - "Through this {framework / lens / norm-inducing perspective / theoretical lens},"  # 4 family
    - "Through application to [X],"              # 1 — gerund-opener
    - "This perspective directs our attention to" # 3 — distinctive bridging move
    - "This is exemplified by"                   # 5
    - "Central to {our study / this theory / much of this work},"  # 4
    - "Core to our discussion is"                # 1 (Origins) — variant
    - "At the core of [X] is"                    # 1
    - "Of central concern for [Author] is that"  # 1
    - "At a fundamental level,"                  # 2
    - "At a more fundamental level,"             # 1 — variant
    - "At their core,"                           # 2
    - "A particular issue at stake here is"      # 1
    - "These critiques are correct, yet are not central to"  # 1 — granted-then-narrowed move
  in_x_openers:
    # Family of "In X," / "Within X," / "Under X," structural sentence-openers (~30+ combined)
    - "Within this,"                             # 3
    - "Within [the discourse surrounding...],"   # 1
    - "In particular,"                           # 2
    - "In a traditional sense,"                  # 1
    - "In a context of [X],"                     # 1
    - "In an Australian context,"                # 1
    - "In a definitional sense,"                 # 1
    - "In their case,"                           # 1
    - "In their response,"                       # 1
    - "In light of these findings,"              # 1
    - "In the past decade,"                      # 1
    - "In the eyes of [X],"                      # 1
    - "In the extreme,"                          # 1
    - "In the short-term,"                       # 1
    - "In this regard,"                          # 1
    - "In this perspective,"                     # 1
    - "In this respect,"                         # 1
    - "In this context,"                         # 1
    - "In this sense,"                           # 3
    - "In terms of [X],"                         # 4+
    - "In order to [X],"                         # 2+ — purpose-clause opener
    - "From a [psychological / grounded] perspective,"  # 2+
    - "From the perspective of [Author],"        # 1
    - "From this perspective,"                   # 1
    - "Under [equalisation / monitorial / supply] perspective,"  # 3+
    - "Under the guise of [X],"                  # 1 (Origins)
  gerund_openers:
    # Subordinate-clause sentence-starts (distinctive in academic prose)
    - "Building on [framework / contributions],"  # 2
    - "Drawing on [Author]'s work,"              # rare
    - "Following [Author]'s proposition,"        # 1
    - "Expanding on [Author]'s work,"            # 1
    - "Utilizing [framework / concept],"         # 1
    - "Using [method / framework],"              # 2
    - "Equipped with [X],"                       # 1
    - "By [X-ing],"                              # 4+ — "By focusing the research on..."; "By examining..."; "By acknowledging..."; "By critically examining..."
    - "Through [X-ing],"                         # 1+ — "Through an examination of..."
    - "Through a utilisation of [X],"            # 1
    - "Highlighting [X] is..."                   # 1
    - "Resonating with [X],"                     # 1 (Origins)
  enumeration:
    - "Firstly / Secondly / Thirdly"             # confirmed in pre-AI; NEVER First/Second/Third
  signature_phrasing:
    - "undergirding [much of this literature] is..."  # 2 — high-perplexity-breaking when used
    - "the architecture of [X]"                  # 8 — recurring noun-phrase pattern

distinctive_vocabulary:
  # CORPUS-VERIFIED (May 2026 — counts across 7 pre-AI essays, 22,167 words).
  # All entries below have count >= 2 in the corpus.
  # Items that scored 0 in the corpus check (valorises, instigates, inveigle, obsequious,
  # avaricious, concomitant, incipient, pertinacity, progenitor, configurations, etc.) have
  # been removed — they were AI-extrapolated, not voice-calibrated.
  verbs:
    - frame                       # 22 — the highest-frequency verb family (frame/frames/framing/framed)
    - reinforces                  # 12
    - facilitates                 # 11
    - exemplifies                 # 9 (also exemplified, exemplifying)
    - legitimises                 # 7 (also legitimation, legitimising) — British -ise spelling
    - generates                   # 6
    - excludes                    # 6
    - harnesses                   # 5
    - characterises               # 5 — British -ise spelling
    - augments                    # 5
    - undermines                  # 4
    - problematises               # 4
    - perpetuates                 # 4
    - contests                    # 4
    - depicts                     # 3
    - incites                     # 3
    - exacerbates                 # 3
    - valorises                   # 3 — paired often with "moralisation" (Origins essay)
    - mediates                    # 2
    - instigates                  # 2
    - fortifies                   # 2
    - advocates                   # 2
    - embeds                      # 3 (also embedded as adj.)
    - construct / constructs      # several — "constructing particular realities"
    - reshape / reshaped          # 3+ (Origins)
    - reproduce / reproduces      # 3+ (Origins)
    - compose / composes          # 1 — "these categories compose the homeless..."
    - augments                    # 5+ — also "augmentation"
    - disseminates                # 7 (also as noun "dissemination")
    - obscures                    # 1 (Origins) — "obscures the moral choices"
    - circumscribes               # 1 — "circumscribe the spread"
    - entrenches / entrenched     # 1 (Origins) — "entrenching the idea"
    - imbues / imbued             # 1 (Origins) — "imbued with bureaucratic expertise"
    - dictates                    # 1 — "discursive effects dictate the parameters"
    - delegitimises / delegitimized # 1 (Origins)
    - proliferates / proliferating # 1 — "further proliferating societal fragmentation"
    - aggravates                  # 2+ — "aggravates partisan hostility"
    - infringes / infringing      # 1 — "infringing on democratic liberal ideals"
    - reinvigorates               # 1 — "predicted to reinvigorate deliberative democracy"
    - incites                     # 3 — "incites collective decision-making"
    - reconfigures                # 1 — "reconfigure their participation"
    - excises                     # 1 — "excises contradicting and dissenting voices"
    - dismantles                  # 1 (Origins)
    - naturalises / naturalized   # 1 (Origins)
    - internalises / internalized # 1 (Origins)
    - marketizes / marketized     # 1 (Origins)
    - stigmatises / stigmatization # 1 (Origins)
    - valorises / valorized       # 3
    - propagates / propagating    # 1 — "propagating favourable misinformation"
  citation_verbs:
    # Dominant verbs Ben uses to attribute claims (count across corpus):
    # argues (22) / argue (... ) / contend (9) / contends (5) / outlines (7) / outline (4)
    # claims (7) / claim (3) / suggest (14) / suggests (12)
    # Prefer these over "says", "states", "writes", "finds".
    - argues
    - contends
    - outlines
    - claims
    - suggests
    - notes
  adjectives:
    - civic                       # 18
    - dominant                    # 12
    - fundamental                 # 11 (also "fundamentally")
    - inherent / inherently       # 17 + 11
    - normative                   # 9
    - hierarchical                # 6 (also "non-hierarchical" x3)
    - contemporary                # 6
    - technocratic                # 5
    - structural                  # 6
    - partisan                    # 5
    - participatory               # 5
    - ideological                 # 9
    - polarising                  # 5
    - homophilous                 # 4
    - unconstrained               # 4
    - heterogeneous               # 4
    - contested                   # 4
    - disunifying                 # 3
    - unmediated                  # 3
    - sociotechnical              # 3
    - pluralistic                 # 3
    - non-hierarchical            # 3 — note hyphenated compound
    - instrumental                # 3
    - egalitarian                 # 3
    - spreadable                  # 2
    - polemical                   # 1 — kept for theory-section availability
    - factitious                  # 1
    - acrimonious                 # 1
    - performative                # 1 — appears in Origins essay only
    - hegemonic                   # 2
  nouns:
    - discourse                   # 31 (+ discourses 18 — total 49)
    - sphere / spheres            # 22 (+ public sphere)
    - values                      # 22
    - framework                   # 15
    - paradigm                    # 9
    - formations                  # 9 (paired with "formation")
    - architecture (of X)         # 8 — pattern: "the architecture of [X]"
    - infrastructure              # 8
    - constituents                # 8
    - stakeholders                # 8
    - logic / logics              # 7
    - ideologies                  # 7
    - dissemination               # 7
    - rhetoric                    # 6
    - narratives                  # 6
    - factions                    # 6 — distinctive choice over "groups"
    - diffusion                   # 6
    - construction                # 6
    - affordances                 # 5 — theory-marker (technology / Web 2.0 register)
    - manifestations              # 4
    - fragmentation               # 4
    - mechanisms                  # 4
    - agency                      # 4
    - dichotomy / dichotomies     # 3
    - dynamics                    # 3
    - undergirding                # 2

negative_space:
  # Words that SOUND like Ben's register but are NOT in his pre-AI corpus (zero hits in 22k words).
  # Do NOT use these as voice signals — they are LLM-default theory vocabulary, not Ben's.
  - hegemony
  - ethos
  - milieu
  - valence
  - imaginary
  - imaginaries
  - assemblage
  - ensemble
  - terrain
  - cleavage
  - conjuncture
  - edifice
  - ecology (figurative)
  - configuration  # appears as plural "configurations" 0 times — even though it sounds Ben-like
  - inveigle
  - obsequious
  - avaricious
  - concomitant
  - incipient
  - pertinacity
  - progenitor
  - elucidates
  - presupposes
  - promulgates
  - internalizes
  - propagates    # 0 hits despite being seeded — verify before using

british_spelling_preference:
  # Pre-AI samples consistently use British -ise/-isation forms in 2017-2018 essays;
  # the 2024-vintage Origins essay shifts to mixed -ize/-ization. Default to British -ise.
  - "polarisation NOT polarization (default)"
  - "characterise NOT characterize (default)"
  - "legitimise NOT legitimize (default)"
  - "marginalise NOT marginalize (default)"
  - "valorise NOT valorize (default)"

sentence_rules:
  default_length_words: "25-40 in argumentative prose"
  long_sentence_acceptable: true     # 67-word opening sentence in Global Media essay
  max_em_dashes_per_sentence: 1
  no_em_dash_apposition_stacking: true
  prefer_semicolon_over_em_dash: true
  embed_citations_mid_sentence: true
  first_person_commitment_explicit: false  # Ben's stated preference (2026-05-10): avoid first-person.
                                           # Pre-AI corpus has 0 "I"; the "I argue / I suggest" instances are Origins-only (post-AI drift).
                                           # Prefer third-person paper-as-agent: "this paper argues", "the analysis shows", "our research".
  short_sentence_share: "20-30%"           # sentences under 8 words
  slight_grammatical_roughness_acceptable: true
  no_throat_clearing_openers: true
  no_definitional_templates: true          # "What X is, is Y" forbidden

structural_rules:
  first_sentence_states_the_claim: true
  no_buried_thesis_in_paragraph: true
  no_grand_opening_world_state: true       # Don't open with "In today's..." or sweeping context
  no_summary_inspirational_close: true     # Start and end on substance
  no_question_restatement: true            # Don't restate the question before answering
  no_bold_term_explanation_lists: true     # "**Term:** explanation" pattern is the #1 AI tell
  vary_paragraph_and_sentence_length: true
  no_signposting: true                     # No "Let's explore..." / "Now let's turn to..."

quote_integration:
  intro_theory_quote_share: "15-25% of words as direct quotes"
  pattern: "paraphrase → direct quote → one-sentence commentary → next claim"
  block_quotes_acceptable: true
  always_include_page_numbers: true

diagnostic_targets:
  em_dashes_per_1000_words: "<8"
  mid_sentence_colons_per_1000_words: "<8"
  semicolons_per_1000_words: "5-12"
  short_sentence_share: "20-30%"
  banned_words_count: 0           # excepting banned_vocabulary_exceptions
  what_x_is_constructions: 0
  ben_transitions_per_1000_words: ">=5"
  first_person_singular_per_1000_words: "<0.5"   # Hard cap; pre-AI corpus is at 0.0
  first_person_plural_per_1000_words: "<3"        # "our research", "our study" are fine; "we find" sparingly

voice_calibration_sources:
  # Anchor priority confirmed 2026-05-10. Higher priority = greater calibration weight when
  # samples disagree (e.g., Origins shifted to American spellings via a ChatGPT spell-check pass;
  # ignore that drift, prefer the British -ise of older essays).
  primary:
    - "manuscripts/Writing Samples/Ben Smart - Final Essay - Global Media.docx"   # 2017, 3544w; 8 of 12 distinctive moves in lexicon source here
  secondary:
    - "manuscripts/Writing Samples/Newspaper representations of homeless version - FINAL.docx"   # 2018, 4610w
    - "manuscripts/Writing Samples/Pre-AI Social Media and Democracy.docx"                       # ~2018, 2531w; source of 'granted-then-narrowed' move
    - "manuscripts/Writing Samples/Ben Smart - 759764- Politicians and Twitter.docx"             # 2017, 1601w
    - "manuscripts/Writing Samples/Ben Smart - 759764 - Culture Policy Analysis.docx"            # 3359w
    - "manuscripts/Writing Samples/Pre-AI - Social capital in an online community - Global Media.docx"  # 1920w
  partial:
    # Origins is the most recent (2024) so it captures Ben's post-2019 hyphen-as-em-dash pattern
    # and modern argumentative density. BUT exclude its first-person ("I argue", "I suggest") and
    # American spellings (-ize) — those are AI-edit drift, not Ben's voice.
    - "manuscripts/Writing Samples/Pre-AI/The Origins of Institutional Menus, Power, Performativity and the Rise of Neoliberalism in Australia.docx"   # 2024, 4602w; partial-anchor only
  reference:
    - "manuscripts/Writing Samples/Voice and Writing Style.txt"
    - "manuscripts/Writing Samples/Voice Sample.txt"
    - "manuscripts/Writing Samples/voice_lexicon.md"   # corpus-verified human-readable companion

scope_applies_to:
  # Prose Ben SIGNS — voice-ben triggers automatically
  - "manuscripts/**/*.md"
  - "manuscripts/**/*.tex"
  - "essays/**/*.md"
  - "papers/**/*.tex"
  - "abstracts/**/*.md"
  - "blog/**/*.md"
  - "Cover letters, statements of purpose, op-eds, public-facing prose"

scope_excludes:
  # Internal docs and tutor-style content — voice-ben does NOT trigger
  - "docs/empirical_walkthrough_v1.md"      # tutor doc TO Ben, not FROM him
  - "docs/learning_econometrics/**/*"
  - "MEMORY.md"
  - "STATUS.md / SESSION_REPORT.md / research_journal.md"
  - "quality_reports/**/*"
  - ".claude/**/*"
  - "Code comments, commit messages, internal plans"
  - "Conversational chat replies"

detection_resistance:
  target: "GPT-Zero (primary), GPTZero document scoring"
  acceptable_human_score: ">=60%"
  ceiling_for_ai_edited_ai_prose: "approximately 60% human; for higher, Ben must retype anchor paragraphs"
  successful_anchor_retype_protocol: "Ben types opening + closing paragraphs from memory (file closed). Three retyped paragraphs out of ten typically averages document score down by 30-50 percentage points."

candidate_extensions:
  # Stylistically congruent expansions (added 2026-05-10) — NOT corpus-verified.
  # Deliberate-extension candidates Ben can use for variety beyond Indeed/undergirding.
  # Future /voice-audit upgrade should treat these as half-weight matches in transition
  # density. Once Ben publishes prose using one and the calibration corpus refreshes,
  # the candidate graduates to a corpus-verified entry above.
  conviction_openers:
    - "Tellingly,"                # Indeed-family; symptom-of-larger-pattern
    - "Strikingly,"               # foregrounds unexpected pattern
    - "Pointedly,"                # signals sharpness
    - "Revealingly,"              # softer Tellingly
    - "Symptomatically,"          # diagnostic-of-structure
    - "Aptly,"                    # citation-fits-with-precision
    - "Critically,"               # stronger than Importantly
    - "Pertinently,"              # tight-connection-to-prior
    - "Fittingly,"                # resolves-prior-tension
    - "Notably,"                  # neutral foregrounder
    - "It is no accident that"    # structural-not-incidental marker
  emphasis_pivots:
    - "More fundamentally,"
    - "More tellingly,"
    - "More acutely,"
    - "More consequentially,"
    - "More revealing still,"
    - "Of greater consequence,"
    - "The deeper point is that"
  concessive_alternatives:
    - "Granted X, Y"              # tighter than Whilst
    - "For all that,"             # post-concession pivot
    - "Even granting X, Y"
    - "X may hold, but it does not follow that Y"
    - "X is true as far as it goes; what it misses is Y"
    - "One might object that X — yet"
    - "It is fashionable to say that X; the more careful claim is Y"
  theoretical_frame_openers:
    - "Read in this register,"
    - "Seen this way,"
    - "On this reading,"
    - "Construed this way,"
    - "Within this frame,"
    - "Recast in these terms,"
    - "Cast in [Author]'s terms,"
    - "Translated into [framework] vocabulary,"
    - "Refracted through [lens],"
    - "Approached through [lens],"
    - "Read against [comparator],"
  focus_phrases:
    - "The animating question is"
    - "The load-bearing claim is"           # extends architecture-of-X family
    - "The decisive move is"
    - "The crucial move is"
    - "What does the work of [X] is"        # multi-word signature
    - "What earns [X] its keep is"
    - "At the heart of [X] sits"
    - "The genuine novelty lies in"
    - "The structural insight is that"
    - "What renders [X] coherent is"
  synthesis_alternatives:
    - "The upshot is"
    - "Taken together,"
    - "All told,"
    - "In sum,"
    - "The cumulative effect is"
    - "The picture that emerges is"
    - "What survives this scrutiny is"
    - "The argument resolves into"
    - "The thread that runs through these is"
    - "The corollary is"
  hedge_alternatives:
    - "Plausibly,"
    - "Defensibly,"
    - "Provisionally,"
    - "It is at least arguable that"
    - "A defensible reading is that"
    - "There is reason to think that"
    - "A more cautious framing would be"
  citation_alternatives:
    - "In [Author]'s reading,"
    - "On [Author]'s account,"
    - "Per [Author],"
    - "After [Author] (YEAR),"
    - "In the spirit of [Author],"
    - "Following the lead of [Author],"
    - "Working in [Author]'s vein,"
    - "[Author]'s account turns on"
    - "[Author]'s contribution is to argue that"
  candidate_verbs:
    - crystallise
    - coalesce
    - delineate
    - render
    - entrench
    - inscribe
    - sediment
    - dislodge
    - destabilise
    - unsettle
    - rupture
    - expose
    - lay bare
    - militate against
    - cut against
    - evince
    - manifest
    - bear witness to
    - attest to
    - bespeak
    - refract
    - inflect
    - modulate
    - attenuate
    - amplify
    - temper
    - channel
    - enshrine
    - vindicate
    - anchor
    - underwrite
    - ground
  candidate_adjectives:
    - constitutive
    - conjunctural        # ⚠ overlaps with negative_space — conscious adoption only
    - recursive
    - emergent
    - relational
    - mediated
    - contingent
    - overdetermined
    - sedimented
    - dispositional
    - generative
    - iterative
    - decisive
    - consequential
    - load-bearing
    - foundational
    - pervasive
    - abiding
    - enduring
    - durable
    - recalcitrant
    - intractable
    - corrosive
    - erosive
    - attritional
    - punitive
    - coercive
  candidate_nouns:
    - nexus
    - entanglement
    - terrain
    - topography
    - lattice
    - circuitry
    - machinery
    - apparatus
    - choreography
    - repertoire
    - grammar
    - lexicon
    - syntax
    - idiom
    - enactment
    - iteration
    - transmission
    - inheritance
    - residue
    - accretion
    - disjuncture
    - ambit
    - horizon
    - register
    - timbre
    - texture
    - contour
    - threshold
  multiword_constructions:
    # Compact phrasing that does argumentative work without single-word reach
    - "what does the work of [X] is"
    - "what earns [X] its keep is"
    - "the load-bearing claim is"
    - "turns on"
    - "consists in"
    - "lies in"
    - "comes down to"
    - "cashes out as"
    - "amounts to"
    - "renders [X] visible / invisible"
    - "is constitutive of"
    - "is parasitic on"
    - "is hostage to"
    - "is a function of"
    - "does the work of [X]"
  candidate_extensions_note: "Use deliberately, not as default cadence. Pair each new word with a familiar anchor. Earn metaphors. Default to corpus-verified entries when in doubt. ⚠ items overlap with negative_space — conscious adoption only."

last_recalibrated: "2026-05-10"
calibration_history:
  - "2026-04-25: initial calibration from three pre-AI samples; 100% AI -> 60% human after quote-mosaic intro restructure"
  - "2026-05-08: em-dash rule revised from 'eliminated' to 'selective use, <8 per 1000 words' after v4 voice pass over-corrected to zero and lost rhythm"
  - "2026-05-10: full corpus extraction across 7 pre-AI essays (22,167 words). Removed AI-extrapolated vocabulary that scored 0 in corpus (valorises in pure form, instigates, inveigle, obsequious, avaricious, concomitant, incipient, pertinacity, progenitor, configurations, elucidates, presupposes, promulgates). Added corpus-verified items including: 'Essentially,' (14), 'Corroborating' (5), 'Supporting this theory,' (6), 'This is exemplified by' (5), 'Whilst X, Y' (7 occurrences, 7:1 over 'while'), the 'Through this perspective' family (9 across variants). Negative-space list added to prevent future LLM drift toward hegemony/ethos/milieu/assemblage/conjuncture vocabulary that sounds-like-theory-but-isn't-Ben."
  - "2026-05-10 (later): added candidate_extensions section — stylistically congruent expansions for variety beyond Indeed/undergirding monotony. NOT corpus-verified; deliberate-adoption candidates only. Includes 11 conviction-openers, 7 emphasis pivots, 7 concessive alternatives, 11 theoretical-frame openers, 10 focus phrases, 10 synthesis closers, 7 hedge variants, 9 citation alternatives, 32 verbs, 27 adjectives, 28 nouns, 15 multiword constructions. Future /voice-audit upgrade should weight these as half-strength matches; corpus-verified entries above remain canonical."
---

# Voice — Ben Smart

> The frontmatter above is **canonical** — `/voice-audit` reads it as deterministic input. This body is **rationale and examples** for human readers. When updating the spec, edit the frontmatter; do not narrate updates in this body.

## When this skill applies

Any task that produces prose Ben will sign his name to (see `scope_applies_to` in the frontmatter). Specifically: paper drafts, abstracts, introductions, discussion sections, essays, op-eds, blog posts, email drafts on academic topics, cover letters, statements of purpose.

This skill does NOT apply to internal docs, code comments, planning documents, tutor-style materials TO Ben, conversational chat replies, or anything in `scope_excludes`. The scope decision lives in `~/.claude/projects/.../memory/feedback_voice_skills_scope.md`.

## Pre-AI sample summary

Three pre-AI samples calibrate this voice (see `voice_calibration_sources`). They reveal:

- **Long compound sentences are the default.** 25-40 words is normal; 67 words is the opening of the Global Media essay.
- **Heavy semicolons, sparing em-dashes.** Em-dashes appear in the 2018 Newspaper Representations sample but never as default cadence punctuation.
- **Citations embedded mid-sentence**, often stacked: `(Sunstein 2007 p.19; Van Aelst et. Al 2017 p.13; Wojcieszak 2010 p.636)`.
- **Avoid first-person; the paper is the agent.** Pre-AI corpus has zero "I" across Global Media, Politicians and Twitter, and Newspaper Representations. The "I argue / I suggest / I aim" instances in the lexicon are Origins-only and reflect post-AI drift. Use "this paper argues", "the analysis shows", "our research / our study"; reserve "we" for genuine multi-author work or sparingly as editorial-we, not as default voice.
- **Distinctive vocabulary:** Ben reaches for `homophilous`, `factitious`, `polemical`, `undergirding`, `valorises`, `disunifying` — words LLMs typically avoid.
- **Slight grammatical roughness is real.** Subject-verb spreads, occasional awkward clause stacks. Don't over-smooth.

## Anti-pattern catalogue

Concrete bad-prose examples Ben has flagged. Each has a concrete rewrite.

### Anti-pattern 1: Smooth definitional opener

> Bad: *"What welfare says, I argue, is the mechanism."*
> Why it fails: "What X is, is Y" is an LLM tic. The claim is fine; the structure is wrong.
> Rewrite: *"Welfare communicates, and that communication is the mechanism."*

### Anti-pattern 2: Bolded sub-claim parallelism

> Bad: Three bolded headers like **Stage one: identity switching.** **Stage two: misattribution.** **Stage three: defensive othering.**
> Why it fails: Wikipedia-AI scaffolding. Ben's pre-AI writing uses inline "Firstly... Secondly... Thirdly..." in flowing prose.
> Rewrite: Convert to inline prose: "Firstly, identity switching does X; secondly, misattribution does Y; thirdly..."

### Anti-pattern 3: "It is X. It is Y." flat sequencing

> Bad: *"The damage mechanism is legible. The protective one is not."*
> Why it fails: Too clean, too tight. Real Ben prose varies more.
> Rewrite: *"The damage mechanism is legible across every specification this paper presents, while the mirror image on the solidarity side is not detectable."*

### Anti-pattern 4: "I should note that..." preamble

> Bad: *"I should note that the parallel trends assumption may not hold here."*
> Why it fails: Hedge tokens that signal LLM uncertainty.
> Rewrite: Cut the preamble. *"The parallel trends assumption may not hold here."*

### Anti-pattern 5: Em-dash apposition stacking

> Bad: *"Welfare design — the institutional architecture of decommodification — shapes..."*
> Why it fails: Stacked apposition em-dashes (two dashes setting off a single mid-sentence aside) read as default punctuation rather than cadence.
> Rewrite: *"Welfare design, the institutional architecture of decommodification, shapes..."* or *"Welfare design (the institutional architecture of decommodification) shapes..."*

## Canonical strong examples

### Strong Ben sentence (Global Media 2017)

> "The open, decentralised technology of the internet was once promised as the foundation of deliberative democracy that opens up new spaces for political participation and democratic decision-making, yet digital technologies have instead contributed to a society facing increasing political divides in public beliefs and media content, where unregulated and often homophilous networks ultimately undermine deliberative values such as compromise and consensus by increasing political polarization and intergroup hostility (Sunstein 2007 p.19; Van Aelst et. Al 2017 p.13; Wojcieszak 2010 p.636)."

67 words; stacked commas (no em-dashes); three inline citations; *homophilous* and *ultimately undermine* as distinctive verbs; *yet* as an argumentative pivot.

### Strong humanised intro paragraph (asymmetric-welfare paper, post-quote-mosaic pass)

> "Since the foundational contributions of Autor, Levy, and Murnane (2003) on the task-based framework, a robust finding has emerged across comparative political economy that workers in routine-task-intensive (RTI) occupations disproportionately support populist radical right parties (Gingrich 2019; Kurer 2020; Im et al. 2019; Autor et al. 2020; Gallego and Kurer 2022). The pattern is particularly observable in countries with weaker welfare provision (Vlandas and Halikiopoulou 2022; Caselli et al. 2021), leading scholars to argue welfare generosity moderates the relationship between economic vulnerability and exclusionary politics. Indeed, undergirding much of this comparative welfare state literature is Ruggie's (1982) framework of embedded liberalism, in which democratic governments, recognising that economic openness produces losers, provide social protection as compensation, on the assumption that compensation will dampen the political resentment of the dislocated. Effectively, the operative variable is purported to be quantity. Spend more, get less populism."

Five Ben tics in five sentences: *Since the foundational contributions*, *a robust finding has emerged*, *Indeed, undergirding much of...*, *Effectively, the operative variable is purported to be*. This paragraph is the model.

## When voice and detector resistance conflict

Voice wins. Specifically:

- `foster` is on most generic AI-banned lists but appears in Ben's pre-AI Global Media essay. Keep it.
- `robust` is fine in methodological contexts ("robust across specifications") even when generic lists flag it.
- WF says max one em-dash per response; Ben uses them more than that, but selectively. Target <8 per 1000 words, not 0.
- WF says use contractions. Ben's academic prose rarely contracts. Don't force contractions where they break register.

When in doubt, look at what the pre-AI samples actually do. The samples are in `manuscripts/Writing Samples/`.

## Self-check before delivery

1. Read the prose aloud. If a sentence stops you, swap it.
2. Run `/voice-audit <path>` for a deterministic check against the frontmatter.
3. Count em-dashes. If >5 per 1000 words, kill the apposition-stack ones first.
4. Check for at least one block quote (or two-three inline quotes) in any theory-heavy section.
5. Confirm 5+ Ben transitions per 1000 words.
6. Look for hedge stacking ("may be", "could be", "is part of what shapes"). Replace at least one with a flat assertion.
7. If detection resistance matters, confirm the anchor-retype protocol has been applied to opening + closing paragraphs.

## Skill scope clarification

`voice-ben` applies to prose Ben SIGNS. It does NOT apply to:

- Internal docs (plans, notes, MEMORY.md entries, session logs)
- Tutor-style documents addressed TO Ben (e.g., `docs/empirical_walkthrough_v1.md`, `docs/learning_econometrics/01_*.md`)
- Code comments, commit messages
- Conversational chat replies in this session
- Anything under `quality_reports/` (council critiques, ideations, session logs are infrastructure, not prose)

This decision lives in the user's auto-memory at `~/.claude/projects/.../memory/feedback_voice_skills_scope.md`. Don't second-guess it.
