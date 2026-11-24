"""Modèle « probabilité qu'un donneur revienne », entraîné sur des données RÉELLES.

Jeu de données : Blood Transfusion Service Center (UCI Machine Learning Repository),
748 donneurs du centre de transfusion de Hsin-Chu (Taïwan), I-Cheng Yeh, 2008, licence CC BY 4.0.
Variables : Recency (mois depuis le dernier don), Frequency (nombre de dons),
Monetary (volume total donné, en cc), Time (mois depuis le premier don),
cible : le donneur a-t-il donné en mars 2007 ? (1 = oui).

Usage, depuis le dossier backend :  python ml/retour_donneur.py
"""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DOSSIER = Path(__file__).resolve().parent
FICHIER = DOSSIER / "transfusion.csv"
COLONNES = ["Recency", "Frequency", "Monetary", "Time", "Donated"]
# Monetary vaut toujours 250 x Frequency : variable redondante, donc écartée.
CARACTERISTIQUES = ["Recency", "Frequency", "Time"]
SOURCE = "UCI Blood Transfusion Service Center (Taïwan, 748 donneurs)"


def charger_donnees():
    """Lit ml/transfusion.csv ; le télécharge depuis UCI s'il est absent."""
    if not FICHIER.exists():
        from ucimlrepo import fetch_ucirepo

        base = fetch_ucirepo(id=176)
        df = pd.concat([base.data.features, base.data.targets], axis=1)
        df.columns = COLONNES
        df.to_csv(FICHIER, index=False)

    df = pd.read_csv(FICHIER)
    if pd.to_numeric(pd.Index(df.columns), errors="coerce").notna().any():
        df = pd.read_csv(FICHIER, header=None)  # fichier sans ligne d'en-tête
    if df.shape[1] != 5:
        raise SystemExit("transfusion.csv doit contenir 5 colonnes (R, F, M, T, cible).")
    df.columns = COLONNES
    return df.apply(pd.to_numeric)


def charger():
    modele = joblib.load(DOSSIER / "retour_modele.joblib")
    metriques = json.loads((DOSSIER / "retour_metriques.json").read_text(encoding="utf-8"))
    return modele, metriques


def probabilite(modele, mois_depuis_dernier_don, nb_dons, mois_depuis_premier_don):
    x = pd.DataFrame(
        [[mois_depuis_dernier_don, nb_dons, mois_depuis_premier_don]], columns=CARACTERISTIQUES
    )
    return float(modele.predict_proba(x)[0][1])


def main():
    df = charger_donnees()
    X, y = df[CARACTERISTIQUES], df["Donated"]
    print(f"{len(df)} donneurs, dont {y.mean():.0%} ont donné en mars 2007.")

    X_app, X_test, y_app, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )
    reference = max(y_test.mean(), 1 - y_test.mean())  # toujours prédire « ne revient pas »
    candidats = {
        "Régression logistique": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        "Forêt aléatoire": RandomForestClassifier(n_estimators=300, min_samples_leaf=5, random_state=42),
    }
    scores = {}
    for nom, modele in candidats.items():
        modele.fit(X_app, y_app)
        scores[nom] = {
            "auc": float(roc_auc_score(y_test, modele.predict_proba(X_test)[:, 1])),
            "precision": float(accuracy_score(y_test, modele.predict(X_test))),
        }

    meilleur = max(scores, key=lambda k: scores[k]["auc"])
    modele = candidats[meilleur]
    modele.fit(X, y)  # ré-entraînement sur toutes les données avant sauvegarde
    joblib.dump(modele, DOSSIER / "retour_modele.joblib")

    metriques = {
        "source": SOURCE,
        "modele": meilleur,
        "auc": round(scores[meilleur]["auc"], 3),
        "precision": round(scores[meilleur]["precision"], 3),
        "precision_reference": round(float(reference), 3),
        "donneurs_apprentissage": int(len(X_app)),
        "donneurs_test": int(len(X_test)),
    }
    (DOSSIER / "retour_metriques.json").write_text(
        json.dumps(metriques, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nRésultats sur le jeu de test (donneurs jamais vus à l'entraînement) :")
    print(f"  Précision de référence (toujours « ne revient pas ») : {reference:.3f}")
    for nom, s in scores.items():
        print(f"  {nom} : AUC {s['auc']:.3f} | précision {s['precision']:.3f}")
    print(f"Modèle retenu : {meilleur}")


if __name__ == "__main__":
    main()