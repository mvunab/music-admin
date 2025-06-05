<template>
  <div class="user-create-form">
    <h2>Crear Nuevo Usuario</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" v-model="nombre" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Contraseña:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Crear Usuario</button>
    </form>
    <p v-if="message" :class="{ 'success-message': isSuccess, 'error-message': !isSuccess }" class="message">{{ message
      }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const nombre = ref('');
const email = ref('');
const password = ref('');
const message = ref('');
const isSuccess = ref(false);


const API_URL = 'http://127.0.0.1:8000/usuarios/';

const handleSubmit = async () => {
  message.value = '';
  isSuccess.value = false;

  if (!nombre.value || !email.value || !password.value) {
    message.value = 'Por favor, completa todos los campos.';
    isSuccess.value = false;
    return;
  }

  try {
    const response = await axios.post(API_URL, {
      nombre: nombre.value,
      email: email.value,
      password: password.value,
    });

    if (response.status === 200 || response.status === 201) {
      message.value = `Usuario "${response.data.nombre}" creado con éxito! ID: ${response.data.id}`;
      isSuccess.value = true;
      // Limpiar el formulario
      nombre.value = '';
      email.value = '';
      password.value = '';
    } else {
      // Manejo de errores inesperados
      message.value = `Error inesperado: ${response.status} ${response.statusText}`;
      isSuccess.value = false;
    }
  } catch (error) {
    if (error.response) {
      // El backend devolvió un error
      if (error.response.data && error.response.data.detail) {
        if (Array.isArray(error.response.data.detail)) {
          // Errores de validación de Pydantic
          message.value = error.response.data.detail.map(err => `${err.loc.join('.')} - ${err.msg}`).join('; ');
        } else {
          message.value = `Error del servidor: ${error.response.data.detail}`;
        }
      } else {
        message.value = `Error del servidor: ${error.response.status} ${error.response.statusText}`;
      }
    } else if (error.request) {
      // La solicitud se hizo pero no se recibió respuesta (ej. problema de red, CORS si no está bien configurado)
      message.value = 'No se pudo conectar al servidor. Verifica la consola para más detalles (CORS o red).';
      console.error('Error de red o CORS:', error.request);
    } else {
      // Algo más causó el error
      message.value = `Error al crear el usuario: ${error.message}`;
    }
    isSuccess.value = false;
  }
};
</script>

<style scoped>
.user-create-form {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: calc(100% - 20px);
  padding: 8px 10px;
  border: 1px solid #ddd;
  background-color: rgb(56, 56, 56);
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #45a049;
}

.message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
}

.success-message {
  color: #155724;
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
}
</style>
