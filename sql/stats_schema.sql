-- Per-user attempt history. Lives in its own database on a mounted volume so
-- that rebuilding the question bank never destroys a user's progress.
--
-- Attempts reference the question Slug rather than its rowid, because rowids
-- are reassigned on every rebuild and slugs are stable by contract.

CREATE TABLE IF NOT EXISTS Attempts (
    AttemptID    INTEGER PRIMARY KEY,
    UserID       INTEGER NOT NULL,
    QuestionSlug TEXT    NOT NULL,
    DomainID     INTEGER NOT NULL,
    IsCorrect    INTEGER NOT NULL CHECK (IsCorrect IN (0, 1)),
    AnsweredAt   TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_attempts_user   ON Attempts(UserID);
CREATE INDEX IF NOT EXISTS idx_attempts_lookup ON Attempts(UserID, QuestionSlug);
