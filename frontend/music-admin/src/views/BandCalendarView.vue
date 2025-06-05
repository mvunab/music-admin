// src/views/BandCalendarView.vue
<template>
  <v-container fluid class="pa-md-6 pa-3">
    <v-row>
      <v-col>
        <div class="d-flex justify-space-between align-center mb-4 flex-wrap ga-2">
          <h1 class="text-h4 font-weight-medium">Agenda Semanal</h1>

          <div class="d-flex ga-2 flex-wrap">
            <v-btn to="/plan-domingo" color="secondary" variant="outlined" prepend-icon="mdi-calendar-edit">
              Planificar Domingo
            </v-btn>
            <v-btn to="/repertorio" color="info" variant="outlined" prepend-icon="mdi-music-box-multiple-outline">
              Repertorio
            </v-btn>
            <v-btn @click="logout" color="primary" variant="flat" prepend-icon="mdi-logout">
              Cerrar Sesión
            </v-btn>
          </div>
        </div>

        <v-row justify="center" align="center" class="mb-6">
          <v-btn icon @click="changeMonth(-1)" aria-label="Mes anterior">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <span class="text-h5 mx-4">{{ monthYearDisplay(targetMonth) }}</span>
          <v-btn icon @click="changeMonth(1)" aria-label="Mes siguiente">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
          <v-btn @click="goToCurrentMonth" variant="outlined" class="ml-4" size="small">Mes Actual</v-btn>
        </v-row>

        <div v-if="weeklyEnsayoSlots.length > 0">
          <v-row>
            <v-col v-for="(slot, index) in weeklyEnsayoSlots" :key="index" cols="12" sm="6" md="4" lg="3">
              <v-card class="mb-4 fill-height" rounded="lg" elevation="2"
                :color="slot.sundayEvent.director === '-' ? 'grey-lighten-3' : undefined">
                <v-card-item class="py-3">
                  <div class="text-h6 font-weight-bold text-center mb-1">
                    DOMINGO {{ slot.sunday.getDate() }}
                  </div>
                  <div class="text-subtitle-1 text-center text-medium-emphasis">
                    DIRIGE: {{ slot.sundayEvent.director }}
                  </div>
                </v-card-item>
                <v-divider></v-divider>

                <v-card-text class="py-3">
                  <div class="text-overline mb-1">MÚSICOS:</div>
                  <div v-if="slot.sundayEvent.musicians && slot.sundayEvent.musicians.length > 0">
                    <v-chip v-for="(musician, mIndex) in slot.sundayEvent.musicians" :key="`m-${mIndex}`" size="small"
                      label class="mr-1 mb-1">
                      {{ musician }}
                    </v-chip>
                  </div>
                  <div v-else class="text-caption text-grey">
                    No asignados
                  </div>
                </v-card-text>
                <v-divider></v-divider>

                <v-card-text class="py-3">
                  <div class="text-overline mb-1">CORO:</div>
                  <div v-if="slot.sundayEvent.choir && slot.sundayEvent.choir.length > 0">
                    <v-chip v-for="(choirMember, cIndex) in slot.sundayEvent.choir" :key="`c-${cIndex}`" size="small"
                      label class="mr-1 mb-1">
                      {{ choirMember }}
                    </v-chip>
                  </div>
                  <div v-else class="text-caption text-grey">
                    No asignado
                  </div>
                </v-card-text>
                <v-divider></v-divider>

                <v-card-text class="py-3">
                  <div class="text-overline mb-1">ENSAYO:</div>
                  <div class="text-body-1">
                    LUNES {{ slot.mondayBefore.getDate() }}
                    <span class="text-caption text-grey"> ({{ slot.mondayBefore.toLocaleDateString(undefined, {
                      month:
                        'short'
                    }) }})</span>
                  </div>
                  <div v-if="slot.mondayRehearsal" class="mt-1">
                    <p class="text-caption font-weight-medium">{{ slot.mondayRehearsal.title || 'Ensayo Programado' }}
                    </p>
                    <p v-if="slot.mondayRehearsal.details" class="text-caption">{{ slot.mondayRehearsal.details }}</p>
                    <p v-if="slot.mondayRehearsal.start" class="text-caption">Hora: {{
                      formatTime(slot.mondayRehearsal.start) }}</p>
                  </div>
                  <div v-else class="text-caption text-orange-darken-2 mt-1">
                    (Sin ensayo programado para este Lunes)
                  </div>
                </v-card-text>

                <v-card-actions v-if="slot.sundayEvent.director !== '-' || slot.mondayRehearsal">
                  <v-spacer></v-spacer>
                  <v-btn variant="text" size="small" color="primary" @click="verDetallesSlot(slot)">
                    Detalles
                  </v-btn>
                </v-card-actions>

              </v-card>
            </v-col>
          </v-row>
        </div>
        <div v-else class="text-center pa-10">
          <v-icon size="64" color="grey-lighten-1">mdi-view-grid-off-outline</v-icon>
          <p class="text-h6 mt-4 grey--text text--darken-1">
            No hay semanas de ensayo para mostrar en {{ monthYearDisplay(targetMonth) }}.
          </p>
        </div>
      </v-col>
    </v-row>

    <v-dialog v-model="showDetailsDialog" max-width="500px" scrollable>
      <v-card v-if="selectedSlot" rounded="lg">
        <v-card-title class="text-h6">
          Semana del {{ formatDate(selectedSlot.mondayBefore) }} al {{ formatDate(selectedSlot.sunday) }}
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pt-4">
          <p class="font-weight-bold mb-1">Domingo {{ selectedSlot.sunday.getDate() }}:</p>
          <p><strong>Dirige:</strong> {{ selectedSlot.sundayEvent.director }}</p>
          <p><strong>Músicos:</strong> {{ selectedSlot.sundayEvent.musicians.join(', ') || 'N/A' }}</p>
          <p><strong>Coro:</strong> {{ selectedSlot.sundayEvent.choir.join(', ') || 'N/A' }}</p>

          <v-divider class="my-3"></v-divider>
          <p class="font-weight-bold mb-1">Lunes {{ selectedSlot.mondayBefore.getDate() }}:</p>
          <div v-if="selectedSlot.mondayRehearsal">
            <p><strong>Ensayo:</strong> {{ selectedSlot.mondayRehearsal.title || 'Programado' }}</p>
            <p v-if="selectedSlot.mondayRehearsal.start"><strong>Hora:</strong> {{
              formatTime(selectedSlot.mondayRehearsal.start) }}</p>
            <p v-if="selectedSlot.mondayRehearsal.details"><strong>Detalles:</strong> {{
              selectedSlot.mondayRehearsal.details }}</p>
          </div>
          <p v-else>Sin ensayo programado.</p>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="showDetailsDialog = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/authService';

