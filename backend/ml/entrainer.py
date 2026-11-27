"""Entraîne le modèle de prévision de la demande de sang.

Les données sont SYNTHÉTIQUES (générées ici) : à présenter comme telles dans le rapport.
Usage, depuis le dossier backend :  python ml/entrainer.py
"""
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ml.prevision import jeu_apprentissage  # noqa: E402

DOSSIER = Path(__file__).resolve().parent
JOURS = 540
POPULARITE = {"O+": 3.0, "A+": 2.6, "B+": 1.4, "O-": 0.8, "A-": 0.7, "AB+": 0.5, "B-": 0.4, "AB-": 0.2}
EFFET_JOUR = [1.15, 1.2, 1.15, 1.1, 1.0, 0.7, 0.6]  # lundi à dimanche


def generer(seed=42):
    """Historique quotidien des demandes par groupe : base par groupe, effet du jour,
    légère tendance, saisonnalité et pics d'urgence (accidents, afflux)."""
    rng = np.random.default_rng(seed)
    fin = pd.Timestamp.today().normalize() - pd.Timedelta(days=1)
    dates = pd.date_range(end=fin, periods=JOURS)
    pics = np.zeros(JOURS)
    for debut in rng.choice(JOURS - 5, size=12, replace=False):
        pics[debut:debut + rng.integers(2, 5)] += rng.uniform(0.5, 1.5)
    lignes = []
    for g, base in POPULARITE.items():
        for i, d in enumerate(dates):
            tendance = 1 + 0.15 * i / JOURS
            saison = 1 + 0.1 * np.sin(2 * np.pi * d.dayofyear / 365)
            lam = base * EFFET_JOUR[d.weekday()] * tendance * saison * (1 + pics[i])
            lignes.append({
                "date": d.date().isoformat(),
                "groupe_sanguin": g,
                "nb_demandes": int(rng.poisson(lam)),
            })
    return pd.DataFrame(lignes)


def main():
    df = generer()
    df.to_csv(DOSSIER / "donnees_synthetiques.csv", index=False)

    X, y, dates = jeu_apprentissage(df)
    coupure = dates.max() - pd.Timedelta(days=60)      # test = 60 derniers jours
    test = (dates > coupure).to_numpy()
    X_app, X_test, y_app, y_test = X[~test], X[test], y[~test], y[test]

    reference = mean_absolute_error(y_test, X_test["moy_7"])  # prédire la moyenne des 7 derniers jours
    candidats = {
        "Régression linéaire": LinearRegression(),
        "Forêt aléatoire": RandomForestRegressor(n_estimators=200, min_samples_leaf=3, random_state=42),
    }
    scores = {}
    for nom, modele in candidats.items():
        modele.fit(X_app, y_app)
        scores[nom] = mean_absolute_error(y_test, modele.predict(X_test))

    meilleur = min(scores, key=scores.get)
    modele = candidats[meilleur]
    modele.fit(X, y)  # ré-entraînement sur toutes les données avant sauvegarde
    joblib.dump(modele, DOSSIER / "modele.joblib")

    metriques = {
        "source": "synthetique",
        "modele": meilleur,
        "mae": round(float(scores[meilleur]), 3),
        "mae_reference": round(float(reference), 3),
        "scores": {k: round(float(v), 3) for k, v in scores.items()},
        "lignes_apprentissage": int((~test).sum()),
        "lignes_test": int(test.sum()),
    }
    (DOSSIER / "metriques.json").write_text(
        json.dumps(metriques, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Erreur absolue moyenne (MAE) sur les 60 derniers jours :")
    print(f"  Référence (moyenne 7 jours) : {reference:.3f}")
    for nom, s in scores.items():
        print(f"  {nom} : {s:.3f}")
    print(f"Modèle retenu : {meilleur}")


if __name__ == "__main__":
    main()