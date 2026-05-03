---
chapter_id: "01"
title: "The Counterfactual Question"
part: I
status: drafted
estimated_word_count: 3200
prerequisites: []
introduces:
  - potential_outcomes
  - selection_bias
  - randomisation
  - fundamental_problem
  - ate_att
  - four_observational_moves
requires: []
related_concepts:
  - chapter_id: "02"
    note: "Sharpens the selection problem into the working tool of conditional independence."
  - chapter_id: "06"
    note: "Regression-as-matching is the mechanical implementation of conditioning, the first of the four moves named here."
  - chapter_id: "22"
    note: "Differencing — the second of the four moves — is the heart of the within-country thesis design."
figures: []
interactives:
  - file: "interactives/ch01_selection_bias.html"
    description: "Selection-bias slider: confounder strength on the x-axis, naive ATE drifting away from the true ATE as the confounder gets stronger. The grey dotted line is the second brace of the bias decomposition, made visible."
    source_script: "analysis/ch01_selection_bias_interactive.py"
recall_prompts: 5
last_updated: 2026-05-03
---

# Chapter 1 — The Counterfactual Question

> Empirical work begins with a question. The question is always counterfactual.
> Everything else is technique.

## 0. Where we're going

By the end of this chapter you should be able to do four things:

1. State the *fundamental problem of causal inference* in one sentence.
2. Explain why a randomised experiment solves it, and why almost everything you have data for isn't one.
3. Identify the (impossible) experiment that would directly answer the central question of your paper.
4. Articulate, in plain English to an imaginary referee, what your paper does *instead*, and what it costs you.

Those four sentences are not the answer to a methods exam. They are the working memory of every econometrician who is good at their job. We are going to build them now and re-build them, with more apparatus attached, in every later chapter.

---

## 1. Two classrooms

Pretend you teach a class of thirty children, and a colleague down the hall teaches another class of thirty. At the end of the year, your students score 75 on a standardised test; hers score 65. Your kids are smarter, right?

Of course not. There are a hundred reasons her kids could have scored ten points lower that have nothing to do with whether they were taught well. Maybe her class had more children who arrived mid-year. Maybe her room got the afternoon sun and they were hot. Maybe parents who fought to get their child into your class were also more involved in homework. Maybe yours was a "gifted" track and hers wasn't.

Every one of those alternative explanations is a story about why the comparison "your students vs hers" doesn't isolate the effect of you-vs-her. The scores reflect not only the effect of teaching but the effect of *who ends up in which classroom*. We have a name for this confusion: it is the **selection problem**, and it is the reason most empirical comparisons quietly lie to you.

The honest comparison would require something we cannot have. We would need to take the same thirty children, taught by you, and observe what they would have scored if they had been taught by your colleague instead — without changing anything else. Then we could subtract. The first number minus the second would be the *causal effect of being taught by you rather than her, for these specific children*.

The trouble is that each child can only be in one classroom. Once we observe them in your class, the version of them that was in hers is gone. We cannot observe both.

This is the **fundamental problem of causal inference**. It has a one-sentence statement worth memorising:

> For every unit, we observe one of two potential outcomes; the other is missing.

The whole edifice of econometrics, every method you will ever learn, is a strategy for constructing a credible substitute for the missing potential outcome. Read that sentence again. Slowly. We will return to it.

> **Try this.** Without reading further, write down (in one sentence each) the analogue of this two-classroom story for your welfare-state paper. Specifically: what is the "your class vs my class" comparison, and what is the missing potential outcome you cannot observe?

<details>
<summary>What I would have written</summary>

The "your class vs my class" comparison is between two welfare states with different decommodification levels — say, the UK (low CWED, ≈28) and Norway (high CWED, ≈43). The observed comparison is "British workers exposed to RTI become more anti-immigration than Norwegian workers exposed to the same RTI". The missing potential outcome is what British high-RTI workers *would* have looked like if Britain had Norway's welfare design — same workers, same labour market shock, different welfare encounter. We can never observe that. Your whole paper is a careful attempt to construct a credible substitute by triangulating across 15 countries and exploiting variation in CWED. (If you wrote something close to this you are already ahead of where most MSc students are.)
</details>

