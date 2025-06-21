import smtplib
from email.message import EmailMessage
import os
import json
import settings

message =  """Hallo {name},

das Produkt "{produkt}" hat ein Problem gemeldet,  
vermutlich handelt es sich um einen geringen Lagerbestand.  
Bitte überprüfe dies so schnell wie möglich, z. B. über unsere Webseite.

Viele Grüße  
Dein Lagerverwaltungssystem
"""

settings = settings.get_settings()
email_sender = settings["email_sender"]
email_recivers = settings["email_recivers"]



def warn(produkt):
    if not email_sender["username"] or not email_sender["password"]:
        print("Email user or password not set in the setttings.")
        return

    with smtplib.SMTP("smtp.mail.me.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email_sender["username"], email_sender["password"])

        for reciver in email_recivers:
            msg = EmailMessage()
            msg["From"] = email_sender["username"]
            msg["To"] = reciver[1]
            msg["Subject"] = f"Warnung: {produkt}"
            msg.set_content(message.format(name=reciver[0], produkt=produkt))

            server.send_message(msg)
