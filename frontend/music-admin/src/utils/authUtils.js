/**
 * authUtils.js - Utilidades centralizadas para autenticación
 * 
 * Este archivo contiene funciones comunes para el manejo de la autenticación,
 * centralizado para reutilización en diferentes componentes.
 */

/**
 * Función para cerrar sesión completamente en la aplicación.
 * Elimina todos los datos de sesión y redirige al usuario a la página de inicio.
 */
export function cerrarSesion() {
  console.log("AuthUtils: Iniciando cierre de sesión completo...");
  
  // 1. Eliminar TODOS los datos de localStorage
  localStorage.clear();
  sessionStorage.clear();
  
  // 2. Eliminar todas las cookies (por si acaso)
  document.cookie.split(";").forEach(function(c) {
    document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
  });
  
  // 3. Eliminar cualquier caché de autenticación en memoria
  try {
    if (window.caches) {
      // Intento de limpiar caché si el navegador lo soporta
      caches.keys().then(names => {
        for (let name of names) {
          caches.delete(name);
        }
      });
    }
  } catch (e) {
    console.error("Error limpiando caché:", e);
  }
  
  console.log("AuthUtils: Sesión eliminada completamente");
  
  // 4. Forzar recarga completa y redirección sin usar el historial
  // El pequeño timeout asegura que la limpieza termine antes de la redirección
  setTimeout(() => {
    console.log("AuthUtils: Redirigiendo a página de inicio");
    window.location.replace('/');
  }, 100);
}

/**
 * Función para verificar si el usuario está autenticado.
 * Usa un enfoque más estricto para validar el token JWT.
 * @returns {boolean} - true si el usuario está autenticado, false en caso contrario
 */
export function verificarAutenticacion() {
  try {
    console.log("AuthUtils: Verificando autenticación...");
    const token = localStorage.getItem("user-token");
    
    // Si no hay token, no está autenticado
    if (!token) {
      console.log('AuthUtils: No hay token, usuario no autenticado');
      return false;
    }
    
    // Verificar formato básico del token
    const parts = token.split('.');
    if (parts.length !== 3) {
      console.log('AuthUtils: Token malformado, cerrando sesión...');
      cerrarSesion();
      return false;
    }
    
    // Decodificar y verificar el payload
    let payload;
    try {
      payload = JSON.parse(atob(parts[1]));
    } catch (e) {
      console.error('AuthUtils: Error decodificando token:', e);
      cerrarSesion();
      return false;
    }
    
    // Verificar expiración
    const currentTime = Math.floor(Date.now() / 1000);
    if (!payload.exp || payload.exp < currentTime) {
      console.log('AuthUtils: Token expirado o sin fecha de expiración:', payload.exp, currentTime);
      cerrarSesion();
      return false;
    }
    
    console.log('AuthUtils: Usuario autenticado correctamente');
    return true;
  } catch (error) {
    console.error('AuthUtils: Error crítico verificando autenticación:', error);
    cerrarSesion();
    return false;
  }
}

/**
 * Función para verificar si el usuario tiene privilegios de administrador.
 * Verifica en el token JWT si el usuario tiene el rol de administrador.
 * @returns {boolean} - true si el usuario es administrador, false en caso contrario
 */
export function verificarAdmin() {
  try {
    console.log("AuthUtils: Verificando privilegios de administrador...");
    
    // Primero verificar si el usuario está autenticado
    if (!verificarAutenticacion()) {
      return false;
    }
    
    const token = localStorage.getItem("user-token");
    const parts = token.split('.');
    const payload = JSON.parse(atob(parts[1]));
    
    // Verificar si el usuario tiene el campo 'is_admin' establecido como true
    if (payload.is_admin === true) {
      console.log('AuthUtils: Usuario tiene privilegios de administrador');
      return true;
    }
    
    console.log('AuthUtils: Usuario no tiene privilegios de administrador');
    return false;
  } catch (error) {
    console.error('AuthUtils: Error verificando privilegios de administrador:', error);
    return false;
  }
}
