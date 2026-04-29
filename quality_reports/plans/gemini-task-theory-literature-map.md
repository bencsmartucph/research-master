# Gemini Task: Build Theory README and Literature Map

## Context
You are working in the `Research_Master` repository. There are 15 theory modules in `docs/theory/` and 97 literature notes in `docs/literature/`. Your job is to create two new bridging files that map between theory and literature, following the pattern of the existing `metadata/theory_data_bridge.md`.

## Goal
Create two files:
1. `docs/theory/README.md` — theory module quick-reference with key papers per module
2. `metadata/literature_map.md` — detailed theory → literature mapping (like theory_data_bridge.md but for papers)

---

## Step 1: Read Reference Files

Before starting, read these files to understand the patterns:
- `metadata/theory_data_bridge.md` — THIS IS YOUR TEMPLATE. Match its style, depth, and formatting.
- `docs/theory/theory_index.json` — machine-readable module metadata with lit note links
- All 15 theory module files in `docs/theory/` (01 through 15)

## Step 2: Create `docs/theory/README.md`

This is the Theory Module Quick Reference, moved from the old CLAUDE.md. Format:

```markdown
# Theory Module Quick Reference

> Load this file when you need to identify which theory modules are relevant to your task.
> For full module prose, read `docs/theory/XX_module_name.md`.
> For theory → data mappings, see `metadata/theory_data_bridge.md`.
> For theory → literature mappings, see `metadata/literature_map.md`.

---

## I. Vulnerability Foundations

### 01 — Embedded Liberalism & Economic Vulnerability
Trade + welfare compensation failing. The bargain between openness and protection, and its breakdown.

**Key papers:**
- burgoon_van_noort_rooduijn_and_underhill_2019.md — Embedded liberalism and populism
- brian_burgoon_and_wouter_schakel_2022.md — Embedded liberalism under duress
- [3-5 more relevant papers from docs/literature/]

### 02 — Automation & Technological Change
RTI/routineness → anticipated status decline → radical right support.

**Key papers:**
- kurer_2020.md — Declining middle, occupational change
- [4-6 more relevant papers]

[... continue for all 15 modules ...]
```

For each module:
- Write a 1-2 sentence summary of the core construct
- List 5-10 key papers from `docs/literature/` with a one-line description each
- Use `theory_index.json` as primary source for paper-module mappings
- If `theory_index.json` links are insufficient, read the theory module file and match paper topics

## Step 3: Create `metadata/literature_map.md`

Follow the EXACT structural pattern of `metadata/theory_data_bridge.md`. Format:

```markdown
# 📚 Literature Map

> **Purpose:** Maps each of the 15 theory modules to the most relevant papers in `docs/literature/`.
> **How to use:** When writing a section related to a theory module, come here to find the key papers.
> **See also:** `docs/theory/README.md` for theory summaries · `docs/literature/INDEX.md` for greppable index.

---

## Navigation

| Module | Theory | Top Papers | Coverage |
|--------|--------|-----------|----------|
| [01](#01-embedded-liberalism) | Embedded Liberalism | 6 | Strong |
| [02](#02-automation) | Automation & Technological Change | 8 | Very Strong |
| ... | ... | ... | ... |

---

## 01: Embedded Liberalism & Economic Vulnerability

### Top Papers (ranked by relevance)

| # | Paper | Core Finding | Method |
|---|-------|-------------|--------|
| 1 | burgoon_van_noort_rooduijn_and_underhill_2019.md | ... | ... |
| 2 | brian_burgoon_and_wouter_schakel_2022.md | ... | ... |
| ... | ... | ... | ... |

### Key Empirical Findings These Papers Establish
- Trade exposure increases support for compensation (Burgoon et al. 2019)
- The embedded liberalism bargain is weakening in practice (Burgoon & Schakel 2022)
- [3-5 more bullet points]

### Gaps in Literature Coverage
- [Note any theoretical concepts in the module that lack strong empirical papers]

---

[... repeat for all 15 modules ...]
```

For each module:
- Rank papers by relevance to that module (most relevant first)
- Include one-line finding summary and method for each paper
- Write 3-5 bullet points summarizing the key empirical findings
- Note any gaps where the theory module discusses concepts not well-covered by the 97 papers
- Assess coverage as: Very Strong (8+ papers), Strong (5-7), Moderate (3-4), Thin (1-2), Gap (0)

## Step 4: Quality Checks

- Every paper in `docs/literature/` should appear in at least one module in the literature map
- No paper should appear in more than 4 modules (if it does, prioritize the top 2-3)
- The README should have 5-10 papers per module
- The literature map should have coverage assessments for all 15 modules

## Step 5: Write Build Log

Save to `metadata/LITERATURE_MAP_BUILD_LOG.md`:
```markdown
# Literature Map Build Log

**Date:** YYYY-MM-DD

## Coverage Summary
| Module | Coverage | Paper Count |
|--------|----------|-------------|
| 01 | Strong | 6 |
| 02 | Very Strong | 8 |
| ... | ... | ... |

## Papers Not Clearly Mapped
- [list any papers that didn't fit any module well]

## Modules with Thin Coverage
- [list any modules with <3 papers]

## Ranking Decisions
- [document how you decided relevance ranking]
```

## Step 6: Git Commit

```bash
git add docs/theory/README.md metadata/literature_map.md metadata/LITERATURE_MAP_BUILD_LOG.md
git commit -m "feat: add theory README and literature map (Phase 2)

- Create docs/theory/README.md (theory quick-ref + key papers per module)
- Create metadata/literature_map.md (theory → top papers, mirrors theory_data_bridge pattern)
- Add build log documenting coverage and decisions"
```

## Important Notes
- Do NOT modify existing theory module files
- Do NOT modify existing literature note files
- Do NOT modify theory_data_bridge.md
- The literature_map.md should MIRROR the structure of theory_data_bridge.md — read it carefully first
- When ranking papers, prioritize empirical papers over review/theoretical papers
