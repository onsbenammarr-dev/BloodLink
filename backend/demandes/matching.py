from donneurs.models import ProfilDonneur
from .constants import COMPATIBLES


def donneurs_compatibles(demande):
    return list(
        ProfilDonneur.objects.filter(
            groupe_sanguin__in=COMPATIBLES[demande.groupe_sanguin],
            ville__iexact=demande.ville,
            disponible=True,
            user__is_active=True,
        ).select_related("user")
    )