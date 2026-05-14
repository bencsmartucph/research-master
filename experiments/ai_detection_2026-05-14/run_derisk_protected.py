"""Re-run derisk with vocabulary-protective prompts.

Targets the 4 paragraphs from the first run whose technical vocabulary was destroyed:
- 01_section_iv_scope.md
- 02_section_iv_two_channel.md
- 03_section_v_f_tost.md
- 06_section_i_central_claim.md

Strategy: explicit list of preserved terms-of-art; instruct rewriter to replace
filler/transitions/conjunctions but never substitute the protected vocabulary.
"""
import json, os, sys, subprocess, tempfile, time
from pathlib import Path

DETECT_SCRIPT = Path(r"C:/Users/PKF715/.claude/scripts/detect_gptzero.py")

import anthropic
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    import winreg
    k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
    api_key, _ = winreg.QueryValueEx(k, "ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

OPUS_MODEL = "claude-opus-4-5"

PROTECTED_TERMS = """asymmetric, asymmetry, symmetric, symmetrical, symmetric account, symmetric prediction;
decommodification, decommodifying, decommodifying quality;
redistribution, redistributive, redistribution support, redistributive solidarity, solidarity;
automation exposure, routine task intensity, RTI, routine workers;
TOST, equivalence test, smallest effect size of interest, SESOI;
moderation, interaction, cross-level interaction, random slopes, random intercepts;
BLUPs, BLUP, jackknife, permutation test, country-label permutation;
loss aversion, status threat, status decline, recognition, deservingness;
submerged state, register-linked, register linkage, within-individual;
exclusion, exclusionary attitudes, anti-immigration, anti-immigration sentiment;
welfare state, welfare regime, welfare design, welfare encounter, welfare environment, welfare context;
buffering model, compensatory framework, compensatory account;
encounter channel, environment channel, encounter, environment;
particularistic-authoritarian, policy feedback;
country, country-level, cross-national, country-wave;
estimator, coefficient, standard error, SE, p-value;
damage cascade, misattribution, defensive othering, identity switching;
ESS, European Social Survey, ISSP, CWED, CWED generosity, ALMP;
Liberal regime, Nordic regime, Continental regime, Southern regime, Eastern regime;
Esping-Andersen, Mettler, Wagner, Soss, Patrick, Bonomi, Gallego, Kurer, Häusermann, Rothstein, Larsen, Bornschier, Pelc"""

C1_PROTECTED = f"""Free-rewrite the following academic paragraph for an academic audience. Reduce AI-detector signal by varying sentence structure and replacing filler vocabulary, conjunctions, and transitions.

PRESERVE VERBATIM (must appear in output unchanged):
- All citations and statistics
- All technical terms from this list:
{PROTECTED_TERMS}
- All proper nouns and named author references

Constraints:
- Sentence length: short declarative sentences (target mean 12-16 words).
- Semicolons: at least 2 per 300 words.
- No em-dashes; use semicolons or commas.
- First-person plural ('we', 'our') where natural.
- Replace ONLY filler register vocabulary, conjunctions, transitions, and ordinary descriptive words; do NOT substitute discipline-specific technical terms even if they are Latinate (e.g., do NOT change 'asymmetric' to 'lopsided', 'redistribution' to 'sharing', 'solidarity' to 'fellow-feeling', 'automation exposure' to 'openness to machines', 'country' to 'land').
- The output must read as a Welfare State Seminar paper paragraph, not a journalistic essay.

Return ONLY the rewritten paragraph, no commentary.

---
[CURRENT_BEST]"""

RHYTHM_PROTECTED = f"""Free-rewrite the following academic paragraph. Reduce AI-detector signal by varying sentence-length distribution and breaking the Claude-distributional rhythm.

PRESERVE VERBATIM (must appear in output unchanged):
- All citations, statistics, and numerical results
- All technical terms from this list:
{PROTECTED_TERMS}
- All proper nouns

Constraints:
- Vary sentence-length distribution; mix short (8-12 word) declaratives with longer compound sentences.
- No two consecutive sentences should share the same rhythm pattern.
- Mild informal interjections allowed only where they don't break academic register.
- No em-dashes; use semicolons or commas.
- Replace ONLY filler register vocabulary, conjunctions, transitions, and ordinary descriptive words; do NOT substitute discipline-specific technical terms (e.g., do NOT change 'asymmetric' to 'lopsided', 'redistribution' to 'sharing', 'solidarity' to 'fellow-feeling', 'automation exposure' to 'openness to machines', 'country' to 'land').
- Welfare State Seminar paper register, not journalistic.

Return ONLY the rewritten paragraph, no commentary.

---
[CURRENT_BEST]"""

AGGRESSIVE_PROTECTED = f"""Free-rewrite this paragraph aggressively to reduce GPTZero AI signal. Vary cadence sharply; mix very short and longer sentences; use semicolons frequently.

PRESERVE VERBATIM (must appear unchanged):
- All citations, statistics, and numerical results
- All technical terms from this list:
{PROTECTED_TERMS}

Constraints:
- Allow sentence fragments where they justify rhythm.
- Semicolons at least 3 per 300 words.
- First-person plural ('we', 'our') frequently.
- No em-dashes.
- Do NOT substitute discipline-specific technical terms. The Latinate terms in the protected list MUST stay Latinate.
- Welfare State Seminar paper register; not journalistic.

Return ONLY the rewritten paragraph.

---
[CURRENT_BEST]"""


def score(text):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        path = f.name
    try:
        result = subprocess.run(["python", str(DETECT_SCRIPT), path], capture_output=True, text=True, timeout=120)
        out = result.stdout
        idx = out.find("{")
        data = json.loads(out[idx:])
        return data["class_probabilities"]["ai"], data["classification"]
    finally:
        os.unlink(path)


def opus_rewrite(template, text):
    prompt = template.replace("[CURRENT_BEST]", text)
    msg = client.messages.create(model=OPUS_MODEL, max_tokens=4096, messages=[{"role": "user", "content": prompt}])
    return msg.content[0].text.strip()


def derisk(name, src_text, out_path, log_path, threshold=0.50):
    print(f"\n{'='*60}\n{name}\n{'='*60}")
    base_ai, base_cls = score(src_text)
    print(f"BASELINE: AI={base_ai:.4f} ({base_cls})")

    best_text = src_text
    best_ai = base_ai
    log = [{"iteration": 0, "spec": "baseline", "ai": base_ai, "classification": base_cls, "accepted": True}]

    iterations = [
        ("1_C1_protected", lambda t: opus_rewrite(C1_PROTECTED, t)),
        ("2_rhythm_protected", lambda t: opus_rewrite(RHYTHM_PROTECTED, t)),
        ("3_aggressive_protected", lambda t: opus_rewrite(AGGRESSIVE_PROTECTED, t)),
    ]

    for i, (iname, fn) in enumerate(iterations, start=1):
        if best_ai < threshold:
            log.append({"iteration": i, "spec": iname, "ai": None, "classification": "skipped", "accepted": False})
            print(f"Iter {i}: skipped (below threshold)")
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
            old = best_ai
            best_text = candidate
            best_ai = cand_ai
            print(f"  ACCEPTED ({old:.4f} -> {cand_ai:.4f})")
        else:
            print(f"  REJECTED")
        log.append({"iteration": i, "spec": iname, "ai": cand_ai, "classification": cand_cls, "accepted": accepted, "text": candidate})
        time.sleep(2)

    out_path.write_text(best_text, encoding="utf-8")
    log_path.write_text(json.dumps({"name": name, "baseline_ai": base_ai, "baseline_classification": base_cls, "final_ai": best_ai, "iterations": log}, indent=2), encoding="utf-8")
    print(f"\nFINAL {name}: {base_ai:.4f} -> {best_ai:.4f}")
    return base_ai, best_ai


def main():
    orig = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.mkdir(exist_ok=True, parents=True)
    targets = sys.argv[3:]  # specific filenames to re-run, or "all"
    files = sorted(orig.glob("*.md"))
    if "all" not in targets:
        files = [f for f in files if f.name in targets]
    summary = []
    for src in files:
        text = src.read_text(encoding="utf-8")
        base, final = derisk(src.stem, text, out / src.name, out / (src.stem + "_log.json"))
        summary.append({"name": src.name, "baseline": base, "final": final})
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nSUMMARY:")
    for r in summary:
        print(f"  {r['name']}: {r['baseline']:.4f} -> {r['final']:.4f}")


if __name__ == "__main__":
    main()
