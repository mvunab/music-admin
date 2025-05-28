# Backend API para Gestión de Banda

Este proyecto es una API backend desarrollada con FastAPI para gestionar la información y asignaciones de una banda musical. Utiliza SQLAlchemy como ORM para interactuar con una base de datos MySQL y Pydantic para la validación de datos.

## Características

*   Gestión de Usuarios (con autenticación básica pendiente)
*   Gestión de Integrantes de la banda
*   Gestión de Roles dentro de la banda
*   Gestión de Pautas musicales
*   Gestión de Domingos (eventos o fechas relevantes)
*   Gestión de Asignaciones (quién toca qué, cuándo)
*   Generación automática de esquema de base de datos al iniciar.
*   Documentación interactiva de la API a través de Swagger UI (`/docs`) y ReDoc (`/redoc`).

## Prerrequisitos

*   Python 3.9+
*   Servidor de base de datos MySQL
*   `pip` para la gestión de paquetes de Python

## Configuración del Entorno

1.  **Clonar el repositorio (si aplica):**
    ```bash
    git clone <tu-repositorio-url>
    cd backend_banda
    ```

2.  **Crear y activar un entorno virtual (recomendado):**
    *   Si usas `venv`:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   Si usas `conda`:
        ```bash
        conda create --name banda_env python=3.9
        conda activate banda_env
        ```

3.  **Instalar dependencias:**
    Navega a la carpeta `backend` y luego instala los requisitos:
    ```bash
    cd backend
    pip install -r requirements.txt
    cd .. 
    ```
    O, desde la raíz del proyecto:
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **Configurar la base de datos:**
    *   Crea un archivo `.env` en la raíz del proyecto (`/Users/matiasvargasmarin/Desktop/backend_banda/.env`).
    *   Añade la URL de conexión a tu base de datos MySQL. Ejemplo:
        ```env
        DATABASE_URL="mysql+pymysql://TU_USUARIO:TU_CONTRASEÑA@TU_HOST:TU_PUERTO/TU_BASE_DE_DATOS"
        ```
        Reemplaza `TU_USUARIO`, `TU_CONTRASEÑA`, `TU_HOST`, `TU_PUERTO` y `TU_BASE_DE_DATOS` con tus credenciales reales. Por ejemplo:
        `DATABASE_URL="mysql+pymysql://user:password.-@localhost:3306/banda_db"`
    *   Asegúrate de que la base de datos especificada (`banda_db` en el ejemplo) exista en tu servidor MySQL. La API intentará crear las tablas automáticamente si no existen.

## Ejecutar la Aplicación

Para iniciar el servidor de desarrollo FastAPI:

Opción 1: Navega al directorio `backend` y ejecuta:
```bash
cd backend
uvicorn main:app --reload
```

Opción 2: Desde el directorio raíz del proyecto (`backend_banda`), ejecuta:
```bash
uvicorn backend.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

*   Documentación interactiva (Swagger UI): `http://127.0.0.1:8000/docs`
*   Documentación alternativa (ReDoc): `http://127.0.0.1:8000/redoc`

## Estructura del Proyecto

```
.
├── .env                # Variables de entorno (configuración de BD)
├── .gitignore          # Archivos ignorados por Git
├── backend/            # Contiene toda la lógica de la API
│   ├── main.py         # Punto de entrada de la aplicación FastAPI
│   ├── database.py     # Configuración de la conexión a la BD
│   ├── models.py       # Modelos de datos SQLAlchemy
│   ├── schemas.py      # Esquemas Pydantic
│   ├── crud.py         # Funciones CRUD
│   ├── requirements.txt # Dependencias del proyecto Python
│   ├── routers/        # Módulo para agrupar los endpoints
│   │   ├── __init__.py
│   │   └── usuarios.py # Endpoints para usuarios
│   └── copilot-instructions.md # Instrucciones para Copilot (si aplica)
├── frontend/           # (Placeholder para futuro frontend)
└── README.md           # Este archivo
```

## Próximos Pasos y Mejoras Pendientes

*   Implementar completamente los routers para todas las entidades (`integrantes`, `roles`, `pautas`, `domingos`, `asignaciones`).
*   Resolver cualquier problema pendiente con las restricciones de clave externa en MySQL.
*   Añadir autenticación y autorización (por ejemplo, con JWT).
*   Implementar pruebas unitarias e de integración.
*   Mejorar el manejo de errores y validaciones.
*   Considerar la paginación para endpoints que devuelvan listas grandes.
