// Servicio para manejar las operaciones con asignaciones
import { apiClient, API_V1_PREFIX } from "./apiService";

export default {
  // Obtener todas las asignaciones
  async getAll() {
    return apiClient.get(`${API_V1_PREFIX}/asignaciones/`);
  },

  // Obtener una asignación por ID
  async getById(id) {
    return apiClient.get(`${API_V1_PREFIX}/asignaciones/${id}`);
  },

  // Obtener asignaciones por domingo
  async getByDomingo(domingoId) {
    return apiClient.get(`${API_V1_PREFIX}/asignaciones/domingo/${domingoId}`);
  },

  // Crear una nueva asignación
  async create(asignacion) {
    return apiClient.post(`${API_V1_PREFIX}/asignaciones/`, asignacion);
  },

  // Actualizar una asignación existente
  async update(id, asignacion) {
    return apiClient.put(`${API_V1_PREFIX}/asignaciones/${id}`, asignacion);
  },

  // Eliminar una asignación
  async delete(id) {
    return apiClient.delete(`${API_V1_PREFIX}/asignaciones/${id}`);
  }
};
