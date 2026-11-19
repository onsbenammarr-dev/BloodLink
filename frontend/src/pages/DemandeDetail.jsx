import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../api";
import { STATUTS_DEMANDE, etatDemande, fmt, messageErreur } from "../utils";

export default function DemandeDetail() {
  const { id } = useParams();
  const [demande, setDemande] = useState(null);
  const [reponses, setReponses] = useState([]);
  const [erreur, setErreur] = useState("");

  useEffect(() => {
    Promise.all([api.get(`/demandes/${id}/`), api.get(`/demandes/${id}/reponses/`)])
      .then(([d, r]) => {
        setDemande(d.data);
        setReponses(r.data);
      })
      .catch((err) => setErreur(messageErreur(err)));
  }, [id]);

  if (erreur) return <p className="alerte">{erreur}</p>;
  if (!demande) return <p>Chargement...</p>;

  const tuiles = [
    ["Groupe sanguin", demande.groupe_sanguin, 32],
    ["Poches demandées", demande.quantite, 32],
    ["Date du don", fmt(demande.date_don), 18],
    ["Statut", STATUTS_DEMANDE[etatDemande(demande)], 22],
  ];

  return (
    <>
      <p><Link to="/demandes">← Retour aux demandes</Link></p>
      <h2>Demande à {demande.ville}</h2>
      <div className="grille">
        {tuiles.map(([titre, valeur, taille]) => (
          <div className="card stat" key={titre}>
            <span>{titre}</span>
            <strong style={{ fontSize: taille }}>{valeur}</strong>
          </div>
        ))}
      </div>
      <h3 style={{ marginTop: 24 }}>Donneurs ayant répondu ({reponses.length})</h3>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>E-mail</th>
              <th>Groupe</th>
              <th>Ville</th>
              <th>Répondu le</th>
            </tr>
          </thead>
          <tbody>
            {reponses.map((r) => (
              <tr key={r.id}>
                <td>{r.donneur_email}</td>
                <td>{r.groupe_sanguin}</td>
                <td>{r.ville}</td>
                <td>{fmt(r.date)}</td>
              </tr>
            ))}
            {reponses.length === 0 && (
              <tr><td colSpan="4" className="vide">Aucune réponse pour le moment.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}