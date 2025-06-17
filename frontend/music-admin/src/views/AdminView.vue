<template>
  <v-container fluid class="pa-md-6 pa-3">
    <v-row>
      <v-col>
        <!-- Header principal -->
        <div class="d-flex justify-space-between align-center mb-4 flex-wrap">
          <h1 class="text-h5 text-md-h4 font-weight-medium">Administración de Usuarios</h1>
          
          <div class="d-flex gap-2">
            <v-btn color="success" prepend-icon="mdi-account-plus" @click="showCreateUserDialog = true">
              Nuevo Usuario
            </v-btn>
            <v-btn color="primary" prepend-icon="mdi-account-multiple-plus" @click="showCreateIntegranteDialog = true">
              Nuevo Integrante
            </v-btn>
          </div>
        </div>

        <!-- Pestañas para separar usuarios e integrantes -->
        <v-tabs v-model="activeTab" color="primary" align-tabs="center" class="mb-6">
          <v-tab value="usuarios" class="px-6">Usuarios</v-tab>
          <v-tab value="integrantes" class="px-6">Integrantes</v-tab>
        </v-tabs>

        <!-- Contenido de Usuarios -->
        <v-window v-model="activeTab">
          <v-window-item value="usuarios">
            <v-card variant="outlined" class="mb-4">
              <v-card-text>
                <v-text-field
                  v-model="searchUsuarios"
                  label="Buscar usuarios"
                  prepend-inner-icon="mdi-magnify"
                  single-line
                  hide-details
                  variant="outlined"
                  density="compact"
                  class="mb-4"
                ></v-text-field>

                <v-data-table
                  :headers="usuariosHeaders"
                  :items="filteredUsuarios"
                  :loading="loadingUsuarios"
                  class="elevation-1"
                >
                  <template v-slot:item.es_admin="{ item }">
                    <v-chip
                      :color="item.rol_plataforma === 'admin' ? 'success' : 'default'"
                      size="small"
                      class="text-capitalize"
                      variant="outlined"
                    >
                      {{ item.rol_plataforma === 'admin' ? 'Administrador' : 'Usuario' }}
                    </v-chip>
                  </template>
                  <template v-slot:item.actions="{ item }">
                    <v-tooltip text="Editar Usuario">
                      <template v-slot:activator="{ props }">
                        <v-btn
                          v-bind="props"
                          density="compact"
                          icon
                          variant="text"
                          @click="editarUsuario(item)"
                        >
                          <v-icon size="small">mdi-pencil</v-icon>
                        </v-btn>
                      </template>
                    </v-tooltip>
                    <v-tooltip text="Asignar como Administrador" v-if="item.rol_plataforma !== 'admin'">
                      <template v-slot:activator="{ props }">
                        <v-btn
                          v-bind="props"
                          density="compact"
                          icon
                          variant="text"
                          color="purple"
                          @click="convertirAdmin(item)"
                        >
                          <v-icon size="small">mdi-shield-account</v-icon>
                        </v-btn>
                      </template>
                    </v-tooltip>
                    <v-tooltip text="Eliminar Usuario">
                      <template v-slot:activator="{ props }">
                        <v-btn
                          v-bind="props"
                          density="compact"
                          icon
                          variant="text"
                          color="error"
                          @click="confirmarEliminarUsuario(item)"
                        >
                          <v-icon size="small">mdi-delete</v-icon>
                        </v-btn>
                      </template>
                    </v-tooltip>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-window-item>

          <!-- Contenido de Integrantes -->
          <v-window-item value="integrantes">
            <v-card variant="outlined" class="mb-4">
              <v-card-text>
                <v-text-field
                  v-model="searchIntegrantes"
                  label="Buscar integrantes"
                  prepend-inner-icon="mdi-magnify"
                  single-line
                  hide-details
                  variant="outlined"
                  density="compact"
                  class="mb-4"
                ></v-text-field>

                <v-data-table
                  :headers="integrantesHeaders"
                  :items="filteredIntegrantes"
                  :loading="loadingIntegrantes"
                  class="elevation-1"
                >
                  <template v-slot:item.roles="{ item }">
                    <v-chip
                      v-for="rol in item.roles"
                      :key="rol.id"
                      size="small"
                      class="mr-1"
                      color="info"
                      variant="outlined"
                    >
                      {{ rol.nombre }}
                    </v-chip>
                  </template>
                  <template v-slot:item.usuario="{ item }">
                    <span v-if="item.usuario">{{ item.usuario.nombre }} ({{ item.usuario.email }})</span>
                    <span v-else class="text-grey">No asignado</span>
                  </template>
                  <template v-slot:item.actions="{ item }">
                    <v-tooltip text="Editar Integrante">
                      <template v-slot:activator="{ props }">
                        <v-btn
                          v-bind="props"
                          density="compact"
                          icon
                          variant="text"
                          @click="editarIntegrante(item)"
                        >
                          <v-icon size="small">mdi-pencil</v-icon>
                        </v-btn>
                      </template>
                    </v-tooltip>
                    <v-tooltip text="Eliminar Integrante">
                      <template v-slot:activator="{ props }">
                        <v-btn
                          v-bind="props"
                          density="compact"
                          icon
                          variant="text"
                          color="error"
                          @click="confirmarEliminarIntegrante(item)"
                        >
                          <v-icon size="small">mdi-delete</v-icon>
                        </v-btn>
                      </template>
                    </v-tooltip>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </v-col>
    </v-row>

    <!-- Dialog para crear/editar usuario -->
    <v-dialog v-model="showUserDialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white pa-4">
          {{ editingUser ? 'Editar Usuario' : 'Crear Nuevo Usuario' }}
        </v-card-title>
        <v-card-text class="pa-4">
          <v-form ref="userForm" v-model="userFormValid" @submit.prevent="guardarUsuario">
            <v-text-field
              v-model="userFormData.nombre"
              label="Nombre completo"
              :rules="[v => !!v || 'El nombre es requerido']"
              required
            ></v-text-field>
            
            <v-text-field
              v-model="userFormData.email"
              label="Email"
              type="email"
              :rules="[
                v => !!v || 'El email es requerido',
                v => /.+@.+\..+/.test(v) || 'El email debe ser válido'
              ]"
              required
            ></v-text-field>
            
            <v-text-field
              v-if="!editingUser"
              v-model="userFormData.password"
              label="Contraseña"
              type="password"
              :rules="[v => !!v || 'La contraseña es requerida', v => v.length >= 6 || 'Mínimo 6 caracteres']"
              required
            ></v-text-field>
            
            <v-switch
              v-model="userFormData.rol_plataforma"
              color="success"
              label="Otorgar permisos de administrador"
              hint="El usuario podrá gestionar todos los usuarios del sistema"
              persistent-hint
              :true-value="'admin'"
              :false-value="'regular'"
            ></v-switch>
          </v-form>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showUserDialog = false">
            Cancelar
          </v-btn>
          <v-btn 
            color="primary" 
            variant="elevated" 
            @click="guardarUsuario" 
            :loading="savingUser"
            :disabled="!userFormValid"
          >
            Guardar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog para crear/editar integrante -->
    <v-dialog v-model="showIntegranteDialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white pa-4">
          {{ editingIntegrante ? 'Editar Integrante' : 'Crear Nuevo Integrante' }}
        </v-card-title>
        <v-card-text class="pa-4">
          <v-form ref="integranteForm" v-model="integranteFormValid" @submit.prevent="guardarIntegrante">
            <v-text-field
              v-model="integranteFormData.nombre"
              label="Nombre del integrante"
              :rules="[v => !!v || 'El nombre es requerido']"
              required
            ></v-text-field>
            
            <v-text-field
              v-model="integranteFormData.apodo"
              label="Apodo (opcional)"
            ></v-text-field>
            
            <v-select
              v-model="integranteFormData.id_usuario"
              :items="usuarios"
              item-title="nombre"
              item-value="id"
              label="Usuario asociado (opcional)"
              hint="Asocia este integrante a un usuario del sistema"
              persistent-hint
              clearable
            >
              <template v-slot:item="{ item, props }">
                <v-list-item v-bind="props" :subtitle="item.raw.email"></v-list-item>
              </template>
            </v-select>
            
            <v-autocomplete
              v-model="integranteFormData.roles"
              :items="roles"
              item-title="nombre"
              item-value="id"
              label="Roles musicales"
              multiple
              chips
              :rules="[v => v.length > 0 || 'Selecciona al menos un rol']"
            >
              <template v-slot:selection="{ item }">
                <v-chip size="small" color="info">{{ item.title }}</v-chip>
              </template>
            </v-autocomplete>
          </v-form>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showIntegranteDialog = false">
            Cancelar
          </v-btn>
          <v-btn 
            color="primary" 
            variant="elevated" 
            @click="guardarIntegrante" 
            :loading="savingIntegrante"
            :disabled="!integranteFormValid"
          >
            Guardar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog de confirmación para eliminar -->
    <v-dialog v-model="showConfirmDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5 bg-error text-white pa-4">
          Confirmar eliminación
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <p>{{ confirmMessage }}</p>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="showConfirmDialog = false">
            Cancelar
          </v-btn>
          <v-btn 
            color="error" 
            variant="elevated" 
            @click="confirmarEliminar" 
            :loading="deleting"
          >
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar para notificaciones -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="snackbar.show = false"
        >
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/authService';
import usuariosService from '@/services/usuariosService';
import integrantesService from '@/services/integrantesService';
import rolesService from '@/services/rolesService';

