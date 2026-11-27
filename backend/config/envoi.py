"""Envoi des e-mails.

Si BREVO_API_KEY est défini dans .env, l'envoi passe par l'API Brevo (HTTPS, port 443),
ce qui fonctionne même quand le réseau bloque le SMTP. Sinon, le mailer de Django est
utilisé (SMTP si EMAIL_HOST est défini, sinon affichage dans le terminal).
"""
import base64
import json
import os
import threading
import urllib.error
import urllib.request
from email.utils import parseaddr

from django.conf import settings


def _par_brevo(message, cle):
    brut = os.getenv("EMAIL_FROM") or message.from_email or settings.DEFAULT_FROM_EMAIL
    adresse = parseaddr(brut)[1]
    charge = {
        "sender": {"name": "BloodLink", "email": adresse},
        "to": [{"email": a} for a in message.to],
        "subject": message.subject,
        "textContent": message.body,
    }
    pieces = []
    for p in message.attachments:
        if isinstance(p, tuple):
            contenu = p[1].encode("utf-8") if isinstance(p[1], str) else p[1]
            pieces.append({"name": p[0], "content": base64.b64encode(contenu).decode()})
    if pieces:
        charge["attachment"] = pieces
    requete = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps(charge).encode("utf-8"),
        headers={
            "api-key": cle,
            "content-type": "application/json",
            "accept": "application/json",
            "user-agent": "BloodLink/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(requete, timeout=30) as reponse:
        reponse.read()


def envoyer(message):
    cle = os.getenv("BREVO_API_KEY")
    try:
        if cle:
            _par_brevo(message, cle)
        else:
            message.send()
    except urllib.error.HTTPError as e:
        print("Erreur envoi e-mail (Brevo) :", e.code, e.read().decode("utf-8", "ignore")[:300])
    except Exception as e:
        print("Erreur envoi e-mail :", e)
    else:
        print("E-mail envoyé à", ", ".join(message.to))


def lancer(messages):
    """Envoie les messages en arrière-plan, sans faire attendre l'utilisateur."""
    if messages:
        threading.Thread(
            target=lambda: [envoyer(m) for m in messages], daemon=True
        ).start()