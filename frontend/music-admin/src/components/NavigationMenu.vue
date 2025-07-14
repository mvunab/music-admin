<template>
  <v-navigation-drawer
    v-model="drawer"
    :rail="miniVariant"
    :rail-width="68"
    permanent
    class="navigation-drawer"
  >
    <!-- Botón flotante para expandir/colapsar cuando está en modo colapsado -->
    <transition name="fade-slide">
      <div v-if="miniVariant" class="toggle-btn-container">
        <v-btn
          icon
          color="primary"
          variant="elevated"
          size="small"
          @click="miniVariant = false"
          class="toggle-rail-btn"
          elevation="4"
        >
          <v-icon>mdi-chevron-double-right</v-icon>
        </v-btn>
      </div>
    </transition>

    <v-list-item
      prepend-avatar="https://scontent-scl2-1.xx.fbcdn.net/v/t39.30808-6/347824368_143649812030424_8457102618182306856_n.png?_nc_cat=101&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeFtRj3QX2p4f3QQyztnXoId3Lxnt0p7TlfcvGe3SntOVwTwgWh_q-0MvCMmdiPRHEs&_nc_ohc=RY2VSa6naHkQ7kNvwH_Jn0Y&_nc_oc=AdkDBhU1arwpTipOHI1rDAwMwO02Ge-yjS15AXmkAo6CnwrOV47Z_9D6mEHPRr-r5BI&_nc_zt=23&_nc_ht=scontent-scl2-1.xx&_nc_gid=b4HoU5IhaiqVndv2n2JQkw&oh=00_AfTdjvDhgEST-ZqxVMCXXlNjWpPvhu2jZSA_SGYy7Omy9A&oe=6875F6B8"
      :title="usuario ? usuario.nombre : 'Usuario'"
      :subtitle="isAdmin ? 'Administrador' : ''"
      :subtitle-class="{ 'text-success': isAdmin }"
      class="mt-2"
    >
      <template v-slot:subtitle v-if="isAdmin">
        <span class="text-success font-weight-medium d-flex align-center">
          <v-icon v-if="miniVariant" color="success" size="small" class="mr-1">mdi-shield-account</v-icon>
          <span v-if="!miniVariant">Administrador</span>
        </span>
      </template>
      <template v-slot:append>
        <v-btn
          variant="text"
          icon="mdi-chevron-double-left"
          color="primary"
          @click.stop="miniVariant = !miniVariant"
          class="collapse-btn"
        ></v-btn>
      </template>
    </v-list-item>

    <v-divider></v-divider>

    <!-- Mostrar botón especial de Administración cuando el usuario es admin -->
    <div v-if="isAdmin" :class="miniVariant ? 'py-3 text-center' : 'px-0 py-3'">
      <v-tooltip
        v-if="miniVariant"
        location="right"
        :text="route.path === '/admin' ? 'Volver al Calendario' : 'Panel de Administrador'"
      >
        <template v-slot:activator="{ props }">
          <v-btn
            icon
            color="success"
            variant="tonal"
            elevation="2"
            :to="route.path === '/admin' ? '/calendar' : '/admin'"
            class="mb-2 font-weight-medium"
            v-bind="props"
            size="large"
          >
            <v-icon>mdi-shield-account</v-icon>
          </v-btn>
        </template>
      </v-tooltip>
      
      <v-btn
        v-else
        block
        color="success"
        variant="tonal"
        elevation="2"
        prepend-icon="mdi-shield-account"
        :to="route.path === '/admin' ? '/calendar' : '/admin'"
        class="mb-2 font-weight-medium"
      >
        {{ route.path === '/admin' ? 'Volver al Calendario' : 'Panel de Administrador' }}
      </v-btn>
      <v-divider class="my-2"></v-divider>
    </div>

    <v-list density="compact" nav>
      <v-tooltip
        v-for="item in filteredMenuItems"
        :key="item.title"
        :text="item.title"
        location="right"
        :disabled="!miniVariant"
      >
        <template v-slot:activator="{ props }">
          <v-list-item
            :to="item.path"
            :prepend-icon="item.icon"
            :title="miniVariant ? '' : item.title"
            :color="item.requiresAdmin ? 'success' : undefined"
            link
            :class="{ 'px-1': miniVariant, 'menu-item': true }"
            :title-class="{ 'text-caption': miniVariant }"
            v-bind="miniVariant ? props : {}"
          >
            <template v-if="item.badge && !miniVariant" v-slot:append>
              <v-chip size="x-small" color="success" variant="flat">{{ item.badge }}</v-chip>
            </template>
          </v-list-item>
        </template>
      </v-tooltip>
    </v-list>

    <template v-slot:append>
      <div class="pa-2">
        <v-tooltip v-if="miniVariant" location="right" text="Cerrar Sesión">
          <template v-slot:activator="{ props }">
            <v-btn
              icon
              color="error"
              @click="logout"
              v-bind="props"
              class="mx-auto mb-2 d-flex"
            >
              <v-icon>mdi-logout</v-icon>
            </v-btn>
          </template>
        </v-tooltip>
        
        <v-btn
          v-else
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
const miniVariant = ref(localStorage.getItem('menuCollapsed') === 'true');
const usuario = ref(null);
const isAdmin = ref(false);

