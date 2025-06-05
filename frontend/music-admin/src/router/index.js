// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import authService from "../services/authService";

// Importa tus vistas
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import BandCalendarView from "../views/BandCalendarView.vue";
import PlanDomingoView from "../views/PlanDomingoView.vue";
import RepertorioView from "../views/RepertorioView.vue";

const routes = [
  {
    path: "/",
    name: "Login",
    component: LoginView,
    meta: { title: "Iniciar Sesión" },
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterView,
    meta: { title: "Crear Cuenta" },
  },
  {
    path: "/calendar",
    name: "BandCalendar",
    component: BandCalendarView,
    meta: { title: "Agenda de Ensayos", requiresAuth: true },
  },
  {
    path: "/plan-domingo",
    name: "PlanDomingo",
    component: PlanDomingoView,
    meta: { title: "Planificar Domingo", requiresAuth: true },
  },
  {
    path: "/repertorio",
    name: "Repertorio",
    component: RepertorioView,
    meta: { title: "Repertorio de Canciones", requiresAuth: true },
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/", // Redirige a la página de login
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || "Gestión de Banda";

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  if (requiresAuth && !authService.isAuthenticated()) {
    // Si la ruta requiere autenticación y el usuario no está autenticado,
    // redirigir al login, guardando la ruta a la que se intentaba acceder.
    next({ name: "Login", query: { redirect: to.fullPath } });
  } else if (
    (to.name === "Login" || to.name === "Register") &&
    authService.isAuthenticated()
  ) {
    // Si el usuario ya está autenticado e intenta ir a Login o Register, redirigirlo al calendario.
    next({ name: "BandCalendar" });
  } else {
    next();
  }
});

export default router;