const router = useRouter();

const targetMonth = ref(new Date(new Date().getFullYear(), new Date().getMonth(), 1));

const monthYearDisplay = (date) => {
  if (!date) return '';
  return date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });
};

function getFirstSundayOfDate(date) {
  const d = new Date(date.getFullYear(), date.getMonth(), 1);
  while (d.getDay() !== 0) {
    d.setDate(d.getDate() + 1);
  }
  return d;
}

const today = new Date();
const firstSundayCurrentMonth = getFirstSundayOfDate(today);
const monday13DaysBeforeFirstSunday = new Date(firstSundayCurrentMonth);
monday13DaysBeforeFirstSunday.setDate(firstSundayCurrentMonth.getDate() - 13);

const formatDateToISOString = (date) => {
  const pad = (num) => (num < 10 ? '0' : '') + num;
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
};

const formatDateToISOStringWithTime = (date, hours, minutes, seconds) => {
  const padH = (num) => (num < 10 ? '0' : '') + num;
  return `${formatDateToISOString(date)}T${padH(hours)}:${padH(minutes)}:${padH(seconds)}`;
};

const exampleEventsForCurrentMonth = [];
if (firstSundayCurrentMonth.getMonth() === today.getMonth()) {
  exampleEventsForCurrentMonth.push({
    id: 'e_curr_dom_1', type: 'sunday_service', date: formatDateToISOString(firstSundayCurrentMonth),
    director: 'Director Actual', musicians: ['Músico Actual 1', 'Músico Actual 2'], choir: ['Corista Actual 1'],
  });
  exampleEventsForCurrentMonth.push({
    id: 'e_curr_lun_1', type: 'monday_rehearsal', date: formatDateToISOString(monday13DaysBeforeFirstSunday),
    title: `Ensayo Lunes (Actual)`, start: formatDateToISOStringWithTime(monday13DaysBeforeFirstSunday, 19, 30, 0),
    details: 'Práctica específica.',
  });
}

