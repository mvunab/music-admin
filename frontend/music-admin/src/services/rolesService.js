// Servicio para manejar las operaciones con roles musicales
import { apiClient, API_V1_PREFIX } from "./apiService";

export default {
  // Obtener todos los roles musicales
  async getRoles() {
    return apiClient.get(`${API_V1_PREFIX}/roles/`);
  },

  // Obtener un rol musical por ID
  async getRolById(id) {
    return apiClient.get(`${API_V1_PREFIX}/roles/${id}`);
  },

  // Crear un nuevo rol musical
  async createRol(rolMusical) {
    return apiClient.post(`${API_V1_PREFIX}/roles/`, rolMusical);
  },

  // Actualizar un rol musical existente
  async updateRol(id, rolMusical) {
    return apiClient.put(`${API_V1_PREFIX}/roles/${id}`, rolMusical);
  },

  // Eliminar un rol musical
  async deleteRol(id) {
    return apiClient.delete(`${API_V1_PREFIX}/roles/${id}`);
  },
  
  // Obtener integrantes por rol musical
  async getIntegrantesByRol(id) {
    return apiClient.get(`${API_V1_PREFIX}/roles/${id}`).then(response => {
      return response.data.integrantes || [];
    });
  }
};
