# Sistema de Gestión de Banda

Este proyecto es una aplicación full-stack para gestionar información musical y asignaciones de una banda, construida con FastAPI (backend) y Vue.js (frontend).

## Características Implementadas

- ✅ Autenticación JWT completa
- ✅ Gestión de usuarios y roles
- ✅ Sistema de repertorio musical con:
  - Gestión de canciones (título, categoría, tonalidad)
  - Transposición de acordes
  - Vista de partitura/letra con acordes
  - Impresión de partituras
- ✅ Integración con MongoDB para el repertorio
- ✅ Integración con MySQL para usuarios y roles
- ✅ Interfaz moderna con Vuetify
- ✅ Rutas protegidas en frontend y backend

## Tecnologías

### Backend

- FastAPI
- SQLAlchemy (MySQL)
- PyMongo/Motor (MongoDB)
- JWT para autenticación

### Frontend

- Vue 3
- Vuetify
- Vue Router
- Axios
- Chord-transposer

## Prerrequisitos

- Python 3.9+
- Node.js y npm
- MySQL Server
- MongoDB Atlas (cuenta configurada)

## Configuración del Entorno

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/music-admin.git
   cd music-admin
   ```

2. **Backend (FastAPI)**

   ```bash
   # Crear y activar entorno virtual
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate

   # Instalar dependencias
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend (Vue.js)**

   ```bash
   cd frontend/music-admin
   npm install
   ```

4. **Variables de Entorno**

   Backend (.env):

   ```env
   DATABASE_URL="mysql+pymysql://usuario:contraseña@localhost:3306/banda_db"
   SECRET_KEY="tu_clave_secreta_para_jwt"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   MONGODB_URI="tu_uri_de_mongodb_atlas"
   ```

   Frontend (.env):

   ```env
   VITE_API_URL=http://127.0.0.1:8000
   ```

## Ejecutar la Aplicación

1. **Iniciar Backend:**

   ```bash
   # Desde /backend
   uvicorn main:app --reload
   ```

2. **Iniciar Frontend:**
   ```bash
   # Desde /frontend/music-admin
   npm run dev
   ```

La aplicación estará disponible en:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## Estructura del Proyecto

```
music-admin/
├── backend/
│   ├── routers/           # Endpoints de la API
│   ├── models.py          # Modelos SQLAlchemy
│   ├── schemas.py         # Esquemas Pydantic
│   ├── crud.py           # Operaciones de base de datos
│   └── main.py           # Aplicación FastAPI
├── frontend/
│   └── music-admin/
│       ├── src/
│       │   ├── views/    # Componentes de página
│       │   ├── components/# Componentes reutilizables
│       │   ├── services/ # Servicios API
│       │   └── router/   # Configuración de rutas
│       └── package.json
└── README.md
```

## Desarrollo

### Endpoints API Principales

- `POST /api/v1/auth/token` - Login
- `GET /api/v1/auth/users/me` - Usuario actual
- `GET /api/v1/songs` - Listar canciones
- `POST /api/v1/songs` - Crear canción
- `GET /api/v1/songs/{id}` - Detalles de canción

### Rutas Frontend Principales

- `/` - Login
- `/register` - Registro
- `/calendar` - Calendario de banda
- `/repertorio` - Gestión de repertorio
- `/song/{id}` - Vista de canción
