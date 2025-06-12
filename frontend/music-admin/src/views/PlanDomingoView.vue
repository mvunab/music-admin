<template>
  <v-container class="pa-md-6 pa-3">
    <v-row>
      <v-col>
        <!-- Header y navegación de mes -->
        <div class="d-none d-md-flex justify-space-between align-center mb-6 flex-wrap ga-2">
          <h1 class="text-h4 font-weight-medium">Planificar Mes</h1>
          <v-btn to="/calendar" variant="text" color="primary" prepend-icon="mdi-arrow-left">
            Volver a Agenda
          </v-btn>
        </div>

        <!-- Navegación de mes: móvil -->
        <v-row class="mb-4 d-flex d-md-none" justify="center">
          <v-col cols="12" class="d-flex flex-wrap align-center justify-center text-center ga-2">
            <v-btn icon size="small" @click="changeTargetMonth(-1)" aria-label="Mes anterior">
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            <div class="text-subtitle-1 mx-2">{{ monthYearDisplay(targetPlanMonth) }}</div>
            <v-btn icon size="small" @click="changeTargetMonth(1)" aria-label="Mes siguiente">
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
            <v-btn size="small" class="mt-2 mt-sm-0 ml-sm-4" variant="outlined" @click="goToCurrentPlanningMonth">
              Mes Actual
            </v-btn>
          </v-col>
        </v-row>

        <!-- Navegación de mes: desktop -->
        <v-row class="mb-6 d-none d-md-flex" justify="center" align="center">
          <v-btn icon @click="changeTargetMonth(-1)" aria-label="Mes anterior para planificar">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <span class="text-h5 mx-4">{{ monthYearDisplay(targetPlanMonth) }}</span>
          <v-btn icon @click="changeTargetMonth(1)" aria-label="Mes siguiente para planificar">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
          <v-btn @click="goToCurrentPlanningMonth" variant="outlined" class="ml-4" size="small">Mes Actual</v-btn>
        </v-row>

        <v-card rounded="xl" class="pa-sm-6 pa-4">
          <v-form ref="planFormRef" v-model="isFormValid" @submit.prevent="submitPlanificacion">
            <!-- Existing inputs section -->
            <v-row class="g-4">
              <v-col cols="12" class="mb-4">
                <v-select v-model="planificacion.selectedSunday" :items="availableSundaysForSelectedMonth"
                  item-title="text" item-value="value" label="Seleccionar Domingo del Servicio"
                  prepend-inner-icon="mdi-calendar-today" variant="outlined" density="comfortable" clearable
                  :rules="[v => !!v || 'Debe seleccionar un Domingo']"
                  :hint="availableSundaysForSelectedMonth.length === 0 ? `No hay Domingos futuros disponibles en ${monthYearDisplay(targetPlanMonth)}` : 'Solo se muestran Domingos futuros'"
                  persistent-hint :no-data-text="`No hay Domingos futuros en ${monthYearDisplay(targetPlanMonth)}`" />
              </v-col>

              <v-col cols="12" class="mb-4">
                <v-select v-model="planificacion.personInCharge" :items="listaPersonasACargo" item-title="name"
                  item-value="id" label="Seleccionar Persona a Cargo (Director)"
                  prepend-inner-icon="mdi-account-tie-outline" variant="outlined" density="comfortable" clearable
                  :rules="[v => !!v || 'Debe seleccionar una persona a cargo']" />
              </v-col>

              <v-col cols="12" class="mb-4">
                <v-autocomplete v-model="planificacion.selectedMusicians" :items="listaMusicos" item-title="name"
                  item-value="id" label="Seleccionar Músicos" prepend-inner-icon="mdi-guitar-acoustic" multiple chips
                  closable-chips variant="outlined" density="comfortable" clearable hint="Selecciona uno o más músicos"
                  persistent-hint>
                  <template v-slot:chip="{ props, item }">
                    <v-chip v-bind="props" :text="item.raw.name"></v-chip>
                  </template>
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :title="item.raw.name" :subtitle="item.raw.instrument"></v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col cols="12" class="mb-4">
                <v-autocomplete v-model="planificacion.selectedChoir" :items="listaCoro" item-title="name"
                  item-value="id" label="Seleccionar Miembros del Coro" prepend-inner-icon="mdi-account-group-outline"
                  multiple chips closable-chips variant="outlined" density="comfortable" clearable
                  hint="Selecciona uno o más miembros del coro" persistent-hint />
              </v-col>
            </v-row>

            <v-divider class="my-6"></v-divider>

            <!-- Modified Songs Section -->
            <h2 class="text-h6 mb-4">Canciones</h2>
            <div v-for="(song, index) in planificacion.songs" :key="index" class="mb-4 pa-3 border rounded">
              <v-row class="align-center" dense no-gutters>
                <!-- Desktop -->
                <v-col cols="12" md="6" class="d-none d-md-block">
                  <v-combobox v-model="song.name" :items="songItems" item-title="title" item-value="id"
                    label="Nombre de la Canción" placeholder="Escribe o selecciona una canción"
                    prepend-inner-icon="mdi-music-note-outline" variant="outlined" density="compact" hide-details="auto"
                    clearable @update:model-value="selection => onSongSelected(selection, index)" />
                </v-col>
                <v-col cols="12" md="4" class="d-none d-md-block">
                  <v-text-field v-model="song.tone" label="Tono" placeholder="Ej: Cm, G, A#"
                    prepend-inner-icon="mdi-music-accidental-sharp" variant="outlined" density="compact"
                    hide-details="auto" clearable readonly />
                </v-col>
                <v-col cols="12" md="2" class="d-none d-md-flex text-right">
                  <v-btn v-if="planificacion.songs.length > 1" icon="mdi-delete-outline" color="error" variant="text"
                    size="small" @click="removeSong(index)" aria-label="Eliminar canción" />
                </v-col>

                <!-- Mobile -->
                <v-col cols="6" class="pr-1 d-block d-md-none">
                  <v-combobox v-model="song.name" :items="songItems" item-title="title" item-value="id" label="Canción"
                    prepend-inner-icon="mdi-music-note-outline" variant="outlined" density="compact" hide-details
                    clearable @update:model-value="selection => onSongSelected(selection, index)" />
                </v-col>
                <v-col cols="5" class="pl-1 pr-1 d-block d-md-none">
                  <v-text-field v-model="song.tone" label="Tono" prepend-inner-icon="mdi-music-accidental-sharp"
                    variant="outlined" density="compact" hide-details clearable readonly />
                </v-col>
                <v-col cols="1" class="text-right pl-1 d-block d-md-none">
                  <v-btn v-if="planificacion.songs.length > 1" icon="mdi-delete-outline" color="error" variant="text"
                    density="comfortable" @click="removeSong(index)" aria-label="Eliminar canción" />
                </v-col>
              </v-row>
              <!-- Debug visual simplificado -->
              <div v-if="song.name" class="mt-1 text-caption">
                <span>
                  Nombre: {{ song.name }}
                </span>
                <span v-if="song.tone" class="ml-4">
                  Tono: {{ song.tone }}
                </span>
              </div>
            </div>

            <v-btn block color="secondary" prepend-icon="mdi-plus" class="mt-2" @click="addSong">
              Añadir Canción
            </v-btn>

            <v-divider class="my-6"></v-divider>

            <v-row>
              <v-col cols="12" class="text-center">
                <v-btn :loading="loading" :disabled="!isFormValid || loading" type="submit" color="primary" size="large"
                  min-width="200">
                  Guardar Planificación
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="4000" location="top center" rounded="pill">
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn icon="mdi-close" variant="text" @click="snackbar.show = false"></v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import axios from 'axios';

