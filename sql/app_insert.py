import sqlite3

# Establish a connection to the database
conn = sqlite3.connect('sql/QuestionsAnswersDB')

# Create a cursor
cursor = conn.cursor()

cursor.execute("INSERT INTO Questions (QuestionText) VALUES (?)",
               ("Which of the following storage types is most closely associated with a database-type storage implementation?",))

# Get the ID of the newly inserted question
cursor.execute("SELECT last_insert_rowid() AS LastID")
last_inserted_id = cursor.fetchone()[0]

# Insert the answers for that question into the "Answers" table
answers = [
    (last_inserted_id, 'Object', 0),
    (last_inserted_id, 'Unstructured', 0),
    (last_inserted_id, 'Volume', 0),
    (last_inserted_id, 'Structured', 1)
]

cursor.executemany("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", answers)

# Confirm the changes and close the connection
conn.commit()
conn.close()
