import smtplib
from email.message import EmailMessage

# E-Mail-Daten
absender = "_________@icloud.com"
empfänger = "samael.schlecht@messelbergschule.de"
betreff = "lol"
inhalt = """
lol
"""

# Nachricht erstellen
msg = EmailMessage()
msg["From"] = absender
msg["To"] = empfänger
msg["Subject"] = betreff
msg.set_content(inhalt)

# Verbindung zu iCloud SMTP
with smtplib.SMTP("smtp.mail.me.com", 587) as server:
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(absender, "ts______")
    server.send_message(msg)


print("E-Mail gesendet!")
