import { useEffect, useState } from "react";
import api from "../api";
import GraphiquePrevision from "../components/GraphiquePrevision";
import { etiquetteJour, messageErreur } from "../utils";

export default function Prevision() {
  const [data, setData] = useState(null);
  const [erreur, setErreur] = useState("");

  useEffect(() => {
    api
      .get("/previsions/")
      .then((r) => setData(r.data))
      .catch((err) => setErreur(messageErreur(err)));
  }, []);

  if (erreur) return <p className="alerte">{erreur}</p>;
  if (!data) return <p>Chargement...</p>;

  const maxCellule = Math.max(...Object.values(data.groupes).flat(), 0.1);

  return (
    <>
      <h2>Prévision de la demande</h2>
      <p className="note-ml">
        Prévisions calculées à partir d'un jeu de données synthétique (démonstration).
      </p>

      <div className="cartes-ml">
        <div className="card"><span>Modèle retenu</span><strong>{data.modele}</strong></div>
        <div className="card">
          <span>Erreur moyenne (MAE)</span>
          <strong>{data.mae} demande/jour/groupe</strong>
        </div>
        <div className="card">
          <span>Référence (moyenne 7 jours)</span>
          <strong>{data.mae_reference}</strong>
        </div>
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>Demandes totales : passé et prévision</h3>
        <GraphiquePrevision historique={data.historique} jours={data.jours} total={data.total} />
      </div>

      <div className="card" style={{ marginTop: 16, overflowX: "auto" }}>
        <h3 style={{ marginTop: 0 }}>Prévision par groupe sanguin</h3>
        <table>
          <thead>
            <tr>
              <th>Groupe</th>
              {data.jours.map((j) => (
                <th key={j} className="cellule">{etiquetteJour(j)}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Object.entries(data.groupes).map(([groupe, valeurs]) => (
              <tr key={groupe}>
                <td><strong>{groupe}</strong></td>
                {valeurs.map((v, i) => (
                  <td
                    key={i}
                    className="cellule"
                    style={{ background: `rgba(198, 40, 40, ${Math.min(0.55, (v / maxCellule) * 0.55)})` }}
                  >
                    {v.toFixed(1)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <details className="card" style={{ marginTop: 16 }}>
        <summary><strong>Comment la prévision est calculée</strong></summary>
        <ul>
          <li>Données : nombre de demandes par jour et par groupe sanguin (jeu synthétique).</li>
          <li>Caractéristiques : jour de la semaine, groupe, demandes de la veille, d'il y a 7 jours, moyennes sur 7 et 14 jours.</li>
          <li>Modèles comparés : régression linéaire et forêt aléatoire (Scikit-learn).</li>
          <li>Évaluation : erreur absolue moyenne sur les 60 derniers jours, jamais vus à l'entraînement.</li>
          <li>Prévision sur 7 jours : jour après jour, chaque prévision alimente la suivante.</li>
        </ul>
      </details>
    </>
  );
}