---

## 2. Potential outcomes — the notation that fixes everything

For each unit $i$ — child, worker, country — we imagine two states of the world:

| Symbol | Meaning |
|---|---|
| $Y_i(1)$ | Outcome for unit $i$ if "treated" (in your class, in a high-CWED country, exposed to a programme) |
| $Y_i(0)$ | Outcome for unit $i$ if "untreated" (the alternative state of the world) |
| $D_i \in \{0, 1\}$ | The treatment status that actually happened for unit $i$ |
| $Y_i$ | The outcome we actually observe: $Y_i = D_i \cdot Y_i(1) + (1 - D_i) \cdot Y_i(0)$ |

That last line is a tiny piece of bookkeeping; it just says "we see whichever potential outcome corresponds to the treatment that actually happened, and never the other." Read it twice.

The **individual treatment effect** is

$$\tau_i = Y_i(1) - Y_i(0).$$

This is the quantity we cannot compute, ever, for any single $i$, because we are missing one of the two terms.

What we usually want, slightly less ambitiously, is the **average treatment effect** across some population:

$$\text{ATE} = \mathbb{E}[Y_i(1) - Y_i(0)] = \mathbb{E}[Y_i(1)] - \mathbb{E}[Y_i(0)].$$

The trick of the field is that even though we cannot compute any individual $\tau_i$, we *might* be able to compute the average — provided we have a credible substitute for the average of the missing potential outcomes.

`★ What's actually going on ─────────────────────────────────────`
The move from $\tau_i$ to $\text{ATE}$ is one of those "technically obvious, conceptually huge" moments. We have given up on knowing the effect for any specific person. In exchange we get to talk about effects on average. *This is the price of admission to causal inference using observational data.* Every method in the rest of this book is buying you the average effect; none of them buys you the individual effect. When a journalist writes "X causes Y by 5 percentage points", what they mean — if they're being honest — is "on average, in a population that looks like our sample, the difference is 5". Internalise this distinction now and you will never confuse the two.
`─────────────────────────────────────────────────────────────`

What does the **naive comparison** give you? If we just compare the average outcome among the treated to the average outcome among the untreated, we get

$$\underbrace{\mathbb{E}[Y_i \mid D_i = 1]}_{\text{average among the treated}} - \underbrace{\mathbb{E}[Y_i \mid D_i = 0]}_{\text{average among the untreated}}.$$

Now do the algebra: substitute in $Y_i = D_i Y_i(1) + (1-D_i) Y_i(0)$, and we get

$$\mathbb{E}[Y_i(1) \mid D_i=1] - \mathbb{E}[Y_i(0) \mid D_i=0].$$

This is *not* the ATE. The ATE involves both potential outcomes for the *same* group of people; this involves one potential outcome for the treated group and the other potential outcome for a *different* group. Add and subtract $\mathbb{E}[Y_i(0) \mid D_i=1]$ and rearrange:

$$\underbrace{\big\{\mathbb{E}[Y_i(1) \mid D_i=1] - \mathbb{E}[Y_i(0) \mid D_i=1]\big\}}_{\text{ATT (effect on the treated)}} + \underbrace{\big\{\mathbb{E}[Y_i(0) \mid D_i=1] - \mathbb{E}[Y_i(0) \mid D_i=0]\big\}}_{\text{selection bias}}.$$

This decomposition is the most important equation in the book. Look at it.

| Equation | What it says |
|---|---|
| First brace (ATT) | The average effect of treatment, computed on the people who actually got treated. This is a real causal quantity; it is what we want. |
| Second brace (selection bias) | The difference, in their *untreated* potential outcome, between the people who got treated and the people who didn't. If treatment is non-random, this is generally not zero, and the naive comparison reports it as if it were part of the effect. |

