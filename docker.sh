#!/bin/bash
# Script avanzado para gestionar Docker de la aplicación Music Admin
# Con verificaciones, mensajes verbosos y funciones de comprobación

# Colores para los mensajes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Lista de servicios disponibles
SERVICES_LIST="mysql mongodb backend frontend"
MYSQL_DESC="Base de datos MySQL (puerto 3306)"
MONGODB_DESC="Base de datos MongoDB (puerto 27017)"
BACKEND_DESC="API Backend FastAPI (puerto 8000)"
FRONTEND_DESC="Frontend Vue.js (puerto 80)"

# Comando base (con sudo)
DOCKER_CMD="sudo docker compose"

# Encabezado
print_header() {
  echo -e "${BOLD}${GREEN}════════════════════════════════════════════${NC}"
  echo -e "${BOLD}${GREEN}        MUSIC ADMIN - DOCKER MANAGER        ${NC}"
  echo -e "${BOLD}${GREEN}════════════════════════════════════════════${NC}"
  echo ""
}

# Imprime información sobre el entorno
print_env_info() {
  echo -e "${BLUE}Información del entorno:${NC}"
  echo -e "  ${YELLOW}Sistema:${NC} $(uname -s) $(uname -r)"
  echo -e "  ${YELLOW}Docker:${NC} $(sudo docker --version | head -n 1)"
  echo -e "  ${YELLOW}Docker Compose:${NC} $(sudo docker compose version | head -n 1)"
  echo ""
}

# Comprueba si un servicio está en ejecución
check_service() {
  local service=$1
  local service_name="music_admin_$service"
  
  echo -e "${YELLOW}Verificando $service...${NC}"
  if sudo docker ps --format '{{.Names}}' | grep -q "$service_name"; then
    local status=$(sudo docker inspect --format='{{.State.Status}}' "$service_name")
    local health=""
    
    if sudo docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' "$service_name" 2>/dev/null | grep -q "healthy"; then
      health=" ${GREEN}[healthy]${NC}"
    elif sudo docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}' "$service_name" 2>/dev/null | grep -q "unhealthy"; then
      health=" ${RED}[unhealthy]${NC}"
    fi
    
    echo -e "  ${GREEN}✓${NC} ${BOLD}$service${NC}: ${GREEN}ejecutándose${NC}${health}"
    echo -e "    ${YELLOW}Estado:${NC} $status"
    echo -e "    ${YELLOW}Contenedor:${NC} $service_name"
    
    # Verificar puertos para servicios específicos
    case "$service" in
      mysql)
        echo -e "    ${YELLOW}Puerto:${NC} $(sudo docker port "$service_name" 3306 2>/dev/null || echo 'No publicado')"
        ;;
      mongodb)
        echo -e "    ${YELLOW}Puerto:${NC} $(sudo docker port "$service_name" 27017 2>/dev/null || echo 'No publicado')"
        ;;
      backend)
        echo -e "    ${YELLOW}Puerto:${NC} $(sudo docker port "$service_name" 8000 2>/dev/null || echo 'No publicado')"
        ;;
      frontend)
        echo -e "    ${YELLOW}Puerto:${NC} $(sudo docker port "$service_name" 80 2>/dev/null || echo 'No publicado')"
        echo -e "    ${YELLOW}URL:${NC} http://localhost"
        ;;
    esac
    
    return 0
  else
    echo -e "  ${RED}✗${NC} ${BOLD}$service${NC}: ${RED}no está ejecutándose${NC}"
    return 1
  fi
}

# Verifica todos los servicios
check_all_services() {
  echo -e "${BLUE}Verificando estado de los servicios:${NC}"
  local all_running=true
  
  for service in $SERVICES_LIST; do
    if ! check_service "$service"; then
      all_running=false
    fi
  done
  
  echo ""
  if $all_running; then
    echo -e "${GREEN}${BOLD}✓ Todos los servicios están ejecutándose correctamente${NC}"
    echo -e "${GREEN}La aplicación está disponible en: http://localhost${NC}"
  else
    echo -e "${RED}${BOLD}✗ Algunos servicios no están ejecutándose${NC}"
    echo -e "${YELLOW}Revisa los mensajes anteriores para más detalles${NC}"
  fi
  
  echo ""
}

