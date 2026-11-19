import math
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from donneurs.models import Reponse
from .models import DemandeSang, DossierPredon, Don, RendezVous


class DemandeSangSerializer(serializers.ModelSerializer):
    nb_reponses = serializers.SerializerMethodField()
    expiree = serializers.SerializerMethodField()

    class Meta:
        model = DemandeSang
        fields = [
            "id", "groupe_sanguin", "quantite", "ville", "date_don", "delai_heures",
            "statut", "date_creation", "nb_reponses", "expiree",
        ]
        read_only_fields = ["statut", "date_creation"]

    def get_nb_reponses(self, obj):
        n = getattr(obj, "nb_rep", None)
        return n if n is not None else obj.reponses.count()

    def get_expiree(self, obj):
        return bool(obj.statut == "active" and obj.date_don and obj.date_don < timezone.now())

    def validate(self, attrs):
        now = timezone.now()
        date_don = attrs.get("date_don")
        if date_don:
            if date_don <= now:
                raise serializers.ValidationError(
                    {"date_don": "La date et l'heure du don doivent être dans le futur."}
                )
            attrs["delai_heures"] = max(1, math.ceil((date_don - now).total_seconds() / 3600))
        else:
            attrs["date_don"] = now + timedelta(hours=attrs.get("delai_heures", 24))
        return attrs


class ReponseSerializer(serializers.ModelSerializer):
    donneur_email = serializers.EmailField(source="donneur.email", read_only=True)
    groupe_sanguin = serializers.CharField(
        source="donneur.profil_donneur.groupe_sanguin", read_only=True
    )
    ville = serializers.CharField(source="donneur.profil_donneur.ville", read_only=True)

    class Meta:
        model = Reponse
        fields = ["id", "donneur", "donneur_email", "groupe_sanguin", "ville", "date"]


class RendezVousSerializer(serializers.ModelSerializer):
    donneur_email = serializers.EmailField(source="donneur.email", read_only=True)
    groupe_sanguin = serializers.SerializerMethodField()
    decision_predon = serializers.SerializerMethodField()

    class Meta:
        model = RendezVous
        fields = [
            "id", "donneur", "donneur_email", "demande", "groupe_sanguin",
            "date_heure", "statut", "decision_predon",
        ]
        read_only_fields = fields

    def get_groupe_sanguin(self, obj):
        return obj.demande.groupe_sanguin if obj.demande else "-"

    def get_decision_predon(self, obj):
        p = getattr(obj, "predon", None)
        return p.decision if p else None


class DossierPredonSerializer(serializers.ModelSerializer):
    motifs = serializers.SerializerMethodField()

    class Meta:
        model = DossierPredon
        fields = [
            "age", "poids", "hemoglobine", "tension_sys", "tension_dia", "pouls",
            "temperature", "jours_depuis_dernier_don", "symptomes_recents",
            "traitement_en_cours", "chirurgie_tatouage_recent", "voyage_zone_risque",
            "grossesse_allaitement", "decision", "motifs", "date_evaluation",
        ]
        read_only_fields = ["decision", "date_evaluation"]

    def get_motifs(self, obj):
        return [m for m in obj.motifs.split("\n") if m]


class DonSerializer(serializers.ModelSerializer):
    donneur_email = serializers.EmailField(source="donneur.email", read_only=True)

    class Meta:
        model = Don
        fields = ["id", "donneur", "donneur_email", "demande", "rendez_vous", "depistage", "date"]
        read_only_fields = ["date", "depistage"]

    def validate_donneur(self, user):
        if user.role != "donneur":
            raise serializers.ValidationError("Cet utilisateur n'est pas un donneur.")
        return user

    def validate(self, attrs):
        etab = self.context["request"].user.etablissement
        for champ in ("demande", "rendez_vous"):
            obj = attrs.get(champ)
            if obj and obj.etablissement_id != etab.id:
                raise serializers.ValidationError(
                    {champ: "N'appartient pas à votre établissement."}
                )
        rdv = attrs.get("rendez_vous")
        if rdv:
            predon = getattr(rdv, "predon", None)
            if not predon or predon.decision != "apte":
                raise serializers.ValidationError({
                    "rendez_vous": "Le donneur doit être déclaré apte lors du pré-don avant l'enregistrement du don."
                })
        return attrs