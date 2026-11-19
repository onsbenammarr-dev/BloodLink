from django.conf import settings
from django.db import models
from demandes.constants import GROUPES


class ProfilDonneur(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profil_donneur"
    )
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPES)
    ville = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} ({self.groupe_sanguin})"


class Reponse(models.Model):
    donneur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reponses"
    )
    demande = models.ForeignKey(
        "demandes.DemandeSang", on_delete=models.CASCADE, related_name="reponses"
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("donneur", "demande")