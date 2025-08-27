from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional
from pathlib import Path

# __file__ es la ruta a config.py
# .parent es el directorio backend/
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent  # Directorio raíz del proyecto
DOTENV_PATH = PROJECT_ROOT / ".env"  # Apunta al .env en la raíz

class Settings(BaseSettings):
    DATABASE_URL: str 
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    MONGODB_URI: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=str(DOTENV_PATH),
        env_file_encoding='utf-8',
        case_sensitive=True
    )

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()