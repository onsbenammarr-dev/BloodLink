"""Code QR remis au donneur après la confirmation de son rendez-vous."""
import hashlib
import hmac
import io

import segno
from django.conf import settings
from django.utils import timezone


def reference(rdv):
    """Référence signée : permet de vérifier que le code a bien été émis par BloodLink."""
    msg = f"{rdv.id}:{rdv.donneur_id}:{rdv.date_heure.isoformat()}".encode()
    signature = hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).hexdigest()
    return f"BL-{rdv.id}-{signature[:8].upper()}"


def contenu_qr(rdv):
    d = rdv.donneur
    profil = getattr(d, "profil_donneur", None)
    quand = timezone.localtime(rdv.date_heure)
    lignes = [
        "BLOODLINK - Rendez-vous de don",
        f"Donneur : {d.get_full_name() or d.email}",
        f"Groupe sanguin : {profil.groupe_sanguin if profil else '-'}",
    ]
    if profil and getattr(profil, "telephone", ""):
        lignes.append(f"Telephone : {profil.telephone}")
    lignes.append(f"E-mail : {d.email}")
    if profil:
        lignes.append(f"Ville : {profil.ville}")
    lignes += [
        f"Etablissement : {rdv.etablissement.nom}",
        f"Rendez-vous : {quand:%d/%m/%Y} a {quand:%H:%M}",
        f"Ref : {reference(rdv)}",
    ]
    return "\n".join(lignes)


def image_qr(rdv):
    tampon = io.BytesIO()
    segno.make(contenu_qr(rdv), error="m", encoding="utf-8").save(
        tampon, kind="png", scale=8, border=3
    )
    return tampon.getvalue()