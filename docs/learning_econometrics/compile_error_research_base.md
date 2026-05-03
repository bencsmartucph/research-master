# Compile Error / Patient Tutor — Research Base

*Source material for the Patient Tutor (LinkedIn) and Compile Error (long-form Substack) essays. Mine this for quotes, citations, counter-arguments, and framings. Updated as new sources surface.*

---

## A. The "compile error is gone" thesis — supporting context

### Karpathy's CLAUDE.md framework (2026)

Andrej Karpathy's CLAUDE.md framework hit #1 on GitHub trending in 2026, addressing three AI coding pitfalls he identified as central:

> "LLMs make silent assumptions instead of asking questions, overcomplicate solutions with unnecessary abstractions, and modify unrelated code as side effects. They don't manage their confusion, don't seek clarifications, don't surface inconsistencies, don't present tradeoffs, don't push back when they should." — Karpathy, 2026

Useful framing for the essay because it identifies the exact mechanism the compile error used to enforce: managing confusion, surfacing inconsistencies, pushing back when something doesn't add up. The compile error did this work invisibly; agentic AI removes it.

A 2025 academic study found that 94% of LLM compilation errors are type-check failures — the model assumed types instead of clarifying them. Quotable: when the compile error is bypassed by the agent, the failure mode shifts from "code doesn't run" to "code runs and is silently wrong."

### Karpathy on coherence threshold

> "LLMs crossed the coherence threshold in December 2025 — they're useful enough to change how we code daily, but not reliable enough to trust without guardrails."

The "coherence threshold" framing is useful for the essay because it positions the current moment specifically: this isn't a far-future concern, it's a today concern, and the gap between "useful enough to change behaviour" and "reliable enough to trust" is exactly where the defence-rehearsal practice has to fill in.

### Vibe coding to agentic engineering

Karpathy popularised "vibe coding" in 2025; in 2026 he describes the shift to "agentic engineering" — AI systems that "break down tasks, use tools, run tests, recover from errors, and iterate toward an outcome". This is the exact transition that removes the compile error as a pedagogical device. The agent recovers from the error before the human encounters it.

---

## B. AI tutoring effectiveness — what the evidence actually shows

### Khan Academy / Khanmigo (2025-2026)

Khan Academy ran a rigorous series of product tests from October 2025 to April 2026 and reported a six-percentage-point improvement in their effectiveness measures. Tests covered more than 15 million tutoring threads across six months.

Adoption: Khanmigo expanded from ~68,000 student and teacher users in partner districts (2023-24) to 700,000+ (2024-25), projected to exceed 1 million in 2025-26.

Crucial caveat for honest framing:
> "Khan Academy has yet to test the efficacy of its own Khanmigo through a randomized control trial study due to the expense and other challenges in running such studies, though the nonprofit still plans to conduct that 'gold standard' research."

Quote-worthy for the honest-limits section: even the most-deployed AI tutor in the world has not been validated by RCT. Anyone making AI tutoring claims at scale is running ahead of the evidence base. Your defence: you're not making scale claims, you're making "this is what it looks like when one person uses it well" claims, which is different.

### The 2-sigma gap

Bloom's (1984) finding that one-on-one tutoring produces 2-sigma improvements over conventional instruction is the foundational claim AI-tutoring evangelists invoke. Recent work qualifies this:
> "Bloom's often-cited results about tutoring's impact were unrealistic, with gains not widely replicated on math and reading tests."

Useful for the essay because it positions the AI-tutoring discourse in a specific historical lineage and notes its empirical fragility. The Patient Tutor argument doesn't need 2-sigma to land; it needs "this works for one person in this specific context", which is testable directly.

---

## C. The cheating-discourse landscape — what to engage with

### Current scale

> "2025 research from HEPI reveals that 18% of UK undergraduate students admit to submitting AI-generated text in their assignments, while 95% of the academic community believes AI is being misused at their institutions. AI-related academic misconduct now represents 60-64% of all cheating cases in higher education institutions globally as of 2025."

Useful framing for the essay's §1 ("the do-my-homework anxiety") to acknowledge the worry is both quantitatively real and culturally dominant. The litmus-test response in the current draft is too thin to discharge this — the cheating-discourse section should be expanded by 50-100 words to engage the strongest version.

### The strongest version of the cheating worry

> "The greatest risk of AI in higher education isn't cheating – it's the erosion of learning itself" (Theodora Kotsiou, *The Conversation*, 2025).

