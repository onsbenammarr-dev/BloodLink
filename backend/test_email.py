"""Diagnostic e-mail. Usage : python test_email.py ton.adresse@gmail.com"""
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

host = os.getenv("EMAIL_HOST")
user = os.getenv("EMAIL_USER")
mdp = os.getenv("EMAIL_PASSWORD") or ""
expediteur = os.getenv("EMAIL_FROM") or user
destinataire = sys.argv[1] if len(sys.argv) > 1 else user

print(f"Serveur : {host} | utilisateur : {user!r} | mot de passe : {len(mdp)} caractères")
if not host or not user or not mdp:
    print("EMAIL_HOST, EMAIL_USER ou EMAIL_PASSWORD est manquant dans backend\\.env")
    sys.exit(1)
if " " in mdp or mdp[0] in "\"'":
    print("ATTENTION : le mot de passe contient des espaces ou des guillemets. Retire-les dans .env.")


def message():
    m = EmailMessage()
    m["Subject"] = "Test BloodLink"
    m["From"] = expediteur
    m["To"] = destinataire
    m.set_content("Si vous lisez ceci, l'envoi d'e-mails fonctionne.")
    return m


def essayer(nom, ouvrir):
    print(f"\n--- {nom} ---")
    try:
        s = ouvrir()
        s.login(user, mdp)
        s.send_message(message())
        s.quit()
        print("OK : e-mail envoyé à", destinataire)
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"Échec d'authentification ({e.smtp_code}) : identifiant ou mot de passe d'application incorrect.")
    except smtplib.SMTPServerDisconnected as e:
        print("Connexion coupée par le serveur : antivirus, réseau ou blocage du fournisseur.", e)
    except (OSError, smtplib.SMTPException) as e:
        print("Échec :", type(e).__name__, e)
    return False


def starttls():
    s = smtplib.SMTP(host, 587, timeout=20)
    s.ehlo()
    s.starttls()
    s.ehlo()
    return s


def ssl():
    return smtplib.SMTP_SSL(host, 465, timeout=20)


ok = essayer("Port 587 (STARTTLS)", starttls) or essayer("Port 465 (SSL)", ssl)
sys.exit(0 if ok else 1)