from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from donneurs.models import ProfilDonneur
from etablissements.models import Etablissement

User = get_user_model()


class LoginValidationTests(APITestCase):
    def _login(self, email):
        return self.client.post(
            "/api/auth/login/", {"email": email, "password": "Test12345"}, format="json"
        )

    def test_etablissement_en_attente_refuse(self):
        user = User.objects.create_user(
            email="att@test.tn", password="Test12345", role="etablissement"
        )
        Etablissement.objects.create(
            user=user, nom="Clinique", ville="Kelibia", statut_validation="en_attente"
        )
        self.assertEqual(self._login("att@test.tn").status_code, 403)

    def test_etablissement_valide_connecte(self):
        user = User.objects.create_user(
            email="ok@test.tn", password="Test12345", role="etablissement"
        )
        Etablissement.objects.create(
            user=user, nom="Hopital", ville="Kelibia", statut_validation="valide"
        )
        self.assertEqual(self._login("ok@test.tn").status_code, 200)

    def test_donneur_connecte_directement(self):
        user = User.objects.create_user(
            email="don@test.tn", password="Test12345", role="donneur"
        )
        ProfilDonneur.objects.create(user=user, groupe_sanguin="O+", ville="Kelibia")
        r = self._login("don@test.tn")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["role"], "donneur")