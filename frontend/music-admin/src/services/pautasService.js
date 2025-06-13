// Servicio para manejar las operaciones con pautas
import { apiClient, API_V1_PREFIX } from "./apiService";

export default {
  // Obtener todas las pautas
  async getAll() {
    return apiClient.get(`${API_V1_PREFIX}/pautas/`);
  },

  // Obtener una pauta por ID
  async getById(id) {
    return apiClient.get(`${API_V1_PREFIX}/pautas/${id}`);
  },

  // Crear una nueva pauta
  async create(pauta) {
    return apiClient.post(`${API_V1_PREFIX}/pautas/`, pauta);
  },

  // Actualizar una pauta existente
  async update(id, pauta) {
    return apiClient.put(`${API_V1_PREFIX}/pautas/${id}`, pauta);
  },

  // Eliminar una pauta
  async delete(id) {
    return apiClient.delete(`${API_V1_PREFIX}/pautas/${id}`);
  }
};
