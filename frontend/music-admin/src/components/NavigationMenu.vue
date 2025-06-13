<template>
  <v-navigation-drawer
    v-model="drawer"
    app
    :rail="miniVariant"
    permanent
  >
    <v-list-item
      prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
      :title="usuario ? usuario.nombre : 'Usuario'"
    >
      <template v-slot:append>
        <v-btn
          variant="text"
          icon="mdi-chevron-left"
          @click.stop="miniVariant = !miniVariant"
        ></v-btn>
      </template>
    </v-list-item>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item
        v-for="item in menuItems"
        :key="item.title"
        :to="item.path"
        :prepend-icon="item.icon"
        :title="item.title"
        link
      ></v-list-item>
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

<script>
import authService from '@/services/authService';

export default {
  name: 'NavigationMenu',
  
  data() {
    return {
      drawer: true,
      miniVariant: false,
      usuario: null,
      menuItems: [
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
        }
      ]
    };
  },
  
  created() {
    this.obtenerUsuario();
  },
  
  methods: {
    async obtenerUsuario() {
      if (authService.isAuthenticated()) {
        try {
          const response = await authService.getCurrentUser();
          this.usuario = response.data;
        } catch (error) {
          console.error('Error al obtener información del usuario', error);
        }
      }
    },
    
    logout() {
      authService.logout();
      this.$router.push('/');
    }
  }
};
</script>