const planFormRef = ref(null);
const isFormValid = ref(null);
const loading = ref(false);
const targetPlanMonth = ref(new Date(new Date().getFullYear(), new Date().getMonth(), 1));

const planificacion = ref({
  selectedSunday: null,
  personInCharge: null,
  selectedMusicians: [],
  selectedChoir: [],
  songs: [{ songId: null, name: '', tone: '' }]
});

const snackbar = ref({ show: false, message: '', color: '' });

const monthYearDisplay = (date) => {
  if (!date) return '';
  return date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });
};

const listaPersonasACargo = ref([
  { id: 'p1', name: 'Ana Pérez (Directora Principal)' },
  { id: 'p2', name: 'Pedro Gómez (Director Asistente)' },
]);
const listaMusicos = ref([
  { id: 'm1', name: 'Juan García', instrument: 'Guitarra Acústica' },
  { id: 'm2', name: 'Laura Méndez', instrument: 'Teclado/Piano' },
]);
const listaCoro = ref([
  { id: 'c1', name: 'Elena Ríos (Soprano)' },
  { id: 'c2', name: 'Fernando Díaz (Tenor)' },
]);

// --- SONGS API ---
const allSongs = ref([]);
const apiUrl = import.meta.env.VITE_API_URL || '';
const songsEndpoint = `${apiUrl}/api/v1/songs`;

