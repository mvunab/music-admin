// Servicio para manejar las operaciones con integrantes
import { apiClient, API_V1_PREFIX } from "./apiService";

export default {
  // Obtener todos los integrantes
  async getAll() {
    return apiClient.get(`${API_V1_PREFIX}/integrantes/`);
  },

  // Obtener un integrante por ID
  async getById(id) {
    return apiClient.get(`${API_V1_PREFIX}/integrantes/${id}`);
  },

  // Crear un nuevo integrante
  async create(integrante) {
    return apiClient.post(`${API_V1_PREFIX}/integrantes/`, integrante);
  },

  // Actualizar un integrante existente
  async update(id, integrante) {
    return apiClient.put(`${API_V1_PREFIX}/integrantes/${id}`, integrante);
  },

  // Eliminar un integrante
  async delete(id) {
    return apiClient.delete(`${API_V1_PREFIX}/integrantes/${id}`);
  },

  // Asignar un rol musical a un integrante
  async assignRolMusical(integranteId, rolMusicalId) {
    return apiClient.post(`${API_V1_PREFIX}/integrantes/${integranteId}/roles/${rolMusicalId}`);
  },

  // Remover un rol musical de un integrante
  async removeRolMusical(integranteId, rolMusicalId) {
    return apiClient.delete(`${API_V1_PREFIX}/integrantes/${integranteId}/roles/${rolMusicalId}`);
  }
};
