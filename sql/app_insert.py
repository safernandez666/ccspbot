import sqlite3

# Establecer una conexión a la base de datos
conn = sqlite3.connect('QuestionsAnswersDB')

# Crear un cursor
cursor = conn.cursor()

cursor.execute("INSERT INTO Questions (QuestionText) VALUES (?)",
               ("Which of the following threat types involves an application that does not validate authorization for portions of itself after the initial checks?",))

# Obtener el ID de la pregunta recién insertada
cursor.execute("SELECT last_insert_rowid() AS LastID")
last_inserted_id = cursor.fetchone()[0]

# Insertar las respuestas para esa pregunta en la tabla "Answers"
answers = [
    (last_inserted_id, 'Injection', 0),
    (last_inserted_id, 'Cross-site scripting', 0),
    (last_inserted_id, 'Cross-site request forgery', 0),
    (last_inserted_id, 'Missing function-level access control', 1)
]

cursor.executemany("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", answers)

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()