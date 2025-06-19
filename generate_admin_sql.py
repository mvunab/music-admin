"""
Script para generar un SQL que inserta un usuario administrador en la base de datos
"""
from passlib.context import CryptContext
import logging

# Suprimir el warning de passlib/bcrypt
logging.getLogger("passlib").setLevel(logging.ERROR)

# Configuración para hashear contraseñas (igual que en crud.py)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

def get_password_hash(password):
    return pwd_context.hash(password)

# Datos del usuario administrador
nombre = "David Marin"
email = "david.marin@example.com"
password = "david123"

# Generar hash de la contraseña
password_hash = get_password_hash(password)

# Generar SQL
sql = f"""
-- SQL para insertar un usuario administrador
INSERT INTO usuarios (nombre, email, password_hash, rol_plataforma, creado_en) 
VALUES (
    '{nombre}', 
    '{email}', 
    '{password_hash}', 
    'admin', 
    NOW()
);
"""

print(sql)

# Guardar SQL en un archivo
with open('insert_admin.sql', 'w') as f:
    f.write(sql)

print("\nEl SQL ha sido generado y guardado en 'insert_admin.sql'")
