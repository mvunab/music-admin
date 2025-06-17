// Servicio para manejar las operaciones con usuarios
import { apiClient, API_V1_PREFIX } from "./apiService";

export default {
  // Obtener todos los usuarios
  async getUsuarios() {
    return apiClient.get(`${API_V1_PREFIX}/usuarios/`);
  },

  // Obtener un usuario por ID
  async getUsuarioById(id) {
    return apiClient.get(`${API_V1_PREFIX}/usuarios/${id}`);
  },

  // Obtener el usuario actual autenticado
  async getCurrentUser() {
    return apiClient.get(`${API_V1_PREFIX}/usuarios/me/`);
  },

  // Crear un nuevo usuario
  async createUsuario(usuario) {
    return apiClient.post(`${API_V1_PREFIX}/usuarios/`, usuario);
  },

  // Actualizar un usuario existente
  async updateUsuario(id, usuario) {
    return apiClient.put(`${API_V1_PREFIX}/usuarios/${id}`, usuario);
  },

  // Eliminar un usuario
  async deleteUsuario(id) {
    return apiClient.delete(`${API_V1_PREFIX}/usuarios/${id}`);
  },

  // Asociar un usuario con un integrante
  async associateWithIntegrante(usuarioId, integranteId) {
    return apiClient.post(`${API_V1_PREFIX}/usuarios/${usuarioId}/integrante/${integranteId}`);
  }
};
