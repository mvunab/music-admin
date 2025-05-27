# Punto de entrada principal de la aplicación FastAPI
from fastapi import FastAPI
from database import engine, Base # Importar engine y Base directamente
import models # Importar models directamente

# Importar el router de usuarios
from routers import usuarios

# Crear todas las tablas en la base de datos (si no existen)
# Esto es útil para el desarrollo. Para producción, podrías usar Alembic.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir el router de usuarios
app.include_router(usuarios.router)

# Aquí es donde incluiremos los routers más adelante
# from routers import integrantes, ...
# app.include_router(integrantes.router)
# ...

@app.get("/")
async def root():
    return {"message": "Hola Mundo"}

# Si quieres ejecutar la app directamente con uvicorn desde aquí (para desarrollo):
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
