from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from config.envoi import lancer

from .qr import image_qr, reference


def _formater(dt):
    d = timezone.localtime(dt)
    return f"{d:%d/%m/%Y} à {d:%H:%M}"


def envoyer_alertes(demande, profils):
    lien = f"{settings.FRONTEND_URL}/espace-donneur"
    if demande.date_don:
        quand = _formater(demande.date_don)
    else:
        quand = f"dans les {demande.delai_heures} heures"
    sujet = f"Urgent : besoin de sang {demande.groupe_sanguin} à {demande.ville}"
    corps = (
        f"Bonjour,\n\n"
        f"{demande.etablissement.nom} ({demande.ville}) a besoin de {demande.quantite} "
        f"poche(s) de sang {demande.groupe_sanguin}.\n"
        f"Don souhaité : {quand}.\n\n"
        f"Répondez et réservez votre créneau : {lien}\n\n"
        f"Merci pour votre générosité.\nL'équipe BloodLink"
    )
    lancer([EmailMessage(sujet, corps, to=[p.user.email]) for p in profils])


def envoyer_confirmation(rdv):
    nom = rdv.donneur.get_full_name() or rdv.donneur.email
    corps = (
        f"Bonjour {nom},\n\n"
        f"Votre rendez-vous de don à {rdv.etablissement.nom} est confirmé "
        f"pour le {_formater(rdv.date_heure)}.\n\n"
        f"Présentez le code QR joint à ce message à votre arrivée. Il contient vos "
        f"informations de donneur (nom, groupe sanguin, coordonnées) et la référence "
        f"{reference(rdv)}.\n\n"
        f"Merci !\nL'équipe BloodLink"
    )
    message = EmailMessage(
        "Rendez-vous de don confirmé : votre code QR", corps, to=[rdv.donneur.email]
    )
    message.attach("code-qr-bloodlink.png", image_qr(rdv), "image/png")
    lancer([message])