# Comprueba la conectividad entre servicios
check_connectivity() {
  echo -e "${BLUE}Verificando conectividad entre servicios:${NC}"
  
  # Verificar conectividad backend -> bases de datos
  echo -e "${YELLOW}Conectividad Backend -> MySQL:${NC}"
  sudo docker exec music_admin_backend curl -s --connect-timeout 5 http://mysql:3306 > /dev/null
  if [ $? -eq 52 ]; then  # 52 es el código cuando se rechaza la conexión pero el host está accesible
    echo -e "  ${GREEN}✓${NC} Backend puede conectar con MySQL"
  else
    echo -e "  ${RED}✗${NC} Backend no puede conectar con MySQL"
  fi
  
  echo -e "${YELLOW}Conectividad Backend -> MongoDB:${NC}"
  sudo docker exec music_admin_backend curl -s --connect-timeout 5 http://mongodb:27017 > /dev/null
  if [ $? -eq 52 ]; then
    echo -e "  ${GREEN}✓${NC} Backend puede conectar con MongoDB"
  else
    echo -e "  ${RED}✗${NC} Backend no puede conectar con MongoDB"
  fi
  
  echo -e "${YELLOW}Conectividad Frontend -> Backend:${NC}"
  sudo docker exec music_admin_frontend curl -s --connect-timeout 5 -o /dev/null -w "%{http_code}" http://backend:8000/ > /dev/null
  backend_status=$?
  if [ $backend_status -eq 0 ] || [ $backend_status -eq 52 ]; then
    echo -e "  ${GREEN}✓${NC} Frontend puede conectar con Backend"
  else
    echo -e "  ${RED}✗${NC} Frontend no puede conectar con Backend"
  fi
  
  echo ""
}

# Muestra los logs recientes de un servicio específico
show_service_logs() {
  local service=$1
  local lines=${2:-20}
  
  echo -e "${BLUE}Mostrando últimas $lines líneas de logs para $service:${NC}"
  sudo docker logs --tail="$lines" "music_admin_$service"
  echo ""
}

# Mostrar uso del script
show_usage() {
  echo -e "${BLUE}Uso:${NC} $0 [comando]"
  echo ""
  echo -e "${YELLOW}Comandos disponibles:${NC}"
  echo -e "  ${GREEN}up${NC}          - Inicia todos los contenedores"
  echo -e "  ${GREEN}down${NC}        - Detiene todos los contenedores"
  echo -e "  ${GREEN}restart${NC}     - Reinicia todos los contenedores"
  echo -e "  ${GREEN}build${NC}       - Construye las imágenes de Docker"
  echo -e "  ${GREEN}status${NC}      - Muestra el estado de los contenedores"
  echo -e "  ${GREEN}logs [servicio]${NC} - Muestra los logs (todos o de un servicio específico)"
  echo -e "  ${GREEN}check${NC}       - Verifica la conectividad entre servicios"
  echo -e "  ${GREEN}clean${NC}       - Elimina contenedores, imágenes y volúmenes no utilizados"
  echo -e "  ${GREEN}ps${NC}          - Lista los contenedores en ejecución"
  echo -e "  ${GREEN}bash <servicio>${NC} - Abre una terminal bash en el servicio especificado"
  echo ""
  echo -e "${YELLOW}Servicios disponibles:${NC}"
  echo -e "  ${GREEN}mysql${NC} - $MYSQL_DESC"
  echo -e "  ${GREEN}mongodb${NC} - $MONGODB_DESC"
  echo -e "  ${GREEN}backend${NC} - $BACKEND_DESC"
  echo -e "  ${GREEN}frontend${NC} - $FRONTEND_DESC"
  echo ""
}

