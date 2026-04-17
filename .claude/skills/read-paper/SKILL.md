---
name: read-paper
description: "Ingest a new paper (PDF, docx, or markdown). Converts heavy formats via subagent, produces a structured literature note, and updates the literature INDEX."
---

# /read-paper

**Usage:** `/read-paper path/to/file.pdf` or `/read-paper path/to/file.docx`

## Workflow

### Step 1: Identify format
- If `.pdf` → convert with `python -c "import pymupdf; doc=pymupdf.open('FILE'); [print(p.get_text()) for p in doc]"` or `pdftotext`
- If `.docx` → convert with `pandoc FILE -o /tmp/converted.md`
- If `.md` → read directly
- **Rule:** Do NOT read the full file in main context if >500 lines. Use a subagent.

### Step 2: Extract via subagent
Delegate to the **explorer** agent with this prompt:

```
Read the converted file and extract:
1. Full citation (authors, year, title, journal)
2. Research question (1 sentence)
3. Data and method (1 sentence: dataset, N, identification strategy)
4. Core finding (2-3 sentences: main result, sign, magnitude)
5. Key mechanism or theory (1 sentence)
6. Limitations (1 sentence)
7. Relevance to welfare-automation-populism research (1 sentence)
8. Which theory modules (01-15) this relates to

Return as structured markdown, max 200 words.
```

### Step 3: Write literature note
Save to `docs/literature/SLUG.md` using the standard format already in use.
- Slug format: `YYYY_authorlast_first_few_words.md`
- Include the full subagent summary plus any additional context

### Step 4: Update INDEX
Append one line to `docs/literature/INDEX.md`:
```
- SLUG.md | Core finding ≤80 chars | method | theory:XX,YY
```

### Step 5: Commit
```bash
git add docs/literature/SLUG.md docs/literature/INDEX.md
git commit -m "lit: add SLUG (via /read-paper)"
```

## What this replaces
The old librarian → librarian-critic pipeline. One skill, no scoring, no frontier maps.
