import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import VueHtmlToPaper from 'vue-html-to-paper';  

import './style.css';

const app = createApp(App);
app.use(router);
app.use(vuetify);
app.use(VueHtmlToPaper);  
app.mount('#app');