This is the version of the worry that doesn't dispense via litmus tests. The argument is that even when students don't intend to cheat, the availability of AI-generated answers changes their relationship to struggle, and struggle is where learning happens. This is the steel-manned version your essay should engage with explicitly.

### The "AI literacy" reframing

> "ChatGPT bans evolve into 'AI literacy' as colleges scramble to answer the question: 'what is cheating?'" (Fortune, 2025).

The institutional response is moving from prohibition to curriculum redesign. This connects directly to your "project + oral, AI explicitly allowed" proposal in the Compile Error essay — you're describing a specific implementation of the AI-literacy reframing.

### Assessment redesign

> "Universities must move beyond detection-based strategies towards ethically grounded, validity-driven assessment practices."
> "Some educators now conduct most writing in-class with monitored screens and teach students to use AI as a study aid 'to get kids learning with AI instead of cheating with AI'."

Both of these support the project-plus-oral proposal. Cite them when the proposal lands; they show you're not inventing the architectural shift, you're describing what the discipline is already moving toward.

---

## D. Learning science citations (for the pedagogical-primitives section)

The citations in the current draft are accurate but should be tightened for direct quotability. Verified primary sources:

- **Roediger & Karpicke (2006)**, *Psychological Science* 17: "Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention." The testing effect: practice retrieval beats re-reading by a wide margin in long-term retention.
- **Sweller (1988)**, *Cognitive Science* 12: "Cognitive Load During Problem Solving." The foundational worked-example paper.
- **Renkl (2014)**, *Cognition & Instruction* 32: "Toward an Instructionally Oriented Theory of Example-Based Learning." Worked-example fading specifically.
- **Chi et al. (1989)**, *Cognitive Science* 13: "Self-Explanations: How Students Study and Use Examples in Learning to Solve Problems."
- **Bjork (1994)**, in Metcalfe & Shimamura eds., *Metacognition*: "Memory and metamemory considerations in the training of human beings." The desirable-difficulties paper.
- **Karpicke & Blunt (2011)**, *Science* 331: "Retrieval Practice Produces More Learning Than Elaborative Studying with Concept Mapping." The pretesting / hypercorrection result.
- **Ainsworth (2006)**, *Learning and Instruction* 16: "DeFT: A conceptual framework for considering learning with multiple representations."

Two more worth adding if the essay grows:

- **Anderson, Reder & Simon (1996)**, *Educational Researcher* 25: "Situated learning and education." The transfer-context paper. Supports the "paper is the curriculum" claim that learning sticks when context matches application.
- **Roediger & Pyc (2012)**, *Educational Psychologist* 47: "Inexpensive techniques to improve education." The "techniques work, but only if used" framing — useful for the close.

---

## E. Counter-evidence and steelman positions

The essay needs to engage these to be credible.

### Bender, Hanna et al. on the limits

The argument from the AI-skeptic position is that LLMs are stochastic parrots, that what looks like tutoring is pattern-matching on memorised text, and that "AI tutors" cannot do what human tutors do because they don't model the student. Engage directly:

> "If the test is whether the AI knows the student, the answer is no. If the test is whether the architecture around the AI can be configured to track the student across sessions, the answer is yes — and the architecture is what does the work, not the model."

That's the move. The Bender/Hanna critique is correct about the model and incorrect about the architecture. The essay's contribution is naming the distinction.

### The AI-use-is-class-stratified objection

Students at well-resourced institutions get the patient-tutor experience; students at under-resourced institutions get the worksheet generator. The architecture-and-prompting practices that make AI tutoring work are themselves a form of cultural capital. This is the strongest left-coded objection to the entire project, and it deserves a paragraph in the essay. The honest answer: yes, this is a real distributional concern, AND the solution is to publish the prompts and architecture so the resource is more accessible than it would be otherwise. Your Workflow piece, if you decide to write it, is one move in that direction.

### The "AI tutors haven't worked at scale yet" objection

LA Unified's pilot of an AI tutoring chatbot collapsed in 2024. Several other district-level rollouts have produced mixed or negative results. The essay should not claim that AI tutoring works in general; it should claim that AI tutoring works for one specific student in one specific architecture, and that the conditions can be characterised. The honest framing is: this is what success looks like when conditions are met, not a claim that conditions are easy to meet.

---

## F. Concrete moments from your own session — pre-tagged for essay use

These are the specific anecdotes from our conversations that anchor abstract claims. Each is tagged with which essay claim it supports.

