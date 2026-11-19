import { useEffect, useState } from "react";
import api from "../api";
import { messageErreur } from "../utils";

const STATUTS = {
  en_attente: "En attente de validation",
  valide: "Établissement validé",
  refuse: "Inscription refusée",
};

export default function Profil() {
  const [etab, setEtab] = useState(null);
  const [form, setForm] = useState({ nom: "", ville: "" });
  const [erreur, setErreur] = useState("");
  const [infoProfil, setInfoProfil] = useState("");
  const [erreurProfil, setErreurProfil] = useState("");
  const [mdp, setMdp] = useState({ ancien: "", nouveau: "", confirmation: "" });
  const [infoMdp, setInfoMdp] = useState("");
  const [erreurMdp, setErreurMdp] = useState("");

  useEffect(() => {
    api
      .get("/etablissements/me/")
      .then((r) => {
        setEtab(r.data);
        setForm({ nom: r.data.nom, ville: r.data.ville });
      })
      .catch((err) => setErreur(messageErreur(err)));
  }, []);

  const enregistrerProfil = async (e) => {
    e.preventDefault();
    setInfoProfil("");
    setErreurProfil("");
    try {
      const { data } = await api.patch("/etablissements/me/", form);
      setEtab(data);
      setInfoProfil("Informations enregistrées.");
    } catch (err) {
      setErreurProfil(messageErreur(err));
    }
  };

  const changerMotDePasse = async (e) => {
    e.preventDefault();
    setInfoMdp("");
    setErreurMdp("");
    if (mdp.nouveau.length < 8) {
      setErreurMdp("Le nouveau mot de passe doit contenir au moins 8 caractères.");
      return;
    }
    if (mdp.nouveau !== mdp.confirmation) {
      setErreurMdp("La confirmation ne correspond pas au nouveau mot de passe.");
      return;
    }
    try {
      const { data } = await api.post("/auth/mot-de-passe/", {
        ancien: mdp.ancien,
        nouveau: mdp.nouveau,
      });
      localStorage.setItem("token", data.token);
      setMdp({ ancien: "", nouveau: "", confirmation: "" });
      setInfoMdp("Mot de passe modifié.");
    } catch (err) {
      setErreurMdp(messageErreur(err));
    }
  };

  if (erreur) return <p className="alerte">{erreur}</p>;
  if (!etab) return <p>Chargement...</p>;

  return (
    <>
      <h2>Mon profil</h2>
      <div className="listes">
        <div className="card">
          <h3>Informations de l'établissement</h3>
          <form onSubmit={enregistrerProfil}>
            <label>Nom de l'établissement</label>
            <input value={form.nom} onChange={(e) => setForm({ ...form, nom: e.target.value })} required />
            <label>Ville</label>
            <input value={form.ville} onChange={(e) => setForm({ ...form, ville: e.target.value })} required />
            <p className="aide">La ville détermine quels donneurs sont alertés pour vos demandes.</p>
            <label>E-mail du compte</label>
            <input value={etab.email} disabled />
            <p style={{ margin: "12px 0 0" }}>
              <span className={`badge ${etab.statut_validation}`}>{STATUTS[etab.statut_validation]}</span>
            </p>
            {erreurProfil && <p className="erreur">{erreurProfil}</p>}
            {infoProfil && <p className="info">{infoProfil}</p>}
            <button type="submit">Enregistrer</button>
          </form>
        </div>

        <div className="card">
          <h3>Changer le mot de passe</h3>
          <form onSubmit={changerMotDePasse}>
            <label>Mot de passe actuel</label>
            <input type="password" value={mdp.ancien}
                   onChange={(e) => setMdp({ ...mdp, ancien: e.target.value })} required />
            <label>Nouveau mot de passe (8 caractères minimum)</label>
            <input type="password" value={mdp.nouveau}
                   onChange={(e) => setMdp({ ...mdp, nouveau: e.target.value })} required />
            <label>Confirmer le nouveau mot de passe</label>
            <input type="password" value={mdp.confirmation}
                   onChange={(e) => setMdp({ ...mdp, confirmation: e.target.value })} required />
            {erreurMdp && <p className="erreur">{erreurMdp}</p>}
            {infoMdp && <p className="info">{infoMdp}</p>}
            <button type="submit">Modifier le mot de passe</button>
          </form>
        </div>
      </div>
    </>
  );
}