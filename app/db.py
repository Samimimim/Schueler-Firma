from flask import jsonify
import sqlite3
import datetime
from contextlib import contextmanager
import send  

DB_PATH = "./db/schüler-firma.db"
critical_quantity = 5  # Kritische Menge für Warnung

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def get_tables():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row["name"] for row in cur.fetchall()]
        all_data = {}
        for table in tables:
            try:
                cur.execute(f"SELECT * FROM {table}")
                rows = [dict(row) for row in cur.fetchall()]
                all_data[table] = rows
            except Exception:
                all_data[table] = "Fehler beim Abrufen"
        return jsonify(all_data)

def add_produkt(data):
    name = data.get('name')
    stueckzahl = data.get('stueckzahl')
    beschreibung = data.get('beschreibung', '')
    preis = data.get('preis')

    if not name or not isinstance(stueckzahl, int) :
        return jsonify({'error': 'Ungültige Eingabedaten'}), 400

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT stueckzahl FROM inventar WHERE name = ?", (name,))
            result = cursor.fetchone()
            if result:
                neue_stueckzahl = result[0] + stueckzahl
                cursor.execute(
                    "UPDATE inventar SET stueckzahl = ? WHERE name = ?",
                    (neue_stueckzahl, name)
                )
            else:
                cursor.execute(
                    "INSERT INTO inventar (name, stueckzahl, beschreibung, preis) VALUES (?, ?, ?, ?)",
                    (name, stueckzahl, beschreibung, preis)
                )
            conn.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def check_seller(cursor, seller_id, label):
    if seller_id is not None:
        cursor.execute("SELECT 1 FROM verkaeufer WHERE id = ?", (seller_id,))
        if not cursor.fetchone():
            raise ValueError(f'{label} mit ID {seller_id} nicht gefunden')
    return seller_id

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
        with get_db() as conn:
            cursor = conn.cursor()
            # Objekt-ID und Preis ermitteln
            if isinstance(input_objekt, int) or (isinstance(input_objekt, str) and str(input_objekt).isdigit()):
                objekt_id = int(input_objekt)
                cursor.execute("SELECT preis, stueckzahl, name FROM inventar WHERE id = ?", (objekt_id,))
                row = cursor.fetchone()
                if not row:
                    return jsonify({'error': f'Kein Inventar-Eintrag mit ID {objekt_id} gefunden'}), 400
                db_preis, aktuelle_stueckzahl, produkt_name = row
            else:
                cursor.execute("SELECT id, preis, stueckzahl, name FROM inventar WHERE name = ?", (input_objekt,))
                row = cursor.fetchone()
                if not row:
                    return jsonify({'error': f'Kein Inventar-Eintrag mit Name \"{input_objekt}\" gefunden'}), 400
                objekt_id, db_preis, aktuelle_stueckzahl, produkt_name = row

            if not preis_pro_stueck:
                preis_pro_stueck = db_preis

            # Verkäufer prüfen
            try:
                seller1_id = check_seller(cursor, seller1_id, "Seller1")
                seller2_id = check_seller(cursor, seller2_id, "Seller2")
            except ValueError as ve:
                return jsonify({'error': str(ve)}), 400

            # Stückzahl updaten
            if aktuelle_stueckzahl is None or aktuelle_stueckzahl < anzahl:
                return jsonify({'error': 'Nicht genügend Stück auf Lager'}), 400
            neue_stueckzahl = aktuelle_stueckzahl - anzahl
            cursor.execute(
                "UPDATE inventar SET stueckzahl = ? WHERE id = ?",
                (neue_stueckzahl, objekt_id)
            )

            # Eintrag speichern
            cursor.execute("""
                INSERT INTO verkaeufe (objekt_id, anzahl, preisPerPiece, date, description, seller1_id, seller2_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (objekt_id, anzahl, preis_pro_stueck, datum, beschreibung, seller1_id, seller2_id))
            conn.commit()

            # Nach Verkauf: Prüfen ob Bestand kritisch und ggf. Mail senden
            try:
                if check_critical_quantity(produkt_name):
                    send.warn(produkt_name)
            except Exception as e:
                print(f"Fehler beim Senden der kritischen Bestandsmail: {e}")

            return jsonify({'success': True, 'id': cursor.lastrowid}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_item(item_id=None, name=None):
    with get_db() as conn:
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

def get_quantity(produkt):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT stueckzahl FROM inventar WHERE name = ?", (produkt,))
        row = cursor.fetchone()
        return row[0] if row else 0

def check_critical_quantity(produkt):
    return get_quantity(produkt) <= critical_quantity