from datetime import timedelta
from functools import lru_cache

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from etablissements.permissions import IsEtablissement


@lru_cache(maxsize=1)
def _charger():
    from ml.prevision import charger
    return charger()


class PrevisionView(APIView):
    permission_classes = [IsEtablissement]

    def get(self, request):
        try:
            modele, metriques, historique, contexte = _charger()
        except FileNotFoundError:
            return Response(
                {"detail": "Le modèle de prévision n'est pas encore entraîné."}, status=503
            )
        from ml.prevision import GROUPES, prevoir

        premier = timezone.localdate() + timedelta(days=1)
        groupes = prevoir(modele, historique, premier, 7)
        jours = [(premier + timedelta(days=k)).isoformat() for k in range(7)]
        total = [round(sum(groupes[g][k] for g in GROUPES), 1) for k in range(7)]
        return Response({
            **metriques,
            "jours": jours,
            "groupes": groupes,
            "total": total,
            "historique": contexte,
        })