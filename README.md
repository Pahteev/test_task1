# SmartPlant

Production-oriented MVP for plant watering tracking with AI image classification and Telegram reminders.

## Stack
- Backend: FastAPI, PostgreSQL, SQLAlchemy Async, Alembic, Redis, Celery.
- Frontend: React, TypeScript, Vite, Tailwind, i18next (RU/EN).
- Infra: Docker Compose, Nginx, GitHub Actions CI.

## Architecture
- `backend/app/domain`: entities/contracts.
- `backend/app/application`: use-cases/services.
- `backend/app/infrastructure`: db, repositories, tasks, integrations.
- `backend/app/api`: REST adapters.

## Core features (MVP)
- Registration/login with JWT access+refresh.
- Argon2 password hashing.
- CSRF header check, XSS hardening headers, CORS allowlist, request rate-limit.
- Plant CRUD baseline, watering logs, dynamic `next_watering_date` recalculation.
- Upload image URL and async AI classification via external service.
- Scheduled Celery task for due watering notifications.
- Telegram notification integration with encrypted chat_id storage.
- OpenAPI via FastAPI `/docs`.

## Database entities
- users, plants, plant_images, water_logs, ai_suggestions, telegram_settings, notifications.
- FK relations, indexes for lookup and schedule scans.
- Soft delete + audit fields (`created_at`, `updated_at`, `deleted_at`).

## Local run
```bash
cp .env.example .env
cd docker && docker compose up --build
```

## Tests
```bash
PYTHONPATH=backend pytest backend/tests
```

## Security checklist
- [x] Argon2 password hashing
- [x] Access/refresh JWT
- [x] CSRF token header required for protected endpoints
- [x] CORS explicit origins
- [x] Rate limiting
- [x] Security headers (CSP, no-sniff, frame deny)
- [x] Encrypted Telegram settings
- [ ] Refresh token rotation + blacklist (next iteration)
- [ ] AV scanning for uploaded files (next iteration)

## MVP roadmap
1. Implement full refresh token rotation, revoke endpoint, device sessions.
2. Replace image URL with direct object storage uploads + signed URLs.
3. Add notification channels (email/push) and retry policies.
4. Add richer plant timeline and analytics dashboard.
5. Extend integration tests with ephemeral PostgreSQL/Redis in CI.
