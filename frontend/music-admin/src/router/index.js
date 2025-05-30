// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import BandCalendarView from '../views/BandCalendarView.vue';
import PlanDomingoView from '../views/PlanDomingoView.vue'; 

// Simulación de verificación de autenticación
const isAuthenticated = () => {
  
  return !!localStorage.getItem('user-token'); 
};

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginView,
    meta: { title: 'Iniciar Sesión' }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { title: 'Crear Cuenta' }
  },
  {
    path: '/calendar',
    name: 'BandCalendar',
    component: BandCalendarView,
    meta: { title: 'Calendario de Ensayos', requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*', 
    redirect: '/' 
  },
   {
    path: '/plan-domingo',
    name: 'PlanDomingo',
    component: PlanDomingoView,
    meta: { title: 'Planificar Domingo', requiresAuth: true } 
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Gestión de Banda';

  if (to.meta.requiresAuth && !isAuthenticated()) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;