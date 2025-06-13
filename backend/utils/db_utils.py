"""
Utilidades para la gestión y verificación de la base de datos.
"""
import os
import pymysql
import sys
from pathlib import Path
from dotenv import load_dotenv

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos MySQL utilizando los valores
    configurados en las variables de entorno.
    
    Returns:
        pymysql.connections.Connection: Conexión a la base de datos MySQL.
    """
    # Cargar variables de entorno
    load_dotenv()
    
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
