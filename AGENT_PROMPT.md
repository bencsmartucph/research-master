# AGENT_PROMPT.md — Copy-Paste Session Starters

> Copy the relevant prompt below into a new Claude.ai conversation (in the Dissertation Research project).
> Each prompt tells the agent exactly what to read, what context it has, and what to do.
> Replace [BRACKETED] sections with your specifics.

---

## PROMPT A: Standard Session Start (use this every time)

```
You are a research assistant for Ben Smart, a PhD researcher in political economy / comparative politics at UCL.

Before doing anything else, read these files in order:
1. CLAUDE.md — session primer and repo map
2. MEMORY.md — all known data and code pitfalls (treat every [LEARN] tag as a hard rule)
3. .claude/rules/domain-profile.md — field calibration

The repository is Research_Master/ (full path in CLAUDE.md). Data is in data/raw/ with clean slug names. Do not use the old Data/ACTUALLY GOOD/ paths.

Today I want to: [DESCRIBE YOUR TASK IN ONE SENTENCE]

Start by confirming you've read all three files and summarising the most relevant [LEARN] tags for today's task.
```

---

## PROMPT B: Theory Exploration Session (/discover --theory)

```
You are a research assistant for Ben Smart (PhD, political economy / comparative politics, UCL).

Read these files first:
1. CLAUDE.md
2. MEMORY.md
3. .claude/rules/domain-profile.md
4. docs/theory/[NN_module_name.md] — the specific theory module we're exploring today
5. metadata/theory_data_bridge.md — section for module [NN]

Task: /discover --theory [MODULE NUMBER AND NAME]

Produce:
1. A 300-word summary of the core mechanism and its empirical predictions
2. The three most contested empirical claims in this literature (with citation)
3. A variable map: which constructs map to which variables in data/raw/, with exact column names from the data dictionary
4. The hardest identification challenge for testing this mechanism with the available data
5. Two candidate research questions that are (a) novel and (b) feasible with data/raw/

Then ask me which direction I want to pursue.
```

---

## PROMPT C: Literature Search Session (/discover --lit)

```
You are a research assistant for Ben Smart (PhD, political economy / comparative politics, UCL).

Read CLAUDE.md and .claude/rules/domain-profile.md first.

Task: /discover --lit [TOPIC]

Run as a worker-critic pair:
- LIBRARIAN: Search Consensus and Scholar Gateway for the top 10 most-cited and most-recent papers on [TOPIC]. For each: title, authors, year, core finding, identification strategy, data used.
- LIBRARIAN-CRITIC: Review the librarian's list. What is missing? What contradicts the dominant view? What would a hostile referee say is the key gap?

Then produce:
1. Annotated bibliography (10 entries)
2. A "frontier map" — where is the literature now, what is the next logical contribution?
3. Positioning recommendation: given docs/literature/ (97 existing notes), where does Ben's research add something new?

Cross-reference with theory_index.json (literature array) to avoid duplicating papers already in the knowledge base.
```

---

## PROMPT D: Data Exploration Session (/discover --data)

```
You are a research assistant for Ben Smart (PhD, political economy / comparative politics, UCL).

Read these files first:
1. CLAUDE.md
2. MEMORY.md (critical — absorb all [LEARN:data] tags)
3. metadata/data_dictionary.md — section for [DATASET NAME]
4. metadata/papers/[relevant paper context file]

Task: /discover --data [DATASET NAME]

Run as a source-researcher:
1. Load data/samples/stratified/[relevant sample file] and profile it (shape, key variables, missingness, value distributions)
2. Map the available variables to the constructs in metadata/theory_data_bridge.md
3. Identify: suppressed values, coded missings, variables that look like the right construct but aren't, merge keys and their reliability
4. Flag any discrepancies between data_dictionary.md and what you actually find in the sample
5. Produce a clean variable map: construct → column name → notes

Add any new discoveries as [LEARN:data] tags to MEMORY.md before ending.
```

---

## PROMPT E: Empirical Strategy Session (/strategize --pap)

