"""
Configuración específica para el entorno Docker.
"""
from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    # Configuración de la base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:Mati10.-@mysql:3306/music_admin")
    
    # Configuración de MongoDB
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://admin:password@mongodb:27017/music_admin?authSource=admin")
    
    # Configuración de JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    class Config:
        env_file = None  # No utilizamos archivo .env en Docker, las variables vienen del entorno

def get_settings():
    return Settings()

settings = get_settings()