const router = useRouter();

// Estado de las pestañas
const activeTab = ref('usuarios');

// Estados para las tablas
const usuarios = ref([]);
const integrantes = ref([]);
const roles = ref([]);
const loadingUsuarios = ref(true);
const loadingIntegrantes = ref(true);
const loadingRoles = ref(true);
const searchUsuarios = ref('');
const searchIntegrantes = ref('');

// Estado para diálogos
const showUserDialog = ref(false);
const showIntegranteDialog = ref(false);
const showCreateUserDialog = ref(false);
const showCreateIntegranteDialog = ref(false);
const showConfirmDialog = ref(false);
const editingUser = ref(null);
const editingIntegrante = ref(null);
const savingUser = ref(false);
const savingIntegrante = ref(false);
const deleting = ref(false);
const confirmMessage = ref('');
const deleteCallback = ref(null);

// Estado para formularios
const userFormData = ref({
  id: null,
  nombre: '',
  email: '',
  password: '',
  rol_plataforma: 'regular'
});

const integranteFormData = ref({
  id: null,
  nombre: '',
  apodo: '',
  id_usuario: null,
  roles: []
});

const userFormValid = ref(false);
const integranteFormValid = ref(false);
const userForm = ref(null);
const integranteForm = ref(null);

// Estado para notificaciones
const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
});

