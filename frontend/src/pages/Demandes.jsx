import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import Pagination from "../components/Pagination";
import { STATUTS_DEMANDE, etatDemande, fmt, messageErreur } from "../utils";

const PAR_PAGE = 8;

export default function Demandes() {
  const [demandes, setDemandes] = useState(null);
  const [filtre, setFiltre] = useState("actives");
  const [recherche, setRecherche] = useState("");
  const [page, setPage] = useState(1);
  const [erreur, setErreur] = useState("");

  const charger = () =>
    api
      .get("/demandes/")
      .then((r) => setDemandes(r.data))
      .catch((err) => setErreur(messageErreur(err)));

  useEffect(() => {
    charger();
  }, []);

  const cloturer = async (id) => {
    if (!window.confirm("Clôturer cette demande ? Les donneurs ne pourront plus y répondre.")) return;
    try {
      await api.post(`/demandes/${id}/cloturer/`);
      charger();
    } catch (err) {
      setErreur(messageErreur(err));
    }
  };

  if (erreur && !demandes) return <p className="alerte">{erreur}</p>;
  if (!demandes) return <p>Chargement...</p>;

  const enCours = (d) => d.statut === "active" && !d.expiree;
  const texte = recherche.trim().toLowerCase();
  const liste = demandes
    .filter((d) => (filtre === "toutes" ? true : filtre === "actives" ? enCours(d) : !enCours(d)))
    .filter(
      (d) =>
        !texte ||
        `${d.groupe_sanguin} ${d.ville} ${STATUTS_DEMANDE[etatDemande(d)]}`.toLowerCase().includes(texte)
    );
  const pages = Math.max(1, Math.ceil(liste.length / PAR_PAGE));
  const pageCourante = Math.min(page, pages);
  const visibles = liste.slice((pageCourante - 1) * PAR_PAGE, pageCourante * PAR_PAGE);

  const choisir = (f) => {
    setFiltre(f);
    setPage(1);
  };

  return (
    <>
      <div className="entete">
        <h2>Mes demandes</h2>
        <Link to="/demandes/nouvelle" className="btn-petit">Nouvelle demande</Link>
      </div>
      <div className="onglets filtres">
        <button className={filtre === "actives" ? "actif" : ""} onClick={() => choisir("actives")}>
          En cours ({demandes.filter(enCours).length})
        </button>
        <button className={filtre === "terminees" ? "actif" : ""} onClick={() => choisir("terminees")}>
          Terminées
        </button>
        <button className={filtre === "toutes" ? "actif" : ""} onClick={() => choisir("toutes")}>
          Toutes
        </button>
      </div>
      <input
        className="recherche"
        type="search"
        placeholder="Rechercher (groupe, ville, statut)"
        value={recherche}
        onChange={(e) => {
          setRecherche(e.target.value);
          setPage(1);
        }}
        aria-label="Rechercher une demande"
      />
      {erreur && <p className="erreur">{erreur}</p>}
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Groupe</th>
              <th>Poches</th>
              <th>Ville</th>
              <th>Date du don</th>
              <th>Statut</th>
              <th>Réponses</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {visibles.map((d) => (
              <tr key={d.id}>
                <td><strong>{d.groupe_sanguin}</strong></td>
                <td>{d.quantite}</td>
                <td>{d.ville}</td>
                <td>{fmt(d.date_don)}</td>
                <td>
                  <span className={`badge ${etatDemande(d)}`}>{STATUTS_DEMANDE[etatDemande(d)]}</span>
                </td>
                <td>{d.nb_reponses}</td>
                <td className="actions">
                  <Link to={`/demandes/${d.id}`} className="lien-voir">Voir</Link>
                  {enCours(d) && (
                    <button className="btn-sec" onClick={() => cloturer(d.id)}>Clôturer</button>
                  )}
                </td>
              </tr>
            ))}
            {visibles.length === 0 && (
              <tr><td colSpan="7" className="vide">Aucune demande ne correspond.</td></tr>
            )}
          </tbody>
        </table>
        <Pagination page={pageCourante} total={liste.length} parPage={PAR_PAGE} onChange={setPage} />
      </div>
    </>
  );
}