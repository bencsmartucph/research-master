---
chapter_id: NN
title: "[Chapter title — short, declarative]"
part: "[I/II/III/IV/V/VI]"
status: drafting   # drafting | drafted | reviewed | published
estimated_word_count: 3000
prerequisites: []  # list of other chapter_ids this chapter assumes
introduces:        # concept slugs this chapter introduces (must match concept_graph.yaml)
  - concept_slug_one
requires:          # concept slugs this chapter assumes from earlier chapters
  - some_earlier_concept
related_concepts:  # for Notion cross-linking
  - chapter_id: NN
    note: "[How this chapter connects to that one]"
figures: []        # populated as figures are added
interactives: []   # populated as interactives are added
recall_prompts: 5  # count for the end-of-chapter check
last_updated: YYYY-MM-DD
---

# Chapter NN — [Chapter title]

> **One-sentence orientation epigraph.** Set the chapter's claim in italics here, in a tone that locates the reader in the larger argument. Short. Declarative. The kind of sentence that comes back to mind a week later.

## 0. Where we're going

By the end of this chapter you should be able to do four things:

1. [First takeaway — stated as a verbal capability, not a topic]
2. [Second]
3. [Third — usually applied to Ben's own paper]
4. [Fourth — usually a "defend in plain English" framing]

Those four sentences are not the answer to a methods exam. They are the working memory of every econometrician who is good at their job. We will build them now and re-build them, with more apparatus attached, in every later chapter.

---

## 1. [Concrete vignette section]

Open with a story or scenario. No math in this section. The story should make the abstract problem visible *without* using technical vocabulary. Two-classroom teaching analogy, ice-cream-and-drowning, two-countries-with-different-welfare. Whatever the chapter is about, find the version of it that a smart non-economist friend would understand at dinner.

End the section by naming the problem the rest of the chapter solves. One sentence. Italicised if it earns it.

> **Try this.** [A short prediction exercise that takes 30 seconds. The reader should be able to answer it from intuition alone, without notation. Forces engagement before reading further.]

<details>
<summary>What I would have written</summary>

[The answer or one defensible answer. Keep this honest about uncertainty where it exists. If there are multiple defensible answers, say so and explain which one this chapter will pursue.]
</details>

---

## 2. [Notation and formal setup section]

Now introduce the notation. Inline, not in a table. First time each symbol appears, define it in plain English in the same sentence.

| Symbol | Meaning |
|---|---|
| $X_i$ | [What this represents for unit $i$] |
| $Y_i$ | [What this represents] |
| $\beta$ | [Coefficient interpretation] |

After the table, write 1-2 paragraphs working through what the notation says. Don't just state definitions; show how they combine.

`★ What's actually going on ─────────────────────────────────────`
A short callout explaining the elegant move the math is doing here. This is the moment where the reader pauses and goes "oh, that's clever". One per chapter, maximum two. Don't overuse — the impact is in the rarity.
`─────────────────────────────────────────────────────────────`

The key result of this section, written as an equation:

$$\color{blue}{Y_i} = \color{purple}{\beta_0} + \color{purple}{\beta_1} \color{blue}{X_i} + \underbrace{\varepsilon_i}_{\text{everything else}}$$

| Equation | What it says |
|---|---|
| $\beta_1$ | [Plain-English reading of the coefficient] |
| $\varepsilon_i$ | [Plain-English reading of the residual] |

> **Open this in a browser:** [`interactives/chNN_xyz.html`](interactives/chNN_xyz.html)
>
> [One-paragraph description of what the interactive shows and what to do with it. Frame as "the algebra above, made movable." End with a one-sentence directive — "drag the slider until you see the bias term reach 0.5; that's selection bias of one standard deviation."]

> **Try this.** [A second exercise, this time involving a small numerical computation. Should take 1-2 minutes. Reveals whether the reader has internalised the notation.]

<details>
<summary>Answer</summary>

[The answer with brief working. If there's a common wrong path, name it.]
</details>

---

## 3. [Application to Ben's paper]

This section is where the chapter's methodological substance lands on the welfare paper specifically. Identify the move from §V that this chapter is unpacking. Be explicit: "Section V uses [method]; here is what that means in our chapter's terms."

Walk through 3-4 sentences from §V slowly, as if reading them with a methods-trained friend who has just asked "wait, what is that doing?". Quote the actual paper text where useful.

> **Defend the choice.** A methodologically aggressive referee says: "[A specific objection a sharp methods referee could raise about this part of §V]." You have 30 seconds. What do you say?

<details>
<summary>One defensible answer</summary>

[The killer-line response, in quote format.]

> *"[The 30-second defence, structured: name the choice, name what it bought, name what it cost, land the substantive payoff.]"*

The structure: (i) [name the move], (ii) [acknowledge what was sacrificed], (iii) [point to the methodology-symmetric robustness check], (iv) [land the substantive conclusion]. Memorise the structure, not the words.
</details>

---

## 4. [What goes wrong without the method]

Show the wrong approach and its consequence. This is error-driven learning — seeing the failure mode and understanding why it fails is one of the most powerful pedagogical moves available.

Concrete is better than abstract here. If naive OLS would have given the wrong answer, show the actual wrong answer (numerical) alongside the right one. If a missing control would have biased the estimate, show the bias (numerical, with sign).

`★ What's actually going on ─────────────────────────────────────`
[Optional second insight callout — only if the chapter has earned a second one.]
`─────────────────────────────────────────────────────────────`

---

## 5. What we have set up

If you have understood this chapter, you have [the conceptual unlock this chapter delivered]. The unlock is:

> [One-sentence formulation of the chapter's conceptual contribution. Should be quotable.]

In Chapter [NN+1] we [preview the next move]. After that, we are ready to [pointer to where the arc is going next].

---

## End-of-chapter check

Five questions, increasing difficulty. Answer them in your head before opening the toggles. If you get fewer than four right, re-read this chapter before Chapter [NN+1]; if you get four or five, you're ready to move on.

**1.** [Recall question — definitional, lowest difficulty]

<details>
<summary>Answer</summary>

[2-4 sentence answer]
</details>

**2.** [Recall question — application of a single concept introduced in the chapter]

<details>
<summary>Answer</summary>

[Answer]
</details>

**3.** [Recall question — connection between two concepts]

<details>
<summary>Answer</summary>

[Answer]
</details>

**4.** [Recall question — application to Ben's paper specifically]

<details>
<summary>Answer</summary>

[Answer]
</details>

**5.** [Recall question — counterfactual reasoning, what would change if some assumption broke. Highest difficulty.]

<details>
<summary>Answer</summary>

[Answer. This is the question that separates "knows the material" from "owns the material". If this one trips you up, that's normal; come back to it next week.]
</details>

---

## Connections

- **Backward** — to [the chapter or prior knowledge this builds on]: [one-sentence explanation of the connection].
- **Forward** — Chapter [NN+1] [preview]. [What this chapter enables in later parts of the resource.]
- **Sideways** — [where Ben has seen the same idea in different clothes — a different field, a different tool, a different vocabulary]: [one-sentence explanation].

---

*Tell Claude what to sharpen before Chapter [NN+1]. Possible directions: [list 3-4 specific dimensions where the chapter could be tuned — "more concrete numbers", "harder defence questions", "the worked example needs another pass", "the interactive isn't doing the work I wanted".] The next chapter calibrates to whatever you say.*
