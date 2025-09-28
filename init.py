import os
import sys
import subprocess
import json
import sqlite3

# Create venv directory
venv_dir = "venv"
if not os.path.exists(venv_dir):
    subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
    print(f"Virtual environment created at ./{venv_dir}")
else:
    print(f"Virtual environment already exists at ./{venv_dir}")

# Install requirements.txt
pip_path = os.path.join(venv_dir, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(venv_dir, "bin", "pip")
requirements_file = "requirements.txt"
if os.path.exists(requirements_file):
    subprocess.check_call([pip_path, "install", "-r", requirements_file])
    print(f"Requirements from {requirements_file} installed.")
else:
    print(f"{requirements_file} not found, skipping requirements installation.")

# Create settings.json config file
config ={
    "backend": {
        "admin_password": "[PASSWORD]",
        "secret_key": "[SECRET_KEY]"
    },
    "email_recivers": [
        [
            "RECIPIENT1_NAME",
            "RECIPIENT2_EMAIL"
        ],
        [
            "[RECIPIENT2_NAME]",
            "[RECIPIENT2_EMAIL]"
        ]
    ],
    "email_sender": {
        "password": "[YOUR_PASSWORD]",
        "username": "[YOUR_EMAIL]"
    },
    "settings": {
        "display": {
            "fontSize": 14
        },
        "theme": "dark"
    },
    "version": "1"
}

config_path = "./config/settings.json"
os.makedirs(os.path.dirname(config_path), exist_ok=True)
with open(config_path, "w") as f:
    json.dump(config, f, indent=4)
    print(f"Config file created at ./{config_path}")

#Creating Database
db_path = "./db/database.db"
con = sqlite3.connect(db_path)

cur = con.cursor()

cur.executescript("""
CREATE TABLE verkaeufer (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE verkaeufe (
    id INTEGER PRIMARY KEY,
    objekt_id INTEGER,
    anzahl INTEGER,
    "preisPerPiece" REAL,
    "date" TEXT,
    "description" TEXT,
 
    seller1_id INTEGER,
    seller2_id INTEGER,
    FOREIGN KEY (objekt_id) REFERENCES inventar(id),
 
    FOREIGN KEY (seller1_id) REFERENCES verkaeufer(id),
    FOREIGN KEY (seller2_id) REFERENCES verkaeufer(id)
);
CREATE TABLE inventar (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    stueckzahl INTEGER NOT NULL,
    beschreibung TEXT
, "preis" REAL);
""")
con.commit()
con.close()
print("""
      -------------------------------------------------
      | Database created at ./{db_path}|
      -------------------------------------------------
      """)