<template>
  <div class="roles-container">
    <h1>Gestión de Roles Musicales</h1>
    
    <!-- Formulario para crear/editar roles musicales -->
    <v-card class="mb-4 pa-4">
      <v-form @submit.prevent="guardarRolMusical">
        <v-text-field 
          v-model="rolActual.nombre" 
          label="Nombre del rol" 
          :rules="[v => !!v || 'El nombre es requerido']"
          required
        ></v-text-field>
        
        <div class="d-flex">
          <v-btn 
            type="submit" 
            color="primary" 
            class="mr-2"
          >
            {{ modoEdicion ? 'Actualizar' : 'Crear' }}
          </v-btn>
          
          <v-btn 
            v-if="modoEdicion" 
            @click="cancelarEdicion" 
            color="grey"
          >
            Cancelar
          </v-btn>
        </div>
      </v-form>
    </v-card>
    
    <!-- Lista de roles musicales -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="rolesMusicales"
        :loading="cargando"
        class="elevation-1"
      >
        <template v-slot:item.integrantes="{ item }">
          <v-chip
            v-for="integrante in item.integrantes"
            :key="integrante.id"
            class="ma-1"
            color="primary"
            text-color="white"
            small
          >
            {{ integrante.nombre }}
          </v-chip>
        </template>
        
        <template v-slot:item.acciones="{ item }">
          <v-btn
            icon
            small
            @click="editarRolMusical(item)"
            color="primary"
            class="mr-2"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          
          <v-btn
            icon
            small
            @click="confirmarEliminar(item)"
            color="error"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
    
    <!-- Diálogo de confirmación para eliminar -->
    <v-dialog v-model="dialogoEliminar" max-width="400">
      <v-card>
        <v-card-title class="headline">¿Confirmar eliminación?</v-card-title>
        <v-card-text>
          ¿Estás seguro de que deseas eliminar el rol musical "{{ rolAEliminar?.nombre }}"? Esta acción no se puede deshacer.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="dialogoEliminar = false">Cancelar</v-btn>
          <v-btn color="error" text @click="eliminarRolMusical">Eliminar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Alerta de mensajes -->
    <v-snackbar
      v-model="mostrarAlerta"
      :color="tipoAlerta"
      timeout="3000"
    >
      {{ mensajeAlerta }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="mostrarAlerta = false"
        >
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import rolesService from '@/services/rolesService';

export default {
  name: 'RolesMusicalesView',
  
  data() {
    return {
      rolesMusicales: [],
      rolActual: {
        nombre: ''
      },
      rolOriginal: null,
      modoEdicion: false,
      cargando: false,
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Nombre', value: 'nombre' },
        { text: 'Integrantes', value: 'integrantes' },
        { text: 'Acciones', value: 'acciones', sortable: false }
      ],
      dialogoEliminar: false,
      rolAEliminar: null,
      mostrarAlerta: false,
      mensajeAlerta: '',
      tipoAlerta: 'info'
    };
  },
  
  created() {
    this.cargarRolesMusicales();
  },
  
  methods: {
    async cargarRolesMusicales() {
      this.cargando = true;
      try {
        const response = await rolesService.getRoles();
        this.rolesMusicales = response.data;
      } catch (error) {
        this.mostrarMensaje('Error al cargar roles musicales: ' + error.message, 'error');
      } finally {
        this.cargando = false;
      }
    },
    
    editarRolMusical(rol) {
      this.rolOriginal = { ...rol };
      this.rolActual = { 
        id: rol.id,
        nombre: rol.nombre 
      };
      this.modoEdicion = true;
    },
    
    cancelarEdicion() {
      this.rolActual = {
        nombre: ''
      };
      this.modoEdicion = false;
    },
    
    async guardarRolMusical() {
      try {
        if (this.modoEdicion) {
          // Actualizar
          await rolesService.updateRol(this.rolActual.id, this.rolActual);
          this.mostrarMensaje('Rol musical actualizado correctamente', 'success');
        } else {
          // Crear nuevo
          await rolesService.createRol(this.rolActual);
          this.mostrarMensaje('Rol musical creado correctamente', 'success');
        }
        
        // Reiniciar formulario y recargar lista
        this.cancelarEdicion();
        this.cargarRolesMusicales();
      } catch (error) {
        this.mostrarMensaje('Error: ' + error.message, 'error');
      }
    },
    
    confirmarEliminar(rol) {
      this.rolAEliminar = rol;
      this.dialogoEliminar = true;
    },
    
    async eliminarRolMusical() {
      try {
        await rolesService.deleteRol(this.rolAEliminar.id);
        this.mostrarMensaje('Rol musical eliminado correctamente', 'success');
        this.cargarRolesMusicales();
      } catch (error) {
        this.mostrarMensaje('Error al eliminar: ' + error.message, 'error');
      } finally {
        this.dialogoEliminar = false;
        this.rolAEliminar = null;
      }
    },
    
    mostrarMensaje(mensaje, tipo = 'info') {
      this.mensajeAlerta = mensaje;
      this.tipoAlerta = tipo;
      this.mostrarAlerta = true;
    }
  }
};
</script>

<style scoped>
.roles-container {
  padding: 20px;
}
</style>