# Función principal
main() {
  print_header
  
  # Verificar si se proporcionó un comando
  if [ $# -eq 0 ]; then
    show_usage
    exit 1
  fi
  
  # Procesar comandos
  case "$1" in
    up)
      echo -e "${BLUE}Iniciando contenedores...${NC}"
      echo -e "${YELLOW}Ejecutando:${NC} $DOCKER_CMD up -d"
      $DOCKER_CMD up -d
      
      echo ""
      echo -e "${BLUE}Esperando a que los servicios estén listos...${NC}"
      sleep 5  # Dar tiempo a que los contenedores se inicien completamente
      
      check_all_services
      ;;
      
    down)
      echo -e "${BLUE}Deteniendo contenedores...${NC}"
      echo -e "${YELLOW}Ejecutando:${NC} $DOCKER_CMD down"
      $DOCKER_CMD down
      ;;
      
    restart)
      echo -e "${BLUE}Reiniciando contenedores...${NC}"
      echo -e "${YELLOW}Ejecutando:${NC} $DOCKER_CMD restart"
      $DOCKER_CMD restart
      
      echo ""
      echo -e "${BLUE}Esperando a que los servicios estén listos...${NC}"
      sleep 5
      
      check_all_services
      ;;
      
    build)
      echo -e "${BLUE}Construyendo imágenes de Docker...${NC}"
      echo -e "${YELLOW}Ejecutando:${NC} $DOCKER_CMD build"
      $DOCKER_CMD build
      ;;
      
    status)
      print_env_info
      check_all_services
      ;;
      
    logs)
      if [ -z "$2" ]; then
        echo -e "${BLUE}Mostrando logs de todos los servicios...${NC}"
        echo -e "${YELLOW}Ejecutando:${NC} $DOCKER_CMD logs -f"
        $DOCKER_CMD logs -f
      else
        # Verificar si el servicio especificado es válido
        valid_service=false
        for svc in $SERVICES_LIST; do
          if [ "$svc" = "$2" ]; then
            valid_service=true
            break
          fi
        done
        
        if $valid_service; then
          echo -e "${BLUE}Mostrando logs de $2...${NC}"
          echo -e "${YELLOW}Ejecutando:${NC} sudo docker logs -f music_admin_$2"
          sudo docker logs -f "music_admin_$2"
        else
          echo -e "${RED}Servicio '$2' no reconocido${NC}"
          echo -e "Servicios disponibles: $SERVICES_LIST"
          exit 1
        fi
      fi
      ;;
      
    check)
      print_env_info
      check_all_services
      check_connectivity
      ;;
      
    clean)
      echo -e "${BLUE}Limpiando recursos Docker no utilizados...${NC}"
      
      echo -e "${YELLOW}Deteniendo todos los contenedores...${NC}"
      $DOCKER_CMD down
      
      echo -e "${YELLOW}Eliminando contenedores detenidos...${NC}"
      sudo docker container prune -f
      
      echo -e "${YELLOW}Eliminando imágenes sin usar...${NC}"
      sudo docker image prune -f
      
      echo -e "${YELLOW}Eliminando volúmenes sin usar...${NC}"
      sudo docker volume prune -f
      
      echo -e "${GREEN}Limpieza completada${NC}"
      ;;
      
    ps)
      echo -e "${BLUE}Listando contenedores en ejecución:${NC}"
      sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
      ;;
      
    bash)
      if [ -z "$2" ]; then
        echo -e "${RED}Debe especificar un servicio${NC}"
        echo -e "Ejemplo: $0 bash backend"
        echo -e "Servicios disponibles: $SERVICES_LIST"
        exit 1
      else
        # Verificar si el servicio especificado es válido
        valid_service=false
        for svc in $SERVICES_LIST; do
          if [ "$svc" = "$2" ]; then
            valid_service=true
            break
          fi
        done
        
        if $valid_service; then
          container_name="music_admin_$2"
          echo -e "${BLUE}Abriendo terminal bash en $container_name...${NC}"
          
          # Verificar si el contenedor está ejecutándose
          if sudo docker ps --format '{{.Names}}' | grep -q "$container_name"; then
            sudo docker exec -it "$container_name" bash || sudo docker exec -it "$container_name" sh
          else
            echo -e "${RED}El contenedor $container_name no está en ejecución${NC}"
            exit 1
          fi
        else
          echo -e "${RED}Servicio '$2' no reconocido${NC}"
          echo -e "Servicios disponibles: $SERVICES_LIST"
          exit 1
        fi
      fi
      ;;
      
    *)
      echo -e "${RED}Comando desconocido: $1${NC}"
      show_usage
      exit 1
      ;;
  esac
}

# Ejecutar la función principal con todos los argumentos
main "$@"
