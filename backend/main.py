from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os 
from dotenv import load_dotenv 


load_dotenv()


from .database import engine as sqlalchemy_engine 
from . import models as sqlalchemy_models 
sqlalchemy_models.Base.metadata.create_all(bind=sqlalchemy_engine) 

# --- Configuración para MongoDB (Canciones) ---
from .db_mongo import connect_to_mongo, close_mongo_connection

# --- Routers ---
from .routers import usuarios as usuarios_router
from .routers import roles as roles_router
from .routers import auth as auth_router
from .routers import songs as songs_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    print("FastAPI application startup: Connections initiated.")
    yield
    await close_mongo_connection()
    print("FastAPI application shutdown: Connections closed.")

app = FastAPI(
    title="API Gestión de Banda",
    description="API para gestionar usuarios, roles, repertorio de canciones y planificación de ensayos.",
    version="0.1.0",
    lifespan=lifespan 
)

# Configuración de CORS
origins = [
    os.getenv("FRONTEND_URL_1", "http://localhost:5173"), # URL de Vite por defecto
    os.getenv("FRONTEND_URL_2", "http://127.0.0.1:5173"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], # Permite todas las cabeceras
)

# --- Incluir Routers ---
# Rutas para la gestión de usuarios, roles y autenticación (MySQL)
app.include_router(usuarios_router.router, prefix="/api/v1/usuarios", tags=["Usuarios"])
app.include_router(roles_router.router, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Autenticación"])

# Rutas para la gestión de canciones (MongoDB)
app.include_router(songs_router.router, prefix="/api/v1/songs", tags=["Canciones"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido a la API de Gestión de Banda"}

# Si quieres ejecutar directamente con uvicorn (para desarrollo fácil)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)