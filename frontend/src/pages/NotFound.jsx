import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="card auth" style={{ textAlign: "center" }}>
      <h2>Page introuvable</h2>
      <p>La page que vous cherchez n'existe pas ou a été déplacée.</p>
      <Link to="/" className="btn-petit">Retour à l'accueil</Link>
    </div>
  );
}