from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    verbindung = sqlite3.connect('database.db')
    cursor = verbindung.cursor()
    
    # Lücke 4: Stored XSS (Beitrag speichern)
    if request.method == "POST":
        neuer_titel = request.form.get("titel")
        neuer_inhalt = request.form.get("inhalt")
        cursor.execute(f"INSERT INTO posts (title, content) VALUES ('{neuer_titel}', '{neuer_inhalt}')")
        verbindung.commit()

    # NEU: HIER IST LÜCKE 5 (IDOR)
    # Wir prüfen ob in der URL "?delete=ID" steht
    loeschen_id = request.args.get("delete")
    if loeschen_id:
        # Wir löschen die angegebene ID einfach ungeprüft aus der Datenbank!
        # Kein Check, ob der Nutzer Admin ist oder ob ihm der Beitrag gehört.
        cursor.execute(f"DELETE FROM posts WHERE id = {loeschen_id}")
        verbindung.commit()

    suche = request.args.get("suchbegriff")
    ergebnisse = []
    
    if suche:
        # Lücke 2: SQL-Injection
        sql_befehl = f"SELECT * FROM posts WHERE title LIKE '%{suche}%'"
        try:
            cursor.execute(sql_befehl)
            ergebnisse = cursor.fetchall()
        except sqlite3.Error as fehler:
            ergebnisse = [("FEHLER", f"Datenbank sagt: {fehler}", "")]
    else:
        cursor.execute("SELECT * FROM posts")
        ergebnisse = cursor.fetchall()
        
    verbindung.close()

    return render_template("index.html", benutzer_suche=suche, posts=ergebnisse)

@app.route("/admin")
def admin():
    # Lücke 3: Broken Access Control
    return render_template("admin.html")

@app.route("/datei")
def datei_lesen():
    # HIER IST LÜCKE 6 (Path Traversal):
    # Wir nehmen den Dateinamen aus der URL und öffnen die Datei blind.
    # Ein Angreifer kann mit "../" aus dem Ordner ausbrechen!
    dateiname = request.args.get("name")
    
    if dateiname:
        try:
            # Wir lesen die Datei ein und schicken sie an den Browser
            with open(dateiname, "r") as datei:
                inhalt = datei.read()
            return f"<h3>Inhalt der Datei:</h3><pre>{inhalt}</pre><br><a href='/'>Zurück</a>"
        except Exception as fehler:
            return f"Fehler: Konnte Datei nicht lesen ({fehler})"
            
    return "Bitte hänge einen Dateinamen an die URL an, z.B. /datei?name=test.txt"

if __name__ == "__main__":
    app.run(debug=True)