When you compare your class's scores to your colleague's, the naive difference is the causal effect of you-versus-her *plus* the average difference in untreated potential outcomes between the children in your class and the children in hers. If your class was a "gifted track", that selection bias is large and positive, and you will report it as evidence of your teaching brilliance.

> **Open this in a browser:** [`interactives/ch01_selection_bias.html`](interactives/ch01_selection_bias.html)
>
> A simulation with a known true ATE of 1.0. The x-axis is the strength of an unobserved confounder $U$ that drives both selection-into-treatment and the outcome. As you slide right, the naive comparison drifts away from the truth; the grey dotted line is the selection-bias term from the algebra above. At zero confounder strength, the comparison is honest. At a strong confounder, the naive estimate can be three times the true effect. *This is what the algebra is saying, drawn out.*

> **Try this.** Suppose I tell you that countries with higher welfare generosity tend to have populations that were already more cosmopolitan and less hostile to immigration before any welfare reforms happened. If you compare anti-immigration attitudes across welfare regimes naively, in which direction does selection bias push the apparent effect of welfare generosity? Toward "welfare reduces hostility" or toward "welfare increases hostility"?

<details>
<summary>Answer</summary>

Toward "welfare reduces hostility". High-CWED countries had lower untreated $Y(0)$ (less baseline hostility) for reasons that have nothing to do with the welfare state's causal effect. The naive comparison would give you a *more* negative welfare-attitudes correlation than the true causal effect warrants. Selection bias and treatment effect run in the same direction here, and you cannot separate them from the comparison alone.

This is exactly why §V.G of your paper says "Country-level welfare indicators are confounded with other institutional differences". You are naming the selection-bias term explicitly.
</details>

---

## 3. Why randomisation solves the problem

Suppose we could flip a coin to decide which children went into your class and which into your colleague's. Now selection bias goes to zero. Here's why, in two lines.

If $D_i$ is assigned by a coin flip independently of everything else about unit $i$, then in expectation the children in your class and the children in hers have the same untreated potential outcomes:

$$\mathbb{E}[Y_i(0) \mid D_i = 1] = \mathbb{E}[Y_i(0) \mid D_i = 0] = \mathbb{E}[Y_i(0)].$$

The bracketed selection-bias term in our decomposition collapses to zero. The naive comparison now estimates the ATE without bias:

$$\mathbb{E}[Y_i \mid D_i = 1] - \mathbb{E}[Y_i \mid D_i = 0] = \mathbb{E}[Y_i(1)] - \mathbb{E}[Y_i(0)] = \text{ATE}.$$

This is the entire reason randomised experiments are the gold standard. They do not magically reveal individual treatment effects (the fundamental problem still applies). What they do is guarantee that the missing potential outcome is, *on average*, well-substituted by the observed outcome of the other group. The substitute is credible because the assignment process severed any link between $D_i$ and $Y_i(0)$.

`★ What's actually going on ─────────────────────────────────────`
Notice what randomisation does NOT do. It does not equalise the two groups on every observable characteristic; with N=30 there will be more boys in one and more girls in the other, more readers in one and more sport-players in the other. What it equalises is the *expected* potential outcomes. In any one experiment, the two groups will differ; across all possible random assignments, the average difference is zero. This is why small experiments produce noisy estimates and large experiments produce precise ones. The estimator is unbiased; the variance scales with $1/N$. Bias and variance are different things.
`─────────────────────────────────────────────────────────────`

> **Try this.** Suppose your colleague secretly switched two of her students for two of yours, picking the strongest of hers and the weakest of yours. (a) What does this do to selection bias in the naive comparison of class averages? (b) What does it do if you re-randomise *after* the swap?

<details>
<summary>Answer</summary>

(a) Selection bias is now non-zero in a specific direction: your class is weaker on average (you lost a strong one, gained a weak one); her class is stronger on average. The naive comparison will *underestimate* the effect of your teaching. (b) Re-randomisation eliminates the bias. The post-swap composition is now balanced in expectation again. This is why "randomisation" is sometimes called the "great equaliser" — it doesn't undo any specific imbalance, it makes the *expected* imbalance zero.
</details>

