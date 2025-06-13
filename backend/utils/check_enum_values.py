"""
Script para verificar y asegurar la correspondencia entre valores del enum en Python y la base de datos.
"""
import os
import sys
import time
from pathlib import Path

# Añadir el directorio raíz al path para poder importar módulos de backend
print("Añadiendo directorio al path...")
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

# Cargar variables de entorno
print("Cargando variables de entorno...")
from dotenv import load_dotenv
load_dotenv()

# Obtener configuración de la base de datos desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL: {DATABASE_URL}")

# Importar utilidades de base de datos
from backend.utils.db_utils import execute_query

try:
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

    print(f"Conectando a la base de datos {db_name} en {host}:{port} como {user}")

    # Importar módulos de backend después de ajustar sys.path
    print("Importando módulos de backend...")
    from backend.models import RolUsuario

    # Mostrar valores del enum en Python
    print("Valores del enum en Python:")
    for rol in RolUsuario:
        print(f"  {rol.name} = \"{rol.value}\"")

    # Conectar a la base de datos
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name
    )
    
    with connection.cursor() as cursor:
        # Verificar la definición del enum en la base de datos
        cursor.execute("""
            SHOW COLUMNS FROM usuarios WHERE Field = 'rol_plataforma'
        """)
        column_info = cursor.fetchone()
        
        if column_info:
            print(f"\nDefinición de la columna rol_plataforma:")
            # El tipo estará en la posición 1 del resultado
            column_type = column_info[1]
            print(f"  Tipo: {column_type}")
            
            # Verificar los valores actuales de rol_plataforma
            cursor.execute("""
                SELECT id, nombre, email, rol_plataforma
                FROM usuarios
            """)
            
            rows = cursor.fetchall()
            
            if rows:
                print(f"\nValores actuales en la base de datos:")
                for row in rows:
                    print(f"  ID: {row[0]}, Nombre: {row[1]}, Email: {row[2]}, Rol: {row[3]}")
                
                # Verificar la correspondencia
                valid_values = {rol.value for rol in RolUsuario}
                db_values = {row[3] for row in rows if row[3] is not None}
                
                print(f"\nValores válidos según el enum: {valid_values}")
                print(f"Valores encontrados en la BD: {db_values}")
                
                if db_values - valid_values:
                    print(f"\n⚠️ ADVERTENCIA: Hay valores en la base de datos que no coinciden con el enum en Python:")
                    for invalid_value in db_values - valid_values:
                        print(f"  Valor inválido: \"{invalid_value}\"")
                    
                    # En un entorno real, aquí se podría preguntar al usuario si desea corregir estos valores
                    # Pero para este ejemplo, vamos a imprimir el mapeo que se usaría
                    print("\nMapeo que se usaría para corregir los valores:")
                    value_mapping = {
                        # Aquí definimos cómo mapear valores inválidos a válidos
                        # Por ejemplo, si hubiera un "REGULAR" (mayúscula) en la BD y necesitáramos cambiarlo a "regular":
                        "REGULAR": "regular",
                        "ADMIN": "admin"
                    }
                    for old_value, new_value in value_mapping.items():
                        if old_value in db_values:
                            print(f"  '{old_value}' → '{new_value}'")
                else:
                    print("\n✅ Todos los valores en la base de datos coinciden con el enum en Python.")
            else:
                print("No se encontraron usuarios.")
        else:
            print("No se encontró la columna rol_plataforma.")
            
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals():
        connection.close()
