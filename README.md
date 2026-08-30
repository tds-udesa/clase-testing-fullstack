# Clase Testing 2 — Dogs App

Aplicación de ejemplo para la materia y Clase de Testing: permite ver imágenes de perros aleatorias y guardar tus favoritas. El repo tiene dos proyectos independientes:

- **[backend/](backend/)** — API en FastAPI (Python) con SQLite para persistencia.
- **[frontend/](frontend/)** — App en Next.js (React) que consume la API.

## Requisitos

- Python 3.13+ y [uv](https://docs.astral.sh/uv/)
- Node.js y [pnpm](https://pnpm.io/)

## Backend

```bash
cd backend
uv sync
uv run fastapi dev main.py
```

La API queda disponible en `http://localhost:8000/api/v1` (docs en `/api/v1/docs`).

Configuración en `backend/.env`:

```
DATABASE_URL="sqlite+aiosqlite:///./dogs.db"
```

Tests:

```bash
cd backend
uv run pytest
```

## Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

La app queda disponible en `http://localhost:3000`.

Configuración en `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

Tests:

```bash
cd frontend
pnpm test        # unit/integration (Jest)
pnpm exec playwright test   # end-to-end
```

## Endpoints principales

- `GET /dogs/random` — devuelve una imagen de perro aleatoria.
- `GET /dogs/my-dogs` — lista las imágenes guardadas.
- `POST /dogs/save` — guarda una imagen de perro.
