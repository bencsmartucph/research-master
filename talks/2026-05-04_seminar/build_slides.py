"""
Build PowerPoint slides for the 2026-05-04 seminar presentation.

Produces a .pptx version of the slides defined in slides.qmd, ready to
present from PowerPoint or LibreOffice Impress on Monday. Use the .qmd
source file for iteration; rebuild .pptx via this script.

Run:
    python talks/2026-05-04_seminar/build_slides.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

ROOT = Path(r'C:\Users\PKF715\Documents\claude_repos\Research_Master')
TALK_DIR = ROOT / 'talks' / '2026-05-04_seminar'
FIG_DIR = ROOT / 'outputs' / 'figures'

# Figure paths
FIG6 = FIG_DIR / 'fig6_cwed_country_slopes.png'
FIG7 = FIG_DIR / 'fig7_cwed_subcomponents.png'
FIG2 = FIG_DIR / 'fig2_rti_vs_antiimmig_by_regime.png'
FIG3 = FIG_DIR / 'fig3_marginal_effects.png'

# Colours — matches custom.scss
NAVY = RGBColor(0x0B, 0x3D, 0x91)   # primary
RED  = RGBColor(0xC9, 0x30, 0x2C)   # emphasis (rare)
GREY = RGBColor(0x6C, 0x75, 0x7D)   # secondary
DARK = RGBColor(0x1A, 0x1A, 0x1A)   # body text

# 16:9 widescreen
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

SW, SH = prs.slide_width, prs.slide_height


def add_blank_slide():
    blank_layout = prs.slide_layouts[6]
    return prs.slides.add_slide(blank_layout)


def add_text(slide, x, y, w, h, text, *, size=24, bold=False, italic=False,
             color=DARK, align=PP_ALIGN.LEFT, font='Calibri'):
    tx = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    return tx


def add_bullet_list(slide, x, y, w, h, items, *, size=20, color=DARK,
                    indent_levels=None, font='Calibri'):
    """items: list of strings or (level, text) tuples."""
    tx = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tx.text_frame
    tf.word_wrap = True
    for i, it in enumerate(items):
        if isinstance(it, tuple):
            level, text = it
        else:
            level, text = 0, it
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = level
        p.alignment = PP_ALIGN.LEFT
        p.space_before = Pt(6)
        p.space_after = Pt(6)
        run = p.add_run()
        run.text = ('•  ' if level == 0 else '–  ') + text
        run.font.size = Pt(size - 2 * level)
        run.font.color.rgb = color
        run.font.name = font
    return tx


def add_title_bar(slide, text):
    """Slide title with navy underline."""
    add_text(slide, 0.6, 0.35, 12, 0.7, text, size=30, bold=True, color=NAVY)
    # underline
    line = slide.shapes.add_shape(1, Inches(0.6), Inches(1.0), Inches(12.1), Inches(0.04))
    line.line.fill.background()
    line.fill.solid()
    line.fill.fore_color.rgb = NAVY


def add_image(slide, x, y, w, h, path):
    if Path(path).exists():
        slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    else:
        add_text(slide, x, y, w, 0.5, f"[FIGURE NOT FOUND: {path.name}]",
                 size=14, color=RED, italic=True)


def add_speaker_notes(slide, text):
    nf = slide.notes_slide.notes_text_frame
    nf.text = text


# =====================================================================
# Slide 1 — Title
# =====================================================================
s = add_blank_slide()
add_text(s, 0, 2.4, 13.333, 1.2,
         "Dignity Is a Baseline",
         size=54, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
add_text(s, 0, 3.7, 13.333, 0.7,
         "Welfare Institutions and the Asymmetric Politics of Economic Disruption",
         size=24, italic=True, color=DARK, align=PP_ALIGN.CENTER)
add_text(s, 0, 5.2, 13.333, 0.5,
         "Ben Smart",
         size=22, bold=True, color=DARK, align=PP_ALIGN.CENTER)
add_text(s, 0, 5.7, 13.333, 0.4,
         "University of Copenhagen — Department of Economics",
         size=16, color=GREY, align=PP_ALIGN.CENTER)
add_text(s, 0, 6.4, 13.333, 0.4,
         "Welfare State Seminar  ·  4 May 2026",
         size=14, italic=True, color=GREY, align=PP_ALIGN.CENTER)
add_speaker_notes(s, """[20 sec open]

Good afternoon. The paper is called "Dignity Is a Baseline." The thirty-second
version: workers exposed to automation are more anti-immigration than their
material interests would predict, the gap is bigger in some welfare states
than in others, and the conventional explanation — that more generous welfare
buffers the political backlash — is wrong about the mechanism in a specific
and testable way. The mechanism is asymmetric. I'll show you why.""")


