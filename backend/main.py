from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os 
from dotenv import load_dotenv 


load_dotenv()


from backend.database import engine as sqlalchemy_engine 
from backend import models as sqlalchemy_models 
sqlalchemy_models.Base.metadata.create_all(bind=sqlalchemy_engine) 

# --- Configuración para MongoDB (Canciones) ---
from backend.db_mongo import connect_to_mongo, close_mongo_connection

# --- Routers ---
from backend.routers import usuarios as usuarios_router
from backend.routers import roles as roles_router
from backend.routers import auth as auth_router
from backend.routers import songs as songs_router 
from backend.routers import integrantes as integrantes_router
from backend.routers import pautas as pautas_router
from backend.routers import domingos as domingos_router
from backend.routers import asignaciones as asignaciones_router

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
    lifespan=lifespan ,
    debug=True
)

# Configuración de CORS
origins = [
    "http://localhost:5173",      # Vite dev server
    "http://127.0.0.1:5173",      # Vite dev server (IP)
    "http://localhost:4173",      # Vite preview
    "http://127.0.0.1:4173",      # Vite preview (IP)
    "http://localhost:3000",      # Desarrollo alternativo
    "http://127.0.0.1:3000",      # Desarrollo alternativo (IP)
    os.getenv("FRONTEND_URL_1", "http://localhost:5173"),
    os.getenv("FRONTEND_URL_2", "http://127.0.0.1:5173"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# --- Incluir Routers ---
# Rutas para la gestión de usuarios, roles y autenticación (MySQL)
app.include_router(usuarios_router.router, prefix="/api/v1/usuarios", tags=["Usuarios"])
app.include_router(roles_router.router, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(integrantes_router.router, prefix="/api/v1/integrantes", tags=["Integrantes"])
app.include_router(pautas_router.router, prefix="/api/v1/pautas", tags=["Pautas"])
app.include_router(domingos_router.router, prefix="/api/v1/domingos", tags=["Domingos"])
app.include_router(asignaciones_router.router, prefix="/api/v1/asignaciones", tags=["Asignaciones"])

# Rutas para la gestión de canciones (MongoDB)
app.include_router(songs_router.router, prefix="/api/v1/songs", tags=["Canciones"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido a la API de Gestión de Banda"}

@app.get("/health", tags=["Health"])
async def healthcheck():
    """
    Endpoint para verificar el estado de salud de la API.
    Utilizado por Docker para verificar que el servicio esté funcionando.
    """
    return {"status": "ok", "service": "backend-api", "version": "0.1.0"}

# Si quieres ejecutar directamente con uvicorn (para desarrollo fácil)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)