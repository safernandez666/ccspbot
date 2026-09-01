"""The quiz session state machine.

This module imports nothing from telegram, so the whole progression - serve a
question, score an answer, advance, finish - is testable without a bot token.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from html import escape

from ccspbot import outline
from ccspbot.db import Item

MAX_QUESTIONS = 50
DEFAULT_QUESTIONS = 10
EXAM_QUESTIONS = 50

#: ISC2 scales the CCSP to 1000 points and passes at 700. Our score is a plain
#: percentage mapped onto that scale, which is a rough indicator and not an
#: equated CAT score - the real exam adapts item difficulty to the candidate.
PASS_MARK = 700


@dataclass
class Session:
    items: list[Item]
    label: str = "challenge"
    index: int = 0
    results: list[bool] = field(default_factory=list)

    @property
    def finished(self) -> bool:
        return self.index >= len(self.items)

    @property
    def current(self) -> Item:
        return self.items[self.index]

    @property
    def position(self) -> str:
        return f"{self.index + 1}/{len(self.items)}"

    def answer(self, answer_id: int) -> tuple[bool, Item]:
        """Score the current question and advance. Returns (was_correct, item)."""
        item = self.current
        correct = any(o.answer_id == answer_id and o.is_correct for o in item.options)
        self.results.append(correct)
        self.index += 1
        return correct, item

    def owns(self, answer_id: int) -> bool:
        """Whether answer_id belongs to the question currently on screen.

        Telegram leaves old keyboards live, so a user can tap a button from a
        question they already answered. Without this check that stale tap would
        be scored against whatever question is now current.
        """
        return not self.finished and any(o.answer_id == answer_id for o in self.current.options)

    @property
    def correct_count(self) -> int:
        return sum(self.results)

    @property
    def percentage(self) -> float:
        return (self.correct_count / len(self.results) * 100) if self.results else 0.0

    @property
    def scaled_score(self) -> int:
        return round(self.percentage * 10)

    def domain_breakdown(self) -> dict[int, tuple[int, int]]:
        """{domain: (correct, attempted)} for the questions answered so far."""
        breakdown: dict[int, list[int]] = {}
        for item, correct in zip(self.items, self.results):
            entry = breakdown.setdefault(item.domain, [0, 0])
            entry[0] += int(correct)
            entry[1] += 1
        return {d: (ok, n) for d, (ok, n) in breakdown.items()}


def format_results(session: Session) -> str:
    """Render the end-of-session summary as Telegram HTML."""
    lines = [
        f"<b>{escape(session.label.title())} complete</b>",
        "",
        f"Score: {session.correct_count}/{len(session.results)}  ({session.percentage:.0f}%)",
    ]

    if session.label == "exam":
        verdict = "PASS" if session.scaled_score >= PASS_MARK else "BELOW PASS MARK"
        lines.append(f"Scaled: {session.scaled_score}/1000 - {verdict} (pass is {PASS_MARK})")

    breakdown = session.domain_breakdown()
    if len(breakdown) > 1:
        lines += ["", "<b>By domain</b>"]
        for domain in sorted(breakdown):
            ok, n = breakdown[domain]
            title = outline.DOMAINS[domain][0]
            lines.append(f"{domain}. {escape(title)} - {ok}/{n} ({ok / n:.0%})")

    return "\n".join(lines)