# =====================================================================
# Slide 2 — The puzzle
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "The puzzle")
add_bullet_list(s, 0.7, 1.5, 12, 5, [
    "Workers in routine-task-intensive (RTI) occupations across Europe disproportionately support populist radical right parties (Gingrich 2019; Kurer 2020; Im et al. 2019; Autor et al. 2020)",
    "Cross-national variation: the same automation exposure converts into anti-immigration sentiment more readily in some welfare states than in others",
    "Standard reading: welfare generosity buffers the political backlash. Spend more, get less populism.",
    "Today's argument: this account is missing the mechanism it claims to describe",
], size=22)
add_speaker_notes(s, """[1.5 min]

Set up the empirical regularity, then the puzzle. RTI workers vote radical right
disproportionately — well documented. The cross-national variation is also
documented. The dominant interpretation is the buffering account: generous
welfare states see less populism because they cushion the dislocated.

I'm going to argue this account is wrong about the mechanism. Not wrong that
welfare matters — wrong about HOW welfare matters. And the consequences for
how we think about welfare-state design are real.""")


# =====================================================================
# Slide 3 — What buffering predicts
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "What the buffering account predicts")
# Quote box
qx = s.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(12), Inches(1.2))
qtf = qx.text_frame
qtf.word_wrap = True
qp = qtf.paragraphs[0]
qrun = qp.add_run()
qrun.text = "Following Ruggie's (1982) embedded liberalism bargain, generous compensation should dampen the political insecurity produced by economic openness."
qrun.font.size = Pt(20)
qrun.font.italic = True
qrun.font.color.rgb = GREY
qrun.font.name = 'Calibri'
# Navy left border via shape
border = s.shapes.add_shape(1, Inches(0.55), Inches(1.5), Inches(0.05), Inches(1.2))
border.line.fill.background()
border.fill.solid()
border.fill.fore_color.rgb = NAVY

add_text(s, 0.7, 3.3, 12, 0.6, "Operative variable: quantity",
         size=26, bold=True, color=NAVY)
add_bullet_list(s, 0.7, 4.0, 12, 3, [
    "More spending → less populism",
    "Symmetric: damage and repair are mirror images of each other",
    "Compensation works by replacing income lost to disruption",
], size=20)
add_speaker_notes(s, """[1 min]

The buffering reading rests on Ruggie's embedded liberalism. Compensation is a
quantity. The mechanism is symmetric — what damages is undone by what compensates.
The variable is how much the welfare state spends.

The quantity assumption is what I want to challenge. Spend more, get less
populism — this turns out to fit the data poorly.""")


# =====================================================================
# Slide 4 — Three streams of evidence
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "Three streams of evidence against buffering")

col_w = 4.0
col_y = 1.4
col_h = 5.5

# Column 1 — does not work
add_text(s, 0.6, col_y, col_w, 0.5, "Compensation that doesn't work",
         size=18, bold=True, color=NAVY)
add_text(s, 0.6, col_y + 0.7, col_w, col_h - 0.7,
         "Gingrich (2019) finds workers exposed to automation are NOT less likely to vote populist in countries with more generous early retirement, more in-kind spending, or more protective regulation.\n\nGallego & Kurer (2022) call this 'a concerning finding'.",
         size=15, color=DARK)

# Column 2 — backfires
add_text(s, 4.7, col_y, col_w, 0.5, "Compensation that backfires",
         size=18, bold=True, color=NAVY)
add_text(s, 4.7, col_y + 0.7, col_w, col_h - 0.7,
         "Stutzmann (2025) examines Germany's coal phase-out. Substantial compensatory investment. Material conditions held.\n\nAffected municipalities showed higher abstention and lower support for the issue-owning party.",
         size=15, color=DARK)

# Column 3 — resisted
add_text(s, 8.8, col_y, col_w, 0.5, "Compensation that is resisted",
         size=18, bold=True, color=NAVY)
add_text(s, 8.8, col_y + 0.7, col_w, col_h - 0.7,
         "Pelc (2025): workers refuse to be compensated out of work even when the compensation fully replaces their income.\n\nForm, source, and meaning of compensation matter independently of material content.",
         size=15, color=DARK)

add_speaker_notes(s, """[2 min — speak to each column for ~30 sec]

Three different research designs, three different findings, all pointing the
same direction. Gingrich's cross-national analysis: more generous welfare
states do not show weaker automation-to-populism effects. Stutzmann on the
German coal phase-out: a textbook case of policy compensation that backfired
politically. Pelc's experimental work: workers reject compensation that
should, materially, satisfy them.

The pattern across these is that material compensation is doing less of the
political work than the buffering model assumes.""")


# =====================================================================
# Slide 5 — Kurer quote
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "Kurer (2020) names the tension")

