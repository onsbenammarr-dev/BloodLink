from django.conf import settings
from django.core.mail import EmailMessage

from config.envoi import lancer


def envoyer_decision(etab):
    """Prévient l'établissement que son inscription est validée ou refusée."""
    if etab.statut_validation == "valide":
        sujet = "Votre établissement a été validé sur BloodLink"
        corps = (
            "Bonjour,\n\n"
            f"Bonne nouvelle : l'inscription de {etab.nom} sur BloodLink a été validée "
            "par l'administrateur.\n\n"
            "Vous pouvez dès maintenant vous connecter et publier vos demandes de sang :\n"
            f"{settings.FRONTEND_URL}/login\n\n"
            "L'équipe BloodLink"
        )
    elif etab.statut_validation == "refuse":
        sujet = "Votre inscription sur BloodLink n'a pas été acceptée"
        motif = f"Motif : {etab.motif_refus}\n\n" if etab.motif_refus else ""
        corps = (
            "Bonjour,\n\n"
            f"Après examen, l'inscription de {etab.nom} sur BloodLink n'a pas pu être acceptée.\n\n"
            f"{motif}"
            "Pour toute question, répondez à ce message.\n\n"
            "L'équipe BloodLink"
        )
    else:
        return

    lancer([EmailMessage(sujet, corps, to=[etab.user.email])])