const songItems = computed(() =>
  allSongs.value.map(song => ({
    title: song.title,
    id: String(song.id),
    originalTonality: song.originalTonality
  }))
);

const getSongDetails = (songId) => {
  if (!songId) return null;
  return allSongs.value.find(song => String(song.id) === String(songId));
};

const fetchSongs = async () => {
  try {
    const res = await axios.get(songsEndpoint);
    if (Array.isArray(res.data)) {
      allSongs.value = res.data.map(song => ({
        ...song,
        id: String(song.id || song._id),
        title: song.title,
        originalTonality: song.originalTonality
      }));
    }
  } catch (e) {
    console.error('Error fetching songs:', e);
    allSongs.value = [];
    snackbar.value = { show: true, message: 'No se pudieron cargar las canciones.', color: 'error' };
  }
};

const onSongSelected = (selection, index) => {
  const songRow = planificacion.value.songs[index];

  if (typeof selection === 'object' && selection !== null) {
    songRow.name = selection.title;
    songRow.songId = selection.id;
    songRow.tone = selection.originalTonality;
  }
  else {
    songRow.songId = null;
    songRow.tone = '';
  }
};


const availableSundaysForSelectedMonth = computed(() => {
  const sundays = [];
  const todayDate = new Date();
  todayDate.setHours(0, 0, 0, 0);
  const year = targetPlanMonth.value.getFullYear();
  const month = targetPlanMonth.value.getMonth();
  const dateIterator = new Date(year, month, 1);
  while (dateIterator.getMonth() === month) {
    if (dateIterator.getDay() === 0) {
      const sundayCandidate = new Date(dateIterator);
      sundayCandidate.setHours(0, 0, 0, 0);
      if (sundayCandidate.getTime() >= todayDate.getTime()) {
        sundays.push({
          text: sundayCandidate.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }),
          value: sundayCandidate.toISOString().split('T')[0]
        });
      }
    }
    dateIterator.setDate(dateIterator.getDate() + 1);
  }
  return sundays;
});

watch(targetPlanMonth, () => {
  planificacion.value.selectedSunday = null;
});

const addSong = () => {
  planificacion.value.songs.push({ songId: null, name: '', tone: '' });
};

const removeSong = (index) => {
  if (planificacion.value.songs.length > 1) {
    planificacion.value.songs.splice(index, 1);
  } else {
    snackbar.value = { show: true, message: 'Debe haber al menos una canción.', color: 'info' };
  }
};

const submitPlanificacion = async () => {
  if (!planFormRef.value) return;
  const { valid } = await planFormRef.value.validate();
  if (valid) {
    loading.value = true;
    console.log('Datos de Planificación a enviar:', JSON.parse(JSON.stringify(planificacion.value)));
    setTimeout(() => {
      loading.value = false;
      snackbar.value = { show: true, message: 'Planificación guardada exitosamente (simulado).', color: 'success' };
    }, 2000);
  } else {
    snackbar.value = { show: true, message: 'Por favor, completa todos los campos requeridos.', color: 'error' };
  }
};

const changeTargetMonth = (increment) => {
  const newDate = new Date(targetPlanMonth.value);
  newDate.setMonth(targetPlanMonth.value.getMonth() + increment, 1);
  targetPlanMonth.value = newDate;
};

const goToCurrentPlanningMonth = () => {
  targetPlanMonth.value = new Date(new Date().getFullYear(), new Date().getMonth(), 1);
};

onMounted(() => {
  fetchSongs();
});
</script>

<style scoped>
.border {
  border: 1px solid rgba(0, 0, 0, 0.12);
}

@media (max-width: 600px) {

  .v-combobox,
  .v-text-field,
  .v-autocomplete,
  .v-select {
    font-size: 0.92rem;
  }

  .text-subtitle-1 {
    font-size: 1rem;
  }

  .v-btn {
    min-height: 40px;
    font-size: 0.9rem;
  }

  .v-chip {
    font-size: 0.75rem;
    margin-right: 4px;
    margin-bottom: 4px;
  }
}
</style>