# Big quote
q1 = s.shapes.add_textbox(Inches(0.7), Inches(1.4), Inches(12), Inches(1.6))
q1tf = q1.text_frame
q1tf.word_wrap = True
q1p = q1tf.paragraphs[0]
q1r = q1p.add_run()
q1r.text = '"When relative societal decline rather than material hardship are at the heart of socially conservative resentment, traditional welfare policy may be an insufficient response to satisfy exposed workers and hence an ineffective remedy to counter the ascent of right-wing populist movements."'
q1r.font.size = Pt(18)
q1r.font.italic = True
q1r.font.color.rgb = DARK
q1r.font.name = 'Calibri'
b1 = s.shapes.add_shape(1, Inches(0.55), Inches(1.4), Inches(0.05), Inches(1.6))
b1.line.fill.background(); b1.fill.solid(); b1.fill.fore_color.rgb = NAVY

add_text(s, 0.7, 3.2, 8, 0.4, "Kurer & Palier (2019):",
         size=14, bold=True, color=NAVY)
q2 = s.shapes.add_textbox(Inches(0.7), Inches(3.65), Inches(12), Inches(1.0))
q2tf = q2.text_frame; q2tf.word_wrap = True
q2p = q2tf.paragraphs[0]
q2r = q2p.add_run()
q2r.text = '"This appeal to personal dignity is key to winning routine workers\' support. Perhaps even more than social protection, they demand economic AND cultural protection."'
q2r.font.size = Pt(15); q2r.font.italic = True
q2r.font.color.rgb = DARK; q2r.font.name = 'Calibri'

add_text(s, 0.7, 5.0, 8, 0.4, "Gidron & Hall (2017, p. 26):",
         size=14, bold=True, color=NAVY)
q3 = s.shapes.add_textbox(Inches(0.7), Inches(5.45), Inches(12), Inches(1.0))
q3tf = q3.text_frame; q3tf.word_wrap = True
q3p = q3tf.paragraphs[0]
q3r = q3p.add_run()
q3r.text = 'Right-populist voters "care as much, or even more, about recognition as about redistribution."'
q3r.font.size = Pt(15); q3r.font.italic = True
q3r.font.color.rgb = DARK; q3r.font.name = 'Calibri'

add_speaker_notes(s, """[1 min]

Three quotes from major contributions in the literature, all pointing at the
same thing: redistribution and recognition aren't fungible. The buffering
framework treats them as if they were. They aren't, and the empirical record
keeps showing this.

This is where my argument enters. I take Kurer's claim literally — that
traditional welfare may be an insufficient response — and ask which
institutional dimension actually does the political work.""")


# =====================================================================
# Slide 6 — The argument in one slide (CENTRAL)
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "The argument")

add_text(s, 0.7, 1.4, 12, 0.6,
         "Welfare institutions are asymmetric in their political effects",
         size=26, bold=True, color=NAVY)

add_text(s, 0.7, 2.4, 12, 0.5,
         "They can fail politically — by damaging the self-concept of vulnerable workers — through a cascade:",
         size=18, color=DARK)

# Three-step cascade boxes
box_w = 3.8
box_h = 1.0
box_y = 3.2
for i, (title, text) in enumerate([
    ("1. Identity switching", "Bonomi, Gennaioli & Tabellini (2021)"),
    ("2. Misattribution",     "Gallego & Kurer (2022)"),
    ("3. Defensive othering", "Wagner (2022); Patrick (2016)"),
]):
    x = 0.7 + i * (box_w + 0.2)
    box = s.shapes.add_shape(5, Inches(x), Inches(box_y), Inches(box_w), Inches(box_h))
    box.fill.solid(); box.fill.fore_color.rgb = RGBColor(0xF6, 0xF8, 0xFA)
    box.line.color.rgb = NAVY
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = Inches(0.15); tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.12); tf.margin_bottom = Inches(0.12)
    p1 = tf.paragraphs[0]
    r1 = p1.add_run(); r1.text = title
    r1.font.size = Pt(18); r1.font.bold = True; r1.font.color.rgb = NAVY; r1.font.name = 'Calibri'
    p2 = tf.add_paragraph()
    r2 = p2.add_run(); r2.text = text
    r2.font.size = Pt(13); r2.font.italic = True; r2.font.color.rgb = GREY; r2.font.name = 'Calibri'

add_text(s, 0.7, 4.7, 12, 0.5,
         "They cannot, by symmetric operation, succeed.",
         size=20, italic=True, color=DARK)

# Highlighted thesis
thesis_box = s.shapes.add_shape(5, Inches(0.7), Inches(5.5), Inches(11.9), Inches(1.5))
thesis_box.fill.solid(); thesis_box.fill.fore_color.rgb = NAVY
thesis_box.line.fill.background()
ttf = thesis_box.text_frame; ttf.word_wrap = True
ttf.margin_left = Inches(0.4); ttf.margin_right = Inches(0.4)
ttf.margin_top = Inches(0.25); ttf.margin_bottom = Inches(0.25)
tp = ttf.paragraphs[0]
tp.alignment = PP_ALIGN.CENTER
tr = tp.add_run()
tr.text = "Dignity is a baseline good."
tr.font.size = Pt(24); tr.font.bold = True
tr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); tr.font.name = 'Calibri'
tp2 = ttf.add_paragraph(); tp2.alignment = PP_ALIGN.CENTER
tr2 = tp2.add_run()
tr2.text = "Its absence damages. Its presence clears the ground for solidarity without producing it."
tr2.font.size = Pt(16); tr2.font.italic = True
tr2.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); tr2.font.name = 'Calibri'

