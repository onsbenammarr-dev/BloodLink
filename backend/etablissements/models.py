from django.conf import settings
from django.db import models


class Etablissement(models.Model):
    STATUTS = [
        ("en_attente", "En attente"),
        ("valide", "Validé"),
        ("refuse", "Refusé"),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="etablissement"
    )
    nom = models.CharField(max_length=150)
    ville = models.CharField(max_length=100)
    statut_validation = models.CharField(max_length=20, choices=STATUTS, default="en_attente")
    motif_refus = models.TextField(blank=True)

    def __str__(self):
        return self.nom