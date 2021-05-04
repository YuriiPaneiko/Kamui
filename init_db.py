import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, agent, content) VALUES (?, ?, ?)",
            ('First Post', 'Azure','Content for the first post')
            )

cur.execute("INSERT INTO posts (title, agent, content) VALUES (?, ?, ?)",
            ('Second Post', 'Google','Content for the second post')
            )

connection.commit()
connection.close()