add_speaker_notes(s, """[2 min — this is the central conceptual slide]

This is the argument. Welfare institutions can fail politically through a
specific cascade — identity switching, misattribution, defensive othering. I'll
walk through each in a moment.

The key claim is asymmetric. The mechanism that damages is real and observable.
The mirror-image protective mechanism — where dignity-preserving welfare
produces solidarity — is not. In my data and in others'.

That last sentence is the paper's title in compressed form. Dignity is a
baseline good. Its absence damages. Its presence clears ground for solidarity
that other things have to build.""")


# =====================================================================
# Slide 7 — Why welfare and not something else
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "Why welfare, and not something else")
add_bullet_list(s, 0.7, 1.4, 12, 1.2, [
    "Many institutions shape identity: media environments, religious traditions, class structures",
    "Why isolate welfare?",
], size=20)

add_text(s, 0.7, 3.0, 12, 0.6,
         "Welfare is the single state domain where economic vulnerability and institutional treatment meet at the same moment",
         size=22, bold=True, color=NAVY)

add_text(s, 0.7, 4.0, 12, 0.7,
         "When a worker encounters the welfare state, the institution allocates resources AND renders judgement about their claim to those resources, in the same act.",
         size=17, color=DARK, italic=True)

add_bullet_list(s, 0.7, 5.0, 12, 1.5, [
    "Courts judge but rarely allocate",
    "Markets allocate without judgement",
    "Religious institutions judge but cannot compel",
], size=16, color=GREY)

add_text(s, 0.7, 6.4, 12, 0.6,
         "Only welfare does both. At the point of maximum material dependence.",
         size=20, bold=True, color=NAVY)

add_speaker_notes(s, """[1 min]

The objection one would make at this stage is that lots of institutions shape
identity. Why is welfare special?

Welfare is the one state domain where economic vulnerability meets institutional
treatment in the same act. A worker encountering the welfare state is being
allocated resources AND being judged about their claim to them, simultaneously.
That joint operation is unusual.

This is what makes welfare uniquely load-bearing as a communicator of citizen
worth. It's what Wagner's recipients are hearing when they "internalize
deservingness criteria." It's what makes dignity an institutional outcome, not
just a personal one.""")


# =====================================================================
# Slide 8 — The damage cascade (detail)
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "The damage cascade")

# Three columns
col_w = 4.0
col_y = 1.5
for i, (num, title, body) in enumerate([
    ("1.", "Identity switches",
     "Bonomi et al. (2021): individuals move from class to cultural identity when class identity is degraded.\n\nStigmatising welfare implementation degrades class identity DIRECTLY — accelerating the switch."),
    ("2.", "Grievances misattribute",
     "Once cultural identity is in charge, frustration finds available scapegoats.\n\nWu (2022): workers at higher automation risk oppose immigration but show no different technology preferences.\n\nMisdirection has no protective analogue."),
    ("3.", "Othering turns defensive",
     "Patrick (2016): UK benefit claimants shore up their own deservingness through critique of those below them — using the welfare system's own criteria.\n\nWagner (2022): 'kicking down'."),
]):
    x = 0.6 + i * (col_w + 0.2)
    add_text(s, x, col_y, col_w, 0.5, num + " " + title,
             size=18, bold=True, color=NAVY)
    add_text(s, x, col_y + 0.6, col_w, 4, body,
             size=13, color=DARK)

# Endpoint box
end_y = 6.3
end = s.shapes.add_shape(5, Inches(0.7), Inches(end_y), Inches(11.9), Inches(0.85))
end.fill.solid(); end.fill.fore_color.rgb = RGBColor(0xF6, 0xF8, 0xFA)
end.line.color.rgb = NAVY
etf = end.text_frame; etf.word_wrap = True
etf.margin_left = Inches(0.3); etf.margin_top = Inches(0.12)
ep = etf.paragraphs[0]
er = ep.add_run()
er.text = "Endpoint (Busemeyer, Rathgeb & Sahm 2023): "
er.font.size = Pt(15); er.font.bold = True; er.font.color.rgb = NAVY; er.font.name = 'Calibri'
er2 = ep.add_run()
er2.text = "the particularistic-authoritarian welfare preference — pro-workfare, anti-poor, anti-social-investment."
er2.font.size = Pt(15); er2.font.color.rgb = DARK; er2.font.name = 'Calibri'

add_speaker_notes(s, """[2 min]

Three steps in sequence. Identity switches first — class to cultural. Then
grievances misattribute — frustration that should target the actual cause of
vulnerability gets pointed at immigrants. Then othering turns defensive — the
worker shores up their own deservingness on critique of those below them.

The cascade ends in what Busemeyer and colleagues call the
"particularistic-authoritarian" preference. Pro-workfare, anti-poor,
anti-social-investment.

What's important about this slide: each step has a documented empirical
literature, but no one has connected the chain. Connecting them — with welfare
design as the upstream condition — is one of the paper's contributions.""")


