<template>
  <div class="integrantes-container">
    <h1>Gestión de Integrantes</h1>
    
    <!-- Formulario para crear/editar integrantes -->
    <v-card class="mb-4 pa-4">
      <v-form @submit.prevent="guardarIntegrante">
        <v-text-field 
          v-model="integranteActual.nombre" 
          label="Nombre" 
          :rules="[v => !!v || 'El nombre es requerido']"
          required
        ></v-text-field>
        
        <v-checkbox 
          v-model="integranteActual.activo" 
          label="Activo"
        ></v-checkbox>
        
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
    
    <!-- Lista de integrantes -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="integrantes"
        :loading="cargando"
        class="elevation-1"
      >
        <template v-slot:item.activo="{ item }">
          <v-chip
            :color="item.activo ? 'success' : 'grey'"
            text-color="white"
          >
            {{ item.activo ? 'Activo' : 'Inactivo' }}
          </v-chip>
        </template>
        
        <template v-slot:item.roles_musicales="{ item }">
          <v-chip
            v-for="rol in item.roles_musicales"
            :key="rol.id"
            class="ma-1"
            color="primary"
            text-color="white"
            small
          >
            {{ rol.nombre }}
          </v-chip>
          <v-btn
            x-small
            icon
            @click="abrirDialogoRoles(item)"
            color="primary"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>
        
        <template v-slot:item.acciones="{ item }">
          <v-btn
            icon
            small
            @click="editarIntegrante(item)"
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
    
    <!-- Diálogo para gestionar roles musicales -->
    <v-dialog v-model="dialogoRoles" max-width="500">
      <v-card>
        <v-card-title class="headline">
          Gestionar roles musicales para {{ integranteSeleccionado?.nombre }}
        </v-card-title>
        <v-card-text>
          <v-autocomplete
            v-model="rolSeleccionado"
            :items="rolesMusicalesDisponibles"
            item-text="nombre"
            item-value="id"
            label="Seleccionar rol musical"
            return-object
          ></v-autocomplete>
          
          <v-list>
            <v-list-item v-for="rol in integranteSeleccionado?.roles_musicales" :key="rol.id">
              <v-list-item-content>
                <v-list-item-title>{{ rol.nombre }}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn icon small color="error" @click="removerRolMusical(rol)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="dialogoRoles = false">Cerrar</v-btn>
          <v-btn color="primary" text @click="asignarRolMusical" :disabled="!rolSeleccionado">Asignar Rol</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Diálogo de confirmación para eliminar -->
    <v-dialog v-model="dialogoEliminar" max-width="400">
      <v-card>
        <v-card-title class="headline">¿Confirmar eliminación?</v-card-title>
        <v-card-text>
          ¿Estás seguro de que deseas eliminar a {{ integranteAEliminar?.nombre }}? Esta acción no se puede deshacer.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="dialogoEliminar = false">Cancelar</v-btn>
          <v-btn color="error" text @click="eliminarIntegrante">Eliminar</v-btn>
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
import integrantesService from '@/services/integrantesService';
import rolesService from '@/services/rolesService';

