import { createRouter, createWebHistory } from "vue-router";
import authService from "../services/authService"; 
import { verificarAutenticacion, verificarAdmin } from "@/utils/authUtils";

// Importa las vistas que se cargan inicialmente o son muy comunes
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";

const BandCalendarView = () => import("../views/BandCalendarView.vue");
const PlanDomingoView = () => import("../views/PlanDomingoView.vue");
const RepertorioView = () => import("../views/RepertorioView.vue");
const SongSheetView = () => import("../views/SongSheetView.vue"); 
const AdminView = () => import("../views/AdminView.vue"); 
const RolesMusicalesView = () => import("../views/RolesMusicalesView.vue");

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
    path: "/admin",
    name: "Admin",
    component: AdminView,
    meta: { 
      title: "Administración de Usuarios", 
      requiresAuth: true,
      requiresAdmin: true 
    },
  },
  {
    path: "/roles-musicales",
    name: "RolesMusicales",
    component: RolesMusicalesView,
    meta: { 
      title: "Roles Musicales", 
      requiresAuth: true 
    },
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

  // Verificar la autenticación antes de cada navegación
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin);
  
  // Usar las funciones centralizadas para verificar autenticación y privilegios de administrador
  const isAuthenticated = verificarAutenticacion();
  const isAdmin = verificarAdmin();
  
  console.log("Estado de autenticación:", isAuthenticated);
  console.log("Es administrador:", isAdmin);

  if (requiresAuth && !isAuthenticated) {
    // Si la ruta requiere autenticación y el usuario no está autenticado
    console.log("Redirigiendo a login: requiere autenticación pero no está autenticado");
    return next({ name: "Login", query: { redirect: to.fullPath } });
  } else if (requiresAdmin && !isAdmin) {
    // Si la ruta requiere privilegios de administrador y el usuario no los tiene
    console.log("Redirigiendo a calendario: requiere privilegios de administrador");
    return next({ name: "BandCalendar" });
  } else if (
    (to.name === "Login" || to.name === "Register") &&
    isAuthenticated
  ) {
    // Si el usuario ya está autenticado e intenta ir a Login o Register
    console.log("Redirigiendo a calendario: ya está autenticado");
    return next({ name: "BandCalendar" }); 
  } else {
    return next(); 
  }
});

export default router;