import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO subreddits(title, sentiment) VALUES (?, ?)",
            ('First Sub', 'NULL')
            )

cur.execute("INSERT INTO subreddits(title, sentiment) VALUES (?, ?)",
            ('Second Sub', 'NULL')
            )

connection.commit()
connection.close()
