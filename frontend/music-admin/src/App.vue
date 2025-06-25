<template>
  <v-app>
    <!-- Menú de navegación lateral (solo visible para usuarios autenticados) -->
    <NavigationMenu v-if="isAuthenticated" />
    
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import NavigationMenu from '@/components/NavigationMenu.vue';
import { verificarAutenticacion } from '@/utils/authUtils';

const router = useRouter();
const route = useRoute();
const isAuthenticated = ref(false);

// Verificar autenticación al montar el componente
onMounted(() => {
  isAuthenticated.value = verificarAutenticacion();
});

// Observar cambios en la ruta para verificar autenticación
watch(
  () => route.path,
  () => {
    isAuthenticated.value = verificarAutenticacion();
  }
);
</script>

<style>
html, body, #app, .v-application, .v-application__wrap {
  height: 100%;
  margin: 0;
  padding: 0;
}
.v-main {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
/* Ajustar espacio para el menú lateral */
.v-navigation-drawer + .v-main {
  padding-left: var(--v-navigation-drawer-width, 256px);
  transition: padding 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
/* Cuando el menú está en modo mini */
.v-navigation-drawer--rail + .v-main {
  padding-left: var(--v-navigation-drawer-rail-width, 68px);
  transition: padding 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>