---

## 4. Why observational data doesn't solve it

You will, in your career, run exactly zero randomised experiments on welfare states. No referee will let you randomise countries to receive Nordic vs Liberal welfare designs and observe the political consequences. You are stuck with the world as it is.

The world as it is presents you with welfare regimes that arose for reasons. Some of those reasons are correlated with the political outcomes you care about. The Nordic countries are not Nordic because of a coin flip; they are Nordic because of long histories of social-democratic coalitions, ethnic homogeneity, oil wealth, Lutheran civic traditions, and a dozen other things that *also* affect anti-immigration attitudes. These confounders do not disappear because you ignore them. They sit inside the selection-bias term, contaminating every naive comparison you might want to make.

This is what makes observational causal inference hard. The problem is not the math (which is straightforward), and not the data (you have plenty). The problem is that you have to construct a *credible argument* that the selection-bias term in your specific setting is small, or that it has been removed by your design, or that it points in a direction that doesn't undermine your claim. That argument is the heart of an empirical paper. Methods are tools for making it.

There are roughly four moves you can make:

1. **Conditioning.** Find variables $X$ such that, *within* groups defined by $X$, treatment is as good as random. Then compare treated to untreated *within* $X$-cells. This is what regression-with-controls is doing, when it works. Chapters 5–7.
2. **Differencing.** If you observe each unit before and after treatment (or in two settings, treated and not), you can subtract out the time-invariant component of the unit's potential outcome. The classroom analogue is "compare each child's score to her own pre-test score, then average". This is the difference-in-differences family. Chapters 22–24.
3. **Instrumenting.** Find a variable $Z$ that affects $D$ but not $Y$ except through $D$. Use $Z$ to extract the part of $D$'s variation that is "as if random". This is instrumental variables. Not central to your current paper but you'll meet it.
4. **Matching.** Find untreated units that look statistically just like the treated units on observables, pair them up, and compute the average difference. Closely related to (1) but emphasises the matching step. Sometimes useful as a robustness check.

Your seminar paper uses (1) — conditioning on individual covariates plus modelling country-level heterogeneity — and *cannot* use (2), because the cross-sectional design has no within-country variation to difference out. Your thesis design will use (2) on Danish registry data, exploiting the 2003/2006/2013 activation reforms. Knowing which move you are making, and which move you are *not* in a position to make, is half of what it means to read your own paper honestly.

> **Try this.** For each of the following claims from your paper, name which of the four moves above it is implicitly relying on (or which one it would need but cannot make).
>
> (a) "RTI predicts anti-immigration attitudes after controlling for age, gender, education, income, and urban residence."
>
> (b) "Welfare decommodification accounts for 72 per cent of the cross-country variation in RTI-slopes."
>
> (c) "The Danish 2003 activation reforms produced damage signatures with decommodification held constant."

<details>
<summary>Answers</summary>

(a) **Conditioning** (move 1). The covariates are functioning as the $X$ in "treatment is as-good-as-random within $X$-cells". Whether that's defensible depends on whether you've conditioned on enough things; the answer is "probably not for full causal identification but enough for a defensible attitudinal-correlation finding".

(b) **None of the above, cleanly.** This is a *between-country* descriptive statistic. You cannot make a causal claim from it without invoking move (1) — that the 15 countries are comparable conditional on observables. Your paper is honest about this in §V.G ("country-level welfare indicators are confounded with other institutional differences"). The cross-level interaction in Model 3 is a partial-conditioning version that does some but not enough work.

(c) **Differencing** (move 2). This is your thesis design speaking, not your seminar paper. You exploit *within-country* variation across reform episodes, holding the country fixed. The before-after-reform difference within each individual identifies the effect of the reform on that individual's attitudes (subject to its own assumptions, which we'll cover in Chapter 22).

If you got the third one right, you have already internalised the central architectural difference between your seminar paper and your thesis. That difference is the entire reason the thesis can claim things the seminar cannot.
</details>

