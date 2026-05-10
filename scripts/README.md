# scripts/ — Reproducible build & analysis commands

> **Why this file exists:** to stop re-deriving build commands every session. If a script lives here, the command to run it lives here too. New session, new Claude — the pandoc/docx/figure recipe is already codified.

**Convention:** any time you and Claude work out a multi-step build (pandoc invocation, docx assembly, figure pipeline, slide render) that would otherwise be re-derived next session, capture it as a numbered or named script in this folder and add a one-line entry below.

---

## Document builds

| Script | What it does | Run from repo root |
|--------|--------------|--------------------|
| `build_submission_docx.py` | Converts `manuscripts/paper_draft_v4_final.md` → AER-style `paper_final_submission.docx` (Times New Roman, single-spaced, inline markdown parser, `python-docx`) | `python scripts/build_submission_docx.py` |
| `_check_docx.py` | Quick sanity check on the produced docx (paragraph count, headings) | `python scripts/_check_docx.py` |
| `../talks/2026-05-04_seminar/build_slides.py` | Builds the seminar `.pptx` deck (`python-pptx`, embeds figures from `outputs/figures/`) | `python talks/2026-05-04_seminar/build_slides.py` |

**Slide rendering (Quarto, no script — direct CLI):**
```powershell
quarto render talks/2026-05-04_seminar/slides.qmd --embed-resources
```
The `--embed-resources` CLI flag is required; the YAML option alone does not produce the self-contained 8 MB RevealJS file.

---

## Data loading & sampling

| Script | What it does | Run |
|--------|--------------|-----|
| `load_ess.py` | Reusable loader for ESS waves; labels, merges, ISCO truncation | imported by other scripts |
| `make_stratified_samples.py` | Generates 200-row stratified samples from large `.dta` files (>10 MB) into `data/samples/` | `python scripts/make_stratified_samples.py` |

---

## Analysis (paper §V and robustness)

| Script | What it does | Run |
|--------|--------------|-----|
| `create_figures_final.py` | Publication figures for §V (RTI × CWED, marginal effects, regime panels) → `outputs/figures/` | `python scripts/create_figures_final.py` |
| `random_slopes_models.py` | Models 2–5 with `re_formula='~task_z'` (random slopes); CWED robustness with GDP/Gini macro controls | `python scripts/random_slopes_models.py` |
| `cwed_subcomponents_analysis.py` | Decomposes composite CWED into three sub-components (UI, sickness, pensions) | `python scripts/cwed_subcomponents_analysis.py` |
| `cwed_subcomponents_extended.py` | Same decomposition under random-slopes spec | `python scripts/cwed_subcomponents_extended.py` |
| `issp_solidarity_leg.py` | ISSP 2006 robustness leg: RTI × CWED on unemployment-spending support (comparator to Model 3) | `python scripts/issp_solidarity_leg.py` |
| `regional_sanity_check.py` | Regional-level (NUTS) test of the §V.D country-level finding | `python scripts/regional_sanity_check.py` |

---

## Learning resource exporters

| Script | What it does | Run |
|--------|--------------|-----|
| `export_recall_to_anki.py` | Walks `docs/learning_econometrics/*.md` chapters, builds Anki-importable TSV from recall prompts and Try-this exercises | `python scripts/export_recall_to_anki.py` |
| `export_chapter_to_notion.py` | Emits a Notion-ingestion payload for one chapter (uses YAML frontmatter from `_template_chapter.md`) | `python scripts/export_chapter_to_notion.py <chapter.md>` |

---

## Adding a new build script — the pattern

When you and Claude solve a multi-step build for the first time:

1. Save the working command sequence as `scripts/<verb>_<noun>.py` with a top docstring stating purpose, inputs (absolute paths or relative to repo root), and outputs.
2. Add a one-line row to the relevant table above.
3. If it's a deadline-critical build (paper docx, slide deck), also reference it from the relevant `STATUS.md` so future-you can grep.
4. Use absolute paths *inside the script* if it touches files outside `scripts/`; the caller should always be able to run from repo root without `cd`.

This is the prevention layer for the "why does this break every session" problem. The fallback (pre-deadline preflight dry-run) only catches breakage; capturing the command here prevents re-derivation in the first place.

---

## Conventions

- **Encoding for Danish characters:** `encoding='utf-8-sig'`, fallback `latin-1` (per global CLAUDE.md).
- **Stochastic scripts:** `np.random.seed(...)` once at top.
- **No hardcoded relative paths inside functions** — set absolute `ROOT = Path(...)` near the top.
- **Output verbosity:** scripts print 5–20 lines max; pipe heavy output through `head` / `tail` if needed.
- **Don't dispatch subagents to write into `.claude/`** — write scripts from the main session only.
