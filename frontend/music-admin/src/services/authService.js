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


export default {
  async register(userData) {
    // userData = { email: '...', password: '...', nombre: '...' }
    // Endpoint: POST /api/v1/usuarios/
    return apiClient.post(`${API_V1_PREFIX}/usuarios/`, userData);
  },

  async login(credentials) {
    // credentials = { email: '...', password: '...' }
    // Endpoint: POST /api/v1/auth/token
    const formData = new FormData();
    formData.append("username", credentials.email); // FastAPI espera 'username' para el email aquí
    formData.append("password", credentials.password);

    // Construir la URL completa incluyendo el prefijo de la API
    return apiClient.post(`${API_V1_PREFIX}/auth/token`, formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded", // Necesario para OAuth2PasswordRequestForm
      },
    });
  },

  logout() {
    localStorage.removeItem("user-token");
  },

  getToken() {
    return localStorage.getItem("user-token");
  },

  saveToken(token) {
    localStorage.setItem("user-token", token);
  },

  isAuthenticated() {
    const token = this.getToken();
    if (!token) {
      return false;
    }
    // TODO: decodificar el JWT aquí y verificar la fecha de expiración (campo 'exp') jwt-decode.

    return true;
  },

  async getCurrentUser() {
    if (!this.isAuthenticated()) {
      return Promise.reject(new Error("Usuario no autenticado."));
    }
    // Endpoint: GET /api/v1/auth/users/me/
    return apiClient.get(`${API_V1_PREFIX}/auth/users/me/`);
  },
};