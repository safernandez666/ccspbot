import sqlite3

# Establish a connection to the database
conn = sqlite3.connect('sql/QuestionsAnswersDB')

# Create a cursor
cursor = conn.cursor()

cursor.execute("INSERT INTO Questions (QuestionText) VALUES (?)",
               ("What does the management plane typically utilize to perform administrative functions on the hypervisors that it has access to?",))

# Get the ID of the newly inserted question
cursor.execute("SELECT last_insert_rowid() AS LastID")
last_inserted_id = cursor.fetchone()[0]

# Insert the answers for that question into the "Answers" table
answers = [
    (last_inserted_id, 'Scripts', 0),
    (last_inserted_id, 'RDP', 0),
    (last_inserted_id, 'APIs', 1),
    (last_inserted_id, 'XML', 0)
]

cursor.executemany("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", answers)

# Confirm the changes and close the connection
conn.commit()
conn.close()
