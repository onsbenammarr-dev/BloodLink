"""Critères indicatifs d'aptitude au don de sang total.

Ces seuils sont des valeurs courantes données à titre d'exemple. Ils doivent être
validés par le médecin de l'établissement. La décision finale lui revient.
"""

AGE = (18, 65)
POIDS_MIN = 50
HEMOGLOBINE_MIN = 12.5
TENSION_SYS = (100, 180)
TENSION_DIA_MAX = 100
POULS = (50, 100)
TEMPERATURE_MAX = 37.5
INTERVALLE_DONS_JOURS = 56


def evaluer(d):
    """Renvoie (decision, motifs) à partir des mesures et des réponses du pré-don."""
    ajourne, avis = [], []

    if not AGE[0] <= d["age"] <= AGE[1]:
        ajourne.append(f"Âge hors de la plage de {AGE[0]} à {AGE[1]} ans")
    if d["poids"] < POIDS_MIN:
        ajourne.append(f"Poids inférieur à {POIDS_MIN} kg")
    if d["hemoglobine"] < HEMOGLOBINE_MIN:
        ajourne.append(f"Hémoglobine inférieure à {HEMOGLOBINE_MIN} g/dL")
    if not TENSION_SYS[0] <= d["tension_sys"] <= TENSION_SYS[1] or d["tension_dia"] > TENSION_DIA_MAX:
        ajourne.append("Tension artérielle hors des limites")
    if not POULS[0] <= d["pouls"] <= POULS[1]:
        ajourne.append("Pouls hors des limites")
    if d["temperature"] > TEMPERATURE_MAX:
        ajourne.append(f"Température supérieure à {TEMPERATURE_MAX} °C")

    jours = d.get("jours_depuis_dernier_don")
    if jours is not None and jours < INTERVALLE_DONS_JOURS:
        ajourne.append(f"Dernier don trop récent (moins de {INTERVALLE_DONS_JOURS} jours)")
    if d.get("symptomes_recents"):
        ajourne.append("Fièvre, infection ou symptômes récents")
    if d.get("chirurgie_tatouage_recent"):
        ajourne.append("Chirurgie, tatouage ou piercing récent")
    if d.get("grossesse_allaitement"):
        ajourne.append("Grossesse ou allaitement")

    if d.get("traitement_en_cours"):
        avis.append("Traitement en cours : avis du médecin requis")
    if d.get("voyage_zone_risque"):
        avis.append("Voyage récent en zone à risque : avis du médecin requis")

    if ajourne:
        return "ajourne", ajourne + avis
    if avis:
        return "avis_medical", avis
    return "apte", []