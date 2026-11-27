from datetime import date

from django.test import SimpleTestCase

from ml.prevision import COLONNES, GROUPES, caracteristiques, prevoir


class ModeleFactice:
    def predict(self, X):
        return [X["moy_7"].iloc[0]]


class PrevisionTests(SimpleTestCase):
    def test_caracteristiques(self):
        ligne = caracteristiques([1.0] * 14, date(2026, 11, 16), "A+")  # un lundi
        self.assertEqual(set(ligne), set(COLONNES))
        self.assertEqual(ligne["jour_0"], 1)
        self.assertEqual(ligne["groupe_A+"], 1)

    def test_prevoir_sept_jours(self):
        historique = {g: [2.0] * 14 for g in GROUPES}
        res = prevoir(ModeleFactice(), historique, date(2026, 11, 16), 7)
        self.assertEqual(set(res), set(GROUPES))
        self.assertTrue(all(len(v) == 7 for v in res.values()))
        self.assertTrue(all(x >= 0 for v in res.values() for x in v))