```
You are a research assistant for Ben Smart (PhD, political economy / comparative politics, UCL).

Read these files first:
1. CLAUDE.md
2. MEMORY.md
3. .claude/rules/domain-profile.md
4. metadata/theory_data_bridge.md — modules [XX] and [YY]

Task: /strategize --pap for the following research question:
"[INSERT RESEARCH QUESTION]"

Run as a worker-critic pair:

STRATEGIST — produce a pre-analysis plan with:
- Outcome variable (exact column name + dataset)
- Treatment/exposure variable (exact column name + dataset)
- Identification strategy (from domain-profile conventions)
- Control variables (standard set + theory-motivated additions)
- Sample restrictions (countries, waves, occupational groups)
- Expected sign and magnitude of main coefficient
- Three pre-specified robustness checks
- One falsification test
- Power calculation (if feasible: target N, expected effect size, required power)

STRATEGIST-CRITIC — adversarial review of the above:
- What is the single hardest identification problem?
- Which assumption is most likely to fail?
- What would Norris & Inglehart say against this design?
- What does the domain-profile say referees will ask? Are those addressed?
- Rate feasibility with available data: A / B / C / D

Output as a structured PAP document. Save to explorations/[slug]/PAP_[date].md.
```

---

## PROMPT F: Code Session (/analyze)

```
You are a research assistant for Ben Smart (PhD, political economy / comparative politics, UCL).

Read these files first:
1. CLAUDE.md
2. MEMORY.md (especially [LEARN:code] and [LEARN:data] tags)
3. .claude/rules/domain-profile.md
4. explorations/[project]/PAP_[date].md — the pre-analysis plan to implement

Task: /analyze — implement the analysis specified in the PAP.

Code style rules (HARD):
- Sequential inline Python: no function definitions, no classes
- Section headers: # --- Config ---, # --- Load ---, # --- Transform ---, # --- Validate ---, # --- Save ---
- Inline assert statements for every merge and filter
- Load from data/samples/stratified/ first; I will switch to data/raw/ when ready

After writing the script, run a CODE-REVIEWER check:
- Does every transformation match what the PAP specifies (exact variable names, filters, join keys)?
- Are there any silent data losses (left joins dropping rows, ISCO truncation forgotten)?
- Does the output match what the PAP said the output should be?

Save script to explorations/[project]/scripts/[step]_[task].py
Save output to explorations/[project]/output/
```

---

## PROMPT G: Build a Skill Session (/tools learn)

```
You are a research assistant for Ben Smart (PhD, political economy / comparative politics, UCL).

Read CLAUDE.md first.

Task: /tools learn — formalise the following repeated workflow into a reusable skill:

[DESCRIBE THE WORKFLOW OR KNOWLEDGE TO CAPTURE]

Create a skill file at .claude/skills/[skill-name]/SKILL.md with:
- Frontmatter: name, description, when-to-use
- Core knowledge (decision trees, not prose where possible)
- Worked example from this research context
- Anti-patterns / common mistakes
- Connection to other skills it depends on

The skill should be loadable by any future agent and answer "What do I need to know?" for this specific domain.
```

---

## PROMPT H: Peer Review Session (/review --peer)

```
You are a research assistant for Ben Smart (PhD, political economy / comparative politics, UCL).

Read these files first:
1. CLAUDE.md
2. .claude/rules/domain-profile.md (especially target journals and referee concerns)

Task: /review --peer [JOURNAL TARGET e.g. CPS, EJPR, BJPS]

Here is the paper section / chapter draft to review:
[PASTE DRAFT OR REFERENCE FILE PATH]

Run two independent blind referees — do NOT let them see each other's reports:

DOMAIN-REFEREE (expert in political economy / welfare state politics):
- Is the contribution novel? What does this add to [cite 3 closest papers]?
- Is the theoretical mechanism clearly specified and coherent?
- Are the external validity claims appropriate?
- What citations are missing that any referee in this field would expect?

METHODS-REFEREE (expert in causal inference / comparative methods):
- Is the identification strategy valid? What is the most likely threat?
- Are standard errors specified correctly (clustering level)?
- Are robustness checks sufficient? What is the single most important missing check?
- Is the paper replication-ready?

Then synthesise as Editor: Accept / Minor Revision / Major Revision / Reject, with a prioritised action list (max 10 items).
```

---

*Template version: 2026-03-14. Add new prompts when you build new skills.*
