"""
Script para probar la conexión a la base de datos y añadir manualmente la columna rol_musical_id
"""
import sys
import os
from pathlib import Path

# Añadir el directorio raíz del proyecto al PYTHONPATH
root_dir = Path(__file__).resolve().parent
sys.path.append(str(root_dir))

from backend.database import engine
from sqlalchemy import text

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            for row in result:
                print(f"Conexión exitosa: {row}")
            return True
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False

def add_column_manually():
    try:
        with engine.connect() as connection:
            # Verificar si la columna ya existe
            query = text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'asignaciones' 
                AND COLUMN_NAME = 'rol_musical_id'
            """)
            result = connection.execute(query)
            if result.rowcount > 0:
                print("La columna rol_musical_id ya existe en la tabla asignaciones")
                return True
                
            # Añadir la columna
            query = text("""
                ALTER TABLE asignaciones 
                ADD COLUMN rol_musical_id INT UNSIGNED DEFAULT NULL,
                ADD INDEX ix_asignaciones_rol_musical_id (rol_musical_id),
                ADD CONSTRAINT fk_rol_musical FOREIGN KEY (rol_musical_id) REFERENCES roles_musicales(id)
            """)
            connection.execute(query)
            connection.commit()
            print("Columna rol_musical_id añadida correctamente")
            return True
    except Exception as e:
        print(f"Error al añadir la columna: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        add_column_manually()