// Cabeceras para las tablas
const usuariosHeaders = [
  { title: 'Nombre', key: 'nombre' },
  { title: 'Email', key: 'email' },
  { title: 'Rol', key: 'es_admin' },  // Mantenemos la key pero mostramos rol_plataforma
  { title: 'Acciones', key: 'actions', sortable: false, align: 'end' }
];

const integrantesHeaders = [
  { title: 'Nombre', key: 'nombre' },
  { title: 'Apodo', key: 'apodo' },
  { title: 'Roles', key: 'roles' },
  { title: 'Usuario Asociado', key: 'usuario' },
  { title: 'Acciones', key: 'actions', sortable: false, align: 'end' }
];

// Datos filtrados para las tablas
const filteredUsuarios = computed(() => {
  if (!searchUsuarios.value) return usuarios.value;
  const searchTerm = searchUsuarios.value.toLowerCase();
  return usuarios.value.filter(usuario => 
    usuario.nombre.toLowerCase().includes(searchTerm) || 
    usuario.email.toLowerCase().includes(searchTerm)
  );
});

const filteredIntegrantes = computed(() => {
  if (!searchIntegrantes.value) return integrantes.value;
  const searchTerm = searchIntegrantes.value.toLowerCase();
  return integrantes.value.filter(integrante => 
    integrante.nombre.toLowerCase().includes(searchTerm) || 
    (integrante.apodo && integrante.apodo.toLowerCase().includes(searchTerm))
  );
});

