#!/usr/bin/env python3
"""Append a batch of new questions to content/domain-N.json.

Takes a JSON file holding a list of question objects without slugs, groups them
by the domain implied by each subdomain, and appends them to the right file with
the next free slug in that domain.

Slugs are assigned here rather than by hand because attempt history references
them: an accidentally reused slug would silently reattribute someone's answers
to a different question. Existing slugs are never renumbered.

    python sql/add_questions.py content/_new_d5.json
    python sql/add_questions.py content/_new_d5.json --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ccspbot import content, outline  # noqa: E402

CONTENT_DIR = ROOT / "content"

FIELD_ORDER = ["slug", "subdomain", "difficulty", "question", "answers", "explanation", "reference"]


def next_index(existing: list[dict], domain: int) -> int:
    prefix = f"d{domain}-"
    used = [
        int(q["slug"][len(prefix):])
        for q in existing
        if q.get("slug", "").startswith(prefix) and q["slug"][len(prefix):].isdigit()
    ]
    return max(used, default=0) + 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path, help="JSON file holding a list of question objects")
    parser.add_argument("--dry-run", action="store_true", help="report what would change, write nothing")
    args = parser.parse_args()

    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    if not isinstance(batch, list):
        print(f"{args.batch} must hold a JSON list of question objects", file=sys.stderr)
        return 1

    by_domain: dict[int, list[dict]] = defaultdict(list)
    for q in batch:
        if q.get("subdomain") not in outline.SUBDOMAINS:
            print(f"unknown subdomain {q.get('subdomain')!r} in batch", file=sys.stderr)
            return 1
        by_domain[outline.domain_of(q["subdomain"])].append(q)

    for domain, new in sorted(by_domain.items()):
        path = CONTENT_DIR / f"domain-{domain}.json"
        data = (
            json.loads(path.read_text(encoding="utf-8"))
            if path.exists()
            else {"domain": domain, "questions": []}
        )

        index = next_index(data["questions"], domain)
        for q in new:
            q["slug"] = f"d{domain}-{index:04d}"
            index += 1

        data["questions"].extend({k: q.get(k) for k in FIELD_ORDER} for q in new)

        if not args.dry_run:
            path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )

        first, last = new[0]["slug"], new[-1]["slug"]
        print(f"domain-{domain}.json: +{len(new)} ({first}..{last}) -> {len(data['questions'])} total")

    questions = content.load() if args.dry_run is False else None
    if questions is not None:
        errors = content.validate(questions)
        if errors:
            print(f"\n{len(errors)} validation problem(s):", file=sys.stderr)
            for e in errors:
                print(f"  {e}", file=sys.stderr)
            return 1
        print("\n" + content.distribution_report(questions))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
