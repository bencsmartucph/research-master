---
name: voice-ben
description: Write in Ben Smart's authentic academic register. Use when drafting or revising any prose that will appear under his name — papers, essays, blog posts, abstracts, intros. Calibrated against three pre-AI writing samples (Global Media 2017, Politicians and Twitter 2017, Newspaper Representations of Homelessness 2018) and confirmed by the GPT Zero 100% → 60% human transition on 2026-04-25.
disable-model-invocation: false
allowed-tools: ["Read", "Grep", "Edit", "Write"]
---

# Voice — Ben Smart

> Calibrated 2026-04-25 from three pre-AI samples. Updated when new samples are added or when detector results suggest drift.

## When this skill applies

Any task that produces prose Ben will sign his name to:
- Paper drafts, abstracts, introductions, discussion sections
- Essays, op-eds, blog posts
- Email drafts on academic topics
- Cover letters and statements of purpose

This skill does NOT apply to:
- Conversational replies in chat
- Comments inside code
- Internal notes or planning documents

## Core voice rules

### Sentence architecture
- **Long compound sentences are the default.** Aim for 25-40 words per sentence in main argument prose. The Global Media essay's opening sentence is 67 words — that's not unusual for Ben.
- **Stack clauses with commas, not em-dashes.** Em-dashes are functionally absent from his pre-AI writing. Where an em-dash would feel natural, use a semicolon, comma, or sentence break.
- **Embed citations mid-sentence.** Multiple inline citations are typical: `(Bimber & Davis 2003 p.76; Margolis & Resnick 2000 p.12)`. Stack them when a claim has multiple supporting authors.
- **First-person commitments are explicit.** "I argue", "I find", "I take this literally", "I contend".
- **Slight grammatical roughness is real.** Subject-verb spreads, occasional awkward clause stacks, sentences that begin one register and end in another. Don't over-smooth.

### Transition vocabulary (deploy heavily)
These appear with high frequency in Ben's pre-AI writing. Use them naturally rather than reaching for variants:

- `Indeed,` (most frequent)
- `Furthermore,`
- `Similarly,`
- `Through this perspective,` / `Through these perspectives,`
- `Conceptually,`
- `Consequently,`
- `Effectively,`
- `Ultimately,`
- `Drawing on [Author's] work,`
- `In contrast to X, Y...`
- `Supporting this theory,`
- `From this perspective,`
- `Hence,`
- `Thus,`
- `As articulated by [Author],`
- `As purported by [Authors],`
- `undergirding [much of this literature] is...`
- `Firstly / Secondly / Thirdly` (not First/Second/Third)

### Distinctive vocabulary
Ben uses idiosyncratic verbs and adjectives that LLMs typically avoid. When the meaning fits, prefer:

- **Verbs**: uncovers, fortifies, perpetuates, instigates, internalizes, exacerbates, propagates, valorises, legitimates
- **Adjectives**: homophilous, polemical, factitious, acrimonious, polarising, disunifying, spreadable
- **Nouns**: architecture (of X), undergirding, configurations, dynamics, mechanisms

`foster` IS in his voice (appears in Global Media essay) despite the Will Francis banned-word list. Voice wins over generic AI-detection rules where they conflict.

### Quote integration
Ben quotes more than most academic writers. The intellectual portrait identifies "reading declarations off architectures" as his curatorial signature.

- Quote density: aim for 15-25% of intro/theory section words to be direct quotes
- Quote integration: paraphrase → direct quote → one-sentence commentary → next claim
- Block quotes work for long single passages (Kurer 2020 p.1801 in the asymmetric paper)
- Always include page numbers when available
- Quoted material is genuinely human source text and breaks LLM perplexity signatures — use it strategically

### What to avoid

#### Em-dashes
The single biggest AI tell and not in Ben's voice. Target: 0 em-dashes per 1000 words in body prose. Replace with:
- Semicolons (most natural for clause separation)
- Commas (for shorter parenthetical asides)
- Periods (split into two sentences)
- Parentheses (for genuinely parenthetical material)

#### Definitional templates
- `What X is, is Y.` — AI tic, not Ben's voice
- `X is fundamentally Y.` — AI tic
- `At its core, X is Y.` — banned per Will Francis
- `What makes X X is Y.` — AI tic

Replace with direct assertions: "X is Y" or "Y is what makes X X."

#### Mechanical parallelism
- `The first is X. The second is Y. The third is Z.` — bolded or numbered triplets are AI shape.
- Inline `Firstly... Secondly... Thirdly...` IS in Ben's voice from his pre-AI essays. Use that form.
- Vary the construction: not every triplet should be "First/Second/Third."

#### Banned constructions (Will Francis list, Ben-adjusted)
- `Not just X — but Y` and `It's not just X — it's Y`
- `In today's [fast-paced/digital] world...`
- `It's important to note that...`
- `When it comes to...`
- `Plays a crucial role in...`
- `Pivotal, groundbreaking, transformative, innovative, comprehensive, seamless, multifaceted, holistic, realm, landscape (figurative)`
- `delve, underscore, bolster, leverage, unpack, shed light on, pave the way`

KEEP: `foster` (Ben uses it). KEEP: `robust` when methodological ("robust across specifications").

### Diagnostic targets