// Cargar datos iniciales
onMounted(async () => {
  // Verificar si el usuario es administrador
  try {
    const currentUser = await authService.getCurrentUser();
    if (currentUser.data.rol_plataforma !== 'admin') {
      mostrarNotificacion('No tienes permiso para acceder a esta sección', 'error');
      router.push('/calendar');
      return;
    }
    
    // Cargar datos
    cargarUsuarios();
    cargarIntegrantes();
    cargarRoles();
  } catch (error) {
    console.error('Error al verificar permisos:', error);
    router.push('/calendar');
  }
});

// Métodos para cargar datos
async function cargarUsuarios() {
  loadingUsuarios.value = true;
  try {
    const response = await usuariosService.getUsuarios();
    usuarios.value = response.data;
  } catch (error) {
    console.error('Error al cargar usuarios:', error);
    mostrarNotificacion('Error al cargar usuarios', 'error');
  } finally {
    loadingUsuarios.value = false;
  }
}

async function cargarIntegrantes() {
  loadingIntegrantes.value = true;
  try {
    const response = await integrantesService.getIntegrantes();
    integrantes.value = response.data;
  } catch (error) {
    console.error('Error al cargar integrantes:', error);
    mostrarNotificacion('Error al cargar integrantes', 'error');
  } finally {
    loadingIntegrantes.value = false;
  }
}

async function cargarRoles() {
  loadingRoles.value = true;
  try {
    const response = await rolesService.getRoles();
    roles.value = response.data;
  } catch (error) {
    console.error('Error al cargar roles:', error);
    mostrarNotificacion('Error al cargar roles musicales', 'error');
  } finally {
    loadingRoles.value = false;
  }
}

// Métodos para usuarios
function editarUsuario(usuario) {
  editingUser.value = usuario;
  userFormData.value = {
    id: usuario.id,
    nombre: usuario.nombre,
    email: usuario.email,
    password: '',  // No se pide la contraseña al editar
    rol_plataforma: usuario.rol_plataforma
  };
  showUserDialog.value = true;
}

async function guardarUsuario() {
  savingUser.value = true;
  try {
    if (editingUser.value) {
      // Actualizar usuario existente
      await usuariosService.updateUsuario(userFormData.value.id, {
        nombre: userFormData.value.nombre,
        email: userFormData.value.email,
        rol_plataforma: userFormData.value.rol_plataforma
      });
      mostrarNotificacion('Usuario actualizado con éxito', 'success');
    } else {
      // Crear nuevo usuario
      await usuariosService.createUsuario({
        nombre: userFormData.value.nombre,
        email: userFormData.value.email,
        password: userFormData.value.password,
        rol_plataforma: userFormData.value.rol_plataforma
      });
      mostrarNotificacion('Usuario creado con éxito', 'success');
    }
    
    // Recargar usuarios y cerrar diálogo
    await cargarUsuarios();
    showUserDialog.value = false;
    resetUserForm();
  } catch (error) {
    console.error('Error al guardar usuario:', error);
    mostrarNotificacion('Error al guardar usuario', 'error');
  } finally {
    savingUser.value = false;
  }
}

function resetUserForm() {
  userFormData.value = {
    id: null,
    nombre: '',
    email: '',
    password: '',
    rol_plataforma: 'regular'
  };
  editingUser.value = null;
}

async function convertirAdmin(usuario) {
  try {
    await usuariosService.updateUsuario(usuario.id, {
      rol_plataforma: 'admin'
    });
    mostrarNotificacion(`${usuario.nombre} ahora es administrador`, 'success');
    await cargarUsuarios();
  } catch (error) {
    console.error('Error al convertir en administrador:', error);
    mostrarNotificacion('Error al cambiar permisos', 'error');
  }
}

