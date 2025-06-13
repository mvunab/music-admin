#!/bin/bash
# Script para iniciar la aplicación en modo desarrollo

# Función para manejar errores
handle_error() {
  echo "Error: $1"
  exit 1
}

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
  handle_error "Python no está instalado. Por favor instálalo e intenta de nuevo."
fi

# Verificar si el archivo run_app.py existe
if [ ! -f "run_app.py" ]; then
  handle_error "El archivo run_app.py no existe en el directorio actual."
fi

# Mensaje de inicio
echo "=== Iniciando aplicación Music Admin ==="

# Verificar si se quiere usar el script de configuración de desarrollo
if [ "$1" = "--dev" ]; then
  echo "Iniciando en modo desarrollo con verificación de entorno..."
  if [ -f "backend/utils/setup_dev.py" ]; then
    python backend/utils/setup_dev.py
    exit $?
  else
    echo "Advertencia: Script de configuración de desarrollo no encontrado."
    echo "Continuando con el inicio normal..."
  fi
fi
echo "Presiona Ctrl+C para detener el servidor"

# Iniciar el backend
python run_app.py
