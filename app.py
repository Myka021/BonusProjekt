from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    suche = request.args.get("suchbegriff")
    ergebnisse = [] #hier speichern wir die gefundenen beiträge

    if suche:
        #wir öffnen die verbindung zur db
        verbindung = sqlite3.connect('database.db')
        cursor = verbindung.cursor()

        #hier ist die lücke (sql-injection)
        #wir kleben den suchbegriff ungeprüft direkt in den sql-befehl
        sqlBefehl = f"SELECT * FROM posts WHERE title LIKE '%{suche}%'"

        #wir führen den befehl aus und holen alle ergebnisse
        #wenn der befehl fehlschlägt fangen wir den fehler ab damit der server nicht abstürtzt
        try:
            cursor.execute(sqlBefehl)
            ergebnisse = cursor.fetchall()
        except sqlite3.Error as fehler:
            #somit verrät uns die die webseite den db fehler
            ergebnisse = [("FEHLER", f"datenbank sagt: {fehler}", "")]

        verbindung.close()

    #wir geben das gesucht wort und die gefundenen beiträge an html weiter
    return render_template("index.html", benutzer_suche = suche, posts = ergebnisse)
    
@app.route("/admin")
def admin():
    # HIER IST DIE 3. LÜCKE (Broken Access Control):
    # Ein sicherer Code würde hier prüfen: "Ist der User eingeloggt? Hat er das Passwort?"
    # Wir machen das absichtlich NICHT. Wir lassen jeden rein, der die Adresse kennt!
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
    #damit wenn bei codefehler das programm nichrt abstürtzt sondern uns sagt wo der fehler liegt
