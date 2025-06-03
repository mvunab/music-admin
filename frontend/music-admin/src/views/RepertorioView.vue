// src/views/RepertorioView.vue
<template>
  <v-container fluid class="pa-md-6 pa-3">
    <v-row>
      <v-col>
        <div class="d-flex justify-space-between align-center mb-6">
          <h1 class="text-h4 font-weight-medium">Repertorio de Canciones</h1>
        </div>

        <v-card rounded="xl">
          <v-data-table
            :headers="headers"
            :items="allSongs"
            item-value="id"
            class="elevation-1"
            :search="search"
            :loading="loadingTable"
            loading-text="Cargando canciones..."
            no-data-text="No hay canciones en el repertorio."
            hover
            hide-default-footer 
          >
            <template v-slot:top>
              <v-toolbar flat color="white">
                <v-toolbar-title class="text-subtitle-1">Lista de Canciones</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-text-field
                  v-model="search"
                  density="compact"
                  label="Buscar canción (título, categoría, etc.)"
                  prepend-inner-icon="mdi-magnify"
                  variant="solo-filled"
                  flat
                  hide-details
                  single-line
                  class="mr-2"
                ></v-text-field>
              </v-toolbar>
            </template>

            <template v-slot:[`item.category`]="{ item }">
              <v-chip :color="item.category === 'REP' ? 'blue' : 'green'" size="small" label>
                {{ item.category }}
              </v-chip>
            </template>

            <template v-slot:[`item.youtubeLink`]="{ item }">
              <v-btn
                v-if="item.youtubeLink"
                icon
                variant="text"
                color="red"
                size="small"
                :href="item.youtubeLink"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Ver video en YouTube"
              >
                <v-icon>mdi-youtube</v-icon>
              </v-btn>
              <span v-else>-</span>
            </template>

            <template v-slot:[`item.docsLink`]="{ item }">
              <v-btn
                v-if="item.docsLink"
                icon
                variant="text"
                color="blue-darken-2"
                size="small"
                :href="item.docsLink"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Ver letra del documento"
              >
                <v-icon>mdi-file-document-outline</v-icon>
              </v-btn>
              <span v-else>-</span>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <v-tooltip location="top" text="Editar Canción">
                  <template v-slot:activator="{ props }">
                    <v-btn icon="mdi-pencil-outline" variant="text" color="info" size="small" class="mr-1" @click="editSong(item)" v-bind="props"></v-btn>
                  </template>
              </v-tooltip>
              <v-tooltip location="top" text="Eliminar Canción">
                  <template v-slot:activator="{ props }">
                    <v-btn icon="mdi-delete-outline" variant="text" color="error" size="small" @click="deleteSongDialog(item)" v-bind="props"></v-btn>
                  </template>
              </v-tooltip>
            </template>

          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-fab
        icon="mdi-plus"
        location="bottom end"
        size="large"
        color="green-darken-1"
        app
        appear
        class="mb-4 mr-4"
        @click="openSongDialog()"
        aria-label="Agregar nueva canción"
    ></v-fab>

    <v-dialog v-model="songDialog.show" max-width="700px" persistent scrollable>
      <v-card rounded="lg">
        <v-form ref="songFormRef" v-model="isSongFormValid" @submit.prevent="saveSong">
          <v-card-title class="text-h5 pt-4 px-6">
            {{ songDialog.isEditMode ? 'Editar Canción' : 'Agregar Nueva Canción' }}
          </v-card-title>
          <v-card-text class="px-6 py-2">
            <v-container>
              <v-row dense>
                <v-col cols="12">
                  <v-text-field
                    v-model="currentSong.title"
                    label="Título de la Canción"
                    :rules="[v => !!v || 'El título es requerido']"
                    required
                    prepend-inner-icon="mdi-text-short"
                    variant="outlined"
                    density="compact"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="currentSong.category"
                    :items="['REP', 'PROP']"
                    label="Categoría"
                    :rules="[v => !!v || 'La categoría es requerida']"
                    required
                    prepend-inner-icon="mdi-tag-outline"
                    variant="outlined"
                    density="compact"
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="currentSong.tonality"
                    :items="tonalidadesDisponibles"
                    label="Tonalidad"
                    prepend-inner-icon="mdi-music-accidental-sharp"
                    variant="outlined"
                    density="compact"
                    clearable
                    :rules="[v => !!v || 'La tonalidad es requerida']"
                    required
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="currentSong.bpm"
                    label="BPM (Tempo)"
                    type="number"
                    prepend-inner-icon="mdi-metronome"
                    variant="outlined"
                    density="compact"
                    clearable
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="currentSong.youtubeLink"
                    label="Link Video YouTube"
                    prepend-inner-icon="mdi-youtube"
                    placeholder="https://www.youtube.com/watch?v=..."
                    :rules="[v => !v || /^https?:\/\/(www\.)?(youtube\.com|youtu\.be)\/.+$/.test(v) || 'Debe ser un link válido de YouTube']"
                    variant="outlined"
                    density="compact"
                    clearable
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="currentSong.docsLink"
                    label="Link Letra (Google Docs, etc.)"
                    prepend-inner-icon="mdi-file-document-outline"
                    placeholder="https://docs.google.com/document/d/..."
                    :rules="[v => !v || /^https?:\/\/.+$/.test(v) || 'Debe ser un link válido']"
                    variant="outlined"
                    density="compact"
                    clearable
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions class="px-6 pb-4">
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="closeSongDialog">Cancelar</v-btn>
            <v-btn 
              color="primary" 
              type="submit"
              :loading="songDialog.loading"
              :disabled="!isSongFormValid || songDialog.loading"
            >
              {{ songDialog.isEditMode ? 'Guardar Cambios' : 'Agregar Canción' }}
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>

    <v-dialog v-model="confirmDeleteDialog.show" max-width="400px" persistent>
        <v-card rounded="lg">
            <v-card-title class="text-h5 error--text"> <v-icon start color="error">mdi-alert-circle-outline</v-icon> Confirmar Eliminación</v-card-title>
            <v-card-text class="pt-3">
                ¿Estás seguro de que quieres eliminar la canción "<strong>{{ confirmDeleteDialog.songTitle }}</strong>"? Esta acción no se puede deshacer.
            </v-card-text>
            <v-card-actions class="pa-4">
                <v-spacer></v-spacer>
                <v-btn variant="text" @click="confirmDeleteDialog.show = false">Cancelar</v-btn>
                <v-btn color="error" variant="flat" @click="confirmDelete" :loading="confirmDeleteDialog.loading">Eliminar</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>

     <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000" location="top center" rounded="pill">
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn icon="mdi-close" variant="text" @click="snackbar.show = false"></v-btn>
      </template>
    </v-snackbar>

  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'; // Ajusta según tu backend

