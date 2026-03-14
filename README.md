# Research Master — Welfare State, Economic Vulnerability & Populism

**Researcher:** Ben Smart · PhD Political Economy / Comparative Politics
**Last updated:** March 2026

---

## What This Repository Is

A structured research hub for a dissertation examining how economic disruption — automation, trade exposure, austerity, occupational decline — shapes political behaviour, and what welfare state design can do about it.

The repository contains three things: a **theory knowledge base** (15 structured modules covering the relevant literature), a **data infrastructure** (replication datasets from 19 studies, cleaned and documented), and a **literature archive** (97 detailed paper notes, fully indexed).

---

## Repository Structure

```
Research_Master/
├── docs/
│   ├── theory/          15 theory modules + theory_index.json (with 97 lit. notes)
│   └── literature/      97 paper notes, renamed to readable slugs
│
├── metadata/
│   ├── data_dictionary.md        Full schema for all 104 datasets
│   ├── theory_data_bridge.md     Theory modules → datasets → variables
│   └── papers/                   Per-paper context files (16 studies)
│
├── data/
│   ├── raw/             Replication data, 19 study folders (~2.6 GB)
│   └── samples/         Test samples (top-100 and stratified by country)
│
├── scripts/             load_ess.py · load_ess.R · make_stratified_samples.py
├── analysis/            Your analysis scripts go here
└── outputs/             Figures and tables
```

---

## The Core Argument Space

The dissertation engages with a specific debate: why do "left-behind" workers support radical right parties rather than demanding more redistribution? The literature offers three competing answers:

**Material hardship** (modules 01–04): Trade exposure and automation create economic losers who demand compensation — but states have failed to deliver it effectively.

**Status anxiety** (modules 08–10): Economic position is zero-sum; relative decline threatens social standing in ways that welfare spending cannot address. Status-anxious voters want recognition, not redistribution.

**Cognitive mediation** (modules 12, 15): Structural causes (automation, trade) are misattributed to visible scapegoats (immigrants, elites). Identity switches from class to culture. Welfare design itself shapes these attributions through feedback effects.

Module 13 (Dual Pathway Synthesis) integrates these into a four-pathway model and identifies the trilemma: no traditional policy can simultaneously satisfy material needs, status concerns, and political legitimacy.

---

## Key Datasets

| Study | Folder | What it adds |
|-------|--------|-------------|
| Baccini (2024) | `data/raw/baccini_2024/` | Austerity → populism; analysis-ready individual + district files |
| Im et al. (2021) | `data/raw/im_2021/` | 402MB pooled ESS; automation risk + radical right vote |
| Milner (2021) | `data/raw/milner_2021/` | Trade + automation; regional merged data |
| Gugushvili (2025) | `data/raw/gugushvili_2025/` | Class mobility; ESS waves 1–5 |
| Cicollini (2025) | `data/raw/cicollini_2025/` | Positional income change (status) |
| Gingrich (2019) | `data/raw/gingrich_2019/` | ISSP ZA-series; ALMP responses to automation |
| Kurer (2020) | `data/raw/kurer_2020_declining_middle/` | Declining middle; ISCO crosswalk |
| ISCO task scores | `data/raw/shared_isco_task_scores/` | RTI scores — the key linking file |

---

## AI Usage Guide

This repository is optimised for AI-assisted research. Any AI agent (Claude or similar) should:

1. **Read `CLAUDE.md` first** — it contains the session primer and all standing instructions
2. **Use `metadata/theory_data_bridge.md`** to translate theory into datasets and variable names
3. **Check `metadata/data_dictionary.md`** before assuming any column name
4. **Load from `data/samples/`** for development; switch to `data/raw/` for production
5. **Consult `docs/theory/theory_index.json`** — it links theory modules to the 97 literature notes

The `theory_index.json` has a `literature` array listing all paper notes with:
- Clean slug and file path
- Inferred theory module links
- Section tags and key concepts
- Favourite flags

---

## Literature Coverage

97 paper notes covering: automation and voting, welfare state legitimacy, austerity and populism, status anxiety, moral economy, trade and globalisation, ALMPs, social investment, ontological security, affective polarization, misattribution and cognitive frames.

---

*AI-optimised research hub — built March 2026.*
