import axios from "axios";
import { cerrarSesion, verificarAutenticacion } from '@/utils/authUtils';

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
      console.log('Error 401: Token inválido o expirado');
      // Usar la función centralizada para cerrar sesión
      cerrarSesion();
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
    cerrarSesion();
  },

  getToken() {
    return localStorage.getItem("user-token");
  },

  saveToken(token) {
    localStorage.setItem("user-token", token);
  },

  isAuthenticated() {
    return verificarAutenticacion();
  },

  async getCurrentUser() {
    if (!this.isAuthenticated()) {
      return Promise.reject(new Error("Usuario no autenticado."));
    }
    // Endpoint: GET /api/v1/auth/users/me/
    return apiClient.get(`${API_V1_PREFIX}/auth/users/me/`);
  },
  
  async isAdmin() {
    try {
      const response = await this.getCurrentUser();
      return response.data.rol_plataforma === 'admin';
    } catch (error) {
      console.error('Error verificando si el usuario es administrador:', error);
      return false;
    }
  },
};