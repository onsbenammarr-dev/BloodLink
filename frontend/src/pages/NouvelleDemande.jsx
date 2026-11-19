import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { GROUPES, messageErreur, pourInputDate } from "../utils";

const dansHeures = (h) => new Date(Date.now() + h * 3600 * 1000);

export default function NouvelleDemande() {
  const [form, setForm] = useState({
    groupe_sanguin: "O+",
    quantite: 1,
    ville: "",
    date_don: pourInputDate(dansHeures(24)),
  });
  const [erreur, setErreur] = useState("");
  const [info, setInfo] = useState("");
  const [envoi, setEnvoi] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    api
      .get("/etablissements/me/")
      .then((r) => setForm((f) => ({ ...f, ville: r.data.ville })))
      .catch(() => {});
  }, []);

  const change = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErreur("");
    setInfo("");
    const date = new Date(form.date_don);
    if (isNaN(date) || date <= new Date()) {
      setErreur("Choisissez une date et une heure de don dans le futur.");
      return;
    }
    setEnvoi(true);
    try {
      const { data } = await api.post("/demandes/", {
        groupe_sanguin: form.groupe_sanguin,
        quantite: Number(form.quantite),
        ville: form.ville,
        date_don: date.toISOString(),
      });
      setInfo(`Demande publiée : ${data.donneurs_alertes} donneur(s) compatible(s) alerté(s) par e-mail.`);
      setTimeout(() => navigate("/demandes"), 1500);
    } catch (err) {
      setErreur(messageErreur(err));
    } finally {
      setEnvoi(false);
    }
  };

  return (
    <div className="card auth">
      <h2>Nouvelle demande urgente</h2>
      <form onSubmit={handleSubmit}>
        <label>Groupe sanguin</label>
        <select name="groupe_sanguin" value={form.groupe_sanguin} onChange={change}>
          {GROUPES.map((g) => (
            <option key={g}>{g}</option>
          ))}
        </select>
        <label>Nombre de poches</label>
        <input name="quantite" type="number" min="1" max="20" value={form.quantite} onChange={change} required />
        <label>Ville</label>
        <input name="ville" value={form.ville} onChange={change} required />
        <p className="aide">Seuls les donneurs compatibles de cette ville seront alertés.</p>
        <label>Date et heure du don</label>
        <input
          name="date_don"
          type="datetime-local"
          min={pourInputDate(new Date())}
          value={form.date_don}
          onChange={change}
          required
        />
        {erreur && <p className="erreur">{erreur}</p>}
        {info && <p className="info">{info}</p>}
        <button type="submit" disabled={envoi}>
          {envoi ? "Publication..." : "Publier la demande"}
        </button>
      </form>
    </div>
  );
}