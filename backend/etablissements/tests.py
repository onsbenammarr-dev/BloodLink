from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from etablissements.emails import envoyer_decision
from etablissements.models import Etablissement

User = get_user_model()


class DecisionEmailTests(TestCase):
    def _etab(self, statut, motif=""):
        user = User.objects.create_user(
            email="h@test.tn", password="Test12345", role="etablissement"
        )
        return Etablissement.objects.create(
            user=user, nom="Clinique", ville="Kelibia",
            statut_validation=statut, motif_refus=motif,
        )

    @patch("etablissements.emails.lancer")
    def test_validation(self, lancer):
        envoyer_decision(self._etab("valide"))
        message = lancer.call_args.args[0][0]
        self.assertEqual(message.to, ["h@test.tn"])
        self.assertIn("validé", message.subject)

    @patch("etablissements.emails.lancer")
    def test_refus_avec_motif(self, lancer):
        envoyer_decision(self._etab("refuse", "Dossier incomplet"))
        message = lancer.call_args.args[0][0]
        self.assertIn("pas été acceptée", message.subject)
        self.assertIn("Dossier incomplet", message.body)

    @patch("etablissements.emails.lancer")
    def test_en_attente_n_envoie_rien(self, lancer):
        envoyer_decision(self._etab("en_attente"))
        lancer.assert_not_called()