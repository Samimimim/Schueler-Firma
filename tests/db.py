from flask import jsonify
import sqlite3
import datetime
from contextlib import contextmanager
import io
import xlsxwriter
from flask import send_file
import random

DB_PATH = "../db/schüler-firma.db"
critical_quantity = 5  # Kritische Menge für Warnung
@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()



def get_item_json(item_id=None, name=None):
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
            return dict(item)
        return {"error": "Item nicht gefunden"}

