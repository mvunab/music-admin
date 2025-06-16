import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import VueHtmlToPaper from 'vue-html-to-paper';
import authService from './services/authService';

import './style.css';

// Manejador global de errores para interceptar problemas de autenticación
window.addEventListener('error', function(event) {
  console.error('Error global interceptado:', event.error);
  // Verificar si el error está relacionado con autenticación
  if (event.error && (
    event.error.message.includes('token') || 
    event.error.message.includes('auth') ||
    event.error.message.includes('unauthorized')
  )) {
    console.log('Error relacionado con autenticación, cerrando sesión por seguridad...');
    authService.logout();
  }
});

// Interceptar errores de red
window.addEventListener('unhandledrejection', function(event) {
  console.error('Promesa rechazada no manejada:', event.reason);
  // Verificar si es un error de red o autenticación
  if (event.reason && (
    (event.reason.response && event.reason.response.status === 401) || 
    event.reason.message.includes('network')
  )) {
    console.log('Error de red o autenticación, verificando sesión...');
    // Forzar verificación de autenticación
    if (!authService.isAuthenticated()) {
      authService.logout();
    }
  }
});

const app = createApp(App);
app.use(router);
app.use(vuetify);
app.use(VueHtmlToPaper);
app.mount('#app');
