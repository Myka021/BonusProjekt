from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# NEU: Wir erlauben jetzt GET (Suchen/Anzeigen) und POST (Daten empfangen)
@app.route("/", methods=["GET", "POST"])
def home():
    verbindung = sqlite3.connect('database.db')
    cursor = verbindung.cursor()
    
    # NEU: Wenn ein neuer Beitrag gesendet wurde, speichern wir ihn direkt und ungeprüft ab
    if request.method == "POST":
        neuer_titel = request.form.get("titel")
        neuer_inhalt = request.form.get("inhalt")
        
        cursor.execute(f"INSERT INTO posts (title, content) VALUES ('{neuer_titel}', '{neuer_inhalt}')")
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
        # Wenn nicht gesucht wird, zeigen wir einfach alle Beiträge an
        cursor.execute("SELECT * FROM posts")
        ergebnisse = cursor.fetchall()
        
    verbindung.close()

    return render_template("index.html", benutzer_suche=suche, posts=ergebnisse)

@app.route("/admin")
def admin():
    # Lücke 3: Broken Access Control
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)