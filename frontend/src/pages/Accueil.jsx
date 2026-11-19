import { Link } from "react-router-dom";
import Logo from "../components/Logo";

const Icone = ({ children }) => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor"
       strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    {children}
  </svg>
);

const BARRES = [26, 40, 34, 58, 46, 30, 38];

export default function Accueil() {
  return (
    <>
      <header className="hero-wrap">
        <div>
          <span className="tag">Don de sang · Urgences</span>
          <h1>
            Le bon sang, au bon endroit, <span className="rouge">au bon moment.</span>
          </h1>
          <p className="lead">
            BloodLink relie les établissements de santé aux donneurs compatibles de leur ville,
            en quelques clics.
          </p>
          <div className="actions-hero">
            <Link to="/register" className="btn-plein">Devenir donneur</Link>
            <Link to="/register" className="btn-contour">Je suis un établissement</Link>
          </div>
        </div>

        <div className="bento">
          <div className="tuile t-urgent">
            <span className="mini">DEMANDE URGENTE</span>
            <div>
              <div className="gros">A+</div>
              <p>2 poches · Kélibia<br />dans les 6 heures</p>
            </div>
          </div>
          <div className="tuile t-blanc">
            <span className="icone-rouge">
              <Icone>
                <path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z" />
                <circle cx="12" cy="10" r="2.5" />
              </Icone>
            </span>
            <h3>Même ville</h3>
            <p>Seuls les donneurs proches sont alertés.</p>
          </div>
          <div className="tuile t-rose">
            <span className="icone-rouge">
              <Icone>
                <rect x="3" y="5" width="18" height="16" rx="2" />
                <path d="M3 10h18M8 3v4M16 3v4" />
              </Icone>
            </span>
            <h3>Rendez-vous en ligne</h3>
            <p>Le donneur réserve son créneau.</p>
          </div>
          <div className="tuile t-large t-sombre">
            <div>
              <h3>Prévision de la demande</h3>
              <p>Anticipez les besoins par groupe sanguin.</p>
            </div>
            <svg width="250" height="80" viewBox="0 0 250 80" role="img" aria-label="Graphique illustratif">
              {BARRES.map((h, i) => (
                <rect key={i} x={10 + i * 34} y={70 - h} width="22" height={h} rx="6"
                      fill={i === 3 ? "#fff" : "#e08a8a"} />
              ))}
            </svg>
          </div>
        </div>
      </header>

      <section className="section">
        <h2>Comment ça marche</h2>
        <div className="etapes">
          <div>
            <span className="num">1</span>
            <h3>L'alerte</h3>
            <p>Un établissement publie sa demande urgente.</p>
          </div>
          <div>
            <span className="num">2</span>
            <h3>Les donneurs</h3>
            <p>Les donneurs compatibles reçoivent un e-mail.</p>
          </div>
          <div>
            <span className="num">3</span>
            <h3>Le don</h3>
            <p>Le donneur réserve, l'établissement confirme.</p>
          </div>
        </div>
      </section>

      <section className="section aud">
        <div className="carte-aud">
          <h3>Donneur</h3>
          <p>Créez votre compte gratuitement : vous pouvez vous connecter tout de suite.</p>
          <Link to="/register" className="btn-plein">Devenir donneur</Link>
        </div>
        <div className="carte-aud sombre">
          <h3>Établissement de santé</h3>
          <p>Publiez, suivez et confirmez. Votre compte est activé après validation par l'administrateur.</p>
          <Link to="/register" className="btn-blanc">Inscrire mon établissement</Link>
        </div>
      </section>

      <section className="section">
        <div className="bandeau">
          <h2>Prêt à rejoindre BloodLink ?</h2>
          <Link to="/register" className="btn-blanc">Créer un compte</Link>
        </div>
      </section>

      <footer className="footer">
        <Logo size={18} /> BloodLink · Projet universitaire, ISET Kélibia · 2026
      </footer>
    </>
  );
}