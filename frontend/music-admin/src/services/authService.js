// src/services/authService.js
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

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

export default {
  async register(userData) {
    // userData = { email: '...', password: '...', nombre: '...' }
    // Endpoint: POST /usuarios/
    return apiClient.post("/usuarios/", userData);
  },

  async login(credentials) {
    // credentials = { email: '...', password: '...' }
    // Endpoint: POST /auth/token
    const formData = new FormData();
    formData.append("username", credentials.email); // FastAPI espera 'username' para el email aquí
    formData.append("password", credentials.password);

    return apiClient.post("/auth/token", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
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
    // TODO: En el futuro, decodificar JWT y verificar 'exp' (expiración)
    return !!token;
  },

  async getCurrentUser() {
    if (!this.isAuthenticated()) {
      return Promise.reject(new Error("No autenticado"));
    }
    // Endpoint: GET /auth/users/me/
    return apiClient.get("/auth/users/me/");
  },
};
