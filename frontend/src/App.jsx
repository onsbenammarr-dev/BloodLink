import { Navigate, Route, Routes } from "react-router-dom";
import PublicLayout from "./components/PublicLayout";
import Layout from "./components/Layout";
import Accueil from "./pages/Accueil";
import Login from "./pages/Login";
import Register from "./pages/Register";
import EspaceAutre from "./pages/EspaceAutre";
import NotFound from "./pages/NotFound";
import Dashboard from "./pages/Dashboard";
import NouvelleDemande from "./pages/NouvelleDemande";
import Demandes from "./pages/Demandes";
import DemandeDetail from "./pages/DemandeDetail";
import RendezVous from "./pages/RendezVous";
import Dons from "./pages/Dons";
import Profil from "./pages/Profil";
import Relances from "./pages/Relances";
import Prevision from "./pages/Prevision";
export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<PublicLayout />}>
        <Route path="/" element={<Accueil />} />
        <Route path="*" element={<NotFound />} />
      </Route>

      <Route path="/espace-donneur" element={<EspaceAutre />} />
      <Route path="/espace-admin" element={<EspaceAutre />} />

      <Route element={<Layout />}>
      <Route path="/relances" element={<Relances />} />
        <Route path="/tableau-de-bord" element={<Dashboard />} />
        <Route path="/demandes/nouvelle" element={<NouvelleDemande />} />
        <Route path="/demandes" element={<Demandes />} />
        <Route path="/demandes/:id" element={<DemandeDetail />} />
        <Route path="/rendez-vous" element={<RendezVous />} />
        <Route path="/dons" element={<Dons />} />
        <Route path="/previsions" element={<Prevision />} />
        <Route path="/profil" element={<Profil />} />
      </Route>

      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}