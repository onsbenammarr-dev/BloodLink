import { useEffect, useState } from "react";
import api from "../api";
import Pagination from "../components/Pagination";
import { DEPISTAGES, fmt, messageErreur } from "../utils";

const PAR_PAGE = 10;

export default function Dons() {
  const [dons, setDons] = useState(null);
  const [recherche, setRecherche] = useState("");
  const [page, setPage] = useState(1);
  const [erreur, setErreur] = useState("");

  const charger = () =>
    api
      .get("/dons/")
      .then((r) => setDons(r.data))
      .catch((err) => setErreur(messageErreur(err)));

  useEffect(() => {
    charger();
  }, []);

  const changerDepistage = async (id, resultat) => {
    setErreur("");
    try {
      await api.post(`/dons/${id}/depistage/`, { resultat });
      charger();
    } catch (err) {
      setErreur(messageErreur(err));
    }
  };

  if (!dons) return erreur ? <p className="alerte">{erreur}</p> : <p>Chargement...</p>;

  const texte = recherche.trim().toLowerCase();
  const liste = dons.filter((d) => !texte || d.donneur_email.toLowerCase().includes(texte));
  const pages = Math.max(1, Math.ceil(liste.length / PAR_PAGE));
  const pageCourante = Math.min(page, pages);
  const visibles = liste.slice((pageCourante - 1) * PAR_PAGE, pageCourante * PAR_PAGE);

  return (
    <>
      <h2>Dons réalisés ({dons.length})</h2>
      <input
        className="recherche"
        type="search"
        placeholder="Rechercher un donneur (e-mail)"
        value={recherche}
        onChange={(e) => {
          setRecherche(e.target.value);
          setPage(1);
        }}
        aria-label="Rechercher un donneur"
      />
      {erreur && <p className="erreur">{erreur}</p>}
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Donneur</th>
              <th>Demande</th>
              <th>Date</th>
              <th>Dépistage biologique</th>
            </tr>
          </thead>
          <tbody>
            {visibles.map((d) => (
              <tr key={d.id}>
                <td>{d.donneur_email}</td>
                <td>{d.demande ? `#${d.demande}` : "-"}</td>
                <td>{fmt(d.date)}</td>
                <td>
                  <span className={`badge ${d.depistage}`}>{DEPISTAGES[d.depistage]}</span>{" "}
                  <select
                    className="petit"
                    value={d.depistage}
                    onChange={(e) => changerDepistage(d.id, e.target.value)}
                    aria-label="Résultat du dépistage"
                  >
                    {Object.entries(DEPISTAGES).map(([cle, lib]) => (
                      <option key={cle} value={cle}>{lib}</option>
                    ))}
                  </select>
                  {d.depistage === "non_conforme" && (
                    <div className="aide">
                      Poche écartée : orienter le donneur vers un suivi médical confidentiel.
                    </div>
                  )}
                </td>
              </tr>
            ))}
            {visibles.length === 0 && (
              <tr><td colSpan="4" className="vide">Aucun don ne correspond.</td></tr>
            )}
          </tbody>
        </table>
        <Pagination page={pageCourante} total={liste.length} parPage={PAR_PAGE} onChange={setPage} />
      </div>
    </>
  );
}