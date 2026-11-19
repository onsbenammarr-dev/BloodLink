import os
from dotenv import load_dotenv

load_dotenv()
p = os.getenv("EMAIL_PASSWORD") or ""
print("adresse :", os.getenv("EMAIL_USER"))
print("longueur :", len(p))
print("espaces :", p.count(" "))
print("lettres et chiffres seulement :", p.isalnum())