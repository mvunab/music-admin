#!/bin/zsh

# Obtener la ruta absoluta del directorio donde se encuentra el script
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

echo "Iniciando el servidor backend de FastAPI..."
osascript -e "tell app \"Terminal\" to do script \"cd '${SCRIPT_DIR}' && echo '🚀 Iniciando FastAPI backend...' && uvicorn backend.main:app --reload\""

echo "Iniciando el servidor de desarrollo frontend de Vue.js (Vite)..."
osascript -e "tell app \"Terminal\" to do script \"cd '${SCRIPT_DIR}/frontend/music-admin' && echo '🎨 Iniciando Vue.js frontend...' && npm run dev\""

echo "Los servidores de desarrollo se están iniciando en nuevas ventanas/pestañas de Terminal."
echo "Puede que necesites conceder permisos a Terminal para controlar otras aplicaciones si es la primera vez que usas un script como este."
echo "Recuerda hacer este script ejecutable con: chmod +x start-dev.sh"
