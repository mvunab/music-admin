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
            no-data-text="No hay canciones en el repertorio. ¡Agrega algunas!"
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

            <template v-slot:[`item.title`]="{ item }">
              <router-link v-if="item.id" :to="{ name: 'SongSheet', params: { id: item.id } }" class="song-title-link">
                {{ item.title }}
              </router-link>
              <span v-else>{{ item.title }} <em class="text-caption text-error">(ID no disponible)</em></span>
            </template>

            <template v-slot:[`item.category`]="{ item }">
              <v-chip :color="item.category === 'REP' ? 'blue' : 'green'" size="small" label>
                {{ item.category }}
              </v-chip>
            </template>

            <template v-slot:[`item.originalTonality`]="{ item }">
              <span>{{ item.originalTonality || '-' }}</span>
            </template>

            <template v-slot:[`item.bpm`]="{ item }">
              <span>{{ item.bpm || '-' }}</span>
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

            <template v-slot:[`item.viewChords`]="{ item }">
              <v-tooltip location="top" text="Ver Letra y Acordes">
                <template v-slot:activator="{ props: tooltipProps }">
                  <v-btn
                    v-if="item.id"
                    icon
                    variant="tonal" 
                    color="primary"   
                    size="small"
                    :to="{ name: 'SongSheet', params: { id: item.id } }"
                    v-bind="tooltipProps"
                    aria-label="Ver letra y acordes de la canción"
                  >
                    <v-icon>mdi-text-box-search-outline</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
              <v-tooltip location="top" text="Editar Canción">
                  <template v-slot:activator="{ props: tooltipProps }">
                    <v-btn icon="mdi-pencil-outline" variant="text" color="info" size="small" class="mr-1" @click="editSong(item)" v-bind="tooltipProps"></v-btn>
                  </template>
              </v-tooltip>
              <v-tooltip location="top" text="Eliminar Canción">
                  <template v-slot:activator="{ props: tooltipProps }">
                    <v-btn icon="mdi-delete-outline" variant="text" color="error" size="small" @click="deleteSongDialog(item)" v-bind="tooltipProps"></v-btn>
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
                  <v-text-field v-model="currentSong.title" label="Título" :rules="[v => !!v || 'Requerido']" required prepend-inner-icon="mdi-text-short" variant="outlined" density="compact"></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select v-model="currentSong.category" :items="['REP', 'PROP']" label="Categoría" :rules="[v => !!v || 'Requerido']" required prepend-inner-icon="mdi-tag-outline" variant="outlined" density="compact"></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select v-model="currentSong.originalTonality" :items="tonalidadesDisponibles" label="Tono Original" :rules="[v => !!v || 'Requerido']" required prepend-inner-icon="mdi-music-accidental-sharp" variant="outlined" density="compact" clearable></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field v-model.number="currentSong.bpm" label="BPM" type="number" prepend-inner-icon="mdi-metronome" variant="outlined" density="compact" clearable></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field v-model="currentSong.youtubeLink" label="Link YouTube" prepend-inner-icon="mdi-youtube" :rules="[v => !v || /^https?:\/\/(www\.)?(youtube\.com|youtu\.be)\/.+$/.test(v) || 'Link inválido']" variant="outlined" density="compact" clearable></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="currentSong.docsLink" label="Link Letra (Docs)" prepend-inner-icon="mdi-file-document-outline" :rules="[v => !v || /^https?:\/\/.+$/.test(v) || 'Link inválido']" variant="outlined" density="compact" clearable></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea v-model="currentSong.lyricsWithChords" label="Letra y Acordes (Tono Original)" placeholder="Ej: [G]Esta es la [C]letra..." prepend-inner-icon="mdi-text-long" variant="outlined" density="compact" rows="8" auto-grow clearable></v-textarea>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions class="px-6 pb-4">
            <v-spacer></v-spacer>
            <v-btn variant="text" @click="closeSongDialog">Cancelar</v-btn>
            <v-btn color="primary" type="submit" :loading="songDialog.loading" :disabled="!isSongFormValid || songDialog.loading">{{ songDialog.isEditMode ? 'Guardar' : 'Agregar' }}</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>

    <v-dialog v-model="confirmDeleteDialog.show" max-width="400px" persistent>
      <v-card rounded="lg">
        <v-card-title class="text-h5 error--text"><v-icon start color="error">mdi-alert-circle-outline</v-icon>Confirmar</v-card-title>
        <v-card-text class="pt-3">¿Eliminar "<strong>{{ confirmDeleteDialog.songTitle }}</strong>"?</v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="confirmDeleteDialog.show = false">Cancelar</v-btn>
          <v-btn color="error" variant="flat" @click="confirmDelete" :loading="confirmDeleteDialog.loading">Eliminar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="4000" location="top center" rounded="pill">
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

const API_DOMAIN = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const API_PREFIX = '/api/v1';
const API_SONGS_COLLECTION_URL = `${API_DOMAIN}${API_PREFIX}/songs/`;
const API_SONGS_ITEM_URL = `${API_DOMAIN}${API_PREFIX}/songs`;

const allSongs = ref([]);
const loadingTable = ref(false);
const search = ref('');
const songFormRef = ref(null);
const isSongFormValid = ref(null);

