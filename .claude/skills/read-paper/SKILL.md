---
name: read-paper
description: "Ingest a new paper (PDF, docx, or markdown). Converts heavy formats via subagent, produces a structured literature note, and updates the literature INDEX."
---

# /read-paper

**Usage:** `/read-paper path/to/file.pdf` or `/read-paper path/to/file.docx`

## Workflow

### Step 1: Convert to markdown
Probe tool availability in order, use the first that works. Output path: use bash `$(mktemp -d)/converted.md` (works on Git Bash for Windows — avoids `/tmp` and cmd-quoting issues).

- **.pdf** — try in order:
  1. `python -c "import pymupdf" 2>/dev/null` → `python -c "import pymupdf,sys; [print(p.get_text()) for p in pymupdf.open(sys.argv[1])]" "$FILE" > "$OUT"`
  2. `pdftotext --version 2>/dev/null` → `pdftotext -layout "$FILE" "$OUT"`
  3. Else: fail with instruction "install pymupdf (`pip install pymupdf`) or poppler pdftotext"
- **.docx** — `pandoc --version 2>/dev/null` → `pandoc "$FILE" -o "$OUT"`; else fail with install hint
- **.md** — skip conversion, set `OUT=$FILE`
- **Scanned/image PDF check:** after conversion, if `wc -w "$OUT" < 200`, warn "likely scanned PDF, OCR not run — aborting; run OCR first" and exit without writing a lit note

### Step 2: Extract via subagent
Invoke the Agent tool with `subagent_type: general-purpose` (keep convention consistent with /critique — do NOT use named agents like `explorer` here; they carry their own framing). Prompt:

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
Save to `docs/literature/SLUG.md` using the template at `docs/literature/_TEMPLATE.md` (create it on first run if missing — mirror the structure of any existing note under `docs/literature/*.md`).

**Slug:** `YYYY_firstauthorlast_three_title_words.md`, lowercase, underscores. If file exists, append `_v2`, `_v3` etc. Never overwrite.

### Step 4: Update INDEX
Append one line to `docs/literature/INDEX.md`:
```
- SLUG.md | Core finding ≤80 chars | method | theory:XX,YY
```
- If theory modules unclear from the paper, write `theory:?` — do not invent
- Before appending, `grep -q "^- SLUG.md" INDEX.md` — if already present, update in place rather than duplicate

### Step 5: Report (do NOT auto-commit)
Print a one-line summary to the user:
```
✓ Wrote docs/literature/SLUG.md and appended INDEX.md entry. Review and commit manually.
```
Rationale: auto-commit sweeps unrelated dirty files and risks network-drive `.git/index.lock` issues (see global CLAUDE.md). The user commits when they're satisfied.

## What this replaces
The old librarian → librarian-critic pipeline. One skill, no scoring, no frontier maps.
