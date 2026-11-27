import json
from datetime import timedelta
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

DOSSIER = Path(__file__).resolve().parent
GROUPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
COLONNES = (
    ["lag_1", "lag_7", "moy_7", "moy_14"]
    + [f"jour_{i}" for i in range(7)]
    + [f"groupe_{g}" for g in GROUPES]
)


def caracteristiques(valeurs, date, groupe):
    """Une ligne de caractéristiques (la valeur la plus récente est en dernier)."""
    ligne = {
        "lag_1": valeurs[-1],
        "lag_7": valeurs[-7],
        "moy_7": float(np.mean(valeurs[-7:])),
        "moy_14": float(np.mean(valeurs[-14:])),
    }
    for i in range(7):
        ligne[f"jour_{i}"] = 1 if date.weekday() == i else 0
    for g in GROUPES:
        ligne[f"groupe_{g}"] = 1 if g == groupe else 0
    return ligne


def jeu_apprentissage(df):
    """df : colonnes date, groupe_sanguin, nb_demandes (une ligne par jour et par groupe)."""
    lignes, cibles, dates = [], [], []
    for g, sous in df.sort_values("date").groupby("groupe_sanguin"):
        valeurs = sous["nb_demandes"].tolist()
        jours = pd.to_datetime(sous["date"]).tolist()
        for i in range(14, len(valeurs)):
            lignes.append(caracteristiques(valeurs[:i], jours[i], g))
            cibles.append(valeurs[i])
            dates.append(jours[i])
    return pd.DataFrame(lignes)[COLONNES], np.array(cibles), pd.Series(dates)


def prevoir(modele, historique, premier_jour, jours=7):
    """historique : dict groupe -> 14 dernières valeurs. Prévision récursive jour par jour."""
    resultat = {}
    for g in GROUPES:
        valeurs = [float(v) for v in historique[g]]
        sorties = []
        for k in range(jours):
            date = premier_jour + timedelta(days=k)
            x = pd.DataFrame([caracteristiques(valeurs, date, g)])[COLONNES]
            p = max(0.0, float(modele.predict(x)[0]))
            sorties.append(round(p, 2))
            valeurs.append(p)
        resultat[g] = sorties
    return resultat


def charger():
    """Charge le modèle, les métriques et l'historique récent. Lève FileNotFoundError si absent."""
    modele = joblib.load(DOSSIER / "modele.joblib")
    metriques = json.loads((DOSSIER / "metriques.json").read_text(encoding="utf-8"))
    df = pd.read_csv(DOSSIER / "donnees_synthetiques.csv", parse_dates=["date"])
    historique = {
        g: s.sort_values("date")["nb_demandes"].tolist()[-14:]
        for g, s in df.groupby("groupe_sanguin")
    }
    par_jour = df.groupby("date")["nb_demandes"].sum().sort_index().tail(14)
    contexte = {
        "dates": [d.date().isoformat() for d in par_jour.index],
        "valeurs": [int(v) for v in par_jour.values],
    }
    return modele, metriques, historique, contexte