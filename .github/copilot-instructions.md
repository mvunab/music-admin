# Copilot Instructions for music-admin

## Project Overview

- **music-admin** is a full-stack app for managing a music band, with a FastAPI backend (Python 3.9+) and a Vue 3 frontend (Vite, Node.js 22+).
- Data is stored in MySQL and MongoDB, both managed via Docker Compose for local/dev environments.
- The backend exposes a REST API for users, roles, assignments, Sundays, and more. See `backend/routers/` for endpoints.
- The frontend (in `frontend/music-admin/`) consumes the API and is built with Vue 3 SFCs.

## Architecture & Data Flow

- **Backend**: FastAPI app in `backend/main.py`, with routers in `backend/routers/` and models in `backend/models.py`.
  - Uses SQLAlchemy ORM for MySQL and Pydantic schemas for validation.
  - MongoDB is used for some data (see `backend/db_mongo.py`).
  - Database migrations: Alembic (`backend/migrations/`).
- **Frontend**: Vue 3 app in `frontend/music-admin/`, entrypoint `src/`.
- **Docker Compose**: Orchestrates backend, frontend, MySQL, and MongoDB. See `compose.yaml`.

## Developer Workflows

- **Start all services**: `docker compose up --build`
- **Backend only (dev)**: `cd backend && uvicorn main:app --reload`
- **Frontend only (dev)**: `cd frontend/music-admin && pnpm install && pnpm dev`
- **Run DB scripts**: Use scripts in `backend/utils/` (e.g., `python backend/utils/fix_database.py`)
- **Testing API**: `python backend/utils/test_api.py`
- **Migrations**: Alembic scripts in `backend/migrations/`

## Project Conventions & Patterns

- **Environment variables**: Set in `.env` files for backend and frontend (see root `README.md` for examples).
- **API endpoints**: Grouped by resource in `backend/routers/` (e.g., `usuarios.py`, `roles.py`).
- **Database models**: All in `backend/models.py`.
- **Pydantic schemas**: In `backend/schemas.py` and `backend/schemas_song.py`.
- **Utility scripts**: All in `backend/utils/` (see its `README.md` for details).
- **Volumes**: MySQL and MongoDB data are persisted in Docker volumes.

## Integration Points

- **Frontend ↔ Backend**: Communicate via REST API (CORS enabled in backend config).
- **Backend ↔ MySQL/MongoDB**: Connection URLs set via env vars, see `backend/config.py`.
- **Docker Compose**: Handles service networking and env var injection.

## Examples

- To fix DB structure: `python backend/utils/fix_database.py`
- To check enum consistency: `python backend/utils/enum_checker.py`
- To run all services: `docker compose up --build`

## Key Files & Directories

- `backend/routers/`: API endpoints
- `backend/models.py`: SQLAlchemy models
- `backend/schemas.py`: Pydantic schemas
- `backend/utils/`: Dev and DB scripts
- `frontend/music-admin/`: Vue app
- `compose.yaml`: Service orchestration

---

If any workflow or integration is unclear, check the relevant `README.md` or ask for clarification.