function confirmarEliminarUsuario(usuario) {
  confirmMessage.value = `¿Estás seguro de eliminar al usuario ${usuario.nombre}?`;
  deleteCallback.value = async () => {
    try {
      await usuariosService.deleteUsuario(usuario.id);
      mostrarNotificacion('Usuario eliminado con éxito', 'success');
      await cargarUsuarios();
    } catch (error) {
      console.error('Error al eliminar usuario:', error);
      mostrarNotificacion('Error al eliminar usuario', 'error');
    }
  };
  showConfirmDialog.value = true;
}

// Métodos para integrantes
function editarIntegrante(integrante) {
  editingIntegrante.value = integrante;
  integranteFormData.value = {
    id: integrante.id,
    nombre: integrante.nombre,
    apodo: integrante.apodo || '',
    id_usuario: integrante.id_usuario,
    roles: integrante.roles.map(rol => rol.id)
  };
  showIntegranteDialog.value = true;
}

async function guardarIntegrante() {
  savingIntegrante.value = true;
  try {
    if (editingIntegrante.value) {
      // Actualizar integrante existente
      await integrantesService.updateIntegrante(integranteFormData.value.id, {
        nombre: integranteFormData.value.nombre,
        apodo: integranteFormData.value.apodo,
        id_usuario: integranteFormData.value.id_usuario,
        roles: integranteFormData.value.roles
      });
      mostrarNotificacion('Integrante actualizado con éxito', 'success');
    } else {
      // Crear nuevo integrante
      await integrantesService.createIntegrante({
        nombre: integranteFormData.value.nombre,
        apodo: integranteFormData.value.apodo,
        id_usuario: integranteFormData.value.id_usuario,
        roles: integranteFormData.value.roles
      });
      mostrarNotificacion('Integrante creado con éxito', 'success');
    }
    
    // Recargar integrantes y cerrar diálogo
    await cargarIntegrantes();
    showIntegranteDialog.value = false;
    resetIntegranteForm();
  } catch (error) {
    console.error('Error al guardar integrante:', error);
    mostrarNotificacion('Error al guardar integrante', 'error');
  } finally {
    savingIntegrante.value = false;
  }
}

function resetIntegranteForm() {
  integranteFormData.value = {
    id: null,
    nombre: '',
    apodo: '',
    id_usuario: null,
    roles: []
  };
  editingIntegrante.value = null;
}

function confirmarEliminarIntegrante(integrante) {
  confirmMessage.value = `¿Estás seguro de eliminar al integrante ${integrante.nombre}?`;
  deleteCallback.value = async () => {
    try {
      await integrantesService.deleteIntegrante(integrante.id);
      mostrarNotificacion('Integrante eliminado con éxito', 'success');
      await cargarIntegrantes();
    } catch (error) {
      console.error('Error al eliminar integrante:', error);
      mostrarNotificacion('Error al eliminar integrante', 'error');
    }
  };
  showConfirmDialog.value = true;
}

// Método para confirmar eliminación
async function confirmarEliminar() {
  deleting.value = true;
  try {
    await deleteCallback.value();
    showConfirmDialog.value = false;
  } catch (error) {
    console.error('Error en eliminación:', error);
  } finally {
    deleting.value = false;
  }
}

// Método para mostrar notificaciones
function mostrarNotificacion(texto, color = 'success') {
  snackbar.value = {
    show: true,
    text: texto,
    color: color
  };
}

// Watchers para diálogos de creación
watch(showCreateUserDialog, (newVal) => {
  if (newVal) {
    resetUserForm();
    showUserDialog.value = true;
    showCreateUserDialog.value = false;
  }
});

watch(showCreateIntegranteDialog, (newVal) => {
  if (newVal) {
    resetIntegranteForm();
    showIntegranteDialog.value = true;
    showCreateIntegranteDialog.value = false;
  }
});
</script>

<style scoped>
.v-data-table :deep(th) {
  font-weight: 600;
  color: rgba(0, 0, 0, 0.87);
  background-color: #f5f5f5;
}

.v-tabs :deep(.v-tab) {
  font-weight: 500;
  letter-spacing: 0.5px;
}

.v-card :deep(.v-card-title) {
  line-height: 1.2;
}
</style>
