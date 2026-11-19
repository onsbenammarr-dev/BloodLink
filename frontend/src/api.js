import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Token ${token}`;
  return config;
});

api.interceptors.response.use(
  (reponse) => reponse,
  (err) => {
    const url = err.config?.url || "";
    if (err.response?.status === 401 && !url.includes("/auth/login")) {
      localStorage.clear();
      sessionStorage.setItem("message", "Votre session a expiré. Veuillez vous reconnecter.");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export default api;