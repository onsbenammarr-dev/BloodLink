import { useState } from "react";
import api from "../api";
import { DECISIONS, STATUTS_RDV, fmt, messageErreur } from "../utils";

export default function VerifierQR() {
  const [code, setCode] = useState("");
  const [resultat, setResultat] = useState(null);
  const [erreur, setErreur] = useState("");

  const verifier = async (e) => {
    e.preventDefault();
    setErreur("");
    setResultat(null);
    try {
      const { data } = await api.get("/rendez-vous/verifier/", { params: { code } });
      setResultat(data);
    } catch (err) {
      setErreur(messageErreur(err));
    }
  };

  return (
    <div className="card" style={{ marginBottom: 16 }}>
      <h3 style={{ marginTop: 0 }}>Vérifier un code QR</h3>
      <form onSubmit={verifier} className="ligne-verif">
        <input
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Collez la référence (BL-12-AB12CD34) ou le texte lu dans le QR"
          required
        />
        <button type="submit">Vérifier</button>
      </form>
      {erreur && <p className="erreur">{erreur}</p>}
      {resultat && (
        <div className="resultat apte">
          <h3>Code valide : {resultat.donneur}</h3>
          <ul>
            <li>Groupe sanguin : <strong>{resultat.groupe_sanguin}</strong></li>
            <li>Téléphone : {resultat.telephone || "-"} | E-mail : {resultat.email}</li>
            <li>Rendez-vous : {fmt(resultat.date_heure)} ({STATUTS_RDV[resultat.statut]})</li>
            <li>
              Pré-don :{" "}
              {resultat.decision_predon ? DECISIONS[resultat.decision_predon] : "pas encore réalisé"}
            </li>
          </ul>
          <p className="avertissement">Référence {resultat.reference}</p>
        </div>
      )}
    </div>
  );
}