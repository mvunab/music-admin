<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
</script>

<style>
html, body, #app, .v-application, .v-application__wrap {
  height: 100%;
  margin: 0;
  padding: 0;
}
.v-main {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
</style>