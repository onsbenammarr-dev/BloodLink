import { useEffect, useState } from "react";
import api from "../api";
import { fmt, messageErreur } from "../utils";

export default function Relances() {
  const [data, setData] = useState(null);
  const [erreur, setErreur] = useState("");

  useEffect(() => {
    api
      .get("/donneurs-a-relancer/")
      .then((r) => setData(r.data))
      .catch((err) => setErreur(messageErreur(err)));
  }, []);

  if (erreur) return <p className="alerte">{erreur}</p>;
  if (!data) return <p>Chargement...</p>;

  return (
    <>
      <h2>Donneurs à relancer</h2>
      <p className="note-ml">
        Probabilité qu'un donneur revienne dans le mois, estimée par un modèle entraîné sur des données
        réelles ({data.source}). Elle sert à prioriser les relances, pas à décider.
      </p>

      <div className="cartes-ml">
        <div className="card"><span>Modèle</span><strong>{data.modele}</strong></div>
        <div className="card"><span>AUC sur donneurs de test</span><strong>{data.auc}</strong></div>
        <div className="card">
          <span>Précision (référence : {data.precision_reference})</span>
          <strong>{data.precision}</strong>
        </div>
      </div>

      <div className="card" style={{ overflowX: "auto" }}>
        <table>
          <thead>
            <tr>
              <th>Donneur</th>
              <th>Groupe</th>
              <th>Dons</th>
              <th>Dernier don</th>
              <th>Probabilité de retour</th>
              <th>Statut</th>
            </tr>
          </thead>
          <tbody>
            {data.donneurs.map((d) => (
              <tr key={d.email}>
                <td>{d.email}</td>
                <td><strong>{d.groupe_sanguin}</strong></td>
                <td>{d.nb_dons}</td>
                <td>{fmt(d.dernier_don)}</td>
                <td>
                  <div className="barre"><span style={{ width: `${Math.round(d.probabilite * 100)}%` }} /></div>
                  {Math.round(d.probabilite * 100)} %
                </td>
                <td>
                  <span className={`badge ${d.eligible ? "confirme" : "propose"}`}>
                    {d.eligible ? "Éligible" : "Trop récent"}
                  </span>
                </td>
              </tr>
            ))}
            {data.donneurs.length === 0 && (
              <tr><td colSpan="6" className="vide">Aucun donneur n'a encore donné dans votre établissement.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}