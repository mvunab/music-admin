// Servicio para manejar las operaciones con domingos
import { apiClient, API_V1_PREFIX } from "./apiService";

export default {
  // Obtener todos los domingos
  async getAll() {
    return apiClient.get(`${API_V1_PREFIX}/domingos/`);
  },

  // Obtener un domingo por ID
  async getById(id) {
    return apiClient.get(`${API_V1_PREFIX}/domingos/${id}`);
  },

  // Obtener un domingo por fecha
  async getByFecha(fecha) {
    return apiClient.get(`${API_V1_PREFIX}/domingos/fecha/${fecha}`);
  },

  // Crear un nuevo domingo
  async create(domingo) {
    return apiClient.post(`${API_V1_PREFIX}/domingos/`, domingo);
  },

  // Actualizar un domingo existente
  async update(id, domingo) {
    return apiClient.put(`${API_V1_PREFIX}/domingos/${id}`, domingo);
  },

  // Eliminar un domingo
  async delete(id) {
    return apiClient.delete(`${API_V1_PREFIX}/domingos/${id}`);
  }
};
