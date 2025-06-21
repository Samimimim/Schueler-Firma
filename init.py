import os
import sys
import subprocess
import json

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
        "admin_password": "passwort",
        "secret_key": "Trallalero Trallala"
    },
    "email_recivers": [
        [
            "Samael",
            "samael.schlecht@messelbergschule.de"
        ],
        [
            "Samael",
            "samaelschlecht@icloud.com"
        ]
    ],
    "email_sender": {
        "password": "dont_you_dare_hack_me",
        "username": "samaelschlecht@icloud.com"
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
 