const allEnsayos = ref([
  ...exampleEventsForCurrentMonth,
  {
    id: 'sun_jun_01_2025', type: 'sunday_service', date: '2025-06-01',
    director: 'Ana Pérez', musicians: ['Juan G.', 'Luis B.', 'Carlos D.'], choir: ['Sofía S.', 'Mateo T.'],
  },
  {
    id: 'mon_may_19_2025', type: 'monday_rehearsal', date: '2025-05-19',
    title: 'Ensayo General Previo', start: '2025-05-19T19:00:00', details: 'Todo el repertorio del Dom 1 Jun.',
  },
  {
    id: 'sun_jun_08_2025', type: 'sunday_service', date: '2025-06-08',
    director: 'Pedro Gómez', musicians: ['Laura T.', 'Miguel V.'], choir: ['Isabella A.', 'David B.'],
  },
  {
    id: 'mon_may_26_2025', type: 'monday_rehearsal', date: '2025-05-26',
    title: 'Ensayo Voces', start: '2025-05-26T20:00:00', details: 'Armonías y coros.',
  },
  {
    id: 'sun_jun_15_2025', type: 'sunday_service', date: '2025-06-15',
    director: 'Carlos Ruiz', musicians: ['Invitado 1', 'Invitado 2'], choir: [],
  },
]);

const weeklyEnsayoSlots = ref([]);
const showDetailsDialog = ref(false);
const selectedSlot = ref(null);

function getSundaysAndMondays13DaysBefore(year, month) {
  const result = [];
  const date = new Date(year, month, 1);
  while (date.getMonth() === month) {
    if (date.getDay() === 0) {
      const sunday = new Date(date);
      const mondayBefore = new Date(sunday);
      mondayBefore.setDate(sunday.getDate() - 13);
      result.push({ sunday, mondayBefore });
    }
    date.setDate(date.getDate() + 1);
  }
  return result;
}

function loadEnsayoSlots() {
  const year = targetMonth.value.getFullYear();
  const month = targetMonth.value.getMonth();

  const calculatedDateSlots = getSundaysAndMondays13DaysBefore(year, month);
  const populatedSlots = [];

  calculatedDateSlots.forEach(dateSlot => {
    const sundayDateStr = formatDateToISOString(dateSlot.sunday);
    const mondayDateStr = formatDateToISOString(dateSlot.mondayBefore);

    const sundayEventData = allEnsayos.value.find(
      e => e.type === 'sunday_service' && e.date === sundayDateStr
    );

    const mondayRehearsalData = allEnsayos.value.find(
      e => e.type === 'monday_rehearsal' && e.date === mondayDateStr
    );

    populatedSlots.push({
      sunday: dateSlot.sunday,
      mondayBefore: dateSlot.mondayBefore,
      sundayEvent: sundayEventData || { director: '-', musicians: [], choir: [] },
      mondayRehearsal: mondayRehearsalData,
    });
  });
  weeklyEnsayoSlots.value = populatedSlots;
}

const changeMonth = (increment) => {
  const newDate = new Date(targetMonth.value);
  newDate.setMonth(targetMonth.value.getMonth() + increment, 1);
  targetMonth.value = newDate;
};

const goToCurrentMonth = () => {
  targetMonth.value = new Date(new Date().getFullYear(), new Date().getMonth(), 1);
};

watch(targetMonth, () => {
  loadEnsayoSlots();
}, { immediate: true });

const formatDate = (dateInput) => {
  if (!dateInput) return '';
  const date = new Date(dateInput);
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' });
};

const formatTime = (dateInput) => {
  if (!dateInput) return '';
  const date = new Date(new Date(dateInput).toLocaleString());
  return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', hour12: false });
};

const verDetallesSlot = (slot) => {
  selectedSlot.value = slot;
  showDetailsDialog.value = true;
};

const logout = () => {
  authService.logout();
  router.push({ name: 'Login' });
};
</script>

<style scoped>
.fill-height {
  display: flex;
  flex-direction: column;
}

.v-card-item,
.v-card-text,
.v-card-actions {
  flex-grow: 0;
}

.v-card-text+.v-card-text {
  padding-top: 8px;
}

.text-overline {
  color: rgba(0, 0, 0, 0.6);
  line-height: 1.2rem;
  display: block;
}

.v-card-text .text-caption {
  display: block;
  color: rgba(0, 0, 0, 0.7);
}

/* ga-2 es una clase de utilidad de Vuetify para gap: 0.5rem (8px) */
</style>