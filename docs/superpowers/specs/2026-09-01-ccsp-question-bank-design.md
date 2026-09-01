# CCSP Question Bank — Design

Date: 2026-09-01
Status: Approved

## Problem

`ccspbot` is a Telegram quiz bot for CCSP exam prep. It has 140 questions
(130 unique — 10 texts are duplicated), none tagged by domain, none carrying
an explanation. That is not enough material to train against: the exam serves
100–150 adaptive items, so a 130-question bank is memorised in two or three
passes.

The content is also aligned to the retired exam outline. The outline in force
changed on 1 August 2026 and the exam moved to CAT on 1 October 2025. The
current bank has zero questions on DevOps, containers, Kubernetes, serverless,
CASB, or zero trust, and effectively zero on AI/ML — which the new outline
added as subdomains 1.6 and 2.9. At least one question (Safe Harbor) tests a
framework that no longer exists.

Three defects also break the bot at runtime; see "Known defects".

## Goals

- Grow the bank to ~600 questions, distributed by official domain weight.
- Tag every question with domain, subdomain, and difficulty.
- Give every question an explanation that says why the distractors are wrong.
- Make the content reviewable in git.
- Let the user practise by domain, sit a mock exam, and see where they are weak.

## Non-goals

- Reproducing ISC2 exam items. Questions are original, written against the
  public exam outline. Braindumps are under NDA, frequently wrong, and
  calibrated to the retired outline.
- Supporting item types beyond 4-option single-answer multiple choice.

## Exam outline in force (effective 1 August 2026)

| # | Domain | Weight | Target questions |
|---|--------|--------|------------------|
| 1 | Cloud Concepts, Architecture and Design | 17% | 102 |
| 2 | Cloud Data Security | 20% | 120 |
| 3 | Cloud Platform and Infrastructure Security | 17% | 102 |
| 4 | Cloud Application Security | 16% | 96 |
| 5 | Cloud Security Operations | 17% | 102 |
| 6 | Legal, Risk and Compliance | 13% | 78 |

Format: CAT, 3 hours, 100–150 items, pass at 700/1000.

## Architecture

### Content is JSON, not a binary database

Today `sql/QuestionsAnswersDB` is a 48 KB binary committed to git. A question
cannot be diffed, reviewed, or corrected in a pull request, and `sql/backup.sql`
has already drifted out of sync with it.

The source of truth becomes `content/domain-{1..6}.json`. `sql/build_db.py`
compiles those into SQLite. The database is generated, and gitignored.

```json
{
  "domain": 2,
  "questions": [
    {
      "slug": "d2-0001",
      "subdomain": "2.3",
      "difficulty": 2,
      "question": "...",
      "answers": [
        {"text": "...", "correct": true},
        {"text": "...", "correct": false},
        {"text": "...", "correct": false},
        {"text": "...", "correct": false}
      ],
      "explanation": "...",
      "reference": "CCSP Domain 2.3 - Data obfuscation"
    }
  ]
}
```

`slug` is stable and hand-assigned. Attempt history references it, so the bank
can be rebuilt without losing a user's statistics.

### Two databases, split by mutability

| File | Contents | Lifecycle |
|------|----------|-----------|
| `sql/questions.db` | Domains, Questions, Answers | Generated at build time, ships in the image, read-only |
| `data/stats.db` | Attempts | Created at runtime, lives on a mounted volume |

Rebuilding the bank therefore never destroys attempt history. This is why the
two cannot share one file.

### Modules

| Module | Responsibility |
|--------|----------------|
| `ccspbot/content.py` | Load and validate `content/*.json` |
| `ccspbot/db.py` | All SQL. Question sampling, attempt recording, stats queries |
| `ccspbot/quiz.py` | Session state machine. No Telegram imports |
| `ccspbot/handlers.py` | Telegram handlers. No SQL |
| `sql/build_db.py` | content JSON -> `questions.db` |
| `app.py` | Entry point: wiring only |

`quiz.py` holds no Telegram types so the session logic is testable without a
bot token.

## Bot behaviour

| Command | Behaviour |
|---------|-----------|
| `/askchallenge [n]` | n questions (default 10, max 50), sampled by domain weight |
| `/domain <1-6>` | Practise one domain |
| `/exam` | 50-question mock, scored overall and per domain |
| `/stats` | Historical accuracy per domain |
| `/weak` | Only questions previously answered wrong |

Sampling never repeats a question inside a session.

After each answer the bot sends the explanation as a **message**, not as a
callback alert: `answerCallbackQuery` truncates at 200 characters and most
explanations are longer.

## Known defects, and where each is fixed

| Defect | Fix |
|--------|-----|
| `callback_data` carries full answer text; Telegram caps it at 64 bytes and 11 answers exceed that, so those questions raise `BadRequest` | Send `AnswerID` instead |
| `random.randint(1, COUNT(*))` assumes contiguous IDs; deleting any question crashes the bot | `ORDER BY RANDOM() LIMIT 1` |
| A question can repeat inside one round | Sample without replacement |
| `display_results` defined twice; the first is dead code | Removed in the rewrite |
| Session state in module-level dicts; lost on restart | Attempts persisted to `stats.db` |
| `TOKEN_BOT` passed as a Docker `ARG` and baked with `ENV`, then pushed to a public registry — the token is readable in the image layers | Removed from `Dockerfile` and CI; injected at runtime. **The existing token must be rotated.** |
| `python-telegram-bot==12.7` (2020, unmaintained) | Upgrade to 21.x |
| `python-decouple` unpinned | Pinned |

## Testing

`tests/test_content.py` runs in CI and fails the build on:

- a question without exactly 4 answers, or without exactly 1 correct answer
- a subdomain not present in the official outline
- an empty explanation, or one shorter than 80 characters
- duplicate question text, across all domains
- duplicate answer text within a question
- duplicate or malformed slugs
- domain distribution drifting more than 3 percentage points from the official weight

`tests/test_quiz.py` covers the session state machine against a temporary
database: sampling without replacement, scoring, and weak-question selection.

## Delivery phases

| Phase | Output |
|-------|--------|
| F0 | Token removed from image and CI; dependencies pinned |
| F1 | Schema, `build_db.py`, content contract, 130 legacy questions migrated and tagged |
| F2 | PTB 21 rewrite, five commands, persistent stats, tests, CI |
| F3+ | Batches of ~100 new questions to 600, prioritising the uncovered topics |

The `app.py` bug fixes are folded into F2 rather than patched in F0, because
the rewrite replaces those handlers wholesale.
