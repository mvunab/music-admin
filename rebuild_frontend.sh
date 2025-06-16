#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${RED}=== RECONSTRUCCIÓN COMPLETA DEL FRONTEND ===${NC}"
cd /Users/matiasvargasmarin/Desktop/music-admin/frontend/music-admin

echo -e "${YELLOW}=== Eliminando node_modules y caché ===${NC}"
rm -rf node_modules
rm -rf .vite
rm -rf dist
rm -rf package-lock.json

echo -e "${YELLOW}=== Limpiando caché de npm ===${NC}"
npm cache clean --force

echo -e "${GREEN}=== Instalando dependencias desde cero ===${NC}"
npm install

echo -e "${GREEN}=== Compilando el frontend para producción ===${NC}"
npm run build

echo -e "${GREEN}=== Iniciando el servidor de desarrollo ===${NC}"
echo -e "${YELLOW}Si quieres detener el servidor, presiona Ctrl+C${NC}"
npm run dev
