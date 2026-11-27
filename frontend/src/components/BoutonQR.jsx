import { useEffect, useState } from "react";
import api from "../api";

export default function BoutonQR({ id }) {
  const [ouvert, setOuvert] = useState(false);
  const [url, setUrl] = useState("");
  const [erreur, setErreur] = useState("");

  useEffect(() => () => { if (url) URL.revokeObjectURL(url); }, [url]);

  const afficher = async () => {
    setErreur("");
    try {
      const { data } = await api.get(`/rendez-vous/${id}/qr/`, { responseType: "blob" });
      setUrl(URL.createObjectURL(data));
      setOuvert(true);
    } catch {
      setErreur("Code QR indisponible.");
    }
  };

  return (
    <>
      <button className="btn-sec" onClick={afficher}>Voir le QR</button>
      {erreur && <span className="erreur">{erreur}</span>}
      {ouvert && (
        <div className="fond-modal" onClick={() => setOuvert(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Code QR du rendez-vous</h3>
            <img src={url} alt="Code QR du rendez-vous" width="260" height="260" />
            <p className="aide">
              Le donneur le présente à son arrivée. Vérifiez-le avec « Vérifier un code QR ».
            </p>
            <a href={url} download={`qr-rendez-vous-${id}.png`} className="btn-petit">Télécharger</a>
            <button onClick={() => setOuvert(false)}>Fermer</button>
          </div>
        </div>
      )}
    </>
  );
}