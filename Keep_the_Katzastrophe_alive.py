from flask import Flask
from threading import Thread

# Initialisiere die Flask-Anwendung
app = Flask ('')

# Definiere die Route für die Hauptseite
@app.route('/')
def home():
    return "Katzastrophe is running!" # Angezeigte Nachricht bei jedem Ping
    
# Flask-Server starten
def run():
    app.run(host='0.0.0.0', port=8080)
 
# Server im separaten Thread ausführen
def keep_alive():
    t = Thread(target=run)
    t.start()