// Observar cambios en el estado del menú para guardar la preferencia
watch(miniVariant, (newValue) => {
  localStorage.setItem('menuCollapsed', newValue);
});

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
    icon: 'mdi-church',
    requiresAdmin: true
  },
  {
    title: 'Repertorio',
    path: '/repertorio',
    icon: 'mdi-music'
  },
  {
    title: 'Roles Musicales',
    path: '/roles-musicales',
    icon: 'mdi-microphone',
    requiresAdmin: true
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
  // Si el usuario es administrador, mostrar todos excepto el botón de Administración
  // (ya que tenemos un botón específico para eso)
  if (isAdmin.value) {
    return menuItems.filter(item => !item.requiresAdmin || item.title !== 'Administración');
  } else {
    // Para usuarios regulares, solo mostrar Calendario y Repertorio
    return menuItems.filter(item => !item.requiresAdmin);
  }
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

<style scoped>
/* Estilo para el botón flotante cuando el menú está colapsado */
.toggle-btn-container {
  position: absolute;
  right: -18px;
  top: 70px;
  z-index: 10;
}

.toggle-rail-btn {
  box-shadow: 0 3px 5px -1px rgba(0,0,0,.2), 0 6px 10px 0 rgba(0,0,0,.14), 0 1px 18px 0 rgba(0,0,0,.12);
  transition: transform 0.2s, box-shadow 0.2s;
}

.toggle-rail-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 5px 8px -2px rgba(0,0,0,.3), 0 8px 15px 0 rgba(0,0,0,.2), 0 2px 25px 0 rgba(0,0,0,.15);
}

/* Cuando el menú está colapsado, asegurar que los íconos sean más visibles */
.v-navigation-drawer--rail :deep(.v-list-item__prepend > .v-icon) {
  margin-inline-start: 4px;
  font-size: 24px;
}

/* Asegurar que el menú colapsado tenga un ancho suficiente */
.v-navigation-drawer--rail {
  width: var(--v-navigation-drawer-rail-width, 68px) !important;
}

/* Mejorar la visibilidad de los elementos en modo colapsado */
.v-navigation-drawer--rail :deep(.v-list-item) {
  padding: 8px 0;
  min-height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Añadir un tooltip o indicador visual al pasar el cursor */
.v-navigation-drawer--rail :deep(.v-list-item:hover) {
  background-color: rgba(var(--v-theme-primary), 0.1);
}

/* Estilo para el botón de colapsar cuando el menú está expandido */
.collapse-btn {
  transition: transform 0.2s;
}

.collapse-btn:hover {
  transform: scale(1.2);
  background-color: rgba(var(--v-theme-primary), 0.1);
}

/* Estilo para los elementos del menú */
.menu-item {
  position: relative;
  transition: background-color 0.2s, transform 0.2s;
}

.menu-item:hover {
  transform: translateX(3px);
}

/* Estilo para el drawer completo */
.navigation-drawer {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}

.v-navigation-drawer--rail .v-list-item__prepend {
  justify-content: center;
  width: 100%;
  margin-right: 0;
}

/* Animaciones */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}
</style>
