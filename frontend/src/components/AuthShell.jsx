import { Link } from "react-router-dom";
import Logo from "./Logo";

const Ico = ({ children }) => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="1.8"
       strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    {children}
  </svg>
);

export default function AuthShell({ children }) {
  return (
    <div className="auth-page">
      <aside className="auth-side">
        <Link to="/" className="auth-logo"><Logo size={28} couleur="#ff8b8f" />BloodLink</Link>
        <h2>Rejoignez le réseau qui sauve des vies</h2>
        <ul>
          <li>
            <span className="pastille">
              <Ico><path d="M6 8a6 6 0 0 1 12 0c0 7 3 8 3 8H3s3-1 3-8" /><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0" /></Ico>
            </span>
            Alertes ciblées par groupe sanguin et par ville
          </li>
          <li>
            <span className="pastille">
              <Ico><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M3 10h18M8 3v4M16 3v4" /></Ico>
            </span>
            Rendez-vous de don réservés en ligne
          </li>
          <li>
            <span className="pastille">
              <Ico><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z" /></Ico>
            </span>
            Établissements validés par un administrateur
          </li>
        </ul>
      </aside>
      <div className="auth-main">
        <div className="auth-card">{children}</div>
      </div>
    </div>
  );
}