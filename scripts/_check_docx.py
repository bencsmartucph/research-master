from docx import Document
import os

doc = Document("manuscripts/paper_final_submission.docx")
paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
size_kb = os.path.getsize("manuscripts/paper_final_submission.docx") / 1024
print("File size: %.1f KB" % size_kb)
print("Total paragraphs: %d" % len(paras))
print()

checks = [
    ("Abstract paradox opener",      any("Why does automation" in p for p in paras)),
    ("More importantly pivot",       any("More importantly" in p for p in paras)),
    ("Spend more punchy line",       any("Spend more" in p for p in paras)),
    ("Three limits opener",          any("Three limits matter" in p for p in paras)),
    ("Wagner P. 2022",               any("Wagner, P." in p for p in paras)),
    ("Ciccolini 2025",               any("Ciccolini" in p and "2025" in p for p in paras)),
    ("Caselli 2021 ref",             any("Caselli" in p and "2021" in p for p in paras)),
    ("Appendix A heading",           any(p == "Appendix A: Robustness Checks" for p in paras)),
    ("Appendix B heading",           any(p == "Appendix B: Education Moderation" for p in paras)),
    ("Appendix C heading",           any(p == "Appendix C: The Solidarity Pathway" for p in paras)),
    ("Figure placeholders clean",    any("Figure" in p and "here" in p and "**" not in p for p in paras)),
]
for label, result in checks:
    print("  %s  %s" % ("PASS" if result else "FAIL", label))
