"""
Export recall prompts and Try-this exercises across all learning chapters
into an Anki-importable TSV file.

Three card types are produced:
  1. Recall (end-of-chapter) — Q/A from "**N.** ... <details>...</details>" patterns
  2. Try-this (inline) — Q/A from "> **Try this.** ... <details>...</details>" patterns
  3. Defence rehearsal — the killer-line answers to "Defend the choice" prompts

Usage:
    python scripts/export_recall_to_anki.py                 # → outputs/anki/learning_econometrics.tsv
    python scripts/export_recall_to_anki.py --output X.tsv  # custom path
    python scripts/export_recall_to_anki.py --include-walkthrough  # also include the empirical_walkthrough_v1.md defences

Anki import: in Anki, File > Import, choose Tab as separator, set the field
mapping to Front / Back / Tags. Allow HTML in fields (the answers contain
<details> markup which renders as plain text in Anki — fine for our purposes).
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
LEARNING_DIR = ROOT / "docs" / "learning_econometrics"
WALKTHROUGH_PATH = ROOT / "docs" / "empirical_walkthrough_v1.md"
DEFAULT_OUT = ROOT / "outputs" / "anki" / "learning_econometrics.tsv"


# ── Frontmatter splitting (lightweight, no yaml dep needed for this script) ─

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
TITLE_RE = re.compile(r"^title:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)
CHAPTER_ID_RE = re.compile(r"^chapter_id:\s*[\"']?(\d+)[\"']?\s*$", re.MULTILINE)


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_text, body)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return "", text
    return match.group(1), text[match.end():]


def get_chapter_meta(text: str) -> tuple[str, str]:
    """Extract (chapter_id, title) from frontmatter."""
    fm, _ = split_frontmatter(text)
    cid_match = CHAPTER_ID_RE.search(fm)
    title_match = TITLE_RE.search(fm)
    cid = cid_match.group(1) if cid_match else "??"
    title = title_match.group(1) if title_match else "Untitled"
    return cid, title


# ── Content cleaning ─────────────────────────────────────────────────────────

def clean_for_anki(text: str) -> str:
    """Strip markdown formatting that doesn't render in Anki's plain card view."""
    # Remove leading > quote markers
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    # Collapse whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    # Anki uses HTML; preserve newlines as <br>
    text = text.replace("\n\n", "<br><br>").replace("\n", " ")
    return text


# ── Card extraction ──────────────────────────────────────────────────────────

def extract_recall_cards(body: str, chapter_id: str, title: str) -> list[dict]:
    """End-of-chapter recall pairs."""
    cards = []
    pattern = re.compile(
        r"\*\*(\d+)\.\*\*\s*(.+?)\s*\n\s*<details>\s*<summary>[^<]*</summary>\s*\n(.*?)</details>",
        re.DOTALL,
    )
    for match in pattern.finditer(body):
        num = match.group(1)
        question = clean_for_anki(match.group(2))
        answer = clean_for_anki(match.group(3))
        cards.append({
            "front": f"[Ch {chapter_id} • Recall {num}] {question}",
            "back": answer,
            "tags": f"chapter::{chapter_id} type::recall {_slugify(title)}",
        })
    return cards


def extract_try_this_cards(body: str, chapter_id: str, title: str) -> list[dict]:
    """Inline 'Try this' exercises."""
    cards = []
    pattern = re.compile(
        r">\s*\*\*Try this\.?\*\*\s*(.+?)\s*\n\s*<details>\s*<summary>[^<]*</summary>\s*\n(.*?)</details>",
        re.DOTALL,
    )
    for i, match in enumerate(pattern.finditer(body), 1):
        prompt = clean_for_anki(match.group(1))
        answer = clean_for_anki(match.group(2))
        cards.append({
            "front": f"[Ch {chapter_id} • Try-this {i}] {prompt}",
            "back": answer,
            "tags": f"chapter::{chapter_id} type::try_this {_slugify(title)}",
        })
    return cards


def extract_defence_cards(body: str, chapter_id: str, title: str) -> list[dict]:
    """Defend-the-choice rehearsals — these become cloze-style fluency cards."""
    cards = []
    pattern = re.compile(
        r"\*\*Defend the choice\.?\*\*\s+(.+?)\s*\n\s*<details>\s*<summary>[^<]*</summary>\s*\n(.*?)</details>",
        re.DOTALL,
    )
    for i, match in enumerate(pattern.finditer(body), 1):
        scenario = clean_for_anki(match.group(1))
        defence = clean_for_anki(match.group(2))
        cards.append({
            "front": f"[Ch {chapter_id} • Defence {i}] {scenario}",
            "back": defence,
            "tags": f"chapter::{chapter_id} type::defence {_slugify(title)}",
        })
    return cards


def extract_walkthrough_defences(text: str) -> list[dict]:
    """Pull all 'Defending the choice in 30 seconds' callouts from the walkthrough doc."""
    cards = []
    # Concept headings look like "## §V.B — Concept N: Title" or similar
    concept_blocks = re.split(r"(?=^##\s+§V\.[A-G]\s+—\s+Concept\s+\d+:)", text, flags=re.MULTILINE)
    for block in concept_blocks:
        title_match = re.match(r"##\s+§V\.[A-G]\s+—\s+(Concept\s+\d+:\s+[^\n]+)", block)
        if not title_match:
            continue
        concept_title = title_match.group(1).strip()
        # Find the defence callout
        defence_match = re.search(
            r"###\s+Defending the choice in 30 seconds\s*\n\s*>\s*\*?(.+?)\*?\n\s*\n",
            block,
            re.DOTALL,
        )
        if not defence_match:
            continue
        defence = clean_for_anki(defence_match.group(1).strip().strip('"'))
        cards.append({
            "front": f"[Walkthrough • {concept_title}] How do you defend this choice in 30 seconds?",
            "back": defence,
            "tags": f"walkthrough type::defence {_slugify(concept_title)}",
        })
    return cards


def _slugify(text: str) -> str:
    """Make a tag-friendly slug from a title."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")[:40]