---

## 5. The counterfactual buried in your paper

Re-read these two sentences from your introduction, slowly:

> "Welfare spending effort, on a matched 15-country sample, is uncorrelated with how strongly RTI exposure converts into exclusionary attitudes (r=0.01, N=15), while welfare decommodification accounts for 72 per cent of the same variation (r=−0.85)."

There is a counterfactual hidden in here, and it is doing all the theoretical work. The counterfactual is something like:

> "If we could take the United Kingdom — same workers, same labour market, same political history — and replace only its welfare design with Norway's, while leaving everything else unchanged, the slope of RTI on anti-immigration in the UK would fall from 0.51 to roughly 0.07."

That is the impossible experiment. You cannot run it; nobody can. But it is the question the paper is trying to answer, and every methodological choice in §V is best read as "given that this experiment is impossible, what is the best substitute we can construct?"

Your substitute is: rather than swapping welfare designs for one country, observe 15 countries that already have different welfare designs, model the within-country slope of RTI on anti-immigration, and ask whether the differences in those slopes line up with differences in welfare design *in the way the impossible experiment would predict*. They do, very strongly (r=−0.85). That is evidence — not proof — that the underlying mechanism is what the theory says it is.

The cost of this substitute is in §V.G: the 15 countries differ in many things besides welfare design. Some of those things might generate the same r=−0.85 even if welfare design were causally irrelevant. The macro-controls robustness check rules out a couple of them (GDP growth, inequality). The within-country thesis design rules out almost all of them, because each country acts as its own control. Each successive design buys you a credibility increment; each costs you data, time, or generalisability.

> **Defend the choice.** A methodologically aggressive referee says: "Your r=−0.85 is just confounding. Sweden has Sweden's welfare state and Sweden's politics; you cannot separate the two from cross-sectional data." You have 30 seconds. What do you say?

<details>
<summary>One defensible answer</summary>

"You're right that I cannot separate them with cross-sectional data alone, and §V.G says so directly. What I can show is that the cross-country pattern is consistent with the asymmetric mechanism *and* inconsistent with the symmetric buffering account that has dominated this literature. Two things sharpen that consistency: (1) the macro-controls robustness rules out the most obvious confounders (GDP growth, inequality), and (2) the asymmetric prediction extends to a *null* on the redistribution side (β=0.011, p=0.29), which the symmetric account cannot generate. The next step is the within-country Danish design that is robust to time-invariant institutional confounding by construction. The seminar paper is a consistency check on a theoretical claim; the thesis is the identification."

The point is not to claim more than the design supports. The point is to be precise about what the design DOES support, which is "consistency with the asymmetric mechanism on multiple independent margins, in a way the symmetric account cannot match". That is a real intellectual contribution even when it isn't yet a clean causal estimate.
</details>

---

## 6. What we have set up

If you have understood this chapter, you have the conceptual frame for everything that follows. The frame is:

> Every empirical claim is a counterfactual claim. We never observe the counterfactual. Methods are strategies for constructing credible substitutes. Each strategy makes assumptions; each is contestable; the contest is the substance of an empirical paper.

