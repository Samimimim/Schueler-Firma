from flask import Flask, jsonify, send_from_directory, render_template_string, request, session, redirect, abort, render_template
from dotenv import load_dotenv
import os
import db

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()


app = Flask(__name__, template_folder='assets/templates')
app.secret_key = os.getenv("SECRET_KEY")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

#API: Alle Tabellen + Inhalte
@app.route('/api/alltables')
def get_tables():
    return db.get_tables()


#Neue Produkt hinzufügen
@app.route('/api/addProdukt', methods=['POST'])
def add_produkt():
    data = request.json
    return db.add_produkt(data)

    

#Neue Transaktion hinzufügen
@app.route('/addTransaktion', methods=['POST'])
def add_transaktion():
    data = request.json
    return db.add_transaktion(data)

    


@app.route("/api/SearchItem", methods=["GET"])
def get_item():
    item_id = request.args.get("id")
    name = request.args.get("name")
    return db.get_item(item_id, name)
     
#--------------
@app.route('/login')
def login():
    if request.args.get('auth') == os.getenv("ADMIN_PASS"):
        session['user'] = 'admin'
        return redirect('/admin')
    return 'Falscher Code', 403

# Adminseite
@app.route('/admin')
def admin():
    if session.get('user') == 'admin':
        return render_template('admin.html')
    return abort(403)

# Logout (optional)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

