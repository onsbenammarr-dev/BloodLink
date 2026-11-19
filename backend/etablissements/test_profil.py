from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from etablissements.models import Etablissement

User = get_user_model()


class ProfilTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="p@test.tn", password="Test12345", role="etablissement"
        )
        self.etab = Etablissement.objects.create(
            user=self.user, nom="Clinique", ville="Kelibia", statut_validation="valide"
        )
        self.client.force_authenticate(user=self.user)

    def test_modifier_nom_et_ville(self):
        r = self.client.patch(
            "/api/etablissements/me/", {"nom": "Nouvelle", "ville": "Nabeul"}, format="json"
        )
        self.assertEqual(r.status_code, 200)
        self.etab.refresh_from_db()
        self.assertEqual((self.etab.nom, self.etab.ville), ("Nouvelle", "Nabeul"))

    def test_statut_non_modifiable(self):
        self.client.patch(
            "/api/etablissements/me/", {"statut_validation": "refuse"}, format="json"
        )
        self.etab.refresh_from_db()
        self.assertEqual(self.etab.statut_validation, "valide")

    def test_changer_mot_de_passe(self):
        r = self.client.post(
            "/api/auth/mot-de-passe/",
            {"ancien": "Test12345", "nouveau": "OrangeTigreBleu"},
            format="json",
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("token", r.data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("OrangeTigreBleu"))

    def test_ancien_mot_de_passe_faux(self):
        r = self.client.post(
            "/api/auth/mot-de-passe/",
            {"ancien": "faux", "nouveau": "OrangeTigreBleu"},
            format="json",
        )
        self.assertEqual(r.status_code, 400)