# ── Main ─────────────────────────────────────────────────────────────────────

def collect_chapter_cards() -> list[dict]:
    cards: list[dict] = []
    chapters = sorted(LEARNING_DIR.glob("[0-9][0-9]_*.md"))
    if not chapters:
        print("No chapter files found in docs/learning_econometrics/", file=sys.stderr)
        return cards

    for ch in chapters:
        text = ch.read_text(encoding="utf-8")
        _, body = split_frontmatter(text)
        cid, title = get_chapter_meta(text)
        cards += extract_recall_cards(body, cid, title)
        cards += extract_try_this_cards(body, cid, title)
        cards += extract_defence_cards(body, cid, title)
    return cards


def write_tsv(cards: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        for card in cards:
            writer.writerow([card["front"], card["back"], card["tags"]])
    print(f"Wrote {len(cards)} cards to {out_path.relative_to(ROOT)}")
    # Summary by type
    by_type = {}
    for card in cards:
        for tag in card["tags"].split():
            if tag.startswith("type::"):
                t = tag.split("::")[1]
                by_type[t] = by_type.get(t, 0) + 1
    for t, count in sorted(by_type.items()):
        print(f"  type::{t}: {count}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT,
                        help=f"Output TSV path (default: {DEFAULT_OUT.relative_to(ROOT)})")
    parser.add_argument("--include-walkthrough", action="store_true",
                        help="Also include the 8 'Defending the choice' rehearsals from the empirical walkthrough doc")
    args = parser.parse_args()

    cards = collect_chapter_cards()

    if args.include_walkthrough and WALKTHROUGH_PATH.exists():
        walkthrough_text = WALKTHROUGH_PATH.read_text(encoding="utf-8")
        wcards = extract_walkthrough_defences(walkthrough_text)
        print(f"Adding {len(wcards)} defence cards from the walkthrough doc", file=sys.stderr)
        cards += wcards

    if not cards:
        print("No cards extracted. Have you drafted any chapters yet?", file=sys.stderr)
        return 1

    write_tsv(cards, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