export default {
  name: 'IntegrantesView',
  
  data() {
    return {
      integrantes: [],
      integranteActual: {
        nombre: '',
        activo: true
      },
      integranteOriginal: null,
      modoEdicion: false,
      cargando: false,
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Nombre', value: 'nombre' },
        { text: 'Estado', value: 'activo' },
        { text: 'Roles Musicales', value: 'roles_musicales' },
        { text: 'Acciones', value: 'acciones', sortable: false }
      ],
      dialogoEliminar: false,
      integranteAEliminar: null,
      mostrarAlerta: false,
      mensajeAlerta: '',
      tipoAlerta: 'info',
      
      // Gestión de roles musicales
      dialogoRoles: false,
      integranteSeleccionado: null,
      rolesMusicales: [],
      rolSeleccionado: null,
      cargandoRoles: false
    };
  },
  
  computed: {
    rolesMusicalesDisponibles() {
      if (!this.integranteSeleccionado) return this.rolesMusicales;
      
      // Filtrar roles que el integrante ya tiene
      const idsRolesActuales = this.integranteSeleccionado.roles_musicales.map(r => r.id);
      return this.rolesMusicales.filter(r => !idsRolesActuales.includes(r.id));
    }
  },
  
  created() {
    this.cargarIntegrantes();
    this.cargarRolesMusicales();
  },
  
  methods: {
    async cargarIntegrantes() {
      this.cargando = true;
      try {
        const response = await integrantesService.getAll();
        this.integrantes = response.data;
      } catch (error) {
        this.mostrarMensaje('Error al cargar integrantes: ' + error.message, 'error');
      } finally {
        this.cargando = false;
      }
    },
    
    async cargarRolesMusicales() {
      this.cargandoRoles = true;
      try {
        const response = await rolesService.getAll();
        this.rolesMusicales = response.data;
      } catch (error) {
        this.mostrarMensaje('Error al cargar roles musicales: ' + error.message, 'error');
      } finally {
        this.cargandoRoles = false;
      }
    },
    
    editarIntegrante(integrante) {
      this.integranteOriginal = { ...integrante };
      this.integranteActual = { ...integrante };
      this.modoEdicion = true;
    },
    
    cancelarEdicion() {
      this.integranteActual = {
        nombre: '',
        activo: true
      };
      this.modoEdicion = false;
    },
    
    async guardarIntegrante() {
      try {
        if (this.modoEdicion) {
          // Actualizar
          await integrantesService.update(this.integranteActual.id, this.integranteActual);
          this.mostrarMensaje('Integrante actualizado correctamente', 'success');
        } else {
          // Crear nuevo
          await integrantesService.create(this.integranteActual);
          this.mostrarMensaje('Integrante creado correctamente', 'success');
        }
        
        // Reiniciar formulario y recargar lista
        this.cancelarEdicion();
        this.cargarIntegrantes();
      } catch (error) {
        this.mostrarMensaje('Error: ' + error.message, 'error');
      }
    },
    
    confirmarEliminar(integrante) {
      this.integranteAEliminar = integrante;
      this.dialogoEliminar = true;
    },
    
    async eliminarIntegrante() {
      try {
        await integrantesService.delete(this.integranteAEliminar.id);
        this.mostrarMensaje('Integrante eliminado correctamente', 'success');
        this.cargarIntegrantes();
      } catch (error) {
        this.mostrarMensaje('Error al eliminar: ' + error.message, 'error');
      } finally {
        this.dialogoEliminar = false;
        this.integranteAEliminar = null;
      }
    },
    
    // Métodos para gestión de roles musicales
    abrirDialogoRoles(integrante) {
      this.integranteSeleccionado = { ...integrante };
      this.rolSeleccionado = null;
      this.dialogoRoles = true;
    },
    
    async asignarRolMusical() {
      if (!this.rolSeleccionado || !this.integranteSeleccionado) return;
      
      try {
        await integrantesService.assignRolMusical(
          this.integranteSeleccionado.id, 
          this.rolSeleccionado.id
        );
        
        // Actualizar el integrante seleccionado con el nuevo rol
        this.integranteSeleccionado.roles_musicales.push(this.rolSeleccionado);
        this.rolSeleccionado = null;
        
        // Recargar todos los integrantes para mantener la lista actualizada
        this.cargarIntegrantes();
        
        this.mostrarMensaje('Rol musical asignado correctamente', 'success');
      } catch (error) {
        this.mostrarMensaje('Error al asignar rol: ' + error.message, 'error');
      }
    },
    
    async removerRolMusical(rol) {
      if (!this.integranteSeleccionado) return;
      
      try {
        await integrantesService.removeRolMusical(
          this.integranteSeleccionado.id, 
          rol.id
        );
        
        // Actualizar el integrante seleccionado quitando el rol
        const index = this.integranteSeleccionado.roles_musicales.findIndex(r => r.id === rol.id);
        if (index !== -1) {
          this.integranteSeleccionado.roles_musicales.splice(index, 1);
        }
        
        // Recargar todos los integrantes para mantener la lista actualizada
        this.cargarIntegrantes();
        
        this.mostrarMensaje('Rol musical removido correctamente', 'success');
      } catch (error) {
        this.mostrarMensaje('Error al remover rol: ' + error.message, 'error');
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
.integrantes-container {
  padding: 20px;
}
</style>
