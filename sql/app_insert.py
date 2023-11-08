import sqlite3

# Establish a connection to the database
conn = sqlite3.connect('sql/QuestionsAnswersDB')

# Create a cursor
cursor = conn.cursor()

cursor.execute("INSERT INTO Questions (QuestionText) VALUES (?)",
               ("What is the biggest negative to leasing space in a data center versus building or maintain your own?",))

# Get the ID of the newly inserted question
cursor.execute("SELECT last_insert_rowid() AS LastID")
last_inserted_id = cursor.fetchone()[0]

# Insert the answers for that question into the "Answers" table
answers = [
    (last_inserted_id, 'Regulation', 0),
    (last_inserted_id, 'Certification', 0),
    (last_inserted_id, 'Costs', 0),
    (last_inserted_id, 'Control', 1)
]

cursor.executemany("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", answers)

# Confirm the changes and close the connection
conn.commit()
conn.close()
