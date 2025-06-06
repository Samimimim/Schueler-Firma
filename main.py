from flask import Flask, jsonify, send_from_directory, render_template_string, request
import db

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('assets', 'index.html')


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
     


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

