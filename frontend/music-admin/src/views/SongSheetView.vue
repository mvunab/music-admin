<!-- src/views/SongSheetView.vue -->
<template>
  <v-container class="pa-md-6 pa-3">
    <div v-if="loadingSong" class="text-center py-10">
      <v-progress-circular indeterminate color="primary" size="64" />
      <p class="mt-4">Cargando canción...</p>
    </div>

    <div v-else-if="songError" class="text-center py-10">
      <v-icon size="64" color="error">mdi-alert-circle-outline</v-icon>
      <p class="text-h6 mt-4 text-error">{{ songError }}</p>
      <v-btn color="primary" @click="goBackToRepertorio" class="mt-4">Volver al Repertorio</v-btn>
    </div>

    <v-card v-else-if="song" rounded="xl" class="pa-sm-6 pa-4">
      <v-row align="center" class="mb-4">
        <v-col cols="auto">
          <v-btn icon variant="text" @click="goBackToRepertorio">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
        </v-col>
        <v-col>
          <h1 class="text-h4 font-weight-bold">{{ song.title }}</h1>
          <div class="text-subtitle-1 text-medium-emphasis">
            <v-chip size="small" :color="song.category === 'REP' ? 'blue' : 'green'" label>
              {{ song.category }}
            </v-chip>
            Tono Original: {{ song.originalTonality }}
            <span v-if="song.bpm">| BPM: {{ song.bpm }}</span>
          </div>
        </v-col>
        <v-col cols="12" md="auto" class="text-md-right mt-3 mt-md-0">
          <div class="d-flex ga-3 flex-wrap">
            <v-btn icon color="primary" @click="printSongSheetAdvanced" aria-label="Imprimir">
              <v-icon>mdi-printer-outline</v-icon>
            </v-btn>
            <v-btn v-if="song.youtubeLink" icon color="red" :href="song.youtubeLink" target="_blank" rel="noopener"
              aria-label="YouTube">
              <v-icon>mdi-youtube</v-icon>
            </v-btn>
            <v-btn v-if="song.docsLink" icon color="blue-darken-2" :href="song.docsLink" target="_blank" rel="noopener"
              aria-label="Documento">
              <v-icon>mdi-file-document-outline</v-icon>
            </v-btn>
          </div>
        </v-col>
      </v-row>

      <v-divider class="my-4" />
      <v-row align="center" class="mb-4" dense>
        <v-col cols="12" sm="auto"><span class="text-subtitle-1 mr-2">Tono Actual:</span></v-col>
        <v-col cols="12" sm="4" md="3" lg="2">
          <v-select v-model="currentDisplayTonality" :items="tonalidadesDisponiblesParaSelector"
            label="Seleccionar Tono" density="compact" variant="outlined" hide-details class="tonality-select" />
        </v-col>
        <v-col cols="auto"><v-btn icon="mdi-minus" @click="transposeStep(-1)" size="small" /></v-col>
        <v-col cols="auto"><v-btn icon="mdi-plus" @click="transposeStep(1)" size="small" /></v-col>
        <v-col cols="auto"><v-btn @click="resetTonality" size="small" variant="text">Original</v-btn></v-col>
      </v-row>

      <div id="song-sheet-content" class="song-lyrics-container pa-3">
        <div class="print-header d-none d-print-block mb-4">
          <h2 class="text-h5 print-song-title">{{ song.title }}</h2>
          <p class="text-subtitle-1 print-tonality">Tono: {{ currentDisplayTonality }}</p>
        </div>
        <div class="lyrics-render-area">
          <template v-for="(line, idx) in displayedLyricsWithChords" :key="idx">
            <div v-if="line.type === 'section'" class="section-header-render">{{ line.content }}</div>
            <div v-else-if="line.type === 'chord-line'" class="chords-line-render">{{ line.content }}</div>
            <div v-else-if="line.type === 'lyrics-line'" class="lyrics-line-render">{{ line.content }}</div>
            <div v-else class="empty-line-render"> </div>
          </template>
        </div>
      </div>
    </v-card>

    <div v-else class="text-center py-10">
      <v-icon size="64" color="grey-lighten-1">mdi-music-note-off-outline</v-icon>
      <p class="text-h6 mt-4 grey--text text--darken-1">Canción no encontrada.</p>
      <v-btn color="primary" @click="goBackToRepertorio">Volver al Repertorio</v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { ref, computed, watch, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import * as Transposer from 'chord-transposer'

const props = defineProps({ id: String })
const router = useRouter()
const { proxy } = getCurrentInstance()

const song = ref(null)
const loadingSong = ref(true)
const songError = ref('')
const currentDisplayTonality = ref('')

const API_SONGS_ITEM_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/songs`

const tonalidadesDisponiblesParaSelector = computed(() =>
  ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb'].flatMap(n => [n, n + 'm'])
)

const displayedLyricsWithChords = computed(() => {
  if (!song.value?.lyricsWithChords || !song.value.originalTonality) {
    return [{ type: 'lyrics-line', content: 'Cargando letra...' }]
  }
  const result = Transposer.transpose(song.value.lyricsWithChords)
    .fromKey(song.value.originalTonality)
    .toKey(currentDisplayTonality.value)
    .toString()

  return result.split('\n').map(line => {
    const sec = line.trim().match(/^\[(.+)\]$/)
    if (sec && /^(Verse|Intro|Chorus|Bridge|Estrofa|Coro)/i.test(sec[1])) {
      return { type: 'section', content: sec[1] }
    }
    if (line.trim() === '') return { type: 'empty-line', content: '' }
    if (/^(\s*\[[^\]]+\]\s*)+$/.test(line)) {
      return { type: 'chord-line', content: line.replace(/\[|\]/g, '') }
    }
    return { type: 'lyrics-line', content: line }
  })
})

async function fetchSongDetails() {
  loadingSong.value = true
  songError.value = ''
  try {
    const { data } = await axios.get(`${API_SONGS_ITEM_URL}/${props.id}`)
    song.value = data
    currentDisplayTonality.value = data.originalTonality
  } catch (e) {
    songError.value = e.response?.status === 404 ? 'Canción no encontrada.' : 'Error cargando canción.'
  } finally {
    loadingSong.value = false
  }
}

function transposeStep(step) {
  const res = Transposer.transpose(song.value.lyricsWithChords)
    .fromKey(song.value.originalTonality)
    .toKey(currentDisplayTonality.value)
  const change = res.change
  const trans = Transposer.transpose(song.value.lyricsWithChords)
    .fromKey(song.value.originalTonality)
    .up(change + step)
  currentDisplayTonality.value = trans.key || currentDisplayTonality.value
}

function resetTonality() {
  if (song.value) currentDisplayTonality.value = song.value.originalTonality
}

function goBackToRepertorio() {
  router.push({ name: 'Repertorio' })
}

function printSongSheetAdvanced() {
  const el = document.getElementById('song-sheet-content')
  if (!el) {
    console.error('Elemento "song-sheet-content" no encontrado')
    return
  }
  const prtHtml = el.innerHTML

  let stylesHtml = ''
  document.querySelectorAll('link[rel="stylesheet"], style').forEach(node => {
    stylesHtml += node.outerHTML
  })

  const WinPrint = window.open('', '_blank', 'toolbar=0,scrollbars=1,status=0,left=0,top=0,width=800,height=900')
  WinPrint.document.write(`<!DOCTYPE html>
<html>
  <head>
    ${stylesHtml}
    <style>
      body { background: #fff; color: #000; margin: 20mm; }
      .section-header-render { font-weight: bold; font-size: 1.1em; }
      .chords-line-render { font-weight: bold; color: #000; white-space: pre; }
      .lyrics-line-render { white-space: pre; letter-spacing: 0.01em; font-family: 'Courier New', monospace; }
    </style>
  </head>
  <body>
    ${prtHtml}
  </body>
</html>`)
  WinPrint.document.close()
  WinPrint.focus()
  setTimeout(() => {
    WinPrint.print()
    WinPrint.close()
  }, 200)
}

watch(props, fetchSongDetails, { immediate: true })
</script>

<style scoped>
.song-lyrics-container {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.lyrics-render-area {
  font-family: 'Courier New', monospace;
  font-size: 0.95rem;
  line-height: 1.4;
  color: #333;
  padding: 10px;
  white-space: pre;
}

.section-header-render {
  font-weight: bold;
  margin: 1em 0.5em;
  font-family: Arial;
  font-size: 1.05rem;
  color: #444;
}

.chords-line-render {
  color: #D32F2F;
  font-weight: bold;
  white-space: pre;
  letter-spacing: 0.01em;
}

.lyrics-line-render {
  white-space: pre;
  letter-spacing: 0.01em;
}

.empty-line-render {
  min-height: 1.2em;
}

@media print {
  .section-header-render {
    font-weight: bold;
    font-size: 1.1em;
  }

  .chords-line-render {
    color: #000;
    font-weight: bold;
  }

  body,
  .song-lyrics-container {
    color: #000;
    background: #fff;
  }

  @page {
    size: auto;
    margin: 20mm;
  }
}
</style>
