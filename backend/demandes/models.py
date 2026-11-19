from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .constants import GROUPES


class DemandeSang(models.Model):
    STATUTS = [
        ("active", "Active"),
        ("satisfaite", "Satisfaite"),
        ("cloturee", "Clôturée"),
    ]
    etablissement = models.ForeignKey(
        "etablissements.Etablissement", on_delete=models.CASCADE, related_name="demandes"
    )
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPES)
    quantite = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    ville = models.CharField(max_length=100)
    delai_heures = models.PositiveIntegerField(default=24)
    date_don = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default="active")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"{self.groupe_sanguin} x{self.quantite} - {self.ville}"


class RendezVous(models.Model):
    STATUTS = [
        ("propose", "Proposé"),
        ("confirme", "Confirmé"),
        ("annule", "Annulé"),
        ("realise", "Réalisé"),
    ]
    donneur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rendez_vous"
    )
    etablissement = models.ForeignKey(
        "etablissements.Etablissement", on_delete=models.CASCADE, related_name="rendez_vous"
    )
    demande = models.ForeignKey(
        DemandeSang, on_delete=models.SET_NULL, null=True, blank=True, related_name="rendez_vous"
    )
    date_heure = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUTS, default="propose")

    class Meta:
        ordering = ["date_heure"]


class Don(models.Model):
    DEPISTAGES = [
        ("en_attente", "En attente"),
        ("conforme", "Conforme"),
        ("non_conforme", "Non conforme"),
    ]
    donneur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dons"
    )
    etablissement = models.ForeignKey(
        "etablissements.Etablissement", on_delete=models.CASCADE, related_name="dons"
    )
    demande = models.ForeignKey(
        DemandeSang, on_delete=models.SET_NULL, null=True, blank=True, related_name="dons"
    )
    rendez_vous = models.OneToOneField(
        RendezVous, on_delete=models.SET_NULL, null=True, blank=True, related_name="don"
    )
    depistage = models.CharField(max_length=20, choices=DEPISTAGES, default="en_attente")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]


class DossierPredon(models.Model):
    DECISIONS = [
        ("apte", "Apte"),
        ("ajourne", "Ajourné"),
        ("avis_medical", "Avis médical requis"),
    ]
    rendez_vous = models.OneToOneField(
        RendezVous, on_delete=models.CASCADE, related_name="predon"
    )
    age = models.PositiveIntegerField(validators=[MinValueValidator(16), MaxValueValidator(90)])
    poids = models.FloatField(validators=[MinValueValidator(30), MaxValueValidator(200)])
    hemoglobine = models.FloatField(validators=[MinValueValidator(5), MaxValueValidator(20)])
    tension_sys = models.PositiveIntegerField(validators=[MinValueValidator(60), MaxValueValidator(250)])
    tension_dia = models.PositiveIntegerField(validators=[MinValueValidator(30), MaxValueValidator(150)])
    pouls = models.PositiveIntegerField(validators=[MinValueValidator(30), MaxValueValidator(220)])
    temperature = models.FloatField(validators=[MinValueValidator(34), MaxValueValidator(42)])
    jours_depuis_dernier_don = models.PositiveIntegerField(null=True, blank=True)
    symptomes_recents = models.BooleanField(default=False)
    traitement_en_cours = models.BooleanField(default=False)
    chirurgie_tatouage_recent = models.BooleanField(default=False)
    voyage_zone_risque = models.BooleanField(default=False)
    grossesse_allaitement = models.BooleanField(default=False)
    decision = models.CharField(max_length=20, choices=DECISIONS)
    motifs = models.TextField(blank=True)
    date_evaluation = models.DateTimeField(auto_now=True)