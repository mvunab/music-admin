// src/views/RegisterView.vue
<template>
  <v-container fluid class="fill-height pa-0 auth-bg">
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" sm="10" md="8" lg="5" xl="4">
        <v-card class="pa-md-8 pa-4" rounded="xl">
           <v-btn icon variant="text" @click="goBack" style="position: absolute; top: 16px; left: 16px;">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-card-title class="text-h4 font-weight-bold text-center mb-6 pt-4">
            Crear Cuenta
          </v-card-title>
          <v-card-text>
            <v-form ref="registerFormRef" v-model="isRegisterFormValid" @submit.prevent="onSubmitRegister">
              <v-text-field
                v-model="registerData.name"
                label="Nombre Completo"
                prepend-inner-icon="mdi-account-outline"
                :rules="nameRules"
                required
                class="mb-5"
                variant="outlined"
                density="comfortable"
              ></v-text-field>

              <v-text-field
                v-model="registerData.email"
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
                v-model="registerData.password"
                label="Contraseña"
                prepend-inner-icon="mdi-lock-outline"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="showPassword = !showPassword"
                :rules="passwordRules"
                required
                hint="Mínimo 6 caracteres"
                class="mb-5"
                variant="outlined"
                density="comfortable"
              ></v-text-field>

              <v-text-field
                v-model="registerData.confirmPassword"
                label="Confirmar Contraseña"
                prepend-inner-icon="mdi-lock-check-outline"
                :type="showConfirmPassword ? 'text' : 'password'"
                :append-inner-icon="showConfirmPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="showConfirmPassword = !showConfirmPassword"
                :rules="confirmPasswordRules"
                required
                class="mb-5"
                variant="outlined"
                density="comfortable"
              ></v-text-field>

              <v-btn
                :loading="loading"
                :disabled="!isRegisterFormValid || loading"
                type="submit"
                color="primary"
                block
                size="x-large"
                class="mt-3 py-3"
                rounded="lg"
              >
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const registerFormRef = ref(null);
const isRegisterFormValid = ref(null);
const loading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const registerData = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const snackbar = ref({
  show: false,
  message: '',
  color: '',
});

// Reglas de validación
const nameRules = [
  v => !!v || 'El nombre es requerido.',
];
const emailRules = [
  v => !!v || 'El correo es requerido.',
  v => /.+@.+\..+/.test(v) || 'Debe ser un correo electrónico válido.',
];
const passwordRules = [
  v => !!v || 'La contraseña es requerida.',
  v => (v && v.length >= 6) || 'Debe tener al menos 6 caracteres.',
];

const confirmPasswordRules = computed(() => [
  (v) => !!v || 'Debes confirmar la contraseña.',
  (v) => v === registerData.value.password || 'Las contraseñas no coinciden.',
]);

const onSubmitRegister = async () => {
  const { valid } = await registerFormRef.value.validate();
  if (valid) {
    loading.value = true;
    console.log('Register data:', registerData.value);
    
    setTimeout(() => { // Simulación de API
      snackbar.value = { show: true, message: '¡Registro exitoso! Ahora puedes iniciar sesión.', color: 'success' };
      loading.value = false;
      router.push('/'); 
    }, 1500);
  } else {
    snackbar.value = { show: true, message: 'Por favor, completa todos los campos correctamente.', color: 'warning' };
  }
};

const goToLogin = () => {
  router.push('/');
};

const goBack = () => {
  router.go(-1); 
};
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
.auth-bg {
 
  background-color: #f0f2f5;
}
</style>