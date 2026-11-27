export const GROUPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];

export const fmt = (iso) => (iso ? new Date(iso).toLocaleString("fr-FR", {
  day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit",
}) : "-");

export const STATUTS_DEMANDE = {
  active: "Active",
  satisfaite: "Satisfaite",
  cloturee: "Clôturée",
  expiree: "Expirée",
};

export const STATUTS_RDV = {
  propose: "À confirmer",
  confirme: "Confirmé",
  annule: "Annulé",
  realise: "Réalisé",
};

export const ESPACES = {
  etablissement: "/tableau-de-bord",
  donneur: "/espace-donneur",
  admin: "/espace-admin",
};

export const etatDemande = (d) => (d.expiree ? "expiree" : d.statut);

export function pourInputDate(d) {
  const p = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`;
}

export function messageErreur(err) {
  const d = err.response?.data;
  if (!d) return "Service momentanément indisponible. Réessayez dans un instant.";
  if (typeof d === "string") return "Une erreur est survenue. Réessayez dans un instant.";
  if (d.detail) return d.detail;
  return Object.values(d).flat().join(" ");
}
export const DECISIONS = {
  apte: "Apte au don",
  ajourne: "Ajourné",
  avis_medical: "Avis médical requis",
};

export const DEPISTAGES = {
  en_attente: "En attente",
  conforme: "Conforme",
  non_conforme: "Non conforme",
};

const JOURS_SEMAINE = ["dim", "lun", "mar", "mer", "jeu", "ven", "sam"];

export function etiquetteJour(iso) {
  const d = new Date(iso + "T00:00:00");
  return `${JOURS_SEMAINE[d.getDay()]} ${String(d.getDate()).padStart(2, "0")}`;
}