const headers = ref([
  { title: 'Título', key: 'title', align: 'start', sortable: true, width: '25%' },
  { title: 'Categoría', key: 'category', sortable: true, width: '10%' },
  { title: 'Tono Original', key: 'originalTonality', sortable: true, width: '10%' },
  { title: 'BPM', key: 'bpm', sortable: true, width: '10%' },
  { title: 'Video', key: 'youtubeLink', sortable: false, align: 'center', width: '10%' },
  { title: 'Letra Link', key: 'docsLink', sortable: false, align: 'center', width: '10%' },
  { title: 'Acordes', key: 'viewChords', sortable: false, align: 'center', width: '10%' },
  { title: 'Acciones', key: 'actions', sortable: false, align: 'end', width: '10%' },
]);

const songDialog = ref({ show: false, isEditMode: false, loading: false });
const defaultSongItem = { 
    id: null, title: '', category: 'REP', originalTonality: '', 
    bpm: null, youtubeLink: '', docsLink: '', lyricsWithChords: ''
};
const currentSong = ref({ ...defaultSongItem });

const snackbar = ref({ show: false, message: '', color: '' });
const confirmDeleteDialog = ref({ show: false, songId: null, songTitle: '', loading: false });

const tonalidadesDisponibles = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B', 'Am', 'A#m', 'Bbm', 'Bm', 'Cm', 'C#m', 'Dbm', 'Dm', 'D#m', 'Ebm', 'Em', 'Fm', 'F#m', 'Gbm', 'Gm', 'G#m', 'Abm'];

const fetchSongs = async () => {
  loadingTable.value = true;
  try {
    const response = await axios.get(API_SONGS_COLLECTION_URL); 
    if (response && response.data && Array.isArray(response.data)) {
        allSongs.value = response.data; 
    } else {
        console.error("Respuesta de API para canciones no es un array válido:", response);
        allSongs.value = [];
    }
  } catch (error) {
    console.error("Error cargando canciones:", error.response ? error.response.data : error.message);
    snackbar.value = { show: true, message: 'Error al cargar canciones.', color: 'error' };
    allSongs.value = [];
  } finally {
    loadingTable.value = false;
  }
};

const openSongDialog = (song = null) => {
  if (song && song.id) {
    songDialog.value.isEditMode = true;
    currentSong.value = { ...defaultSongItem, ...song }; 
  } else {
    songDialog.value.isEditMode = false;
    currentSong.value = { ...defaultSongItem };
  }
  setTimeout(() => { if (songFormRef.value) songFormRef.value.resetValidation(); }, 0);
  songDialog.value.show = true;
};

const closeSongDialog = () => { songDialog.value.show = false; songDialog.value.loading = false; };

const saveSong = async () => {
  if (!songFormRef.value) return;
  const { valid } = await songFormRef.value.validate();
  if (!valid) {
    snackbar.value = { show: true, message: 'Por favor, completa los campos requeridos.', color: 'warning' };
    return;
  }
  songDialog.value.loading = true;
  const songDataToSave = { ...currentSong.value }; 
  if (songDataToSave.bpm === '' || songDataToSave.bpm === undefined || isNaN(parseInt(songDataToSave.bpm))) songDataToSave.bpm = null;
  else songDataToSave.bpm = parseInt(songDataToSave.bpm);
  if (songDataToSave.youtubeLink === '') songDataToSave.youtubeLink = null;
  if (songDataToSave.docsLink === '') songDataToSave.docsLink = null;
  if (songDataToSave.lyricsWithChords === '') songDataToSave.lyricsWithChords = null;

  try {
    if (songDialog.value.isEditMode && songDataToSave.id) {
      await axios.put(`${API_SONGS_ITEM_URL}/${songDataToSave.id}`, songDataToSave);
      snackbar.value = { show: true, message: 'Canción actualizada.', color: 'success' };
    } else {
      const { id, ...newSongData } = songDataToSave;
      await axios.post(API_SONGS_COLLECTION_URL, newSongData);
      snackbar.value = { show: true, message: 'Canción agregada.', color: 'success' };
    }
    closeSongDialog();
    await fetchSongs(); 
  } catch (error) {
    let errorMsg = `Error al ${songDialog.value.isEditMode ? 'actualizar' : 'agregar'} canción.`;
    if (error.response?.data?.detail) errorMsg = typeof error.response.data.detail === 'string' ? error.response.data.detail : JSON.stringify(error.response.data.detail);
    snackbar.value = { show: true, message: errorMsg, color: 'error' };
  } finally {
     songDialog.value.loading = false;
  }
};
const editSong = (song) => openSongDialog(song);
const deleteSongDialog = (song) => { confirmDeleteDialog.value = { show: true, songId: song.id, songTitle: song.title, loading: false }; };
const confirmDelete = async () => { 
    if (!confirmDeleteDialog.value.songId) return;
    confirmDeleteDialog.value.loading = true;
    try {
        await axios.delete(`${API_SONGS_ITEM_URL}/${confirmDeleteDialog.value.songId}`);
        snackbar.value = { show: true, message: 'Canción eliminada.', color: 'success' };
        await fetchSongs();
    } catch (error) {
        snackbar.value = { show: true, message: 'Error al eliminar.', color: 'error' };
    } finally {
        confirmDeleteDialog.value.show = false;
        confirmDeleteDialog.value.loading = false;
    }
};
onMounted(fetchSongs);
</script>

<style scoped>
.v-fab {}
.v-data-table { margin-bottom: 80px; }
.song-title-link { color: var(--v-theme-on-surface); text-decoration: none; font-weight: 500; }
.song-title-link:hover { color: var(--v-theme-primary); text-decoration: underline; }
</style>