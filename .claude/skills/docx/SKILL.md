---
name: docx
description: "Build a .docx document from markdown source. Use when generating Word documents for submission, assignment hand-in, or any deliverable requiring proper formatting."
---

# /docx — Build submission document

**Usage:** `/docx <source.md>` or `/docx <source.md> --template <reference.docx>`

Builds a properly formatted .docx from a markdown source file using pandoc with a reference document for styling.

---

## Pre-flight (before any build)

1. **Identify the formatting source.** Ask: "Do you have a previously submitted/graded document I should match?" A user's own graded submission is ALWAYS more authoritative than a HANDOVER, brief, or secondary instruction file. If a reference doc exists, use it as `--reference-doc`. Do not invent formatting specs.

2. **Verify pandoc is available.** Run `pandoc --version`. If missing, stop and say so.

3. **Inventory what the source contains:**
   - Images/figures referenced via `![](path)` — verify each path exists
   - LaTeX math (`$...$` or `$$...$$`) — will become native Word equations
   - Tables — verify they render (pipe tables need the `pipe_tables` extension)
   
4. **If the source references figures that exist as separate files** (PNGs, PDFs), note their paths. These MUST survive the build. After building, verify they are embedded.

---

## Build recipe

```powershell
pandoc "<source.md>" `
  --from markdown `
  --to docx `
  --reference-doc="<template.docx>" `
  --resource-path="<dir containing images>" `
  -o "<output.docx>"
```

**Key flags:**
- `--reference-doc` carries font, spacing, heading styles, footer/page numbers from the template
- `--resource-path` tells pandoc where to find images referenced in the markdown
- For math-heavy docs, `--from markdown` (not `gfm`) handles `$...$` reliably

---

## Post-build verification (MANDATORY)

After every build, verify ALL of these before declaring done:

1. **Charts/figures survived:**
   ```powershell
   # Count embedded images in the docx
   python -c "import zipfile; z=zipfile.ZipFile('<output.docx>'); print([f for f in z.namelist() if f.startswith('word/media/')])"
   ```
   If fewer images than expected → the build lost charts. Fix before reporting success.

2. **Font and spacing match template:**
   ```powershell
   python -c "import zipfile; z=zipfile.ZipFile('<output.docx>'); print(z.read('word/styles.xml').decode()[:2000])"
   ```
   Check `w:sz` (font size in half-points: 22=11pt, 24=12pt) and `w:spacing` values.

3. **Math rendered (if applicable):**
   ```powershell
   python -c "import zipfile; z=zipfile.ZipFile('<output.docx>'); xml=z.read('word/document.xml').decode(); print(f'Equations: {xml.count(\"m:oMath\")}'); print(f'Literal LaTeX: {\"\\\\frac\" in xml or \"\\\\sqrt\" in xml}')"
   ```
   Equations count should be >0 if source had math. Literal LaTeX in `w:t` runs means conversion failed.

4. **No orphan references:** grep the document XML for figure/table captions that reference content not present.

---

## Known failure modes (from experience)

| Failure | Cause | Fix |
|---------|-------|-----|
| Charts disappear after rebuild | Source .md doesn't have `![](path)` lines, or `--resource-path` wrong | Re-add image references; verify paths before build |
| Wrong font/spacing | No `--reference-doc`, or using specs from a brief instead of actual template | Always use the user's own graded/submitted doc as reference |
| Math renders as literal `$x^2$` | Using `--from gfm` which doesn't parse dollar-math | Use `--from markdown` |
| "12pt 1.5 spacing" doesn't match actual style | Formatting spec came from a secondary source (handover/brief) not the primary template | Inspect the actual template XML; user's submitted doc wins |
| PDF export fails | No LibreOffice on Windows PATH; sandbox-only converter | Tell user: open in Word → File → Save As → PDF. Don't pretend you can do it. |

---

## Scope control

- **Single source of truth:** the .md is canonical. Edits go in the .md; the .docx is derived. Never edit the .docx directly.
- **Don't restructure during a docx build.** If the user asks to "build the docx" and also "restructure the sections," do the restructure FIRST in the .md, verify it, THEN build. Mixing them is how charts get lost and versions diverge.
- **Under time pressure:** build once, verify once, deliver. Do not iterate formatting. If something looks wrong, flag it and let the user decide whether to fix or submit as-is.
