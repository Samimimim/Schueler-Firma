from flask import jsonify
import sqlite3
import datetime

def get_tables():
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

#------------------------
def add_produkt(data):
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

#------------------------------
def add_transaktion(data):
    input_objekt = data.get('objekt_name')
    anzahl = data.get('anzahl')
    preis_pro_stueck = data.get('preis_pro_stueck')
    datum = data.get('datum') or datetime.date.today().isoformat()
    beschreibung = data.get('beschreibung', '')
    seller1_id = data.get('seller1_id')
    seller2_id = data.get('seller2_id')

    if not input_objekt or not isinstance(anzahl, int):
        return jsonify({'error': 'Ungültige Eingabedaten'}), 400

    try:
        with sqlite3.connect("./db/schüler-firma.db") as conn:
            cursor = conn.cursor()

            # Objekt-ID und Preis ermitteln
            objekt_id, db_preis = None, None
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
                    return jsonify({'error': f'Kein Inventar-Eintrag mit Name \"{input_objekt}\" gefunden'}), 400
                objekt_id, db_preis = row

            # Preis ggf. aus DB übernehmen
            if not preis_pro_stueck:
                preis_pro_stueck = db_preis

            # Verkäufer prüfen (None zulassen)
            def check_seller(seller_id, label):
                if seller_id is not None:
                    cursor.execute("SELECT 1 FROM verkaeufer WHERE id = ?", (seller_id,))
                    if not cursor.fetchone():
                        raise ValueError(f'{label} mit ID {seller_id} nicht gefunden')
                return seller_id

            try:
                seller1_id = check_seller(seller1_id, "Seller1")
                seller2_id = check_seller(seller2_id, "Seller2")
            except ValueError as ve:
                return jsonify({'error': str(ve)}), 400

            # Eintrag speichern
            cursor.execute("""
                INSERT INTO verkaeufe (objekt_id, anzahl, preisPerPiece, date, description, seller1_id, seller2_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (objekt_id, anzahl, preis_pro_stueck, datum, beschreibung, seller1_id, seller2_id))
            conn.commit()

            return jsonify({'success': True, 'id': cursor.lastrowid}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-------------------------
def get_item(item_id, name):
    with sqlite3.connect("./db/schüler-firma.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        

        if item_id:
            cursor.execute("SELECT * FROM inventar WHERE id = ?", (item_id,))
        elif name:
            cursor.execute("SELECT * FROM inventar WHERE name = ?", (name,))
        else:
            return jsonify({"error": "Bitte 'id' oder 'name' angeben."}), 400

        item = cursor.fetchone()

        if item:
            return jsonify(dict(item))
        return jsonify({"error": "Item nicht gefunden"}), 404