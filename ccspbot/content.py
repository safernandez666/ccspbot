"""Load and validate the question bank held in content/*.json.

The JSON files are the source of truth. Everything downstream - the SQLite
build, the tests, the bot - reads through this module, so a rule enforced here
is enforced everywhere.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from ccspbot import outline

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"

#: Explanations shorter than this are almost always a restatement of the
#: correct answer rather than a reason, which teaches nothing.
MIN_EXPLANATION_CHARS = 80

#: Inline keyboard buttons stop being readable well before this, but a hard
#: cap keeps a runaway answer from breaking the layout entirely.
MAX_ANSWER_CHARS = 200

ANSWERS_PER_QUESTION = 4


@dataclass(frozen=True)
class Answer:
    text: str
    correct: bool


@dataclass(frozen=True)
class Question:
    slug: str
    domain: int
    subdomain: str
    difficulty: int
    text: str
    answers: tuple[Answer, ...]
    explanation: str
    reference: str | None

    @property
    def correct_answer(self) -> Answer:
        return next(a for a in self.answers if a.correct)


def _parse_question(raw: dict, domain: int) -> Question:
    return Question(
        slug=raw["slug"],
        domain=domain,
        subdomain=raw["subdomain"],
        difficulty=raw["difficulty"],
        text=raw["question"],
        answers=tuple(
            Answer(text=a["text"], correct=bool(a.get("correct", False)))
            for a in raw["answers"]
        ),
        explanation=raw["explanation"],
        reference=raw.get("reference"),
    )


def load(content_dir: Path | None = None) -> list[Question]:
    """Read every content/domain-N.json file, in domain order."""
    content_dir = content_dir or CONTENT_DIR
    questions: list[Question] = []

    for domain in sorted(outline.DOMAINS):
        path = content_dir / f"domain-{domain}.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("domain") != domain:
            raise ValueError(f"{path.name}: 'domain' field is {data.get('domain')}, expected {domain}")
        questions.extend(_parse_question(q, domain) for q in data["questions"])

    return questions


def validate(questions: list[Question]) -> list[str]:
    """Return a list of human-readable problems. Empty means the bank is sound.

    Every rule here exists because breaking it produces either a broken bot or
    a question that cannot teach anything.
    """
    errors: list[str] = []
    seen_slugs: dict[str, str] = {}
    seen_texts: dict[str, str] = {}

    for q in questions:
        where = f"[{q.slug}]"

        if q.slug in seen_slugs:
            errors.append(f"{where} duplicate slug (also used by a question in domain {seen_slugs[q.slug]})")
        seen_slugs[q.slug] = str(q.domain)

        expected_prefix = f"d{q.domain}-"
        if not q.slug.startswith(expected_prefix) or not q.slug[len(expected_prefix):].isdigit():
            errors.append(f"{where} slug must look like {expected_prefix}0001")

        normalised = " ".join(q.text.lower().split())
        if normalised in seen_texts:
            errors.append(f"{where} duplicate question text (also in {seen_texts[normalised]})")
        seen_texts[normalised] = q.slug

        if q.subdomain not in outline.SUBDOMAINS:
            errors.append(f"{where} unknown subdomain {q.subdomain!r}")
        elif outline.domain_of(q.subdomain) != q.domain:
            errors.append(f"{where} subdomain {q.subdomain} does not belong to domain {q.domain}")

        if q.difficulty not in outline.DIFFICULTIES:
            errors.append(f"{where} difficulty {q.difficulty} is not one of {sorted(outline.DIFFICULTIES)}")

        if len(q.answers) != ANSWERS_PER_QUESTION:
            errors.append(f"{where} has {len(q.answers)} answers, expected {ANSWERS_PER_QUESTION}")

        correct = [a for a in q.answers if a.correct]
        if len(correct) != 1:
            errors.append(f"{where} has {len(correct)} correct answers, expected exactly 1")

        answer_texts = [" ".join(a.text.lower().split()) for a in q.answers]
        if len(set(answer_texts)) != len(answer_texts):
            errors.append(f"{where} has duplicate answer options")

        for a in q.answers:
            if not a.text.strip():
                errors.append(f"{where} has an empty answer option")
            elif len(a.text) > MAX_ANSWER_CHARS:
                errors.append(f"{where} answer is {len(a.text)} chars, over the {MAX_ANSWER_CHARS} limit")

        if len(q.explanation.strip()) < MIN_EXPLANATION_CHARS:
            errors.append(
                f"{where} explanation is {len(q.explanation.strip())} chars; "
                f"under {MIN_EXPLANATION_CHARS} it is a restatement, not a reason"
            )

    return errors


def distribution(questions: list[Question]) -> dict[int, int]:
    """Question count per domain."""
    counts = {d: 0 for d in outline.DOMAINS}
    for q in questions:
        counts[q.domain] = counts.get(q.domain, 0) + 1
    return counts


def distribution_report(questions: list[Question]) -> str:
    """A table of where the bank stands against the official domain weights."""
    counts = distribution(questions)
    total = len(questions)
    lines = [f"{'Domain':<52} {'have':>5} {'target':>7} {'share':>7} {'weight':>7}"]

    for d, (title, weight) in outline.DOMAINS.items():
        have = counts[d]
        share = have / total if total else 0.0
        lines.append(
            f"{d}. {title:<49} {have:>5} {outline.target_count(d):>7} "
            f"{share:>6.1%} {weight:>6.0%}"
        )

    lines.append(f"{'TOTAL':<52} {total:>5} {outline.TARGET_BANK_SIZE:>7}")
    return "\n".join(lines)
