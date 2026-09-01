"""Database access. Every SQL statement in the project lives here.

Two stores, deliberately separate:

- ``QuestionBank`` reads sql/questions.db, a build artifact regenerated from
  content/*.json. It is read-only at runtime.
- ``StatsStore`` owns data/stats.db, which holds attempt history and lives on
  a mounted volume so rebuilding the bank never destroys a user's progress.

They reference each other only through the question slug, which is stable by
contract.
"""

from __future__ import annotations

import random
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from ccspbot import outline

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_DB = ROOT / "sql" / "questions.db"
STATS_DB = ROOT / "data" / "stats.db"
STATS_SCHEMA = ROOT / "sql" / "stats_schema.sql"


@dataclass(frozen=True)
class Option:
    answer_id: int
    text: str
    is_correct: bool


@dataclass(frozen=True)
class Item:
    """A question as served to a user, with its options already shuffled."""

    slug: str
    domain: int
    subdomain: str
    text: str
    explanation: str
    reference: str | None
    options: tuple[Option, ...]

    @property
    def correct(self) -> Option:
        return next(o for o in self.options if o.is_correct)


class QuestionBank:
    def __init__(self, path: Path = QUESTIONS_DB):
        if not path.exists():
            raise FileNotFoundError(
                f"{path} not found. Build it first: python sql/build_db.py"
            )
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

    def close(self) -> None:
        self._conn.close()

    def total(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM Questions").fetchone()[0]

    def counts_by_domain(self) -> dict[int, int]:
        rows = self._conn.execute(
            "SELECT DomainID, COUNT(*) AS n FROM Questions GROUP BY DomainID"
        ).fetchall()
        return {r["DomainID"]: r["n"] for r in rows}

    def _items_from_rows(self, rows, rng: random.Random) -> list[Item]:
        items = []
        for row in rows:
            options = [
                Option(a["AnswerID"], a["AnswerText"], bool(a["IsCorrect"]))
                for a in self._conn.execute(
                    "SELECT AnswerID, AnswerText, IsCorrect FROM Answers WHERE QuestionID = ?",
                    (row["QuestionID"],),
                )
            ]
            rng.shuffle(options)
            items.append(
                Item(
                    slug=row["Slug"],
                    domain=row["DomainID"],
                    subdomain=row["Subdomain"],
                    text=row["QuestionText"],
                    explanation=row["Explanation"],
                    reference=row["Reference"],
                    options=tuple(options),
                )
            )
        return items

    def sample(
        self,
        n: int,
        domain: int | None = None,
        slugs: list[str] | None = None,
        rng: random.Random | None = None,
    ) -> list[Item]:
        """Draw n questions without replacement.

        ``ORDER BY RANDOM()`` rather than picking a random rowid, so that gaps
        in the ID sequence - which a rebuild produces routinely - cannot select
        a question that does not exist.
        """
        rng = rng or random.Random()
        sql = "SELECT * FROM Questions"
        params: list = []
        where = []

        if domain is not None:
            where.append("DomainID = ?")
            params.append(domain)
        if slugs is not None:
            if not slugs:
                return []
            where.append(f"Slug IN ({','.join('?' * len(slugs))})")
            params.extend(slugs)
        if where:
            sql += " WHERE " + " AND ".join(where)

        sql += " ORDER BY RANDOM() LIMIT ?"
        params.append(n)

        return self._items_from_rows(self._conn.execute(sql, params).fetchall(), rng)

    def sample_weighted(self, n: int, rng: random.Random | None = None) -> list[Item]:
        """Draw n questions distributed across domains by official exam weight.

        Domains short of their quota give up their shortfall to the others, so
        an incomplete bank still returns n questions rather than silently
        returning fewer.
        """
        rng = rng or random.Random()
        available = self.counts_by_domain()
        picked: list[Item] = []

        for domain, (_, weight) in outline.DOMAINS.items():
            want = min(round(weight * n), available.get(domain, 0))
            picked.extend(self.sample(want, domain=domain, rng=rng))

        if len(picked) < n:
            have = {i.slug for i in picked}
            for extra in self.sample(n * 2, rng=rng):
                if extra.slug not in have:
                    picked.append(extra)
                    have.add(extra.slug)
                if len(picked) == n:
                    break

        rng.shuffle(picked)
        return picked[:n]


class StatsStore:
    def __init__(self, path: Path = STATS_DB):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(STATS_SCHEMA.read_text(encoding="utf-8"))
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def record(self, user_id: int, slug: str, domain: int, is_correct: bool) -> None:
        self._conn.execute(
            "INSERT INTO Attempts (UserID, QuestionSlug, DomainID, IsCorrect, AnsweredAt) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, slug, domain, int(is_correct), datetime.now(timezone.utc).isoformat()),
        )
        self._conn.commit()

    def accuracy_by_domain(self, user_id: int) -> dict[int, tuple[int, int]]:
        """Return {domain: (correct, attempted)} for one user."""
        rows = self._conn.execute(
            "SELECT DomainID, SUM(IsCorrect) AS ok, COUNT(*) AS n "
            "FROM Attempts WHERE UserID = ? GROUP BY DomainID",
            (user_id,),
        ).fetchall()
        return {r["DomainID"]: (r["ok"], r["n"]) for r in rows}

    def weak_slugs(self, user_id: int, limit: int = 100) -> list[str]:
        """Questions whose most recent attempt by this user was wrong.

        Most recent, not ever-wrong: a question you have since got right is no
        longer a weak spot, and keeping it in the pool would crowd out the ones
        that still are.
        """
        rows = self._conn.execute(
            """
            SELECT QuestionSlug FROM Attempts a
            WHERE UserID = ?
              AND AttemptID = (
                    SELECT MAX(AttemptID) FROM Attempts b
                    WHERE b.UserID = a.UserID AND b.QuestionSlug = a.QuestionSlug
              )
              AND IsCorrect = 0
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return [r["QuestionSlug"] for r in rows]
