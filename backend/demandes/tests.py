from django.test import TestCase

class LoginValidationTests(APITestCase):
    def test_etablissement_en_attente_refuse(self):
        creer_etablissement(email="att@test.tn", statut="en_attente")
        r = self.client.post("/api/auth/login/",
                             {"email": "att@test.tn", "password": "Test12345"}, format="json")
        self.assertEqual(r.status_code, 403)

    def test_donneur_connecte_directement(self):
        creer_donneur("don@test.tn", "O+")
        r = self.client.post("/api/auth/login/",
                             {"email": "don@test.tn", "password": "Test12345"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["role"], "donneur")