import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import AuthShell from "../components/AuthShell";
import { GROUPES, messageErreur } from "../utils";

export default function Register() {
  const [type, setType] = useState("donneur");
  const [form, setForm] = useState({
    email: "", password: "", nom: "", prenom: "", telephone: "", ville: "", groupe_sanguin: "O+",
  });
  const [erreur, setErreur] = useState("");
  const [ok, setOk] = useState("");

  const change = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErreur("");
    const donneur = type === "donneur";
    const url = donneur ? "/donneurs/register/" : "/etablissements/register/";
    const payload = donneur
      ? {
          email: form.email, password: form.password, groupe_sanguin: form.groupe_sanguin,
          ville: form.ville, prenom: form.prenom, nom: form.nom, telephone: form.telephone,
        }
      : { email: form.email, password: form.password, nom: form.nom, ville: form.ville };
    try {
      await api.post(url, payload);
      setOk(type);
    } catch (err) {
      setErreur(messageErreur(err));
    }
  };

  if (ok)
    return (
      <AuthShell>
        <h1>{ok === "donneur" ? "Compte créé" : "Inscription envoyée"}</h1>
        <p className="sous">
          {ok === "donneur"
            ? "Votre compte donneur est prêt. Vous pouvez vous connecter dès maintenant."
            : "Votre établissement doit être validé par l'administrateur. Vous pourrez vous connecter une fois votre compte activé."}
        </p>
        <p className="bas"><Link to="/login">Aller à la connexion</Link></p>
      </AuthShell>
    );

  return (
    <AuthShell>
      <h1>Créer un compte</h1>
      <p className="sous">Choisissez votre profil.</p>
      <div className="onglets">
        <button type="button" className={type === "donneur" ? "actif" : ""} onClick={() => setType("donneur")}>
          Donneur
        </button>
        <button type="button" className={type === "etablissement" ? "actif" : ""} onClick={() => setType("etablissement")}>
          Établissement
        </button>
      </div>
      <form onSubmit={handleSubmit}>
        {type === "etablissement" && (
          <>
            <label>Nom de l'établissement</label>
            <input name="nom" value={form.nom} onChange={change} required />
          </>
        )}
        {type === "donneur" && (
          <>
            <label>Prénom</label>
            <input name="prenom" value={form.prenom} onChange={change} required />
            <label>Nom</label>
            <input name="nom" value={form.nom} onChange={change} required />
            <label>Téléphone</label>
            <input name="telephone" type="tel" placeholder="+216 20 123 456"
                   value={form.telephone} onChange={change} required />
            <label>Groupe sanguin</label>
            <select name="groupe_sanguin" value={form.groupe_sanguin} onChange={change}>
              {GROUPES.map((g) => <option key={g}>{g}</option>)}
            </select>
          </>
        )}
        <label>Ville</label>
        <input name="ville" value={form.ville} onChange={change} required />
        <label>E-mail</label>
        <input name="email" type="email" value={form.email} onChange={change} required />
        <label>Mot de passe (8 caractères minimum)</label>
        <input name="password" type="password" minLength={8} value={form.password} onChange={change} required />
        {type === "etablissement" && (
          <p className="info-box">Votre compte sera activé après validation par l'administrateur.</p>
        )}
        {erreur && <p className="erreur">{erreur}</p>}
        <button type="submit">Créer mon compte</button>
      </form>
      <p className="bas">
        Déjà inscrit ? <Link to="/login">Se connecter</Link>
      </p>
    </AuthShell>
  );
}