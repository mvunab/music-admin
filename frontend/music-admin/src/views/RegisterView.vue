// src/views/RegisterView.vue
<template>
  <v-container fluid class="fill-height pa-0 auth-bg">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="10" md="8" lg="5" xl="4">
        <v-card class="pa-md-8 pa-4" rounded="xl">
          <v-btn icon variant="text" @click="goBack" style="position: absolute; top: 16px; left: 16px;"
            aria-label="Volver">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-card-title class="text-h4 font-weight-bold text-center mb-6 pt-4">
            Crear Cuenta
          </v-card-title>
          <v-card-text>
            <v-form ref="registerFormRef" v-model="isRegisterFormValid" @submit.prevent="onSubmitRegister">
              <v-text-field v-model="registerData.name" label="Nombre Completo" prepend-inner-icon="mdi-account-outline"
                :rules="nameRules" required class="mb-5" variant="outlined" density="comfortable"></v-text-field>

              <v-text-field v-model="registerData.email" label="Correo Electrónico"
                prepend-inner-icon="mdi-email-outline" type="email" :rules="emailRules" required class="mb-5"
                variant="outlined" density="comfortable"></v-text-field>

              <v-text-field v-model="registerData.password" label="Contraseña" prepend-inner-icon="mdi-lock-outline"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="showPassword = !showPassword" :rules="passwordRules" required
                hint="Mínimo 6 caracteres" class="mb-5" variant="outlined" density="comfortable"></v-text-field>

              <v-text-field v-model="confirmPasswordModel" label="Confirmar Contraseña"
                prepend-inner-icon="mdi-lock-check-outline" :type="showConfirmPassword ? 'text' : 'password'"
                :append-inner-icon="showConfirmPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="showConfirmPassword = !showConfirmPassword" :rules="confirmPasswordRules" required
                class="mb-5" variant="outlined" density="comfortable"></v-text-field>

              <v-btn :loading="loading" :disabled="!isRegisterFormValid || loading" type="submit" color="primary" block
                size="x-large" class="mt-3 py-3" rounded="lg">
                Registrarme
              </v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions class="justify-center pt-4 pb-2">
            <span class="text-body-1 mr-1">¿Ya tienes una cuenta?</span>
            <v-btn variant="text" color="primary" @click="goToLogin" class="px-1">
              Iniciar Sesión
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="5000" location="top center" rounded="pill"
      multi-line>
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn icon="mdi-close" variant="text" @click="snackbar.show = false"></v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/authService';

const router = useRouter();
const registerFormRef = ref(null);
const isRegisterFormValid = ref(null);
const loading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const registerData = ref({ name: '', email: '', password: '' });
const confirmPasswordModel = ref('');
const snackbar = ref({ show: false, message: '', color: '' });

const nameRules = [v => !!v || 'El nombre es requerido.'];
const emailRules = [v => !!v || 'El correo es requerido.', v => /.+@.+\..+/.test(v) || 'El correo debe ser válido.'];
const passwordRules = [v => !!v || 'La contraseña es requerida.', v => (v && v.length >= 6) || 'Mínimo 6 caracteres.'];
const confirmPasswordRules = computed(() => [
  (v) => !!v || 'Debes confirmar la contraseña.',
  (v) => v === registerData.value.password || 'Las contraseñas no coinciden.',
]);

const onSubmitRegister = async () => {
  if (!registerFormRef.value) return;
  const { valid } = await registerFormRef.value.validate();

  if (valid) {
    loading.value = true;
    try {
      const payload = {
        email: registerData.value.email,
        password: registerData.value.password,
        nombre: registerData.value.name, // El servicio y backend esperan 'nombre'
      };

      const response = await authService.register(payload);
      // suele devolver el objeto del usuario creado (status 200 o 201)
      console.log('Respuesta de registro:', response.data);

      snackbar.value = { show: true, message: '¡Registro exitoso! Ahora puedes iniciar sesión.', color: 'success' };
      router.push({ name: 'Login' }); // Redirigir al login

    } catch (error) {
      console.error('Error de registro:', error.response ? error.response.data : error.message);
      let errorMessage = 'Error al registrar el usuario. Intenta de nuevo.';
      if (error.response && error.response.data && error.response.data.detail) {
        if (Array.isArray(error.response.data.detail)) { // Errores de validación Pydantic
          errorMessage = error.response.data.detail.map(err => {
            const fieldLocation = err.loc && err.loc.length > 1 ? err.loc.slice(-1)[0] : 'Campo';
            // Capitalizar la primera letra del campo para mejor lectura
            const field = fieldLocation.charAt(0).toUpperCase() + fieldLocation.slice(1);
            return `${field}: ${err.msg}`;
          }).join('\n'); //  \n para que el snackbar multi-line lo muestre mejor
        } else if (typeof error.response.data.detail === 'string') { // Error general como "Email ya registrado"
          errorMessage = error.response.data.detail;
        }
      }
      snackbar.value = { show: true, message: errorMessage, color: 'error' };
    } finally {
      loading.value = false;
    }
  } else {
    snackbar.value = { show: true, message: 'Por favor, completa todos los campos correctamente.', color: 'warning' };
  }
};

const goToLogin = () => { router.push('/'); };
const goBack = () => { router.go(-1); };
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.auth-bg {
  background-color: #f0f2f5;
}
</style>