# =====================================================================
# Slide 9 — Why no mirror image
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "Why no mirror image")

add_text(s, 0.7, 1.4, 12, 0.6,
         "Three asymmetries, none with a symmetric counterpart",
         size=22, bold=True, color=NAVY)

# Three asymmetry blocks
blocks = [
    ("Loss aversion (Kahneman & Tversky 1979)",
     "Stigmatising encounters register as losses; dignity-preserving ones don't register as gains of equivalent magnitude. Damage mobilises; the absence of damage tends not to."),
    ("Status is positional",
     "Recognition cannot be redistributed without losses to the currently-recognised (Gidron & Hall 2017). Dignity-preserving welfare REMOVES an obstacle to inclusive solidarity. It does not, by itself, CONSTRUCT inclusion."),
    ("Defensive othering is costly to reverse",
     "Identity investments are not undone by changing the institutional environment alone. Pierson's (1994) positive feedback runs forward into supportive constituencies; the damage cascade runs forward into a population that has forgotten the position it now defends was constructed for it."),
]
for i, (title, body) in enumerate(blocks):
    y = 2.2 + i * 1.55
    # Number circle
    add_text(s, 0.6, y, 0.5, 0.5, str(i+1) + ".",
             size=22, bold=True, color=NAVY)
    add_text(s, 1.1, y, 11.5, 0.5, title,
             size=18, bold=True, color=NAVY)
    add_text(s, 1.1, y + 0.5, 11.5, 1.0, body,
             size=14, color=DARK)

add_speaker_notes(s, """[2 min]

Three reasons the mechanism is one-way, not symmetric.

First, loss aversion. Damage is psychologically heavier than equivalent
non-damage. This applies to dignity shocks just as it applies to material ones.

Second, status is positional. Recognition can't be redistributed the way money
can — relational goods don't add to a fixed pool. Dignity-preserving welfare
clears space for inclusive solidarity but doesn't itself produce the inclusion.

Third — and the one I find theoretically most interesting — defensive othering,
once committed to, is costly to reverse. The cascade isn't just additive. It's
identity-investing. Pierson's classic positive-feedback story is forward into
support; the damage cascade is forward into opposition that gets harder to
reverse with each iteration.

The implication: even if you fix the institutions, the cascade has already
made commitments that institutions alone cannot undo.""")


# =====================================================================
# Slide 10 — Empirical setup
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "Empirical setup")

# Two columns
add_text(s, 0.7, 1.4, 6, 0.5, "Data", size=20, bold=True, color=NAVY)
add_bullet_list(s, 0.7, 2.0, 6, 3, [
    "European Social Survey rounds 6–9 (2012–2018)",
    "34 countries, N = 188,764",
    "15 Western European countries (CWED welfare-quality analysis)",
], size=15)

add_text(s, 0.7, 4.5, 6, 0.5, "Key variables", size=20, bold=True, color=NAVY)
add_bullet_list(s, 0.7, 5.0, 6, 2.5, [
    "RTI: routine task intensity (Goos, Manning & Salomons 2014)",
    "Anti-immigration: 3-item index (α = 0.864)",
    "Welfare context: regimes; ALMP spending; CWED decommodification",
], size=15)

add_text(s, 7.0, 1.4, 6, 0.5, "Approach", size=20, bold=True, color=NAVY)
add_bullet_list(s, 7.0, 2.0, 6, 5, [
    "Cross-level interactions: RTI × Welfare → attitudes",
    "Country-wave fixed effects, cluster-robust SEs",
    "Random-slope mixed models for cross-national heterogeneity",
    "15-country matched sample for ALMP/CWED comparison",
    "Cross-sectional design — claim is consistency, not causation",
], size=15)

add_speaker_notes(s, """[1 min]

Quick description of the data. ESS waves 6 to 9, 34 countries. The headline
analysis is a cross-level interaction — RTI predicting anti-immigration
attitudes, with the slope conditional on welfare context. I run regimes,
spending, and decommodification as alternative welfare measures.

Cross-sectional design — I'm honest about that in the paper. I can show the
pattern is consistent with the asymmetric mechanism; I can't establish
causation here. The thesis follow-up does that with Danish registry data.""")


# =====================================================================
# Slide 11 — ALMP vs CWED (HEADLINE)
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "ALMP vs CWED — the headline")

add_image(s, 2.0, 1.3, 9.3, 4.5, FIG6)

# Findings strip
add_text(s, 0.7, 6.0, 12, 0.4, "Same 15 countries, two welfare measures:",
         size=16, bold=True, color=DARK)
add_bullet_list(s, 0.7, 6.5, 12.5, 1, [
    "ALMP spending:  r = +0.01 (n.s.)  →  spending effort doesn't predict the slope",
    "CWED decommodification:  r = −0.85 (p<0.001)  →  72 per cent of cross-national variation",
], size=15)

