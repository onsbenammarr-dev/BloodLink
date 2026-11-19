import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api";
import AuthShell from "../components/AuthShell";
import { ESPACES, messageErreur } from "../utils";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [erreur, setErreur] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const message = sessionStorage.getItem("message");
    if (message) {
      setErreur(message);
      sessionStorage.removeItem("message");
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErreur("");
    try {
      const { data } = await api.post("/auth/login/", { email, password });
      localStorage.setItem("token", data.token);
      localStorage.setItem("role", data.role);
      navigate(ESPACES[data.role] || "/");
    } catch (err) {
      setErreur(messageErreur(err));
    }
  };

  return (
    <AuthShell>
      <h1>Bon retour parmi nous</h1>
      <p className="sous">Connectez-vous à votre espace.</p>
      <form onSubmit={handleSubmit}>
        <label>E-mail</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label>Mot de passe</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        {erreur && <p className="erreur">{erreur}</p>}
        <button type="submit">Se connecter</button>
      </form>
      <p className="bas">
        Pas encore de compte ? <Link to="/register">Créer un compte</Link>
      </p>
    </AuthShell>
  );
}