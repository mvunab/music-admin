<template>
  <v-navigation-drawer
    v-model="drawer"
    :rail="miniVariant"
    permanent
  >
    <v-list-item
      prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
      :title="usuario ? usuario.nombre : 'Usuario'"
      :subtitle="isAdmin ? 'Administrador' : ''"
      :subtitle-class="{ 'text-success': isAdmin }"
    >
      <template v-slot:subtitle v-if="isAdmin">
        <span class="text-success font-weight-medium">Administrador</span>
      </template>
      <template v-slot:append>
        <v-btn
          variant="text"
          icon="mdi-chevron-left"
          @click.stop="miniVariant = !miniVariant"
        ></v-btn>
      </template>
    </v-list-item>

    <v-divider></v-divider>

    <!-- Mostrar botón especial de Administración cuando el usuario es admin -->
    <div v-if="isAdmin" class="px-2 py-3">
      <v-btn
        block
        color="success"
        variant="tonal"
        elevation="2"
        prepend-icon="mdi-shield-account"
        :to="route.path === '/admin' ? '/calendar' : '/admin'"
        class="mb-2 font-weight-medium"
      >
        {{ route.path === '/admin' ? 'Volver al Calendario' : 'Panel de Administración' }}
      </v-btn>
      <v-divider class="my-2"></v-divider>
    </div>

    <v-list density="compact" nav>
      <v-list-item
        v-for="item in filteredMenuItems"
        :key="item.title"
        :to="item.path"
        :prepend-icon="item.icon"
        :title="item.title"
        :color="item.requiresAdmin ? 'success' : undefined"
        link
      >
        <template v-if="item.badge" v-slot:append>
          <v-chip size="x-small" color="success" variant="flat">{{ item.badge }}</v-chip>
        </template>
      </v-list-item>
    </v-list>

    <template v-slot:append>
      <div class="pa-2">
        <v-btn
          block
          color="error"
          prepend-icon="mdi-logout"
          @click="logout"
        >
          Cerrar Sesión
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import authService from '@/services/authService';
import { cerrarSesion, verificarAutenticacion, verificarAdmin } from '@/utils/authUtils';

const route = useRoute();
const router = useRouter();

// Estado del menú
const drawer = ref(true);
const miniVariant = ref(false);
const usuario = ref(null);
const isAdmin = ref(false);

// Definición de elementos del menú
const menuItems = [
  {
    title: 'Calendario',
    path: '/calendar',
    icon: 'mdi-calendar'
  },
  {
    title: 'Planificar Domingo',
    path: '/plan-domingo',
    icon: 'mdi-church'
  },
  {
    title: 'Repertorio',
    path: '/repertorio',
    icon: 'mdi-music'
  },
  {
    title: 'Integrantes',
    path: '/integrantes',
    icon: 'mdi-account-group'
  },
  {
    title: 'Roles Musicales',
    path: '/roles-musicales',
    icon: 'mdi-microphone'
  },
  {
    title: 'Administración',
    path: '/admin',
    icon: 'mdi-shield-account',
    requiresAdmin: true,
    badge: 'Admin'
  }
];

// Filtrar elementos del menú
const filteredMenuItems = computed(() => {
  // Filtrar los elementos del menú, excluyendo el de Administración 
  // ya que ahora tenemos un botón específico para eso
  return menuItems.filter(item => !item.requiresAdmin);
});

// Funciones
async function obtenerUsuario() {
  if (verificarAutenticacion()) {
    try {
      // Intentar obtener el usuario actual desde el endpoint
      const response = await authService.getCurrentUser();
      usuario.value = response.data;
      console.log('Usuario obtenido:', usuario.value);
      
      // Actualizar estado de administrador al obtener el usuario
      verificarAdminStatus();
    } catch (error) {
      console.error('Error al obtener información del usuario:', error);
      
      // Si falla, intentar verificar desde el token
      isAdmin.value = verificarAdmin();
      console.log('Estado de administrador desde token (fallback):', isAdmin.value);
    }
  } else {
    console.log('Usuario no autenticado');
    usuario.value = null;
    isAdmin.value = false;
  }
}

function verificarAdminStatus() {
  // Verificar primero si tenemos el usuario cargado y su rol
  if (usuario.value && usuario.value.rol_plataforma) {
    isAdmin.value = usuario.value.rol_plataforma === 'admin';
    console.log('Estado de administrador actualizado desde usuario:', isAdmin.value);
  } else {
    // Usar la función de verificación del token como respaldo
    isAdmin.value = verificarAdmin();
    console.log('Estado de administrador actualizado desde token:', isAdmin.value);
  }
  
  // Si no es admin pero está en la ruta de admin, debemos actualizarlo a mano
  if (!isAdmin.value && route.path === '/admin') {
    console.log('Forzando actualización del estado de administrador desde JWT');
    const isAdminFromToken = verificarAdmin();
    if (isAdminFromToken) {
      isAdmin.value = true;
      console.log('Estado de administrador corregido desde token JWT');
    }
  }
}

function logout() {
  cerrarSesion();
  // Redirigir inmediatamente para una mejor experiencia de usuario
  router.push('/');
}

// Cargar datos al inicio
onMounted(() => {
  obtenerUsuario();
  verificarAdminStatus();
});

// Watchers
watch(usuario, (newValue) => {
  if (newValue) {
    verificarAdminStatus();
  }
}, { deep: true });

watch(() => route.path, () => {
  // Actualizar estado de administrador cuando cambia la ruta
  obtenerUsuario();
}, { immediate: true });
</script>
