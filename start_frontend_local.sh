#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Ejecutando script actualizado para iniciar el frontend ===${NC}"
echo -e "${YELLOW}=== Con implementación centralizada de autenticación ===${NC}"

echo -e "${GREEN}=== Limpiando caché y archivos temporales ===${NC}"
cd /Users/matiasvargasmarin/Desktop/music-admin/frontend/music-admin
rm -rf node_modules/.vite
rm -rf dist

echo -e "${GREEN}=== Instalando dependencias del frontend ===${NC}"
npm install

echo -e "${GREEN}=== Compilando el frontend para producción ===${NC}"
npm run build

echo -e "${GREEN}=== Iniciando el servidor de desarrollo del frontend ===${NC}"
echo -e "${YELLOW}Si quieres detener el servidor, presiona Ctrl+C${NC}"
echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}= AUTENTICACIÓN CENTRALIZADA IMPLEMENTADA         =${NC}"
echo -e "${BLUE}= El cierre de sesión ahora debería funcionar bien =${NC}"
echo -e "${BLUE}====================================================${NC}"
npm run dev