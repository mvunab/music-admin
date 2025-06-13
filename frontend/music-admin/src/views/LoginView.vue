<template>
  <v-container fluid class="fill-height pa-0 auth-bg">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="8" md="4">
        <v-card class="pa-md-8 pa-4" rounded="xl">
          <v-card-title class="text-h4 text-md-h2 font-weight-bold text-center mb-6">
            Iniciar Sesión
          </v-card-title>
          <v-card-text>
            <v-form ref="loginFormRef" v-model="isLoginFormValid" @submit.prevent="onSubmitLogin">
              <v-text-field v-model="loginData.email" label="Correo Electrónico" prepend-inner-icon="mdi-email-outline"
                type="email" :rules="emailRules" required class="mb-5" variant="outlined" density="comfortable"
                autocomplete="username" :style="{ minHeight: '48px' }"></v-text-field>

              <v-text-field v-model="loginData.password" label="Contraseña" prepend-inner-icon="mdi-lock-outline"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="showPassword = !showPassword" :rules="passwordRules" required class="mb-5"
                variant="outlined" density="comfortable" autocomplete="current-password"
                :style="{ minHeight: '48px' }"></v-text-field>

              <v-btn :loading="loading" :disabled="!isLoginFormValid || loading" type="submit" color="primary" block
                size="x-large" class="mt-3 py-3" rounded="lg" style="min-height: 48px;">
                Ingresar
              </v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions class="justify-center pt-4 pb-2">
            <span class="text-body-1 mr-1">¿No tienes una cuenta?</span>
            <v-btn variant="text" color="primary" @click="goToRegister" class="px-1">
              Crear Cuenta
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="5000" location="top center" rounded="pill">
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn icon="mdi-close" variant="text" @click="snackbar.show = false"></v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import authService from '@/services/authService';

const router = useRouter();
const route = useRoute();
const loginFormRef = ref(null);
const isLoginFormValid = ref(null);
const loading = ref(false);
const showPassword = ref(false);
const loginData = ref({ email: '', password: '' });
const snackbar = ref({ show: false, message: '', color: '' });

const emailRules = [
  v => !!v || 'El correo es requerido.',
  v => /.+@.+\..+/.test(v) || 'El correo debe ser válido.'
];
const passwordRules = [
  v => !!v || 'La contraseña es requerida.'
];

const onSubmitLogin = async () => {
  if (!loginFormRef.value) return;
  const { valid } = await loginFormRef.value.validate();

  if (valid) {
    loading.value = true;
    try {
      const response = await authService.login({
        email: loginData.value.email,
        password: loginData.value.password,
      });

      authService.saveToken(response.data.access_token);

      snackbar.value = { show: true, message: '¡Bienvenido de nuevo!', color: 'success' };

      const redirectPath = route.query.redirect || '/calendar';
      router.push(redirectPath);

    } catch (error) {
      console.error('Error de login:', error.response ? error.response.data : error.message);
      let errorMessage = 'Error al iniciar sesión. Intenta de nuevo.';
      if (error.response && error.response.data && error.response.data.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
          if (errorMessage.toLowerCase().includes("incorrect username or password") ||
            errorMessage.toLowerCase().includes("incorrect email or password")) {
            errorMessage = "Correo o contraseña incorrectos.";
          }
        } else {
          errorMessage = "Ocurrió un error inesperado durante el login.";
        }
      } else if (error.response && error.response.status === 401) {
        errorMessage = "Credenciales no válidas o cuenta no activa.";
      }
      snackbar.value = { show: true, message: errorMessage, color: 'error' };
    } finally {
      loading.value = false;
    }
  } else {
    snackbar.value = { show: true, message: 'Por favor, completa todos los campos requeridos.', color: 'warning' };
  }
};

const goToRegister = () => { router.push('/register'); };
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.auth-bg {
  background-color: #f0f2f5;
}
</style>