add_speaker_notes(s, """[2 min — the empirical highlight]

This is the paper's most important empirical contrast. Same fifteen Western
European countries, two ways of measuring welfare. Active labour market policy
spending — what most of the buffering literature uses as its measure of
welfare effort. CWED decommodification — the degree to which the welfare
state lets you sustain yourself without market employment.

ALMP spending: essentially zero correlation with how strongly automation
exposure converts into exclusion. Spending more on labour market policies has
nothing to do with the cross-national pattern.

CWED decommodification: r equals negative point eight five. Seventy-two percent
of the cross-national variation. The line you're looking at is what the
asymmetric mechanism predicts and what the buffering account cannot explain.

What's the difference? ALMP captures effort. You can spend a lot on punitive
workfare. CWED captures decommodification — what the welfare state lets you
have, not what it costs to provide. The dignity dimension travels along the
second variable.""")


# =====================================================================
# Slide 12 — Sub-components decomposition (NEW)
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "Decomposition: which decommodification dimension matters?")

add_image(s, 0.5, 1.3, 7.5, 3.5, FIG7)

# Right panel — table
add_text(s, 8.3, 1.3, 4.5, 0.5, "Individual-level interactions",
         size=15, bold=True, color=NAVY)

# Mini table
table_data = [
    ("Component",     "β",       "p"),
    ("Unemployment",  "−0.053",  "<0.001 ★"),
    ("Sickness",      "−0.037",  "0.003"),
    ("Pensions",      "−0.019",  "0.066"),
    ("Composite",     "−0.051",  "<0.001"),
]
ty = 1.85
for r, row in enumerate(table_data):
    is_header = r == 0
    is_highlight = (r == 1)  # unemployment
    fcolor = NAVY if (is_header or is_highlight) else DARK
    fbold = is_header or is_highlight
    add_text(s, 8.3, ty, 1.7, 0.35, row[0], size=13, bold=fbold, color=fcolor)
    add_text(s, 10.0, ty, 1.0, 0.35, row[1], size=13, bold=fbold, color=fcolor)
    add_text(s, 11.0, ty, 1.7, 0.35, row[2], size=13, bold=fbold, color=fcolor)
    ty += 0.4

# Predicted ordering
add_text(s, 0.7, 5.2, 12, 0.45, "Predicted ordering: UE > SK > PEN.",
         size=15, italic=True, color=GREY)
add_text(s, 0.7, 5.65, 12, 0.45, "Observed at individual level: UE > SK > PEN.  ✓",
         size=16, bold=True, color=NAVY)

add_text(s, 0.7, 6.4, 12, 0.4,
         "The damage cascade fires through the point of economic vulnerability.",
         size=16, italic=True, color=DARK)

add_speaker_notes(s, """[1.5 min — the new finding]

This is the new analysis I ran this week. The composite CWED hides three
sub-components: unemployment generosity, sickness generosity, pension
generosity. Theory predicts unemployment should drive the result — that's where
automation-exposed workers actually meet the welfare state.

Individual-level interaction: unemployment generosity, beta minus zero point
zero five three, p less than point zero zero one. Sickness intermediate.
Pensions weakest, marginally significant only.

Theory holds at the test that matters: the institutional channel runs through
the point of economic vulnerability, not through welfare expenditure in the
abstract.

For thesis design, this matters: the within-Denmark test should focus on
unemployment benefit reforms — the 2003, 2006, and 2013 activation reforms.
Pension reforms should NOT show damage signatures of the same magnitude.""")


# =====================================================================
# Slide 13 — Asymmetric confirmation
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "The asymmetric confirmation")

add_text(s, 0.7, 1.4, 12, 0.5, "Same data, opposite outcome",
         size=22, bold=True, color=NAVY)

# Comparison table
ty = 2.2
headers = ("Outcome", "RTI × Liberal interaction", "p")
add_text(s, 0.7, ty, 4.5, 0.4, headers[0], size=16, bold=True, color=GREY)
add_text(s, 5.5, ty, 4.5, 0.4, headers[1], size=16, bold=True, color=GREY)
add_text(s, 10.5, ty, 2, 0.4, headers[2], size=16, bold=True, color=GREY)

# Underline
ul = s.shapes.add_shape(1, Inches(0.7), Inches(2.65), Inches(12), Inches(0.03))
ul.line.fill.background(); ul.fill.solid(); ul.fill.fore_color.rgb = NAVY

add_text(s, 0.7, 2.8, 4.5, 0.5, "Anti-immigration", size=18, bold=True, color=NAVY)
add_text(s, 5.5, 2.8, 4.5, 0.5, "β = +0.127", size=18, bold=True, color=NAVY)
add_text(s, 10.5, 2.8, 2, 0.5, "0.003 ✓", size=18, bold=True, color=NAVY)

