## Ejecución con Docker

Este proyecto incluye configuración completa para ejecutarse con Docker y Docker Compose, facilitando el despliegue tanto en desarrollo como en producción.

### Requisitos Específicos

- **Backend:** Python 3.9 (imagen `python:3.9-slim`)
- **Frontend:** Node.js 22.14.0 y pnpm 10.4.1 (ver Dockerfile)
- **Bases de datos:** MySQL y MongoDB (imágenes oficiales)

### Variables de Entorno

Asegúrate de definir las siguientes variables en los archivos `.env` correspondientes:

**Backend (`backend/.env`):**
```env
DATABASE_URL="mysql+pymysql://usuario:contrasena@mysql-db:3306/banda_db"
SECRET_KEY="tu_clave_secreta_para_jwt"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
MONGODB_URI="mongodb://root:example@mongo-db:27017/banda_db"
```

**Frontend (`frontend/music-admin/.env`):**
```env
VITE_API_URL=http://127.0.0.1:8000
```

**Bases de datos:**
- MySQL: credenciales y nombre de base de datos configurados en `docker-compose.yml` (modifica para producción)
- MongoDB: usuario `root`, contraseña `example`, base de datos `banda_db` (modifica para producción)

### Puertos Expuestos

- **Backend (FastAPI):** `8000` (API y documentación)
- **Frontend (Vite Preview):** `4173`
- **MySQL:** `3306`
- **MongoDB:** `27017`

### Instrucciones de Uso

1. **Construir y levantar los servicios:**

   ```bash
   docker compose up --build
   ```

   Esto iniciará los siguientes contenedores:
   - `python-backend`: API FastAPI en `http://localhost:8000`
   - `javascript-music-admin`: Frontend Vue en `http://localhost:4173`
   - `mysql-db`: Base de datos MySQL
   - `mongo-db`: Base de datos MongoDB

2. **Configuración especial:**
   - Los servicios se comunican en la red interna `music-admin-net`.
   - Los datos de MySQL y MongoDB se persisten en volúmenes locales (`mysql-data`, `mongo-data`).
   - Para desarrollo, puedes usar los archivos `.env.example` como referencia.
   - Cambia todas las contraseñas y claves secretas antes de usar en producción.

3. **Acceso a la aplicación:**
   - **Frontend:** `http://localhost:4173`
   - **Backend API:** `http://localhost:8000`
   - **Documentación API:** `http://localhost:8000/docs`

> **Nota:** Si modificas los archivos `.env`, reinicia los contenedores para aplicar los cambios.

---
