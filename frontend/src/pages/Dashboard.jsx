import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import GraphiquePrevision from "../components/GraphiquePrevision";
import { STATUTS_RDV, fmt, messageErreur } from "../utils";

const STATUTS = {
  en_attente: "En attente de validation",
  valide: "Établissement validé",
  refuse: "Inscription refusée",
};

export default function Dashboard() {
  const [etab, setEtab] = useState(null);
  const [stats, setStats] = useState(null);
  const [prev, setPrev] = useState(null);
  const [erreur, setErreur] = useState("");

  useEffect(() => {
    Promise.all([api.get("/etablissements/me/"), api.get("/dashboard/")])
      .then(([a, b]) => {
        setEtab(a.data);
        setStats(b.data);
      })
      .catch((err) => setErreur(messageErreur(err)));
    api.get("/previsions/").then((r) => setPrev(r.data)).catch(() => {});
  }, []);

  if (erreur) return <p className="alerte">{erreur}</p>;
  if (!etab || !stats) return <p>Chargement...</p>;

  const cartes = [
    ["Demandes actives", stats.demandes_actives],
    ["Réponses reçues", stats.reponses_recues],
    ["Rendez-vous à confirmer", stats.rdv_a_confirmer],
    ["Dons réalisés", stats.dons_realises],
  ];

  return (
    <>
      <div className="entete">
        <div>
          <h2>{etab.nom}</h2>
          <span className={`badge ${etab.statut_validation}`}>
            {etab.ville} · {STATUTS[etab.statut_validation]}
          </span>
        </div>
        <Link to="/demandes/nouvelle" className="btn-petit">Nouvelle demande</Link>
      </div>

      <div className="grille">
        {cartes.map(([titre, valeur]) => (
          <div className="card stat" key={titre}>
            <span>{titre}</span>
            <strong>{valeur}</strong>
          </div>
        ))}
      </div>

      {prev && (
        <div className="card" style={{ marginTop: 16 }}>
          <div className="entete">
            <h3 style={{ margin: 0 }}>Prévision de la demande : 7 prochains jours</h3>
            <Link to="/previsions" className="lien-voir">Voir le détail</Link>
          </div>
          <GraphiquePrevision historique={prev.historique} jours={prev.jours} total={prev.total} />
        </div>
      )}

      <div className="listes">
        <div className="card">
          <h3>Demandes à surveiller</h3>
          <table>
            <thead>
              <tr><th>Groupe</th><th>Poches</th><th>Date du don</th><th>Réponses</th><th></th></tr>
            </thead>
            <tbody>
              {stats.demandes_recentes.map((d) => (
                <tr key={d.id}>
                  <td><strong>{d.groupe_sanguin}</strong></td>
                  <td>{d.quantite}</td>
                  <td>{fmt(d.date_don)}</td>
                  <td>{d.nb_reponses}</td>
                  <td><Link to={`/demandes/${d.id}`} className="lien-voir">Voir</Link></td>
                </tr>
              ))}
              {stats.demandes_recentes.length === 0 && (
                <tr><td colSpan="5" className="vide">Aucune demande en cours.</td></tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="card">
          <h3>Prochains rendez-vous</h3>
          <table>
            <thead>
              <tr><th>Donneur</th><th>Date et heure</th><th>Statut</th></tr>
            </thead>
            <tbody>
              {stats.rdv_a_venir.map((r) => (
                <tr key={r.id}>
                  <td>{r.donneur_email}</td>
                  <td>{fmt(r.date_heure)}</td>
                  <td><span className={`badge ${r.statut}`}>{STATUTS_RDV[r.statut]}</span></td>
                </tr>
              ))}
              {stats.rdv_a_venir.length === 0 && (
                <tr><td colSpan="3" className="vide">Aucun rendez-vous à venir.</td></tr>
              )}
            </tbody>
          </table>
          <p style={{ margin: "10px 0 0" }}>
            <Link to="/rendez-vous" className="lien-voir">Gérer les rendez-vous</Link>
          </p>
        </div>
      </div>
    </>
  );
}