add_text(s, 0.7, 3.5, 4.5, 0.5, "Redistribution support", size=18, color=DARK)
add_text(s, 5.5, 3.5, 4.5, 0.5, "β = +0.011", size=18, color=DARK)
add_text(s, 10.5, 3.5, 2, 0.5, "0.285 (n.s.)", size=18, color=GREY)

# Underline
ul2 = s.shapes.add_shape(1, Inches(0.7), Inches(4.05), Inches(12), Inches(0.03))
ul2.line.fill.background(); ul2.fill.solid(); ul2.fill.fore_color.rgb = NAVY

add_text(s, 0.7, 4.4, 12, 0.5,
         "The exclusion side is robust. The solidarity side is null.",
         size=22, bold=True, color=NAVY)

add_bullet_list(s, 0.7, 5.1, 12, 2, [
    "Welfare context cleanly attenuates the conversion of vulnerability into exclusion",
    "Welfare context does NOT detectably moderate the conversion of the same vulnerability into solidarity",
    "Supplementary ISSP test on different sample, outcome, time period: same null",
], size=15)

add_text(s, 0.7, 6.6, 12, 0.45,
         "This is what the asymmetric mechanism predicts.",
         size=18, italic=True, bold=True, color=NAVY)

add_speaker_notes(s, """[1 min]

The same data tested two ways. RTI predicts anti-immigration attitudes more
strongly in Liberal regimes than Nordic ones — the interaction is significant
across every specification. RTI predicts slightly higher redistribution support
across all regimes — but the cross-regime variation in that pathway is small,
non-significant, and in the wrong direction.

Welfare context attenuates conversion into exclusion. It does not detectably
moderate conversion into solidarity.

Two ways to read the null. As a measurement limitation — single-item scales,
panel limitations. Or as a substantive confirmation — the mechanism IS
asymmetric. The supplementary ISSP analysis on different data with a different
outcome returns the same null. I take the substantive reading. It's what the
theory predicts.""")


# =====================================================================
# Slide 14 — Implications
# =====================================================================
s = add_blank_slide()
add_title_bar(s, "Implications")

implications = [
    ("Welfare-state theory",
     "the political consequences of welfare design travel along WHAT welfare communicates, not HOW MUCH welfare spends"),
    ("Cultural-vs-economic debate",
     "cultural backlash isn't a rival explanation to economic disruption — it's what economic disruption looks like, cross-nationally, where welfare institutions are less decommodifying"),
    ("Policy",
     "dignity-preserving welfare is necessary for solidarity but not sufficient. Active solidarity requires political work that welfare design alone cannot do"),
    ("Thesis follow-up",
     "Danish registry data on individuals before and after the 2003/2006/2013 activation reforms — testing within-individual whether conditionality shocks produce damage signatures"),
]

for i, (title, text) in enumerate(implications):
    y = 1.5 + i * 1.3
    add_text(s, 0.7, y, 3.5, 0.5, "For " + title + ":",
             size=16, bold=True, color=NAVY)
    add_text(s, 4.4, y, 8.5, 1.2, text,
             size=15, color=DARK)

add_speaker_notes(s, """[1 min]

Four implications.

First, welfare-state theory: the dimension along which welfare's political
effects travel is what it communicates, not how much it spends. Decommodification
is a measure of the former. Spending is a measure of the latter.

Second, the cultural-vs-economic debate. People keep arguing about whether
populism is fundamentally about culture or about economics. My answer is: this
distinction is misleading. Cultural backlash is what economic disruption looks
like cross-nationally, when welfare institutions don't preserve recognition.

Third, policy. Dignity-preserving welfare is a baseline good. It's necessary
for solidarity but doesn't itself construct it.

Fourth, where this goes next. Danish registry data lets me test the
within-individual claim — that conditionality reforms produce damage signatures
in panel attitudes. That's the thesis.""")


# =====================================================================
# Slide 15 — Closing
# =====================================================================
s = add_blank_slide()