const allSongs = ref([]);
const loadingTable = ref(false);
const search = ref('');
const songFormRef = ref(null);
const isSongFormValid = ref(null);

const headers = ref([
  { title: 'Título', key: 'title', align: 'start', sortable: true, width: '30%' },
  { title: 'Categoría', key: 'category', sortable: true, width: '10%' },
  { title: 'Tonalidad', key: 'tonality', sortable: true, width: '10%' },
  { title: 'BPM', key: 'bpm', sortable: true, width: '10%' },
  { title: 'Video', key: 'youtubeLink', sortable: false, align: 'center', width: '10%' },
  { title: 'Letra', key: 'docsLink', sortable: false, align: 'center', width: '10%' },
  { title: 'Acciones', key: 'actions', sortable: false, align: 'end', width: '10%' },
]);

const songDialog = ref({ show: false, isEditMode: false, loading: false });
const defaultSongItem = { id: null, title: '', category: 'REP', tonality: '', bpm: null, youtubeLink: '', docsLink: '' };
const currentSong = ref({ ...defaultSongItem });

const snackbar = ref({ show: false, message: '', color: '' });
const confirmDeleteDialog = ref({ show: false, songId: null, songTitle: '', loading: false });

const tonalidadesDisponibles = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B', 'Am', 'A#m', 'Bbm', 'Bm', 'Cm', 'C#m', 'Dbm', 'Dm', 'D#m', 'Ebm', 'Em', 'Fm', 'F#m', 'Gbm', 'Gm', 'G#m', 'Abm'];

