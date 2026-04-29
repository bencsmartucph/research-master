# Gemini Task: Generate Literature INDEX

## Context
You are working in the `Research_Master` repository. This is an academic research project about how economic disruption shapes political preferences. There are 97 literature note files in `docs/literature/`, each summarizing a research paper. Your job is to create a greppable one-line-per-paper index.

## Goal
Create `docs/literature/INDEX.md` — a flat, greppable literature index with one line per paper.

## Steps

### 1. Read `docs/theory/theory_index.json`
This JSON file contains mappings between theory modules (01-15) and the literature notes. Use it as your primary source for which theory modules each paper relates to.

### 2. Process each file in `docs/literature/`
For each of the 97 `.md` files, extract:
- **Filename** (keep exactly as-is)
- **Core finding** — ≤80 characters summarizing the paper's main result
- **Method** — one of: `panel FE`, `DiD`, `RDD`, `IV`, `cross-sectional`, `survey experiment`, `qualitative`, `review`, `descriptive`, `mixed methods`, `multilevel`
- **Theory modules** — which modules 01-15 the paper relates to (use theory_index.json, or infer from content if not found)

### 3. Write `docs/literature/INDEX.md`
Format:
```markdown
# Literature Index

> One-line greppable index of 97 literature notes. Updated YYYY-MM-DD.
> Format: `filename | core finding | method | theory modules`

- 2016_patrick_living_with_and_responding_to_the.md | How workers respond to precarity through coping strategies | qualitative | theory:04,09
- 2019_hameleers_reinemann_schmuck_and_fawzi_pa.md | Populist framing increases blame attribution to elites and outgroups | survey experiment | theory:12,15
...
```

### 4. Quality checks
- Line count should equal 97 (one per file in `docs/literature/`)
- No line should exceed 120 characters total
- Every file in `docs/literature/` must appear exactly once
- Sort alphabetically by filename

### 5. Write build log
Save to `docs/literature/INDEX_BUILD_LOG.md`:
```markdown
# INDEX Build Log

**Date:** YYYY-MM-DD
**Files processed:** 97
**Method:** Read each .md file, extracted core finding, classified method, mapped to theory modules via theory_index.json

## Ambiguous Files
- [list any files where the summary was hard to write in ≤80 chars]

## Uncertain Theory Module Assignments
- [list any files where theory module mapping was unclear]

## Method Classification Decisions
- [document any judgment calls about method classification]
```

## Important Notes
- Do NOT modify any existing literature note files
- Do NOT modify theory_index.json
- The index is meant to be grep-searchable — keep each line self-contained
- When in doubt about a finding summary, prioritize the paper's main empirical result over theoretical contributions
