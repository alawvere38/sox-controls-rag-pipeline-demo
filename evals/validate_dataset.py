"""Validate evals/dataset.jsonl against the knowledge-base corpus.

Checks that the golden eval set is internally consistent and grounded:
  - every line is valid JSON with the required fields and a known category
  - ids are unique
  - refusal items (expect_refusal=true) carry no expectations
  - answerable items list at least one expected source and key fact
  - every expected/acceptable source file exists in knowledge-base/
  - acceptable_citation_sources is a superset of expected_sources
  - every expected control ID appears verbatim in at least one expected source file
  - control IDs used as refusal bait (e.g. ITGC-AC-99) do NOT exist in the corpus

Run: python evals/validate_dataset.py
Exits non-zero on any failure.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE = REPO_ROOT / "knowledge-base"
DATASET = REPO_ROOT / "evals" / "dataset.jsonl"

CATEGORIES = {
    "in_scope_single_control",
    "in_scope_process_level",
    "cross_document",
    "out_of_scope",
    "not_in_corpus",
}
REQUIRED_FIELDS = [
    "id",
    "category",
    "question",
    "expected_key_facts",
    "expected_sources",
    "acceptable_citation_sources",
    "expected_control_ids",
    "expect_refusal",
]
CONTROL_ID_PATTERN = re.compile(r"\b(?:ITGC-[A-Z]+|OTC|PTP|FC)-\d{2}\b")


def main() -> int:
    errors = []
    corpus = {p.name: p.read_text() for p in sorted(KNOWLEDGE_BASE.glob("*.md"))}
    corpus_text = "\n".join(corpus.values())

    items = []
    for lineno, line in enumerate(DATASET.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            items.append((lineno, json.loads(line)))
        except json.JSONDecodeError as exc:
            errors.append(f"line {lineno}: invalid JSON ({exc})")

    dupes = [i for i, n in Counter(item["id"] for _, item in items).items() if n > 1]
    if dupes:
        errors.append(f"duplicate ids: {dupes}")

    for lineno, item in items:
        label = f"{item.get('id', f'line {lineno}')}"
        missing = [f for f in REQUIRED_FIELDS if f not in item]
        if missing:
            errors.append(f"{label}: missing fields {missing}")
            continue
        if item["category"] not in CATEGORIES:
            errors.append(f"{label}: unknown category {item['category']!r}")

        if item["expect_refusal"]:
            for field in ("expected_key_facts", "expected_sources",
                          "acceptable_citation_sources", "expected_control_ids"):
                if item[field]:
                    errors.append(f"{label}: refusal item must have empty {field}")
            # bait control IDs in the question must not actually exist
            for cid in CONTROL_ID_PATTERN.findall(item["question"]):
                if cid in corpus_text:
                    errors.append(f"{label}: bait control ID {cid} exists in corpus")
            continue

        if not item["expected_sources"]:
            errors.append(f"{label}: answerable item needs expected_sources")
        if not item["expected_key_facts"]:
            errors.append(f"{label}: answerable item needs expected_key_facts")

        for src in item["expected_sources"] + item["acceptable_citation_sources"]:
            if src not in corpus:
                errors.append(f"{label}: source file not in knowledge-base/: {src}")
        if not set(item["expected_sources"]) <= set(item["acceptable_citation_sources"]):
            errors.append(f"{label}: acceptable_citation_sources must include all expected_sources")

        expected_text = "\n".join(corpus.get(s, "") for s in item["expected_sources"])
        for cid in item["expected_control_ids"]:
            if cid not in expected_text:
                errors.append(f"{label}: control ID {cid} not found in expected sources")

    counts = Counter(item["category"] for _, item in items if "category" in item)
    print(f"dataset: {len(items)} items")
    for cat in sorted(counts):
        print(f"  {cat}: {counts[cat]}")

    if errors:
        print(f"\nFAIL — {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nOK — all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
