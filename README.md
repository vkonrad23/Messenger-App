# Messenger App

Stack:
- Frontend: React + TypeScript + Tailwind (Vite)
- Backend: FastAPI (Python), SQLAlchemy, Alembic
- DB: Postgres
- Dockerized with docker-compose

## Features
- JWT auth (FastAPI OAuth2PasswordBearer)
- One-to-one messages
- Multiple file attachments per message
- Edit and delete own messages

## Quick start

1. Create a `.env` in `backend` (already included for local dev). For production, override secrets via env vars.
2. Run docker compose:

```
pwsh
# from repo root
docker compose up --build
```

- API: http://localhost:8000
- Frontend: http://localhost:5173

## Notes
- Files are served from `/uploads` mounted volume.
- Update `BACKEND_CORS_ORIGINS` if frontend origin changes.
