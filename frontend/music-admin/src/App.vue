<script setup>
// import HelloWorld from './components/HelloWorld.vue' // Comentamos o eliminamos el HelloWorld si no se usa
import UserCreateForm from './components/UserCreateForm.vue';
</script>

<template>
  <div id="app">
    <header>
      <h1>Gestión de Banda</h1>
    </header>
    <main>
      <UserCreateForm />
      <!-- <HelloWorld msg="Vite + Vue" /> --> {/* Comentamos o eliminamos el HelloWorld si no se usa */}
    </main>
  </div>
</template>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

header h1 {
  margin-bottom: 30px;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
