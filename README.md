#


# Projektstart

## 1. Virtuelle Umgebung erstellen

```powershell
python -m venv venv
```

## 2. Umgebung aktivieren (Windows PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

### ❗ Bei Fehler:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Dann erneut aktivieren:

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Abhängigkeiten installieren

```powershell
pip install -r requirements.txt
```

## 4. Anwendung starten

```powershell
python main.py
```
## 5. .env Datei erstellen
Erstelle eine .env Datei mit:
EMAIL_USER (Optional)
EMAIL_PASS (OPtional)
SECRET_KEY (Sicherer Schlüssel)
ADMIN_PASS (Passwort für das Admin Panal)