from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .qr import image_qr, reference
import hmac
import re
from donneurs.models import Reponse
from etablissements.permissions import IsEtablissement, IsEtablissementValide
from django.http import HttpResponse
from .emails import envoyer_alertes, envoyer_confirmation
from .matching import donneurs_compatibles
from .models import DemandeSang, Don, RendezVous
from .sante import evaluer
from .serializers import (
    DemandeSangSerializer, DonSerializer, DossierPredonSerializer,
    ReponseSerializer, RendezVousSerializer,
)


class DemandeSangViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet,
):
    serializer_class = DemandeSangSerializer

    def get_permissions(self):
        if self.action in ("create", "cloturer"):
            return [IsEtablissementValide()]
        return [IsEtablissement()]

    def get_queryset(self):
        return DemandeSang.objects.filter(
            etablissement=self.request.user.etablissement
        ).annotate(nb_rep=Count("reponses"))

    def create(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        demande = s.save(etablissement=request.user.etablissement)
        profils = donneurs_compatibles(demande)
        envoyer_alertes(demande, profils)
        data = self.get_serializer(demande).data
        data["donneurs_alertes"] = len(profils)
        return Response(data, status=201)

    @action(detail=True, methods=["get"])
    def reponses(self, request, pk=None):
        demande = self.get_object()
        qs = demande.reponses.select_related("donneur__profil_donneur")
        return Response(ReponseSerializer(qs, many=True).data)

    @action(detail=True, methods=["post"])
    def cloturer(self, request, pk=None):
        demande = self.get_object()
        demande.statut = "cloturee"
        demande.save(update_fields=["statut"])
        return Response(self.get_serializer(demande).data)


class RendezVousViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = RendezVousSerializer

    def get_permissions(self):
        ecriture = self.action in ("confirmer", "annuler") or (
            self.action == "predon" and self.request.method == "POST"
        )
        return [IsEtablissementValide()] if ecriture else [IsEtablissement()]

    def get_queryset(self):
        return RendezVous.objects.filter(
            etablissement=self.request.user.etablissement
        ).select_related("donneur", "demande", "predon")

    def _changer_statut(self, nouveau):
        rdv = self.get_object()
        if rdv.statut != "propose":
            return None, Response({"detail": "Rendez-vous déjà traité."}, status=400)
        rdv.statut = nouveau
        rdv.save(update_fields=["statut"])
        return rdv, None

    @action(detail=True, methods=["post"])
    def confirmer(self, request, pk=None):
        rdv, erreur = self._changer_statut("confirme")
        if erreur:
            return erreur
        envoyer_confirmation(rdv)
        return Response(self.get_serializer(rdv).data)

    @action(detail=True, methods=["post"])
    def annuler(self, request, pk=None):
        rdv, erreur = self._changer_statut("annule")
        if erreur:
            return erreur
        return Response(self.get_serializer(rdv).data)

    @action(detail=True, methods=["get", "post"])
    def predon(self, request, pk=None):
        rdv = self.get_object()
        existant = getattr(rdv, "predon", None)
        if request.method == "GET":
            if not existant:
                return Response({"decision": None})
            return Response(DossierPredonSerializer(existant).data)

        if rdv.statut != "confirme":
            return Response(
                {"detail": "Le rendez-vous doit être confirmé avant le pré-don."}, status=400
            )
        s = DossierPredonSerializer(existant, data=request.data)
        s.is_valid(raise_exception=True)
        decision, motifs = evaluer(s.validated_data)
        s.save(rendez_vous=rdv, decision=decision, motifs="\n".join(motifs))
        return Response(s.data, status=201)

    @action(detail=False, methods=["get"])
    def verifier(self, request):
        trouve = re.search(r"BL-(\d+)-([0-9A-Fa-f]{8})", request.query_params.get("code", ""))
        if not trouve:
            return Response(
                {"detail": "Code illisible : collez la référence (BL-...) ou tout le texte du QR."},
                status=400,
            )
        rdv = self.get_queryset().filter(pk=int(trouve.group(1))).first()
        if not rdv or not hmac.compare_digest(reference(rdv), trouve.group(0).upper()):
            return Response(
                {"detail": "Code invalide, ou rendez-vous absent de votre établissement."},
                status=400,
            )
        profil = getattr(rdv.donneur, "profil_donneur", None)
        return Response({
            "reference": reference(rdv),
            "donneur": rdv.donneur.get_full_name() or rdv.donneur.email,
            "email": rdv.donneur.email,
            "telephone": profil.telephone if profil else "",
            "groupe_sanguin": profil.groupe_sanguin if profil else "-",
            "date_heure": rdv.date_heure,
            "statut": rdv.statut,
            "decision_predon": rdv.predon.decision if hasattr(rdv, "predon") else None,
        })
    @action(detail=True, methods=["get"])
    def qr(self, request, pk=None):
        rdv = self.get_object()
        if rdv.statut not in ("confirme", "realise"):
            return Response(
                {"detail": "Le code QR est disponible après la confirmation du rendez-vous."},
                status=400,
            )
        return HttpResponse(image_qr(rdv), content_type="image/png")

class DonViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = DonSerializer

    def get_permissions(self):
        if self.action in ("create", "depistage"):
            return [IsEtablissementValide()]
        return [IsEtablissement()]

    def get_queryset(self):
        return Don.objects.filter(
            etablissement=self.request.user.etablissement
        ).select_related("donneur")

    def perform_create(self, serializer):
        don = serializer.save(etablissement=self.request.user.etablissement)
        if don.rendez_vous:
            don.rendez_vous.statut = "realise"
            don.rendez_vous.save(update_fields=["statut"])
        d = don.demande
        if d and d.statut == "active" and d.dons.count() >= d.quantite:
            d.statut = "satisfaite"
            d.save(update_fields=["statut"])

    @action(detail=True, methods=["post"])
    def depistage(self, request, pk=None):
        don = self.get_object()
        resultat = request.data.get("resultat")
        if resultat not in ("en_attente", "conforme", "non_conforme"):
            return Response({"detail": "Résultat invalide."}, status=400)
        don.depistage = resultat
        don.save(update_fields=["depistage"])
        return Response(self.get_serializer(don).data)


class DashboardView(APIView):
    permission_classes = [IsEtablissement]

    def get(self, request):
        e = request.user.etablissement
        now = timezone.now()
        actives = e.demandes.filter(statut="active").filter(
            Q(date_don__gte=now) | Q(date_don__isnull=True)
        )
        rdv_futurs = e.rendez_vous.filter(
            statut__in=["propose", "confirme"], date_heure__gte=now
        ).select_related("donneur", "demande", "predon")
        recentes = actives.annotate(nb_rep=Count("reponses")).order_by("date_don")[:5]
        return Response({
            "demandes_actives": actives.count(),
            "reponses_recues": Reponse.objects.filter(demande__etablissement=e).count(),
            "rdv_a_confirmer": e.rendez_vous.filter(statut="propose").count(),
            "dons_realises": e.dons.count(),
            "demandes_recentes": DemandeSangSerializer(recentes, many=True).data,
            "rdv_a_venir": RendezVousSerializer(rdv_futurs[:5], many=True).data,
        })