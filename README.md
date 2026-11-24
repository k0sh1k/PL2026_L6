# Smart Home: two FastAPI services (lab 5)

Two independent services:

- `api-gateway` (port 8000): external API, validation, orchestration, resilience.
- `storage` (port 8001): owns device data (in-memory dict).

The gateway calls storage over HTTP with httpx. Details: `docs/architecture.md`.

## Layout

    api-gateway/app/{api,domain,storage}, config.py, main.py
    storage/app/{api,domain,storage},     config.py, main.py
    docs/architecture.md
    scripts/demo.sh

## Setup (each service has its own venv)

    cd storage
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env

    cd ../api-gateway
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env

## Configuration (pydantic-settings, env or .env)

| Service | Variable | Meaning |
|---|---|---|
| storage | ST_HOST, ST_PORT, ST_LOG_LEVEL | bind address, port, log level |
| gateway | GW_HOST, GW_PORT | bind address, port |
| gateway | GW_STORAGE_BASE_URL | address of storage |
| gateway | GW_STORAGE_TIMEOUT_S | timeout of calls to storage |
| gateway | GW_LOG_LEVEL | log level |

Required variables have no defaults: a missing one fails at startup.

## Run (two terminals, storage first)

    cd storage && source .venv/bin/activate && python -m app.main
    cd api-gateway && source .venv/bin/activate && python -m app.main

## API (via gateway)

- `POST /devices` -> 201
- `GET /devices/{id}` -> 200 / 404
- `GET /devices/search?q=...` -> 200
- Errors: 404 not found, 409 duplicate, 422 invalid, 503 storage unavailable.
  Error body: `{"error": "<code>", "detail": "<text>"}`.

## End-to-end demo

    ./scripts/demo.sh

The script runs POST/GET through the gateway, then asks you to stop storage
and shows the 503 response.

## Tests (run inside each service directory)

    cd storage && source .venv/bin/activate && pytest -v
    cd api-gateway && source .venv/bin/activate && pytest -v

Do not run pytest from the repo root: both services have a package named `app`.
