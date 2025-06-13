"""
Script para verificar los valores actuales de rol_plataforma en la base de datos.
"""
import os
import pymysql
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener configuración de la base de datos desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

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

try:
    # Conectar a la base de datos
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name
    )
    
    with connection.cursor() as cursor:
        # Verificar los valores actuales de rol_plataforma
        cursor.execute("""
            SELECT id, nombre, email, rol_plataforma
            FROM usuarios
        """)
        
        rows = cursor.fetchall()
        
        if rows:
            print(f"Se encontraron {len(rows)} usuarios:")
            for row in rows:
                print(f"ID: {row[0]}, Nombre: {row[1]}, Email: {row[2]}, Rol: {row[3]}")
        else:
            print("No se encontraron usuarios.")
            
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals():
        connection.close()
