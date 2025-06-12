from flask import Flask, jsonify, send_from_directory, render_template_string, request, session, redirect, abort, render_template
from dotenv import load_dotenv
from functools import wraps
import os
from app import db

#Admin Zugang
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# Lade Umgebungsvariablen aus .env-Datei
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)


app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY","23456%$§WSDFG&54edfghjuzTRFG")




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')


@app.route('/login')
def login_site():
    return render_template('login.html')

#Admin stuff
@app.route('/admin-only/<path:filename>')
@admin_required
def serve_admin_only(filename):
    return send_from_directory('admin-only', filename+'.html')



#API: Alle Tabellen + Inhalte
@app.route('/api/alltables')
@admin_required
def get_tables():
    return db.get_tables()


#Neue Produkt hinzufügen
@app.route('/api/addProdukt', methods=['POST'])
@admin_required
def add_produkt():
    data = request.json
    return db.add_produkt(data)

    

#Neue Transaktion hinzufügen
@app.route('/addTransaktion', methods=['POST'])
@admin_required
def add_transaktion():
    data = request.json
    return db.add_transaktion(data)

    


@app.route("/api/SearchItem", methods=["GET"])
@admin_required
def get_item():
    item_id = request.args.get("id")
    name = request.args.get("name")
    return db.get_item(item_id, name)
     
#--------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.getenv("ADMIN_PASS","Schule10"):
            session['admin'] = True
            return redirect('/admin-only/admin')
        return 'Falsches Passwort', 403
    return render_template('login.html')

# Logout (optional)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

