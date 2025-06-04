from flask import Flask, jsonify, send_from_directory, render_template_string, request

import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('assets', 'index.html')


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

#API: Alle Tabellen + Inhalte
@app.route('/api/alltables')
def get_all_tables():
    conn = sqlite3.connect('./db/schüler-firma.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row["name"] for row in cur.fetchall()]

    all_data = {}
    for table in tables:
        try:
            cur.execute(f"SELECT * FROM {table}")
            rows = [dict(row) for row in cur.fetchall()]
            all_data[table] = rows
        except:
            all_data[table] = "Fehler beim Abrufen"

    conn.close()
    return jsonify(all_data)

@app.route('/api/addProdukt', methods=['POST'])
def add_produkt():
    data = request.json
    name = data.get('name')
    stueckzahl = data.get('stueckzahl')
    beschreibung = data.get('beschreibung', '')

    if not name or not isinstance(stueckzahl, int):
        return jsonify({'error': 'Ungültige Eingabedaten'}), 400

    try:
        with sqlite3.connect("./db/schüler-firma.db") as conn:
            cursor = conn.cursor()
            # Prüfen, ob Produkt schon existiert
            cursor.execute("SELECT stueckzahl FROM inventar WHERE name = ?", (name,))
            result = cursor.fetchone()

            if result:
                # Produkt existiert -> Stückzahl erhöhen
                neue_stueckzahl = result[0] + stueckzahl
                cursor.execute(
                    "UPDATE inventar SET stueckzahl = ? WHERE name = ?",
                    (neue_stueckzahl, name)
                )
            else:
                # Produkt existiert nicht -> neu einfügen
                cursor.execute(
                    "INSERT INTO inventar (name, stueckzahl, beschreibung) VALUES (?, ?, ?)",
                    (name, stueckzahl, beschreibung)
                )

            conn.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

