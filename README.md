# FoodGuard

A responsive React + TypeScript frontend for smart food safety monitoring and expiry alerts.

## Start locally

1. Provision PostgreSQL and set `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, and `POSTGRES_PORT`. In `backend`, create a virtual environment, install `requirements.txt`, then run `python manage.py makemigrations users products inventory notifications analytics`, `python manage.py migrate`, and `python manage.py runserver`.
2. In the project root, install packages with `npm install`, then run `npm run dev`.
3. Copy `.env.example` to `.env` if your API is not hosted at the default local address.

## Architecture

- `src/components` — reusable layout and UI primitives
- `src/data` — strongly typed demo domain data
- `src/lib` — small shared utilities
- `src/pages.tsx` / `src/pages-extra.tsx` — routed page views
- `src/App.tsx` — route map and protected-route boundary

Authentication uses short-lived access JWTs and rotating, blacklisted refresh JWTs. Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, a real email backend, and production HTTPS at deployment.

OpenAPI documentation is available at `/api/docs/`, ReDoc at `/api/redoc/`, and the raw schema at `/api/schema/`.

## QR scanning

Authenticated clients submit a multipart `image` to `POST /api/inventory/scan-qr/`. FoodGuard uses OpenCV, then pyzbar as a decoder fallback. QR payloads may be a barcode or JSON with `name`, `brand`, `manufacturing_date`, `expiry_date`, `ingredients`, and `storage_instructions`. On Windows production hosts, install the ZBar runtime for pyzbar fallback support.

## Automated expiry reminders

Run Redis, then start a worker with `celery -A config worker -l info` and the scheduler with `celery -A config beat -l info`. The configured beat job runs daily at 07:00 in `TIME_ZONE`, creates idempotent in-app expiry alerts, and sends email where the user has enabled it. Set `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` for your Redis deployment.

## Inventory API

`/api/inventory/items/` supports authenticated create, list, retrieve, update, and delete operations. It accepts `search`, `expiry_category` (`safe`, `expiring_soon`, `expired`), `storage_location`, `status`, `ordering`, `page`, and `page_size` query parameters. Use `POST /api/inventory/items/{id}/consume/` or `/discard/` to retain lifecycle history. Statistics are available at `GET /api/inventory/stats/`.
