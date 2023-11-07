import sqlite3

# Establish a connection to the database
conn = sqlite3.connect('sql/QuestionsAnswersDB')

# Create a cursor
cursor = conn.cursor()

cursor.execute("INSERT INTO Questions (QuestionText) VALUES (?)",
               ("Which concept BEST describes the capability for a cloud environment to automatically scale a system or application, based on its current resource demands?",))

# Get the ID of the newly inserted question
cursor.execute("SELECT last_insert_rowid() AS LastID")
last_inserted_id = cursor.fetchone()[0]

# Insert the answers for that question into the "Answers" table
answers = [
    (last_inserted_id, 'On-demand self-service', 0),
    (last_inserted_id, 'Resource pooling', 0),
    (last_inserted_id, 'Measured service', 0),
    (last_inserted_id, 'Rapid elasticity', 1)
]

cursor.executemany("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", answers)

# Confirm the changes and close the connection
conn.commit()
conn.close()
