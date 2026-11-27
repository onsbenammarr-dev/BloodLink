"""Crée des données de démonstration pour présenter BloodLink.

Usage, depuis le dossier backend :
  python manage.py demo           crée les données (une seule fois)
  python manage.py demo --reset   supprime puis recrée les données de démonstration

Aucun e-mail n'est envoyé. Les comptes de démonstration ont une adresse
se terminant par @demo.bloodlink.tn (adresses fictives).
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from demandes.models import DemandeSang, Don, DossierPredon, RendezVous
from demandes.sante import evaluer
from donneurs.models import ProfilDonneur, Reponse
from etablissements.models import Etablissement

User = get_user_model()
DOMAINE = "@demo.bloodlink.tn"
MOT_DE_PASSE = "Demo12345"

DONNEURS = [
    ("Amine", "Trabelsi", "O+", "Kélibia", "+216 20 111 001"),
    ("Sarra", "BenSalah", "A+", "Kélibia", "+216 20 111 002"),
    ("Yassine", "Mejri", "O-", "Kélibia", "+216 20 111 003"),
    ("Ines", "Khelifi", "B+", "Kélibia", "+216 20 111 004"),
    ("Mehdi", "Jaziri", "A-", "Nabeul", "+216 20 111 005"),
    ("Rania", "Gharbi", "AB+", "Kélibia", "+216 20 111 006"),
    ("Karim", "BenYoussef", "O+", "Tunis", "+216 20 111 007"),
    ("Lina", "Hamdi", "A+", "Kélibia", "+216 20 111 008"),
]

NORMAL = {
    "age": 30, "poids": 70.0, "hemoglobine": 14.0, "tension_sys": 120, "tension_dia": 80,
    "pouls": 70, "temperature": 36.8, "jours_depuis_dernier_don": None,
    "symptomes_recents": False, "traitement_en_cours": False,
    "chirurgie_tatouage_recent": False, "voyage_zone_risque": False,
    "grossesse_allaitement": False,
}


class Command(BaseCommand):
    help = "Crée des données de démonstration (établissement, donneurs, demandes, rendez-vous, dons)."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true",
                            help="Supprime puis recrée les données de démonstration.")

    @transaction.atomic
    def handle(self, *args, **options):
        existants = User.objects.filter(email__endswith=DOMAINE)
        if existants.exists():
            if not options["reset"]:
                self.stdout.write("Les données de démonstration existent déjà. "
                                  "Utilise  python manage.py demo --reset  pour les recréer.")
                return
            existants.delete()

        maintenant = timezone.now()

        # --- Établissements -------------------------------------------------
        u = User.objects.create_user(email="etablissement" + DOMAINE, password=MOT_DE_PASSE,
                                     role="etablissement")
        etab = Etablissement.objects.create(user=u, nom="Hôpital Régional de Kélibia",
                                            ville="Kélibia", statut_validation="valide")
        u2 = User.objects.create_user(email="clinique.attente" + DOMAINE, password=MOT_DE_PASSE,
                                      role="etablissement")
        Etablissement.objects.create(user=u2, nom="Clinique El Manar", ville="Nabeul",
                                     statut_validation="en_attente")

        # --- Donneurs -------------------------------------------------------
        donneurs = {}
        for prenom, nom, groupe, ville, tel in DONNEURS:
            user = User.objects.create_user(
                email=f"{prenom}.{nom}".lower() + DOMAINE, password=MOT_DE_PASSE,
                role="donneur", first_name=prenom, last_name=nom)
            ProfilDonneur.objects.create(user=user, groupe_sanguin=groupe, ville=ville, telephone=tel)
            donneurs[prenom] = user

        # --- Outils ---------------------------------------------------------
        def demande(groupe, quantite, jours, statut="active", il_y_a=0):
            d = DemandeSang.objects.create(
                etablissement=etab, groupe_sanguin=groupe, quantite=quantite, ville="Kélibia",
                date_don=maintenant + timedelta(days=jours),
                delai_heures=max(1, abs(jours) * 24), statut=statut)
            if il_y_a:
                DemandeSang.objects.filter(pk=d.pk).update(
                    date_creation=maintenant - timedelta(days=il_y_a))
            return d

        def rdv(prenom, dem, jours, heure, statut):
            quand = timezone.localtime(maintenant + timedelta(days=jours)).replace(
                hour=heure, minute=0, second=0, microsecond=0)
            return RendezVous.objects.create(donneur=donneurs[prenom], etablissement=etab,
                                             demande=dem, date_heure=quand, statut=statut)

        def predon(rendez_vous, **modifs):
            mesures = {**NORMAL, **modifs}
            decision, motifs = evaluer(mesures)
            DossierPredon.objects.create(rendez_vous=rendez_vous, decision=decision,
                                         motifs="\n".join(motifs), **mesures)

        def don(prenom, jours_passes, dem=None, rendez_vous=None, depistage="conforme"):
            d = Don.objects.create(donneur=donneurs[prenom], etablissement=etab, demande=dem,
                                   rendez_vous=rendez_vous, depistage=depistage)
            Don.objects.filter(pk=d.pk).update(date=maintenant - timedelta(days=jours_passes))

        # --- Demandes -------------------------------------------------------
        d1 = demande("A+", 3, 2)
        d2 = demande("O-", 2, 1)
        d3 = demande("B+", 2, 5)
        d4 = demande("O+", 2, -3, "satisfaite", il_y_a=5)
        demande("A+", 1, -1, "active", il_y_a=3)  # expirée

        # --- Réponses et rendez-vous ---------------------------------------
        for prenom, dem in [("Sarra", d1), ("Lina", d1), ("Amine", d1), ("Yassine", d2), ("Ines", d3)]:
            Reponse.objects.create(donneur=donneurs[prenom], demande=dem)

        rdv("Sarra", d1, 2, 10, "propose")
        rdv("Lina", d1, 2, 11, "propose")
        r3 = rdv("Amine", d1, 3, 9, "confirme")
        predon(r3)                                    # apte : « Enregistrer le don » disponible
        r4 = rdv("Yassine", d2, 1, 15, "confirme")
        predon(r4, poids=48.0)                        # ajourné : poids insuffisant
        rdv("Ines", d3, 4, 14, "propose")

        # --- Dons réalisés et historique -------------------------------------
        r6 = rdv("Amine", d4, -3, 9, "realise")
        predon(r6)
        r7 = rdv("Yassine", d4, -3, 10, "realise")
        predon(r7)
        don("Amine", 3, d4, r6, "en_attente")
        don("Yassine", 3, d4, r7, "en_attente")
        for jours in (420, 300, 200, 90):
            don("Amine", jours)
        don("Yassine", 250)
        don("Sarra", 150, depistage="non_conforme")
        don("Lina", 60)
        don("Ines", 40)

        self.stdout.write(self.style.SUCCESS("Données de démonstration créées."))
        self.stdout.write(f"  Établissement validé : etablissement{DOMAINE} / {MOT_DE_PASSE}")
        self.stdout.write(f"  Établissement en attente : clinique.attente{DOMAINE} / {MOT_DE_PASSE}")
        self.stdout.write(f"  Donneurs : prenom.nom{DOMAINE} / {MOT_DE_PASSE}  "
                          f"(par exemple amine.trabelsi{DOMAINE})")