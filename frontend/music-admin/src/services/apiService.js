// Servicio base que contiene la configuración común para todas las peticiones API
import axios from "axios";

const API_DOMAIN = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const API_V1_PREFIX = "/api/v1"; 

const apiClient = axios.create({
  baseURL: API_DOMAIN, 
  headers: {
    "Content-Type": "application/json", 
  },
});

// Interceptor para añadir el token JWT a las cabeceras de las peticiones salientes
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("user-token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de respuesta para manejar errores 401 globalmente
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Si el token es inválido o expiró, limpiar y redirigir al login
      localStorage.removeItem("user-token");
      // Evitar bucles de redirección si ya estamos en login
      if (window.location.pathname !== '/login' && window.location.pathname !== '/') {
          window.location.href = '/login?session_expired=true'; 
      }
    }
    return Promise.reject(error);
  }
);

export { apiClient, API_V1_PREFIX };
