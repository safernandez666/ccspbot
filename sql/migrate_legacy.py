#!/usr/bin/env python3
"""Convert the original QuestionsAnswersDB into the JSON content format.

The legacy database holds the question and answer text but no domain,
subdomain, or explanation. Those are supplied by content/legacy_tags.json,
keyed by the legacy QuestionID:

    "42": {
      "subdomain": "3.1",
      "difficulty": 2,
      "explanation": "...",
      "reference": "..."
    }

A legacy question can also be retired, which records why rather than silently
dropping it:

    "28": {"drop": "Safe Harbor was invalidated by Schrems I in 2015."}

Where the legacy bank marked the wrong option as correct, the tag states the
answer that is actually right. The migration then moves the flag and fails
loudly if that text is not one of the four options:

    "46": {"subdomain": "4.1", ..., "correct": "Cross-site scripting"}

Questions with no entry are reported as untagged and left out, so the
migration can run in batches while tagging is still in progress.

    python sql/migrate_legacy.py --legacy-db sql/QuestionsAnswersDB
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ccspbot import outline  # noqa: E402

TAGS_PATH = ROOT / "content" / "legacy_tags.json"
CONTENT_DIR = ROOT / "content"


def read_legacy(db_path: Path) -> dict[int, dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    questions: dict[int, dict] = {}
    for row in conn.execute("SELECT QuestionID, QuestionText FROM Questions ORDER BY QuestionID"):
        questions[row["QuestionID"]] = {"text": row["QuestionText"], "answers": []}

    for row in conn.execute("SELECT QuestionID, AnswerText, IsCorrect FROM Answers ORDER BY AnswerID"):
        questions[row["QuestionID"]]["answers"].append(
            {"text": row["AnswerText"], "correct": bool(row["IsCorrect"])}
        )

    conn.close()
    return questions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy-db", type=Path, default=ROOT / "sql" / "QuestionsAnswersDB")
    args = parser.parse_args()

    legacy = read_legacy(args.legacy_db)
    tags = json.loads(TAGS_PATH.read_text(encoding="utf-8")) if TAGS_PATH.exists() else {}

    by_domain: dict[int, list[dict]] = defaultdict(list)
    seen_text: dict[str, int] = {}
    untagged: list[int] = []
    dropped: list[tuple[int, str]] = []
    deduped: list[tuple[int, int]] = []
    corrected: list[tuple[int, str]] = []

    for qid, q in legacy.items():
        tag = tags.get(str(qid))
        if tag is None:
            untagged.append(qid)
            continue
        if "drop" in tag:
            dropped.append((qid, tag["drop"]))
            continue

        answers = [dict(a) for a in q["answers"]]
        if "correct" in tag:
            wanted = tag["correct"]
            if wanted not in [a["text"] for a in answers]:
                raise ValueError(
                    f"legacy {qid}: correction {wanted!r} is not one of the options: "
                    + " | ".join(a["text"] for a in answers)
                )
            for a in answers:
                a["correct"] = a["text"] == wanted
            corrected.append((qid, wanted))

        normalised = " ".join(q["text"].lower().split())
        if normalised in seen_text:
            deduped.append((qid, seen_text[normalised]))
            continue
        seen_text[normalised] = qid

        domain = outline.domain_of(tag["subdomain"])
        by_domain[domain].append(
            {
                "slug": None,  # assigned below, once the domain ordering is known
                "subdomain": tag["subdomain"],
                "difficulty": tag["difficulty"],
                "question": q["text"],
                "answers": answers,
                "explanation": tag["explanation"],
                "reference": tag.get("reference"),
                "_legacy_id": qid,
            }
        )

    CONTENT_DIR.mkdir(exist_ok=True)
    written = 0
    for domain in sorted(outline.DOMAINS):
        items = sorted(by_domain.get(domain, []), key=lambda q: q["_legacy_id"])
        for i, q in enumerate(items, start=1):
            q["slug"] = f"d{domain}-{i:04d}"
            del q["_legacy_id"]

        path = CONTENT_DIR / f"domain-{domain}.json"
        path.write_text(
            json.dumps({"domain": domain, "questions": items}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        written += len(items)
        print(f"domain-{domain}.json: {len(items)} questions")

    print(f"\nMigrated {written} of {len(legacy)} legacy rows.")
    if deduped:
        print(f"Skipped {len(deduped)} duplicates: " + ", ".join(f"{a}=={b}" for a, b in deduped))
    if corrected:
        print(f"Corrected {len(corrected)} wrongly-keyed answers:")
        for qid, wanted in corrected:
            print(f"  {qid}: correct answer is now {wanted!r}")
    if dropped:
        print(f"Retired {len(dropped)}:")
        for qid, why in dropped:
            print(f"  {qid}: {why}")
    if untagged:
        print(f"Still untagged ({len(untagged)}): {', '.join(map(str, untagged))}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
