import sqlite3

# Establish a connection to the database
conn = sqlite3.connect('sql/QuestionsAnswersDB')

# Create a cursor
cursor = conn.cursor()

cursor.execute("INSERT INTO Questions (QuestionText) VALUES (?)",
               ("What type of PII is controlled based on laws and carries legal penalties for noncompliance with requirements?",))

# Get the ID of the newly inserted question
cursor.execute("SELECT last_insert_rowid() AS LastID")
last_inserted_id = cursor.fetchone()[0]

# Insert the answers for that question into the "Answers" table
answers = [
    (last_inserted_id, 'Regulated', 1),
    (last_inserted_id, 'Contractual', 0),
    (last_inserted_id, 'Specific', 0),
    (last_inserted_id, 'Jurisdictional', 0)
]

cursor.executemany("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", answers)

# Confirm the changes and close the connection
conn.commit()
conn.close()
