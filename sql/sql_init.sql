-- Create the Questions table
CREATE TABLE Questions (
    QuestionID INTEGER PRIMARY KEY,
    QuestionText TEXT
);

-- Create the Answers table
CREATE TABLE Answers (
    AnswerID INTEGER PRIMARY KEY,
    QuestionID INTEGER,
    AnswerText TEXT,
    IsCorrect BOOLEAN
);
