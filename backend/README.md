# Backend API (FastAPI)

Este directorio contiene el backend de la API para la aplicación de Gestión de Banda, desarrollado con FastAPI.

## Características del Backend

*   API RESTful para gestionar Usuarios, Integrantes, Roles, Pautas, Domingos y Asignaciones.
*   SQLAlchemy como ORM para interactuar con una base de datos MySQL.
*   Pydantic para la validación de datos y serialización.
*   Generación automática del esquema de base de datos al iniciar (configurable).
*   Documentación interactiva de la API autogenerada por FastAPI (Swagger UI en `/docs` y ReDoc en `/redoc`).
*   Configuración de CORS para permitir la comunicación con el frontend.

## Prerrequisitos Específicos del Backend

*   Python 3.9+
*   `pip` para la gestión de paquetes de Python.
*   Un servidor de base de datos MySQL en ejecución.

## Configuración del Entorno del Backend

1.  **Entorno Virtual (Recomendado)**:
    Asegúrate de tener un entorno virtual de Python creado y activado en la raíz del proyecto (`backend_banda/venv` o similar).

2.  **Instalar Dependencias del Backend**:
    Desde el directorio raíz del proyecto (`backend_banda/`), ejecuta:
    ```bash
    pip install -r backend/requirements.txt
    ```
    O, si estás dentro del directorio `backend/`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar la Base de Datos**:
    *   Crea un archivo `.env` en la raíz del proyecto (`backend_banda/.env`).
    *   Añade la URL de conexión a tu base de datos MySQL. Ejemplo:
        ```env
        DATABASE_URL="mysql+pymysql://TU_USUARIO:TU_CONTRASEÑA@TU_HOST:TU_PUERTO/TU_BASE_DE_DATOS"
        ```
        Reemplaza los placeholders con tus credenciales reales. Por ejemplo:
        `DATABASE_URL="mysql+pymysql://user:password@localhost:3306/banda_db"`
    *   Asegúrate de que la base de datos especificada exista en tu servidor MySQL. La API intentará crear las tablas automáticamente si no existen.

## Ejecutar el Servidor Backend (FastAPI)

Para iniciar solo el servidor de desarrollo FastAPI:

Opción 1: Navega al directorio `backend/` y ejecuta:
```bash
cd backend
uvicorn main:app --reload
```

Opción 2: Desde el directorio raíz del proyecto (`backend_banda/`), ejecuta:
```bash
uvicorn backend.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000` (o el puerto que Uvicorn indique).

*   Documentación interactiva (Swagger UI): `http://127.0.0.1:8000/docs`
*   Documentación alternativa (ReDoc): `http://127.0.0.1:8000/redoc`

## Estructura del Proyecto Backend

```
backend/
├── main.py             # Punto de entrada de la aplicación FastAPI, configuración inicial
├── database.py         # Configuración de la conexión a la base de datos (SQLAlchemy)
├── models.py           # Modelos de datos SQLAlchemy (tablas de la BD)
├── schemas.py          # Esquemas Pydantic para validación y serialización
├── crud.py             # Funciones CRUD para interactuar con la base de datos
├── requirements.txt    # Dependencias del proyecto Python
├── routers/            # Módulo para agrupar los endpoints de la API
│   ├── __init__.py
│   └── usuarios.py     # Endpoints relacionados con usuarios (ejemplo)
├── copilot-instructions.md # (Opcional) Instrucciones para GitHub Copilot
└── README.md           # Este archivo
```

## Próximos Pasos y Mejoras Pendientes (Backend)

*   Implementar completamente los routers para todas las entidades (`integrantes`, `roles`, `pautas`, `domingos`, `asignaciones`).
*   Resolver cualquier problema pendiente con las restricciones de clave externa en MySQL.
*   Añadir autenticación y autorización robustas (por ejemplo, con JWT).
*   Implementar pruebas unitarias e de integración para la API.
*   Mejorar el manejo de errores y validaciones específicas.
*   Considerar la paginación para endpoints que devuelvan listas grandes.
