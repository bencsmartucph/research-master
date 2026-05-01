# Script Audit — `script_rti_descriptive.py`

**Reviewer:** coder-critic
**Date:** 2026-05-01
**Score:** 61 / 100
**Recommendation:** REVISE
**Overnight-safety verdict:** SAFE-WITH-CAVEATS

---

## Strategic Alignment: PARTIAL MATCH

What the brief asked for:
- Scatterplot of RTI vs. anti-immigration, faceted by country: **YES**
- 3-digit ISCO truncation for RTI: **NO** — falls back to 1-digit major-group proxy because `data/raw/shared_isco_task_scores/isco08_3d-task3.csv` is gitignored
- Source = Baccini sample: **NO** — switches to Im sample because Baccini lacks the immigration battery
- Anti-immigration index: **YES**

Both deviations documented in docstring + runtime stdout, and the brief anticipated fallback. But the figure caption / output filename does not encode the fallback — the PDF consumer cannot tell which sample produced the figure without re-reading the script.

---

## Issues Found

### 1. Hardcoded absolute path (-20)
Line 39: `REPO_ROOT = Path("/home/user/research-master")` — explicit project rule violation. Should be `Path(__file__).resolve().parents[2]` or env var. Largest single defect; destroys portability.

### 2. Source-substitution not encoded in figure/sidecar (-5)
`src_label` printed to stdout only. PDF consumer cannot tell Baccini vs Im sample without re-reading script.

### 3. RTI "z-like" major-group scalars are invented (-5)
Values (-1.5, +1.4, etc.) roughly track the Goos/Manning/Salomons direction but are not from a published task index. Axis label is honest ("major-group proxy, z-like") but downstream readers will treat the axis as if it carried real RTI metric.

### 4. Silent NaN drops on unmatched ISCO labels (-3)
Only `matched/total` printed. Unmatched-but-non-null labels dropped silently at `dropna`. No list of unmatched strings — invisible data loss if ESS adds new occupation strings.

### 5. Linear fit at n>=3 (-3)
A 3-point line is meaningless. With ~100 obs spread across multiple countries, per-panel n is 5–20. Threshold should be 10+ or include a CI band.

### 6. `sys.exit(0)` on fatal-branch failures (-2)
Should be non-zero exit code; currently looks like a graceful skip when it's actually a failure.

### 7. No author/date/project header (-1)
Convention, not rule.

---

## What the script gets right

- Module docstring with inputs, outputs, fallback chain
- Section headers (`# --- Config ---`, `# --- Path checks ---`, etc.)
- `Path(f).exists()` checks before reading
- Seeds set: `random.seed(42)`, `np.random.seed(42)`, separate RNG for jitter
- Inline asserts at every critical boundary
- `figures.md` rule compliance: `fig.suptitle("")`, serif fonts, no embedded title, panel labels via `ax.text`
- Defensive fallbacks: gracefully handles gitignored data/raw and lacking attitudes columns
- Comments explain WHY (not what) at every non-obvious choice

---

## Overnight-Safety Verdict

**SAFE-WITH-CAVEATS.** On this exact machine, the script will run, produce a PDF, and not corrupt anything.

**Failure modes that would cost Ben morning debug time:**

1. **Wrong-machine run.** If overnight mode ever dispatches to a different host (CI, laptop, container), absolute path fails and the run `sys.exit(0)`s — Ben wakes to no figure and a misleading "exited cleanly" status. **This is the worst failure mode here because it looks like a graceful skip rather than an error.**

2. **Provenance loss.** PDF doesn't say which sample it came from. If Ben opens it without re-reading the script, he assumes Baccini + canonical 3-digit RTI. It is neither.

3. **Silent data loss.** Unmatched ISCO labels drop without count. Future ESS waves with new occupation strings would shrink the sample invisibly.

None are destructive. But #1 and #2 would cost morning debug time and could propagate wrong provenance into commits or session reports.

---

## Recommendation: REVISE

Two minor changes lift this above 80:
1. Derive `REPO_ROOT = Path(__file__).resolve().parents[2]`
2. Embed source label in figure (subtitle text below panels OR sidecar `.txt`)
