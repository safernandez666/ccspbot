"""Session state machine and sampling, against a temporary database."""

import random

import pytest

from ccspbot import content, outline, quiz
from ccspbot.db import QuestionBank, StatsStore


@pytest.fixture(scope="module")
def bank(tmp_path_factory):
    import sql.build_db as build_db  # noqa: PLC0415

    db_path = tmp_path_factory.mktemp("bank") / "questions.db"
    build_db.build(db_path, content.load())
    b = QuestionBank(db_path)
    yield b
    b.close()


@pytest.fixture
def stats(tmp_path):
    s = StatsStore(tmp_path / "stats.db")
    yield s
    s.close()


def test_sample_never_repeats_a_question(bank):
    items = bank.sample(20, rng=random.Random(1))
    assert len({i.slug for i in items}) == len(items)


def test_weighted_sample_never_repeats_a_question(bank):
    items = bank.sample_weighted(40, rng=random.Random(2))
    assert len({i.slug for i in items}) == len(items)


def test_weighted_sample_returns_the_requested_count(bank):
    """Domains short of their quota must not silently shrink the round."""
    assert len(bank.sample_weighted(40, rng=random.Random(3))) == 40


def test_sample_by_domain_returns_only_that_domain(bank):
    for d in outline.DOMAINS:
        for item in bank.sample(5, domain=d, rng=random.Random(d)):
            assert item.domain == d


def test_sample_with_empty_slug_list_returns_nothing(bank):
    assert bank.sample(10, slugs=[]) == []


def test_every_option_carries_a_distinct_id(bank):
    for item in bank.sample(30, rng=random.Random(4)):
        ids = [o.answer_id for o in item.options]
        assert len(set(ids)) == len(ids)


def test_scoring_a_correct_answer(bank):
    session = quiz.Session(items=bank.sample(3, rng=random.Random(5)))
    correct, item = session.answer(session.current.correct.answer_id)
    assert correct
    assert session.correct_count == 1
    assert session.index == 1


def test_scoring_a_wrong_answer(bank):
    session = quiz.Session(items=bank.sample(3, rng=random.Random(6)))
    wrong = next(o for o in session.current.options if not o.is_correct)
    correct, _ = session.answer(wrong.answer_id)
    assert not correct
    assert session.correct_count == 0


def test_session_finishes_after_every_question(bank):
    session = quiz.Session(items=bank.sample(4, rng=random.Random(7)))
    for _ in range(4):
        assert not session.finished
        session.answer(session.current.correct.answer_id)
    assert session.finished
    assert session.percentage == 100.0
    assert session.scaled_score == 1000


def test_stale_button_is_rejected(bank):
    """A tap on a previous question's keyboard must not score the current one."""
    session = quiz.Session(items=bank.sample(2, rng=random.Random(8)))
    stale = session.current.options[0].answer_id
    session.answer(session.current.correct.answer_id)

    assert not session.owns(stale)
    assert session.owns(session.current.options[0].answer_id)


def test_finished_session_owns_nothing(bank):
    session = quiz.Session(items=bank.sample(1, rng=random.Random(9)))
    answer_id = session.current.options[0].answer_id
    session.answer(answer_id)
    assert not session.owns(answer_id)


def test_domain_breakdown_counts_per_domain(bank):
    session = quiz.Session(items=bank.sample_weighted(12, rng=random.Random(10)))
    while not session.finished:
        session.answer(session.current.correct.answer_id)

    breakdown = session.domain_breakdown()
    assert sum(n for _, n in breakdown.values()) == 12
    assert all(ok == n for ok, n in breakdown.values())


def test_weak_slugs_tracks_the_most_recent_attempt(bank, stats):
    """A question answered wrong then right is no longer weak."""
    stats.record(1, "d1-0001", 1, is_correct=False)
    assert stats.weak_slugs(1) == ["d1-0001"]

    stats.record(1, "d1-0001", 1, is_correct=True)
    assert stats.weak_slugs(1) == []


def test_weak_slugs_are_per_user(bank, stats):
    stats.record(1, "d1-0002", 1, is_correct=False)
    assert stats.weak_slugs(2) == []


def test_accuracy_by_domain(bank, stats):
    stats.record(9, "d2-0001", 2, is_correct=True)
    stats.record(9, "d2-0002", 2, is_correct=False)
    stats.record(9, "d3-0001", 3, is_correct=True)

    assert stats.accuracy_by_domain(9) == {2: (1, 2), 3: (1, 1)}


def test_results_render_without_error(bank):
    session = quiz.Session(items=bank.sample_weighted(10, rng=random.Random(11)), label="exam")
    while not session.finished:
        session.answer(session.current.correct.answer_id)

    text = quiz.format_results(session)
    assert "1000/1000" in text or "PASS" in text
