// src/views/PlanDomingoView.vue
<template>
  <v-container class="pa-md-6 pa-3">
    <v-row>
      <v-col>
        <div class="d-flex justify-space-between align-center mb-6">
          <h1 class="text-h4 font-weight-medium">Planificar Servicio Dominical</h1>
          <v-btn to="/calendar" variant="text" color="primary" prepend-icon="mdi-arrow-left">
            Volver a Agenda
          </v-btn>
        </div>

        <v-row justify="center" align="center" class="mb-6">
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
            <v-row>
              <v-col cols="12">
                <v-select v-model="planificacion.selectedSunday" :items="availableSundaysForSelectedMonth"
                  item-title="text" item-value="value" label="Seleccionar Domingo del Servicio"
                  :hint="availableSundaysForSelectedMonth.length === 0 ? `No hay Domingos futuros disponibles en ${monthYearDisplay(targetPlanMonth)}` : 'Solo se muestran Domingos futuros'"
                  persistent-hint prepend-inner-icon="mdi-calendar-today"
                  :rules="[v => !!v || 'Debe seleccionar un Domingo']" required variant="outlined" clearable
                  :no-data-text="`No hay Domingos futuros en ${monthYearDisplay(targetPlanMonth)}`"></v-select>
              </v-col>

              <v-col cols="12">
                <v-select v-model="planificacion.personInCharge" :items="listaPersonasACargo" item-title="name"
                  item-value="id" label="Seleccionar Persona a Cargo (Director)"
                  prepend-inner-icon="mdi-account-tie-outline"
                  :rules="[v => !!v || 'Debe seleccionar una persona a cargo']" required variant="outlined"
                  clearable></v-select>
              </v-col>

              <v-col cols="12">
                <v-autocomplete v-model="planificacion.selectedMusicians" :items="listaMusicos" item-title="name"
                  item-value="id" label="Seleccionar Músicos" prepend-inner-icon="mdi-guitar-acoustic" multiple chips
                  closable-chips variant="outlined" clearable hint="Selecciona uno o más músicos" persistent-hint>
                  <template v-slot:chip="{ props, item }">
                    <v-chip v-bind="props" :text="item.raw.name"></v-chip>
                  </template>
                  <template v-slot:item="{ props, item }">
                    <v-list-item v-bind="props" :title="item.raw.name" :subtitle="item.raw.instrument"></v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col cols="12">
                <v-autocomplete v-model="planificacion.selectedChoir" :items="listaCoro" item-title="name"
                  item-value="id" label="Seleccionar Miembros del Coro" prepend-inner-icon="mdi-account-group-outline"
                  multiple chips closable-chips variant="outlined" clearable
                  hint="Selecciona uno o más miembros del coro" persistent-hint></v-autocomplete>
              </v-col>
            </v-row>

            <v-divider class="my-6"></v-divider>

            <h2 class="text-h6 mb-4">Canciones</h2>
            <div v-for="(song, index) in planificacion.songs" :key="index" class="mb-4 pa-3 border rounded">
              <v-row align="center" dense>
                <v-col cols="12" md="6">
                  <v-combobox v-model="song.name" :items="listaCancionesSugeridas" label="Nombre de la Canción"
                    placeholder="Escribe o selecciona una canción" prepend-inner-icon="mdi-music-note-outline"
                    variant="outlined" density="compact" hide-details="auto"></v-combobox>
                </v-col>
                <v-col cols="9" md="4">
                  <v-text-field v-model="song.tone" label="Tono" placeholder="Ej: Cm, G, A#"
                    prepend-inner-icon="mdi-music-accidental-sharp" variant="outlined" density="compact"
                    hide-details="auto"></v-text-field>
                </v-col>
                <v-col cols="3" md="2" class="text-right">
                  <v-btn v-if="planificacion.songs.length > 1" icon="mdi-delete-outline" color="error" variant="text"
                    size="small" @click="removeSong(index)" aria-label="Eliminar canción"></v-btn>
                </v-col>
              </v-row>
            </div>

            <v-btn color="secondary" @click="addSong" class="mb-6" prepend-icon="mdi-plus">
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
import { ref, computed, watch } from 'vue';
// import { useRouter } from 'vue-router'; // 

// const router = useRouter();
const planFormRef = ref(null);
const isFormValid = ref(null);
const loading = ref(false);

const targetPlanMonth = ref(new Date(new Date().getFullYear(), new Date().getMonth(), 1));

const planificacion = ref({
  selectedSunday: null,
  personInCharge: null,
  selectedMusicians: [],
  selectedChoir: [],
  songs: [{ name: '', tone: '' }]
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
const listaCancionesSugeridas = ref(['Cuán Grande es Él', 'Sublime Gracia']);


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
  planificacion.value.songs.push({ name: '', tone: '' });
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
    console.log('Datos de Planificación:', JSON.parse(JSON.stringify(planificacion.value)));
    setTimeout(() => {
      loading.value = false;
      snackbar.value = { show: true, message: 'Planificación guardada exitosamente (simulado).', color: 'success' };
      // planFormRef.value.reset(); // Opcional: resetear formulario
      // planificacion.value.songs = [{ name: '', tone: '' }];
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

</script>

<style scoped>
.border {
  border: 1px solid rgba(0, 0, 0, 0.12);
}
</style>