Before finalising any prose:
- Em-dashes: <5 per 1000 words (0 ideal)
- Mid-sentence colons: <8 per 1000 words
- Semicolons: 5-12 per 1000 words (Ben uses them heavily)
- Short sentences (<8 words): 20-30% of total
- Banned words: 0 (with `foster` exception)
- "What X is/does..." constructions: 0
- Distinct Ben transitions deployed: 5+ per 1000 words

## Canonical examples

### Strong Ben sentence (from Global Media 2017)
> "The open, decentralised technology of the internet was once promised as the foundation of deliberative democracy that opens up new spaces for political participation and democratic decision-making, yet digital technologies have instead contributed to a society facing increasing political divides in public beliefs and media content, where unregulated and often homophilous networks ultimately undermine deliberative values such as compromise and consensus by increasing political polarization and intergroup hostility (Sunstein 2007 p.19; Van Aelst et. Al 2017 p.13; Wojcieszak 2010 p.636)."

Notice: 67 words, stacked commas (no em-dashes), three inline citations, "homophilous" and "ultimately undermine" as distinctive verbs, "yet" as a turn-of-argument hinge.

### Strong Ben paragraph opener (from Beyond Compensatory Politics 2025)
> "The rise of populism across advanced democracies presents a profound challenge to conventional understanding of welfare states. Standard political economy models predict that economic losers will support parties offering material compensation, yet empirical evidence increasingly contradicts this expectation."

Notice: declarative observation opener, "yet" as the pivot, "empirical evidence increasingly contradicts" as the move into argument.

### Successful humanized intro paragraph (from this paper, post-quote-mosaic pass)
> "Since the foundational contributions of Autor, Levy, and Murnane (2003) on the task-based framework, a robust finding has emerged across comparative political economy that workers in routine-task-intensive (RTI) occupations disproportionately support populist radical right parties (Gingrich 2019; Kurer 2020; Im et al. 2019; Autor et al. 2020; Gallego and Kurer 2022). The pattern is particularly observable in countries with weaker welfare provision (Vlandas and Halikiopoulou 2022; Caselli et al. 2021), leading scholars to argue welfare generosity moderates the relationship between economic vulnerability and exclusionary politics. Indeed, undergirding much of this comparative welfare state literature is Ruggie's (1982) framework of embedded liberalism, in which democratic governments, recognising that economic openness produces losers, provide social protection as compensation, on the assumption that compensation will dampen the political resentment of the dislocated. Effectively, the operative variable is purported to be quantity. Spend more, get less populism."

Notice: "Since the foundational contributions", "a robust finding has emerged", "Indeed, undergirding much of...", "Effectively, the operative variable is purported to be" — five Ben tics in five sentences. This paragraph is the model.

## Anti-patterns from this session

These are versions I produced that Ben said didn't sound like him. Don't repeat them.

### Anti-pattern 1: Smooth definitional opener
> "What welfare says, I argue, is the mechanism."

Why this fails: "What X is, is Y" construction is an LLM tic. The claim is fine; the structure is wrong. Replace with "Welfare communicates, and that communication is the mechanism."

### Anti-pattern 2: Bolded sub-claim parallelism
Three bolded headers like **Stage one: identity switching.** **Stage two: misattribution.** **Stage three: defensive othering.**

Why this fails: this is Wikipedia-AI scaffolding. Ben's pre-AI writing uses inline "Firstly... Secondly... Thirdly..." in flowing prose. Convert bolded scaffolds to inline.

### Anti-pattern 3: "It is X. It is Y." flat sequencing
> "The damage mechanism is legible. The protective one is not."

Why this fails: too clean, too tight. Real Ben prose has more variation. Better: "The damage mechanism is legible across every specification this paper presents, while the mirror image on the solidarity side is not detectable."

### Anti-pattern 4: "I should note that..." preamble
Hedge tokens that signal LLM uncertainty. Cut the preamble; just say the thing.

### Anti-pattern 5: Em-dash apposition stacking
> "Welfare design — the institutional architecture of decommodification — shapes..."

Why this fails: em-dashes are not in his voice and are the #1 detector tell. Replace with "Welfare design, the institutional architecture of decommodification, shapes..." or "Welfare design (the institutional architecture of decommodification) shapes..."

## When voice and detector resistance conflict

The Will Francis humanizing rules are a starting heuristic, but voice wins. Specifically:
- `foster` is on the WF banned list but appears in Ben's pre-AI Global Media essay. Keep it.
- `robust` is fine in methodological contexts ("robust across specifications") even if WF flags it.
- WF says max one em-dash per response. For Ben's voice, the target is zero.
- WF says use contractions. Ben's academic prose rarely contracts. Don't force contractions where they break register.

When in doubt, look at what the pre-AI samples actually do. The samples are in `manuscripts/Writing Samples/`.

## Self-check before delivery

1. Read the prose aloud. If a sentence stops you, swap it.
2. Count em-dashes. If >5 per 1000 words, kill them.
3. Check for at least one block quote (or two-three inline quotes) in any theory-heavy section.
4. Confirm 5+ Ben transitions per 1000 words.
5. Look for hedge stacking ("may be", "could be", "is part of what shapes"). Replace at least one with a flat assertion.
6. If detection-resistant prose is required, run the diagnostic in `humanize-academic/SKILL.md`.
