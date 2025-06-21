from flask import Flask, jsonify, send_from_directory, request, session, redirect, abort, render_template
from functools import wraps
import settings
import pathlib
import db
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
    settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"data", 'settings.json')
    try:
        with open(settings_path, 'r') as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/settings', methods=['POST'])
@admin_required
def update_settings():
    settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"data", 'settings.json')
    data = request.json
    content = data.get("content")
    if not isinstance(content, str):
        return jsonify({"error": "No content provided"}), 400
    try:
        # Optional: Backup der alten Datei
        backup_path = settings_path + ".bak"
        if os.path.exists(backup_path):
            os.remove(backup_path)
        pathlib.Path(settings_path).rename(backup_path)
        with open(settings_path, 'w') as f:
            f.write(content)
        return jsonify({"success": True})
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
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

