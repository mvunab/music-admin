# Instrucciones para GitHub Copilot

Este es un proyecto de API backend desarrollado con FastAPI y Python.
El objetivo principal es gestionar el acceso y las modificaciones de las tablas definidas en el archivo `schema.sql`.

## Estructura del Proyecto (Planeada)

- `main.py`: Punto de entrada de la aplicación FastAPI. Contendrá la inicialización de la app y la inclusión de los routers.
- `database.py`: Configuración de la conexión a la base de datos PostgreSQL y utilidades de SQLAlchemy.
- `models.py`: Definiciones de los modelos SQLAlchemy que se mapean a las tablas de `schema.sql`.
- `schemas.py`: Definiciones de los esquemas Pydantic para la validación de datos de entrada y salida de la API.
- `crud.py`: Funciones para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en la base de datos.
- `routers/`: Directorio que contendrá los diferentes routers para cada entidad (usuarios, integrantes, roles, etc.).
  - `usuarios.py`
  - `integrantes.py`
  - `roles.py`
  - `pautas.py`
  - `domingos.py`
  - `asignaciones.py`
- `requirements.txt`: Lista de dependencias de Python.
- `schema.sql`: Esquema de la base de datos.

## Tablas de la Base de Datos (schema.sql)

- `usuarios`: Administradores del sistema.
- `integrantes`: Miembros de la banda.
- `roles`: Roles musicales (ej. Guitarra, Batería, Voz).
- `pautas`: Contenido de las pautas musicales y su tonalidad.
- `domingos`: Información sobre los eventos de los domingos, incluyendo ensayos y líderes.
- `asignaciones`: Asignación de integrantes a roles específicos para un domingo determinado.

## Tareas Principales

1.  **Configurar la conexión a la base de datos** en `database.py`.
2.  **Definir los modelos SQLAlchemy** en `models.py` basados en `schema.sql`.
3.  **Definir los esquemas Pydantic** en `schemas.py` para la validación.
4.  **Implementar las funciones CRUD** en `crud.py` para cada modelo.
5.  **Crear los routers FastAPI** en el directorio `routers/` para exponer los endpoints de la API.
6.  **Ensamblar la aplicación** en `main.py`.

## Consideraciones

- Utilizar SQLAlchemy para la interacción con la base de datos PostgreSQL.
- Utilizar Pydantic para la validación de datos y la serialización.
- Seguir las mejores prácticas de FastAPI para la estructura del proyecto y el diseño de la API.
- Asegurar que cada tabla en `schema.sql` tenga sus correspondientes modelos, esquemas, funciones CRUD y endpoints en la API.
- Prestar atención a las relaciones entre tablas (claves foráneas) y cómo se manejan en los modelos y en la lógica de la API.
