import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import BoutonQR from "../components/BoutonQR";
import VerifierQR from "../components/VerifierQR";
import { DECISIONS, STATUTS_RDV, fmt, messageErreur } from "../utils";

const ONGLETS = [
  ["a_confirmer", "À confirmer", (r) => r.statut === "propose"],
  ["confirmes", "Confirmés", (r) => r.statut === "confirme"],
  ["historique", "Historique", (r) => r.statut === "realise" || r.statut === "annule"],
];

export default function RendezVous() {
  const [rdvs, setRdvs] = useState(null);
  const [onglet, setOnglet] = useState("a_confirmer");
  const [erreur, setErreur] = useState("");

  const charger = () =>
    api
      .get("/rendez-vous/")
      .then((r) => setRdvs(r.data))
      .catch((err) => setErreur(messageErreur(err)));

  useEffect(() => {
    charger();
  }, []);

  const agir = async (id, action) => {
    setErreur("");
    try {
      await api.post(`/rendez-vous/${id}/${action}/`);
      charger();
    } catch (err) {
      setErreur(messageErreur(err));
    }
  };

  const enregistrerDon = async (r) => {
    setErreur("");
    try {
      await api.post("/dons/", { donneur: r.donneur, demande: r.demande, rendez_vous: r.id });
      charger();
    } catch (err) {
      setErreur(messageErreur(err));
    }
  };

  if (!rdvs) return erreur ? <p className="alerte">{erreur}</p> : <p>Chargement...</p>;

  const filtre = ONGLETS.find((o) => o[0] === onglet)[2];
  const liste = rdvs.filter(filtre);

  return (
    <>
      <h2>Rendez-vous</h2>
      <VerifierQR />
      <div className="onglets filtres">
        {ONGLETS.map(([cle, titre, test]) => (
          <button key={cle} className={onglet === cle ? "actif" : ""} onClick={() => setOnglet(cle)}>
            {titre} ({rdvs.filter(test).length})
          </button>
        ))}
      </div>
      {erreur && <p className="erreur">{erreur}</p>}
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Donneur</th>
              <th>Groupe</th>
              <th>Date et heure</th>
              <th>Pré-don</th>
              <th>Statut</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {liste.map((r) => (
              <tr key={r.id}>
                <td>{r.donneur_email}</td>
                <td><strong>{r.groupe_sanguin}</strong></td>
                <td>{fmt(r.date_heure)}</td>
                
                <td><span className={`badge ${r.statut}`}>{STATUTS_RDV[r.statut]}</span></td>
                <td className="actions">
                  {(r.statut === "confirme" || r.statut === "realise") && <BoutonQR id={r.id} />}
                  {r.statut === "propose" && (
                    <>
                      <button onClick={() => agir(r.id, "confirmer")}>Confirmer</button>
                      <button className="btn-sec" onClick={() => agir(r.id, "annuler")}>Refuser</button>
                    </>
                  )}
                  
                </td>
              </tr>
            ))}
            {liste.length === 0 && (
              <tr><td colSpan="6" className="vide">Aucun rendez-vous dans cette liste.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}