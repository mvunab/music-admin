# Configuración de la conexión a la base de datos PostgreSQL y utilidades de SQLAlchemy
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv() # Carga las variables de entorno desde .env (si existe)

# Actualizar la URL por defecto para que sea un ejemplo de MySQL con PyMySQL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@host:port/database")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
