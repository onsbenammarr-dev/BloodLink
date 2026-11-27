import { etiquetteJour } from "../utils";

export default function GraphiquePrevision({ historique, jours, total }) {
  const valeurs = [...historique.valeurs, ...total];
  const max = Math.max(...valeurs, 1);
  const L = 700, H = 220, bas = 185, haut = 22;
  const pas = L / valeurs.length;
  const largeur = pas * 0.62;
  const n = historique.valeurs.length;

  return (
    <>
      <svg viewBox={`0 0 ${L} ${H}`} width="100%" role="img"
           aria-label="Demandes des 14 derniers jours et prévision des 7 prochains jours">
        <line x1="0" y1={bas} x2={L} y2={bas} stroke="#f0d9d6" />
        {valeurs.map((v, i) => {
          const prevu = i >= n;
          const h = (v / max) * (bas - haut);
          const x = i * pas + (pas - largeur) / 2;
          return (
            <g key={i}>
              <rect x={x} y={bas - h} width={largeur} height={h} rx="4"
                    fill={prevu ? "#c62828" : "#e3c9c6"} />
              {prevu && (
                <>
                  <text x={x + largeur / 2} y={bas - h - 5} fontSize="11" textAnchor="middle" fill="#2a1215">
                    {Math.round(v)}
                  </text>
                  <text x={x + largeur / 2} y={bas + 15} fontSize="10" textAnchor="middle" fill="#6b5457">
                    {etiquetteJour(jours[i - n])}
                  </text>
                </>
              )}
            </g>
          );
        })}
      </svg>
      <div className="legende">
        <span><i style={{ background: "#e3c9c6" }} />14 derniers jours</span>
        <span><i style={{ background: "#c62828" }} />Prévision des 7 prochains jours</span>
      </div>
    </>
  );
}