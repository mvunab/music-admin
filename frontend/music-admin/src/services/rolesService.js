import { apiClient, API_V1_PREFIX } from './apiService';

const BASE_URL = `${API_V1_PREFIX}/roles`;  // Usando el prefijo correcto

export default {
  // Obtener todos los roles musicales
  getRoles() {
    return apiClient.get(BASE_URL);
  },

  // Obtener un rol musical por ID
  getRolById(id) {
    return apiClient.get(`${BASE_URL}/${id}`);
  },

  // Crear un nuevo rol musical
  createRol(rol) {
    return apiClient.post(BASE_URL, rol);
  },

  // Actualizar un rol musical existente
  updateRol(id, rol) {
    return apiClient.put(`${BASE_URL}/${id}`, rol);
  },

  // Eliminar un rol musical
  deleteRol(id) {
    return apiClient.delete(`${BASE_URL}/${id}`);
  }
};
