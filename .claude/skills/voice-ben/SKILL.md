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

required_transitions:
  # Deploy at least 5 per 1000 words in argumentative prose
  high_frequency:
    - "Indeed,"
    - "Furthermore,"
    - "Similarly,"
    - "Through this perspective,"
    - "Through these perspectives,"
    - "Conceptually,"
    - "Consequently,"
    - "Effectively,"
    - "Ultimately,"
  citation_framings:
    - "Drawing on [Author]'s work,"
    - "Supporting this theory,"
    - "As articulated by [Author],"
    - "As purported by [Authors],"
    - "From this perspective,"
  argument_pivots:
    - "In contrast to X, Y..."
    - "Hence,"
    - "Thus,"
    - "yet"                # mid-sentence pivot, common in Ben's prose
  enumeration:
    - "Firstly / Secondly / Thirdly"   # NEVER First/Second/Third
  signature_phrasing:
    - "undergirding [much of this literature] is..."

distinctive_vocabulary:
  # LLMs typically avoid these; Ben uses them. Prefer when meaning fits.
  verbs:
    - uncovers
    - fortifies
    - perpetuates
    - instigates
    - internalizes
    - exacerbates
    - propagates
    - valorises
    - legitimates
    - promulgates
    - elucidates
    - presupposes
    - inveigle
  adjectives:
    - homophilous
    - polemical
    - factitious
    - acrimonious
    - polarising
    - disunifying
    - spreadable
    - obsequious
    - avaricious
    - concomitant
    - incipient
  nouns:
    - "architecture (of X)"
    - undergirding
    - configurations
    - dynamics
    - mechanisms
    - pertinacity
    - progenitor

sentence_rules:
  default_length_words: "25-40 in argumentative prose"
  long_sentence_acceptable: true     # 67-word opening sentence in Global Media essay
  max_em_dashes_per_sentence: 1
  no_em_dash_apposition_stacking: true
  prefer_semicolon_over_em_dash: true
  embed_citations_mid_sentence: true
  first_person_commitment_explicit: true   # "I argue", "I find", "I contend"
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

voice_calibration_sources:
  - "manuscripts/Writing Samples/Ben Smart - Final Essay - Global Media.docx"
  - "manuscripts/Writing Samples/Ben Smart - 759764- Politicians and Twitter.docx"
  - "manuscripts/Writing Samples/Newspaper representations of homeless version - FINAL.docx"
  - "manuscripts/Writing Samples/Voice and Writing Style.txt"
  - "manuscripts/Writing Samples/Voice Sample.txt"

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

last_recalibrated: "2026-05-08"
calibration_history:
  - "2026-04-25: initial calibration from three pre-AI samples; 100% AI -> 60% human after quote-mosaic intro restructure"
  - "2026-05-08: em-dash rule revised from 'eliminated' to 'selective use, <8 per 1000 words' after v4 voice pass over-corrected to zero and lost rhythm"
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
- **First-person argumentative commitments are explicit:** "I argue", "I contend", "I take this literally".
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
