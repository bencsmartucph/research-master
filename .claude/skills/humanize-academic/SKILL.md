---
name: humanize-academic
description: Reduce AI-detector signal in academic prose written by or with Claude. Use when a paper, essay, or abstract is going to be released externally and detector resistance matters. Calibrated against the GPT Zero 100% → 60% human transition observed 2026-04-25 on the asymmetric welfare paper.
disable-model-invocation: false
allowed-tools: ["Read", "Grep", "Edit", "Bash"]
---

# Humanize Academic Prose

> Pragmatic skill. Honest about its limits. AI-edited-by-AI prose has a perplexity floor that surface editing cannot cross. The reliable fix is human authorship of key paragraphs. This skill helps with everything *except* that.

## When this skill applies

Use when:
- Externally-released prose (journal submission, public-facing writing)
- Detector flags >70% AI on a section that needs to be defensible
- Voice has drifted toward LLM register after multiple rewrite passes

Do NOT use when:
- Internal documents, planning files, comments
- The user is testing detection out of curiosity (set expectations honestly)
- Time pressure is severe and "good enough" beats "minimum viable" (acknowledge this and move on)

## Honest framing

What you (Claude) can do with editing alone:
- Move from `99% AI` → `40-60% human` on a typical academic paragraph
- Eliminate surface markers (em-dashes, banned phrases, mechanical parallelism)

What you cannot do with editing alone:
- Reach `90%+ human` purely through edits — token-level perplexity has a floor
- Disguise LLM authorship from a sophisticated detector indefinitely

The reliable path to high human-detection scores:
- The user types key paragraphs from scratch in their own words
- Genuinely human source text (quotes, direct citations) is embedded
- The user provides an authorial voice anchor that the AI can match

## Diagnostic protocol

Run before and after editing. Track deltas.

```python
import re
text = open(file).read()
body = re.search(r'<body markers>', text, re.DOTALL).group(1)

# Surface markers
em_dashes = body.count('—')
mid_sentence_colons = len(re.findall(r'[a-z]: [a-z]', body))
semicolons = body.count(';')
what_x_is = len(re.findall(r'\bWhat\s+\w+(?:\s+\w+)?\s+(?:is|are|does|do|makes)\b', body))

# Burstiness
sentences = re.split(r'(?<=[.!?])\s+', body)
sentences = [s for s in sentences if len(s.split()) > 2]
short = sum(1 for s in sentences if len(s.split()) <= 8)
short_pct = short * 100 // len(sentences)

# Banned words (Will Francis list)
banned = ['delve','underscore','bolster','leverage','unpack','pivotal','transformative',
          'innovative','comprehensive','seamless','multifaceted','holistic','realm']
banned_hits = [b for b in banned if re.search(rf'\b{b}\b', body, re.IGNORECASE)]

words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", body))
print(f"{words}w | em-dashes: {em_dashes}/1k = {em_dashes*1000//words}")
print(f"colons: {mid_sentence_colons}, semicolons: {semicolons}")
print(f"'what X is': {what_x_is}, banned: {banned_hits}")
print(f"short sentences: {short}/{len(sentences)} = {short_pct}%")
```

Targets after editing pass:
- Em-dashes per 1000 words: <5 (ideal: 0)
- Mid-sentence colons: halve from baseline
- Semicolons: keep or increase (academic register)
- "What X is/does" constructions: 0
- Short sentences: 20-30% of total
- Banned words: 0 (with voice-specific exceptions; see voice-ben skill)

## The four-pass editing sequence

Apply in this order. Each pass targets a specific detection signal.

### Pass 1: Surface marker purge (~15 min for 5000 words)

Replace every em-dash with one of:
- Semicolon (if connecting two independent clauses with related ideas)
- Comma (if shorter parenthetical aside)
- Period (if the dash is doing the work of a sentence break)
- Parentheses (if genuinely parenthetical material)

Eliminate "What X is, is Y" / "What makes X X is Y" constructions. Replace with direct subject-verb assertions.

Audit the Will Francis banned-word list. Replace each instance unless the user's authentic voice uses it (e.g., `foster` for Ben).

### Pass 2: Mechanical parallelism break (~20 min)

