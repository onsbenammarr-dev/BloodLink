import { Link, Outlet } from "react-router-dom";
import Logo from "./Logo";
import { ESPACES } from "../utils";

export default function PublicLayout() {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  return (
    <>
      <div className="topbar">
        <nav className="nav">
          <Link to="/" className="brand"><Logo />BloodLink</Link>
          <span className="spacer" />
          {token ? (
            <Link to={ESPACES[role] || "/"} className="cta">Mon espace</Link>
          ) : (
            <>
              <Link to="/login">Connexion</Link>
              <Link to="/register" className="cta">Créer un compte</Link>
            </>
          )}
        </nav>
      </div>
      <Outlet />
    </>
  );
}