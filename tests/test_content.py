"""Content quality gate.

These run in CI. A question that fails any of them either breaks the bot or
teaches something false, which is worse than not having the question at all.
"""

import pytest

from ccspbot import content, outline

QUESTIONS = content.load()


def test_bank_is_not_empty():
    assert QUESTIONS, "content/ contains no questions"


def test_no_validation_errors():
    errors = content.validate(QUESTIONS)
    assert not errors, "\n" + "\n".join(errors)


@pytest.mark.parametrize("q", QUESTIONS, ids=lambda q: q.slug)
def test_exactly_one_correct_answer(q):
    assert sum(a.correct for a in q.answers) == 1


@pytest.mark.parametrize("q", QUESTIONS, ids=lambda q: q.slug)
def test_four_options(q):
    assert len(q.answers) == content.ANSWERS_PER_QUESTION


@pytest.mark.parametrize("q", QUESTIONS, ids=lambda q: q.slug)
def test_subdomain_belongs_to_its_domain(q):
    assert q.subdomain in outline.SUBDOMAINS
    assert outline.domain_of(q.subdomain) == q.domain


@pytest.mark.parametrize("q", QUESTIONS, ids=lambda q: q.slug)
def test_explanation_gives_a_reason(q):
    assert len(q.explanation.strip()) >= content.MIN_EXPLANATION_CHARS


@pytest.mark.parametrize("q", QUESTIONS, ids=lambda q: q.slug)
def test_explanation_is_not_just_the_correct_answer(q):
    """An explanation that only names the right option teaches nothing."""
    assert q.explanation.strip().lower() != q.correct_answer.text.strip().lower()


def test_question_text_is_unique():
    seen = {}
    for q in QUESTIONS:
        key = " ".join(q.text.lower().split())
        assert key not in seen, f"{q.slug} duplicates {seen[key]}"
        seen[key] = q.slug


def test_slugs_are_unique():
    slugs = [q.slug for q in QUESTIONS]
    assert len(slugs) == len(set(slugs))


def test_distribution_matches_exam_weights():
    """Enforced only once the bank is close to its target size.

    Below that the bank is still being filled domain by domain, so drift is
    expected rather than a defect. The threshold is what makes this a real
    gate rather than a permanently skipped test.
    """
    total = len(QUESTIONS)
    if total < outline.TARGET_BANK_SIZE * 0.9:
        pytest.skip(
            f"bank has {total} of {outline.TARGET_BANK_SIZE} questions; "
            f"distribution is enforced from {int(outline.TARGET_BANK_SIZE * 0.9)}"
        )

    counts = content.distribution(QUESTIONS)
    for d, (title, weight) in outline.DOMAINS.items():
        share = counts[d] / total
        assert abs(share - weight) <= 0.03, (
            f"domain {d} ({title}) is {share:.1%} of the bank, target {weight:.0%}"
        )
