import os
import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al PYTHONPATH
BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.database import engine
from sqlalchemy import inspect
from backend.models import Base

def check_database_structure():
    """Verifica si la estructura de la base de datos coincide con los modelos"""
    try:
        inspector = inspect(engine)
        
        print("[DB] Verificando tablas...")
        
        # Obtener todas las tablas definidas en los modelos
        model_tables = Base.metadata.tables.keys()
        
        # Obtener todas las tablas existentes en la base de datos
        db_tables = inspector.get_table_names()
        
        # Verificar si faltan tablas
        missing_tables = set(model_tables) - set(db_tables)
        if missing_tables:
            print(f"[DB] ⚠️ Tablas faltantes: {missing_tables}")
            return False
        
        print("[DB] ✅ Todas las tablas están presentes")
        return True
        
    except Exception as e:
        print(f"[DB] ❌ Error al verificar la base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    needs_migration = not check_database_structure()
    exit(0 if not needs_migration else 1)