add_text(s, 0, 1.8, 13.333, 1.0,
         "Dignity is a baseline",
         size=56, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

add_text(s, 0, 3.4, 13.333, 0.6,
         "Its absence damages.",
         size=26, italic=True, color=DARK, align=PP_ALIGN.CENTER)
add_text(s, 0, 4.0, 13.333, 0.6,
         "Its presence clears the ground for solidarity.",
         size=26, italic=True, color=DARK, align=PP_ALIGN.CENTER)
add_text(s, 0, 4.6, 13.333, 0.6,
         "It does not, by itself, produce solidarity.",
         size=26, italic=True, color=DARK, align=PP_ALIGN.CENTER)

add_text(s, 0, 6.0, 13.333, 0.6,
         "Thank you.",
         size=32, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
add_text(s, 0, 6.7, 13.333, 0.4,
         "ben.smart@econ.ku.dk",
         size=14, color=GREY, align=PP_ALIGN.CENTER)

add_speaker_notes(s, """[Closing — 30 seconds]

The line that holds the paper together. Dignity is a baseline good. Its absence
damages. Its presence clears ground for solidarity that has to be built on top,
by other means.

The asymmetric mechanism is the technical version. The line is the moral version.
Both are saying the same thing.

Thank you. Happy to take questions.""")


# =====================================================================
# Backup slides (16-19) — for Q&A
# =====================================================================

# Backup 1: Regime descriptive
s = add_blank_slide()
add_title_bar(s, "Backup: regime descriptive results")
add_image(s, 1.5, 1.3, 7, 4.5, FIG2)

# Right panel — table
add_text(s, 9, 2.0, 4, 0.4, "Regime", size=14, bold=True, color=NAVY)
add_text(s, 11.5, 2.0, 1.5, 0.4, "Slope", size=14, bold=True, color=NAVY)
ty = 2.5
for regime, slope in [
    ("Liberal", "β = 0.512"),
    ("Southern", "β = 0.462"),
    ("Continental", "β = 0.443"),
    ("Nordic", "β = 0.413"),
    ("Eastern", "β = 0.263"),
]:
    add_text(s, 9, ty, 4, 0.4, regime, size=13, color=DARK)
    add_text(s, 11.5, ty, 1.5, 0.4, slope, size=13, color=DARK)
    ty += 0.4

# Backup 2: Marginal effects
s = add_blank_slide()
add_title_bar(s, "Backup: marginal effects")
add_image(s, 2.5, 1.3, 8.5, 4.5, FIG3)
add_text(s, 0.7, 6.0, 12, 0.5,
         "A 1-SD increase in RTI is associated with:",
         size=16, bold=True, color=DARK)
add_bullet_list(s, 0.7, 6.5, 12, 1.5, [
    "0.32 additional scale points of anti-immigration sentiment in Liberal regimes",
    "0.20 in Nordic regimes — gap is significant and substantively meaningful",
], size=14)

# Backup 3: Burgoon & Schakel
s = add_blank_slide()
add_title_bar(s, "Backup: Burgoon & Schakel (2022)")
add_text(s, 0.7, 1.3, 12, 0.6, "They find:", size=18, bold=True, color=NAVY)
add_text(s, 0.7, 1.9, 12, 0.6,
         "welfare generosity dampens anti-globalisation nationalism in European party platforms.",
         size=16, color=DARK)
add_text(s, 0.7, 2.9, 12, 0.6,
         "Apparent contradiction with my null on ALMP — resolved by unit of analysis:",
         size=16, italic=True, color=DARK)
add_bullet_list(s, 0.7, 3.6, 12, 2, [
    "B&S measure platform language at the PARTY level",
    "I measure attitudinal slopes at the INDIVIDUAL level conditional on RTI exposure",
    "Mechanisms differ: elite incentives + coalition arithmetic vs. institutional encounter + self-concept",
], size=15)
add_text(s, 0.7, 5.6, 12, 0.5,
         "Both can be true.",
         size=18, bold=True, color=NAVY)
add_text(s, 0.7, 6.1, 12, 1,
         "Welfare generosity at scale may dampen the SUPPLY of anti-globalisation rhetoric in party systems while the DEMAND for exclusionary attitudes among vulnerable workers responds to a different welfare dimension entirely.",
         size=14, color=DARK)

# Backup 4: Denmark
s = add_blank_slide()
add_title_bar(s, "Backup: Denmark complication")
add_text(s, 0.7, 1.3, 12, 0.7,
         "Despite high CWED generosity, Denmark shows steeper RTI → exclusion slope (β=0.50) than Finland, Sweden, or Norway.",
         size=15, color=DARK)
add_text(s, 0.7, 2.4, 12, 0.6,
         "Reading: not an anomaly. Confirmation.",
         size=20, bold=True, color=NAVY)
add_text(s, 0.7, 3.1, 12, 0.7,
         "Danish 'flexicurity' combines generous benefits with high labour market flexibility and active job search requirements — generous in transfers but demanding in activation.",
         size=14, italic=True, color=DARK)
add_text(s, 0.7, 4.2, 12, 0.5, "The asymmetric mechanism predicts:",
         size=16, bold=True, color=NAVY)
add_bullet_list(s, 0.7, 4.7, 12, 2, [
    "Conditionality and surveillance damage the self-concept EVEN WHEN transfer levels are high",
    "Conditionality is what communicates suspicion, not (only) thinness of provision",
], size=14)
add_text(s, 0.7, 6.5, 12, 0.4,
         "Robustness: country-level finding survives all single-country exclusions. r=−0.717 even with both highest-leverage observations dropped (p=0.006).",
         size=12, italic=True, color=GREY)


# =====================================================================
# Save
# =====================================================================
out = TALK_DIR / 'Dignity_Is_a_Baseline_2026-05-04.pptx'
prs.save(str(out))
print(f"Saved: {out}")
print(f"Total slides: {len(prs.slides)}")
print(f"Including: title, 13 main slides, closing, 4 backup")
