// src/views/LoginView.vue
<template>
  <v-container fluid class="fill-height pa-0 auth-bg">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="10" md="8" lg="5" xl="4">
        <v-card class="pa-md-8 pa-4" rounded="xl">
          <v-card-title class="text-h4 font-weight-bold text-center mb-6">
            Iniciar Sesión
          </v-card-title>
          <v-card-text>
            <v-form ref="loginFormRef" v-model="isLoginFormValid" @submit.prevent="onSubmitLogin">
              <v-text-field
                v-model="loginData.email"
                label="Correo Electrónico"
                prepend-inner-icon="mdi-email-outline"
                type="email"
                :rules="emailRules"
                required
                class="mb-5"
                variant="outlined" 
                density="comfortable"
              ></v-text-field>

              <v-text-field
                v-model="loginData.password"
                label="Contraseña"
                prepend-inner-icon="mdi-lock-outline"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="showPassword = !showPassword"
                :rules="passwordRules"
                required
                class="mb-5"
                variant="outlined"
                density="comfortable"
              ></v-text-field>

              <v-btn
                :loading="loading"
                :disabled="!isLoginFormValid || loading"
                type="submit"
                color="primary"
                block
                size="x-large"
                class="mt-3 py-3"
                rounded="lg"
              >
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
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="4000" location="top center">
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn icon @click="snackbar.show = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const loginFormRef = ref(null);
const isLoginFormValid = ref(null); 
const loading = ref(false);
const showPassword = ref(false);

const loginData = ref({
  email: '',
  password: '',
});

const snackbar = ref({
  show: false,
  message: '',
  color: '', // Se define en la lógica
});

const emailRules = [
  v => !!v || 'El correo es requerido.',
  v => /.+@.+\..+/.test(v) || 'Debe ser un correo electrónico válido.',
];
const passwordRules = [
  v => !!v || 'La contraseña es requerida.',
];

const onSubmitLogin = async () => {
  const { valid } = await loginFormRef.value.validate();

  if (valid) {
    loading.value = true;
    console.log('Login data:', loginData.value);

    setTimeout(() => { // Simulación de API
      const loginExitoso = true; // Cambia para probar error
      if (loginExitoso) {
        localStorage.setItem('user-token', 'vuetify-fake-token');
        snackbar.value = { show: true, message: '¡Bienvenido de nuevo!', color: 'success' };
        router.push('/calendar');
      } else {
        snackbar.value = { show: true, message: 'Credenciales incorrectas. Intenta de nuevo.', color: 'error' };
      }
      loading.value = false;
    }, 1500);
  } else {
    snackbar.value = { show: true, message: 'Por favor, revisa los campos.', color: 'warning' };
  }
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.fill-height {
  min-height: 100vh; 
}
.auth-bg {
 
  background-color: #f0f2f5; 
}
.v-card {
  
}
</style>