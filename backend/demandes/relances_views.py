from functools import lru_cache

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from etablissements.permissions import IsEtablissement

from .sante import INTERVALLE_DONS_JOURS


@lru_cache(maxsize=1)
def _charger():
    from ml.retour_donneur import charger
    return charger()


class DonneursARelancerView(APIView):
    permission_classes = [IsEtablissement]

    def get(self, request):
        try:
            modele, metriques = _charger()
        except FileNotFoundError:
            return Response({"detail": "Le modèle n'est pas encore entraîné."}, status=503)
        from ml.retour_donneur import probabilite

        e = request.user.etablissement
        now = timezone.now()
        par_donneur = {}
        for don in e.dons.select_related("donneur").order_by("date"):
            par_donneur.setdefault(don.donneur, []).append(don.date)

        lignes = []
        for donneur, dates in par_donneur.items():
            profil = getattr(donneur, "profil_donneur", None)
            dernier, premier = dates[-1], dates[0]
            mois_dernier = (now - dernier).days / 30.44
            mois_premier = (now - premier).days / 30.44
            lignes.append({
                "email": donneur.email,
                "groupe_sanguin": profil.groupe_sanguin if profil else "-",
                "nb_dons": len(dates),
                "dernier_don": dernier,
                "eligible": (now - dernier).days >= INTERVALLE_DONS_JOURS,
                "probabilite": round(probabilite(modele, mois_dernier, len(dates), mois_premier), 3),
            })
        lignes.sort(key=lambda l: (l["eligible"], l["probabilite"]), reverse=True)
        return Response({**metriques, "donneurs": lignes})