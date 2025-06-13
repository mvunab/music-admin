"""
Script para verificar la correspondencia entre los valores de RolUsuario en Python y los valores almacenados en la base de datos.
Versión mejorada usando utilidades.
"""
import os
import sys
from pathlib import Path

# Añadir el directorio raíz al PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

from dotenv import load_dotenv
load_dotenv()

# Importar el enum RolUsuario desde el modelo
from backend.models import RolUsuario
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

def check_enum_values():
    """
    Verifica la correspondencia entre los valores del enum RolUsuario
    en Python y los valores almacenados en la base de datos.
    """
    print("Verificando valores del enum RolUsuario...")
    
    # Verificar los valores del enum en Python
    print("\nValores del enum en Python:")
    enum_values = set()
    for role in RolUsuario:
        print(f"  {role.name} = \"{role.value}\"")
        enum_values.add(role.value)
    
    # Verificar la definición del enum en la base de datos
    column_type = execute_query("""
        SELECT COLUMN_TYPE
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'usuarios'
        AND COLUMN_NAME = 'rol_plataforma'
    """)[0][0]
    
    print(f"\nDefinición de la columna rol_plataforma:")
    print(f"  Tipo: {column_type}")
    
    # Verificar los valores actuales en la base de datos
    rows = execute_query("""
        SELECT id, nombre, email, rol_plataforma
        FROM usuarios
    """)
    
    if rows:
        print(f"\nValores actuales en la base de datos:")
        db_values = set()
        for row in rows:
            print(f"  ID: {row[0]}, Nombre: {row[1]}, Email: {row[2]}, Rol: {row[3]}")
            db_values.add(row[3])
        
        print(f"\nValores válidos según el enum: {enum_values}")
        print(f"Valores encontrados en la BD: {db_values}")
        
        # Verificar si todos los valores de la BD están en el enum
        if db_values.issubset(enum_values):
            print("\n✅ Todos los valores en la base de datos coinciden con el enum en Python.")
        else:
            invalid_values = db_values - enum_values
            print(f"\n❌ Algunos valores en la base de datos no coinciden con el enum en Python:")
            for val in invalid_values:
                print(f"  - '{val}' no está definido en el enum RolUsuario")
    else:
        print("No se encontraron usuarios en la base de datos.")

if __name__ == "__main__":
    try:
        check_enum_values()
    except Exception as e:
        print(f"Error: {e}")
