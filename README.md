# ccspbot

A Telegram bot for practising the **ISC2 Certified Cloud Security Professional (CCSP)** exam.

Ask it for a round of questions, answer with inline buttons, and get an explanation of why the
answer is what it is — not just a tick or a cross. Every question is tagged to a subdomain of the
official exam outline, so the bot can tell you which domain you are weakest in and drill you on it.

## Features

- **Explanations on every question.** Each answer comes with a paragraph on why the correct option
  is correct *and* why the distractors are wrong.
- **Tagged to the live outline.** Every question maps to a subdomain of the ISC2 outline in force
  since 1 August 2026.
- **Exam-weighted practice.** Rounds are sampled to match the real domain weights, so what you
  practise looks like what you sit.
- **Mock exam.** A 50-question run scored per domain and mapped onto the 1000-point scale.
- **Persistent statistics.** Accuracy per domain survives restarts, so `/stats` reflects your whole
  history rather than the current session.
- **Targeted review.** `/weak` serves only the questions you last got wrong.
- **Content as reviewable JSON.** Questions live in `content/*.json`, not in a binary database, so a
  wrong answer can be fixed in a pull request.

## Commands

| Command | What it does |
|---|---|
| `/start` | Bank size and the command list |
| `/askchallenge [n]` | `n` questions (default 10, max 50), weighted like the exam |
| `/domain <1-6>` | Practise one domain |
| `/exam` | 50-question mock, scored overall and per domain |
| `/stats` | Your accuracy per domain, and your weakest one |
| `/weak` | Only the questions you last answered wrong |
| `/domains` | The six domains, their weights, and how many questions each has |

## Prerequisites

- Python 3.9 or newer (or Docker; the image uses 3.12)
- A bot token from [@BotFather](https://t.me/BotFather)

## Installation

```bash
git clone https://github.com/safernandez666/ccspbot.git
cd ccspbot

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Compile content/*.json into sql/questions.db
python sql/build_db.py
```

Then run it:

```bash
export TOKEN_BOT="your-token-from-botfather"
python app.py
```

### Docker

```bash
docker build -t ccspbot .
docker run -e TOKEN_BOT="your-token" -v ccspbot-data:/app/data ccspbot
```

> **The token is passed at run time, never at build time.** A `--build-arg` is written into the
> image history, and this image is published to a public registry. Mount `/app/data` as shown or
> attempt history is lost when the container restarts.

## Project layout

```
content/            Question bank — the source of truth
  domain-{1..6}.json    Questions, one file per CCSP domain
  legacy_tags.json      Domain/explanation tags applied to the original bank
ccspbot/
  outline.py            Domain weights and subdomains from the ISC2 outline
  content.py            Loads and validates content/*.json
  db.py                 All SQL: question sampling, attempts, statistics
  quiz.py               Session state machine (no Telegram imports)
  handlers.py           Telegram handlers (no SQL)
sql/
  schema.sql            Question bank schema
  stats_schema.sql      Attempt history schema
  build_db.py           content/*.json  ->  sql/questions.db
  add_questions.py      Append a batch of questions, assigning slugs
  migrate_legacy.py     Original database  ->  content/*.json
tests/                Content quality gate and session logic
app.py                Entry point — wiring only
```

Two databases, split by mutability. `sql/questions.db` is a build artifact, regenerated from
`content/` and gitignored. `data/stats.db` holds attempt history on a mounted volume, so rebuilding
the bank never destroys your progress. They reference each other only by question slug, which is
stable by contract.

## Adding questions

Write the batch to a JSON file as a list of question objects, leaving out the slug:

```json
[
  {
    "subdomain": "2.3",
    "difficulty": 2,
    "question": "An organization must let analysts report against production records without exposing real card numbers, while preserving joins across tables. Which technique meets this?",
    "answers": [
      {"text": "Tokenization", "correct": true},
      {"text": "Static data masking", "correct": false},
      {"text": "Format-preserving encryption", "correct": false},
      {"text": "Salted hashing", "correct": false}
    ],
    "explanation": "Tokenization substitutes a surrogate held in a vault, and the same input always maps to the same token, so joins still resolve and no reversible key travels with the data. Static masking breaks referential integrity across copies, FPE leaves the value reversible with a key that is still in scope, and salted hashing destroys the join.",
    "reference": "CCSP 2.3 - Data obfuscation"
  }
]
```

Then merge it in and rebuild:

```bash
python sql/add_questions.py batch.json --dry-run   # report what would change
python sql/add_questions.py batch.json             # append, then validate
python sql/build_db.py                             # rebuild sql/questions.db
pytest -q
```

`add_questions.py` routes each question to the file for the domain its subdomain belongs to, and
assigns the next free slug there. Let it do that rather than writing slugs by hand: attempt history
references the slug, so **reusing or renumbering one silently reassigns someone's answer history to
a different question.** Existing slugs are never renumbered.

Every question needs an explanation that says why the distractors are wrong, not just what the
correct answer is — the tests enforce a minimum length, but the standard is whether someone who got
it wrong would now understand why.

## Testing

```bash
pip install -r requirements-dev.txt
pytest -q
```

The suite fails the build on a question with the wrong number of options, no correct answer, an
unknown subdomain, a missing explanation, a duplicate slug or duplicate text — and, once the bank
reaches 90% of its target size, on a domain distribution that drifts more than 3 points from the
official weights.

## Exam outline

The bank is built against the outline effective 1 August 2026: CAT format, 3 hours, 100–150 items,
pass at 700/1000.

| # | Domain | Weight |
|---|---|---|
| 1 | Cloud Concepts, Architecture and Design | 17% |
| 2 | Cloud Data Security | 20% |
| 3 | Cloud Platform and Infrastructure Security | 17% |
| 4 | Cloud Application Security | 16% |
| 5 | Cloud Security Operations | 17% |
| 6 | Legal, Risk and Compliance | 13% |

Source: [ISC2 CCSP exam outline](https://www.isc2.org/certifications/ccsp/ccsp-certification-exam-outline).

Questions are written originally against that public outline. This project does not reproduce ISC2
exam items, which are under NDA.

## Contributing

Pull requests are welcome, particularly new questions in the under-filled domains — run
`python sql/build_db.py` to see where the bank stands. If you spot a wrong answer, open an issue
with the slug; the bank was seeded from an older set and at least two keying errors have already
been found and corrected.

## Contact

Maintained by [@safernandez666](https://github.com/safernandez666).
