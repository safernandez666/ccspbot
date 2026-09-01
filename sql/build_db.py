#!/usr/bin/env python3
"""Compile content/*.json into sql/questions.db.

The database is a build artifact. It is gitignored, rebuilt from scratch on
every run, and never edited by hand.

    python sql/build_db.py            # build, refusing to write if invalid
    python sql/build_db.py --check    # validate only, write nothing
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ccspbot import content, outline  # noqa: E402

DB_PATH = ROOT / "sql" / "questions.db"
SCHEMA_PATH = ROOT / "sql" / "schema.sql"


def build(db_path: Path, questions: list[content.Question]) -> None:
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

    conn.executemany(
        "INSERT INTO Domains (DomainID, Title, Weight) VALUES (?, ?, ?)",
        [(d, title, weight) for d, (title, weight) in outline.DOMAINS.items()],
    )

    for q in questions:
        cur = conn.execute(
            "INSERT INTO Questions "
            "(Slug, QuestionText, DomainID, Subdomain, Difficulty, Explanation, Reference) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (q.slug, q.text, q.domain, q.subdomain, q.difficulty, q.explanation, q.reference),
        )
        conn.executemany(
            "INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)",
            [(cur.lastrowid, a.text, int(a.correct)) for a in q.answers],
        )

    conn.commit()
    conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate only, do not write the database")
    args = parser.parse_args()

    questions = content.load()
    if not questions:
        print("No questions found in content/. Nothing to build.", file=sys.stderr)
        return 1

    errors = content.validate(questions)
    if errors:
        print(f"{len(errors)} problem(s) in the question bank:\n", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(content.distribution_report(questions))

    if args.check:
        print("\nContent is valid. Nothing written (--check).")
        return 0

    build(DB_PATH, questions)
    print(f"\nBuilt {DB_PATH.relative_to(ROOT)} with {len(questions)} questions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