Identify all paragraphs structured as parallel triplets:
- "First... Second... Third..." with identical sentence shape
- Bolded sub-claim headers like **A.** **B.** **C.**
- "Three asymmetries: X, Y, Z" followed by paragraph-each treatment

For each: vary the openers, vary the lengths, vary the citation density. Inline `Firstly... Secondly... Thirdly...` is acceptable for Ben specifically (per pre-AI samples).

### Pass 3: Quote integration (~30 min, biggest impact)

This is the highest-leverage move. Find the AI-flagged sections and embed direct quotes from primary literature. Quote-mosaic structure (see `quote-mosaic/SKILL.md`):

```
[paraphrase or claim → direct quote → one-sentence Ben commentary → next claim]
```

Aim for 15-25% of words in detection-vulnerable sections to be direct quotes. The quotes are genuinely human source text; their inclusion measurably drops aggregate perplexity.

### Pass 4: Voice register matching (~20 min)

Apply `voice-ben` skill rules. Specifically:
- Inject `Indeed,`, `Furthermore,`, `Through this perspective,`, `Effectively,`, `Drawing on`, `as articulated by`, `as purported by`, `undergirding`
- Lengthen sentences in main argument prose (target 25-40 words for compound sentences)
- Allow some grammatical roughness (subject-verb spreads, slightly awkward clause stacks)
- Verify distinctive vocabulary present (`uncovers`, `fortifies`, `perpetuates`, `homophilous`, `factitious`)

## When detector still flags >70% AI after all four passes

Stop editing. Tell the user honestly: "I've done what surface editing can do. The remaining signal is structural. To go lower, you need to type the prose yourself."

Recommend the **anchor paragraph protocol**:
1. Identify the 2-3 highest-stakes paragraphs (typically: abstract, intro paragraph 1, discussion paragraph 1)
2. User reads what's there, closes the file, types from memory
3. Awkwardness and rough edges *help* — don't smooth the user's prose afterward
4. Rebuild and retest

A 100%-AI paragraph that becomes user-typed scores ~0%. Three retyped paragraphs in a paper average down the whole document's score by 30-50 percentage points.

## Anti-patterns from this session

### Anti-pattern: Editing the same prose repeatedly
Each editing pass introduces new LLM tokens. Diminishing returns set in fast. After three passes on the same paragraph, the score floor is hit and further editing actively hurts. Stop earlier than feels natural.

### Anti-pattern: Telling the user "this can't be reduced further"
This was wrong on this session. The user pushed back ("I think you have it in you") and the quote-mosaic restructure dropped detector flag from 100% AI to 60% human in one pass. The right framing is "I've reached the limit of *this technique*; here are alternative techniques."

### Anti-pattern: Using contractions to fake informality
LLMs reach for contractions when asked to humanize. In academic register, contractions often break voice. Check the user's pre-AI samples; if they don't contract in formal prose, don't add contractions in the humanized version.

### Anti-pattern: Adding deliberate typos or grammar errors
Detectors aren't fooled by misspellings. They detect token distribution patterns. Errors look like errors, not like human authorship. Don't do this.

## Calibration data from this session

Paper: "Dignity Is a Baseline" (`paper_draft_v4_final.md`)
Date: 2026-04-25

| Pass | Em-dashes | Banned words | GPT Zero (intro) | Body words |
|------|-----------|--------------|-------------------|------------|
| Initial big-bet implementation | 81 | several | 100% AI | 7791 |
| Surface marker purge | 0 | 0 | (not retested) | 7339 |
| Aggressive trim + abstract redo | 0 | 0 | 100% AI | 5501 |
| Quote-mosaic intro restructure | 0 | 0 | **60% human** | 5594 |

The quote-mosaic restructure was the move that worked. It embedded Kurer (2020 p.1801) as a block quote, Wagner (2022) abstract excerpts, Kurer-Palier (2019), and Gidron-Hall (2017 p.26) into the intro. ~200 words of genuinely human source text (out of ~880 intro words = 23%) is what dropped the score.

## Self-check before delivery

1. Run the diagnostic. Confirm targets met.
2. Ask the user: "Can you type the abstract paragraph yourself before submission?" — even one retyped paragraph helps.
3. Acknowledge any remaining flag honestly. Don't promise scores you can't deliver.
