"""
Script mejorado para añadir o modificar columnas en la base de datos.
"""
import os
import sys
from pathlib import Path

# Añadir el directorio raíz al PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

from dotenv import load_dotenv
load_dotenv()

import pymysql

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos MySQL utilizando los valores
    configurados en las variables de entorno.
    
    Returns:
        pymysql.connections.Connection: Conexión a la base de datos MySQL.
    """
    # Obtener configuración de la base de datos desde variables de entorno
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        raise ValueError("La variable de entorno DATABASE_URL no está configurada")
    
    # Extraer componentes de la URL de la base de datos
    # Formato típico: mysql+pymysql://usuario:contraseña@host:puerto/nombre_db
    parts = DATABASE_URL.replace("mysql+pymysql://", "").split("/")
    db_name = parts[1]
    credentials_host = parts[0].split("@")
    user_pass = credentials_host[0].split(":")
    host_port = credentials_host[1].split(":")
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 3306
    user = user_pass[0]
    password = user_pass[1] if len(user_pass) > 1 else ""
    
    # Conectar a la base de datos
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name
    )
    
    return connection

def execute_query(query, params=None, fetch=True):
    """
    Ejecuta una consulta SQL en la base de datos.
    
    Args:
        query (str): Consulta SQL a ejecutar.
        params (tuple, optional): Parámetros para la consulta SQL. Por defecto es None.
        fetch (bool, optional): Indica si se debe retornar el resultado de la consulta.
            Por defecto es True.
            
    Returns:
        list: Resultado de la consulta si fetch es True, de lo contrario None.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            connection.commit()
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        if not fetch:
            connection.rollback()
        raise
    finally:
        connection.close()

def fix_database_structure():
    """
    Corrige la estructura de la base de datos añadiendo columnas faltantes.
    """
    db_name = os.getenv("DATABASE_URL").replace("mysql+pymysql://", "").split("/")[1]
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # Verificar si la columna rol_plataforma ya existe
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s
                AND TABLE_NAME = 'usuarios'
                AND COLUMN_NAME = 'rol_plataforma'
            """, (db_name,))
            
            column_exists = cursor.fetchone()[0] > 0
            
            if not column_exists:
                print("La columna rol_plataforma no existe. Añadiéndola...")
                # Añadir la columna rol_plataforma
                cursor.execute("""
                    ALTER TABLE usuarios
                    ADD COLUMN rol_plataforma ENUM('admin', 'regular') NOT NULL DEFAULT 'regular'
                """)
                connection.commit()
                print("Columna rol_plataforma añadida con éxito.")
            else:
                print("La columna rol_plataforma ya existe.")
                
            # Verificar si la columna integrante_id ya existe
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s
                AND TABLE_NAME = 'usuarios'
                AND COLUMN_NAME = 'integrante_id'
            """, (db_name,))
            
            column_exists = cursor.fetchone()[0] > 0
            
            if not column_exists:
                print("La columna integrante_id no existe. Añadiéndola...")
                # Añadir la columna integrante_id
                cursor.execute("""
                    ALTER TABLE usuarios
                    ADD COLUMN integrante_id INT UNSIGNED NULL
                """)
                connection.commit()
                print("Columna integrante_id añadida con éxito.")
            else:
                print("La columna integrante_id ya existe.")
        
        print("Actualización de la estructura de la base de datos completada.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    fix_database_structure()