| Moment | Best essay use |
|---|---|
| BLUPs discovery (paper text says separate-OLS, actual code is BLUPs, r moves from −0.625 to −0.855) | Patient Tutor opening; Compile Error central case study |
| LR test χ² = −∞ bug (convergence error misreported a real test statistic) | Honest-limits section in both essays |
| Cluster-SE inflation calc (n̄=1400, ρ=0.05, design effect 71, naive SE 8× too small) | Workflow / methodology depth section if Workflow piece survives |
| The "you've named something I couldn't articulate" turn (compile-error realisation) | Compile Error essay opener; meta-evidence the practice is collaborative |
| The intellectual portrait prompt itself (asking AI to read your annotation database and produce a portrait of your mind) | Compile Error essay; centerpiece artifact in any Workflow piece |
| Working-with-Ben markdown file written by Claude about you | Workflow piece evidence; Patient Tutor footer if you mention infrastructure |

---

## G. Open questions the essay should engage with (not avoid)

Pre-tagged so you don't write past them.

1. **Where does the cost of teaching shift?** If the tutor is free at point of use but the architecture and prompting are bottlenecks, who builds the architecture? The student? The institution? A vendor? The political economy of AI tutoring matters and the essay should at least gesture at it.

2. **What happens when methodology becomes infinitely scrutable but readers still don't bother?** The asymmetry-equalisation thesis assumes reader-side scrutiny will rise. It might not. The essay should distinguish "the cost has fallen" from "the practice has changed", and acknowledge the gap.

3. **What's the failure mode of defence-rehearsal-as-assessment?** Rehearsed answers can themselves be hollow. A student who memorises 30-second defences for every choice in their paper might still not understand the choices. The defence rehearsal is necessary but not sufficient; the essay should say so.

4. **Does this generalise to fields without quantitative methodology?** The compile-error analogy works for econometrics, code, formal proofs. It works less obviously for history, ethnography, theory. The essay should either bound the claim or make the bridging argument explicit.

5. **What's your relationship to the AI labs whose tools you're praising?** If the essay is aimed partly at Anthropic as an audience, that proximity should be disclosed lightly somewhere — once, not repeatedly. Ideally as a short bio note rather than in the essay body.

---

## H. Sources

- [How Khan Academy Is Building a Better AI Tutor — Khan Academy Blog](https://blog.khanacademy.org/how-khan-academy-is-building-a-better-ai-tutor-our-most-recent-learnings/)
- [Can an AI-Powered Tutor Produce Meaningful Results? — Education Week](https://www.edweek.org/technology/opinion-can-an-ai-powered-tutor-produce-meaningful-results/2025/07)
- [3 questions for K-12 leaders to consider amid the AI tutoring boom — K-12 Dive](https://www.k12dive.com/news/3-questions-for-k-12-leaders-to-consider-amid-the-ai-tutoring-boom/757314/)
- [Andrej Karpathy's CLAUDE.md framework — Medium](https://medium.com/@creativeaininja/andrej-karpathys-fix-for-ai-coding-agents-gone-wrong-a-single-markdown-file-6fb377097717)
- [Andrej Karpathy on Code Agents, AutoResearch — NextBigFuture](https://www.nextbigfuture.com/2026/03/andrej-karpathy-on-code-agents-autoresearch-and-the-self-improvement-loopy-era-of-ai.html)
- [From Vibe Coding to Agentic Engineering — Atal Upadhyay](https://atalupadhyay.wordpress.com/2026/05/02/from-vibe-coding-to-agentic-engineering-building-with-ai-in-the-software-3-0-era/)
- [Karpathy's CLAUDE.md: Fix AI Coding Pitfalls — byteiota](https://byteiota.com/karpathy-claude-md-ai-coding-pitfalls-accuracy-2/)
- [Cheating, teaching, and tutoring — Chalkbeat](https://www.chalkbeat.org/2025/11/04/three-theories-on-ai-in-schools-about-cheating-teaching-and-tutoring/)
- [The greatest risk of AI in higher education isn't cheating — The Conversation](https://theconversation.com/the-greatest-risk-of-ai-in-higher-education-isnt-cheating-its-the-erosion-of-learning-itself-270243)
- [ChatGPT bans evolve into 'AI literacy' — Fortune](https://fortune.com/2025/09/12/college-cheating-ai-literacy-bans-exams-homework/)
- [AI-Based Digital Cheating At University — Springer Journal of Academic Ethics](https://link.springer.com/article/10.1007/s10805-025-09642-y)
- [How vulnerable are UK universities to cheating with new GenAI tools? — Tandfonline](https://www.tandfonline.com/doi/full/10.1080/02602938.2025.2511794)

---

*Last updated: 2026-05-03 by the strategy session that preceded the new project setup.*
