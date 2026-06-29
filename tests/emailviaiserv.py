import smtplib
from email.message import EmailMessage

# ==========================
# Konfiguration (Platzhalter)
# ==========================
SMTP_SERVER = "messelbergschule.de"
SMTP_PORT = 587  # Häufig 587 für STARTTLS oder 465 für SSL

USERNAME = "schuelerfirma"
PASSWORD = "luissoeinehrenman"

ABSENDER = "noreply@messelbergschule.de"
EMPFÄNGER = "samael.schlecht@messelbergschule.de"

BETREFF = "Test-E-Mail"
NACHRICHT = """
Hallo,

dies ist eine Test-E-Mail aus Python.

Viele Grüße
Max Mustermann
"""

# ==========================
# E-Mail erstellen
# ==========================
email = EmailMessage()
email["From"] = ABSENDER
email["To"] = EMPFÄNGER
email["Subject"] = BETREFF
email.set_content(NACHRICHT)

# ==========================
# Verbindung aufbauen
# ==========================
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Verschlüsselung aktivieren
        server.login(USERNAME, PASSWORD)
        server.send_message(email)

    print("E-Mail erfolgreich versendet!")

except Exception as e:
    print(f"Fehler beim Versand: {e}")