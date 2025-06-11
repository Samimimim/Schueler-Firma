import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import json


#Private Daten holen
# Lade Umgebungsvariablen aus .env-Datei
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")


def warn(produkt):
    with open('./data/email_recivers.json', 'r') as file:
        recivers = json.load(file)

    with smtplib.SMTP("smtp.mail.me.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email_user, email_pass)

        for reciver in recivers:
            msg = EmailMessage()
            msg["From"] = email_user
            msg["To"] = reciver[1]
            msg["Subject"] = f"Warnung: {produkt}"
            msg.set_content(
                f"""Hallo {reciver[0]},
                Das Produkt "{produkt}" hat ein Problem gemeldet,
                was vermutlich einen gerinen Lagerbestand bedeutet. 
                Bitte überprüfe es so schnell wie möglich, z.B. über die Webseite.
                
                Viele Grüße,
                Lagerverwaltungssystem.
                """)

            server.send_message(msg)
