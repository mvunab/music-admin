from pydantic_settings import BaseSettings
from pathlib import Path

# Construir la ruta al directorio raíz del proyecto
# __file__ es la ruta a config.py
# .parent es el directorio backend/
# .parent es el directorio raíz del proyecto /Users/matiasvargasmarin/Desktop/backend_banda/
PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = PROJECT_ROOT_DIR / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = DOTENV_PATH
        env_file_encoding = 'utf-8'
        extra = 'ignore' 

def get_settings():
    return Settings()

settings = get_settings()
