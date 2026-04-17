# Heavy Reads Convention

> Files that are too large for main context must be delegated or converted.

## Rule

**Never read the following in main context:**
- `.pdf` files (any size)
- `.docx` files (any size)
- Files > 500 lines
- `metadata/data_dictionary.md` (2.8 MB — read specific sections only)
- `analysis/final_analysis_pipeline.py` (1,320 lines — ask subagent for targeted summary)
- Any `.dta` file (binary, use pyreadstat in a script)

## Instead

1. **For PDFs:** Use `/read-paper` skill, or `pdftotext` / `pymupdf` to convert first
2. **For .docx:** Use `pandoc file.docx -o file.md`
3. **For long pipelines:** Delegate to explorer agent: "grep the pipeline for [concept] and summarize in 50 words"
4. **For data dictionary:** Grep for the variable name: `grep -A5 'variable_name' metadata/data_dictionary.md`
5. **For .dta files:** Write a small script, don't try to read binary

## Why

Main context has finite capacity. A 1,320-line pipeline or 2.8 MB data dictionary consumes ~30% of a session's working memory. Delegating the read and receiving a 50-word summary is 100x more efficient.

## Subagent patterns

```
Explorer: "find the 3 lit notes most relevant to redistribution-as-recognition"
Explorer: "grep the pipeline for the CWED merge logic and summarize in 50 words"
Explorer: "read metadata/data_dictionary.md and list all variables containing 'immig'"
```
