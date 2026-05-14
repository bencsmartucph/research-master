"""Multi-paragraph driver implementation of /derisk-paragraph.

Topic: welfare-political-economy (validated cell, Opus rewriter).
Iterations 1-3 (skip cross-model laundering by default to control cost) + iter 5 aggressive.
No-regression keep-rule.

Usage:
    python run_derisk_multi.py <originals_dir> <derisked_dir>

Reads all .md files in originals_dir, processes each, writes derisked outputs +
per-paragraph iteration logs to derisked_dir.
"""
import json, os, sys, subprocess, tempfile, time
from pathlib import Path

DETECT_SCRIPT = Path(r"C:/Users/PKF715/.claude/scripts/detect_gptzero.py")

# API setup
import anthropic

api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    import winreg
    k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
    api_key, _ = winreg.QueryValueEx(k, "ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

# Use claude-opus-4-5 (current production); 4.7 is preview-tier and not API-stable as of 2026-05-14
OPUS_MODEL = "claude-opus-4-5"

# Gemini optional
GEMINI_AVAILABLE = False
try:
    import google.generativeai as gen_ai
    gen_ai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    GEMINI_AVAILABLE = True
except ImportError:
    print("[WARN] google.generativeai not installed; cross-model iteration will fall back to second Opus pass")


def score(text):
    """Write text to a temp file, run detect_gptzero, return AI prob + classification."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        path = f.name
    try:
        result = subprocess.run(
            ["python", str(DETECT_SCRIPT), path],
            capture_output=True, text=True, timeout=120
        )
        out = result.stdout
        idx = out.find("{")
        data = json.loads(out[idx:])
        return data["class_probabilities"]["ai"], data["classification"]
    finally:
        os.unlink(path)


def opus_rewrite(prompt_template, text):
    prompt = prompt_template.replace("[CURRENT_BEST]", text)
    msg = client.messages.create(
        model=OPUS_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def gemini_rewrite(text):
    if not GEMINI_AVAILABLE:
        return opus_rewrite(RHYTHM_VARIANCE + "\n\nIMPORTANT: Use a markedly different sentence-cadence than the input.", text)
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


C1_STRUCTURAL = """Free-rewrite the following academic paragraph for an academic audience. Keep all claims, citations, and statistics. Apply these constraints exactly:
- Sentence length: short declarative sentences (target mean 12-16 words).
- Semicolons: at least 2 per 300 words.
- Compound modifiers: none (no hyphenated adjective phrases like 'outcome-oriented').
- Lexical: prefer Germanic/Anglo-Saxon vocabulary over Latinate; formal register.
- First-person plural ('we', 'our') where natural.
- No em-dashes; use semicolons or commas.
- ACADEMIC REGISTER: do not use journalistic phrasing like 'sets up shop', 'dark twin', 'playbook', 'goes round and round'. Welfare State Seminar paper register.

Return ONLY the rewritten paragraph, no commentary.

---
[CURRENT_BEST]"""

RHYTHM_VARIANCE = """Free-rewrite the following academic paragraph. Keep all claims, citations, and statistics. Apply these constraints:
- Vary sentence-length distribution across the paragraph; mix short (8-12 word) declaratives with longer compound sentences.
- Introduce mild informal interjections and idiosyncratic phrasing where they don't break academic register.
- No two consecutive sentences should share the same rhythm pattern.
- Prefer Germanic/Anglo-Saxon vocabulary over Latinate.
- No em-dashes; use semicolons or commas.
- ACADEMIC REGISTER: stay in welfare-state political economy register. No journalistic phrasing.

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
- ACADEMIC REGISTER: do not use journalistic phrasing. Welfare State Seminar paper register.

Return ONLY the rewritten paragraph, no commentary.

---
[CURRENT_BEST]"""


def derisk_paragraph(src_path, out_path, log_path, threshold=0.50):
    src = src_path.read_text(encoding="utf-8")
    name = src_path.stem
    print(f"\n{'='*60}\n{name}\n{'='*60}")

    base_ai, base_cls = score(src)
    print(f"BASELINE: AI={base_ai:.4f} ({base_cls})")

    best_text = src
    best_ai = base_ai
    log = [{"iteration": 0, "spec": "baseline", "ai": base_ai, "classification": base_cls, "accepted": True}]

    iterations = [
        ("1_C1_structural", lambda t: opus_rewrite(C1_STRUCTURAL, t)),
        ("2_rhythm_variance", lambda t: opus_rewrite(RHYTHM_VARIANCE, t)),
        ("3_cross_model_laundering", lambda t: opus_rewrite(OPUS_POLISH, gemini_rewrite(t))),
        ("5_aggressive_C1", lambda t: opus_rewrite(AGGRESSIVE_C1, t)),
    ]

    for i, (iname, fn) in enumerate(iterations, start=1):
        if best_ai < threshold:
            log.append({"iteration": i, "spec": iname, "ai": None, "classification": "skipped (threshold reached)", "accepted": False})
            print(f"Iter {i} {iname}: skipped (already below threshold)")
            continue
        print(f"\n--- Iter {i}: {iname} ---")
        try:
            candidate = fn(best_text)
        except Exception as e:
            log.append({"iteration": i, "spec": iname, "ai": None, "classification": f"error: {e}", "accepted": False})
            print(f"  ERROR: {e}")
            continue
        cand_ai, cand_cls = score(candidate)
        print(f"  Candidate: AI={cand_ai:.4f} ({cand_cls})")
        accepted = cand_ai < best_ai
        if accepted:
            old_best = best_ai
            best_text = candidate
            best_ai = cand_ai
            print(f"  ACCEPTED (improvement {old_best:.4f} -> {cand_ai:.4f})")
        else:
            print(f"  REJECTED (no improvement)")
        log.append({"iteration": i, "spec": iname, "ai": cand_ai, "classification": cand_cls, "accepted": accepted, "text": candidate})
        time.sleep(2)

    out_path.write_text(best_text, encoding="utf-8")
    with log_path.open("w") as f:
        json.dump({
            "name": name,
            "baseline_ai": base_ai,
            "baseline_classification": base_cls,
            "final_ai": best_ai,
            "iterations": log,
        }, f, indent=2)

    print(f"\nFINAL {name}: baseline {base_ai:.4f} -> best {best_ai:.4f}")
    return base_ai, best_ai


def main():
    if len(sys.argv) != 3:
        print("Usage: python run_derisk_multi.py <originals_dir> <derisked_dir>")
        sys.exit(1)

    orig_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(exist_ok=True, parents=True)

    summary = []
    for src in sorted(orig_dir.glob("*.md")):
        out_path = out_dir / src.name
        log_path = out_dir / (src.stem + "_log.json")
        base, final = derisk_paragraph(src, out_path, log_path)
        summary.append({"name": src.name, "baseline": base, "final": final, "delta": base - final})

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n{'='*60}\nSUMMARY\n{'='*60}")
    for r in summary:
        print(f"  {r['name']}: {r['baseline']:.4f} -> {r['final']:.4f} (delta -{r['delta']:.4f})")


if __name__ == "__main__":
    main()
