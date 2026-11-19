import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../api";
import { DECISIONS, messageErreur } from "../utils";

const VIDE = {
  age: "", poids: "", hemoglobine: "", tension_sys: "", tension_dia: "", pouls: "",
  temperature: "", jours_depuis_dernier_don: "",
  symptomes_recents: false, traitement_en_cours: false, chirurgie_tatouage_recent: false,
  voyage_zone_risque: false, grossesse_allaitement: false,
};

const NUM = ["age", "poids", "hemoglobine", "tension_sys", "tension_dia", "pouls", "temperature", "jours_depuis_dernier_don"];

const CHAMPS = [
  ["age", "Âge (ans)", "1", true],
  ["poids", "Poids (kg)", "0.1", true],
  ["hemoglobine", "Hémoglobine (g/dL)", "0.1", true],
  ["temperature", "Température (°C)", "0.1", true],
  ["tension_sys", "Tension systolique", "1", true],
  ["tension_dia", "Tension diastolique", "1", true],
  ["pouls", "Pouls (battements/min)", "1", true],
  ["jours_depuis_dernier_don", "Jours depuis le dernier don (vide si aucun)", "1", false],
];

const QUESTIONS = [
  ["symptomes_recents", "Fièvre, infection ou symptômes dans les 14 derniers jours"],
  ["traitement_en_cours", "Traitement médicamenteux en cours"],
  ["chirurgie_tatouage_recent", "Chirurgie, tatouage ou piercing dans les 4 derniers mois"],
  ["voyage_zone_risque", "Voyage récent en zone à risque"],
  ["grossesse_allaitement", "Grossesse ou allaitement"],
];

export default function PreDon() {
  const { id } = useParams();
  const [form, setForm] = useState(VIDE);
  const [resultat, setResultat] = useState(null);
  const [erreur, setErreur] = useState("");
  const [envoi, setEnvoi] = useState(false);

  useEffect(() => {
    api
      .get(`/rendez-vous/${id}/predon/`)
      .then((r) => {
        if (!r.data.decision) return;
        setResultat(r.data);
        const rempli = { ...VIDE };
        Object.keys(VIDE).forEach((k) => {
          if (r.data[k] !== null && r.data[k] !== undefined) rempli[k] = r.data[k];
        });
        setForm(rempli);
      })
      .catch((err) => setErreur(messageErreur(err)));
  }, [id]);

  const change = (e) => {
    const { name, type, checked, value } = e.target;
    setForm({ ...form, [name]: type === "checkbox" ? checked : value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErreur("");
    const payload = { ...form };
    NUM.forEach((k) => {
      payload[k] = payload[k] === "" ? null : Number(payload[k]);
    });
    setEnvoi(true);
    try {
      const { data } = await api.post(`/rendez-vous/${id}/predon/`, payload);
      setResultat(data);
    } catch (err) {
      setErreur(messageErreur(err));
    } finally {
      setEnvoi(false);
    }
  };

  return (
    <div className="card page-large">
      <p><Link to="/rendez-vous">← Retour aux rendez-vous</Link></p>
      <h2>Pré-don : évaluation d'aptitude</h2>
      <form onSubmit={handleSubmit}>
        <div className="grille-form">
          {CHAMPS.map(([cle, libelle, pas, requis]) => (
            <div key={cle}>
              <label>{libelle}</label>
              <input
                name={cle}
                type="number"
                step={pas}
                value={form[cle]}
                onChange={change}
                required={requis}
              />
            </div>
          ))}
        </div>
        <h3 style={{ marginTop: 20 }}>Questionnaire</h3>
        {QUESTIONS.map(([cle, texte]) => (
          <label className="case" key={cle}>
            <input type="checkbox" name={cle} checked={form[cle]} onChange={change} />
            {texte}
          </label>
        ))}
        {erreur && <p className="erreur">{erreur}</p>}
        <button type="submit" disabled={envoi}>
          {envoi ? "Évaluation..." : "Évaluer l'aptitude"}
        </button>
      </form>

      {resultat && (
        <div className={`resultat ${resultat.decision}`}>
          <h3>{DECISIONS[resultat.decision]}</h3>
          {resultat.motifs.length > 0 && (
            <ul>
              {resultat.motifs.map((m) => (
                <li key={m}>{m}</li>
              ))}
            </ul>
          )}
          {resultat.decision === "apte" && (
            <p>Le donneur peut donner. Retournez aux rendez-vous pour enregistrer le don.</p>
          )}
          <p className="avertissement">
            Aide à la décision fondée sur des critères indicatifs. La décision finale revient au médecin de l'établissement.
          </p>
        </div>
      )}
    </div>
  );
}