from django.test import SimpleTestCase

from demandes.sante import evaluer

BASE = {
    "age": 30, "poids": 70, "hemoglobine": 14.0, "tension_sys": 120,
    "tension_dia": 80, "pouls": 70, "temperature": 36.8,
    "jours_depuis_dernier_don": None,
}


class EvaluerTests(SimpleTestCase):
    def test_apte(self):
        self.assertEqual(evaluer(BASE), ("apte", []))

    def test_poids_insuffisant(self):
        decision, motifs = evaluer({**BASE, "poids": 45})
        self.assertEqual(decision, "ajourne")
        self.assertTrue(any("Poids" in m for m in motifs))

    def test_hemoglobine_basse(self):
        self.assertEqual(evaluer({**BASE, "hemoglobine": 11.0})[0], "ajourne")

    def test_dernier_don_trop_recent(self):
        self.assertEqual(evaluer({**BASE, "jours_depuis_dernier_don": 20})[0], "ajourne")

    def test_mineur(self):
        self.assertEqual(evaluer({**BASE, "age": 17})[0], "ajourne")

    def test_voyage_avis_medical(self):
        self.assertEqual(evaluer({**BASE, "voyage_zone_risque": True})[0], "avis_medical")

    def test_traitement_avis_medical(self):
        self.assertEqual(evaluer({**BASE, "traitement_en_cours": True})[0], "avis_medical")