In Chapter 2 we look at the **selection problem** in more detail and develop the language to say *exactly* when a control variable does and does not solve it. We will introduce conditional independence and the back-door criterion (without the heavy graph-theoretic machinery; just enough to know what we're invoking when we add a control). After that, we are ready to build OLS from the ground up in Part II.

---

## End-of-chapter check

Five questions, increasing difficulty. Answer them in your head before opening the toggles. If you get fewer than four right, re-read this chapter before Chapter 2; if you get four or five, you're ready to move on.

**1.** State the fundamental problem of causal inference in one sentence.

<details>
<summary>Answer</summary>

For every unit, we observe one of two potential outcomes; the other is missing. (Equivalently: we observe $Y_i(D_i)$ and never the other one.)
</details>

**2.** Why does randomisation solve the selection-bias problem?

<details>
<summary>Answer</summary>

Because randomisation severs the link between treatment status $D_i$ and the potential outcomes $Y_i(0), Y_i(1)$. In expectation, treated and untreated units have the same untreated potential outcome, so the bracketed selection-bias term in the decomposition collapses to zero, and the naive comparison estimates the ATE without bias. It does not equalise the two groups on every realisation; it equalises them in expectation.
</details>

**3.** In your paper's setting, what is the (impossible) experiment that would directly answer the central question?

<details>
<summary>Answer</summary>

Pick a country (say the UK). Hold its workers, labour market, electoral history, and demographic composition fixed. Replace *only* its welfare design with Norway's (or some other high-CWED design). Observe the slope of RTI on anti-immigration before and after the swap. The difference is the causal effect of welfare design on the RTI-to-exclusion conversion, holding everything else constant. This is impossible because welfare designs are not detachable from the institutional histories that produced them.
</details>

**4.** Given that experiment is impossible, what's your paper's substitute, and what does it cost you?

<details>
<summary>Answer</summary>

The substitute is a cross-sectional comparison across 15 countries that already vary in welfare design, modelling within-country slopes of RTI on anti-immigration and asking whether between-country slope variation tracks between-country welfare design variation. The cost is that the 15 countries differ in many things besides welfare design; the substitute conflates the welfare-design effect with anything else that varies cross-nationally. Macro-controls partly address this; the within-country thesis design will address it more cleanly.
</details>

**5.** Suppose your paper's r=−0.85 had come out instead at r=−0.10, p=0.71. Would that have been evidence for the *symmetric* buffering account, or evidence for "no welfare-design effect at all", or something else? Be precise.

<details>
<summary>Answer</summary>

It would have been evidence for "no detectable welfare-design effect at this scale of variation, given this slope-extraction methodology". It would *not* by itself be evidence for the symmetric account, because the symmetric account predicts a positive correlation in the *other* direction (more spending → less exclusion would show up as a different sign). r=−0.10 with high p-value would be a wash — consistent with no effect, with a small effect masked by sample noise, with measurement issues, or with the pattern being too small to detect at N=15. To distinguish "small true effect" from "no true effect" you would need either a much larger N or a much sharper measurement, neither of which observational welfare-state data offers easily. The asymmetric mechanism's empirical content lives in its predictions being *strong enough* to be seen at N=15. If they hadn't been, the theoretical claim would still be live but the empirical case would be much weaker.

If you got this right, you have understood that "no result" and "result against the theory" are different things, and that small samples do not give you the power to distinguish them cleanly. Hold onto this thought; it returns in Chapter 18 when we discuss reading nulls as evidence.
</details>

---

## Connections

- **Backward** — to your existing knowledge of regression: you've been computing $\beta$ coefficients for years. From now on, every $\beta$ in this resource is to be read as "the regression's best attempt to recover a causal contrast in potential outcomes, under the assumptions of this specific design." When the design is honest, the $\beta$ has a causal interpretation. When it isn't, the $\beta$ is just a description of the conditional mean.

- **Forward** — Chapter 2 sharpens "selection problem" into a working tool. Then Chapter 3 introduces the assumption (conditional independence) that has to hold for regression-with-controls to recover a causal estimate. Chapters 5–7 build OLS as the workhorse implementation of that idea, paying special attention to what each control is doing and what each isn't.

- **Sideways** — the same potential-outcomes framework underwrites the entire credibility revolution in applied economics from the 1980s onwards. When you read a Card paper, an Angrist paper, a Chetty paper, the language they use ("compliers", "always-takers", "ATT", "LATE") is all built on the four-symbol notation we just introduced. If those terms are mysterious to you now, they will not be by the time we finish Part II.

---

*Tell Claude what to sharpen before Chapter 2. Possible directions: "more concrete numbers in the algebra", "I want to see the bias decomposition with actual welfare-state numbers plugged in", "give me harder defence-the-choice questions", "the potential outcomes notation needs another worked example", or any other adjustment that would have made this chapter land more firmly. The next chapter calibrates to whatever you say.*
