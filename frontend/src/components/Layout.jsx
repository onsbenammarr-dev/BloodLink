import { Link, Navigate, Outlet, useNavigate } from "react-router-dom";
import Logo from "./Logo";

export default function Layout() {
  const navigate = useNavigate();

  if (!localStorage.getItem("token")) return <Navigate to="/login" />;
  if (localStorage.getItem("role") !== "etablissement") return <Navigate to="/" />;

  const logout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <>
      <div className="topbar">
        <nav className="nav">
          <Link to="/" className="brand"><Logo />BloodLink</Link>
          <Link to="/tableau-de-bord">Tableau de bord</Link>
          <Link to="/demandes/nouvelle">Nouvelle demande</Link>
          <Link to="/demandes">Demandes</Link>
          <Link to="/rendez-vous">Rendez-vous</Link>
          <Link to="/dons">Dons</Link>
          <Link to="/relances">Relances</Link>
          <Link to="/previsions">Prévisions</Link>
          <span className="spacer" />
          <Link to="/profil">Mon profil</Link>
          <button onClick={logout}>Déconnexion</button>
        </nav>
      </div>
      <main className="container">
        <Outlet />
      </main>
    </>
  );
}