# 📦 Web-App zur Lagersverwaltung

Verwalte Verkäufe, Verkäufer und Inventar einfach über den Browser. Ideal für Schülerfirmen, kleine Betriebe oder private Projekte.

---

## 🚀 Schnellstart

### 1. Virtuelle Umgebung erstellen

```powershell
python -m venv venv
```

### 2. Umgebung aktivieren (Windows PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

❗ Bei Problemen mit der Ausführung:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Dann erneut aktivieren:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Abhängigkeiten installieren

```powershell
pip install -r requirements.txt
```

**Benötigte Pakete:**
- `flask` – Webserver
- `python-dotenv` – Laden von Umgebungsvariablen aus `.env`

---

### 4. `.env`-Datei erstellen

Erstelle im Hauptverzeichnis eine Datei namens `.env` mit folgendem Inhalt:

```env
EMAIL_USER=dein.email@example.com     # Optional
EMAIL_PASS=deinEmailPasswort          # Optional
SECRET_KEY=ein_sicherer_schlüssel     # Pflicht
ADMIN_PASS=adminPasswort              # Pflicht (für Admin-Login)
```

---

### 5. Anwendung starten

```powershell
python main.py
```

Ein lokaler **Flask-Server** wird gestartet. Die Web-App ist dann erreichbar unter:

```
http://localhost:5000
```

---

## 🔐 Admin-Zugang

- Das **Admin-Panel** ist über die Web-Oberfläche erreichbar.
- Den Knopf **Admin werden doppelt drücken**
- Zugang erfolgt über das Passwort in der `.env`-Datei (`ADMIN_PASS`).

---

## ✅ Funktionen

- Inventar, Verkaufe, Verkaufer einsehen und teilweise bearbeiten
- Produkte suchen
- Teilweise geschützter admin Bereich

## 📷Screenshots

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
<img src="app/static/screenshots/11.png" alt="Screenshot 10" width="220"/>

</div>
