"""Driver implementation of /derisk-paragraph for section_iiid_original.md.

Topic: welfare-political-economy (validated cell, Opus rewriter).
Iterations 1-5 per skill spec; no-regression keep-rule.
"""
import json, os, sys, subprocess, tempfile, time
from pathlib import Path

REPO = Path(r"C:/Users/PKF715/Documents/claude_repos/Research_Master")
EXPT = REPO / "experiments/ai_detection_2026-05-11"
DETECT_SCRIPT = Path(r"C:/Users/PKF715/.claude/scripts/detect_gptzero.py")

# Read source
src = (EXPT / "section_iiid_original.md").read_text(encoding="utf-8")

# API setup
import anthropic

# ANTHROPIC: try env first, fall back to winreg
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    import winreg
    k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
    api_key, _ = winreg.QueryValueEx(k, "ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

# Gemini optional — skip cross-model iteration if not installed
GEMINI_AVAILABLE = False
try:
    import google.generativeai as gen_ai
    gen_ai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    GEMINI_AVAILABLE = True
except ImportError:
    print("[WARN] google.generativeai not installed; cross-model iteration will fall back to Opus polish only")


def score(text):
    """Write text to a temp file, run detect_gptzero, return AI prob."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        path = f.name
    try:
        result = subprocess.run(
            ["python", str(DETECT_SCRIPT), path],
            capture_output=True, text=True, timeout=120
        )
        # Parse JSON from stdout (may have a warning line first)
        out = result.stdout
        # Find first '{'
        idx = out.find("{")
        data = json.loads(out[idx:])
        return data["class_probabilities"]["ai"], data["classification"]
    finally:
        os.unlink(path)


def opus_rewrite(prompt_template, text):
    """Call Claude Opus with the given template, return rewritten text."""
    prompt = prompt_template.replace("[CURRENT_BEST]", text)
    msg = client.messages.create(
        model="claude-opus-4-5",  # use opus 4.5 since 4.7 may not be available
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def gemini_rewrite(text):
    """Cross-model laundering via Gemini 2.5 Pro. Falls back to second Opus pass if Gemini unavailable."""
    if not GEMINI_AVAILABLE:
        # Fallback: second Opus pass with different temperature / phrasing
        return opus_rewrite(RHYTHM_VARIANCE + "\n\nIMPORTANT: Use a markedly different sentence-cadence than the input; avoid mirroring the input's rhythm.", text)
    prompt = (
        "Rewrite the following academic paragraph in your own register, "
        "preserving all claims, citations, and statistics. Vary sentence "
        "length; mix short and long sentences; no em-dashes. Return only "
        "the paragraph.\n\n"
        f"{text}"
    )
    model = gen_ai.GenerativeModel("gemini-2.5-pro")
    resp = model.generate_content(prompt)
    return resp.text.strip()


# Prompt templates
C1_STRUCTURAL = """Free-rewrite the following academic paragraph for an academic audience. Keep all claims, citations, and statistics. Apply these constraints exactly:
- Sentence length: short declarative sentences (target mean 12-16 words).
- Semicolons: at least 2 per 300 words.
- Compound modifiers: none (no hyphenated adjective phrases like 'outcome-oriented').
- Lexical: prefer Germanic/Anglo-Saxon vocabulary over Latinate; formal register.
- First-person plural ('we', 'our') where natural.
- No em-dashes; use semicolons or commas.

Return ONLY the rewritten paragraph, no commentary.

---
[CURRENT_BEST]"""

RHYTHM_VARIANCE = """Free-rewrite the following academic paragraph. Keep all claims, citations, and statistics. Apply these constraints:
- Vary sentence-length distribution across the paragraph; mix short (8-12 word) declaratives with longer compound sentences.
- Introduce mild informal interjections and idiosyncratic phrasing where they don't break academic register.
- No two consecutive sentences should share the same rhythm pattern.
- Prefer Germanic/Anglo-Saxon vocabulary over Latinate.
- No em-dashes; use semicolons or commas.

Return ONLY the rewritten paragraph, no commentary.

---
[CURRENT_BEST]"""

OPUS_POLISH = """Lightly polish the following paragraph for academic register, fixing any awkward phrasing while preserving the sentence structure, sentence-length variance, and content. Do not lengthen sentences. Do not introduce em-dashes. Return only the polished paragraph.

[CURRENT_BEST]"""

AGGRESSIVE_C1 = """Free-rewrite the following paragraph for an academic audience. Keep all claims, citations, and statistics. Apply these constraints exactly:
- Sentence length: very short declarative sentences (target mean 8-12 words).
- Allow sentence fragments where rhythm justifies them.
- Semicolons: at least 3 per 300 words.
- First-person plural ('we', 'our') at least twice per 100 words.
- Compound modifiers: none.
- Lexical: prefer Germanic/Anglo-Saxon vocabulary over Latinate.
- No em-dashes; use semicolons or periods.

Return ONLY the rewritten paragraph, no commentary.

---
[CURRENT_BEST]"""

# Baseline
base_ai, base_cls = score(src)
print(f"BASELINE: AI={base_ai:.4f} ({base_cls})")

best_text = src
best_ai = base_ai
log = [{"iteration": 0, "spec": "baseline", "ai": base_ai, "classification": base_cls, "accepted": True}]

THRESHOLD = 0.50

for i, (name, fn) in enumerate([
    ("1_C1_structural", lambda t: opus_rewrite(C1_STRUCTURAL, t)),
    ("2_rhythm_variance", lambda t: opus_rewrite(RHYTHM_VARIANCE, t)),
    ("3_cross_model_laundering", lambda t: opus_rewrite(OPUS_POLISH, gemini_rewrite(t))),
    ("5_aggressive_C1", lambda t: opus_rewrite(AGGRESSIVE_C1, t)),
], start=1):
    if best_ai < THRESHOLD:
        log.append({"iteration": i, "spec": name, "ai": None, "classification": "skipped (threshold reached)", "accepted": False})
        continue
    print(f"\n=== Iteration {i}: {name} ===")
    try:
        candidate = fn(best_text)
    except Exception as e:
        log.append({"iteration": i, "spec": name, "ai": None, "classification": f"error: {e}", "accepted": False})
        print(f"  ERROR: {e}")
        continue
    cand_ai, cand_cls = score(candidate)
    print(f"  Candidate: AI={cand_ai:.4f} ({cand_cls})")
    accepted = cand_ai < best_ai
    if accepted:
        best_text = candidate
        best_ai = cand_ai
        print(f"  ACCEPTED (improvement from {best_ai:.4f})")
    else:
        print(f"  REJECTED (no improvement)")
    log.append({"iteration": i, "spec": name, "ai": cand_ai, "classification": cand_cls, "accepted": accepted, "text": candidate})
    time.sleep(2)  # gentle rate-limit

# Save best
(EXPT / "section_iiid_derisked_best.md").write_text(best_text, encoding="utf-8")

# Save log
with (EXPT / "derisk_iteration_log.json").open("w") as f:
    json.dump({
        "baseline_ai": base_ai,
        "baseline_classification": base_cls,
        "final_ai": best_ai,
        "final_text_path": "section_iiid_derisked_best.md",
        "iterations": log,
    }, f, indent=2)

print(f"\n=== FINAL ===")
print(f"Baseline AI: {base_ai:.4f}")
print(f"Final AI:    {best_ai:.4f}")
print(f"Best at:     {next((r['spec'] for r in reversed(log) if r['accepted']), 'baseline')}")
print(f"Log saved to derisk_iteration_log.json")
