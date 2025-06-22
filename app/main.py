from flask import Flask, jsonify, send_from_directory, request, session, redirect, abort, render_template
from functools import wraps
from app import settings
import pathlib
from app import db
import os


#Admin Zugang
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)

#Einstellungen laden
backend = settings.get_settings()["backend"]
app.secret_key = backend["secret_key"]



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

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
@app.route('/admin/<path:filename>')
@admin_required
def serve_admin_only(filename):
    return send_from_directory('templates/admin', filename+'.html')



#API: Alle Tabellen + Inhalte
@app.route('/api/alltables')
@admin_required
def get_tables():
    return db.get_tables()


#API: Alle aktuellen verkaufe
@app.route('/api/todaysSales')
@admin_required
def get_todays_sales():
    return db.get_todays_sales()

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
     
@app.route('/api/settings', methods=['GET'])
@admin_required
def get_settings():
    try:
        current_settings = settings.get_settings()
        return jsonify({"content": current_settings})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/settings', methods=['POST'])
@admin_required
def update_settings():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid settings format"}), 400
    try:
        settings.save_settings(data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#API: Get Database
@app.route('/api/database')
@admin_required
def get_database():
    try:
        db_content = db.serve_db_as_xlsx()
        return db_content
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#--------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == backend["admin_password"]:
            session['admin'] = True
            return redirect('/admin/dashboard')
        return render_template('403.html'), 403
    return render_template('login.html')

# Logout 
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
