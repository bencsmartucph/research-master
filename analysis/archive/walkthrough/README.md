# Pedagogical Walkthrough Scripts (Archived)

**Status:** Archived 2026-05-04 per `audit_and_review_2026-05-04.md` Action 6.

These scripts produced the figures and interactive HTML files in `outputs/figures/walkthrough/` that are embedded in `docs/empirical_walkthrough_v1.md`. They are pedagogical infrastructure: step-by-step explanations of clustering, cross-level interactions, and figure generation. They are NOT used by the canonical paper pipeline (`scripts/random_slopes_models.py`).

**Files:**
- `walkthrough_interactive.py` — full pipeline walkthrough (condensed)
- `walkthrough_cluster_se_interactive.py` — clustering logic (Plotly interactive)
- `walkthrough_cluster_se_static.py` — clustering logic (static PNG mirror)
- `walkthrough_cross_level_interactive.py` — cross-level interactions (RTI × CWED)
- `walkthrough_figures.py` — figure regeneration with annotations (8 PNGs + 3 Plotly HTMLs)
- `fix_plots_ab.py` — March 16 hotfix for plot grid layout (no longer needed; original notebook bug)

**To re-run** (if master CSV changes):
```bash
python analysis/archive/walkthrough/walkthrough_figures.py  # regenerates outputs/figures/walkthrough/
```

**Why archived:** They lived alongside canonical pipeline scripts in `analysis/` and were starting to generate confusion about which scripts were canonical. Moving them clarifies that the canonical headline-number pipeline is `scripts/random_slopes_models.py`.
