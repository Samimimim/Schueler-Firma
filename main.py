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
#Neue Produkt hinzufügen
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

#Neue Transaktion hinzufügen
@app.route('/addTransaktion', methods=['POST'])
def add_transaktion():
    import datetime
    data = request.json

    input_objekt = data.get('objekt_name')  # kann Name (str) oder ID (int) sein
    anzahl = data.get('anzahl')
    preis_pro_stueck = data.get('preis_pro_stueck')
    datum = data.get('datum')
    beschreibung = data.get('beschreibung', '')
    seller1_id = data.get('seller1_id')
    seller2_id = data.get('seller2_id')

    if input_objekt is None or anzahl is None or not isinstance(anzahl, int):
        return jsonify({'error': 'Ungültige Eingabedaten'}), 400

    try:
        with sqlite3.connect("./db/schüler-firma.db") as conn:
            cursor = conn.cursor()

            # Objekt-ID ermitteln (egal ob Name oder ID übergeben wurde)
            if isinstance(input_objekt, int) or (isinstance(input_objekt, str) and input_objekt.isdigit()):
                objekt_id = int(input_objekt)
                cursor.execute("SELECT price FROM inventar WHERE id = ?", (objekt_id,))
                row = cursor.fetchone()
                if not row:
                    return jsonify({'error': f'Kein Inventar-Eintrag mit ID {objekt_id} gefunden'}), 400
                db_preis = row[0]
            else:
                cursor.execute("SELECT id, price FROM inventar WHERE name = ?", (input_objekt,))
                row = cursor.fetchone()
                if not row:
                    return jsonify({'error': f'Kein Inventar-Eintrag mit Name "{input_objekt}" gefunden'}), 400
                objekt_id = row[0]
                db_preis = row[1]

            # Falls Preis nicht gesetzt oder 0: Preis aus DB verwenden
            if preis_pro_stueck in (None, '', 0):
                preis_pro_stueck = db_preis

            # Datum auf heute setzen, falls leer
            if not datum:
                datum = datetime.date.today().isoformat()

            # Seller1 prüfen
            if seller1_id is not None:
                cursor.execute("SELECT 1 FROM verkaeufer WHERE id = ?", (seller1_id,))
                if not cursor.fetchone():
                    return jsonify({'error': f'Seller1 mit ID {seller1_id} nicht gefunden'}), 400
            else:
                seller1_id = None

            # Seller2 prüfen
            if seller2_id is not None:
                cursor.execute("SELECT 1 FROM verkaeufer WHERE id = ?", (seller2_id,))
                if not cursor.fetchone():
                    return jsonify({'error': f'Seller2 mit ID {seller2_id} nicht gefunden'}), 400
            else:
                seller2_id = None

            # In DB schreiben (jetzt mit objekt_id, NICHT objektname)
            cursor.execute("""
                INSERT INTO verkaeufe (objekt_id, anzahl, preisPerPiece, date, description, seller1_id, seller2_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (objekt_id, anzahl, preis_pro_stueck, datum, beschreibung, seller1_id, seller2_id))
            conn.commit()

            return jsonify({'success': True, 'id': cursor.lastrowid}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