const fetchSongs = async () => {
  loadingTable.value = true;
  try {
    // const response = await axios.get(`${API_BASE_URL}/songs`);
    // allSongs.value = response.data;
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulación
    allSongs.value = [
      { id: 's1', title: 'Cuán Grande es Él', category: 'REP', tonality: 'G', bpm: 72, youtubeLink: 'https://www.youtube.com/watch?v=example1', docsLink: 'https://docs.google.com/document/d/exampledoc1' },
      { id: 's2', title: 'Dios Imparable', category: 'PROP', tonality: 'Bm', bpm: 120, youtubeLink: 'https://www.youtube.com/watch?v=example2', docsLink: '' },
      { id: 's3', title: 'Sublime Gracia', category: 'REP', tonality: 'C', bpm: 60, youtubeLink: '', docsLink: 'https://docs.google.com/document/d/exampledoc2' },
      { id: 's4', title: 'Renuévame', category: 'PROP', tonality: 'D', bpm: 80, youtubeLink: 'https://www.youtube.com/watch?v=example3', docsLink: 'https://docs.google.com/document/d/exampledoc3' },
    ];
  } catch (error) {
    console.error("Error fetching songs:", error);
    snackbar.value = { show: true, message: 'Error al cargar canciones.', color: 'error' };
  } finally {
    loadingTable.value = false;
  }
};

const openSongDialog = (song = null) => {
  if (song) {
    songDialog.value.isEditMode = true;
    currentSong.value = { ...song };
  } else {
    songDialog.value.isEditMode = false;
    currentSong.value = { ...defaultSongItem };
  }
  // Esperar al siguiente ciclo de tick para que el formulario esté en el DOM si se estaba ocultando
  // y luego resetear la validación.
  setTimeout(() => {
    if (songFormRef.value) {
        songFormRef.value.resetValidation();
    }
  }, 0);
  songDialog.value.show = true;
};

const closeSongDialog = () => {
  songDialog.value.show = false;
  songDialog.value.loading = false;
};

const saveSong = async () => {
  if (!songFormRef.value) return;
  const { valid } = await songFormRef.value.validate();
  if (!valid) {
    snackbar.value = { show: true, message: 'Por favor, completa los campos requeridos.', color: 'warning' };
    return;
  }

  songDialog.value.loading = true;
  const songData = { ...currentSong.value };

  try {
    if (songDialog.value.isEditMode) {
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulación
      const index = allSongs.value.findIndex(s => s.id === songData.id);
      if (index !== -1) allSongs.value.splice(index, 1, songData);
      snackbar.value = { show: true, message: 'Canción actualizada exitosamente.', color: 'success' };
    } else {
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulación
      const newSongWithId = { ...songData, id: `s${Date.now()}` };
      allSongs.value.push(newSongWithId);
      snackbar.value = { show: true, message: 'Canción agregada exitosamente.', color: 'success' };
    }
    closeSongDialog();
  } catch (error) {
    console.error("Error saving song:", error);
    snackbar.value = { show: true, message: `Error al ${songDialog.value.isEditMode ? 'actualizar' : 'agregar'} canción.`, color: 'error' };
  } finally {
     songDialog.value.loading = false;
  }
};

const editSong = (song) => {
  openSongDialog(song);
};

const deleteSongDialog = (song) => {
    confirmDeleteDialog.value = {
        show: true,
        songId: song.id,
        songTitle: song.title,
        loading: false,
    };
};

const confirmDelete = async () => {
    if (!confirmDeleteDialog.value.songId) return;
    confirmDeleteDialog.value.loading = true;
    try {
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulación
        allSongs.value = allSongs.value.filter(s => s.id !== confirmDeleteDialog.value.songId);
        snackbar.value = { show: true, message: 'Canción eliminada exitosamente.', color: 'success' };
    } catch (error) {
        console.error("Error deleting song:", error);
        snackbar.value = { show: true, message: 'Error al eliminar la canción.', color: 'error' };
    } finally {
        confirmDeleteDialog.value.show = false;
        confirmDeleteDialog.value.loading = false;
    }
};

onMounted(() => {
  fetchSongs();
});

</script>

<style scoped>
.v-fab {
  /* Las props 'app' y 'location' ya manejan bien el posicionamiento */
}
.v-data-table {
  margin-bottom: 80px; 
}
</style>