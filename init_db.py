import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, agent, content) VALUES (?, ?, ?)",
            ('First Post', 'Azure','echo $PATH')
            )

cur.execute("INSERT INTO posts (title, agent, content) VALUES (?, ?, ?)",
            ('Second Post', 'Google','echo $HOME')
            )

connection.commit()
connection.close()
