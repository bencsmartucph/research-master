# Heavy Reads Convention

> Files that are too large for main context must be delegated, converted, or chunked. Updated 2026-05-10 to reflect the higher-tier usage plan and a documented incident where a delegated analytical subagent returned confident-but-wrong stats.

## Rule

### Always heavy (delegate or convert before reading)

- `.pdf` files (any size) — convert with `pdftotext` or use `/read-paper`
- Files > 2000 lines — chunk or summarise
- `metadata/data_dictionary.md` (2.8 MB — read specific sections only via grep)
- `analysis/final_analysis_pipeline.py` (1,320 lines — chunk-read or summarise)
- Any `.dta` file (binary, use pyreadstat in a script)

### Acceptable in main context (was previously heavy)

- `.docx` files **after** pandoc conversion to `.md`, when the resulting `.md` is under 2000 lines
- Markdown / Python / R / TeX files of 500-2000 lines, when calibration accuracy or analytical fidelity matters more than context economy
- Any file the user has explicitly @-mentioned — read directly, never glob to "find" it

The previous 500-line ceiling was too tight for the higher-tier usage plan and forced delegations that lost important detail. The new ceiling is 2000 lines or `.pdf`-or-binary, whichever is stricter.

## Always before reading

1. **For PDFs:** Use `/read-paper` skill, or `pdftotext` / `pymupdf` to convert first.
2. **For .docx:** Use `pandoc file.docx -o file.md`, then read the `.md` directly if under 2000 lines.
3. **For long pipelines (>2000 lines):** Chunk-read with offset/limit or delegate to a subagent.
4. **For data dictionary:** Grep for the variable name: `grep -A5 'variable_name' metadata/data_dictionary.md`
5. **For .dta files:** Write a small script, never try to read binary.

## Subagent contract — when you DO delegate

A subagent doing analytical work (counts, stats, stylometry, structural mapping) **must** return:

1. **Raw data alongside the summary.** Counts AND a sample of the actual matches (e.g., five line-numbered example occurrences). Not just "found 12 instances of X" but "found 12 instances; here are five with line numbers".
2. **The exact method used.** Regex pattern, grep flags, sentence-tokeniser choice, chunk boundaries. Not "I counted sentences" but "I split on `[.!?]\s+` then filtered tokens >2 chars".
3. **A confidence note when the method is brittle.** "Sentence count may be inflated by citation periods (`Schmidt, V. A.`)"; "regex won't catch hyphen-as-em-dash if pandoc collapsed spaces".

If a subagent returns only summary stats with no raw data or method, **do not trust the analysis.** Either re-dispatch with the contract, or read the file directly within the new ceiling.

This rule exists because of a 2026-05-10 incident: a delegated voice-stylometry agent reported "0.0 hyphen-as-em-dash density" and "first-person 2.2/1k" on a 671-line `.docx`-derived `.md`; direct read showed ~2.4/1k hyphen-as-em-dash and ~1.7/1k first-person. The agent's regex missed the hyphen pattern entirely, and its sentence tokeniser broke at citation periods. The summary read confidently and led to wrong calibration recommendations until the file was read directly. The contract above prevents recurrence.

## Why

Main context has finite capacity. A 2.8 MB data dictionary or a 5000-line pipeline still consumes ~30% of working memory if read whole. Delegation is the right tool when (a) the file is genuinely too large to read, AND (b) the task is summarisation or targeted lookup, not stylometry/counting/raw-evidence verification.

When the task is calibration or analytical fidelity, **prefer direct reading within the new ceiling over delegation.** A 1500-line direct read costs context but gives ground truth. A delegation gives a summary that may or may not be right.

## Subagent patterns (still useful)

```
Explorer: "find the 3 lit notes most relevant to redistribution-as-recognition"
Explorer: "grep the pipeline for the CWED merge logic and summarise in 50 words"
Explorer: "read metadata/data_dictionary.md and list all variables containing 'immig'"
```

These are summary/lookup tasks where the agent can't easily be wrong about the structure of the answer. Use the subagent contract above for anything analytical.
