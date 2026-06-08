import sqlite3

#wir öffnen die akte oder erstellen sie
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#wir bauen eine tbelle für die beiträge mit id, titel und inhalt
cursor.execute('CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)')

#2 test beiträge reinlegen
cursor.execute("INSERT INTO posts (title, content) VALUES ('Erster Beitrag', 'Hallo Welt, das ist mein IT-Security Blog.')")
cursor.execute("INSERT INTO posts (title, content) VALUES ('Streng Geheim', 'Das Admin-Passwort lautet: sommer2026')")

#abspeichern und schlissen
connection.commit()
connection.close()