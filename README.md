# 📦 Schüler-Firma Lagerverwaltung

Verwalte Verkäufe, Verkäufer und Inventar einfach und sicher über den Browser.

---

## 🚀 Schnellstart

### 1. Initialisierung (empfohlen)

Führe das Setup-Skript aus, um alles automatisch einzurichten:

```powershell
python init.py
```

Das Skript erstellt eine virtuelle Umgebung, installiert Abhängigkeiten und legt die Konfigurationsdatei an.

---

### 2. Manuelle Einrichtung (optional)

#### a) Virtuelle Umgebung erstellen

```powershell
python -m venv venv
```

#### b) Umgebung aktivieren (Windows PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

> Bei Problemen mit der Ausführung:
>
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
>
> Dann erneut aktivieren.

#### c) Abhängigkeiten installieren

```powershell
pip install -r requirements.txt
```

**Benötigte Pakete:**

- `flask` – Webserver
- `gunicorn` – Produktionsserver

#### d) Konfiguration

Die Datei `config/settings.json` wird automatisch durch `init.py` erstellt.  
Du kannst sie nach deinen Bedürfnissen anpassen.

---

### 3. Anwendung starten

```powershell
python run.py
```

Die Web-App ist dann erreichbar unter:

```
http://localhost:5000
```

---

## 🔐 Admin-Zugang

- Das **Admin-Panel** ist über die Web-Oberfläche erreichbar.
- Zugang erfolgt über das Passwort aus der Konfiguration (`admin_password` in `config/settings.json`).

---

## ✅ Funktionen

- Inventar, Verkäufe und Verkäufer einsehen und bearbeiten
- Produkte suchen
- Geschützter Admin-Bereich
- Einstellungen direkt im Browser bearbeiten

---

## 🛠️ Projektstruktur

```
Schueler-Firma/
│
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── routes.py
│   ├── settings.py
│   ├── static/
│   └── templates/
│
├── config/
│   └── settings.json
│
├── venv/
├── requirements.txt
├── run.py
├── init.py
└── README.md
```

---

## 📷 Screenshots

<div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;">

<img src="app/static/screenshots/1.png" alt="Screenshot 1" width="220"/>
<img src="app/static/screenshots/2.png" alt="Screenshot 2" width="220"/>
<img src="app/static/screenshots/3.png" alt="Screenshot 3" width="220"/>
<img src="app/static/screenshots/4.png" alt="Screenshot 4" width="220"/>
<img src="app/static/screenshots/5.png" alt="Screenshot 5" width="220"/>
<img src="app/static/screenshots/6.png" alt="Screenshot 6" width="220"/>
<img src="app/static/screenshots/7.png" alt="Screenshot 7" width="220"/>
<img src="app/static/screenshots/8.png" alt="Screenshot 8" width="220"/>
<img src="app/static/screenshots/9.png" alt="Screenshot 9" width="220"/>
<img src="app/static/screenshots/10.png" alt="Screenshot 10" width="220"/>
<img src="app/static/screenshots/11.png" alt="Screenshot 11" width="220"/>
<img src="app/static/screenshots/12.png" alt="Screenshot 12" width="220"/>
<img src="app/static/screenshots/13.png" alt="Screenshot 13" width="220"/>
<img src="app/static/screenshots/14.png" alt="Screenshot 14" width="220"/>

</div>
