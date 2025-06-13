"""
Script para iniciar el servidor FastAPI asegurando
que el directorio raíz del proyecto esté en el PYTHONPATH
"""
import sys
import os
from pathlib import Path

# Añadir el directorio raíz del proyecto al PYTHONPATH
root_dir = Path(__file__).resolve().parent
sys.path.append(str(root_dir))

# Iniciar la aplicación con uvicorn
import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
