"""
Export a learning_econometrics chapter to a Notion-ingestion payload.

Reads a chapter markdown file (with YAML frontmatter conforming to the
_template_chapter.md schema) and emits the structured field-marker block
that the Notion Claude agent can ingest using the conventions in
docs/notion_setup_prompt.md.

Usage:
    python scripts/export_chapter_to_notion.py docs/learning_econometrics/01_counterfactual_question.md

    # Or batch all chapters:
    python scripts/export_chapter_to_notion.py --all

Output goes to stdout by default, or to a sibling .notion.txt file with --write.

Validation:
- Checks that all `requires` slugs in the frontmatter appear in `introduces`
  of some earlier chapter (per concept_graph.yaml).
- Warns if `introduces` slugs are not present in concept_graph.yaml.
- Warns if any `figures` or `interactives` listed in frontmatter don't exist
  on disk.

The exporter is deliberately simple: it parses by section heading, not by
fancy markdown AST. That makes it brittle to non-standard chapter layouts,
which is the point — chapters that don't conform to the template fail loudly.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LEARNING_DIR = ROOT / "docs" / "learning_econometrics"
CONCEPT_GRAPH_PATH = LEARNING_DIR / "concept_graph.yaml"


# ── Frontmatter + section parsing ────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Split a markdown file into (frontmatter dict, body text)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(
            "Chapter file is missing YAML frontmatter. See _template_chapter.md "
            "for the required schema."
        )
    fm = yaml.safe_load(match.group(1))
    body = text[match.end():]
    return fm, body


def split_sections(body: str) -> dict[str, str]:
    """Split the chapter body into sections keyed by heading text.

    Recognises level-2 headings (## ...) as section breaks. Returns a dict
    mapping the heading text (stripped of leading ##) to the section body.
    The first chunk before any ## heading is keyed as '_preamble'.
    """
    sections: dict[str, str] = {}
    current_key = "_preamble"
    current_lines: list[str] = []
    for line in body.splitlines():
        h2_match = re.match(r"^##\s+(.+?)\s*$", line)
        if h2_match:
            sections[current_key] = "\n".join(current_lines).strip()
            current_key = h2_match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    sections[current_key] = "\n".join(current_lines).strip()
    return sections


def find_section(sections: dict[str, str], pattern: str) -> tuple[str, str] | None:
    """Find the first section whose heading matches the regex pattern."""
    for key, value in sections.items():
        if re.search(pattern, key, re.IGNORECASE):
            return key, value
    return None


# ── Validation against concept graph ─────────────────────────────────────────

def load_concept_graph() -> dict:
    if not CONCEPT_GRAPH_PATH.exists():
        return {}
    with open(CONCEPT_GRAPH_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_chapter(fm: dict, graph: dict) -> list[str]:
    """Check frontmatter against the concept graph. Returns list of warnings."""
    warnings = []
    if not graph:
        return ["concept_graph.yaml not found; skipping validation"]

    chapter_id = fm.get("chapter_id")
    introduces = fm.get("introduces") or []
    requires = fm.get("requires") or []

    # Check all `introduces` slugs exist as top-level keys in the graph
    for slug in introduces:
        if slug not in graph:
            warnings.append(f"introduces['{slug}'] not found in concept_graph.yaml")

    # Check all `requires` slugs exist somewhere
    for slug in requires:
        if slug not in graph:
            warnings.append(f"requires['{slug}'] not found in concept_graph.yaml")

    # Check that `requires` are introduced by some chapter with smaller id
    chapters = graph.get("chapters", {})
    if chapter_id and chapter_id in chapters:
        earlier_chapter_ids = [cid for cid in chapters if cid < chapter_id]
        introduced_so_far = set()
        for cid in earlier_chapter_ids:
            introduced_so_far.update(chapters[cid].get("introduces") or [])
        for slug in requires:
            if slug not in introduced_so_far:
                warnings.append(
                    f"requires['{slug}'] is not introduced by any chapter before "
                    f"chapter_id={chapter_id}. Either add it to an earlier chapter's "
                    f"`introduces` list, or remove it from this chapter's `requires`."
                )

    # Check that figures and interactives exist on disk
    for fig in fm.get("figures") or []:
        path = LEARNING_DIR / fig.get("file", "")
        if not path.exists():
            warnings.append(f"figure file not found on disk: {path.relative_to(ROOT)}")
    for inter in fm.get("interactives") or []:
        path = LEARNING_DIR / inter.get("file", "")
        if not path.exists():
            warnings.append(f"interactive file not found on disk: {path.relative_to(ROOT)}")

    return warnings


# ── Field extraction ─────────────────────────────────────────────────────────

def extract_problem_framing(sections: dict[str, str]) -> str:
    """Pull the orientation section (where we're going / section 0)."""
    # Prefer an explicit "Where we're going" heading
    candidate = find_section(sections, r"where\s+we'?re\s+going|introduction|orientation")
    if candidate:
        return candidate[1]
    # Fall back to section "0. ..."
    for key, value in sections.items():
        if re.match(r"^0\.", key):
            return value
    return ""


def extract_concrete_first(sections: dict[str, str]) -> str:
    """Pull the first concrete vignette section (number ≥ 1, skip orientation)."""
    for key, value in sections.items():
        # Match sections numbered 1, 2, 3, ... (not 0., not non-numbered)
        if re.match(r"^[1-9]\d*\.", key):
            return value
    return ""


def extract_defence(body: str) -> str:
    """Pull the first 'Defend the choice' answer block."""
    match = re.search(
        r"\*\*Defend the choice\.?\*\*[^<]*?<details>\s*<summary>[^<]*</summary>\s*\n(.*?)</details>",
        body,
        re.DOTALL,
    )
    if not match:
        return ""
    return match.group(1).strip()


def extract_recall_qa(body: str) -> list[tuple[str, str]]:
    """Pull (question, answer) pairs from end-of-chapter check.

    Looks for patterns like:
        **N.** Question text...
        <details>
        <summary>Answer</summary>
        Answer text...
        </details>
    """
    qa_pairs = []
    pattern = re.compile(
        r"\*\*\d+\.\*\*\s*(.+?)\s*\n\s*<details>\s*<summary>[^<]*</summary>\s*\n(.*?)</details>",
        re.DOTALL,
    )
    for match in pattern.finditer(body):
        question = match.group(1).strip()
        answer = match.group(2).strip()
        qa_pairs.append((question, answer))
    return qa_pairs


def extract_try_this(body: str) -> list[tuple[str, str]]:
    """Pull (prompt, answer) pairs from 'Try this' inline exercises."""
    qa_pairs = []
    pattern = re.compile(
        r">\s*\*\*Try this\.?\*\*\s*(.+?)\s*\n\s*<details>\s*<summary>[^<]*</summary>\s*\n(.*?)</details>",
        re.DOTALL,
    )
    for match in pattern.finditer(body):
        prompt = match.group(1).strip()
        answer = match.group(2).strip()
        qa_pairs.append((prompt, answer))
    return qa_pairs


# ── Notion payload formatting ────────────────────────────────────────────────

def format_payload(fm: dict, body: str) -> str:
    """Format the chapter as a Notion-ingestion payload block."""
    sections = split_sections(body)

    chapter_id = fm.get("chapter_id", "??")
    title = fm.get("title", "Untitled")
    part = fm.get("part", "?")
    status = fm.get("status", "drafted")
    introduces = fm.get("introduces") or []
    requires = fm.get("requires") or []

    figures_block = ""
    for fig in fm.get("figures") or []:
        figures_block += f"- file: {fig.get('file')}\n  caption: \"{fig.get('caption', '')}\"\n"

    interactive_block = ""
    for inter in fm.get("interactives") or []:
        interactive_block += f"- file: {inter.get('file')}\n  description: \"{inter.get('description', '')}\"\n"

    related_block = ""
    for rel in fm.get("related_concepts") or []:
        related_block += f"- chapter_id: {rel.get('chapter_id')}\n  note: \"{rel.get('note', '')}\"\n"

    framing = extract_problem_framing(sections)
    concrete = extract_concrete_first(sections)
    defence = extract_defence(body)
    recall = extract_recall_qa(body)
    try_this = extract_try_this(body)

    recall_block = ""
    for i, (q, a) in enumerate(recall, 1):
        recall_block += f"  {i}. Q: {q}\n     A: {a}\n\n"

    try_this_block = ""
    for i, (q, a) in enumerate(try_this, 1):
        try_this_block += f"  {i}. Prompt: {q}\n     Answer: {a}\n\n"

    payload = f"""## CHAPTER_{chapter_id}

```
Title: {title}
Part: {part}
Status: {status}
Introduces: {', '.join(introduces) if introduces else '(none)'}
Requires: {', '.join(requires) if requires else '(none)'}

PROBLEM_FRAMING:
{framing[:1200]}{'...' if len(framing) > 1200 else ''}

CONCRETE_FIRST:
{concrete[:1500]}{'...' if len(concrete) > 1500 else ''}

DEFENCE_30_SECONDS:
{defence if defence else '(no defence rehearsal in this chapter)'}

RELATED_CONCEPTS:
{related_block.strip() if related_block else '(none)'}

FIGURES:
{figures_block.strip() if figures_block else '(none)'}

INTERACTIVE:
{interactive_block.strip() if interactive_block else '(none)'}

TRY_THIS_EXERCISES (inline, with answers):
{try_this_block.strip() if try_this_block else '(none)'}

END_OF_CHAPTER_RECALL ({len(recall)} questions):
{recall_block.strip() if recall_block else '(none)'}
```
"""
    return payload


# ── Main ─────────────────────────────────────────────────────────────────────

def export_chapter(path: Path, write: bool = False) -> None:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    graph = load_concept_graph()

    warnings = validate_chapter(fm, graph)
    for w in warnings:
        print(f"  WARN [{path.name}]: {w}", file=sys.stderr)

    payload = format_payload(fm, body)

    if write:
        out_path = path.with_suffix(".notion.txt")
        out_path.write_text(payload, encoding="utf-8")
        print(f"Wrote {out_path.relative_to(ROOT)}", file=sys.stderr)
    else:
        print(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chapter", nargs="?", help="Path to a chapter markdown file")
    parser.add_argument("--all", action="store_true", help="Export all chapters in docs/learning_econometrics/")
    parser.add_argument("--write", action="store_true", help="Write to sibling .notion.txt instead of stdout")
    args = parser.parse_args()

    if args.all:
        chapters = sorted(LEARNING_DIR.glob("[0-9][0-9]_*.md"))
        for ch in chapters:
            export_chapter(ch, write=args.write)
        return 0

    if not args.chapter:
        parser.print_help()
        return 1

    path = Path(args.chapter).resolve()
    if not path.exists():
        print(f"Not found: {path}", file=sys.stderr)
        return 1

    export_chapter(path, write=args.write)
    return 0


if __name__ == "__main__":
    sys.exit(main())
