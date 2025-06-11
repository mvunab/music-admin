import { createRouter, createWebHistory } from "vue-router";
import authService from "../services/authService"; 

// Importa las vistas que se cargan inicialmente o son muy comunes
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";

const BandCalendarView = () => import("../views/BandCalendarView.vue");
const PlanDomingoView = () => import("../views/PlanDomingoView.vue");
const RepertorioView = () => import("../views/RepertorioView.vue");
const SongSheetView = () => import("../views/SongSheetView.vue"); 

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
    path: "/song/:id", 
    name: "SongSheet",
    component: SongSheetView,
    props: true, 
    meta: { title: "Hoja de Canción", requiresAuth: true },
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/", 
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || "Gestión de Banda";

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const isAuthenticated = authService.isAuthenticated(); // Llama al método de tu servicio

  if (requiresAuth && !isAuthenticated) {
    // Si la ruta requiere autenticación y el usuario no está autenticado,
    // redirigir al login, guardando la ruta a la que se intentaba acceder.
    next({ name: "Login", query: { redirect: to.fullPath } });
  } else if (
    (to.name === "Login" || to.name === "Register") &&
    isAuthenticated
  ) {
    // Si el usuario ya está autenticado e intenta ir a Login o Register, redirigirlo al calendario.
    next({ name: "BandCalendar" }); 
  } else {
    next(); 
  }
});

export default router;