import { Link, Navigate, useNavigate } from "react-router-dom";

export default function EspaceAutre() {
  const navigate = useNavigate();
  const role = localStorage.getItem("role");

  if (!localStorage.getItem("token")) return <Navigate to="/login" />;

  const admin = role === "admin";

  const logout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <div className="card auth">
      <h2>{admin ? "Espace administrateur" : "Espace donneur"}</h2>
      <p>
        {admin
          ? "Bienvenue. Validez les inscriptions des établissements depuis l'interface de gestion."
          : "Bienvenue sur BloodLink. Vous recevrez par e-mail les demandes compatibles avec votre groupe sanguin et votre ville."}
      </p>
      {admin && (
        <a className="btn-petit" href="http://127.0.0.1:8000/admin/" target="_blank" rel="noreferrer">
          Ouvrir la gestion des établissements
        </a>
      )}
      <p style={{ marginTop: 16 }}>
        <Link to="/">Retour à l'accueil</Link>
      </p>
      <button onClick={logout}>Déconnexion</button>
    </div>
  );
}